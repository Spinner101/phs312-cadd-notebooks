# Interactive notebook apps (Shiny for Python, run in the browser)

The site is built by GitHub Actions (`.github/workflows/apps.yml`) on every push that changes `notebooks/` or `apps/`, and published by GitHub Pages: **https://spinner101.github.io/phs312-cadd-notebooks/**

Each app is built from a notebook in `notebooks/`: every `#@param` form becomes live controls, and the figures, calculation
cards ("Solve step by step"), concept checks (same feedback as the notebook), performance summary and lab-report download are
all there. Python runs inside the student's browser through Shinylive (Pyodide), so there is no server and nothing to install;
answers stay in the open tab.

| App | Notebook |
|---|---|
| `apps/L23/` on the site | `notebooks/PHS312_L23_Conformational_Analysis_I.ipynb` |
| `apps/L24/` on the site | `notebooks/PHS312_L24_Conformational_Analysis_II.ipynb` |

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
