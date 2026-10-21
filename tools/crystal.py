# -*- coding: utf-8 -*-
"""PHS 312 — real-structure activities built on crystallographic coordinates.

Everything here operates on a PDB entry embedded in the notebook itself.
No network, no install beyond NumPy and matplotlib. Optional 3D viewing via
py3Dmol when it is available; otherwise matplotlib draws the structure.

Structure: PDB 1ACJ, Harel et al., acetylcholinesterase with tacrine (THA)
bound in the active-site gorge.
"""
import base64, gzip, itertools, math
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401

PRIMARY, SECOND, MUTED, OK = "#0B6E8F", "#C2410C", "#6B7280", "#15803D"
PDB_B64 = ""          # filled in by the notebook builder
_cache = {}

# covalent radii, enough to infer bonds from coordinates
_COV = {"C": 0.76, "N": 0.71, "O": 0.66, "S": 1.05, "H": 0.31, "P": 1.07}
VDW = {"C": 1.70, "N": 1.55, "O": 1.52, "S": 1.80, "H": 1.20, "P": 1.80}


def _fig(w=9.5, h=4.4):
    f, ax = plt.subplots(figsize=(w, h))
    ax.grid(alpha=.25); ax.set_axisbelow(True)
    for s in ("top", "right"): ax.spines[s].set_visible(False)
    return f, ax


def pdb_text():
    if "txt" not in _cache:
        _cache["txt"] = gzip.decompress(base64.b64decode(PDB_B64)).decode()
    return _cache["txt"]


def _parse():
    if "parsed" in _cache:
        return _cache["parsed"]
    prot, lig = [], []
    for l in pdb_text().splitlines():
        if l.startswith(("ATOM", "HETATM")):
            rec = dict(name=l[12:16].strip(), resn=l[17:20].strip(),
                       chain=l[21].strip(), resi=l[22:26].strip(),
                       x=float(l[30:38]), y=float(l[38:46]), z=float(l[46:54]),
                       elem=(l[76:78].strip() or l[12:16].strip()[0]).upper())
            (lig if l.startswith("HETATM") else prot).append(rec)
    _cache["parsed"] = (prot, lig)
    return prot, lig


def ligand(resn="THA"):
    _, lig = _parse()
    if not isinstance(resn, str):
        raise TypeError(
            f"ligand() wants a residue name such as 'THA', got {resn!r}. "
            "If you meant a distance, pass it as cutoff=...")
    a = [r for r in lig if r["resn"] == resn.upper()]
    if not a:
        have = sorted({r["resn"] for r in lig})
        raise ValueError(f"no residue {resn!r} in this structure; available: {have}")
    X = np.array([[r["x"], r["y"], r["z"]] for r in a])
    return a, X


def protein():
    prot, _ = _parse()
    X = np.array([[r["x"], r["y"], r["z"]] for r in prot])
    return prot, X


def bonds_of(atoms, X, tol=0.45):
    """Infer bonds from covalent radii. Returns (i, j, distance)."""
    out = []
    for i, j in itertools.combinations(range(len(X)), 2):
        d = float(np.linalg.norm(X[i] - X[j]))
        lim = _COV.get(atoms[i]["elem"], 0.77) + _COV.get(atoms[j]["elem"], 0.77) + tol
        if d <= lim:
            out.append((i, j, d))
    return out


def angles_of(atoms, X, bonds):
    adj = {}
    for i, j, _ in bonds:
        adj.setdefault(i, []).append(j); adj.setdefault(j, []).append(i)
    out = []
    for c, ns in adj.items():
        for a, b in itertools.combinations(sorted(ns), 2):
            v1, v2 = X[a] - X[c], X[b] - X[c]
            cos = float(v1 @ v2 / (np.linalg.norm(v1) * np.linalg.norm(v2)))
            out.append((a, c, b, math.degrees(math.acos(max(-1, min(1, cos))))))
    return out


