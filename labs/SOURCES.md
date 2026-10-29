# Sources, licences and provenance — PHS 312 computational labs

Every external source consulted while building `labs/` is listed here with its licence, the commit or
version checked, and exactly what was taken. **All prose, markdown and Python in these notebooks was
written for this course.** Where a workflow idea came from an external source it is named below and
cited in the notebook itself; no text or code was copied verbatim from any source that does not permit
it, and nothing was taken from a textbook or from any source without a licence.

Repositories were cloned into `refs/` while building the labs (they are not part of the course
repository) and the API calls used in the notebooks were checked against their current source:
`python3 check_labs.py --api refs/rdkit refs/Meeko` re-runs that check.

## 1. Software used in the notebooks

| Software | Version pinned | Licence | Where it is installed from | Used for |
|---|---|---|---|---|
| RDKit | latest PyPI wheel (`pip install rdkit`); APIs verified against release `Release_2026_09_1`, commit `fece8caa860bdf6c9c82bdb9253f22a0cf87150c` | BSD-3-Clause | PyPI wheel (cp312/cp313 available) | conformers, MMFF94, RMSD, descriptors, BRICS, reactions, drawing |
| AutoDock Vina | **1.2.7** (released 2025-02-26) | Apache-2.0 | official GitHub release binary `vina_1.2.7_linux_x86_64`, SHA-256 `f31f774f723bba7bbe6e9d1c47577020eea9a8da16424284c043d22593570644`; fallback `apt-get install autodock-vina` | docking, scoring, redocking validation |
| Meeko | **0.8.0** (2026-08-27), repo commit `41ff6414e53d71c027ccc20d9cbf0f08d2268ba5` (tag `v0.8.0`) | LGPL-2.1 | PyPI (`pip install meeko==0.8.0`) | receptor and ligand preparation to PDBQT, pose export back to RDKit |
| py3Dmol | latest PyPI | MIT (3Dmol.js, commit `c46c63b15881d41ff571e1579a11500bacf60b80` checked) | PyPI | interactive 3D views |
| numpy, pandas, matplotlib | Colab preinstalled | BSD-3-Clause | preinstalled | regression, tables, every figure |
| gemmi | latest PyPI | MPL-2.0 | PyPI (Meeko dependency) | structure parsing inside Meeko |

