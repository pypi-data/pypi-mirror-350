var Vi = { exports: {} }, T = {};
/**
 * @license React
 * react.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var Yt = Symbol.for("react.element"), ec = Symbol.for("react.portal"), nc = Symbol.for("react.fragment"), tc = Symbol.for("react.strict_mode"), rc = Symbol.for("react.profiler"), lc = Symbol.for("react.provider"), oc = Symbol.for("react.context"), uc = Symbol.for("react.forward_ref"), ic = Symbol.for("react.suspense"), sc = Symbol.for("react.memo"), ac = Symbol.for("react.lazy"), Mu = Symbol.iterator;
function cc(e) {
  return e === null || typeof e != "object" ? null : (e = Mu && e[Mu] || e["@@iterator"], typeof e == "function" ? e : null);
}
var Bi = { isMounted: function() {
  return !1;
}, enqueueForceUpdate: function() {
}, enqueueReplaceState: function() {
}, enqueueSetState: function() {
} }, Hi = Object.assign, Qi = {};
function lt(e, n, t) {
  this.props = e, this.context = n, this.refs = Qi, this.updater = t || Bi;
}
lt.prototype.isReactComponent = {};
lt.prototype.setState = function(e, n) {
  if (typeof e != "object" && typeof e != "function" && e != null) throw Error("setState(...): takes an object of state variables to update or a function which returns an object of state variables.");
  this.updater.enqueueSetState(this, e, n, "setState");
};
lt.prototype.forceUpdate = function(e) {
  this.updater.enqueueForceUpdate(this, e, "forceUpdate");
};
function Wi() {
}
Wi.prototype = lt.prototype;
function Uo(e, n, t) {
  this.props = e, this.context = n, this.refs = Qi, this.updater = t || Bi;
}
var jo = Uo.prototype = new Wi();
jo.constructor = Uo;
Hi(jo, lt.prototype);
jo.isPureReactComponent = !0;
var Ou = Array.isArray, Ki = Object.prototype.hasOwnProperty, $o = { current: null }, Yi = { key: !0, ref: !0, __self: !0, __source: !0 };
function Xi(e, n, t) {
  var r, l = {}, o = null, u = null;
  if (n != null) for (r in n.ref !== void 0 && (u = n.ref), n.key !== void 0 && (o = "" + n.key), n) Ki.call(n, r) && !Yi.hasOwnProperty(r) && (l[r] = n[r]);
  var i = arguments.length - 2;
  if (i === 1) l.children = t;
  else if (1 < i) {
    for (var s = Array(i), f = 0; f < i; f++) s[f] = arguments[f + 2];
    l.children = s;
  }
  if (e && e.defaultProps) for (r in i = e.defaultProps, i) l[r] === void 0 && (l[r] = i[r]);
  return { $$typeof: Yt, type: e, key: o, ref: u, props: l, _owner: $o.current };
}
function fc(e, n) {
  return { $$typeof: Yt, type: e.type, key: n, ref: e.ref, props: e.props, _owner: e._owner };
}
function Ao(e) {
  return typeof e == "object" && e !== null && e.$$typeof === Yt;
}
function dc(e) {
  var n = { "=": "=0", ":": "=2" };
  return "$" + e.replace(/[=:]/g, function(t) {
    return n[t];
  });
}
var Du = /\/+/g;
function gl(e, n) {
  return typeof e == "object" && e !== null && e.key != null ? dc("" + e.key) : n.toString(36);
}
function gr(e, n, t, r, l) {
  var o = typeof e;
  (o === "undefined" || o === "boolean") && (e = null);
  var u = !1;
  if (e === null) u = !0;
  else switch (o) {
    case "string":
    case "number":
      u = !0;
      break;
    case "object":
      switch (e.$$typeof) {
        case Yt:
        case ec:
          u = !0;
      }
  }
  if (u) return u = e, l = l(u), e = r === "" ? "." + gl(u, 0) : r, Ou(l) ? (t = "", e != null && (t = e.replace(Du, "$&/") + "/"), gr(l, n, t, "", function(f) {
    return f;
  })) : l != null && (Ao(l) && (l = fc(l, t + (!l.key || u && u.key === l.key ? "" : ("" + l.key).replace(Du, "$&/") + "/") + e)), n.push(l)), 1;
  if (u = 0, r = r === "" ? "." : r + ":", Ou(e)) for (var i = 0; i < e.length; i++) {
    o = e[i];
    var s = r + gl(o, i);
    u += gr(o, n, t, s, l);
  }
  else if (s = cc(e), typeof s == "function") for (e = s.call(e), i = 0; !(o = e.next()).done; ) o = o.value, s = r + gl(o, i++), u += gr(o, n, t, s, l);
  else if (o === "object") throw n = String(e), Error("Objects are not valid as a React child (found: " + (n === "[object Object]" ? "object with keys {" + Object.keys(e).join(", ") + "}" : n) + "). If you meant to render a collection of children, use an array instead.");
  return u;
}
function er(e, n, t) {
  if (e == null) return e;
  var r = [], l = 0;
  return gr(e, r, "", "", function(o) {
    return n.call(t, o, l++);
  }), r;
}
function pc(e) {
  if (e._status === -1) {
    var n = e._result;
    n = n(), n.then(function(t) {
      (e._status === 0 || e._status === -1) && (e._status = 1, e._result = t);
    }, function(t) {
      (e._status === 0 || e._status === -1) && (e._status = 2, e._result = t);
    }), e._status === -1 && (e._status = 0, e._result = n);
  }
  if (e._status === 1) return e._result.default;
  throw e._result;
}
var ie = { current: null }, wr = { transition: null }, mc = { ReactCurrentDispatcher: ie, ReactCurrentBatchConfig: wr, ReactCurrentOwner: $o };
function Gi() {
  throw Error("act(...) is not supported in production builds of React.");
}
T.Children = { map: er, forEach: function(e, n, t) {
  er(e, function() {
    n.apply(this, arguments);
  }, t);
}, count: function(e) {
  var n = 0;
  return er(e, function() {
    n++;
  }), n;
}, toArray: function(e) {
  return er(e, function(n) {
    return n;
  }) || [];
}, only: function(e) {
  if (!Ao(e)) throw Error("React.Children.only expected to receive a single React element child.");
  return e;
} };
T.Component = lt;
T.Fragment = nc;
T.Profiler = rc;
T.PureComponent = Uo;
T.StrictMode = tc;
T.Suspense = ic;
T.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED = mc;
T.act = Gi;
T.cloneElement = function(e, n, t) {
  if (e == null) throw Error("React.cloneElement(...): The argument must be a React element, but you passed " + e + ".");
  var r = Hi({}, e.props), l = e.key, o = e.ref, u = e._owner;
  if (n != null) {
    if (n.ref !== void 0 && (o = n.ref, u = $o.current), n.key !== void 0 && (l = "" + n.key), e.type && e.type.defaultProps) var i = e.type.defaultProps;
    for (s in n) Ki.call(n, s) && !Yi.hasOwnProperty(s) && (r[s] = n[s] === void 0 && i !== void 0 ? i[s] : n[s]);
  }
  var s = arguments.length - 2;
  if (s === 1) r.children = t;
  else if (1 < s) {
    i = Array(s);
    for (var f = 0; f < s; f++) i[f] = arguments[f + 2];
    r.children = i;
  }
  return { $$typeof: Yt, type: e.type, key: l, ref: o, props: r, _owner: u };
};
T.createContext = function(e) {
  return e = { $$typeof: oc, _currentValue: e, _currentValue2: e, _threadCount: 0, Provider: null, Consumer: null, _defaultValue: null, _globalName: null }, e.Provider = { $$typeof: lc, _context: e }, e.Consumer = e;
};
T.createElement = Xi;
T.createFactory = function(e) {
  var n = Xi.bind(null, e);
  return n.type = e, n;
};
T.createRef = function() {
  return { current: null };
};
T.forwardRef = function(e) {
  return { $$typeof: uc, render: e };
};
T.isValidElement = Ao;
T.lazy = function(e) {
  return { $$typeof: ac, _payload: { _status: -1, _result: e }, _init: pc };
};
T.memo = function(e, n) {
  return { $$typeof: sc, type: e, compare: n === void 0 ? null : n };
};
T.startTransition = function(e) {
  var n = wr.transition;
  wr.transition = {};
  try {
    e();
  } finally {
    wr.transition = n;
  }
};
T.unstable_act = Gi;
T.useCallback = function(e, n) {
  return ie.current.useCallback(e, n);
};
T.useContext = function(e) {
  return ie.current.useContext(e);
};
T.useDebugValue = function() {
};
T.useDeferredValue = function(e) {
  return ie.current.useDeferredValue(e);
};
T.useEffect = function(e, n) {
  return ie.current.useEffect(e, n);
};
T.useId = function() {
  return ie.current.useId();
};
T.useImperativeHandle = function(e, n, t) {
  return ie.current.useImperativeHandle(e, n, t);
};
T.useInsertionEffect = function(e, n) {
  return ie.current.useInsertionEffect(e, n);
};
T.useLayoutEffect = function(e, n) {
  return ie.current.useLayoutEffect(e, n);
};
T.useMemo = function(e, n) {
  return ie.current.useMemo(e, n);
};
T.useReducer = function(e, n, t) {
  return ie.current.useReducer(e, n, t);
};
T.useRef = function(e) {
  return ie.current.useRef(e);
};
T.useState = function(e) {
  return ie.current.useState(e);
};
T.useSyncExternalStore = function(e, n, t) {
  return ie.current.useSyncExternalStore(e, n, t);
};
T.useTransition = function() {
  return ie.current.useTransition();
};
T.version = "18.3.1";
Vi.exports = T;
var te = Vi.exports, Zi = { exports: {} }, ge = {}, Ji = { exports: {} }, qi = {};
/**
 * @license React
 * scheduler.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
(function(e) {
  function n(C, z) {
    var L = C.length;
    C.push(z);
    e: for (; 0 < L; ) {
      var H = L - 1 >>> 1, X = C[H];
      if (0 < l(X, z)) C[H] = z, C[L] = X, L = H;
      else break e;
    }
  }
  function t(C) {
    return C.length === 0 ? null : C[0];
  }
  function r(C) {
    if (C.length === 0) return null;
    var z = C[0], L = C.pop();
    if (L !== z) {
      C[0] = L;
      e: for (var H = 0, X = C.length, qt = X >>> 1; H < qt; ) {
        var vn = 2 * (H + 1) - 1, yl = C[vn], yn = vn + 1, bt = C[yn];
        if (0 > l(yl, L)) yn < X && 0 > l(bt, yl) ? (C[H] = bt, C[yn] = L, H = yn) : (C[H] = yl, C[vn] = L, H = vn);
        else if (yn < X && 0 > l(bt, L)) C[H] = bt, C[yn] = L, H = yn;
        else break e;
      }
    }
    return z;
  }
  function l(C, z) {
    var L = C.sortIndex - z.sortIndex;
    return L !== 0 ? L : C.id - z.id;
  }
  if (typeof performance == "object" && typeof performance.now == "function") {
    var o = performance;
    e.unstable_now = function() {
      return o.now();
    };
  } else {
    var u = Date, i = u.now();
    e.unstable_now = function() {
      return u.now() - i;
    };
  }
  var s = [], f = [], h = 1, m = null, p = 3, S = !1, v = !1, w = !1, N = typeof setTimeout == "function" ? setTimeout : null, c = typeof clearTimeout == "function" ? clearTimeout : null, a = typeof setImmediate < "u" ? setImmediate : null;
  typeof navigator < "u" && navigator.scheduling !== void 0 && navigator.scheduling.isInputPending !== void 0 && navigator.scheduling.isInputPending.bind(navigator.scheduling);
  function d(C) {
    for (var z = t(f); z !== null; ) {
      if (z.callback === null) r(f);
      else if (z.startTime <= C) r(f), z.sortIndex = z.expirationTime, n(s, z);
      else break;
      z = t(f);
    }
  }
  function y(C) {
    if (w = !1, d(C), !v) if (t(s) !== null) v = !0, hl(E);
    else {
      var z = t(f);
      z !== null && vl(y, z.startTime - C);
    }
  }
  function E(C, z) {
    v = !1, w && (w = !1, c(P), P = -1), S = !0;
    var L = p;
    try {
      for (d(z), m = t(s); m !== null && (!(m.expirationTime > z) || C && !Pe()); ) {
        var H = m.callback;
        if (typeof H == "function") {
          m.callback = null, p = m.priorityLevel;
          var X = H(m.expirationTime <= z);
          z = e.unstable_now(), typeof X == "function" ? m.callback = X : m === t(s) && r(s), d(z);
        } else r(s);
        m = t(s);
      }
      if (m !== null) var qt = !0;
      else {
        var vn = t(f);
        vn !== null && vl(y, vn.startTime - z), qt = !1;
      }
      return qt;
    } finally {
      m = null, p = L, S = !1;
    }
  }
  var _ = !1, x = null, P = -1, B = 5, R = -1;
  function Pe() {
    return !(e.unstable_now() - R < B);
  }
  function it() {
    if (x !== null) {
      var C = e.unstable_now();
      R = C;
      var z = !0;
      try {
        z = x(!0, C);
      } finally {
        z ? st() : (_ = !1, x = null);
      }
    } else _ = !1;
  }
  var st;
  if (typeof a == "function") st = function() {
    a(it);
  };
  else if (typeof MessageChannel < "u") {
    var Ru = new MessageChannel(), ba = Ru.port2;
    Ru.port1.onmessage = it, st = function() {
      ba.postMessage(null);
    };
  } else st = function() {
    N(it, 0);
  };
  function hl(C) {
    x = C, _ || (_ = !0, st());
  }
  function vl(C, z) {
    P = N(function() {
      C(e.unstable_now());
    }, z);
  }
  e.unstable_IdlePriority = 5, e.unstable_ImmediatePriority = 1, e.unstable_LowPriority = 4, e.unstable_NormalPriority = 3, e.unstable_Profiling = null, e.unstable_UserBlockingPriority = 2, e.unstable_cancelCallback = function(C) {
    C.callback = null;
  }, e.unstable_continueExecution = function() {
    v || S || (v = !0, hl(E));
  }, e.unstable_forceFrameRate = function(C) {
    0 > C || 125 < C ? console.error("forceFrameRate takes a positive int between 0 and 125, forcing frame rates higher than 125 fps is not supported") : B = 0 < C ? Math.floor(1e3 / C) : 5;
  }, e.unstable_getCurrentPriorityLevel = function() {
    return p;
  }, e.unstable_getFirstCallbackNode = function() {
    return t(s);
  }, e.unstable_next = function(C) {
    switch (p) {
      case 1:
      case 2:
      case 3:
        var z = 3;
        break;
      default:
        z = p;
    }
    var L = p;
    p = z;
    try {
      return C();
    } finally {
      p = L;
    }
  }, e.unstable_pauseExecution = function() {
  }, e.unstable_requestPaint = function() {
  }, e.unstable_runWithPriority = function(C, z) {
    switch (C) {
      case 1:
      case 2:
      case 3:
      case 4:
      case 5:
        break;
      default:
        C = 3;
    }
    var L = p;
    p = C;
    try {
      return z();
    } finally {
      p = L;
    }
  }, e.unstable_scheduleCallback = function(C, z, L) {
    var H = e.unstable_now();
    switch (typeof L == "object" && L !== null ? (L = L.delay, L = typeof L == "number" && 0 < L ? H + L : H) : L = H, C) {
      case 1:
        var X = -1;
        break;
      case 2:
        X = 250;
        break;
      case 5:
        X = 1073741823;
        break;
      case 4:
        X = 1e4;
        break;
      default:
        X = 5e3;
    }
    return X = L + X, C = { id: h++, callback: z, priorityLevel: C, startTime: L, expirationTime: X, sortIndex: -1 }, L > H ? (C.sortIndex = L, n(f, C), t(s) === null && C === t(f) && (w ? (c(P), P = -1) : w = !0, vl(y, L - H))) : (C.sortIndex = X, n(s, C), v || S || (v = !0, hl(E))), C;
  }, e.unstable_shouldYield = Pe, e.unstable_wrapCallback = function(C) {
    var z = p;
    return function() {
      var L = p;
      p = z;
      try {
        return C.apply(this, arguments);
      } finally {
        p = L;
      }
    };
  };
})(qi);
Ji.exports = qi;
var hc = Ji.exports;
/**
 * @license React
 * react-dom.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var vc = te, ye = hc;
function g(e) {
  for (var n = "https://reactjs.org/docs/error-decoder.html?invariant=" + e, t = 1; t < arguments.length; t++) n += "&args[]=" + encodeURIComponent(arguments[t]);
  return "Minified React error #" + e + "; visit " + n + " for the full message or use the non-minified dev environment for full errors and additional helpful warnings.";
}
var bi = /* @__PURE__ */ new Set(), Tt = {};
function Tn(e, n) {
  Jn(e, n), Jn(e + "Capture", n);
}
function Jn(e, n) {
  for (Tt[e] = n, e = 0; e < n.length; e++) bi.add(n[e]);
}
var Qe = !(typeof window > "u" || typeof window.document > "u" || typeof window.document.createElement > "u"), Ql = Object.prototype.hasOwnProperty, yc = /^[:A-Z_a-z\u00C0-\u00D6\u00D8-\u00F6\u00F8-\u02FF\u0370-\u037D\u037F-\u1FFF\u200C-\u200D\u2070-\u218F\u2C00-\u2FEF\u3001-\uD7FF\uF900-\uFDCF\uFDF0-\uFFFD][:A-Z_a-z\u00C0-\u00D6\u00D8-\u00F6\u00F8-\u02FF\u0370-\u037D\u037F-\u1FFF\u200C-\u200D\u2070-\u218F\u2C00-\u2FEF\u3001-\uD7FF\uF900-\uFDCF\uFDF0-\uFFFD\-.0-9\u00B7\u0300-\u036F\u203F-\u2040]*$/, Iu = {}, Fu = {};
function gc(e) {
  return Ql.call(Fu, e) ? !0 : Ql.call(Iu, e) ? !1 : yc.test(e) ? Fu[e] = !0 : (Iu[e] = !0, !1);
}
function wc(e, n, t, r) {
  if (t !== null && t.type === 0) return !1;
  switch (typeof n) {
    case "function":
    case "symbol":
      return !0;
    case "boolean":
      return r ? !1 : t !== null ? !t.acceptsBooleans : (e = e.toLowerCase().slice(0, 5), e !== "data-" && e !== "aria-");
    default:
      return !1;
  }
}
function Sc(e, n, t, r) {
  if (n === null || typeof n > "u" || wc(e, n, t, r)) return !0;
  if (r) return !1;
  if (t !== null) switch (t.type) {
    case 3:
      return !n;
    case 4:
      return n === !1;
    case 5:
      return isNaN(n);
    case 6:
      return isNaN(n) || 1 > n;
  }
  return !1;
}
function se(e, n, t, r, l, o, u) {
  this.acceptsBooleans = n === 2 || n === 3 || n === 4, this.attributeName = r, this.attributeNamespace = l, this.mustUseProperty = t, this.propertyName = e, this.type = n, this.sanitizeURL = o, this.removeEmptyString = u;
}
var b = {};
"children dangerouslySetInnerHTML defaultValue defaultChecked innerHTML suppressContentEditableWarning suppressHydrationWarning style".split(" ").forEach(function(e) {
  b[e] = new se(e, 0, !1, e, null, !1, !1);
});
[["acceptCharset", "accept-charset"], ["className", "class"], ["htmlFor", "for"], ["httpEquiv", "http-equiv"]].forEach(function(e) {
  var n = e[0];
  b[n] = new se(n, 1, !1, e[1], null, !1, !1);
});
["contentEditable", "draggable", "spellCheck", "value"].forEach(function(e) {
  b[e] = new se(e, 2, !1, e.toLowerCase(), null, !1, !1);
});
["autoReverse", "externalResourcesRequired", "focusable", "preserveAlpha"].forEach(function(e) {
  b[e] = new se(e, 2, !1, e, null, !1, !1);
});
"allowFullScreen async autoFocus autoPlay controls default defer disabled disablePictureInPicture disableRemotePlayback formNoValidate hidden loop noModule noValidate open playsInline readOnly required reversed scoped seamless itemScope".split(" ").forEach(function(e) {
  b[e] = new se(e, 3, !1, e.toLowerCase(), null, !1, !1);
});
["checked", "multiple", "muted", "selected"].forEach(function(e) {
  b[e] = new se(e, 3, !0, e, null, !1, !1);
});
["capture", "download"].forEach(function(e) {
  b[e] = new se(e, 4, !1, e, null, !1, !1);
});
["cols", "rows", "size", "span"].forEach(function(e) {
  b[e] = new se(e, 6, !1, e, null, !1, !1);
});
["rowSpan", "start"].forEach(function(e) {
  b[e] = new se(e, 5, !1, e.toLowerCase(), null, !1, !1);
});
var Vo = /[\-:]([a-z])/g;
function Bo(e) {
  return e[1].toUpperCase();
}
"accent-height alignment-baseline arabic-form baseline-shift cap-height clip-path clip-rule color-interpolation color-interpolation-filters color-profile color-rendering dominant-baseline enable-background fill-opacity fill-rule flood-color flood-opacity font-family font-size font-size-adjust font-stretch font-style font-variant font-weight glyph-name glyph-orientation-horizontal glyph-orientation-vertical horiz-adv-x horiz-origin-x image-rendering letter-spacing lighting-color marker-end marker-mid marker-start overline-position overline-thickness paint-order panose-1 pointer-events rendering-intent shape-rendering stop-color stop-opacity strikethrough-position strikethrough-thickness stroke-dasharray stroke-dashoffset stroke-linecap stroke-linejoin stroke-miterlimit stroke-opacity stroke-width text-anchor text-decoration text-rendering underline-position underline-thickness unicode-bidi unicode-range units-per-em v-alphabetic v-hanging v-ideographic v-mathematical vector-effect vert-adv-y vert-origin-x vert-origin-y word-spacing writing-mode xmlns:xlink x-height".split(" ").forEach(function(e) {
  var n = e.replace(
    Vo,
    Bo
  );
  b[n] = new se(n, 1, !1, e, null, !1, !1);
});
"xlink:actuate xlink:arcrole xlink:role xlink:show xlink:title xlink:type".split(" ").forEach(function(e) {
  var n = e.replace(Vo, Bo);
  b[n] = new se(n, 1, !1, e, "http://www.w3.org/1999/xlink", !1, !1);
});
["xml:base", "xml:lang", "xml:space"].forEach(function(e) {
  var n = e.replace(Vo, Bo);
  b[n] = new se(n, 1, !1, e, "http://www.w3.org/XML/1998/namespace", !1, !1);
});
["tabIndex", "crossOrigin"].forEach(function(e) {
  b[e] = new se(e, 1, !1, e.toLowerCase(), null, !1, !1);
});
b.xlinkHref = new se("xlinkHref", 1, !1, "xlink:href", "http://www.w3.org/1999/xlink", !0, !1);
["src", "href", "action", "formAction"].forEach(function(e) {
  b[e] = new se(e, 1, !1, e.toLowerCase(), null, !0, !0);
});
function Ho(e, n, t, r) {
  var l = b.hasOwnProperty(n) ? b[n] : null;
  (l !== null ? l.type !== 0 : r || !(2 < n.length) || n[0] !== "o" && n[0] !== "O" || n[1] !== "n" && n[1] !== "N") && (Sc(n, t, l, r) && (t = null), r || l === null ? gc(n) && (t === null ? e.removeAttribute(n) : e.setAttribute(n, "" + t)) : l.mustUseProperty ? e[l.propertyName] = t === null ? l.type === 3 ? !1 : "" : t : (n = l.attributeName, r = l.attributeNamespace, t === null ? e.removeAttribute(n) : (l = l.type, t = l === 3 || l === 4 && t === !0 ? "" : "" + t, r ? e.setAttributeNS(r, n, t) : e.setAttribute(n, t))));
}
var Xe = vc.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED, nr = Symbol.for("react.element"), On = Symbol.for("react.portal"), Dn = Symbol.for("react.fragment"), Qo = Symbol.for("react.strict_mode"), Wl = Symbol.for("react.profiler"), es = Symbol.for("react.provider"), ns = Symbol.for("react.context"), Wo = Symbol.for("react.forward_ref"), Kl = Symbol.for("react.suspense"), Yl = Symbol.for("react.suspense_list"), Ko = Symbol.for("react.memo"), Ze = Symbol.for("react.lazy"), ts = Symbol.for("react.offscreen"), Uu = Symbol.iterator;
function at(e) {
  return e === null || typeof e != "object" ? null : (e = Uu && e[Uu] || e["@@iterator"], typeof e == "function" ? e : null);
}
var A = Object.assign, wl;
function yt(e) {
  if (wl === void 0) try {
    throw Error();
  } catch (t) {
    var n = t.stack.trim().match(/\n( *(at )?)/);
    wl = n && n[1] || "";
  }
  return `
` + wl + e;
}
var Sl = !1;
function kl(e, n) {
  if (!e || Sl) return "";
  Sl = !0;
  var t = Error.prepareStackTrace;
  Error.prepareStackTrace = void 0;
  try {
    if (n) if (n = function() {
      throw Error();
    }, Object.defineProperty(n.prototype, "props", { set: function() {
      throw Error();
    } }), typeof Reflect == "object" && Reflect.construct) {
      try {
        Reflect.construct(n, []);
      } catch (f) {
        var r = f;
      }
      Reflect.construct(e, [], n);
    } else {
      try {
        n.call();
      } catch (f) {
        r = f;
      }
      e.call(n.prototype);
    }
    else {
      try {
        throw Error();
      } catch (f) {
        r = f;
      }
      e();
    }
  } catch (f) {
    if (f && r && typeof f.stack == "string") {
      for (var l = f.stack.split(`
`), o = r.stack.split(`
`), u = l.length - 1, i = o.length - 1; 1 <= u && 0 <= i && l[u] !== o[i]; ) i--;
      for (; 1 <= u && 0 <= i; u--, i--) if (l[u] !== o[i]) {
        if (u !== 1 || i !== 1)
          do
            if (u--, i--, 0 > i || l[u] !== o[i]) {
              var s = `
` + l[u].replace(" at new ", " at ");
              return e.displayName && s.includes("<anonymous>") && (s = s.replace("<anonymous>", e.displayName)), s;
            }
          while (1 <= u && 0 <= i);
        break;
      }
    }
  } finally {
    Sl = !1, Error.prepareStackTrace = t;
  }
  return (e = e ? e.displayName || e.name : "") ? yt(e) : "";
}
function kc(e) {
  switch (e.tag) {
    case 5:
      return yt(e.type);
    case 16:
      return yt("Lazy");
    case 13:
      return yt("Suspense");
    case 19:
      return yt("SuspenseList");
    case 0:
    case 2:
    case 15:
      return e = kl(e.type, !1), e;
    case 11:
      return e = kl(e.type.render, !1), e;
    case 1:
      return e = kl(e.type, !0), e;
    default:
      return "";
  }
}
function Xl(e) {
  if (e == null) return null;
  if (typeof e == "function") return e.displayName || e.name || null;
  if (typeof e == "string") return e;
  switch (e) {
    case Dn:
      return "Fragment";
    case On:
      return "Portal";
    case Wl:
      return "Profiler";
    case Qo:
      return "StrictMode";
    case Kl:
      return "Suspense";
    case Yl:
      return "SuspenseList";
  }
  if (typeof e == "object") switch (e.$$typeof) {
    case ns:
      return (e.displayName || "Context") + ".Consumer";
    case es:
      return (e._context.displayName || "Context") + ".Provider";
    case Wo:
      var n = e.render;
      return e = e.displayName, e || (e = n.displayName || n.name || "", e = e !== "" ? "ForwardRef(" + e + ")" : "ForwardRef"), e;
    case Ko:
      return n = e.displayName || null, n !== null ? n : Xl(e.type) || "Memo";
    case Ze:
      n = e._payload, e = e._init;
      try {
        return Xl(e(n));
      } catch {
      }
  }
  return null;
}
function Ec(e) {
  var n = e.type;
  switch (e.tag) {
    case 24:
      return "Cache";
    case 9:
      return (n.displayName || "Context") + ".Consumer";
    case 10:
      return (n._context.displayName || "Context") + ".Provider";
    case 18:
      return "DehydratedFragment";
    case 11:
      return e = n.render, e = e.displayName || e.name || "", n.displayName || (e !== "" ? "ForwardRef(" + e + ")" : "ForwardRef");
    case 7:
      return "Fragment";
    case 5:
      return n;
    case 4:
      return "Portal";
    case 3:
      return "Root";
    case 6:
      return "Text";
    case 16:
      return Xl(n);
    case 8:
      return n === Qo ? "StrictMode" : "Mode";
    case 22:
      return "Offscreen";
    case 12:
      return "Profiler";
    case 21:
      return "Scope";
    case 13:
      return "Suspense";
    case 19:
      return "SuspenseList";
    case 25:
      return "TracingMarker";
    case 1:
    case 0:
    case 17:
    case 2:
    case 14:
    case 15:
      if (typeof n == "function") return n.displayName || n.name || null;
      if (typeof n == "string") return n;
  }
  return null;
}
function fn(e) {
  switch (typeof e) {
    case "boolean":
    case "number":
    case "string":
    case "undefined":
      return e;
    case "object":
      return e;
    default:
      return "";
  }
}
function rs(e) {
  var n = e.type;
  return (e = e.nodeName) && e.toLowerCase() === "input" && (n === "checkbox" || n === "radio");
}
function Cc(e) {
  var n = rs(e) ? "checked" : "value", t = Object.getOwnPropertyDescriptor(e.constructor.prototype, n), r = "" + e[n];
  if (!e.hasOwnProperty(n) && typeof t < "u" && typeof t.get == "function" && typeof t.set == "function") {
    var l = t.get, o = t.set;
    return Object.defineProperty(e, n, { configurable: !0, get: function() {
      return l.call(this);
    }, set: function(u) {
      r = "" + u, o.call(this, u);
    } }), Object.defineProperty(e, n, { enumerable: t.enumerable }), { getValue: function() {
      return r;
    }, setValue: function(u) {
      r = "" + u;
    }, stopTracking: function() {
      e._valueTracker = null, delete e[n];
    } };
  }
}
function tr(e) {
  e._valueTracker || (e._valueTracker = Cc(e));
}
function ls(e) {
  if (!e) return !1;
  var n = e._valueTracker;
  if (!n) return !0;
  var t = n.getValue(), r = "";
  return e && (r = rs(e) ? e.checked ? "true" : "false" : e.value), e = r, e !== t ? (n.setValue(e), !0) : !1;
}
function Tr(e) {
  if (e = e || (typeof document < "u" ? document : void 0), typeof e > "u") return null;
  try {
    return e.activeElement || e.body;
  } catch {
    return e.body;
  }
}
function Gl(e, n) {
  var t = n.checked;
  return A({}, n, { defaultChecked: void 0, defaultValue: void 0, value: void 0, checked: t ?? e._wrapperState.initialChecked });
}
function ju(e, n) {
  var t = n.defaultValue == null ? "" : n.defaultValue, r = n.checked != null ? n.checked : n.defaultChecked;
  t = fn(n.value != null ? n.value : t), e._wrapperState = { initialChecked: r, initialValue: t, controlled: n.type === "checkbox" || n.type === "radio" ? n.checked != null : n.value != null };
}
function os(e, n) {
  n = n.checked, n != null && Ho(e, "checked", n, !1);
}
function Zl(e, n) {
  os(e, n);
  var t = fn(n.value), r = n.type;
  if (t != null) r === "number" ? (t === 0 && e.value === "" || e.value != t) && (e.value = "" + t) : e.value !== "" + t && (e.value = "" + t);
  else if (r === "submit" || r === "reset") {
    e.removeAttribute("value");
    return;
  }
  n.hasOwnProperty("value") ? Jl(e, n.type, t) : n.hasOwnProperty("defaultValue") && Jl(e, n.type, fn(n.defaultValue)), n.checked == null && n.defaultChecked != null && (e.defaultChecked = !!n.defaultChecked);
}
function $u(e, n, t) {
  if (n.hasOwnProperty("value") || n.hasOwnProperty("defaultValue")) {
    var r = n.type;
    if (!(r !== "submit" && r !== "reset" || n.value !== void 0 && n.value !== null)) return;
    n = "" + e._wrapperState.initialValue, t || n === e.value || (e.value = n), e.defaultValue = n;
  }
  t = e.name, t !== "" && (e.name = ""), e.defaultChecked = !!e._wrapperState.initialChecked, t !== "" && (e.name = t);
}
function Jl(e, n, t) {
  (n !== "number" || Tr(e.ownerDocument) !== e) && (t == null ? e.defaultValue = "" + e._wrapperState.initialValue : e.defaultValue !== "" + t && (e.defaultValue = "" + t));
}
var gt = Array.isArray;
function Wn(e, n, t, r) {
  if (e = e.options, n) {
    n = {};
    for (var l = 0; l < t.length; l++) n["$" + t[l]] = !0;
    for (t = 0; t < e.length; t++) l = n.hasOwnProperty("$" + e[t].value), e[t].selected !== l && (e[t].selected = l), l && r && (e[t].defaultSelected = !0);
  } else {
    for (t = "" + fn(t), n = null, l = 0; l < e.length; l++) {
      if (e[l].value === t) {
        e[l].selected = !0, r && (e[l].defaultSelected = !0);
        return;
      }
      n !== null || e[l].disabled || (n = e[l]);
    }
    n !== null && (n.selected = !0);
  }
}
function ql(e, n) {
  if (n.dangerouslySetInnerHTML != null) throw Error(g(91));
  return A({}, n, { value: void 0, defaultValue: void 0, children: "" + e._wrapperState.initialValue });
}
function Au(e, n) {
  var t = n.value;
  if (t == null) {
    if (t = n.children, n = n.defaultValue, t != null) {
      if (n != null) throw Error(g(92));
      if (gt(t)) {
        if (1 < t.length) throw Error(g(93));
        t = t[0];
      }
      n = t;
    }
    n == null && (n = ""), t = n;
  }
  e._wrapperState = { initialValue: fn(t) };
}
function us(e, n) {
  var t = fn(n.value), r = fn(n.defaultValue);
  t != null && (t = "" + t, t !== e.value && (e.value = t), n.defaultValue == null && e.defaultValue !== t && (e.defaultValue = t)), r != null && (e.defaultValue = "" + r);
}
function Vu(e) {
  var n = e.textContent;
  n === e._wrapperState.initialValue && n !== "" && n !== null && (e.value = n);
}
function is(e) {
  switch (e) {
    case "svg":
      return "http://www.w3.org/2000/svg";
    case "math":
      return "http://www.w3.org/1998/Math/MathML";
    default:
      return "http://www.w3.org/1999/xhtml";
  }
}
function bl(e, n) {
  return e == null || e === "http://www.w3.org/1999/xhtml" ? is(n) : e === "http://www.w3.org/2000/svg" && n === "foreignObject" ? "http://www.w3.org/1999/xhtml" : e;
}
var rr, ss = function(e) {
  return typeof MSApp < "u" && MSApp.execUnsafeLocalFunction ? function(n, t, r, l) {
    MSApp.execUnsafeLocalFunction(function() {
      return e(n, t, r, l);
    });
  } : e;
}(function(e, n) {
  if (e.namespaceURI !== "http://www.w3.org/2000/svg" || "innerHTML" in e) e.innerHTML = n;
  else {
    for (rr = rr || document.createElement("div"), rr.innerHTML = "<svg>" + n.valueOf().toString() + "</svg>", n = rr.firstChild; e.firstChild; ) e.removeChild(e.firstChild);
    for (; n.firstChild; ) e.appendChild(n.firstChild);
  }
});
function Rt(e, n) {
  if (n) {
    var t = e.firstChild;
    if (t && t === e.lastChild && t.nodeType === 3) {
      t.nodeValue = n;
      return;
    }
  }
  e.textContent = n;
}
var kt = {
  animationIterationCount: !0,
  aspectRatio: !0,
  borderImageOutset: !0,
  borderImageSlice: !0,
  borderImageWidth: !0,
  boxFlex: !0,
  boxFlexGroup: !0,
  boxOrdinalGroup: !0,
  columnCount: !0,
  columns: !0,
  flex: !0,
  flexGrow: !0,
  flexPositive: !0,
  flexShrink: !0,
  flexNegative: !0,
  flexOrder: !0,
  gridArea: !0,
  gridRow: !0,
  gridRowEnd: !0,
  gridRowSpan: !0,
  gridRowStart: !0,
  gridColumn: !0,
  gridColumnEnd: !0,
  gridColumnSpan: !0,
  gridColumnStart: !0,
  fontWeight: !0,
  lineClamp: !0,
  lineHeight: !0,
  opacity: !0,
  order: !0,
  orphans: !0,
  tabSize: !0,
  widows: !0,
  zIndex: !0,
  zoom: !0,
  fillOpacity: !0,
  floodOpacity: !0,
  stopOpacity: !0,
  strokeDasharray: !0,
  strokeDashoffset: !0,
  strokeMiterlimit: !0,
  strokeOpacity: !0,
  strokeWidth: !0
}, _c = ["Webkit", "ms", "Moz", "O"];
Object.keys(kt).forEach(function(e) {
  _c.forEach(function(n) {
    n = n + e.charAt(0).toUpperCase() + e.substring(1), kt[n] = kt[e];
  });
});
function as(e, n, t) {
  return n == null || typeof n == "boolean" || n === "" ? "" : t || typeof n != "number" || n === 0 || kt.hasOwnProperty(e) && kt[e] ? ("" + n).trim() : n + "px";
}
function cs(e, n) {
  e = e.style;
  for (var t in n) if (n.hasOwnProperty(t)) {
    var r = t.indexOf("--") === 0, l = as(t, n[t], r);
    t === "float" && (t = "cssFloat"), r ? e.setProperty(t, l) : e[t] = l;
  }
}
var xc = A({ menuitem: !0 }, { area: !0, base: !0, br: !0, col: !0, embed: !0, hr: !0, img: !0, input: !0, keygen: !0, link: !0, meta: !0, param: !0, source: !0, track: !0, wbr: !0 });
function eo(e, n) {
  if (n) {
    if (xc[e] && (n.children != null || n.dangerouslySetInnerHTML != null)) throw Error(g(137, e));
    if (n.dangerouslySetInnerHTML != null) {
      if (n.children != null) throw Error(g(60));
      if (typeof n.dangerouslySetInnerHTML != "object" || !("__html" in n.dangerouslySetInnerHTML)) throw Error(g(61));
    }
    if (n.style != null && typeof n.style != "object") throw Error(g(62));
  }
}
function no(e, n) {
  if (e.indexOf("-") === -1) return typeof n.is == "string";
  switch (e) {
    case "annotation-xml":
    case "color-profile":
    case "font-face":
    case "font-face-src":
    case "font-face-uri":
    case "font-face-format":
    case "font-face-name":
    case "missing-glyph":
      return !1;
    default:
      return !0;
  }
}
var to = null;
function Yo(e) {
  return e = e.target || e.srcElement || window, e.correspondingUseElement && (e = e.correspondingUseElement), e.nodeType === 3 ? e.parentNode : e;
}
var ro = null, Kn = null, Yn = null;
function Bu(e) {
  if (e = Zt(e)) {
    if (typeof ro != "function") throw Error(g(280));
    var n = e.stateNode;
    n && (n = ll(n), ro(e.stateNode, e.type, n));
  }
}
function fs(e) {
  Kn ? Yn ? Yn.push(e) : Yn = [e] : Kn = e;
}
function ds() {
  if (Kn) {
    var e = Kn, n = Yn;
    if (Yn = Kn = null, Bu(e), n) for (e = 0; e < n.length; e++) Bu(n[e]);
  }
}
function ps(e, n) {
  return e(n);
}
function ms() {
}
var El = !1;
function hs(e, n, t) {
  if (El) return e(n, t);
  El = !0;
  try {
    return ps(e, n, t);
  } finally {
    El = !1, (Kn !== null || Yn !== null) && (ms(), ds());
  }
}
function Mt(e, n) {
  var t = e.stateNode;
  if (t === null) return null;
  var r = ll(t);
  if (r === null) return null;
  t = r[n];
  e: switch (n) {
    case "onClick":
    case "onClickCapture":
    case "onDoubleClick":
    case "onDoubleClickCapture":
    case "onMouseDown":
    case "onMouseDownCapture":
    case "onMouseMove":
    case "onMouseMoveCapture":
    case "onMouseUp":
    case "onMouseUpCapture":
    case "onMouseEnter":
      (r = !r.disabled) || (e = e.type, r = !(e === "button" || e === "input" || e === "select" || e === "textarea")), e = !r;
      break e;
    default:
      e = !1;
  }
  if (e) return null;
  if (t && typeof t != "function") throw Error(g(231, n, typeof t));
  return t;
}
var lo = !1;
if (Qe) try {
  var ct = {};
  Object.defineProperty(ct, "passive", { get: function() {
    lo = !0;
  } }), window.addEventListener("test", ct, ct), window.removeEventListener("test", ct, ct);
} catch {
  lo = !1;
}
function Pc(e, n, t, r, l, o, u, i, s) {
  var f = Array.prototype.slice.call(arguments, 3);
  try {
    n.apply(t, f);
  } catch (h) {
    this.onError(h);
  }
}
var Et = !1, Rr = null, Mr = !1, oo = null, Nc = { onError: function(e) {
  Et = !0, Rr = e;
} };
function zc(e, n, t, r, l, o, u, i, s) {
  Et = !1, Rr = null, Pc.apply(Nc, arguments);
}
function Lc(e, n, t, r, l, o, u, i, s) {
  if (zc.apply(this, arguments), Et) {
    if (Et) {
      var f = Rr;
      Et = !1, Rr = null;
    } else throw Error(g(198));
    Mr || (Mr = !0, oo = f);
  }
}
function Rn(e) {
  var n = e, t = e;
  if (e.alternate) for (; n.return; ) n = n.return;
  else {
    e = n;
    do
      n = e, n.flags & 4098 && (t = n.return), e = n.return;
    while (e);
  }
  return n.tag === 3 ? t : null;
}
function vs(e) {
  if (e.tag === 13) {
    var n = e.memoizedState;
    if (n === null && (e = e.alternate, e !== null && (n = e.memoizedState)), n !== null) return n.dehydrated;
  }
  return null;
}
function Hu(e) {
  if (Rn(e) !== e) throw Error(g(188));
}
function Tc(e) {
  var n = e.alternate;
  if (!n) {
    if (n = Rn(e), n === null) throw Error(g(188));
    return n !== e ? null : e;
  }
  for (var t = e, r = n; ; ) {
    var l = t.return;
    if (l === null) break;
    var o = l.alternate;
    if (o === null) {
      if (r = l.return, r !== null) {
        t = r;
        continue;
      }
      break;
    }
    if (l.child === o.child) {
      for (o = l.child; o; ) {
        if (o === t) return Hu(l), e;
        if (o === r) return Hu(l), n;
        o = o.sibling;
      }
      throw Error(g(188));
    }
    if (t.return !== r.return) t = l, r = o;
    else {
      for (var u = !1, i = l.child; i; ) {
        if (i === t) {
          u = !0, t = l, r = o;
          break;
        }
        if (i === r) {
          u = !0, r = l, t = o;
          break;
        }
        i = i.sibling;
      }
      if (!u) {
        for (i = o.child; i; ) {
          if (i === t) {
            u = !0, t = o, r = l;
            break;
          }
          if (i === r) {
            u = !0, r = o, t = l;
            break;
          }
          i = i.sibling;
        }
        if (!u) throw Error(g(189));
      }
    }
    if (t.alternate !== r) throw Error(g(190));
  }
  if (t.tag !== 3) throw Error(g(188));
  return t.stateNode.current === t ? e : n;
}
function ys(e) {
  return e = Tc(e), e !== null ? gs(e) : null;
}
function gs(e) {
  if (e.tag === 5 || e.tag === 6) return e;
  for (e = e.child; e !== null; ) {
    var n = gs(e);
    if (n !== null) return n;
    e = e.sibling;
  }
  return null;
}
var ws = ye.unstable_scheduleCallback, Qu = ye.unstable_cancelCallback, Rc = ye.unstable_shouldYield, Mc = ye.unstable_requestPaint, Q = ye.unstable_now, Oc = ye.unstable_getCurrentPriorityLevel, Xo = ye.unstable_ImmediatePriority, Ss = ye.unstable_UserBlockingPriority, Or = ye.unstable_NormalPriority, Dc = ye.unstable_LowPriority, ks = ye.unstable_IdlePriority, el = null, Ue = null;
function Ic(e) {
  if (Ue && typeof Ue.onCommitFiberRoot == "function") try {
    Ue.onCommitFiberRoot(el, e, void 0, (e.current.flags & 128) === 128);
  } catch {
  }
}
var Re = Math.clz32 ? Math.clz32 : jc, Fc = Math.log, Uc = Math.LN2;
function jc(e) {
  return e >>>= 0, e === 0 ? 32 : 31 - (Fc(e) / Uc | 0) | 0;
}
var lr = 64, or = 4194304;
function wt(e) {
  switch (e & -e) {
    case 1:
      return 1;
    case 2:
      return 2;
    case 4:
      return 4;
    case 8:
      return 8;
    case 16:
      return 16;
    case 32:
      return 32;
    case 64:
    case 128:
    case 256:
    case 512:
    case 1024:
    case 2048:
    case 4096:
    case 8192:
    case 16384:
    case 32768:
    case 65536:
    case 131072:
    case 262144:
    case 524288:
    case 1048576:
    case 2097152:
      return e & 4194240;
    case 4194304:
    case 8388608:
    case 16777216:
    case 33554432:
    case 67108864:
      return e & 130023424;
    case 134217728:
      return 134217728;
    case 268435456:
      return 268435456;
    case 536870912:
      return 536870912;
    case 1073741824:
      return 1073741824;
    default:
      return e;
  }
}
function Dr(e, n) {
  var t = e.pendingLanes;
  if (t === 0) return 0;
  var r = 0, l = e.suspendedLanes, o = e.pingedLanes, u = t & 268435455;
  if (u !== 0) {
    var i = u & ~l;
    i !== 0 ? r = wt(i) : (o &= u, o !== 0 && (r = wt(o)));
  } else u = t & ~l, u !== 0 ? r = wt(u) : o !== 0 && (r = wt(o));
  if (r === 0) return 0;
  if (n !== 0 && n !== r && !(n & l) && (l = r & -r, o = n & -n, l >= o || l === 16 && (o & 4194240) !== 0)) return n;
  if (r & 4 && (r |= t & 16), n = e.entangledLanes, n !== 0) for (e = e.entanglements, n &= r; 0 < n; ) t = 31 - Re(n), l = 1 << t, r |= e[t], n &= ~l;
  return r;
}
function $c(e, n) {
  switch (e) {
    case 1:
    case 2:
    case 4:
      return n + 250;
    case 8:
    case 16:
    case 32:
    case 64:
    case 128:
    case 256:
    case 512:
    case 1024:
    case 2048:
    case 4096:
    case 8192:
    case 16384:
    case 32768:
    case 65536:
    case 131072:
    case 262144:
    case 524288:
    case 1048576:
    case 2097152:
      return n + 5e3;
    case 4194304:
    case 8388608:
    case 16777216:
    case 33554432:
    case 67108864:
      return -1;
    case 134217728:
    case 268435456:
    case 536870912:
    case 1073741824:
      return -1;
    default:
      return -1;
  }
}
function Ac(e, n) {
  for (var t = e.suspendedLanes, r = e.pingedLanes, l = e.expirationTimes, o = e.pendingLanes; 0 < o; ) {
    var u = 31 - Re(o), i = 1 << u, s = l[u];
    s === -1 ? (!(i & t) || i & r) && (l[u] = $c(i, n)) : s <= n && (e.expiredLanes |= i), o &= ~i;
  }
}
function uo(e) {
  return e = e.pendingLanes & -1073741825, e !== 0 ? e : e & 1073741824 ? 1073741824 : 0;
}
function Es() {
  var e = lr;
  return lr <<= 1, !(lr & 4194240) && (lr = 64), e;
}
function Cl(e) {
  for (var n = [], t = 0; 31 > t; t++) n.push(e);
  return n;
}
function Xt(e, n, t) {
  e.pendingLanes |= n, n !== 536870912 && (e.suspendedLanes = 0, e.pingedLanes = 0), e = e.eventTimes, n = 31 - Re(n), e[n] = t;
}
function Vc(e, n) {
  var t = e.pendingLanes & ~n;
  e.pendingLanes = n, e.suspendedLanes = 0, e.pingedLanes = 0, e.expiredLanes &= n, e.mutableReadLanes &= n, e.entangledLanes &= n, n = e.entanglements;
  var r = e.eventTimes;
  for (e = e.expirationTimes; 0 < t; ) {
    var l = 31 - Re(t), o = 1 << l;
    n[l] = 0, r[l] = -1, e[l] = -1, t &= ~o;
  }
}
function Go(e, n) {
  var t = e.entangledLanes |= n;
  for (e = e.entanglements; t; ) {
    var r = 31 - Re(t), l = 1 << r;
    l & n | e[r] & n && (e[r] |= n), t &= ~l;
  }
}
var O = 0;
function Cs(e) {
  return e &= -e, 1 < e ? 4 < e ? e & 268435455 ? 16 : 536870912 : 4 : 1;
}
var _s, Zo, xs, Ps, Ns, io = !1, ur = [], tn = null, rn = null, ln = null, Ot = /* @__PURE__ */ new Map(), Dt = /* @__PURE__ */ new Map(), qe = [], Bc = "mousedown mouseup touchcancel touchend touchstart auxclick dblclick pointercancel pointerdown pointerup dragend dragstart drop compositionend compositionstart keydown keypress keyup input textInput copy cut paste click change contextmenu reset submit".split(" ");
function Wu(e, n) {
  switch (e) {
    case "focusin":
    case "focusout":
      tn = null;
      break;
    case "dragenter":
    case "dragleave":
      rn = null;
      break;
    case "mouseover":
    case "mouseout":
      ln = null;
      break;
    case "pointerover":
    case "pointerout":
      Ot.delete(n.pointerId);
      break;
    case "gotpointercapture":
    case "lostpointercapture":
      Dt.delete(n.pointerId);
  }
}
function ft(e, n, t, r, l, o) {
  return e === null || e.nativeEvent !== o ? (e = { blockedOn: n, domEventName: t, eventSystemFlags: r, nativeEvent: o, targetContainers: [l] }, n !== null && (n = Zt(n), n !== null && Zo(n)), e) : (e.eventSystemFlags |= r, n = e.targetContainers, l !== null && n.indexOf(l) === -1 && n.push(l), e);
}
function Hc(e, n, t, r, l) {
  switch (n) {
    case "focusin":
      return tn = ft(tn, e, n, t, r, l), !0;
    case "dragenter":
      return rn = ft(rn, e, n, t, r, l), !0;
    case "mouseover":
      return ln = ft(ln, e, n, t, r, l), !0;
    case "pointerover":
      var o = l.pointerId;
      return Ot.set(o, ft(Ot.get(o) || null, e, n, t, r, l)), !0;
    case "gotpointercapture":
      return o = l.pointerId, Dt.set(o, ft(Dt.get(o) || null, e, n, t, r, l)), !0;
  }
  return !1;
}
function zs(e) {
  var n = Sn(e.target);
  if (n !== null) {
    var t = Rn(n);
    if (t !== null) {
      if (n = t.tag, n === 13) {
        if (n = vs(t), n !== null) {
          e.blockedOn = n, Ns(e.priority, function() {
            xs(t);
          });
          return;
        }
      } else if (n === 3 && t.stateNode.current.memoizedState.isDehydrated) {
        e.blockedOn = t.tag === 3 ? t.stateNode.containerInfo : null;
        return;
      }
    }
  }
  e.blockedOn = null;
}
function Sr(e) {
  if (e.blockedOn !== null) return !1;
  for (var n = e.targetContainers; 0 < n.length; ) {
    var t = so(e.domEventName, e.eventSystemFlags, n[0], e.nativeEvent);
    if (t === null) {
      t = e.nativeEvent;
      var r = new t.constructor(t.type, t);
      to = r, t.target.dispatchEvent(r), to = null;
    } else return n = Zt(t), n !== null && Zo(n), e.blockedOn = t, !1;
    n.shift();
  }
  return !0;
}
function Ku(e, n, t) {
  Sr(e) && t.delete(n);
}
function Qc() {
  io = !1, tn !== null && Sr(tn) && (tn = null), rn !== null && Sr(rn) && (rn = null), ln !== null && Sr(ln) && (ln = null), Ot.forEach(Ku), Dt.forEach(Ku);
}
function dt(e, n) {
  e.blockedOn === n && (e.blockedOn = null, io || (io = !0, ye.unstable_scheduleCallback(ye.unstable_NormalPriority, Qc)));
}
function It(e) {
  function n(l) {
    return dt(l, e);
  }
  if (0 < ur.length) {
    dt(ur[0], e);
    for (var t = 1; t < ur.length; t++) {
      var r = ur[t];
      r.blockedOn === e && (r.blockedOn = null);
    }
  }
  for (tn !== null && dt(tn, e), rn !== null && dt(rn, e), ln !== null && dt(ln, e), Ot.forEach(n), Dt.forEach(n), t = 0; t < qe.length; t++) r = qe[t], r.blockedOn === e && (r.blockedOn = null);
  for (; 0 < qe.length && (t = qe[0], t.blockedOn === null); ) zs(t), t.blockedOn === null && qe.shift();
}
var Xn = Xe.ReactCurrentBatchConfig, Ir = !0;
function Wc(e, n, t, r) {
  var l = O, o = Xn.transition;
  Xn.transition = null;
  try {
    O = 1, Jo(e, n, t, r);
  } finally {
    O = l, Xn.transition = o;
  }
}
function Kc(e, n, t, r) {
  var l = O, o = Xn.transition;
  Xn.transition = null;
  try {
    O = 4, Jo(e, n, t, r);
  } finally {
    O = l, Xn.transition = o;
  }
}
function Jo(e, n, t, r) {
  if (Ir) {
    var l = so(e, n, t, r);
    if (l === null) Ol(e, n, r, Fr, t), Wu(e, r);
    else if (Hc(l, e, n, t, r)) r.stopPropagation();
    else if (Wu(e, r), n & 4 && -1 < Bc.indexOf(e)) {
      for (; l !== null; ) {
        var o = Zt(l);
        if (o !== null && _s(o), o = so(e, n, t, r), o === null && Ol(e, n, r, Fr, t), o === l) break;
        l = o;
      }
      l !== null && r.stopPropagation();
    } else Ol(e, n, r, null, t);
  }
}
var Fr = null;
function so(e, n, t, r) {
  if (Fr = null, e = Yo(r), e = Sn(e), e !== null) if (n = Rn(e), n === null) e = null;
  else if (t = n.tag, t === 13) {
    if (e = vs(n), e !== null) return e;
    e = null;
  } else if (t === 3) {
    if (n.stateNode.current.memoizedState.isDehydrated) return n.tag === 3 ? n.stateNode.containerInfo : null;
    e = null;
  } else n !== e && (e = null);
  return Fr = e, null;
}
function Ls(e) {
  switch (e) {
    case "cancel":
    case "click":
    case "close":
    case "contextmenu":
    case "copy":
    case "cut":
    case "auxclick":
    case "dblclick":
    case "dragend":
    case "dragstart":
    case "drop":
    case "focusin":
    case "focusout":
    case "input":
    case "invalid":
    case "keydown":
    case "keypress":
    case "keyup":
    case "mousedown":
    case "mouseup":
    case "paste":
    case "pause":
    case "play":
    case "pointercancel":
    case "pointerdown":
    case "pointerup":
    case "ratechange":
    case "reset":
    case "resize":
    case "seeked":
    case "submit":
    case "touchcancel":
    case "touchend":
    case "touchstart":
    case "volumechange":
    case "change":
    case "selectionchange":
    case "textInput":
    case "compositionstart":
    case "compositionend":
    case "compositionupdate":
    case "beforeblur":
    case "afterblur":
    case "beforeinput":
    case "blur":
    case "fullscreenchange":
    case "focus":
    case "hashchange":
    case "popstate":
    case "select":
    case "selectstart":
      return 1;
    case "drag":
    case "dragenter":
    case "dragexit":
    case "dragleave":
    case "dragover":
    case "mousemove":
    case "mouseout":
    case "mouseover":
    case "pointermove":
    case "pointerout":
    case "pointerover":
    case "scroll":
    case "toggle":
    case "touchmove":
    case "wheel":
    case "mouseenter":
    case "mouseleave":
    case "pointerenter":
    case "pointerleave":
      return 4;
    case "message":
      switch (Oc()) {
        case Xo:
          return 1;
        case Ss:
          return 4;
        case Or:
        case Dc:
          return 16;
        case ks:
          return 536870912;
        default:
          return 16;
      }
    default:
      return 16;
  }
}
var en = null, qo = null, kr = null;
function Ts() {
  if (kr) return kr;
  var e, n = qo, t = n.length, r, l = "value" in en ? en.value : en.textContent, o = l.length;
  for (e = 0; e < t && n[e] === l[e]; e++) ;
  var u = t - e;
  for (r = 1; r <= u && n[t - r] === l[o - r]; r++) ;
  return kr = l.slice(e, 1 < r ? 1 - r : void 0);
}
function Er(e) {
  var n = e.keyCode;
  return "charCode" in e ? (e = e.charCode, e === 0 && n === 13 && (e = 13)) : e = n, e === 10 && (e = 13), 32 <= e || e === 13 ? e : 0;
}
function ir() {
  return !0;
}
function Yu() {
  return !1;
}
function we(e) {
  function n(t, r, l, o, u) {
    this._reactName = t, this._targetInst = l, this.type = r, this.nativeEvent = o, this.target = u, this.currentTarget = null;
    for (var i in e) e.hasOwnProperty(i) && (t = e[i], this[i] = t ? t(o) : o[i]);
    return this.isDefaultPrevented = (o.defaultPrevented != null ? o.defaultPrevented : o.returnValue === !1) ? ir : Yu, this.isPropagationStopped = Yu, this;
  }
  return A(n.prototype, { preventDefault: function() {
    this.defaultPrevented = !0;
    var t = this.nativeEvent;
    t && (t.preventDefault ? t.preventDefault() : typeof t.returnValue != "unknown" && (t.returnValue = !1), this.isDefaultPrevented = ir);
  }, stopPropagation: function() {
    var t = this.nativeEvent;
    t && (t.stopPropagation ? t.stopPropagation() : typeof t.cancelBubble != "unknown" && (t.cancelBubble = !0), this.isPropagationStopped = ir);
  }, persist: function() {
  }, isPersistent: ir }), n;
}
var ot = { eventPhase: 0, bubbles: 0, cancelable: 0, timeStamp: function(e) {
  return e.timeStamp || Date.now();
}, defaultPrevented: 0, isTrusted: 0 }, bo = we(ot), Gt = A({}, ot, { view: 0, detail: 0 }), Yc = we(Gt), _l, xl, pt, nl = A({}, Gt, { screenX: 0, screenY: 0, clientX: 0, clientY: 0, pageX: 0, pageY: 0, ctrlKey: 0, shiftKey: 0, altKey: 0, metaKey: 0, getModifierState: eu, button: 0, buttons: 0, relatedTarget: function(e) {
  return e.relatedTarget === void 0 ? e.fromElement === e.srcElement ? e.toElement : e.fromElement : e.relatedTarget;
}, movementX: function(e) {
  return "movementX" in e ? e.movementX : (e !== pt && (pt && e.type === "mousemove" ? (_l = e.screenX - pt.screenX, xl = e.screenY - pt.screenY) : xl = _l = 0, pt = e), _l);
}, movementY: function(e) {
  return "movementY" in e ? e.movementY : xl;
} }), Xu = we(nl), Xc = A({}, nl, { dataTransfer: 0 }), Gc = we(Xc), Zc = A({}, Gt, { relatedTarget: 0 }), Pl = we(Zc), Jc = A({}, ot, { animationName: 0, elapsedTime: 0, pseudoElement: 0 }), qc = we(Jc), bc = A({}, ot, { clipboardData: function(e) {
  return "clipboardData" in e ? e.clipboardData : window.clipboardData;
} }), ef = we(bc), nf = A({}, ot, { data: 0 }), Gu = we(nf), tf = {
  Esc: "Escape",
  Spacebar: " ",
  Left: "ArrowLeft",
  Up: "ArrowUp",
  Right: "ArrowRight",
  Down: "ArrowDown",
  Del: "Delete",
  Win: "OS",
  Menu: "ContextMenu",
  Apps: "ContextMenu",
  Scroll: "ScrollLock",
  MozPrintableKey: "Unidentified"
}, rf = {
  8: "Backspace",
  9: "Tab",
  12: "Clear",
  13: "Enter",
  16: "Shift",
  17: "Control",
  18: "Alt",
  19: "Pause",
  20: "CapsLock",
  27: "Escape",
  32: " ",
  33: "PageUp",
  34: "PageDown",
  35: "End",
  36: "Home",
  37: "ArrowLeft",
  38: "ArrowUp",
  39: "ArrowRight",
  40: "ArrowDown",
  45: "Insert",
  46: "Delete",
  112: "F1",
  113: "F2",
  114: "F3",
  115: "F4",
  116: "F5",
  117: "F6",
  118: "F7",
  119: "F8",
  120: "F9",
  121: "F10",
  122: "F11",
  123: "F12",
  144: "NumLock",
  145: "ScrollLock",
  224: "Meta"
}, lf = { Alt: "altKey", Control: "ctrlKey", Meta: "metaKey", Shift: "shiftKey" };
function of(e) {
  var n = this.nativeEvent;
  return n.getModifierState ? n.getModifierState(e) : (e = lf[e]) ? !!n[e] : !1;
}
function eu() {
  return of;
}
var uf = A({}, Gt, { key: function(e) {
  if (e.key) {
    var n = tf[e.key] || e.key;
    if (n !== "Unidentified") return n;
  }
  return e.type === "keypress" ? (e = Er(e), e === 13 ? "Enter" : String.fromCharCode(e)) : e.type === "keydown" || e.type === "keyup" ? rf[e.keyCode] || "Unidentified" : "";
}, code: 0, location: 0, ctrlKey: 0, shiftKey: 0, altKey: 0, metaKey: 0, repeat: 0, locale: 0, getModifierState: eu, charCode: function(e) {
  return e.type === "keypress" ? Er(e) : 0;
}, keyCode: function(e) {
  return e.type === "keydown" || e.type === "keyup" ? e.keyCode : 0;
}, which: function(e) {
  return e.type === "keypress" ? Er(e) : e.type === "keydown" || e.type === "keyup" ? e.keyCode : 0;
} }), sf = we(uf), af = A({}, nl, { pointerId: 0, width: 0, height: 0, pressure: 0, tangentialPressure: 0, tiltX: 0, tiltY: 0, twist: 0, pointerType: 0, isPrimary: 0 }), Zu = we(af), cf = A({}, Gt, { touches: 0, targetTouches: 0, changedTouches: 0, altKey: 0, metaKey: 0, ctrlKey: 0, shiftKey: 0, getModifierState: eu }), ff = we(cf), df = A({}, ot, { propertyName: 0, elapsedTime: 0, pseudoElement: 0 }), pf = we(df), mf = A({}, nl, {
  deltaX: function(e) {
    return "deltaX" in e ? e.deltaX : "wheelDeltaX" in e ? -e.wheelDeltaX : 0;
  },
  deltaY: function(e) {
    return "deltaY" in e ? e.deltaY : "wheelDeltaY" in e ? -e.wheelDeltaY : "wheelDelta" in e ? -e.wheelDelta : 0;
  },
  deltaZ: 0,
  deltaMode: 0
}), hf = we(mf), vf = [9, 13, 27, 32], nu = Qe && "CompositionEvent" in window, Ct = null;
Qe && "documentMode" in document && (Ct = document.documentMode);
var yf = Qe && "TextEvent" in window && !Ct, Rs = Qe && (!nu || Ct && 8 < Ct && 11 >= Ct), Ju = " ", qu = !1;
function Ms(e, n) {
  switch (e) {
    case "keyup":
      return vf.indexOf(n.keyCode) !== -1;
    case "keydown":
      return n.keyCode !== 229;
    case "keypress":
    case "mousedown":
    case "focusout":
      return !0;
    default:
      return !1;
  }
}
function Os(e) {
  return e = e.detail, typeof e == "object" && "data" in e ? e.data : null;
}
var In = !1;
function gf(e, n) {
  switch (e) {
    case "compositionend":
      return Os(n);
    case "keypress":
      return n.which !== 32 ? null : (qu = !0, Ju);
    case "textInput":
      return e = n.data, e === Ju && qu ? null : e;
    default:
      return null;
  }
}
function wf(e, n) {
  if (In) return e === "compositionend" || !nu && Ms(e, n) ? (e = Ts(), kr = qo = en = null, In = !1, e) : null;
  switch (e) {
    case "paste":
      return null;
    case "keypress":
      if (!(n.ctrlKey || n.altKey || n.metaKey) || n.ctrlKey && n.altKey) {
        if (n.char && 1 < n.char.length) return n.char;
        if (n.which) return String.fromCharCode(n.which);
      }
      return null;
    case "compositionend":
      return Rs && n.locale !== "ko" ? null : n.data;
    default:
      return null;
  }
}
var Sf = { color: !0, date: !0, datetime: !0, "datetime-local": !0, email: !0, month: !0, number: !0, password: !0, range: !0, search: !0, tel: !0, text: !0, time: !0, url: !0, week: !0 };
function bu(e) {
  var n = e && e.nodeName && e.nodeName.toLowerCase();
  return n === "input" ? !!Sf[e.type] : n === "textarea";
}
function Ds(e, n, t, r) {
  fs(r), n = Ur(n, "onChange"), 0 < n.length && (t = new bo("onChange", "change", null, t, r), e.push({ event: t, listeners: n }));
}
var _t = null, Ft = null;
function kf(e) {
  Ws(e, 0);
}
function tl(e) {
  var n = jn(e);
  if (ls(n)) return e;
}
function Ef(e, n) {
  if (e === "change") return n;
}
var Is = !1;
if (Qe) {
  var Nl;
  if (Qe) {
    var zl = "oninput" in document;
    if (!zl) {
      var ei = document.createElement("div");
      ei.setAttribute("oninput", "return;"), zl = typeof ei.oninput == "function";
    }
    Nl = zl;
  } else Nl = !1;
  Is = Nl && (!document.documentMode || 9 < document.documentMode);
}
function ni() {
  _t && (_t.detachEvent("onpropertychange", Fs), Ft = _t = null);
}
function Fs(e) {
  if (e.propertyName === "value" && tl(Ft)) {
    var n = [];
    Ds(n, Ft, e, Yo(e)), hs(kf, n);
  }
}
function Cf(e, n, t) {
  e === "focusin" ? (ni(), _t = n, Ft = t, _t.attachEvent("onpropertychange", Fs)) : e === "focusout" && ni();
}
function _f(e) {
  if (e === "selectionchange" || e === "keyup" || e === "keydown") return tl(Ft);
}
function xf(e, n) {
  if (e === "click") return tl(n);
}
function Pf(e, n) {
  if (e === "input" || e === "change") return tl(n);
}
function Nf(e, n) {
  return e === n && (e !== 0 || 1 / e === 1 / n) || e !== e && n !== n;
}
var Oe = typeof Object.is == "function" ? Object.is : Nf;
function Ut(e, n) {
  if (Oe(e, n)) return !0;
  if (typeof e != "object" || e === null || typeof n != "object" || n === null) return !1;
  var t = Object.keys(e), r = Object.keys(n);
  if (t.length !== r.length) return !1;
  for (r = 0; r < t.length; r++) {
    var l = t[r];
    if (!Ql.call(n, l) || !Oe(e[l], n[l])) return !1;
  }
  return !0;
}
function ti(e) {
  for (; e && e.firstChild; ) e = e.firstChild;
  return e;
}
function ri(e, n) {
  var t = ti(e);
  e = 0;
  for (var r; t; ) {
    if (t.nodeType === 3) {
      if (r = e + t.textContent.length, e <= n && r >= n) return { node: t, offset: n - e };
      e = r;
    }
    e: {
      for (; t; ) {
        if (t.nextSibling) {
          t = t.nextSibling;
          break e;
        }
        t = t.parentNode;
      }
      t = void 0;
    }
    t = ti(t);
  }
}
function Us(e, n) {
  return e && n ? e === n ? !0 : e && e.nodeType === 3 ? !1 : n && n.nodeType === 3 ? Us(e, n.parentNode) : "contains" in e ? e.contains(n) : e.compareDocumentPosition ? !!(e.compareDocumentPosition(n) & 16) : !1 : !1;
}
function js() {
  for (var e = window, n = Tr(); n instanceof e.HTMLIFrameElement; ) {
    try {
      var t = typeof n.contentWindow.location.href == "string";
    } catch {
      t = !1;
    }
    if (t) e = n.contentWindow;
    else break;
    n = Tr(e.document);
  }
  return n;
}
function tu(e) {
  var n = e && e.nodeName && e.nodeName.toLowerCase();
  return n && (n === "input" && (e.type === "text" || e.type === "search" || e.type === "tel" || e.type === "url" || e.type === "password") || n === "textarea" || e.contentEditable === "true");
}
function zf(e) {
  var n = js(), t = e.focusedElem, r = e.selectionRange;
  if (n !== t && t && t.ownerDocument && Us(t.ownerDocument.documentElement, t)) {
    if (r !== null && tu(t)) {
      if (n = r.start, e = r.end, e === void 0 && (e = n), "selectionStart" in t) t.selectionStart = n, t.selectionEnd = Math.min(e, t.value.length);
      else if (e = (n = t.ownerDocument || document) && n.defaultView || window, e.getSelection) {
        e = e.getSelection();
        var l = t.textContent.length, o = Math.min(r.start, l);
        r = r.end === void 0 ? o : Math.min(r.end, l), !e.extend && o > r && (l = r, r = o, o = l), l = ri(t, o);
        var u = ri(
          t,
          r
        );
        l && u && (e.rangeCount !== 1 || e.anchorNode !== l.node || e.anchorOffset !== l.offset || e.focusNode !== u.node || e.focusOffset !== u.offset) && (n = n.createRange(), n.setStart(l.node, l.offset), e.removeAllRanges(), o > r ? (e.addRange(n), e.extend(u.node, u.offset)) : (n.setEnd(u.node, u.offset), e.addRange(n)));
      }
    }
    for (n = [], e = t; e = e.parentNode; ) e.nodeType === 1 && n.push({ element: e, left: e.scrollLeft, top: e.scrollTop });
    for (typeof t.focus == "function" && t.focus(), t = 0; t < n.length; t++) e = n[t], e.element.scrollLeft = e.left, e.element.scrollTop = e.top;
  }
}
var Lf = Qe && "documentMode" in document && 11 >= document.documentMode, Fn = null, ao = null, xt = null, co = !1;
function li(e, n, t) {
  var r = t.window === t ? t.document : t.nodeType === 9 ? t : t.ownerDocument;
  co || Fn == null || Fn !== Tr(r) || (r = Fn, "selectionStart" in r && tu(r) ? r = { start: r.selectionStart, end: r.selectionEnd } : (r = (r.ownerDocument && r.ownerDocument.defaultView || window).getSelection(), r = { anchorNode: r.anchorNode, anchorOffset: r.anchorOffset, focusNode: r.focusNode, focusOffset: r.focusOffset }), xt && Ut(xt, r) || (xt = r, r = Ur(ao, "onSelect"), 0 < r.length && (n = new bo("onSelect", "select", null, n, t), e.push({ event: n, listeners: r }), n.target = Fn)));
}
function sr(e, n) {
  var t = {};
  return t[e.toLowerCase()] = n.toLowerCase(), t["Webkit" + e] = "webkit" + n, t["Moz" + e] = "moz" + n, t;
}
var Un = { animationend: sr("Animation", "AnimationEnd"), animationiteration: sr("Animation", "AnimationIteration"), animationstart: sr("Animation", "AnimationStart"), transitionend: sr("Transition", "TransitionEnd") }, Ll = {}, $s = {};
Qe && ($s = document.createElement("div").style, "AnimationEvent" in window || (delete Un.animationend.animation, delete Un.animationiteration.animation, delete Un.animationstart.animation), "TransitionEvent" in window || delete Un.transitionend.transition);
function rl(e) {
  if (Ll[e]) return Ll[e];
  if (!Un[e]) return e;
  var n = Un[e], t;
  for (t in n) if (n.hasOwnProperty(t) && t in $s) return Ll[e] = n[t];
  return e;
}
var As = rl("animationend"), Vs = rl("animationiteration"), Bs = rl("animationstart"), Hs = rl("transitionend"), Qs = /* @__PURE__ */ new Map(), oi = "abort auxClick cancel canPlay canPlayThrough click close contextMenu copy cut drag dragEnd dragEnter dragExit dragLeave dragOver dragStart drop durationChange emptied encrypted ended error gotPointerCapture input invalid keyDown keyPress keyUp load loadedData loadedMetadata loadStart lostPointerCapture mouseDown mouseMove mouseOut mouseOver mouseUp paste pause play playing pointerCancel pointerDown pointerMove pointerOut pointerOver pointerUp progress rateChange reset resize seeked seeking stalled submit suspend timeUpdate touchCancel touchEnd touchStart volumeChange scroll toggle touchMove waiting wheel".split(" ");
function pn(e, n) {
  Qs.set(e, n), Tn(n, [e]);
}
for (var Tl = 0; Tl < oi.length; Tl++) {
  var Rl = oi[Tl], Tf = Rl.toLowerCase(), Rf = Rl[0].toUpperCase() + Rl.slice(1);
  pn(Tf, "on" + Rf);
}
pn(As, "onAnimationEnd");
pn(Vs, "onAnimationIteration");
pn(Bs, "onAnimationStart");
pn("dblclick", "onDoubleClick");
pn("focusin", "onFocus");
pn("focusout", "onBlur");
pn(Hs, "onTransitionEnd");
Jn("onMouseEnter", ["mouseout", "mouseover"]);
Jn("onMouseLeave", ["mouseout", "mouseover"]);
Jn("onPointerEnter", ["pointerout", "pointerover"]);
Jn("onPointerLeave", ["pointerout", "pointerover"]);
Tn("onChange", "change click focusin focusout input keydown keyup selectionchange".split(" "));
Tn("onSelect", "focusout contextmenu dragend focusin keydown keyup mousedown mouseup selectionchange".split(" "));
Tn("onBeforeInput", ["compositionend", "keypress", "textInput", "paste"]);
Tn("onCompositionEnd", "compositionend focusout keydown keypress keyup mousedown".split(" "));
Tn("onCompositionStart", "compositionstart focusout keydown keypress keyup mousedown".split(" "));
Tn("onCompositionUpdate", "compositionupdate focusout keydown keypress keyup mousedown".split(" "));
var St = "abort canplay canplaythrough durationchange emptied encrypted ended error loadeddata loadedmetadata loadstart pause play playing progress ratechange resize seeked seeking stalled suspend timeupdate volumechange waiting".split(" "), Mf = new Set("cancel close invalid load scroll toggle".split(" ").concat(St));
function ui(e, n, t) {
  var r = e.type || "unknown-event";
  e.currentTarget = t, Lc(r, n, void 0, e), e.currentTarget = null;
}
function Ws(e, n) {
  n = (n & 4) !== 0;
  for (var t = 0; t < e.length; t++) {
    var r = e[t], l = r.event;
    r = r.listeners;
    e: {
      var o = void 0;
      if (n) for (var u = r.length - 1; 0 <= u; u--) {
        var i = r[u], s = i.instance, f = i.currentTarget;
        if (i = i.listener, s !== o && l.isPropagationStopped()) break e;
        ui(l, i, f), o = s;
      }
      else for (u = 0; u < r.length; u++) {
        if (i = r[u], s = i.instance, f = i.currentTarget, i = i.listener, s !== o && l.isPropagationStopped()) break e;
        ui(l, i, f), o = s;
      }
    }
  }
  if (Mr) throw e = oo, Mr = !1, oo = null, e;
}
function I(e, n) {
  var t = n[vo];
  t === void 0 && (t = n[vo] = /* @__PURE__ */ new Set());
  var r = e + "__bubble";
  t.has(r) || (Ks(n, e, 2, !1), t.add(r));
}
function Ml(e, n, t) {
  var r = 0;
  n && (r |= 4), Ks(t, e, r, n);
}
var ar = "_reactListening" + Math.random().toString(36).slice(2);
function jt(e) {
  if (!e[ar]) {
    e[ar] = !0, bi.forEach(function(t) {
      t !== "selectionchange" && (Mf.has(t) || Ml(t, !1, e), Ml(t, !0, e));
    });
    var n = e.nodeType === 9 ? e : e.ownerDocument;
    n === null || n[ar] || (n[ar] = !0, Ml("selectionchange", !1, n));
  }
}
function Ks(e, n, t, r) {
  switch (Ls(n)) {
    case 1:
      var l = Wc;
      break;
    case 4:
      l = Kc;
      break;
    default:
      l = Jo;
  }
  t = l.bind(null, n, t, e), l = void 0, !lo || n !== "touchstart" && n !== "touchmove" && n !== "wheel" || (l = !0), r ? l !== void 0 ? e.addEventListener(n, t, { capture: !0, passive: l }) : e.addEventListener(n, t, !0) : l !== void 0 ? e.addEventListener(n, t, { passive: l }) : e.addEventListener(n, t, !1);
}
function Ol(e, n, t, r, l) {
  var o = r;
  if (!(n & 1) && !(n & 2) && r !== null) e: for (; ; ) {
    if (r === null) return;
    var u = r.tag;
    if (u === 3 || u === 4) {
      var i = r.stateNode.containerInfo;
      if (i === l || i.nodeType === 8 && i.parentNode === l) break;
      if (u === 4) for (u = r.return; u !== null; ) {
        var s = u.tag;
        if ((s === 3 || s === 4) && (s = u.stateNode.containerInfo, s === l || s.nodeType === 8 && s.parentNode === l)) return;
        u = u.return;
      }
      for (; i !== null; ) {
        if (u = Sn(i), u === null) return;
        if (s = u.tag, s === 5 || s === 6) {
          r = o = u;
          continue e;
        }
        i = i.parentNode;
      }
    }
    r = r.return;
  }
  hs(function() {
    var f = o, h = Yo(t), m = [];
    e: {
      var p = Qs.get(e);
      if (p !== void 0) {
        var S = bo, v = e;
        switch (e) {
          case "keypress":
            if (Er(t) === 0) break e;
          case "keydown":
          case "keyup":
            S = sf;
            break;
          case "focusin":
            v = "focus", S = Pl;
            break;
          case "focusout":
            v = "blur", S = Pl;
            break;
          case "beforeblur":
          case "afterblur":
            S = Pl;
            break;
          case "click":
            if (t.button === 2) break e;
          case "auxclick":
          case "dblclick":
          case "mousedown":
          case "mousemove":
          case "mouseup":
          case "mouseout":
          case "mouseover":
          case "contextmenu":
            S = Xu;
            break;
          case "drag":
          case "dragend":
          case "dragenter":
          case "dragexit":
          case "dragleave":
          case "dragover":
          case "dragstart":
          case "drop":
            S = Gc;
            break;
          case "touchcancel":
          case "touchend":
          case "touchmove":
          case "touchstart":
            S = ff;
            break;
          case As:
          case Vs:
          case Bs:
            S = qc;
            break;
          case Hs:
            S = pf;
            break;
          case "scroll":
            S = Yc;
            break;
          case "wheel":
            S = hf;
            break;
          case "copy":
          case "cut":
          case "paste":
            S = ef;
            break;
          case "gotpointercapture":
          case "lostpointercapture":
          case "pointercancel":
          case "pointerdown":
          case "pointermove":
          case "pointerout":
          case "pointerover":
          case "pointerup":
            S = Zu;
        }
        var w = (n & 4) !== 0, N = !w && e === "scroll", c = w ? p !== null ? p + "Capture" : null : p;
        w = [];
        for (var a = f, d; a !== null; ) {
          d = a;
          var y = d.stateNode;
          if (d.tag === 5 && y !== null && (d = y, c !== null && (y = Mt(a, c), y != null && w.push($t(a, y, d)))), N) break;
          a = a.return;
        }
        0 < w.length && (p = new S(p, v, null, t, h), m.push({ event: p, listeners: w }));
      }
    }
    if (!(n & 7)) {
      e: {
        if (p = e === "mouseover" || e === "pointerover", S = e === "mouseout" || e === "pointerout", p && t !== to && (v = t.relatedTarget || t.fromElement) && (Sn(v) || v[We])) break e;
        if ((S || p) && (p = h.window === h ? h : (p = h.ownerDocument) ? p.defaultView || p.parentWindow : window, S ? (v = t.relatedTarget || t.toElement, S = f, v = v ? Sn(v) : null, v !== null && (N = Rn(v), v !== N || v.tag !== 5 && v.tag !== 6) && (v = null)) : (S = null, v = f), S !== v)) {
          if (w = Xu, y = "onMouseLeave", c = "onMouseEnter", a = "mouse", (e === "pointerout" || e === "pointerover") && (w = Zu, y = "onPointerLeave", c = "onPointerEnter", a = "pointer"), N = S == null ? p : jn(S), d = v == null ? p : jn(v), p = new w(y, a + "leave", S, t, h), p.target = N, p.relatedTarget = d, y = null, Sn(h) === f && (w = new w(c, a + "enter", v, t, h), w.target = d, w.relatedTarget = N, y = w), N = y, S && v) n: {
            for (w = S, c = v, a = 0, d = w; d; d = Mn(d)) a++;
            for (d = 0, y = c; y; y = Mn(y)) d++;
            for (; 0 < a - d; ) w = Mn(w), a--;
            for (; 0 < d - a; ) c = Mn(c), d--;
            for (; a--; ) {
              if (w === c || c !== null && w === c.alternate) break n;
              w = Mn(w), c = Mn(c);
            }
            w = null;
          }
          else w = null;
          S !== null && ii(m, p, S, w, !1), v !== null && N !== null && ii(m, N, v, w, !0);
        }
      }
      e: {
        if (p = f ? jn(f) : window, S = p.nodeName && p.nodeName.toLowerCase(), S === "select" || S === "input" && p.type === "file") var E = Ef;
        else if (bu(p)) if (Is) E = Pf;
        else {
          E = _f;
          var _ = Cf;
        }
        else (S = p.nodeName) && S.toLowerCase() === "input" && (p.type === "checkbox" || p.type === "radio") && (E = xf);
        if (E && (E = E(e, f))) {
          Ds(m, E, t, h);
          break e;
        }
        _ && _(e, p, f), e === "focusout" && (_ = p._wrapperState) && _.controlled && p.type === "number" && Jl(p, "number", p.value);
      }
      switch (_ = f ? jn(f) : window, e) {
        case "focusin":
          (bu(_) || _.contentEditable === "true") && (Fn = _, ao = f, xt = null);
          break;
        case "focusout":
          xt = ao = Fn = null;
          break;
        case "mousedown":
          co = !0;
          break;
        case "contextmenu":
        case "mouseup":
        case "dragend":
          co = !1, li(m, t, h);
          break;
        case "selectionchange":
          if (Lf) break;
        case "keydown":
        case "keyup":
          li(m, t, h);
      }
      var x;
      if (nu) e: {
        switch (e) {
          case "compositionstart":
            var P = "onCompositionStart";
            break e;
          case "compositionend":
            P = "onCompositionEnd";
            break e;
          case "compositionupdate":
            P = "onCompositionUpdate";
            break e;
        }
        P = void 0;
      }
      else In ? Ms(e, t) && (P = "onCompositionEnd") : e === "keydown" && t.keyCode === 229 && (P = "onCompositionStart");
      P && (Rs && t.locale !== "ko" && (In || P !== "onCompositionStart" ? P === "onCompositionEnd" && In && (x = Ts()) : (en = h, qo = "value" in en ? en.value : en.textContent, In = !0)), _ = Ur(f, P), 0 < _.length && (P = new Gu(P, e, null, t, h), m.push({ event: P, listeners: _ }), x ? P.data = x : (x = Os(t), x !== null && (P.data = x)))), (x = yf ? gf(e, t) : wf(e, t)) && (f = Ur(f, "onBeforeInput"), 0 < f.length && (h = new Gu("onBeforeInput", "beforeinput", null, t, h), m.push({ event: h, listeners: f }), h.data = x));
    }
    Ws(m, n);
  });
}
function $t(e, n, t) {
  return { instance: e, listener: n, currentTarget: t };
}
function Ur(e, n) {
  for (var t = n + "Capture", r = []; e !== null; ) {
    var l = e, o = l.stateNode;
    l.tag === 5 && o !== null && (l = o, o = Mt(e, t), o != null && r.unshift($t(e, o, l)), o = Mt(e, n), o != null && r.push($t(e, o, l))), e = e.return;
  }
  return r;
}
function Mn(e) {
  if (e === null) return null;
  do
    e = e.return;
  while (e && e.tag !== 5);
  return e || null;
}
function ii(e, n, t, r, l) {
  for (var o = n._reactName, u = []; t !== null && t !== r; ) {
    var i = t, s = i.alternate, f = i.stateNode;
    if (s !== null && s === r) break;
    i.tag === 5 && f !== null && (i = f, l ? (s = Mt(t, o), s != null && u.unshift($t(t, s, i))) : l || (s = Mt(t, o), s != null && u.push($t(t, s, i)))), t = t.return;
  }
  u.length !== 0 && e.push({ event: n, listeners: u });
}
var Of = /\r\n?/g, Df = /\u0000|\uFFFD/g;
function si(e) {
  return (typeof e == "string" ? e : "" + e).replace(Of, `
`).replace(Df, "");
}
function cr(e, n, t) {
  if (n = si(n), si(e) !== n && t) throw Error(g(425));
}
function jr() {
}
var fo = null, po = null;
function mo(e, n) {
  return e === "textarea" || e === "noscript" || typeof n.children == "string" || typeof n.children == "number" || typeof n.dangerouslySetInnerHTML == "object" && n.dangerouslySetInnerHTML !== null && n.dangerouslySetInnerHTML.__html != null;
}
var ho = typeof setTimeout == "function" ? setTimeout : void 0, If = typeof clearTimeout == "function" ? clearTimeout : void 0, ai = typeof Promise == "function" ? Promise : void 0, Ff = typeof queueMicrotask == "function" ? queueMicrotask : typeof ai < "u" ? function(e) {
  return ai.resolve(null).then(e).catch(Uf);
} : ho;
function Uf(e) {
  setTimeout(function() {
    throw e;
  });
}
function Dl(e, n) {
  var t = n, r = 0;
  do {
    var l = t.nextSibling;
    if (e.removeChild(t), l && l.nodeType === 8) if (t = l.data, t === "/$") {
      if (r === 0) {
        e.removeChild(l), It(n);
        return;
      }
      r--;
    } else t !== "$" && t !== "$?" && t !== "$!" || r++;
    t = l;
  } while (t);
  It(n);
}
function on(e) {
  for (; e != null; e = e.nextSibling) {
    var n = e.nodeType;
    if (n === 1 || n === 3) break;
    if (n === 8) {
      if (n = e.data, n === "$" || n === "$!" || n === "$?") break;
      if (n === "/$") return null;
    }
  }
  return e;
}
function ci(e) {
  e = e.previousSibling;
  for (var n = 0; e; ) {
    if (e.nodeType === 8) {
      var t = e.data;
      if (t === "$" || t === "$!" || t === "$?") {
        if (n === 0) return e;
        n--;
      } else t === "/$" && n++;
    }
    e = e.previousSibling;
  }
  return null;
}
var ut = Math.random().toString(36).slice(2), Fe = "__reactFiber$" + ut, At = "__reactProps$" + ut, We = "__reactContainer$" + ut, vo = "__reactEvents$" + ut, jf = "__reactListeners$" + ut, $f = "__reactHandles$" + ut;
function Sn(e) {
  var n = e[Fe];
  if (n) return n;
  for (var t = e.parentNode; t; ) {
    if (n = t[We] || t[Fe]) {
      if (t = n.alternate, n.child !== null || t !== null && t.child !== null) for (e = ci(e); e !== null; ) {
        if (t = e[Fe]) return t;
        e = ci(e);
      }
      return n;
    }
    e = t, t = e.parentNode;
  }
  return null;
}
function Zt(e) {
  return e = e[Fe] || e[We], !e || e.tag !== 5 && e.tag !== 6 && e.tag !== 13 && e.tag !== 3 ? null : e;
}
function jn(e) {
  if (e.tag === 5 || e.tag === 6) return e.stateNode;
  throw Error(g(33));
}
function ll(e) {
  return e[At] || null;
}
var yo = [], $n = -1;
function mn(e) {
  return { current: e };
}
function F(e) {
  0 > $n || (e.current = yo[$n], yo[$n] = null, $n--);
}
function D(e, n) {
  $n++, yo[$n] = e.current, e.current = n;
}
var dn = {}, le = mn(dn), fe = mn(!1), xn = dn;
function qn(e, n) {
  var t = e.type.contextTypes;
  if (!t) return dn;
  var r = e.stateNode;
  if (r && r.__reactInternalMemoizedUnmaskedChildContext === n) return r.__reactInternalMemoizedMaskedChildContext;
  var l = {}, o;
  for (o in t) l[o] = n[o];
  return r && (e = e.stateNode, e.__reactInternalMemoizedUnmaskedChildContext = n, e.__reactInternalMemoizedMaskedChildContext = l), l;
}
function de(e) {
  return e = e.childContextTypes, e != null;
}
function $r() {
  F(fe), F(le);
}
function fi(e, n, t) {
  if (le.current !== dn) throw Error(g(168));
  D(le, n), D(fe, t);
}
function Ys(e, n, t) {
  var r = e.stateNode;
  if (n = n.childContextTypes, typeof r.getChildContext != "function") return t;
  r = r.getChildContext();
  for (var l in r) if (!(l in n)) throw Error(g(108, Ec(e) || "Unknown", l));
  return A({}, t, r);
}
function Ar(e) {
  return e = (e = e.stateNode) && e.__reactInternalMemoizedMergedChildContext || dn, xn = le.current, D(le, e), D(fe, fe.current), !0;
}
function di(e, n, t) {
  var r = e.stateNode;
  if (!r) throw Error(g(169));
  t ? (e = Ys(e, n, xn), r.__reactInternalMemoizedMergedChildContext = e, F(fe), F(le), D(le, e)) : F(fe), D(fe, t);
}
var Ae = null, ol = !1, Il = !1;
function Xs(e) {
  Ae === null ? Ae = [e] : Ae.push(e);
}
function Af(e) {
  ol = !0, Xs(e);
}
function hn() {
  if (!Il && Ae !== null) {
    Il = !0;
    var e = 0, n = O;
    try {
      var t = Ae;
      for (O = 1; e < t.length; e++) {
        var r = t[e];
        do
          r = r(!0);
        while (r !== null);
      }
      Ae = null, ol = !1;
    } catch (l) {
      throw Ae !== null && (Ae = Ae.slice(e + 1)), ws(Xo, hn), l;
    } finally {
      O = n, Il = !1;
    }
  }
  return null;
}
var An = [], Vn = 0, Vr = null, Br = 0, Se = [], ke = 0, Pn = null, Ve = 1, Be = "";
function gn(e, n) {
  An[Vn++] = Br, An[Vn++] = Vr, Vr = e, Br = n;
}
function Gs(e, n, t) {
  Se[ke++] = Ve, Se[ke++] = Be, Se[ke++] = Pn, Pn = e;
  var r = Ve;
  e = Be;
  var l = 32 - Re(r) - 1;
  r &= ~(1 << l), t += 1;
  var o = 32 - Re(n) + l;
  if (30 < o) {
    var u = l - l % 5;
    o = (r & (1 << u) - 1).toString(32), r >>= u, l -= u, Ve = 1 << 32 - Re(n) + l | t << l | r, Be = o + e;
  } else Ve = 1 << o | t << l | r, Be = e;
}
function ru(e) {
  e.return !== null && (gn(e, 1), Gs(e, 1, 0));
}
function lu(e) {
  for (; e === Vr; ) Vr = An[--Vn], An[Vn] = null, Br = An[--Vn], An[Vn] = null;
  for (; e === Pn; ) Pn = Se[--ke], Se[ke] = null, Be = Se[--ke], Se[ke] = null, Ve = Se[--ke], Se[ke] = null;
}
var ve = null, he = null, U = !1, Te = null;
function Zs(e, n) {
  var t = Ee(5, null, null, 0);
  t.elementType = "DELETED", t.stateNode = n, t.return = e, n = e.deletions, n === null ? (e.deletions = [t], e.flags |= 16) : n.push(t);
}
function pi(e, n) {
  switch (e.tag) {
    case 5:
      var t = e.type;
      return n = n.nodeType !== 1 || t.toLowerCase() !== n.nodeName.toLowerCase() ? null : n, n !== null ? (e.stateNode = n, ve = e, he = on(n.firstChild), !0) : !1;
    case 6:
      return n = e.pendingProps === "" || n.nodeType !== 3 ? null : n, n !== null ? (e.stateNode = n, ve = e, he = null, !0) : !1;
    case 13:
      return n = n.nodeType !== 8 ? null : n, n !== null ? (t = Pn !== null ? { id: Ve, overflow: Be } : null, e.memoizedState = { dehydrated: n, treeContext: t, retryLane: 1073741824 }, t = Ee(18, null, null, 0), t.stateNode = n, t.return = e, e.child = t, ve = e, he = null, !0) : !1;
    default:
      return !1;
  }
}
function go(e) {
  return (e.mode & 1) !== 0 && (e.flags & 128) === 0;
}
function wo(e) {
  if (U) {
    var n = he;
    if (n) {
      var t = n;
      if (!pi(e, n)) {
        if (go(e)) throw Error(g(418));
        n = on(t.nextSibling);
        var r = ve;
        n && pi(e, n) ? Zs(r, t) : (e.flags = e.flags & -4097 | 2, U = !1, ve = e);
      }
    } else {
      if (go(e)) throw Error(g(418));
      e.flags = e.flags & -4097 | 2, U = !1, ve = e;
    }
  }
}
function mi(e) {
  for (e = e.return; e !== null && e.tag !== 5 && e.tag !== 3 && e.tag !== 13; ) e = e.return;
  ve = e;
}
function fr(e) {
  if (e !== ve) return !1;
  if (!U) return mi(e), U = !0, !1;
  var n;
  if ((n = e.tag !== 3) && !(n = e.tag !== 5) && (n = e.type, n = n !== "head" && n !== "body" && !mo(e.type, e.memoizedProps)), n && (n = he)) {
    if (go(e)) throw Js(), Error(g(418));
    for (; n; ) Zs(e, n), n = on(n.nextSibling);
  }
  if (mi(e), e.tag === 13) {
    if (e = e.memoizedState, e = e !== null ? e.dehydrated : null, !e) throw Error(g(317));
    e: {
      for (e = e.nextSibling, n = 0; e; ) {
        if (e.nodeType === 8) {
          var t = e.data;
          if (t === "/$") {
            if (n === 0) {
              he = on(e.nextSibling);
              break e;
            }
            n--;
          } else t !== "$" && t !== "$!" && t !== "$?" || n++;
        }
        e = e.nextSibling;
      }
      he = null;
    }
  } else he = ve ? on(e.stateNode.nextSibling) : null;
  return !0;
}
function Js() {
  for (var e = he; e; ) e = on(e.nextSibling);
}
function bn() {
  he = ve = null, U = !1;
}
function ou(e) {
  Te === null ? Te = [e] : Te.push(e);
}
var Vf = Xe.ReactCurrentBatchConfig;
function mt(e, n, t) {
  if (e = t.ref, e !== null && typeof e != "function" && typeof e != "object") {
    if (t._owner) {
      if (t = t._owner, t) {
        if (t.tag !== 1) throw Error(g(309));
        var r = t.stateNode;
      }
      if (!r) throw Error(g(147, e));
      var l = r, o = "" + e;
      return n !== null && n.ref !== null && typeof n.ref == "function" && n.ref._stringRef === o ? n.ref : (n = function(u) {
        var i = l.refs;
        u === null ? delete i[o] : i[o] = u;
      }, n._stringRef = o, n);
    }
    if (typeof e != "string") throw Error(g(284));
    if (!t._owner) throw Error(g(290, e));
  }
  return e;
}
function dr(e, n) {
  throw e = Object.prototype.toString.call(n), Error(g(31, e === "[object Object]" ? "object with keys {" + Object.keys(n).join(", ") + "}" : e));
}
function hi(e) {
  var n = e._init;
  return n(e._payload);
}
function qs(e) {
  function n(c, a) {
    if (e) {
      var d = c.deletions;
      d === null ? (c.deletions = [a], c.flags |= 16) : d.push(a);
    }
  }
  function t(c, a) {
    if (!e) return null;
    for (; a !== null; ) n(c, a), a = a.sibling;
    return null;
  }
  function r(c, a) {
    for (c = /* @__PURE__ */ new Map(); a !== null; ) a.key !== null ? c.set(a.key, a) : c.set(a.index, a), a = a.sibling;
    return c;
  }
  function l(c, a) {
    return c = cn(c, a), c.index = 0, c.sibling = null, c;
  }
  function o(c, a, d) {
    return c.index = d, e ? (d = c.alternate, d !== null ? (d = d.index, d < a ? (c.flags |= 2, a) : d) : (c.flags |= 2, a)) : (c.flags |= 1048576, a);
  }
  function u(c) {
    return e && c.alternate === null && (c.flags |= 2), c;
  }
  function i(c, a, d, y) {
    return a === null || a.tag !== 6 ? (a = Bl(d, c.mode, y), a.return = c, a) : (a = l(a, d), a.return = c, a);
  }
  function s(c, a, d, y) {
    var E = d.type;
    return E === Dn ? h(c, a, d.props.children, y, d.key) : a !== null && (a.elementType === E || typeof E == "object" && E !== null && E.$$typeof === Ze && hi(E) === a.type) ? (y = l(a, d.props), y.ref = mt(c, a, d), y.return = c, y) : (y = Lr(d.type, d.key, d.props, null, c.mode, y), y.ref = mt(c, a, d), y.return = c, y);
  }
  function f(c, a, d, y) {
    return a === null || a.tag !== 4 || a.stateNode.containerInfo !== d.containerInfo || a.stateNode.implementation !== d.implementation ? (a = Hl(d, c.mode, y), a.return = c, a) : (a = l(a, d.children || []), a.return = c, a);
  }
  function h(c, a, d, y, E) {
    return a === null || a.tag !== 7 ? (a = _n(d, c.mode, y, E), a.return = c, a) : (a = l(a, d), a.return = c, a);
  }
  function m(c, a, d) {
    if (typeof a == "string" && a !== "" || typeof a == "number") return a = Bl("" + a, c.mode, d), a.return = c, a;
    if (typeof a == "object" && a !== null) {
      switch (a.$$typeof) {
        case nr:
          return d = Lr(a.type, a.key, a.props, null, c.mode, d), d.ref = mt(c, null, a), d.return = c, d;
        case On:
          return a = Hl(a, c.mode, d), a.return = c, a;
        case Ze:
          var y = a._init;
          return m(c, y(a._payload), d);
      }
      if (gt(a) || at(a)) return a = _n(a, c.mode, d, null), a.return = c, a;
      dr(c, a);
    }
    return null;
  }
  function p(c, a, d, y) {
    var E = a !== null ? a.key : null;
    if (typeof d == "string" && d !== "" || typeof d == "number") return E !== null ? null : i(c, a, "" + d, y);
    if (typeof d == "object" && d !== null) {
      switch (d.$$typeof) {
        case nr:
          return d.key === E ? s(c, a, d, y) : null;
        case On:
          return d.key === E ? f(c, a, d, y) : null;
        case Ze:
          return E = d._init, p(
            c,
            a,
            E(d._payload),
            y
          );
      }
      if (gt(d) || at(d)) return E !== null ? null : h(c, a, d, y, null);
      dr(c, d);
    }
    return null;
  }
  function S(c, a, d, y, E) {
    if (typeof y == "string" && y !== "" || typeof y == "number") return c = c.get(d) || null, i(a, c, "" + y, E);
    if (typeof y == "object" && y !== null) {
      switch (y.$$typeof) {
        case nr:
          return c = c.get(y.key === null ? d : y.key) || null, s(a, c, y, E);
        case On:
          return c = c.get(y.key === null ? d : y.key) || null, f(a, c, y, E);
        case Ze:
          var _ = y._init;
          return S(c, a, d, _(y._payload), E);
      }
      if (gt(y) || at(y)) return c = c.get(d) || null, h(a, c, y, E, null);
      dr(a, y);
    }
    return null;
  }
  function v(c, a, d, y) {
    for (var E = null, _ = null, x = a, P = a = 0, B = null; x !== null && P < d.length; P++) {
      x.index > P ? (B = x, x = null) : B = x.sibling;
      var R = p(c, x, d[P], y);
      if (R === null) {
        x === null && (x = B);
        break;
      }
      e && x && R.alternate === null && n(c, x), a = o(R, a, P), _ === null ? E = R : _.sibling = R, _ = R, x = B;
    }
    if (P === d.length) return t(c, x), U && gn(c, P), E;
    if (x === null) {
      for (; P < d.length; P++) x = m(c, d[P], y), x !== null && (a = o(x, a, P), _ === null ? E = x : _.sibling = x, _ = x);
      return U && gn(c, P), E;
    }
    for (x = r(c, x); P < d.length; P++) B = S(x, c, P, d[P], y), B !== null && (e && B.alternate !== null && x.delete(B.key === null ? P : B.key), a = o(B, a, P), _ === null ? E = B : _.sibling = B, _ = B);
    return e && x.forEach(function(Pe) {
      return n(c, Pe);
    }), U && gn(c, P), E;
  }
  function w(c, a, d, y) {
    var E = at(d);
    if (typeof E != "function") throw Error(g(150));
    if (d = E.call(d), d == null) throw Error(g(151));
    for (var _ = E = null, x = a, P = a = 0, B = null, R = d.next(); x !== null && !R.done; P++, R = d.next()) {
      x.index > P ? (B = x, x = null) : B = x.sibling;
      var Pe = p(c, x, R.value, y);
      if (Pe === null) {
        x === null && (x = B);
        break;
      }
      e && x && Pe.alternate === null && n(c, x), a = o(Pe, a, P), _ === null ? E = Pe : _.sibling = Pe, _ = Pe, x = B;
    }
    if (R.done) return t(
      c,
      x
    ), U && gn(c, P), E;
    if (x === null) {
      for (; !R.done; P++, R = d.next()) R = m(c, R.value, y), R !== null && (a = o(R, a, P), _ === null ? E = R : _.sibling = R, _ = R);
      return U && gn(c, P), E;
    }
    for (x = r(c, x); !R.done; P++, R = d.next()) R = S(x, c, P, R.value, y), R !== null && (e && R.alternate !== null && x.delete(R.key === null ? P : R.key), a = o(R, a, P), _ === null ? E = R : _.sibling = R, _ = R);
    return e && x.forEach(function(it) {
      return n(c, it);
    }), U && gn(c, P), E;
  }
  function N(c, a, d, y) {
    if (typeof d == "object" && d !== null && d.type === Dn && d.key === null && (d = d.props.children), typeof d == "object" && d !== null) {
      switch (d.$$typeof) {
        case nr:
          e: {
            for (var E = d.key, _ = a; _ !== null; ) {
              if (_.key === E) {
                if (E = d.type, E === Dn) {
                  if (_.tag === 7) {
                    t(c, _.sibling), a = l(_, d.props.children), a.return = c, c = a;
                    break e;
                  }
                } else if (_.elementType === E || typeof E == "object" && E !== null && E.$$typeof === Ze && hi(E) === _.type) {
                  t(c, _.sibling), a = l(_, d.props), a.ref = mt(c, _, d), a.return = c, c = a;
                  break e;
                }
                t(c, _);
                break;
              } else n(c, _);
              _ = _.sibling;
            }
            d.type === Dn ? (a = _n(d.props.children, c.mode, y, d.key), a.return = c, c = a) : (y = Lr(d.type, d.key, d.props, null, c.mode, y), y.ref = mt(c, a, d), y.return = c, c = y);
          }
          return u(c);
        case On:
          e: {
            for (_ = d.key; a !== null; ) {
              if (a.key === _) if (a.tag === 4 && a.stateNode.containerInfo === d.containerInfo && a.stateNode.implementation === d.implementation) {
                t(c, a.sibling), a = l(a, d.children || []), a.return = c, c = a;
                break e;
              } else {
                t(c, a);
                break;
              }
              else n(c, a);
              a = a.sibling;
            }
            a = Hl(d, c.mode, y), a.return = c, c = a;
          }
          return u(c);
        case Ze:
          return _ = d._init, N(c, a, _(d._payload), y);
      }
      if (gt(d)) return v(c, a, d, y);
      if (at(d)) return w(c, a, d, y);
      dr(c, d);
    }
    return typeof d == "string" && d !== "" || typeof d == "number" ? (d = "" + d, a !== null && a.tag === 6 ? (t(c, a.sibling), a = l(a, d), a.return = c, c = a) : (t(c, a), a = Bl(d, c.mode, y), a.return = c, c = a), u(c)) : t(c, a);
  }
  return N;
}
var et = qs(!0), bs = qs(!1), Hr = mn(null), Qr = null, Bn = null, uu = null;
function iu() {
  uu = Bn = Qr = null;
}
function su(e) {
  var n = Hr.current;
  F(Hr), e._currentValue = n;
}
function So(e, n, t) {
  for (; e !== null; ) {
    var r = e.alternate;
    if ((e.childLanes & n) !== n ? (e.childLanes |= n, r !== null && (r.childLanes |= n)) : r !== null && (r.childLanes & n) !== n && (r.childLanes |= n), e === t) break;
    e = e.return;
  }
}
function Gn(e, n) {
  Qr = e, uu = Bn = null, e = e.dependencies, e !== null && e.firstContext !== null && (e.lanes & n && (ce = !0), e.firstContext = null);
}
function _e(e) {
  var n = e._currentValue;
  if (uu !== e) if (e = { context: e, memoizedValue: n, next: null }, Bn === null) {
    if (Qr === null) throw Error(g(308));
    Bn = e, Qr.dependencies = { lanes: 0, firstContext: e };
  } else Bn = Bn.next = e;
  return n;
}
var kn = null;
function au(e) {
  kn === null ? kn = [e] : kn.push(e);
}
function ea(e, n, t, r) {
  var l = n.interleaved;
  return l === null ? (t.next = t, au(n)) : (t.next = l.next, l.next = t), n.interleaved = t, Ke(e, r);
}
function Ke(e, n) {
  e.lanes |= n;
  var t = e.alternate;
  for (t !== null && (t.lanes |= n), t = e, e = e.return; e !== null; ) e.childLanes |= n, t = e.alternate, t !== null && (t.childLanes |= n), t = e, e = e.return;
  return t.tag === 3 ? t.stateNode : null;
}
var Je = !1;
function cu(e) {
  e.updateQueue = { baseState: e.memoizedState, firstBaseUpdate: null, lastBaseUpdate: null, shared: { pending: null, interleaved: null, lanes: 0 }, effects: null };
}
function na(e, n) {
  e = e.updateQueue, n.updateQueue === e && (n.updateQueue = { baseState: e.baseState, firstBaseUpdate: e.firstBaseUpdate, lastBaseUpdate: e.lastBaseUpdate, shared: e.shared, effects: e.effects });
}
function He(e, n) {
  return { eventTime: e, lane: n, tag: 0, payload: null, callback: null, next: null };
}
function un(e, n, t) {
  var r = e.updateQueue;
  if (r === null) return null;
  if (r = r.shared, M & 2) {
    var l = r.pending;
    return l === null ? n.next = n : (n.next = l.next, l.next = n), r.pending = n, Ke(e, t);
  }
  return l = r.interleaved, l === null ? (n.next = n, au(r)) : (n.next = l.next, l.next = n), r.interleaved = n, Ke(e, t);
}
function Cr(e, n, t) {
  if (n = n.updateQueue, n !== null && (n = n.shared, (t & 4194240) !== 0)) {
    var r = n.lanes;
    r &= e.pendingLanes, t |= r, n.lanes = t, Go(e, t);
  }
}
function vi(e, n) {
  var t = e.updateQueue, r = e.alternate;
  if (r !== null && (r = r.updateQueue, t === r)) {
    var l = null, o = null;
    if (t = t.firstBaseUpdate, t !== null) {
      do {
        var u = { eventTime: t.eventTime, lane: t.lane, tag: t.tag, payload: t.payload, callback: t.callback, next: null };
        o === null ? l = o = u : o = o.next = u, t = t.next;
      } while (t !== null);
      o === null ? l = o = n : o = o.next = n;
    } else l = o = n;
    t = { baseState: r.baseState, firstBaseUpdate: l, lastBaseUpdate: o, shared: r.shared, effects: r.effects }, e.updateQueue = t;
    return;
  }
  e = t.lastBaseUpdate, e === null ? t.firstBaseUpdate = n : e.next = n, t.lastBaseUpdate = n;
}
function Wr(e, n, t, r) {
  var l = e.updateQueue;
  Je = !1;
  var o = l.firstBaseUpdate, u = l.lastBaseUpdate, i = l.shared.pending;
  if (i !== null) {
    l.shared.pending = null;
    var s = i, f = s.next;
    s.next = null, u === null ? o = f : u.next = f, u = s;
    var h = e.alternate;
    h !== null && (h = h.updateQueue, i = h.lastBaseUpdate, i !== u && (i === null ? h.firstBaseUpdate = f : i.next = f, h.lastBaseUpdate = s));
  }
  if (o !== null) {
    var m = l.baseState;
    u = 0, h = f = s = null, i = o;
    do {
      var p = i.lane, S = i.eventTime;
      if ((r & p) === p) {
        h !== null && (h = h.next = {
          eventTime: S,
          lane: 0,
          tag: i.tag,
          payload: i.payload,
          callback: i.callback,
          next: null
        });
        e: {
          var v = e, w = i;
          switch (p = n, S = t, w.tag) {
            case 1:
              if (v = w.payload, typeof v == "function") {
                m = v.call(S, m, p);
                break e;
              }
              m = v;
              break e;
            case 3:
              v.flags = v.flags & -65537 | 128;
            case 0:
              if (v = w.payload, p = typeof v == "function" ? v.call(S, m, p) : v, p == null) break e;
              m = A({}, m, p);
              break e;
            case 2:
              Je = !0;
          }
        }
        i.callback !== null && i.lane !== 0 && (e.flags |= 64, p = l.effects, p === null ? l.effects = [i] : p.push(i));
      } else S = { eventTime: S, lane: p, tag: i.tag, payload: i.payload, callback: i.callback, next: null }, h === null ? (f = h = S, s = m) : h = h.next = S, u |= p;
      if (i = i.next, i === null) {
        if (i = l.shared.pending, i === null) break;
        p = i, i = p.next, p.next = null, l.lastBaseUpdate = p, l.shared.pending = null;
      }
    } while (!0);
    if (h === null && (s = m), l.baseState = s, l.firstBaseUpdate = f, l.lastBaseUpdate = h, n = l.shared.interleaved, n !== null) {
      l = n;
      do
        u |= l.lane, l = l.next;
      while (l !== n);
    } else o === null && (l.shared.lanes = 0);
    zn |= u, e.lanes = u, e.memoizedState = m;
  }
}
function yi(e, n, t) {
  if (e = n.effects, n.effects = null, e !== null) for (n = 0; n < e.length; n++) {
    var r = e[n], l = r.callback;
    if (l !== null) {
      if (r.callback = null, r = t, typeof l != "function") throw Error(g(191, l));
      l.call(r);
    }
  }
}
var Jt = {}, je = mn(Jt), Vt = mn(Jt), Bt = mn(Jt);
function En(e) {
  if (e === Jt) throw Error(g(174));
  return e;
}
function fu(e, n) {
  switch (D(Bt, n), D(Vt, e), D(je, Jt), e = n.nodeType, e) {
    case 9:
    case 11:
      n = (n = n.documentElement) ? n.namespaceURI : bl(null, "");
      break;
    default:
      e = e === 8 ? n.parentNode : n, n = e.namespaceURI || null, e = e.tagName, n = bl(n, e);
  }
  F(je), D(je, n);
}
function nt() {
  F(je), F(Vt), F(Bt);
}
function ta(e) {
  En(Bt.current);
  var n = En(je.current), t = bl(n, e.type);
  n !== t && (D(Vt, e), D(je, t));
}
function du(e) {
  Vt.current === e && (F(je), F(Vt));
}
var j = mn(0);
function Kr(e) {
  for (var n = e; n !== null; ) {
    if (n.tag === 13) {
      var t = n.memoizedState;
      if (t !== null && (t = t.dehydrated, t === null || t.data === "$?" || t.data === "$!")) return n;
    } else if (n.tag === 19 && n.memoizedProps.revealOrder !== void 0) {
      if (n.flags & 128) return n;
    } else if (n.child !== null) {
      n.child.return = n, n = n.child;
      continue;
    }
    if (n === e) break;
    for (; n.sibling === null; ) {
      if (n.return === null || n.return === e) return null;
      n = n.return;
    }
    n.sibling.return = n.return, n = n.sibling;
  }
  return null;
}
var Fl = [];
function pu() {
  for (var e = 0; e < Fl.length; e++) Fl[e]._workInProgressVersionPrimary = null;
  Fl.length = 0;
}
var _r = Xe.ReactCurrentDispatcher, Ul = Xe.ReactCurrentBatchConfig, Nn = 0, $ = null, K = null, G = null, Yr = !1, Pt = !1, Ht = 0, Bf = 0;
function ee() {
  throw Error(g(321));
}
function mu(e, n) {
  if (n === null) return !1;
  for (var t = 0; t < n.length && t < e.length; t++) if (!Oe(e[t], n[t])) return !1;
  return !0;
}
function hu(e, n, t, r, l, o) {
  if (Nn = o, $ = n, n.memoizedState = null, n.updateQueue = null, n.lanes = 0, _r.current = e === null || e.memoizedState === null ? Kf : Yf, e = t(r, l), Pt) {
    o = 0;
    do {
      if (Pt = !1, Ht = 0, 25 <= o) throw Error(g(301));
      o += 1, G = K = null, n.updateQueue = null, _r.current = Xf, e = t(r, l);
    } while (Pt);
  }
  if (_r.current = Xr, n = K !== null && K.next !== null, Nn = 0, G = K = $ = null, Yr = !1, n) throw Error(g(300));
  return e;
}
function vu() {
  var e = Ht !== 0;
  return Ht = 0, e;
}
function Ie() {
  var e = { memoizedState: null, baseState: null, baseQueue: null, queue: null, next: null };
  return G === null ? $.memoizedState = G = e : G = G.next = e, G;
}
function xe() {
  if (K === null) {
    var e = $.alternate;
    e = e !== null ? e.memoizedState : null;
  } else e = K.next;
  var n = G === null ? $.memoizedState : G.next;
  if (n !== null) G = n, K = e;
  else {
    if (e === null) throw Error(g(310));
    K = e, e = { memoizedState: K.memoizedState, baseState: K.baseState, baseQueue: K.baseQueue, queue: K.queue, next: null }, G === null ? $.memoizedState = G = e : G = G.next = e;
  }
  return G;
}
function Qt(e, n) {
  return typeof n == "function" ? n(e) : n;
}
function jl(e) {
  var n = xe(), t = n.queue;
  if (t === null) throw Error(g(311));
  t.lastRenderedReducer = e;
  var r = K, l = r.baseQueue, o = t.pending;
  if (o !== null) {
    if (l !== null) {
      var u = l.next;
      l.next = o.next, o.next = u;
    }
    r.baseQueue = l = o, t.pending = null;
  }
  if (l !== null) {
    o = l.next, r = r.baseState;
    var i = u = null, s = null, f = o;
    do {
      var h = f.lane;
      if ((Nn & h) === h) s !== null && (s = s.next = { lane: 0, action: f.action, hasEagerState: f.hasEagerState, eagerState: f.eagerState, next: null }), r = f.hasEagerState ? f.eagerState : e(r, f.action);
      else {
        var m = {
          lane: h,
          action: f.action,
          hasEagerState: f.hasEagerState,
          eagerState: f.eagerState,
          next: null
        };
        s === null ? (i = s = m, u = r) : s = s.next = m, $.lanes |= h, zn |= h;
      }
      f = f.next;
    } while (f !== null && f !== o);
    s === null ? u = r : s.next = i, Oe(r, n.memoizedState) || (ce = !0), n.memoizedState = r, n.baseState = u, n.baseQueue = s, t.lastRenderedState = r;
  }
  if (e = t.interleaved, e !== null) {
    l = e;
    do
      o = l.lane, $.lanes |= o, zn |= o, l = l.next;
    while (l !== e);
  } else l === null && (t.lanes = 0);
  return [n.memoizedState, t.dispatch];
}
function $l(e) {
  var n = xe(), t = n.queue;
  if (t === null) throw Error(g(311));
  t.lastRenderedReducer = e;
  var r = t.dispatch, l = t.pending, o = n.memoizedState;
  if (l !== null) {
    t.pending = null;
    var u = l = l.next;
    do
      o = e(o, u.action), u = u.next;
    while (u !== l);
    Oe(o, n.memoizedState) || (ce = !0), n.memoizedState = o, n.baseQueue === null && (n.baseState = o), t.lastRenderedState = o;
  }
  return [o, r];
}
function ra() {
}
function la(e, n) {
  var t = $, r = xe(), l = n(), o = !Oe(r.memoizedState, l);
  if (o && (r.memoizedState = l, ce = !0), r = r.queue, yu(ia.bind(null, t, r, e), [e]), r.getSnapshot !== n || o || G !== null && G.memoizedState.tag & 1) {
    if (t.flags |= 2048, Wt(9, ua.bind(null, t, r, l, n), void 0, null), Z === null) throw Error(g(349));
    Nn & 30 || oa(t, n, l);
  }
  return l;
}
function oa(e, n, t) {
  e.flags |= 16384, e = { getSnapshot: n, value: t }, n = $.updateQueue, n === null ? (n = { lastEffect: null, stores: null }, $.updateQueue = n, n.stores = [e]) : (t = n.stores, t === null ? n.stores = [e] : t.push(e));
}
function ua(e, n, t, r) {
  n.value = t, n.getSnapshot = r, sa(n) && aa(e);
}
function ia(e, n, t) {
  return t(function() {
    sa(n) && aa(e);
  });
}
function sa(e) {
  var n = e.getSnapshot;
  e = e.value;
  try {
    var t = n();
    return !Oe(e, t);
  } catch {
    return !0;
  }
}
function aa(e) {
  var n = Ke(e, 1);
  n !== null && Me(n, e, 1, -1);
}
function gi(e) {
  var n = Ie();
  return typeof e == "function" && (e = e()), n.memoizedState = n.baseState = e, e = { pending: null, interleaved: null, lanes: 0, dispatch: null, lastRenderedReducer: Qt, lastRenderedState: e }, n.queue = e, e = e.dispatch = Wf.bind(null, $, e), [n.memoizedState, e];
}
function Wt(e, n, t, r) {
  return e = { tag: e, create: n, destroy: t, deps: r, next: null }, n = $.updateQueue, n === null ? (n = { lastEffect: null, stores: null }, $.updateQueue = n, n.lastEffect = e.next = e) : (t = n.lastEffect, t === null ? n.lastEffect = e.next = e : (r = t.next, t.next = e, e.next = r, n.lastEffect = e)), e;
}
function ca() {
  return xe().memoizedState;
}
function xr(e, n, t, r) {
  var l = Ie();
  $.flags |= e, l.memoizedState = Wt(1 | n, t, void 0, r === void 0 ? null : r);
}
function ul(e, n, t, r) {
  var l = xe();
  r = r === void 0 ? null : r;
  var o = void 0;
  if (K !== null) {
    var u = K.memoizedState;
    if (o = u.destroy, r !== null && mu(r, u.deps)) {
      l.memoizedState = Wt(n, t, o, r);
      return;
    }
  }
  $.flags |= e, l.memoizedState = Wt(1 | n, t, o, r);
}
function wi(e, n) {
  return xr(8390656, 8, e, n);
}
function yu(e, n) {
  return ul(2048, 8, e, n);
}
function fa(e, n) {
  return ul(4, 2, e, n);
}
function da(e, n) {
  return ul(4, 4, e, n);
}
function pa(e, n) {
  if (typeof n == "function") return e = e(), n(e), function() {
    n(null);
  };
  if (n != null) return e = e(), n.current = e, function() {
    n.current = null;
  };
}
function ma(e, n, t) {
  return t = t != null ? t.concat([e]) : null, ul(4, 4, pa.bind(null, n, e), t);
}
function gu() {
}
function ha(e, n) {
  var t = xe();
  n = n === void 0 ? null : n;
  var r = t.memoizedState;
  return r !== null && n !== null && mu(n, r[1]) ? r[0] : (t.memoizedState = [e, n], e);
}
function va(e, n) {
  var t = xe();
  n = n === void 0 ? null : n;
  var r = t.memoizedState;
  return r !== null && n !== null && mu(n, r[1]) ? r[0] : (e = e(), t.memoizedState = [e, n], e);
}
function ya(e, n, t) {
  return Nn & 21 ? (Oe(t, n) || (t = Es(), $.lanes |= t, zn |= t, e.baseState = !0), n) : (e.baseState && (e.baseState = !1, ce = !0), e.memoizedState = t);
}
function Hf(e, n) {
  var t = O;
  O = t !== 0 && 4 > t ? t : 4, e(!0);
  var r = Ul.transition;
  Ul.transition = {};
  try {
    e(!1), n();
  } finally {
    O = t, Ul.transition = r;
  }
}
function ga() {
  return xe().memoizedState;
}
function Qf(e, n, t) {
  var r = an(e);
  if (t = { lane: r, action: t, hasEagerState: !1, eagerState: null, next: null }, wa(e)) Sa(n, t);
  else if (t = ea(e, n, t, r), t !== null) {
    var l = ue();
    Me(t, e, r, l), ka(t, n, r);
  }
}
function Wf(e, n, t) {
  var r = an(e), l = { lane: r, action: t, hasEagerState: !1, eagerState: null, next: null };
  if (wa(e)) Sa(n, l);
  else {
    var o = e.alternate;
    if (e.lanes === 0 && (o === null || o.lanes === 0) && (o = n.lastRenderedReducer, o !== null)) try {
      var u = n.lastRenderedState, i = o(u, t);
      if (l.hasEagerState = !0, l.eagerState = i, Oe(i, u)) {
        var s = n.interleaved;
        s === null ? (l.next = l, au(n)) : (l.next = s.next, s.next = l), n.interleaved = l;
        return;
      }
    } catch {
    } finally {
    }
    t = ea(e, n, l, r), t !== null && (l = ue(), Me(t, e, r, l), ka(t, n, r));
  }
}
function wa(e) {
  var n = e.alternate;
  return e === $ || n !== null && n === $;
}
function Sa(e, n) {
  Pt = Yr = !0;
  var t = e.pending;
  t === null ? n.next = n : (n.next = t.next, t.next = n), e.pending = n;
}
function ka(e, n, t) {
  if (t & 4194240) {
    var r = n.lanes;
    r &= e.pendingLanes, t |= r, n.lanes = t, Go(e, t);
  }
}
var Xr = { readContext: _e, useCallback: ee, useContext: ee, useEffect: ee, useImperativeHandle: ee, useInsertionEffect: ee, useLayoutEffect: ee, useMemo: ee, useReducer: ee, useRef: ee, useState: ee, useDebugValue: ee, useDeferredValue: ee, useTransition: ee, useMutableSource: ee, useSyncExternalStore: ee, useId: ee, unstable_isNewReconciler: !1 }, Kf = { readContext: _e, useCallback: function(e, n) {
  return Ie().memoizedState = [e, n === void 0 ? null : n], e;
}, useContext: _e, useEffect: wi, useImperativeHandle: function(e, n, t) {
  return t = t != null ? t.concat([e]) : null, xr(
    4194308,
    4,
    pa.bind(null, n, e),
    t
  );
}, useLayoutEffect: function(e, n) {
  return xr(4194308, 4, e, n);
}, useInsertionEffect: function(e, n) {
  return xr(4, 2, e, n);
}, useMemo: function(e, n) {
  var t = Ie();
  return n = n === void 0 ? null : n, e = e(), t.memoizedState = [e, n], e;
}, useReducer: function(e, n, t) {
  var r = Ie();
  return n = t !== void 0 ? t(n) : n, r.memoizedState = r.baseState = n, e = { pending: null, interleaved: null, lanes: 0, dispatch: null, lastRenderedReducer: e, lastRenderedState: n }, r.queue = e, e = e.dispatch = Qf.bind(null, $, e), [r.memoizedState, e];
}, useRef: function(e) {
  var n = Ie();
  return e = { current: e }, n.memoizedState = e;
}, useState: gi, useDebugValue: gu, useDeferredValue: function(e) {
  return Ie().memoizedState = e;
}, useTransition: function() {
  var e = gi(!1), n = e[0];
  return e = Hf.bind(null, e[1]), Ie().memoizedState = e, [n, e];
}, useMutableSource: function() {
}, useSyncExternalStore: function(e, n, t) {
  var r = $, l = Ie();
  if (U) {
    if (t === void 0) throw Error(g(407));
    t = t();
  } else {
    if (t = n(), Z === null) throw Error(g(349));
    Nn & 30 || oa(r, n, t);
  }
  l.memoizedState = t;
  var o = { value: t, getSnapshot: n };
  return l.queue = o, wi(ia.bind(
    null,
    r,
    o,
    e
  ), [e]), r.flags |= 2048, Wt(9, ua.bind(null, r, o, t, n), void 0, null), t;
}, useId: function() {
  var e = Ie(), n = Z.identifierPrefix;
  if (U) {
    var t = Be, r = Ve;
    t = (r & ~(1 << 32 - Re(r) - 1)).toString(32) + t, n = ":" + n + "R" + t, t = Ht++, 0 < t && (n += "H" + t.toString(32)), n += ":";
  } else t = Bf++, n = ":" + n + "r" + t.toString(32) + ":";
  return e.memoizedState = n;
}, unstable_isNewReconciler: !1 }, Yf = {
  readContext: _e,
  useCallback: ha,
  useContext: _e,
  useEffect: yu,
  useImperativeHandle: ma,
  useInsertionEffect: fa,
  useLayoutEffect: da,
  useMemo: va,
  useReducer: jl,
  useRef: ca,
  useState: function() {
    return jl(Qt);
  },
  useDebugValue: gu,
  useDeferredValue: function(e) {
    var n = xe();
    return ya(n, K.memoizedState, e);
  },
  useTransition: function() {
    var e = jl(Qt)[0], n = xe().memoizedState;
    return [e, n];
  },
  useMutableSource: ra,
  useSyncExternalStore: la,
  useId: ga,
  unstable_isNewReconciler: !1
}, Xf = { readContext: _e, useCallback: ha, useContext: _e, useEffect: yu, useImperativeHandle: ma, useInsertionEffect: fa, useLayoutEffect: da, useMemo: va, useReducer: $l, useRef: ca, useState: function() {
  return $l(Qt);
}, useDebugValue: gu, useDeferredValue: function(e) {
  var n = xe();
  return K === null ? n.memoizedState = e : ya(n, K.memoizedState, e);
}, useTransition: function() {
  var e = $l(Qt)[0], n = xe().memoizedState;
  return [e, n];
}, useMutableSource: ra, useSyncExternalStore: la, useId: ga, unstable_isNewReconciler: !1 };
function ze(e, n) {
  if (e && e.defaultProps) {
    n = A({}, n), e = e.defaultProps;
    for (var t in e) n[t] === void 0 && (n[t] = e[t]);
    return n;
  }
  return n;
}
function ko(e, n, t, r) {
  n = e.memoizedState, t = t(r, n), t = t == null ? n : A({}, n, t), e.memoizedState = t, e.lanes === 0 && (e.updateQueue.baseState = t);
}
var il = { isMounted: function(e) {
  return (e = e._reactInternals) ? Rn(e) === e : !1;
}, enqueueSetState: function(e, n, t) {
  e = e._reactInternals;
  var r = ue(), l = an(e), o = He(r, l);
  o.payload = n, t != null && (o.callback = t), n = un(e, o, l), n !== null && (Me(n, e, l, r), Cr(n, e, l));
}, enqueueReplaceState: function(e, n, t) {
  e = e._reactInternals;
  var r = ue(), l = an(e), o = He(r, l);
  o.tag = 1, o.payload = n, t != null && (o.callback = t), n = un(e, o, l), n !== null && (Me(n, e, l, r), Cr(n, e, l));
}, enqueueForceUpdate: function(e, n) {
  e = e._reactInternals;
  var t = ue(), r = an(e), l = He(t, r);
  l.tag = 2, n != null && (l.callback = n), n = un(e, l, r), n !== null && (Me(n, e, r, t), Cr(n, e, r));
} };
function Si(e, n, t, r, l, o, u) {
  return e = e.stateNode, typeof e.shouldComponentUpdate == "function" ? e.shouldComponentUpdate(r, o, u) : n.prototype && n.prototype.isPureReactComponent ? !Ut(t, r) || !Ut(l, o) : !0;
}
function Ea(e, n, t) {
  var r = !1, l = dn, o = n.contextType;
  return typeof o == "object" && o !== null ? o = _e(o) : (l = de(n) ? xn : le.current, r = n.contextTypes, o = (r = r != null) ? qn(e, l) : dn), n = new n(t, o), e.memoizedState = n.state !== null && n.state !== void 0 ? n.state : null, n.updater = il, e.stateNode = n, n._reactInternals = e, r && (e = e.stateNode, e.__reactInternalMemoizedUnmaskedChildContext = l, e.__reactInternalMemoizedMaskedChildContext = o), n;
}
function ki(e, n, t, r) {
  e = n.state, typeof n.componentWillReceiveProps == "function" && n.componentWillReceiveProps(t, r), typeof n.UNSAFE_componentWillReceiveProps == "function" && n.UNSAFE_componentWillReceiveProps(t, r), n.state !== e && il.enqueueReplaceState(n, n.state, null);
}
function Eo(e, n, t, r) {
  var l = e.stateNode;
  l.props = t, l.state = e.memoizedState, l.refs = {}, cu(e);
  var o = n.contextType;
  typeof o == "object" && o !== null ? l.context = _e(o) : (o = de(n) ? xn : le.current, l.context = qn(e, o)), l.state = e.memoizedState, o = n.getDerivedStateFromProps, typeof o == "function" && (ko(e, n, o, t), l.state = e.memoizedState), typeof n.getDerivedStateFromProps == "function" || typeof l.getSnapshotBeforeUpdate == "function" || typeof l.UNSAFE_componentWillMount != "function" && typeof l.componentWillMount != "function" || (n = l.state, typeof l.componentWillMount == "function" && l.componentWillMount(), typeof l.UNSAFE_componentWillMount == "function" && l.UNSAFE_componentWillMount(), n !== l.state && il.enqueueReplaceState(l, l.state, null), Wr(e, t, l, r), l.state = e.memoizedState), typeof l.componentDidMount == "function" && (e.flags |= 4194308);
}
function tt(e, n) {
  try {
    var t = "", r = n;
    do
      t += kc(r), r = r.return;
    while (r);
    var l = t;
  } catch (o) {
    l = `
Error generating stack: ` + o.message + `
` + o.stack;
  }
  return { value: e, source: n, stack: l, digest: null };
}
function Al(e, n, t) {
  return { value: e, source: null, stack: t ?? null, digest: n ?? null };
}
function Co(e, n) {
  try {
    console.error(n.value);
  } catch (t) {
    setTimeout(function() {
      throw t;
    });
  }
}
var Gf = typeof WeakMap == "function" ? WeakMap : Map;
function Ca(e, n, t) {
  t = He(-1, t), t.tag = 3, t.payload = { element: null };
  var r = n.value;
  return t.callback = function() {
    Zr || (Zr = !0, Oo = r), Co(e, n);
  }, t;
}
function _a(e, n, t) {
  t = He(-1, t), t.tag = 3;
  var r = e.type.getDerivedStateFromError;
  if (typeof r == "function") {
    var l = n.value;
    t.payload = function() {
      return r(l);
    }, t.callback = function() {
      Co(e, n);
    };
  }
  var o = e.stateNode;
  return o !== null && typeof o.componentDidCatch == "function" && (t.callback = function() {
    Co(e, n), typeof r != "function" && (sn === null ? sn = /* @__PURE__ */ new Set([this]) : sn.add(this));
    var u = n.stack;
    this.componentDidCatch(n.value, { componentStack: u !== null ? u : "" });
  }), t;
}
function Ei(e, n, t) {
  var r = e.pingCache;
  if (r === null) {
    r = e.pingCache = new Gf();
    var l = /* @__PURE__ */ new Set();
    r.set(n, l);
  } else l = r.get(n), l === void 0 && (l = /* @__PURE__ */ new Set(), r.set(n, l));
  l.has(t) || (l.add(t), e = ad.bind(null, e, n, t), n.then(e, e));
}
function Ci(e) {
  do {
    var n;
    if ((n = e.tag === 13) && (n = e.memoizedState, n = n !== null ? n.dehydrated !== null : !0), n) return e;
    e = e.return;
  } while (e !== null);
  return null;
}
function _i(e, n, t, r, l) {
  return e.mode & 1 ? (e.flags |= 65536, e.lanes = l, e) : (e === n ? e.flags |= 65536 : (e.flags |= 128, t.flags |= 131072, t.flags &= -52805, t.tag === 1 && (t.alternate === null ? t.tag = 17 : (n = He(-1, 1), n.tag = 2, un(t, n, 1))), t.lanes |= 1), e);
}
var Zf = Xe.ReactCurrentOwner, ce = !1;
function oe(e, n, t, r) {
  n.child = e === null ? bs(n, null, t, r) : et(n, e.child, t, r);
}
function xi(e, n, t, r, l) {
  t = t.render;
  var o = n.ref;
  return Gn(n, l), r = hu(e, n, t, r, o, l), t = vu(), e !== null && !ce ? (n.updateQueue = e.updateQueue, n.flags &= -2053, e.lanes &= ~l, Ye(e, n, l)) : (U && t && ru(n), n.flags |= 1, oe(e, n, r, l), n.child);
}
function Pi(e, n, t, r, l) {
  if (e === null) {
    var o = t.type;
    return typeof o == "function" && !Pu(o) && o.defaultProps === void 0 && t.compare === null && t.defaultProps === void 0 ? (n.tag = 15, n.type = o, xa(e, n, o, r, l)) : (e = Lr(t.type, null, r, n, n.mode, l), e.ref = n.ref, e.return = n, n.child = e);
  }
  if (o = e.child, !(e.lanes & l)) {
    var u = o.memoizedProps;
    if (t = t.compare, t = t !== null ? t : Ut, t(u, r) && e.ref === n.ref) return Ye(e, n, l);
  }
  return n.flags |= 1, e = cn(o, r), e.ref = n.ref, e.return = n, n.child = e;
}
function xa(e, n, t, r, l) {
  if (e !== null) {
    var o = e.memoizedProps;
    if (Ut(o, r) && e.ref === n.ref) if (ce = !1, n.pendingProps = r = o, (e.lanes & l) !== 0) e.flags & 131072 && (ce = !0);
    else return n.lanes = e.lanes, Ye(e, n, l);
  }
  return _o(e, n, t, r, l);
}
function Pa(e, n, t) {
  var r = n.pendingProps, l = r.children, o = e !== null ? e.memoizedState : null;
  if (r.mode === "hidden") if (!(n.mode & 1)) n.memoizedState = { baseLanes: 0, cachePool: null, transitions: null }, D(Qn, me), me |= t;
  else {
    if (!(t & 1073741824)) return e = o !== null ? o.baseLanes | t : t, n.lanes = n.childLanes = 1073741824, n.memoizedState = { baseLanes: e, cachePool: null, transitions: null }, n.updateQueue = null, D(Qn, me), me |= e, null;
    n.memoizedState = { baseLanes: 0, cachePool: null, transitions: null }, r = o !== null ? o.baseLanes : t, D(Qn, me), me |= r;
  }
  else o !== null ? (r = o.baseLanes | t, n.memoizedState = null) : r = t, D(Qn, me), me |= r;
  return oe(e, n, l, t), n.child;
}
function Na(e, n) {
  var t = n.ref;
  (e === null && t !== null || e !== null && e.ref !== t) && (n.flags |= 512, n.flags |= 2097152);
}
function _o(e, n, t, r, l) {
  var o = de(t) ? xn : le.current;
  return o = qn(n, o), Gn(n, l), t = hu(e, n, t, r, o, l), r = vu(), e !== null && !ce ? (n.updateQueue = e.updateQueue, n.flags &= -2053, e.lanes &= ~l, Ye(e, n, l)) : (U && r && ru(n), n.flags |= 1, oe(e, n, t, l), n.child);
}
function Ni(e, n, t, r, l) {
  if (de(t)) {
    var o = !0;
    Ar(n);
  } else o = !1;
  if (Gn(n, l), n.stateNode === null) Pr(e, n), Ea(n, t, r), Eo(n, t, r, l), r = !0;
  else if (e === null) {
    var u = n.stateNode, i = n.memoizedProps;
    u.props = i;
    var s = u.context, f = t.contextType;
    typeof f == "object" && f !== null ? f = _e(f) : (f = de(t) ? xn : le.current, f = qn(n, f));
    var h = t.getDerivedStateFromProps, m = typeof h == "function" || typeof u.getSnapshotBeforeUpdate == "function";
    m || typeof u.UNSAFE_componentWillReceiveProps != "function" && typeof u.componentWillReceiveProps != "function" || (i !== r || s !== f) && ki(n, u, r, f), Je = !1;
    var p = n.memoizedState;
    u.state = p, Wr(n, r, u, l), s = n.memoizedState, i !== r || p !== s || fe.current || Je ? (typeof h == "function" && (ko(n, t, h, r), s = n.memoizedState), (i = Je || Si(n, t, i, r, p, s, f)) ? (m || typeof u.UNSAFE_componentWillMount != "function" && typeof u.componentWillMount != "function" || (typeof u.componentWillMount == "function" && u.componentWillMount(), typeof u.UNSAFE_componentWillMount == "function" && u.UNSAFE_componentWillMount()), typeof u.componentDidMount == "function" && (n.flags |= 4194308)) : (typeof u.componentDidMount == "function" && (n.flags |= 4194308), n.memoizedProps = r, n.memoizedState = s), u.props = r, u.state = s, u.context = f, r = i) : (typeof u.componentDidMount == "function" && (n.flags |= 4194308), r = !1);
  } else {
    u = n.stateNode, na(e, n), i = n.memoizedProps, f = n.type === n.elementType ? i : ze(n.type, i), u.props = f, m = n.pendingProps, p = u.context, s = t.contextType, typeof s == "object" && s !== null ? s = _e(s) : (s = de(t) ? xn : le.current, s = qn(n, s));
    var S = t.getDerivedStateFromProps;
    (h = typeof S == "function" || typeof u.getSnapshotBeforeUpdate == "function") || typeof u.UNSAFE_componentWillReceiveProps != "function" && typeof u.componentWillReceiveProps != "function" || (i !== m || p !== s) && ki(n, u, r, s), Je = !1, p = n.memoizedState, u.state = p, Wr(n, r, u, l);
    var v = n.memoizedState;
    i !== m || p !== v || fe.current || Je ? (typeof S == "function" && (ko(n, t, S, r), v = n.memoizedState), (f = Je || Si(n, t, f, r, p, v, s) || !1) ? (h || typeof u.UNSAFE_componentWillUpdate != "function" && typeof u.componentWillUpdate != "function" || (typeof u.componentWillUpdate == "function" && u.componentWillUpdate(r, v, s), typeof u.UNSAFE_componentWillUpdate == "function" && u.UNSAFE_componentWillUpdate(r, v, s)), typeof u.componentDidUpdate == "function" && (n.flags |= 4), typeof u.getSnapshotBeforeUpdate == "function" && (n.flags |= 1024)) : (typeof u.componentDidUpdate != "function" || i === e.memoizedProps && p === e.memoizedState || (n.flags |= 4), typeof u.getSnapshotBeforeUpdate != "function" || i === e.memoizedProps && p === e.memoizedState || (n.flags |= 1024), n.memoizedProps = r, n.memoizedState = v), u.props = r, u.state = v, u.context = s, r = f) : (typeof u.componentDidUpdate != "function" || i === e.memoizedProps && p === e.memoizedState || (n.flags |= 4), typeof u.getSnapshotBeforeUpdate != "function" || i === e.memoizedProps && p === e.memoizedState || (n.flags |= 1024), r = !1);
  }
  return xo(e, n, t, r, o, l);
}
function xo(e, n, t, r, l, o) {
  Na(e, n);
  var u = (n.flags & 128) !== 0;
  if (!r && !u) return l && di(n, t, !1), Ye(e, n, o);
  r = n.stateNode, Zf.current = n;
  var i = u && typeof t.getDerivedStateFromError != "function" ? null : r.render();
  return n.flags |= 1, e !== null && u ? (n.child = et(n, e.child, null, o), n.child = et(n, null, i, o)) : oe(e, n, i, o), n.memoizedState = r.state, l && di(n, t, !0), n.child;
}
function za(e) {
  var n = e.stateNode;
  n.pendingContext ? fi(e, n.pendingContext, n.pendingContext !== n.context) : n.context && fi(e, n.context, !1), fu(e, n.containerInfo);
}
function zi(e, n, t, r, l) {
  return bn(), ou(l), n.flags |= 256, oe(e, n, t, r), n.child;
}
var Po = { dehydrated: null, treeContext: null, retryLane: 0 };
function No(e) {
  return { baseLanes: e, cachePool: null, transitions: null };
}
function La(e, n, t) {
  var r = n.pendingProps, l = j.current, o = !1, u = (n.flags & 128) !== 0, i;
  if ((i = u) || (i = e !== null && e.memoizedState === null ? !1 : (l & 2) !== 0), i ? (o = !0, n.flags &= -129) : (e === null || e.memoizedState !== null) && (l |= 1), D(j, l & 1), e === null)
    return wo(n), e = n.memoizedState, e !== null && (e = e.dehydrated, e !== null) ? (n.mode & 1 ? e.data === "$!" ? n.lanes = 8 : n.lanes = 1073741824 : n.lanes = 1, null) : (u = r.children, e = r.fallback, o ? (r = n.mode, o = n.child, u = { mode: "hidden", children: u }, !(r & 1) && o !== null ? (o.childLanes = 0, o.pendingProps = u) : o = cl(u, r, 0, null), e = _n(e, r, t, null), o.return = n, e.return = n, o.sibling = e, n.child = o, n.child.memoizedState = No(t), n.memoizedState = Po, e) : wu(n, u));
  if (l = e.memoizedState, l !== null && (i = l.dehydrated, i !== null)) return Jf(e, n, u, r, i, l, t);
  if (o) {
    o = r.fallback, u = n.mode, l = e.child, i = l.sibling;
    var s = { mode: "hidden", children: r.children };
    return !(u & 1) && n.child !== l ? (r = n.child, r.childLanes = 0, r.pendingProps = s, n.deletions = null) : (r = cn(l, s), r.subtreeFlags = l.subtreeFlags & 14680064), i !== null ? o = cn(i, o) : (o = _n(o, u, t, null), o.flags |= 2), o.return = n, r.return = n, r.sibling = o, n.child = r, r = o, o = n.child, u = e.child.memoizedState, u = u === null ? No(t) : { baseLanes: u.baseLanes | t, cachePool: null, transitions: u.transitions }, o.memoizedState = u, o.childLanes = e.childLanes & ~t, n.memoizedState = Po, r;
  }
  return o = e.child, e = o.sibling, r = cn(o, { mode: "visible", children: r.children }), !(n.mode & 1) && (r.lanes = t), r.return = n, r.sibling = null, e !== null && (t = n.deletions, t === null ? (n.deletions = [e], n.flags |= 16) : t.push(e)), n.child = r, n.memoizedState = null, r;
}
function wu(e, n) {
  return n = cl({ mode: "visible", children: n }, e.mode, 0, null), n.return = e, e.child = n;
}
function pr(e, n, t, r) {
  return r !== null && ou(r), et(n, e.child, null, t), e = wu(n, n.pendingProps.children), e.flags |= 2, n.memoizedState = null, e;
}
function Jf(e, n, t, r, l, o, u) {
  if (t)
    return n.flags & 256 ? (n.flags &= -257, r = Al(Error(g(422))), pr(e, n, u, r)) : n.memoizedState !== null ? (n.child = e.child, n.flags |= 128, null) : (o = r.fallback, l = n.mode, r = cl({ mode: "visible", children: r.children }, l, 0, null), o = _n(o, l, u, null), o.flags |= 2, r.return = n, o.return = n, r.sibling = o, n.child = r, n.mode & 1 && et(n, e.child, null, u), n.child.memoizedState = No(u), n.memoizedState = Po, o);
  if (!(n.mode & 1)) return pr(e, n, u, null);
  if (l.data === "$!") {
    if (r = l.nextSibling && l.nextSibling.dataset, r) var i = r.dgst;
    return r = i, o = Error(g(419)), r = Al(o, r, void 0), pr(e, n, u, r);
  }
  if (i = (u & e.childLanes) !== 0, ce || i) {
    if (r = Z, r !== null) {
      switch (u & -u) {
        case 4:
          l = 2;
          break;
        case 16:
          l = 8;
          break;
        case 64:
        case 128:
        case 256:
        case 512:
        case 1024:
        case 2048:
        case 4096:
        case 8192:
        case 16384:
        case 32768:
        case 65536:
        case 131072:
        case 262144:
        case 524288:
        case 1048576:
        case 2097152:
        case 4194304:
        case 8388608:
        case 16777216:
        case 33554432:
        case 67108864:
          l = 32;
          break;
        case 536870912:
          l = 268435456;
          break;
        default:
          l = 0;
      }
      l = l & (r.suspendedLanes | u) ? 0 : l, l !== 0 && l !== o.retryLane && (o.retryLane = l, Ke(e, l), Me(r, e, l, -1));
    }
    return xu(), r = Al(Error(g(421))), pr(e, n, u, r);
  }
  return l.data === "$?" ? (n.flags |= 128, n.child = e.child, n = cd.bind(null, e), l._reactRetry = n, null) : (e = o.treeContext, he = on(l.nextSibling), ve = n, U = !0, Te = null, e !== null && (Se[ke++] = Ve, Se[ke++] = Be, Se[ke++] = Pn, Ve = e.id, Be = e.overflow, Pn = n), n = wu(n, r.children), n.flags |= 4096, n);
}
function Li(e, n, t) {
  e.lanes |= n;
  var r = e.alternate;
  r !== null && (r.lanes |= n), So(e.return, n, t);
}
function Vl(e, n, t, r, l) {
  var o = e.memoizedState;
  o === null ? e.memoizedState = { isBackwards: n, rendering: null, renderingStartTime: 0, last: r, tail: t, tailMode: l } : (o.isBackwards = n, o.rendering = null, o.renderingStartTime = 0, o.last = r, o.tail = t, o.tailMode = l);
}
function Ta(e, n, t) {
  var r = n.pendingProps, l = r.revealOrder, o = r.tail;
  if (oe(e, n, r.children, t), r = j.current, r & 2) r = r & 1 | 2, n.flags |= 128;
  else {
    if (e !== null && e.flags & 128) e: for (e = n.child; e !== null; ) {
      if (e.tag === 13) e.memoizedState !== null && Li(e, t, n);
      else if (e.tag === 19) Li(e, t, n);
      else if (e.child !== null) {
        e.child.return = e, e = e.child;
        continue;
      }
      if (e === n) break e;
      for (; e.sibling === null; ) {
        if (e.return === null || e.return === n) break e;
        e = e.return;
      }
      e.sibling.return = e.return, e = e.sibling;
    }
    r &= 1;
  }
  if (D(j, r), !(n.mode & 1)) n.memoizedState = null;
  else switch (l) {
    case "forwards":
      for (t = n.child, l = null; t !== null; ) e = t.alternate, e !== null && Kr(e) === null && (l = t), t = t.sibling;
      t = l, t === null ? (l = n.child, n.child = null) : (l = t.sibling, t.sibling = null), Vl(n, !1, l, t, o);
      break;
    case "backwards":
      for (t = null, l = n.child, n.child = null; l !== null; ) {
        if (e = l.alternate, e !== null && Kr(e) === null) {
          n.child = l;
          break;
        }
        e = l.sibling, l.sibling = t, t = l, l = e;
      }
      Vl(n, !0, t, null, o);
      break;
    case "together":
      Vl(n, !1, null, null, void 0);
      break;
    default:
      n.memoizedState = null;
  }
  return n.child;
}
function Pr(e, n) {
  !(n.mode & 1) && e !== null && (e.alternate = null, n.alternate = null, n.flags |= 2);
}
function Ye(e, n, t) {
  if (e !== null && (n.dependencies = e.dependencies), zn |= n.lanes, !(t & n.childLanes)) return null;
  if (e !== null && n.child !== e.child) throw Error(g(153));
  if (n.child !== null) {
    for (e = n.child, t = cn(e, e.pendingProps), n.child = t, t.return = n; e.sibling !== null; ) e = e.sibling, t = t.sibling = cn(e, e.pendingProps), t.return = n;
    t.sibling = null;
  }
  return n.child;
}
function qf(e, n, t) {
  switch (n.tag) {
    case 3:
      za(n), bn();
      break;
    case 5:
      ta(n);
      break;
    case 1:
      de(n.type) && Ar(n);
      break;
    case 4:
      fu(n, n.stateNode.containerInfo);
      break;
    case 10:
      var r = n.type._context, l = n.memoizedProps.value;
      D(Hr, r._currentValue), r._currentValue = l;
      break;
    case 13:
      if (r = n.memoizedState, r !== null)
        return r.dehydrated !== null ? (D(j, j.current & 1), n.flags |= 128, null) : t & n.child.childLanes ? La(e, n, t) : (D(j, j.current & 1), e = Ye(e, n, t), e !== null ? e.sibling : null);
      D(j, j.current & 1);
      break;
    case 19:
      if (r = (t & n.childLanes) !== 0, e.flags & 128) {
        if (r) return Ta(e, n, t);
        n.flags |= 128;
      }
      if (l = n.memoizedState, l !== null && (l.rendering = null, l.tail = null, l.lastEffect = null), D(j, j.current), r) break;
      return null;
    case 22:
    case 23:
      return n.lanes = 0, Pa(e, n, t);
  }
  return Ye(e, n, t);
}
var Ra, zo, Ma, Oa;
Ra = function(e, n) {
  for (var t = n.child; t !== null; ) {
    if (t.tag === 5 || t.tag === 6) e.appendChild(t.stateNode);
    else if (t.tag !== 4 && t.child !== null) {
      t.child.return = t, t = t.child;
      continue;
    }
    if (t === n) break;
    for (; t.sibling === null; ) {
      if (t.return === null || t.return === n) return;
      t = t.return;
    }
    t.sibling.return = t.return, t = t.sibling;
  }
};
zo = function() {
};
Ma = function(e, n, t, r) {
  var l = e.memoizedProps;
  if (l !== r) {
    e = n.stateNode, En(je.current);
    var o = null;
    switch (t) {
      case "input":
        l = Gl(e, l), r = Gl(e, r), o = [];
        break;
      case "select":
        l = A({}, l, { value: void 0 }), r = A({}, r, { value: void 0 }), o = [];
        break;
      case "textarea":
        l = ql(e, l), r = ql(e, r), o = [];
        break;
      default:
        typeof l.onClick != "function" && typeof r.onClick == "function" && (e.onclick = jr);
    }
    eo(t, r);
    var u;
    t = null;
    for (f in l) if (!r.hasOwnProperty(f) && l.hasOwnProperty(f) && l[f] != null) if (f === "style") {
      var i = l[f];
      for (u in i) i.hasOwnProperty(u) && (t || (t = {}), t[u] = "");
    } else f !== "dangerouslySetInnerHTML" && f !== "children" && f !== "suppressContentEditableWarning" && f !== "suppressHydrationWarning" && f !== "autoFocus" && (Tt.hasOwnProperty(f) ? o || (o = []) : (o = o || []).push(f, null));
    for (f in r) {
      var s = r[f];
      if (i = l != null ? l[f] : void 0, r.hasOwnProperty(f) && s !== i && (s != null || i != null)) if (f === "style") if (i) {
        for (u in i) !i.hasOwnProperty(u) || s && s.hasOwnProperty(u) || (t || (t = {}), t[u] = "");
        for (u in s) s.hasOwnProperty(u) && i[u] !== s[u] && (t || (t = {}), t[u] = s[u]);
      } else t || (o || (o = []), o.push(
        f,
        t
      )), t = s;
      else f === "dangerouslySetInnerHTML" ? (s = s ? s.__html : void 0, i = i ? i.__html : void 0, s != null && i !== s && (o = o || []).push(f, s)) : f === "children" ? typeof s != "string" && typeof s != "number" || (o = o || []).push(f, "" + s) : f !== "suppressContentEditableWarning" && f !== "suppressHydrationWarning" && (Tt.hasOwnProperty(f) ? (s != null && f === "onScroll" && I("scroll", e), o || i === s || (o = [])) : (o = o || []).push(f, s));
    }
    t && (o = o || []).push("style", t);
    var f = o;
    (n.updateQueue = f) && (n.flags |= 4);
  }
};
Oa = function(e, n, t, r) {
  t !== r && (n.flags |= 4);
};
function ht(e, n) {
  if (!U) switch (e.tailMode) {
    case "hidden":
      n = e.tail;
      for (var t = null; n !== null; ) n.alternate !== null && (t = n), n = n.sibling;
      t === null ? e.tail = null : t.sibling = null;
      break;
    case "collapsed":
      t = e.tail;
      for (var r = null; t !== null; ) t.alternate !== null && (r = t), t = t.sibling;
      r === null ? n || e.tail === null ? e.tail = null : e.tail.sibling = null : r.sibling = null;
  }
}
function ne(e) {
  var n = e.alternate !== null && e.alternate.child === e.child, t = 0, r = 0;
  if (n) for (var l = e.child; l !== null; ) t |= l.lanes | l.childLanes, r |= l.subtreeFlags & 14680064, r |= l.flags & 14680064, l.return = e, l = l.sibling;
  else for (l = e.child; l !== null; ) t |= l.lanes | l.childLanes, r |= l.subtreeFlags, r |= l.flags, l.return = e, l = l.sibling;
  return e.subtreeFlags |= r, e.childLanes = t, n;
}
function bf(e, n, t) {
  var r = n.pendingProps;
  switch (lu(n), n.tag) {
    case 2:
    case 16:
    case 15:
    case 0:
    case 11:
    case 7:
    case 8:
    case 12:
    case 9:
    case 14:
      return ne(n), null;
    case 1:
      return de(n.type) && $r(), ne(n), null;
    case 3:
      return r = n.stateNode, nt(), F(fe), F(le), pu(), r.pendingContext && (r.context = r.pendingContext, r.pendingContext = null), (e === null || e.child === null) && (fr(n) ? n.flags |= 4 : e === null || e.memoizedState.isDehydrated && !(n.flags & 256) || (n.flags |= 1024, Te !== null && (Fo(Te), Te = null))), zo(e, n), ne(n), null;
    case 5:
      du(n);
      var l = En(Bt.current);
      if (t = n.type, e !== null && n.stateNode != null) Ma(e, n, t, r, l), e.ref !== n.ref && (n.flags |= 512, n.flags |= 2097152);
      else {
        if (!r) {
          if (n.stateNode === null) throw Error(g(166));
          return ne(n), null;
        }
        if (e = En(je.current), fr(n)) {
          r = n.stateNode, t = n.type;
          var o = n.memoizedProps;
          switch (r[Fe] = n, r[At] = o, e = (n.mode & 1) !== 0, t) {
            case "dialog":
              I("cancel", r), I("close", r);
              break;
            case "iframe":
            case "object":
            case "embed":
              I("load", r);
              break;
            case "video":
            case "audio":
              for (l = 0; l < St.length; l++) I(St[l], r);
              break;
            case "source":
              I("error", r);
              break;
            case "img":
            case "image":
            case "link":
              I(
                "error",
                r
              ), I("load", r);
              break;
            case "details":
              I("toggle", r);
              break;
            case "input":
              ju(r, o), I("invalid", r);
              break;
            case "select":
              r._wrapperState = { wasMultiple: !!o.multiple }, I("invalid", r);
              break;
            case "textarea":
              Au(r, o), I("invalid", r);
          }
          eo(t, o), l = null;
          for (var u in o) if (o.hasOwnProperty(u)) {
            var i = o[u];
            u === "children" ? typeof i == "string" ? r.textContent !== i && (o.suppressHydrationWarning !== !0 && cr(r.textContent, i, e), l = ["children", i]) : typeof i == "number" && r.textContent !== "" + i && (o.suppressHydrationWarning !== !0 && cr(
              r.textContent,
              i,
              e
            ), l = ["children", "" + i]) : Tt.hasOwnProperty(u) && i != null && u === "onScroll" && I("scroll", r);
          }
          switch (t) {
            case "input":
              tr(r), $u(r, o, !0);
              break;
            case "textarea":
              tr(r), Vu(r);
              break;
            case "select":
            case "option":
              break;
            default:
              typeof o.onClick == "function" && (r.onclick = jr);
          }
          r = l, n.updateQueue = r, r !== null && (n.flags |= 4);
        } else {
          u = l.nodeType === 9 ? l : l.ownerDocument, e === "http://www.w3.org/1999/xhtml" && (e = is(t)), e === "http://www.w3.org/1999/xhtml" ? t === "script" ? (e = u.createElement("div"), e.innerHTML = "<script><\/script>", e = e.removeChild(e.firstChild)) : typeof r.is == "string" ? e = u.createElement(t, { is: r.is }) : (e = u.createElement(t), t === "select" && (u = e, r.multiple ? u.multiple = !0 : r.size && (u.size = r.size))) : e = u.createElementNS(e, t), e[Fe] = n, e[At] = r, Ra(e, n, !1, !1), n.stateNode = e;
          e: {
            switch (u = no(t, r), t) {
              case "dialog":
                I("cancel", e), I("close", e), l = r;
                break;
              case "iframe":
              case "object":
              case "embed":
                I("load", e), l = r;
                break;
              case "video":
              case "audio":
                for (l = 0; l < St.length; l++) I(St[l], e);
                l = r;
                break;
              case "source":
                I("error", e), l = r;
                break;
              case "img":
              case "image":
              case "link":
                I(
                  "error",
                  e
                ), I("load", e), l = r;
                break;
              case "details":
                I("toggle", e), l = r;
                break;
              case "input":
                ju(e, r), l = Gl(e, r), I("invalid", e);
                break;
              case "option":
                l = r;
                break;
              case "select":
                e._wrapperState = { wasMultiple: !!r.multiple }, l = A({}, r, { value: void 0 }), I("invalid", e);
                break;
              case "textarea":
                Au(e, r), l = ql(e, r), I("invalid", e);
                break;
              default:
                l = r;
            }
            eo(t, l), i = l;
            for (o in i) if (i.hasOwnProperty(o)) {
              var s = i[o];
              o === "style" ? cs(e, s) : o === "dangerouslySetInnerHTML" ? (s = s ? s.__html : void 0, s != null && ss(e, s)) : o === "children" ? typeof s == "string" ? (t !== "textarea" || s !== "") && Rt(e, s) : typeof s == "number" && Rt(e, "" + s) : o !== "suppressContentEditableWarning" && o !== "suppressHydrationWarning" && o !== "autoFocus" && (Tt.hasOwnProperty(o) ? s != null && o === "onScroll" && I("scroll", e) : s != null && Ho(e, o, s, u));
            }
            switch (t) {
              case "input":
                tr(e), $u(e, r, !1);
                break;
              case "textarea":
                tr(e), Vu(e);
                break;
              case "option":
                r.value != null && e.setAttribute("value", "" + fn(r.value));
                break;
              case "select":
                e.multiple = !!r.multiple, o = r.value, o != null ? Wn(e, !!r.multiple, o, !1) : r.defaultValue != null && Wn(
                  e,
                  !!r.multiple,
                  r.defaultValue,
                  !0
                );
                break;
              default:
                typeof l.onClick == "function" && (e.onclick = jr);
            }
            switch (t) {
              case "button":
              case "input":
              case "select":
              case "textarea":
                r = !!r.autoFocus;
                break e;
              case "img":
                r = !0;
                break e;
              default:
                r = !1;
            }
          }
          r && (n.flags |= 4);
        }
        n.ref !== null && (n.flags |= 512, n.flags |= 2097152);
      }
      return ne(n), null;
    case 6:
      if (e && n.stateNode != null) Oa(e, n, e.memoizedProps, r);
      else {
        if (typeof r != "string" && n.stateNode === null) throw Error(g(166));
        if (t = En(Bt.current), En(je.current), fr(n)) {
          if (r = n.stateNode, t = n.memoizedProps, r[Fe] = n, (o = r.nodeValue !== t) && (e = ve, e !== null)) switch (e.tag) {
            case 3:
              cr(r.nodeValue, t, (e.mode & 1) !== 0);
              break;
            case 5:
              e.memoizedProps.suppressHydrationWarning !== !0 && cr(r.nodeValue, t, (e.mode & 1) !== 0);
          }
          o && (n.flags |= 4);
        } else r = (t.nodeType === 9 ? t : t.ownerDocument).createTextNode(r), r[Fe] = n, n.stateNode = r;
      }
      return ne(n), null;
    case 13:
      if (F(j), r = n.memoizedState, e === null || e.memoizedState !== null && e.memoizedState.dehydrated !== null) {
        if (U && he !== null && n.mode & 1 && !(n.flags & 128)) Js(), bn(), n.flags |= 98560, o = !1;
        else if (o = fr(n), r !== null && r.dehydrated !== null) {
          if (e === null) {
            if (!o) throw Error(g(318));
            if (o = n.memoizedState, o = o !== null ? o.dehydrated : null, !o) throw Error(g(317));
            o[Fe] = n;
          } else bn(), !(n.flags & 128) && (n.memoizedState = null), n.flags |= 4;
          ne(n), o = !1;
        } else Te !== null && (Fo(Te), Te = null), o = !0;
        if (!o) return n.flags & 65536 ? n : null;
      }
      return n.flags & 128 ? (n.lanes = t, n) : (r = r !== null, r !== (e !== null && e.memoizedState !== null) && r && (n.child.flags |= 8192, n.mode & 1 && (e === null || j.current & 1 ? Y === 0 && (Y = 3) : xu())), n.updateQueue !== null && (n.flags |= 4), ne(n), null);
    case 4:
      return nt(), zo(e, n), e === null && jt(n.stateNode.containerInfo), ne(n), null;
    case 10:
      return su(n.type._context), ne(n), null;
    case 17:
      return de(n.type) && $r(), ne(n), null;
    case 19:
      if (F(j), o = n.memoizedState, o === null) return ne(n), null;
      if (r = (n.flags & 128) !== 0, u = o.rendering, u === null) if (r) ht(o, !1);
      else {
        if (Y !== 0 || e !== null && e.flags & 128) for (e = n.child; e !== null; ) {
          if (u = Kr(e), u !== null) {
            for (n.flags |= 128, ht(o, !1), r = u.updateQueue, r !== null && (n.updateQueue = r, n.flags |= 4), n.subtreeFlags = 0, r = t, t = n.child; t !== null; ) o = t, e = r, o.flags &= 14680066, u = o.alternate, u === null ? (o.childLanes = 0, o.lanes = e, o.child = null, o.subtreeFlags = 0, o.memoizedProps = null, o.memoizedState = null, o.updateQueue = null, o.dependencies = null, o.stateNode = null) : (o.childLanes = u.childLanes, o.lanes = u.lanes, o.child = u.child, o.subtreeFlags = 0, o.deletions = null, o.memoizedProps = u.memoizedProps, o.memoizedState = u.memoizedState, o.updateQueue = u.updateQueue, o.type = u.type, e = u.dependencies, o.dependencies = e === null ? null : { lanes: e.lanes, firstContext: e.firstContext }), t = t.sibling;
            return D(j, j.current & 1 | 2), n.child;
          }
          e = e.sibling;
        }
        o.tail !== null && Q() > rt && (n.flags |= 128, r = !0, ht(o, !1), n.lanes = 4194304);
      }
      else {
        if (!r) if (e = Kr(u), e !== null) {
          if (n.flags |= 128, r = !0, t = e.updateQueue, t !== null && (n.updateQueue = t, n.flags |= 4), ht(o, !0), o.tail === null && o.tailMode === "hidden" && !u.alternate && !U) return ne(n), null;
        } else 2 * Q() - o.renderingStartTime > rt && t !== 1073741824 && (n.flags |= 128, r = !0, ht(o, !1), n.lanes = 4194304);
        o.isBackwards ? (u.sibling = n.child, n.child = u) : (t = o.last, t !== null ? t.sibling = u : n.child = u, o.last = u);
      }
      return o.tail !== null ? (n = o.tail, o.rendering = n, o.tail = n.sibling, o.renderingStartTime = Q(), n.sibling = null, t = j.current, D(j, r ? t & 1 | 2 : t & 1), n) : (ne(n), null);
    case 22:
    case 23:
      return _u(), r = n.memoizedState !== null, e !== null && e.memoizedState !== null !== r && (n.flags |= 8192), r && n.mode & 1 ? me & 1073741824 && (ne(n), n.subtreeFlags & 6 && (n.flags |= 8192)) : ne(n), null;
    case 24:
      return null;
    case 25:
      return null;
  }
  throw Error(g(156, n.tag));
}
function ed(e, n) {
  switch (lu(n), n.tag) {
    case 1:
      return de(n.type) && $r(), e = n.flags, e & 65536 ? (n.flags = e & -65537 | 128, n) : null;
    case 3:
      return nt(), F(fe), F(le), pu(), e = n.flags, e & 65536 && !(e & 128) ? (n.flags = e & -65537 | 128, n) : null;
    case 5:
      return du(n), null;
    case 13:
      if (F(j), e = n.memoizedState, e !== null && e.dehydrated !== null) {
        if (n.alternate === null) throw Error(g(340));
        bn();
      }
      return e = n.flags, e & 65536 ? (n.flags = e & -65537 | 128, n) : null;
    case 19:
      return F(j), null;
    case 4:
      return nt(), null;
    case 10:
      return su(n.type._context), null;
    case 22:
    case 23:
      return _u(), null;
    case 24:
      return null;
    default:
      return null;
  }
}
var mr = !1, re = !1, nd = typeof WeakSet == "function" ? WeakSet : Set, k = null;
function Hn(e, n) {
  var t = e.ref;
  if (t !== null) if (typeof t == "function") try {
    t(null);
  } catch (r) {
    V(e, n, r);
  }
  else t.current = null;
}
function Lo(e, n, t) {
  try {
    t();
  } catch (r) {
    V(e, n, r);
  }
}
var Ti = !1;
function td(e, n) {
  if (fo = Ir, e = js(), tu(e)) {
    if ("selectionStart" in e) var t = { start: e.selectionStart, end: e.selectionEnd };
    else e: {
      t = (t = e.ownerDocument) && t.defaultView || window;
      var r = t.getSelection && t.getSelection();
      if (r && r.rangeCount !== 0) {
        t = r.anchorNode;
        var l = r.anchorOffset, o = r.focusNode;
        r = r.focusOffset;
        try {
          t.nodeType, o.nodeType;
        } catch {
          t = null;
          break e;
        }
        var u = 0, i = -1, s = -1, f = 0, h = 0, m = e, p = null;
        n: for (; ; ) {
          for (var S; m !== t || l !== 0 && m.nodeType !== 3 || (i = u + l), m !== o || r !== 0 && m.nodeType !== 3 || (s = u + r), m.nodeType === 3 && (u += m.nodeValue.length), (S = m.firstChild) !== null; )
            p = m, m = S;
          for (; ; ) {
            if (m === e) break n;
            if (p === t && ++f === l && (i = u), p === o && ++h === r && (s = u), (S = m.nextSibling) !== null) break;
            m = p, p = m.parentNode;
          }
          m = S;
        }
        t = i === -1 || s === -1 ? null : { start: i, end: s };
      } else t = null;
    }
    t = t || { start: 0, end: 0 };
  } else t = null;
  for (po = { focusedElem: e, selectionRange: t }, Ir = !1, k = n; k !== null; ) if (n = k, e = n.child, (n.subtreeFlags & 1028) !== 0 && e !== null) e.return = n, k = e;
  else for (; k !== null; ) {
    n = k;
    try {
      var v = n.alternate;
      if (n.flags & 1024) switch (n.tag) {
        case 0:
        case 11:
        case 15:
          break;
        case 1:
          if (v !== null) {
            var w = v.memoizedProps, N = v.memoizedState, c = n.stateNode, a = c.getSnapshotBeforeUpdate(n.elementType === n.type ? w : ze(n.type, w), N);
            c.__reactInternalSnapshotBeforeUpdate = a;
          }
          break;
        case 3:
          var d = n.stateNode.containerInfo;
          d.nodeType === 1 ? d.textContent = "" : d.nodeType === 9 && d.documentElement && d.removeChild(d.documentElement);
          break;
        case 5:
        case 6:
        case 4:
        case 17:
          break;
        default:
          throw Error(g(163));
      }
    } catch (y) {
      V(n, n.return, y);
    }
    if (e = n.sibling, e !== null) {
      e.return = n.return, k = e;
      break;
    }
    k = n.return;
  }
  return v = Ti, Ti = !1, v;
}
function Nt(e, n, t) {
  var r = n.updateQueue;
  if (r = r !== null ? r.lastEffect : null, r !== null) {
    var l = r = r.next;
    do {
      if ((l.tag & e) === e) {
        var o = l.destroy;
        l.destroy = void 0, o !== void 0 && Lo(n, t, o);
      }
      l = l.next;
    } while (l !== r);
  }
}
function sl(e, n) {
  if (n = n.updateQueue, n = n !== null ? n.lastEffect : null, n !== null) {
    var t = n = n.next;
    do {
      if ((t.tag & e) === e) {
        var r = t.create;
        t.destroy = r();
      }
      t = t.next;
    } while (t !== n);
  }
}
function To(e) {
  var n = e.ref;
  if (n !== null) {
    var t = e.stateNode;
    switch (e.tag) {
      case 5:
        e = t;
        break;
      default:
        e = t;
    }
    typeof n == "function" ? n(e) : n.current = e;
  }
}
function Da(e) {
  var n = e.alternate;
  n !== null && (e.alternate = null, Da(n)), e.child = null, e.deletions = null, e.sibling = null, e.tag === 5 && (n = e.stateNode, n !== null && (delete n[Fe], delete n[At], delete n[vo], delete n[jf], delete n[$f])), e.stateNode = null, e.return = null, e.dependencies = null, e.memoizedProps = null, e.memoizedState = null, e.pendingProps = null, e.stateNode = null, e.updateQueue = null;
}
function Ia(e) {
  return e.tag === 5 || e.tag === 3 || e.tag === 4;
}
function Ri(e) {
  e: for (; ; ) {
    for (; e.sibling === null; ) {
      if (e.return === null || Ia(e.return)) return null;
      e = e.return;
    }
    for (e.sibling.return = e.return, e = e.sibling; e.tag !== 5 && e.tag !== 6 && e.tag !== 18; ) {
      if (e.flags & 2 || e.child === null || e.tag === 4) continue e;
      e.child.return = e, e = e.child;
    }
    if (!(e.flags & 2)) return e.stateNode;
  }
}
function Ro(e, n, t) {
  var r = e.tag;
  if (r === 5 || r === 6) e = e.stateNode, n ? t.nodeType === 8 ? t.parentNode.insertBefore(e, n) : t.insertBefore(e, n) : (t.nodeType === 8 ? (n = t.parentNode, n.insertBefore(e, t)) : (n = t, n.appendChild(e)), t = t._reactRootContainer, t != null || n.onclick !== null || (n.onclick = jr));
  else if (r !== 4 && (e = e.child, e !== null)) for (Ro(e, n, t), e = e.sibling; e !== null; ) Ro(e, n, t), e = e.sibling;
}
function Mo(e, n, t) {
  var r = e.tag;
  if (r === 5 || r === 6) e = e.stateNode, n ? t.insertBefore(e, n) : t.appendChild(e);
  else if (r !== 4 && (e = e.child, e !== null)) for (Mo(e, n, t), e = e.sibling; e !== null; ) Mo(e, n, t), e = e.sibling;
}
var J = null, Le = !1;
function Ge(e, n, t) {
  for (t = t.child; t !== null; ) Fa(e, n, t), t = t.sibling;
}
function Fa(e, n, t) {
  if (Ue && typeof Ue.onCommitFiberUnmount == "function") try {
    Ue.onCommitFiberUnmount(el, t);
  } catch {
  }
  switch (t.tag) {
    case 5:
      re || Hn(t, n);
    case 6:
      var r = J, l = Le;
      J = null, Ge(e, n, t), J = r, Le = l, J !== null && (Le ? (e = J, t = t.stateNode, e.nodeType === 8 ? e.parentNode.removeChild(t) : e.removeChild(t)) : J.removeChild(t.stateNode));
      break;
    case 18:
      J !== null && (Le ? (e = J, t = t.stateNode, e.nodeType === 8 ? Dl(e.parentNode, t) : e.nodeType === 1 && Dl(e, t), It(e)) : Dl(J, t.stateNode));
      break;
    case 4:
      r = J, l = Le, J = t.stateNode.containerInfo, Le = !0, Ge(e, n, t), J = r, Le = l;
      break;
    case 0:
    case 11:
    case 14:
    case 15:
      if (!re && (r = t.updateQueue, r !== null && (r = r.lastEffect, r !== null))) {
        l = r = r.next;
        do {
          var o = l, u = o.destroy;
          o = o.tag, u !== void 0 && (o & 2 || o & 4) && Lo(t, n, u), l = l.next;
        } while (l !== r);
      }
      Ge(e, n, t);
      break;
    case 1:
      if (!re && (Hn(t, n), r = t.stateNode, typeof r.componentWillUnmount == "function")) try {
        r.props = t.memoizedProps, r.state = t.memoizedState, r.componentWillUnmount();
      } catch (i) {
        V(t, n, i);
      }
      Ge(e, n, t);
      break;
    case 21:
      Ge(e, n, t);
      break;
    case 22:
      t.mode & 1 ? (re = (r = re) || t.memoizedState !== null, Ge(e, n, t), re = r) : Ge(e, n, t);
      break;
    default:
      Ge(e, n, t);
  }
}
function Mi(e) {
  var n = e.updateQueue;
  if (n !== null) {
    e.updateQueue = null;
    var t = e.stateNode;
    t === null && (t = e.stateNode = new nd()), n.forEach(function(r) {
      var l = fd.bind(null, e, r);
      t.has(r) || (t.add(r), r.then(l, l));
    });
  }
}
function Ne(e, n) {
  var t = n.deletions;
  if (t !== null) for (var r = 0; r < t.length; r++) {
    var l = t[r];
    try {
      var o = e, u = n, i = u;
      e: for (; i !== null; ) {
        switch (i.tag) {
          case 5:
            J = i.stateNode, Le = !1;
            break e;
          case 3:
            J = i.stateNode.containerInfo, Le = !0;
            break e;
          case 4:
            J = i.stateNode.containerInfo, Le = !0;
            break e;
        }
        i = i.return;
      }
      if (J === null) throw Error(g(160));
      Fa(o, u, l), J = null, Le = !1;
      var s = l.alternate;
      s !== null && (s.return = null), l.return = null;
    } catch (f) {
      V(l, n, f);
    }
  }
  if (n.subtreeFlags & 12854) for (n = n.child; n !== null; ) Ua(n, e), n = n.sibling;
}
function Ua(e, n) {
  var t = e.alternate, r = e.flags;
  switch (e.tag) {
    case 0:
    case 11:
    case 14:
    case 15:
      if (Ne(n, e), De(e), r & 4) {
        try {
          Nt(3, e, e.return), sl(3, e);
        } catch (w) {
          V(e, e.return, w);
        }
        try {
          Nt(5, e, e.return);
        } catch (w) {
          V(e, e.return, w);
        }
      }
      break;
    case 1:
      Ne(n, e), De(e), r & 512 && t !== null && Hn(t, t.return);
      break;
    case 5:
      if (Ne(n, e), De(e), r & 512 && t !== null && Hn(t, t.return), e.flags & 32) {
        var l = e.stateNode;
        try {
          Rt(l, "");
        } catch (w) {
          V(e, e.return, w);
        }
      }
      if (r & 4 && (l = e.stateNode, l != null)) {
        var o = e.memoizedProps, u = t !== null ? t.memoizedProps : o, i = e.type, s = e.updateQueue;
        if (e.updateQueue = null, s !== null) try {
          i === "input" && o.type === "radio" && o.name != null && os(l, o), no(i, u);
          var f = no(i, o);
          for (u = 0; u < s.length; u += 2) {
            var h = s[u], m = s[u + 1];
            h === "style" ? cs(l, m) : h === "dangerouslySetInnerHTML" ? ss(l, m) : h === "children" ? Rt(l, m) : Ho(l, h, m, f);
          }
          switch (i) {
            case "input":
              Zl(l, o);
              break;
            case "textarea":
              us(l, o);
              break;
            case "select":
              var p = l._wrapperState.wasMultiple;
              l._wrapperState.wasMultiple = !!o.multiple;
              var S = o.value;
              S != null ? Wn(l, !!o.multiple, S, !1) : p !== !!o.multiple && (o.defaultValue != null ? Wn(
                l,
                !!o.multiple,
                o.defaultValue,
                !0
              ) : Wn(l, !!o.multiple, o.multiple ? [] : "", !1));
          }
          l[At] = o;
        } catch (w) {
          V(e, e.return, w);
        }
      }
      break;
    case 6:
      if (Ne(n, e), De(e), r & 4) {
        if (e.stateNode === null) throw Error(g(162));
        l = e.stateNode, o = e.memoizedProps;
        try {
          l.nodeValue = o;
        } catch (w) {
          V(e, e.return, w);
        }
      }
      break;
    case 3:
      if (Ne(n, e), De(e), r & 4 && t !== null && t.memoizedState.isDehydrated) try {
        It(n.containerInfo);
      } catch (w) {
        V(e, e.return, w);
      }
      break;
    case 4:
      Ne(n, e), De(e);
      break;
    case 13:
      Ne(n, e), De(e), l = e.child, l.flags & 8192 && (o = l.memoizedState !== null, l.stateNode.isHidden = o, !o || l.alternate !== null && l.alternate.memoizedState !== null || (Eu = Q())), r & 4 && Mi(e);
      break;
    case 22:
      if (h = t !== null && t.memoizedState !== null, e.mode & 1 ? (re = (f = re) || h, Ne(n, e), re = f) : Ne(n, e), De(e), r & 8192) {
        if (f = e.memoizedState !== null, (e.stateNode.isHidden = f) && !h && e.mode & 1) for (k = e, h = e.child; h !== null; ) {
          for (m = k = h; k !== null; ) {
            switch (p = k, S = p.child, p.tag) {
              case 0:
              case 11:
              case 14:
              case 15:
                Nt(4, p, p.return);
                break;
              case 1:
                Hn(p, p.return);
                var v = p.stateNode;
                if (typeof v.componentWillUnmount == "function") {
                  r = p, t = p.return;
                  try {
                    n = r, v.props = n.memoizedProps, v.state = n.memoizedState, v.componentWillUnmount();
                  } catch (w) {
                    V(r, t, w);
                  }
                }
                break;
              case 5:
                Hn(p, p.return);
                break;
              case 22:
                if (p.memoizedState !== null) {
                  Di(m);
                  continue;
                }
            }
            S !== null ? (S.return = p, k = S) : Di(m);
          }
          h = h.sibling;
        }
        e: for (h = null, m = e; ; ) {
          if (m.tag === 5) {
            if (h === null) {
              h = m;
              try {
                l = m.stateNode, f ? (o = l.style, typeof o.setProperty == "function" ? o.setProperty("display", "none", "important") : o.display = "none") : (i = m.stateNode, s = m.memoizedProps.style, u = s != null && s.hasOwnProperty("display") ? s.display : null, i.style.display = as("display", u));
              } catch (w) {
                V(e, e.return, w);
              }
            }
          } else if (m.tag === 6) {
            if (h === null) try {
              m.stateNode.nodeValue = f ? "" : m.memoizedProps;
            } catch (w) {
              V(e, e.return, w);
            }
          } else if ((m.tag !== 22 && m.tag !== 23 || m.memoizedState === null || m === e) && m.child !== null) {
            m.child.return = m, m = m.child;
            continue;
          }
          if (m === e) break e;
          for (; m.sibling === null; ) {
            if (m.return === null || m.return === e) break e;
            h === m && (h = null), m = m.return;
          }
          h === m && (h = null), m.sibling.return = m.return, m = m.sibling;
        }
      }
      break;
    case 19:
      Ne(n, e), De(e), r & 4 && Mi(e);
      break;
    case 21:
      break;
    default:
      Ne(
        n,
        e
      ), De(e);
  }
}
function De(e) {
  var n = e.flags;
  if (n & 2) {
    try {
      e: {
        for (var t = e.return; t !== null; ) {
          if (Ia(t)) {
            var r = t;
            break e;
          }
          t = t.return;
        }
        throw Error(g(160));
      }
      switch (r.tag) {
        case 5:
          var l = r.stateNode;
          r.flags & 32 && (Rt(l, ""), r.flags &= -33);
          var o = Ri(e);
          Mo(e, o, l);
          break;
        case 3:
        case 4:
          var u = r.stateNode.containerInfo, i = Ri(e);
          Ro(e, i, u);
          break;
        default:
          throw Error(g(161));
      }
    } catch (s) {
      V(e, e.return, s);
    }
    e.flags &= -3;
  }
  n & 4096 && (e.flags &= -4097);
}
function rd(e, n, t) {
  k = e, ja(e);
}
function ja(e, n, t) {
  for (var r = (e.mode & 1) !== 0; k !== null; ) {
    var l = k, o = l.child;
    if (l.tag === 22 && r) {
      var u = l.memoizedState !== null || mr;
      if (!u) {
        var i = l.alternate, s = i !== null && i.memoizedState !== null || re;
        i = mr;
        var f = re;
        if (mr = u, (re = s) && !f) for (k = l; k !== null; ) u = k, s = u.child, u.tag === 22 && u.memoizedState !== null ? Ii(l) : s !== null ? (s.return = u, k = s) : Ii(l);
        for (; o !== null; ) k = o, ja(o), o = o.sibling;
        k = l, mr = i, re = f;
      }
      Oi(e);
    } else l.subtreeFlags & 8772 && o !== null ? (o.return = l, k = o) : Oi(e);
  }
}
function Oi(e) {
  for (; k !== null; ) {
    var n = k;
    if (n.flags & 8772) {
      var t = n.alternate;
      try {
        if (n.flags & 8772) switch (n.tag) {
          case 0:
          case 11:
          case 15:
            re || sl(5, n);
            break;
          case 1:
            var r = n.stateNode;
            if (n.flags & 4 && !re) if (t === null) r.componentDidMount();
            else {
              var l = n.elementType === n.type ? t.memoizedProps : ze(n.type, t.memoizedProps);
              r.componentDidUpdate(l, t.memoizedState, r.__reactInternalSnapshotBeforeUpdate);
            }
            var o = n.updateQueue;
            o !== null && yi(n, o, r);
            break;
          case 3:
            var u = n.updateQueue;
            if (u !== null) {
              if (t = null, n.child !== null) switch (n.child.tag) {
                case 5:
                  t = n.child.stateNode;
                  break;
                case 1:
                  t = n.child.stateNode;
              }
              yi(n, u, t);
            }
            break;
          case 5:
            var i = n.stateNode;
            if (t === null && n.flags & 4) {
              t = i;
              var s = n.memoizedProps;
              switch (n.type) {
                case "button":
                case "input":
                case "select":
                case "textarea":
                  s.autoFocus && t.focus();
                  break;
                case "img":
                  s.src && (t.src = s.src);
              }
            }
            break;
          case 6:
            break;
          case 4:
            break;
          case 12:
            break;
          case 13:
            if (n.memoizedState === null) {
              var f = n.alternate;
              if (f !== null) {
                var h = f.memoizedState;
                if (h !== null) {
                  var m = h.dehydrated;
                  m !== null && It(m);
                }
              }
            }
            break;
          case 19:
          case 17:
          case 21:
          case 22:
          case 23:
          case 25:
            break;
          default:
            throw Error(g(163));
        }
        re || n.flags & 512 && To(n);
      } catch (p) {
        V(n, n.return, p);
      }
    }
    if (n === e) {
      k = null;
      break;
    }
    if (t = n.sibling, t !== null) {
      t.return = n.return, k = t;
      break;
    }
    k = n.return;
  }
}
function Di(e) {
  for (; k !== null; ) {
    var n = k;
    if (n === e) {
      k = null;
      break;
    }
    var t = n.sibling;
    if (t !== null) {
      t.return = n.return, k = t;
      break;
    }
    k = n.return;
  }
}
function Ii(e) {
  for (; k !== null; ) {
    var n = k;
    try {
      switch (n.tag) {
        case 0:
        case 11:
        case 15:
          var t = n.return;
          try {
            sl(4, n);
          } catch (s) {
            V(n, t, s);
          }
          break;
        case 1:
          var r = n.stateNode;
          if (typeof r.componentDidMount == "function") {
            var l = n.return;
            try {
              r.componentDidMount();
            } catch (s) {
              V(n, l, s);
            }
          }
          var o = n.return;
          try {
            To(n);
          } catch (s) {
            V(n, o, s);
          }
          break;
        case 5:
          var u = n.return;
          try {
            To(n);
          } catch (s) {
            V(n, u, s);
          }
      }
    } catch (s) {
      V(n, n.return, s);
    }
    if (n === e) {
      k = null;
      break;
    }
    var i = n.sibling;
    if (i !== null) {
      i.return = n.return, k = i;
      break;
    }
    k = n.return;
  }
}
var ld = Math.ceil, Gr = Xe.ReactCurrentDispatcher, Su = Xe.ReactCurrentOwner, Ce = Xe.ReactCurrentBatchConfig, M = 0, Z = null, W = null, q = 0, me = 0, Qn = mn(0), Y = 0, Kt = null, zn = 0, al = 0, ku = 0, zt = null, ae = null, Eu = 0, rt = 1 / 0, $e = null, Zr = !1, Oo = null, sn = null, hr = !1, nn = null, Jr = 0, Lt = 0, Do = null, Nr = -1, zr = 0;
function ue() {
  return M & 6 ? Q() : Nr !== -1 ? Nr : Nr = Q();
}
function an(e) {
  return e.mode & 1 ? M & 2 && q !== 0 ? q & -q : Vf.transition !== null ? (zr === 0 && (zr = Es()), zr) : (e = O, e !== 0 || (e = window.event, e = e === void 0 ? 16 : Ls(e.type)), e) : 1;
}
function Me(e, n, t, r) {
  if (50 < Lt) throw Lt = 0, Do = null, Error(g(185));
  Xt(e, t, r), (!(M & 2) || e !== Z) && (e === Z && (!(M & 2) && (al |= t), Y === 4 && be(e, q)), pe(e, r), t === 1 && M === 0 && !(n.mode & 1) && (rt = Q() + 500, ol && hn()));
}
function pe(e, n) {
  var t = e.callbackNode;
  Ac(e, n);
  var r = Dr(e, e === Z ? q : 0);
  if (r === 0) t !== null && Qu(t), e.callbackNode = null, e.callbackPriority = 0;
  else if (n = r & -r, e.callbackPriority !== n) {
    if (t != null && Qu(t), n === 1) e.tag === 0 ? Af(Fi.bind(null, e)) : Xs(Fi.bind(null, e)), Ff(function() {
      !(M & 6) && hn();
    }), t = null;
    else {
      switch (Cs(r)) {
        case 1:
          t = Xo;
          break;
        case 4:
          t = Ss;
          break;
        case 16:
          t = Or;
          break;
        case 536870912:
          t = ks;
          break;
        default:
          t = Or;
      }
      t = Ka(t, $a.bind(null, e));
    }
    e.callbackPriority = n, e.callbackNode = t;
  }
}
function $a(e, n) {
  if (Nr = -1, zr = 0, M & 6) throw Error(g(327));
  var t = e.callbackNode;
  if (Zn() && e.callbackNode !== t) return null;
  var r = Dr(e, e === Z ? q : 0);
  if (r === 0) return null;
  if (r & 30 || r & e.expiredLanes || n) n = qr(e, r);
  else {
    n = r;
    var l = M;
    M |= 2;
    var o = Va();
    (Z !== e || q !== n) && ($e = null, rt = Q() + 500, Cn(e, n));
    do
      try {
        id();
        break;
      } catch (i) {
        Aa(e, i);
      }
    while (!0);
    iu(), Gr.current = o, M = l, W !== null ? n = 0 : (Z = null, q = 0, n = Y);
  }
  if (n !== 0) {
    if (n === 2 && (l = uo(e), l !== 0 && (r = l, n = Io(e, l))), n === 1) throw t = Kt, Cn(e, 0), be(e, r), pe(e, Q()), t;
    if (n === 6) be(e, r);
    else {
      if (l = e.current.alternate, !(r & 30) && !od(l) && (n = qr(e, r), n === 2 && (o = uo(e), o !== 0 && (r = o, n = Io(e, o))), n === 1)) throw t = Kt, Cn(e, 0), be(e, r), pe(e, Q()), t;
      switch (e.finishedWork = l, e.finishedLanes = r, n) {
        case 0:
        case 1:
          throw Error(g(345));
        case 2:
          wn(e, ae, $e);
          break;
        case 3:
          if (be(e, r), (r & 130023424) === r && (n = Eu + 500 - Q(), 10 < n)) {
            if (Dr(e, 0) !== 0) break;
            if (l = e.suspendedLanes, (l & r) !== r) {
              ue(), e.pingedLanes |= e.suspendedLanes & l;
              break;
            }
            e.timeoutHandle = ho(wn.bind(null, e, ae, $e), n);
            break;
          }
          wn(e, ae, $e);
          break;
        case 4:
          if (be(e, r), (r & 4194240) === r) break;
          for (n = e.eventTimes, l = -1; 0 < r; ) {
            var u = 31 - Re(r);
            o = 1 << u, u = n[u], u > l && (l = u), r &= ~o;
          }
          if (r = l, r = Q() - r, r = (120 > r ? 120 : 480 > r ? 480 : 1080 > r ? 1080 : 1920 > r ? 1920 : 3e3 > r ? 3e3 : 4320 > r ? 4320 : 1960 * ld(r / 1960)) - r, 10 < r) {
            e.timeoutHandle = ho(wn.bind(null, e, ae, $e), r);
            break;
          }
          wn(e, ae, $e);
          break;
        case 5:
          wn(e, ae, $e);
          break;
        default:
          throw Error(g(329));
      }
    }
  }
  return pe(e, Q()), e.callbackNode === t ? $a.bind(null, e) : null;
}
function Io(e, n) {
  var t = zt;
  return e.current.memoizedState.isDehydrated && (Cn(e, n).flags |= 256), e = qr(e, n), e !== 2 && (n = ae, ae = t, n !== null && Fo(n)), e;
}
function Fo(e) {
  ae === null ? ae = e : ae.push.apply(ae, e);
}
function od(e) {
  for (var n = e; ; ) {
    if (n.flags & 16384) {
      var t = n.updateQueue;
      if (t !== null && (t = t.stores, t !== null)) for (var r = 0; r < t.length; r++) {
        var l = t[r], o = l.getSnapshot;
        l = l.value;
        try {
          if (!Oe(o(), l)) return !1;
        } catch {
          return !1;
        }
      }
    }
    if (t = n.child, n.subtreeFlags & 16384 && t !== null) t.return = n, n = t;
    else {
      if (n === e) break;
      for (; n.sibling === null; ) {
        if (n.return === null || n.return === e) return !0;
        n = n.return;
      }
      n.sibling.return = n.return, n = n.sibling;
    }
  }
  return !0;
}
function be(e, n) {
  for (n &= ~ku, n &= ~al, e.suspendedLanes |= n, e.pingedLanes &= ~n, e = e.expirationTimes; 0 < n; ) {
    var t = 31 - Re(n), r = 1 << t;
    e[t] = -1, n &= ~r;
  }
}
function Fi(e) {
  if (M & 6) throw Error(g(327));
  Zn();
  var n = Dr(e, 0);
  if (!(n & 1)) return pe(e, Q()), null;
  var t = qr(e, n);
  if (e.tag !== 0 && t === 2) {
    var r = uo(e);
    r !== 0 && (n = r, t = Io(e, r));
  }
  if (t === 1) throw t = Kt, Cn(e, 0), be(e, n), pe(e, Q()), t;
  if (t === 6) throw Error(g(345));
  return e.finishedWork = e.current.alternate, e.finishedLanes = n, wn(e, ae, $e), pe(e, Q()), null;
}
function Cu(e, n) {
  var t = M;
  M |= 1;
  try {
    return e(n);
  } finally {
    M = t, M === 0 && (rt = Q() + 500, ol && hn());
  }
}
function Ln(e) {
  nn !== null && nn.tag === 0 && !(M & 6) && Zn();
  var n = M;
  M |= 1;
  var t = Ce.transition, r = O;
  try {
    if (Ce.transition = null, O = 1, e) return e();
  } finally {
    O = r, Ce.transition = t, M = n, !(M & 6) && hn();
  }
}
function _u() {
  me = Qn.current, F(Qn);
}
function Cn(e, n) {
  e.finishedWork = null, e.finishedLanes = 0;
  var t = e.timeoutHandle;
  if (t !== -1 && (e.timeoutHandle = -1, If(t)), W !== null) for (t = W.return; t !== null; ) {
    var r = t;
    switch (lu(r), r.tag) {
      case 1:
        r = r.type.childContextTypes, r != null && $r();
        break;
      case 3:
        nt(), F(fe), F(le), pu();
        break;
      case 5:
        du(r);
        break;
      case 4:
        nt();
        break;
      case 13:
        F(j);
        break;
      case 19:
        F(j);
        break;
      case 10:
        su(r.type._context);
        break;
      case 22:
      case 23:
        _u();
    }
    t = t.return;
  }
  if (Z = e, W = e = cn(e.current, null), q = me = n, Y = 0, Kt = null, ku = al = zn = 0, ae = zt = null, kn !== null) {
    for (n = 0; n < kn.length; n++) if (t = kn[n], r = t.interleaved, r !== null) {
      t.interleaved = null;
      var l = r.next, o = t.pending;
      if (o !== null) {
        var u = o.next;
        o.next = l, r.next = u;
      }
      t.pending = r;
    }
    kn = null;
  }
  return e;
}
function Aa(e, n) {
  do {
    var t = W;
    try {
      if (iu(), _r.current = Xr, Yr) {
        for (var r = $.memoizedState; r !== null; ) {
          var l = r.queue;
          l !== null && (l.pending = null), r = r.next;
        }
        Yr = !1;
      }
      if (Nn = 0, G = K = $ = null, Pt = !1, Ht = 0, Su.current = null, t === null || t.return === null) {
        Y = 1, Kt = n, W = null;
        break;
      }
      e: {
        var o = e, u = t.return, i = t, s = n;
        if (n = q, i.flags |= 32768, s !== null && typeof s == "object" && typeof s.then == "function") {
          var f = s, h = i, m = h.tag;
          if (!(h.mode & 1) && (m === 0 || m === 11 || m === 15)) {
            var p = h.alternate;
            p ? (h.updateQueue = p.updateQueue, h.memoizedState = p.memoizedState, h.lanes = p.lanes) : (h.updateQueue = null, h.memoizedState = null);
          }
          var S = Ci(u);
          if (S !== null) {
            S.flags &= -257, _i(S, u, i, o, n), S.mode & 1 && Ei(o, f, n), n = S, s = f;
            var v = n.updateQueue;
            if (v === null) {
              var w = /* @__PURE__ */ new Set();
              w.add(s), n.updateQueue = w;
            } else v.add(s);
            break e;
          } else {
            if (!(n & 1)) {
              Ei(o, f, n), xu();
              break e;
            }
            s = Error(g(426));
          }
        } else if (U && i.mode & 1) {
          var N = Ci(u);
          if (N !== null) {
            !(N.flags & 65536) && (N.flags |= 256), _i(N, u, i, o, n), ou(tt(s, i));
            break e;
          }
        }
        o = s = tt(s, i), Y !== 4 && (Y = 2), zt === null ? zt = [o] : zt.push(o), o = u;
        do {
          switch (o.tag) {
            case 3:
              o.flags |= 65536, n &= -n, o.lanes |= n;
              var c = Ca(o, s, n);
              vi(o, c);
              break e;
            case 1:
              i = s;
              var a = o.type, d = o.stateNode;
              if (!(o.flags & 128) && (typeof a.getDerivedStateFromError == "function" || d !== null && typeof d.componentDidCatch == "function" && (sn === null || !sn.has(d)))) {
                o.flags |= 65536, n &= -n, o.lanes |= n;
                var y = _a(o, i, n);
                vi(o, y);
                break e;
              }
          }
          o = o.return;
        } while (o !== null);
      }
      Ha(t);
    } catch (E) {
      n = E, W === t && t !== null && (W = t = t.return);
      continue;
    }
    break;
  } while (!0);
}
function Va() {
  var e = Gr.current;
  return Gr.current = Xr, e === null ? Xr : e;
}
function xu() {
  (Y === 0 || Y === 3 || Y === 2) && (Y = 4), Z === null || !(zn & 268435455) && !(al & 268435455) || be(Z, q);
}
function qr(e, n) {
  var t = M;
  M |= 2;
  var r = Va();
  (Z !== e || q !== n) && ($e = null, Cn(e, n));
  do
    try {
      ud();
      break;
    } catch (l) {
      Aa(e, l);
    }
  while (!0);
  if (iu(), M = t, Gr.current = r, W !== null) throw Error(g(261));
  return Z = null, q = 0, Y;
}
function ud() {
  for (; W !== null; ) Ba(W);
}
function id() {
  for (; W !== null && !Rc(); ) Ba(W);
}
function Ba(e) {
  var n = Wa(e.alternate, e, me);
  e.memoizedProps = e.pendingProps, n === null ? Ha(e) : W = n, Su.current = null;
}
function Ha(e) {
  var n = e;
  do {
    var t = n.alternate;
    if (e = n.return, n.flags & 32768) {
      if (t = ed(t, n), t !== null) {
        t.flags &= 32767, W = t;
        return;
      }
      if (e !== null) e.flags |= 32768, e.subtreeFlags = 0, e.deletions = null;
      else {
        Y = 6, W = null;
        return;
      }
    } else if (t = bf(t, n, me), t !== null) {
      W = t;
      return;
    }
    if (n = n.sibling, n !== null) {
      W = n;
      return;
    }
    W = n = e;
  } while (n !== null);
  Y === 0 && (Y = 5);
}
function wn(e, n, t) {
  var r = O, l = Ce.transition;
  try {
    Ce.transition = null, O = 1, sd(e, n, t, r);
  } finally {
    Ce.transition = l, O = r;
  }
  return null;
}
function sd(e, n, t, r) {
  do
    Zn();
  while (nn !== null);
  if (M & 6) throw Error(g(327));
  t = e.finishedWork;
  var l = e.finishedLanes;
  if (t === null) return null;
  if (e.finishedWork = null, e.finishedLanes = 0, t === e.current) throw Error(g(177));
  e.callbackNode = null, e.callbackPriority = 0;
  var o = t.lanes | t.childLanes;
  if (Vc(e, o), e === Z && (W = Z = null, q = 0), !(t.subtreeFlags & 2064) && !(t.flags & 2064) || hr || (hr = !0, Ka(Or, function() {
    return Zn(), null;
  })), o = (t.flags & 15990) !== 0, t.subtreeFlags & 15990 || o) {
    o = Ce.transition, Ce.transition = null;
    var u = O;
    O = 1;
    var i = M;
    M |= 4, Su.current = null, td(e, t), Ua(t, e), zf(po), Ir = !!fo, po = fo = null, e.current = t, rd(t), Mc(), M = i, O = u, Ce.transition = o;
  } else e.current = t;
  if (hr && (hr = !1, nn = e, Jr = l), o = e.pendingLanes, o === 0 && (sn = null), Ic(t.stateNode), pe(e, Q()), n !== null) for (r = e.onRecoverableError, t = 0; t < n.length; t++) l = n[t], r(l.value, { componentStack: l.stack, digest: l.digest });
  if (Zr) throw Zr = !1, e = Oo, Oo = null, e;
  return Jr & 1 && e.tag !== 0 && Zn(), o = e.pendingLanes, o & 1 ? e === Do ? Lt++ : (Lt = 0, Do = e) : Lt = 0, hn(), null;
}
function Zn() {
  if (nn !== null) {
    var e = Cs(Jr), n = Ce.transition, t = O;
    try {
      if (Ce.transition = null, O = 16 > e ? 16 : e, nn === null) var r = !1;
      else {
        if (e = nn, nn = null, Jr = 0, M & 6) throw Error(g(331));
        var l = M;
        for (M |= 4, k = e.current; k !== null; ) {
          var o = k, u = o.child;
          if (k.flags & 16) {
            var i = o.deletions;
            if (i !== null) {
              for (var s = 0; s < i.length; s++) {
                var f = i[s];
                for (k = f; k !== null; ) {
                  var h = k;
                  switch (h.tag) {
                    case 0:
                    case 11:
                    case 15:
                      Nt(8, h, o);
                  }
                  var m = h.child;
                  if (m !== null) m.return = h, k = m;
                  else for (; k !== null; ) {
                    h = k;
                    var p = h.sibling, S = h.return;
                    if (Da(h), h === f) {
                      k = null;
                      break;
                    }
                    if (p !== null) {
                      p.return = S, k = p;
                      break;
                    }
                    k = S;
                  }
                }
              }
              var v = o.alternate;
              if (v !== null) {
                var w = v.child;
                if (w !== null) {
                  v.child = null;
                  do {
                    var N = w.sibling;
                    w.sibling = null, w = N;
                  } while (w !== null);
                }
              }
              k = o;
            }
          }
          if (o.subtreeFlags & 2064 && u !== null) u.return = o, k = u;
          else e: for (; k !== null; ) {
            if (o = k, o.flags & 2048) switch (o.tag) {
              case 0:
              case 11:
              case 15:
                Nt(9, o, o.return);
            }
            var c = o.sibling;
            if (c !== null) {
              c.return = o.return, k = c;
              break e;
            }
            k = o.return;
          }
        }
        var a = e.current;
        for (k = a; k !== null; ) {
          u = k;
          var d = u.child;
          if (u.subtreeFlags & 2064 && d !== null) d.return = u, k = d;
          else e: for (u = a; k !== null; ) {
            if (i = k, i.flags & 2048) try {
              switch (i.tag) {
                case 0:
                case 11:
                case 15:
                  sl(9, i);
              }
            } catch (E) {
              V(i, i.return, E);
            }
            if (i === u) {
              k = null;
              break e;
            }
            var y = i.sibling;
            if (y !== null) {
              y.return = i.return, k = y;
              break e;
            }
            k = i.return;
          }
        }
        if (M = l, hn(), Ue && typeof Ue.onPostCommitFiberRoot == "function") try {
          Ue.onPostCommitFiberRoot(el, e);
        } catch {
        }
        r = !0;
      }
      return r;
    } finally {
      O = t, Ce.transition = n;
    }
  }
  return !1;
}
function Ui(e, n, t) {
  n = tt(t, n), n = Ca(e, n, 1), e = un(e, n, 1), n = ue(), e !== null && (Xt(e, 1, n), pe(e, n));
}
function V(e, n, t) {
  if (e.tag === 3) Ui(e, e, t);
  else for (; n !== null; ) {
    if (n.tag === 3) {
      Ui(n, e, t);
      break;
    } else if (n.tag === 1) {
      var r = n.stateNode;
      if (typeof n.type.getDerivedStateFromError == "function" || typeof r.componentDidCatch == "function" && (sn === null || !sn.has(r))) {
        e = tt(t, e), e = _a(n, e, 1), n = un(n, e, 1), e = ue(), n !== null && (Xt(n, 1, e), pe(n, e));
        break;
      }
    }
    n = n.return;
  }
}
function ad(e, n, t) {
  var r = e.pingCache;
  r !== null && r.delete(n), n = ue(), e.pingedLanes |= e.suspendedLanes & t, Z === e && (q & t) === t && (Y === 4 || Y === 3 && (q & 130023424) === q && 500 > Q() - Eu ? Cn(e, 0) : ku |= t), pe(e, n);
}
function Qa(e, n) {
  n === 0 && (e.mode & 1 ? (n = or, or <<= 1, !(or & 130023424) && (or = 4194304)) : n = 1);
  var t = ue();
  e = Ke(e, n), e !== null && (Xt(e, n, t), pe(e, t));
}
function cd(e) {
  var n = e.memoizedState, t = 0;
  n !== null && (t = n.retryLane), Qa(e, t);
}
function fd(e, n) {
  var t = 0;
  switch (e.tag) {
    case 13:
      var r = e.stateNode, l = e.memoizedState;
      l !== null && (t = l.retryLane);
      break;
    case 19:
      r = e.stateNode;
      break;
    default:
      throw Error(g(314));
  }
  r !== null && r.delete(n), Qa(e, t);
}
var Wa;
Wa = function(e, n, t) {
  if (e !== null) if (e.memoizedProps !== n.pendingProps || fe.current) ce = !0;
  else {
    if (!(e.lanes & t) && !(n.flags & 128)) return ce = !1, qf(e, n, t);
    ce = !!(e.flags & 131072);
  }
  else ce = !1, U && n.flags & 1048576 && Gs(n, Br, n.index);
  switch (n.lanes = 0, n.tag) {
    case 2:
      var r = n.type;
      Pr(e, n), e = n.pendingProps;
      var l = qn(n, le.current);
      Gn(n, t), l = hu(null, n, r, e, l, t);
      var o = vu();
      return n.flags |= 1, typeof l == "object" && l !== null && typeof l.render == "function" && l.$$typeof === void 0 ? (n.tag = 1, n.memoizedState = null, n.updateQueue = null, de(r) ? (o = !0, Ar(n)) : o = !1, n.memoizedState = l.state !== null && l.state !== void 0 ? l.state : null, cu(n), l.updater = il, n.stateNode = l, l._reactInternals = n, Eo(n, r, e, t), n = xo(null, n, r, !0, o, t)) : (n.tag = 0, U && o && ru(n), oe(null, n, l, t), n = n.child), n;
    case 16:
      r = n.elementType;
      e: {
        switch (Pr(e, n), e = n.pendingProps, l = r._init, r = l(r._payload), n.type = r, l = n.tag = pd(r), e = ze(r, e), l) {
          case 0:
            n = _o(null, n, r, e, t);
            break e;
          case 1:
            n = Ni(null, n, r, e, t);
            break e;
          case 11:
            n = xi(null, n, r, e, t);
            break e;
          case 14:
            n = Pi(null, n, r, ze(r.type, e), t);
            break e;
        }
        throw Error(g(
          306,
          r,
          ""
        ));
      }
      return n;
    case 0:
      return r = n.type, l = n.pendingProps, l = n.elementType === r ? l : ze(r, l), _o(e, n, r, l, t);
    case 1:
      return r = n.type, l = n.pendingProps, l = n.elementType === r ? l : ze(r, l), Ni(e, n, r, l, t);
    case 3:
      e: {
        if (za(n), e === null) throw Error(g(387));
        r = n.pendingProps, o = n.memoizedState, l = o.element, na(e, n), Wr(n, r, null, t);
        var u = n.memoizedState;
        if (r = u.element, o.isDehydrated) if (o = { element: r, isDehydrated: !1, cache: u.cache, pendingSuspenseBoundaries: u.pendingSuspenseBoundaries, transitions: u.transitions }, n.updateQueue.baseState = o, n.memoizedState = o, n.flags & 256) {
          l = tt(Error(g(423)), n), n = zi(e, n, r, t, l);
          break e;
        } else if (r !== l) {
          l = tt(Error(g(424)), n), n = zi(e, n, r, t, l);
          break e;
        } else for (he = on(n.stateNode.containerInfo.firstChild), ve = n, U = !0, Te = null, t = bs(n, null, r, t), n.child = t; t; ) t.flags = t.flags & -3 | 4096, t = t.sibling;
        else {
          if (bn(), r === l) {
            n = Ye(e, n, t);
            break e;
          }
          oe(e, n, r, t);
        }
        n = n.child;
      }
      return n;
    case 5:
      return ta(n), e === null && wo(n), r = n.type, l = n.pendingProps, o = e !== null ? e.memoizedProps : null, u = l.children, mo(r, l) ? u = null : o !== null && mo(r, o) && (n.flags |= 32), Na(e, n), oe(e, n, u, t), n.child;
    case 6:
      return e === null && wo(n), null;
    case 13:
      return La(e, n, t);
    case 4:
      return fu(n, n.stateNode.containerInfo), r = n.pendingProps, e === null ? n.child = et(n, null, r, t) : oe(e, n, r, t), n.child;
    case 11:
      return r = n.type, l = n.pendingProps, l = n.elementType === r ? l : ze(r, l), xi(e, n, r, l, t);
    case 7:
      return oe(e, n, n.pendingProps, t), n.child;
    case 8:
      return oe(e, n, n.pendingProps.children, t), n.child;
    case 12:
      return oe(e, n, n.pendingProps.children, t), n.child;
    case 10:
      e: {
        if (r = n.type._context, l = n.pendingProps, o = n.memoizedProps, u = l.value, D(Hr, r._currentValue), r._currentValue = u, o !== null) if (Oe(o.value, u)) {
          if (o.children === l.children && !fe.current) {
            n = Ye(e, n, t);
            break e;
          }
        } else for (o = n.child, o !== null && (o.return = n); o !== null; ) {
          var i = o.dependencies;
          if (i !== null) {
            u = o.child;
            for (var s = i.firstContext; s !== null; ) {
              if (s.context === r) {
                if (o.tag === 1) {
                  s = He(-1, t & -t), s.tag = 2;
                  var f = o.updateQueue;
                  if (f !== null) {
                    f = f.shared;
                    var h = f.pending;
                    h === null ? s.next = s : (s.next = h.next, h.next = s), f.pending = s;
                  }
                }
                o.lanes |= t, s = o.alternate, s !== null && (s.lanes |= t), So(
                  o.return,
                  t,
                  n
                ), i.lanes |= t;
                break;
              }
              s = s.next;
            }
          } else if (o.tag === 10) u = o.type === n.type ? null : o.child;
          else if (o.tag === 18) {
            if (u = o.return, u === null) throw Error(g(341));
            u.lanes |= t, i = u.alternate, i !== null && (i.lanes |= t), So(u, t, n), u = o.sibling;
          } else u = o.child;
          if (u !== null) u.return = o;
          else for (u = o; u !== null; ) {
            if (u === n) {
              u = null;
              break;
            }
            if (o = u.sibling, o !== null) {
              o.return = u.return, u = o;
              break;
            }
            u = u.return;
          }
          o = u;
        }
        oe(e, n, l.children, t), n = n.child;
      }
      return n;
    case 9:
      return l = n.type, r = n.pendingProps.children, Gn(n, t), l = _e(l), r = r(l), n.flags |= 1, oe(e, n, r, t), n.child;
    case 14:
      return r = n.type, l = ze(r, n.pendingProps), l = ze(r.type, l), Pi(e, n, r, l, t);
    case 15:
      return xa(e, n, n.type, n.pendingProps, t);
    case 17:
      return r = n.type, l = n.pendingProps, l = n.elementType === r ? l : ze(r, l), Pr(e, n), n.tag = 1, de(r) ? (e = !0, Ar(n)) : e = !1, Gn(n, t), Ea(n, r, l), Eo(n, r, l, t), xo(null, n, r, !0, e, t);
    case 19:
      return Ta(e, n, t);
    case 22:
      return Pa(e, n, t);
  }
  throw Error(g(156, n.tag));
};
function Ka(e, n) {
  return ws(e, n);
}
function dd(e, n, t, r) {
  this.tag = e, this.key = t, this.sibling = this.child = this.return = this.stateNode = this.type = this.elementType = null, this.index = 0, this.ref = null, this.pendingProps = n, this.dependencies = this.memoizedState = this.updateQueue = this.memoizedProps = null, this.mode = r, this.subtreeFlags = this.flags = 0, this.deletions = null, this.childLanes = this.lanes = 0, this.alternate = null;
}
function Ee(e, n, t, r) {
  return new dd(e, n, t, r);
}
function Pu(e) {
  return e = e.prototype, !(!e || !e.isReactComponent);
}
function pd(e) {
  if (typeof e == "function") return Pu(e) ? 1 : 0;
  if (e != null) {
    if (e = e.$$typeof, e === Wo) return 11;
    if (e === Ko) return 14;
  }
  return 2;
}
function cn(e, n) {
  var t = e.alternate;
  return t === null ? (t = Ee(e.tag, n, e.key, e.mode), t.elementType = e.elementType, t.type = e.type, t.stateNode = e.stateNode, t.alternate = e, e.alternate = t) : (t.pendingProps = n, t.type = e.type, t.flags = 0, t.subtreeFlags = 0, t.deletions = null), t.flags = e.flags & 14680064, t.childLanes = e.childLanes, t.lanes = e.lanes, t.child = e.child, t.memoizedProps = e.memoizedProps, t.memoizedState = e.memoizedState, t.updateQueue = e.updateQueue, n = e.dependencies, t.dependencies = n === null ? null : { lanes: n.lanes, firstContext: n.firstContext }, t.sibling = e.sibling, t.index = e.index, t.ref = e.ref, t;
}
function Lr(e, n, t, r, l, o) {
  var u = 2;
  if (r = e, typeof e == "function") Pu(e) && (u = 1);
  else if (typeof e == "string") u = 5;
  else e: switch (e) {
    case Dn:
      return _n(t.children, l, o, n);
    case Qo:
      u = 8, l |= 8;
      break;
    case Wl:
      return e = Ee(12, t, n, l | 2), e.elementType = Wl, e.lanes = o, e;
    case Kl:
      return e = Ee(13, t, n, l), e.elementType = Kl, e.lanes = o, e;
    case Yl:
      return e = Ee(19, t, n, l), e.elementType = Yl, e.lanes = o, e;
    case ts:
      return cl(t, l, o, n);
    default:
      if (typeof e == "object" && e !== null) switch (e.$$typeof) {
        case es:
          u = 10;
          break e;
        case ns:
          u = 9;
          break e;
        case Wo:
          u = 11;
          break e;
        case Ko:
          u = 14;
          break e;
        case Ze:
          u = 16, r = null;
          break e;
      }
      throw Error(g(130, e == null ? e : typeof e, ""));
  }
  return n = Ee(u, t, n, l), n.elementType = e, n.type = r, n.lanes = o, n;
}
function _n(e, n, t, r) {
  return e = Ee(7, e, r, n), e.lanes = t, e;
}
function cl(e, n, t, r) {
  return e = Ee(22, e, r, n), e.elementType = ts, e.lanes = t, e.stateNode = { isHidden: !1 }, e;
}
function Bl(e, n, t) {
  return e = Ee(6, e, null, n), e.lanes = t, e;
}
function Hl(e, n, t) {
  return n = Ee(4, e.children !== null ? e.children : [], e.key, n), n.lanes = t, n.stateNode = { containerInfo: e.containerInfo, pendingChildren: null, implementation: e.implementation }, n;
}
function md(e, n, t, r, l) {
  this.tag = n, this.containerInfo = e, this.finishedWork = this.pingCache = this.current = this.pendingChildren = null, this.timeoutHandle = -1, this.callbackNode = this.pendingContext = this.context = null, this.callbackPriority = 0, this.eventTimes = Cl(0), this.expirationTimes = Cl(-1), this.entangledLanes = this.finishedLanes = this.mutableReadLanes = this.expiredLanes = this.pingedLanes = this.suspendedLanes = this.pendingLanes = 0, this.entanglements = Cl(0), this.identifierPrefix = r, this.onRecoverableError = l, this.mutableSourceEagerHydrationData = null;
}
function Nu(e, n, t, r, l, o, u, i, s) {
  return e = new md(e, n, t, i, s), n === 1 ? (n = 1, o === !0 && (n |= 8)) : n = 0, o = Ee(3, null, null, n), e.current = o, o.stateNode = e, o.memoizedState = { element: r, isDehydrated: t, cache: null, transitions: null, pendingSuspenseBoundaries: null }, cu(o), e;
}
function hd(e, n, t) {
  var r = 3 < arguments.length && arguments[3] !== void 0 ? arguments[3] : null;
  return { $$typeof: On, key: r == null ? null : "" + r, children: e, containerInfo: n, implementation: t };
}
function Ya(e) {
  if (!e) return dn;
  e = e._reactInternals;
  e: {
    if (Rn(e) !== e || e.tag !== 1) throw Error(g(170));
    var n = e;
    do {
      switch (n.tag) {
        case 3:
          n = n.stateNode.context;
          break e;
        case 1:
          if (de(n.type)) {
            n = n.stateNode.__reactInternalMemoizedMergedChildContext;
            break e;
          }
      }
      n = n.return;
    } while (n !== null);
    throw Error(g(171));
  }
  if (e.tag === 1) {
    var t = e.type;
    if (de(t)) return Ys(e, t, n);
  }
  return n;
}
function Xa(e, n, t, r, l, o, u, i, s) {
  return e = Nu(t, r, !0, e, l, o, u, i, s), e.context = Ya(null), t = e.current, r = ue(), l = an(t), o = He(r, l), o.callback = n ?? null, un(t, o, l), e.current.lanes = l, Xt(e, l, r), pe(e, r), e;
}
function fl(e, n, t, r) {
  var l = n.current, o = ue(), u = an(l);
  return t = Ya(t), n.context === null ? n.context = t : n.pendingContext = t, n = He(o, u), n.payload = { element: e }, r = r === void 0 ? null : r, r !== null && (n.callback = r), e = un(l, n, u), e !== null && (Me(e, l, u, o), Cr(e, l, u)), u;
}
function br(e) {
  if (e = e.current, !e.child) return null;
  switch (e.child.tag) {
    case 5:
      return e.child.stateNode;
    default:
      return e.child.stateNode;
  }
}
function ji(e, n) {
  if (e = e.memoizedState, e !== null && e.dehydrated !== null) {
    var t = e.retryLane;
    e.retryLane = t !== 0 && t < n ? t : n;
  }
}
function zu(e, n) {
  ji(e, n), (e = e.alternate) && ji(e, n);
}
function vd() {
  return null;
}
var Ga = typeof reportError == "function" ? reportError : function(e) {
  console.error(e);
};
function Lu(e) {
  this._internalRoot = e;
}
dl.prototype.render = Lu.prototype.render = function(e) {
  var n = this._internalRoot;
  if (n === null) throw Error(g(409));
  fl(e, n, null, null);
};
dl.prototype.unmount = Lu.prototype.unmount = function() {
  var e = this._internalRoot;
  if (e !== null) {
    this._internalRoot = null;
    var n = e.containerInfo;
    Ln(function() {
      fl(null, e, null, null);
    }), n[We] = null;
  }
};
function dl(e) {
  this._internalRoot = e;
}
dl.prototype.unstable_scheduleHydration = function(e) {
  if (e) {
    var n = Ps();
    e = { blockedOn: null, target: e, priority: n };
    for (var t = 0; t < qe.length && n !== 0 && n < qe[t].priority; t++) ;
    qe.splice(t, 0, e), t === 0 && zs(e);
  }
};
function Tu(e) {
  return !(!e || e.nodeType !== 1 && e.nodeType !== 9 && e.nodeType !== 11);
}
function pl(e) {
  return !(!e || e.nodeType !== 1 && e.nodeType !== 9 && e.nodeType !== 11 && (e.nodeType !== 8 || e.nodeValue !== " react-mount-point-unstable "));
}
function $i() {
}
function yd(e, n, t, r, l) {
  if (l) {
    if (typeof r == "function") {
      var o = r;
      r = function() {
        var f = br(u);
        o.call(f);
      };
    }
    var u = Xa(n, r, e, 0, null, !1, !1, "", $i);
    return e._reactRootContainer = u, e[We] = u.current, jt(e.nodeType === 8 ? e.parentNode : e), Ln(), u;
  }
  for (; l = e.lastChild; ) e.removeChild(l);
  if (typeof r == "function") {
    var i = r;
    r = function() {
      var f = br(s);
      i.call(f);
    };
  }
  var s = Nu(e, 0, !1, null, null, !1, !1, "", $i);
  return e._reactRootContainer = s, e[We] = s.current, jt(e.nodeType === 8 ? e.parentNode : e), Ln(function() {
    fl(n, s, t, r);
  }), s;
}
function ml(e, n, t, r, l) {
  var o = t._reactRootContainer;
  if (o) {
    var u = o;
    if (typeof l == "function") {
      var i = l;
      l = function() {
        var s = br(u);
        i.call(s);
      };
    }
    fl(n, u, e, l);
  } else u = yd(t, n, e, l, r);
  return br(u);
}
_s = function(e) {
  switch (e.tag) {
    case 3:
      var n = e.stateNode;
      if (n.current.memoizedState.isDehydrated) {
        var t = wt(n.pendingLanes);
        t !== 0 && (Go(n, t | 1), pe(n, Q()), !(M & 6) && (rt = Q() + 500, hn()));
      }
      break;
    case 13:
      Ln(function() {
        var r = Ke(e, 1);
        if (r !== null) {
          var l = ue();
          Me(r, e, 1, l);
        }
      }), zu(e, 1);
  }
};
Zo = function(e) {
  if (e.tag === 13) {
    var n = Ke(e, 134217728);
    if (n !== null) {
      var t = ue();
      Me(n, e, 134217728, t);
    }
    zu(e, 134217728);
  }
};
xs = function(e) {
  if (e.tag === 13) {
    var n = an(e), t = Ke(e, n);
    if (t !== null) {
      var r = ue();
      Me(t, e, n, r);
    }
    zu(e, n);
  }
};
Ps = function() {
  return O;
};
Ns = function(e, n) {
  var t = O;
  try {
    return O = e, n();
  } finally {
    O = t;
  }
};
ro = function(e, n, t) {
  switch (n) {
    case "input":
      if (Zl(e, t), n = t.name, t.type === "radio" && n != null) {
        for (t = e; t.parentNode; ) t = t.parentNode;
        for (t = t.querySelectorAll("input[name=" + JSON.stringify("" + n) + '][type="radio"]'), n = 0; n < t.length; n++) {
          var r = t[n];
          if (r !== e && r.form === e.form) {
            var l = ll(r);
            if (!l) throw Error(g(90));
            ls(r), Zl(r, l);
          }
        }
      }
      break;
    case "textarea":
      us(e, t);
      break;
    case "select":
      n = t.value, n != null && Wn(e, !!t.multiple, n, !1);
  }
};
ps = Cu;
ms = Ln;
var gd = { usingClientEntryPoint: !1, Events: [Zt, jn, ll, fs, ds, Cu] }, vt = { findFiberByHostInstance: Sn, bundleType: 0, version: "18.3.1", rendererPackageName: "react-dom" }, wd = { bundleType: vt.bundleType, version: vt.version, rendererPackageName: vt.rendererPackageName, rendererConfig: vt.rendererConfig, overrideHookState: null, overrideHookStateDeletePath: null, overrideHookStateRenamePath: null, overrideProps: null, overridePropsDeletePath: null, overridePropsRenamePath: null, setErrorHandler: null, setSuspenseHandler: null, scheduleUpdate: null, currentDispatcherRef: Xe.ReactCurrentDispatcher, findHostInstanceByFiber: function(e) {
  return e = ys(e), e === null ? null : e.stateNode;
}, findFiberByHostInstance: vt.findFiberByHostInstance || vd, findHostInstancesForRefresh: null, scheduleRefresh: null, scheduleRoot: null, setRefreshHandler: null, getCurrentFiber: null, reconcilerVersion: "18.3.1-next-f1338f8080-20240426" };
if (typeof __REACT_DEVTOOLS_GLOBAL_HOOK__ < "u") {
  var vr = __REACT_DEVTOOLS_GLOBAL_HOOK__;
  if (!vr.isDisabled && vr.supportsFiber) try {
    el = vr.inject(wd), Ue = vr;
  } catch {
  }
}
ge.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED = gd;
ge.createPortal = function(e, n) {
  var t = 2 < arguments.length && arguments[2] !== void 0 ? arguments[2] : null;
  if (!Tu(n)) throw Error(g(200));
  return hd(e, n, null, t);
};
ge.createRoot = function(e, n) {
  if (!Tu(e)) throw Error(g(299));
  var t = !1, r = "", l = Ga;
  return n != null && (n.unstable_strictMode === !0 && (t = !0), n.identifierPrefix !== void 0 && (r = n.identifierPrefix), n.onRecoverableError !== void 0 && (l = n.onRecoverableError)), n = Nu(e, 1, !1, null, null, t, !1, r, l), e[We] = n.current, jt(e.nodeType === 8 ? e.parentNode : e), new Lu(n);
};
ge.findDOMNode = function(e) {
  if (e == null) return null;
  if (e.nodeType === 1) return e;
  var n = e._reactInternals;
  if (n === void 0)
    throw typeof e.render == "function" ? Error(g(188)) : (e = Object.keys(e).join(","), Error(g(268, e)));
  return e = ys(n), e = e === null ? null : e.stateNode, e;
};
ge.flushSync = function(e) {
  return Ln(e);
};
ge.hydrate = function(e, n, t) {
  if (!pl(n)) throw Error(g(200));
  return ml(null, e, n, !0, t);
};
ge.hydrateRoot = function(e, n, t) {
  if (!Tu(e)) throw Error(g(405));
  var r = t != null && t.hydratedSources || null, l = !1, o = "", u = Ga;
  if (t != null && (t.unstable_strictMode === !0 && (l = !0), t.identifierPrefix !== void 0 && (o = t.identifierPrefix), t.onRecoverableError !== void 0 && (u = t.onRecoverableError)), n = Xa(n, null, e, 1, t ?? null, l, !1, o, u), e[We] = n.current, jt(e), r) for (e = 0; e < r.length; e++) t = r[e], l = t._getVersion, l = l(t._source), n.mutableSourceEagerHydrationData == null ? n.mutableSourceEagerHydrationData = [t, l] : n.mutableSourceEagerHydrationData.push(
    t,
    l
  );
  return new dl(n);
};
ge.render = function(e, n, t) {
  if (!pl(n)) throw Error(g(200));
  return ml(null, e, n, !1, t);
};
ge.unmountComponentAtNode = function(e) {
  if (!pl(e)) throw Error(g(40));
  return e._reactRootContainer ? (Ln(function() {
    ml(null, null, e, !1, function() {
      e._reactRootContainer = null, e[We] = null;
    });
  }), !0) : !1;
};
ge.unstable_batchedUpdates = Cu;
ge.unstable_renderSubtreeIntoContainer = function(e, n, t, r) {
  if (!pl(t)) throw Error(g(200));
  if (e == null || e._reactInternals === void 0) throw Error(g(38));
  return ml(e, n, t, !1, r);
};
ge.version = "18.3.1-next-f1338f8080-20240426";
function Za() {
  if (!(typeof __REACT_DEVTOOLS_GLOBAL_HOOK__ > "u" || typeof __REACT_DEVTOOLS_GLOBAL_HOOK__.checkDCE != "function"))
    try {
      __REACT_DEVTOOLS_GLOBAL_HOOK__.checkDCE(Za);
    } catch (e) {
      console.error(e);
    }
}
Za(), Zi.exports = ge;
var Sd = Zi.exports, Ja, Ai = Sd;
Ja = Ai.createRoot, Ai.hydrateRoot;
let qa = te.createContext(
  /** @type {any} */
  null
);
function kd() {
  let e = te.useContext(qa);
  if (!e) throw new Error("RenderContext not found");
  return e;
}
function Ed() {
  return kd().model;
}
function yr(e) {
  let n = Ed(), [t, r] = te.useState(n.get(e));
  return te.useEffect(() => {
    let l = () => r(n.get(e));
    return n.on(`change:${e}`, l), () => n.off(`change:${e}`, l);
  }, [n, e]), [
    t,
    (l) => {
      n.set(e, l), n.save_changes();
    }
  ];
}
function Cd(e) {
  return ({ el: n, model: t, experimental: r }) => {
    let l = Ja(n);
    return l.render(
      te.createElement(
        te.StrictMode,
        null,
        te.createElement(
          qa.Provider,
          { value: { model: t, experimental: r } },
          te.createElement(e)
        )
      )
    ), () => l.unmount();
  };
}
function _d() {
  const [e, n] = yr("browser_query_params"), [t, r] = yr("browser_path_segments"), [l, o] = yr("browser_current_url"), [u, i] = yr("browser_base_url"), s = te.useRef({
    queryParams: {},
    pathSegments: [],
    currentURL: "",
    baseURL: ""
  }), f = te.useCallback((v, w) => {
    if (v === w) return !0;
    if (typeof v != typeof w || typeof v != "object" || v === null || w === null || Array.isArray(v) !== Array.isArray(w)) return !1;
    if (Array.isArray(v))
      return v.length !== w.length ? !1 : v.every((a, d) => f(a, w[d]));
    const N = Object.keys(v), c = Object.keys(w);
    return N.length !== c.length ? !1 : N.every((a) => f(v[a], w[a]));
  }, []), h = te.useCallback(() => {
    try {
      const v = {}, w = new URLSearchParams(window.location.search);
      for (const [N, c] of w.entries())
        v[N] = c;
      return console.log("Parsed query params:", v), v;
    } catch (v) {
      return console.error("Error parsing query parameters:", v), {};
    }
  }, []), m = te.useCallback(() => {
    try {
      const v = window.location.pathname.replace(/^\/+|\/+$/g, ""), w = v ? v.split("/") : [];
      return console.log("Parsed path segments:", w), w;
    } catch (v) {
      return console.error("Error parsing path segments:", v), [];
    }
  }, []), p = te.useCallback((v, w, N, c) => {
    let a = !1;
    return console.log("Current state:", s.current), console.log("New params:", v), console.log("New segments:", w), console.log("New URL:", N), console.log("New base:", c), f(v, s.current.queryParams) || (console.log("Sending query params to Python:", v), s.current.queryParams = { ...v }, n(v), a = !0, console.log("Query params updated")), f(w, s.current.pathSegments) || (s.current.pathSegments = [...w], r(w), a = !0, console.log("Path segments updated")), N !== s.current.currentURL && (s.current.currentURL = N, o(N), a = !0, console.log("Current URL updated")), c !== s.current.baseURL && (s.current.baseURL = c, i(c), a = !0, console.log("Base URL updated")), console.log("Has changes:", a), a;
  }, [n, r, o, i, f]), S = te.useCallback(() => {
    console.log("Updating all URL state..."), console.log("Current location:", window.location.href);
    const v = h(), w = m(), N = window.location.href, c = `${window.location.protocol}//${window.location.host}`;
    p(v, w, N, c);
  }, [h, m, p]);
  return te.useEffect(() => {
    console.log("Setting up URL monitoring...");
    const v = history.pushState, w = history.replaceState;
    history.pushState = function(...c) {
      v.apply(history, c), window.dispatchEvent(new Event("locationchange"));
    }, history.replaceState = function(...c) {
      w.apply(history, c), window.dispatchEvent(new Event("locationchange"));
    };
    const N = () => {
      console.log("URL change detected"), S();
    };
    return N(), window.addEventListener("popstate", N), window.addEventListener("hashchange", N), window.addEventListener("locationchange", N), () => {
      window.removeEventListener("popstate", N), window.removeEventListener("hashchange", N), window.removeEventListener("locationchange", N), history.pushState = v, history.replaceState = w;
    };
  }, [S]), null;
}
const xd = {
  render: Cd(_d)
};
export {
  xd as default
};
