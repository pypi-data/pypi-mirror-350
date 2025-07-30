import sys
import sqlite3
import os
from os.path import isfile, join

def control_args():
    if (len(sys.argv) < 2):
        print("Error : need arguments")
    if (len(sys.argv) > 2):
        print("Error : too much arguments")
    if (len(sys.argv) < 2 or len(sys.argv) > 2):
        print("extract.py Directory_name")

def get_last_pos(str, source):
    str_find = bytearray(str,'ascii')
    last_pos = 0
    pos = 0
    while True:
        pos = source.find(str_find, last_pos)
        if pos == -1:
            break
        last_pos = pos + 1
    return (last_pos -1)

from array import array

def readimage(path):
    with open(path, "rb") as f:
        return bytearray(f.read())

def extract_png_from_layer(working_file):
    import PIL.Image as Image
    import sys
    from PIL import Image
    from io import BytesIO
    import io
    s = 'PNG'
    with open(working_file, "rb") as inputFile:
        content = inputFile.read()
        begin_pos = get_last_pos(s, content)
        begin_pos -= 1

        s = 'IEND'
        end_pos = get_last_pos(s, content)
        end_pos += 4

        bytes = content[begin_pos:end_pos]
        image = Image.open(io.BytesIO(bytes))
        image.save(working_file + ".png")

def extract_sqlite_layers(working_file):
    file_name = working_file+".layer"

    extract_png_from_layer(working_file)


def main():
    # Control args
    #control_args()

    _dir = "D:\\download\\FA_CSP_Brushes\\test"
    if isfile(_dir):
        print("A file provided as an argument, extracting textures from the file...")
        filedir=''
        files = [_dir]
    else:
        filedir = _dir
        files = [join(filedir,x) for x in os.listdir(filedir)]
        files = [x for x in files if isfile(x)]

    for m_file in files:
        print(m_file)
        extract_sqlite_layers(m_file)

if __name__ == "__main__":
   main()