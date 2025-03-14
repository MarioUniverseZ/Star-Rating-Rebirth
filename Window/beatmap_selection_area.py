import tkinter as tk
import getpass
import os

class BeatmapSelectionArea(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.frame = tk.Frame(master,
                              width=250,
                              height=600,
                              padx=10,
                              pady=10
                              )

        self.frame.pack_propagate(False)
        self.frame.pack(side=tk.LEFT, fill=tk.BOTH)

        self.canvas_area()
        self.scrollbar.bind("<Motion>", self.check_scroll)

        self.folders = self.generate_result()
        self.current_index = 0
        self.beatmap_button()

    def canvas_area(self):
        self.canvas = tk.Canvas(self.frame, width=200)
        self.scrollbar = tk.Scrollbar(self.frame,
                                      orient="vertical",
                                      command=self.canvas.yview
                                      )
        self.scrollable_frame = tk.Frame(self.canvas)

        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        self.scrollable_frame.bind("<Configure>",
                                   lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw", width=200)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.pack(side="left", fill=tk.BOTH, expand=True)

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def beatmap_button(self):
        if self.folders:
            self.load_more_buttons()

    def generate_result(self):
        osu_root = os.getenv("LOCALAPPDATA")
        with open (f'{osu_root}\\osu!\\osu!.{getpass.getuser()}.cfg', 'r', encoding='utf8') as f:
            cfg = f.readlines()
            for line in cfg:
                if line.startswith('BeatmapDirectory'):
                    folder_path = line.split('=')[1].strip()
                    break
        # Get all subfolders with their modification times
        subfolders = []
        for entry in os.scandir(folder_path):
            if entry.is_dir():
                mod_time = entry.stat().st_mtime
                subfolders.append((entry.path, mod_time))
    
        # Sort by modification time (newest first) and take first 50
        sorted_folders = sorted(subfolders, key=lambda x: x[1], reverse=True)
        return sorted_folders

    def check_scroll(self, event):
        if self.scrollbar.get()[1] > 0.9:
            self.load_more_buttons()

    def load_more_buttons(self):
        next_batch = self.folders[self.current_index:self.current_index + 50]
        for item in next_batch:
            self.artist_title = tk.StringVar()
            title = item[0].split('\\')[-1]
            self.artist_title.set(title)
            self.beatmapbutton = tk.Button(self.scrollable_frame,
                width=22,
                height=4,
                padx=10,
                font=("Arial", 11),
                wraplength=180,
                textvariable=self.artist_title,
                command=lambda x=item[0]: self.master.result_area.display(x)
                )
            self.beatmapbutton.pack(side=tk.TOP, fill=tk.X, pady=5)
        self.current_index += 50