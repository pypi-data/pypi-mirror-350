import { i as ue, a as A, r as de, b as fe, w as k, g as me, c as _e } from "./Index-GRvK6_HQ.js";
const v = window.ms_globals.React, ae = window.ms_globals.React.forwardRef, N = window.ms_globals.React.useRef, ee = window.ms_globals.React.useState, W = window.ms_globals.React.useEffect, te = window.ms_globals.React.useMemo, M = window.ms_globals.ReactDOM.createPortal, he = window.ms_globals.internalContext.useContextPropsContext, H = window.ms_globals.internalContext.ContextPropsProvider, pe = window.ms_globals.antd.Mentions, ge = window.ms_globals.createItemsContext.createItemsContext;
var be = /\s/;
function we(e) {
  for (var t = e.length; t-- && be.test(e.charAt(t)); )
    ;
  return t;
}
var xe = /^\s+/;
function Ce(e) {
  return e && e.slice(0, we(e) + 1).replace(xe, "");
}
var q = NaN, Ee = /^[-+]0x[0-9a-f]+$/i, ve = /^0b[01]+$/i, ye = /^0o[0-7]+$/i, Ie = parseInt;
function z(e) {
  if (typeof e == "number")
    return e;
  if (ue(e))
    return q;
  if (A(e)) {
    var t = typeof e.valueOf == "function" ? e.valueOf() : e;
    e = A(t) ? t + "" : t;
  }
  if (typeof e != "string")
    return e === 0 ? e : +e;
  e = Ce(e);
  var s = ve.test(e);
  return s || ye.test(e) ? Ie(e.slice(2), s ? 2 : 8) : Ee.test(e) ? q : +e;
}
var j = function() {
  return de.Date.now();
}, Se = "Expected a function", Re = Math.max, ke = Math.min;
function Oe(e, t, s) {
  var l, r, n, o, i, u, h = 0, p = !1, c = !1, g = !0;
  if (typeof e != "function")
    throw new TypeError(Se);
  t = z(t) || 0, A(s) && (p = !!s.leading, c = "maxWait" in s, n = c ? Re(z(s.maxWait) || 0, t) : n, g = "trailing" in s ? !!s.trailing : g);
  function f(_) {
    var E = l, R = r;
    return l = r = void 0, h = _, o = e.apply(R, E), o;
  }
  function w(_) {
    return h = _, i = setTimeout(d, t), p ? f(_) : o;
  }
  function b(_) {
    var E = _ - u, R = _ - h, B = t - E;
    return c ? ke(B, n - R) : B;
  }
  function a(_) {
    var E = _ - u, R = _ - h;
    return u === void 0 || E >= t || E < 0 || c && R >= n;
  }
  function d() {
    var _ = j();
    if (a(_))
      return x(_);
    i = setTimeout(d, b(_));
  }
  function x(_) {
    return i = void 0, g && l ? f(_) : (l = r = void 0, o);
  }
  function S() {
    i !== void 0 && clearTimeout(i), h = 0, l = u = r = i = void 0;
  }
  function m() {
    return i === void 0 ? o : x(j());
  }
  function y() {
    var _ = j(), E = a(_);
    if (l = arguments, r = this, u = _, E) {
      if (i === void 0)
        return w(u);
      if (c)
        return clearTimeout(i), i = setTimeout(d, t), f(u);
    }
    return i === void 0 && (i = setTimeout(d, t)), o;
  }
  return y.cancel = S, y.flush = m, y;
}
function Pe(e, t) {
  return fe(e, t);
}
var ne = {
  exports: {}
}, T = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var Te = v, je = Symbol.for("react.element"), Fe = Symbol.for("react.fragment"), Le = Object.prototype.hasOwnProperty, Ne = Te.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, We = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function re(e, t, s) {
  var l, r = {}, n = null, o = null;
  s !== void 0 && (n = "" + s), t.key !== void 0 && (n = "" + t.key), t.ref !== void 0 && (o = t.ref);
  for (l in t) Le.call(t, l) && !We.hasOwnProperty(l) && (r[l] = t[l]);
  if (e && e.defaultProps) for (l in t = e.defaultProps, t) r[l] === void 0 && (r[l] = t[l]);
  return {
    $$typeof: je,
    type: e,
    key: n,
    ref: o,
    props: r,
    _owner: Ne.current
  };
}
T.Fragment = Fe;
T.jsx = re;
T.jsxs = re;
ne.exports = T;
var C = ne.exports;
const {
  SvelteComponent: Me,
  assign: G,
  binding_callbacks: J,
  check_outros: Ae,
  children: oe,
  claim_element: se,
  claim_space: De,
  component_subscribe: X,
  compute_slots: Ve,
  create_slot: Ue,
  detach: I,
  element: le,
  empty: Y,
  exclude_internal_props: K,
  get_all_dirty_from_scope: Be,
  get_slot_changes: He,
  group_outros: qe,
  init: ze,
  insert_hydration: O,
  safe_not_equal: Ge,
  set_custom_element_data: ie,
  space: Je,
  transition_in: P,
  transition_out: D,
  update_slot_base: Xe
} = window.__gradio__svelte__internal, {
  beforeUpdate: Ye,
  getContext: Ke,
  onDestroy: Qe,
  setContext: Ze
} = window.__gradio__svelte__internal;
function Q(e) {
  let t, s;
  const l = (
    /*#slots*/
    e[7].default
  ), r = Ue(
    l,
    e,
    /*$$scope*/
    e[6],
    null
  );
  return {
    c() {
      t = le("svelte-slot"), r && r.c(), this.h();
    },
    l(n) {
      t = se(n, "SVELTE-SLOT", {
        class: !0
      });
      var o = oe(t);
      r && r.l(o), o.forEach(I), this.h();
    },
    h() {
      ie(t, "class", "svelte-1rt0kpf");
    },
    m(n, o) {
      O(n, t, o), r && r.m(t, null), e[9](t), s = !0;
    },
    p(n, o) {
      r && r.p && (!s || o & /*$$scope*/
      64) && Xe(
        r,
        l,
        n,
        /*$$scope*/
        n[6],
        s ? He(
          l,
          /*$$scope*/
          n[6],
          o,
          null
        ) : Be(
          /*$$scope*/
          n[6]
        ),
        null
      );
    },
    i(n) {
      s || (P(r, n), s = !0);
    },
    o(n) {
      D(r, n), s = !1;
    },
    d(n) {
      n && I(t), r && r.d(n), e[9](null);
    }
  };
}
function $e(e) {
  let t, s, l, r, n = (
    /*$$slots*/
    e[4].default && Q(e)
  );
  return {
    c() {
      t = le("react-portal-target"), s = Je(), n && n.c(), l = Y(), this.h();
    },
    l(o) {
      t = se(o, "REACT-PORTAL-TARGET", {
        class: !0
      }), oe(t).forEach(I), s = De(o), n && n.l(o), l = Y(), this.h();
    },
    h() {
      ie(t, "class", "svelte-1rt0kpf");
    },
    m(o, i) {
      O(o, t, i), e[8](t), O(o, s, i), n && n.m(o, i), O(o, l, i), r = !0;
    },
    p(o, [i]) {
      /*$$slots*/
      o[4].default ? n ? (n.p(o, i), i & /*$$slots*/
      16 && P(n, 1)) : (n = Q(o), n.c(), P(n, 1), n.m(l.parentNode, l)) : n && (qe(), D(n, 1, 1, () => {
        n = null;
      }), Ae());
    },
    i(o) {
      r || (P(n), r = !0);
    },
    o(o) {
      D(n), r = !1;
    },
    d(o) {
      o && (I(t), I(s), I(l)), e[8](null), n && n.d(o);
    }
  };
}
function Z(e) {
  const {
    svelteInit: t,
    ...s
  } = e;
  return s;
}
function et(e, t, s) {
  let l, r, {
    $$slots: n = {},
    $$scope: o
  } = t;
  const i = Ve(n);
  let {
    svelteInit: u
  } = t;
  const h = k(Z(t)), p = k();
  X(e, p, (m) => s(0, l = m));
  const c = k();
  X(e, c, (m) => s(1, r = m));
  const g = [], f = Ke("$$ms-gr-react-wrapper"), {
    slotKey: w,
    slotIndex: b,
    subSlotIndex: a
  } = me() || {}, d = u({
    parent: f,
    props: h,
    target: p,
    slot: c,
    slotKey: w,
    slotIndex: b,
    subSlotIndex: a,
    onDestroy(m) {
      g.push(m);
    }
  });
  Ze("$$ms-gr-react-wrapper", d), Ye(() => {
    h.set(Z(t));
  }), Qe(() => {
    g.forEach((m) => m());
  });
  function x(m) {
    J[m ? "unshift" : "push"](() => {
      l = m, p.set(l);
    });
  }
  function S(m) {
    J[m ? "unshift" : "push"](() => {
      r = m, c.set(r);
    });
  }
  return e.$$set = (m) => {
    s(17, t = G(G({}, t), K(m))), "svelteInit" in m && s(5, u = m.svelteInit), "$$scope" in m && s(6, o = m.$$scope);
  }, t = K(t), [l, r, p, c, i, u, o, n, x, S];
}
class tt extends Me {
  constructor(t) {
    super(), ze(this, t, et, $e, Ge, {
      svelteInit: 5
    });
  }
}
const {
  SvelteComponent: ht
} = window.__gradio__svelte__internal, $ = window.ms_globals.rerender, F = window.ms_globals.tree;
function nt(e, t = {}) {
  function s(l) {
    const r = k(), n = new tt({
      ...l,
      props: {
        svelteInit(o) {
          window.ms_globals.autokey += 1;
          const i = {
            key: window.ms_globals.autokey,
            svelteInstance: r,
            reactComponent: e,
            props: o.props,
            slot: o.slot,
            target: o.target,
            slotIndex: o.slotIndex,
            subSlotIndex: o.subSlotIndex,
            ignore: t.ignore,
            slotKey: o.slotKey,
            nodes: []
          }, u = o.parent ?? F;
          return u.nodes = [...u.nodes, i], $({
            createPortal: M,
            node: F
          }), o.onDestroy(() => {
            u.nodes = u.nodes.filter((h) => h.svelteInstance !== r), $({
              createPortal: M,
              node: F
            });
          }), i;
        },
        ...l.props
      }
    });
    return r.set(n), n;
  }
  return new Promise((l) => {
    window.ms_globals.initializePromise.then(() => {
      l(s);
    });
  });
}
const rt = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function ot(e) {
  return e ? Object.keys(e).reduce((t, s) => {
    const l = e[s];
    return t[s] = st(s, l), t;
  }, {}) : {};
}
function st(e, t) {
  return typeof t == "number" && !rt.includes(e) ? t + "px" : t;
}
function V(e) {
  const t = [], s = e.cloneNode(!1);
  if (e._reactElement) {
    const r = v.Children.toArray(e._reactElement.props.children).map((n) => {
      if (v.isValidElement(n) && n.props.__slot__) {
        const {
          portals: o,
          clonedElement: i
        } = V(n.props.el);
        return v.cloneElement(n, {
          ...n.props,
          el: i,
          children: [...v.Children.toArray(n.props.children), ...o]
        });
      }
      return null;
    });
    return r.originalChildren = e._reactElement.props.children, t.push(M(v.cloneElement(e._reactElement, {
      ...e._reactElement.props,
      children: r
    }), s)), {
      clonedElement: s,
      portals: t
    };
  }
  Object.keys(e.getEventListeners()).forEach((r) => {
    e.getEventListeners(r).forEach(({
      listener: o,
      type: i,
      useCapture: u
    }) => {
      s.addEventListener(i, o, u);
    });
  });
  const l = Array.from(e.childNodes);
  for (let r = 0; r < l.length; r++) {
    const n = l[r];
    if (n.nodeType === 1) {
      const {
        clonedElement: o,
        portals: i
      } = V(n);
      t.push(...i), s.appendChild(o);
    } else n.nodeType === 3 && s.appendChild(n.cloneNode());
  }
  return {
    clonedElement: s,
    portals: t
  };
}
function lt(e, t) {
  e && (typeof e == "function" ? e(t) : e.current = t);
}
const U = ae(({
  slot: e,
  clone: t,
  className: s,
  style: l,
  observeAttributes: r
}, n) => {
  const o = N(), [i, u] = ee([]), {
    forceClone: h
  } = he(), p = h ? !0 : t;
  return W(() => {
    var b;
    if (!o.current || !e)
      return;
    let c = e;
    function g() {
      let a = c;
      if (c.tagName.toLowerCase() === "svelte-slot" && c.children.length === 1 && c.children[0] && (a = c.children[0], a.tagName.toLowerCase() === "react-portal-target" && a.children[0] && (a = a.children[0])), lt(n, a), s && a.classList.add(...s.split(" ")), l) {
        const d = ot(l);
        Object.keys(d).forEach((x) => {
          a.style[x] = d[x];
        });
      }
    }
    let f = null, w = null;
    if (p && window.MutationObserver) {
      let a = function() {
        var m, y, _;
        (m = o.current) != null && m.contains(c) && ((y = o.current) == null || y.removeChild(c));
        const {
          portals: x,
          clonedElement: S
        } = V(e);
        c = S, u(x), c.style.display = "contents", w && clearTimeout(w), w = setTimeout(() => {
          g();
        }, 50), (_ = o.current) == null || _.appendChild(c);
      };
      a();
      const d = Oe(() => {
        a(), f == null || f.disconnect(), f == null || f.observe(e, {
          childList: !0,
          subtree: !0,
          attributes: r
        });
      }, 50);
      f = new window.MutationObserver(d), f.observe(e, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      c.style.display = "contents", g(), (b = o.current) == null || b.appendChild(c);
    return () => {
      var a, d;
      c.style.display = "", (a = o.current) != null && a.contains(c) && ((d = o.current) == null || d.removeChild(c)), f == null || f.disconnect();
    };
  }, [e, p, s, l, n, r, h]), v.createElement("react-child", {
    ref: o,
    style: {
      display: "contents"
    }
  }, ...i);
});
function it(e) {
  return /^(?:async\s+)?(?:function\s*(?:\w*\s*)?\(|\([\w\s,=]*\)\s*=>|\(\{[\w\s,=]*\}\)\s*=>|function\s*\*\s*\w*\s*\()/i.test(e.trim());
}
function ct(e, t = !1) {
  try {
    if (_e(e))
      return e;
    if (t && !it(e))
      return;
    if (typeof e == "string") {
      let s = e.trim();
      return s.startsWith(";") && (s = s.slice(1)), s.endsWith(";") && (s = s.slice(0, -1)), new Function(`return (...args) => (${s})(...args)`)();
    }
    return;
  } catch {
    return;
  }
}
function L(e, t) {
  return te(() => ct(e, t), [e, t]);
}
function at({
  value: e,
  onValueChange: t
}) {
  const [s, l] = ee(e), r = N(t);
  r.current = t;
  const n = N(s);
  return n.current = s, W(() => {
    r.current(s);
  }, [s]), W(() => {
    Pe(e, n.current) || l(e);
  }, [e]), [s, l];
}
const ut = ({
  children: e,
  ...t
}) => /* @__PURE__ */ C.jsx(C.Fragment, {
  children: e(t)
});
function dt(e) {
  return v.createElement(ut, {
    children: e
  });
}
function ce(e, t, s) {
  const l = e.filter(Boolean);
  if (l.length !== 0)
    return l.map((r, n) => {
      var h;
      if (typeof r != "object")
        return t != null && t.fallback ? t.fallback(r) : r;
      const o = {
        ...r.props,
        key: ((h = r.props) == null ? void 0 : h.key) ?? (s ? `${s}-${n}` : `${n}`)
      };
      let i = o;
      Object.keys(r.slots).forEach((p) => {
        if (!r.slots[p] || !(r.slots[p] instanceof Element) && !r.slots[p].el)
          return;
        const c = p.split(".");
        c.forEach((d, x) => {
          i[d] || (i[d] = {}), x !== c.length - 1 && (i = o[d]);
        });
        const g = r.slots[p];
        let f, w, b = (t == null ? void 0 : t.clone) ?? !1, a = t == null ? void 0 : t.forceClone;
        g instanceof Element ? f = g : (f = g.el, w = g.callback, b = g.clone ?? b, a = g.forceClone ?? a), a = a ?? !!w, i[c[c.length - 1]] = f ? w ? (...d) => (w(c[c.length - 1], d), /* @__PURE__ */ C.jsx(H, {
          ...r.ctx,
          params: d,
          forceClone: a,
          children: /* @__PURE__ */ C.jsx(U, {
            slot: f,
            clone: b
          })
        })) : dt((d) => /* @__PURE__ */ C.jsx(H, {
          ...r.ctx,
          forceClone: a,
          children: /* @__PURE__ */ C.jsx(U, {
            ...d,
            slot: f,
            clone: b
          })
        })) : i[c[c.length - 1]], i = o;
      });
      const u = (t == null ? void 0 : t.children) || "children";
      return r[u] ? o[u] = ce(r[u], t, `${n}`) : t != null && t.children && (o[u] = void 0, Reflect.deleteProperty(o, u)), o;
    });
}
const {
  useItems: ft,
  withItemsContextProvider: mt,
  ItemHandler: pt
} = ge("antd-mentions-options"), gt = nt(mt(["options", "default"], ({
  slots: e,
  children: t,
  onValueChange: s,
  filterOption: l,
  onChange: r,
  options: n,
  validateSearch: o,
  getPopupContainer: i,
  elRef: u,
  ...h
}) => {
  const p = L(i), c = L(l), g = L(o), [f, w] = at({
    onValueChange: s,
    value: h.value
  }), {
    items: b
  } = ft(), a = b.options.length > 0 ? b.options : b.default;
  return /* @__PURE__ */ C.jsxs(C.Fragment, {
    children: [/* @__PURE__ */ C.jsx("div", {
      style: {
        display: "none"
      },
      children: t
    }), /* @__PURE__ */ C.jsx(pe, {
      ...h,
      ref: u,
      value: f,
      options: te(() => n || ce(a, {
        clone: !0
      }), [a, n]),
      onChange: (d, ...x) => {
        r == null || r(d, ...x), w(d);
      },
      validateSearch: g,
      notFoundContent: e.notFoundContent ? /* @__PURE__ */ C.jsx(U, {
        slot: e.notFoundContent
      }) : h.notFoundContent,
      filterOption: c || l,
      getPopupContainer: p
    })]
  });
}));
export {
  gt as Mentions,
  gt as default
};
