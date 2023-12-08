import pytesseract
import utils.image_process as ip
from utils.remove_shadow import process_image_file

pytesseract.pytesseract.tesseract_cmd = '/home/jboss/tesseract_install/tesseract/tesseract'

def get_plage_number_from_image(image, boundRectArea, doMorph=True, debug = False):
    # image = process_image_file(image.copy())[2]
    morphimg = image.copy()
    morphd = 8
    if boundRectArea < 12000 :
        morphd = 0
    if doMorph == True:
        morphimg = ip.get_best_image_for_text(image.copy(), morphd, debug)
    plate = pytesseract.image_to_string(morphimg, lang='eng',
                                        config='--oem 3 --psm 11 -c tessedit_char_whitelist="ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789- "')

    result = clean_plate_number(plate)
    result = check_number_and_change_g_to_zero(result)
    if validaton(result):
        return result
    else:
        if doMorph == True:
            return get_plage_number_from_image(image.copy(), boundRectArea, False, debug)
        else:
            return "Failed : " + result


def clean_plate_number(plate):
    print("clean_plate_number")
    print(plate.splitlines())
    plate_number = "";
    isCompletionIndex = -1;
    for index, v in enumerate(plate.splitlines()):
        if (v.find("-") == -1 and 8 == len(v.replace(" ", ""))) \
                or (v.find("-") != -1 and len(v.replace(" ", "")) == 9):
            isCompletionIndex = index
            break
    if (isCompletionIndex != -1):
        # print("isCompletionIndex :", isCompletionIndex)
        return plate.splitlines()[isCompletionIndex].replace(" ", "")

    if plate.find("-") != -1:
        # old plate
        for v in plate.splitlines():
            if v.strip() != "":
                plate_number += v.replace(" ", "").strip()
    else:
        # new plate
        lines = plate.splitlines()
        # if len(lines) == 1 :
        #     i = 0
        #     for v in lines[0].split(" ") :
        #         if i == 1 and len(v) > 3:
        #             v = v[0:3]
        #         if v.strip() != "":
        #             plate_number += v.replace(" ", "").strip()
        #         i += 1
        # else :
        for v in lines:
            if v.strip() != "":
                plate_number += v.replace(" ", "").strip()

    return plate_number


def validaton(plate):
    # 글자수 확인
    if plate.find("-") == -1:
        if len(plate) == 8:
            return True
        else:
            return False
    else:
        if len(plate) == 8 or len(plate) == 9:
            return True
        else:
            return False


def check_number_and_change_g_to_zero(value):
    change_number = "";
    if value.find("-") == -1 :
        value[3:6].replace("G","0") #모잠비크 폰트 교정

    return value


    # if index == 0:
    #     # 영문 3글자
    #     print()
    # elif index == 1:
    #     # 숫자 3자
    #     print()
    # elif index == 2:
    #     # 영문 2자
    #     print()
