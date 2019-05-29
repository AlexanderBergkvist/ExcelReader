from pytesseract import image_to_string
import cv2
import numpy as np

def get_string_rep(cells):
    array = []
    for cellrow in cells:
        row = []
        for cell in cellrow:
            row.append(image_to_string(cell,lang = "swe"))
            #show_image(cell)

        array.append(row)
    return array
