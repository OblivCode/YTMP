from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWebEngineWidgets import *
from PyQt6.QtWebEngineCore import *
from PyQt6.QtNetwork import *
import os


class WebEngine(QMainWindow):
    def __init__(self, screen_width, screen_height):
        super().__init__()
        self.setWindowTitle("YTM Presence")
        self.setGeometry(0, 0, int(screen_width * 0.75), int(screen_height * 0.75))
        self.base_url = f"https://music.youtube.com/"
        
        self.cookies_dir = '.\\cookies'
        self.cookies: list[QNetworkCookie] = []
        

        self.profile = QWebEngineProfile()
        self.LoadCookies()
        self.profile.setPersistentCookiesPolicy(QWebEngineProfile.PersistentCookiesPolicy.ForcePersistentCookies)
        self.profile.setHttpCacheType(QWebEngineProfile.HttpCacheType.DiskHttpCache)
        self.profile.setHttpUserAgent("Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0")
        self.profile.cookieStore().cookieAdded.connect(self.onCookieAdded)
        self.view = QWebEngineView()
        self.page = QWebEnginePage(self.profile, self.view)
        self.view.setPage(self.page)
        self.page.load(QUrl(self.base_url))
        

        self.setCentralWidget(self.view)

        self.timer = QTimer(self) 
        self.timer.timeout.connect(self.onTimerElapsed)
        self.timer.setSingleShot(False)
        self.timer.start(2 * 1000)
    
    #events
    def onCookieAdded(self, cookie: QNetworkCookie):
        self.cookies.append(cookie)

    def onTimerElapsed(self):
        self.ExecuteJSScraper()

    

    def onJSCallback(self, response):
        if response:
            self.callback(response)
                
    def closeEvent(self, e):
        self.ClearSavedCookies()
        self.SaveCookies()
    
    #js
    def AddCallback(self, function):
        self.callback = function

    def ExecuteJSScraper(self):
        with open('scrap.js', 'r') as f:
            script = f.read()
            f.close()
        self.page.runJavaScript(script, self.onJSCallback)
    #cookies
    def SaveCookies(self):
        num = len(os.listdir(self.cookies_dir))
        for cookie in self.cookies:
            print(cookie)
            filename = f"{self.cookies_dir}\\{num}"

            with open(filename + "name", 'wb') as f:
                f.write(cookie.name().data())
                f.close()
            with open(filename + "value", 'wb') as f:
                f.write(cookie.value().data())
                f.close()

            num = num + 1


    def LoadCookies(self):
        name = ""
        for file in os.listdir(self.cookies_dir):

            filename = self.cookies_dir + "\\" + file
            if name == "":
                with open(filename, 'rb') as f:
                    name = f.read()
                    f.close()
                continue
            
            with open(filename, 'rb') as f:
                value = f.read()
                f.close()
            
            cookie = QNetworkCookie(name, value)
            self.profile.cookieStore().setCookie(cookie, QUrl(self.base_url))
            name = ""

    def ClearSavedCookies(self):
        for file in os.listdir(self.cookies_dir):
            filename = self.cookies_dir + "\\" + file
            os.remove(filename)


        

