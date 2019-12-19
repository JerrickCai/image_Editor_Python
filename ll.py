from tkinter import filedialog
import numpy as np
from tkinter import *
from PIL import Image, ImageTk, ImageEnhance

class myGUI(object):
    def __init__(self):
        # create a window
        self.root = Tk()
        self.root.title('image editor')
        self.root.resizable(width=False, height=False)

        self.canvasW = 800
        self.canvasH = 800
        # self.root.configure(background='grey')
        self.canvas = Canvas(width=self.canvasW, height=self.canvasH, bg='gray')
        self.canvas.pack(fill='both', expand='no')

        #default parameters
        self.zoomScale = 1

        #setting default imgae
        path = 'default.jpg'
        self.originImg = Image.open(path)#origin image keeps the origin size and image information
        self.modifiedOriginImg = self.originImg #for saving file
        self.checkSize(self.originImg)#img is the resized image
        self.photo = ImageTk.PhotoImage(image=self.displayedImg)
        self.canvasImg = self.canvas.create_image(self.canvasH/2, self.canvasW/2, anchor='center', image=self.photo)

        self.text = StringVar()
        # create frame to put control buttons onto
        self.frameBottom = Frame(self.root, width=800, height=50)
        self.frameBottom.pack(fill='both', expand='yes')

        # create frame to put scales
        self.frameScales = Frame(self.root, width=800, height=50)
        self.frameScales.pack(fill='both', expand='yes')

        # create frame to put status bar onto
        self.frameStatus = Frame(self.root, width=800, height=50)
        self.frameStatus.pack(fill='both', expand='yes')

        # create label, which shows status
        self.statusLabel = Label(self.frameStatus, textvariable=self.text, bd = 1,relief = SUNKEN, anchor = W)
        self.statusLabel.pack(side=BOTTOM, fill = X)

        # create import image button
        self.importImageButton = Button(self.frameBottom , text="import image", command=self.importImg)
        self.importImageButton.pack(side='left', padx=10)

        # create save image button
        self.exportImageButton = Button(self.frameBottom, text="save as", command=self.exportImg)
        self.exportImageButton.pack(side='left', padx=10)

        # create zoom in button
        self.zoomInButton = Button(self.frameBottom, text="zoom in", command=lambda:self.zoom(0.1))
        self.zoomInButton.pack(side='left', padx=10)

        # create zoom out button
        self.zoomOutButton = Button(self.frameBottom, text="zoom out", command=lambda:self.zoom(-0.1))
        self.zoomOutButton.pack(side='left', padx=10)

        # create reset button
        self.resetButton = Button(self.frameBottom, text="reset", command=self.reset)
        self.resetButton.pack(side='left', padx=10)

        # create flip Horizontally button
        self.flipHButton = Button(self.frameBottom, text="flipH", command=lambda:self.flip(0))
        self.flipHButton.pack(side='left', padx=10)

        # create flip vertically button
        self.flipVButton = Button(self.frameBottom, text="flipV", command=lambda:self.flip(1))
        self.flipVButton.pack(side='left', padx=10)

        # create rotation button
        self.rotationButton = Button(self.frameBottom, text="rotate", command=self.rotation)
        self.rotationButton.pack(side='left', padx=10)

        # create scale of brightness
        self.brightnessScale = Scale(self.frameScales, label='Brightness', from_=0, to=2, orient=HORIZONTAL,
                     length=200, showvalue=1, tickinterval=0.3, resolution=0.1, command=self.brightnessSetScale)
        self.brightnessScale.pack(side='left', padx=10)

        # create brightness button
        self.brightnessButton = Button(self.frameScales, text=" adjust Brightness", command=self.brightnessSelection)
        self.brightnessButton.pack(side='left', padx=10)

        self.root.mainloop()

    # set image to canvas
    def setImg(self):
        self.photo = ImageTk.PhotoImage(image=self.displayedImg)
        self.canvas.itemconfig(self.canvasImg, image=self.photo)

    #read image from disk
    def importImg(self):
        path = filedialog.askopenfilename()
        self.originImg = Image.open(path)
        self.checkSize(self.originImg)
        self.setImg()
        self.displayedImgOrigin = self.displayedImg
        self.modifiedOriginImg = self.originImg
        self.reset()
        self.text.set('imported')

    # save image to disk
    def exportImg(self):
        path = filedialog.asksaveasfilename()
        self.modifiedOriginImg.save(path)
        self.text.set('saved')

    # zoom in and zoom out
    def zoom(self, step):
        self.zoomScale += step #ositive step is zoom in, O.W. zoom out
        h, w = self.displayedImgOrigin.size
        self.displayedImg = self.displayedImgOrigin.resize( (int(w*self.zoomScale), int(h*self.zoomScale)))
        self.setImg()
        self.text.set('zoomed in')

    # flip Horizontally and flip Vertically
    def flip(self, direction):
        if direction == 0:
            self.modifiedOriginImg = self.modifiedOriginImg.transpose(Image.FLIP_LEFT_RIGHT)#direction=0 is H, 1 is Vertically
            self.displayedImgOrigin = self.displayedImgOrigin.transpose(Image.FLIP_LEFT_RIGHT)
        else:
            self.modifiedOriginImg = self.modifiedOriginImg.transpose(
                Image.FLIP_TOP_BOTTOM)
            self.displayedImgOrigin = self.displayedImgOrigin.transpose(Image.FLIP_TOP_BOTTOM)
        self.zoom(0)
        self.text.set('flipped')

    # rotation
    def rotation(self):
        self.modifiedOriginImg = self.modifiedOriginImg.transpose(Image.ROTATE_90)

        self.displayedImgOrigin = self.displayedImgOrigin.transpose(Image.ROTATE_90)
        self.zoom(0)
        self.text.set('rotated')

    #set brightness scale
    def brightnessSetScale(self, scale):
        self.scale = scale

    #brightness
    def brightnessSelection(self):
        # image brightness enhancer
        enhancer = ImageEnhance.Brightness(self.modifiedOriginImg)
        factor = float(self.scale)  # darkens the image
        self.modifiedOriginImg = enhancer.enhance(factor)

        enhancer = ImageEnhance.Brightness(self.displayedImgOrigin)
        factor = float(self.scale)  # darkens the image
        self.displayedImgOrigin = enhancer.enhance(factor)

        self.zoom(0)
        self.text.set('has set brightness')

    # reset
    def reset(self):
        #parameter back to default
        self.zoomScale = 1

        # image back to default
        self.modifiedOriginImg = self.originImg

        #reset displayed image
        self.checkSize(self.originImg)
        self.setImg()

        self.text.set('has reset')

    #resize image according the ratio of image
    def checkSize(self, img):
        h, w = img.size
        ratio1 = h/w
        ratio2 = w/h
        self.root.update()
        canvasWidth = self.canvas.winfo_width()
        canvasHeight = self.canvas.winfo_height()
        if h>w:
            self.displayedImg = img.resize((int(canvasHeight*ratio2), canvasHeight))
        else:
            self.displayedImg = img.resize((canvasWidth, int(canvasWidth*ratio1)))
        self.displayedImgOrigin = self.displayedImg #make a copy of the very first resized to window sized image, to keep a clear and sharp preview image
        h, w = self.displayedImgOrigin.size
        self.displayedImg = self.displayedImgOrigin.resize((int(w * self.zoomScale), int(h * self.zoomScale)))

if __name__ == "__main__":
    gui = myGUI()
