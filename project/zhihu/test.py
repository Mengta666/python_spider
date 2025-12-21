import time
import json
import requests
import re
from requests import Session
from lxml import etree
from bs4 import BeautifulSoup


# 获取cookie，cookie保存在mongo数据库中，并在后台保持更新
cookies = requests.get("http://127.0.0.1:5000/cookies", json={"username": 18026853660})
cookie = { cookie['name']: cookie['value']  for cookie in cookies.json()['data']['cookie']}
cookie_string = ';'.join([f"{cookie_name}={cookie_value}" for cookie_name, cookie_value in cookie.items()])

# 通用的头
headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
}

with Session() as session:
    # 获取全部大的主题下的内容
    session.cookies.update(cookie)
    response = session.get('https://www.zhihu.com/topics', headers=headers)
    html = etree.HTML(response.text)
    topics_id = html.xpath("/html/body/div[3]/div[1]/div/div/ul//@data-id")
    name = html.xpath("/html/body/div[3]/div[1]/div/div/ul//@href")
    topics_name = [[id , name] for id, name in zip(topics_id, name)]              # 组合：主题id和名字
    print(topics_name)
    # 获取hashid
    hash_id = json.loads(html.xpath("/html/body/div[3]/div[1]/div/div/div[2]/div/@data-init")[0])["params"]['hash_id']
    offset = 0                  # 偏移量
    data = {
        'method': 'next',
        'params': json.dumps({"topic_id": topics_name[3][0], "offset": offset, "hash_id": hash_id})
    }
    topics_headers = headers                                          # 新建一个专用请求头
    topics_headers['x-requested-with'] = 'XMLHttpRequest'
    topics_headers['x-xsrftoken'] = f"{cookie['_xsrf']}"
    time.sleep(3)       # 休眠3秒，避免被知乎识别为爬虫

    response = session.post('https://www.zhihu.com/node/TopicsPlazzaListV2', headers=topics_headers, data= data)
    # 处理获得的小主题
    any_topics = []
    for topic in response.json()['msg']:
        html_topic = etree.HTML(topic)
        topic_name = html_topic.xpath("//a[@target='_blank']//@alt")[0]
        topic_url = html_topic.xpath("//a[@target='_blank']/@href")[0]
        # 小主题对应的热门话题链接
        top_answer_url = f"https://www.zhihu.com{topic_url}/top-answers"
        any_topics.append([topic_name, top_answer_url])

    # print(any_topics)
    time.sleep(2)
    # 取其中一个小主题，可以循环取多个，有一个__zse_ck cookie需要逆向，才能获得数据，不过经过改进，已经在登录cookie中加入了这个cookie
    i = 0
    response = session.get(url=any_topics[i][1], headers=headers)
    html = etree.HTML(response.text)
    url = html.xpath('//*[@id="TopicMain"]//div[@class="List-item TopicFeedItem"]//h2[@class="ContentItem-title"]//@href')
    title = html.xpath('//*[@id="TopicMain"]//div[@class="List-item TopicFeedItem"]//h2[@class="ContentItem-title"]//text()')
    url_title = [item for item in zip(url, title)]
    print(url_title)

    # 已经获取到其中一个小主题下的所有内容了，取其中一个标题(问题)进行测试（同样可以循环取多个），可以取得高赞的前五个回答
    for i in range(len(title)):
        try:
            url = re.search(r'(.*)/answer/', url_title[i][0])
            url = 'https:' + url.group(1)
            question_id = re.search(r'/question/(\d+)', url).group(1)
            title = url_title[i][1]
            response = session.get(url=url,headers=headers)
            html = etree.HTML(response.text)
            # 找出json文件对应的数据
            content_data = json.loads(html.xpath('//*[@id="js-initialData"]/text()')[0])
            answers_info = content_data['initialState']['question']['answers']
            answers = content_data['initialState']['entities']['answers']
            all_answer = {}
            all_answer['title'] = title
            for j, answer in enumerate(answers_info[question_id]['newIds']):
                answer_id = answer['target']
                answer_content = answers[answer_id]['content']
                soup = BeautifulSoup(answer_content, 'html.parser')
                src = soup.find_all('img')
                src_content = {}
                src_list = []
                for img in src:
                    if img.find_parent('noscript'):
                        src_list.append(img.get('src'))
                answer_content = soup.get_text()
                src_content['answer_id'] = answer_id
                src_content['answer_content'] = answer_content
                src_content['src'] = src_list
                all_answer[f'{j}'] = src_content

            print(all_answer)
            # 处理完的数据保存为json文件，也可以存入数据库（mongodb）
            with open(f'{i}、{title}.txt', 'w', encoding='utf-8') as f:
                json.dump(all_answer, f, ensure_ascii=False)
            time.sleep(1)
        except  Exception as e:
            print(e)





