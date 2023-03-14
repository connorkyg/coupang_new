import os
import time
import requests
from selenium.webdriver.common.by import By

from apis.webact import chrome
from _hidden import _keys
from lib.lib import random_sleep


class auth:
    class data_info:
        def __init__(self):
            self.path = None
            self.domain = None
            self.url = None

    def __init__(self):
        self.web = chrome.browser()

    def login(self):
        # todo: driver 관련 method 분리시키느라, 세션 유지가 안될 수 있으니 안되는 경우, driver 관련 내용 모두 모듈화하여 리팩토링할 것
        url = 'https://www.tistory.com/auth/login'
        self.web.driver.get(url)
        if self.web.driver.find_element(By.XPATH, '//*[@id="cMain"]/div/div/div/a[1]/span[2]'):
            self.web.driver.find_element(By.XPATH, '//*[@id="cMain"]/div/div/div/a[1]/span[2]').click()
            time.sleep(2)
            self.web.driver.find_element(By.XPATH, '//*[@id="loginKey--1"]').send_keys(
                _keys.TISTORY['LOGIN_INFO']['ID'])
            pw = input("PW 입력: ")
            self.web.driver.find_element(By.XPATH, '//*[@id="password--2"]').send_keys(pw)
            random_sleep(2, 5)
            self.web.driver.find_element(By.XPATH, '//*[@id="mainContent"]/div/div/form/div[4]/button[1]').click()
            # return self.driver.
        else:
            pass
            # return self.driver

    def get_auth(self):
        auth_code = self.data_info()

        auth_code.domain = 'https://www.tistory.com/oauth/authorize'
        auth_code.url = auth_code.domain + '?client_id=' + _keys.TISTORY['API_KEY']['APP_ID'] + '&redirect_uri=' + \
                        _keys.TISTORY['BLOG_INFO']['redirect_uri'] + '&response_type=code'

        auth_code.path = f'./authorization_code_{_keys.TISTORY["BLOG_INFO"]["BLOG_NAME"]}.txt'
        if os.path.isfile(auth_code.path):
            with open(auth_code.path, 'r', encoding='utf-8') as f:
                code = f.read()
            return code
        elif not os.path.isfile(auth_code.path):
            self.login()
            random_sleep(1, 2)
            self.web.driver.get(auth_code.url)
            random_sleep(1, 2)
            self.web.driver.find_element(By.XPATH, '//*[@id="contents"]/div[4]/button[1]').click()
            current_url = self.web.driver.current_url
            random_sleep(1, 2)
            if 'error' in current_url:
                print("error while getting \'get_auth_url\'")
            random_sleep(2, 5)
            code = current_url.split('=')[1].split('&')[0]
            with open(auth_code.path, 'w+', encoding='utf-8') as f:
                f.write(code)
            return code

    def get_access_token(self):
        USER_AGENT = chrome.browser().USER_AGENT
        access_token = self.data_info()
        access_token.url = 'https://www.tistory.com/oauth/access_token'
        access_token.path = f'./access_token_{_keys.TISTORY["BLOG_INFO"]["BLOG_NAME"]}.txt'
        auth_code = self.get_auth()

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
        'access_token': f'{auth().get_access_token()}',
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


def post_write_s():
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.action_chains import ActionChains

    class TestTest():
        def setup_method(self, method):
            self.driver = webdriver.Chrome()
            self.vars = {}

        def teardown_method(self, method):
            self.driver.quit()

        def test_test(self):
            self.driver.get("https://www.tistory.com/")
            self.driver.set_window_size(1427, 835)
            self.driver.find_element(By.CSS_SELECTOR, ".thumb_profile").click()
            self.driver.find_element(By.LINK_TEXT, "쓰기").click()
            assert self.driver.switch_to.alert.text == "2023. 3. 14. 15:51에 저장된 글이 있습니다.\n이어서 작성하시겠습니까?"
            self.driver.switch_to.alert.dismiss()
            self.driver.find_element(By.ID, "editor-mode-layer-btn-open").click()
            self.driver.find_element(By.ID, "editor-mode-html-text").click()
            self.driver.find_element(By.ID, "post-title-inp").click()
            self.driver.find_element(By.ID, "post-title-inp").send_keys("aaaaaaa")
            self.driver.find_element(By.CSS_SELECTOR, ".CodeMirror-line").click()
            self.driver.execute_script("window.scrollTo(0,0)")
            self.driver.find_element(By.CSS_SELECTOR, ".cm-s-tistory-html textarea").send_keys("bbbbbbbbb")
            self.driver.find_element(By.ID, "tagText").click()
            self.driver.find_element(By.ID, "tagText").send_keys("ccccccccc")
            self.driver.find_element(By.ID, "publish-layer-btn").click()
            element = self.driver.find_element(By.ID, "open20")
            actions = ActionChains(self.driver)
            actions.move_to_element(element).perform()
            self.driver.find_element(By.ID, "open20").click()
            element = self.driver.find_element(By.CSS_SELECTOR, "body")
            actions = ActionChains(self.driver)
            actions.move_to_element(element, 0, 0).perform()
            element = self.driver.find_element(By.ID, "open20")
            actions = ActionChains(self.driver)
            actions.move_to_element(element).perform()
            self.driver.find_element(By.ID, "open20").click()
            element = self.driver.find_element(By.CSS_SELECTOR, "body")
            actions = ActionChains(self.driver)
            actions.move_to_element(element, 0, 0).perform()
            self.driver.switch_to.frame(1)
            self.driver.find_element(By.CSS_SELECTOR, ".recaptcha-checkbox-border").click()
            self.driver.switch_to.default_content()
            self.driver.find_element(By.ID, "publish-btn").click()