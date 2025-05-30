// 使用构造器创造对象

// 实例对象
function Teacher(name,age,major){
    this.name = name;
    this.age = age;
    this.major = major;
    this.teacher = function(){
        console.log(this.name + "老师教" + this.major)
    }
}

// 实例化后的对象单独有存储空间，后续再在原型对象中添加方法不会影响已经实例化的对象
// 这与前面直接用 var obj = {} 创建的对象显然不一样（这种对象原来就分配了内存），obj1 = obj实际上是共享内存，并没有新申请内存
test =  new Teacher("张三",18,"C++")
test.teacher()
// test.sport()

// 类似于继承，在实例对象的构造器中添加新方法，生成的对象构造器叫做原型对象，
// 所谓的原型对象Teacher.prototype就是实例化对象添加新方法后的对象
Teacher.prototype.sport = function(){
    console.log(this.name + "老师喜欢运动")
}
// 当实例对象中已经有sport方法时，实例化后的对象（perry）会优先调用实例对象中的方法，而不是原型对象中的方法

// 原型对象Teacher.prototype
Teacher.prototype.swim = function(){
    console.log(this.name + "老师喜欢游泳")
}

// perry实际是原型对象实例化后的结果
perry = new Teacher("perry",18,"C++")
perry.name = "李四"
perry.teacher()
perry.sport()
perry.swim()
// 使用__proto__来查询当前实例化对象的父实例化对象，所有的自定义对象都是由Object创建的
console.log(perry.__proto__)

