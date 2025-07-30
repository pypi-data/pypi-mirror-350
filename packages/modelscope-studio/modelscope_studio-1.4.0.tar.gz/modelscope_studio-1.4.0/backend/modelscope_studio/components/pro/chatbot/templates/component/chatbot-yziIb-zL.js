var jr = (e) => {
  throw TypeError(e);
};
var Nr = (e, t, r) => t.has(e) || jr("Cannot " + r);
var He = (e, t, r) => (Nr(e, t, "read from private field"), r ? r.call(e) : t.get(e)), Fr = (e, t, r) => t.has(e) ? jr("Cannot add the same private member more than once") : t instanceof WeakSet ? t.add(e) : t.set(e, r), kr = (e, t, r, n) => (Nr(e, t, "write to private field"), n ? n.call(e, r) : t.set(e, r), r);
import { i as Ao, a as ye, r as zo, b as Do, w as mt, g as Ho, c as F, d as Sr, e as pt, o as zr } from "./Index-BnNHOsOb.js";
const R = window.ms_globals.React, c = window.ms_globals.React, Oo = window.ms_globals.React.isValidElement, jo = window.ms_globals.React.version, J = window.ms_globals.React.useRef, No = window.ms_globals.React.useLayoutEffect, Ee = window.ms_globals.React.useEffect, Fo = window.ms_globals.React.useCallback, fe = window.ms_globals.React.useMemo, ko = window.ms_globals.React.forwardRef, Ze = window.ms_globals.React.useState, Ar = window.ms_globals.ReactDOM, yt = window.ms_globals.ReactDOM.createPortal, Bo = window.ms_globals.antdIcons.FileTextFilled, Wo = window.ms_globals.antdIcons.CloseCircleFilled, Vo = window.ms_globals.antdIcons.FileExcelFilled, Xo = window.ms_globals.antdIcons.FileImageFilled, Uo = window.ms_globals.antdIcons.FileMarkdownFilled, Go = window.ms_globals.antdIcons.FilePdfFilled, Ko = window.ms_globals.antdIcons.FilePptFilled, qo = window.ms_globals.antdIcons.FileWordFilled, Yo = window.ms_globals.antdIcons.FileZipFilled, Qo = window.ms_globals.antdIcons.PlusOutlined, Zo = window.ms_globals.antdIcons.LeftOutlined, Jo = window.ms_globals.antdIcons.RightOutlined, es = window.ms_globals.antdIcons.CloseOutlined, Fn = window.ms_globals.antdIcons.CheckOutlined, ts = window.ms_globals.antdIcons.DeleteOutlined, rs = window.ms_globals.antdIcons.EditOutlined, ns = window.ms_globals.antdIcons.SyncOutlined, os = window.ms_globals.antdIcons.DislikeOutlined, ss = window.ms_globals.antdIcons.LikeOutlined, is = window.ms_globals.antdIcons.CopyOutlined, as = window.ms_globals.antdIcons.EyeOutlined, ls = window.ms_globals.antdIcons.ArrowDownOutlined, cs = window.ms_globals.antd.ConfigProvider, kn = window.ms_globals.antd.Upload, Je = window.ms_globals.antd.theme, us = window.ms_globals.antd.Progress, fs = window.ms_globals.antd.Image, re = window.ms_globals.antd.Button, Ce = window.ms_globals.antd.Flex, $e = window.ms_globals.antd.Typography, ds = window.ms_globals.antd.Avatar, ms = window.ms_globals.antd.Popconfirm, ps = window.ms_globals.antd.Tooltip, gs = window.ms_globals.antd.Collapse, hs = window.ms_globals.antd.Input, An = window.ms_globals.createItemsContext.createItemsContext, ys = window.ms_globals.internalContext.useContextPropsContext, Dr = window.ms_globals.internalContext.ContextPropsProvider, Xe = window.ms_globals.antdCssinjs.unit, Xt = window.ms_globals.antdCssinjs.token2CSSVar, Hr = window.ms_globals.antdCssinjs.useStyleRegister, vs = window.ms_globals.antdCssinjs.useCSSVarRegister, bs = window.ms_globals.antdCssinjs.createTheme, Ss = window.ms_globals.antdCssinjs.useCacheToken, zn = window.ms_globals.antdCssinjs.Keyframes, vt = window.ms_globals.components.Markdown;
var xs = /\s/;
function ws(e) {
  for (var t = e.length; t-- && xs.test(e.charAt(t)); )
    ;
  return t;
}
var _s = /^\s+/;
function Es(e) {
  return e && e.slice(0, ws(e) + 1).replace(_s, "");
}
var Br = NaN, Cs = /^[-+]0x[0-9a-f]+$/i, Ts = /^0b[01]+$/i, $s = /^0o[0-7]+$/i, Ps = parseInt;
function Wr(e) {
  if (typeof e == "number")
    return e;
  if (Ao(e))
    return Br;
  if (ye(e)) {
    var t = typeof e.valueOf == "function" ? e.valueOf() : e;
    e = ye(t) ? t + "" : t;
  }
  if (typeof e != "string")
    return e === 0 ? e : +e;
  e = Es(e);
  var r = Ts.test(e);
  return r || $s.test(e) ? Ps(e.slice(2), r ? 2 : 8) : Cs.test(e) ? Br : +e;
}
var Ut = function() {
  return zo.Date.now();
}, Rs = "Expected a function", Is = Math.max, Ms = Math.min;
function Ls(e, t, r) {
  var n, o, s, i, a, l, u = 0, f = !1, m = !1, d = !0;
  if (typeof e != "function")
    throw new TypeError(Rs);
  t = Wr(t) || 0, ye(r) && (f = !!r.leading, m = "maxWait" in r, s = m ? Is(Wr(r.maxWait) || 0, t) : s, d = "trailing" in r ? !!r.trailing : d);
  function h(b) {
    var I = n, E = o;
    return n = o = void 0, u = b, i = e.apply(E, I), i;
  }
  function v(b) {
    return u = b, a = setTimeout(y, t), f ? h(b) : i;
  }
  function g(b) {
    var I = b - l, E = b - u, O = t - I;
    return m ? Ms(O, s - E) : O;
  }
  function p(b) {
    var I = b - l, E = b - u;
    return l === void 0 || I >= t || I < 0 || m && E >= s;
  }
  function y() {
    var b = Ut();
    if (p(b))
      return T(b);
    a = setTimeout(y, g(b));
  }
  function T(b) {
    return a = void 0, d && n ? h(b) : (n = o = void 0, i);
  }
  function P() {
    a !== void 0 && clearTimeout(a), u = 0, n = l = o = a = void 0;
  }
  function _() {
    return a === void 0 ? i : T(Ut());
  }
  function $() {
    var b = Ut(), I = p(b);
    if (n = arguments, o = this, l = b, I) {
      if (a === void 0)
        return v(l);
      if (m)
        return clearTimeout(a), a = setTimeout(y, t), h(l);
    }
    return a === void 0 && (a = setTimeout(y, t)), i;
  }
  return $.cancel = P, $.flush = _, $;
}
function Os(e, t) {
  return Do(e, t);
}
var Dn = {
  exports: {}
}, Et = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var js = c, Ns = Symbol.for("react.element"), Fs = Symbol.for("react.fragment"), ks = Object.prototype.hasOwnProperty, As = js.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, zs = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function Hn(e, t, r) {
  var n, o = {}, s = null, i = null;
  r !== void 0 && (s = "" + r), t.key !== void 0 && (s = "" + t.key), t.ref !== void 0 && (i = t.ref);
  for (n in t) ks.call(t, n) && !zs.hasOwnProperty(n) && (o[n] = t[n]);
  if (e && e.defaultProps) for (n in t = e.defaultProps, t) o[n] === void 0 && (o[n] = t[n]);
  return {
    $$typeof: Ns,
    type: e,
    key: s,
    ref: i,
    props: o,
    _owner: As.current
  };
}
Et.Fragment = Fs;
Et.jsx = Hn;
Et.jsxs = Hn;
Dn.exports = Et;
var S = Dn.exports;
const {
  SvelteComponent: Ds,
  assign: Vr,
  binding_callbacks: Xr,
  check_outros: Hs,
  children: Bn,
  claim_element: Wn,
  claim_space: Bs,
  component_subscribe: Ur,
  compute_slots: Ws,
  create_slot: Vs,
  detach: Be,
  element: Vn,
  empty: Gr,
  exclude_internal_props: Kr,
  get_all_dirty_from_scope: Xs,
  get_slot_changes: Us,
  group_outros: Gs,
  init: Ks,
  insert_hydration: gt,
  safe_not_equal: qs,
  set_custom_element_data: Xn,
  space: Ys,
  transition_in: ht,
  transition_out: nr,
  update_slot_base: Qs
} = window.__gradio__svelte__internal, {
  beforeUpdate: Zs,
  getContext: Js,
  onDestroy: ei,
  setContext: ti
} = window.__gradio__svelte__internal;
function qr(e) {
  let t, r;
  const n = (
    /*#slots*/
    e[7].default
  ), o = Vs(
    n,
    e,
    /*$$scope*/
    e[6],
    null
  );
  return {
    c() {
      t = Vn("svelte-slot"), o && o.c(), this.h();
    },
    l(s) {
      t = Wn(s, "SVELTE-SLOT", {
        class: !0
      });
      var i = Bn(t);
      o && o.l(i), i.forEach(Be), this.h();
    },
    h() {
      Xn(t, "class", "svelte-1rt0kpf");
    },
    m(s, i) {
      gt(s, t, i), o && o.m(t, null), e[9](t), r = !0;
    },
    p(s, i) {
      o && o.p && (!r || i & /*$$scope*/
      64) && Qs(
        o,
        n,
        s,
        /*$$scope*/
        s[6],
        r ? Us(
          n,
          /*$$scope*/
          s[6],
          i,
          null
        ) : Xs(
          /*$$scope*/
          s[6]
        ),
        null
      );
    },
    i(s) {
      r || (ht(o, s), r = !0);
    },
    o(s) {
      nr(o, s), r = !1;
    },
    d(s) {
      s && Be(t), o && o.d(s), e[9](null);
    }
  };
}
function ri(e) {
  let t, r, n, o, s = (
    /*$$slots*/
    e[4].default && qr(e)
  );
  return {
    c() {
      t = Vn("react-portal-target"), r = Ys(), s && s.c(), n = Gr(), this.h();
    },
    l(i) {
      t = Wn(i, "REACT-PORTAL-TARGET", {
        class: !0
      }), Bn(t).forEach(Be), r = Bs(i), s && s.l(i), n = Gr(), this.h();
    },
    h() {
      Xn(t, "class", "svelte-1rt0kpf");
    },
    m(i, a) {
      gt(i, t, a), e[8](t), gt(i, r, a), s && s.m(i, a), gt(i, n, a), o = !0;
    },
    p(i, [a]) {
      /*$$slots*/
      i[4].default ? s ? (s.p(i, a), a & /*$$slots*/
      16 && ht(s, 1)) : (s = qr(i), s.c(), ht(s, 1), s.m(n.parentNode, n)) : s && (Gs(), nr(s, 1, 1, () => {
        s = null;
      }), Hs());
    },
    i(i) {
      o || (ht(s), o = !0);
    },
    o(i) {
      nr(s), o = !1;
    },
    d(i) {
      i && (Be(t), Be(r), Be(n)), e[8](null), s && s.d(i);
    }
  };
}
function Yr(e) {
  const {
    svelteInit: t,
    ...r
  } = e;
  return r;
}
function ni(e, t, r) {
  let n, o, {
    $$slots: s = {},
    $$scope: i
  } = t;
  const a = Ws(s);
  let {
    svelteInit: l
  } = t;
  const u = mt(Yr(t)), f = mt();
  Ur(e, f, (_) => r(0, n = _));
  const m = mt();
  Ur(e, m, (_) => r(1, o = _));
  const d = [], h = Js("$$ms-gr-react-wrapper"), {
    slotKey: v,
    slotIndex: g,
    subSlotIndex: p
  } = Ho() || {}, y = l({
    parent: h,
    props: u,
    target: f,
    slot: m,
    slotKey: v,
    slotIndex: g,
    subSlotIndex: p,
    onDestroy(_) {
      d.push(_);
    }
  });
  ti("$$ms-gr-react-wrapper", y), Zs(() => {
    u.set(Yr(t));
  }), ei(() => {
    d.forEach((_) => _());
  });
  function T(_) {
    Xr[_ ? "unshift" : "push"](() => {
      n = _, f.set(n);
    });
  }
  function P(_) {
    Xr[_ ? "unshift" : "push"](() => {
      o = _, m.set(o);
    });
  }
  return e.$$set = (_) => {
    r(17, t = Vr(Vr({}, t), Kr(_))), "svelteInit" in _ && r(5, l = _.svelteInit), "$$scope" in _ && r(6, i = _.$$scope);
  }, t = Kr(t), [n, o, f, m, a, l, i, s, T, P];
}
class oi extends Ds {
  constructor(t) {
    super(), Ks(this, t, ni, ri, qs, {
      svelteInit: 5
    });
  }
}
const {
  SvelteComponent: yc
} = window.__gradio__svelte__internal, Qr = window.ms_globals.rerender, Gt = window.ms_globals.tree;
function si(e, t = {}) {
  function r(n) {
    const o = mt(), s = new oi({
      ...n,
      props: {
        svelteInit(i) {
          window.ms_globals.autokey += 1;
          const a = {
            key: window.ms_globals.autokey,
            svelteInstance: o,
            reactComponent: e,
            props: i.props,
            slot: i.slot,
            target: i.target,
            slotIndex: i.slotIndex,
            subSlotIndex: i.subSlotIndex,
            ignore: t.ignore,
            slotKey: i.slotKey,
            nodes: []
          }, l = i.parent ?? Gt;
          return l.nodes = [...l.nodes, a], Qr({
            createPortal: yt,
            node: Gt
          }), i.onDestroy(() => {
            l.nodes = l.nodes.filter((u) => u.svelteInstance !== o), Qr({
              createPortal: yt,
              node: Gt
            });
          }), a;
        },
        ...n.props
      }
    });
    return o.set(s), s;
  }
  return new Promise((n) => {
    window.ms_globals.initializePromise.then(() => {
      n(r);
    });
  });
}
const ii = "1.3.0", ai = /* @__PURE__ */ c.createContext({}), li = {
  classNames: {},
  styles: {},
  className: "",
  style: {}
}, Ct = (e) => {
  const t = c.useContext(ai);
  return c.useMemo(() => ({
    ...li,
    ...t[e]
  }), [t[e]]);
};
function ve() {
  return ve = Object.assign ? Object.assign.bind() : function(e) {
    for (var t = 1; t < arguments.length; t++) {
      var r = arguments[t];
      for (var n in r) ({}).hasOwnProperty.call(r, n) && (e[n] = r[n]);
    }
    return e;
  }, ve.apply(null, arguments);
}
function Pe() {
  const {
    getPrefixCls: e,
    direction: t,
    csp: r,
    iconPrefixCls: n,
    theme: o
  } = c.useContext(cs.ConfigContext);
  return {
    theme: o,
    getPrefixCls: e,
    direction: t,
    csp: r,
    iconPrefixCls: n
  };
}
function je(e) {
  var t = R.useRef();
  t.current = e;
  var r = R.useCallback(function() {
    for (var n, o = arguments.length, s = new Array(o), i = 0; i < o; i++)
      s[i] = arguments[i];
    return (n = t.current) === null || n === void 0 ? void 0 : n.call.apply(n, [t].concat(s));
  }, []);
  return r;
}
function ci(e) {
  if (Array.isArray(e)) return e;
}
function ui(e, t) {
  var r = e == null ? null : typeof Symbol < "u" && e[Symbol.iterator] || e["@@iterator"];
  if (r != null) {
    var n, o, s, i, a = [], l = !0, u = !1;
    try {
      if (s = (r = r.call(e)).next, t !== 0) for (; !(l = (n = s.call(r)).done) && (a.push(n.value), a.length !== t); l = !0) ;
    } catch (f) {
      u = !0, o = f;
    } finally {
      try {
        if (!l && r.return != null && (i = r.return(), Object(i) !== i)) return;
      } finally {
        if (u) throw o;
      }
    }
    return a;
  }
}
function Zr(e, t) {
  (t == null || t > e.length) && (t = e.length);
  for (var r = 0, n = Array(t); r < t; r++) n[r] = e[r];
  return n;
}
function fi(e, t) {
  if (e) {
    if (typeof e == "string") return Zr(e, t);
    var r = {}.toString.call(e).slice(8, -1);
    return r === "Object" && e.constructor && (r = e.constructor.name), r === "Map" || r === "Set" ? Array.from(e) : r === "Arguments" || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r) ? Zr(e, t) : void 0;
  }
}
function di() {
  throw new TypeError(`Invalid attempt to destructure non-iterable instance.
In order to be iterable, non-array objects must have a [Symbol.iterator]() method.`);
}
function bt(e, t) {
  return ci(e) || ui(e, t) || fi(e, t) || di();
}
function Tt() {
  return !!(typeof window < "u" && window.document && window.document.createElement);
}
var Jr = Tt() ? R.useLayoutEffect : R.useEffect, Un = function(t, r) {
  var n = R.useRef(!0);
  Jr(function() {
    return t(n.current);
  }, r), Jr(function() {
    return n.current = !1, function() {
      n.current = !0;
    };
  }, []);
}, en = function(t, r) {
  Un(function(n) {
    if (!n)
      return t();
  }, r);
};
function et(e) {
  var t = R.useRef(!1), r = R.useState(e), n = bt(r, 2), o = n[0], s = n[1];
  R.useEffect(function() {
    return t.current = !1, function() {
      t.current = !0;
    };
  }, []);
  function i(a, l) {
    l && t.current || s(a);
  }
  return [o, i];
}
function Kt(e) {
  return e !== void 0;
}
function mi(e, t) {
  var r = t || {}, n = r.defaultValue, o = r.value, s = r.onChange, i = r.postState, a = et(function() {
    return Kt(o) ? o : Kt(n) ? typeof n == "function" ? n() : n : typeof e == "function" ? e() : e;
  }), l = bt(a, 2), u = l[0], f = l[1], m = o !== void 0 ? o : u, d = i ? i(m) : m, h = je(s), v = et([m]), g = bt(v, 2), p = g[0], y = g[1];
  en(function() {
    var P = p[0];
    u !== P && h(u, P);
  }, [p]), en(function() {
    Kt(o) || f(o);
  }, [o]);
  var T = je(function(P, _) {
    f(P, _), y([m], _);
  });
  return [d, T];
}
function Re(e) {
  "@babel/helpers - typeof";
  return Re = typeof Symbol == "function" && typeof Symbol.iterator == "symbol" ? function(t) {
    return typeof t;
  } : function(t) {
    return t && typeof Symbol == "function" && t.constructor === Symbol && t !== Symbol.prototype ? "symbol" : typeof t;
  }, Re(e);
}
var Gn = {
  exports: {}
}, H = {};
/**
 * @license React
 * react-is.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var xr = Symbol.for("react.element"), wr = Symbol.for("react.portal"), $t = Symbol.for("react.fragment"), Pt = Symbol.for("react.strict_mode"), Rt = Symbol.for("react.profiler"), It = Symbol.for("react.provider"), Mt = Symbol.for("react.context"), pi = Symbol.for("react.server_context"), Lt = Symbol.for("react.forward_ref"), Ot = Symbol.for("react.suspense"), jt = Symbol.for("react.suspense_list"), Nt = Symbol.for("react.memo"), Ft = Symbol.for("react.lazy"), gi = Symbol.for("react.offscreen"), Kn;
Kn = Symbol.for("react.module.reference");
function me(e) {
  if (typeof e == "object" && e !== null) {
    var t = e.$$typeof;
    switch (t) {
      case xr:
        switch (e = e.type, e) {
          case $t:
          case Rt:
          case Pt:
          case Ot:
          case jt:
            return e;
          default:
            switch (e = e && e.$$typeof, e) {
              case pi:
              case Mt:
              case Lt:
              case Ft:
              case Nt:
              case It:
                return e;
              default:
                return t;
            }
        }
      case wr:
        return t;
    }
  }
}
H.ContextConsumer = Mt;
H.ContextProvider = It;
H.Element = xr;
H.ForwardRef = Lt;
H.Fragment = $t;
H.Lazy = Ft;
H.Memo = Nt;
H.Portal = wr;
H.Profiler = Rt;
H.StrictMode = Pt;
H.Suspense = Ot;
H.SuspenseList = jt;
H.isAsyncMode = function() {
  return !1;
};
H.isConcurrentMode = function() {
  return !1;
};
H.isContextConsumer = function(e) {
  return me(e) === Mt;
};
H.isContextProvider = function(e) {
  return me(e) === It;
};
H.isElement = function(e) {
  return typeof e == "object" && e !== null && e.$$typeof === xr;
};
H.isForwardRef = function(e) {
  return me(e) === Lt;
};
H.isFragment = function(e) {
  return me(e) === $t;
};
H.isLazy = function(e) {
  return me(e) === Ft;
};
H.isMemo = function(e) {
  return me(e) === Nt;
};
H.isPortal = function(e) {
  return me(e) === wr;
};
H.isProfiler = function(e) {
  return me(e) === Rt;
};
H.isStrictMode = function(e) {
  return me(e) === Pt;
};
H.isSuspense = function(e) {
  return me(e) === Ot;
};
H.isSuspenseList = function(e) {
  return me(e) === jt;
};
H.isValidElementType = function(e) {
  return typeof e == "string" || typeof e == "function" || e === $t || e === Rt || e === Pt || e === Ot || e === jt || e === gi || typeof e == "object" && e !== null && (e.$$typeof === Ft || e.$$typeof === Nt || e.$$typeof === It || e.$$typeof === Mt || e.$$typeof === Lt || e.$$typeof === Kn || e.getModuleId !== void 0);
};
H.typeOf = me;
Gn.exports = H;
var qt = Gn.exports, hi = Symbol.for("react.element"), yi = Symbol.for("react.transitional.element"), vi = Symbol.for("react.fragment");
function bi(e) {
  return (
    // Base object type
    e && Re(e) === "object" && // React Element type
    (e.$$typeof === hi || e.$$typeof === yi) && // React Fragment type
    e.type === vi
  );
}
var Si = Number(jo.split(".")[0]), xi = function(t, r) {
  typeof t == "function" ? t(r) : Re(t) === "object" && t && "current" in t && (t.current = r);
}, wi = function(t) {
  var r, n;
  if (!t)
    return !1;
  if (qn(t) && Si >= 19)
    return !0;
  var o = qt.isMemo(t) ? t.type.type : t.type;
  return !(typeof o == "function" && !((r = o.prototype) !== null && r !== void 0 && r.render) && o.$$typeof !== qt.ForwardRef || typeof t == "function" && !((n = t.prototype) !== null && n !== void 0 && n.render) && t.$$typeof !== qt.ForwardRef);
};
function qn(e) {
  return /* @__PURE__ */ Oo(e) && !bi(e);
}
var _i = function(t) {
  if (t && qn(t)) {
    var r = t;
    return r.props.propertyIsEnumerable("ref") ? r.props.ref : r.ref;
  }
  return null;
};
function Ei(e, t) {
  if (Re(e) != "object" || !e) return e;
  var r = e[Symbol.toPrimitive];
  if (r !== void 0) {
    var n = r.call(e, t);
    if (Re(n) != "object") return n;
    throw new TypeError("@@toPrimitive must return a primitive value.");
  }
  return (t === "string" ? String : Number)(e);
}
function Ci(e) {
  var t = Ei(e, "string");
  return Re(t) == "symbol" ? t : t + "";
}
function Ti(e, t, r) {
  return (t = Ci(t)) in e ? Object.defineProperty(e, t, {
    value: r,
    enumerable: !0,
    configurable: !0,
    writable: !0
  }) : e[t] = r, e;
}
function tn(e, t) {
  var r = Object.keys(e);
  if (Object.getOwnPropertySymbols) {
    var n = Object.getOwnPropertySymbols(e);
    t && (n = n.filter(function(o) {
      return Object.getOwnPropertyDescriptor(e, o).enumerable;
    })), r.push.apply(r, n);
  }
  return r;
}
function $i(e) {
  for (var t = 1; t < arguments.length; t++) {
    var r = arguments[t] != null ? arguments[t] : {};
    t % 2 ? tn(Object(r), !0).forEach(function(n) {
      Ti(e, n, r[n]);
    }) : Object.getOwnPropertyDescriptors ? Object.defineProperties(e, Object.getOwnPropertyDescriptors(r)) : tn(Object(r)).forEach(function(n) {
      Object.defineProperty(e, n, Object.getOwnPropertyDescriptor(r, n));
    });
  }
  return e;
}
const ot = /* @__PURE__ */ c.createContext(null);
function rn(e) {
  const {
    getDropContainer: t,
    className: r,
    prefixCls: n,
    children: o
  } = e, {
    disabled: s
  } = c.useContext(ot), [i, a] = c.useState(), [l, u] = c.useState(null);
  if (c.useEffect(() => {
    const d = t == null ? void 0 : t();
    i !== d && a(d);
  }, [t]), c.useEffect(() => {
    if (i) {
      const d = () => {
        u(!0);
      }, h = (p) => {
        p.preventDefault();
      }, v = (p) => {
        p.relatedTarget || u(!1);
      }, g = (p) => {
        u(!1), p.preventDefault();
      };
      return document.addEventListener("dragenter", d), document.addEventListener("dragover", h), document.addEventListener("dragleave", v), document.addEventListener("drop", g), () => {
        document.removeEventListener("dragenter", d), document.removeEventListener("dragover", h), document.removeEventListener("dragleave", v), document.removeEventListener("drop", g);
      };
    }
  }, [!!i]), !(t && i && !s))
    return null;
  const m = `${n}-drop-area`;
  return /* @__PURE__ */ yt(/* @__PURE__ */ c.createElement("div", {
    className: F(m, r, {
      [`${m}-on-body`]: i.tagName === "BODY"
    }),
    style: {
      display: l ? "block" : "none"
    }
  }, o), i);
}
function ne(e) {
  "@babel/helpers - typeof";
  return ne = typeof Symbol == "function" && typeof Symbol.iterator == "symbol" ? function(t) {
    return typeof t;
  } : function(t) {
    return t && typeof Symbol == "function" && t.constructor === Symbol && t !== Symbol.prototype ? "symbol" : typeof t;
  }, ne(e);
}
function Pi(e, t) {
  if (ne(e) != "object" || !e) return e;
  var r = e[Symbol.toPrimitive];
  if (r !== void 0) {
    var n = r.call(e, t);
    if (ne(n) != "object") return n;
    throw new TypeError("@@toPrimitive must return a primitive value.");
  }
  return (t === "string" ? String : Number)(e);
}
function Yn(e) {
  var t = Pi(e, "string");
  return ne(t) == "symbol" ? t : t + "";
}
function z(e, t, r) {
  return (t = Yn(t)) in e ? Object.defineProperty(e, t, {
    value: r,
    enumerable: !0,
    configurable: !0,
    writable: !0
  }) : e[t] = r, e;
}
function nn(e, t) {
  var r = Object.keys(e);
  if (Object.getOwnPropertySymbols) {
    var n = Object.getOwnPropertySymbols(e);
    t && (n = n.filter(function(o) {
      return Object.getOwnPropertyDescriptor(e, o).enumerable;
    })), r.push.apply(r, n);
  }
  return r;
}
function N(e) {
  for (var t = 1; t < arguments.length; t++) {
    var r = arguments[t] != null ? arguments[t] : {};
    t % 2 ? nn(Object(r), !0).forEach(function(n) {
      z(e, n, r[n]);
    }) : Object.getOwnPropertyDescriptors ? Object.defineProperties(e, Object.getOwnPropertyDescriptors(r)) : nn(Object(r)).forEach(function(n) {
      Object.defineProperty(e, n, Object.getOwnPropertyDescriptor(r, n));
    });
  }
  return e;
}
function Ri(e) {
  if (Array.isArray(e)) return e;
}
function Ii(e, t) {
  var r = e == null ? null : typeof Symbol < "u" && e[Symbol.iterator] || e["@@iterator"];
  if (r != null) {
    var n, o, s, i, a = [], l = !0, u = !1;
    try {
      if (s = (r = r.call(e)).next, t === 0) {
        if (Object(r) !== r) return;
        l = !1;
      } else for (; !(l = (n = s.call(r)).done) && (a.push(n.value), a.length !== t); l = !0) ;
    } catch (f) {
      u = !0, o = f;
    } finally {
      try {
        if (!l && r.return != null && (i = r.return(), Object(i) !== i)) return;
      } finally {
        if (u) throw o;
      }
    }
    return a;
  }
}
function on(e, t) {
  (t == null || t > e.length) && (t = e.length);
  for (var r = 0, n = Array(t); r < t; r++) n[r] = e[r];
  return n;
}
function Mi(e, t) {
  if (e) {
    if (typeof e == "string") return on(e, t);
    var r = {}.toString.call(e).slice(8, -1);
    return r === "Object" && e.constructor && (r = e.constructor.name), r === "Map" || r === "Set" ? Array.from(e) : r === "Arguments" || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r) ? on(e, t) : void 0;
  }
}
function Li() {
  throw new TypeError(`Invalid attempt to destructure non-iterable instance.
In order to be iterable, non-array objects must have a [Symbol.iterator]() method.`);
}
function de(e, t) {
  return Ri(e) || Ii(e, t) || Mi(e, t) || Li();
}
function sn(e) {
  return e instanceof HTMLElement || e instanceof SVGElement;
}
function Oi(e) {
  return e && Re(e) === "object" && sn(e.nativeElement) ? e.nativeElement : sn(e) ? e : null;
}
function ji(e) {
  var t = Oi(e);
  if (t)
    return t;
  if (e instanceof c.Component) {
    var r;
    return (r = Ar.findDOMNode) === null || r === void 0 ? void 0 : r.call(Ar, e);
  }
  return null;
}
function Ni(e, t) {
  if (e == null) return {};
  var r = {};
  for (var n in e) if ({}.hasOwnProperty.call(e, n)) {
    if (t.indexOf(n) !== -1) continue;
    r[n] = e[n];
  }
  return r;
}
function an(e, t) {
  if (e == null) return {};
  var r, n, o = Ni(e, t);
  if (Object.getOwnPropertySymbols) {
    var s = Object.getOwnPropertySymbols(e);
    for (n = 0; n < s.length; n++) r = s[n], t.indexOf(r) === -1 && {}.propertyIsEnumerable.call(e, r) && (o[r] = e[r]);
  }
  return o;
}
var Fi = /* @__PURE__ */ R.createContext({});
function Ke(e, t) {
  if (!(e instanceof t)) throw new TypeError("Cannot call a class as a function");
}
function ln(e, t) {
  for (var r = 0; r < t.length; r++) {
    var n = t[r];
    n.enumerable = n.enumerable || !1, n.configurable = !0, "value" in n && (n.writable = !0), Object.defineProperty(e, Yn(n.key), n);
  }
}
function qe(e, t, r) {
  return t && ln(e.prototype, t), r && ln(e, r), Object.defineProperty(e, "prototype", {
    writable: !1
  }), e;
}
function or(e, t) {
  return or = Object.setPrototypeOf ? Object.setPrototypeOf.bind() : function(r, n) {
    return r.__proto__ = n, r;
  }, or(e, t);
}
function kt(e, t) {
  if (typeof t != "function" && t !== null) throw new TypeError("Super expression must either be null or a function");
  e.prototype = Object.create(t && t.prototype, {
    constructor: {
      value: e,
      writable: !0,
      configurable: !0
    }
  }), Object.defineProperty(e, "prototype", {
    writable: !1
  }), t && or(e, t);
}
function St(e) {
  return St = Object.setPrototypeOf ? Object.getPrototypeOf.bind() : function(t) {
    return t.__proto__ || Object.getPrototypeOf(t);
  }, St(e);
}
function Qn() {
  try {
    var e = !Boolean.prototype.valueOf.call(Reflect.construct(Boolean, [], function() {
    }));
  } catch {
  }
  return (Qn = function() {
    return !!e;
  })();
}
function Oe(e) {
  if (e === void 0) throw new ReferenceError("this hasn't been initialised - super() hasn't been called");
  return e;
}
function ki(e, t) {
  if (t && (ne(t) == "object" || typeof t == "function")) return t;
  if (t !== void 0) throw new TypeError("Derived constructors may only return object or undefined");
  return Oe(e);
}
function At(e) {
  var t = Qn();
  return function() {
    var r, n = St(e);
    if (t) {
      var o = St(this).constructor;
      r = Reflect.construct(n, arguments, o);
    } else r = n.apply(this, arguments);
    return ki(this, r);
  };
}
var Ai = /* @__PURE__ */ function(e) {
  kt(r, e);
  var t = At(r);
  function r() {
    return Ke(this, r), t.apply(this, arguments);
  }
  return qe(r, [{
    key: "render",
    value: function() {
      return this.props.children;
    }
  }]), r;
}(R.Component);
function zi(e) {
  var t = R.useReducer(function(a) {
    return a + 1;
  }, 0), r = bt(t, 2), n = r[1], o = R.useRef(e), s = je(function() {
    return o.current;
  }), i = je(function(a) {
    o.current = typeof a == "function" ? a(o.current) : a, n();
  });
  return [s, i];
}
var Te = "none", it = "appear", at = "enter", lt = "leave", cn = "none", ge = "prepare", We = "start", Ve = "active", _r = "end", Zn = "prepared";
function un(e, t) {
  var r = {};
  return r[e.toLowerCase()] = t.toLowerCase(), r["Webkit".concat(e)] = "webkit".concat(t), r["Moz".concat(e)] = "moz".concat(t), r["ms".concat(e)] = "MS".concat(t), r["O".concat(e)] = "o".concat(t.toLowerCase()), r;
}
function Di(e, t) {
  var r = {
    animationend: un("Animation", "AnimationEnd"),
    transitionend: un("Transition", "TransitionEnd")
  };
  return e && ("AnimationEvent" in t || delete r.animationend.animation, "TransitionEvent" in t || delete r.transitionend.transition), r;
}
var Hi = Di(Tt(), typeof window < "u" ? window : {}), Jn = {};
if (Tt()) {
  var Bi = document.createElement("div");
  Jn = Bi.style;
}
var ct = {};
function eo(e) {
  if (ct[e])
    return ct[e];
  var t = Hi[e];
  if (t)
    for (var r = Object.keys(t), n = r.length, o = 0; o < n; o += 1) {
      var s = r[o];
      if (Object.prototype.hasOwnProperty.call(t, s) && s in Jn)
        return ct[e] = t[s], ct[e];
    }
  return "";
}
var to = eo("animationend"), ro = eo("transitionend"), no = !!(to && ro), fn = to || "animationend", dn = ro || "transitionend";
function mn(e, t) {
  if (!e) return null;
  if (ne(e) === "object") {
    var r = t.replace(/-\w/g, function(n) {
      return n[1].toUpperCase();
    });
    return e[r];
  }
  return "".concat(e, "-").concat(t);
}
const Wi = function(e) {
  var t = J();
  function r(o) {
    o && (o.removeEventListener(dn, e), o.removeEventListener(fn, e));
  }
  function n(o) {
    t.current && t.current !== o && r(t.current), o && o !== t.current && (o.addEventListener(dn, e), o.addEventListener(fn, e), t.current = o);
  }
  return R.useEffect(function() {
    return function() {
      r(t.current);
    };
  }, []), [n, r];
};
var oo = Tt() ? No : Ee, so = function(t) {
  return +setTimeout(t, 16);
}, io = function(t) {
  return clearTimeout(t);
};
typeof window < "u" && "requestAnimationFrame" in window && (so = function(t) {
  return window.requestAnimationFrame(t);
}, io = function(t) {
  return window.cancelAnimationFrame(t);
});
var pn = 0, Er = /* @__PURE__ */ new Map();
function ao(e) {
  Er.delete(e);
}
var sr = function(t) {
  var r = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : 1;
  pn += 1;
  var n = pn;
  function o(s) {
    if (s === 0)
      ao(n), t();
    else {
      var i = so(function() {
        o(s - 1);
      });
      Er.set(n, i);
    }
  }
  return o(r), n;
};
sr.cancel = function(e) {
  var t = Er.get(e);
  return ao(e), io(t);
};
const Vi = function() {
  var e = R.useRef(null);
  function t() {
    sr.cancel(e.current);
  }
  function r(n) {
    var o = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : 2;
    t();
    var s = sr(function() {
      o <= 1 ? n({
        isCanceled: function() {
          return s !== e.current;
        }
      }) : r(n, o - 1);
    });
    e.current = s;
  }
  return R.useEffect(function() {
    return function() {
      t();
    };
  }, []), [r, t];
};
var Xi = [ge, We, Ve, _r], Ui = [ge, Zn], lo = !1, Gi = !0;
function co(e) {
  return e === Ve || e === _r;
}
const Ki = function(e, t, r) {
  var n = et(cn), o = de(n, 2), s = o[0], i = o[1], a = Vi(), l = de(a, 2), u = l[0], f = l[1];
  function m() {
    i(ge, !0);
  }
  var d = t ? Ui : Xi;
  return oo(function() {
    if (s !== cn && s !== _r) {
      var h = d.indexOf(s), v = d[h + 1], g = r(s);
      g === lo ? i(v, !0) : v && u(function(p) {
        function y() {
          p.isCanceled() || i(v, !0);
        }
        g === !0 ? y() : Promise.resolve(g).then(y);
      });
    }
  }, [e, s]), R.useEffect(function() {
    return function() {
      f();
    };
  }, []), [m, s];
};
function qi(e, t, r, n) {
  var o = n.motionEnter, s = o === void 0 ? !0 : o, i = n.motionAppear, a = i === void 0 ? !0 : i, l = n.motionLeave, u = l === void 0 ? !0 : l, f = n.motionDeadline, m = n.motionLeaveImmediately, d = n.onAppearPrepare, h = n.onEnterPrepare, v = n.onLeavePrepare, g = n.onAppearStart, p = n.onEnterStart, y = n.onLeaveStart, T = n.onAppearActive, P = n.onEnterActive, _ = n.onLeaveActive, $ = n.onAppearEnd, b = n.onEnterEnd, I = n.onLeaveEnd, E = n.onVisibleChanged, O = et(), L = de(O, 2), j = L[0], M = L[1], x = zi(Te), w = de(x, 2), k = w[0], A = w[1], D = et(null), B = de(D, 2), oe = B[0], se = B[1], X = k(), W = J(!1), G = J(null);
  function U() {
    return r();
  }
  var q = J(!1);
  function ie() {
    A(Te), se(null, !0);
  }
  var ee = je(function(Z) {
    var Y = k();
    if (Y !== Te) {
      var ae = U();
      if (!(Z && !Z.deadline && Z.target !== ae)) {
        var Ie = q.current, Me;
        Y === it && Ie ? Me = $ == null ? void 0 : $(ae, Z) : Y === at && Ie ? Me = b == null ? void 0 : b(ae, Z) : Y === lt && Ie && (Me = I == null ? void 0 : I(ae, Z)), Ie && Me !== !1 && ie();
      }
    }
  }), xe = Wi(ee), ke = de(xe, 1), Ae = ke[0], ze = function(Y) {
    switch (Y) {
      case it:
        return z(z(z({}, ge, d), We, g), Ve, T);
      case at:
        return z(z(z({}, ge, h), We, p), Ve, P);
      case lt:
        return z(z(z({}, ge, v), We, y), Ve, _);
      default:
        return {};
    }
  }, we = R.useMemo(function() {
    return ze(X);
  }, [X]), De = Ki(X, !e, function(Z) {
    if (Z === ge) {
      var Y = we[ge];
      return Y ? Y(U()) : lo;
    }
    if (C in we) {
      var ae;
      se(((ae = we[C]) === null || ae === void 0 ? void 0 : ae.call(we, U(), null)) || null);
    }
    return C === Ve && X !== Te && (Ae(U()), f > 0 && (clearTimeout(G.current), G.current = setTimeout(function() {
      ee({
        deadline: !0
      });
    }, f))), C === Zn && ie(), Gi;
  }), st = de(De, 2), Vt = st[0], C = st[1], K = co(C);
  q.current = K;
  var V = J(null);
  oo(function() {
    if (!(W.current && V.current === t)) {
      M(t);
      var Z = W.current;
      W.current = !0;
      var Y;
      !Z && t && a && (Y = it), Z && t && s && (Y = at), (Z && !t && u || !Z && m && !t && u) && (Y = lt);
      var ae = ze(Y);
      Y && (e || ae[ge]) ? (A(Y), Vt()) : A(Te), V.current = t;
    }
  }, [t]), Ee(function() {
    // Cancel appear
    (X === it && !a || // Cancel enter
    X === at && !s || // Cancel leave
    X === lt && !u) && A(Te);
  }, [a, s, u]), Ee(function() {
    return function() {
      W.current = !1, clearTimeout(G.current);
    };
  }, []);
  var pe = R.useRef(!1);
  Ee(function() {
    j && (pe.current = !0), j !== void 0 && X === Te && ((pe.current || j) && (E == null || E(j)), pe.current = !0);
  }, [j, X]);
  var ue = oe;
  return we[ge] && C === We && (ue = N({
    transition: "none"
  }, ue)), [X, C, ue, j ?? t];
}
function Yi(e) {
  var t = e;
  ne(e) === "object" && (t = e.transitionSupport);
  function r(o, s) {
    return !!(o.motionName && t && s !== !1);
  }
  var n = /* @__PURE__ */ R.forwardRef(function(o, s) {
    var i = o.visible, a = i === void 0 ? !0 : i, l = o.removeOnLeave, u = l === void 0 ? !0 : l, f = o.forceRender, m = o.children, d = o.motionName, h = o.leavedClassName, v = o.eventProps, g = R.useContext(Fi), p = g.motion, y = r(o, p), T = J(), P = J();
    function _() {
      try {
        return T.current instanceof HTMLElement ? T.current : ji(P.current);
      } catch {
        return null;
      }
    }
    var $ = qi(y, a, _, o), b = de($, 4), I = b[0], E = b[1], O = b[2], L = b[3], j = R.useRef(L);
    L && (j.current = !0);
    var M = R.useCallback(function(B) {
      T.current = B, xi(s, B);
    }, [s]), x, w = N(N({}, v), {}, {
      visible: a
    });
    if (!m)
      x = null;
    else if (I === Te)
      L ? x = m(N({}, w), M) : !u && j.current && h ? x = m(N(N({}, w), {}, {
        className: h
      }), M) : f || !u && !h ? x = m(N(N({}, w), {}, {
        style: {
          display: "none"
        }
      }), M) : x = null;
    else {
      var k;
      E === ge ? k = "prepare" : co(E) ? k = "active" : E === We && (k = "start");
      var A = mn(d, "".concat(I, "-").concat(k));
      x = m(N(N({}, w), {}, {
        className: F(mn(d, I), z(z({}, A, A && k), d, typeof d == "string")),
        style: O
      }), M);
    }
    if (/* @__PURE__ */ R.isValidElement(x) && wi(x)) {
      var D = _i(x);
      D || (x = /* @__PURE__ */ R.cloneElement(x, {
        ref: M
      }));
    }
    return /* @__PURE__ */ R.createElement(Ai, {
      ref: P
    }, x);
  });
  return n.displayName = "CSSMotion", n;
}
const Qi = Yi(no);
var ir = "add", ar = "keep", lr = "remove", Yt = "removed";
function Zi(e) {
  var t;
  return e && ne(e) === "object" && "key" in e ? t = e : t = {
    key: e
  }, N(N({}, t), {}, {
    key: String(t.key)
  });
}
function cr() {
  var e = arguments.length > 0 && arguments[0] !== void 0 ? arguments[0] : [];
  return e.map(Zi);
}
function Ji() {
  var e = arguments.length > 0 && arguments[0] !== void 0 ? arguments[0] : [], t = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : [], r = [], n = 0, o = t.length, s = cr(e), i = cr(t);
  s.forEach(function(u) {
    for (var f = !1, m = n; m < o; m += 1) {
      var d = i[m];
      if (d.key === u.key) {
        n < m && (r = r.concat(i.slice(n, m).map(function(h) {
          return N(N({}, h), {}, {
            status: ir
          });
        })), n = m), r.push(N(N({}, d), {}, {
          status: ar
        })), n += 1, f = !0;
        break;
      }
    }
    f || r.push(N(N({}, u), {}, {
      status: lr
    }));
  }), n < o && (r = r.concat(i.slice(n).map(function(u) {
    return N(N({}, u), {}, {
      status: ir
    });
  })));
  var a = {};
  r.forEach(function(u) {
    var f = u.key;
    a[f] = (a[f] || 0) + 1;
  });
  var l = Object.keys(a).filter(function(u) {
    return a[u] > 1;
  });
  return l.forEach(function(u) {
    r = r.filter(function(f) {
      var m = f.key, d = f.status;
      return m !== u || d !== lr;
    }), r.forEach(function(f) {
      f.key === u && (f.status = ar);
    });
  }), r;
}
var ea = ["component", "children", "onVisibleChanged", "onAllRemoved"], ta = ["status"], ra = ["eventProps", "visible", "children", "motionName", "motionAppear", "motionEnter", "motionLeave", "motionLeaveImmediately", "motionDeadline", "removeOnLeave", "leavedClassName", "onAppearPrepare", "onAppearStart", "onAppearActive", "onAppearEnd", "onEnterStart", "onEnterActive", "onEnterEnd", "onLeaveStart", "onLeaveActive", "onLeaveEnd"];
function na(e) {
  var t = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : Qi, r = /* @__PURE__ */ function(n) {
    kt(s, n);
    var o = At(s);
    function s() {
      var i;
      Ke(this, s);
      for (var a = arguments.length, l = new Array(a), u = 0; u < a; u++)
        l[u] = arguments[u];
      return i = o.call.apply(o, [this].concat(l)), z(Oe(i), "state", {
        keyEntities: []
      }), z(Oe(i), "removeKey", function(f) {
        i.setState(function(m) {
          var d = m.keyEntities.map(function(h) {
            return h.key !== f ? h : N(N({}, h), {}, {
              status: Yt
            });
          });
          return {
            keyEntities: d
          };
        }, function() {
          var m = i.state.keyEntities, d = m.filter(function(h) {
            var v = h.status;
            return v !== Yt;
          }).length;
          d === 0 && i.props.onAllRemoved && i.props.onAllRemoved();
        });
      }), i;
    }
    return qe(s, [{
      key: "render",
      value: function() {
        var a = this, l = this.state.keyEntities, u = this.props, f = u.component, m = u.children, d = u.onVisibleChanged;
        u.onAllRemoved;
        var h = an(u, ea), v = f || R.Fragment, g = {};
        return ra.forEach(function(p) {
          g[p] = h[p], delete h[p];
        }), delete h.keys, /* @__PURE__ */ R.createElement(v, h, l.map(function(p, y) {
          var T = p.status, P = an(p, ta), _ = T === ir || T === ar;
          return /* @__PURE__ */ R.createElement(t, ve({}, g, {
            key: P.key,
            visible: _,
            eventProps: P,
            onVisibleChanged: function(b) {
              d == null || d(b, {
                key: P.key
              }), b || a.removeKey(P.key);
            }
          }), function($, b) {
            return m(N(N({}, $), {}, {
              index: y
            }), b);
          });
        }));
      }
    }], [{
      key: "getDerivedStateFromProps",
      value: function(a, l) {
        var u = a.keys, f = l.keyEntities, m = cr(u), d = Ji(f, m);
        return {
          keyEntities: d.filter(function(h) {
            var v = f.find(function(g) {
              var p = g.key;
              return h.key === p;
            });
            return !(v && v.status === Yt && h.status === lr);
          })
        };
      }
    }]), s;
  }(R.Component);
  return z(r, "defaultProps", {
    component: "div"
  }), r;
}
const oa = na(no);
function sa(e, t) {
  const {
    children: r,
    upload: n,
    rootClassName: o
  } = e, s = c.useRef(null);
  return c.useImperativeHandle(t, () => s.current), /* @__PURE__ */ c.createElement(kn, ve({}, n, {
    showUploadList: !1,
    rootClassName: o,
    ref: s
  }), r);
}
const uo = /* @__PURE__ */ c.forwardRef(sa);
var fo = /* @__PURE__ */ qe(function e() {
  Ke(this, e);
}), mo = "CALC_UNIT", ia = new RegExp(mo, "g");
function Qt(e) {
  return typeof e == "number" ? "".concat(e).concat(mo) : e;
}
var aa = /* @__PURE__ */ function(e) {
  kt(r, e);
  var t = At(r);
  function r(n, o) {
    var s;
    Ke(this, r), s = t.call(this), z(Oe(s), "result", ""), z(Oe(s), "unitlessCssVar", void 0), z(Oe(s), "lowPriority", void 0);
    var i = ne(n);
    return s.unitlessCssVar = o, n instanceof r ? s.result = "(".concat(n.result, ")") : i === "number" ? s.result = Qt(n) : i === "string" && (s.result = n), s;
  }
  return qe(r, [{
    key: "add",
    value: function(o) {
      return o instanceof r ? this.result = "".concat(this.result, " + ").concat(o.getResult()) : (typeof o == "number" || typeof o == "string") && (this.result = "".concat(this.result, " + ").concat(Qt(o))), this.lowPriority = !0, this;
    }
  }, {
    key: "sub",
    value: function(o) {
      return o instanceof r ? this.result = "".concat(this.result, " - ").concat(o.getResult()) : (typeof o == "number" || typeof o == "string") && (this.result = "".concat(this.result, " - ").concat(Qt(o))), this.lowPriority = !0, this;
    }
  }, {
    key: "mul",
    value: function(o) {
      return this.lowPriority && (this.result = "(".concat(this.result, ")")), o instanceof r ? this.result = "".concat(this.result, " * ").concat(o.getResult(!0)) : (typeof o == "number" || typeof o == "string") && (this.result = "".concat(this.result, " * ").concat(o)), this.lowPriority = !1, this;
    }
  }, {
    key: "div",
    value: function(o) {
      return this.lowPriority && (this.result = "(".concat(this.result, ")")), o instanceof r ? this.result = "".concat(this.result, " / ").concat(o.getResult(!0)) : (typeof o == "number" || typeof o == "string") && (this.result = "".concat(this.result, " / ").concat(o)), this.lowPriority = !1, this;
    }
  }, {
    key: "getResult",
    value: function(o) {
      return this.lowPriority || o ? "(".concat(this.result, ")") : this.result;
    }
  }, {
    key: "equal",
    value: function(o) {
      var s = this, i = o || {}, a = i.unit, l = !0;
      return typeof a == "boolean" ? l = a : Array.from(this.unitlessCssVar).some(function(u) {
        return s.result.includes(u);
      }) && (l = !1), this.result = this.result.replace(ia, l ? "px" : ""), typeof this.lowPriority < "u" ? "calc(".concat(this.result, ")") : this.result;
    }
  }]), r;
}(fo), la = /* @__PURE__ */ function(e) {
  kt(r, e);
  var t = At(r);
  function r(n) {
    var o;
    return Ke(this, r), o = t.call(this), z(Oe(o), "result", 0), n instanceof r ? o.result = n.result : typeof n == "number" && (o.result = n), o;
  }
  return qe(r, [{
    key: "add",
    value: function(o) {
      return o instanceof r ? this.result += o.result : typeof o == "number" && (this.result += o), this;
    }
  }, {
    key: "sub",
    value: function(o) {
      return o instanceof r ? this.result -= o.result : typeof o == "number" && (this.result -= o), this;
    }
  }, {
    key: "mul",
    value: function(o) {
      return o instanceof r ? this.result *= o.result : typeof o == "number" && (this.result *= o), this;
    }
  }, {
    key: "div",
    value: function(o) {
      return o instanceof r ? this.result /= o.result : typeof o == "number" && (this.result /= o), this;
    }
  }, {
    key: "equal",
    value: function() {
      return this.result;
    }
  }]), r;
}(fo), ca = function(t, r) {
  var n = t === "css" ? aa : la;
  return function(o) {
    return new n(o, r);
  };
}, gn = function(t, r) {
  return "".concat([r, t.replace(/([A-Z]+)([A-Z][a-z]+)/g, "$1-$2").replace(/([a-z])([A-Z])/g, "$1-$2")].filter(Boolean).join("-"));
};
function hn(e, t, r, n) {
  var o = N({}, t[e]);
  if (n != null && n.deprecatedTokens) {
    var s = n.deprecatedTokens;
    s.forEach(function(a) {
      var l = de(a, 2), u = l[0], f = l[1];
      if (o != null && o[u] || o != null && o[f]) {
        var m;
        (m = o[f]) !== null && m !== void 0 || (o[f] = o == null ? void 0 : o[u]);
      }
    });
  }
  var i = N(N({}, r), o);
  return Object.keys(i).forEach(function(a) {
    i[a] === t[a] && delete i[a];
  }), i;
}
var po = typeof CSSINJS_STATISTIC < "u", ur = !0;
function Ye() {
  for (var e = arguments.length, t = new Array(e), r = 0; r < e; r++)
    t[r] = arguments[r];
  if (!po)
    return Object.assign.apply(Object, [{}].concat(t));
  ur = !1;
  var n = {};
  return t.forEach(function(o) {
    if (ne(o) === "object") {
      var s = Object.keys(o);
      s.forEach(function(i) {
        Object.defineProperty(n, i, {
          configurable: !0,
          enumerable: !0,
          get: function() {
            return o[i];
          }
        });
      });
    }
  }), ur = !0, n;
}
var yn = {};
function ua() {
}
var fa = function(t) {
  var r, n = t, o = ua;
  return po && typeof Proxy < "u" && (r = /* @__PURE__ */ new Set(), n = new Proxy(t, {
    get: function(i, a) {
      if (ur) {
        var l;
        (l = r) === null || l === void 0 || l.add(a);
      }
      return i[a];
    }
  }), o = function(i, a) {
    var l;
    yn[i] = {
      global: Array.from(r),
      component: N(N({}, (l = yn[i]) === null || l === void 0 ? void 0 : l.component), a)
    };
  }), {
    token: n,
    keys: r,
    flush: o
  };
};
function vn(e, t, r) {
  if (typeof r == "function") {
    var n;
    return r(Ye(t, (n = t[e]) !== null && n !== void 0 ? n : {}));
  }
  return r ?? {};
}
function da(e) {
  return e === "js" ? {
    max: Math.max,
    min: Math.min
  } : {
    max: function() {
      for (var r = arguments.length, n = new Array(r), o = 0; o < r; o++)
        n[o] = arguments[o];
      return "max(".concat(n.map(function(s) {
        return Xe(s);
      }).join(","), ")");
    },
    min: function() {
      for (var r = arguments.length, n = new Array(r), o = 0; o < r; o++)
        n[o] = arguments[o];
      return "min(".concat(n.map(function(s) {
        return Xe(s);
      }).join(","), ")");
    }
  };
}
var ma = 1e3 * 60 * 10, pa = /* @__PURE__ */ function() {
  function e() {
    Ke(this, e), z(this, "map", /* @__PURE__ */ new Map()), z(this, "objectIDMap", /* @__PURE__ */ new WeakMap()), z(this, "nextID", 0), z(this, "lastAccessBeat", /* @__PURE__ */ new Map()), z(this, "accessBeat", 0);
  }
  return qe(e, [{
    key: "set",
    value: function(r, n) {
      this.clear();
      var o = this.getCompositeKey(r);
      this.map.set(o, n), this.lastAccessBeat.set(o, Date.now());
    }
  }, {
    key: "get",
    value: function(r) {
      var n = this.getCompositeKey(r), o = this.map.get(n);
      return this.lastAccessBeat.set(n, Date.now()), this.accessBeat += 1, o;
    }
  }, {
    key: "getCompositeKey",
    value: function(r) {
      var n = this, o = r.map(function(s) {
        return s && ne(s) === "object" ? "obj_".concat(n.getObjectID(s)) : "".concat(ne(s), "_").concat(s);
      });
      return o.join("|");
    }
  }, {
    key: "getObjectID",
    value: function(r) {
      if (this.objectIDMap.has(r))
        return this.objectIDMap.get(r);
      var n = this.nextID;
      return this.objectIDMap.set(r, n), this.nextID += 1, n;
    }
  }, {
    key: "clear",
    value: function() {
      var r = this;
      if (this.accessBeat > 1e4) {
        var n = Date.now();
        this.lastAccessBeat.forEach(function(o, s) {
          n - o > ma && (r.map.delete(s), r.lastAccessBeat.delete(s));
        }), this.accessBeat = 0;
      }
    }
  }]), e;
}(), bn = new pa();
function ga(e, t) {
  return c.useMemo(function() {
    var r = bn.get(t);
    if (r)
      return r;
    var n = e();
    return bn.set(t, n), n;
  }, t);
}
var ha = function() {
  return {};
};
function ya(e) {
  var t = e.useCSP, r = t === void 0 ? ha : t, n = e.useToken, o = e.usePrefix, s = e.getResetStyles, i = e.getCommonStyle, a = e.getCompUnitless;
  function l(d, h, v, g) {
    var p = Array.isArray(d) ? d[0] : d;
    function y(E) {
      return "".concat(String(p)).concat(E.slice(0, 1).toUpperCase()).concat(E.slice(1));
    }
    var T = (g == null ? void 0 : g.unitless) || {}, P = typeof a == "function" ? a(d) : {}, _ = N(N({}, P), {}, z({}, y("zIndexPopup"), !0));
    Object.keys(T).forEach(function(E) {
      _[y(E)] = T[E];
    });
    var $ = N(N({}, g), {}, {
      unitless: _,
      prefixToken: y
    }), b = f(d, h, v, $), I = u(p, v, $);
    return function(E) {
      var O = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : E, L = b(E, O), j = de(L, 2), M = j[1], x = I(O), w = de(x, 2), k = w[0], A = w[1];
      return [k, M, A];
    };
  }
  function u(d, h, v) {
    var g = v.unitless, p = v.injectStyle, y = p === void 0 ? !0 : p, T = v.prefixToken, P = v.ignore, _ = function(I) {
      var E = I.rootCls, O = I.cssVar, L = O === void 0 ? {} : O, j = n(), M = j.realToken;
      return vs({
        path: [d],
        prefix: L.prefix,
        key: L.key,
        unitless: g,
        ignore: P,
        token: M,
        scope: E
      }, function() {
        var x = vn(d, M, h), w = hn(d, M, x, {
          deprecatedTokens: v == null ? void 0 : v.deprecatedTokens
        });
        return Object.keys(x).forEach(function(k) {
          w[T(k)] = w[k], delete w[k];
        }), w;
      }), null;
    }, $ = function(I) {
      var E = n(), O = E.cssVar;
      return [function(L) {
        return y && O ? /* @__PURE__ */ c.createElement(c.Fragment, null, /* @__PURE__ */ c.createElement(_, {
          rootCls: I,
          cssVar: O,
          component: d
        }), L) : L;
      }, O == null ? void 0 : O.key];
    };
    return $;
  }
  function f(d, h, v) {
    var g = arguments.length > 3 && arguments[3] !== void 0 ? arguments[3] : {}, p = Array.isArray(d) ? d : [d, d], y = de(p, 1), T = y[0], P = p.join("-"), _ = e.layer || {
      name: "antd"
    };
    return function($) {
      var b = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : $, I = n(), E = I.theme, O = I.realToken, L = I.hashId, j = I.token, M = I.cssVar, x = o(), w = x.rootPrefixCls, k = x.iconPrefixCls, A = r(), D = M ? "css" : "js", B = ga(function() {
        var U = /* @__PURE__ */ new Set();
        return M && Object.keys(g.unitless || {}).forEach(function(q) {
          U.add(Xt(q, M.prefix)), U.add(Xt(q, gn(T, M.prefix)));
        }), ca(D, U);
      }, [D, T, M == null ? void 0 : M.prefix]), oe = da(D), se = oe.max, X = oe.min, W = {
        theme: E,
        token: j,
        hashId: L,
        nonce: function() {
          return A.nonce;
        },
        clientOnly: g.clientOnly,
        layer: _,
        // antd is always at top of styles
        order: g.order || -999
      };
      typeof s == "function" && Hr(N(N({}, W), {}, {
        clientOnly: !1,
        path: ["Shared", w]
      }), function() {
        return s(j, {
          prefix: {
            rootPrefixCls: w,
            iconPrefixCls: k
          },
          csp: A
        });
      });
      var G = Hr(N(N({}, W), {}, {
        path: [P, $, k]
      }), function() {
        if (g.injectStyle === !1)
          return [];
        var U = fa(j), q = U.token, ie = U.flush, ee = vn(T, O, v), xe = ".".concat($), ke = hn(T, O, ee, {
          deprecatedTokens: g.deprecatedTokens
        });
        M && ee && ne(ee) === "object" && Object.keys(ee).forEach(function(De) {
          ee[De] = "var(".concat(Xt(De, gn(T, M.prefix)), ")");
        });
        var Ae = Ye(q, {
          componentCls: xe,
          prefixCls: $,
          iconCls: ".".concat(k),
          antCls: ".".concat(w),
          calc: B,
          // @ts-ignore
          max: se,
          // @ts-ignore
          min: X
        }, M ? ee : ke), ze = h(Ae, {
          hashId: L,
          prefixCls: $,
          rootPrefixCls: w,
          iconPrefixCls: k
        });
        ie(T, ke);
        var we = typeof i == "function" ? i(Ae, $, b, g.resetFont) : null;
        return [g.resetStyle === !1 ? null : we, ze];
      });
      return [G, L];
    };
  }
  function m(d, h, v) {
    var g = arguments.length > 3 && arguments[3] !== void 0 ? arguments[3] : {}, p = f(d, h, v, N({
      resetStyle: !1,
      // Sub Style should default after root one
      order: -998
    }, g)), y = function(P) {
      var _ = P.prefixCls, $ = P.rootCls, b = $ === void 0 ? _ : $;
      return p(_, b), null;
    };
    return y;
  }
  return {
    genStyleHooks: l,
    genSubStyleComponent: m,
    genComponentStyleHook: f
  };
}
const Q = Math.round;
function Zt(e, t) {
  const r = e.replace(/^[^(]*\((.*)/, "$1").replace(/\).*/, "").match(/\d*\.?\d+%?/g) || [], n = r.map((o) => parseFloat(o));
  for (let o = 0; o < 3; o += 1)
    n[o] = t(n[o] || 0, r[o] || "", o);
  return r[3] ? n[3] = r[3].includes("%") ? n[3] / 100 : n[3] : n[3] = 1, n;
}
const Sn = (e, t, r) => r === 0 ? e : e / 100;
function Qe(e, t) {
  const r = t || 255;
  return e > r ? r : e < 0 ? 0 : e;
}
class Se {
  constructor(t) {
    z(this, "isValid", !0), z(this, "r", 0), z(this, "g", 0), z(this, "b", 0), z(this, "a", 1), z(this, "_h", void 0), z(this, "_s", void 0), z(this, "_l", void 0), z(this, "_v", void 0), z(this, "_max", void 0), z(this, "_min", void 0), z(this, "_brightness", void 0);
    function r(n) {
      return n[0] in t && n[1] in t && n[2] in t;
    }
    if (t) if (typeof t == "string") {
      let o = function(s) {
        return n.startsWith(s);
      };
      const n = t.trim();
      /^#?[A-F\d]{3,8}$/i.test(n) ? this.fromHexString(n) : o("rgb") ? this.fromRgbString(n) : o("hsl") ? this.fromHslString(n) : (o("hsv") || o("hsb")) && this.fromHsvString(n);
    } else if (t instanceof Se)
      this.r = t.r, this.g = t.g, this.b = t.b, this.a = t.a, this._h = t._h, this._s = t._s, this._l = t._l, this._v = t._v;
    else if (r("rgb"))
      this.r = Qe(t.r), this.g = Qe(t.g), this.b = Qe(t.b), this.a = typeof t.a == "number" ? Qe(t.a, 1) : 1;
    else if (r("hsl"))
      this.fromHsl(t);
    else if (r("hsv"))
      this.fromHsv(t);
    else
      throw new Error("@ant-design/fast-color: unsupported input " + JSON.stringify(t));
  }
  // ======================= Setter =======================
  setR(t) {
    return this._sc("r", t);
  }
  setG(t) {
    return this._sc("g", t);
  }
  setB(t) {
    return this._sc("b", t);
  }
  setA(t) {
    return this._sc("a", t, 1);
  }
  setHue(t) {
    const r = this.toHsv();
    return r.h = t, this._c(r);
  }
  // ======================= Getter =======================
  /**
   * Returns the perceived luminance of a color, from 0-1.
   * @see http://www.w3.org/TR/2008/REC-WCAG20-20081211/#relativeluminancedef
   */
  getLuminance() {
    function t(s) {
      const i = s / 255;
      return i <= 0.03928 ? i / 12.92 : Math.pow((i + 0.055) / 1.055, 2.4);
    }
    const r = t(this.r), n = t(this.g), o = t(this.b);
    return 0.2126 * r + 0.7152 * n + 0.0722 * o;
  }
  getHue() {
    if (typeof this._h > "u") {
      const t = this.getMax() - this.getMin();
      t === 0 ? this._h = 0 : this._h = Q(60 * (this.r === this.getMax() ? (this.g - this.b) / t + (this.g < this.b ? 6 : 0) : this.g === this.getMax() ? (this.b - this.r) / t + 2 : (this.r - this.g) / t + 4));
    }
    return this._h;
  }
  getSaturation() {
    if (typeof this._s > "u") {
      const t = this.getMax() - this.getMin();
      t === 0 ? this._s = 0 : this._s = t / this.getMax();
    }
    return this._s;
  }
  getLightness() {
    return typeof this._l > "u" && (this._l = (this.getMax() + this.getMin()) / 510), this._l;
  }
  getValue() {
    return typeof this._v > "u" && (this._v = this.getMax() / 255), this._v;
  }
  /**
   * Returns the perceived brightness of the color, from 0-255.
   * Note: this is not the b of HSB
   * @see http://www.w3.org/TR/AERT#color-contrast
   */
  getBrightness() {
    return typeof this._brightness > "u" && (this._brightness = (this.r * 299 + this.g * 587 + this.b * 114) / 1e3), this._brightness;
  }
  // ======================== Func ========================
  darken(t = 10) {
    const r = this.getHue(), n = this.getSaturation();
    let o = this.getLightness() - t / 100;
    return o < 0 && (o = 0), this._c({
      h: r,
      s: n,
      l: o,
      a: this.a
    });
  }
  lighten(t = 10) {
    const r = this.getHue(), n = this.getSaturation();
    let o = this.getLightness() + t / 100;
    return o > 1 && (o = 1), this._c({
      h: r,
      s: n,
      l: o,
      a: this.a
    });
  }
  /**
   * Mix the current color a given amount with another color, from 0 to 100.
   * 0 means no mixing (return current color).
   */
  mix(t, r = 50) {
    const n = this._c(t), o = r / 100, s = (a) => (n[a] - this[a]) * o + this[a], i = {
      r: Q(s("r")),
      g: Q(s("g")),
      b: Q(s("b")),
      a: Q(s("a") * 100) / 100
    };
    return this._c(i);
  }
  /**
   * Mix the color with pure white, from 0 to 100.
   * Providing 0 will do nothing, providing 100 will always return white.
   */
  tint(t = 10) {
    return this.mix({
      r: 255,
      g: 255,
      b: 255,
      a: 1
    }, t);
  }
  /**
   * Mix the color with pure black, from 0 to 100.
   * Providing 0 will do nothing, providing 100 will always return black.
   */
  shade(t = 10) {
    return this.mix({
      r: 0,
      g: 0,
      b: 0,
      a: 1
    }, t);
  }
  onBackground(t) {
    const r = this._c(t), n = this.a + r.a * (1 - this.a), o = (s) => Q((this[s] * this.a + r[s] * r.a * (1 - this.a)) / n);
    return this._c({
      r: o("r"),
      g: o("g"),
      b: o("b"),
      a: n
    });
  }
  // ======================= Status =======================
  isDark() {
    return this.getBrightness() < 128;
  }
  isLight() {
    return this.getBrightness() >= 128;
  }
  // ======================== MISC ========================
  equals(t) {
    return this.r === t.r && this.g === t.g && this.b === t.b && this.a === t.a;
  }
  clone() {
    return this._c(this);
  }
  // ======================= Format =======================
  toHexString() {
    let t = "#";
    const r = (this.r || 0).toString(16);
    t += r.length === 2 ? r : "0" + r;
    const n = (this.g || 0).toString(16);
    t += n.length === 2 ? n : "0" + n;
    const o = (this.b || 0).toString(16);
    if (t += o.length === 2 ? o : "0" + o, typeof this.a == "number" && this.a >= 0 && this.a < 1) {
      const s = Q(this.a * 255).toString(16);
      t += s.length === 2 ? s : "0" + s;
    }
    return t;
  }
  /** CSS support color pattern */
  toHsl() {
    return {
      h: this.getHue(),
      s: this.getSaturation(),
      l: this.getLightness(),
      a: this.a
    };
  }
  /** CSS support color pattern */
  toHslString() {
    const t = this.getHue(), r = Q(this.getSaturation() * 100), n = Q(this.getLightness() * 100);
    return this.a !== 1 ? `hsla(${t},${r}%,${n}%,${this.a})` : `hsl(${t},${r}%,${n}%)`;
  }
  /** Same as toHsb */
  toHsv() {
    return {
      h: this.getHue(),
      s: this.getSaturation(),
      v: this.getValue(),
      a: this.a
    };
  }
  toRgb() {
    return {
      r: this.r,
      g: this.g,
      b: this.b,
      a: this.a
    };
  }
  toRgbString() {
    return this.a !== 1 ? `rgba(${this.r},${this.g},${this.b},${this.a})` : `rgb(${this.r},${this.g},${this.b})`;
  }
  toString() {
    return this.toRgbString();
  }
  // ====================== Privates ======================
  /** Return a new FastColor object with one channel changed */
  _sc(t, r, n) {
    const o = this.clone();
    return o[t] = Qe(r, n), o;
  }
  _c(t) {
    return new this.constructor(t);
  }
  getMax() {
    return typeof this._max > "u" && (this._max = Math.max(this.r, this.g, this.b)), this._max;
  }
  getMin() {
    return typeof this._min > "u" && (this._min = Math.min(this.r, this.g, this.b)), this._min;
  }
  fromHexString(t) {
    const r = t.replace("#", "");
    function n(o, s) {
      return parseInt(r[o] + r[s || o], 16);
    }
    r.length < 6 ? (this.r = n(0), this.g = n(1), this.b = n(2), this.a = r[3] ? n(3) / 255 : 1) : (this.r = n(0, 1), this.g = n(2, 3), this.b = n(4, 5), this.a = r[6] ? n(6, 7) / 255 : 1);
  }
  fromHsl({
    h: t,
    s: r,
    l: n,
    a: o
  }) {
    if (this._h = t % 360, this._s = r, this._l = n, this.a = typeof o == "number" ? o : 1, r <= 0) {
      const d = Q(n * 255);
      this.r = d, this.g = d, this.b = d;
    }
    let s = 0, i = 0, a = 0;
    const l = t / 60, u = (1 - Math.abs(2 * n - 1)) * r, f = u * (1 - Math.abs(l % 2 - 1));
    l >= 0 && l < 1 ? (s = u, i = f) : l >= 1 && l < 2 ? (s = f, i = u) : l >= 2 && l < 3 ? (i = u, a = f) : l >= 3 && l < 4 ? (i = f, a = u) : l >= 4 && l < 5 ? (s = f, a = u) : l >= 5 && l < 6 && (s = u, a = f);
    const m = n - u / 2;
    this.r = Q((s + m) * 255), this.g = Q((i + m) * 255), this.b = Q((a + m) * 255);
  }
  fromHsv({
    h: t,
    s: r,
    v: n,
    a: o
  }) {
    this._h = t % 360, this._s = r, this._v = n, this.a = typeof o == "number" ? o : 1;
    const s = Q(n * 255);
    if (this.r = s, this.g = s, this.b = s, r <= 0)
      return;
    const i = t / 60, a = Math.floor(i), l = i - a, u = Q(n * (1 - r) * 255), f = Q(n * (1 - r * l) * 255), m = Q(n * (1 - r * (1 - l)) * 255);
    switch (a) {
      case 0:
        this.g = m, this.b = u;
        break;
      case 1:
        this.r = f, this.b = u;
        break;
      case 2:
        this.r = u, this.b = m;
        break;
      case 3:
        this.r = u, this.g = f;
        break;
      case 4:
        this.r = m, this.g = u;
        break;
      case 5:
      default:
        this.g = u, this.b = f;
        break;
    }
  }
  fromHsvString(t) {
    const r = Zt(t, Sn);
    this.fromHsv({
      h: r[0],
      s: r[1],
      v: r[2],
      a: r[3]
    });
  }
  fromHslString(t) {
    const r = Zt(t, Sn);
    this.fromHsl({
      h: r[0],
      s: r[1],
      l: r[2],
      a: r[3]
    });
  }
  fromRgbString(t) {
    const r = Zt(t, (n, o) => (
      // Convert percentage to number. e.g. 50% -> 128
      o.includes("%") ? Q(n / 100 * 255) : n
    ));
    this.r = r[0], this.g = r[1], this.b = r[2], this.a = r[3];
  }
}
const va = {
  blue: "#1677FF",
  purple: "#722ED1",
  cyan: "#13C2C2",
  green: "#52C41A",
  magenta: "#EB2F96",
  /**
   * @deprecated Use magenta instead
   */
  pink: "#EB2F96",
  red: "#F5222D",
  orange: "#FA8C16",
  yellow: "#FADB14",
  volcano: "#FA541C",
  geekblue: "#2F54EB",
  gold: "#FAAD14",
  lime: "#A0D911"
}, ba = Object.assign(Object.assign({}, va), {
  // Color
  colorPrimary: "#1677ff",
  colorSuccess: "#52c41a",
  colorWarning: "#faad14",
  colorError: "#ff4d4f",
  colorInfo: "#1677ff",
  colorLink: "",
  colorTextBase: "",
  colorBgBase: "",
  // Font
  fontFamily: `-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial,
'Noto Sans', sans-serif, 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol',
'Noto Color Emoji'`,
  fontFamilyCode: "'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, Courier, monospace",
  fontSize: 14,
  // Line
  lineWidth: 1,
  lineType: "solid",
  // Motion
  motionUnit: 0.1,
  motionBase: 0,
  motionEaseOutCirc: "cubic-bezier(0.08, 0.82, 0.17, 1)",
  motionEaseInOutCirc: "cubic-bezier(0.78, 0.14, 0.15, 0.86)",
  motionEaseOut: "cubic-bezier(0.215, 0.61, 0.355, 1)",
  motionEaseInOut: "cubic-bezier(0.645, 0.045, 0.355, 1)",
  motionEaseOutBack: "cubic-bezier(0.12, 0.4, 0.29, 1.46)",
  motionEaseInBack: "cubic-bezier(0.71, -0.46, 0.88, 0.6)",
  motionEaseInQuint: "cubic-bezier(0.755, 0.05, 0.855, 0.06)",
  motionEaseOutQuint: "cubic-bezier(0.23, 1, 0.32, 1)",
  // Radius
  borderRadius: 6,
  // Size
  sizeUnit: 4,
  sizeStep: 4,
  sizePopupArrow: 16,
  // Control Base
  controlHeight: 32,
  // zIndex
  zIndexBase: 0,
  zIndexPopupBase: 1e3,
  // Image
  opacityImage: 1,
  // Wireframe
  wireframe: !1,
  // Motion
  motion: !0
});
function Jt(e) {
  return e >= 0 && e <= 255;
}
function ut(e, t) {
  const {
    r,
    g: n,
    b: o,
    a: s
  } = new Se(e).toRgb();
  if (s < 1)
    return e;
  const {
    r: i,
    g: a,
    b: l
  } = new Se(t).toRgb();
  for (let u = 0.01; u <= 1; u += 0.01) {
    const f = Math.round((r - i * (1 - u)) / u), m = Math.round((n - a * (1 - u)) / u), d = Math.round((o - l * (1 - u)) / u);
    if (Jt(f) && Jt(m) && Jt(d))
      return new Se({
        r: f,
        g: m,
        b: d,
        a: Math.round(u * 100) / 100
      }).toRgbString();
  }
  return new Se({
    r,
    g: n,
    b: o,
    a: 1
  }).toRgbString();
}
var Sa = function(e, t) {
  var r = {};
  for (var n in e) Object.prototype.hasOwnProperty.call(e, n) && t.indexOf(n) < 0 && (r[n] = e[n]);
  if (e != null && typeof Object.getOwnPropertySymbols == "function") for (var o = 0, n = Object.getOwnPropertySymbols(e); o < n.length; o++)
    t.indexOf(n[o]) < 0 && Object.prototype.propertyIsEnumerable.call(e, n[o]) && (r[n[o]] = e[n[o]]);
  return r;
};
function xa(e) {
  const {
    override: t
  } = e, r = Sa(e, ["override"]), n = Object.assign({}, t);
  Object.keys(ba).forEach((d) => {
    delete n[d];
  });
  const o = Object.assign(Object.assign({}, r), n), s = 480, i = 576, a = 768, l = 992, u = 1200, f = 1600;
  if (o.motion === !1) {
    const d = "0s";
    o.motionDurationFast = d, o.motionDurationMid = d, o.motionDurationSlow = d;
  }
  return Object.assign(Object.assign(Object.assign({}, o), {
    // ============== Background ============== //
    colorFillContent: o.colorFillSecondary,
    colorFillContentHover: o.colorFill,
    colorFillAlter: o.colorFillQuaternary,
    colorBgContainerDisabled: o.colorFillTertiary,
    // ============== Split ============== //
    colorBorderBg: o.colorBgContainer,
    colorSplit: ut(o.colorBorderSecondary, o.colorBgContainer),
    // ============== Text ============== //
    colorTextPlaceholder: o.colorTextQuaternary,
    colorTextDisabled: o.colorTextQuaternary,
    colorTextHeading: o.colorText,
    colorTextLabel: o.colorTextSecondary,
    colorTextDescription: o.colorTextTertiary,
    colorTextLightSolid: o.colorWhite,
    colorHighlight: o.colorError,
    colorBgTextHover: o.colorFillSecondary,
    colorBgTextActive: o.colorFill,
    colorIcon: o.colorTextTertiary,
    colorIconHover: o.colorText,
    colorErrorOutline: ut(o.colorErrorBg, o.colorBgContainer),
    colorWarningOutline: ut(o.colorWarningBg, o.colorBgContainer),
    // Font
    fontSizeIcon: o.fontSizeSM,
    // Line
    lineWidthFocus: o.lineWidth * 3,
    // Control
    lineWidth: o.lineWidth,
    controlOutlineWidth: o.lineWidth * 2,
    // Checkbox size and expand icon size
    controlInteractiveSize: o.controlHeight / 2,
    controlItemBgHover: o.colorFillTertiary,
    controlItemBgActive: o.colorPrimaryBg,
    controlItemBgActiveHover: o.colorPrimaryBgHover,
    controlItemBgActiveDisabled: o.colorFill,
    controlTmpOutline: o.colorFillQuaternary,
    controlOutline: ut(o.colorPrimaryBg, o.colorBgContainer),
    lineType: o.lineType,
    borderRadius: o.borderRadius,
    borderRadiusXS: o.borderRadiusXS,
    borderRadiusSM: o.borderRadiusSM,
    borderRadiusLG: o.borderRadiusLG,
    fontWeightStrong: 600,
    opacityLoading: 0.65,
    linkDecoration: "none",
    linkHoverDecoration: "none",
    linkFocusDecoration: "none",
    controlPaddingHorizontal: 12,
    controlPaddingHorizontalSM: 8,
    paddingXXS: o.sizeXXS,
    paddingXS: o.sizeXS,
    paddingSM: o.sizeSM,
    padding: o.size,
    paddingMD: o.sizeMD,
    paddingLG: o.sizeLG,
    paddingXL: o.sizeXL,
    paddingContentHorizontalLG: o.sizeLG,
    paddingContentVerticalLG: o.sizeMS,
    paddingContentHorizontal: o.sizeMS,
    paddingContentVertical: o.sizeSM,
    paddingContentHorizontalSM: o.size,
    paddingContentVerticalSM: o.sizeXS,
    marginXXS: o.sizeXXS,
    marginXS: o.sizeXS,
    marginSM: o.sizeSM,
    margin: o.size,
    marginMD: o.sizeMD,
    marginLG: o.sizeLG,
    marginXL: o.sizeXL,
    marginXXL: o.sizeXXL,
    boxShadow: `
      0 6px 16px 0 rgba(0, 0, 0, 0.08),
      0 3px 6px -4px rgba(0, 0, 0, 0.12),
      0 9px 28px 8px rgba(0, 0, 0, 0.05)
    `,
    boxShadowSecondary: `
      0 6px 16px 0 rgba(0, 0, 0, 0.08),
      0 3px 6px -4px rgba(0, 0, 0, 0.12),
      0 9px 28px 8px rgba(0, 0, 0, 0.05)
    `,
    boxShadowTertiary: `
      0 1px 2px 0 rgba(0, 0, 0, 0.03),
      0 1px 6px -1px rgba(0, 0, 0, 0.02),
      0 2px 4px 0 rgba(0, 0, 0, 0.02)
    `,
    screenXS: s,
    screenXSMin: s,
    screenXSMax: i - 1,
    screenSM: i,
    screenSMMin: i,
    screenSMMax: a - 1,
    screenMD: a,
    screenMDMin: a,
    screenMDMax: l - 1,
    screenLG: l,
    screenLGMin: l,
    screenLGMax: u - 1,
    screenXL: u,
    screenXLMin: u,
    screenXLMax: f - 1,
    screenXXL: f,
    screenXXLMin: f,
    boxShadowPopoverArrow: "2px 2px 5px rgba(0, 0, 0, 0.05)",
    boxShadowCard: `
      0 1px 2px -2px ${new Se("rgba(0, 0, 0, 0.16)").toRgbString()},
      0 3px 6px 0 ${new Se("rgba(0, 0, 0, 0.12)").toRgbString()},
      0 5px 12px 4px ${new Se("rgba(0, 0, 0, 0.09)").toRgbString()}
    `,
    boxShadowDrawerRight: `
      -6px 0 16px 0 rgba(0, 0, 0, 0.08),
      -3px 0 6px -4px rgba(0, 0, 0, 0.12),
      -9px 0 28px 8px rgba(0, 0, 0, 0.05)
    `,
    boxShadowDrawerLeft: `
      6px 0 16px 0 rgba(0, 0, 0, 0.08),
      3px 0 6px -4px rgba(0, 0, 0, 0.12),
      9px 0 28px 8px rgba(0, 0, 0, 0.05)
    `,
    boxShadowDrawerUp: `
      0 6px 16px 0 rgba(0, 0, 0, 0.08),
      0 3px 6px -4px rgba(0, 0, 0, 0.12),
      0 9px 28px 8px rgba(0, 0, 0, 0.05)
    `,
    boxShadowDrawerDown: `
      0 -6px 16px 0 rgba(0, 0, 0, 0.08),
      0 -3px 6px -4px rgba(0, 0, 0, 0.12),
      0 -9px 28px 8px rgba(0, 0, 0, 0.05)
    `,
    boxShadowTabsOverflowLeft: "inset 10px 0 8px -8px rgba(0, 0, 0, 0.08)",
    boxShadowTabsOverflowRight: "inset -10px 0 8px -8px rgba(0, 0, 0, 0.08)",
    boxShadowTabsOverflowTop: "inset 0 10px 8px -8px rgba(0, 0, 0, 0.08)",
    boxShadowTabsOverflowBottom: "inset 0 -10px 8px -8px rgba(0, 0, 0, 0.08)"
  }), n);
}
const wa = {
  lineHeight: !0,
  lineHeightSM: !0,
  lineHeightLG: !0,
  lineHeightHeading1: !0,
  lineHeightHeading2: !0,
  lineHeightHeading3: !0,
  lineHeightHeading4: !0,
  lineHeightHeading5: !0,
  opacityLoading: !0,
  fontWeightStrong: !0,
  zIndexPopupBase: !0,
  zIndexBase: !0,
  opacityImage: !0
}, _a = {
  size: !0,
  sizeSM: !0,
  sizeLG: !0,
  sizeMD: !0,
  sizeXS: !0,
  sizeXXS: !0,
  sizeMS: !0,
  sizeXL: !0,
  sizeXXL: !0,
  sizeUnit: !0,
  sizeStep: !0,
  motionBase: !0,
  motionUnit: !0
}, Ea = bs(Je.defaultAlgorithm), Ca = {
  screenXS: !0,
  screenXSMin: !0,
  screenXSMax: !0,
  screenSM: !0,
  screenSMMin: !0,
  screenSMMax: !0,
  screenMD: !0,
  screenMDMin: !0,
  screenMDMax: !0,
  screenLG: !0,
  screenLGMin: !0,
  screenLGMax: !0,
  screenXL: !0,
  screenXLMin: !0,
  screenXLMax: !0,
  screenXXL: !0,
  screenXXLMin: !0
}, go = (e, t, r) => {
  const n = r.getDerivativeToken(e), {
    override: o,
    ...s
  } = t;
  let i = {
    ...n,
    override: o
  };
  return i = xa(i), s && Object.entries(s).forEach(([a, l]) => {
    const {
      theme: u,
      ...f
    } = l;
    let m = f;
    u && (m = go({
      ...i,
      ...f
    }, {
      override: f
    }, u)), i[a] = m;
  }), i;
};
function Ta() {
  const {
    token: e,
    hashed: t,
    theme: r = Ea,
    override: n,
    cssVar: o
  } = c.useContext(Je._internalContext), [s, i, a] = Ss(r, [Je.defaultSeed, e], {
    salt: `${ii}-${t || ""}`,
    override: n,
    getComputedToken: go,
    cssVar: o && {
      prefix: o.prefix,
      key: o.key,
      unitless: wa,
      ignore: _a,
      preserve: Ca
    }
  });
  return [r, a, t ? i : "", s, o];
}
const {
  genStyleHooks: zt
} = ya({
  usePrefix: () => {
    const {
      getPrefixCls: e,
      iconPrefixCls: t
    } = Pe();
    return {
      iconPrefixCls: t,
      rootPrefixCls: e()
    };
  },
  useToken: () => {
    const [e, t, r, n, o] = Ta();
    return {
      theme: e,
      realToken: t,
      hashId: r,
      token: n,
      cssVar: o
    };
  },
  useCSP: () => {
    const {
      csp: e
    } = Pe();
    return e ?? {};
  },
  layer: {
    name: "antdx",
    dependencies: ["antd"]
  }
}), $a = (e) => {
  const {
    componentCls: t,
    antCls: r,
    calc: n
  } = e, o = `${t}-list-card`, s = n(e.fontSize).mul(e.lineHeight).mul(2).add(e.paddingSM).add(e.paddingSM).equal();
  return {
    [o]: {
      borderRadius: e.borderRadius,
      position: "relative",
      background: e.colorFillContent,
      borderWidth: e.lineWidth,
      borderStyle: "solid",
      borderColor: "transparent",
      flex: "none",
      // =============================== Desc ================================
      [`${o}-name,${o}-desc`]: {
        display: "flex",
        flexWrap: "nowrap",
        maxWidth: "100%"
      },
      [`${o}-ellipsis-prefix`]: {
        flex: "0 1 auto",
        minWidth: 0,
        overflow: "hidden",
        textOverflow: "ellipsis",
        whiteSpace: "nowrap"
      },
      [`${o}-ellipsis-suffix`]: {
        flex: "none"
      },
      // ============================= Overview ==============================
      "&-type-overview": {
        padding: n(e.paddingSM).sub(e.lineWidth).equal(),
        paddingInlineStart: n(e.padding).add(e.lineWidth).equal(),
        display: "flex",
        flexWrap: "nowrap",
        gap: e.paddingXS,
        alignItems: "flex-start",
        width: 236,
        // Icon
        [`${o}-icon`]: {
          fontSize: n(e.fontSizeLG).mul(2).equal(),
          lineHeight: 1,
          paddingTop: n(e.paddingXXS).mul(1.5).equal(),
          flex: "none"
        },
        // Content
        [`${o}-content`]: {
          flex: "auto",
          minWidth: 0,
          display: "flex",
          flexDirection: "column",
          alignItems: "stretch"
        },
        [`${o}-desc`]: {
          color: e.colorTextTertiary
        }
      },
      // ============================== Preview ==============================
      "&-type-preview": {
        width: s,
        height: s,
        lineHeight: 1,
        display: "flex",
        alignItems: "center",
        [`&:not(${o}-status-error)`]: {
          border: 0
        },
        // Img
        [`${r}-image`]: {
          width: "100%",
          height: "100%",
          borderRadius: "inherit",
          img: {
            height: "100%",
            objectFit: "cover",
            borderRadius: "inherit"
          }
        },
        // Mask
        [`${o}-img-mask`]: {
          position: "absolute",
          inset: 0,
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          background: `rgba(0, 0, 0, ${e.opacityLoading})`,
          borderRadius: "inherit"
        },
        // Error
        [`&${o}-status-error`]: {
          [`img, ${o}-img-mask`]: {
            borderRadius: n(e.borderRadius).sub(e.lineWidth).equal()
          },
          [`${o}-desc`]: {
            paddingInline: e.paddingXXS
          }
        },
        // Progress
        [`${o}-progress`]: {}
      },
      // ============================ Remove Icon ============================
      [`${o}-remove`]: {
        position: "absolute",
        top: 0,
        insetInlineEnd: 0,
        border: 0,
        padding: e.paddingXXS,
        background: "transparent",
        lineHeight: 1,
        transform: "translate(50%, -50%)",
        fontSize: e.fontSize,
        cursor: "pointer",
        opacity: e.opacityLoading,
        display: "none",
        "&:dir(rtl)": {
          transform: "translate(-50%, -50%)"
        },
        "&:hover": {
          opacity: 1
        },
        "&:active": {
          opacity: e.opacityLoading
        }
      },
      [`&:hover ${o}-remove`]: {
        display: "block"
      },
      // ============================== Status ===============================
      "&-status-error": {
        borderColor: e.colorError,
        [`${o}-desc`]: {
          color: e.colorError
        }
      },
      // ============================== Motion ===============================
      "&-motion": {
        transition: ["opacity", "width", "margin", "padding"].map((i) => `${i} ${e.motionDurationSlow}`).join(","),
        "&-appear-start": {
          width: 0,
          transition: "none"
        },
        "&-leave-active": {
          opacity: 0,
          width: 0,
          paddingInline: 0,
          borderInlineWidth: 0,
          marginInlineEnd: n(e.paddingSM).mul(-1).equal()
        }
      }
    }
  };
}, fr = {
  "&, *": {
    boxSizing: "border-box"
  }
}, Pa = (e) => {
  const {
    componentCls: t,
    calc: r,
    antCls: n
  } = e, o = `${t}-drop-area`, s = `${t}-placeholder`;
  return {
    // ============================== Full Screen ==============================
    [o]: {
      position: "absolute",
      inset: 0,
      zIndex: e.zIndexPopupBase,
      ...fr,
      "&-on-body": {
        position: "fixed",
        inset: 0
      },
      "&-hide-placement": {
        [`${s}-inner`]: {
          display: "none"
        }
      },
      [s]: {
        padding: 0
      }
    },
    "&": {
      // ============================= Placeholder =============================
      [s]: {
        height: "100%",
        borderRadius: e.borderRadius,
        borderWidth: e.lineWidthBold,
        borderStyle: "dashed",
        borderColor: "transparent",
        padding: e.padding,
        position: "relative",
        backdropFilter: "blur(10px)",
        background: e.colorBgPlaceholderHover,
        ...fr,
        [`${n}-upload-wrapper ${n}-upload${n}-upload-btn`]: {
          padding: 0
        },
        [`&${s}-drag-in`]: {
          borderColor: e.colorPrimaryHover
        },
        [`&${s}-disabled`]: {
          opacity: 0.25,
          pointerEvents: "none"
        },
        [`${s}-inner`]: {
          gap: r(e.paddingXXS).div(2).equal()
        },
        [`${s}-icon`]: {
          fontSize: e.fontSizeHeading2,
          lineHeight: 1
        },
        [`${s}-title${s}-title`]: {
          margin: 0,
          fontSize: e.fontSize,
          lineHeight: e.lineHeight
        },
        [`${s}-description`]: {}
      }
    }
  };
}, Ra = (e) => {
  const {
    componentCls: t,
    calc: r
  } = e, n = `${t}-list`, o = r(e.fontSize).mul(e.lineHeight).mul(2).add(e.paddingSM).add(e.paddingSM).equal();
  return {
    [t]: {
      position: "relative",
      width: "100%",
      ...fr,
      // =============================== File List ===============================
      [n]: {
        display: "flex",
        flexWrap: "wrap",
        gap: e.paddingSM,
        fontSize: e.fontSize,
        lineHeight: e.lineHeight,
        color: e.colorText,
        paddingBlock: e.paddingSM,
        paddingInline: e.padding,
        width: "100%",
        background: e.colorBgContainer,
        // Hide scrollbar
        scrollbarWidth: "none",
        "-ms-overflow-style": "none",
        "&::-webkit-scrollbar": {
          display: "none"
        },
        // Scroll
        "&-overflow-scrollX, &-overflow-scrollY": {
          "&:before, &:after": {
            content: '""',
            position: "absolute",
            opacity: 0,
            transition: `opacity ${e.motionDurationSlow}`,
            zIndex: 1
          }
        },
        "&-overflow-ping-start:before": {
          opacity: 1
        },
        "&-overflow-ping-end:after": {
          opacity: 1
        },
        "&-overflow-scrollX": {
          overflowX: "auto",
          overflowY: "hidden",
          flexWrap: "nowrap",
          "&:before, &:after": {
            insetBlock: 0,
            width: 8
          },
          "&:before": {
            insetInlineStart: 0,
            background: "linear-gradient(to right, rgba(0,0,0,0.06), rgba(0,0,0,0));"
          },
          "&:after": {
            insetInlineEnd: 0,
            background: "linear-gradient(to left, rgba(0,0,0,0.06), rgba(0,0,0,0));"
          },
          "&:dir(rtl)": {
            "&:before": {
              background: "linear-gradient(to left, rgba(0,0,0,0.06), rgba(0,0,0,0));"
            },
            "&:after": {
              background: "linear-gradient(to right, rgba(0,0,0,0.06), rgba(0,0,0,0));"
            }
          }
        },
        "&-overflow-scrollY": {
          overflowX: "hidden",
          overflowY: "auto",
          maxHeight: r(o).mul(3).equal(),
          "&:before, &:after": {
            insetInline: 0,
            height: 8
          },
          "&:before": {
            insetBlockStart: 0,
            background: "linear-gradient(to bottom, rgba(0,0,0,0.06), rgba(0,0,0,0));"
          },
          "&:after": {
            insetBlockEnd: 0,
            background: "linear-gradient(to top, rgba(0,0,0,0.06), rgba(0,0,0,0));"
          }
        },
        // ======================================================================
        // ==                              Upload                              ==
        // ======================================================================
        "&-upload-btn": {
          width: o,
          height: o,
          fontSize: e.fontSizeHeading2,
          color: "#999"
        },
        // ======================================================================
        // ==                             PrevNext                             ==
        // ======================================================================
        "&-prev-btn, &-next-btn": {
          position: "absolute",
          top: "50%",
          transform: "translateY(-50%)",
          boxShadow: e.boxShadowTertiary,
          opacity: 0,
          pointerEvents: "none"
        },
        "&-prev-btn": {
          left: {
            _skip_check_: !0,
            value: e.padding
          }
        },
        "&-next-btn": {
          right: {
            _skip_check_: !0,
            value: e.padding
          }
        },
        "&:dir(ltr)": {
          [`&${n}-overflow-ping-start ${n}-prev-btn`]: {
            opacity: 1,
            pointerEvents: "auto"
          },
          [`&${n}-overflow-ping-end ${n}-next-btn`]: {
            opacity: 1,
            pointerEvents: "auto"
          }
        },
        "&:dir(rtl)": {
          [`&${n}-overflow-ping-end ${n}-prev-btn`]: {
            opacity: 1,
            pointerEvents: "auto"
          },
          [`&${n}-overflow-ping-start ${n}-next-btn`]: {
            opacity: 1,
            pointerEvents: "auto"
          }
        }
      }
    }
  };
}, Ia = (e) => {
  const {
    colorBgContainer: t
  } = e;
  return {
    colorBgPlaceholderHover: new Se(t).setA(0.85).toRgbString()
  };
}, ho = zt("Attachments", (e) => {
  const t = Ye(e, {});
  return [Pa(t), Ra(t), $a(t)];
}, Ia), Ma = (e) => e.indexOf("image/") === 0, ft = 200;
function La(e) {
  return new Promise((t) => {
    if (!e || !e.type || !Ma(e.type)) {
      t("");
      return;
    }
    const r = new Image();
    if (r.onload = () => {
      const {
        width: n,
        height: o
      } = r, s = n / o, i = s > 1 ? ft : ft * s, a = s > 1 ? ft / s : ft, l = document.createElement("canvas");
      l.width = i, l.height = a, l.style.cssText = `position: fixed; left: 0; top: 0; width: ${i}px; height: ${a}px; z-index: 9999; display: none;`, document.body.appendChild(l), l.getContext("2d").drawImage(r, 0, 0, i, a);
      const f = l.toDataURL();
      document.body.removeChild(l), window.URL.revokeObjectURL(r.src), t(f);
    }, r.crossOrigin = "anonymous", e.type.startsWith("image/svg+xml")) {
      const n = new FileReader();
      n.onload = () => {
        n.result && typeof n.result == "string" && (r.src = n.result);
      }, n.readAsDataURL(e);
    } else if (e.type.startsWith("image/gif")) {
      const n = new FileReader();
      n.onload = () => {
        n.result && t(n.result);
      }, n.readAsDataURL(e);
    } else
      r.src = window.URL.createObjectURL(e);
  });
}
function Oa() {
  return /* @__PURE__ */ c.createElement("svg", {
    width: "1em",
    height: "1em",
    viewBox: "0 0 16 16",
    version: "1.1",
    xmlns: "http://www.w3.org/2000/svg"
    //xmlnsXlink="http://www.w3.org/1999/xlink"
  }, /* @__PURE__ */ c.createElement("title", null, "audio"), /* @__PURE__ */ c.createElement("g", {
    stroke: "none",
    strokeWidth: "1",
    fill: "none",
    fillRule: "evenodd"
  }, /* @__PURE__ */ c.createElement("path", {
    d: "M14.1178571,4.0125 C14.225,4.11964286 14.2857143,4.26428571 14.2857143,4.41607143 L14.2857143,15.4285714 C14.2857143,15.7446429 14.0303571,16 13.7142857,16 L2.28571429,16 C1.96964286,16 1.71428571,15.7446429 1.71428571,15.4285714 L1.71428571,0.571428571 C1.71428571,0.255357143 1.96964286,0 2.28571429,0 L9.86964286,0 C10.0214286,0 10.1678571,0.0607142857 10.275,0.167857143 L14.1178571,4.0125 Z M10.7315824,7.11216117 C10.7428131,7.15148751 10.7485063,7.19218979 10.7485063,7.23309113 L10.7485063,8.07742614 C10.7484199,8.27364959 10.6183424,8.44607275 10.4296853,8.50003683 L8.32984514,9.09986306 L8.32984514,11.7071803 C8.32986605,12.5367078 7.67249692,13.217028 6.84345686,13.2454634 L6.79068592,13.2463395 C6.12766108,13.2463395 5.53916361,12.8217001 5.33010655,12.1924966 C5.1210495,11.563293 5.33842118,10.8709227 5.86959669,10.4741173 C6.40077221,10.0773119 7.12636292,10.0652587 7.67042486,10.4442027 L7.67020842,7.74937024 L7.68449368,7.74937024 C7.72405122,7.59919041 7.83988806,7.48101083 7.98924584,7.4384546 L10.1880418,6.81004755 C10.42156,6.74340323 10.6648954,6.87865515 10.7315824,7.11216117 Z M9.60714286,1.31785714 L12.9678571,4.67857143 L9.60714286,4.67857143 L9.60714286,1.31785714 Z",
    fill: "currentColor"
  })));
}
function ja(e) {
  const {
    percent: t
  } = e, {
    token: r
  } = Je.useToken();
  return /* @__PURE__ */ c.createElement(us, {
    type: "circle",
    percent: t,
    size: r.fontSizeHeading2 * 2,
    strokeColor: "#FFF",
    trailColor: "rgba(255, 255, 255, 0.3)",
    format: (n) => /* @__PURE__ */ c.createElement("span", {
      style: {
        color: "#FFF"
      }
    }, (n || 0).toFixed(0), "%")
  });
}
function Na() {
  return /* @__PURE__ */ c.createElement("svg", {
    width: "1em",
    height: "1em",
    viewBox: "0 0 16 16",
    version: "1.1",
    xmlns: "http://www.w3.org/2000/svg"
    // xmlnsXlink="http://www.w3.org/1999/xlink"
  }, /* @__PURE__ */ c.createElement("title", null, "video"), /* @__PURE__ */ c.createElement("g", {
    stroke: "none",
    strokeWidth: "1",
    fill: "none",
    fillRule: "evenodd"
  }, /* @__PURE__ */ c.createElement("path", {
    d: "M14.1178571,4.0125 C14.225,4.11964286 14.2857143,4.26428571 14.2857143,4.41607143 L14.2857143,15.4285714 C14.2857143,15.7446429 14.0303571,16 13.7142857,16 L2.28571429,16 C1.96964286,16 1.71428571,15.7446429 1.71428571,15.4285714 L1.71428571,0.571428571 C1.71428571,0.255357143 1.96964286,0 2.28571429,0 L9.86964286,0 C10.0214286,0 10.1678571,0.0607142857 10.275,0.167857143 L14.1178571,4.0125 Z M12.9678571,4.67857143 L9.60714286,1.31785714 L9.60714286,4.67857143 L12.9678571,4.67857143 Z M10.5379461,10.3101106 L6.68957555,13.0059749 C6.59910784,13.0693494 6.47439406,13.0473861 6.41101953,12.9569184 C6.3874624,12.9232903 6.37482581,12.8832269 6.37482581,12.8421686 L6.37482581,7.45043999 C6.37482581,7.33998304 6.46436886,7.25043999 6.57482581,7.25043999 C6.61588409,7.25043999 6.65594753,7.26307658 6.68957555,7.28663371 L10.5379461,9.98249803 C10.6284138,10.0458726 10.6503772,10.1705863 10.5870027,10.2610541 C10.5736331,10.2801392 10.5570312,10.2967411 10.5379461,10.3101106 Z",
    fill: "currentColor"
  })));
}
const er = " ", dr = "#8c8c8c", yo = ["png", "jpg", "jpeg", "gif", "bmp", "webp", "svg"], Fa = [{
  icon: /* @__PURE__ */ c.createElement(Vo, null),
  color: "#22b35e",
  ext: ["xlsx", "xls"]
}, {
  icon: /* @__PURE__ */ c.createElement(Xo, null),
  color: dr,
  ext: yo
}, {
  icon: /* @__PURE__ */ c.createElement(Uo, null),
  color: dr,
  ext: ["md", "mdx"]
}, {
  icon: /* @__PURE__ */ c.createElement(Go, null),
  color: "#ff4d4f",
  ext: ["pdf"]
}, {
  icon: /* @__PURE__ */ c.createElement(Ko, null),
  color: "#ff6e31",
  ext: ["ppt", "pptx"]
}, {
  icon: /* @__PURE__ */ c.createElement(qo, null),
  color: "#1677ff",
  ext: ["doc", "docx"]
}, {
  icon: /* @__PURE__ */ c.createElement(Yo, null),
  color: "#fab714",
  ext: ["zip", "rar", "7z", "tar", "gz"]
}, {
  icon: /* @__PURE__ */ c.createElement(Na, null),
  color: "#ff4d4f",
  ext: ["mp4", "avi", "mov", "wmv", "flv", "mkv"]
}, {
  icon: /* @__PURE__ */ c.createElement(Oa, null),
  color: "#8c8c8c",
  ext: ["mp3", "wav", "flac", "ape", "aac", "ogg"]
}];
function xn(e, t) {
  return t.some((r) => e.toLowerCase() === `.${r}`);
}
function ka(e) {
  let t = e;
  const r = ["B", "KB", "MB", "GB", "TB", "PB", "EB"];
  let n = 0;
  for (; t >= 1024 && n < r.length - 1; )
    t /= 1024, n++;
  return `${t.toFixed(0)} ${r[n]}`;
}
function Aa(e, t) {
  const {
    prefixCls: r,
    item: n,
    onRemove: o,
    className: s,
    style: i,
    imageProps: a
  } = e, l = c.useContext(ot), {
    disabled: u
  } = l || {}, {
    name: f,
    size: m,
    percent: d,
    status: h = "done",
    description: v
  } = n, {
    getPrefixCls: g
  } = Pe(), p = g("attachment", r), y = `${p}-list-card`, [T, P, _] = ho(p), [$, b] = c.useMemo(() => {
    const A = f || "", D = A.match(/^(.*)\.[^.]+$/);
    return D ? [D[1], A.slice(D[1].length)] : [A, ""];
  }, [f]), I = c.useMemo(() => xn(b, yo), [b]), E = c.useMemo(() => v || (h === "uploading" ? `${d || 0}%` : h === "error" ? n.response || er : m ? ka(m) : er), [h, d]), [O, L] = c.useMemo(() => {
    for (const {
      ext: A,
      icon: D,
      color: B
    } of Fa)
      if (xn(b, A))
        return [D, B];
    return [/* @__PURE__ */ c.createElement(Bo, {
      key: "defaultIcon"
    }), dr];
  }, [b]), [j, M] = c.useState();
  c.useEffect(() => {
    if (n.originFileObj) {
      let A = !0;
      return La(n.originFileObj).then((D) => {
        A && M(D);
      }), () => {
        A = !1;
      };
    }
    M(void 0);
  }, [n.originFileObj]);
  let x = null;
  const w = n.thumbUrl || n.url || j, k = I && (n.originFileObj || w);
  return k ? x = /* @__PURE__ */ c.createElement(c.Fragment, null, w && /* @__PURE__ */ c.createElement(fs, ve({
    alt: "preview",
    src: w
  }, a)), h !== "done" && /* @__PURE__ */ c.createElement("div", {
    className: `${y}-img-mask`
  }, h === "uploading" && d !== void 0 && /* @__PURE__ */ c.createElement(ja, {
    percent: d,
    prefixCls: y
  }), h === "error" && /* @__PURE__ */ c.createElement("div", {
    className: `${y}-desc`
  }, /* @__PURE__ */ c.createElement("div", {
    className: `${y}-ellipsis-prefix`
  }, E)))) : x = /* @__PURE__ */ c.createElement(c.Fragment, null, /* @__PURE__ */ c.createElement("div", {
    className: `${y}-icon`,
    style: {
      color: L
    }
  }, O), /* @__PURE__ */ c.createElement("div", {
    className: `${y}-content`
  }, /* @__PURE__ */ c.createElement("div", {
    className: `${y}-name`
  }, /* @__PURE__ */ c.createElement("div", {
    className: `${y}-ellipsis-prefix`
  }, $ ?? er), /* @__PURE__ */ c.createElement("div", {
    className: `${y}-ellipsis-suffix`
  }, b)), /* @__PURE__ */ c.createElement("div", {
    className: `${y}-desc`
  }, /* @__PURE__ */ c.createElement("div", {
    className: `${y}-ellipsis-prefix`
  }, E)))), T(/* @__PURE__ */ c.createElement("div", {
    className: F(y, {
      [`${y}-status-${h}`]: h,
      [`${y}-type-preview`]: k,
      [`${y}-type-overview`]: !k
    }, s, P, _),
    style: i,
    ref: t
  }, x, !u && o && /* @__PURE__ */ c.createElement("button", {
    type: "button",
    className: `${y}-remove`,
    onClick: () => {
      o(n);
    }
  }, /* @__PURE__ */ c.createElement(Wo, null))));
}
const vo = /* @__PURE__ */ c.forwardRef(Aa), wn = 1;
function za(e) {
  const {
    prefixCls: t,
    items: r,
    onRemove: n,
    overflow: o,
    upload: s,
    listClassName: i,
    listStyle: a,
    itemClassName: l,
    itemStyle: u,
    imageProps: f
  } = e, m = `${t}-list`, d = c.useRef(null), [h, v] = c.useState(!1), {
    disabled: g
  } = c.useContext(ot);
  c.useEffect(() => (v(!0), () => {
    v(!1);
  }), []);
  const [p, y] = c.useState(!1), [T, P] = c.useState(!1), _ = () => {
    const E = d.current;
    E && (o === "scrollX" ? (y(Math.abs(E.scrollLeft) >= wn), P(E.scrollWidth - E.clientWidth - Math.abs(E.scrollLeft) >= wn)) : o === "scrollY" && (y(E.scrollTop !== 0), P(E.scrollHeight - E.clientHeight !== E.scrollTop)));
  };
  c.useEffect(() => {
    _();
  }, [o, r.length]);
  const $ = (E) => {
    const O = d.current;
    O && O.scrollTo({
      left: O.scrollLeft + E * O.clientWidth,
      behavior: "smooth"
    });
  }, b = () => {
    $(-1);
  }, I = () => {
    $(1);
  };
  return /* @__PURE__ */ c.createElement("div", {
    className: F(m, {
      [`${m}-overflow-${e.overflow}`]: o,
      [`${m}-overflow-ping-start`]: p,
      [`${m}-overflow-ping-end`]: T
    }, i),
    ref: d,
    onScroll: _,
    style: a
  }, /* @__PURE__ */ c.createElement(oa, {
    keys: r.map((E) => ({
      key: E.uid,
      item: E
    })),
    motionName: `${m}-card-motion`,
    component: !1,
    motionAppear: h,
    motionLeave: !0,
    motionEnter: !0
  }, ({
    key: E,
    item: O,
    className: L,
    style: j
  }) => /* @__PURE__ */ c.createElement(vo, {
    key: E,
    prefixCls: t,
    item: O,
    onRemove: n,
    className: F(L, l),
    imageProps: f,
    style: {
      ...j,
      ...u
    }
  })), !g && /* @__PURE__ */ c.createElement(uo, {
    upload: s
  }, /* @__PURE__ */ c.createElement(re, {
    className: `${m}-upload-btn`,
    type: "dashed"
  }, /* @__PURE__ */ c.createElement(Qo, {
    className: `${m}-upload-btn-icon`
  }))), o === "scrollX" && /* @__PURE__ */ c.createElement(c.Fragment, null, /* @__PURE__ */ c.createElement(re, {
    size: "small",
    shape: "circle",
    className: `${m}-prev-btn`,
    icon: /* @__PURE__ */ c.createElement(Zo, null),
    onClick: b
  }), /* @__PURE__ */ c.createElement(re, {
    size: "small",
    shape: "circle",
    className: `${m}-next-btn`,
    icon: /* @__PURE__ */ c.createElement(Jo, null),
    onClick: I
  })));
}
function Da(e, t) {
  const {
    prefixCls: r,
    placeholder: n = {},
    upload: o,
    className: s,
    style: i
  } = e, a = `${r}-placeholder`, l = n || {}, {
    disabled: u
  } = c.useContext(ot), [f, m] = c.useState(!1), d = () => {
    m(!0);
  }, h = (p) => {
    p.currentTarget.contains(p.relatedTarget) || m(!1);
  }, v = () => {
    m(!1);
  }, g = /* @__PURE__ */ c.isValidElement(n) ? n : /* @__PURE__ */ c.createElement(Ce, {
    align: "center",
    justify: "center",
    vertical: !0,
    className: `${a}-inner`
  }, /* @__PURE__ */ c.createElement($e.Text, {
    className: `${a}-icon`
  }, l.icon), /* @__PURE__ */ c.createElement($e.Title, {
    className: `${a}-title`,
    level: 5
  }, l.title), /* @__PURE__ */ c.createElement($e.Text, {
    className: `${a}-description`,
    type: "secondary"
  }, l.description));
  return /* @__PURE__ */ c.createElement("div", {
    className: F(a, {
      [`${a}-drag-in`]: f,
      [`${a}-disabled`]: u
    }, s),
    onDragEnter: d,
    onDragLeave: h,
    onDrop: v,
    "aria-hidden": u,
    style: i
  }, /* @__PURE__ */ c.createElement(kn.Dragger, ve({
    showUploadList: !1
  }, o, {
    ref: t,
    style: {
      padding: 0,
      border: 0,
      background: "transparent"
    }
  }), g));
}
const Ha = /* @__PURE__ */ c.forwardRef(Da);
function Ba(e, t) {
  const {
    prefixCls: r,
    rootClassName: n,
    rootStyle: o,
    className: s,
    style: i,
    items: a,
    children: l,
    getDropContainer: u,
    placeholder: f,
    onChange: m,
    onRemove: d,
    overflow: h,
    imageProps: v,
    disabled: g,
    classNames: p = {},
    styles: y = {},
    ...T
  } = e, {
    getPrefixCls: P,
    direction: _
  } = Pe(), $ = P("attachment", r), b = Ct("attachments"), {
    classNames: I,
    styles: E
  } = b, O = c.useRef(null), L = c.useRef(null);
  c.useImperativeHandle(t, () => ({
    nativeElement: O.current,
    upload: (W) => {
      var U, q;
      const G = (q = (U = L.current) == null ? void 0 : U.nativeElement) == null ? void 0 : q.querySelector('input[type="file"]');
      if (G) {
        const ie = new DataTransfer();
        ie.items.add(W), G.files = ie.files, G.dispatchEvent(new Event("change", {
          bubbles: !0
        }));
      }
    }
  }));
  const [j, M, x] = ho($), w = F(M, x), [k, A] = mi([], {
    value: a
  }), D = je((W) => {
    A(W.fileList), m == null || m(W);
  }), B = {
    ...T,
    fileList: k,
    onChange: D
  }, oe = (W) => Promise.resolve(typeof d == "function" ? d(W) : d).then((G) => {
    if (G === !1)
      return;
    const U = k.filter((q) => q.uid !== W.uid);
    D({
      file: {
        ...W,
        status: "removed"
      },
      fileList: U
    });
  });
  let se;
  const X = (W, G, U) => {
    const q = typeof f == "function" ? f(W) : f;
    return /* @__PURE__ */ c.createElement(Ha, {
      placeholder: q,
      upload: B,
      prefixCls: $,
      className: F(I.placeholder, p.placeholder),
      style: {
        ...E.placeholder,
        ...y.placeholder,
        ...G == null ? void 0 : G.style
      },
      ref: U
    });
  };
  if (l)
    se = /* @__PURE__ */ c.createElement(c.Fragment, null, /* @__PURE__ */ c.createElement(uo, {
      upload: B,
      rootClassName: n,
      ref: L
    }, l), /* @__PURE__ */ c.createElement(rn, {
      getDropContainer: u,
      prefixCls: $,
      className: F(w, n)
    }, X("drop")));
  else {
    const W = k.length > 0;
    se = /* @__PURE__ */ c.createElement("div", {
      className: F($, w, {
        [`${$}-rtl`]: _ === "rtl"
      }, s, n),
      style: {
        ...o,
        ...i
      },
      dir: _ || "ltr",
      ref: O
    }, /* @__PURE__ */ c.createElement(za, {
      prefixCls: $,
      items: k,
      onRemove: oe,
      overflow: h,
      upload: B,
      listClassName: F(I.list, p.list),
      listStyle: {
        ...E.list,
        ...y.list,
        ...!W && {
          display: "none"
        }
      },
      itemClassName: F(I.item, p.item),
      itemStyle: {
        ...E.item,
        ...y.item
      },
      imageProps: v
    }), X("inline", W ? {
      style: {
        display: "none"
      }
    } : {}, L), /* @__PURE__ */ c.createElement(rn, {
      getDropContainer: u || (() => O.current),
      prefixCls: $,
      className: w
    }, X("drop")));
  }
  return j(/* @__PURE__ */ c.createElement(ot.Provider, {
    value: {
      disabled: g
    }
  }, se));
}
const bo = /* @__PURE__ */ c.forwardRef(Ba);
bo.FileCard = vo;
var Wa = `accept acceptCharset accessKey action allowFullScreen allowTransparency
    alt async autoComplete autoFocus autoPlay capture cellPadding cellSpacing challenge
    charSet checked classID className colSpan cols content contentEditable contextMenu
    controls coords crossOrigin data dateTime default defer dir disabled download draggable
    encType form formAction formEncType formMethod formNoValidate formTarget frameBorder
    headers height hidden high href hrefLang htmlFor httpEquiv icon id inputMode integrity
    is keyParams keyType kind label lang list loop low manifest marginHeight marginWidth max maxLength media
    mediaGroup method min minLength multiple muted name noValidate nonce open
    optimum pattern placeholder poster preload radioGroup readOnly rel required
    reversed role rowSpan rows sandbox scope scoped scrolling seamless selected
    shape size sizes span spellCheck src srcDoc srcLang srcSet start step style
    summary tabIndex target title type useMap value width wmode wrap`, Va = `onCopy onCut onPaste onCompositionEnd onCompositionStart onCompositionUpdate onKeyDown
    onKeyPress onKeyUp onFocus onBlur onChange onInput onSubmit onClick onContextMenu onDoubleClick
    onDrag onDragEnd onDragEnter onDragExit onDragLeave onDragOver onDragStart onDrop onMouseDown
    onMouseEnter onMouseLeave onMouseMove onMouseOut onMouseOver onMouseUp onSelect onTouchCancel
    onTouchEnd onTouchMove onTouchStart onScroll onWheel onAbort onCanPlay onCanPlayThrough
    onDurationChange onEmptied onEncrypted onEnded onError onLoadedData onLoadedMetadata
    onLoadStart onPause onPlay onPlaying onProgress onRateChange onSeeked onSeeking onStalled onSuspend onTimeUpdate onVolumeChange onWaiting onLoad onError`, Xa = "".concat(Wa, " ").concat(Va).split(/[\s\n]+/), Ua = "aria-", Ga = "data-";
function _n(e, t) {
  return e.indexOf(t) === 0;
}
function Ka(e) {
  var t = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : !1, r;
  t === !1 ? r = {
    aria: !0,
    data: !0,
    attr: !0
  } : t === !0 ? r = {
    aria: !0
  } : r = $i({}, t);
  var n = {};
  return Object.keys(e).forEach(function(o) {
    // Aria
    (r.aria && (o === "role" || _n(o, Ua)) || // Data
    r.data && _n(o, Ga) || // Attr
    r.attr && Xa.includes(o)) && (n[o] = e[o]);
  }), n;
}
function dt(e) {
  return typeof e == "string";
}
const qa = (e, t, r, n) => {
  const o = R.useRef(""), [s, i] = R.useState(1), a = t && dt(e);
  return Un(() => {
    !a && dt(e) ? i(e.length) : dt(e) && dt(o.current) && e.indexOf(o.current) !== 0 && i(1), o.current = e;
  }, [e]), R.useEffect(() => {
    if (a && s < e.length) {
      const u = setTimeout(() => {
        i((f) => f + r);
      }, n);
      return () => {
        clearTimeout(u);
      };
    }
  }, [s, t, e]), [a ? e.slice(0, s) : e, a && s < e.length];
};
function Ya(e) {
  return R.useMemo(() => {
    if (!e)
      return [!1, 0, 0, null];
    let t = {
      step: 1,
      interval: 50,
      // set default suffix is empty
      suffix: null
    };
    return typeof e == "object" && (t = {
      ...t,
      ...e
    }), [!0, t.step, t.interval, t.suffix];
  }, [e]);
}
const Qa = ({
  prefixCls: e
}) => /* @__PURE__ */ c.createElement("span", {
  className: `${e}-dot`
}, /* @__PURE__ */ c.createElement("i", {
  className: `${e}-dot-item`,
  key: "item-1"
}), /* @__PURE__ */ c.createElement("i", {
  className: `${e}-dot-item`,
  key: "item-2"
}), /* @__PURE__ */ c.createElement("i", {
  className: `${e}-dot-item`,
  key: "item-3"
})), Za = (e) => {
  const {
    componentCls: t,
    paddingSM: r,
    padding: n
  } = e;
  return {
    [t]: {
      [`${t}-content`]: {
        // Shared: filled, outlined, shadow
        "&-filled,&-outlined,&-shadow": {
          padding: `${Xe(r)} ${Xe(n)}`,
          borderRadius: e.borderRadiusLG
        },
        // Filled:
        "&-filled": {
          backgroundColor: e.colorFillContent
        },
        // Outlined:
        "&-outlined": {
          border: `1px solid ${e.colorBorderSecondary}`
        },
        // Shadow:
        "&-shadow": {
          boxShadow: e.boxShadowTertiary
        }
      }
    }
  };
}, Ja = (e) => {
  const {
    componentCls: t,
    fontSize: r,
    lineHeight: n,
    paddingSM: o,
    padding: s,
    calc: i
  } = e, a = i(r).mul(n).div(2).add(o).equal(), l = `${t}-content`;
  return {
    [t]: {
      [l]: {
        // round:
        "&-round": {
          borderRadius: {
            _skip_check_: !0,
            value: a
          },
          paddingInline: i(s).mul(1.25).equal()
        }
      },
      // corner:
      [`&-start ${l}-corner`]: {
        borderStartStartRadius: e.borderRadiusXS
      },
      [`&-end ${l}-corner`]: {
        borderStartEndRadius: e.borderRadiusXS
      }
    }
  };
}, el = (e) => {
  const {
    componentCls: t,
    padding: r
  } = e;
  return {
    [`${t}-list`]: {
      display: "flex",
      flexDirection: "column",
      gap: r,
      overflowY: "auto",
      "&::-webkit-scrollbar": {
        width: 8,
        backgroundColor: "transparent"
      },
      "&::-webkit-scrollbar-thumb": {
        backgroundColor: e.colorTextTertiary,
        borderRadius: e.borderRadiusSM
      },
      // For Firefox
      "&": {
        scrollbarWidth: "thin",
        scrollbarColor: `${e.colorTextTertiary} transparent`
      }
    }
  };
}, tl = new zn("loadingMove", {
  "0%": {
    transform: "translateY(0)"
  },
  "10%": {
    transform: "translateY(4px)"
  },
  "20%": {
    transform: "translateY(0)"
  },
  "30%": {
    transform: "translateY(-4px)"
  },
  "40%": {
    transform: "translateY(0)"
  }
}), rl = new zn("cursorBlink", {
  "0%": {
    opacity: 1
  },
  "50%": {
    opacity: 0
  },
  "100%": {
    opacity: 1
  }
}), nl = (e) => {
  const {
    componentCls: t,
    fontSize: r,
    lineHeight: n,
    paddingSM: o,
    colorText: s,
    calc: i
  } = e;
  return {
    [t]: {
      display: "flex",
      columnGap: o,
      [`&${t}-end`]: {
        justifyContent: "end",
        flexDirection: "row-reverse",
        [`& ${t}-content-wrapper`]: {
          alignItems: "flex-end"
        }
      },
      [`&${t}-rtl`]: {
        direction: "rtl"
      },
      [`&${t}-typing ${t}-content:last-child::after`]: {
        content: '"|"',
        fontWeight: 900,
        userSelect: "none",
        opacity: 1,
        marginInlineStart: "0.1em",
        animationName: rl,
        animationDuration: "0.8s",
        animationIterationCount: "infinite",
        animationTimingFunction: "linear"
      },
      // ============================ Avatar =============================
      [`& ${t}-avatar`]: {
        display: "inline-flex",
        justifyContent: "center",
        alignSelf: "flex-start"
      },
      // ======================== Header & Footer ========================
      [`& ${t}-header, & ${t}-footer`]: {
        fontSize: r,
        lineHeight: n,
        color: e.colorText
      },
      [`& ${t}-header`]: {
        marginBottom: e.paddingXXS
      },
      [`& ${t}-footer`]: {
        marginTop: o
      },
      // =========================== Content =============================
      [`& ${t}-content-wrapper`]: {
        flex: "auto",
        display: "flex",
        flexDirection: "column",
        alignItems: "flex-start",
        minWidth: 0,
        maxWidth: "100%"
      },
      [`& ${t}-content`]: {
        position: "relative",
        boxSizing: "border-box",
        minWidth: 0,
        maxWidth: "100%",
        color: s,
        fontSize: e.fontSize,
        lineHeight: e.lineHeight,
        minHeight: i(o).mul(2).add(i(n).mul(r)).equal(),
        wordBreak: "break-word",
        [`& ${t}-dot`]: {
          position: "relative",
          height: "100%",
          display: "flex",
          alignItems: "center",
          columnGap: e.marginXS,
          padding: `0 ${Xe(e.paddingXXS)}`,
          "&-item": {
            backgroundColor: e.colorPrimary,
            borderRadius: "100%",
            width: 4,
            height: 4,
            animationName: tl,
            animationDuration: "2s",
            animationIterationCount: "infinite",
            animationTimingFunction: "linear",
            "&:nth-child(1)": {
              animationDelay: "0s"
            },
            "&:nth-child(2)": {
              animationDelay: "0.2s"
            },
            "&:nth-child(3)": {
              animationDelay: "0.4s"
            }
          }
        }
      }
    }
  };
}, ol = () => ({}), So = zt("Bubble", (e) => {
  const t = Ye(e, {});
  return [nl(t), el(t), Za(t), Ja(t)];
}, ol), xo = /* @__PURE__ */ c.createContext({}), sl = (e, t) => {
  const {
    prefixCls: r,
    className: n,
    rootClassName: o,
    style: s,
    classNames: i = {},
    styles: a = {},
    avatar: l,
    placement: u = "start",
    loading: f = !1,
    loadingRender: m,
    typing: d,
    content: h = "",
    messageRender: v,
    variant: g = "filled",
    shape: p,
    onTypingComplete: y,
    header: T,
    footer: P,
    _key: _,
    ...$
  } = e, {
    onUpdate: b
  } = c.useContext(xo), I = c.useRef(null);
  c.useImperativeHandle(t, () => ({
    nativeElement: I.current
  }));
  const {
    direction: E,
    getPrefixCls: O
  } = Pe(), L = O("bubble", r), j = Ct("bubble"), [M, x, w, k] = Ya(d), [A, D] = qa(h, M, x, w);
  c.useEffect(() => {
    b == null || b();
  }, [A]);
  const B = c.useRef(!1);
  c.useEffect(() => {
    !D && !f ? B.current || (B.current = !0, y == null || y()) : B.current = !1;
  }, [D, f]);
  const [oe, se, X] = So(L), W = F(L, o, j.className, n, se, X, `${L}-${u}`, {
    [`${L}-rtl`]: E === "rtl",
    [`${L}-typing`]: D && !f && !v && !k
  }), G = c.useMemo(() => /* @__PURE__ */ c.isValidElement(l) ? l : /* @__PURE__ */ c.createElement(ds, l), [l]), U = c.useMemo(() => v ? v(A) : A, [A, v]), q = (xe) => typeof xe == "function" ? xe(A, {
    key: _
  }) : xe;
  let ie;
  f ? ie = m ? m() : /* @__PURE__ */ c.createElement(Qa, {
    prefixCls: L
  }) : ie = /* @__PURE__ */ c.createElement(c.Fragment, null, U, D && k);
  let ee = /* @__PURE__ */ c.createElement("div", {
    style: {
      ...j.styles.content,
      ...a.content
    },
    className: F(`${L}-content`, `${L}-content-${g}`, p && `${L}-content-${p}`, j.classNames.content, i.content)
  }, ie);
  return (T || P) && (ee = /* @__PURE__ */ c.createElement("div", {
    className: `${L}-content-wrapper`
  }, T && /* @__PURE__ */ c.createElement("div", {
    className: F(`${L}-header`, j.classNames.header, i.header),
    style: {
      ...j.styles.header,
      ...a.header
    }
  }, q(T)), ee, P && /* @__PURE__ */ c.createElement("div", {
    className: F(`${L}-footer`, j.classNames.footer, i.footer),
    style: {
      ...j.styles.footer,
      ...a.footer
    }
  }, q(P)))), oe(/* @__PURE__ */ c.createElement("div", ve({
    style: {
      ...j.style,
      ...s
    },
    className: W
  }, $, {
    ref: I
  }), l && /* @__PURE__ */ c.createElement("div", {
    style: {
      ...j.styles.avatar,
      ...a.avatar
    },
    className: F(`${L}-avatar`, j.classNames.avatar, i.avatar)
  }, G), ee));
}, Cr = /* @__PURE__ */ c.forwardRef(sl);
function il(e, t) {
  const r = R.useCallback((n, o) => typeof t == "function" ? t(n, o) : t ? t[n.role] || {} : {}, [t]);
  return R.useMemo(() => (e || []).map((n, o) => {
    const s = n.key ?? `preset_${o}`;
    return {
      ...r(n, o),
      ...n,
      key: s
    };
  }), [e, r]);
}
const al = ({
  _key: e,
  ...t
}, r) => /* @__PURE__ */ R.createElement(Cr, ve({}, t, {
  ref: (n) => {
    var o;
    n ? r.current[e] = n : (o = r.current) == null || delete o[e];
  }
})), ll = /* @__PURE__ */ R.memo(/* @__PURE__ */ R.forwardRef(al)), cl = 1, ul = (e, t) => {
  const {
    prefixCls: r,
    rootClassName: n,
    className: o,
    items: s,
    autoScroll: i = !0,
    roles: a,
    ...l
  } = e, u = Ka(l, {
    attr: !0,
    aria: !0
  }), f = R.useRef(null), m = R.useRef({}), {
    getPrefixCls: d
  } = Pe(), h = d("bubble", r), v = `${h}-list`, [g, p, y] = So(h), [T, P] = R.useState(!1);
  R.useEffect(() => (P(!0), () => {
    P(!1);
  }), []);
  const _ = il(s, a), [$, b] = R.useState(!0), [I, E] = R.useState(0), O = (M) => {
    const x = M.target;
    b(x.scrollHeight - Math.abs(x.scrollTop) - x.clientHeight <= cl);
  };
  R.useEffect(() => {
    i && f.current && $ && f.current.scrollTo({
      top: f.current.scrollHeight
    });
  }, [I]), R.useEffect(() => {
    var M;
    if (i) {
      const x = (M = _[_.length - 2]) == null ? void 0 : M.key, w = m.current[x];
      if (w) {
        const {
          nativeElement: k
        } = w, {
          top: A,
          bottom: D
        } = k.getBoundingClientRect(), {
          top: B,
          bottom: oe
        } = f.current.getBoundingClientRect();
        A < oe && D > B && (E((X) => X + 1), b(!0));
      }
    }
  }, [_.length]), R.useImperativeHandle(t, () => ({
    nativeElement: f.current,
    scrollTo: ({
      key: M,
      offset: x,
      behavior: w = "smooth",
      block: k
    }) => {
      if (typeof x == "number")
        f.current.scrollTo({
          top: x,
          behavior: w
        });
      else if (M !== void 0) {
        const A = m.current[M];
        if (A) {
          const D = _.findIndex((B) => B.key === M);
          b(D === _.length - 1), A.nativeElement.scrollIntoView({
            behavior: w,
            block: k
          });
        }
      }
    }
  }));
  const L = je(() => {
    i && E((M) => M + 1);
  }), j = R.useMemo(() => ({
    onUpdate: L
  }), []);
  return g(/* @__PURE__ */ R.createElement(xo.Provider, {
    value: j
  }, /* @__PURE__ */ R.createElement("div", ve({}, u, {
    className: F(v, n, o, p, y, {
      [`${v}-reach-end`]: $
    }),
    ref: f,
    onScroll: O
  }), _.map(({
    key: M,
    ...x
  }) => /* @__PURE__ */ R.createElement(ll, ve({}, x, {
    key: M,
    _key: M,
    ref: m,
    typing: T ? x.typing : !1
  }))))));
}, fl = /* @__PURE__ */ R.forwardRef(ul);
Cr.List = fl;
const dl = (e) => {
  const {
    componentCls: t
  } = e;
  return {
    [t]: {
      // ======================== Prompt ========================
      "&, & *": {
        boxSizing: "border-box"
      },
      maxWidth: "100%",
      [`&${t}-rtl`]: {
        direction: "rtl"
      },
      [`& ${t}-title`]: {
        marginBlockStart: 0,
        fontWeight: "normal",
        color: e.colorTextTertiary
      },
      [`& ${t}-list`]: {
        display: "flex",
        gap: e.paddingSM,
        overflowX: "auto",
        // Hide scrollbar
        scrollbarWidth: "none",
        "-ms-overflow-style": "none",
        "&::-webkit-scrollbar": {
          display: "none"
        },
        listStyle: "none",
        paddingInlineStart: 0,
        marginBlock: 0,
        alignItems: "stretch",
        "&-wrap": {
          flexWrap: "wrap"
        },
        "&-vertical": {
          flexDirection: "column",
          alignItems: "flex-start"
        }
      },
      // ========================= Item =========================
      [`${t}-item`]: {
        flex: "none",
        display: "flex",
        gap: e.paddingXS,
        height: "auto",
        paddingBlock: e.paddingSM,
        paddingInline: e.padding,
        alignItems: "flex-start",
        justifyContent: "flex-start",
        background: e.colorBgContainer,
        borderRadius: e.borderRadiusLG,
        transition: ["border", "background"].map((r) => `${r} ${e.motionDurationSlow}`).join(","),
        border: `${Xe(e.lineWidth)} ${e.lineType} ${e.colorBorderSecondary}`,
        [`&:not(${t}-item-has-nest)`]: {
          "&:hover": {
            cursor: "pointer",
            background: e.colorFillTertiary
          },
          "&:active": {
            background: e.colorFill
          }
        },
        [`${t}-content`]: {
          flex: "auto",
          minWidth: 0,
          display: "flex",
          gap: e.paddingXXS,
          flexDirection: "column",
          alignItems: "flex-start"
        },
        [`${t}-icon, ${t}-label, ${t}-desc`]: {
          margin: 0,
          padding: 0,
          fontSize: e.fontSize,
          lineHeight: e.lineHeight,
          textAlign: "start",
          whiteSpace: "normal"
        },
        [`${t}-label`]: {
          color: e.colorTextHeading,
          fontWeight: 500
        },
        [`${t}-label + ${t}-desc`]: {
          color: e.colorTextTertiary
        },
        // Disabled
        [`&${t}-item-disabled`]: {
          pointerEvents: "none",
          background: e.colorBgContainerDisabled,
          [`${t}-label, ${t}-desc`]: {
            color: e.colorTextTertiary
          }
        }
      }
    }
  };
}, ml = (e) => {
  const {
    componentCls: t
  } = e;
  return {
    [t]: {
      // ========================= Parent =========================
      [`${t}-item-has-nest`]: {
        [`> ${t}-content`]: {
          // gap: token.paddingSM,
          [`> ${t}-label`]: {
            fontSize: e.fontSizeLG,
            lineHeight: e.lineHeightLG
          }
        }
      },
      // ========================= Nested =========================
      [`&${t}-nested`]: {
        marginTop: e.paddingXS,
        // ======================== Prompt ========================
        alignSelf: "stretch",
        [`${t}-list`]: {
          alignItems: "stretch"
        },
        // ========================= Item =========================
        [`${t}-item`]: {
          border: 0,
          background: e.colorFillQuaternary
        }
      }
    }
  };
}, pl = () => ({}), gl = zt("Prompts", (e) => {
  const t = Ye(e, {});
  return [dl(t), ml(t)];
}, pl), Tr = (e) => {
  const {
    prefixCls: t,
    title: r,
    className: n,
    items: o,
    onItemClick: s,
    vertical: i,
    wrap: a,
    rootClassName: l,
    styles: u = {},
    classNames: f = {},
    style: m,
    ...d
  } = e, {
    getPrefixCls: h,
    direction: v
  } = Pe(), g = h("prompts", t), p = Ct("prompts"), [y, T, P] = gl(g), _ = F(g, p.className, n, l, T, P, {
    [`${g}-rtl`]: v === "rtl"
  }), $ = F(`${g}-list`, p.classNames.list, f.list, {
    [`${g}-list-wrap`]: a
  }, {
    [`${g}-list-vertical`]: i
  });
  return y(/* @__PURE__ */ c.createElement("div", ve({}, d, {
    className: _,
    style: {
      ...m,
      ...p.style
    }
  }), r && /* @__PURE__ */ c.createElement($e.Title, {
    level: 5,
    className: F(`${g}-title`, p.classNames.title, f.title),
    style: {
      ...p.styles.title,
      ...u.title
    }
  }, r), /* @__PURE__ */ c.createElement("div", {
    className: $,
    style: {
      ...p.styles.list,
      ...u.list
    }
  }, o == null ? void 0 : o.map((b, I) => {
    const E = b.children && b.children.length > 0;
    return /* @__PURE__ */ c.createElement("div", {
      key: b.key || `key_${I}`,
      style: {
        ...p.styles.item,
        ...u.item
      },
      className: F(`${g}-item`, p.classNames.item, f.item, {
        [`${g}-item-disabled`]: b.disabled,
        [`${g}-item-has-nest`]: E
      }),
      onClick: () => {
        !E && s && s({
          data: b
        });
      }
    }, b.icon && /* @__PURE__ */ c.createElement("div", {
      className: `${g}-icon`
    }, b.icon), /* @__PURE__ */ c.createElement("div", {
      className: F(`${g}-content`, p.classNames.itemContent, f.itemContent),
      style: {
        ...p.styles.itemContent,
        ...u.itemContent
      }
    }, b.label && /* @__PURE__ */ c.createElement("h6", {
      className: `${g}-label`
    }, b.label), b.description && /* @__PURE__ */ c.createElement("p", {
      className: `${g}-desc`
    }, b.description), E && /* @__PURE__ */ c.createElement(Tr, {
      className: `${g}-nested`,
      items: b.children,
      vertical: !0,
      onItemClick: s,
      classNames: {
        list: f.subList,
        item: f.subItem
      },
      styles: {
        list: u.subList,
        item: u.subItem
      }
    })));
  }))));
}, hl = (e) => {
  const {
    componentCls: t,
    calc: r
  } = e, n = r(e.fontSizeHeading3).mul(e.lineHeightHeading3).equal(), o = r(e.fontSize).mul(e.lineHeight).equal();
  return {
    [t]: {
      gap: e.padding,
      // ======================== Icon ========================
      [`${t}-icon`]: {
        height: r(n).add(o).add(e.paddingXXS).equal(),
        display: "flex",
        img: {
          height: "100%"
        }
      },
      // ==================== Content Wrap ====================
      [`${t}-content-wrapper`]: {
        gap: e.paddingXS,
        flex: "auto",
        minWidth: 0,
        [`${t}-title-wrapper`]: {
          gap: e.paddingXS
        },
        [`${t}-title`]: {
          margin: 0
        },
        [`${t}-extra`]: {
          marginInlineStart: "auto"
        }
      }
    }
  };
}, yl = (e) => {
  const {
    componentCls: t
  } = e;
  return {
    [t]: {
      // ======================== Filled ========================
      "&-filled": {
        paddingInline: e.padding,
        paddingBlock: e.paddingSM,
        background: e.colorFillContent,
        borderRadius: e.borderRadiusLG
      },
      // ====================== Borderless ======================
      "&-borderless": {
        [`${t}-title`]: {
          fontSize: e.fontSizeHeading3,
          lineHeight: e.lineHeightHeading3
        }
      }
    }
  };
}, vl = () => ({}), bl = zt("Welcome", (e) => {
  const t = Ye(e, {});
  return [hl(t), yl(t)];
}, vl);
function Sl(e, t) {
  const {
    prefixCls: r,
    rootClassName: n,
    className: o,
    style: s,
    variant: i = "filled",
    // Semantic
    classNames: a = {},
    styles: l = {},
    // Layout
    icon: u,
    title: f,
    description: m,
    extra: d
  } = e, {
    direction: h,
    getPrefixCls: v
  } = Pe(), g = v("welcome", r), p = Ct("welcome"), [y, T, P] = bl(g), _ = c.useMemo(() => {
    if (!u)
      return null;
    let I = u;
    return typeof u == "string" && u.startsWith("http") && (I = /* @__PURE__ */ c.createElement("img", {
      src: u,
      alt: "icon"
    })), /* @__PURE__ */ c.createElement("div", {
      className: F(`${g}-icon`, p.classNames.icon, a.icon),
      style: l.icon
    }, I);
  }, [u]), $ = c.useMemo(() => f ? /* @__PURE__ */ c.createElement($e.Title, {
    level: 4,
    className: F(`${g}-title`, p.classNames.title, a.title),
    style: l.title
  }, f) : null, [f]), b = c.useMemo(() => d ? /* @__PURE__ */ c.createElement("div", {
    className: F(`${g}-extra`, p.classNames.extra, a.extra),
    style: l.extra
  }, d) : null, [d]);
  return y(/* @__PURE__ */ c.createElement(Ce, {
    ref: t,
    className: F(g, p.className, o, n, T, P, `${g}-${i}`, {
      [`${g}-rtl`]: h === "rtl"
    }),
    style: s
  }, _, /* @__PURE__ */ c.createElement(Ce, {
    vertical: !0,
    className: `${g}-content-wrapper`
  }, d ? /* @__PURE__ */ c.createElement(Ce, {
    align: "flex-start",
    className: `${g}-title-wrapper`
  }, $, b) : $, m && /* @__PURE__ */ c.createElement($e.Text, {
    className: F(`${g}-description`, p.classNames.description, a.description),
    style: l.description
  }, m))));
}
const xl = /* @__PURE__ */ c.forwardRef(Sl);
function te(e) {
  const t = J(e);
  return t.current = e, Fo((...r) => {
    var n;
    return (n = t.current) == null ? void 0 : n.call(t, ...r);
  }, []);
}
function be(e, t) {
  return Object.keys(e).reduce((r, n) => (e[n] !== void 0 && (!(t != null && t.omitNull) || e[n] !== null) && (r[n] = e[n]), r), {});
}
var wo = Symbol.for("immer-nothing"), En = Symbol.for("immer-draftable"), le = Symbol.for("immer-state");
function he(e, ...t) {
  throw new Error(`[Immer] minified error nr: ${e}. Full error at: https://bit.ly/3cXEKWf`);
}
var Ue = Object.getPrototypeOf;
function Ge(e) {
  return !!e && !!e[le];
}
function Ne(e) {
  var t;
  return e ? _o(e) || Array.isArray(e) || !!e[En] || !!((t = e.constructor) != null && t[En]) || Ht(e) || Bt(e) : !1;
}
var wl = Object.prototype.constructor.toString();
function _o(e) {
  if (!e || typeof e != "object") return !1;
  const t = Ue(e);
  if (t === null)
    return !0;
  const r = Object.hasOwnProperty.call(t, "constructor") && t.constructor;
  return r === Object ? !0 : typeof r == "function" && Function.toString.call(r) === wl;
}
function xt(e, t) {
  Dt(e) === 0 ? Reflect.ownKeys(e).forEach((r) => {
    t(r, e[r], e);
  }) : e.forEach((r, n) => t(n, r, e));
}
function Dt(e) {
  const t = e[le];
  return t ? t.type_ : Array.isArray(e) ? 1 : Ht(e) ? 2 : Bt(e) ? 3 : 0;
}
function mr(e, t) {
  return Dt(e) === 2 ? e.has(t) : Object.prototype.hasOwnProperty.call(e, t);
}
function Eo(e, t, r) {
  const n = Dt(e);
  n === 2 ? e.set(t, r) : n === 3 ? e.add(r) : e[t] = r;
}
function _l(e, t) {
  return e === t ? e !== 0 || 1 / e === 1 / t : e !== e && t !== t;
}
function Ht(e) {
  return e instanceof Map;
}
function Bt(e) {
  return e instanceof Set;
}
function Le(e) {
  return e.copy_ || e.base_;
}
function pr(e, t) {
  if (Ht(e))
    return new Map(e);
  if (Bt(e))
    return new Set(e);
  if (Array.isArray(e)) return Array.prototype.slice.call(e);
  const r = _o(e);
  if (t === !0 || t === "class_only" && !r) {
    const n = Object.getOwnPropertyDescriptors(e);
    delete n[le];
    let o = Reflect.ownKeys(n);
    for (let s = 0; s < o.length; s++) {
      const i = o[s], a = n[i];
      a.writable === !1 && (a.writable = !0, a.configurable = !0), (a.get || a.set) && (n[i] = {
        configurable: !0,
        writable: !0,
        // could live with !!desc.set as well here...
        enumerable: a.enumerable,
        value: e[i]
      });
    }
    return Object.create(Ue(e), n);
  } else {
    const n = Ue(e);
    if (n !== null && r)
      return {
        ...e
      };
    const o = Object.create(n);
    return Object.assign(o, e);
  }
}
function $r(e, t = !1) {
  return Wt(e) || Ge(e) || !Ne(e) || (Dt(e) > 1 && (e.set = e.add = e.clear = e.delete = El), Object.freeze(e), t && Object.entries(e).forEach(([r, n]) => $r(n, !0))), e;
}
function El() {
  he(2);
}
function Wt(e) {
  return Object.isFrozen(e);
}
var Cl = {};
function Fe(e) {
  const t = Cl[e];
  return t || he(0, e), t;
}
var tt;
function Co() {
  return tt;
}
function Tl(e, t) {
  return {
    drafts_: [],
    parent_: e,
    immer_: t,
    // Whenever the modified draft contains a draft from another scope, we
    // need to prevent auto-freezing so the unowned draft can be finalized.
    canAutoFreeze_: !0,
    unfinalizedDrafts_: 0
  };
}
function Cn(e, t) {
  t && (Fe("Patches"), e.patches_ = [], e.inversePatches_ = [], e.patchListener_ = t);
}
function gr(e) {
  hr(e), e.drafts_.forEach($l), e.drafts_ = null;
}
function hr(e) {
  e === tt && (tt = e.parent_);
}
function Tn(e) {
  return tt = Tl(tt, e);
}
function $l(e) {
  const t = e[le];
  t.type_ === 0 || t.type_ === 1 ? t.revoke_() : t.revoked_ = !0;
}
function $n(e, t) {
  t.unfinalizedDrafts_ = t.drafts_.length;
  const r = t.drafts_[0];
  return e !== void 0 && e !== r ? (r[le].modified_ && (gr(t), he(4)), Ne(e) && (e = wt(t, e), t.parent_ || _t(t, e)), t.patches_ && Fe("Patches").generateReplacementPatches_(r[le].base_, e, t.patches_, t.inversePatches_)) : e = wt(t, r, []), gr(t), t.patches_ && t.patchListener_(t.patches_, t.inversePatches_), e !== wo ? e : void 0;
}
function wt(e, t, r) {
  if (Wt(t)) return t;
  const n = t[le];
  if (!n)
    return xt(t, (o, s) => Pn(e, n, t, o, s, r)), t;
  if (n.scope_ !== e) return t;
  if (!n.modified_)
    return _t(e, n.base_, !0), n.base_;
  if (!n.finalized_) {
    n.finalized_ = !0, n.scope_.unfinalizedDrafts_--;
    const o = n.copy_;
    let s = o, i = !1;
    n.type_ === 3 && (s = new Set(o), o.clear(), i = !0), xt(s, (a, l) => Pn(e, n, o, a, l, r, i)), _t(e, o, !1), r && e.patches_ && Fe("Patches").generatePatches_(n, r, e.patches_, e.inversePatches_);
  }
  return n.copy_;
}
function Pn(e, t, r, n, o, s, i) {
  if (Ge(o)) {
    const a = s && t && t.type_ !== 3 && // Set objects are atomic since they have no keys.
    !mr(t.assigned_, n) ? s.concat(n) : void 0, l = wt(e, o, a);
    if (Eo(r, n, l), Ge(l))
      e.canAutoFreeze_ = !1;
    else return;
  } else i && r.add(o);
  if (Ne(o) && !Wt(o)) {
    if (!e.immer_.autoFreeze_ && e.unfinalizedDrafts_ < 1)
      return;
    wt(e, o), (!t || !t.scope_.parent_) && typeof n != "symbol" && Object.prototype.propertyIsEnumerable.call(r, n) && _t(e, o);
  }
}
function _t(e, t, r = !1) {
  !e.parent_ && e.immer_.autoFreeze_ && e.canAutoFreeze_ && $r(t, r);
}
function Pl(e, t) {
  const r = Array.isArray(e), n = {
    type_: r ? 1 : 0,
    // Track which produce call this is associated with.
    scope_: t ? t.scope_ : Co(),
    // True for both shallow and deep changes.
    modified_: !1,
    // Used during finalization.
    finalized_: !1,
    // Track which properties have been assigned (true) or deleted (false).
    assigned_: {},
    // The parent draft state.
    parent_: t,
    // The base state.
    base_: e,
    // The base proxy.
    draft_: null,
    // set below
    // The base copy with any updated values.
    copy_: null,
    // Called by the `produce` function.
    revoke_: null,
    isManual_: !1
  };
  let o = n, s = Pr;
  r && (o = [n], s = rt);
  const {
    revoke: i,
    proxy: a
  } = Proxy.revocable(o, s);
  return n.draft_ = a, n.revoke_ = i, a;
}
var Pr = {
  get(e, t) {
    if (t === le) return e;
    const r = Le(e);
    if (!mr(r, t))
      return Rl(e, r, t);
    const n = r[t];
    return e.finalized_ || !Ne(n) ? n : n === tr(e.base_, t) ? (rr(e), e.copy_[t] = vr(n, e)) : n;
  },
  has(e, t) {
    return t in Le(e);
  },
  ownKeys(e) {
    return Reflect.ownKeys(Le(e));
  },
  set(e, t, r) {
    const n = To(Le(e), t);
    if (n != null && n.set)
      return n.set.call(e.draft_, r), !0;
    if (!e.modified_) {
      const o = tr(Le(e), t), s = o == null ? void 0 : o[le];
      if (s && s.base_ === r)
        return e.copy_[t] = r, e.assigned_[t] = !1, !0;
      if (_l(r, o) && (r !== void 0 || mr(e.base_, t))) return !0;
      rr(e), yr(e);
    }
    return e.copy_[t] === r && // special case: handle new props with value 'undefined'
    (r !== void 0 || t in e.copy_) || // special case: NaN
    Number.isNaN(r) && Number.isNaN(e.copy_[t]) || (e.copy_[t] = r, e.assigned_[t] = !0), !0;
  },
  deleteProperty(e, t) {
    return tr(e.base_, t) !== void 0 || t in e.base_ ? (e.assigned_[t] = !1, rr(e), yr(e)) : delete e.assigned_[t], e.copy_ && delete e.copy_[t], !0;
  },
  // Note: We never coerce `desc.value` into an Immer draft, because we can't make
  // the same guarantee in ES5 mode.
  getOwnPropertyDescriptor(e, t) {
    const r = Le(e), n = Reflect.getOwnPropertyDescriptor(r, t);
    return n && {
      writable: !0,
      configurable: e.type_ !== 1 || t !== "length",
      enumerable: n.enumerable,
      value: r[t]
    };
  },
  defineProperty() {
    he(11);
  },
  getPrototypeOf(e) {
    return Ue(e.base_);
  },
  setPrototypeOf() {
    he(12);
  }
}, rt = {};
xt(Pr, (e, t) => {
  rt[e] = function() {
    return arguments[0] = arguments[0][0], t.apply(this, arguments);
  };
});
rt.deleteProperty = function(e, t) {
  return rt.set.call(this, e, t, void 0);
};
rt.set = function(e, t, r) {
  return Pr.set.call(this, e[0], t, r, e[0]);
};
function tr(e, t) {
  const r = e[le];
  return (r ? Le(r) : e)[t];
}
function Rl(e, t, r) {
  var o;
  const n = To(t, r);
  return n ? "value" in n ? n.value : (
    // This is a very special case, if the prop is a getter defined by the
    // prototype, we should invoke it with the draft as context!
    (o = n.get) == null ? void 0 : o.call(e.draft_)
  ) : void 0;
}
function To(e, t) {
  if (!(t in e)) return;
  let r = Ue(e);
  for (; r; ) {
    const n = Object.getOwnPropertyDescriptor(r, t);
    if (n) return n;
    r = Ue(r);
  }
}
function yr(e) {
  e.modified_ || (e.modified_ = !0, e.parent_ && yr(e.parent_));
}
function rr(e) {
  e.copy_ || (e.copy_ = pr(e.base_, e.scope_.immer_.useStrictShallowCopy_));
}
var Il = class {
  constructor(e) {
    this.autoFreeze_ = !0, this.useStrictShallowCopy_ = !1, this.produce = (t, r, n) => {
      if (typeof t == "function" && typeof r != "function") {
        const s = r;
        r = t;
        const i = this;
        return function(l = s, ...u) {
          return i.produce(l, (f) => r.call(this, f, ...u));
        };
      }
      typeof r != "function" && he(6), n !== void 0 && typeof n != "function" && he(7);
      let o;
      if (Ne(t)) {
        const s = Tn(this), i = vr(t, void 0);
        let a = !0;
        try {
          o = r(i), a = !1;
        } finally {
          a ? gr(s) : hr(s);
        }
        return Cn(s, n), $n(o, s);
      } else if (!t || typeof t != "object") {
        if (o = r(t), o === void 0 && (o = t), o === wo && (o = void 0), this.autoFreeze_ && $r(o, !0), n) {
          const s = [], i = [];
          Fe("Patches").generateReplacementPatches_(t, o, s, i), n(s, i);
        }
        return o;
      } else he(1, t);
    }, this.produceWithPatches = (t, r) => {
      if (typeof t == "function")
        return (i, ...a) => this.produceWithPatches(i, (l) => t(l, ...a));
      let n, o;
      return [this.produce(t, r, (i, a) => {
        n = i, o = a;
      }), n, o];
    }, typeof (e == null ? void 0 : e.autoFreeze) == "boolean" && this.setAutoFreeze(e.autoFreeze), typeof (e == null ? void 0 : e.useStrictShallowCopy) == "boolean" && this.setUseStrictShallowCopy(e.useStrictShallowCopy);
  }
  createDraft(e) {
    Ne(e) || he(8), Ge(e) && (e = Ml(e));
    const t = Tn(this), r = vr(e, void 0);
    return r[le].isManual_ = !0, hr(t), r;
  }
  finishDraft(e, t) {
    const r = e && e[le];
    (!r || !r.isManual_) && he(9);
    const {
      scope_: n
    } = r;
    return Cn(n, t), $n(void 0, n);
  }
  /**
   * Pass true to automatically freeze all copies created by Immer.
   *
   * By default, auto-freezing is enabled.
   */
  setAutoFreeze(e) {
    this.autoFreeze_ = e;
  }
  /**
   * Pass true to enable strict shallow copy.
   *
   * By default, immer does not copy the object descriptors such as getter, setter and non-enumrable properties.
   */
  setUseStrictShallowCopy(e) {
    this.useStrictShallowCopy_ = e;
  }
  applyPatches(e, t) {
    let r;
    for (r = t.length - 1; r >= 0; r--) {
      const o = t[r];
      if (o.path.length === 0 && o.op === "replace") {
        e = o.value;
        break;
      }
    }
    r > -1 && (t = t.slice(r + 1));
    const n = Fe("Patches").applyPatches_;
    return Ge(e) ? n(e, t) : this.produce(e, (o) => n(o, t));
  }
};
function vr(e, t) {
  const r = Ht(e) ? Fe("MapSet").proxyMap_(e, t) : Bt(e) ? Fe("MapSet").proxySet_(e, t) : Pl(e, t);
  return (t ? t.scope_ : Co()).drafts_.push(r), r;
}
function Ml(e) {
  return Ge(e) || he(10, e), $o(e);
}
function $o(e) {
  if (!Ne(e) || Wt(e)) return e;
  const t = e[le];
  let r;
  if (t) {
    if (!t.modified_) return t.base_;
    t.finalized_ = !0, r = pr(e, t.scope_.immer_.useStrictShallowCopy_);
  } else
    r = pr(e, !0);
  return xt(r, (n, o) => {
    Eo(r, n, $o(o));
  }), t && (t.finalized_ = !1), r;
}
var ce = new Il(), Rn = ce.produce;
ce.produceWithPatches.bind(ce);
ce.setAutoFreeze.bind(ce);
ce.setUseStrictShallowCopy.bind(ce);
ce.applyPatches.bind(ce);
ce.createDraft.bind(ce);
ce.finishDraft.bind(ce);
const {
  useItems: vc,
  withItemsContextProvider: bc,
  ItemHandler: Sc
} = An("antdx-bubble.list-items"), {
  useItems: Ll,
  withItemsContextProvider: Ol,
  ItemHandler: xc
} = An("antdx-bubble.list-roles");
function jl(e) {
  return /^(?:async\s+)?(?:function\s*(?:\w*\s*)?\(|\([\w\s,=]*\)\s*=>|\(\{[\w\s,=]*\}\)\s*=>|function\s*\*\s*\w*\s*\()/i.test(e.trim());
}
function Nl(e, t = !1) {
  try {
    if (Sr(e))
      return e;
    if (t && !jl(e))
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
function Fl(e, t) {
  return fe(() => Nl(e, t), [e, t]);
}
function kl(e, t) {
  return t((n, o) => Sr(n) ? o ? (...s) => ye(o) && o.unshift ? n(...e, ...s) : n(...s, ...e) : n(...e) : n);
}
const Al = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function zl(e) {
  return e ? Object.keys(e).reduce((t, r) => {
    const n = e[r];
    return t[r] = Dl(r, n), t;
  }, {}) : {};
}
function Dl(e, t) {
  return typeof t == "number" && !Al.includes(e) ? t + "px" : t;
}
function br(e) {
  const t = [], r = e.cloneNode(!1);
  if (e._reactElement) {
    const o = c.Children.toArray(e._reactElement.props.children).map((s) => {
      if (c.isValidElement(s) && s.props.__slot__) {
        const {
          portals: i,
          clonedElement: a
        } = br(s.props.el);
        return c.cloneElement(s, {
          ...s.props,
          el: a,
          children: [...c.Children.toArray(s.props.children), ...i]
        });
      }
      return null;
    });
    return o.originalChildren = e._reactElement.props.children, t.push(yt(c.cloneElement(e._reactElement, {
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
      type: a,
      useCapture: l
    }) => {
      r.addEventListener(a, i, l);
    });
  });
  const n = Array.from(e.childNodes);
  for (let o = 0; o < n.length; o++) {
    const s = n[o];
    if (s.nodeType === 1) {
      const {
        clonedElement: i,
        portals: a
      } = br(s);
      t.push(...a), r.appendChild(i);
    } else s.nodeType === 3 && r.appendChild(s.cloneNode());
  }
  return {
    clonedElement: r,
    portals: t
  };
}
function Hl(e, t) {
  e && (typeof e == "function" ? e(t) : e.current = t);
}
const In = ko(({
  slot: e,
  clone: t,
  className: r,
  style: n,
  observeAttributes: o
}, s) => {
  const i = J(), [a, l] = Ze([]), {
    forceClone: u
  } = ys(), f = u ? !0 : t;
  return Ee(() => {
    var g;
    if (!i.current || !e)
      return;
    let m = e;
    function d() {
      let p = m;
      if (m.tagName.toLowerCase() === "svelte-slot" && m.children.length === 1 && m.children[0] && (p = m.children[0], p.tagName.toLowerCase() === "react-portal-target" && p.children[0] && (p = p.children[0])), Hl(s, p), r && p.classList.add(...r.split(" ")), n) {
        const y = zl(n);
        Object.keys(y).forEach((T) => {
          p.style[T] = y[T];
        });
      }
    }
    let h = null, v = null;
    if (f && window.MutationObserver) {
      let p = function() {
        var _, $, b;
        (_ = i.current) != null && _.contains(m) && (($ = i.current) == null || $.removeChild(m));
        const {
          portals: T,
          clonedElement: P
        } = br(e);
        m = P, l(T), m.style.display = "contents", v && clearTimeout(v), v = setTimeout(() => {
          d();
        }, 50), (b = i.current) == null || b.appendChild(m);
      };
      p();
      const y = Ls(() => {
        p(), h == null || h.disconnect(), h == null || h.observe(e, {
          childList: !0,
          subtree: !0,
          attributes: o
        });
      }, 50);
      h = new window.MutationObserver(y), h.observe(e, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      m.style.display = "contents", d(), (g = i.current) == null || g.appendChild(m);
    return () => {
      var p, y;
      m.style.display = "", (p = i.current) != null && p.contains(m) && ((y = i.current) == null || y.removeChild(m)), h == null || h.disconnect();
    };
  }, [e, f, r, n, s, o, u]), c.createElement("react-child", {
    ref: i,
    style: {
      display: "contents"
    }
  }, ...a);
}), Bl = ({
  children: e,
  ...t
}) => /* @__PURE__ */ S.jsx(S.Fragment, {
  children: e(t)
});
function Wl(e) {
  return c.createElement(Bl, {
    children: e
  });
}
function Po(e, t, r) {
  const n = e.filter(Boolean);
  if (n.length !== 0)
    return n.map((o, s) => {
      var u;
      if (typeof o != "object")
        return t != null && t.fallback ? t.fallback(o) : o;
      const i = {
        ...o.props,
        key: ((u = o.props) == null ? void 0 : u.key) ?? (r ? `${r}-${s}` : `${s}`)
      };
      let a = i;
      Object.keys(o.slots).forEach((f) => {
        if (!o.slots[f] || !(o.slots[f] instanceof Element) && !o.slots[f].el)
          return;
        const m = f.split(".");
        m.forEach((y, T) => {
          a[y] || (a[y] = {}), T !== m.length - 1 && (a = i[y]);
        });
        const d = o.slots[f];
        let h, v, g = (t == null ? void 0 : t.clone) ?? !1, p = t == null ? void 0 : t.forceClone;
        d instanceof Element ? h = d : (h = d.el, v = d.callback, g = d.clone ?? g, p = d.forceClone ?? p), p = p ?? !!v, a[m[m.length - 1]] = h ? v ? (...y) => (v(m[m.length - 1], y), /* @__PURE__ */ S.jsx(Dr, {
          ...o.ctx,
          params: y,
          forceClone: p,
          children: /* @__PURE__ */ S.jsx(In, {
            slot: h,
            clone: g
          })
        })) : Wl((y) => /* @__PURE__ */ S.jsx(Dr, {
          ...o.ctx,
          forceClone: p,
          children: /* @__PURE__ */ S.jsx(In, {
            ...y,
            slot: h,
            clone: g
          })
        })) : a[m[m.length - 1]], a = i;
      });
      const l = (t == null ? void 0 : t.children) || "children";
      return o[l] ? i[l] = Po(o[l], t, `${s}`) : t != null && t.children && (i[l] = void 0, Reflect.deleteProperty(i, l)), i;
    });
}
const Ro = Symbol();
function Vl(e, t) {
  return kl(t, (r) => {
    var n, o;
    return {
      ...e,
      avatar: Sr(e.avatar) ? r(e.avatar) : ye(e.avatar) ? {
        ...e.avatar,
        icon: r((n = e.avatar) == null ? void 0 : n.icon),
        src: r((o = e.avatar) == null ? void 0 : o.src)
      } : e.avatar,
      footer: r(e.footer, {
        unshift: !0
      }),
      header: r(e.header, {
        unshift: !0
      }),
      loadingRender: r(e.loadingRender, !0),
      messageRender: r(e.messageRender, !0)
    };
  });
}
function Xl({
  roles: e,
  preProcess: t,
  postProcess: r
}, n = []) {
  const o = Fl(e), s = te(t), i = te(r), {
    items: {
      roles: a
    }
  } = Ll(), l = fe(() => {
    var f;
    return e || ((f = Po(a, {
      clone: !0,
      forceClone: !0
    })) == null ? void 0 : f.reduce((m, d) => (d.role !== void 0 && (m[d.role] = d), m), {}));
  }, [a, e]), u = fe(() => (f, m) => {
    const d = m ?? f[Ro], h = s(f, d) || f;
    if (h.role && (l || {})[h.role])
      return Vl((l || {})[h.role], [h, d]);
    let v;
    return v = i(h, d), v || {
      messageRender(g) {
        return /* @__PURE__ */ S.jsx(S.Fragment, {
          children: ye(g) ? JSON.stringify(g) : g
        });
      }
    };
  }, [l, i, s, ...n]);
  return o || u;
}
function Ul(e) {
  const [t, r] = Ze(!1), n = J(0), o = J(!0), s = J(!0), {
    autoScroll: i,
    scrollButtonOffset: a,
    ref: l,
    value: u
  } = e, f = te((d = "instant") => {
    l.current && (s.current = !0, requestAnimationFrame(() => {
      var h;
      (h = l.current) == null || h.scrollTo({
        offset: l.current.nativeElement.scrollHeight,
        behavior: d
      });
    }), r(!1));
  }), m = te((d = 100) => {
    if (!l.current)
      return !1;
    const h = l.current.nativeElement, v = h.scrollHeight, {
      scrollTop: g,
      clientHeight: p
    } = h;
    return v - (g + p) < d;
  });
  return Ee(() => {
    l.current && i && (u.length !== n.current && (o.current = !0), o.current && requestAnimationFrame(() => {
      f();
    }), n.current = u.length);
  }, [u, l, i, f, m]), Ee(() => {
    if (l.current && i) {
      const d = l.current.nativeElement;
      let h = 0, v = 0;
      const g = (p) => {
        const y = p.target;
        s.current ? s.current = !1 : y.scrollTop < h && y.scrollHeight >= v ? o.current = !1 : m() && (o.current = !0), h = y.scrollTop, v = y.scrollHeight, r(!m(a));
      };
      return d.addEventListener("scroll", g), () => {
        d.removeEventListener("scroll", g);
      };
    }
  }, [i, m, a]), {
    showScrollButton: t,
    scrollToBottom: f
  };
}
new Intl.Collator(0, {
  numeric: 1
}).compare;
typeof process < "u" && process.versions && process.versions.node;
var _e;
class wc extends TransformStream {
  /** Constructs a new instance. */
  constructor(r = {
    allowCR: !1
  }) {
    super({
      transform: (n, o) => {
        for (n = He(this, _e) + n; ; ) {
          const s = n.indexOf(`
`), i = r.allowCR ? n.indexOf("\r") : -1;
          if (i !== -1 && i !== n.length - 1 && (s === -1 || s - 1 > i)) {
            o.enqueue(n.slice(0, i)), n = n.slice(i + 1);
            continue;
          }
          if (s === -1) break;
          const a = n[s - 1] === "\r" ? s - 1 : s;
          o.enqueue(n.slice(0, a)), n = n.slice(s + 1);
        }
        kr(this, _e, n);
      },
      flush: (n) => {
        if (He(this, _e) === "") return;
        const o = r.allowCR && He(this, _e).endsWith("\r") ? He(this, _e).slice(0, -1) : He(this, _e);
        n.enqueue(o);
      }
    });
    Fr(this, _e, "");
  }
}
_e = new WeakMap();
function Gl(e) {
  try {
    const t = new URL(e);
    return t.protocol === "http:" || t.protocol === "https:";
  } catch {
    return !1;
  }
}
function Kl() {
  const e = document.querySelector(".gradio-container");
  if (!e)
    return "";
  const t = e.className.match(/gradio-container-(.+)/);
  return t ? t[1] : "";
}
const ql = +Kl()[0];
function nt(e, t, r) {
  const n = ql >= 5 ? "gradio_api/" : "";
  return e == null ? r ? `/proxy=${r}${n}file=` : `${t}${n}file=` : Gl(e) ? e : r ? `/proxy=${r}${n}file=${e}` : `${t}/${n}file=${e}`;
}
const Yl = (e) => !!e.url;
function Io(e, t, r) {
  if (e)
    return Yl(e) ? e.url : typeof e == "string" ? e.startsWith("http") ? e : nt(e, t, r) : e;
}
const Ql = ({
  options: e,
  urlProxyUrl: t,
  urlRoot: r,
  onWelcomePromptSelect: n
}) => {
  var a;
  const {
    prompts: o,
    ...s
  } = e, i = fe(() => be(o || {}, {
    omitNull: !0
  }), [o]);
  return /* @__PURE__ */ S.jsxs(Ce, {
    vertical: !0,
    gap: "middle",
    children: [/* @__PURE__ */ S.jsx(xl, {
      ...s,
      icon: Io(s.icon, r, t),
      styles: {
        ...s == null ? void 0 : s.styles,
        icon: {
          flexShrink: 0,
          ...(a = s == null ? void 0 : s.styles) == null ? void 0 : a.icon
        }
      },
      classNames: s.class_names,
      className: F(s.elem_classes),
      style: s.elem_style
    }), /* @__PURE__ */ S.jsx(Tr, {
      ...i,
      classNames: i == null ? void 0 : i.class_names,
      className: F(i == null ? void 0 : i.elem_classes),
      style: i == null ? void 0 : i.elem_style,
      onItemClick: ({
        data: l
      }) => {
        n({
          value: l
        });
      }
    })]
  });
}, Mn = Symbol(), Ln = Symbol(), On = Symbol(), jn = Symbol(), Zl = (e) => e ? typeof e == "string" ? {
  src: e
} : ((r) => !!r.url)(e) ? {
  src: e.url
} : e.src ? {
  ...e,
  src: typeof e.src == "string" ? e.src : e.src.url
} : e : void 0, Jl = (e) => typeof e == "string" ? [{
  type: "text",
  content: e
}] : Array.isArray(e) ? e.map((t) => typeof t == "string" ? {
  type: "text",
  content: t
} : t) : ye(e) ? [e] : [], ec = (e, t) => {
  if (typeof e == "string")
    return t[0];
  if (Array.isArray(e)) {
    const r = [...e];
    return Object.keys(t).forEach((n) => {
      const o = r[n];
      typeof o == "string" ? r[n] = t[n] : r[n] = {
        ...o,
        content: t[n]
      };
    }), r;
  }
  return ye(e) ? {
    ...e,
    content: t[0]
  } : e;
}, Mo = (e, t, r) => typeof e == "string" ? e : Array.isArray(e) ? e.map((n) => Mo(n, t, r)).filter(Boolean).join(`
`) : ye(e) ? e.copyable ?? !0 ? typeof e.content == "string" ? e.content : e.type === "file" ? JSON.stringify(e.content.map((n) => Io(n, t, r))) : JSON.stringify(e.content) : "" : JSON.stringify(e), Lo = (e, t) => (e || []).map((r) => ({
  ...t(r),
  children: Array.isArray(r.children) ? Lo(r.children, t) : void 0
})), tc = ({
  content: e,
  className: t,
  style: r,
  disabled: n,
  urlRoot: o,
  urlProxyUrl: s,
  onCopy: i
}) => {
  const a = fe(() => Mo(e, o, s), [e, s, o]), l = J(null);
  return /* @__PURE__ */ S.jsx($e.Text, {
    copyable: {
      tooltips: !1,
      onCopy() {
        i == null || i(a);
      },
      text: a,
      icon: [/* @__PURE__ */ S.jsx(re, {
        ref: l,
        variant: "text",
        color: "default",
        disabled: n,
        size: "small",
        className: t,
        style: r,
        icon: /* @__PURE__ */ S.jsx(is, {})
      }, "copy"), /* @__PURE__ */ S.jsx(re, {
        variant: "text",
        color: "default",
        size: "small",
        disabled: n,
        className: t,
        style: r,
        icon: /* @__PURE__ */ S.jsx(Fn, {})
      }, "copied")]
    }
  });
}, rc = ({
  action: e,
  disabledActions: t,
  message: r,
  onCopy: n,
  onDelete: o,
  onEdit: s,
  onLike: i,
  onRetry: a,
  urlRoot: l,
  urlProxyUrl: u
}) => {
  var h;
  const f = J(), d = (() => {
    var y, T;
    const {
      action: v,
      disabled: g,
      disableHandler: p
    } = ye(e) ? {
      action: e.action,
      disabled: (t == null ? void 0 : t.includes(e.action)) || !!e.disabled,
      disableHandler: !!e.popconfirm
    } : {
      action: e,
      disabled: (t == null ? void 0 : t.includes(e)) || !1,
      disableHandler: !1
    };
    switch (v) {
      case "copy":
        return /* @__PURE__ */ S.jsx(tc, {
          disabled: g,
          content: r.content,
          onCopy: n,
          urlRoot: l,
          urlProxyUrl: u
        });
      case "like":
        return f.current = () => i(!0), /* @__PURE__ */ S.jsx(re, {
          variant: "text",
          color: ((y = r.meta) == null ? void 0 : y.feedback) === "like" ? "primary" : "default",
          disabled: g,
          size: "small",
          icon: /* @__PURE__ */ S.jsx(ss, {}),
          onClick: () => {
            !p && i(!0);
          }
        });
      case "dislike":
        return f.current = () => i(!1), /* @__PURE__ */ S.jsx(re, {
          variant: "text",
          color: ((T = r.meta) == null ? void 0 : T.feedback) === "dislike" ? "primary" : "default",
          size: "small",
          icon: /* @__PURE__ */ S.jsx(os, {}),
          disabled: g,
          onClick: () => !p && i(!1)
        });
      case "retry":
        return f.current = a, /* @__PURE__ */ S.jsx(re, {
          variant: "text",
          color: "default",
          size: "small",
          disabled: g,
          icon: /* @__PURE__ */ S.jsx(ns, {}),
          onClick: () => !p && a()
        });
      case "edit":
        return f.current = s, /* @__PURE__ */ S.jsx(re, {
          variant: "text",
          color: "default",
          size: "small",
          disabled: g,
          icon: /* @__PURE__ */ S.jsx(rs, {}),
          onClick: () => !p && s()
        });
      case "delete":
        return f.current = o, /* @__PURE__ */ S.jsx(re, {
          variant: "text",
          color: "default",
          size: "small",
          disabled: g,
          icon: /* @__PURE__ */ S.jsx(ts, {}),
          onClick: () => !p && o()
        });
      default:
        return null;
    }
  })();
  if (ye(e)) {
    const v = {
      ...typeof e.popconfirm == "string" ? {
        title: e.popconfirm
      } : {
        ...e.popconfirm,
        title: (h = e.popconfirm) == null ? void 0 : h.title
      },
      onConfirm() {
        var g;
        (g = f.current) == null || g.call(f);
      }
    };
    return c.createElement(e.popconfirm ? ms : c.Fragment, e.popconfirm ? v : void 0, c.createElement(e.tooltip ? ps : c.Fragment, e.tooltip ? typeof e.tooltip == "string" ? {
      title: e.tooltip
    } : e.tooltip : void 0, d));
  }
  return d;
}, nc = ({
  isEditing: e,
  onEditCancel: t,
  onEditConfirm: r,
  onCopy: n,
  onEdit: o,
  onLike: s,
  onDelete: i,
  onRetry: a,
  editValues: l,
  message: u,
  extra: f,
  index: m,
  actions: d,
  disabledActions: h,
  urlRoot: v,
  urlProxyUrl: g
}) => e ? /* @__PURE__ */ S.jsxs(Ce, {
  justify: "end",
  children: [/* @__PURE__ */ S.jsx(re, {
    variant: "text",
    color: "default",
    size: "small",
    icon: /* @__PURE__ */ S.jsx(es, {}),
    onClick: () => {
      t == null || t();
    }
  }), /* @__PURE__ */ S.jsx(re, {
    variant: "text",
    color: "default",
    size: "small",
    icon: /* @__PURE__ */ S.jsx(Fn, {}),
    onClick: () => {
      const p = ec(u.content, l);
      r == null || r({
        index: m,
        value: p,
        previous_value: u.content
      });
    }
  })]
}) : /* @__PURE__ */ S.jsx(Ce, {
  justify: "space-between",
  align: "center",
  gap: f && (d != null && d.length) ? "small" : void 0,
  children: (u.role === "user" ? ["extra", "actions"] : ["actions", "extra"]).map((p) => {
    switch (p) {
      case "extra":
        return /* @__PURE__ */ S.jsx($e.Text, {
          type: "secondary",
          children: f
        }, "extra");
      case "actions":
        return /* @__PURE__ */ S.jsx("div", {
          children: (d || []).map((y, T) => /* @__PURE__ */ S.jsx(rc, {
            urlRoot: v,
            urlProxyUrl: g,
            action: y,
            disabledActions: h,
            message: u,
            onCopy: (P) => n({
              value: P,
              index: m
            }),
            onDelete: () => i({
              index: m,
              value: u.content
            }),
            onEdit: () => o(m),
            onLike: (P) => s == null ? void 0 : s({
              value: u.content,
              liked: P,
              index: m
            }),
            onRetry: () => a == null ? void 0 : a({
              index: m,
              value: u.content
            })
          }, `${y}-${T}`))
        }, "actions");
    }
  })
}), oc = ({
  markdownConfig: e,
  title: t
}) => t ? e.renderMarkdown ? /* @__PURE__ */ S.jsx(vt, {
  ...e,
  value: t
}) : /* @__PURE__ */ S.jsx(S.Fragment, {
  children: t
}) : null, sc = ({
  item: e,
  urlRoot: t,
  urlProxyUrl: r,
  ...n
}) => {
  const o = fe(() => e ? typeof e == "string" ? {
    url: e.startsWith("http") ? e : nt(e, t, r),
    uid: e,
    name: e.split("/").pop()
  } : {
    ...e,
    uid: e.uid || e.path || e.url,
    name: e.name || e.orig_name || (e.url || e.path).split("/").pop(),
    url: e.url || nt(e.path, t, r)
  } : {}, [e, r, t]);
  return /* @__PURE__ */ S.jsx(bo.FileCard, {
    ...n,
    imageProps: {
      ...n.imageProps
      // fixed in @ant-design/x@1.2.0
      // wrapperStyle: {
      //   width: '100%',
      //   height: '100%',
      //   ...props.imageProps?.wrapperStyle,
      // },
      // style: {
      //   width: '100%',
      //   height: '100%',
      //   objectFit: 'contain',
      //   borderRadius: token.borderRadius,
      //   ...props.imageProps?.style,
      // },
    },
    item: o
  });
}, ic = ["png", "jpg", "jpeg", "gif", "bmp", "webp", "svg"];
function ac(e, t) {
  return t.some((r) => e.toLowerCase() === `.${r}`);
}
const lc = (e, t, r) => e ? typeof e == "string" ? {
  url: e.startsWith("http") ? e : nt(e, t, r),
  uid: e,
  name: e.split("/").pop()
} : {
  ...e,
  uid: e.uid || e.path || e.url,
  name: e.name || e.orig_name || (e.url || e.path).split("/").pop(),
  url: e.url || nt(e.path, t, r)
} : {}, cc = ({
  children: e,
  item: t
}) => {
  const {
    token: r
  } = Je.useToken(), n = fe(() => {
    const o = t.name || "", s = o.match(/^(.*)\.[^.]+$/), i = s ? o.slice(s[1].length) : "";
    return ac(i, ic);
  }, [t.name]);
  return /* @__PURE__ */ S.jsx("div", {
    className: "ms-gr-pro-chatbot-message-file-message-container",
    style: {
      borderRadius: r.borderRadius
    },
    children: n ? /* @__PURE__ */ S.jsxs(S.Fragment, {
      children: [" ", e]
    }) : /* @__PURE__ */ S.jsxs(S.Fragment, {
      children: [e, /* @__PURE__ */ S.jsx("div", {
        className: "ms-gr-pro-chatbot-message-file-message-toolbar",
        style: {
          backgroundColor: r.colorBgMask,
          zIndex: r.zIndexPopupBase,
          borderRadius: r.borderRadius
        },
        children: /* @__PURE__ */ S.jsx(re, {
          icon: /* @__PURE__ */ S.jsx(as, {
            style: {
              color: r.colorWhite
            }
          }),
          variant: "link",
          color: "default",
          size: "small",
          href: t.url,
          target: "_blank",
          rel: "noopener noreferrer"
        })
      })]
    })
  });
}, uc = ({
  value: e,
  urlProxyUrl: t,
  urlRoot: r,
  options: n
}) => {
  const {
    imageProps: o
  } = n;
  return /* @__PURE__ */ S.jsx(Ce, {
    gap: "small",
    wrap: !0,
    ...n,
    className: "ms-gr-pro-chatbot-message-file-message",
    children: e == null ? void 0 : e.map((s, i) => {
      const a = lc(s, r, t);
      return /* @__PURE__ */ S.jsx(cc, {
        item: a,
        children: /* @__PURE__ */ S.jsx(sc, {
          item: a,
          urlRoot: r,
          urlProxyUrl: t,
          imageProps: o
        })
      }, `${a.uid}-${i}`);
    })
  });
}, fc = ({
  value: e,
  options: t,
  onItemClick: r
}) => {
  const {
    elem_style: n,
    elem_classes: o,
    class_names: s,
    styles: i,
    ...a
  } = t;
  return /* @__PURE__ */ S.jsx(Tr, {
    ...a,
    classNames: s,
    className: F(o),
    style: n,
    styles: i,
    items: e,
    onItemClick: ({
      data: l
    }) => {
      r(l);
    }
  });
}, Nn = ({
  value: e,
  options: t
}) => {
  const {
    renderMarkdown: r,
    ...n
  } = t;
  return /* @__PURE__ */ S.jsx(S.Fragment, {
    children: r ? /* @__PURE__ */ S.jsx(vt, {
      ...n,
      value: e
    }) : e
  });
}, dc = ({
  value: e,
  options: t
}) => {
  const {
    renderMarkdown: r,
    status: n,
    title: o,
    ...s
  } = t, [i, a] = Ze(() => n !== "done");
  return Ee(() => {
    a(n !== "done");
  }, [n]), /* @__PURE__ */ S.jsx(S.Fragment, {
    children: /* @__PURE__ */ S.jsx(gs, {
      activeKey: i ? ["tool"] : [],
      onChange: () => {
        a(!i);
      },
      items: [{
        key: "tool",
        label: r ? /* @__PURE__ */ S.jsx(vt, {
          ...s,
          value: o
        }) : o,
        children: r ? /* @__PURE__ */ S.jsx(vt, {
          ...s,
          value: e
        }) : e
      }]
    })
  });
}, mc = ["text", "tool"], pc = ({
  isEditing: e,
  index: t,
  message: r,
  isLastMessage: n,
  markdownConfig: o,
  onEdit: s,
  onSuggestionSelect: i,
  urlProxyUrl: a,
  urlRoot: l
}) => {
  const u = J(null), f = () => Jl(r.content).map((d, h) => {
    const v = () => {
      var g;
      if (e && (d.editable ?? !0) && mc.includes(d.type)) {
        const p = d.content, y = (g = u.current) == null ? void 0 : g.getBoundingClientRect().width;
        return /* @__PURE__ */ S.jsx("div", {
          style: {
            width: y,
            minWidth: 200,
            maxWidth: "100%"
          },
          children: /* @__PURE__ */ S.jsx(hs.TextArea, {
            autoSize: {
              minRows: 1,
              maxRows: 10
            },
            defaultValue: p,
            onChange: (T) => {
              s(h, T.target.value);
            }
          })
        });
      }
      switch (d.type) {
        case "text":
          return /* @__PURE__ */ S.jsx(Nn, {
            value: d.content,
            options: be({
              ...o,
              ...pt(d.options)
            }, {
              omitNull: !0
            })
          });
        case "tool":
          return /* @__PURE__ */ S.jsx(dc, {
            value: d.content,
            options: be({
              ...o,
              ...pt(d.options)
            }, {
              omitNull: !0
            })
          });
        case "file":
          return /* @__PURE__ */ S.jsx(uc, {
            value: d.content,
            urlRoot: l,
            urlProxyUrl: a,
            options: be(d.options || {}, {
              omitNull: !0
            })
          });
        case "suggestion":
          return /* @__PURE__ */ S.jsx(fc, {
            value: n ? d.content : Lo(d.content, (p) => ({
              ...p,
              disabled: p.disabled ?? !0
            })),
            options: be(d.options || {}, {
              omitNull: !0
            }),
            onItemClick: (p) => {
              i({
                index: t,
                value: p
              });
            }
          });
        default:
          return typeof d.content != "string" ? null : /* @__PURE__ */ S.jsx(Nn, {
            value: d.content,
            options: be({
              ...o,
              ...pt(d.options)
            }, {
              omitNull: !0
            })
          });
      }
    };
    return /* @__PURE__ */ S.jsx(c.Fragment, {
      children: v()
    }, h);
  });
  return /* @__PURE__ */ S.jsx("div", {
    ref: u,
    children: /* @__PURE__ */ S.jsx(Ce, {
      vertical: !0,
      gap: "small",
      children: f()
    })
  });
}, _c = si(Ol(["roles"], ({
  id: e,
  className: t,
  style: r,
  height: n,
  minHeight: o,
  maxHeight: s,
  value: i,
  roles: a,
  urlRoot: l,
  urlProxyUrl: u,
  themeMode: f,
  autoScroll: m = !0,
  showScrollToBottomButton: d = !0,
  scrollToBottomButtonOffset: h = 200,
  markdownConfig: v,
  welcomeConfig: g,
  userConfig: p,
  botConfig: y,
  onValueChange: T,
  onCopy: P,
  onChange: _,
  onEdit: $,
  onRetry: b,
  onDelete: I,
  onLike: E,
  onSuggestionSelect: O,
  onWelcomePromptSelect: L
}) => {
  const j = fe(() => ({
    variant: "borderless",
    ...g ? be(g, {
      omitNull: !0
    }) : {}
  }), [g]), M = fe(() => ({
    lineBreaks: !0,
    renderMarkdown: !0,
    ...pt(v),
    urlRoot: l,
    themeMode: f
  }), [v, f, l]), x = fe(() => p ? be(p, {
    omitNull: !0
  }) : {}, [p]), w = fe(() => y ? be(y, {
    omitNull: !0
  }) : {}, [y]), k = fe(() => {
    const C = (i || []).map((K, V) => {
      const pe = V === i.length - 1, ue = be(K, {
        omitNull: !0
      });
      return {
        ...zr(ue, ["header", "footer", "avatar"]),
        [Ro]: V,
        [Mn]: ue.header,
        [Ln]: ue.footer,
        [On]: ue.avatar,
        [jn]: pe,
        key: ue.key ?? `${V}`
      };
    }).filter((K) => K.role !== "system");
    return C.length > 0 ? C : [{
      role: "chatbot-internal-welcome"
    }];
  }, [i]), A = J(null), [D, B] = Ze(-1), [oe, se] = Ze({}), X = J(), W = te((C, K) => {
    se((V) => ({
      ...V,
      [C]: K
    }));
  }), G = te(_);
  Ee(() => {
    Os(X.current, i) || (G(), X.current = i);
  }, [i, G]);
  const U = te((C) => {
    O == null || O(C);
  }), q = te((C) => {
    L == null || L(C);
  }), ie = te((C) => {
    b == null || b(C);
  }), ee = te((C) => {
    B(C);
  }), xe = te(() => {
    B(-1);
  }), ke = te((C) => {
    B(-1), T([...i.slice(0, C.index), {
      ...i[C.index],
      content: C.value
    }, ...i.slice(C.index + 1)]), $ == null || $(C);
  }), Ae = te((C) => {
    P == null || P(C);
  }), ze = te((C) => {
    E == null || E(C), T(Rn(i, (K) => {
      const V = K[C.index].meta || {}, pe = C.liked ? "like" : "dislike";
      K[C.index] = {
        ...K[C.index],
        meta: {
          ...V,
          feedback: V.feedback === pe ? null : pe
        }
      };
    }));
  }), we = te((C) => {
    T(Rn(i, (K) => {
      K.splice(C.index, 1);
    })), I == null || I(C);
  }), De = Xl({
    roles: a,
    preProcess(C, K) {
      var pe, ue, Z, Y, ae, Ie, Me, Rr, Ir, Mr, Lr, Or;
      const V = C.role === "user";
      return {
        ...C,
        style: C.elem_style,
        className: F(C.elem_classes, "ms-gr-pro-chatbot-message"),
        classNames: {
          ...C.class_names,
          avatar: F(V ? (pe = x == null ? void 0 : x.class_names) == null ? void 0 : pe.avatar : (ue = w == null ? void 0 : w.class_names) == null ? void 0 : ue.avatar, (Z = C.class_names) == null ? void 0 : Z.avatar, "ms-gr-pro-chatbot-message-avatar"),
          header: F(V ? (Y = x == null ? void 0 : x.class_names) == null ? void 0 : Y.header : (ae = w == null ? void 0 : w.class_names) == null ? void 0 : ae.header, (Ie = C.class_names) == null ? void 0 : Ie.header, "ms-gr-pro-chatbot-message-header"),
          footer: F(V ? (Me = x == null ? void 0 : x.class_names) == null ? void 0 : Me.footer : (Rr = w == null ? void 0 : w.class_names) == null ? void 0 : Rr.footer, (Ir = C.class_names) == null ? void 0 : Ir.footer, "ms-gr-pro-chatbot-message-footer", K === D ? "ms-gr-pro-chatbot-message-footer-editing" : void 0),
          content: F(V ? (Mr = x == null ? void 0 : x.class_names) == null ? void 0 : Mr.content : (Lr = w == null ? void 0 : w.class_names) == null ? void 0 : Lr.content, (Or = C.class_names) == null ? void 0 : Or.content, "ms-gr-pro-chatbot-message-content")
        }
      };
    },
    postProcess(C, K) {
      const V = C.role === "user";
      switch (C.role) {
        case "chatbot-internal-welcome":
          return {
            variant: "borderless",
            styles: {
              content: {
                width: "100%"
              }
            },
            messageRender() {
              return /* @__PURE__ */ S.jsx(Ql, {
                urlRoot: l,
                urlProxyUrl: u,
                options: j || {},
                onWelcomePromptSelect: q
              });
            }
          };
        case "user":
        case "assistant":
          return {
            ...zr(V ? x : w, ["actions", "avatar", "header"]),
            ...C,
            style: {
              ...V ? x == null ? void 0 : x.style : w == null ? void 0 : w.style,
              ...C.style
            },
            className: F(C.className, V ? x == null ? void 0 : x.elem_classes : w == null ? void 0 : w.elem_classes),
            header: /* @__PURE__ */ S.jsx(oc, {
              title: C[Mn] ?? (V ? x == null ? void 0 : x.header : w == null ? void 0 : w.header),
              markdownConfig: M
            }),
            avatar: Zl(C[On] ?? (V ? x == null ? void 0 : x.avatar : w == null ? void 0 : w.avatar)),
            footer: (
              // bubbleProps[lastMessageSymbol] &&
              C.loading || C.status === "pending" ? null : /* @__PURE__ */ S.jsx(nc, {
                isEditing: D === K,
                message: C,
                extra: C[Ln] ?? (V ? x == null ? void 0 : x.footer : w == null ? void 0 : w.footer),
                urlRoot: l,
                urlProxyUrl: u,
                editValues: oe,
                index: K,
                actions: C.actions ?? (V ? (x == null ? void 0 : x.actions) || [] : (w == null ? void 0 : w.actions) || []),
                disabledActions: C.disabled_actions ?? (V ? (x == null ? void 0 : x.disabled_actions) || [] : (w == null ? void 0 : w.disabled_actions) || []),
                onEditCancel: xe,
                onEditConfirm: ke,
                onCopy: Ae,
                onEdit: ee,
                onDelete: we,
                onRetry: ie,
                onLike: ze
              })
            ),
            messageRender() {
              return /* @__PURE__ */ S.jsx(pc, {
                index: K,
                urlProxyUrl: u,
                urlRoot: l,
                isEditing: D === K,
                message: C,
                isLastMessage: C[jn] || !1,
                markdownConfig: M,
                onEdit: W,
                onSuggestionSelect: U
              });
            }
          };
        default:
          return;
      }
    }
  }, [D, x, j, w, M, oe]), {
    scrollToBottom: st,
    showScrollButton: Vt
  } = Ul({
    ref: A,
    value: i,
    autoScroll: m,
    scrollButtonOffset: h
  });
  return /* @__PURE__ */ S.jsxs("div", {
    id: e,
    className: F(t, "ms-gr-pro-chatbot"),
    style: {
      height: n,
      minHeight: o,
      maxHeight: s,
      ...r
    },
    children: [/* @__PURE__ */ S.jsx(Cr.List, {
      ref: A,
      className: "ms-gr-pro-chatbot-messages",
      autoScroll: !1,
      roles: De,
      items: k
    }), d && Vt && /* @__PURE__ */ S.jsx("div", {
      className: "ms-gr-pro-chatbot-scroll-to-bottom-button",
      children: /* @__PURE__ */ S.jsx(re, {
        icon: /* @__PURE__ */ S.jsx(ls, {}),
        shape: "circle",
        variant: "outlined",
        color: "primary",
        onClick: () => st("smooth")
      })
    })]
  });
}));
export {
  _c as Chatbot,
  _c as default
};
