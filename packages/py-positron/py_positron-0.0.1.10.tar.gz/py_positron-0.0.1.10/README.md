# PyPositron

**PyPositron** is a Python-powered desktop app framework that lets you build cross-platform apps using HTML, CSS, and Python—just like Electron, but with Python as the backend. Write your UI in HTML/CSS, add interactivity with Python, and run your app natively!


## Features

- Build desktop apps using HTML and CSS.
- Use Python for backend logic.
- Virtual environment support.
- Effecient installer creation for easy distribution 
(the installer automatically finds an existing browser instead of installing a new one for every app like Electron.JS).


## Quick Start

### 1. Create a New Project
Install PyPositron if not already installed:
```bash
pip install py-positron 
```
Them create a new project using the CLI:
```bash
positron create
# Follow the prompts to set up your project
cd <your_app_name>
```

### 2. Run Your App

```bash
positron start
```

### 3. Install Python Packages

```bash
positron install <package>
```

### 4. Create a Virtual Environment

```bash
positron venv
```

## Example Project Structure

```
your_app/
├── main
│   └── main.py
├── views/
│   └── index.html
├── [win/linux]venv/
│   └──[bin/Scripts]/
│       ├── activate
│       ├── python.exe
│       └── ...
├──LICENSE
└── ...
```

- **main_app.py**: Entry point for your app. 
- **views/index.html**: Your app's UI (HTML/CSS/inline Python). 
- **winvenv/** or **linuxvenv/**:: (Optional) Virtual environment for dependencies. 


## Example: Hello World App

**main_app.py**
```python
import py_positron as main

# Run this file by typing 'positron start' in your project root.
main.openUI("views/index.html", None, 900, 700, title="Example app") #openUI opens a UI and starts automatically
print("Stopping...") #This runs after the app is closed
```

**views/index.html**
```html
<!DOCTYPE html>
<html>
<head>
    <title>Python-Powered App</title>
</head>
<body>
    <h1>Hello from PyPositron!</h1>
    <button id="button">Show Time</button>
<py>
import time
button = document.getElementById('button')
def button_handler():
    document.alert("The current time is " + str(time.strftime("%H:%M:%S")))
button.addEventListener('click', button_handler)
</py>
<!--<script>
    //You can also use JavaScript if you want.
</script>-->
</body>
</html>
```

## CLI Commands

| Command                         | Description                                              |
|---------------------------------|----------------------------------------------------------|
| `positron create`               | Create a new PyPositron project (interactive setup).     |
| `positron start`                | Run your PyPositron app from the project root.           |
| `positron install <package>`    | Install a Python package into the project venv.          |
| `positron venv`                 | Create a virtual environment inside your project folder. |


## Documentation & Resources

- [Official Tutorial & Docs](https://github.com/itzmetanjim/py-positron/wiki)

## License

GNU AGPL v3 License. See [LICENSE](LICENSE) for details.