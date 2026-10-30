# Interactive notebook apps (Shiny for Python, run in the browser)

The site is built by GitHub Actions (`.github/workflows/apps.yml`) on every push that changes `notebooks/` or `apps/`, and published by GitHub Pages: **https://spinner101.github.io/phs312-cadd-notebooks/**

Each app is built from a notebook in `notebooks/`: every `#@param` form becomes live controls, and the figures, calculation
cards ("Solve step by step"), concept checks (same feedback as the notebook), performance summary and lab-report download are
all there. Python runs inside the student's browser through Shinylive (Pyodide), so there is no server and nothing to install;
answers stay in the open tab.

| App | Session |
|---|---|
| `apps/L22/` on the site | Computer-Aided Drug Design: An Overview |
| `apps/L23/` on the site | Conformational Analysis I |
| `apps/L24/` on the site | Conformational Analysis II |
| `apps/L25/` on the site | Molecular Docking Studies I |
| `apps/L26/` on the site | Molecular Docking Studies II |
| `apps/L27/` on the site | De Novo Drug Design |
| `apps/L28/` on the site | Exam 3 Review Session |
| `apps/L29/` on the site | QSAR I |
| `apps/L30/` on the site | QSAR II |
| `apps/L29-L30-Hansch/` on the site | Building a Hansch Equation (in-class activity) |
| `apps/L31/` on the site | Bioisosterism |
| `apps/L32/` on the site | Prodrugs |

## One-time setup
Repository **Settings → Pages → Build and deployment → Source: GitHub Actions**. After that, every push that changes a notebook
rebuilds the apps automatically (about 2 minutes; progress under the **Actions** tab).

Add a notebook by adding a line to `APPS` in `build_site.py`. To preview locally: `pip install shiny shinylive`,
`python apps/build_site.py`, then `python -m http.server --directory docs 8008` and open http://localhost:8008
(`docs/` is git-ignored; GitHub builds its own copy).

## Files
- `apps/nbapp/engine.py`: runs the notebook's set-up cell and any cell with new form values; captures figures, displayed text and printed output.
- `apps/nbapp/build.py`: builds the page (one tab per notebook Part) and wires the controls, cards, checks and report.
- `apps/build_site.py`: bundles each app with its notebook and exports the static site to `docs/`.

Equations are rendered with KaTeX (MIT licence) loaded from the jsDelivr CDN.
