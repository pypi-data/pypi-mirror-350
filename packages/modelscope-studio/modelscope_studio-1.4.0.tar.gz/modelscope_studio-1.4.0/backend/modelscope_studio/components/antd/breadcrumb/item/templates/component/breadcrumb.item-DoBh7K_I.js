import { i as me, a as B, r as pe, w as k, g as he, b as _e } from "./Index-BGAN9exw.js";
const I = window.ms_globals.React, ae = window.ms_globals.React.forwardRef, de = window.ms_globals.React.useRef, ue = window.ms_globals.React.useState, fe = window.ms_globals.React.useEffect, A = window.ms_globals.ReactDOM.createPortal, we = window.ms_globals.internalContext.useContextPropsContext, M = window.ms_globals.internalContext.ContextPropsProvider, te = window.ms_globals.createItemsContext.createItemsContext;
var ge = /\s/;
function ve(t) {
  for (var e = t.length; e-- && ge.test(t.charAt(e)); )
    ;
  return e;
}
var xe = /^\s+/;
function be(t) {
  return t && t.slice(0, ve(t) + 1).replace(xe, "");
}
var G = NaN, Ie = /^[-+]0x[0-9a-f]+$/i, Ce = /^0b[01]+$/i, ye = /^0o[0-7]+$/i, Ee = parseInt;
function q(t) {
  if (typeof t == "number")
    return t;
  if (me(t))
    return G;
  if (B(t)) {
    var e = typeof t.valueOf == "function" ? t.valueOf() : t;
    t = B(e) ? e + "" : e;
  }
  if (typeof t != "string")
    return t === 0 ? t : +t;
  t = be(t);
  var l = Ce.test(t);
  return l || ye.test(t) ? Ee(t.slice(2), l ? 2 : 8) : Ie.test(t) ? G : +t;
}
var W = function() {
  return pe.Date.now();
}, Se = "Expected a function", Pe = Math.max, Re = Math.min;
function ke(t, e, l) {
  var s, o, n, r, c, a, h = 0, _ = !1, i = !1, w = !0;
  if (typeof t != "function")
    throw new TypeError(Se);
  e = q(e) || 0, B(l) && (_ = !!l.leading, i = "maxWait" in l, n = i ? Pe(q(l.maxWait) || 0, e) : n, w = "trailing" in l ? !!l.trailing : w);
  function f(p) {
    var y = s, P = o;
    return s = o = void 0, h = p, r = t.apply(P, y), r;
  }
  function g(p) {
    return h = p, c = setTimeout(m, e), _ ? f(p) : r;
  }
  function v(p) {
    var y = p - a, P = p - h, z = e - y;
    return i ? Re(z, n - P) : z;
  }
  function d(p) {
    var y = p - a, P = p - h;
    return a === void 0 || y >= e || y < 0 || i && P >= n;
  }
  function m() {
    var p = W();
    if (d(p))
      return x(p);
    c = setTimeout(m, v(p));
  }
  function x(p) {
    return c = void 0, w && s ? f(p) : (s = o = void 0, r);
  }
  function C() {
    c !== void 0 && clearTimeout(c), h = 0, s = a = o = c = void 0;
  }
  function u() {
    return c === void 0 ? r : x(W());
  }
  function E() {
    var p = W(), y = d(p);
    if (s = arguments, o = this, a = p, y) {
      if (c === void 0)
        return g(a);
      if (i)
        return clearTimeout(c), c = setTimeout(m, e), f(a);
    }
    return c === void 0 && (c = setTimeout(m, e)), r;
  }
  return E.cancel = C, E.flush = u, E;
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
var Oe = I, Te = Symbol.for("react.element"), je = Symbol.for("react.fragment"), Le = Object.prototype.hasOwnProperty, Ne = Oe.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, We = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function re(t, e, l) {
  var s, o = {}, n = null, r = null;
  l !== void 0 && (n = "" + l), e.key !== void 0 && (n = "" + e.key), e.ref !== void 0 && (r = e.ref);
  for (s in e) Le.call(e, s) && !We.hasOwnProperty(s) && (o[s] = e[s]);
  if (t && t.defaultProps) for (s in e = t.defaultProps, e) o[s] === void 0 && (o[s] = e[s]);
  return {
    $$typeof: Te,
    type: t,
    key: n,
    ref: r,
    props: o,
    _owner: Ne.current
  };
}
N.Fragment = je;
N.jsx = re;
N.jsxs = re;
ne.exports = N;
var b = ne.exports;
const {
  SvelteComponent: Fe,
  assign: V,
  binding_callbacks: J,
  check_outros: Ae,
  children: oe,
  claim_element: le,
  claim_space: Be,
  component_subscribe: X,
  compute_slots: Me,
  create_slot: De,
  detach: S,
  element: se,
  empty: Y,
  exclude_internal_props: K,
  get_all_dirty_from_scope: He,
  get_slot_changes: Ue,
  group_outros: ze,
  init: Ge,
  insert_hydration: O,
  safe_not_equal: qe,
  set_custom_element_data: ce,
  space: Ve,
  transition_in: T,
  transition_out: D,
  update_slot_base: Je
} = window.__gradio__svelte__internal, {
  beforeUpdate: Xe,
  getContext: Ye,
  onDestroy: Ke,
  setContext: Qe
} = window.__gradio__svelte__internal;
function Q(t) {
  let e, l;
  const s = (
    /*#slots*/
    t[7].default
  ), o = De(
    s,
    t,
    /*$$scope*/
    t[6],
    null
  );
  return {
    c() {
      e = se("svelte-slot"), o && o.c(), this.h();
    },
    l(n) {
      e = le(n, "SVELTE-SLOT", {
        class: !0
      });
      var r = oe(e);
      o && o.l(r), r.forEach(S), this.h();
    },
    h() {
      ce(e, "class", "svelte-1rt0kpf");
    },
    m(n, r) {
      O(n, e, r), o && o.m(e, null), t[9](e), l = !0;
    },
    p(n, r) {
      o && o.p && (!l || r & /*$$scope*/
      64) && Je(
        o,
        s,
        n,
        /*$$scope*/
        n[6],
        l ? Ue(
          s,
          /*$$scope*/
          n[6],
          r,
          null
        ) : He(
          /*$$scope*/
          n[6]
        ),
        null
      );
    },
    i(n) {
      l || (T(o, n), l = !0);
    },
    o(n) {
      D(o, n), l = !1;
    },
    d(n) {
      n && S(e), o && o.d(n), t[9](null);
    }
  };
}
function Ze(t) {
  let e, l, s, o, n = (
    /*$$slots*/
    t[4].default && Q(t)
  );
  return {
    c() {
      e = se("react-portal-target"), l = Ve(), n && n.c(), s = Y(), this.h();
    },
    l(r) {
      e = le(r, "REACT-PORTAL-TARGET", {
        class: !0
      }), oe(e).forEach(S), l = Be(r), n && n.l(r), s = Y(), this.h();
    },
    h() {
      ce(e, "class", "svelte-1rt0kpf");
    },
    m(r, c) {
      O(r, e, c), t[8](e), O(r, l, c), n && n.m(r, c), O(r, s, c), o = !0;
    },
    p(r, [c]) {
      /*$$slots*/
      r[4].default ? n ? (n.p(r, c), c & /*$$slots*/
      16 && T(n, 1)) : (n = Q(r), n.c(), T(n, 1), n.m(s.parentNode, s)) : n && (ze(), D(n, 1, 1, () => {
        n = null;
      }), Ae());
    },
    i(r) {
      o || (T(n), o = !0);
    },
    o(r) {
      D(n), o = !1;
    },
    d(r) {
      r && (S(e), S(l), S(s)), t[8](null), n && n.d(r);
    }
  };
}
function Z(t) {
  const {
    svelteInit: e,
    ...l
  } = t;
  return l;
}
function $e(t, e, l) {
  let s, o, {
    $$slots: n = {},
    $$scope: r
  } = e;
  const c = Me(n);
  let {
    svelteInit: a
  } = e;
  const h = k(Z(e)), _ = k();
  X(t, _, (u) => l(0, s = u));
  const i = k();
  X(t, i, (u) => l(1, o = u));
  const w = [], f = Ye("$$ms-gr-react-wrapper"), {
    slotKey: g,
    slotIndex: v,
    subSlotIndex: d
  } = he() || {}, m = a({
    parent: f,
    props: h,
    target: _,
    slot: i,
    slotKey: g,
    slotIndex: v,
    subSlotIndex: d,
    onDestroy(u) {
      w.push(u);
    }
  });
  Qe("$$ms-gr-react-wrapper", m), Xe(() => {
    h.set(Z(e));
  }), Ke(() => {
    w.forEach((u) => u());
  });
  function x(u) {
    J[u ? "unshift" : "push"](() => {
      s = u, _.set(s);
    });
  }
  function C(u) {
    J[u ? "unshift" : "push"](() => {
      o = u, i.set(o);
    });
  }
  return t.$$set = (u) => {
    l(17, e = V(V({}, e), K(u))), "svelteInit" in u && l(5, a = u.svelteInit), "$$scope" in u && l(6, r = u.$$scope);
  }, e = K(e), [s, o, _, i, c, a, r, n, x, C];
}
class et extends Fe {
  constructor(e) {
    super(), Ge(this, e, $e, Ze, qe, {
      svelteInit: 5
    });
  }
}
const {
  SvelteComponent: ft
} = window.__gradio__svelte__internal, $ = window.ms_globals.rerender, F = window.ms_globals.tree;
function tt(t, e = {}) {
  function l(s) {
    const o = k(), n = new et({
      ...s,
      props: {
        svelteInit(r) {
          window.ms_globals.autokey += 1;
          const c = {
            key: window.ms_globals.autokey,
            svelteInstance: o,
            reactComponent: t,
            props: r.props,
            slot: r.slot,
            target: r.target,
            slotIndex: r.slotIndex,
            subSlotIndex: r.subSlotIndex,
            ignore: e.ignore,
            slotKey: r.slotKey,
            nodes: []
          }, a = r.parent ?? F;
          return a.nodes = [...a.nodes, c], $({
            createPortal: A,
            node: F
          }), r.onDestroy(() => {
            a.nodes = a.nodes.filter((h) => h.svelteInstance !== o), $({
              createPortal: A,
              node: F
            });
          }), c;
        },
        ...s.props
      }
    });
    return o.set(n), n;
  }
  return new Promise((s) => {
    window.ms_globals.initializePromise.then(() => {
      s(l);
    });
  });
}
function nt(t) {
  return /^(?:async\s+)?(?:function\s*(?:\w*\s*)?\(|\([\w\s,=]*\)\s*=>|\(\{[\w\s,=]*\}\)\s*=>|function\s*\*\s*\w*\s*\()/i.test(t.trim());
}
function ee(t, e = !1) {
  try {
    if (_e(t))
      return t;
    if (e && !nt(t))
      return;
    if (typeof t == "string") {
      let l = t.trim();
      return l.startsWith(";") && (l = l.slice(1)), l.endsWith(";") && (l = l.slice(0, -1)), new Function(`return (...args) => (${l})(...args)`)();
    }
    return;
  } catch {
    return;
  }
}
const rt = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function ot(t) {
  return t ? Object.keys(t).reduce((e, l) => {
    const s = t[l];
    return e[l] = lt(l, s), e;
  }, {}) : {};
}
function lt(t, e) {
  return typeof e == "number" && !rt.includes(t) ? e + "px" : e;
}
function H(t) {
  const e = [], l = t.cloneNode(!1);
  if (t._reactElement) {
    const o = I.Children.toArray(t._reactElement.props.children).map((n) => {
      if (I.isValidElement(n) && n.props.__slot__) {
        const {
          portals: r,
          clonedElement: c
        } = H(n.props.el);
        return I.cloneElement(n, {
          ...n.props,
          el: c,
          children: [...I.Children.toArray(n.props.children), ...r]
        });
      }
      return null;
    });
    return o.originalChildren = t._reactElement.props.children, e.push(A(I.cloneElement(t._reactElement, {
      ...t._reactElement.props,
      children: o
    }), l)), {
      clonedElement: l,
      portals: e
    };
  }
  Object.keys(t.getEventListeners()).forEach((o) => {
    t.getEventListeners(o).forEach(({
      listener: r,
      type: c,
      useCapture: a
    }) => {
      l.addEventListener(c, r, a);
    });
  });
  const s = Array.from(t.childNodes);
  for (let o = 0; o < s.length; o++) {
    const n = s[o];
    if (n.nodeType === 1) {
      const {
        clonedElement: r,
        portals: c
      } = H(n);
      e.push(...c), l.appendChild(r);
    } else n.nodeType === 3 && l.appendChild(n.cloneNode());
  }
  return {
    clonedElement: l,
    portals: e
  };
}
function st(t, e) {
  t && (typeof t == "function" ? t(e) : t.current = e);
}
const j = ae(({
  slot: t,
  clone: e,
  className: l,
  style: s,
  observeAttributes: o
}, n) => {
  const r = de(), [c, a] = ue([]), {
    forceClone: h
  } = we(), _ = h ? !0 : e;
  return fe(() => {
    var v;
    if (!r.current || !t)
      return;
    let i = t;
    function w() {
      let d = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (d = i.children[0], d.tagName.toLowerCase() === "react-portal-target" && d.children[0] && (d = d.children[0])), st(n, d), l && d.classList.add(...l.split(" ")), s) {
        const m = ot(s);
        Object.keys(m).forEach((x) => {
          d.style[x] = m[x];
        });
      }
    }
    let f = null, g = null;
    if (_ && window.MutationObserver) {
      let d = function() {
        var u, E, p;
        (u = r.current) != null && u.contains(i) && ((E = r.current) == null || E.removeChild(i));
        const {
          portals: x,
          clonedElement: C
        } = H(t);
        i = C, a(x), i.style.display = "contents", g && clearTimeout(g), g = setTimeout(() => {
          w();
        }, 50), (p = r.current) == null || p.appendChild(i);
      };
      d();
      const m = ke(() => {
        d(), f == null || f.disconnect(), f == null || f.observe(t, {
          childList: !0,
          subtree: !0,
          attributes: o
        });
      }, 50);
      f = new window.MutationObserver(m), f.observe(t, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      i.style.display = "contents", w(), (v = r.current) == null || v.appendChild(i);
    return () => {
      var d, m;
      i.style.display = "", (d = r.current) != null && d.contains(i) && ((m = r.current) == null || m.removeChild(i)), f == null || f.disconnect();
    };
  }, [t, _, l, s, n, o, h]), I.createElement("react-child", {
    ref: r,
    style: {
      display: "contents"
    }
  }, ...c);
}), ct = ({
  children: t,
  ...e
}) => /* @__PURE__ */ b.jsx(b.Fragment, {
  children: t(e)
});
function ie(t) {
  return I.createElement(ct, {
    children: t
  });
}
function U(t, e, l) {
  const s = t.filter(Boolean);
  if (s.length !== 0)
    return s.map((o, n) => {
      var h;
      if (typeof o != "object")
        return e != null && e.fallback ? e.fallback(o) : o;
      const r = {
        ...o.props,
        key: ((h = o.props) == null ? void 0 : h.key) ?? (l ? `${l}-${n}` : `${n}`)
      };
      let c = r;
      Object.keys(o.slots).forEach((_) => {
        if (!o.slots[_] || !(o.slots[_] instanceof Element) && !o.slots[_].el)
          return;
        const i = _.split(".");
        i.forEach((m, x) => {
          c[m] || (c[m] = {}), x !== i.length - 1 && (c = r[m]);
        });
        const w = o.slots[_];
        let f, g, v = (e == null ? void 0 : e.clone) ?? !1, d = e == null ? void 0 : e.forceClone;
        w instanceof Element ? f = w : (f = w.el, g = w.callback, v = w.clone ?? v, d = w.forceClone ?? d), d = d ?? !!g, c[i[i.length - 1]] = f ? g ? (...m) => (g(i[i.length - 1], m), /* @__PURE__ */ b.jsx(M, {
          ...o.ctx,
          params: m,
          forceClone: d,
          children: /* @__PURE__ */ b.jsx(j, {
            slot: f,
            clone: v
          })
        })) : ie((m) => /* @__PURE__ */ b.jsx(M, {
          ...o.ctx,
          forceClone: d,
          children: /* @__PURE__ */ b.jsx(j, {
            ...m,
            slot: f,
            clone: v
          })
        })) : c[i[i.length - 1]], c = r;
      });
      const a = (e == null ? void 0 : e.children) || "children";
      return o[a] ? r[a] = U(o[a], e, `${n}`) : e != null && e.children && (r[a] = void 0, Reflect.deleteProperty(r, a)), r;
    });
}
function L(t, e) {
  return t ? e != null && e.forceClone || e != null && e.params ? ie((l) => /* @__PURE__ */ b.jsx(M, {
    forceClone: e == null ? void 0 : e.forceClone,
    params: e == null ? void 0 : e.params,
    children: /* @__PURE__ */ b.jsx(j, {
      slot: t,
      clone: e == null ? void 0 : e.clone,
      ...l
    })
  })) : /* @__PURE__ */ b.jsx(j, {
    slot: t,
    clone: e == null ? void 0 : e.clone
  }) : null;
}
function R({
  key: t,
  slots: e,
  targets: l
}, s) {
  return e[t] ? (...o) => l ? l.map((n, r) => /* @__PURE__ */ b.jsx(I.Fragment, {
    children: L(n, {
      clone: !0,
      params: o,
      forceClone: (s == null ? void 0 : s.forceClone) ?? !0
    })
  }, r)) : /* @__PURE__ */ b.jsx(b.Fragment, {
    children: L(e[t], {
      clone: !0,
      params: o,
      forceClone: (s == null ? void 0 : s.forceClone) ?? !0
    })
  }) : void 0;
}
const {
  useItems: it,
  withItemsContextProvider: at,
  ItemHandler: mt
} = te("antd-menu-items"), {
  useItems: pt,
  withItemsContextProvider: ht,
  ItemHandler: dt
} = te("antd-breadcrumb-items"), _t = tt(at(["menu.items", "dropdownProps.menu.items"], ({
  setSlotParams: t,
  itemSlots: e,
  ...l
}) => {
  const {
    items: {
      "menu.items": s,
      "dropdownProps.menu.items": o
    }
  } = it();
  return /* @__PURE__ */ b.jsx(dt, {
    ...l,
    itemProps: (n) => {
      var h, _, i, w, f, g, v, d, m, x, C, u;
      const r = {
        ...n.menu || {},
        items: (h = n.menu) != null && h.items || s.length > 0 ? U(s, {
          clone: !0
        }) : void 0,
        expandIcon: R({
          slots: e,
          key: "menu.expandIcon"
        }, {}) || ((_ = n.menu) == null ? void 0 : _.expandIcon),
        overflowedIndicator: L(e["menu.overflowedIndicator"]) || ((i = n.menu) == null ? void 0 : i.overflowedIndicator)
      }, c = {
        ...((w = n.dropdownProps) == null ? void 0 : w.menu) || {},
        items: (g = (f = n.dropdownProps) == null ? void 0 : f.menu) != null && g.items || o.length > 0 ? U(o, {
          clone: !0
        }) : void 0,
        expandIcon: R({
          slots: e,
          key: "dropdownProps.menu.expandIcon"
        }, {}) || ((d = (v = n.dropdownProps) == null ? void 0 : v.menu) == null ? void 0 : d.expandIcon),
        overflowedIndicator: L(e["dropdownProps.menu.overflowedIndicator"]) || ((x = (m = n.dropdownProps) == null ? void 0 : m.menu) == null ? void 0 : x.overflowedIndicator)
      }, a = {
        ...n.dropdownProps || {},
        dropdownRender: e["dropdownProps.dropdownRender"] ? R({
          slots: e,
          key: "dropdownProps.dropdownRender"
        }, {}) : ee((C = n.dropdownProps) == null ? void 0 : C.dropdownRender),
        popupRender: e["dropdownProps.popupRender"] ? R({
          slots: e,
          key: "dropdownProps.popupRender"
        }, {}) : ee((u = n.dropdownProps) == null ? void 0 : u.popupRender),
        menu: Object.values(c).filter(Boolean).length > 0 ? c : void 0
      };
      return {
        ...n,
        menu: Object.values(r).filter(Boolean).length > 0 ? r : void 0,
        dropdownProps: Object.values(a).filter(Boolean).length > 0 ? a : void 0
      };
    }
  });
}));
export {
  _t as BreadcrumbItem,
  _t as default
};
