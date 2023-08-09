import time
from tkinter import *
from tkinter import messagebox
import RPi.GPIO as GPIO
from time import sleep
class Display:
    def __init__(self):
        self.lcd_init()

    def lcd_init(self):
        GPIO.setwarnings(False)
        # Define GPIO to LCD mapping
        self.LCD_RS = 7
        self.LCD_E = 8

        self.LCD_D4 = 25
        self.LCD_D5 = 24
        self.LCD_D6 = 23
        self.LCD_D7 = 18

        # Define some device constants
        self.LCD_WIDTH = 16  # Maximum characters per line
        self.LCD_CHR = True
        self.LCD_CMD = False

        self.LCD_LINE_1 = 0x80  # LCD RAM address for the 1st line
        self.LCD_LINE_2 = 0xC0  # LCD RAM address for the 2nd line

        # Timing constants
        self.E_PULSE = 0.0005
        self.E_DELAY = 0.005

        

        GPIO.setmode(GPIO.BCM)  # Use BCM GPIO numbers
        
        GPIO.setup(self.LCD_D4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.LCD_D5, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.LCD_D6, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.LCD_D7, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
       
        GPIO.setup(self.LCD_E, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.LCD_RS, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


        

        
        GPIO.setup(self.LCD_E, GPIO.OUT)  # E
        GPIO.setup(self.LCD_RS, GPIO.OUT)  # RS
        GPIO.setup(self.LCD_D4, GPIO.OUT)  # DB4
        GPIO.setup(self.LCD_D5, GPIO.OUT)  # DB5
        GPIO.setup(self.LCD_D6, GPIO.OUT)  # DB6
        GPIO.setup(self.LCD_D7, GPIO.OUT)  # DB7

        self.lcd_display(0x28, self.LCD_CMD)  # Selecting 4 - bit mode with two rows
        self.lcd_display(0x0C, self.LCD_CMD)  # Display On,Cursor Off, Blink Off
        self.lcd_display(0x01, self.LCD_CMD)  # Clear display
        self.lcd_display(0x01, self.LCD_CMD)

        sleep(self.E_DELAY)

    def lcd_display(self,bits, mode):

        
        # Send byte to data pins
        # bits = data
        # mode = True  for character
        #        False for command

        GPIO.output(self.LCD_RS, mode)  # RS

        # High bits
        GPIO.output(self.LCD_D4, False)
        GPIO.output(self.LCD_D5, False)
        GPIO.output(self.LCD_D6, False)
        GPIO.output(self.LCD_D7, False)
        if bits & 0x10 == 0x10:
            GPIO.output(self.LCD_D4, True)
        if bits & 0x20 == 0x20:
            GPIO.output(self.LCD_D5, True)
        if bits & 0x40 == 0x40:
            GPIO.output(self.LCD_D6, True)
        if bits & 0x80 == 0x80:
            GPIO.output(self.LCD_D7, True)

        # Toggle 'Enable' pin
        self.lcd_toggle_enable()

        # Low bits
        GPIO.output(self.LCD_D4, False)
        GPIO.output(self.LCD_D5, False)
        GPIO.output(self.LCD_D6, False)
        GPIO.output(self.LCD_D7, False)
        if bits & 0x01 == 0x01:
            GPIO.output(self.LCD_D4, True)
        if bits & 0x02 == 0x02:
            GPIO.output(self.LCD_D5, True)
        if bits & 0x04 == 0x04:
            GPIO.output(self.LCD_D6, True)
        if bits & 0x08 == 0x08:
            GPIO.output(self.LCD_D7, True)

        # Toggle 'Enable' pin
        self.lcd_toggle_enable()


    def lcd_toggle_enable(self):
        # Toggle enable
        time.sleep(self.E_DELAY)
        GPIO.output(self.LCD_E, True)
        time.sleep(self.E_PULSE)
        GPIO.output(self.LCD_E, False)
        time.sleep(self.E_DELAY)

    def lcdPrint(self,message, line):

        print("line:",line,message)
        # LCD RAM address for the 1st line
        if line ==1:
            line = self.LCD_LINE_1
        elif line ==2:
            line =self.LCD_LINE_2

        # Send string to display

        message = message.ljust(self.LCD_WIDTH, " ")  #update ; why this comes error?

        self.lcd_display(line, self.LCD_CMD)

        for i in range(self.LCD_WIDTH):
            self.lcd_display(ord(message[i]), self.LCD_CHR)
    def lcdClear(self):
        
        self.lcd_display(0x01, self.LCD_CMD)
    
    

    def alert(self,type,message):

        if type =="error":
            messagebox.showerror("showerror", message)
        elif type =="info":
            messagebox.showinfo("showinfo", message)
        elif type =="warning":
            messagebox.showwarning("showwarning",message)
        elif type =="confirmation":
            messagebox.askquestion("askquestion",message)

        # messagebox.askokcancel("askokcancel", "Want to continue?")
        #
        # messagebox.askyesno("askyesno", "Find the value?")
        #
        # messagebox.askretrycancel("askretrycancel", "Try again?d")








#while True:
    #display = Display()
    #display.lcdClear()
    #display.lcdPrint('11fdf1 jo',1)
    #display.lcdPrint('jog\jh jo',2)
