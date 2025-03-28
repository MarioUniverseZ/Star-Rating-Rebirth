import tkinter as tk
import win32gui, win32con, win32api
import random
import pyglet
import os
import sys
sys.path.append("..")
from osu_file_parser import parser, InvalidModeError
from algorithm import calculate
from pathlib import Path
from .render_font import RenderFont
from PIL import ImageTk, Image, ImageFilter

class ResultArea(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        pyglet.options['win32_gdi_font'] = True
        fontpath = Path(__file__).parents[0] / "font\\TorusNotched-Regular.ttf"
        pyglet.font.add_file(str(fontpath))
        self.font = RenderFont(str(fontpath))

        self.frame = tk.Frame(master,
                              width=750,
                              padx=10,
                              pady=10
                              )
        self.frame.pack_propagate(False)
        self.frame.pack(side=tk.RIGHT, fill=tk.BOTH)

        self.canvas_area()

    def canvas_area(self):
        # canvas container
        self.canvas_container = tk.Frame(self.frame)
        self.canvas_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # background canvas(for beatmap bg)
        self.bg_canvas = tk.Canvas(self.canvas_container,
                                   width=700,
                                   )
        self.bg_canvas.place(x=0, y=0, relwidth=1, relheight=1)
        
        # foreground canvas(for diffname, sr)
        self.canvas = tk.Canvas(self.bg_canvas,
                                width=700,
                                highlightthickness=0,
                                bd=0,
                                bg='#7F7F7F',
                                )
        
        # credit: https://stackoverflow.com/a/70150296
        hwnd = self.canvas.winfo_id()
        colorkey = win32api.RGB(127, 127, 127)
        wnd_exstyle = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
        new_exstyle = wnd_exstyle | win32con.WS_EX_LAYERED
        win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, new_exstyle)
        win32gui.SetLayeredWindowAttributes(hwnd, colorkey, 255, win32con.LWA_COLORKEY)

        self.scrollbar = tk.Scrollbar(self.frame,
                                      orient="vertical",
                                      command=self.canvas.yview
                                      )

        self.scrollable_frame = tk.Frame(self.canvas,
                              background='')

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw", width=700)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.place(x=0, y=-1, relwidth=1, relheight=1)

    def display(self, item, mod):
        w_0, w_1, p_1, w_2, p_0 = 0.4, 2.7, 1.5, 0.27, 1.0

        result = []
        background = []
        osu_count = 0
        for file in os.listdir(item):
            if file.endswith('.osu'):
                try:
                    osu_count += 1
                    file_path = os.path.join(item, file)
                    metadata = parser(file_path)
                    title, artist, diffname, bg = metadata.get_metadata()
                    sr = calculate(file_path, mod, 6, 0.8, w_0, w_1, p_1, w_2, p_0)
                    result.append({
                        "title": title,
                        "artist": artist,
                        "diffname": diffname,
                        "SR": sr
                    })
                    background.append(f'{item}\\{bg}')
                    # print(file, "|", f'{result:.4f}')
                except (InvalidModeError, SystemExit, ValueError) as e:
                    print(file_path.split("\\")[-1].rstrip(".osu"), e)
        
        if osu_count == 0:
            print("No osu file found in the folder")

        result = sorted(result, key=lambda x: x['SR'], reverse=False)
        background = list(set(background))

        new_canvas_height = len(result) * 65 + 15

        self.canvas.configure(scrollregion=(0, 0, 0, new_canvas_height))
        self.canvas.delete("all")

        for item in background:
            if item.split("\\")[-1] == "None":
                background.remove(item)
        
        if background:
            self.choice = random.choice(background)
            self.bg_candidate = Image.open(self.choice)
            width, height = self.bg_candidate.size
            ratio = width / height
            if ratio >= 1:
                self.bg_candidate = self.bg_candidate.resize((int(750*ratio), 750))
            else:
                self.bg_candidate = self.bg_candidate.resize((750, int(750/ratio)))
            self.bg_candidate.putalpha(111)
            self.bg_candidate = self.bg_candidate.filter(ImageFilter.BLUR)
            self.bg_candidate = ImageTk.PhotoImage(self.bg_candidate)
            self.bg_canvas.create_image(356, 290, image=self.bg_candidate, anchor=tk.CENTER)
        else:
            self.bg_canvas.delete("all")

        self.images = []
        for i in range(len(result)):
            img_diffname = ImageTk.PhotoImage(self.font.get_render(32, str(result[i]['diffname'])))
            img_sr = ImageTk.PhotoImage(self.font.get_render(48, result[i]['SR']))
            self.images.extend([img_diffname, img_sr])
            self.canvas.create_image(50, 22 + i * 65, image=img_diffname, anchor=tk.NW)
            self.canvas.create_image(450, 15 + i * 65, image=img_sr, anchor=tk.NW)