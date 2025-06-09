import requests
import re
import json

headers = {
    'accept': '*/*',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'referer': 'https://detail.tmall.com/',
    'sec-ch-ua': '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'script',
    'sec-fetch-mode': 'no-cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
    'cookie': ''
}


response = requests.get(
    'https://h5api.m.tmall.com/h5/mtop.taobao.pcdetail.data.get/1.0/?jsv=2.7.5&appKey=12574478&t=1749473185188&sign=b0192f97f08b5e4fcaf5d799b257f9c5&api=mtop.taobao.pcdetail.data.get&v=1.0&isSec=0&ecode=0&timeout=10000&ttid=2022%40taobao_litepc_9.17.0&AntiFlood=true&AntiCreep=true&jsonpIncPrefix=pcdetail&type=jsonp&dataType=jsonp&callback=mtopjsonppcdetail2&data=%7B%22id%22%3A%22897269589370%22%2C%22detail_v%22%3A%223.3.2%22%2C%22exParams%22%3A%22%7B%5C%22abbucket%5C%22%3A%5C%228%5C%22%2C%5C%22detail_redpacket_pop%5C%22%3A%5C%22true%5C%22%2C%5C%22id%5C%22%3A%5C%22897269589370%5C%22%2C%5C%22ns%5C%22%3A%5C%221%5C%22%2C%5C%22priceTId%5C%22%3A%5C%222147800a17494692675442492e1a32%5C%22%2C%5C%22query%5C%22%3A%5C%22%E7%BB%B4%E7%AE%80K2%5C%22%2C%5C%22skuId%5C%22%3A%5C%225921371470662%5C%22%2C%5C%22spm%5C%22%3A%5C%22a21n57.1.hoverItem.1%5C%22%2C%5C%22utparam%5C%22%3A%5C%22%7B%5C%5C%5C%22aplus_abtest%5C%5C%5C%22%3A%5C%5C%5C%2267d7ff917d55df6470995c710d096c04%5C%5C%5C%22%7D%5C%22%2C%5C%22xxc%5C%22%3A%5C%22taobaoSearch%5C%22%2C%5C%22queryParams%5C%22%3A%5C%22abbucket%3D8%26detail_redpacket_pop%3Dtrue%26id%3D897269589370%26ltk2%3D1749469269740yljzvjre5timovongdrcpc%26ns%3D1%26priceTId%3D2147800a17494692675442492e1a32%26query%3D%25E7%25BB%25B4%25E7%25AE%2580K2%26skuId%3D5921371470662%26spm%3Da21n57.1.hoverItem.1%26utparam%3D%257B%2522aplus_abtest%2522%253A%252267d7ff917d55df6470995c710d096c04%2522%257D%26xxc%3DtaobaoSearch%5C%22%2C%5C%22domain%5C%22%3A%5C%22https%3A%2F%2Fdetail.tmall.com%5C%22%2C%5C%22path_name%5C%22%3A%5C%22%2Fitem.htm%5C%22%2C%5C%22pcSource%5C%22%3A%5C%22pcTaobaoMain%5C%22%2C%5C%22appKey%5C%22%3A%5C%223q2%2B7wX9z8JkLmN1oP5QrStUvWxYzA0B%5C%22%2C%5C%22refId%5C%22%3A%5C%225DVyxO2JxeoubKVdIAx%2BPrbQc%2FYtWx4c2I6mI3sfh2M%3D%5C%22%2C%5C%22nonce%5C%22%3A%5C%22GF7eKjzaygHgB0l4e2ftBmWUdH6ajvnDOPi0qsyBGRQ%3D%5C%22%2C%5C%22feTraceId%5C%22%3A%5C%22068169a6-a07e-4784-8e99-a31d50e6746d%5C%22%7D%22%7D&bx-umidtoken=T2gAZ4CzS9vHOQF0NqmO-FIgYfQglAYSyzWkwpxHhNhV3Kr0KPktkG9smvmp9TQCX5s%3D&x-pipu2=h%257Bdug%2560ztlngjgsb%257D~*k5hg%253D%252B%253D%2520%253E7%253Dojf%2524.25%257B%2526j%257B*11%2750%2520%2526%253B%257B*11%2750%2520%2526%253B%257B*11%2750%2520%2526%253B%257Bo%257Bef&bx-ua=fast-load',
    headers=headers
)

pattern = r'mtopjsonppcdetail2\((.*?)\)$'

match = re.search(pattern, response.text, re.DOTALL)
json_text = json.loads(match.group(1))
# vid和 skuid
vid_skuid = json_text['data']['skuBase']['skus']
vid_skuid_json = []
for i in vid_skuid:
    vid = i['propPath'].split(':')[1]
    shuid_vid = {
        'vid': vid,
        'skuid': i['skuId']
    }
    vid_skuid_json.append(shuid_vid)
# id 和 价格
price_status = json_text['data']['skuCore']['sku2info']
price_id_json = []
for vid_shuid  in vid_skuid_json:
    shuid_text_price = {
        'shuid': vid_shuid['skuid'],
        'vid' : vid_shuid['vid'],
        'price': price_status[vid_shuid['skuid']]['price']['priceText'],
        'text': price_status[vid_shuid['skuid']]['quantityText']
    }
    price_id_json.append(shuid_text_price)
# 名字 和 vid
name_vid = json_text['data']['skuBase']['props'][0]['values']
name_vid_json = {}
for i in name_vid:
    vid = i['vid']
    name_vid_json[vid] = i['name']

# 将vid与名字配对
price_id_name_json = []
for i in price_id_json:
    price_id_name_json.append({
        'name': name_vid_json[i['vid']],
        'shuid': i['shuid'],
        'vid': i['vid'],
        'price': i['price'],
        'text': i['text']
    })

print(price_id_name_json)
# 输出

