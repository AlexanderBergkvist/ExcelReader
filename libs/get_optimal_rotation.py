import matplotlib.pyplot as plt
import numpy as np
import cv2
from math import sqrt,ceil
from .get_lines import *
from .global_variables import *
import random

INFO_STRING = "Q = Counter-ClockWise, W = When done, E = ClockWise, R = Redo, D = Decrease StepSize"

def draw_lines(img, linesv, linesh):
    if linesv is None:
        print("Couldn't find vertical lines")
    else:
        for line in linesv:
            if len(line) > 1:
                for i in line:
                    [x1,y1,x2,y2] = i
                    cv2.line(img,(x1,y1),(x2,y2),LINE_COLOR,3)
            else:
                [x1,y1,x2,y2] = line[0]
                cv2.line(img,(x1,y1),(x2,y2),LINE_COLOR,3)
    if linesh is None:
        print("Couldn't find horizontal lines")
    else:
        for line in linesh:
            [x1,y1,x2,y2] = line[0]
            cv2.line(img,(x1,y1),(x2,y2),LINE_COLOR,3)
    return img


def rotateImage(image, angle, fill_color):
    image_center = tuple(np.array(image.shape[1::-1]) / 2)
    rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
    result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR, borderValue=(int(fill_color[0]),
                                                                                                     int(fill_color[1]),
                                                                                                     int(fill_color[2])))
    return result


def refresh_img(img, imgc, increment_acc, fill_color):
    img = rotateImage(img, increment_acc, fill_color)
    imgc = rotateImage(imgc, increment_acc, fill_color)
    return img, imgc

def find_fill_color(img): #Fix this later
    acc = [0,0,0]
    amount = 0
    for i in range(5):
        for pixel in img[-i - 1]:
            if pixel[0] >= 200 and pixel[1] >= 200 and pixel[2] >= 200:
                acc += pixel
                amount += 1
    for i in range(len(acc)):
        acc[i] = ceil(acc[i] / amount)
    if acc.all() == 0:
        return [220,220,200]
    return acc

def gather_score(linesh, linesv):
    rotate_score = 0
    for line in linesh:
        [x1, y1, x2, y2] = line[0]
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
    fill_color = find_fill_color(imgc)
    original_img = img
    original_imgc = imgc
    increment_acc = 0
    linesv, linesh = get_lines(img, MODE_GET_LINES_WITHOUT_AVERAGING)
    rotate_score = 1000
    increment = 0.08
    additional_increment = 0
    direction = 1
    picture_integrity = 0
    picture_integrity_max_value = 2
    done = False
    while not done:
        try:
            img = rotateImage(img, increment_acc, fill_color)
            imgc = rotateImage(imgc, increment_acc, fill_color)
            linesv, linesh = get_lines(img, MODE_GET_LINES_WITHOUT_AVERAGING)
            picture_integrity += 1
            rotate_score = gather_score(linesh, linesv)
            if abs(rotate_score) < goal:
                done = True
                print("\n\nRotate_score " + str(rotate_score))
                print("Done")
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
            print("\n\nRotate_score " + str(rotate_score))
            print(increment)

            if rotate_score < 0:
                img = rotateImage(img, -increment, fill_color)
                imgc = rotateImage(imgc, -increment, fill_color)
                increment_acc -= increment
            else:
                img = rotateImage(img, increment, fill_color)
                imgc = rotateImage(imgc, increment, fill_color)
                increment_acc += increment
        except:
            show_image(img, "Image when crashed")
    show_image(imgc, "Optimal rotation")
    return img, imgc


def let_user_rotate(img, imgc):
    fill_color = find_fill_color(imgc)
    original_img = img
    original_imgc = imgc
    increment_acc = 0
    increment = 0.1
    while True:
        img = original_img
        imgc = original_imgc
        img = rotateImage(img, increment_acc, fill_color)
        imgc = rotateImage(imgc, increment_acc, fill_color)

        linesv, linesh = get_lines(img, MODE_IRREGULAR_SPREADSHEET)
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
            cv2.destroyAllWindows()

    return img, imgc
