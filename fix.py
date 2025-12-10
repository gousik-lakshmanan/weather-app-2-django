import shutil
import os

# The path where the files are currently stuck
wrong_path = os.path.join('weather_project', 'weather_project')
# The path where they SHOULD be
correct_path = 'weather_project'

if os.path.exists(wrong_path):
    print(f"Found files in {wrong_path}...")
    # Move every file out to the parent folder
    for file_name in os.listdir(wrong_path):
        full_file_name = os.path.join(wrong_path, file_name)
        if os.path.isfile(full_file_name):
            shutil.move(full_file_name, correct_path)
            print(f"Moved: {file_name}")
    
    # Delete the empty folder
    os.rmdir(wrong_path)
    print("✅ Structure fixed successfully!")
else:
    print("⚠️  Folder 'weather_project/weather_project' not found. Check if it's already fixed.")