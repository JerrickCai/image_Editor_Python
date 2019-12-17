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
        self.root.geometry('800x900')
        self.root.configure(background='grey')
        self.canvas = Canvas(width=800, height=800, bg='white')
        self.canvas.pack()

        filename='1.jpg'
        image = Image.open(filename)
        self.photo = ImageTk.PhotoImage(image)
        self.img = self.canvas.create_image(250, 250, image=self.photo)

        self.text = StringVar()
        # create frame to put control buttons onto
        self.frame = Frame(self.root, bg='grey', width=800, height=100)
        self.frame.pack(fill='x')

        # create label, which shows status
        self.statusLabel = Label(self.frame, textvariable=self.text)
        self.statusLabel.pack(side='left', padx=10)

        # create import image button
        self.importImageButton = Button(self.frame , text="import image", command=self.importImg)
        self.importImageButton.pack(side='left')

        self.root.mainloop()
        self.root.destroy()

    def importImg(self):
        path = filedialog.askopenfilename()
        img = cv2.imread(path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.photo = ImageTk.PhotoImage(image=Image.fromarray(img))
        self.canvas.itemconfig(self.img, image=self.photo)
        self.text.set('imported')

if __name__ == "__main__":
    gui = myGUI()

# img = cv2.imread('Scan 1.jpeg')
# # cv2.imshow('src',img)
# gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
# img4 = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
# cv2.imshow('src',gray)
# print(img.shape)
# print(img.size) # 像素总数目
# print(img.dtype)
# print(img)
#
# cv2.waitKey()