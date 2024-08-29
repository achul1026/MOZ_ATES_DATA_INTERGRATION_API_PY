# 이미지 전처리
import cv2
import numpy as np
import calendar
import time

from scipy.ndimage import interpolation as inter

def get_best_image_for_text(image, extandsize = 8, isThreshold = True, debug = False) :
    # image = correct_skew(image)

    # print("morphd : ", extandsize)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray_image = correct_skew(gray_image)
    # gray_image = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]


    # blurImg = cv2.bilateralFilter(gray_image, 13, 15, 15)
    # kernel = np.ones((extandsize, extandsize), np.uint8)
    # result = cv2.morphologyEx(gray_image, cv2.MORPH_OPEN, kernel)
    # kernel = np.ones((4, 4), np.uint8)
    # result = cv2.morphologyEx(gray_image, cv2.MORPH_DILATE, kernel)

    if extandsize != 0 :
        print("do MORPH_OPEN")
        kernel = np.ones((extandsize-3, extandsize), np.uint8)
        gray_image = cv2.morphologyEx(gray_image, cv2.MORPH_OPEN, kernel)
    kernel = np.ones((3, 3), np.uint8)
    gray_image = cv2.morphologyEx(gray_image, cv2.MORPH_DILATE, kernel)
    if isThreshold :
        print("do Threshold")

        #First
        gray_image = cv2.GaussianBlur(gray_image, (7, 7), 7)
        gray_image = cv2.adaptiveThreshold(gray_image, 255.0, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 19, 9)
        # gray_image =  cv2.threshold(gray_image, 127, 255, cv2.THRESH_OTSU)[1]
    gmt = time.gmtime()
    ts = calendar.timegm(gmt)
    cv2.imwrite('/home/jboss/mozates_source/mozates/moz_ates_traffic/dataintegrationapi/learndata/'+str(ts)+'.png', gray_image)
    # if debug :
    # cv2.imshow("morph image", gray_image)
    # cv2.waitKey(0)
    return gray_image


def process(image, blockSize, boundRectArea = None, type = None, thresh = False, debug = False) :
    # print("blur type", type)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # gray_image = correct_skew(gray_image)
    if debug == True :
        cv2.imshow("greyed image", gray_image)
        cv2.waitKey(0)

    # 블러처리

    if type == 1 :
        blurImg = cv2.GaussianBlur(gray_image, (5, 5), 0)
    elif type == 3:
        blurImg = cv2.GaussianBlur(gray_image, (7, 7), 0)
    else :
        blurImg = cv2.bilateralFilter(gray_image, 13, 15, 15)
        # blurImg = cv2.bilateralFilter(gray_image, -1, 50, 10)
    if debug == True:
        cv2.imshow("blured image", blurImg)
        cv2.waitKey(0)
    if thresh == True :
        # kernel = np.ones((2, 2), np.uint8)
        # blurImg = cv2.morphologyEx(blurImg, cv2.MORPH_DILATE, kernel)
        # cv2.imshow("morph image 1", blurImg)
        # cv2.waitKey(0)
        # kernel = np.ones((5, 5), np.uint8)
        # blurImg = cv2.morphologyEx(blurImg, cv2.MORPH_OPEN, kernel)
        # cv2.imshow("morph image 2", blurImg)
        # cv2.waitKey(0)

        blurImg = cv2.adaptiveThreshold(blurImg, 255.0, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, blockSize, 9)
        # blurImg = cv2.adaptiveThreshold(blurImg, 255.0, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 467, 9)
        # blurImg = cv2.threshold(blurImg, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    if debug == True:
        cv2.imshow("thresh image", blurImg)
        cv2.waitKey(0)

    # edged = cv2.Canny(blurImg, 100, 300)
    edged = cv2.Canny(blurImg, 20, 150)
    if debug == True:
        cv2.imshow("edged image", edged)
        cv2.waitKey(0)

    contours, hierarchy = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    # image1 = image.copy()
    return contours


def image_resize(image, width = None, height = None, inter = cv2.INTER_AREA):
    dim = None
    (h, w) = image.shape[:2]

    if width is None and height is None:
        return image

    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)

    else:
        r = width / float(w)
        dim = (width, int(h * r))

    resized = cv2.resize(image, dim, interpolation = inter)
    return resized

def correct_skew(image, delta=2, limit=15):
    def determine_score(arr, angle):
        data = inter.rotate(arr, angle, reshape=False, order=0)
        histogram = np.sum(data, axis=1, dtype=float)
        score = np.sum((histogram[1:] - histogram[:-1]) ** 2, dtype=float)
        return histogram, score

    gray = image.copy()
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    scores = []
    angles = np.arange(-limit, limit + delta, delta)
    for angle in angles:
        histogram, score = determine_score(thresh, angle)
        scores.append(score)

    best_angle = angles[scores.index(max(scores))]

    (h, w) = gray.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, best_angle, 1.0)
    corrected = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, \
            borderMode=cv2.BORDER_REPLICATE)
    # cv2.imshow("correct", corrected)
    # cv2.waitKey(0)
    # print(best_angle)
    return corrected
