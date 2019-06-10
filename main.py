import matplotlib.pyplot as plt
import numpy as np
import cv2
import sys
import pyexcel

from math import sqrt

from libs.get_cropped_picture import get_cropped_picture
from libs.get_lines import *
from libs.get_cells import *
from libs.tesseract import *
from libs.show_image import *
from libs.get_optimal_rotation import *
from libs.global_variables import *

ASSUME_PERFECT_GRID = True


np.set_printoptions(threshold=sys.maxsize)
pic_directory = "/home/alexander/Desktop/Projects/Ericsson/ExcelReader/pictures/"
pic_name = "qa_test1.png"

imgc, automatic = get_cropped_picture(pic_directory + pic_name)
#imgc = rotateImage(imgc, -1.5)
img = cv2.cvtColor(imgc, cv2.COLOR_BGR2GRAY)
#show_image(imgc, "rotated image")
if automatic:
    img, imgc = find_optimal_rotation(img, imgc, 0.001)
else:
    img, imgc = let_user_rotate(img, imgc)


if ASSUME_PERFECT_GRID:
    linesv, linesh = get_lines(img, MODE_PERFECT_SPREADSHEET)
else:
    linesv, linesh = get_lines(img, MODE_IRREGULAR_SPREADSHEET)

imgc = draw_lines(imgc, linesv, linesh)


HEIGHT, WIDTH = img.shape[:2]


show_image(imgc, "Actual lines")
print("Entering get cells")
if ASSUME_PERFECT_GRID:
    cells = get_cells(img, linesv, linesh)
else:
    cells = get_cells_irreg(img, linesv, linesh)
print("Entering get string rep")
spreadsheet = get_string_rep(cells)
print(spreadsheet)
pyexcel.save_as(array=spreadsheet, dest_file_name="result.xls")
