import tkinter as tk
import os
import glob
from pathlib import Path
from .beatmap_selection_area import BeatmapSelectionArea
from .result_area import ResultArea
from .game_modifier_area import GameModifierArea

def get_resultbackup_path():
    return str(Path(__file__).parents[0] / "resultbackup")

def remove_resultbackup():
    result_path = get_resultbackup_path()
    resultbackup = glob.glob(f"{result_path}\\resultbackup_*.png")
    for item in resultbackup:
        os.remove(item)

class Window(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("SR-Rebirth")
        self.geometry("1086x600")
        self.resizable(False, False)

        self.beatmap_selection_area = BeatmapSelectionArea(self)
        self.game_modifier_area = GameModifierArea(self)
        self.result_area = ResultArea(self)

        result_path = get_resultbackup_path()
        os.makedirs(result_path, exist_ok=True)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        remove_resultbackup()
        self.quit()