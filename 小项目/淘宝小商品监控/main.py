import requests
import re
import json


headers = {
    'accept': 'application/json',
    'accept-language': 'zh-CN,zh;q=0.9',
    'bx-umidtoken': 'T2gAihzKj860LjBGhrq3nZLbW5dsQmxysXMRBkcSyYdVz3xC02Ee02a4eG3B6P8Vg3Y=',
    'cache-control': 'no-cache',
    'content-type': 'application/x-www-form-urlencoded',
    'origin': 'https://item.taobao.com',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://item.taobao.com/',
    'sec-ch-ua': '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
    'x-pipu2': "h%7Bdug%60ztggnoase%7D%232'h-7%25!g%2B%22u7*i99)9%3C-%24%7B*1%3B0%24%3A7%2B'%7B*1%3B0%24%3A7%2B'%7B*1%3B0%24%3A7%2B'%7Bo%7Boq",
    'cookie': ''
}

params = {
    'jsv': '2.7.5',
    'appKey': '12574478',
    't': '1749478810387',
    'sign': '481b0c255e262a0cf52cfb0cf5ae4350',
    'api': 'mtop.taobao.pcdetail.data.get',
    'v': '1.0',
    'isSec': '0',
    'ecode': '0',
    'timeout': '10000',
    'ttid': '2022@taobao_litepc_9.17.0',
    'AntiFlood': 'true',
    'AntiCreep': 'true',
    'dataType': 'json',
    'valueType': 'string',
    'type': 'json',
    'data': '{"id":"617219859305","detail_v":"3.3.2","exParams":"{\\"id\\":\\"617219859305\\",\\"priceTId\\":\\"213e07c917494783114667930e145e\\",\\"skuId\\":\\"4347871784889\\",\\"spm\\":\\"a21bo.tmall/a.201876.d18.77bac3d5BbbtSv\\",\\"utparam\\":\\"{\\\\\\"item_ctr\\\\\\":0.007128,\\\\\\"x_object_type\\\\\\":\\\\\\"p4p_item\\\\\\",\\\\\\"item_price\\\\\\":\\\\\\"44.8\\\\\\",\\\\\\"item_cvr\\\\\\":0.037043,\\\\\\"pc_scene\\\\\\":\\\\\\"20001\\\\\\",\\\\\\"aplus_abtest\\\\\\":\\\\\\"98c1e93d5515155cc9746aa4caf6bd6f\\\\\\",\\\\\\"tpp_buckets\\\\\\":\\\\\\"30986#418557#module\\\\\\",\\\\\\"ab_info\\\\\\":\\\\\\"30986#418557#-1#\\\\\\",\\\\\\"abid\\\\\\":\\\\\\"0\\\\\\",\\\\\\"pc_pvid\\\\\\":\\\\\\"c77535c3-0d06-44e8-8223-677f2762ddee\\\\\\",\\\\\\"mix_group\\\\\\":\\\\\\"\\\\\\",\\\\\\"item_ecpm\\\\\\":0.001283,\\\\\\"x_object_id\\\\\\":617219859305}\\",\\"xxc\\":\\"ad_ct\\",\\"queryParams\\":\\"id=617219859305&ltk2=1749478806940qd41py3eilwgpatpe73t7&priceTId=213e07c917494783114667930e145e&skuId=4347871784889&spm=a21bo.tmall%2Fa.201876.d18.77bac3d5BbbtSv&utparam=%7B%22item_ctr%22%3A0.007128%2C%22x_object_type%22%3A%22p4p_item%22%2C%22item_price%22%3A%2244.8%22%2C%22item_cvr%22%3A0.037043%2C%22pc_scene%22%3A%2220001%22%2C%22aplus_abtest%22%3A%2298c1e93d5515155cc9746aa4caf6bd6f%22%2C%22tpp_buckets%22%3A%2230986%23418557%23module%22%2C%22ab_info%22%3A%2230986%23418557%23-1%23%22%2C%22abid%22%3A%220%22%2C%22pc_pvid%22%3A%22c77535c3-0d06-44e8-8223-677f2762ddee%22%2C%22mix_group%22%3A%22%22%2C%22item_ecpm%22%3A0.001283%2C%22x_object_id%22%3A617219859305%7D&xxc=ad_ct\\",\\"domain\\":\\"https://item.taobao.com\\",\\"path_name\\":\\"/item.htm\\",\\"pcSource\\":\\"pcTaobaoMain\\",\\"appKey\\":\\"3q2+7wX9z8JkLmN1oP5QrStUvWxYzA0B\\",\\"refId\\":\\"tE98pXy+ryIcQEf0DFL/JQbpU8H3zoIqdjDZGlS2XI4=\\",\\"nonce\\":\\"Ee2tV0ThuXTDT4xJugMGTA==\\",\\"feTraceId\\":\\"b178fb1d-ab1c-4537-a914-30fd7350afdf\\"}"}',
}

response = requests.get(
    'https://h5api.m.taobao.com/h5/mtop.taobao.pcdetail.data.get/1.0/',
    params=params,
    headers=headers,
)


# 1. 包含 mtopjsonppcdetail2的处理方式
# pattern = r'mtopjsonppcdetail2\((.*?)\)$'
# match = re.search(pattern, response.text, re.DOTALL)
# json_text = json.loads(match.group(1))

# 2. 不包含 mtopjsonppcdetail2的处理方式
json_text = json.loads(response.text)
# vid和 skuid
vid_skuid = json_text['data']['skuBase']['skus']
vid_skuid_json = []
for i in vid_skuid:
    vid = i['propPath'].split(':')[1]
    skuid_vid = {
        'vid': vid,
        'skuid': i['skuId']
    }
    vid_skuid_json.append(skuid_vid)
# id 和 价格
price_status = json_text['data']['skuCore']['sku2info']
price_id_json = []
for vid_skuid  in vid_skuid_json:
    skuid_text_price = {
        'skuid': vid_skuid['skuid'],
        'vid' : vid_skuid['vid'],
        'price': price_status[vid_skuid['skuid']]['price']['priceText'],
        'text': price_status[vid_skuid['skuid']]['quantityText']
    }
    price_id_json.append(skuid_text_price)
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
        'skuid': i['skuid'],
        'vid': i['vid'],
        'price': i['price'],
        'text': i['text']
    })

print(price_id_name_json)
# 输出

