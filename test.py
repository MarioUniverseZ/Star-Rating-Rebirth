import os
import algorithm
import getpass
from osu_file_parser import InvalidModeError
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime


def find_osu_root():
    with open (f'{osu_root}\\osu!\\osu!.{getpass.getuser()}.cfg', 'r', encoding='utf8') as f:
        cfg = f.readlines()
        for line in cfg:
            if line.startswith('BeatmapDirectory'):
                folder_path = line.split('=')[1].strip()
                break
        return folder_path
        
def process_folder(folder_path):
    for file in os.listdir(folder_path):
        if file.endswith('.osu'):
            file_path = os.path.join(folder_path, file)
            try:
                result = algorithm.calculate(file_path, 'NM', 6, 0.8, w_0, w_1, p_1, w_2, p_0)
                print(file, "|", f'{result:.4f}')
            except (InvalidModeError, SystemExit, ValueError):
                continue
            except KeyboardInterrupt:
                exit()

def calculate_result(root_folder):
    # Get all subfolders with their modification times
    subfolders = []
    for entry in os.scandir(root_folder):
        if entry.is_dir():
            mod_time = entry.stat().st_mtime
            subfolders.append((entry.path, mod_time))
    
    # Sort by modification time (newest first) and take first 50
    sorted_folders = sorted(subfolders, key=lambda x: x[1], reverse=True)[:50]
    folder_paths = [folder[0] for folder in sorted_folders]
    
    # Process folders in parallel using ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=20) as executor:
        executor.map(process_folder, folder_paths)                
if __name__ == "__main__":
    osu_root = os.getenv("LOCALAPPDATA")  # Update this to the path of your Test folder
    w_0, w_1, p_1, w_2, p_0 = 0.4, 2.7, 1.5, 0.27, 1.0

    folder_path = find_osu_root()
    calculate_result(folder_path)
