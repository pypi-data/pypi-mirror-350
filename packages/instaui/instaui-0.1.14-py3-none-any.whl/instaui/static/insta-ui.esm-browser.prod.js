var Wn = Object.defineProperty;
var Un = (e, t, n) => t in e ? Wn(e, t, { enumerable: !0, configurable: !0, writable: !0, value: n }) : e[t] = n;
var B = (e, t, n) => Un(e, typeof t != "symbol" ? t + "" : t, n);
import * as Kn from "vue";
import { toRaw as Gn, customRef as Ce, toValue as q, unref as W, watch as G, nextTick as Te, isRef as qt, ref as Z, shallowRef as J, watchEffect as Ht, computed as U, readonly as qn, provide as Ie, inject as ee, shallowReactive as Hn, defineComponent as F, reactive as zn, h as A, getCurrentInstance as zt, normalizeStyle as Jn, normalizeClass as Ye, toDisplayString as Jt, onUnmounted as xe, Fragment as De, vModelDynamic as Qn, vShow as Yn, resolveDynamicComponent as ft, normalizeProps as Xn, withDirectives as Zn, onErrorCaptured as er, openBlock as he, createElementBlock as Ve, createElementVNode as tr, createVNode as nr, withCtx as rr, renderList as or, createBlock as sr, TransitionGroup as Qt, KeepAlive as ir } from "vue";
let Yt;
function ar(e) {
  Yt = e;
}
function Xe() {
  return Yt;
}
function ye() {
  const { queryPath: e, pathParams: t, queryParams: n } = Xe();
  return {
    path: e,
    ...t === void 0 ? {} : { params: t },
    ...n === void 0 ? {} : { queryParams: n }
  };
}
class cr extends Map {
  constructor(t) {
    super(), this.factory = t;
  }
  getOrDefault(t) {
    if (!this.has(t)) {
      const n = this.factory();
      return this.set(t, n), n;
    }
    return super.get(t);
  }
}
function _e(e) {
  return new cr(e);
}
function Ot(e, t) {
  Object.entries(e).forEach(([n, r]) => t(r, n));
}
function Oe(e, t) {
  return Xt(e, {
    valueFn: t
  });
}
function Xt(e, t) {
  const { valueFn: n, keyFn: r } = t;
  return Object.fromEntries(
    Object.entries(e).map(([o, s], i) => [
      r ? r(o, s) : o,
      n(s, o, i)
    ])
  );
}
function Zt(e, t, n) {
  if (Array.isArray(t)) {
    const [o, ...s] = t;
    switch (o) {
      case "!":
        return !e;
      case "+":
        return e + s[0];
      case "~+":
        return s[0] + e;
    }
  }
  const r = en(t, n);
  return e[r];
}
function en(e, t) {
  if (typeof e == "string" || typeof e == "number")
    return e;
  if (!Array.isArray(e))
    throw new Error(`Invalid path ${e}`);
  const [n, ...r] = e;
  switch (n) {
    case "bind":
      if (!t)
        throw new Error("No bindable function provided");
      return t(r[0]);
    default:
      throw new Error(`Invalid flag ${n} in array at ${e}`);
  }
}
function be(e, t, n) {
  return t.reduce(
    (r, o) => Zt(r, o, n),
    e
  );
}
function Ze(e, t, n, r) {
  t.reduce((o, s, i) => {
    if (i === t.length - 1)
      o[en(s, r)] = n;
    else
      return Zt(o, s, r);
  }, e);
}
function tn(e) {
  return JSON.parse(JSON.stringify(e));
}
class ur {
  toString() {
    return "";
  }
}
const we = new ur();
function Ee(e) {
  return Gn(e) === we;
}
function bt(e, t, n) {
  const { paths: r, getBindableValueFn: o } = t, { paths: s, getBindableValueFn: i } = t;
  return r === void 0 || r.length === 0 ? e : Ce(() => ({
    get() {
      try {
        return be(
          q(e),
          r,
          o
        );
      } catch {
        return;
      }
    },
    set(c) {
      Ze(
        q(e),
        s || r,
        c,
        i
      );
    }
  }));
}
function nn(e) {
  return Ce((t, n) => ({
    get() {
      return t(), e;
    },
    set(r) {
      !Ee(e) && JSON.stringify(r) === JSON.stringify(e) || (e = r, n());
    }
  }));
}
function de(e) {
  return typeof e == "function" ? e() : W(e);
}
typeof WorkerGlobalScope < "u" && globalThis instanceof WorkerGlobalScope;
const et = () => {
};
function tt(e, t = !1, n = "Timeout") {
  return new Promise((r, o) => {
    setTimeout(t ? () => o(n) : r, e);
  });
}
function nt(e, t = !1) {
  function n(u, { flush: f = "sync", deep: d = !1, timeout: v, throwOnTimeout: p } = {}) {
    let g = null;
    const _ = [new Promise((O) => {
      g = G(
        e,
        (R) => {
          u(R) !== t && (g ? g() : Te(() => g == null ? void 0 : g()), O(R));
        },
        {
          flush: f,
          deep: d,
          immediate: !0
        }
      );
    })];
    return v != null && _.push(
      tt(v, p).then(() => de(e)).finally(() => g == null ? void 0 : g())
    ), Promise.race(_);
  }
  function r(u, f) {
    if (!qt(u))
      return n((R) => R === u, f);
    const { flush: d = "sync", deep: v = !1, timeout: p, throwOnTimeout: g } = f ?? {};
    let y = null;
    const O = [new Promise((R) => {
      y = G(
        [e, u],
        ([D, C]) => {
          t !== (D === C) && (y ? y() : Te(() => y == null ? void 0 : y()), R(D));
        },
        {
          flush: d,
          deep: v,
          immediate: !0
        }
      );
    })];
    return p != null && O.push(
      tt(p, g).then(() => de(e)).finally(() => (y == null || y(), de(e)))
    ), Promise.race(O);
  }
  function o(u) {
    return n((f) => !!f, u);
  }
  function s(u) {
    return r(null, u);
  }
  function i(u) {
    return r(void 0, u);
  }
  function c(u) {
    return n(Number.isNaN, u);
  }
  function l(u, f) {
    return n((d) => {
      const v = Array.from(d);
      return v.includes(u) || v.includes(de(u));
    }, f);
  }
  function h(u) {
    return a(1, u);
  }
  function a(u = 1, f) {
    let d = -1;
    return n(() => (d += 1, d >= u), f);
  }
  return Array.isArray(de(e)) ? {
    toMatch: n,
    toContains: l,
    changed: h,
    changedTimes: a,
    get not() {
      return nt(e, !t);
    }
  } : {
    toMatch: n,
    toBe: r,
    toBeTruthy: o,
    toBeNull: s,
    toBeNaN: c,
    toBeUndefined: i,
    changed: h,
    changedTimes: a,
    get not() {
      return nt(e, !t);
    }
  };
}
function lr(e) {
  return nt(e);
}
function fr(e, t, n) {
  let r;
  qt(n) ? r = {
    evaluating: n
  } : r = n || {};
  const {
    lazy: o = !1,
    evaluating: s = void 0,
    shallow: i = !0,
    onError: c = et
  } = r, l = Z(!o), h = i ? J(t) : Z(t);
  let a = 0;
  return Ht(async (u) => {
    if (!l.value)
      return;
    a++;
    const f = a;
    let d = !1;
    s && Promise.resolve().then(() => {
      s.value = !0;
    });
    try {
      const v = await e((p) => {
        u(() => {
          s && (s.value = !1), d || p();
        });
      });
      f === a && (h.value = v);
    } catch (v) {
      c(v);
    } finally {
      s && f === a && (s.value = !1), d = !0;
    }
  }), o ? U(() => (l.value = !0, h.value)) : h;
}
function hr(e, t, n) {
  const {
    immediate: r = !0,
    delay: o = 0,
    onError: s = et,
    onSuccess: i = et,
    resetOnExecute: c = !0,
    shallow: l = !0,
    throwError: h
  } = {}, a = l ? J(t) : Z(t), u = Z(!1), f = Z(!1), d = J(void 0);
  async function v(y = 0, ..._) {
    c && (a.value = t), d.value = void 0, u.value = !1, f.value = !0, y > 0 && await tt(y);
    const O = typeof e == "function" ? e(..._) : e;
    try {
      const R = await O;
      a.value = R, u.value = !0, i(R);
    } catch (R) {
      if (d.value = R, s(R), h)
        throw R;
    } finally {
      f.value = !1;
    }
    return a.value;
  }
  r && v(o);
  const p = {
    state: a,
    isReady: u,
    isLoading: f,
    error: d,
    execute: v
  };
  function g() {
    return new Promise((y, _) => {
      lr(f).toBe(!1).then(() => y(p)).catch(_);
    });
  }
  return {
    ...p,
    then(y, _) {
      return g().then(y, _);
    }
  };
}
function L(e, t) {
  t = t || {};
  const n = [...Object.keys(t), "__Vue"], r = [...Object.values(t), Kn];
  try {
    return new Function(...n, `return (${e})`)(...r);
  } catch (o) {
    throw new Error(o + " in function code: " + e);
  }
}
function dr(e) {
  if (e.startsWith(":")) {
    e = e.slice(1);
    try {
      return L(e);
    } catch (t) {
      throw new Error(t + " in function code: " + e);
    }
  }
}
function rn(e) {
  return e.constructor.name === "AsyncFunction";
}
function pr(e, t) {
  return Z(e.value);
}
function mr(e, t, n) {
  const { bind: r = {}, code: o, const: s = [] } = e, i = Object.values(r).map((a, u) => s[u] === 1 ? a : t.getVueRefObjectOrValue(a));
  if (rn(new Function(o)))
    return fr(
      async () => {
        const a = Object.fromEntries(
          Object.keys(r).map((u, f) => [u, i[f]])
        );
        return await L(o, a)();
      },
      null,
      { lazy: !0 }
    );
  const c = Object.fromEntries(
    Object.keys(r).map((a, u) => [a, i[u]])
  ), l = L(o, c);
  return U(l);
}
function gr(e, t, n) {
  const {
    inputs: r = [],
    code: o,
    slient: s,
    data: i,
    asyncInit: c = null,
    deepEqOnInput: l = 0
  } = e, h = s || Array(r.length).fill(0), a = i || Array(r.length).fill(0), u = r.filter((g, y) => h[y] === 0 && a[y] === 0).map((g) => t.getVueRefObject(g));
  function f() {
    return r.map(
      (g, y) => a[y] === 1 ? g : t.getObjectToValue(g)
    );
  }
  const d = L(o), v = l === 0 ? J(we) : nn(we), p = { immediate: !0, deep: !0 };
  return rn(d) ? (v.value = c, G(
    u,
    async () => {
      f().some(Ee) || (v.value = await d(...f()));
    },
    p
  )) : G(
    u,
    () => {
      const g = f();
      g.some(Ee) || (v.value = d(...g));
    },
    p
  ), qn(v);
}
function vr() {
  return [];
}
const Se = _e(vr);
function on(e, t) {
  var s, i, c, l, h;
  const n = Se.getOrDefault(e.id), r = /* @__PURE__ */ new Map();
  n.push(r), t.replaceSnapshot({
    scopeSnapshot: sn()
  });
  const o = (a, u) => {
    r.set(a.id, u);
  };
  return (s = e.refs) == null || s.forEach((a) => {
    o(a, pr(a));
  }), (i = e.web_computed) == null || i.forEach((a) => {
    const { init: u } = a, f = a.deepEqOnInput === void 0 ? J(u ?? we) : nn(u ?? we);
    o(a, f);
  }), (c = e.vue_computed) == null || c.forEach((a) => {
    o(
      a,
      mr(a, t)
    );
  }), (l = e.js_computed) == null || l.forEach((a) => {
    o(
      a,
      gr(a, t)
    );
  }), (h = e.data) == null || h.forEach((a) => {
    o(a, a.value);
  }), n.length - 1;
}
function sn() {
  const e = /* @__PURE__ */ new Map();
  for (const [n, r] of Se) {
    const o = r[r.length - 1];
    e.set(n, [o]);
  }
  function t(n) {
    return an(n, e);
  }
  return {
    getVueRef: t
  };
}
function yr(e) {
  return an(e, Se);
}
function an(e, t) {
  const n = t.get(e.sid);
  if (!n)
    throw new Error(`Scope ${e.sid} not found`);
  const o = n[n.length - 1].get(e.id);
  if (!o)
    throw new Error(`Var ${e.id} not found in scope ${e.sid}`);
  return o;
}
function wr(e) {
  Se.delete(e);
}
function cn(e, t) {
  const n = Se.get(e);
  n && n.splice(t, 1);
}
const ht = _e(() => []);
function Er(e) {
  var r;
  const t = /* @__PURE__ */ new Map(), n = ht.getOrDefault(e.id).push(t);
  return (r = e.eRefs) == null || r.forEach((o) => {
    const s = J();
    t.set(o.id, s);
  }), n;
}
function _r(e, t) {
  const n = ht.get(e);
  n && n.splice(t, 1);
}
function un() {
  const e = new Map(
    Array.from(ht.entries()).map(([n, r]) => [
      n,
      r[r.length - 1]
    ])
  );
  function t(n) {
    return e.get(n.sid).get(n.id);
  }
  return {
    getRef: t
  };
}
var N;
((e) => {
  function t(f) {
    return f.type === "var";
  }
  e.isVar = t;
  function n(f) {
    return f.type === "routePar";
  }
  e.isRouterParams = n;
  function r(f) {
    return f.type === "routeAct";
  }
  e.isRouterAction = r;
  function o(f) {
    return f.type === "js";
  }
  e.isJs = o;
  function s(f) {
    return f.type === "jsOutput";
  }
  e.isJsOutput = s;
  function i(f) {
    return f.type === "vf";
  }
  e.isVForItem = i;
  function c(f) {
    return f.type === "vf-i";
  }
  e.isVForIndex = c;
  function l(f) {
    return f.type === "sp";
  }
  e.isSlotProp = l;
  function h(f) {
    return f.type === "event";
  }
  e.isEventContext = h;
  function a(f) {
    return f.type === "ele_ref";
  }
  e.isElementRef = a;
  function u(f) {
    return f.type !== void 0;
  }
  e.IsBinding = u;
})(N || (N = {}));
const Me = _e(() => []);
function Or(e) {
  const t = Me.getOrDefault(e);
  return t.push(J({})), t.length - 1;
}
function br(e, t, n) {
  Me.get(e)[t].value = n;
}
function Sr(e) {
  Me.delete(e);
}
function Rr() {
  const e = /* @__PURE__ */ new Map();
  for (const [n, r] of Me) {
    const o = r[r.length - 1];
    e.set(n, o);
  }
  function t(n) {
    return e.get(n.id).value[n.name];
  }
  return {
    getPropsValue: t
  };
}
const ln = /* @__PURE__ */ new Map(), dt = _e(() => /* @__PURE__ */ new Map()), fn = /* @__PURE__ */ new Set(), hn = Symbol("vfor");
function Pr(e) {
  const t = dn() ?? {};
  Ie(hn, { ...t, [e.fid]: e.key });
}
function dn() {
  return ee(hn, void 0);
}
function kr() {
  const e = dn(), t = /* @__PURE__ */ new Map();
  return e === void 0 || Object.keys(e).forEach((n) => {
    t.set(n, e[n]);
  }), t;
}
function Vr(e, t, n, r) {
  if (r) {
    fn.add(e);
    return;
  }
  let o;
  if (n)
    o = new Cr(t);
  else {
    const s = Array.isArray(t) ? t : Object.entries(t).map(([i, c], l) => [c, i, l]);
    o = new jr(s);
  }
  ln.set(e, o);
}
function Nr(e, t, n) {
  const r = dt.getOrDefault(e);
  r.has(t) || r.set(t, Z(n)), r.get(t).value = n;
}
function Ir(e) {
  const t = /* @__PURE__ */ new Set();
  function n(o) {
    t.add(o);
  }
  function r() {
    const o = dt.get(e);
    o !== void 0 && o.forEach((s, i) => {
      t.has(i) || o.delete(i);
    });
  }
  return {
    add: n,
    removeUnusedKeys: r
  };
}
function Tr(e) {
  const t = e, n = kr();
  function r(o) {
    const s = n.get(o) ?? t;
    return dt.get(o).get(s).value;
  }
  return {
    getVForIndex: r
  };
}
function Ar(e) {
  return ln.get(e.binding.fid).createRefObjectWithPaths(e);
}
function $r(e) {
  return fn.has(e);
}
class jr {
  constructor(t) {
    this.array = t;
  }
  createRefObjectWithPaths(t) {
    const { binding: n } = t, { snapshot: r } = t, { path: o = [] } = n, s = [...o], i = r.getVForIndex(n.fid);
    return s.unshift(i), Ce(() => ({
      get: () => be(
        this.array,
        s,
        r.getObjectToValue
      ),
      set: () => {
        throw new Error("Cannot set value to a constant array");
      }
    }));
  }
}
class Cr {
  constructor(t) {
    B(this, "_isDictSource");
    this.binding = t;
  }
  isDictSource(t) {
    if (this._isDictSource === void 0) {
      const n = q(t);
      this._isDictSource = n !== null && !Array.isArray(n);
    }
    return this._isDictSource;
  }
  createRefObjectWithPaths(t) {
    const { binding: n } = t, { path: r = [] } = n, o = [...r], { snapshot: s } = t, i = s.getVueRefObject(this.binding), c = this.isDictSource(i), l = s.getVForIndex(n.fid), h = c && o.length === 0 ? [0] : [];
    return o.unshift(l, ...h), Ce(() => ({
      get: () => {
        const a = q(i), u = c ? Object.entries(a).map(([f, d], v) => [
          d,
          f,
          v
        ]) : a;
        try {
          return be(
            q(u),
            o,
            s.getObjectToValue
          );
        } catch {
          return;
        }
      },
      set: (a) => {
        const u = q(i);
        if (c) {
          const f = Object.keys(u);
          if (l >= f.length)
            throw new Error("Cannot set value to a non-existent key");
          const d = f[l];
          Ze(
            u,
            [d],
            a,
            s.getObjectToValue
          );
          return;
        }
        Ze(
          u,
          o,
          a,
          s.getObjectToValue
        );
      }
    }));
  }
}
function xr(e, t, n = !1) {
  return n && (e = `$computed(${e})`, t = { ...t, $computed: U }), L(e, t);
}
function St(e) {
  return e == null;
}
function Dr() {
  return pn().__VUE_DEVTOOLS_GLOBAL_HOOK__;
}
function pn() {
  return typeof navigator < "u" && typeof window < "u" ? window : typeof globalThis < "u" ? globalThis : {};
}
const Mr = typeof Proxy == "function", Fr = "devtools-plugin:setup", Br = "plugin:settings:set";
let ie, rt;
function Lr() {
  var e;
  return ie !== void 0 || (typeof window < "u" && window.performance ? (ie = !0, rt = window.performance) : typeof globalThis < "u" && (!((e = globalThis.perf_hooks) === null || e === void 0) && e.performance) ? (ie = !0, rt = globalThis.perf_hooks.performance) : ie = !1), ie;
}
function Wr() {
  return Lr() ? rt.now() : Date.now();
}
class Ur {
  constructor(t, n) {
    this.target = null, this.targetQueue = [], this.onQueue = [], this.plugin = t, this.hook = n;
    const r = {};
    if (t.settings)
      for (const i in t.settings) {
        const c = t.settings[i];
        r[i] = c.defaultValue;
      }
    const o = `__vue-devtools-plugin-settings__${t.id}`;
    let s = Object.assign({}, r);
    try {
      const i = localStorage.getItem(o), c = JSON.parse(i);
      Object.assign(s, c);
    } catch {
    }
    this.fallbacks = {
      getSettings() {
        return s;
      },
      setSettings(i) {
        try {
          localStorage.setItem(o, JSON.stringify(i));
        } catch {
        }
        s = i;
      },
      now() {
        return Wr();
      }
    }, n && n.on(Br, (i, c) => {
      i === this.plugin.id && this.fallbacks.setSettings(c);
    }), this.proxiedOn = new Proxy({}, {
      get: (i, c) => this.target ? this.target.on[c] : (...l) => {
        this.onQueue.push({
          method: c,
          args: l
        });
      }
    }), this.proxiedTarget = new Proxy({}, {
      get: (i, c) => this.target ? this.target[c] : c === "on" ? this.proxiedOn : Object.keys(this.fallbacks).includes(c) ? (...l) => (this.targetQueue.push({
        method: c,
        args: l,
        resolve: () => {
        }
      }), this.fallbacks[c](...l)) : (...l) => new Promise((h) => {
        this.targetQueue.push({
          method: c,
          args: l,
          resolve: h
        });
      })
    });
  }
  async setRealTarget(t) {
    this.target = t;
    for (const n of this.onQueue)
      this.target.on[n.method](...n.args);
    for (const n of this.targetQueue)
      n.resolve(await this.target[n.method](...n.args));
  }
}
function Kr(e, t) {
  const n = e, r = pn(), o = Dr(), s = Mr && n.enableEarlyProxy;
  if (o && (r.__VUE_DEVTOOLS_PLUGIN_API_AVAILABLE__ || !s))
    o.emit(Fr, e, t);
  else {
    const i = s ? new Ur(n, o) : null;
    (r.__VUE_DEVTOOLS_PLUGINS__ = r.__VUE_DEVTOOLS_PLUGINS__ || []).push({
      pluginDescriptor: n,
      setupFn: t,
      proxy: i
    }), i && t(i.proxiedTarget);
  }
}
var S = {};
const z = typeof document < "u";
function mn(e) {
  return typeof e == "object" || "displayName" in e || "props" in e || "__vccOpts" in e;
}
function Gr(e) {
  return e.__esModule || e[Symbol.toStringTag] === "Module" || // support CF with dynamic imports that do not
  // add the Module string tag
  e.default && mn(e.default);
}
const I = Object.assign;
function He(e, t) {
  const n = {};
  for (const r in t) {
    const o = t[r];
    n[r] = K(o) ? o.map(e) : e(o);
  }
  return n;
}
const ve = () => {
}, K = Array.isArray;
function P(e) {
  const t = Array.from(arguments).slice(1);
  console.warn.apply(console, ["[Vue Router warn]: " + e].concat(t));
}
const gn = /#/g, qr = /&/g, Hr = /\//g, zr = /=/g, Jr = /\?/g, vn = /\+/g, Qr = /%5B/g, Yr = /%5D/g, yn = /%5E/g, Xr = /%60/g, wn = /%7B/g, Zr = /%7C/g, En = /%7D/g, eo = /%20/g;
function pt(e) {
  return encodeURI("" + e).replace(Zr, "|").replace(Qr, "[").replace(Yr, "]");
}
function to(e) {
  return pt(e).replace(wn, "{").replace(En, "}").replace(yn, "^");
}
function ot(e) {
  return pt(e).replace(vn, "%2B").replace(eo, "+").replace(gn, "%23").replace(qr, "%26").replace(Xr, "`").replace(wn, "{").replace(En, "}").replace(yn, "^");
}
function no(e) {
  return ot(e).replace(zr, "%3D");
}
function ro(e) {
  return pt(e).replace(gn, "%23").replace(Jr, "%3F");
}
function oo(e) {
  return e == null ? "" : ro(e).replace(Hr, "%2F");
}
function ae(e) {
  try {
    return decodeURIComponent("" + e);
  } catch {
    S.NODE_ENV !== "production" && P(`Error decoding "${e}". Using original value`);
  }
  return "" + e;
}
const so = /\/$/, io = (e) => e.replace(so, "");
function ze(e, t, n = "/") {
  let r, o = {}, s = "", i = "";
  const c = t.indexOf("#");
  let l = t.indexOf("?");
  return c < l && c >= 0 && (l = -1), l > -1 && (r = t.slice(0, l), s = t.slice(l + 1, c > -1 ? c : t.length), o = e(s)), c > -1 && (r = r || t.slice(0, c), i = t.slice(c, t.length)), r = uo(r ?? t, n), {
    fullPath: r + (s && "?") + s + i,
    path: r,
    query: o,
    hash: ae(i)
  };
}
function ao(e, t) {
  const n = t.query ? e(t.query) : "";
  return t.path + (n && "?") + n + (t.hash || "");
}
function Rt(e, t) {
  return !t || !e.toLowerCase().startsWith(t.toLowerCase()) ? e : e.slice(t.length) || "/";
}
function Pt(e, t, n) {
  const r = t.matched.length - 1, o = n.matched.length - 1;
  return r > -1 && r === o && te(t.matched[r], n.matched[o]) && _n(t.params, n.params) && e(t.query) === e(n.query) && t.hash === n.hash;
}
function te(e, t) {
  return (e.aliasOf || e) === (t.aliasOf || t);
}
function _n(e, t) {
  if (Object.keys(e).length !== Object.keys(t).length)
    return !1;
  for (const n in e)
    if (!co(e[n], t[n]))
      return !1;
  return !0;
}
function co(e, t) {
  return K(e) ? kt(e, t) : K(t) ? kt(t, e) : e === t;
}
function kt(e, t) {
  return K(t) ? e.length === t.length && e.every((n, r) => n === t[r]) : e.length === 1 && e[0] === t;
}
function uo(e, t) {
  if (e.startsWith("/"))
    return e;
  if (S.NODE_ENV !== "production" && !t.startsWith("/"))
    return P(`Cannot resolve a relative location without an absolute path. Trying to resolve "${e}" from "${t}". It should look like "/${t}".`), e;
  if (!e)
    return t;
  const n = t.split("/"), r = e.split("/"), o = r[r.length - 1];
  (o === ".." || o === ".") && r.push("");
  let s = n.length - 1, i, c;
  for (i = 0; i < r.length; i++)
    if (c = r[i], c !== ".")
      if (c === "..")
        s > 1 && s--;
      else
        break;
  return n.slice(0, s).join("/") + "/" + r.slice(i).join("/");
}
const Y = {
  path: "/",
  // TODO: could we use a symbol in the future?
  name: void 0,
  params: {},
  query: {},
  hash: "",
  fullPath: "/",
  matched: [],
  meta: {},
  redirectedFrom: void 0
};
var ce;
(function(e) {
  e.pop = "pop", e.push = "push";
})(ce || (ce = {}));
var oe;
(function(e) {
  e.back = "back", e.forward = "forward", e.unknown = "";
})(oe || (oe = {}));
const Je = "";
function On(e) {
  if (!e)
    if (z) {
      const t = document.querySelector("base");
      e = t && t.getAttribute("href") || "/", e = e.replace(/^\w+:\/\/[^\/]+/, "");
    } else
      e = "/";
  return e[0] !== "/" && e[0] !== "#" && (e = "/" + e), io(e);
}
const lo = /^[^#]+#/;
function bn(e, t) {
  return e.replace(lo, "#") + t;
}
function fo(e, t) {
  const n = document.documentElement.getBoundingClientRect(), r = e.getBoundingClientRect();
  return {
    behavior: t.behavior,
    left: r.left - n.left - (t.left || 0),
    top: r.top - n.top - (t.top || 0)
  };
}
const Fe = () => ({
  left: window.scrollX,
  top: window.scrollY
});
function ho(e) {
  let t;
  if ("el" in e) {
    const n = e.el, r = typeof n == "string" && n.startsWith("#");
    if (S.NODE_ENV !== "production" && typeof e.el == "string" && (!r || !document.getElementById(e.el.slice(1))))
      try {
        const s = document.querySelector(e.el);
        if (r && s) {
          P(`The selector "${e.el}" should be passed as "el: document.querySelector('${e.el}')" because it starts with "#".`);
          return;
        }
      } catch {
        P(`The selector "${e.el}" is invalid. If you are using an id selector, make sure to escape it. You can find more information about escaping characters in selectors at https://mathiasbynens.be/notes/css-escapes or use CSS.escape (https://developer.mozilla.org/en-US/docs/Web/API/CSS/escape).`);
        return;
      }
    const o = typeof n == "string" ? r ? document.getElementById(n.slice(1)) : document.querySelector(n) : n;
    if (!o) {
      S.NODE_ENV !== "production" && P(`Couldn't find element using selector "${e.el}" returned by scrollBehavior.`);
      return;
    }
    t = fo(o, e);
  } else
    t = e;
  "scrollBehavior" in document.documentElement.style ? window.scrollTo(t) : window.scrollTo(t.left != null ? t.left : window.scrollX, t.top != null ? t.top : window.scrollY);
}
function Vt(e, t) {
  return (history.state ? history.state.position - t : -1) + e;
}
const st = /* @__PURE__ */ new Map();
function po(e, t) {
  st.set(e, t);
}
function mo(e) {
  const t = st.get(e);
  return st.delete(e), t;
}
let go = () => location.protocol + "//" + location.host;
function Sn(e, t) {
  const { pathname: n, search: r, hash: o } = t, s = e.indexOf("#");
  if (s > -1) {
    let c = o.includes(e.slice(s)) ? e.slice(s).length : 1, l = o.slice(c);
    return l[0] !== "/" && (l = "/" + l), Rt(l, "");
  }
  return Rt(n, e) + r + o;
}
function vo(e, t, n, r) {
  let o = [], s = [], i = null;
  const c = ({ state: f }) => {
    const d = Sn(e, location), v = n.value, p = t.value;
    let g = 0;
    if (f) {
      if (n.value = d, t.value = f, i && i === v) {
        i = null;
        return;
      }
      g = p ? f.position - p.position : 0;
    } else
      r(d);
    o.forEach((y) => {
      y(n.value, v, {
        delta: g,
        type: ce.pop,
        direction: g ? g > 0 ? oe.forward : oe.back : oe.unknown
      });
    });
  };
  function l() {
    i = n.value;
  }
  function h(f) {
    o.push(f);
    const d = () => {
      const v = o.indexOf(f);
      v > -1 && o.splice(v, 1);
    };
    return s.push(d), d;
  }
  function a() {
    const { history: f } = window;
    f.state && f.replaceState(I({}, f.state, { scroll: Fe() }), "");
  }
  function u() {
    for (const f of s)
      f();
    s = [], window.removeEventListener("popstate", c), window.removeEventListener("beforeunload", a);
  }
  return window.addEventListener("popstate", c), window.addEventListener("beforeunload", a, {
    passive: !0
  }), {
    pauseListeners: l,
    listen: h,
    destroy: u
  };
}
function Nt(e, t, n, r = !1, o = !1) {
  return {
    back: e,
    current: t,
    forward: n,
    replaced: r,
    position: window.history.length,
    scroll: o ? Fe() : null
  };
}
function yo(e) {
  const { history: t, location: n } = window, r = {
    value: Sn(e, n)
  }, o = { value: t.state };
  o.value || s(r.value, {
    back: null,
    current: r.value,
    forward: null,
    // the length is off by one, we need to decrease it
    position: t.length - 1,
    replaced: !0,
    // don't add a scroll as the user may have an anchor, and we want
    // scrollBehavior to be triggered without a saved position
    scroll: null
  }, !0);
  function s(l, h, a) {
    const u = e.indexOf("#"), f = u > -1 ? (n.host && document.querySelector("base") ? e : e.slice(u)) + l : go() + e + l;
    try {
      t[a ? "replaceState" : "pushState"](h, "", f), o.value = h;
    } catch (d) {
      S.NODE_ENV !== "production" ? P("Error with push/replace State", d) : console.error(d), n[a ? "replace" : "assign"](f);
    }
  }
  function i(l, h) {
    const a = I({}, t.state, Nt(
      o.value.back,
      // keep back and forward entries but override current position
      l,
      o.value.forward,
      !0
    ), h, { position: o.value.position });
    s(l, a, !0), r.value = l;
  }
  function c(l, h) {
    const a = I(
      {},
      // use current history state to gracefully handle a wrong call to
      // history.replaceState
      // https://github.com/vuejs/router/issues/366
      o.value,
      t.state,
      {
        forward: l,
        scroll: Fe()
      }
    );
    S.NODE_ENV !== "production" && !t.state && P(`history.state seems to have been manually replaced without preserving the necessary values. Make sure to preserve existing history state if you are manually calling history.replaceState:

history.replaceState(history.state, '', url)

You can find more information at https://router.vuejs.org/guide/migration/#Usage-of-history-state`), s(a.current, a, !0);
    const u = I({}, Nt(r.value, l, null), { position: a.position + 1 }, h);
    s(l, u, !1), r.value = l;
  }
  return {
    location: r,
    state: o,
    push: c,
    replace: i
  };
}
function Rn(e) {
  e = On(e);
  const t = yo(e), n = vo(e, t.state, t.location, t.replace);
  function r(s, i = !0) {
    i || n.pauseListeners(), history.go(s);
  }
  const o = I({
    // it's overridden right after
    location: "",
    base: e,
    go: r,
    createHref: bn.bind(null, e)
  }, t, n);
  return Object.defineProperty(o, "location", {
    enumerable: !0,
    get: () => t.location.value
  }), Object.defineProperty(o, "state", {
    enumerable: !0,
    get: () => t.state.value
  }), o;
}
function wo(e = "") {
  let t = [], n = [Je], r = 0;
  e = On(e);
  function o(c) {
    r++, r !== n.length && n.splice(r), n.push(c);
  }
  function s(c, l, { direction: h, delta: a }) {
    const u = {
      direction: h,
      delta: a,
      type: ce.pop
    };
    for (const f of t)
      f(c, l, u);
  }
  const i = {
    // rewritten by Object.defineProperty
    location: Je,
    // TODO: should be kept in queue
    state: {},
    base: e,
    createHref: bn.bind(null, e),
    replace(c) {
      n.splice(r--, 1), o(c);
    },
    push(c, l) {
      o(c);
    },
    listen(c) {
      return t.push(c), () => {
        const l = t.indexOf(c);
        l > -1 && t.splice(l, 1);
      };
    },
    destroy() {
      t = [], n = [Je], r = 0;
    },
    go(c, l = !0) {
      const h = this.location, a = (
        // we are considering delta === 0 going forward, but in abstract mode
        // using 0 for the delta doesn't make sense like it does in html5 where
        // it reloads the page
        c < 0 ? oe.back : oe.forward
      );
      r = Math.max(0, Math.min(r + c, n.length - 1)), l && s(this.location, h, {
        direction: a,
        delta: c
      });
    }
  };
  return Object.defineProperty(i, "location", {
    enumerable: !0,
    get: () => n[r]
  }), i;
}
function Eo(e) {
  return e = location.host ? e || location.pathname + location.search : "", e.includes("#") || (e += "#"), S.NODE_ENV !== "production" && !e.endsWith("#/") && !e.endsWith("#") && P(`A hash base must end with a "#":
"${e}" should be "${e.replace(/#.*$/, "#")}".`), Rn(e);
}
function Ae(e) {
  return typeof e == "string" || e && typeof e == "object";
}
function Pn(e) {
  return typeof e == "string" || typeof e == "symbol";
}
const it = Symbol(S.NODE_ENV !== "production" ? "navigation failure" : "");
var It;
(function(e) {
  e[e.aborted = 4] = "aborted", e[e.cancelled = 8] = "cancelled", e[e.duplicated = 16] = "duplicated";
})(It || (It = {}));
const _o = {
  1({ location: e, currentLocation: t }) {
    return `No match for
 ${JSON.stringify(e)}${t ? `
while being at
` + JSON.stringify(t) : ""}`;
  },
  2({ from: e, to: t }) {
    return `Redirected from "${e.fullPath}" to "${bo(t)}" via a navigation guard.`;
  },
  4({ from: e, to: t }) {
    return `Navigation aborted from "${e.fullPath}" to "${t.fullPath}" via a navigation guard.`;
  },
  8({ from: e, to: t }) {
    return `Navigation cancelled from "${e.fullPath}" to "${t.fullPath}" with a new navigation.`;
  },
  16({ from: e, to: t }) {
    return `Avoided redundant navigation to current location: "${e.fullPath}".`;
  }
};
function ue(e, t) {
  return S.NODE_ENV !== "production" ? I(new Error(_o[e](t)), {
    type: e,
    [it]: !0
  }, t) : I(new Error(), {
    type: e,
    [it]: !0
  }, t);
}
function H(e, t) {
  return e instanceof Error && it in e && (t == null || !!(e.type & t));
}
const Oo = ["params", "query", "hash"];
function bo(e) {
  if (typeof e == "string")
    return e;
  if (e.path != null)
    return e.path;
  const t = {};
  for (const n of Oo)
    n in e && (t[n] = e[n]);
  return JSON.stringify(t, null, 2);
}
const Tt = "[^/]+?", So = {
  sensitive: !1,
  strict: !1,
  start: !0,
  end: !0
}, Ro = /[.+*?^${}()[\]/\\]/g;
function Po(e, t) {
  const n = I({}, So, t), r = [];
  let o = n.start ? "^" : "";
  const s = [];
  for (const h of e) {
    const a = h.length ? [] : [
      90
      /* PathScore.Root */
    ];
    n.strict && !h.length && (o += "/");
    for (let u = 0; u < h.length; u++) {
      const f = h[u];
      let d = 40 + (n.sensitive ? 0.25 : 0);
      if (f.type === 0)
        u || (o += "/"), o += f.value.replace(Ro, "\\$&"), d += 40;
      else if (f.type === 1) {
        const { value: v, repeatable: p, optional: g, regexp: y } = f;
        s.push({
          name: v,
          repeatable: p,
          optional: g
        });
        const _ = y || Tt;
        if (_ !== Tt) {
          d += 10;
          try {
            new RegExp(`(${_})`);
          } catch (R) {
            throw new Error(`Invalid custom RegExp for param "${v}" (${_}): ` + R.message);
          }
        }
        let O = p ? `((?:${_})(?:/(?:${_}))*)` : `(${_})`;
        u || (O = // avoid an optional / if there are more segments e.g. /:p?-static
        // or /:p?-:p2
        g && h.length < 2 ? `(?:/${O})` : "/" + O), g && (O += "?"), o += O, d += 20, g && (d += -8), p && (d += -20), _ === ".*" && (d += -50);
      }
      a.push(d);
    }
    r.push(a);
  }
  if (n.strict && n.end) {
    const h = r.length - 1;
    r[h][r[h].length - 1] += 0.7000000000000001;
  }
  n.strict || (o += "/?"), n.end ? o += "$" : n.strict && !o.endsWith("/") && (o += "(?:/|$)");
  const i = new RegExp(o, n.sensitive ? "" : "i");
  function c(h) {
    const a = h.match(i), u = {};
    if (!a)
      return null;
    for (let f = 1; f < a.length; f++) {
      const d = a[f] || "", v = s[f - 1];
      u[v.name] = d && v.repeatable ? d.split("/") : d;
    }
    return u;
  }
  function l(h) {
    let a = "", u = !1;
    for (const f of e) {
      (!u || !a.endsWith("/")) && (a += "/"), u = !1;
      for (const d of f)
        if (d.type === 0)
          a += d.value;
        else if (d.type === 1) {
          const { value: v, repeatable: p, optional: g } = d, y = v in h ? h[v] : "";
          if (K(y) && !p)
            throw new Error(`Provided param "${v}" is an array but it is not repeatable (* or + modifiers)`);
          const _ = K(y) ? y.join("/") : y;
          if (!_)
            if (g)
              f.length < 2 && (a.endsWith("/") ? a = a.slice(0, -1) : u = !0);
            else
              throw new Error(`Missing required param "${v}"`);
          a += _;
        }
    }
    return a || "/";
  }
  return {
    re: i,
    score: r,
    keys: s,
    parse: c,
    stringify: l
  };
}
function ko(e, t) {
  let n = 0;
  for (; n < e.length && n < t.length; ) {
    const r = t[n] - e[n];
    if (r)
      return r;
    n++;
  }
  return e.length < t.length ? e.length === 1 && e[0] === 80 ? -1 : 1 : e.length > t.length ? t.length === 1 && t[0] === 80 ? 1 : -1 : 0;
}
function kn(e, t) {
  let n = 0;
  const r = e.score, o = t.score;
  for (; n < r.length && n < o.length; ) {
    const s = ko(r[n], o[n]);
    if (s)
      return s;
    n++;
  }
  if (Math.abs(o.length - r.length) === 1) {
    if (At(r))
      return 1;
    if (At(o))
      return -1;
  }
  return o.length - r.length;
}
function At(e) {
  const t = e[e.length - 1];
  return e.length > 0 && t[t.length - 1] < 0;
}
const Vo = {
  type: 0,
  value: ""
}, No = /[a-zA-Z0-9_]/;
function Io(e) {
  if (!e)
    return [[]];
  if (e === "/")
    return [[Vo]];
  if (!e.startsWith("/"))
    throw new Error(S.NODE_ENV !== "production" ? `Route paths should start with a "/": "${e}" should be "/${e}".` : `Invalid path "${e}"`);
  function t(d) {
    throw new Error(`ERR (${n})/"${h}": ${d}`);
  }
  let n = 0, r = n;
  const o = [];
  let s;
  function i() {
    s && o.push(s), s = [];
  }
  let c = 0, l, h = "", a = "";
  function u() {
    h && (n === 0 ? s.push({
      type: 0,
      value: h
    }) : n === 1 || n === 2 || n === 3 ? (s.length > 1 && (l === "*" || l === "+") && t(`A repeatable param (${h}) must be alone in its segment. eg: '/:ids+.`), s.push({
      type: 1,
      value: h,
      regexp: a,
      repeatable: l === "*" || l === "+",
      optional: l === "*" || l === "?"
    })) : t("Invalid state to consume buffer"), h = "");
  }
  function f() {
    h += l;
  }
  for (; c < e.length; ) {
    if (l = e[c++], l === "\\" && n !== 2) {
      r = n, n = 4;
      continue;
    }
    switch (n) {
      case 0:
        l === "/" ? (h && u(), i()) : l === ":" ? (u(), n = 1) : f();
        break;
      case 4:
        f(), n = r;
        break;
      case 1:
        l === "(" ? n = 2 : No.test(l) ? f() : (u(), n = 0, l !== "*" && l !== "?" && l !== "+" && c--);
        break;
      case 2:
        l === ")" ? a[a.length - 1] == "\\" ? a = a.slice(0, -1) + l : n = 3 : a += l;
        break;
      case 3:
        u(), n = 0, l !== "*" && l !== "?" && l !== "+" && c--, a = "";
        break;
      default:
        t("Unknown state");
        break;
    }
  }
  return n === 2 && t(`Unfinished custom RegExp for param "${h}"`), u(), i(), o;
}
function To(e, t, n) {
  const r = Po(Io(e.path), n);
  if (S.NODE_ENV !== "production") {
    const s = /* @__PURE__ */ new Set();
    for (const i of r.keys)
      s.has(i.name) && P(`Found duplicated params with name "${i.name}" for path "${e.path}". Only the last one will be available on "$route.params".`), s.add(i.name);
  }
  const o = I(r, {
    record: e,
    parent: t,
    // these needs to be populated by the parent
    children: [],
    alias: []
  });
  return t && !o.record.aliasOf == !t.record.aliasOf && t.children.push(o), o;
}
function Ao(e, t) {
  const n = [], r = /* @__PURE__ */ new Map();
  t = xt({ strict: !1, end: !0, sensitive: !1 }, t);
  function o(u) {
    return r.get(u);
  }
  function s(u, f, d) {
    const v = !d, p = jt(u);
    S.NODE_ENV !== "production" && xo(p, f), p.aliasOf = d && d.record;
    const g = xt(t, u), y = [p];
    if ("alias" in u) {
      const R = typeof u.alias == "string" ? [u.alias] : u.alias;
      for (const D of R)
        y.push(
          // we need to normalize again to ensure the `mods` property
          // being non enumerable
          jt(I({}, p, {
            // this allows us to hold a copy of the `components` option
            // so that async components cache is hold on the original record
            components: d ? d.record.components : p.components,
            path: D,
            // we might be the child of an alias
            aliasOf: d ? d.record : p
            // the aliases are always of the same kind as the original since they
            // are defined on the same record
          }))
        );
    }
    let _, O;
    for (const R of y) {
      const { path: D } = R;
      if (f && D[0] !== "/") {
        const C = f.record.path, x = C[C.length - 1] === "/" ? "" : "/";
        R.path = f.record.path + (D && x + D);
      }
      if (S.NODE_ENV !== "production" && R.path === "*")
        throw new Error(`Catch all routes ("*") must now be defined using a param with a custom regexp.
See more at https://router.vuejs.org/guide/migration/#Removed-star-or-catch-all-routes.`);
      if (_ = To(R, f, g), S.NODE_ENV !== "production" && f && D[0] === "/" && Mo(_, f), d ? (d.alias.push(_), S.NODE_ENV !== "production" && Co(d, _)) : (O = O || _, O !== _ && O.alias.push(_), v && u.name && !Ct(_) && (S.NODE_ENV !== "production" && Do(u, f), i(u.name))), Vn(_) && l(_), p.children) {
        const C = p.children;
        for (let x = 0; x < C.length; x++)
          s(C[x], _, d && d.children[x]);
      }
      d = d || _;
    }
    return O ? () => {
      i(O);
    } : ve;
  }
  function i(u) {
    if (Pn(u)) {
      const f = r.get(u);
      f && (r.delete(u), n.splice(n.indexOf(f), 1), f.children.forEach(i), f.alias.forEach(i));
    } else {
      const f = n.indexOf(u);
      f > -1 && (n.splice(f, 1), u.record.name && r.delete(u.record.name), u.children.forEach(i), u.alias.forEach(i));
    }
  }
  function c() {
    return n;
  }
  function l(u) {
    const f = Fo(u, n);
    n.splice(f, 0, u), u.record.name && !Ct(u) && r.set(u.record.name, u);
  }
  function h(u, f) {
    let d, v = {}, p, g;
    if ("name" in u && u.name) {
      if (d = r.get(u.name), !d)
        throw ue(1, {
          location: u
        });
      if (S.NODE_ENV !== "production") {
        const O = Object.keys(u.params || {}).filter((R) => !d.keys.find((D) => D.name === R));
        O.length && P(`Discarded invalid param(s) "${O.join('", "')}" when navigating. See https://github.com/vuejs/router/blob/main/packages/router/CHANGELOG.md#414-2022-08-22 for more details.`);
      }
      g = d.record.name, v = I(
        // paramsFromLocation is a new object
        $t(
          f.params,
          // only keep params that exist in the resolved location
          // only keep optional params coming from a parent record
          d.keys.filter((O) => !O.optional).concat(d.parent ? d.parent.keys.filter((O) => O.optional) : []).map((O) => O.name)
        ),
        // discard any existing params in the current location that do not exist here
        // #1497 this ensures better active/exact matching
        u.params && $t(u.params, d.keys.map((O) => O.name))
      ), p = d.stringify(v);
    } else if (u.path != null)
      p = u.path, S.NODE_ENV !== "production" && !p.startsWith("/") && P(`The Matcher cannot resolve relative paths but received "${p}". Unless you directly called \`matcher.resolve("${p}")\`, this is probably a bug in vue-router. Please open an issue at https://github.com/vuejs/router/issues/new/choose.`), d = n.find((O) => O.re.test(p)), d && (v = d.parse(p), g = d.record.name);
    else {
      if (d = f.name ? r.get(f.name) : n.find((O) => O.re.test(f.path)), !d)
        throw ue(1, {
          location: u,
          currentLocation: f
        });
      g = d.record.name, v = I({}, f.params, u.params), p = d.stringify(v);
    }
    const y = [];
    let _ = d;
    for (; _; )
      y.unshift(_.record), _ = _.parent;
    return {
      name: g,
      path: p,
      params: v,
      matched: y,
      meta: jo(y)
    };
  }
  e.forEach((u) => s(u));
  function a() {
    n.length = 0, r.clear();
  }
  return {
    addRoute: s,
    resolve: h,
    removeRoute: i,
    clearRoutes: a,
    getRoutes: c,
    getRecordMatcher: o
  };
}
function $t(e, t) {
  const n = {};
  for (const r of t)
    r in e && (n[r] = e[r]);
  return n;
}
function jt(e) {
  const t = {
    path: e.path,
    redirect: e.redirect,
    name: e.name,
    meta: e.meta || {},
    aliasOf: e.aliasOf,
    beforeEnter: e.beforeEnter,
    props: $o(e),
    children: e.children || [],
    instances: {},
    leaveGuards: /* @__PURE__ */ new Set(),
    updateGuards: /* @__PURE__ */ new Set(),
    enterCallbacks: {},
    // must be declared afterwards
    // mods: {},
    components: "components" in e ? e.components || null : e.component && { default: e.component }
  };
  return Object.defineProperty(t, "mods", {
    value: {}
  }), t;
}
function $o(e) {
  const t = {}, n = e.props || !1;
  if ("component" in e)
    t.default = n;
  else
    for (const r in e.components)
      t[r] = typeof n == "object" ? n[r] : n;
  return t;
}
function Ct(e) {
  for (; e; ) {
    if (e.record.aliasOf)
      return !0;
    e = e.parent;
  }
  return !1;
}
function jo(e) {
  return e.reduce((t, n) => I(t, n.meta), {});
}
function xt(e, t) {
  const n = {};
  for (const r in e)
    n[r] = r in t ? t[r] : e[r];
  return n;
}
function at(e, t) {
  return e.name === t.name && e.optional === t.optional && e.repeatable === t.repeatable;
}
function Co(e, t) {
  for (const n of e.keys)
    if (!n.optional && !t.keys.find(at.bind(null, n)))
      return P(`Alias "${t.record.path}" and the original record: "${e.record.path}" must have the exact same param named "${n.name}"`);
  for (const n of t.keys)
    if (!n.optional && !e.keys.find(at.bind(null, n)))
      return P(`Alias "${t.record.path}" and the original record: "${e.record.path}" must have the exact same param named "${n.name}"`);
}
function xo(e, t) {
  t && t.record.name && !e.name && !e.path && P(`The route named "${String(t.record.name)}" has a child without a name and an empty path. Using that name won't render the empty path child so you probably want to move the name to the child instead. If this is intentional, add a name to the child route to remove the warning.`);
}
function Do(e, t) {
  for (let n = t; n; n = n.parent)
    if (n.record.name === e.name)
      throw new Error(`A route named "${String(e.name)}" has been added as a ${t === n ? "child" : "descendant"} of a route with the same name. Route names must be unique and a nested route cannot use the same name as an ancestor.`);
}
function Mo(e, t) {
  for (const n of t.keys)
    if (!e.keys.find(at.bind(null, n)))
      return P(`Absolute path "${e.record.path}" must have the exact same param named "${n.name}" as its parent "${t.record.path}".`);
}
function Fo(e, t) {
  let n = 0, r = t.length;
  for (; n !== r; ) {
    const s = n + r >> 1;
    kn(e, t[s]) < 0 ? r = s : n = s + 1;
  }
  const o = Bo(e);
  return o && (r = t.lastIndexOf(o, r - 1), S.NODE_ENV !== "production" && r < 0 && P(`Finding ancestor route "${o.record.path}" failed for "${e.record.path}"`)), r;
}
function Bo(e) {
  let t = e;
  for (; t = t.parent; )
    if (Vn(t) && kn(e, t) === 0)
      return t;
}
function Vn({ record: e }) {
  return !!(e.name || e.components && Object.keys(e.components).length || e.redirect);
}
function Lo(e) {
  const t = {};
  if (e === "" || e === "?")
    return t;
  const r = (e[0] === "?" ? e.slice(1) : e).split("&");
  for (let o = 0; o < r.length; ++o) {
    const s = r[o].replace(vn, " "), i = s.indexOf("="), c = ae(i < 0 ? s : s.slice(0, i)), l = i < 0 ? null : ae(s.slice(i + 1));
    if (c in t) {
      let h = t[c];
      K(h) || (h = t[c] = [h]), h.push(l);
    } else
      t[c] = l;
  }
  return t;
}
function Dt(e) {
  let t = "";
  for (let n in e) {
    const r = e[n];
    if (n = no(n), r == null) {
      r !== void 0 && (t += (t.length ? "&" : "") + n);
      continue;
    }
    (K(r) ? r.map((s) => s && ot(s)) : [r && ot(r)]).forEach((s) => {
      s !== void 0 && (t += (t.length ? "&" : "") + n, s != null && (t += "=" + s));
    });
  }
  return t;
}
function Wo(e) {
  const t = {};
  for (const n in e) {
    const r = e[n];
    r !== void 0 && (t[n] = K(r) ? r.map((o) => o == null ? null : "" + o) : r == null ? r : "" + r);
  }
  return t;
}
const Uo = Symbol(S.NODE_ENV !== "production" ? "router view location matched" : ""), Mt = Symbol(S.NODE_ENV !== "production" ? "router view depth" : ""), Be = Symbol(S.NODE_ENV !== "production" ? "router" : ""), mt = Symbol(S.NODE_ENV !== "production" ? "route location" : ""), ct = Symbol(S.NODE_ENV !== "production" ? "router view location" : "");
function pe() {
  let e = [];
  function t(r) {
    return e.push(r), () => {
      const o = e.indexOf(r);
      o > -1 && e.splice(o, 1);
    };
  }
  function n() {
    e = [];
  }
  return {
    add: t,
    list: () => e.slice(),
    reset: n
  };
}
function X(e, t, n, r, o, s = (i) => i()) {
  const i = r && // name is defined if record is because of the function overload
  (r.enterCallbacks[o] = r.enterCallbacks[o] || []);
  return () => new Promise((c, l) => {
    const h = (f) => {
      f === !1 ? l(ue(4, {
        from: n,
        to: t
      })) : f instanceof Error ? l(f) : Ae(f) ? l(ue(2, {
        from: t,
        to: f
      })) : (i && // since enterCallbackArray is truthy, both record and name also are
      r.enterCallbacks[o] === i && typeof f == "function" && i.push(f), c());
    }, a = s(() => e.call(r && r.instances[o], t, n, S.NODE_ENV !== "production" ? Ko(h, t, n) : h));
    let u = Promise.resolve(a);
    if (e.length < 3 && (u = u.then(h)), S.NODE_ENV !== "production" && e.length > 2) {
      const f = `The "next" callback was never called inside of ${e.name ? '"' + e.name + '"' : ""}:
${e.toString()}
. If you are returning a value instead of calling "next", make sure to remove the "next" parameter from your function.`;
      if (typeof a == "object" && "then" in a)
        u = u.then((d) => h._called ? d : (P(f), Promise.reject(new Error("Invalid navigation guard"))));
      else if (a !== void 0 && !h._called) {
        P(f), l(new Error("Invalid navigation guard"));
        return;
      }
    }
    u.catch((f) => l(f));
  });
}
function Ko(e, t, n) {
  let r = 0;
  return function() {
    r++ === 1 && P(`The "next" callback was called more than once in one navigation guard when going from "${n.fullPath}" to "${t.fullPath}". It should be called exactly one time in each navigation guard. This will fail in production.`), e._called = !0, r === 1 && e.apply(null, arguments);
  };
}
function Qe(e, t, n, r, o = (s) => s()) {
  const s = [];
  for (const i of e) {
    S.NODE_ENV !== "production" && !i.components && !i.children.length && P(`Record with path "${i.path}" is either missing a "component(s)" or "children" property.`);
    for (const c in i.components) {
      let l = i.components[c];
      if (S.NODE_ENV !== "production") {
        if (!l || typeof l != "object" && typeof l != "function")
          throw P(`Component "${c}" in record with path "${i.path}" is not a valid component. Received "${String(l)}".`), new Error("Invalid route component");
        if ("then" in l) {
          P(`Component "${c}" in record with path "${i.path}" is a Promise instead of a function that returns a Promise. Did you write "import('./MyPage.vue')" instead of "() => import('./MyPage.vue')" ? This will break in production if not fixed.`);
          const h = l;
          l = () => h;
        } else l.__asyncLoader && // warn only once per component
        !l.__warnedDefineAsync && (l.__warnedDefineAsync = !0, P(`Component "${c}" in record with path "${i.path}" is defined using "defineAsyncComponent()". Write "() => import('./MyPage.vue')" instead of "defineAsyncComponent(() => import('./MyPage.vue'))".`));
      }
      if (!(t !== "beforeRouteEnter" && !i.instances[c]))
        if (mn(l)) {
          const a = (l.__vccOpts || l)[t];
          a && s.push(X(a, n, r, i, c, o));
        } else {
          let h = l();
          S.NODE_ENV !== "production" && !("catch" in h) && (P(`Component "${c}" in record with path "${i.path}" is a function that does not return a Promise. If you were passing a functional component, make sure to add a "displayName" to the component. This will break in production if not fixed.`), h = Promise.resolve(h)), s.push(() => h.then((a) => {
            if (!a)
              throw new Error(`Couldn't resolve component "${c}" at "${i.path}"`);
            const u = Gr(a) ? a.default : a;
            i.mods[c] = a, i.components[c] = u;
            const d = (u.__vccOpts || u)[t];
            return d && X(d, n, r, i, c, o)();
          }));
        }
    }
  }
  return s;
}
function Ft(e) {
  const t = ee(Be), n = ee(mt);
  let r = !1, o = null;
  const s = U(() => {
    const a = W(e.to);
    return S.NODE_ENV !== "production" && (!r || a !== o) && (Ae(a) || (r ? P(`Invalid value for prop "to" in useLink()
- to:`, a, `
- previous to:`, o, `
- props:`, e) : P(`Invalid value for prop "to" in useLink()
- to:`, a, `
- props:`, e)), o = a, r = !0), t.resolve(a);
  }), i = U(() => {
    const { matched: a } = s.value, { length: u } = a, f = a[u - 1], d = n.matched;
    if (!f || !d.length)
      return -1;
    const v = d.findIndex(te.bind(null, f));
    if (v > -1)
      return v;
    const p = Bt(a[u - 2]);
    return (
      // we are dealing with nested routes
      u > 1 && // if the parent and matched route have the same path, this link is
      // referring to the empty child. Or we currently are on a different
      // child of the same parent
      Bt(f) === p && // avoid comparing the child with its parent
      d[d.length - 1].path !== p ? d.findIndex(te.bind(null, a[u - 2])) : v
    );
  }), c = U(() => i.value > -1 && Jo(n.params, s.value.params)), l = U(() => i.value > -1 && i.value === n.matched.length - 1 && _n(n.params, s.value.params));
  function h(a = {}) {
    if (zo(a)) {
      const u = t[W(e.replace) ? "replace" : "push"](
        W(e.to)
        // avoid uncaught errors are they are logged anyway
      ).catch(ve);
      return e.viewTransition && typeof document < "u" && "startViewTransition" in document && document.startViewTransition(() => u), u;
    }
    return Promise.resolve();
  }
  if (S.NODE_ENV !== "production" && z) {
    const a = zt();
    if (a) {
      const u = {
        route: s.value,
        isActive: c.value,
        isExactActive: l.value,
        error: null
      };
      a.__vrl_devtools = a.__vrl_devtools || [], a.__vrl_devtools.push(u), Ht(() => {
        u.route = s.value, u.isActive = c.value, u.isExactActive = l.value, u.error = Ae(W(e.to)) ? null : 'Invalid "to" value';
      }, { flush: "post" });
    }
  }
  return {
    route: s,
    href: U(() => s.value.href),
    isActive: c,
    isExactActive: l,
    navigate: h
  };
}
function Go(e) {
  return e.length === 1 ? e[0] : e;
}
const qo = /* @__PURE__ */ F({
  name: "RouterLink",
  compatConfig: { MODE: 3 },
  props: {
    to: {
      type: [String, Object],
      required: !0
    },
    replace: Boolean,
    activeClass: String,
    // inactiveClass: String,
    exactActiveClass: String,
    custom: Boolean,
    ariaCurrentValue: {
      type: String,
      default: "page"
    }
  },
  useLink: Ft,
  setup(e, { slots: t }) {
    const n = zn(Ft(e)), { options: r } = ee(Be), o = U(() => ({
      [Lt(e.activeClass, r.linkActiveClass, "router-link-active")]: n.isActive,
      // [getLinkClass(
      //   props.inactiveClass,
      //   options.linkInactiveClass,
      //   'router-link-inactive'
      // )]: !link.isExactActive,
      [Lt(e.exactActiveClass, r.linkExactActiveClass, "router-link-exact-active")]: n.isExactActive
    }));
    return () => {
      const s = t.default && Go(t.default(n));
      return e.custom ? s : A("a", {
        "aria-current": n.isExactActive ? e.ariaCurrentValue : null,
        href: n.href,
        // this would override user added attrs but Vue will still add
        // the listener, so we end up triggering both
        onClick: n.navigate,
        class: o.value
      }, s);
    };
  }
}), Ho = qo;
function zo(e) {
  if (!(e.metaKey || e.altKey || e.ctrlKey || e.shiftKey) && !e.defaultPrevented && !(e.button !== void 0 && e.button !== 0)) {
    if (e.currentTarget && e.currentTarget.getAttribute) {
      const t = e.currentTarget.getAttribute("target");
      if (/\b_blank\b/i.test(t))
        return;
    }
    return e.preventDefault && e.preventDefault(), !0;
  }
}
function Jo(e, t) {
  for (const n in t) {
    const r = t[n], o = e[n];
    if (typeof r == "string") {
      if (r !== o)
        return !1;
    } else if (!K(o) || o.length !== r.length || r.some((s, i) => s !== o[i]))
      return !1;
  }
  return !0;
}
function Bt(e) {
  return e ? e.aliasOf ? e.aliasOf.path : e.path : "";
}
const Lt = (e, t, n) => e ?? t ?? n, Qo = /* @__PURE__ */ F({
  name: "RouterView",
  // #674 we manually inherit them
  inheritAttrs: !1,
  props: {
    name: {
      type: String,
      default: "default"
    },
    route: Object
  },
  // Better compat for @vue/compat users
  // https://github.com/vuejs/router/issues/1315
  compatConfig: { MODE: 3 },
  setup(e, { attrs: t, slots: n }) {
    S.NODE_ENV !== "production" && Xo();
    const r = ee(ct), o = U(() => e.route || r.value), s = ee(Mt, 0), i = U(() => {
      let h = W(s);
      const { matched: a } = o.value;
      let u;
      for (; (u = a[h]) && !u.components; )
        h++;
      return h;
    }), c = U(() => o.value.matched[i.value]);
    Ie(Mt, U(() => i.value + 1)), Ie(Uo, c), Ie(ct, o);
    const l = Z();
    return G(() => [l.value, c.value, e.name], ([h, a, u], [f, d, v]) => {
      a && (a.instances[u] = h, d && d !== a && h && h === f && (a.leaveGuards.size || (a.leaveGuards = d.leaveGuards), a.updateGuards.size || (a.updateGuards = d.updateGuards))), h && a && // if there is no instance but to and from are the same this might be
      // the first visit
      (!d || !te(a, d) || !f) && (a.enterCallbacks[u] || []).forEach((p) => p(h));
    }, { flush: "post" }), () => {
      const h = o.value, a = e.name, u = c.value, f = u && u.components[a];
      if (!f)
        return Wt(n.default, { Component: f, route: h });
      const d = u.props[a], v = d ? d === !0 ? h.params : typeof d == "function" ? d(h) : d : null, g = A(f, I({}, v, t, {
        onVnodeUnmounted: (y) => {
          y.component.isUnmounted && (u.instances[a] = null);
        },
        ref: l
      }));
      if (S.NODE_ENV !== "production" && z && g.ref) {
        const y = {
          depth: i.value,
          name: u.name,
          path: u.path,
          meta: u.meta
        };
        (K(g.ref) ? g.ref.map((O) => O.i) : [g.ref.i]).forEach((O) => {
          O.__vrv_devtools = y;
        });
      }
      return (
        // pass the vnode to the slot as a prop.
        // h and <component :is="..."> both accept vnodes
        Wt(n.default, { Component: g, route: h }) || g
      );
    };
  }
});
function Wt(e, t) {
  if (!e)
    return null;
  const n = e(t);
  return n.length === 1 ? n[0] : n;
}
const Yo = Qo;
function Xo() {
  const e = zt(), t = e.parent && e.parent.type.name, n = e.parent && e.parent.subTree && e.parent.subTree.type;
  if (t && (t === "KeepAlive" || t.includes("Transition")) && typeof n == "object" && n.name === "RouterView") {
    const r = t === "KeepAlive" ? "keep-alive" : "transition";
    P(`<router-view> can no longer be used directly inside <transition> or <keep-alive>.
Use slot props instead:

<router-view v-slot="{ Component }">
  <${r}>
    <component :is="Component" />
  </${r}>
</router-view>`);
  }
}
function me(e, t) {
  const n = I({}, e, {
    // remove variables that can contain vue instances
    matched: e.matched.map((r) => us(r, ["instances", "children", "aliasOf"]))
  });
  return {
    _custom: {
      type: null,
      readOnly: !0,
      display: e.fullPath,
      tooltip: t,
      value: n
    }
  };
}
function Ne(e) {
  return {
    _custom: {
      display: e
    }
  };
}
let Zo = 0;
function es(e, t, n) {
  if (t.__hasDevtools)
    return;
  t.__hasDevtools = !0;
  const r = Zo++;
  Kr({
    id: "org.vuejs.router" + (r ? "." + r : ""),
    label: "Vue Router",
    packageName: "vue-router",
    homepage: "https://router.vuejs.org",
    logo: "https://router.vuejs.org/logo.png",
    componentStateTypes: ["Routing"],
    app: e
  }, (o) => {
    typeof o.now != "function" && console.warn("[Vue Router]: You seem to be using an outdated version of Vue Devtools. Are you still using the Beta release instead of the stable one? You can find the links at https://devtools.vuejs.org/guide/installation.html."), o.on.inspectComponent((a, u) => {
      a.instanceData && a.instanceData.state.push({
        type: "Routing",
        key: "$route",
        editable: !1,
        value: me(t.currentRoute.value, "Current Route")
      });
    }), o.on.visitComponentTree(({ treeNode: a, componentInstance: u }) => {
      if (u.__vrv_devtools) {
        const f = u.__vrv_devtools;
        a.tags.push({
          label: (f.name ? `${f.name.toString()}: ` : "") + f.path,
          textColor: 0,
          tooltip: "This component is rendered by &lt;router-view&gt;",
          backgroundColor: Nn
        });
      }
      K(u.__vrl_devtools) && (u.__devtoolsApi = o, u.__vrl_devtools.forEach((f) => {
        let d = f.route.path, v = An, p = "", g = 0;
        f.error ? (d = f.error, v = ss, g = is) : f.isExactActive ? (v = Tn, p = "This is exactly active") : f.isActive && (v = In, p = "This link is active"), a.tags.push({
          label: d,
          textColor: g,
          tooltip: p,
          backgroundColor: v
        });
      }));
    }), G(t.currentRoute, () => {
      l(), o.notifyComponentUpdate(), o.sendInspectorTree(c), o.sendInspectorState(c);
    });
    const s = "router:navigations:" + r;
    o.addTimelineLayer({
      id: s,
      label: `Router${r ? " " + r : ""} Navigations`,
      color: 4237508
    }), t.onError((a, u) => {
      o.addTimelineEvent({
        layerId: s,
        event: {
          title: "Error during Navigation",
          subtitle: u.fullPath,
          logType: "error",
          time: o.now(),
          data: { error: a },
          groupId: u.meta.__navigationId
        }
      });
    });
    let i = 0;
    t.beforeEach((a, u) => {
      const f = {
        guard: Ne("beforeEach"),
        from: me(u, "Current Location during this navigation"),
        to: me(a, "Target location")
      };
      Object.defineProperty(a.meta, "__navigationId", {
        value: i++
      }), o.addTimelineEvent({
        layerId: s,
        event: {
          time: o.now(),
          title: "Start of navigation",
          subtitle: a.fullPath,
          data: f,
          groupId: a.meta.__navigationId
        }
      });
    }), t.afterEach((a, u, f) => {
      const d = {
        guard: Ne("afterEach")
      };
      f ? (d.failure = {
        _custom: {
          type: Error,
          readOnly: !0,
          display: f ? f.message : "",
          tooltip: "Navigation Failure",
          value: f
        }
      }, d.status = Ne("❌")) : d.status = Ne("✅"), d.from = me(u, "Current Location during this navigation"), d.to = me(a, "Target location"), o.addTimelineEvent({
        layerId: s,
        event: {
          title: "End of navigation",
          subtitle: a.fullPath,
          time: o.now(),
          data: d,
          logType: f ? "warning" : "default",
          groupId: a.meta.__navigationId
        }
      });
    });
    const c = "router-inspector:" + r;
    o.addInspector({
      id: c,
      label: "Routes" + (r ? " " + r : ""),
      icon: "book",
      treeFilterPlaceholder: "Search routes"
    });
    function l() {
      if (!h)
        return;
      const a = h;
      let u = n.getRoutes().filter((f) => !f.parent || // these routes have a parent with no component which will not appear in the view
      // therefore we still need to include them
      !f.parent.record.components);
      u.forEach(Cn), a.filter && (u = u.filter((f) => (
        // save matches state based on the payload
        ut(f, a.filter.toLowerCase())
      ))), u.forEach((f) => jn(f, t.currentRoute.value)), a.rootNodes = u.map($n);
    }
    let h;
    o.on.getInspectorTree((a) => {
      h = a, a.app === e && a.inspectorId === c && l();
    }), o.on.getInspectorState((a) => {
      if (a.app === e && a.inspectorId === c) {
        const f = n.getRoutes().find((d) => d.record.__vd_id === a.nodeId);
        f && (a.state = {
          options: ns(f)
        });
      }
    }), o.sendInspectorTree(c), o.sendInspectorState(c);
  });
}
function ts(e) {
  return e.optional ? e.repeatable ? "*" : "?" : e.repeatable ? "+" : "";
}
function ns(e) {
  const { record: t } = e, n = [
    { editable: !1, key: "path", value: t.path }
  ];
  return t.name != null && n.push({
    editable: !1,
    key: "name",
    value: t.name
  }), n.push({ editable: !1, key: "regexp", value: e.re }), e.keys.length && n.push({
    editable: !1,
    key: "keys",
    value: {
      _custom: {
        type: null,
        readOnly: !0,
        display: e.keys.map((r) => `${r.name}${ts(r)}`).join(" "),
        tooltip: "Param keys",
        value: e.keys
      }
    }
  }), t.redirect != null && n.push({
    editable: !1,
    key: "redirect",
    value: t.redirect
  }), e.alias.length && n.push({
    editable: !1,
    key: "aliases",
    value: e.alias.map((r) => r.record.path)
  }), Object.keys(e.record.meta).length && n.push({
    editable: !1,
    key: "meta",
    value: e.record.meta
  }), n.push({
    key: "score",
    editable: !1,
    value: {
      _custom: {
        type: null,
        readOnly: !0,
        display: e.score.map((r) => r.join(", ")).join(" | "),
        tooltip: "Score used to sort routes",
        value: e.score
      }
    }
  }), n;
}
const Nn = 15485081, In = 2450411, Tn = 8702998, rs = 2282478, An = 16486972, os = 6710886, ss = 16704226, is = 12131356;
function $n(e) {
  const t = [], { record: n } = e;
  n.name != null && t.push({
    label: String(n.name),
    textColor: 0,
    backgroundColor: rs
  }), n.aliasOf && t.push({
    label: "alias",
    textColor: 0,
    backgroundColor: An
  }), e.__vd_match && t.push({
    label: "matches",
    textColor: 0,
    backgroundColor: Nn
  }), e.__vd_exactActive && t.push({
    label: "exact",
    textColor: 0,
    backgroundColor: Tn
  }), e.__vd_active && t.push({
    label: "active",
    textColor: 0,
    backgroundColor: In
  }), n.redirect && t.push({
    label: typeof n.redirect == "string" ? `redirect: ${n.redirect}` : "redirects",
    textColor: 16777215,
    backgroundColor: os
  });
  let r = n.__vd_id;
  return r == null && (r = String(as++), n.__vd_id = r), {
    id: r,
    label: n.path,
    tags: t,
    children: e.children.map($n)
  };
}
let as = 0;
const cs = /^\/(.*)\/([a-z]*)$/;
function jn(e, t) {
  const n = t.matched.length && te(t.matched[t.matched.length - 1], e.record);
  e.__vd_exactActive = e.__vd_active = n, n || (e.__vd_active = t.matched.some((r) => te(r, e.record))), e.children.forEach((r) => jn(r, t));
}
function Cn(e) {
  e.__vd_match = !1, e.children.forEach(Cn);
}
function ut(e, t) {
  const n = String(e.re).match(cs);
  if (e.__vd_match = !1, !n || n.length < 3)
    return !1;
  if (new RegExp(n[1].replace(/\$$/, ""), n[2]).test(t))
    return e.children.forEach((i) => ut(i, t)), e.record.path !== "/" || t === "/" ? (e.__vd_match = e.re.test(t), !0) : !1;
  const o = e.record.path.toLowerCase(), s = ae(o);
  return !t.startsWith("/") && (s.includes(t) || o.includes(t)) || s.startsWith(t) || o.startsWith(t) || e.record.name && String(e.record.name).includes(t) ? !0 : e.children.some((i) => ut(i, t));
}
function us(e, t) {
  const n = {};
  for (const r in e)
    t.includes(r) || (n[r] = e[r]);
  return n;
}
function ls(e) {
  const t = Ao(e.routes, e), n = e.parseQuery || Lo, r = e.stringifyQuery || Dt, o = e.history;
  if (S.NODE_ENV !== "production" && !o)
    throw new Error('Provide the "history" option when calling "createRouter()": https://router.vuejs.org/api/interfaces/RouterOptions.html#history');
  const s = pe(), i = pe(), c = pe(), l = J(Y);
  let h = Y;
  z && e.scrollBehavior && "scrollRestoration" in history && (history.scrollRestoration = "manual");
  const a = He.bind(null, (m) => "" + m), u = He.bind(null, oo), f = (
    // @ts-expect-error: intentionally avoid the type check
    He.bind(null, ae)
  );
  function d(m, E) {
    let w, b;
    return Pn(m) ? (w = t.getRecordMatcher(m), S.NODE_ENV !== "production" && !w && P(`Parent route "${String(m)}" not found when adding child route`, E), b = E) : b = m, t.addRoute(b, w);
  }
  function v(m) {
    const E = t.getRecordMatcher(m);
    E ? t.removeRoute(E) : S.NODE_ENV !== "production" && P(`Cannot remove non-existent route "${String(m)}"`);
  }
  function p() {
    return t.getRoutes().map((m) => m.record);
  }
  function g(m) {
    return !!t.getRecordMatcher(m);
  }
  function y(m, E) {
    if (E = I({}, E || l.value), typeof m == "string") {
      const k = ze(n, m, E.path), $ = t.resolve({ path: k.path }, E), re = o.createHref(k.fullPath);
      return S.NODE_ENV !== "production" && (re.startsWith("//") ? P(`Location "${m}" resolved to "${re}". A resolved location cannot start with multiple slashes.`) : $.matched.length || P(`No match found for location with path "${m}"`)), I(k, $, {
        params: f($.params),
        hash: ae(k.hash),
        redirectedFrom: void 0,
        href: re
      });
    }
    if (S.NODE_ENV !== "production" && !Ae(m))
      return P(`router.resolve() was passed an invalid location. This will fail in production.
- Location:`, m), y({});
    let w;
    if (m.path != null)
      S.NODE_ENV !== "production" && "params" in m && !("name" in m) && // @ts-expect-error: the type is never
      Object.keys(m.params).length && P(`Path "${m.path}" was passed with params but they will be ignored. Use a named route alongside params instead.`), w = I({}, m, {
        path: ze(n, m.path, E.path).path
      });
    else {
      const k = I({}, m.params);
      for (const $ in k)
        k[$] == null && delete k[$];
      w = I({}, m, {
        params: u(k)
      }), E.params = u(E.params);
    }
    const b = t.resolve(w, E), T = m.hash || "";
    S.NODE_ENV !== "production" && T && !T.startsWith("#") && P(`A \`hash\` should always start with the character "#". Replace "${T}" with "#${T}".`), b.params = a(f(b.params));
    const j = ao(r, I({}, m, {
      hash: to(T),
      path: b.path
    })), V = o.createHref(j);
    return S.NODE_ENV !== "production" && (V.startsWith("//") ? P(`Location "${m}" resolved to "${V}". A resolved location cannot start with multiple slashes.`) : b.matched.length || P(`No match found for location with path "${m.path != null ? m.path : m}"`)), I({
      fullPath: j,
      // keep the hash encoded so fullPath is effectively path + encodedQuery +
      // hash
      hash: T,
      query: (
        // if the user is using a custom query lib like qs, we might have
        // nested objects, so we keep the query as is, meaning it can contain
        // numbers at `$route.query`, but at the point, the user will have to
        // use their own type anyway.
        // https://github.com/vuejs/router/issues/328#issuecomment-649481567
        r === Dt ? Wo(m.query) : m.query || {}
      )
    }, b, {
      redirectedFrom: void 0,
      href: V
    });
  }
  function _(m) {
    return typeof m == "string" ? ze(n, m, l.value.path) : I({}, m);
  }
  function O(m, E) {
    if (h !== m)
      return ue(8, {
        from: E,
        to: m
      });
  }
  function R(m) {
    return x(m);
  }
  function D(m) {
    return R(I(_(m), { replace: !0 }));
  }
  function C(m) {
    const E = m.matched[m.matched.length - 1];
    if (E && E.redirect) {
      const { redirect: w } = E;
      let b = typeof w == "function" ? w(m) : w;
      if (typeof b == "string" && (b = b.includes("?") || b.includes("#") ? b = _(b) : (
        // force empty params
        { path: b }
      ), b.params = {}), S.NODE_ENV !== "production" && b.path == null && !("name" in b))
        throw P(`Invalid redirect found:
${JSON.stringify(b, null, 2)}
 when navigating to "${m.fullPath}". A redirect must contain a name or path. This will break in production.`), new Error("Invalid redirect");
      return I({
        query: m.query,
        hash: m.hash,
        // avoid transferring params if the redirect has a path
        params: b.path != null ? {} : m.params
      }, b);
    }
  }
  function x(m, E) {
    const w = h = y(m), b = l.value, T = m.state, j = m.force, V = m.replace === !0, k = C(w);
    if (k)
      return x(
        I(_(k), {
          state: typeof k == "object" ? I({}, T, k.state) : T,
          force: j,
          replace: V
        }),
        // keep original redirectedFrom if it exists
        E || w
      );
    const $ = w;
    $.redirectedFrom = E;
    let re;
    return !j && Pt(r, b, w) && (re = ue(16, { to: $, from: b }), Et(
      b,
      b,
      // this is a push, the only way for it to be triggered from a
      // history.listen is with a redirect, which makes it become a push
      !0,
      // This cannot be the first navigation because the initial location
      // cannot be manually navigated to
      !1
    )), (re ? Promise.resolve(re) : gt($, b)).catch((M) => H(M) ? (
      // navigation redirects still mark the router as ready
      H(
        M,
        2
        /* ErrorTypes.NAVIGATION_GUARD_REDIRECT */
      ) ? M : Ke(M)
    ) : (
      // reject any unknown error
      Ue(M, $, b)
    )).then((M) => {
      if (M) {
        if (H(
          M,
          2
          /* ErrorTypes.NAVIGATION_GUARD_REDIRECT */
        ))
          return S.NODE_ENV !== "production" && // we are redirecting to the same location we were already at
          Pt(r, y(M.to), $) && // and we have done it a couple of times
          E && // @ts-expect-error: added only in dev
          (E._count = E._count ? (
            // @ts-expect-error
            E._count + 1
          ) : 1) > 30 ? (P(`Detected a possibly infinite redirection in a navigation guard when going from "${b.fullPath}" to "${$.fullPath}". Aborting to avoid a Stack Overflow.
 Are you always returning a new location within a navigation guard? That would lead to this error. Only return when redirecting or aborting, that should fix this. This might break in production if not fixed.`), Promise.reject(new Error("Infinite redirect in navigation guard"))) : x(
            // keep options
            I({
              // preserve an existing replacement but allow the redirect to override it
              replace: V
            }, _(M.to), {
              state: typeof M.to == "object" ? I({}, T, M.to.state) : T,
              force: j
            }),
            // preserve the original redirectedFrom if any
            E || $
          );
      } else
        M = yt($, b, !0, V, T);
      return vt($, b, M), M;
    });
  }
  function Le(m, E) {
    const w = O(m, E);
    return w ? Promise.reject(w) : Promise.resolve();
  }
  function le(m) {
    const E = ke.values().next().value;
    return E && typeof E.runWithContext == "function" ? E.runWithContext(m) : m();
  }
  function gt(m, E) {
    let w;
    const [b, T, j] = fs(m, E);
    w = Qe(b.reverse(), "beforeRouteLeave", m, E);
    for (const k of b)
      k.leaveGuards.forEach(($) => {
        w.push(X($, m, E));
      });
    const V = Le.bind(null, m, E);
    return w.push(V), se(w).then(() => {
      w = [];
      for (const k of s.list())
        w.push(X(k, m, E));
      return w.push(V), se(w);
    }).then(() => {
      w = Qe(T, "beforeRouteUpdate", m, E);
      for (const k of T)
        k.updateGuards.forEach(($) => {
          w.push(X($, m, E));
        });
      return w.push(V), se(w);
    }).then(() => {
      w = [];
      for (const k of j)
        if (k.beforeEnter)
          if (K(k.beforeEnter))
            for (const $ of k.beforeEnter)
              w.push(X($, m, E));
          else
            w.push(X(k.beforeEnter, m, E));
      return w.push(V), se(w);
    }).then(() => (m.matched.forEach((k) => k.enterCallbacks = {}), w = Qe(j, "beforeRouteEnter", m, E, le), w.push(V), se(w))).then(() => {
      w = [];
      for (const k of i.list())
        w.push(X(k, m, E));
      return w.push(V), se(w);
    }).catch((k) => H(
      k,
      8
      /* ErrorTypes.NAVIGATION_CANCELLED */
    ) ? k : Promise.reject(k));
  }
  function vt(m, E, w) {
    c.list().forEach((b) => le(() => b(m, E, w)));
  }
  function yt(m, E, w, b, T) {
    const j = O(m, E);
    if (j)
      return j;
    const V = E === Y, k = z ? history.state : {};
    w && (b || V ? o.replace(m.fullPath, I({
      scroll: V && k && k.scroll
    }, T)) : o.push(m.fullPath, T)), l.value = m, Et(m, E, w, V), Ke();
  }
  let fe;
  function Bn() {
    fe || (fe = o.listen((m, E, w) => {
      if (!_t.listening)
        return;
      const b = y(m), T = C(b);
      if (T) {
        x(I(T, { replace: !0, force: !0 }), b).catch(ve);
        return;
      }
      h = b;
      const j = l.value;
      z && po(Vt(j.fullPath, w.delta), Fe()), gt(b, j).catch((V) => H(
        V,
        12
        /* ErrorTypes.NAVIGATION_CANCELLED */
      ) ? V : H(
        V,
        2
        /* ErrorTypes.NAVIGATION_GUARD_REDIRECT */
      ) ? (x(
        I(_(V.to), {
          force: !0
        }),
        b
        // avoid an uncaught rejection, let push call triggerError
      ).then((k) => {
        H(
          k,
          20
          /* ErrorTypes.NAVIGATION_DUPLICATED */
        ) && !w.delta && w.type === ce.pop && o.go(-1, !1);
      }).catch(ve), Promise.reject()) : (w.delta && o.go(-w.delta, !1), Ue(V, b, j))).then((V) => {
        V = V || yt(
          // after navigation, all matched components are resolved
          b,
          j,
          !1
        ), V && (w.delta && // a new navigation has been triggered, so we do not want to revert, that will change the current history
        // entry while a different route is displayed
        !H(
          V,
          8
          /* ErrorTypes.NAVIGATION_CANCELLED */
        ) ? o.go(-w.delta, !1) : w.type === ce.pop && H(
          V,
          20
          /* ErrorTypes.NAVIGATION_DUPLICATED */
        ) && o.go(-1, !1)), vt(b, j, V);
      }).catch(ve);
    }));
  }
  let We = pe(), wt = pe(), Pe;
  function Ue(m, E, w) {
    Ke(m);
    const b = wt.list();
    return b.length ? b.forEach((T) => T(m, E, w)) : (S.NODE_ENV !== "production" && P("uncaught error during route navigation:"), console.error(m)), Promise.reject(m);
  }
  function Ln() {
    return Pe && l.value !== Y ? Promise.resolve() : new Promise((m, E) => {
      We.add([m, E]);
    });
  }
  function Ke(m) {
    return Pe || (Pe = !m, Bn(), We.list().forEach(([E, w]) => m ? w(m) : E()), We.reset()), m;
  }
  function Et(m, E, w, b) {
    const { scrollBehavior: T } = e;
    if (!z || !T)
      return Promise.resolve();
    const j = !w && mo(Vt(m.fullPath, 0)) || (b || !w) && history.state && history.state.scroll || null;
    return Te().then(() => T(m, E, j)).then((V) => V && ho(V)).catch((V) => Ue(V, m, E));
  }
  const Ge = (m) => o.go(m);
  let qe;
  const ke = /* @__PURE__ */ new Set(), _t = {
    currentRoute: l,
    listening: !0,
    addRoute: d,
    removeRoute: v,
    clearRoutes: t.clearRoutes,
    hasRoute: g,
    getRoutes: p,
    resolve: y,
    options: e,
    push: R,
    replace: D,
    go: Ge,
    back: () => Ge(-1),
    forward: () => Ge(1),
    beforeEach: s.add,
    beforeResolve: i.add,
    afterEach: c.add,
    onError: wt.add,
    isReady: Ln,
    install(m) {
      const E = this;
      m.component("RouterLink", Ho), m.component("RouterView", Yo), m.config.globalProperties.$router = E, Object.defineProperty(m.config.globalProperties, "$route", {
        enumerable: !0,
        get: () => W(l)
      }), z && // used for the initial navigation client side to avoid pushing
      // multiple times when the router is used in multiple apps
      !qe && l.value === Y && (qe = !0, R(o.location).catch((T) => {
        S.NODE_ENV !== "production" && P("Unexpected error when starting the router:", T);
      }));
      const w = {};
      for (const T in Y)
        Object.defineProperty(w, T, {
          get: () => l.value[T],
          enumerable: !0
        });
      m.provide(Be, E), m.provide(mt, Hn(w)), m.provide(ct, l);
      const b = m.unmount;
      ke.add(m), m.unmount = function() {
        ke.delete(m), ke.size < 1 && (h = Y, fe && fe(), fe = null, l.value = Y, qe = !1, Pe = !1), b();
      }, S.NODE_ENV !== "production" && z && es(m, E, t);
    }
  };
  function se(m) {
    return m.reduce((E, w) => E.then(() => le(w)), Promise.resolve());
  }
  return _t;
}
function fs(e, t) {
  const n = [], r = [], o = [], s = Math.max(t.matched.length, e.matched.length);
  for (let i = 0; i < s; i++) {
    const c = t.matched[i];
    c && (e.matched.find((h) => te(h, c)) ? r.push(c) : n.push(c));
    const l = e.matched[i];
    l && (t.matched.find((h) => te(h, l)) || o.push(l));
  }
  return [n, r, o];
}
function hs() {
  return ee(Be);
}
function ds(e) {
  return ee(mt);
}
function ne(e) {
  let t = sn(), n = Rr(), r = Tr(e), o = un(), s = hs(), i = ds();
  function c(p) {
    p.scopeSnapshot && (t = p.scopeSnapshot), p.slotSnapshot && (n = p.slotSnapshot), p.vforSnapshot && (r = p.vforSnapshot), p.elementRefSnapshot && (o = p.elementRefSnapshot), p.routerSnapshot && (s = p.routerSnapshot);
  }
  function l(p) {
    if (N.isVar(p))
      return q(h(p));
    if (N.isVForItem(p))
      return $r(p.fid) ? r.getVForIndex(p.fid) : q(h(p));
    if (N.isVForIndex(p))
      return r.getVForIndex(p.fid);
    if (N.isJs(p)) {
      const { code: g, bind: y } = p, _ = Oe(y, (O) => a(O));
      return xr(g, _)();
    }
    if (N.isSlotProp(p))
      return n.getPropsValue(p);
    if (N.isRouterParams(p))
      return q(h(p));
    throw new Error(`Invalid binding: ${p}`);
  }
  function h(p) {
    if (N.isVar(p)) {
      const g = t.getVueRef(p) || yr(p);
      return bt(g, {
        paths: p.path,
        getBindableValueFn: l
      });
    }
    if (N.isVForItem(p))
      return Ar({
        binding: p,
        snapshot: v
      });
    if (N.isVForIndex(p))
      return () => l(p);
    if (N.isRouterParams(p)) {
      const { prop: g = "params" } = p;
      return bt(() => i[g], {
        paths: p.path,
        getBindableValueFn: l
      });
    }
    throw new Error(`Invalid binding: ${p}`);
  }
  function a(p) {
    if (N.isVar(p) || N.isVForItem(p))
      return h(p);
    if (N.isVForIndex(p))
      return l(p);
    if (N.isJs(p))
      return null;
    if (N.isRouterParams(p))
      return h(p);
    throw new Error(`Invalid binding: ${p}`);
  }
  function u(p) {
    if (N.isVar(p))
      return {
        sid: p.sid,
        id: p.id
      };
    if (N.isVForItem(p))
      return {
        type: "vf",
        fid: p.fid
      };
    if (N.isVForIndex(p))
      return {
        type: "vf-i",
        fid: p.fid,
        value: null
      };
    if (N.isJs(p))
      return null;
  }
  function f(p) {
    var g, y;
    (g = p.vars) == null || g.forEach((_) => {
      h({ type: "var", ..._ }).value = _.val;
    }), (y = p.ele_refs) == null || y.forEach((_) => {
      o.getRef({
        sid: _.sid,
        id: _.id
      }).value[_.method](..._.args);
    });
  }
  function d(p, g) {
    if (St(g) || St(p.values))
      return;
    g = g;
    const y = p.values, _ = p.skips || new Array(g.length).fill(0);
    g.forEach((O, R) => {
      if (_[R] === 1)
        return;
      if (N.isVar(O)) {
        const C = h(O);
        C.value = y[R];
        return;
      }
      if (N.isRouterAction(O)) {
        const C = y[R], x = s[C.fn];
        x(...C.args);
        return;
      }
      if (N.isElementRef(O)) {
        const C = o.getRef(O).value, x = y[R], { method: Le, args: le = [] } = x;
        C[Le](...le);
        return;
      }
      if (N.isJsOutput(O)) {
        const C = y[R], x = L(C);
        typeof x == "function" && x();
        return;
      }
      const D = h(O);
      D.value = y[R];
    });
  }
  const v = {
    getVForIndex: r.getVForIndex,
    getObjectToValue: l,
    getVueRefObject: h,
    getVueRefObjectOrValue: a,
    getBindingServerInfo: u,
    updateRefFromServer: f,
    updateOutputsRefFromServer: d,
    replaceSnapshot: c
  };
  return v;
}
class ps {
  async eventSend(t, n) {
    const { fType: r, hKey: o, key: s } = t, i = Xe().webServerInfo, c = s !== void 0 ? { key: s } : {}, l = r === "sync" ? i.event_url : i.event_async_url;
    let h = {};
    const a = await fetch(l, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        bind: n,
        hKey: o,
        ...c,
        page: ye(),
        ...h
      })
    });
    if (!a.ok)
      throw new Error(`HTTP error! status: ${a.status}`);
    return await a.json();
  }
  async watchSend(t) {
    const { outputs: n, fType: r, key: o } = t.watchConfig, s = Xe().webServerInfo, i = r === "sync" ? s.watch_url : s.watch_async_url, c = t.getServerInputs(), l = {
      key: o,
      input: c,
      page: ye()
    };
    return await (await fetch(i, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(l)
    })).json();
  }
}
class ms {
  async eventSend(t, n) {
    const { fType: r, hKey: o, key: s } = t, i = s !== void 0 ? { key: s } : {};
    let c = {};
    const l = {
      bind: n,
      fType: r,
      hKey: o,
      ...i,
      page: ye(),
      ...c
    };
    return await window.pywebview.api.event_call(l);
  }
  async watchSend(t) {
    const { outputs: n, fType: r, key: o } = t.watchConfig, s = t.getServerInputs(), i = {
      key: o,
      input: s,
      fType: r,
      page: ye()
    };
    return await window.pywebview.api.watch_call(i);
  }
}
let lt;
function gs(e) {
  switch (e.mode) {
    case "web":
      lt = new ps();
      break;
    case "webview":
      lt = new ms();
      break;
  }
}
function xn() {
  return lt;
}
function vs(e) {
  const t = {
    type: "var",
    sid: e.sid,
    id: e.id
  };
  return {
    ...e,
    immediate: !0,
    outputs: [t, ...e.outputs || []]
  };
}
function ys(e, t, n) {
  return new ws(e, t, n);
}
class ws {
  constructor(t, n, r) {
    B(this, "taskQueue", []);
    B(this, "id2TaskMap", /* @__PURE__ */ new Map());
    B(this, "input2TaskIdMap", _e(() => []));
    this.snapshots = r;
    const o = [], s = (i) => {
      var l;
      const c = new Es(i, r);
      return this.id2TaskMap.set(c.id, c), (l = i.inputs) == null || l.forEach((h, a) => {
        var f, d;
        if (((f = i.data) == null ? void 0 : f[a]) === 0 && ((d = i.slient) == null ? void 0 : d[a]) === 0) {
          const v = `${h.sid}-${h.id}`;
          this.input2TaskIdMap.getOrDefault(v).push(c.id);
        }
      }), c;
    };
    t == null || t.forEach((i) => {
      const c = s(i);
      o.push(c);
    }), n == null || n.forEach((i) => {
      const c = s(
        vs(i)
      );
      o.push(c);
    }), o.forEach((i) => {
      const {
        deep: c = !0,
        once: l,
        flush: h,
        immediate: a = !0
      } = i.watchConfig, u = {
        immediate: a,
        deep: c,
        once: l,
        flush: h
      }, f = this._getWatchTargets(i);
      G(
        f,
        (d) => {
          d.some(Ee) || (i.modify = !0, this.taskQueue.push(new _s(i)), this._scheduleNextTick());
        },
        u
      );
    });
  }
  _getWatchTargets(t) {
    if (!t.watchConfig.inputs)
      return [];
    const n = t.slientInputs, r = t.constDataInputs;
    return t.watchConfig.inputs.filter(
      (s, i) => !r[i] && (N.isVar(s) || N.isVForItem(s) || N.isRouterParams(s)) && !n[i]
    ).map((s) => this.snapshots.getVueRefObjectOrValue(s));
  }
  _scheduleNextTick() {
    Te(() => this._runAllTasks());
  }
  _runAllTasks() {
    const t = this.taskQueue.slice();
    this.taskQueue.length = 0, this._setTaskNodeRelations(t), t.forEach((n) => {
      n.run();
    });
  }
  _setTaskNodeRelations(t) {
    t.forEach((n) => {
      const r = this._findNextNodes(n, t);
      n.appendNextNodes(...r), r.forEach((o) => {
        o.appendPrevNodes(n);
      });
    });
  }
  _findNextNodes(t, n) {
    const r = t.watchTask.watchConfig.outputs;
    if (r && r.length <= 0)
      return [];
    const o = this._getCalculatorTasksByOutput(
      t.watchTask.watchConfig.outputs
    );
    return n.filter(
      (s) => o.has(s.watchTask.id) && s.watchTask.id !== t.watchTask.id
    );
  }
  _getCalculatorTasksByOutput(t) {
    const n = /* @__PURE__ */ new Set();
    return t == null || t.forEach((r) => {
      const o = `${r.sid}-${r.id}`;
      (this.input2TaskIdMap.get(o) || []).forEach((i) => n.add(i));
    }), n;
  }
}
class Es {
  constructor(t, n) {
    B(this, "modify", !0);
    B(this, "_running", !1);
    B(this, "id");
    B(this, "_runningPromise", null);
    B(this, "_runningPromiseResolve", null);
    B(this, "_inputInfos");
    this.watchConfig = t, this.snapshot = n, this.id = Symbol(t.debug), this._inputInfos = this.createInputInfos();
  }
  createInputInfos() {
    const { inputs: t = [] } = this.watchConfig, n = this.watchConfig.data || new Array(t.length).fill(0), r = this.watchConfig.slient || new Array(t.length).fill(0);
    return {
      const_data: n,
      slients: r
    };
  }
  get slientInputs() {
    return this._inputInfos.slients;
  }
  get constDataInputs() {
    return this._inputInfos.const_data;
  }
  getServerInputs() {
    const { const_data: t } = this._inputInfos;
    return this.watchConfig.inputs ? this.watchConfig.inputs.map((n, r) => t[r] === 0 ? this.snapshot.getObjectToValue(n) : n) : [];
  }
  get running() {
    return this._running;
  }
  get runningPromise() {
    return this._runningPromise;
  }
  /**
   * setRunning
   */
  setRunning() {
    this._running = !0, this._runningPromise = new Promise((t) => {
      this._runningPromiseResolve = t;
    }), this._trySetRunningRef(!0);
  }
  /**
   * taskDone
   */
  taskDone() {
    this._running = !1, this._runningPromiseResolve && (this._runningPromiseResolve(), this._runningPromiseResolve = null), this._trySetRunningRef(!1);
  }
  _trySetRunningRef(t) {
    if (this.watchConfig.running) {
      const n = this.snapshot.getVueRefObject(
        this.watchConfig.running
      );
      n.value = t;
    }
  }
}
class _s {
  /**
   *
   */
  constructor(t) {
    B(this, "prevNodes", []);
    B(this, "nextNodes", []);
    B(this, "_runningPrev", !1);
    this.watchTask = t;
  }
  /**
   * appendPrevNodes
   */
  appendPrevNodes(...t) {
    this.prevNodes.push(...t);
  }
  /**
   *
   */
  appendNextNodes(...t) {
    this.nextNodes.push(...t);
  }
  /**
   * hasNextNodes
   */
  hasNextNodes() {
    return this.nextNodes.length > 0;
  }
  /**
   * run
   */
  async run() {
    if (this.prevNodes.length > 0 && !this._runningPrev)
      try {
        this._runningPrev = !0, await Promise.all(this.prevNodes.map((t) => t.run()));
      } finally {
        this._runningPrev = !1;
      }
    if (this.watchTask.running) {
      await this.watchTask.runningPromise;
      return;
    }
    if (this.watchTask.modify) {
      this.watchTask.modify = !1, this.watchTask.setRunning();
      try {
        await Os(this.watchTask);
      } finally {
        this.watchTask.taskDone();
      }
    }
  }
}
async function Os(e) {
  const { snapshot: t } = e, { outputs: n } = e.watchConfig, r = await xn().watchSend(e);
  r && t.updateOutputsRefFromServer(r, n);
}
function bs(e, t) {
  const {
    on: n,
    code: r,
    immediate: o,
    deep: s,
    once: i,
    flush: c,
    bind: l = {},
    onData: h,
    bindData: a
  } = e, u = h || new Array(n.length).fill(0), f = a || new Array(Object.keys(l).length).fill(0), d = Oe(
    l,
    (g, y, _) => f[_] === 0 ? t.getVueRefObject(g) : g
  ), v = L(r, d), p = n.length === 1 ? Ut(u[0] === 1, n[0], t) : n.map(
    (g, y) => Ut(u[y] === 1, g, t)
  );
  return G(p, v, { immediate: o, deep: s, once: i, flush: c });
}
function Ut(e, t, n) {
  return e ? () => t : n.getVueRefObject(t);
}
function Ss(e, t) {
  const {
    inputs: n = [],
    outputs: r,
    slient: o,
    data: s,
    code: i,
    immediate: c = !0,
    deep: l,
    once: h,
    flush: a
  } = e, u = o || new Array(n.length).fill(0), f = s || new Array(n.length).fill(0), d = L(i), v = n.filter((g, y) => u[y] === 0 && f[y] === 0).map((g) => t.getVueRefObject(g));
  function p() {
    return n.map((g, y) => f[y] === 0 ? tn(q(t.getVueRefObject(g))) : g);
  }
  G(
    v,
    () => {
      let g = d(...p());
      if (!r)
        return;
      const _ = r.length === 1 ? [g] : g, O = _.map((R) => R === void 0 ? 1 : 0);
      t.updateOutputsRefFromServer(
        { values: _, skips: O },
        r
      );
    },
    { immediate: c, deep: l, once: h, flush: a }
  );
}
function Rs(e, t) {
  return Object.assign(
    {},
    ...Object.entries(e ?? {}).map(([n, r]) => {
      const o = r.map((c) => {
        if (c.type === "web") {
          const l = Ps(c.bind, t);
          return ks(c, l, t);
        } else {
          if (c.type === "vue")
            return Ns(c, t);
          if (c.type === "js")
            return Vs(c, t);
        }
        throw new Error(`unknown event type ${c}`);
      }), i = L(
        " (...args)=> Promise.all(promises(...args))",
        {
          promises: (...c) => o.map(async (l) => {
            await l(...c);
          })
        }
      );
      return { [n]: i };
    })
  );
}
function Ps(e, t) {
  return (...n) => (e ?? []).map((r) => {
    if (N.isEventContext(r)) {
      if (r.path.startsWith(":")) {
        const o = r.path.slice(1);
        return L(o)(...n);
      }
      return be(n[0], r.path.split("."));
    }
    return N.IsBinding(r) ? t.getObjectToValue(r) : r;
  });
}
function ks(e, t, n) {
  async function r(...o) {
    const s = t(...o), i = await xn().eventSend(e, s);
    i && n.updateOutputsRefFromServer(i, e.set);
  }
  return r;
}
function Vs(e, t) {
  const { code: n, inputs: r = [], set: o } = e, s = L(n);
  function i(...c) {
    const l = (r ?? []).map((a) => {
      if (N.isEventContext(a)) {
        if (a.path.startsWith(":")) {
          const u = a.path.slice(1);
          return L(u)(...c);
        }
        return be(c[0], a.path.split("."));
      }
      return N.IsBinding(a) ? tn(t.getObjectToValue(a)) : a;
    }), h = s(...l);
    if (o !== void 0) {
      const u = o.length === 1 ? [h] : h, f = u.map((d) => d === void 0 ? 1 : 0);
      t.updateOutputsRefFromServer({ values: u, skips: f }, o);
    }
  }
  return i;
}
function Ns(e, t) {
  const { code: n, bind: r = {}, bindData: o } = e, s = o || new Array(Object.keys(r).length).fill(0), i = Oe(
    r,
    (h, a, u) => s[u] === 0 ? t.getVueRefObject(h) : h
  ), c = L(n, i);
  function l(...h) {
    c(...h);
  }
  return l;
}
function Is(e, t) {
  const n = [];
  (e.bStyle || []).forEach((s) => {
    Array.isArray(s) ? n.push(
      ...s.map((i) => t.getObjectToValue(i))
    ) : n.push(
      Oe(
        s,
        (i) => t.getObjectToValue(i)
      )
    );
  });
  const r = Jn([e.style || {}, n]);
  return {
    hasStyle: r && Object.keys(r).length > 0,
    styles: r
  };
}
function Ts(e, t) {
  const n = e.classes;
  if (!n)
    return null;
  if (typeof n == "string")
    return Ye(n);
  const { str: r, map: o, bind: s } = n, i = [];
  return r && i.push(r), o && i.push(
    Oe(
      o,
      (c) => t.getObjectToValue(c)
    )
  ), s && i.push(...s.map((c) => t.getObjectToValue(c))), Ye(i);
}
function $e(e, t = !0) {
  if (!(typeof e != "object" || e === null)) {
    if (Array.isArray(e)) {
      t && e.forEach((n) => $e(n, !0));
      return;
    }
    for (const [n, r] of Object.entries(e))
      if (n.startsWith(":"))
        try {
          e[n.slice(1)] = new Function(`return (${r})`)(), delete e[n];
        } catch (o) {
          console.error(
            `Error while converting ${n} attribute to function:`,
            o
          );
        }
      else
        t && $e(r, !0);
  }
}
function As(e, t) {
  const n = e.startsWith(":");
  return n && (e = e.slice(1), t = L(t)), { name: e, value: t, isFunc: n };
}
function $s(e, t, n) {
  var o;
  const r = {};
  return Ot(e.bProps || {}, (s, i) => {
    const c = n.getObjectToValue(s);
    Ee(c) || ($e(c), r[i] = js(c, i));
  }), (o = e.proxyProps) == null || o.forEach((s) => {
    const i = n.getObjectToValue(s);
    typeof i == "object" && Ot(i, (c, l) => {
      const { name: h, value: a } = As(l, c);
      r[h] = a;
    });
  }), { ...t || {}, ...r };
}
function js(e, t) {
  return t === "innerText" ? Jt(e) : e;
}
function Cs(e, { slots: t }) {
  const { id: n, use: r } = e.propsInfo, o = Or(n);
  return xe(() => {
    Sr(n);
  }), () => {
    const s = e.propsValue;
    return br(
      n,
      o,
      Object.fromEntries(
        r.map((i) => [i, s[i]])
      )
    ), A(De, null, t.default());
  };
}
const xs = F(Cs, {
  props: ["propsInfo", "propsValue"]
});
function Ds(e, t) {
  if (!e.slots)
    return null;
  const n = e.slots ?? {};
  return Array.isArray(n) ? t ? ge(n) : () => ge(n) : Xt(n, { keyFn: (i) => i === ":" ? "default" : i, valueFn: (i) => {
    const { items: c } = i;
    return (l) => {
      if (i.scope) {
        const h = () => i.props ? Kt(i.props, l, c) : ge(c);
        return A(Re, { scope: i.scope }, h);
      }
      return i.props ? Kt(i.props, l, c) : ge(c);
    };
  } });
}
function Kt(e, t, n) {
  return A(
    xs,
    { propsInfo: e, propsValue: t },
    () => ge(n)
  );
}
function ge(e) {
  const t = (e ?? []).map((n) => A(Q, {
    component: n
  }));
  return t.length <= 0 ? null : t;
}
function Ms(e, t) {
  const n = {}, r = [];
  return (e || []).forEach((o) => {
    const { sys: s, name: i, arg: c, value: l, mf: h } = o;
    if (i === "vmodel") {
      const a = t.getVueRefObject(l);
      if (n[`onUpdate:${c}`] = (u) => {
        a.value = u;
      }, s === 1) {
        const u = h ? Object.fromEntries(h.map((f) => [f, !0])) : {};
        r.push([Qn, a.value, void 0, u]);
      } else
        n[c] = a.value;
    } else if (i === "vshow") {
      const a = t.getVueRefObject(l);
      r.push([Yn, a.value]);
    } else
      console.warn(`Directive ${i} is not supported yet`);
  }), {
    newProps: n,
    directiveArray: r
  };
}
function Fs(e, t) {
  const { eRef: n } = e;
  return n === void 0 ? {} : { ref: t.getRef(n) };
}
function Bs(e) {
  const t = ne(), n = un(), r = e.component.props ?? {};
  return $e(r, !0), () => {
    const { tag: o } = e.component, s = N.IsBinding(o) ? t.getObjectToValue(o) : o, i = ft(s), c = typeof i == "string", l = Ts(e.component, t), { styles: h, hasStyle: a } = Is(e.component, t), u = Rs(e.component.events ?? {}, t), f = Ds(e.component, c), d = $s(e.component, r, t), { newProps: v, directiveArray: p } = Ms(
      e.component.dir,
      t
    ), g = Fs(
      e.component,
      n
    ), y = Xn({
      ...d,
      ...u,
      ...v,
      ...g
    }) || {};
    a && (y.style = h), l && (y.class = l);
    const _ = A(i, { ...y }, f);
    return p.length > 0 ? Zn(
      // @ts-ignore
      _,
      p
    ) : _;
  };
}
const Q = F(Bs, {
  props: ["component"]
});
function Dn(e, t) {
  var n, r;
  if (e) {
    const o = Er(e), s = on(e, ne(t)), i = ne(t);
    ys(e.py_watch, e.web_computed, i), (n = e.vue_watch) == null || n.forEach((c) => bs(c, i)), (r = e.js_watch) == null || r.forEach((c) => Ss(c, i)), xe(() => {
      cn(e.id, s), _r(e.id, o);
    });
  }
}
function Ls(e, { slots: t }) {
  const { scope: n } = e;
  return Dn(n), () => A(De, null, t.default());
}
const Re = F(Ls, {
  props: ["scope"]
}), Ws = F(
  (e) => {
    const { scope: t, items: n, vforInfo: r } = e;
    return Pr(r), Dn(t, r.key), n.length === 1 ? () => A(Q, {
      component: n[0]
    }) : () => n.map(
      (s) => A(Q, {
        component: s
      })
    );
  },
  {
    props: ["scope", "items", "vforInfo"]
  }
);
function Us(e, t) {
  const { state: n, isReady: r, isLoading: o } = hr(async () => {
    let s = e;
    const i = t;
    if (!s && !i)
      throw new Error("Either config or configUrl must be provided");
    if (!s && i && (s = await (await fetch(i)).json()), !s)
      throw new Error("Failed to load config");
    return s;
  }, {});
  return { config: n, isReady: r, isLoading: o };
}
function Ks(e, t) {
  let n;
  return t.component ? n = `Error captured from component:tag: ${t.component.tag} ; id: ${t.component.id} ` : n = "Error captured from app init", console.group(n), console.error("Component:", t.component), console.error("Error:", e), console.groupEnd(), !1;
}
const Gs = { class: "app-box" }, qs = {
  key: 0,
  style: { position: "absolute", top: "50%", left: "50%", transform: "translate(-50%, -50%)" }
}, Hs = /* @__PURE__ */ F({
  __name: "App",
  props: {
    config: {},
    configUrl: {}
  },
  setup(e) {
    const t = e, { config: n, isLoading: r } = Us(
      t.config,
      t.configUrl
    );
    let o = null;
    return G(n, (s) => {
      o = s, s.url && (ar({
        mode: s.mode,
        version: s.version,
        queryPath: s.url.path,
        pathParams: s.url.params,
        webServerInfo: s.webInfo
      }), gs(s));
    }), er(Ks), (s, i) => (he(), Ve("div", Gs, [
      W(r) ? (he(), Ve("div", qs, i[0] || (i[0] = [
        tr("p", { style: { margin: "auto" } }, "Loading ...", -1)
      ]))) : (he(), Ve("div", {
        key: 1,
        class: Ye(["insta-main", W(n).class])
      }, [
        nr(W(Re), {
          scope: W(o).scope
        }, {
          default: rr(() => [
            (he(!0), Ve(De, null, or(W(o).items, (c) => (he(), sr(W(Q), { component: c }, null, 8, ["component"]))), 256))
          ]),
          _: 1
        }, 8, ["scope"])
      ], 2))
    ]));
  }
});
function zs(e) {
  const { on: t, scope: n, items: r } = e, o = ne();
  return () => {
    const s = o.getObjectToValue(t);
    return A(Re, { scope: n }, () => s ? r.map(
      (c) => A(Q, { component: c })
    ) : void 0);
  };
}
const Js = F(zs, {
  props: ["on", "scope", "items"]
});
function Qs(e) {
  const { start: t = 0, end: n, step: r = 1 } = e;
  let o = [];
  if (r > 0)
    for (let s = t; s < n; s += r)
      o.push(s);
  else
    for (let s = t; s > n; s += r)
      o.push(s);
  return o;
}
function Ys(e) {
  const { array: t, bArray: n, items: r, fkey: o, fid: s, scope: i, num: c, tsGroup: l = {} } = e, h = t === void 0, a = c !== void 0, u = h ? n : t, f = ne();
  Vr(s, u, h, a);
  const v = ni(o ?? "index");
  return xe(() => {
    wr(i.id);
  }), () => {
    const p = Zs(
      a,
      h,
      u,
      f,
      c
    ), g = Ir(s), y = p.map((_, O) => {
      const R = v(_, O);
      return g.add(R), Nr(s, R, O), A(Ws, {
        scope: e.scope,
        items: r,
        vforInfo: {
          fid: s,
          key: R
        },
        key: R
      });
    });
    return g.removeUnusedKeys(), l && Object.keys(l).length > 0 ? A(Qt, l, {
      default: () => y
    }) : y;
  };
}
const Xs = F(Ys, {
  props: ["array", "items", "fid", "bArray", "scope", "num", "fkey", "tsGroup"]
});
function Zs(e, t, n, r, o) {
  if (e) {
    let i = 0;
    return typeof o == "number" ? i = o : i = r.getObjectToValue(o) ?? 0, Qs({
      end: Math.max(0, i)
    });
  }
  const s = t ? r.getObjectToValue(n) || [] : n;
  return typeof s == "object" ? Object.values(s) : s;
}
const ei = (e) => e, ti = (e, t) => t;
function ni(e) {
  const t = dr(e);
  return typeof t == "function" ? t : e === "item" ? ei : ti;
}
function ri(e) {
  return e.map((n) => {
    if (n.tag)
      return A(Q, { component: n });
    const r = ft(Mn);
    return A(r, {
      scope: n
    });
  });
}
const Mn = F(
  (e) => {
    const t = e.scope;
    return () => ri(t.items ?? []);
  },
  {
    props: ["scope"]
  }
);
function oi(e) {
  return e.map((t) => {
    if (t.tag)
      return A(Q, { component: t });
    const n = ft(Mn);
    return A(n, {
      scope: t
    });
  });
}
const si = F(
  (e) => {
    const { scope: t, on: n, items: r } = e, o = J(r), s = on(t), i = ne();
    return je.createDynamicWatchRefresh(n, i, async () => {
      const { items: c, on: l } = await je.fetchRemote(e, i);
      return o.value = c, l;
    }), xe(() => {
      cn(t.id, s);
    }), () => oi(o.value);
  },
  {
    props: ["sid", "url", "hKey", "on", "bind", "items", "scope"]
  }
);
var je;
((e) => {
  function t(r, o, s) {
    let i = null, c = r, l = c.map((a) => o.getVueRefObject(a));
    function h() {
      i && i(), i = G(
        l,
        async () => {
          c = await s(), l = c.map((a) => o.getVueRefObject(a)), h();
        },
        { deep: !0 }
      );
    }
    return h(), () => {
      i && i();
    };
  }
  e.createDynamicWatchRefresh = t;
  async function n(r, o) {
    const s = Object.values(r.bind).map((a) => ({
      sid: a.sid,
      id: a.id,
      value: o.getObjectToValue(a)
    })), i = {
      sid: r.sid,
      bind: s,
      hKey: r.hKey,
      page: ye()
    }, c = {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(i)
    }, l = await fetch(r.url, c);
    if (!l.ok)
      throw new Error("Failed to fetch data");
    return await l.json();
  }
  e.fetchRemote = n;
})(je || (je = {}));
function ii(e) {
  const { scope: t, items: n } = e;
  return () => {
    const r = n.map((o) => A(Q, { component: o }));
    return A(Re, { scope: t }, () => r);
  };
}
const Gt = F(ii, {
  props: ["scope", "items"]
});
function ai(e) {
  const { on: t, case: n, default: r } = e, o = ne();
  return () => {
    const s = o.getObjectToValue(t), i = n.map((c) => {
      const { value: l, items: h, scope: a } = c.props;
      if (s === l)
        return A(Gt, {
          scope: a,
          items: h,
          key: ["case", l].join("-")
        });
    }).filter((c) => c);
    if (r && !i.length) {
      const { items: c, scope: l } = r.props;
      i.push(A(Gt, { scope: l, items: c, key: "default" }));
    }
    return A(De, i);
  };
}
const ci = F(ai, {
  props: ["case", "on", "default"]
});
function ui(e, { slots: t }) {
  const { name: n = "fade", tag: r } = e;
  return () => A(
    Qt,
    { name: n, tag: r },
    {
      default: t.default
    }
  );
}
const li = F(ui, {
  props: ["name", "tag"]
});
function fi(e) {
  const { content: t, r: n = 0 } = e, r = ne(), o = n === 1 ? () => r.getObjectToValue(t) : () => t;
  return () => Jt(o());
}
const hi = F(fi, {
  props: ["content", "r"]
});
function di(e) {
  if (!e.router)
    throw new Error("Router config is not provided.");
  const { routes: t, kAlive: n = !1 } = e.router;
  return t.map(
    (o) => Fn(o, n)
  );
}
function Fn(e, t) {
  var l;
  const { server: n = !1, vueItem: r, scope: o } = e, s = () => {
    if (n)
      throw new Error("Server-side rendering is not supported yet.");
    return Promise.resolve(pi(r, o, t));
  }, i = (l = r.children) == null ? void 0 : l.map(
    (h) => Fn(h, t)
  ), c = {
    ...r,
    children: i,
    component: s
  };
  return r.component.length === 0 && delete c.component, i === void 0 && delete c.children, c;
}
function pi(e, t, n) {
  const { path: r, component: o } = e, s = A(
    Re,
    { scope: t, key: r },
    () => o.map((c) => A(Q, { component: c }))
  );
  return n ? A(ir, null, () => s) : s;
}
function mi(e, t) {
  const { mode: n = "hash" } = t.router, r = n === "hash" ? Eo() : n === "memory" ? wo() : Rn();
  e.use(
    ls({
      history: r,
      routes: di(t)
    })
  );
}
function yi(e, t) {
  e.component("insta-ui", Hs), e.component("vif", Js), e.component("vfor", Xs), e.component("match", ci), e.component("refresh", si), e.component("ts-group", li), e.component("content", hi), t.router && mi(e, t);
}
export {
  $e as convertDynamicProperties,
  yi as install
};
//# sourceMappingURL=insta-ui.js.map
