import re

txt = r'760.第760章 今晚能发生点啥\.txt'

txt = re.sub(r"[<|>|?|*|\"|:|/|\\]+", "", txt)
print(txt)