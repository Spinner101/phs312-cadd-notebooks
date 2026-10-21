# Structure provenance

The in-class activities for Lectures 22-27 measure a real crystal structure.

**PDB 1ACJ** — *Torpedo californica* acetylcholinesterase in complex with
tacrine (THA).

> Harel, M.; Schalk, I.; Ehret-Sabatier, L.; Bouet, F.; Goeldner, M.;
> Hirth, C.; Axelsen, P. H.; Silman, I.; Sussman, J. L.
> "Quaternary ligand binding to aromatic residues in the active-site gorge of
> acetylcholinesterase." *Proc. Natl. Acad. Sci. U.S.A.* **1993**, *90*,
> 9031-9035. DOI: 10.1073/pnas.90.19.9031

Protein Data Bank data are released without restriction
(https://www.rcsb.org/pages/usage-policy); please cite the primary reference
above and the PDB when reusing these materials.

## What was done to the file

`pdb_1acj.b64` is the deposited coordinate file with waters and ANISOU
records removed, then gzipped and base64-encoded. It retains **4,095 protein
atoms and the 15 atoms of tacrine**. Nothing else was altered: no
minimisation, no re-refinement, no added hydrogens. A round-trip decode was
checked against the original file.

The structure is embedded directly in each notebook, so the activities
**download nothing and transmit nothing**. No student data of any kind is
collected, which keeps the activities clear of FERPA and HIPAA concerns.

## What the notebooks compute

`tools/crystal.py` is the measurement library embedded in the notebooks. It
uses only NumPy and matplotlib - no RDKit, no network access. Everything it
reports is derived from the coordinates:

- bonds inferred from covalent radii; valence angles from those bonds
- ligand-protein contacts and van der Waals overlap
- aromatic ring stacking: signed distance from the ligand plane, interplanar angle
- side-chain chi-1 torsions and rotamer classification
- rigid-body ligand movement, RMSD to the crystal pose
- a transparent contact/hydrogen-bond/clash score, and score-versus-RMSD plots
- free volume beside the ligand by grid probing

Every numeric claim made in the notebook questions is checked against live
output by `verify_claims.py` in the build system.
