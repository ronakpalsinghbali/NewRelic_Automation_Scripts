import os
import subprocess
import json

APP_ENTRY_FILE = "app.js"  # Change this to your application's entry file

def run_command(command):
    """Run a system command and check for errors."""
    result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
    if result.stderr:
        print(result.stderr)

def uninstall_newrelic():
    """Uninstall New Relic using npm."""
    run_command("npm uninstall newrelic")

def delete_newrelic_file():
    """Delete newrelic.js from the root directory."""
    dst = 'newrelic.js'
    if os.path.exists(dst):
        os.remove(dst)
        print(f'Deleted {dst}')
    else:
        print(f'{dst} not found.')

def update_package_json():
    """Update package.json to remove New Relic from the start script."""
    with open('package.json', 'r') as file:
        package_json = json.load(file)
    if 'scripts' in package_json and 'start' in package_json['scripts']:
        # Only remove the New Relic reference if it's part of the start script
        start_script = package_json['scripts']['start']
        if 'node -r newrelic' in start_script:
            package_json['scripts']['start'] = start_script.replace('-r newrelic ', '')
    with open('package.json', 'w') as file:
        json.dump(package_json, file, indent=2)
    print('Updated package.json to remove New Relic.')

def main():
    try:
        uninstall_newrelic()
        delete_newrelic_file()
        update_package_json()
        print("New Relic removal completed.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
