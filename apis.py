# -*- coding: utf-8 -*-

import os
import requests
import json
import hmac
import hashlib
import time
import random
import logging
from urllib import parse


from _hidden import _keys
from data import keywords

# from db import db

now = time.strftime('%Y%m%d_%H%M%S')
now_log = time.strftime('%Y-%m-%d %H:%M:%S')

DOMAIN = "https://api-gateway.coupang.com"

LOG_FILENAME = 'coupang.log'
logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)



def generate_hmac(method, url, secret_key, access_key):
    path, *query = url.split("?")
    dateGMT = time.strftime('%y%m%d', time.gmtime())
    timeGMT = time.strftime('%H%M%S', time.gmtime())
    datetime = dateGMT + 'T' + timeGMT + 'Z'
    message = datetime + method + path + (query[0] if query else "")
    signature = hmac.new(bytes(secret_key, "utf-8"),
                         message.encode("utf-8"),
                         hashlib.sha256).hexdigest()

    return "CEA algorithm=HmacSHA256, access-key={}, signed-date={}, signature={}".format(access_key, datetime,
                                                                                          signature)


def get_product():
    keyword = random.sample(keywords.keyword_list, 1)[0]
    url_keyword = parse.quote(keyword)
    limit = 10
    url = f"/v2/providers/affiliate_open_api/apis/openapi/products/search?keyword={url_keyword}&limit={limit}"
    method = 'GET'
    authorization = generate_hmac(method, url, _keys.API_KEY['COUPANG_SECRET_KEY'],
                                  _keys.API_KEY['COUPANG_ACCESS_KEY'])
    coupang_url = '{}{}'.format(DOMAIN, url)
    response = requests.request(method=method, url=coupang_url,
                                headers={"Authorization": authorization, "Content-Type": "application/json"})
    if response.status_code >= 400:
        logging.error(response.text)
        exit()
    else:
        os.makedirs('./log', exist_ok=True)
        with open(file='./log/coupang_api.txt', mode='w+', encoding='utf-8') as f:
            f.write(f'{now_log} API request\n')
            f.write(f'\t\t\t\t\t{response.url}')
        retdata = json.dumps(response.json(), indent=4).encode('utf-8')
        jsondata = json.loads(retdata)
        data = jsondata['data']
        productdata = data['productData']
        with open(f'./log/product_data_{now}.txt', 'w+', encoding='utf-8') as f:
            f.write(str(productdata))
        with open(f'./log/jsondata_{now}.txt', 'w+', encoding='utf-8') as f:
            f.write(json.dumps(productdata))

        return productdata
