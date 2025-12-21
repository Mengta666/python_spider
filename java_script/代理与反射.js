// teacher = {
//     name : "alice"
// }
//
// // 对对象teacher的name属性进行代理，通过代理可以对需要的数据进行拦截，并返回需要的值
// Object.defineProperty(teacher, "name", {
//     set(value){
//         console.log(value)
//         name = value
//     },
//     get(){
//         console.log("this.name")
//         return 'nihao'
//     }
// })

// // 使用反射创建代理，与前Object.defineProperty()创建代理效果相同
// // Reflect.defineProperty(teacher, "name", {
// //     set(value){
// //         console.log(value)
// //         return value
// //     }
// //     ,
// //     get(){
// //         console.log("this.name")
// //         return 'nihao'
// //     }
// // })
//
// teacher.name = "bob"
// console.log(teacher.name)


// 假如使用set(value)函数，并不影响将teacher中的name正确赋值，需要在代理里面再定义一个代理，这个代理用来设置name值
let teacher = { name: "" }; // 初始有一个普通 name 属性

function hookNameProperty(obj) {
    let descriptor = Object.getOwnPropertyDescriptor(obj, "name") || { value: undefined, writable: true };
    let originalValue = descriptor.value; // 保存原始值

    Object.defineProperty(obj, "name", {
        set(value) {
            console.log("Setting name to:", value); // hook 逻辑
            // 临时移除 getter/setter，设置原始值
            Object.defineProperty(obj, "name", {
                value: value,
                writable: true,
                enumerable: true,
                configurable: true
            });
            // 重新定义 getter/setter, 将属性重新赋予set和get方法
            hookNameProperty(obj);
        },
        get() {
            console.log("Getting name"); // hook 逻辑
            let currentDescriptor = Object.getOwnPropertyDescriptor(obj, "name");
            return currentDescriptor && "value" in currentDescriptor ? currentDescriptor.value : originalValue;
        }
    });
}

hookNameProperty(teacher);

// 测试
teacher.name = "Alice"; // 打印 "Setting name to: Alice"
console.log(teacher.name); // 打印 "Getting name"，返回 "Alice"
teacher.name = "Bob"; // 打印 "Setting name to: Bob"
console.log(teacher.name); // 打印 "Getting name"，返回 "Bob"
console.log(teacher); // teacher 对象的 name 属性实际存储了值