import requests
import execjs

with  open(r'E:\python\spider\java_script\天翼云登录.js', 'r', encoding='utf-8') as f:
    js_code = f.read()


headers = {
    'accept': '*/*',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'no-cache',
    'content-type': 'application/x-www-form-urlencoded',
    'origin': 'https://www.ctyun.cn',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://www.ctyun.cn/h5/auth/login',
    'sec-ch-ua': '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
    'x-ctyun-accesstoken': 'null',
    'x-riskdevicesign': '1709fd6b3b14dbc4aa2bc12df2297677',
    'cookie': 'ct_m_search_from=google; ct_m_postId_expries=1748793599999; ct_m_pv_postId_expries=1748793599999; ct_m_ori_search_from=google; ct_m_event_postId_expries=1748793599999; vid=hmkWfdVribp3jNlcvWNTAYKqqnmhP2CDi1F9vfVEXQtFfCpujoGbRVEFIBF2FD03; ct_m_flow_postId_expries=1748793599999; ct_tgc=9b0409f9-ab5a-4763-a6be-5de10cc395cc; ct_m_pv_postId=4; ct_m_sid1=1748771176168-ifZNHm2mqn; ct_m_sid2=1748771176168-ifZNHm2mqn; ct_m_pvid=1; ct_m_dvc_id=1709fd6b3b14dbc4aa2bc12df2297677; ct_m_event_postId=51; ct_m_cat2_time=1748771256951; ct_m_cat2_id=10001.0.3; ct_m_label_id=4; ct_m_postId=92; ct_m_flow_postId=37; JSESSIONID=3lkqw66eel8y6mws6rmx9n7i',
}

username =  '1234567890'
password = '1234567890'
encrypt = execjs.compile(js_code).call('encrypt', f'{username}', f'{password}')
print(encrypt)

data = {
    'id': f'{username}',
    'loginFree': 'false',
    'loginType': 'password',
    'newMode': 'true',
    'other': f'{username}',
    'password': f'{encrypt}',
}

response = requests.post('https://www.ctyun.cn/gw/auth/Login', headers=headers, data=data)

print(response.text)