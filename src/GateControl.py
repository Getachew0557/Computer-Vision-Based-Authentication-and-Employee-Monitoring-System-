#import libraries
import RPi.GPIO as GPIO
import time
from Display import Display

"""

door movement
    inetialy-------------------------------> finaly
      Closed                                open
      45 deg                               45+90deg
du.cycle 4.5                               9.5

assumption
lets
    open the door with one complet step and
    close it with in to step movment 

"""
class door:
    
    def __init__(self):
           
        # set GPIO numbering mode
        GPIO.setmode(GPIO.BCM) # Use BCM GPIO numbers 
        #set pin 17 as output and set servomotor as pin27 as PWM
        self.servoPin = 17
        GPIO.setup(self.servoPin, GPIO.OUT)
        #set frequency of 50 == 2ms cycle time
        self.servo_motor = GPIO.PWM(self.servoPin,50)
        self.servo_motor.start(0)
        
    def setAngle(self,angle):
        duty = angle / 18 + 2
        GPIO.output(self.servoPin, True)
        self.servo_motor.ChangeDutyCycle(duty)
        time.sleep(1)
        GPIO.output(self.servoPin, False)
        self.servo_motor.ChangeDutyCycle(duty)
 
 
       
    def doorControl(self):
        display = Display()
        display.lcdPrint("--DOOR OPENING--",1)
        display.lcdPrint('Please, get in',2)
        self.setAngle(50)

        #wait for 7 second untile the employee/gust enter to the  room
        time.sleep(5)
        display.lcdPrint("-Safety Warning-",1)
        display.lcdPrint('Door is Closing ',2)
        time.sleep(3)
        display.lcdPrint("-Safety Warning-",1)
        display.lcdPrint('--Closing!!-- ',2)
        time.sleep(2)

        self.setAngle(140)
        
        # clean thing up at the end
        self.servo_motor.stop()
        GPIO.cleanup()
   
#d = door()

#d.doorControl()
