import threading

from imutils import paths
# import face_recognition
import pickle
import cv2
import os
import tkinter as tk
from tkinter import ttk


class Trainer:
    def srartTrain(self):

        # our images are located in the dataset folder
        print("[INFO] start processing faces...")
        imagePaths = list(paths.list_images("dataset"))
        # initialize the list of known encodings and known names
        knownEncodings = []
        knownNames = []

        for (i, imagePath) in enumerate(imagePaths):
            # extract the person name from the image path
            print("[INFO] processing image {}/{}".format(i + 1, len(imagePaths)))

            # update the progress variable value
            self.variable.set(100 // len(imagePaths) * (i + 1))
            self.style.configure('text.Horizontal.TProgressbar',
                                 text='{:g} %'.format(self.variable.get()))  # update label
            self.root.update_idletasks()
            name = imagePath.split(os.path.sep)[-2]

            # load the input image and convert it from RGB (OpenCV ordering)
            # to dlib ordering (RGB)
            image = cv2.imread(imagePath)
            rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            # detect the (x, y)-coordinates of the bounding boxes
            # corresponding to each face in the input image
            boxes = face_recognition.face_locations(rgb, model="hog")

            # compute the facial embedding for the face
            encodings = face_recognition.face_encodings(rgb, boxes)

            # loop over the encodings
            for encoding in encodings:
                # add each encoding + name to our set of known names and
                # encodings
                knownEncodings.append(encoding)
                knownNames.append(name)

        # dump the facial encodings + names to disk
        print("[INFO] serializing encodings...")
        data = {"encodings": knownEncodings, "names": knownNames}
        f = open("encodings.pickle", "wb")
        f.write(pickle.dumps(data))
        f.close()

    def start_encoding_thread(self, event):
        global encoding_thread
        encoding_thread = threading.Thread(target=self.srartTrain)
        encoding_thread.daemon = True
        encoding_thread.start()
        self.root.after(10, self.check_encoding_thread)

    def check_encoding_thread(self):

        if encoding_thread.is_alive():
            self.style.configure('text.Horizontal.TProgressbar',
                                 text='{:g} %'.format(self.variable.get()))  # update label
            self.root.update_idletasks()
            self.root.after(10, self.check_encoding_thread)
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
                  pady=5, command=lambda: self.start_encoding_thread(None)).pack(pady=10)
        # ttk.Button(self.root, text="Check",
        # 		   command=lambda: self.start_encoding_thread(None)).pack()
        for child in self.root.winfo_children():
            child.pack_propagate()
        self.root.bind('<Return>', self.start_encoding_thread)

        self.root.mainloop()
