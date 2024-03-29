from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWebEngineWidgets import *
from PyQt6.QtWebEngineCore import *
from PyQt6.QtNetwork import *
from cookiesaver import LoadWEProfile, SaveCookies, ClearSavedCookies, AddCookie
import os


class WebEngine(QMainWindow):
    def __init__(self, screen_width, screen_height):
        super().__init__()
        self.setWindowTitle("YTM Presence")
        self.setGeometry(0, 0, int(screen_width * 0.75), int(screen_height * 0.75))
        self.base_url = f"https://music.youtube.com/"
        
        print("Loading profile")
        self.profile = LoadWEProfile()
        self.profile.setPersistentCookiesPolicy(QWebEngineProfile.PersistentCookiesPolicy.ForcePersistentCookies)
        self.profile.setHttpCacheType(QWebEngineProfile.HttpCacheType.DiskHttpCache)
        self.profile.setHttpUserAgent("Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0")
        self.profile.cookieStore().cookieAdded.connect(self.onCookieAdded)

        print("Loading WebEngine")
        self.view = QWebEngineView()
        self.page = QWebEnginePage(self.profile, self.view)
        self.view.setPage(self.page)
        self.page.load(QUrl(self.base_url))
        self.setCentralWidget(self.view)
        print("Loading Timer")
        self.timer = QTimer(self) 
        self.timer.timeout.connect(self.onTimerElapsed)
        self.timer.setSingleShot(False)
        self.timer.start(5 * 1000)
    
    #events
    def onCookieAdded(self, cookie: QNetworkCookie):
        AddCookie(cookie)

    def onTimerElapsed(self):
        
        self.ExecuteJSScraper()

    def onJSCallback(self, response):
        if response:
            self.callback(response)
                
    def closeEvent(self, e):
        ClearSavedCookies()
        SaveCookies()
    
    #js
    def AddCallback(self, function):
        self.callback = function

    def ExecuteJSScraper(self):
        with open('scrap.js', 'r') as f:
            script = f.read()
            f.close()
        self.page.runJavaScript(script, self.onJSCallback)
   


        
