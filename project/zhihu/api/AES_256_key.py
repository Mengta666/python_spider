import os
import configparser
from pathlib import Path
from Crypto.Random import get_random_bytes

config = configparser.ConfigParser()
config.read(r"E:\python\spider\project\zhihu\cnf\api.cnf", encoding="utf-8")
key_path = Path(config['keys']['path'])


if __name__ == "__main__":
    print("目标文件路径:", key_path)

    # 检查文件是否存在
    if key_path.exists():
        print("keys.bin文件已存在")
        exit()

    try:
        # 创建keys目录
        key_dir = key_path.cwd() / "keys"
        key_dir.mkdir()

        # 生成AES-256密钥（32字节）
        keys = get_random_bytes(32)
        # 写入密钥文件
        with key_path.open("wb") as f:
            f.write(keys)

        # 验证文件是否创建
        if key_path.exists():
            print("密钥文件已成功创建:", key_path)
        else:
            print("密钥文件创建失败")
    except PermissionError:
        print("错误：无权限在", key_dir, "创建文件，请检查目录权限或以管理员身份运行")
    except Exception as e:
        print("创建密钥文件时出错:", str(e))