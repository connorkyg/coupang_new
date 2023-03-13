import json
import openai
import time
from db import db

from _hidden import _keys

now = time.strftime('%Y%m%d_%H%M%S')
SECRET_KEY = _keys.GPT['SECRET_KEY']
openai.api_key = SECRET_KEY


# def command_davinci(cmd):
#     completion = openai.Completion.create(
#         model="text-davinci-003",
#         prompt=cmd,
#         max_tokens=4000,
#         temperature=0
#     )
#     response = json.loads(json.dumps(completion))
#     text = response['choices'][0]['text']
#     with open(file='gpt.log', mode='w+', encoding='utf-8') as f:
#         f.write(text)
#
#     print(text)
#
#     try:
#         db.insert_request_info(ri_type='gpt', ri_raw=response, ri_payload=text)
#     except Exception as e:
#         print(e)
#
#     return text


def command_turbo(cmd):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=cmd,
        max_tokens=3500,
        temperature=0
    )
    response = json.loads(json.dumps(completion))
    text = response['choices'][0]['message']['content']
    with open(file='%s_gpt.log' % now, mode='w+', encoding='utf-8') as f:
        f.write(text)

    print(text)

    try:
        db.insert_request_info(ri_type='gpt', ri_raw=response, ri_payload=text)
    except Exception as e:
        print(e)

    return 0
