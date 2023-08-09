import cv2
import numpy as np
import sqlite3
import os

from DataBase import Database
from Display import Display
from mailing import Mailing
from keypad import KeyPad


class FaceRecognitionClass:
    def recognize(self):
        return startRecognition()


def startRecognition():
    # Initialize 'currentname' to trigger only when a new person is identified.
    recognizedId = -1

    fname = "recognizer/trainingData.yml"
    if not os.path.isfile(fname):
        print("Please train the data first")
        exit(0)
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(0)
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read(fname)

    faceScanLimit = 30
    scanCount = 0
    detectionVote = []
    """
    for detection vote 
    id = -1 for  unknown face
    id = -2 for no face found
    id > 0  for normal registered id  
    """

    display = Display()
    while True:
        ret, img = cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        if faces == ():
            display.lcdPrint(' ---Scaning---', 1)
            display.lcdPrint("NO FACE FOUND", 2)
            detectionVote.append(-2)
        scanCount += 1

        # after sufficient scanning process ,vote for detection
        if scanCount >= faceScanLimit:

            # refine the vote dataset
            noFaceFrequency = 0
            for voted in detectionVote:
                if int(voted) == -2:
                    noFaceFrequency += 1
            # if noFaceFrequency is bellow 75%
            # remove noFaceVote from detectionVote
            if noFaceFrequency < (len(detectionVote) * 75) // 100:
                # compress the list by removing nofacefound candidate
                detectionVote = [candidate for candidate in detectionVote if candidate != -2]

            recognizedId = max(set(detectionVote), key=detectionVote.count)

            # to handle the case unable to detect face
            if recognizedId == -2:
                keypad = KeyPad()
                ch = keypad.getCharInput('Initiate 2FA ?', 'yes= # no= *')
                if ch == '#':
                    display.lcdPrint("Login Via 2FA.", 1)
                    cap.release()
                    cv2.destroyAllWindows()

                    authentication = Mailing()
                    recognizedId = authentication.TwofactorAuthontication()
                    break
                elif ch == '*':
                    scanCount = 0
                    detectionVote = []
                    display.lcdPrint('Face scaning...', 2)
            # person/employ is unknown / registered/known
            else:
                break

        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3)
            ids, conf = recognizer.predict(gray[y:y + h, x:x + w])
            db = Database()

            if conf <50:
                name = db.getEmployee(ids)[1]
                cv2.putText(img, name, (x + 2, y + h - 5), cv2.FONT_HERSHEY_SIMPLEX, 1, (150, 255, 0), 2)
                detectionVote.append(ids)
                display.lcdPrint(' ---Scaning---', 1)
                display.lcdPrint(f"___ {name}  __", 2)

            else:
                cv2.putText(img, 'Unknown', (x + 2, y + h - 5), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                display.lcdPrint(' ---Scaning---', 1)

                display.lcdPrint("  =Unknown=", 2)
                detectionVote.append(-1)

        cv2.imshow('Face Recognizer', img)
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break
    cap.release()
    cv2.destroyAllWindows()
    return recognizedId
