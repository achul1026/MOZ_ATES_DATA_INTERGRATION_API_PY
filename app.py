import cv2
import numpy as np
import werkzeug.datastructures
from flask import Flask, jsonify, request
from flask_restx import Resource, Api, reqparse
from class_OCR_ver3 import OCRVer3

app = Flask(__name__)
api = Api(app)

app.config["CACHE_TYPE"] = "null"

@api.route('/plate_number')
class App(Resource):

    def get(self):
        return "init"

    def post(self):
        parser = reqparse.RequestParser()
        parser.remove_argument('file')
        parser.add_argument('file', type=werkzeug.datastructures.FileStorage, location="files")

        # parser.add_argument('name', type=)
        args = parser.parse_args()
        # print(args['name'])
        file_obj = args['file']
        print(file_obj)
        if file_obj is None:
            return "Image file required."
        image = np.asarray(bytearray(file_obj.read()), dtype="uint8")
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)
        # ocrv3 = OCRVer3(image=image)
        # process_type = 1
        plate = "Failed"
        lastocrtype = None
        for ocrtype in range(1, 3) :
            ocrv3 = OCRVer3(image=image, ocrtype=ocrtype)
            lastocrtype = ocrtype;
            for process_type in range(1,4) :
                plate = ocrv3.do(process_type)
                if plate.find("Failed") == -1 :
                    break
            if plate.find("Failed") == -1:
                break

        print("ocrtype : ", ocrtype)
        success = True
        if plate.find("Failed") != -1 :
            success = False
        res = {
                "success" : success,
                "plate_number" : plate
               }
        if success :
            res.update({
                "vehicle_info": {
                    "vehicle_type": "1",
                    "vehicle_registration_number" : "12192192",
                    "manufacture": "Toyota"
                },
                "driver_info": {
                    "license_number": "123456789",
                    "license_expiry": "20221230",
                    "birth": "18031993",
                    "forename": "José",
                    "surname": "Cossa",
                    "address": "Mozambique Maputo City",
                    "phone" : "12301023",
                    "email" : "email@email.com",
                    "licence_type" : "2"
                }
            })
        return res

if __name__ == '__main__':
    app.run(debug=True, port=5001)
