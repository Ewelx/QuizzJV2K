import tkinter as tk
from PIL import ImageTk, Image
import json
import os
import playlist

# File to save the image path
CONFIG_FILE = 'config.json'

playlist.start_playlist()

# Create the main application window
root = tk.Tk()
root.configure(bg='#e3a0ac')  # Burgundy red color
root.title("QuizzJV2K")

# Set the window to fullscreen
root.attributes('-fullscreen', True)

# Configure the grid layout
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=2)
root.grid_rowconfigure(2, weight=1)
root.grid_columnconfigure(0, weight=3)
root.grid_columnconfigure(1, weight=7)

# Constants
SCREEN_WIDTH = root.winfo_screenwidth()
SCREEN_HEIGHT = root.winfo_screenheight()
IMAGE_SCALE_FACTOR = 0.625  
BUTTON_WIDTH_FACTOR = 0.1  
BUTTON_HEIGHT_FACTOR = 0.1 

# Title
title = tk.Label(root, text="QuizzJV2K", font=("Arial", 32, "bold"), bg="#e3a0ac")
title.grid(row=0, column=0, columnspan=3, pady=10, sticky="nsew")

# Buttons
def update_buttons():
    button_width = int(SCREEN_WIDTH * BUTTON_WIDTH_FACTOR)
    button_height = int(SCREEN_HEIGHT * BUTTON_HEIGHT_FACTOR)
    
    for button in buttons:
        button.config(width=button_width, height=button_height)
        
# Buttons Frame
buttons_frame = tk.Frame(root, bg='#e3a0ac')  # Set background color of the frame
buttons_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        
# Buttons names
button_names = ["Play Quizz", "Create Quizz", "Load Quizz", "Delete Quizz", "Options", "Quit"]
button_fg_color = 'white'  # Text color

buttons = []
for name in button_names:
    button = tk.Button(buttons_frame, text=name, command=lambda n=name: button_command(n))
    button.pack(pady=5, padx=10, fill='x')
    buttons.append(button)
    
def button_command(name):
    print(f"{name} button clicked")
    
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
    """Update the image displayed in the application to be 62.5% of the screen size."""
    try:
        # Calculate the new size for the image
        new_width = int(SCREEN_WIDTH * IMAGE_SCALE_FACTOR)
        new_height = int(SCREEN_HEIGHT * IMAGE_SCALE_FACTOR)
        
        # Load and resize the image
        img = Image.open(image_path)
        img = img.resize((new_width, new_height), Image.LANCZOS)
        img_tk = ImageTk.PhotoImage(img)
        
        # Update the image in the label
        image_label.config(image=img_tk)
        image_label.image = img_tk  # Keep a reference to avoid garbage collection
    except Exception as e:
        print(f"Error loading image: {e}")
        
# Image Frame (with border)
image_frame = tk.Frame(root, bg='#e3a0ac', padx=2, pady=2)  # Black border
image_frame.grid(row=1, column=1, padx=(0, 75), pady=120, sticky="nsew")
image_label = tk.Label(image_frame, bg='#000000')  # Background color inside the border
image_label.pack()
image_path = load_image_path()
update_image(image_path)

# Footer
footer = tk.Label(root, text="Created by Ewel", font=("Arial", 10), bg="#e3a0ac")
footer.grid(row=2, column=0, columnspan=3, pady=10, sticky="s")

# Start the Tkinter event loop
root.mainloop()
