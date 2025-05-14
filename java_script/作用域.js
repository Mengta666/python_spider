
// 全局作用域
var  a = 3
// 块级作用域 函数内
function test(){
    a = 1;        // 全局变量不加var
    console.log(a)
}
// 语句作用域
test()
console.log(a)

// var优先级查找顺序：块级作用域 > 语句作用域 > 全局作用域
// 全局包含语句，语句包含块级

// 闭包
var perry
// 一般无法访问函数内部子函数（闭包）
function test(){
    var b = 1;
    function test1(){
        console.log(b)
    }
    perry  = test1
}
perry()
