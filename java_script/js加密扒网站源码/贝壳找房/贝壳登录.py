
import execjs
from requests import Session

from get_publickey import get_publickey

seesion = Session()

header = {
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Referer': 'https://bj.ke.com/',
    'Sec-Fetch-Dest': 'script',
    'Sec-Fetch-Mode': 'no-cors',
    'Sec-Fetch-Site': 'cross-site',
    'Sec-Fetch-Storage-Access': 'active',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

params = {
    'sceneId': 'login_slider',
    'token': 'biieic8PVqYzzmssGncss8DKTYT8bKU4',
    'callback': '__jp0',
}

# 获取持久化cookie
seesion.options(url = 'https://captcha.lianjia.com/captcha/resource', headers = header, params=params)

publickey_id  = get_publickey(seesion)
# print(publickey_id)

with open("beike.js", "r", encoding="utf-8") as f:
    publickey = f.read()
t = {"username": "12323222323", "password": "qq123456", "encodeVersion": "1"}
password_key = execjs.compile(publickey).call("password_encrypt", publickey_id[0], publickey_id[1], t)


headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json;charset=UTF-8',
    'Origin': 'https://bj.ke.com',
    'Pragma': 'no-cache',
    'Referer': 'https://bj.ke.com/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"'
}

json_data = {
    'service': 'https://ajax.api.ke.com/login/login/getuserinfo',
    'mainAuthMethodName': 'username-password',
    'accountSystem': 'customer',
    'credential': {
        'username': '12323222323',
        'password': f'{password_key}',
        'encodeVersion': '1',
    },
    'loginTicketId': f'{publickey_id[1]}',
    'version': '2.0',
    'ticketMaxAge': 604800,
}

response = seesion.post('https://clogin.ke.com/authentication/authenticate', headers=headers, json=json_data)
print(response.text)
print(seesion.cookies)
seesion.close()


