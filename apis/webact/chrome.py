from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import subprocess


class browser:
    USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'

    def __init__(self):
        service = Service(ChromeDriverManager().install())
        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        options.add_argument(f'user-agent={self.USER_AGENT}')
        options.add_argument("lang=ko_KR")
        self.driver = webdriver.Chrome(service=service, options=options)

    def navigate(self, url):
        self.driver.get(url)

    def quit(self):
        self.driver.quit()

# class browser:
#     subprocess.Popen(
#         r'C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\chrometemp"')  # 디버거 크롬 구동
#     USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
#     options = webdriver.ChromeOptions()
#     options.add_experimental_option("excludeSwitches", ["enable-automation"])
#     options.add_experimental_option("useAutomationExtension", False)
#     options.add_argument(f'user-agent={USER_AGENT}')
#     options.add_argument("lang=ko_KR")
#     service = Service(ChromeDriverManager().install())
#     driver = webdriver.Chrome(service=service, options=options)
