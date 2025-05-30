// nmp install crypto-js

const CryptoJs = require('crypto-js')

s = "这是原始数据"

// hook md5
var backup_md5 = CryptoJs.MD5

CryptoJs.MD5 = function (s) {
    console.log(s)
    return backup_md5(s)
}




encrypt = CryptoJs.MD5(s).toString()
console.log(encrypt)

// base64
s = "这是原始数据"
// 转成url编码，再加密
s = encodeURIComponent(s)
console.log(s)
encrypt = btoa(s)
console.log(encrypt)
console.log(atob(encrypt))
console.log(decodeURIComponent(atob(encrypt)))