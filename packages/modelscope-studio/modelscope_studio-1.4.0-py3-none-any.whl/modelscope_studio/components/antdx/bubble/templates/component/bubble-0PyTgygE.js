import { i as Gt, a as me, r as Kt, w as fe, g as qt, c as Y, b as Yt } from "./Index-DU2yGUUr.js";
const C = window.ms_globals.React, g = window.ms_globals.React, Xt = window.ms_globals.React.forwardRef, Nt = window.ms_globals.React.useRef, Vt = window.ms_globals.React.useState, Wt = window.ms_globals.React.useEffect, Ut = window.ms_globals.React.version, xt = window.ms_globals.React.useMemo, He = window.ms_globals.ReactDOM.createPortal, Qt = window.ms_globals.internalContext.useContextPropsContext, Jt = window.ms_globals.internalContext.ContextPropsProvider, Zt = window.ms_globals.antd.ConfigProvider, ze = window.ms_globals.antd.theme, er = window.ms_globals.antd.Avatar, oe = window.ms_globals.antdCssinjs.unit, Ie = window.ms_globals.antdCssinjs.token2CSSVar, Qe = window.ms_globals.antdCssinjs.useStyleRegister, tr = window.ms_globals.antdCssinjs.useCSSVarRegister, rr = window.ms_globals.antdCssinjs.createTheme, nr = window.ms_globals.antdCssinjs.useCacheToken, Ct = window.ms_globals.antdCssinjs.Keyframes;
var or = /\s/;
function ir(t) {
  for (var e = t.length; e-- && or.test(t.charAt(e)); )
    ;
  return e;
}
var sr = /^\s+/;
function ar(t) {
  return t && t.slice(0, ir(t) + 1).replace(sr, "");
}
var Je = NaN, cr = /^[-+]0x[0-9a-f]+$/i, lr = /^0b[01]+$/i, ur = /^0o[0-7]+$/i, fr = parseInt;
function Ze(t) {
  if (typeof t == "number")
    return t;
  if (Gt(t))
    return Je;
  if (me(t)) {
    var e = typeof t.valueOf == "function" ? t.valueOf() : t;
    t = me(e) ? e + "" : e;
  }
  if (typeof t != "string")
    return t === 0 ? t : +t;
  t = ar(t);
  var r = lr.test(t);
  return r || ur.test(t) ? fr(t.slice(2), r ? 2 : 8) : cr.test(t) ? Je : +t;
}
var ke = function() {
  return Kt.Date.now();
}, dr = "Expected a function", hr = Math.max, gr = Math.min;
function mr(t, e, r) {
  var o, n, i, s, a, c, l = 0, u = !1, f = !1, d = !0;
  if (typeof t != "function")
    throw new TypeError(dr);
  e = Ze(e) || 0, me(r) && (u = !!r.leading, f = "maxWait" in r, i = f ? hr(Ze(r.maxWait) || 0, e) : i, d = "trailing" in r ? !!r.trailing : d);
  function y(m) {
    var P = o, O = n;
    return o = n = void 0, l = m, s = t.apply(O, P), s;
  }
  function v(m) {
    return l = m, a = setTimeout(S, e), u ? y(m) : s;
  }
  function _(m) {
    var P = m - c, O = m - l, j = e - P;
    return f ? gr(j, i - O) : j;
  }
  function p(m) {
    var P = m - c, O = m - l;
    return c === void 0 || P >= e || P < 0 || f && O >= i;
  }
  function S() {
    var m = ke();
    if (p(m))
      return x(m);
    a = setTimeout(S, _(m));
  }
  function x(m) {
    return a = void 0, d && o ? y(m) : (o = n = void 0, s);
  }
  function R() {
    a !== void 0 && clearTimeout(a), l = 0, o = c = n = a = void 0;
  }
  function h() {
    return a === void 0 ? s : x(ke());
  }
  function E() {
    var m = ke(), P = p(m);
    if (o = arguments, n = this, c = m, P) {
      if (a === void 0)
        return v(c);
      if (f)
        return clearTimeout(a), a = setTimeout(S, e), y(c);
    }
    return a === void 0 && (a = setTimeout(S, e)), s;
  }
  return E.cancel = R, E.flush = h, E;
}
var wt = {
  exports: {}
}, ye = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var pr = g, br = Symbol.for("react.element"), yr = Symbol.for("react.fragment"), vr = Object.prototype.hasOwnProperty, Sr = pr.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, xr = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function _t(t, e, r) {
  var o, n = {}, i = null, s = null;
  r !== void 0 && (i = "" + r), e.key !== void 0 && (i = "" + e.key), e.ref !== void 0 && (s = e.ref);
  for (o in e) vr.call(e, o) && !xr.hasOwnProperty(o) && (n[o] = e[o]);
  if (t && t.defaultProps) for (o in e = t.defaultProps, e) n[o] === void 0 && (n[o] = e[o]);
  return {
    $$typeof: br,
    type: t,
    key: i,
    ref: s,
    props: n,
    _owner: Sr.current
  };
}
ye.Fragment = yr;
ye.jsx = _t;
ye.jsxs = _t;
wt.exports = ye;
var $ = wt.exports;
const {
  SvelteComponent: Cr,
  assign: et,
  binding_callbacks: tt,
  check_outros: wr,
  children: Tt,
  claim_element: Et,
  claim_space: _r,
  component_subscribe: rt,
  compute_slots: Tr,
  create_slot: Er,
  detach: Q,
  element: Pt,
  empty: nt,
  exclude_internal_props: ot,
  get_all_dirty_from_scope: Pr,
  get_slot_changes: Or,
  group_outros: Mr,
  init: Rr,
  insert_hydration: de,
  safe_not_equal: jr,
  set_custom_element_data: Ot,
  space: Ir,
  transition_in: he,
  transition_out: Ae,
  update_slot_base: kr
} = window.__gradio__svelte__internal, {
  beforeUpdate: Lr,
  getContext: $r,
  onDestroy: Dr,
  setContext: Br
} = window.__gradio__svelte__internal;
function it(t) {
  let e, r;
  const o = (
    /*#slots*/
    t[7].default
  ), n = Er(
    o,
    t,
    /*$$scope*/
    t[6],
    null
  );
  return {
    c() {
      e = Pt("svelte-slot"), n && n.c(), this.h();
    },
    l(i) {
      e = Et(i, "SVELTE-SLOT", {
        class: !0
      });
      var s = Tt(e);
      n && n.l(s), s.forEach(Q), this.h();
    },
    h() {
      Ot(e, "class", "svelte-1rt0kpf");
    },
    m(i, s) {
      de(i, e, s), n && n.m(e, null), t[9](e), r = !0;
    },
    p(i, s) {
      n && n.p && (!r || s & /*$$scope*/
      64) && kr(
        n,
        o,
        i,
        /*$$scope*/
        i[6],
        r ? Or(
          o,
          /*$$scope*/
          i[6],
          s,
          null
        ) : Pr(
          /*$$scope*/
          i[6]
        ),
        null
      );
    },
    i(i) {
      r || (he(n, i), r = !0);
    },
    o(i) {
      Ae(n, i), r = !1;
    },
    d(i) {
      i && Q(e), n && n.d(i), t[9](null);
    }
  };
}
function Hr(t) {
  let e, r, o, n, i = (
    /*$$slots*/
    t[4].default && it(t)
  );
  return {
    c() {
      e = Pt("react-portal-target"), r = Ir(), i && i.c(), o = nt(), this.h();
    },
    l(s) {
      e = Et(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), Tt(e).forEach(Q), r = _r(s), i && i.l(s), o = nt(), this.h();
    },
    h() {
      Ot(e, "class", "svelte-1rt0kpf");
    },
    m(s, a) {
      de(s, e, a), t[8](e), de(s, r, a), i && i.m(s, a), de(s, o, a), n = !0;
    },
    p(s, [a]) {
      /*$$slots*/
      s[4].default ? i ? (i.p(s, a), a & /*$$slots*/
      16 && he(i, 1)) : (i = it(s), i.c(), he(i, 1), i.m(o.parentNode, o)) : i && (Mr(), Ae(i, 1, 1, () => {
        i = null;
      }), wr());
    },
    i(s) {
      n || (he(i), n = !0);
    },
    o(s) {
      Ae(i), n = !1;
    },
    d(s) {
      s && (Q(e), Q(r), Q(o)), t[8](null), i && i.d(s);
    }
  };
}
function st(t) {
  const {
    svelteInit: e,
    ...r
  } = t;
  return r;
}
function zr(t, e, r) {
  let o, n, {
    $$slots: i = {},
    $$scope: s
  } = e;
  const a = Tr(i);
  let {
    svelteInit: c
  } = e;
  const l = fe(st(e)), u = fe();
  rt(t, u, (h) => r(0, o = h));
  const f = fe();
  rt(t, f, (h) => r(1, n = h));
  const d = [], y = $r("$$ms-gr-react-wrapper"), {
    slotKey: v,
    slotIndex: _,
    subSlotIndex: p
  } = qt() || {}, S = c({
    parent: y,
    props: l,
    target: u,
    slot: f,
    slotKey: v,
    slotIndex: _,
    subSlotIndex: p,
    onDestroy(h) {
      d.push(h);
    }
  });
  Br("$$ms-gr-react-wrapper", S), Lr(() => {
    l.set(st(e));
  }), Dr(() => {
    d.forEach((h) => h());
  });
  function x(h) {
    tt[h ? "unshift" : "push"](() => {
      o = h, u.set(o);
    });
  }
  function R(h) {
    tt[h ? "unshift" : "push"](() => {
      n = h, f.set(n);
    });
  }
  return t.$$set = (h) => {
    r(17, e = et(et({}, e), ot(h))), "svelteInit" in h && r(5, c = h.svelteInit), "$$scope" in h && r(6, s = h.$$scope);
  }, e = ot(e), [o, n, u, f, a, c, s, i, x, R];
}
class Ar extends Cr {
  constructor(e) {
    super(), Rr(this, e, zr, Hr, jr, {
      svelteInit: 5
    });
  }
}
const {
  SvelteComponent: lo
} = window.__gradio__svelte__internal, at = window.ms_globals.rerender, Le = window.ms_globals.tree;
function Fr(t, e = {}) {
  function r(o) {
    const n = fe(), i = new Ar({
      ...o,
      props: {
        svelteInit(s) {
          window.ms_globals.autokey += 1;
          const a = {
            key: window.ms_globals.autokey,
            svelteInstance: n,
            reactComponent: t,
            props: s.props,
            slot: s.slot,
            target: s.target,
            slotIndex: s.slotIndex,
            subSlotIndex: s.subSlotIndex,
            ignore: e.ignore,
            slotKey: s.slotKey,
            nodes: []
          }, c = s.parent ?? Le;
          return c.nodes = [...c.nodes, a], at({
            createPortal: He,
            node: Le
          }), s.onDestroy(() => {
            c.nodes = c.nodes.filter((l) => l.svelteInstance !== n), at({
              createPortal: He,
              node: Le
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
const Xr = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Nr(t) {
  return t ? Object.keys(t).reduce((e, r) => {
    const o = t[r];
    return e[r] = Vr(r, o), e;
  }, {}) : {};
}
function Vr(t, e) {
  return typeof e == "number" && !Xr.includes(t) ? e + "px" : e;
}
function Fe(t) {
  const e = [], r = t.cloneNode(!1);
  if (t._reactElement) {
    const n = g.Children.toArray(t._reactElement.props.children).map((i) => {
      if (g.isValidElement(i) && i.props.__slot__) {
        const {
          portals: s,
          clonedElement: a
        } = Fe(i.props.el);
        return g.cloneElement(i, {
          ...i.props,
          el: a,
          children: [...g.Children.toArray(i.props.children), ...s]
        });
      }
      return null;
    });
    return n.originalChildren = t._reactElement.props.children, e.push(He(g.cloneElement(t._reactElement, {
      ...t._reactElement.props,
      children: n
    }), r)), {
      clonedElement: r,
      portals: e
    };
  }
  Object.keys(t.getEventListeners()).forEach((n) => {
    t.getEventListeners(n).forEach(({
      listener: s,
      type: a,
      useCapture: c
    }) => {
      r.addEventListener(a, s, c);
    });
  });
  const o = Array.from(t.childNodes);
  for (let n = 0; n < o.length; n++) {
    const i = o[n];
    if (i.nodeType === 1) {
      const {
        clonedElement: s,
        portals: a
      } = Fe(i);
      e.push(...a), r.appendChild(s);
    } else i.nodeType === 3 && r.appendChild(i.cloneNode());
  }
  return {
    clonedElement: r,
    portals: e
  };
}
function Wr(t, e) {
  t && (typeof t == "function" ? t(e) : t.current = e);
}
const U = Xt(({
  slot: t,
  clone: e,
  className: r,
  style: o,
  observeAttributes: n
}, i) => {
  const s = Nt(), [a, c] = Vt([]), {
    forceClone: l
  } = Qt(), u = l ? !0 : e;
  return Wt(() => {
    var _;
    if (!s.current || !t)
      return;
    let f = t;
    function d() {
      let p = f;
      if (f.tagName.toLowerCase() === "svelte-slot" && f.children.length === 1 && f.children[0] && (p = f.children[0], p.tagName.toLowerCase() === "react-portal-target" && p.children[0] && (p = p.children[0])), Wr(i, p), r && p.classList.add(...r.split(" ")), o) {
        const S = Nr(o);
        Object.keys(S).forEach((x) => {
          p.style[x] = S[x];
        });
      }
    }
    let y = null, v = null;
    if (u && window.MutationObserver) {
      let p = function() {
        var h, E, m;
        (h = s.current) != null && h.contains(f) && ((E = s.current) == null || E.removeChild(f));
        const {
          portals: x,
          clonedElement: R
        } = Fe(t);
        f = R, c(x), f.style.display = "contents", v && clearTimeout(v), v = setTimeout(() => {
          d();
        }, 50), (m = s.current) == null || m.appendChild(f);
      };
      p();
      const S = mr(() => {
        p(), y == null || y.disconnect(), y == null || y.observe(t, {
          childList: !0,
          subtree: !0,
          attributes: n
        });
      }, 50);
      y = new window.MutationObserver(S), y.observe(t, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      f.style.display = "contents", d(), (_ = s.current) == null || _.appendChild(f);
    return () => {
      var p, S;
      f.style.display = "", (p = s.current) != null && p.contains(f) && ((S = s.current) == null || S.removeChild(f)), y == null || y.disconnect();
    };
  }, [t, u, r, o, i, n, l]), g.createElement("react-child", {
    ref: s,
    style: {
      display: "contents"
    }
  }, ...a);
}), Ur = "1.3.0", Gr = /* @__PURE__ */ g.createContext({}), Kr = {
  classNames: {},
  styles: {},
  className: "",
  style: {}
}, qr = (t) => {
  const e = g.useContext(Gr);
  return g.useMemo(() => ({
    ...Kr,
    ...e[t]
  }), [e[t]]);
};
function J() {
  return J = Object.assign ? Object.assign.bind() : function(t) {
    for (var e = 1; e < arguments.length; e++) {
      var r = arguments[e];
      for (var o in r) ({}).hasOwnProperty.call(r, o) && (t[o] = r[o]);
    }
    return t;
  }, J.apply(null, arguments);
}
function pe() {
  const {
    getPrefixCls: t,
    direction: e,
    csp: r,
    iconPrefixCls: o,
    theme: n
  } = g.useContext(Zt.ConfigContext);
  return {
    theme: n,
    getPrefixCls: t,
    direction: e,
    csp: r,
    iconPrefixCls: o
  };
}
function Yr(t) {
  var e = C.useRef();
  e.current = t;
  var r = C.useCallback(function() {
    for (var o, n = arguments.length, i = new Array(n), s = 0; s < n; s++)
      i[s] = arguments[s];
    return (o = e.current) === null || o === void 0 ? void 0 : o.call.apply(o, [e].concat(i));
  }, []);
  return r;
}
function Qr() {
  return !!(typeof window < "u" && window.document && window.document.createElement);
}
var ct = Qr() ? C.useLayoutEffect : C.useEffect, Jr = function(e, r) {
  var o = C.useRef(!0);
  ct(function() {
    return e(o.current);
  }, r), ct(function() {
    return o.current = !1, function() {
      o.current = !0;
    };
  }, []);
};
function ie(t) {
  "@babel/helpers - typeof";
  return ie = typeof Symbol == "function" && typeof Symbol.iterator == "symbol" ? function(e) {
    return typeof e;
  } : function(e) {
    return e && typeof Symbol == "function" && e.constructor === Symbol && e !== Symbol.prototype ? "symbol" : typeof e;
  }, ie(t);
}
var w = {};
/**
 * @license React
 * react-is.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var Ve = Symbol.for("react.element"), We = Symbol.for("react.portal"), ve = Symbol.for("react.fragment"), Se = Symbol.for("react.strict_mode"), xe = Symbol.for("react.profiler"), Ce = Symbol.for("react.provider"), we = Symbol.for("react.context"), Zr = Symbol.for("react.server_context"), _e = Symbol.for("react.forward_ref"), Te = Symbol.for("react.suspense"), Ee = Symbol.for("react.suspense_list"), Pe = Symbol.for("react.memo"), Oe = Symbol.for("react.lazy"), en = Symbol.for("react.offscreen"), Mt;
Mt = Symbol.for("react.module.reference");
function F(t) {
  if (typeof t == "object" && t !== null) {
    var e = t.$$typeof;
    switch (e) {
      case Ve:
        switch (t = t.type, t) {
          case ve:
          case xe:
          case Se:
          case Te:
          case Ee:
            return t;
          default:
            switch (t = t && t.$$typeof, t) {
              case Zr:
              case we:
              case _e:
              case Oe:
              case Pe:
              case Ce:
                return t;
              default:
                return e;
            }
        }
      case We:
        return e;
    }
  }
}
w.ContextConsumer = we;
w.ContextProvider = Ce;
w.Element = Ve;
w.ForwardRef = _e;
w.Fragment = ve;
w.Lazy = Oe;
w.Memo = Pe;
w.Portal = We;
w.Profiler = xe;
w.StrictMode = Se;
w.Suspense = Te;
w.SuspenseList = Ee;
w.isAsyncMode = function() {
  return !1;
};
w.isConcurrentMode = function() {
  return !1;
};
w.isContextConsumer = function(t) {
  return F(t) === we;
};
w.isContextProvider = function(t) {
  return F(t) === Ce;
};
w.isElement = function(t) {
  return typeof t == "object" && t !== null && t.$$typeof === Ve;
};
w.isForwardRef = function(t) {
  return F(t) === _e;
};
w.isFragment = function(t) {
  return F(t) === ve;
};
w.isLazy = function(t) {
  return F(t) === Oe;
};
w.isMemo = function(t) {
  return F(t) === Pe;
};
w.isPortal = function(t) {
  return F(t) === We;
};
w.isProfiler = function(t) {
  return F(t) === xe;
};
w.isStrictMode = function(t) {
  return F(t) === Se;
};
w.isSuspense = function(t) {
  return F(t) === Te;
};
w.isSuspenseList = function(t) {
  return F(t) === Ee;
};
w.isValidElementType = function(t) {
  return typeof t == "string" || typeof t == "function" || t === ve || t === xe || t === Se || t === Te || t === Ee || t === en || typeof t == "object" && t !== null && (t.$$typeof === Oe || t.$$typeof === Pe || t.$$typeof === Ce || t.$$typeof === we || t.$$typeof === _e || t.$$typeof === Mt || t.getModuleId !== void 0);
};
w.typeOf = F;
Number(Ut.split(".")[0]);
function tn(t, e) {
  if (ie(t) != "object" || !t) return t;
  var r = t[Symbol.toPrimitive];
  if (r !== void 0) {
    var o = r.call(t, e);
    if (ie(o) != "object") return o;
    throw new TypeError("@@toPrimitive must return a primitive value.");
  }
  return (e === "string" ? String : Number)(t);
}
function rn(t) {
  var e = tn(t, "string");
  return ie(e) == "symbol" ? e : e + "";
}
function nn(t, e, r) {
  return (e = rn(e)) in t ? Object.defineProperty(t, e, {
    value: r,
    enumerable: !0,
    configurable: !0,
    writable: !0
  }) : t[e] = r, t;
}
function lt(t, e) {
  var r = Object.keys(t);
  if (Object.getOwnPropertySymbols) {
    var o = Object.getOwnPropertySymbols(t);
    e && (o = o.filter(function(n) {
      return Object.getOwnPropertyDescriptor(t, n).enumerable;
    })), r.push.apply(r, o);
  }
  return r;
}
function on(t) {
  for (var e = 1; e < arguments.length; e++) {
    var r = arguments[e] != null ? arguments[e] : {};
    e % 2 ? lt(Object(r), !0).forEach(function(o) {
      nn(t, o, r[o]);
    }) : Object.getOwnPropertyDescriptors ? Object.defineProperties(t, Object.getOwnPropertyDescriptors(r)) : lt(Object(r)).forEach(function(o) {
      Object.defineProperty(t, o, Object.getOwnPropertyDescriptor(r, o));
    });
  }
  return t;
}
function X(t) {
  "@babel/helpers - typeof";
  return X = typeof Symbol == "function" && typeof Symbol.iterator == "symbol" ? function(e) {
    return typeof e;
  } : function(e) {
    return e && typeof Symbol == "function" && e.constructor === Symbol && e !== Symbol.prototype ? "symbol" : typeof e;
  }, X(t);
}
function sn(t, e) {
  if (X(t) != "object" || !t) return t;
  var r = t[Symbol.toPrimitive];
  if (r !== void 0) {
    var o = r.call(t, e);
    if (X(o) != "object") return o;
    throw new TypeError("@@toPrimitive must return a primitive value.");
  }
  return (e === "string" ? String : Number)(t);
}
function Rt(t) {
  var e = sn(t, "string");
  return X(e) == "symbol" ? e : e + "";
}
function M(t, e, r) {
  return (e = Rt(e)) in t ? Object.defineProperty(t, e, {
    value: r,
    enumerable: !0,
    configurable: !0,
    writable: !0
  }) : t[e] = r, t;
}
function ut(t, e) {
  var r = Object.keys(t);
  if (Object.getOwnPropertySymbols) {
    var o = Object.getOwnPropertySymbols(t);
    e && (o = o.filter(function(n) {
      return Object.getOwnPropertyDescriptor(t, n).enumerable;
    })), r.push.apply(r, o);
  }
  return r;
}
function z(t) {
  for (var e = 1; e < arguments.length; e++) {
    var r = arguments[e] != null ? arguments[e] : {};
    e % 2 ? ut(Object(r), !0).forEach(function(o) {
      M(t, o, r[o]);
    }) : Object.getOwnPropertyDescriptors ? Object.defineProperties(t, Object.getOwnPropertyDescriptors(r)) : ut(Object(r)).forEach(function(o) {
      Object.defineProperty(t, o, Object.getOwnPropertyDescriptor(r, o));
    });
  }
  return t;
}
function an(t) {
  if (Array.isArray(t)) return t;
}
function cn(t, e) {
  var r = t == null ? null : typeof Symbol < "u" && t[Symbol.iterator] || t["@@iterator"];
  if (r != null) {
    var o, n, i, s, a = [], c = !0, l = !1;
    try {
      if (i = (r = r.call(t)).next, e === 0) {
        if (Object(r) !== r) return;
        c = !1;
      } else for (; !(c = (o = i.call(r)).done) && (a.push(o.value), a.length !== e); c = !0) ;
    } catch (u) {
      l = !0, n = u;
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
function ft(t, e) {
  (e == null || e > t.length) && (e = t.length);
  for (var r = 0, o = Array(e); r < e; r++) o[r] = t[r];
  return o;
}
function ln(t, e) {
  if (t) {
    if (typeof t == "string") return ft(t, e);
    var r = {}.toString.call(t).slice(8, -1);
    return r === "Object" && t.constructor && (r = t.constructor.name), r === "Map" || r === "Set" ? Array.from(t) : r === "Arguments" || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r) ? ft(t, e) : void 0;
  }
}
function un() {
  throw new TypeError(`Invalid attempt to destructure non-iterable instance.
In order to be iterable, non-array objects must have a [Symbol.iterator]() method.`);
}
function ge(t, e) {
  return an(t) || cn(t, e) || ln(t, e) || un();
}
function Me(t, e) {
  if (!(t instanceof e)) throw new TypeError("Cannot call a class as a function");
}
function fn(t, e) {
  for (var r = 0; r < e.length; r++) {
    var o = e[r];
    o.enumerable = o.enumerable || !1, o.configurable = !0, "value" in o && (o.writable = !0), Object.defineProperty(t, Rt(o.key), o);
  }
}
function Re(t, e, r) {
  return e && fn(t.prototype, e), Object.defineProperty(t, "prototype", {
    writable: !1
  }), t;
}
function Xe(t, e) {
  return Xe = Object.setPrototypeOf ? Object.setPrototypeOf.bind() : function(r, o) {
    return r.__proto__ = o, r;
  }, Xe(t, e);
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
  }), e && Xe(t, e);
}
function be(t) {
  return be = Object.setPrototypeOf ? Object.getPrototypeOf.bind() : function(e) {
    return e.__proto__ || Object.getPrototypeOf(e);
  }, be(t);
}
function It() {
  try {
    var t = !Boolean.prototype.valueOf.call(Reflect.construct(Boolean, [], function() {
    }));
  } catch {
  }
  return (It = function() {
    return !!t;
  })();
}
function ne(t) {
  if (t === void 0) throw new ReferenceError("this hasn't been initialised - super() hasn't been called");
  return t;
}
function dn(t, e) {
  if (e && (X(e) == "object" || typeof e == "function")) return e;
  if (e !== void 0) throw new TypeError("Derived constructors may only return object or undefined");
  return ne(t);
}
function kt(t) {
  var e = It();
  return function() {
    var r, o = be(t);
    if (e) {
      var n = be(this).constructor;
      r = Reflect.construct(o, arguments, n);
    } else r = o.apply(this, arguments);
    return dn(this, r);
  };
}
var Lt = /* @__PURE__ */ Re(function t() {
  Me(this, t);
}), $t = "CALC_UNIT", hn = new RegExp($t, "g");
function $e(t) {
  return typeof t == "number" ? "".concat(t).concat($t) : t;
}
var gn = /* @__PURE__ */ function(t) {
  jt(r, t);
  var e = kt(r);
  function r(o, n) {
    var i;
    Me(this, r), i = e.call(this), M(ne(i), "result", ""), M(ne(i), "unitlessCssVar", void 0), M(ne(i), "lowPriority", void 0);
    var s = X(o);
    return i.unitlessCssVar = n, o instanceof r ? i.result = "(".concat(o.result, ")") : s === "number" ? i.result = $e(o) : s === "string" && (i.result = o), i;
  }
  return Re(r, [{
    key: "add",
    value: function(n) {
      return n instanceof r ? this.result = "".concat(this.result, " + ").concat(n.getResult()) : (typeof n == "number" || typeof n == "string") && (this.result = "".concat(this.result, " + ").concat($e(n))), this.lowPriority = !0, this;
    }
  }, {
    key: "sub",
    value: function(n) {
      return n instanceof r ? this.result = "".concat(this.result, " - ").concat(n.getResult()) : (typeof n == "number" || typeof n == "string") && (this.result = "".concat(this.result, " - ").concat($e(n))), this.lowPriority = !0, this;
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
      }) && (c = !1), this.result = this.result.replace(hn, c ? "px" : ""), typeof this.lowPriority < "u" ? "calc(".concat(this.result, ")") : this.result;
    }
  }]), r;
}(Lt), mn = /* @__PURE__ */ function(t) {
  jt(r, t);
  var e = kt(r);
  function r(o) {
    var n;
    return Me(this, r), n = e.call(this), M(ne(n), "result", 0), o instanceof r ? n.result = o.result : typeof o == "number" && (n.result = o), n;
  }
  return Re(r, [{
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
}(Lt), pn = function(e, r) {
  var o = e === "css" ? gn : mn;
  return function(n) {
    return new o(n, r);
  };
}, dt = function(e, r) {
  return "".concat([r, e.replace(/([A-Z]+)([A-Z][a-z]+)/g, "$1-$2").replace(/([a-z])([A-Z])/g, "$1-$2")].filter(Boolean).join("-"));
};
function ht(t, e, r, o) {
  var n = z({}, e[t]);
  if (o != null && o.deprecatedTokens) {
    var i = o.deprecatedTokens;
    i.forEach(function(a) {
      var c = ge(a, 2), l = c[0], u = c[1];
      if (n != null && n[l] || n != null && n[u]) {
        var f;
        (f = n[u]) !== null && f !== void 0 || (n[u] = n == null ? void 0 : n[l]);
      }
    });
  }
  var s = z(z({}, r), n);
  return Object.keys(s).forEach(function(a) {
    s[a] === e[a] && delete s[a];
  }), s;
}
var Dt = typeof CSSINJS_STATISTIC < "u", Ne = !0;
function Ue() {
  for (var t = arguments.length, e = new Array(t), r = 0; r < t; r++)
    e[r] = arguments[r];
  if (!Dt)
    return Object.assign.apply(Object, [{}].concat(e));
  Ne = !1;
  var o = {};
  return e.forEach(function(n) {
    if (X(n) === "object") {
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
  }), Ne = !0, o;
}
var gt = {};
function bn() {
}
var yn = function(e) {
  var r, o = e, n = bn;
  return Dt && typeof Proxy < "u" && (r = /* @__PURE__ */ new Set(), o = new Proxy(e, {
    get: function(s, a) {
      if (Ne) {
        var c;
        (c = r) === null || c === void 0 || c.add(a);
      }
      return s[a];
    }
  }), n = function(s, a) {
    var c;
    gt[s] = {
      global: Array.from(r),
      component: z(z({}, (c = gt[s]) === null || c === void 0 ? void 0 : c.component), a)
    };
  }), {
    token: o,
    keys: r,
    flush: n
  };
};
function mt(t, e, r) {
  if (typeof r == "function") {
    var o;
    return r(Ue(e, (o = e[t]) !== null && o !== void 0 ? o : {}));
  }
  return r ?? {};
}
function vn(t) {
  return t === "js" ? {
    max: Math.max,
    min: Math.min
  } : {
    max: function() {
      for (var r = arguments.length, o = new Array(r), n = 0; n < r; n++)
        o[n] = arguments[n];
      return "max(".concat(o.map(function(i) {
        return oe(i);
      }).join(","), ")");
    },
    min: function() {
      for (var r = arguments.length, o = new Array(r), n = 0; n < r; n++)
        o[n] = arguments[n];
      return "min(".concat(o.map(function(i) {
        return oe(i);
      }).join(","), ")");
    }
  };
}
var Sn = 1e3 * 60 * 10, xn = /* @__PURE__ */ function() {
  function t() {
    Me(this, t), M(this, "map", /* @__PURE__ */ new Map()), M(this, "objectIDMap", /* @__PURE__ */ new WeakMap()), M(this, "nextID", 0), M(this, "lastAccessBeat", /* @__PURE__ */ new Map()), M(this, "accessBeat", 0);
  }
  return Re(t, [{
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
        return i && X(i) === "object" ? "obj_".concat(o.getObjectID(i)) : "".concat(X(i), "_").concat(i);
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
          o - n > Sn && (r.map.delete(i), r.lastAccessBeat.delete(i));
        }), this.accessBeat = 0;
      }
    }
  }]), t;
}(), pt = new xn();
function Cn(t, e) {
  return g.useMemo(function() {
    var r = pt.get(e);
    if (r)
      return r;
    var o = t();
    return pt.set(e, o), o;
  }, e);
}
var wn = function() {
  return {};
};
function _n(t) {
  var e = t.useCSP, r = e === void 0 ? wn : e, o = t.useToken, n = t.usePrefix, i = t.getResetStyles, s = t.getCommonStyle, a = t.getCompUnitless;
  function c(d, y, v, _) {
    var p = Array.isArray(d) ? d[0] : d;
    function S(O) {
      return "".concat(String(p)).concat(O.slice(0, 1).toUpperCase()).concat(O.slice(1));
    }
    var x = (_ == null ? void 0 : _.unitless) || {}, R = typeof a == "function" ? a(d) : {}, h = z(z({}, R), {}, M({}, S("zIndexPopup"), !0));
    Object.keys(x).forEach(function(O) {
      h[S(O)] = x[O];
    });
    var E = z(z({}, _), {}, {
      unitless: h,
      prefixToken: S
    }), m = u(d, y, v, E), P = l(p, v, E);
    return function(O) {
      var j = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : O, T = m(O, j), k = ge(T, 2), b = k[1], I = P(j), L = ge(I, 2), B = L[0], H = L[1];
      return [B, b, H];
    };
  }
  function l(d, y, v) {
    var _ = v.unitless, p = v.injectStyle, S = p === void 0 ? !0 : p, x = v.prefixToken, R = v.ignore, h = function(P) {
      var O = P.rootCls, j = P.cssVar, T = j === void 0 ? {} : j, k = o(), b = k.realToken;
      return tr({
        path: [d],
        prefix: T.prefix,
        key: T.key,
        unitless: _,
        ignore: R,
        token: b,
        scope: O
      }, function() {
        var I = mt(d, b, y), L = ht(d, b, I, {
          deprecatedTokens: v == null ? void 0 : v.deprecatedTokens
        });
        return Object.keys(I).forEach(function(B) {
          L[x(B)] = L[B], delete L[B];
        }), L;
      }), null;
    }, E = function(P) {
      var O = o(), j = O.cssVar;
      return [function(T) {
        return S && j ? /* @__PURE__ */ g.createElement(g.Fragment, null, /* @__PURE__ */ g.createElement(h, {
          rootCls: P,
          cssVar: j,
          component: d
        }), T) : T;
      }, j == null ? void 0 : j.key];
    };
    return E;
  }
  function u(d, y, v) {
    var _ = arguments.length > 3 && arguments[3] !== void 0 ? arguments[3] : {}, p = Array.isArray(d) ? d : [d, d], S = ge(p, 1), x = S[0], R = p.join("-"), h = t.layer || {
      name: "antd"
    };
    return function(E) {
      var m = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : E, P = o(), O = P.theme, j = P.realToken, T = P.hashId, k = P.token, b = P.cssVar, I = n(), L = I.rootPrefixCls, B = I.iconPrefixCls, H = r(), A = b ? "css" : "js", V = Cn(function() {
        var W = /* @__PURE__ */ new Set();
        return b && Object.keys(_.unitless || {}).forEach(function(K) {
          W.add(Ie(K, b.prefix)), W.add(Ie(K, dt(x, b.prefix)));
        }), pn(A, W);
      }, [A, x, b == null ? void 0 : b.prefix]), q = vn(A), se = q.max, Z = q.min, ae = {
        theme: O,
        token: k,
        hashId: T,
        nonce: function() {
          return H.nonce;
        },
        clientOnly: _.clientOnly,
        layer: h,
        // antd is always at top of styles
        order: _.order || -999
      };
      typeof i == "function" && Qe(z(z({}, ae), {}, {
        clientOnly: !1,
        path: ["Shared", L]
      }), function() {
        return i(k, {
          prefix: {
            rootPrefixCls: L,
            iconPrefixCls: B
          },
          csp: H
        });
      });
      var je = Qe(z(z({}, ae), {}, {
        path: [R, E, B]
      }), function() {
        if (_.injectStyle === !1)
          return [];
        var W = yn(k), K = W.token, ee = W.flush, N = mt(x, j, v), te = ".".concat(E), Ke = ht(x, j, N, {
          deprecatedTokens: _.deprecatedTokens
        });
        b && N && X(N) === "object" && Object.keys(N).forEach(function(Ye) {
          N[Ye] = "var(".concat(Ie(Ye, dt(x, b.prefix)), ")");
        });
        var qe = Ue(K, {
          componentCls: te,
          prefixCls: E,
          iconCls: ".".concat(B),
          antCls: ".".concat(L),
          calc: V,
          // @ts-ignore
          max: se,
          // @ts-ignore
          min: Z
        }, b ? N : Ke), At = y(qe, {
          hashId: T,
          prefixCls: E,
          rootPrefixCls: L,
          iconPrefixCls: B
        });
        ee(x, Ke);
        var Ft = typeof s == "function" ? s(qe, E, m, _.resetFont) : null;
        return [_.resetStyle === !1 ? null : Ft, At];
      });
      return [je, T];
    };
  }
  function f(d, y, v) {
    var _ = arguments.length > 3 && arguments[3] !== void 0 ? arguments[3] : {}, p = u(d, y, v, z({
      resetStyle: !1,
      // Sub Style should default after root one
      order: -998
    }, _)), S = function(R) {
      var h = R.prefixCls, E = R.rootCls, m = E === void 0 ? h : E;
      return p(h, m), null;
    };
    return S;
  }
  return {
    genStyleHooks: c,
    genSubStyleComponent: f,
    genComponentStyleHook: u
  };
}
const D = Math.round;
function De(t, e) {
  const r = t.replace(/^[^(]*\((.*)/, "$1").replace(/\).*/, "").match(/\d*\.?\d+%?/g) || [], o = r.map((n) => parseFloat(n));
  for (let n = 0; n < 3; n += 1)
    o[n] = e(o[n] || 0, r[n] || "", n);
  return r[3] ? o[3] = r[3].includes("%") ? o[3] / 100 : o[3] : o[3] = 1, o;
}
const bt = (t, e, r) => r === 0 ? t : t / 100;
function re(t, e) {
  const r = e || 255;
  return t > r ? r : t < 0 ? 0 : t;
}
class G {
  constructor(e) {
    M(this, "isValid", !0), M(this, "r", 0), M(this, "g", 0), M(this, "b", 0), M(this, "a", 1), M(this, "_h", void 0), M(this, "_s", void 0), M(this, "_l", void 0), M(this, "_v", void 0), M(this, "_max", void 0), M(this, "_min", void 0), M(this, "_brightness", void 0);
    function r(o) {
      return o[0] in e && o[1] in e && o[2] in e;
    }
    if (e) if (typeof e == "string") {
      let n = function(i) {
        return o.startsWith(i);
      };
      const o = e.trim();
      /^#?[A-F\d]{3,8}$/i.test(o) ? this.fromHexString(o) : n("rgb") ? this.fromRgbString(o) : n("hsl") ? this.fromHslString(o) : (n("hsv") || n("hsb")) && this.fromHsvString(o);
    } else if (e instanceof G)
      this.r = e.r, this.g = e.g, this.b = e.b, this.a = e.a, this._h = e._h, this._s = e._s, this._l = e._l, this._v = e._v;
    else if (r("rgb"))
      this.r = re(e.r), this.g = re(e.g), this.b = re(e.b), this.a = typeof e.a == "number" ? re(e.a, 1) : 1;
    else if (r("hsl"))
      this.fromHsl(e);
    else if (r("hsv"))
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
    const r = this.toHsv();
    return r.h = e, this._c(r);
  }
  // ======================= Getter =======================
  /**
   * Returns the perceived luminance of a color, from 0-1.
   * @see http://www.w3.org/TR/2008/REC-WCAG20-20081211/#relativeluminancedef
   */
  getLuminance() {
    function e(i) {
      const s = i / 255;
      return s <= 0.03928 ? s / 12.92 : Math.pow((s + 0.055) / 1.055, 2.4);
    }
    const r = e(this.r), o = e(this.g), n = e(this.b);
    return 0.2126 * r + 0.7152 * o + 0.0722 * n;
  }
  getHue() {
    if (typeof this._h > "u") {
      const e = this.getMax() - this.getMin();
      e === 0 ? this._h = 0 : this._h = D(60 * (this.r === this.getMax() ? (this.g - this.b) / e + (this.g < this.b ? 6 : 0) : this.g === this.getMax() ? (this.b - this.r) / e + 2 : (this.r - this.g) / e + 4));
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
    const r = this.getHue(), o = this.getSaturation();
    let n = this.getLightness() - e / 100;
    return n < 0 && (n = 0), this._c({
      h: r,
      s: o,
      l: n,
      a: this.a
    });
  }
  lighten(e = 10) {
    const r = this.getHue(), o = this.getSaturation();
    let n = this.getLightness() + e / 100;
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
  mix(e, r = 50) {
    const o = this._c(e), n = r / 100, i = (a) => (o[a] - this[a]) * n + this[a], s = {
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
    const r = this._c(e), o = this.a + r.a * (1 - this.a), n = (i) => D((this[i] * this.a + r[i] * r.a * (1 - this.a)) / o);
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
  equals(e) {
    return this.r === e.r && this.g === e.g && this.b === e.b && this.a === e.a;
  }
  clone() {
    return this._c(this);
  }
  // ======================= Format =======================
  toHexString() {
    let e = "#";
    const r = (this.r || 0).toString(16);
    e += r.length === 2 ? r : "0" + r;
    const o = (this.g || 0).toString(16);
    e += o.length === 2 ? o : "0" + o;
    const n = (this.b || 0).toString(16);
    if (e += n.length === 2 ? n : "0" + n, typeof this.a == "number" && this.a >= 0 && this.a < 1) {
      const i = D(this.a * 255).toString(16);
      e += i.length === 2 ? i : "0" + i;
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
    const e = this.getHue(), r = D(this.getSaturation() * 100), o = D(this.getLightness() * 100);
    return this.a !== 1 ? `hsla(${e},${r}%,${o}%,${this.a})` : `hsl(${e},${r}%,${o}%)`;
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
  _sc(e, r, o) {
    const n = this.clone();
    return n[e] = re(r, o), n;
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
    const r = e.replace("#", "");
    function o(n, i) {
      return parseInt(r[n] + r[i || n], 16);
    }
    r.length < 6 ? (this.r = o(0), this.g = o(1), this.b = o(2), this.a = r[3] ? o(3) / 255 : 1) : (this.r = o(0, 1), this.g = o(2, 3), this.b = o(4, 5), this.a = r[6] ? o(6, 7) / 255 : 1);
  }
  fromHsl({
    h: e,
    s: r,
    l: o,
    a: n
  }) {
    if (this._h = e % 360, this._s = r, this._l = o, this.a = typeof n == "number" ? n : 1, r <= 0) {
      const d = D(o * 255);
      this.r = d, this.g = d, this.b = d;
    }
    let i = 0, s = 0, a = 0;
    const c = e / 60, l = (1 - Math.abs(2 * o - 1)) * r, u = l * (1 - Math.abs(c % 2 - 1));
    c >= 0 && c < 1 ? (i = l, s = u) : c >= 1 && c < 2 ? (i = u, s = l) : c >= 2 && c < 3 ? (s = l, a = u) : c >= 3 && c < 4 ? (s = u, a = l) : c >= 4 && c < 5 ? (i = u, a = l) : c >= 5 && c < 6 && (i = l, a = u);
    const f = o - l / 2;
    this.r = D((i + f) * 255), this.g = D((s + f) * 255), this.b = D((a + f) * 255);
  }
  fromHsv({
    h: e,
    s: r,
    v: o,
    a: n
  }) {
    this._h = e % 360, this._s = r, this._v = o, this.a = typeof n == "number" ? n : 1;
    const i = D(o * 255);
    if (this.r = i, this.g = i, this.b = i, r <= 0)
      return;
    const s = e / 60, a = Math.floor(s), c = s - a, l = D(o * (1 - r) * 255), u = D(o * (1 - r * c) * 255), f = D(o * (1 - r * (1 - c)) * 255);
    switch (a) {
      case 0:
        this.g = f, this.b = l;
        break;
      case 1:
        this.r = u, this.b = l;
        break;
      case 2:
        this.r = l, this.b = f;
        break;
      case 3:
        this.r = l, this.g = u;
        break;
      case 4:
        this.r = f, this.g = l;
        break;
      case 5:
      default:
        this.g = l, this.b = u;
        break;
    }
  }
  fromHsvString(e) {
    const r = De(e, bt);
    this.fromHsv({
      h: r[0],
      s: r[1],
      v: r[2],
      a: r[3]
    });
  }
  fromHslString(e) {
    const r = De(e, bt);
    this.fromHsl({
      h: r[0],
      s: r[1],
      l: r[2],
      a: r[3]
    });
  }
  fromRgbString(e) {
    const r = De(e, (o, n) => (
      // Convert percentage to number. e.g. 50% -> 128
      n.includes("%") ? D(o / 100 * 255) : o
    ));
    this.r = r[0], this.g = r[1], this.b = r[2], this.a = r[3];
  }
}
const Tn = {
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
}, En = Object.assign(Object.assign({}, Tn), {
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
function Be(t) {
  return t >= 0 && t <= 255;
}
function ce(t, e) {
  const {
    r,
    g: o,
    b: n,
    a: i
  } = new G(t).toRgb();
  if (i < 1)
    return t;
  const {
    r: s,
    g: a,
    b: c
  } = new G(e).toRgb();
  for (let l = 0.01; l <= 1; l += 0.01) {
    const u = Math.round((r - s * (1 - l)) / l), f = Math.round((o - a * (1 - l)) / l), d = Math.round((n - c * (1 - l)) / l);
    if (Be(u) && Be(f) && Be(d))
      return new G({
        r: u,
        g: f,
        b: d,
        a: Math.round(l * 100) / 100
      }).toRgbString();
  }
  return new G({
    r,
    g: o,
    b: n,
    a: 1
  }).toRgbString();
}
var Pn = function(t, e) {
  var r = {};
  for (var o in t) Object.prototype.hasOwnProperty.call(t, o) && e.indexOf(o) < 0 && (r[o] = t[o]);
  if (t != null && typeof Object.getOwnPropertySymbols == "function") for (var n = 0, o = Object.getOwnPropertySymbols(t); n < o.length; n++)
    e.indexOf(o[n]) < 0 && Object.prototype.propertyIsEnumerable.call(t, o[n]) && (r[o[n]] = t[o[n]]);
  return r;
};
function On(t) {
  const {
    override: e
  } = t, r = Pn(t, ["override"]), o = Object.assign({}, e);
  Object.keys(En).forEach((d) => {
    delete o[d];
  });
  const n = Object.assign(Object.assign({}, r), o), i = 480, s = 576, a = 768, c = 992, l = 1200, u = 1600;
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
    colorSplit: ce(n.colorBorderSecondary, n.colorBgContainer),
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
    colorErrorOutline: ce(n.colorErrorBg, n.colorBgContainer),
    colorWarningOutline: ce(n.colorWarningBg, n.colorBgContainer),
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
    controlOutline: ce(n.colorPrimaryBg, n.colorBgContainer),
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
    screenXLMax: u - 1,
    screenXXL: u,
    screenXXLMin: u,
    boxShadowPopoverArrow: "2px 2px 5px rgba(0, 0, 0, 0.05)",
    boxShadowCard: `
      0 1px 2px -2px ${new G("rgba(0, 0, 0, 0.16)").toRgbString()},
      0 3px 6px 0 ${new G("rgba(0, 0, 0, 0.12)").toRgbString()},
      0 5px 12px 4px ${new G("rgba(0, 0, 0, 0.09)").toRgbString()}
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
const Mn = {
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
}, Rn = {
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
}, jn = rr(ze.defaultAlgorithm), In = {
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
}, Bt = (t, e, r) => {
  const o = r.getDerivativeToken(t), {
    override: n,
    ...i
  } = e;
  let s = {
    ...o,
    override: n
  };
  return s = On(s), i && Object.entries(i).forEach(([a, c]) => {
    const {
      theme: l,
      ...u
    } = c;
    let f = u;
    l && (f = Bt({
      ...s,
      ...u
    }, {
      override: u
    }, l)), s[a] = f;
  }), s;
};
function kn() {
  const {
    token: t,
    hashed: e,
    theme: r = jn,
    override: o,
    cssVar: n
  } = g.useContext(ze._internalContext), [i, s, a] = nr(r, [ze.defaultSeed, t], {
    salt: `${Ur}-${e || ""}`,
    override: o,
    getComputedToken: Bt,
    cssVar: n && {
      prefix: n.prefix,
      key: n.key,
      unitless: Mn,
      ignore: Rn,
      preserve: In
    }
  });
  return [r, a, e ? s : "", i, n];
}
const {
  genStyleHooks: Ln
} = _n({
  usePrefix: () => {
    const {
      getPrefixCls: t,
      iconPrefixCls: e
    } = pe();
    return {
      iconPrefixCls: e,
      rootPrefixCls: t()
    };
  },
  useToken: () => {
    const [t, e, r, o, n] = kn();
    return {
      theme: t,
      realToken: e,
      hashId: r,
      token: o,
      cssVar: n
    };
  },
  useCSP: () => {
    const {
      csp: t
    } = pe();
    return t ?? {};
  },
  layer: {
    name: "antdx",
    dependencies: ["antd"]
  }
});
var $n = `accept acceptCharset accessKey action allowFullScreen allowTransparency
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
    summary tabIndex target title type useMap value width wmode wrap`, Dn = `onCopy onCut onPaste onCompositionEnd onCompositionStart onCompositionUpdate onKeyDown
    onKeyPress onKeyUp onFocus onBlur onChange onInput onSubmit onClick onContextMenu onDoubleClick
    onDrag onDragEnd onDragEnter onDragExit onDragLeave onDragOver onDragStart onDrop onMouseDown
    onMouseEnter onMouseLeave onMouseMove onMouseOut onMouseOver onMouseUp onSelect onTouchCancel
    onTouchEnd onTouchMove onTouchStart onScroll onWheel onAbort onCanPlay onCanPlayThrough
    onDurationChange onEmptied onEncrypted onEnded onError onLoadedData onLoadedMetadata
    onLoadStart onPause onPlay onPlaying onProgress onRateChange onSeeked onSeeking onStalled onSuspend onTimeUpdate onVolumeChange onWaiting onLoad onError`, Bn = "".concat($n, " ").concat(Dn).split(/[\s\n]+/), Hn = "aria-", zn = "data-";
function yt(t, e) {
  return t.indexOf(e) === 0;
}
function An(t) {
  var e = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : !1, r;
  e === !1 ? r = {
    aria: !0,
    data: !0,
    attr: !0
  } : e === !0 ? r = {
    aria: !0
  } : r = on({}, e);
  var o = {};
  return Object.keys(t).forEach(function(n) {
    // Aria
    (r.aria && (n === "role" || yt(n, Hn)) || // Data
    r.data && yt(n, zn) || // Attr
    r.attr && Bn.includes(n)) && (o[n] = t[n]);
  }), o;
}
function le(t) {
  return typeof t == "string";
}
const Fn = (t, e, r, o) => {
  const n = C.useRef(""), [i, s] = C.useState(1), a = e && le(t);
  return Jr(() => {
    !a && le(t) ? s(t.length) : le(t) && le(n.current) && t.indexOf(n.current) !== 0 && s(1), n.current = t;
  }, [t]), C.useEffect(() => {
    if (a && i < t.length) {
      const l = setTimeout(() => {
        s((u) => u + r);
      }, o);
      return () => {
        clearTimeout(l);
      };
    }
  }, [i, e, t]), [a ? t.slice(0, i) : t, a && i < t.length];
};
function Xn(t) {
  return C.useMemo(() => {
    if (!t)
      return [!1, 0, 0, null];
    let e = {
      step: 1,
      interval: 50,
      // set default suffix is empty
      suffix: null
    };
    return typeof t == "object" && (e = {
      ...e,
      ...t
    }), [!0, e.step, e.interval, e.suffix];
  }, [t]);
}
const Nn = ({
  prefixCls: t
}) => /* @__PURE__ */ g.createElement("span", {
  className: `${t}-dot`
}, /* @__PURE__ */ g.createElement("i", {
  className: `${t}-dot-item`,
  key: "item-1"
}), /* @__PURE__ */ g.createElement("i", {
  className: `${t}-dot-item`,
  key: "item-2"
}), /* @__PURE__ */ g.createElement("i", {
  className: `${t}-dot-item`,
  key: "item-3"
})), Vn = (t) => {
  const {
    componentCls: e,
    paddingSM: r,
    padding: o
  } = t;
  return {
    [e]: {
      [`${e}-content`]: {
        // Shared: filled, outlined, shadow
        "&-filled,&-outlined,&-shadow": {
          padding: `${oe(r)} ${oe(o)}`,
          borderRadius: t.borderRadiusLG
        },
        // Filled:
        "&-filled": {
          backgroundColor: t.colorFillContent
        },
        // Outlined:
        "&-outlined": {
          border: `1px solid ${t.colorBorderSecondary}`
        },
        // Shadow:
        "&-shadow": {
          boxShadow: t.boxShadowTertiary
        }
      }
    }
  };
}, Wn = (t) => {
  const {
    componentCls: e,
    fontSize: r,
    lineHeight: o,
    paddingSM: n,
    padding: i,
    calc: s
  } = t, a = s(r).mul(o).div(2).add(n).equal(), c = `${e}-content`;
  return {
    [e]: {
      [c]: {
        // round:
        "&-round": {
          borderRadius: {
            _skip_check_: !0,
            value: a
          },
          paddingInline: s(i).mul(1.25).equal()
        }
      },
      // corner:
      [`&-start ${c}-corner`]: {
        borderStartStartRadius: t.borderRadiusXS
      },
      [`&-end ${c}-corner`]: {
        borderStartEndRadius: t.borderRadiusXS
      }
    }
  };
}, Un = (t) => {
  const {
    componentCls: e,
    padding: r
  } = t;
  return {
    [`${e}-list`]: {
      display: "flex",
      flexDirection: "column",
      gap: r,
      overflowY: "auto",
      "&::-webkit-scrollbar": {
        width: 8,
        backgroundColor: "transparent"
      },
      "&::-webkit-scrollbar-thumb": {
        backgroundColor: t.colorTextTertiary,
        borderRadius: t.borderRadiusSM
      },
      // For Firefox
      "&": {
        scrollbarWidth: "thin",
        scrollbarColor: `${t.colorTextTertiary} transparent`
      }
    }
  };
}, Gn = new Ct("loadingMove", {
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
}), Kn = new Ct("cursorBlink", {
  "0%": {
    opacity: 1
  },
  "50%": {
    opacity: 0
  },
  "100%": {
    opacity: 1
  }
}), qn = (t) => {
  const {
    componentCls: e,
    fontSize: r,
    lineHeight: o,
    paddingSM: n,
    colorText: i,
    calc: s
  } = t;
  return {
    [e]: {
      display: "flex",
      columnGap: n,
      [`&${e}-end`]: {
        justifyContent: "end",
        flexDirection: "row-reverse",
        [`& ${e}-content-wrapper`]: {
          alignItems: "flex-end"
        }
      },
      [`&${e}-rtl`]: {
        direction: "rtl"
      },
      [`&${e}-typing ${e}-content:last-child::after`]: {
        content: '"|"',
        fontWeight: 900,
        userSelect: "none",
        opacity: 1,
        marginInlineStart: "0.1em",
        animationName: Kn,
        animationDuration: "0.8s",
        animationIterationCount: "infinite",
        animationTimingFunction: "linear"
      },
      // ============================ Avatar =============================
      [`& ${e}-avatar`]: {
        display: "inline-flex",
        justifyContent: "center",
        alignSelf: "flex-start"
      },
      // ======================== Header & Footer ========================
      [`& ${e}-header, & ${e}-footer`]: {
        fontSize: r,
        lineHeight: o,
        color: t.colorText
      },
      [`& ${e}-header`]: {
        marginBottom: t.paddingXXS
      },
      [`& ${e}-footer`]: {
        marginTop: n
      },
      // =========================== Content =============================
      [`& ${e}-content-wrapper`]: {
        flex: "auto",
        display: "flex",
        flexDirection: "column",
        alignItems: "flex-start",
        minWidth: 0,
        maxWidth: "100%"
      },
      [`& ${e}-content`]: {
        position: "relative",
        boxSizing: "border-box",
        minWidth: 0,
        maxWidth: "100%",
        color: i,
        fontSize: t.fontSize,
        lineHeight: t.lineHeight,
        minHeight: s(n).mul(2).add(s(o).mul(r)).equal(),
        wordBreak: "break-word",
        [`& ${e}-dot`]: {
          position: "relative",
          height: "100%",
          display: "flex",
          alignItems: "center",
          columnGap: t.marginXS,
          padding: `0 ${oe(t.paddingXXS)}`,
          "&-item": {
            backgroundColor: t.colorPrimary,
            borderRadius: "100%",
            width: 4,
            height: 4,
            animationName: Gn,
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
}, Yn = () => ({}), Ht = Ln("Bubble", (t) => {
  const e = Ue(t, {});
  return [qn(e), Un(e), Vn(e), Wn(e)];
}, Yn), zt = /* @__PURE__ */ g.createContext({}), Qn = (t, e) => {
  const {
    prefixCls: r,
    className: o,
    rootClassName: n,
    style: i,
    classNames: s = {},
    styles: a = {},
    avatar: c,
    placement: l = "start",
    loading: u = !1,
    loadingRender: f,
    typing: d,
    content: y = "",
    messageRender: v,
    variant: _ = "filled",
    shape: p,
    onTypingComplete: S,
    header: x,
    footer: R,
    _key: h,
    ...E
  } = t, {
    onUpdate: m
  } = g.useContext(zt), P = g.useRef(null);
  g.useImperativeHandle(e, () => ({
    nativeElement: P.current
  }));
  const {
    direction: O,
    getPrefixCls: j
  } = pe(), T = j("bubble", r), k = qr("bubble"), [b, I, L, B] = Xn(d), [H, A] = Fn(y, b, I, L);
  g.useEffect(() => {
    m == null || m();
  }, [H]);
  const V = g.useRef(!1);
  g.useEffect(() => {
    !A && !u ? V.current || (V.current = !0, S == null || S()) : V.current = !1;
  }, [A, u]);
  const [q, se, Z] = Ht(T), ae = Y(T, n, k.className, o, se, Z, `${T}-${l}`, {
    [`${T}-rtl`]: O === "rtl",
    [`${T}-typing`]: A && !u && !v && !B
  }), je = g.useMemo(() => /* @__PURE__ */ g.isValidElement(c) ? c : /* @__PURE__ */ g.createElement(er, c), [c]), W = g.useMemo(() => v ? v(H) : H, [H, v]), K = (te) => typeof te == "function" ? te(H, {
    key: h
  }) : te;
  let ee;
  u ? ee = f ? f() : /* @__PURE__ */ g.createElement(Nn, {
    prefixCls: T
  }) : ee = /* @__PURE__ */ g.createElement(g.Fragment, null, W, A && B);
  let N = /* @__PURE__ */ g.createElement("div", {
    style: {
      ...k.styles.content,
      ...a.content
    },
    className: Y(`${T}-content`, `${T}-content-${_}`, p && `${T}-content-${p}`, k.classNames.content, s.content)
  }, ee);
  return (x || R) && (N = /* @__PURE__ */ g.createElement("div", {
    className: `${T}-content-wrapper`
  }, x && /* @__PURE__ */ g.createElement("div", {
    className: Y(`${T}-header`, k.classNames.header, s.header),
    style: {
      ...k.styles.header,
      ...a.header
    }
  }, K(x)), N, R && /* @__PURE__ */ g.createElement("div", {
    className: Y(`${T}-footer`, k.classNames.footer, s.footer),
    style: {
      ...k.styles.footer,
      ...a.footer
    }
  }, K(R)))), q(/* @__PURE__ */ g.createElement("div", J({
    style: {
      ...k.style,
      ...i
    },
    className: ae
  }, E, {
    ref: P
  }), c && /* @__PURE__ */ g.createElement("div", {
    style: {
      ...k.styles.avatar,
      ...a.avatar
    },
    className: Y(`${T}-avatar`, k.classNames.avatar, s.avatar)
  }, je), N));
}, Ge = /* @__PURE__ */ g.forwardRef(Qn);
function Jn(t, e) {
  const r = C.useCallback((o, n) => typeof e == "function" ? e(o, n) : e ? e[o.role] || {} : {}, [e]);
  return C.useMemo(() => (t || []).map((o, n) => {
    const i = o.key ?? `preset_${n}`;
    return {
      ...r(o, n),
      ...o,
      key: i
    };
  }), [t, r]);
}
const Zn = ({
  _key: t,
  ...e
}, r) => /* @__PURE__ */ C.createElement(Ge, J({}, e, {
  ref: (o) => {
    var n;
    o ? r.current[t] = o : (n = r.current) == null || delete n[t];
  }
})), eo = /* @__PURE__ */ C.memo(/* @__PURE__ */ C.forwardRef(Zn)), to = 1, ro = (t, e) => {
  const {
    prefixCls: r,
    rootClassName: o,
    className: n,
    items: i,
    autoScroll: s = !0,
    roles: a,
    ...c
  } = t, l = An(c, {
    attr: !0,
    aria: !0
  }), u = C.useRef(null), f = C.useRef({}), {
    getPrefixCls: d
  } = pe(), y = d("bubble", r), v = `${y}-list`, [_, p, S] = Ht(y), [x, R] = C.useState(!1);
  C.useEffect(() => (R(!0), () => {
    R(!1);
  }), []);
  const h = Jn(i, a), [E, m] = C.useState(!0), [P, O] = C.useState(0), j = (b) => {
    const I = b.target;
    m(I.scrollHeight - Math.abs(I.scrollTop) - I.clientHeight <= to);
  };
  C.useEffect(() => {
    s && u.current && E && u.current.scrollTo({
      top: u.current.scrollHeight
    });
  }, [P]), C.useEffect(() => {
    var b;
    if (s) {
      const I = (b = h[h.length - 2]) == null ? void 0 : b.key, L = f.current[I];
      if (L) {
        const {
          nativeElement: B
        } = L, {
          top: H,
          bottom: A
        } = B.getBoundingClientRect(), {
          top: V,
          bottom: q
        } = u.current.getBoundingClientRect();
        H < q && A > V && (O((Z) => Z + 1), m(!0));
      }
    }
  }, [h.length]), C.useImperativeHandle(e, () => ({
    nativeElement: u.current,
    scrollTo: ({
      key: b,
      offset: I,
      behavior: L = "smooth",
      block: B
    }) => {
      if (typeof I == "number")
        u.current.scrollTo({
          top: I,
          behavior: L
        });
      else if (b !== void 0) {
        const H = f.current[b];
        if (H) {
          const A = h.findIndex((V) => V.key === b);
          m(A === h.length - 1), H.nativeElement.scrollIntoView({
            behavior: L,
            block: B
          });
        }
      }
    }
  }));
  const T = Yr(() => {
    s && O((b) => b + 1);
  }), k = C.useMemo(() => ({
    onUpdate: T
  }), []);
  return _(/* @__PURE__ */ C.createElement(zt.Provider, {
    value: k
  }, /* @__PURE__ */ C.createElement("div", J({}, l, {
    className: Y(v, o, n, p, S, {
      [`${v}-reach-end`]: E
    }),
    ref: u,
    onScroll: j
  }), h.map(({
    key: b,
    ...I
  }) => /* @__PURE__ */ C.createElement(eo, J({}, I, {
    key: b,
    _key: b,
    ref: f,
    typing: x ? I.typing : !1
  }))))));
}, no = /* @__PURE__ */ C.forwardRef(ro);
Ge.List = no;
function oo(t) {
  return /^(?:async\s+)?(?:function\s*(?:\w*\s*)?\(|\([\w\s,=]*\)\s*=>|\(\{[\w\s,=]*\}\)\s*=>|function\s*\*\s*\w*\s*\()/i.test(t.trim());
}
function io(t, e = !1) {
  try {
    if (Yt(t))
      return t;
    if (e && !oo(t))
      return;
    if (typeof t == "string") {
      let r = t.trim();
      return r.startsWith(";") && (r = r.slice(1)), r.endsWith(";") && (r = r.slice(0, -1)), new Function(`return (...args) => (${r})(...args)`)();
    }
    return;
  } catch {
    return;
  }
}
function ue(t, e) {
  return xt(() => io(t, e), [t, e]);
}
const so = ({
  children: t,
  ...e
}) => /* @__PURE__ */ $.jsx($.Fragment, {
  children: t(e)
});
function ao(t) {
  return g.createElement(so, {
    children: t
  });
}
function vt(t, e) {
  return t ? e != null && e.forceClone || e != null && e.params ? ao((r) => /* @__PURE__ */ $.jsx(Jt, {
    forceClone: e == null ? void 0 : e.forceClone,
    params: e == null ? void 0 : e.params,
    children: /* @__PURE__ */ $.jsx(U, {
      slot: t,
      clone: e == null ? void 0 : e.clone,
      ...r
    })
  })) : /* @__PURE__ */ $.jsx(U, {
    slot: t,
    clone: e == null ? void 0 : e.clone
  }) : null;
}
function St({
  key: t,
  slots: e,
  targets: r
}, o) {
  return e[t] ? (...n) => r ? r.map((i, s) => /* @__PURE__ */ $.jsx(g.Fragment, {
    children: vt(i, {
      clone: !0,
      params: n,
      forceClone: !0
    })
  }, s)) : /* @__PURE__ */ $.jsx($.Fragment, {
    children: vt(e[t], {
      clone: !0,
      params: n,
      forceClone: !0
    })
  }) : void 0;
}
const uo = Fr(({
  loadingRender: t,
  messageRender: e,
  slots: r,
  setSlotParams: o,
  children: n,
  ...i
}) => {
  const s = ue(t), a = ue(e), c = ue(i.header, !0), l = ue(i.footer, !0), u = xt(() => {
    var f, d;
    return r.avatar ? /* @__PURE__ */ $.jsx(U, {
      slot: r.avatar
    }) : r["avatar.icon"] || r["avatar.src"] ? {
      ...i.avatar || {},
      icon: r["avatar.icon"] ? /* @__PURE__ */ $.jsx(U, {
        slot: r["avatar.icon"]
      }) : (f = i.avatar) == null ? void 0 : f.icon,
      src: r["avatar.src"] ? /* @__PURE__ */ $.jsx(U, {
        slot: r["avatar.src"]
      }) : (d = i.avatar) == null ? void 0 : d.src
    } : i.avatar;
  }, [i.avatar, r]);
  return /* @__PURE__ */ $.jsxs($.Fragment, {
    children: [/* @__PURE__ */ $.jsx("div", {
      style: {
        display: "none"
      },
      children: n
    }), /* @__PURE__ */ $.jsx(Ge, {
      ...i,
      avatar: u,
      typing: r["typing.suffix"] ? {
        ...me(i.typing) ? i.typing : {},
        suffix: /* @__PURE__ */ $.jsx(U, {
          slot: r["typing.suffix"]
        })
      } : i.typing,
      content: r.content ? /* @__PURE__ */ $.jsx(U, {
        slot: r.content
      }) : i.content,
      footer: r.footer ? /* @__PURE__ */ $.jsx(U, {
        slot: r.footer
      }) : l || i.footer,
      header: r.header ? /* @__PURE__ */ $.jsx(U, {
        slot: r.header
      }) : c || i.header,
      loadingRender: r.loadingRender ? St({
        slots: r,
        key: "loadingRender"
      }) : s,
      messageRender: r.messageRender ? St({
        slots: r,
        key: "messageRender"
      }) : a
    })]
  });
});
export {
  uo as Bubble,
  uo as default
};
