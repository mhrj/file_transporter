import os
import shutil
import zipfile
from pathlib import Path


# File categories and extensions
FILE_TYPES = {
    "documents": [
        '.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt', '.tex', '.wps', 
        '.wpd', '.csv', '.xls', '.xlsx', '.ppt', '.pptx', '.log', '.md'
    ],
    "images": [
        '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.tif', '.svg', 
        '.ico', '.webp', '.heif', '.heic', '.raw', '.nef', '.cr2', '.orf', '.sr2'
    ],
    "videos": [
        '.mp4', '.mov', '.avi', '.mkv', '.flv', '.wmv', '.mpeg', '.mpg', 
        '.3gp', '.webm', '.m4v', '.m2ts', '.mts', '.vob', '.ogv'
    ],
    "audios": [
        '.mp3', '.wav', '.aac', '.flac', '.m4a', '.wma', '.ogg', '.opus', 
        '.amr', '.aiff', '.aif', '.mid', '.midi', '.ra', '.voc'
    ]
}

# Setup destination directory and return subdirectories for each file type
def setup_destination(main_dir, destination_dir=None):
    if not destination_dir:
        destination_dir = os.path.join(main_dir, "transported_files")
    os.makedirs(destination_dir, exist_ok=True)
    
    subdirectories = {}
    for category, extensions in FILE_TYPES.items():
        category_path = os.path.join(destination_dir, category)
        os.makedirs(category_path, exist_ok=True)
        subdirectories[category] = {ext.lower(): os.path.join(category_path, ext[1:].lower()) for ext in extensions}
        for ext_folder in subdirectories[category].values():
            os.makedirs(ext_folder, exist_ok=True)
    return destination_dir, subdirectories

# Encode file name for zipped files only to avoid name clashes
def encode_filename(filename):
    base, ext = os.path.splitext(filename)
    return f"{base.encode('utf-8').hex()}{ext}"

# Determine the category and extension for each file
def categorize_file(file):
    _, ext = os.path.splitext(file)
    ext = ext.lower()
    for category, extensions in FILE_TYPES.items():
        if ext in extensions:
            return category, ext
    return None, None

# Log individual files being processed
def log_scanned_file(file,callback_log):
    callback_log(f"Scanned file: {file}")

# Log the summary of moved/copied files
def log_summary(counts, sizes,callback_log):
    callback_log("\nFile processing complete.")
    for category, count in counts.items():
        size_mb = sizes[category] / (1024 * 1024)  # Convert bytes to MB
        callback_log(f"{category.capitalize()} - Moved {count} files, Total Size: {size_mb:.2f} MB")

# Get the list of file types to process
def get_selected_types(user_input):
    return [key for idx, key in enumerate(FILE_TYPES.keys(), 1) if idx in user_input]

# Create zip files of selected files in a category
def zip_files(files, destination_folder, extension):
    zip_name = encode_filename(f"{extension[1:]}_files.zip")
    zip_path = os.path.join(destination_folder, zip_name)
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for file in files:
            zipf.write(file, os.path.basename(file))
    return zip_path

# Process files by moving/copying/zipping based on the method
def process_files(main_dir, destination_dir, method, selected_types, log_callback):
    destination_dir, subdirectories = setup_destination(main_dir, destination_dir)
    
    counts = {category: 0 for category in FILE_TYPES}
    sizes = {category: 0 for category in FILE_TYPES}

    log_callback("Starting file processing...\n")
    
    for root, _, files in os.walk(main_dir):
        # Skip the destination directory if it's inside main_dir
        if os.path.commonpath([root, destination_dir]) == destination_dir:
            continue

        for file in files:
            file_path = os.path.join(root, file)
            category, ext = categorize_file(file)
            if category and category in selected_types:
                log_scanned_file(file,log_callback)
                dest_folder = subdirectories[category][ext]
                file_size = os.path.getsize(file_path)
                
                # Update counts and sizes
                counts[category] += 1
                sizes[category] += file_size

                # Move, Copy, or Zip based on selected method
                handle_file_action(file_path, dest_folder, method, ext)
                
    log_summary(counts, sizes,log_callback)

# Handle individual file action based on the selected method
def handle_file_action(file_path, dest_folder, method, extension):
    if method == 1:  # Zip then move
        zip_files([file_path], dest_folder, extension)
        os.remove(file_path)
    elif method == 2:  # Move
        move_or_skip(file_path, dest_folder)
    elif method == 3:  # Zip then copy
        zip_files([file_path], dest_folder, extension)
    elif method == 4:  # Copy
        copy_or_skip(file_path, dest_folder)

# Move file to destination, skipping if file already exists
def move_or_skip(file_path, dest_folder):
    dest_path = os.path.join(dest_folder, os.path.basename(file_path))
    if not os.path.exists(dest_path):
        shutil.move(file_path, dest_path)
    else:
        os.remove(file_path)

# Copy file to destination, skipping if file already exists
def copy_or_skip(file_path, dest_folder):
    dest_path = os.path.join(dest_folder, os.path.basename(file_path))
    if not os.path.exists(dest_path):
        shutil.copy(file_path, dest_path)
