import { i as _n, a as Me, r as Sn, w as le, g as wn, c as fe } from "./Index-CoMKotgF.js";
const v = window.ms_globals.React, $ = window.ms_globals.React, yn = window.ms_globals.React.forwardRef, K = window.ms_globals.React.useRef, En = window.ms_globals.React.useState, ee = window.ms_globals.React.useEffect, bn = window.ms_globals.React.isValidElement, gn = window.ms_globals.React.version, hn = window.ms_globals.React.useLayoutEffect, st = window.ms_globals.ReactDOM, Ne = window.ms_globals.ReactDOM.createPortal, Cn = window.ms_globals.internalContext.useContextPropsContext, Rn = window.ms_globals.antdIcons.CloseOutlined, An = window.ms_globals.antd.Button, Tn = window.ms_globals.antd.ConfigProvider;
var Pn = /\s/;
function xn(e) {
  for (var t = e.length; t-- && Pn.test(e.charAt(t)); )
    ;
  return t;
}
var On = /^\s+/;
function Ln(e) {
  return e && e.slice(0, xn(e) + 1).replace(On, "");
}
var ut = NaN, kn = /^[-+]0x[0-9a-f]+$/i, In = /^0b[01]+$/i, jn = /^0o[0-7]+$/i, Nn = parseInt;
function ct(e) {
  if (typeof e == "number")
    return e;
  if (_n(e))
    return ut;
  if (Me(e)) {
    var t = typeof e.valueOf == "function" ? e.valueOf() : e;
    e = Me(t) ? t + "" : t;
  }
  if (typeof e != "string")
    return e === 0 ? e : +e;
  e = Ln(e);
  var n = In.test(e);
  return n || jn.test(e) ? Nn(e.slice(2), n ? 2 : 8) : kn.test(e) ? ut : +e;
}
var Oe = function() {
  return Sn.Date.now();
}, Mn = "Expected a function", $n = Math.max, Dn = Math.min;
function Fn(e, t, n) {
  var r, o, i, a, s, l, u = 0, d = !1, c = !1, m = !0;
  if (typeof e != "function")
    throw new TypeError(Mn);
  t = ct(t) || 0, Me(n) && (d = !!n.leading, c = "maxWait" in n, i = c ? $n(ct(n.maxWait) || 0, t) : i, m = "trailing" in n ? !!n.trailing : m);
  function f(p) {
    var C = r, L = o;
    return r = o = void 0, u = p, a = e.apply(L, C), a;
  }
  function g(p) {
    return u = p, s = setTimeout(_, t), d ? f(p) : a;
  }
  function S(p) {
    var C = p - l, L = p - u, Q = t - C;
    return c ? Dn(Q, i - L) : Q;
  }
  function y(p) {
    var C = p - l, L = p - u;
    return l === void 0 || C >= t || C < 0 || c && L >= i;
  }
  function _() {
    var p = Oe();
    if (y(p))
      return w(p);
    s = setTimeout(_, S(p));
  }
  function w(p) {
    return s = void 0, m && r ? f(p) : (r = o = void 0, a);
  }
  function A() {
    s !== void 0 && clearTimeout(s), u = 0, r = l = o = s = void 0;
  }
  function E() {
    return s === void 0 ? a : w(Oe());
  }
  function T() {
    var p = Oe(), C = y(p);
    if (r = arguments, o = this, l = p, C) {
      if (s === void 0)
        return g(l);
      if (c)
        return clearTimeout(s), s = setTimeout(_, t), f(l);
    }
    return s === void 0 && (s = setTimeout(_, t)), a;
  }
  return T.cancel = A, T.flush = E, T;
}
var kt = {
  exports: {}
}, ve = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var Un = $, Vn = Symbol.for("react.element"), Kn = Symbol.for("react.fragment"), Wn = Object.prototype.hasOwnProperty, Hn = Un.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, zn = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function It(e, t, n) {
  var r, o = {}, i = null, a = null;
  n !== void 0 && (i = "" + n), t.key !== void 0 && (i = "" + t.key), t.ref !== void 0 && (a = t.ref);
  for (r in t) Wn.call(t, r) && !zn.hasOwnProperty(r) && (o[r] = t[r]);
  if (e && e.defaultProps) for (r in t = e.defaultProps, t) o[r] === void 0 && (o[r] = t[r]);
  return {
    $$typeof: Vn,
    type: e,
    key: i,
    ref: a,
    props: o,
    _owner: Hn.current
  };
}
ve.Fragment = Kn;
ve.jsx = It;
ve.jsxs = It;
kt.exports = ve;
var Le = kt.exports;
const {
  SvelteComponent: Bn,
  assign: lt,
  binding_callbacks: ft,
  check_outros: Qn,
  children: jt,
  claim_element: Nt,
  claim_space: Gn,
  component_subscribe: dt,
  compute_slots: qn,
  create_slot: Yn,
  detach: Y,
  element: Mt,
  empty: mt,
  exclude_internal_props: pt,
  get_all_dirty_from_scope: Jn,
  get_slot_changes: Xn,
  group_outros: Zn,
  init: er,
  insert_hydration: de,
  safe_not_equal: tr,
  set_custom_element_data: $t,
  space: nr,
  transition_in: me,
  transition_out: $e,
  update_slot_base: rr
} = window.__gradio__svelte__internal, {
  beforeUpdate: or,
  getContext: ir,
  onDestroy: ar,
  setContext: sr
} = window.__gradio__svelte__internal;
function vt(e) {
  let t, n;
  const r = (
    /*#slots*/
    e[7].default
  ), o = Yn(
    r,
    e,
    /*$$scope*/
    e[6],
    null
  );
  return {
    c() {
      t = Mt("svelte-slot"), o && o.c(), this.h();
    },
    l(i) {
      t = Nt(i, "SVELTE-SLOT", {
        class: !0
      });
      var a = jt(t);
      o && o.l(a), a.forEach(Y), this.h();
    },
    h() {
      $t(t, "class", "svelte-1rt0kpf");
    },
    m(i, a) {
      de(i, t, a), o && o.m(t, null), e[9](t), n = !0;
    },
    p(i, a) {
      o && o.p && (!n || a & /*$$scope*/
      64) && rr(
        o,
        r,
        i,
        /*$$scope*/
        i[6],
        n ? Xn(
          r,
          /*$$scope*/
          i[6],
          a,
          null
        ) : Jn(
          /*$$scope*/
          i[6]
        ),
        null
      );
    },
    i(i) {
      n || (me(o, i), n = !0);
    },
    o(i) {
      $e(o, i), n = !1;
    },
    d(i) {
      i && Y(t), o && o.d(i), e[9](null);
    }
  };
}
function ur(e) {
  let t, n, r, o, i = (
    /*$$slots*/
    e[4].default && vt(e)
  );
  return {
    c() {
      t = Mt("react-portal-target"), n = nr(), i && i.c(), r = mt(), this.h();
    },
    l(a) {
      t = Nt(a, "REACT-PORTAL-TARGET", {
        class: !0
      }), jt(t).forEach(Y), n = Gn(a), i && i.l(a), r = mt(), this.h();
    },
    h() {
      $t(t, "class", "svelte-1rt0kpf");
    },
    m(a, s) {
      de(a, t, s), e[8](t), de(a, n, s), i && i.m(a, s), de(a, r, s), o = !0;
    },
    p(a, [s]) {
      /*$$slots*/
      a[4].default ? i ? (i.p(a, s), s & /*$$slots*/
      16 && me(i, 1)) : (i = vt(a), i.c(), me(i, 1), i.m(r.parentNode, r)) : i && (Zn(), $e(i, 1, 1, () => {
        i = null;
      }), Qn());
    },
    i(a) {
      o || (me(i), o = !0);
    },
    o(a) {
      $e(i), o = !1;
    },
    d(a) {
      a && (Y(t), Y(n), Y(r)), e[8](null), i && i.d(a);
    }
  };
}
function yt(e) {
  const {
    svelteInit: t,
    ...n
  } = e;
  return n;
}
function cr(e, t, n) {
  let r, o, {
    $$slots: i = {},
    $$scope: a
  } = t;
  const s = qn(i);
  let {
    svelteInit: l
  } = t;
  const u = le(yt(t)), d = le();
  dt(e, d, (E) => n(0, r = E));
  const c = le();
  dt(e, c, (E) => n(1, o = E));
  const m = [], f = ir("$$ms-gr-react-wrapper"), {
    slotKey: g,
    slotIndex: S,
    subSlotIndex: y
  } = wn() || {}, _ = l({
    parent: f,
    props: u,
    target: d,
    slot: c,
    slotKey: g,
    slotIndex: S,
    subSlotIndex: y,
    onDestroy(E) {
      m.push(E);
    }
  });
  sr("$$ms-gr-react-wrapper", _), or(() => {
    u.set(yt(t));
  }), ar(() => {
    m.forEach((E) => E());
  });
  function w(E) {
    ft[E ? "unshift" : "push"](() => {
      r = E, d.set(r);
    });
  }
  function A(E) {
    ft[E ? "unshift" : "push"](() => {
      o = E, c.set(o);
    });
  }
  return e.$$set = (E) => {
    n(17, t = lt(lt({}, t), pt(E))), "svelteInit" in E && n(5, l = E.svelteInit), "$$scope" in E && n(6, a = E.$$scope);
  }, t = pt(t), [r, o, d, c, s, l, a, i, w, A];
}
class lr extends Bn {
  constructor(t) {
    super(), er(this, t, cr, ur, tr, {
      svelteInit: 5
    });
  }
}
const {
  SvelteComponent: uo
} = window.__gradio__svelte__internal, Et = window.ms_globals.rerender, ke = window.ms_globals.tree;
function fr(e, t = {}) {
  function n(r) {
    const o = le(), i = new lr({
      ...r,
      props: {
        svelteInit(a) {
          window.ms_globals.autokey += 1;
          const s = {
            key: window.ms_globals.autokey,
            svelteInstance: o,
            reactComponent: e,
            props: a.props,
            slot: a.slot,
            target: a.target,
            slotIndex: a.slotIndex,
            subSlotIndex: a.subSlotIndex,
            ignore: t.ignore,
            slotKey: a.slotKey,
            nodes: []
          }, l = a.parent ?? ke;
          return l.nodes = [...l.nodes, s], Et({
            createPortal: Ne,
            node: ke
          }), a.onDestroy(() => {
            l.nodes = l.nodes.filter((u) => u.svelteInstance !== o), Et({
              createPortal: Ne,
              node: ke
            });
          }), s;
        },
        ...r.props
      }
    });
    return o.set(i), i;
  }
  return new Promise((r) => {
    window.ms_globals.initializePromise.then(() => {
      r(n);
    });
  });
}
const dr = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function mr(e) {
  return e ? Object.keys(e).reduce((t, n) => {
    const r = e[n];
    return t[n] = pr(n, r), t;
  }, {}) : {};
}
function pr(e, t) {
  return typeof t == "number" && !dr.includes(e) ? t + "px" : t;
}
function De(e) {
  const t = [], n = e.cloneNode(!1);
  if (e._reactElement) {
    const o = $.Children.toArray(e._reactElement.props.children).map((i) => {
      if ($.isValidElement(i) && i.props.__slot__) {
        const {
          portals: a,
          clonedElement: s
        } = De(i.props.el);
        return $.cloneElement(i, {
          ...i.props,
          el: s,
          children: [...$.Children.toArray(i.props.children), ...a]
        });
      }
      return null;
    });
    return o.originalChildren = e._reactElement.props.children, t.push(Ne($.cloneElement(e._reactElement, {
      ...e._reactElement.props,
      children: o
    }), n)), {
      clonedElement: n,
      portals: t
    };
  }
  Object.keys(e.getEventListeners()).forEach((o) => {
    e.getEventListeners(o).forEach(({
      listener: a,
      type: s,
      useCapture: l
    }) => {
      n.addEventListener(s, a, l);
    });
  });
  const r = Array.from(e.childNodes);
  for (let o = 0; o < r.length; o++) {
    const i = r[o];
    if (i.nodeType === 1) {
      const {
        clonedElement: a,
        portals: s
      } = De(i);
      t.push(...s), n.appendChild(a);
    } else i.nodeType === 3 && n.appendChild(i.cloneNode());
  }
  return {
    clonedElement: n,
    portals: t
  };
}
function vr(e, t) {
  e && (typeof e == "function" ? e(t) : e.current = t);
}
const yr = yn(({
  slot: e,
  clone: t,
  className: n,
  style: r,
  observeAttributes: o
}, i) => {
  const a = K(), [s, l] = En([]), {
    forceClone: u
  } = Cn(), d = u ? !0 : t;
  return ee(() => {
    var S;
    if (!a.current || !e)
      return;
    let c = e;
    function m() {
      let y = c;
      if (c.tagName.toLowerCase() === "svelte-slot" && c.children.length === 1 && c.children[0] && (y = c.children[0], y.tagName.toLowerCase() === "react-portal-target" && y.children[0] && (y = y.children[0])), vr(i, y), n && y.classList.add(...n.split(" ")), r) {
        const _ = mr(r);
        Object.keys(_).forEach((w) => {
          y.style[w] = _[w];
        });
      }
    }
    let f = null, g = null;
    if (d && window.MutationObserver) {
      let y = function() {
        var E, T, p;
        (E = a.current) != null && E.contains(c) && ((T = a.current) == null || T.removeChild(c));
        const {
          portals: w,
          clonedElement: A
        } = De(e);
        c = A, l(w), c.style.display = "contents", g && clearTimeout(g), g = setTimeout(() => {
          m();
        }, 50), (p = a.current) == null || p.appendChild(c);
      };
      y();
      const _ = Fn(() => {
        y(), f == null || f.disconnect(), f == null || f.observe(e, {
          childList: !0,
          subtree: !0,
          attributes: o
        });
      }, 50);
      f = new window.MutationObserver(_), f.observe(e, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      c.style.display = "contents", m(), (S = a.current) == null || S.appendChild(c);
    return () => {
      var y, _;
      c.style.display = "", (y = a.current) != null && y.contains(c) && ((_ = a.current) == null || _.removeChild(c)), f == null || f.disconnect();
    };
  }, [e, d, n, r, i, o, u]), $.createElement("react-child", {
    ref: a,
    style: {
      display: "contents"
    }
  }, ...s);
});
function D(e) {
  "@babel/helpers - typeof";
  return D = typeof Symbol == "function" && typeof Symbol.iterator == "symbol" ? function(t) {
    return typeof t;
  } : function(t) {
    return t && typeof Symbol == "function" && t.constructor === Symbol && t !== Symbol.prototype ? "symbol" : typeof t;
  }, D(e);
}
function Er(e, t) {
  if (D(e) != "object" || !e) return e;
  var n = e[Symbol.toPrimitive];
  if (n !== void 0) {
    var r = n.call(e, t);
    if (D(r) != "object") return r;
    throw new TypeError("@@toPrimitive must return a primitive value.");
  }
  return (t === "string" ? String : Number)(e);
}
function Dt(e) {
  var t = Er(e, "string");
  return D(t) == "symbol" ? t : t + "";
}
function P(e, t, n) {
  return (t = Dt(t)) in e ? Object.defineProperty(e, t, {
    value: n,
    enumerable: !0,
    configurable: !0,
    writable: !0
  }) : e[t] = n, e;
}
function bt(e, t) {
  var n = Object.keys(e);
  if (Object.getOwnPropertySymbols) {
    var r = Object.getOwnPropertySymbols(e);
    t && (r = r.filter(function(o) {
      return Object.getOwnPropertyDescriptor(e, o).enumerable;
    })), n.push.apply(n, r);
  }
  return n;
}
function h(e) {
  for (var t = 1; t < arguments.length; t++) {
    var n = arguments[t] != null ? arguments[t] : {};
    t % 2 ? bt(Object(n), !0).forEach(function(r) {
      P(e, r, n[r]);
    }) : Object.getOwnPropertyDescriptors ? Object.defineProperties(e, Object.getOwnPropertyDescriptors(n)) : bt(Object(n)).forEach(function(r) {
      Object.defineProperty(e, r, Object.getOwnPropertyDescriptor(n, r));
    });
  }
  return e;
}
function br(e) {
  if (Array.isArray(e)) return e;
}
function gr(e, t) {
  var n = e == null ? null : typeof Symbol < "u" && e[Symbol.iterator] || e["@@iterator"];
  if (n != null) {
    var r, o, i, a, s = [], l = !0, u = !1;
    try {
      if (i = (n = n.call(e)).next, t === 0) {
        if (Object(n) !== n) return;
        l = !1;
      } else for (; !(l = (r = i.call(n)).done) && (s.push(r.value), s.length !== t); l = !0) ;
    } catch (d) {
      u = !0, o = d;
    } finally {
      try {
        if (!l && n.return != null && (a = n.return(), Object(a) !== a)) return;
      } finally {
        if (u) throw o;
      }
    }
    return s;
  }
}
function gt(e, t) {
  (t == null || t > e.length) && (t = e.length);
  for (var n = 0, r = Array(t); n < t; n++) r[n] = e[n];
  return r;
}
function hr(e, t) {
  if (e) {
    if (typeof e == "string") return gt(e, t);
    var n = {}.toString.call(e).slice(8, -1);
    return n === "Object" && e.constructor && (n = e.constructor.name), n === "Map" || n === "Set" ? Array.from(e) : n === "Arguments" || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n) ? gt(e, t) : void 0;
  }
}
function _r() {
  throw new TypeError(`Invalid attempt to destructure non-iterable instance.
In order to be iterable, non-array objects must have a [Symbol.iterator]() method.`);
}
function V(e, t) {
  return br(e) || gr(e, t) || hr(e, t) || _r();
}
function te(e) {
  "@babel/helpers - typeof";
  return te = typeof Symbol == "function" && typeof Symbol.iterator == "symbol" ? function(t) {
    return typeof t;
  } : function(t) {
    return t && typeof Symbol == "function" && t.constructor === Symbol && t !== Symbol.prototype ? "symbol" : typeof t;
  }, te(e);
}
function ht(e) {
  return e instanceof HTMLElement || e instanceof SVGElement;
}
function Sr(e) {
  return e && te(e) === "object" && ht(e.nativeElement) ? e.nativeElement : ht(e) ? e : null;
}
function wr(e) {
  var t = Sr(e);
  if (t)
    return t;
  if (e instanceof $.Component) {
    var n;
    return (n = st.findDOMNode) === null || n === void 0 ? void 0 : n.call(st, e);
  }
  return null;
}
var Ft = {
  exports: {}
}, b = {};
/**
 * @license React
 * react-is.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var qe = Symbol.for("react.element"), Ye = Symbol.for("react.portal"), ye = Symbol.for("react.fragment"), Ee = Symbol.for("react.strict_mode"), be = Symbol.for("react.profiler"), ge = Symbol.for("react.provider"), he = Symbol.for("react.context"), Cr = Symbol.for("react.server_context"), _e = Symbol.for("react.forward_ref"), Se = Symbol.for("react.suspense"), we = Symbol.for("react.suspense_list"), Ce = Symbol.for("react.memo"), Re = Symbol.for("react.lazy"), Rr = Symbol.for("react.offscreen"), Ut;
Ut = Symbol.for("react.module.reference");
function k(e) {
  if (typeof e == "object" && e !== null) {
    var t = e.$$typeof;
    switch (t) {
      case qe:
        switch (e = e.type, e) {
          case ye:
          case be:
          case Ee:
          case Se:
          case we:
            return e;
          default:
            switch (e = e && e.$$typeof, e) {
              case Cr:
              case he:
              case _e:
              case Re:
              case Ce:
              case ge:
                return e;
              default:
                return t;
            }
        }
      case Ye:
        return t;
    }
  }
}
b.ContextConsumer = he;
b.ContextProvider = ge;
b.Element = qe;
b.ForwardRef = _e;
b.Fragment = ye;
b.Lazy = Re;
b.Memo = Ce;
b.Portal = Ye;
b.Profiler = be;
b.StrictMode = Ee;
b.Suspense = Se;
b.SuspenseList = we;
b.isAsyncMode = function() {
  return !1;
};
b.isConcurrentMode = function() {
  return !1;
};
b.isContextConsumer = function(e) {
  return k(e) === he;
};
b.isContextProvider = function(e) {
  return k(e) === ge;
};
b.isElement = function(e) {
  return typeof e == "object" && e !== null && e.$$typeof === qe;
};
b.isForwardRef = function(e) {
  return k(e) === _e;
};
b.isFragment = function(e) {
  return k(e) === ye;
};
b.isLazy = function(e) {
  return k(e) === Re;
};
b.isMemo = function(e) {
  return k(e) === Ce;
};
b.isPortal = function(e) {
  return k(e) === Ye;
};
b.isProfiler = function(e) {
  return k(e) === be;
};
b.isStrictMode = function(e) {
  return k(e) === Ee;
};
b.isSuspense = function(e) {
  return k(e) === Se;
};
b.isSuspenseList = function(e) {
  return k(e) === we;
};
b.isValidElementType = function(e) {
  return typeof e == "string" || typeof e == "function" || e === ye || e === be || e === Ee || e === Se || e === we || e === Rr || typeof e == "object" && e !== null && (e.$$typeof === Re || e.$$typeof === Ce || e.$$typeof === ge || e.$$typeof === he || e.$$typeof === _e || e.$$typeof === Ut || e.getModuleId !== void 0);
};
b.typeOf = k;
Ft.exports = b;
var Ie = Ft.exports, Ar = Symbol.for("react.element"), Tr = Symbol.for("react.transitional.element"), Pr = Symbol.for("react.fragment");
function xr(e) {
  return (
    // Base object type
    e && te(e) === "object" && // React Element type
    (e.$$typeof === Ar || e.$$typeof === Tr) && // React Fragment type
    e.type === Pr
  );
}
var Or = Number(gn.split(".")[0]), Lr = function(t, n) {
  typeof t == "function" ? t(n) : te(t) === "object" && t && "current" in t && (t.current = n);
}, kr = function(t) {
  var n, r;
  if (!t)
    return !1;
  if (Vt(t) && Or >= 19)
    return !0;
  var o = Ie.isMemo(t) ? t.type.type : t.type;
  return !(typeof o == "function" && !((n = o.prototype) !== null && n !== void 0 && n.render) && o.$$typeof !== Ie.ForwardRef || typeof t == "function" && !((r = t.prototype) !== null && r !== void 0 && r.render) && t.$$typeof !== Ie.ForwardRef);
};
function Vt(e) {
  return /* @__PURE__ */ bn(e) && !xr(e);
}
var Ir = function(t) {
  if (t && Vt(t)) {
    var n = t;
    return n.props.propertyIsEnumerable("ref") ? n.props.ref : n.ref;
  }
  return null;
};
function jr(e, t) {
  if (e == null) return {};
  var n = {};
  for (var r in e) if ({}.hasOwnProperty.call(e, r)) {
    if (t.indexOf(r) !== -1) continue;
    n[r] = e[r];
  }
  return n;
}
function _t(e, t) {
  if (e == null) return {};
  var n, r, o = jr(e, t);
  if (Object.getOwnPropertySymbols) {
    var i = Object.getOwnPropertySymbols(e);
    for (r = 0; r < i.length; r++) n = i[r], t.indexOf(n) === -1 && {}.propertyIsEnumerable.call(e, n) && (o[n] = e[n]);
  }
  return o;
}
var Nr = /* @__PURE__ */ v.createContext({});
function Kt(e, t) {
  if (!(e instanceof t)) throw new TypeError("Cannot call a class as a function");
}
function St(e, t) {
  for (var n = 0; n < t.length; n++) {
    var r = t[n];
    r.enumerable = r.enumerable || !1, r.configurable = !0, "value" in r && (r.writable = !0), Object.defineProperty(e, Dt(r.key), r);
  }
}
function Wt(e, t, n) {
  return t && St(e.prototype, t), n && St(e, n), Object.defineProperty(e, "prototype", {
    writable: !1
  }), e;
}
function Fe(e, t) {
  return Fe = Object.setPrototypeOf ? Object.setPrototypeOf.bind() : function(n, r) {
    return n.__proto__ = r, n;
  }, Fe(e, t);
}
function Ht(e, t) {
  if (typeof t != "function" && t !== null) throw new TypeError("Super expression must either be null or a function");
  e.prototype = Object.create(t && t.prototype, {
    constructor: {
      value: e,
      writable: !0,
      configurable: !0
    }
  }), Object.defineProperty(e, "prototype", {
    writable: !1
  }), t && Fe(e, t);
}
function pe(e) {
  return pe = Object.setPrototypeOf ? Object.getPrototypeOf.bind() : function(t) {
    return t.__proto__ || Object.getPrototypeOf(t);
  }, pe(e);
}
function zt() {
  try {
    var e = !Boolean.prototype.valueOf.call(Reflect.construct(Boolean, [], function() {
    }));
  } catch {
  }
  return (zt = function() {
    return !!e;
  })();
}
function Ue(e) {
  if (e === void 0) throw new ReferenceError("this hasn't been initialised - super() hasn't been called");
  return e;
}
function Mr(e, t) {
  if (t && (D(t) == "object" || typeof t == "function")) return t;
  if (t !== void 0) throw new TypeError("Derived constructors may only return object or undefined");
  return Ue(e);
}
function Bt(e) {
  var t = zt();
  return function() {
    var n, r = pe(e);
    if (t) {
      var o = pe(this).constructor;
      n = Reflect.construct(r, arguments, o);
    } else n = r.apply(this, arguments);
    return Mr(this, n);
  };
}
var $r = /* @__PURE__ */ function(e) {
  Ht(n, e);
  var t = Bt(n);
  function n() {
    return Kt(this, n), t.apply(this, arguments);
  }
  return Wt(n, [{
    key: "render",
    value: function() {
      return this.props.children;
    }
  }]), n;
}(v.Component);
function Ve(e) {
  var t = v.useRef();
  t.current = e;
  var n = v.useCallback(function() {
    for (var r, o = arguments.length, i = new Array(o), a = 0; a < o; a++)
      i[a] = arguments[a];
    return (r = t.current) === null || r === void 0 ? void 0 : r.call.apply(r, [t].concat(i));
  }, []);
  return n;
}
function Dr(e) {
  if (Array.isArray(e)) return e;
}
function Fr(e, t) {
  var n = e == null ? null : typeof Symbol < "u" && e[Symbol.iterator] || e["@@iterator"];
  if (n != null) {
    var r, o, i, a, s = [], l = !0, u = !1;
    try {
      if (i = (n = n.call(e)).next, t !== 0) for (; !(l = (r = i.call(n)).done) && (s.push(r.value), s.length !== t); l = !0) ;
    } catch (d) {
      u = !0, o = d;
    } finally {
      try {
        if (!l && n.return != null && (a = n.return(), Object(a) !== a)) return;
      } finally {
        if (u) throw o;
      }
    }
    return s;
  }
}
function wt(e, t) {
  (t == null || t > e.length) && (t = e.length);
  for (var n = 0, r = Array(t); n < t; n++) r[n] = e[n];
  return r;
}
function Ur(e, t) {
  if (e) {
    if (typeof e == "string") return wt(e, t);
    var n = {}.toString.call(e).slice(8, -1);
    return n === "Object" && e.constructor && (n = e.constructor.name), n === "Map" || n === "Set" ? Array.from(e) : n === "Arguments" || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n) ? wt(e, t) : void 0;
  }
}
function Vr() {
  throw new TypeError(`Invalid attempt to destructure non-iterable instance.
In order to be iterable, non-array objects must have a [Symbol.iterator]() method.`);
}
function Qt(e, t) {
  return Dr(e) || Fr(e, t) || Ur(e, t) || Vr();
}
function Je() {
  return !!(typeof window < "u" && window.document && window.document.createElement);
}
function Ke(e) {
  var t = v.useRef(!1), n = v.useState(e), r = Qt(n, 2), o = r[0], i = r[1];
  v.useEffect(function() {
    return t.current = !1, function() {
      t.current = !0;
    };
  }, []);
  function a(s, l) {
    l && t.current || i(s);
  }
  return [o, a];
}
function Kr(e) {
  var t = v.useReducer(function(s) {
    return s + 1;
  }, 0), n = Qt(t, 2), r = n[1], o = v.useRef(e), i = Ve(function() {
    return o.current;
  }), a = Ve(function(s) {
    o.current = typeof s == "function" ? s(o.current) : s, r();
  });
  return [i, a];
}
var U = "none", ae = "appear", se = "enter", ue = "leave", Ct = "none", j = "prepare", J = "start", X = "active", Xe = "end", Gt = "prepared";
function Rt(e, t) {
  var n = {};
  return n[e.toLowerCase()] = t.toLowerCase(), n["Webkit".concat(e)] = "webkit".concat(t), n["Moz".concat(e)] = "moz".concat(t), n["ms".concat(e)] = "MS".concat(t), n["O".concat(e)] = "o".concat(t.toLowerCase()), n;
}
function Wr(e, t) {
  var n = {
    animationend: Rt("Animation", "AnimationEnd"),
    transitionend: Rt("Transition", "TransitionEnd")
  };
  return e && ("AnimationEvent" in t || delete n.animationend.animation, "TransitionEvent" in t || delete n.transitionend.transition), n;
}
var Hr = Wr(Je(), typeof window < "u" ? window : {}), qt = {};
if (Je()) {
  var zr = document.createElement("div");
  qt = zr.style;
}
var ce = {};
function Yt(e) {
  if (ce[e])
    return ce[e];
  var t = Hr[e];
  if (t)
    for (var n = Object.keys(t), r = n.length, o = 0; o < r; o += 1) {
      var i = n[o];
      if (Object.prototype.hasOwnProperty.call(t, i) && i in qt)
        return ce[e] = t[i], ce[e];
    }
  return "";
}
var Jt = Yt("animationend"), Xt = Yt("transitionend"), Zt = !!(Jt && Xt), At = Jt || "animationend", Tt = Xt || "transitionend";
function Pt(e, t) {
  if (!e) return null;
  if (D(e) === "object") {
    var n = t.replace(/-\w/g, function(r) {
      return r[1].toUpperCase();
    });
    return e[n];
  }
  return "".concat(e, "-").concat(t);
}
const Br = function(e) {
  var t = K();
  function n(o) {
    o && (o.removeEventListener(Tt, e), o.removeEventListener(At, e));
  }
  function r(o) {
    t.current && t.current !== o && n(t.current), o && o !== t.current && (o.addEventListener(Tt, e), o.addEventListener(At, e), t.current = o);
  }
  return v.useEffect(function() {
    return function() {
      n(t.current);
    };
  }, []), [r, n];
};
var en = Je() ? hn : ee, tn = function(t) {
  return +setTimeout(t, 16);
}, nn = function(t) {
  return clearTimeout(t);
};
typeof window < "u" && "requestAnimationFrame" in window && (tn = function(t) {
  return window.requestAnimationFrame(t);
}, nn = function(t) {
  return window.cancelAnimationFrame(t);
});
var xt = 0, Ze = /* @__PURE__ */ new Map();
function rn(e) {
  Ze.delete(e);
}
var We = function(t) {
  var n = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : 1;
  xt += 1;
  var r = xt;
  function o(i) {
    if (i === 0)
      rn(r), t();
    else {
      var a = tn(function() {
        o(i - 1);
      });
      Ze.set(r, a);
    }
  }
  return o(n), r;
};
We.cancel = function(e) {
  var t = Ze.get(e);
  return rn(e), nn(t);
};
const Qr = function() {
  var e = v.useRef(null);
  function t() {
    We.cancel(e.current);
  }
  function n(r) {
    var o = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : 2;
    t();
    var i = We(function() {
      o <= 1 ? r({
        isCanceled: function() {
          return i !== e.current;
        }
      }) : n(r, o - 1);
    });
    e.current = i;
  }
  return v.useEffect(function() {
    return function() {
      t();
    };
  }, []), [n, t];
};
var Gr = [j, J, X, Xe], qr = [j, Gt], on = !1, Yr = !0;
function an(e) {
  return e === X || e === Xe;
}
const Jr = function(e, t, n) {
  var r = Ke(Ct), o = V(r, 2), i = o[0], a = o[1], s = Qr(), l = V(s, 2), u = l[0], d = l[1];
  function c() {
    a(j, !0);
  }
  var m = t ? qr : Gr;
  return en(function() {
    if (i !== Ct && i !== Xe) {
      var f = m.indexOf(i), g = m[f + 1], S = n(i);
      S === on ? a(g, !0) : g && u(function(y) {
        function _() {
          y.isCanceled() || a(g, !0);
        }
        S === !0 ? _() : Promise.resolve(S).then(_);
      });
    }
  }, [e, i]), v.useEffect(function() {
    return function() {
      d();
    };
  }, []), [c, i];
};
function Xr(e, t, n, r) {
  var o = r.motionEnter, i = o === void 0 ? !0 : o, a = r.motionAppear, s = a === void 0 ? !0 : a, l = r.motionLeave, u = l === void 0 ? !0 : l, d = r.motionDeadline, c = r.motionLeaveImmediately, m = r.onAppearPrepare, f = r.onEnterPrepare, g = r.onLeavePrepare, S = r.onAppearStart, y = r.onEnterStart, _ = r.onLeaveStart, w = r.onAppearActive, A = r.onEnterActive, E = r.onLeaveActive, T = r.onAppearEnd, p = r.onEnterEnd, C = r.onLeaveEnd, L = r.onVisibleChanged, Q = Ke(), G = V(Q, 2), I = G[0], W = G[1], x = Kr(U), H = V(x, 2), F = H[0], z = H[1], Ae = Ke(null), q = V(Ae, 2), cn = q[0], et = q[1], N = F(), ne = K(!1), Te = K(null);
  function re() {
    return n();
  }
  var tt = K(!1);
  function nt() {
    z(U), et(null, !0);
  }
  var rt = Ve(function(O) {
    var R = F();
    if (R !== U) {
      var M = re();
      if (!(O && !O.deadline && O.target !== M)) {
        var oe = tt.current, ie;
        R === ae && oe ? ie = T == null ? void 0 : T(M, O) : R === se && oe ? ie = p == null ? void 0 : p(M, O) : R === ue && oe && (ie = C == null ? void 0 : C(M, O)), oe && ie !== !1 && nt();
      }
    }
  }), ln = Br(rt), fn = V(ln, 1), dn = fn[0], ot = function(R) {
    switch (R) {
      case ae:
        return P(P(P({}, j, m), J, S), X, w);
      case se:
        return P(P(P({}, j, f), J, y), X, A);
      case ue:
        return P(P(P({}, j, g), J, _), X, E);
      default:
        return {};
    }
  }, Z = v.useMemo(function() {
    return ot(N);
  }, [N]), mn = Jr(N, !e, function(O) {
    if (O === j) {
      var R = Z[j];
      return R ? R(re()) : on;
    }
    if (B in Z) {
      var M;
      et(((M = Z[B]) === null || M === void 0 ? void 0 : M.call(Z, re(), null)) || null);
    }
    return B === X && N !== U && (dn(re()), d > 0 && (clearTimeout(Te.current), Te.current = setTimeout(function() {
      rt({
        deadline: !0
      });
    }, d))), B === Gt && nt(), Yr;
  }), it = V(mn, 2), pn = it[0], B = it[1], vn = an(B);
  tt.current = vn;
  var at = K(null);
  en(function() {
    if (!(ne.current && at.current === t)) {
      W(t);
      var O = ne.current;
      ne.current = !0;
      var R;
      !O && t && s && (R = ae), O && t && i && (R = se), (O && !t && u || !O && c && !t && u) && (R = ue);
      var M = ot(R);
      R && (e || M[j]) ? (z(R), pn()) : z(U), at.current = t;
    }
  }, [t]), ee(function() {
    // Cancel appear
    (N === ae && !s || // Cancel enter
    N === se && !i || // Cancel leave
    N === ue && !u) && z(U);
  }, [s, i, u]), ee(function() {
    return function() {
      ne.current = !1, clearTimeout(Te.current);
    };
  }, []);
  var Pe = v.useRef(!1);
  ee(function() {
    I && (Pe.current = !0), I !== void 0 && N === U && ((Pe.current || I) && (L == null || L(I)), Pe.current = !0);
  }, [I, N]);
  var xe = cn;
  return Z[j] && B === J && (xe = h({
    transition: "none"
  }, xe)), [N, B, xe, I ?? t];
}
function Zr(e) {
  var t = e;
  D(e) === "object" && (t = e.transitionSupport);
  function n(o, i) {
    return !!(o.motionName && t && i !== !1);
  }
  var r = /* @__PURE__ */ v.forwardRef(function(o, i) {
    var a = o.visible, s = a === void 0 ? !0 : a, l = o.removeOnLeave, u = l === void 0 ? !0 : l, d = o.forceRender, c = o.children, m = o.motionName, f = o.leavedClassName, g = o.eventProps, S = v.useContext(Nr), y = S.motion, _ = n(o, y), w = K(), A = K();
    function E() {
      try {
        return w.current instanceof HTMLElement ? w.current : wr(A.current);
      } catch {
        return null;
      }
    }
    var T = Xr(_, s, E, o), p = V(T, 4), C = p[0], L = p[1], Q = p[2], G = p[3], I = v.useRef(G);
    G && (I.current = !0);
    var W = v.useCallback(function(q) {
      w.current = q, Lr(i, q);
    }, [i]), x, H = h(h({}, g), {}, {
      visible: s
    });
    if (!c)
      x = null;
    else if (C === U)
      G ? x = c(h({}, H), W) : !u && I.current && f ? x = c(h(h({}, H), {}, {
        className: f
      }), W) : d || !u && !f ? x = c(h(h({}, H), {}, {
        style: {
          display: "none"
        }
      }), W) : x = null;
    else {
      var F;
      L === j ? F = "prepare" : an(L) ? F = "active" : L === J && (F = "start");
      var z = Pt(m, "".concat(C, "-").concat(F));
      x = c(h(h({}, H), {}, {
        className: fe(Pt(m, C), P(P({}, z, z && F), m, typeof m == "string")),
        style: Q
      }), W);
    }
    if (/* @__PURE__ */ v.isValidElement(x) && kr(x)) {
      var Ae = Ir(x);
      Ae || (x = /* @__PURE__ */ v.cloneElement(x, {
        ref: W
      }));
    }
    return /* @__PURE__ */ v.createElement($r, {
      ref: A
    }, x);
  });
  return r.displayName = "CSSMotion", r;
}
const sn = Zr(Zt);
function He() {
  return He = Object.assign ? Object.assign.bind() : function(e) {
    for (var t = 1; t < arguments.length; t++) {
      var n = arguments[t];
      for (var r in n) ({}).hasOwnProperty.call(n, r) && (e[r] = n[r]);
    }
    return e;
  }, He.apply(null, arguments);
}
var ze = "add", Be = "keep", Qe = "remove", je = "removed";
function eo(e) {
  var t;
  return e && D(e) === "object" && "key" in e ? t = e : t = {
    key: e
  }, h(h({}, t), {}, {
    key: String(t.key)
  });
}
function Ge() {
  var e = arguments.length > 0 && arguments[0] !== void 0 ? arguments[0] : [];
  return e.map(eo);
}
function to() {
  var e = arguments.length > 0 && arguments[0] !== void 0 ? arguments[0] : [], t = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : [], n = [], r = 0, o = t.length, i = Ge(e), a = Ge(t);
  i.forEach(function(u) {
    for (var d = !1, c = r; c < o; c += 1) {
      var m = a[c];
      if (m.key === u.key) {
        r < c && (n = n.concat(a.slice(r, c).map(function(f) {
          return h(h({}, f), {}, {
            status: ze
          });
        })), r = c), n.push(h(h({}, m), {}, {
          status: Be
        })), r += 1, d = !0;
        break;
      }
    }
    d || n.push(h(h({}, u), {}, {
      status: Qe
    }));
  }), r < o && (n = n.concat(a.slice(r).map(function(u) {
    return h(h({}, u), {}, {
      status: ze
    });
  })));
  var s = {};
  n.forEach(function(u) {
    var d = u.key;
    s[d] = (s[d] || 0) + 1;
  });
  var l = Object.keys(s).filter(function(u) {
    return s[u] > 1;
  });
  return l.forEach(function(u) {
    n = n.filter(function(d) {
      var c = d.key, m = d.status;
      return c !== u || m !== Qe;
    }), n.forEach(function(d) {
      d.key === u && (d.status = Be);
    });
  }), n;
}
var no = ["component", "children", "onVisibleChanged", "onAllRemoved"], ro = ["status"], oo = ["eventProps", "visible", "children", "motionName", "motionAppear", "motionEnter", "motionLeave", "motionLeaveImmediately", "motionDeadline", "removeOnLeave", "leavedClassName", "onAppearPrepare", "onAppearStart", "onAppearActive", "onAppearEnd", "onEnterStart", "onEnterActive", "onEnterEnd", "onLeaveStart", "onLeaveActive", "onLeaveEnd"];
function io(e) {
  var t = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : sn, n = /* @__PURE__ */ function(r) {
    Ht(i, r);
    var o = Bt(i);
    function i() {
      var a;
      Kt(this, i);
      for (var s = arguments.length, l = new Array(s), u = 0; u < s; u++)
        l[u] = arguments[u];
      return a = o.call.apply(o, [this].concat(l)), P(Ue(a), "state", {
        keyEntities: []
      }), P(Ue(a), "removeKey", function(d) {
        a.setState(function(c) {
          var m = c.keyEntities.map(function(f) {
            return f.key !== d ? f : h(h({}, f), {}, {
              status: je
            });
          });
          return {
            keyEntities: m
          };
        }, function() {
          var c = a.state.keyEntities, m = c.filter(function(f) {
            var g = f.status;
            return g !== je;
          }).length;
          m === 0 && a.props.onAllRemoved && a.props.onAllRemoved();
        });
      }), a;
    }
    return Wt(i, [{
      key: "render",
      value: function() {
        var s = this, l = this.state.keyEntities, u = this.props, d = u.component, c = u.children, m = u.onVisibleChanged;
        u.onAllRemoved;
        var f = _t(u, no), g = d || v.Fragment, S = {};
        return oo.forEach(function(y) {
          S[y] = f[y], delete f[y];
        }), delete f.keys, /* @__PURE__ */ v.createElement(g, f, l.map(function(y, _) {
          var w = y.status, A = _t(y, ro), E = w === ze || w === Be;
          return /* @__PURE__ */ v.createElement(t, He({}, S, {
            key: A.key,
            visible: E,
            eventProps: A,
            onVisibleChanged: function(p) {
              m == null || m(p, {
                key: A.key
              }), p || s.removeKey(A.key);
            }
          }), function(T, p) {
            return c(h(h({}, T), {}, {
              index: _
            }), p);
          });
        }));
      }
    }], [{
      key: "getDerivedStateFromProps",
      value: function(s, l) {
        var u = s.keys, d = l.keyEntities, c = Ge(u), m = to(d, c);
        return {
          keyEntities: m.filter(function(f) {
            var g = d.find(function(S) {
              var y = S.key;
              return f.key === y;
            });
            return !(g && g.status === je && f.status === Qe);
          })
        };
      }
    }]), i;
  }(v.Component);
  return P(n, "defaultProps", {
    component: "div"
  }), n;
}
io(Zt);
const un = /* @__PURE__ */ v.createContext({}), Ot = () => ({
  height: 0
}), Lt = (e) => ({
  height: e.scrollHeight
});
function ao(e) {
  const {
    title: t,
    onOpenChange: n,
    open: r,
    children: o,
    className: i,
    style: a,
    classNames: s = {},
    styles: l = {},
    closable: u,
    forceRender: d
  } = e, {
    prefixCls: c
  } = v.useContext(un), m = `${c}-header`;
  return /* @__PURE__ */ v.createElement(sn, {
    motionEnter: !0,
    motionLeave: !0,
    motionName: `${m}-motion`,
    leavedClassName: `${m}-motion-hidden`,
    onEnterStart: Ot,
    onEnterActive: Lt,
    onLeaveStart: Lt,
    onLeaveActive: Ot,
    visible: r,
    forceRender: d
  }, ({
    className: f,
    style: g
  }) => /* @__PURE__ */ v.createElement("div", {
    className: fe(m, f, i),
    style: {
      ...g,
      ...a
    }
  }, (u !== !1 || t) && /* @__PURE__ */ v.createElement("div", {
    className: (
      // We follow antd naming standard here.
      // So the header part is use `-header` suffix.
      // Though its little bit weird for double `-header`.
      fe(`${m}-header`, s.header)
    ),
    style: {
      ...l.header
    }
  }, /* @__PURE__ */ v.createElement("div", {
    className: `${m}-title`
  }, t), u !== !1 && /* @__PURE__ */ v.createElement("div", {
    className: `${m}-close`
  }, /* @__PURE__ */ v.createElement(An, {
    type: "text",
    icon: /* @__PURE__ */ v.createElement(Rn, null),
    size: "small",
    onClick: () => {
      n == null || n(!r);
    }
  }))), o && /* @__PURE__ */ v.createElement("div", {
    className: fe(`${m}-content`, s.content),
    style: {
      ...l.content
    }
  }, o)));
}
const co = fr(({
  slots: e,
  ...t
}) => {
  const {
    getPrefixCls: n
  } = $.useContext(Tn.ConfigContext);
  return /* @__PURE__ */ Le.jsx(un.Provider, {
    value: {
      prefixCls: n("sender")
    },
    children: /* @__PURE__ */ Le.jsx(ao, {
      ...t,
      title: e.title ? /* @__PURE__ */ Le.jsx(yr, {
        slot: e.title
      }) : t.title
    })
  });
});
export {
  co as SenderHeader,
  co as default
};
