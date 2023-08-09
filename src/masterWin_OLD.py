import csv
import os
import shutil
import time
import cv2
from datetime import datetime
from tkinter import *
from tkinter import ttk

from DataBase import Database
from Display import Display
from Register import RegisterClass
from facial_req import FaceRecognitionClass
from mailing import Mailing


class MasterClass:
    print('hello test')
    def showMain(self):
        self.display = Display()

        self.mainWindow = Tk()

        width = self.mainWindow.winfo_screenwidth()
        height = self.mainWindow.winfo_screenheight()
        self.mainWindow.geometry("%dx%d" % (width, height))
        self.mainWindow.title("AASTU -->Main window")
        self.mainWindow.grid_columnconfigure(0, weight=1)
        self.employeeTrackTree = ttk.Treeview(self.mainWindow,
                                              column=("rollNumber", "id", "fname", "lname", "gender", "department",
                                                       "gate","date" ,"time", "pic"),
                                              show="headings",
                                              height=7)

        self.employeeAttendanceTree = ttk.Treeview(self.mainWindow,
                                              column=("rollNumber", "id", "fname", "lname", "gender", "department",
                                                      'date',"time"),
                                              show="headings",
                                              height=12)


        #style = ttk.Style()
        #style.theme_use('winnative')
        label = Label(self.mainWindow,
                      text="Computer Vision Based Authentication And Employ monitoring System",

                      font=('times', 20, 'bold'), fg='blue', bg="#88cffa", pady=13)
        label.grid(row=0, column=0, columnspan=5, sticky='ew')
        label = Label(self.mainWindow,
                      font=('times', 20, 'bold'), fg='blue', bg="#81cffa", pady=8)
        label.grid(row=10, column=0, columnspan=4, sticky='nsew')

        # ===================push button===========================================================
        openDor = Button(self.mainWindow, text="Open Door",
                         font=('times', 15, 'bold'), fg='blue', bg="gray", pady=5,
                         command =self.startFaceRecognition)
        openDor.grid(row=10, column=0, columnspan=2)


        # ===============================left side button frame==================================
        buttonFrame = LabelFrame(self.mainWindow, fg='blue', text="For only the admins", padx=20, pady=20,
                                 font=('times', 15, 'bold'))
        buttonFrame.grid(row=1, column=0)

        button1 = Button(buttonFrame, text="New Registration", font=('times', 13, 'bold italic'), fg='blue',
                         width='15', bg="#88cffa",
                         pady=5,command =self.register).pack(pady=5)

        button2 = Button(buttonFrame, text="Total List", font=('times', 13, 'bold italic'), fg='blue',
                         width='15', bg="#88cffa",
                         pady=5,command =self.showEmployeesList).pack(pady=5)

        button3 = Button(buttonFrame, text="Remove", font=('times', 13, 'bold italic'), fg='blue',
                         width='15', bg="#88cffa",
                         pady=5,command=self.remove).pack(pady=5)

        button4 = Button(buttonFrame, text="Generate Attendance", font=('times', 13, 'bold italic'), fg='blue',
                         width='15', bg="#88cffa",
                         pady=5,command=self.attendance).pack(pady=5)

        button5 = Button(buttonFrame, text="Generate Report", font=('times', 13, 'bold italic'), fg='blue',
                            width='15', bg="#88cffa",
                         pady=5 ,command = self.report).pack(pady=6)

    # ===============================right side image frame ===============================

        imageFrame = LabelFrame(self.mainWindow, fg='blue', text="pic at the moment", padx=20, pady=20,
                                font=('times', 15, 'bold'))
        imageFrame.grid(row=2, column=3)

        img = PhotoImage(file="aastuIcon.png")
        # label2 = Label(imageFrame, image=img).pack()


    # ================ employe traking table ======================

        self.employeeTrackTree.heading('rollNumber', text="#")
        self.employeeTrackTree.heading('id', text="ID")
        self.employeeTrackTree.heading('fname', text="First Name")
        self.employeeTrackTree.heading('lname', text="Last Name")
        self.employeeTrackTree.heading('gender', text="Gender")
        self.employeeTrackTree.heading('department', text="Department")
        self.employeeTrackTree.heading('gate', text="Gate Number")
        self.employeeTrackTree.heading('date', text="Date")
        self.employeeTrackTree.heading('time', text="Time")
        self.employeeTrackTree.heading('pic', text="picture at the gate")

        self.employeeTrackTree.column('rollNumber', width=15)
        self.employeeTrackTree.column('id', width=40)
        self.employeeTrackTree.column('fname', width=120)
        self.employeeTrackTree.column('lname', width=120)
        self.employeeTrackTree.column('gender', width=70)

        self.employeeTrackTree.column('gate', width=100)
        self.employeeTrackTree.column('department', width=100)
        self.employeeTrackTree.column('date', width=120)
        self.employeeTrackTree.column('time', width=170)

        self.employeeTrackTree.column('pic', width=150)


    # ================ employe Attendance table ======================

        self.employeeAttendanceTree.heading('rollNumber', text="#")
        self.employeeAttendanceTree.heading('id', text="ID")
        self.employeeAttendanceTree.heading('fname', text="First Name")
        self.employeeAttendanceTree.heading('lname', text="Last Name")
        self.employeeAttendanceTree.heading('gender', text="Gender")
        self.employeeAttendanceTree.heading('department', text="Department")
        self.employeeAttendanceTree.heading('time', text="Time")
        self.employeeAttendanceTree.heading('date', text="Date")

        self.employeeAttendanceTree.column('rollNumber', width=15)
        self.employeeAttendanceTree.column('id', width=30)
        self.employeeAttendanceTree.column('fname', width=90)
        self.employeeAttendanceTree.column('lname', width=90)
        self.employeeAttendanceTree.column('gender', width=70)
        self.employeeAttendanceTree.column('department', width=100)
        self.employeeAttendanceTree.column('time', width=150)
        self.employeeAttendanceTree.column('date', width=150)


        # self.tree.bind('<<TreeviewSelect>>', self.itemSelected)
        # lis of today entry


        db = Database()

        registerdPersons = db.getReportTable()
        for person in registerdPersons:
            self.employeeTrackTree.insert('', 0, values=person)

        antendances = db.getAttendanceTable()
        for attendance in antendances:
            self.employeeAttendanceTree.insert('', 0, values=attendance)

    # add scrollbar to the employee traking table
        scrollbar1 = ttk.Scrollbar(self.mainWindow,orient=VERTICAL, command=self.employeeTrackTree.yview)
        self.employeeTrackTree.configure(yscroll=scrollbar1.set)
        scrollbar1.grid(row=1, column=4,sticky='ns')
        self.employeeTrackTree.grid(row=1, column=1,columnspan = 3, sticky='nsew')




    # add scrollbar to attendance table
        scrollbar2 = ttk.Scrollbar(self.mainWindow, orient=VERTICAL, command=self.employeeAttendanceTree.yview)
        self.employeeAttendanceTree.configure(yscroll=scrollbar2.set)
        scrollbar2.grid(row=2, column=2, sticky='ns')
        self.employeeAttendanceTree.grid(row=2, column=1,columnspan = 1, sticky='nsew')


        self.mainWindow.mainloop()

    def register(self):
        registerWindow = RegisterClass()
        registerWindow.showWindow()


    def startFaceRecognition(self):
        # instance of the recognizer class
        faceDetection = FaceRecognitionClass()
        recognizedId = faceDetection.recognize()
        if recognizedId >=0:
            print('reterned ids ====', recognizedId)
            db = Database()
            recognizedEmployee =db.getEmployee(recognizedId)
            self.display.lcdPrint(f"Dear {recognizedEmployee[1]}",1)
            self.display.lcdPrint(" == Welcome == ",2)

            ctypes.windll.user32.MessageBoxW(0, f"Dear {recognizedEmployee[1]} ,Welcome   ",
                                              "AASTU -> Face Recognized", 1)
            
            db.inserToAttendanceTable(recognizedId)
            db.inserToReportTable(recognizedId)

    # for attendance recording
            attendances = db.getAttendanceTable()
            # to remove the initial value of table to avoid dependency
            for row in self.employeeAttendanceTree.get_children():
                self.employeeAttendanceTree.delete(row)

            for attendance in attendances:
                self.employeeAttendanceTree.insert('', 0, values=attendance)
            self.mainWindow.update_idletasks()

    # for recording employee repoort table
            reports = db.getReportTable()
            # to remove the initial value of table to avoid dependency
            for row in self.employeeTrackTree.get_children():
                self.employeeTrackTree.delete(row)

            for report in reports:
                self.employeeTrackTree.insert('', 0, values=report)
            self.mainWindow.update_idletasks()

        else:
            self.display.lcdPrint("Unknown Face!",1)
            self.display.lcdPrint("Unauthorized.",2)
            self.gustMode()

    def showEmployeesList(self):
        db = Database()
        db.showEmployeesList()

 #methods to remove/delete employee
    def remove(self):

        self.removeroot = Tk()
        self.removeroot.geometry('500x280')
        self.removeroot.title('removing  ...')

        labelTitle = Label(self.removeroot, text="  Removing selected person    ", fg='blue',
                           font=('times', 25, 'bold'),
                           bg="#88cffa",
                           pady=10, padx=40)
        labelTitle.grid(column=0, row=0, columnspan=3, pady=10)

        label2 = Label(self.removeroot, text="Warning!!! data can't be recovered once it removed  ", fg='red',
                       font=('times', 15, 'bold'),
                       pady=10).grid(row=1, column=0, columnspan=3)

        label1 = Label(self.removeroot, text="  Enter ID number:", fg='blue', font=('times', 15, 'bold'),
                       pady=10).grid(row=2, column=0)
        detailBtn = Button(self.removeroot, text="Detail", fg='blue', font=('times', 10, 'italic'),
                           command=self.detile).grid(row=2, column=2, )

        self.id = Entry(self.removeroot, font=('times', 13, 'italic'), width=20, fg='blue')
        self.id.grid(row=2, column=1)

        removeBtn = Button(self.removeroot, text="Remove", fg='blue', font=('times', 15, 'bold'),
                           command=self.removed).grid(row=10, column=0, columnspan=3)
        self.removeroot.mainloop()

    def detile(self):
        d = Database()
        print(d.getEmployee(int(self.id.get())))
        self.detailLabell = Label(self.removeroot, text="", fg='black',
                                  font=('times', 12, 'italic'),
                                  pady=10).grid(row=5, column=0, columnspan=3)
        self.detailLabell = Label(self.removeroot, text=f"{d.getEmployee(int(self.id.get()))}", fg='black',
                                  font=('times', 12, 'italic'),
                                  pady=10).grid(row=5, column=0, columnspan=3)

        self.removeroot.update_idletasks()

    def removed(self):
        db = Database()
        subject = "Account Removed"
        messages = "Since your account is permanently deleted by System admins,you can't access the system as like other employees.For more info contact the system admins"
        header = " your Account is removed by admin of the system"
        email = db.getEmployee(int(self.id.get()))[5]

        #db.removeEmployee(int(self.id.get()))
        mailing = Mailing()
        mailing.sentMail(email,subject,header,messages)
        print("========= malling sent" )
 #===============================

    def report(self):
        desktop = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')
        #desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')

        path = desktop+"\\Monitoring System\\Tracking Report"
        if not os.path.exists(path):
            os.makedirs(path)
        todayReport = path+"\\Today's Report .csv"
        summarisedReport =path+"\\Summarised Report.csv"

        db = Database()
        header = ['ID', 'First Name', 'Last Name', 'Gender', 'Department', 'Gate number',
                  'Entry Date', 'Entry Time']

        todaysrow = db.getTodaysReport()
        with open(todayReport, 'w', newline="") as file:
            writer = csv.writer(file)
            writer.writerow(header)
            for row in todaysrow:
                writer.writerow(row[1:])
            file.close()
    #generating summarised report
        summarisedRow = db.getReportTable()
        with open(summarisedReport, 'w', newline="") as file:
            writer = csv.writer(file)
            writer.writerow(header)
            for row in summarisedRow:
                writer.writerow(row[1:])
            file.close()
            self.display.alert('info',"report Generated on:"+path)
    def attendance(self):
        desktop = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')
        #desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')

        path = desktop+"\\Monitoring System\\Attendance Report"
        if not os.path.exists(path):
            os.makedirs(path)
        todayAttendance = path+"\\Today's Attendance .csv"
        summarisedAttendance =path+"\\Summarised Attendance.csv"

        db = Database()
        header = ['ID', 'First Name', 'Last Name', 'Gender', 'Department','Date'
                  'Time']

        todaysrow = db.getTodaysAttendance()
        with open(todayAttendance, 'w', newline="") as file:
            writer = csv.writer(file)
            writer.writerow(header)
            for row in todaysrow:
                writer.writerow(row[1:])
            file.close()
    #generating summarised report
        summarisedRow = db.getAttendanceTable()
        with open(summarisedAttendance, 'w', newline="") as file:
            writer = csv.writer(file)
            writer.writerow(header)
            for row in summarisedRow:
                writer.writerow(row[1:])
            file.close()
        self.display.alert('info', "Attendance Generated on:" + path)


 #=============optional authentication=====
    def gustMode(self):
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

            if faces == ():
                cv2.putText(frame, 'NO FACE FOUND!', (50, 50), cv2.FONT_HERSHEY_TRIPLEX, 1, (0, 0, 255), 2)
                cv2.putText(frame, 'pleas change your position!', (50, 80), cv2.FONT_HERSHEY_TRIPLEX, 1, (0, 0, 255), 1)
                cv2.imshow("AASTU -> Capturing of your photo...", frame)

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
        mailing.sentAdminAllert('getachewgetu2010@gmail.com','Gusts') # Guests is image_directory
         #update  : below two lines causen error; why?
        self.display.lcdPrint(1,"Request sent")
        self.display.lcdPrint(2,"Waiting replay")
        print("Dear user, If the Admin confirm your request, you will get an entry psw")
        
       #update :to be done... 
       #call password login window via the lcd:
       
       #the best so/n is using otp, after the admin press "confirm" button @the gmail's html page;
       
       #let the admin sent confirm :
       

a = MasterClass()
a.showMain()
