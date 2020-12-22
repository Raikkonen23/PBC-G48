import tkinter as tk
import tkinter.font as tkfont
from PIL import ImageTk, Image
import webbrowser



SPOTIFY_ID = -1
SPOTIFY_TOKEN = -1
YOUTUBE_URL = -1

class App(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self, className='TranMusic')


        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        self.geometry('400x500')
        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self, height=500, width=400)

        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, PageOne, PageTwo):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.background_image = tk.PhotoImage(file='intro.png')

        self.background_label = tk.Label(self, image=self.background_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # label = tk.Label(self, text="This is the start page", font=controller.title_font)
        # label.pack(side="top", fill="x", pady=10)
        self.button_image = tk.PhotoImage(file='play button.png')
        button1 = tk.Button(self, command=lambda: controller.show_frame("PageOne")
                            , image=self.button_image, height=103, width=103)
        button1.place(x=145, y=330)



class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.background_image = tk.PhotoImage(file='spotify.png')
        self.background_label = tk.Label(self, image=self.background_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
        def OpenUrl1():
            webbrowser.open("https://www.spotify.com/us/account/overview/", new=1)
        def OpenUrl2():
            webbrowser.open("https://developer.spotify.com/console/post-playlists/", new=1)
        self.get_id_button = tk.PhotoImage(file='get_id.png')
        self.get_token_button = tk.PhotoImage(file='get_token.png')
        self.confirm_button = tk.PhotoImage(file='confirm.png')
        get_id_button = tk.Button(self, image=self.get_id_button, height=28, width=131, command=OpenUrl1)
        get_id_button.place(x=60, y=120)
        get_token_button = tk.Button(self, image=self.get_token_button, height=28, width=122, command=OpenUrl2)
        get_token_button.place(x=220, y=120)
        confirm_button = tk.Button(self, image=self.confirm_button
                                   , command=lambda: [controller.show_frame("PageTwo"), self.p1_entry()])
        confirm_button.place(x=300, y=220)

        id = tk.StringVar()
        token = tk.StringVar()
        self.entry_id = tk.Entry(self, width=25, textvariable=id)
        self.entry_token = tk.Entry(self, width=25, textvariable=token)
        self.entry_id.place(x=170, y= 170)
        self.entry_token.place(x=170, y=195)

    def p1_entry(self):
        global SPOTIFY_ID
        global SPOTIFY_TOKEN
        SPOTIFY_ID = self.entry_id.get()
        SPOTIFY_TOKEN =self.entry_token.get()



class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.background_image = tk.PhotoImage(file='youtube.png')
        self.background_label = tk.Label(self, image=self.background_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.tran_button = tk.PhotoImage(file='start_tran.png')
        tran_button = tk.Button(self, image=self.tran_button
                                , command=lambda: self.p2_entry())
        tran_button.place(x=160, y=220)

        YT_url = tk.StringVar()
        self.entry_YT_url = tk.Entry(self, width=40, textvariable=YT_url)
        self.entry_YT_url.place(x=50, y=170)

    def p2_entry(self):
        global YOUTUBE_URL
        YOUTUBE_URL = self.entry_YT_url.get()
        print(SPOTIFY_ID, SPOTIFY_TOKEN, YOUTUBE_URL)




if __name__ == "__main__":
    app = App()
    app.mainloop()