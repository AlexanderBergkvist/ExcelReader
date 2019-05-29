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

imgc = get_cropped_picture(pic_directory + pic_name)
imgc = rotateImage(imgc, -1.5)
img = cv2.cvtColor(imgc, cv2.COLOR_BGR2GRAY)
show_image(imgc)
img, imgc = find_optimal_rotation(img, imgc, 0.03)

linesv, linesh = get_lines(img, 100, 200, 15)






HEIGHT,WIDTH = img.shape[:2]

for line in linesv:
    [x1,y1,x2,y2] = line[0]
    cv2.line(imgc,(x1,0),(x2,HEIGHT),(0,0,255),3)

for line in linesh:
    [x1,y1,x2,y2] = line[0]
    cv2.line(imgc,(0,y1),(WIDTH,y2),(0,0,255),3)

show_image(imgc)
print("entering get cells")
cells = get_cells(img,linesv, linesh)
print("entering get string rep")
spreadsheet = get_string_rep(cells)
print(spreadsheet)
pyexcel.save_as(array=spreadsheet, dest_file_name="result.xls")
