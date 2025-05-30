# 网页： https://interface.bidcenter.com.cn/search/GetSearchProHandler.ashx
import json
import pprint

# python 调用js代码

import execjs
import requests


url = "https://interface.bidcenter.com.cn/search/GetSearchProHandler.ashx"
header = {
    "authority" : "interface.bidcenter.com.cn",
    "method" : "POST",
    "path" : "/search/GetSearchProHandler.ashx",
    "scheme" : "https",
    "accept" : "text/plain, */*; q=0.01",
    "accept-encoding" :"gzip, deflate, br, zstd",
    "accept-language" : "zh-CN,zh;q=0.9",
    "cache-control" : "no-cache",
    "content-length" : "185",
    "content-type" : "application/x-www-form-urlencoded;charset=UTF-8",
    "origin" : "https://search.bidcenter.com.cn",
    "pragma" : "no-cache",
    "priority" : "u=1,i",
    "referer" : "https://search.bidcenter.com.cn/",
    "sec-ch-ua" : 'Chromium";v="136", "Google Chrome";v="136","Not.A/Brand";v="99"',
    "sec-ch-ua-mobile" : "?0",
    "sec-ch-ua-platform" : '"Windows"' ,
    "sec-fetch-dest" : "empty",
    "sec-fetch-mode" : "cors",
    "sec-fetch-site" : "same-site",
    "user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36"
}

data = {
    "from" : 6137,
    "guid" : "3416DE2C-CB99-047C-1D61-CA3961DE5745",
    "location" : 6138,
    "keywords" : "%e5%85%ac%e5%85%b1%e8%b5%84%e6%ba%90%e4%ba%a4%e6%98%93",
    "token" : "",
    "mod" : 0,
    "page" : 3
}

str_data_encrypt = requests.post(url = url, headers = header, data=data)


with open ("caizhao.js", "r",  encoding="utf-8") as f:
    js_code = f.read()


# print(js_code)
# print(str_data_encrypt.text)

decrypted_data = execjs.compile(js_code).call("get_data", str_data_encrypt.text)

pprint.pprint(decrypted_data['other2']['listData'])

