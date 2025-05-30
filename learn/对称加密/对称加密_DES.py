from Crypto.Cipher import DES
from Crypto.Util.Padding import unpad, pad
import base64

key = b"12345678"   # DES 8个字节即可
iv = b"12345678"
# 加密
cipher = DES.new(key, DES.MODE_CBC, iv)
s = "你好".encode()
s_pad = pad(s, DES.block_size)
s_encrypt = cipher.encrypt(s_pad)
s_base64 = base64.b64encode(s_encrypt)
print(s_base64.decode())

# 解密
cipher = DES.new(key, DES.MODE_CBC, iv)
# 解码
s_decrypt = base64.b64decode(s_base64)
# 解密
s_pad = cipher.decrypt(s_decrypt)
s_unpad = unpad(s_pad, DES.block_size)
print(s_unpad.decode())