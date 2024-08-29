import datetime

import cv2
import utils.image_process as ip
import utils.plate_number as pn

# 이미지 로드
image = cv2.imread('TestData/IMG_0052.jpg')
image = ip.image_resize(image, 900)
contours = ip.process(image, 2,thresh=False, debug=True)
# cv2.drawContours(image1,contours,-1,(0,255,0),1)


cnts = sorted(contours, key = cv2.contourArea, reverse = True)[:30]
screenCnt = None
image2 = image.copy()
cv2.drawContours(image2,cnts,-1,(0,255,0),2)
cv2.imshow("Top 30 contours",image2)
cv2.waitKey(0)


addSize = -1
i=7
cropped_img = None
cx = 0
cy = 0
cw = 0
ch = 0
cratio = 0
for c in cnts:
        perimeter = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.018 * perimeter, True)
        # print(len(approx))
        cx, cy, cw, ch = cv2.boundingRect(c)
        nratio = cw/ch;
        if len(approx) == 4 and 1.7 < nratio < 3.83:
            print(len(approx))
            print(cv2.contourArea(c))
            screenCnt = approx
            # cx, cy, cw, ch = cv2.boundingRect(c)
            cratio = cw / ch
            print(cratio)
            cv2.drawContours(image, [screenCnt], -1, (0, 255, 0), 3)
            cv2.imshow("image with detected license plate", image)
            cv2.waitKey(0)
            # new_img = image[y:y + h, x:x + w]
            new_img = image[cy - addSize:cy + ch + addSize, cx - addSize:cx + cw + addSize]
            cv2.imwrite('./' + str(i) + '.png', new_img)
            i += 1
            break

cv2.drawContours(image, [screenCnt], -1, (0, 255, 0), 3)
cv2.imshow("image with detected license plate", image)
cv2.waitKey(0)
print(screenCnt)
print("ratio" , cratio)
Cropped_loc = './7.png'
cropped_img = cv2.imread(Cropped_loc)

# cropped_img = cv2.resize(cropped_img, (220, ch))
# cropped_img = imutils.resize(cropped_img, 400)
cv2.imshow("cropped", cropped_img)
cv2.waitKey(0)
plate = pn.get_plage_number_from_image(cropped_img)


cv2.imshow("image with detected license plate", image)
cv2.waitKey(0)
# pn.clean_plate_number(plate)
print("Normal Number plate is:", plate)
cv2.waitKey(0)


exit(0)
#2차 가공
MIN_WIDTH, MIN_HEIGHT = 2, 8         # 최소 너비 높이 범위 지정
MIN_RATIO, MAX_RATIO = 0.25, 1.0     # 최소 비율 범위 지정
h, w, c = cropped_img.shape
cropped_img = cv2.resize(cropped_img, (300, h))
second_contours = ip.process(cropped_img, 2, True)
cropped_img2 = cropped_img.copy()
contourlist=[]
index = 0;
for contour in second_contours :
    x, y, w, h = cv2.boundingRect(contour)
    area = w * h
    ratio = w / h

    if h > w :
        cv2.rectangle(cropped_img2, pt1=(x, y), pt2=(x + w, y + h), color=(0, 255, 0), thickness=1)
        contourlist.append({
            'contour': contour,
            'x': x,
            'y': y,
            'w': w,
            'h': h,
            'cx': x + (w / 2),
            'cy': y + (h / 2)
        })
        print(area, ratio)
        cv2.imshow("second", cropped_img2)
        cv2.waitKey(0)
    index += 1

# cv2.drawContours(cropped_img2,contourlist,-1,(0,255,0),1)
cv2.imshow("second", cropped_img2)
cv2.waitKey(0)
cv2.destroyAllWindows()
