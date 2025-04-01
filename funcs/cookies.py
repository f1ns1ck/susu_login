import requests
from bs4 import BeautifulSoup
import os


class CookieGrab: 
    def __init__(self):
        self.login_data = { 
                           "logintoken": f"{self.GetLoginToken()}",
                           "username": os.getenv("USERNAME"), 
                           "password": os.getenv("PASSWORD"),
                          }
        

        self.url_login = "https://edu.susu.ru/login/index.php"
    
    # Получение logintoken для авторизации на сайт
    def GetLoginToken(self): 
        self.session = requests.Session()
        self.session.headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"}
        response = self.session.get("https://edu.susu.ru/login/index.php", stream=True)
        
        soup = BeautifulSoup(response.text, "lxml")
        
        data = soup.find(class_="login-form").find_all(name="input")
        
        return data[1]["value"]

    # Авторизация и возврат куки под формат playwright
    def Login(self):
        self.session.post(self.url_login, data=self.login_data)
        
        # Получение словаря куки
        cookies_dict = self.session.cookies.get_dict()
        cookies_list = []
        # заполнение куки
        for name, value in cookies_dict.items():
            cookies_list.append({
                "name": name,
                "value": value,
                "domain": "edu.susu.ru",  
                "path": "/",              
            })

        return cookies_list

 