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

ASSUME_PERFECT_GRID = False



np.set_printoptions(threshold=sys.maxsize)
pic_directory = "/home/alexander/Desktop/Projects/Ericsson/ExcelReader/pictures/"
pic_name = "gt3.jpg"

imgc, automatic = get_cropped_picture(pic_directory + pic_name)
#imgc = rotateImage(imgc, -1.5)
img = cv2.cvtColor(imgc, cv2.COLOR_BGR2GRAY)
#show_image(imgc, "rotated image")
print(img)
