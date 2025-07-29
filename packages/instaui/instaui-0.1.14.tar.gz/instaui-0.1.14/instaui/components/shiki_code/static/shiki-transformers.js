const M = [
  [/^(<!--)(.+)(-->)$/, !1],
  [/^(\/\*)(.+)(\*\/)$/, !1],
  [/^(\/\/|["'#]|;{1,2}|%{1,2}|--)(.*)$/, !0],
  /**
   * for multi-line comments like this
   */
  [/^(\*)(.+)$/, !0]
];
function b(t, i, e) {
  const r = [];
  for (const n of t) {
    if (e === "v3") {
      const o = n.children.flatMap((a, l) => {
        if (a.type !== "element")
          return a;
        const h = a.children[0];
        if (h.type !== "text")
          return a;
        const f = l === n.children.length - 1;
        if (!k(h.value, f))
          return a;
        const d = h.value.split(/(\s+\/\/)/);
        if (d.length <= 1)
          return a;
        let m = [d[0]];
        for (let g = 1; g < d.length; g += 2)
          m.push(d[g] + (d[g + 1] || ""));
        return m = m.filter(Boolean), m.length <= 1 ? a : m.map((g) => ({
          ...a,
          children: [
            {
              type: "text",
              value: g
            }
          ]
        }));
      });
      o.length !== n.children.length && (n.children = o);
    }
    const s = n.children;
    let c = s.length - 1;
    e === "v1" ? c = 0 : i && (c = s.length - 2);
    for (let o = Math.max(c, 0); o < s.length; o++) {
      const a = s[o];
      if (a.type !== "element")
        continue;
      const l = a.children.at(0);
      if ((l == null ? void 0 : l.type) !== "text")
        continue;
      const h = o === s.length - 1, f = k(l.value, h);
      if (f)
        if (i && !h && o !== 0) {
          const u = x(s[o - 1], "{") && x(s[o + 1], "}");
          r.push({
            info: f,
            line: n,
            token: a,
            isLineCommentOnly: s.length === 3 && a.children.length === 1,
            isJsxStyle: u
          });
        } else
          r.push({
            info: f,
            line: n,
            token: a,
            isLineCommentOnly: s.length === 1 && a.children.length === 1,
            isJsxStyle: !1
          });
    }
  }
  return r;
}
function x(t, i) {
  if (t.type !== "element")
    return !1;
  const e = t.children[0];
  return e.type !== "text" ? !1 : e.value.trim() === i;
}
function k(t, i) {
  let e = t.trimStart();
  const r = t.length - e.length;
  e = e.trimEnd();
  const n = t.length - e.length - r;
  for (const [s, c] of M) {
    if (c && !i)
      continue;
    const o = s.exec(e);
    if (o)
      return [
        " ".repeat(r) + o[1],
        o[2],
        o[3] ? o[3] + " ".repeat(n) : void 0
      ];
  }
}
function N(t) {
  const i = t.match(/(?:\/\/|["'#]|;{1,2}|%{1,2}|--)(\s*)$/);
  return i && i[1].trim().length === 0 ? t.slice(0, i.index) : t;
}
function C(t, i, e, r) {
  return r == null && (r = "v3"), {
    name: t,
    code(n) {
      const s = n.children.filter((l) => l.type === "element"), c = [];
      n.data ?? (n.data = {});
      const o = n.data;
      o._shiki_notation ?? (o._shiki_notation = b(s, ["jsx", "tsx"].includes(this.options.lang), r));
      const a = o._shiki_notation;
      for (const l of a) {
        if (l.info[1].length === 0)
          continue;
        let h = s.indexOf(l.line);
        l.isLineCommentOnly && r !== "v1" && h++;
        let f = !1;
        if (l.info[1] = l.info[1].replace(i, (...d) => e.call(this, d, l.line, l.token, s, h) ? (f = !0, "") : d[0]), !f)
          continue;
        r === "v1" && (l.info[1] = N(l.info[1]));
        const u = l.info[1].trim().length === 0;
        if (u && (l.info[1] = ""), u && l.isLineCommentOnly)
          c.push(l.line);
        else if (u && l.isJsxStyle)
          l.line.children.splice(l.line.children.indexOf(l.token) - 1, 3);
        else if (u)
          l.line.children.splice(l.line.children.indexOf(l.token), 1);
        else {
          const d = l.token.children[0];
          d.type === "text" && (d.value = l.info.join(""));
        }
      }
      for (const l of c) {
        const h = n.children.indexOf(l), f = n.children[h + 1];
        let u = 1;
        (f == null ? void 0 : f.type) === "text" && (f == null ? void 0 : f.value) === `
` && (u = 2), n.children.splice(h, u);
      }
    }
  };
}
function _(t) {
  if (!t)
    return null;
  const i = t.match(/\{([\d,-]+)\}/);
  return i ? i[1].split(",").flatMap((r) => {
    const n = r.split("-").map((s) => Number.parseInt(s, 10));
    return n.length === 1 ? [n[0]] : Array.from({ length: n[1] - n[0] + 1 }, (s, c) => c + n[0]);
  }) : null;
}
const v = Symbol("highlighted-lines");
function R(t = {}) {
  const {
    className: i = "highlighted"
  } = t;
  return {
    name: "@shikijs/transformers:meta-highlight",
    line(e, r) {
      var c;
      if (!((c = this.options.meta) != null && c.__raw))
        return;
      const n = this.meta;
      return n[v] ?? (n[v] = _(this.options.meta.__raw)), (n[v] ?? []).includes(r) && this.addClassToHast(e, i), e;
    }
  };
}
function j(t) {
  return t ? Array.from(t.matchAll(/\/((?:\\.|[^/])+)\//g)).map((e) => e[1].replace(/\\(.)/g, "$1")) : [];
}
function W(t = {}) {
  const {
    className: i = "highlighted-word"
  } = t;
  return {
    name: "@shikijs/transformers:meta-word-highlight",
    preprocess(e, r) {
      var s;
      if (!((s = this.options.meta) != null && s.__raw))
        return;
      const n = j(this.options.meta.__raw);
      r.decorations || (r.decorations = []);
      for (const c of n) {
        const o = O(e, c);
        for (const a of o)
          r.decorations.push({
            start: a,
            end: a + c.length,
            properties: {
              class: i
            }
          });
      }
    }
  };
}
function O(t, i) {
  const e = [];
  let r = 0;
  for (; ; ) {
    const n = t.indexOf(i, r);
    if (n === -1 || n >= t.length || n < r)
      break;
    e.push(n), r = n + i.length;
  }
  return e;
}
function w(t) {
  return t.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}
function y(t = {}, i = "@shikijs/transformers:notation-map") {
  const {
    classMap: e = {},
    classActivePre: r = void 0
  } = t;
  return C(
    i,
    new RegExp(`\\s*\\[!code (${Object.keys(e).map(w).join("|")})(:\\d+)?\\]`),
    function([n, s, c = ":1"], o, a, l, h) {
      const f = Number.parseInt(c.slice(1), 10);
      for (let u = h; u < Math.min(h + f, l.length); u++)
        this.addClassToHast(l[u], e[s]);
      return r && this.addClassToHast(this.pre, r), !0;
    },
    t.matchAlgorithm
  );
}
function B(t = {}) {
  const {
    classLineAdd: i = "diff add",
    classLineRemove: e = "diff remove",
    classActivePre: r = "has-diff"
  } = t;
  return y(
    {
      classMap: {
        "++": i,
        "--": e
      },
      classActivePre: r,
      matchAlgorithm: t.matchAlgorithm
    },
    "@shikijs/transformers:notation-diff"
  );
}
function J(t = {}) {
  const {
    classMap: i = {
      error: ["highlighted", "error"],
      warning: ["highlighted", "warning"]
    },
    classActivePre: e = "has-highlighted"
  } = t;
  return y(
    {
      classMap: i,
      classActivePre: e,
      matchAlgorithm: t.matchAlgorithm
    },
    "@shikijs/transformers:notation-error-level"
  );
}
function F(t = {}) {
  const {
    classActiveLine: i = "focused",
    classActivePre: e = "has-focused"
  } = t;
  return y(
    {
      classMap: {
        focus: i
      },
      classActivePre: e,
      matchAlgorithm: t.matchAlgorithm
    },
    "@shikijs/transformers:notation-focus"
  );
}
function D(t = {}) {
  const {
    classActiveLine: i = "highlighted",
    classActivePre: e = "has-highlighted"
  } = t;
  return y(
    {
      classMap: {
        highlight: i,
        hl: i
      },
      classActivePre: e,
      matchAlgorithm: t.matchAlgorithm
    },
    "@shikijs/transformers:notation-highlight"
  );
}
function T(t, i, e, r) {
  const n = A(t);
  let s = n.indexOf(e);
  for (; s !== -1; )
    H.call(this, t.children, i, s, e.length, r), s = n.indexOf(e, s + 1);
}
function A(t) {
  return t.type === "text" ? t.value : t.type === "element" && t.tagName === "span" ? t.children.map(A).join("") : "";
}
function H(t, i, e, r, n) {
  let s = 0;
  for (let c = 0; c < t.length; c++) {
    const o = t[c];
    if (o.type !== "element" || o.tagName !== "span" || o === i)
      continue;
    const a = o.children[0];
    if (a.type === "text") {
      if (L([s, s + a.value.length - 1], [e, e + r])) {
        const l = Math.max(0, e - s), h = r - Math.max(0, s - e);
        if (h === 0)
          continue;
        const f = S(o, a, l, h);
        this.addClassToHast(f[1], n);
        const u = f.filter(Boolean);
        t.splice(c, 1, ...u), c += u.length - 1;
      }
      s += a.value.length;
    }
  }
}
function L(t, i) {
  return t[0] <= i[1] && t[1] >= i[0];
}
function S(t, i, e, r) {
  const n = i.value, s = (c) => E(t, {
    children: [
      {
        type: "text",
        value: c
      }
    ]
  });
  return [
    e > 0 ? s(n.slice(0, e)) : void 0,
    s(n.slice(e, e + r)),
    e + r < n.length ? s(n.slice(e + r)) : void 0
  ];
}
function E(t, i) {
  return {
    ...t,
    properties: {
      ...t.properties
    },
    ...i
  };
}
function V(t = {}) {
  const {
    classActiveWord: i = "highlighted-word",
    classActivePre: e = void 0
  } = t;
  return C(
    "@shikijs/transformers:notation-highlight-word",
    /\s*\[!code word:((?:\\.|[^:\]])+)(:\d+)?\]/,
    function([r, n, s], c, o, a, l) {
      const h = s ? Number.parseInt(s.slice(1), 10) : a.length;
      n = n.replace(/\\(.)/g, "$1");
      for (let f = l; f < Math.min(l + h, a.length); f++)
        T.call(this, a[f], o, n, i);
      return e && this.addClassToHast(this.pre, e), !0;
    },
    t.matchAlgorithm
  );
}
function q() {
  return {
    name: "@shikijs/transformers:remove-line-break",
    code(t) {
      t.children = t.children.filter((i) => !(i.type === "text" && i.value === `
`));
    }
  };
}
function $(t) {
  return t === "	";
}
function p(t) {
  return t === " " || t === "	";
}
function I(t) {
  const i = [];
  let e = "";
  function r() {
    e.length && i.push(e), e = "";
  }
  return t.forEach((n, s) => {
    $(n) || p(n) && (p(t[s - 1]) || p(t[s + 1])) ? (r(), i.push(n)) : e += n;
  }), r(), i;
}
function P(t, i, e = !0) {
  if (i === "all")
    return t;
  let r = 0, n = 0;
  if (i === "boundary")
    for (let c = 0; c < t.length && p(t[c]); c++)
      r++;
  if (i === "boundary" || i === "trailing")
    for (let c = t.length - 1; c >= 0 && p(t[c]); c--)
      n++;
  const s = t.slice(r, t.length - n);
  return [
    ...t.slice(0, r),
    ...e ? I(s) : [s.join("")],
    ...t.slice(t.length - n)
  ];
}
function z(t = {}) {
  const i = {
    " ": t.classSpace ?? "space",
    "	": t.classTab ?? "tab"
  }, e = t.position ?? "all", r = Object.keys(i);
  return {
    name: "@shikijs/transformers:render-whitespace",
    // We use `root` hook here to ensure it runs after all other transformers
    root(n) {
      n.children[0].children[0].children.forEach(
        (o) => {
          if (o.type !== "element")
            return;
          const a = o.children.filter((h) => h.type === "element"), l = a.length - 1;
          o.children = o.children.flatMap((h) => {
            if (h.type !== "element")
              return h;
            const f = a.indexOf(h);
            if (e === "boundary" && f !== 0 && f !== l || e === "trailing" && f !== l)
              return h;
            const u = h.children[0];
            if (u.type !== "text" || !u.value)
              return h;
            const d = P(
              u.value.split(/([ \t])/).filter((m) => m.length),
              e === "boundary" && f === l && l !== 0 ? "trailing" : e,
              e !== "trailing"
            );
            return d.length <= 1 ? h : d.map((m) => {
              const g = {
                ...h,
                properties: { ...h.properties }
              };
              return g.children = [{ type: "text", value: m }], r.includes(m) && (this.addClassToHast(g, i[m]), delete g.properties.style), g;
            });
          });
        }
      );
    }
  };
}
export {
  R as transformerMetaHighlight,
  W as transformerMetaWordHighlight,
  B as transformerNotationDiff,
  J as transformerNotationErrorLevel,
  F as transformerNotationFocus,
  D as transformerNotationHighlight,
  V as transformerNotationWordHighlight,
  q as transformerRemoveLineBreak,
  z as transformerRenderWhitespace
};
