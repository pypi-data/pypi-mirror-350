import { i as Kt, a as oe, r as qt, b as Qt, w as ee, g as Jt, c as We, d as Ct } from "./Index-CWLfznSN.js";
const V = window.ms_globals.React, w = window.ms_globals.React, St = window.ms_globals.React.forwardRef, xt = window.ms_globals.React.useRef, ze = window.ms_globals.React.useState, _t = window.ms_globals.React.useEffect, Gt = window.ms_globals.React.version, J = window.ms_globals.React.useMemo, Pe = window.ms_globals.ReactDOM.createPortal, Zt = window.ms_globals.internalContext.useContextPropsContext, Ge = window.ms_globals.internalContext.ContextPropsProvider, Yt = window.ms_globals.internalContext.SuggestionOpenContext, er = window.ms_globals.internalContext.SuggestionContext, tr = window.ms_globals.createItemsContext.createItemsContext, rr = window.ms_globals.antd.ConfigProvider, Ee = window.ms_globals.antd.theme, nr = window.ms_globals.antd.Cascader, or = window.ms_globals.antd.version, sr = window.ms_globals.antd.Flex, Ke = window.ms_globals.antdCssinjs.unit, Se = window.ms_globals.antdCssinjs.token2CSSVar, qe = window.ms_globals.antdCssinjs.useStyleRegister, ir = window.ms_globals.antdCssinjs.useCSSVarRegister, ar = window.ms_globals.antdCssinjs.createTheme, cr = window.ms_globals.antdCssinjs.useCacheToken;
var lr = /\s/;
function ur(t) {
  for (var e = t.length; e-- && lr.test(t.charAt(e)); )
    ;
  return e;
}
var fr = /^\s+/;
function hr(t) {
  return t && t.slice(0, ur(t) + 1).replace(fr, "");
}
var Qe = NaN, dr = /^[-+]0x[0-9a-f]+$/i, gr = /^0b[01]+$/i, pr = /^0o[0-7]+$/i, mr = parseInt;
function Je(t) {
  if (typeof t == "number")
    return t;
  if (Kt(t))
    return Qe;
  if (oe(t)) {
    var e = typeof t.valueOf == "function" ? t.valueOf() : t;
    t = oe(e) ? e + "" : e;
  }
  if (typeof t != "string")
    return t === 0 ? t : +t;
  t = hr(t);
  var n = gr.test(t);
  return n || pr.test(t) ? mr(t.slice(2), n ? 2 : 8) : dr.test(t) ? Qe : +t;
}
var xe = function() {
  return qt.Date.now();
}, br = "Expected a function", vr = Math.max, yr = Math.min;
function Sr(t, e, n) {
  var o, r, s, i, a, c, l = 0, h = !1, u = !1, d = !0;
  if (typeof t != "function")
    throw new TypeError(br);
  e = Je(e) || 0, oe(n) && (h = !!n.leading, u = "maxWait" in n, s = u ? vr(Je(n.maxWait) || 0, e) : s, d = "trailing" in n ? !!n.trailing : d);
  function f(S) {
    var T = o, C = r;
    return o = r = void 0, l = S, i = t.apply(C, T), i;
  }
  function b(S) {
    return l = S, a = setTimeout(p, e), h ? f(S) : i;
  }
  function m(S) {
    var T = S - c, C = S - l, P = e - T;
    return u ? yr(P, s - C) : P;
  }
  function g(S) {
    var T = S - c, C = S - l;
    return c === void 0 || T >= e || T < 0 || u && C >= s;
  }
  function p() {
    var S = xe();
    if (g(S))
      return y(S);
    a = setTimeout(p, m(S));
  }
  function y(S) {
    return a = void 0, d && o ? f(S) : (o = r = void 0, i);
  }
  function x() {
    a !== void 0 && clearTimeout(a), l = 0, o = c = r = a = void 0;
  }
  function v() {
    return a === void 0 ? i : y(xe());
  }
  function O() {
    var S = xe(), T = g(S);
    if (o = arguments, r = this, c = S, T) {
      if (a === void 0)
        return b(c);
      if (u)
        return clearTimeout(a), a = setTimeout(p, e), f(c);
    }
    return a === void 0 && (a = setTimeout(p, e)), i;
  }
  return O.cancel = x, O.flush = v, O;
}
function xr(t, e) {
  return Qt(t, e);
}
function Ze(t) {
  return t === void 0;
}
var wt = {
  exports: {}
}, ae = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var _r = w, Cr = Symbol.for("react.element"), wr = Symbol.for("react.fragment"), Or = Object.prototype.hasOwnProperty, Tr = _r.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, Mr = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function Ot(t, e, n) {
  var o, r = {}, s = null, i = null;
  n !== void 0 && (s = "" + n), e.key !== void 0 && (s = "" + e.key), e.ref !== void 0 && (i = e.ref);
  for (o in e) Or.call(e, o) && !Mr.hasOwnProperty(o) && (r[o] = e[o]);
  if (t && t.defaultProps) for (o in e = t.defaultProps, e) r[o] === void 0 && (r[o] = e[o]);
  return {
    $$typeof: Cr,
    type: t,
    key: s,
    ref: i,
    props: r,
    _owner: Tr.current
  };
}
ae.Fragment = wr;
ae.jsx = Ot;
ae.jsxs = Ot;
wt.exports = ae;
var A = wt.exports;
const {
  SvelteComponent: Pr,
  assign: Ye,
  binding_callbacks: et,
  check_outros: Er,
  children: Tt,
  claim_element: Mt,
  claim_space: Ir,
  component_subscribe: tt,
  compute_slots: kr,
  create_slot: jr,
  detach: G,
  element: Pt,
  empty: rt,
  exclude_internal_props: nt,
  get_all_dirty_from_scope: Rr,
  get_slot_changes: Lr,
  group_outros: Ar,
  init: Dr,
  insert_hydration: te,
  safe_not_equal: Hr,
  set_custom_element_data: Et,
  space: zr,
  transition_in: re,
  transition_out: Ie,
  update_slot_base: $r
} = window.__gradio__svelte__internal, {
  beforeUpdate: Br,
  getContext: Fr,
  onDestroy: Vr,
  setContext: Xr
} = window.__gradio__svelte__internal;
function ot(t) {
  let e, n;
  const o = (
    /*#slots*/
    t[7].default
  ), r = jr(
    o,
    t,
    /*$$scope*/
    t[6],
    null
  );
  return {
    c() {
      e = Pt("svelte-slot"), r && r.c(), this.h();
    },
    l(s) {
      e = Mt(s, "SVELTE-SLOT", {
        class: !0
      });
      var i = Tt(e);
      r && r.l(i), i.forEach(G), this.h();
    },
    h() {
      Et(e, "class", "svelte-1rt0kpf");
    },
    m(s, i) {
      te(s, e, i), r && r.m(e, null), t[9](e), n = !0;
    },
    p(s, i) {
      r && r.p && (!n || i & /*$$scope*/
      64) && $r(
        r,
        o,
        s,
        /*$$scope*/
        s[6],
        n ? Lr(
          o,
          /*$$scope*/
          s[6],
          i,
          null
        ) : Rr(
          /*$$scope*/
          s[6]
        ),
        null
      );
    },
    i(s) {
      n || (re(r, s), n = !0);
    },
    o(s) {
      Ie(r, s), n = !1;
    },
    d(s) {
      s && G(e), r && r.d(s), t[9](null);
    }
  };
}
function Nr(t) {
  let e, n, o, r, s = (
    /*$$slots*/
    t[4].default && ot(t)
  );
  return {
    c() {
      e = Pt("react-portal-target"), n = zr(), s && s.c(), o = rt(), this.h();
    },
    l(i) {
      e = Mt(i, "REACT-PORTAL-TARGET", {
        class: !0
      }), Tt(e).forEach(G), n = Ir(i), s && s.l(i), o = rt(), this.h();
    },
    h() {
      Et(e, "class", "svelte-1rt0kpf");
    },
    m(i, a) {
      te(i, e, a), t[8](e), te(i, n, a), s && s.m(i, a), te(i, o, a), r = !0;
    },
    p(i, [a]) {
      /*$$slots*/
      i[4].default ? s ? (s.p(i, a), a & /*$$slots*/
      16 && re(s, 1)) : (s = ot(i), s.c(), re(s, 1), s.m(o.parentNode, o)) : s && (Ar(), Ie(s, 1, 1, () => {
        s = null;
      }), Er());
    },
    i(i) {
      r || (re(s), r = !0);
    },
    o(i) {
      Ie(s), r = !1;
    },
    d(i) {
      i && (G(e), G(n), G(o)), t[8](null), s && s.d(i);
    }
  };
}
function st(t) {
  const {
    svelteInit: e,
    ...n
  } = t;
  return n;
}
function Ur(t, e, n) {
  let o, r, {
    $$slots: s = {},
    $$scope: i
  } = e;
  const a = kr(s);
  let {
    svelteInit: c
  } = e;
  const l = ee(st(e)), h = ee();
  tt(t, h, (v) => n(0, o = v));
  const u = ee();
  tt(t, u, (v) => n(1, r = v));
  const d = [], f = Fr("$$ms-gr-react-wrapper"), {
    slotKey: b,
    slotIndex: m,
    subSlotIndex: g
  } = Jt() || {}, p = c({
    parent: f,
    props: l,
    target: h,
    slot: u,
    slotKey: b,
    slotIndex: m,
    subSlotIndex: g,
    onDestroy(v) {
      d.push(v);
    }
  });
  Xr("$$ms-gr-react-wrapper", p), Br(() => {
    l.set(st(e));
  }), Vr(() => {
    d.forEach((v) => v());
  });
  function y(v) {
    et[v ? "unshift" : "push"](() => {
      o = v, h.set(o);
    });
  }
  function x(v) {
    et[v ? "unshift" : "push"](() => {
      r = v, u.set(r);
    });
  }
  return t.$$set = (v) => {
    n(17, e = Ye(Ye({}, e), nt(v))), "svelteInit" in v && n(5, c = v.svelteInit), "$$scope" in v && n(6, i = v.$$scope);
  }, e = nt(e), [o, r, h, u, a, c, i, s, y, x];
}
class Wr extends Pr {
  constructor(e) {
    super(), Dr(this, e, Ur, Nr, Hr, {
      svelteInit: 5
    });
  }
}
const {
  SvelteComponent: no
} = window.__gradio__svelte__internal, it = window.ms_globals.rerender, _e = window.ms_globals.tree;
function Gr(t, e = {}) {
  function n(o) {
    const r = ee(), s = new Wr({
      ...o,
      props: {
        svelteInit(i) {
          window.ms_globals.autokey += 1;
          const a = {
            key: window.ms_globals.autokey,
            svelteInstance: r,
            reactComponent: t,
            props: i.props,
            slot: i.slot,
            target: i.target,
            slotIndex: i.slotIndex,
            subSlotIndex: i.subSlotIndex,
            ignore: e.ignore,
            slotKey: i.slotKey,
            nodes: []
          }, c = i.parent ?? _e;
          return c.nodes = [...c.nodes, a], it({
            createPortal: Pe,
            node: _e
          }), i.onDestroy(() => {
            c.nodes = c.nodes.filter((l) => l.svelteInstance !== r), it({
              createPortal: Pe,
              node: _e
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
const Kr = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function qr(t) {
  return t ? Object.keys(t).reduce((e, n) => {
    const o = t[n];
    return e[n] = Qr(n, o), e;
  }, {}) : {};
}
function Qr(t, e) {
  return typeof e == "number" && !Kr.includes(t) ? e + "px" : e;
}
function ke(t) {
  const e = [], n = t.cloneNode(!1);
  if (t._reactElement) {
    const r = w.Children.toArray(t._reactElement.props.children).map((s) => {
      if (w.isValidElement(s) && s.props.__slot__) {
        const {
          portals: i,
          clonedElement: a
        } = ke(s.props.el);
        return w.cloneElement(s, {
          ...s.props,
          el: a,
          children: [...w.Children.toArray(s.props.children), ...i]
        });
      }
      return null;
    });
    return r.originalChildren = t._reactElement.props.children, e.push(Pe(w.cloneElement(t._reactElement, {
      ...t._reactElement.props,
      children: r
    }), n)), {
      clonedElement: n,
      portals: e
    };
  }
  Object.keys(t.getEventListeners()).forEach((r) => {
    t.getEventListeners(r).forEach(({
      listener: i,
      type: a,
      useCapture: c
    }) => {
      n.addEventListener(a, i, c);
    });
  });
  const o = Array.from(t.childNodes);
  for (let r = 0; r < o.length; r++) {
    const s = o[r];
    if (s.nodeType === 1) {
      const {
        clonedElement: i,
        portals: a
      } = ke(s);
      e.push(...a), n.appendChild(i);
    } else s.nodeType === 3 && n.appendChild(s.cloneNode());
  }
  return {
    clonedElement: n,
    portals: e
  };
}
function Jr(t, e) {
  t && (typeof t == "function" ? t(e) : t.current = e);
}
const je = St(({
  slot: t,
  clone: e,
  className: n,
  style: o,
  observeAttributes: r
}, s) => {
  const i = xt(), [a, c] = ze([]), {
    forceClone: l
  } = Zt(), h = l ? !0 : e;
  return _t(() => {
    var m;
    if (!i.current || !t)
      return;
    let u = t;
    function d() {
      let g = u;
      if (u.tagName.toLowerCase() === "svelte-slot" && u.children.length === 1 && u.children[0] && (g = u.children[0], g.tagName.toLowerCase() === "react-portal-target" && g.children[0] && (g = g.children[0])), Jr(s, g), n && g.classList.add(...n.split(" ")), o) {
        const p = qr(o);
        Object.keys(p).forEach((y) => {
          g.style[y] = p[y];
        });
      }
    }
    let f = null, b = null;
    if (h && window.MutationObserver) {
      let g = function() {
        var v, O, S;
        (v = i.current) != null && v.contains(u) && ((O = i.current) == null || O.removeChild(u));
        const {
          portals: y,
          clonedElement: x
        } = ke(t);
        u = x, c(y), u.style.display = "contents", b && clearTimeout(b), b = setTimeout(() => {
          d();
        }, 50), (S = i.current) == null || S.appendChild(u);
      };
      g();
      const p = Sr(() => {
        g(), f == null || f.disconnect(), f == null || f.observe(t, {
          childList: !0,
          subtree: !0,
          attributes: r
        });
      }, 50);
      f = new window.MutationObserver(p), f.observe(t, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      u.style.display = "contents", d(), (m = i.current) == null || m.appendChild(u);
    return () => {
      var g, p;
      u.style.display = "", (g = i.current) != null && g.contains(u) && ((p = i.current) == null || p.removeChild(u)), f == null || f.disconnect();
    };
  }, [t, h, n, o, s, r, l]), w.createElement("react-child", {
    ref: i,
    style: {
      display: "contents"
    }
  }, ...a);
}), Zr = "1.3.0", Yr = /* @__PURE__ */ w.createContext({}), en = {
  classNames: {},
  styles: {},
  className: "",
  style: {}
}, tn = (t) => {
  const e = w.useContext(Yr);
  return w.useMemo(() => ({
    ...en,
    ...e[t]
  }), [e[t]]);
};
function Re() {
  return Re = Object.assign ? Object.assign.bind() : function(t) {
    for (var e = 1; e < arguments.length; e++) {
      var n = arguments[e];
      for (var o in n) ({}).hasOwnProperty.call(n, o) && (t[o] = n[o]);
    }
    return t;
  }, Re.apply(null, arguments);
}
function Le() {
  const {
    getPrefixCls: t,
    direction: e,
    csp: n,
    iconPrefixCls: o,
    theme: r
  } = w.useContext(rr.ConfigContext);
  return {
    theme: r,
    getPrefixCls: t,
    direction: e,
    csp: n,
    iconPrefixCls: o
  };
}
function se(t) {
  var e = V.useRef();
  e.current = t;
  var n = V.useCallback(function() {
    for (var o, r = arguments.length, s = new Array(r), i = 0; i < r; i++)
      s[i] = arguments[i];
    return (o = e.current) === null || o === void 0 ? void 0 : o.call.apply(o, [e].concat(s));
  }, []);
  return n;
}
function rn(t) {
  if (Array.isArray(t)) return t;
}
function nn(t, e) {
  var n = t == null ? null : typeof Symbol < "u" && t[Symbol.iterator] || t["@@iterator"];
  if (n != null) {
    var o, r, s, i, a = [], c = !0, l = !1;
    try {
      if (s = (n = n.call(t)).next, e !== 0) for (; !(c = (o = s.call(n)).done) && (a.push(o.value), a.length !== e); c = !0) ;
    } catch (h) {
      l = !0, r = h;
    } finally {
      try {
        if (!c && n.return != null && (i = n.return(), Object(i) !== i)) return;
      } finally {
        if (l) throw r;
      }
    }
    return a;
  }
}
function at(t, e) {
  (e == null || e > t.length) && (e = t.length);
  for (var n = 0, o = Array(e); n < e; n++) o[n] = t[n];
  return o;
}
function on(t, e) {
  if (t) {
    if (typeof t == "string") return at(t, e);
    var n = {}.toString.call(t).slice(8, -1);
    return n === "Object" && t.constructor && (n = t.constructor.name), n === "Map" || n === "Set" ? Array.from(t) : n === "Arguments" || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n) ? at(t, e) : void 0;
  }
}
function sn() {
  throw new TypeError(`Invalid attempt to destructure non-iterable instance.
In order to be iterable, non-array objects must have a [Symbol.iterator]() method.`);
}
function Ae(t, e) {
  return rn(t) || nn(t, e) || on(t, e) || sn();
}
function an() {
  return !!(typeof window < "u" && window.document && window.document.createElement);
}
var ct = an() ? V.useLayoutEffect : V.useEffect, cn = function(e, n) {
  var o = V.useRef(!0);
  ct(function() {
    return e(o.current);
  }, n), ct(function() {
    return o.current = !1, function() {
      o.current = !0;
    };
  }, []);
}, lt = function(e, n) {
  cn(function(o) {
    if (!o)
      return e();
  }, n);
};
function ut(t) {
  var e = V.useRef(!1), n = V.useState(t), o = Ae(n, 2), r = o[0], s = o[1];
  V.useEffect(function() {
    return e.current = !1, function() {
      e.current = !0;
    };
  }, []);
  function i(a, c) {
    c && e.current || s(a);
  }
  return [r, i];
}
function Ce(t) {
  return t !== void 0;
}
function ln(t, e) {
  var n = e || {}, o = n.defaultValue, r = n.value, s = n.onChange, i = n.postState, a = ut(function() {
    return Ce(r) ? r : Ce(o) ? typeof o == "function" ? o() : o : t;
  }), c = Ae(a, 2), l = c[0], h = c[1], u = r !== void 0 ? r : l, d = i ? i(u) : u, f = se(s), b = ut([u]), m = Ae(b, 2), g = m[0], p = m[1];
  lt(function() {
    var x = g[0];
    l !== x && f(l, x);
  }, [g]), lt(function() {
    Ce(r) || h(r);
  }, [r]);
  var y = se(function(x, v) {
    h(x, v), p([u], v);
  });
  return [d, y];
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
var $e = Symbol.for("react.element"), Be = Symbol.for("react.portal"), ce = Symbol.for("react.fragment"), le = Symbol.for("react.strict_mode"), ue = Symbol.for("react.profiler"), fe = Symbol.for("react.provider"), he = Symbol.for("react.context"), un = Symbol.for("react.server_context"), de = Symbol.for("react.forward_ref"), ge = Symbol.for("react.suspense"), pe = Symbol.for("react.suspense_list"), me = Symbol.for("react.memo"), be = Symbol.for("react.lazy"), fn = Symbol.for("react.offscreen"), It;
It = Symbol.for("react.module.reference");
function H(t) {
  if (typeof t == "object" && t !== null) {
    var e = t.$$typeof;
    switch (e) {
      case $e:
        switch (t = t.type, t) {
          case ce:
          case ue:
          case le:
          case ge:
          case pe:
            return t;
          default:
            switch (t = t && t.$$typeof, t) {
              case un:
              case he:
              case de:
              case be:
              case me:
              case fe:
                return t;
              default:
                return e;
            }
        }
      case Be:
        return e;
    }
  }
}
_.ContextConsumer = he;
_.ContextProvider = fe;
_.Element = $e;
_.ForwardRef = de;
_.Fragment = ce;
_.Lazy = be;
_.Memo = me;
_.Portal = Be;
_.Profiler = ue;
_.StrictMode = le;
_.Suspense = ge;
_.SuspenseList = pe;
_.isAsyncMode = function() {
  return !1;
};
_.isConcurrentMode = function() {
  return !1;
};
_.isContextConsumer = function(t) {
  return H(t) === he;
};
_.isContextProvider = function(t) {
  return H(t) === fe;
};
_.isElement = function(t) {
  return typeof t == "object" && t !== null && t.$$typeof === $e;
};
_.isForwardRef = function(t) {
  return H(t) === de;
};
_.isFragment = function(t) {
  return H(t) === ce;
};
_.isLazy = function(t) {
  return H(t) === be;
};
_.isMemo = function(t) {
  return H(t) === me;
};
_.isPortal = function(t) {
  return H(t) === Be;
};
_.isProfiler = function(t) {
  return H(t) === ue;
};
_.isStrictMode = function(t) {
  return H(t) === le;
};
_.isSuspense = function(t) {
  return H(t) === ge;
};
_.isSuspenseList = function(t) {
  return H(t) === pe;
};
_.isValidElementType = function(t) {
  return typeof t == "string" || typeof t == "function" || t === ce || t === ue || t === le || t === ge || t === pe || t === fn || typeof t == "object" && t !== null && (t.$$typeof === be || t.$$typeof === me || t.$$typeof === fe || t.$$typeof === he || t.$$typeof === de || t.$$typeof === It || t.getModuleId !== void 0);
};
_.typeOf = H;
Number(Gt.split(".")[0]);
function z(t) {
  "@babel/helpers - typeof";
  return z = typeof Symbol == "function" && typeof Symbol.iterator == "symbol" ? function(e) {
    return typeof e;
  } : function(e) {
    return e && typeof Symbol == "function" && e.constructor === Symbol && e !== Symbol.prototype ? "symbol" : typeof e;
  }, z(t);
}
function hn(t, e) {
  if (z(t) != "object" || !t) return t;
  var n = t[Symbol.toPrimitive];
  if (n !== void 0) {
    var o = n.call(t, e);
    if (z(o) != "object") return o;
    throw new TypeError("@@toPrimitive must return a primitive value.");
  }
  return (e === "string" ? String : Number)(t);
}
function kt(t) {
  var e = hn(t, "string");
  return z(e) == "symbol" ? e : e + "";
}
function M(t, e, n) {
  return (e = kt(e)) in t ? Object.defineProperty(t, e, {
    value: n,
    enumerable: !0,
    configurable: !0,
    writable: !0
  }) : t[e] = n, t;
}
function ft(t, e) {
  var n = Object.keys(t);
  if (Object.getOwnPropertySymbols) {
    var o = Object.getOwnPropertySymbols(t);
    e && (o = o.filter(function(r) {
      return Object.getOwnPropertyDescriptor(t, r).enumerable;
    })), n.push.apply(n, o);
  }
  return n;
}
function L(t) {
  for (var e = 1; e < arguments.length; e++) {
    var n = arguments[e] != null ? arguments[e] : {};
    e % 2 ? ft(Object(n), !0).forEach(function(o) {
      M(t, o, n[o]);
    }) : Object.getOwnPropertyDescriptors ? Object.defineProperties(t, Object.getOwnPropertyDescriptors(n)) : ft(Object(n)).forEach(function(o) {
      Object.defineProperty(t, o, Object.getOwnPropertyDescriptor(n, o));
    });
  }
  return t;
}
function dn(t) {
  if (Array.isArray(t)) return t;
}
function gn(t, e) {
  var n = t == null ? null : typeof Symbol < "u" && t[Symbol.iterator] || t["@@iterator"];
  if (n != null) {
    var o, r, s, i, a = [], c = !0, l = !1;
    try {
      if (s = (n = n.call(t)).next, e === 0) {
        if (Object(n) !== n) return;
        c = !1;
      } else for (; !(c = (o = s.call(n)).done) && (a.push(o.value), a.length !== e); c = !0) ;
    } catch (h) {
      l = !0, r = h;
    } finally {
      try {
        if (!c && n.return != null && (i = n.return(), Object(i) !== i)) return;
      } finally {
        if (l) throw r;
      }
    }
    return a;
  }
}
function ht(t, e) {
  (e == null || e > t.length) && (e = t.length);
  for (var n = 0, o = Array(e); n < e; n++) o[n] = t[n];
  return o;
}
function pn(t, e) {
  if (t) {
    if (typeof t == "string") return ht(t, e);
    var n = {}.toString.call(t).slice(8, -1);
    return n === "Object" && t.constructor && (n = t.constructor.name), n === "Map" || n === "Set" ? Array.from(t) : n === "Arguments" || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n) ? ht(t, e) : void 0;
  }
}
function mn() {
  throw new TypeError(`Invalid attempt to destructure non-iterable instance.
In order to be iterable, non-array objects must have a [Symbol.iterator]() method.`);
}
function ne(t, e) {
  return dn(t) || gn(t, e) || pn(t, e) || mn();
}
function ve(t, e) {
  if (!(t instanceof e)) throw new TypeError("Cannot call a class as a function");
}
function bn(t, e) {
  for (var n = 0; n < e.length; n++) {
    var o = e[n];
    o.enumerable = o.enumerable || !1, o.configurable = !0, "value" in o && (o.writable = !0), Object.defineProperty(t, kt(o.key), o);
  }
}
function ye(t, e, n) {
  return e && bn(t.prototype, e), Object.defineProperty(t, "prototype", {
    writable: !1
  }), t;
}
function De(t, e) {
  return De = Object.setPrototypeOf ? Object.setPrototypeOf.bind() : function(n, o) {
    return n.__proto__ = o, n;
  }, De(t, e);
}
function jt(t, e) {
  if (typeof e != "function" && e !== null) throw new TypeError("Super expression must either be null or a function");
  t.prototype = Object.create(e && e.prototype, {
    constructor: {
      value: t,
      writable: !0,
      configurable: !0
    }
  }), Object.defineProperty(t, "prototype", {
    writable: !1
  }), e && De(t, e);
}
function ie(t) {
  return ie = Object.setPrototypeOf ? Object.getPrototypeOf.bind() : function(e) {
    return e.__proto__ || Object.getPrototypeOf(e);
  }, ie(t);
}
function Rt() {
  try {
    var t = !Boolean.prototype.valueOf.call(Reflect.construct(Boolean, [], function() {
    }));
  } catch {
  }
  return (Rt = function() {
    return !!t;
  })();
}
function Q(t) {
  if (t === void 0) throw new ReferenceError("this hasn't been initialised - super() hasn't been called");
  return t;
}
function vn(t, e) {
  if (e && (z(e) == "object" || typeof e == "function")) return e;
  if (e !== void 0) throw new TypeError("Derived constructors may only return object or undefined");
  return Q(t);
}
function Lt(t) {
  var e = Rt();
  return function() {
    var n, o = ie(t);
    if (e) {
      var r = ie(this).constructor;
      n = Reflect.construct(o, arguments, r);
    } else n = o.apply(this, arguments);
    return vn(this, n);
  };
}
var At = /* @__PURE__ */ ye(function t() {
  ve(this, t);
}), Dt = "CALC_UNIT", yn = new RegExp(Dt, "g");
function we(t) {
  return typeof t == "number" ? "".concat(t).concat(Dt) : t;
}
var Sn = /* @__PURE__ */ function(t) {
  jt(n, t);
  var e = Lt(n);
  function n(o, r) {
    var s;
    ve(this, n), s = e.call(this), M(Q(s), "result", ""), M(Q(s), "unitlessCssVar", void 0), M(Q(s), "lowPriority", void 0);
    var i = z(o);
    return s.unitlessCssVar = r, o instanceof n ? s.result = "(".concat(o.result, ")") : i === "number" ? s.result = we(o) : i === "string" && (s.result = o), s;
  }
  return ye(n, [{
    key: "add",
    value: function(r) {
      return r instanceof n ? this.result = "".concat(this.result, " + ").concat(r.getResult()) : (typeof r == "number" || typeof r == "string") && (this.result = "".concat(this.result, " + ").concat(we(r))), this.lowPriority = !0, this;
    }
  }, {
    key: "sub",
    value: function(r) {
      return r instanceof n ? this.result = "".concat(this.result, " - ").concat(r.getResult()) : (typeof r == "number" || typeof r == "string") && (this.result = "".concat(this.result, " - ").concat(we(r))), this.lowPriority = !0, this;
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
      var s = this, i = r || {}, a = i.unit, c = !0;
      return typeof a == "boolean" ? c = a : Array.from(this.unitlessCssVar).some(function(l) {
        return s.result.includes(l);
      }) && (c = !1), this.result = this.result.replace(yn, c ? "px" : ""), typeof this.lowPriority < "u" ? "calc(".concat(this.result, ")") : this.result;
    }
  }]), n;
}(At), xn = /* @__PURE__ */ function(t) {
  jt(n, t);
  var e = Lt(n);
  function n(o) {
    var r;
    return ve(this, n), r = e.call(this), M(Q(r), "result", 0), o instanceof n ? r.result = o.result : typeof o == "number" && (r.result = o), r;
  }
  return ye(n, [{
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
}(At), _n = function(e, n) {
  var o = e === "css" ? Sn : xn;
  return function(r) {
    return new o(r, n);
  };
}, dt = function(e, n) {
  return "".concat([n, e.replace(/([A-Z]+)([A-Z][a-z]+)/g, "$1-$2").replace(/([a-z])([A-Z])/g, "$1-$2")].filter(Boolean).join("-"));
};
function gt(t, e, n, o) {
  var r = L({}, e[t]);
  if (o != null && o.deprecatedTokens) {
    var s = o.deprecatedTokens;
    s.forEach(function(a) {
      var c = ne(a, 2), l = c[0], h = c[1];
      if (r != null && r[l] || r != null && r[h]) {
        var u;
        (u = r[h]) !== null && u !== void 0 || (r[h] = r == null ? void 0 : r[l]);
      }
    });
  }
  var i = L(L({}, n), r);
  return Object.keys(i).forEach(function(a) {
    i[a] === e[a] && delete i[a];
  }), i;
}
var Ht = typeof CSSINJS_STATISTIC < "u", He = !0;
function Fe() {
  for (var t = arguments.length, e = new Array(t), n = 0; n < t; n++)
    e[n] = arguments[n];
  if (!Ht)
    return Object.assign.apply(Object, [{}].concat(e));
  He = !1;
  var o = {};
  return e.forEach(function(r) {
    if (z(r) === "object") {
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
  }), He = !0, o;
}
var pt = {};
function Cn() {
}
var wn = function(e) {
  var n, o = e, r = Cn;
  return Ht && typeof Proxy < "u" && (n = /* @__PURE__ */ new Set(), o = new Proxy(e, {
    get: function(i, a) {
      if (He) {
        var c;
        (c = n) === null || c === void 0 || c.add(a);
      }
      return i[a];
    }
  }), r = function(i, a) {
    var c;
    pt[i] = {
      global: Array.from(n),
      component: L(L({}, (c = pt[i]) === null || c === void 0 ? void 0 : c.component), a)
    };
  }), {
    token: o,
    keys: n,
    flush: r
  };
};
function mt(t, e, n) {
  if (typeof n == "function") {
    var o;
    return n(Fe(e, (o = e[t]) !== null && o !== void 0 ? o : {}));
  }
  return n ?? {};
}
function On(t) {
  return t === "js" ? {
    max: Math.max,
    min: Math.min
  } : {
    max: function() {
      for (var n = arguments.length, o = new Array(n), r = 0; r < n; r++)
        o[r] = arguments[r];
      return "max(".concat(o.map(function(s) {
        return Ke(s);
      }).join(","), ")");
    },
    min: function() {
      for (var n = arguments.length, o = new Array(n), r = 0; r < n; r++)
        o[r] = arguments[r];
      return "min(".concat(o.map(function(s) {
        return Ke(s);
      }).join(","), ")");
    }
  };
}
var Tn = 1e3 * 60 * 10, Mn = /* @__PURE__ */ function() {
  function t() {
    ve(this, t), M(this, "map", /* @__PURE__ */ new Map()), M(this, "objectIDMap", /* @__PURE__ */ new WeakMap()), M(this, "nextID", 0), M(this, "lastAccessBeat", /* @__PURE__ */ new Map()), M(this, "accessBeat", 0);
  }
  return ye(t, [{
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
        return s && z(s) === "object" ? "obj_".concat(o.getObjectID(s)) : "".concat(z(s), "_").concat(s);
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
          o - r > Tn && (n.map.delete(s), n.lastAccessBeat.delete(s));
        }), this.accessBeat = 0;
      }
    }
  }]), t;
}(), bt = new Mn();
function Pn(t, e) {
  return w.useMemo(function() {
    var n = bt.get(e);
    if (n)
      return n;
    var o = t();
    return bt.set(e, o), o;
  }, e);
}
var En = function() {
  return {};
};
function In(t) {
  var e = t.useCSP, n = e === void 0 ? En : e, o = t.useToken, r = t.usePrefix, s = t.getResetStyles, i = t.getCommonStyle, a = t.getCompUnitless;
  function c(d, f, b, m) {
    var g = Array.isArray(d) ? d[0] : d;
    function p(C) {
      return "".concat(String(g)).concat(C.slice(0, 1).toUpperCase()).concat(C.slice(1));
    }
    var y = (m == null ? void 0 : m.unitless) || {}, x = typeof a == "function" ? a(d) : {}, v = L(L({}, x), {}, M({}, p("zIndexPopup"), !0));
    Object.keys(y).forEach(function(C) {
      v[p(C)] = y[C];
    });
    var O = L(L({}, m), {}, {
      unitless: v,
      prefixToken: p
    }), S = h(d, f, b, O), T = l(g, b, O);
    return function(C) {
      var P = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : C, j = S(C, P), $ = ne(j, 2), I = $[1], B = T(P), R = ne(B, 2), D = R[0], N = R[1];
      return [D, I, N];
    };
  }
  function l(d, f, b) {
    var m = b.unitless, g = b.injectStyle, p = g === void 0 ? !0 : g, y = b.prefixToken, x = b.ignore, v = function(T) {
      var C = T.rootCls, P = T.cssVar, j = P === void 0 ? {} : P, $ = o(), I = $.realToken;
      return ir({
        path: [d],
        prefix: j.prefix,
        key: j.key,
        unitless: m,
        ignore: x,
        token: I,
        scope: C
      }, function() {
        var B = mt(d, I, f), R = gt(d, I, B, {
          deprecatedTokens: b == null ? void 0 : b.deprecatedTokens
        });
        return Object.keys(B).forEach(function(D) {
          R[y(D)] = R[D], delete R[D];
        }), R;
      }), null;
    }, O = function(T) {
      var C = o(), P = C.cssVar;
      return [function(j) {
        return p && P ? /* @__PURE__ */ w.createElement(w.Fragment, null, /* @__PURE__ */ w.createElement(v, {
          rootCls: T,
          cssVar: P,
          component: d
        }), j) : j;
      }, P == null ? void 0 : P.key];
    };
    return O;
  }
  function h(d, f, b) {
    var m = arguments.length > 3 && arguments[3] !== void 0 ? arguments[3] : {}, g = Array.isArray(d) ? d : [d, d], p = ne(g, 1), y = p[0], x = g.join("-"), v = t.layer || {
      name: "antd"
    };
    return function(O) {
      var S = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : O, T = o(), C = T.theme, P = T.realToken, j = T.hashId, $ = T.token, I = T.cssVar, B = r(), R = B.rootPrefixCls, D = B.iconPrefixCls, N = n(), U = I ? "css" : "js", K = Pn(function() {
        var X = /* @__PURE__ */ new Set();
        return I && Object.keys(m.unitless || {}).forEach(function(Z) {
          X.add(Se(Z, I.prefix)), X.add(Se(Z, dt(y, I.prefix)));
        }), _n(U, X);
      }, [U, y, I == null ? void 0 : I.prefix]), E = On(U), Bt = E.max, Ft = E.min, Ve = {
        theme: C,
        token: $,
        hashId: j,
        nonce: function() {
          return N.nonce;
        },
        clientOnly: m.clientOnly,
        layer: v,
        // antd is always at top of styles
        order: m.order || -999
      };
      typeof s == "function" && qe(L(L({}, Ve), {}, {
        clientOnly: !1,
        path: ["Shared", R]
      }), function() {
        return s($, {
          prefix: {
            rootPrefixCls: R,
            iconPrefixCls: D
          },
          csp: N
        });
      });
      var Vt = qe(L(L({}, Ve), {}, {
        path: [x, O, D]
      }), function() {
        if (m.injectStyle === !1)
          return [];
        var X = wn($), Z = X.token, Xt = X.flush, W = mt(y, P, b), Nt = ".".concat(O), Xe = gt(y, P, W, {
          deprecatedTokens: m.deprecatedTokens
        });
        I && W && z(W) === "object" && Object.keys(W).forEach(function(Ue) {
          W[Ue] = "var(".concat(Se(Ue, dt(y, I.prefix)), ")");
        });
        var Ne = Fe(Z, {
          componentCls: Nt,
          prefixCls: O,
          iconCls: ".".concat(D),
          antCls: ".".concat(R),
          calc: K,
          // @ts-ignore
          max: Bt,
          // @ts-ignore
          min: Ft
        }, I ? W : Xe), Ut = f(Ne, {
          hashId: j,
          prefixCls: O,
          rootPrefixCls: R,
          iconPrefixCls: D
        });
        Xt(y, Xe);
        var Wt = typeof i == "function" ? i(Ne, O, S, m.resetFont) : null;
        return [m.resetStyle === !1 ? null : Wt, Ut];
      });
      return [Vt, j];
    };
  }
  function u(d, f, b) {
    var m = arguments.length > 3 && arguments[3] !== void 0 ? arguments[3] : {}, g = h(d, f, b, L({
      resetStyle: !1,
      // Sub Style should default after root one
      order: -998
    }, m)), p = function(x) {
      var v = x.prefixCls, O = x.rootCls, S = O === void 0 ? v : O;
      return g(v, S), null;
    };
    return p;
  }
  return {
    genStyleHooks: c,
    genSubStyleComponent: u,
    genComponentStyleHook: h
  };
}
const k = Math.round;
function Oe(t, e) {
  const n = t.replace(/^[^(]*\((.*)/, "$1").replace(/\).*/, "").match(/\d*\.?\d+%?/g) || [], o = n.map((r) => parseFloat(r));
  for (let r = 0; r < 3; r += 1)
    o[r] = e(o[r] || 0, n[r] || "", r);
  return n[3] ? o[3] = n[3].includes("%") ? o[3] / 100 : o[3] : o[3] = 1, o;
}
const vt = (t, e, n) => n === 0 ? t : t / 100;
function q(t, e) {
  const n = e || 255;
  return t > n ? n : t < 0 ? 0 : t;
}
class F {
  constructor(e) {
    M(this, "isValid", !0), M(this, "r", 0), M(this, "g", 0), M(this, "b", 0), M(this, "a", 1), M(this, "_h", void 0), M(this, "_s", void 0), M(this, "_l", void 0), M(this, "_v", void 0), M(this, "_max", void 0), M(this, "_min", void 0), M(this, "_brightness", void 0);
    function n(o) {
      return o[0] in e && o[1] in e && o[2] in e;
    }
    if (e) if (typeof e == "string") {
      let r = function(s) {
        return o.startsWith(s);
      };
      const o = e.trim();
      /^#?[A-F\d]{3,8}$/i.test(o) ? this.fromHexString(o) : r("rgb") ? this.fromRgbString(o) : r("hsl") ? this.fromHslString(o) : (r("hsv") || r("hsb")) && this.fromHsvString(o);
    } else if (e instanceof F)
      this.r = e.r, this.g = e.g, this.b = e.b, this.a = e.a, this._h = e._h, this._s = e._s, this._l = e._l, this._v = e._v;
    else if (n("rgb"))
      this.r = q(e.r), this.g = q(e.g), this.b = q(e.b), this.a = typeof e.a == "number" ? q(e.a, 1) : 1;
    else if (n("hsl"))
      this.fromHsl(e);
    else if (n("hsv"))
      this.fromHsv(e);
    else
      throw new Error("@ant-design/fast-color: unsupported input " + JSON.stringify(e));
  }
  // ======================= Setter =======================
  setR(e) {
    return this._sc("r", e);
  }
  setG(e) {
    return this._sc("g", e);
  }
  setB(e) {
    return this._sc("b", e);
  }
  setA(e) {
    return this._sc("a", e, 1);
  }
  setHue(e) {
    const n = this.toHsv();
    return n.h = e, this._c(n);
  }
  // ======================= Getter =======================
  /**
   * Returns the perceived luminance of a color, from 0-1.
   * @see http://www.w3.org/TR/2008/REC-WCAG20-20081211/#relativeluminancedef
   */
  getLuminance() {
    function e(s) {
      const i = s / 255;
      return i <= 0.03928 ? i / 12.92 : Math.pow((i + 0.055) / 1.055, 2.4);
    }
    const n = e(this.r), o = e(this.g), r = e(this.b);
    return 0.2126 * n + 0.7152 * o + 0.0722 * r;
  }
  getHue() {
    if (typeof this._h > "u") {
      const e = this.getMax() - this.getMin();
      e === 0 ? this._h = 0 : this._h = k(60 * (this.r === this.getMax() ? (this.g - this.b) / e + (this.g < this.b ? 6 : 0) : this.g === this.getMax() ? (this.b - this.r) / e + 2 : (this.r - this.g) / e + 4));
    }
    return this._h;
  }
  getSaturation() {
    if (typeof this._s > "u") {
      const e = this.getMax() - this.getMin();
      e === 0 ? this._s = 0 : this._s = e / this.getMax();
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
  darken(e = 10) {
    const n = this.getHue(), o = this.getSaturation();
    let r = this.getLightness() - e / 100;
    return r < 0 && (r = 0), this._c({
      h: n,
      s: o,
      l: r,
      a: this.a
    });
  }
  lighten(e = 10) {
    const n = this.getHue(), o = this.getSaturation();
    let r = this.getLightness() + e / 100;
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
  mix(e, n = 50) {
    const o = this._c(e), r = n / 100, s = (a) => (o[a] - this[a]) * r + this[a], i = {
      r: k(s("r")),
      g: k(s("g")),
      b: k(s("b")),
      a: k(s("a") * 100) / 100
    };
    return this._c(i);
  }
  /**
   * Mix the color with pure white, from 0 to 100.
   * Providing 0 will do nothing, providing 100 will always return white.
   */
  tint(e = 10) {
    return this.mix({
      r: 255,
      g: 255,
      b: 255,
      a: 1
    }, e);
  }
  /**
   * Mix the color with pure black, from 0 to 100.
   * Providing 0 will do nothing, providing 100 will always return black.
   */
  shade(e = 10) {
    return this.mix({
      r: 0,
      g: 0,
      b: 0,
      a: 1
    }, e);
  }
  onBackground(e) {
    const n = this._c(e), o = this.a + n.a * (1 - this.a), r = (s) => k((this[s] * this.a + n[s] * n.a * (1 - this.a)) / o);
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
  equals(e) {
    return this.r === e.r && this.g === e.g && this.b === e.b && this.a === e.a;
  }
  clone() {
    return this._c(this);
  }
  // ======================= Format =======================
  toHexString() {
    let e = "#";
    const n = (this.r || 0).toString(16);
    e += n.length === 2 ? n : "0" + n;
    const o = (this.g || 0).toString(16);
    e += o.length === 2 ? o : "0" + o;
    const r = (this.b || 0).toString(16);
    if (e += r.length === 2 ? r : "0" + r, typeof this.a == "number" && this.a >= 0 && this.a < 1) {
      const s = k(this.a * 255).toString(16);
      e += s.length === 2 ? s : "0" + s;
    }
    return e;
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
    const e = this.getHue(), n = k(this.getSaturation() * 100), o = k(this.getLightness() * 100);
    return this.a !== 1 ? `hsla(${e},${n}%,${o}%,${this.a})` : `hsl(${e},${n}%,${o}%)`;
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
  _sc(e, n, o) {
    const r = this.clone();
    return r[e] = q(n, o), r;
  }
  _c(e) {
    return new this.constructor(e);
  }
  getMax() {
    return typeof this._max > "u" && (this._max = Math.max(this.r, this.g, this.b)), this._max;
  }
  getMin() {
    return typeof this._min > "u" && (this._min = Math.min(this.r, this.g, this.b)), this._min;
  }
  fromHexString(e) {
    const n = e.replace("#", "");
    function o(r, s) {
      return parseInt(n[r] + n[s || r], 16);
    }
    n.length < 6 ? (this.r = o(0), this.g = o(1), this.b = o(2), this.a = n[3] ? o(3) / 255 : 1) : (this.r = o(0, 1), this.g = o(2, 3), this.b = o(4, 5), this.a = n[6] ? o(6, 7) / 255 : 1);
  }
  fromHsl({
    h: e,
    s: n,
    l: o,
    a: r
  }) {
    if (this._h = e % 360, this._s = n, this._l = o, this.a = typeof r == "number" ? r : 1, n <= 0) {
      const d = k(o * 255);
      this.r = d, this.g = d, this.b = d;
    }
    let s = 0, i = 0, a = 0;
    const c = e / 60, l = (1 - Math.abs(2 * o - 1)) * n, h = l * (1 - Math.abs(c % 2 - 1));
    c >= 0 && c < 1 ? (s = l, i = h) : c >= 1 && c < 2 ? (s = h, i = l) : c >= 2 && c < 3 ? (i = l, a = h) : c >= 3 && c < 4 ? (i = h, a = l) : c >= 4 && c < 5 ? (s = h, a = l) : c >= 5 && c < 6 && (s = l, a = h);
    const u = o - l / 2;
    this.r = k((s + u) * 255), this.g = k((i + u) * 255), this.b = k((a + u) * 255);
  }
  fromHsv({
    h: e,
    s: n,
    v: o,
    a: r
  }) {
    this._h = e % 360, this._s = n, this._v = o, this.a = typeof r == "number" ? r : 1;
    const s = k(o * 255);
    if (this.r = s, this.g = s, this.b = s, n <= 0)
      return;
    const i = e / 60, a = Math.floor(i), c = i - a, l = k(o * (1 - n) * 255), h = k(o * (1 - n * c) * 255), u = k(o * (1 - n * (1 - c)) * 255);
    switch (a) {
      case 0:
        this.g = u, this.b = l;
        break;
      case 1:
        this.r = h, this.b = l;
        break;
      case 2:
        this.r = l, this.b = u;
        break;
      case 3:
        this.r = l, this.g = h;
        break;
      case 4:
        this.r = u, this.g = l;
        break;
      case 5:
      default:
        this.g = l, this.b = h;
        break;
    }
  }
  fromHsvString(e) {
    const n = Oe(e, vt);
    this.fromHsv({
      h: n[0],
      s: n[1],
      v: n[2],
      a: n[3]
    });
  }
  fromHslString(e) {
    const n = Oe(e, vt);
    this.fromHsl({
      h: n[0],
      s: n[1],
      l: n[2],
      a: n[3]
    });
  }
  fromRgbString(e) {
    const n = Oe(e, (o, r) => (
      // Convert percentage to number. e.g. 50% -> 128
      r.includes("%") ? k(o / 100 * 255) : o
    ));
    this.r = n[0], this.g = n[1], this.b = n[2], this.a = n[3];
  }
}
const kn = {
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
}, jn = Object.assign(Object.assign({}, kn), {
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
function Te(t) {
  return t >= 0 && t <= 255;
}
function Y(t, e) {
  const {
    r: n,
    g: o,
    b: r,
    a: s
  } = new F(t).toRgb();
  if (s < 1)
    return t;
  const {
    r: i,
    g: a,
    b: c
  } = new F(e).toRgb();
  for (let l = 0.01; l <= 1; l += 0.01) {
    const h = Math.round((n - i * (1 - l)) / l), u = Math.round((o - a * (1 - l)) / l), d = Math.round((r - c * (1 - l)) / l);
    if (Te(h) && Te(u) && Te(d))
      return new F({
        r: h,
        g: u,
        b: d,
        a: Math.round(l * 100) / 100
      }).toRgbString();
  }
  return new F({
    r: n,
    g: o,
    b: r,
    a: 1
  }).toRgbString();
}
var Rn = function(t, e) {
  var n = {};
  for (var o in t) Object.prototype.hasOwnProperty.call(t, o) && e.indexOf(o) < 0 && (n[o] = t[o]);
  if (t != null && typeof Object.getOwnPropertySymbols == "function") for (var r = 0, o = Object.getOwnPropertySymbols(t); r < o.length; r++)
    e.indexOf(o[r]) < 0 && Object.prototype.propertyIsEnumerable.call(t, o[r]) && (n[o[r]] = t[o[r]]);
  return n;
};
function Ln(t) {
  const {
    override: e
  } = t, n = Rn(t, ["override"]), o = Object.assign({}, e);
  Object.keys(jn).forEach((d) => {
    delete o[d];
  });
  const r = Object.assign(Object.assign({}, n), o), s = 480, i = 576, a = 768, c = 992, l = 1200, h = 1600;
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
    colorSplit: Y(r.colorBorderSecondary, r.colorBgContainer),
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
    colorErrorOutline: Y(r.colorErrorBg, r.colorBgContainer),
    colorWarningOutline: Y(r.colorWarningBg, r.colorBgContainer),
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
    controlOutline: Y(r.colorPrimaryBg, r.colorBgContainer),
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
    screenMDMax: c - 1,
    screenLG: c,
    screenLGMin: c,
    screenLGMax: l - 1,
    screenXL: l,
    screenXLMin: l,
    screenXLMax: h - 1,
    screenXXL: h,
    screenXXLMin: h,
    boxShadowPopoverArrow: "2px 2px 5px rgba(0, 0, 0, 0.05)",
    boxShadowCard: `
      0 1px 2px -2px ${new F("rgba(0, 0, 0, 0.16)").toRgbString()},
      0 3px 6px 0 ${new F("rgba(0, 0, 0, 0.12)").toRgbString()},
      0 5px 12px 4px ${new F("rgba(0, 0, 0, 0.09)").toRgbString()}
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
const An = {
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
}, Dn = {
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
}, Hn = ar(Ee.defaultAlgorithm), zn = {
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
}, zt = (t, e, n) => {
  const o = n.getDerivativeToken(t), {
    override: r,
    ...s
  } = e;
  let i = {
    ...o,
    override: r
  };
  return i = Ln(i), s && Object.entries(s).forEach(([a, c]) => {
    const {
      theme: l,
      ...h
    } = c;
    let u = h;
    l && (u = zt({
      ...i,
      ...h
    }, {
      override: h
    }, l)), i[a] = u;
  }), i;
};
function $n() {
  const {
    token: t,
    hashed: e,
    theme: n = Hn,
    override: o,
    cssVar: r
  } = w.useContext(Ee._internalContext), [s, i, a] = cr(n, [Ee.defaultSeed, t], {
    salt: `${Zr}-${e || ""}`,
    override: o,
    getComputedToken: zt,
    cssVar: r && {
      prefix: r.prefix,
      key: r.key,
      unitless: An,
      ignore: Dn,
      preserve: zn
    }
  });
  return [n, a, e ? i : "", s, r];
}
const {
  genStyleHooks: Bn
} = In({
  usePrefix: () => {
    const {
      getPrefixCls: t,
      iconPrefixCls: e
    } = Le();
    return {
      iconPrefixCls: e,
      rootPrefixCls: t()
    };
  },
  useToken: () => {
    const [t, e, n, o, r] = $n();
    return {
      theme: t,
      realToken: e,
      hashId: n,
      token: o,
      cssVar: r
    };
  },
  useCSP: () => {
    const {
      csp: t
    } = Le();
    return t ?? {};
  },
  layer: {
    name: "antdx",
    dependencies: ["antd"]
  }
}), Fn = (t) => {
  const {
    componentCls: e,
    antCls: n
  } = t;
  return {
    [e]: {
      [`${n}-cascader-menus ${n}-cascader-menu`]: {
        height: "auto"
      },
      [`${e}-item`]: {
        "&-icon": {
          marginInlineEnd: t.paddingXXS
        },
        "&-extra": {
          marginInlineStart: t.padding
        }
      },
      [`&${e}-block`]: {
        [`${e}-item-extra`]: {
          marginInlineStart: "auto"
        }
      }
    }
  };
}, Vn = () => ({}), Xn = Bn("Suggestion", (t) => {
  const e = Fe(t, {});
  return Fn(e);
}, Vn);
function Nn(t, e, n, o, r) {
  const [s, i] = w.useState([]), a = (f, b = s) => {
    let m = t;
    for (let g = 0; g < f - 1; g += 1) {
      const p = b[g], y = m.find((x) => x.value === p);
      if (!y)
        break;
      m = y.children || [];
    }
    return m;
  }, c = (f) => f.map((b, m) => {
    const p = a(m + 1, f).find((y) => y.value === b);
    return p == null ? void 0 : p.value;
  }), l = (f) => {
    const b = s.length || 1, m = a(b), g = m.findIndex((x) => x.value === s[b - 1]), p = m.length, y = m[(g + f + p) % p];
    i([...s.slice(0, b - 1), y.value]);
  }, h = () => {
    s.length > 1 && i(s.slice(0, s.length - 1));
  }, u = () => {
    const f = a(s.length + 1);
    f.length && i([...s, f[0].value]);
  }, d = se((f) => {
    if (e)
      switch (f.key) {
        case "ArrowDown":
          l(1), f.preventDefault();
          break;
        case "ArrowUp":
          l(-1), f.preventDefault();
          break;
        case "ArrowRight":
          n ? h() : u(), f.preventDefault();
          break;
        case "ArrowLeft":
          n ? u() : h(), f.preventDefault();
          break;
        case "Enter":
          a(s.length + 1).length || o(c(s)), f.preventDefault();
          break;
        case "Escape":
          r(), f.preventDefault();
          break;
      }
  });
  return w.useEffect(() => {
    e && i([t[0].value]);
  }, [e]), [s, d];
}
const Me = or.split(".").map(Number), Un = Me[0] > 5 || Me[0] === 5 && Me[1] >= 25;
function Wn(t) {
  const {
    prefixCls: e,
    className: n,
    rootClassName: o,
    style: r,
    children: s,
    open: i,
    onOpenChange: a,
    items: c,
    onSelect: l,
    block: h
  } = t, {
    direction: u,
    getPrefixCls: d
  } = Le(), f = d("suggestion", e), b = `${f}-item`, m = u === "rtl", g = tn("suggestion"), [p, y, x] = Xn(f), [v, O] = ln(!1, {
    value: i
  }), [S, T] = ze(), C = (E) => {
    O(E), a == null || a(E);
  }, P = se((E) => {
    E === !1 ? C(!1) : (T(E), C(!0));
  }), j = () => {
    C(!1);
  }, $ = w.useMemo(() => typeof c == "function" ? c(S) : c, [c, S]), I = (E) => /* @__PURE__ */ w.createElement(sr, {
    className: b
  }, E.icon && /* @__PURE__ */ w.createElement("div", {
    className: `${b}-icon`
  }, E.icon), E.label, E.extra && /* @__PURE__ */ w.createElement("div", {
    className: `${b}-extra`
  }, E.extra)), B = (E) => {
    l && l(E[E.length - 1]), C(!1);
  }, [R, D] = Nn($, v, m, B, j), N = s == null ? void 0 : s({
    onTrigger: P,
    onKeyDown: D
  }), U = (E) => {
    E || j();
  }, K = {};
  return Un ? K.onOpenChange = U : K.onDropdownVisibleChange = U, p(/* @__PURE__ */ w.createElement(nr, Re({
    options: $,
    open: v,
    value: R,
    placement: m ? "topRight" : "topLeft"
  }, K, {
    optionRender: I,
    rootClassName: We(o, f, y, x, {
      [`${f}-block`]: h
    }),
    onChange: B,
    dropdownMatchSelectWidth: h
  }), /* @__PURE__ */ w.createElement("div", {
    className: We(f, g.className, o, n, `${f}-wrapper`, y, x),
    style: {
      ...g.style,
      ...r
    }
  }, N)));
}
function Gn(t) {
  return /^(?:async\s+)?(?:function\s*(?:\w*\s*)?\(|\([\w\s,=]*\)\s*=>|\(\{[\w\s,=]*\}\)\s*=>|function\s*\*\s*\w*\s*\()/i.test(t.trim());
}
function Kn(t, e = !1) {
  try {
    if (Ct(t))
      return t;
    if (e && !Gn(t))
      return;
    if (typeof t == "string") {
      let n = t.trim();
      return n.startsWith(";") && (n = n.slice(1)), n.endsWith(";") && (n = n.slice(0, -1)), new Function(`return (...args) => (${n})(...args)`)();
    }
    return;
  } catch {
    return;
  }
}
function yt(t, e) {
  return J(() => Kn(t, e), [t, e]);
}
function qn(t) {
  const e = xt();
  return J(() => xr(t, e.current) ? e.current : (e.current = t, t), [t]);
}
function Qn(t, e) {
  return e((o, r) => Ct(o) ? r ? (...s) => oe(r) && r.unshift ? o(...t, ...s) : o(...s, ...t) : o(...t) : o);
}
const Jn = ({
  children: t,
  ...e
}) => /* @__PURE__ */ A.jsx(A.Fragment, {
  children: t(e)
});
function Zn(t) {
  return w.createElement(Jn, {
    children: t
  });
}
function $t(t, e, n) {
  const o = t.filter(Boolean);
  if (o.length !== 0)
    return o.map((r, s) => {
      var l;
      if (typeof r != "object")
        return e != null && e.fallback ? e.fallback(r) : r;
      const i = {
        ...r.props,
        key: ((l = r.props) == null ? void 0 : l.key) ?? (n ? `${n}-${s}` : `${s}`)
      };
      let a = i;
      Object.keys(r.slots).forEach((h) => {
        if (!r.slots[h] || !(r.slots[h] instanceof Element) && !r.slots[h].el)
          return;
        const u = h.split(".");
        u.forEach((p, y) => {
          a[p] || (a[p] = {}), y !== u.length - 1 && (a = i[p]);
        });
        const d = r.slots[h];
        let f, b, m = (e == null ? void 0 : e.clone) ?? !1, g = e == null ? void 0 : e.forceClone;
        d instanceof Element ? f = d : (f = d.el, b = d.callback, m = d.clone ?? m, g = d.forceClone ?? g), g = g ?? !!b, a[u[u.length - 1]] = f ? b ? (...p) => (b(u[u.length - 1], p), /* @__PURE__ */ A.jsx(Ge, {
          ...r.ctx,
          params: p,
          forceClone: g,
          children: /* @__PURE__ */ A.jsx(je, {
            slot: f,
            clone: m
          })
        })) : Zn((p) => /* @__PURE__ */ A.jsx(Ge, {
          ...r.ctx,
          forceClone: g,
          children: /* @__PURE__ */ A.jsx(je, {
            ...p,
            slot: f,
            clone: m
          })
        })) : a[u[u.length - 1]], a = i;
      });
      const c = (e == null ? void 0 : e.children) || "children";
      return r[c] ? i[c] = $t(r[c], e, `${s}`) : e != null && e.children && (i[c] = void 0, Reflect.deleteProperty(i, c)), i;
    });
}
const {
  useItems: Yn,
  withItemsContextProvider: eo,
  ItemHandler: oo
} = tr("antdx-suggestion-chain-items"), to = St(({
  children: t,
  props: e,
  shouldTrigger: n
}, o) => {
  const r = qn(e);
  return /* @__PURE__ */ A.jsx(er.Provider, {
    value: J(() => ({
      ...r,
      onKeyDown: (s) => {
        var i;
        n ? requestAnimationFrame(() => {
          n(s, {
            onTrigger: r.onTrigger,
            onKeyDown: r.onKeyDown
          });
        }) : (i = r.onKeyDown) == null || i.call(r, s);
      },
      elRef: o
    }), [r, n, o]),
    children: t
  });
}), so = Gr(eo(["default", "items"], ({
  children: t,
  items: e,
  shouldTrigger: n,
  slots: o,
  ...r
}) => {
  const [s, i] = ze(() => r.open ?? !1), {
    items: a
  } = Yn(), c = a.items.length > 0 ? a.items : a.default, l = yt(e), h = yt(n), u = J(() => e || $t(c, {
    clone: !0
  }) || [{}], [e, c]), d = J(() => (...f) => u.map((b) => Qn(f, (m) => {
    const g = (p) => {
      var y;
      return {
        ...p,
        extra: m(p.extra),
        icon: m(p.icon),
        label: m(p.label),
        children: (y = p.children) == null ? void 0 : y.map((x) => g(x))
      };
    };
    return g(b);
  })), [u]);
  return _t(() => {
    Ze(r.open) || i(r.open);
  }, [r.open]), /* @__PURE__ */ A.jsx(A.Fragment, {
    children: /* @__PURE__ */ A.jsx(Wn, {
      ...r,
      items: l || d,
      onOpenChange: (f, ...b) => {
        var m;
        Ze(r.open) && i(f), (m = r.onOpenChange) == null || m.call(r, f, ...b);
      },
      children: (f) => /* @__PURE__ */ A.jsx(Yt.Provider, {
        value: s,
        children: /* @__PURE__ */ A.jsxs(to, {
          props: f,
          shouldTrigger: h,
          children: [/* @__PURE__ */ A.jsx("div", {
            style: {
              display: "none"
            },
            children: t
          }), o.children ? /* @__PURE__ */ A.jsx(je, {
            slot: o.children
          }) : null]
        })
      })
    })
  });
}));
export {
  so as Suggestion,
  so as default
};
