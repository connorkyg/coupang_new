import os
import requests
from selenium.webdriver.common.by import By

from apis.webact import chrome
from _hidden import _keys
from lib.lib import random_sleep

if __name__ == '__main__':
    web = chrome.browser()


    def login():
        # todo: driver 관련 method 분리시키느라, 세션 유지가 안될 수 있으니 안되는 경우, driver 관련 내용 모두 모듈화하여 리팩토링할 것
        url = 'https://www.tistorycom/auth/login'
        web.driver.get(url)
        if web.driver.find_element(By.CLASS_NAME, 'txt_login'):
            web.driver.find_element(By.CLASS_NAME, 'txt_login').click()
            web.driver.find_element(By.XPATH, '//*[@id="input-loginKey"]').send_keys(
                _keys.TISTORY['LOGIN_INFO']['ID'])
            pw = input("PW 입력: ")
            web.driver.find_element(By.XPATH, '//*[@id="input-password"]').send_keys(pw)
            random_sleep(2, 5)
            web.driver.find_element(By.XPATH, '//*[@id="mainContent"]/div/div/form/div[4]/button[1]').click()
            # return self.driver.
        else:
            pass
            # return self.driver


    def get_auth():
        auth_code = data_info()

        auth_code.domain = 'https://www.tistory.com/oauth/authorize'
        auth_code.url = auth_code.domain + '?client_id=' + _keys.TISTORY['API_KEY']['APP_ID'] + '&redirect_uri=' + \
                        _keys.TISTORY['BLOG_INFO']['redirect_uri'] + '&response_type=code'

        auth_code.path = f'./authorization_code_{_keys.TISTORY["BLOG_INFO"]["BLOG_NAME"]}.txt'
        if os.path.isfile(auth_code.path):
            with open(auth_code.path, 'r', encoding='utf-8') as f:
                code = f.read()
            return code
        elif not os.path.isfile(auth_code.path):
            web.login()
            random_sleep(1, 2)
            web.driver.get(auth_code.url)
            random_sleep(1, 2)
            web.driver.find_element(By.XPATH, '//*[@id="contents"]/div[4]/button[1]').click()
            current_url = web.driver.current_url
            random_sleep(1, 2)
            if 'error' in current_url:
                print("error while getting \'get_auth_url\'")
            random_sleep(2, 5)
            code = current_url.split('=')[1].split('&')[0]
            with open(auth_code.path, 'w+', encoding='utf-8') as f:
                f.write(code)
            return code


    def get_access_token():
        USER_AGENT = chrome.browser().USER_AGENT
        access_token = data_info()
        access_token.url = 'https://www.tistory.com/oauth/access_token'
        access_token.path = f'./access_token_{_keys.TISTORY["BLOG_INFO"]["BLOG_NAME"]}.txt'
        auth_code = get_auth()

        if os.path.isfile(access_token.path):
            with open(access_token.path, 'r', encoding='utf-8') as f:
                return f.read()
        elif not os.path.isfile(access_token.path):
            params = {
                'client_id': _keys.TISTORY['API_KEY']['APP_ID'],
                'client_secret': _keys.TISTORY['API_KEY']['SECRET_KEY'],
                'redirect_uri': _keys.TISTORY['BLOG_INFO']['redirect_uri'],
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


    def post_write(blog_name, title, content, tag):
        baseUrl = 'https://www.tistory.com/apis/post/write'
        data = {
            'access_token': f'{get_access_token()}',
            'output': 'json',
            'blogName': blog_name,
            'title': title,
            'content': content,
            'visibility': 3,
            'tag': f'{tag}'
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
