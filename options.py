from functions import get_current_screen, center_window
import tkinter as tk


def open_options_window(root):
    # Constants
    CONFIG_FILE = 'config.json'

    # Create the options window
    options_window = tk.Toplevel(root)
    
    # Screen dimensions
    SCREEN_WIDTH = get_current_screen(root).width
    SCREEN_HEIGHT = get_current_screen(root).height
    WINDOW_WIDTH = int(SCREEN_WIDTH / 2)
    WINDOW_HEIGHT = int(SCREEN_HEIGHT / 2)

    # Configure the options menu
    options_window.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
    options_window.title("Options")
    options_window.bind('<Configure>', lambda event: update_sizes()) # Bind the window resize event to update the application dynamically
    options_window.resizable(False, False)
    center_window(options_window, SCREEN_WIDTH, SCREEN_HEIGHT, WINDOW_WIDTH, WINDOW_HEIGHT)

    # Make the child window modal
    options_window.transient(root)
    options_window.grab_set()

    # Add a label and a button to close the child window
    label = tk.Label(options_window, text="This is a child window", font=("Arial", 16))
    label.pack(pady=50)

    close_button = tk.Button(options_window, text="Close", command=options_window.destroy)
    close_button.pack(pady=20)

    # When the child window is closed, the main window will be accessible again
    options_window.protocol("WM_DELETE_WINDOW", lambda: on_child_close(options_window))
    
    def update_sizes():
        return

def on_child_close(options_window):
    options_window.grab_release()
    options_window.destroy()