var dt = typeof global == "object" && global && global.Object === Object && global, rr = typeof self == "object" && self && self.Object === Object && self, E = dt || rr || Function("return this")(), w = E.Symbol, _t = Object.prototype, nr = _t.hasOwnProperty, or = _t.toString, H = w ? w.toStringTag : void 0;
function ir(e) {
  var t = nr.call(e, H), r = e[H];
  try {
    e[H] = void 0;
    var n = !0;
  } catch {
  }
  var i = or.call(e);
  return n && (t ? e[H] = r : delete e[H]), i;
}
var ar = Object.prototype, sr = ar.toString;
function ur(e) {
  return sr.call(e);
}
var lr = "[object Null]", cr = "[object Undefined]", Le = w ? w.toStringTag : void 0;
function D(e) {
  return e == null ? e === void 0 ? cr : lr : Le && Le in Object(e) ? ir(e) : ur(e);
}
function I(e) {
  return e != null && typeof e == "object";
}
var fr = "[object Symbol]";
function Te(e) {
  return typeof e == "symbol" || I(e) && D(e) == fr;
}
function ht(e, t) {
  for (var r = -1, n = e == null ? 0 : e.length, i = Array(n); ++r < n; )
    i[r] = t(e[r], r, e);
  return i;
}
var x = Array.isArray, De = w ? w.prototype : void 0, Ne = De ? De.toString : void 0;
function bt(e) {
  if (typeof e == "string")
    return e;
  if (x(e))
    return ht(e, bt) + "";
  if (Te(e))
    return Ne ? Ne.call(e) : "";
  var t = e + "";
  return t == "0" && 1 / e == -1 / 0 ? "-0" : t;
}
function z(e) {
  var t = typeof e;
  return e != null && (t == "object" || t == "function");
}
function yt(e) {
  return e;
}
var pr = "[object AsyncFunction]", gr = "[object Function]", dr = "[object GeneratorFunction]", _r = "[object Proxy]";
function mt(e) {
  if (!z(e))
    return !1;
  var t = D(e);
  return t == gr || t == dr || t == pr || t == _r;
}
var ce = E["__core-js_shared__"], Ke = function() {
  var e = /[^.]+$/.exec(ce && ce.keys && ce.keys.IE_PROTO || "");
  return e ? "Symbol(src)_1." + e : "";
}();
function hr(e) {
  return !!Ke && Ke in e;
}
var br = Function.prototype, yr = br.toString;
function N(e) {
  if (e != null) {
    try {
      return yr.call(e);
    } catch {
    }
    try {
      return e + "";
    } catch {
    }
  }
  return "";
}
var mr = /[\\^$.*+?()[\]{}|]/g, vr = /^\[object .+?Constructor\]$/, Tr = Function.prototype, Pr = Object.prototype, Or = Tr.toString, wr = Pr.hasOwnProperty, Ar = RegExp("^" + Or.call(wr).replace(mr, "\\$&").replace(/hasOwnProperty|(function).*?(?=\\\()| for .+?(?=\\\])/g, "$1.*?") + "$");
function $r(e) {
  if (!z(e) || hr(e))
    return !1;
  var t = mt(e) ? Ar : vr;
  return t.test(N(e));
}
function Sr(e, t) {
  return e == null ? void 0 : e[t];
}
function K(e, t) {
  var r = Sr(e, t);
  return $r(r) ? r : void 0;
}
var _e = K(E, "WeakMap");
function xr(e, t, r) {
  switch (r.length) {
    case 0:
      return e.call(t);
    case 1:
      return e.call(t, r[0]);
    case 2:
      return e.call(t, r[0], r[1]);
    case 3:
      return e.call(t, r[0], r[1], r[2]);
  }
  return e.apply(t, r);
}
var Cr = 800, jr = 16, Er = Date.now;
function Ir(e) {
  var t = 0, r = 0;
  return function() {
    var n = Er(), i = jr - (n - r);
    if (r = n, i > 0) {
      if (++t >= Cr)
        return arguments[0];
    } else
      t = 0;
    return e.apply(void 0, arguments);
  };
}
function Mr(e) {
  return function() {
    return e;
  };
}
var te = function() {
  try {
    var e = K(Object, "defineProperty");
    return e({}, "", {}), e;
  } catch {
  }
}(), Fr = te ? function(e, t) {
  return te(e, "toString", {
    configurable: !0,
    enumerable: !1,
    value: Mr(t),
    writable: !0
  });
} : yt, Rr = Ir(Fr);
function Lr(e, t) {
  for (var r = -1, n = e == null ? 0 : e.length; ++r < n && t(e[r], r, e) !== !1; )
    ;
  return e;
}
var Dr = 9007199254740991, Nr = /^(?:0|[1-9]\d*)$/;
function vt(e, t) {
  var r = typeof e;
  return t = t ?? Dr, !!t && (r == "number" || r != "symbol" && Nr.test(e)) && e > -1 && e % 1 == 0 && e < t;
}
function Pe(e, t, r) {
  t == "__proto__" && te ? te(e, t, {
    configurable: !0,
    enumerable: !0,
    value: r,
    writable: !0
  }) : e[t] = r;
}
function Oe(e, t) {
  return e === t || e !== e && t !== t;
}
var Kr = Object.prototype, Ur = Kr.hasOwnProperty;
function Tt(e, t, r) {
  var n = e[t];
  (!(Ur.call(e, t) && Oe(n, r)) || r === void 0 && !(t in e)) && Pe(e, t, r);
}
function Gr(e, t, r, n) {
  var i = !r;
  r || (r = {});
  for (var o = -1, a = t.length; ++o < a; ) {
    var s = t[o], u = void 0;
    u === void 0 && (u = e[s]), i ? Pe(r, s, u) : Tt(r, s, u);
  }
  return r;
}
var Ue = Math.max;
function Br(e, t, r) {
  return t = Ue(t === void 0 ? e.length - 1 : t, 0), function() {
    for (var n = arguments, i = -1, o = Ue(n.length - t, 0), a = Array(o); ++i < o; )
      a[i] = n[t + i];
    i = -1;
    for (var s = Array(t + 1); ++i < t; )
      s[i] = n[i];
    return s[t] = r(a), xr(e, this, s);
  };
}
var zr = 9007199254740991;
function we(e) {
  return typeof e == "number" && e > -1 && e % 1 == 0 && e <= zr;
}
function Pt(e) {
  return e != null && we(e.length) && !mt(e);
}
var Hr = Object.prototype;
function Ot(e) {
  var t = e && e.constructor, r = typeof t == "function" && t.prototype || Hr;
  return e === r;
}
function qr(e, t) {
  for (var r = -1, n = Array(e); ++r < e; )
    n[r] = t(r);
  return n;
}
var Jr = "[object Arguments]";
function Ge(e) {
  return I(e) && D(e) == Jr;
}
var wt = Object.prototype, Xr = wt.hasOwnProperty, Yr = wt.propertyIsEnumerable, Ae = Ge(/* @__PURE__ */ function() {
  return arguments;
}()) ? Ge : function(e) {
  return I(e) && Xr.call(e, "callee") && !Yr.call(e, "callee");
};
function Zr() {
  return !1;
}
var At = typeof exports == "object" && exports && !exports.nodeType && exports, Be = At && typeof module == "object" && module && !module.nodeType && module, Wr = Be && Be.exports === At, ze = Wr ? E.Buffer : void 0, Qr = ze ? ze.isBuffer : void 0, re = Qr || Zr, Vr = "[object Arguments]", kr = "[object Array]", en = "[object Boolean]", tn = "[object Date]", rn = "[object Error]", nn = "[object Function]", on = "[object Map]", an = "[object Number]", sn = "[object Object]", un = "[object RegExp]", ln = "[object Set]", cn = "[object String]", fn = "[object WeakMap]", pn = "[object ArrayBuffer]", gn = "[object DataView]", dn = "[object Float32Array]", _n = "[object Float64Array]", hn = "[object Int8Array]", bn = "[object Int16Array]", yn = "[object Int32Array]", mn = "[object Uint8Array]", vn = "[object Uint8ClampedArray]", Tn = "[object Uint16Array]", Pn = "[object Uint32Array]", m = {};
m[dn] = m[_n] = m[hn] = m[bn] = m[yn] = m[mn] = m[vn] = m[Tn] = m[Pn] = !0;
m[Vr] = m[kr] = m[pn] = m[en] = m[gn] = m[tn] = m[rn] = m[nn] = m[on] = m[an] = m[sn] = m[un] = m[ln] = m[cn] = m[fn] = !1;
function On(e) {
  return I(e) && we(e.length) && !!m[D(e)];
}
function $e(e) {
  return function(t) {
    return e(t);
  };
}
var $t = typeof exports == "object" && exports && !exports.nodeType && exports, q = $t && typeof module == "object" && module && !module.nodeType && module, wn = q && q.exports === $t, fe = wn && dt.process, B = function() {
  try {
    var e = q && q.require && q.require("util").types;
    return e || fe && fe.binding && fe.binding("util");
  } catch {
  }
}(), He = B && B.isTypedArray, St = He ? $e(He) : On, An = Object.prototype, $n = An.hasOwnProperty;
function xt(e, t) {
  var r = x(e), n = !r && Ae(e), i = !r && !n && re(e), o = !r && !n && !i && St(e), a = r || n || i || o, s = a ? qr(e.length, String) : [], u = s.length;
  for (var l in e)
    (t || $n.call(e, l)) && !(a && // Safari 9 has enumerable `arguments.length` in strict mode.
    (l == "length" || // Node.js 0.10 has enumerable non-index properties on buffers.
    i && (l == "offset" || l == "parent") || // PhantomJS 2 has enumerable non-index properties on typed arrays.
    o && (l == "buffer" || l == "byteLength" || l == "byteOffset") || // Skip index properties.
    vt(l, u))) && s.push(l);
  return s;
}
function Ct(e, t) {
  return function(r) {
    return e(t(r));
  };
}
var Sn = Ct(Object.keys, Object), xn = Object.prototype, Cn = xn.hasOwnProperty;
function jn(e) {
  if (!Ot(e))
    return Sn(e);
  var t = [];
  for (var r in Object(e))
    Cn.call(e, r) && r != "constructor" && t.push(r);
  return t;
}
function Se(e) {
  return Pt(e) ? xt(e) : jn(e);
}
function En(e) {
  var t = [];
  if (e != null)
    for (var r in Object(e))
      t.push(r);
  return t;
}
var In = Object.prototype, Mn = In.hasOwnProperty;
function Fn(e) {
  if (!z(e))
    return En(e);
  var t = Ot(e), r = [];
  for (var n in e)
    n == "constructor" && (t || !Mn.call(e, n)) || r.push(n);
  return r;
}
function Rn(e) {
  return Pt(e) ? xt(e, !0) : Fn(e);
}
var Ln = /\.|\[(?:[^[\]]*|(["'])(?:(?!\1)[^\\]|\\.)*?\1)\]/, Dn = /^\w*$/;
function xe(e, t) {
  if (x(e))
    return !1;
  var r = typeof e;
  return r == "number" || r == "symbol" || r == "boolean" || e == null || Te(e) ? !0 : Dn.test(e) || !Ln.test(e) || t != null && e in Object(t);
}
var J = K(Object, "create");
function Nn() {
  this.__data__ = J ? J(null) : {}, this.size = 0;
}
function Kn(e) {
  var t = this.has(e) && delete this.__data__[e];
  return this.size -= t ? 1 : 0, t;
}
var Un = "__lodash_hash_undefined__", Gn = Object.prototype, Bn = Gn.hasOwnProperty;
function zn(e) {
  var t = this.__data__;
  if (J) {
    var r = t[e];
    return r === Un ? void 0 : r;
  }
  return Bn.call(t, e) ? t[e] : void 0;
}
var Hn = Object.prototype, qn = Hn.hasOwnProperty;
function Jn(e) {
  var t = this.__data__;
  return J ? t[e] !== void 0 : qn.call(t, e);
}
var Xn = "__lodash_hash_undefined__";
function Yn(e, t) {
  var r = this.__data__;
  return this.size += this.has(e) ? 0 : 1, r[e] = J && t === void 0 ? Xn : t, this;
}
function L(e) {
  var t = -1, r = e == null ? 0 : e.length;
  for (this.clear(); ++t < r; ) {
    var n = e[t];
    this.set(n[0], n[1]);
  }
}
L.prototype.clear = Nn;
L.prototype.delete = Kn;
L.prototype.get = zn;
L.prototype.has = Jn;
L.prototype.set = Yn;
function Zn() {
  this.__data__ = [], this.size = 0;
}
function ae(e, t) {
  for (var r = e.length; r--; )
    if (Oe(e[r][0], t))
      return r;
  return -1;
}
var Wn = Array.prototype, Qn = Wn.splice;
function Vn(e) {
  var t = this.__data__, r = ae(t, e);
  if (r < 0)
    return !1;
  var n = t.length - 1;
  return r == n ? t.pop() : Qn.call(t, r, 1), --this.size, !0;
}
function kn(e) {
  var t = this.__data__, r = ae(t, e);
  return r < 0 ? void 0 : t[r][1];
}
function eo(e) {
  return ae(this.__data__, e) > -1;
}
function to(e, t) {
  var r = this.__data__, n = ae(r, e);
  return n < 0 ? (++this.size, r.push([e, t])) : r[n][1] = t, this;
}
function M(e) {
  var t = -1, r = e == null ? 0 : e.length;
  for (this.clear(); ++t < r; ) {
    var n = e[t];
    this.set(n[0], n[1]);
  }
}
M.prototype.clear = Zn;
M.prototype.delete = Vn;
M.prototype.get = kn;
M.prototype.has = eo;
M.prototype.set = to;
var X = K(E, "Map");
function ro() {
  this.size = 0, this.__data__ = {
    hash: new L(),
    map: new (X || M)(),
    string: new L()
  };
}
function no(e) {
  var t = typeof e;
  return t == "string" || t == "number" || t == "symbol" || t == "boolean" ? e !== "__proto__" : e === null;
}
function se(e, t) {
  var r = e.__data__;
  return no(t) ? r[typeof t == "string" ? "string" : "hash"] : r.map;
}
function oo(e) {
  var t = se(this, e).delete(e);
  return this.size -= t ? 1 : 0, t;
}
function io(e) {
  return se(this, e).get(e);
}
function ao(e) {
  return se(this, e).has(e);
}
function so(e, t) {
  var r = se(this, e), n = r.size;
  return r.set(e, t), this.size += r.size == n ? 0 : 1, this;
}
function F(e) {
  var t = -1, r = e == null ? 0 : e.length;
  for (this.clear(); ++t < r; ) {
    var n = e[t];
    this.set(n[0], n[1]);
  }
}
F.prototype.clear = ro;
F.prototype.delete = oo;
F.prototype.get = io;
F.prototype.has = ao;
F.prototype.set = so;
var uo = "Expected a function";
function Ce(e, t) {
  if (typeof e != "function" || t != null && typeof t != "function")
    throw new TypeError(uo);
  var r = function() {
    var n = arguments, i = t ? t.apply(this, n) : n[0], o = r.cache;
    if (o.has(i))
      return o.get(i);
    var a = e.apply(this, n);
    return r.cache = o.set(i, a) || o, a;
  };
  return r.cache = new (Ce.Cache || F)(), r;
}
Ce.Cache = F;
var lo = 500;
function co(e) {
  var t = Ce(e, function(n) {
    return r.size === lo && r.clear(), n;
  }), r = t.cache;
  return t;
}
var fo = /[^.[\]]+|\[(?:(-?\d+(?:\.\d+)?)|(["'])((?:(?!\2)[^\\]|\\.)*?)\2)\]|(?=(?:\.|\[\])(?:\.|\[\]|$))/g, po = /\\(\\)?/g, go = co(function(e) {
  var t = [];
  return e.charCodeAt(0) === 46 && t.push(""), e.replace(fo, function(r, n, i, o) {
    t.push(i ? o.replace(po, "$1") : n || r);
  }), t;
});
function _o(e) {
  return e == null ? "" : bt(e);
}
function ue(e, t) {
  return x(e) ? e : xe(e, t) ? [e] : go(_o(e));
}
function Z(e) {
  if (typeof e == "string" || Te(e))
    return e;
  var t = e + "";
  return t == "0" && 1 / e == -1 / 0 ? "-0" : t;
}
function je(e, t) {
  t = ue(t, e);
  for (var r = 0, n = t.length; e != null && r < n; )
    e = e[Z(t[r++])];
  return r && r == n ? e : void 0;
}
function ho(e, t, r) {
  var n = e == null ? void 0 : je(e, t);
  return n === void 0 ? r : n;
}
function Ee(e, t) {
  for (var r = -1, n = t.length, i = e.length; ++r < n; )
    e[i + r] = t[r];
  return e;
}
var qe = w ? w.isConcatSpreadable : void 0;
function bo(e) {
  return x(e) || Ae(e) || !!(qe && e && e[qe]);
}
function yo(e, t, r, n, i) {
  var o = -1, a = e.length;
  for (r || (r = bo), i || (i = []); ++o < a; ) {
    var s = e[o];
    r(s) ? Ee(i, s) : i[i.length] = s;
  }
  return i;
}
function mo(e) {
  var t = e == null ? 0 : e.length;
  return t ? yo(e) : [];
}
function vo(e) {
  return Rr(Br(e, void 0, mo), e + "");
}
var jt = Ct(Object.getPrototypeOf, Object), To = "[object Object]", Po = Function.prototype, Oo = Object.prototype, Et = Po.toString, wo = Oo.hasOwnProperty, Ao = Et.call(Object);
function he(e) {
  if (!I(e) || D(e) != To)
    return !1;
  var t = jt(e);
  if (t === null)
    return !0;
  var r = wo.call(t, "constructor") && t.constructor;
  return typeof r == "function" && r instanceof r && Et.call(r) == Ao;
}
function $o(e, t, r) {
  var n = -1, i = e.length;
  t < 0 && (t = -t > i ? 0 : i + t), r = r > i ? i : r, r < 0 && (r += i), i = t > r ? 0 : r - t >>> 0, t >>>= 0;
  for (var o = Array(i); ++n < i; )
    o[n] = e[n + t];
  return o;
}
function So() {
  this.__data__ = new M(), this.size = 0;
}
function xo(e) {
  var t = this.__data__, r = t.delete(e);
  return this.size = t.size, r;
}
function Co(e) {
  return this.__data__.get(e);
}
function jo(e) {
  return this.__data__.has(e);
}
var Eo = 200;
function Io(e, t) {
  var r = this.__data__;
  if (r instanceof M) {
    var n = r.__data__;
    if (!X || n.length < Eo - 1)
      return n.push([e, t]), this.size = ++r.size, this;
    r = this.__data__ = new F(n);
  }
  return r.set(e, t), this.size = r.size, this;
}
function j(e) {
  var t = this.__data__ = new M(e);
  this.size = t.size;
}
j.prototype.clear = So;
j.prototype.delete = xo;
j.prototype.get = Co;
j.prototype.has = jo;
j.prototype.set = Io;
var It = typeof exports == "object" && exports && !exports.nodeType && exports, Je = It && typeof module == "object" && module && !module.nodeType && module, Mo = Je && Je.exports === It, Xe = Mo ? E.Buffer : void 0;
Xe && Xe.allocUnsafe;
function Fo(e, t) {
  return e.slice();
}
function Ro(e, t) {
  for (var r = -1, n = e == null ? 0 : e.length, i = 0, o = []; ++r < n; ) {
    var a = e[r];
    t(a, r, e) && (o[i++] = a);
  }
  return o;
}
function Mt() {
  return [];
}
var Lo = Object.prototype, Do = Lo.propertyIsEnumerable, Ye = Object.getOwnPropertySymbols, Ft = Ye ? function(e) {
  return e == null ? [] : (e = Object(e), Ro(Ye(e), function(t) {
    return Do.call(e, t);
  }));
} : Mt, No = Object.getOwnPropertySymbols, Ko = No ? function(e) {
  for (var t = []; e; )
    Ee(t, Ft(e)), e = jt(e);
  return t;
} : Mt;
function Rt(e, t, r) {
  var n = t(e);
  return x(e) ? n : Ee(n, r(e));
}
function Ze(e) {
  return Rt(e, Se, Ft);
}
function Lt(e) {
  return Rt(e, Rn, Ko);
}
var be = K(E, "DataView"), ye = K(E, "Promise"), me = K(E, "Set"), We = "[object Map]", Uo = "[object Object]", Qe = "[object Promise]", Ve = "[object Set]", ke = "[object WeakMap]", et = "[object DataView]", Go = N(be), Bo = N(X), zo = N(ye), Ho = N(me), qo = N(_e), S = D;
(be && S(new be(new ArrayBuffer(1))) != et || X && S(new X()) != We || ye && S(ye.resolve()) != Qe || me && S(new me()) != Ve || _e && S(new _e()) != ke) && (S = function(e) {
  var t = D(e), r = t == Uo ? e.constructor : void 0, n = r ? N(r) : "";
  if (n)
    switch (n) {
      case Go:
        return et;
      case Bo:
        return We;
      case zo:
        return Qe;
      case Ho:
        return Ve;
      case qo:
        return ke;
    }
  return t;
});
var Jo = Object.prototype, Xo = Jo.hasOwnProperty;
function Yo(e) {
  var t = e.length, r = new e.constructor(t);
  return t && typeof e[0] == "string" && Xo.call(e, "index") && (r.index = e.index, r.input = e.input), r;
}
var ne = E.Uint8Array;
function Ie(e) {
  var t = new e.constructor(e.byteLength);
  return new ne(t).set(new ne(e)), t;
}
function Zo(e, t) {
  var r = Ie(e.buffer);
  return new e.constructor(r, e.byteOffset, e.byteLength);
}
var Wo = /\w*$/;
function Qo(e) {
  var t = new e.constructor(e.source, Wo.exec(e));
  return t.lastIndex = e.lastIndex, t;
}
var tt = w ? w.prototype : void 0, rt = tt ? tt.valueOf : void 0;
function Vo(e) {
  return rt ? Object(rt.call(e)) : {};
}
function ko(e, t) {
  var r = Ie(e.buffer);
  return new e.constructor(r, e.byteOffset, e.length);
}
var ei = "[object Boolean]", ti = "[object Date]", ri = "[object Map]", ni = "[object Number]", oi = "[object RegExp]", ii = "[object Set]", ai = "[object String]", si = "[object Symbol]", ui = "[object ArrayBuffer]", li = "[object DataView]", ci = "[object Float32Array]", fi = "[object Float64Array]", pi = "[object Int8Array]", gi = "[object Int16Array]", di = "[object Int32Array]", _i = "[object Uint8Array]", hi = "[object Uint8ClampedArray]", bi = "[object Uint16Array]", yi = "[object Uint32Array]";
function mi(e, t, r) {
  var n = e.constructor;
  switch (t) {
    case ui:
      return Ie(e);
    case ei:
    case ti:
      return new n(+e);
    case li:
      return Zo(e);
    case ci:
    case fi:
    case pi:
    case gi:
    case di:
    case _i:
    case hi:
    case bi:
    case yi:
      return ko(e);
    case ri:
      return new n();
    case ni:
    case ai:
      return new n(e);
    case oi:
      return Qo(e);
    case ii:
      return new n();
    case si:
      return Vo(e);
  }
}
var vi = "[object Map]";
function Ti(e) {
  return I(e) && S(e) == vi;
}
var nt = B && B.isMap, Pi = nt ? $e(nt) : Ti, Oi = "[object Set]";
function wi(e) {
  return I(e) && S(e) == Oi;
}
var ot = B && B.isSet, Ai = ot ? $e(ot) : wi, Dt = "[object Arguments]", $i = "[object Array]", Si = "[object Boolean]", xi = "[object Date]", Ci = "[object Error]", Nt = "[object Function]", ji = "[object GeneratorFunction]", Ei = "[object Map]", Ii = "[object Number]", Kt = "[object Object]", Mi = "[object RegExp]", Fi = "[object Set]", Ri = "[object String]", Li = "[object Symbol]", Di = "[object WeakMap]", Ni = "[object ArrayBuffer]", Ki = "[object DataView]", Ui = "[object Float32Array]", Gi = "[object Float64Array]", Bi = "[object Int8Array]", zi = "[object Int16Array]", Hi = "[object Int32Array]", qi = "[object Uint8Array]", Ji = "[object Uint8ClampedArray]", Xi = "[object Uint16Array]", Yi = "[object Uint32Array]", y = {};
y[Dt] = y[$i] = y[Ni] = y[Ki] = y[Si] = y[xi] = y[Ui] = y[Gi] = y[Bi] = y[zi] = y[Hi] = y[Ei] = y[Ii] = y[Kt] = y[Mi] = y[Fi] = y[Ri] = y[Li] = y[qi] = y[Ji] = y[Xi] = y[Yi] = !0;
y[Ci] = y[Nt] = y[Di] = !1;
function k(e, t, r, n, i, o) {
  var a;
  if (r && (a = i ? r(e, n, i, o) : r(e)), a !== void 0)
    return a;
  if (!z(e))
    return e;
  var s = x(e);
  if (s)
    a = Yo(e);
  else {
    var u = S(e), l = u == Nt || u == ji;
    if (re(e))
      return Fo(e);
    if (u == Kt || u == Dt || l && !i)
      a = {};
    else {
      if (!y[u])
        return i ? e : {};
      a = mi(e, u);
    }
  }
  o || (o = new j());
  var d = o.get(e);
  if (d)
    return d;
  o.set(e, a), Ai(e) ? e.forEach(function(f) {
    a.add(k(f, t, r, f, e, o));
  }) : Pi(e) && e.forEach(function(f, h) {
    a.set(h, k(f, t, r, h, e, o));
  });
  var _ = Lt, c = s ? void 0 : _(e);
  return Lr(c || e, function(f, h) {
    c && (h = f, f = e[h]), Tt(a, h, k(f, t, r, h, e, o));
  }), a;
}
var Zi = "__lodash_hash_undefined__";
function Wi(e) {
  return this.__data__.set(e, Zi), this;
}
function Qi(e) {
  return this.__data__.has(e);
}
function oe(e) {
  var t = -1, r = e == null ? 0 : e.length;
  for (this.__data__ = new F(); ++t < r; )
    this.add(e[t]);
}
oe.prototype.add = oe.prototype.push = Wi;
oe.prototype.has = Qi;
function Vi(e, t) {
  for (var r = -1, n = e == null ? 0 : e.length; ++r < n; )
    if (t(e[r], r, e))
      return !0;
  return !1;
}
function ki(e, t) {
  return e.has(t);
}
var ea = 1, ta = 2;
function Ut(e, t, r, n, i, o) {
  var a = r & ea, s = e.length, u = t.length;
  if (s != u && !(a && u > s))
    return !1;
  var l = o.get(e), d = o.get(t);
  if (l && d)
    return l == t && d == e;
  var _ = -1, c = !0, f = r & ta ? new oe() : void 0;
  for (o.set(e, t), o.set(t, e); ++_ < s; ) {
    var h = e[_], b = t[_];
    if (n)
      var p = a ? n(b, h, _, t, e, o) : n(h, b, _, e, t, o);
    if (p !== void 0) {
      if (p)
        continue;
      c = !1;
      break;
    }
    if (f) {
      if (!Vi(t, function(v, P) {
        if (!ki(f, P) && (h === v || i(h, v, r, n, o)))
          return f.push(P);
      })) {
        c = !1;
        break;
      }
    } else if (!(h === b || i(h, b, r, n, o))) {
      c = !1;
      break;
    }
  }
  return o.delete(e), o.delete(t), c;
}
function ra(e) {
  var t = -1, r = Array(e.size);
  return e.forEach(function(n, i) {
    r[++t] = [i, n];
  }), r;
}
function na(e) {
  var t = -1, r = Array(e.size);
  return e.forEach(function(n) {
    r[++t] = n;
  }), r;
}
var oa = 1, ia = 2, aa = "[object Boolean]", sa = "[object Date]", ua = "[object Error]", la = "[object Map]", ca = "[object Number]", fa = "[object RegExp]", pa = "[object Set]", ga = "[object String]", da = "[object Symbol]", _a = "[object ArrayBuffer]", ha = "[object DataView]", it = w ? w.prototype : void 0, pe = it ? it.valueOf : void 0;
function ba(e, t, r, n, i, o, a) {
  switch (r) {
    case ha:
      if (e.byteLength != t.byteLength || e.byteOffset != t.byteOffset)
        return !1;
      e = e.buffer, t = t.buffer;
    case _a:
      return !(e.byteLength != t.byteLength || !o(new ne(e), new ne(t)));
    case aa:
    case sa:
    case ca:
      return Oe(+e, +t);
    case ua:
      return e.name == t.name && e.message == t.message;
    case fa:
    case ga:
      return e == t + "";
    case la:
      var s = ra;
    case pa:
      var u = n & oa;
      if (s || (s = na), e.size != t.size && !u)
        return !1;
      var l = a.get(e);
      if (l)
        return l == t;
      n |= ia, a.set(e, t);
      var d = Ut(s(e), s(t), n, i, o, a);
      return a.delete(e), d;
    case da:
      if (pe)
        return pe.call(e) == pe.call(t);
  }
  return !1;
}
var ya = 1, ma = Object.prototype, va = ma.hasOwnProperty;
function Ta(e, t, r, n, i, o) {
  var a = r & ya, s = Ze(e), u = s.length, l = Ze(t), d = l.length;
  if (u != d && !a)
    return !1;
  for (var _ = u; _--; ) {
    var c = s[_];
    if (!(a ? c in t : va.call(t, c)))
      return !1;
  }
  var f = o.get(e), h = o.get(t);
  if (f && h)
    return f == t && h == e;
  var b = !0;
  o.set(e, t), o.set(t, e);
  for (var p = a; ++_ < u; ) {
    c = s[_];
    var v = e[c], P = t[c];
    if (n)
      var O = a ? n(P, v, c, t, e, o) : n(v, P, c, e, t, o);
    if (!(O === void 0 ? v === P || i(v, P, r, n, o) : O)) {
      b = !1;
      break;
    }
    p || (p = c == "constructor");
  }
  if (b && !p) {
    var C = e.constructor, A = t.constructor;
    C != A && "constructor" in e && "constructor" in t && !(typeof C == "function" && C instanceof C && typeof A == "function" && A instanceof A) && (b = !1);
  }
  return o.delete(e), o.delete(t), b;
}
var Pa = 1, at = "[object Arguments]", st = "[object Array]", V = "[object Object]", Oa = Object.prototype, ut = Oa.hasOwnProperty;
function wa(e, t, r, n, i, o) {
  var a = x(e), s = x(t), u = a ? st : S(e), l = s ? st : S(t);
  u = u == at ? V : u, l = l == at ? V : l;
  var d = u == V, _ = l == V, c = u == l;
  if (c && re(e)) {
    if (!re(t))
      return !1;
    a = !0, d = !1;
  }
  if (c && !d)
    return o || (o = new j()), a || St(e) ? Ut(e, t, r, n, i, o) : ba(e, t, u, r, n, i, o);
  if (!(r & Pa)) {
    var f = d && ut.call(e, "__wrapped__"), h = _ && ut.call(t, "__wrapped__");
    if (f || h) {
      var b = f ? e.value() : e, p = h ? t.value() : t;
      return o || (o = new j()), i(b, p, r, n, o);
    }
  }
  return c ? (o || (o = new j()), Ta(e, t, r, n, i, o)) : !1;
}
function Me(e, t, r, n, i) {
  return e === t ? !0 : e == null || t == null || !I(e) && !I(t) ? e !== e && t !== t : wa(e, t, r, n, Me, i);
}
var Aa = 1, $a = 2;
function Sa(e, t, r, n) {
  var i = r.length, o = i;
  if (e == null)
    return !o;
  for (e = Object(e); i--; ) {
    var a = r[i];
    if (a[2] ? a[1] !== e[a[0]] : !(a[0] in e))
      return !1;
  }
  for (; ++i < o; ) {
    a = r[i];
    var s = a[0], u = e[s], l = a[1];
    if (a[2]) {
      if (u === void 0 && !(s in e))
        return !1;
    } else {
      var d = new j(), _;
      if (!(_ === void 0 ? Me(l, u, Aa | $a, n, d) : _))
        return !1;
    }
  }
  return !0;
}
function Gt(e) {
  return e === e && !z(e);
}
function xa(e) {
  for (var t = Se(e), r = t.length; r--; ) {
    var n = t[r], i = e[n];
    t[r] = [n, i, Gt(i)];
  }
  return t;
}
function Bt(e, t) {
  return function(r) {
    return r == null ? !1 : r[e] === t && (t !== void 0 || e in Object(r));
  };
}
function Ca(e) {
  var t = xa(e);
  return t.length == 1 && t[0][2] ? Bt(t[0][0], t[0][1]) : function(r) {
    return r === e || Sa(r, e, t);
  };
}
function ja(e, t) {
  return e != null && t in Object(e);
}
function Ea(e, t, r) {
  t = ue(t, e);
  for (var n = -1, i = t.length, o = !1; ++n < i; ) {
    var a = Z(t[n]);
    if (!(o = e != null && r(e, a)))
      break;
    e = e[a];
  }
  return o || ++n != i ? o : (i = e == null ? 0 : e.length, !!i && we(i) && vt(a, i) && (x(e) || Ae(e)));
}
function Ia(e, t) {
  return e != null && Ea(e, t, ja);
}
var Ma = 1, Fa = 2;
function Ra(e, t) {
  return xe(e) && Gt(t) ? Bt(Z(e), t) : function(r) {
    var n = ho(r, e);
    return n === void 0 && n === t ? Ia(r, e) : Me(t, n, Ma | Fa);
  };
}
function La(e) {
  return function(t) {
    return t == null ? void 0 : t[e];
  };
}
function Da(e) {
  return function(t) {
    return je(t, e);
  };
}
function Na(e) {
  return xe(e) ? La(Z(e)) : Da(e);
}
function Ka(e) {
  return typeof e == "function" ? e : e == null ? yt : typeof e == "object" ? x(e) ? Ra(e[0], e[1]) : Ca(e) : Na(e);
}
function Ua(e) {
  return function(t, r, n) {
    for (var i = -1, o = Object(t), a = n(t), s = a.length; s--; ) {
      var u = a[++i];
      if (r(o[u], u, o) === !1)
        break;
    }
    return t;
  };
}
var Ga = Ua();
function Ba(e, t) {
  return e && Ga(e, t, Se);
}
function za(e) {
  var t = e == null ? 0 : e.length;
  return t ? e[t - 1] : void 0;
}
function Ha(e, t) {
  return t.length < 2 ? e : je(e, $o(t, 0, -1));
}
function qa(e, t) {
  var r = {};
  return t = Ka(t), Ba(e, function(n, i, o) {
    Pe(r, t(n, i, o), n);
  }), r;
}
function Ja(e, t) {
  return t = ue(t, e), e = Ha(e, t), e == null || delete e[Z(za(t))];
}
function Xa(e) {
  return he(e) ? void 0 : e;
}
var Ya = 1, Za = 2, Wa = 4, zt = vo(function(e, t) {
  var r = {};
  if (e == null)
    return r;
  var n = !1;
  t = ht(t, function(o) {
    return o = ue(o, e), n || (n = o.length > 1), o;
  }), Gr(e, Lt(e), r), n && (r = k(r, Ya | Za | Wa, Xa));
  for (var i = t.length; i--; )
    Ja(r, t[i]);
  return r;
});
function Ht(e) {
  return e.replace(/(^|_)(\w)/g, (t, r, n, i) => i === 0 ? n.toLowerCase() : n.toUpperCase());
}
const Us = (e) => z(e) ? Object.keys(e).reduce((t, r) => (t[Ht(r)] = e[r], t), {}) : e;
async function Qa() {
  window.ms_globals || (window.ms_globals = {}), window.ms_globals.initializePromise || (window.ms_globals.initializePromise = new Promise((e) => {
    window.ms_globals.initialize = () => {
      e();
    };
  })), await window.ms_globals.initializePromise;
}
async function Va(e) {
  return await Qa(), e().then((t) => t.default);
}
const qt = [
  "interactive",
  "gradio",
  "server",
  "target",
  "theme_mode",
  "root",
  "name",
  // 'visible',
  // 'elem_id',
  // 'elem_classes',
  // 'elem_style',
  "_internal",
  "props",
  // 'value',
  "_selectable",
  "loading_status",
  "value_is_output"
], ka = qt.concat(["attached_events"]);
function es(e, t = {}, r = !1) {
  return qa(zt(e, r ? [] : qt), (n, i) => t[i] || Ht(i));
}
function lt(e, t) {
  const {
    gradio: r,
    _internal: n,
    restProps: i,
    originalRestProps: o,
    ...a
  } = e, s = (i == null ? void 0 : i.attachedEvents) || [];
  return {
    ...Array.from(/* @__PURE__ */ new Set([...Object.keys(n).map((u) => {
      const l = u.match(/bind_(.+)_event/);
      return l && l[1] ? l[1] : null;
    }).filter(Boolean), ...s.map((u) => t && t[u] ? t[u] : u)])).reduce((u, l) => {
      const d = l.split("_"), _ = (...f) => {
        const h = f.map((p) => f && typeof p == "object" && (p.nativeEvent || p instanceof Event) ? {
          type: p.type,
          detail: p.detail,
          timestamp: p.timeStamp,
          clientX: p.clientX,
          clientY: p.clientY,
          targetId: p.target.id,
          targetClassName: p.target.className,
          altKey: p.altKey,
          ctrlKey: p.ctrlKey,
          shiftKey: p.shiftKey,
          metaKey: p.metaKey
        } : p);
        let b;
        try {
          b = JSON.parse(JSON.stringify(h));
        } catch {
          let p = function(v) {
            try {
              return JSON.stringify(v), v;
            } catch {
              return he(v) ? Object.fromEntries(Object.entries(v).map(([P, O]) => {
                try {
                  return JSON.stringify(O), [P, O];
                } catch {
                  return he(O) ? [P, Object.fromEntries(Object.entries(O).filter(([C, A]) => {
                    try {
                      return JSON.stringify(A), !0;
                    } catch {
                      return !1;
                    }
                  }))] : null;
                }
              }).filter(Boolean)) : {};
            }
          };
          b = h.map((v) => p(v));
        }
        return r.dispatch(l.replace(/[A-Z]/g, (p) => "_" + p.toLowerCase()), {
          payload: b,
          component: {
            ...a,
            ...zt(o, ka)
          }
        });
      };
      if (d.length > 1) {
        let f = {
          ...a.props[d[0]] || (i == null ? void 0 : i[d[0]]) || {}
        };
        u[d[0]] = f;
        for (let b = 1; b < d.length - 1; b++) {
          const p = {
            ...a.props[d[b]] || (i == null ? void 0 : i[d[b]]) || {}
          };
          f[d[b]] = p, f = p;
        }
        const h = d[d.length - 1];
        return f[`on${h.slice(0, 1).toUpperCase()}${h.slice(1)}`] = _, u;
      }
      const c = d[0];
      return u[`on${c.slice(0, 1).toUpperCase()}${c.slice(1)}`] = _, u;
    }, {}),
    __render_eventProps: {
      props: e,
      eventsMapping: t
    }
  };
}
function ee() {
}
function ts(e, t) {
  return e != e ? t == t : e !== t || e && typeof e == "object" || typeof e == "function";
}
function rs(e, ...t) {
  if (e == null) {
    for (const n of t)
      n(void 0);
    return ee;
  }
  const r = e.subscribe(...t);
  return r.unsubscribe ? () => r.unsubscribe() : r;
}
function Jt(e) {
  let t;
  return rs(e, (r) => t = r)(), t;
}
const U = [];
function R(e, t = ee) {
  let r;
  const n = /* @__PURE__ */ new Set();
  function i(s) {
    if (ts(e, s) && (e = s, r)) {
      const u = !U.length;
      for (const l of n)
        l[1](), U.push(l, e);
      if (u) {
        for (let l = 0; l < U.length; l += 2)
          U[l][0](U[l + 1]);
        U.length = 0;
      }
    }
  }
  function o(s) {
    i(s(e));
  }
  function a(s, u = ee) {
    const l = [s, u];
    return n.add(l), n.size === 1 && (r = t(i, o) || ee), s(e), () => {
      n.delete(l), n.size === 0 && r && (r(), r = null);
    };
  }
  return {
    set: i,
    update: o,
    subscribe: a
  };
}
const {
  getContext: ns,
  setContext: Gs
} = window.__gradio__svelte__internal, os = "$$ms-gr-loading-status-key";
function is() {
  const e = window.ms_globals.loadingKey++, t = ns(os);
  return (r) => {
    if (!t || !r)
      return;
    const {
      loadingStatusMap: n,
      options: i
    } = t, {
      generating: o,
      error: a
    } = Jt(i);
    (r == null ? void 0 : r.status) === "pending" || a && (r == null ? void 0 : r.status) === "error" || (o && (r == null ? void 0 : r.status)) === "generating" ? n.update(({
      map: s
    }) => (s.set(e, r), {
      map: s
    })) : n.update(({
      map: s
    }) => (s.delete(e), {
      map: s
    }));
  };
}
const {
  getContext: le,
  setContext: W
} = window.__gradio__svelte__internal, as = "$$ms-gr-slots-key";
function ss() {
  const e = R({});
  return W(as, e);
}
const Xt = "$$ms-gr-slot-params-mapping-fn-key";
function us() {
  return le(Xt);
}
function ls(e) {
  return W(Xt, R(e));
}
const Yt = "$$ms-gr-sub-index-context-key";
function cs() {
  return le(Yt) || null;
}
function ct(e) {
  return W(Yt, e);
}
function fs(e, t, r) {
  if (!Reflect.has(e, "as_item") || !Reflect.has(e, "_internal"))
    throw new Error("`as_item` and `_internal` is required");
  const n = gs(), i = us();
  ls().set(void 0);
  const a = ds({
    slot: void 0,
    index: e._internal.index,
    subIndex: e._internal.subIndex
  }), s = cs();
  typeof s == "number" && ct(void 0);
  const u = is();
  typeof e._internal.subIndex == "number" && ct(e._internal.subIndex), n && n.subscribe((c) => {
    a.slotKey.set(c);
  }), ps();
  const l = e.as_item, d = (c, f) => c ? {
    ...es({
      ...c
    }, t),
    __render_slotParamsMappingFn: i ? Jt(i) : void 0,
    __render_as_item: f,
    __render_restPropsMapping: t
  } : void 0, _ = R({
    ...e,
    _internal: {
      ...e._internal,
      index: s ?? e._internal.index
    },
    restProps: d(e.restProps, l),
    originalRestProps: e.restProps
  });
  return i && i.subscribe((c) => {
    _.update((f) => ({
      ...f,
      restProps: {
        ...f.restProps,
        __slotParamsMappingFn: c
      }
    }));
  }), [_, (c) => {
    var f;
    u((f = c.restProps) == null ? void 0 : f.loading_status), _.set({
      ...c,
      _internal: {
        ...c._internal,
        index: s ?? c._internal.index
      },
      restProps: d(c.restProps, c.as_item),
      originalRestProps: c.restProps
    });
  }];
}
const Zt = "$$ms-gr-slot-key";
function ps() {
  W(Zt, R(void 0));
}
function gs() {
  return le(Zt);
}
const Wt = "$$ms-gr-component-slot-context-key";
function ds({
  slot: e,
  index: t,
  subIndex: r
}) {
  return W(Wt, {
    slotKey: R(e),
    slotIndex: R(t),
    subSlotIndex: R(r)
  });
}
function Bs() {
  return le(Wt);
}
function _s(e) {
  return e && e.__esModule && Object.prototype.hasOwnProperty.call(e, "default") ? e.default : e;
}
var Qt = {
  exports: {}
};
/*!
	Copyright (c) 2018 Jed Watson.
	Licensed under the MIT License (MIT), see
	http://jedwatson.github.io/classnames
*/
(function(e) {
  (function() {
    var t = {}.hasOwnProperty;
    function r() {
      for (var o = "", a = 0; a < arguments.length; a++) {
        var s = arguments[a];
        s && (o = i(o, n(s)));
      }
      return o;
    }
    function n(o) {
      if (typeof o == "string" || typeof o == "number")
        return o;
      if (typeof o != "object")
        return "";
      if (Array.isArray(o))
        return r.apply(null, o);
      if (o.toString !== Object.prototype.toString && !o.toString.toString().includes("[native code]"))
        return o.toString();
      var a = "";
      for (var s in o)
        t.call(o, s) && o[s] && (a = i(a, s));
      return a;
    }
    function i(o, a) {
      return a ? o ? o + " " + a : o + a : o;
    }
    e.exports ? (r.default = r, e.exports = r) : window.classNames = r;
  })();
})(Qt);
var hs = Qt.exports;
const ft = /* @__PURE__ */ _s(hs), {
  SvelteComponent: bs,
  assign: ve,
  check_outros: ys,
  claim_component: ms,
  component_subscribe: ge,
  compute_rest_props: pt,
  create_component: vs,
  create_slot: Ts,
  destroy_component: Ps,
  detach: Vt,
  empty: ie,
  exclude_internal_props: Os,
  flush: $,
  get_all_dirty_from_scope: ws,
  get_slot_changes: As,
  get_spread_object: de,
  get_spread_update: $s,
  group_outros: Ss,
  handle_promise: xs,
  init: Cs,
  insert_hydration: kt,
  mount_component: js,
  noop: T,
  safe_not_equal: Es,
  transition_in: G,
  transition_out: Y,
  update_await_block_branch: Is,
  update_slot_base: Ms
} = window.__gradio__svelte__internal;
function gt(e) {
  let t, r, n = {
    ctx: e,
    current: null,
    token: null,
    hasCatch: !1,
    pending: Ds,
    then: Rs,
    catch: Fs,
    value: 23,
    blocks: [, , ,]
  };
  return xs(
    /*AwaitedChatbot*/
    e[6],
    n
  ), {
    c() {
      t = ie(), n.block.c();
    },
    l(i) {
      t = ie(), n.block.l(i);
    },
    m(i, o) {
      kt(i, t, o), n.block.m(i, n.anchor = o), n.mount = () => t.parentNode, n.anchor = t, r = !0;
    },
    p(i, o) {
      e = i, Is(n, e, o);
    },
    i(i) {
      r || (G(n.block), r = !0);
    },
    o(i) {
      for (let o = 0; o < 3; o += 1) {
        const a = n.blocks[o];
        Y(a);
      }
      r = !1;
    },
    d(i) {
      i && Vt(t), n.block.d(i), n.token = null, n = null;
    }
  };
}
function Fs(e) {
  return {
    c: T,
    l: T,
    m: T,
    p: T,
    i: T,
    o: T,
    d: T
  };
}
function Rs(e) {
  let t, r;
  const n = [
    {
      style: (
        /*$mergedProps*/
        e[4].elem_style
      )
    },
    {
      className: ft(
        /*$mergedProps*/
        e[4].elem_classes
      )
    },
    {
      id: (
        /*$mergedProps*/
        e[4].elem_id
      )
    },
    /*$mergedProps*/
    e[4].restProps,
    /*$mergedProps*/
    e[4].props,
    lt(
      /*$mergedProps*/
      e[4],
      {
        suggestion_select: "suggestionSelect",
        welcome_prompt_select: "welcomePromptSelect"
      }
    ),
    {
      value: (
        /*$mergedProps*/
        e[4].value
      )
    },
    {
      onValueChange: (
        /*func*/
        e[19]
      )
    },
    {
      urlRoot: (
        /*root*/
        e[2]
      )
    },
    {
      urlProxyUrl: (
        /*proxy_url*/
        e[3]
      )
    },
    {
      themeMode: (
        /*gradio*/
        e[1].theme
      )
    },
    {
      slots: (
        /*$slots*/
        e[5]
      )
    }
  ];
  let i = {
    $$slots: {
      default: [Ls]
    },
    $$scope: {
      ctx: e
    }
  };
  for (let o = 0; o < n.length; o += 1)
    i = ve(i, n[o]);
  return t = new /*Chatbot*/
  e[23]({
    props: i
  }), {
    c() {
      vs(t.$$.fragment);
    },
    l(o) {
      ms(t.$$.fragment, o);
    },
    m(o, a) {
      js(t, o, a), r = !0;
    },
    p(o, a) {
      const s = a & /*$mergedProps, value, root, proxy_url, gradio, $slots*/
      63 ? $s(n, [a & /*$mergedProps*/
      16 && {
        style: (
          /*$mergedProps*/
          o[4].elem_style
        )
      }, a & /*$mergedProps*/
      16 && {
        className: ft(
          /*$mergedProps*/
          o[4].elem_classes
        )
      }, a & /*$mergedProps*/
      16 && {
        id: (
          /*$mergedProps*/
          o[4].elem_id
        )
      }, a & /*$mergedProps*/
      16 && de(
        /*$mergedProps*/
        o[4].restProps
      ), a & /*$mergedProps*/
      16 && de(
        /*$mergedProps*/
        o[4].props
      ), a & /*$mergedProps*/
      16 && de(lt(
        /*$mergedProps*/
        o[4],
        {
          suggestion_select: "suggestionSelect",
          welcome_prompt_select: "welcomePromptSelect"
        }
      )), a & /*$mergedProps*/
      16 && {
        value: (
          /*$mergedProps*/
          o[4].value
        )
      }, a & /*value*/
      1 && {
        onValueChange: (
          /*func*/
          o[19]
        )
      }, a & /*root*/
      4 && {
        urlRoot: (
          /*root*/
          o[2]
        )
      }, a & /*proxy_url*/
      8 && {
        urlProxyUrl: (
          /*proxy_url*/
          o[3]
        )
      }, a & /*gradio*/
      2 && {
        themeMode: (
          /*gradio*/
          o[1].theme
        )
      }, a & /*$slots*/
      32 && {
        slots: (
          /*$slots*/
          o[5]
        )
      }]) : {};
      a & /*$$scope*/
      1048576 && (s.$$scope = {
        dirty: a,
        ctx: o
      }), t.$set(s);
    },
    i(o) {
      r || (G(t.$$.fragment, o), r = !0);
    },
    o(o) {
      Y(t.$$.fragment, o), r = !1;
    },
    d(o) {
      Ps(t, o);
    }
  };
}
function Ls(e) {
  let t;
  const r = (
    /*#slots*/
    e[18].default
  ), n = Ts(
    r,
    e,
    /*$$scope*/
    e[20],
    null
  );
  return {
    c() {
      n && n.c();
    },
    l(i) {
      n && n.l(i);
    },
    m(i, o) {
      n && n.m(i, o), t = !0;
    },
    p(i, o) {
      n && n.p && (!t || o & /*$$scope*/
      1048576) && Ms(
        n,
        r,
        i,
        /*$$scope*/
        i[20],
        t ? As(
          r,
          /*$$scope*/
          i[20],
          o,
          null
        ) : ws(
          /*$$scope*/
          i[20]
        ),
        null
      );
    },
    i(i) {
      t || (G(n, i), t = !0);
    },
    o(i) {
      Y(n, i), t = !1;
    },
    d(i) {
      n && n.d(i);
    }
  };
}
function Ds(e) {
  return {
    c: T,
    l: T,
    m: T,
    p: T,
    i: T,
    o: T,
    d: T
  };
}
function Ns(e) {
  let t, r, n = (
    /*$mergedProps*/
    e[4].visible && gt(e)
  );
  return {
    c() {
      n && n.c(), t = ie();
    },
    l(i) {
      n && n.l(i), t = ie();
    },
    m(i, o) {
      n && n.m(i, o), kt(i, t, o), r = !0;
    },
    p(i, [o]) {
      /*$mergedProps*/
      i[4].visible ? n ? (n.p(i, o), o & /*$mergedProps*/
      16 && G(n, 1)) : (n = gt(i), n.c(), G(n, 1), n.m(t.parentNode, t)) : n && (Ss(), Y(n, 1, 1, () => {
        n = null;
      }), ys());
    },
    i(i) {
      r || (G(n), r = !0);
    },
    o(i) {
      Y(n), r = !1;
    },
    d(i) {
      i && Vt(t), n && n.d(i);
    }
  };
}
function Ks(e, t, r) {
  const n = ["value", "gradio", "props", "_internal", "as_item", "root", "proxy_url", "visible", "elem_id", "elem_classes", "elem_style"];
  let i = pt(t, n), o, a, s, {
    $$slots: u = {},
    $$scope: l
  } = t;
  const d = Va(() => import("./chatbot-yziIb-zL.js"));
  let {
    value: _ = []
  } = t, {
    gradio: c
  } = t, {
    props: f = {}
  } = t;
  const h = R(f);
  ge(e, h, (g) => r(17, o = g));
  let {
    _internal: b = {}
  } = t, {
    as_item: p
  } = t, {
    root: v
  } = t, {
    proxy_url: P
  } = t, {
    visible: O = !0
  } = t, {
    elem_id: C = ""
  } = t, {
    elem_classes: A = []
  } = t, {
    elem_style: Q = {}
  } = t;
  const [Fe, er] = fs({
    gradio: c,
    props: o,
    _internal: b,
    visible: O,
    elem_id: C,
    elem_classes: A,
    elem_style: Q,
    as_item: p,
    value: _,
    restProps: i
  });
  ge(e, Fe, (g) => r(4, a = g));
  const Re = ss();
  ge(e, Re, (g) => r(5, s = g));
  const tr = (g) => {
    r(0, _ = g);
  };
  return e.$$set = (g) => {
    t = ve(ve({}, t), Os(g)), r(22, i = pt(t, n)), "value" in g && r(0, _ = g.value), "gradio" in g && r(1, c = g.gradio), "props" in g && r(10, f = g.props), "_internal" in g && r(11, b = g._internal), "as_item" in g && r(12, p = g.as_item), "root" in g && r(2, v = g.root), "proxy_url" in g && r(3, P = g.proxy_url), "visible" in g && r(13, O = g.visible), "elem_id" in g && r(14, C = g.elem_id), "elem_classes" in g && r(15, A = g.elem_classes), "elem_style" in g && r(16, Q = g.elem_style), "$$scope" in g && r(20, l = g.$$scope);
  }, e.$$.update = () => {
    e.$$.dirty & /*props*/
    1024 && h.update((g) => ({
      ...g,
      ...f
    })), er({
      gradio: c,
      props: o,
      _internal: b,
      visible: O,
      elem_id: C,
      elem_classes: A,
      elem_style: Q,
      as_item: p,
      value: _,
      restProps: i
    });
  }, [_, c, v, P, a, s, d, h, Fe, Re, f, b, p, O, C, A, Q, o, u, tr, l];
}
class zs extends bs {
  constructor(t) {
    super(), Cs(this, t, Ks, Ns, Es, {
      value: 0,
      gradio: 1,
      props: 10,
      _internal: 11,
      as_item: 12,
      root: 2,
      proxy_url: 3,
      visible: 13,
      elem_id: 14,
      elem_classes: 15,
      elem_style: 16
    });
  }
  get value() {
    return this.$$.ctx[0];
  }
  set value(t) {
    this.$$set({
      value: t
    }), $();
  }
  get gradio() {
    return this.$$.ctx[1];
  }
  set gradio(t) {
    this.$$set({
      gradio: t
    }), $();
  }
  get props() {
    return this.$$.ctx[10];
  }
  set props(t) {
    this.$$set({
      props: t
    }), $();
  }
  get _internal() {
    return this.$$.ctx[11];
  }
  set _internal(t) {
    this.$$set({
      _internal: t
    }), $();
  }
  get as_item() {
    return this.$$.ctx[12];
  }
  set as_item(t) {
    this.$$set({
      as_item: t
    }), $();
  }
  get root() {
    return this.$$.ctx[2];
  }
  set root(t) {
    this.$$set({
      root: t
    }), $();
  }
  get proxy_url() {
    return this.$$.ctx[3];
  }
  set proxy_url(t) {
    this.$$set({
      proxy_url: t
    }), $();
  }
  get visible() {
    return this.$$.ctx[13];
  }
  set visible(t) {
    this.$$set({
      visible: t
    }), $();
  }
  get elem_id() {
    return this.$$.ctx[14];
  }
  set elem_id(t) {
    this.$$set({
      elem_id: t
    }), $();
  }
  get elem_classes() {
    return this.$$.ctx[15];
  }
  set elem_classes(t) {
    this.$$set({
      elem_classes: t
    }), $();
  }
  get elem_style() {
    return this.$$.ctx[16];
  }
  set elem_style(t) {
    this.$$set({
      elem_style: t
    }), $();
  }
}
export {
  zs as I,
  z as a,
  Me as b,
  ft as c,
  mt as d,
  Us as e,
  Bs as g,
  Te as i,
  zt as o,
  E as r,
  R as w
};
