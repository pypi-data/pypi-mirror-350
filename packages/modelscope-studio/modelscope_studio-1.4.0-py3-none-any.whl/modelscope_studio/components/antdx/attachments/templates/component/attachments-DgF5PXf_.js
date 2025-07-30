import { i as pn, a as Tt, r as mn, w as We, g as gn, d as hn, b as $e, c as oe, e as vn } from "./Index-DsTsc-eq.js";
const F = window.ms_globals.React, c = window.ms_globals.React, tt = window.ms_globals.React.useMemo, qe = window.ms_globals.React.useState, xe = window.ms_globals.React.useEffect, cn = window.ms_globals.React.forwardRef, be = window.ms_globals.React.useRef, un = window.ms_globals.React.version, fn = window.ms_globals.React.isValidElement, dn = window.ms_globals.React.useLayoutEffect, Wt = window.ms_globals.ReactDOM, Ze = window.ms_globals.ReactDOM.createPortal, yn = window.ms_globals.internalContext.useContextPropsContext, bn = window.ms_globals.internalContext.ContextPropsProvider, Sn = window.ms_globals.antd.ConfigProvider, Tr = window.ms_globals.antd.Upload, Qe = window.ms_globals.antd.theme, wn = window.ms_globals.antd.Progress, xn = window.ms_globals.antd.Image, ht = window.ms_globals.antd.Button, En = window.ms_globals.antd.Flex, vt = window.ms_globals.antd.Typography, Cn = window.ms_globals.antdIcons.FileTextFilled, _n = window.ms_globals.antdIcons.CloseCircleFilled, Ln = window.ms_globals.antdIcons.FileExcelFilled, Rn = window.ms_globals.antdIcons.FileImageFilled, In = window.ms_globals.antdIcons.FileMarkdownFilled, Tn = window.ms_globals.antdIcons.FilePdfFilled, Pn = window.ms_globals.antdIcons.FilePptFilled, Mn = window.ms_globals.antdIcons.FileWordFilled, On = window.ms_globals.antdIcons.FileZipFilled, Fn = window.ms_globals.antdIcons.PlusOutlined, An = window.ms_globals.antdIcons.LeftOutlined, $n = window.ms_globals.antdIcons.RightOutlined, Gt = window.ms_globals.antdCssinjs.unit, yt = window.ms_globals.antdCssinjs.token2CSSVar, Kt = window.ms_globals.antdCssinjs.useStyleRegister, kn = window.ms_globals.antdCssinjs.useCSSVarRegister, jn = window.ms_globals.antdCssinjs.createTheme, Dn = window.ms_globals.antdCssinjs.useCacheToken;
var Nn = /\s/;
function zn(e) {
  for (var t = e.length; t-- && Nn.test(e.charAt(t)); )
    ;
  return t;
}
var Hn = /^\s+/;
function Un(e) {
  return e && e.slice(0, zn(e) + 1).replace(Hn, "");
}
var qt = NaN, Bn = /^[-+]0x[0-9a-f]+$/i, Vn = /^0b[01]+$/i, Xn = /^0o[0-7]+$/i, Wn = parseInt;
function Zt(e) {
  if (typeof e == "number")
    return e;
  if (pn(e))
    return qt;
  if (Tt(e)) {
    var t = typeof e.valueOf == "function" ? e.valueOf() : e;
    e = Tt(t) ? t + "" : t;
  }
  if (typeof e != "string")
    return e === 0 ? e : +e;
  e = Un(e);
  var r = Vn.test(e);
  return r || Xn.test(e) ? Wn(e.slice(2), r ? 2 : 8) : Bn.test(e) ? qt : +e;
}
function Gn() {
}
var bt = function() {
  return mn.Date.now();
}, Kn = "Expected a function", qn = Math.max, Zn = Math.min;
function Qn(e, t, r) {
  var o, n, i, s, a, l, u = 0, p = !1, f = !1, d = !0;
  if (typeof e != "function")
    throw new TypeError(Kn);
  t = Zt(t) || 0, Tt(r) && (p = !!r.leading, f = "maxWait" in r, i = f ? qn(Zt(r.maxWait) || 0, t) : i, d = "trailing" in r ? !!r.trailing : d);
  function m(v) {
    var L = o, S = n;
    return o = n = void 0, u = v, s = e.apply(S, L), s;
  }
  function b(v) {
    return u = v, a = setTimeout(y, t), p ? m(v) : s;
  }
  function w(v) {
    var L = v - l, S = v - u, T = t - L;
    return f ? Zn(T, i - S) : T;
  }
  function g(v) {
    var L = v - l, S = v - u;
    return l === void 0 || L >= t || L < 0 || f && S >= i;
  }
  function y() {
    var v = bt();
    if (g(v))
      return E(v);
    a = setTimeout(y, w(v));
  }
  function E(v) {
    return a = void 0, d && o ? m(v) : (o = n = void 0, s);
  }
  function C() {
    a !== void 0 && clearTimeout(a), u = 0, o = l = n = a = void 0;
  }
  function h() {
    return a === void 0 ? s : E(bt());
  }
  function x() {
    var v = bt(), L = g(v);
    if (o = arguments, n = this, l = v, L) {
      if (a === void 0)
        return b(l);
      if (f)
        return clearTimeout(a), a = setTimeout(y, t), m(l);
    }
    return a === void 0 && (a = setTimeout(y, t)), s;
  }
  return x.cancel = C, x.flush = h, x;
}
var Pr = {
  exports: {}
}, rt = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var Yn = c, Jn = Symbol.for("react.element"), eo = Symbol.for("react.fragment"), to = Object.prototype.hasOwnProperty, ro = Yn.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, no = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function Mr(e, t, r) {
  var o, n = {}, i = null, s = null;
  r !== void 0 && (i = "" + r), t.key !== void 0 && (i = "" + t.key), t.ref !== void 0 && (s = t.ref);
  for (o in t) to.call(t, o) && !no.hasOwnProperty(o) && (n[o] = t[o]);
  if (e && e.defaultProps) for (o in t = e.defaultProps, t) n[o] === void 0 && (n[o] = t[o]);
  return {
    $$typeof: Jn,
    type: e,
    key: i,
    ref: s,
    props: n,
    _owner: ro.current
  };
}
rt.Fragment = eo;
rt.jsx = Mr;
rt.jsxs = Mr;
Pr.exports = rt;
var Y = Pr.exports;
const {
  SvelteComponent: oo,
  assign: Qt,
  binding_callbacks: Yt,
  check_outros: io,
  children: Or,
  claim_element: Fr,
  claim_space: so,
  component_subscribe: Jt,
  compute_slots: ao,
  create_slot: lo,
  detach: Le,
  element: Ar,
  empty: er,
  exclude_internal_props: tr,
  get_all_dirty_from_scope: co,
  get_slot_changes: uo,
  group_outros: fo,
  init: po,
  insert_hydration: Ge,
  safe_not_equal: mo,
  set_custom_element_data: $r,
  space: go,
  transition_in: Ke,
  transition_out: Pt,
  update_slot_base: ho
} = window.__gradio__svelte__internal, {
  beforeUpdate: vo,
  getContext: yo,
  onDestroy: bo,
  setContext: So
} = window.__gradio__svelte__internal;
function rr(e) {
  let t, r;
  const o = (
    /*#slots*/
    e[7].default
  ), n = lo(
    o,
    e,
    /*$$scope*/
    e[6],
    null
  );
  return {
    c() {
      t = Ar("svelte-slot"), n && n.c(), this.h();
    },
    l(i) {
      t = Fr(i, "SVELTE-SLOT", {
        class: !0
      });
      var s = Or(t);
      n && n.l(s), s.forEach(Le), this.h();
    },
    h() {
      $r(t, "class", "svelte-1rt0kpf");
    },
    m(i, s) {
      Ge(i, t, s), n && n.m(t, null), e[9](t), r = !0;
    },
    p(i, s) {
      n && n.p && (!r || s & /*$$scope*/
      64) && ho(
        n,
        o,
        i,
        /*$$scope*/
        i[6],
        r ? uo(
          o,
          /*$$scope*/
          i[6],
          s,
          null
        ) : co(
          /*$$scope*/
          i[6]
        ),
        null
      );
    },
    i(i) {
      r || (Ke(n, i), r = !0);
    },
    o(i) {
      Pt(n, i), r = !1;
    },
    d(i) {
      i && Le(t), n && n.d(i), e[9](null);
    }
  };
}
function wo(e) {
  let t, r, o, n, i = (
    /*$$slots*/
    e[4].default && rr(e)
  );
  return {
    c() {
      t = Ar("react-portal-target"), r = go(), i && i.c(), o = er(), this.h();
    },
    l(s) {
      t = Fr(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), Or(t).forEach(Le), r = so(s), i && i.l(s), o = er(), this.h();
    },
    h() {
      $r(t, "class", "svelte-1rt0kpf");
    },
    m(s, a) {
      Ge(s, t, a), e[8](t), Ge(s, r, a), i && i.m(s, a), Ge(s, o, a), n = !0;
    },
    p(s, [a]) {
      /*$$slots*/
      s[4].default ? i ? (i.p(s, a), a & /*$$slots*/
      16 && Ke(i, 1)) : (i = rr(s), i.c(), Ke(i, 1), i.m(o.parentNode, o)) : i && (fo(), Pt(i, 1, 1, () => {
        i = null;
      }), io());
    },
    i(s) {
      n || (Ke(i), n = !0);
    },
    o(s) {
      Pt(i), n = !1;
    },
    d(s) {
      s && (Le(t), Le(r), Le(o)), e[8](null), i && i.d(s);
    }
  };
}
function nr(e) {
  const {
    svelteInit: t,
    ...r
  } = e;
  return r;
}
function xo(e, t, r) {
  let o, n, {
    $$slots: i = {},
    $$scope: s
  } = t;
  const a = ao(i);
  let {
    svelteInit: l
  } = t;
  const u = We(nr(t)), p = We();
  Jt(e, p, (h) => r(0, o = h));
  const f = We();
  Jt(e, f, (h) => r(1, n = h));
  const d = [], m = yo("$$ms-gr-react-wrapper"), {
    slotKey: b,
    slotIndex: w,
    subSlotIndex: g
  } = gn() || {}, y = l({
    parent: m,
    props: u,
    target: p,
    slot: f,
    slotKey: b,
    slotIndex: w,
    subSlotIndex: g,
    onDestroy(h) {
      d.push(h);
    }
  });
  So("$$ms-gr-react-wrapper", y), vo(() => {
    u.set(nr(t));
  }), bo(() => {
    d.forEach((h) => h());
  });
  function E(h) {
    Yt[h ? "unshift" : "push"](() => {
      o = h, p.set(o);
    });
  }
  function C(h) {
    Yt[h ? "unshift" : "push"](() => {
      n = h, f.set(n);
    });
  }
  return e.$$set = (h) => {
    r(17, t = Qt(Qt({}, t), tr(h))), "svelteInit" in h && r(5, l = h.svelteInit), "$$scope" in h && r(6, s = h.$$scope);
  }, t = tr(t), [o, n, p, f, a, l, s, i, E, C];
}
class Eo extends oo {
  constructor(t) {
    super(), po(this, t, xo, wo, mo, {
      svelteInit: 5
    });
  }
}
const {
  SvelteComponent: ws
} = window.__gradio__svelte__internal, or = window.ms_globals.rerender, St = window.ms_globals.tree;
function Co(e, t = {}) {
  function r(o) {
    const n = We(), i = new Eo({
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
          }, l = s.parent ?? St;
          return l.nodes = [...l.nodes, a], or({
            createPortal: Ze,
            node: St
          }), s.onDestroy(() => {
            l.nodes = l.nodes.filter((u) => u.svelteInstance !== n), or({
              createPortal: Ze,
              node: St
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
function _o(e) {
  const [t, r] = qe(() => $e(e));
  return xe(() => {
    let o = !0;
    return e.subscribe((i) => {
      o && (o = !1, i === t) || r(i);
    });
  }, [e]), t;
}
function Lo(e) {
  const t = tt(() => hn(e, (r) => r), [e]);
  return _o(t);
}
const Ro = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Io(e) {
  return e ? Object.keys(e).reduce((t, r) => {
    const o = e[r];
    return t[r] = To(r, o), t;
  }, {}) : {};
}
function To(e, t) {
  return typeof t == "number" && !Ro.includes(e) ? t + "px" : t;
}
function Mt(e) {
  const t = [], r = e.cloneNode(!1);
  if (e._reactElement) {
    const n = c.Children.toArray(e._reactElement.props.children).map((i) => {
      if (c.isValidElement(i) && i.props.__slot__) {
        const {
          portals: s,
          clonedElement: a
        } = Mt(i.props.el);
        return c.cloneElement(i, {
          ...i.props,
          el: a,
          children: [...c.Children.toArray(i.props.children), ...s]
        });
      }
      return null;
    });
    return n.originalChildren = e._reactElement.props.children, t.push(Ze(c.cloneElement(e._reactElement, {
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
      useCapture: l
    }) => {
      r.addEventListener(a, s, l);
    });
  });
  const o = Array.from(e.childNodes);
  for (let n = 0; n < o.length; n++) {
    const i = o[n];
    if (i.nodeType === 1) {
      const {
        clonedElement: s,
        portals: a
      } = Mt(i);
      t.push(...a), r.appendChild(s);
    } else i.nodeType === 3 && r.appendChild(i.cloneNode());
  }
  return {
    clonedElement: r,
    portals: t
  };
}
function Po(e, t) {
  e && (typeof e == "function" ? e(t) : e.current = t);
}
const ke = cn(({
  slot: e,
  clone: t,
  className: r,
  style: o,
  observeAttributes: n
}, i) => {
  const s = be(), [a, l] = qe([]), {
    forceClone: u
  } = yn(), p = u ? !0 : t;
  return xe(() => {
    var w;
    if (!s.current || !e)
      return;
    let f = e;
    function d() {
      let g = f;
      if (f.tagName.toLowerCase() === "svelte-slot" && f.children.length === 1 && f.children[0] && (g = f.children[0], g.tagName.toLowerCase() === "react-portal-target" && g.children[0] && (g = g.children[0])), Po(i, g), r && g.classList.add(...r.split(" ")), o) {
        const y = Io(o);
        Object.keys(y).forEach((E) => {
          g.style[E] = y[E];
        });
      }
    }
    let m = null, b = null;
    if (p && window.MutationObserver) {
      let g = function() {
        var h, x, v;
        (h = s.current) != null && h.contains(f) && ((x = s.current) == null || x.removeChild(f));
        const {
          portals: E,
          clonedElement: C
        } = Mt(e);
        f = C, l(E), f.style.display = "contents", b && clearTimeout(b), b = setTimeout(() => {
          d();
        }, 50), (v = s.current) == null || v.appendChild(f);
      };
      g();
      const y = Qn(() => {
        g(), m == null || m.disconnect(), m == null || m.observe(e, {
          childList: !0,
          subtree: !0,
          attributes: n
        });
      }, 50);
      m = new window.MutationObserver(y), m.observe(e, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      f.style.display = "contents", d(), (w = s.current) == null || w.appendChild(f);
    return () => {
      var g, y;
      f.style.display = "", (g = s.current) != null && g.contains(f) && ((y = s.current) == null || y.removeChild(f)), m == null || m.disconnect();
    };
  }, [e, p, r, o, i, n, u]), c.createElement("react-child", {
    ref: s,
    style: {
      display: "contents"
    }
  }, ...a);
}), Mo = "1.3.0", Oo = /* @__PURE__ */ c.createContext({}), Fo = {
  classNames: {},
  styles: {},
  className: "",
  style: {}
}, Ao = (e) => {
  const t = c.useContext(Oo);
  return c.useMemo(() => ({
    ...Fo,
    ...t[e]
  }), [t[e]]);
};
function Te() {
  return Te = Object.assign ? Object.assign.bind() : function(e) {
    for (var t = 1; t < arguments.length; t++) {
      var r = arguments[t];
      for (var o in r) ({}).hasOwnProperty.call(r, o) && (e[o] = r[o]);
    }
    return e;
  }, Te.apply(null, arguments);
}
function Ye() {
  const {
    getPrefixCls: e,
    direction: t,
    csp: r,
    iconPrefixCls: o,
    theme: n
  } = c.useContext(Sn.ConfigContext);
  return {
    theme: n,
    getPrefixCls: e,
    direction: t,
    csp: r,
    iconPrefixCls: o
  };
}
function Pe(e) {
  var t = F.useRef();
  t.current = e;
  var r = F.useCallback(function() {
    for (var o, n = arguments.length, i = new Array(n), s = 0; s < n; s++)
      i[s] = arguments[s];
    return (o = t.current) === null || o === void 0 ? void 0 : o.call.apply(o, [t].concat(i));
  }, []);
  return r;
}
function $o(e) {
  if (Array.isArray(e)) return e;
}
function ko(e, t) {
  var r = e == null ? null : typeof Symbol < "u" && e[Symbol.iterator] || e["@@iterator"];
  if (r != null) {
    var o, n, i, s, a = [], l = !0, u = !1;
    try {
      if (i = (r = r.call(e)).next, t !== 0) for (; !(l = (o = i.call(r)).done) && (a.push(o.value), a.length !== t); l = !0) ;
    } catch (p) {
      u = !0, n = p;
    } finally {
      try {
        if (!l && r.return != null && (s = r.return(), Object(s) !== s)) return;
      } finally {
        if (u) throw n;
      }
    }
    return a;
  }
}
function ir(e, t) {
  (t == null || t > e.length) && (t = e.length);
  for (var r = 0, o = Array(t); r < t; r++) o[r] = e[r];
  return o;
}
function jo(e, t) {
  if (e) {
    if (typeof e == "string") return ir(e, t);
    var r = {}.toString.call(e).slice(8, -1);
    return r === "Object" && e.constructor && (r = e.constructor.name), r === "Map" || r === "Set" ? Array.from(e) : r === "Arguments" || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r) ? ir(e, t) : void 0;
  }
}
function Do() {
  throw new TypeError(`Invalid attempt to destructure non-iterable instance.
In order to be iterable, non-array objects must have a [Symbol.iterator]() method.`);
}
function Je(e, t) {
  return $o(e) || ko(e, t) || jo(e, t) || Do();
}
function nt() {
  return !!(typeof window < "u" && window.document && window.document.createElement);
}
var sr = nt() ? F.useLayoutEffect : F.useEffect, No = function(t, r) {
  var o = F.useRef(!0);
  sr(function() {
    return t(o.current);
  }, r), sr(function() {
    return o.current = !1, function() {
      o.current = !0;
    };
  }, []);
}, ar = function(t, r) {
  No(function(o) {
    if (!o)
      return t();
  }, r);
};
function je(e) {
  var t = F.useRef(!1), r = F.useState(e), o = Je(r, 2), n = o[0], i = o[1];
  F.useEffect(function() {
    return t.current = !1, function() {
      t.current = !0;
    };
  }, []);
  function s(a, l) {
    l && t.current || i(a);
  }
  return [n, s];
}
function wt(e) {
  return e !== void 0;
}
function zo(e, t) {
  var r = t || {}, o = r.defaultValue, n = r.value, i = r.onChange, s = r.postState, a = je(function() {
    return wt(n) ? n : wt(o) ? typeof o == "function" ? o() : o : typeof e == "function" ? e() : e;
  }), l = Je(a, 2), u = l[0], p = l[1], f = n !== void 0 ? n : u, d = s ? s(f) : f, m = Pe(i), b = je([f]), w = Je(b, 2), g = w[0], y = w[1];
  ar(function() {
    var C = g[0];
    u !== C && m(u, C);
  }, [g]), ar(function() {
    wt(n) || p(n);
  }, [n]);
  var E = Pe(function(C, h) {
    p(C, h), y([f], h);
  });
  return [d, E];
}
function De(e) {
  "@babel/helpers - typeof";
  return De = typeof Symbol == "function" && typeof Symbol.iterator == "symbol" ? function(t) {
    return typeof t;
  } : function(t) {
    return t && typeof Symbol == "function" && t.constructor === Symbol && t !== Symbol.prototype ? "symbol" : typeof t;
  }, De(e);
}
var kr = {
  exports: {}
}, A = {};
/**
 * @license React
 * react-is.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var Ht = Symbol.for("react.element"), Ut = Symbol.for("react.portal"), ot = Symbol.for("react.fragment"), it = Symbol.for("react.strict_mode"), st = Symbol.for("react.profiler"), at = Symbol.for("react.provider"), lt = Symbol.for("react.context"), Ho = Symbol.for("react.server_context"), ct = Symbol.for("react.forward_ref"), ut = Symbol.for("react.suspense"), ft = Symbol.for("react.suspense_list"), dt = Symbol.for("react.memo"), pt = Symbol.for("react.lazy"), Uo = Symbol.for("react.offscreen"), jr;
jr = Symbol.for("react.module.reference");
function se(e) {
  if (typeof e == "object" && e !== null) {
    var t = e.$$typeof;
    switch (t) {
      case Ht:
        switch (e = e.type, e) {
          case ot:
          case st:
          case it:
          case ut:
          case ft:
            return e;
          default:
            switch (e = e && e.$$typeof, e) {
              case Ho:
              case lt:
              case ct:
              case pt:
              case dt:
              case at:
                return e;
              default:
                return t;
            }
        }
      case Ut:
        return t;
    }
  }
}
A.ContextConsumer = lt;
A.ContextProvider = at;
A.Element = Ht;
A.ForwardRef = ct;
A.Fragment = ot;
A.Lazy = pt;
A.Memo = dt;
A.Portal = Ut;
A.Profiler = st;
A.StrictMode = it;
A.Suspense = ut;
A.SuspenseList = ft;
A.isAsyncMode = function() {
  return !1;
};
A.isConcurrentMode = function() {
  return !1;
};
A.isContextConsumer = function(e) {
  return se(e) === lt;
};
A.isContextProvider = function(e) {
  return se(e) === at;
};
A.isElement = function(e) {
  return typeof e == "object" && e !== null && e.$$typeof === Ht;
};
A.isForwardRef = function(e) {
  return se(e) === ct;
};
A.isFragment = function(e) {
  return se(e) === ot;
};
A.isLazy = function(e) {
  return se(e) === pt;
};
A.isMemo = function(e) {
  return se(e) === dt;
};
A.isPortal = function(e) {
  return se(e) === Ut;
};
A.isProfiler = function(e) {
  return se(e) === st;
};
A.isStrictMode = function(e) {
  return se(e) === it;
};
A.isSuspense = function(e) {
  return se(e) === ut;
};
A.isSuspenseList = function(e) {
  return se(e) === ft;
};
A.isValidElementType = function(e) {
  return typeof e == "string" || typeof e == "function" || e === ot || e === st || e === it || e === ut || e === ft || e === Uo || typeof e == "object" && e !== null && (e.$$typeof === pt || e.$$typeof === dt || e.$$typeof === at || e.$$typeof === lt || e.$$typeof === ct || e.$$typeof === jr || e.getModuleId !== void 0);
};
A.typeOf = se;
kr.exports = A;
var xt = kr.exports, Bo = Symbol.for("react.element"), Vo = Symbol.for("react.transitional.element"), Xo = Symbol.for("react.fragment");
function Wo(e) {
  return (
    // Base object type
    e && De(e) === "object" && // React Element type
    (e.$$typeof === Bo || e.$$typeof === Vo) && // React Fragment type
    e.type === Xo
  );
}
var Go = Number(un.split(".")[0]), Ko = function(t, r) {
  typeof t == "function" ? t(r) : De(t) === "object" && t && "current" in t && (t.current = r);
}, qo = function(t) {
  var r, o;
  if (!t)
    return !1;
  if (Dr(t) && Go >= 19)
    return !0;
  var n = xt.isMemo(t) ? t.type.type : t.type;
  return !(typeof n == "function" && !((r = n.prototype) !== null && r !== void 0 && r.render) && n.$$typeof !== xt.ForwardRef || typeof t == "function" && !((o = t.prototype) !== null && o !== void 0 && o.render) && t.$$typeof !== xt.ForwardRef);
};
function Dr(e) {
  return /* @__PURE__ */ fn(e) && !Wo(e);
}
var Zo = function(t) {
  if (t && Dr(t)) {
    var r = t;
    return r.props.propertyIsEnumerable("ref") ? r.props.ref : r.ref;
  }
  return null;
};
const Ne = /* @__PURE__ */ c.createContext(null);
function lr(e) {
  const {
    getDropContainer: t,
    className: r,
    prefixCls: o,
    children: n
  } = e, {
    disabled: i
  } = c.useContext(Ne), [s, a] = c.useState(), [l, u] = c.useState(null);
  if (c.useEffect(() => {
    const d = t == null ? void 0 : t();
    s !== d && a(d);
  }, [t]), c.useEffect(() => {
    if (s) {
      const d = () => {
        u(!0);
      }, m = (g) => {
        g.preventDefault();
      }, b = (g) => {
        g.relatedTarget || u(!1);
      }, w = (g) => {
        u(!1), g.preventDefault();
      };
      return document.addEventListener("dragenter", d), document.addEventListener("dragover", m), document.addEventListener("dragleave", b), document.addEventListener("drop", w), () => {
        document.removeEventListener("dragenter", d), document.removeEventListener("dragover", m), document.removeEventListener("dragleave", b), document.removeEventListener("drop", w);
      };
    }
  }, [!!s]), !(t && s && !i))
    return null;
  const f = `${o}-drop-area`;
  return /* @__PURE__ */ Ze(/* @__PURE__ */ c.createElement("div", {
    className: oe(f, r, {
      [`${f}-on-body`]: s.tagName === "BODY"
    }),
    style: {
      display: l ? "block" : "none"
    }
  }, n), s);
}
function ee(e) {
  "@babel/helpers - typeof";
  return ee = typeof Symbol == "function" && typeof Symbol.iterator == "symbol" ? function(t) {
    return typeof t;
  } : function(t) {
    return t && typeof Symbol == "function" && t.constructor === Symbol && t !== Symbol.prototype ? "symbol" : typeof t;
  }, ee(e);
}
function Qo(e, t) {
  if (ee(e) != "object" || !e) return e;
  var r = e[Symbol.toPrimitive];
  if (r !== void 0) {
    var o = r.call(e, t);
    if (ee(o) != "object") return o;
    throw new TypeError("@@toPrimitive must return a primitive value.");
  }
  return (t === "string" ? String : Number)(e);
}
function Nr(e) {
  var t = Qo(e, "string");
  return ee(t) == "symbol" ? t : t + "";
}
function I(e, t, r) {
  return (t = Nr(t)) in e ? Object.defineProperty(e, t, {
    value: r,
    enumerable: !0,
    configurable: !0,
    writable: !0
  }) : e[t] = r, e;
}
function cr(e, t) {
  var r = Object.keys(e);
  if (Object.getOwnPropertySymbols) {
    var o = Object.getOwnPropertySymbols(e);
    t && (o = o.filter(function(n) {
      return Object.getOwnPropertyDescriptor(e, n).enumerable;
    })), r.push.apply(r, o);
  }
  return r;
}
function R(e) {
  for (var t = 1; t < arguments.length; t++) {
    var r = arguments[t] != null ? arguments[t] : {};
    t % 2 ? cr(Object(r), !0).forEach(function(o) {
      I(e, o, r[o]);
    }) : Object.getOwnPropertyDescriptors ? Object.defineProperties(e, Object.getOwnPropertyDescriptors(r)) : cr(Object(r)).forEach(function(o) {
      Object.defineProperty(e, o, Object.getOwnPropertyDescriptor(r, o));
    });
  }
  return e;
}
function Yo(e) {
  if (Array.isArray(e)) return e;
}
function Jo(e, t) {
  var r = e == null ? null : typeof Symbol < "u" && e[Symbol.iterator] || e["@@iterator"];
  if (r != null) {
    var o, n, i, s, a = [], l = !0, u = !1;
    try {
      if (i = (r = r.call(e)).next, t === 0) {
        if (Object(r) !== r) return;
        l = !1;
      } else for (; !(l = (o = i.call(r)).done) && (a.push(o.value), a.length !== t); l = !0) ;
    } catch (p) {
      u = !0, n = p;
    } finally {
      try {
        if (!l && r.return != null && (s = r.return(), Object(s) !== s)) return;
      } finally {
        if (u) throw n;
      }
    }
    return a;
  }
}
function ur(e, t) {
  (t == null || t > e.length) && (t = e.length);
  for (var r = 0, o = Array(t); r < t; r++) o[r] = e[r];
  return o;
}
function ei(e, t) {
  if (e) {
    if (typeof e == "string") return ur(e, t);
    var r = {}.toString.call(e).slice(8, -1);
    return r === "Object" && e.constructor && (r = e.constructor.name), r === "Map" || r === "Set" ? Array.from(e) : r === "Arguments" || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r) ? ur(e, t) : void 0;
  }
}
function ti() {
  throw new TypeError(`Invalid attempt to destructure non-iterable instance.
In order to be iterable, non-array objects must have a [Symbol.iterator]() method.`);
}
function ie(e, t) {
  return Yo(e) || Jo(e, t) || ei(e, t) || ti();
}
function fr(e) {
  return e instanceof HTMLElement || e instanceof SVGElement;
}
function ri(e) {
  return e && De(e) === "object" && fr(e.nativeElement) ? e.nativeElement : fr(e) ? e : null;
}
function ni(e) {
  var t = ri(e);
  if (t)
    return t;
  if (e instanceof c.Component) {
    var r;
    return (r = Wt.findDOMNode) === null || r === void 0 ? void 0 : r.call(Wt, e);
  }
  return null;
}
function oi(e, t) {
  if (e == null) return {};
  var r = {};
  for (var o in e) if ({}.hasOwnProperty.call(e, o)) {
    if (t.indexOf(o) !== -1) continue;
    r[o] = e[o];
  }
  return r;
}
function dr(e, t) {
  if (e == null) return {};
  var r, o, n = oi(e, t);
  if (Object.getOwnPropertySymbols) {
    var i = Object.getOwnPropertySymbols(e);
    for (o = 0; o < i.length; o++) r = i[o], t.indexOf(r) === -1 && {}.propertyIsEnumerable.call(e, r) && (n[r] = e[r]);
  }
  return n;
}
var ii = /* @__PURE__ */ F.createContext({});
function Me(e, t) {
  if (!(e instanceof t)) throw new TypeError("Cannot call a class as a function");
}
function pr(e, t) {
  for (var r = 0; r < t.length; r++) {
    var o = t[r];
    o.enumerable = o.enumerable || !1, o.configurable = !0, "value" in o && (o.writable = !0), Object.defineProperty(e, Nr(o.key), o);
  }
}
function Oe(e, t, r) {
  return t && pr(e.prototype, t), r && pr(e, r), Object.defineProperty(e, "prototype", {
    writable: !1
  }), e;
}
function Ot(e, t) {
  return Ot = Object.setPrototypeOf ? Object.setPrototypeOf.bind() : function(r, o) {
    return r.__proto__ = o, r;
  }, Ot(e, t);
}
function mt(e, t) {
  if (typeof t != "function" && t !== null) throw new TypeError("Super expression must either be null or a function");
  e.prototype = Object.create(t && t.prototype, {
    constructor: {
      value: e,
      writable: !0,
      configurable: !0
    }
  }), Object.defineProperty(e, "prototype", {
    writable: !1
  }), t && Ot(e, t);
}
function et(e) {
  return et = Object.setPrototypeOf ? Object.getPrototypeOf.bind() : function(t) {
    return t.__proto__ || Object.getPrototypeOf(t);
  }, et(e);
}
function zr() {
  try {
    var e = !Boolean.prototype.valueOf.call(Reflect.construct(Boolean, [], function() {
    }));
  } catch {
  }
  return (zr = function() {
    return !!e;
  })();
}
function Ee(e) {
  if (e === void 0) throw new ReferenceError("this hasn't been initialised - super() hasn't been called");
  return e;
}
function si(e, t) {
  if (t && (ee(t) == "object" || typeof t == "function")) return t;
  if (t !== void 0) throw new TypeError("Derived constructors may only return object or undefined");
  return Ee(e);
}
function gt(e) {
  var t = zr();
  return function() {
    var r, o = et(e);
    if (t) {
      var n = et(this).constructor;
      r = Reflect.construct(o, arguments, n);
    } else r = o.apply(this, arguments);
    return si(this, r);
  };
}
var ai = /* @__PURE__ */ function(e) {
  mt(r, e);
  var t = gt(r);
  function r() {
    return Me(this, r), t.apply(this, arguments);
  }
  return Oe(r, [{
    key: "render",
    value: function() {
      return this.props.children;
    }
  }]), r;
}(F.Component);
function li(e) {
  var t = F.useReducer(function(a) {
    return a + 1;
  }, 0), r = Je(t, 2), o = r[1], n = F.useRef(e), i = Pe(function() {
    return n.current;
  }), s = Pe(function(a) {
    n.current = typeof a == "function" ? a(n.current) : a, o();
  });
  return [i, s];
}
var ye = "none", ze = "appear", He = "enter", Ue = "leave", mr = "none", le = "prepare", Re = "start", Ie = "active", Bt = "end", Hr = "prepared";
function gr(e, t) {
  var r = {};
  return r[e.toLowerCase()] = t.toLowerCase(), r["Webkit".concat(e)] = "webkit".concat(t), r["Moz".concat(e)] = "moz".concat(t), r["ms".concat(e)] = "MS".concat(t), r["O".concat(e)] = "o".concat(t.toLowerCase()), r;
}
function ci(e, t) {
  var r = {
    animationend: gr("Animation", "AnimationEnd"),
    transitionend: gr("Transition", "TransitionEnd")
  };
  return e && ("AnimationEvent" in t || delete r.animationend.animation, "TransitionEvent" in t || delete r.transitionend.transition), r;
}
var ui = ci(nt(), typeof window < "u" ? window : {}), Ur = {};
if (nt()) {
  var fi = document.createElement("div");
  Ur = fi.style;
}
var Be = {};
function Br(e) {
  if (Be[e])
    return Be[e];
  var t = ui[e];
  if (t)
    for (var r = Object.keys(t), o = r.length, n = 0; n < o; n += 1) {
      var i = r[n];
      if (Object.prototype.hasOwnProperty.call(t, i) && i in Ur)
        return Be[e] = t[i], Be[e];
    }
  return "";
}
var Vr = Br("animationend"), Xr = Br("transitionend"), Wr = !!(Vr && Xr), hr = Vr || "animationend", vr = Xr || "transitionend";
function yr(e, t) {
  if (!e) return null;
  if (ee(e) === "object") {
    var r = t.replace(/-\w/g, function(o) {
      return o[1].toUpperCase();
    });
    return e[r];
  }
  return "".concat(e, "-").concat(t);
}
const di = function(e) {
  var t = be();
  function r(n) {
    n && (n.removeEventListener(vr, e), n.removeEventListener(hr, e));
  }
  function o(n) {
    t.current && t.current !== n && r(t.current), n && n !== t.current && (n.addEventListener(vr, e), n.addEventListener(hr, e), t.current = n);
  }
  return F.useEffect(function() {
    return function() {
      r(t.current);
    };
  }, []), [o, r];
};
var Gr = nt() ? dn : xe, Kr = function(t) {
  return +setTimeout(t, 16);
}, qr = function(t) {
  return clearTimeout(t);
};
typeof window < "u" && "requestAnimationFrame" in window && (Kr = function(t) {
  return window.requestAnimationFrame(t);
}, qr = function(t) {
  return window.cancelAnimationFrame(t);
});
var br = 0, Vt = /* @__PURE__ */ new Map();
function Zr(e) {
  Vt.delete(e);
}
var Ft = function(t) {
  var r = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : 1;
  br += 1;
  var o = br;
  function n(i) {
    if (i === 0)
      Zr(o), t();
    else {
      var s = Kr(function() {
        n(i - 1);
      });
      Vt.set(o, s);
    }
  }
  return n(r), o;
};
Ft.cancel = function(e) {
  var t = Vt.get(e);
  return Zr(e), qr(t);
};
const pi = function() {
  var e = F.useRef(null);
  function t() {
    Ft.cancel(e.current);
  }
  function r(o) {
    var n = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : 2;
    t();
    var i = Ft(function() {
      n <= 1 ? o({
        isCanceled: function() {
          return i !== e.current;
        }
      }) : r(o, n - 1);
    });
    e.current = i;
  }
  return F.useEffect(function() {
    return function() {
      t();
    };
  }, []), [r, t];
};
var mi = [le, Re, Ie, Bt], gi = [le, Hr], Qr = !1, hi = !0;
function Yr(e) {
  return e === Ie || e === Bt;
}
const vi = function(e, t, r) {
  var o = je(mr), n = ie(o, 2), i = n[0], s = n[1], a = pi(), l = ie(a, 2), u = l[0], p = l[1];
  function f() {
    s(le, !0);
  }
  var d = t ? gi : mi;
  return Gr(function() {
    if (i !== mr && i !== Bt) {
      var m = d.indexOf(i), b = d[m + 1], w = r(i);
      w === Qr ? s(b, !0) : b && u(function(g) {
        function y() {
          g.isCanceled() || s(b, !0);
        }
        w === !0 ? y() : Promise.resolve(w).then(y);
      });
    }
  }, [e, i]), F.useEffect(function() {
    return function() {
      p();
    };
  }, []), [f, i];
};
function yi(e, t, r, o) {
  var n = o.motionEnter, i = n === void 0 ? !0 : n, s = o.motionAppear, a = s === void 0 ? !0 : s, l = o.motionLeave, u = l === void 0 ? !0 : l, p = o.motionDeadline, f = o.motionLeaveImmediately, d = o.onAppearPrepare, m = o.onEnterPrepare, b = o.onLeavePrepare, w = o.onAppearStart, g = o.onEnterStart, y = o.onLeaveStart, E = o.onAppearActive, C = o.onEnterActive, h = o.onLeaveActive, x = o.onAppearEnd, v = o.onEnterEnd, L = o.onLeaveEnd, S = o.onVisibleChanged, T = je(), $ = ie(T, 2), k = $[0], _ = $[1], M = li(ye), P = ie(M, 2), O = P[0], D = P[1], U = je(null), W = ie(U, 2), ge = W[0], ce = W[1], V = O(), N = be(!1), G = be(null);
  function H() {
    return r();
  }
  var Z = be(!1);
  function pe() {
    D(ye), ce(null, !0);
  }
  var ae = Pe(function(q) {
    var B = O();
    if (B !== ye) {
      var J = H();
      if (!(q && !q.deadline && q.target !== J)) {
        var z = Z.current, _e;
        B === ze && z ? _e = x == null ? void 0 : x(J, q) : B === He && z ? _e = v == null ? void 0 : v(J, q) : B === Ue && z && (_e = L == null ? void 0 : L(J, q)), z && _e !== !1 && pe();
      }
    }
  }), Fe = di(ae), me = ie(Fe, 1), ue = me[0], he = function(B) {
    switch (B) {
      case ze:
        return I(I(I({}, le, d), Re, w), Ie, E);
      case He:
        return I(I(I({}, le, m), Re, g), Ie, C);
      case Ue:
        return I(I(I({}, le, b), Re, y), Ie, h);
      default:
        return {};
    }
  }, fe = F.useMemo(function() {
    return he(V);
  }, [V]), Se = vi(V, !e, function(q) {
    if (q === le) {
      var B = fe[le];
      return B ? B(H()) : Qr;
    }
    if (j in fe) {
      var J;
      ce(((J = fe[j]) === null || J === void 0 ? void 0 : J.call(fe, H(), null)) || null);
    }
    return j === Ie && V !== ye && (ue(H()), p > 0 && (clearTimeout(G.current), G.current = setTimeout(function() {
      ae({
        deadline: !0
      });
    }, p))), j === Hr && pe(), hi;
  }), Ce = ie(Se, 2), te = Ce[0], j = Ce[1], re = Yr(j);
  Z.current = re;
  var ve = be(null);
  Gr(function() {
    if (!(N.current && ve.current === t)) {
      _(t);
      var q = N.current;
      N.current = !0;
      var B;
      !q && t && a && (B = ze), q && t && i && (B = He), (q && !t && u || !q && f && !t && u) && (B = Ue);
      var J = he(B);
      B && (e || J[le]) ? (D(B), te()) : D(ye), ve.current = t;
    }
  }, [t]), xe(function() {
    // Cancel appear
    (V === ze && !a || // Cancel enter
    V === He && !i || // Cancel leave
    V === Ue && !u) && D(ye);
  }, [a, i, u]), xe(function() {
    return function() {
      N.current = !1, clearTimeout(G.current);
    };
  }, []);
  var K = F.useRef(!1);
  xe(function() {
    k && (K.current = !0), k !== void 0 && V === ye && ((K.current || k) && (S == null || S(k)), K.current = !0);
  }, [k, V]);
  var we = ge;
  return fe[le] && j === Re && (we = R({
    transition: "none"
  }, we)), [V, j, we, k ?? t];
}
function bi(e) {
  var t = e;
  ee(e) === "object" && (t = e.transitionSupport);
  function r(n, i) {
    return !!(n.motionName && t && i !== !1);
  }
  var o = /* @__PURE__ */ F.forwardRef(function(n, i) {
    var s = n.visible, a = s === void 0 ? !0 : s, l = n.removeOnLeave, u = l === void 0 ? !0 : l, p = n.forceRender, f = n.children, d = n.motionName, m = n.leavedClassName, b = n.eventProps, w = F.useContext(ii), g = w.motion, y = r(n, g), E = be(), C = be();
    function h() {
      try {
        return E.current instanceof HTMLElement ? E.current : ni(C.current);
      } catch {
        return null;
      }
    }
    var x = yi(y, a, h, n), v = ie(x, 4), L = v[0], S = v[1], T = v[2], $ = v[3], k = F.useRef($);
    $ && (k.current = !0);
    var _ = F.useCallback(function(W) {
      E.current = W, Ko(i, W);
    }, [i]), M, P = R(R({}, b), {}, {
      visible: a
    });
    if (!f)
      M = null;
    else if (L === ye)
      $ ? M = f(R({}, P), _) : !u && k.current && m ? M = f(R(R({}, P), {}, {
        className: m
      }), _) : p || !u && !m ? M = f(R(R({}, P), {}, {
        style: {
          display: "none"
        }
      }), _) : M = null;
    else {
      var O;
      S === le ? O = "prepare" : Yr(S) ? O = "active" : S === Re && (O = "start");
      var D = yr(d, "".concat(L, "-").concat(O));
      M = f(R(R({}, P), {}, {
        className: oe(yr(d, L), I(I({}, D, D && O), d, typeof d == "string")),
        style: T
      }), _);
    }
    if (/* @__PURE__ */ F.isValidElement(M) && qo(M)) {
      var U = Zo(M);
      U || (M = /* @__PURE__ */ F.cloneElement(M, {
        ref: _
      }));
    }
    return /* @__PURE__ */ F.createElement(ai, {
      ref: C
    }, M);
  });
  return o.displayName = "CSSMotion", o;
}
const Si = bi(Wr);
var At = "add", $t = "keep", kt = "remove", Et = "removed";
function wi(e) {
  var t;
  return e && ee(e) === "object" && "key" in e ? t = e : t = {
    key: e
  }, R(R({}, t), {}, {
    key: String(t.key)
  });
}
function jt() {
  var e = arguments.length > 0 && arguments[0] !== void 0 ? arguments[0] : [];
  return e.map(wi);
}
function xi() {
  var e = arguments.length > 0 && arguments[0] !== void 0 ? arguments[0] : [], t = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : [], r = [], o = 0, n = t.length, i = jt(e), s = jt(t);
  i.forEach(function(u) {
    for (var p = !1, f = o; f < n; f += 1) {
      var d = s[f];
      if (d.key === u.key) {
        o < f && (r = r.concat(s.slice(o, f).map(function(m) {
          return R(R({}, m), {}, {
            status: At
          });
        })), o = f), r.push(R(R({}, d), {}, {
          status: $t
        })), o += 1, p = !0;
        break;
      }
    }
    p || r.push(R(R({}, u), {}, {
      status: kt
    }));
  }), o < n && (r = r.concat(s.slice(o).map(function(u) {
    return R(R({}, u), {}, {
      status: At
    });
  })));
  var a = {};
  r.forEach(function(u) {
    var p = u.key;
    a[p] = (a[p] || 0) + 1;
  });
  var l = Object.keys(a).filter(function(u) {
    return a[u] > 1;
  });
  return l.forEach(function(u) {
    r = r.filter(function(p) {
      var f = p.key, d = p.status;
      return f !== u || d !== kt;
    }), r.forEach(function(p) {
      p.key === u && (p.status = $t);
    });
  }), r;
}
var Ei = ["component", "children", "onVisibleChanged", "onAllRemoved"], Ci = ["status"], _i = ["eventProps", "visible", "children", "motionName", "motionAppear", "motionEnter", "motionLeave", "motionLeaveImmediately", "motionDeadline", "removeOnLeave", "leavedClassName", "onAppearPrepare", "onAppearStart", "onAppearActive", "onAppearEnd", "onEnterStart", "onEnterActive", "onEnterEnd", "onLeaveStart", "onLeaveActive", "onLeaveEnd"];
function Li(e) {
  var t = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : Si, r = /* @__PURE__ */ function(o) {
    mt(i, o);
    var n = gt(i);
    function i() {
      var s;
      Me(this, i);
      for (var a = arguments.length, l = new Array(a), u = 0; u < a; u++)
        l[u] = arguments[u];
      return s = n.call.apply(n, [this].concat(l)), I(Ee(s), "state", {
        keyEntities: []
      }), I(Ee(s), "removeKey", function(p) {
        s.setState(function(f) {
          var d = f.keyEntities.map(function(m) {
            return m.key !== p ? m : R(R({}, m), {}, {
              status: Et
            });
          });
          return {
            keyEntities: d
          };
        }, function() {
          var f = s.state.keyEntities, d = f.filter(function(m) {
            var b = m.status;
            return b !== Et;
          }).length;
          d === 0 && s.props.onAllRemoved && s.props.onAllRemoved();
        });
      }), s;
    }
    return Oe(i, [{
      key: "render",
      value: function() {
        var a = this, l = this.state.keyEntities, u = this.props, p = u.component, f = u.children, d = u.onVisibleChanged;
        u.onAllRemoved;
        var m = dr(u, Ei), b = p || F.Fragment, w = {};
        return _i.forEach(function(g) {
          w[g] = m[g], delete m[g];
        }), delete m.keys, /* @__PURE__ */ F.createElement(b, m, l.map(function(g, y) {
          var E = g.status, C = dr(g, Ci), h = E === At || E === $t;
          return /* @__PURE__ */ F.createElement(t, Te({}, w, {
            key: C.key,
            visible: h,
            eventProps: C,
            onVisibleChanged: function(v) {
              d == null || d(v, {
                key: C.key
              }), v || a.removeKey(C.key);
            }
          }), function(x, v) {
            return f(R(R({}, x), {}, {
              index: y
            }), v);
          });
        }));
      }
    }], [{
      key: "getDerivedStateFromProps",
      value: function(a, l) {
        var u = a.keys, p = l.keyEntities, f = jt(u), d = xi(p, f);
        return {
          keyEntities: d.filter(function(m) {
            var b = p.find(function(w) {
              var g = w.key;
              return m.key === g;
            });
            return !(b && b.status === Et && m.status === kt);
          })
        };
      }
    }]), i;
  }(F.Component);
  return I(r, "defaultProps", {
    component: "div"
  }), r;
}
const Ri = Li(Wr);
function Ii(e, t) {
  const {
    children: r,
    upload: o,
    rootClassName: n
  } = e, i = c.useRef(null);
  return c.useImperativeHandle(t, () => i.current), /* @__PURE__ */ c.createElement(Tr, Te({}, o, {
    showUploadList: !1,
    rootClassName: n,
    ref: i
  }), r);
}
const Jr = /* @__PURE__ */ c.forwardRef(Ii);
var en = /* @__PURE__ */ Oe(function e() {
  Me(this, e);
}), tn = "CALC_UNIT", Ti = new RegExp(tn, "g");
function Ct(e) {
  return typeof e == "number" ? "".concat(e).concat(tn) : e;
}
var Pi = /* @__PURE__ */ function(e) {
  mt(r, e);
  var t = gt(r);
  function r(o, n) {
    var i;
    Me(this, r), i = t.call(this), I(Ee(i), "result", ""), I(Ee(i), "unitlessCssVar", void 0), I(Ee(i), "lowPriority", void 0);
    var s = ee(o);
    return i.unitlessCssVar = n, o instanceof r ? i.result = "(".concat(o.result, ")") : s === "number" ? i.result = Ct(o) : s === "string" && (i.result = o), i;
  }
  return Oe(r, [{
    key: "add",
    value: function(n) {
      return n instanceof r ? this.result = "".concat(this.result, " + ").concat(n.getResult()) : (typeof n == "number" || typeof n == "string") && (this.result = "".concat(this.result, " + ").concat(Ct(n))), this.lowPriority = !0, this;
    }
  }, {
    key: "sub",
    value: function(n) {
      return n instanceof r ? this.result = "".concat(this.result, " - ").concat(n.getResult()) : (typeof n == "number" || typeof n == "string") && (this.result = "".concat(this.result, " - ").concat(Ct(n))), this.lowPriority = !0, this;
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
      var i = this, s = n || {}, a = s.unit, l = !0;
      return typeof a == "boolean" ? l = a : Array.from(this.unitlessCssVar).some(function(u) {
        return i.result.includes(u);
      }) && (l = !1), this.result = this.result.replace(Ti, l ? "px" : ""), typeof this.lowPriority < "u" ? "calc(".concat(this.result, ")") : this.result;
    }
  }]), r;
}(en), Mi = /* @__PURE__ */ function(e) {
  mt(r, e);
  var t = gt(r);
  function r(o) {
    var n;
    return Me(this, r), n = t.call(this), I(Ee(n), "result", 0), o instanceof r ? n.result = o.result : typeof o == "number" && (n.result = o), n;
  }
  return Oe(r, [{
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
}(en), Oi = function(t, r) {
  var o = t === "css" ? Pi : Mi;
  return function(n) {
    return new o(n, r);
  };
}, Sr = function(t, r) {
  return "".concat([r, t.replace(/([A-Z]+)([A-Z][a-z]+)/g, "$1-$2").replace(/([a-z])([A-Z])/g, "$1-$2")].filter(Boolean).join("-"));
};
function wr(e, t, r, o) {
  var n = R({}, t[e]);
  if (o != null && o.deprecatedTokens) {
    var i = o.deprecatedTokens;
    i.forEach(function(a) {
      var l = ie(a, 2), u = l[0], p = l[1];
      if (n != null && n[u] || n != null && n[p]) {
        var f;
        (f = n[p]) !== null && f !== void 0 || (n[p] = n == null ? void 0 : n[u]);
      }
    });
  }
  var s = R(R({}, r), n);
  return Object.keys(s).forEach(function(a) {
    s[a] === t[a] && delete s[a];
  }), s;
}
var rn = typeof CSSINJS_STATISTIC < "u", Dt = !0;
function Xt() {
  for (var e = arguments.length, t = new Array(e), r = 0; r < e; r++)
    t[r] = arguments[r];
  if (!rn)
    return Object.assign.apply(Object, [{}].concat(t));
  Dt = !1;
  var o = {};
  return t.forEach(function(n) {
    if (ee(n) === "object") {
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
  }), Dt = !0, o;
}
var xr = {};
function Fi() {
}
var Ai = function(t) {
  var r, o = t, n = Fi;
  return rn && typeof Proxy < "u" && (r = /* @__PURE__ */ new Set(), o = new Proxy(t, {
    get: function(s, a) {
      if (Dt) {
        var l;
        (l = r) === null || l === void 0 || l.add(a);
      }
      return s[a];
    }
  }), n = function(s, a) {
    var l;
    xr[s] = {
      global: Array.from(r),
      component: R(R({}, (l = xr[s]) === null || l === void 0 ? void 0 : l.component), a)
    };
  }), {
    token: o,
    keys: r,
    flush: n
  };
};
function Er(e, t, r) {
  if (typeof r == "function") {
    var o;
    return r(Xt(t, (o = t[e]) !== null && o !== void 0 ? o : {}));
  }
  return r ?? {};
}
function $i(e) {
  return e === "js" ? {
    max: Math.max,
    min: Math.min
  } : {
    max: function() {
      for (var r = arguments.length, o = new Array(r), n = 0; n < r; n++)
        o[n] = arguments[n];
      return "max(".concat(o.map(function(i) {
        return Gt(i);
      }).join(","), ")");
    },
    min: function() {
      for (var r = arguments.length, o = new Array(r), n = 0; n < r; n++)
        o[n] = arguments[n];
      return "min(".concat(o.map(function(i) {
        return Gt(i);
      }).join(","), ")");
    }
  };
}
var ki = 1e3 * 60 * 10, ji = /* @__PURE__ */ function() {
  function e() {
    Me(this, e), I(this, "map", /* @__PURE__ */ new Map()), I(this, "objectIDMap", /* @__PURE__ */ new WeakMap()), I(this, "nextID", 0), I(this, "lastAccessBeat", /* @__PURE__ */ new Map()), I(this, "accessBeat", 0);
  }
  return Oe(e, [{
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
        return i && ee(i) === "object" ? "obj_".concat(o.getObjectID(i)) : "".concat(ee(i), "_").concat(i);
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
          o - n > ki && (r.map.delete(i), r.lastAccessBeat.delete(i));
        }), this.accessBeat = 0;
      }
    }
  }]), e;
}(), Cr = new ji();
function Di(e, t) {
  return c.useMemo(function() {
    var r = Cr.get(t);
    if (r)
      return r;
    var o = e();
    return Cr.set(t, o), o;
  }, t);
}
var Ni = function() {
  return {};
};
function zi(e) {
  var t = e.useCSP, r = t === void 0 ? Ni : t, o = e.useToken, n = e.usePrefix, i = e.getResetStyles, s = e.getCommonStyle, a = e.getCompUnitless;
  function l(d, m, b, w) {
    var g = Array.isArray(d) ? d[0] : d;
    function y(S) {
      return "".concat(String(g)).concat(S.slice(0, 1).toUpperCase()).concat(S.slice(1));
    }
    var E = (w == null ? void 0 : w.unitless) || {}, C = typeof a == "function" ? a(d) : {}, h = R(R({}, C), {}, I({}, y("zIndexPopup"), !0));
    Object.keys(E).forEach(function(S) {
      h[y(S)] = E[S];
    });
    var x = R(R({}, w), {}, {
      unitless: h,
      prefixToken: y
    }), v = p(d, m, b, x), L = u(g, b, x);
    return function(S) {
      var T = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : S, $ = v(S, T), k = ie($, 2), _ = k[1], M = L(T), P = ie(M, 2), O = P[0], D = P[1];
      return [O, _, D];
    };
  }
  function u(d, m, b) {
    var w = b.unitless, g = b.injectStyle, y = g === void 0 ? !0 : g, E = b.prefixToken, C = b.ignore, h = function(L) {
      var S = L.rootCls, T = L.cssVar, $ = T === void 0 ? {} : T, k = o(), _ = k.realToken;
      return kn({
        path: [d],
        prefix: $.prefix,
        key: $.key,
        unitless: w,
        ignore: C,
        token: _,
        scope: S
      }, function() {
        var M = Er(d, _, m), P = wr(d, _, M, {
          deprecatedTokens: b == null ? void 0 : b.deprecatedTokens
        });
        return Object.keys(M).forEach(function(O) {
          P[E(O)] = P[O], delete P[O];
        }), P;
      }), null;
    }, x = function(L) {
      var S = o(), T = S.cssVar;
      return [function($) {
        return y && T ? /* @__PURE__ */ c.createElement(c.Fragment, null, /* @__PURE__ */ c.createElement(h, {
          rootCls: L,
          cssVar: T,
          component: d
        }), $) : $;
      }, T == null ? void 0 : T.key];
    };
    return x;
  }
  function p(d, m, b) {
    var w = arguments.length > 3 && arguments[3] !== void 0 ? arguments[3] : {}, g = Array.isArray(d) ? d : [d, d], y = ie(g, 1), E = y[0], C = g.join("-"), h = e.layer || {
      name: "antd"
    };
    return function(x) {
      var v = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : x, L = o(), S = L.theme, T = L.realToken, $ = L.hashId, k = L.token, _ = L.cssVar, M = n(), P = M.rootPrefixCls, O = M.iconPrefixCls, D = r(), U = _ ? "css" : "js", W = Di(function() {
        var H = /* @__PURE__ */ new Set();
        return _ && Object.keys(w.unitless || {}).forEach(function(Z) {
          H.add(yt(Z, _.prefix)), H.add(yt(Z, Sr(E, _.prefix)));
        }), Oi(U, H);
      }, [U, E, _ == null ? void 0 : _.prefix]), ge = $i(U), ce = ge.max, V = ge.min, N = {
        theme: S,
        token: k,
        hashId: $,
        nonce: function() {
          return D.nonce;
        },
        clientOnly: w.clientOnly,
        layer: h,
        // antd is always at top of styles
        order: w.order || -999
      };
      typeof i == "function" && Kt(R(R({}, N), {}, {
        clientOnly: !1,
        path: ["Shared", P]
      }), function() {
        return i(k, {
          prefix: {
            rootPrefixCls: P,
            iconPrefixCls: O
          },
          csp: D
        });
      });
      var G = Kt(R(R({}, N), {}, {
        path: [C, x, O]
      }), function() {
        if (w.injectStyle === !1)
          return [];
        var H = Ai(k), Z = H.token, pe = H.flush, ae = Er(E, T, b), Fe = ".".concat(x), me = wr(E, T, ae, {
          deprecatedTokens: w.deprecatedTokens
        });
        _ && ae && ee(ae) === "object" && Object.keys(ae).forEach(function(Se) {
          ae[Se] = "var(".concat(yt(Se, Sr(E, _.prefix)), ")");
        });
        var ue = Xt(Z, {
          componentCls: Fe,
          prefixCls: x,
          iconCls: ".".concat(O),
          antCls: ".".concat(P),
          calc: W,
          // @ts-ignore
          max: ce,
          // @ts-ignore
          min: V
        }, _ ? ae : me), he = m(ue, {
          hashId: $,
          prefixCls: x,
          rootPrefixCls: P,
          iconPrefixCls: O
        });
        pe(E, me);
        var fe = typeof s == "function" ? s(ue, x, v, w.resetFont) : null;
        return [w.resetStyle === !1 ? null : fe, he];
      });
      return [G, $];
    };
  }
  function f(d, m, b) {
    var w = arguments.length > 3 && arguments[3] !== void 0 ? arguments[3] : {}, g = p(d, m, b, R({
      resetStyle: !1,
      // Sub Style should default after root one
      order: -998
    }, w)), y = function(C) {
      var h = C.prefixCls, x = C.rootCls, v = x === void 0 ? h : x;
      return g(h, v), null;
    };
    return y;
  }
  return {
    genStyleHooks: l,
    genSubStyleComponent: f,
    genComponentStyleHook: p
  };
}
const X = Math.round;
function _t(e, t) {
  const r = e.replace(/^[^(]*\((.*)/, "$1").replace(/\).*/, "").match(/\d*\.?\d+%?/g) || [], o = r.map((n) => parseFloat(n));
  for (let n = 0; n < 3; n += 1)
    o[n] = t(o[n] || 0, r[n] || "", n);
  return r[3] ? o[3] = r[3].includes("%") ? o[3] / 100 : o[3] : o[3] = 1, o;
}
const _r = (e, t, r) => r === 0 ? e : e / 100;
function Ae(e, t) {
  const r = t || 255;
  return e > r ? r : e < 0 ? 0 : e;
}
class de {
  constructor(t) {
    I(this, "isValid", !0), I(this, "r", 0), I(this, "g", 0), I(this, "b", 0), I(this, "a", 1), I(this, "_h", void 0), I(this, "_s", void 0), I(this, "_l", void 0), I(this, "_v", void 0), I(this, "_max", void 0), I(this, "_min", void 0), I(this, "_brightness", void 0);
    function r(o) {
      return o[0] in t && o[1] in t && o[2] in t;
    }
    if (t) if (typeof t == "string") {
      let n = function(i) {
        return o.startsWith(i);
      };
      const o = t.trim();
      /^#?[A-F\d]{3,8}$/i.test(o) ? this.fromHexString(o) : n("rgb") ? this.fromRgbString(o) : n("hsl") ? this.fromHslString(o) : (n("hsv") || n("hsb")) && this.fromHsvString(o);
    } else if (t instanceof de)
      this.r = t.r, this.g = t.g, this.b = t.b, this.a = t.a, this._h = t._h, this._s = t._s, this._l = t._l, this._v = t._v;
    else if (r("rgb"))
      this.r = Ae(t.r), this.g = Ae(t.g), this.b = Ae(t.b), this.a = typeof t.a == "number" ? Ae(t.a, 1) : 1;
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
      t === 0 ? this._h = 0 : this._h = X(60 * (this.r === this.getMax() ? (this.g - this.b) / t + (this.g < this.b ? 6 : 0) : this.g === this.getMax() ? (this.b - this.r) / t + 2 : (this.r - this.g) / t + 4));
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
      r: X(i("r")),
      g: X(i("g")),
      b: X(i("b")),
      a: X(i("a") * 100) / 100
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
    const r = this._c(t), o = this.a + r.a * (1 - this.a), n = (i) => X((this[i] * this.a + r[i] * r.a * (1 - this.a)) / o);
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
      const i = X(this.a * 255).toString(16);
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
    const t = this.getHue(), r = X(this.getSaturation() * 100), o = X(this.getLightness() * 100);
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
    return n[t] = Ae(r, o), n;
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
      const d = X(o * 255);
      this.r = d, this.g = d, this.b = d;
    }
    let i = 0, s = 0, a = 0;
    const l = t / 60, u = (1 - Math.abs(2 * o - 1)) * r, p = u * (1 - Math.abs(l % 2 - 1));
    l >= 0 && l < 1 ? (i = u, s = p) : l >= 1 && l < 2 ? (i = p, s = u) : l >= 2 && l < 3 ? (s = u, a = p) : l >= 3 && l < 4 ? (s = p, a = u) : l >= 4 && l < 5 ? (i = p, a = u) : l >= 5 && l < 6 && (i = u, a = p);
    const f = o - u / 2;
    this.r = X((i + f) * 255), this.g = X((s + f) * 255), this.b = X((a + f) * 255);
  }
  fromHsv({
    h: t,
    s: r,
    v: o,
    a: n
  }) {
    this._h = t % 360, this._s = r, this._v = o, this.a = typeof n == "number" ? n : 1;
    const i = X(o * 255);
    if (this.r = i, this.g = i, this.b = i, r <= 0)
      return;
    const s = t / 60, a = Math.floor(s), l = s - a, u = X(o * (1 - r) * 255), p = X(o * (1 - r * l) * 255), f = X(o * (1 - r * (1 - l)) * 255);
    switch (a) {
      case 0:
        this.g = f, this.b = u;
        break;
      case 1:
        this.r = p, this.b = u;
        break;
      case 2:
        this.r = u, this.b = f;
        break;
      case 3:
        this.r = u, this.g = p;
        break;
      case 4:
        this.r = f, this.g = u;
        break;
      case 5:
      default:
        this.g = u, this.b = p;
        break;
    }
  }
  fromHsvString(t) {
    const r = _t(t, _r);
    this.fromHsv({
      h: r[0],
      s: r[1],
      v: r[2],
      a: r[3]
    });
  }
  fromHslString(t) {
    const r = _t(t, _r);
    this.fromHsl({
      h: r[0],
      s: r[1],
      l: r[2],
      a: r[3]
    });
  }
  fromRgbString(t) {
    const r = _t(t, (o, n) => (
      // Convert percentage to number. e.g. 50% -> 128
      n.includes("%") ? X(o / 100 * 255) : o
    ));
    this.r = r[0], this.g = r[1], this.b = r[2], this.a = r[3];
  }
}
const Hi = {
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
}, Ui = Object.assign(Object.assign({}, Hi), {
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
function Lt(e) {
  return e >= 0 && e <= 255;
}
function Ve(e, t) {
  const {
    r,
    g: o,
    b: n,
    a: i
  } = new de(e).toRgb();
  if (i < 1)
    return e;
  const {
    r: s,
    g: a,
    b: l
  } = new de(t).toRgb();
  for (let u = 0.01; u <= 1; u += 0.01) {
    const p = Math.round((r - s * (1 - u)) / u), f = Math.round((o - a * (1 - u)) / u), d = Math.round((n - l * (1 - u)) / u);
    if (Lt(p) && Lt(f) && Lt(d))
      return new de({
        r: p,
        g: f,
        b: d,
        a: Math.round(u * 100) / 100
      }).toRgbString();
  }
  return new de({
    r,
    g: o,
    b: n,
    a: 1
  }).toRgbString();
}
var Bi = function(e, t) {
  var r = {};
  for (var o in e) Object.prototype.hasOwnProperty.call(e, o) && t.indexOf(o) < 0 && (r[o] = e[o]);
  if (e != null && typeof Object.getOwnPropertySymbols == "function") for (var n = 0, o = Object.getOwnPropertySymbols(e); n < o.length; n++)
    t.indexOf(o[n]) < 0 && Object.prototype.propertyIsEnumerable.call(e, o[n]) && (r[o[n]] = e[o[n]]);
  return r;
};
function Vi(e) {
  const {
    override: t
  } = e, r = Bi(e, ["override"]), o = Object.assign({}, t);
  Object.keys(Ui).forEach((d) => {
    delete o[d];
  });
  const n = Object.assign(Object.assign({}, r), o), i = 480, s = 576, a = 768, l = 992, u = 1200, p = 1600;
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
    colorSplit: Ve(n.colorBorderSecondary, n.colorBgContainer),
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
    colorErrorOutline: Ve(n.colorErrorBg, n.colorBgContainer),
    colorWarningOutline: Ve(n.colorWarningBg, n.colorBgContainer),
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
    controlOutline: Ve(n.colorPrimaryBg, n.colorBgContainer),
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
    screenMDMax: l - 1,
    screenLG: l,
    screenLGMin: l,
    screenLGMax: u - 1,
    screenXL: u,
    screenXLMin: u,
    screenXLMax: p - 1,
    screenXXL: p,
    screenXXLMin: p,
    boxShadowPopoverArrow: "2px 2px 5px rgba(0, 0, 0, 0.05)",
    boxShadowCard: `
      0 1px 2px -2px ${new de("rgba(0, 0, 0, 0.16)").toRgbString()},
      0 3px 6px 0 ${new de("rgba(0, 0, 0, 0.12)").toRgbString()},
      0 5px 12px 4px ${new de("rgba(0, 0, 0, 0.09)").toRgbString()}
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
const Xi = {
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
}, Wi = {
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
}, Gi = jn(Qe.defaultAlgorithm), Ki = {
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
}, nn = (e, t, r) => {
  const o = r.getDerivativeToken(e), {
    override: n,
    ...i
  } = t;
  let s = {
    ...o,
    override: n
  };
  return s = Vi(s), i && Object.entries(i).forEach(([a, l]) => {
    const {
      theme: u,
      ...p
    } = l;
    let f = p;
    u && (f = nn({
      ...s,
      ...p
    }, {
      override: p
    }, u)), s[a] = f;
  }), s;
};
function qi() {
  const {
    token: e,
    hashed: t,
    theme: r = Gi,
    override: o,
    cssVar: n
  } = c.useContext(Qe._internalContext), [i, s, a] = Dn(r, [Qe.defaultSeed, e], {
    salt: `${Mo}-${t || ""}`,
    override: o,
    getComputedToken: nn,
    cssVar: n && {
      prefix: n.prefix,
      key: n.key,
      unitless: Xi,
      ignore: Wi,
      preserve: Ki
    }
  });
  return [r, a, t ? s : "", i, n];
}
const {
  genStyleHooks: Zi
} = zi({
  usePrefix: () => {
    const {
      getPrefixCls: e,
      iconPrefixCls: t
    } = Ye();
    return {
      iconPrefixCls: t,
      rootPrefixCls: e()
    };
  },
  useToken: () => {
    const [e, t, r, o, n] = qi();
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
    } = Ye();
    return e ?? {};
  },
  layer: {
    name: "antdx",
    dependencies: ["antd"]
  }
}), Qi = (e) => {
  const {
    componentCls: t,
    antCls: r,
    calc: o
  } = e, n = `${t}-list-card`, i = o(e.fontSize).mul(e.lineHeight).mul(2).add(e.paddingSM).add(e.paddingSM).equal();
  return {
    [n]: {
      borderRadius: e.borderRadius,
      position: "relative",
      background: e.colorFillContent,
      borderWidth: e.lineWidth,
      borderStyle: "solid",
      borderColor: "transparent",
      flex: "none",
      // =============================== Desc ================================
      [`${n}-name,${n}-desc`]: {
        display: "flex",
        flexWrap: "nowrap",
        maxWidth: "100%"
      },
      [`${n}-ellipsis-prefix`]: {
        flex: "0 1 auto",
        minWidth: 0,
        overflow: "hidden",
        textOverflow: "ellipsis",
        whiteSpace: "nowrap"
      },
      [`${n}-ellipsis-suffix`]: {
        flex: "none"
      },
      // ============================= Overview ==============================
      "&-type-overview": {
        padding: o(e.paddingSM).sub(e.lineWidth).equal(),
        paddingInlineStart: o(e.padding).add(e.lineWidth).equal(),
        display: "flex",
        flexWrap: "nowrap",
        gap: e.paddingXS,
        alignItems: "flex-start",
        width: 236,
        // Icon
        [`${n}-icon`]: {
          fontSize: o(e.fontSizeLG).mul(2).equal(),
          lineHeight: 1,
          paddingTop: o(e.paddingXXS).mul(1.5).equal(),
          flex: "none"
        },
        // Content
        [`${n}-content`]: {
          flex: "auto",
          minWidth: 0,
          display: "flex",
          flexDirection: "column",
          alignItems: "stretch"
        },
        [`${n}-desc`]: {
          color: e.colorTextTertiary
        }
      },
      // ============================== Preview ==============================
      "&-type-preview": {
        width: i,
        height: i,
        lineHeight: 1,
        display: "flex",
        alignItems: "center",
        [`&:not(${n}-status-error)`]: {
          border: 0
        },
        // Img
        [`${r}-image`]: {
          width: "100%",
          height: "100%",
          borderRadius: "inherit",
          img: {
            height: "100%",
            objectFit: "cover",
            borderRadius: "inherit"
          }
        },
        // Mask
        [`${n}-img-mask`]: {
          position: "absolute",
          inset: 0,
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          background: `rgba(0, 0, 0, ${e.opacityLoading})`,
          borderRadius: "inherit"
        },
        // Error
        [`&${n}-status-error`]: {
          [`img, ${n}-img-mask`]: {
            borderRadius: o(e.borderRadius).sub(e.lineWidth).equal()
          },
          [`${n}-desc`]: {
            paddingInline: e.paddingXXS
          }
        },
        // Progress
        [`${n}-progress`]: {}
      },
      // ============================ Remove Icon ============================
      [`${n}-remove`]: {
        position: "absolute",
        top: 0,
        insetInlineEnd: 0,
        border: 0,
        padding: e.paddingXXS,
        background: "transparent",
        lineHeight: 1,
        transform: "translate(50%, -50%)",
        fontSize: e.fontSize,
        cursor: "pointer",
        opacity: e.opacityLoading,
        display: "none",
        "&:dir(rtl)": {
          transform: "translate(-50%, -50%)"
        },
        "&:hover": {
          opacity: 1
        },
        "&:active": {
          opacity: e.opacityLoading
        }
      },
      [`&:hover ${n}-remove`]: {
        display: "block"
      },
      // ============================== Status ===============================
      "&-status-error": {
        borderColor: e.colorError,
        [`${n}-desc`]: {
          color: e.colorError
        }
      },
      // ============================== Motion ===============================
      "&-motion": {
        transition: ["opacity", "width", "margin", "padding"].map((s) => `${s} ${e.motionDurationSlow}`).join(","),
        "&-appear-start": {
          width: 0,
          transition: "none"
        },
        "&-leave-active": {
          opacity: 0,
          width: 0,
          paddingInline: 0,
          borderInlineWidth: 0,
          marginInlineEnd: o(e.paddingSM).mul(-1).equal()
        }
      }
    }
  };
}, Nt = {
  "&, *": {
    boxSizing: "border-box"
  }
}, Yi = (e) => {
  const {
    componentCls: t,
    calc: r,
    antCls: o
  } = e, n = `${t}-drop-area`, i = `${t}-placeholder`;
  return {
    // ============================== Full Screen ==============================
    [n]: {
      position: "absolute",
      inset: 0,
      zIndex: e.zIndexPopupBase,
      ...Nt,
      "&-on-body": {
        position: "fixed",
        inset: 0
      },
      "&-hide-placement": {
        [`${i}-inner`]: {
          display: "none"
        }
      },
      [i]: {
        padding: 0
      }
    },
    "&": {
      // ============================= Placeholder =============================
      [i]: {
        height: "100%",
        borderRadius: e.borderRadius,
        borderWidth: e.lineWidthBold,
        borderStyle: "dashed",
        borderColor: "transparent",
        padding: e.padding,
        position: "relative",
        backdropFilter: "blur(10px)",
        background: e.colorBgPlaceholderHover,
        ...Nt,
        [`${o}-upload-wrapper ${o}-upload${o}-upload-btn`]: {
          padding: 0
        },
        [`&${i}-drag-in`]: {
          borderColor: e.colorPrimaryHover
        },
        [`&${i}-disabled`]: {
          opacity: 0.25,
          pointerEvents: "none"
        },
        [`${i}-inner`]: {
          gap: r(e.paddingXXS).div(2).equal()
        },
        [`${i}-icon`]: {
          fontSize: e.fontSizeHeading2,
          lineHeight: 1
        },
        [`${i}-title${i}-title`]: {
          margin: 0,
          fontSize: e.fontSize,
          lineHeight: e.lineHeight
        },
        [`${i}-description`]: {}
      }
    }
  };
}, Ji = (e) => {
  const {
    componentCls: t,
    calc: r
  } = e, o = `${t}-list`, n = r(e.fontSize).mul(e.lineHeight).mul(2).add(e.paddingSM).add(e.paddingSM).equal();
  return {
    [t]: {
      position: "relative",
      width: "100%",
      ...Nt,
      // =============================== File List ===============================
      [o]: {
        display: "flex",
        flexWrap: "wrap",
        gap: e.paddingSM,
        fontSize: e.fontSize,
        lineHeight: e.lineHeight,
        color: e.colorText,
        paddingBlock: e.paddingSM,
        paddingInline: e.padding,
        width: "100%",
        background: e.colorBgContainer,
        // Hide scrollbar
        scrollbarWidth: "none",
        "-ms-overflow-style": "none",
        "&::-webkit-scrollbar": {
          display: "none"
        },
        // Scroll
        "&-overflow-scrollX, &-overflow-scrollY": {
          "&:before, &:after": {
            content: '""',
            position: "absolute",
            opacity: 0,
            transition: `opacity ${e.motionDurationSlow}`,
            zIndex: 1
          }
        },
        "&-overflow-ping-start:before": {
          opacity: 1
        },
        "&-overflow-ping-end:after": {
          opacity: 1
        },
        "&-overflow-scrollX": {
          overflowX: "auto",
          overflowY: "hidden",
          flexWrap: "nowrap",
          "&:before, &:after": {
            insetBlock: 0,
            width: 8
          },
          "&:before": {
            insetInlineStart: 0,
            background: "linear-gradient(to right, rgba(0,0,0,0.06), rgba(0,0,0,0));"
          },
          "&:after": {
            insetInlineEnd: 0,
            background: "linear-gradient(to left, rgba(0,0,0,0.06), rgba(0,0,0,0));"
          },
          "&:dir(rtl)": {
            "&:before": {
              background: "linear-gradient(to left, rgba(0,0,0,0.06), rgba(0,0,0,0));"
            },
            "&:after": {
              background: "linear-gradient(to right, rgba(0,0,0,0.06), rgba(0,0,0,0));"
            }
          }
        },
        "&-overflow-scrollY": {
          overflowX: "hidden",
          overflowY: "auto",
          maxHeight: r(n).mul(3).equal(),
          "&:before, &:after": {
            insetInline: 0,
            height: 8
          },
          "&:before": {
            insetBlockStart: 0,
            background: "linear-gradient(to bottom, rgba(0,0,0,0.06), rgba(0,0,0,0));"
          },
          "&:after": {
            insetBlockEnd: 0,
            background: "linear-gradient(to top, rgba(0,0,0,0.06), rgba(0,0,0,0));"
          }
        },
        // ======================================================================
        // ==                              Upload                              ==
        // ======================================================================
        "&-upload-btn": {
          width: n,
          height: n,
          fontSize: e.fontSizeHeading2,
          color: "#999"
        },
        // ======================================================================
        // ==                             PrevNext                             ==
        // ======================================================================
        "&-prev-btn, &-next-btn": {
          position: "absolute",
          top: "50%",
          transform: "translateY(-50%)",
          boxShadow: e.boxShadowTertiary,
          opacity: 0,
          pointerEvents: "none"
        },
        "&-prev-btn": {
          left: {
            _skip_check_: !0,
            value: e.padding
          }
        },
        "&-next-btn": {
          right: {
            _skip_check_: !0,
            value: e.padding
          }
        },
        "&:dir(ltr)": {
          [`&${o}-overflow-ping-start ${o}-prev-btn`]: {
            opacity: 1,
            pointerEvents: "auto"
          },
          [`&${o}-overflow-ping-end ${o}-next-btn`]: {
            opacity: 1,
            pointerEvents: "auto"
          }
        },
        "&:dir(rtl)": {
          [`&${o}-overflow-ping-end ${o}-prev-btn`]: {
            opacity: 1,
            pointerEvents: "auto"
          },
          [`&${o}-overflow-ping-start ${o}-next-btn`]: {
            opacity: 1,
            pointerEvents: "auto"
          }
        }
      }
    }
  };
}, es = (e) => {
  const {
    colorBgContainer: t
  } = e;
  return {
    colorBgPlaceholderHover: new de(t).setA(0.85).toRgbString()
  };
}, on = Zi("Attachments", (e) => {
  const t = Xt(e, {});
  return [Yi(t), Ji(t), Qi(t)];
}, es), ts = (e) => e.indexOf("image/") === 0, Xe = 200;
function rs(e) {
  return new Promise((t) => {
    if (!e || !e.type || !ts(e.type)) {
      t("");
      return;
    }
    const r = new Image();
    if (r.onload = () => {
      const {
        width: o,
        height: n
      } = r, i = o / n, s = i > 1 ? Xe : Xe * i, a = i > 1 ? Xe / i : Xe, l = document.createElement("canvas");
      l.width = s, l.height = a, l.style.cssText = `position: fixed; left: 0; top: 0; width: ${s}px; height: ${a}px; z-index: 9999; display: none;`, document.body.appendChild(l), l.getContext("2d").drawImage(r, 0, 0, s, a);
      const p = l.toDataURL();
      document.body.removeChild(l), window.URL.revokeObjectURL(r.src), t(p);
    }, r.crossOrigin = "anonymous", e.type.startsWith("image/svg+xml")) {
      const o = new FileReader();
      o.onload = () => {
        o.result && typeof o.result == "string" && (r.src = o.result);
      }, o.readAsDataURL(e);
    } else if (e.type.startsWith("image/gif")) {
      const o = new FileReader();
      o.onload = () => {
        o.result && t(o.result);
      }, o.readAsDataURL(e);
    } else
      r.src = window.URL.createObjectURL(e);
  });
}
function ns() {
  return /* @__PURE__ */ c.createElement("svg", {
    width: "1em",
    height: "1em",
    viewBox: "0 0 16 16",
    version: "1.1",
    xmlns: "http://www.w3.org/2000/svg"
    //xmlnsXlink="http://www.w3.org/1999/xlink"
  }, /* @__PURE__ */ c.createElement("title", null, "audio"), /* @__PURE__ */ c.createElement("g", {
    stroke: "none",
    strokeWidth: "1",
    fill: "none",
    fillRule: "evenodd"
  }, /* @__PURE__ */ c.createElement("path", {
    d: "M14.1178571,4.0125 C14.225,4.11964286 14.2857143,4.26428571 14.2857143,4.41607143 L14.2857143,15.4285714 C14.2857143,15.7446429 14.0303571,16 13.7142857,16 L2.28571429,16 C1.96964286,16 1.71428571,15.7446429 1.71428571,15.4285714 L1.71428571,0.571428571 C1.71428571,0.255357143 1.96964286,0 2.28571429,0 L9.86964286,0 C10.0214286,0 10.1678571,0.0607142857 10.275,0.167857143 L14.1178571,4.0125 Z M10.7315824,7.11216117 C10.7428131,7.15148751 10.7485063,7.19218979 10.7485063,7.23309113 L10.7485063,8.07742614 C10.7484199,8.27364959 10.6183424,8.44607275 10.4296853,8.50003683 L8.32984514,9.09986306 L8.32984514,11.7071803 C8.32986605,12.5367078 7.67249692,13.217028 6.84345686,13.2454634 L6.79068592,13.2463395 C6.12766108,13.2463395 5.53916361,12.8217001 5.33010655,12.1924966 C5.1210495,11.563293 5.33842118,10.8709227 5.86959669,10.4741173 C6.40077221,10.0773119 7.12636292,10.0652587 7.67042486,10.4442027 L7.67020842,7.74937024 L7.68449368,7.74937024 C7.72405122,7.59919041 7.83988806,7.48101083 7.98924584,7.4384546 L10.1880418,6.81004755 C10.42156,6.74340323 10.6648954,6.87865515 10.7315824,7.11216117 Z M9.60714286,1.31785714 L12.9678571,4.67857143 L9.60714286,4.67857143 L9.60714286,1.31785714 Z",
    fill: "currentColor"
  })));
}
function os(e) {
  const {
    percent: t
  } = e, {
    token: r
  } = Qe.useToken();
  return /* @__PURE__ */ c.createElement(wn, {
    type: "circle",
    percent: t,
    size: r.fontSizeHeading2 * 2,
    strokeColor: "#FFF",
    trailColor: "rgba(255, 255, 255, 0.3)",
    format: (o) => /* @__PURE__ */ c.createElement("span", {
      style: {
        color: "#FFF"
      }
    }, (o || 0).toFixed(0), "%")
  });
}
function is() {
  return /* @__PURE__ */ c.createElement("svg", {
    width: "1em",
    height: "1em",
    viewBox: "0 0 16 16",
    version: "1.1",
    xmlns: "http://www.w3.org/2000/svg"
    // xmlnsXlink="http://www.w3.org/1999/xlink"
  }, /* @__PURE__ */ c.createElement("title", null, "video"), /* @__PURE__ */ c.createElement("g", {
    stroke: "none",
    strokeWidth: "1",
    fill: "none",
    fillRule: "evenodd"
  }, /* @__PURE__ */ c.createElement("path", {
    d: "M14.1178571,4.0125 C14.225,4.11964286 14.2857143,4.26428571 14.2857143,4.41607143 L14.2857143,15.4285714 C14.2857143,15.7446429 14.0303571,16 13.7142857,16 L2.28571429,16 C1.96964286,16 1.71428571,15.7446429 1.71428571,15.4285714 L1.71428571,0.571428571 C1.71428571,0.255357143 1.96964286,0 2.28571429,0 L9.86964286,0 C10.0214286,0 10.1678571,0.0607142857 10.275,0.167857143 L14.1178571,4.0125 Z M12.9678571,4.67857143 L9.60714286,1.31785714 L9.60714286,4.67857143 L12.9678571,4.67857143 Z M10.5379461,10.3101106 L6.68957555,13.0059749 C6.59910784,13.0693494 6.47439406,13.0473861 6.41101953,12.9569184 C6.3874624,12.9232903 6.37482581,12.8832269 6.37482581,12.8421686 L6.37482581,7.45043999 C6.37482581,7.33998304 6.46436886,7.25043999 6.57482581,7.25043999 C6.61588409,7.25043999 6.65594753,7.26307658 6.68957555,7.28663371 L10.5379461,9.98249803 C10.6284138,10.0458726 10.6503772,10.1705863 10.5870027,10.2610541 C10.5736331,10.2801392 10.5570312,10.2967411 10.5379461,10.3101106 Z",
    fill: "currentColor"
  })));
}
const Rt = " ", zt = "#8c8c8c", sn = ["png", "jpg", "jpeg", "gif", "bmp", "webp", "svg"], ss = [{
  icon: /* @__PURE__ */ c.createElement(Ln, null),
  color: "#22b35e",
  ext: ["xlsx", "xls"]
}, {
  icon: /* @__PURE__ */ c.createElement(Rn, null),
  color: zt,
  ext: sn
}, {
  icon: /* @__PURE__ */ c.createElement(In, null),
  color: zt,
  ext: ["md", "mdx"]
}, {
  icon: /* @__PURE__ */ c.createElement(Tn, null),
  color: "#ff4d4f",
  ext: ["pdf"]
}, {
  icon: /* @__PURE__ */ c.createElement(Pn, null),
  color: "#ff6e31",
  ext: ["ppt", "pptx"]
}, {
  icon: /* @__PURE__ */ c.createElement(Mn, null),
  color: "#1677ff",
  ext: ["doc", "docx"]
}, {
  icon: /* @__PURE__ */ c.createElement(On, null),
  color: "#fab714",
  ext: ["zip", "rar", "7z", "tar", "gz"]
}, {
  icon: /* @__PURE__ */ c.createElement(is, null),
  color: "#ff4d4f",
  ext: ["mp4", "avi", "mov", "wmv", "flv", "mkv"]
}, {
  icon: /* @__PURE__ */ c.createElement(ns, null),
  color: "#8c8c8c",
  ext: ["mp3", "wav", "flac", "ape", "aac", "ogg"]
}];
function Lr(e, t) {
  return t.some((r) => e.toLowerCase() === `.${r}`);
}
function as(e) {
  let t = e;
  const r = ["B", "KB", "MB", "GB", "TB", "PB", "EB"];
  let o = 0;
  for (; t >= 1024 && o < r.length - 1; )
    t /= 1024, o++;
  return `${t.toFixed(0)} ${r[o]}`;
}
function ls(e, t) {
  const {
    prefixCls: r,
    item: o,
    onRemove: n,
    className: i,
    style: s,
    imageProps: a
  } = e, l = c.useContext(Ne), {
    disabled: u
  } = l || {}, {
    name: p,
    size: f,
    percent: d,
    status: m = "done",
    description: b
  } = o, {
    getPrefixCls: w
  } = Ye(), g = w("attachment", r), y = `${g}-list-card`, [E, C, h] = on(g), [x, v] = c.useMemo(() => {
    const D = p || "", U = D.match(/^(.*)\.[^.]+$/);
    return U ? [U[1], D.slice(U[1].length)] : [D, ""];
  }, [p]), L = c.useMemo(() => Lr(v, sn), [v]), S = c.useMemo(() => b || (m === "uploading" ? `${d || 0}%` : m === "error" ? o.response || Rt : f ? as(f) : Rt), [m, d]), [T, $] = c.useMemo(() => {
    for (const {
      ext: D,
      icon: U,
      color: W
    } of ss)
      if (Lr(v, D))
        return [U, W];
    return [/* @__PURE__ */ c.createElement(Cn, {
      key: "defaultIcon"
    }), zt];
  }, [v]), [k, _] = c.useState();
  c.useEffect(() => {
    if (o.originFileObj) {
      let D = !0;
      return rs(o.originFileObj).then((U) => {
        D && _(U);
      }), () => {
        D = !1;
      };
    }
    _(void 0);
  }, [o.originFileObj]);
  let M = null;
  const P = o.thumbUrl || o.url || k, O = L && (o.originFileObj || P);
  return O ? M = /* @__PURE__ */ c.createElement(c.Fragment, null, P && /* @__PURE__ */ c.createElement(xn, Te({
    alt: "preview",
    src: P
  }, a)), m !== "done" && /* @__PURE__ */ c.createElement("div", {
    className: `${y}-img-mask`
  }, m === "uploading" && d !== void 0 && /* @__PURE__ */ c.createElement(os, {
    percent: d,
    prefixCls: y
  }), m === "error" && /* @__PURE__ */ c.createElement("div", {
    className: `${y}-desc`
  }, /* @__PURE__ */ c.createElement("div", {
    className: `${y}-ellipsis-prefix`
  }, S)))) : M = /* @__PURE__ */ c.createElement(c.Fragment, null, /* @__PURE__ */ c.createElement("div", {
    className: `${y}-icon`,
    style: {
      color: $
    }
  }, T), /* @__PURE__ */ c.createElement("div", {
    className: `${y}-content`
  }, /* @__PURE__ */ c.createElement("div", {
    className: `${y}-name`
  }, /* @__PURE__ */ c.createElement("div", {
    className: `${y}-ellipsis-prefix`
  }, x ?? Rt), /* @__PURE__ */ c.createElement("div", {
    className: `${y}-ellipsis-suffix`
  }, v)), /* @__PURE__ */ c.createElement("div", {
    className: `${y}-desc`
  }, /* @__PURE__ */ c.createElement("div", {
    className: `${y}-ellipsis-prefix`
  }, S)))), E(/* @__PURE__ */ c.createElement("div", {
    className: oe(y, {
      [`${y}-status-${m}`]: m,
      [`${y}-type-preview`]: O,
      [`${y}-type-overview`]: !O
    }, i, C, h),
    style: s,
    ref: t
  }, M, !u && n && /* @__PURE__ */ c.createElement("button", {
    type: "button",
    className: `${y}-remove`,
    onClick: () => {
      n(o);
    }
  }, /* @__PURE__ */ c.createElement(_n, null))));
}
const an = /* @__PURE__ */ c.forwardRef(ls), Rr = 1;
function cs(e) {
  const {
    prefixCls: t,
    items: r,
    onRemove: o,
    overflow: n,
    upload: i,
    listClassName: s,
    listStyle: a,
    itemClassName: l,
    itemStyle: u,
    imageProps: p
  } = e, f = `${t}-list`, d = c.useRef(null), [m, b] = c.useState(!1), {
    disabled: w
  } = c.useContext(Ne);
  c.useEffect(() => (b(!0), () => {
    b(!1);
  }), []);
  const [g, y] = c.useState(!1), [E, C] = c.useState(!1), h = () => {
    const S = d.current;
    S && (n === "scrollX" ? (y(Math.abs(S.scrollLeft) >= Rr), C(S.scrollWidth - S.clientWidth - Math.abs(S.scrollLeft) >= Rr)) : n === "scrollY" && (y(S.scrollTop !== 0), C(S.scrollHeight - S.clientHeight !== S.scrollTop)));
  };
  c.useEffect(() => {
    h();
  }, [n, r.length]);
  const x = (S) => {
    const T = d.current;
    T && T.scrollTo({
      left: T.scrollLeft + S * T.clientWidth,
      behavior: "smooth"
    });
  }, v = () => {
    x(-1);
  }, L = () => {
    x(1);
  };
  return /* @__PURE__ */ c.createElement("div", {
    className: oe(f, {
      [`${f}-overflow-${e.overflow}`]: n,
      [`${f}-overflow-ping-start`]: g,
      [`${f}-overflow-ping-end`]: E
    }, s),
    ref: d,
    onScroll: h,
    style: a
  }, /* @__PURE__ */ c.createElement(Ri, {
    keys: r.map((S) => ({
      key: S.uid,
      item: S
    })),
    motionName: `${f}-card-motion`,
    component: !1,
    motionAppear: m,
    motionLeave: !0,
    motionEnter: !0
  }, ({
    key: S,
    item: T,
    className: $,
    style: k
  }) => /* @__PURE__ */ c.createElement(an, {
    key: S,
    prefixCls: t,
    item: T,
    onRemove: o,
    className: oe($, l),
    imageProps: p,
    style: {
      ...k,
      ...u
    }
  })), !w && /* @__PURE__ */ c.createElement(Jr, {
    upload: i
  }, /* @__PURE__ */ c.createElement(ht, {
    className: `${f}-upload-btn`,
    type: "dashed"
  }, /* @__PURE__ */ c.createElement(Fn, {
    className: `${f}-upload-btn-icon`
  }))), n === "scrollX" && /* @__PURE__ */ c.createElement(c.Fragment, null, /* @__PURE__ */ c.createElement(ht, {
    size: "small",
    shape: "circle",
    className: `${f}-prev-btn`,
    icon: /* @__PURE__ */ c.createElement(An, null),
    onClick: v
  }), /* @__PURE__ */ c.createElement(ht, {
    size: "small",
    shape: "circle",
    className: `${f}-next-btn`,
    icon: /* @__PURE__ */ c.createElement($n, null),
    onClick: L
  })));
}
function us(e, t) {
  const {
    prefixCls: r,
    placeholder: o = {},
    upload: n,
    className: i,
    style: s
  } = e, a = `${r}-placeholder`, l = o || {}, {
    disabled: u
  } = c.useContext(Ne), [p, f] = c.useState(!1), d = () => {
    f(!0);
  }, m = (g) => {
    g.currentTarget.contains(g.relatedTarget) || f(!1);
  }, b = () => {
    f(!1);
  }, w = /* @__PURE__ */ c.isValidElement(o) ? o : /* @__PURE__ */ c.createElement(En, {
    align: "center",
    justify: "center",
    vertical: !0,
    className: `${a}-inner`
  }, /* @__PURE__ */ c.createElement(vt.Text, {
    className: `${a}-icon`
  }, l.icon), /* @__PURE__ */ c.createElement(vt.Title, {
    className: `${a}-title`,
    level: 5
  }, l.title), /* @__PURE__ */ c.createElement(vt.Text, {
    className: `${a}-description`,
    type: "secondary"
  }, l.description));
  return /* @__PURE__ */ c.createElement("div", {
    className: oe(a, {
      [`${a}-drag-in`]: p,
      [`${a}-disabled`]: u
    }, i),
    onDragEnter: d,
    onDragLeave: m,
    onDrop: b,
    "aria-hidden": u,
    style: s
  }, /* @__PURE__ */ c.createElement(Tr.Dragger, Te({
    showUploadList: !1
  }, n, {
    ref: t,
    style: {
      padding: 0,
      border: 0,
      background: "transparent"
    }
  }), w));
}
const fs = /* @__PURE__ */ c.forwardRef(us);
function ds(e, t) {
  const {
    prefixCls: r,
    rootClassName: o,
    rootStyle: n,
    className: i,
    style: s,
    items: a,
    children: l,
    getDropContainer: u,
    placeholder: p,
    onChange: f,
    onRemove: d,
    overflow: m,
    imageProps: b,
    disabled: w,
    classNames: g = {},
    styles: y = {},
    ...E
  } = e, {
    getPrefixCls: C,
    direction: h
  } = Ye(), x = C("attachment", r), v = Ao("attachments"), {
    classNames: L,
    styles: S
  } = v, T = c.useRef(null), $ = c.useRef(null);
  c.useImperativeHandle(t, () => ({
    nativeElement: T.current,
    upload: (N) => {
      var H, Z;
      const G = (Z = (H = $.current) == null ? void 0 : H.nativeElement) == null ? void 0 : Z.querySelector('input[type="file"]');
      if (G) {
        const pe = new DataTransfer();
        pe.items.add(N), G.files = pe.files, G.dispatchEvent(new Event("change", {
          bubbles: !0
        }));
      }
    }
  }));
  const [k, _, M] = on(x), P = oe(_, M), [O, D] = zo([], {
    value: a
  }), U = Pe((N) => {
    D(N.fileList), f == null || f(N);
  }), W = {
    ...E,
    fileList: O,
    onChange: U
  }, ge = (N) => Promise.resolve(typeof d == "function" ? d(N) : d).then((G) => {
    if (G === !1)
      return;
    const H = O.filter((Z) => Z.uid !== N.uid);
    U({
      file: {
        ...N,
        status: "removed"
      },
      fileList: H
    });
  });
  let ce;
  const V = (N, G, H) => {
    const Z = typeof p == "function" ? p(N) : p;
    return /* @__PURE__ */ c.createElement(fs, {
      placeholder: Z,
      upload: W,
      prefixCls: x,
      className: oe(L.placeholder, g.placeholder),
      style: {
        ...S.placeholder,
        ...y.placeholder,
        ...G == null ? void 0 : G.style
      },
      ref: H
    });
  };
  if (l)
    ce = /* @__PURE__ */ c.createElement(c.Fragment, null, /* @__PURE__ */ c.createElement(Jr, {
      upload: W,
      rootClassName: o,
      ref: $
    }, l), /* @__PURE__ */ c.createElement(lr, {
      getDropContainer: u,
      prefixCls: x,
      className: oe(P, o)
    }, V("drop")));
  else {
    const N = O.length > 0;
    ce = /* @__PURE__ */ c.createElement("div", {
      className: oe(x, P, {
        [`${x}-rtl`]: h === "rtl"
      }, i, o),
      style: {
        ...n,
        ...s
      },
      dir: h || "ltr",
      ref: T
    }, /* @__PURE__ */ c.createElement(cs, {
      prefixCls: x,
      items: O,
      onRemove: ge,
      overflow: m,
      upload: W,
      listClassName: oe(L.list, g.list),
      listStyle: {
        ...S.list,
        ...y.list,
        ...!N && {
          display: "none"
        }
      },
      itemClassName: oe(L.item, g.item),
      itemStyle: {
        ...S.item,
        ...y.item
      },
      imageProps: b
    }), V("inline", N ? {
      style: {
        display: "none"
      }
    } : {}, $), /* @__PURE__ */ c.createElement(lr, {
      getDropContainer: u || (() => T.current),
      prefixCls: x,
      className: P
    }, V("drop")));
  }
  return k(/* @__PURE__ */ c.createElement(Ne.Provider, {
    value: {
      disabled: w
    }
  }, ce));
}
const ln = /* @__PURE__ */ c.forwardRef(ds);
ln.FileCard = an;
function ps(e) {
  return /^(?:async\s+)?(?:function\s*(?:\w*\s*)?\(|\([\w\s,=]*\)\s*=>|\(\{[\w\s,=]*\}\)\s*=>|function\s*\*\s*\w*\s*\()/i.test(e.trim());
}
function ms(e, t = !1) {
  try {
    if (vn(e))
      return e;
    if (t && !ps(e))
      return;
    if (typeof e == "string") {
      let r = e.trim();
      return r.startsWith(";") && (r = r.slice(1)), r.endsWith(";") && (r = r.slice(0, -1)), new Function(`return (...args) => (${r})(...args)`)();
    }
    return;
  } catch {
    return;
  }
}
function Q(e, t) {
  return tt(() => ms(e, t), [e, t]);
}
function gs(e, t) {
  const r = tt(() => c.Children.toArray(e.originalChildren || e).filter((i) => i.props.node && !i.props.node.ignore && (!i.props.nodeSlotKey || t)).sort((i, s) => {
    if (i.props.node.slotIndex && s.props.node.slotIndex) {
      const a = $e(i.props.node.slotIndex) || 0, l = $e(s.props.node.slotIndex) || 0;
      return a - l === 0 && i.props.node.subSlotIndex && s.props.node.subSlotIndex ? ($e(i.props.node.subSlotIndex) || 0) - ($e(s.props.node.subSlotIndex) || 0) : a - l;
    }
    return 0;
  }).map((i) => i.props.node.target), [e, t]);
  return Lo(r);
}
function hs(e, t) {
  return Object.keys(e).reduce((r, o) => (e[o] !== void 0 && (r[o] = e[o]), r), {});
}
const vs = ({
  children: e,
  ...t
}) => /* @__PURE__ */ Y.jsx(Y.Fragment, {
  children: e(t)
});
function ys(e) {
  return c.createElement(vs, {
    children: e
  });
}
function Ir(e, t) {
  return e ? t != null && t.forceClone || t != null && t.params ? ys((r) => /* @__PURE__ */ Y.jsx(bn, {
    forceClone: t == null ? void 0 : t.forceClone,
    params: t == null ? void 0 : t.params,
    children: /* @__PURE__ */ Y.jsx(ke, {
      slot: e,
      clone: t == null ? void 0 : t.clone,
      ...r
    })
  })) : /* @__PURE__ */ Y.jsx(ke, {
    slot: e,
    clone: t == null ? void 0 : t.clone
  }) : null;
}
function ne({
  key: e,
  slots: t,
  targets: r
}, o) {
  return t[e] ? (...n) => r ? r.map((i, s) => /* @__PURE__ */ Y.jsx(c.Fragment, {
    children: Ir(i, {
      clone: !0,
      params: n,
      forceClone: !0
    })
  }, s)) : /* @__PURE__ */ Y.jsx(Y.Fragment, {
    children: Ir(t[e], {
      clone: !0,
      params: n,
      forceClone: !0
    })
  }) : void 0;
}
const bs = (e) => !!e.name;
function It(e) {
  return typeof e == "object" && e !== null ? e : {};
}
const xs = Co(({
  slots: e,
  upload: t,
  showUploadList: r,
  progress: o,
  beforeUpload: n,
  customRequest: i,
  previewFile: s,
  isImageUrl: a,
  itemRender: l,
  iconRender: u,
  data: p,
  onChange: f,
  onValueChange: d,
  onRemove: m,
  items: b,
  setSlotParams: w,
  placeholder: g,
  getDropContainer: y,
  children: E,
  maxCount: C,
  imageProps: h,
  ...x
}) => {
  const v = It(h == null ? void 0 : h.preview), L = e["imageProps.preview.mask"] || e["imageProps.preview.closeIcon"] || e["imageProps.preview.toolbarRender"] || e["imageProps.preview.imageRender"] || (h == null ? void 0 : h.preview) !== !1, S = Q(v.getContainer), T = Q(v.toolbarRender), $ = Q(v.imageRender), k = e["showUploadList.downloadIcon"] || e["showUploadList.removeIcon"] || e["showUploadList.previewIcon"] || e["showUploadList.extra"] || typeof r == "object", _ = It(r), M = e["placeholder.title"] || e["placeholder.description"] || e["placeholder.icon"] || typeof g == "object", P = It(g), O = Q(_.showPreviewIcon), D = Q(_.showRemoveIcon), U = Q(_.showDownloadIcon), W = Q(n), ge = Q(i), ce = Q(o == null ? void 0 : o.format), V = Q(s), N = Q(a), G = Q(l), H = Q(u), Z = Q(g, !0), pe = Q(y), ae = Q(p), [Fe, me] = qe(!1), [ue, he] = qe(b);
  xe(() => {
    he(b);
  }, [b]);
  const fe = tt(() => {
    const te = {};
    return ue.map((j) => {
      if (!bs(j)) {
        const re = j.uid || j.url || j.path;
        return te[re] || (te[re] = 0), te[re]++, {
          ...j,
          name: j.orig_name || j.path,
          uid: j.uid || re + "-" + te[re],
          status: "done"
        };
      }
      return j;
    }) || [];
  }, [ue]), Se = gs(E), Ce = x.disabled || Fe;
  return /* @__PURE__ */ Y.jsxs(Y.Fragment, {
    children: [/* @__PURE__ */ Y.jsx("div", {
      style: {
        display: "none"
      },
      children: Se.length > 0 ? null : E
    }), /* @__PURE__ */ Y.jsx(ln, {
      ...x,
      disabled: Ce,
      imageProps: {
        ...h,
        preview: L ? hs({
          ...v,
          getContainer: S,
          toolbarRender: e["imageProps.preview.toolbarRender"] ? ne({
            slots: e,
            key: "imageProps.preview.toolbarRender"
          }) : T,
          imageRender: e["imageProps.preview.imageRender"] ? ne({
            slots: e,
            key: "imageProps.preview.imageRender"
          }) : $,
          ...e["imageProps.preview.mask"] || Reflect.has(v, "mask") ? {
            mask: e["imageProps.preview.mask"] ? /* @__PURE__ */ Y.jsx(ke, {
              slot: e["imageProps.preview.mask"]
            }) : v.mask
          } : {},
          closeIcon: e["imageProps.preview.closeIcon"] ? /* @__PURE__ */ Y.jsx(ke, {
            slot: e["imageProps.preview.closeIcon"]
          }) : v.closeIcon
        }) : !1,
        placeholder: e["imageProps.placeholder"] ? /* @__PURE__ */ Y.jsx(ke, {
          slot: e["imageProps.placeholder"]
        }) : h == null ? void 0 : h.placeholder
      },
      getDropContainer: pe,
      placeholder: e.placeholder ? ne({
        slots: e,
        key: "placeholder"
      }) : M ? (...te) => {
        var j, re, ve;
        return {
          ...P,
          icon: e["placeholder.icon"] ? (j = ne({
            slots: e,
            key: "placeholder.icon"
          })) == null ? void 0 : j(...te) : P.icon,
          title: e["placeholder.title"] ? (re = ne({
            slots: e,
            key: "placeholder.title"
          })) == null ? void 0 : re(...te) : P.title,
          description: e["placeholder.description"] ? (ve = ne({
            slots: e,
            key: "placeholder.description"
          })) == null ? void 0 : ve(...te) : P.description
        };
      } : Z || g,
      items: fe,
      data: ae || p,
      previewFile: V,
      isImageUrl: N,
      itemRender: e.itemRender ? ne({
        slots: e,
        key: "itemRender"
      }) : G,
      iconRender: e.iconRender ? ne({
        slots: e,
        key: "iconRender"
      }) : H,
      maxCount: C,
      onChange: async (te) => {
        try {
          const j = te.file, re = te.fileList, ve = fe.findIndex((K) => K.uid === j.uid);
          if (ve !== -1) {
            if (Ce)
              return;
            m == null || m(j);
            const K = ue.slice();
            K.splice(ve, 1), d == null || d(K), f == null || f(K.map((we) => we.path));
          } else {
            if (W && !await W(j, re) || Ce)
              return;
            me(!0);
            let K = re.filter((z) => z.status !== "done");
            if (C === 1)
              K = K.slice(0, 1);
            else if (K.length === 0) {
              me(!1);
              return;
            } else if (typeof C == "number") {
              const z = C - ue.length;
              K = K.slice(0, z < 0 ? 0 : z);
            }
            const we = ue, q = K.map((z) => ({
              ...z,
              size: z.size,
              uid: z.uid,
              name: z.name,
              status: "uploading"
            }));
            he((z) => [...C === 1 ? [] : z, ...q]);
            const B = (await t(K.map((z) => z.originFileObj))).filter(Boolean).map((z, _e) => ({
              ...z,
              uid: q[_e].uid
            })), J = C === 1 ? B : [...we, ...B];
            me(!1), he(J), d == null || d(J), f == null || f(J.map((z) => z.path));
          }
        } catch (j) {
          console.error(j), me(!1);
        }
      },
      customRequest: ge || Gn,
      progress: o && {
        ...o,
        format: ce
      },
      showUploadList: k ? {
        ..._,
        showDownloadIcon: U || _.showDownloadIcon,
        showRemoveIcon: D || _.showRemoveIcon,
        showPreviewIcon: O || _.showPreviewIcon,
        downloadIcon: e["showUploadList.downloadIcon"] ? ne({
          slots: e,
          key: "showUploadList.downloadIcon"
        }) : _.downloadIcon,
        removeIcon: e["showUploadList.removeIcon"] ? ne({
          slots: e,
          key: "showUploadList.removeIcon"
        }) : _.removeIcon,
        previewIcon: e["showUploadList.previewIcon"] ? ne({
          slots: e,
          key: "showUploadList.previewIcon"
        }) : _.previewIcon,
        extra: e["showUploadList.extra"] ? ne({
          slots: e,
          key: "showUploadList.extra"
        }) : _.extra
      } : r,
      children: Se.length > 0 ? E : void 0
    })]
  });
});
export {
  xs as Attachments,
  xs as default
};
