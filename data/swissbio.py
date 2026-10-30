# -*- coding: utf-8 -*-
"""Curated bioisosteric replacement data for PHS 312 Lecture 31.

SOURCE
    SwissBioisostere, https://www.swissbioisostere.ch
    Molecular Modelling Group, SIB Swiss Institute of Bioinformatics and
    the University of Lausanne. Underlying data derived from ChEMBL 36.

LICENCE
    CC-BY 4.0  https://creativecommons.org/licenses/by/4.0/
    Redistribution and adaptation permitted with attribution.

CHANGES MADE (required by CC-BY)
    Retrieved 20 October 2026 through the SwissBioisostere web interface.
    Two single-attachment-point ("side chain") fragment queries were run:
    carboxylic acid [*:1]C(=O)O  and primary amide [*:1]C(=O)N.
    The full result tables (7,714 and 6,955 replacements) were reduced to the
    highest-frequency entries shown below. Column names were shortened and
    values were not otherwise altered. No structures were recomputed.

CITE
    Cuozzo A., Daina A., Perez M.A.S., Michielin O., Zoete V.
    SwissBioisostere: molecular replacements for drug discovery guided by
    updated structural, bioactivity and physico-chemical data accessible
    through a reshaped Web interface. Nucleic Acids Research, 2021.
    Wirth M., Zoete V., Michielin O., Sauer W.H.B. SwissBioisostere: a
    database of molecular replacements for ligand design. Nucleic Acids
    Research 2013, 41(D1), D1137-D1143. doi:10.1093/nar/gks1059

COLUMNS
    smiles  replacement fragment, [*:1] marks the attachment point
    freq    number of matched molecular pairs in which this replacement occurs
    rank    rank by frequency within that query
    better / similar / worse
            how the replacement changed measured activity across those pairs
    dlogp, dtpsa, dmw
            mean change in calculated logP, topological PSA and molecular
            weight on making the replacement
"""

FIELDS = ("smiles", "freq", "rank", "better", "similar", "worse",
          "dlogp", "dtpsa", "dmw")

# common names for the fragments students meet in Patrick 7e 13.3.7
NAMES = {
    "COC(=O)[*:1]": "methyl ester",
    "NC(=O)[*:1]": "primary amide",
    "CCOC(=O)[*:1]": "ethyl ester",
    "O[*:1]": "hydroxyl",
    "C[*:1]": "methyl",
    "OC[*:1]": "hydroxymethyl",
    "O=C(O)C[*:1]": "carboxymethyl (homologue)",
    "N#C[*:1]": "nitrile",
    "CNC(=O)[*:1]": "N-methyl amide",
    "CO[*:1]": "methoxy",
    "N[*:1]": "amine",
    "CN(C)C(=O)[*:1]": "N,N-dimethyl amide",
    "O=C(NO)[*:1]": "hydroxamic acid",
    "c1ccc([*:1])cc1": "phenyl",
    "F[*:1]": "fluorine",
    "Cl[*:1]": "chlorine",
    "n1n[nH]c([*:1])n1": "tetrazol-5-yl",
    "FC(F)(F)[*:1]": "trifluoromethyl",
    "n1nc([*:1])n[nH]1": "tetrazol-5-yl (tautomer)",
    "O=[N+]([O-])[*:1]": "nitro",
    "NS(=O)(=O)[*:1]": "sulfonamide",
    "CS(=O)(=O)NC(=O)[*:1]": "acylsulfonamide",
    "O=C(O)CC[*:1]": "2-carboxyethyl (homologue)",
    "O=C(NCCO)[*:1]": "N-(2-hydroxyethyl) amide",
    "CC(=O)N[*:1]": "acetamido",
    "Br[*:1]": "bromine",
    "CS(=O)(=O)[*:1]": "methylsulfonyl",
    "O=C(N1CCOCC1)[*:1]": "morpholine amide",
    "CC(=O)[*:1]": "acetyl",
    "CN(C)[*:1]": "dimethylamino",
    "O=C(O)[*:1]": "carboxylic acid",
    "CCNC(=O)[*:1]": "N-ethyl amide",
    "O=C(NC1CC1)[*:1]": "N-cyclopropyl amide",
    "CS(=O)(=O)N[*:1]": "methanesulfonamido",
}

