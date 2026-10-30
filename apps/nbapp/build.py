"""Build a Shiny for Python app from a course notebook: one tab per notebook Part, holding its interactive
tools, figures, calculation cards and concept checks; plus a results/report tab.

    from nbapp import make_app
    app = make_app("notebooks/PHS312_L23_Conformational_Analysis_I.ipynb")
"""
import html, json, os, re, sys

from markdown_it import MarkdownIt
from shiny import App, reactive, render, ui

from .engine import Session, form_markdown, parse_params, png_uri, src, title_of, with_values

HERE = os.path.dirname(os.path.abspath(__file__))
WWW = os.path.join(os.path.dirname(HERE), "www")
_md = MarkdownIt("commonmark", {"html": True}).enable("table")


# ---------------------------------------------------------------- markdown with math kept for KaTeX
def md(s):
    if not s:
        return ui.HTML("")
    keep = []

    def stash(m):
        keep.append(m.group(0))
        return "\u0001%d\u0002" % (len(keep) - 1)
    s = re.sub(r"\$\$.+?\$\$", stash, s, flags=re.S)
    s = re.sub(r"(?<![\\$])\$(?!\s)[^$\n]+?(?<!\s)\$", stash, s)
    s = s.replace("<details>", '<details class="nbdetails">')
    h = _md.render(s)
    h = re.sub("\u0001(\\d+)\u0002", lambda m: html.escape(keep[int(m.group(1))], quote=False), h)
    return ui.HTML(h)


def output_html(r):
    """Captured cell output → HTML (displayed Markdown/HTML, figures, printed text, errors)."""
    parts = []
    for kind, text in r["shown"]:
        parts.append(str(md(text)) if kind == "md" else text)
    for b in r["figures"]:
        parts.append('<img class="nbfig" src="%s">' % png_uri(b))
    if r["stdout"].strip():
        parts.append('<pre class="nbout">%s</pre>' % html.escape(r["stdout"].rstrip()))
    if r["error"]:
        parts.append('<div class="nberr">This cell stopped with <code>%s</code>. Check the settings above; '
                     'if a setting is blank or out of range, change it and the output will refresh.</div>' % html.escape(r["error"]))
    return ui.HTML("\n".join(parts))


# ---------------------------------------------------------------- notebook → structure
def structure(nb_path):
    nb = json.load(open(nb_path, encoding="utf-8"))
    cells = nb["cells"]
    title = src(next(c for c in cells if c["cell_type"] == "markdown")).split("\n")[0].lstrip("# ").strip()
    parts, cur = [], None
    for i, c in enumerate(cells):
        s = src(c)
        if c["cell_type"] == "markdown":
            if c.get("metadata", {}).get("card"):
                if cur is not None:
                    cur["items"].append(("card", c["metadata"]["card"], i))
                continue
            m = re.match(r"## (.+)", s)
            if m:
                head = m.group(1).strip()
                if re.match(r"(Lab report|Your results)", head):
                    cur = None
                    continue
                cur = dict(title=re.sub(r"^Part\s+", "", head), md=[s.split("\n", 1)[1] if "\n" in s else ""],
                           slos=c.get("metadata", {}).get("slos", []), items=[], idx=i)
                parts.append(cur)
            elif cur is not None:
                cur["md"].append(s)
            continue
        first = s.split("\n")[0]
        if "Set-up" in first or title_of(s).startswith("0.1") or cur is None:
            continue
        if re.search(r'gb\.answer\("([\w-]+)"', s):
            cur["items"].append(("question", re.search(r'gb\.answer\("([\w-]+)"', s).group(1), i))
        elif re.search(r"^(card\(|report_panel\(\))", s, re.M):
            continue                                   # cards are shown from their markdown cell
        elif "gb.summary" in s:
            continue
        else:
            cur["items"].append(("tool" if parse_params(s) else "static", s, i))
    return title, cells, parts


