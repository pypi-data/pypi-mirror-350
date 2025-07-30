import { i as pe, a as B, r as he, w as j, g as ge, d as xe, b as P, c as we } from "./Index-CJUrFNvR.js";
const v = window.ms_globals.React, A = window.ms_globals.React.useMemo, re = window.ms_globals.React.useState, oe = window.ms_globals.React.useEffect, me = window.ms_globals.React.forwardRef, _e = window.ms_globals.React.useRef, M = window.ms_globals.ReactDOM.createPortal, be = window.ms_globals.internalContext.useContextPropsContext, U = window.ms_globals.internalContext.ContextPropsProvider, Ce = window.ms_globals.antd.Dropdown, ve = window.ms_globals.createItemsContext.createItemsContext;
var Ie = /\s/;
function ye(t) {
  for (var e = t.length; e-- && Ie.test(t.charAt(e)); )
    ;
  return e;
}
var Ee = /^\s+/;
function Se(t) {
  return t && t.slice(0, ye(t) + 1).replace(Ee, "");
}
var V = NaN, Re = /^[-+]0x[0-9a-f]+$/i, ke = /^0b[01]+$/i, Pe = /^0o[0-7]+$/i, Te = parseInt;
function q(t) {
  if (typeof t == "number")
    return t;
  if (pe(t))
    return V;
  if (B(t)) {
    var e = typeof t.valueOf == "function" ? t.valueOf() : t;
    t = B(e) ? e + "" : e;
  }
  if (typeof t != "string")
    return t === 0 ? t : +t;
  t = Se(t);
  var o = ke.test(t);
  return o || Pe.test(t) ? Te(t.slice(2), o ? 2 : 8) : Re.test(t) ? V : +t;
}
var W = function() {
  return he.Date.now();
}, Oe = "Expected a function", je = Math.max, Fe = Math.min;
function Le(t, e, o) {
  var s, l, n, r, c, i, p = 0, h = !1, a = !1, g = !0;
  if (typeof t != "function")
    throw new TypeError(Oe);
  e = q(e) || 0, B(o) && (h = !!o.leading, a = "maxWait" in o, n = a ? je(q(o.maxWait) || 0, e) : n, g = "trailing" in o ? !!o.trailing : g);
  function d(_) {
    var y = s, k = l;
    return s = l = void 0, p = _, r = t.apply(k, y), r;
  }
  function w(_) {
    return p = _, c = setTimeout(f, e), h ? d(_) : r;
  }
  function b(_) {
    var y = _ - i, k = _ - p, G = e - y;
    return a ? Fe(G, n - k) : G;
  }
  function u(_) {
    var y = _ - i, k = _ - p;
    return i === void 0 || y >= e || y < 0 || a && k >= n;
  }
  function f() {
    var _ = W();
    if (u(_))
      return C(_);
    c = setTimeout(f, b(_));
  }
  function C(_) {
    return c = void 0, g && s ? d(_) : (s = l = void 0, r);
  }
  function I() {
    c !== void 0 && clearTimeout(c), p = 0, s = i = l = c = void 0;
  }
  function m() {
    return c === void 0 ? r : C(W());
  }
  function E() {
    var _ = W(), y = u(_);
    if (s = arguments, l = this, i = _, y) {
      if (c === void 0)
        return w(i);
      if (a)
        return clearTimeout(c), c = setTimeout(f, e), d(i);
    }
    return c === void 0 && (c = setTimeout(f, e)), r;
  }
  return E.cancel = I, E.flush = m, E;
}
var le = {
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
var Ae = v, Ne = Symbol.for("react.element"), We = Symbol.for("react.fragment"), De = Object.prototype.hasOwnProperty, Me = Ae.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, Be = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function se(t, e, o) {
  var s, l = {}, n = null, r = null;
  o !== void 0 && (n = "" + o), e.key !== void 0 && (n = "" + e.key), e.ref !== void 0 && (r = e.ref);
  for (s in e) De.call(e, s) && !Be.hasOwnProperty(s) && (l[s] = e[s]);
  if (t && t.defaultProps) for (s in e = t.defaultProps, e) l[s] === void 0 && (l[s] = e[s]);
  return {
    $$typeof: Ne,
    type: t,
    key: n,
    ref: r,
    props: l,
    _owner: Me.current
  };
}
N.Fragment = We;
N.jsx = se;
N.jsxs = se;
le.exports = N;
var x = le.exports;
const {
  SvelteComponent: Ue,
  assign: J,
  binding_callbacks: X,
  check_outros: He,
  children: ce,
  claim_element: ie,
  claim_space: ze,
  component_subscribe: Y,
  compute_slots: Ge,
  create_slot: Ve,
  detach: S,
  element: ae,
  empty: Q,
  exclude_internal_props: Z,
  get_all_dirty_from_scope: qe,
  get_slot_changes: Je,
  group_outros: Xe,
  init: Ye,
  insert_hydration: F,
  safe_not_equal: Qe,
  set_custom_element_data: ue,
  space: Ze,
  transition_in: L,
  transition_out: H,
  update_slot_base: Ke
} = window.__gradio__svelte__internal, {
  beforeUpdate: $e,
  getContext: et,
  onDestroy: tt,
  setContext: nt
} = window.__gradio__svelte__internal;
function K(t) {
  let e, o;
  const s = (
    /*#slots*/
    t[7].default
  ), l = Ve(
    s,
    t,
    /*$$scope*/
    t[6],
    null
  );
  return {
    c() {
      e = ae("svelte-slot"), l && l.c(), this.h();
    },
    l(n) {
      e = ie(n, "SVELTE-SLOT", {
        class: !0
      });
      var r = ce(e);
      l && l.l(r), r.forEach(S), this.h();
    },
    h() {
      ue(e, "class", "svelte-1rt0kpf");
    },
    m(n, r) {
      F(n, e, r), l && l.m(e, null), t[9](e), o = !0;
    },
    p(n, r) {
      l && l.p && (!o || r & /*$$scope*/
      64) && Ke(
        l,
        s,
        n,
        /*$$scope*/
        n[6],
        o ? Je(
          s,
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
      H(l, n), o = !1;
    },
    d(n) {
      n && S(e), l && l.d(n), t[9](null);
    }
  };
}
function rt(t) {
  let e, o, s, l, n = (
    /*$$slots*/
    t[4].default && K(t)
  );
  return {
    c() {
      e = ae("react-portal-target"), o = Ze(), n && n.c(), s = Q(), this.h();
    },
    l(r) {
      e = ie(r, "REACT-PORTAL-TARGET", {
        class: !0
      }), ce(e).forEach(S), o = ze(r), n && n.l(r), s = Q(), this.h();
    },
    h() {
      ue(e, "class", "svelte-1rt0kpf");
    },
    m(r, c) {
      F(r, e, c), t[8](e), F(r, o, c), n && n.m(r, c), F(r, s, c), l = !0;
    },
    p(r, [c]) {
      /*$$slots*/
      r[4].default ? n ? (n.p(r, c), c & /*$$slots*/
      16 && L(n, 1)) : (n = K(r), n.c(), L(n, 1), n.m(s.parentNode, s)) : n && (Xe(), H(n, 1, 1, () => {
        n = null;
      }), He());
    },
    i(r) {
      l || (L(n), l = !0);
    },
    o(r) {
      H(n), l = !1;
    },
    d(r) {
      r && (S(e), S(o), S(s)), t[8](null), n && n.d(r);
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
function ot(t, e, o) {
  let s, l, {
    $$slots: n = {},
    $$scope: r
  } = e;
  const c = Ge(n);
  let {
    svelteInit: i
  } = e;
  const p = j($(e)), h = j();
  Y(t, h, (m) => o(0, s = m));
  const a = j();
  Y(t, a, (m) => o(1, l = m));
  const g = [], d = et("$$ms-gr-react-wrapper"), {
    slotKey: w,
    slotIndex: b,
    subSlotIndex: u
  } = ge() || {}, f = i({
    parent: d,
    props: p,
    target: h,
    slot: a,
    slotKey: w,
    slotIndex: b,
    subSlotIndex: u,
    onDestroy(m) {
      g.push(m);
    }
  });
  nt("$$ms-gr-react-wrapper", f), $e(() => {
    p.set($(e));
  }), tt(() => {
    g.forEach((m) => m());
  });
  function C(m) {
    X[m ? "unshift" : "push"](() => {
      s = m, h.set(s);
    });
  }
  function I(m) {
    X[m ? "unshift" : "push"](() => {
      l = m, a.set(l);
    });
  }
  return t.$$set = (m) => {
    o(17, e = J(J({}, e), Z(m))), "svelteInit" in m && o(5, i = m.svelteInit), "$$scope" in m && o(6, r = m.$$scope);
  }, e = Z(e), [s, l, h, a, c, i, r, n, C, I];
}
class lt extends Ue {
  constructor(e) {
    super(), Ye(this, e, ot, rt, Qe, {
      svelteInit: 5
    });
  }
}
const {
  SvelteComponent: wt
} = window.__gradio__svelte__internal, ee = window.ms_globals.rerender, D = window.ms_globals.tree;
function st(t, e = {}) {
  function o(s) {
    const l = j(), n = new lt({
      ...s,
      props: {
        svelteInit(r) {
          window.ms_globals.autokey += 1;
          const c = {
            key: window.ms_globals.autokey,
            svelteInstance: l,
            reactComponent: t,
            props: r.props,
            slot: r.slot,
            target: r.target,
            slotIndex: r.slotIndex,
            subSlotIndex: r.subSlotIndex,
            ignore: e.ignore,
            slotKey: r.slotKey,
            nodes: []
          }, i = r.parent ?? D;
          return i.nodes = [...i.nodes, c], ee({
            createPortal: M,
            node: D
          }), r.onDestroy(() => {
            i.nodes = i.nodes.filter((p) => p.svelteInstance !== l), ee({
              createPortal: M,
              node: D
            });
          }), c;
        },
        ...s.props
      }
    });
    return l.set(n), n;
  }
  return new Promise((s) => {
    window.ms_globals.initializePromise.then(() => {
      s(o);
    });
  });
}
function ct(t) {
  const [e, o] = re(() => P(t));
  return oe(() => {
    let s = !0;
    return t.subscribe((n) => {
      s && (s = !1, n === e) || o(n);
    });
  }, [t]), e;
}
function it(t) {
  const e = A(() => xe(t, (o) => o), [t]);
  return ct(e);
}
const at = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function ut(t) {
  return t ? Object.keys(t).reduce((e, o) => {
    const s = t[o];
    return e[o] = dt(o, s), e;
  }, {}) : {};
}
function dt(t, e) {
  return typeof e == "number" && !at.includes(t) ? e + "px" : e;
}
function z(t) {
  const e = [], o = t.cloneNode(!1);
  if (t._reactElement) {
    const l = v.Children.toArray(t._reactElement.props.children).map((n) => {
      if (v.isValidElement(n) && n.props.__slot__) {
        const {
          portals: r,
          clonedElement: c
        } = z(n.props.el);
        return v.cloneElement(n, {
          ...n.props,
          el: c,
          children: [...v.Children.toArray(n.props.children), ...r]
        });
      }
      return null;
    });
    return l.originalChildren = t._reactElement.props.children, e.push(M(v.cloneElement(t._reactElement, {
      ...t._reactElement.props,
      children: l
    }), o)), {
      clonedElement: o,
      portals: e
    };
  }
  Object.keys(t.getEventListeners()).forEach((l) => {
    t.getEventListeners(l).forEach(({
      listener: r,
      type: c,
      useCapture: i
    }) => {
      o.addEventListener(c, r, i);
    });
  });
  const s = Array.from(t.childNodes);
  for (let l = 0; l < s.length; l++) {
    const n = s[l];
    if (n.nodeType === 1) {
      const {
        clonedElement: r,
        portals: c
      } = z(n);
      e.push(...c), o.appendChild(r);
    } else n.nodeType === 3 && o.appendChild(n.cloneNode());
  }
  return {
    clonedElement: o,
    portals: e
  };
}
function ft(t, e) {
  t && (typeof t == "function" ? t(e) : t.current = e);
}
const R = me(({
  slot: t,
  clone: e,
  className: o,
  style: s,
  observeAttributes: l
}, n) => {
  const r = _e(), [c, i] = re([]), {
    forceClone: p
  } = be(), h = p ? !0 : e;
  return oe(() => {
    var b;
    if (!r.current || !t)
      return;
    let a = t;
    function g() {
      let u = a;
      if (a.tagName.toLowerCase() === "svelte-slot" && a.children.length === 1 && a.children[0] && (u = a.children[0], u.tagName.toLowerCase() === "react-portal-target" && u.children[0] && (u = u.children[0])), ft(n, u), o && u.classList.add(...o.split(" ")), s) {
        const f = ut(s);
        Object.keys(f).forEach((C) => {
          u.style[C] = f[C];
        });
      }
    }
    let d = null, w = null;
    if (h && window.MutationObserver) {
      let u = function() {
        var m, E, _;
        (m = r.current) != null && m.contains(a) && ((E = r.current) == null || E.removeChild(a));
        const {
          portals: C,
          clonedElement: I
        } = z(t);
        a = I, i(C), a.style.display = "contents", w && clearTimeout(w), w = setTimeout(() => {
          g();
        }, 50), (_ = r.current) == null || _.appendChild(a);
      };
      u();
      const f = Le(() => {
        u(), d == null || d.disconnect(), d == null || d.observe(t, {
          childList: !0,
          subtree: !0,
          attributes: l
        });
      }, 50);
      d = new window.MutationObserver(f), d.observe(t, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      a.style.display = "contents", g(), (b = r.current) == null || b.appendChild(a);
    return () => {
      var u, f;
      a.style.display = "", (u = r.current) != null && u.contains(a) && ((f = r.current) == null || f.removeChild(a)), d == null || d.disconnect();
    };
  }, [t, h, o, s, n, l, p]), v.createElement("react-child", {
    ref: r,
    style: {
      display: "contents"
    }
  }, ...c);
});
function mt(t) {
  return /^(?:async\s+)?(?:function\s*(?:\w*\s*)?\(|\([\w\s,=]*\)\s*=>|\(\{[\w\s,=]*\}\)\s*=>|function\s*\*\s*\w*\s*\()/i.test(t.trim());
}
function _t(t, e = !1) {
  try {
    if (we(t))
      return t;
    if (e && !mt(t))
      return;
    if (typeof t == "string") {
      let o = t.trim();
      return o.startsWith(";") && (o = o.slice(1)), o.endsWith(";") && (o = o.slice(0, -1)), new Function(`return (...args) => (${o})(...args)`)();
    }
    return;
  } catch {
    return;
  }
}
function T(t, e) {
  return A(() => _t(t, e), [t, e]);
}
function te(t, e) {
  const o = A(() => v.Children.toArray(t.originalChildren || t).filter((n) => n.props.node && !n.props.node.ignore && (!e && !n.props.nodeSlotKey || e && e === n.props.nodeSlotKey)).sort((n, r) => {
    if (n.props.node.slotIndex && r.props.node.slotIndex) {
      const c = P(n.props.node.slotIndex) || 0, i = P(r.props.node.slotIndex) || 0;
      return c - i === 0 && n.props.node.subSlotIndex && r.props.node.subSlotIndex ? (P(n.props.node.subSlotIndex) || 0) - (P(r.props.node.subSlotIndex) || 0) : c - i;
    }
    return 0;
  }).map((n) => n.props.node.target), [t, e]);
  return it(o);
}
const pt = ({
  children: t,
  ...e
}) => /* @__PURE__ */ x.jsx(x.Fragment, {
  children: t(e)
});
function de(t) {
  return v.createElement(pt, {
    children: t
  });
}
function fe(t, e, o) {
  const s = t.filter(Boolean);
  if (s.length !== 0)
    return s.map((l, n) => {
      var p;
      if (typeof l != "object")
        return e != null && e.fallback ? e.fallback(l) : l;
      const r = {
        ...l.props,
        key: ((p = l.props) == null ? void 0 : p.key) ?? (o ? `${o}-${n}` : `${n}`)
      };
      let c = r;
      Object.keys(l.slots).forEach((h) => {
        if (!l.slots[h] || !(l.slots[h] instanceof Element) && !l.slots[h].el)
          return;
        const a = h.split(".");
        a.forEach((f, C) => {
          c[f] || (c[f] = {}), C !== a.length - 1 && (c = r[f]);
        });
        const g = l.slots[h];
        let d, w, b = (e == null ? void 0 : e.clone) ?? !1, u = e == null ? void 0 : e.forceClone;
        g instanceof Element ? d = g : (d = g.el, w = g.callback, b = g.clone ?? b, u = g.forceClone ?? u), u = u ?? !!w, c[a[a.length - 1]] = d ? w ? (...f) => (w(a[a.length - 1], f), /* @__PURE__ */ x.jsx(U, {
          ...l.ctx,
          params: f,
          forceClone: u,
          children: /* @__PURE__ */ x.jsx(R, {
            slot: d,
            clone: b
          })
        })) : de((f) => /* @__PURE__ */ x.jsx(U, {
          ...l.ctx,
          forceClone: u,
          children: /* @__PURE__ */ x.jsx(R, {
            ...f,
            slot: d,
            clone: b
          })
        })) : c[a[a.length - 1]], c = r;
      });
      const i = (e == null ? void 0 : e.children) || "children";
      return l[i] ? r[i] = fe(l[i], e, `${n}`) : e != null && e.children && (r[i] = void 0, Reflect.deleteProperty(r, i)), r;
    });
}
function ne(t, e) {
  return t ? e != null && e.forceClone || e != null && e.params ? de((o) => /* @__PURE__ */ x.jsx(U, {
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
function O({
  key: t,
  slots: e,
  targets: o
}, s) {
  return e[t] ? (...l) => o ? o.map((n, r) => /* @__PURE__ */ x.jsx(v.Fragment, {
    children: ne(n, {
      clone: !0,
      params: l,
      forceClone: (s == null ? void 0 : s.forceClone) ?? !0
    })
  }, r)) : /* @__PURE__ */ x.jsx(x.Fragment, {
    children: ne(e[t], {
      clone: !0,
      params: l,
      forceClone: (s == null ? void 0 : s.forceClone) ?? !0
    })
  }) : void 0;
}
const {
  useItems: ht,
  withItemsContextProvider: gt,
  ItemHandler: bt
} = ve("antd-menu-items"), Ct = st(gt(["menu.items"], ({
  getPopupContainer: t,
  slots: e,
  children: o,
  dropdownRender: s,
  popupRender: l,
  buttonsRender: n,
  setSlotParams: r,
  value: c,
  ...i
}) => {
  var u, f, C;
  const p = T(t), h = T(s), a = T(n), g = T(l), d = te(o, "buttonsRender"), w = te(o), {
    items: {
      "menu.items": b
    }
  } = ht();
  return /* @__PURE__ */ x.jsxs(x.Fragment, {
    children: [/* @__PURE__ */ x.jsx("div", {
      style: {
        display: "none"
      },
      children: w.length > 0 ? null : o
    }), /* @__PURE__ */ x.jsx(Ce.Button, {
      ...i,
      buttonsRender: d.length ? O({
        key: "buttonsRender",
        slots: e,
        targets: d
      }) : a,
      menu: {
        ...i.menu,
        items: A(() => {
          var I;
          return ((I = i.menu) == null ? void 0 : I.items) || fe(b, {
            clone: !0
          }) || [];
        }, [b, (u = i.menu) == null ? void 0 : u.items]),
        expandIcon: e["menu.expandIcon"] ? O({
          slots: e,
          key: "menu.expandIcon"
        }, {}) : (f = i.menu) == null ? void 0 : f.expandIcon,
        overflowedIndicator: e["menu.overflowedIndicator"] ? /* @__PURE__ */ x.jsx(R, {
          slot: e["menu.overflowedIndicator"]
        }) : (C = i.menu) == null ? void 0 : C.overflowedIndicator
      },
      getPopupContainer: p,
      dropdownRender: e.dropdownRender ? O({
        slots: e,
        key: "dropdownRender"
      }) : h,
      popupRender: e.popupRender ? O({
        slots: e,
        key: "popupRender"
      }, {}) : g,
      icon: e.icon ? /* @__PURE__ */ x.jsx(R, {
        slot: e.icon
      }) : i.icon,
      children: w.length > 0 ? o : c
    })]
  });
}));
export {
  Ct as DropdownButton,
  Ct as default
};
