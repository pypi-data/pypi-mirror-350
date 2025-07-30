import { i as he, a as A, r as _e, w as j, g as ge, b as we } from "./Index-DzCV6Hds.js";
const E = window.ms_globals.React, ue = window.ms_globals.React.forwardRef, de = window.ms_globals.React.useRef, fe = window.ms_globals.React.useState, me = window.ms_globals.React.useEffect, te = window.ms_globals.React.useMemo, W = window.ms_globals.ReactDOM.createPortal, be = window.ms_globals.internalContext.useContextPropsContext, M = window.ms_globals.internalContext.ContextPropsProvider, z = window.ms_globals.antd.Tree, pe = window.ms_globals.createItemsContext.createItemsContext;
var xe = /\s/;
function ye(e) {
  for (var t = e.length; t-- && xe.test(e.charAt(t)); )
    ;
  return t;
}
var ve = /^\s+/;
function Ce(e) {
  return e && e.slice(0, ye(e) + 1).replace(ve, "");
}
var G = NaN, Ie = /^[-+]0x[0-9a-f]+$/i, Ee = /^0b[01]+$/i, Re = /^0o[0-7]+$/i, Se = parseInt;
function q(e) {
  if (typeof e == "number")
    return e;
  if (he(e))
    return G;
  if (A(e)) {
    var t = typeof e.valueOf == "function" ? e.valueOf() : e;
    e = A(t) ? t + "" : t;
  }
  if (typeof e != "string")
    return e === 0 ? e : +e;
  e = Ce(e);
  var l = Ee.test(e);
  return l || Re.test(e) ? Se(e.slice(2), l ? 2 : 8) : Ie.test(e) ? G : +e;
}
var N = function() {
  return _e.Date.now();
}, Te = "Expected a function", Pe = Math.max, Oe = Math.min;
function je(e, t, l) {
  var s, o, n, r, i, d, _ = 0, g = !1, c = !1, w = !0;
  if (typeof e != "function")
    throw new TypeError(Te);
  t = q(t) || 0, A(l) && (g = !!l.leading, c = "maxWait" in l, n = c ? Pe(q(l.maxWait) || 0, t) : n, w = "trailing" in l ? !!l.trailing : w);
  function a(h) {
    var y = s, C = o;
    return s = o = void 0, _ = h, r = e.apply(C, y), r;
  }
  function p(h) {
    return _ = h, i = setTimeout(m, t), g ? a(h) : r;
  }
  function x(h) {
    var y = h - d, C = h - _, H = t - y;
    return c ? Oe(H, n - C) : H;
  }
  function u(h) {
    var y = h - d, C = h - _;
    return d === void 0 || y >= t || y < 0 || c && C >= n;
  }
  function m() {
    var h = N();
    if (u(h))
      return v(h);
    i = setTimeout(m, x(h));
  }
  function v(h) {
    return i = void 0, w && s ? a(h) : (s = o = void 0, r);
  }
  function R() {
    i !== void 0 && clearTimeout(i), _ = 0, s = d = o = i = void 0;
  }
  function f() {
    return i === void 0 ? r : v(N());
  }
  function I() {
    var h = N(), y = u(h);
    if (s = arguments, o = this, d = h, y) {
      if (i === void 0)
        return p(d);
      if (c)
        return clearTimeout(i), i = setTimeout(m, t), a(d);
    }
    return i === void 0 && (i = setTimeout(m, t)), r;
  }
  return I.cancel = R, I.flush = f, I;
}
var ne = {
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
var ke = E, Le = Symbol.for("react.element"), Fe = Symbol.for("react.fragment"), Ne = Object.prototype.hasOwnProperty, De = ke.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, We = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function re(e, t, l) {
  var s, o = {}, n = null, r = null;
  l !== void 0 && (n = "" + l), t.key !== void 0 && (n = "" + t.key), t.ref !== void 0 && (r = t.ref);
  for (s in t) Ne.call(t, s) && !We.hasOwnProperty(s) && (o[s] = t[s]);
  if (e && e.defaultProps) for (s in t = e.defaultProps, t) o[s] === void 0 && (o[s] = t[s]);
  return {
    $$typeof: Le,
    type: e,
    key: n,
    ref: r,
    props: o,
    _owner: De.current
  };
}
F.Fragment = Fe;
F.jsx = re;
F.jsxs = re;
ne.exports = F;
var b = ne.exports;
const {
  SvelteComponent: Ae,
  assign: V,
  binding_callbacks: J,
  check_outros: Me,
  children: le,
  claim_element: oe,
  claim_space: Ue,
  component_subscribe: X,
  compute_slots: Be,
  create_slot: He,
  detach: S,
  element: se,
  empty: Y,
  exclude_internal_props: K,
  get_all_dirty_from_scope: ze,
  get_slot_changes: Ge,
  group_outros: qe,
  init: Ve,
  insert_hydration: k,
  safe_not_equal: Je,
  set_custom_element_data: ie,
  space: Xe,
  transition_in: L,
  transition_out: U,
  update_slot_base: Ye
} = window.__gradio__svelte__internal, {
  beforeUpdate: Ke,
  getContext: Qe,
  onDestroy: Ze,
  setContext: $e
} = window.__gradio__svelte__internal;
function Q(e) {
  let t, l;
  const s = (
    /*#slots*/
    e[7].default
  ), o = He(
    s,
    e,
    /*$$scope*/
    e[6],
    null
  );
  return {
    c() {
      t = se("svelte-slot"), o && o.c(), this.h();
    },
    l(n) {
      t = oe(n, "SVELTE-SLOT", {
        class: !0
      });
      var r = le(t);
      o && o.l(r), r.forEach(S), this.h();
    },
    h() {
      ie(t, "class", "svelte-1rt0kpf");
    },
    m(n, r) {
      k(n, t, r), o && o.m(t, null), e[9](t), l = !0;
    },
    p(n, r) {
      o && o.p && (!l || r & /*$$scope*/
      64) && Ye(
        o,
        s,
        n,
        /*$$scope*/
        n[6],
        l ? Ge(
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
      l || (L(o, n), l = !0);
    },
    o(n) {
      U(o, n), l = !1;
    },
    d(n) {
      n && S(t), o && o.d(n), e[9](null);
    }
  };
}
function et(e) {
  let t, l, s, o, n = (
    /*$$slots*/
    e[4].default && Q(e)
  );
  return {
    c() {
      t = se("react-portal-target"), l = Xe(), n && n.c(), s = Y(), this.h();
    },
    l(r) {
      t = oe(r, "REACT-PORTAL-TARGET", {
        class: !0
      }), le(t).forEach(S), l = Ue(r), n && n.l(r), s = Y(), this.h();
    },
    h() {
      ie(t, "class", "svelte-1rt0kpf");
    },
    m(r, i) {
      k(r, t, i), e[8](t), k(r, l, i), n && n.m(r, i), k(r, s, i), o = !0;
    },
    p(r, [i]) {
      /*$$slots*/
      r[4].default ? n ? (n.p(r, i), i & /*$$slots*/
      16 && L(n, 1)) : (n = Q(r), n.c(), L(n, 1), n.m(s.parentNode, s)) : n && (qe(), U(n, 1, 1, () => {
        n = null;
      }), Me());
    },
    i(r) {
      o || (L(n), o = !0);
    },
    o(r) {
      U(n), o = !1;
    },
    d(r) {
      r && (S(t), S(l), S(s)), e[8](null), n && n.d(r);
    }
  };
}
function Z(e) {
  const {
    svelteInit: t,
    ...l
  } = e;
  return l;
}
function tt(e, t, l) {
  let s, o, {
    $$slots: n = {},
    $$scope: r
  } = t;
  const i = Be(n);
  let {
    svelteInit: d
  } = t;
  const _ = j(Z(t)), g = j();
  X(e, g, (f) => l(0, s = f));
  const c = j();
  X(e, c, (f) => l(1, o = f));
  const w = [], a = Qe("$$ms-gr-react-wrapper"), {
    slotKey: p,
    slotIndex: x,
    subSlotIndex: u
  } = ge() || {}, m = d({
    parent: a,
    props: _,
    target: g,
    slot: c,
    slotKey: p,
    slotIndex: x,
    subSlotIndex: u,
    onDestroy(f) {
      w.push(f);
    }
  });
  $e("$$ms-gr-react-wrapper", m), Ke(() => {
    _.set(Z(t));
  }), Ze(() => {
    w.forEach((f) => f());
  });
  function v(f) {
    J[f ? "unshift" : "push"](() => {
      s = f, g.set(s);
    });
  }
  function R(f) {
    J[f ? "unshift" : "push"](() => {
      o = f, c.set(o);
    });
  }
  return e.$$set = (f) => {
    l(17, t = V(V({}, t), K(f))), "svelteInit" in f && l(5, d = f.svelteInit), "$$scope" in f && l(6, r = f.$$scope);
  }, t = K(t), [s, o, g, c, i, d, r, n, v, R];
}
class nt extends Ae {
  constructor(t) {
    super(), Ve(this, t, tt, et, Je, {
      svelteInit: 5
    });
  }
}
const {
  SvelteComponent: _t
} = window.__gradio__svelte__internal, $ = window.ms_globals.rerender, D = window.ms_globals.tree;
function rt(e, t = {}) {
  function l(s) {
    const o = j(), n = new nt({
      ...s,
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
          }, d = r.parent ?? D;
          return d.nodes = [...d.nodes, i], $({
            createPortal: W,
            node: D
          }), r.onDestroy(() => {
            d.nodes = d.nodes.filter((_) => _.svelteInstance !== o), $({
              createPortal: W,
              node: D
            });
          }), i;
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
const lt = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function ot(e) {
  return e ? Object.keys(e).reduce((t, l) => {
    const s = e[l];
    return t[l] = st(l, s), t;
  }, {}) : {};
}
function st(e, t) {
  return typeof t == "number" && !lt.includes(e) ? t + "px" : t;
}
function B(e) {
  const t = [], l = e.cloneNode(!1);
  if (e._reactElement) {
    const o = E.Children.toArray(e._reactElement.props.children).map((n) => {
      if (E.isValidElement(n) && n.props.__slot__) {
        const {
          portals: r,
          clonedElement: i
        } = B(n.props.el);
        return E.cloneElement(n, {
          ...n.props,
          el: i,
          children: [...E.Children.toArray(n.props.children), ...r]
        });
      }
      return null;
    });
    return o.originalChildren = e._reactElement.props.children, t.push(W(E.cloneElement(e._reactElement, {
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
      type: i,
      useCapture: d
    }) => {
      l.addEventListener(i, r, d);
    });
  });
  const s = Array.from(e.childNodes);
  for (let o = 0; o < s.length; o++) {
    const n = s[o];
    if (n.nodeType === 1) {
      const {
        clonedElement: r,
        portals: i
      } = B(n);
      t.push(...i), l.appendChild(r);
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
const T = ue(({
  slot: e,
  clone: t,
  className: l,
  style: s,
  observeAttributes: o
}, n) => {
  const r = de(), [i, d] = fe([]), {
    forceClone: _
  } = be(), g = _ ? !0 : t;
  return me(() => {
    var x;
    if (!r.current || !e)
      return;
    let c = e;
    function w() {
      let u = c;
      if (c.tagName.toLowerCase() === "svelte-slot" && c.children.length === 1 && c.children[0] && (u = c.children[0], u.tagName.toLowerCase() === "react-portal-target" && u.children[0] && (u = u.children[0])), it(n, u), l && u.classList.add(...l.split(" ")), s) {
        const m = ot(s);
        Object.keys(m).forEach((v) => {
          u.style[v] = m[v];
        });
      }
    }
    let a = null, p = null;
    if (g && window.MutationObserver) {
      let u = function() {
        var f, I, h;
        (f = r.current) != null && f.contains(c) && ((I = r.current) == null || I.removeChild(c));
        const {
          portals: v,
          clonedElement: R
        } = B(e);
        c = R, d(v), c.style.display = "contents", p && clearTimeout(p), p = setTimeout(() => {
          w();
        }, 50), (h = r.current) == null || h.appendChild(c);
      };
      u();
      const m = je(() => {
        u(), a == null || a.disconnect(), a == null || a.observe(e, {
          childList: !0,
          subtree: !0,
          attributes: o
        });
      }, 50);
      a = new window.MutationObserver(m), a.observe(e, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      c.style.display = "contents", w(), (x = r.current) == null || x.appendChild(c);
    return () => {
      var u, m;
      c.style.display = "", (u = r.current) != null && u.contains(c) && ((m = r.current) == null || m.removeChild(c)), a == null || a.disconnect();
    };
  }, [e, g, l, s, n, o, _]), E.createElement("react-child", {
    ref: r,
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
    if (we(e))
      return e;
    if (t && !ct(e))
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
function P(e, t) {
  return te(() => at(e, t), [e, t]);
}
function ut(e, t) {
  return Object.keys(e).reduce((l, s) => (e[s] !== void 0 && (l[s] = e[s]), l), {});
}
const dt = ({
  children: e,
  ...t
}) => /* @__PURE__ */ b.jsx(b.Fragment, {
  children: e(t)
});
function ce(e) {
  return E.createElement(dt, {
    children: e
  });
}
function ae(e, t, l) {
  const s = e.filter(Boolean);
  if (s.length !== 0)
    return s.map((o, n) => {
      var _;
      if (typeof o != "object")
        return t != null && t.fallback ? t.fallback(o) : o;
      const r = {
        ...o.props,
        key: ((_ = o.props) == null ? void 0 : _.key) ?? (l ? `${l}-${n}` : `${n}`)
      };
      let i = r;
      Object.keys(o.slots).forEach((g) => {
        if (!o.slots[g] || !(o.slots[g] instanceof Element) && !o.slots[g].el)
          return;
        const c = g.split(".");
        c.forEach((m, v) => {
          i[m] || (i[m] = {}), v !== c.length - 1 && (i = r[m]);
        });
        const w = o.slots[g];
        let a, p, x = (t == null ? void 0 : t.clone) ?? !1, u = t == null ? void 0 : t.forceClone;
        w instanceof Element ? a = w : (a = w.el, p = w.callback, x = w.clone ?? x, u = w.forceClone ?? u), u = u ?? !!p, i[c[c.length - 1]] = a ? p ? (...m) => (p(c[c.length - 1], m), /* @__PURE__ */ b.jsx(M, {
          ...o.ctx,
          params: m,
          forceClone: u,
          children: /* @__PURE__ */ b.jsx(T, {
            slot: a,
            clone: x
          })
        })) : ce((m) => /* @__PURE__ */ b.jsx(M, {
          ...o.ctx,
          forceClone: u,
          children: /* @__PURE__ */ b.jsx(T, {
            ...m,
            slot: a,
            clone: x
          })
        })) : i[c[c.length - 1]], i = r;
      });
      const d = (t == null ? void 0 : t.children) || "children";
      return o[d] ? r[d] = ae(o[d], t, `${n}`) : t != null && t.children && (r[d] = void 0, Reflect.deleteProperty(r, d)), r;
    });
}
function ee(e, t) {
  return e ? t != null && t.forceClone || t != null && t.params ? ce((l) => /* @__PURE__ */ b.jsx(M, {
    forceClone: t == null ? void 0 : t.forceClone,
    params: t == null ? void 0 : t.params,
    children: /* @__PURE__ */ b.jsx(T, {
      slot: e,
      clone: t == null ? void 0 : t.clone,
      ...l
    })
  })) : /* @__PURE__ */ b.jsx(T, {
    slot: e,
    clone: t == null ? void 0 : t.clone
  }) : null;
}
function O({
  key: e,
  slots: t,
  targets: l
}, s) {
  return t[e] ? (...o) => l ? l.map((n, r) => /* @__PURE__ */ b.jsx(E.Fragment, {
    children: ee(n, {
      clone: !0,
      params: o,
      forceClone: !0
    })
  }, r)) : /* @__PURE__ */ b.jsx(b.Fragment, {
    children: ee(t[e], {
      clone: !0,
      params: o,
      forceClone: !0
    })
  }) : void 0;
}
const {
  withItemsContextProvider: ft,
  useItems: mt,
  ItemHandler: gt
} = pe("antd-tree-tree-nodes"), wt = rt(ft(["default", "treeData"], ({
  slots: e,
  filterTreeNode: t,
  treeData: l,
  draggable: s,
  allowDrop: o,
  onCheck: n,
  onSelect: r,
  onExpand: i,
  children: d,
  directory: _,
  setSlotParams: g,
  onLoadData: c,
  titleRender: w,
  ...a
}) => {
  const p = P(t), x = P(s), u = P(w), m = P(typeof s == "object" ? s.nodeDraggable : void 0), v = P(o), R = _ ? z.DirectoryTree : z, {
    items: f
  } = mt(), I = f.treeData.length > 0 ? f.treeData : f.default, h = te(() => ({
    ...a,
    treeData: l || ae(I, {
      clone: !0
    }),
    showLine: e["showLine.showLeafIcon"] ? {
      showLeafIcon: O({
        slots: e,
        key: "showLine.showLeafIcon"
      })
    } : a.showLine,
    icon: e.icon ? O({
      slots: e,
      key: "icon"
    }) : a.icon,
    switcherLoadingIcon: e.switcherLoadingIcon ? /* @__PURE__ */ b.jsx(T, {
      slot: e.switcherLoadingIcon
    }) : a.switcherLoadingIcon,
    switcherIcon: e.switcherIcon ? O({
      slots: e,
      key: "switcherIcon"
    }) : a.switcherIcon,
    titleRender: e.titleRender ? O({
      slots: e,
      key: "titleRender"
    }) : u,
    draggable: e["draggable.icon"] || m ? {
      icon: e["draggable.icon"] ? /* @__PURE__ */ b.jsx(T, {
        slot: e["draggable.icon"]
      }) : typeof s == "object" ? s.icon : void 0,
      nodeDraggable: m
    } : x || s,
    loadData: c
  }), [a, l, I, e, g, m, s, u, x, c]);
  return /* @__PURE__ */ b.jsxs(b.Fragment, {
    children: [/* @__PURE__ */ b.jsx("div", {
      style: {
        display: "none"
      },
      children: d
    }), /* @__PURE__ */ b.jsx(R, {
      ...ut(h),
      filterTreeNode: p,
      allowDrop: v,
      onSelect: (y, ...C) => {
        r == null || r(y, ...C);
      },
      onExpand: (y, ...C) => {
        i == null || i(y, ...C);
      },
      onCheck: (y, ...C) => {
        n == null || n(y, ...C);
      }
    })]
  });
}));
export {
  wt as Tree,
  wt as default
};