# ---------------------------------------------------------------- L22
def measure_geometry(term="bond lengths", resn="THA", show=True):
    """Measure what a force field parameterises, from the real crystal structure."""
    atoms, X = ligand(resn)
    bl = bonds_of(atoms, X)
    if term == "bond lengths":
        vals = [d for _, _, d in bl]
        labels = [f"{atoms[i]['name']}-{atoms[j]['name']}" for i, j, _ in bl]
        unit, ideal, title = "angstrom", None, "every bond in the ligand"
    else:
        ang = angles_of(atoms, X, bl)
        vals = [v for *_, v in ang]
        labels = [f"{atoms[a]['name']}-{atoms[c]['name']}-{atoms[b]['name']}"
                  for a, c, b, _ in ang]
        unit, ideal, title = "degrees", (109.5, 120.0), "every valence angle"

    if show:
        f, ax = _fig(10.0, 3.8)
        order = np.argsort(vals)
        ax.bar(range(len(vals)), [vals[i] for i in order], color=PRIMARY)
        ax.set_xticks(range(len(vals)))
        ax.set_xticklabels([labels[i] for i in order], rotation=90, fontsize=7)
        ax.set_ylabel(unit)
        ax.set_ylim(min(vals) * 0.97, max(vals) * 1.02)
        if ideal:
            for v, lab in zip(ideal, ("sp3  109.5", "sp2  120")):
                ax.axhline(v, color=SECOND, ls="--", lw=1.4)
                ax.text(len(vals) - .5, v, "  " + lab, va="center",
                        color=SECOND, fontsize=9)
        ax.set_title(f"{title}, measured in the crystal structure")
        plt.tight_layout(); plt.show()

    v = np.array(vals)
    if not show:
        out = dict(term=term, n=len(v), lo=round(float(v.min()), 3),
                   hi=round(float(v.max()), 3), mean=round(float(v.mean()), 3))
        return out
    print(f"{len(v)} measurements from the real structure")
    print(f"  range  {v.min():.3f} to {v.max():.3f} {unit}")
    print(f"  mean   {v.mean():.3f}   spread {v.std():.3f}")
    out = dict(term=term, n=len(v), lo=round(float(v.min()), 3),
               hi=round(float(v.max()), 3), mean=round(float(v.mean()), 3))
    if term == "bond lengths":
        ar = [d for _, _, d in bl if 1.33 <= d <= 1.43]
        sp3 = [d for _, _, d in bl if d > 1.48]
        print(f"  aromatic-like (1.33-1.43 A): {len(ar)}")
        print(f"  single sp3-like (> 1.48 A) : {len(sp3)}")
        print("\n  One force-field parameter cannot cover both. That is why a")
        print("  force field carries a different constant for each bond type.")
        out.update(aromatic=len(ar), sp3=len(sp3))
    else:
        n120 = int(((v > 112) & (v < 128)).sum()); n109 = int(((v > 103) & (v < 116)).sum())
        print(f"  near 120 deg (sp2): {n120}      near 109.5 deg (sp3): {n109}")
        print("\n  The angles cluster around the two hybridisation ideals, which")
        print("  is exactly what the bending term is fitted to reproduce.")
        out.update(near_120=n120, near_109=n109)
    return out


def contacts(cutoff=4.5, resn="THA", show=True):
    """Real non-bonded contacts between the ligand and the protein."""
    atoms, L = ligand(resn)
    prot, P = protein()
    d = np.linalg.norm(L[:, None, :] - P[None, :, :], axis=2)
    pairs = []
    for i in range(len(L)):
        for j in np.where(d[i] <= cutoff)[0]:
            r = prot[int(j)]
            s = (VDW.get(atoms[i]["elem"], 1.7) + VDW.get(r["elem"], 1.7))
            pairs.append((float(d[i, int(j)]), atoms[i]["name"], r["resn"],
                          r["resi"], r["name"], s))
    pairs.sort()
    if show:
        gap = np.array([p[0] - p[5] for p in pairs])
        col = ["#DC2626" if g < -0.4 else (OK if g < 0.5 else MUTED) for g in gap]
        f, ax = _fig(9.4, 4.2)
        ax.bar(range(len(gap)), gap, color=col, width=1.0)
        ax.axhline(0, color="#1F2937", lw=1.6)
        ax.set_xlabel(f"ligand-protein atom pairs within {cutoff} A, closest first")
        ax.set_ylabel("distance minus sum of vdW radii (A)")
        ax.set_title("zero means exactly at van der Waals contact;\n"
                     "a real clash sits well below zero, and there are none here",
                     fontsize=10)
        nc = int((gap < -0.4).sum()); nt = int(((gap >= -0.4) & (gap < 0.5)).sum())
        ax.legend(handles=[
            plt.Line2D([], [], color="#DC2626", lw=6, label=f"clash ({nc})"),
            plt.Line2D([], [], color=OK, lw=6, label=f"at contact ({nt})"),
            plt.Line2D([], [], color=MUTED, lw=6, label="further out")],
            fontsize=8, loc="lower right")
        plt.tight_layout(); plt.show()
    tight = [p for p in pairs if p[0] < p[5]]
    clash = [p for p in pairs if p[0] < p[5] - 0.4]
    if show:
        print(f"{len(pairs)} ligand-protein atom pairs within {cutoff} A")
        print(f"  {'dist':>6}  {'sum vdW':>8}  contact")
        for p in pairs[:10]:
            mark = "  at/inside vdW contact" if p[0] < p[5] else ""
            print(f"  {p[0]:>6.2f}  {p[5]:>8.2f}  {p[1]:<4} ... "
                  f"{p[2]}{p[3]} {p[4]:<4}{mark}")
        print(f"\n  at or just inside the vdW sum : {len(tight)}")
        print(f"  genuinely clashing (>0.4 A in): {len(clash)}")
        print()
        if not clash:
            print("  Nothing clashes. That is what a real binding mode looks like:")
            print("  the ligand sits AT van der Waals contact with the protein,")
            print("  never inside it. A docking pose that scores well while pushing")
            print("  atoms closer than this is wrong, however good its number.")
    resid = sorted({(p[2], p[3]) for p in pairs})
    return dict(cutoff=cutoff, pairs=len(pairs), at_or_inside_vdw=len(tight),
                clashing=len(clash), residues=len(resid),
                nearest=round(pairs[0][0], 2) if pairs else None)


