"""Build the in-browser (Shinylive) versions of the notebook apps into ../docs for GitHub Pages.

    pip install shiny shinylive
    python apps/build_site.py          (run from the repository root)

Each app is bundled with the engine (nbapp/) and its notebook copied from notebooks/, so the site always
matches the notebooks in the repo. Re-run after a notebook changes, then commit docs/ and push.
"""
import os, re, shutil, subprocess, sys, tempfile, json, html

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
DOCS = os.path.join(REPO, "docs")
COURSE = "PHS 312 · Drug Discovery, Design and Development"
APPS = [  # (folder under docs/apps, notebook, short title)
    ('L22', 'notebooks/PHS312_L22_CADD_Overview.ipynb', 'L22 · Computer-Aided Drug Design: An Overview'),
    ('L23', 'notebooks/PHS312_L23_Conformational_Analysis_I.ipynb', 'L23 · Conformational Analysis I'),
    ('L24', 'notebooks/PHS312_L24_Conformational_Analysis_II.ipynb', 'L24 · Conformational Analysis II'),
    ('L25', 'notebooks/PHS312_L25_Molecular_Docking_I.ipynb', 'L25 · Molecular Docking Studies I'),
    ('L26', 'notebooks/PHS312_L26_Molecular_Docking_II.ipynb', 'L26 · Molecular Docking Studies II'),
    ('L27', 'notebooks/PHS312_L27_De_Novo_Drug_Design.ipynb', 'L27 · De Novo Drug Design'),
    ('L28', 'notebooks/PHS312_L28_Exam_3_Review.ipynb', 'L28 · Exam 3 Review Session'),
    ('L29', 'notebooks/PHS312_L29_QSAR_I.ipynb', 'L29 · Quantitative Structure–Activity Relationships I'),
    ('L30', 'notebooks/PHS312_L30_QSAR_II.ipynb', 'L30 · Quantitative Structure–Activity Relationships II'),
    ('L29-L30-Hansch', 'notebooks/PHS312_L29_L30_QSAR_Hansch_Equation.ipynb', 'L29–L30 · Building a Hansch Equation (in-class activity)'),
    ('L31', 'notebooks/PHS312_L31_Bioisosterism.ipynb', 'L31 · Bioisosterism'),
    ('L32', 'notebooks/PHS312_L32_Prodrugs.ipynb', 'L32 · Prodrugs'),
]
APP_PY = '''import os
from nbapp import make_app
app = make_app(os.path.join(os.path.dirname(os.path.abspath(__file__)), {nb!r}), course={course!r})
'''


def main():
    os.makedirs(DOCS, exist_ok=True)
    for key, nb, _ in APPS:
        dest = os.path.join(DOCS, "apps", key)
        shutil.rmtree(dest, ignore_errors=True)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        with tempfile.TemporaryDirectory() as tmp:
            shutil.copytree(os.path.join(HERE, "nbapp"), os.path.join(tmp, "nbapp"),
                            ignore=shutil.ignore_patterns("__pycache__"))
            shutil.copy(os.path.join(REPO, nb), tmp)
            open(os.path.join(tmp, "app.py"), "w").write(APP_PY.format(nb=os.path.basename(nb), course=COURSE))
            cells = json.load(open(os.path.join(REPO, nb), encoding="utf-8"))["cells"]
            code = "\n".join("".join(c["source"]) for c in cells if c["cell_type"] == "code")
            extra = [m for m in ("pandas", "scipy") if re.search(r"(?m)^\s*(?:import|from)\s[^\n]*\b%s\b" % m, code)]
            open(os.path.join(tmp, "requirements.txt"), "w").write("\n".join(["numpy", "matplotlib"] + extra) + "\n")
            subprocess.run([shutil.which("shinylive") or "shinylive", "export", tmp, DOCS, "--subdir", "apps/" + key], check=True)
    open(os.path.join(DOCS, ".nojekyll"), "w").close()
    rows = "".join('<li><a href="apps/%s/">%s</a></li>' % (k, html.escape(t)) for k, _, t in APPS)
    open(os.path.join(DOCS, "index.html"), "w", encoding="utf-8").write(INDEX.replace("@@ROWS@@", rows))
    print("Site written to", DOCS)


INDEX = """<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>PHS 312 interactive apps</title>
<style>:root{--bg:#f6f8fb;--fg:#16202b;--ac:#0b4f6c}body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.5 system-ui,sans-serif}
header{background:var(--ac);color:#fff;padding:22px max(16px,env(safe-area-inset-left))}h1{margin:0;font-size:1.5rem}
main{max-width:720px;margin:0 auto;padding:20px max(16px,env(safe-area-inset-left))}li{margin:.5em 0;font-size:1.1rem}a{color:var(--ac)}
.note{background:#fff;border:1px solid #d7e0ea;border-radius:8px;padding:10px 14px;font-size:.92rem}</style></head>
<body><header><h1>PHS 312 · Interactive notebook apps</h1><div>Drug Discovery, Design and Development</div></header>
<main><p>Each app is the in-class Colab notebook as an interactive page: tools, figures, calculation cards and concept checks.
It runs entirely in your browser (nothing to install, nothing sent anywhere). The first load takes 10–30 seconds.</p>
<ul>@@ROWS@@</ul>
<p class="note">Use a recent Chrome, Edge, Firefox or Safari. Your answers stay in the open tab: download your lab report from
the last tab before you close it. The Colab notebooks remain the full version with all the reading.</p></main></body></html>"""

if __name__ == "__main__":
    main()
