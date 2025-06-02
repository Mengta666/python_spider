// teacher = {
//     name : "alice"
// }
//
// Object.defineProperty(teacher, "name", {
//     set(value){
//         console.log(value)
//         return value
//     },
//     get(){
//         console.log("this.name")
//         return this.name
//     }
// })
//
// teacher.name = "alice"

// 可以在浏览器中运行
// const Person = {
//     name : "alice",
//     a: () => console.log("这是函数Person")
// }
// function test( age = 18){
//     console.log( this.name, age)
//     this.age =  age
// }
// test.call( Person, 18)
// console.log(Person.age)