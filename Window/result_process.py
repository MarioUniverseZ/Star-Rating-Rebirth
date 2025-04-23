import os
import sys
sys.path.append("..")
from osu_file_parser import parser, InvalidModeError
from algorithm import calculate

#credit: https://stackoverflow.com/a/42221437
class ResultProcess:
    def __init__(self):
        self.__init__(self)

    def _resultprocess(self, item, file, mod, result: list):
        w_0, w_1, p_1, w_2, p_0 = 0.4, 2.7, 1.5, 0.27, 1.0

        parent_path = item
        for content_index in range(len(file)):
            file_path = os.path.join(parent_path, file[content_index])
            sr = calculate(file_path, mod, 6, 0.8, w_0, w_1, p_1, w_2, p_0)
            result[content_index]['SR'] = sr

        return result