# ---------------------------------------------------------------- the app
CSS = """
body{background:#f6f8fb;color:#16202b}
.apphead{background:#0b4f6c;color:#fff;padding:14px 22px;margin:0 -12px 14px}
.apphead h1{font-size:1.45rem;margin:0}.apphead .sub{opacity:.85;font-size:.92rem}
.nbtool,.nbq,.nbcard{background:#fff;border:1px solid #d7e0ea;border-radius:8px;padding:12px 16px;margin:12px 0}
.nbtool h4,.nbcard h4{font-size:1.02rem;color:#0b4f6c;margin:0 0 6px}
.nbq{border-color:#f1b9a3;background:#fffaf7}.nbq h4{font-size:1rem;color:#c2410c;margin:0 0 4px}
.nbcard{border-color:#e9b44c;background:#fffdf7}
.nbfig{max-width:100%;height:auto;display:block;margin:8px auto}
pre.nbout{background:#f8fafc;border:1px dashed #cbd5e1;padding:8px;font-size:.82rem;white-space:pre-wrap}
.nberr{color:#b91c1c;font-size:.9rem}
.chip{display:inline-block;font-size:.72rem;font-weight:600;color:#c2410c;border:1px solid #c2410c;border-radius:9px;padding:0 6px;margin-left:6px}
.fb{margin-top:8px;font-size:.93rem}
table{border-collapse:collapse;margin:6px 0}td,th{border:1px solid #cbd5e1;padding:3px 7px;font-size:.88rem;vertical-align:top}
th{background:#eef4fb}
.nav-pills .nav-link{text-align:left;font-size:.9rem;padding:6px 10px}
.nav-pills .nav-link.active{background:#0b4f6c}
details.nbdetails{background:#f4f7fa;border:1px solid #cbd5e1;border-radius:6px;padding:4px 10px;margin:6px 0}
"""

IN_BROWSER = sys.platform == "emscripten"       # Shinylive: Python running inside the student's browser
_KX = "https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/" if IN_BROWSER else ""
KATEX_JS = """
<link rel="stylesheet" href="@@KX@@katex.min.css">
<script src="@@KX@@katex.min.js"></script>
<script src="@@KX@@contrib/auto-render.min.js"></script>
<script>
function nbMath(el){ try{ renderMathInElement(el||document.body,{delimiters:[{left:'$$',right:'$$',display:true},
 {left:'$',right:'$',display:false}],throwOnError:false,trust:true}); }catch(e){} }
document.addEventListener('DOMContentLoaded',()=>nbMath());
$(document).on('shiny:value', e => setTimeout(()=>nbMath(e.target), 30));
$(document).on('shown.bs.tab', e => nbMath());
</script>
""".replace("@@KX@@", _KX if IN_BROWSER else "katex/")


def chip(slos):
    return ui.span(" · ".join(slos), class_="chip") if slos else ""


