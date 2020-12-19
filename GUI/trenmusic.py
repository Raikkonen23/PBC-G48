import tkinter as tk
import tkinter.font as tkFont
from PIL import ImageTk, Image

class TrenMusic(tk.Frame):
  
  def __init__(self):
    tk.Frame.__init__(self) 
    self.grid()
    self.createWidgets()

  def createWidgets(self):
    self.imagecanvas = ImageTk.PhotoImage(file = "tmlabel.png")
    self.imagebutton1 = ImageTk.PhotoImage(file = "button2.png")
    mycolor = '#%02x%02x%02x' % (255, 87, 87)
    f1 = tkFont.Font(size = 48, family = "Gill Sans Ultra Bold Condensed")
    f2 = tkFont.Font(size = 32, family = "Courier New")
    self.button = tk.Button(self, image = self.imagebutton1)
    self.lbl1 = tk.Label(self, bg = mycolor)
    #self.lbl2 = tk.Label(self, bg = mycolor)
    self.lblNum = tk.Label(self, image = self.imagecanvas)    
    self.lblNum.grid(row = 0, column = 0, columnspan = 3)
    self.button.grid(row = 1, column = 0)
    #self.lbl1.grid(row = 1, column = 0 , sticky = tk.NE + tk.SW)
    #self.lbl2.grid(row = 1, column = 2)

cal = TrenMusic()
cal.master.title("TrenMusic")
cal.mainloop()