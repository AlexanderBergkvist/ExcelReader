import numpy as np
import cv2
from .show_image import show_image
from .global_variables import *


def get_cells(img, linesv, linesh):
    pointsv = []
    for line in linesv:
        [x1, y1, x2, y2] = line[0]
        pointsv.append(x1)
    pointsv.sort()

    pointsh = []
    for line in linesh:
        [x1, y1, x2, y2] = line[0]
        pointsh.append(y1)
    pointsh.sort()

    cells = []
    for i in range(len(pointsh)):
        row = []
        if i == len(pointsh) - 1:
            continue
        for x in range(len(pointsv)):
            if x == len(pointsv) - 1:
                continue
            cell = img[pointsh[i] + FROM_LINE_OFFSET:pointsh[i + 1] +
                       FROM_LINE_OFFSET, pointsv[x]:pointsv[x + 1]].copy()
            # show_image(cell,"Particular cell")
            cell = cv2.GaussianBlur(cell, (7, 7), 0)
            cell = cv2.addWeighted(cell, 2.4, np.zeros(
                cell.shape, cell.dtype), 0, -180)
            kernel = np.array([[-1, -1, -1],
                               [-1, 9, -1],
                               [-1, -1, -1]])
            cell = cv2.filter2D(cell, -1, kernel)
            row.append(cell)
        cells.append(row)
    return cells


def find_correct_line(p1, p2, lines):
    if p2 < p1:
        self.assertTrue(False, 'WeirdFormating')

    allowed_offset = abs(p1 - p2) / 3 #If the line goes less than a third into cell it cannot be considered a valid line.
    for line in lines:
        [x1, y1, x2, y2] = line
        if (y1 < (p1 + allowed_offset) and y2 < (p1 + allowed_offset)) or (y1 > (p2 - allowed_offset) and y2 > (p2 - allowed_offset)):
            continue
        else:
            return line
    print("Found no correct lines!")
    print(p1, p2)
    print(y1, y2, lines)


def get_cells_irreg(img, linesv, linesh):
    linesv = sorted(linesv, key=lambda x: x[0][0])
    linesh = sorted(linesh, key=lambda x: x[0][1])

    cells = []
    for i in range(len(linesh)):
        row = []
        if i == len(linesh) - 1:
            continue
        [_, iy1, _, _] = linesh[i][0]
        [_, iyy1, _, _] = linesh[i + 1][0]
        for z in range(len(linesv)):
            if z == len(linesv) - 1:
                continue
            # First line
            line = find_correct_line(iy1, iyy1, linesv[z])
            if line == None:
                continue
            else:
                [zx1, _, _, _] = line
            # Second line
            for iteration in range(len(linesv)): #If the first line isn't valid keep looking
                line = find_correct_line(iy1, iyy1, linesv[z + iteration + 1])
                if line == None:
                    continue
                else:
                    [zxx1, _, _, _] = line
                    break

            cell = img[iy1 + FROM_LINE_OFFSET:iyy1 + FROM_LINE_OFFSET, zx1:zxx1].copy()
            # show_image(cell,"Particular cell")
            cell = cv2.GaussianBlur(cell, (7, 7), 0)
            cell = cv2.addWeighted(cell, 2.4, np.zeros(
                cell.shape, cell.dtype), 0, -180)
            kernel = np.array([[-1, -1, -1],
                               [-1, 9, -1],
                               [-1, -1, -1]])
            cell = cv2.filter2D(cell, -1, kernel)
            row.append(cell)
        cells.append(row)
    return cells