# ---- carboxylic acid: what replaces [*:1]C(=O)O  (7,714 replacements total)
ACID_TOTAL = 7714
ACID = [
 ("COC(=O)[*:1]", 4530, 1, 1238, 2353, 939, 0.09, -11.00, 14.03),
 ("NC(=O)[*:1]", 2781, 2, 1000, 1334, 447, -0.60, 5.79, -0.99),
 ("CCOC(=O)[*:1]", 2449, 3, 703, 1024, 722, 0.48, -11.00, 28.06),
 ("O[*:1]", 1626, 4, 604, 793, 229, 0.01, -17.07, -28.01),
 ("C[*:1]", 1478, 5, 620, 616, 242, 0.61, -37.30, -29.98),
 ("OC[*:1]", 1144, 6, 395, 546, 203, -0.20, -17.07, -13.98),
 ("O=C(O)C[*:1]", 956, 7, 253, 530, 173, -0.08, 0.00, 14.02),
 ("N#C[*:1]", 877, 8, 346, 353, 178, 0.17, -13.51, -19.00),
 ("CNC(=O)[*:1]", 818, 9, 298, 412, 108, -0.34, -8.20, 13.04),
 ("CO[*:1]", 788, 10, 331, 334, 123, 0.31, -28.07, -13.98),
 ("N[*:1]", 721, 11, 201, 368, 152, -0.51, -11.28, -29.00),
 ("CN(C)C(=O)[*:1]", 692, 12, 230, 331, 131, 0.00, -16.99, 27.07),
 ("O=C(NO)[*:1]", 654, 13, 440, 157, 57, -0.58, 12.03, 15.02),
 ("c1ccc([*:1])cc1", 635, 14, 271, 262, 102, 1.96, -37.30, 32.09),
 ("F[*:1]", 625, 15, 265, 259, 101, 0.44, -37.30, -26.02),
 ("Cl[*:1]", 604, 16, 276, 240, 88, 0.95, -37.30, -9.57),
 ("n1n[nH]c([*:1])n1", 545, 17, 105, 325, 115, -0.52, 17.16, 24.03),
 ("FC(F)(F)[*:1]", 503, 18, 214, 206, 83, 1.32, -37.30, 23.98),
 ("n1nc([*:1])n[nH]1", 484, 19, 135, 256, 93, -0.51, 17.16, 24.03),
 ("O=[N+]([O-])[*:1]", 384, 20, 166, 167, 51, 0.21, 5.84, 0.99),
 ("NS(=O)(=O)[*:1]", 382, 21, 157, 168, 57, -1.05, 22.86, 35.07),
 ("CS(=O)(=O)NC(=O)[*:1]", 369, 22, 36, 226, 107, -1.01, 25.94, 77.11),
 ("O=C(O)CC[*:1]", 348, 23, 112, 191, 45, 0.32, 0.00, 28.06),
 ("O=C(NCCO)[*:1]", 341, 24, 148, 142, 51, -0.98, 12.03, 43.07),
 ("CC(=O)N[*:1]", 331, 25, 111, 160, 60, 0.26, -8.20, 13.04),
 ("Br[*:1]", 330, 26, 153, 125, 52, 1.06, -37.30, 34.89),
 ("CS(=O)(=O)[*:1]", 327, 27, 132, 141, 54, -0.43, -3.16, 34.08),
 ("O=C(N1CCOCC1)[*:1]", 315, 28, 93, 151, 71, -0.23, -7.76, 69.10),
 ("CC(=O)[*:1]", 296, 29, 120, 118, 58, 0.50, -20.23, -1.97),
 ("CN(C)[*:1]", 283, 30, 93, 116, 74, 0.08, -34.06, -0.94),
]

