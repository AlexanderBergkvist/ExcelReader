import cv2
import numpy as np
cordinate = []
image = []




def crop(event, x, y, flags, param):
    global cordinate, image

    if event == cv2.EVENT_LBUTTONDOWN:
        cordinate = [(x, y)]

    elif event == cv2.EVENT_LBUTTONUP:
        cordinate.append((x, y))

        cv2.rectangle(image, cordinate[0], cordinate[1], (0, 255, 0), 4)
        cv2.imshow("image", image)


def get_cropped_picture(path):
    global cordinate, image
    image = cv2.imread(path)
    clone = image.copy()

    #cv2.namedWindow('img', cv2.WINDOW_NORMAL)
    cv2.namedWindow("image", cv2.WINDOW_NORMAL)
    cv2.setMouseCallback("image", crop)

    while True:
        cv2.imshow("image", image)
        key = cv2.waitKey(1) & 0xFF

        if key == ord("r"):
            image = clone.copy()

        elif key == ord("c"):
            break

    cv2.destroyAllWindows()

    if len(cordinate) == 2:
        roi = clone[cordinate[0][1]:cordinate[1]
                    [1], cordinate[0][0]:cordinate[1][0]]
        return roi
