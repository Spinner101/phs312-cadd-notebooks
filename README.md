# PHS 312 — Computational Activities

In-class notebooks for **PHS 312: Drug Discovery, Design and Development**
(Hampton University School of Pharmacy, Dr. Sidney Bolden, Jr.).

Each notebook is a 30-minute paired activity. Click a badge and it opens in
Google Colab — nothing to install, no account needed beyond a Google login.

| Lecture | Activity | Open |
| --- | --- | --- |
| L23 · Conformational Analysis I | Mapping a conformational energy surface | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Spinner101/phs312-cadd-notebooks/blob/main/notebooks/PHS312_L23_Conformational_Analysis_Torsion_Scan.ipynb) |
| L29/L30 · QSAR | Building a Hansch equation | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Spinner101/phs312-cadd-notebooks/blob/main/notebooks/PHS312_L29_L30_QSAR_Hansch_Equation.ipynb) |

## For students

1. Click the badge for today's lecture.
2. Run the first cell. In Colab it installs what it needs; on a machine that
   already has RDKit it installs nothing.
3. Work in pairs. Each part ends with questions — write the answers down,
   you will report two of them to the class.

Your edits in Colab are **not** saved back here. Use *File ▸ Save a copy in
Drive* to keep your work.

## Running locally instead

```bash
git clone https://github.com/Spinner101/phs312-cadd-notebooks.git
cd phs312-cadd-notebooks
pip install -r requirements.txt
jupyter lab
```

Tested on RDKit 2024.03.6. The notebooks avoid `nglview`, which is
unreliable in Colab, and use only matplotlib for display.

## What is here, and what is not

This repository holds **only original teaching code and writing**.

Course readings, lecture slide decks, textbook figures, publisher case
studies and assessment material are **not** here and will not be added.
Those derive from Oxford University Press instructor resources, which are
released to validated adopting instructors; OUP reserves all rights and its
terms do not grant public redistribution. Enrolled students get that
material through Canvas.

The `.gitignore` is written to block those file types from ever being
committed here by accident. Please leave it in place.

## Data provenance

The QSAR notebook uses published activity data and standard Hansch
substituent constants (π, MR, F, R) for two congeneric series — coumarin
MAO-B inhibitors and 6,7-disubstituted tacrine analogues. These are
literature values; the code, the questions and the framing are original to
this course.

## Licence

Code and written content: MIT (see `LICENSE`). If you reuse an activity in
your own teaching, an attribution line is appreciated.
