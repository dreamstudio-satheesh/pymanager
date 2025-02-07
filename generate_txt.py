import os
# from dotenv import load_dotenv

# load_dotenv()

# Fetch the project location from environment variables
base_directory = os.getenv('PROJECT_LOCATION')  # Ensure you set this in your .env file
if not base_directory:
    raise ValueError("PROJECT_LOCATION environment variable is not set in .env file.")

# Define output directory
output_dir = r"output_txts"

# Create output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Function to fetch files in a directory recursively
def get_files_in_directory(directory, extensions):
    file_list = []
    for root, _, files in os.walk(directory):
        for file in files:
            if any(file.endswith(ext) for ext in extensions):
                file_list.append(os.path.join(root, file))
    return file_list

# Function to write files to separate TXT files with context and standardized keywords
def write_files_to_txt(file_list, output_dir, category):
    output_file = os.path.join(output_dir, f"{category}.txt")
    with open(output_file, "w", encoding="utf-8") as txt_file:
        txt_file.write(f"=== {category.upper()} ===\n")
        txt_file.write("-" * 80 + "\n\n")
        for file_path in file_list:
            file_name = os.path.basename(file_path)
            relative_path = os.path.relpath(file_path, base_directory)

            # Write file metadata with standardized keywords
            txt_file.write(f"File: {file_name}\n")
            txt_file.write(f"Path: {relative_path}\n")
            txt_file.write(f"Purpose: Automatically extracted.\n\n")

            # Write file content
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    txt_file.write(content)
            except Exception as e:
                txt_file.write(f"Error reading file: {e}\n")

            txt_file.write("\n" + "-" * 80 + "\n\n")  # Separator between files

    print(f"{category.capitalize()} written to {output_file}")

# Directories and their file extensions
categories = {
    "controllers": {"path": "app/Http/Controllers", "extensions": [".php"]},
    "models": {"path": "app/Models", "extensions": [".php"]},
    "livewire": {"path": "app/Livewire", "extensions": [".php"]},
    "traits": {"path": "app/Traits", "extensions": [".php"]},
    "helpers": {"path": "app/Http/Helpers", "extensions": [".php"]},
    "views": {"path": "resources/views", "extensions": [".blade.php"]},
}

# Process each category and write to separate files
for category, info in categories.items():
    full_path = os.path.join(base_directory, info["path"])
    all_files = get_files_in_directory(full_path, info["extensions"])
    if all_files:
        write_files_to_txt(all_files, output_dir, category)
    else:
        print(f"No files found in {info['path']}.")
