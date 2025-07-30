import { i as Yt, a as Q, r as Qt, w as ue, g as Jt, c as q, b as Ne } from "./Index-t0HLZeBw.js";
const w = window.ms_globals.React, p = window.ms_globals.React, Wt = window.ms_globals.React.version, Ut = window.ms_globals.React.forwardRef, wt = window.ms_globals.React.useRef, Gt = window.ms_globals.React.useState, Kt = window.ms_globals.React.useEffect, qt = window.ms_globals.React.useCallback, ge = window.ms_globals.React.useMemo, Be = window.ms_globals.ReactDOM.createPortal, Zt = window.ms_globals.internalContext.useContextPropsContext, Je = window.ms_globals.internalContext.ContextPropsProvider, _t = window.ms_globals.createItemsContext.createItemsContext, er = window.ms_globals.antd.ConfigProvider, He = window.ms_globals.antd.theme, tr = window.ms_globals.antd.Avatar, oe = window.ms_globals.antdCssinjs.unit, Re = window.ms_globals.antdCssinjs.token2CSSVar, Ze = window.ms_globals.antdCssinjs.useStyleRegister, rr = window.ms_globals.antdCssinjs.useCSSVarRegister, nr = window.ms_globals.antdCssinjs.createTheme, or = window.ms_globals.antdCssinjs.useCacheToken, Tt = window.ms_globals.antdCssinjs.Keyframes;
var sr = /\s/;
function ir(e) {
  for (var t = e.length; t-- && sr.test(e.charAt(t)); )
    ;
  return t;
}
var ar = /^\s+/;
function lr(e) {
  return e && e.slice(0, ir(e) + 1).replace(ar, "");
}
var et = NaN, cr = /^[-+]0x[0-9a-f]+$/i, ur = /^0b[01]+$/i, fr = /^0o[0-7]+$/i, dr = parseInt;
function tt(e) {
  if (typeof e == "number")
    return e;
  if (Yt(e))
    return et;
  if (Q(e)) {
    var t = typeof e.valueOf == "function" ? e.valueOf() : e;
    e = Q(t) ? t + "" : t;
  }
  if (typeof e != "string")
    return e === 0 ? e : +e;
  e = lr(e);
  var n = ur.test(e);
  return n || fr.test(e) ? dr(e.slice(2), n ? 2 : 8) : cr.test(e) ? et : +e;
}
var je = function() {
  return Qt.Date.now();
}, hr = "Expected a function", gr = Math.max, mr = Math.min;
function pr(e, t, n) {
  var o, r, s, i, a, l, f = 0, c = !1, u = !1, d = !0;
  if (typeof e != "function")
    throw new TypeError(hr);
  t = tt(t) || 0, Q(n) && (c = !!n.leading, u = "maxWait" in n, s = u ? gr(tt(n.maxWait) || 0, t) : s, d = "trailing" in n ? !!n.trailing : d);
  function g(v) {
    var O = o, P = r;
    return o = r = void 0, f = v, i = e.apply(P, O), i;
  }
  function b(v) {
    return f = v, a = setTimeout(y, t), c ? g(v) : i;
  }
  function S(v) {
    var O = v - l, P = v - f, R = t - O;
    return u ? mr(R, s - P) : R;
  }
  function m(v) {
    var O = v - l, P = v - f;
    return l === void 0 || O >= t || O < 0 || u && P >= s;
  }
  function y() {
    var v = je();
    if (m(v))
      return C(v);
    a = setTimeout(y, S(v));
  }
  function C(v) {
    return a = void 0, d && o ? g(v) : (o = r = void 0, i);
  }
  function I() {
    a !== void 0 && clearTimeout(a), f = 0, o = l = r = a = void 0;
  }
  function h() {
    return a === void 0 ? i : C(je());
  }
  function E() {
    var v = je(), O = m(v);
    if (o = arguments, r = this, l = v, O) {
      if (a === void 0)
        return b(l);
      if (u)
        return clearTimeout(a), a = setTimeout(y, t), g(l);
    }
    return a === void 0 && (a = setTimeout(y, t)), i;
  }
  return E.cancel = I, E.flush = h, E;
}
var Et = {
  exports: {}
}, be = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var br = p, yr = Symbol.for("react.element"), vr = Symbol.for("react.fragment"), Sr = Object.prototype.hasOwnProperty, xr = br.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, Cr = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function Ot(e, t, n) {
  var o, r = {}, s = null, i = null;
  n !== void 0 && (s = "" + n), t.key !== void 0 && (s = "" + t.key), t.ref !== void 0 && (i = t.ref);
  for (o in t) Sr.call(t, o) && !Cr.hasOwnProperty(o) && (r[o] = t[o]);
  if (e && e.defaultProps) for (o in t = e.defaultProps, t) r[o] === void 0 && (r[o] = t[o]);
  return {
    $$typeof: yr,
    type: e,
    key: s,
    ref: i,
    props: r,
    _owner: xr.current
  };
}
be.Fragment = vr;
be.jsx = Ot;
be.jsxs = Ot;
Et.exports = be;
var A = Et.exports;
const {
  SvelteComponent: wr,
  assign: rt,
  binding_callbacks: nt,
  check_outros: _r,
  children: Pt,
  claim_element: Mt,
  claim_space: Tr,
  component_subscribe: ot,
  compute_slots: Er,
  create_slot: Or,
  detach: Y,
  element: It,
  empty: st,
  exclude_internal_props: it,
  get_all_dirty_from_scope: Pr,
  get_slot_changes: Mr,
  group_outros: Ir,
  init: Rr,
  insert_hydration: fe,
  safe_not_equal: jr,
  set_custom_element_data: Rt,
  space: kr,
  transition_in: de,
  transition_out: ze,
  update_slot_base: Lr
} = window.__gradio__svelte__internal, {
  beforeUpdate: $r,
  getContext: Dr,
  onDestroy: Br,
  setContext: Hr
} = window.__gradio__svelte__internal;
function at(e) {
  let t, n;
  const o = (
    /*#slots*/
    e[7].default
  ), r = Or(
    o,
    e,
    /*$$scope*/
    e[6],
    null
  );
  return {
    c() {
      t = It("svelte-slot"), r && r.c(), this.h();
    },
    l(s) {
      t = Mt(s, "SVELTE-SLOT", {
        class: !0
      });
      var i = Pt(t);
      r && r.l(i), i.forEach(Y), this.h();
    },
    h() {
      Rt(t, "class", "svelte-1rt0kpf");
    },
    m(s, i) {
      fe(s, t, i), r && r.m(t, null), e[9](t), n = !0;
    },
    p(s, i) {
      r && r.p && (!n || i & /*$$scope*/
      64) && Lr(
        r,
        o,
        s,
        /*$$scope*/
        s[6],
        n ? Mr(
          o,
          /*$$scope*/
          s[6],
          i,
          null
        ) : Pr(
          /*$$scope*/
          s[6]
        ),
        null
      );
    },
    i(s) {
      n || (de(r, s), n = !0);
    },
    o(s) {
      ze(r, s), n = !1;
    },
    d(s) {
      s && Y(t), r && r.d(s), e[9](null);
    }
  };
}
function zr(e) {
  let t, n, o, r, s = (
    /*$$slots*/
    e[4].default && at(e)
  );
  return {
    c() {
      t = It("react-portal-target"), n = kr(), s && s.c(), o = st(), this.h();
    },
    l(i) {
      t = Mt(i, "REACT-PORTAL-TARGET", {
        class: !0
      }), Pt(t).forEach(Y), n = Tr(i), s && s.l(i), o = st(), this.h();
    },
    h() {
      Rt(t, "class", "svelte-1rt0kpf");
    },
    m(i, a) {
      fe(i, t, a), e[8](t), fe(i, n, a), s && s.m(i, a), fe(i, o, a), r = !0;
    },
    p(i, [a]) {
      /*$$slots*/
      i[4].default ? s ? (s.p(i, a), a & /*$$slots*/
      16 && de(s, 1)) : (s = at(i), s.c(), de(s, 1), s.m(o.parentNode, o)) : s && (Ir(), ze(s, 1, 1, () => {
        s = null;
      }), _r());
    },
    i(i) {
      r || (de(s), r = !0);
    },
    o(i) {
      ze(s), r = !1;
    },
    d(i) {
      i && (Y(t), Y(n), Y(o)), e[8](null), s && s.d(i);
    }
  };
}
function lt(e) {
  const {
    svelteInit: t,
    ...n
  } = e;
  return n;
}
function Ar(e, t, n) {
  let o, r, {
    $$slots: s = {},
    $$scope: i
  } = t;
  const a = Er(s);
  let {
    svelteInit: l
  } = t;
  const f = ue(lt(t)), c = ue();
  ot(e, c, (h) => n(0, o = h));
  const u = ue();
  ot(e, u, (h) => n(1, r = h));
  const d = [], g = Dr("$$ms-gr-react-wrapper"), {
    slotKey: b,
    slotIndex: S,
    subSlotIndex: m
  } = Jt() || {}, y = l({
    parent: g,
    props: f,
    target: c,
    slot: u,
    slotKey: b,
    slotIndex: S,
    subSlotIndex: m,
    onDestroy(h) {
      d.push(h);
    }
  });
  Hr("$$ms-gr-react-wrapper", y), $r(() => {
    f.set(lt(t));
  }), Br(() => {
    d.forEach((h) => h());
  });
  function C(h) {
    nt[h ? "unshift" : "push"](() => {
      o = h, c.set(o);
    });
  }
  function I(h) {
    nt[h ? "unshift" : "push"](() => {
      r = h, u.set(r);
    });
  }
  return e.$$set = (h) => {
    n(17, t = rt(rt({}, t), it(h))), "svelteInit" in h && n(5, l = h.svelteInit), "$$scope" in h && n(6, i = h.$$scope);
  }, t = it(t), [o, r, c, u, a, l, i, s, C, I];
}
class Fr extends wr {
  constructor(t) {
    super(), Rr(this, t, Ar, zr, jr, {
      svelteInit: 5
    });
  }
}
const {
  SvelteComponent: So
} = window.__gradio__svelte__internal, ct = window.ms_globals.rerender, ke = window.ms_globals.tree;
function Xr(e, t = {}) {
  function n(o) {
    const r = ue(), s = new Fr({
      ...o,
      props: {
        svelteInit(i) {
          window.ms_globals.autokey += 1;
          const a = {
            key: window.ms_globals.autokey,
            svelteInstance: r,
            reactComponent: e,
            props: i.props,
            slot: i.slot,
            target: i.target,
            slotIndex: i.slotIndex,
            subSlotIndex: i.subSlotIndex,
            ignore: t.ignore,
            slotKey: i.slotKey,
            nodes: []
          }, l = i.parent ?? ke;
          return l.nodes = [...l.nodes, a], ct({
            createPortal: Be,
            node: ke
          }), i.onDestroy(() => {
            l.nodes = l.nodes.filter((f) => f.svelteInstance !== r), ct({
              createPortal: Be,
              node: ke
            });
          }), a;
        },
        ...o.props
      }
    });
    return r.set(s), s;
  }
  return new Promise((o) => {
    window.ms_globals.initializePromise.then(() => {
      o(n);
    });
  });
}
const Nr = "1.3.0", Vr = /* @__PURE__ */ p.createContext({}), Wr = {
  classNames: {},
  styles: {},
  className: "",
  style: {}
}, Ur = (e) => {
  const t = p.useContext(Vr);
  return p.useMemo(() => ({
    ...Wr,
    ...t[e]
  }), [t[e]]);
};
function J() {
  return J = Object.assign ? Object.assign.bind() : function(e) {
    for (var t = 1; t < arguments.length; t++) {
      var n = arguments[t];
      for (var o in n) ({}).hasOwnProperty.call(n, o) && (e[o] = n[o]);
    }
    return e;
  }, J.apply(null, arguments);
}
function me() {
  const {
    getPrefixCls: e,
    direction: t,
    csp: n,
    iconPrefixCls: o,
    theme: r
  } = p.useContext(er.ConfigContext);
  return {
    theme: r,
    getPrefixCls: e,
    direction: t,
    csp: n,
    iconPrefixCls: o
  };
}
function Gr(e) {
  var t = w.useRef();
  t.current = e;
  var n = w.useCallback(function() {
    for (var o, r = arguments.length, s = new Array(r), i = 0; i < r; i++)
      s[i] = arguments[i];
    return (o = t.current) === null || o === void 0 ? void 0 : o.call.apply(o, [t].concat(s));
  }, []);
  return n;
}
function Kr() {
  return !!(typeof window < "u" && window.document && window.document.createElement);
}
var ut = Kr() ? w.useLayoutEffect : w.useEffect, qr = function(t, n) {
  var o = w.useRef(!0);
  ut(function() {
    return t(o.current);
  }, n), ut(function() {
    return o.current = !1, function() {
      o.current = !0;
    };
  }, []);
};
function se(e) {
  "@babel/helpers - typeof";
  return se = typeof Symbol == "function" && typeof Symbol.iterator == "symbol" ? function(t) {
    return typeof t;
  } : function(t) {
    return t && typeof Symbol == "function" && t.constructor === Symbol && t !== Symbol.prototype ? "symbol" : typeof t;
  }, se(e);
}
var _ = {};
/**
 * @license React
 * react-is.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var Ve = Symbol.for("react.element"), We = Symbol.for("react.portal"), ye = Symbol.for("react.fragment"), ve = Symbol.for("react.strict_mode"), Se = Symbol.for("react.profiler"), xe = Symbol.for("react.provider"), Ce = Symbol.for("react.context"), Yr = Symbol.for("react.server_context"), we = Symbol.for("react.forward_ref"), _e = Symbol.for("react.suspense"), Te = Symbol.for("react.suspense_list"), Ee = Symbol.for("react.memo"), Oe = Symbol.for("react.lazy"), Qr = Symbol.for("react.offscreen"), jt;
jt = Symbol.for("react.module.reference");
function F(e) {
  if (typeof e == "object" && e !== null) {
    var t = e.$$typeof;
    switch (t) {
      case Ve:
        switch (e = e.type, e) {
          case ye:
          case Se:
          case ve:
          case _e:
          case Te:
            return e;
          default:
            switch (e = e && e.$$typeof, e) {
              case Yr:
              case Ce:
              case we:
              case Oe:
              case Ee:
              case xe:
                return e;
              default:
                return t;
            }
        }
      case We:
        return t;
    }
  }
}
_.ContextConsumer = Ce;
_.ContextProvider = xe;
_.Element = Ve;
_.ForwardRef = we;
_.Fragment = ye;
_.Lazy = Oe;
_.Memo = Ee;
_.Portal = We;
_.Profiler = Se;
_.StrictMode = ve;
_.Suspense = _e;
_.SuspenseList = Te;
_.isAsyncMode = function() {
  return !1;
};
_.isConcurrentMode = function() {
  return !1;
};
_.isContextConsumer = function(e) {
  return F(e) === Ce;
};
_.isContextProvider = function(e) {
  return F(e) === xe;
};
_.isElement = function(e) {
  return typeof e == "object" && e !== null && e.$$typeof === Ve;
};
_.isForwardRef = function(e) {
  return F(e) === we;
};
_.isFragment = function(e) {
  return F(e) === ye;
};
_.isLazy = function(e) {
  return F(e) === Oe;
};
_.isMemo = function(e) {
  return F(e) === Ee;
};
_.isPortal = function(e) {
  return F(e) === We;
};
_.isProfiler = function(e) {
  return F(e) === Se;
};
_.isStrictMode = function(e) {
  return F(e) === ve;
};
_.isSuspense = function(e) {
  return F(e) === _e;
};
_.isSuspenseList = function(e) {
  return F(e) === Te;
};
_.isValidElementType = function(e) {
  return typeof e == "string" || typeof e == "function" || e === ye || e === Se || e === ve || e === _e || e === Te || e === Qr || typeof e == "object" && e !== null && (e.$$typeof === Oe || e.$$typeof === Ee || e.$$typeof === xe || e.$$typeof === Ce || e.$$typeof === we || e.$$typeof === jt || e.getModuleId !== void 0);
};
_.typeOf = F;
Number(Wt.split(".")[0]);
function Jr(e, t) {
  if (se(e) != "object" || !e) return e;
  var n = e[Symbol.toPrimitive];
  if (n !== void 0) {
    var o = n.call(e, t);
    if (se(o) != "object") return o;
    throw new TypeError("@@toPrimitive must return a primitive value.");
  }
  return (t === "string" ? String : Number)(e);
}
function Zr(e) {
  var t = Jr(e, "string");
  return se(t) == "symbol" ? t : t + "";
}
function en(e, t, n) {
  return (t = Zr(t)) in e ? Object.defineProperty(e, t, {
    value: n,
    enumerable: !0,
    configurable: !0,
    writable: !0
  }) : e[t] = n, e;
}
function ft(e, t) {
  var n = Object.keys(e);
  if (Object.getOwnPropertySymbols) {
    var o = Object.getOwnPropertySymbols(e);
    t && (o = o.filter(function(r) {
      return Object.getOwnPropertyDescriptor(e, r).enumerable;
    })), n.push.apply(n, o);
  }
  return n;
}
function tn(e) {
  for (var t = 1; t < arguments.length; t++) {
    var n = arguments[t] != null ? arguments[t] : {};
    t % 2 ? ft(Object(n), !0).forEach(function(o) {
      en(e, o, n[o]);
    }) : Object.getOwnPropertyDescriptors ? Object.defineProperties(e, Object.getOwnPropertyDescriptors(n)) : ft(Object(n)).forEach(function(o) {
      Object.defineProperty(e, o, Object.getOwnPropertyDescriptor(n, o));
    });
  }
  return e;
}
function X(e) {
  "@babel/helpers - typeof";
  return X = typeof Symbol == "function" && typeof Symbol.iterator == "symbol" ? function(t) {
    return typeof t;
  } : function(t) {
    return t && typeof Symbol == "function" && t.constructor === Symbol && t !== Symbol.prototype ? "symbol" : typeof t;
  }, X(e);
}
function rn(e, t) {
  if (X(e) != "object" || !e) return e;
  var n = e[Symbol.toPrimitive];
  if (n !== void 0) {
    var o = n.call(e, t);
    if (X(o) != "object") return o;
    throw new TypeError("@@toPrimitive must return a primitive value.");
  }
  return (t === "string" ? String : Number)(e);
}
function kt(e) {
  var t = rn(e, "string");
  return X(t) == "symbol" ? t : t + "";
}
function M(e, t, n) {
  return (t = kt(t)) in e ? Object.defineProperty(e, t, {
    value: n,
    enumerable: !0,
    configurable: !0,
    writable: !0
  }) : e[t] = n, e;
}
function dt(e, t) {
  var n = Object.keys(e);
  if (Object.getOwnPropertySymbols) {
    var o = Object.getOwnPropertySymbols(e);
    t && (o = o.filter(function(r) {
      return Object.getOwnPropertyDescriptor(e, r).enumerable;
    })), n.push.apply(n, o);
  }
  return n;
}
function H(e) {
  for (var t = 1; t < arguments.length; t++) {
    var n = arguments[t] != null ? arguments[t] : {};
    t % 2 ? dt(Object(n), !0).forEach(function(o) {
      M(e, o, n[o]);
    }) : Object.getOwnPropertyDescriptors ? Object.defineProperties(e, Object.getOwnPropertyDescriptors(n)) : dt(Object(n)).forEach(function(o) {
      Object.defineProperty(e, o, Object.getOwnPropertyDescriptor(n, o));
    });
  }
  return e;
}
function nn(e) {
  if (Array.isArray(e)) return e;
}
function on(e, t) {
  var n = e == null ? null : typeof Symbol < "u" && e[Symbol.iterator] || e["@@iterator"];
  if (n != null) {
    var o, r, s, i, a = [], l = !0, f = !1;
    try {
      if (s = (n = n.call(e)).next, t === 0) {
        if (Object(n) !== n) return;
        l = !1;
      } else for (; !(l = (o = s.call(n)).done) && (a.push(o.value), a.length !== t); l = !0) ;
    } catch (c) {
      f = !0, r = c;
    } finally {
      try {
        if (!l && n.return != null && (i = n.return(), Object(i) !== i)) return;
      } finally {
        if (f) throw r;
      }
    }
    return a;
  }
}
function ht(e, t) {
  (t == null || t > e.length) && (t = e.length);
  for (var n = 0, o = Array(t); n < t; n++) o[n] = e[n];
  return o;
}
function sn(e, t) {
  if (e) {
    if (typeof e == "string") return ht(e, t);
    var n = {}.toString.call(e).slice(8, -1);
    return n === "Object" && e.constructor && (n = e.constructor.name), n === "Map" || n === "Set" ? Array.from(e) : n === "Arguments" || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n) ? ht(e, t) : void 0;
  }
}
function an() {
  throw new TypeError(`Invalid attempt to destructure non-iterable instance.
In order to be iterable, non-array objects must have a [Symbol.iterator]() method.`);
}
function he(e, t) {
  return nn(e) || on(e, t) || sn(e, t) || an();
}
function Pe(e, t) {
  if (!(e instanceof t)) throw new TypeError("Cannot call a class as a function");
}
function ln(e, t) {
  for (var n = 0; n < t.length; n++) {
    var o = t[n];
    o.enumerable = o.enumerable || !1, o.configurable = !0, "value" in o && (o.writable = !0), Object.defineProperty(e, kt(o.key), o);
  }
}
function Me(e, t, n) {
  return t && ln(e.prototype, t), Object.defineProperty(e, "prototype", {
    writable: !1
  }), e;
}
function Ae(e, t) {
  return Ae = Object.setPrototypeOf ? Object.setPrototypeOf.bind() : function(n, o) {
    return n.__proto__ = o, n;
  }, Ae(e, t);
}
function Lt(e, t) {
  if (typeof t != "function" && t !== null) throw new TypeError("Super expression must either be null or a function");
  e.prototype = Object.create(t && t.prototype, {
    constructor: {
      value: e,
      writable: !0,
      configurable: !0
    }
  }), Object.defineProperty(e, "prototype", {
    writable: !1
  }), t && Ae(e, t);
}
function pe(e) {
  return pe = Object.setPrototypeOf ? Object.getPrototypeOf.bind() : function(t) {
    return t.__proto__ || Object.getPrototypeOf(t);
  }, pe(e);
}
function $t() {
  try {
    var e = !Boolean.prototype.valueOf.call(Reflect.construct(Boolean, [], function() {
    }));
  } catch {
  }
  return ($t = function() {
    return !!e;
  })();
}
function ne(e) {
  if (e === void 0) throw new ReferenceError("this hasn't been initialised - super() hasn't been called");
  return e;
}
function cn(e, t) {
  if (t && (X(t) == "object" || typeof t == "function")) return t;
  if (t !== void 0) throw new TypeError("Derived constructors may only return object or undefined");
  return ne(e);
}
function Dt(e) {
  var t = $t();
  return function() {
    var n, o = pe(e);
    if (t) {
      var r = pe(this).constructor;
      n = Reflect.construct(o, arguments, r);
    } else n = o.apply(this, arguments);
    return cn(this, n);
  };
}
var Bt = /* @__PURE__ */ Me(function e() {
  Pe(this, e);
}), Ht = "CALC_UNIT", un = new RegExp(Ht, "g");
function Le(e) {
  return typeof e == "number" ? "".concat(e).concat(Ht) : e;
}
var fn = /* @__PURE__ */ function(e) {
  Lt(n, e);
  var t = Dt(n);
  function n(o, r) {
    var s;
    Pe(this, n), s = t.call(this), M(ne(s), "result", ""), M(ne(s), "unitlessCssVar", void 0), M(ne(s), "lowPriority", void 0);
    var i = X(o);
    return s.unitlessCssVar = r, o instanceof n ? s.result = "(".concat(o.result, ")") : i === "number" ? s.result = Le(o) : i === "string" && (s.result = o), s;
  }
  return Me(n, [{
    key: "add",
    value: function(r) {
      return r instanceof n ? this.result = "".concat(this.result, " + ").concat(r.getResult()) : (typeof r == "number" || typeof r == "string") && (this.result = "".concat(this.result, " + ").concat(Le(r))), this.lowPriority = !0, this;
    }
  }, {
    key: "sub",
    value: function(r) {
      return r instanceof n ? this.result = "".concat(this.result, " - ").concat(r.getResult()) : (typeof r == "number" || typeof r == "string") && (this.result = "".concat(this.result, " - ").concat(Le(r))), this.lowPriority = !0, this;
    }
  }, {
    key: "mul",
    value: function(r) {
      return this.lowPriority && (this.result = "(".concat(this.result, ")")), r instanceof n ? this.result = "".concat(this.result, " * ").concat(r.getResult(!0)) : (typeof r == "number" || typeof r == "string") && (this.result = "".concat(this.result, " * ").concat(r)), this.lowPriority = !1, this;
    }
  }, {
    key: "div",
    value: function(r) {
      return this.lowPriority && (this.result = "(".concat(this.result, ")")), r instanceof n ? this.result = "".concat(this.result, " / ").concat(r.getResult(!0)) : (typeof r == "number" || typeof r == "string") && (this.result = "".concat(this.result, " / ").concat(r)), this.lowPriority = !1, this;
    }
  }, {
    key: "getResult",
    value: function(r) {
      return this.lowPriority || r ? "(".concat(this.result, ")") : this.result;
    }
  }, {
    key: "equal",
    value: function(r) {
      var s = this, i = r || {}, a = i.unit, l = !0;
      return typeof a == "boolean" ? l = a : Array.from(this.unitlessCssVar).some(function(f) {
        return s.result.includes(f);
      }) && (l = !1), this.result = this.result.replace(un, l ? "px" : ""), typeof this.lowPriority < "u" ? "calc(".concat(this.result, ")") : this.result;
    }
  }]), n;
}(Bt), dn = /* @__PURE__ */ function(e) {
  Lt(n, e);
  var t = Dt(n);
  function n(o) {
    var r;
    return Pe(this, n), r = t.call(this), M(ne(r), "result", 0), o instanceof n ? r.result = o.result : typeof o == "number" && (r.result = o), r;
  }
  return Me(n, [{
    key: "add",
    value: function(r) {
      return r instanceof n ? this.result += r.result : typeof r == "number" && (this.result += r), this;
    }
  }, {
    key: "sub",
    value: function(r) {
      return r instanceof n ? this.result -= r.result : typeof r == "number" && (this.result -= r), this;
    }
  }, {
    key: "mul",
    value: function(r) {
      return r instanceof n ? this.result *= r.result : typeof r == "number" && (this.result *= r), this;
    }
  }, {
    key: "div",
    value: function(r) {
      return r instanceof n ? this.result /= r.result : typeof r == "number" && (this.result /= r), this;
    }
  }, {
    key: "equal",
    value: function() {
      return this.result;
    }
  }]), n;
}(Bt), hn = function(t, n) {
  var o = t === "css" ? fn : dn;
  return function(r) {
    return new o(r, n);
  };
}, gt = function(t, n) {
  return "".concat([n, t.replace(/([A-Z]+)([A-Z][a-z]+)/g, "$1-$2").replace(/([a-z])([A-Z])/g, "$1-$2")].filter(Boolean).join("-"));
};
function mt(e, t, n, o) {
  var r = H({}, t[e]);
  if (o != null && o.deprecatedTokens) {
    var s = o.deprecatedTokens;
    s.forEach(function(a) {
      var l = he(a, 2), f = l[0], c = l[1];
      if (r != null && r[f] || r != null && r[c]) {
        var u;
        (u = r[c]) !== null && u !== void 0 || (r[c] = r == null ? void 0 : r[f]);
      }
    });
  }
  var i = H(H({}, n), r);
  return Object.keys(i).forEach(function(a) {
    i[a] === t[a] && delete i[a];
  }), i;
}
var zt = typeof CSSINJS_STATISTIC < "u", Fe = !0;
function Ue() {
  for (var e = arguments.length, t = new Array(e), n = 0; n < e; n++)
    t[n] = arguments[n];
  if (!zt)
    return Object.assign.apply(Object, [{}].concat(t));
  Fe = !1;
  var o = {};
  return t.forEach(function(r) {
    if (X(r) === "object") {
      var s = Object.keys(r);
      s.forEach(function(i) {
        Object.defineProperty(o, i, {
          configurable: !0,
          enumerable: !0,
          get: function() {
            return r[i];
          }
        });
      });
    }
  }), Fe = !0, o;
}
var pt = {};
function gn() {
}
var mn = function(t) {
  var n, o = t, r = gn;
  return zt && typeof Proxy < "u" && (n = /* @__PURE__ */ new Set(), o = new Proxy(t, {
    get: function(i, a) {
      if (Fe) {
        var l;
        (l = n) === null || l === void 0 || l.add(a);
      }
      return i[a];
    }
  }), r = function(i, a) {
    var l;
    pt[i] = {
      global: Array.from(n),
      component: H(H({}, (l = pt[i]) === null || l === void 0 ? void 0 : l.component), a)
    };
  }), {
    token: o,
    keys: n,
    flush: r
  };
};
function bt(e, t, n) {
  if (typeof n == "function") {
    var o;
    return n(Ue(t, (o = t[e]) !== null && o !== void 0 ? o : {}));
  }
  return n ?? {};
}
function pn(e) {
  return e === "js" ? {
    max: Math.max,
    min: Math.min
  } : {
    max: function() {
      for (var n = arguments.length, o = new Array(n), r = 0; r < n; r++)
        o[r] = arguments[r];
      return "max(".concat(o.map(function(s) {
        return oe(s);
      }).join(","), ")");
    },
    min: function() {
      for (var n = arguments.length, o = new Array(n), r = 0; r < n; r++)
        o[r] = arguments[r];
      return "min(".concat(o.map(function(s) {
        return oe(s);
      }).join(","), ")");
    }
  };
}
var bn = 1e3 * 60 * 10, yn = /* @__PURE__ */ function() {
  function e() {
    Pe(this, e), M(this, "map", /* @__PURE__ */ new Map()), M(this, "objectIDMap", /* @__PURE__ */ new WeakMap()), M(this, "nextID", 0), M(this, "lastAccessBeat", /* @__PURE__ */ new Map()), M(this, "accessBeat", 0);
  }
  return Me(e, [{
    key: "set",
    value: function(n, o) {
      this.clear();
      var r = this.getCompositeKey(n);
      this.map.set(r, o), this.lastAccessBeat.set(r, Date.now());
    }
  }, {
    key: "get",
    value: function(n) {
      var o = this.getCompositeKey(n), r = this.map.get(o);
      return this.lastAccessBeat.set(o, Date.now()), this.accessBeat += 1, r;
    }
  }, {
    key: "getCompositeKey",
    value: function(n) {
      var o = this, r = n.map(function(s) {
        return s && X(s) === "object" ? "obj_".concat(o.getObjectID(s)) : "".concat(X(s), "_").concat(s);
      });
      return r.join("|");
    }
  }, {
    key: "getObjectID",
    value: function(n) {
      if (this.objectIDMap.has(n))
        return this.objectIDMap.get(n);
      var o = this.nextID;
      return this.objectIDMap.set(n, o), this.nextID += 1, o;
    }
  }, {
    key: "clear",
    value: function() {
      var n = this;
      if (this.accessBeat > 1e4) {
        var o = Date.now();
        this.lastAccessBeat.forEach(function(r, s) {
          o - r > bn && (n.map.delete(s), n.lastAccessBeat.delete(s));
        }), this.accessBeat = 0;
      }
    }
  }]), e;
}(), yt = new yn();
function vn(e, t) {
  return p.useMemo(function() {
    var n = yt.get(t);
    if (n)
      return n;
    var o = e();
    return yt.set(t, o), o;
  }, t);
}
var Sn = function() {
  return {};
};
function xn(e) {
  var t = e.useCSP, n = t === void 0 ? Sn : t, o = e.useToken, r = e.usePrefix, s = e.getResetStyles, i = e.getCommonStyle, a = e.getCompUnitless;
  function l(d, g, b, S) {
    var m = Array.isArray(d) ? d[0] : d;
    function y(P) {
      return "".concat(String(m)).concat(P.slice(0, 1).toUpperCase()).concat(P.slice(1));
    }
    var C = (S == null ? void 0 : S.unitless) || {}, I = typeof a == "function" ? a(d) : {}, h = H(H({}, I), {}, M({}, y("zIndexPopup"), !0));
    Object.keys(C).forEach(function(P) {
      h[y(P)] = C[P];
    });
    var E = H(H({}, S), {}, {
      unitless: h,
      prefixToken: y
    }), v = c(d, g, b, E), O = f(m, b, E);
    return function(P) {
      var R = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : P, T = v(P, R), k = he(T, 2), x = k[1], j = O(R), L = he(j, 2), D = L[0], B = L[1];
      return [D, x, B];
    };
  }
  function f(d, g, b) {
    var S = b.unitless, m = b.injectStyle, y = m === void 0 ? !0 : m, C = b.prefixToken, I = b.ignore, h = function(O) {
      var P = O.rootCls, R = O.cssVar, T = R === void 0 ? {} : R, k = o(), x = k.realToken;
      return rr({
        path: [d],
        prefix: T.prefix,
        key: T.key,
        unitless: S,
        ignore: I,
        token: x,
        scope: P
      }, function() {
        var j = bt(d, x, g), L = mt(d, x, j, {
          deprecatedTokens: b == null ? void 0 : b.deprecatedTokens
        });
        return Object.keys(j).forEach(function(D) {
          L[C(D)] = L[D], delete L[D];
        }), L;
      }), null;
    }, E = function(O) {
      var P = o(), R = P.cssVar;
      return [function(T) {
        return y && R ? /* @__PURE__ */ p.createElement(p.Fragment, null, /* @__PURE__ */ p.createElement(h, {
          rootCls: O,
          cssVar: R,
          component: d
        }), T) : T;
      }, R == null ? void 0 : R.key];
    };
    return E;
  }
  function c(d, g, b) {
    var S = arguments.length > 3 && arguments[3] !== void 0 ? arguments[3] : {}, m = Array.isArray(d) ? d : [d, d], y = he(m, 1), C = y[0], I = m.join("-"), h = e.layer || {
      name: "antd"
    };
    return function(E) {
      var v = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : E, O = o(), P = O.theme, R = O.realToken, T = O.hashId, k = O.token, x = O.cssVar, j = r(), L = j.rootPrefixCls, D = j.iconPrefixCls, B = n(), z = x ? "css" : "js", V = vn(function() {
        var W = /* @__PURE__ */ new Set();
        return x && Object.keys(S.unitless || {}).forEach(function(G) {
          W.add(Re(G, x.prefix)), W.add(Re(G, gt(C, x.prefix)));
        }), hn(z, W);
      }, [z, C, x == null ? void 0 : x.prefix]), K = pn(z), ie = K.max, Z = K.min, ae = {
        theme: P,
        token: k,
        hashId: T,
        nonce: function() {
          return B.nonce;
        },
        clientOnly: S.clientOnly,
        layer: h,
        // antd is always at top of styles
        order: S.order || -999
      };
      typeof s == "function" && Ze(H(H({}, ae), {}, {
        clientOnly: !1,
        path: ["Shared", L]
      }), function() {
        return s(k, {
          prefix: {
            rootPrefixCls: L,
            iconPrefixCls: D
          },
          csp: B
        });
      });
      var Ie = Ze(H(H({}, ae), {}, {
        path: [I, E, D]
      }), function() {
        if (S.injectStyle === !1)
          return [];
        var W = mn(k), G = W.token, ee = W.flush, N = bt(C, R, b), te = ".".concat(E), qe = mt(C, R, N, {
          deprecatedTokens: S.deprecatedTokens
        });
        x && N && X(N) === "object" && Object.keys(N).forEach(function(Qe) {
          N[Qe] = "var(".concat(Re(Qe, gt(C, x.prefix)), ")");
        });
        var Ye = Ue(G, {
          componentCls: te,
          prefixCls: E,
          iconCls: ".".concat(D),
          antCls: ".".concat(L),
          calc: V,
          // @ts-ignore
          max: ie,
          // @ts-ignore
          min: Z
        }, x ? N : qe), Nt = g(Ye, {
          hashId: T,
          prefixCls: E,
          rootPrefixCls: L,
          iconPrefixCls: D
        });
        ee(C, qe);
        var Vt = typeof i == "function" ? i(Ye, E, v, S.resetFont) : null;
        return [S.resetStyle === !1 ? null : Vt, Nt];
      });
      return [Ie, T];
    };
  }
  function u(d, g, b) {
    var S = arguments.length > 3 && arguments[3] !== void 0 ? arguments[3] : {}, m = c(d, g, b, H({
      resetStyle: !1,
      // Sub Style should default after root one
      order: -998
    }, S)), y = function(I) {
      var h = I.prefixCls, E = I.rootCls, v = E === void 0 ? h : E;
      return m(h, v), null;
    };
    return y;
  }
  return {
    genStyleHooks: l,
    genSubStyleComponent: u,
    genComponentStyleHook: c
  };
}
const $ = Math.round;
function $e(e, t) {
  const n = e.replace(/^[^(]*\((.*)/, "$1").replace(/\).*/, "").match(/\d*\.?\d+%?/g) || [], o = n.map((r) => parseFloat(r));
  for (let r = 0; r < 3; r += 1)
    o[r] = t(o[r] || 0, n[r] || "", r);
  return n[3] ? o[3] = n[3].includes("%") ? o[3] / 100 : o[3] : o[3] = 1, o;
}
const vt = (e, t, n) => n === 0 ? e : e / 100;
function re(e, t) {
  const n = t || 255;
  return e > n ? n : e < 0 ? 0 : e;
}
class U {
  constructor(t) {
    M(this, "isValid", !0), M(this, "r", 0), M(this, "g", 0), M(this, "b", 0), M(this, "a", 1), M(this, "_h", void 0), M(this, "_s", void 0), M(this, "_l", void 0), M(this, "_v", void 0), M(this, "_max", void 0), M(this, "_min", void 0), M(this, "_brightness", void 0);
    function n(o) {
      return o[0] in t && o[1] in t && o[2] in t;
    }
    if (t) if (typeof t == "string") {
      let r = function(s) {
        return o.startsWith(s);
      };
      const o = t.trim();
      /^#?[A-F\d]{3,8}$/i.test(o) ? this.fromHexString(o) : r("rgb") ? this.fromRgbString(o) : r("hsl") ? this.fromHslString(o) : (r("hsv") || r("hsb")) && this.fromHsvString(o);
    } else if (t instanceof U)
      this.r = t.r, this.g = t.g, this.b = t.b, this.a = t.a, this._h = t._h, this._s = t._s, this._l = t._l, this._v = t._v;
    else if (n("rgb"))
      this.r = re(t.r), this.g = re(t.g), this.b = re(t.b), this.a = typeof t.a == "number" ? re(t.a, 1) : 1;
    else if (n("hsl"))
      this.fromHsl(t);
    else if (n("hsv"))
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
    const n = this.toHsv();
    return n.h = t, this._c(n);
  }
  // ======================= Getter =======================
  /**
   * Returns the perceived luminance of a color, from 0-1.
   * @see http://www.w3.org/TR/2008/REC-WCAG20-20081211/#relativeluminancedef
   */
  getLuminance() {
    function t(s) {
      const i = s / 255;
      return i <= 0.03928 ? i / 12.92 : Math.pow((i + 0.055) / 1.055, 2.4);
    }
    const n = t(this.r), o = t(this.g), r = t(this.b);
    return 0.2126 * n + 0.7152 * o + 0.0722 * r;
  }
  getHue() {
    if (typeof this._h > "u") {
      const t = this.getMax() - this.getMin();
      t === 0 ? this._h = 0 : this._h = $(60 * (this.r === this.getMax() ? (this.g - this.b) / t + (this.g < this.b ? 6 : 0) : this.g === this.getMax() ? (this.b - this.r) / t + 2 : (this.r - this.g) / t + 4));
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
    const n = this.getHue(), o = this.getSaturation();
    let r = this.getLightness() - t / 100;
    return r < 0 && (r = 0), this._c({
      h: n,
      s: o,
      l: r,
      a: this.a
    });
  }
  lighten(t = 10) {
    const n = this.getHue(), o = this.getSaturation();
    let r = this.getLightness() + t / 100;
    return r > 1 && (r = 1), this._c({
      h: n,
      s: o,
      l: r,
      a: this.a
    });
  }
  /**
   * Mix the current color a given amount with another color, from 0 to 100.
   * 0 means no mixing (return current color).
   */
  mix(t, n = 50) {
    const o = this._c(t), r = n / 100, s = (a) => (o[a] - this[a]) * r + this[a], i = {
      r: $(s("r")),
      g: $(s("g")),
      b: $(s("b")),
      a: $(s("a") * 100) / 100
    };
    return this._c(i);
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
    const n = this._c(t), o = this.a + n.a * (1 - this.a), r = (s) => $((this[s] * this.a + n[s] * n.a * (1 - this.a)) / o);
    return this._c({
      r: r("r"),
      g: r("g"),
      b: r("b"),
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
    const n = (this.r || 0).toString(16);
    t += n.length === 2 ? n : "0" + n;
    const o = (this.g || 0).toString(16);
    t += o.length === 2 ? o : "0" + o;
    const r = (this.b || 0).toString(16);
    if (t += r.length === 2 ? r : "0" + r, typeof this.a == "number" && this.a >= 0 && this.a < 1) {
      const s = $(this.a * 255).toString(16);
      t += s.length === 2 ? s : "0" + s;
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
    const t = this.getHue(), n = $(this.getSaturation() * 100), o = $(this.getLightness() * 100);
    return this.a !== 1 ? `hsla(${t},${n}%,${o}%,${this.a})` : `hsl(${t},${n}%,${o}%)`;
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
  _sc(t, n, o) {
    const r = this.clone();
    return r[t] = re(n, o), r;
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
    const n = t.replace("#", "");
    function o(r, s) {
      return parseInt(n[r] + n[s || r], 16);
    }
    n.length < 6 ? (this.r = o(0), this.g = o(1), this.b = o(2), this.a = n[3] ? o(3) / 255 : 1) : (this.r = o(0, 1), this.g = o(2, 3), this.b = o(4, 5), this.a = n[6] ? o(6, 7) / 255 : 1);
  }
  fromHsl({
    h: t,
    s: n,
    l: o,
    a: r
  }) {
    if (this._h = t % 360, this._s = n, this._l = o, this.a = typeof r == "number" ? r : 1, n <= 0) {
      const d = $(o * 255);
      this.r = d, this.g = d, this.b = d;
    }
    let s = 0, i = 0, a = 0;
    const l = t / 60, f = (1 - Math.abs(2 * o - 1)) * n, c = f * (1 - Math.abs(l % 2 - 1));
    l >= 0 && l < 1 ? (s = f, i = c) : l >= 1 && l < 2 ? (s = c, i = f) : l >= 2 && l < 3 ? (i = f, a = c) : l >= 3 && l < 4 ? (i = c, a = f) : l >= 4 && l < 5 ? (s = c, a = f) : l >= 5 && l < 6 && (s = f, a = c);
    const u = o - f / 2;
    this.r = $((s + u) * 255), this.g = $((i + u) * 255), this.b = $((a + u) * 255);
  }
  fromHsv({
    h: t,
    s: n,
    v: o,
    a: r
  }) {
    this._h = t % 360, this._s = n, this._v = o, this.a = typeof r == "number" ? r : 1;
    const s = $(o * 255);
    if (this.r = s, this.g = s, this.b = s, n <= 0)
      return;
    const i = t / 60, a = Math.floor(i), l = i - a, f = $(o * (1 - n) * 255), c = $(o * (1 - n * l) * 255), u = $(o * (1 - n * (1 - l)) * 255);
    switch (a) {
      case 0:
        this.g = u, this.b = f;
        break;
      case 1:
        this.r = c, this.b = f;
        break;
      case 2:
        this.r = f, this.b = u;
        break;
      case 3:
        this.r = f, this.g = c;
        break;
      case 4:
        this.r = u, this.g = f;
        break;
      case 5:
      default:
        this.g = f, this.b = c;
        break;
    }
  }
  fromHsvString(t) {
    const n = $e(t, vt);
    this.fromHsv({
      h: n[0],
      s: n[1],
      v: n[2],
      a: n[3]
    });
  }
  fromHslString(t) {
    const n = $e(t, vt);
    this.fromHsl({
      h: n[0],
      s: n[1],
      l: n[2],
      a: n[3]
    });
  }
  fromRgbString(t) {
    const n = $e(t, (o, r) => (
      // Convert percentage to number. e.g. 50% -> 128
      r.includes("%") ? $(o / 100 * 255) : o
    ));
    this.r = n[0], this.g = n[1], this.b = n[2], this.a = n[3];
  }
}
const Cn = {
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
}, wn = Object.assign(Object.assign({}, Cn), {
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
function De(e) {
  return e >= 0 && e <= 255;
}
function le(e, t) {
  const {
    r: n,
    g: o,
    b: r,
    a: s
  } = new U(e).toRgb();
  if (s < 1)
    return e;
  const {
    r: i,
    g: a,
    b: l
  } = new U(t).toRgb();
  for (let f = 0.01; f <= 1; f += 0.01) {
    const c = Math.round((n - i * (1 - f)) / f), u = Math.round((o - a * (1 - f)) / f), d = Math.round((r - l * (1 - f)) / f);
    if (De(c) && De(u) && De(d))
      return new U({
        r: c,
        g: u,
        b: d,
        a: Math.round(f * 100) / 100
      }).toRgbString();
  }
  return new U({
    r: n,
    g: o,
    b: r,
    a: 1
  }).toRgbString();
}
var _n = function(e, t) {
  var n = {};
  for (var o in e) Object.prototype.hasOwnProperty.call(e, o) && t.indexOf(o) < 0 && (n[o] = e[o]);
  if (e != null && typeof Object.getOwnPropertySymbols == "function") for (var r = 0, o = Object.getOwnPropertySymbols(e); r < o.length; r++)
    t.indexOf(o[r]) < 0 && Object.prototype.propertyIsEnumerable.call(e, o[r]) && (n[o[r]] = e[o[r]]);
  return n;
};
function Tn(e) {
  const {
    override: t
  } = e, n = _n(e, ["override"]), o = Object.assign({}, t);
  Object.keys(wn).forEach((d) => {
    delete o[d];
  });
  const r = Object.assign(Object.assign({}, n), o), s = 480, i = 576, a = 768, l = 992, f = 1200, c = 1600;
  if (r.motion === !1) {
    const d = "0s";
    r.motionDurationFast = d, r.motionDurationMid = d, r.motionDurationSlow = d;
  }
  return Object.assign(Object.assign(Object.assign({}, r), {
    // ============== Background ============== //
    colorFillContent: r.colorFillSecondary,
    colorFillContentHover: r.colorFill,
    colorFillAlter: r.colorFillQuaternary,
    colorBgContainerDisabled: r.colorFillTertiary,
    // ============== Split ============== //
    colorBorderBg: r.colorBgContainer,
    colorSplit: le(r.colorBorderSecondary, r.colorBgContainer),
    // ============== Text ============== //
    colorTextPlaceholder: r.colorTextQuaternary,
    colorTextDisabled: r.colorTextQuaternary,
    colorTextHeading: r.colorText,
    colorTextLabel: r.colorTextSecondary,
    colorTextDescription: r.colorTextTertiary,
    colorTextLightSolid: r.colorWhite,
    colorHighlight: r.colorError,
    colorBgTextHover: r.colorFillSecondary,
    colorBgTextActive: r.colorFill,
    colorIcon: r.colorTextTertiary,
    colorIconHover: r.colorText,
    colorErrorOutline: le(r.colorErrorBg, r.colorBgContainer),
    colorWarningOutline: le(r.colorWarningBg, r.colorBgContainer),
    // Font
    fontSizeIcon: r.fontSizeSM,
    // Line
    lineWidthFocus: r.lineWidth * 3,
    // Control
    lineWidth: r.lineWidth,
    controlOutlineWidth: r.lineWidth * 2,
    // Checkbox size and expand icon size
    controlInteractiveSize: r.controlHeight / 2,
    controlItemBgHover: r.colorFillTertiary,
    controlItemBgActive: r.colorPrimaryBg,
    controlItemBgActiveHover: r.colorPrimaryBgHover,
    controlItemBgActiveDisabled: r.colorFill,
    controlTmpOutline: r.colorFillQuaternary,
    controlOutline: le(r.colorPrimaryBg, r.colorBgContainer),
    lineType: r.lineType,
    borderRadius: r.borderRadius,
    borderRadiusXS: r.borderRadiusXS,
    borderRadiusSM: r.borderRadiusSM,
    borderRadiusLG: r.borderRadiusLG,
    fontWeightStrong: 600,
    opacityLoading: 0.65,
    linkDecoration: "none",
    linkHoverDecoration: "none",
    linkFocusDecoration: "none",
    controlPaddingHorizontal: 12,
    controlPaddingHorizontalSM: 8,
    paddingXXS: r.sizeXXS,
    paddingXS: r.sizeXS,
    paddingSM: r.sizeSM,
    padding: r.size,
    paddingMD: r.sizeMD,
    paddingLG: r.sizeLG,
    paddingXL: r.sizeXL,
    paddingContentHorizontalLG: r.sizeLG,
    paddingContentVerticalLG: r.sizeMS,
    paddingContentHorizontal: r.sizeMS,
    paddingContentVertical: r.sizeSM,
    paddingContentHorizontalSM: r.size,
    paddingContentVerticalSM: r.sizeXS,
    marginXXS: r.sizeXXS,
    marginXS: r.sizeXS,
    marginSM: r.sizeSM,
    margin: r.size,
    marginMD: r.sizeMD,
    marginLG: r.sizeLG,
    marginXL: r.sizeXL,
    marginXXL: r.sizeXXL,
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
    screenXS: s,
    screenXSMin: s,
    screenXSMax: i - 1,
    screenSM: i,
    screenSMMin: i,
    screenSMMax: a - 1,
    screenMD: a,
    screenMDMin: a,
    screenMDMax: l - 1,
    screenLG: l,
    screenLGMin: l,
    screenLGMax: f - 1,
    screenXL: f,
    screenXLMin: f,
    screenXLMax: c - 1,
    screenXXL: c,
    screenXXLMin: c,
    boxShadowPopoverArrow: "2px 2px 5px rgba(0, 0, 0, 0.05)",
    boxShadowCard: `
      0 1px 2px -2px ${new U("rgba(0, 0, 0, 0.16)").toRgbString()},
      0 3px 6px 0 ${new U("rgba(0, 0, 0, 0.12)").toRgbString()},
      0 5px 12px 4px ${new U("rgba(0, 0, 0, 0.09)").toRgbString()}
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
const En = {
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
}, On = {
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
}, Pn = nr(He.defaultAlgorithm), Mn = {
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
}, At = (e, t, n) => {
  const o = n.getDerivativeToken(e), {
    override: r,
    ...s
  } = t;
  let i = {
    ...o,
    override: r
  };
  return i = Tn(i), s && Object.entries(s).forEach(([a, l]) => {
    const {
      theme: f,
      ...c
    } = l;
    let u = c;
    f && (u = At({
      ...i,
      ...c
    }, {
      override: c
    }, f)), i[a] = u;
  }), i;
};
function In() {
  const {
    token: e,
    hashed: t,
    theme: n = Pn,
    override: o,
    cssVar: r
  } = p.useContext(He._internalContext), [s, i, a] = or(n, [He.defaultSeed, e], {
    salt: `${Nr}-${t || ""}`,
    override: o,
    getComputedToken: At,
    cssVar: r && {
      prefix: r.prefix,
      key: r.key,
      unitless: En,
      ignore: On,
      preserve: Mn
    }
  });
  return [n, a, t ? i : "", s, r];
}
const {
  genStyleHooks: Rn
} = xn({
  usePrefix: () => {
    const {
      getPrefixCls: e,
      iconPrefixCls: t
    } = me();
    return {
      iconPrefixCls: t,
      rootPrefixCls: e()
    };
  },
  useToken: () => {
    const [e, t, n, o, r] = In();
    return {
      theme: e,
      realToken: t,
      hashId: n,
      token: o,
      cssVar: r
    };
  },
  useCSP: () => {
    const {
      csp: e
    } = me();
    return e ?? {};
  },
  layer: {
    name: "antdx",
    dependencies: ["antd"]
  }
});
var jn = `accept acceptCharset accessKey action allowFullScreen allowTransparency
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
    summary tabIndex target title type useMap value width wmode wrap`, kn = `onCopy onCut onPaste onCompositionEnd onCompositionStart onCompositionUpdate onKeyDown
    onKeyPress onKeyUp onFocus onBlur onChange onInput onSubmit onClick onContextMenu onDoubleClick
    onDrag onDragEnd onDragEnter onDragExit onDragLeave onDragOver onDragStart onDrop onMouseDown
    onMouseEnter onMouseLeave onMouseMove onMouseOut onMouseOver onMouseUp onSelect onTouchCancel
    onTouchEnd onTouchMove onTouchStart onScroll onWheel onAbort onCanPlay onCanPlayThrough
    onDurationChange onEmptied onEncrypted onEnded onError onLoadedData onLoadedMetadata
    onLoadStart onPause onPlay onPlaying onProgress onRateChange onSeeked onSeeking onStalled onSuspend onTimeUpdate onVolumeChange onWaiting onLoad onError`, Ln = "".concat(jn, " ").concat(kn).split(/[\s\n]+/), $n = "aria-", Dn = "data-";
function St(e, t) {
  return e.indexOf(t) === 0;
}
function Bn(e) {
  var t = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : !1, n;
  t === !1 ? n = {
    aria: !0,
    data: !0,
    attr: !0
  } : t === !0 ? n = {
    aria: !0
  } : n = tn({}, t);
  var o = {};
  return Object.keys(e).forEach(function(r) {
    // Aria
    (n.aria && (r === "role" || St(r, $n)) || // Data
    n.data && St(r, Dn) || // Attr
    n.attr && Ln.includes(r)) && (o[r] = e[r]);
  }), o;
}
function ce(e) {
  return typeof e == "string";
}
const Hn = (e, t, n, o) => {
  const r = w.useRef(""), [s, i] = w.useState(1), a = t && ce(e);
  return qr(() => {
    !a && ce(e) ? i(e.length) : ce(e) && ce(r.current) && e.indexOf(r.current) !== 0 && i(1), r.current = e;
  }, [e]), w.useEffect(() => {
    if (a && s < e.length) {
      const f = setTimeout(() => {
        i((c) => c + n);
      }, o);
      return () => {
        clearTimeout(f);
      };
    }
  }, [s, t, e]), [a ? e.slice(0, s) : e, a && s < e.length];
};
function zn(e) {
  return w.useMemo(() => {
    if (!e)
      return [!1, 0, 0, null];
    let t = {
      step: 1,
      interval: 50,
      // set default suffix is empty
      suffix: null
    };
    return typeof e == "object" && (t = {
      ...t,
      ...e
    }), [!0, t.step, t.interval, t.suffix];
  }, [e]);
}
const An = ({
  prefixCls: e
}) => /* @__PURE__ */ p.createElement("span", {
  className: `${e}-dot`
}, /* @__PURE__ */ p.createElement("i", {
  className: `${e}-dot-item`,
  key: "item-1"
}), /* @__PURE__ */ p.createElement("i", {
  className: `${e}-dot-item`,
  key: "item-2"
}), /* @__PURE__ */ p.createElement("i", {
  className: `${e}-dot-item`,
  key: "item-3"
})), Fn = (e) => {
  const {
    componentCls: t,
    paddingSM: n,
    padding: o
  } = e;
  return {
    [t]: {
      [`${t}-content`]: {
        // Shared: filled, outlined, shadow
        "&-filled,&-outlined,&-shadow": {
          padding: `${oe(n)} ${oe(o)}`,
          borderRadius: e.borderRadiusLG
        },
        // Filled:
        "&-filled": {
          backgroundColor: e.colorFillContent
        },
        // Outlined:
        "&-outlined": {
          border: `1px solid ${e.colorBorderSecondary}`
        },
        // Shadow:
        "&-shadow": {
          boxShadow: e.boxShadowTertiary
        }
      }
    }
  };
}, Xn = (e) => {
  const {
    componentCls: t,
    fontSize: n,
    lineHeight: o,
    paddingSM: r,
    padding: s,
    calc: i
  } = e, a = i(n).mul(o).div(2).add(r).equal(), l = `${t}-content`;
  return {
    [t]: {
      [l]: {
        // round:
        "&-round": {
          borderRadius: {
            _skip_check_: !0,
            value: a
          },
          paddingInline: i(s).mul(1.25).equal()
        }
      },
      // corner:
      [`&-start ${l}-corner`]: {
        borderStartStartRadius: e.borderRadiusXS
      },
      [`&-end ${l}-corner`]: {
        borderStartEndRadius: e.borderRadiusXS
      }
    }
  };
}, Nn = (e) => {
  const {
    componentCls: t,
    padding: n
  } = e;
  return {
    [`${t}-list`]: {
      display: "flex",
      flexDirection: "column",
      gap: n,
      overflowY: "auto",
      "&::-webkit-scrollbar": {
        width: 8,
        backgroundColor: "transparent"
      },
      "&::-webkit-scrollbar-thumb": {
        backgroundColor: e.colorTextTertiary,
        borderRadius: e.borderRadiusSM
      },
      // For Firefox
      "&": {
        scrollbarWidth: "thin",
        scrollbarColor: `${e.colorTextTertiary} transparent`
      }
    }
  };
}, Vn = new Tt("loadingMove", {
  "0%": {
    transform: "translateY(0)"
  },
  "10%": {
    transform: "translateY(4px)"
  },
  "20%": {
    transform: "translateY(0)"
  },
  "30%": {
    transform: "translateY(-4px)"
  },
  "40%": {
    transform: "translateY(0)"
  }
}), Wn = new Tt("cursorBlink", {
  "0%": {
    opacity: 1
  },
  "50%": {
    opacity: 0
  },
  "100%": {
    opacity: 1
  }
}), Un = (e) => {
  const {
    componentCls: t,
    fontSize: n,
    lineHeight: o,
    paddingSM: r,
    colorText: s,
    calc: i
  } = e;
  return {
    [t]: {
      display: "flex",
      columnGap: r,
      [`&${t}-end`]: {
        justifyContent: "end",
        flexDirection: "row-reverse",
        [`& ${t}-content-wrapper`]: {
          alignItems: "flex-end"
        }
      },
      [`&${t}-rtl`]: {
        direction: "rtl"
      },
      [`&${t}-typing ${t}-content:last-child::after`]: {
        content: '"|"',
        fontWeight: 900,
        userSelect: "none",
        opacity: 1,
        marginInlineStart: "0.1em",
        animationName: Wn,
        animationDuration: "0.8s",
        animationIterationCount: "infinite",
        animationTimingFunction: "linear"
      },
      // ============================ Avatar =============================
      [`& ${t}-avatar`]: {
        display: "inline-flex",
        justifyContent: "center",
        alignSelf: "flex-start"
      },
      // ======================== Header & Footer ========================
      [`& ${t}-header, & ${t}-footer`]: {
        fontSize: n,
        lineHeight: o,
        color: e.colorText
      },
      [`& ${t}-header`]: {
        marginBottom: e.paddingXXS
      },
      [`& ${t}-footer`]: {
        marginTop: r
      },
      // =========================== Content =============================
      [`& ${t}-content-wrapper`]: {
        flex: "auto",
        display: "flex",
        flexDirection: "column",
        alignItems: "flex-start",
        minWidth: 0,
        maxWidth: "100%"
      },
      [`& ${t}-content`]: {
        position: "relative",
        boxSizing: "border-box",
        minWidth: 0,
        maxWidth: "100%",
        color: s,
        fontSize: e.fontSize,
        lineHeight: e.lineHeight,
        minHeight: i(r).mul(2).add(i(o).mul(n)).equal(),
        wordBreak: "break-word",
        [`& ${t}-dot`]: {
          position: "relative",
          height: "100%",
          display: "flex",
          alignItems: "center",
          columnGap: e.marginXS,
          padding: `0 ${oe(e.paddingXXS)}`,
          "&-item": {
            backgroundColor: e.colorPrimary,
            borderRadius: "100%",
            width: 4,
            height: 4,
            animationName: Vn,
            animationDuration: "2s",
            animationIterationCount: "infinite",
            animationTimingFunction: "linear",
            "&:nth-child(1)": {
              animationDelay: "0s"
            },
            "&:nth-child(2)": {
              animationDelay: "0.2s"
            },
            "&:nth-child(3)": {
              animationDelay: "0.4s"
            }
          }
        }
      }
    }
  };
}, Gn = () => ({}), Ft = Rn("Bubble", (e) => {
  const t = Ue(e, {});
  return [Un(t), Nn(t), Fn(t), Xn(t)];
}, Gn), Xt = /* @__PURE__ */ p.createContext({}), Kn = (e, t) => {
  const {
    prefixCls: n,
    className: o,
    rootClassName: r,
    style: s,
    classNames: i = {},
    styles: a = {},
    avatar: l,
    placement: f = "start",
    loading: c = !1,
    loadingRender: u,
    typing: d,
    content: g = "",
    messageRender: b,
    variant: S = "filled",
    shape: m,
    onTypingComplete: y,
    header: C,
    footer: I,
    _key: h,
    ...E
  } = e, {
    onUpdate: v
  } = p.useContext(Xt), O = p.useRef(null);
  p.useImperativeHandle(t, () => ({
    nativeElement: O.current
  }));
  const {
    direction: P,
    getPrefixCls: R
  } = me(), T = R("bubble", n), k = Ur("bubble"), [x, j, L, D] = zn(d), [B, z] = Hn(g, x, j, L);
  p.useEffect(() => {
    v == null || v();
  }, [B]);
  const V = p.useRef(!1);
  p.useEffect(() => {
    !z && !c ? V.current || (V.current = !0, y == null || y()) : V.current = !1;
  }, [z, c]);
  const [K, ie, Z] = Ft(T), ae = q(T, r, k.className, o, ie, Z, `${T}-${f}`, {
    [`${T}-rtl`]: P === "rtl",
    [`${T}-typing`]: z && !c && !b && !D
  }), Ie = p.useMemo(() => /* @__PURE__ */ p.isValidElement(l) ? l : /* @__PURE__ */ p.createElement(tr, l), [l]), W = p.useMemo(() => b ? b(B) : B, [B, b]), G = (te) => typeof te == "function" ? te(B, {
    key: h
  }) : te;
  let ee;
  c ? ee = u ? u() : /* @__PURE__ */ p.createElement(An, {
    prefixCls: T
  }) : ee = /* @__PURE__ */ p.createElement(p.Fragment, null, W, z && D);
  let N = /* @__PURE__ */ p.createElement("div", {
    style: {
      ...k.styles.content,
      ...a.content
    },
    className: q(`${T}-content`, `${T}-content-${S}`, m && `${T}-content-${m}`, k.classNames.content, i.content)
  }, ee);
  return (C || I) && (N = /* @__PURE__ */ p.createElement("div", {
    className: `${T}-content-wrapper`
  }, C && /* @__PURE__ */ p.createElement("div", {
    className: q(`${T}-header`, k.classNames.header, i.header),
    style: {
      ...k.styles.header,
      ...a.header
    }
  }, G(C)), N, I && /* @__PURE__ */ p.createElement("div", {
    className: q(`${T}-footer`, k.classNames.footer, i.footer),
    style: {
      ...k.styles.footer,
      ...a.footer
    }
  }, G(I)))), K(/* @__PURE__ */ p.createElement("div", J({
    style: {
      ...k.style,
      ...s
    },
    className: ae
  }, E, {
    ref: O
  }), l && /* @__PURE__ */ p.createElement("div", {
    style: {
      ...k.styles.avatar,
      ...a.avatar
    },
    className: q(`${T}-avatar`, k.classNames.avatar, i.avatar)
  }, Ie), N));
}, Ge = /* @__PURE__ */ p.forwardRef(Kn);
function qn(e, t) {
  const n = w.useCallback((o, r) => typeof t == "function" ? t(o, r) : t ? t[o.role] || {} : {}, [t]);
  return w.useMemo(() => (e || []).map((o, r) => {
    const s = o.key ?? `preset_${r}`;
    return {
      ...n(o, r),
      ...o,
      key: s
    };
  }), [e, n]);
}
const Yn = ({
  _key: e,
  ...t
}, n) => /* @__PURE__ */ w.createElement(Ge, J({}, t, {
  ref: (o) => {
    var r;
    o ? n.current[e] = o : (r = n.current) == null || delete r[e];
  }
})), Qn = /* @__PURE__ */ w.memo(/* @__PURE__ */ w.forwardRef(Yn)), Jn = 1, Zn = (e, t) => {
  const {
    prefixCls: n,
    rootClassName: o,
    className: r,
    items: s,
    autoScroll: i = !0,
    roles: a,
    ...l
  } = e, f = Bn(l, {
    attr: !0,
    aria: !0
  }), c = w.useRef(null), u = w.useRef({}), {
    getPrefixCls: d
  } = me(), g = d("bubble", n), b = `${g}-list`, [S, m, y] = Ft(g), [C, I] = w.useState(!1);
  w.useEffect(() => (I(!0), () => {
    I(!1);
  }), []);
  const h = qn(s, a), [E, v] = w.useState(!0), [O, P] = w.useState(0), R = (x) => {
    const j = x.target;
    v(j.scrollHeight - Math.abs(j.scrollTop) - j.clientHeight <= Jn);
  };
  w.useEffect(() => {
    i && c.current && E && c.current.scrollTo({
      top: c.current.scrollHeight
    });
  }, [O]), w.useEffect(() => {
    var x;
    if (i) {
      const j = (x = h[h.length - 2]) == null ? void 0 : x.key, L = u.current[j];
      if (L) {
        const {
          nativeElement: D
        } = L, {
          top: B,
          bottom: z
        } = D.getBoundingClientRect(), {
          top: V,
          bottom: K
        } = c.current.getBoundingClientRect();
        B < K && z > V && (P((Z) => Z + 1), v(!0));
      }
    }
  }, [h.length]), w.useImperativeHandle(t, () => ({
    nativeElement: c.current,
    scrollTo: ({
      key: x,
      offset: j,
      behavior: L = "smooth",
      block: D
    }) => {
      if (typeof j == "number")
        c.current.scrollTo({
          top: j,
          behavior: L
        });
      else if (x !== void 0) {
        const B = u.current[x];
        if (B) {
          const z = h.findIndex((V) => V.key === x);
          v(z === h.length - 1), B.nativeElement.scrollIntoView({
            behavior: L,
            block: D
          });
        }
      }
    }
  }));
  const T = Gr(() => {
    i && P((x) => x + 1);
  }), k = w.useMemo(() => ({
    onUpdate: T
  }), []);
  return S(/* @__PURE__ */ w.createElement(Xt.Provider, {
    value: k
  }, /* @__PURE__ */ w.createElement("div", J({}, f, {
    className: q(b, o, r, m, y, {
      [`${b}-reach-end`]: E
    }),
    ref: c,
    onScroll: R
  }), h.map(({
    key: x,
    ...j
  }) => /* @__PURE__ */ w.createElement(Qn, J({}, j, {
    key: x,
    _key: x,
    ref: u,
    typing: C ? j.typing : !1
  }))))));
}, eo = /* @__PURE__ */ w.forwardRef(Zn);
Ge.List = eo;
const to = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function ro(e) {
  return e ? Object.keys(e).reduce((t, n) => {
    const o = e[n];
    return t[n] = no(n, o), t;
  }, {}) : {};
}
function no(e, t) {
  return typeof t == "number" && !to.includes(e) ? t + "px" : t;
}
function Xe(e) {
  const t = [], n = e.cloneNode(!1);
  if (e._reactElement) {
    const r = p.Children.toArray(e._reactElement.props.children).map((s) => {
      if (p.isValidElement(s) && s.props.__slot__) {
        const {
          portals: i,
          clonedElement: a
        } = Xe(s.props.el);
        return p.cloneElement(s, {
          ...s.props,
          el: a,
          children: [...p.Children.toArray(s.props.children), ...i]
        });
      }
      return null;
    });
    return r.originalChildren = e._reactElement.props.children, t.push(Be(p.cloneElement(e._reactElement, {
      ...e._reactElement.props,
      children: r
    }), n)), {
      clonedElement: n,
      portals: t
    };
  }
  Object.keys(e.getEventListeners()).forEach((r) => {
    e.getEventListeners(r).forEach(({
      listener: i,
      type: a,
      useCapture: l
    }) => {
      n.addEventListener(a, i, l);
    });
  });
  const o = Array.from(e.childNodes);
  for (let r = 0; r < o.length; r++) {
    const s = o[r];
    if (s.nodeType === 1) {
      const {
        clonedElement: i,
        portals: a
      } = Xe(s);
      t.push(...a), n.appendChild(i);
    } else s.nodeType === 3 && n.appendChild(s.cloneNode());
  }
  return {
    clonedElement: n,
    portals: t
  };
}
function oo(e, t) {
  e && (typeof e == "function" ? e(t) : e.current = t);
}
const xt = Ut(({
  slot: e,
  clone: t,
  className: n,
  style: o,
  observeAttributes: r
}, s) => {
  const i = wt(), [a, l] = Gt([]), {
    forceClone: f
  } = Zt(), c = f ? !0 : t;
  return Kt(() => {
    var S;
    if (!i.current || !e)
      return;
    let u = e;
    function d() {
      let m = u;
      if (u.tagName.toLowerCase() === "svelte-slot" && u.children.length === 1 && u.children[0] && (m = u.children[0], m.tagName.toLowerCase() === "react-portal-target" && m.children[0] && (m = m.children[0])), oo(s, m), n && m.classList.add(...n.split(" ")), o) {
        const y = ro(o);
        Object.keys(y).forEach((C) => {
          m.style[C] = y[C];
        });
      }
    }
    let g = null, b = null;
    if (c && window.MutationObserver) {
      let m = function() {
        var h, E, v;
        (h = i.current) != null && h.contains(u) && ((E = i.current) == null || E.removeChild(u));
        const {
          portals: C,
          clonedElement: I
        } = Xe(e);
        u = I, l(C), u.style.display = "contents", b && clearTimeout(b), b = setTimeout(() => {
          d();
        }, 50), (v = i.current) == null || v.appendChild(u);
      };
      m();
      const y = pr(() => {
        m(), g == null || g.disconnect(), g == null || g.observe(e, {
          childList: !0,
          subtree: !0,
          attributes: r
        });
      }, 50);
      g = new window.MutationObserver(y), g.observe(e, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      u.style.display = "contents", d(), (S = i.current) == null || S.appendChild(u);
    return () => {
      var m, y;
      u.style.display = "", (m = i.current) != null && m.contains(u) && ((y = i.current) == null || y.removeChild(u)), g == null || g.disconnect();
    };
  }, [e, c, n, o, s, r, f]), p.createElement("react-child", {
    ref: i,
    style: {
      display: "contents"
    }
  }, ...a);
});
function Ct(e) {
  const t = wt(e);
  return t.current = e, qt((...n) => {
    var o;
    return (o = t.current) == null ? void 0 : o.call(t, ...n);
  }, []);
}
const so = ({
  children: e,
  ...t
}) => /* @__PURE__ */ A.jsx(A.Fragment, {
  children: e(t)
});
function io(e) {
  return p.createElement(so, {
    children: e
  });
}
function Ke(e, t, n) {
  const o = e.filter(Boolean);
  if (o.length !== 0)
    return o.map((r, s) => {
      var f;
      if (typeof r != "object")
        return t != null && t.fallback ? t.fallback(r) : r;
      const i = {
        ...r.props,
        key: ((f = r.props) == null ? void 0 : f.key) ?? (n ? `${n}-${s}` : `${s}`)
      };
      let a = i;
      Object.keys(r.slots).forEach((c) => {
        if (!r.slots[c] || !(r.slots[c] instanceof Element) && !r.slots[c].el)
          return;
        const u = c.split(".");
        u.forEach((y, C) => {
          a[y] || (a[y] = {}), C !== u.length - 1 && (a = i[y]);
        });
        const d = r.slots[c];
        let g, b, S = (t == null ? void 0 : t.clone) ?? !1, m = t == null ? void 0 : t.forceClone;
        d instanceof Element ? g = d : (g = d.el, b = d.callback, S = d.clone ?? S, m = d.forceClone ?? m), m = m ?? !!b, a[u[u.length - 1]] = g ? b ? (...y) => (b(u[u.length - 1], y), /* @__PURE__ */ A.jsx(Je, {
          ...r.ctx,
          params: y,
          forceClone: m,
          children: /* @__PURE__ */ A.jsx(xt, {
            slot: g,
            clone: S
          })
        })) : io((y) => /* @__PURE__ */ A.jsx(Je, {
          ...r.ctx,
          forceClone: m,
          children: /* @__PURE__ */ A.jsx(xt, {
            ...y,
            slot: g,
            clone: S
          })
        })) : a[u[u.length - 1]], a = i;
      });
      const l = (t == null ? void 0 : t.children) || "children";
      return r[l] ? i[l] = Ke(r[l], t, `${s}`) : t != null && t.children && (i[l] = void 0, Reflect.deleteProperty(i, l)), i;
    });
}
const {
  useItems: ao,
  withItemsContextProvider: lo,
  ItemHandler: xo
} = _t("antdx-bubble.list-items"), {
  useItems: co,
  withItemsContextProvider: uo,
  ItemHandler: Co
} = _t("antdx-bubble.list-roles");
function fo(e) {
  return /^(?:async\s+)?(?:function\s*(?:\w*\s*)?\(|\([\w\s,=]*\)\s*=>|\(\{[\w\s,=]*\}\)\s*=>|function\s*\*\s*\w*\s*\()/i.test(e.trim());
}
function ho(e, t = !1) {
  try {
    if (Ne(e))
      return e;
    if (t && !fo(e))
      return;
    if (typeof e == "string") {
      let n = e.trim();
      return n.startsWith(";") && (n = n.slice(1)), n.endsWith(";") && (n = n.slice(0, -1)), new Function(`return (...args) => (${n})(...args)`)();
    }
    return;
  } catch {
    return;
  }
}
function go(e, t) {
  return ge(() => ho(e, t), [e, t]);
}
function mo(e, t) {
  return t((o, r) => Ne(o) ? r ? (...s) => Q(r) && r.unshift ? o(...e, ...s) : o(...s, ...e) : o(...e) : o);
}
const po = Symbol();
function bo(e, t) {
  return mo(t, (n) => {
    var o, r;
    return {
      ...e,
      avatar: Ne(e.avatar) ? n(e.avatar) : Q(e.avatar) ? {
        ...e.avatar,
        icon: n((o = e.avatar) == null ? void 0 : o.icon),
        src: n((r = e.avatar) == null ? void 0 : r.src)
      } : e.avatar,
      footer: n(e.footer, {
        unshift: !0
      }),
      header: n(e.header, {
        unshift: !0
      }),
      loadingRender: n(e.loadingRender, !0),
      messageRender: n(e.messageRender, !0)
    };
  });
}
function yo({
  roles: e,
  preProcess: t,
  postProcess: n
}, o = []) {
  const r = go(e), s = Ct(t), i = Ct(n), {
    items: {
      roles: a
    }
  } = co(), l = ge(() => {
    var c;
    return e || ((c = Ke(a, {
      clone: !0,
      forceClone: !0
    })) == null ? void 0 : c.reduce((u, d) => (d.role !== void 0 && (u[d.role] = d), u), {}));
  }, [a, e]), f = ge(() => (c, u) => {
    const d = u ?? c[po], g = s(c, d) || c;
    if (g.role && (l || {})[g.role])
      return bo((l || {})[g.role], [g, d]);
    let b;
    return b = i(g, d), b || {
      messageRender(S) {
        return /* @__PURE__ */ A.jsx(A.Fragment, {
          children: Q(S) ? JSON.stringify(S) : S
        });
      }
    };
  }, [l, i, s, ...o]);
  return r || f;
}
const wo = Xr(uo(["roles"], lo(["items", "default"], ({
  items: e,
  roles: t,
  children: n,
  ...o
}) => {
  const {
    items: r
  } = ao(), s = yo({
    roles: t
  }), i = r.items.length > 0 ? r.items : r.default;
  return /* @__PURE__ */ A.jsxs(A.Fragment, {
    children: [/* @__PURE__ */ A.jsx("div", {
      style: {
        display: "none"
      },
      children: n
    }), /* @__PURE__ */ A.jsx(Ge.List, {
      ...o,
      items: ge(() => e || Ke(i), [e, i]),
      roles: s
    })]
  });
})));
export {
  wo as BubbleList,
  wo as default
};
