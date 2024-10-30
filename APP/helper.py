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

def setup_destination(destination_dir):
    """Create main category directories in the destination."""
    os.makedirs(destination_dir, exist_ok=True)
    
    subdirectories = {category: os.path.join(destination_dir, category) for category in FILE_TYPES}
    for path in subdirectories.values():
        os.makedirs(path, exist_ok=True)
    return destination_dir, subdirectories

def categorize_file(file):
    """Return the category and extension of the file if it matches a known type."""
    _, ext = os.path.splitext(file)
    for category, extensions in FILE_TYPES.items():
        if ext.lower() in extensions:
            return category
    return None

def move_or_copy_or_skip(file_path, dest_folder, method):
    """Move file to destination if not already present."""
    dest_path = os.path.join(dest_folder, os.path.basename(file_path))
    if not os.path.exists(dest_path):
        if method == 2:
            shutil.move(file_path, dest_path)
        else:
            shutil.copy(file_path, dest_path)

def handle_file(file_path, category, dest_folder, method, files_by_category=None):
    """Handle the file based on the selected method (move, copy, zip then move/copy)."""
    if method in (1, 3):  # Zip methods
        files_by_category.setdefault(category, []).append(file_path)
    elif method == 2:  # Move
        move_or_copy_or_skip(file_path, dest_folder, method)
    elif method == 4:  # Copy
        move_or_copy_or_skip(file_path, dest_folder, method)

def encode_zip_name(category):
    """Generate a unique zip file name for each category based on a timestamp and random salt."""
    unique_id = hashlib.sha256(os.urandom(16) + str(int(time.time())).encode()).hexdigest()
    return f"{category}_{unique_id}.zip"

def zip_files_by_category(files_by_category, subdirectories, method):
    """Create a zip file for each category and delete originals if method is 'zip and move'."""
    for category, files in files_by_category.items():
        if not files:
            continue
        zip_name = encode_zip_name(category)
        zip_path = os.path.join(subdirectories[category], zip_name)
        
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for file in files:
                zipf.write(file, os.path.basename(file))
                if method == 1:  # Zip and Move - delete original after zipping
                    os.remove(file)

def log_summary(counts, sizes, callback_log):
    """Log the summary of processed files by category and total size."""
    callback_log("\nFile processing complete.\n")
    for category, count in counts.items():
        size_mb = sizes[category] / (1024 * 1024)  # Convert bytes to MB
        callback_log(f"{category.capitalize()} \n\t Processed {count} files, Total Size: {size_mb:.2f} MB")

def process_files(main_dir, destination_dir, method, selected_types, log_callback):
    """Process files in the main directory according to the selected method and type."""
    destination_dir, subdirectories = setup_destination(destination_dir)
    counts, sizes, files_by_category = {cat: 0 for cat in FILE_TYPES}, {cat: 0 for cat in FILE_TYPES}, {}

    log_callback("Starting file processing...\n")
    
    for file in os.listdir(main_dir):
        file_path = os.path.join(main_dir, file)
        if os.path.isfile(file_path):
            category = categorize_file(file)
            if category and category in selected_types:
                dest_folder = subdirectories[category]
                counts[category] += 1
                sizes[category] += os.path.getsize(file_path)

                log_callback(f"Processing file: {file}")
                handle_file(file_path, category, dest_folder, method, files_by_category)

    if method in (1, 3):  # Zip methods
        zip_files_by_category(files_by_category, subdirectories, method)
    
    log_summary(counts, sizes, log_callback)
