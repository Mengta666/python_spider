

// 自执行函数写法1
// a = (function (a,b){
//     return a+b
// })(1,2)
// console.log(a)
// 自执行函数写法2
//  a =    (function (a,b){
//     return a+b
// }(1,2))
// console.log(a)
// 自执行函数写法3
// !function (a,b){
//     console.log(a+b)
// }(1,2)

//匿名函数 没有函数名的函数，可以赋值给变量，也可以直接执行（自执行函数）
let func = function (a,b){
    return a+b
}
console.log(func(1,2))
// 在对象中使用
var obj = {
    name : "张三",
    age : 18,
    func : function () {
        console.log(this.name)
        return this.name
    }
}
console.log(obj.func())


// 函数传参时，传对象是引用传递，其他是值传递（对象名实际存储是对象地址）