from playwright.async_api import async_playwright
import time, asyncio
from funcs.cookies import *
import logging

logging.basicConfig(level=logging.INFO, format="time: %(asctime)s | level: %(levelname)s | %(message)s")


class Susu: 
    def __init__(self, browser, cookies):
        self.browser = browser
        self.page = None
        self.cookies = cookies

    async def CreateBrowser(self): 
        # Создает экземпляр контекста 
        context = await self.browser.new_context(
            viewport={'width': 700, 'height': 500},
            user_agent='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
            ignore_https_errors=True,
            bypass_csp=True,
            no_viewport=False,
        )
        logging.info("Создание контекста")
        # Создаем новую вкладку
        self.page = await context.new_page()

        # Обновляем куки контекста
        await context.add_cookies(self.cookies)  
        logging.info("Получение куки")


    # Вход в аккаунт
    async def Login(self): 
        try: 
            await self.page.goto("https://edu.susu.ru/my/courses.php")
            logging.info("Вход в аккаунт выполнен")
            time.sleep(100)
        except Exception as e:
            print(e)

async def Start(): 
    logging.info("Запуск программы")
    # Инициализация класса reqSusu 
    edu = CookieGrab()
    # Получение куки
    cookie = edu.Login()

    # Создание экземпляра браузера
    async with async_playwright() as s: 
        browser = await s.chromium.launch(headless=False)
        edususu = Susu(browser, cookie)
        await edususu.CreateBrowser()
        await edususu.Login()


if __name__ == "__main__": 
    asyncio.run(Start())