import os
import subprocess
import json
import shutil
import platform


# Variables
APP_NAME = "Ronak-APN-ToDo-APP-1"
LICENSE_KEY = "19b39ad8f492b8deecdd4135a9534e9fc78dNRAL"
APP_ENTRY_FILE = "Server.js"
OS = "Windows"

def run_command(command):
    """Run a system command and check for errors."""
    result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
    if result.stderr:
        print(result.stderr)

def install_newrelic():
    """Install New Relic using npm."""
    run_command("npm install newrelic")

def copy_newrelic_file():
    """Copy newrelic.js from node_modules to the root directory."""
    src = os.path.join('node_modules', 'newrelic', 'newrelic.js')
    dst = 'newrelic.js'
    if os.path.exists(src):
        if platform.system() == "Windows":
            shutil.copy(src, dst)
        else:
            os.system(f'cp {src} {dst}')
        # if OS == "Windows":
        #     shutil.copy(src, dst)
        # elif OS == "Linux":
        #     os.system(f'cp {src} {dst}')
        print(f'Copied {src} to {dst}')
    else:
        print(f'{src} not found.')

def edit_newrelic_file():
    """Edit newrelic.js to include the app name and license key."""
    with open('newrelic.js', 'r') as file:
        content = file.read()
    content = content.replace("app_name: ['My Application']", f"app_name: ['{APP_NAME}']")
    content = content.replace("license_key: 'license key here'", f"license_key: '{LICENSE_KEY}'")
    with open('newrelic.js', 'w') as file:
        file.write(content)
    print('Edited newrelic.js with app name and license key.')

def update_package_json():
    """Update package.json to include New Relic in the start script."""
    with open('package.json', 'r') as file:
        package_json = json.load(file)
    package_json.setdefault('scripts', {})
    package_json['scripts']['start'] = f'node -r newrelic {APP_ENTRY_FILE}'
    with open('package.json', 'w') as file:
        json.dump(package_json, file, indent=2)
    print('Updated package.json to include New Relic.')

def main():
    try:
        install_newrelic()
        copy_newrelic_file()
        edit_newrelic_file()
        update_package_json()
        print("New Relic setup completed.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
