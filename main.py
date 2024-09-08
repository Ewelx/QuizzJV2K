from functions import get_current_screen
from options import open_options_window
from PIL import ImageTk, Image
import tkinter as tk
import playlist
import json
import sys
import os

# Constants
CONFIG_FILE = 'config.json'
# Title constant
TITLE_PADY_COEFFICIENT = 0.01351851851
TITLE_FONT_SIZE_COEFFICIENT = 0.020625
# Buttons constants
BUTTON_WIDTH_FACTOR_COEFFICIENT = 0.019
BUTTON_HEIGHT_FACTOR_COEFFICIENT = 0.0042
BUTTONS_FRAME_PADX_COEFFICIENT = 0.095
BUTTONS_FRAME_SECOND_PADX_COEFFICIENT = 0.025208333333
BUTTONS_FRAME_PADY_COEFFICIENT = 0.02
BUTTONS_SPACE_PADY_COEFFICIENT = 0.01851851851
# Image constants
IMAGE_SCALE_FACTOR_COEFFICIENT = 0.625  
IMAGE_FRAME_PADY_COEFFICIENT = 0.01944444444
# Footer constants
FOOTER_FONT_SIZE_COEFFICIENT = 0.012

# Create the main application window
root = tk.Tk()
root.configure(bg='#e3a0ac')  # Font color of the main menu of the application
root.title("QuizzJV2K") # Title of the application
root.attributes('-fullscreen', True) # Put the application in full screen
root.bind('<Configure>', lambda event: update_sizes()) # Bind the window resize event to update the application dynamically

# Screen dimensions
SCREEN_WIDTH = get_current_screen(root).width
SCREEN_HEIGHT = get_current_screen(root).height

# Configure the grid layout
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)
root.grid_columnconfigure(0, weight=3)
root.grid_columnconfigure(1, weight=8)

# Title
title = tk.Label(root, text="QuizzJV2K", font=("Arial", int(SCREEN_WIDTH * TITLE_FONT_SIZE_COEFFICIENT), "bold"), bg="#e3a0ac", anchor="center")

# Buttons
# Buttons Frame
buttons_frame = tk.Frame(root, bg='#e3a0ac')  # Set background color of the frame        
# Buttons names
button_names = ["Play Quizz", "Create Quizz", "Load Quizz", "Delete Quizz", "Options", "Quit"]
button_fg_color = 'white'  # Button color
# Create all the buttons
buttons = []
for name in button_names:
    button = tk.Button(buttons_frame, text=name, command=lambda n=name: button_command(n))
    buttons.append(button)
    
# Image Frame with border
image_frame = tk.Frame(root, bg='#e3a0ac', padx=2, pady=2) 
image_label = tk.Label(image_frame, bg='#000000')  # Background color inside the border

# Footer
footer = tk.Label(root, text="Created by Ewel", font=("Arial",int(SCREEN_HEIGHT * FOOTER_FONT_SIZE_COEFFICIENT)), bg="#e3a0ac")

# Update the size of the title
def update_title(SCREEN_WIDTH, SCREEN_HEIGHT):
    new_pady = int(SCREEN_HEIGHT * TITLE_PADY_COEFFICIENT)
    new_font_size = max(int(SCREEN_WIDTH * TITLE_FONT_SIZE_COEFFICIENT / 2), int(SCREEN_WIDTH * TITLE_FONT_SIZE_COEFFICIENT))  # Example: scale font size
    title.config(font=("Arial", new_font_size, "bold"), pady=new_pady)
    title.grid(row=0, column=0, columnspan=3, pady=SCREEN_HEIGHT * TITLE_PADY_COEFFICIENT, sticky="nsew")
    
# Update the size of the buttons
def update_buttons(SCREEN_WIDTH, SCREEN_HEIGHT):
    button_width = int(SCREEN_WIDTH * BUTTON_WIDTH_FACTOR_COEFFICIENT)
    button_height = int(SCREEN_HEIGHT * BUTTON_HEIGHT_FACTOR_COEFFICIENT)
    
    buttons_frame.grid(row=1, column=0, padx=(SCREEN_WIDTH * BUTTONS_FRAME_PADX_COEFFICIENT, SCREEN_WIDTH * BUTTONS_FRAME_SECOND_PADX_COEFFICIENT), pady=SCREEN_HEIGHT*BUTTONS_FRAME_PADY_COEFFICIENT, sticky="nsew")
    
    for button in buttons:
        button.config(width=button_width, height=button_height)
        button.pack(pady=SCREEN_HEIGHT * BUTTONS_SPACE_PADY_COEFFICIENT, fill='x')
        
# Update the size of the image
def update_image(image_path, SCREEN_WIDTH, SCREEN_HEIGHT):
    try:
        # Calculate the new size for the image
        new_width = int(SCREEN_WIDTH * IMAGE_SCALE_FACTOR_COEFFICIENT)
        new_height = int(SCREEN_HEIGHT * IMAGE_SCALE_FACTOR_COEFFICIENT)
        image_frame.grid(row=1, column=1, pady=SCREEN_HEIGHT * IMAGE_FRAME_PADY_COEFFICIENT, sticky="nsew")
        
        # Load and resize the image
        img = Image.open(image_path)
        img = img.resize((new_width, new_height), Image.LANCZOS)
        img_tk = ImageTk.PhotoImage(img)
        
        # Update the image in the label
        image_label.config(image=img_tk)
        image_label.image = img_tk 
        image_label.pack()
    except Exception as e:
        print(f"Error loading image: {e}")
        
# Update the size of the footer
def update_footer(SCREEN_HEIGHT):
    footer.config(font=("Arial", int(SCREEN_HEIGHT * FOOTER_FONT_SIZE_COEFFICIENT)))
    footer.grid(row=2, column=0, columnspan=3, sticky="s")
        
# Update the sizes of all elements
def update_sizes():
    root.unbind('<Configure>')
    SCREEN_WIDTH = get_current_screen(root).width
    SCREEN_HEIGHT = get_current_screen(root).height
    update_title(SCREEN_WIDTH, SCREEN_HEIGHT)
    update_buttons(SCREEN_WIDTH, SCREEN_HEIGHT)
    update_image(load_image_path(), SCREEN_WIDTH, SCREEN_HEIGHT)
    update_footer(SCREEN_HEIGHT)
    # Réactiver l'événement <Configure> après un court délai pour éviter la boucle
    root.after(100, lambda: root.bind('<Configure>', lambda event: update_sizes()))
    return

# Load the image path from the configuration file.
def load_image_path():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as file:
            config = json.load(file)
            return config.get('image_path', '')
    else:
        print("image not found")
    return ''

# The command that activate when clicking a button
def button_command(name):
    if name == "Play Quizz":
        print("1")
    elif name == "Create Quizz":
        print("2")
    elif name == "Load Quizz":
        print("3")
    elif name == "Delete Quizz":
        print("4")
    elif name == "Options":
        open_options_window(root)
    else:
        on_closing()
        
update_sizes()

# Start the playlist
playlist.start_playlist()

# On application window closing
def on_closing():
        playlist.stop_playlist()
        root.destroy()
        sys.exit()
root.protocol("WM_DELETE_WINDOW", on_closing)

# Start the Tkinter event loop
root.mainloop()


