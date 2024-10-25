import tkinter as tk
from tkinter import ttk, filedialog, messagebox

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

# Display selections function
def display_selection():
    if any(not folder_var.get() for folder_var in folder_vars):
        messagebox.showwarning("Warning", "Please select both folders.")
        return

    result_area.config(state=tk.NORMAL)
    result_area.delete(1.0, tk.END)
    selected_options = [combo.get() for combo in combo_vars if isinstance(combo, ttk.Combobox)]
    selected_folders = [folder_var.get() for folder_var in folder_vars]
    selected_checkboxes = [option for i, option in enumerate(checkbox_options) if checkbox_vars[i].get()]

    result_area.insert(tk.END, "Selected Options: " + ", ".join(selected_options) + "\n")
    result_area.insert(tk.END, "Folders: " + ", ".join(selected_folders) + "\n")
    result_area.insert(tk.END, "Selected Checkboxes: " + ", ".join(selected_checkboxes) + "\n")
    result_area.config(state=tk.DISABLED)

# Browse folder function
def browse_folder(index):
    foldername = filedialog.askdirectory()
    if foldername:
        folder_vars[index].set(foldername)
        folder_labels[index].config(text=foldername)

# Toggle dropdown menu for checkboxes
def toggle_dropdown():
    if checkbox_frame.winfo_ismapped():
        checkbox_frame.grid_remove()
    else:
        checkbox_frame.grid(row=1, column=0, padx=5, pady=5, sticky='w')

# Create the main window
root = tk.Tk()
root.title("File Transfer")
root.geometry("800x500")
root.configure(bg="white")
root.withdraw()  # Hide the main window initially

show_splash()  # Show the splash screen

# Create a frame for the dropdown menus
dropdown_frame = tk.Frame(root, bg="white")
dropdown_frame.grid(row=0, column=0, padx=10, pady=10, sticky='w')

options = ["Zip and Cut", "Zip and Copy", "Copy", "Cut"]
combo_vars = []
combo1 = ttk.Combobox(dropdown_frame, values=options, state='readonly', width=30)
combo1.grid(row=0, column=0, pady=(0, 5))
combo_vars.append(combo1)

checkbox_options = ["Videos", "Images", "Text Files"]
checkbox_vars = [tk.BooleanVar() for _ in checkbox_options]

toggle_button = tk.Button(dropdown_frame, text="File Type", command=toggle_dropdown, bg="#007BFF", fg="black", font=("Helvetica", 10), relief="raised")
toggle_button.grid(row=1, column=0, pady=(30, 10), padx=90)

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

from_browse_button = tk.Button(folder_frame, text="Browse (from)", command=lambda: browse_folder(0), width=15, bg="#28a745", fg="black", relief="raised")
from_browse_button.grid(row=0, column=0, pady=(5, 10), sticky='w')

from_folder_label = tk.Label(folder_frame, text="", fg="black", width=50, font=("Helvetica", 10, "bold"), bg="lightyellow")
from_folder_label.grid(row=1, column=0, pady=(0, 10), sticky='w')
folder_labels.append(from_folder_label)

to_var = tk.StringVar()
folder_vars.append(to_var)

to_browse_button = tk.Button(folder_frame, text="Browse (to)", command=lambda: browse_folder(1), width=15, bg="#28a745", fg="black", relief="raised")
to_browse_button.grid(row=2, column=0, pady=(5, 10), sticky='w')

to_folder_label = tk.Label(folder_frame, text="", fg="black", width=50, font=("Helvetica", 10, "bold"), bg="lightyellow")
to_folder_label.grid(row=3, column=0, pady=(0, 10), sticky='w')
folder_labels.append(to_folder_label)

text_frame = tk.Frame(root, bg="white")
text_frame.grid(row=1, column=1, columnspan=1, padx=10, pady=10, sticky='w')

result_area = tk.Text(text_frame, height=15, width=42, state=tk.DISABLED, bg="white", fg="black", font=("Helvetica", 10))
result_area.pack(side=tk.LEFT)

scrollbar = tk.Scrollbar(text_frame, command=result_area.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

result_area.config(yscrollcommand=scrollbar.set)

display_button = tk.Button(root, text="Transfer!!", command=display_selection, width=55, height=2, bg="#007BFF", fg="black", relief="raised")
display_button.grid(row=2, column=0, pady=20, columnspan=2)

checkbox_frame.grid_remove()

# Close splash screen and main window
def on_closing():
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

# Start the main loop
root.mainloop()
