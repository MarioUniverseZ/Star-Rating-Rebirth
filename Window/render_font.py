# credit: https://stackoverflow.com/a/73428832
from PIL import Image, ImageDraw, ImageFont
from .colormap import ColorMap
import numpy as np
from pathlib import Path
from io import BytesIO
from math import floor

class RenderFont:
    def __init__(self, filename, fill=(0, 0, 0)):
        """
        constructor for RenderFont
        filename: the filename to the ttf font file
        fill: the color of the text
        """
        self._file = filename
        self._fill = fill
        self._image = None
        
    def get_render(self, font_size, txt, type_="normal"):
        """
        returns a transparent PIL image that contains the text
        font_size: the size of text
        txt: the actual text
        type_: the type of the text, "normal" or "bold"
        """

        if type(font_size) is not int:
            raise TypeError("font_size must be a int")
        
        if type(txt) is str:
            if len(txt) > 24:
                txt = txt[:23] + "..."
                font_size = 26
            width = len(txt)*font_size
        if type(txt) is np.float64:
            width = 200

        height = font_size+2

        font = ImageFont.truetype(font=self._file, size=font_size)
        if type(txt) is str:
            self._image = Image.new(mode='RGBA', size=(width, height+12), color=(255, 255, 255))
        if type(txt) is np.float64:
            colormap = ColorMap(txt)
            r,g,b = colormap.get_difficulty_color(txt)
            self._image = Image.new(mode='RGBA', size=(width, height), color=(r,g,b))

            # border-radius in self._image
            mask = Image.new('L', (width, height), 0)
            mask_draw = ImageDraw.Draw(mask)
            mask_draw.rounded_rectangle((0, 0, width, height), 60, fill=255)
            self._image.putalpha(mask)

        rgba_data = self._image.getdata()
        newdata = []

        for item in rgba_data:
            if item[0] == 255 and item[1] == 255 and item[2] == 255:
                newdata.append((255, 255, 255, 0))

            else:
                newdata.append(item)

        self._image.putdata(newdata)

        draw = ImageDraw.Draw(im=self._image)

        if type_ == "normal":
            if type(txt) is np.float64:
                star_path = Path(__file__).parents[0] / "icon\\sr\\star.png"
                if txt.item() > 6.5:
                    star_path = Path(__file__).parents[0] / "icon\\sr\\star_gold.png"
                    self._fill = (255, 217, 102)
                star_icon = Image.open(star_path)
                star_icon = star_icon.resize((28, 28))
                self._image.paste(star_icon, (12, 10), star_icon)
                draw.text(xy=(50, height/2), text=f'{txt:.3f}', font=font, fill=self._fill, anchor='lm',
                stroke_width=1, stroke_fill=self._fill)
            else:
                self._fill = (0, 0, 0)
                draw.text(xy=(5,2), text=txt, font=font, fill='white', anchor='la',
                stroke_width=4.5, stroke_fill=self._fill)
        return self._image