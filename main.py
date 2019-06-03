import matplotlib.pyplot as plt
import numpy as np
import cv2
import sys
import pyexcel

from math import sqrt
from libs.get_cropped_picture import get_cropped_picture
from libs.get_lines import *
from libs.get_cells import get_cells
from libs.tesseract import *
from libs.show_image import show_image
from libs.get_optimal_rotation import *




np.set_printoptions(threshold=sys.maxsize)
pic_directory = "/home/alexander/Desktop/Projects/Ericsson/ExcelReader/pictures/"
pic_name = "gt3.jpg"

imgc, automatic = get_cropped_picture(pic_directory + pic_name)
#imgc = rotateImage(imgc, -1.5)
img = cv2.cvtColor(imgc, cv2.COLOR_BGR2GRAY)
#show_image(imgc, "rotated image")
if automatic:
    img, imgc = find_optimal_rotation(img, imgc, 0.001)
else:
    img, imgc = let_user_rotate(img, imgc)

linesv, linesh = get_lines_irreg(img, 100, 200, 15)



imgc = draw_lines(imgc,linesv,linesh)


HEIGHT,WIDTH = img.shape[:2]


show_image(imgc, "actual lines")
print("entering get cells")
cells = get_cells(img,linesv, linesh)
print("entering get string rep")
spreadsheet = get_string_rep(cells)
print(spreadsheet)
pyexcel.save_as(array=spreadsheet, dest_file_name="result.xls")
