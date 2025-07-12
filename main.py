import pystray
from pystray import MenuItem as item, Menu
from PIL import Image
import webbrowser
import subprocess
import platform
import time
import os
import pathlib
import json

def resource_path(relative_path):
    return str(pathlib.Path(__file__).parent / relative_path)

def run_command(command):
    try:
        subprocess.run(command, check=True)
    except Exception as e:
        print("Error running command:", e)

def open_webpage(page):
    webbrowser.open(page)

def restart_pc():
    try:
        if platform.system() == "Windows":
            run_command(["shutdown", "/r", "/t", "0"])
        elif platform.system() == "Linux":
            run_command(["reboot"])
    except Exception as e:
        print("Error restarting PC:", e)

def restart_fw():
    try:
        if platform.system() == "Windows":
            run_command(["shutdown", "/r", "/fw", "/f", "/t", "0"])
        elif platform.system() == "Linux":
            run_command(["systemctl", "reboot", "--firmware-setup"])
    except Exception as e:
        print("Error restarting PC:", e)

def shutdown():
    try:
        if platform.system() == "Windows":
            run_command(["shutdown", "/s", "/t", "0"])
        elif platform.system() == "Linux":
            run_command(["shutdown", "now"])
    except Exception as e:
        print("Error shutting down PC:", e)

def restart_steam():
    try:
        if platform.system() == "Windows":
            run_command(["taskkill", "/IM", "steam.exe", "/F"])
            time.sleep(3)
    
            # Attempt default Steam path, adjust if installed elsewhere
            steam_path = os.path.expandvars(r"C:\\Program Files (x86)\\Steam\\Steam.exe")
    
            if not os.path.exists(steam_path):
                print(f"Could not find Steam at {steam_path}. Please check the path.")
                return

            subprocess.Popen([steam_path])
        if platform.system() == "Linux":
            run_command(["pkill", "-x", "steam"])
            time.sleep(3)
            subprocess.Popen(["steam"])
    except Exception as e:
        print("Error restarting Steam:", e)

def on_quit(icon, item):
    icon.stop()

def create_menu_item(config):
    if 'submenu' in config:
        submenu_items = [create_menu_item(sub_item) for sub_item in config['submenu']]
        return item(config['name'], Menu(*submenu_items))
    else:
        action = None
        if config.get('type') == 'webpage':
            action = lambda icon, item: open_webpage(config['url'])
        elif config.get('type') == 'command':
            action = lambda icon, item: run_command(config['command'])
        elif config.get('type') == 'function':
            if config['function'] == 'restart_steam':
                action = lambda icon, item: restart_steam()
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
    menu_items.append(item("Quit", on_quit))

    icon = pystray.Icon("test_icon", icon_image, "Ori General Tools", menu=Menu(*menu_items))    
    icon.run()

if __name__ == "__main__":
    start_tray()