### Why the Vina binary and not the `vina` PyPI wheel
`pip install vina` ships wheels only up to **cp312** (vina 1.2.7 on PyPI: cp38–cp312, manylinux/musllinux
x86-64), and building from source needs Boost and SWIG. Colab's default runtime has been **Python 3.13 since
2026-08-19** (googlecolab/colabtools issue #6081), so the wheel would be compiled from source or fail. The
statically linked release binary is independent of the Python version and is what the labs use; it was
downloaded and run (`AutoDock Vina v1.2.7`) while building these labs. `condacolab` and the smina
binary from SourceForge (used by TeachOpenCADD T015 and by the UCL handbook) were rejected: condacolab
restarts the kernel and is slow, and SourceForge smina has not been released since 2020.

## 2. Teaching material used as a model (not copied)

| Source | Licence | What was taken |
|---|---|---|
| **UCL Open Docking Lab Handbook** (github.com/UCL/Open_Docking_Lab_Handbook, commit `99b9d9f767cab2410624847c4339a461125bbdab`); Ho, Jones et al., *J. Chem. Educ.* 2021, 98, 1922, doi:10.1021/acs.jchemed.1c00289 | **No licence file** — therefore all rights reserved | **Structure only**: the idea of a numbered end-to-end workflow (choose structure → inspect site → prepare → box from the bound ligand → dock → analyse poses → report), and the practice of stating resolution/organism when choosing a PDB entry. **No text, no code, no data, no figures** were reused. Its notebooks are also outdated (Python 3.7 miniconda, smina from SourceForge, `%pylab`), so nothing in them was carried over. Cited in every lab. |
| **TeachOpenCADD** (github.com/volkamerlab/teachopencadd, commit `c140d6cd2fa76d5d077d21bf0e5096f00d522151`); Sydow et al., *J. Chem. Inf. Model.* 2019, 59, 4 | **CC BY 4.0** (code and text) | T015: the **protocol pattern** of defining the box from the co-crystallised ligand's extent plus a fixed padding, and of validating by redocking. Their implementation uses OpenBabel + smina + nglview; our code is written for Meeko + Vina 1.2.7 + py3Dmol and shares no lines with theirs. T002/T003: the idea of a property-profile plus unwanted-substructure filter cascade (L27). T001: the **data set** (see §3). Attributed in each notebook's source list. |
| **AutoDock Vina documentation** (`docs/source/docking_basic.rst`, `colab_examples.rst`, repo commit `bb64e5e26b520569a86360d69248069b5e665b3f`) | Apache-2.0 | The documented `mk_prepare_receptor.py -p -v --box_center --box_size` / `vina --receptor --ligand --config` sequence, re-expressed as Python `subprocess` calls with explicit `--center_*`/`--size_*` flags. Option names verified against `src/main/main.cpp` of 1.2.7 by `check_labs.py`. |
| **Meeko documentation** (`docs/source/lig_prep_basic.rst`, `py_rec_prep.rst`, `export_usage.rst`) | LGPL-2.1 | The documented `MoleculePreparation().prepare(mol)` → `PDBQTWriterLegacy.write_string(setup)` idiom and the `PDBQTMolecule` → `RDKitMolCreate.from_pdbqt_mol` export idiom. Our helpers add the error handling and the `None` filtering. |
| **RDKit documentation and Cookbook** (rdkit.org/docs) | BSD-3-Clause | Standard idioms: `EmbedMultipleConfs` with `ETKDGv3`, `MMFFOptimizeMoleculeConfs`, relaxed torsion scanning with `MMFFAddTorsionConstraint`, `GetBestRMS` for symmetry-aware conformer pruning. Written out independently in each lab; the parallelisation recipe used by the UCL notebooks was not used. |

## 3. Data sets (every value cited in the notebook that uses it)

| Data | Source | Licence | Used in |
|---|---|---|---|
| Crystal structure **3POZ** (EGFR kinase domain + TAK-285, X-ray, 1.50 Å) | RCSB PDB, downloaded at run time from `files.rcsb.org`; Aertgeerts et al., *J. Biol. Chem.* 2011, 286, 18756; PDB: Berman et al., *Nucleic Acids Res.* 2000, 28, 235 | PDB data are in the public domain (CC0) | L25–L26 (receptor, box, redocking reference) |
| **EGFR IC50 values** for 4-anilino-6,7-dimethoxyquinazolines, gefitinib and erlotinib | **ChEMBL 27** (doi:10.6019/CHEMBL.database.27; Mendez et al., *Nucleic Acids Res.* 2019, 47, D930), target CHEMBL203, type IC50, relation `=`, assay type B, first record per molecule, as frozen in TeachOpenCADD T001 `data/EGFR_compounds.csv` (commit `c140d6c`, md5 `c76d6d611f7dc794436961fb4a78e430`) | ChEMBL data **CC BY-SA 3.0**; TeachOpenCADD CC BY 4.0 | L25–L26, L27, L29–L30. Ten of these values are transcribed into the notebooks (ChEMBL IDs, IC50, SMILES); the CSV itself is not redistributed. Every notebook states that the records come from different publications and assays, which limits their comparability. |
| Original SAR of the series | Bridges et al., *J. Med. Chem.* 1996, 39, 267 | cited only | L25–L26, L27, L29–L30 |
| Substituent constants **π, σ_m, MR** | Hansch, Leo & Taft, *Chem. Rev.* 1991, 91, 165 (standard published tables; ten substituents transcribed) | cited only (short factual data table) | L29–L30 |
| Approximate pKa values for carboxylic-acid bioisosteres, ibuprofen pKa and logP | Ballatore, Huryn & Smith, *ChemMedChem* 2013, 8, 385; Meanwell, *J. Med. Chem.* 2011, 54, 2529; standard reference data. Labelled **illustrative** in every table and card | cited only | L31–L32 |
| Propranolol structure (SMILES written for this lab) | — | — | L23–L24 |

No proprietary, textbook, publisher or question-bank material is used anywhere in `labs/`, and no
instructor keys or assessment items appear in these notebooks.

## 4. Methods cited (concepts, no code or text reused)

ETKDG: Riniker & Landrum, *J. Chem. Inf. Model.* 2015, 55, 2562; ETKDGv3: Wang et al., *J. Chem. Inf. Model.*
2020, 60, 2044 · MMFF94: Halgren, *J. Comput. Chem.* 1996, 17, 490; RDKit implementation: Tosco, Stiefl &
Landrum, *J. Cheminform.* 2014, 6, 37 · conformer-count guidance: Ebejer, Morris & Deane, *J. Chem. Inf.
Model.* 2012, 52, 1146 · Vina scoring: Trott & Olson, *J. Comput. Chem.* 2010, 31, 455; Eberhardt et al.,
*J. Chem. Inf. Model.* 2021, 61, 3891 · smina (for context only): Koes, Baumgartner & Camacho, *J. Chem.
Inf. Model.* 2013, 53, 1893 · docking reporting standards: Cole et al., *Proteins* 2005, 60, 325; Warren et
al., *J. Med. Chem.* 2006, 49, 5912; Jain & Nicholls, *J. Comput.-Aided Mol. Des.* 2008, 22, 133 · BRICS:
Degen et al., *ChemMedChem* 2008, 3, 1503 · Rule of Three: Congreve et al., *Drug Discov. Today* 2003, 8,
876 · Lipinski et al., *Adv. Drug Deliv. Rev.* 2001, 46, 3 · Veber et al., *J. Med. Chem.* 2002, 45, 2615 ·
PAINS: Baell & Holloway, *J. Med. Chem.* 2010, 53, 2719 · LE: Hopkins, Groom & Alex, *Drug Discov. Today*
2004, 9, 430 · LLE: Leeson & Springthorpe, *Nat. Rev. Drug Discov.* 2007, 6, 881 · group efficiency:
Verdonk & Rees, *ChemMedChem* 2008, 3, 1179 · Hansch analysis: Hansch & Fujita, *J. Am. Chem. Soc.* 1964, 86,
1616 · q²/PRESS: Cramer, Bunce & Patterson, *Quant. Struct.-Act. Relat.* 1988, 7, 18 · QSAR validation:
Golbraikh & Tropsha, *J. Mol. Graph. Model.* 2002, 20, 269; OECD *Guidance Document on the Validation of
(Q)SAR Models*, 2007 · Crippen logP/MR: Wildman & Crippen, *J. Chem. Inf. Comput. Sci.* 1999, 39, 868 ·
TPSA: Ertl, Rohde & Selzer, *J. Med. Chem.* 2000, 43, 3714 · bioisosteres: Patani & LaVoie, *Chem. Rev.*
1996, 96, 3147 · prodrugs: Rautio et al., *Nat. Rev. Drug Discov.* 2008, 7, 255 and 2018, 17, 559;
(acyloxy)methyl esters: Alexander et al., *J. Med. Chem.* 1988, 31, 318 · py3Dmol: Rego & Koes,
*Bioinformatics* 2015, 31, 1322.

## 5. Course-internal components

* The calculation cards, the `LabReport` collector, the calculator faceplates and the notebook glue come
  from the course's own `nbs/kit2/` kit and are embedded in each lab's set-up cell by
  `build_labs.py`, in the same way `p312/enhance.py` embeds them in the lecture notebooks
  (`calc_engine`, `stepsolve`, `report`, `pathway`, `calc_ui` with `CALC_LAYOUTS` loaded via
  `json.loads`, then `glue`; `from stepsolve import …` lines stripped). `nbs/kit2/` was not modified.
* `src/lab_helpers.py` (report tables, checkpoints, PIL-to-figure conversion so RDKit drawings reach the
  report, Boltzmann populations, version collection) and the per-lab `src/<LAB>.py` helper blocks are
  original code written for these labs.
