import requests
import execjs
import json

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Content-Type': 'application/json',
    'Origin': 'http://jx.381314.xyz',
    'Pragma': 'no-cache',
    'Proxy-Connection': 'keep-alive',
    'Referer': 'http://jx.381314.xyz/user/parse',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
    'X-XSRF-TOKEN': 'eyJpdiI6IlZWUXpuS3F5NUxoZ1BwemJodG5IclE9PSIsInZhbHVlIjoiY3RtY3grelAwN1pRbGZNQlN3WGVWeC9BaWdjTjMrazNTbEZDWkRBTDNlSTNLM2J5Vk1aajJkMWVDUWhKd0YyQm1pT1JaaDQyNmtiZnBQc2ZGYml3WFRKUDVsVDJqdjBJTU55Q3RHYUVaS0FEeWtlTG9UYnE0L1pFTFNpNVd0N3ciLCJtYWMiOiJkZGY4ZDRlMjIyN2M1N2Q5MGU5ZGIyZDI5NGMxMjY2Yjc2ZDNiMmU2MDQwNDU3ZThhMWU0MTU5M2Y5MjExNTc4IiwidGFnIjoiIn0=',
}

# 目前用不到，不需要校验也能直接获取
with open("rand2.js",  "r", encoding="utf-8") as f:
    rand2 = f.read()
with open("rand1_3.js",  "r", encoding="utf-8") as f:
    rand1_3 = f.read()


# 解析的百度链接
jiexi_url = "https://pan.baidu.com/s/1ma-aC5obs1BYU2vG9co0fw"
# 解析的链接的路径（最后一个/后面的内容）
surl = "1ma-aC5obs1BYU2vG9co0fw"
# 提取码
pwd = "2i0o"
# 解析的路径（初始设为 /）
dir = "/10万首·音乐歌曲全类目合集（车载·DJ·抖音·MV·榜单歌曲·经典老歌·BGM等）[打造最全资源，持续更新不断]"
# 解析的密码
parse_password = "963plm"

# rand系列加密数据（用于服务器验证）
# 伪造了一个指纹，直接获取校验2即可
func_rand2 = execjs.compile(rand2)
func_rand1_3 = execjs.compile(rand1_3)
rand2 = func_rand2.call("get_rand2")
# 需替换成上面的各个自定义变量
rand_path = '{"url":"https://pan.baidu.com/s/1ma-aC5obs1BYU2vG9co0fw","surl":"1ma-aC5obs1BYU2vG9co0fw","pwd":"2i0o","dir":"/10万首·音乐歌曲全类目合集（车载·DJ·抖音·MV·榜单歌曲·经典老歌·BGM等）[打造最全资源，持续更新不断]","parse_password":"963plm"}'
# 校验1用的请求的路径和其他参数，校验3通过校验2生成
rand13 = func_rand1_3.call("get_rand1_3", rand_path, rand2)
# print(rand13)

json_data = {
    'url': f'{jiexi_url}',
    'surl': f'{surl}',
    'pwd': f'{pwd}',
    'dir': f'{dir}',
    'parse_password': f'{parse_password}',
    'rand1': f'{rand13[0]}',
    'rand2': f'{rand2}',
    'rand3': f'{rand13[1]}'
}

response = requests.post(
    'http://jx.381314.xyz/api/v1/user/parse/get_file_list',
    headers=headers,
    json=json_data,
    verify=False,
)

# print(response.json())
randsk = response.json()['data']['randsk']
uk = response.json()['data']['uk']
shareid = response.json()['data']['shareid']
file_list = response.json()['data']['list']
# print(file_list)
fs_id = file_list[2]['fs_id']
dir = file_list[2]['path']
surl = surl
pwd = pwd
parse_password = parse_password
down_rand = {"randsk":f"{randsk}","uk":uk,"shareid":shareid,"fs_id":[fs_id],"surl":f"{surl}","dir":f"{dir}","pwd":f"{pwd}","token":"guest","parse_password":f"{parse_password}","vcode_str":"","vcode_input":""}

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json',
    'Origin': 'http://jx.381314.xyz',
    'Pragma': 'no-cache',
    'Referer': 'http://jx.381314.xyz/user/parse',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
    'Cookie': 'XSRF-TOKEN=eyJpdiI6IkIzSXppUm9Xb1ZsYTRJZUtDU3JwNmc9PSIsInZhbHVlIjoiK2Nzai8vZ3ZLWHdtTHpGUTNFYWRCcUQwdjcrelJkb1ZEbjhZQ1dBV1F0dXdCTEhEYWhlYlF0TjRMTEFtTmUyYnhielNwWVc0alk3S3F6ZFd1emZKMFJJcytycUg4Sm4vTGdiUFVvdkhLVG5RV2RIU0hSKytmK0d6SlBUMHJiRjkiLCJtYWMiOiJmOTM4Yzg3OThjMWVmMjRiNjc0ODQ3OWU2MjI0M2RlZDc3MzliNTUxMjk0NzY0YjExMWE3ZDIyODNlZmIwYTYwIiwidGFnIjoiIn0%3D; _session=eyJpdiI6Ink3bjVSV1p1VnVQYmtJZG5IMDFYRHc9PSIsInZhbHVlIjoiTWVMSys1Z1prTUZ5ZzZIYmJ4TENjQml1RnExV2VHMEhpODRyRjNFRGxKN1pmS1R5WmEwU3dLT1MyZjhLSWQ3bDZ1ZTRMYWdzbEh1cFBOYWY2ZFhxU1E1a05ueS9pbWxwYzFJc1NvQ1crc1pPanJ1Y0ZDQnM0OERZMm5kWDNCam0iLCJtYWMiOiI3NDY1ZmIzYjRhNGZjNGZhMzZiNTFmYjA0MWNmZmUxZmE3MDk4YWYzMmQzODNkMDZkMmFiOGJlOTRkMjc0YTQ1IiwidGFnIjoiIn0%3D'
}

# 新的
rand2 = func_rand2.call("get_rand2")
rand13  = func_rand1_3.call("get_rand1_3", down_rand, rand2)
print(rand13, rand2)
json_data = {
    'randsk': f'{randsk}',
    'uk': uk,
    'shareid': shareid,
    'fs_id': [
        fs_id,
    ],
    'surl': f'{surl}',
    'dir': f'{dir}',
    'pwd': f'{pwd}',
    'token': 'guest',
    'parse_password': f'{parse_password}',
    'vcode_str': '',
    'vcode_input': '',
    'rand1': f'{rand13[0]}',
    'rand2': f'{rand2}',
    'rand3': f'{rand13[1]}'

}

try :
    response = requests.post(
        'http://jx.381314.xyz/api/v1/user/parse/get_download_links',
        headers=headers,
        json=json_data,
        verify=False,
    )

    print(response.json())
except Exception as e:
    print(e)


