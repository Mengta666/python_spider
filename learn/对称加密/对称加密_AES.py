# aes, des, 3des
# 见笔记

from Crypto.Cipher import  AES
from Crypto.Util.Padding import pad, unpad
import base64

from cryptography.hazmat.primitives.ciphers import Cipher


def aes_encrypt(string, key, iv):
    Cipher = AES.new(key = key, mode = AES.MODE_CBC, iv = iv)

    s = string.encode("utf-8")
    # 需要对数据进行填充补位，原本的s可能不是16的倍数，所以需要填充补位
    s_pad = pad(s , AES.block_size)
    # 加密
    cipher = Cipher.encrypt(s_pad)

    # print(cipher)
    # 使用base64进行编码
    cipher_base64 = base64.b64encode(cipher).decode()
    # NSIhTLHfrHpZEKuUiufGubEKtWxt5uHSmiebTlx5PfQ=    = 表示填充补位
    return cipher_base64

def aes_decrypt(string_base64, key, iv):

    cipher = AES.new(key = key, mode = AES.MODE_CBC, iv = iv)
    # base64 解码
    string_unbase64 = base64.b64decode(string_base64)
    # 解密
    string = cipher.decrypt(string_unbase64)
    # 取消填充
    string_unpad = unpad(string, AES.block_size)
    return string_unpad.decode("utf-8")

if __name__ == "__main__":
    key = b"0123456789abcdef"  # 16个字节
    iv = b"0123456789abcdef"  # 对首部进行加密需要用到的偏移（ECB不需要）

    string = "hello world"
    string_base64 = aes_encrypt(string, key, iv)
    print(string_base64)
    string_unbase64 = aes_decrypt(string_base64, key, iv)
    print(string_unbase64)
