var t = "input is invalid type"
              , r = "finalize already called"
              , n = typeof window == "object"
              , o = n ? window : {};
            o.JS_SHA1_NO_WINDOW && (n = !1);
            var i = !n && typeof self == "object"
            var u = !o.JS_SHA1_NO_ARRAY_BUFFER && typeof ArrayBuffer < "u"
              , l = "0123456789abcdef".split("")
              , c = [-2147483648, 8388608, 32768, 128]
              , f = [24, 16, 8, 0]
              , d = ["hex", "array", "digest", "arrayBuffer"]
              , p = []
              , h = Array.isArray;
            (o.JS_SHA1_NO_NODE_JS || !h) && (h = function(_) {
                return Object.prototype.toString.call(_) === "[object Array]"
            }
            );
            var v = ArrayBuffer.isView;
            u && (o.JS_SHA1_NO_ARRAY_BUFFER_IS_VIEW || !v) && (v = function(_) {
                return typeof _ == "object" && _.buffer && _.buffer.constructor === ArrayBuffer
            }
            );
            var g = function(_) {
                var A = typeof _;
                if (A === "string")
                    return [_, !0];
                if (A !== "object" || _ === null)
                    throw new Error(t);
                if (u && _.constructor === ArrayBuffer)
                    return [new Uint8Array(_), !1];
                if (!h(_) && !v(_))
                    throw new Error(t);
                return [_, !1]
            }
              , m = function(_) {
                return function(A) {
                    return new R(!0).update(A)[_]()
                }
            }
              , y = function() {
                var _ = m("hex");
                a && (_ = x(_)),
                _.create = function() {
                    return new R
                }
                ,
                _.update = function(C) {
                    return _.create().update(C)
                }
                ;
                for (var A = 0; A < d.length; ++A) {
                    var L = d[A];
                    _[L] = m(L)
                }
                return _
            }
              , x = function(_) {
                var A = $u, L = $u.Buffer, C;
                L.from && !o.JS_SHA1_NO_BUFFER_FROM ? C = L.from : C = function(k) {
                    return new L(k)
                }
                ;
                var V = function(k) {
                    if (typeof k == "string")
                        return A.createHash("sha1").update(k, "utf8").digest("hex");
                    if (k == null)
                        throw new Error(t);
                    return k.constructor === ArrayBuffer && (k = new Uint8Array(k)),
                    h(k) || v(k) || k.constructor === L ? A.createHash("sha1").update(C(k)).digest("hex") : _(k)
                };
                return V
            }
              , b = function(_) {
                return function(A, L) {
                    return new P(A,!0).update(L)[_]()
                }
            }
              , T = function() {
                var _ = b("hex");
                _.create = function(C) {
                    return new P(C)
                }
                ,
                _.update = function(C, V) {
                    return _.create(C).update(V)
                }
                ;
                for (var A = 0; A < d.length; ++A) {
                    var L = d[A];
                    _[L] = b(L)
                }
                return _
            };


