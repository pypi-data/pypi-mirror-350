import { i as ir, a as Ie, r as sr, w as ee, g as ar, c as q, b as wt } from "./Index-C6hyMPFT.js";
const F = window.ms_globals.React, S = window.ms_globals.React, er = window.ms_globals.React.forwardRef, tr = window.ms_globals.React.useRef, rr = window.ms_globals.React.useState, nr = window.ms_globals.React.useEffect, or = window.ms_globals.React.version, Ee = window.ms_globals.React.useMemo, je = window.ms_globals.ReactDOM.createPortal, lr = window.ms_globals.internalContext.useContextPropsContext, ke = window.ms_globals.internalContext.ContextPropsProvider, Ot = window.ms_globals.createItemsContext.createItemsContext, cr = window.ms_globals.antd.ConfigProvider, Le = window.ms_globals.antd.theme, Pt = window.ms_globals.antd.Typography, ur = window.ms_globals.antd.Dropdown, fr = window.ms_globals.antdIcons.EllipsisOutlined, oe = window.ms_globals.antdCssinjs.unit, Se = window.ms_globals.antdCssinjs.token2CSSVar, qe = window.ms_globals.antdCssinjs.useStyleRegister, dr = window.ms_globals.antdCssinjs.useCSSVarRegister, hr = window.ms_globals.antdCssinjs.createTheme, gr = window.ms_globals.antdCssinjs.useCacheToken;
var mr = /\s/;
function pr(t) {
  for (var e = t.length; e-- && mr.test(t.charAt(e)); )
    ;
  return e;
}
var br = /^\s+/;
function yr(t) {
  return t && t.slice(0, pr(t) + 1).replace(br, "");
}
var Qe = NaN, vr = /^[-+]0x[0-9a-f]+$/i, Sr = /^0b[01]+$/i, xr = /^0o[0-7]+$/i, Cr = parseInt;
function Je(t) {
  if (typeof t == "number")
    return t;
  if (ir(t))
    return Qe;
  if (Ie(t)) {
    var e = typeof t.valueOf == "function" ? t.valueOf() : t;
    t = Ie(e) ? e + "" : e;
  }
  if (typeof t != "string")
    return t === 0 ? t : +t;
  t = yr(t);
  var n = Sr.test(t);
  return n || xr.test(t) ? Cr(t.slice(2), n ? 2 : 8) : vr.test(t) ? Qe : +t;
}
var xe = function() {
  return sr.Date.now();
}, _r = "Expected a function", wr = Math.max, Or = Math.min;
function Pr(t, e, n) {
  var o, r, i, s, a, l, c = 0, f = !1, u = !1, d = !0;
  if (typeof t != "function")
    throw new TypeError(_r);
  e = Je(e) || 0, Ie(n) && (f = !!n.leading, u = "maxWait" in n, i = u ? wr(Je(n.maxWait) || 0, e) : i, d = "trailing" in n ? !!n.trailing : d);
  function g(v) {
    var O = o, T = r;
    return o = r = void 0, c = v, s = t.apply(T, O), s;
  }
  function b(v) {
    return c = v, a = setTimeout(m, e), f ? g(v) : s;
  }
  function y(v) {
    var O = v - l, T = v - c, E = e - O;
    return u ? Or(E, i - T) : E;
  }
  function h(v) {
    var O = v - l, T = v - c;
    return l === void 0 || O >= e || O < 0 || u && T >= i;
  }
  function m() {
    var v = xe();
    if (h(v))
      return x(v);
    a = setTimeout(m, y(v));
  }
  function x(v) {
    return a = void 0, d && o ? g(v) : (o = r = void 0, s);
  }
  function M() {
    a !== void 0 && clearTimeout(a), c = 0, o = l = r = a = void 0;
  }
  function p() {
    return a === void 0 ? s : x(xe());
  }
  function C() {
    var v = xe(), O = h(v);
    if (o = arguments, r = this, l = v, O) {
      if (a === void 0)
        return b(l);
      if (u)
        return clearTimeout(a), a = setTimeout(m, e), g(l);
    }
    return a === void 0 && (a = setTimeout(m, e)), s;
  }
  return C.cancel = M, C.flush = p, C;
}
var Tt = {
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
var Tr = S, Mr = Symbol.for("react.element"), Er = Symbol.for("react.fragment"), jr = Object.prototype.hasOwnProperty, Ir = Tr.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, kr = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function Mt(t, e, n) {
  var o, r = {}, i = null, s = null;
  n !== void 0 && (i = "" + n), e.key !== void 0 && (i = "" + e.key), e.ref !== void 0 && (s = e.ref);
  for (o in e) jr.call(e, o) && !kr.hasOwnProperty(o) && (r[o] = e[o]);
  if (t && t.defaultProps) for (o in e = t.defaultProps, e) r[o] === void 0 && (r[o] = e[o]);
  return {
    $$typeof: Mr,
    type: t,
    key: i,
    ref: s,
    props: r,
    _owner: Ir.current
  };
}
ae.Fragment = Er;
ae.jsx = Mt;
ae.jsxs = Mt;
Tt.exports = ae;
var I = Tt.exports;
const {
  SvelteComponent: Lr,
  assign: Ze,
  binding_callbacks: Ye,
  check_outros: Rr,
  children: Et,
  claim_element: jt,
  claim_space: $r,
  component_subscribe: et,
  compute_slots: Ar,
  create_slot: Dr,
  detach: G,
  element: It,
  empty: tt,
  exclude_internal_props: rt,
  get_all_dirty_from_scope: Hr,
  get_slot_changes: zr,
  group_outros: Br,
  init: Xr,
  insert_hydration: te,
  safe_not_equal: Fr,
  set_custom_element_data: kt,
  space: Vr,
  transition_in: re,
  transition_out: Re,
  update_slot_base: Nr
} = window.__gradio__svelte__internal, {
  beforeUpdate: Gr,
  getContext: Ur,
  onDestroy: Wr,
  setContext: Kr
} = window.__gradio__svelte__internal;
function nt(t) {
  let e, n;
  const o = (
    /*#slots*/
    t[7].default
  ), r = Dr(
    o,
    t,
    /*$$scope*/
    t[6],
    null
  );
  return {
    c() {
      e = It("svelte-slot"), r && r.c(), this.h();
    },
    l(i) {
      e = jt(i, "SVELTE-SLOT", {
        class: !0
      });
      var s = Et(e);
      r && r.l(s), s.forEach(G), this.h();
    },
    h() {
      kt(e, "class", "svelte-1rt0kpf");
    },
    m(i, s) {
      te(i, e, s), r && r.m(e, null), t[9](e), n = !0;
    },
    p(i, s) {
      r && r.p && (!n || s & /*$$scope*/
      64) && Nr(
        r,
        o,
        i,
        /*$$scope*/
        i[6],
        n ? zr(
          o,
          /*$$scope*/
          i[6],
          s,
          null
        ) : Hr(
          /*$$scope*/
          i[6]
        ),
        null
      );
    },
    i(i) {
      n || (re(r, i), n = !0);
    },
    o(i) {
      Re(r, i), n = !1;
    },
    d(i) {
      i && G(e), r && r.d(i), t[9](null);
    }
  };
}
function qr(t) {
  let e, n, o, r, i = (
    /*$$slots*/
    t[4].default && nt(t)
  );
  return {
    c() {
      e = It("react-portal-target"), n = Vr(), i && i.c(), o = tt(), this.h();
    },
    l(s) {
      e = jt(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), Et(e).forEach(G), n = $r(s), i && i.l(s), o = tt(), this.h();
    },
    h() {
      kt(e, "class", "svelte-1rt0kpf");
    },
    m(s, a) {
      te(s, e, a), t[8](e), te(s, n, a), i && i.m(s, a), te(s, o, a), r = !0;
    },
    p(s, [a]) {
      /*$$slots*/
      s[4].default ? i ? (i.p(s, a), a & /*$$slots*/
      16 && re(i, 1)) : (i = nt(s), i.c(), re(i, 1), i.m(o.parentNode, o)) : i && (Br(), Re(i, 1, 1, () => {
        i = null;
      }), Rr());
    },
    i(s) {
      r || (re(i), r = !0);
    },
    o(s) {
      Re(i), r = !1;
    },
    d(s) {
      s && (G(e), G(n), G(o)), t[8](null), i && i.d(s);
    }
  };
}
function ot(t) {
  const {
    svelteInit: e,
    ...n
  } = t;
  return n;
}
function Qr(t, e, n) {
  let o, r, {
    $$slots: i = {},
    $$scope: s
  } = e;
  const a = Ar(i);
  let {
    svelteInit: l
  } = e;
  const c = ee(ot(e)), f = ee();
  et(t, f, (p) => n(0, o = p));
  const u = ee();
  et(t, u, (p) => n(1, r = p));
  const d = [], g = Ur("$$ms-gr-react-wrapper"), {
    slotKey: b,
    slotIndex: y,
    subSlotIndex: h
  } = ar() || {}, m = l({
    parent: g,
    props: c,
    target: f,
    slot: u,
    slotKey: b,
    slotIndex: y,
    subSlotIndex: h,
    onDestroy(p) {
      d.push(p);
    }
  });
  Kr("$$ms-gr-react-wrapper", m), Gr(() => {
    c.set(ot(e));
  }), Wr(() => {
    d.forEach((p) => p());
  });
  function x(p) {
    Ye[p ? "unshift" : "push"](() => {
      o = p, f.set(o);
    });
  }
  function M(p) {
    Ye[p ? "unshift" : "push"](() => {
      r = p, u.set(r);
    });
  }
  return t.$$set = (p) => {
    n(17, e = Ze(Ze({}, e), rt(p))), "svelteInit" in p && n(5, l = p.svelteInit), "$$scope" in p && n(6, s = p.$$scope);
  }, e = rt(e), [o, r, f, u, a, l, s, i, x, M];
}
class Jr extends Lr {
  constructor(e) {
    super(), Xr(this, e, Qr, qr, Fr, {
      svelteInit: 5
    });
  }
}
const {
  SvelteComponent: yo
} = window.__gradio__svelte__internal, it = window.ms_globals.rerender, Ce = window.ms_globals.tree;
function Zr(t, e = {}) {
  function n(o) {
    const r = ee(), i = new Jr({
      ...o,
      props: {
        svelteInit(s) {
          window.ms_globals.autokey += 1;
          const a = {
            key: window.ms_globals.autokey,
            svelteInstance: r,
            reactComponent: t,
            props: s.props,
            slot: s.slot,
            target: s.target,
            slotIndex: s.slotIndex,
            subSlotIndex: s.subSlotIndex,
            ignore: e.ignore,
            slotKey: s.slotKey,
            nodes: []
          }, l = s.parent ?? Ce;
          return l.nodes = [...l.nodes, a], it({
            createPortal: je,
            node: Ce
          }), s.onDestroy(() => {
            l.nodes = l.nodes.filter((c) => c.svelteInstance !== r), it({
              createPortal: je,
              node: Ce
            });
          }), a;
        },
        ...o.props
      }
    });
    return r.set(i), i;
  }
  return new Promise((o) => {
    window.ms_globals.initializePromise.then(() => {
      o(n);
    });
  });
}
const Yr = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function en(t) {
  return t ? Object.keys(t).reduce((e, n) => {
    const o = t[n];
    return e[n] = tn(n, o), e;
  }, {}) : {};
}
function tn(t, e) {
  return typeof e == "number" && !Yr.includes(t) ? e + "px" : e;
}
function $e(t) {
  const e = [], n = t.cloneNode(!1);
  if (t._reactElement) {
    const r = S.Children.toArray(t._reactElement.props.children).map((i) => {
      if (S.isValidElement(i) && i.props.__slot__) {
        const {
          portals: s,
          clonedElement: a
        } = $e(i.props.el);
        return S.cloneElement(i, {
          ...i.props,
          el: a,
          children: [...S.Children.toArray(i.props.children), ...s]
        });
      }
      return null;
    });
    return r.originalChildren = t._reactElement.props.children, e.push(je(S.cloneElement(t._reactElement, {
      ...t._reactElement.props,
      children: r
    }), n)), {
      clonedElement: n,
      portals: e
    };
  }
  Object.keys(t.getEventListeners()).forEach((r) => {
    t.getEventListeners(r).forEach(({
      listener: s,
      type: a,
      useCapture: l
    }) => {
      n.addEventListener(a, s, l);
    });
  });
  const o = Array.from(t.childNodes);
  for (let r = 0; r < o.length; r++) {
    const i = o[r];
    if (i.nodeType === 1) {
      const {
        clonedElement: s,
        portals: a
      } = $e(i);
      e.push(...a), n.appendChild(s);
    } else i.nodeType === 3 && n.appendChild(i.cloneNode());
  }
  return {
    clonedElement: n,
    portals: e
  };
}
function rn(t, e) {
  t && (typeof t == "function" ? t(e) : t.current = e);
}
const Q = er(({
  slot: t,
  clone: e,
  className: n,
  style: o,
  observeAttributes: r
}, i) => {
  const s = tr(), [a, l] = rr([]), {
    forceClone: c
  } = lr(), f = c ? !0 : e;
  return nr(() => {
    var y;
    if (!s.current || !t)
      return;
    let u = t;
    function d() {
      let h = u;
      if (u.tagName.toLowerCase() === "svelte-slot" && u.children.length === 1 && u.children[0] && (h = u.children[0], h.tagName.toLowerCase() === "react-portal-target" && h.children[0] && (h = h.children[0])), rn(i, h), n && h.classList.add(...n.split(" ")), o) {
        const m = en(o);
        Object.keys(m).forEach((x) => {
          h.style[x] = m[x];
        });
      }
    }
    let g = null, b = null;
    if (f && window.MutationObserver) {
      let h = function() {
        var p, C, v;
        (p = s.current) != null && p.contains(u) && ((C = s.current) == null || C.removeChild(u));
        const {
          portals: x,
          clonedElement: M
        } = $e(t);
        u = M, l(x), u.style.display = "contents", b && clearTimeout(b), b = setTimeout(() => {
          d();
        }, 50), (v = s.current) == null || v.appendChild(u);
      };
      h();
      const m = Pr(() => {
        h(), g == null || g.disconnect(), g == null || g.observe(t, {
          childList: !0,
          subtree: !0,
          attributes: r
        });
      }, 50);
      g = new window.MutationObserver(m), g.observe(t, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      u.style.display = "contents", d(), (y = s.current) == null || y.appendChild(u);
    return () => {
      var h, m;
      u.style.display = "", (h = s.current) != null && h.contains(u) && ((m = s.current) == null || m.removeChild(u)), g == null || g.disconnect();
    };
  }, [t, f, n, o, i, r, c]), S.createElement("react-child", {
    ref: s,
    style: {
      display: "contents"
    }
  }, ...a);
}), nn = "1.3.0", on = /* @__PURE__ */ S.createContext({}), sn = {
  classNames: {},
  styles: {},
  className: "",
  style: {}
}, an = (t) => {
  const e = S.useContext(on);
  return S.useMemo(() => ({
    ...sn,
    ...e[t]
  }), [e[t]]);
};
function ie() {
  return ie = Object.assign ? Object.assign.bind() : function(t) {
    for (var e = 1; e < arguments.length; e++) {
      var n = arguments[e];
      for (var o in n) ({}).hasOwnProperty.call(n, o) && (t[o] = n[o]);
    }
    return t;
  }, ie.apply(null, arguments);
}
function Ae() {
  const {
    getPrefixCls: t,
    direction: e,
    csp: n,
    iconPrefixCls: o,
    theme: r
  } = S.useContext(cr.ConfigContext);
  return {
    theme: r,
    getPrefixCls: t,
    direction: e,
    csp: n,
    iconPrefixCls: o
  };
}
function st(t) {
  var e = F.useRef();
  e.current = t;
  var n = F.useCallback(function() {
    for (var o, r = arguments.length, i = new Array(r), s = 0; s < r; s++)
      i[s] = arguments[s];
    return (o = e.current) === null || o === void 0 ? void 0 : o.call.apply(o, [e].concat(i));
  }, []);
  return n;
}
function ln(t) {
  if (Array.isArray(t)) return t;
}
function cn(t, e) {
  var n = t == null ? null : typeof Symbol < "u" && t[Symbol.iterator] || t["@@iterator"];
  if (n != null) {
    var o, r, i, s, a = [], l = !0, c = !1;
    try {
      if (i = (n = n.call(t)).next, e !== 0) for (; !(l = (o = i.call(n)).done) && (a.push(o.value), a.length !== e); l = !0) ;
    } catch (f) {
      c = !0, r = f;
    } finally {
      try {
        if (!l && n.return != null && (s = n.return(), Object(s) !== s)) return;
      } finally {
        if (c) throw r;
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
function un(t, e) {
  if (t) {
    if (typeof t == "string") return at(t, e);
    var n = {}.toString.call(t).slice(8, -1);
    return n === "Object" && t.constructor && (n = t.constructor.name), n === "Map" || n === "Set" ? Array.from(t) : n === "Arguments" || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n) ? at(t, e) : void 0;
  }
}
function fn() {
  throw new TypeError(`Invalid attempt to destructure non-iterable instance.
In order to be iterable, non-array objects must have a [Symbol.iterator]() method.`);
}
function De(t, e) {
  return ln(t) || cn(t, e) || un(t, e) || fn();
}
function dn() {
  return !!(typeof window < "u" && window.document && window.document.createElement);
}
var lt = dn() ? F.useLayoutEffect : F.useEffect, hn = function(e, n) {
  var o = F.useRef(!0);
  lt(function() {
    return e(o.current);
  }, n), lt(function() {
    return o.current = !1, function() {
      o.current = !0;
    };
  }, []);
}, ct = function(e, n) {
  hn(function(o) {
    if (!o)
      return e();
  }, n);
};
function ut(t) {
  var e = F.useRef(!1), n = F.useState(t), o = De(n, 2), r = o[0], i = o[1];
  F.useEffect(function() {
    return e.current = !1, function() {
      e.current = !0;
    };
  }, []);
  function s(a, l) {
    l && e.current || i(a);
  }
  return [r, s];
}
function _e(t) {
  return t !== void 0;
}
function gn(t, e) {
  var n = e || {}, o = n.defaultValue, r = n.value, i = n.onChange, s = n.postState, a = ut(function() {
    return _e(r) ? r : _e(o) ? typeof o == "function" ? o() : o : typeof t == "function" ? t() : t;
  }), l = De(a, 2), c = l[0], f = l[1], u = r !== void 0 ? r : c, d = s ? s(u) : u, g = st(i), b = ut([u]), y = De(b, 2), h = y[0], m = y[1];
  ct(function() {
    var M = h[0];
    c !== M && g(c, M);
  }, [h]), ct(function() {
    _e(r) || f(r);
  }, [r]);
  var x = st(function(M, p) {
    f(M, p), m([u], p);
  });
  return [d, x];
}
function J(t) {
  "@babel/helpers - typeof";
  return J = typeof Symbol == "function" && typeof Symbol.iterator == "symbol" ? function(e) {
    return typeof e;
  } : function(e) {
    return e && typeof Symbol == "function" && e.constructor === Symbol && e !== Symbol.prototype ? "symbol" : typeof e;
  }, J(t);
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
var Xe = Symbol.for("react.element"), Fe = Symbol.for("react.portal"), le = Symbol.for("react.fragment"), ce = Symbol.for("react.strict_mode"), ue = Symbol.for("react.profiler"), fe = Symbol.for("react.provider"), de = Symbol.for("react.context"), mn = Symbol.for("react.server_context"), he = Symbol.for("react.forward_ref"), ge = Symbol.for("react.suspense"), me = Symbol.for("react.suspense_list"), pe = Symbol.for("react.memo"), be = Symbol.for("react.lazy"), pn = Symbol.for("react.offscreen"), Lt;
Lt = Symbol.for("react.module.reference");
function A(t) {
  if (typeof t == "object" && t !== null) {
    var e = t.$$typeof;
    switch (e) {
      case Xe:
        switch (t = t.type, t) {
          case le:
          case ue:
          case ce:
          case ge:
          case me:
            return t;
          default:
            switch (t = t && t.$$typeof, t) {
              case mn:
              case de:
              case he:
              case be:
              case pe:
              case fe:
                return t;
              default:
                return e;
            }
        }
      case Fe:
        return e;
    }
  }
}
w.ContextConsumer = de;
w.ContextProvider = fe;
w.Element = Xe;
w.ForwardRef = he;
w.Fragment = le;
w.Lazy = be;
w.Memo = pe;
w.Portal = Fe;
w.Profiler = ue;
w.StrictMode = ce;
w.Suspense = ge;
w.SuspenseList = me;
w.isAsyncMode = function() {
  return !1;
};
w.isConcurrentMode = function() {
  return !1;
};
w.isContextConsumer = function(t) {
  return A(t) === de;
};
w.isContextProvider = function(t) {
  return A(t) === fe;
};
w.isElement = function(t) {
  return typeof t == "object" && t !== null && t.$$typeof === Xe;
};
w.isForwardRef = function(t) {
  return A(t) === he;
};
w.isFragment = function(t) {
  return A(t) === le;
};
w.isLazy = function(t) {
  return A(t) === be;
};
w.isMemo = function(t) {
  return A(t) === pe;
};
w.isPortal = function(t) {
  return A(t) === Fe;
};
w.isProfiler = function(t) {
  return A(t) === ue;
};
w.isStrictMode = function(t) {
  return A(t) === ce;
};
w.isSuspense = function(t) {
  return A(t) === ge;
};
w.isSuspenseList = function(t) {
  return A(t) === me;
};
w.isValidElementType = function(t) {
  return typeof t == "string" || typeof t == "function" || t === le || t === ue || t === ce || t === ge || t === me || t === pn || typeof t == "object" && t !== null && (t.$$typeof === be || t.$$typeof === pe || t.$$typeof === fe || t.$$typeof === de || t.$$typeof === he || t.$$typeof === Lt || t.getModuleId !== void 0);
};
w.typeOf = A;
Number(or.split(".")[0]);
function bn(t, e) {
  if (J(t) != "object" || !t) return t;
  var n = t[Symbol.toPrimitive];
  if (n !== void 0) {
    var o = n.call(t, e);
    if (J(o) != "object") return o;
    throw new TypeError("@@toPrimitive must return a primitive value.");
  }
  return (e === "string" ? String : Number)(t);
}
function yn(t) {
  var e = bn(t, "string");
  return J(e) == "symbol" ? e : e + "";
}
function vn(t, e, n) {
  return (e = yn(e)) in t ? Object.defineProperty(t, e, {
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
function Sn(t) {
  for (var e = 1; e < arguments.length; e++) {
    var n = arguments[e] != null ? arguments[e] : {};
    e % 2 ? ft(Object(n), !0).forEach(function(o) {
      vn(t, o, n[o]);
    }) : Object.getOwnPropertyDescriptors ? Object.defineProperties(t, Object.getOwnPropertyDescriptors(n)) : ft(Object(n)).forEach(function(o) {
      Object.defineProperty(t, o, Object.getOwnPropertyDescriptor(n, o));
    });
  }
  return t;
}
function D(t) {
  "@babel/helpers - typeof";
  return D = typeof Symbol == "function" && typeof Symbol.iterator == "symbol" ? function(e) {
    return typeof e;
  } : function(e) {
    return e && typeof Symbol == "function" && e.constructor === Symbol && e !== Symbol.prototype ? "symbol" : typeof e;
  }, D(t);
}
function xn(t, e) {
  if (D(t) != "object" || !t) return t;
  var n = t[Symbol.toPrimitive];
  if (n !== void 0) {
    var o = n.call(t, e);
    if (D(o) != "object") return o;
    throw new TypeError("@@toPrimitive must return a primitive value.");
  }
  return (e === "string" ? String : Number)(t);
}
function Rt(t) {
  var e = xn(t, "string");
  return D(e) == "symbol" ? e : e + "";
}
function P(t, e, n) {
  return (e = Rt(e)) in t ? Object.defineProperty(t, e, {
    value: n,
    enumerable: !0,
    configurable: !0,
    writable: !0
  }) : t[e] = n, t;
}
function dt(t, e) {
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
    e % 2 ? dt(Object(n), !0).forEach(function(o) {
      P(t, o, n[o]);
    }) : Object.getOwnPropertyDescriptors ? Object.defineProperties(t, Object.getOwnPropertyDescriptors(n)) : dt(Object(n)).forEach(function(o) {
      Object.defineProperty(t, o, Object.getOwnPropertyDescriptor(n, o));
    });
  }
  return t;
}
function Cn(t) {
  if (Array.isArray(t)) return t;
}
function _n(t, e) {
  var n = t == null ? null : typeof Symbol < "u" && t[Symbol.iterator] || t["@@iterator"];
  if (n != null) {
    var o, r, i, s, a = [], l = !0, c = !1;
    try {
      if (i = (n = n.call(t)).next, e === 0) {
        if (Object(n) !== n) return;
        l = !1;
      } else for (; !(l = (o = i.call(n)).done) && (a.push(o.value), a.length !== e); l = !0) ;
    } catch (f) {
      c = !0, r = f;
    } finally {
      try {
        if (!l && n.return != null && (s = n.return(), Object(s) !== s)) return;
      } finally {
        if (c) throw r;
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
function wn(t, e) {
  if (t) {
    if (typeof t == "string") return ht(t, e);
    var n = {}.toString.call(t).slice(8, -1);
    return n === "Object" && t.constructor && (n = t.constructor.name), n === "Map" || n === "Set" ? Array.from(t) : n === "Arguments" || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n) ? ht(t, e) : void 0;
  }
}
function On() {
  throw new TypeError(`Invalid attempt to destructure non-iterable instance.
In order to be iterable, non-array objects must have a [Symbol.iterator]() method.`);
}
function ne(t, e) {
  return Cn(t) || _n(t, e) || wn(t, e) || On();
}
function ye(t, e) {
  if (!(t instanceof e)) throw new TypeError("Cannot call a class as a function");
}
function Pn(t, e) {
  for (var n = 0; n < e.length; n++) {
    var o = e[n];
    o.enumerable = o.enumerable || !1, o.configurable = !0, "value" in o && (o.writable = !0), Object.defineProperty(t, Rt(o.key), o);
  }
}
function ve(t, e, n) {
  return e && Pn(t.prototype, e), Object.defineProperty(t, "prototype", {
    writable: !1
  }), t;
}
function He(t, e) {
  return He = Object.setPrototypeOf ? Object.setPrototypeOf.bind() : function(n, o) {
    return n.__proto__ = o, n;
  }, He(t, e);
}
function $t(t, e) {
  if (typeof e != "function" && e !== null) throw new TypeError("Super expression must either be null or a function");
  t.prototype = Object.create(e && e.prototype, {
    constructor: {
      value: t,
      writable: !0,
      configurable: !0
    }
  }), Object.defineProperty(t, "prototype", {
    writable: !1
  }), e && He(t, e);
}
function se(t) {
  return se = Object.setPrototypeOf ? Object.getPrototypeOf.bind() : function(e) {
    return e.__proto__ || Object.getPrototypeOf(e);
  }, se(t);
}
function At() {
  try {
    var t = !Boolean.prototype.valueOf.call(Reflect.construct(Boolean, [], function() {
    }));
  } catch {
  }
  return (At = function() {
    return !!t;
  })();
}
function K(t) {
  if (t === void 0) throw new ReferenceError("this hasn't been initialised - super() hasn't been called");
  return t;
}
function Tn(t, e) {
  if (e && (D(e) == "object" || typeof e == "function")) return e;
  if (e !== void 0) throw new TypeError("Derived constructors may only return object or undefined");
  return K(t);
}
function Dt(t) {
  var e = At();
  return function() {
    var n, o = se(t);
    if (e) {
      var r = se(this).constructor;
      n = Reflect.construct(o, arguments, r);
    } else n = o.apply(this, arguments);
    return Tn(this, n);
  };
}
var Ht = /* @__PURE__ */ ve(function t() {
  ye(this, t);
}), zt = "CALC_UNIT", Mn = new RegExp(zt, "g");
function we(t) {
  return typeof t == "number" ? "".concat(t).concat(zt) : t;
}
var En = /* @__PURE__ */ function(t) {
  $t(n, t);
  var e = Dt(n);
  function n(o, r) {
    var i;
    ye(this, n), i = e.call(this), P(K(i), "result", ""), P(K(i), "unitlessCssVar", void 0), P(K(i), "lowPriority", void 0);
    var s = D(o);
    return i.unitlessCssVar = r, o instanceof n ? i.result = "(".concat(o.result, ")") : s === "number" ? i.result = we(o) : s === "string" && (i.result = o), i;
  }
  return ve(n, [{
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
      var i = this, s = r || {}, a = s.unit, l = !0;
      return typeof a == "boolean" ? l = a : Array.from(this.unitlessCssVar).some(function(c) {
        return i.result.includes(c);
      }) && (l = !1), this.result = this.result.replace(Mn, l ? "px" : ""), typeof this.lowPriority < "u" ? "calc(".concat(this.result, ")") : this.result;
    }
  }]), n;
}(Ht), jn = /* @__PURE__ */ function(t) {
  $t(n, t);
  var e = Dt(n);
  function n(o) {
    var r;
    return ye(this, n), r = e.call(this), P(K(r), "result", 0), o instanceof n ? r.result = o.result : typeof o == "number" && (r.result = o), r;
  }
  return ve(n, [{
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
}(Ht), In = function(e, n) {
  var o = e === "css" ? En : jn;
  return function(r) {
    return new o(r, n);
  };
}, gt = function(e, n) {
  return "".concat([n, e.replace(/([A-Z]+)([A-Z][a-z]+)/g, "$1-$2").replace(/([a-z])([A-Z])/g, "$1-$2")].filter(Boolean).join("-"));
};
function mt(t, e, n, o) {
  var r = L({}, e[t]);
  if (o != null && o.deprecatedTokens) {
    var i = o.deprecatedTokens;
    i.forEach(function(a) {
      var l = ne(a, 2), c = l[0], f = l[1];
      if (r != null && r[c] || r != null && r[f]) {
        var u;
        (u = r[f]) !== null && u !== void 0 || (r[f] = r == null ? void 0 : r[c]);
      }
    });
  }
  var s = L(L({}, n), r);
  return Object.keys(s).forEach(function(a) {
    s[a] === e[a] && delete s[a];
  }), s;
}
var Bt = typeof CSSINJS_STATISTIC < "u", ze = !0;
function Ve() {
  for (var t = arguments.length, e = new Array(t), n = 0; n < t; n++)
    e[n] = arguments[n];
  if (!Bt)
    return Object.assign.apply(Object, [{}].concat(e));
  ze = !1;
  var o = {};
  return e.forEach(function(r) {
    if (D(r) === "object") {
      var i = Object.keys(r);
      i.forEach(function(s) {
        Object.defineProperty(o, s, {
          configurable: !0,
          enumerable: !0,
          get: function() {
            return r[s];
          }
        });
      });
    }
  }), ze = !0, o;
}
var pt = {};
function kn() {
}
var Ln = function(e) {
  var n, o = e, r = kn;
  return Bt && typeof Proxy < "u" && (n = /* @__PURE__ */ new Set(), o = new Proxy(e, {
    get: function(s, a) {
      if (ze) {
        var l;
        (l = n) === null || l === void 0 || l.add(a);
      }
      return s[a];
    }
  }), r = function(s, a) {
    var l;
    pt[s] = {
      global: Array.from(n),
      component: L(L({}, (l = pt[s]) === null || l === void 0 ? void 0 : l.component), a)
    };
  }), {
    token: o,
    keys: n,
    flush: r
  };
};
function bt(t, e, n) {
  if (typeof n == "function") {
    var o;
    return n(Ve(e, (o = e[t]) !== null && o !== void 0 ? o : {}));
  }
  return n ?? {};
}
function Rn(t) {
  return t === "js" ? {
    max: Math.max,
    min: Math.min
  } : {
    max: function() {
      for (var n = arguments.length, o = new Array(n), r = 0; r < n; r++)
        o[r] = arguments[r];
      return "max(".concat(o.map(function(i) {
        return oe(i);
      }).join(","), ")");
    },
    min: function() {
      for (var n = arguments.length, o = new Array(n), r = 0; r < n; r++)
        o[r] = arguments[r];
      return "min(".concat(o.map(function(i) {
        return oe(i);
      }).join(","), ")");
    }
  };
}
var $n = 1e3 * 60 * 10, An = /* @__PURE__ */ function() {
  function t() {
    ye(this, t), P(this, "map", /* @__PURE__ */ new Map()), P(this, "objectIDMap", /* @__PURE__ */ new WeakMap()), P(this, "nextID", 0), P(this, "lastAccessBeat", /* @__PURE__ */ new Map()), P(this, "accessBeat", 0);
  }
  return ve(t, [{
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
      var o = this, r = n.map(function(i) {
        return i && D(i) === "object" ? "obj_".concat(o.getObjectID(i)) : "".concat(D(i), "_").concat(i);
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
        this.lastAccessBeat.forEach(function(r, i) {
          o - r > $n && (n.map.delete(i), n.lastAccessBeat.delete(i));
        }), this.accessBeat = 0;
      }
    }
  }]), t;
}(), yt = new An();
function Dn(t, e) {
  return S.useMemo(function() {
    var n = yt.get(e);
    if (n)
      return n;
    var o = t();
    return yt.set(e, o), o;
  }, e);
}
var Hn = function() {
  return {};
};
function zn(t) {
  var e = t.useCSP, n = e === void 0 ? Hn : e, o = t.useToken, r = t.usePrefix, i = t.getResetStyles, s = t.getCommonStyle, a = t.getCompUnitless;
  function l(d, g, b, y) {
    var h = Array.isArray(d) ? d[0] : d;
    function m(T) {
      return "".concat(String(h)).concat(T.slice(0, 1).toUpperCase()).concat(T.slice(1));
    }
    var x = (y == null ? void 0 : y.unitless) || {}, M = typeof a == "function" ? a(d) : {}, p = L(L({}, M), {}, P({}, m("zIndexPopup"), !0));
    Object.keys(x).forEach(function(T) {
      p[m(T)] = x[T];
    });
    var C = L(L({}, y), {}, {
      unitless: p,
      prefixToken: m
    }), v = f(d, g, b, C), O = c(h, b, C);
    return function(T) {
      var E = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : T, R = v(T, E), H = ne(R, 2), _ = H[1], z = O(E), k = ne(z, 2), $ = k[0], B = k[1];
      return [$, _, B];
    };
  }
  function c(d, g, b) {
    var y = b.unitless, h = b.injectStyle, m = h === void 0 ? !0 : h, x = b.prefixToken, M = b.ignore, p = function(O) {
      var T = O.rootCls, E = O.cssVar, R = E === void 0 ? {} : E, H = o(), _ = H.realToken;
      return dr({
        path: [d],
        prefix: R.prefix,
        key: R.key,
        unitless: y,
        ignore: M,
        token: _,
        scope: T
      }, function() {
        var z = bt(d, _, g), k = mt(d, _, z, {
          deprecatedTokens: b == null ? void 0 : b.deprecatedTokens
        });
        return Object.keys(z).forEach(function($) {
          k[x($)] = k[$], delete k[$];
        }), k;
      }), null;
    }, C = function(O) {
      var T = o(), E = T.cssVar;
      return [function(R) {
        return m && E ? /* @__PURE__ */ S.createElement(S.Fragment, null, /* @__PURE__ */ S.createElement(p, {
          rootCls: O,
          cssVar: E,
          component: d
        }), R) : R;
      }, E == null ? void 0 : E.key];
    };
    return C;
  }
  function f(d, g, b) {
    var y = arguments.length > 3 && arguments[3] !== void 0 ? arguments[3] : {}, h = Array.isArray(d) ? d : [d, d], m = ne(h, 1), x = m[0], M = h.join("-"), p = t.layer || {
      name: "antd"
    };
    return function(C) {
      var v = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : C, O = o(), T = O.theme, E = O.realToken, R = O.hashId, H = O.token, _ = O.cssVar, z = r(), k = z.rootPrefixCls, $ = z.iconPrefixCls, B = n(), U = _ ? "css" : "js", Ut = Dn(function() {
        var V = /* @__PURE__ */ new Set();
        return _ && Object.keys(y.unitless || {}).forEach(function(Z) {
          V.add(Se(Z, _.prefix)), V.add(Se(Z, gt(x, _.prefix)));
        }), In(U, V);
      }, [U, x, _ == null ? void 0 : _.prefix]), Ne = Rn(U), Wt = Ne.max, Kt = Ne.min, Ge = {
        theme: T,
        token: H,
        hashId: R,
        nonce: function() {
          return B.nonce;
        },
        clientOnly: y.clientOnly,
        layer: p,
        // antd is always at top of styles
        order: y.order || -999
      };
      typeof i == "function" && qe(L(L({}, Ge), {}, {
        clientOnly: !1,
        path: ["Shared", k]
      }), function() {
        return i(H, {
          prefix: {
            rootPrefixCls: k,
            iconPrefixCls: $
          },
          csp: B
        });
      });
      var qt = qe(L(L({}, Ge), {}, {
        path: [M, C, $]
      }), function() {
        if (y.injectStyle === !1)
          return [];
        var V = Ln(H), Z = V.token, Qt = V.flush, N = bt(x, E, b), Jt = ".".concat(C), Ue = mt(x, E, N, {
          deprecatedTokens: y.deprecatedTokens
        });
        _ && N && D(N) === "object" && Object.keys(N).forEach(function(Ke) {
          N[Ke] = "var(".concat(Se(Ke, gt(x, _.prefix)), ")");
        });
        var We = Ve(Z, {
          componentCls: Jt,
          prefixCls: C,
          iconCls: ".".concat($),
          antCls: ".".concat(k),
          calc: Ut,
          // @ts-ignore
          max: Wt,
          // @ts-ignore
          min: Kt
        }, _ ? N : Ue), Zt = g(We, {
          hashId: R,
          prefixCls: C,
          rootPrefixCls: k,
          iconPrefixCls: $
        });
        Qt(x, Ue);
        var Yt = typeof s == "function" ? s(We, C, v, y.resetFont) : null;
        return [y.resetStyle === !1 ? null : Yt, Zt];
      });
      return [qt, R];
    };
  }
  function u(d, g, b) {
    var y = arguments.length > 3 && arguments[3] !== void 0 ? arguments[3] : {}, h = f(d, g, b, L({
      resetStyle: !1,
      // Sub Style should default after root one
      order: -998
    }, y)), m = function(M) {
      var p = M.prefixCls, C = M.rootCls, v = C === void 0 ? p : C;
      return h(p, v), null;
    };
    return m;
  }
  return {
    genStyleHooks: l,
    genSubStyleComponent: u,
    genComponentStyleHook: f
  };
}
const j = Math.round;
function Oe(t, e) {
  const n = t.replace(/^[^(]*\((.*)/, "$1").replace(/\).*/, "").match(/\d*\.?\d+%?/g) || [], o = n.map((r) => parseFloat(r));
  for (let r = 0; r < 3; r += 1)
    o[r] = e(o[r] || 0, n[r] || "", r);
  return n[3] ? o[3] = n[3].includes("%") ? o[3] / 100 : o[3] : o[3] = 1, o;
}
const vt = (t, e, n) => n === 0 ? t : t / 100;
function W(t, e) {
  const n = e || 255;
  return t > n ? n : t < 0 ? 0 : t;
}
class X {
  constructor(e) {
    P(this, "isValid", !0), P(this, "r", 0), P(this, "g", 0), P(this, "b", 0), P(this, "a", 1), P(this, "_h", void 0), P(this, "_s", void 0), P(this, "_l", void 0), P(this, "_v", void 0), P(this, "_max", void 0), P(this, "_min", void 0), P(this, "_brightness", void 0);
    function n(o) {
      return o[0] in e && o[1] in e && o[2] in e;
    }
    if (e) if (typeof e == "string") {
      let r = function(i) {
        return o.startsWith(i);
      };
      const o = e.trim();
      /^#?[A-F\d]{3,8}$/i.test(o) ? this.fromHexString(o) : r("rgb") ? this.fromRgbString(o) : r("hsl") ? this.fromHslString(o) : (r("hsv") || r("hsb")) && this.fromHsvString(o);
    } else if (e instanceof X)
      this.r = e.r, this.g = e.g, this.b = e.b, this.a = e.a, this._h = e._h, this._s = e._s, this._l = e._l, this._v = e._v;
    else if (n("rgb"))
      this.r = W(e.r), this.g = W(e.g), this.b = W(e.b), this.a = typeof e.a == "number" ? W(e.a, 1) : 1;
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
    function e(i) {
      const s = i / 255;
      return s <= 0.03928 ? s / 12.92 : Math.pow((s + 0.055) / 1.055, 2.4);
    }
    const n = e(this.r), o = e(this.g), r = e(this.b);
    return 0.2126 * n + 0.7152 * o + 0.0722 * r;
  }
  getHue() {
    if (typeof this._h > "u") {
      const e = this.getMax() - this.getMin();
      e === 0 ? this._h = 0 : this._h = j(60 * (this.r === this.getMax() ? (this.g - this.b) / e + (this.g < this.b ? 6 : 0) : this.g === this.getMax() ? (this.b - this.r) / e + 2 : (this.r - this.g) / e + 4));
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
    const o = this._c(e), r = n / 100, i = (a) => (o[a] - this[a]) * r + this[a], s = {
      r: j(i("r")),
      g: j(i("g")),
      b: j(i("b")),
      a: j(i("a") * 100) / 100
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
    const n = this._c(e), o = this.a + n.a * (1 - this.a), r = (i) => j((this[i] * this.a + n[i] * n.a * (1 - this.a)) / o);
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
      const i = j(this.a * 255).toString(16);
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
    const e = this.getHue(), n = j(this.getSaturation() * 100), o = j(this.getLightness() * 100);
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
    return r[e] = W(n, o), r;
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
    function o(r, i) {
      return parseInt(n[r] + n[i || r], 16);
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
      const d = j(o * 255);
      this.r = d, this.g = d, this.b = d;
    }
    let i = 0, s = 0, a = 0;
    const l = e / 60, c = (1 - Math.abs(2 * o - 1)) * n, f = c * (1 - Math.abs(l % 2 - 1));
    l >= 0 && l < 1 ? (i = c, s = f) : l >= 1 && l < 2 ? (i = f, s = c) : l >= 2 && l < 3 ? (s = c, a = f) : l >= 3 && l < 4 ? (s = f, a = c) : l >= 4 && l < 5 ? (i = f, a = c) : l >= 5 && l < 6 && (i = c, a = f);
    const u = o - c / 2;
    this.r = j((i + u) * 255), this.g = j((s + u) * 255), this.b = j((a + u) * 255);
  }
  fromHsv({
    h: e,
    s: n,
    v: o,
    a: r
  }) {
    this._h = e % 360, this._s = n, this._v = o, this.a = typeof r == "number" ? r : 1;
    const i = j(o * 255);
    if (this.r = i, this.g = i, this.b = i, n <= 0)
      return;
    const s = e / 60, a = Math.floor(s), l = s - a, c = j(o * (1 - n) * 255), f = j(o * (1 - n * l) * 255), u = j(o * (1 - n * (1 - l)) * 255);
    switch (a) {
      case 0:
        this.g = u, this.b = c;
        break;
      case 1:
        this.r = f, this.b = c;
        break;
      case 2:
        this.r = c, this.b = u;
        break;
      case 3:
        this.r = c, this.g = f;
        break;
      case 4:
        this.r = u, this.g = c;
        break;
      case 5:
      default:
        this.g = c, this.b = f;
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
      r.includes("%") ? j(o / 100 * 255) : o
    ));
    this.r = n[0], this.g = n[1], this.b = n[2], this.a = n[3];
  }
}
const Bn = {
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
}, Xn = Object.assign(Object.assign({}, Bn), {
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
function Pe(t) {
  return t >= 0 && t <= 255;
}
function Y(t, e) {
  const {
    r: n,
    g: o,
    b: r,
    a: i
  } = new X(t).toRgb();
  if (i < 1)
    return t;
  const {
    r: s,
    g: a,
    b: l
  } = new X(e).toRgb();
  for (let c = 0.01; c <= 1; c += 0.01) {
    const f = Math.round((n - s * (1 - c)) / c), u = Math.round((o - a * (1 - c)) / c), d = Math.round((r - l * (1 - c)) / c);
    if (Pe(f) && Pe(u) && Pe(d))
      return new X({
        r: f,
        g: u,
        b: d,
        a: Math.round(c * 100) / 100
      }).toRgbString();
  }
  return new X({
    r: n,
    g: o,
    b: r,
    a: 1
  }).toRgbString();
}
var Fn = function(t, e) {
  var n = {};
  for (var o in t) Object.prototype.hasOwnProperty.call(t, o) && e.indexOf(o) < 0 && (n[o] = t[o]);
  if (t != null && typeof Object.getOwnPropertySymbols == "function") for (var r = 0, o = Object.getOwnPropertySymbols(t); r < o.length; r++)
    e.indexOf(o[r]) < 0 && Object.prototype.propertyIsEnumerable.call(t, o[r]) && (n[o[r]] = t[o[r]]);
  return n;
};
function Vn(t) {
  const {
    override: e
  } = t, n = Fn(t, ["override"]), o = Object.assign({}, e);
  Object.keys(Xn).forEach((d) => {
    delete o[d];
  });
  const r = Object.assign(Object.assign({}, n), o), i = 480, s = 576, a = 768, l = 992, c = 1200, f = 1600;
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
    screenXS: i,
    screenXSMin: i,
    screenXSMax: s - 1,
    screenSM: s,
    screenSMMin: s,
    screenSMMax: a - 1,
    screenMD: a,
    screenMDMin: a,
    screenMDMax: l - 1,
    screenLG: l,
    screenLGMin: l,
    screenLGMax: c - 1,
    screenXL: c,
    screenXLMin: c,
    screenXLMax: f - 1,
    screenXXL: f,
    screenXXLMin: f,
    boxShadowPopoverArrow: "2px 2px 5px rgba(0, 0, 0, 0.05)",
    boxShadowCard: `
      0 1px 2px -2px ${new X("rgba(0, 0, 0, 0.16)").toRgbString()},
      0 3px 6px 0 ${new X("rgba(0, 0, 0, 0.12)").toRgbString()},
      0 5px 12px 4px ${new X("rgba(0, 0, 0, 0.09)").toRgbString()}
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
const Nn = {
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
}, Gn = {
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
}, Un = hr(Le.defaultAlgorithm), Wn = {
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
}, Xt = (t, e, n) => {
  const o = n.getDerivativeToken(t), {
    override: r,
    ...i
  } = e;
  let s = {
    ...o,
    override: r
  };
  return s = Vn(s), i && Object.entries(i).forEach(([a, l]) => {
    const {
      theme: c,
      ...f
    } = l;
    let u = f;
    c && (u = Xt({
      ...s,
      ...f
    }, {
      override: f
    }, c)), s[a] = u;
  }), s;
};
function Kn() {
  const {
    token: t,
    hashed: e,
    theme: n = Un,
    override: o,
    cssVar: r
  } = S.useContext(Le._internalContext), [i, s, a] = gr(n, [Le.defaultSeed, t], {
    salt: `${nn}-${e || ""}`,
    override: o,
    getComputedToken: Xt,
    cssVar: r && {
      prefix: r.prefix,
      key: r.key,
      unitless: Nn,
      ignore: Gn,
      preserve: Wn
    }
  });
  return [n, a, e ? s : "", i, r];
}
const {
  genStyleHooks: qn
} = zn({
  usePrefix: () => {
    const {
      getPrefixCls: t,
      iconPrefixCls: e
    } = Ae();
    return {
      iconPrefixCls: e,
      rootPrefixCls: t()
    };
  },
  useToken: () => {
    const [t, e, n, o, r] = Kn();
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
    } = Ae();
    return t ?? {};
  },
  layer: {
    name: "antdx",
    dependencies: ["antd"]
  }
});
var Qn = `accept acceptCharset accessKey action allowFullScreen allowTransparency
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
    summary tabIndex target title type useMap value width wmode wrap`, Jn = `onCopy onCut onPaste onCompositionEnd onCompositionStart onCompositionUpdate onKeyDown
    onKeyPress onKeyUp onFocus onBlur onChange onInput onSubmit onClick onContextMenu onDoubleClick
    onDrag onDragEnd onDragEnter onDragExit onDragLeave onDragOver onDragStart onDrop onMouseDown
    onMouseEnter onMouseLeave onMouseMove onMouseOut onMouseOver onMouseUp onSelect onTouchCancel
    onTouchEnd onTouchMove onTouchStart onScroll onWheel onAbort onCanPlay onCanPlayThrough
    onDurationChange onEmptied onEncrypted onEnded onError onLoadedData onLoadedMetadata
    onLoadStart onPause onPlay onPlaying onProgress onRateChange onSeeked onSeeking onStalled onSuspend onTimeUpdate onVolumeChange onWaiting onLoad onError`, Zn = "".concat(Qn, " ").concat(Jn).split(/[\s\n]+/), Yn = "aria-", eo = "data-";
function St(t, e) {
  return t.indexOf(e) === 0;
}
function Ft(t) {
  var e = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : !1, n;
  e === !1 ? n = {
    aria: !0,
    data: !0,
    attr: !0
  } : e === !0 ? n = {
    aria: !0
  } : n = Sn({}, e);
  var o = {};
  return Object.keys(t).forEach(function(r) {
    // Aria
    (n.aria && (r === "role" || St(r, Yn)) || // Data
    n.data && St(r, eo) || // Attr
    n.attr && Zn.includes(r)) && (o[r] = t[r]);
  }), o;
}
const Vt = /* @__PURE__ */ S.createContext(null), xt = ({
  children: t
}) => {
  const {
    prefixCls: e
  } = S.useContext(Vt);
  return /* @__PURE__ */ S.createElement("div", {
    className: q(`${e}-group-title`)
  }, t && /* @__PURE__ */ S.createElement(Pt.Text, null, t));
}, to = (t) => {
  t.stopPropagation();
}, ro = (t) => {
  const {
    prefixCls: e,
    info: n,
    className: o,
    direction: r,
    onClick: i,
    active: s,
    menu: a,
    ...l
  } = t, c = Ft(l, {
    aria: !0,
    data: !0,
    attr: !0
  }), {
    disabled: f
  } = n, u = q(o, `${e}-item`, {
    [`${e}-item-active`]: s && !f
  }, {
    [`${e}-item-disabled`]: f
  }), d = () => {
    !f && i && i(n);
  }, {
    trigger: g,
    ...b
  } = a || {}, y = b == null ? void 0 : b.getPopupContainer, h = (m) => {
    const x = /* @__PURE__ */ S.createElement(fr, {
      onClick: to,
      className: `${e}-menu-icon`
    });
    return g ? typeof g == "function" ? g(m, {
      originNode: x
    }) : g : x;
  };
  return /* @__PURE__ */ S.createElement("li", ie({}, c, {
    className: u,
    onClick: d,
    title: `${n.label}`
  }), n.icon && /* @__PURE__ */ S.createElement("div", {
    className: `${e}-icon`
  }, n.icon), /* @__PURE__ */ S.createElement(Pt.Text, {
    className: `${e}-label`
  }, n.label), !f && a && /* @__PURE__ */ S.createElement(ur, {
    menu: b,
    placement: r === "rtl" ? "bottomLeft" : "bottomRight",
    trigger: ["click"],
    disabled: f,
    getPopupContainer: y
  }, h(n)));
}, Te = "__ungrouped", no = (t, e = []) => {
  const [n, o, r] = S.useMemo(() => {
    if (!t)
      return [!1, void 0, void 0];
    let i = {
      sort: void 0,
      title: void 0
    };
    return typeof t == "object" && (i = {
      ...i,
      ...t
    }), [!0, i.sort, i.title];
  }, [t]);
  return S.useMemo(() => {
    if (!n)
      return [[{
        name: Te,
        data: e,
        title: void 0
      }], n];
    const i = e.reduce((l, c) => {
      const f = c.group || Te;
      return l[f] || (l[f] = []), l[f].push(c), l;
    }, {});
    return [(o ? Object.keys(i).sort(o) : Object.keys(i)).map((l) => ({
      name: l === Te ? void 0 : l,
      title: r,
      data: i[l]
    })), n];
  }, [e, t]);
}, oo = (t) => {
  const {
    componentCls: e
  } = t;
  return {
    [e]: {
      display: "flex",
      flexDirection: "column",
      gap: t.paddingXXS,
      overflowY: "auto",
      padding: t.paddingSM,
      margin: 0,
      listStyle: "none",
      "ul, ol": {
        margin: 0,
        padding: 0,
        listStyle: "none"
      },
      [`&${e}-rtl`]: {
        direction: "rtl"
      },
      // 会话列表
      [`& ${e}-list`]: {
        display: "flex",
        gap: t.paddingXXS,
        flexDirection: "column",
        [`& ${e}-item`]: {
          paddingInlineStart: t.paddingXL
        },
        [`& ${e}-label`]: {
          color: t.colorTextDescription,
          overflow: "hidden",
          textOverflow: "ellipsis",
          whiteSpace: "nowrap"
        }
      },
      // 会话列表项
      [`& ${e}-item`]: {
        display: "flex",
        height: t.controlHeightLG,
        minHeight: t.controlHeightLG,
        gap: t.paddingXS,
        padding: `0 ${oe(t.paddingXS)}`,
        alignItems: "center",
        borderRadius: t.borderRadiusLG,
        cursor: "pointer",
        transition: `all ${t.motionDurationMid} ${t.motionEaseInOut}`,
        // 悬浮样式
        "&:hover": {
          backgroundColor: t.colorBgTextHover
        },
        // 选中样式
        "&-active": {
          backgroundColor: t.colorBgTextHover,
          [`& ${e}-label, ${e}-menu-icon`]: {
            color: t.colorText
          }
        },
        // 禁用样式
        "&-disabled": {
          cursor: "not-allowed",
          [`& ${e}-label`]: {
            color: t.colorTextDisabled
          }
        },
        // 悬浮、选中时激活操作菜单
        "&:hover, &-active": {
          [`& ${e}-menu-icon`]: {
            opacity: 0.6
          }
        },
        [`${e}-menu-icon:hover`]: {
          opacity: 1
        }
      },
      // 会话名
      [`& ${e}-label`]: {
        flex: 1,
        color: t.colorText
      },
      // 会话操作菜单
      [`& ${e}-menu-icon`]: {
        opacity: 0,
        fontSize: t.fontSizeXL
      },
      // 会话图标
      [`& ${e}-group-title`]: {
        display: "flex",
        alignItems: "center",
        height: t.controlHeightLG,
        minHeight: t.controlHeightLG,
        padding: `0 ${oe(t.paddingXS)}`
      }
    }
  };
}, io = () => ({}), so = qn("Conversations", (t) => {
  const e = Ve(t, {});
  return oo(e);
}, io), ao = (t) => {
  const {
    prefixCls: e,
    rootClassName: n,
    items: o,
    activeKey: r,
    defaultActiveKey: i,
    onActiveChange: s,
    menu: a,
    styles: l = {},
    classNames: c = {},
    groupable: f,
    className: u,
    style: d,
    ...g
  } = t, b = Ft(g, {
    attr: !0,
    aria: !0,
    data: !0
  }), [y, h] = gn(i, {
    value: r
  }), [m, x] = no(f, o), {
    getPrefixCls: M,
    direction: p
  } = Ae(), C = M("conversations", e), v = an("conversations"), [O, T, E] = so(C), R = q(C, v.className, u, n, T, E, {
    [`${C}-rtl`]: p === "rtl"
  }), H = (_) => {
    h(_.key), s && s(_.key);
  };
  return O(/* @__PURE__ */ S.createElement("ul", ie({}, b, {
    style: {
      ...v.style,
      ...d
    },
    className: R
  }), m.map((_, z) => {
    var $;
    const k = _.data.map((B, U) => /* @__PURE__ */ S.createElement(ro, {
      key: B.key || `key-${U}`,
      info: B,
      prefixCls: C,
      direction: p,
      className: q(c.item, v.classNames.item),
      style: {
        ...v.styles.item,
        ...l.item
      },
      menu: typeof a == "function" ? a(B) : a,
      active: y === B.key,
      onClick: H
    }));
    return x ? /* @__PURE__ */ S.createElement("li", {
      key: _.name || `key-${z}`
    }, /* @__PURE__ */ S.createElement(Vt.Provider, {
      value: {
        prefixCls: C
      }
    }, (($ = _.title) == null ? void 0 : $.call(_, _.name, {
      components: {
        GroupTitle: xt
      }
    })) || /* @__PURE__ */ S.createElement(xt, {
      key: _.name
    }, _.name)), /* @__PURE__ */ S.createElement("ul", {
      className: `${C}-list`
    }, k)) : k;
  })));
};
function lo(t) {
  return /^(?:async\s+)?(?:function\s*(?:\w*\s*)?\(|\([\w\s,=]*\)\s*=>|\(\{[\w\s,=]*\}\)\s*=>|function\s*\*\s*\w*\s*\()/i.test(t.trim());
}
function Nt(t, e = !1) {
  try {
    if (wt(t))
      return t;
    if (e && !lo(t))
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
function Ct(t, e) {
  return Ee(() => Nt(t, e), [t, e]);
}
const co = ({
  children: t,
  ...e
}) => /* @__PURE__ */ I.jsx(I.Fragment, {
  children: t(e)
});
function Gt(t) {
  return S.createElement(co, {
    children: t
  });
}
function Be(t, e, n) {
  const o = t.filter(Boolean);
  if (o.length !== 0)
    return o.map((r, i) => {
      var c;
      if (typeof r != "object")
        return e != null && e.fallback ? e.fallback(r) : r;
      const s = {
        ...r.props,
        key: ((c = r.props) == null ? void 0 : c.key) ?? (n ? `${n}-${i}` : `${i}`)
      };
      let a = s;
      Object.keys(r.slots).forEach((f) => {
        if (!r.slots[f] || !(r.slots[f] instanceof Element) && !r.slots[f].el)
          return;
        const u = f.split(".");
        u.forEach((m, x) => {
          a[m] || (a[m] = {}), x !== u.length - 1 && (a = s[m]);
        });
        const d = r.slots[f];
        let g, b, y = (e == null ? void 0 : e.clone) ?? !1, h = e == null ? void 0 : e.forceClone;
        d instanceof Element ? g = d : (g = d.el, b = d.callback, y = d.clone ?? y, h = d.forceClone ?? h), h = h ?? !!b, a[u[u.length - 1]] = g ? b ? (...m) => (b(u[u.length - 1], m), /* @__PURE__ */ I.jsx(ke, {
          ...r.ctx,
          params: m,
          forceClone: h,
          children: /* @__PURE__ */ I.jsx(Q, {
            slot: g,
            clone: y
          })
        })) : Gt((m) => /* @__PURE__ */ I.jsx(ke, {
          ...r.ctx,
          forceClone: h,
          children: /* @__PURE__ */ I.jsx(Q, {
            ...m,
            slot: g,
            clone: y
          })
        })) : a[u[u.length - 1]], a = s;
      });
      const l = (e == null ? void 0 : e.children) || "children";
      return r[l] ? s[l] = Be(r[l], e, `${i}`) : e != null && e.children && (s[l] = void 0, Reflect.deleteProperty(s, l)), s;
    });
}
function _t(t, e) {
  return t ? e != null && e.forceClone || e != null && e.params ? Gt((n) => /* @__PURE__ */ I.jsx(ke, {
    forceClone: e == null ? void 0 : e.forceClone,
    params: e == null ? void 0 : e.params,
    children: /* @__PURE__ */ I.jsx(Q, {
      slot: t,
      clone: e == null ? void 0 : e.clone,
      ...n
    })
  })) : /* @__PURE__ */ I.jsx(Q, {
    slot: t,
    clone: e == null ? void 0 : e.clone
  }) : null;
}
function Me({
  key: t,
  slots: e,
  targets: n
}, o) {
  return e[t] ? (...r) => n ? n.map((i, s) => /* @__PURE__ */ I.jsx(S.Fragment, {
    children: _t(i, {
      clone: !0,
      params: r,
      forceClone: (o == null ? void 0 : o.forceClone) ?? !0
    })
  }, s)) : /* @__PURE__ */ I.jsx(I.Fragment, {
    children: _t(e[t], {
      clone: !0,
      params: r,
      forceClone: (o == null ? void 0 : o.forceClone) ?? !0
    })
  }) : void 0;
}
const {
  useItems: uo,
  withItemsContextProvider: fo,
  ItemHandler: vo
} = Ot("antd-menu-items"), {
  useItems: ho,
  withItemsContextProvider: go,
  ItemHandler: So
} = Ot("antdx-conversations-items");
function mo(t) {
  return typeof t == "object" && t !== null ? t : {};
}
function po(t, e) {
  return Object.keys(t).reduce((n, o) => {
    if (o.startsWith("on") && wt(t[o])) {
      const r = t[o];
      o === "onClick" ? n[o] = (i, ...s) => {
        i.domEvent.stopPropagation(), r == null || r(e, i, ...s);
      } : n[o] = (...i) => {
        r == null || r(e, ...i);
      };
    } else
      n[o] = t[o];
    return n;
  }, {});
}
const xo = Zr(fo(["menu.items"], go(["default", "items"], ({
  slots: t,
  setSlotParams: e,
  children: n,
  items: o,
  ...r
}) => {
  var b;
  const {
    items: {
      "menu.items": i
    }
  } = uo(), s = Ct(r.menu), a = typeof r.groupable == "object" || t["groupable.title"], l = mo(r.groupable), c = Ct(r.groupable), f = Ee(() => {
    var y;
    if (typeof r.menu == "string")
      return s;
    {
      const h = r.menu || {};
      return ((y = h.items) == null ? void 0 : y.length) || i.length > 0 ? (x) => ({
        ...po(h, x),
        items: h.items || Be(i, {
          clone: !0
        }) || [],
        trigger: t["menu.trigger"] ? Me({
          slots: t,
          key: "menu.trigger"
        }, {}) : Nt(h.trigger, !0) || h.trigger,
        expandIcon: t["menu.expandIcon"] ? Me({
          slots: t,
          key: "menu.expandIcon"
        }, {}) : h.expandIcon,
        overflowedIndicator: t["menu.overflowedIndicator"] ? /* @__PURE__ */ I.jsx(Q, {
          slot: t["menu.overflowedIndicator"]
        }) : h.overflowedIndicator
      }) : void 0;
    }
  }, [s, i, r.menu, e, t]), {
    items: u
  } = ho(), d = u.items.length > 0 ? u.items : u.default, g = Ee(() => o || Be(d, {
    clone: !0
  }), [o, d]);
  return /* @__PURE__ */ I.jsxs(I.Fragment, {
    children: [/* @__PURE__ */ I.jsx("div", {
      style: {
        display: "none"
      },
      children: n
    }), /* @__PURE__ */ I.jsx(ao, {
      ...r,
      menu: f,
      classNames: {
        ...r.classNames,
        item: q((b = r.classNames) == null ? void 0 : b.item, "ms-gr-antdx-conversations-item")
      },
      items: g,
      groupable: a ? {
        ...l,
        title: t["groupable.title"] ? Me({
          slots: t,
          key: "groupable.title"
        }) : l.title,
        sort: c || l.sort
      } : r.groupable
    })]
  });
})));
export {
  xo as Conversations,
  xo as default
};
