import numpy as np
import sys

# ...Why does python 3.x change next to __next__......


def string_to_int(str):
    return int(float(str))


def collect_data(data, new_datum):
    data = data.append(new_datum)

# Parser Class that can be used on other class.

class InvalidModeError(Exception):
    pass

class parser:
    def __init__(self, file_path):
        # Need to find some way to escape \.
        # self.file_path = file_path.replace("\\", "\\\\")
        self.file_path = file_path
        self.od = -1
        self.column_count = -1
        self.columns = []
        self.note_starts = []
        self.note_ends = []
        self.note_types = []
        self.title = ""
        self.artist = ""

    def get_title_artist(self):
        with open(self.file_path, 'r', encoding='utf-8') as f:
            self.title, self.artist = self.read_metadata(f)

    def process(self):
        with open(self.file_path, "r+", encoding='utf-8') as f:

            try:
                self.read_mode(f)
                for line in f:

                    temp_cc = self.read_column_count(f, line)
                    if temp_cc != -1:
                       self.column_count = temp_cc

                    temp_od = self.read_overall_difficulty(f, line)
                    if temp_od != -1:
                       self.od = temp_od

                    if self.column_count != -1:
                       self.read_note(f, line, self.column_count)

            except StopIteration:
                pass
            except InvalidModeError:
                sys.exit()

    def read_mode(self, f):
        for line in f:
            if line.startswith("osu file format"):
                version_str = line.rstrip('\n')
                version = int(version_str.split("v")[-1])
                if version < 5:
                    raise InvalidModeError("Version too old")
            while "Mode:" not in line:
                line = f.__next__()
            mode_str = line.rstrip('\n')
            if mode_str.split(": ")[-1] != '3':
                raise InvalidModeError("Not mania mode")
            else:
                break

    # Read metadata from .osu file.
    def read_metadata(self, f):
        for line in f:
            if line.startswith("Title:"):
                title = line.split(":")[1]
            if line.startswith("Artist:"):
                artist = line.split(":")[1]
            line = f.__next__()
            if "Source:" in line:
                return title, artist

    def read_overall_difficulty(self, f, line):
        od = -1
        if "OverallDifficulty:" in line:
            temp = line.strip()
            pos_of_point = temp.index(':')
            if (pos_of_point == None):
                od = float(temp[-1])
            else:
                od = float(temp[pos_of_point+1:])
            # line = f.__next__()
        return float(od)

    # Read mode: key count.
    def read_column_count(self, f, line):
        column_count = -1
        if "CircleSize:" in line:
            temp = line.strip()
            column_count = temp[-1]
            if column_count=='0':
                column_count='10'
            # line = f.__next__()
            # print(line, end='')
        return string_to_int(column_count)

    def read_Timing_Points(self, f, object_line, line):
        if "[TimingPoints]" in line:
            line = f.__next__()
            params = object_line.split(",")
            offset = string_to_int(params[0])
            # mpb = 60000 / bpm...
            mpb = string_to_int(params[1])
            # meter: number of beats in a measure. .
            meter = string_to_int(params[2])
            # Other parameters are not important for measuring difficulty.

    # Main function for parsing note data.
    # https://osu.ppy.sh/help/wiki/osu!_File_Formats/Osu_(file_format)

    def read_note(self, f, line, column_count):
        if "[HitObjects]" in line:
            line = f.__next__()
            while line != None:
                self.parse_hit_object(f, line, column_count)
                line = f.__next__()

    # Helper function for read_note().
    # Store all note information in 4 arrays: column, type, start, end.
    # If note_end is 0, the note is a single note, otherwise a hold.
    def parse_hit_object(self, f, object_line, column_count):
        params = object_line.split(",")
        column = string_to_int((params[0]))
        column_width = int(512 / column_count)
        column = int(column / column_width)
        collect_data(self.columns, column)

        note_start = int(params[2])
        collect_data(self.note_starts, note_start)

        # 1: single note
        # 128: Hold(LN)
        note_type = int(params[3])
        collect_data(self.note_types, note_type)

        last_param_chunk = params[5].split(":")
        note_end = int(last_param_chunk[0])
        collect_data(self.note_ends, note_end)

    def get_parsed_data(self):
        return [self.column_count,
                self.columns,
                self.note_starts,
                self.note_ends,
                self.note_types,
                self.od]
