import os
import sys
import shutil
import subprocess

project_root = os.path.dirname(os.path.abspath(__file__))
gui_folder = os.path.join(project_root, "gui")
sys.path.insert(0, gui_folder)

'''
Clears the old pycache if it exists then runs the main program "MacroPadGUI.py"

Parameters:
    root_dir: 
        The directory of the root folder
'''
def clearCache(root_dir):
    for root, dirs, files in os.walk(root_dir): # go through root directories and its subdirectories where: root is current path, dirs is list of subdirectories in root, files is files in root
        for dir_name in dirs: # loop through each subdirectory in current directory
            if dir_name == "__pycache__": # if the subdirectory is the pycache
                full_path = os.path.join(root, dir_name) # make the absolute to "__pycache__"
                print(f"Deleting {full_path}") # tell user in console that pycache is being depeted with the full path
                shutil.rmtree(full_path, ignore_errors=True) # recursively delete "__pycache__" directory and all its contents, suppress errors as well

if __name__ == "__main__":
    project_root = os.path.dirname(os.path.abspath(__file__)) # get the absolute path the project is at 
    gui_folder = os.path.join(project_root, "gui") # set the gui folder to the project root
    clearCache(project_root) # call clearCache on project_root to delete all "__pycache__" folders inside project

    print("\nLaunching MacroPadGUI...\n") # output that gui is about to launch
    subprocess.run(["python", "-m", "gui.MacroPadGUI"], cwd=project_root) # run "MacroPadGUI.py" as a new python process