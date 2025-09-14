import tkinter as tk
import os
from Window.interface.beatmap_selection_area import BeatmapSelectionArea
from Window.interface.result_area import ResultArea
from Window.interface.game_modifier_area import GameModifierArea
from Window.function.window_func import get_resultbackup_path, remove_resultbackup_folder

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
        remove_resultbackup_folder()
        self.quit()