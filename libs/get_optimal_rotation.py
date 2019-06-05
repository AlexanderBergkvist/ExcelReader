import matplotlib.pyplot as plt
import numpy as np
import cv2
from math import sqrt
from .get_lines import *
import random

INFO_STRING = "Q = Counter-ClockWise, W = When done, E = ClockWise, D = Decrease StepSize"

def draw_lines(img, linesv, linesh):
    for line in linesv:
        if len(line) > 1:
            for i in line:
                [x1,y1,x2,y2] = i
                cv2.line(img,(x1,y1),(x2,y2),(0,0,255),3)
        else:
            [x1,y1,x2,y2] = line[0]
            cv2.line(img,(x1,y1),(x2,y2),(0,0,255),3)

    for line in linesh:
        [x1,y1,x2,y2] = line[0]
        cv2.line(img,(x1,y1),(x2,y2),(0,0,255),3)
    return img



def rotateImage(image, angle):
    image_center = tuple(np.array(image.shape[1::-1]) / 2)
    rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
    result = cv2.warpAffine(
        image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR, borderValue=(200, 200, 200))
    return result


def refresh_img(img, imgc, increment_acc):
    img = rotateImage(img, increment_acc)
    imgc = rotateImage(imgc, increment_acc)
    return img, imgc


def gather_score(linesh, linesv):
    rotate_score = 0
    for line in linesh:
        [x1, y1, x2, y2] = line[0]
        #print("y1: " + str(y1) + " y2: " + str(y2))
        if x2 < x1:
            print("hori weird format")
            continue
        rotate_score -= ((y1 - y2) / 2)  # / 2 to make horizontall score less impactfull
    for line in linesv:
        [x1, y1, x2, y2] = line[0]
        if y2 > y1:
            rotate_score += ((x1 - x2) * 2)
        else:
            rotate_score += ((x1 - x2) * 2)

    return rotate_score / (len(linesh) + len(linesv))


def find_optimal_rotation(img, imgc, goal):

    original_img = img
    original_imgc = imgc
    increment_acc = 0
    linesv, linesh = get_lines_without_averaging(img, 100, 100, 15)
    rotate_score = 1000
    increment = 0.08
    additional_increment = 0
    direction = 1
    picture_integrity = 0
    picture_integrity_max_value = 2
    done = False
    while not done:
        try:
            #if picture_integrity >= picture_integrity_max_value:
            img, imgc = refresh_img(original_img, original_imgc, increment_acc)
            #    picture_integrity = 0
            linesv, linesh = get_lines_without_averaging(img, 100, 100, 15)
            picture_integrity += 1
            # show_image(imgc)
            # show_image(img)
            rotate_score = gather_score(linesh, linesv)
            if abs(rotate_score) < goal:#0 <= rotate_score and rotate_score < goal:
                done = True
                print("\n\nrotate_score " + str(rotate_score))
                print("done mofo!")
                break

            elif abs(rotate_score) < 0.15:
                increment = 0.01 - additional_increment
            elif abs(rotate_score) < 0.2:
                increment = 0.05 - additional_increment
            elif abs(rotate_score) < 0.5:
                increment = 0.08 - additional_increment
            elif abs(rotate_score) < 1:
                increment = 0.1 - additional_increment
            additional_increment +=0.0001
            if increment < 0.0001:
                increment = 0.0001 * random.randrange(1,4)
            print("\n\nrotate_score " + str(rotate_score))
            print(increment)

            if rotate_score < 0:
                img = rotateImage(img, -increment)
                imgc = rotateImage(imgc, -increment)
                increment_acc -= increment
            else:
                img = rotateImage(img, increment)
                imgc = rotateImage(imgc, increment)
                increment_acc += increment
        except:
            show_image(img, "Image when crashed")
    show_image(imgc, "Optimal rotation")
    return img, imgc


def let_user_rotate(img, imgc):

    original_img = img
    original_imgc = imgc
    increment_acc = 0
    increment = 0.1
    while True:
        img = original_img
        imgc = original_imgc
        img = rotateImage(img, increment_acc)
        imgc = rotateImage(imgc, increment_acc)

        linesv, linesh = get_lines_irreg(img, 200, 200, 15)
        draw_lines(imgc, linesv, linesh)
        cv2.namedWindow(INFO_STRING + " CurrentStep: " + str(increment), cv2.WINDOW_NORMAL)
        cv2.imshow(INFO_STRING + " CurrentStep: " + str(increment), imgc)
        key = cv2.waitKey(0) & 0xFF

        if key == ord("q"):
            increment_acc += increment
        elif key == ord("w"):
            break
        elif key == ord("e"):
            increment_acc -= increment
        elif key == ord("d"):
            increment = increment / 2

    return img, imgc
