import tkinter as tk
from .beatmap_selection_area import BeatmapSelectionArea
from .result_area import ResultArea

class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SR-Rebirth")
        self.geometry("1000x600")
        self.resizable(False, False)

        self.beatmap_selection_area = BeatmapSelectionArea(self)
        self.result_area = ResultArea(self)