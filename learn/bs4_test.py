from bs4 import BeautifulSoup

html_doc = """
<!DOCTYPE html>
<html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <title>简单的HTML文档</title>
    </head>
    <body>
        <header>
            <h1>欢迎来到我的网站</h1>
            <nav>
                <ul class="nav-list">
                    <li><a href="/home">首页</a></li>
                    <li><a href="/about">关于</a></li>
                    <li><a href="/contact">联系</a></li>
                </ul>
            </nav>
        </header>
        <main>
            <section id="intro">
                <h2>简介</h2>
                <p>这是一个用于lxml练习的简单HTML页面，包含多种元素和结构。</p>
            </section>
            <section id="articles">
                <h2>文章列表</h2>
                <p id="post">以下是文章列表：</p>
                <article class="post">
                    <h3>第一篇文章</h3>
                    <p>这是第一篇文章的摘要。</p>
                    <span Author="author">作者：张三</span>
                </article>
                <article class="post">
                    <h3>第二篇文章</h3>
                    <p>这是第二篇文章的摘要。</p>
                    <span Author="author">作者：李四</span>
                </article>
            </section>
        </main>
        <footer>
            <p>© 2025 我的网站。保留所有权利。</p>
        </footer>
    </body>
    <b><!------------------这是注释----------------></b>
</html>

"""

soup = BeautifulSoup(html_doc, 'html.parser')
# print(soup.prettify())

# # 获取标签，只能获取第一个标签
# print(soup.a)
# # 获取标签名称
# print(soup.a.name)
# # 获取标签属性
# print(soup.a.attrs)
# # 获取标签下的指定属性
# print(soup.a['href'])
#
# # 改变标签的属性值
# soup.a['href'] = 'brother'
# print(soup.a['href'])
#
# # 获取标签的内容
# print(soup.a.text)
# print(soup.b.string)
#
# # 获取注释文本内容
# print(type(soup.b.string))
#
# # 遍历文档
# body_tag = soup.body
# # 返回所以节点
# # print(f"\n所有节点：\n{body_tag.contents}")
# # 返回所有结点的迭代器
# print(f"\n所有节点迭代器：")
# for child in body_tag.children:
#     print(repr(child))
#
# # 返回所有文本内容
# print(f"\n所有文本内容：\n")
# for context in body_tag.strings:              # strippd_strings 去除空格和换行符
#     print(repr(context))


# # 搜索文档
# # find只返回第一个匹配的标签
# print(soup.find('a'))
# # findall 返回所有匹配的标签
# context = soup.find_all('article',class_="post")
# print(context[0].p.text)

# css选择器 soup.select
# 查找所有叫article的标签
# print(soup.select('article'))
# 查找所有属性值为post的标签
# print(soup.select('.post'))
# 查找所有class = post的标签
# print(soup.select('[class="post"]'))

