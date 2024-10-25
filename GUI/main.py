import tkinter as tk
from tkinter import ttk, filedialog, messagebox

# Splash Screen
def show_splash():
    splash = tk.Toplevel()
    splash.title("Welcome")
    splash.geometry("400x200")
    splash.configure(bg="#007BFF")  # Blue background
    splash.overrideredirect(True)  # Remove window decorations

    # Center the splash screen
    splash_width = 400
    splash_height = 200
    screen_width = splash.winfo_screenwidth()
    screen_height = splash.winfo_screenheight()
    x = (screen_width // 2) - (splash_width // 2)
    y = (screen_height // 2) - (splash_height // 2)
    splash.geometry(f"{splash_width}x{splash_height}+{x}+{y}")

    label = tk.Label(splash, text="Welcome to the File Transfer App", bg="#007BFF", font=("Helvetica", 16, "bold"), fg="black")
    label.pack(pady=50)

    splash.after(2000, lambda: [splash.destroy(), root.deiconify()])  # Close after 2 seconds

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
        update_dropdown()  # Update options when shown

# Update dropdown values directly
def update_dropdown():
    selected_types = [option for i, option in enumerate(checkbox_options) if checkbox_vars[i].get()]
    if selected_types:
        new_options = [f"Option for {type_}" for type_ in selected_types]
        combo1['values'] = new_options
    else:
        combo1['values'] = options
    combo1.set('')

# Create the main window
root = tk.Tk()
root.title("File Transfer")
root.geometry("800x500")
root.configure(bg="#f0f8ff")  # Set light background color for root
root.withdraw()  # Hide the main window initially

show_splash()  # Show the splash screen

# Create a frame for the dropdown menus
dropdown_frame = tk.Frame(root, bg="#f0f8ff")
dropdown_frame.grid(row=0, column=0, padx=10, pady=10, sticky='w')

# List of options for the dropdown menus
options = ["Zip and Cut", "Zip and Copy", "Copy", "Cut"]

# Create variables for dropdowns
combo_vars = []
combo1 = ttk.Combobox(dropdown_frame, values=options, state='readonly', width=30)
combo1.grid(row=0, column=0, pady=(0, 5))
combo_vars.append(combo1)

# Checkbox options
checkbox_options = ["Videos", "Images", "Text Files"]
checkbox_vars = [tk.BooleanVar() for _ in checkbox_options]

# Create a button to toggle the checkbox dropdown
toggle_button = tk.Button(dropdown_frame, text="File Type", command=toggle_dropdown, bg="#007BFF", fg="white", font=("Helvetica", 10), relief="raised")
toggle_button.grid(row=1, column=0, pady=(30, 10), padx=90)

# Frame for checkboxes
checkbox_frame = tk.Frame(dropdown_frame, bg="#f0f8ff")
for i, option in enumerate(checkbox_options):
    checkbox = tk.Checkbutton(checkbox_frame, text=option, variable=checkbox_vars[i], bg="#f0f8ff")
    checkbox.grid(row=i, column=0, sticky='w')

# Create a frame for the folder selection
folder_frame = tk.Frame(root, bg="#f0f8ff")
folder_frame.grid(row=1, column=0, padx=10, pady=10, sticky='w')

# Create variables for folders
folder_vars = []
folder_labels = []

# Define first browse button ("From")
from_var = tk.StringVar()
folder_vars.append(from_var)

from_browse_button = tk.Button(folder_frame, text="Browse (from)", command=lambda: browse_folder(0), width=15, height=1, bg="#28a745", fg="white", relief="raised")
from_browse_button.grid(row=0, column=0, pady=(5, 10), sticky='w')

from_folder_label = tk.Label(folder_frame, text="", width=50, font=("Helvetica", 10, "bold"), bg="lightyellow")
from_folder_label.grid(row=1, column=0, pady=(0, 10), sticky='w')
folder_labels.append(from_folder_label)

# Define second browse button ("To")
to_var = tk.StringVar()
folder_vars.append(to_var)

to_browse_button = tk.Button(folder_frame, text="Browse (to)", command=lambda: browse_folder(1), width=15, height=1, bg="#28a745", fg="white", relief="raised")
to_browse_button.grid(row=2, column=0, pady=(5, 10), sticky='w')

to_folder_label = tk.Label(folder_frame, text="", width=50, font=("Helvetica", 10, "bold"), bg="lightyellow")
to_folder_label.grid(row=3, column=0, pady=(0, 10), sticky='w')
folder_labels.append(to_folder_label)

# Create a frame for the text area and scrollbar
text_frame = tk.Frame(root, bg="#f0f8ff")
text_frame.grid(row=1, column=1, columnspan=1, padx=10, pady=10, sticky='w')

# Create a text area for results
result_area = tk.Text(text_frame, height=15, width=42, state=tk.DISABLED, bg="white", font=("Helvetica", 10))
result_area.pack(side=tk.LEFT)

# Create a scrollbar for the text area
scrollbar = tk.Scrollbar(text_frame, command=result_area.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Configure the text area to use the scrollbar
result_area.config(yscrollcommand=scrollbar.set)

# Create a button to display selected options and folders
display_button = tk.Button(root, text="Transfer!!", command=display_selection, width=55, height=2, bg="#007BFF", fg="white", relief="raised")
display_button.grid(row=2, column=0, pady=20, columnspan=2)

# Pack the checkbox frame (initially hidden)
checkbox_frame.grid_remove()

# Start the main loop
root.mainloop()
