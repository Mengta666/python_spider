const  CryptoJs = require('crypto-js')

key = CryptoJs.enc.Utf8.parse('1234567890123456')
iv = CryptoJs.enc.Utf8.parse('1234567890123456')

s = 'hello world'


// hook 加密
backup_encrypt = CryptoJs.AES.encrypt
CryptoJs.AES.encrypt = function(s, key, options) {
    console.log(s)
    return backup_encrypt(s, key, options)
}

// 加密
encrypt = CryptoJs.AES.encrypt(s, key, {iv: iv,  mode: CryptoJs.mode.CBC, padding: CryptoJs.pad.Pkcs7})
console.log(encrypt.toString())

// 解密
decrypt = CryptoJs.AES.decrypt(encrypt, key, {iv: iv,  mode: CryptoJs.mode.CBC, padding: CryptoJs.pad.Pkcs7})
console.log(decrypt.toString(CryptoJs.enc.Utf8))