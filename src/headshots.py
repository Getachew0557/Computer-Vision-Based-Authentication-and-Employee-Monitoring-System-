import cv2
import os
import time
from Display import Display
from keypad import KeyPad

class HeadShote:
    def __init__(self, employId):
        self.employId = employId
        if not os.path.exists('./Dataset'):
            os.makedirs('./Dataset')
        self.classifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    def startHeadshot(self):
        self.dispaly = Display()
        # to create folder with trainer name
        global img_tobeSaved


        cam = cv2.VideoCapture(0)
        cv2.namedWindow("AASTU -> Capturing of your photo...", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("AASTU -> Capturing of your photo...", 500, 300)

        img_counter = 0
        while True:
            ret, frame = cam.read()

            if not ret:
                print("failed to grab frame")
                break
            faces = self.classifier.detectMultiScale(frame, 1.3, 5)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            if faces == ():
                cv2.putText(frame, 'NO FACE FOUND!', (50, 50), cv2.FONT_HERSHEY_TRIPLEX, 1, (0, 0, 255), 2)
                cv2.putText(frame, 'pleas change your position!', (50, 80), cv2.FONT_HERSHEY_TRIPLEX, 1, (0, 0, 255), 1)
                cv2.imshow("AASTU -> Capturing of your photo...", frame)
                
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.imshow("AASTU -> Capturing of your photo...", frame)
                img_tobeSaved = gray[y:y + h, x:x + w]

            if img_counter < 10:
                cv2.putText(frame, 'NORMAL!', (500, 50), cv2.FONT_HERSHEY_TRIPLEX, 1, (255, 0, 0), 2)
                cv2.imshow("AASTU -> Capturing of your photo...", frame)
                time.sleep(0.5)
            elif img_counter < 20:
                cv2.putText(frame, 'SMILE!', (500, 50), cv2.FONT_HERSHEY_TRIPLEX, 1, (255, 0, 0), 2)
                cv2.imshow("AASTU -> Capturing of your photo...", frame)
                time.sleep(0.5)

            elif img_counter < 30:
                cv2.putText(frame, 'ANGER!', (500, 50), cv2.FONT_HERSHEY_TRIPLEX, 1, (255, 0, 0), 2)
                cv2.imshow("AASTU -> Capturing of your photo...", frame)
                time.sleep(0.5)

            elif img_counter < 40:
                cv2.putText(frame, 'SURPRISE!', (600, 50), cv2.FONT_HERSHEY_TRIPLEX, 1, (255, 0, 0), 2)
                cv2.imshow("AASTU -> Capturing of your photo...", frame)

            key = cv2.waitKey(1)

            if key % 256 == 27:
                # ESC pressed
                print("Escape hit, closing...")
                break
            if faces != ():
                imagePath ="Dataset/Employee." + str(self.employId) + "." + str(img_counter) + ".jpg"
                isWriten = cv2.imwrite(imagePath,img_tobeSaved)

                if isWriten:
                    print(f'{imagePath} is writen')
                    img_counter += 1

            if img_counter > 50:
                break
            # two second delay for the nest facial  expression preparation
            if img_counter%11 == 0:
                time.sleep(1)

        cam.release()
        cv2.destroyAllWindows()
