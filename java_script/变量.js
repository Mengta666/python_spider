var a = 1
var b = "string"
var c = null
let d = '0xFF'

console.log(Boolean(d))

var min = Number.MIN_VALUE
var max = Number.MAX_VALUE
console.log(min, max)

a = "1.2"
// 转化为整型数字parseInt，转化为浮点型数字parseFloat
console.log(parseInt(a))
a = "0b100"
console.log(Number(a))

// 转换字符串
var str1 = "a我", str2 = "爱", str3 = "你", str4="666"
var str = str1 + str2 + str3 + str4
console.log(typeof(str1+ str2 + str3 + str4))

var arr = [1,2,3,4,5]
console.log(typeof(arr + ",2"))

// 使用类py输出print(f"{arr}")
console.log(`这是一个列表：${arr}`)

// 切片 (a,b) 包前不包后 a到b-1
console.log(str.substring(0,5))
// 按元素切片，装入列表
console.log(str.split(""))
console.log(str.split("6"))
// 查找某个元素（词）位置，从左到右查到到的第一个，-1为不存在
console.log(str.indexOf("你66"))
// 从右到左查找到的第一个
console.log(str.lastIndexOf("爱"))
// 字符串长度
console.log(str.length)
// 取第几个字符
console.log(str.charAt(2))
// 取某个字母ascii码（UTF-16也行）
console.log(str.charCodeAt(2))
// 获取编码对应的字符
console.log(String.fromCharCode(29233))