import tkinter as tk
from tkinter import ttk, filedialog

# Display selections function
def display_selection():
    result_area.config(state=tk.NORMAL)
    result_area.delete(1.0, tk.END)  # Clear previous results
    selected_options = [combo.get() for combo in combo_vars if isinstance(combo, ttk.Combobox)]  # Get options from dropdown
    selected_folders = [folder_var.get() for folder_var in folder_vars]  # Get selected folders
    selected_checkboxes = [option for i, option in enumerate(checkbox_options) if checkbox_vars[i].get()]
    result_area.insert(tk.END, "Selected Options: " + ", ".join(selected_options) + "\n")
    result_area.insert(tk.END, "Folders: " + ", ".join(selected_folders) + "\n")
    result_area.insert(tk.END, "Selected Checkboxes: " + ", ".join(selected_checkboxes) + "\n")
    result_area.config(state=tk.DISABLED)

# Browse folder function
def browse_folder(index):
    foldername = filedialog.askdirectory()  # Open folder selection dialog
    folder_vars[index].set(foldername)  # Set the variable to the selected folder
    folder_labels[index].config(text=foldername)  # Update the label with the selected folder

# Toggle dropdown menu for checkboxes
def toggle_dropdown():
    if checkbox_frame.winfo_ismapped():
        checkbox_frame.grid_remove()
    else:
        checkbox_frame.grid(row=1, column=0, padx=5, pady=5, sticky='w')

# Create the main window
root = tk.Tk()
root.title("Simple Dummy App")
root.geometry("1366x768")  # Set window size to 1366x768 pixels

# Create a frame for the dropdown menus
dropdown_frame = tk.Frame(root)
dropdown_frame.grid(row=0, column=0, padx=(10, 5), pady=10)  # Add padding on the left side

# List of options for the dropdown menus
options = ["Option 1", "Option 2", "Option 3", "Option 4"]

# Create variables for dropdowns
combo_vars = []

# Create the first dropdown
combo1 = ttk.Combobox(dropdown_frame, values=options, state='readonly', width=30)
combo1.grid(row=0, column=0, pady=5)  # Add padding
combo_vars.append(combo1)

# Checkbox options
checkbox_options = ["Checkbox 1", "Checkbox 2", "Checkbox 3"]
checkbox_vars = [tk.BooleanVar() for _ in checkbox_options]

# Create a button to toggle the checkbox dropdown
toggle_button = tk.Button(dropdown_frame, text="Select Options", command=toggle_dropdown)
toggle_button.grid(row=1, column=0, pady=5)

# Frame for checkboxes (dropdown effect)
checkbox_frame = tk.Frame(dropdown_frame)

for i, option in enumerate(checkbox_options):
    checkbox = tk.Checkbutton(checkbox_frame, text=option, variable=checkbox_vars[i])
    checkbox.grid(row=i, column=0, sticky='w')

# Create a frame for the folder selection
folder_frame = tk.Frame(root)
folder_frame.grid(row=0, column=1, padx=10, pady=10)

# Create variables for folders
folder_vars = []
folder_labels = []  # To store labels for folder display

# Create Browse buttons for folder selection
for i in range(2):
    var = tk.StringVar()
    folder_vars.append(var)
    folder_label = tk.Label(folder_frame, text="", width=50)  # Label to display selected folder
    folder_label.grid(row=i, column=0, pady=5)
    folder_labels.append(folder_label)

    browse_button = tk.Button(folder_frame, text=f"Browse Folder {i + 1}", command=lambda idx=i: browse_folder(idx), width=20, height=2)
    browse_button.grid(row=i, column=1, pady=5)  # Place button next to the label

# Create a frame for the text area and scrollbar
text_frame = tk.Frame(root)
text_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

# Create a text area for results with adjusted size
result_area = tk.Text(text_frame, height=15, width=80, state=tk.DISABLED)  # Set height and width of text area
result_area.pack(side=tk.LEFT)

# Create a scrollbar for the text area
scrollbar = tk.Scrollbar(text_frame, command=result_area.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Configure the text area to use the scrollbar
result_area.config(yscrollcommand=scrollbar.set)

# Create a button to display selected options and folders
display_button = tk.Button(root, text="Show Selections", command=display_selection, width=20, height=2)  # Set width and height of button
display_button.grid(row=2, column=0, columnspan=2, pady=20)  # Span across two columns

# Pack the checkbox frame (initially hidden)
checkbox_frame.grid_remove()

# Start the main loop
root.mainloop()
