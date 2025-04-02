from playwright.async_api import async_playwright
import time, asyncio, logging, os
from funcs.cookies import *

logging.basicConfig(level=logging.INFO, 
                    format="time: %(asctime)s | level: %(levelname)s | %(message)s",
                    filename="logwarning.log",
                    filemode="a+",
                    encoding="utf-8"
                    )


class Susu: 
    def __init__(self, browser, cookies):
        self.browser = browser
        self.page = None
        self.cookies = cookies

    # Создание браузера
    async def CreateBrowser(self): 
        # Создает экземпляр контекста 
        context = await self.browser.new_context(
            viewport={'width': 700, 'height': 500},
            user_agent=os.getenv("USER_AGENT"),
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


    # Переход на ссылку с курсами
    async def Login(self): 
        try: 
            await self.page.goto("https://edu.susu.ru/my/courses.php")
            logging.info("Вход в аккаунт выполнен")
            print(self.cookies)
            time.sleep(100)
        except Exception as e:
            print(e)

async def Start(): 
    logging.info("Запуск программы")
    # Инициализация класса CookieGrab | Получение куки 
    edu = CookieGrab()
    # Получение куки
    cookie = edu.SusuLogin()
    print(cookie)

    # Создание экземпляра браузера
    async with async_playwright() as s: 
        browser = await s.chromium.launch(headless=False)
        edususu = Susu(browser, cookie)
        await edususu.CreateBrowser()
        await edususu.Login()


if __name__ == "__main__": 
    asyncio.run(Start())