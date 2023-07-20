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

def process_images(directory, hue_level):
    for filename in os.listdir(directory):
        if fnmatch.fnmatch(filename, '*_enemy.png') or fnmatch.fnmatch(filename, '*_enemy_outside.png'):
            image_file = os.path.join(directory, filename)
            modified_filename = filename.replace('enemy', 'target')
            modified_file = os.path.join(directory, modified_filename)
            change_hue(image_file, modified_file, hue_level)

# Process hue from red to purple
process_images('.', hue_level=-60)