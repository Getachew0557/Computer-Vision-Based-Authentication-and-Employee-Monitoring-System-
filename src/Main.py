import tkinter as tk
from PIL import Image,ImageTk
from masterWin import MasterClass

class Main:
    def login(self):
        print("testing")
        window1 = tk.Tk()
        window1.title("AASTU -->Login window")

        # get height and wodth to make the frame full screen
        width = window1.winfo_screenwidth()
        height = window1.winfo_screenheight()
        window1.geometry("%dx%d" % (width, height))

        # bg = tk.PhotoImage(file="bg.png")
        img = (Image.open("bg.png"))
        resized_image = img.resize((width, height), Image.ANTIALIAS)
        bg = ImageTk.PhotoImage(resized_image)

        cavana = tk.Canvas(window1, width=width, height=height)
        cavana.pack(fill='both', expand=True)
        cavana.create_image(0, 0, image=bg, anchor='nw')
      #  cavana.create_text(200, 200, text="joojo")



        astuIcon = tk.PhotoImage(file=r"aastuIcon.png", height=500)

        # labelIcon = tk.Label(window1, image=astuIcon).pack()

        # labelTitle = tk.Label(window1, text="CV Based Authentication and Employee monitoring System", fg='blue',
        #                       font=('times', 30, 'bold'))
        # labelTitle.pack()
        # cavana.create_window(160+width/2, 100, window=labelTitle)

        frame = tk.LabelFrame(window1, fg='red', text="For only the admins", padx=20, pady=20,
                              font=('times', 15, 'bold'))
        frame.pack(padx=20, pady=20)
        cavana.create_window(width/1.5, height/1.3, window=frame)



        label1 = tk.Label(frame, text="UserName", font=('times', 10, 'bold')).grid(row=0, column=0)
        cavana.create_window(100, 100, window=label1)

        self.uname = tk.Entry(frame, text="UserName", font=('times', 10, 'bold'))
        self.uname.grid(row=0, column=1)
        # cavana.create_window(100, 100, window=self.uname)


        label2 = tk.Label(frame, text="password", font=('times', 10, 'bold')).grid(row=1, column=0)
        cavana.create_window(100, 100, window=label2)

        self.passkey = tk.Entry(frame, show="*", font=('times', 10, 'bold'))
        self.passkey.grid(row=1, column=1)
        # cavana.create_window(100, 100, window=self.passkey)


        def loginn():
            print('login_test')
            admins = {"Getachew":"gech_123",
                      "Yinebeb":"yina_123",
                      "Yosef":"jo_123"}
            
            if self.uname.get() in admins.keys() and self.passkey.get()in admins.values():
                master = MasterClass()
                window1.destroy()
                master.showMain()
            else:
                label3 = tk.Label(frame, text="user name or password incorrect", font=('times', 10, 'bold'),
                                  fg="red").grid(row=3, column=0, columnspan=2)

        button = tk.Button(frame, text="Login", font=('times', 10, 'bold'), padx=20, command=loginn).grid(row=2,column =0,columnspan =2)
        window1.mainloop()
system = Main()
system.login()
