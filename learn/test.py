import re

txt = r'760.第760章 今晚能发生点啥\.txt'

txt = re.sub(r"[<|>|?|*|\"|:|/|\\]+", "", txt)
print(txt)

ls = [1,2,3,4,5,6]
print(ls[::-1])