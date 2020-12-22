import tkinter as tk
import tkinter.font as tkFont
from PIL import ImageTk, Image

class TranMusic(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        self.grid()
        self.createWidgets()

    def createWidgets(self):
        background_image = tk.PhotoImage(file="intro.png")
        background_label = tk.Label(self, image=background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        mycolor = 'white'
        self.imagebutton1 = ImageTk.PhotoImage(file = "button2.png")
        f1 = tkFont.Font(size = 48, family = "Gill Sans Ultra Bold Condensed")
        f2 = tkFont.Font(size = 32, family = "Courier New")
        self.button = tk.Button(self, image = self.imagebutton1)
        self.lbl1 = tk.Label(self, bg = mycolor)
        self.lbl2 = tk.Label(self, bg = mycolor)
        # self.lblNum = tk.Label(self, image = self.imagecanvas)
        # self.lblNum.grid(row = 0, column = 0, columnspan = 3)
        self.button.grid(row = 1, column = 0)
        #self.lbl1.grid(row = 1, column = 0 , sticky = tk.NE + tk.SW)
        #self.lbl2.grid(row = 1, column = 2)

cal = TranMusic()
cal.master.title("TranMusic")
cal.mainloop()