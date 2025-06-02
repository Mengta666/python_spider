import requests

def get_publickey(session = None):
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
        'sec-ch-ua-platform': '"Windows"',
        # 'Cookie': 'lianjia_uuid=84cc6240-2736-4aba-993e-63d1d0f7ed07; select_city=110000; lianjia_ssid=1dbd798d-e3b5-48d6-b2c8-15a25e740d58; sajssdk_2015_cross_new_user=1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%221973013c065636-0217d68f6a22f2-26011f51-1638720-1973013c066d3a%22%2C%22%24device_id%22%3A%221973013c065636-0217d68f6a22f2-26011f51-1638720-1973013c066d3a%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E8%87%AA%E7%84%B6%E6%90%9C%E7%B4%A2%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fwww.google.com%2F%22%2C%22%24latest_referrer_host%22%3A%22www.google.com%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC%22%7D%7D; crosSdkDT2019DeviceId=-amkxow--p7z7kn-bl8ntusrgq9p5no-94bemqn3v',
    }

    json_data = {
        'service': 'https://ajax.api.ke.com/login/login/getuserinfo',
        'version': '2.0',
    }
    if session:
        response = session.post('https://clogin.ke.com/authentication/initialize', headers=headers, json=json_data)
    else:
        response = requests.post('https://clogin.ke.com/authentication/initialize', headers=headers, json=json_data)

    publickey = response.json()["publicKey"]["key"]
    loginTicketId = response.json()["loginTicketId"]
    return [publickey, loginTicketId]