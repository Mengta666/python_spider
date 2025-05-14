let a = [1,2,-1,3,4,5]

// 取出，删除末尾元素（栈）
a.pop()
console.log(a)
// 放入，末尾放入
a.push(6)
console.log(a)
// 取出开头的元素，shift（列表）
a.shift()
console.log(a)
// 从头放入元素
a.unshift(0,-1)
console.log(a)

// 一次性取出所有元素
// while(a.length){
//     console.log(a.shift())
// }
// 或者用forEach
a.forEach(function (a , b) {
    console.log(a, b)
})

// 排序(默认升序)
a.sort()
console.log(a)
// 逆置
a.reverse()
console.log(a)

// 数组合并成字符串
console.log(a.join(''))
// 两个数组合并concat
console.log(a.concat([7,8,9]))

// 数组切片
// console.log(a.slice(1,4))

// 删除数组指定位置元素（第一位，第二位。。。），返回删除的元素数组
b = a.splice(1,2)
console.log(a)

// 查找元素索引，同样是第一个匹配的
console.log(a.indexOf(-1))


