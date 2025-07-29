import re
import json
import aiohttp 
import requests
from requests_ip_rotator import ApiGateway
from playwright.async_api import async_playwright
from typing import Any
import asyncio
import random
from fake_useragent import UserAgent

ua = UserAgent()
"""
setattr - это настройка для aiohttp, что бы работать с прокси.
из Python3.12 без этого работать не будет.
"""
setattr(asyncio.sslproto._SSLProtocolTransport, "_start_tls_compatible", True)

class Mixin:
    async def text_normalizer(self, text: str, remove_from_str: list[str] = None) -> str:
        """
        This method takes a string as an argument and removes all occurrences of 
        the strings in the list 'defect' from the string.

        :param text: The string to be normalized
        :return: The normalized string
        """
        defect = ['\n', '\b', '\r', '\\', '\xa0', '\ufeff', '&nbsp;']
        if remove_from_str != None:
            defect.extend(remove_from_str)
        try:
            if text == None:
                return text
            for symbol in defect:
                if symbol in text:
                    text = text.replace(symbol, ' ')
                    
            return text
        except Exception as ex:
            ValueError

    async def get_page(self, url: str, login: str, password: str, proxy_ip: str = None) -> str:
        """
        Функция для получения страницы для работи из beautifulsoup

        This method takes a URL as an argument and returns the page as a string.
        :proxy - "http://login:password@11.11.11.11:1111"
        :param url: The URL to get the page from
        :return: The page as a string
        :raises aiohttp.ClientError: If an error occurs during the execution of the task
        """
        if not proxy_ip or proxy_ip == "None":
            async with aiohttp.ClientSession( 
                max_line_size=8190 * 2, 
                max_field_size=8190 * 2, 
                headers={'Accept': 'text/html'}
                ) as session:
                async with session.get(url) as response:
                    return await response.text()
        elif proxy_ip:
            IP_= await self.proxy_checker(proxy_ip=proxy_ip, login=login, password=password)
            full_proxy = f"http://{login}:{password}@{IP_}"
            async with aiohttp.ClientSession( 
                max_line_size=8190 * 2, 
                max_field_size=8190 * 2, 
                headers={'Accept': 'text/html'}
                ) as session:
                async with session.get(url, proxy=full_proxy) as response:
                    return await response.text()
            

    @staticmethod
    def pw_main( 
          headless: bool = False, 
          proxy_ip: str = None, 
          login: str = None, 
          password: str = None
        ) -> Any | None:
        """ 
        При вызове функции передаете только url в виде строки
        pw_result = await some_parser('some_url')

        @pw_main(time_browser_work: int = 5, headless: bool = False, proxy: dict)
        async def some_parser(page, url):
                await page.goto(url)
        ::proxy - {
            "server": "http:://11.11.11.11:1111",
            "username": login,
            "password": password
            }
        ::time_browser_work - время работы браузера в секундах
        ::headless - режим браузера(если True - браузер не открывается)"""
        def decorator(function):
            """
            A decorator that sets up a Playwright browser context and page for the decorated function.

            This static method wraps a function that requires a Playwright page, handling the setup and teardown
            of the browser context. It launches a Chromium browser, creates a new context with specified settings,
            and passes a Playwright page object to the wrapped function. After the function execution, it waits
            for a short timeout before returning the result.

            :param function: The function to wrap, which should accept `self`, `page`, and `url` as arguments.
            :return: A wrapper function that sets up the Playwright environment and executes the wrapped function.
            """
            async def wrapper(self, *args): 
                playwright = await async_playwright().start()

                if proxy_ip:
                    list_of_ip = [ip.strip() for ip in proxy_ip.split(',')]
                    IP_ = random.choice(list_of_ip)
                    proxy = {
                        'server':  f"http://{IP_}", 
                        'username': login, 
                        'password': password}
                    browser = await playwright.chromium.launch(headless=headless, proxy=proxy)
                elif proxy_ip == None or proxy_ip == "None":
                    browser = await playwright.chromium.launch(headless=headless)

                context = await browser.new_context(
                    ignore_https_errors=True,
                    java_script_enabled=True,
                    locale='en-US',
                    timezone_id="America/New_York", 
                    geolocation={"longitude": -74.0060, "latitude": 40.7128}, 
                    permissions=['geolocation'],
                    user_agent=ua.random, #"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36\
                                #(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
                    viewport={'width': 1920, 'height': 1080},
                    extra_http_headers={
                        "Accept-Language": "en-US,en;q=0.9"
                    })
                await context.add_cookies([
                    {
                        'name': 'locale',
                        'value': 'en',
                        'domain': 'www.google.com',
                        'path': '/',
                        'expires': -1,
                        'httpOnly': False,
                        'secure': False,
                        'sameSite': 'Lax'
                    }])
                page = await context.new_page()
                parse_result = await function(self, page=page, url=args[0])
                await browser.close()
                await playwright.stop()
                return parse_result
            return wrapper
        return decorator
    


    async def send_data_to_srm(self, parse_data: dict, crm_url: str) -> None:
        """
        This function sends the data to the server.

        It takes a dictionary of the data which should be sent as an argument.
        The dictionary should contain the following keys:
        dict = {
            "title": title - str - the title of the news,
            "content": content - str - the content of the news,
            "image": image - str - the link to the image of the news,
            "region": "region - str - the region of the news,
            "categories_name": "categories_name - str - the name of the category of the news
        }
        If something goes wrong during the sending, it raises ValueError.
        """
        try:
            req = requests.post(url=crm_url, json=parse_data)
            print(req.status_code)
        except Exception as ex:
            ValueError

    
    async def proxy_checker(self, proxy_ip: str, login: str, password: str) -> str:
        """Проверка прокси на работоспособность"""

        list_of_ip = [ip.strip() for ip in proxy_ip.split(',')] # разбиваем прокси на список
        
        for i in list_of_ip:
            IP_ = random.choice(list_of_ip) # выбираем рандомный прокси
            full_proxy = f"http://{login}:{password}@{IP_}" # формируем прокси
            try:
                """если в течении 3 секунд прокси работает(нет исключений), то возвращаем его,
                иначе идем дальше по списку прокси"""
                requests.get("http://google.com", proxies={'http': full_proxy, 'https': full_proxy}, timeout=3)
                return IP_
            except Exception as ex:
                print(f"IP: {IP_} error: {ex}")
                continue


    async def request_proxy(self, login: str, password: str, proxy_ip: str = None) -> dict:
        """рандомно генерируется прокси для запросов через aiohttp и requests"""
        if proxy_ip == None or proxy_ip == "None":
            return None
        IP_ = await self.proxy_checker(proxy_ip=proxy_ip, login=login, password=password)
        full_proxy = f"http://{login}:{password}@{IP_}"
        return {'http': full_proxy, 'https': full_proxy}
    
    
    async def pw_proxy(self, proxy_ip: str, login: str, password: str) -> dict:
        """рандомно генерируется прокси для запросов через krawl4ai и playwright"""
        IP_ = await self.proxy_checker(proxy_ip=proxy_ip, login=login, password=password)
        return {
            'server':  f"http://{IP_}", 
            'username': login, 
            'password': password}
