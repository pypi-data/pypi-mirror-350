var Ht = (e) => {
  throw TypeError(e);
};
var Bt = (e, t, r) => t.has(e) || Ht("Cannot " + r);
var de = (e, t, r) => (Bt(e, t, "read from private field"), r ? r.call(e) : t.get(e)), Vt = (e, t, r) => t.has(e) ? Ht("Cannot add the same private member more than once") : t instanceof WeakSet ? t.add(e) : t.set(e, r), Ut = (e, t, r, n) => (Bt(e, t, "write to private field"), n ? n.call(e, r) : t.set(e, r), r);
import { i as bn, a as wt, r as yn, w as De, g as Sn, b as xn, c as Z } from "./Index-B4AMkQxh.js";
const M = window.ms_globals.React, l = window.ms_globals.React, pn = window.ms_globals.React.forwardRef, se = window.ms_globals.React.useRef, mn = window.ms_globals.React.useState, xe = window.ms_globals.React.useEffect, Mr = window.ms_globals.React.useMemo, gn = window.ms_globals.React.version, hn = window.ms_globals.React.isValidElement, vn = window.ms_globals.React.useLayoutEffect, Xt = window.ms_globals.ReactDOM, He = window.ms_globals.ReactDOM.createPortal, wn = window.ms_globals.internalContext.useContextPropsContext, En = window.ms_globals.internalContext.ContextPropsProvider, Cn = window.ms_globals.antd.ConfigProvider, Ir = window.ms_globals.antd.Upload, Be = window.ms_globals.antd.theme, _n = window.ms_globals.antd.Progress, Rn = window.ms_globals.antd.Image, ct = window.ms_globals.antd.Button, Tn = window.ms_globals.antd.Flex, ut = window.ms_globals.antd.Typography, Ln = window.ms_globals.antdIcons.FileTextFilled, Pn = window.ms_globals.antdIcons.CloseCircleFilled, Mn = window.ms_globals.antdIcons.FileExcelFilled, In = window.ms_globals.antdIcons.FileImageFilled, On = window.ms_globals.antdIcons.FileMarkdownFilled, $n = window.ms_globals.antdIcons.FilePdfFilled, An = window.ms_globals.antdIcons.FilePptFilled, Fn = window.ms_globals.antdIcons.FileWordFilled, kn = window.ms_globals.antdIcons.FileZipFilled, jn = window.ms_globals.antdIcons.PlusOutlined, Dn = window.ms_globals.antdIcons.LeftOutlined, Nn = window.ms_globals.antdIcons.RightOutlined, Wt = window.ms_globals.antdCssinjs.unit, ft = window.ms_globals.antdCssinjs.token2CSSVar, Gt = window.ms_globals.antdCssinjs.useStyleRegister, zn = window.ms_globals.antdCssinjs.useCSSVarRegister, Hn = window.ms_globals.antdCssinjs.createTheme, Bn = window.ms_globals.antdCssinjs.useCacheToken;
var Vn = /\s/;
function Un(e) {
  for (var t = e.length; t-- && Vn.test(e.charAt(t)); )
    ;
  return t;
}
var Xn = /^\s+/;
function Wn(e) {
  return e && e.slice(0, Un(e) + 1).replace(Xn, "");
}
var qt = NaN, Gn = /^[-+]0x[0-9a-f]+$/i, qn = /^0b[01]+$/i, Kn = /^0o[0-7]+$/i, Zn = parseInt;
function Kt(e) {
  if (typeof e == "number")
    return e;
  if (bn(e))
    return qt;
  if (wt(e)) {
    var t = typeof e.valueOf == "function" ? e.valueOf() : e;
    e = wt(t) ? t + "" : t;
  }
  if (typeof e != "string")
    return e === 0 ? e : +e;
  e = Wn(e);
  var r = qn.test(e);
  return r || Kn.test(e) ? Zn(e.slice(2), r ? 2 : 8) : Gn.test(e) ? qt : +e;
}
var dt = function() {
  return yn.Date.now();
}, Qn = "Expected a function", Yn = Math.max, Jn = Math.min;
function eo(e, t, r) {
  var n, o, i, s, a, c, u = 0, p = !1, f = !1, d = !0;
  if (typeof e != "function")
    throw new TypeError(Qn);
  t = Kt(t) || 0, wt(r) && (p = !!r.leading, f = "maxWait" in r, i = f ? Yn(Kt(r.maxWait) || 0, t) : i, d = "trailing" in r ? !!r.trailing : d);
  function m(v) {
    var _ = n, y = o;
    return n = o = void 0, u = v, s = e.apply(y, _), s;
  }
  function b(v) {
    return u = v, a = setTimeout(h, t), p ? m(v) : s;
  }
  function x(v) {
    var _ = v - c, y = v - u, L = t - _;
    return f ? Jn(L, i - y) : L;
  }
  function g(v) {
    var _ = v - c, y = v - u;
    return c === void 0 || _ >= t || _ < 0 || f && y >= i;
  }
  function h() {
    var v = dt();
    if (g(v))
      return E(v);
    a = setTimeout(h, x(v));
  }
  function E(v) {
    return a = void 0, d && n ? m(v) : (n = o = void 0, s);
  }
  function T() {
    a !== void 0 && clearTimeout(a), u = 0, n = c = o = a = void 0;
  }
  function S() {
    return a === void 0 ? s : E(dt());
  }
  function w() {
    var v = dt(), _ = g(v);
    if (n = arguments, o = this, c = v, _) {
      if (a === void 0)
        return b(c);
      if (f)
        return clearTimeout(a), a = setTimeout(h, t), m(c);
    }
    return a === void 0 && (a = setTimeout(h, t)), s;
  }
  return w.cancel = T, w.flush = S, w;
}
var Or = {
  exports: {}
}, We = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var to = l, ro = Symbol.for("react.element"), no = Symbol.for("react.fragment"), oo = Object.prototype.hasOwnProperty, io = to.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, so = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function $r(e, t, r) {
  var n, o = {}, i = null, s = null;
  r !== void 0 && (i = "" + r), t.key !== void 0 && (i = "" + t.key), t.ref !== void 0 && (s = t.ref);
  for (n in t) oo.call(t, n) && !so.hasOwnProperty(n) && (o[n] = t[n]);
  if (e && e.defaultProps) for (n in t = e.defaultProps, t) o[n] === void 0 && (o[n] = t[n]);
  return {
    $$typeof: ro,
    type: e,
    key: i,
    ref: s,
    props: o,
    _owner: io.current
  };
}
We.Fragment = no;
We.jsx = $r;
We.jsxs = $r;
Or.exports = We;
var U = Or.exports;
const {
  SvelteComponent: ao,
  assign: Zt,
  binding_callbacks: Qt,
  check_outros: lo,
  children: Ar,
  claim_element: Fr,
  claim_space: co,
  component_subscribe: Yt,
  compute_slots: uo,
  create_slot: fo,
  detach: pe,
  element: kr,
  empty: Jt,
  exclude_internal_props: er,
  get_all_dirty_from_scope: po,
  get_slot_changes: mo,
  group_outros: go,
  init: ho,
  insert_hydration: Ne,
  safe_not_equal: vo,
  set_custom_element_data: jr,
  space: bo,
  transition_in: ze,
  transition_out: Et,
  update_slot_base: yo
} = window.__gradio__svelte__internal, {
  beforeUpdate: So,
  getContext: xo,
  onDestroy: wo,
  setContext: Eo
} = window.__gradio__svelte__internal;
function tr(e) {
  let t, r;
  const n = (
    /*#slots*/
    e[7].default
  ), o = fo(
    n,
    e,
    /*$$scope*/
    e[6],
    null
  );
  return {
    c() {
      t = kr("svelte-slot"), o && o.c(), this.h();
    },
    l(i) {
      t = Fr(i, "SVELTE-SLOT", {
        class: !0
      });
      var s = Ar(t);
      o && o.l(s), s.forEach(pe), this.h();
    },
    h() {
      jr(t, "class", "svelte-1rt0kpf");
    },
    m(i, s) {
      Ne(i, t, s), o && o.m(t, null), e[9](t), r = !0;
    },
    p(i, s) {
      o && o.p && (!r || s & /*$$scope*/
      64) && yo(
        o,
        n,
        i,
        /*$$scope*/
        i[6],
        r ? mo(
          n,
          /*$$scope*/
          i[6],
          s,
          null
        ) : po(
          /*$$scope*/
          i[6]
        ),
        null
      );
    },
    i(i) {
      r || (ze(o, i), r = !0);
    },
    o(i) {
      Et(o, i), r = !1;
    },
    d(i) {
      i && pe(t), o && o.d(i), e[9](null);
    }
  };
}
function Co(e) {
  let t, r, n, o, i = (
    /*$$slots*/
    e[4].default && tr(e)
  );
  return {
    c() {
      t = kr("react-portal-target"), r = bo(), i && i.c(), n = Jt(), this.h();
    },
    l(s) {
      t = Fr(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), Ar(t).forEach(pe), r = co(s), i && i.l(s), n = Jt(), this.h();
    },
    h() {
      jr(t, "class", "svelte-1rt0kpf");
    },
    m(s, a) {
      Ne(s, t, a), e[8](t), Ne(s, r, a), i && i.m(s, a), Ne(s, n, a), o = !0;
    },
    p(s, [a]) {
      /*$$slots*/
      s[4].default ? i ? (i.p(s, a), a & /*$$slots*/
      16 && ze(i, 1)) : (i = tr(s), i.c(), ze(i, 1), i.m(n.parentNode, n)) : i && (go(), Et(i, 1, 1, () => {
        i = null;
      }), lo());
    },
    i(s) {
      o || (ze(i), o = !0);
    },
    o(s) {
      Et(i), o = !1;
    },
    d(s) {
      s && (pe(t), pe(r), pe(n)), e[8](null), i && i.d(s);
    }
  };
}
function rr(e) {
  const {
    svelteInit: t,
    ...r
  } = e;
  return r;
}
function _o(e, t, r) {
  let n, o, {
    $$slots: i = {},
    $$scope: s
  } = t;
  const a = uo(i);
  let {
    svelteInit: c
  } = t;
  const u = De(rr(t)), p = De();
  Yt(e, p, (S) => r(0, n = S));
  const f = De();
  Yt(e, f, (S) => r(1, o = S));
  const d = [], m = xo("$$ms-gr-react-wrapper"), {
    slotKey: b,
    slotIndex: x,
    subSlotIndex: g
  } = Sn() || {}, h = c({
    parent: m,
    props: u,
    target: p,
    slot: f,
    slotKey: b,
    slotIndex: x,
    subSlotIndex: g,
    onDestroy(S) {
      d.push(S);
    }
  });
  Eo("$$ms-gr-react-wrapper", h), So(() => {
    u.set(rr(t));
  }), wo(() => {
    d.forEach((S) => S());
  });
  function E(S) {
    Qt[S ? "unshift" : "push"](() => {
      n = S, p.set(n);
    });
  }
  function T(S) {
    Qt[S ? "unshift" : "push"](() => {
      o = S, f.set(o);
    });
  }
  return e.$$set = (S) => {
    r(17, t = Zt(Zt({}, t), er(S))), "svelteInit" in S && r(5, c = S.svelteInit), "$$scope" in S && r(6, s = S.$$scope);
  }, t = er(t), [n, o, p, f, a, c, s, i, E, T];
}
class Ro extends ao {
  constructor(t) {
    super(), ho(this, t, _o, Co, vo, {
      svelteInit: 5
    });
  }
}
const {
  SvelteComponent: Rs
} = window.__gradio__svelte__internal, nr = window.ms_globals.rerender, pt = window.ms_globals.tree;
function To(e, t = {}) {
  function r(n) {
    const o = De(), i = new Ro({
      ...n,
      props: {
        svelteInit(s) {
          window.ms_globals.autokey += 1;
          const a = {
            key: window.ms_globals.autokey,
            svelteInstance: o,
            reactComponent: e,
            props: s.props,
            slot: s.slot,
            target: s.target,
            slotIndex: s.slotIndex,
            subSlotIndex: s.subSlotIndex,
            ignore: t.ignore,
            slotKey: s.slotKey,
            nodes: []
          }, c = s.parent ?? pt;
          return c.nodes = [...c.nodes, a], nr({
            createPortal: He,
            node: pt
          }), s.onDestroy(() => {
            c.nodes = c.nodes.filter((u) => u.svelteInstance !== o), nr({
              createPortal: He,
              node: pt
            });
          }), a;
        },
        ...n.props
      }
    });
    return o.set(i), i;
  }
  return new Promise((n) => {
    window.ms_globals.initializePromise.then(() => {
      n(r);
    });
  });
}
const Lo = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Po(e) {
  return e ? Object.keys(e).reduce((t, r) => {
    const n = e[r];
    return t[r] = Mo(r, n), t;
  }, {}) : {};
}
function Mo(e, t) {
  return typeof t == "number" && !Lo.includes(e) ? t + "px" : t;
}
function Ct(e) {
  const t = [], r = e.cloneNode(!1);
  if (e._reactElement) {
    const o = l.Children.toArray(e._reactElement.props.children).map((i) => {
      if (l.isValidElement(i) && i.props.__slot__) {
        const {
          portals: s,
          clonedElement: a
        } = Ct(i.props.el);
        return l.cloneElement(i, {
          ...i.props,
          el: a,
          children: [...l.Children.toArray(i.props.children), ...s]
        });
      }
      return null;
    });
    return o.originalChildren = e._reactElement.props.children, t.push(He(l.cloneElement(e._reactElement, {
      ...e._reactElement.props,
      children: o
    }), r)), {
      clonedElement: r,
      portals: t
    };
  }
  Object.keys(e.getEventListeners()).forEach((o) => {
    e.getEventListeners(o).forEach(({
      listener: s,
      type: a,
      useCapture: c
    }) => {
      r.addEventListener(a, s, c);
    });
  });
  const n = Array.from(e.childNodes);
  for (let o = 0; o < n.length; o++) {
    const i = n[o];
    if (i.nodeType === 1) {
      const {
        clonedElement: s,
        portals: a
      } = Ct(i);
      t.push(...a), r.appendChild(s);
    } else i.nodeType === 3 && r.appendChild(i.cloneNode());
  }
  return {
    clonedElement: r,
    portals: t
  };
}
function Io(e, t) {
  e && (typeof e == "function" ? e(t) : e.current = t);
}
const we = pn(({
  slot: e,
  clone: t,
  className: r,
  style: n,
  observeAttributes: o
}, i) => {
  const s = se(), [a, c] = mn([]), {
    forceClone: u
  } = wn(), p = u ? !0 : t;
  return xe(() => {
    var x;
    if (!s.current || !e)
      return;
    let f = e;
    function d() {
      let g = f;
      if (f.tagName.toLowerCase() === "svelte-slot" && f.children.length === 1 && f.children[0] && (g = f.children[0], g.tagName.toLowerCase() === "react-portal-target" && g.children[0] && (g = g.children[0])), Io(i, g), r && g.classList.add(...r.split(" ")), n) {
        const h = Po(n);
        Object.keys(h).forEach((E) => {
          g.style[E] = h[E];
        });
      }
    }
    let m = null, b = null;
    if (p && window.MutationObserver) {
      let g = function() {
        var S, w, v;
        (S = s.current) != null && S.contains(f) && ((w = s.current) == null || w.removeChild(f));
        const {
          portals: E,
          clonedElement: T
        } = Ct(e);
        f = T, c(E), f.style.display = "contents", b && clearTimeout(b), b = setTimeout(() => {
          d();
        }, 50), (v = s.current) == null || v.appendChild(f);
      };
      g();
      const h = eo(() => {
        g(), m == null || m.disconnect(), m == null || m.observe(e, {
          childList: !0,
          subtree: !0,
          attributes: o
        });
      }, 50);
      m = new window.MutationObserver(h), m.observe(e, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      f.style.display = "contents", d(), (x = s.current) == null || x.appendChild(f);
    return () => {
      var g, h;
      f.style.display = "", (g = s.current) != null && g.contains(f) && ((h = s.current) == null || h.removeChild(f)), m == null || m.disconnect();
    };
  }, [e, p, r, n, i, o, u]), l.createElement("react-child", {
    ref: s,
    style: {
      display: "contents"
    }
  }, ...a);
});
function Oo(e) {
  return /^(?:async\s+)?(?:function\s*(?:\w*\s*)?\(|\([\w\s,=]*\)\s*=>|\(\{[\w\s,=]*\}\)\s*=>|function\s*\*\s*\w*\s*\()/i.test(e.trim());
}
function $o(e, t = !1) {
  try {
    if (xn(e))
      return e;
    if (t && !Oo(e))
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
function mt(e, t) {
  return Mr(() => $o(e, t), [e, t]);
}
function Ao(e, t) {
  return Object.keys(e).reduce((r, n) => (e[n] !== void 0 && (r[n] = e[n]), r), {});
}
const Fo = ({
  children: e,
  ...t
}) => /* @__PURE__ */ U.jsx(U.Fragment, {
  children: e(t)
});
function ko(e) {
  return l.createElement(Fo, {
    children: e
  });
}
function or(e, t) {
  return e ? t != null && t.forceClone || t != null && t.params ? ko((r) => /* @__PURE__ */ U.jsx(En, {
    forceClone: t == null ? void 0 : t.forceClone,
    params: t == null ? void 0 : t.params,
    children: /* @__PURE__ */ U.jsx(we, {
      slot: e,
      clone: t == null ? void 0 : t.clone,
      ...r
    })
  })) : /* @__PURE__ */ U.jsx(we, {
    slot: e,
    clone: t == null ? void 0 : t.clone
  }) : null;
}
function ir({
  key: e,
  slots: t,
  targets: r
}, n) {
  return t[e] ? (...o) => r ? r.map((i, s) => /* @__PURE__ */ U.jsx(l.Fragment, {
    children: or(i, {
      clone: !0,
      params: o,
      forceClone: !0
    })
  }, s)) : /* @__PURE__ */ U.jsx(U.Fragment, {
    children: or(t[e], {
      clone: !0,
      params: o,
      forceClone: !0
    })
  }) : void 0;
}
const jo = "1.3.0", Do = /* @__PURE__ */ l.createContext({}), No = {
  classNames: {},
  styles: {},
  className: "",
  style: {}
}, zo = (e) => {
  const t = l.useContext(Do);
  return l.useMemo(() => ({
    ...No,
    ...t[e]
  }), [t[e]]);
};
function he() {
  return he = Object.assign ? Object.assign.bind() : function(e) {
    for (var t = 1; t < arguments.length; t++) {
      var r = arguments[t];
      for (var n in r) ({}).hasOwnProperty.call(r, n) && (e[n] = r[n]);
    }
    return e;
  }, he.apply(null, arguments);
}
function Ve() {
  const {
    getPrefixCls: e,
    direction: t,
    csp: r,
    iconPrefixCls: n,
    theme: o
  } = l.useContext(Cn.ConfigContext);
  return {
    theme: o,
    getPrefixCls: e,
    direction: t,
    csp: r,
    iconPrefixCls: n
  };
}
function ve(e) {
  var t = M.useRef();
  t.current = e;
  var r = M.useCallback(function() {
    for (var n, o = arguments.length, i = new Array(o), s = 0; s < o; s++)
      i[s] = arguments[s];
    return (n = t.current) === null || n === void 0 ? void 0 : n.call.apply(n, [t].concat(i));
  }, []);
  return r;
}
function Ho(e) {
  if (Array.isArray(e)) return e;
}
function Bo(e, t) {
  var r = e == null ? null : typeof Symbol < "u" && e[Symbol.iterator] || e["@@iterator"];
  if (r != null) {
    var n, o, i, s, a = [], c = !0, u = !1;
    try {
      if (i = (r = r.call(e)).next, t !== 0) for (; !(c = (n = i.call(r)).done) && (a.push(n.value), a.length !== t); c = !0) ;
    } catch (p) {
      u = !0, o = p;
    } finally {
      try {
        if (!c && r.return != null && (s = r.return(), Object(s) !== s)) return;
      } finally {
        if (u) throw o;
      }
    }
    return a;
  }
}
function sr(e, t) {
  (t == null || t > e.length) && (t = e.length);
  for (var r = 0, n = Array(t); r < t; r++) n[r] = e[r];
  return n;
}
function Vo(e, t) {
  if (e) {
    if (typeof e == "string") return sr(e, t);
    var r = {}.toString.call(e).slice(8, -1);
    return r === "Object" && e.constructor && (r = e.constructor.name), r === "Map" || r === "Set" ? Array.from(e) : r === "Arguments" || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r) ? sr(e, t) : void 0;
  }
}
function Uo() {
  throw new TypeError(`Invalid attempt to destructure non-iterable instance.
In order to be iterable, non-array objects must have a [Symbol.iterator]() method.`);
}
function Ue(e, t) {
  return Ho(e) || Bo(e, t) || Vo(e, t) || Uo();
}
function Ge() {
  return !!(typeof window < "u" && window.document && window.document.createElement);
}
var ar = Ge() ? M.useLayoutEffect : M.useEffect, Xo = function(t, r) {
  var n = M.useRef(!0);
  ar(function() {
    return t(n.current);
  }, r), ar(function() {
    return n.current = !1, function() {
      n.current = !0;
    };
  }, []);
}, lr = function(t, r) {
  Xo(function(n) {
    if (!n)
      return t();
  }, r);
};
function Ee(e) {
  var t = M.useRef(!1), r = M.useState(e), n = Ue(r, 2), o = n[0], i = n[1];
  M.useEffect(function() {
    return t.current = !1, function() {
      t.current = !0;
    };
  }, []);
  function s(a, c) {
    c && t.current || i(a);
  }
  return [o, s];
}
function gt(e) {
  return e !== void 0;
}
function Wo(e, t) {
  var r = t || {}, n = r.defaultValue, o = r.value, i = r.onChange, s = r.postState, a = Ee(function() {
    return gt(o) ? o : gt(n) ? typeof n == "function" ? n() : n : typeof e == "function" ? e() : e;
  }), c = Ue(a, 2), u = c[0], p = c[1], f = o !== void 0 ? o : u, d = s ? s(f) : f, m = ve(i), b = Ee([f]), x = Ue(b, 2), g = x[0], h = x[1];
  lr(function() {
    var T = g[0];
    u !== T && m(u, T);
  }, [g]), lr(function() {
    gt(o) || p(o);
  }, [o]);
  var E = ve(function(T, S) {
    p(T, S), h([f], S);
  });
  return [d, E];
}
function Ce(e) {
  "@babel/helpers - typeof";
  return Ce = typeof Symbol == "function" && typeof Symbol.iterator == "symbol" ? function(t) {
    return typeof t;
  } : function(t) {
    return t && typeof Symbol == "function" && t.constructor === Symbol && t !== Symbol.prototype ? "symbol" : typeof t;
  }, Ce(e);
}
var Dr = {
  exports: {}
}, I = {};
/**
 * @license React
 * react-is.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var At = Symbol.for("react.element"), Ft = Symbol.for("react.portal"), qe = Symbol.for("react.fragment"), Ke = Symbol.for("react.strict_mode"), Ze = Symbol.for("react.profiler"), Qe = Symbol.for("react.provider"), Ye = Symbol.for("react.context"), Go = Symbol.for("react.server_context"), Je = Symbol.for("react.forward_ref"), et = Symbol.for("react.suspense"), tt = Symbol.for("react.suspense_list"), rt = Symbol.for("react.memo"), nt = Symbol.for("react.lazy"), qo = Symbol.for("react.offscreen"), Nr;
Nr = Symbol.for("react.module.reference");
function Y(e) {
  if (typeof e == "object" && e !== null) {
    var t = e.$$typeof;
    switch (t) {
      case At:
        switch (e = e.type, e) {
          case qe:
          case Ze:
          case Ke:
          case et:
          case tt:
            return e;
          default:
            switch (e = e && e.$$typeof, e) {
              case Go:
              case Ye:
              case Je:
              case nt:
              case rt:
              case Qe:
                return e;
              default:
                return t;
            }
        }
      case Ft:
        return t;
    }
  }
}
I.ContextConsumer = Ye;
I.ContextProvider = Qe;
I.Element = At;
I.ForwardRef = Je;
I.Fragment = qe;
I.Lazy = nt;
I.Memo = rt;
I.Portal = Ft;
I.Profiler = Ze;
I.StrictMode = Ke;
I.Suspense = et;
I.SuspenseList = tt;
I.isAsyncMode = function() {
  return !1;
};
I.isConcurrentMode = function() {
  return !1;
};
I.isContextConsumer = function(e) {
  return Y(e) === Ye;
};
I.isContextProvider = function(e) {
  return Y(e) === Qe;
};
I.isElement = function(e) {
  return typeof e == "object" && e !== null && e.$$typeof === At;
};
I.isForwardRef = function(e) {
  return Y(e) === Je;
};
I.isFragment = function(e) {
  return Y(e) === qe;
};
I.isLazy = function(e) {
  return Y(e) === nt;
};
I.isMemo = function(e) {
  return Y(e) === rt;
};
I.isPortal = function(e) {
  return Y(e) === Ft;
};
I.isProfiler = function(e) {
  return Y(e) === Ze;
};
I.isStrictMode = function(e) {
  return Y(e) === Ke;
};
I.isSuspense = function(e) {
  return Y(e) === et;
};
I.isSuspenseList = function(e) {
  return Y(e) === tt;
};
I.isValidElementType = function(e) {
  return typeof e == "string" || typeof e == "function" || e === qe || e === Ze || e === Ke || e === et || e === tt || e === qo || typeof e == "object" && e !== null && (e.$$typeof === nt || e.$$typeof === rt || e.$$typeof === Qe || e.$$typeof === Ye || e.$$typeof === Je || e.$$typeof === Nr || e.getModuleId !== void 0);
};
I.typeOf = Y;
Dr.exports = I;
var ht = Dr.exports, Ko = Symbol.for("react.element"), Zo = Symbol.for("react.transitional.element"), Qo = Symbol.for("react.fragment");
function Yo(e) {
  return (
    // Base object type
    e && Ce(e) === "object" && // React Element type
    (e.$$typeof === Ko || e.$$typeof === Zo) && // React Fragment type
    e.type === Qo
  );
}
var Jo = Number(gn.split(".")[0]), ei = function(t, r) {
  typeof t == "function" ? t(r) : Ce(t) === "object" && t && "current" in t && (t.current = r);
}, ti = function(t) {
  var r, n;
  if (!t)
    return !1;
  if (zr(t) && Jo >= 19)
    return !0;
  var o = ht.isMemo(t) ? t.type.type : t.type;
  return !(typeof o == "function" && !((r = o.prototype) !== null && r !== void 0 && r.render) && o.$$typeof !== ht.ForwardRef || typeof t == "function" && !((n = t.prototype) !== null && n !== void 0 && n.render) && t.$$typeof !== ht.ForwardRef);
};
function zr(e) {
  return /* @__PURE__ */ hn(e) && !Yo(e);
}
var ri = function(t) {
  if (t && zr(t)) {
    var r = t;
    return r.props.propertyIsEnumerable("ref") ? r.props.ref : r.ref;
  }
  return null;
};
const _e = /* @__PURE__ */ l.createContext(null);
function cr(e) {
  const {
    getDropContainer: t,
    className: r,
    prefixCls: n,
    children: o
  } = e, {
    disabled: i
  } = l.useContext(_e), [s, a] = l.useState(), [c, u] = l.useState(null);
  if (l.useEffect(() => {
    const d = t == null ? void 0 : t();
    s !== d && a(d);
  }, [t]), l.useEffect(() => {
    if (s) {
      const d = () => {
        u(!0);
      }, m = (g) => {
        g.preventDefault();
      }, b = (g) => {
        g.relatedTarget || u(!1);
      }, x = (g) => {
        u(!1), g.preventDefault();
      };
      return document.addEventListener("dragenter", d), document.addEventListener("dragover", m), document.addEventListener("dragleave", b), document.addEventListener("drop", x), () => {
        document.removeEventListener("dragenter", d), document.removeEventListener("dragover", m), document.removeEventListener("dragleave", b), document.removeEventListener("drop", x);
      };
    }
  }, [!!s]), !(t && s && !i))
    return null;
  const f = `${n}-drop-area`;
  return /* @__PURE__ */ He(/* @__PURE__ */ l.createElement("div", {
    className: Z(f, r, {
      [`${f}-on-body`]: s.tagName === "BODY"
    }),
    style: {
      display: c ? "block" : "none"
    }
  }, o), s);
}
function K(e) {
  "@babel/helpers - typeof";
  return K = typeof Symbol == "function" && typeof Symbol.iterator == "symbol" ? function(t) {
    return typeof t;
  } : function(t) {
    return t && typeof Symbol == "function" && t.constructor === Symbol && t !== Symbol.prototype ? "symbol" : typeof t;
  }, K(e);
}
function ni(e, t) {
  if (K(e) != "object" || !e) return e;
  var r = e[Symbol.toPrimitive];
  if (r !== void 0) {
    var n = r.call(e, t);
    if (K(n) != "object") return n;
    throw new TypeError("@@toPrimitive must return a primitive value.");
  }
  return (t === "string" ? String : Number)(e);
}
function Hr(e) {
  var t = ni(e, "string");
  return K(t) == "symbol" ? t : t + "";
}
function R(e, t, r) {
  return (t = Hr(t)) in e ? Object.defineProperty(e, t, {
    value: r,
    enumerable: !0,
    configurable: !0,
    writable: !0
  }) : e[t] = r, e;
}
function ur(e, t) {
  var r = Object.keys(e);
  if (Object.getOwnPropertySymbols) {
    var n = Object.getOwnPropertySymbols(e);
    t && (n = n.filter(function(o) {
      return Object.getOwnPropertyDescriptor(e, o).enumerable;
    })), r.push.apply(r, n);
  }
  return r;
}
function C(e) {
  for (var t = 1; t < arguments.length; t++) {
    var r = arguments[t] != null ? arguments[t] : {};
    t % 2 ? ur(Object(r), !0).forEach(function(n) {
      R(e, n, r[n]);
    }) : Object.getOwnPropertyDescriptors ? Object.defineProperties(e, Object.getOwnPropertyDescriptors(r)) : ur(Object(r)).forEach(function(n) {
      Object.defineProperty(e, n, Object.getOwnPropertyDescriptor(r, n));
    });
  }
  return e;
}
function oi(e) {
  if (Array.isArray(e)) return e;
}
function ii(e, t) {
  var r = e == null ? null : typeof Symbol < "u" && e[Symbol.iterator] || e["@@iterator"];
  if (r != null) {
    var n, o, i, s, a = [], c = !0, u = !1;
    try {
      if (i = (r = r.call(e)).next, t === 0) {
        if (Object(r) !== r) return;
        c = !1;
      } else for (; !(c = (n = i.call(r)).done) && (a.push(n.value), a.length !== t); c = !0) ;
    } catch (p) {
      u = !0, o = p;
    } finally {
      try {
        if (!c && r.return != null && (s = r.return(), Object(s) !== s)) return;
      } finally {
        if (u) throw o;
      }
    }
    return a;
  }
}
function fr(e, t) {
  (t == null || t > e.length) && (t = e.length);
  for (var r = 0, n = Array(t); r < t; r++) n[r] = e[r];
  return n;
}
function si(e, t) {
  if (e) {
    if (typeof e == "string") return fr(e, t);
    var r = {}.toString.call(e).slice(8, -1);
    return r === "Object" && e.constructor && (r = e.constructor.name), r === "Map" || r === "Set" ? Array.from(e) : r === "Arguments" || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r) ? fr(e, t) : void 0;
  }
}
function ai() {
  throw new TypeError(`Invalid attempt to destructure non-iterable instance.
In order to be iterable, non-array objects must have a [Symbol.iterator]() method.`);
}
function Q(e, t) {
  return oi(e) || ii(e, t) || si(e, t) || ai();
}
function dr(e) {
  return e instanceof HTMLElement || e instanceof SVGElement;
}
function li(e) {
  return e && Ce(e) === "object" && dr(e.nativeElement) ? e.nativeElement : dr(e) ? e : null;
}
function ci(e) {
  var t = li(e);
  if (t)
    return t;
  if (e instanceof l.Component) {
    var r;
    return (r = Xt.findDOMNode) === null || r === void 0 ? void 0 : r.call(Xt, e);
  }
  return null;
}
function ui(e, t) {
  if (e == null) return {};
  var r = {};
  for (var n in e) if ({}.hasOwnProperty.call(e, n)) {
    if (t.indexOf(n) !== -1) continue;
    r[n] = e[n];
  }
  return r;
}
function pr(e, t) {
  if (e == null) return {};
  var r, n, o = ui(e, t);
  if (Object.getOwnPropertySymbols) {
    var i = Object.getOwnPropertySymbols(e);
    for (n = 0; n < i.length; n++) r = i[n], t.indexOf(r) === -1 && {}.propertyIsEnumerable.call(e, r) && (o[r] = e[r]);
  }
  return o;
}
var fi = /* @__PURE__ */ M.createContext({});
function be(e, t) {
  if (!(e instanceof t)) throw new TypeError("Cannot call a class as a function");
}
function mr(e, t) {
  for (var r = 0; r < t.length; r++) {
    var n = t[r];
    n.enumerable = n.enumerable || !1, n.configurable = !0, "value" in n && (n.writable = !0), Object.defineProperty(e, Hr(n.key), n);
  }
}
function ye(e, t, r) {
  return t && mr(e.prototype, t), r && mr(e, r), Object.defineProperty(e, "prototype", {
    writable: !1
  }), e;
}
function _t(e, t) {
  return _t = Object.setPrototypeOf ? Object.setPrototypeOf.bind() : function(r, n) {
    return r.__proto__ = n, r;
  }, _t(e, t);
}
function ot(e, t) {
  if (typeof t != "function" && t !== null) throw new TypeError("Super expression must either be null or a function");
  e.prototype = Object.create(t && t.prototype, {
    constructor: {
      value: e,
      writable: !0,
      configurable: !0
    }
  }), Object.defineProperty(e, "prototype", {
    writable: !1
  }), t && _t(e, t);
}
function Xe(e) {
  return Xe = Object.setPrototypeOf ? Object.getPrototypeOf.bind() : function(t) {
    return t.__proto__ || Object.getPrototypeOf(t);
  }, Xe(e);
}
function Br() {
  try {
    var e = !Boolean.prototype.valueOf.call(Reflect.construct(Boolean, [], function() {
    }));
  } catch {
  }
  return (Br = function() {
    return !!e;
  })();
}
function ue(e) {
  if (e === void 0) throw new ReferenceError("this hasn't been initialised - super() hasn't been called");
  return e;
}
function di(e, t) {
  if (t && (K(t) == "object" || typeof t == "function")) return t;
  if (t !== void 0) throw new TypeError("Derived constructors may only return object or undefined");
  return ue(e);
}
function it(e) {
  var t = Br();
  return function() {
    var r, n = Xe(e);
    if (t) {
      var o = Xe(this).constructor;
      r = Reflect.construct(n, arguments, o);
    } else r = n.apply(this, arguments);
    return di(this, r);
  };
}
var pi = /* @__PURE__ */ function(e) {
  ot(r, e);
  var t = it(r);
  function r() {
    return be(this, r), t.apply(this, arguments);
  }
  return ye(r, [{
    key: "render",
    value: function() {
      return this.props.children;
    }
  }]), r;
}(M.Component);
function mi(e) {
  var t = M.useReducer(function(a) {
    return a + 1;
  }, 0), r = Ue(t, 2), n = r[1], o = M.useRef(e), i = ve(function() {
    return o.current;
  }), s = ve(function(a) {
    o.current = typeof a == "function" ? a(o.current) : a, n();
  });
  return [i, s];
}
var ie = "none", Oe = "appear", $e = "enter", Ae = "leave", gr = "none", J = "prepare", me = "start", ge = "active", kt = "end", Vr = "prepared";
function hr(e, t) {
  var r = {};
  return r[e.toLowerCase()] = t.toLowerCase(), r["Webkit".concat(e)] = "webkit".concat(t), r["Moz".concat(e)] = "moz".concat(t), r["ms".concat(e)] = "MS".concat(t), r["O".concat(e)] = "o".concat(t.toLowerCase()), r;
}
function gi(e, t) {
  var r = {
    animationend: hr("Animation", "AnimationEnd"),
    transitionend: hr("Transition", "TransitionEnd")
  };
  return e && ("AnimationEvent" in t || delete r.animationend.animation, "TransitionEvent" in t || delete r.transitionend.transition), r;
}
var hi = gi(Ge(), typeof window < "u" ? window : {}), Ur = {};
if (Ge()) {
  var vi = document.createElement("div");
  Ur = vi.style;
}
var Fe = {};
function Xr(e) {
  if (Fe[e])
    return Fe[e];
  var t = hi[e];
  if (t)
    for (var r = Object.keys(t), n = r.length, o = 0; o < n; o += 1) {
      var i = r[o];
      if (Object.prototype.hasOwnProperty.call(t, i) && i in Ur)
        return Fe[e] = t[i], Fe[e];
    }
  return "";
}
var Wr = Xr("animationend"), Gr = Xr("transitionend"), qr = !!(Wr && Gr), vr = Wr || "animationend", br = Gr || "transitionend";
function yr(e, t) {
  if (!e) return null;
  if (K(e) === "object") {
    var r = t.replace(/-\w/g, function(n) {
      return n[1].toUpperCase();
    });
    return e[r];
  }
  return "".concat(e, "-").concat(t);
}
const bi = function(e) {
  var t = se();
  function r(o) {
    o && (o.removeEventListener(br, e), o.removeEventListener(vr, e));
  }
  function n(o) {
    t.current && t.current !== o && r(t.current), o && o !== t.current && (o.addEventListener(br, e), o.addEventListener(vr, e), t.current = o);
  }
  return M.useEffect(function() {
    return function() {
      r(t.current);
    };
  }, []), [n, r];
};
var Kr = Ge() ? vn : xe, Zr = function(t) {
  return +setTimeout(t, 16);
}, Qr = function(t) {
  return clearTimeout(t);
};
typeof window < "u" && "requestAnimationFrame" in window && (Zr = function(t) {
  return window.requestAnimationFrame(t);
}, Qr = function(t) {
  return window.cancelAnimationFrame(t);
});
var Sr = 0, jt = /* @__PURE__ */ new Map();
function Yr(e) {
  jt.delete(e);
}
var Rt = function(t) {
  var r = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : 1;
  Sr += 1;
  var n = Sr;
  function o(i) {
    if (i === 0)
      Yr(n), t();
    else {
      var s = Zr(function() {
        o(i - 1);
      });
      jt.set(n, s);
    }
  }
  return o(r), n;
};
Rt.cancel = function(e) {
  var t = jt.get(e);
  return Yr(e), Qr(t);
};
const yi = function() {
  var e = M.useRef(null);
  function t() {
    Rt.cancel(e.current);
  }
  function r(n) {
    var o = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : 2;
    t();
    var i = Rt(function() {
      o <= 1 ? n({
        isCanceled: function() {
          return i !== e.current;
        }
      }) : r(n, o - 1);
    });
    e.current = i;
  }
  return M.useEffect(function() {
    return function() {
      t();
    };
  }, []), [r, t];
};
var Si = [J, me, ge, kt], xi = [J, Vr], Jr = !1, wi = !0;
function en(e) {
  return e === ge || e === kt;
}
const Ei = function(e, t, r) {
  var n = Ee(gr), o = Q(n, 2), i = o[0], s = o[1], a = yi(), c = Q(a, 2), u = c[0], p = c[1];
  function f() {
    s(J, !0);
  }
  var d = t ? xi : Si;
  return Kr(function() {
    if (i !== gr && i !== kt) {
      var m = d.indexOf(i), b = d[m + 1], x = r(i);
      x === Jr ? s(b, !0) : b && u(function(g) {
        function h() {
          g.isCanceled() || s(b, !0);
        }
        x === !0 ? h() : Promise.resolve(x).then(h);
      });
    }
  }, [e, i]), M.useEffect(function() {
    return function() {
      p();
    };
  }, []), [f, i];
};
function Ci(e, t, r, n) {
  var o = n.motionEnter, i = o === void 0 ? !0 : o, s = n.motionAppear, a = s === void 0 ? !0 : s, c = n.motionLeave, u = c === void 0 ? !0 : c, p = n.motionDeadline, f = n.motionLeaveImmediately, d = n.onAppearPrepare, m = n.onEnterPrepare, b = n.onLeavePrepare, x = n.onAppearStart, g = n.onEnterStart, h = n.onLeaveStart, E = n.onAppearActive, T = n.onEnterActive, S = n.onLeaveActive, w = n.onAppearEnd, v = n.onEnterEnd, _ = n.onLeaveEnd, y = n.onVisibleChanged, L = Ee(), F = Q(L, 2), k = F[0], P = F[1], O = mi(ie), $ = Q(O, 2), A = $[0], j = $[1], z = Ee(null), W = Q(z, 2), fe = W[0], oe = W[1], B = A(), D = se(!1), X = se(null);
  function N() {
    return r();
  }
  var G = se(!1);
  function ae() {
    j(ie), oe(null, !0);
  }
  var re = ve(function(q) {
    var V = A();
    if (V !== ie) {
      var ee = N();
      if (!(q && !q.deadline && q.target !== ee)) {
        var Me = G.current, Ie;
        V === Oe && Me ? Ie = w == null ? void 0 : w(ee, q) : V === $e && Me ? Ie = v == null ? void 0 : v(ee, q) : V === Ae && Me && (Ie = _ == null ? void 0 : _(ee, q)), Me && Ie !== !1 && ae();
      }
    }
  }), st = bi(re), Re = Q(st, 1), Te = Re[0], Le = function(V) {
    switch (V) {
      case Oe:
        return R(R(R({}, J, d), me, x), ge, E);
      case $e:
        return R(R(R({}, J, m), me, g), ge, T);
      case Ae:
        return R(R(R({}, J, b), me, h), ge, S);
      default:
        return {};
    }
  }, le = M.useMemo(function() {
    return Le(B);
  }, [B]), Pe = Ei(B, !e, function(q) {
    if (q === J) {
      var V = le[J];
      return V ? V(N()) : Jr;
    }
    if (ce in le) {
      var ee;
      oe(((ee = le[ce]) === null || ee === void 0 ? void 0 : ee.call(le, N(), null)) || null);
    }
    return ce === ge && B !== ie && (Te(N()), p > 0 && (clearTimeout(X.current), X.current = setTimeout(function() {
      re({
        deadline: !0
      });
    }, p))), ce === Vr && ae(), wi;
  }), Nt = Q(Pe, 2), fn = Nt[0], ce = Nt[1], dn = en(ce);
  G.current = dn;
  var zt = se(null);
  Kr(function() {
    if (!(D.current && zt.current === t)) {
      P(t);
      var q = D.current;
      D.current = !0;
      var V;
      !q && t && a && (V = Oe), q && t && i && (V = $e), (q && !t && u || !q && f && !t && u) && (V = Ae);
      var ee = Le(V);
      V && (e || ee[J]) ? (j(V), fn()) : j(ie), zt.current = t;
    }
  }, [t]), xe(function() {
    // Cancel appear
    (B === Oe && !a || // Cancel enter
    B === $e && !i || // Cancel leave
    B === Ae && !u) && j(ie);
  }, [a, i, u]), xe(function() {
    return function() {
      D.current = !1, clearTimeout(X.current);
    };
  }, []);
  var at = M.useRef(!1);
  xe(function() {
    k && (at.current = !0), k !== void 0 && B === ie && ((at.current || k) && (y == null || y(k)), at.current = !0);
  }, [k, B]);
  var lt = fe;
  return le[J] && ce === me && (lt = C({
    transition: "none"
  }, lt)), [B, ce, lt, k ?? t];
}
function _i(e) {
  var t = e;
  K(e) === "object" && (t = e.transitionSupport);
  function r(o, i) {
    return !!(o.motionName && t && i !== !1);
  }
  var n = /* @__PURE__ */ M.forwardRef(function(o, i) {
    var s = o.visible, a = s === void 0 ? !0 : s, c = o.removeOnLeave, u = c === void 0 ? !0 : c, p = o.forceRender, f = o.children, d = o.motionName, m = o.leavedClassName, b = o.eventProps, x = M.useContext(fi), g = x.motion, h = r(o, g), E = se(), T = se();
    function S() {
      try {
        return E.current instanceof HTMLElement ? E.current : ci(T.current);
      } catch {
        return null;
      }
    }
    var w = Ci(h, a, S, o), v = Q(w, 4), _ = v[0], y = v[1], L = v[2], F = v[3], k = M.useRef(F);
    F && (k.current = !0);
    var P = M.useCallback(function(W) {
      E.current = W, ei(i, W);
    }, [i]), O, $ = C(C({}, b), {}, {
      visible: a
    });
    if (!f)
      O = null;
    else if (_ === ie)
      F ? O = f(C({}, $), P) : !u && k.current && m ? O = f(C(C({}, $), {}, {
        className: m
      }), P) : p || !u && !m ? O = f(C(C({}, $), {}, {
        style: {
          display: "none"
        }
      }), P) : O = null;
    else {
      var A;
      y === J ? A = "prepare" : en(y) ? A = "active" : y === me && (A = "start");
      var j = yr(d, "".concat(_, "-").concat(A));
      O = f(C(C({}, $), {}, {
        className: Z(yr(d, _), R(R({}, j, j && A), d, typeof d == "string")),
        style: L
      }), P);
    }
    if (/* @__PURE__ */ M.isValidElement(O) && ti(O)) {
      var z = ri(O);
      z || (O = /* @__PURE__ */ M.cloneElement(O, {
        ref: P
      }));
    }
    return /* @__PURE__ */ M.createElement(pi, {
      ref: T
    }, O);
  });
  return n.displayName = "CSSMotion", n;
}
const Ri = _i(qr);
var Tt = "add", Lt = "keep", Pt = "remove", vt = "removed";
function Ti(e) {
  var t;
  return e && K(e) === "object" && "key" in e ? t = e : t = {
    key: e
  }, C(C({}, t), {}, {
    key: String(t.key)
  });
}
function Mt() {
  var e = arguments.length > 0 && arguments[0] !== void 0 ? arguments[0] : [];
  return e.map(Ti);
}
function Li() {
  var e = arguments.length > 0 && arguments[0] !== void 0 ? arguments[0] : [], t = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : [], r = [], n = 0, o = t.length, i = Mt(e), s = Mt(t);
  i.forEach(function(u) {
    for (var p = !1, f = n; f < o; f += 1) {
      var d = s[f];
      if (d.key === u.key) {
        n < f && (r = r.concat(s.slice(n, f).map(function(m) {
          return C(C({}, m), {}, {
            status: Tt
          });
        })), n = f), r.push(C(C({}, d), {}, {
          status: Lt
        })), n += 1, p = !0;
        break;
      }
    }
    p || r.push(C(C({}, u), {}, {
      status: Pt
    }));
  }), n < o && (r = r.concat(s.slice(n).map(function(u) {
    return C(C({}, u), {}, {
      status: Tt
    });
  })));
  var a = {};
  r.forEach(function(u) {
    var p = u.key;
    a[p] = (a[p] || 0) + 1;
  });
  var c = Object.keys(a).filter(function(u) {
    return a[u] > 1;
  });
  return c.forEach(function(u) {
    r = r.filter(function(p) {
      var f = p.key, d = p.status;
      return f !== u || d !== Pt;
    }), r.forEach(function(p) {
      p.key === u && (p.status = Lt);
    });
  }), r;
}
var Pi = ["component", "children", "onVisibleChanged", "onAllRemoved"], Mi = ["status"], Ii = ["eventProps", "visible", "children", "motionName", "motionAppear", "motionEnter", "motionLeave", "motionLeaveImmediately", "motionDeadline", "removeOnLeave", "leavedClassName", "onAppearPrepare", "onAppearStart", "onAppearActive", "onAppearEnd", "onEnterStart", "onEnterActive", "onEnterEnd", "onLeaveStart", "onLeaveActive", "onLeaveEnd"];
function Oi(e) {
  var t = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : Ri, r = /* @__PURE__ */ function(n) {
    ot(i, n);
    var o = it(i);
    function i() {
      var s;
      be(this, i);
      for (var a = arguments.length, c = new Array(a), u = 0; u < a; u++)
        c[u] = arguments[u];
      return s = o.call.apply(o, [this].concat(c)), R(ue(s), "state", {
        keyEntities: []
      }), R(ue(s), "removeKey", function(p) {
        s.setState(function(f) {
          var d = f.keyEntities.map(function(m) {
            return m.key !== p ? m : C(C({}, m), {}, {
              status: vt
            });
          });
          return {
            keyEntities: d
          };
        }, function() {
          var f = s.state.keyEntities, d = f.filter(function(m) {
            var b = m.status;
            return b !== vt;
          }).length;
          d === 0 && s.props.onAllRemoved && s.props.onAllRemoved();
        });
      }), s;
    }
    return ye(i, [{
      key: "render",
      value: function() {
        var a = this, c = this.state.keyEntities, u = this.props, p = u.component, f = u.children, d = u.onVisibleChanged;
        u.onAllRemoved;
        var m = pr(u, Pi), b = p || M.Fragment, x = {};
        return Ii.forEach(function(g) {
          x[g] = m[g], delete m[g];
        }), delete m.keys, /* @__PURE__ */ M.createElement(b, m, c.map(function(g, h) {
          var E = g.status, T = pr(g, Mi), S = E === Tt || E === Lt;
          return /* @__PURE__ */ M.createElement(t, he({}, x, {
            key: T.key,
            visible: S,
            eventProps: T,
            onVisibleChanged: function(v) {
              d == null || d(v, {
                key: T.key
              }), v || a.removeKey(T.key);
            }
          }), function(w, v) {
            return f(C(C({}, w), {}, {
              index: h
            }), v);
          });
        }));
      }
    }], [{
      key: "getDerivedStateFromProps",
      value: function(a, c) {
        var u = a.keys, p = c.keyEntities, f = Mt(u), d = Li(p, f);
        return {
          keyEntities: d.filter(function(m) {
            var b = p.find(function(x) {
              var g = x.key;
              return m.key === g;
            });
            return !(b && b.status === vt && m.status === Pt);
          })
        };
      }
    }]), i;
  }(M.Component);
  return R(r, "defaultProps", {
    component: "div"
  }), r;
}
const $i = Oi(qr);
function Ai(e, t) {
  const {
    children: r,
    upload: n,
    rootClassName: o
  } = e, i = l.useRef(null);
  return l.useImperativeHandle(t, () => i.current), /* @__PURE__ */ l.createElement(Ir, he({}, n, {
    showUploadList: !1,
    rootClassName: o,
    ref: i
  }), r);
}
const tn = /* @__PURE__ */ l.forwardRef(Ai);
var rn = /* @__PURE__ */ ye(function e() {
  be(this, e);
}), nn = "CALC_UNIT", Fi = new RegExp(nn, "g");
function bt(e) {
  return typeof e == "number" ? "".concat(e).concat(nn) : e;
}
var ki = /* @__PURE__ */ function(e) {
  ot(r, e);
  var t = it(r);
  function r(n, o) {
    var i;
    be(this, r), i = t.call(this), R(ue(i), "result", ""), R(ue(i), "unitlessCssVar", void 0), R(ue(i), "lowPriority", void 0);
    var s = K(n);
    return i.unitlessCssVar = o, n instanceof r ? i.result = "(".concat(n.result, ")") : s === "number" ? i.result = bt(n) : s === "string" && (i.result = n), i;
  }
  return ye(r, [{
    key: "add",
    value: function(o) {
      return o instanceof r ? this.result = "".concat(this.result, " + ").concat(o.getResult()) : (typeof o == "number" || typeof o == "string") && (this.result = "".concat(this.result, " + ").concat(bt(o))), this.lowPriority = !0, this;
    }
  }, {
    key: "sub",
    value: function(o) {
      return o instanceof r ? this.result = "".concat(this.result, " - ").concat(o.getResult()) : (typeof o == "number" || typeof o == "string") && (this.result = "".concat(this.result, " - ").concat(bt(o))), this.lowPriority = !0, this;
    }
  }, {
    key: "mul",
    value: function(o) {
      return this.lowPriority && (this.result = "(".concat(this.result, ")")), o instanceof r ? this.result = "".concat(this.result, " * ").concat(o.getResult(!0)) : (typeof o == "number" || typeof o == "string") && (this.result = "".concat(this.result, " * ").concat(o)), this.lowPriority = !1, this;
    }
  }, {
    key: "div",
    value: function(o) {
      return this.lowPriority && (this.result = "(".concat(this.result, ")")), o instanceof r ? this.result = "".concat(this.result, " / ").concat(o.getResult(!0)) : (typeof o == "number" || typeof o == "string") && (this.result = "".concat(this.result, " / ").concat(o)), this.lowPriority = !1, this;
    }
  }, {
    key: "getResult",
    value: function(o) {
      return this.lowPriority || o ? "(".concat(this.result, ")") : this.result;
    }
  }, {
    key: "equal",
    value: function(o) {
      var i = this, s = o || {}, a = s.unit, c = !0;
      return typeof a == "boolean" ? c = a : Array.from(this.unitlessCssVar).some(function(u) {
        return i.result.includes(u);
      }) && (c = !1), this.result = this.result.replace(Fi, c ? "px" : ""), typeof this.lowPriority < "u" ? "calc(".concat(this.result, ")") : this.result;
    }
  }]), r;
}(rn), ji = /* @__PURE__ */ function(e) {
  ot(r, e);
  var t = it(r);
  function r(n) {
    var o;
    return be(this, r), o = t.call(this), R(ue(o), "result", 0), n instanceof r ? o.result = n.result : typeof n == "number" && (o.result = n), o;
  }
  return ye(r, [{
    key: "add",
    value: function(o) {
      return o instanceof r ? this.result += o.result : typeof o == "number" && (this.result += o), this;
    }
  }, {
    key: "sub",
    value: function(o) {
      return o instanceof r ? this.result -= o.result : typeof o == "number" && (this.result -= o), this;
    }
  }, {
    key: "mul",
    value: function(o) {
      return o instanceof r ? this.result *= o.result : typeof o == "number" && (this.result *= o), this;
    }
  }, {
    key: "div",
    value: function(o) {
      return o instanceof r ? this.result /= o.result : typeof o == "number" && (this.result /= o), this;
    }
  }, {
    key: "equal",
    value: function() {
      return this.result;
    }
  }]), r;
}(rn), Di = function(t, r) {
  var n = t === "css" ? ki : ji;
  return function(o) {
    return new n(o, r);
  };
}, xr = function(t, r) {
  return "".concat([r, t.replace(/([A-Z]+)([A-Z][a-z]+)/g, "$1-$2").replace(/([a-z])([A-Z])/g, "$1-$2")].filter(Boolean).join("-"));
};
function wr(e, t, r, n) {
  var o = C({}, t[e]);
  if (n != null && n.deprecatedTokens) {
    var i = n.deprecatedTokens;
    i.forEach(function(a) {
      var c = Q(a, 2), u = c[0], p = c[1];
      if (o != null && o[u] || o != null && o[p]) {
        var f;
        (f = o[p]) !== null && f !== void 0 || (o[p] = o == null ? void 0 : o[u]);
      }
    });
  }
  var s = C(C({}, r), o);
  return Object.keys(s).forEach(function(a) {
    s[a] === t[a] && delete s[a];
  }), s;
}
var on = typeof CSSINJS_STATISTIC < "u", It = !0;
function Dt() {
  for (var e = arguments.length, t = new Array(e), r = 0; r < e; r++)
    t[r] = arguments[r];
  if (!on)
    return Object.assign.apply(Object, [{}].concat(t));
  It = !1;
  var n = {};
  return t.forEach(function(o) {
    if (K(o) === "object") {
      var i = Object.keys(o);
      i.forEach(function(s) {
        Object.defineProperty(n, s, {
          configurable: !0,
          enumerable: !0,
          get: function() {
            return o[s];
          }
        });
      });
    }
  }), It = !0, n;
}
var Er = {};
function Ni() {
}
var zi = function(t) {
  var r, n = t, o = Ni;
  return on && typeof Proxy < "u" && (r = /* @__PURE__ */ new Set(), n = new Proxy(t, {
    get: function(s, a) {
      if (It) {
        var c;
        (c = r) === null || c === void 0 || c.add(a);
      }
      return s[a];
    }
  }), o = function(s, a) {
    var c;
    Er[s] = {
      global: Array.from(r),
      component: C(C({}, (c = Er[s]) === null || c === void 0 ? void 0 : c.component), a)
    };
  }), {
    token: n,
    keys: r,
    flush: o
  };
};
function Cr(e, t, r) {
  if (typeof r == "function") {
    var n;
    return r(Dt(t, (n = t[e]) !== null && n !== void 0 ? n : {}));
  }
  return r ?? {};
}
function Hi(e) {
  return e === "js" ? {
    max: Math.max,
    min: Math.min
  } : {
    max: function() {
      for (var r = arguments.length, n = new Array(r), o = 0; o < r; o++)
        n[o] = arguments[o];
      return "max(".concat(n.map(function(i) {
        return Wt(i);
      }).join(","), ")");
    },
    min: function() {
      for (var r = arguments.length, n = new Array(r), o = 0; o < r; o++)
        n[o] = arguments[o];
      return "min(".concat(n.map(function(i) {
        return Wt(i);
      }).join(","), ")");
    }
  };
}
var Bi = 1e3 * 60 * 10, Vi = /* @__PURE__ */ function() {
  function e() {
    be(this, e), R(this, "map", /* @__PURE__ */ new Map()), R(this, "objectIDMap", /* @__PURE__ */ new WeakMap()), R(this, "nextID", 0), R(this, "lastAccessBeat", /* @__PURE__ */ new Map()), R(this, "accessBeat", 0);
  }
  return ye(e, [{
    key: "set",
    value: function(r, n) {
      this.clear();
      var o = this.getCompositeKey(r);
      this.map.set(o, n), this.lastAccessBeat.set(o, Date.now());
    }
  }, {
    key: "get",
    value: function(r) {
      var n = this.getCompositeKey(r), o = this.map.get(n);
      return this.lastAccessBeat.set(n, Date.now()), this.accessBeat += 1, o;
    }
  }, {
    key: "getCompositeKey",
    value: function(r) {
      var n = this, o = r.map(function(i) {
        return i && K(i) === "object" ? "obj_".concat(n.getObjectID(i)) : "".concat(K(i), "_").concat(i);
      });
      return o.join("|");
    }
  }, {
    key: "getObjectID",
    value: function(r) {
      if (this.objectIDMap.has(r))
        return this.objectIDMap.get(r);
      var n = this.nextID;
      return this.objectIDMap.set(r, n), this.nextID += 1, n;
    }
  }, {
    key: "clear",
    value: function() {
      var r = this;
      if (this.accessBeat > 1e4) {
        var n = Date.now();
        this.lastAccessBeat.forEach(function(o, i) {
          n - o > Bi && (r.map.delete(i), r.lastAccessBeat.delete(i));
        }), this.accessBeat = 0;
      }
    }
  }]), e;
}(), _r = new Vi();
function Ui(e, t) {
  return l.useMemo(function() {
    var r = _r.get(t);
    if (r)
      return r;
    var n = e();
    return _r.set(t, n), n;
  }, t);
}
var Xi = function() {
  return {};
};
function Wi(e) {
  var t = e.useCSP, r = t === void 0 ? Xi : t, n = e.useToken, o = e.usePrefix, i = e.getResetStyles, s = e.getCommonStyle, a = e.getCompUnitless;
  function c(d, m, b, x) {
    var g = Array.isArray(d) ? d[0] : d;
    function h(y) {
      return "".concat(String(g)).concat(y.slice(0, 1).toUpperCase()).concat(y.slice(1));
    }
    var E = (x == null ? void 0 : x.unitless) || {}, T = typeof a == "function" ? a(d) : {}, S = C(C({}, T), {}, R({}, h("zIndexPopup"), !0));
    Object.keys(E).forEach(function(y) {
      S[h(y)] = E[y];
    });
    var w = C(C({}, x), {}, {
      unitless: S,
      prefixToken: h
    }), v = p(d, m, b, w), _ = u(g, b, w);
    return function(y) {
      var L = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : y, F = v(y, L), k = Q(F, 2), P = k[1], O = _(L), $ = Q(O, 2), A = $[0], j = $[1];
      return [A, P, j];
    };
  }
  function u(d, m, b) {
    var x = b.unitless, g = b.injectStyle, h = g === void 0 ? !0 : g, E = b.prefixToken, T = b.ignore, S = function(_) {
      var y = _.rootCls, L = _.cssVar, F = L === void 0 ? {} : L, k = n(), P = k.realToken;
      return zn({
        path: [d],
        prefix: F.prefix,
        key: F.key,
        unitless: x,
        ignore: T,
        token: P,
        scope: y
      }, function() {
        var O = Cr(d, P, m), $ = wr(d, P, O, {
          deprecatedTokens: b == null ? void 0 : b.deprecatedTokens
        });
        return Object.keys(O).forEach(function(A) {
          $[E(A)] = $[A], delete $[A];
        }), $;
      }), null;
    }, w = function(_) {
      var y = n(), L = y.cssVar;
      return [function(F) {
        return h && L ? /* @__PURE__ */ l.createElement(l.Fragment, null, /* @__PURE__ */ l.createElement(S, {
          rootCls: _,
          cssVar: L,
          component: d
        }), F) : F;
      }, L == null ? void 0 : L.key];
    };
    return w;
  }
  function p(d, m, b) {
    var x = arguments.length > 3 && arguments[3] !== void 0 ? arguments[3] : {}, g = Array.isArray(d) ? d : [d, d], h = Q(g, 1), E = h[0], T = g.join("-"), S = e.layer || {
      name: "antd"
    };
    return function(w) {
      var v = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : w, _ = n(), y = _.theme, L = _.realToken, F = _.hashId, k = _.token, P = _.cssVar, O = o(), $ = O.rootPrefixCls, A = O.iconPrefixCls, j = r(), z = P ? "css" : "js", W = Ui(function() {
        var N = /* @__PURE__ */ new Set();
        return P && Object.keys(x.unitless || {}).forEach(function(G) {
          N.add(ft(G, P.prefix)), N.add(ft(G, xr(E, P.prefix)));
        }), Di(z, N);
      }, [z, E, P == null ? void 0 : P.prefix]), fe = Hi(z), oe = fe.max, B = fe.min, D = {
        theme: y,
        token: k,
        hashId: F,
        nonce: function() {
          return j.nonce;
        },
        clientOnly: x.clientOnly,
        layer: S,
        // antd is always at top of styles
        order: x.order || -999
      };
      typeof i == "function" && Gt(C(C({}, D), {}, {
        clientOnly: !1,
        path: ["Shared", $]
      }), function() {
        return i(k, {
          prefix: {
            rootPrefixCls: $,
            iconPrefixCls: A
          },
          csp: j
        });
      });
      var X = Gt(C(C({}, D), {}, {
        path: [T, w, A]
      }), function() {
        if (x.injectStyle === !1)
          return [];
        var N = zi(k), G = N.token, ae = N.flush, re = Cr(E, L, b), st = ".".concat(w), Re = wr(E, L, re, {
          deprecatedTokens: x.deprecatedTokens
        });
        P && re && K(re) === "object" && Object.keys(re).forEach(function(Pe) {
          re[Pe] = "var(".concat(ft(Pe, xr(E, P.prefix)), ")");
        });
        var Te = Dt(G, {
          componentCls: st,
          prefixCls: w,
          iconCls: ".".concat(A),
          antCls: ".".concat($),
          calc: W,
          // @ts-ignore
          max: oe,
          // @ts-ignore
          min: B
        }, P ? re : Re), Le = m(Te, {
          hashId: F,
          prefixCls: w,
          rootPrefixCls: $,
          iconPrefixCls: A
        });
        ae(E, Re);
        var le = typeof s == "function" ? s(Te, w, v, x.resetFont) : null;
        return [x.resetStyle === !1 ? null : le, Le];
      });
      return [X, F];
    };
  }
  function f(d, m, b) {
    var x = arguments.length > 3 && arguments[3] !== void 0 ? arguments[3] : {}, g = p(d, m, b, C({
      resetStyle: !1,
      // Sub Style should default after root one
      order: -998
    }, x)), h = function(T) {
      var S = T.prefixCls, w = T.rootCls, v = w === void 0 ? S : w;
      return g(S, v), null;
    };
    return h;
  }
  return {
    genStyleHooks: c,
    genSubStyleComponent: f,
    genComponentStyleHook: p
  };
}
const H = Math.round;
function yt(e, t) {
  const r = e.replace(/^[^(]*\((.*)/, "$1").replace(/\).*/, "").match(/\d*\.?\d+%?/g) || [], n = r.map((o) => parseFloat(o));
  for (let o = 0; o < 3; o += 1)
    n[o] = t(n[o] || 0, r[o] || "", o);
  return r[3] ? n[3] = r[3].includes("%") ? n[3] / 100 : n[3] : n[3] = 1, n;
}
const Rr = (e, t, r) => r === 0 ? e : e / 100;
function Se(e, t) {
  const r = t || 255;
  return e > r ? r : e < 0 ? 0 : e;
}
class te {
  constructor(t) {
    R(this, "isValid", !0), R(this, "r", 0), R(this, "g", 0), R(this, "b", 0), R(this, "a", 1), R(this, "_h", void 0), R(this, "_s", void 0), R(this, "_l", void 0), R(this, "_v", void 0), R(this, "_max", void 0), R(this, "_min", void 0), R(this, "_brightness", void 0);
    function r(n) {
      return n[0] in t && n[1] in t && n[2] in t;
    }
    if (t) if (typeof t == "string") {
      let o = function(i) {
        return n.startsWith(i);
      };
      const n = t.trim();
      /^#?[A-F\d]{3,8}$/i.test(n) ? this.fromHexString(n) : o("rgb") ? this.fromRgbString(n) : o("hsl") ? this.fromHslString(n) : (o("hsv") || o("hsb")) && this.fromHsvString(n);
    } else if (t instanceof te)
      this.r = t.r, this.g = t.g, this.b = t.b, this.a = t.a, this._h = t._h, this._s = t._s, this._l = t._l, this._v = t._v;
    else if (r("rgb"))
      this.r = Se(t.r), this.g = Se(t.g), this.b = Se(t.b), this.a = typeof t.a == "number" ? Se(t.a, 1) : 1;
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
    const r = t(this.r), n = t(this.g), o = t(this.b);
    return 0.2126 * r + 0.7152 * n + 0.0722 * o;
  }
  getHue() {
    if (typeof this._h > "u") {
      const t = this.getMax() - this.getMin();
      t === 0 ? this._h = 0 : this._h = H(60 * (this.r === this.getMax() ? (this.g - this.b) / t + (this.g < this.b ? 6 : 0) : this.g === this.getMax() ? (this.b - this.r) / t + 2 : (this.r - this.g) / t + 4));
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
    const r = this.getHue(), n = this.getSaturation();
    let o = this.getLightness() - t / 100;
    return o < 0 && (o = 0), this._c({
      h: r,
      s: n,
      l: o,
      a: this.a
    });
  }
  lighten(t = 10) {
    const r = this.getHue(), n = this.getSaturation();
    let o = this.getLightness() + t / 100;
    return o > 1 && (o = 1), this._c({
      h: r,
      s: n,
      l: o,
      a: this.a
    });
  }
  /**
   * Mix the current color a given amount with another color, from 0 to 100.
   * 0 means no mixing (return current color).
   */
  mix(t, r = 50) {
    const n = this._c(t), o = r / 100, i = (a) => (n[a] - this[a]) * o + this[a], s = {
      r: H(i("r")),
      g: H(i("g")),
      b: H(i("b")),
      a: H(i("a") * 100) / 100
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
    const r = this._c(t), n = this.a + r.a * (1 - this.a), o = (i) => H((this[i] * this.a + r[i] * r.a * (1 - this.a)) / n);
    return this._c({
      r: o("r"),
      g: o("g"),
      b: o("b"),
      a: n
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
    const n = (this.g || 0).toString(16);
    t += n.length === 2 ? n : "0" + n;
    const o = (this.b || 0).toString(16);
    if (t += o.length === 2 ? o : "0" + o, typeof this.a == "number" && this.a >= 0 && this.a < 1) {
      const i = H(this.a * 255).toString(16);
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
    const t = this.getHue(), r = H(this.getSaturation() * 100), n = H(this.getLightness() * 100);
    return this.a !== 1 ? `hsla(${t},${r}%,${n}%,${this.a})` : `hsl(${t},${r}%,${n}%)`;
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
  _sc(t, r, n) {
    const o = this.clone();
    return o[t] = Se(r, n), o;
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
    function n(o, i) {
      return parseInt(r[o] + r[i || o], 16);
    }
    r.length < 6 ? (this.r = n(0), this.g = n(1), this.b = n(2), this.a = r[3] ? n(3) / 255 : 1) : (this.r = n(0, 1), this.g = n(2, 3), this.b = n(4, 5), this.a = r[6] ? n(6, 7) / 255 : 1);
  }
  fromHsl({
    h: t,
    s: r,
    l: n,
    a: o
  }) {
    if (this._h = t % 360, this._s = r, this._l = n, this.a = typeof o == "number" ? o : 1, r <= 0) {
      const d = H(n * 255);
      this.r = d, this.g = d, this.b = d;
    }
    let i = 0, s = 0, a = 0;
    const c = t / 60, u = (1 - Math.abs(2 * n - 1)) * r, p = u * (1 - Math.abs(c % 2 - 1));
    c >= 0 && c < 1 ? (i = u, s = p) : c >= 1 && c < 2 ? (i = p, s = u) : c >= 2 && c < 3 ? (s = u, a = p) : c >= 3 && c < 4 ? (s = p, a = u) : c >= 4 && c < 5 ? (i = p, a = u) : c >= 5 && c < 6 && (i = u, a = p);
    const f = n - u / 2;
    this.r = H((i + f) * 255), this.g = H((s + f) * 255), this.b = H((a + f) * 255);
  }
  fromHsv({
    h: t,
    s: r,
    v: n,
    a: o
  }) {
    this._h = t % 360, this._s = r, this._v = n, this.a = typeof o == "number" ? o : 1;
    const i = H(n * 255);
    if (this.r = i, this.g = i, this.b = i, r <= 0)
      return;
    const s = t / 60, a = Math.floor(s), c = s - a, u = H(n * (1 - r) * 255), p = H(n * (1 - r * c) * 255), f = H(n * (1 - r * (1 - c)) * 255);
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
    const r = yt(t, Rr);
    this.fromHsv({
      h: r[0],
      s: r[1],
      v: r[2],
      a: r[3]
    });
  }
  fromHslString(t) {
    const r = yt(t, Rr);
    this.fromHsl({
      h: r[0],
      s: r[1],
      l: r[2],
      a: r[3]
    });
  }
  fromRgbString(t) {
    const r = yt(t, (n, o) => (
      // Convert percentage to number. e.g. 50% -> 128
      o.includes("%") ? H(n / 100 * 255) : n
    ));
    this.r = r[0], this.g = r[1], this.b = r[2], this.a = r[3];
  }
}
const Gi = {
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
}, qi = Object.assign(Object.assign({}, Gi), {
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
function St(e) {
  return e >= 0 && e <= 255;
}
function ke(e, t) {
  const {
    r,
    g: n,
    b: o,
    a: i
  } = new te(e).toRgb();
  if (i < 1)
    return e;
  const {
    r: s,
    g: a,
    b: c
  } = new te(t).toRgb();
  for (let u = 0.01; u <= 1; u += 0.01) {
    const p = Math.round((r - s * (1 - u)) / u), f = Math.round((n - a * (1 - u)) / u), d = Math.round((o - c * (1 - u)) / u);
    if (St(p) && St(f) && St(d))
      return new te({
        r: p,
        g: f,
        b: d,
        a: Math.round(u * 100) / 100
      }).toRgbString();
  }
  return new te({
    r,
    g: n,
    b: o,
    a: 1
  }).toRgbString();
}
var Ki = function(e, t) {
  var r = {};
  for (var n in e) Object.prototype.hasOwnProperty.call(e, n) && t.indexOf(n) < 0 && (r[n] = e[n]);
  if (e != null && typeof Object.getOwnPropertySymbols == "function") for (var o = 0, n = Object.getOwnPropertySymbols(e); o < n.length; o++)
    t.indexOf(n[o]) < 0 && Object.prototype.propertyIsEnumerable.call(e, n[o]) && (r[n[o]] = e[n[o]]);
  return r;
};
function Zi(e) {
  const {
    override: t
  } = e, r = Ki(e, ["override"]), n = Object.assign({}, t);
  Object.keys(qi).forEach((d) => {
    delete n[d];
  });
  const o = Object.assign(Object.assign({}, r), n), i = 480, s = 576, a = 768, c = 992, u = 1200, p = 1600;
  if (o.motion === !1) {
    const d = "0s";
    o.motionDurationFast = d, o.motionDurationMid = d, o.motionDurationSlow = d;
  }
  return Object.assign(Object.assign(Object.assign({}, o), {
    // ============== Background ============== //
    colorFillContent: o.colorFillSecondary,
    colorFillContentHover: o.colorFill,
    colorFillAlter: o.colorFillQuaternary,
    colorBgContainerDisabled: o.colorFillTertiary,
    // ============== Split ============== //
    colorBorderBg: o.colorBgContainer,
    colorSplit: ke(o.colorBorderSecondary, o.colorBgContainer),
    // ============== Text ============== //
    colorTextPlaceholder: o.colorTextQuaternary,
    colorTextDisabled: o.colorTextQuaternary,
    colorTextHeading: o.colorText,
    colorTextLabel: o.colorTextSecondary,
    colorTextDescription: o.colorTextTertiary,
    colorTextLightSolid: o.colorWhite,
    colorHighlight: o.colorError,
    colorBgTextHover: o.colorFillSecondary,
    colorBgTextActive: o.colorFill,
    colorIcon: o.colorTextTertiary,
    colorIconHover: o.colorText,
    colorErrorOutline: ke(o.colorErrorBg, o.colorBgContainer),
    colorWarningOutline: ke(o.colorWarningBg, o.colorBgContainer),
    // Font
    fontSizeIcon: o.fontSizeSM,
    // Line
    lineWidthFocus: o.lineWidth * 3,
    // Control
    lineWidth: o.lineWidth,
    controlOutlineWidth: o.lineWidth * 2,
    // Checkbox size and expand icon size
    controlInteractiveSize: o.controlHeight / 2,
    controlItemBgHover: o.colorFillTertiary,
    controlItemBgActive: o.colorPrimaryBg,
    controlItemBgActiveHover: o.colorPrimaryBgHover,
    controlItemBgActiveDisabled: o.colorFill,
    controlTmpOutline: o.colorFillQuaternary,
    controlOutline: ke(o.colorPrimaryBg, o.colorBgContainer),
    lineType: o.lineType,
    borderRadius: o.borderRadius,
    borderRadiusXS: o.borderRadiusXS,
    borderRadiusSM: o.borderRadiusSM,
    borderRadiusLG: o.borderRadiusLG,
    fontWeightStrong: 600,
    opacityLoading: 0.65,
    linkDecoration: "none",
    linkHoverDecoration: "none",
    linkFocusDecoration: "none",
    controlPaddingHorizontal: 12,
    controlPaddingHorizontalSM: 8,
    paddingXXS: o.sizeXXS,
    paddingXS: o.sizeXS,
    paddingSM: o.sizeSM,
    padding: o.size,
    paddingMD: o.sizeMD,
    paddingLG: o.sizeLG,
    paddingXL: o.sizeXL,
    paddingContentHorizontalLG: o.sizeLG,
    paddingContentVerticalLG: o.sizeMS,
    paddingContentHorizontal: o.sizeMS,
    paddingContentVertical: o.sizeSM,
    paddingContentHorizontalSM: o.size,
    paddingContentVerticalSM: o.sizeXS,
    marginXXS: o.sizeXXS,
    marginXS: o.sizeXS,
    marginSM: o.sizeSM,
    margin: o.size,
    marginMD: o.sizeMD,
    marginLG: o.sizeLG,
    marginXL: o.sizeXL,
    marginXXL: o.sizeXXL,
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
    screenLGMax: u - 1,
    screenXL: u,
    screenXLMin: u,
    screenXLMax: p - 1,
    screenXXL: p,
    screenXXLMin: p,
    boxShadowPopoverArrow: "2px 2px 5px rgba(0, 0, 0, 0.05)",
    boxShadowCard: `
      0 1px 2px -2px ${new te("rgba(0, 0, 0, 0.16)").toRgbString()},
      0 3px 6px 0 ${new te("rgba(0, 0, 0, 0.12)").toRgbString()},
      0 5px 12px 4px ${new te("rgba(0, 0, 0, 0.09)").toRgbString()}
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
  }), n);
}
const Qi = {
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
}, Yi = {
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
}, Ji = Hn(Be.defaultAlgorithm), es = {
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
}, sn = (e, t, r) => {
  const n = r.getDerivativeToken(e), {
    override: o,
    ...i
  } = t;
  let s = {
    ...n,
    override: o
  };
  return s = Zi(s), i && Object.entries(i).forEach(([a, c]) => {
    const {
      theme: u,
      ...p
    } = c;
    let f = p;
    u && (f = sn({
      ...s,
      ...p
    }, {
      override: p
    }, u)), s[a] = f;
  }), s;
};
function ts() {
  const {
    token: e,
    hashed: t,
    theme: r = Ji,
    override: n,
    cssVar: o
  } = l.useContext(Be._internalContext), [i, s, a] = Bn(r, [Be.defaultSeed, e], {
    salt: `${jo}-${t || ""}`,
    override: n,
    getComputedToken: sn,
    cssVar: o && {
      prefix: o.prefix,
      key: o.key,
      unitless: Qi,
      ignore: Yi,
      preserve: es
    }
  });
  return [r, a, t ? s : "", i, o];
}
const {
  genStyleHooks: rs
} = Wi({
  usePrefix: () => {
    const {
      getPrefixCls: e,
      iconPrefixCls: t
    } = Ve();
    return {
      iconPrefixCls: t,
      rootPrefixCls: e()
    };
  },
  useToken: () => {
    const [e, t, r, n, o] = ts();
    return {
      theme: e,
      realToken: t,
      hashId: r,
      token: n,
      cssVar: o
    };
  },
  useCSP: () => {
    const {
      csp: e
    } = Ve();
    return e ?? {};
  },
  layer: {
    name: "antdx",
    dependencies: ["antd"]
  }
}), ns = (e) => {
  const {
    componentCls: t,
    antCls: r,
    calc: n
  } = e, o = `${t}-list-card`, i = n(e.fontSize).mul(e.lineHeight).mul(2).add(e.paddingSM).add(e.paddingSM).equal();
  return {
    [o]: {
      borderRadius: e.borderRadius,
      position: "relative",
      background: e.colorFillContent,
      borderWidth: e.lineWidth,
      borderStyle: "solid",
      borderColor: "transparent",
      flex: "none",
      // =============================== Desc ================================
      [`${o}-name,${o}-desc`]: {
        display: "flex",
        flexWrap: "nowrap",
        maxWidth: "100%"
      },
      [`${o}-ellipsis-prefix`]: {
        flex: "0 1 auto",
        minWidth: 0,
        overflow: "hidden",
        textOverflow: "ellipsis",
        whiteSpace: "nowrap"
      },
      [`${o}-ellipsis-suffix`]: {
        flex: "none"
      },
      // ============================= Overview ==============================
      "&-type-overview": {
        padding: n(e.paddingSM).sub(e.lineWidth).equal(),
        paddingInlineStart: n(e.padding).add(e.lineWidth).equal(),
        display: "flex",
        flexWrap: "nowrap",
        gap: e.paddingXS,
        alignItems: "flex-start",
        width: 236,
        // Icon
        [`${o}-icon`]: {
          fontSize: n(e.fontSizeLG).mul(2).equal(),
          lineHeight: 1,
          paddingTop: n(e.paddingXXS).mul(1.5).equal(),
          flex: "none"
        },
        // Content
        [`${o}-content`]: {
          flex: "auto",
          minWidth: 0,
          display: "flex",
          flexDirection: "column",
          alignItems: "stretch"
        },
        [`${o}-desc`]: {
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
        [`&:not(${o}-status-error)`]: {
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
        [`${o}-img-mask`]: {
          position: "absolute",
          inset: 0,
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          background: `rgba(0, 0, 0, ${e.opacityLoading})`,
          borderRadius: "inherit"
        },
        // Error
        [`&${o}-status-error`]: {
          [`img, ${o}-img-mask`]: {
            borderRadius: n(e.borderRadius).sub(e.lineWidth).equal()
          },
          [`${o}-desc`]: {
            paddingInline: e.paddingXXS
          }
        },
        // Progress
        [`${o}-progress`]: {}
      },
      // ============================ Remove Icon ============================
      [`${o}-remove`]: {
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
      [`&:hover ${o}-remove`]: {
        display: "block"
      },
      // ============================== Status ===============================
      "&-status-error": {
        borderColor: e.colorError,
        [`${o}-desc`]: {
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
          marginInlineEnd: n(e.paddingSM).mul(-1).equal()
        }
      }
    }
  };
}, Ot = {
  "&, *": {
    boxSizing: "border-box"
  }
}, os = (e) => {
  const {
    componentCls: t,
    calc: r,
    antCls: n
  } = e, o = `${t}-drop-area`, i = `${t}-placeholder`;
  return {
    // ============================== Full Screen ==============================
    [o]: {
      position: "absolute",
      inset: 0,
      zIndex: e.zIndexPopupBase,
      ...Ot,
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
        ...Ot,
        [`${n}-upload-wrapper ${n}-upload${n}-upload-btn`]: {
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
}, is = (e) => {
  const {
    componentCls: t,
    calc: r
  } = e, n = `${t}-list`, o = r(e.fontSize).mul(e.lineHeight).mul(2).add(e.paddingSM).add(e.paddingSM).equal();
  return {
    [t]: {
      position: "relative",
      width: "100%",
      ...Ot,
      // =============================== File List ===============================
      [n]: {
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
          maxHeight: r(o).mul(3).equal(),
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
          width: o,
          height: o,
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
          [`&${n}-overflow-ping-start ${n}-prev-btn`]: {
            opacity: 1,
            pointerEvents: "auto"
          },
          [`&${n}-overflow-ping-end ${n}-next-btn`]: {
            opacity: 1,
            pointerEvents: "auto"
          }
        },
        "&:dir(rtl)": {
          [`&${n}-overflow-ping-end ${n}-prev-btn`]: {
            opacity: 1,
            pointerEvents: "auto"
          },
          [`&${n}-overflow-ping-start ${n}-next-btn`]: {
            opacity: 1,
            pointerEvents: "auto"
          }
        }
      }
    }
  };
}, ss = (e) => {
  const {
    colorBgContainer: t
  } = e;
  return {
    colorBgPlaceholderHover: new te(t).setA(0.85).toRgbString()
  };
}, an = rs("Attachments", (e) => {
  const t = Dt(e, {});
  return [os(t), is(t), ns(t)];
}, ss), as = (e) => e.indexOf("image/") === 0, je = 200;
function ls(e) {
  return new Promise((t) => {
    if (!e || !e.type || !as(e.type)) {
      t("");
      return;
    }
    const r = new Image();
    if (r.onload = () => {
      const {
        width: n,
        height: o
      } = r, i = n / o, s = i > 1 ? je : je * i, a = i > 1 ? je / i : je, c = document.createElement("canvas");
      c.width = s, c.height = a, c.style.cssText = `position: fixed; left: 0; top: 0; width: ${s}px; height: ${a}px; z-index: 9999; display: none;`, document.body.appendChild(c), c.getContext("2d").drawImage(r, 0, 0, s, a);
      const p = c.toDataURL();
      document.body.removeChild(c), window.URL.revokeObjectURL(r.src), t(p);
    }, r.crossOrigin = "anonymous", e.type.startsWith("image/svg+xml")) {
      const n = new FileReader();
      n.onload = () => {
        n.result && typeof n.result == "string" && (r.src = n.result);
      }, n.readAsDataURL(e);
    } else if (e.type.startsWith("image/gif")) {
      const n = new FileReader();
      n.onload = () => {
        n.result && t(n.result);
      }, n.readAsDataURL(e);
    } else
      r.src = window.URL.createObjectURL(e);
  });
}
function cs() {
  return /* @__PURE__ */ l.createElement("svg", {
    width: "1em",
    height: "1em",
    viewBox: "0 0 16 16",
    version: "1.1",
    xmlns: "http://www.w3.org/2000/svg"
    //xmlnsXlink="http://www.w3.org/1999/xlink"
  }, /* @__PURE__ */ l.createElement("title", null, "audio"), /* @__PURE__ */ l.createElement("g", {
    stroke: "none",
    strokeWidth: "1",
    fill: "none",
    fillRule: "evenodd"
  }, /* @__PURE__ */ l.createElement("path", {
    d: "M14.1178571,4.0125 C14.225,4.11964286 14.2857143,4.26428571 14.2857143,4.41607143 L14.2857143,15.4285714 C14.2857143,15.7446429 14.0303571,16 13.7142857,16 L2.28571429,16 C1.96964286,16 1.71428571,15.7446429 1.71428571,15.4285714 L1.71428571,0.571428571 C1.71428571,0.255357143 1.96964286,0 2.28571429,0 L9.86964286,0 C10.0214286,0 10.1678571,0.0607142857 10.275,0.167857143 L14.1178571,4.0125 Z M10.7315824,7.11216117 C10.7428131,7.15148751 10.7485063,7.19218979 10.7485063,7.23309113 L10.7485063,8.07742614 C10.7484199,8.27364959 10.6183424,8.44607275 10.4296853,8.50003683 L8.32984514,9.09986306 L8.32984514,11.7071803 C8.32986605,12.5367078 7.67249692,13.217028 6.84345686,13.2454634 L6.79068592,13.2463395 C6.12766108,13.2463395 5.53916361,12.8217001 5.33010655,12.1924966 C5.1210495,11.563293 5.33842118,10.8709227 5.86959669,10.4741173 C6.40077221,10.0773119 7.12636292,10.0652587 7.67042486,10.4442027 L7.67020842,7.74937024 L7.68449368,7.74937024 C7.72405122,7.59919041 7.83988806,7.48101083 7.98924584,7.4384546 L10.1880418,6.81004755 C10.42156,6.74340323 10.6648954,6.87865515 10.7315824,7.11216117 Z M9.60714286,1.31785714 L12.9678571,4.67857143 L9.60714286,4.67857143 L9.60714286,1.31785714 Z",
    fill: "currentColor"
  })));
}
function us(e) {
  const {
    percent: t
  } = e, {
    token: r
  } = Be.useToken();
  return /* @__PURE__ */ l.createElement(_n, {
    type: "circle",
    percent: t,
    size: r.fontSizeHeading2 * 2,
    strokeColor: "#FFF",
    trailColor: "rgba(255, 255, 255, 0.3)",
    format: (n) => /* @__PURE__ */ l.createElement("span", {
      style: {
        color: "#FFF"
      }
    }, (n || 0).toFixed(0), "%")
  });
}
function fs() {
  return /* @__PURE__ */ l.createElement("svg", {
    width: "1em",
    height: "1em",
    viewBox: "0 0 16 16",
    version: "1.1",
    xmlns: "http://www.w3.org/2000/svg"
    // xmlnsXlink="http://www.w3.org/1999/xlink"
  }, /* @__PURE__ */ l.createElement("title", null, "video"), /* @__PURE__ */ l.createElement("g", {
    stroke: "none",
    strokeWidth: "1",
    fill: "none",
    fillRule: "evenodd"
  }, /* @__PURE__ */ l.createElement("path", {
    d: "M14.1178571,4.0125 C14.225,4.11964286 14.2857143,4.26428571 14.2857143,4.41607143 L14.2857143,15.4285714 C14.2857143,15.7446429 14.0303571,16 13.7142857,16 L2.28571429,16 C1.96964286,16 1.71428571,15.7446429 1.71428571,15.4285714 L1.71428571,0.571428571 C1.71428571,0.255357143 1.96964286,0 2.28571429,0 L9.86964286,0 C10.0214286,0 10.1678571,0.0607142857 10.275,0.167857143 L14.1178571,4.0125 Z M12.9678571,4.67857143 L9.60714286,1.31785714 L9.60714286,4.67857143 L12.9678571,4.67857143 Z M10.5379461,10.3101106 L6.68957555,13.0059749 C6.59910784,13.0693494 6.47439406,13.0473861 6.41101953,12.9569184 C6.3874624,12.9232903 6.37482581,12.8832269 6.37482581,12.8421686 L6.37482581,7.45043999 C6.37482581,7.33998304 6.46436886,7.25043999 6.57482581,7.25043999 C6.61588409,7.25043999 6.65594753,7.26307658 6.68957555,7.28663371 L10.5379461,9.98249803 C10.6284138,10.0458726 10.6503772,10.1705863 10.5870027,10.2610541 C10.5736331,10.2801392 10.5570312,10.2967411 10.5379461,10.3101106 Z",
    fill: "currentColor"
  })));
}
const xt = " ", $t = "#8c8c8c", ln = ["png", "jpg", "jpeg", "gif", "bmp", "webp", "svg"], ds = [{
  icon: /* @__PURE__ */ l.createElement(Mn, null),
  color: "#22b35e",
  ext: ["xlsx", "xls"]
}, {
  icon: /* @__PURE__ */ l.createElement(In, null),
  color: $t,
  ext: ln
}, {
  icon: /* @__PURE__ */ l.createElement(On, null),
  color: $t,
  ext: ["md", "mdx"]
}, {
  icon: /* @__PURE__ */ l.createElement($n, null),
  color: "#ff4d4f",
  ext: ["pdf"]
}, {
  icon: /* @__PURE__ */ l.createElement(An, null),
  color: "#ff6e31",
  ext: ["ppt", "pptx"]
}, {
  icon: /* @__PURE__ */ l.createElement(Fn, null),
  color: "#1677ff",
  ext: ["doc", "docx"]
}, {
  icon: /* @__PURE__ */ l.createElement(kn, null),
  color: "#fab714",
  ext: ["zip", "rar", "7z", "tar", "gz"]
}, {
  icon: /* @__PURE__ */ l.createElement(fs, null),
  color: "#ff4d4f",
  ext: ["mp4", "avi", "mov", "wmv", "flv", "mkv"]
}, {
  icon: /* @__PURE__ */ l.createElement(cs, null),
  color: "#8c8c8c",
  ext: ["mp3", "wav", "flac", "ape", "aac", "ogg"]
}];
function Tr(e, t) {
  return t.some((r) => e.toLowerCase() === `.${r}`);
}
function ps(e) {
  let t = e;
  const r = ["B", "KB", "MB", "GB", "TB", "PB", "EB"];
  let n = 0;
  for (; t >= 1024 && n < r.length - 1; )
    t /= 1024, n++;
  return `${t.toFixed(0)} ${r[n]}`;
}
function ms(e, t) {
  const {
    prefixCls: r,
    item: n,
    onRemove: o,
    className: i,
    style: s,
    imageProps: a
  } = e, c = l.useContext(_e), {
    disabled: u
  } = c || {}, {
    name: p,
    size: f,
    percent: d,
    status: m = "done",
    description: b
  } = n, {
    getPrefixCls: x
  } = Ve(), g = x("attachment", r), h = `${g}-list-card`, [E, T, S] = an(g), [w, v] = l.useMemo(() => {
    const j = p || "", z = j.match(/^(.*)\.[^.]+$/);
    return z ? [z[1], j.slice(z[1].length)] : [j, ""];
  }, [p]), _ = l.useMemo(() => Tr(v, ln), [v]), y = l.useMemo(() => b || (m === "uploading" ? `${d || 0}%` : m === "error" ? n.response || xt : f ? ps(f) : xt), [m, d]), [L, F] = l.useMemo(() => {
    for (const {
      ext: j,
      icon: z,
      color: W
    } of ds)
      if (Tr(v, j))
        return [z, W];
    return [/* @__PURE__ */ l.createElement(Ln, {
      key: "defaultIcon"
    }), $t];
  }, [v]), [k, P] = l.useState();
  l.useEffect(() => {
    if (n.originFileObj) {
      let j = !0;
      return ls(n.originFileObj).then((z) => {
        j && P(z);
      }), () => {
        j = !1;
      };
    }
    P(void 0);
  }, [n.originFileObj]);
  let O = null;
  const $ = n.thumbUrl || n.url || k, A = _ && (n.originFileObj || $);
  return A ? O = /* @__PURE__ */ l.createElement(l.Fragment, null, $ && /* @__PURE__ */ l.createElement(Rn, he({
    alt: "preview",
    src: $
  }, a)), m !== "done" && /* @__PURE__ */ l.createElement("div", {
    className: `${h}-img-mask`
  }, m === "uploading" && d !== void 0 && /* @__PURE__ */ l.createElement(us, {
    percent: d,
    prefixCls: h
  }), m === "error" && /* @__PURE__ */ l.createElement("div", {
    className: `${h}-desc`
  }, /* @__PURE__ */ l.createElement("div", {
    className: `${h}-ellipsis-prefix`
  }, y)))) : O = /* @__PURE__ */ l.createElement(l.Fragment, null, /* @__PURE__ */ l.createElement("div", {
    className: `${h}-icon`,
    style: {
      color: F
    }
  }, L), /* @__PURE__ */ l.createElement("div", {
    className: `${h}-content`
  }, /* @__PURE__ */ l.createElement("div", {
    className: `${h}-name`
  }, /* @__PURE__ */ l.createElement("div", {
    className: `${h}-ellipsis-prefix`
  }, w ?? xt), /* @__PURE__ */ l.createElement("div", {
    className: `${h}-ellipsis-suffix`
  }, v)), /* @__PURE__ */ l.createElement("div", {
    className: `${h}-desc`
  }, /* @__PURE__ */ l.createElement("div", {
    className: `${h}-ellipsis-prefix`
  }, y)))), E(/* @__PURE__ */ l.createElement("div", {
    className: Z(h, {
      [`${h}-status-${m}`]: m,
      [`${h}-type-preview`]: A,
      [`${h}-type-overview`]: !A
    }, i, T, S),
    style: s,
    ref: t
  }, O, !u && o && /* @__PURE__ */ l.createElement("button", {
    type: "button",
    className: `${h}-remove`,
    onClick: () => {
      o(n);
    }
  }, /* @__PURE__ */ l.createElement(Pn, null))));
}
const cn = /* @__PURE__ */ l.forwardRef(ms), Lr = 1;
function gs(e) {
  const {
    prefixCls: t,
    items: r,
    onRemove: n,
    overflow: o,
    upload: i,
    listClassName: s,
    listStyle: a,
    itemClassName: c,
    itemStyle: u,
    imageProps: p
  } = e, f = `${t}-list`, d = l.useRef(null), [m, b] = l.useState(!1), {
    disabled: x
  } = l.useContext(_e);
  l.useEffect(() => (b(!0), () => {
    b(!1);
  }), []);
  const [g, h] = l.useState(!1), [E, T] = l.useState(!1), S = () => {
    const y = d.current;
    y && (o === "scrollX" ? (h(Math.abs(y.scrollLeft) >= Lr), T(y.scrollWidth - y.clientWidth - Math.abs(y.scrollLeft) >= Lr)) : o === "scrollY" && (h(y.scrollTop !== 0), T(y.scrollHeight - y.clientHeight !== y.scrollTop)));
  };
  l.useEffect(() => {
    S();
  }, [o, r.length]);
  const w = (y) => {
    const L = d.current;
    L && L.scrollTo({
      left: L.scrollLeft + y * L.clientWidth,
      behavior: "smooth"
    });
  }, v = () => {
    w(-1);
  }, _ = () => {
    w(1);
  };
  return /* @__PURE__ */ l.createElement("div", {
    className: Z(f, {
      [`${f}-overflow-${e.overflow}`]: o,
      [`${f}-overflow-ping-start`]: g,
      [`${f}-overflow-ping-end`]: E
    }, s),
    ref: d,
    onScroll: S,
    style: a
  }, /* @__PURE__ */ l.createElement($i, {
    keys: r.map((y) => ({
      key: y.uid,
      item: y
    })),
    motionName: `${f}-card-motion`,
    component: !1,
    motionAppear: m,
    motionLeave: !0,
    motionEnter: !0
  }, ({
    key: y,
    item: L,
    className: F,
    style: k
  }) => /* @__PURE__ */ l.createElement(cn, {
    key: y,
    prefixCls: t,
    item: L,
    onRemove: n,
    className: Z(F, c),
    imageProps: p,
    style: {
      ...k,
      ...u
    }
  })), !x && /* @__PURE__ */ l.createElement(tn, {
    upload: i
  }, /* @__PURE__ */ l.createElement(ct, {
    className: `${f}-upload-btn`,
    type: "dashed"
  }, /* @__PURE__ */ l.createElement(jn, {
    className: `${f}-upload-btn-icon`
  }))), o === "scrollX" && /* @__PURE__ */ l.createElement(l.Fragment, null, /* @__PURE__ */ l.createElement(ct, {
    size: "small",
    shape: "circle",
    className: `${f}-prev-btn`,
    icon: /* @__PURE__ */ l.createElement(Dn, null),
    onClick: v
  }), /* @__PURE__ */ l.createElement(ct, {
    size: "small",
    shape: "circle",
    className: `${f}-next-btn`,
    icon: /* @__PURE__ */ l.createElement(Nn, null),
    onClick: _
  })));
}
function hs(e, t) {
  const {
    prefixCls: r,
    placeholder: n = {},
    upload: o,
    className: i,
    style: s
  } = e, a = `${r}-placeholder`, c = n || {}, {
    disabled: u
  } = l.useContext(_e), [p, f] = l.useState(!1), d = () => {
    f(!0);
  }, m = (g) => {
    g.currentTarget.contains(g.relatedTarget) || f(!1);
  }, b = () => {
    f(!1);
  }, x = /* @__PURE__ */ l.isValidElement(n) ? n : /* @__PURE__ */ l.createElement(Tn, {
    align: "center",
    justify: "center",
    vertical: !0,
    className: `${a}-inner`
  }, /* @__PURE__ */ l.createElement(ut.Text, {
    className: `${a}-icon`
  }, c.icon), /* @__PURE__ */ l.createElement(ut.Title, {
    className: `${a}-title`,
    level: 5
  }, c.title), /* @__PURE__ */ l.createElement(ut.Text, {
    className: `${a}-description`,
    type: "secondary"
  }, c.description));
  return /* @__PURE__ */ l.createElement("div", {
    className: Z(a, {
      [`${a}-drag-in`]: p,
      [`${a}-disabled`]: u
    }, i),
    onDragEnter: d,
    onDragLeave: m,
    onDrop: b,
    "aria-hidden": u,
    style: s
  }, /* @__PURE__ */ l.createElement(Ir.Dragger, he({
    showUploadList: !1
  }, o, {
    ref: t,
    style: {
      padding: 0,
      border: 0,
      background: "transparent"
    }
  }), x));
}
const vs = /* @__PURE__ */ l.forwardRef(hs);
function bs(e, t) {
  const {
    prefixCls: r,
    rootClassName: n,
    rootStyle: o,
    className: i,
    style: s,
    items: a,
    children: c,
    getDropContainer: u,
    placeholder: p,
    onChange: f,
    onRemove: d,
    overflow: m,
    imageProps: b,
    disabled: x,
    classNames: g = {},
    styles: h = {},
    ...E
  } = e, {
    getPrefixCls: T,
    direction: S
  } = Ve(), w = T("attachment", r), v = zo("attachments"), {
    classNames: _,
    styles: y
  } = v, L = l.useRef(null), F = l.useRef(null);
  l.useImperativeHandle(t, () => ({
    nativeElement: L.current,
    upload: (D) => {
      var N, G;
      const X = (G = (N = F.current) == null ? void 0 : N.nativeElement) == null ? void 0 : G.querySelector('input[type="file"]');
      if (X) {
        const ae = new DataTransfer();
        ae.items.add(D), X.files = ae.files, X.dispatchEvent(new Event("change", {
          bubbles: !0
        }));
      }
    }
  }));
  const [k, P, O] = an(w), $ = Z(P, O), [A, j] = Wo([], {
    value: a
  }), z = ve((D) => {
    j(D.fileList), f == null || f(D);
  }), W = {
    ...E,
    fileList: A,
    onChange: z
  }, fe = (D) => Promise.resolve(typeof d == "function" ? d(D) : d).then((X) => {
    if (X === !1)
      return;
    const N = A.filter((G) => G.uid !== D.uid);
    z({
      file: {
        ...D,
        status: "removed"
      },
      fileList: N
    });
  });
  let oe;
  const B = (D, X, N) => {
    const G = typeof p == "function" ? p(D) : p;
    return /* @__PURE__ */ l.createElement(vs, {
      placeholder: G,
      upload: W,
      prefixCls: w,
      className: Z(_.placeholder, g.placeholder),
      style: {
        ...y.placeholder,
        ...h.placeholder,
        ...X == null ? void 0 : X.style
      },
      ref: N
    });
  };
  if (c)
    oe = /* @__PURE__ */ l.createElement(l.Fragment, null, /* @__PURE__ */ l.createElement(tn, {
      upload: W,
      rootClassName: n,
      ref: F
    }, c), /* @__PURE__ */ l.createElement(cr, {
      getDropContainer: u,
      prefixCls: w,
      className: Z($, n)
    }, B("drop")));
  else {
    const D = A.length > 0;
    oe = /* @__PURE__ */ l.createElement("div", {
      className: Z(w, $, {
        [`${w}-rtl`]: S === "rtl"
      }, i, n),
      style: {
        ...o,
        ...s
      },
      dir: S || "ltr",
      ref: L
    }, /* @__PURE__ */ l.createElement(gs, {
      prefixCls: w,
      items: A,
      onRemove: fe,
      overflow: m,
      upload: W,
      listClassName: Z(_.list, g.list),
      listStyle: {
        ...y.list,
        ...h.list,
        ...!D && {
          display: "none"
        }
      },
      itemClassName: Z(_.item, g.item),
      itemStyle: {
        ...y.item,
        ...h.item
      },
      imageProps: b
    }), B("inline", D ? {
      style: {
        display: "none"
      }
    } : {}, F), /* @__PURE__ */ l.createElement(cr, {
      getDropContainer: u || (() => L.current),
      prefixCls: w,
      className: $
    }, B("drop")));
  }
  return k(/* @__PURE__ */ l.createElement(_e.Provider, {
    value: {
      disabled: x
    }
  }, oe));
}
const un = /* @__PURE__ */ l.forwardRef(bs);
un.FileCard = cn;
new Intl.Collator(0, {
  numeric: 1
}).compare;
typeof process < "u" && process.versions && process.versions.node;
var ne;
class Ts extends TransformStream {
  /** Constructs a new instance. */
  constructor(r = {
    allowCR: !1
  }) {
    super({
      transform: (n, o) => {
        for (n = de(this, ne) + n; ; ) {
          const i = n.indexOf(`
`), s = r.allowCR ? n.indexOf("\r") : -1;
          if (s !== -1 && s !== n.length - 1 && (i === -1 || i - 1 > s)) {
            o.enqueue(n.slice(0, s)), n = n.slice(s + 1);
            continue;
          }
          if (i === -1) break;
          const a = n[i - 1] === "\r" ? i - 1 : i;
          o.enqueue(n.slice(0, a)), n = n.slice(i + 1);
        }
        Ut(this, ne, n);
      },
      flush: (n) => {
        if (de(this, ne) === "") return;
        const o = r.allowCR && de(this, ne).endsWith("\r") ? de(this, ne).slice(0, -1) : de(this, ne);
        n.enqueue(o);
      }
    });
    Vt(this, ne, "");
  }
}
ne = new WeakMap();
function ys(e) {
  try {
    const t = new URL(e);
    return t.protocol === "http:" || t.protocol === "https:";
  } catch {
    return !1;
  }
}
function Ss() {
  const e = document.querySelector(".gradio-container");
  if (!e)
    return "";
  const t = e.className.match(/gradio-container-(.+)/);
  return t ? t[1] : "";
}
const xs = +Ss()[0];
function Pr(e, t, r) {
  const n = xs >= 5 ? "gradio_api/" : "";
  return e == null ? r ? `/proxy=${r}${n}file=` : `${t}${n}file=` : ys(e) ? e : r ? `/proxy=${r}${n}file=${e}` : `${t}/${n}file=${e}`;
}
const ws = ({
  item: e,
  urlRoot: t,
  urlProxyUrl: r,
  ...n
}) => {
  const o = Mr(() => e ? typeof e == "string" ? {
    url: e.startsWith("http") ? e : Pr(e, t, r),
    uid: e,
    name: e.split("/").pop()
  } : {
    ...e,
    uid: e.uid || e.path || e.url,
    name: e.name || e.orig_name || (e.url || e.path).split("/").pop(),
    url: e.url || Pr(e.path, t, r)
  } : {}, [e, r, t]);
  return /* @__PURE__ */ U.jsx(un.FileCard, {
    ...n,
    imageProps: {
      ...n.imageProps
      // fixed in @ant-design/x@1.2.0
      // wrapperStyle: {
      //   width: '100%',
      //   height: '100%',
      //   ...props.imageProps?.wrapperStyle,
      // },
      // style: {
      //   width: '100%',
      //   height: '100%',
      //   objectFit: 'contain',
      //   borderRadius: token.borderRadius,
      //   ...props.imageProps?.style,
      // },
    },
    item: o
  });
};
function Es(e) {
  return typeof e == "object" && e !== null ? e : {};
}
const Ls = To(({
  setSlotParams: e,
  imageProps: t,
  slots: r,
  children: n,
  ...o
}) => {
  const i = Es(t == null ? void 0 : t.preview), s = r["imageProps.preview.mask"] || r["imageProps.preview.closeIcon"] || r["imageProps.preview.toolbarRender"] || r["imageProps.preview.imageRender"] || (t == null ? void 0 : t.preview) !== !1, a = mt(i.getContainer), c = mt(i.toolbarRender), u = mt(i.imageRender);
  return /* @__PURE__ */ U.jsxs(U.Fragment, {
    children: [/* @__PURE__ */ U.jsx("div", {
      style: {
        display: "none"
      },
      children: n
    }), /* @__PURE__ */ U.jsx(ws, {
      ...o,
      imageProps: {
        ...t,
        preview: s ? Ao({
          ...i,
          getContainer: a,
          toolbarRender: r["imageProps.preview.toolbarRender"] ? ir({
            slots: r,
            key: "imageProps.preview.toolbarRender"
          }) : c,
          imageRender: r["imageProps.preview.imageRender"] ? ir({
            slots: r,
            key: "imageProps.preview.imageRender"
          }) : u,
          ...r["imageProps.preview.mask"] || Reflect.has(i, "mask") ? {
            mask: r["imageProps.preview.mask"] ? /* @__PURE__ */ U.jsx(we, {
              slot: r["imageProps.preview.mask"]
            }) : i.mask
          } : {},
          closeIcon: r["imageProps.preview.closeIcon"] ? /* @__PURE__ */ U.jsx(we, {
            slot: r["imageProps.preview.closeIcon"]
          }) : i.closeIcon
        }) : !1,
        placeholder: r["imageProps.placeholder"] ? /* @__PURE__ */ U.jsx(we, {
          slot: r["imageProps.placeholder"]
        }) : t == null ? void 0 : t.placeholder
      }
    })]
  });
});
export {
  Ls as AttachmentsFileCard,
  Ls as default
};
