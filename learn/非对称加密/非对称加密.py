from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
import base64

def generate_key():
    # 生成钥匙类
    key = RSA.generate(2048)
    # 生成私钥 （解密用私钥)
    private_key = key.export_key()
    # 生成密钥对应的公钥 (加密用公钥)
    public_key = key.publickey().export_key()

    with open("private_key.pem", "wb") as f:
        f.write(private_key)
    with open("public_key.pem", "wb") as f:
        f.write(public_key)

    return True

def encrypt(plain_key):
    public_key = RSA.import_key(open("public_key.pem").read())

    Cipher = PKCS1_v1_5.new(public_key)
    Cipher_text = Cipher.encrypt(plain_text)
    # print(Cipher_text)

    base64_text = base64.b64encode(Cipher_text)
    # print(base64_text)

    return base64_text

# 解密
def decrypt(base64_text):
    private_key = RSA.import_key(open("private_key.pem").read())
    # 创建解密对象
    Cipher = PKCS1_v1_5.new(private_key)
    base64_text = base64.b64decode(base64_text)
    plain_text = Cipher.decrypt(base64_text, None)
    return plain_text

if __name__ == "__main__":
    plain_text = "hello world".encode("utf-8")
    if generate_key() :
        base64_text = encrypt(plain_text)
        print(base64_text)
        plain_text = decrypt(base64_text)
        print(plain_text)
