import tkinter as tk
import pyglet
import os
import sys
sys.path.append("..")
from osu_file_parser import parser, InvalidModeError
from algorithm import calculate
from pathlib import Path
from .render_font import RenderFont
from PIL import ImageTk

class ResultArea(tk.Frame):

    def __init__(self, master):
        super().__init__(master)

        pyglet.options['win32_gdi_font'] = True
        fontpath = Path(__file__).parents[0] / "font\\TorusNotched-Regular.ttf"
        pyglet.font.add_file(str(fontpath))
        self.font = RenderFont(str(fontpath))
        # self.img = ImageTk.PhotoImage(self.font.get_render(20, "1234567890"))

        self.is_executed = False

        self.frame = tk.Frame(master,
                              width=750,
                              height=600,
                              padx=10,
                              pady=10,
                              )
        self.frame.pack_propagate(False)
        self.frame.pack(side=tk.LEFT, fill=tk.BOTH)

        self.canvas_area()

    def canvas_area(self):
        self.canvas = tk.Canvas(self.frame,
                                width=700,
                                bd=5)
        self.scrollbar = tk.Scrollbar(self.frame,
                                      orient="vertical"
                                      )

        self.scrollable_frame = tk.Frame(self.canvas)
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw", width=700)
        self.scrollable_frame.bind("<Configure>", self._configure_scroll_region)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # self.scrollbar.config(command=self.canvas.yview)

        # self.canvas.create_image(10, 10, image=self.img, anchor=tk.NW)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        
    def _configure_scroll_region(self, event):
        # Update scroll region when content changes
        if self.is_executed:
            self.canvas.configure(height = new_canvas_height,
                                  scrollregion=self.canvas.bbox("all"))
            self.scrollbar.configure(command=self.canvas.yview)
            self.canvas.configure(yscrollcommand=self.scrollbar.set)

    def display(self, item):
        w_0, w_1, p_1, w_2, p_0 = 0.4, 2.7, 1.5, 0.27, 1.0

        result = []
        for file in os.listdir(item):
            if file.endswith('.osu'):
                try:
                    file_path = os.path.join(item, file)
                    metadata = parser(file_path)
                    title, artist, diffname = metadata.get_metadata()
                    sr = calculate(file_path, 'NM', 6, 0.8, w_0, w_1, p_1, w_2, p_0)
                    result.append({
                        "title": title,
                        "artist": artist,
                        "diffname": diffname,
                        "SR": sr
                    })
                    # print(file, "|", f'{result:.4f}')
                except (InvalidModeError, SystemExit, ValueError) as e:
                    print(e)
        
        result = sorted(result, key=lambda x: x['SR'], reverse=False)
        global new_canvas_height
        new_canvas_height = 150 + len(result) * 80
        self.canvas.delete("all")
        self.images = []
        for i in range(len(result)):
            img_diffname = ImageTk.PhotoImage(self.font.get_render(32, str(result[i]['diffname'])))
            img_sr = ImageTk.PhotoImage(self.font.get_render(50, result[i]['SR']))
            self.images.extend([img_diffname, img_sr])
            self.canvas.create_image(30, 20 + i * 80, image=img_diffname, anchor=tk.NW)
            self.canvas.create_image(430, 10 + i * 80, image=img_sr, anchor=tk.NW)
        self.is_executed = True