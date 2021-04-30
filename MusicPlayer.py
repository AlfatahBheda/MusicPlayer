import os
import tkinter as tk
from tkinter import filedialog
from tkinter import PhotoImage
from pygame import mixer


class Player(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.root = root
        self.pack()
        mixer.init()

        self.songlist = []
        self.played = False
        self.paused = True
        self.current = 0

        self.create_frames()
        self.track_elements()
        self.playlist_elements()
        self.control_elements()

    def create_frames(self, background="grey"):
        self.track = tk.LabelFrame(self, text="Music Player", font=("calibri", 25, "bold"),
                                   bg=background, fg="white", bd=5, relief=tk.GROOVE)
        self.track.configure(width=400, height=400)
        self.track.grid(row=0, column=0, pady=10, padx=10)

        self.playlist = tk.LabelFrame(self, text=f"Total Songs : {str(len(self.songlist))}",
                                      font=("calibri", 25, "bold"),
                                      bg=background, fg="white", bd=5, relief=tk.GROOVE)
        self.playlist.configure(width=300, height=500)
        self.playlist.grid(row=0, column=1, rowspan=3, pady=10)

        self.control = tk.LabelFrame(self, font=("calibri", 25, "bold"),
                                     bg=background, fg="white", bd=5, relief=tk.GROOVE)
        self.control.configure(width=400, height=100)
        self.control.grid(row=1, column=0)

    def track_elements(self):
        self.canvas = tk.Label(self.track, image=music)
        self.canvas.configure(width=390, height=300)
        self.canvas.grid(row=0, column=0)

        self.current_track = tk.Label(self.track, font=("calibri", 25, "bold"),
                                      bg="white", fg="black", )
        self.current_track['text'] = "Onyx - Music Player"
        self.current_track.grid(row=1, column=0)

    def playlist_elements(self):
        self.scrollbar = tk.Scrollbar(self.playlist, orient=tk.VERTICAL)
        self.scrollbar.grid(row=0, column=1, sticky="ns")

        self.list = tk.Listbox(self.playlist, selectmode=tk.SINGLE,
                               yscrollcommand=self.scrollbar.set, selectbackground="sky blue")
        self.enumerate_playlist()
        self.list.configure(height=28, width=30)
        self.list.bind('<Double-1>', self.play_song)
        self.scrollbar.configure(command=self.list.yview)
        self.list.grid(row=0, column=0)

    def control_elements(self):
        self.getsongs = tk.Button(self.control, bg="blue", fg="white", font=("calibri", 15))
        self.getsongs['text'] = "Open Songs"
        self.getsongs['command'] = self.retrieve_songs
        self.getsongs.grid(row=0, column=0, pady=20, padx=10)

        self.rev = tk.Button(self.control, image=reverse)
        self.rev['command'] = self.rev_song
        self.rev.grid(row=0, column=1)

        self.pauseb = tk.Button(self.control, image=pause)
        self.pauseb['command'] = self.pause_song
        self.pauseb.grid(row=0, column=2)

        self.forw = tk.Button(self.control, image=forward)
        self.forw['command'] = self.forw_song
        self.forw.grid(row=0, column=3)

        self.volume = tk.DoubleVar()
        self.slider = tk.Scale(self.control, from_=0, to=100, orient=tk.HORIZONTAL)
        self.slider['variable'] = self.volume
        self.slider['command'] = self.adjust_volume
        self.slider.set(50)
        mixer.music.set_volume(0.5)
        self.slider.grid(row=0, column=4, padx=10)

    def enumerate_playlist(self):
        for i, song in enumerate(self.songlist):
            self.list.insert(i, os.path.basename(song))

    def retrieve_songs(self):
        self.list_songs = []
        directory = filedialog.askdirectory()
        for root_, dirs, files in os.walk(directory):
            for file in files:
                if os.path.splitext(file)[1] == ".mp3":
                    path = (root_ + "/" + file).replace("\\", "/")
                    self.list_songs.append(path)
        self.songlist = self.list_songs
        self.list.delete(0, tk.END)
        self.playlist['text'] = f"Total Songs : {str(len(self.songlist))}"
        self.enumerate_playlist()

    def play_song(self, event=None):
        if event is not None:
            self.current = self.list.curselection()[0]
            for i in range(len(self.songlist)):
                self.list.itemconfigure(i, bg="white")
        mixer.music.load(self.songlist[self.current])
        self.pauseb['image'] = play
        self.played = True
        self.current_track['text'] = os.path.basename(self.songlist[self.current])
        self.current_track['anchor'] = 'w'
        self.list.itemconfigure(self.current, bg="sky blue")
        mixer.music.play()

    def rev_song(self):
        if self.current > 0:
            self.current -= 1
        else:
            self.current = 0
            self.play_song()
        self.list.itemconfigure(self.current + 1, bg="white")
        self.play_song()

    def pause_song(self):
        if self.played:
            self.played = False
            mixer.music.pause()
            self.pauseb['image'] = pause
        else:
            if self.paused:
                self.paused = False
                self.play_song()
            self.played = True
            mixer.music.unpause()
            self.pauseb['image'] = play

    def forw_song(self):
        if self.current < len(self.songlist) - 1:
            self.current += 1
        else:
            self.current = len(self.songlist) - 1
            self.play_song()
        self.list.itemconfigure(self.current - 1, bg="white")
        self.play_song()

    def adjust_volume(self, event=None):
        self.vol = self.volume.get()
        mixer.music.set_volume(self.vol / 100)


window = tk.Tk()
window.geometry("700x550")
window.wm_title("Onyx - Music Player")

music = PhotoImage(file="images/music.gif")
forward = PhotoImage(file="images/forward.png")
reverse = PhotoImage(file="images/reverse.png")
pause = PhotoImage(file="images/pause.png")
play = PhotoImage(file="images/play.png")

musicplayer = Player(root=window)
musicplayer.mainloop()
