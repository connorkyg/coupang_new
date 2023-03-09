import random
import requests

from apis.webact import chrome
from _hidden import _keys
from apis import tistory
from data import tags
from data import titles

BLOG_NAME = _keys.TISTORY['ACCOUNT']['topnot']['BLOG_NAME']
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'


def post_write(keyword, content):
    baseUrl = 'https://www.tistory.com/apis/post/write'
    tag = random.sample(tags.tag_list, 4)
    data = {
        'access_token': f'{tistory.tistory().get_access_token()}',
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