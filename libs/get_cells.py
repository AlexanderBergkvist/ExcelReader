import numpy as np
import cv2
from .show_image import show_image
OFFSET = 1


def get_cells(img,linesv, linesh):
    pointsv = []
    for line in linesv:
        [x1,y1,x2,y2] = line[0]
        pointsv.append(x1)
    pointsv.sort()

    pointsh = []
    for line in linesh:
        [x1,y1,x2,y2] = line[0]
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
            cell = img[pointsh[i]+OFFSET:pointsh[i+1]+OFFSET, pointsv[x]:pointsv[x+1]].copy()
            #cell = cv2.resize(cell, (0,0), fx=7, fy=7)
            show_image(cell)
            cell = cv2.GaussianBlur(cell,(7,7),0)
            cell = cv2.addWeighted(cell, 2.4, np.zeros(cell.shape, cell.dtype), 0, -180) #2,-120
            kernel = np.array([[-1,-1,-1],
                               [-1, 9,-1],
                               [-1,-1,-1]])
            cell = cv2.filter2D(cell, -1, kernel)
            row.append(cell)
        cells.append(row)
    return cells
