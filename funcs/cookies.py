import requests
from bs4 import BeautifulSoup
import os


class CookieGrab: 
    def __init__(self):
        self.url_login = "https://edu.susu.ru/login/index.php"

        self.login_data = { 
                        "logintoken": f"{self.GetLoginToken()}",
                        "username": os.getenv("USERNAME"), 
                        "password": os.getenv("PASSWORD"),
                        }

        
    # Для авторизации необходимо передать logintoken | username | password
    # logintoken получаем на странице авторизации (он генерируется рандомно при каждом открытии сайта на 1 (одну) сессию)
    def GetLoginToken(self): 
        self.session = requests.Session()
        self.session.headers = {"User-Agent" : os.getenv("USER_AGENT")}
        response = self.session.get(url=self.url_login, stream=True)
        
        soup = BeautifulSoup(response.text, "lxml")
        
        data = soup.find(class_="login-form").find_all(name="input")
        
        return data[1]["value"]

    def SusuLogin(self):
        self.session.post(self.url_login, data=self.login_data) # Авторизация
        
        # Получение куки
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

 