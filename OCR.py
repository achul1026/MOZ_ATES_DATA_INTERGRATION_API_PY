import cv2
import imutils
import numpy as np
import pytesseract
from PIL import Image
faceCascade = cv2.CascadeClassifier('haarcascade_russian_plate_number.xml')

path = "TestData/diff1.jpeg"
imgs = cv2.imread(path)
imgs = imutils.resize(imgs, width=1025)
gray2 = cv2.cvtColor(imgs, cv2.COLOR_BGR2GRAY)
gray2 = cv2.bilateralFilter(gray2, 13, 15, 15)
faces = faceCascade.detectMultiScale(gray2,scaleFactor=1.2,
    minNeighbors = 5, minSize=(25,25))
gray2 = imutils.resize(gray2, width=800)
cv2.imshow("resized", gray2)
cv2.waitKey(0)
for (x,y,w,h) in faces:
    # print(x)
    # print(y)
    # print(w)
    # print(h)
    cv2.rectangle(gray2,(x,y),(x+w,y+h),(255,255,255),4)
    new_img = gray2[y:y + h, x:x + w]
    ret, thresh = cv2.threshold(new_img, 120, 255, cv2.THRESH_BINARY)
    kernel = np.ones((3, 3), np.uint8)
    new_img = cv2.erode(thresh, kernel, iterations=1)
    # cv2.imshow("arg", new_img)
    # cv2.waitKey(0)
    data = pytesseract.image_to_data(new_img, lang='eng',
                                       config='--psm 11 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-')  # converts image characters to string
    print(data)
    text = pytesseract.image_to_string(new_img,lang='eng', config='-c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-') #converts image characters to string
    print(text)
    # plate = gray[y: y+h, x:x+w]
    # plate = cv2.blur(plate,ksize=(20,20))
    # put the blurred plate into the original image
    # gray[y: y+h, x:x+w] = plate

    cv2.imshow('plates',new_img)