import openai
from _hidden import _keys

SECRET_KEY = _keys.KEYS['secretKey']
openai.api_key = SECRET_KEY

baseUrl = 'https://api.openai.com/v1/'


def command(cmd):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=cmd,
        max_tokens=1000,
        temperature=0
    )
    print(response)
    return response


### testtesttesttesttesttesttesttesttest ###
if __name__ == '__main__':
    command('hi. are you there?')
