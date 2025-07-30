import { az as b, aH as p } from "./mermaid.core-Bmt021c3.js";
import { f as x, h as m, j as P, l as w, m as I, n as o, k as y, o as A, p as N, q as E, r as M, s as g, t as _, u as $, v as c, w as B } from "./Index-RuHPazS6.js";
import { c as F, d as T } from "./_baseUniq-CMyUoDnL.js";
var H = /\s/;
function S(r) {
  for (var n = r.length; n-- && H.test(r.charAt(n)); )
    ;
  return n;
}
var l = /^\s+/;
function q(r) {
  return r && r.slice(0, S(r) + 1).replace(l, "");
}
var v = NaN, z = /^[-+]0x[0-9a-f]+$/i, G = /^0b[01]+$/i, L = /^0o[0-7]+$/i, R = parseInt;
function C(r) {
  if (typeof r == "number")
    return r;
  if (x(r))
    return v;
  if (m(r)) {
    var n = typeof r.valueOf == "function" ? r.valueOf() : r;
    r = m(n) ? n + "" : n;
  }
  if (typeof r != "string")
    return r === 0 ? r : +r;
  r = q(r);
  var t = G.test(r);
  return t || L.test(r) ? R(r.slice(2), t ? 2 : 8) : z.test(r) ? v : +r;
}
var K = 1 / 0, W = 17976931348623157e292;
function X(r) {
  if (!r)
    return r === 0 ? r : 0;
  if (r = C(r), r === K || r === -1 / 0) {
    var n = r < 0 ? -1 : 1;
    return n * W;
  }
  return r === r ? r : 0;
}
function Y(r) {
  var n = X(r), t = n % 1;
  return n === n ? t ? n - t : n : 0;
}
var O = Object.prototype, D = O.hasOwnProperty, sr = b(function(r, n) {
  r = Object(r);
  var t = -1, e = n.length, i = e > 2 ? n[2] : void 0;
  for (i && p(n[0], n[1], i) && (e = 1); ++t < e; )
    for (var f = n[t], a = P(f), s = -1, d = a.length; ++s < d; ) {
      var u = a[s], h = r[u];
      (h === void 0 || w(h, O[u]) && !D.call(r, u)) && (r[u] = f[u]);
    }
  return r;
});
function J(r) {
  return function(n, t, e) {
    var i = Object(n);
    if (!I(n)) {
      var f = o(t);
      n = y(n), t = function(s) {
        return f(i[s], s, i);
      };
    }
    var a = r(n, t, e);
    return a > -1 ? i[f ? n[a] : a] : void 0;
  };
}
var Q = Math.max;
function U(r, n, t) {
  var e = r == null ? 0 : r.length;
  if (!e)
    return -1;
  var i = t == null ? 0 : Y(t);
  return i < 0 && (i = Q(e + i, 0)), F(r, o(n), i);
}
var fr = J(U);
function Z(r, n) {
  var t = -1, e = I(r) ? Array(r.length) : [];
  return T(r, function(i, f, a) {
    e[++t] = n(i, f, a);
  }), e;
}
function dr(r, n) {
  var t = N(r) ? A : Z;
  return t(r, o(n));
}
var V = Object.prototype, k = V.hasOwnProperty;
function j(r, n) {
  return r != null && k.call(r, n);
}
function ur(r, n) {
  return r != null && E(r, n, j);
}
function rr(r, n) {
  return r < n;
}
function nr(r, n, t) {
  for (var e = -1, i = r.length; ++e < i; ) {
    var f = r[e], a = n(f);
    if (a != null && (s === void 0 ? a === a && !x(a) : t(a, s)))
      var s = a, d = f;
  }
  return d;
}
function hr(r) {
  return r && r.length ? nr(r, M, rr) : void 0;
}
function tr(r, n, t, e) {
  if (!m(r))
    return r;
  n = g(n, r);
  for (var i = -1, f = n.length, a = f - 1, s = r; s != null && ++i < f; ) {
    var d = _(n[i]), u = t;
    if (d === "__proto__" || d === "constructor" || d === "prototype")
      return r;
    if (i != a) {
      var h = s[d];
      u = void 0, u === void 0 && (u = m(h) ? h : $(n[i + 1]) ? [] : {});
    }
    c(s, d, u), s = s[d];
  }
  return r;
}
function mr(r, n, t) {
  for (var e = -1, i = n.length, f = {}; ++e < i; ) {
    var a = n[e], s = B(r, a);
    t(s, a) && tr(f, g(a, r), s);
  }
  return f;
}
export {
  rr as a,
  nr as b,
  Z as c,
  mr as d,
  hr as e,
  fr as f,
  sr as g,
  ur as h,
  Y as i,
  dr as m,
  X as t
};
