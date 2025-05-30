teacher = {
    name : "alice"
}

Object.defineProperty(teacher, "name", {
    set(value){
        console.log(value)
        return value
    },
    get(){
        console.log("this.name")
        return this.name
    }
})

teacher.name = "alice"