def dihedral(p0, p1, p2, p3):
    """Standard IUPAC torsion angle in degrees."""
    b0, b1, b2 = p0 - p1, p2 - p1, p3 - p2
    b1n = b1 / np.linalg.norm(b1)
    v = b0 - (b0 @ b1n) * b1n
    w = b2 - (b2 @ b1n) * b1n
    x = v @ w
    y = np.cross(b1n, v) @ w
    return math.degrees(math.atan2(y, x))


CHI1 = {"ARG": "CG", "ASN": "CG", "ASP": "CG", "CYS": "SG", "GLN": "CG",
        "GLU": "CG", "HIS": "CG", "ILE": "CG1", "LEU": "CG", "LYS": "CG",
        "MET": "CG", "PHE": "CG", "PRO": "CG", "SER": "OG", "THR": "OG1",
        "TRP": "CG", "TYR": "CG", "VAL": "CG1"}


def sidechain_torsions(near_ligand=8.0, resn="THA"):
    """Real chi1 torsions of residues lining the pocket."""
    prot, P = protein()
    _, L = ligand(resn)
    byres = {}
    for i, r in enumerate(prot):
        byres.setdefault((r["chain"], r["resi"], r["resn"]), {})[r["name"]] = P[i]
    out = []
    for (ch, ri, rn), at in byres.items():
        g = CHI1.get(rn)
        if not g or not all(k in at for k in ("N", "CA", "CB", g)):
            continue
        d = float(np.min(np.linalg.norm(L - at["CA"], axis=1)))
        if d > near_ligand:
            continue
        chi = dihedral(at["N"], at["CA"], at["CB"], at[g])
        out.append(dict(resn=rn, resi=ri, chain=ch, chi1=chi, dist=d))
    out.sort(key=lambda r: r["dist"])
    return out


def rotamers(near_ligand=8.0, show=True):
    """Real side-chain torsions cluster at the three staggered minima."""
    rows = sidechain_torsions(near_ligand)
    chi = np.array([r["chi1"] for r in rows])
    def bucket(a):
        a = (a + 360) % 360
        if 0 <= a < 120: return "gauche+ (~60)"
        if 120 <= a < 240: return "trans (~180)"
        return "gauche- (~300)"
    buckets = [bucket(c) for c in chi]
    if show:
        f, ax = _fig(9.4, 4.0)
        ax.hist(((chi + 360) % 360), bins=36, range=(0, 360), color=PRIMARY)
        for v, lab in ((60, "gauche+"), (180, "trans"), (300, "gauche-")):
            ax.axvline(v, color=SECOND, ls="--", lw=1.5)
            ax.text(v, ax.get_ylim()[1] * .92, "  " + lab, color=SECOND, fontsize=9)
        ax.set_xlim(0, 360); ax.set_xticks(range(0, 361, 60))
        ax.set_xlabel("chi-1 torsion angle (degrees)")
        ax.set_ylabel("side chains")
        ax.set_title(f"{len(rows)} residues within {near_ligand} A of the ligand, "
                     "measured in the crystal")
        plt.tight_layout(); plt.show()
        print(f"{'residue':<10}{'chi-1':>9}   rotamer                 dist to ligand")
        for r in rows[:12]:
            print(f"  {r['resn']}{r['resi']:<6}{r['chi1']:>9.1f}   "
                  f"{bucket(r['chi1']):<22}  {r['dist']:.1f} A")
        from collections import Counter
        c = Counter(buckets)
        print(f"\n  {c}")
        print("\n  Side chains do not sit at random angles. They occupy three")
        print("  staggered wells, which is the same local-minimum structure you")
        print("  see in a torsion profile - measured here in a real protein.")
    from collections import Counter
    c = Counter(buckets)
    return dict(n=len(rows), counts=dict(c),
                near_stagger=int(sum(1 for a in chi
                                     if min(abs(((a + 360) % 360) - v)
                                            for v in (60, 180, 300)) < 40)))


