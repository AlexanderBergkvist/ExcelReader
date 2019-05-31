import cv2

def show_image(img, label):
    cv2.namedWindow(label, cv2.WINDOW_NORMAL)
    cv2.imshow(label,img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
