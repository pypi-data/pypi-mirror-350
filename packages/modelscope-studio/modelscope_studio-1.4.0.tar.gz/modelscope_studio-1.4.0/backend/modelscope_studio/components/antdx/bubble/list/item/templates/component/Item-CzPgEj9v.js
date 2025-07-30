import { i as ae, a as B, r as ue, m as fe, b as de, c as me, d as _e } from "./Index-CQKnXL9C.js";
const I = window.ms_globals.React, pe = window.ms_globals.React.forwardRef, ge = window.ms_globals.React.useRef, be = window.ms_globals.React.useState, he = window.ms_globals.React.useEffect, ye = window.ms_globals.internalContext.useContextPropsContext, xe = window.ms_globals.ReactDOM.createPortal;
var Pe = /\s/;
function Ce(e) {
  for (var t = e.length; t-- && Pe.test(e.charAt(t)); )
    ;
  return t;
}
var Ee = /^\s+/;
function ve(e) {
  return e && e.slice(0, Ce(e) + 1).replace(Ee, "");
}
var G = NaN, Se = /^[-+]0x[0-9a-f]+$/i, Re = /^0b[01]+$/i, ke = /^0o[0-7]+$/i, we = parseInt;
function V(e) {
  if (typeof e == "number")
    return e;
  if (ae(e))
    return G;
  if (B(e)) {
    var t = typeof e.valueOf == "function" ? e.valueOf() : e;
    e = B(t) ? t + "" : t;
  }
  if (typeof e != "string")
    return e === 0 ? e : +e;
  e = ve(e);
  var r = Re.test(e);
  return r || ke.test(e) ? we(e.slice(2), r ? 2 : 8) : Se.test(e) ? G : +e;
}
var q = function() {
  return ue.Date.now();
}, Ie = "Expected a function", Oe = Math.max, Fe = Math.min;
function Te(e, t, r) {
  var s, o, n, i, l, p, m = 0, y = !1, u = !1, f = !0;
  if (typeof e != "function")
    throw new TypeError(Ie);
  t = V(t) || 0, B(r) && (y = !!r.leading, u = "maxWait" in r, n = u ? Oe(V(r.maxWait) || 0, t) : n, f = "trailing" in r ? !!r.trailing : f);
  function a(d) {
    var x = s, P = o;
    return s = o = void 0, m = d, i = e.apply(P, x), i;
  }
  function C(d) {
    return m = d, l = setTimeout(g, t), y ? a(d) : i;
  }
  function E(d) {
    var x = d - p, P = d - m, M = t - x;
    return u ? Fe(M, n - P) : M;
  }
  function _(d) {
    var x = d - p, P = d - m;
    return p === void 0 || x >= t || x < 0 || u && P >= n;
  }
  function g() {
    var d = q();
    if (_(d))
      return h(d);
    l = setTimeout(g, E(d));
  }
  function h(d) {
    return l = void 0, f && s ? a(d) : (s = o = void 0, i);
  }
  function k() {
    l !== void 0 && clearTimeout(l), m = 0, s = p = o = l = void 0;
  }
  function v() {
    return l === void 0 ? i : h(q());
  }
  function S() {
    var d = q(), x = _(d);
    if (s = arguments, o = this, p = d, x) {
      if (l === void 0)
        return C(p);
      if (u)
        return clearTimeout(l), l = setTimeout(g, t), a(p);
    }
    return l === void 0 && (l = setTimeout(g, t)), i;
  }
  return S.cancel = k, S.flush = v, S;
}
function L() {
}
function Me(e, t) {
  return e != e ? t == t : e !== t || e && typeof e == "object" || typeof e == "function";
}
function je(e, ...t) {
  if (e == null) {
    for (const s of t)
      s(void 0);
    return L;
  }
  const r = e.subscribe(...t);
  return r.unsubscribe ? () => r.unsubscribe() : r;
}
function Z(e) {
  let t;
  return je(e, (r) => t = r)(), t;
}
const O = [];
function R(e, t = L) {
  let r;
  const s = /* @__PURE__ */ new Set();
  function o(l) {
    if (Me(e, l) && (e = l, r)) {
      const p = !O.length;
      for (const m of s)
        m[1](), O.push(m, e);
      if (p) {
        for (let m = 0; m < O.length; m += 2)
          O[m][0](O[m + 1]);
        O.length = 0;
      }
    }
  }
  function n(l) {
    o(l(e));
  }
  function i(l, p = L) {
    const m = [l, p];
    return s.add(m), s.size === 1 && (r = t(o, n) || L), l(e), () => {
      s.delete(m), s.size === 0 && r && (r(), r = null);
    };
  }
  return {
    set: o,
    update: n,
    subscribe: i
  };
}
const {
  getContext: Ke,
  setContext: Lt
} = window.__gradio__svelte__internal, Le = "$$ms-gr-loading-status-key";
function Ne() {
  const e = window.ms_globals.loadingKey++, t = Ke(Le);
  return (r) => {
    if (!t || !r)
      return;
    const {
      loadingStatusMap: s,
      options: o
    } = t, {
      generating: n,
      error: i
    } = Z(o);
    (r == null ? void 0 : r.status) === "pending" || i && (r == null ? void 0 : r.status) === "error" || (n && (r == null ? void 0 : r.status)) === "generating" ? s.update(({
      map: l
    }) => (l.set(e, r), {
      map: l
    })) : s.update(({
      map: l
    }) => (l.delete(e), {
      map: l
    }));
  };
}
const {
  getContext: A,
  setContext: T
} = window.__gradio__svelte__internal, Ae = "$$ms-gr-slots-key";
function We() {
  const e = R({});
  return T(Ae, e);
}
const $ = "$$ms-gr-slot-params-mapping-fn-key";
function qe() {
  return A($);
}
function ze(e) {
  return T($, R(e));
}
const Be = "$$ms-gr-slot-params-key";
function De() {
  const e = T(Be, R({}));
  return (t, r) => {
    e.update((s) => typeof r == "function" ? {
      ...s,
      [t]: r(s[t])
    } : {
      ...s,
      [t]: r
    });
  };
}
const ee = "$$ms-gr-sub-index-context-key";
function Ue() {
  return A(ee) || null;
}
function J(e) {
  return T(ee, e);
}
function He(e, t, r) {
  if (!Reflect.has(e, "as_item") || !Reflect.has(e, "_internal"))
    throw new Error("`as_item` and `_internal` is required");
  const s = ne(), o = qe();
  ze().set(void 0);
  const i = Ve({
    slot: void 0,
    index: e._internal.index,
    subIndex: e._internal.subIndex
  }), l = Ue();
  typeof l == "number" && J(void 0);
  const p = Ne();
  typeof e._internal.subIndex == "number" && J(e._internal.subIndex), s && s.subscribe((f) => {
    i.slotKey.set(f);
  }), Ge();
  const m = e.as_item, y = (f, a) => f ? {
    ...fe({
      ...f
    }, t),
    __render_slotParamsMappingFn: o ? Z(o) : void 0,
    __render_as_item: a,
    __render_restPropsMapping: t
  } : void 0, u = R({
    ...e,
    _internal: {
      ...e._internal,
      index: l ?? e._internal.index
    },
    restProps: y(e.restProps, m),
    originalRestProps: e.restProps
  });
  return o && o.subscribe((f) => {
    u.update((a) => ({
      ...a,
      restProps: {
        ...a.restProps,
        __slotParamsMappingFn: f
      }
    }));
  }), [u, (f) => {
    var a;
    p((a = f.restProps) == null ? void 0 : a.loading_status), u.set({
      ...f,
      _internal: {
        ...f._internal,
        index: l ?? f._internal.index
      },
      restProps: y(f.restProps, f.as_item),
      originalRestProps: f.restProps
    });
  }];
}
const te = "$$ms-gr-slot-key";
function Ge() {
  T(te, R(void 0));
}
function ne() {
  return A(te);
}
const re = "$$ms-gr-component-slot-context-key";
function Ve({
  slot: e,
  index: t,
  subIndex: r
}) {
  return T(re, {
    slotKey: R(e),
    slotIndex: R(t),
    subSlotIndex: R(r)
  });
}
function Nt() {
  return A(re);
}
function Je(e) {
  return /^(?:async\s+)?(?:function\s*(?:\w*\s*)?\(|\([\w\s,=]*\)\s*=>|\(\{[\w\s,=]*\}\)\s*=>|function\s*\*\s*\w*\s*\()/i.test(e.trim());
}
function X(e, t = !1) {
  try {
    if (de(e))
      return e;
    if (t && !Je(e))
      return;
    if (typeof e == "string") {
      let r = e.trim();
      return r.startsWith(";") && (r = r.slice(1)), r.endsWith(";") && (r = r.slice(0, -1)), new Function(`return (...args) => (${r})(...args)`)();
    }
    return;
  } catch {
    return;
  }
}
function Xe(e) {
  return e && e.__esModule && Object.prototype.hasOwnProperty.call(e, "default") ? e.default : e;
}
var se = {
  exports: {}
}, W = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var Ye = I, Qe = Symbol.for("react.element"), Ze = Symbol.for("react.fragment"), $e = Object.prototype.hasOwnProperty, et = Ye.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, tt = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function oe(e, t, r) {
  var s, o = {}, n = null, i = null;
  r !== void 0 && (n = "" + r), t.key !== void 0 && (n = "" + t.key), t.ref !== void 0 && (i = t.ref);
  for (s in t) $e.call(t, s) && !tt.hasOwnProperty(s) && (o[s] = t[s]);
  if (e && e.defaultProps) for (s in t = e.defaultProps, t) o[s] === void 0 && (o[s] = t[s]);
  return {
    $$typeof: Qe,
    type: e,
    key: n,
    ref: i,
    props: o,
    _owner: et.current
  };
}
W.Fragment = Ze;
W.jsx = oe;
W.jsxs = oe;
se.exports = W;
var nt = se.exports;
const rt = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function st(e) {
  return e ? Object.keys(e).reduce((t, r) => {
    const s = e[r];
    return t[r] = ot(r, s), t;
  }, {}) : {};
}
function ot(e, t) {
  return typeof t == "number" && !rt.includes(e) ? t + "px" : t;
}
function D(e) {
  const t = [], r = e.cloneNode(!1);
  if (e._reactElement) {
    const o = I.Children.toArray(e._reactElement.props.children).map((n) => {
      if (I.isValidElement(n) && n.props.__slot__) {
        const {
          portals: i,
          clonedElement: l
        } = D(n.props.el);
        return I.cloneElement(n, {
          ...n.props,
          el: l,
          children: [...I.Children.toArray(n.props.children), ...i]
        });
      }
      return null;
    });
    return o.originalChildren = e._reactElement.props.children, t.push(xe(I.cloneElement(e._reactElement, {
      ...e._reactElement.props,
      children: o
    }), r)), {
      clonedElement: r,
      portals: t
    };
  }
  Object.keys(e.getEventListeners()).forEach((o) => {
    e.getEventListeners(o).forEach(({
      listener: i,
      type: l,
      useCapture: p
    }) => {
      r.addEventListener(l, i, p);
    });
  });
  const s = Array.from(e.childNodes);
  for (let o = 0; o < s.length; o++) {
    const n = s[o];
    if (n.nodeType === 1) {
      const {
        clonedElement: i,
        portals: l
      } = D(n);
      t.push(...l), r.appendChild(i);
    } else n.nodeType === 3 && r.appendChild(n.cloneNode());
  }
  return {
    clonedElement: r,
    portals: t
  };
}
function it(e, t) {
  e && (typeof e == "function" ? e(t) : e.current = t);
}
const lt = pe(({
  slot: e,
  clone: t,
  className: r,
  style: s,
  observeAttributes: o
}, n) => {
  const i = ge(), [l, p] = be([]), {
    forceClone: m
  } = ye(), y = m ? !0 : t;
  return he(() => {
    var E;
    if (!i.current || !e)
      return;
    let u = e;
    function f() {
      let _ = u;
      if (u.tagName.toLowerCase() === "svelte-slot" && u.children.length === 1 && u.children[0] && (_ = u.children[0], _.tagName.toLowerCase() === "react-portal-target" && _.children[0] && (_ = _.children[0])), it(n, _), r && _.classList.add(...r.split(" ")), s) {
        const g = st(s);
        Object.keys(g).forEach((h) => {
          _.style[h] = g[h];
        });
      }
    }
    let a = null, C = null;
    if (y && window.MutationObserver) {
      let _ = function() {
        var v, S, d;
        (v = i.current) != null && v.contains(u) && ((S = i.current) == null || S.removeChild(u));
        const {
          portals: h,
          clonedElement: k
        } = D(e);
        u = k, p(h), u.style.display = "contents", C && clearTimeout(C), C = setTimeout(() => {
          f();
        }, 50), (d = i.current) == null || d.appendChild(u);
      };
      _();
      const g = Te(() => {
        _(), a == null || a.disconnect(), a == null || a.observe(e, {
          childList: !0,
          subtree: !0,
          attributes: o
        });
      }, 50);
      a = new window.MutationObserver(g), a.observe(e, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      u.style.display = "contents", f(), (E = i.current) == null || E.appendChild(u);
    return () => {
      var _, g;
      u.style.display = "", (_ = i.current) != null && _.contains(u) && ((g = i.current) == null || g.removeChild(u)), a == null || a.disconnect();
    };
  }, [e, y, r, s, n, o, m]), I.createElement("react-child", {
    ref: i,
    style: {
      display: "contents"
    }
  }, ...l);
});
function z(e, t) {
  return e ? /* @__PURE__ */ nt.jsx(lt, {
    slot: e,
    clone: t == null ? void 0 : t.clone
  }) : null;
}
var ie = {
  exports: {}
};
/*!
	Copyright (c) 2018 Jed Watson.
	Licensed under the MIT License (MIT), see
	http://jedwatson.github.io/classnames
*/
(function(e) {
  (function() {
    var t = {}.hasOwnProperty;
    function r() {
      for (var n = "", i = 0; i < arguments.length; i++) {
        var l = arguments[i];
        l && (n = o(n, s(l)));
      }
      return n;
    }
    function s(n) {
      if (typeof n == "string" || typeof n == "number")
        return n;
      if (typeof n != "object")
        return "";
      if (Array.isArray(n))
        return r.apply(null, n);
      if (n.toString !== Object.prototype.toString && !n.toString.toString().includes("[native code]"))
        return n.toString();
      var i = "";
      for (var l in n)
        t.call(n, l) && n[l] && (i = o(i, l));
      return i;
    }
    function o(n, i) {
      return i ? n ? n + " " + i : n + i : n;
    }
    e.exports ? (r.default = r, e.exports = r) : window.classNames = r;
  })();
})(ie);
var ct = ie.exports;
const at = /* @__PURE__ */ Xe(ct), {
  SvelteComponent: ut,
  assign: U,
  check_outros: ft,
  claim_component: dt,
  component_subscribe: K,
  compute_rest_props: Y,
  create_component: mt,
  create_slot: _t,
  destroy_component: pt,
  detach: le,
  empty: N,
  exclude_internal_props: gt,
  flush: w,
  get_all_dirty_from_scope: bt,
  get_slot_changes: ht,
  get_spread_object: yt,
  get_spread_update: xt,
  group_outros: Pt,
  handle_promise: Ct,
  init: Et,
  insert_hydration: ce,
  mount_component: vt,
  noop: b,
  safe_not_equal: St,
  transition_in: F,
  transition_out: j,
  update_await_block_branch: Rt,
  update_slot_base: kt
} = window.__gradio__svelte__internal;
function wt(e) {
  return {
    c: b,
    l: b,
    m: b,
    p: b,
    i: b,
    o: b,
    d: b
  };
}
function It(e) {
  let t, r;
  const s = [
    /*itemProps*/
    e[1].props,
    {
      slots: (
        /*itemProps*/
        e[1].slots
      )
    },
    {
      itemIndex: (
        /*$mergedProps*/
        e[0]._internal.index || 0
      )
    },
    {
      itemSlotKey: (
        /*$slotKey*/
        e[2]
      )
    }
  ];
  let o = {
    $$slots: {
      default: [Ot]
    },
    $$scope: {
      ctx: e
    }
  };
  for (let n = 0; n < s.length; n += 1)
    o = U(o, s[n]);
  return t = new /*BubbleListItem*/
  e[23]({
    props: o
  }), {
    c() {
      mt(t.$$.fragment);
    },
    l(n) {
      dt(t.$$.fragment, n);
    },
    m(n, i) {
      vt(t, n, i), r = !0;
    },
    p(n, i) {
      const l = i & /*itemProps, $mergedProps, $slotKey*/
      7 ? xt(s, [i & /*itemProps*/
      2 && yt(
        /*itemProps*/
        n[1].props
      ), i & /*itemProps*/
      2 && {
        slots: (
          /*itemProps*/
          n[1].slots
        )
      }, i & /*$mergedProps*/
      1 && {
        itemIndex: (
          /*$mergedProps*/
          n[0]._internal.index || 0
        )
      }, i & /*$slotKey*/
      4 && {
        itemSlotKey: (
          /*$slotKey*/
          n[2]
        )
      }]) : {};
      i & /*$$scope, $mergedProps*/
      524289 && (l.$$scope = {
        dirty: i,
        ctx: n
      }), t.$set(l);
    },
    i(n) {
      r || (F(t.$$.fragment, n), r = !0);
    },
    o(n) {
      j(t.$$.fragment, n), r = !1;
    },
    d(n) {
      pt(t, n);
    }
  };
}
function Q(e) {
  let t;
  const r = (
    /*#slots*/
    e[18].default
  ), s = _t(
    r,
    e,
    /*$$scope*/
    e[19],
    null
  );
  return {
    c() {
      s && s.c();
    },
    l(o) {
      s && s.l(o);
    },
    m(o, n) {
      s && s.m(o, n), t = !0;
    },
    p(o, n) {
      s && s.p && (!t || n & /*$$scope*/
      524288) && kt(
        s,
        r,
        o,
        /*$$scope*/
        o[19],
        t ? ht(
          r,
          /*$$scope*/
          o[19],
          n,
          null
        ) : bt(
          /*$$scope*/
          o[19]
        ),
        null
      );
    },
    i(o) {
      t || (F(s, o), t = !0);
    },
    o(o) {
      j(s, o), t = !1;
    },
    d(o) {
      s && s.d(o);
    }
  };
}
function Ot(e) {
  let t, r, s = (
    /*$mergedProps*/
    e[0].visible && Q(e)
  );
  return {
    c() {
      s && s.c(), t = N();
    },
    l(o) {
      s && s.l(o), t = N();
    },
    m(o, n) {
      s && s.m(o, n), ce(o, t, n), r = !0;
    },
    p(o, n) {
      /*$mergedProps*/
      o[0].visible ? s ? (s.p(o, n), n & /*$mergedProps*/
      1 && F(s, 1)) : (s = Q(o), s.c(), F(s, 1), s.m(t.parentNode, t)) : s && (Pt(), j(s, 1, 1, () => {
        s = null;
      }), ft());
    },
    i(o) {
      r || (F(s), r = !0);
    },
    o(o) {
      j(s), r = !1;
    },
    d(o) {
      o && le(t), s && s.d(o);
    }
  };
}
function Ft(e) {
  return {
    c: b,
    l: b,
    m: b,
    p: b,
    i: b,
    o: b,
    d: b
  };
}
function Tt(e) {
  let t, r, s = {
    ctx: e,
    current: null,
    token: null,
    hasCatch: !1,
    pending: Ft,
    then: It,
    catch: wt,
    value: 23,
    blocks: [, , ,]
  };
  return Ct(
    /*AwaitedBubbleListItem*/
    e[3],
    s
  ), {
    c() {
      t = N(), s.block.c();
    },
    l(o) {
      t = N(), s.block.l(o);
    },
    m(o, n) {
      ce(o, t, n), s.block.m(o, s.anchor = n), s.mount = () => t.parentNode, s.anchor = t, r = !0;
    },
    p(o, [n]) {
      e = o, Rt(s, e, n);
    },
    i(o) {
      r || (F(s.block), r = !0);
    },
    o(o) {
      for (let n = 0; n < 3; n += 1) {
        const i = s.blocks[n];
        j(i);
      }
      r = !1;
    },
    d(o) {
      o && le(t), s.block.d(o), s.token = null, s = null;
    }
  };
}
function Mt(e, t, r) {
  const s = ["gradio", "props", "_internal", "as_item", "visible", "elem_id", "elem_classes", "elem_style"];
  let o = Y(t, s), n, i, l, p, {
    $$slots: m = {},
    $$scope: y
  } = t;
  const u = me(() => import("./bubble.list.item-DKz9u47G.js"));
  let {
    gradio: f
  } = t, {
    props: a = {}
  } = t;
  const C = R(a);
  K(e, C, (c) => r(17, l = c));
  let {
    _internal: E = {}
  } = t, {
    as_item: _
  } = t, {
    visible: g = !0
  } = t, {
    elem_id: h = ""
  } = t, {
    elem_classes: k = []
  } = t, {
    elem_style: v = {}
  } = t;
  const S = ne();
  K(e, S, (c) => r(2, p = c));
  const [d, x] = He({
    gradio: f,
    props: l,
    _internal: E,
    visible: g,
    elem_id: h,
    elem_classes: k,
    elem_style: v,
    as_item: _,
    restProps: o
  });
  K(e, d, (c) => r(0, i = c));
  const P = De(), M = We();
  K(e, M, (c) => r(16, n = c));
  let H = {
    props: {},
    slots: {}
  };
  return e.$$set = (c) => {
    t = U(U({}, t), gt(c)), r(22, o = Y(t, s)), "gradio" in c && r(8, f = c.gradio), "props" in c && r(9, a = c.props), "_internal" in c && r(10, E = c._internal), "as_item" in c && r(11, _ = c.as_item), "visible" in c && r(12, g = c.visible), "elem_id" in c && r(13, h = c.elem_id), "elem_classes" in c && r(14, k = c.elem_classes), "elem_style" in c && r(15, v = c.elem_style), "$$scope" in c && r(19, y = c.$$scope);
  }, e.$$.update = () => {
    if (e.$$.dirty & /*props*/
    512 && C.update((c) => ({
      ...c,
      ...a
    })), x({
      gradio: f,
      props: l,
      _internal: E,
      visible: g,
      elem_id: h,
      elem_classes: k,
      elem_style: v,
      as_item: _,
      restProps: o
    }), e.$$.dirty & /*$mergedProps, $slots*/
    65537) {
      let c = i.props.avatar || i.restProps.avatar;
      n.avatar ? c = z(n.avatar) : (n["avatar.icon"] || n["avatar.src"]) && (c = {
        ...c || {},
        icon: n["avatar.icon"] ? z(n["avatar.icon"]) : c == null ? void 0 : c.icon,
        src: n["avatar.src"] ? z(n["avatar.src"]) : c == null ? void 0 : c.src
      }), r(1, H = {
        props: {
          style: i.elem_style,
          className: at(i.elem_classes, "ms-gr-antdx-bubble-list-role"),
          id: i.elem_id,
          ...i.restProps,
          ...i.props,
          ..._e(i, {
            typing_complete: "typingComplete"
          }),
          avatar: c,
          loadingRender: X(i.props.loadingRender || i.restProps.loadingRender),
          messageRender: X(i.props.messageRender || i.restProps.messageRender)
        },
        slots: {
          ...n,
          avatar: void 0,
          "avatar.icon": void 0,
          "avatar.src": void 0,
          header: {
            el: n.header,
            callback: P
          },
          footer: {
            el: n.footer,
            callback: P
          },
          loadingRender: {
            el: n.loadingRender,
            callback: P
          },
          messageRender: {
            el: n.messageRender,
            callback: P
          }
        }
      });
    }
  }, [i, H, p, u, C, S, d, M, f, a, E, _, g, h, k, v, n, l, m, y];
}
class jt extends ut {
  constructor(t) {
    super(), Et(this, t, Mt, Tt, St, {
      gradio: 8,
      props: 9,
      _internal: 10,
      as_item: 11,
      visible: 12,
      elem_id: 13,
      elem_classes: 14,
      elem_style: 15
    });
  }
  get gradio() {
    return this.$$.ctx[8];
  }
  set gradio(t) {
    this.$$set({
      gradio: t
    }), w();
  }
  get props() {
    return this.$$.ctx[9];
  }
  set props(t) {
    this.$$set({
      props: t
    }), w();
  }
  get _internal() {
    return this.$$.ctx[10];
  }
  set _internal(t) {
    this.$$set({
      _internal: t
    }), w();
  }
  get as_item() {
    return this.$$.ctx[11];
  }
  set as_item(t) {
    this.$$set({
      as_item: t
    }), w();
  }
  get visible() {
    return this.$$.ctx[12];
  }
  set visible(t) {
    this.$$set({
      visible: t
    }), w();
  }
  get elem_id() {
    return this.$$.ctx[13];
  }
  set elem_id(t) {
    this.$$set({
      elem_id: t
    }), w();
  }
  get elem_classes() {
    return this.$$.ctx[14];
  }
  set elem_classes(t) {
    this.$$set({
      elem_classes: t
    }), w();
  }
  get elem_style() {
    return this.$$.ctx[15];
  }
  set elem_style(t) {
    this.$$set({
      elem_style: t
    }), w();
  }
}
const At = /* @__PURE__ */ Object.freeze(/* @__PURE__ */ Object.defineProperty({
  __proto__: null,
  default: jt
}, Symbol.toStringTag, {
  value: "Module"
}));
export {
  At as I,
  Nt as g,
  nt as j,
  R as w
};
