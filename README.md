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

## Computational labs (RDKit and AutoDock Vina)

Five lab notebooks put the lecture methods to work on real molecules, in the
style of a lab manual: a numbered protocol with the reason for each step,
checkpoints with expected ranges, calculation cards with step-by-step
solutions, reporting standards, and an automatic lab report (.docx + .html)
that collects every figure, table and calculation. The first cell installs
RDKit, py3Dmol and Meeko from PyPI and the official AutoDock Vina 1.2.7
binary (allow a few minutes). Every adapted source and dataset is listed with
its licence in [`labs/SOURCES.md`](labs/SOURCES.md).

| Lectures | Lab | What you do | Open |
| --- | --- | --- | --- |
| L23–L24 | Conformer ensembles | RDKit ETKDG conformers, MMFF94 minimization, RMSD pruning, torsion scan, Boltzmann populations | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Spinner101/phs312-cadd-notebooks/blob/main/labs/PHS312_L23_L24_Lab_Conformers.ipynb) |
| L25–L26 | Docking with AutoDock Vina | PDB 3POZ (EGFR): receptor and ligand prep, box from the co-crystal ligand, redocking validation (RMSD ≤ 2 Å), a congeneric series, py3Dmol pose view | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Spinner101/phs312-cadd-notebooks/blob/main/labs/PHS312_L25_L26_Lab_Docking.ipynb) |
| L27 | Fragments and de novo growth | BRICS decomposition and recombination, property and PAINS filters, ligand efficiency and LLE | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Spinner101/phs312-cadd-notebooks/blob/main/labs/PHS312_L27_Lab_Fragments_DeNovo.ipynb) |
| L29–L30 | QSAR from real data | RDKit descriptors for ten cited EGFR inhibitors, Hansch-type regression, r², leave-one-out q² | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Spinner101/phs312-cadd-notebooks/blob/main/labs/PHS312_L29_L30_Lab_QSAR.ipynb) |
| L31–L32 | Bioisosteres and prodrugs | SMARTS swaps, Crippen log P, TPSA, % ionized and log D, ester prodrug properties | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Spinner101/phs312-cadd-notebooks/blob/main/labs/PHS312_L31_L32_Lab_Bioisosteres_Prodrugs.ipynb) |

Every lecture notebook now also has **calculation cards** (equation with each
variable's role, units and source; a colour-matched case; a step-by-step
solution with a unit check), an **Open calculator** panel laid out like the
HP-15C, HP 35s, TI-30XS MultiView, TI-84 Plus CE and Casio fx-991EX, and a
**Build and download my lab report** cell at the end.

## Interactive apps (no Colab needed)

The lecture notebooks and the Hansch activity are also available as interactive web apps that run entirely in your browser: nothing to install, nothing sent
anywhere. Each has the notebook's tools, figures, calculation cards, concept checks and lab-report download.

| Session | App |
|---|---|
| L22 · Computer-Aided Drug Design: An Overview | https://spinner101.github.io/phs312-cadd-notebooks/apps/L22/ |
| L23 · Conformational Analysis I | https://spinner101.github.io/phs312-cadd-notebooks/apps/L23/ |
| L24 · Conformational Analysis II | https://spinner101.github.io/phs312-cadd-notebooks/apps/L24/ |
| L25 · Molecular Docking Studies I | https://spinner101.github.io/phs312-cadd-notebooks/apps/L25/ |
| L26 · Molecular Docking Studies II | https://spinner101.github.io/phs312-cadd-notebooks/apps/L26/ |
| L27 · De Novo Drug Design | https://spinner101.github.io/phs312-cadd-notebooks/apps/L27/ |
| L28 · Exam 3 Review Session | https://spinner101.github.io/phs312-cadd-notebooks/apps/L28/ |
| L29 · QSAR I | https://spinner101.github.io/phs312-cadd-notebooks/apps/L29/ |
| L30 · QSAR II | https://spinner101.github.io/phs312-cadd-notebooks/apps/L30/ |
| L29–L30 · Building a Hansch Equation (in-class activity) | https://spinner101.github.io/phs312-cadd-notebooks/apps/L29-L30-Hansch/ |
| L31 · Bioisosterism | https://spinner101.github.io/phs312-cadd-notebooks/apps/L31/ |
| L32 · Prodrugs | https://spinner101.github.io/phs312-cadd-notebooks/apps/L32/ |

The first load takes 10–30 seconds. Download your lab report from the last tab before closing the tab. How the apps are built: `apps/README.md`.

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

## Third-party data: SwissBioisostere

The **L31 Bioisosterism** activity uses real matched-molecular-pair data from
[SwissBioisostere](https://www.swissbioisostere.ch), from the Molecular
Modelling Group of the SIB Swiss Institute of Bioinformatics and the
University of Lausanne. The underlying data derive from ChEMBL 36.

SwissBioisostere is made available under the
[CC-BY 4.0 licence](https://creativecommons.org/licenses/by/4.0/).

**Changes made:** retrieved 20 October 2026 through the SwissBioisostere web
interface. Two single-attachment-point fragment queries were run, carboxylic
acid `[*:1]C(=O)O` and primary amide `[*:1]C(=O)N`. The full result tables
(7,714 and 6,955 replacements) were reduced to the highest-frequency entries,
column names were shortened, and common chemical names were added. No values
were altered and no structures were recomputed. The curated extract is in
`data/` as both a Python module and a CSV.

Please cite:

> Cuozzo A., Daina A., Perez M.A.S., Michielin O., Zoete V. *SwissBioisostere:
> molecular replacements for drug discovery guided by updated structural,
> bioactivity and physico-chemical data accessible through a reshaped Web
> interface.* Nucleic Acids Research, 2021.

> Wirth M., Zoete V., Michielin O., Sauer W.H.B. *SwissBioisostere: a database
> of molecular replacements for ligand design.* Nucleic Acids Research 2013,
> 41(D1), D1137–D1143. doi:10.1093/nar/gks1059

SIB does not endorse this course or its materials.

## Licence

Code and written content: MIT (see `LICENSE`). If you reuse an activity in
your own teaching, an attribution line is appreciated.
