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


def rotateImage(image, angle):
    image_center = tuple(np.array(image.shape[1::-1]) / 2)
    rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
    result = cv2.warpAffine(
        image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR,borderValue=(255,255,255))
    return result

def find_optimal_rotation(img, imgc):
    old_rotate_score = 0
    increment = 0.5
    direction = -1
    for i in range(5):
        linesv,linesh = get_lines_wo(img, 100, 100, 15)
        rotate_score = 0
        for line in linesh:
            [x1,y1,x2,y2] = line[0]
            #print("y1: " + str(y1) + " y2: " + str(y2))
            rotate_score += abs(x1 - x2) #sqrt((y1 - y2)**2 + (x1 - x2)**2)
        rotate_score = rotate_score / len(linesh)

        print("\n\nrotate_score " + str(rotate_score))
        print("old rotate " + str(old_rotate_score))
        print(increment)
        if rotate_score < old_rotate_score:
            print("Switching direction!")
            direction = -direction
            if direction > 0:
                img = rotateImage(img, -increment)
                imgc = rotateImage(imgc, -increment)
            else:
                img = rotateImage(img, increment)
                imgc = rotateImage(imgc, increment)
            increment = increment / 2
            continue

        else:
            print("keeping on going")

        old_rotate_score = rotate_score

        if direction > 0:
            img = rotateImage(img, -increment)
            imgc = rotateImage(imgc, -increment)
        else:
            img = rotateImage(img, increment)
            imgc = rotateImage(imgc, increment)
        imgq = cv2.cvtColor(imgc, cv2.COLOR_BGR2GRAY)

    linesv,linesh = get_lines_wo(imgc, 100, 100, 15)
    for line in linesh:
        [x1,y1,x2,y2] = line[0]
        cv2.line(imgc,(x1,y1),(x2,y2),(0,0,255),1)
    show_image(imgc)
    return linesv, linesh


np.set_printoptions(threshold=sys.maxsize)
pic_directory = "/home/alexander/Desktop/Projects/Ericsson/ExcelReader/pictures/"
pic_name = "gt3.jpg"

imgc = get_cropped_picture(pic_directory + pic_name)
imgc = rotateImage(imgc, -3)
img = cv2.cvtColor(imgc, cv2.COLOR_BGR2GRAY)

linesv,linesh = find_optimal_rotation(img,imgc)








HEIGHT,WIDTH = img.shape[:2]

for line in linesv:
    [x1,y1,x2,y2] = line[0]
    cv2.line(imgc,(x1,0),(x2,HEIGHT),(0,0,255),1)

for line in linesh:
    [x1,y1,x2,y2] = line[0]
    cv2.line(imgc,(0,y1),(WIDTH,y2),(0,0,255),1)

show_image(imgc)
print("entering get cells")
cells = get_cells(img,linesv, linesh)
print("entering get string rep")
spreadsheet = get_string_rep(cells)
print(spreadsheet)
pyexcel.save_as(array=spreadsheet, dest_file_name="result.xls")
