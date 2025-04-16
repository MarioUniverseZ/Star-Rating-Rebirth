import tkinter as tk
import win32gui, win32con, win32api
import random
import pyglet
import os
from pathlib import Path
from .render_font import RenderFont
from .result_process import ResultProcess
from PIL import ImageTk, Image, ImageFilter
from concurrent.futures import ProcessPoolExecutor, as_completed

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

        self.previous_item = None
        self.current_item = None
        self.previous_mod = None
        self.current_mod = None

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
        from .main_window import remove_resultbackup, get_resultbackup_path
        result_path = get_resultbackup_path()

        if self.current_item:
            self.previous_item = self.current_item
        if self.current_mod:
            self.previous_mod = self.current_mod
        self.current_item = item
        self.current_mod = mod

        same_item = bool(self.previous_item == self.current_item)
        previous_moditem = os.path.isfile(f'{result_path}\\resultbackup_{mod}.png')
        condition = bool(same_item and previous_moditem)

        # calculate only when the item is changed or all mods are not calculated
        if not condition:
            if not same_item:
                remove_resultbackup()
            
            rp = ResultProcess
            files = os.listdir(item)
            cpu_count = os.cpu_count()
            results = []
            backgrounds = []
            with ProcessPoolExecutor() as executor:
                chunk_size = 1 if len(files) <= cpu_count else len(files) // cpu_count
                futures = [executor.submit(rp._resultprocess, rp, item, files[i:i+chunk_size], mod) for i in range(0, len(files), chunk_size)]
                for future in as_completed(futures):
                    result, background = future.result()
                    results.append(result)
                    backgrounds.append(background)

                if not results:
                    print("No osu files found in the folder")

            results = [x for x in results if x != []]
            results = [x for xs in results for x in xs]
            backgrounds = [x for x in backgrounds if x != []]
            backgrounds = [x for xs in backgrounds for x in xs]
            
            result = sorted(results, key=lambda x: x['SR'], reverse=False)
            background = list(set(backgrounds)) if backgrounds else []

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
            self.img_backup = Image.new("RGBA", (700, new_canvas_height))
            for i in range(len(result)):
                img_diffname = ImageTk.PhotoImage(self.font.get_render(32, str(result[i]['diffname'])))
                img_sr = ImageTk.PhotoImage(self.font.get_render(48, result[i]['SR']))
                self.images.extend([img_diffname, img_sr])
                self.canvas.create_image(50, 22 + i * 65, image=img_diffname, anchor=tk.NW)
                self.img_backup.paste(ImageTk.getimage(img_diffname), (50, 22 + i * 65))
                self.canvas.create_image(450, 15 + i * 65, image=img_sr, anchor=tk.NW)
                self.img_backup.paste(ImageTk.getimage(img_sr), (450, 15 + i * 65))

            self.img_backup.save(f'{result_path}\\resultbackup_{mod}.png')

        else:
            self.canvas.delete("all") # prevent different sort order across mods
            self.backup = []
            img = Image.open(f'{result_path}\\resultbackup_{mod}.png')
            new_canvas_height = img.height
            self.canvas.configure(scrollregion=(0, 0, 0, new_canvas_height))
            tk_img = ImageTk.PhotoImage(img)
            self.backup.extend([tk_img])
            self.canvas.create_image(0, 0, image=tk_img, anchor=tk.NW)