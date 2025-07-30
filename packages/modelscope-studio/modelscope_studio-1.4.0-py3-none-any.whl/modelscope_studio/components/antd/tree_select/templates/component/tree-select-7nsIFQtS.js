import { i as he, a as M, r as _e, w as j, g as ge, b as pe } from "./Index-Bz5wPFDf.js";
const I = window.ms_globals.React, ue = window.ms_globals.React.forwardRef, de = window.ms_globals.React.useRef, fe = window.ms_globals.React.useState, me = window.ms_globals.React.useEffect, ee = window.ms_globals.React.useMemo, D = window.ms_globals.ReactDOM.createPortal, xe = window.ms_globals.internalContext.useContextPropsContext, U = window.ms_globals.internalContext.ContextPropsProvider, we = window.ms_globals.antd.TreeSelect, Ce = window.ms_globals.createItemsContext.createItemsContext;
var be = /\s/;
function ye(e) {
  for (var t = e.length; t-- && be.test(e.charAt(t)); )
    ;
  return t;
}
var ve = /^\s+/;
function Ie(e) {
  return e && e.slice(0, ye(e) + 1).replace(ve, "");
}
var z = NaN, Ee = /^[-+]0x[0-9a-f]+$/i, Re = /^0b[01]+$/i, Se = /^0o[0-7]+$/i, Te = parseInt;
function G(e) {
  if (typeof e == "number")
    return e;
  if (he(e))
    return z;
  if (M(e)) {
    var t = typeof e.valueOf == "function" ? e.valueOf() : e;
    e = M(t) ? t + "" : t;
  }
  if (typeof e != "string")
    return e === 0 ? e : +e;
  e = Ie(e);
  var l = Re.test(e);
  return l || Se.test(e) ? Te(e.slice(2), l ? 2 : 8) : Ee.test(e) ? z : +e;
}
var W = function() {
  return _e.Date.now();
}, Pe = "Expected a function", ke = Math.max, Oe = Math.min;
function je(e, t, l) {
  var c, o, n, r, s, u, _ = 0, x = !1, i = !1, w = !0;
  if (typeof e != "function")
    throw new TypeError(Pe);
  t = G(t) || 0, M(l) && (x = !!l.leading, i = "maxWait" in l, n = i ? ke(G(l.maxWait) || 0, t) : n, w = "trailing" in l ? !!l.trailing : w);
  function h(m) {
    var y = c, S = o;
    return c = o = void 0, _ = m, r = e.apply(S, y), r;
  }
  function C(m) {
    return _ = m, s = setTimeout(f, t), x ? h(m) : r;
  }
  function p(m) {
    var y = m - u, S = m - _, O = t - y;
    return i ? Oe(O, n - S) : O;
  }
  function a(m) {
    var y = m - u, S = m - _;
    return u === void 0 || y >= t || y < 0 || i && S >= n;
  }
  function f() {
    var m = W();
    if (a(m))
      return b(m);
    s = setTimeout(f, p(m));
  }
  function b(m) {
    return s = void 0, w && c ? h(m) : (c = o = void 0, r);
  }
  function E() {
    s !== void 0 && clearTimeout(s), _ = 0, c = u = o = s = void 0;
  }
  function d() {
    return s === void 0 ? r : b(W());
  }
  function v() {
    var m = W(), y = a(m);
    if (c = arguments, o = this, u = m, y) {
      if (s === void 0)
        return C(u);
      if (i)
        return clearTimeout(s), s = setTimeout(f, t), h(u);
    }
    return s === void 0 && (s = setTimeout(f, t)), r;
  }
  return v.cancel = E, v.flush = d, v;
}
var te = {
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
var Fe = I, Le = Symbol.for("react.element"), Ne = Symbol.for("react.fragment"), We = Object.prototype.hasOwnProperty, Ae = Fe.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, De = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function ne(e, t, l) {
  var c, o = {}, n = null, r = null;
  l !== void 0 && (n = "" + l), t.key !== void 0 && (n = "" + t.key), t.ref !== void 0 && (r = t.ref);
  for (c in t) We.call(t, c) && !De.hasOwnProperty(c) && (o[c] = t[c]);
  if (e && e.defaultProps) for (c in t = e.defaultProps, t) o[c] === void 0 && (o[c] = t[c]);
  return {
    $$typeof: Le,
    type: e,
    key: n,
    ref: r,
    props: o,
    _owner: Ae.current
  };
}
N.Fragment = Ne;
N.jsx = ne;
N.jsxs = ne;
te.exports = N;
var g = te.exports;
const {
  SvelteComponent: Me,
  assign: q,
  binding_callbacks: V,
  check_outros: Ue,
  children: re,
  claim_element: le,
  claim_space: Be,
  component_subscribe: J,
  compute_slots: He,
  create_slot: ze,
  detach: k,
  element: oe,
  empty: X,
  exclude_internal_props: Y,
  get_all_dirty_from_scope: Ge,
  get_slot_changes: qe,
  group_outros: Ve,
  init: Je,
  insert_hydration: F,
  safe_not_equal: Xe,
  set_custom_element_data: ce,
  space: Ye,
  transition_in: L,
  transition_out: B,
  update_slot_base: Ke
} = window.__gradio__svelte__internal, {
  beforeUpdate: Qe,
  getContext: Ze,
  onDestroy: $e,
  setContext: et
} = window.__gradio__svelte__internal;
function K(e) {
  let t, l;
  const c = (
    /*#slots*/
    e[7].default
  ), o = ze(
    c,
    e,
    /*$$scope*/
    e[6],
    null
  );
  return {
    c() {
      t = oe("svelte-slot"), o && o.c(), this.h();
    },
    l(n) {
      t = le(n, "SVELTE-SLOT", {
        class: !0
      });
      var r = re(t);
      o && o.l(r), r.forEach(k), this.h();
    },
    h() {
      ce(t, "class", "svelte-1rt0kpf");
    },
    m(n, r) {
      F(n, t, r), o && o.m(t, null), e[9](t), l = !0;
    },
    p(n, r) {
      o && o.p && (!l || r & /*$$scope*/
      64) && Ke(
        o,
        c,
        n,
        /*$$scope*/
        n[6],
        l ? qe(
          c,
          /*$$scope*/
          n[6],
          r,
          null
        ) : Ge(
          /*$$scope*/
          n[6]
        ),
        null
      );
    },
    i(n) {
      l || (L(o, n), l = !0);
    },
    o(n) {
      B(o, n), l = !1;
    },
    d(n) {
      n && k(t), o && o.d(n), e[9](null);
    }
  };
}
function tt(e) {
  let t, l, c, o, n = (
    /*$$slots*/
    e[4].default && K(e)
  );
  return {
    c() {
      t = oe("react-portal-target"), l = Ye(), n && n.c(), c = X(), this.h();
    },
    l(r) {
      t = le(r, "REACT-PORTAL-TARGET", {
        class: !0
      }), re(t).forEach(k), l = Be(r), n && n.l(r), c = X(), this.h();
    },
    h() {
      ce(t, "class", "svelte-1rt0kpf");
    },
    m(r, s) {
      F(r, t, s), e[8](t), F(r, l, s), n && n.m(r, s), F(r, c, s), o = !0;
    },
    p(r, [s]) {
      /*$$slots*/
      r[4].default ? n ? (n.p(r, s), s & /*$$slots*/
      16 && L(n, 1)) : (n = K(r), n.c(), L(n, 1), n.m(c.parentNode, c)) : n && (Ve(), B(n, 1, 1, () => {
        n = null;
      }), Ue());
    },
    i(r) {
      o || (L(n), o = !0);
    },
    o(r) {
      B(n), o = !1;
    },
    d(r) {
      r && (k(t), k(l), k(c)), e[8](null), n && n.d(r);
    }
  };
}
function Q(e) {
  const {
    svelteInit: t,
    ...l
  } = e;
  return l;
}
function nt(e, t, l) {
  let c, o, {
    $$slots: n = {},
    $$scope: r
  } = t;
  const s = He(n);
  let {
    svelteInit: u
  } = t;
  const _ = j(Q(t)), x = j();
  J(e, x, (d) => l(0, c = d));
  const i = j();
  J(e, i, (d) => l(1, o = d));
  const w = [], h = Ze("$$ms-gr-react-wrapper"), {
    slotKey: C,
    slotIndex: p,
    subSlotIndex: a
  } = ge() || {}, f = u({
    parent: h,
    props: _,
    target: x,
    slot: i,
    slotKey: C,
    slotIndex: p,
    subSlotIndex: a,
    onDestroy(d) {
      w.push(d);
    }
  });
  et("$$ms-gr-react-wrapper", f), Qe(() => {
    _.set(Q(t));
  }), $e(() => {
    w.forEach((d) => d());
  });
  function b(d) {
    V[d ? "unshift" : "push"](() => {
      c = d, x.set(c);
    });
  }
  function E(d) {
    V[d ? "unshift" : "push"](() => {
      o = d, i.set(o);
    });
  }
  return e.$$set = (d) => {
    l(17, t = q(q({}, t), Y(d))), "svelteInit" in d && l(5, u = d.svelteInit), "$$scope" in d && l(6, r = d.$$scope);
  }, t = Y(t), [c, o, x, i, s, u, r, n, b, E];
}
class rt extends Me {
  constructor(t) {
    super(), Je(this, t, nt, tt, Xe, {
      svelteInit: 5
    });
  }
}
const {
  SvelteComponent: gt
} = window.__gradio__svelte__internal, Z = window.ms_globals.rerender, A = window.ms_globals.tree;
function lt(e, t = {}) {
  function l(c) {
    const o = j(), n = new rt({
      ...c,
      props: {
        svelteInit(r) {
          window.ms_globals.autokey += 1;
          const s = {
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
          }, u = r.parent ?? A;
          return u.nodes = [...u.nodes, s], Z({
            createPortal: D,
            node: A
          }), r.onDestroy(() => {
            u.nodes = u.nodes.filter((_) => _.svelteInstance !== o), Z({
              createPortal: D,
              node: A
            });
          }), s;
        },
        ...c.props
      }
    });
    return o.set(n), n;
  }
  return new Promise((c) => {
    window.ms_globals.initializePromise.then(() => {
      c(l);
    });
  });
}
const ot = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function ct(e) {
  return e ? Object.keys(e).reduce((t, l) => {
    const c = e[l];
    return t[l] = st(l, c), t;
  }, {}) : {};
}
function st(e, t) {
  return typeof t == "number" && !ot.includes(e) ? t + "px" : t;
}
function H(e) {
  const t = [], l = e.cloneNode(!1);
  if (e._reactElement) {
    const o = I.Children.toArray(e._reactElement.props.children).map((n) => {
      if (I.isValidElement(n) && n.props.__slot__) {
        const {
          portals: r,
          clonedElement: s
        } = H(n.props.el);
        return I.cloneElement(n, {
          ...n.props,
          el: s,
          children: [...I.Children.toArray(n.props.children), ...r]
        });
      }
      return null;
    });
    return o.originalChildren = e._reactElement.props.children, t.push(D(I.cloneElement(e._reactElement, {
      ...e._reactElement.props,
      children: o
    }), l)), {
      clonedElement: l,
      portals: t
    };
  }
  Object.keys(e.getEventListeners()).forEach((o) => {
    e.getEventListeners(o).forEach(({
      listener: r,
      type: s,
      useCapture: u
    }) => {
      l.addEventListener(s, r, u);
    });
  });
  const c = Array.from(e.childNodes);
  for (let o = 0; o < c.length; o++) {
    const n = c[o];
    if (n.nodeType === 1) {
      const {
        clonedElement: r,
        portals: s
      } = H(n);
      t.push(...s), l.appendChild(r);
    } else n.nodeType === 3 && l.appendChild(n.cloneNode());
  }
  return {
    clonedElement: l,
    portals: t
  };
}
function it(e, t) {
  e && (typeof e == "function" ? e(t) : e.current = t);
}
const R = ue(({
  slot: e,
  clone: t,
  className: l,
  style: c,
  observeAttributes: o
}, n) => {
  const r = de(), [s, u] = fe([]), {
    forceClone: _
  } = xe(), x = _ ? !0 : t;
  return me(() => {
    var p;
    if (!r.current || !e)
      return;
    let i = e;
    function w() {
      let a = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (a = i.children[0], a.tagName.toLowerCase() === "react-portal-target" && a.children[0] && (a = a.children[0])), it(n, a), l && a.classList.add(...l.split(" ")), c) {
        const f = ct(c);
        Object.keys(f).forEach((b) => {
          a.style[b] = f[b];
        });
      }
    }
    let h = null, C = null;
    if (x && window.MutationObserver) {
      let a = function() {
        var d, v, m;
        (d = r.current) != null && d.contains(i) && ((v = r.current) == null || v.removeChild(i));
        const {
          portals: b,
          clonedElement: E
        } = H(e);
        i = E, u(b), i.style.display = "contents", C && clearTimeout(C), C = setTimeout(() => {
          w();
        }, 50), (m = r.current) == null || m.appendChild(i);
      };
      a();
      const f = je(() => {
        a(), h == null || h.disconnect(), h == null || h.observe(e, {
          childList: !0,
          subtree: !0,
          attributes: o
        });
      }, 50);
      h = new window.MutationObserver(f), h.observe(e, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      i.style.display = "contents", w(), (p = r.current) == null || p.appendChild(i);
    return () => {
      var a, f;
      i.style.display = "", (a = r.current) != null && a.contains(i) && ((f = r.current) == null || f.removeChild(i)), h == null || h.disconnect();
    };
  }, [e, x, l, c, n, o, _]), I.createElement("react-child", {
    ref: r,
    style: {
      display: "contents"
    }
  }, ...s);
});
function at(e) {
  return /^(?:async\s+)?(?:function\s*(?:\w*\s*)?\(|\([\w\s,=]*\)\s*=>|\(\{[\w\s,=]*\}\)\s*=>|function\s*\*\s*\w*\s*\()/i.test(e.trim());
}
function ut(e, t = !1) {
  try {
    if (pe(e))
      return e;
    if (t && !at(e))
      return;
    if (typeof e == "string") {
      let l = e.trim();
      return l.startsWith(";") && (l = l.slice(1)), l.endsWith(";") && (l = l.slice(0, -1)), new Function(`return (...args) => (${l})(...args)`)();
    }
    return;
  } catch {
    return;
  }
}
function T(e, t) {
  return ee(() => ut(e, t), [e, t]);
}
function dt(e, t) {
  return Object.keys(e).reduce((l, c) => (e[c] !== void 0 && (l[c] = e[c]), l), {});
}
const ft = ({
  children: e,
  ...t
}) => /* @__PURE__ */ g.jsx(g.Fragment, {
  children: e(t)
});
function se(e) {
  return I.createElement(ft, {
    children: e
  });
}
function ie(e, t, l) {
  const c = e.filter(Boolean);
  if (c.length !== 0)
    return c.map((o, n) => {
      var _;
      if (typeof o != "object")
        return t != null && t.fallback ? t.fallback(o) : o;
      const r = {
        ...o.props,
        key: ((_ = o.props) == null ? void 0 : _.key) ?? (l ? `${l}-${n}` : `${n}`)
      };
      let s = r;
      Object.keys(o.slots).forEach((x) => {
        if (!o.slots[x] || !(o.slots[x] instanceof Element) && !o.slots[x].el)
          return;
        const i = x.split(".");
        i.forEach((f, b) => {
          s[f] || (s[f] = {}), b !== i.length - 1 && (s = r[f]);
        });
        const w = o.slots[x];
        let h, C, p = (t == null ? void 0 : t.clone) ?? !1, a = t == null ? void 0 : t.forceClone;
        w instanceof Element ? h = w : (h = w.el, C = w.callback, p = w.clone ?? p, a = w.forceClone ?? a), a = a ?? !!C, s[i[i.length - 1]] = h ? C ? (...f) => (C(i[i.length - 1], f), /* @__PURE__ */ g.jsx(U, {
          ...o.ctx,
          params: f,
          forceClone: a,
          children: /* @__PURE__ */ g.jsx(R, {
            slot: h,
            clone: p
          })
        })) : se((f) => /* @__PURE__ */ g.jsx(U, {
          ...o.ctx,
          forceClone: a,
          children: /* @__PURE__ */ g.jsx(R, {
            ...f,
            slot: h,
            clone: p
          })
        })) : s[i[i.length - 1]], s = r;
      });
      const u = (t == null ? void 0 : t.children) || "children";
      return o[u] ? r[u] = ie(o[u], t, `${n}`) : t != null && t.children && (r[u] = void 0, Reflect.deleteProperty(r, u)), r;
    });
}
function $(e, t) {
  return e ? t != null && t.forceClone || t != null && t.params ? se((l) => /* @__PURE__ */ g.jsx(U, {
    forceClone: t == null ? void 0 : t.forceClone,
    params: t == null ? void 0 : t.params,
    children: /* @__PURE__ */ g.jsx(R, {
      slot: e,
      clone: t == null ? void 0 : t.clone,
      ...l
    })
  })) : /* @__PURE__ */ g.jsx(R, {
    slot: e,
    clone: t == null ? void 0 : t.clone
  }) : null;
}
function P({
  key: e,
  slots: t,
  targets: l
}, c) {
  return t[e] ? (...o) => l ? l.map((n, r) => /* @__PURE__ */ g.jsx(I.Fragment, {
    children: $(n, {
      clone: !0,
      params: o,
      forceClone: !0
    })
  }, r)) : /* @__PURE__ */ g.jsx(g.Fragment, {
    children: $(t[e], {
      clone: !0,
      params: o,
      forceClone: !0
    })
  }) : void 0;
}
const {
  withItemsContextProvider: mt,
  useItems: ht,
  ItemHandler: pt
} = Ce("antd-tree-select-tree-nodes"), xt = lt(mt(["default", "treeData"], ({
  slots: e,
  filterTreeNode: t,
  getPopupContainer: l,
  dropdownRender: c,
  popupRender: o,
  tagRender: n,
  treeTitleRender: r,
  treeData: s,
  onValueChange: u,
  onChange: _,
  children: x,
  maxTagPlaceholder: i,
  elRef: w,
  setSlotParams: h,
  onLoadData: C,
  ...p
}) => {
  const a = T(t), f = T(l), b = T(n), E = T(c), d = T(o), v = T(r), {
    items: m
  } = ht(), y = m.treeData.length > 0 ? m.treeData : m.default, S = ee(() => ({
    ...p,
    loadData: C,
    treeData: s || ie(y, {
      clone: !0
    }),
    dropdownRender: e.dropdownRender ? P({
      slots: e,
      key: "dropdownRender"
    }) : E,
    popupRender: e.popupRender ? P({
      slots: e,
      key: "popupRender"
    }) : d,
    allowClear: e["allowClear.clearIcon"] ? {
      clearIcon: /* @__PURE__ */ g.jsx(R, {
        slot: e["allowClear.clearIcon"]
      })
    } : p.allowClear,
    suffixIcon: e.suffixIcon ? /* @__PURE__ */ g.jsx(R, {
      slot: e.suffixIcon
    }) : p.suffixIcon,
    prefix: e.prefix ? /* @__PURE__ */ g.jsx(R, {
      slot: e.prefix
    }) : p.prefix,
    switcherIcon: e.switcherIcon ? P({
      slots: e,
      key: "switcherIcon"
    }) : p.switcherIcon,
    getPopupContainer: f,
    tagRender: e.tagRender ? P({
      slots: e,
      key: "tagRender"
    }) : b,
    treeTitleRender: e.treeTitleRender ? P({
      slots: e,
      key: "treeTitleRender"
    }) : v,
    filterTreeNode: a || t,
    maxTagPlaceholder: e.maxTagPlaceholder ? P({
      slots: e,
      key: "maxTagPlaceholder"
    }) : i,
    notFoundContent: e.notFoundContent ? /* @__PURE__ */ g.jsx(R, {
      slot: e.notFoundContent
    }) : p.notFoundContent
  }), [E, d, t, a, f, i, C, p, h, y, e, b, s, v]);
  return /* @__PURE__ */ g.jsxs(g.Fragment, {
    children: [/* @__PURE__ */ g.jsx("div", {
      style: {
        display: "none"
      },
      children: x
    }), /* @__PURE__ */ g.jsx(we, {
      ...dt(S),
      ref: w,
      onChange: (O, ...ae) => {
        _ == null || _(O, ...ae), u(O);
      }
    })]
  });
}));
export {
  xt as TreeSelect,
  xt as default
};
