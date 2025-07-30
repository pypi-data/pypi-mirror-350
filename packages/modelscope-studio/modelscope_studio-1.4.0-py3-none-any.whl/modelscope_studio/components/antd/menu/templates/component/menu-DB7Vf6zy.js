import { i as de, a as M, r as fe, w as k, g as me } from "./Index-c4He3_16.js";
const C = window.ms_globals.React, oe = window.ms_globals.React.forwardRef, ce = window.ms_globals.React.useRef, ae = window.ms_globals.React.useState, ie = window.ms_globals.React.useEffect, ue = window.ms_globals.React.useMemo, A = window.ms_globals.ReactDOM.createPortal, _e = window.ms_globals.internalContext.useContextPropsContext, W = window.ms_globals.internalContext.ContextPropsProvider, he = window.ms_globals.antd.Menu, ge = window.ms_globals.createItemsContext.createItemsContext;
var xe = /\s/;
function be(t) {
  for (var e = t.length; e-- && xe.test(t.charAt(e)); )
    ;
  return e;
}
var we = /^\s+/;
function pe(t) {
  return t && t.slice(0, be(t) + 1).replace(we, "");
}
var H = NaN, ve = /^[-+]0x[0-9a-f]+$/i, Ce = /^0b[01]+$/i, Ee = /^0o[0-7]+$/i, Ie = parseInt;
function z(t) {
  if (typeof t == "number")
    return t;
  if (de(t))
    return H;
  if (M(t)) {
    var e = typeof t.valueOf == "function" ? t.valueOf() : t;
    t = M(e) ? e + "" : e;
  }
  if (typeof t != "string")
    return t === 0 ? t : +t;
  t = pe(t);
  var o = Ce.test(t);
  return o || Ee.test(t) ? Ie(t.slice(2), o ? 2 : 8) : ve.test(t) ? H : +t;
}
var L = function() {
  return fe.Date.now();
}, ye = "Expected a function", Se = Math.max, Pe = Math.min;
function Re(t, e, o) {
  var s, l, r, n, c, i, g = 0, _ = !1, a = !1, b = !0;
  if (typeof t != "function")
    throw new TypeError(ye);
  e = z(e) || 0, M(o) && (_ = !!o.leading, a = "maxWait" in o, r = a ? Se(z(o.maxWait) || 0, e) : r, b = "trailing" in o ? !!o.trailing : b);
  function f(h) {
    var E = s, P = l;
    return s = l = void 0, g = h, n = t.apply(P, E), n;
  }
  function w(h) {
    return g = h, c = setTimeout(m, e), _ ? f(h) : n;
  }
  function p(h) {
    var E = h - i, P = h - g, B = e - E;
    return a ? Pe(B, r - P) : B;
  }
  function u(h) {
    var E = h - i, P = h - g;
    return i === void 0 || E >= e || E < 0 || a && P >= r;
  }
  function m() {
    var h = L();
    if (u(h))
      return v(h);
    c = setTimeout(m, p(h));
  }
  function v(h) {
    return c = void 0, b && s ? f(h) : (s = l = void 0, n);
  }
  function S() {
    c !== void 0 && clearTimeout(c), g = 0, s = i = l = c = void 0;
  }
  function d() {
    return c === void 0 ? n : v(L());
  }
  function I() {
    var h = L(), E = u(h);
    if (s = arguments, l = this, i = h, E) {
      if (c === void 0)
        return w(i);
      if (a)
        return clearTimeout(c), c = setTimeout(m, e), f(i);
    }
    return c === void 0 && (c = setTimeout(m, e)), n;
  }
  return I.cancel = S, I.flush = d, I;
}
var Z = {
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
var ke = C, Te = Symbol.for("react.element"), Oe = Symbol.for("react.fragment"), je = Object.prototype.hasOwnProperty, Le = ke.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, Ne = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function $(t, e, o) {
  var s, l = {}, r = null, n = null;
  o !== void 0 && (r = "" + o), e.key !== void 0 && (r = "" + e.key), e.ref !== void 0 && (n = e.ref);
  for (s in e) je.call(e, s) && !Ne.hasOwnProperty(s) && (l[s] = e[s]);
  if (t && t.defaultProps) for (s in e = t.defaultProps, e) l[s] === void 0 && (l[s] = e[s]);
  return {
    $$typeof: Te,
    type: t,
    key: r,
    ref: n,
    props: l,
    _owner: Le.current
  };
}
j.Fragment = Oe;
j.jsx = $;
j.jsxs = $;
Z.exports = j;
var x = Z.exports;
const {
  SvelteComponent: Ae,
  assign: D,
  binding_callbacks: G,
  check_outros: Me,
  children: ee,
  claim_element: te,
  claim_space: We,
  component_subscribe: q,
  compute_slots: Fe,
  create_slot: Ue,
  detach: y,
  element: re,
  empty: V,
  exclude_internal_props: J,
  get_all_dirty_from_scope: Be,
  get_slot_changes: He,
  group_outros: ze,
  init: De,
  insert_hydration: T,
  safe_not_equal: Ge,
  set_custom_element_data: ne,
  space: qe,
  transition_in: O,
  transition_out: F,
  update_slot_base: Ve
} = window.__gradio__svelte__internal, {
  beforeUpdate: Je,
  getContext: Xe,
  onDestroy: Ye,
  setContext: Ke
} = window.__gradio__svelte__internal;
function X(t) {
  let e, o;
  const s = (
    /*#slots*/
    t[7].default
  ), l = Ue(
    s,
    t,
    /*$$scope*/
    t[6],
    null
  );
  return {
    c() {
      e = re("svelte-slot"), l && l.c(), this.h();
    },
    l(r) {
      e = te(r, "SVELTE-SLOT", {
        class: !0
      });
      var n = ee(e);
      l && l.l(n), n.forEach(y), this.h();
    },
    h() {
      ne(e, "class", "svelte-1rt0kpf");
    },
    m(r, n) {
      T(r, e, n), l && l.m(e, null), t[9](e), o = !0;
    },
    p(r, n) {
      l && l.p && (!o || n & /*$$scope*/
      64) && Ve(
        l,
        s,
        r,
        /*$$scope*/
        r[6],
        o ? He(
          s,
          /*$$scope*/
          r[6],
          n,
          null
        ) : Be(
          /*$$scope*/
          r[6]
        ),
        null
      );
    },
    i(r) {
      o || (O(l, r), o = !0);
    },
    o(r) {
      F(l, r), o = !1;
    },
    d(r) {
      r && y(e), l && l.d(r), t[9](null);
    }
  };
}
function Qe(t) {
  let e, o, s, l, r = (
    /*$$slots*/
    t[4].default && X(t)
  );
  return {
    c() {
      e = re("react-portal-target"), o = qe(), r && r.c(), s = V(), this.h();
    },
    l(n) {
      e = te(n, "REACT-PORTAL-TARGET", {
        class: !0
      }), ee(e).forEach(y), o = We(n), r && r.l(n), s = V(), this.h();
    },
    h() {
      ne(e, "class", "svelte-1rt0kpf");
    },
    m(n, c) {
      T(n, e, c), t[8](e), T(n, o, c), r && r.m(n, c), T(n, s, c), l = !0;
    },
    p(n, [c]) {
      /*$$slots*/
      n[4].default ? r ? (r.p(n, c), c & /*$$slots*/
      16 && O(r, 1)) : (r = X(n), r.c(), O(r, 1), r.m(s.parentNode, s)) : r && (ze(), F(r, 1, 1, () => {
        r = null;
      }), Me());
    },
    i(n) {
      l || (O(r), l = !0);
    },
    o(n) {
      F(r), l = !1;
    },
    d(n) {
      n && (y(e), y(o), y(s)), t[8](null), r && r.d(n);
    }
  };
}
function Y(t) {
  const {
    svelteInit: e,
    ...o
  } = t;
  return o;
}
function Ze(t, e, o) {
  let s, l, {
    $$slots: r = {},
    $$scope: n
  } = e;
  const c = Fe(r);
  let {
    svelteInit: i
  } = e;
  const g = k(Y(e)), _ = k();
  q(t, _, (d) => o(0, s = d));
  const a = k();
  q(t, a, (d) => o(1, l = d));
  const b = [], f = Xe("$$ms-gr-react-wrapper"), {
    slotKey: w,
    slotIndex: p,
    subSlotIndex: u
  } = me() || {}, m = i({
    parent: f,
    props: g,
    target: _,
    slot: a,
    slotKey: w,
    slotIndex: p,
    subSlotIndex: u,
    onDestroy(d) {
      b.push(d);
    }
  });
  Ke("$$ms-gr-react-wrapper", m), Je(() => {
    g.set(Y(e));
  }), Ye(() => {
    b.forEach((d) => d());
  });
  function v(d) {
    G[d ? "unshift" : "push"](() => {
      s = d, _.set(s);
    });
  }
  function S(d) {
    G[d ? "unshift" : "push"](() => {
      l = d, a.set(l);
    });
  }
  return t.$$set = (d) => {
    o(17, e = D(D({}, e), J(d))), "svelteInit" in d && o(5, i = d.svelteInit), "$$scope" in d && o(6, n = d.$$scope);
  }, e = J(e), [s, l, _, a, c, i, n, r, v, S];
}
class $e extends Ae {
  constructor(e) {
    super(), De(this, e, Ze, Qe, Ge, {
      svelteInit: 5
    });
  }
}
const {
  SvelteComponent: dt
} = window.__gradio__svelte__internal, K = window.ms_globals.rerender, N = window.ms_globals.tree;
function et(t, e = {}) {
  function o(s) {
    const l = k(), r = new $e({
      ...s,
      props: {
        svelteInit(n) {
          window.ms_globals.autokey += 1;
          const c = {
            key: window.ms_globals.autokey,
            svelteInstance: l,
            reactComponent: t,
            props: n.props,
            slot: n.slot,
            target: n.target,
            slotIndex: n.slotIndex,
            subSlotIndex: n.subSlotIndex,
            ignore: e.ignore,
            slotKey: n.slotKey,
            nodes: []
          }, i = n.parent ?? N;
          return i.nodes = [...i.nodes, c], K({
            createPortal: A,
            node: N
          }), n.onDestroy(() => {
            i.nodes = i.nodes.filter((g) => g.svelteInstance !== l), K({
              createPortal: A,
              node: N
            });
          }), c;
        },
        ...s.props
      }
    });
    return l.set(r), r;
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
function U(t) {
  const e = [], o = t.cloneNode(!1);
  if (t._reactElement) {
    const l = C.Children.toArray(t._reactElement.props.children).map((r) => {
      if (C.isValidElement(r) && r.props.__slot__) {
        const {
          portals: n,
          clonedElement: c
        } = U(r.props.el);
        return C.cloneElement(r, {
          ...r.props,
          el: c,
          children: [...C.Children.toArray(r.props.children), ...n]
        });
      }
      return null;
    });
    return l.originalChildren = t._reactElement.props.children, e.push(A(C.cloneElement(t._reactElement, {
      ...t._reactElement.props,
      children: l
    }), o)), {
      clonedElement: o,
      portals: e
    };
  }
  Object.keys(t.getEventListeners()).forEach((l) => {
    t.getEventListeners(l).forEach(({
      listener: n,
      type: c,
      useCapture: i
    }) => {
      o.addEventListener(c, n, i);
    });
  });
  const s = Array.from(t.childNodes);
  for (let l = 0; l < s.length; l++) {
    const r = s[l];
    if (r.nodeType === 1) {
      const {
        clonedElement: n,
        portals: c
      } = U(r);
      e.push(...c), o.appendChild(n);
    } else r.nodeType === 3 && o.appendChild(r.cloneNode());
  }
  return {
    clonedElement: o,
    portals: e
  };
}
function lt(t, e) {
  t && (typeof t == "function" ? t(e) : t.current = e);
}
const R = oe(({
  slot: t,
  clone: e,
  className: o,
  style: s,
  observeAttributes: l
}, r) => {
  const n = ce(), [c, i] = ae([]), {
    forceClone: g
  } = _e(), _ = g ? !0 : e;
  return ie(() => {
    var p;
    if (!n.current || !t)
      return;
    let a = t;
    function b() {
      let u = a;
      if (a.tagName.toLowerCase() === "svelte-slot" && a.children.length === 1 && a.children[0] && (u = a.children[0], u.tagName.toLowerCase() === "react-portal-target" && u.children[0] && (u = u.children[0])), lt(r, u), o && u.classList.add(...o.split(" ")), s) {
        const m = rt(s);
        Object.keys(m).forEach((v) => {
          u.style[v] = m[v];
        });
      }
    }
    let f = null, w = null;
    if (_ && window.MutationObserver) {
      let u = function() {
        var d, I, h;
        (d = n.current) != null && d.contains(a) && ((I = n.current) == null || I.removeChild(a));
        const {
          portals: v,
          clonedElement: S
        } = U(t);
        a = S, i(v), a.style.display = "contents", w && clearTimeout(w), w = setTimeout(() => {
          b();
        }, 50), (h = n.current) == null || h.appendChild(a);
      };
      u();
      const m = Re(() => {
        u(), f == null || f.disconnect(), f == null || f.observe(t, {
          childList: !0,
          subtree: !0,
          attributes: l
        });
      }, 50);
      f = new window.MutationObserver(m), f.observe(t, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      a.style.display = "contents", b(), (p = n.current) == null || p.appendChild(a);
    return () => {
      var u, m;
      a.style.display = "", (u = n.current) != null && u.contains(a) && ((m = n.current) == null || m.removeChild(a)), f == null || f.disconnect();
    };
  }, [t, _, o, s, r, l, g]), C.createElement("react-child", {
    ref: n,
    style: {
      display: "contents"
    }
  }, ...c);
});
function st(t, e) {
  return Object.keys(t).reduce((o, s) => (t[s] !== void 0 && (o[s] = t[s]), o), {});
}
const ot = ({
  children: t,
  ...e
}) => /* @__PURE__ */ x.jsx(x.Fragment, {
  children: t(e)
});
function le(t) {
  return C.createElement(ot, {
    children: t
  });
}
function se(t, e, o) {
  const s = t.filter(Boolean);
  if (s.length !== 0)
    return s.map((l, r) => {
      var g;
      if (typeof l != "object")
        return e != null && e.fallback ? e.fallback(l) : l;
      const n = {
        ...l.props,
        key: ((g = l.props) == null ? void 0 : g.key) ?? (o ? `${o}-${r}` : `${r}`)
      };
      let c = n;
      Object.keys(l.slots).forEach((_) => {
        if (!l.slots[_] || !(l.slots[_] instanceof Element) && !l.slots[_].el)
          return;
        const a = _.split(".");
        a.forEach((m, v) => {
          c[m] || (c[m] = {}), v !== a.length - 1 && (c = n[m]);
        });
        const b = l.slots[_];
        let f, w, p = (e == null ? void 0 : e.clone) ?? !1, u = e == null ? void 0 : e.forceClone;
        b instanceof Element ? f = b : (f = b.el, w = b.callback, p = b.clone ?? p, u = b.forceClone ?? u), u = u ?? !!w, c[a[a.length - 1]] = f ? w ? (...m) => (w(a[a.length - 1], m), /* @__PURE__ */ x.jsx(W, {
          ...l.ctx,
          params: m,
          forceClone: u,
          children: /* @__PURE__ */ x.jsx(R, {
            slot: f,
            clone: p
          })
        })) : le((m) => /* @__PURE__ */ x.jsx(W, {
          ...l.ctx,
          forceClone: u,
          children: /* @__PURE__ */ x.jsx(R, {
            ...m,
            slot: f,
            clone: p
          })
        })) : c[a[a.length - 1]], c = n;
      });
      const i = (e == null ? void 0 : e.children) || "children";
      return l[i] ? n[i] = se(l[i], e, `${r}`) : e != null && e.children && (n[i] = void 0, Reflect.deleteProperty(n, i)), n;
    });
}
function Q(t, e) {
  return t ? e != null && e.forceClone || e != null && e.params ? le((o) => /* @__PURE__ */ x.jsx(W, {
    forceClone: e == null ? void 0 : e.forceClone,
    params: e == null ? void 0 : e.params,
    children: /* @__PURE__ */ x.jsx(R, {
      slot: t,
      clone: e == null ? void 0 : e.clone,
      ...o
    })
  })) : /* @__PURE__ */ x.jsx(R, {
    slot: t,
    clone: e == null ? void 0 : e.clone
  }) : null;
}
function ct({
  key: t,
  slots: e,
  targets: o
}, s) {
  return e[t] ? (...l) => o ? o.map((r, n) => /* @__PURE__ */ x.jsx(C.Fragment, {
    children: Q(r, {
      clone: !0,
      params: l,
      forceClone: (s == null ? void 0 : s.forceClone) ?? !0
    })
  }, n)) : /* @__PURE__ */ x.jsx(x.Fragment, {
    children: Q(e[t], {
      clone: !0,
      params: l,
      forceClone: (s == null ? void 0 : s.forceClone) ?? !0
    })
  }) : void 0;
}
const {
  useItems: at,
  withItemsContextProvider: it,
  ItemHandler: ft
} = ge("antd-menu-items"), mt = et(it(["default", "items"], ({
  slots: t,
  items: e,
  children: o,
  onOpenChange: s,
  onSelect: l,
  onDeselect: r,
  setSlotParams: n,
  ...c
}) => {
  const {
    items: i
  } = at(), g = i.items.length > 0 ? i.items : i.default;
  return /* @__PURE__ */ x.jsxs(x.Fragment, {
    children: [/* @__PURE__ */ x.jsx("div", {
      style: {
        display: "none"
      },
      children: o
    }), /* @__PURE__ */ x.jsx(he, {
      ...st(c),
      onOpenChange: (_) => {
        s == null || s(_);
      },
      onSelect: (_) => {
        l == null || l(_);
      },
      onDeselect: (_) => {
        r == null || r(_);
      },
      items: ue(() => e || se(g, {
        clone: !0
      }), [e, g]),
      expandIcon: t.expandIcon ? ct({
        key: "expandIcon",
        slots: t
      }, {}) : c.expandIcon,
      overflowedIndicator: t.overflowedIndicator ? /* @__PURE__ */ x.jsx(R, {
        slot: t.overflowedIndicator
      }) : c.overflowedIndicator
    })]
  });
}));
export {
  mt as Menu,
  mt as default
};
