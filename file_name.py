import os

def rename_files_in_folder(folder_path):
    """
    Renames files in a specified folder by adding a prefix and numbering them sequentially.
    """
    # Define the folder path, prefix, and file extension
    # Change this to your folder
    prefix = 'test_'
    file_extension = '.jpeg'  # or '.png', '.txt', etc.

    # List all files (filtering only ones with the right extension)
    files = [f for f in os.listdir(folder_path) if f.endswith(file_extension)]

    # Sort files alphabetically (optional)
    files.sort()

    # Rename files
    for i, filename in enumerate(files, start=1):
        new_name = f"{prefix}{i:03d}{file_extension}"  # Pads with zeros e.g. 001
        src = os.path.join(folder_path, filename)
        dst = os.path.join(folder_path, new_name)
        os.rename(src, dst)
        print(f"Renamed {filename} -> {new_name}")

rename_files_in_folder("/Users/sandrawang/Documents/Optometry_Apps/OCR_test/")
    


