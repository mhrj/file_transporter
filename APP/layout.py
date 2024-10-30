import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import os
import helper

BG_COLOR = "#f0f0f0"
BUTTON_WIDTH = 55
SPLASH_BG = "#007BFF"
current_directory = os.path.dirname(os.path.abspath(__file__))

def create_button(parent, text, command, width=15, icon_path=None):
    button = ttk.Button(parent, text=text, command=command, width=width, style="Rounded.TButton", cursor="hand2")
    if icon_path:
        img = Image.open(os.path.join(current_directory, "images", icon_path)).resize((20, 20), Image.LANCZOS)
        icon = ImageTk.PhotoImage(img)
        button.config(image=icon, compound=tk.LEFT)
        button.image = icon
    return button

def show_splash_screen():
    splash = tk.Toplevel()
    splash.geometry("400x200+%d+%d" % ((splash.winfo_screenwidth() - 400) // 2, (splash.winfo_screenheight() - 200) // 2))
    splash.configure(bg=SPLASH_BG)
    splash.overrideredirect(True)

    tk.Label(splash, text="File Transfer (v0.10 beta)", bg=SPLASH_BG, font=("Helvetica", 16, "bold"), fg="white").pack(pady=20)
    animation_label = tk.Label(splash, bg=SPLASH_BG)
    animation_label.pack(pady=10)

    frames = [ImageTk.PhotoImage(Image.open(os.path.join(current_directory, f"animation/frame{i}.png")).resize((100, 100), Image.LANCZOS)) for i in range(1, 5)]
    
    def animate(index=0):
        animation_label.config(image=frames[index])
        splash.after(600, animate, (index + 1) % len(frames))
    animate()

    splash.after(3000, lambda: [splash.destroy(), root.deiconify()])

def log_message(message):
    result_area.config(state=tk.NORMAL)
    result_area.insert(tk.END, message + "\n")
    result_area.config(state=tk.DISABLED)
    result_area.yview(tk.END)

def set_buttons_state(state):
    cursor_type = "watch" if state == "disabled" else "hand2"
    for button in buttons:
        button.config(state=state, cursor=cursor_type)

def get_method_value(method_name):
    method_mapping = {"Zip and Cut": 1, "Cut": 2, "Zip and Copy": 3, "Copy": 4}
    return method_mapping.get(method_name, 0)

def process_selection():
    set_buttons_state("disabled")
    if any(not folder.get() for folder in folder_vars):
        messagebox.showwarning("Warning", "Please select both folders.")
        set_buttons_state("normal")
        return
    
    main_dir, destination_dir = folder_vars[0].get(), folder_vars[1].get()
    method = get_method_value(combo_method.get())
    selected_types = [opt.lower() for i, opt in enumerate(checkbox_options) if checkbox_vars[i].get()]

    log_message("✅ **Selected Options:** " + ", ".join(combo.get() for combo in combo_vars))
    log_message("📂 **Source Folder:** " + main_dir)
    log_message("📂 **Destination Folder:** " + destination_dir)
    log_message("✅ **Selected File Types:** " + ", ".join(option for i, option in enumerate(checkbox_options) if checkbox_vars[i].get()))
    
    helper.process_files(main_dir, destination_dir, method, selected_types, log_message)
    status_label.config(text="✅ Transfer details logged successfully.")
    set_buttons_state("normal")

def browse_for_folder(index):
    foldername = filedialog.askdirectory()
    if foldername:
        folder_vars[index].set(foldername)
        folder_labels[index].config(text=foldername)
        status_label.config(text="Folder selected.")

def clear_all_selections():
    for var in folder_vars: var.set('')
    for label in folder_labels: label.config(text="Select a folder...")
    for var in checkbox_vars: var.set(False)
    combo_method.set('')
    result_area.config(state=tk.NORMAL)
    result_area.delete(1.0, tk.END)
    result_area.config(state=tk.DISABLED)
    status_label.config(text="Selections cleared.")

root = tk.Tk()
root.title("File Transfer")
root.withdraw()
show_splash_screen()
root.geometry("800x600")
root.configure(bg=BG_COLOR)
root.iconphoto(False, ImageTk.PhotoImage(file=os.path.join(current_directory, "logo.png")))
root.resizable(width=False, height=False)

style = ttk.Style()
style.theme_use("clam")

bg_image = ImageTk.PhotoImage(Image.open(os.path.join(current_directory, "images", "background.jpg")).resize((800, 600), Image.LANCZOS))
tk.Label(root, image=bg_image).place(relwidth=1, relheight=1)

options = ["Zip and Cut", "Zip and Copy", "Copy", "Cut"]
dropdown_frame = tk.Frame(root, bg=BG_COLOR)
dropdown_frame.grid(row=0, column=0, padx=10, pady=10, sticky='w')

combo_method = ttk.Combobox(dropdown_frame, values=options, state='readonly', width=30)
combo_method.grid(row=0, column=0, pady=(0, 5))
combo_vars = [combo_method]

checkbox_options = ["Documents", "Images", "Videos", "Audios"]
checkbox_frame = tk.Frame(dropdown_frame, bg=BG_COLOR)
checkbox_vars = [tk.BooleanVar() for _ in checkbox_options]

for i, option in enumerate(checkbox_options):
    row, col = divmod(i, 2)
    tk.Checkbutton(checkbox_frame, text=option, variable=checkbox_vars[i], bg=BG_COLOR, bd=0, fg="black", cursor="hand2").grid(row=row, column=col, sticky='w', padx=5, pady=5)

checkbox_frame.grid(row=1, column=0, pady=(5, 10), sticky='w')

folder_frame = tk.Frame(root, bg=BG_COLOR)
folder_frame.grid(row=1, column=0, padx=10, pady=10, sticky='w')

folder_vars = [tk.StringVar() for _ in range(2)]
folder_labels = []
for i, label_text in enumerate(["From", "To"]):
    folder_button = create_button(folder_frame, f"Browse ({label_text})", lambda idx=i: browse_for_folder(idx))
    folder_button.grid(row=2 * i, column=0, pady=(5, 10), sticky='w')
    folder_labels.append(tk.Label(folder_frame, text="Select a folder...", width=50, font=("Helvetica", 10, "bold"), bg=BG_COLOR))
    folder_labels[-1].grid(row=2 * i + 1, column=0, pady=(0, 10), sticky='w')

text_frame = tk.Frame(root, bg=BG_COLOR)
text_frame.grid(row=1, column=1, padx=10, pady=10, sticky='w')
result_area = tk.Text(text_frame, height=15, width=42, state=tk.DISABLED, bg="#ffffff", font=("Helvetica", 10))
result_area.grid(row=0, column=0)
scrollbar = tk.Scrollbar(text_frame, command=result_area.yview)
scrollbar.grid(row=0, column=1, sticky='ns')
result_area.config(yscrollcommand=scrollbar.set)

display_button = create_button(root, "Transfer!!", process_selection, width=BUTTON_WIDTH)
display_button.grid(row=2, column=0, pady=20, columnspan=2)
clear_button = create_button(root, "Clear Selections", clear_all_selections, width=BUTTON_WIDTH)
clear_button.grid(row=3, column=0, pady=10, columnspan=2)
buttons = [display_button, clear_button]

status_label = tk.Label(root, text="", fg="green", font=("Helvetica", 10), bg=BG_COLOR)
status_label.grid(row=4, column=0, columnspan=2)

root.protocol("WM_DELETE_WINDOW", root.destroy)
root.mainloop()
