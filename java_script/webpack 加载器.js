! function (t){
    // 加载器
    function e(s){
        if (i[s])
            return  i[s].exports;
        var n = i[s] = {
            id : s,
            loader : false,
            exports : {}
        }
        return t[s].call(n.exports,n,n.exports,e), n.loader = true, n.exports
    }
    global.e = e
    var i  = {}
    // e('a')

}( {
    a : function a(a,b,c){
        console.log("这是函数a")
        c('b')
    },
    b : function b(a,b,c){
        console.log("这是函数b")
    }
})

global.e( 'a')

