import { i as _e, a as D, r as pe, w as O, g as ge, b as xe } from "./Index-BhfqJShs.js";
const E = window.ms_globals.React, de = window.ms_globals.React.forwardRef, fe = window.ms_globals.React.useRef, me = window.ms_globals.React.useState, he = window.ms_globals.React.useEffect, te = window.ms_globals.React.useMemo, M = window.ms_globals.ReactDOM.createPortal, we = window.ms_globals.internalContext.useContextPropsContext, U = window.ms_globals.internalContext.ContextPropsProvider, be = window.ms_globals.antd.Select, Ce = window.ms_globals.createItemsContext.createItemsContext;
var Ie = /\s/;
function ye(e) {
  for (var t = e.length; t-- && Ie.test(e.charAt(t)); )
    ;
  return t;
}
var ve = /^\s+/;
function Ee(e) {
  return e && e.slice(0, ye(e) + 1).replace(ve, "");
}
var G = NaN, Re = /^[-+]0x[0-9a-f]+$/i, Se = /^0b[01]+$/i, Pe = /^0o[0-7]+$/i, ke = parseInt;
function q(e) {
  if (typeof e == "number")
    return e;
  if (_e(e))
    return G;
  if (D(e)) {
    var t = typeof e.valueOf == "function" ? e.valueOf() : e;
    e = D(t) ? t + "" : t;
  }
  if (typeof e != "string")
    return e === 0 ? e : +e;
  e = Ee(e);
  var o = Se.test(e);
  return o || Pe.test(e) ? ke(e.slice(2), o ? 2 : 8) : Re.test(e) ? G : +e;
}
var W = function() {
  return pe.Date.now();
}, Te = "Expected a function", je = Math.max, Oe = Math.min;
function Fe(e, t, o) {
  var c, l, n, r, s, a, g = 0, x = !1, i = !1, w = !0;
  if (typeof e != "function")
    throw new TypeError(Te);
  t = q(t) || 0, D(o) && (x = !!o.leading, i = "maxWait" in o, n = i ? je(q(o.maxWait) || 0, t) : n, w = "trailing" in o ? !!o.trailing : w);
  function f(h) {
    var I = c, v = l;
    return c = l = void 0, g = h, r = e.apply(v, I), r;
  }
  function b(h) {
    return g = h, s = setTimeout(m, t), x ? f(h) : r;
  }
  function p(h) {
    var I = h - a, v = h - g, j = t - I;
    return i ? Oe(j, n - v) : j;
  }
  function u(h) {
    var I = h - a, v = h - g;
    return a === void 0 || I >= t || I < 0 || i && v >= n;
  }
  function m() {
    var h = W();
    if (u(h))
      return C(h);
    s = setTimeout(m, p(h));
  }
  function C(h) {
    return s = void 0, w && c ? f(h) : (c = l = void 0, r);
  }
  function P() {
    s !== void 0 && clearTimeout(s), g = 0, c = a = l = s = void 0;
  }
  function d() {
    return s === void 0 ? r : C(W());
  }
  function R() {
    var h = W(), I = u(h);
    if (c = arguments, l = this, a = h, I) {
      if (s === void 0)
        return b(a);
      if (i)
        return clearTimeout(s), s = setTimeout(m, t), f(a);
    }
    return s === void 0 && (s = setTimeout(m, t)), r;
  }
  return R.cancel = P, R.flush = d, R;
}
var ne = {
  exports: {}
}, N = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var Le = E, Ne = Symbol.for("react.element"), We = Symbol.for("react.fragment"), Ae = Object.prototype.hasOwnProperty, Me = Le.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, De = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function re(e, t, o) {
  var c, l = {}, n = null, r = null;
  o !== void 0 && (n = "" + o), t.key !== void 0 && (n = "" + t.key), t.ref !== void 0 && (r = t.ref);
  for (c in t) Ae.call(t, c) && !De.hasOwnProperty(c) && (l[c] = t[c]);
  if (e && e.defaultProps) for (c in t = e.defaultProps, t) l[c] === void 0 && (l[c] = t[c]);
  return {
    $$typeof: Ne,
    type: e,
    key: n,
    ref: r,
    props: l,
    _owner: Me.current
  };
}
N.Fragment = We;
N.jsx = re;
N.jsxs = re;
ne.exports = N;
var _ = ne.exports;
const {
  SvelteComponent: Ue,
  assign: V,
  binding_callbacks: J,
  check_outros: Be,
  children: le,
  claim_element: oe,
  claim_space: He,
  component_subscribe: X,
  compute_slots: ze,
  create_slot: Ge,
  detach: T,
  element: ce,
  empty: Y,
  exclude_internal_props: K,
  get_all_dirty_from_scope: qe,
  get_slot_changes: Ve,
  group_outros: Je,
  init: Xe,
  insert_hydration: F,
  safe_not_equal: Ye,
  set_custom_element_data: se,
  space: Ke,
  transition_in: L,
  transition_out: B,
  update_slot_base: Qe
} = window.__gradio__svelte__internal, {
  beforeUpdate: Ze,
  getContext: $e,
  onDestroy: et,
  setContext: tt
} = window.__gradio__svelte__internal;
function Q(e) {
  let t, o;
  const c = (
    /*#slots*/
    e[7].default
  ), l = Ge(
    c,
    e,
    /*$$scope*/
    e[6],
    null
  );
  return {
    c() {
      t = ce("svelte-slot"), l && l.c(), this.h();
    },
    l(n) {
      t = oe(n, "SVELTE-SLOT", {
        class: !0
      });
      var r = le(t);
      l && l.l(r), r.forEach(T), this.h();
    },
    h() {
      se(t, "class", "svelte-1rt0kpf");
    },
    m(n, r) {
      F(n, t, r), l && l.m(t, null), e[9](t), o = !0;
    },
    p(n, r) {
      l && l.p && (!o || r & /*$$scope*/
      64) && Qe(
        l,
        c,
        n,
        /*$$scope*/
        n[6],
        o ? Ve(
          c,
          /*$$scope*/
          n[6],
          r,
          null
        ) : qe(
          /*$$scope*/
          n[6]
        ),
        null
      );
    },
    i(n) {
      o || (L(l, n), o = !0);
    },
    o(n) {
      B(l, n), o = !1;
    },
    d(n) {
      n && T(t), l && l.d(n), e[9](null);
    }
  };
}
function nt(e) {
  let t, o, c, l, n = (
    /*$$slots*/
    e[4].default && Q(e)
  );
  return {
    c() {
      t = ce("react-portal-target"), o = Ke(), n && n.c(), c = Y(), this.h();
    },
    l(r) {
      t = oe(r, "REACT-PORTAL-TARGET", {
        class: !0
      }), le(t).forEach(T), o = He(r), n && n.l(r), c = Y(), this.h();
    },
    h() {
      se(t, "class", "svelte-1rt0kpf");
    },
    m(r, s) {
      F(r, t, s), e[8](t), F(r, o, s), n && n.m(r, s), F(r, c, s), l = !0;
    },
    p(r, [s]) {
      /*$$slots*/
      r[4].default ? n ? (n.p(r, s), s & /*$$slots*/
      16 && L(n, 1)) : (n = Q(r), n.c(), L(n, 1), n.m(c.parentNode, c)) : n && (Je(), B(n, 1, 1, () => {
        n = null;
      }), Be());
    },
    i(r) {
      l || (L(n), l = !0);
    },
    o(r) {
      B(n), l = !1;
    },
    d(r) {
      r && (T(t), T(o), T(c)), e[8](null), n && n.d(r);
    }
  };
}
function Z(e) {
  const {
    svelteInit: t,
    ...o
  } = e;
  return o;
}
function rt(e, t, o) {
  let c, l, {
    $$slots: n = {},
    $$scope: r
  } = t;
  const s = ze(n);
  let {
    svelteInit: a
  } = t;
  const g = O(Z(t)), x = O();
  X(e, x, (d) => o(0, c = d));
  const i = O();
  X(e, i, (d) => o(1, l = d));
  const w = [], f = $e("$$ms-gr-react-wrapper"), {
    slotKey: b,
    slotIndex: p,
    subSlotIndex: u
  } = ge() || {}, m = a({
    parent: f,
    props: g,
    target: x,
    slot: i,
    slotKey: b,
    slotIndex: p,
    subSlotIndex: u,
    onDestroy(d) {
      w.push(d);
    }
  });
  tt("$$ms-gr-react-wrapper", m), Ze(() => {
    g.set(Z(t));
  }), et(() => {
    w.forEach((d) => d());
  });
  function C(d) {
    J[d ? "unshift" : "push"](() => {
      c = d, x.set(c);
    });
  }
  function P(d) {
    J[d ? "unshift" : "push"](() => {
      l = d, i.set(l);
    });
  }
  return e.$$set = (d) => {
    o(17, t = V(V({}, t), K(d))), "svelteInit" in d && o(5, a = d.svelteInit), "$$scope" in d && o(6, r = d.$$scope);
  }, t = K(t), [c, l, x, i, s, a, r, n, C, P];
}
class lt extends Ue {
  constructor(t) {
    super(), Xe(this, t, rt, nt, Ye, {
      svelteInit: 5
    });
  }
}
const {
  SvelteComponent: pt
} = window.__gradio__svelte__internal, $ = window.ms_globals.rerender, A = window.ms_globals.tree;
function ot(e, t = {}) {
  function o(c) {
    const l = O(), n = new lt({
      ...c,
      props: {
        svelteInit(r) {
          window.ms_globals.autokey += 1;
          const s = {
            key: window.ms_globals.autokey,
            svelteInstance: l,
            reactComponent: e,
            props: r.props,
            slot: r.slot,
            target: r.target,
            slotIndex: r.slotIndex,
            subSlotIndex: r.subSlotIndex,
            ignore: t.ignore,
            slotKey: r.slotKey,
            nodes: []
          }, a = r.parent ?? A;
          return a.nodes = [...a.nodes, s], $({
            createPortal: M,
            node: A
          }), r.onDestroy(() => {
            a.nodes = a.nodes.filter((g) => g.svelteInstance !== l), $({
              createPortal: M,
              node: A
            });
          }), s;
        },
        ...c.props
      }
    });
    return l.set(n), n;
  }
  return new Promise((c) => {
    window.ms_globals.initializePromise.then(() => {
      c(o);
    });
  });
}
const ct = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function st(e) {
  return e ? Object.keys(e).reduce((t, o) => {
    const c = e[o];
    return t[o] = it(o, c), t;
  }, {}) : {};
}
function it(e, t) {
  return typeof t == "number" && !ct.includes(e) ? t + "px" : t;
}
function H(e) {
  const t = [], o = e.cloneNode(!1);
  if (e._reactElement) {
    const l = E.Children.toArray(e._reactElement.props.children).map((n) => {
      if (E.isValidElement(n) && n.props.__slot__) {
        const {
          portals: r,
          clonedElement: s
        } = H(n.props.el);
        return E.cloneElement(n, {
          ...n.props,
          el: s,
          children: [...E.Children.toArray(n.props.children), ...r]
        });
      }
      return null;
    });
    return l.originalChildren = e._reactElement.props.children, t.push(M(E.cloneElement(e._reactElement, {
      ...e._reactElement.props,
      children: l
    }), o)), {
      clonedElement: o,
      portals: t
    };
  }
  Object.keys(e.getEventListeners()).forEach((l) => {
    e.getEventListeners(l).forEach(({
      listener: r,
      type: s,
      useCapture: a
    }) => {
      o.addEventListener(s, r, a);
    });
  });
  const c = Array.from(e.childNodes);
  for (let l = 0; l < c.length; l++) {
    const n = c[l];
    if (n.nodeType === 1) {
      const {
        clonedElement: r,
        portals: s
      } = H(n);
      t.push(...s), o.appendChild(r);
    } else n.nodeType === 3 && o.appendChild(n.cloneNode());
  }
  return {
    clonedElement: o,
    portals: t
  };
}
function at(e, t) {
  e && (typeof e == "function" ? e(t) : e.current = t);
}
const y = de(({
  slot: e,
  clone: t,
  className: o,
  style: c,
  observeAttributes: l
}, n) => {
  const r = fe(), [s, a] = me([]), {
    forceClone: g
  } = we(), x = g ? !0 : t;
  return he(() => {
    var p;
    if (!r.current || !e)
      return;
    let i = e;
    function w() {
      let u = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (u = i.children[0], u.tagName.toLowerCase() === "react-portal-target" && u.children[0] && (u = u.children[0])), at(n, u), o && u.classList.add(...o.split(" ")), c) {
        const m = st(c);
        Object.keys(m).forEach((C) => {
          u.style[C] = m[C];
        });
      }
    }
    let f = null, b = null;
    if (x && window.MutationObserver) {
      let u = function() {
        var d, R, h;
        (d = r.current) != null && d.contains(i) && ((R = r.current) == null || R.removeChild(i));
        const {
          portals: C,
          clonedElement: P
        } = H(e);
        i = P, a(C), i.style.display = "contents", b && clearTimeout(b), b = setTimeout(() => {
          w();
        }, 50), (h = r.current) == null || h.appendChild(i);
      };
      u();
      const m = Fe(() => {
        u(), f == null || f.disconnect(), f == null || f.observe(e, {
          childList: !0,
          subtree: !0,
          attributes: l
        });
      }, 50);
      f = new window.MutationObserver(m), f.observe(e, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      i.style.display = "contents", w(), (p = r.current) == null || p.appendChild(i);
    return () => {
      var u, m;
      i.style.display = "", (u = r.current) != null && u.contains(i) && ((m = r.current) == null || m.removeChild(i)), f == null || f.disconnect();
    };
  }, [e, x, o, c, n, l, g]), E.createElement("react-child", {
    ref: r,
    style: {
      display: "contents"
    }
  }, ...s);
});
function ut(e) {
  return /^(?:async\s+)?(?:function\s*(?:\w*\s*)?\(|\([\w\s,=]*\)\s*=>|\(\{[\w\s,=]*\}\)\s*=>|function\s*\*\s*\w*\s*\()/i.test(e.trim());
}
function dt(e, t = !1) {
  try {
    if (xe(e))
      return e;
    if (t && !ut(e))
      return;
    if (typeof e == "string") {
      let o = e.trim();
      return o.startsWith(";") && (o = o.slice(1)), o.endsWith(";") && (o = o.slice(0, -1)), new Function(`return (...args) => (${o})(...args)`)();
    }
    return;
  } catch {
    return;
  }
}
function S(e, t) {
  return te(() => dt(e, t), [e, t]);
}
const ft = ({
  children: e,
  ...t
}) => /* @__PURE__ */ _.jsx(_.Fragment, {
  children: e(t)
});
function ie(e) {
  return E.createElement(ft, {
    children: e
  });
}
function ae(e, t, o) {
  const c = e.filter(Boolean);
  if (c.length !== 0)
    return c.map((l, n) => {
      var g;
      if (typeof l != "object")
        return t != null && t.fallback ? t.fallback(l) : l;
      const r = {
        ...l.props,
        key: ((g = l.props) == null ? void 0 : g.key) ?? (o ? `${o}-${n}` : `${n}`)
      };
      let s = r;
      Object.keys(l.slots).forEach((x) => {
        if (!l.slots[x] || !(l.slots[x] instanceof Element) && !l.slots[x].el)
          return;
        const i = x.split(".");
        i.forEach((m, C) => {
          s[m] || (s[m] = {}), C !== i.length - 1 && (s = r[m]);
        });
        const w = l.slots[x];
        let f, b, p = (t == null ? void 0 : t.clone) ?? !1, u = t == null ? void 0 : t.forceClone;
        w instanceof Element ? f = w : (f = w.el, b = w.callback, p = w.clone ?? p, u = w.forceClone ?? u), u = u ?? !!b, s[i[i.length - 1]] = f ? b ? (...m) => (b(i[i.length - 1], m), /* @__PURE__ */ _.jsx(U, {
          ...l.ctx,
          params: m,
          forceClone: u,
          children: /* @__PURE__ */ _.jsx(y, {
            slot: f,
            clone: p
          })
        })) : ie((m) => /* @__PURE__ */ _.jsx(U, {
          ...l.ctx,
          forceClone: u,
          children: /* @__PURE__ */ _.jsx(y, {
            ...m,
            slot: f,
            clone: p
          })
        })) : s[i[i.length - 1]], s = r;
      });
      const a = (t == null ? void 0 : t.children) || "children";
      return l[a] ? r[a] = ae(l[a], t, `${n}`) : t != null && t.children && (r[a] = void 0, Reflect.deleteProperty(r, a)), r;
    });
}
function ee(e, t) {
  return e ? t != null && t.forceClone || t != null && t.params ? ie((o) => /* @__PURE__ */ _.jsx(U, {
    forceClone: t == null ? void 0 : t.forceClone,
    params: t == null ? void 0 : t.params,
    children: /* @__PURE__ */ _.jsx(y, {
      slot: e,
      clone: t == null ? void 0 : t.clone,
      ...o
    })
  })) : /* @__PURE__ */ _.jsx(y, {
    slot: e,
    clone: t == null ? void 0 : t.clone
  }) : null;
}
function k({
  key: e,
  slots: t,
  targets: o
}, c) {
  return t[e] ? (...l) => o ? o.map((n, r) => /* @__PURE__ */ _.jsx(E.Fragment, {
    children: ee(n, {
      clone: !0,
      params: l,
      forceClone: !0
    })
  }, r)) : /* @__PURE__ */ _.jsx(_.Fragment, {
    children: ee(t[e], {
      clone: !0,
      params: l,
      forceClone: !0
    })
  }) : void 0;
}
const {
  withItemsContextProvider: mt,
  useItems: ht,
  ItemHandler: gt
} = Ce("antd-select-options"), xt = ot(mt(["options", "default"], ({
  slots: e,
  children: t,
  onValueChange: o,
  filterOption: c,
  onChange: l,
  options: n,
  getPopupContainer: r,
  dropdownRender: s,
  popupRender: a,
  optionRender: g,
  tagRender: x,
  labelRender: i,
  filterSort: w,
  elRef: f,
  setSlotParams: b,
  ...p
}) => {
  const u = S(r), m = S(c), C = S(s), P = S(a), d = S(w), R = S(g), h = S(x), I = S(i), {
    items: v
  } = ht(), j = v.options.length > 0 ? v.options : v.default;
  return /* @__PURE__ */ _.jsxs(_.Fragment, {
    children: [/* @__PURE__ */ _.jsx("div", {
      style: {
        display: "none"
      },
      children: t
    }), /* @__PURE__ */ _.jsx(be, {
      ...p,
      ref: f,
      options: te(() => n || ae(j, {
        children: "options",
        clone: !0
      }), [j, n]),
      onChange: (z, ...ue) => {
        l == null || l(z, ...ue), o(z);
      },
      allowClear: e["allowClear.clearIcon"] ? {
        clearIcon: /* @__PURE__ */ _.jsx(y, {
          slot: e["allowClear.clearIcon"]
        })
      } : p.allowClear,
      prefix: e.prefix ? /* @__PURE__ */ _.jsx(y, {
        slot: e.prefix
      }) : p.prefix,
      removeIcon: e.removeIcon ? /* @__PURE__ */ _.jsx(y, {
        slot: e.removeIcon
      }) : p.removeIcon,
      suffixIcon: e.suffixIcon ? /* @__PURE__ */ _.jsx(y, {
        slot: e.suffixIcon
      }) : p.suffixIcon,
      notFoundContent: e.notFoundContent ? /* @__PURE__ */ _.jsx(y, {
        slot: e.notFoundContent
      }) : p.notFoundContent,
      menuItemSelectedIcon: e.menuItemSelectedIcon ? /* @__PURE__ */ _.jsx(y, {
        slot: e.menuItemSelectedIcon
      }) : p.menuItemSelectedIcon,
      filterOption: m || c,
      maxTagPlaceholder: e.maxTagPlaceholder ? k({
        slots: e,
        key: "maxTagPlaceholder"
      }) : p.maxTagPlaceholder,
      getPopupContainer: u,
      dropdownRender: e.dropdownRender ? k({
        slots: e,
        key: "dropdownRender"
      }) : C,
      popupRender: e.popupRender ? k({
        slots: e,
        key: "popupRender"
      }) : P,
      optionRender: e.optionRender ? k({
        slots: e,
        key: "optionRender"
      }) : R,
      tagRender: e.tagRender ? k({
        slots: e,
        key: "tagRender"
      }) : h,
      labelRender: e.labelRender ? k({
        slots: e,
        key: "labelRender"
      }) : I,
      filterSort: d
    })]
  });
}));
export {
  xt as Select,
  xt as default
};
