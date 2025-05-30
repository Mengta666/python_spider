window = global;
const JsEncrypt = require('jsencrypt');
const fs = require('fs');

window.JSEncrypt = JsEncrypt;

var public_key = fs.readFileSync('./public_key.pem', 'utf8');
var private_key = fs.readFileSync('./private_key.pem', 'utf8');


// 使用 HOOK 劫持加密前数据，由于有实例化对象，需要在原型对象上面进行HOOK
// 取得私钥
const org_setPublicKey = JSEncrypt.prototype.setPublicKey;
JSEncrypt.prototype.setPublicKey = function (key) {
    console.log('setPublicKey', key)
    org_setPublicKey.call(this, key)
}
// 取得加密前数据
const org_encrypt = JSEncrypt.prototype.encrypt;
JSEncrypt.prototype.encrypt = function (plain_text) {
    console.log('encrypt', plain_text)
    return org_encrypt.call(this, plain_text)
}



// 加密
plain_text = '123456';
cipher = new JSEncrypt();
cipher.setPublicKey(public_key);
cipher_text = cipher.encrypt(plain_text)
console.log(cipher_text)

// 解密
cipher.setPrivateKey(private_key);
plain_text = cipher.decrypt(cipher_text)
console.log(plain_text)
