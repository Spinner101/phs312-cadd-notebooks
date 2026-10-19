# PHS 312 — Computational Activities

In-class Colab notebooks for **PHS 312: Drug Discovery, Design and
Development** (Hampton University School of Pharmacy, Dr. Sidney Bolden, Jr.).

Each notebook is a **30–35 minute paired activity**. Click a badge and it
opens in Google Colab. There is nothing to install and no code to write —
every cell is a form with sliders and dropdowns.

## The ten lecture activities

| Lecture | Activity | What you manipulate | Open |
| --- | --- | --- | --- |
| **L22** · CADD Overview | Force-field terms and choosing a method | force-field parameters; molecule size vs. question | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Spinner101/phs312-cadd-notebooks/blob/main/notebooks/PHS312_L22_CADD_Overview.ipynb) |
| **L23** · Conformational Analysis I | Where minimization stops; the size of the search | starting dihedral; rotatable bonds and grid step | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Spinner101/phs312-cadd-notebooks/blob/main/notebooks/PHS312_L23_Conformational_Analysis_I.ipynb) |
| **L24** · Conformational Analysis II | Simulated annealing; overlay and RMSD | temperature; displacement and rotation | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Spinner101/phs312-cadd-notebooks/blob/main/notebooks/PHS312_L24_Conformational_Analysis_II.ipynb) |
| **L25** · Molecular Docking I | Probe radius and surfaces; posing a rigid ligand | probe size; ligand position and orientation | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Spinner101/phs312-cadd-notebooks/blob/main/notebooks/PHS312_L25_Molecular_Docking_I.ipynb) |
| **L26** · Molecular Docking II | Scores against crystallographic truth | virtual-screening cutoff | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Spinner101/phs312-cadd-notebooks/blob/main/notebooks/PHS312_L26_Molecular_Docking_II.ipynb) |
| **L27** · De Novo Drug Design | Growing and linking fragments into a site | fragment choice, linker length, site filling | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Spinner101/phs312-cadd-notebooks/blob/main/notebooks/PHS312_L27_De_Novo_Drug_Design.ipynb) |
| **L29** · QSAR I | One descriptor at a time; linear vs. parabolic | descriptor and functional form | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Spinner101/phs312-cadd-notebooks/blob/main/notebooks/PHS312_L29_QSAR_I.ipynb) |
| **L30** · QSAR II | Over-fitting: r rises while q² collapses | which descriptors enter the equation | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Spinner101/phs312-cadd-notebooks/blob/main/notebooks/PHS312_L30_QSAR_II.ipynb) |
| **L31** · Bioisosterism | Replacing a carboxylic acid | replacement group; design requirements | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Spinner101/phs312-cadd-notebooks/blob/main/notebooks/PHS312_L31_Bioisosterism.ipynb) |
| **L32** · Prodrugs | Activation rate and between-patient variability | promoiety; patient esterase activity | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Spinner101/phs312-cadd-notebooks/blob/main/notebooks/PHS312_L32_Prodrugs.ipynb) |

## Two optional extension notebooks

These use RDKit on real molecules and install it on first run (about a
minute). They are richer but slower, and are not required for class.

| Topic | Activity | Open |
| --- | --- | --- |
| Conformational analysis | Relaxed torsion scan of a real molecule | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Spinner101/phs312-cadd-notebooks/blob/main/notebooks/PHS312_L23_Conformational_Analysis_Torsion_Scan.ipynb) |
| QSAR | Building a Hansch equation from tabulated constants | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Spinner101/phs312-cadd-notebooks/blob/main/notebooks/PHS312_L29_L30_QSAR_Hansch_Equation.ipynb) |

## For students

1. Click the badge for today's lecture. Sign in with your **Hampton Google
   account** if you are asked.
2. Run the first cell once. Then work down the notebook in pairs.
3. Answer every question. You get feedback on the concept checks and the
   end-of-activity assessment, including why each wrong option is wrong.
4. At the end, copy the single report code and paste it into the Canvas
   assignment.

**Nothing you type is sent anywhere.** These notebooks make no network
calls, write no files and do not connect to Google Drive. Your answers exist
only in your own browser tab until you paste the report code into Canvas
yourself.

Your edits are not saved back to this repository. Use *File ▸ Save a copy in
Drive* if you want to keep your work.

## How each notebook is built

* **Learning objectives** are tagged with a Bloom level and the syllabus
  level numeral, and with the Student Intended Learning Outcome they serve.
* **A prior-knowledge check** of three questions opens each notebook. It
  deliberately withholds correctness feedback, so that the pre/post
  comparison at the end is meaningful.
* **Concept checks** sit beside the simulation they test.
* **The end-of-activity assessment** uses items from the course MCQ bank,
  with per-distractor explanations.
* **The summary cell** reports each section, the pre/post comparison and the
  normalised learning gain *g* = (post − pre) / (100 − pre).

## Running locally instead

The ten lecture notebooks need only NumPy and matplotlib:

```bash
git clone https://github.com/Spinner101/phs312-cadd-notebooks.git
cd phs312-cadd-notebooks
pip install -r requirements.txt
jupyter lab
```

The `#@param` form controls are a Colab feature. Locally the notebooks still
run correctly — you edit the value in the code rather than moving a slider.

## What is here, and what is not

This repository holds **only original teaching code and writing**.

Course readings, lecture slide decks, textbook figures, publisher case
studies and the assessment bank are **not** here and will not be added.
Those derive from Oxford University Press instructor resources, which are
released to validated adopting instructors; OUP reserves all rights and its
terms do not grant public redistribution. Enrolled students get that
material through Canvas.

The `.gitignore` is written to block those file types from ever being
committed here by accident. Please leave it in place.

## Data provenance

The QSAR activities use published activity data and standard Hansch
substituent constants (π, MR, F, R) for two congeneric series — coumarin
MAO-B inhibitors and 6,7-disubstituted tacrine analogues. These are
literature values; the code, the questions and the framing are original to
this course.

All other simulations are deliberate, transparent toy models written for
teaching. They reproduce the qualitative behaviour discussed in Patrick
chapters 17 and 18 — local versus global minima, combinatorial search cost,
the Metropolis rule, shape complementarity and steric clash, enrichment,
over-fitting — and they are not quantitative predictions of any real system.

## Licence

Code and written content: MIT (see `LICENSE`). If you reuse an activity in
your own teaching, an attribution line is appreciated.