def search_cost(n_rot=7, step=30, seconds_each=0.05, show=True):
    """Arithmetic, not simulation: how many structures a grid search needs."""
    per_bond = int(round(360 / step))
    n = per_bond ** n_rot
    secs = n * seconds_each
    yrs = secs / 3600 / 24 / 365
    if show:
        print(f"settings per bond        {per_bond}   ({step} degree steps)")
        print(f"rotatable bonds          {n_rot}")
        print(f"conformations to score   {n:,}")
        print(f"at {seconds_each} s each            {secs/3600:,.1f} hours", end="")
        print(f"   =  {yrs:,.0f} years" if yrs >= 1 else "")
        if yrs >= 1:
            print("\n  This is why no docking program does a systematic search.")
    return dict(conformations=n, per_bond=per_bond, hours=secs / 3600,
                years=yrs)


# ---------------------------------------------------------------- L24
def rmsd(A, B):
    return float(np.sqrt(((A - B) ** 2).sum(axis=1).mean()))


def move_ligand(dx=0.0, dy=0.0, dz=0.0, rot_deg=0.0, axis="z", resn="THA"):
    """Rigid-body move of the real ligand. Returns the moved coordinates."""
    _, X = ligand(resn)
    c = X.mean(axis=0)
    t = math.radians(rot_deg)
    ax = {"x": np.array([1., 0, 0]), "y": np.array([0, 1., 0]),
          "z": np.array([0, 0, 1.])}[axis]
    K = np.array([[0, -ax[2], ax[1]], [ax[2], 0, -ax[0]], [-ax[1], ax[0], 0]])
    R = np.eye(3) + math.sin(t) * K + (1 - math.cos(t)) * (K @ K)
    return (X - c) @ R.T + c + np.array([dx, dy, dz])


def pose_rmsd(dx=0.0, dy=0.0, dz=0.0, rot_deg=0.0, resn="THA", show=True):
    """Move the real crystal pose and measure the real RMSD you created."""
    atoms, X = ligand(resn)
    Y = move_ligand(dx, dy, dz, rot_deg, resn=resn)
    r = rmsd(X, Y)
    per = np.linalg.norm(X - Y, axis=1)
    if show:
        f, (a1, a2) = plt.subplots(1, 2, figsize=(12.4, 4.2))
        a1.bar(range(len(per)), per, color=PRIMARY)
        a1.set_xticks(range(len(per)))
        a1.set_xticklabels([a["name"] for a in atoms], rotation=90, fontsize=7)
        a1.set_ylabel("displacement (A)")
        a1.axhline(r, color=SECOND, ls="--", lw=1.6, label=f"RMSD = {r:.2f} A")
        a1.legend(fontsize=9)
        a1.set_title("how far each atom moved")
        a2.scatter(X[:, 0], X[:, 1], s=60, color=MUTED, label="crystal pose")
        a2.scatter(Y[:, 0], Y[:, 1], s=60, color=SECOND, label="your pose")
        for i in range(len(X)):
            a2.plot([X[i, 0], Y[i, 0]], [X[i, 1], Y[i, 1]], color="#AAB", lw=.8)
        a2.set_aspect("equal"); a2.legend(fontsize=9)
        a2.set_xlabel("x (A)"); a2.set_ylabel("y (A)")
        a2.set_title("looking down z")
        for ax_ in (a1, a2):
            ax_.grid(alpha=.25)
            for s in ("top", "right"): ax_.spines[s].set_visible(False)
        plt.tight_layout(); plt.show()
    verdict = ("counts as the correct pose (under 2 A)" if r < 2.0
               else "would be scored as a wrong pose (2 A or more)")
    print(f"RMSD to the crystal pose : {r:.2f} A   -> {verdict}")
    print(f"furthest atom moved      : {per.max():.2f} A")
    print(f"closest atom moved       : {per.min():.2f} A")
    return dict(rmsd=round(r, 2), max_move=round(float(per.max()), 2),
                correct_pose=bool(r < 2.0))


