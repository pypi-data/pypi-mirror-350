import { i as be, a as B, r as Ie, b as ve, w as F, g as Ee, c as Re } from "./Index-Q7eUC8GS.js";
const R = window.ms_globals.React, ye = window.ms_globals.React.forwardRef, D = window.ms_globals.React.useRef, le = window.ms_globals.React.useState, V = window.ms_globals.React.useEffect, ce = window.ms_globals.React.useMemo, U = window.ms_globals.ReactDOM.createPortal, Se = window.ms_globals.internalContext.useContextPropsContext, H = window.ms_globals.internalContext.ContextPropsProvider, ke = window.ms_globals.antd.Cascader, Pe = window.ms_globals.createItemsContext.createItemsContext;
var je = /\s/;
function Te(e) {
  for (var t = e.length; t-- && je.test(e.charAt(t)); )
    ;
  return t;
}
var Fe = /^\s+/;
function Oe(e) {
  return e && e.slice(0, Te(e) + 1).replace(Fe, "");
}
var X = NaN, Le = /^[-+]0x[0-9a-f]+$/i, Ne = /^0b[01]+$/i, We = /^0o[0-7]+$/i, Ae = parseInt;
function Y(e) {
  if (typeof e == "number")
    return e;
  if (be(e))
    return X;
  if (B(e)) {
    var t = typeof e.valueOf == "function" ? e.valueOf() : e;
    e = B(t) ? t + "" : t;
  }
  if (typeof e != "string")
    return e === 0 ? e : +e;
  e = Oe(e);
  var o = Ne.test(e);
  return o || We.test(e) ? Ae(e.slice(2), o ? 2 : 8) : Le.test(e) ? X : +e;
}
var A = function() {
  return Ie.Date.now();
}, Me = "Expected a function", De = Math.max, Ve = Math.min;
function Ue(e, t, o) {
  var c, l, n, r, s, u, g = 0, x = !1, i = !1, p = !0;
  if (typeof e != "function")
    throw new TypeError(Me);
  t = Y(t) || 0, B(o) && (x = !!o.leading, i = "maxWait" in o, n = i ? De(Y(o.maxWait) || 0, t) : n, p = "trailing" in o ? !!o.trailing : p);
  function d(h) {
    var b = c, P = l;
    return c = l = void 0, g = h, r = e.apply(P, b), r;
  }
  function w(h) {
    return g = h, s = setTimeout(m, t), x ? d(h) : r;
  }
  function C(h) {
    var b = h - u, P = h - g, I = t - b;
    return i ? Ve(I, n - P) : I;
  }
  function a(h) {
    var b = h - u, P = h - g;
    return u === void 0 || b >= t || b < 0 || i && P >= n;
  }
  function m() {
    var h = A();
    if (a(h))
      return y(h);
    s = setTimeout(m, C(h));
  }
  function y(h) {
    return s = void 0, p && c ? d(h) : (c = l = void 0, r);
  }
  function k() {
    s !== void 0 && clearTimeout(s), g = 0, c = u = l = s = void 0;
  }
  function f() {
    return s === void 0 ? r : y(A());
  }
  function S() {
    var h = A(), b = a(h);
    if (c = arguments, l = this, u = h, b) {
      if (s === void 0)
        return w(u);
      if (i)
        return clearTimeout(s), s = setTimeout(m, t), d(u);
    }
    return s === void 0 && (s = setTimeout(m, t)), r;
  }
  return S.cancel = k, S.flush = f, S;
}
function Be(e, t) {
  return ve(e, t);
}
var se = {
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
var He = R, qe = Symbol.for("react.element"), ze = Symbol.for("react.fragment"), Ge = Object.prototype.hasOwnProperty, Je = He.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, Xe = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function ie(e, t, o) {
  var c, l = {}, n = null, r = null;
  o !== void 0 && (n = "" + o), t.key !== void 0 && (n = "" + t.key), t.ref !== void 0 && (r = t.ref);
  for (c in t) Ge.call(t, c) && !Xe.hasOwnProperty(c) && (l[c] = t[c]);
  if (e && e.defaultProps) for (c in t = e.defaultProps, t) l[c] === void 0 && (l[c] = t[c]);
  return {
    $$typeof: qe,
    type: e,
    key: n,
    ref: r,
    props: l,
    _owner: Je.current
  };
}
N.Fragment = ze;
N.jsx = ie;
N.jsxs = ie;
se.exports = N;
var _ = se.exports;
const {
  SvelteComponent: Ye,
  assign: K,
  binding_callbacks: Q,
  check_outros: Ke,
  children: ae,
  claim_element: ue,
  claim_space: Qe,
  component_subscribe: Z,
  compute_slots: Ze,
  create_slot: $e,
  detach: T,
  element: de,
  empty: $,
  exclude_internal_props: ee,
  get_all_dirty_from_scope: et,
  get_slot_changes: tt,
  group_outros: nt,
  init: rt,
  insert_hydration: O,
  safe_not_equal: ot,
  set_custom_element_data: fe,
  space: lt,
  transition_in: L,
  transition_out: q,
  update_slot_base: ct
} = window.__gradio__svelte__internal, {
  beforeUpdate: st,
  getContext: it,
  onDestroy: at,
  setContext: ut
} = window.__gradio__svelte__internal;
function te(e) {
  let t, o;
  const c = (
    /*#slots*/
    e[7].default
  ), l = $e(
    c,
    e,
    /*$$scope*/
    e[6],
    null
  );
  return {
    c() {
      t = de("svelte-slot"), l && l.c(), this.h();
    },
    l(n) {
      t = ue(n, "SVELTE-SLOT", {
        class: !0
      });
      var r = ae(t);
      l && l.l(r), r.forEach(T), this.h();
    },
    h() {
      fe(t, "class", "svelte-1rt0kpf");
    },
    m(n, r) {
      O(n, t, r), l && l.m(t, null), e[9](t), o = !0;
    },
    p(n, r) {
      l && l.p && (!o || r & /*$$scope*/
      64) && ct(
        l,
        c,
        n,
        /*$$scope*/
        n[6],
        o ? tt(
          c,
          /*$$scope*/
          n[6],
          r,
          null
        ) : et(
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
      q(l, n), o = !1;
    },
    d(n) {
      n && T(t), l && l.d(n), e[9](null);
    }
  };
}
function dt(e) {
  let t, o, c, l, n = (
    /*$$slots*/
    e[4].default && te(e)
  );
  return {
    c() {
      t = de("react-portal-target"), o = lt(), n && n.c(), c = $(), this.h();
    },
    l(r) {
      t = ue(r, "REACT-PORTAL-TARGET", {
        class: !0
      }), ae(t).forEach(T), o = Qe(r), n && n.l(r), c = $(), this.h();
    },
    h() {
      fe(t, "class", "svelte-1rt0kpf");
    },
    m(r, s) {
      O(r, t, s), e[8](t), O(r, o, s), n && n.m(r, s), O(r, c, s), l = !0;
    },
    p(r, [s]) {
      /*$$slots*/
      r[4].default ? n ? (n.p(r, s), s & /*$$slots*/
      16 && L(n, 1)) : (n = te(r), n.c(), L(n, 1), n.m(c.parentNode, c)) : n && (nt(), q(n, 1, 1, () => {
        n = null;
      }), Ke());
    },
    i(r) {
      l || (L(n), l = !0);
    },
    o(r) {
      q(n), l = !1;
    },
    d(r) {
      r && (T(t), T(o), T(c)), e[8](null), n && n.d(r);
    }
  };
}
function ne(e) {
  const {
    svelteInit: t,
    ...o
  } = e;
  return o;
}
function ft(e, t, o) {
  let c, l, {
    $$slots: n = {},
    $$scope: r
  } = t;
  const s = Ze(n);
  let {
    svelteInit: u
  } = t;
  const g = F(ne(t)), x = F();
  Z(e, x, (f) => o(0, c = f));
  const i = F();
  Z(e, i, (f) => o(1, l = f));
  const p = [], d = it("$$ms-gr-react-wrapper"), {
    slotKey: w,
    slotIndex: C,
    subSlotIndex: a
  } = Ee() || {}, m = u({
    parent: d,
    props: g,
    target: x,
    slot: i,
    slotKey: w,
    slotIndex: C,
    subSlotIndex: a,
    onDestroy(f) {
      p.push(f);
    }
  });
  ut("$$ms-gr-react-wrapper", m), st(() => {
    g.set(ne(t));
  }), at(() => {
    p.forEach((f) => f());
  });
  function y(f) {
    Q[f ? "unshift" : "push"](() => {
      c = f, x.set(c);
    });
  }
  function k(f) {
    Q[f ? "unshift" : "push"](() => {
      l = f, i.set(l);
    });
  }
  return e.$$set = (f) => {
    o(17, t = K(K({}, t), ee(f))), "svelteInit" in f && o(5, u = f.svelteInit), "$$scope" in f && o(6, r = f.$$scope);
  }, t = ee(t), [c, l, x, i, s, u, r, n, y, k];
}
class mt extends Ye {
  constructor(t) {
    super(), rt(this, t, ft, dt, ot, {
      svelteInit: 5
    });
  }
}
const {
  SvelteComponent: St
} = window.__gradio__svelte__internal, re = window.ms_globals.rerender, M = window.ms_globals.tree;
function ht(e, t = {}) {
  function o(c) {
    const l = F(), n = new mt({
      ...c,
      props: {
        svelteInit(r) {
          window.ms_globals.autokey += 1;
          const s = {
            key: window.ms_globals.autokey,
            svelteInstance: l,
            reactComponent: e,
            props: r.props,
            slot: r.slot,
            target: r.target,
            slotIndex: r.slotIndex,
            subSlotIndex: r.subSlotIndex,
            ignore: t.ignore,
            slotKey: r.slotKey,
            nodes: []
          }, u = r.parent ?? M;
          return u.nodes = [...u.nodes, s], re({
            createPortal: U,
            node: M
          }), r.onDestroy(() => {
            u.nodes = u.nodes.filter((g) => g.svelteInstance !== l), re({
              createPortal: U,
              node: M
            });
          }), s;
        },
        ...c.props
      }
    });
    return l.set(n), n;
  }
  return new Promise((c) => {
    window.ms_globals.initializePromise.then(() => {
      c(o);
    });
  });
}
const _t = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function pt(e) {
  return e ? Object.keys(e).reduce((t, o) => {
    const c = e[o];
    return t[o] = gt(o, c), t;
  }, {}) : {};
}
function gt(e, t) {
  return typeof t == "number" && !_t.includes(e) ? t + "px" : t;
}
function z(e) {
  const t = [], o = e.cloneNode(!1);
  if (e._reactElement) {
    const l = R.Children.toArray(e._reactElement.props.children).map((n) => {
      if (R.isValidElement(n) && n.props.__slot__) {
        const {
          portals: r,
          clonedElement: s
        } = z(n.props.el);
        return R.cloneElement(n, {
          ...n.props,
          el: s,
          children: [...R.Children.toArray(n.props.children), ...r]
        });
      }
      return null;
    });
    return l.originalChildren = e._reactElement.props.children, t.push(U(R.cloneElement(e._reactElement, {
      ...e._reactElement.props,
      children: l
    }), o)), {
      clonedElement: o,
      portals: t
    };
  }
  Object.keys(e.getEventListeners()).forEach((l) => {
    e.getEventListeners(l).forEach(({
      listener: r,
      type: s,
      useCapture: u
    }) => {
      o.addEventListener(s, r, u);
    });
  });
  const c = Array.from(e.childNodes);
  for (let l = 0; l < c.length; l++) {
    const n = c[l];
    if (n.nodeType === 1) {
      const {
        clonedElement: r,
        portals: s
      } = z(n);
      t.push(...s), o.appendChild(r);
    } else n.nodeType === 3 && o.appendChild(n.cloneNode());
  }
  return {
    clonedElement: o,
    portals: t
  };
}
function xt(e, t) {
  e && (typeof e == "function" ? e(t) : e.current = t);
}
const E = ye(({
  slot: e,
  clone: t,
  className: o,
  style: c,
  observeAttributes: l
}, n) => {
  const r = D(), [s, u] = le([]), {
    forceClone: g
  } = Se(), x = g ? !0 : t;
  return V(() => {
    var C;
    if (!r.current || !e)
      return;
    let i = e;
    function p() {
      let a = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (a = i.children[0], a.tagName.toLowerCase() === "react-portal-target" && a.children[0] && (a = a.children[0])), xt(n, a), o && a.classList.add(...o.split(" ")), c) {
        const m = pt(c);
        Object.keys(m).forEach((y) => {
          a.style[y] = m[y];
        });
      }
    }
    let d = null, w = null;
    if (x && window.MutationObserver) {
      let a = function() {
        var f, S, h;
        (f = r.current) != null && f.contains(i) && ((S = r.current) == null || S.removeChild(i));
        const {
          portals: y,
          clonedElement: k
        } = z(e);
        i = k, u(y), i.style.display = "contents", w && clearTimeout(w), w = setTimeout(() => {
          p();
        }, 50), (h = r.current) == null || h.appendChild(i);
      };
      a();
      const m = Ue(() => {
        a(), d == null || d.disconnect(), d == null || d.observe(e, {
          childList: !0,
          subtree: !0,
          attributes: l
        });
      }, 50);
      d = new window.MutationObserver(m), d.observe(e, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      i.style.display = "contents", p(), (C = r.current) == null || C.appendChild(i);
    return () => {
      var a, m;
      i.style.display = "", (a = r.current) != null && a.contains(i) && ((m = r.current) == null || m.removeChild(i)), d == null || d.disconnect();
    };
  }, [e, x, o, c, n, l, g]), R.createElement("react-child", {
    ref: r,
    style: {
      display: "contents"
    }
  }, ...s);
});
function wt(e) {
  return /^(?:async\s+)?(?:function\s*(?:\w*\s*)?\(|\([\w\s,=]*\)\s*=>|\(\{[\w\s,=]*\}\)\s*=>|function\s*\*\s*\w*\s*\()/i.test(e.trim());
}
function Ct(e, t = !1) {
  try {
    if (Re(e))
      return e;
    if (t && !wt(e))
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
function v(e, t) {
  return ce(() => Ct(e, t), [e, t]);
}
function yt({
  value: e,
  onValueChange: t
}) {
  const [o, c] = le(e), l = D(t);
  l.current = t;
  const n = D(o);
  return n.current = o, V(() => {
    l.current(o);
  }, [o]), V(() => {
    Be(e, n.current) || c(e);
  }, [e]), [o, c];
}
const bt = ({
  children: e,
  ...t
}) => /* @__PURE__ */ _.jsx(_.Fragment, {
  children: e(t)
});
function me(e) {
  return R.createElement(bt, {
    children: e
  });
}
function he(e, t, o) {
  const c = e.filter(Boolean);
  if (c.length !== 0)
    return c.map((l, n) => {
      var g;
      if (typeof l != "object")
        return t != null && t.fallback ? t.fallback(l) : l;
      const r = {
        ...l.props,
        key: ((g = l.props) == null ? void 0 : g.key) ?? (o ? `${o}-${n}` : `${n}`)
      };
      let s = r;
      Object.keys(l.slots).forEach((x) => {
        if (!l.slots[x] || !(l.slots[x] instanceof Element) && !l.slots[x].el)
          return;
        const i = x.split(".");
        i.forEach((m, y) => {
          s[m] || (s[m] = {}), y !== i.length - 1 && (s = r[m]);
        });
        const p = l.slots[x];
        let d, w, C = (t == null ? void 0 : t.clone) ?? !1, a = t == null ? void 0 : t.forceClone;
        p instanceof Element ? d = p : (d = p.el, w = p.callback, C = p.clone ?? C, a = p.forceClone ?? a), a = a ?? !!w, s[i[i.length - 1]] = d ? w ? (...m) => (w(i[i.length - 1], m), /* @__PURE__ */ _.jsx(H, {
          ...l.ctx,
          params: m,
          forceClone: a,
          children: /* @__PURE__ */ _.jsx(E, {
            slot: d,
            clone: C
          })
        })) : me((m) => /* @__PURE__ */ _.jsx(H, {
          ...l.ctx,
          forceClone: a,
          children: /* @__PURE__ */ _.jsx(E, {
            ...m,
            slot: d,
            clone: C
          })
        })) : s[i[i.length - 1]], s = r;
      });
      const u = (t == null ? void 0 : t.children) || "children";
      return l[u] ? r[u] = he(l[u], t, `${n}`) : t != null && t.children && (r[u] = void 0, Reflect.deleteProperty(r, u)), r;
    });
}
function oe(e, t) {
  return e ? t != null && t.forceClone || t != null && t.params ? me((o) => /* @__PURE__ */ _.jsx(H, {
    forceClone: t == null ? void 0 : t.forceClone,
    params: t == null ? void 0 : t.params,
    children: /* @__PURE__ */ _.jsx(E, {
      slot: e,
      clone: t == null ? void 0 : t.clone,
      ...o
    })
  })) : /* @__PURE__ */ _.jsx(E, {
    slot: e,
    clone: t == null ? void 0 : t.clone
  }) : null;
}
function j({
  key: e,
  slots: t,
  targets: o
}, c) {
  return t[e] ? (...l) => o ? o.map((n, r) => /* @__PURE__ */ _.jsx(R.Fragment, {
    children: oe(n, {
      clone: !0,
      params: l,
      forceClone: !0
    })
  }, r)) : /* @__PURE__ */ _.jsx(_.Fragment, {
    children: oe(t[e], {
      clone: !0,
      params: l,
      forceClone: !0
    })
  }) : void 0;
}
const {
  useItems: It,
  withItemsContextProvider: vt,
  ItemHandler: kt
} = Pe("antd-cascader-options");
function Et(e) {
  return typeof e == "object" && e !== null ? e : {};
}
const Pt = ht(vt(["default", "options"], ({
  slots: e,
  children: t,
  onValueChange: o,
  onChange: c,
  displayRender: l,
  elRef: n,
  getPopupContainer: r,
  tagRender: s,
  maxTagPlaceholder: u,
  dropdownRender: g,
  popupRender: x,
  optionRender: i,
  showSearch: p,
  options: d,
  setSlotParams: w,
  onLoadData: C,
  ...a
}) => {
  const m = v(r), y = v(l), k = v(s), f = v(i), S = v(g), h = v(x), b = v(u), P = typeof p == "object" || e["showSearch.render"], I = Et(p), _e = v(I.filter), pe = v(I.render), ge = v(I.sort), [xe, we] = yt({
    onValueChange: o,
    value: a.value
  }), {
    items: W
  } = It(), G = W.options.length > 0 ? W.options : W.default;
  return /* @__PURE__ */ _.jsxs(_.Fragment, {
    children: [/* @__PURE__ */ _.jsx("div", {
      style: {
        display: "none"
      },
      children: t
    }), /* @__PURE__ */ _.jsx(ke, {
      ...a,
      ref: n,
      value: xe,
      options: ce(() => d || he(G, {
        clone: !0
      }), [d, G]),
      showSearch: P ? {
        ...I,
        filter: _e || I.filter,
        render: e["showSearch.render"] ? j({
          slots: e,
          key: "showSearch.render"
        }) : pe || I.render,
        sort: ge || I.sort
      } : p,
      loadData: C,
      optionRender: f,
      getPopupContainer: m,
      prefix: e.prefix ? /* @__PURE__ */ _.jsx(E, {
        slot: e.prefix
      }) : a.prefix,
      dropdownRender: e.dropdownRender ? j({
        slots: e,
        key: "dropdownRender"
      }) : S,
      popupRender: e.popupRender ? j({
        slots: e,
        key: "popupRender"
      }) : h,
      displayRender: e.displayRender ? j({
        slots: e,
        key: "displayRender"
      }) : y,
      tagRender: e.tagRender ? j({
        slots: e,
        key: "tagRender"
      }) : k,
      onChange: (J, ...Ce) => {
        c == null || c(J, ...Ce), we(J);
      },
      suffixIcon: e.suffixIcon ? /* @__PURE__ */ _.jsx(E, {
        slot: e.suffixIcon
      }) : a.suffixIcon,
      expandIcon: e.expandIcon ? /* @__PURE__ */ _.jsx(E, {
        slot: e.expandIcon
      }) : a.expandIcon,
      removeIcon: e.removeIcon ? /* @__PURE__ */ _.jsx(E, {
        slot: e.removeIcon
      }) : a.removeIcon,
      notFoundContent: e.notFoundContent ? /* @__PURE__ */ _.jsx(E, {
        slot: e.notFoundContent
      }) : a.notFoundContent,
      maxTagPlaceholder: e.maxTagPlaceholder ? j({
        slots: e,
        key: "maxTagPlaceholder"
      }) : b || u,
      allowClear: e["allowClear.clearIcon"] ? {
        clearIcon: /* @__PURE__ */ _.jsx(E, {
          slot: e["allowClear.clearIcon"]
        })
      } : a.allowClear
    })]
  });
}));
export {
  Pt as Cascader,
  Pt as default
};
