#https://docs.opencv.org/3.4/dd/dd7/tutorial_morph_lines_detection.html

import cv2
import numpy as np
from .show_image import show_image
from math import ceil
LINE_SPACE_VERTICAL = 70
LINE_SPACE_HORIZONTAL = 25

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

                if abs(ix1 - zx1) < LINE_SPACE_VERTICAL and abs(ix2 - zx2) < LINE_SPACE_VERTICAL:
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

                if abs(iy1 - zy1) < LINE_SPACE_HORIZONTAL and abs(iy2 - zy2) < LINE_SPACE_HORIZONTAL:
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
        kernel = np.ones((8,1),np.uint8)
        dil = cv2.dilate(erode,kernel,iterations = 1)
        kernel = np.ones((10,1),np.uint8)
        erode = cv2.erode(dil,kernel,iterations = 1)
    else:
        kernel = np.ones((8,3),np.uint8)
        dil = cv2.dilate(edges,kernel,iterations = 1)
        kernel = np.ones((10,1),np.uint8)
        erode = cv2.erode(dil,kernel,iterations = 1)
    return (dil,erode)


#horizontall
def extract_horizontall(edges, erode):
    if erode != []:
        kernel = np.ones((1,4),np.uint8)
        dil = cv2.dilate(erode,kernel,iterations = 1)
        kernel = np.ones((1,8),np.uint8)
        erode = cv2.erode(dil,kernel,iterations = 1)
    else:
        kernel = np.ones((3,4),np.uint8)
        dil = cv2.dilate(edges,kernel,iterations = 1)
        kernel = np.ones((1,8),np.uint8)
        erode = cv2.erode(dil,kernel,iterations = 1)
    return (dil,erode)

def get_lines(img, vert_line_size, hor_line_size,iter):
    edges = cv2.Canny(img,80,170,apertureSize = 3)

    #Vertical
    (dilv,erodev) = extract_vertical(edges, [])
    for i in range(iter):
        (dilv,erodev) = extract_vertical([], erodev)
    show_image(erodev)
    linesv = cv2.HoughLinesP(erodev,1,np.pi/180,100,vert_line_size,10)
    linesv = remove_duplicates(linesv, 'vertical')
    #horizontall
    (dilh,erodeh) = extract_horizontall(edges, [])
    for i in range(iter):
        (dilh,erodeh) = extract_horizontall([], erodeh)
    show_image(erodeh)
    linesh = cv2.HoughLinesP(erodeh,1,np.pi/180,70,hor_line_size,10)
    linesh = remove_duplicates(linesh, 'horizontal')

    return linesv,linesh


def get_lines_wo(img, vert_line_size, hor_line_size,iter):
    edges = cv2.Canny(img,80,170,apertureSize = 3)

    #Vertical
    (dilv,erodev) = extract_vertical(edges, [])
    for i in range(iter):
        (dilv,erodev) = extract_vertical([], erodev)
    #show_image(erodev)
    linesv = cv2.HoughLinesP(erodev,1,np.pi/180,100,vert_line_size,10)
    #linesv = remove_duplicates(linesv, 'vertical')
    #horizontall
    (dilh,erodeh) = extract_horizontall(edges, [])
    for i in range(iter):
        (dilh,erodeh) = extract_horizontall([], erodeh)
    #show_image(erodeh)
    linesh = cv2.HoughLinesP(erodeh,1,np.pi/180,70,hor_line_size,10)
    #linesh = remove_duplicates(linesh, 'horizontal')

    return linesv,linesh
