import tkinter as tk
from PIL import ImageTk
from pathlib import Path

class GameModifierArea(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.frame =  tk.Frame(master,
                               width=86
                               )
        self.frame.pack_propagate(False)
        self.frame.pack(side=tk.LEFT, fill=tk.BOTH)

        self.modstr = tk.StringVar()
        self.button_area()

    def button_area(self):
        ht_path = Path(__file__).parents[0] / "icon\\game_modifier\\HT.png"
        dt_path = Path(__file__).parents[0] / "icon\\game_modifier\\DT.png"

        self.ht_image = ImageTk.PhotoImage(file=ht_path)
        self.dt_image = ImageTk.PhotoImage(file=dt_path)
        self.halftime = tk.Radiobutton(self.frame,
                                  width=32,
                                  pady=10,
                                  image=self.ht_image,
                                  value="HT",
                                  variable=self.modstr
                                  )
        self.doubletime = tk.Radiobutton(self.frame,
                                  width=32,
                                  pady=10,
                                  image=self.dt_image,
                                  value="DT",
                                  variable=self.modstr
                                  )
        self.normalmod = tk.Radiobutton(self.frame,
                                   width=65,
                                   height=1,
                                   pady=10,
                                   text="±0",
                                   font=("Arial", 22),
                                   value="NM",
                                   variable=self.modstr
                                   )
        self.normalmod.pack(side=tk.TOP, fill="none", pady=5)
        self.normalmod.select()
        self.halftime.pack(side=tk.TOP, fill=tk.X, pady=5)
        self.halftime.deselect()
        self.doubletime.pack(side=tk.TOP, fill=tk.X, pady=5)
        self.doubletime.deselect()

    def get_mod(self):
        return self.modstr.get()