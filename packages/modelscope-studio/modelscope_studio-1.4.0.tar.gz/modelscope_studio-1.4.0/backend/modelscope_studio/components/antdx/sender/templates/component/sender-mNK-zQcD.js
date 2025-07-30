import { i as xr, a as Rt, r as Er, b as Cr, w as Ge, g as wr, c as ee, d as _r } from "./Index-DKw0y_Bv.js";
const h = window.ms_globals.React, b = window.ms_globals.React, mr = window.ms_globals.React.forwardRef, ne = window.ms_globals.React.useRef, In = window.ms_globals.React.useState, ge = window.ms_globals.React.useEffect, hr = window.ms_globals.React.version, gr = window.ms_globals.React.isValidElement, vr = window.ms_globals.React.useLayoutEffect, yr = window.ms_globals.React.useImperativeHandle, br = window.ms_globals.React.memo, Sr = window.ms_globals.React.useMemo, Ut = window.ms_globals.ReactDOM, Tt = window.ms_globals.ReactDOM.createPortal, Tr = window.ms_globals.internalContext.useContextPropsContext, Rr = window.ms_globals.internalContext.useSuggestionOpenContext, Pr = window.ms_globals.antd.ConfigProvider, Pt = window.ms_globals.antd.theme, Ln = window.ms_globals.antd.Button, Or = window.ms_globals.antd.Input, Mr = window.ms_globals.antd.Flex, Ar = window.ms_globals.antdIcons.CloseOutlined, Ir = window.ms_globals.antdIcons.ClearOutlined, Lr = window.ms_globals.antdIcons.ArrowUpOutlined, kr = window.ms_globals.antdIcons.AudioMutedOutlined, jr = window.ms_globals.antdIcons.AudioOutlined, Ot = window.ms_globals.antdCssinjs.unit, vt = window.ms_globals.antdCssinjs.token2CSSVar, Wt = window.ms_globals.antdCssinjs.useStyleRegister, $r = window.ms_globals.antdCssinjs.useCSSVarRegister, Dr = window.ms_globals.antdCssinjs.createTheme, Nr = window.ms_globals.antdCssinjs.useCacheToken;
var Br = /\s/;
function Hr(e) {
  for (var t = e.length; t-- && Br.test(e.charAt(t)); )
    ;
  return t;
}
var Vr = /^\s+/;
function Fr(e) {
  return e && e.slice(0, Hr(e) + 1).replace(Vr, "");
}
var Kt = NaN, zr = /^[-+]0x[0-9a-f]+$/i, Xr = /^0b[01]+$/i, Ur = /^0o[0-7]+$/i, Wr = parseInt;
function Gt(e) {
  if (typeof e == "number")
    return e;
  if (xr(e))
    return Kt;
  if (Rt(e)) {
    var t = typeof e.valueOf == "function" ? e.valueOf() : e;
    e = Rt(t) ? t + "" : t;
  }
  if (typeof e != "string")
    return e === 0 ? e : +e;
  e = Fr(e);
  var n = Xr.test(e);
  return n || Ur.test(e) ? Wr(e.slice(2), n ? 2 : 8) : zr.test(e) ? Kt : +e;
}
var yt = function() {
  return Er.Date.now();
}, Kr = "Expected a function", Gr = Math.max, qr = Math.min;
function Qr(e, t, n) {
  var o, r, i, s, a, u, c = 0, f = !1, l = !1, d = !0;
  if (typeof e != "function")
    throw new TypeError(Kr);
  t = Gt(t) || 0, Rt(n) && (f = !!n.leading, l = "maxWait" in n, i = l ? Gr(Gt(n.maxWait) || 0, t) : i, d = "trailing" in n ? !!n.trailing : d);
  function p(S) {
    var R = o, P = r;
    return o = r = void 0, c = S, s = e.apply(P, R), s;
  }
  function v(S) {
    return c = S, a = setTimeout(x, t), f ? p(S) : s;
  }
  function g(S) {
    var R = S - u, P = S - c, I = t - R;
    return l ? qr(I, i - P) : I;
  }
  function m(S) {
    var R = S - u, P = S - c;
    return u === void 0 || R >= t || R < 0 || l && P >= i;
  }
  function x() {
    var S = yt();
    if (m(S))
      return E(S);
    a = setTimeout(x, g(S));
  }
  function E(S) {
    return a = void 0, d && o ? p(S) : (o = r = void 0, s);
  }
  function _() {
    a !== void 0 && clearTimeout(a), c = 0, o = u = r = a = void 0;
  }
  function y() {
    return a === void 0 ? s : E(yt());
  }
  function T() {
    var S = yt(), R = m(S);
    if (o = arguments, r = this, u = S, R) {
      if (a === void 0)
        return v(u);
      if (l)
        return clearTimeout(a), a = setTimeout(x, t), p(u);
    }
    return a === void 0 && (a = setTimeout(x, t)), s;
  }
  return T.cancel = _, T.flush = y, T;
}
function Yr(e, t) {
  return Cr(e, t);
}
var kn = {
  exports: {}
}, tt = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var Zr = b, Jr = Symbol.for("react.element"), eo = Symbol.for("react.fragment"), to = Object.prototype.hasOwnProperty, no = Zr.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, ro = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function jn(e, t, n) {
  var o, r = {}, i = null, s = null;
  n !== void 0 && (i = "" + n), t.key !== void 0 && (i = "" + t.key), t.ref !== void 0 && (s = t.ref);
  for (o in t) to.call(t, o) && !ro.hasOwnProperty(o) && (r[o] = t[o]);
  if (e && e.defaultProps) for (o in t = e.defaultProps, t) r[o] === void 0 && (r[o] = t[o]);
  return {
    $$typeof: Jr,
    type: e,
    key: i,
    ref: s,
    props: r,
    _owner: no.current
  };
}
tt.Fragment = eo;
tt.jsx = jn;
tt.jsxs = jn;
kn.exports = tt;
var ce = kn.exports;
const {
  SvelteComponent: oo,
  assign: qt,
  binding_callbacks: Qt,
  check_outros: io,
  children: $n,
  claim_element: Dn,
  claim_space: so,
  component_subscribe: Yt,
  compute_slots: ao,
  create_slot: co,
  detach: Ce,
  element: Nn,
  empty: Zt,
  exclude_internal_props: Jt,
  get_all_dirty_from_scope: uo,
  get_slot_changes: lo,
  group_outros: fo,
  init: po,
  insert_hydration: qe,
  safe_not_equal: mo,
  set_custom_element_data: Bn,
  space: ho,
  transition_in: Qe,
  transition_out: Mt,
  update_slot_base: go
} = window.__gradio__svelte__internal, {
  beforeUpdate: vo,
  getContext: yo,
  onDestroy: bo,
  setContext: So
} = window.__gradio__svelte__internal;
function en(e) {
  let t, n;
  const o = (
    /*#slots*/
    e[7].default
  ), r = co(
    o,
    e,
    /*$$scope*/
    e[6],
    null
  );
  return {
    c() {
      t = Nn("svelte-slot"), r && r.c(), this.h();
    },
    l(i) {
      t = Dn(i, "SVELTE-SLOT", {
        class: !0
      });
      var s = $n(t);
      r && r.l(s), s.forEach(Ce), this.h();
    },
    h() {
      Bn(t, "class", "svelte-1rt0kpf");
    },
    m(i, s) {
      qe(i, t, s), r && r.m(t, null), e[9](t), n = !0;
    },
    p(i, s) {
      r && r.p && (!n || s & /*$$scope*/
      64) && go(
        r,
        o,
        i,
        /*$$scope*/
        i[6],
        n ? lo(
          o,
          /*$$scope*/
          i[6],
          s,
          null
        ) : uo(
          /*$$scope*/
          i[6]
        ),
        null
      );
    },
    i(i) {
      n || (Qe(r, i), n = !0);
    },
    o(i) {
      Mt(r, i), n = !1;
    },
    d(i) {
      i && Ce(t), r && r.d(i), e[9](null);
    }
  };
}
function xo(e) {
  let t, n, o, r, i = (
    /*$$slots*/
    e[4].default && en(e)
  );
  return {
    c() {
      t = Nn("react-portal-target"), n = ho(), i && i.c(), o = Zt(), this.h();
    },
    l(s) {
      t = Dn(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), $n(t).forEach(Ce), n = so(s), i && i.l(s), o = Zt(), this.h();
    },
    h() {
      Bn(t, "class", "svelte-1rt0kpf");
    },
    m(s, a) {
      qe(s, t, a), e[8](t), qe(s, n, a), i && i.m(s, a), qe(s, o, a), r = !0;
    },
    p(s, [a]) {
      /*$$slots*/
      s[4].default ? i ? (i.p(s, a), a & /*$$slots*/
      16 && Qe(i, 1)) : (i = en(s), i.c(), Qe(i, 1), i.m(o.parentNode, o)) : i && (fo(), Mt(i, 1, 1, () => {
        i = null;
      }), io());
    },
    i(s) {
      r || (Qe(i), r = !0);
    },
    o(s) {
      Mt(i), r = !1;
    },
    d(s) {
      s && (Ce(t), Ce(n), Ce(o)), e[8](null), i && i.d(s);
    }
  };
}
function tn(e) {
  const {
    svelteInit: t,
    ...n
  } = e;
  return n;
}
function Eo(e, t, n) {
  let o, r, {
    $$slots: i = {},
    $$scope: s
  } = t;
  const a = ao(i);
  let {
    svelteInit: u
  } = t;
  const c = Ge(tn(t)), f = Ge();
  Yt(e, f, (y) => n(0, o = y));
  const l = Ge();
  Yt(e, l, (y) => n(1, r = y));
  const d = [], p = yo("$$ms-gr-react-wrapper"), {
    slotKey: v,
    slotIndex: g,
    subSlotIndex: m
  } = wr() || {}, x = u({
    parent: p,
    props: c,
    target: f,
    slot: l,
    slotKey: v,
    slotIndex: g,
    subSlotIndex: m,
    onDestroy(y) {
      d.push(y);
    }
  });
  So("$$ms-gr-react-wrapper", x), vo(() => {
    c.set(tn(t));
  }), bo(() => {
    d.forEach((y) => y());
  });
  function E(y) {
    Qt[y ? "unshift" : "push"](() => {
      o = y, f.set(o);
    });
  }
  function _(y) {
    Qt[y ? "unshift" : "push"](() => {
      r = y, l.set(r);
    });
  }
  return e.$$set = (y) => {
    n(17, t = qt(qt({}, t), Jt(y))), "svelteInit" in y && n(5, u = y.svelteInit), "$$scope" in y && n(6, s = y.$$scope);
  }, t = Jt(t), [o, r, f, l, a, u, s, i, E, _];
}
class Co extends oo {
  constructor(t) {
    super(), po(this, t, Eo, xo, mo, {
      svelteInit: 5
    });
  }
}
const {
  SvelteComponent: Cs
} = window.__gradio__svelte__internal, nn = window.ms_globals.rerender, bt = window.ms_globals.tree;
function wo(e, t = {}) {
  function n(o) {
    const r = Ge(), i = new Co({
      ...o,
      props: {
        svelteInit(s) {
          window.ms_globals.autokey += 1;
          const a = {
            key: window.ms_globals.autokey,
            svelteInstance: r,
            reactComponent: e,
            props: s.props,
            slot: s.slot,
            target: s.target,
            slotIndex: s.slotIndex,
            subSlotIndex: s.subSlotIndex,
            ignore: t.ignore,
            slotKey: s.slotKey,
            nodes: []
          }, u = s.parent ?? bt;
          return u.nodes = [...u.nodes, a], nn({
            createPortal: Tt,
            node: bt
          }), s.onDestroy(() => {
            u.nodes = u.nodes.filter((c) => c.svelteInstance !== r), nn({
              createPortal: Tt,
              node: bt
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
const _o = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function To(e) {
  return e ? Object.keys(e).reduce((t, n) => {
    const o = e[n];
    return t[n] = Ro(n, o), t;
  }, {}) : {};
}
function Ro(e, t) {
  return typeof t == "number" && !_o.includes(e) ? t + "px" : t;
}
function At(e) {
  const t = [], n = e.cloneNode(!1);
  if (e._reactElement) {
    const r = b.Children.toArray(e._reactElement.props.children).map((i) => {
      if (b.isValidElement(i) && i.props.__slot__) {
        const {
          portals: s,
          clonedElement: a
        } = At(i.props.el);
        return b.cloneElement(i, {
          ...i.props,
          el: a,
          children: [...b.Children.toArray(i.props.children), ...s]
        });
      }
      return null;
    });
    return r.originalChildren = e._reactElement.props.children, t.push(Tt(b.cloneElement(e._reactElement, {
      ...e._reactElement.props,
      children: r
    }), n)), {
      clonedElement: n,
      portals: t
    };
  }
  Object.keys(e.getEventListeners()).forEach((r) => {
    e.getEventListeners(r).forEach(({
      listener: s,
      type: a,
      useCapture: u
    }) => {
      n.addEventListener(a, s, u);
    });
  });
  const o = Array.from(e.childNodes);
  for (let r = 0; r < o.length; r++) {
    const i = o[r];
    if (i.nodeType === 1) {
      const {
        clonedElement: s,
        portals: a
      } = At(i);
      t.push(...a), n.appendChild(s);
    } else i.nodeType === 3 && n.appendChild(i.cloneNode());
  }
  return {
    clonedElement: n,
    portals: t
  };
}
function Po(e, t) {
  e && (typeof e == "function" ? e(t) : e.current = t);
}
const He = mr(({
  slot: e,
  clone: t,
  className: n,
  style: o,
  observeAttributes: r
}, i) => {
  const s = ne(), [a, u] = In([]), {
    forceClone: c
  } = Tr(), f = c ? !0 : t;
  return ge(() => {
    var g;
    if (!s.current || !e)
      return;
    let l = e;
    function d() {
      let m = l;
      if (l.tagName.toLowerCase() === "svelte-slot" && l.children.length === 1 && l.children[0] && (m = l.children[0], m.tagName.toLowerCase() === "react-portal-target" && m.children[0] && (m = m.children[0])), Po(i, m), n && m.classList.add(...n.split(" ")), o) {
        const x = To(o);
        Object.keys(x).forEach((E) => {
          m.style[E] = x[E];
        });
      }
    }
    let p = null, v = null;
    if (f && window.MutationObserver) {
      let m = function() {
        var y, T, S;
        (y = s.current) != null && y.contains(l) && ((T = s.current) == null || T.removeChild(l));
        const {
          portals: E,
          clonedElement: _
        } = At(e);
        l = _, u(E), l.style.display = "contents", v && clearTimeout(v), v = setTimeout(() => {
          d();
        }, 50), (S = s.current) == null || S.appendChild(l);
      };
      m();
      const x = Qr(() => {
        m(), p == null || p.disconnect(), p == null || p.observe(e, {
          childList: !0,
          subtree: !0,
          attributes: r
        });
      }, 50);
      p = new window.MutationObserver(x), p.observe(e, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      l.style.display = "contents", d(), (g = s.current) == null || g.appendChild(l);
    return () => {
      var m, x;
      l.style.display = "", (m = s.current) != null && m.contains(l) && ((x = s.current) == null || x.removeChild(l)), p == null || p.disconnect();
    };
  }, [e, f, n, o, i, r, c]), b.createElement("react-child", {
    ref: s,
    style: {
      display: "contents"
    }
  }, ...a);
}), Oo = "1.3.0", Mo = /* @__PURE__ */ b.createContext({}), Ao = {
  classNames: {},
  styles: {},
  className: "",
  style: {}
}, Io = (e) => {
  const t = b.useContext(Mo);
  return b.useMemo(() => ({
    ...Ao,
    ...t[e]
  }), [t[e]]);
};
function ae() {
  return ae = Object.assign ? Object.assign.bind() : function(e) {
    for (var t = 1; t < arguments.length; t++) {
      var n = arguments[t];
      for (var o in n) ({}).hasOwnProperty.call(n, o) && (e[o] = n[o]);
    }
    return e;
  }, ae.apply(null, arguments);
}
function It() {
  const {
    getPrefixCls: e,
    direction: t,
    csp: n,
    iconPrefixCls: o,
    theme: r
  } = b.useContext(Pr.ConfigContext);
  return {
    theme: r,
    getPrefixCls: e,
    direction: t,
    csp: n,
    iconPrefixCls: o
  };
}
function ye(e) {
  var t = h.useRef();
  t.current = e;
  var n = h.useCallback(function() {
    for (var o, r = arguments.length, i = new Array(r), s = 0; s < r; s++)
      i[s] = arguments[s];
    return (o = t.current) === null || o === void 0 ? void 0 : o.call.apply(o, [t].concat(i));
  }, []);
  return n;
}
function Lo(e) {
  if (Array.isArray(e)) return e;
}
function ko(e, t) {
  var n = e == null ? null : typeof Symbol < "u" && e[Symbol.iterator] || e["@@iterator"];
  if (n != null) {
    var o, r, i, s, a = [], u = !0, c = !1;
    try {
      if (i = (n = n.call(e)).next, t !== 0) for (; !(u = (o = i.call(n)).done) && (a.push(o.value), a.length !== t); u = !0) ;
    } catch (f) {
      c = !0, r = f;
    } finally {
      try {
        if (!u && n.return != null && (s = n.return(), Object(s) !== s)) return;
      } finally {
        if (c) throw r;
      }
    }
    return a;
  }
}
function rn(e, t) {
  (t == null || t > e.length) && (t = e.length);
  for (var n = 0, o = Array(t); n < t; n++) o[n] = e[n];
  return o;
}
function jo(e, t) {
  if (e) {
    if (typeof e == "string") return rn(e, t);
    var n = {}.toString.call(e).slice(8, -1);
    return n === "Object" && e.constructor && (n = e.constructor.name), n === "Map" || n === "Set" ? Array.from(e) : n === "Arguments" || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n) ? rn(e, t) : void 0;
  }
}
function $o() {
  throw new TypeError(`Invalid attempt to destructure non-iterable instance.
In order to be iterable, non-array objects must have a [Symbol.iterator]() method.`);
}
function Ze(e, t) {
  return Lo(e) || ko(e, t) || jo(e, t) || $o();
}
function nt() {
  return !!(typeof window < "u" && window.document && window.document.createElement);
}
var on = nt() ? h.useLayoutEffect : h.useEffect, Do = function(t, n) {
  var o = h.useRef(!0);
  on(function() {
    return t(o.current);
  }, n), on(function() {
    return o.current = !1, function() {
      o.current = !0;
    };
  }, []);
}, sn = function(t, n) {
  Do(function(o) {
    if (!o)
      return t();
  }, n);
};
function De(e) {
  var t = h.useRef(!1), n = h.useState(e), o = Ze(n, 2), r = o[0], i = o[1];
  h.useEffect(function() {
    return t.current = !1, function() {
      t.current = !0;
    };
  }, []);
  function s(a, u) {
    u && t.current || i(a);
  }
  return [r, s];
}
function St(e) {
  return e !== void 0;
}
function Hn(e, t) {
  var n = t || {}, o = n.defaultValue, r = n.value, i = n.onChange, s = n.postState, a = De(function() {
    return St(r) ? r : St(o) ? typeof o == "function" ? o() : o : typeof e == "function" ? e() : e;
  }), u = Ze(a, 2), c = u[0], f = u[1], l = r !== void 0 ? r : c, d = s ? s(l) : l, p = ye(i), v = De([l]), g = Ze(v, 2), m = g[0], x = g[1];
  sn(function() {
    var _ = m[0];
    c !== _ && p(c, _);
  }, [m]), sn(function() {
    St(r) || f(r);
  }, [r]);
  var E = ye(function(_, y) {
    f(_, y), x([l], y);
  });
  return [d, E];
}
function le(e) {
  "@babel/helpers - typeof";
  return le = typeof Symbol == "function" && typeof Symbol.iterator == "symbol" ? function(t) {
    return typeof t;
  } : function(t) {
    return t && typeof Symbol == "function" && t.constructor === Symbol && t !== Symbol.prototype ? "symbol" : typeof t;
  }, le(e);
}
var Vn = {
  exports: {}
}, M = {};
/**
 * @license React
 * react-is.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var Ht = Symbol.for("react.element"), Vt = Symbol.for("react.portal"), rt = Symbol.for("react.fragment"), ot = Symbol.for("react.strict_mode"), it = Symbol.for("react.profiler"), st = Symbol.for("react.provider"), at = Symbol.for("react.context"), No = Symbol.for("react.server_context"), ct = Symbol.for("react.forward_ref"), ut = Symbol.for("react.suspense"), lt = Symbol.for("react.suspense_list"), ft = Symbol.for("react.memo"), dt = Symbol.for("react.lazy"), Bo = Symbol.for("react.offscreen"), Fn;
Fn = Symbol.for("react.module.reference");
function Q(e) {
  if (typeof e == "object" && e !== null) {
    var t = e.$$typeof;
    switch (t) {
      case Ht:
        switch (e = e.type, e) {
          case rt:
          case it:
          case ot:
          case ut:
          case lt:
            return e;
          default:
            switch (e = e && e.$$typeof, e) {
              case No:
              case at:
              case ct:
              case dt:
              case ft:
              case st:
                return e;
              default:
                return t;
            }
        }
      case Vt:
        return t;
    }
  }
}
M.ContextConsumer = at;
M.ContextProvider = st;
M.Element = Ht;
M.ForwardRef = ct;
M.Fragment = rt;
M.Lazy = dt;
M.Memo = ft;
M.Portal = Vt;
M.Profiler = it;
M.StrictMode = ot;
M.Suspense = ut;
M.SuspenseList = lt;
M.isAsyncMode = function() {
  return !1;
};
M.isConcurrentMode = function() {
  return !1;
};
M.isContextConsumer = function(e) {
  return Q(e) === at;
};
M.isContextProvider = function(e) {
  return Q(e) === st;
};
M.isElement = function(e) {
  return typeof e == "object" && e !== null && e.$$typeof === Ht;
};
M.isForwardRef = function(e) {
  return Q(e) === ct;
};
M.isFragment = function(e) {
  return Q(e) === rt;
};
M.isLazy = function(e) {
  return Q(e) === dt;
};
M.isMemo = function(e) {
  return Q(e) === ft;
};
M.isPortal = function(e) {
  return Q(e) === Vt;
};
M.isProfiler = function(e) {
  return Q(e) === it;
};
M.isStrictMode = function(e) {
  return Q(e) === ot;
};
M.isSuspense = function(e) {
  return Q(e) === ut;
};
M.isSuspenseList = function(e) {
  return Q(e) === lt;
};
M.isValidElementType = function(e) {
  return typeof e == "string" || typeof e == "function" || e === rt || e === it || e === ot || e === ut || e === lt || e === Bo || typeof e == "object" && e !== null && (e.$$typeof === dt || e.$$typeof === ft || e.$$typeof === st || e.$$typeof === at || e.$$typeof === ct || e.$$typeof === Fn || e.getModuleId !== void 0);
};
M.typeOf = Q;
Vn.exports = M;
var xt = Vn.exports, Ho = Symbol.for("react.element"), Vo = Symbol.for("react.transitional.element"), Fo = Symbol.for("react.fragment");
function zo(e) {
  return (
    // Base object type
    e && le(e) === "object" && // React Element type
    (e.$$typeof === Ho || e.$$typeof === Vo) && // React Fragment type
    e.type === Fo
  );
}
var Xo = Number(hr.split(".")[0]), Uo = function(t, n) {
  typeof t == "function" ? t(n) : le(t) === "object" && t && "current" in t && (t.current = n);
}, Wo = function(t) {
  var n, o;
  if (!t)
    return !1;
  if (zn(t) && Xo >= 19)
    return !0;
  var r = xt.isMemo(t) ? t.type.type : t.type;
  return !(typeof r == "function" && !((n = r.prototype) !== null && n !== void 0 && n.render) && r.$$typeof !== xt.ForwardRef || typeof t == "function" && !((o = t.prototype) !== null && o !== void 0 && o.render) && t.$$typeof !== xt.ForwardRef);
};
function zn(e) {
  return /* @__PURE__ */ gr(e) && !zo(e);
}
var Ko = function(t) {
  if (t && zn(t)) {
    var n = t;
    return n.props.propertyIsEnumerable("ref") ? n.props.ref : n.ref;
  }
  return null;
};
function Go(e, t) {
  for (var n = e, o = 0; o < t.length; o += 1) {
    if (n == null)
      return;
    n = n[t[o]];
  }
  return n;
}
function qo(e, t) {
  if (le(e) != "object" || !e) return e;
  var n = e[Symbol.toPrimitive];
  if (n !== void 0) {
    var o = n.call(e, t);
    if (le(o) != "object") return o;
    throw new TypeError("@@toPrimitive must return a primitive value.");
  }
  return (t === "string" ? String : Number)(e);
}
function Qo(e) {
  var t = qo(e, "string");
  return le(t) == "symbol" ? t : t + "";
}
function Yo(e, t, n) {
  return (t = Qo(t)) in e ? Object.defineProperty(e, t, {
    value: n,
    enumerable: !0,
    configurable: !0,
    writable: !0
  }) : e[t] = n, e;
}
function an(e, t) {
  var n = Object.keys(e);
  if (Object.getOwnPropertySymbols) {
    var o = Object.getOwnPropertySymbols(e);
    t && (o = o.filter(function(r) {
      return Object.getOwnPropertyDescriptor(e, r).enumerable;
    })), n.push.apply(n, o);
  }
  return n;
}
function Zo(e) {
  for (var t = 1; t < arguments.length; t++) {
    var n = arguments[t] != null ? arguments[t] : {};
    t % 2 ? an(Object(n), !0).forEach(function(o) {
      Yo(e, o, n[o]);
    }) : Object.getOwnPropertyDescriptors ? Object.defineProperties(e, Object.getOwnPropertyDescriptors(n)) : an(Object(n)).forEach(function(o) {
      Object.defineProperty(e, o, Object.getOwnPropertyDescriptor(n, o));
    });
  }
  return e;
}
function K(e) {
  "@babel/helpers - typeof";
  return K = typeof Symbol == "function" && typeof Symbol.iterator == "symbol" ? function(t) {
    return typeof t;
  } : function(t) {
    return t && typeof Symbol == "function" && t.constructor === Symbol && t !== Symbol.prototype ? "symbol" : typeof t;
  }, K(e);
}
function Jo(e, t) {
  if (K(e) != "object" || !e) return e;
  var n = e[Symbol.toPrimitive];
  if (n !== void 0) {
    var o = n.call(e, t);
    if (K(o) != "object") return o;
    throw new TypeError("@@toPrimitive must return a primitive value.");
  }
  return (t === "string" ? String : Number)(e);
}
function Xn(e) {
  var t = Jo(e, "string");
  return K(t) == "symbol" ? t : t + "";
}
function w(e, t, n) {
  return (t = Xn(t)) in e ? Object.defineProperty(e, t, {
    value: n,
    enumerable: !0,
    configurable: !0,
    writable: !0
  }) : e[t] = n, e;
}
function cn(e, t) {
  var n = Object.keys(e);
  if (Object.getOwnPropertySymbols) {
    var o = Object.getOwnPropertySymbols(e);
    t && (o = o.filter(function(r) {
      return Object.getOwnPropertyDescriptor(e, r).enumerable;
    })), n.push.apply(n, o);
  }
  return n;
}
function C(e) {
  for (var t = 1; t < arguments.length; t++) {
    var n = arguments[t] != null ? arguments[t] : {};
    t % 2 ? cn(Object(n), !0).forEach(function(o) {
      w(e, o, n[o]);
    }) : Object.getOwnPropertyDescriptors ? Object.defineProperties(e, Object.getOwnPropertyDescriptors(n)) : cn(Object(n)).forEach(function(o) {
      Object.defineProperty(e, o, Object.getOwnPropertyDescriptor(n, o));
    });
  }
  return e;
}
function ei(e) {
  if (Array.isArray(e)) return e;
}
function ti(e, t) {
  var n = e == null ? null : typeof Symbol < "u" && e[Symbol.iterator] || e["@@iterator"];
  if (n != null) {
    var o, r, i, s, a = [], u = !0, c = !1;
    try {
      if (i = (n = n.call(e)).next, t === 0) {
        if (Object(n) !== n) return;
        u = !1;
      } else for (; !(u = (o = i.call(n)).done) && (a.push(o.value), a.length !== t); u = !0) ;
    } catch (f) {
      c = !0, r = f;
    } finally {
      try {
        if (!u && n.return != null && (s = n.return(), Object(s) !== s)) return;
      } finally {
        if (c) throw r;
      }
    }
    return a;
  }
}
function un(e, t) {
  (t == null || t > e.length) && (t = e.length);
  for (var n = 0, o = Array(t); n < t; n++) o[n] = e[n];
  return o;
}
function ni(e, t) {
  if (e) {
    if (typeof e == "string") return un(e, t);
    var n = {}.toString.call(e).slice(8, -1);
    return n === "Object" && e.constructor && (n = e.constructor.name), n === "Map" || n === "Set" ? Array.from(e) : n === "Arguments" || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n) ? un(e, t) : void 0;
  }
}
function ri() {
  throw new TypeError(`Invalid attempt to destructure non-iterable instance.
In order to be iterable, non-array objects must have a [Symbol.iterator]() method.`);
}
function q(e, t) {
  return ei(e) || ti(e, t) || ni(e, t) || ri();
}
function ln(e) {
  return e instanceof HTMLElement || e instanceof SVGElement;
}
function oi(e) {
  return e && le(e) === "object" && ln(e.nativeElement) ? e.nativeElement : ln(e) ? e : null;
}
function ii(e) {
  var t = oi(e);
  if (t)
    return t;
  if (e instanceof b.Component) {
    var n;
    return (n = Ut.findDOMNode) === null || n === void 0 ? void 0 : n.call(Ut, e);
  }
  return null;
}
function si(e, t) {
  if (e == null) return {};
  var n = {};
  for (var o in e) if ({}.hasOwnProperty.call(e, o)) {
    if (t.indexOf(o) !== -1) continue;
    n[o] = e[o];
  }
  return n;
}
function fn(e, t) {
  if (e == null) return {};
  var n, o, r = si(e, t);
  if (Object.getOwnPropertySymbols) {
    var i = Object.getOwnPropertySymbols(e);
    for (o = 0; o < i.length; o++) n = i[o], t.indexOf(n) === -1 && {}.propertyIsEnumerable.call(e, n) && (r[n] = e[n]);
  }
  return r;
}
var ai = /* @__PURE__ */ h.createContext({});
function Te(e, t) {
  if (!(e instanceof t)) throw new TypeError("Cannot call a class as a function");
}
function dn(e, t) {
  for (var n = 0; n < t.length; n++) {
    var o = t[n];
    o.enumerable = o.enumerable || !1, o.configurable = !0, "value" in o && (o.writable = !0), Object.defineProperty(e, Xn(o.key), o);
  }
}
function Re(e, t, n) {
  return t && dn(e.prototype, t), n && dn(e, n), Object.defineProperty(e, "prototype", {
    writable: !1
  }), e;
}
function Lt(e, t) {
  return Lt = Object.setPrototypeOf ? Object.setPrototypeOf.bind() : function(n, o) {
    return n.__proto__ = o, n;
  }, Lt(e, t);
}
function pt(e, t) {
  if (typeof t != "function" && t !== null) throw new TypeError("Super expression must either be null or a function");
  e.prototype = Object.create(t && t.prototype, {
    constructor: {
      value: e,
      writable: !0,
      configurable: !0
    }
  }), Object.defineProperty(e, "prototype", {
    writable: !1
  }), t && Lt(e, t);
}
function Je(e) {
  return Je = Object.setPrototypeOf ? Object.getPrototypeOf.bind() : function(t) {
    return t.__proto__ || Object.getPrototypeOf(t);
  }, Je(e);
}
function Un() {
  try {
    var e = !Boolean.prototype.valueOf.call(Reflect.construct(Boolean, [], function() {
    }));
  } catch {
  }
  return (Un = function() {
    return !!e;
  })();
}
function ve(e) {
  if (e === void 0) throw new ReferenceError("this hasn't been initialised - super() hasn't been called");
  return e;
}
function ci(e, t) {
  if (t && (K(t) == "object" || typeof t == "function")) return t;
  if (t !== void 0) throw new TypeError("Derived constructors may only return object or undefined");
  return ve(e);
}
function mt(e) {
  var t = Un();
  return function() {
    var n, o = Je(e);
    if (t) {
      var r = Je(this).constructor;
      n = Reflect.construct(o, arguments, r);
    } else n = o.apply(this, arguments);
    return ci(this, n);
  };
}
var ui = /* @__PURE__ */ function(e) {
  pt(n, e);
  var t = mt(n);
  function n() {
    return Te(this, n), t.apply(this, arguments);
  }
  return Re(n, [{
    key: "render",
    value: function() {
      return this.props.children;
    }
  }]), n;
}(h.Component);
function li(e) {
  var t = h.useReducer(function(a) {
    return a + 1;
  }, 0), n = Ze(t, 2), o = n[1], r = h.useRef(e), i = ye(function() {
    return r.current;
  }), s = ye(function(a) {
    r.current = typeof a == "function" ? a(r.current) : a, o();
  });
  return [i, s];
}
var ue = "none", Ve = "appear", Fe = "enter", ze = "leave", pn = "none", J = "prepare", we = "start", _e = "active", Ft = "end", Wn = "prepared";
function mn(e, t) {
  var n = {};
  return n[e.toLowerCase()] = t.toLowerCase(), n["Webkit".concat(e)] = "webkit".concat(t), n["Moz".concat(e)] = "moz".concat(t), n["ms".concat(e)] = "MS".concat(t), n["O".concat(e)] = "o".concat(t.toLowerCase()), n;
}
function fi(e, t) {
  var n = {
    animationend: mn("Animation", "AnimationEnd"),
    transitionend: mn("Transition", "TransitionEnd")
  };
  return e && ("AnimationEvent" in t || delete n.animationend.animation, "TransitionEvent" in t || delete n.transitionend.transition), n;
}
var di = fi(nt(), typeof window < "u" ? window : {}), Kn = {};
if (nt()) {
  var pi = document.createElement("div");
  Kn = pi.style;
}
var Xe = {};
function Gn(e) {
  if (Xe[e])
    return Xe[e];
  var t = di[e];
  if (t)
    for (var n = Object.keys(t), o = n.length, r = 0; r < o; r += 1) {
      var i = n[r];
      if (Object.prototype.hasOwnProperty.call(t, i) && i in Kn)
        return Xe[e] = t[i], Xe[e];
    }
  return "";
}
var qn = Gn("animationend"), Qn = Gn("transitionend"), Yn = !!(qn && Qn), hn = qn || "animationend", gn = Qn || "transitionend";
function vn(e, t) {
  if (!e) return null;
  if (K(e) === "object") {
    var n = t.replace(/-\w/g, function(o) {
      return o[1].toUpperCase();
    });
    return e[n];
  }
  return "".concat(e, "-").concat(t);
}
const mi = function(e) {
  var t = ne();
  function n(r) {
    r && (r.removeEventListener(gn, e), r.removeEventListener(hn, e));
  }
  function o(r) {
    t.current && t.current !== r && n(t.current), r && r !== t.current && (r.addEventListener(gn, e), r.addEventListener(hn, e), t.current = r);
  }
  return h.useEffect(function() {
    return function() {
      n(t.current);
    };
  }, []), [o, n];
};
var Zn = nt() ? vr : ge, Jn = function(t) {
  return +setTimeout(t, 16);
}, er = function(t) {
  return clearTimeout(t);
};
typeof window < "u" && "requestAnimationFrame" in window && (Jn = function(t) {
  return window.requestAnimationFrame(t);
}, er = function(t) {
  return window.cancelAnimationFrame(t);
});
var yn = 0, zt = /* @__PURE__ */ new Map();
function tr(e) {
  zt.delete(e);
}
var kt = function(t) {
  var n = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : 1;
  yn += 1;
  var o = yn;
  function r(i) {
    if (i === 0)
      tr(o), t();
    else {
      var s = Jn(function() {
        r(i - 1);
      });
      zt.set(o, s);
    }
  }
  return r(n), o;
};
kt.cancel = function(e) {
  var t = zt.get(e);
  return tr(e), er(t);
};
const hi = function() {
  var e = h.useRef(null);
  function t() {
    kt.cancel(e.current);
  }
  function n(o) {
    var r = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : 2;
    t();
    var i = kt(function() {
      r <= 1 ? o({
        isCanceled: function() {
          return i !== e.current;
        }
      }) : n(o, r - 1);
    });
    e.current = i;
  }
  return h.useEffect(function() {
    return function() {
      t();
    };
  }, []), [n, t];
};
var gi = [J, we, _e, Ft], vi = [J, Wn], nr = !1, yi = !0;
function rr(e) {
  return e === _e || e === Ft;
}
const bi = function(e, t, n) {
  var o = De(pn), r = q(o, 2), i = r[0], s = r[1], a = hi(), u = q(a, 2), c = u[0], f = u[1];
  function l() {
    s(J, !0);
  }
  var d = t ? vi : gi;
  return Zn(function() {
    if (i !== pn && i !== Ft) {
      var p = d.indexOf(i), v = d[p + 1], g = n(i);
      g === nr ? s(v, !0) : v && c(function(m) {
        function x() {
          m.isCanceled() || s(v, !0);
        }
        g === !0 ? x() : Promise.resolve(g).then(x);
      });
    }
  }, [e, i]), h.useEffect(function() {
    return function() {
      f();
    };
  }, []), [l, i];
};
function Si(e, t, n, o) {
  var r = o.motionEnter, i = r === void 0 ? !0 : r, s = o.motionAppear, a = s === void 0 ? !0 : s, u = o.motionLeave, c = u === void 0 ? !0 : u, f = o.motionDeadline, l = o.motionLeaveImmediately, d = o.onAppearPrepare, p = o.onEnterPrepare, v = o.onLeavePrepare, g = o.onAppearStart, m = o.onEnterStart, x = o.onLeaveStart, E = o.onAppearActive, _ = o.onEnterActive, y = o.onLeaveActive, T = o.onAppearEnd, S = o.onEnterEnd, R = o.onLeaveEnd, P = o.onVisibleChanged, I = De(), $ = q(I, 2), D = $[0], A = $[1], L = li(ue), j = q(L, 2), O = j[0], V = j[1], G = De(null), N = q(G, 2), fe = N[0], be = N[1], U = O(), re = ne(!1), de = ne(null);
  function W() {
    return n();
  }
  var te = ne(!1);
  function Y() {
    V(ue), be(null, !0);
  }
  var Z = ye(function(F) {
    var B = O();
    if (B !== ue) {
      var z = W();
      if (!(F && !F.deadline && F.target !== z)) {
        var Ee = te.current, he;
        B === Ve && Ee ? he = T == null ? void 0 : T(z, F) : B === Fe && Ee ? he = S == null ? void 0 : S(z, F) : B === ze && Ee && (he = R == null ? void 0 : R(z, F)), Ee && he !== !1 && Y();
      }
    }
  }), pe = mi(Z), Se = q(pe, 1), me = Se[0], xe = function(B) {
    switch (B) {
      case Ve:
        return w(w(w({}, J, d), we, g), _e, E);
      case Fe:
        return w(w(w({}, J, p), we, m), _e, _);
      case ze:
        return w(w(w({}, J, v), we, x), _e, y);
      default:
        return {};
    }
  }, oe = h.useMemo(function() {
    return xe(U);
  }, [U]), Pe = bi(U, !e, function(F) {
    if (F === J) {
      var B = oe[J];
      return B ? B(W()) : nr;
    }
    if (ie in oe) {
      var z;
      be(((z = oe[ie]) === null || z === void 0 ? void 0 : z.call(oe, W(), null)) || null);
    }
    return ie === _e && U !== ue && (me(W()), f > 0 && (clearTimeout(de.current), de.current = setTimeout(function() {
      Z({
        deadline: !0
      });
    }, f))), ie === Wn && Y(), yi;
  }), Ne = q(Pe, 2), Oe = Ne[0], ie = Ne[1], Me = rr(ie);
  te.current = Me;
  var Be = ne(null);
  Zn(function() {
    if (!(re.current && Be.current === t)) {
      A(t);
      var F = re.current;
      re.current = !0;
      var B;
      !F && t && a && (B = Ve), F && t && i && (B = Fe), (F && !t && c || !F && l && !t && c) && (B = ze);
      var z = xe(B);
      B && (e || z[J]) ? (V(B), Oe()) : V(ue), Be.current = t;
    }
  }, [t]), ge(function() {
    // Cancel appear
    (U === Ve && !a || // Cancel enter
    U === Fe && !i || // Cancel leave
    U === ze && !c) && V(ue);
  }, [a, i, c]), ge(function() {
    return function() {
      re.current = !1, clearTimeout(de.current);
    };
  }, []);
  var Ae = h.useRef(!1);
  ge(function() {
    D && (Ae.current = !0), D !== void 0 && U === ue && ((Ae.current || D) && (P == null || P(D)), Ae.current = !0);
  }, [D, U]);
  var Ie = fe;
  return oe[J] && ie === we && (Ie = C({
    transition: "none"
  }, Ie)), [U, ie, Ie, D ?? t];
}
function xi(e) {
  var t = e;
  K(e) === "object" && (t = e.transitionSupport);
  function n(r, i) {
    return !!(r.motionName && t && i !== !1);
  }
  var o = /* @__PURE__ */ h.forwardRef(function(r, i) {
    var s = r.visible, a = s === void 0 ? !0 : s, u = r.removeOnLeave, c = u === void 0 ? !0 : u, f = r.forceRender, l = r.children, d = r.motionName, p = r.leavedClassName, v = r.eventProps, g = h.useContext(ai), m = g.motion, x = n(r, m), E = ne(), _ = ne();
    function y() {
      try {
        return E.current instanceof HTMLElement ? E.current : ii(_.current);
      } catch {
        return null;
      }
    }
    var T = Si(x, a, y, r), S = q(T, 4), R = S[0], P = S[1], I = S[2], $ = S[3], D = h.useRef($);
    $ && (D.current = !0);
    var A = h.useCallback(function(N) {
      E.current = N, Uo(i, N);
    }, [i]), L, j = C(C({}, v), {}, {
      visible: a
    });
    if (!l)
      L = null;
    else if (R === ue)
      $ ? L = l(C({}, j), A) : !c && D.current && p ? L = l(C(C({}, j), {}, {
        className: p
      }), A) : f || !c && !p ? L = l(C(C({}, j), {}, {
        style: {
          display: "none"
        }
      }), A) : L = null;
    else {
      var O;
      P === J ? O = "prepare" : rr(P) ? O = "active" : P === we && (O = "start");
      var V = vn(d, "".concat(R, "-").concat(O));
      L = l(C(C({}, j), {}, {
        className: ee(vn(d, R), w(w({}, V, V && O), d, typeof d == "string")),
        style: I
      }), A);
    }
    if (/* @__PURE__ */ h.isValidElement(L) && Wo(L)) {
      var G = Ko(L);
      G || (L = /* @__PURE__ */ h.cloneElement(L, {
        ref: A
      }));
    }
    return /* @__PURE__ */ h.createElement(ui, {
      ref: _
    }, L);
  });
  return o.displayName = "CSSMotion", o;
}
const or = xi(Yn);
var jt = "add", $t = "keep", Dt = "remove", Et = "removed";
function Ei(e) {
  var t;
  return e && K(e) === "object" && "key" in e ? t = e : t = {
    key: e
  }, C(C({}, t), {}, {
    key: String(t.key)
  });
}
function Nt() {
  var e = arguments.length > 0 && arguments[0] !== void 0 ? arguments[0] : [];
  return e.map(Ei);
}
function Ci() {
  var e = arguments.length > 0 && arguments[0] !== void 0 ? arguments[0] : [], t = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : [], n = [], o = 0, r = t.length, i = Nt(e), s = Nt(t);
  i.forEach(function(c) {
    for (var f = !1, l = o; l < r; l += 1) {
      var d = s[l];
      if (d.key === c.key) {
        o < l && (n = n.concat(s.slice(o, l).map(function(p) {
          return C(C({}, p), {}, {
            status: jt
          });
        })), o = l), n.push(C(C({}, d), {}, {
          status: $t
        })), o += 1, f = !0;
        break;
      }
    }
    f || n.push(C(C({}, c), {}, {
      status: Dt
    }));
  }), o < r && (n = n.concat(s.slice(o).map(function(c) {
    return C(C({}, c), {}, {
      status: jt
    });
  })));
  var a = {};
  n.forEach(function(c) {
    var f = c.key;
    a[f] = (a[f] || 0) + 1;
  });
  var u = Object.keys(a).filter(function(c) {
    return a[c] > 1;
  });
  return u.forEach(function(c) {
    n = n.filter(function(f) {
      var l = f.key, d = f.status;
      return l !== c || d !== Dt;
    }), n.forEach(function(f) {
      f.key === c && (f.status = $t);
    });
  }), n;
}
var wi = ["component", "children", "onVisibleChanged", "onAllRemoved"], _i = ["status"], Ti = ["eventProps", "visible", "children", "motionName", "motionAppear", "motionEnter", "motionLeave", "motionLeaveImmediately", "motionDeadline", "removeOnLeave", "leavedClassName", "onAppearPrepare", "onAppearStart", "onAppearActive", "onAppearEnd", "onEnterStart", "onEnterActive", "onEnterEnd", "onLeaveStart", "onLeaveActive", "onLeaveEnd"];
function Ri(e) {
  var t = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : or, n = /* @__PURE__ */ function(o) {
    pt(i, o);
    var r = mt(i);
    function i() {
      var s;
      Te(this, i);
      for (var a = arguments.length, u = new Array(a), c = 0; c < a; c++)
        u[c] = arguments[c];
      return s = r.call.apply(r, [this].concat(u)), w(ve(s), "state", {
        keyEntities: []
      }), w(ve(s), "removeKey", function(f) {
        s.setState(function(l) {
          var d = l.keyEntities.map(function(p) {
            return p.key !== f ? p : C(C({}, p), {}, {
              status: Et
            });
          });
          return {
            keyEntities: d
          };
        }, function() {
          var l = s.state.keyEntities, d = l.filter(function(p) {
            var v = p.status;
            return v !== Et;
          }).length;
          d === 0 && s.props.onAllRemoved && s.props.onAllRemoved();
        });
      }), s;
    }
    return Re(i, [{
      key: "render",
      value: function() {
        var a = this, u = this.state.keyEntities, c = this.props, f = c.component, l = c.children, d = c.onVisibleChanged;
        c.onAllRemoved;
        var p = fn(c, wi), v = f || h.Fragment, g = {};
        return Ti.forEach(function(m) {
          g[m] = p[m], delete p[m];
        }), delete p.keys, /* @__PURE__ */ h.createElement(v, p, u.map(function(m, x) {
          var E = m.status, _ = fn(m, _i), y = E === jt || E === $t;
          return /* @__PURE__ */ h.createElement(t, ae({}, g, {
            key: _.key,
            visible: y,
            eventProps: _,
            onVisibleChanged: function(S) {
              d == null || d(S, {
                key: _.key
              }), S || a.removeKey(_.key);
            }
          }), function(T, S) {
            return l(C(C({}, T), {}, {
              index: x
            }), S);
          });
        }));
      }
    }], [{
      key: "getDerivedStateFromProps",
      value: function(a, u) {
        var c = a.keys, f = u.keyEntities, l = Nt(c), d = Ci(f, l);
        return {
          keyEntities: d.filter(function(p) {
            var v = f.find(function(g) {
              var m = g.key;
              return p.key === m;
            });
            return !(v && v.status === Et && p.status === Dt);
          })
        };
      }
    }]), i;
  }(h.Component);
  return w(n, "defaultProps", {
    component: "div"
  }), n;
}
Ri(Yn);
var ir = /* @__PURE__ */ Re(function e() {
  Te(this, e);
}), sr = "CALC_UNIT", Pi = new RegExp(sr, "g");
function Ct(e) {
  return typeof e == "number" ? "".concat(e).concat(sr) : e;
}
var Oi = /* @__PURE__ */ function(e) {
  pt(n, e);
  var t = mt(n);
  function n(o, r) {
    var i;
    Te(this, n), i = t.call(this), w(ve(i), "result", ""), w(ve(i), "unitlessCssVar", void 0), w(ve(i), "lowPriority", void 0);
    var s = K(o);
    return i.unitlessCssVar = r, o instanceof n ? i.result = "(".concat(o.result, ")") : s === "number" ? i.result = Ct(o) : s === "string" && (i.result = o), i;
  }
  return Re(n, [{
    key: "add",
    value: function(r) {
      return r instanceof n ? this.result = "".concat(this.result, " + ").concat(r.getResult()) : (typeof r == "number" || typeof r == "string") && (this.result = "".concat(this.result, " + ").concat(Ct(r))), this.lowPriority = !0, this;
    }
  }, {
    key: "sub",
    value: function(r) {
      return r instanceof n ? this.result = "".concat(this.result, " - ").concat(r.getResult()) : (typeof r == "number" || typeof r == "string") && (this.result = "".concat(this.result, " - ").concat(Ct(r))), this.lowPriority = !0, this;
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
      var i = this, s = r || {}, a = s.unit, u = !0;
      return typeof a == "boolean" ? u = a : Array.from(this.unitlessCssVar).some(function(c) {
        return i.result.includes(c);
      }) && (u = !1), this.result = this.result.replace(Pi, u ? "px" : ""), typeof this.lowPriority < "u" ? "calc(".concat(this.result, ")") : this.result;
    }
  }]), n;
}(ir), Mi = /* @__PURE__ */ function(e) {
  pt(n, e);
  var t = mt(n);
  function n(o) {
    var r;
    return Te(this, n), r = t.call(this), w(ve(r), "result", 0), o instanceof n ? r.result = o.result : typeof o == "number" && (r.result = o), r;
  }
  return Re(n, [{
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
}(ir), Ai = function(t, n) {
  var o = t === "css" ? Oi : Mi;
  return function(r) {
    return new o(r, n);
  };
}, bn = function(t, n) {
  return "".concat([n, t.replace(/([A-Z]+)([A-Z][a-z]+)/g, "$1-$2").replace(/([a-z])([A-Z])/g, "$1-$2")].filter(Boolean).join("-"));
};
function Sn(e, t, n, o) {
  var r = C({}, t[e]);
  if (o != null && o.deprecatedTokens) {
    var i = o.deprecatedTokens;
    i.forEach(function(a) {
      var u = q(a, 2), c = u[0], f = u[1];
      if (r != null && r[c] || r != null && r[f]) {
        var l;
        (l = r[f]) !== null && l !== void 0 || (r[f] = r == null ? void 0 : r[c]);
      }
    });
  }
  var s = C(C({}, n), r);
  return Object.keys(s).forEach(function(a) {
    s[a] === t[a] && delete s[a];
  }), s;
}
var ar = typeof CSSINJS_STATISTIC < "u", Bt = !0;
function Xt() {
  for (var e = arguments.length, t = new Array(e), n = 0; n < e; n++)
    t[n] = arguments[n];
  if (!ar)
    return Object.assign.apply(Object, [{}].concat(t));
  Bt = !1;
  var o = {};
  return t.forEach(function(r) {
    if (K(r) === "object") {
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
  }), Bt = !0, o;
}
var xn = {};
function Ii() {
}
var Li = function(t) {
  var n, o = t, r = Ii;
  return ar && typeof Proxy < "u" && (n = /* @__PURE__ */ new Set(), o = new Proxy(t, {
    get: function(s, a) {
      if (Bt) {
        var u;
        (u = n) === null || u === void 0 || u.add(a);
      }
      return s[a];
    }
  }), r = function(s, a) {
    var u;
    xn[s] = {
      global: Array.from(n),
      component: C(C({}, (u = xn[s]) === null || u === void 0 ? void 0 : u.component), a)
    };
  }), {
    token: o,
    keys: n,
    flush: r
  };
};
function En(e, t, n) {
  if (typeof n == "function") {
    var o;
    return n(Xt(t, (o = t[e]) !== null && o !== void 0 ? o : {}));
  }
  return n ?? {};
}
function ki(e) {
  return e === "js" ? {
    max: Math.max,
    min: Math.min
  } : {
    max: function() {
      for (var n = arguments.length, o = new Array(n), r = 0; r < n; r++)
        o[r] = arguments[r];
      return "max(".concat(o.map(function(i) {
        return Ot(i);
      }).join(","), ")");
    },
    min: function() {
      for (var n = arguments.length, o = new Array(n), r = 0; r < n; r++)
        o[r] = arguments[r];
      return "min(".concat(o.map(function(i) {
        return Ot(i);
      }).join(","), ")");
    }
  };
}
var ji = 1e3 * 60 * 10, $i = /* @__PURE__ */ function() {
  function e() {
    Te(this, e), w(this, "map", /* @__PURE__ */ new Map()), w(this, "objectIDMap", /* @__PURE__ */ new WeakMap()), w(this, "nextID", 0), w(this, "lastAccessBeat", /* @__PURE__ */ new Map()), w(this, "accessBeat", 0);
  }
  return Re(e, [{
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
        return i && K(i) === "object" ? "obj_".concat(o.getObjectID(i)) : "".concat(K(i), "_").concat(i);
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
          o - r > ji && (n.map.delete(i), n.lastAccessBeat.delete(i));
        }), this.accessBeat = 0;
      }
    }
  }]), e;
}(), Cn = new $i();
function Di(e, t) {
  return b.useMemo(function() {
    var n = Cn.get(t);
    if (n)
      return n;
    var o = e();
    return Cn.set(t, o), o;
  }, t);
}
var Ni = function() {
  return {};
};
function Bi(e) {
  var t = e.useCSP, n = t === void 0 ? Ni : t, o = e.useToken, r = e.usePrefix, i = e.getResetStyles, s = e.getCommonStyle, a = e.getCompUnitless;
  function u(d, p, v, g) {
    var m = Array.isArray(d) ? d[0] : d;
    function x(P) {
      return "".concat(String(m)).concat(P.slice(0, 1).toUpperCase()).concat(P.slice(1));
    }
    var E = (g == null ? void 0 : g.unitless) || {}, _ = typeof a == "function" ? a(d) : {}, y = C(C({}, _), {}, w({}, x("zIndexPopup"), !0));
    Object.keys(E).forEach(function(P) {
      y[x(P)] = E[P];
    });
    var T = C(C({}, g), {}, {
      unitless: y,
      prefixToken: x
    }), S = f(d, p, v, T), R = c(m, v, T);
    return function(P) {
      var I = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : P, $ = S(P, I), D = q($, 2), A = D[1], L = R(I), j = q(L, 2), O = j[0], V = j[1];
      return [O, A, V];
    };
  }
  function c(d, p, v) {
    var g = v.unitless, m = v.injectStyle, x = m === void 0 ? !0 : m, E = v.prefixToken, _ = v.ignore, y = function(R) {
      var P = R.rootCls, I = R.cssVar, $ = I === void 0 ? {} : I, D = o(), A = D.realToken;
      return $r({
        path: [d],
        prefix: $.prefix,
        key: $.key,
        unitless: g,
        ignore: _,
        token: A,
        scope: P
      }, function() {
        var L = En(d, A, p), j = Sn(d, A, L, {
          deprecatedTokens: v == null ? void 0 : v.deprecatedTokens
        });
        return Object.keys(L).forEach(function(O) {
          j[E(O)] = j[O], delete j[O];
        }), j;
      }), null;
    }, T = function(R) {
      var P = o(), I = P.cssVar;
      return [function($) {
        return x && I ? /* @__PURE__ */ b.createElement(b.Fragment, null, /* @__PURE__ */ b.createElement(y, {
          rootCls: R,
          cssVar: I,
          component: d
        }), $) : $;
      }, I == null ? void 0 : I.key];
    };
    return T;
  }
  function f(d, p, v) {
    var g = arguments.length > 3 && arguments[3] !== void 0 ? arguments[3] : {}, m = Array.isArray(d) ? d : [d, d], x = q(m, 1), E = x[0], _ = m.join("-"), y = e.layer || {
      name: "antd"
    };
    return function(T) {
      var S = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : T, R = o(), P = R.theme, I = R.realToken, $ = R.hashId, D = R.token, A = R.cssVar, L = r(), j = L.rootPrefixCls, O = L.iconPrefixCls, V = n(), G = A ? "css" : "js", N = Di(function() {
        var W = /* @__PURE__ */ new Set();
        return A && Object.keys(g.unitless || {}).forEach(function(te) {
          W.add(vt(te, A.prefix)), W.add(vt(te, bn(E, A.prefix)));
        }), Ai(G, W);
      }, [G, E, A == null ? void 0 : A.prefix]), fe = ki(G), be = fe.max, U = fe.min, re = {
        theme: P,
        token: D,
        hashId: $,
        nonce: function() {
          return V.nonce;
        },
        clientOnly: g.clientOnly,
        layer: y,
        // antd is always at top of styles
        order: g.order || -999
      };
      typeof i == "function" && Wt(C(C({}, re), {}, {
        clientOnly: !1,
        path: ["Shared", j]
      }), function() {
        return i(D, {
          prefix: {
            rootPrefixCls: j,
            iconPrefixCls: O
          },
          csp: V
        });
      });
      var de = Wt(C(C({}, re), {}, {
        path: [_, T, O]
      }), function() {
        if (g.injectStyle === !1)
          return [];
        var W = Li(D), te = W.token, Y = W.flush, Z = En(E, I, v), pe = ".".concat(T), Se = Sn(E, I, Z, {
          deprecatedTokens: g.deprecatedTokens
        });
        A && Z && K(Z) === "object" && Object.keys(Z).forEach(function(Pe) {
          Z[Pe] = "var(".concat(vt(Pe, bn(E, A.prefix)), ")");
        });
        var me = Xt(te, {
          componentCls: pe,
          prefixCls: T,
          iconCls: ".".concat(O),
          antCls: ".".concat(j),
          calc: N,
          // @ts-ignore
          max: be,
          // @ts-ignore
          min: U
        }, A ? Z : Se), xe = p(me, {
          hashId: $,
          prefixCls: T,
          rootPrefixCls: j,
          iconPrefixCls: O
        });
        Y(E, Se);
        var oe = typeof s == "function" ? s(me, T, S, g.resetFont) : null;
        return [g.resetStyle === !1 ? null : oe, xe];
      });
      return [de, $];
    };
  }
  function l(d, p, v) {
    var g = arguments.length > 3 && arguments[3] !== void 0 ? arguments[3] : {}, m = f(d, p, v, C({
      resetStyle: !1,
      // Sub Style should default after root one
      order: -998
    }, g)), x = function(_) {
      var y = _.prefixCls, T = _.rootCls, S = T === void 0 ? y : T;
      return m(y, S), null;
    };
    return x;
  }
  return {
    genStyleHooks: u,
    genSubStyleComponent: l,
    genComponentStyleHook: f
  };
}
const H = Math.round;
function wt(e, t) {
  const n = e.replace(/^[^(]*\((.*)/, "$1").replace(/\).*/, "").match(/\d*\.?\d+%?/g) || [], o = n.map((r) => parseFloat(r));
  for (let r = 0; r < 3; r += 1)
    o[r] = t(o[r] || 0, n[r] || "", r);
  return n[3] ? o[3] = n[3].includes("%") ? o[3] / 100 : o[3] : o[3] = 1, o;
}
const wn = (e, t, n) => n === 0 ? e : e / 100;
function ke(e, t) {
  const n = t || 255;
  return e > n ? n : e < 0 ? 0 : e;
}
class se {
  constructor(t) {
    w(this, "isValid", !0), w(this, "r", 0), w(this, "g", 0), w(this, "b", 0), w(this, "a", 1), w(this, "_h", void 0), w(this, "_s", void 0), w(this, "_l", void 0), w(this, "_v", void 0), w(this, "_max", void 0), w(this, "_min", void 0), w(this, "_brightness", void 0);
    function n(o) {
      return o[0] in t && o[1] in t && o[2] in t;
    }
    if (t) if (typeof t == "string") {
      let r = function(i) {
        return o.startsWith(i);
      };
      const o = t.trim();
      /^#?[A-F\d]{3,8}$/i.test(o) ? this.fromHexString(o) : r("rgb") ? this.fromRgbString(o) : r("hsl") ? this.fromHslString(o) : (r("hsv") || r("hsb")) && this.fromHsvString(o);
    } else if (t instanceof se)
      this.r = t.r, this.g = t.g, this.b = t.b, this.a = t.a, this._h = t._h, this._s = t._s, this._l = t._l, this._v = t._v;
    else if (n("rgb"))
      this.r = ke(t.r), this.g = ke(t.g), this.b = ke(t.b), this.a = typeof t.a == "number" ? ke(t.a, 1) : 1;
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
    function t(i) {
      const s = i / 255;
      return s <= 0.03928 ? s / 12.92 : Math.pow((s + 0.055) / 1.055, 2.4);
    }
    const n = t(this.r), o = t(this.g), r = t(this.b);
    return 0.2126 * n + 0.7152 * o + 0.0722 * r;
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
    const o = this._c(t), r = n / 100, i = (a) => (o[a] - this[a]) * r + this[a], s = {
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
    const n = this._c(t), o = this.a + n.a * (1 - this.a), r = (i) => H((this[i] * this.a + n[i] * n.a * (1 - this.a)) / o);
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
    const t = this.getHue(), n = H(this.getSaturation() * 100), o = H(this.getLightness() * 100);
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
    return r[t] = ke(n, o), r;
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
    function o(r, i) {
      return parseInt(n[r] + n[i || r], 16);
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
      const d = H(o * 255);
      this.r = d, this.g = d, this.b = d;
    }
    let i = 0, s = 0, a = 0;
    const u = t / 60, c = (1 - Math.abs(2 * o - 1)) * n, f = c * (1 - Math.abs(u % 2 - 1));
    u >= 0 && u < 1 ? (i = c, s = f) : u >= 1 && u < 2 ? (i = f, s = c) : u >= 2 && u < 3 ? (s = c, a = f) : u >= 3 && u < 4 ? (s = f, a = c) : u >= 4 && u < 5 ? (i = f, a = c) : u >= 5 && u < 6 && (i = c, a = f);
    const l = o - c / 2;
    this.r = H((i + l) * 255), this.g = H((s + l) * 255), this.b = H((a + l) * 255);
  }
  fromHsv({
    h: t,
    s: n,
    v: o,
    a: r
  }) {
    this._h = t % 360, this._s = n, this._v = o, this.a = typeof r == "number" ? r : 1;
    const i = H(o * 255);
    if (this.r = i, this.g = i, this.b = i, n <= 0)
      return;
    const s = t / 60, a = Math.floor(s), u = s - a, c = H(o * (1 - n) * 255), f = H(o * (1 - n * u) * 255), l = H(o * (1 - n * (1 - u)) * 255);
    switch (a) {
      case 0:
        this.g = l, this.b = c;
        break;
      case 1:
        this.r = f, this.b = c;
        break;
      case 2:
        this.r = c, this.b = l;
        break;
      case 3:
        this.r = c, this.g = f;
        break;
      case 4:
        this.r = l, this.g = c;
        break;
      case 5:
      default:
        this.g = c, this.b = f;
        break;
    }
  }
  fromHsvString(t) {
    const n = wt(t, wn);
    this.fromHsv({
      h: n[0],
      s: n[1],
      v: n[2],
      a: n[3]
    });
  }
  fromHslString(t) {
    const n = wt(t, wn);
    this.fromHsl({
      h: n[0],
      s: n[1],
      l: n[2],
      a: n[3]
    });
  }
  fromRgbString(t) {
    const n = wt(t, (o, r) => (
      // Convert percentage to number. e.g. 50% -> 128
      r.includes("%") ? H(o / 100 * 255) : o
    ));
    this.r = n[0], this.g = n[1], this.b = n[2], this.a = n[3];
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
}, Vi = Object.assign(Object.assign({}, Hi), {
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
function _t(e) {
  return e >= 0 && e <= 255;
}
function Ue(e, t) {
  const {
    r: n,
    g: o,
    b: r,
    a: i
  } = new se(e).toRgb();
  if (i < 1)
    return e;
  const {
    r: s,
    g: a,
    b: u
  } = new se(t).toRgb();
  for (let c = 0.01; c <= 1; c += 0.01) {
    const f = Math.round((n - s * (1 - c)) / c), l = Math.round((o - a * (1 - c)) / c), d = Math.round((r - u * (1 - c)) / c);
    if (_t(f) && _t(l) && _t(d))
      return new se({
        r: f,
        g: l,
        b: d,
        a: Math.round(c * 100) / 100
      }).toRgbString();
  }
  return new se({
    r: n,
    g: o,
    b: r,
    a: 1
  }).toRgbString();
}
var Fi = function(e, t) {
  var n = {};
  for (var o in e) Object.prototype.hasOwnProperty.call(e, o) && t.indexOf(o) < 0 && (n[o] = e[o]);
  if (e != null && typeof Object.getOwnPropertySymbols == "function") for (var r = 0, o = Object.getOwnPropertySymbols(e); r < o.length; r++)
    t.indexOf(o[r]) < 0 && Object.prototype.propertyIsEnumerable.call(e, o[r]) && (n[o[r]] = e[o[r]]);
  return n;
};
function zi(e) {
  const {
    override: t
  } = e, n = Fi(e, ["override"]), o = Object.assign({}, t);
  Object.keys(Vi).forEach((d) => {
    delete o[d];
  });
  const r = Object.assign(Object.assign({}, n), o), i = 480, s = 576, a = 768, u = 992, c = 1200, f = 1600;
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
    colorSplit: Ue(r.colorBorderSecondary, r.colorBgContainer),
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
    colorErrorOutline: Ue(r.colorErrorBg, r.colorBgContainer),
    colorWarningOutline: Ue(r.colorWarningBg, r.colorBgContainer),
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
    controlOutline: Ue(r.colorPrimaryBg, r.colorBgContainer),
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
    screenMDMax: u - 1,
    screenLG: u,
    screenLGMin: u,
    screenLGMax: c - 1,
    screenXL: c,
    screenXLMin: c,
    screenXLMax: f - 1,
    screenXXL: f,
    screenXXLMin: f,
    boxShadowPopoverArrow: "2px 2px 5px rgba(0, 0, 0, 0.05)",
    boxShadowCard: `
      0 1px 2px -2px ${new se("rgba(0, 0, 0, 0.16)").toRgbString()},
      0 3px 6px 0 ${new se("rgba(0, 0, 0, 0.12)").toRgbString()},
      0 5px 12px 4px ${new se("rgba(0, 0, 0, 0.09)").toRgbString()}
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
}, Ui = {
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
}, Wi = Dr(Pt.defaultAlgorithm), Ki = {
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
}, cr = (e, t, n) => {
  const o = n.getDerivativeToken(e), {
    override: r,
    ...i
  } = t;
  let s = {
    ...o,
    override: r
  };
  return s = zi(s), i && Object.entries(i).forEach(([a, u]) => {
    const {
      theme: c,
      ...f
    } = u;
    let l = f;
    c && (l = cr({
      ...s,
      ...f
    }, {
      override: f
    }, c)), s[a] = l;
  }), s;
};
function Gi() {
  const {
    token: e,
    hashed: t,
    theme: n = Wi,
    override: o,
    cssVar: r
  } = b.useContext(Pt._internalContext), [i, s, a] = Nr(n, [Pt.defaultSeed, e], {
    salt: `${Oo}-${t || ""}`,
    override: o,
    getComputedToken: cr,
    cssVar: r && {
      prefix: r.prefix,
      key: r.key,
      unitless: Xi,
      ignore: Ui,
      preserve: Ki
    }
  });
  return [n, a, t ? s : "", i, r];
}
const {
  genStyleHooks: qi
} = Bi({
  usePrefix: () => {
    const {
      getPrefixCls: e,
      iconPrefixCls: t
    } = It();
    return {
      iconPrefixCls: t,
      rootPrefixCls: e()
    };
  },
  useToken: () => {
    const [e, t, n, o, r] = Gi();
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
    } = It();
    return e ?? {};
  },
  layer: {
    name: "antdx",
    dependencies: ["antd"]
  }
});
var Qi = `accept acceptCharset accessKey action allowFullScreen allowTransparency
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
    summary tabIndex target title type useMap value width wmode wrap`, Yi = `onCopy onCut onPaste onCompositionEnd onCompositionStart onCompositionUpdate onKeyDown
    onKeyPress onKeyUp onFocus onBlur onChange onInput onSubmit onClick onContextMenu onDoubleClick
    onDrag onDragEnd onDragEnter onDragExit onDragLeave onDragOver onDragStart onDrop onMouseDown
    onMouseEnter onMouseLeave onMouseMove onMouseOut onMouseOver onMouseUp onSelect onTouchCancel
    onTouchEnd onTouchMove onTouchStart onScroll onWheel onAbort onCanPlay onCanPlayThrough
    onDurationChange onEmptied onEncrypted onEnded onError onLoadedData onLoadedMetadata
    onLoadStart onPause onPlay onPlaying onProgress onRateChange onSeeked onSeeking onStalled onSuspend onTimeUpdate onVolumeChange onWaiting onLoad onError`, Zi = "".concat(Qi, " ").concat(Yi).split(/[\s\n]+/), Ji = "aria-", es = "data-";
function _n(e, t) {
  return e.indexOf(t) === 0;
}
function ts(e) {
  var t = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : !1, n;
  t === !1 ? n = {
    aria: !0,
    data: !0,
    attr: !0
  } : t === !0 ? n = {
    aria: !0
  } : n = Zo({}, t);
  var o = {};
  return Object.keys(e).forEach(function(r) {
    // Aria
    (n.aria && (r === "role" || _n(r, Ji)) || // Data
    n.data && _n(r, es) || // Attr
    n.attr && Zi.includes(r)) && (o[r] = e[r]);
  }), o;
}
function ns(e, t) {
  return yr(e, () => {
    const n = t(), {
      nativeElement: o
    } = n;
    return new Proxy(o, {
      get(r, i) {
        return n[i] ? n[i] : Reflect.get(r, i);
      }
    });
  });
}
const ur = /* @__PURE__ */ h.createContext({}), Tn = () => ({
  height: 0
}), Rn = (e) => ({
  height: e.scrollHeight
});
function rs(e) {
  const {
    title: t,
    onOpenChange: n,
    open: o,
    children: r,
    className: i,
    style: s,
    classNames: a = {},
    styles: u = {},
    closable: c,
    forceRender: f
  } = e, {
    prefixCls: l
  } = h.useContext(ur), d = `${l}-header`;
  return /* @__PURE__ */ h.createElement(or, {
    motionEnter: !0,
    motionLeave: !0,
    motionName: `${d}-motion`,
    leavedClassName: `${d}-motion-hidden`,
    onEnterStart: Tn,
    onEnterActive: Rn,
    onLeaveStart: Rn,
    onLeaveActive: Tn,
    visible: o,
    forceRender: f
  }, ({
    className: p,
    style: v
  }) => /* @__PURE__ */ h.createElement("div", {
    className: ee(d, p, i),
    style: {
      ...v,
      ...s
    }
  }, (c !== !1 || t) && /* @__PURE__ */ h.createElement("div", {
    className: (
      // We follow antd naming standard here.
      // So the header part is use `-header` suffix.
      // Though its little bit weird for double `-header`.
      ee(`${d}-header`, a.header)
    ),
    style: {
      ...u.header
    }
  }, /* @__PURE__ */ h.createElement("div", {
    className: `${d}-title`
  }, t), c !== !1 && /* @__PURE__ */ h.createElement("div", {
    className: `${d}-close`
  }, /* @__PURE__ */ h.createElement(Ln, {
    type: "text",
    icon: /* @__PURE__ */ h.createElement(Ar, null),
    size: "small",
    onClick: () => {
      n == null || n(!o);
    }
  }))), r && /* @__PURE__ */ h.createElement("div", {
    className: ee(`${d}-content`, a.content),
    style: {
      ...u.content
    }
  }, r)));
}
const ht = /* @__PURE__ */ h.createContext(null);
function os(e, t) {
  const {
    className: n,
    action: o,
    onClick: r,
    ...i
  } = e, s = h.useContext(ht), {
    prefixCls: a,
    disabled: u
  } = s, c = i.disabled ?? u ?? s[`${o}Disabled`];
  return /* @__PURE__ */ h.createElement(Ln, ae({
    type: "text"
  }, i, {
    ref: t,
    onClick: (f) => {
      var l;
      c || ((l = s[o]) == null || l.call(s), r == null || r(f));
    },
    className: ee(a, n, {
      [`${a}-disabled`]: c
    })
  }));
}
const gt = /* @__PURE__ */ h.forwardRef(os);
function is(e, t) {
  return /* @__PURE__ */ h.createElement(gt, ae({
    icon: /* @__PURE__ */ h.createElement(Ir, null)
  }, e, {
    action: "onClear",
    ref: t
  }));
}
const ss = /* @__PURE__ */ h.forwardRef(is), as = /* @__PURE__ */ br((e) => {
  const {
    className: t
  } = e;
  return /* @__PURE__ */ b.createElement("svg", {
    color: "currentColor",
    viewBox: "0 0 1000 1000",
    xmlns: "http://www.w3.org/2000/svg",
    className: t
  }, /* @__PURE__ */ b.createElement("title", null, "Stop Loading"), /* @__PURE__ */ b.createElement("rect", {
    fill: "currentColor",
    height: "250",
    rx: "24",
    ry: "24",
    width: "250",
    x: "375",
    y: "375"
  }), /* @__PURE__ */ b.createElement("circle", {
    cx: "500",
    cy: "500",
    fill: "none",
    r: "450",
    stroke: "currentColor",
    strokeWidth: "100",
    opacity: "0.45"
  }), /* @__PURE__ */ b.createElement("circle", {
    cx: "500",
    cy: "500",
    fill: "none",
    r: "450",
    stroke: "currentColor",
    strokeWidth: "100",
    strokeDasharray: "600 9999999"
  }, /* @__PURE__ */ b.createElement("animateTransform", {
    attributeName: "transform",
    dur: "1s",
    from: "0 500 500",
    repeatCount: "indefinite",
    to: "360 500 500",
    type: "rotate"
  })));
});
function cs(e, t) {
  const {
    prefixCls: n
  } = h.useContext(ht), {
    className: o
  } = e;
  return /* @__PURE__ */ h.createElement(gt, ae({
    icon: null,
    color: "primary",
    variant: "text",
    shape: "circle"
  }, e, {
    className: ee(o, `${n}-loading-button`),
    action: "onCancel",
    ref: t
  }), /* @__PURE__ */ h.createElement(as, {
    className: `${n}-loading-icon`
  }));
}
const lr = /* @__PURE__ */ h.forwardRef(cs);
function us(e, t) {
  return /* @__PURE__ */ h.createElement(gt, ae({
    icon: /* @__PURE__ */ h.createElement(Lr, null),
    type: "primary",
    shape: "circle"
  }, e, {
    action: "onSend",
    ref: t
  }));
}
const fr = /* @__PURE__ */ h.forwardRef(us), je = 1e3, $e = 4, Ye = 140, Pn = Ye / 2, We = 250, On = 500, Ke = 0.8;
function ls({
  className: e
}) {
  return /* @__PURE__ */ b.createElement("svg", {
    color: "currentColor",
    viewBox: `0 0 ${je} ${je}`,
    xmlns: "http://www.w3.org/2000/svg",
    className: e
  }, /* @__PURE__ */ b.createElement("title", null, "Speech Recording"), Array.from({
    length: $e
  }).map((t, n) => {
    const o = (je - Ye * $e) / ($e - 1), r = n * (o + Ye), i = je / 2 - We / 2, s = je / 2 - On / 2;
    return /* @__PURE__ */ b.createElement("rect", {
      fill: "currentColor",
      rx: Pn,
      ry: Pn,
      height: We,
      width: Ye,
      x: r,
      y: i,
      key: n
    }, /* @__PURE__ */ b.createElement("animate", {
      attributeName: "height",
      values: `${We}; ${On}; ${We}`,
      keyTimes: "0; 0.5; 1",
      dur: `${Ke}s`,
      begin: `${Ke / $e * n}s`,
      repeatCount: "indefinite"
    }), /* @__PURE__ */ b.createElement("animate", {
      attributeName: "y",
      values: `${i}; ${s}; ${i}`,
      keyTimes: "0; 0.5; 1",
      dur: `${Ke}s`,
      begin: `${Ke / $e * n}s`,
      repeatCount: "indefinite"
    }));
  }));
}
function fs(e, t) {
  const {
    speechRecording: n,
    onSpeechDisabled: o,
    prefixCls: r
  } = h.useContext(ht);
  let i = null;
  return n ? i = /* @__PURE__ */ h.createElement(ls, {
    className: `${r}-recording-icon`
  }) : o ? i = /* @__PURE__ */ h.createElement(kr, null) : i = /* @__PURE__ */ h.createElement(jr, null), /* @__PURE__ */ h.createElement(gt, ae({
    icon: i,
    color: "primary",
    variant: "text"
  }, e, {
    action: "onSpeech",
    ref: t
  }));
}
const dr = /* @__PURE__ */ h.forwardRef(fs), ds = (e) => {
  const {
    componentCls: t,
    calc: n
  } = e, o = `${t}-header`;
  return {
    [t]: {
      [o]: {
        borderBottomWidth: e.lineWidth,
        borderBottomStyle: "solid",
        borderBottomColor: e.colorBorder,
        // ======================== Header ========================
        "&-header": {
          background: e.colorFillAlter,
          fontSize: e.fontSize,
          lineHeight: e.lineHeight,
          paddingBlock: n(e.paddingSM).sub(e.lineWidthBold).equal(),
          paddingInlineStart: e.padding,
          paddingInlineEnd: e.paddingXS,
          display: "flex",
          borderRadius: {
            _skip_check_: !0,
            value: n(e.borderRadius).mul(2).equal()
          },
          borderEndStartRadius: 0,
          borderEndEndRadius: 0,
          [`${o}-title`]: {
            flex: "auto"
          }
        },
        // ======================= Content ========================
        "&-content": {
          padding: e.padding
        },
        // ======================== Motion ========================
        "&-motion": {
          transition: ["height", "border"].map((r) => `${r} ${e.motionDurationSlow}`).join(","),
          overflow: "hidden",
          "&-enter-start, &-leave-active": {
            borderBottomColor: "transparent"
          },
          "&-hidden": {
            display: "none"
          }
        }
      }
    }
  };
}, ps = (e) => {
  const {
    componentCls: t,
    padding: n,
    paddingSM: o,
    paddingXS: r,
    paddingXXS: i,
    lineWidth: s,
    lineWidthBold: a,
    calc: u
  } = e;
  return {
    [t]: {
      position: "relative",
      width: "100%",
      boxSizing: "border-box",
      boxShadow: `${e.boxShadowTertiary}`,
      transition: `background ${e.motionDurationSlow}`,
      // Border
      borderRadius: {
        _skip_check_: !0,
        value: u(e.borderRadius).mul(2).equal()
      },
      borderColor: e.colorBorder,
      borderWidth: 0,
      borderStyle: "solid",
      // Border
      "&:after": {
        content: '""',
        position: "absolute",
        inset: 0,
        pointerEvents: "none",
        transition: `border-color ${e.motionDurationSlow}`,
        borderRadius: {
          _skip_check_: !0,
          value: "inherit"
        },
        borderStyle: "inherit",
        borderColor: "inherit",
        borderWidth: s
      },
      // Focus
      "&:focus-within": {
        boxShadow: `${e.boxShadowSecondary}`,
        borderColor: e.colorPrimary,
        "&:after": {
          borderWidth: a
        }
      },
      "&-disabled": {
        background: e.colorBgContainerDisabled
      },
      // ============================== RTL ==============================
      [`&${t}-rtl`]: {
        direction: "rtl"
      },
      // ============================ Content ============================
      [`${t}-content`]: {
        display: "flex",
        gap: r,
        width: "100%",
        paddingBlock: o,
        paddingInlineStart: n,
        paddingInlineEnd: o,
        boxSizing: "border-box",
        alignItems: "flex-end"
      },
      // ============================ Prefix =============================
      [`${t}-prefix`]: {
        flex: "none"
      },
      // ============================= Input =============================
      [`${t}-input`]: {
        padding: 0,
        borderRadius: 0,
        flex: "auto",
        alignSelf: "center",
        minHeight: "auto"
      },
      // ============================ Actions ============================
      [`${t}-actions-list`]: {
        flex: "none",
        display: "flex",
        "&-presets": {
          gap: e.paddingXS
        }
      },
      [`${t}-actions-btn`]: {
        "&-disabled": {
          opacity: 0.45
        },
        "&-loading-button": {
          padding: 0,
          border: 0
        },
        "&-loading-icon": {
          height: e.controlHeight,
          width: e.controlHeight,
          verticalAlign: "top"
        },
        "&-recording-icon": {
          height: "1.2em",
          width: "1.2em",
          verticalAlign: "top"
        }
      },
      // ============================ Footer =============================
      [`${t}-footer`]: {
        paddingInlineStart: n,
        paddingInlineEnd: o,
        paddingBlockEnd: o,
        paddingBlockStart: i,
        boxSizing: "border-box"
      }
    }
  };
}, ms = () => ({}), hs = qi("Sender", (e) => {
  const {
    paddingXS: t,
    calc: n
  } = e, o = Xt(e, {
    SenderContentMaxWidth: `calc(100% - ${Ot(n(t).add(32).equal())})`
  });
  return [ps(o), ds(o)];
}, ms);
let et;
!et && typeof window < "u" && (et = window.SpeechRecognition || window.webkitSpeechRecognition);
function gs(e, t) {
  const n = ye(e), [o, r, i] = b.useMemo(() => typeof t == "object" ? [t.recording, t.onRecordingChange, typeof t.recording == "boolean"] : [void 0, void 0, !1], [t]), [s, a] = b.useState(null);
  b.useEffect(() => {
    if (typeof navigator < "u" && "permissions" in navigator) {
      let g = null;
      return navigator.permissions.query({
        name: "microphone"
      }).then((m) => {
        a(m.state), m.onchange = function() {
          a(this.state);
        }, g = m;
      }), () => {
        g && (g.onchange = null);
      };
    }
  }, []);
  const u = et && s !== "denied", c = b.useRef(null), [f, l] = Hn(!1, {
    value: o
  }), d = b.useRef(!1), p = () => {
    if (u && !c.current) {
      const g = new et();
      g.onstart = () => {
        l(!0);
      }, g.onend = () => {
        l(!1);
      }, g.onresult = (m) => {
        var x, E, _;
        if (!d.current) {
          const y = (_ = (E = (x = m.results) == null ? void 0 : x[0]) == null ? void 0 : E[0]) == null ? void 0 : _.transcript;
          n(y);
        }
        d.current = !1;
      }, c.current = g;
    }
  }, v = ye((g) => {
    g && !f || (d.current = g, i ? r == null || r(!f) : (p(), c.current && (f ? (c.current.stop(), r == null || r(!1)) : (c.current.start(), r == null || r(!0)))));
  });
  return [u, v, f];
}
function vs(e, t, n) {
  return Go(e, t) || n;
}
const Mn = {
  SendButton: fr,
  ClearButton: ss,
  LoadingButton: lr,
  SpeechButton: dr
}, ys = /* @__PURE__ */ b.forwardRef((e, t) => {
  const {
    prefixCls: n,
    styles: o = {},
    classNames: r = {},
    className: i,
    rootClassName: s,
    style: a,
    defaultValue: u,
    value: c,
    readOnly: f,
    submitType: l = "enter",
    onSubmit: d,
    loading: p,
    components: v,
    onCancel: g,
    onChange: m,
    actions: x,
    onKeyPress: E,
    onKeyDown: _,
    disabled: y,
    allowSpeech: T,
    prefix: S,
    footer: R,
    header: P,
    onPaste: I,
    onPasteFile: $,
    autoSize: D = {
      maxRows: 8
    },
    ...A
  } = e, {
    direction: L,
    getPrefixCls: j
  } = It(), O = j("sender", n), V = b.useRef(null), G = b.useRef(null);
  ns(t, () => {
    var k, X;
    return {
      nativeElement: V.current,
      focus: (k = G.current) == null ? void 0 : k.focus,
      blur: (X = G.current) == null ? void 0 : X.blur
    };
  });
  const N = Io("sender"), fe = `${O}-input`, [be, U, re] = hs(O), de = ee(O, N.className, i, s, U, re, {
    [`${O}-rtl`]: L === "rtl",
    [`${O}-disabled`]: y
  }), W = `${O}-actions-btn`, te = `${O}-actions-list`, [Y, Z] = Hn(u || "", {
    value: c
  }), pe = (k, X) => {
    Z(k), m && m(k, X);
  }, [Se, me, xe] = gs((k) => {
    pe(`${Y} ${k}`);
  }, T), oe = vs(v, ["input"], Or.TextArea), Ne = {
    ...ts(A, {
      attr: !0,
      aria: !0,
      data: !0
    }),
    ref: G
  }, Oe = () => {
    Y && d && !p && d(Y);
  }, ie = () => {
    pe("");
  }, Me = b.useRef(!1), Be = () => {
    Me.current = !0;
  }, Ae = () => {
    Me.current = !1;
  }, Ie = (k) => {
    const X = k.key === "Enter" && !Me.current;
    switch (l) {
      case "enter":
        X && !k.shiftKey && (k.preventDefault(), Oe());
        break;
      case "shiftEnter":
        X && k.shiftKey && (k.preventDefault(), Oe());
        break;
    }
    E == null || E(k);
  }, F = (k) => {
    var Le;
    const X = (Le = k.clipboardData) == null ? void 0 : Le.files;
    X != null && X.length && $ && ($(X[0], X), k.preventDefault()), I == null || I(k);
  }, B = (k) => {
    var X, Le;
    k.target !== ((X = V.current) == null ? void 0 : X.querySelector(`.${fe}`)) && k.preventDefault(), (Le = G.current) == null || Le.focus();
  };
  let z = /* @__PURE__ */ b.createElement(Mr, {
    className: `${te}-presets`
  }, T && /* @__PURE__ */ b.createElement(dr, null), p ? /* @__PURE__ */ b.createElement(lr, null) : /* @__PURE__ */ b.createElement(fr, null));
  typeof x == "function" ? z = x(z, {
    components: Mn
  }) : (x || x === !1) && (z = x);
  const Ee = {
    prefixCls: W,
    onSend: Oe,
    onSendDisabled: !Y,
    onClear: ie,
    onClearDisabled: !Y,
    onCancel: g,
    onCancelDisabled: !p,
    onSpeech: () => me(!1),
    onSpeechDisabled: !Se,
    speechRecording: xe,
    disabled: y
  }, he = typeof R == "function" ? R({
    components: Mn
  }) : R || null;
  return be(/* @__PURE__ */ b.createElement("div", {
    ref: V,
    className: de,
    style: {
      ...N.style,
      ...a
    }
  }, P && /* @__PURE__ */ b.createElement(ur.Provider, {
    value: {
      prefixCls: O
    }
  }, P), /* @__PURE__ */ b.createElement(ht.Provider, {
    value: Ee
  }, /* @__PURE__ */ b.createElement("div", {
    className: `${O}-content`,
    onMouseDown: B
  }, S && /* @__PURE__ */ b.createElement("div", {
    className: ee(`${O}-prefix`, N.classNames.prefix, r.prefix),
    style: {
      ...N.styles.prefix,
      ...o.prefix
    }
  }, S), /* @__PURE__ */ b.createElement(oe, ae({}, Ne, {
    disabled: y,
    style: {
      ...N.styles.input,
      ...o.input
    },
    className: ee(fe, N.classNames.input, r.input),
    autoSize: D,
    value: Y,
    onChange: (k) => {
      pe(k.target.value, k), me(!0);
    },
    onPressEnter: Ie,
    onCompositionStart: Be,
    onCompositionEnd: Ae,
    onKeyDown: _,
    onPaste: F,
    variant: "borderless",
    readOnly: f
  })), z && /* @__PURE__ */ b.createElement("div", {
    className: ee(te, N.classNames.actions, r.actions),
    style: {
      ...N.styles.actions,
      ...o.actions
    }
  }, z)), he && /* @__PURE__ */ b.createElement("div", {
    className: ee(`${O}-footer`, N.classNames.footer, r.footer),
    style: {
      ...N.styles.footer,
      ...o.footer
    }
  }, he))));
}), pr = ys;
pr.Header = rs;
function bs(e) {
  return /^(?:async\s+)?(?:function\s*(?:\w*\s*)?\(|\([\w\s,=]*\)\s*=>|\(\{[\w\s,=]*\}\)\s*=>|function\s*\*\s*\w*\s*\()/i.test(e.trim());
}
function Ss(e, t = !1) {
  try {
    if (_r(e))
      return e;
    if (t && !bs(e))
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
function An(e, t) {
  return Sr(() => Ss(e, t), [e, t]);
}
function xs({
  value: e,
  onValueChange: t
}) {
  const [n, o] = In(e), r = ne(t);
  r.current = t;
  const i = ne(n);
  return i.current = n, ge(() => {
    r.current(n);
  }, [n]), ge(() => {
    Yr(e, i.current) || o(e);
  }, [e]), [n, o];
}
const ws = wo(({
  slots: e,
  children: t,
  onValueChange: n,
  onChange: o,
  onPasteFile: r,
  upload: i,
  elRef: s,
  ...a
}) => {
  const u = An(a.actions, !0), c = An(a.footer, !0), [f, l] = xs({
    onValueChange: n,
    value: a.value
  }), d = Rr();
  return /* @__PURE__ */ ce.jsxs(ce.Fragment, {
    children: [/* @__PURE__ */ ce.jsx("div", {
      style: {
        display: "none"
      },
      children: t
    }), /* @__PURE__ */ ce.jsx(pr, {
      ...a,
      value: f,
      ref: s,
      onSubmit: (...p) => {
        var v;
        d || (v = a.onSubmit) == null || v.call(a, ...p);
      },
      onChange: (p) => {
        o == null || o(p), l(p);
      },
      onPasteFile: async (p, v) => {
        const g = await i(Array.from(v));
        r == null || r(g.map((m) => m.path));
      },
      header: e.header ? /* @__PURE__ */ ce.jsx(He, {
        slot: e.header
      }) : a.header,
      prefix: e.prefix ? /* @__PURE__ */ ce.jsx(He, {
        slot: e.prefix
      }) : a.prefix,
      actions: e.actions ? /* @__PURE__ */ ce.jsx(He, {
        slot: e.actions
      }) : u || a.actions,
      footer: e.footer ? /* @__PURE__ */ ce.jsx(He, {
        slot: e.footer
      }) : c || a.footer
    })]
  });
});
export {
  ws as Sender,
  ws as default
};
