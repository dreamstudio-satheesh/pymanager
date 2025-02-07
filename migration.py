import os
import re
# from dotenv import load_dotenv

# load_dotenv()

# Fetch the project location from environment variables
base_directory = os.getenv('PROJECT_LOCATION')  # Ensure you set this in your .env file
if not base_directory:
    raise ValueError("PROJECT_LOCATION environment variable is not set in .env file.")

# Function to extract schema from migration files
def extract_migration_schema(migrations_path, output_file):
    schema_data = ""
    if os.path.exists(migrations_path):
        for root, _, files in os.walk(migrations_path):
            for file in files:
                if file.endswith('.php'):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()

                        # Regex to extract the Schema::create block
                        schema_matches = re.findall(
                            r"Schema::create\(.*?\{.*?\}\);", content, re.DOTALL
                        )

                        if schema_matches:
                            schema_data += f"\nFile: {file}\n"
                            for schema in schema_matches:
                                schema_data += f"{schema.strip()}\n"
    else:
        schema_data = f"[Path '{migrations_path}' does not exist]\n"

    # Save extracted schema to a file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(schema_data)

# Define the migrations folder path
migrations_path = os.path.join(base_directory, "database/migrations")
output_file = r"output_txts\migration_schemas.txt"

# Extract and save the schemas
extract_migration_schema(migrations_path, output_file)

print(f"Schema definitions extracted to {output_file}")
