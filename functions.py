from screeninfo import get_monitors
import json
import os

# Get the current screen on which the application is
def get_current_screen(window):
    x = window.winfo_x()
    y = window.winfo_y()

    for monitor in get_monitors():
        if monitor.x <= x < monitor.x + monitor.width and monitor.y <= y < monitor.y + monitor.height:
            return monitor
    return None

# Load the configuration from the JSON file.
def load_config(CONFIG_FILE):
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as file:
            return json.load(file)
    return {}

# Center the window on the screen
def center_window(window, screen_width, screen_height, width, height):
    position_x = int((screen_width - width) / 2)
    position_y = int((screen_height - height) / 2)

    window.geometry(f"{width}x{height}+{position_x}+{position_y}")