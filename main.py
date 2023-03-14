# -*- coding: utf-8 -*-

import time
import random
import logging

from _hidden import _keys
from data import tags
from data import titles
from data import form
from data.keywords import keyword
from data.messages import message
from apis import gpt
from apis import coupang
from apis import tistory
from lib.lib import now
from lib.lib import random_sleep
from lib.lib import convert_to_html

logging.basicConfig(filename='example.log', level=logging.INFO)



def auto_A_type():
    """
    random으로 추출한 keyword의 쿠팡 검색 결과 (최대 10개)
    검색 결과를 form 글 양식에 맞추어 tistory에 posting

    * 쿠팡 검색 결과는 1시간에 최대 10번만 호출 가능
    * 사람이 쓴 것 처럼 일정 시간 간격을 두고 posting (tistory에 무작정 업로드하면 차단됨)

    :return: 성공 시 0 반환
    """
    # COMMENT: random keyword 검색 결과를 tistory에 form에 맞추어 posting
    for i in range(10):  # COMMENT: 시간당 최대 10번이므로 10으로 설정이 default
        blog_name = _keys.TISTORY["BLOG_INFO"]["BLOG_NAME"]
        title = f'{random.sample(titles.title_list, 1)[0]} {keyword} {random.sample(titles.title_end, 1)[0]}'
        content = form.top_ten(coupang.search_product(), keyword)
        tag = f'{random.choice(tags.tag_list)},{random.choice(tags.tag_list)},{random.choice(tags.tag_list)}'

        tistory.post_write(blog_name, title, content, tag)
        random_sleep(30, 600)
    time.sleep(60 * 60)  # COMMENT: (60*65)초 interval
    return 0


def auto_B_type():
    """
    gpt에 api로 message에 입력된 값 전달하여 answer 추출
    db에 gpt request, response(answer)을 저장
    db에 저장된 answer을 tistory에 posting

    :return:
    """

    blog_name = _keys.TISTORY["BLOG_INFO"]["BLOG_NAME"]
    title = f'{random.sample(titles.title_list, 1)[0]} {keyword} {random.sample(titles.title_end, 1)[0]}'
    content = convert_to_html(gpt.completion_turbo(message))
    tag = f'{random.choice(tags.tag_list)},{random.choice(tags.tag_list)},{random.choice(tags.tag_list)}'

    tistory.post_write(blog_name=blog_name, title=title, content=content, tag=tag)


def auto_C_type():
    """

    :return:
    """
    path = 'content_%s.txt' % now()
    with open(file=path, mode='w+', encoding='utf-8') as f:
        a = convert_to_html(gpt.completion_turbo(message))
        b = f'<br><br><br><br><h2 data-ke-size="size26"> {random.sample(titles.title_list, 1)[0]} 제품 정보 정리</h2><br><br><br>'
        c = form.top_ten(coupang.search_product(), keyword)
        d = a + b + c
        f.write(d)
        f.seek(0)
        content = f.read()

    blog_name = _keys.TISTORY["BLOG_INFO"]["BLOG_NAME"]
    title = f'{random.sample(titles.title_list, 1)[0]} {keyword} {random.sample(titles.title_end, 1)[0]}'
    tag = f'{random.choice(tags.tag_list)},{random.choice(tags.tag_list)},{random.choice(tags.tag_list)}'

    tistory.post_write(blog_name=blog_name, title=title, content=content, tag=tag)


if __name__ == '__main__':
    auto_C_type()