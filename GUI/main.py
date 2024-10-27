import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import os

current_directory = os.path.dirname(os.path.abspath(__file__))

def create_rounded_button(parent, text, command, width=15, icon_path=None):
    button = ttk.Button(parent, text=text, command=command, width=width)
    button.config(style="Rounded.TButton")

    if icon_path:
        img = Image.open(f"{current_directory}//images//folder_icon.png")
        img = img.resize((20, 20), Image.LANCZOS)
        icon = ImageTk.PhotoImage(img)
        button.config(image=icon, compound=tk.LEFT)
        button.image = icon

    button.bind("<Enter>", lambda e: button.config(style="RoundedHover.TButton"))
    button.bind("<Leave>", lambda e: button.config(style="Rounded.TButton"))

    return button

def show_splash():
    splash = tk.Toplevel()
    splash.title("Welcome")
    splash.geometry("400x200")
    splash.configure(bg="#007BFF")
    splash.overrideredirect(True)

    screen_width = splash.winfo_screenwidth()
    screen_height = splash.winfo_screenheight()
    x = (screen_width // 2) - (200)
    y = (screen_height // 2) - (100)
    splash.geometry(f"400x200+{x}+{y}")

    label = tk.Label(splash, text="Welcome to File Transfer App", bg="#007BFF", font=("Helvetica", 16, "bold"), fg="white")
    label.pack(pady=20)

    animation_label = tk.Label(splash, bg="#007BFF")
    animation_label.pack(pady=10)

    animation_images = []
    for i in range(1, 5):
        img_path = os.path.join(current_directory, f"animation//frame{i}.png")
        img = Image.open(img_path).resize((100, 100), Image.LANCZOS)
        animation_images.append(ImageTk.PhotoImage(img))

    def animate(index=0):
        animation_label.config(image=animation_images[index])
        index = (index + 1) % len(animation_images)
        splash.after(600, animate, index)

    animate()
    splash.after(3000, lambda: [splash.destroy(), root.deiconify()])

def log_message(message):
    result_area.config(state=tk.NORMAL)
    result_area.insert(tk.END, message + "\n")
    result_area.config(state=tk.DISABLED)
    result_area.yview(tk.END)

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

def browse_folder(index):
    foldername = filedialog.askdirectory()
    if foldername:
        folder_vars[index].set(foldername)
        folder_labels[index].config(text=foldername)
        status_label.config(text="Folder selected.")
        update_placeholder(index)

def update_placeholder(index):
    if folder_vars[index].get() == '':
        folder_labels[index].config(text="Select a folder...")
    else:
        folder_labels[index].config(text=folder_vars[index].get())

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
    for i in range(len(folder_vars)):
        update_placeholder(i)

root = tk.Tk()
icon_photo = ImageTk.PhotoImage(file=os.path.join(current_directory, "logo.png"))
root.iconphoto(False, icon_photo)

root.geometry("800x600")
root.configure(bg="#f0f0f0")

background_image = Image.open(os.path.join(current_directory, "images", "background.jpg"))
background_image = background_image.resize((800, 600), Image.LANCZOS)
bg_image = ImageTk.PhotoImage(background_image)

bg_label = tk.Label(root, image=bg_image)
bg_label.place(relwidth=1, relheight=1)

root.withdraw()
show_splash()

style = ttk.Style()
style.theme_use("clam")
style.configure("Rounded.TButton", relief="flat", background="#007BFF", foreground="black", padding=6)
style.map("Rounded.TButton", background=[("active", "#0056b3")])
style.configure("RoundedHover.TButton", background="#0056b3")

dropdown_frame = tk.Frame(root, bg="#f0f0f0")
dropdown_frame.grid(row=0, column=0, padx=10, pady=10, sticky='w')

options = ["Zip and Cut", "Zip and Copy", "Copy", "Cut"]
combo_vars = []
combo1 = ttk.Combobox(dropdown_frame, values=options, state='readonly', width=30)
combo1.grid(row=0, column=0, pady=(0, 5))
combo_vars.append(combo1)

def toggle_checkbox_options():
    if checkbox_frame.winfo_ismapped():
        checkbox_frame.grid_remove()
        toggle_button.config(text="File Type")
    else:
        checkbox_frame.grid()
        toggle_button.config(text="Hide File Type")

toggle_button = create_rounded_button(dropdown_frame, "File Type", toggle_checkbox_options)
toggle_button.grid(row=1, column=0, pady=(5, 10))

checkbox_options = ["Videos", "Images", "Text Files"]
checkbox_vars = [tk.BooleanVar() for _ in checkbox_options]

checkbox_frame = tk.Frame(dropdown_frame, bg="#f0f0f0")
for i, option in enumerate(checkbox_options):
    checkbox = tk.Checkbutton(checkbox_frame, text=option, variable=checkbox_vars[i], bg="#f0f0f0", bd=0, fg="black")
    checkbox.grid(row=i, column=0, sticky='w')

folder_frame = tk.Frame(root, bg="#f0f0f0")
folder_frame.grid(row=1, column=0, padx=10, pady=10, sticky='w')

folder_vars = []
folder_labels = []

from_var = tk.StringVar()
folder_vars.append(from_var)

from_browse_button = create_rounded_button(folder_frame, "Browse (from)", lambda: browse_folder(0))
from_browse_button.grid(row=0, column=0, pady=(5, 10), sticky='w')
from_folder_label = tk.Label(folder_frame, text="Select a folder...", width=50, font=("Helvetica", 10, "bold"), bd=0, bg="#f0f0f0", fg="black")
from_folder_label.grid(row=1, column=0, pady=(0, 10), sticky='w')
folder_labels.append(from_folder_label)

to_var = tk.StringVar()
folder_vars.append(to_var)

to_browse_button = create_rounded_button(folder_frame, "Browse (to)", lambda: browse_folder(1))
to_browse_button.grid(row=2, column=0, pady=(5, 10), sticky='w')
to_folder_label = tk.Label(folder_frame, text="Select a folder...", width=50, font=("Helvetica", 10, "bold"), bd=0, bg="#f0f0f0", fg="black")
to_folder_label.grid(row=3, column=0, pady=(0, 10), sticky='w')
folder_labels.append(to_folder_label)

text_frame = tk.Frame(root, bg="#f0f0f0")
text_frame.grid(row=1, column=1, columnspan=1, padx=10, pady=10, sticky='w')

result_area = tk.Text(text_frame, height=15, width=42, state=tk.DISABLED, bd=0, bg="#ffffff", fg="black")
result_area.grid(row=0, column=0)

scrollbar = tk.Scrollbar(text_frame, command=result_area.yview)
scrollbar.grid(row=0, column=1, sticky='ns')
result_area.config(yscrollcommand=scrollbar.set)

display_button = create_rounded_button(root, "Transfer!!", display_selection, width=55)
display_button.grid(row=2, column=0, pady=20, columnspan=2)

clear_button = create_rounded_button(root, "Clear Selections", clear_selections, width=55)
clear_button.grid(row=3, column=0, pady=10, columnspan=2)

checkbox_frame.grid_remove()

status_label = tk.Label(root, text="", fg="green", font=("Helvetica", 10), bd=0, bg="#f0f0f0")
status_label.grid(row=4, column=0, columnspan=2)

def on_closing():
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()
