# Django Python Playground

## Overview

This Django project provides a web-based Python playground where users can run Python scripts in isolated environments. The playground is designed for experimentation, learning, and testing Python code with custom environments.

## Features

### 1. Pip Package Installation
- Users can install Python packages within their session.
- Each session has a separate environment, allowing for customized setups tailored to specific projects or experiments.

### 2. Session Management
- **Active Sessions**: Each session remains active for 60 minutes after the last user interaction. If the browser is closed, the session will stay active for 30 minutes before expiring.
- **Inactivity Handling**: If the user remains on the page without any activity for 30 minutes, the session will expire.

### 3. Isolated Environments
- A unique session ID is generated for each user session.
- The session ID is used to create a virtual environment, ensuring that scripts and package installations in one session do not interfere with others.

## Usage

1. **Start a Session**: Open the playground in your browser to start a new session.
2. **Install Packages**: Use pip to install any Python packages you need within your session.
3. **Run Python Scripts**: Execute your Python code in the isolated environment.
4. **Session Expiry**: Keep track of your session time. The session will expire after 60 minutes of inactivity or 30 minutes if the browser is closed.

## Credits

This project uses the following open-source libraries:
- [Monaco Editor](https://microsoft.github.io/monaco-editor/): A powerful code editor for providing syntax highlighting and code completion.
- [jQuery](https://jquery.com/): A fast, small, and feature-rich JavaScript library.
- [Font Awesome](https://fontawesome.com/): Provides a vast collection of icons for use in web applications.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
