import { i as me, a as A, r as _e, w as T, g as he, b as pe } from "./Index-DBK2q-RQ.js";
const v = window.ms_globals.React, ae = window.ms_globals.React.forwardRef, ue = window.ms_globals.React.useRef, de = window.ms_globals.React.useState, fe = window.ms_globals.React.useEffect, ee = window.ms_globals.React.useMemo, W = window.ms_globals.ReactDOM.createPortal, ge = window.ms_globals.internalContext.useContextPropsContext, M = window.ms_globals.internalContext.ContextPropsProvider, we = window.ms_globals.antd.Tour, xe = window.ms_globals.createItemsContext.createItemsContext;
var be = /\s/;
function ye(e) {
  for (var t = e.length; t-- && be.test(e.charAt(t)); )
    ;
  return t;
}
var ve = /^\s+/;
function Ee(e) {
  return e && e.slice(0, ye(e) + 1).replace(ve, "");
}
var H = NaN, Ce = /^[-+]0x[0-9a-f]+$/i, Ie = /^0b[01]+$/i, Se = /^0o[0-7]+$/i, Re = parseInt;
function z(e) {
  if (typeof e == "number")
    return e;
  if (me(e))
    return H;
  if (A(e)) {
    var t = typeof e.valueOf == "function" ? e.valueOf() : e;
    e = A(t) ? t + "" : t;
  }
  if (typeof e != "string")
    return e === 0 ? e : +e;
  e = Ee(e);
  var o = Ie.test(e);
  return o || Se.test(e) ? Re(e.slice(2), o ? 2 : 8) : Ce.test(e) ? H : +e;
}
var F = function() {
  return _e.Date.now();
}, Pe = "Expected a function", Te = Math.max, ke = Math.min;
function Oe(e, t, o) {
  var l, r, n, s, i, d, h = 0, p = !1, c = !1, g = !0;
  if (typeof e != "function")
    throw new TypeError(Pe);
  t = z(t) || 0, A(o) && (p = !!o.leading, c = "maxWait" in o, n = c ? Te(z(o.maxWait) || 0, t) : n, g = "trailing" in o ? !!o.trailing : g);
  function u(_) {
    var E = l, R = r;
    return l = r = void 0, h = _, s = e.apply(R, E), s;
  }
  function x(_) {
    return h = _, i = setTimeout(m, t), p ? u(_) : s;
  }
  function b(_) {
    var E = _ - d, R = _ - h, B = t - E;
    return c ? ke(B, n - R) : B;
  }
  function a(_) {
    var E = _ - d, R = _ - h;
    return d === void 0 || E >= t || E < 0 || c && R >= n;
  }
  function m() {
    var _ = F();
    if (a(_))
      return y(_);
    i = setTimeout(m, b(_));
  }
  function y(_) {
    return i = void 0, g && l ? u(_) : (l = r = void 0, s);
  }
  function S() {
    i !== void 0 && clearTimeout(i), h = 0, l = d = r = i = void 0;
  }
  function f() {
    return i === void 0 ? s : y(F());
  }
  function C() {
    var _ = F(), E = a(_);
    if (l = arguments, r = this, d = _, E) {
      if (i === void 0)
        return x(d);
      if (c)
        return clearTimeout(i), i = setTimeout(m, t), u(d);
    }
    return i === void 0 && (i = setTimeout(m, t)), s;
  }
  return C.cancel = S, C.flush = f, C;
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
function ne(e, t, o) {
  var l, r = {}, n = null, s = null;
  o !== void 0 && (n = "" + o), t.key !== void 0 && (n = "" + t.key), t.ref !== void 0 && (s = t.ref);
  for (l in t) Ne.call(t, l) && !Ae.hasOwnProperty(l) && (r[l] = t[l]);
  if (e && e.defaultProps) for (l in t = e.defaultProps, t) r[l] === void 0 && (r[l] = t[l]);
  return {
    $$typeof: Fe,
    type: e,
    key: n,
    ref: s,
    props: r,
    _owner: We.current
  };
}
j.Fragment = Le;
j.jsx = ne;
j.jsxs = ne;
te.exports = j;
var w = te.exports;
const {
  SvelteComponent: Me,
  assign: G,
  binding_callbacks: q,
  check_outros: De,
  children: re,
  claim_element: se,
  claim_space: Ue,
  component_subscribe: V,
  compute_slots: Be,
  create_slot: He,
  detach: I,
  element: oe,
  empty: J,
  exclude_internal_props: X,
  get_all_dirty_from_scope: ze,
  get_slot_changes: Ge,
  group_outros: qe,
  init: Ve,
  insert_hydration: k,
  safe_not_equal: Je,
  set_custom_element_data: le,
  space: Xe,
  transition_in: O,
  transition_out: D,
  update_slot_base: Ye
} = window.__gradio__svelte__internal, {
  beforeUpdate: Ke,
  getContext: Qe,
  onDestroy: Ze,
  setContext: $e
} = window.__gradio__svelte__internal;
function Y(e) {
  let t, o;
  const l = (
    /*#slots*/
    e[7].default
  ), r = He(
    l,
    e,
    /*$$scope*/
    e[6],
    null
  );
  return {
    c() {
      t = oe("svelte-slot"), r && r.c(), this.h();
    },
    l(n) {
      t = se(n, "SVELTE-SLOT", {
        class: !0
      });
      var s = re(t);
      r && r.l(s), s.forEach(I), this.h();
    },
    h() {
      le(t, "class", "svelte-1rt0kpf");
    },
    m(n, s) {
      k(n, t, s), r && r.m(t, null), e[9](t), o = !0;
    },
    p(n, s) {
      r && r.p && (!o || s & /*$$scope*/
      64) && Ye(
        r,
        l,
        n,
        /*$$scope*/
        n[6],
        o ? Ge(
          l,
          /*$$scope*/
          n[6],
          s,
          null
        ) : ze(
          /*$$scope*/
          n[6]
        ),
        null
      );
    },
    i(n) {
      o || (O(r, n), o = !0);
    },
    o(n) {
      D(r, n), o = !1;
    },
    d(n) {
      n && I(t), r && r.d(n), e[9](null);
    }
  };
}
function et(e) {
  let t, o, l, r, n = (
    /*$$slots*/
    e[4].default && Y(e)
  );
  return {
    c() {
      t = oe("react-portal-target"), o = Xe(), n && n.c(), l = J(), this.h();
    },
    l(s) {
      t = se(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), re(t).forEach(I), o = Ue(s), n && n.l(s), l = J(), this.h();
    },
    h() {
      le(t, "class", "svelte-1rt0kpf");
    },
    m(s, i) {
      k(s, t, i), e[8](t), k(s, o, i), n && n.m(s, i), k(s, l, i), r = !0;
    },
    p(s, [i]) {
      /*$$slots*/
      s[4].default ? n ? (n.p(s, i), i & /*$$slots*/
      16 && O(n, 1)) : (n = Y(s), n.c(), O(n, 1), n.m(l.parentNode, l)) : n && (qe(), D(n, 1, 1, () => {
        n = null;
      }), De());
    },
    i(s) {
      r || (O(n), r = !0);
    },
    o(s) {
      D(n), r = !1;
    },
    d(s) {
      s && (I(t), I(o), I(l)), e[8](null), n && n.d(s);
    }
  };
}
function K(e) {
  const {
    svelteInit: t,
    ...o
  } = e;
  return o;
}
function tt(e, t, o) {
  let l, r, {
    $$slots: n = {},
    $$scope: s
  } = t;
  const i = Be(n);
  let {
    svelteInit: d
  } = t;
  const h = T(K(t)), p = T();
  V(e, p, (f) => o(0, l = f));
  const c = T();
  V(e, c, (f) => o(1, r = f));
  const g = [], u = Qe("$$ms-gr-react-wrapper"), {
    slotKey: x,
    slotIndex: b,
    subSlotIndex: a
  } = he() || {}, m = d({
    parent: u,
    props: h,
    target: p,
    slot: c,
    slotKey: x,
    slotIndex: b,
    subSlotIndex: a,
    onDestroy(f) {
      g.push(f);
    }
  });
  $e("$$ms-gr-react-wrapper", m), Ke(() => {
    h.set(K(t));
  }), Ze(() => {
    g.forEach((f) => f());
  });
  function y(f) {
    q[f ? "unshift" : "push"](() => {
      l = f, p.set(l);
    });
  }
  function S(f) {
    q[f ? "unshift" : "push"](() => {
      r = f, c.set(r);
    });
  }
  return e.$$set = (f) => {
    o(17, t = G(G({}, t), X(f))), "svelteInit" in f && o(5, d = f.svelteInit), "$$scope" in f && o(6, s = f.$$scope);
  }, t = X(t), [l, r, p, c, i, d, s, n, y, S];
}
class nt extends Me {
  constructor(t) {
    super(), Ve(this, t, tt, et, Je, {
      svelteInit: 5
    });
  }
}
const {
  SvelteComponent: _t
} = window.__gradio__svelte__internal, Q = window.ms_globals.rerender, L = window.ms_globals.tree;
function rt(e, t = {}) {
  function o(l) {
    const r = T(), n = new nt({
      ...l,
      props: {
        svelteInit(s) {
          window.ms_globals.autokey += 1;
          const i = {
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
          }, d = s.parent ?? L;
          return d.nodes = [...d.nodes, i], Q({
            createPortal: W,
            node: L
          }), s.onDestroy(() => {
            d.nodes = d.nodes.filter((h) => h.svelteInstance !== r), Q({
              createPortal: W,
              node: L
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
      l(o);
    });
  });
}
const st = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function ot(e) {
  return e ? Object.keys(e).reduce((t, o) => {
    const l = e[o];
    return t[o] = lt(o, l), t;
  }, {}) : {};
}
function lt(e, t) {
  return typeof t == "number" && !st.includes(e) ? t + "px" : t;
}
function U(e) {
  const t = [], o = e.cloneNode(!1);
  if (e._reactElement) {
    const r = v.Children.toArray(e._reactElement.props.children).map((n) => {
      if (v.isValidElement(n) && n.props.__slot__) {
        const {
          portals: s,
          clonedElement: i
        } = U(n.props.el);
        return v.cloneElement(n, {
          ...n.props,
          el: i,
          children: [...v.Children.toArray(n.props.children), ...s]
        });
      }
      return null;
    });
    return r.originalChildren = e._reactElement.props.children, t.push(W(v.cloneElement(e._reactElement, {
      ...e._reactElement.props,
      children: r
    }), o)), {
      clonedElement: o,
      portals: t
    };
  }
  Object.keys(e.getEventListeners()).forEach((r) => {
    e.getEventListeners(r).forEach(({
      listener: s,
      type: i,
      useCapture: d
    }) => {
      o.addEventListener(i, s, d);
    });
  });
  const l = Array.from(e.childNodes);
  for (let r = 0; r < l.length; r++) {
    const n = l[r];
    if (n.nodeType === 1) {
      const {
        clonedElement: s,
        portals: i
      } = U(n);
      t.push(...i), o.appendChild(s);
    } else n.nodeType === 3 && o.appendChild(n.cloneNode());
  }
  return {
    clonedElement: o,
    portals: t
  };
}
function it(e, t) {
  e && (typeof e == "function" ? e(t) : e.current = t);
}
const P = ae(({
  slot: e,
  clone: t,
  className: o,
  style: l,
  observeAttributes: r
}, n) => {
  const s = ue(), [i, d] = de([]), {
    forceClone: h
  } = ge(), p = h ? !0 : t;
  return fe(() => {
    var b;
    if (!s.current || !e)
      return;
    let c = e;
    function g() {
      let a = c;
      if (c.tagName.toLowerCase() === "svelte-slot" && c.children.length === 1 && c.children[0] && (a = c.children[0], a.tagName.toLowerCase() === "react-portal-target" && a.children[0] && (a = a.children[0])), it(n, a), o && a.classList.add(...o.split(" ")), l) {
        const m = ot(l);
        Object.keys(m).forEach((y) => {
          a.style[y] = m[y];
        });
      }
    }
    let u = null, x = null;
    if (p && window.MutationObserver) {
      let a = function() {
        var f, C, _;
        (f = s.current) != null && f.contains(c) && ((C = s.current) == null || C.removeChild(c));
        const {
          portals: y,
          clonedElement: S
        } = U(e);
        c = S, d(y), c.style.display = "contents", x && clearTimeout(x), x = setTimeout(() => {
          g();
        }, 50), (_ = s.current) == null || _.appendChild(c);
      };
      a();
      const m = Oe(() => {
        a(), u == null || u.disconnect(), u == null || u.observe(e, {
          childList: !0,
          subtree: !0,
          attributes: r
        });
      }, 50);
      u = new window.MutationObserver(m), u.observe(e, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      c.style.display = "contents", g(), (b = s.current) == null || b.appendChild(c);
    return () => {
      var a, m;
      c.style.display = "", (a = s.current) != null && a.contains(c) && ((m = s.current) == null || m.removeChild(c)), u == null || u.disconnect();
    };
  }, [e, p, o, l, n, r, h]), v.createElement("react-child", {
    ref: s,
    style: {
      display: "contents"
    }
  }, ...i);
});
function ct(e) {
  return /^(?:async\s+)?(?:function\s*(?:\w*\s*)?\(|\([\w\s,=]*\)\s*=>|\(\{[\w\s,=]*\}\)\s*=>|function\s*\*\s*\w*\s*\()/i.test(e.trim());
}
function at(e, t = !1) {
  try {
    if (pe(e))
      return e;
    if (t && !ct(e))
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
function N(e, t) {
  return ee(() => at(e, t), [e, t]);
}
const ut = ({
  children: e,
  ...t
}) => /* @__PURE__ */ w.jsx(w.Fragment, {
  children: e(t)
});
function ie(e) {
  return v.createElement(ut, {
    children: e
  });
}
function ce(e, t, o) {
  const l = e.filter(Boolean);
  if (l.length !== 0)
    return l.map((r, n) => {
      var h;
      if (typeof r != "object")
        return r;
      const s = {
        ...r.props,
        key: ((h = r.props) == null ? void 0 : h.key) ?? (o ? `${o}-${n}` : `${n}`)
      };
      let i = s;
      Object.keys(r.slots).forEach((p) => {
        if (!r.slots[p] || !(r.slots[p] instanceof Element) && !r.slots[p].el)
          return;
        const c = p.split(".");
        c.forEach((m, y) => {
          i[m] || (i[m] = {}), y !== c.length - 1 && (i = s[m]);
        });
        const g = r.slots[p];
        let u, x, b = !1, a = t == null ? void 0 : t.forceClone;
        g instanceof Element ? u = g : (u = g.el, x = g.callback, b = g.clone ?? b, a = g.forceClone ?? a), a = a ?? !!x, i[c[c.length - 1]] = u ? x ? (...m) => (x(c[c.length - 1], m), /* @__PURE__ */ w.jsx(M, {
          ...r.ctx,
          params: m,
          forceClone: a,
          children: /* @__PURE__ */ w.jsx(P, {
            slot: u,
            clone: b
          })
        })) : ie((m) => /* @__PURE__ */ w.jsx(M, {
          ...r.ctx,
          forceClone: a,
          children: /* @__PURE__ */ w.jsx(P, {
            ...m,
            slot: u,
            clone: b
          })
        })) : i[c[c.length - 1]], i = s;
      });
      const d = "children";
      return r[d] && (s[d] = ce(r[d], t, `${n}`)), s;
    });
}
function Z(e, t) {
  return e ? t != null && t.forceClone || t != null && t.params ? ie((o) => /* @__PURE__ */ w.jsx(M, {
    forceClone: t == null ? void 0 : t.forceClone,
    params: t == null ? void 0 : t.params,
    children: /* @__PURE__ */ w.jsx(P, {
      slot: e,
      clone: t == null ? void 0 : t.clone,
      ...o
    })
  })) : /* @__PURE__ */ w.jsx(P, {
    slot: e,
    clone: t == null ? void 0 : t.clone
  }) : null;
}
function $({
  key: e,
  slots: t,
  targets: o
}, l) {
  return t[e] ? (...r) => o ? o.map((n, s) => /* @__PURE__ */ w.jsx(v.Fragment, {
    children: Z(n, {
      clone: !0,
      params: r,
      forceClone: !0
    })
  }, s)) : /* @__PURE__ */ w.jsx(w.Fragment, {
    children: Z(t[e], {
      clone: !0,
      params: r,
      forceClone: !0
    })
  }) : void 0;
}
const {
  withItemsContextProvider: dt,
  useItems: ft,
  ItemHandler: ht
} = xe("antd-tour-items"), pt = rt(dt(["steps", "default"], ({
  slots: e,
  steps: t,
  children: o,
  onChange: l,
  onClose: r,
  getPopupContainer: n,
  setSlotParams: s,
  indicatorsRender: i,
  actionsRender: d,
  ...h
}) => {
  const p = N(n), c = N(i), g = N(d), {
    items: u
  } = ft(), x = u.steps.length > 0 ? u.steps : u.default;
  return /* @__PURE__ */ w.jsxs(w.Fragment, {
    children: [/* @__PURE__ */ w.jsx("div", {
      style: {
        display: "none"
      },
      children: o
    }), /* @__PURE__ */ w.jsx(we, {
      ...h,
      steps: ee(() => t || ce(x), [t, x]),
      onChange: (b) => {
        l == null || l(b);
      },
      closeIcon: e.closeIcon ? /* @__PURE__ */ w.jsx(P, {
        slot: e.closeIcon
      }) : h.closeIcon,
      actionsRender: e.actionsRender ? $({
        slots: e,
        key: "actionsRender"
      }) : g,
      indicatorsRender: e.indicatorsRender ? $({
        slots: e,
        key: "indicatorsRender"
      }) : c,
      getPopupContainer: p,
      onClose: (b, ...a) => {
        r == null || r(b, ...a);
      }
    })]
  });
}));
export {
  pt as Tour,
  pt as default
};
