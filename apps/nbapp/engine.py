"""Run a course Colab notebook outside Colab: load it, execute its set-up cell in a private namespace,
and re-run any code cell with new form values, capturing figures, displayed Markdown/HTML and printed text.

One Session per browser connection, so each student's answers, report and settings are separate.
"""
import ast, base64, contextlib, io, json, re, sys, types

import numpy  # noqa: F401  (the notebooks use numpy; listed so Shinylive bundles it)
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ---------------------------------------------------------------- stand-ins for IPython / ipywidgets
_SHOWN = []          # display() calls during the current cell run


def _install_stubs():
    """The notebooks call IPython.display and ipywidgets; give them stand-ins that record output."""
    disp = types.ModuleType("IPython.display")
    disp.display = lambda *a, **k: _SHOWN.extend(a)
    disp.Markdown = lambda s: ("md", s)
    disp.HTML = lambda s: ("html", s)
    disp.Javascript = lambda s: ("js", s)
    disp.Image = lambda *a, **k: ("img", k.get("data") or (a[0] if a else b""))
    disp.clear_output = lambda *a, **k: None
    ip = types.ModuleType("IPython")
    ip.display = disp
    ip.version_info = (9, 0, 0)
    ip.get_ipython = lambda: None
    sys.modules["IPython"] = ip
    sys.modules["IPython.display"] = disp

    w = types.ModuleType("ipywidgets")

    class _Style(dict):
        def __getattr__(s, k): return s.get(k)
        def __setattr__(s, k, v): s[k] = v

    class Layout(_Style):
        def __init__(s, **k): super().__init__(**k)

    class _W:
        def __init__(s, *a, **k):
            s.children = list(a[0]) if a and isinstance(a[0], (list, tuple)) else k.get("children", [])
            s.__dict__.update({x: y for x, y in k.items() if x != "children"})
            s.style, s.layout, s._cb = _Style(), k.get("layout") or Layout(), []
            s.value = k.get("value", "")
        def on_click(s, f): s._cb.append(f)
        def observe(s, *a, **k): pass
        def clear_output(s, *a, **k): pass
        def __enter__(s): return s
        def __exit__(s, *a): return False

    w.Layout = Layout
    for n in ("Button", "HTML", "Text", "Textarea", "FloatText", "IntText", "Dropdown", "Output", "VBox", "HBox",
              "GridBox", "Label", "Checkbox", "FloatSlider", "IntSlider", "ToggleButtons", "Tab", "Accordion"):
        setattr(w, n, type(n, (_W,), {}))
    sys.modules["ipywidgets"] = w


_install_stubs()

# ---------------------------------------------------------------- notebook parsing
PARAM = re.compile(r"^(\s*)(\w+)\s*=\s*(.+?)\s*#@param\s*(.*)$", re.M)


def src(c):
    return "".join(c["source"]) if isinstance(c["source"], list) else c["source"]


def title_of(s):
    m = re.match(r"#@title\s+(.+?)(\{|$)", s.split("\n")[0])
    return m.group(1).strip() if m else ""


def form_markdown(s):
    """The #@markdown lines of a form cell (instructions shown above the controls)."""
    t = "\n".join(l[len("#@markdown"):].strip() for l in s.split("\n") if l.startswith("#@markdown")
                   and l.strip() != "#@markdown ---")
    # in the app the output refreshes as soon as a control moves; there is no play button
    t = re.sub(r",?\s*(then|and)\s+press (the )?play( button)?\.?", ". The output updates as you change a setting.", t)
    return re.sub(r"(?i)press (the )?play( button)?\.?", "The output updates as you change a setting.", t)


def parse_params(s):
    """[(name, default, spec)] for every `name = default  #@param spec` line.
    spec kind: slider | number | integer | string | boolean | choice."""
    out = []
    for m in PARAM.finditer(s):
        name, raw, spec = m.group(2), m.group(3), m.group(4)
        try:
            default = ast.literal_eval(raw)
        except Exception:
            default = raw.strip("\"'")
        p = dict(name=name, default=default, kind="string")
        if spec.startswith("["):
            lst = spec[:spec.index("]") + 1]
            try:
                p["choices"] = ast.literal_eval(lst)
            except Exception:
                p["choices"] = [x.strip().strip("\"'") for x in lst[1:-1].split(",")]
            p["kind"] = "choice"
        else:
            t = re.search(r'type:\s*"(\w+)"', spec)
            t = t.group(1) if t else ("number" if isinstance(default, (int, float)) else "string")
            p["kind"] = t
            if t == "slider":
                for k in ("min", "max", "step"):
                    mm = re.search(r"%s:\s*(-?[\d.]+)" % k, spec)
                    if mm:
                        p[k] = float(mm.group(1))
        out.append(p)
    return out


def with_values(s, values):
    """The cell source with each #@param line set to the given value."""
    def rep(m):
        name = m.group(2)
        if name in values:
            return "%s%s = %r" % (m.group(1), name, values[name])
        return m.group(0)
    return PARAM.sub(rep, s)


# ---------------------------------------------------------------- a student's session
class Session:
    def __init__(self, nb_path):
        self.nb = json.load(open(nb_path, encoding="utf-8"))
        self.cells = self.nb["cells"]
        self.ns = {"__name__": "__main__"}
        setup = next(c for c in self.cells if c["cell_type"] == "code" and
                     ("Set-up" in src(c).split("\n")[0] or title_of(src(c)).startswith("0.1")))
        self.setup_output = self.run(src(setup))

    @property
    def gb(self):
        return self.ns.get("gb")

    @property
    def cards(self):
        return self.ns.get("CARDS") or {}

    def run(self, code):
        """Execute code in the session namespace; return {'figures': [png bytes], 'shown': [...], 'stdout': str, 'error': str}."""
        _SHOWN.clear()
        figs = []

        def _show(*a, **k):
            for num in plt.get_fignums():
                f = plt.figure(num)
                rep = self.ns.get("REPORT")
                if rep is not None:
                    try:
                        rep.add_figure(f)
                    except Exception:
                        pass
                b = io.BytesIO()
                f.savefig(b, format="png", dpi=110, bbox_inches="tight", facecolor="white")
                figs.append(b.getvalue())
            plt.close("all")

        plt.show = _show
        import matplotlib.pyplot as _p2
        _p2.show = _show
        out, err = io.StringIO(), ""
        with contextlib.redirect_stdout(out):
            try:
                exec(compile(code, "<cell>", "exec"), self.ns)
            except Exception as e:
                err = "%s: %s" % (type(e).__name__, e)
        if plt.get_fignums():
            _show()
        shown = []
        for o in list(_SHOWN):
            if isinstance(o, tuple) and len(o) == 2 and o[0] in ("md", "html"):
                shown.append(o)
            elif isinstance(o, str):
                shown.append(("md", o))
        return dict(figures=figs, shown=shown, stdout=out.getvalue(), error=err)


def png_uri(b):
    return "data:image/png;base64," + base64.b64encode(b).decode()
