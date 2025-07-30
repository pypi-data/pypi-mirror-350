import { i as Je, a as q, r as Qe, w as W, g as Xe, b as ze } from "./Index-D4hDx03S.js";
const O = window.ms_globals.React, He = window.ms_globals.React.forwardRef, De = window.ms_globals.React.useRef, Be = window.ms_globals.React.useState, Ge = window.ms_globals.React.useEffect, N = window.ms_globals.React.useMemo, z = window.ms_globals.ReactDOM.createPortal, qe = window.ms_globals.internalContext.useContextPropsContext, V = window.ms_globals.internalContext.ContextPropsProvider, j = window.ms_globals.antd.Table, G = window.ms_globals.createItemsContext.createItemsContext;
var Ve = /\s/;
function Ke(t) {
  for (var e = t.length; e-- && Ve.test(t.charAt(e)); )
    ;
  return e;
}
var Ye = /^\s+/;
function Ze(t) {
  return t && t.slice(0, Ke(t) + 1).replace(Ye, "");
}
var ce = NaN, $e = /^[-+]0x[0-9a-f]+$/i, et = /^0b[01]+$/i, tt = /^0o[0-7]+$/i, rt = parseInt;
function ue(t) {
  if (typeof t == "number")
    return t;
  if (Je(t))
    return ce;
  if (q(t)) {
    var e = typeof t.valueOf == "function" ? t.valueOf() : t;
    t = q(e) ? e + "" : e;
  }
  if (typeof t != "string")
    return t === 0 ? t : +t;
  t = Ze(t);
  var l = et.test(t);
  return l || tt.test(t) ? rt(t.slice(2), l ? 2 : 8) : $e.test(t) ? ce : +t;
}
var Q = function() {
  return Qe.Date.now();
}, nt = "Expected a function", lt = Math.max, it = Math.min;
function ot(t, e, l) {
  var a, i, r, n, s, u, _ = 0, w = !1, c = !1, C = !0;
  if (typeof t != "function")
    throw new TypeError(nt);
  e = ue(e) || 0, q(l) && (w = !!l.leading, c = "maxWait" in l, r = c ? lt(ue(l.maxWait) || 0, e) : r, C = "trailing" in l ? !!l.trailing : C);
  function d(m) {
    var E = a, P = i;
    return a = i = void 0, _ = m, n = t.apply(P, E), n;
  }
  function p(m) {
    return _ = m, s = setTimeout(h, e), w ? d(m) : n;
  }
  function y(m) {
    var E = m - u, P = m - _, L = e - E;
    return c ? it(L, r - P) : L;
  }
  function o(m) {
    var E = m - u, P = m - _;
    return u === void 0 || E >= e || E < 0 || c && P >= r;
  }
  function h() {
    var m = Q();
    if (o(m))
      return x(m);
    s = setTimeout(h, y(m));
  }
  function x(m) {
    return s = void 0, C && a ? d(m) : (a = i = void 0, n);
  }
  function R() {
    s !== void 0 && clearTimeout(s), _ = 0, a = u = i = s = void 0;
  }
  function f() {
    return s === void 0 ? n : x(Q());
  }
  function S() {
    var m = Q(), E = o(m);
    if (a = arguments, i = this, u = m, E) {
      if (s === void 0)
        return p(u);
      if (c)
        return clearTimeout(s), s = setTimeout(h, e), d(u);
    }
    return s === void 0 && (s = setTimeout(h, e)), n;
  }
  return S.cancel = R, S.flush = f, S;
}
var pe = {
  exports: {}
}, J = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var at = O, st = Symbol.for("react.element"), ct = Symbol.for("react.fragment"), ut = Object.prototype.hasOwnProperty, dt = at.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, ft = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function xe(t, e, l) {
  var a, i = {}, r = null, n = null;
  l !== void 0 && (r = "" + l), e.key !== void 0 && (r = "" + e.key), e.ref !== void 0 && (n = e.ref);
  for (a in e) ut.call(e, a) && !ft.hasOwnProperty(a) && (i[a] = e[a]);
  if (t && t.defaultProps) for (a in e = t.defaultProps, e) i[a] === void 0 && (i[a] = e[a]);
  return {
    $$typeof: st,
    type: t,
    key: r,
    ref: n,
    props: i,
    _owner: dt.current
  };
}
J.Fragment = ct;
J.jsx = xe;
J.jsxs = xe;
pe.exports = J;
var g = pe.exports;
const {
  SvelteComponent: ht,
  assign: de,
  binding_callbacks: fe,
  check_outros: mt,
  children: ye,
  claim_element: Ie,
  claim_space: gt,
  component_subscribe: he,
  compute_slots: _t,
  create_slot: wt,
  detach: k,
  element: Ee,
  empty: me,
  exclude_internal_props: ge,
  get_all_dirty_from_scope: Ct,
  get_slot_changes: bt,
  group_outros: pt,
  init: xt,
  insert_hydration: H,
  safe_not_equal: yt,
  set_custom_element_data: ve,
  space: It,
  transition_in: D,
  transition_out: K,
  update_slot_base: Et
} = window.__gradio__svelte__internal, {
  beforeUpdate: vt,
  getContext: St,
  onDestroy: Pt,
  setContext: Ot
} = window.__gradio__svelte__internal;
function _e(t) {
  let e, l;
  const a = (
    /*#slots*/
    t[7].default
  ), i = wt(
    a,
    t,
    /*$$scope*/
    t[6],
    null
  );
  return {
    c() {
      e = Ee("svelte-slot"), i && i.c(), this.h();
    },
    l(r) {
      e = Ie(r, "SVELTE-SLOT", {
        class: !0
      });
      var n = ye(e);
      i && i.l(n), n.forEach(k), this.h();
    },
    h() {
      ve(e, "class", "svelte-1rt0kpf");
    },
    m(r, n) {
      H(r, e, n), i && i.m(e, null), t[9](e), l = !0;
    },
    p(r, n) {
      i && i.p && (!l || n & /*$$scope*/
      64) && Et(
        i,
        a,
        r,
        /*$$scope*/
        r[6],
        l ? bt(
          a,
          /*$$scope*/
          r[6],
          n,
          null
        ) : Ct(
          /*$$scope*/
          r[6]
        ),
        null
      );
    },
    i(r) {
      l || (D(i, r), l = !0);
    },
    o(r) {
      K(i, r), l = !1;
    },
    d(r) {
      r && k(e), i && i.d(r), t[9](null);
    }
  };
}
function Rt(t) {
  let e, l, a, i, r = (
    /*$$slots*/
    t[4].default && _e(t)
  );
  return {
    c() {
      e = Ee("react-portal-target"), l = It(), r && r.c(), a = me(), this.h();
    },
    l(n) {
      e = Ie(n, "REACT-PORTAL-TARGET", {
        class: !0
      }), ye(e).forEach(k), l = gt(n), r && r.l(n), a = me(), this.h();
    },
    h() {
      ve(e, "class", "svelte-1rt0kpf");
    },
    m(n, s) {
      H(n, e, s), t[8](e), H(n, l, s), r && r.m(n, s), H(n, a, s), i = !0;
    },
    p(n, [s]) {
      /*$$slots*/
      n[4].default ? r ? (r.p(n, s), s & /*$$slots*/
      16 && D(r, 1)) : (r = _e(n), r.c(), D(r, 1), r.m(a.parentNode, a)) : r && (pt(), K(r, 1, 1, () => {
        r = null;
      }), mt());
    },
    i(n) {
      i || (D(r), i = !0);
    },
    o(n) {
      K(r), i = !1;
    },
    d(n) {
      n && (k(e), k(l), k(a)), t[8](null), r && r.d(n);
    }
  };
}
function we(t) {
  const {
    svelteInit: e,
    ...l
  } = t;
  return l;
}
function Tt(t, e, l) {
  let a, i, {
    $$slots: r = {},
    $$scope: n
  } = e;
  const s = _t(r);
  let {
    svelteInit: u
  } = e;
  const _ = W(we(e)), w = W();
  he(t, w, (f) => l(0, a = f));
  const c = W();
  he(t, c, (f) => l(1, i = f));
  const C = [], d = St("$$ms-gr-react-wrapper"), {
    slotKey: p,
    slotIndex: y,
    subSlotIndex: o
  } = Xe() || {}, h = u({
    parent: d,
    props: _,
    target: w,
    slot: c,
    slotKey: p,
    slotIndex: y,
    subSlotIndex: o,
    onDestroy(f) {
      C.push(f);
    }
  });
  Ot("$$ms-gr-react-wrapper", h), vt(() => {
    _.set(we(e));
  }), Pt(() => {
    C.forEach((f) => f());
  });
  function x(f) {
    fe[f ? "unshift" : "push"](() => {
      a = f, w.set(a);
    });
  }
  function R(f) {
    fe[f ? "unshift" : "push"](() => {
      i = f, c.set(i);
    });
  }
  return t.$$set = (f) => {
    l(17, e = de(de({}, e), ge(f))), "svelteInit" in f && l(5, u = f.svelteInit), "$$scope" in f && l(6, n = f.$$scope);
  }, e = ge(e), [a, i, w, c, s, u, n, r, x, R];
}
class kt extends ht {
  constructor(e) {
    super(), xt(this, e, Tt, Rt, yt, {
      svelteInit: 5
    });
  }
}
const {
  SvelteComponent: zt
} = window.__gradio__svelte__internal, Ce = window.ms_globals.rerender, X = window.ms_globals.tree;
function jt(t, e = {}) {
  function l(a) {
    const i = W(), r = new kt({
      ...a,
      props: {
        svelteInit(n) {
          window.ms_globals.autokey += 1;
          const s = {
            key: window.ms_globals.autokey,
            svelteInstance: i,
            reactComponent: t,
            props: n.props,
            slot: n.slot,
            target: n.target,
            slotIndex: n.slotIndex,
            subSlotIndex: n.subSlotIndex,
            ignore: e.ignore,
            slotKey: n.slotKey,
            nodes: []
          }, u = n.parent ?? X;
          return u.nodes = [...u.nodes, s], Ce({
            createPortal: z,
            node: X
          }), n.onDestroy(() => {
            u.nodes = u.nodes.filter((_) => _.svelteInstance !== i), Ce({
              createPortal: z,
              node: X
            });
          }), s;
        },
        ...a.props
      }
    });
    return i.set(r), r;
  }
  return new Promise((a) => {
    window.ms_globals.initializePromise.then(() => {
      a(l);
    });
  });
}
const Nt = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Lt(t) {
  return t ? Object.keys(t).reduce((e, l) => {
    const a = t[l];
    return e[l] = Ft(l, a), e;
  }, {}) : {};
}
function Ft(t, e) {
  return typeof e == "number" && !Nt.includes(t) ? e + "px" : e;
}
function Y(t) {
  const e = [], l = t.cloneNode(!1);
  if (t._reactElement) {
    const i = O.Children.toArray(t._reactElement.props.children).map((r) => {
      if (O.isValidElement(r) && r.props.__slot__) {
        const {
          portals: n,
          clonedElement: s
        } = Y(r.props.el);
        return O.cloneElement(r, {
          ...r.props,
          el: s,
          children: [...O.Children.toArray(r.props.children), ...n]
        });
      }
      return null;
    });
    return i.originalChildren = t._reactElement.props.children, e.push(z(O.cloneElement(t._reactElement, {
      ...t._reactElement.props,
      children: i
    }), l)), {
      clonedElement: l,
      portals: e
    };
  }
  Object.keys(t.getEventListeners()).forEach((i) => {
    t.getEventListeners(i).forEach(({
      listener: n,
      type: s,
      useCapture: u
    }) => {
      l.addEventListener(s, n, u);
    });
  });
  const a = Array.from(t.childNodes);
  for (let i = 0; i < a.length; i++) {
    const r = a[i];
    if (r.nodeType === 1) {
      const {
        clonedElement: n,
        portals: s
      } = Y(r);
      e.push(...s), l.appendChild(n);
    } else r.nodeType === 3 && l.appendChild(r.cloneNode());
  }
  return {
    clonedElement: l,
    portals: e
  };
}
function At(t, e) {
  t && (typeof t == "function" ? t(e) : t.current = e);
}
const T = He(({
  slot: t,
  clone: e,
  className: l,
  style: a,
  observeAttributes: i
}, r) => {
  const n = De(), [s, u] = Be([]), {
    forceClone: _
  } = qe(), w = _ ? !0 : e;
  return Ge(() => {
    var y;
    if (!n.current || !t)
      return;
    let c = t;
    function C() {
      let o = c;
      if (c.tagName.toLowerCase() === "svelte-slot" && c.children.length === 1 && c.children[0] && (o = c.children[0], o.tagName.toLowerCase() === "react-portal-target" && o.children[0] && (o = o.children[0])), At(r, o), l && o.classList.add(...l.split(" ")), a) {
        const h = Lt(a);
        Object.keys(h).forEach((x) => {
          o.style[x] = h[x];
        });
      }
    }
    let d = null, p = null;
    if (w && window.MutationObserver) {
      let o = function() {
        var f, S, m;
        (f = n.current) != null && f.contains(c) && ((S = n.current) == null || S.removeChild(c));
        const {
          portals: x,
          clonedElement: R
        } = Y(t);
        c = R, u(x), c.style.display = "contents", p && clearTimeout(p), p = setTimeout(() => {
          C();
        }, 50), (m = n.current) == null || m.appendChild(c);
      };
      o();
      const h = ot(() => {
        o(), d == null || d.disconnect(), d == null || d.observe(t, {
          childList: !0,
          subtree: !0,
          attributes: i
        });
      }, 50);
      d = new window.MutationObserver(h), d.observe(t, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      c.style.display = "contents", C(), (y = n.current) == null || y.appendChild(c);
    return () => {
      var o, h;
      c.style.display = "", (o = n.current) != null && o.contains(c) && ((h = n.current) == null || h.removeChild(c)), d == null || d.disconnect();
    };
  }, [t, w, l, a, r, i, _]), O.createElement("react-child", {
    ref: n,
    style: {
      display: "contents"
    }
  }, ...s);
});
function Mt(t) {
  return /^(?:async\s+)?(?:function\s*(?:\w*\s*)?\(|\([\w\s,=]*\)\s*=>|\(\{[\w\s,=]*\}\)\s*=>|function\s*\*\s*\w*\s*\()/i.test(t.trim());
}
function v(t, e = !1) {
  try {
    if (ze(t))
      return t;
    if (e && !Mt(t))
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
function I(t, e) {
  return N(() => v(t, e), [t, e]);
}
function Ut(t, e) {
  return Object.keys(t).reduce((l, a) => (t[a] !== void 0 && (l[a] = t[a]), l), {});
}
const Wt = ({
  children: t,
  ...e
}) => /* @__PURE__ */ g.jsx(g.Fragment, {
  children: t(e)
});
function Se(t) {
  return O.createElement(Wt, {
    children: t
  });
}
function B(t, e, l) {
  const a = t.filter(Boolean);
  if (a.length !== 0)
    return a.map((i, r) => {
      var _;
      if (typeof i != "object")
        return e != null && e.fallback ? e.fallback(i) : i;
      const n = {
        ...i.props,
        key: ((_ = i.props) == null ? void 0 : _.key) ?? (l ? `${l}-${r}` : `${r}`)
      };
      let s = n;
      Object.keys(i.slots).forEach((w) => {
        if (!i.slots[w] || !(i.slots[w] instanceof Element) && !i.slots[w].el)
          return;
        const c = w.split(".");
        c.forEach((h, x) => {
          s[h] || (s[h] = {}), x !== c.length - 1 && (s = n[h]);
        });
        const C = i.slots[w];
        let d, p, y = (e == null ? void 0 : e.clone) ?? !1, o = e == null ? void 0 : e.forceClone;
        C instanceof Element ? d = C : (d = C.el, p = C.callback, y = C.clone ?? y, o = C.forceClone ?? o), o = o ?? !!p, s[c[c.length - 1]] = d ? p ? (...h) => (p(c[c.length - 1], h), /* @__PURE__ */ g.jsx(V, {
          ...i.ctx,
          params: h,
          forceClone: o,
          children: /* @__PURE__ */ g.jsx(T, {
            slot: d,
            clone: y
          })
        })) : Se((h) => /* @__PURE__ */ g.jsx(V, {
          ...i.ctx,
          forceClone: o,
          children: /* @__PURE__ */ g.jsx(T, {
            ...h,
            slot: d,
            clone: y
          })
        })) : s[c[c.length - 1]], s = n;
      });
      const u = (e == null ? void 0 : e.children) || "children";
      return i[u] ? n[u] = B(i[u], e, `${r}`) : e != null && e.children && (n[u] = void 0, Reflect.deleteProperty(n, u)), n;
    });
}
function be(t, e) {
  return t ? e != null && e.forceClone || e != null && e.params ? Se((l) => /* @__PURE__ */ g.jsx(V, {
    forceClone: e == null ? void 0 : e.forceClone,
    params: e == null ? void 0 : e.params,
    children: /* @__PURE__ */ g.jsx(T, {
      slot: t,
      clone: e == null ? void 0 : e.clone,
      ...l
    })
  })) : /* @__PURE__ */ g.jsx(T, {
    slot: t,
    clone: e == null ? void 0 : e.clone
  }) : null;
}
function M({
  key: t,
  slots: e,
  targets: l
}, a) {
  return e[t] ? (...i) => l ? l.map((r, n) => /* @__PURE__ */ g.jsx(O.Fragment, {
    children: be(r, {
      clone: !0,
      params: i,
      forceClone: !0
    })
  }, n)) : /* @__PURE__ */ g.jsx(g.Fragment, {
    children: be(e[t], {
      clone: !0,
      params: i,
      forceClone: !0
    })
  }) : void 0;
}
const {
  useItems: Ht,
  withItemsContextProvider: Dt,
  ItemHandler: qt
} = G("antd-table-columns"), {
  useItems: Vt,
  withItemsContextProvider: Kt,
  ItemHandler: Yt
} = G("antd-table-row-selection-selections"), {
  useItems: Bt,
  withItemsContextProvider: Gt,
  ItemHandler: Zt
} = G("antd-table-row-selection"), {
  useItems: Jt,
  withItemsContextProvider: Qt,
  ItemHandler: $t
} = G("antd-table-expandable");
function U(t) {
  return typeof t == "object" && t !== null ? t : {};
}
const er = jt(Gt(["rowSelection"], Qt(["expandable"], Dt(["default"], ({
  children: t,
  slots: e,
  columns: l,
  getPopupContainer: a,
  pagination: i,
  loading: r,
  rowKey: n,
  rowClassName: s,
  summary: u,
  rowSelection: _,
  expandable: w,
  sticky: c,
  footer: C,
  showSorterTooltip: d,
  onRow: p,
  onHeaderRow: y,
  components: o,
  setSlotParams: h,
  ...x
}) => {
  const {
    items: {
      default: R
    }
  } = Ht(), {
    items: {
      expandable: f
    }
  } = Jt(), {
    items: {
      rowSelection: S
    }
  } = Bt(), m = I(a), E = e["loading.tip"] || e["loading.indicator"], P = U(r), L = e["pagination.showQuickJumper.goButton"] || e["pagination.itemRender"], F = U(i), Pe = I(F.showTotal), Oe = I(s), Re = I(n, !0), Te = e["showSorterTooltip.title"] || typeof d == "object", A = U(d), ke = I(A.afterOpenChange), je = I(A.getPopupContainer), Ne = typeof c == "object", Z = U(c), Le = I(Z.getContainer), Fe = I(p), Ae = I(y), Me = I(u), Ue = I(C), We = N(() => {
    var re, ne, le, ie, oe, ae, se;
    const b = v((re = o == null ? void 0 : o.header) == null ? void 0 : re.table), $ = v((ne = o == null ? void 0 : o.header) == null ? void 0 : ne.row), ee = v((le = o == null ? void 0 : o.header) == null ? void 0 : le.cell), te = v((ie = o == null ? void 0 : o.header) == null ? void 0 : ie.wrapper);
    return {
      table: v(o == null ? void 0 : o.table),
      header: b || $ || ee || te ? {
        table: b,
        row: $,
        cell: ee,
        wrapper: te
      } : void 0,
      body: typeof (o == null ? void 0 : o.body) == "object" ? {
        wrapper: v((oe = o == null ? void 0 : o.body) == null ? void 0 : oe.wrapper),
        row: v((ae = o == null ? void 0 : o.body) == null ? void 0 : ae.row),
        cell: v((se = o == null ? void 0 : o.body) == null ? void 0 : se.cell)
      } : v(o == null ? void 0 : o.body)
    };
  }, [o]);
  return /* @__PURE__ */ g.jsxs(g.Fragment, {
    children: [/* @__PURE__ */ g.jsx("div", {
      style: {
        display: "none"
      },
      children: t
    }), /* @__PURE__ */ g.jsx(j, {
      ...x,
      components: We,
      columns: N(() => (l == null ? void 0 : l.map((b) => b === "EXPAND_COLUMN" ? j.EXPAND_COLUMN : b === "SELECTION_COLUMN" ? j.SELECTION_COLUMN : b)) || B(R, {
        fallback: (b) => b === "EXPAND_COLUMN" ? j.EXPAND_COLUMN : b === "SELECTION_COLUMN" ? j.SELECTION_COLUMN : b
      }), [R, l]),
      onRow: Fe,
      onHeaderRow: Ae,
      summary: e.summary ? M({
        slots: e,
        key: "summary"
      }) : Me,
      rowSelection: N(() => {
        var b;
        return _ || ((b = B(S)) == null ? void 0 : b[0]);
      }, [_, S]),
      expandable: N(() => {
        var b;
        return w || ((b = B(f)) == null ? void 0 : b[0]);
      }, [w, f]),
      rowClassName: Oe,
      rowKey: Re || n,
      sticky: Ne ? {
        ...Z,
        getContainer: Le
      } : c,
      showSorterTooltip: Te ? {
        ...A,
        afterOpenChange: ke,
        getPopupContainer: je,
        title: e["showSorterTooltip.title"] ? /* @__PURE__ */ g.jsx(T, {
          slot: e["showSorterTooltip.title"]
        }) : A.title
      } : d,
      pagination: L ? Ut({
        ...F,
        showTotal: Pe,
        showQuickJumper: e["pagination.showQuickJumper.goButton"] ? {
          goButton: /* @__PURE__ */ g.jsx(T, {
            slot: e["pagination.showQuickJumper.goButton"]
          })
        } : F.showQuickJumper,
        itemRender: e["pagination.itemRender"] ? M({
          slots: e,
          key: "pagination.itemRender"
        }) : F.itemRender
      }) : i,
      getPopupContainer: m,
      loading: E ? {
        ...P,
        tip: e["loading.tip"] ? /* @__PURE__ */ g.jsx(T, {
          slot: e["loading.tip"]
        }) : P.tip,
        indicator: e["loading.indicator"] ? /* @__PURE__ */ g.jsx(T, {
          slot: e["loading.indicator"]
        }) : P.indicator
      } : r,
      footer: e.footer ? M({
        slots: e,
        key: "footer"
      }) : Ue,
      title: e.title ? M({
        slots: e,
        key: "title"
      }) : x.title
    })]
  });
}))));
export {
  er as Table,
  er as default
};