def make_app(nb_path, course=""):
    title, cells, parts = structure(nb_path)
    probe = Session(nb_path)                 # read item bank and cards once to lay out the page
    items, cards = probe.gb.items if probe.gb else {}, probe.cards

    def q_ui(qid, i):
        it = items[qid]
        opts = it.options if isinstance(it.options, dict) else {k: v for k, v in zip("ABCD", it.options)}
        choices = {"none": "(choose an answer)"}
        choices.update({L: ui.HTML(str(md("**%s.** %s" % (L, t)))[3:-5]) for L, t in sorted(opts.items())})
        sec = {"precheck": "Readiness (no feedback, by design)", "post": "End-of-activity assessment"}.get(it.section, "Concept check")
        return ui.div(ui.h4("%s · %s" % (qid, sec)), md(it.stem),
                      ui.input_radio_buttons("q_%d" % i, None, choices, selected="none", width="100%"),
                      ui.input_action_button("qb_%d" % i, "Check my answer", class_="btn-sm btn-outline-danger"),
                      ui.output_ui("qo_%d" % i), class_="nbq")

    def card_ui(cid, i):
        c = cards.get(cid)
        if c is None:
            return ui.div("Card %s not found." % cid, class_="nbcard")
        boxes = [ui.input_numeric("cv_%d_%s" % (i, k), "%s (%s)" % (c.V[k].name, c.V[k].unit or "–"),
                                  value=c.V[k].value, width="100%") for k in c.inputs]
        return ui.div(ui.h4("Calculation card · " + c.title), md(c.md_equation()), md(c.md_case()),
                      ui.p(ui.em("Work it on paper first, then enter the case values (or your own) and solve."), class_="small"),
                      ui.layout_columns(*boxes, col_widths=[6] * len(boxes)) if boxes else "",
                      ui.input_action_button("cb_%d" % i, "Solve step by step", class_="btn-sm btn-success"),
                      ui.output_ui("co_%d" % i), class_="nbcard")

    def param_input(i, p):
        iid = "p_%d_%s" % (i, p["name"])
        lab = p["name"].replace("_", " ")
        k = p["kind"]
        if k == "slider":
            return ui.input_slider(iid, lab, min=p.get("min", 0), max=p.get("max", 100), value=p["default"], step=p.get("step", 1))
        if k == "boolean":
            return ui.input_checkbox(iid, lab, value=bool(p["default"]))
        if k == "choice":
            ch = {str(x): str(x) for x in p["choices"]}
            return ui.input_select(iid, lab, ch, selected=str(p["default"]))
        if k in ("number", "integer"):
            return ui.input_numeric(iid, lab, value=p["default"])
        return ui.input_text(iid, lab, value=str(p["default"]))

    def tool_ui(code, i):
        t = title_of(code) or "Tool"
        ps = parse_params(code)
        return ui.div(ui.h4(t), md(form_markdown(code)),
                      ui.layout_columns(*[param_input(i, p) for p in ps], col_widths=[4] * len(ps)),
                      ui.output_ui("to_%d" % i), class_="nbtool")

    def static_ui(code, i):
        return ui.div(ui.h4(title_of(code) or "Output"), ui.output_ui("to_%d" % i), class_="nbtool")

    panels = []
    for p in parts:
        body = [ui.h3(p["title"], chip(p["slos"]))]
        txt = "\n\n".join(x for x in p["md"] if x.strip())
        if p["title"].lower().startswith("learning objectives"):
            body.append(md(txt))
        elif txt.strip():
            body.append(ui.accordion(ui.accordion_panel("Background from the notebook", md(txt)), open=False))
        for kind, x, i in p["items"]:
            body.append({"question": q_ui, "card": card_ui, "tool": tool_ui, "static": static_ui}[kind](x, i))
        if len(body) > 1:
            panels.append(ui.nav_panel(re.sub(r"\s*[-—–]\s*", " · ", p["title"], count=1), *body))
    panels.append(ui.nav_panel(
        "Results and lab report",
        ui.h3("Your results"),
        ui.input_action_button("summary", "Show my performance and report code", class_="btn-primary"),
        ui.output_ui("summary_out"),
        ui.hr(), ui.h3("Lab report"),
        ui.p("Every figure you displayed, every card you solved and your first answer to each check were collected. "
             "Add your name and a short discussion, then download."),
        ui.input_text("rep_name", "Your name", width="420px"),
        ui.input_text_area("rep_notes", "Discussion", width="100%", rows=4),
        ui.download_button("rep_docx", "Download report (.docx)", class_="btn-success"),
        " ", ui.download_button("rep_html", "Download report (.html)")))

    app_ui = ui.page_fluid(
        ui.head_content(ui.tags.style(CSS), ui.HTML(KATEX_JS)),
        ui.div(ui.h1(title), ui.div(course + " · interactive version of the Colab notebook · " + ("runs in your browser; nothing is sent anywhere" if IN_BROWSER else "runs on this computer"), class_="sub"),
               class_="apphead"),
        ui.navset_pill_list(*panels, widths=(2, 10)),
        title=title)

    # ------------------------------------------------------------ server
    def server(input, output, session):
        S = Session(nb_path)
        all_items = [it for p in parts for it in p["items"]]
        # "Run all" once, in notebook order, so a cell that uses an earlier cell's results works whichever
        # tab a student opens first. Figures from this pass are not added to the student's report.
        static_res, seen = {}, set()
        rep, S.ns["REPORT"] = S.ns.get("REPORT"), None
        for kind, x, i in all_items:
            if kind == "static":
                static_res[i] = S.run(x)
            elif kind == "tool":
                S.run(x)
        S.ns["REPORT"] = rep

        def bind_tool(code, i):
            ps = parse_params(code)

            def f():
                vals = {}
                for p in ps:
                    v = input["p_%d_%s" % (i, p["name"])]()
                    if p["kind"] == "choice":
                        orig = {str(x): x for x in p["choices"]}
                        v = orig.get(v, v)
                    elif p["kind"] == "integer" and v is not None:
                        v = int(v)
                    elif p["kind"] == "slider" and float(v).is_integer() and isinstance(p["default"], int):
                        v = int(v)
                    vals[p["name"]] = v
                return output_html(S.run(with_values(code, vals)))
            output(render.ui(f), id="to_%d" % i)

        def bind_static(code, i):
            def f():
                if i not in static_res:
                    static_res[i] = S.run(code)
                rep_ = S.ns.get("REPORT")              # the student has now seen this figure: add it to the report once
                if rep_ is not None and i not in seen:
                    seen.add(i)
                    for png in static_res[i]["figures"]:
                        rep_.entries.append(dict(kind="figure", section=getattr(rep_, "section", ""),
                                                 title=title_of(code) or "Figure", png=png))
                return output_html(static_res[i])
            output(render.ui(f), id="to_%d" % i)

        def bind_q(qid, i):
            def f():
                input["qb_%d" % i]()
                with reactive.isolate():
                    ch = input["q_%d" % i]()
                if not input["qb_%d" % i]():
                    return ""
                if not ch or ch == "none":
                    return ui.div("Choose an option first.", class_="fb")
                r = S.run('gb.answer(%r, %r)' % (qid, ch))
                txt = "\n".join(l for l in r["stdout"].splitlines() if not re.match(r"^\s*[-=]{8,}\s*$", l)).strip()
                body = "".join(str(md(t)) for k, t in r["shown"] if k == "md") + (str(md(txt)) if txt else "")
                return ui.div(ui.HTML(body or "Answer recorded."), class_="fb")
            output(render.ui(f), id="qo_%d" % i)

        def bind_card(cid, i):
            c = S.cards.get(cid)

            def f():
                if not input["cb_%d" % i]():
                    return ""
                with reactive.isolate():
                    vals = {k: input["cv_%d_%s" % (i, k)]() for k in c.inputs}
                if any(v is None for v in vals.values()):
                    return ui.div("Fill in every value first.", class_="fb")
                try:
                    sol = c.solve(**vals)
                except (ValueError, ZeroDivisionError) as e:
                    return ui.div("Check the inputs: %s" % e, class_="nberr")
                rep = S.ns.get("REPORT")
                if rep is not None:
                    rep.add_calc(c, sol)
                changed = any(abs((vals[k] or 0) - (c.V[k].value or 0)) > 1e-12 for k in vals)
                return md((c.md_case(vals).replace("2. Practice problem (case)", "Your values") + "\n\n" if changed else "")
                          + "**3. Step-by-step solution**\n\n" + sol.markdown())
            output(render.ui(f), id="co_%d" % i)

        for kind, x, i in all_items:
            {"tool": bind_tool, "static": bind_static, "question": bind_q,
             "card": lambda cid, i: bind_card(cid, i) if S.cards.get(cid) else None}[kind](x, i)

        @render.ui
        def summary_out():
            if not input.summary():
                return ""
            r = S.run("gb.summary()\nprint()\n_ = gb.report_code()")
            return output_html(r)

        def _report():
            rep = S.ns.get("REPORT")
            rep.student = input.rep_name().strip()
            rep.entries = [e for e in rep.entries if not (e["kind"] == "note" and e["title"] == "Discussion")]
            if input.rep_notes().strip():
                rep.section = "Discussion"
                rep.add_note("Discussion", input.rep_notes().strip())
            return rep

        def _base():
            n = re.sub(r"\W+", "_", input.rep_name().strip()) or "student"
            return "%s_%s_lab_report" % (os.path.basename(nb_path).split("_")[0] + "_" + os.path.basename(nb_path).split("_")[1], n)

        @render.download(filename=lambda: _base() + ".docx")
        def rep_docx():
            yield _report().to_docx()

        @render.download(filename=lambda: _base() + ".html")
        def rep_html():
            yield _report().to_html().encode("utf-8")

    return App(app_ui, server, static_assets=None if IN_BROWSER or not os.path.isdir(WWW) else WWW)
