import os
import time
import requests
import random
from selenium.webdriver.common.by import By

from data import tags
from data import titles
from data import keywords
from apis.webact import chrome
from _hidden import _keys
from lib import sleep


class tistory(chrome.browser):
    driver = chrome.browser().driver

    def login(self):
        url = 'https://www.tistorycom/auth/login'
        self.driver.get(url)
        if self.driver.find_element(By.CLASS_NAME, 'txt_login'):
            self.driver.find_element(By.CLASS_NAME, 'txt_login').click()
            self.driver.find_element(By.XPATH, '//*[@id="input-loginKey"]').send_keys(_keys.LOGIN_INFO['ID'])
            pw = input("PW 입력: ")
            self.driver.find_element(By.XPATH, '//*[@id="input-password"]').send_keys(pw)
            sleep(2, 5)
            self.driver.find_element(By.XPATH, '//*[@id="mainContent"]/div/div/form/div[4]/button[1]').click()
            # return self.driver.
        else:
            pass
            # return self.driver

    def get_auth(self):
        auth_code = data_info()

        auth_code.domain = 'https://www.tistory.com/oauth/authorize'
        auth_code.url = auth_code.domain + '?client_id=' + _keys.API_KEY['TISTORY_APP_ID'] + '&redirect_uri=' + \
                        _keys.BLOG_INFO['redirect_uri'] + '&response_type=code'

        auth_code.path = f'./authorization_code_{_keys.BLOG_INFO["BLOG_NAME"]}.txt'
        if os.path.isfile(auth_code.path):
            with open(auth_code.path, 'r', encoding='utf-8') as f:
                code = f.read()
            return code
        elif not os.path.isfile(auth_code.path):
            self.login()
            sleep(1, 2)
            self.driver.get(auth_code.url)
            sleep(1, 2)
            self.driver.find_element(By.XPATH, '//*[@id="contents"]/div[4]/button[1]').click()
            current_url = self.driver.current_url
            sleep(1, 2)
            if 'error' in current_url:
                print("error while getting \'get_auth_url\'")
            sleep(2, 5)
            code = current_url.split('=')[1].split('&')[0]
            with open(auth_code.path, 'w+', encoding='utf-8') as f:
                f.write(code)
            return code

    def get_access_token(self):
        USER_AGENT = chrome.browser().USER_AGENT
        access_token = data_info()
        access_token.url = 'https://www.tistory.com/oauth/access_token'
        access_token.path = f'./access_token_{_keys.BLOG_INFO["BLOG_NAME"]}.txt'
        auth_code = self.get_auth()

        if os.path.isfile(access_token.path):
            with open(access_token.path, 'r', encoding='utf-8') as f:
                return f.read()
        elif not os.path.isfile(access_token.path):
            params = {
                'client_id': _keys.API_KEY['TISTORY_APP_ID'],
                'client_secret': _keys.API_KEY['TISTORY_SECRET_KEY'],
                'redirect_uri': _keys.BLOG_INFO['redirect_uri'],
                'code': f'{auth_code}',
                'grant_type': 'authorization_code'
            }
            # Access-Token 발급
            request = requests.get(access_token.url, params=params,
                                   headers={'Accept': 'application/xml; charset=utf-8', 'User-Agent': USER_AGENT})
            if 'error' in request.text:
                print(request.text)
                exit()
            token = request.text.split('=')[1]
            with open(access_token.path, 'w+', encoding='utf-8') as f:
                f.write(token)
            return token

    def post_write(self, keyword, content):
        baseUrl = 'https://www.tistory.com/apis/post/write'
        tag = random.sample(tags.tag_list, 4)
        data = {
            'access_token': f'{self.get_access_token()}',
            'output': 'json',
            'blogName': f'{_keys.BLOG_INFO["BLOG_NAME"]}',
            'title': f'{random.sample(titles.title_list, 1)[0]} {keyword} {random.sample(titles.title_end, 1)[0]}',
            'content': f'{content}',
            'visibility': 3,
            'tag': f'{tag[0]}, {tag[1]}, {tag[2]}, {tag[3]}'
        }

        response = requests.post(baseUrl, data=data, headers={'Accept': 'application/xml; charset=utf-8',
                                                              'User-Agent': chrome.browser().USER_AGENT})
        print(response.text)
        return response


class data_info:
    def __init__(self):
        self.path = None
        self.domain = None
        self.url = None
