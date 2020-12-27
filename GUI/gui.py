import tkinter as tk
import tkinter.font as tkfont
from PIL import ImageTk, Image
import webbrowser
import create_playlist_withURL
import os

# 接input的變數，設成global
SPOTIFY_ID = -1
SPOTIFY_TOKEN = -1
YOUTUBE_ID = -1


class App(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self, className='TranMusic')
        self.geometry('400x500')

        # 裝frames的東西(一頁是一個frame)
        container = tk.Frame(self, height=500, width=400)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, PageOne, PageTwo):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # 所有的frame都放在同一個地方
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    # 顯示各個frame的方法: 把要叫出來的frame拉到最前面
    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        # 背景圖片放在最下層
        self.background_image = tk.PhotoImage(file='intro.png')
        self.background_label = tk.Label(self, image=self.background_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.button_image = tk.PhotoImage(file='play button.png')
        # '開始轉換按鈕'
        button1 = tk.Button(self,
                            command=lambda: controller.show_frame("PageOne")
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
            webbrowser.open("https://www.spotify.com/us/account/overview/",
                            new=1)

        def OpenUrl2():
            webbrowser.open(
                "https://developer.spotify.com/console/post-playlists/", new=1)

        # '取得Spotify id','取得Spotify token'按鈕，打開會連到Spotify網頁
        self.get_id_button = tk.PhotoImage(file='get_id.png')
        self.get_token_button = tk.PhotoImage(file='get_token.png')
        self.confirm_button = tk.PhotoImage(file='confirm.png')
        get_id_button = tk.Button(self, image=self.get_id_button, height=28,
                                  width=131, command=OpenUrl1)
        get_id_button.place(x=60, y=120)
        get_token_button = tk.Button(self, image=self.get_token_button,
                                     height=28, width=122, command=OpenUrl2)
        get_token_button.place(x=220, y=120)

        ''''確認'按鈕, 按下之後會跳到下一頁，然後在p1_entry()改變
        SPOTIFY_ID, SPOTIFY_TOKEN兩個變數'''
        confirm_button = tk.Button(self, image=self.confirm_button
                                   , command=lambda: [
                controller.show_frame("PageTwo"), self.p1_entry()])
        confirm_button.place(x=300, y=220)

        # Spotify輸入框
        id = tk.StringVar()
        token = tk.StringVar()
        self.entry_id = tk.Entry(self, width=25, textvariable=id)
        self.entry_token = tk.Entry(self, width=25, textvariable=token)
        self.entry_id.place(x=170, y=170)
        self.entry_token.place(x=170, y=195)

    def p1_entry(self):
        global SPOTIFY_ID
        global SPOTIFY_TOKEN
        SPOTIFY_ID = self.entry_id.get().strip('\n ')
        SPOTIFY_TOKEN = self.entry_token.get().strip('\n ')


class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.background_image = tk.PhotoImage(file='youtube.png')
        self.background_label = tk.Label(self, image=self.background_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # '開始轉換'按鈕，按下之後會透過p2_entry啟動主程式，主程式跑完會顯示'轉換成功'label
        self.tran_button = tk.PhotoImage(file='start_tran.png')
        tran_button = tk.Button(self, image=self.tran_button
                                , command=lambda: self.p2_entry())
        tran_button.place(x=160, y=220)

        YT_url = tk.StringVar()
        self.entry_YT_url = tk.Entry(self, width=40, textvariable=YT_url)
        self.entry_YT_url.place(x=50, y=170)

    def p2_entry(self):
        '''
        self.transform_png = tk.PhotoImage(file='transforming.png')
        self.transform_label = tk.Label(self, image=self.transform_png)
        self.transform_label.place(x=150, y=270)'''

        global YOUTUBE_ID

        # 從yt網址取出播放清單id，存進YOUTUBE_ID裡
        full_yt_url = self.entry_YT_url.get().strip('\n ')
        for_getting_id = full_yt_url.split('&')
        for i in for_getting_id:
            possible_id = i.split('=')
            if possible_id[0][
               len(possible_id[0]) - 4:len(possible_id[0])] == 'list':
                YOUTUBE_ID = possible_id[1]
                print('id get!')
        # print(SPOTIFY_ID, SPOTIFY_TOKEN, YOUTUBE_ID)

        '''
        with open('all_secrets.txt', 'w') as in_put:
            in_put.write(SPOTIFY_ID + '\n')
            in_put.write(SPOTIFY_TOKEN + '\n')
            in_put.write(YOUTUBE_ID + '\n')
            in_put.close()'''

        playlist_id = YOUTUBE_ID
        spotify_id = SPOTIFY_ID
        spotify_token = SPOTIFY_TOKEN

        # 主程式
        cp = create_playlist_withURL.CreatePlaylist(spotify_id, spotify_token,
                                                    playlist_id)
        cp.add_song_to_playlist()
        print("OK!")

        # os.system('create_playlist_withURL.py')

        self.transform_done_png = tk.PhotoImage(file='transformed.png')
        self.transform_done_label = tk.Label(self,
                                             image=self.transform_done_png)
        self.transform_done_label.place(x=95, y=270)


if __name__ == "__main__":
    app = App()
    app.mainloop()
