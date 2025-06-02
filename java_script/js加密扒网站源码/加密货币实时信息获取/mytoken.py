import requests

import execjs

headers = {
    'accept': '*/*',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'no-cache',
    'origin': 'https://www.mytokencap.com',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://www.mytokencap.com/',
    'sec-ch-ua': '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
}


with open(r"E:\python\spider\java_script\js加密扒网站源码\加密货币实时信息获取\mytoken.js", "r", encoding="utf-8") as fp:
     js_code = fp.read()


time_code = execjs.compile(js_code).call("get_time_and_code")
print( time_code)

params = {
    'pages': '1,1',
    'sizes': '100,100',
    'subject': 'market_cap',
    'language': 'zh_CN',
    'legal_currency': 'USD',
    'code': f'{time_code[1]}',
    'timestamp': f'{time_code[0]}',
    'platform': 'web_pc',
    'v': '0.1.0',
    'mytoken': '',
}

response = requests.get('https://api.mytokenapi.com/ticker/currencyranklist', params=params, headers=headers)

print(response.json()['data']['list'])