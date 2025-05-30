import hashlib
import base64
from hashlib import md5, sha1, sha256, sha512

obj = md5()
obj = sha256()
text = "这是要加密的数据".encode("utf-8")

obj.update(text)
encrypt = obj.hexdigest()
print(encrypt, len(encrypt))

base64_text = base64.b64encode(text)
print(base64_text, (base64.b64decode(base64_text)).decode("utf-8"))