def pharmacophore(resn="THA", show=True):
    """The real 3-point geometry of the bound ligand."""
    atoms, X = ligand(resn)
    idx = {a["name"]: i for i, a in enumerate(atoms)}
    ring = [idx[n] for n in ("C1", "C2", "C3", "C4", "C5", "C6") if n in idx]
    pts = {}
    if ring: pts["aromatic centroid"] = X[ring].mean(axis=0)
    for nm, lab in (("N15", "amine N (donor)"), ("N7", "ring N (acceptor)")):
        if nm in idx: pts[lab] = X[idx[nm]]
    names = list(pts)
    print("Three-point pharmacophore, measured in the crystal structure:")
    out = {}
    for a, b in itertools.combinations(names, 2):
        d = float(np.linalg.norm(pts[a] - pts[b]))
        out[f"{a} - {b}"] = round(d, 2)
        print(f"   {a:<22} to {b:<22} {d:5.2f} A")
    if show and len(names) == 3:
        f, ax = _fig(6.4, 5.2)
        P2 = np.array([pts[n] for n in names])
        ax.scatter(P2[:, 0], P2[:, 1], s=180,
                   color=[PRIMARY, SECOND, OK][:len(names)], zorder=3)
        for i, n in enumerate(names):
            ax.annotate(n, (P2[i, 0], P2[i, 1]), fontsize=9,
                        xytext=(8, 6), textcoords="offset points")
        for i, j in itertools.combinations(range(len(names)), 2):
            ax.plot(P2[[i, j], 0], P2[[i, j], 1], color=MUTED, lw=1.4)
            m = P2[[i, j]].mean(axis=0)
            ax.text(m[0], m[1], f"{np.linalg.norm(P2[i]-P2[j]):.2f} A",
                    fontsize=8, color=MUTED)
        ax.set_aspect("equal"); ax.set_xlabel("x (A)"); ax.set_ylabel("y (A)")
        ax.margins(0.28)
        ax.set_title("the pharmacophore is this triangle, not the skeleton",
                     pad=16)
        plt.tight_layout(); plt.show()
    return out


# ---------------------------------------------------------------- L25 / L26
def score_pose(Y, resn="THA", cutoff=6.0):
    """A deliberately simple score over REAL coordinates.

    contact reward - clash penalty - desolvation-ish term. It is transparent
    on purpose: every piece is printed, so the point is not that this is a
    good scoring function but that you can see exactly what it rewards.
    """
    atoms, _ = ligand(resn)
    prot, P = protein()
    d = np.linalg.norm(Y[:, None, :] - P[None, :, :], axis=2)
    ser = np.array([VDW.get(a["elem"], 1.7) for a in atoms])[:, None]
    spr = np.array([VDW.get(r["elem"], 1.7) for r in prot])[None, :]
    s = ser + spr
    near = d <= cutoff
    gap = d - s
    contact = float(np.sum(np.exp(-((gap[near]) ** 2) / 0.8)))
    overlap = np.clip(-gap, 0, None)
    clash = float(np.sum(overlap[near] ** 2) * 20)
    polar_l = np.array([a["elem"] in ("N", "O") for a in atoms])[:, None]
    polar_p = np.array([r["elem"] in ("N", "O") for r in prot])[None, :]
    hb_mask = near & polar_l & polar_p & (d > 2.4) & (d < 3.5)
    hbond = float(hb_mask.sum()) * 2.5
    total = -(contact + hbond) + clash
    return dict(score=round(total, 2), contact=round(contact, 2),
                hbond=round(hbond, 2), clash=round(clash, 2),
                clashing_atoms=int((overlap > 0.4).any(axis=1).sum()))


