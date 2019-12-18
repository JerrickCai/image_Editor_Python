from tkinter import filedialog
import cv2
import numpy as np
from tkinter import *
from PIL import Image, ImageTk

class myGUI(object):
    def __init__(self):
        # create a window
        self.root = Tk()
        self.root.title('image editor')
        self.root.resizable(width=False, height=False)

        canvasW = 800
        canvasH = 800
        # self.root.configure(background='grey')
        self.canvas = Canvas(width=canvasW, height=canvasH, bg='gray')
        self.canvas.pack(fill='both', expand='yes')

        path = 'default.jpg'
        img = cv2.imread(path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        print(img.shape)
        img = self.checkSize(img)
        print(img.shape)
        self.photo = ImageTk.PhotoImage(image=Image.fromarray(img))
        self.img = self.canvas.create_image(canvasH/2, canvasW/2, anchor='center', image=self.photo)

        self.text = StringVar()
        # create frame to put control buttons onto
        self.frameBottom = Frame(self.root, width=800, height=50)
        self.frameBottom.pack(fill='both', expand='yes')

        # create frame to put status bar onto
        self.frameStatus = Frame(self.root, width=800, height=50)
        self.frameStatus.pack(fill='both', expand='yes')

        # create label, which shows status
        self.statusLabel = Label(self.frameStatus, textvariable=self.text, bd = 1,relief = SUNKEN, anchor = W)
        self.statusLabel.pack(side=BOTTOM, fill = X)

        # create import image button
        self.importImageButton = Button(self.frameBottom , text="import image", command=self.importImg)
        self.importImageButton.pack(side='left', padx=10)

        self.root.mainloop()
        # self.root.destroy()

    def importImg(self):
        path = filedialog.askopenfilename()
        img = cv2.imread(path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = self.checkSize(img)
        self.photo = ImageTk.PhotoImage(image=Image.fromarray(img))
        self.canvas.itemconfig(self.img, image=self.photo)
        self.text.set('imported')

    def checkSize(self,img):
        h, w = img.shape[:2]
        ratio1 = h/w
        ratio2 = w/h
        self.root.update()
        canvasWidth = self.canvas.winfo_width()
        canvasHeight = self.canvas.winfo_height()
        if h>w:
            img = cv2.resize(img, (int(canvasHeight*ratio2), canvasHeight))
        else:
            img = cv2.resize(img, (canvasWidth, int(canvasWidth*ratio1)))
        return img

if __name__ == "__main__":
    gui = myGUI()
