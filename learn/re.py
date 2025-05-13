# 正则表达式
import re

txt = r"aaa888\water"
t1 = re.findall(r"(\d+)",txt)
print(t1)

# compile 将字符串编译成正则表达式对象，若该字符串正则多次使用，编译后更快
# t2 = re.compile(r"(\d+)")
# match 从头开始匹配
# findall 匹配所有满足的字符串
# search 匹配第一个满足的字符串
# sub 匹配并替换字符串
# split 匹配并分割字符串