def dock_pose(dx=0.0, dy=0.0, dz=0.0, rot_deg=0.0, axis="z", resn="THA",
              show=True):
    """Move the real ligand in the real gorge and score it."""
    atoms, X = ligand(resn)
    Y = move_ligand(dx, dy, dz, rot_deg, axis, resn)
    sc = score_pose(Y, resn)
    r = rmsd(X, Y)
    if show:
        prot, P = protein()
        d = np.linalg.norm(Y[:, None, :] - P[None, :, :], axis=2)
        nearby = np.where(d.min(axis=0) <= 8.0)[0]
        f, ax = _fig(7.2, 6.0)
        ax.scatter(P[nearby, 0], P[nearby, 1], s=14, color="#CBD5E1",
                   label="gorge atoms within 8 A")
        ax.scatter(X[:, 0], X[:, 1], s=70, color=MUTED, label="crystal pose")
        bad = np.zeros(len(Y), bool)
        ov = np.clip((np.array([VDW.get(a["elem"],1.7) for a in atoms])[:,None]
                      + np.array([VDW.get(p["elem"],1.7) for p in prot])[None,:]) - d, 0, None)
        bad = (ov > 0.4).any(axis=1)
        ax.scatter(Y[~bad, 0], Y[~bad, 1], s=90, color=SECOND, label="your pose")
        if bad.any():
            ax.scatter(Y[bad, 0], Y[bad, 1], s=130, color="#DC2626", marker="X",
                       label="clashing atom")
        ax.set_aspect("equal"); ax.legend(fontsize=8, loc="best")
        ax.set_xlabel("x (A)"); ax.set_ylabel("y (A)")
        ax.set_title(f"score {sc['score']:+.1f}    RMSD to crystal {r:.2f} A")
        plt.tight_layout(); plt.show()
    print(f"score            {sc['score']:+8.2f}   (more negative is better)")
    print(f"  contact        {sc['contact']:8.2f}")
    print(f"  hydrogen bonds {sc['hbond']:8.2f}")
    print(f"  clash penalty  {sc['clash']:8.2f}   from {sc['clashing_atoms']} atoms")
    print(f"RMSD to crystal  {r:8.2f} A")
    return dict(**sc, rmsd=round(r, 2))


def score_vs_truth(n=220, spread=4.0, seed=7, resn="THA", show=True):
    """Generate real perturbed poses; plot score against RMSD to the crystal."""
    rng = np.random.default_rng(seed)
    atoms, X = ligand(resn)
    rows = []
    for _ in range(n):
        t = rng.normal(0, spread / 2, 3)
        a = rng.uniform(-180, 180)
        ax_ = "xyz"[rng.integers(0, 3)]
        Y = move_ligand(*t, rot_deg=a, axis=ax_, resn=resn)
        sc = score_pose(Y, resn)
        rows.append((rmsd(X, Y), sc["score"], sc["clashing_atoms"]))
    R = np.array([r[0] for r in rows]); S = np.array([r[1] for r in rows])
    good_rmsd = R < 2.0
    best = int(np.argmin(S))
    if show:
        f, ax = _fig(9.0, 5.0)
        ax.scatter(R[~good_rmsd], S[~good_rmsd], s=26, color=MUTED,
                   label="wrong pose (RMSD >= 2 A)", alpha=.75)
        ax.scatter(R[good_rmsd], S[good_rmsd], s=40, color=PRIMARY,
                   label="correct pose (RMSD < 2 A)")
        ax.scatter([R[best]], [S[best]], s=150, marker="*", color=SECOND,
                   zorder=5, label="best-scoring pose")
        lo = float(S.min()); hi = float(np.percentile(S, 55))
        pad = max(10.0, 0.10 * (hi - lo)); off = int((S > hi + pad).sum())
        ax.set_ylim(lo - pad, hi + pad)
        if off:
            ax.text(0.99, 0.03, f"{off} heavily clashing poses lie above this axis",
                    transform=ax.transAxes, ha="right", va="bottom",
                    fontsize=8, color=MUTED)
        ax.axvline(2.0, color="#B45309", ls=":", lw=1.4)
        ax.set_xlabel("RMSD to the crystal pose (A)")
        ax.set_ylabel("score (more negative = better)")
        ax.legend(fontsize=8)
        ax.set_title(f"{n} real poses of tacrine in the real gorge")
        plt.tight_layout(); plt.show()
    picked_right = bool(R[best] < 2.0)
    print(f"{n} poses generated from the real crystal coordinates")
    print(f"  poses within 2 A of the crystal : {int(good_rmsd.sum())}")
    print(f"  best-scoring pose has RMSD      : {R[best]:.2f} A")
    print(f"  did the score pick a correct pose? {'yes' if picked_right else 'NO'}")
    return dict(n=n, correct_available=int(good_rmsd.sum()),
                best_rmsd=round(float(R[best]), 2),
                best_score=round(float(S[best]), 2),
                score_picked_correct=picked_right)


