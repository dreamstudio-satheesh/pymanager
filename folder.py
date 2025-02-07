import os
# from dotenv import load_dotenv

# load_dotenv()

# Fetch the project location from environment variables
base_directory = os.getenv('PROJECT_LOCATION')  # Ensure you set this in your .env file
if not base_directory:
    raise ValueError("PROJECT_LOCATION environment variable is not set in .env file.")

# Function to generate the folder structure for specified directories
def generate_custom_folder_structure(base_directory, categories, prefix=""):
    structure = ""
    for category, info in categories.items():
        full_path = os.path.join(base_directory, info["path"])
        structure += f"{prefix}├── {category}/\n"
        if os.path.exists(full_path):
            for root, dirs, files in os.walk(full_path):
                relative_root = os.path.relpath(root, base_directory)
                indent_level = relative_root.count(os.sep)
                indent = prefix + "│   " * (indent_level + 1)

                # Add the current folder and its files
                for directory in dirs:
                    subfolder_path = os.path.join(root, directory)
                    structure += f"{indent}├── {directory}/\n"

                    # List files inside the subfolder
                    for sub_root, _, sub_files in os.walk(subfolder_path):
                        sub_indent = indent + "│   "
                        for file in sub_files:
                            if any(file.endswith(ext) for ext in info["extensions"]):
                                structure += f"{sub_indent}└── {file}\n"
                        break  # Prevent descending into deeper subdirectories

                # Add files in the current directory
                for file in files:
                    if any(file.endswith(ext) for ext in info["extensions"]):
                        structure += f"{indent}└── {file}\n"
                break  # Prevent further recursive traversal (limit to immediate children)
        else:
            structure += f"{prefix}│   └── [Path '{info['path']}' does not exist]\n"
    return structure

# Function to save the structure to a file
def save_structure_to_file(structure, output_file):
    with open(output_file, "w", encoding="utf-8") as file:
        file.write(structure)

# Define categories
categories = {
    "controllers": {"path": "app/Http/Controllers", "extensions": [".php"]},
    "middleware": {"path": "app/Http/Middleware", "extensions": [".php"]},
    "helpers": {"path": "app/Http/Helpers", "extensions": [".php"]},
    "models": {"path": "app/Models", "extensions": [".php"]},
    "traits": {"path": "app/Traits", "extensions": [".php"]},
    "livewire": {"path": "app/Livewire", "extensions": [".php"]},
    "views": {"path": "resources/views", "extensions": [".blade.php"]},
    "migrations": {"path": "database/migrations", "extensions": [".php"]},
}

# Generate the folder structure
project_name = "ServCP Mobile Repair Shop"
structure = f"Project: {project_name}\n\n"
structure += generate_custom_folder_structure(base_directory, categories)

# Save to a file
output_file = r"output_txts\project_structure.txt"
save_structure_to_file(structure, output_file)

print(f"Folder structure saved to {output_file}")
