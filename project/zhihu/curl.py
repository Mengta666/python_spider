import re

url = "//www.zhihu.com/question/437783708/answer/1660566169"
url = re.search(r'(.*)/answer/',url)
url = 'https:' + url.group(1)
question_id = re.search(r'/question/(\d+)', url).group(1)
print(url, question_id)