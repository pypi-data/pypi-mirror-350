import { i as me, a as D, r as _e, w as P, g as he, b as ge } from "./Index-C8YAxz37.js";
const v = window.ms_globals.React, ae = window.ms_globals.React.forwardRef, ue = window.ms_globals.React.useRef, de = window.ms_globals.React.useState, fe = window.ms_globals.React.useEffect, ee = window.ms_globals.React.useMemo, A = window.ms_globals.ReactDOM.createPortal, pe = window.ms_globals.internalContext.useContextPropsContext, M = window.ms_globals.internalContext.ContextPropsProvider, we = window.ms_globals.antd.Dropdown, xe = window.ms_globals.createItemsContext.createItemsContext;
var be = /\s/;
function Ce(t) {
  for (var e = t.length; e-- && be.test(t.charAt(e)); )
    ;
  return e;
}
var ve = /^\s+/;
function ye(t) {
  return t && t.slice(0, Ce(t) + 1).replace(ve, "");
}
var z = NaN, Ee = /^[-+]0x[0-9a-f]+$/i, Ie = /^0b[01]+$/i, Re = /^0o[0-7]+$/i, Se = parseInt;
function G(t) {
  if (typeof t == "number")
    return t;
  if (me(t))
    return z;
  if (D(t)) {
    var e = typeof t.valueOf == "function" ? t.valueOf() : t;
    t = D(e) ? e + "" : e;
  }
  if (typeof t != "string")
    return t === 0 ? t : +t;
  t = ye(t);
  var o = Ie.test(t);
  return o || Re.test(t) ? Se(t.slice(2), o ? 2 : 8) : Ee.test(t) ? z : +t;
}
var F = function() {
  return _e.Date.now();
}, ke = "Expected a function", Pe = Math.max, Oe = Math.min;
function Te(t, e, o) {
  var s, l, n, r, c, a, g = 0, p = !1, i = !1, h = !0;
  if (typeof t != "function")
    throw new TypeError(ke);
  e = G(e) || 0, D(o) && (p = !!o.leading, i = "maxWait" in o, n = i ? Pe(G(o.maxWait) || 0, e) : n, h = "trailing" in o ? !!o.trailing : h);
  function u(_) {
    var y = s, S = l;
    return s = l = void 0, g = _, r = t.apply(S, y), r;
  }
  function x(_) {
    return g = _, c = setTimeout(m, e), p ? u(_) : r;
  }
  function b(_) {
    var y = _ - a, S = _ - g, H = e - y;
    return i ? Oe(H, n - S) : H;
  }
  function d(_) {
    var y = _ - a, S = _ - g;
    return a === void 0 || y >= e || y < 0 || i && S >= n;
  }
  function m() {
    var _ = F();
    if (d(_))
      return C(_);
    c = setTimeout(m, b(_));
  }
  function C(_) {
    return c = void 0, h && s ? u(_) : (s = l = void 0, r);
  }
  function R() {
    c !== void 0 && clearTimeout(c), g = 0, s = a = l = c = void 0;
  }
  function f() {
    return c === void 0 ? r : C(F());
  }
  function E() {
    var _ = F(), y = d(_);
    if (s = arguments, l = this, a = _, y) {
      if (c === void 0)
        return x(a);
      if (i)
        return clearTimeout(c), c = setTimeout(m, e), u(a);
    }
    return c === void 0 && (c = setTimeout(m, e)), r;
  }
  return E.cancel = R, E.flush = f, E;
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
var je = v, Fe = Symbol.for("react.element"), Le = Symbol.for("react.fragment"), Ne = Object.prototype.hasOwnProperty, We = je.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, Ae = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function ne(t, e, o) {
  var s, l = {}, n = null, r = null;
  o !== void 0 && (n = "" + o), e.key !== void 0 && (n = "" + e.key), e.ref !== void 0 && (r = e.ref);
  for (s in e) Ne.call(e, s) && !Ae.hasOwnProperty(s) && (l[s] = e[s]);
  if (t && t.defaultProps) for (s in e = t.defaultProps, e) l[s] === void 0 && (l[s] = e[s]);
  return {
    $$typeof: Fe,
    type: t,
    key: n,
    ref: r,
    props: l,
    _owner: We.current
  };
}
j.Fragment = Le;
j.jsx = ne;
j.jsxs = ne;
te.exports = j;
var w = te.exports;
const {
  SvelteComponent: De,
  assign: q,
  binding_callbacks: V,
  check_outros: Me,
  children: re,
  claim_element: le,
  claim_space: Ue,
  component_subscribe: J,
  compute_slots: Be,
  create_slot: He,
  detach: I,
  element: oe,
  empty: X,
  exclude_internal_props: Y,
  get_all_dirty_from_scope: ze,
  get_slot_changes: Ge,
  group_outros: qe,
  init: Ve,
  insert_hydration: O,
  safe_not_equal: Je,
  set_custom_element_data: se,
  space: Xe,
  transition_in: T,
  transition_out: U,
  update_slot_base: Ye
} = window.__gradio__svelte__internal, {
  beforeUpdate: Ke,
  getContext: Qe,
  onDestroy: Ze,
  setContext: $e
} = window.__gradio__svelte__internal;
function K(t) {
  let e, o;
  const s = (
    /*#slots*/
    t[7].default
  ), l = He(
    s,
    t,
    /*$$scope*/
    t[6],
    null
  );
  return {
    c() {
      e = oe("svelte-slot"), l && l.c(), this.h();
    },
    l(n) {
      e = le(n, "SVELTE-SLOT", {
        class: !0
      });
      var r = re(e);
      l && l.l(r), r.forEach(I), this.h();
    },
    h() {
      se(e, "class", "svelte-1rt0kpf");
    },
    m(n, r) {
      O(n, e, r), l && l.m(e, null), t[9](e), o = !0;
    },
    p(n, r) {
      l && l.p && (!o || r & /*$$scope*/
      64) && Ye(
        l,
        s,
        n,
        /*$$scope*/
        n[6],
        o ? Ge(
          s,
          /*$$scope*/
          n[6],
          r,
          null
        ) : ze(
          /*$$scope*/
          n[6]
        ),
        null
      );
    },
    i(n) {
      o || (T(l, n), o = !0);
    },
    o(n) {
      U(l, n), o = !1;
    },
    d(n) {
      n && I(e), l && l.d(n), t[9](null);
    }
  };
}
function et(t) {
  let e, o, s, l, n = (
    /*$$slots*/
    t[4].default && K(t)
  );
  return {
    c() {
      e = oe("react-portal-target"), o = Xe(), n && n.c(), s = X(), this.h();
    },
    l(r) {
      e = le(r, "REACT-PORTAL-TARGET", {
        class: !0
      }), re(e).forEach(I), o = Ue(r), n && n.l(r), s = X(), this.h();
    },
    h() {
      se(e, "class", "svelte-1rt0kpf");
    },
    m(r, c) {
      O(r, e, c), t[8](e), O(r, o, c), n && n.m(r, c), O(r, s, c), l = !0;
    },
    p(r, [c]) {
      /*$$slots*/
      r[4].default ? n ? (n.p(r, c), c & /*$$slots*/
      16 && T(n, 1)) : (n = K(r), n.c(), T(n, 1), n.m(s.parentNode, s)) : n && (qe(), U(n, 1, 1, () => {
        n = null;
      }), Me());
    },
    i(r) {
      l || (T(n), l = !0);
    },
    o(r) {
      U(n), l = !1;
    },
    d(r) {
      r && (I(e), I(o), I(s)), t[8](null), n && n.d(r);
    }
  };
}
function Q(t) {
  const {
    svelteInit: e,
    ...o
  } = t;
  return o;
}
function tt(t, e, o) {
  let s, l, {
    $$slots: n = {},
    $$scope: r
  } = e;
  const c = Be(n);
  let {
    svelteInit: a
  } = e;
  const g = P(Q(e)), p = P();
  J(t, p, (f) => o(0, s = f));
  const i = P();
  J(t, i, (f) => o(1, l = f));
  const h = [], u = Qe("$$ms-gr-react-wrapper"), {
    slotKey: x,
    slotIndex: b,
    subSlotIndex: d
  } = he() || {}, m = a({
    parent: u,
    props: g,
    target: p,
    slot: i,
    slotKey: x,
    slotIndex: b,
    subSlotIndex: d,
    onDestroy(f) {
      h.push(f);
    }
  });
  $e("$$ms-gr-react-wrapper", m), Ke(() => {
    g.set(Q(e));
  }), Ze(() => {
    h.forEach((f) => f());
  });
  function C(f) {
    V[f ? "unshift" : "push"](() => {
      s = f, p.set(s);
    });
  }
  function R(f) {
    V[f ? "unshift" : "push"](() => {
      l = f, i.set(l);
    });
  }
  return t.$$set = (f) => {
    o(17, e = q(q({}, e), Y(f))), "svelteInit" in f && o(5, a = f.svelteInit), "$$scope" in f && o(6, r = f.$$scope);
  }, e = Y(e), [s, l, p, i, c, a, r, n, C, R];
}
class nt extends De {
  constructor(e) {
    super(), Ve(this, e, tt, et, Je, {
      svelteInit: 5
    });
  }
}
const {
  SvelteComponent: _t
} = window.__gradio__svelte__internal, Z = window.ms_globals.rerender, L = window.ms_globals.tree;
function rt(t, e = {}) {
  function o(s) {
    const l = P(), n = new nt({
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
          }, a = r.parent ?? L;
          return a.nodes = [...a.nodes, c], Z({
            createPortal: A,
            node: L
          }), r.onDestroy(() => {
            a.nodes = a.nodes.filter((g) => g.svelteInstance !== l), Z({
              createPortal: A,
              node: L
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
const lt = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function ot(t) {
  return t ? Object.keys(t).reduce((e, o) => {
    const s = t[o];
    return e[o] = st(o, s), e;
  }, {}) : {};
}
function st(t, e) {
  return typeof e == "number" && !lt.includes(t) ? e + "px" : e;
}
function B(t) {
  const e = [], o = t.cloneNode(!1);
  if (t._reactElement) {
    const l = v.Children.toArray(t._reactElement.props.children).map((n) => {
      if (v.isValidElement(n) && n.props.__slot__) {
        const {
          portals: r,
          clonedElement: c
        } = B(n.props.el);
        return v.cloneElement(n, {
          ...n.props,
          el: c,
          children: [...v.Children.toArray(n.props.children), ...r]
        });
      }
      return null;
    });
    return l.originalChildren = t._reactElement.props.children, e.push(A(v.cloneElement(t._reactElement, {
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
      useCapture: a
    }) => {
      o.addEventListener(c, r, a);
    });
  });
  const s = Array.from(t.childNodes);
  for (let l = 0; l < s.length; l++) {
    const n = s[l];
    if (n.nodeType === 1) {
      const {
        clonedElement: r,
        portals: c
      } = B(n);
      e.push(...c), o.appendChild(r);
    } else n.nodeType === 3 && o.appendChild(n.cloneNode());
  }
  return {
    clonedElement: o,
    portals: e
  };
}
function ct(t, e) {
  t && (typeof t == "function" ? t(e) : t.current = e);
}
const k = ae(({
  slot: t,
  clone: e,
  className: o,
  style: s,
  observeAttributes: l
}, n) => {
  const r = ue(), [c, a] = de([]), {
    forceClone: g
  } = pe(), p = g ? !0 : e;
  return fe(() => {
    var b;
    if (!r.current || !t)
      return;
    let i = t;
    function h() {
      let d = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (d = i.children[0], d.tagName.toLowerCase() === "react-portal-target" && d.children[0] && (d = d.children[0])), ct(n, d), o && d.classList.add(...o.split(" ")), s) {
        const m = ot(s);
        Object.keys(m).forEach((C) => {
          d.style[C] = m[C];
        });
      }
    }
    let u = null, x = null;
    if (p && window.MutationObserver) {
      let d = function() {
        var f, E, _;
        (f = r.current) != null && f.contains(i) && ((E = r.current) == null || E.removeChild(i));
        const {
          portals: C,
          clonedElement: R
        } = B(t);
        i = R, a(C), i.style.display = "contents", x && clearTimeout(x), x = setTimeout(() => {
          h();
        }, 50), (_ = r.current) == null || _.appendChild(i);
      };
      d();
      const m = Te(() => {
        d(), u == null || u.disconnect(), u == null || u.observe(t, {
          childList: !0,
          subtree: !0,
          attributes: l
        });
      }, 50);
      u = new window.MutationObserver(m), u.observe(t, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      i.style.display = "contents", h(), (b = r.current) == null || b.appendChild(i);
    return () => {
      var d, m;
      i.style.display = "", (d = r.current) != null && d.contains(i) && ((m = r.current) == null || m.removeChild(i)), u == null || u.disconnect();
    };
  }, [t, p, o, s, n, l, g]), v.createElement("react-child", {
    ref: r,
    style: {
      display: "contents"
    }
  }, ...c);
});
function it(t) {
  return /^(?:async\s+)?(?:function\s*(?:\w*\s*)?\(|\([\w\s,=]*\)\s*=>|\(\{[\w\s,=]*\}\)\s*=>|function\s*\*\s*\w*\s*\()/i.test(t.trim());
}
function at(t, e = !1) {
  try {
    if (ge(t))
      return t;
    if (e && !it(t))
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
function N(t, e) {
  return ee(() => at(t, e), [t, e]);
}
const ut = ({
  children: t,
  ...e
}) => /* @__PURE__ */ w.jsx(w.Fragment, {
  children: t(e)
});
function ce(t) {
  return v.createElement(ut, {
    children: t
  });
}
function ie(t, e, o) {
  const s = t.filter(Boolean);
  if (s.length !== 0)
    return s.map((l, n) => {
      var g;
      if (typeof l != "object")
        return e != null && e.fallback ? e.fallback(l) : l;
      const r = {
        ...l.props,
        key: ((g = l.props) == null ? void 0 : g.key) ?? (o ? `${o}-${n}` : `${n}`)
      };
      let c = r;
      Object.keys(l.slots).forEach((p) => {
        if (!l.slots[p] || !(l.slots[p] instanceof Element) && !l.slots[p].el)
          return;
        const i = p.split(".");
        i.forEach((m, C) => {
          c[m] || (c[m] = {}), C !== i.length - 1 && (c = r[m]);
        });
        const h = l.slots[p];
        let u, x, b = (e == null ? void 0 : e.clone) ?? !1, d = e == null ? void 0 : e.forceClone;
        h instanceof Element ? u = h : (u = h.el, x = h.callback, b = h.clone ?? b, d = h.forceClone ?? d), d = d ?? !!x, c[i[i.length - 1]] = u ? x ? (...m) => (x(i[i.length - 1], m), /* @__PURE__ */ w.jsx(M, {
          ...l.ctx,
          params: m,
          forceClone: d,
          children: /* @__PURE__ */ w.jsx(k, {
            slot: u,
            clone: b
          })
        })) : ce((m) => /* @__PURE__ */ w.jsx(M, {
          ...l.ctx,
          forceClone: d,
          children: /* @__PURE__ */ w.jsx(k, {
            ...m,
            slot: u,
            clone: b
          })
        })) : c[i[i.length - 1]], c = r;
      });
      const a = (e == null ? void 0 : e.children) || "children";
      return l[a] ? r[a] = ie(l[a], e, `${n}`) : e != null && e.children && (r[a] = void 0, Reflect.deleteProperty(r, a)), r;
    });
}
function $(t, e) {
  return t ? e != null && e.forceClone || e != null && e.params ? ce((o) => /* @__PURE__ */ w.jsx(M, {
    forceClone: e == null ? void 0 : e.forceClone,
    params: e == null ? void 0 : e.params,
    children: /* @__PURE__ */ w.jsx(k, {
      slot: t,
      clone: e == null ? void 0 : e.clone,
      ...o
    })
  })) : /* @__PURE__ */ w.jsx(k, {
    slot: t,
    clone: e == null ? void 0 : e.clone
  }) : null;
}
function W({
  key: t,
  slots: e,
  targets: o
}, s) {
  return e[t] ? (...l) => o ? o.map((n, r) => /* @__PURE__ */ w.jsx(v.Fragment, {
    children: $(n, {
      clone: !0,
      params: l,
      forceClone: (s == null ? void 0 : s.forceClone) ?? !0
    })
  }, r)) : /* @__PURE__ */ w.jsx(w.Fragment, {
    children: $(e[t], {
      clone: !0,
      params: l,
      forceClone: (s == null ? void 0 : s.forceClone) ?? !0
    })
  }) : void 0;
}
const {
  useItems: dt,
  withItemsContextProvider: ft,
  ItemHandler: ht
} = xe("antd-menu-items"), gt = rt(ft(["menu.items"], ({
  getPopupContainer: t,
  innerStyle: e,
  children: o,
  slots: s,
  dropdownRender: l,
  popupRender: n,
  setSlotParams: r,
  ...c
}) => {
  var h, u, x;
  const a = N(t), g = N(l), p = N(n), {
    items: {
      "menu.items": i
    }
  } = dt();
  return /* @__PURE__ */ w.jsx(w.Fragment, {
    children: /* @__PURE__ */ w.jsx(we, {
      ...c,
      menu: {
        ...c.menu,
        items: ee(() => {
          var b;
          return ((b = c.menu) == null ? void 0 : b.items) || ie(i, {
            clone: !0
          }) || [];
        }, [i, (h = c.menu) == null ? void 0 : h.items]),
        expandIcon: s["menu.expandIcon"] ? W({
          slots: s,
          key: "menu.expandIcon"
        }, {}) : (u = c.menu) == null ? void 0 : u.expandIcon,
        overflowedIndicator: s["menu.overflowedIndicator"] ? /* @__PURE__ */ w.jsx(k, {
          slot: s["menu.overflowedIndicator"]
        }) : (x = c.menu) == null ? void 0 : x.overflowedIndicator
      },
      getPopupContainer: a,
      dropdownRender: s.dropdownRender ? W({
        slots: s,
        key: "dropdownRender"
      }, {}) : g,
      popupRender: s.popupRender ? W({
        slots: s,
        key: "popupRender"
      }, {}) : p,
      children: /* @__PURE__ */ w.jsx("div", {
        className: "ms-gr-antd-dropdown-content",
        style: {
          display: "inline-block",
          ...e
        },
        children: o
      })
    })
  });
}));
export {
  gt as Dropdown,
  gt as default
};
