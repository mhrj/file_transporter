import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import os

# Constants
BG_COLOR = "#f0f0f0"
BUTTON_WIDTH = 55
SPLASH_BG = "#007BFF"

current_directory = os.path.dirname(os.path.abspath(__file__))

# GUI-related Functions
def create_rounded_button(parent, text, command, width=15, icon_path=None):
    """Creates a rounded button with optional icon."""
    button = ttk.Button(parent, text=text, command=command, width=width, style="Rounded.TButton", cursor="hand2")
    if icon_path:
        img = Image.open(os.path.join(current_directory, "images", icon_path)).resize((20, 20), Image.LANCZOS)
        icon = ImageTk.PhotoImage(img)
        button.config(image=icon, compound=tk.LEFT)
        button.image = icon
    return button

def show_splash():
    """Displays the splash screen at application start."""
    splash = tk.Toplevel()
    splash.title("Welcome")
    splash.geometry("400x200+%d+%d" % ((splash.winfo_screenwidth() - 400) // 2, (splash.winfo_screenheight() - 200) // 2))
    splash.configure(bg=SPLASH_BG)
    splash.overrideredirect(True)
    tk.Label(splash, text="Welcome to File Transfer App", bg=SPLASH_BG, font=("Helvetica", 16, "bold"), fg="white").pack(pady=20)

    animation_label = tk.Label(splash, bg=SPLASH_BG)
    animation_label.pack(pady=10)

    animation_images = [ImageTk.PhotoImage(Image.open(os.path.join(current_directory, f"animation/frame{i}.png")).resize((100, 100), Image.LANCZOS)) for i in range(1, 5)]
    def animate(index=0):
        animation_label.config(image=animation_images[index])
        splash.after(600, animate, (index + 1) % len(animation_images))

    animate()
    splash.after(3000, lambda: [splash.destroy(), root.deiconify()])

def log_message(message):
    """Logs messages in the result text area."""
    result_area.config(state=tk.NORMAL)
    result_area.insert(tk.END, message + "\n")
    result_area.config(state=tk.DISABLED)
    result_area.yview(tk.END)

# State Management
def set_buttons_state(state):
    """Enables or disables all interactive buttons and changes cursor based on state."""
    cursor_type = "watch" if state == "disabled" else "hand2"
    for button in buttons:
        button.config(state=state, cursor=cursor_type)

# Main functions
def display_selection():
    """Logs the selected options, folders, and checkboxes."""
    set_buttons_state("disabled")
    if any(not folder.get() for folder in folder_vars):
        messagebox.showwarning("Warning", "Please select both folders.")
        set_buttons_state("normal")
        return

    log_message("Selected Options: " + ", ".join(combo.get() for combo in combo_vars))
    log_message("Folders: " + ", ".join(folder.get() for folder in folder_vars))
    log_message("Selected Checkboxes: " + ", ".join(option for i, option in enumerate(checkbox_options) if checkbox_vars[i].get()))

    status_label.config(text="Transfer details logged.")
    set_buttons_state("normal")

def browse_folder(index):
    """Opens file dialog to select a folder and updates the label."""
    foldername = filedialog.askdirectory()
    if foldername:
        folder_vars[index].set(foldername)
        folder_labels[index].config(text=foldername or "Select a folder...")
        status_label.config(text="Folder selected.")

def clear_selections():
    """Clears all selections, checkboxes, and the result text area."""
    for var in folder_vars: var.set('')
    for var in checkbox_vars: var.set(False)
    result_area.config(state=tk.NORMAL)
    result_area.delete(1.0, tk.END)
    result_area.config(state=tk.DISABLED)
    status_label.config(text="Selections cleared.")

# Main application window setup
root = tk.Tk()
root.title("File Transfer App")
root.withdraw()
show_splash()
root.geometry("800x600")
root.configure(bg=BG_COLOR)
root.iconphoto(False, ImageTk.PhotoImage(file=os.path.join(current_directory, "logo.png")))
root.resizable(width=False, height=False)

# Styles and Background
style = ttk.Style()
style.theme_use("clam")

# Background image
bg_image = ImageTk.PhotoImage(Image.open(os.path.join(current_directory, "images", "background.jpg")).resize((800, 600), Image.LANCZOS))
tk.Label(root, image=bg_image).place(relwidth=1, relheight=1)

# Dropdown menu for options
options = ["Zip and Cut", "Zip and Copy", "Copy", "Cut"]
dropdown_frame = tk.Frame(root, bg=BG_COLOR)
dropdown_frame.grid(row=0, column=0, padx=10, pady=10, sticky='w')

combo1 = ttk.Combobox(dropdown_frame, values=options, state='readonly', width=30)
combo1.grid(row=0, column=0, pady=(0, 5))
combo_vars = [combo1]

# Toggle for checkbox options
checkbox_options = ["Videos", "Images", "Text Files"]
checkbox_frame = tk.Frame(dropdown_frame, bg=BG_COLOR)
checkbox_vars = [tk.BooleanVar() for _ in checkbox_options]
for i, option in enumerate(checkbox_options):
    tk.Checkbutton(checkbox_frame, text=option, variable=checkbox_vars[i], bg=BG_COLOR, bd=0, fg="black", cursor="hand2").grid(row=i, column=0, sticky='w')

def toggle_checkbox_options():
    checkbox_frame.grid_remove() if checkbox_frame.winfo_ismapped() else checkbox_frame.grid()

toggle_button = create_rounded_button(dropdown_frame, "File Type", toggle_checkbox_options)
toggle_button.grid(row=1, column=0, pady=(5, 10))
checkbox_frame.grid_remove()

# Folder selection
folder_frame = tk.Frame(root, bg=BG_COLOR)
folder_frame.grid(row=1, column=0, padx=10, pady=10, sticky='w')

folder_vars = [tk.StringVar() for _ in range(2)]
folder_labels = []
for i, label_text in enumerate(["from", "to"]):
    folder_button = create_rounded_button(folder_frame, f"Browse ({label_text})", lambda idx=i: browse_folder(idx))
    folder_button.grid(row=2*i, column=0, pady=(5, 10), sticky='w')
    folder_labels.append(tk.Label(folder_frame, text="Select a folder...", width=50, font=("Helvetica", 10, "bold"), bg=BG_COLOR))
    folder_labels[-1].grid(row=2*i + 1, column=0, pady=(0, 10), sticky='w')

# Result area and status label
text_frame = tk.Frame(root, bg=BG_COLOR)
text_frame.grid(row=1, column=1, padx=10, pady=10, sticky='w')
result_area = tk.Text(text_frame, height=15, width=42, state=tk.DISABLED, bg="#ffffff")
result_area.grid(row=0, column=0)
scrollbar = tk.Scrollbar(text_frame, command=result_area.yview)
scrollbar.grid(row=0, column=1, sticky='ns')
result_area.config(yscrollcommand=scrollbar.set)

# Action buttons
display_button = create_rounded_button(root, "Transfer!!", display_selection, width=BUTTON_WIDTH)
display_button.grid(row=2, column=0, pady=20, columnspan=2)
clear_button = create_rounded_button(root, "Clear Selections", clear_selections, width=BUTTON_WIDTH)
clear_button.grid(row=3, column=0, pady=10, columnspan=2)
buttons = [display_button, clear_button, toggle_button]

status_label = tk.Label(root, text="", fg="green", font=("Helvetica", 10), bg=BG_COLOR)
status_label.grid(row=4, column=0, columnspan=2)

root.protocol("WM_DELETE_WINDOW", root.destroy)
root.mainloop()
