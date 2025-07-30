import { i as me, a as D, r as he, b as _e, w as j, g as pe, c as ge } from "./Index-CuDnWEmo.js";
const y = window.ms_globals.React, re = window.ms_globals.React.forwardRef, W = window.ms_globals.React.useRef, le = window.ms_globals.React.useState, N = window.ms_globals.React.useEffect, H = window.ms_globals.React.useMemo, M = window.ms_globals.ReactDOM.createPortal, Ce = window.ms_globals.internalContext.useContextPropsContext, V = window.ms_globals.internalContext.ContextPropsProvider, we = window.ms_globals.internalContext.AutoCompleteContext, xe = window.ms_globals.antd.AutoComplete, be = window.ms_globals.createItemsContext.createItemsContext;
var ye = /\s/;
function ve(t) {
  for (var e = t.length; e-- && ye.test(t.charAt(e)); )
    ;
  return e;
}
var Ee = /^\s+/;
function Ie(t) {
  return t && t.slice(0, ve(t) + 1).replace(Ee, "");
}
var z = NaN, Re = /^[-+]0x[0-9a-f]+$/i, Se = /^0b[01]+$/i, Pe = /^0o[0-7]+$/i, ke = parseInt;
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
  t = Ie(t);
  var r = Se.test(t);
  return r || Pe.test(t) ? ke(t.slice(2), r ? 2 : 8) : Re.test(t) ? z : +t;
}
var A = function() {
  return he.Date.now();
}, je = "Expected a function", Oe = Math.max, Te = Math.min;
function Fe(t, e, r) {
  var s, l, n, o, c, a, p = 0, C = !1, i = !1, g = !0;
  if (typeof t != "function")
    throw new TypeError(je);
  e = G(e) || 0, D(r) && (C = !!r.leading, i = "maxWait" in r, n = i ? Oe(G(r.maxWait) || 0, e) : n, g = "trailing" in r ? !!r.trailing : g);
  function f(h) {
    var I = s, P = l;
    return s = l = void 0, p = h, o = t.apply(P, I), o;
  }
  function x(h) {
    return p = h, c = setTimeout(m, e), C ? f(h) : o;
  }
  function b(h) {
    var I = h - a, P = h - p, q = e - I;
    return i ? Te(q, n - P) : q;
  }
  function u(h) {
    var I = h - a, P = h - p;
    return a === void 0 || I >= e || I < 0 || i && P >= n;
  }
  function m() {
    var h = A();
    if (u(h))
      return w(h);
    c = setTimeout(m, b(h));
  }
  function w(h) {
    return c = void 0, g && s ? f(h) : (s = l = void 0, o);
  }
  function v() {
    c !== void 0 && clearTimeout(c), p = 0, s = a = l = c = void 0;
  }
  function d() {
    return c === void 0 ? o : w(A());
  }
  function E() {
    var h = A(), I = u(h);
    if (s = arguments, l = this, a = h, I) {
      if (c === void 0)
        return x(a);
      if (i)
        return clearTimeout(c), c = setTimeout(m, e), f(a);
    }
    return c === void 0 && (c = setTimeout(m, e)), o;
  }
  return E.cancel = v, E.flush = d, E;
}
function Ae(t, e) {
  return _e(t, e);
}
var oe = {
  exports: {}
}, F = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var Le = y, We = Symbol.for("react.element"), Ne = Symbol.for("react.fragment"), Me = Object.prototype.hasOwnProperty, De = Le.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, Ve = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function se(t, e, r) {
  var s, l = {}, n = null, o = null;
  r !== void 0 && (n = "" + r), e.key !== void 0 && (n = "" + e.key), e.ref !== void 0 && (o = e.ref);
  for (s in e) Me.call(e, s) && !Ve.hasOwnProperty(s) && (l[s] = e[s]);
  if (t && t.defaultProps) for (s in e = t.defaultProps, e) l[s] === void 0 && (l[s] = e[s]);
  return {
    $$typeof: We,
    type: t,
    key: n,
    ref: o,
    props: l,
    _owner: De.current
  };
}
F.Fragment = Ne;
F.jsx = se;
F.jsxs = se;
oe.exports = F;
var _ = oe.exports;
const {
  SvelteComponent: Ue,
  assign: J,
  binding_callbacks: X,
  check_outros: Be,
  children: ce,
  claim_element: ie,
  claim_space: He,
  component_subscribe: Y,
  compute_slots: qe,
  create_slot: ze,
  detach: S,
  element: ae,
  empty: K,
  exclude_internal_props: Q,
  get_all_dirty_from_scope: Ge,
  get_slot_changes: Je,
  group_outros: Xe,
  init: Ye,
  insert_hydration: O,
  safe_not_equal: Ke,
  set_custom_element_data: ue,
  space: Qe,
  transition_in: T,
  transition_out: U,
  update_slot_base: Ze
} = window.__gradio__svelte__internal, {
  beforeUpdate: $e,
  getContext: et,
  onDestroy: tt,
  setContext: nt
} = window.__gradio__svelte__internal;
function Z(t) {
  let e, r;
  const s = (
    /*#slots*/
    t[7].default
  ), l = ze(
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
      var o = ce(e);
      l && l.l(o), o.forEach(S), this.h();
    },
    h() {
      ue(e, "class", "svelte-1rt0kpf");
    },
    m(n, o) {
      O(n, e, o), l && l.m(e, null), t[9](e), r = !0;
    },
    p(n, o) {
      l && l.p && (!r || o & /*$$scope*/
      64) && Ze(
        l,
        s,
        n,
        /*$$scope*/
        n[6],
        r ? Je(
          s,
          /*$$scope*/
          n[6],
          o,
          null
        ) : Ge(
          /*$$scope*/
          n[6]
        ),
        null
      );
    },
    i(n) {
      r || (T(l, n), r = !0);
    },
    o(n) {
      U(l, n), r = !1;
    },
    d(n) {
      n && S(e), l && l.d(n), t[9](null);
    }
  };
}
function rt(t) {
  let e, r, s, l, n = (
    /*$$slots*/
    t[4].default && Z(t)
  );
  return {
    c() {
      e = ae("react-portal-target"), r = Qe(), n && n.c(), s = K(), this.h();
    },
    l(o) {
      e = ie(o, "REACT-PORTAL-TARGET", {
        class: !0
      }), ce(e).forEach(S), r = He(o), n && n.l(o), s = K(), this.h();
    },
    h() {
      ue(e, "class", "svelte-1rt0kpf");
    },
    m(o, c) {
      O(o, e, c), t[8](e), O(o, r, c), n && n.m(o, c), O(o, s, c), l = !0;
    },
    p(o, [c]) {
      /*$$slots*/
      o[4].default ? n ? (n.p(o, c), c & /*$$slots*/
      16 && T(n, 1)) : (n = Z(o), n.c(), T(n, 1), n.m(s.parentNode, s)) : n && (Xe(), U(n, 1, 1, () => {
        n = null;
      }), Be());
    },
    i(o) {
      l || (T(n), l = !0);
    },
    o(o) {
      U(n), l = !1;
    },
    d(o) {
      o && (S(e), S(r), S(s)), t[8](null), n && n.d(o);
    }
  };
}
function $(t) {
  const {
    svelteInit: e,
    ...r
  } = t;
  return r;
}
function lt(t, e, r) {
  let s, l, {
    $$slots: n = {},
    $$scope: o
  } = e;
  const c = qe(n);
  let {
    svelteInit: a
  } = e;
  const p = j($(e)), C = j();
  Y(t, C, (d) => r(0, s = d));
  const i = j();
  Y(t, i, (d) => r(1, l = d));
  const g = [], f = et("$$ms-gr-react-wrapper"), {
    slotKey: x,
    slotIndex: b,
    subSlotIndex: u
  } = pe() || {}, m = a({
    parent: f,
    props: p,
    target: C,
    slot: i,
    slotKey: x,
    slotIndex: b,
    subSlotIndex: u,
    onDestroy(d) {
      g.push(d);
    }
  });
  nt("$$ms-gr-react-wrapper", m), $e(() => {
    p.set($(e));
  }), tt(() => {
    g.forEach((d) => d());
  });
  function w(d) {
    X[d ? "unshift" : "push"](() => {
      s = d, C.set(s);
    });
  }
  function v(d) {
    X[d ? "unshift" : "push"](() => {
      l = d, i.set(l);
    });
  }
  return t.$$set = (d) => {
    r(17, e = J(J({}, e), Q(d))), "svelteInit" in d && r(5, a = d.svelteInit), "$$scope" in d && r(6, o = d.$$scope);
  }, e = Q(e), [s, l, C, i, c, a, o, n, w, v];
}
class ot extends Ue {
  constructor(e) {
    super(), Ye(this, e, lt, rt, Ke, {
      svelteInit: 5
    });
  }
}
const {
  SvelteComponent: wt
} = window.__gradio__svelte__internal, ee = window.ms_globals.rerender, L = window.ms_globals.tree;
function st(t, e = {}) {
  function r(s) {
    const l = j(), n = new ot({
      ...s,
      props: {
        svelteInit(o) {
          window.ms_globals.autokey += 1;
          const c = {
            key: window.ms_globals.autokey,
            svelteInstance: l,
            reactComponent: t,
            props: o.props,
            slot: o.slot,
            target: o.target,
            slotIndex: o.slotIndex,
            subSlotIndex: o.subSlotIndex,
            ignore: e.ignore,
            slotKey: o.slotKey,
            nodes: []
          }, a = o.parent ?? L;
          return a.nodes = [...a.nodes, c], ee({
            createPortal: M,
            node: L
          }), o.onDestroy(() => {
            a.nodes = a.nodes.filter((p) => p.svelteInstance !== l), ee({
              createPortal: M,
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
      s(r);
    });
  });
}
const ct = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function it(t) {
  return t ? Object.keys(t).reduce((e, r) => {
    const s = t[r];
    return e[r] = at(r, s), e;
  }, {}) : {};
}
function at(t, e) {
  return typeof e == "number" && !ct.includes(t) ? e + "px" : e;
}
function B(t) {
  const e = [], r = t.cloneNode(!1);
  if (t._reactElement) {
    const l = y.Children.toArray(t._reactElement.props.children).map((n) => {
      if (y.isValidElement(n) && n.props.__slot__) {
        const {
          portals: o,
          clonedElement: c
        } = B(n.props.el);
        return y.cloneElement(n, {
          ...n.props,
          el: c,
          children: [...y.Children.toArray(n.props.children), ...o]
        });
      }
      return null;
    });
    return l.originalChildren = t._reactElement.props.children, e.push(M(y.cloneElement(t._reactElement, {
      ...t._reactElement.props,
      children: l
    }), r)), {
      clonedElement: r,
      portals: e
    };
  }
  Object.keys(t.getEventListeners()).forEach((l) => {
    t.getEventListeners(l).forEach(({
      listener: o,
      type: c,
      useCapture: a
    }) => {
      r.addEventListener(c, o, a);
    });
  });
  const s = Array.from(t.childNodes);
  for (let l = 0; l < s.length; l++) {
    const n = s[l];
    if (n.nodeType === 1) {
      const {
        clonedElement: o,
        portals: c
      } = B(n);
      e.push(...c), r.appendChild(o);
    } else n.nodeType === 3 && r.appendChild(n.cloneNode());
  }
  return {
    clonedElement: r,
    portals: e
  };
}
function ut(t, e) {
  t && (typeof t == "function" ? t(e) : t.current = e);
}
const R = re(({
  slot: t,
  clone: e,
  className: r,
  style: s,
  observeAttributes: l
}, n) => {
  const o = W(), [c, a] = le([]), {
    forceClone: p
  } = Ce(), C = p ? !0 : e;
  return N(() => {
    var b;
    if (!o.current || !t)
      return;
    let i = t;
    function g() {
      let u = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (u = i.children[0], u.tagName.toLowerCase() === "react-portal-target" && u.children[0] && (u = u.children[0])), ut(n, u), r && u.classList.add(...r.split(" ")), s) {
        const m = it(s);
        Object.keys(m).forEach((w) => {
          u.style[w] = m[w];
        });
      }
    }
    let f = null, x = null;
    if (C && window.MutationObserver) {
      let u = function() {
        var d, E, h;
        (d = o.current) != null && d.contains(i) && ((E = o.current) == null || E.removeChild(i));
        const {
          portals: w,
          clonedElement: v
        } = B(t);
        i = v, a(w), i.style.display = "contents", x && clearTimeout(x), x = setTimeout(() => {
          g();
        }, 50), (h = o.current) == null || h.appendChild(i);
      };
      u();
      const m = Fe(() => {
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
      i.style.display = "contents", g(), (b = o.current) == null || b.appendChild(i);
    return () => {
      var u, m;
      i.style.display = "", (u = o.current) != null && u.contains(i) && ((m = o.current) == null || m.removeChild(i)), f == null || f.disconnect();
    };
  }, [t, C, r, s, n, l, p]), y.createElement("react-child", {
    ref: o,
    style: {
      display: "contents"
    }
  }, ...c);
});
function dt(t) {
  return /^(?:async\s+)?(?:function\s*(?:\w*\s*)?\(|\([\w\s,=]*\)\s*=>|\(\{[\w\s,=]*\}\)\s*=>|function\s*\*\s*\w*\s*\()/i.test(t.trim());
}
function ft(t, e = !1) {
  try {
    if (ge(t))
      return t;
    if (e && !dt(t))
      return;
    if (typeof t == "string") {
      let r = t.trim();
      return r.startsWith(";") && (r = r.slice(1)), r.endsWith(";") && (r = r.slice(0, -1)), new Function(`return (...args) => (${r})(...args)`)();
    }
    return;
  } catch {
    return;
  }
}
function k(t, e) {
  return H(() => ft(t, e), [t, e]);
}
function mt({
  value: t,
  onValueChange: e
}) {
  const [r, s] = le(t), l = W(e);
  l.current = e;
  const n = W(r);
  return n.current = r, N(() => {
    l.current(r);
  }, [r]), N(() => {
    Ae(t, n.current) || s(t);
  }, [t]), [r, s];
}
const ht = ({
  children: t,
  ...e
}) => /* @__PURE__ */ _.jsx(_.Fragment, {
  children: t(e)
});
function de(t) {
  return y.createElement(ht, {
    children: t
  });
}
function fe(t, e, r) {
  const s = t.filter(Boolean);
  if (s.length !== 0)
    return s.map((l, n) => {
      var p;
      if (typeof l != "object")
        return e != null && e.fallback ? e.fallback(l) : l;
      const o = {
        ...l.props,
        key: ((p = l.props) == null ? void 0 : p.key) ?? (r ? `${r}-${n}` : `${n}`)
      };
      let c = o;
      Object.keys(l.slots).forEach((C) => {
        if (!l.slots[C] || !(l.slots[C] instanceof Element) && !l.slots[C].el)
          return;
        const i = C.split(".");
        i.forEach((m, w) => {
          c[m] || (c[m] = {}), w !== i.length - 1 && (c = o[m]);
        });
        const g = l.slots[C];
        let f, x, b = (e == null ? void 0 : e.clone) ?? !1, u = e == null ? void 0 : e.forceClone;
        g instanceof Element ? f = g : (f = g.el, x = g.callback, b = g.clone ?? b, u = g.forceClone ?? u), u = u ?? !!x, c[i[i.length - 1]] = f ? x ? (...m) => (x(i[i.length - 1], m), /* @__PURE__ */ _.jsx(V, {
          ...l.ctx,
          params: m,
          forceClone: u,
          children: /* @__PURE__ */ _.jsx(R, {
            slot: f,
            clone: b
          })
        })) : de((m) => /* @__PURE__ */ _.jsx(V, {
          ...l.ctx,
          forceClone: u,
          children: /* @__PURE__ */ _.jsx(R, {
            ...m,
            slot: f,
            clone: b
          })
        })) : c[i[i.length - 1]], c = o;
      });
      const a = (e == null ? void 0 : e.children) || "children";
      return l[a] ? o[a] = fe(l[a], e, `${n}`) : e != null && e.children && (o[a] = void 0, Reflect.deleteProperty(o, a)), o;
    });
}
function te(t, e) {
  return t ? e != null && e.forceClone || e != null && e.params ? de((r) => /* @__PURE__ */ _.jsx(V, {
    forceClone: e == null ? void 0 : e.forceClone,
    params: e == null ? void 0 : e.params,
    children: /* @__PURE__ */ _.jsx(R, {
      slot: t,
      clone: e == null ? void 0 : e.clone,
      ...r
    })
  })) : /* @__PURE__ */ _.jsx(R, {
    slot: t,
    clone: e == null ? void 0 : e.clone
  }) : null;
}
function ne({
  key: t,
  slots: e,
  targets: r
}, s) {
  return e[t] ? (...l) => r ? r.map((n, o) => /* @__PURE__ */ _.jsx(y.Fragment, {
    children: te(n, {
      clone: !0,
      params: l,
      forceClone: (s == null ? void 0 : s.forceClone) ?? !0
    })
  }, o)) : /* @__PURE__ */ _.jsx(_.Fragment, {
    children: te(e[t], {
      clone: !0,
      params: l,
      forceClone: (s == null ? void 0 : s.forceClone) ?? !0
    })
  }) : void 0;
}
const {
  useItems: _t,
  withItemsContextProvider: pt,
  ItemHandler: xt
} = be("antd-auto-complete-options"), gt = re(({
  children: t,
  ...e
}, r) => /* @__PURE__ */ _.jsx(we.Provider, {
  value: H(() => ({
    ...e,
    elRef: r
  }), [e, r]),
  children: t
})), bt = st(pt(["options", "default"], ({
  slots: t,
  children: e,
  onValueChange: r,
  filterOption: s,
  onChange: l,
  options: n,
  getPopupContainer: o,
  dropdownRender: c,
  popupRender: a,
  elRef: p,
  setSlotParams: C,
  ...i
}) => {
  const g = k(o), f = k(s), x = k(c), b = k(a), [u, m] = mt({
    onValueChange: r,
    value: i.value
  }), {
    items: w
  } = _t(), v = w.options.length > 0 ? w.options : w.default;
  return /* @__PURE__ */ _.jsxs(_.Fragment, {
    children: [t.children ? null : /* @__PURE__ */ _.jsx("div", {
      style: {
        display: "none"
      },
      children: e
    }), /* @__PURE__ */ _.jsx(xe, {
      ...i,
      value: u,
      ref: p,
      allowClear: t["allowClear.clearIcon"] ? {
        clearIcon: /* @__PURE__ */ _.jsx(R, {
          slot: t["allowClear.clearIcon"]
        })
      } : i.allowClear,
      options: H(() => n || fe(v, {
        children: "options"
        // clone: true,
      }), [v, n]),
      onChange: (d, ...E) => {
        l == null || l(d, ...E), m(d);
      },
      notFoundContent: t.notFoundContent ? /* @__PURE__ */ _.jsx(R, {
        slot: t.notFoundContent
      }) : i.notFoundContent,
      filterOption: f || s,
      getPopupContainer: g,
      popupRender: t.popupRender ? ne({
        slots: t,
        key: "popupRender"
      }, {}) : b,
      dropdownRender: t.dropdownRender ? ne({
        slots: t,
        key: "dropdownRender"
      }, {}) : x,
      children: t.children ? /* @__PURE__ */ _.jsxs(gt, {
        children: [/* @__PURE__ */ _.jsx("div", {
          style: {
            display: "none"
          },
          children: e
        }), /* @__PURE__ */ _.jsx(R, {
          slot: t.children
        })]
      }) : null
    })]
  });
}));
export {
  bt as AutoComplete,
  bt as default
};
