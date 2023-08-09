import tkinter as tk
from datetime import datetime
from tkinter.ttk import Progressbar

# from headshots import HeadShote
# from train_model import Trainer
from DataBase import Database
from headshots import HeadShote
from train_model import Trainer


class RegisterClass:
    def showWindow(self):
        root = tk.Tk()
        root.geometry('1060x680')
        root.title('Registration...')
        labelTitle = tk.Label(root, text="New Registration", fg='blue', font=('times', 25, 'bold'), bg="#88cffa",
                              pady=10,
                              width=850)
        labelTitle.pack()

        self.frame = tk.LabelFrame(root, text="Fill all the required field", padx=30, pady=30, font=('times', 15, 'italic'),fg='#9a1e1e')
        self.frame.pack(pady=40)

    # labeled fields
        label1 = tk.Label(self.frame, text="First Name", font=('times', 13, 'bold')).grid(row=0, column=0,sticky='e')
        label2 = tk.Label(self.frame, text="Last Name", font=('times', 13, 'bold')).grid(row=1, column=0,sticky='e')
        label3 = tk.Label(self.frame, text="Department", font=('times', 13, 'bold')).grid(row=2, column=0,sticky='e')

        frame2 = tk.LabelFrame(self.frame, text="Gender", font=('times', 13, 'bold'), padx=5, pady=5)
        frame2.grid(row=3, column=0, columnspan=3,sticky='ew')


    #entry filed
        self.fNameE = tk.Entry(self.frame, textvariable=tk.StringVar(), font=('times', 13, 'italic'), width=45, fg='blue')
        self.fNameE.grid(row=0, column=1)

        self.lNameE = tk.Entry(self.frame, textvariable=tk.StringVar(), font=('times', 13, 'italic'), width=45,fg='blue')
        self.lNameE.grid(row=1, column=1)

        self.departmentE = tk.Entry(self.frame, font=('times', 13, 'italic'), width=45, fg='blue')
        self.departmentE.grid(row=2, column=1)

        # variable to hold the selected of gender
        self.genderVariable = tk.StringVar(frame2, '1')
        options_gender = {"Male": "Male",
                          "Female": "Female", }
        for (text, option) in options_gender.items():
            tk.Radiobutton(frame2, text=text, variable=self.genderVariable, value=option,
                           font=('times', 13, 'italic')).pack(side="left", padx=67)

    #Security related label
        self.fram3 = tk.LabelFrame(self.frame, text="Personal private fields", padx=30, pady=30,font=('times', 15, 'italic'), fg='#9a1e1e')
        self.fram3.grid(row =4,column =0,columnspan = 2 )

     #labeled fields
        label11 = tk.Label(self.fram3, text="Email Address", font=('times', 13, 'bold')).grid(row=0, column=0,sticky='e')
        label22 = tk.Label(self.fram3, text="UserID", font=('times', 13, 'bold')).grid(row=1, column=0,sticky='e')
        label33 = tk.Label(self.fram3, text="Password", font=('times', 13, 'bold')).grid(row=3, column=0,sticky='e')
        label44 = tk.Label(self.fram3, text="Confirm", font=('times', 13, 'bold')).grid(row=4, column=0,sticky='e')

     #entry filed
        self.emailE = tk.Entry(self.fram3, textvariable=tk.StringVar(), font=('times', 13, 'italic'), width=45,fg='blue')
        self.emailE.grid(row=0, column=1)

        self.userIdE = tk.Entry(self.fram3, textvariable=tk.StringVar(), font=('times', 13, 'italic'), width=45,fg='blue')
        self.userIdE.grid(row=1, column=1)

        self.passwordE = tk.Entry(self.fram3,show="*", font=('times', 13, 'italic'), width=45, fg='blue')
        self.passwordE.grid(row=3, column=1)

        self.confirmE = tk.Entry(self.fram3,show="*", font=('times', 13, 'italic'), width=45, fg='blue')
        self.confirmE.grid(row=4, column=1)

     #private field validation with respect to the keypad
        reg = root.register(self.callback)

        self.userIdE.config(validate="key",validatecommand=(reg, '%P'))
        self.passwordE.config(validate="key",validatecommand=(reg, '%P'))
        self.confirmE.config(validate="key",validatecommand=(reg, '%P'))

    # button to take pictur
        self.buttonTakeCapture = tk.Button(self.frame, text=fr'Take pictures of {self.fNameE.get()}',
                                           font=('times', 13, 'italic'), fg='blue', width='20',
                                           bg="#88cffa",
                                           pady=5, command=self.takeCaptur).grid(row=6, column=0, pady=5, columnspan=2)

    # button to indicate user input error
        self.errorHint= tk.Label(self.fram3, text="", font=('times', 13, 'bold'),fg = 'red')
        self.errorHint.grid(row=22, column=0,columnspan = '2',sticky='ew')

    # button to initiate the training
        buttonTrain = tk.Button(self.frame, text="Train", font=('times', 13, 'bold italic'), fg='blue', width='50', bg="#88cffa",
                           pady=5,command =self.train).grid(row=9, column=0, columnspan=2,sticky='ew')


        root.mainloop()

    def takeCaptur(self):

        # to handle date and time of the registration
        today = datetime.now()
        registrationTime = today.strftime("%d/%m/%Y  %I:%M:%S")




        # employee's data validation and stor to db only-if it is valied
        if self.isEmployeeDataValid(self.fNameE.get(),self.lNameE.get(),self.userIdE.get(),self.passwordE.get(),self.confirmE.get()):
            # trainer is the person to be registerd

            trainer = [self.fNameE.get(), self.lNameE.get(), self.genderVariable.get(), self.departmentE.get(),
                       self.emailE.get(), self.userIdE.get(), self.passwordE.get(),
                       registrationTime]
            self.errorHint.config(fg = "green",text = "Processing over your the camera...")
            # create a database object and add the person to the
            db = Database()
            db.insertToEmployee(trainer)
            zisEmployId = db.getEmployeeId(self.fNameE.get(),self.lNameE.get())

            # capturing trainer pic and save
            headShoot = HeadShote(zisEmployId)
            headShoot.startHeadshot()
            self.errorHint.config(fg = "green",text = f"Done, {self.fNameE} {self.lNameE} is registered,you can add "
                                                      f"new employee,initiate the trainer after finishing  all of the "
                                                      f"new comer employees")


        print(' captur complet========================')

    def train(self):
        #train and encode
        trainer = Trainer()
        trainer.srartTrain()
        print('training finished ========================')

    def callback(sel,input):

        if input == "":
            print(input)
            return True
        else:
            last = str(input)[-1]
            if last.isdigit():
                print(input)
                return True
            elif last in str("ABCD"):
                print(input)
                return True
            else:
                print(input)
                return False

    def isEmployeeDataValid(self,fName,lName,userid,passwd,confirm):
        val = False
        db = Database()
        if str(fName).strip() == "":
            self.errorHint.config(text = "Employee name can't be empty!")
        elif db.isEmployeeExist(str(fName).strip(),str(lName).strip()):
            self.errorHint.config(text = f"{fName} {lName} is already registered")

        elif db.isUserIdToken(str(userid).strip()):
            self.errorHint.config(text = "User Id is token,Try another")
            val = False
        elif self.password_check(passwd):
            if confirm == passwd:
                val = True
            else:
                self.errorHint.config(text = "re-enter the password in confirm field")
                val = False

        return  val
    # method to validate password
    # with respect to the keypad
    def password_check(self,passwd):

        SpecialSym = ['A', 'B', 'C', 'D']
        val = True

        if len(passwd) < 4:
            self.errorHint.config(text = "Password length should be at least 4")
            val = False

        elif len(passwd) > 6:
            self.errorHint.config(text = "Password length length should be not be greater than 6")
            val = False

        elif not any(char.isdigit() for char in passwd):
            self.errorHint.config(text = "Password should have at least one numeral")
            val = False

        elif not any(char in SpecialSym for char in passwd):
            self.errorHint.config(text = "Password should have at least one of the the letter A B C or D")
            val = False

        if val:
            return val
