import { i as me, a as W, r as pe, w as k, g as he, c as G } from "./Index-O5ykJ4uC.js";
const b = window.ms_globals.React, ae = window.ms_globals.React.forwardRef, de = window.ms_globals.React.useRef, ue = window.ms_globals.React.useState, fe = window.ms_globals.React.useEffect, A = window.ms_globals.ReactDOM.createPortal, _e = window.ms_globals.internalContext.useContextPropsContext, F = window.ms_globals.internalContext.ContextPropsProvider, R = window.ms_globals.createItemsContext.createItemsContext;
var we = /\s/;
function ge(t) {
  for (var e = t.length; e-- && we.test(t.charAt(e)); )
    ;
  return e;
}
var xe = /^\s+/;
function Ie(t) {
  return t && t.slice(0, ge(t) + 1).replace(xe, "");
}
var q = NaN, Ce = /^[-+]0x[0-9a-f]+$/i, be = /^0b[01]+$/i, ve = /^0o[0-7]+$/i, Ee = parseInt;
function V(t) {
  if (typeof t == "number")
    return t;
  if (me(t))
    return q;
  if (W(t)) {
    var e = typeof t.valueOf == "function" ? t.valueOf() : t;
    t = W(e) ? e + "" : e;
  }
  if (typeof t != "string")
    return t === 0 ? t : +t;
  t = Ie(t);
  var o = be.test(t);
  return o || ve.test(t) ? Ee(t.slice(2), o ? 2 : 8) : Ce.test(t) ? q : +t;
}
var L = function() {
  return pe.Date.now();
}, ye = "Expected a function", Pe = Math.max, Se = Math.min;
function Re(t, e, o) {
  var s, r, n, l, c, a, h = 0, _ = !1, i = !1, w = !0;
  if (typeof t != "function")
    throw new TypeError(ye);
  e = V(e) || 0, W(o) && (_ = !!o.leading, i = "maxWait" in o, n = i ? Pe(V(o.maxWait) || 0, e) : n, w = "trailing" in o ? !!o.trailing : w);
  function d(p) {
    var v = s, S = r;
    return s = r = void 0, h = p, l = t.apply(S, v), l;
  }
  function g(p) {
    return h = p, c = setTimeout(m, e), _ ? d(p) : l;
  }
  function x(p) {
    var v = p - a, S = p - h, z = e - v;
    return i ? Se(z, n - S) : z;
  }
  function u(p) {
    var v = p - a, S = p - h;
    return a === void 0 || v >= e || v < 0 || i && S >= n;
  }
  function m() {
    var p = L();
    if (u(p))
      return C(p);
    c = setTimeout(m, x(p));
  }
  function C(p) {
    return c = void 0, w && s ? d(p) : (s = r = void 0, l);
  }
  function P() {
    c !== void 0 && clearTimeout(c), h = 0, s = a = r = c = void 0;
  }
  function f() {
    return c === void 0 ? l : C(L());
  }
  function E() {
    var p = L(), v = u(p);
    if (s = arguments, r = this, a = p, v) {
      if (c === void 0)
        return g(a);
      if (i)
        return clearTimeout(c), c = setTimeout(m, e), d(a);
    }
    return c === void 0 && (c = setTimeout(m, e)), l;
  }
  return E.cancel = P, E.flush = f, E;
}
var te = {
  exports: {}
}, j = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var ke = b, Oe = Symbol.for("react.element"), Te = Symbol.for("react.fragment"), De = Object.prototype.hasOwnProperty, je = ke.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, Le = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function re(t, e, o) {
  var s, r = {}, n = null, l = null;
  o !== void 0 && (n = "" + o), e.key !== void 0 && (n = "" + e.key), e.ref !== void 0 && (l = e.ref);
  for (s in e) De.call(e, s) && !Le.hasOwnProperty(s) && (r[s] = e[s]);
  if (t && t.defaultProps) for (s in e = t.defaultProps, e) r[s] === void 0 && (r[s] = e[s]);
  return {
    $$typeof: Oe,
    type: t,
    key: n,
    ref: l,
    props: r,
    _owner: je.current
  };
}
j.Fragment = Te;
j.jsx = re;
j.jsxs = re;
te.exports = j;
var I = te.exports;
const {
  SvelteComponent: Ne,
  assign: J,
  binding_callbacks: X,
  check_outros: He,
  children: ne,
  claim_element: le,
  claim_space: Ae,
  component_subscribe: Y,
  compute_slots: We,
  create_slot: Fe,
  detach: y,
  element: oe,
  empty: K,
  exclude_internal_props: Q,
  get_all_dirty_from_scope: Me,
  get_slot_changes: Be,
  group_outros: Ue,
  init: ze,
  insert_hydration: O,
  safe_not_equal: Ge,
  set_custom_element_data: se,
  space: qe,
  transition_in: T,
  transition_out: M,
  update_slot_base: Ve
} = window.__gradio__svelte__internal, {
  beforeUpdate: Je,
  getContext: Xe,
  onDestroy: Ye,
  setContext: Ke
} = window.__gradio__svelte__internal;
function Z(t) {
  let e, o;
  const s = (
    /*#slots*/
    t[7].default
  ), r = Fe(
    s,
    t,
    /*$$scope*/
    t[6],
    null
  );
  return {
    c() {
      e = oe("svelte-slot"), r && r.c(), this.h();
    },
    l(n) {
      e = le(n, "SVELTE-SLOT", {
        class: !0
      });
      var l = ne(e);
      r && r.l(l), l.forEach(y), this.h();
    },
    h() {
      se(e, "class", "svelte-1rt0kpf");
    },
    m(n, l) {
      O(n, e, l), r && r.m(e, null), t[9](e), o = !0;
    },
    p(n, l) {
      r && r.p && (!o || l & /*$$scope*/
      64) && Ve(
        r,
        s,
        n,
        /*$$scope*/
        n[6],
        o ? Be(
          s,
          /*$$scope*/
          n[6],
          l,
          null
        ) : Me(
          /*$$scope*/
          n[6]
        ),
        null
      );
    },
    i(n) {
      o || (T(r, n), o = !0);
    },
    o(n) {
      M(r, n), o = !1;
    },
    d(n) {
      n && y(e), r && r.d(n), t[9](null);
    }
  };
}
function Qe(t) {
  let e, o, s, r, n = (
    /*$$slots*/
    t[4].default && Z(t)
  );
  return {
    c() {
      e = oe("react-portal-target"), o = qe(), n && n.c(), s = K(), this.h();
    },
    l(l) {
      e = le(l, "REACT-PORTAL-TARGET", {
        class: !0
      }), ne(e).forEach(y), o = Ae(l), n && n.l(l), s = K(), this.h();
    },
    h() {
      se(e, "class", "svelte-1rt0kpf");
    },
    m(l, c) {
      O(l, e, c), t[8](e), O(l, o, c), n && n.m(l, c), O(l, s, c), r = !0;
    },
    p(l, [c]) {
      /*$$slots*/
      l[4].default ? n ? (n.p(l, c), c & /*$$slots*/
      16 && T(n, 1)) : (n = Z(l), n.c(), T(n, 1), n.m(s.parentNode, s)) : n && (Ue(), M(n, 1, 1, () => {
        n = null;
      }), He());
    },
    i(l) {
      r || (T(n), r = !0);
    },
    o(l) {
      M(n), r = !1;
    },
    d(l) {
      l && (y(e), y(o), y(s)), t[8](null), n && n.d(l);
    }
  };
}
function $(t) {
  const {
    svelteInit: e,
    ...o
  } = t;
  return o;
}
function Ze(t, e, o) {
  let s, r, {
    $$slots: n = {},
    $$scope: l
  } = e;
  const c = We(n);
  let {
    svelteInit: a
  } = e;
  const h = k($(e)), _ = k();
  Y(t, _, (f) => o(0, s = f));
  const i = k();
  Y(t, i, (f) => o(1, r = f));
  const w = [], d = Xe("$$ms-gr-react-wrapper"), {
    slotKey: g,
    slotIndex: x,
    subSlotIndex: u
  } = he() || {}, m = a({
    parent: d,
    props: h,
    target: _,
    slot: i,
    slotKey: g,
    slotIndex: x,
    subSlotIndex: u,
    onDestroy(f) {
      w.push(f);
    }
  });
  Ke("$$ms-gr-react-wrapper", m), Je(() => {
    h.set($(e));
  }), Ye(() => {
    w.forEach((f) => f());
  });
  function C(f) {
    X[f ? "unshift" : "push"](() => {
      s = f, _.set(s);
    });
  }
  function P(f) {
    X[f ? "unshift" : "push"](() => {
      r = f, i.set(r);
    });
  }
  return t.$$set = (f) => {
    o(17, e = J(J({}, e), Q(f))), "svelteInit" in f && o(5, a = f.svelteInit), "$$scope" in f && o(6, l = f.$$scope);
  }, e = Q(e), [s, r, _, i, c, a, l, n, C, P];
}
class $e extends Ne {
  constructor(e) {
    super(), ze(this, e, Ze, Qe, Ge, {
      svelteInit: 5
    });
  }
}
const {
  SvelteComponent: dt
} = window.__gradio__svelte__internal, ee = window.ms_globals.rerender, N = window.ms_globals.tree;
function et(t, e = {}) {
  function o(s) {
    const r = k(), n = new $e({
      ...s,
      props: {
        svelteInit(l) {
          window.ms_globals.autokey += 1;
          const c = {
            key: window.ms_globals.autokey,
            svelteInstance: r,
            reactComponent: t,
            props: l.props,
            slot: l.slot,
            target: l.target,
            slotIndex: l.slotIndex,
            subSlotIndex: l.subSlotIndex,
            ignore: e.ignore,
            slotKey: l.slotKey,
            nodes: []
          }, a = l.parent ?? N;
          return a.nodes = [...a.nodes, c], ee({
            createPortal: A,
            node: N
          }), l.onDestroy(() => {
            a.nodes = a.nodes.filter((h) => h.svelteInstance !== r), ee({
              createPortal: A,
              node: N
            });
          }), c;
        },
        ...s.props
      }
    });
    return r.set(n), n;
  }
  return new Promise((s) => {
    window.ms_globals.initializePromise.then(() => {
      s(o);
    });
  });
}
const tt = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function rt(t) {
  return t ? Object.keys(t).reduce((e, o) => {
    const s = t[o];
    return e[o] = nt(o, s), e;
  }, {}) : {};
}
function nt(t, e) {
  return typeof e == "number" && !tt.includes(t) ? e + "px" : e;
}
function B(t) {
  const e = [], o = t.cloneNode(!1);
  if (t._reactElement) {
    const r = b.Children.toArray(t._reactElement.props.children).map((n) => {
      if (b.isValidElement(n) && n.props.__slot__) {
        const {
          portals: l,
          clonedElement: c
        } = B(n.props.el);
        return b.cloneElement(n, {
          ...n.props,
          el: c,
          children: [...b.Children.toArray(n.props.children), ...l]
        });
      }
      return null;
    });
    return r.originalChildren = t._reactElement.props.children, e.push(A(b.cloneElement(t._reactElement, {
      ...t._reactElement.props,
      children: r
    }), o)), {
      clonedElement: o,
      portals: e
    };
  }
  Object.keys(t.getEventListeners()).forEach((r) => {
    t.getEventListeners(r).forEach(({
      listener: l,
      type: c,
      useCapture: a
    }) => {
      o.addEventListener(c, l, a);
    });
  });
  const s = Array.from(t.childNodes);
  for (let r = 0; r < s.length; r++) {
    const n = s[r];
    if (n.nodeType === 1) {
      const {
        clonedElement: l,
        portals: c
      } = B(n);
      e.push(...c), o.appendChild(l);
    } else n.nodeType === 3 && o.appendChild(n.cloneNode());
  }
  return {
    clonedElement: o,
    portals: e
  };
}
function lt(t, e) {
  t && (typeof t == "function" ? t(e) : t.current = e);
}
const D = ae(({
  slot: t,
  clone: e,
  className: o,
  style: s,
  observeAttributes: r
}, n) => {
  const l = de(), [c, a] = ue([]), {
    forceClone: h
  } = _e(), _ = h ? !0 : e;
  return fe(() => {
    var x;
    if (!l.current || !t)
      return;
    let i = t;
    function w() {
      let u = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (u = i.children[0], u.tagName.toLowerCase() === "react-portal-target" && u.children[0] && (u = u.children[0])), lt(n, u), o && u.classList.add(...o.split(" ")), s) {
        const m = rt(s);
        Object.keys(m).forEach((C) => {
          u.style[C] = m[C];
        });
      }
    }
    let d = null, g = null;
    if (_ && window.MutationObserver) {
      let u = function() {
        var f, E, p;
        (f = l.current) != null && f.contains(i) && ((E = l.current) == null || E.removeChild(i));
        const {
          portals: C,
          clonedElement: P
        } = B(t);
        i = P, a(C), i.style.display = "contents", g && clearTimeout(g), g = setTimeout(() => {
          w();
        }, 50), (p = l.current) == null || p.appendChild(i);
      };
      u();
      const m = Re(() => {
        u(), d == null || d.disconnect(), d == null || d.observe(t, {
          childList: !0,
          subtree: !0,
          attributes: r
        });
      }, 50);
      d = new window.MutationObserver(m), d.observe(t, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      i.style.display = "contents", w(), (x = l.current) == null || x.appendChild(i);
    return () => {
      var u, m;
      i.style.display = "", (u = l.current) != null && u.contains(i) && ((m = l.current) == null || m.removeChild(i)), d == null || d.disconnect();
    };
  }, [t, _, o, s, n, r, h]), b.createElement("react-child", {
    ref: l,
    style: {
      display: "contents"
    }
  }, ...c);
}), ot = ({
  children: t,
  ...e
}) => /* @__PURE__ */ I.jsx(I.Fragment, {
  children: t(e)
});
function ce(t) {
  return b.createElement(ot, {
    children: t
  });
}
function ie(t, e, o) {
  const s = t.filter(Boolean);
  if (s.length !== 0)
    return s.map((r, n) => {
      var h;
      if (typeof r != "object")
        return e != null && e.fallback ? e.fallback(r) : r;
      const l = {
        ...r.props,
        key: ((h = r.props) == null ? void 0 : h.key) ?? (o ? `${o}-${n}` : `${n}`)
      };
      let c = l;
      Object.keys(r.slots).forEach((_) => {
        if (!r.slots[_] || !(r.slots[_] instanceof Element) && !r.slots[_].el)
          return;
        const i = _.split(".");
        i.forEach((m, C) => {
          c[m] || (c[m] = {}), C !== i.length - 1 && (c = l[m]);
        });
        const w = r.slots[_];
        let d, g, x = (e == null ? void 0 : e.clone) ?? !1, u = e == null ? void 0 : e.forceClone;
        w instanceof Element ? d = w : (d = w.el, g = w.callback, x = w.clone ?? x, u = w.forceClone ?? u), u = u ?? !!g, c[i[i.length - 1]] = d ? g ? (...m) => (g(i[i.length - 1], m), /* @__PURE__ */ I.jsx(F, {
          ...r.ctx,
          params: m,
          forceClone: u,
          children: /* @__PURE__ */ I.jsx(D, {
            slot: d,
            clone: x
          })
        })) : ce((m) => /* @__PURE__ */ I.jsx(F, {
          ...r.ctx,
          forceClone: u,
          children: /* @__PURE__ */ I.jsx(D, {
            ...m,
            slot: d,
            clone: x
          })
        })) : c[i[i.length - 1]], c = l;
      });
      const a = (e == null ? void 0 : e.children) || "children";
      return r[a] ? l[a] = ie(r[a], e, `${n}`) : e != null && e.children && (l[a] = void 0, Reflect.deleteProperty(l, a)), l;
    });
}
function U(t, e) {
  return t ? e != null && e.forceClone || e != null && e.params ? ce((o) => /* @__PURE__ */ I.jsx(F, {
    forceClone: e == null ? void 0 : e.forceClone,
    params: e == null ? void 0 : e.params,
    children: /* @__PURE__ */ I.jsx(D, {
      slot: t,
      clone: e == null ? void 0 : e.clone,
      ...o
    })
  })) : /* @__PURE__ */ I.jsx(D, {
    slot: t,
    clone: e == null ? void 0 : e.clone
  }) : null;
}
function H({
  key: t,
  slots: e,
  targets: o
}, s) {
  return e[t] ? (...r) => o ? o.map((n, l) => /* @__PURE__ */ I.jsx(b.Fragment, {
    children: U(n, {
      clone: !0,
      params: r,
      forceClone: (s == null ? void 0 : s.forceClone) ?? !0
    })
  }, l)) : /* @__PURE__ */ I.jsx(I.Fragment, {
    children: U(e[t], {
      clone: !0,
      params: r,
      forceClone: (s == null ? void 0 : s.forceClone) ?? !0
    })
  }) : void 0;
}
const {
  useItems: st,
  withItemsContextProvider: ct,
  ItemHandler: ut
} = R("antd-menu-items"), {
  useItems: ft,
  withItemsContextProvider: mt,
  ItemHandler: it
} = R("antd-table-columns"), {
  useItems: pt,
  withItemsContextProvider: ht,
  ItemHandler: _t
} = R("antd-table-row-selection-selections"), {
  useItems: wt,
  withItemsContextProvider: gt,
  ItemHandler: xt
} = R("antd-table-row-selection"), {
  useItems: It,
  withItemsContextProvider: Ct,
  ItemHandler: bt
} = R("antd-table-expandable"), vt = et(ct(["filterDropdownProps.menu.items"], ({
  setSlotParams: t,
  itemSlots: e,
  ...o
}) => {
  const {
    items: {
      "filterDropdownProps.menu.items": s
    }
  } = st();
  return /* @__PURE__ */ I.jsx(it, {
    ...o,
    itemProps: (r) => {
      var c, a, h, _, i, w, d, g, x;
      const n = {
        ...((c = r.filterDropdownProps) == null ? void 0 : c.menu) || {},
        items: (h = (a = r.filterDropdownProps) == null ? void 0 : a.menu) != null && h.items || s.length > 0 ? ie(s, {
          clone: !0
        }) : void 0,
        expandIcon: H({
          slots: e,
          key: "filterDropdownProps.menu.expandIcon"
        }, {}) || ((i = (_ = r.filterDropdownProps) == null ? void 0 : _.menu) == null ? void 0 : i.expandIcon),
        overflowedIndicator: U(e["filterDropdownProps.menu.overflowedIndicator"]) || ((d = (w = r.filterDropdownProps) == null ? void 0 : w.menu) == null ? void 0 : d.overflowedIndicator)
      }, l = {
        ...r.filterDropdownProps || {},
        dropdownRender: e["filterDropdownProps.dropdownRender"] ? H({
          slots: e,
          key: "filterDropdownProps.dropdownRender"
        }, {}) : G((g = r.filterDropdownProps) == null ? void 0 : g.dropdownRender),
        popupRender: e["filterDropdownProps.popupRender"] ? H({
          slots: e,
          key: "filterDropdownProps.popupRender"
        }, {}) : G((x = r.filterDropdownProps) == null ? void 0 : x.popupRender),
        menu: Object.values(n).filter(Boolean).length > 0 ? n : void 0
      };
      return {
        ...r,
        filterDropdownProps: Object.values(l).filter(Boolean).length > 0 ? l : void 0
      };
    }
  });
}));
export {
  vt as TableColumn,
  vt as default
};
