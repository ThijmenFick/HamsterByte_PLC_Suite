import zipfile
import tempfile
import os

# Create a temporary directory
temp_dir_obj = tempfile.TemporaryDirectory(prefix="HamsterByteProject_")
temp_dir = temp_dir_obj.name

# Path to your zip file
zip_path = "SimpleProject.plcp"

# Extract contents to the temporary directory
with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall(temp_dir)

def st_to_c(filepath):




# Print the full paths of the extracted files
for root, dirs, files in os.walk(temp_dir):
    for file in files:
        print(os.path.join(root, file))

        if file.endswith(".st"):
            print("Structured Text")
        elif file.endswith(".tb"):
            print("Table File")