# ---------------------------------------------------------------- L27
def empty_space(probe=1.6, grid=1.0, around=9.0, resn="THA", show=True):
    """Find unfilled volume in the real gorge next to the bound ligand.

    Only gorge atoms are considered and the grid is processed in chunks, so a
    fine grid stays within memory.
    """
    if not isinstance(resn, str):
        raise TypeError("resn must be a residue name such as 'THA'; "
                        "did you mean empty_space(probe=%r)?" % resn)
    if grid < 0.3:
        raise ValueError("grid finer than 0.3 A is not useful here and is slow")
    atoms, X = ligand(resn)
    prot, Pall = protein()
    c = X.mean(axis=0)
    # prune to atoms that could possibly matter
    keep_p = np.linalg.norm(Pall - c, axis=1) <= (around + probe + 2.5)
    P = Pall[keep_p]
    rp = np.array([VDW.get(r["elem"], 1.7) for r in np.array(prot)[keep_p]])[None, :]
    rl = np.array([VDW.get(a["elem"], 1.7) for a in atoms])[None, :]
    rng_ = np.arange(-around, around + 1e-9, grid)
    G = np.array([[x, y, z] for x in rng_ for y in rng_ for z in rng_]) + c
    G = G[np.linalg.norm(G - c, axis=1) <= around]
    free = np.empty(len(G), bool)
    dlmin = np.empty(len(G))
    notlig = np.empty(len(G), bool)
    step = max(1, int(4e6 // max(len(P), 1)))
    for i in range(0, len(G), step):
        g = G[i:i + step]
        dp = np.linalg.norm(g[:, None, :] - P[None, :, :], axis=2)
        free[i:i + step] = (dp > (rp + probe)).all(axis=1)
        dl = np.linalg.norm(g[:, None, :] - X[None, :, :], axis=2)
        notlig[i:i + step] = (dl > (rl + probe)).all(axis=1)
        dlmin[i:i + step] = dl.min(axis=1)
    pocket = free & (dlmin < 8.0)
    unfilled = pocket & notlig
    if show:
        zc = float(X[:, 2].mean()); slab = 2.0
        sl = np.abs(G[:, 2] - zc) <= slab
        lig = np.abs(X[:, 2] - zc) <= slab
        f, ax = _fig(7.0, 6.0)
        ax.scatter(G[pocket & ~notlig & sl, 0], G[pocket & ~notlig & sl, 1],
                   s=9, color="#CBD5E1", label="taken up by the ligand")
        ax.scatter(G[unfilled & sl, 0], G[unfilled & sl, 1], s=12, color=OK,
                   label=f"free, probe {probe} A")
        ax.scatter(X[lig, 0], X[lig, 1], s=80, color=SECOND, label="tacrine")
        ax.set_aspect("equal"); ax.legend(fontsize=8, loc="upper right")
        ax.set_xlabel("x (A)"); ax.set_ylabel("y (A)")
        ax.set_title(f"a {2*slab:.0f} A slice through the gorge, not the whole "
                     f"volume\n{int((unfilled & sl).sum())} of the "
                     f"{int(unfilled.sum())} free points lie in this slice",
                     fontsize=10)
        plt.tight_layout(); plt.show()
    vol = float(unfilled.sum()) * grid ** 3
    print(f"probe radius             {probe} A")
    print(f"grid points sampled      {len(G):,} at {grid} A spacing")
    print(f"free and near the ligand {unfilled.sum():>8,}  -> about {vol:,.0f} A^3")
    print("\n  That volume is what a de novo program would try to fill, and why")
    print("  a first design should NOT fill all of it.")
    return dict(probe=probe, grid=grid, grid_points=len(G),
                unfilled=int(unfilled.sum()), volume_A3=round(vol, 1))


def score_ranking(n=220, spread=2.0, seed=7, top=10, resn="THA"):
    """Rank real poses by score and show the RMSD of each. The question is not
    only whether the top pose is right but how well the score SEPARATES."""
    rng = np.random.default_rng(seed)
    atoms, X = ligand(resn)
    rows = []
    for _ in range(n):
        t = rng.normal(0, spread / 2, 3)
        Y = move_ligand(*t, rot_deg=rng.uniform(-180, 180),
                        axis="xyz"[rng.integers(0, 3)], resn=resn)
        rows.append((rmsd(X, Y), score_pose(Y, resn)["score"]))
    rows.sort(key=lambda r: r[1])
    print(f"top {top} of {n} poses, ranked by score")
    print(f"  {'rank':>4}  {'score':>9}  {'RMSD':>6}   verdict")
    for i, (r, sc) in enumerate(rows[:top], 1):
        print(f"  {i:>4}  {sc:>9.2f}  {r:>5.2f} A   "
              f"{'correct' if r < 2 else 'WRONG POSE'}")
    wrong = sum(1 for r, _ in rows[:top] if r >= 2)
    print(f"\n  {wrong} of the top {top} scoring poses are the wrong pose.")
    return dict(top=top, wrong_in_top=wrong,
                rows=[(round(r, 2), round(s, 2)) for r, s in rows[:top]])


_RING = {"TRP": {"CD2", "CE2", "CE3", "CZ2", "CZ3", "CH2"},
         "PHE": {"CG", "CD1", "CD2", "CE1", "CE2", "CZ"},
         "TYR": {"CG", "CD1", "CD2", "CE1", "CE2", "CZ"},
         "HIS": {"CG", "ND1", "CD2", "CE1", "NE2"}}


def stacking(near=6.0, resn="THA", show=True):
    """Is the ligand sandwiched? Measure each nearby aromatic ring's position
    relative to the plane of the ligand itself."""
    atoms, X = ligand(resn)
    prot, P = protein()
    cen = X.mean(axis=0)
    nrm = np.linalg.svd(X - cen)[2][2]
    seen, rows = set(), []
    for j, r in enumerate(prot):
        kk = (r["resn"], r["resi"])
        if r["resn"] not in _RING or kk in seen:
            continue
        idx = [k for k, q in enumerate(prot)
               if q["resn"] == r["resn"] and q["resi"] == r["resi"]
               and q["name"] in _RING[r["resn"]]]
        if len(idx) < 5:
            continue
        Q = P[idx]
        qc = Q.mean(axis=0)
        if np.linalg.norm(qc - cen) > near + 3.0:
            continue
        seen.add(kk)
        qn = np.linalg.svd(Q - qc)[2][2]
        signed = float(np.dot(qc - cen, nrm))
        ang = float(np.degrees(np.arccos(min(1.0, abs(float(np.dot(nrm, qn)))))))
        rows.append((f"{r['resn']}{r['resi']}", signed,
                     float(np.linalg.norm(qc - cen)), ang))
    rows.sort(key=lambda t: t[2])
    rows = [t for t in rows if t[2] <= near + 1.0]
    if show:
        f, ax = _fig(7.6, 4.4)
        for nm, sg, dd, an in rows:
            st = an < 30
            ax.barh(nm, sg, height=.6, color=(PRIMARY if sg > 0 else SECOND),
                    alpha=(1.0 if st else 0.35),
                    hatch=(None if st else "///"), edgecolor="white")
            ax.text(sg + (0.2 if sg > 0 else -0.2), nm,
                    f"{an:.0f} deg" + ("" if st else "  edge-on"),
                    va="center", ha=("left" if sg > 0 else "right"),
                    fontsize=8, color=("#1F2937" if st else MUTED))
        ax.set_xlim(min(r[1] for r in rows) - 3.0, max(r[1] for r in rows) + 3.0)
        ax.axvline(0, color="#1F2937", lw=1.4)
        ax.set_xlabel("signed distance from the ligand's plane (A)")
        ax.set_title("opposite sides of zero = sandwiched;\nsolid bar = near-parallel = genuinely stacked", fontsize=10)
        plt.tight_layout(); plt.show()
    print("aromatic rings near the ligand, measured against the ligand's own plane")
    print(f"  {'residue':<9}{'side':>6}{'perp (A)':>10}{'centroid (A)':>14}"
          f"{'planes (deg)':>14}")
    for nm, sg, dd, an in rows:
        print(f"  {nm:<9}{('above' if sg > 0 else 'below'):>6}{sg:>10.2f}"
              f"{dd:>14.2f}{an:>14.1f}")
    above = [r for r in rows if r[1] > 0]
    below = [r for r in rows if r[1] < 0]
    print(f"\n  {len(above)} above the plane, {len(below)} below.")
    if above and below:
        print("  Rings on both sides: the ligand is sandwiched.")
    print("  A plane angle under about 30 degrees means the rings are "
          "roughly parallel,\n  which is face-to-face stacking rather than "
          "edge-on contact.")
    return dict(rows=[(n, round(s, 2), round(d, 2), round(a, 1))
                      for n, s, d, a in rows],
                above=len(above), below=len(below),
                sandwiched=bool(above and below))
