from PyQt6.QtNetwork import QNetworkCookie
from PyQt6.QtWebEngineCore import QWebEngineProfile, QWebEngineCookieStore
from PyQt6.QtCore import QUrl
import os, threading

cookies: list[QNetworkCookie] = []
COOKIES_DIR = '.\\cookies'
if not os.path.exists(COOKIES_DIR):
    os.mkdir(COOKIES_DIR)

def AddCookie(cookie: QNetworkCookie):
    cookies.append(cookie)

def LoadWEProfile() -> QWebEngineProfile:
    profile = QWebEngineProfile()
    
    for file in os.listdir(COOKIES_DIR):
        filename = COOKIES_DIR + "\\" + file
        with open(filename, 'rb') as f:
            buffer = f.read()
            f.close()
            
        name_index_start = buffer.find(bytes("NAME", "utf8")) + 4
        name_index_end = buffer.find(bytes("VALUE", "utf8"))
        name = buffer[name_index_start:name_index_end]

        value_index_start = name_index_end + 5
        value_index_end = buffer.find(b"PATH")
        value = buffer[value_index_start:value_index_end]

        path_index_start = value_index_end + 4
        path = str(buffer[path_index_start:], "utf8")
        
        cookie = QNetworkCookie(name, value)
        profile.cookieStore().setCookie(cookie, QUrl(path))
        
    return profile

last_cookie_count = 0


def SaveCookies():
    if last_cookie_count < len(cookies):
        print(f"{len(cookies) - last_cookie_count} new cookies to save")

    print(f"{len(cookies)} total cookies")
    counter = 0
   
    for cookie in cookies:
        
        filename = f"{COOKIES_DIR}\\cookie{counter}"
        print(f"Writing to",filename)
        with open(filename, 'wb') as f:
            f.write(bytes("NAME", "utf8"))
            print(2)
            f.write(cookie.name().data())
            print(4)
            f.write(bytes("VALUE", "utf8"))
            print(3)
            f.write(cookie.value().data())
            f.write(bytes("PATH", "utf8"))
            f.write(bytes(cookie.path(), "utf8"))
            f.flush()
            f.close()
        counter += 1


def ClearSavedCookies():
    for file in os.listdir(COOKIES_DIR):
        filename = COOKIES_DIR + "\\" + file
        os.remove(filename)
