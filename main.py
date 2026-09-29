import pystray
from pystray import MenuItem as item, Menu
from PIL import Image
import webbrowser
import subprocess
import os
import sys
import pathlib
import json
import tkinter as tk
from tkinter import messagebox

def resource_path(relative_path):
    return str(pathlib.Path(__file__).parent / relative_path)

def report_error(message):
    print("Error:", message)
    try:
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("OGT", message)
        root.destroy()
    except tk.TclError:
        pass

def run_command(command):
    try:
        subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception as e:
        print("Error running command:", e)

def open_webpage(page):
    if isinstance(page, str) and page.lower().startswith(("http://", "https://")):
        webbrowser.open(page)
    else:
        print("Blocked non-web URL:", page)

def restart_app(icon):
    icon.stop()
    python = sys.executable
    script = os.path.abspath(__file__)
    subprocess.Popen([python, script])    
    sys.exit()

def quit_app(icon):
    icon.stop()

def show_confirmation_dialog(config):
    try:
        message = config.get('confirm_message', f"Are you sure you want to execute '{config.get('name', 'this item')}'?")
        
        root = tk.Tk()
        root.withdraw()
        result = messagebox.askyesno("OGT", message)
        root.destroy()
        return result
    except tk.TclError as e:
        print(f"Error: Failed to show confirmation dialog: {str(e)}")
        return False

REQUIRED_KEY = {'webpage': 'url', 'command': 'command', 'function': 'function'}
FUNCTIONS = {'restart': restart_app, 'quit': quit_app}

def create_menu_item(config):
    if not isinstance(config, dict):
        print(f"Skipping invalid menu entry (expected an object): {config!r}")
        return None

    entry_type = config.get('type')
    if entry_type == 'separator':
        return Menu.SEPARATOR

    name = config.get('name')
    if not isinstance(name, str) or not name:
        print(f"Skipping menu entry without a valid 'name': {config!r}")
        return None

    if 'submenu' in config:
        entries = config['submenu']
        if not isinstance(entries, list):
            print(f"Skipping '{name}': 'submenu' must be a list")
            return None
        submenu_items = [m for m in map(create_menu_item, entries) if m is not None]
        if not submenu_items:
            print(f"Skipping '{name}': submenu has no valid entries")
            return None
        return item(name, Menu(*submenu_items))

    required = REQUIRED_KEY.get(entry_type)
    if required is None:
        print(f"Skipping '{name}': unknown or missing type {entry_type!r}")
        return None
    if required not in config:
        print(f"Skipping '{name}': type '{entry_type}' requires '{required}'")
        return None

    if entry_type == 'webpage':
        run = lambda icon: open_webpage(config['url'])
    elif entry_type == 'command':
        run = lambda icon: run_command(config['command'])
    else:  # 'function'
        function_name = config['function']
        run = FUNCTIONS.get(function_name) if isinstance(function_name, str) else None
        if run is None:
            print(f"Skipping '{name}': unknown function {function_name!r}")
            return None

    if config.get('confirm', False):
        return item(name, lambda icon, _item: run(icon) if show_confirmation_dialog(config) else None)
    return item(name, lambda icon, _item: run(icon))

def load_preset(preset_path):
    try:
        with open(preset_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: Preset '{preset_path}' not found.")
    except (OSError, json.JSONDecodeError) as e:
        print(f"Error: Could not read preset '{preset_path}': {e}")
    return None

def save_config(config, config_path):
    os.makedirs(os.path.dirname(config_path), exist_ok=True)
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=4)
    
def get_default_config():
    name = "win_config.json" if sys.platform == "win32" else "linux_config.json"
    return load_preset(resource_path(os.path.join("presets", name)))

def get_config_path():
    if sys.platform == "win32":
        appdata = os.getenv("APPDATA")
        if not appdata:
            return None
        return os.path.join(appdata, "OGT", "config.json")
    return os.path.expanduser("~/.config/ogt/config.json")

def load_config(config_path):
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Creating default configuration at {config_path}...")
        default_config = get_default_config()
        if default_config is None:
            report_error("No configuration found and no default preset could be loaded.")
            return None
        try:
            save_config(default_config, config_path)
        except OSError as e:
            print(f"Warning: Could not save default config to '{config_path}': {e}")
        return default_config
    except json.JSONDecodeError as e:
        report_error(f"Invalid JSON in '{config_path}':\n{e}")
        return None
    except OSError as e:
        report_error(f"Could not read '{config_path}':\n{e}")
        return None
        
def start_tray():
    icon_path = resource_path("icon.ico")
    try:
        icon_image = Image.open(icon_path)
    except OSError as e:
        report_error(f"Could not load icon '{icon_path}':\n{e}")
        return

    config_path = get_config_path()
    if config_path is None:
        report_error("Could not find the configuration folder (APPDATA is not set).")
        return

    config = load_config(config_path)
    if config is None:
        return

    if not isinstance(config, list):
        report_error(f"'{config_path}' must contain a JSON list of menu entries.")
        return

    menu_items = [m for m in map(create_menu_item, config) if m is not None]
    if not menu_items:
        report_error(f"No valid menu entries found in '{config_path}'.")
        return

    icon = pystray.Icon("test_icon", icon_image, "OGT", menu=Menu(*menu_items))    
    icon.run()

if __name__ == "__main__":
    start_tray()