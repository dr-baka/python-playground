from django.shortcuts import render
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from master.settings import VENV_PATH
import json
import os
import subprocess
import shutil
import datetime

class Parser:
    
    def data(self, request):
        try: body = json.loads(request.body) 
        except: body = request.POST.dict()
        
        return body


    def ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        
        return ip


parser = Parser()

def home(request, *args, **kwargs):
    return render(request, 'home.html')

@csrf_exempt
def index(request, *args, **kwargs):
    session_name = kwargs.get('session_name', 'default_session')
    # Get the code from the request data
    body = parser.data(request)
    code = body.get('code', '# put your code here \n')
    results = ''
    if request.method == 'POST':
        # Create a temporary directory for the virtual environment
        venv_dir = os.path.join(VENV_PATH, session_name)
        os.makedirs(venv_dir, exist_ok=True)
        last_activity_file = os.path.join(VENV_PATH, 'last_activity.json')

        # Create virtual environment
        if not os.path.exists(os.path.join(venv_dir, 'bin')):
            subprocess.run(['python', '-m', 'venv', venv_dir], check=True)
        
        # Read existing activity data if the file exists
        activity = {}
        
        if not os.path.exists(last_activity_file):
            with open(last_activity_file, 'w') as f:
                json.dump(activity, f, indent=2)
                f.close()
                
        with open(last_activity_file, 'r') as f:
            try:
                activity = json.load(f)
            except json.JSONDecodeError:
                # Handle the case where the file is not valid JSON
                activity = {}
            f.close()

            # Record the current time as the last activity
            activity[venv_dir] = datetime.datetime.utcnow().isoformat()

            # Write the updated activity data back to the file
            with open(last_activity_file, 'w') as f:
                json.dump(activity, f, indent=2) 
                f.close()
            
                    
                
        
        # Path to the Python executable in the virtual environment
        python_exec = os.path.join(venv_dir, 'bin', 'python')

        # Install any required packages if necessary
        # For example, subprocess.run([python_exec, '-m', 'pip', 'install', 'some_package'])

        
        
        # Save the code to a temporary file
        code_file = os.path.join(venv_dir, 'script.py')
        with open(code_file, 'w') as file:
            file.write(code)
        
        try:
            # Run the code in the virtual environment
            result = subprocess.run([python_exec, code_file], capture_output=True, text=True, check=True)
            results = result.stdout
        except subprocess.CalledProcessError as e:
            results = f"Error: {e.stderr}"
        
    
    return render(request, 'index.html', context={
        'session_name': session_name,
        'code': code, 
        'results': results
    })


@csrf_exempt
def install(request, *args, **kwargs):
    body = parser.data(request)
    session_name = body.get('venv_name', 'default_session')
    
    # Create a temporary directory for the virtual environment
    venv_dir = os.path.join(VENV_PATH, session_name)
    os.makedirs(venv_dir, exist_ok=True)
    last_activity_file = os.path.join(VENV_PATH, 'last_activity.json')

    # Create virtual environment
    if not os.path.exists(os.path.join(venv_dir, 'bin')):
        subprocess.run(['python3.10', '-m', 'venv', venv_dir], check=True)
    
    # Read existing activity data if the file exists
    activity = {}
    if not os.path.exists(last_activity_file):
        with open(last_activity_file, 'w') as f:
            json.dump(activity, f, indent=2)
            f.close()
            
    with open(last_activity_file, 'r') as f:
        try:
            activity = json.load(f)
        except json.JSONDecodeError:
            # Handle the case where the file is not valid JSON
            activity = {}
        f.close()

        # Record the current time as the last activity
        activity[venv_dir] = datetime.datetime.utcnow().isoformat()

        # Write the updated activity data back to the file
        with open(last_activity_file, 'w') as f:
            json.dump(activity, f, indent=2)
            f.close()
    
    # Path to the Python executable in the virtual environment
    python_exec = os.path.join(venv_dir, 'bin', 'python') 

    # Install any required packages if necessary
    try:
        # Run the code in the virtual environment
        pip_name = body.get('pip_name', '')
        result = subprocess.run([python_exec, '-m', 'pip', 'install', pip_name])
        return JsonResponse({
            'is_error': False,
            'message': f'{pip_name} successfully installed'
        })
    except subprocess.CalledProcessError as e:
        return JsonResponse({
            'is_error': True,
            'message': f'{pip_name} failed installed'
        })

@csrf_exempt
def delete(request, *args, **kwargs):
    
    if request.method != 'DELETE':
        return JsonResponse({
            'is_error': True,
            'message': f'method "{request.method}" not allowed'
        }, status=405)
    
    session_name = kwargs.get('session_name', 'default_session')
    
    venv_dir = os.path.join(VENV_PATH, session_name)
    last_activity_file = os.path.join(VENV_PATH, 'last_activity.json')

    # Create virtual environment
    if os.path.exists(venv_dir):
        shutil.rmtree(venv_dir)
    
    # Read existing activity data if the file exists
    activity = {}
    if not os.path.exists(last_activity_file):
        with open(last_activity_file, 'w') as f:
            json.dump(activity, f, indent=2)
            f.close()
            
    with open(last_activity_file, 'r') as f:
        try:
            activity = json.load(f)
        except json.JSONDecodeError:
            # Handle the case where the file is not valid JSON
            activity = {}
        f.close()

        # Record the current time as the last activity
        activity.pop(venv_dir)

        # Write the updated activity data back to the file
        with open(last_activity_file, 'w') as f:
            json.dump(activity, f, indent=2)
            f.close()
    

    return JsonResponse({
        'is_error': True,
        'message': 'success'
    })
    