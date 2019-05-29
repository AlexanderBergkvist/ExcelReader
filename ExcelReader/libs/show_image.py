import cv2

def show_image(img):
    cv2.namedWindow('img', cv2.WINDOW_NORMAL)
    cv2.imshow('img',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