# ---- primary amide: what replaces [*:1]C(=O)N  (6,955 replacements total)
AMIDE_TOTAL = 6955
AMIDE = [
 ("O=C(O)[*:1]", 2781, 1, 447, 1334, 1000, 0.60, -5.79, 0.99),
 ("N#C[*:1]", 2384, 2, 586, 1189, 609, 1.04, -19.30, -18.01),
 ("CNC(=O)[*:1]", 2202, 3, 192, 1591, 419, 0.26, -13.99, 14.03),
 ("O[*:1]", 1622, 4, 398, 1003, 221, 0.11, -22.86, -27.02),
 ("COC(=O)[*:1]", 1269, 5, 259, 699, 311, 0.68, -16.79, 15.02),
 ("C[*:1]", 1238, 6, 361, 668, 209, 1.21, -43.09, -28.99),
 ("CN(C)C(=O)[*:1]", 1112, 7, 128, 590, 394, 0.61, -22.78, 28.06),
 ("OC[*:1]", 1060, 8, 233, 651, 176, 0.51, -22.86, -13.00),
 ("CO[*:1]", 1003, 9, 235, 554, 214, 0.91, -33.86, -12.99),
 ("F[*:1]", 720, 10, 195, 360, 165, 1.04, -43.09, -25.04),
 ("Cl[*:1]", 669, 11, 262, 281, 126, 1.55, -43.09, -8.58),
 ("N[*:1]", 646, 12, 151, 332, 163, 0.08, -17.07, -28.01),
 ("FC(F)(F)[*:1]", 635, 13, 194, 272, 169, 1.92, -43.09, 24.97),
 ("CCOC(=O)[*:1]", 612, 14, 146, 344, 122, 1.08, -16.79, 29.03),
 ("CS(=O)(=O)[*:1]", 599, 15, 90, 403, 106, 0.17, -8.95, 35.06),
 ("CC(=O)N[*:1]", 546, 16, 80, 349, 117, 0.26, -13.99, 14.03),
 ("O=C(NCCO)[*:1]", 532, 17, 42, 385, 105, -0.38, 6.24, 44.05),
 ("c1ccc([*:1])cc1", 476, 18, 128, 246, 102, 2.37, -43.09, 33.07),
 ("O=C(N1CCOCC1)[*:1]", 443, 19, 45, 250, 148, 0.37, -13.55, 70.09),
 ("CC(=O)[*:1]", 441, 20, 112, 235, 94, 1.10, -26.02, -0.98),
 ("CCNC(=O)[*:1]", 438, 21, 65, 269, 104, 0.65, -13.99, 28.06),
 ("O=C(NC1CC1)[*:1]", 431, 22, 94, 246, 91, 0.80, -13.99, 40.06),
 ("NS(=O)(=O)[*:1]", 382, 23, 72, 232, 78, -0.45, 17.07, 36.06),
 ("CS(=O)(=O)N[*:1]", 359, 24, 58, 225, 76, 0.27, 3.08, 50.08),
 ("Br[*:1]", 339, 25, 137, 146, 56, 1.66, -43.09, 35.88),
]

QUERIES = {
    "carboxylic acid": dict(query="[*:1]C(=O)O", total=ACID_TOTAL, rows=ACID),
    "primary amide":   dict(query="[*:1]C(=O)N", total=AMIDE_TOTAL, rows=AMIDE),
}


def table(which="carboxylic acid"):
    q = QUERIES[which]
    return [dict(zip(FIELDS, r), name=NAMES.get(r[0], r[0])) for r in q["rows"]]


def success_rate(row):
    """Fraction of matched pairs where activity did not get worse."""
    n = row["better"] + row["similar"] + row["worse"]
    return (row["better"] + row["similar"]) / n if n else 0.0
