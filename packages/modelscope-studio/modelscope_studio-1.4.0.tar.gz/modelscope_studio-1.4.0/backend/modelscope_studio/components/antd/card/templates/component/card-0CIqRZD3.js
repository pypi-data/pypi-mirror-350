import { i as de, a as B, r as fe, w as k, g as pe, d as me, b as R } from "./Index-DUf4wzsH.js";
const w = window.ms_globals.React, F = window.ms_globals.React.useMemo, ee = window.ms_globals.React.useState, te = window.ms_globals.React.useEffect, ce = window.ms_globals.React.forwardRef, ue = window.ms_globals.React.useRef, W = window.ms_globals.ReactDOM.createPortal, _e = window.ms_globals.internalContext.useContextPropsContext, G = window.ms_globals.internalContext.ContextPropsProvider, H = window.ms_globals.antd.Card, he = window.ms_globals.createItemsContext.createItemsContext;
var ge = /\s/;
function xe(e) {
  for (var t = e.length; t-- && ge.test(e.charAt(t)); )
    ;
  return t;
}
var be = /^\s+/;
function Ce(e) {
  return e && e.slice(0, xe(e) + 1).replace(be, "");
}
var z = NaN, Ee = /^[-+]0x[0-9a-f]+$/i, we = /^0b[01]+$/i, ve = /^0o[0-7]+$/i, ye = parseInt;
function V(e) {
  if (typeof e == "number")
    return e;
  if (de(e))
    return z;
  if (B(e)) {
    var t = typeof e.valueOf == "function" ? e.valueOf() : e;
    e = B(t) ? t + "" : t;
  }
  if (typeof e != "string")
    return e === 0 ? e : +e;
  e = Ce(e);
  var s = we.test(e);
  return s || ve.test(e) ? ye(e.slice(2), s ? 2 : 8) : Ee.test(e) ? z : +e;
}
var A = function() {
  return fe.Date.now();
}, Ie = "Expected a function", Se = Math.max, Te = Math.min;
function Oe(e, t, s) {
  var l, o, n, r, i, c, _ = 0, h = !1, a = !1, g = !0;
  if (typeof e != "function")
    throw new TypeError(Ie);
  t = V(t) || 0, B(s) && (h = !!s.leading, a = "maxWait" in s, n = a ? Se(V(s.maxWait) || 0, t) : n, g = "trailing" in s ? !!s.trailing : g);
  function f(m) {
    var v = l, O = o;
    return l = o = void 0, _ = m, r = e.apply(O, v), r;
  }
  function b(m) {
    return _ = m, i = setTimeout(p, t), h ? f(m) : r;
  }
  function C(m) {
    var v = m - c, O = m - _, U = t - v;
    return a ? Te(U, n - O) : U;
  }
  function u(m) {
    var v = m - c, O = m - _;
    return c === void 0 || v >= t || v < 0 || a && O >= n;
  }
  function p() {
    var m = A();
    if (u(m))
      return E(m);
    i = setTimeout(p, C(m));
  }
  function E(m) {
    return i = void 0, g && l ? f(m) : (l = o = void 0, r);
  }
  function T() {
    i !== void 0 && clearTimeout(i), _ = 0, l = c = o = i = void 0;
  }
  function d() {
    return i === void 0 ? r : E(A());
  }
  function I() {
    var m = A(), v = u(m);
    if (l = arguments, o = this, c = m, v) {
      if (i === void 0)
        return b(c);
      if (a)
        return clearTimeout(i), i = setTimeout(p, t), f(c);
    }
    return i === void 0 && (i = setTimeout(p, t)), r;
  }
  return I.cancel = T, I.flush = d, I;
}
var ne = {
  exports: {}
}, L = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var Re = w, ke = Symbol.for("react.element"), Pe = Symbol.for("react.fragment"), je = Object.prototype.hasOwnProperty, Le = Re.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, Ae = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function re(e, t, s) {
  var l, o = {}, n = null, r = null;
  s !== void 0 && (n = "" + s), t.key !== void 0 && (n = "" + t.key), t.ref !== void 0 && (r = t.ref);
  for (l in t) je.call(t, l) && !Ae.hasOwnProperty(l) && (o[l] = t[l]);
  if (e && e.defaultProps) for (l in t = e.defaultProps, t) o[l] === void 0 && (o[l] = t[l]);
  return {
    $$typeof: ke,
    type: e,
    key: n,
    ref: r,
    props: o,
    _owner: Le.current
  };
}
L.Fragment = Pe;
L.jsx = re;
L.jsxs = re;
ne.exports = L;
var x = ne.exports;
const {
  SvelteComponent: Ne,
  assign: q,
  binding_callbacks: J,
  check_outros: We,
  children: oe,
  claim_element: se,
  claim_space: Be,
  component_subscribe: X,
  compute_slots: Me,
  create_slot: De,
  detach: S,
  element: le,
  empty: Y,
  exclude_internal_props: K,
  get_all_dirty_from_scope: Fe,
  get_slot_changes: Ue,
  group_outros: Ge,
  init: He,
  insert_hydration: P,
  safe_not_equal: ze,
  set_custom_element_data: ie,
  space: Ve,
  transition_in: j,
  transition_out: M,
  update_slot_base: qe
} = window.__gradio__svelte__internal, {
  beforeUpdate: Je,
  getContext: Xe,
  onDestroy: Ye,
  setContext: Ke
} = window.__gradio__svelte__internal;
function Q(e) {
  let t, s;
  const l = (
    /*#slots*/
    e[7].default
  ), o = De(
    l,
    e,
    /*$$scope*/
    e[6],
    null
  );
  return {
    c() {
      t = le("svelte-slot"), o && o.c(), this.h();
    },
    l(n) {
      t = se(n, "SVELTE-SLOT", {
        class: !0
      });
      var r = oe(t);
      o && o.l(r), r.forEach(S), this.h();
    },
    h() {
      ie(t, "class", "svelte-1rt0kpf");
    },
    m(n, r) {
      P(n, t, r), o && o.m(t, null), e[9](t), s = !0;
    },
    p(n, r) {
      o && o.p && (!s || r & /*$$scope*/
      64) && qe(
        o,
        l,
        n,
        /*$$scope*/
        n[6],
        s ? Ue(
          l,
          /*$$scope*/
          n[6],
          r,
          null
        ) : Fe(
          /*$$scope*/
          n[6]
        ),
        null
      );
    },
    i(n) {
      s || (j(o, n), s = !0);
    },
    o(n) {
      M(o, n), s = !1;
    },
    d(n) {
      n && S(t), o && o.d(n), e[9](null);
    }
  };
}
function Qe(e) {
  let t, s, l, o, n = (
    /*$$slots*/
    e[4].default && Q(e)
  );
  return {
    c() {
      t = le("react-portal-target"), s = Ve(), n && n.c(), l = Y(), this.h();
    },
    l(r) {
      t = se(r, "REACT-PORTAL-TARGET", {
        class: !0
      }), oe(t).forEach(S), s = Be(r), n && n.l(r), l = Y(), this.h();
    },
    h() {
      ie(t, "class", "svelte-1rt0kpf");
    },
    m(r, i) {
      P(r, t, i), e[8](t), P(r, s, i), n && n.m(r, i), P(r, l, i), o = !0;
    },
    p(r, [i]) {
      /*$$slots*/
      r[4].default ? n ? (n.p(r, i), i & /*$$slots*/
      16 && j(n, 1)) : (n = Q(r), n.c(), j(n, 1), n.m(l.parentNode, l)) : n && (Ge(), M(n, 1, 1, () => {
        n = null;
      }), We());
    },
    i(r) {
      o || (j(n), o = !0);
    },
    o(r) {
      M(n), o = !1;
    },
    d(r) {
      r && (S(t), S(s), S(l)), e[8](null), n && n.d(r);
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
function Ze(e, t, s) {
  let l, o, {
    $$slots: n = {},
    $$scope: r
  } = t;
  const i = Me(n);
  let {
    svelteInit: c
  } = t;
  const _ = k(Z(t)), h = k();
  X(e, h, (d) => s(0, l = d));
  const a = k();
  X(e, a, (d) => s(1, o = d));
  const g = [], f = Xe("$$ms-gr-react-wrapper"), {
    slotKey: b,
    slotIndex: C,
    subSlotIndex: u
  } = pe() || {}, p = c({
    parent: f,
    props: _,
    target: h,
    slot: a,
    slotKey: b,
    slotIndex: C,
    subSlotIndex: u,
    onDestroy(d) {
      g.push(d);
    }
  });
  Ke("$$ms-gr-react-wrapper", p), Je(() => {
    _.set(Z(t));
  }), Ye(() => {
    g.forEach((d) => d());
  });
  function E(d) {
    J[d ? "unshift" : "push"](() => {
      l = d, h.set(l);
    });
  }
  function T(d) {
    J[d ? "unshift" : "push"](() => {
      o = d, a.set(o);
    });
  }
  return e.$$set = (d) => {
    s(17, t = q(q({}, t), K(d))), "svelteInit" in d && s(5, c = d.svelteInit), "$$scope" in d && s(6, r = d.$$scope);
  }, t = K(t), [l, o, h, a, i, c, r, n, E, T];
}
class $e extends Ne {
  constructor(t) {
    super(), He(this, t, Ze, Qe, ze, {
      svelteInit: 5
    });
  }
}
const {
  SvelteComponent: pt
} = window.__gradio__svelte__internal, $ = window.ms_globals.rerender, N = window.ms_globals.tree;
function et(e, t = {}) {
  function s(l) {
    const o = k(), n = new $e({
      ...l,
      props: {
        svelteInit(r) {
          window.ms_globals.autokey += 1;
          const i = {
            key: window.ms_globals.autokey,
            svelteInstance: o,
            reactComponent: e,
            props: r.props,
            slot: r.slot,
            target: r.target,
            slotIndex: r.slotIndex,
            subSlotIndex: r.subSlotIndex,
            ignore: t.ignore,
            slotKey: r.slotKey,
            nodes: []
          }, c = r.parent ?? N;
          return c.nodes = [...c.nodes, i], $({
            createPortal: W,
            node: N
          }), r.onDestroy(() => {
            c.nodes = c.nodes.filter((_) => _.svelteInstance !== o), $({
              createPortal: W,
              node: N
            });
          }), i;
        },
        ...l.props
      }
    });
    return o.set(n), n;
  }
  return new Promise((l) => {
    window.ms_globals.initializePromise.then(() => {
      l(s);
    });
  });
}
function tt(e) {
  const [t, s] = ee(() => R(e));
  return te(() => {
    let l = !0;
    return e.subscribe((n) => {
      l && (l = !1, n === t) || s(n);
    });
  }, [e]), t;
}
function nt(e) {
  const t = F(() => me(e, (s) => s), [e]);
  return tt(t);
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
function D(e) {
  const t = [], s = e.cloneNode(!1);
  if (e._reactElement) {
    const o = w.Children.toArray(e._reactElement.props.children).map((n) => {
      if (w.isValidElement(n) && n.props.__slot__) {
        const {
          portals: r,
          clonedElement: i
        } = D(n.props.el);
        return w.cloneElement(n, {
          ...n.props,
          el: i,
          children: [...w.Children.toArray(n.props.children), ...r]
        });
      }
      return null;
    });
    return o.originalChildren = e._reactElement.props.children, t.push(W(w.cloneElement(e._reactElement, {
      ...e._reactElement.props,
      children: o
    }), s)), {
      clonedElement: s,
      portals: t
    };
  }
  Object.keys(e.getEventListeners()).forEach((o) => {
    e.getEventListeners(o).forEach(({
      listener: r,
      type: i,
      useCapture: c
    }) => {
      s.addEventListener(i, r, c);
    });
  });
  const l = Array.from(e.childNodes);
  for (let o = 0; o < l.length; o++) {
    const n = l[o];
    if (n.nodeType === 1) {
      const {
        clonedElement: r,
        portals: i
      } = D(n);
      t.push(...i), s.appendChild(r);
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
const y = ce(({
  slot: e,
  clone: t,
  className: s,
  style: l,
  observeAttributes: o
}, n) => {
  const r = ue(), [i, c] = ee([]), {
    forceClone: _
  } = _e(), h = _ ? !0 : t;
  return te(() => {
    var C;
    if (!r.current || !e)
      return;
    let a = e;
    function g() {
      let u = a;
      if (a.tagName.toLowerCase() === "svelte-slot" && a.children.length === 1 && a.children[0] && (u = a.children[0], u.tagName.toLowerCase() === "react-portal-target" && u.children[0] && (u = u.children[0])), lt(n, u), s && u.classList.add(...s.split(" ")), l) {
        const p = ot(l);
        Object.keys(p).forEach((E) => {
          u.style[E] = p[E];
        });
      }
    }
    let f = null, b = null;
    if (h && window.MutationObserver) {
      let u = function() {
        var d, I, m;
        (d = r.current) != null && d.contains(a) && ((I = r.current) == null || I.removeChild(a));
        const {
          portals: E,
          clonedElement: T
        } = D(e);
        a = T, c(E), a.style.display = "contents", b && clearTimeout(b), b = setTimeout(() => {
          g();
        }, 50), (m = r.current) == null || m.appendChild(a);
      };
      u();
      const p = Oe(() => {
        u(), f == null || f.disconnect(), f == null || f.observe(e, {
          childList: !0,
          subtree: !0,
          attributes: o
        });
      }, 50);
      f = new window.MutationObserver(p), f.observe(e, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      a.style.display = "contents", g(), (C = r.current) == null || C.appendChild(a);
    return () => {
      var u, p;
      a.style.display = "", (u = r.current) != null && u.contains(a) && ((p = r.current) == null || p.removeChild(a)), f == null || f.disconnect();
    };
  }, [e, h, s, l, n, o, _]), w.createElement("react-child", {
    ref: r,
    style: {
      display: "contents"
    }
  }, ...i);
});
function it(e, t) {
  const s = F(() => w.Children.toArray(e.originalChildren || e).filter((n) => n.props.node && !n.props.node.ignore && t === n.props.nodeSlotKey).sort((n, r) => {
    if (n.props.node.slotIndex && r.props.node.slotIndex) {
      const i = R(n.props.node.slotIndex) || 0, c = R(r.props.node.slotIndex) || 0;
      return i - c === 0 && n.props.node.subSlotIndex && r.props.node.subSlotIndex ? (R(n.props.node.subSlotIndex) || 0) - (R(r.props.node.subSlotIndex) || 0) : i - c;
    }
    return 0;
  }).map((n) => n.props.node.target), [e, t]);
  return nt(s);
}
const at = ({
  children: e,
  ...t
}) => /* @__PURE__ */ x.jsx(x.Fragment, {
  children: e(t)
});
function ct(e) {
  return w.createElement(at, {
    children: e
  });
}
function ae(e, t, s) {
  const l = e.filter(Boolean);
  if (l.length !== 0)
    return l.map((o, n) => {
      var _;
      if (typeof o != "object")
        return o;
      const r = {
        ...o.props,
        key: ((_ = o.props) == null ? void 0 : _.key) ?? (s ? `${s}-${n}` : `${n}`)
      };
      let i = r;
      Object.keys(o.slots).forEach((h) => {
        if (!o.slots[h] || !(o.slots[h] instanceof Element) && !o.slots[h].el)
          return;
        const a = h.split(".");
        a.forEach((p, E) => {
          i[p] || (i[p] = {}), E !== a.length - 1 && (i = r[p]);
        });
        const g = o.slots[h];
        let f, b, C = !1, u = t == null ? void 0 : t.forceClone;
        g instanceof Element ? f = g : (f = g.el, b = g.callback, C = g.clone ?? C, u = g.forceClone ?? u), u = u ?? !!b, i[a[a.length - 1]] = f ? b ? (...p) => (b(a[a.length - 1], p), /* @__PURE__ */ x.jsx(G, {
          ...o.ctx,
          params: p,
          forceClone: u,
          children: /* @__PURE__ */ x.jsx(y, {
            slot: f,
            clone: C
          })
        })) : ct((p) => /* @__PURE__ */ x.jsx(G, {
          ...o.ctx,
          forceClone: u,
          children: /* @__PURE__ */ x.jsx(y, {
            ...p,
            slot: f,
            clone: C
          })
        })) : i[a[a.length - 1]], i = r;
      });
      const c = "children";
      return o[c] && (r[c] = ae(o[c], t, `${n}`)), r;
    });
}
const {
  withItemsContextProvider: ut,
  useItems: dt,
  ItemHandler: mt
} = he("antd-tabs-items"), _t = et(ut(["tabList"], ({
  children: e,
  containsGrid: t,
  slots: s,
  tabList: l,
  tabProps: o,
  ...n
}) => {
  const r = it(e, "actions"), {
    items: {
      tabList: i
    }
  } = dt();
  return /* @__PURE__ */ x.jsxs(H, {
    ...n,
    tabProps: o,
    tabList: F(() => l || ae(i), [l, i]),
    title: s.title ? /* @__PURE__ */ x.jsx(y, {
      slot: s.title
    }) : n.title,
    extra: s.extra ? /* @__PURE__ */ x.jsx(y, {
      slot: s.extra
    }) : n.extra,
    cover: s.cover ? /* @__PURE__ */ x.jsx(y, {
      slot: s.cover
    }) : n.cover,
    tabBarExtraContent: s.tabBarExtraContent ? /* @__PURE__ */ x.jsx(y, {
      slot: s.tabBarExtraContent
    }) : n.tabBarExtraContent,
    actions: r.length > 0 ? r.map((c, _) => /* @__PURE__ */ x.jsx(y, {
      slot: c
    }, _)) : n.actions,
    children: [t ? /* @__PURE__ */ x.jsx(H.Grid, {
      style: {
        display: "none"
      }
    }) : null, e]
  });
}));
export {
  _t as Card,
  _t as default
};
