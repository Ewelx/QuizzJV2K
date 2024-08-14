import tkinter as tk
from tkinter import PhotoImage, filedialog
from PIL import ImageTk, Image
import json
import os

# File to save the image path
CONFIG_FILE = 'config.json'

# Create the main application window
root = tk.Tk()
root.title("QuizzJV2K")

# Set the window to fullscreen
root.attributes('-fullscreen', True)

# Configure the grid layout
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=2)
root.grid_rowconfigure(2, weight=1)
root.grid_columnconfigure(0, weight=3)
root.grid_columnconfigure(1, weight=7)

# Title
title = tk.Label(root, text="QuizzJV2K", font=("Arial", 32, "bold"))
title.grid(row=0, column=0, columnspan=3, pady=10, sticky="nsew")

# Buttons
button_names = ["Play Quizz", "Create Quizz", "Load Quizz", "Delete Quizz", "Options", "Quit"]

def button_command(name):
    print(f"{name} button clicked")

# Create a frame for buttons
buttons_frame = tk.Frame(root)
buttons_frame.grid(row=1, column=0, padx=200, pady=70, sticky="ns") 

for name in button_names:
    button = tk.Button(buttons_frame, text=name, command=lambda n=name: button_command(n),
                       width=30, height=4)  # Adjust width and height to make buttons bigger
    button.pack(pady=30, padx=15, fill='x')  # Increase pady for vertical spacing between buttons

# Image
def load_image_path():
    """Load the image path from the configuration file."""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as file:
            config = json.load(file)
            return config.get('image_path', '')
    else:
        print("image not found")
    return ''
        
def update_image(image_path):
    """Update the image displayed in the application."""
    try:
        img = ImageTk.PhotoImage(Image.open(image_path))
        image_label.config(image=img)
        image_label.image = img  # Keep a reference to avoid garbage collection
    except Exception as e:
        print(f"Error loading image: {e}")
        
image_path = load_image_path()
image_label = tk.Label(root)
update_image(image_path)
image_label.grid(row=1, column=1, padx=(0, 100), pady=5, sticky="nsew")

# Footer
footer = tk.Label(root, text="Created by Ewel", font=("Arial", 10))
footer.grid(row=2, column=0, columnspan=3, pady=10, sticky="s")

# Start the Tkinter event loop
root.mainloop()
