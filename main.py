import pystray
from pystray import MenuItem as item, Menu
from PIL import Image
import webbrowser
import subprocess
import platform
import time
import os
import sys
import pathlib
import json
import tkinter as tk
from tkinter import messagebox

def resource_path(relative_path):
    return str(pathlib.Path(__file__).parent / relative_path)

def run_command(command):
    try:
        # subprocess.run(command, check=True)
        subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    except Exception as e:
        print("Error running command:", e)

def open_webpage(page):
    webbrowser.open(page)

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
        # use this default if message is not provide
        message = config.get('confirm_message', f"Are you sure you want to execute '{config['name']}'?")
        
        root = tk.Tk()
        root.withdraw()
        result = messagebox.askyesno("OGT", message)
        root.destroy()
        return result
    except tk.TclError as e:
        print(f"Error: Failed to show confirmation dialog: {str(e)}")
        return False

def create_menu_item(config):
    if 'submenu' in config:
        submenu_items = [create_menu_item(sub_item) for sub_item in config['submenu']]
        return item(config['name'], Menu(*submenu_items))
    else:
        action = None
        confirm_required = config.get('confirm', False)
                
        match config['type']:
            case 'webpage':
                if confirm_required:
                    action = lambda icon, item: open_webpage(config['url']) if show_confirmation_dialog(config) else None
                else:
                    action = lambda icon, item: open_webpage(config['url'])
            case 'command':
                if confirm_required:
                    action = lambda icon, item: run_command(config['command']) if show_confirmation_dialog(config) else None
                else:
                    action = lambda icon, item: run_command(config['command'])
            case 'function':
                match config['function']:
                    case 'restart':
                        if confirm_required:
                            action = lambda icon, item: restart_app(icon) if show_confirmation_dialog(config) else None
                        else:
                            action = lambda icon, item: restart_app(icon)
                    case 'quit':
                        if confirm_required:
                            action = lambda icon, item: quit_app(icon) if show_confirmation_dialog(config) else None
                        else:
                            action = lambda icon, item: quit_app(icon)
                    case _:
                        print("Unknown function:", config['function'], "-", config['name'])
            case _:
                print("Unknown type:", config['type'], "-", config['name'])
        return item(config['name'], action)

def load_config(config_path):
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: Configuration file '{config_path}' not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in '{config_path}'.")
        return None
        
def start_tray():
    icon_path = resource_path("icon.ico")
    try:
        icon_image = Image.open(icon_path)
    except FileNotFoundError:
        print(f"Error: '{icon_path}' file not found.")
        return

    config_path = resource_path("config.json")
    config = load_config(config_path)
    if not config:
        return

    menu_items = []
    for config_item in config:
        if config_item.get('type') == 'separator':
            menu_items.append(Menu.SEPARATOR)
        else:
            menu_items.append(create_menu_item(config_item))

    icon = pystray.Icon("test_icon", icon_image, "OGT", menu=Menu(*menu_items))    
    icon.run()

if __name__ == "__main__":
    start_tray()