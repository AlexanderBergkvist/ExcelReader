import cv2
import numpy as np

def extract_vertical(edges, erode):
    if erode != []:
        kernel = np.ones((6,1),np.uint8)
        dil = cv2.dilate(erode,kernel,iterations = 1)
        kernel = np.ones((14,1),np.uint8)
        erode = cv2.erode(dil,kernel,iterations = 1)
    else:
        kernel = np.ones((6,2),np.uint8)
        dil = cv2.dilate(edges,kernel,iterations = 1)
        kernel = np.ones((8,1),np.uint8)
        erode = cv2.erode(dil,kernel,iterations = 1)
    return (dil,erode)


img = cv2.imread("/home/alexander/Desktop/Projects/Ericsson/edgedetection/pictures/t.png")

edges = cv2.Canny(img,80,170,apertureSize = 3)

#Vertical
(dilv,erodev) = extract_vertical(edges, [])
for i in range(15):
    (dilv,erodev) = extract_vertical([], erodev)
cv2.namedWindow('edges', cv2.WINDOW_NORMAL)
cv2.imshow('edges',edges)
cv2.namedWindow('img', cv2.WINDOW_NORMAL)
cv2.imshow('img',erodev)
cv2.waitKey(0)
cv2.destroyAllWindows()
