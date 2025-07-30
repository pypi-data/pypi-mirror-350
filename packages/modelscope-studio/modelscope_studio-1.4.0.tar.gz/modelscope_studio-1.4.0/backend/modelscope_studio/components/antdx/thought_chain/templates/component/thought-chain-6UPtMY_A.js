import { i as on, a as gt, r as sn, w as $e, g as an, c as G } from "./Index-BgKBKA12.js";
const M = window.ms_globals.React, x = window.ms_globals.React, Jr = window.ms_globals.React.isValidElement, Zr = window.ms_globals.React.version, ee = window.ms_globals.React.useRef, en = window.ms_globals.React.useLayoutEffect, ge = window.ms_globals.React.useEffect, tn = window.ms_globals.React.forwardRef, rn = window.ms_globals.React.useState, nn = window.ms_globals.React.useMemo, jt = window.ms_globals.ReactDOM, pt = window.ms_globals.ReactDOM.createPortal, cn = window.ms_globals.internalContext.useContextPropsContext, zt = window.ms_globals.internalContext.ContextPropsProvider, ln = window.ms_globals.createItemsContext.createItemsContext, un = window.ms_globals.antd.ConfigProvider, vt = window.ms_globals.antd.theme, fn = window.ms_globals.antd.Avatar, Dt = window.ms_globals.antd.Typography, ze = window.ms_globals.antdCssinjs.unit, rt = window.ms_globals.antdCssinjs.token2CSSVar, kt = window.ms_globals.antdCssinjs.useStyleRegister, dn = window.ms_globals.antdCssinjs.useCSSVarRegister, mn = window.ms_globals.antdCssinjs.createTheme, hn = window.ms_globals.antdCssinjs.useCacheToken, pn = window.ms_globals.antdIcons.LeftOutlined, gn = window.ms_globals.antdIcons.RightOutlined;
var vn = /\s/;
function yn(e) {
  for (var t = e.length; t-- && vn.test(e.charAt(t)); )
    ;
  return t;
}
var bn = /^\s+/;
function Sn(e) {
  return e && e.slice(0, yn(e) + 1).replace(bn, "");
}
var Nt = NaN, xn = /^[-+]0x[0-9a-f]+$/i, Cn = /^0b[01]+$/i, En = /^0o[0-7]+$/i, _n = parseInt;
function Ft(e) {
  if (typeof e == "number")
    return e;
  if (on(e))
    return Nt;
  if (gt(e)) {
    var t = typeof e.valueOf == "function" ? e.valueOf() : e;
    e = gt(t) ? t + "" : t;
  }
  if (typeof e != "string")
    return e === 0 ? e : +e;
  e = Sn(e);
  var r = Cn.test(e);
  return r || En.test(e) ? _n(e.slice(2), r ? 2 : 8) : xn.test(e) ? Nt : +e;
}
var nt = function() {
  return sn.Date.now();
}, wn = "Expected a function", Tn = Math.max, Pn = Math.min;
function Mn(e, t, r) {
  var o, n, i, s, a, c, l = 0, f = !1, u = !1, d = !0;
  if (typeof e != "function")
    throw new TypeError(wn);
  t = Ft(t) || 0, gt(r) && (f = !!r.leading, u = "maxWait" in r, i = u ? Tn(Ft(r.maxWait) || 0, t) : i, d = "trailing" in r ? !!r.trailing : d);
  function h(p) {
    var P = o, T = n;
    return o = n = void 0, l = p, s = e.apply(T, P), s;
  }
  function v(p) {
    return l = p, a = setTimeout(y, t), f ? h(p) : s;
  }
  function g(p) {
    var P = p - c, T = p - l, R = t - P;
    return u ? Pn(R, i - T) : R;
  }
  function m(p) {
    var P = p - c, T = p - l;
    return c === void 0 || P >= t || P < 0 || u && T >= i;
  }
  function y() {
    var p = nt();
    if (m(p))
      return S(p);
    a = setTimeout(y, g(p));
  }
  function S(p) {
    return a = void 0, d && o ? h(p) : (o = n = void 0, s);
  }
  function w() {
    a !== void 0 && clearTimeout(a), l = 0, o = c = n = a = void 0;
  }
  function b() {
    return a === void 0 ? s : S(nt());
  }
  function _() {
    var p = nt(), P = m(p);
    if (o = arguments, n = this, c = p, P) {
      if (a === void 0)
        return v(c);
      if (u)
        return clearTimeout(a), a = setTimeout(y, t), h(c);
    }
    return a === void 0 && (a = setTimeout(y, t)), s;
  }
  return _.cancel = w, _.flush = b, _;
}
var br = {
  exports: {}
}, Ne = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var On = x, Rn = Symbol.for("react.element"), Ln = Symbol.for("react.fragment"), An = Object.prototype.hasOwnProperty, $n = On.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, In = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function Sr(e, t, r) {
  var o, n = {}, i = null, s = null;
  r !== void 0 && (i = "" + r), t.key !== void 0 && (i = "" + t.key), t.ref !== void 0 && (s = t.ref);
  for (o in t) An.call(t, o) && !In.hasOwnProperty(o) && (n[o] = t[o]);
  if (e && e.defaultProps) for (o in t = e.defaultProps, t) n[o] === void 0 && (n[o] = t[o]);
  return {
    $$typeof: Rn,
    type: e,
    key: i,
    ref: s,
    props: n,
    _owner: $n.current
  };
}
Ne.Fragment = Ln;
Ne.jsx = Sr;
Ne.jsxs = Sr;
br.exports = Ne;
var q = br.exports;
const {
  SvelteComponent: jn,
  assign: Ht,
  binding_callbacks: Vt,
  check_outros: zn,
  children: xr,
  claim_element: Cr,
  claim_space: Dn,
  component_subscribe: Bt,
  compute_slots: kn,
  create_slot: Nn,
  detach: ce,
  element: Er,
  empty: Gt,
  exclude_internal_props: Xt,
  get_all_dirty_from_scope: Fn,
  get_slot_changes: Hn,
  group_outros: Vn,
  init: Bn,
  insert_hydration: Ie,
  safe_not_equal: Gn,
  set_custom_element_data: _r,
  space: Xn,
  transition_in: je,
  transition_out: yt,
  update_slot_base: Un
} = window.__gradio__svelte__internal, {
  beforeUpdate: Wn,
  getContext: Kn,
  onDestroy: qn,
  setContext: Qn
} = window.__gradio__svelte__internal;
function Ut(e) {
  let t, r;
  const o = (
    /*#slots*/
    e[7].default
  ), n = Nn(
    o,
    e,
    /*$$scope*/
    e[6],
    null
  );
  return {
    c() {
      t = Er("svelte-slot"), n && n.c(), this.h();
    },
    l(i) {
      t = Cr(i, "SVELTE-SLOT", {
        class: !0
      });
      var s = xr(t);
      n && n.l(s), s.forEach(ce), this.h();
    },
    h() {
      _r(t, "class", "svelte-1rt0kpf");
    },
    m(i, s) {
      Ie(i, t, s), n && n.m(t, null), e[9](t), r = !0;
    },
    p(i, s) {
      n && n.p && (!r || s & /*$$scope*/
      64) && Un(
        n,
        o,
        i,
        /*$$scope*/
        i[6],
        r ? Hn(
          o,
          /*$$scope*/
          i[6],
          s,
          null
        ) : Fn(
          /*$$scope*/
          i[6]
        ),
        null
      );
    },
    i(i) {
      r || (je(n, i), r = !0);
    },
    o(i) {
      yt(n, i), r = !1;
    },
    d(i) {
      i && ce(t), n && n.d(i), e[9](null);
    }
  };
}
function Yn(e) {
  let t, r, o, n, i = (
    /*$$slots*/
    e[4].default && Ut(e)
  );
  return {
    c() {
      t = Er("react-portal-target"), r = Xn(), i && i.c(), o = Gt(), this.h();
    },
    l(s) {
      t = Cr(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), xr(t).forEach(ce), r = Dn(s), i && i.l(s), o = Gt(), this.h();
    },
    h() {
      _r(t, "class", "svelte-1rt0kpf");
    },
    m(s, a) {
      Ie(s, t, a), e[8](t), Ie(s, r, a), i && i.m(s, a), Ie(s, o, a), n = !0;
    },
    p(s, [a]) {
      /*$$slots*/
      s[4].default ? i ? (i.p(s, a), a & /*$$slots*/
      16 && je(i, 1)) : (i = Ut(s), i.c(), je(i, 1), i.m(o.parentNode, o)) : i && (Vn(), yt(i, 1, 1, () => {
        i = null;
      }), zn());
    },
    i(s) {
      n || (je(i), n = !0);
    },
    o(s) {
      yt(i), n = !1;
    },
    d(s) {
      s && (ce(t), ce(r), ce(o)), e[8](null), i && i.d(s);
    }
  };
}
function Wt(e) {
  const {
    svelteInit: t,
    ...r
  } = e;
  return r;
}
function Jn(e, t, r) {
  let o, n, {
    $$slots: i = {},
    $$scope: s
  } = t;
  const a = kn(i);
  let {
    svelteInit: c
  } = t;
  const l = $e(Wt(t)), f = $e();
  Bt(e, f, (b) => r(0, o = b));
  const u = $e();
  Bt(e, u, (b) => r(1, n = b));
  const d = [], h = Kn("$$ms-gr-react-wrapper"), {
    slotKey: v,
    slotIndex: g,
    subSlotIndex: m
  } = an() || {}, y = c({
    parent: h,
    props: l,
    target: f,
    slot: u,
    slotKey: v,
    slotIndex: g,
    subSlotIndex: m,
    onDestroy(b) {
      d.push(b);
    }
  });
  Qn("$$ms-gr-react-wrapper", y), Wn(() => {
    l.set(Wt(t));
  }), qn(() => {
    d.forEach((b) => b());
  });
  function S(b) {
    Vt[b ? "unshift" : "push"](() => {
      o = b, f.set(o);
    });
  }
  function w(b) {
    Vt[b ? "unshift" : "push"](() => {
      n = b, u.set(n);
    });
  }
  return e.$$set = (b) => {
    r(17, t = Ht(Ht({}, t), Xt(b))), "svelteInit" in b && r(5, c = b.svelteInit), "$$scope" in b && r(6, s = b.$$scope);
  }, t = Xt(t), [o, n, f, u, a, c, s, i, S, w];
}
class Zn extends jn {
  constructor(t) {
    super(), Bn(this, t, Jn, Yn, Gn, {
      svelteInit: 5
    });
  }
}
const {
  SvelteComponent: qi
} = window.__gradio__svelte__internal, Kt = window.ms_globals.rerender, ot = window.ms_globals.tree;
function eo(e, t = {}) {
  function r(o) {
    const n = $e(), i = new Zn({
      ...o,
      props: {
        svelteInit(s) {
          window.ms_globals.autokey += 1;
          const a = {
            key: window.ms_globals.autokey,
            svelteInstance: n,
            reactComponent: e,
            props: s.props,
            slot: s.slot,
            target: s.target,
            slotIndex: s.slotIndex,
            subSlotIndex: s.subSlotIndex,
            ignore: t.ignore,
            slotKey: s.slotKey,
            nodes: []
          }, c = s.parent ?? ot;
          return c.nodes = [...c.nodes, a], Kt({
            createPortal: pt,
            node: ot
          }), s.onDestroy(() => {
            c.nodes = c.nodes.filter((l) => l.svelteInstance !== n), Kt({
              createPortal: pt,
              node: ot
            });
          }), a;
        },
        ...o.props
      }
    });
    return n.set(i), i;
  }
  return new Promise((o) => {
    window.ms_globals.initializePromise.then(() => {
      o(r);
    });
  });
}
const to = "1.3.0", ro = /* @__PURE__ */ x.createContext({}), no = {
  classNames: {},
  styles: {},
  className: "",
  style: {}
}, oo = (e) => {
  const t = x.useContext(ro);
  return x.useMemo(() => ({
    ...no,
    ...t[e]
  }), [t[e]]);
};
function fe() {
  return fe = Object.assign ? Object.assign.bind() : function(e) {
    for (var t = 1; t < arguments.length; t++) {
      var r = arguments[t];
      for (var o in r) ({}).hasOwnProperty.call(r, o) && (e[o] = r[o]);
    }
    return e;
  }, fe.apply(null, arguments);
}
const io = "ant";
function bt() {
  const {
    getPrefixCls: e,
    direction: t,
    csp: r,
    iconPrefixCls: o,
    theme: n
  } = x.useContext(un.ConfigContext);
  return {
    theme: n,
    getPrefixCls: e,
    direction: t,
    csp: r,
    iconPrefixCls: o
  };
}
function ve(e) {
  var t = M.useRef();
  t.current = e;
  var r = M.useCallback(function() {
    for (var o, n = arguments.length, i = new Array(n), s = 0; s < n; s++)
      i[s] = arguments[s];
    return (o = t.current) === null || o === void 0 ? void 0 : o.call.apply(o, [t].concat(i));
  }, []);
  return r;
}
function so(e) {
  if (Array.isArray(e)) return e;
}
function ao(e, t) {
  var r = e == null ? null : typeof Symbol < "u" && e[Symbol.iterator] || e["@@iterator"];
  if (r != null) {
    var o, n, i, s, a = [], c = !0, l = !1;
    try {
      if (i = (r = r.call(e)).next, t !== 0) for (; !(c = (o = i.call(r)).done) && (a.push(o.value), a.length !== t); c = !0) ;
    } catch (f) {
      l = !0, n = f;
    } finally {
      try {
        if (!c && r.return != null && (s = r.return(), Object(s) !== s)) return;
      } finally {
        if (l) throw n;
      }
    }
    return a;
  }
}
function qt(e, t) {
  (t == null || t > e.length) && (t = e.length);
  for (var r = 0, o = Array(t); r < t; r++) o[r] = e[r];
  return o;
}
function co(e, t) {
  if (e) {
    if (typeof e == "string") return qt(e, t);
    var r = {}.toString.call(e).slice(8, -1);
    return r === "Object" && e.constructor && (r = e.constructor.name), r === "Map" || r === "Set" ? Array.from(e) : r === "Arguments" || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r) ? qt(e, t) : void 0;
  }
}
function lo() {
  throw new TypeError(`Invalid attempt to destructure non-iterable instance.
In order to be iterable, non-array objects must have a [Symbol.iterator]() method.`);
}
function De(e, t) {
  return so(e) || ao(e, t) || co(e, t) || lo();
}
function Fe() {
  return !!(typeof window < "u" && window.document && window.document.createElement);
}
var Qt = Fe() ? M.useLayoutEffect : M.useEffect, uo = function(t, r) {
  var o = M.useRef(!0);
  Qt(function() {
    return t(o.current);
  }, r), Qt(function() {
    return o.current = !1, function() {
      o.current = !0;
    };
  }, []);
}, Yt = function(t, r) {
  uo(function(o) {
    if (!o)
      return t();
  }, r);
};
function ye(e) {
  var t = M.useRef(!1), r = M.useState(e), o = De(r, 2), n = o[0], i = o[1];
  M.useEffect(function() {
    return t.current = !1, function() {
      t.current = !0;
    };
  }, []);
  function s(a, c) {
    c && t.current || i(a);
  }
  return [n, s];
}
function it(e) {
  return e !== void 0;
}
function fo(e, t) {
  var r = t || {}, o = r.defaultValue, n = r.value, i = r.onChange, s = r.postState, a = ye(function() {
    return it(n) ? n : it(o) ? typeof o == "function" ? o() : o : typeof e == "function" ? e() : e;
  }), c = De(a, 2), l = c[0], f = c[1], u = n !== void 0 ? n : l, d = s ? s(u) : u, h = ve(i), v = ye([u]), g = De(v, 2), m = g[0], y = g[1];
  Yt(function() {
    var w = m[0];
    l !== w && h(l, w);
  }, [m]), Yt(function() {
    it(n) || f(n);
  }, [n]);
  var S = ve(function(w, b) {
    f(w, b), y([u], b);
  });
  return [d, S];
}
function te(e) {
  "@babel/helpers - typeof";
  return te = typeof Symbol == "function" && typeof Symbol.iterator == "symbol" ? function(t) {
    return typeof t;
  } : function(t) {
    return t && typeof Symbol == "function" && t.constructor === Symbol && t !== Symbol.prototype ? "symbol" : typeof t;
  }, te(e);
}
var wr = {
  exports: {}
}, O = {};
/**
 * @license React
 * react-is.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var Mt = Symbol.for("react.element"), Ot = Symbol.for("react.portal"), He = Symbol.for("react.fragment"), Ve = Symbol.for("react.strict_mode"), Be = Symbol.for("react.profiler"), Ge = Symbol.for("react.provider"), Xe = Symbol.for("react.context"), mo = Symbol.for("react.server_context"), Ue = Symbol.for("react.forward_ref"), We = Symbol.for("react.suspense"), Ke = Symbol.for("react.suspense_list"), qe = Symbol.for("react.memo"), Qe = Symbol.for("react.lazy"), ho = Symbol.for("react.offscreen"), Tr;
Tr = Symbol.for("react.module.reference");
function U(e) {
  if (typeof e == "object" && e !== null) {
    var t = e.$$typeof;
    switch (t) {
      case Mt:
        switch (e = e.type, e) {
          case He:
          case Be:
          case Ve:
          case We:
          case Ke:
            return e;
          default:
            switch (e = e && e.$$typeof, e) {
              case mo:
              case Xe:
              case Ue:
              case Qe:
              case qe:
              case Ge:
                return e;
              default:
                return t;
            }
        }
      case Ot:
        return t;
    }
  }
}
O.ContextConsumer = Xe;
O.ContextProvider = Ge;
O.Element = Mt;
O.ForwardRef = Ue;
O.Fragment = He;
O.Lazy = Qe;
O.Memo = qe;
O.Portal = Ot;
O.Profiler = Be;
O.StrictMode = Ve;
O.Suspense = We;
O.SuspenseList = Ke;
O.isAsyncMode = function() {
  return !1;
};
O.isConcurrentMode = function() {
  return !1;
};
O.isContextConsumer = function(e) {
  return U(e) === Xe;
};
O.isContextProvider = function(e) {
  return U(e) === Ge;
};
O.isElement = function(e) {
  return typeof e == "object" && e !== null && e.$$typeof === Mt;
};
O.isForwardRef = function(e) {
  return U(e) === Ue;
};
O.isFragment = function(e) {
  return U(e) === He;
};
O.isLazy = function(e) {
  return U(e) === Qe;
};
O.isMemo = function(e) {
  return U(e) === qe;
};
O.isPortal = function(e) {
  return U(e) === Ot;
};
O.isProfiler = function(e) {
  return U(e) === Be;
};
O.isStrictMode = function(e) {
  return U(e) === Ve;
};
O.isSuspense = function(e) {
  return U(e) === We;
};
O.isSuspenseList = function(e) {
  return U(e) === Ke;
};
O.isValidElementType = function(e) {
  return typeof e == "string" || typeof e == "function" || e === He || e === Be || e === Ve || e === We || e === Ke || e === ho || typeof e == "object" && e !== null && (e.$$typeof === Qe || e.$$typeof === qe || e.$$typeof === Ge || e.$$typeof === Xe || e.$$typeof === Ue || e.$$typeof === Tr || e.getModuleId !== void 0);
};
O.typeOf = U;
wr.exports = O;
var st = wr.exports, po = Symbol.for("react.element"), go = Symbol.for("react.transitional.element"), vo = Symbol.for("react.fragment");
function yo(e) {
  return (
    // Base object type
    e && te(e) === "object" && // React Element type
    (e.$$typeof === po || e.$$typeof === go) && // React Fragment type
    e.type === vo
  );
}
var bo = Number(Zr.split(".")[0]), So = function(t, r) {
  typeof t == "function" ? t(r) : te(t) === "object" && t && "current" in t && (t.current = r);
}, xo = function(t) {
  var r, o;
  if (!t)
    return !1;
  if (Pr(t) && bo >= 19)
    return !0;
  var n = st.isMemo(t) ? t.type.type : t.type;
  return !(typeof n == "function" && !((r = n.prototype) !== null && r !== void 0 && r.render) && n.$$typeof !== st.ForwardRef || typeof t == "function" && !((o = t.prototype) !== null && o !== void 0 && o.render) && t.$$typeof !== st.ForwardRef);
};
function Pr(e) {
  return /* @__PURE__ */ Jr(e) && !yo(e);
}
var Co = function(t) {
  if (t && Pr(t)) {
    var r = t;
    return r.props.propertyIsEnumerable("ref") ? r.props.ref : r.ref;
  }
  return null;
};
function Eo(e, t) {
  if (te(e) != "object" || !e) return e;
  var r = e[Symbol.toPrimitive];
  if (r !== void 0) {
    var o = r.call(e, t);
    if (te(o) != "object") return o;
    throw new TypeError("@@toPrimitive must return a primitive value.");
  }
  return (t === "string" ? String : Number)(e);
}
function _o(e) {
  var t = Eo(e, "string");
  return te(t) == "symbol" ? t : t + "";
}
function wo(e, t, r) {
  return (t = _o(t)) in e ? Object.defineProperty(e, t, {
    value: r,
    enumerable: !0,
    configurable: !0,
    writable: !0
  }) : e[t] = r, e;
}
function Jt(e, t) {
  var r = Object.keys(e);
  if (Object.getOwnPropertySymbols) {
    var o = Object.getOwnPropertySymbols(e);
    t && (o = o.filter(function(n) {
      return Object.getOwnPropertyDescriptor(e, n).enumerable;
    })), r.push.apply(r, o);
  }
  return r;
}
function To(e) {
  for (var t = 1; t < arguments.length; t++) {
    var r = arguments[t] != null ? arguments[t] : {};
    t % 2 ? Jt(Object(r), !0).forEach(function(o) {
      wo(e, o, r[o]);
    }) : Object.getOwnPropertyDescriptors ? Object.defineProperties(e, Object.getOwnPropertyDescriptors(r)) : Jt(Object(r)).forEach(function(o) {
      Object.defineProperty(e, o, Object.getOwnPropertyDescriptor(r, o));
    });
  }
  return e;
}
function F(e) {
  "@babel/helpers - typeof";
  return F = typeof Symbol == "function" && typeof Symbol.iterator == "symbol" ? function(t) {
    return typeof t;
  } : function(t) {
    return t && typeof Symbol == "function" && t.constructor === Symbol && t !== Symbol.prototype ? "symbol" : typeof t;
  }, F(e);
}
function Po(e, t) {
  if (F(e) != "object" || !e) return e;
  var r = e[Symbol.toPrimitive];
  if (r !== void 0) {
    var o = r.call(e, t);
    if (F(o) != "object") return o;
    throw new TypeError("@@toPrimitive must return a primitive value.");
  }
  return (t === "string" ? String : Number)(e);
}
function Mr(e) {
  var t = Po(e, "string");
  return F(t) == "symbol" ? t : t + "";
}
function E(e, t, r) {
  return (t = Mr(t)) in e ? Object.defineProperty(e, t, {
    value: r,
    enumerable: !0,
    configurable: !0,
    writable: !0
  }) : e[t] = r, e;
}
function Zt(e, t) {
  var r = Object.keys(e);
  if (Object.getOwnPropertySymbols) {
    var o = Object.getOwnPropertySymbols(e);
    t && (o = o.filter(function(n) {
      return Object.getOwnPropertyDescriptor(e, n).enumerable;
    })), r.push.apply(r, o);
  }
  return r;
}
function C(e) {
  for (var t = 1; t < arguments.length; t++) {
    var r = arguments[t] != null ? arguments[t] : {};
    t % 2 ? Zt(Object(r), !0).forEach(function(o) {
      E(e, o, r[o]);
    }) : Object.getOwnPropertyDescriptors ? Object.defineProperties(e, Object.getOwnPropertyDescriptors(r)) : Zt(Object(r)).forEach(function(o) {
      Object.defineProperty(e, o, Object.getOwnPropertyDescriptor(r, o));
    });
  }
  return e;
}
function Mo(e) {
  if (Array.isArray(e)) return e;
}
function Oo(e, t) {
  var r = e == null ? null : typeof Symbol < "u" && e[Symbol.iterator] || e["@@iterator"];
  if (r != null) {
    var o, n, i, s, a = [], c = !0, l = !1;
    try {
      if (i = (r = r.call(e)).next, t === 0) {
        if (Object(r) !== r) return;
        c = !1;
      } else for (; !(c = (o = i.call(r)).done) && (a.push(o.value), a.length !== t); c = !0) ;
    } catch (f) {
      l = !0, n = f;
    } finally {
      try {
        if (!c && r.return != null && (s = r.return(), Object(s) !== s)) return;
      } finally {
        if (l) throw n;
      }
    }
    return a;
  }
}
function er(e, t) {
  (t == null || t > e.length) && (t = e.length);
  for (var r = 0, o = Array(t); r < t; r++) o[r] = e[r];
  return o;
}
function Ro(e, t) {
  if (e) {
    if (typeof e == "string") return er(e, t);
    var r = {}.toString.call(e).slice(8, -1);
    return r === "Object" && e.constructor && (r = e.constructor.name), r === "Map" || r === "Set" ? Array.from(e) : r === "Arguments" || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r) ? er(e, t) : void 0;
  }
}
function Lo() {
  throw new TypeError(`Invalid attempt to destructure non-iterable instance.
In order to be iterable, non-array objects must have a [Symbol.iterator]() method.`);
}
function X(e, t) {
  return Mo(e) || Oo(e, t) || Ro(e, t) || Lo();
}
function tr(e) {
  return e instanceof HTMLElement || e instanceof SVGElement;
}
function Ao(e) {
  return e && te(e) === "object" && tr(e.nativeElement) ? e.nativeElement : tr(e) ? e : null;
}
function $o(e) {
  var t = Ao(e);
  if (t)
    return t;
  if (e instanceof x.Component) {
    var r;
    return (r = jt.findDOMNode) === null || r === void 0 ? void 0 : r.call(jt, e);
  }
  return null;
}
function Io(e, t) {
  if (e == null) return {};
  var r = {};
  for (var o in e) if ({}.hasOwnProperty.call(e, o)) {
    if (t.indexOf(o) !== -1) continue;
    r[o] = e[o];
  }
  return r;
}
function rr(e, t) {
  if (e == null) return {};
  var r, o, n = Io(e, t);
  if (Object.getOwnPropertySymbols) {
    var i = Object.getOwnPropertySymbols(e);
    for (o = 0; o < i.length; o++) r = i[o], t.indexOf(r) === -1 && {}.propertyIsEnumerable.call(e, r) && (n[r] = e[r]);
  }
  return n;
}
var jo = /* @__PURE__ */ M.createContext({});
function de(e, t) {
  if (!(e instanceof t)) throw new TypeError("Cannot call a class as a function");
}
function nr(e, t) {
  for (var r = 0; r < t.length; r++) {
    var o = t[r];
    o.enumerable = o.enumerable || !1, o.configurable = !0, "value" in o && (o.writable = !0), Object.defineProperty(e, Mr(o.key), o);
  }
}
function me(e, t, r) {
  return t && nr(e.prototype, t), r && nr(e, r), Object.defineProperty(e, "prototype", {
    writable: !1
  }), e;
}
function St(e, t) {
  return St = Object.setPrototypeOf ? Object.setPrototypeOf.bind() : function(r, o) {
    return r.__proto__ = o, r;
  }, St(e, t);
}
function Ye(e, t) {
  if (typeof t != "function" && t !== null) throw new TypeError("Super expression must either be null or a function");
  e.prototype = Object.create(t && t.prototype, {
    constructor: {
      value: e,
      writable: !0,
      configurable: !0
    }
  }), Object.defineProperty(e, "prototype", {
    writable: !1
  }), t && St(e, t);
}
function ke(e) {
  return ke = Object.setPrototypeOf ? Object.getPrototypeOf.bind() : function(t) {
    return t.__proto__ || Object.getPrototypeOf(t);
  }, ke(e);
}
function Or() {
  try {
    var e = !Boolean.prototype.valueOf.call(Reflect.construct(Boolean, [], function() {
    }));
  } catch {
  }
  return (Or = function() {
    return !!e;
  })();
}
function ae(e) {
  if (e === void 0) throw new ReferenceError("this hasn't been initialised - super() hasn't been called");
  return e;
}
function zo(e, t) {
  if (t && (F(t) == "object" || typeof t == "function")) return t;
  if (t !== void 0) throw new TypeError("Derived constructors may only return object or undefined");
  return ae(e);
}
function Je(e) {
  var t = Or();
  return function() {
    var r, o = ke(e);
    if (t) {
      var n = ke(this).constructor;
      r = Reflect.construct(o, arguments, n);
    } else r = o.apply(this, arguments);
    return zo(this, r);
  };
}
var Do = /* @__PURE__ */ function(e) {
  Ye(r, e);
  var t = Je(r);
  function r() {
    return de(this, r), t.apply(this, arguments);
  }
  return me(r, [{
    key: "render",
    value: function() {
      return this.props.children;
    }
  }]), r;
}(M.Component);
function ko(e) {
  var t = M.useReducer(function(a) {
    return a + 1;
  }, 0), r = De(t, 2), o = r[1], n = M.useRef(e), i = ve(function() {
    return n.current;
  }), s = ve(function(a) {
    n.current = typeof a == "function" ? a(n.current) : a, o();
  });
  return [i, s];
}
var Z = "none", Me = "appear", Oe = "enter", Re = "leave", or = "none", W = "prepare", le = "start", ue = "active", Rt = "end", Rr = "prepared";
function ir(e, t) {
  var r = {};
  return r[e.toLowerCase()] = t.toLowerCase(), r["Webkit".concat(e)] = "webkit".concat(t), r["Moz".concat(e)] = "moz".concat(t), r["ms".concat(e)] = "MS".concat(t), r["O".concat(e)] = "o".concat(t.toLowerCase()), r;
}
function No(e, t) {
  var r = {
    animationend: ir("Animation", "AnimationEnd"),
    transitionend: ir("Transition", "TransitionEnd")
  };
  return e && ("AnimationEvent" in t || delete r.animationend.animation, "TransitionEvent" in t || delete r.transitionend.transition), r;
}
var Fo = No(Fe(), typeof window < "u" ? window : {}), Lr = {};
if (Fe()) {
  var Ho = document.createElement("div");
  Lr = Ho.style;
}
var Le = {};
function Ar(e) {
  if (Le[e])
    return Le[e];
  var t = Fo[e];
  if (t)
    for (var r = Object.keys(t), o = r.length, n = 0; n < o; n += 1) {
      var i = r[n];
      if (Object.prototype.hasOwnProperty.call(t, i) && i in Lr)
        return Le[e] = t[i], Le[e];
    }
  return "";
}
var $r = Ar("animationend"), Ir = Ar("transitionend"), jr = !!($r && Ir), sr = $r || "animationend", ar = Ir || "transitionend";
function cr(e, t) {
  if (!e) return null;
  if (F(e) === "object") {
    var r = t.replace(/-\w/g, function(o) {
      return o[1].toUpperCase();
    });
    return e[r];
  }
  return "".concat(e, "-").concat(t);
}
const Vo = function(e) {
  var t = ee();
  function r(n) {
    n && (n.removeEventListener(ar, e), n.removeEventListener(sr, e));
  }
  function o(n) {
    t.current && t.current !== n && r(t.current), n && n !== t.current && (n.addEventListener(ar, e), n.addEventListener(sr, e), t.current = n);
  }
  return M.useEffect(function() {
    return function() {
      r(t.current);
    };
  }, []), [o, r];
};
var zr = Fe() ? en : ge, Dr = function(t) {
  return +setTimeout(t, 16);
}, kr = function(t) {
  return clearTimeout(t);
};
typeof window < "u" && "requestAnimationFrame" in window && (Dr = function(t) {
  return window.requestAnimationFrame(t);
}, kr = function(t) {
  return window.cancelAnimationFrame(t);
});
var lr = 0, Lt = /* @__PURE__ */ new Map();
function Nr(e) {
  Lt.delete(e);
}
var xt = function(t) {
  var r = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : 1;
  lr += 1;
  var o = lr;
  function n(i) {
    if (i === 0)
      Nr(o), t();
    else {
      var s = Dr(function() {
        n(i - 1);
      });
      Lt.set(o, s);
    }
  }
  return n(r), o;
};
xt.cancel = function(e) {
  var t = Lt.get(e);
  return Nr(e), kr(t);
};
const Bo = function() {
  var e = M.useRef(null);
  function t() {
    xt.cancel(e.current);
  }
  function r(o) {
    var n = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : 2;
    t();
    var i = xt(function() {
      n <= 1 ? o({
        isCanceled: function() {
          return i !== e.current;
        }
      }) : r(o, n - 1);
    });
    e.current = i;
  }
  return M.useEffect(function() {
    return function() {
      t();
    };
  }, []), [r, t];
};
var Go = [W, le, ue, Rt], Xo = [W, Rr], Fr = !1, Uo = !0;
function Hr(e) {
  return e === ue || e === Rt;
}
const Wo = function(e, t, r) {
  var o = ye(or), n = X(o, 2), i = n[0], s = n[1], a = Bo(), c = X(a, 2), l = c[0], f = c[1];
  function u() {
    s(W, !0);
  }
  var d = t ? Xo : Go;
  return zr(function() {
    if (i !== or && i !== Rt) {
      var h = d.indexOf(i), v = d[h + 1], g = r(i);
      g === Fr ? s(v, !0) : v && l(function(m) {
        function y() {
          m.isCanceled() || s(v, !0);
        }
        g === !0 ? y() : Promise.resolve(g).then(y);
      });
    }
  }, [e, i]), M.useEffect(function() {
    return function() {
      f();
    };
  }, []), [u, i];
};
function Ko(e, t, r, o) {
  var n = o.motionEnter, i = n === void 0 ? !0 : n, s = o.motionAppear, a = s === void 0 ? !0 : s, c = o.motionLeave, l = c === void 0 ? !0 : c, f = o.motionDeadline, u = o.motionLeaveImmediately, d = o.onAppearPrepare, h = o.onEnterPrepare, v = o.onLeavePrepare, g = o.onAppearStart, m = o.onEnterStart, y = o.onLeaveStart, S = o.onAppearActive, w = o.onEnterActive, b = o.onLeaveActive, _ = o.onAppearEnd, p = o.onEnterEnd, P = o.onLeaveEnd, T = o.onVisibleChanged, R = ye(), L = X(R, 2), A = L[0], $ = L[1], I = ko(Z), j = X(I, 2), z = j[0], H = j[1], re = ye(null), J = X(re, 2), be = J[0], Se = J[1], V = z(), ne = ee(!1), he = ee(null);
  function B() {
    return r();
  }
  var oe = ee(!1);
  function xe() {
    H(Z), Se(null, !0);
  }
  var Q = ve(function(N) {
    var k = z();
    if (k !== Z) {
      var K = B();
      if (!(N && !N.deadline && N.target !== K)) {
        var Te = oe.current, Pe;
        k === Me && Te ? Pe = _ == null ? void 0 : _(K, N) : k === Oe && Te ? Pe = p == null ? void 0 : p(K, N) : k === Re && Te && (Pe = P == null ? void 0 : P(K, N)), Te && Pe !== !1 && xe();
      }
    }
  }), Ze = Vo(Q), Ce = X(Ze, 1), Ee = Ce[0], _e = function(k) {
    switch (k) {
      case Me:
        return E(E(E({}, W, d), le, g), ue, S);
      case Oe:
        return E(E(E({}, W, h), le, m), ue, w);
      case Re:
        return E(E(E({}, W, v), le, y), ue, b);
      default:
        return {};
    }
  }, ie = M.useMemo(function() {
    return _e(V);
  }, [V]), we = Wo(V, !e, function(N) {
    if (N === W) {
      var k = ie[W];
      return k ? k(B()) : Fr;
    }
    if (se in ie) {
      var K;
      Se(((K = ie[se]) === null || K === void 0 ? void 0 : K.call(ie, B(), null)) || null);
    }
    return se === ue && V !== Z && (Ee(B()), f > 0 && (clearTimeout(he.current), he.current = setTimeout(function() {
      Q({
        deadline: !0
      });
    }, f))), se === Rr && xe(), Uo;
  }), $t = X(we, 2), Qr = $t[0], se = $t[1], Yr = Hr(se);
  oe.current = Yr;
  var It = ee(null);
  zr(function() {
    if (!(ne.current && It.current === t)) {
      $(t);
      var N = ne.current;
      ne.current = !0;
      var k;
      !N && t && a && (k = Me), N && t && i && (k = Oe), (N && !t && l || !N && u && !t && l) && (k = Re);
      var K = _e(k);
      k && (e || K[W]) ? (H(k), Qr()) : H(Z), It.current = t;
    }
  }, [t]), ge(function() {
    // Cancel appear
    (V === Me && !a || // Cancel enter
    V === Oe && !i || // Cancel leave
    V === Re && !l) && H(Z);
  }, [a, i, l]), ge(function() {
    return function() {
      ne.current = !1, clearTimeout(he.current);
    };
  }, []);
  var et = M.useRef(!1);
  ge(function() {
    A && (et.current = !0), A !== void 0 && V === Z && ((et.current || A) && (T == null || T(A)), et.current = !0);
  }, [A, V]);
  var tt = be;
  return ie[W] && se === le && (tt = C({
    transition: "none"
  }, tt)), [V, se, tt, A ?? t];
}
function qo(e) {
  var t = e;
  F(e) === "object" && (t = e.transitionSupport);
  function r(n, i) {
    return !!(n.motionName && t && i !== !1);
  }
  var o = /* @__PURE__ */ M.forwardRef(function(n, i) {
    var s = n.visible, a = s === void 0 ? !0 : s, c = n.removeOnLeave, l = c === void 0 ? !0 : c, f = n.forceRender, u = n.children, d = n.motionName, h = n.leavedClassName, v = n.eventProps, g = M.useContext(jo), m = g.motion, y = r(n, m), S = ee(), w = ee();
    function b() {
      try {
        return S.current instanceof HTMLElement ? S.current : $o(w.current);
      } catch {
        return null;
      }
    }
    var _ = Ko(y, a, b, n), p = X(_, 4), P = p[0], T = p[1], R = p[2], L = p[3], A = M.useRef(L);
    L && (A.current = !0);
    var $ = M.useCallback(function(J) {
      S.current = J, So(i, J);
    }, [i]), I, j = C(C({}, v), {}, {
      visible: a
    });
    if (!u)
      I = null;
    else if (P === Z)
      L ? I = u(C({}, j), $) : !l && A.current && h ? I = u(C(C({}, j), {}, {
        className: h
      }), $) : f || !l && !h ? I = u(C(C({}, j), {}, {
        style: {
          display: "none"
        }
      }), $) : I = null;
    else {
      var z;
      T === W ? z = "prepare" : Hr(T) ? z = "active" : T === le && (z = "start");
      var H = cr(d, "".concat(P, "-").concat(z));
      I = u(C(C({}, j), {}, {
        className: G(cr(d, P), E(E({}, H, H && z), d, typeof d == "string")),
        style: R
      }), $);
    }
    if (/* @__PURE__ */ M.isValidElement(I) && xo(I)) {
      var re = Co(I);
      re || (I = /* @__PURE__ */ M.cloneElement(I, {
        ref: $
      }));
    }
    return /* @__PURE__ */ M.createElement(Do, {
      ref: w
    }, I);
  });
  return o.displayName = "CSSMotion", o;
}
const Vr = qo(jr);
var Ct = "add", Et = "keep", _t = "remove", at = "removed";
function Qo(e) {
  var t;
  return e && F(e) === "object" && "key" in e ? t = e : t = {
    key: e
  }, C(C({}, t), {}, {
    key: String(t.key)
  });
}
function wt() {
  var e = arguments.length > 0 && arguments[0] !== void 0 ? arguments[0] : [];
  return e.map(Qo);
}
function Yo() {
  var e = arguments.length > 0 && arguments[0] !== void 0 ? arguments[0] : [], t = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : [], r = [], o = 0, n = t.length, i = wt(e), s = wt(t);
  i.forEach(function(l) {
    for (var f = !1, u = o; u < n; u += 1) {
      var d = s[u];
      if (d.key === l.key) {
        o < u && (r = r.concat(s.slice(o, u).map(function(h) {
          return C(C({}, h), {}, {
            status: Ct
          });
        })), o = u), r.push(C(C({}, d), {}, {
          status: Et
        })), o += 1, f = !0;
        break;
      }
    }
    f || r.push(C(C({}, l), {}, {
      status: _t
    }));
  }), o < n && (r = r.concat(s.slice(o).map(function(l) {
    return C(C({}, l), {}, {
      status: Ct
    });
  })));
  var a = {};
  r.forEach(function(l) {
    var f = l.key;
    a[f] = (a[f] || 0) + 1;
  });
  var c = Object.keys(a).filter(function(l) {
    return a[l] > 1;
  });
  return c.forEach(function(l) {
    r = r.filter(function(f) {
      var u = f.key, d = f.status;
      return u !== l || d !== _t;
    }), r.forEach(function(f) {
      f.key === l && (f.status = Et);
    });
  }), r;
}
var Jo = ["component", "children", "onVisibleChanged", "onAllRemoved"], Zo = ["status"], ei = ["eventProps", "visible", "children", "motionName", "motionAppear", "motionEnter", "motionLeave", "motionLeaveImmediately", "motionDeadline", "removeOnLeave", "leavedClassName", "onAppearPrepare", "onAppearStart", "onAppearActive", "onAppearEnd", "onEnterStart", "onEnterActive", "onEnterEnd", "onLeaveStart", "onLeaveActive", "onLeaveEnd"];
function ti(e) {
  var t = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : Vr, r = /* @__PURE__ */ function(o) {
    Ye(i, o);
    var n = Je(i);
    function i() {
      var s;
      de(this, i);
      for (var a = arguments.length, c = new Array(a), l = 0; l < a; l++)
        c[l] = arguments[l];
      return s = n.call.apply(n, [this].concat(c)), E(ae(s), "state", {
        keyEntities: []
      }), E(ae(s), "removeKey", function(f) {
        s.setState(function(u) {
          var d = u.keyEntities.map(function(h) {
            return h.key !== f ? h : C(C({}, h), {}, {
              status: at
            });
          });
          return {
            keyEntities: d
          };
        }, function() {
          var u = s.state.keyEntities, d = u.filter(function(h) {
            var v = h.status;
            return v !== at;
          }).length;
          d === 0 && s.props.onAllRemoved && s.props.onAllRemoved();
        });
      }), s;
    }
    return me(i, [{
      key: "render",
      value: function() {
        var a = this, c = this.state.keyEntities, l = this.props, f = l.component, u = l.children, d = l.onVisibleChanged;
        l.onAllRemoved;
        var h = rr(l, Jo), v = f || M.Fragment, g = {};
        return ei.forEach(function(m) {
          g[m] = h[m], delete h[m];
        }), delete h.keys, /* @__PURE__ */ M.createElement(v, h, c.map(function(m, y) {
          var S = m.status, w = rr(m, Zo), b = S === Ct || S === Et;
          return /* @__PURE__ */ M.createElement(t, fe({}, g, {
            key: w.key,
            visible: b,
            eventProps: w,
            onVisibleChanged: function(p) {
              d == null || d(p, {
                key: w.key
              }), p || a.removeKey(w.key);
            }
          }), function(_, p) {
            return u(C(C({}, _), {}, {
              index: y
            }), p);
          });
        }));
      }
    }], [{
      key: "getDerivedStateFromProps",
      value: function(a, c) {
        var l = a.keys, f = c.keyEntities, u = wt(l), d = Yo(f, u);
        return {
          keyEntities: d.filter(function(h) {
            var v = f.find(function(g) {
              var m = g.key;
              return h.key === m;
            });
            return !(v && v.status === at && h.status === _t);
          })
        };
      }
    }]), i;
  }(M.Component);
  return E(r, "defaultProps", {
    component: "div"
  }), r;
}
ti(jr);
var Br = /* @__PURE__ */ me(function e() {
  de(this, e);
}), Gr = "CALC_UNIT", ri = new RegExp(Gr, "g");
function ct(e) {
  return typeof e == "number" ? "".concat(e).concat(Gr) : e;
}
var ni = /* @__PURE__ */ function(e) {
  Ye(r, e);
  var t = Je(r);
  function r(o, n) {
    var i;
    de(this, r), i = t.call(this), E(ae(i), "result", ""), E(ae(i), "unitlessCssVar", void 0), E(ae(i), "lowPriority", void 0);
    var s = F(o);
    return i.unitlessCssVar = n, o instanceof r ? i.result = "(".concat(o.result, ")") : s === "number" ? i.result = ct(o) : s === "string" && (i.result = o), i;
  }
  return me(r, [{
    key: "add",
    value: function(n) {
      return n instanceof r ? this.result = "".concat(this.result, " + ").concat(n.getResult()) : (typeof n == "number" || typeof n == "string") && (this.result = "".concat(this.result, " + ").concat(ct(n))), this.lowPriority = !0, this;
    }
  }, {
    key: "sub",
    value: function(n) {
      return n instanceof r ? this.result = "".concat(this.result, " - ").concat(n.getResult()) : (typeof n == "number" || typeof n == "string") && (this.result = "".concat(this.result, " - ").concat(ct(n))), this.lowPriority = !0, this;
    }
  }, {
    key: "mul",
    value: function(n) {
      return this.lowPriority && (this.result = "(".concat(this.result, ")")), n instanceof r ? this.result = "".concat(this.result, " * ").concat(n.getResult(!0)) : (typeof n == "number" || typeof n == "string") && (this.result = "".concat(this.result, " * ").concat(n)), this.lowPriority = !1, this;
    }
  }, {
    key: "div",
    value: function(n) {
      return this.lowPriority && (this.result = "(".concat(this.result, ")")), n instanceof r ? this.result = "".concat(this.result, " / ").concat(n.getResult(!0)) : (typeof n == "number" || typeof n == "string") && (this.result = "".concat(this.result, " / ").concat(n)), this.lowPriority = !1, this;
    }
  }, {
    key: "getResult",
    value: function(n) {
      return this.lowPriority || n ? "(".concat(this.result, ")") : this.result;
    }
  }, {
    key: "equal",
    value: function(n) {
      var i = this, s = n || {}, a = s.unit, c = !0;
      return typeof a == "boolean" ? c = a : Array.from(this.unitlessCssVar).some(function(l) {
        return i.result.includes(l);
      }) && (c = !1), this.result = this.result.replace(ri, c ? "px" : ""), typeof this.lowPriority < "u" ? "calc(".concat(this.result, ")") : this.result;
    }
  }]), r;
}(Br), oi = /* @__PURE__ */ function(e) {
  Ye(r, e);
  var t = Je(r);
  function r(o) {
    var n;
    return de(this, r), n = t.call(this), E(ae(n), "result", 0), o instanceof r ? n.result = o.result : typeof o == "number" && (n.result = o), n;
  }
  return me(r, [{
    key: "add",
    value: function(n) {
      return n instanceof r ? this.result += n.result : typeof n == "number" && (this.result += n), this;
    }
  }, {
    key: "sub",
    value: function(n) {
      return n instanceof r ? this.result -= n.result : typeof n == "number" && (this.result -= n), this;
    }
  }, {
    key: "mul",
    value: function(n) {
      return n instanceof r ? this.result *= n.result : typeof n == "number" && (this.result *= n), this;
    }
  }, {
    key: "div",
    value: function(n) {
      return n instanceof r ? this.result /= n.result : typeof n == "number" && (this.result /= n), this;
    }
  }, {
    key: "equal",
    value: function() {
      return this.result;
    }
  }]), r;
}(Br), ii = function(t, r) {
  var o = t === "css" ? ni : oi;
  return function(n) {
    return new o(n, r);
  };
}, ur = function(t, r) {
  return "".concat([r, t.replace(/([A-Z]+)([A-Z][a-z]+)/g, "$1-$2").replace(/([a-z])([A-Z])/g, "$1-$2")].filter(Boolean).join("-"));
};
function fr(e, t, r, o) {
  var n = C({}, t[e]);
  if (o != null && o.deprecatedTokens) {
    var i = o.deprecatedTokens;
    i.forEach(function(a) {
      var c = X(a, 2), l = c[0], f = c[1];
      if (n != null && n[l] || n != null && n[f]) {
        var u;
        (u = n[f]) !== null && u !== void 0 || (n[f] = n == null ? void 0 : n[l]);
      }
    });
  }
  var s = C(C({}, r), n);
  return Object.keys(s).forEach(function(a) {
    s[a] === t[a] && delete s[a];
  }), s;
}
var Xr = typeof CSSINJS_STATISTIC < "u", Tt = !0;
function At() {
  for (var e = arguments.length, t = new Array(e), r = 0; r < e; r++)
    t[r] = arguments[r];
  if (!Xr)
    return Object.assign.apply(Object, [{}].concat(t));
  Tt = !1;
  var o = {};
  return t.forEach(function(n) {
    if (F(n) === "object") {
      var i = Object.keys(n);
      i.forEach(function(s) {
        Object.defineProperty(o, s, {
          configurable: !0,
          enumerable: !0,
          get: function() {
            return n[s];
          }
        });
      });
    }
  }), Tt = !0, o;
}
var dr = {};
function si() {
}
var ai = function(t) {
  var r, o = t, n = si;
  return Xr && typeof Proxy < "u" && (r = /* @__PURE__ */ new Set(), o = new Proxy(t, {
    get: function(s, a) {
      if (Tt) {
        var c;
        (c = r) === null || c === void 0 || c.add(a);
      }
      return s[a];
    }
  }), n = function(s, a) {
    var c;
    dr[s] = {
      global: Array.from(r),
      component: C(C({}, (c = dr[s]) === null || c === void 0 ? void 0 : c.component), a)
    };
  }), {
    token: o,
    keys: r,
    flush: n
  };
};
function mr(e, t, r) {
  if (typeof r == "function") {
    var o;
    return r(At(t, (o = t[e]) !== null && o !== void 0 ? o : {}));
  }
  return r ?? {};
}
function ci(e) {
  return e === "js" ? {
    max: Math.max,
    min: Math.min
  } : {
    max: function() {
      for (var r = arguments.length, o = new Array(r), n = 0; n < r; n++)
        o[n] = arguments[n];
      return "max(".concat(o.map(function(i) {
        return ze(i);
      }).join(","), ")");
    },
    min: function() {
      for (var r = arguments.length, o = new Array(r), n = 0; n < r; n++)
        o[n] = arguments[n];
      return "min(".concat(o.map(function(i) {
        return ze(i);
      }).join(","), ")");
    }
  };
}
var li = 1e3 * 60 * 10, ui = /* @__PURE__ */ function() {
  function e() {
    de(this, e), E(this, "map", /* @__PURE__ */ new Map()), E(this, "objectIDMap", /* @__PURE__ */ new WeakMap()), E(this, "nextID", 0), E(this, "lastAccessBeat", /* @__PURE__ */ new Map()), E(this, "accessBeat", 0);
  }
  return me(e, [{
    key: "set",
    value: function(r, o) {
      this.clear();
      var n = this.getCompositeKey(r);
      this.map.set(n, o), this.lastAccessBeat.set(n, Date.now());
    }
  }, {
    key: "get",
    value: function(r) {
      var o = this.getCompositeKey(r), n = this.map.get(o);
      return this.lastAccessBeat.set(o, Date.now()), this.accessBeat += 1, n;
    }
  }, {
    key: "getCompositeKey",
    value: function(r) {
      var o = this, n = r.map(function(i) {
        return i && F(i) === "object" ? "obj_".concat(o.getObjectID(i)) : "".concat(F(i), "_").concat(i);
      });
      return n.join("|");
    }
  }, {
    key: "getObjectID",
    value: function(r) {
      if (this.objectIDMap.has(r))
        return this.objectIDMap.get(r);
      var o = this.nextID;
      return this.objectIDMap.set(r, o), this.nextID += 1, o;
    }
  }, {
    key: "clear",
    value: function() {
      var r = this;
      if (this.accessBeat > 1e4) {
        var o = Date.now();
        this.lastAccessBeat.forEach(function(n, i) {
          o - n > li && (r.map.delete(i), r.lastAccessBeat.delete(i));
        }), this.accessBeat = 0;
      }
    }
  }]), e;
}(), hr = new ui();
function fi(e, t) {
  return x.useMemo(function() {
    var r = hr.get(t);
    if (r)
      return r;
    var o = e();
    return hr.set(t, o), o;
  }, t);
}
var di = function() {
  return {};
};
function mi(e) {
  var t = e.useCSP, r = t === void 0 ? di : t, o = e.useToken, n = e.usePrefix, i = e.getResetStyles, s = e.getCommonStyle, a = e.getCompUnitless;
  function c(d, h, v, g) {
    var m = Array.isArray(d) ? d[0] : d;
    function y(T) {
      return "".concat(String(m)).concat(T.slice(0, 1).toUpperCase()).concat(T.slice(1));
    }
    var S = (g == null ? void 0 : g.unitless) || {}, w = typeof a == "function" ? a(d) : {}, b = C(C({}, w), {}, E({}, y("zIndexPopup"), !0));
    Object.keys(S).forEach(function(T) {
      b[y(T)] = S[T];
    });
    var _ = C(C({}, g), {}, {
      unitless: b,
      prefixToken: y
    }), p = f(d, h, v, _), P = l(m, v, _);
    return function(T) {
      var R = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : T, L = p(T, R), A = X(L, 2), $ = A[1], I = P(R), j = X(I, 2), z = j[0], H = j[1];
      return [z, $, H];
    };
  }
  function l(d, h, v) {
    var g = v.unitless, m = v.injectStyle, y = m === void 0 ? !0 : m, S = v.prefixToken, w = v.ignore, b = function(P) {
      var T = P.rootCls, R = P.cssVar, L = R === void 0 ? {} : R, A = o(), $ = A.realToken;
      return dn({
        path: [d],
        prefix: L.prefix,
        key: L.key,
        unitless: g,
        ignore: w,
        token: $,
        scope: T
      }, function() {
        var I = mr(d, $, h), j = fr(d, $, I, {
          deprecatedTokens: v == null ? void 0 : v.deprecatedTokens
        });
        return Object.keys(I).forEach(function(z) {
          j[S(z)] = j[z], delete j[z];
        }), j;
      }), null;
    }, _ = function(P) {
      var T = o(), R = T.cssVar;
      return [function(L) {
        return y && R ? /* @__PURE__ */ x.createElement(x.Fragment, null, /* @__PURE__ */ x.createElement(b, {
          rootCls: P,
          cssVar: R,
          component: d
        }), L) : L;
      }, R == null ? void 0 : R.key];
    };
    return _;
  }
  function f(d, h, v) {
    var g = arguments.length > 3 && arguments[3] !== void 0 ? arguments[3] : {}, m = Array.isArray(d) ? d : [d, d], y = X(m, 1), S = y[0], w = m.join("-"), b = e.layer || {
      name: "antd"
    };
    return function(_) {
      var p = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : _, P = o(), T = P.theme, R = P.realToken, L = P.hashId, A = P.token, $ = P.cssVar, I = n(), j = I.rootPrefixCls, z = I.iconPrefixCls, H = r(), re = $ ? "css" : "js", J = fi(function() {
        var B = /* @__PURE__ */ new Set();
        return $ && Object.keys(g.unitless || {}).forEach(function(oe) {
          B.add(rt(oe, $.prefix)), B.add(rt(oe, ur(S, $.prefix)));
        }), ii(re, B);
      }, [re, S, $ == null ? void 0 : $.prefix]), be = ci(re), Se = be.max, V = be.min, ne = {
        theme: T,
        token: A,
        hashId: L,
        nonce: function() {
          return H.nonce;
        },
        clientOnly: g.clientOnly,
        layer: b,
        // antd is always at top of styles
        order: g.order || -999
      };
      typeof i == "function" && kt(C(C({}, ne), {}, {
        clientOnly: !1,
        path: ["Shared", j]
      }), function() {
        return i(A, {
          prefix: {
            rootPrefixCls: j,
            iconPrefixCls: z
          },
          csp: H
        });
      });
      var he = kt(C(C({}, ne), {}, {
        path: [w, _, z]
      }), function() {
        if (g.injectStyle === !1)
          return [];
        var B = ai(A), oe = B.token, xe = B.flush, Q = mr(S, R, v), Ze = ".".concat(_), Ce = fr(S, R, Q, {
          deprecatedTokens: g.deprecatedTokens
        });
        $ && Q && F(Q) === "object" && Object.keys(Q).forEach(function(we) {
          Q[we] = "var(".concat(rt(we, ur(S, $.prefix)), ")");
        });
        var Ee = At(oe, {
          componentCls: Ze,
          prefixCls: _,
          iconCls: ".".concat(z),
          antCls: ".".concat(j),
          calc: J,
          // @ts-ignore
          max: Se,
          // @ts-ignore
          min: V
        }, $ ? Q : Ce), _e = h(Ee, {
          hashId: L,
          prefixCls: _,
          rootPrefixCls: j,
          iconPrefixCls: z
        });
        xe(S, Ce);
        var ie = typeof s == "function" ? s(Ee, _, p, g.resetFont) : null;
        return [g.resetStyle === !1 ? null : ie, _e];
      });
      return [he, L];
    };
  }
  function u(d, h, v) {
    var g = arguments.length > 3 && arguments[3] !== void 0 ? arguments[3] : {}, m = f(d, h, v, C({
      resetStyle: !1,
      // Sub Style should default after root one
      order: -998
    }, g)), y = function(w) {
      var b = w.prefixCls, _ = w.rootCls, p = _ === void 0 ? b : _;
      return m(b, p), null;
    };
    return y;
  }
  return {
    genStyleHooks: c,
    genSubStyleComponent: u,
    genComponentStyleHook: f
  };
}
const D = Math.round;
function lt(e, t) {
  const r = e.replace(/^[^(]*\((.*)/, "$1").replace(/\).*/, "").match(/\d*\.?\d+%?/g) || [], o = r.map((n) => parseFloat(n));
  for (let n = 0; n < 3; n += 1)
    o[n] = t(o[n] || 0, r[n] || "", n);
  return r[3] ? o[3] = r[3].includes("%") ? o[3] / 100 : o[3] : o[3] = 1, o;
}
const pr = (e, t, r) => r === 0 ? e : e / 100;
function pe(e, t) {
  const r = t || 255;
  return e > r ? r : e < 0 ? 0 : e;
}
class Y {
  constructor(t) {
    E(this, "isValid", !0), E(this, "r", 0), E(this, "g", 0), E(this, "b", 0), E(this, "a", 1), E(this, "_h", void 0), E(this, "_s", void 0), E(this, "_l", void 0), E(this, "_v", void 0), E(this, "_max", void 0), E(this, "_min", void 0), E(this, "_brightness", void 0);
    function r(o) {
      return o[0] in t && o[1] in t && o[2] in t;
    }
    if (t) if (typeof t == "string") {
      let n = function(i) {
        return o.startsWith(i);
      };
      const o = t.trim();
      /^#?[A-F\d]{3,8}$/i.test(o) ? this.fromHexString(o) : n("rgb") ? this.fromRgbString(o) : n("hsl") ? this.fromHslString(o) : (n("hsv") || n("hsb")) && this.fromHsvString(o);
    } else if (t instanceof Y)
      this.r = t.r, this.g = t.g, this.b = t.b, this.a = t.a, this._h = t._h, this._s = t._s, this._l = t._l, this._v = t._v;
    else if (r("rgb"))
      this.r = pe(t.r), this.g = pe(t.g), this.b = pe(t.b), this.a = typeof t.a == "number" ? pe(t.a, 1) : 1;
    else if (r("hsl"))
      this.fromHsl(t);
    else if (r("hsv"))
      this.fromHsv(t);
    else
      throw new Error("@ant-design/fast-color: unsupported input " + JSON.stringify(t));
  }
  // ======================= Setter =======================
  setR(t) {
    return this._sc("r", t);
  }
  setG(t) {
    return this._sc("g", t);
  }
  setB(t) {
    return this._sc("b", t);
  }
  setA(t) {
    return this._sc("a", t, 1);
  }
  setHue(t) {
    const r = this.toHsv();
    return r.h = t, this._c(r);
  }
  // ======================= Getter =======================
  /**
   * Returns the perceived luminance of a color, from 0-1.
   * @see http://www.w3.org/TR/2008/REC-WCAG20-20081211/#relativeluminancedef
   */
  getLuminance() {
    function t(i) {
      const s = i / 255;
      return s <= 0.03928 ? s / 12.92 : Math.pow((s + 0.055) / 1.055, 2.4);
    }
    const r = t(this.r), o = t(this.g), n = t(this.b);
    return 0.2126 * r + 0.7152 * o + 0.0722 * n;
  }
  getHue() {
    if (typeof this._h > "u") {
      const t = this.getMax() - this.getMin();
      t === 0 ? this._h = 0 : this._h = D(60 * (this.r === this.getMax() ? (this.g - this.b) / t + (this.g < this.b ? 6 : 0) : this.g === this.getMax() ? (this.b - this.r) / t + 2 : (this.r - this.g) / t + 4));
    }
    return this._h;
  }
  getSaturation() {
    if (typeof this._s > "u") {
      const t = this.getMax() - this.getMin();
      t === 0 ? this._s = 0 : this._s = t / this.getMax();
    }
    return this._s;
  }
  getLightness() {
    return typeof this._l > "u" && (this._l = (this.getMax() + this.getMin()) / 510), this._l;
  }
  getValue() {
    return typeof this._v > "u" && (this._v = this.getMax() / 255), this._v;
  }
  /**
   * Returns the perceived brightness of the color, from 0-255.
   * Note: this is not the b of HSB
   * @see http://www.w3.org/TR/AERT#color-contrast
   */
  getBrightness() {
    return typeof this._brightness > "u" && (this._brightness = (this.r * 299 + this.g * 587 + this.b * 114) / 1e3), this._brightness;
  }
  // ======================== Func ========================
  darken(t = 10) {
    const r = this.getHue(), o = this.getSaturation();
    let n = this.getLightness() - t / 100;
    return n < 0 && (n = 0), this._c({
      h: r,
      s: o,
      l: n,
      a: this.a
    });
  }
  lighten(t = 10) {
    const r = this.getHue(), o = this.getSaturation();
    let n = this.getLightness() + t / 100;
    return n > 1 && (n = 1), this._c({
      h: r,
      s: o,
      l: n,
      a: this.a
    });
  }
  /**
   * Mix the current color a given amount with another color, from 0 to 100.
   * 0 means no mixing (return current color).
   */
  mix(t, r = 50) {
    const o = this._c(t), n = r / 100, i = (a) => (o[a] - this[a]) * n + this[a], s = {
      r: D(i("r")),
      g: D(i("g")),
      b: D(i("b")),
      a: D(i("a") * 100) / 100
    };
    return this._c(s);
  }
  /**
   * Mix the color with pure white, from 0 to 100.
   * Providing 0 will do nothing, providing 100 will always return white.
   */
  tint(t = 10) {
    return this.mix({
      r: 255,
      g: 255,
      b: 255,
      a: 1
    }, t);
  }
  /**
   * Mix the color with pure black, from 0 to 100.
   * Providing 0 will do nothing, providing 100 will always return black.
   */
  shade(t = 10) {
    return this.mix({
      r: 0,
      g: 0,
      b: 0,
      a: 1
    }, t);
  }
  onBackground(t) {
    const r = this._c(t), o = this.a + r.a * (1 - this.a), n = (i) => D((this[i] * this.a + r[i] * r.a * (1 - this.a)) / o);
    return this._c({
      r: n("r"),
      g: n("g"),
      b: n("b"),
      a: o
    });
  }
  // ======================= Status =======================
  isDark() {
    return this.getBrightness() < 128;
  }
  isLight() {
    return this.getBrightness() >= 128;
  }
  // ======================== MISC ========================
  equals(t) {
    return this.r === t.r && this.g === t.g && this.b === t.b && this.a === t.a;
  }
  clone() {
    return this._c(this);
  }
  // ======================= Format =======================
  toHexString() {
    let t = "#";
    const r = (this.r || 0).toString(16);
    t += r.length === 2 ? r : "0" + r;
    const o = (this.g || 0).toString(16);
    t += o.length === 2 ? o : "0" + o;
    const n = (this.b || 0).toString(16);
    if (t += n.length === 2 ? n : "0" + n, typeof this.a == "number" && this.a >= 0 && this.a < 1) {
      const i = D(this.a * 255).toString(16);
      t += i.length === 2 ? i : "0" + i;
    }
    return t;
  }
  /** CSS support color pattern */
  toHsl() {
    return {
      h: this.getHue(),
      s: this.getSaturation(),
      l: this.getLightness(),
      a: this.a
    };
  }
  /** CSS support color pattern */
  toHslString() {
    const t = this.getHue(), r = D(this.getSaturation() * 100), o = D(this.getLightness() * 100);
    return this.a !== 1 ? `hsla(${t},${r}%,${o}%,${this.a})` : `hsl(${t},${r}%,${o}%)`;
  }
  /** Same as toHsb */
  toHsv() {
    return {
      h: this.getHue(),
      s: this.getSaturation(),
      v: this.getValue(),
      a: this.a
    };
  }
  toRgb() {
    return {
      r: this.r,
      g: this.g,
      b: this.b,
      a: this.a
    };
  }
  toRgbString() {
    return this.a !== 1 ? `rgba(${this.r},${this.g},${this.b},${this.a})` : `rgb(${this.r},${this.g},${this.b})`;
  }
  toString() {
    return this.toRgbString();
  }
  // ====================== Privates ======================
  /** Return a new FastColor object with one channel changed */
  _sc(t, r, o) {
    const n = this.clone();
    return n[t] = pe(r, o), n;
  }
  _c(t) {
    return new this.constructor(t);
  }
  getMax() {
    return typeof this._max > "u" && (this._max = Math.max(this.r, this.g, this.b)), this._max;
  }
  getMin() {
    return typeof this._min > "u" && (this._min = Math.min(this.r, this.g, this.b)), this._min;
  }
  fromHexString(t) {
    const r = t.replace("#", "");
    function o(n, i) {
      return parseInt(r[n] + r[i || n], 16);
    }
    r.length < 6 ? (this.r = o(0), this.g = o(1), this.b = o(2), this.a = r[3] ? o(3) / 255 : 1) : (this.r = o(0, 1), this.g = o(2, 3), this.b = o(4, 5), this.a = r[6] ? o(6, 7) / 255 : 1);
  }
  fromHsl({
    h: t,
    s: r,
    l: o,
    a: n
  }) {
    if (this._h = t % 360, this._s = r, this._l = o, this.a = typeof n == "number" ? n : 1, r <= 0) {
      const d = D(o * 255);
      this.r = d, this.g = d, this.b = d;
    }
    let i = 0, s = 0, a = 0;
    const c = t / 60, l = (1 - Math.abs(2 * o - 1)) * r, f = l * (1 - Math.abs(c % 2 - 1));
    c >= 0 && c < 1 ? (i = l, s = f) : c >= 1 && c < 2 ? (i = f, s = l) : c >= 2 && c < 3 ? (s = l, a = f) : c >= 3 && c < 4 ? (s = f, a = l) : c >= 4 && c < 5 ? (i = f, a = l) : c >= 5 && c < 6 && (i = l, a = f);
    const u = o - l / 2;
    this.r = D((i + u) * 255), this.g = D((s + u) * 255), this.b = D((a + u) * 255);
  }
  fromHsv({
    h: t,
    s: r,
    v: o,
    a: n
  }) {
    this._h = t % 360, this._s = r, this._v = o, this.a = typeof n == "number" ? n : 1;
    const i = D(o * 255);
    if (this.r = i, this.g = i, this.b = i, r <= 0)
      return;
    const s = t / 60, a = Math.floor(s), c = s - a, l = D(o * (1 - r) * 255), f = D(o * (1 - r * c) * 255), u = D(o * (1 - r * (1 - c)) * 255);
    switch (a) {
      case 0:
        this.g = u, this.b = l;
        break;
      case 1:
        this.r = f, this.b = l;
        break;
      case 2:
        this.r = l, this.b = u;
        break;
      case 3:
        this.r = l, this.g = f;
        break;
      case 4:
        this.r = u, this.g = l;
        break;
      case 5:
      default:
        this.g = l, this.b = f;
        break;
    }
  }
  fromHsvString(t) {
    const r = lt(t, pr);
    this.fromHsv({
      h: r[0],
      s: r[1],
      v: r[2],
      a: r[3]
    });
  }
  fromHslString(t) {
    const r = lt(t, pr);
    this.fromHsl({
      h: r[0],
      s: r[1],
      l: r[2],
      a: r[3]
    });
  }
  fromRgbString(t) {
    const r = lt(t, (o, n) => (
      // Convert percentage to number. e.g. 50% -> 128
      n.includes("%") ? D(o / 100 * 255) : o
    ));
    this.r = r[0], this.g = r[1], this.b = r[2], this.a = r[3];
  }
}
const hi = {
  blue: "#1677FF",
  purple: "#722ED1",
  cyan: "#13C2C2",
  green: "#52C41A",
  magenta: "#EB2F96",
  /**
   * @deprecated Use magenta instead
   */
  pink: "#EB2F96",
  red: "#F5222D",
  orange: "#FA8C16",
  yellow: "#FADB14",
  volcano: "#FA541C",
  geekblue: "#2F54EB",
  gold: "#FAAD14",
  lime: "#A0D911"
}, pi = Object.assign(Object.assign({}, hi), {
  // Color
  colorPrimary: "#1677ff",
  colorSuccess: "#52c41a",
  colorWarning: "#faad14",
  colorError: "#ff4d4f",
  colorInfo: "#1677ff",
  colorLink: "",
  colorTextBase: "",
  colorBgBase: "",
  // Font
  fontFamily: `-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial,
'Noto Sans', sans-serif, 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol',
'Noto Color Emoji'`,
  fontFamilyCode: "'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, Courier, monospace",
  fontSize: 14,
  // Line
  lineWidth: 1,
  lineType: "solid",
  // Motion
  motionUnit: 0.1,
  motionBase: 0,
  motionEaseOutCirc: "cubic-bezier(0.08, 0.82, 0.17, 1)",
  motionEaseInOutCirc: "cubic-bezier(0.78, 0.14, 0.15, 0.86)",
  motionEaseOut: "cubic-bezier(0.215, 0.61, 0.355, 1)",
  motionEaseInOut: "cubic-bezier(0.645, 0.045, 0.355, 1)",
  motionEaseOutBack: "cubic-bezier(0.12, 0.4, 0.29, 1.46)",
  motionEaseInBack: "cubic-bezier(0.71, -0.46, 0.88, 0.6)",
  motionEaseInQuint: "cubic-bezier(0.755, 0.05, 0.855, 0.06)",
  motionEaseOutQuint: "cubic-bezier(0.23, 1, 0.32, 1)",
  // Radius
  borderRadius: 6,
  // Size
  sizeUnit: 4,
  sizeStep: 4,
  sizePopupArrow: 16,
  // Control Base
  controlHeight: 32,
  // zIndex
  zIndexBase: 0,
  zIndexPopupBase: 1e3,
  // Image
  opacityImage: 1,
  // Wireframe
  wireframe: !1,
  // Motion
  motion: !0
});
function ut(e) {
  return e >= 0 && e <= 255;
}
function Ae(e, t) {
  const {
    r,
    g: o,
    b: n,
    a: i
  } = new Y(e).toRgb();
  if (i < 1)
    return e;
  const {
    r: s,
    g: a,
    b: c
  } = new Y(t).toRgb();
  for (let l = 0.01; l <= 1; l += 0.01) {
    const f = Math.round((r - s * (1 - l)) / l), u = Math.round((o - a * (1 - l)) / l), d = Math.round((n - c * (1 - l)) / l);
    if (ut(f) && ut(u) && ut(d))
      return new Y({
        r: f,
        g: u,
        b: d,
        a: Math.round(l * 100) / 100
      }).toRgbString();
  }
  return new Y({
    r,
    g: o,
    b: n,
    a: 1
  }).toRgbString();
}
var gi = function(e, t) {
  var r = {};
  for (var o in e) Object.prototype.hasOwnProperty.call(e, o) && t.indexOf(o) < 0 && (r[o] = e[o]);
  if (e != null && typeof Object.getOwnPropertySymbols == "function") for (var n = 0, o = Object.getOwnPropertySymbols(e); n < o.length; n++)
    t.indexOf(o[n]) < 0 && Object.prototype.propertyIsEnumerable.call(e, o[n]) && (r[o[n]] = e[o[n]]);
  return r;
};
function vi(e) {
  const {
    override: t
  } = e, r = gi(e, ["override"]), o = Object.assign({}, t);
  Object.keys(pi).forEach((d) => {
    delete o[d];
  });
  const n = Object.assign(Object.assign({}, r), o), i = 480, s = 576, a = 768, c = 992, l = 1200, f = 1600;
  if (n.motion === !1) {
    const d = "0s";
    n.motionDurationFast = d, n.motionDurationMid = d, n.motionDurationSlow = d;
  }
  return Object.assign(Object.assign(Object.assign({}, n), {
    // ============== Background ============== //
    colorFillContent: n.colorFillSecondary,
    colorFillContentHover: n.colorFill,
    colorFillAlter: n.colorFillQuaternary,
    colorBgContainerDisabled: n.colorFillTertiary,
    // ============== Split ============== //
    colorBorderBg: n.colorBgContainer,
    colorSplit: Ae(n.colorBorderSecondary, n.colorBgContainer),
    // ============== Text ============== //
    colorTextPlaceholder: n.colorTextQuaternary,
    colorTextDisabled: n.colorTextQuaternary,
    colorTextHeading: n.colorText,
    colorTextLabel: n.colorTextSecondary,
    colorTextDescription: n.colorTextTertiary,
    colorTextLightSolid: n.colorWhite,
    colorHighlight: n.colorError,
    colorBgTextHover: n.colorFillSecondary,
    colorBgTextActive: n.colorFill,
    colorIcon: n.colorTextTertiary,
    colorIconHover: n.colorText,
    colorErrorOutline: Ae(n.colorErrorBg, n.colorBgContainer),
    colorWarningOutline: Ae(n.colorWarningBg, n.colorBgContainer),
    // Font
    fontSizeIcon: n.fontSizeSM,
    // Line
    lineWidthFocus: n.lineWidth * 3,
    // Control
    lineWidth: n.lineWidth,
    controlOutlineWidth: n.lineWidth * 2,
    // Checkbox size and expand icon size
    controlInteractiveSize: n.controlHeight / 2,
    controlItemBgHover: n.colorFillTertiary,
    controlItemBgActive: n.colorPrimaryBg,
    controlItemBgActiveHover: n.colorPrimaryBgHover,
    controlItemBgActiveDisabled: n.colorFill,
    controlTmpOutline: n.colorFillQuaternary,
    controlOutline: Ae(n.colorPrimaryBg, n.colorBgContainer),
    lineType: n.lineType,
    borderRadius: n.borderRadius,
    borderRadiusXS: n.borderRadiusXS,
    borderRadiusSM: n.borderRadiusSM,
    borderRadiusLG: n.borderRadiusLG,
    fontWeightStrong: 600,
    opacityLoading: 0.65,
    linkDecoration: "none",
    linkHoverDecoration: "none",
    linkFocusDecoration: "none",
    controlPaddingHorizontal: 12,
    controlPaddingHorizontalSM: 8,
    paddingXXS: n.sizeXXS,
    paddingXS: n.sizeXS,
    paddingSM: n.sizeSM,
    padding: n.size,
    paddingMD: n.sizeMD,
    paddingLG: n.sizeLG,
    paddingXL: n.sizeXL,
    paddingContentHorizontalLG: n.sizeLG,
    paddingContentVerticalLG: n.sizeMS,
    paddingContentHorizontal: n.sizeMS,
    paddingContentVertical: n.sizeSM,
    paddingContentHorizontalSM: n.size,
    paddingContentVerticalSM: n.sizeXS,
    marginXXS: n.sizeXXS,
    marginXS: n.sizeXS,
    marginSM: n.sizeSM,
    margin: n.size,
    marginMD: n.sizeMD,
    marginLG: n.sizeLG,
    marginXL: n.sizeXL,
    marginXXL: n.sizeXXL,
    boxShadow: `
      0 6px 16px 0 rgba(0, 0, 0, 0.08),
      0 3px 6px -4px rgba(0, 0, 0, 0.12),
      0 9px 28px 8px rgba(0, 0, 0, 0.05)
    `,
    boxShadowSecondary: `
      0 6px 16px 0 rgba(0, 0, 0, 0.08),
      0 3px 6px -4px rgba(0, 0, 0, 0.12),
      0 9px 28px 8px rgba(0, 0, 0, 0.05)
    `,
    boxShadowTertiary: `
      0 1px 2px 0 rgba(0, 0, 0, 0.03),
      0 1px 6px -1px rgba(0, 0, 0, 0.02),
      0 2px 4px 0 rgba(0, 0, 0, 0.02)
    `,
    screenXS: i,
    screenXSMin: i,
    screenXSMax: s - 1,
    screenSM: s,
    screenSMMin: s,
    screenSMMax: a - 1,
    screenMD: a,
    screenMDMin: a,
    screenMDMax: c - 1,
    screenLG: c,
    screenLGMin: c,
    screenLGMax: l - 1,
    screenXL: l,
    screenXLMin: l,
    screenXLMax: f - 1,
    screenXXL: f,
    screenXXLMin: f,
    boxShadowPopoverArrow: "2px 2px 5px rgba(0, 0, 0, 0.05)",
    boxShadowCard: `
      0 1px 2px -2px ${new Y("rgba(0, 0, 0, 0.16)").toRgbString()},
      0 3px 6px 0 ${new Y("rgba(0, 0, 0, 0.12)").toRgbString()},
      0 5px 12px 4px ${new Y("rgba(0, 0, 0, 0.09)").toRgbString()}
    `,
    boxShadowDrawerRight: `
      -6px 0 16px 0 rgba(0, 0, 0, 0.08),
      -3px 0 6px -4px rgba(0, 0, 0, 0.12),
      -9px 0 28px 8px rgba(0, 0, 0, 0.05)
    `,
    boxShadowDrawerLeft: `
      6px 0 16px 0 rgba(0, 0, 0, 0.08),
      3px 0 6px -4px rgba(0, 0, 0, 0.12),
      9px 0 28px 8px rgba(0, 0, 0, 0.05)
    `,
    boxShadowDrawerUp: `
      0 6px 16px 0 rgba(0, 0, 0, 0.08),
      0 3px 6px -4px rgba(0, 0, 0, 0.12),
      0 9px 28px 8px rgba(0, 0, 0, 0.05)
    `,
    boxShadowDrawerDown: `
      0 -6px 16px 0 rgba(0, 0, 0, 0.08),
      0 -3px 6px -4px rgba(0, 0, 0, 0.12),
      0 -9px 28px 8px rgba(0, 0, 0, 0.05)
    `,
    boxShadowTabsOverflowLeft: "inset 10px 0 8px -8px rgba(0, 0, 0, 0.08)",
    boxShadowTabsOverflowRight: "inset -10px 0 8px -8px rgba(0, 0, 0, 0.08)",
    boxShadowTabsOverflowTop: "inset 0 10px 8px -8px rgba(0, 0, 0, 0.08)",
    boxShadowTabsOverflowBottom: "inset 0 -10px 8px -8px rgba(0, 0, 0, 0.08)"
  }), o);
}
const yi = {
  lineHeight: !0,
  lineHeightSM: !0,
  lineHeightLG: !0,
  lineHeightHeading1: !0,
  lineHeightHeading2: !0,
  lineHeightHeading3: !0,
  lineHeightHeading4: !0,
  lineHeightHeading5: !0,
  opacityLoading: !0,
  fontWeightStrong: !0,
  zIndexPopupBase: !0,
  zIndexBase: !0,
  opacityImage: !0
}, bi = {
  size: !0,
  sizeSM: !0,
  sizeLG: !0,
  sizeMD: !0,
  sizeXS: !0,
  sizeXXS: !0,
  sizeMS: !0,
  sizeXL: !0,
  sizeXXL: !0,
  sizeUnit: !0,
  sizeStep: !0,
  motionBase: !0,
  motionUnit: !0
}, Si = mn(vt.defaultAlgorithm), xi = {
  screenXS: !0,
  screenXSMin: !0,
  screenXSMax: !0,
  screenSM: !0,
  screenSMMin: !0,
  screenSMMax: !0,
  screenMD: !0,
  screenMDMin: !0,
  screenMDMax: !0,
  screenLG: !0,
  screenLGMin: !0,
  screenLGMax: !0,
  screenXL: !0,
  screenXLMin: !0,
  screenXLMax: !0,
  screenXXL: !0,
  screenXXLMin: !0
}, Ur = (e, t, r) => {
  const o = r.getDerivativeToken(e), {
    override: n,
    ...i
  } = t;
  let s = {
    ...o,
    override: n
  };
  return s = vi(s), i && Object.entries(i).forEach(([a, c]) => {
    const {
      theme: l,
      ...f
    } = c;
    let u = f;
    l && (u = Ur({
      ...s,
      ...f
    }, {
      override: f
    }, l)), s[a] = u;
  }), s;
};
function Ci() {
  const {
    token: e,
    hashed: t,
    theme: r = Si,
    override: o,
    cssVar: n
  } = x.useContext(vt._internalContext), [i, s, a] = hn(r, [vt.defaultSeed, e], {
    salt: `${to}-${t || ""}`,
    override: o,
    getComputedToken: Ur,
    cssVar: n && {
      prefix: n.prefix,
      key: n.key,
      unitless: yi,
      ignore: bi,
      preserve: xi
    }
  });
  return [r, a, t ? s : "", i, n];
}
const {
  genStyleHooks: Ei
} = mi({
  usePrefix: () => {
    const {
      getPrefixCls: e,
      iconPrefixCls: t
    } = bt();
    return {
      iconPrefixCls: t,
      rootPrefixCls: e()
    };
  },
  useToken: () => {
    const [e, t, r, o, n] = Ci();
    return {
      theme: e,
      realToken: t,
      hashId: r,
      token: o,
      cssVar: n
    };
  },
  useCSP: () => {
    const {
      csp: e
    } = bt();
    return e ?? {};
  },
  layer: {
    name: "antdx",
    dependencies: ["antd"]
  }
});
var _i = `accept acceptCharset accessKey action allowFullScreen allowTransparency
    alt async autoComplete autoFocus autoPlay capture cellPadding cellSpacing challenge
    charSet checked classID className colSpan cols content contentEditable contextMenu
    controls coords crossOrigin data dateTime default defer dir disabled download draggable
    encType form formAction formEncType formMethod formNoValidate formTarget frameBorder
    headers height hidden high href hrefLang htmlFor httpEquiv icon id inputMode integrity
    is keyParams keyType kind label lang list loop low manifest marginHeight marginWidth max maxLength media
    mediaGroup method min minLength multiple muted name noValidate nonce open
    optimum pattern placeholder poster preload radioGroup readOnly rel required
    reversed role rowSpan rows sandbox scope scoped scrolling seamless selected
    shape size sizes span spellCheck src srcDoc srcLang srcSet start step style
    summary tabIndex target title type useMap value width wmode wrap`, wi = `onCopy onCut onPaste onCompositionEnd onCompositionStart onCompositionUpdate onKeyDown
    onKeyPress onKeyUp onFocus onBlur onChange onInput onSubmit onClick onContextMenu onDoubleClick
    onDrag onDragEnd onDragEnter onDragExit onDragLeave onDragOver onDragStart onDrop onMouseDown
    onMouseEnter onMouseLeave onMouseMove onMouseOut onMouseOver onMouseUp onSelect onTouchCancel
    onTouchEnd onTouchMove onTouchStart onScroll onWheel onAbort onCanPlay onCanPlayThrough
    onDurationChange onEmptied onEncrypted onEnded onError onLoadedData onLoadedMetadata
    onLoadStart onPause onPlay onPlaying onProgress onRateChange onSeeked onSeeking onStalled onSuspend onTimeUpdate onVolumeChange onWaiting onLoad onError`, Ti = "".concat(_i, " ").concat(wi).split(/[\s\n]+/), Pi = "aria-", Mi = "data-";
function gr(e, t) {
  return e.indexOf(t) === 0;
}
function Wr(e) {
  var t = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : !1, r;
  t === !1 ? r = {
    aria: !0,
    data: !0,
    attr: !0
  } : t === !0 ? r = {
    aria: !0
  } : r = To({}, t);
  var o = {};
  return Object.keys(e).forEach(function(n) {
    // Aria
    (r.aria && (n === "role" || gr(n, Pi)) || // Data
    r.data && gr(n, Mi) || // Attr
    r.attr && Ti.includes(n)) && (o[n] = e[n]);
  }), o;
}
const ft = () => ({
  height: 0,
  opacity: 0
}), vr = (e) => {
  const {
    scrollHeight: t
  } = e;
  return {
    height: t,
    opacity: 1
  };
}, Oi = (e) => ({
  height: e ? e.offsetHeight : 0
}), dt = (e, t) => (t == null ? void 0 : t.deadline) === !0 || t.propertyName === "height", Ri = (e = io) => ({
  motionName: `${e}-motion-collapse`,
  onAppearStart: ft,
  onEnterStart: ft,
  onAppearActive: vr,
  onEnterActive: vr,
  onLeaveStart: Oi,
  onLeaveActive: ft,
  onAppearEnd: dt,
  onEnterEnd: dt,
  onLeaveEnd: dt,
  motionDeadline: 500
}), Li = (e, t, r) => {
  const o = typeof e == "boolean" || (e == null ? void 0 : e.expandedKeys) === void 0, [n, i, s] = x.useMemo(() => {
    let u = {
      expandedKeys: [],
      onExpand: () => {
      }
    };
    return e ? (typeof e == "object" && (u = {
      ...u,
      ...e
    }), [!0, u.expandedKeys, u.onExpand]) : [!1, u.expandedKeys, u.onExpand];
  }, [e]), [a, c] = fo(i, {
    value: o ? void 0 : i,
    onChange: s
  }), l = (u) => {
    c((d) => {
      const h = o ? d : i, v = h.includes(u) ? h.filter((g) => g !== u) : [...h, u];
      return s == null || s(v), v;
    });
  }, f = x.useMemo(() => n ? {
    ...Ri(r),
    motionAppear: !1,
    leavedClassName: `${t}-content-hidden`
  } : {}, [r, t, n]);
  return [n, a, n ? l : void 0, f];
}, Ai = (e) => ({
  [e.componentCls]: {
    // For common/openAnimation
    [`${e.antCls}-motion-collapse-legacy`]: {
      overflow: "hidden",
      "&-active": {
        transition: `height ${e.motionDurationMid} ${e.motionEaseInOut},
        opacity ${e.motionDurationMid} ${e.motionEaseInOut} !important`
      }
    },
    [`${e.antCls}-motion-collapse`]: {
      overflow: "hidden",
      transition: `height ${e.motionDurationMid} ${e.motionEaseInOut},
        opacity ${e.motionDurationMid} ${e.motionEaseInOut} !important`
    }
  }
});
let mt = /* @__PURE__ */ function(e) {
  return e.PENDING = "pending", e.SUCCESS = "success", e.ERROR = "error", e;
}({});
const Kr = /* @__PURE__ */ x.createContext(null), $i = (e) => {
  const {
    info: t = {},
    nextStatus: r,
    onClick: o,
    ...n
  } = e, i = Wr(n, {
    attr: !0,
    aria: !0,
    data: !0
  }), {
    prefixCls: s,
    collapseMotion: a,
    enableCollapse: c,
    expandedKeys: l,
    direction: f,
    classNames: u = {},
    styles: d = {}
  } = x.useContext(Kr), h = x.useId(), {
    key: v = h,
    icon: g,
    title: m,
    extra: y,
    content: S,
    footer: w,
    status: b,
    description: _
  } = t, p = `${s}-item`, P = () => o == null ? void 0 : o(v), T = l == null ? void 0 : l.includes(v);
  return /* @__PURE__ */ x.createElement("div", fe({}, i, {
    className: G(p, {
      [`${p}-${b}${r ? `-${r}` : ""}`]: b
    }, e.className),
    style: e.style
  }), /* @__PURE__ */ x.createElement("div", {
    className: G(`${p}-header`, u.itemHeader),
    style: d.itemHeader,
    onClick: P
  }, /* @__PURE__ */ x.createElement(fn, {
    icon: g,
    className: `${p}-icon`
  }), /* @__PURE__ */ x.createElement("div", {
    className: G(`${p}-header-box`, {
      [`${p}-collapsible`]: c && S
    })
  }, /* @__PURE__ */ x.createElement(Dt.Text, {
    strong: !0,
    ellipsis: {
      tooltip: {
        placement: f === "rtl" ? "topRight" : "topLeft",
        title: m
      }
    },
    className: `${p}-title`
  }, c && S && (f === "rtl" ? /* @__PURE__ */ x.createElement(pn, {
    className: `${p}-collapse-icon`,
    rotate: T ? -90 : 0
  }) : /* @__PURE__ */ x.createElement(gn, {
    className: `${p}-collapse-icon`,
    rotate: T ? 90 : 0
  })), m), _ && /* @__PURE__ */ x.createElement(Dt.Text, {
    className: `${p}-desc`,
    ellipsis: {
      tooltip: {
        placement: f === "rtl" ? "topRight" : "topLeft",
        title: _
      }
    },
    type: "secondary"
  }, _)), y && /* @__PURE__ */ x.createElement("div", {
    className: `${p}-extra`
  }, y)), S && /* @__PURE__ */ x.createElement(Vr, fe({}, a, {
    visible: c ? T : !0
  }), ({
    className: R,
    style: L
  }, A) => /* @__PURE__ */ x.createElement("div", {
    className: G(`${p}-content`, R),
    ref: A,
    style: L
  }, /* @__PURE__ */ x.createElement("div", {
    className: G(`${p}-content-box`, u.itemContent),
    style: d.itemContent
  }, S))), w && /* @__PURE__ */ x.createElement("div", {
    className: G(`${p}-footer`, u.itemFooter),
    style: d.itemFooter
  }, w));
}, Ii = (e) => {
  const {
    componentCls: t
  } = e, r = `${t}-item`, o = {
    [mt.PENDING]: e.colorPrimaryText,
    [mt.SUCCESS]: e.colorSuccessText,
    [mt.ERROR]: e.colorErrorText
  }, n = Object.keys(o);
  return n.reduce((i, s) => {
    const a = o[s];
    return n.forEach((c) => {
      const l = `& ${r}-${s}-${c}`, f = s === c ? {} : {
        backgroundColor: "none !important",
        backgroundImage: `linear-gradient(${a}, ${o[c]})`
      };
      i[l] = {
        [`& ${r}-icon, & > *::before`]: {
          backgroundColor: `${a} !important`
        },
        "& > :last-child::before": f
      };
    }), i;
  }, {});
}, ji = (e) => {
  const {
    calc: t,
    componentCls: r
  } = e, o = `${r}-item`, n = {
    content: '""',
    width: t(e.lineWidth).mul(2).equal(),
    display: "block",
    position: "absolute",
    insetInlineEnd: "none",
    backgroundColor: e.colorTextPlaceholder
  };
  return {
    "& > :last-child > :last-child": {
      "&::before": {
        display: "none !important"
      },
      [`&${o}-footer`]: {
        "&::before": {
          display: "block !important",
          bottom: 0
        }
      }
    },
    [`& > ${o}`]: {
      [`& ${o}-header, & ${o}-content, & ${o}-footer`]: {
        position: "relative",
        "&::before": {
          bottom: t(e.itemGap).mul(-1).equal()
        }
      },
      [`& ${o}-header, & ${o}-content`]: {
        marginInlineStart: t(e.itemSize).mul(-1).equal(),
        "&::before": {
          ...n,
          insetInlineStart: t(e.itemSize).div(2).sub(e.lineWidth).equal()
        }
      },
      [`& ${o}-header::before`]: {
        top: e.itemSize,
        bottom: t(e.itemGap).mul(-2).equal()
      },
      [`& ${o}-content::before`]: {
        top: "100%"
      },
      [`& ${o}-footer::before`]: {
        ...n,
        top: 0,
        insetInlineStart: t(e.itemSize).div(-2).sub(e.lineWidth).equal()
      }
    }
  };
}, zi = (e) => {
  const {
    componentCls: t
  } = e, r = `${t}-item`;
  return {
    [r]: {
      display: "flex",
      flexDirection: "column",
      [`& ${r}-collapsible`]: {
        cursor: "pointer"
      },
      [`& ${r}-header`]: {
        display: "flex",
        marginBottom: e.itemGap,
        gap: e.itemGap,
        alignItems: "flex-start",
        [`& ${r}-icon`]: {
          height: e.itemSize,
          width: e.itemSize,
          fontSize: e.itemFontSize
        },
        [`& ${r}-extra`]: {
          height: e.itemSize,
          maxHeight: e.itemSize
        },
        [`& ${r}-header-box`]: {
          flex: 1,
          display: "flex",
          flexDirection: "column",
          overflow: "hidden",
          [`& ${r}-title`]: {
            height: e.itemSize,
            lineHeight: `${ze(e.itemSize)}`,
            maxHeight: e.itemSize,
            fontSize: e.itemFontSize,
            [`& ${r}-collapse-icon`]: {
              marginInlineEnd: e.marginXS
            }
          },
          [`& ${r}-desc`]: {
            fontSize: e.itemFontSize
          }
        }
      },
      [`& ${r}-content`]: {
        [`& ${r}-content-hidden`]: {
          display: "none"
        },
        [`& ${r}-content-box`]: {
          padding: e.itemGap,
          display: "inline-block",
          maxWidth: `calc(100% - ${e.itemSize})`,
          borderRadius: e.borderRadiusLG,
          backgroundColor: e.colorBgContainer,
          border: `${ze(e.lineWidth)} ${e.lineType} ${e.colorBorderSecondary}`
        }
      },
      [`& ${r}-footer`]: {
        marginTop: e.itemGap,
        display: "inline-flex"
      }
    }
  };
}, ht = (e, t = "middle") => {
  const {
    componentCls: r
  } = e, o = {
    large: {
      itemSize: e.itemSizeLG,
      itemGap: e.itemGapLG,
      itemFontSize: e.itemFontSizeLG
    },
    middle: {
      itemSize: e.itemSize,
      itemGap: e.itemGap,
      itemFontSize: e.itemFontSize
    },
    small: {
      itemSize: e.itemSizeSM,
      itemGap: e.itemGapSM,
      itemFontSize: e.itemFontSizeSM
    }
  }[t];
  return {
    [`&${r}-${t}`]: {
      paddingInlineStart: o.itemSize,
      gap: o.itemGap,
      ...zi({
        ...e,
        ...o
      }),
      ...ji({
        ...e,
        ...o
      })
    }
  };
}, Di = (e) => {
  const {
    componentCls: t
  } = e;
  return {
    [t]: {
      display: "flex",
      flexDirection: "column",
      ...Ii(e),
      ...ht(e),
      ...ht(e, "large"),
      ...ht(e, "small"),
      [`&${t}-rtl`]: {
        direction: "rtl"
      }
    }
  };
}, ki = Ei("ThoughtChain", (e) => {
  const t = At(e, {
    // small size tokens
    itemFontSizeSM: e.fontSizeSM,
    itemSizeSM: e.calc(e.controlHeightXS).add(e.controlHeightSM).div(2).equal(),
    itemGapSM: e.marginSM,
    // default size tokens
    itemFontSize: e.fontSize,
    itemSize: e.calc(e.controlHeightSM).add(e.controlHeight).div(2).equal(),
    itemGap: e.margin,
    // large size tokens
    itemFontSizeLG: e.fontSizeLG,
    itemSizeLG: e.calc(e.controlHeight).add(e.controlHeightLG).div(2).equal(),
    itemGapLG: e.marginLG
  });
  return [Di(t), Ai(t)];
}), Ni = (e) => {
  const {
    prefixCls: t,
    rootClassName: r,
    className: o,
    items: n,
    collapsible: i,
    styles: s = {},
    style: a,
    classNames: c = {},
    size: l = "middle",
    ...f
  } = e, u = Wr(f, {
    attr: !0,
    aria: !0,
    data: !0
  }), {
    getPrefixCls: d,
    direction: h
  } = bt(), v = d(), g = d("thought-chain", t), m = oo("thoughtChain"), [y, S, w, b] = Li(i, g, v), [_, p, P] = ki(g), T = G(o, r, g, m.className, p, P, {
    [`${g}-rtl`]: h === "rtl"
  }, `${g}-${l}`);
  return _(/* @__PURE__ */ x.createElement("div", fe({}, u, {
    className: T,
    style: {
      ...m.style,
      ...a
    }
  }), /* @__PURE__ */ x.createElement(Kr.Provider, {
    value: {
      prefixCls: g,
      enableCollapse: y,
      collapseMotion: b,
      expandedKeys: S,
      direction: h,
      classNames: {
        itemHeader: G(m.classNames.itemHeader, c.itemHeader),
        itemContent: G(m.classNames.itemContent, c.itemContent),
        itemFooter: G(m.classNames.itemFooter, c.itemFooter)
      },
      styles: {
        itemHeader: {
          ...m.styles.itemHeader,
          ...s.itemHeader
        },
        itemContent: {
          ...m.styles.itemContent,
          ...s.itemContent
        },
        itemFooter: {
          ...m.styles.itemFooter,
          ...s.itemFooter
        }
      }
    }
  }, n == null ? void 0 : n.map((R, L) => {
    var A;
    return /* @__PURE__ */ x.createElement($i, {
      key: R.key || `key_${L}`,
      className: G(m.classNames.item, c.item),
      style: {
        ...m.styles.item,
        ...s.item
      },
      info: {
        ...R,
        icon: R.icon || L + 1
      },
      onClick: w,
      nextStatus: ((A = n[L + 1]) == null ? void 0 : A.status) || R.status
    });
  }))));
}, Fi = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Hi(e) {
  return e ? Object.keys(e).reduce((t, r) => {
    const o = e[r];
    return t[r] = Vi(r, o), t;
  }, {}) : {};
}
function Vi(e, t) {
  return typeof t == "number" && !Fi.includes(e) ? t + "px" : t;
}
function Pt(e) {
  const t = [], r = e.cloneNode(!1);
  if (e._reactElement) {
    const n = x.Children.toArray(e._reactElement.props.children).map((i) => {
      if (x.isValidElement(i) && i.props.__slot__) {
        const {
          portals: s,
          clonedElement: a
        } = Pt(i.props.el);
        return x.cloneElement(i, {
          ...i.props,
          el: a,
          children: [...x.Children.toArray(i.props.children), ...s]
        });
      }
      return null;
    });
    return n.originalChildren = e._reactElement.props.children, t.push(pt(x.cloneElement(e._reactElement, {
      ...e._reactElement.props,
      children: n
    }), r)), {
      clonedElement: r,
      portals: t
    };
  }
  Object.keys(e.getEventListeners()).forEach((n) => {
    e.getEventListeners(n).forEach(({
      listener: s,
      type: a,
      useCapture: c
    }) => {
      r.addEventListener(a, s, c);
    });
  });
  const o = Array.from(e.childNodes);
  for (let n = 0; n < o.length; n++) {
    const i = o[n];
    if (i.nodeType === 1) {
      const {
        clonedElement: s,
        portals: a
      } = Pt(i);
      t.push(...a), r.appendChild(s);
    } else i.nodeType === 3 && r.appendChild(i.cloneNode());
  }
  return {
    clonedElement: r,
    portals: t
  };
}
function Bi(e, t) {
  e && (typeof e == "function" ? e(t) : e.current = t);
}
const yr = tn(({
  slot: e,
  clone: t,
  className: r,
  style: o,
  observeAttributes: n
}, i) => {
  const s = ee(), [a, c] = rn([]), {
    forceClone: l
  } = cn(), f = l ? !0 : t;
  return ge(() => {
    var g;
    if (!s.current || !e)
      return;
    let u = e;
    function d() {
      let m = u;
      if (u.tagName.toLowerCase() === "svelte-slot" && u.children.length === 1 && u.children[0] && (m = u.children[0], m.tagName.toLowerCase() === "react-portal-target" && m.children[0] && (m = m.children[0])), Bi(i, m), r && m.classList.add(...r.split(" ")), o) {
        const y = Hi(o);
        Object.keys(y).forEach((S) => {
          m.style[S] = y[S];
        });
      }
    }
    let h = null, v = null;
    if (f && window.MutationObserver) {
      let m = function() {
        var b, _, p;
        (b = s.current) != null && b.contains(u) && ((_ = s.current) == null || _.removeChild(u));
        const {
          portals: S,
          clonedElement: w
        } = Pt(e);
        u = w, c(S), u.style.display = "contents", v && clearTimeout(v), v = setTimeout(() => {
          d();
        }, 50), (p = s.current) == null || p.appendChild(u);
      };
      m();
      const y = Mn(() => {
        m(), h == null || h.disconnect(), h == null || h.observe(e, {
          childList: !0,
          subtree: !0,
          attributes: n
        });
      }, 50);
      h = new window.MutationObserver(y), h.observe(e, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      u.style.display = "contents", d(), (g = s.current) == null || g.appendChild(u);
    return () => {
      var m, y;
      u.style.display = "", (m = s.current) != null && m.contains(u) && ((y = s.current) == null || y.removeChild(u)), h == null || h.disconnect();
    };
  }, [e, f, r, o, i, n, l]), x.createElement("react-child", {
    ref: s,
    style: {
      display: "contents"
    }
  }, ...a);
}), Gi = ({
  children: e,
  ...t
}) => /* @__PURE__ */ q.jsx(q.Fragment, {
  children: e(t)
});
function Xi(e) {
  return x.createElement(Gi, {
    children: e
  });
}
function qr(e, t, r) {
  const o = e.filter(Boolean);
  if (o.length !== 0)
    return o.map((n, i) => {
      var l;
      if (typeof n != "object")
        return t != null && t.fallback ? t.fallback(n) : n;
      const s = {
        ...n.props,
        key: ((l = n.props) == null ? void 0 : l.key) ?? (r ? `${r}-${i}` : `${i}`)
      };
      let a = s;
      Object.keys(n.slots).forEach((f) => {
        if (!n.slots[f] || !(n.slots[f] instanceof Element) && !n.slots[f].el)
          return;
        const u = f.split(".");
        u.forEach((y, S) => {
          a[y] || (a[y] = {}), S !== u.length - 1 && (a = s[y]);
        });
        const d = n.slots[f];
        let h, v, g = (t == null ? void 0 : t.clone) ?? !1, m = t == null ? void 0 : t.forceClone;
        d instanceof Element ? h = d : (h = d.el, v = d.callback, g = d.clone ?? g, m = d.forceClone ?? m), m = m ?? !!v, a[u[u.length - 1]] = h ? v ? (...y) => (v(u[u.length - 1], y), /* @__PURE__ */ q.jsx(zt, {
          ...n.ctx,
          params: y,
          forceClone: m,
          children: /* @__PURE__ */ q.jsx(yr, {
            slot: h,
            clone: g
          })
        })) : Xi((y) => /* @__PURE__ */ q.jsx(zt, {
          ...n.ctx,
          forceClone: m,
          children: /* @__PURE__ */ q.jsx(yr, {
            ...y,
            slot: h,
            clone: g
          })
        })) : a[u[u.length - 1]], a = s;
      });
      const c = (t == null ? void 0 : t.children) || "children";
      return n[c] ? s[c] = qr(n[c], t, `${i}`) : t != null && t.children && (s[c] = void 0, Reflect.deleteProperty(s, c)), s;
    });
}
const {
  useItems: Ui,
  withItemsContextProvider: Wi,
  ItemHandler: Qi
} = ln("antdx-thought-chain-items"), Yi = eo(Wi(["default", "items"], ({
  children: e,
  items: t,
  ...r
}) => {
  const {
    items: o
  } = Ui(), n = o.items.length > 0 ? o.items : o.default;
  return /* @__PURE__ */ q.jsxs(q.Fragment, {
    children: [/* @__PURE__ */ q.jsx("div", {
      style: {
        display: "none"
      },
      children: e
    }), /* @__PURE__ */ q.jsx(Ni, {
      ...r,
      items: nn(() => t || qr(n, {
        clone: !0
      }), [t, n])
    })]
  });
}));
export {
  Yi as ThoughtChain,
  Yi as default
};
