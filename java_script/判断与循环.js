
a = 10

if (a>5){
    console.log("大于5")
}else{
    console.log("小于5")
}


a = [1,2,3]
// 同C语言一样
for (i in a)
{
    switch (a[i]) {
        case 1:
            console.log("1")
            break
        case 2:
            console.log("2")
            break
        default:
            console.log("default")
    }
}

// 同c
// for( i=0;i<=10;i++)
// {
//     console.log(i)
// }
//
// while  (i<=10)
// {
//     console.log(i)
//     i++
// }
//
// do{
//     console.log(i)
//     i++
// }while(i<=10)