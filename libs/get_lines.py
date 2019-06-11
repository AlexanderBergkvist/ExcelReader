import cv2
import numpy as np
from .show_image import show_image
from .global_variables import *
from math import ceil


def connected(q1, q2, p1, p2):
    if q1 > p2:
        return False
    if p1 > q2:
        return False
    else:
        return True

def reformat_lines_vert(lines):
    if lines is None:
        print("No lines to reformat")
        return
    for line in lines:
        [x1, y1, x2, y2] = line[0]
        if y1 > y2:
            line[0] = [x2, y2, x1, y1]
    return lines

def reformat_lines_hor(lines):
    if lines is None:
        print("No lines to reformat")
        return
    for line in lines:
        [x1, y1, x2, y2] = line[0]
        if x1 > x2:
            line[0] = [x2, y2, x1, y1]
    return lines



def remove_duplicates(lines, direction):
    if lines is None:
        return
    length = len(lines)
    i = 0
    while i < length:
        z = i + 1
        while z < length:
            if z >= length:
                break
            ix1, iy1, ix2, iy2 = lines[i][0]
            zx1, zy1, zx2, zy2 = lines[z][0]
            if direction == 'vertical':
                if abs(ix1 - zx1) < LINE_SPACE_VERTICAL and abs(ix2 - zx2) < LINE_SPACE_VERTICAL:
                    # Remove one line and make the other one average of both
                    lines[i][0]=[ceil((ix1 + zx1) / 2), min(iy1, zy1), ceil((ix2 + zx2) / 2), max(iy2, zy2)]
                    lines=np.delete(lines, z, 0)
                    length -= 1
                    continue
            elif direction == 'horizontal':
                if abs(iy1 - zy1) < LINE_SPACE_HORIZONTAL and abs(iy2 - zy2) < LINE_SPACE_HORIZONTAL:
                    lines[i][0]=[min(ix1, zx1), ceil((iy1 + zy1) / 2), max(ix2, zx2), ceil((iy2 + zy2)) / 2]
                    lines=np.delete(lines, z, 0)
                    length -= 1
                    continue
            z += 1
        i += 1
    return lines


def remove_duplicates_irreg(lines, direction):
    if lines is None:
        return
    length = len(lines)
    i = 0
    while i < length:
        z = i + 1
        while z < length:
            if z >= length:
                break
            ix1, iy1, ix2, iy2 = lines[i][0]
            zx1, zy1, zx2, zy2 = lines[z][0]
            if direction == 'vertical':
                if abs(ix1 - zx1) < LINE_SPACE_VERTICAL and abs(ix2 - zx2) < LINE_SPACE_VERTICAL:
                    if connected(zy1, zy2, iy1, iy2):
                        # Remove one line and make the other one average of both
                        lines[i][0]=[ceil((ix1 + zx1) / 2), min(iy1, zy1), ceil((ix2 + zx2) / 2), max(iy2, zy2)]
                        lines=np.delete(lines, z, 0)
                        length -= 1
                        i -= 1
                        break
            elif direction == 'horizontal':
                if abs(iy1 - zy1) < LINE_SPACE_HORIZONTAL and abs(iy2 - zy2) < LINE_SPACE_HORIZONTAL:
                    if connected(zx1, zx2, ix1, ix2):
                        lines[i][0]=[min(ix1, zx1), ceil((iy1 + zy1) / 2), max(ix2, zx2), ceil((iy2 + zy2)) / 2]
                        lines=np.delete(lines, z, 0)
                        length -= 1
                        i -= 1
                        break
            z += 1
        i += 1
    return lines

def bunch_up_lines(lines, direction):
    if lines is None:
        return
    lines = lines.tolist()
    for line in lines:
        line = [line]


    length = len(lines)

    i = 0
    while i < length:
        z = i + 1
        while z < length:
            if z >= length:
                break
            ix1, iy1, ix2, iy2 = lines[i][0]
            zx1, zy1, zx2, zy2 = lines[z][0]
            if direction == 'vertical':
                if abs(ix1 - zx1) < LINE_SPACE_VERTICAL and abs(ix2 - zx2) < LINE_SPACE_VERTICAL:
                    lines[i].append(lines[z][0])
                    lines.pop(z)
                    length -= 1
                    continue
            elif direction == 'horizontal':
                if abs(iy1 - zy1) < LINE_SPACE_HORIZONTAL and abs(iy2 - zy2) < LINE_SPACE_HORIZONTAL:
                    lines[i].append(lines[z][0])
                    lines.pop(z)
                    length -= 1
                    continue
            z += 1
        i += 1
    return lines


# Vertical
def extract_vertical(edges, erode):
    if erode != []:
        kernel=np.ones(VERTICAL_INITIAL_DILATION, np.uint8)
        dil=cv2.dilate(erode, kernel, iterations=1)
        kernel=np.ones(VERTICAL_INITIAL_ERODE, np.uint8)
        erode=cv2.erode(dil, kernel, iterations=1)
    else:
        kernel=np.ones(VERTICAL_COMMON_DILATION, np.uint8)
        dil=cv2.dilate(edges, kernel, iterations=1)
        kernel=np.ones(VERTICAL_COMMON_ERODE, np.uint8)
        erode=cv2.erode(dil, kernel, iterations=1)
    return (dil, erode)


# horizontall
def extract_horizontall(edges, erode):
    if erode != []:
        kernel=np.ones(HORIZONTAL_INITIAL_DILATION, np.uint8)
        dil=cv2.dilate(erode, kernel, iterations=1)
        kernel=np.ones(HORIZONTAL_INITIAL_ERODE, np.uint8)
        erode=cv2.erode(dil, kernel, iterations=1)
    else:
        kernel=np.ones(HORIZONTAL_COMMON_DILATION, np.uint8)
        dil=cv2.dilate(edges, kernel, iterations=1)
        kernel=np.ones(HORIZONTAL_INITIAL_ERODE, np.uint8)
        erode=cv2.erode(dil, kernel, iterations=1)
    return (dil, erode)

def get_lines(img, mode):
    edges=cv2.Canny(img, 80, 170, apertureSize=3)
    # Vertical
    (dilv, erodev)=extract_vertical(edges, [])
    for i in range(PIC_ENHANCEMENT_ITERATION):
        (dilv, erodev)=extract_vertical([], erodev)
    # show_image(erodev, "Vertical erodes")
    linesv=cv2.HoughLinesP(erodev, 1, np.pi / 180, 100, VERTICAL_LINE_LENGTH, 10)
    linesv=reformat_lines_vert(linesv)


    if mode == "irregular":
        linesv = remove_duplicates_irreg(linesv, 'vertical')
        linesv = bunch_up_lines(linesv, 'vertical')
    elif mode =="perfect":
        linesv=remove_duplicates(linesv, 'vertical')

    # horizontall
    (dilh, erodeh)=extract_horizontall(edges, [])
    for i in range(PIC_ENHANCEMENT_ITERATION):
        (dilh, erodeh)=extract_horizontall([], erodeh)
    # show_image(erodeh, "Horizontall erodes")
    linesh=cv2.HoughLinesP(erodeh, 1, np.pi / 180, 70, HORIZONTAL_LINE_LENGTH, 10)
    linesh=reformat_lines_hor(linesh)
    if mode == "irregular":
        linesh=remove_duplicates_irreg(linesh, 'horizontal')
        linesh = bunch_up_lines(linesh, 'horizontal')
    elif mode == "perfect":
        linesh=remove_duplicates(linesh, 'horizontal')
    if not linesv is None:
        print(len(linesv))
    if not linesv is None:
        print(len(linesh))
    return linesv, linesh
