import colorsys
import os
import fnmatch

import cv2
import numpy as np
from PIL import Image
import colorsys


def change_hue(image_path, save_path, hue_shift):
    im = Image.open(image_path).convert('RGBA')
    im = im.convert("RGBA")
    datas = im.getdata()

    newData = []
    for item in datas:
        h, s, v = colorsys.rgb_to_hsv(item[0]/255., item[1]/255., item[2]/255.)
        h = (h + hue_shift/360.) % 1
        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        newData.append((int(r*255), int(g*255), int(b*255), item[3]))
    im.putdata(newData)
    im.save(save_path, "PNG")


def process_images(directory, hue_shift, exclude_patterns=None, include_patterns=None):
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if any(fnmatch.fnmatch(filename, pattern) for pattern in (exclude_patterns or [])):
                continue

            if any(fnmatch.fnmatch(filename, pattern) for pattern in (include_patterns or [])):
                filepath = os.path.join(root, filename)
                new_filename = filename.replace('enemy', 'target')
                new_filepath = os.path.join(root, new_filename)
                change_hue(filepath, new_filepath, hue_shift)


# Process hue from red to purple
process_images(
    directory='.',
    hue_shift=-60,
    include_patterns=['*_enemy.png', '*_enemy_outside.png']
)