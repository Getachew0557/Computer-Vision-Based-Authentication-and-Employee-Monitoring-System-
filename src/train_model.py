import threading

import os
import cv2
import numpy as np
from PIL import Image
import tkinter as tk
from tkinter import ttk


class Trainer:
    def __init__(self):
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.path = "Dataset"
        self.i = 0
        if not os.path.exists('./recognizer'):
            os.makedirs('./recognizer')


    def srartTrain(self):

        # our images are located in the dataset folder
        print("[INFO] start processing faces...")
        print("[INFO] processing image {} ,40".format(self.i + 1))


        Ids, faces = self.getImagesWithID(self.path)
        # update the progress variable value

        self.recognizer.train(faces, Ids)

        # self.variable.set(100 // len(Ids) * (self.i + 1))
        # self.i = self.i + 1
        # self.style.configure('text.Horizontal.TProgressbar',
        #                      text='{:g} %'.format(self.variable.get()))  # update label
        # self.root.update_idletasks()
        self.recognizer.save('recognizer/trainingData.yml')
        cv2.destroyAllWindows()
    def getImagesWithID(self,path):
        imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
        faces = []
        IDs = []
        for imagePath in imagePaths:
            faceImg = Image.open(imagePath).convert('L')
            faceNp = np.array(faceImg, 'uint8')
            ID = int(os.path.split(imagePath)[-1].split('.')[1])
            faces.append(faceNp)
            IDs.append(ID)
            cv2.imshow("training", faceNp)
            cv2.waitKey(10)
        return np.array(IDs), faces
    def start_trainning_thread(self, event):
        global encoding_thread
        encoding_thread = threading.Thread(target=self.srartTrain)
        encoding_thread.daemon = True
        encoding_thread.start()
        self.root.after(10, self.check_traninng_thread)

    def check_traninng_thread(self):

        if encoding_thread.is_alive():
            self.style.configure('text.Horizontal.TProgressbar',
                                 text='{:g} %'.format(self.variable.get()))  # update label
            self.root.update_idletasks()
            self.root.after(10, self.check_traninng_thread)
        else:
            self.variable.set(100)
            self.pbar.stop()
            self.style.configure('text.Horizontal.TProgressbar',
                                 text='{:g} %'.format(self.variable.get()))  # update label
            self.root.update_idletasks()
            # lable to indicate the compilation of the process
            label = tk.Label(self.root, text="Training completed", font=('serif', 15, 'bold italic'), fg='green').pack()

    def startprocess(self):

        self.root = tk.Tk()
        self.root.geometry('550x260')
        self.root.title('AASTU---> model training ...')
        labelTitle = tk.Label(self.root, text="Training The Model", fg='blue', font=('times', 20, 'bold'), bg="#88cffa",
                              pady=10, width=850)
        labelTitle.pack()
        warnLabel2 = tk.Label(self.root, text="Training the model may take a few seconds please waite...", fg='red',
                              font=('times', 16, 'italic'),
                              pady=10, width=850)
        warnLabel2.pack(pady=10)

        self.style = ttk.Style(self.root)
        # add label in the layout
        self.style.layout('text.Horizontal.TProgressbar',
                          [('Horizontal.Progressbar.trough',
                            {'children': [('Horizontal.Progressbar.pbar',
                                           {'side': 'left', 'sticky': 'ns'})],
                             'sticky': 'nswe'}),
                           ('Horizontal.Progressbar.label', {'sticky': 'nswe'})])
        # set initial text
        self.style.configure('text.Horizontal.TProgressbar', text='0 %', anchor='center')

        # mainframe = ttk.Frame(self.root, padding="3 3 12 12")
        # mainframe.pack()
        # mainframe.columnconfigure(0, weight=1)
        # mainframe.rowconfigure(0, weight=1)

        self.variable = tk.DoubleVar(self.root)
        self.pbar = ttk.Progressbar(self.root, style='text.Horizontal.TProgressbar', variable=self.variable, length=300)
        self.pbar.pack()

        tk.Button(self.root, text="Start Training",
                  font=('times', 13, 'italic'), fg='blue', width='12',
                  bg="#88cffa",
                  pady=5, command=lambda: self.start_trainning_thread(None)).pack(pady=10)
        # ttk.Button(self.root, text="Check",
        # 		   command=lambda: self.start_trainning_thread(None)).pack()
        for child in self.root.winfo_children():
            child.pack_propagate()
        self.root.bind('<Return>', self.start_trainning_thread)

        self.root.mainloop()

