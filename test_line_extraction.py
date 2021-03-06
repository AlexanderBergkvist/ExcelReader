#https://docs.opencv.org/3.4/dd/dd7/tutorial_morph_lines_detection.html
import sys
#sys.path.append('/home/alexander/Desktop/Projects/Ericsson/ExcelReader/libs')
import cv2
import numpy as np
from libs.show_image import *
from libs.get_cropped_picture import *
from libs.global_variables import *
from math import ceil


def remove_duplicates(lines, direction):
    length = len(lines)
    if direction == 'vertical':
        i = 0
        while i < length:
            z = i + 1
            while z < length:
                if z >= length:
                    break
                ix1,y1,ix2,y2 = lines[i][0]
                zx1,_,zx2,_ = lines[z][0]

                if abs(ix1 - zx1) < 4 and abs(ix2 - zx2) < 4:
                    lines[i][0] = [ceil((ix1+zx1)/2), y1, ceil((ix2+zx2)/2), y2] #Remove one line and make the other one average of both
                    lines = np.delete(lines,z,0)
                    length -=1
                    continue
                else:
                    z +=1
            i +=1
    elif direction == 'horizontal':
        i = 0
        while i < length:
            z = i + 1
            while z < length:

                if z >= length:
                    break
                x1,iy1,x2,iy2 = lines[i][0]
                _,zy1,_,zy2 = lines[z][0]

                if abs(iy1 - zy1) < 4 and abs(iy2 - zy2) < 4:
                    lines[i][0] = [x1,ceil((iy1+zy1)/2), x2, ceil((iy2+zy2))/2]
                    lines = np.delete(lines,z,0)
                    length -=1
                    continue
                else:
                    z +=1
            i +=1
    return lines


#Vertical
def extract_vertical(edges, erode):
    if erode != []:
        kernel = np.ones(VERTICAL_INITIAL_DILATION,np.uint8)
        dil = cv2.dilate(erode,kernel,iterations = 1)
        kernel = np.ones(VERTICAL_INITIAL_ERODE,np.uint8)
        erode = cv2.erode(dil,kernel,iterations = 1)
    else:
        kernel = np.ones(VERTICAL_COMMON_DILATION,np.uint8)
        dil = cv2.dilate(edges,kernel,iterations = 1)
        kernel = np.ones(VERTICAL_COMMON_ERODE,np.uint8)
        erode = cv2.erode(dil,kernel,iterations = 1)
    return (dil,erode)


#horizontall
def extract_horizontall(edges, erode):
    if erode != []:
        kernel = np.ones(HORIZONTAL_INITIAL_DILATION,np.uint8)
        dil = cv2.dilate(erode,kernel,iterations = 1)
        kernel = np.ones(HORIZONTAL_INITIAL_ERODE,np.uint8)
        erode = cv2.erode(dil,kernel,iterations = 1)
    else:
        kernel = np.ones(HORIZONTAL_COMMON_DILATION,np.uint8)
        dil = cv2.dilate(edges,kernel,iterations = 1)
        kernel = np.ones(HORIZONTAL_COMMON_ERODE,np.uint8)
        erode = cv2.erode(dil,kernel,iterations = 1)
    return (dil,erode)

def get_lines():
    pic_directory = "/home/alexander/Desktop/Projects/Ericsson/ExcelReader/pictures/"
    pic_name = "qa_test1.png"

    imgc, _ = get_cropped_picture(pic_directory + pic_name)
    img = cv2.cvtColor(imgc, cv2.COLOR_BGR2GRAY)

    edges = cv2.Canny(img,80,170,apertureSize = 3)

    #Vertical
    (dilv,erodev) = extract_vertical(edges, [])
    for i in range(PIC_ENHANCEMENT_ITERATION):
        (dilv,erodev) = extract_vertical([], erodev)
    linesv = cv2.HoughLinesP(erodev,1,np.pi/180,100, VERTICAL_LINE_LENGTH,10)
    linesv = remove_duplicates(linesv, 'vertical')
    #horizontall
    (dilh,erodeh) = extract_horizontall(edges, [])
    for i in range(PIC_ENHANCEMENT_ITERATION):
        (dilh,erodeh) = extract_horizontall([], erodeh)

    cv2.namedWindow('e', cv2.WINDOW_NORMAL)
    cv2.imshow('e',erodeh)
    cv2.namedWindow('r', cv2.WINDOW_NORMAL)
    cv2.imshow('r',erodev)
    #cv2.namedWindow('img', cv2.WINDOW_NORMAL)
    #cv2.imshow('img',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    linesh = cv2.HoughLinesP(erodeh,1,np.pi/180,70, HORIZONTAL_LINE_LENGTH, 10)
    linesh = remove_duplicates(linesh, 'horizontal')

get_lines()
