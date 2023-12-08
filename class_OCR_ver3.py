import cv2
import utils.image_process as ip
import utils.plate_number as pn


class OCRVer3:
    addSize = -4
    i = 7
    cropped_img = None
    cx = 0
    cy = 0
    cw = 0
    ch = 0
    cratio = 0
    boundRectArea = 0
    image = None
    ocrtype = 1

    def __init__(self, image, ocrtype = 1):
        # 이미지 로드
        self.image = image
        self.ocrtype = ocrtype

    def getScreenCnt(self, cnts):
        screenCnt = None
        new_img = None
        for c in cnts:
            perimeter = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.022 * perimeter, True)
            self.cx, self.cy, self.cw, self.ch = cv2.boundingRect(c)
            nratio = self.cw / self.ch
            cArea = cv2.contourArea(c)

            boundingRect = cv2.boundingRect(c)

            [intX, intY, intWidth, intHeight] = boundingRect

            intBoundingRectX = intX
            intBoundingRectY = intY
            intBoundingRectWidth = intWidth
            intBoundingRectHeight = intHeight

            intBoundingRectArea = intBoundingRectWidth * intBoundingRectHeight
            intBoundingRectRatio = intBoundingRectWidth / intBoundingRectHeight

            print("intBoundingRectArea : ", intBoundingRectArea)
            print("intBoundingRectRatio : ", intBoundingRectRatio)
            print("all contourArea : ", cArea)
            print("꼭지점 : ", len(approx))
            self.boundRectArea = intBoundingRectArea
            # if len(approx) == 4 and 1.7 < nratio < 3.83 :
            # if len(approx) == 4 and 1.7 < nratio < 3.83 and 11300.0 < cArea < 21000.0:
            ocrtypeTest = (len(approx) == 4)
            if self.ocrtype == 1 :
                ocrtypeTest = len(approx) == 4 and ((1.7 < intBoundingRectRatio < 2.5 and 8000 < intBoundingRectArea < 21000) or (2.8 < intBoundingRectRatio < 3.9 and 3800 < intBoundingRectArea < 13000))

            if ocrtypeTest :
                screenCnt = approx
                self.cratio = self.cw / self.ch
                # new_img = image[y:y + h, x:x + w]
                new_img = self.image[self.cy - self.addSize:self.cy + self.ch + self.addSize,
                          self.cx - self.addSize:self.cx + self.cw + self.addSize]
                # cv2.imwrite('./' + str(i) + '.png', new_img)
                break
        return screenCnt, new_img

    def do(self, process_type = 1):
        # print("process_type : ", process_type)
        # if w > 2000 :
        self.image = ip.image_resize(self.image, width=900)

        type = [
            {
                "blockSize": 19,
                "thresh": False,
            },
            {
                "blockSize": 19,
                "thresh": True
            },
            {
                "blockSize": 467,
                "thresh": True
            },
            {
                "blockSize": 467,
                "thresh": False
            },
        ]
        for value in type :
            contours = ip.process(self.image, blockSize=value['blockSize'], boundRectArea=self.boundRectArea, type=process_type, thresh=value['thresh'] ,debug=False)
            cnts = sorted(contours, key=cv2.contourArea, reverse=True)[:30]
            screenCnt, new_img = self.getScreenCnt(cnts)
            if screenCnt is not None :
                break

        if screenCnt is None :
            print("screenCnt is None return")
            return "Failed"

        print("ratio : ", self.cratio)
        if self.cratio < 2:
            cropped_img = ip.image_resize(new_img, width=300)
        else:
            cropped_img = ip.image_resize(new_img, width=500)

        plate = pn.get_plage_number_from_image(cropped_img.copy(), boundRectArea = self.boundRectArea)

        # cv2.imshow("image with detected license plate", self.image)
        # print("blurtype", process_type)
        return plate