function R(_) {
                _ ? (p[0] = p[16] = p[1] = p[2] = p[3] = p[4] = p[5] = p[6] = p[7] = p[8] = p[9] = p[10] = p[11] = p[12] = p[13] = p[14] = p[15] = 0,
                this.blocks = p) : this.blocks = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                this.h0 = 1732584193,
                this.h1 = 4023233417,
                this.h2 = 2562383102,
                this.h3 = 271733878,
                this.h4 = 3285377520,
                this.block = this.start = this.bytes = this.hBytes = 0,
                this.finalized = this.hashed = !1,
                this.first = !0
            }
            R.prototype.update = function(_) {
                if (this.finalized)
                    throw new Error(r);
                var A = g(_);
                _ = A[0];
                for (var L = A[1], C, V = 0, k, $ = _.length || 0, F = this.blocks; V < $; ) {
                    if (this.hashed && (this.hashed = !1,
                    F[0] = this.block,
                    this.block = F[16] = F[1] = F[2] = F[3] = F[4] = F[5] = F[6] = F[7] = F[8] = F[9] = F[10] = F[11] = F[12] = F[13] = F[14] = F[15] = 0),
                    L)
                        for (k = this.start; V < $ && k < 64; ++V)
                            C = _.charCodeAt(V),
                            C < 128 ? F[k >>> 2] |= C << f[k++ & 3] : C < 2048 ? (F[k >>> 2] |= (192 | C >>> 6) << f[k++ & 3],
                            F[k >>> 2] |= (128 | C & 63) << f[k++ & 3]) : C < 55296 || C >= 57344 ? (F[k >>> 2] |= (224 | C >>> 12) << f[k++ & 3],
                            F[k >>> 2] |= (128 | C >>> 6 & 63) << f[k++ & 3],
                            F[k >>> 2] |= (128 | C & 63) << f[k++ & 3]) : (C = 65536 + ((C & 1023) << 10 | _.charCodeAt(++V) & 1023),
                            F[k >>> 2] |= (240 | C >>> 18) << f[k++ & 3],
                            F[k >>> 2] |= (128 | C >>> 12 & 63) << f[k++ & 3],
                            F[k >>> 2] |= (128 | C >>> 6 & 63) << f[k++ & 3],
                            F[k >>> 2] |= (128 | C & 63) << f[k++ & 3]);
                    else
                        for (k = this.start; V < $ && k < 64; ++V)
                            F[k >>> 2] |= _[V] << f[k++ & 3];
                    this.lastByteIndex = k,
                    this.bytes += k - this.start,
                    k >= 64 ? (this.block = F[16],
                    this.start = k - 64,
                    this.hash(),
                    this.hashed = !0) : this.start = k
                }
                return this.bytes > 4294967295 && (this.hBytes += this.bytes / 4294967296 << 0,
                this.bytes = this.bytes % 4294967296),
                this
            }
            ,
            R.prototype.finalize = function() {
                if (!this.finalized) {
                    this.finalized = !0;
                    var _ = this.blocks
                      , A = this.lastByteIndex;
                    _[16] = this.block,
                    _[A >>> 2] |= c[A & 3],
                    this.block = _[16],
                    A >= 56 && (this.hashed || this.hash(),
                    _[0] = this.block,
                    _[16] = _[1] = _[2] = _[3] = _[4] = _[5] = _[6] = _[7] = _[8] = _[9] = _[10] = _[11] = _[12] = _[13] = _[14] = _[15] = 0),
                    _[14] = this.hBytes << 3 | this.bytes >>> 29,
                    _[15] = this.bytes << 3,
                    this.hash()
                }
            }
            ,
            R.prototype.hash = function() {
                var _ = this.h0, A = this.h1, L = this.h2, C = this.h3, V = this.h4, k, $, F, j = this.blocks;
                for ($ = 16; $ < 80; ++$)
                    F = j[$ - 3] ^ j[$ - 8] ^ j[$ - 14] ^ j[$ - 16],
                    j[$] = F << 1 | F >>> 31;
                for ($ = 0; $ < 20; $ += 5)
                    k = A & L | ~A & C,
                    F = _ << 5 | _ >>> 27,
                    V = F + k + V + 1518500249 + j[$] << 0,
                    A = A << 30 | A >>> 2,
                    k = _ & A | ~_ & L,
                    F = V << 5 | V >>> 27,
                    C = F + k + C + 1518500249 + j[$ + 1] << 0,
                    _ = _ << 30 | _ >>> 2,
                    k = V & _ | ~V & A,
                    F = C << 5 | C >>> 27,
                    L = F + k + L + 1518500249 + j[$ + 2] << 0,
                    V = V << 30 | V >>> 2,
                    k = C & V | ~C & _,
                    F = L << 5 | L >>> 27,
                    A = F + k + A + 1518500249 + j[$ + 3] << 0,
                    C = C << 30 | C >>> 2,
                    k = L & C | ~L & V,
                    F = A << 5 | A >>> 27,
                    _ = F + k + _ + 1518500249 + j[$ + 4] << 0,
                    L = L << 30 | L >>> 2;
                for (; $ < 40; $ += 5)
                    k = A ^ L ^ C,
                    F = _ << 5 | _ >>> 27,
                    V = F + k + V + 1859775393 + j[$] << 0,
                    A = A << 30 | A >>> 2,
                    k = _ ^ A ^ L,
                    F = V << 5 | V >>> 27,
                    C = F + k + C + 1859775393 + j[$ + 1] << 0,
                    _ = _ << 30 | _ >>> 2,
                    k = V ^ _ ^ A,
                    F = C << 5 | C >>> 27,
                    L = F + k + L + 1859775393 + j[$ + 2] << 0,
                    V = V << 30 | V >>> 2,
                    k = C ^ V ^ _,
                    F = L << 5 | L >>> 27,
                    A = F + k + A + 1859775393 + j[$ + 3] << 0,
                    C = C << 30 | C >>> 2,
                    k = L ^ C ^ V,
                    F = A << 5 | A >>> 27,
                    _ = F + k + _ + 1859775393 + j[$ + 4] << 0,
                    L = L << 30 | L >>> 2;
                for (; $ < 60; $ += 5)
                    k = A & L | A & C | L & C,
                    F = _ << 5 | _ >>> 27,
                    V = F + k + V - 1894007588 + j[$] << 0,
                    A = A << 30 | A >>> 2,
                    k = _ & A | _ & L | A & L,
                    F = V << 5 | V >>> 27,
                    C = F + k + C - 1894007588 + j[$ + 1] << 0,
                    _ = _ << 30 | _ >>> 2,
                    k = V & _ | V & A | _ & A,
                    F = C << 5 | C >>> 27,
                    L = F + k + L - 1894007588 + j[$ + 2] << 0,
                    V = V << 30 | V >>> 2,
                    k = C & V | C & _ | V & _,
                    F = L << 5 | L >>> 27,
                    A = F + k + A - 1894007588 + j[$ + 3] << 0,
                    C = C << 30 | C >>> 2,
                    k = L & C | L & V | C & V,
                    F = A << 5 | A >>> 27,
                    _ = F + k + _ - 1894007588 + j[$ + 4] << 0,
                    L = L << 30 | L >>> 2;
                for (; $ < 80; $ += 5)
                    k = A ^ L ^ C,
                    F = _ << 5 | _ >>> 27,
                    V = F + k + V - 899497514 + j[$] << 0,
                    A = A << 30 | A >>> 2,
                    k = _ ^ A ^ L,
                    F = V << 5 | V >>> 27,
                    C = F + k + C - 899497514 + j[$ + 1] << 0,
                    _ = _ << 30 | _ >>> 2,
                    k = V ^ _ ^ A,
                    F = C << 5 | C >>> 27,
                    L = F + k + L - 899497514 + j[$ + 2] << 0,
                    V = V << 30 | V >>> 2,
                    k = C ^ V ^ _,
                    F = L << 5 | L >>> 27,
                    A = F + k + A - 899497514 + j[$ + 3] << 0,
                    C = C << 30 | C >>> 2,
                    k = L ^ C ^ V,
                    F = A << 5 | A >>> 27,
                    _ = F + k + _ - 899497514 + j[$ + 4] << 0,
                    L = L << 30 | L >>> 2;
                this.h0 = this.h0 + _ << 0,
                this.h1 = this.h1 + A << 0,
                this.h2 = this.h2 + L << 0,
                this.h3 = this.h3 + C << 0,
                this.h4 = this.h4 + V << 0
            }
            ,
            R.prototype.hex = function() {
                this.finalize();
                var _ = this.h0
                  , A = this.h1
                  , L = this.h2
                  , C = this.h3
                  , V = this.h4;
                return l[_ >>> 28 & 15] + l[_ >>> 24 & 15] + l[_ >>> 20 & 15] + l[_ >>> 16 & 15] + l[_ >>> 12 & 15] + l[_ >>> 8 & 15] + l[_ >>> 4 & 15] + l[_ & 15] + l[A >>> 28 & 15] + l[A >>> 24 & 15] + l[A >>> 20 & 15] + l[A >>> 16 & 15] + l[A >>> 12 & 15] + l[A >>> 8 & 15] + l[A >>> 4 & 15] + l[A & 15] + l[L >>> 28 & 15] + l[L >>> 24 & 15] + l[L >>> 20 & 15] + l[L >>> 16 & 15] + l[L >>> 12 & 15] + l[L >>> 8 & 15] + l[L >>> 4 & 15] + l[L & 15] + l[C >>> 28 & 15] + l[C >>> 24 & 15] + l[C >>> 20 & 15] + l[C >>> 16 & 15] + l[C >>> 12 & 15] + l[C >>> 8 & 15] + l[C >>> 4 & 15] + l[C & 15] + l[V >>> 28 & 15] + l[V >>> 24 & 15] + l[V >>> 20 & 15] + l[V >>> 16 & 15] + l[V >>> 12 & 15] + l[V >>> 8 & 15] + l[V >>> 4 & 15] + l[V & 15]
            }
            ,
            R.prototype.toString = R.prototype.hex,
            R.prototype.digest = function() {
                this.finalize();
                var _ = this.h0
                  , A = this.h1
                  , L = this.h2
                  , C = this.h3
                  , V = this.h4;
                return [_ >>> 24 & 255, _ >>> 16 & 255, _ >>> 8 & 255, _ & 255, A >>> 24 & 255, A >>> 16 & 255, A >>> 8 & 255, A & 255, L >>> 24 & 255, L >>> 16 & 255, L >>> 8 & 255, L & 255, C >>> 24 & 255, C >>> 16 & 255, C >>> 8 & 255, C & 255, V >>> 24 & 255, V >>> 16 & 255, V >>> 8 & 255, V & 255]
            }
            ,
            R.prototype.array = R.prototype.digest,
            R.prototype.arrayBuffer = function() {
                this.finalize();
                var _ = new ArrayBuffer(20)
                  , A = new DataView(_);
                return A.setUint32(0, this.h0),
                A.setUint32(4, this.h1),
                A.setUint32(8, this.h2),
                A.setUint32(12, this.h3),
                A.setUint32(16, this.h4),
                _
            }

A = '{"url":"https://pan.baidu.com/s/1ma-aC5obs1BYU2vG9co0fw","surl":"1ma-aC5obs1BYU2vG9co0fw","pwd":"2i0o","dir":"/","parse_password":"12212"}'
function get_rand1_3(path, rand2){
    path = path.toString()
    var rand1 = new R(true).update(path)["hex"]()
    var rand3 = new R(true).update(rand2)["hex"]()
    return [rand1, rand3]
}

