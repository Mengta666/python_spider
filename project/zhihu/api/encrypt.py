import base64
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from project.zhihu.api.AES_256_key import key_path


def aes_encrypt(password):
    """
    对数据进行加密，步骤如下：
    1、编码成 utf-8 格式
    2、对数据进行填充，保证数据长度为16的倍数
    3、使用AES加密模式，对数据进行加密
    4、使用base64进行编码，返回加密后的数据
    """

    if not key_path.exists():
        raise FileNotFoundError(f"密钥文件不存在: {key_path}")

    with key_path.open("rb") as f:
        key = f.read()

    iv = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)

    # 编码成utf-8字节流
    pw_code = password.encode("utf-8")
    pw_pad = pad(pw_code, AES.block_size)

    pw_encrypt = cipher.encrypt(pw_pad)
    pw_base64 = base64.b64encode(pw_encrypt)

    return pw_base64, iv


def aes_decrypt(pw_base64, iv):
    """
    对加密的数据进行解密，步骤如下：
    1、对base64解码
    2、AES解密
    3、取消填充
    4、按照 utf-8 解码，得到原始数据
    """
    if not key_path.exists():
        raise FileNotFoundError(f"密钥文件不存在: {key_path}")

    with key_path.open("rb") as f:
        key = f.read()

    cipher = AES.new(key, AES.MODE_CBC, iv)
    pw = base64.b64decode(pw_base64)
    pw_decrypt = cipher.decrypt(pw)
    password = unpad(pw_decrypt, AES.block_size)

    return password.decode("utf-8")


if __name__ == "__main__":
    password = "你好"
    try:
        pw_base64, iv = aes_encrypt(password)
        print("加密结果:", pw_base64)
        pw = aes_decrypt(pw_base64, iv)
        print("解密结果:", pw)
    except FileNotFoundError as e:
        print(e)
    except Exception as e:
        print("加密/解密出错:", str(e))