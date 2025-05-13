from idlelib.rpc import response_queue

import lxml
from lxml import etree

# html = etree.HTMLParser(encoding='utf-8')    # 显式指定读取的格式
#
# xml = etree.parse('hello.html', html)
# print(etree.tostring(xml).decode())
#
# # 读取某个路径下的某个节点的内容
#
# result = xml.xpath("//title/text()")
# print(result)
#
# result = xml.xpath("//ul[@class='nav-list']//a[@href='/home']/text()")
# print(result)
#
# result = xml.xpath("//article[@class='post']/p/text()")
# print(result)
#
# # 通过元素定位上一个标签
# result = xml.xpath("//section[h2 and p]")[1]
# print(result)
# # 在前基础上查找文章
# result = result.xpath(".//p[@id='post']/text()")
# print(result)


# 上面的输出：
# ['简单的HTML文档']
# ['首页']
# ['这是第一篇文章的摘要。', '这是第二篇文章的摘要。']
# <Element section at 0x1a69f1527c0>
# ['以下是文章列表：']


# ==============================实战==========================
# 获取某网页的内容
import requests
from lxml import etree
import re

def get_content(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0'
    }
    res = requests.get(url=url, headers=headers)
    res.encoding = res.apparent_encoding   # 自动识别编码格式, requests 请求会将网页的原编码放入到 res.apparent_encoding  中
    xml = etree.HTML(res.text)
    result = xml.xpath("//div[@class='txt' and @id='txt']/p//text()")
    output = []
    # 移除掉不需要的符号
    reg = re.compile(r'[\d]+[、].*?(。|？|！|\.\.\.\.\.\.|\.|\?|!|\(|\)|（|）|)$')
    for i in result:
        Match = re.match(reg, i)
        if Match:
            output.append(Match.group())
    result = output
    del output
    output = []
    # 移除括号
    reg = re.compile(r'\(.*?\)|（.*?）|[\(\)（）]')
    for i in result:
        output.append(re.sub(reg, "", i))

    title = xml.xpath("//div[@id='article']/h1/text()")
    output.insert(0, title[0])
    output = '\n'.join(output)
    return title, output

# 提取主页的全部名言目录
def get_table():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0'
    }
    url = "https://www.mingyannet.com/"
    res = requests.get(url=url, headers=headers)
    res.encoding = res.apparent_encoding
    result = etree.HTML(res.text)
    result = result.xpath("//div[@class='container main']//li//@href")
    base_url = "https://www.mingyannet.com"
    return [base_url + url for url in result]


if __name__ == '__main__':
    url = ''
    table = get_table()
    for url in table:
        title, output = get_content(url)
        with open(f'名人名言/{title[0]}.txt', 'w', encoding='utf-8') as file:
            file.write(output)
        print(f'{title[0]} 保存成功')

