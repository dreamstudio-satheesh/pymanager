import subprocess
import os
from dotenv import load_dotenv

load_dotenv()

# Define the scripts to run
scripts = [
    "generate_txt.py",
    "migration.py",
    "folder.py"
]

# Function to run a script
def run_script(script_name):
    try:
        print(f"Running {script_name}...")
        result = subprocess.run(["python", script_name], check=True, text=True, capture_output=True)
        print(result.stdout)  # Print script output
    except subprocess.CalledProcessError as e:
        print(f"Error running {script_name}:\n{e.stderr}")

# Ensure the scripts exist
for script in scripts:
    if not os.path.exists(script):
        print(f"Error: {script} not found. Make sure all scripts are in the same directory.")
        exit(1)

# Run the scripts one by one
for script in scripts:
    run_script(script)

print("All scripts executed successfully.")
