import requests


data = {
"province" : "北京",
"city" : "北京"
}
header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0",
    "Cookie": "weather_data=mengta123"
}
url = f"http://127.0.0.1:5000/get_weather"
res = requests.get(url=url, params=data)
res.encoding = res.apparent_encoding
print(res.json())

url = f"http://127.0.0.1:5000/post_weather"
params = {
    "province": "北京",
    "city": "北京"
}
res = requests.post(url=url, headers= header, json=params)
res.encoding = res.apparent_encoding
print(res.json())