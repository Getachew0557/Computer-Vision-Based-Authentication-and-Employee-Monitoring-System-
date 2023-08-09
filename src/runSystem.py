

import RPi.GPIO as GPIO
import time
from DataBase import Database
from Display import Display
from facial_req import FaceRecognitionClass
from keypad import KeyPad
import os
import shutil
from datetime import datetime
import cv2
from PIL import Image, ImageTk
from DataBase import Database
from Display import Display

from Register import RegisterClass
from facial_req import FaceRecognitionClass
from mailing import Mailing
from keypad import KeyPad
from GateControl import door

GPIO.setwarnings(False)
GPIO.cleanup()

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM) # Use BCM GPIO numbers
pirSensorPIn = 5
ledPin = 11;
#Read output from PIR motion sensor
GPIO.setup(pirSensorPIn, GPIO.IN)
#lED indicator
GPIO.setup(ledPin, GPIO.OUT)
display = Display()

def gustMode():
    global img_tobeSaved
    classifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    if os.path.exists('./Gusts'):
        shutil.rmtree('./Gusts')
        os.makedirs('./Gusts')

        # to create folder with trainer name

        cam = cv2.VideoCapture(0)
        cv2.namedWindow("AASTU -> Capturing of your photo...", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("AASTU -> Capturing of your photo...", 500, 300)

        img_counter = 0
        while True:
            ret, frame = cam.read()

            if not ret:
                print("failed to grab frame")
                break
            faces = classifier.detectMultiScale(frame, 1.3, 5)
            """
            if faces == ():
                cv2.putText(frame, 'NO FACE FOUND!', (50, 50), cv2.FONT_HERSHEY_TRIPLEX, 1, (0, 0, 255), 2)
                cv2.putText(frame, 'pleas change your position!', (50, 80), cv2.FONT_HERSHEY_TRIPLEX, 1, (0, 0, 255), 1)
                cv2.imshow("AASTU -> Capturing of your photo...", frame)
            """
            for (x, y, w, h) in faces:
                today = datetime.now()
                date = today.strftime("%d/%m/%Y")
                times = today.strftime("%I:%M:%S")
                cv2.putText(frame, f'Captured at{date} {times}', (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255))

                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.imshow("AASTU -> Capturing of your photo...", frame)

                img_tobeSaved = frame

            key = cv2.waitKey(1)

            if key % 256 == 27:
                # ESC pressed
                print("Escape hit, closing...")
                break
            if faces != ():
                today = datetime.now()
                date = today.strftime("%d_%m_%Y")
                times = today.strftime("%I-%M-%S")
                imagePath = "Gusts/gust_Captured at" + date + " " + times + ".jpg"
                isWriten = cv2.imwrite(imagePath, img_tobeSaved)

                if isWriten:
                    print(f'{imagePath} is writen')
                    img_counter += 1
                    time.sleep(.5)

            if img_counter > 2:
                break
            # two second delay

        cam.release()
        cv2.destroyAllWindows()
        mailing = Mailing()

        gustId = mailing.gustMode('yosfemyayu@gmail.com', 'Gusts')

        # =====for the gust =============hear little code for motor implementation
        if gustId == -2:
            display.lcdPrint("  welcome", 1)

            ## call the door opening fun()
            
            dr  = door()
            dr.doorControl()


        else:
            display.lcdPrint("== Warning !==", 1)
            display.lcdPrint("Pls go away ", 2)
def startFaceRecognition():
    # instance of the recognizer class
    faceDetection = FaceRecognitionClass()
    recognizedId = faceDetection.recognize()
    if recognizedId >= 0:
        print('reterned ids ====', recognizedId)
        db = Database()
        recognizedEmployee = db.getEmployee(recognizedId)
        display.lcdPrint(f"Dear {recognizedEmployee[1]}", 1)
        display.lcdPrint(" == Welcome == ", 2)


          
        db.inserToAttendanceTable(recognizedId)

        db.inserToReportTable(recognizedId)
         

            # for attendance recording
        attendances = db.getAttendanceTable()
        dr  = door()
        dr.doorControl()

    else:
        display.lcdPrint("FACE UNKNOWN!", 1)
        display.lcdPrint("Unauthorized...", 2)
        time.sleep(3)

        keypad = KeyPad()
        ch = keypad.getCharInput('Are you Gust ?','yes= # no= *')
        if ch == '#':
            display.lcdPrint("Look at z camera",1)
            display.lcdPrint("Capturing...",2)
            gustMode()

        elif ch == '*':
            display.lcdPrint('---WARNING---',1)
            display.lcdPrint('Please, go away!',2)
            time.sleep(3)

isPersinPresent = False
display = Display()
display.lcdPrint('___ WELLCOME __',1)
display.lcdPrint('   1________1',2)
time.sleep(3)

while True:
    display = Display()
    print(GPIO.input(pirSensorPIn))
    result=GPIO.input(pirSensorPIn)
    #GPIO.output(ledPin,result)
    # When output from motion sensor is LOW
    if result==1:
        print( "person  detected:============== ",result)
        display.lcdPrint("person detected", 1)
        startFaceRecognition () #start recognitio
        time.sleep(0.005)
        
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM) # Use BCM GPIO numbers
        pirSensorPIn = 5
        ledPin = 11;
        #Read output from PIR motion sensor
        GPIO.setup(pirSensorPIn, GPIO.IN)
        #lED indicator
        GPIO.setup(ledPin, GPIO.OUT)
        
    elif result==0:               #When output from motion sensor is HIGH
        print( "no person detected :i= ",result)
        time.sleep(0.001)
    #result=GPIO.input(pirSensorPIn)


    