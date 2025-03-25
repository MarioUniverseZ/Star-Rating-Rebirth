import tkinter as tk
import getpass
import os
import re

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

        self.search_entry()

        self.load_beatmap_count = 0

        self.folders = self.generate_result()
        self.initial_result = self.folders
        self.current_index = 0
        self.beatmap_button()

    def canvas_area(self):
        self.canvas = tk.Canvas(self.frame, width=200)
        self.scrollbar = tk.Scrollbar(self.frame,
                                      orient="vertical",
                                      command=self.canvas.yview
                                      )
        self.scrollable_frame = tk.Frame(self.canvas)

        self.scrollable_frame.bind("<Configure>",
                                   lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw", width=200)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.pack(side="left", fill=tk.BOTH, expand=True)

    def search_entry(self):
        self.substring = tk.StringVar()
        self.substring.trace_add("write", self.callback)
        self.searchentry = tk.Entry(self.scrollable_frame,
                                       width=20,
                                       font=("Arial", 12),
                                       borderwidth=1,
                                       relief="solid",
                                       textvariable=self.substring,
                                       )
        self.searchentry.pack(side=tk.TOP, padx=10, pady=10)

    def callback(self, var, index, mode):
        self.search_result = []
        substr_casefold = self.substring.get().casefold()
        have_metacharacters = re.search(r'[\\/*?:\"<>|]', substr_casefold)
        content = [re.sub(r'[\\/*?:\"<>|]', "", (substr_casefold)),
                   re.sub(r'[\\/*?:\"<>|]', "_", (substr_casefold))]
        if content != '':
            for folder in self.initial_result:
                if have_metacharacters is not None: # If there are metacharacters in the search term
                    for content_item in content:
                        if content_item in folder[0].split("\\")[-1].casefold():
                            self.search_result.append(folder)
                else:
                    if content[0] in folder[0].split("\\")[-1].casefold():
                        self.search_result.append(folder)
            
            for widget in self.scrollable_frame.winfo_children():
                if widget.winfo_class() != "Entry":
                    widget.destroy()

            self.current_index = 0

            if self.search_result:
                self.folders = self.search_result
                self.load_more_buttons()
            else:
                # If no search results, you might want to show a message
                no_results_label = tk.Label(self.scrollable_frame, 
                                        text="No matching beatmaps found",
                                        font=("Arial", 11))
                no_results_label.pack(pady=20)
        else:
            for widget in self.scrollable_frame.winfo_children():
                if widget.winfo_class() != "Entry":
                    widget.destroy()
            self.folders = self.initial_result  # Restore original folders
            self.current_index = 0
            self.load_more_buttons()

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
        is_end = False
        if self.scrollbar.get()[1] > 0.95:
            if self.load_beatmap_count < 4:
                if self.current_index + 50 < len(self.folders):
                    self.current_index += 50
                else:
                    self.current_index = len(self.folders)
                    is_end = True
                self.load_more_buttons() if not is_end else None
                self.load_beatmap_count += 1
            else:
                pass


    def load_more_buttons(self):
        if self.current_index + 50 < len(self.folders):
            next_batch = self.folders[self.current_index:self.current_index + 50]
        else:
            next_batch = self.folders
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
            self.beatmapbutton.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)