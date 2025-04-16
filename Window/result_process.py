import os
import sys
sys.path.append("..")
from osu_file_parser import parser, InvalidModeError
from algorithm import calculate

#credit: https://stackoverflow.com/a/42221437
class ResultProcess:
    def __init__(self):
        self.__init__(self)

    def _resultprocess(self, item, file, mod):
        w_0, w_1, p_1, w_2, p_0 = 0.4, 2.7, 1.5, 0.27, 1.0

        result = []
        background = []
        parent_path = item
        for content in file:
            if content.endswith('.osu'):
                try:
                    file_path = os.path.join(parent_path, content)
                    metadata = parser(file_path)
                    title, artist, diffname, bg = metadata.get_metadata()
                    sr = calculate(file_path, mod, 6, 0.8, w_0, w_1, p_1, w_2, p_0)
                    result.append({
                                "title": title,
                                "artist": artist,
                                "diffname": diffname,
                                "SR": sr
                    })
                    background.append(f'{parent_path}\\{bg}')
                except (InvalidModeError, SystemExit, ValueError) as e:
                    print(file_path.split("\\")[-1].rstrip(".osu"), e)

        return result, background