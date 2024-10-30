import os
import shutil
import zipfile
import time
import hashlib

# File categories and extensions
FILE_TYPES = {
    "documents": ['.pdf', '.doc', '.docx', '.txt', '.csv', '.xls', '.xlsx', '.ppt', '.log', '.md'],
    "images": ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.ico', '.webp', '.raw'],
    "videos": ['.mp4', '.mov', '.avi', '.mkv', '.flv', '.wmv', '.mpeg', '.webm'],
    "audios": ['.mp3', '.wav', '.aac', '.flac', '.m4a', '.wma', '.ogg']
}

# Setup destination directory and subdirectories for each file type
def setup_destination(main_dir, destination_dir=None):
    destination_dir = destination_dir or os.path.join(main_dir, "transported_files")
    os.makedirs(destination_dir, exist_ok=True)
    
    subdirectories = {}
    for category, extensions in FILE_TYPES.items():
        category_path = os.path.join(destination_dir, category)
        os.makedirs(category_path, exist_ok=True)
        subdirectories[category] = {ext.lower(): os.path.join(category_path, ext[1:].lower()) for ext in extensions}
        for folder in subdirectories[category].values():
            os.makedirs(folder, exist_ok=True)
    return destination_dir, subdirectories

# Encode zip file name using salt and timestamp for uniqueness
def encode_zip_name(extension):
    unique_id = hashlib.sha256(os.urandom(16) + str(int(time.time())).encode()).hexdigest()
    return f"{extension[1:]}_{unique_id}.zip"

# Determine category and extension of a file
def categorize_file(file):
    _, ext = os.path.splitext(file)
    for category, extensions in FILE_TYPES.items():
        if ext.lower() in extensions:
            return category, ext.lower()
    return None, None

# Group files by extension and create zip files for each group
def zip_files_by_extension(files_by_extension, destination_dir, subdirectories, method):
    for extension, files in files_by_extension.items():
        if files:
            zip_name = encode_zip_name(extension)
            category = next((cat for cat, exts in FILE_TYPES.items() if extension in exts), None)
            dest_folder = subdirectories[category][extension] if category else destination_dir
            zip_path = os.path.join(dest_folder, zip_name)
            
            with zipfile.ZipFile(zip_path, 'w') as zipf:
                for file in files:
                    zipf.write(file, os.path.basename(file))
                    if method == 1:  # Zip and Move - delete original after zipping
                        os.remove(file)

# Perform the selected file action (move, copy, zip then move/copy)
def handle_file_action(file_path, dest_folder, method, files_by_extension=None, extension=None):
    if method in (1, 3):  # Zip methods
        files_by_extension.setdefault(extension, []).append(file_path)
    elif method == 2:  # Move
        move_or_skip(file_path, dest_folder)
    elif method == 4:  # Copy
        copy_or_skip(file_path, dest_folder)

# Move file, skipping if it exists
def move_or_skip(file_path, dest_folder):
    dest_path = os.path.join(dest_folder, os.path.basename(file_path))
    if not os.path.exists(dest_path):
        shutil.move(file_path, dest_path)
    else:
        os.remove(file_path)

# Copy file, skipping if it exists
def copy_or_skip(file_path, dest_folder):
    dest_path = os.path.join(dest_folder, os.path.basename(file_path))
    if not os.path.exists(dest_path):
        shutil.copy(file_path, dest_path)

# Process files by organizing and applying the chosen action
def process_files(main_dir, destination_dir, method, selected_types, log_callback):
    destination_dir, subdirectories = setup_destination(main_dir, destination_dir)
    counts, sizes, files_by_extension = {cat: 0 for cat in FILE_TYPES}, {cat: 0 for cat in FILE_TYPES}, {}

    log_callback("Starting file processing...\n")
    
    for root, _, files in os.walk(main_dir):
        if os.path.commonpath([root, destination_dir]) == destination_dir:
            continue

        for file in files:
            file_path = os.path.join(root, file)
            category, ext = categorize_file(file)
            if category and category in selected_types:
                dest_folder = subdirectories[category][ext]
                counts[category] += 1
                sizes[category] += os.path.getsize(file_path)

                # Log and handle file action
                log_callback(f"Processing file: {file}")
                handle_file_action(file_path, dest_folder, method, files_by_extension, ext)

    # Create zip files if zip methods are selected
    if method in (1, 3):
        zip_files_by_extension(files_by_extension, destination_dir, subdirectories, method)
    
    log_summary(counts, sizes, log_callback)

# Log summary of processed files
def log_summary(counts, sizes, callback_log):
    callback_log("\nFile processing complete.")
    for category, count in counts.items():
        size_mb = sizes[category] / (1024 * 1024)  # Convert bytes to MB
        callback_log(f"{category.capitalize()} - Processed {count} files, Total Size: {size_mb:.2f} MB")
