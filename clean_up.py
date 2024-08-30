import json
import os
import shutil
from datetime import datetime, timedelta
# Path to your JSON file
json_file_path = os.path.join(os.getcwd(), 'venvs/last_activity.json')

# Function to delete files if the current time is greater than the timestamp
def delete_expired_files(json_file_path):
    try:
        # Load JSON data from the file
        with open(json_file_path, 'r') as file:
            data = json.load(file)
        
        # Get the current time
        now = datetime.utcnow()
        
        # Iterate over the items in the JSON data
        for file_path, timestamp in data.items():
            # Parse the timestamp
            file_time = datetime.fromisoformat(timestamp)
            
            # Check if the current time is greater than the file timestamp
            print(f'------------------------- {now} -------------------------')
            if now > (file_time + timedelta(hours=1)):
                # Delete the file if it exists
                if os.path.exists(file_path):
                    shutil.rmtree(file_path)
                    print(f"{datetime.now()} | Deleted: {file_path}")
                else:
                    print(f"{datetime.now()} | File not found: {file_path}")
    
    except Exception as e:
        print(f"{datetime.now()} | An error occurred: {e}")

# Call the function
delete_expired_files(json_file_path)
