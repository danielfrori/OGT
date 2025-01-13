import pystray
from pystray import MenuItem as item, Menu
from PIL import Image
import webbrowser
import subprocess
import platform
import os
import sys

# Helper function to locate resources
def resource_path(relative_path):
    """ Get the absolute path to a resource, works for both dev and bundled modes. """
    if hasattr(sys, '_MEIPASS'):
        # If running in a PyInstaller/Nuitka bundle
        return os.path.join(sys._MEIPASS, relative_path)
    else:
        # If running as a standard Python script
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), relative_path)


# Function to handle the "Open Webpage" action
def open_webpage(page):
    webbrowser.open(page)

# Function to restart the PC
def restart_pc():
    try:
        if platform.system() == "Windows":
            command = ["shutdown", "/r", "/t", "0"]  # Restart immediately
        elif platform.system() == "Linux":
            command = ["reboot"]

        subprocess.run(command, check=True)
    except Exception as e:
        print("Error restarting PC:", e)

# Function to restart into firmware settings
def restart_fw():
    try:
        if platform.system() == "Windows":
            command = ["shutdown", "/r", "/fw", "/f", "/t", "0"]
        elif platform.system() == "Linux":
            command = ["systemctl", "reboot", "--firmware-setup"]

        subprocess.run(command, check=True)
    except Exception as e:
        print("Error restarting PC:", e)

# Function to shut down the PC
def shutdown():
    try:
        if platform.system() == "Windows":
            command = ["shutdown", "/s", "/t", "0"]
        elif platform.system() == "Linux":
            command = ["shutdown", "now"]
        
        subprocess.run(command, check=True)
    except Exception as e:
        print("Error shutting down PC:", e)

# Function to handle the "Exit" menu item
def on_quit(icon, item):
    icon.stop()

# Function to start the system tray application
def start_tray():
    # Locate the icon.ico file
    icon_path = resource_path("icon.ico")
    try:
        icon_image = Image.open(icon_path)
    except FileNotFoundError:
        print(f"Error: '{icon_path}' file not found.")
        return

    # Create the sub-menu for links
    usefulLinksMenu = Menu(
        item("Speedtest", lambda icon, item: open_webpage("https://www.speedtest.net/")),
        item("Rapidtables", lambda icon, item: open_webpage("https://www.rapidtables.com/")),
        item("TinyWow", lambda icon, item: open_webpage("https://www.tinywow.com/")),
        item("WeTransfer", lambda icon, item: open_webpage("https://www.wetransfer.com/")),
        item("Joypad.ai", lambda icon, item: open_webpage("https://joypad.ai/")),
        pystray.Menu.SEPARATOR,
        item("Arch Linux", lambda icon, item: open_webpage("https://archlinux.org")),
        item("ProtonDB", lambda icon, item: open_webpage("https://www.protondb.com/")),
    )

    steamMenu = Menu(
        item("Big Picture Mode", lambda icon, item: open_webpage("steam://open/bigpicture")),
        item("Steam Console", lambda icon, item: open_webpage("steam://open/console"))
    )

    systemMenu = Menu(
        item("Restart PC", lambda icon, item: restart_pc()),
        item("Restart into Firmware Setup", lambda icon, item: restart_fw()),
        item("Shutdown", lambda icon, item: shutdown())
    )

    # Create the main menu
    menu = Menu(
        item("Links", usefulLinksMenu),  # Add sub-menu here
        item("Steam", steamMenu),
        pystray.Menu.SEPARATOR,
        item("System", systemMenu),
        item("Quit", on_quit)
    )

    # Create and run the system tray icon
    icon = pystray.Icon("test_icon", icon_image, "Ori General Tools", menu=menu)
    icon.run()

# Start the application
if __name__ == "__main__":
    start_tray()