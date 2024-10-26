import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk

# Function to create rounded buttons with hover effects
def create_rounded_button(parent, text, command, width=15, icon_path=None):
    button = ttk.Button(parent, text=text, command=command, width=width)
    button.config(style="Rounded.TButton")
    
    if icon_path:
        img = Image.open("D:\\hp backups\\barname nevisi\\PlayGround\\Python\\Uni\\file_transporter\\GUI\\folder_icon.png")
        img = img.resize((20, 20), Image.ANTIALIAS)  # Resize icon
        icon = ImageTk.PhotoImage(img)
        button.config(image=icon, compound=tk.LEFT)  # Place icon on the left
        button.image = icon  # Keep a reference to avoid garbage collection
    
    # Bind hover effects
    button.bind("<Enter>", lambda e: button.config(style="RoundedHover.TButton"))
    button.bind("<Leave>", lambda e: button.config(style="Rounded.TButton"))
    
    return button

# Splash Screen
def show_splash():
    splash = tk.Toplevel()
    splash.title("Welcome")
    splash.geometry("400x200")
    splash.configure(bg="#007BFF")
    splash.overrideredirect(True)

    splash_width = 400
    splash_height = 200
    screen_width = splash.winfo_screenwidth()
    screen_height = splash.winfo_screenheight()
    x = (screen_width // 2) - (splash_width // 2)
    y = (screen_height // 2) - (splash_height // 2)
    splash.geometry(f"{splash_width}x{splash_height}+{x}+{y}")

    label = tk.Label(splash, text="Welcome to the File Transfer App", bg="#007BFF", font=("Helvetica", 16, "bold"), fg="white")
    label.pack(pady=50)

    splash.after(2000, lambda: [splash.destroy(), root.deiconify()])

# Log message function
def log_message(message):
    result_area.config(state=tk.NORMAL)
    result_area.insert(tk.END, message + "\n")
    result_area.config(state=tk.DISABLED)
    result_area.yview(tk.END)  # Scroll to the bottom

# Display selections function
def display_selection():
    if any(not folder_var.get() for folder_var in folder_vars):
        messagebox.showwarning("Warning", "Please select both folders.")
        return

    selected_options = [combo.get() for combo in combo_vars if isinstance(combo, ttk.Combobox)]
    selected_folders = [folder_var.get() for folder_var in folder_vars]
    selected_checkboxes = [option for i, option in enumerate(checkbox_options) if checkbox_vars[i].get()]

    log_message("Selected Options: " + ", ".join(selected_options))
    log_message("Folders: " + ", ".join(selected_folders))
    log_message("Selected Checkboxes: " + ", ".join(selected_checkboxes))
    status_label.config(text="Transfer details logged.")

# Browse folder function
def browse_folder(index):
    foldername = filedialog.askdirectory()
    if foldername:
        folder_vars[index].set(foldername)
        folder_labels[index].config(text=foldername)
        status_label.config(text="Folder selected.")

# Clear selections function
def clear_selections():
    for folder_var in folder_vars:
        folder_var.set('')
    for checkbox_var in checkbox_vars:
        checkbox_var.set(False)
    combo1.set('')
    result_area.config(state=tk.NORMAL)
    result_area.delete(1.0, tk.END)
    result_area.config(state=tk.DISABLED)
    status_label.config(text="Selections cleared.")

# Toggle dropdown menu for checkboxes
def toggle_dropdown():
    if checkbox_frame.winfo_ismapped():
        checkbox_frame.grid_remove()
    else:
        checkbox_frame.grid(row=2, column=0, padx=5, pady=5, sticky='w')

# Create the main window
root = tk.Tk()
root.title("File Transfer")

# Get screen dimensions
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Set the initial size
window_width = 800
window_height = 600
root.geometry(f"{window_width}x{window_height}")

root.configure(bg="white")
root.withdraw()  # Hide the main window initially

show_splash()  # Show the splash screen

# Configure styles
style = ttk.Style()
style.theme_use("clam")
style.configure("Rounded.TButton", relief="flat", background="#007BFF", foreground="white", padding=6)
style.map("Rounded.TButton", background=[("active", "#0056b3")])
style.configure("RoundedHover.TButton", background="#0056b3")  # Hover effect style

# Create a frame for the dropdown menus
dropdown_frame = tk.Frame(root, bg="white")
dropdown_frame.grid(row=0, column=0, padx=10, pady=10, sticky='w')

options = ["Zip and Cut", "Zip and Copy", "Copy", "Cut"]
combo_vars = []
combo1 = ttk.Combobox(dropdown_frame, values=options, state='readonly', width=30)
combo1.grid(row=0, column=0, pady=(0, 5))
combo_vars.append(combo1)

# Button to toggle file type options
toggle_button = create_rounded_button(dropdown_frame, "File Type", toggle_dropdown)
toggle_button.grid(row=1, column=0, pady=(5, 10))

checkbox_options = ["Videos", "Images", "Text Files"]
checkbox_vars = [tk.BooleanVar() for _ in checkbox_options]

checkbox_frame = tk.Frame(dropdown_frame, bg="white")
for i, option in enumerate(checkbox_options):
    checkbox = tk.Checkbutton(checkbox_frame, text=option, variable=checkbox_vars[i], bg="white", fg="black")
    checkbox.grid(row=i, column=0, sticky='w')

folder_frame = tk.Frame(root, bg="white")
folder_frame.grid(row=1, column=0, padx=10, pady=10, sticky='w')

folder_vars = []
folder_labels = []

from_var = tk.StringVar()
folder_vars.append(from_var)

from_browse_button = create_rounded_button(folder_frame, "Browse (from)", lambda: browse_folder(0), icon_path="folder_icon.png")
from_browse_button.grid(row=0, column=0, pady=(5, 10), sticky='w')
from_folder_label = tk.Label(folder_frame, text="", fg="black", width=50, font=("Helvetica", 10, "bold"), bg="lightyellow")
from_folder_label.grid(row=1, column=0, pady=(0, 10), sticky='w')
folder_labels.append(from_folder_label)

to_var = tk.StringVar()
folder_vars.append(to_var)

to_browse_button = create_rounded_button(folder_frame, "Browse (to)", lambda: browse_folder(1), icon_path="folder_icon.png")
to_browse_button.grid(row=2, column=0, pady=(5, 10), sticky='w')
to_folder_label = tk.Label(folder_frame, text="", fg="black", width=50, font=("Helvetica", 10, "bold"), bg="lightyellow")
to_folder_label.grid(row=3, column=0, pady=(0, 10), sticky='w')
folder_labels.append(to_folder_label)

text_frame = tk.Frame(root, bg="white")
text_frame.grid(row=1, column=1, columnspan=1, padx=10, pady=10, sticky='w')

result_area = tk.Text(text_frame, height=15, width=42, state=tk.DISABLED, bg="white", fg="black", font=("Helvetica", 10))
result_area.grid(row=0, column=0)

scrollbar = tk.Scrollbar(text_frame, command=result_area.yview)
scrollbar.grid(row=0, column=1, sticky='ns')

result_area.config(yscrollcommand=scrollbar.set)

display_button = create_rounded_button(root, "Transfer!!", display_selection, width=55)
display_button.grid(row=2, column=0, pady=20, columnspan=2)

clear_button = create_rounded_button(root, "Clear Selections", clear_selections, width=55)
clear_button.grid(row=3, column=0, pady=10, columnspan=2)

checkbox_frame.grid_remove()

# Status label
status_label = tk.Label(root, text="", fg="green", bg="white", font=("Helvetica", 10))
status_label.grid(row=4, column=0, columnspan=2)

# Close splash screen and main window
def on_closing():
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

# Start the main loop
root.mainloop()
