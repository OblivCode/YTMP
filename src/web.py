from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWebEngineWidgets import *
from PyQt6.QtWebEngineCore import *
from PyQt6.QtNetwork import *

CACHE_DIR = './cache'
STORAGE_DIR = './storage'

class WebEngine(QMainWindow):
    def __init__(self, screen_width, screen_height):
        super().__init__()
        self.setWindowTitle("YTM Presence")
        self.setGeometry(0, 0, int(screen_width * 0.75), int(screen_height * 0.75))
        self.base_url = f"https://music.youtube.com/"
        
        

        self.profile = QWebEngineProfile()
        self.profile.setPersistentCookiesPolicy(QWebEngineProfile.PersistentCookiesPolicy.ForcePersistentCookies)
        
        self.profile.setPersistentStoragePath(STORAGE_DIR)
        self.profile.setCachePath(CACHE_DIR)
        self.profile.setHttpCacheType(QWebEngineProfile.HttpCacheType.DiskHttpCache)
        self.profile.setHttpUserAgent("Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0")
        
        self.view = QWebEngineView()
        self.page = QWebEnginePage(self.profile, self.view)
        self.view.setPage(self.page)
        self.page.load(QUrl(self.base_url))
        self.setCentralWidget(self.view)
        self.page.event = self.onEvent

        self.timer = QTimer(self) 
        self.timer.timeout.connect(self.onTimerElapsed)
        self.timer.setSingleShot(False)
        self.timer.start(2 * 1000)


    def onTimerElapsed(self):
        self.ExecuteJSScraper()

    def AddCallback(self, function):
        self.callback = function

    def ExecuteJSScraper(self):
        with open('scrap.js', 'r') as f:
            script = f.read()
            f.close()
        self.page.runJavaScript(script, self.onJSCallback)
    def onJSCallback(self, response):
        if response:
            self.callback(response)
                
    def closeEvent(self, e):
        print('CLOSE')
        c = self.page.profile().cookieStore().children()
        self.FlushCookies()
        print("cookies", len(c))
        for i in c:
            print(i)
            print(type(i))

    def onEvent(self, e):
        self.FlushCookies()
        return True
    def FlushCookies(self):
        cookie = QNetworkCookie()
        self.page.profile().cookieStore().deleteCookie(cookie)
        

