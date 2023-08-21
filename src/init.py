from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from web import WebEngine
from presence import Update, Close
import sys

#runs whenever we get a response from scrap.js
def callback(response):
    page_url = None
    image_url = None
    buttons = None
    
    if response["ad"]:
        text = "Ad break"  
    else:
        song_name = response["song"]
        artist_name = response["artist"]
        album_name = response["album"]
        released_year = response["year"]
        time_stamp = response["time"]
        image_url = response["image"]
        page_url = response["url"]
        text1 = f"Listening to {song_name} by {artist_name} on {album_name} ({time_stamp})"
        text2 = f"Listening to {song_name} by {artist_name} ({time_stamp})"
        text = text2

        buttons = [
            {
                "label": "Project",
                "url": "https://github.com/OblivCode/YTMP"
            }, {
                "label": "Song link",
                "url": page_url
            }
        ]
    Update(text, image_url, buttons)
    

app = QApplication(sys.argv)

s =  app.primaryScreen().size()
screen_height = s.height()
screen_width = s.width()

win = WebEngine(screen_width, screen_height)
win.AddCallback(callback)
win.show()
app.exec()
#closing app
Close()
