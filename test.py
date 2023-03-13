import requests

# 요청 보내기
url = "https://api.openai.com/v1/completions"
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer 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",
}
data = {
    "prompt": "Hello, world!",
    "temperature": 0.5,
    "max_tokens": 100,
    "model": "text-davinci-003"
}
response = requests.post(url, json=data, headers=headers)

print(response.text)