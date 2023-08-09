# import required libraries
import RPi.GPIO as GPIO
import time
from Display import Display


class KeyPad:
    def __init__(self):
        self.keypadInit()

    def keypadInit(self):
        self.L1 = 26
        self.L2 = 19
        self.L3 = 13
        self.L4 = 6

        self.C1 = 12
        self.C2 = 16
        self.C3 = 20
        self.C4 = 21
        # Initialize the GPIO pins
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)

        GPIO.setup(self.L1, GPIO.OUT)
        GPIO.setup(self.L2, GPIO.OUT)
        GPIO.setup(self.L3, GPIO.OUT)
        GPIO.setup(self.L4, GPIO.OUT)

        # Make sure to configure the input pins to use the internal pull-down resistors

        GPIO.setup(self.C1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.C2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.C3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.C4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        self.input = ""
        self.display = Display()

    def readLine(self, preText, line, characters):

        GPIO.output(line, GPIO.HIGH)
        self.display.lcdPrint("Clear=* Submit=#",1)
        self.display.lcdPrint(f"{preText}:{self.input}", 2)

        if (GPIO.input(self.C1) == 1):
            if characters[0] == '*':
                self.input = ""
            else:
                self.input += characters[0]
            self.display.lcdPrint(f"{preText}:{self.input}", 2)

        if (GPIO.input(self.C2) == 1):
            self.input += characters[1]
            self.display.lcdPrint(f"{preText}:{self.input}", 2)
        if (GPIO.input(self.C3) == 1):
            if characters[2] == '#':
                self.input += characters[2]
                return self.input
            else:
                self.input += characters[2]
            self.display.lcdPrint(f"{preText}:{self.input}", 2)

        if (GPIO.input(self.C4) == 1):
            self.input += characters[3]
            self.display.lcdPrint(f"{preText}:{self.input}", 2)
        GPIO.output(line, GPIO.LOW)

    def getKeyPadInput(self, preText):
        try:
            while "#" not in self.input:
                # call the readLine function for each row of the keypad
                self.readLine(preText, self.L1, ["1", "2", "3", "A"])
                self.readLine(preText, self.L2, ["4", "5", "6", "B"])
                self.readLine(preText, self.L3, ["7", "8", "9", "C"])
                self.readLine(preText, self.L4, ["*", "0", "#", "D"])
            return self.input.replace("#", "")
        except KeyboardInterrupt:
            print("\nApplication stopped!")



    def rearChar(self,quation, preText, line, characters):

        GPIO.output(line, GPIO.HIGH)
        self.display.lcdPrint(f'{quation}',1)
        self.display.lcdPrint(f"{preText}:{self.input}", 2)

        if (GPIO.input(self.C1) == 1):
            if characters[0] == '*':
                self.input = characters[0]
                self.display.lcdPrint(f"{preText}:{self.input}", 2)
                return self.input


        elif (GPIO.input(self.C3) == 1):
            if characters[2] == '#':
                self.input = characters[2]
                self.display.lcdPrint(f"{preText}:{self.input}", 2)
                return self.input
        else:
            self.input = "___"
            self.display.lcdPrint(f"{preText}:{self.input}", 2)
        GPIO.output(line, GPIO.LOW)

    def getCharInput(self,quation,preText):
        try:
            while '#' not in self.input  and  '*' not in self.input :
                # call the readLine function for each row of the keypad
                self.rearChar(quation,preText, self.L1, ["1", "2", "3", "A"])
                self.rearChar(quation,preText, self.L2, ["4", "5", "6", "B"])
                self.rearChar(quation,preText, self.L3, ["7", "8", "9", "C"])
                self.rearChar(quation,preText, self.L4, ["*", "0", "#", "D"])
            return self.input
        except KeyboardInterrupt:
            print("\nApplication stopped!")


#k = KeyPad()
#display = Display()
#display.lcdClear()
#ch = k.getKeyPadInput("test")
#ch = k.getCharInput('Initiate 2FA ?','yes= # no= *')
#print('ch=====================================================>',ch)
