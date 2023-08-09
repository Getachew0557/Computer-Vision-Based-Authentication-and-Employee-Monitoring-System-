import sqlite3
from datetime import datetime
from tkinter import ttk, END, VERTICAL
import tkinter as tk
from tkinter.messagebox import showinfo

class Database:
    # employees
    def insertToEmployee(self, trainer):
        connection = sqlite3.connect('trainer.db')
        cursor = connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS employee(
                         id INTEGER PRIMARY KEY AUTOINCREMENT,
                         firstName TEXT NOT NULL,
                         lastName TEXT NOT NULL,
                         gender TEXT NOT NULL,
                    
                         department TEXT,
                         
                         email TEXT NOT NULL,
                         userId TEXT NOT NULL,
                         password TEXT NOT NULL,
                         
                         registerdDate TEXT)
        ''')

        cursor.execute(fr"SELECT * FROM employee WHERE firstName ='{trainer[0]}' and lastName ='{trainer[0]}' ")
        rows = cursor.fetchall()
        if len(rows) > 0:
            print(trainer[0], ' is already registered')
        else:
            cursor.execute("INSERT INTO employee VALUeS(null,?,?,?,?,?,?,?,?)",
                           (trainer[0], trainer[1], trainer[2], trainer[3], trainer[4], trainer[5]
                            , trainer[6], trainer[7]))
        connection.commit()
        connection.close()

    def getEmployees(self):
        connection = sqlite3.connect('trainer.db')
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM employee")
        rows = cursor.fetchall()
        connection.commit()
        connection.close()
        return rows

    def getEmployee(self, id):
        connection = sqlite3.connect('trainer.db')
        cursor = connection.cursor()
        cursor.execute(fr"SELECT *FROM employee WHERE id ={id}")
        row = cursor.fetchall()
        connection.commit()
        connection.close()
        return row[0]

    def getEmployeeEmail(self, userId,password):
        connection = sqlite3.connect('trainer.db')
        cursor = connection.cursor()
        cursor.execute(fr"SELECT email FROM employee WHERE userId ='{userId}' and password ='{password}'")
        row = cursor.fetchall()
        connection.commit()
        connection.close()
        return row

    def removeEmployee(self, id):
        connection = sqlite3.connect('trainer.db')
        cursor = connection.cursor()
        cursor.execute(fr"DELETE FROM employee WHERE id ={id}")
        connection.commit()
        connection.close()

    def showEmployeesList(self):
        root = tk.Tk()
        # root.geometry("40x400")
        root.title("AASTU -->list of all Employees")
        root.attributes('-topmost', True)
        # style = ttk.Style()
        # style.theme_use('winnative')

        label = tk.Label(root,
                         text="List Of All Registered Employees",
                         font=('times', 20, 'bold'), fg='blue', bg="#88cffa", pady=10)
        label.grid(row=0, column=0, columnspan=4, sticky='nsew')

        # ===================table =====================================
        self.tree = ttk.Treeview(root,
                                 column=(
                                     "id", "fName", "lName", "gender", "department",
                                     "email", "userId", "password", "registrationDate"),
                                 show="headings",
                                 height=30)
        self.tree.heading('id', text="ID")
        self.tree.heading('fName', text="Firs Name")
        self.tree.heading('lName', text="Last Name")
        self.tree.heading('gender', text="Gender")
        self.tree.heading('department', text="Department")

        self.tree.heading('email', text="Email")
        self.tree.heading('userId', text="userId")
        self.tree.heading('password', text="Password")

        self.tree.heading('registrationDate', text="Date of Registration")

        self.tree.column('id', width=30)
        self.tree.column('fName', width=80)
        self.tree.column('lName', width=80)
        self.tree.column('gender', width=50)
        self.tree.column('email', width=100)
        self.tree.column('userId', width=100)
        self.tree.column('password', width=100)
        # self.tree.bind('<<TreeviewSelect>>', self.itemSelected)
        # ============================end table=======================

        # lis of registerd person
        employees = self.getEmployees()
        for employee in employees:
            self.tree.insert('', END, values=employee)
        # add scrollbar to the table
        scrollbar = ttk.Scrollbar(root, orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=1, column=2, sticky='ns')
        self.tree.grid(row=1, column=1, sticky='nsew')
        root.mainloop()

    #
    # def itemSelected(self, event):
    #     for selectedItem in self.tree.selection():
    #         item = self.tree.item(selectedItem)
    #         record = item['values']
    #         showinfo(title="information", message=record[5])

    # for the report table

    # attendance
    def inserToAttendanceTable(self, detectedPersonId):
        connection = sqlite3.connect('trainer.db')
        cursor = connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS Attendance(
                         rollNumber INTEGER PRIMARY KEY AUTOINCREMENT,
                         id INTEGER NOT NULL,
                         firstName TEXT NOT NULL,
                         lastName TEXT NOT NULL,
                         gender TEXT NOT NULL,
                         department TEXT,
                         date TEXT,
                         time TEXT
                         )
     ''')

        detectedPerson = self.getEmployee(detectedPersonId)
        today = datetime.now()
        date = today.strftime("%d/%m/%Y")
        time = today.strftime("%I:%M:%S")

        # leave if the employee's attendance already token for today
        quarry = fr"SELECT * FROM Attendance WHERE id ='{detectedPersonId}' and date ='{date}'"
        rows = self.executeQuery(quarry)
        if len(rows)== 0:
            # jo create a directory when trained a person in register class
            cursor.execute("INSERT INTO Attendance VALUeS(null,   ?,?,?,?,?,   ?,?)",
                           (detectedPerson[0], detectedPerson[1], detectedPerson[2], detectedPerson[3],
                            detectedPerson[4], date, time))

        connection.commit()
        connection.close()

    def getAttendanceTable(self):
        connection = sqlite3.connect('trainer.db')
        cursor = connection.cursor()
        # jo exclude it
        # cursor.execute('''CREATE TABLE IF NOT EXISTS Attendance(
        #                          rollNumber INTEGER PRIMARY KEY AUTOINCREMENT,
        #                          id INTEGER NOT NULL,
        #                          firstName TEXT NOT NULL,
        #                          lastName TEXT NOT NULL,
        #                          gender TEXT NOT NULL,
        #                          department TEXT,
        #                          date TEXT,
        #                          time TEXT
        #                          )
        #      ''')
        try:
            cursor.execute("SELECT * FROM Attendance")
            rows = cursor.fetchall()
        except:
            rows =(())
        connection.commit()
        connection.close()
        return rows

    def getTodaysAttendance(self):
        connection = sqlite3.connect('trainer.db')
        cursor = connection.cursor()
        today = datetime.now()
        date = today.strftime("%d/%m/%Y")
        # filter-out only today's Attendance
        cursor.execute(fr"SELECT * FROM Attendance WHERE date ='{date}'")
        rows = cursor.fetchall()
        connection.commit()
        connection.close()
        return rows

    def getAttendanceOf(self, name):
        connection = sqlite3.connect('trainer.db')
        cursor = connection.cursor()
        cursor.execute(fr"SELECT * FROM Attendance WHERE firstName ='{name}'")
        rows = cursor.fetchall()
        connection.commit()
        connection.close()
        return rows

    def showAttendanceList(self):
        root = tk.Tk()
        # root.geometry("200x400")
        root.title("AASTU -->Reports")
        root.attributes('-topmost', True)
        # style = ttk.Style()
        # style.theme_use('winnative')

        label = tk.Label(root,
                         text="List Of All Records",
                         font=('times', 20, 'bold'), fg='blue', bg="#88cffa", pady=10)
        label.grid(row=0, column=0, columnspan=4, sticky='nsew')

        # ===================table =====================================
        self.tree = ttk.Treeview(root,
                                 column=(
                                     "id", "fName", "lName", "gender", "department"),
                                 show="headings",
                                 height=30)
        self.tree.heading('id', text="ID")
        self.tree.heading('fName', text="Firs Name")
        self.tree.heading('lName', text="Last Name")
        self.tree.heading('gender', text="Gender")
        self.tree.heading('department', text="Department")

        self.tree.column('id', width=30)
        self.tree.column('fName', width=80)
        self.tree.column('lName', width=80)
        self.tree.column('gender', width=50)
        # self.tree.bind('<<TreeviewSelect>>', self.itemSelected)
        # ============================end table=======================

        # lis of registerd person
        attendances = self.getAttendanceTable()
        for attendance in attendances:
            self.tree.insert('', END, values=attendance)
        # add scrollbar to the table
        scrollbar = ttk.Scrollbar(root, orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=1, column=2, sticky='ns')
        self.tree.grid(row=1, column=1, sticky='nsew')
        root.mainloop()

    # reports
    def inserToReportTable(self, detectedPersonId):
        connection = sqlite3.connect('trainer.db')
        cursor = connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS Report(
                         rollNumber INTEGER PRIMARY KEY AUTOINCREMENT,
                         
                         id INTEGER NOT NULL,
                         firstName TEXT NOT NULL,
                         lastName TEXT NOT NULL,
                         gender TEXT NOT NULL,
                         department TEXT,
                         
                         gate TEXT,
                         date TEXT,
                         time TEXT,
                         pic TEXT
                         )
     ''')

        detectedPerson = self.getEmployee(detectedPersonId)
        today = datetime.now()
        date = today.strftime("%d/%m/%Y")
        time = today.strftime("%I:%M:%S")

        # jo create a directory when trained a person in register class
        pic = fr'c:/joj/am/pic At the gate{detectedPerson}/AT {date} {time}'
        gateNumber = 'GATE 1'

        cursor.execute("INSERT INTO Report VALUeS(null,?,?,?,?,?,?,?,?,?)",
                       (detectedPerson[0], detectedPerson[1], detectedPerson[2], detectedPerson[3],
                        detectedPerson[4], gateNumber, date, time, pic))
        connection.commit()
        connection.close()

    def getReportTable(self):
        connection = sqlite3.connect('trainer.db')
        cursor = connection.cursor()

        cursor.execute('''CREATE TABLE IF NOT EXISTS Report(
                                rollNumber INTEGER PRIMARY KEY AUTOINCREMENT,
                                id INTEGER NOT NULL,
                                firstName TEXT NOT NULL,
                                lastName TEXT NOT NULL,
                                gender TEXT NOT NULL,
                                department TEXT,
                                gate TEXT,
                                date TEXT,
                                time TEXT,
                                pic TEXT
                                )
            ''')
        cursor.execute("SELECT * FROM Report")
        rows = cursor.fetchall()
        connection.commit()
        connection.close()
        return rows

    def getTodaysReport(self):
        connection = sqlite3.connect('trainer.db')
        cursor = connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS Report(
                                   rollNumber INTEGER PRIMARY KEY AUTOINCREMENT,
                                   id INTEGER NOT NULL,
                                   firstName TEXT NOT NULL,
                                   lastName TEXT NOT NULL,
                                   gender TEXT NOT NULL,
                                   department TEXT,
                                   gate TEXT,
                                   date TEXT,
                                   time TEXT,
                                   pic TEXT
                                   )
               ''')
        today = datetime.now()
        date = today.strftime("%d/%m/%Y")
        # filter-out only today's report
        cursor.execute(fr"SELECT * FROM Report WHERE date ='{date}'")
        rows = cursor.fetchall()
        connection.commit()
        connection.close()
        return rows


    def getReportOf(self, name):
        connection = sqlite3.connect('trainer.db')
        cursor = connection.cursor()
        cursor.execute(fr"SELECT * FROM Report WHERE firstName ='{name}'")
        rows = cursor.fetchall()
        connection.commit()
        connection.close()
        return rows

    def showReportList(self):
        root = tk.Tk()
        # root.geometry("200x400")
        root.title("AASTU -->Reports")
        root.attributes('-topmost', True)
        # style = ttk.Style()
        # style.theme_use('winnative')

        label = tk.Label(root,
                         text="List Of All Recors",
                         font=('times', 20, 'bold'), fg='blue', bg="#88cffa", pady=10)
        label.grid(row=0, column=0, columnspan=4, sticky='nsew')

        # ===================table =====================================
        self.tree = ttk.Treeview(root,
                                 column=(
                                     "id", "fName", "lName", "gender", "department", "registrationDate"),
                                 show="headings",
                                 height=30)
        self.tree.heading('id', text="ID")
        self.tree.heading('fName', text="Firs Name")
        self.tree.heading('lName', text="Last Name")
        self.tree.heading('gender', text="Gender")
        self.tree.heading('department', text="Department")
        self.tree.heading('registrationDate', text="Date of Registration")

        self.tree.column('id', width=30)
        self.tree.column('fName', width=80)
        self.tree.column('lName', width=80)
        self.tree.column('gender', width=50)
        # self.tree.bind('<<TreeviewSelect>>', self.itemSelected)
        # ============================end table=======================

        # lis of registerd person
        reports = self.getReportTable()
        for report in reports:
            self.tree.insert('', END, values=report)
        # add scrollbar to the table
        scrollbar = ttk.Scrollbar(root, orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=1, column=2, sticky='ns')
        self.tree.grid(row=1, column=1, sticky='nsew')
        root.mainloop()

    #
    # def increamentId(self):
    #     connection = sqlite3.connect('trainer.db')
    #     cursor = connection.cursor()
    #     cursor.execute('''CREATE TABLE IF NOT EXISTS ids(
    #                      id INTEGER PRIMARY KEY AUTOINCREMENT)
    #                    ''')
    #     cursor.execute("INSERT INTO ids VALUeS(null)",
    #                    ())
    #     connection.commit()
    #     connection.close()
    #
    # def getLastId(self):
    #     self.increamentId()
    #     connection = sqlite3.connect('trainer.db')
    #     cursor = connection.cursor()
    #     cursor.execute("SELECT * FROM ids")
    #     rows = cursor.fetchall()
    #     connection.commit()
    #     connection.close()
    #     lastId = len(rows)
    #     return lastId

    # method to execute Query
    def executeQuery(self,query):
        connection = sqlite3.connect('trainer.db')
        cursor = connection.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        connection.commit()
        connection.close()
        return rows

    def isEmployeeExist(self, fName,lName):
        val = False
        connection = sqlite3.connect('trainer.db')
        cursor = connection.cursor()
        #handl exception incase table is not exist or created
        try:
            cursor.execute(fr"SELECT * FROM employee WHERE firstName ='{fName}' and lastName ='{lName}' ")
            rows = cursor.fetchall()
            if len(rows) > 0:
                val = True
        except:
            print('exception handled in table existance')
        connection.commit()
        connection.close()
        return val

    def isUserIdToken(self, userid):
        val = False
        connection = sqlite3.connect('trainer.db')
        cursor = connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS employee(
                         id INTEGER PRIMARY KEY AUTOINCREMENT,
                         firstName TEXT NOT NULL,
                         lastName TEXT NOT NULL,
                         gender TEXT NOT NULL,

                         department TEXT,

                         email TEXT NOT NULL,
                         userId TEXT NOT NULL,
                         password TEXT NOT NULL,

                         registerdDate TEXT)
        ''')

        cursor.execute(fr"SELECT * FROM employee WHERE userId ='{userid}'")
        rows = cursor.fetchall()
        if len(rows) > 0:
            val = True
        connection.commit()
        connection.close()
        return val

    def getEmployeeId(self, fName,lName):
           query = fr"SELECT id FROM employee WHERE firstName ='{fName}' and lastName ='{lName}' "
           id = self.executeQuery(query)
           return id[0][0]
