import sys
import os
import glob
import shutil

def get_resource_path(relative_path):
    """PyInstaller onefile專用"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def get_resultbackup_path():
    return get_resource_path("resultbackup")

def remove_resultbackup():
    result_path = get_resultbackup_path()
    resultbackup = glob.glob(f"{result_path}\\resultbackup_*.png")
    for item in resultbackup:
        os.remove(item)

def remove_resultbackup_folder():
    folder_path = get_resource_path("resultbackup")
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)