// 自执行函数写法1
// a = (function (a,b){
//     return a+b
// })(1,2)
// console.log(a)
// 自执行函数写法2
//  a =    (function func (a,b){
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
// 在对象中使用（这个不是构造器构造的对象）
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
// 就算函数没有形参，js函数内部也有一个arguments(实际上是一个对象（不是构造器构造的对象，类似于py字典）)来接收传入的实参
function func1(){
    console.log(arguments)
}
func1(1,2,3,4,5)

func2()
// 函数提升（即使在func2()调用后面在声明定义函数也可以，因为声明会自动提升到代码顶部，
// 与变量提升类似，但是变量提升只提升声明，不是提升定义的值），同名以最后一个函数为准
function func2(){
    console.log("这是原本的的func2")
}
function func2(){
    console.log("这是新的func2")
}
