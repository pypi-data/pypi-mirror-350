"""
Classifies: CHEBI:35343 17beta-hydroxy steroid
"""
"""
Classifies: 17β-hydroxy steroid
Definition: A 17β-hydroxy steroid is defined as a steroid containing a fused carbocyclic nucleus with 4 rings – three 6‐membered (A, B, C rings) and one 5‐membered (D ring) – where one carbon in the five‐membered D–ring carries an –OH group at C17 with explicitly assigned (likely beta) stereochemistry.
The algorithm:
  1. Parse the SMILES.
  2. Identify candidate rings (5- or 6-membered mostly made of carbons).
  3. Build a “fusion graph” (rings fused if they share at least 2 atoms) and collect connected ring sets.
  4. Find a fused set with exactly 4 rings (3 six‐membered and 1 five‐membered), i.e. a steroid nucleus.
  5. From the nucleus, isolate the five–membered ring (assumed D–ring).
  6. For each carbon atom in the five–membered ring that is sp³, examine its neighbors.
     To be considered a candidate for the 17β –OH position, the carbon must have a single-bonded oxygen that carries at least one hydrogen, and aside from that oxygen (and hydrogens) every other heavy–atom neighbor must belong to the steroid nucleus. This is meant to ensure that the –OH is “integral” to the steroid core (and not part of a sugar or side–chain).
  7. If the candidate carbon has an explicitly set chiral tag then we return True with a note that the beta configuration is likely, otherwise the configuration is uncertain.
If any step fails, we return False with a reason.
"""

from rdkit import Chem
from rdkit.Chem import rdchem

def is_17beta_hydroxy_steroid(smiles: str):
    """
    Determines whether a molecule is a 17β-hydroxy steroid based on its SMILES string.
    
    The procedure is:
      (a) Parse the SMILES string.
      (b) Identify rings of size 5 or 6 that are mostly made of carbon:
          for 5-membered: require at least 4 carbons;
          for 6-membered: require at least 5 carbons.
      (c) Build a fusion graph among these candidate rings (two rings are fused if they share 2 or more atoms).
      (d) Find a fused component (connected set of rings) with exactly 4 rings: 3 six-membered and 1 five-membered.
      (e) From this nucleus, isolate the five-membered ring (the D-ring). Then, for each carbon (atom) from
          that ring (only sp3 carbons are considered) check for an attached -OH group.
          In addition, verify that aside from the oxygen the carbon is bonded only to atoms in the steroid nucleus.
      (f) If a candidate is found, return True along with an explanation indicating whether the –OH-bearing carbon
          has an explicit chiral tag (likely beta) or not.
    
    Args:
      smiles (str): SMILES string of the molecule.
    
    Returns:
      (bool, str): Tuple with True if the molecule appears to be a 17β-hydroxy steroid; otherwise False and an explanation.
    """
    # Parse the SMILES string.
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
    
    ring_info = mol.GetRingInfo()
    atom_rings = ring_info.AtomRings()
    if not atom_rings:
        return False, "No rings found in molecule"
    
    # Filter candidate rings: only those of size 5 or 6 which are largely carbocyclic.
    candidate_rings = []
    for ring in atom_rings:
        ring_size = len(ring)
        if ring_size not in (5, 6):
            continue
        n_carbons = sum(1 for idx in ring if mol.GetAtomWithIdx(idx).GetAtomicNum() == 6)
        if ring_size == 5 and n_carbons < 4:
            continue
        if ring_size == 6 and n_carbons < 5:
            continue
        candidate_rings.append(set(ring))
    
    if not candidate_rings:
        return False, "No 5- or 6-membered (mostly) carbocyclic rings found (steroid nucleus expected)"
    
    # Build a fusion graph among candidate rings: rings are fused if they share 2 or more atoms.
    n_rings = len(candidate_rings)
    fusion = {i: set() for i in range(n_rings)}
    for i in range(n_rings):
        for j in range(i+1, n_rings):
            if len(candidate_rings[i].intersection(candidate_rings[j])) >= 2:
                fusion[i].add(j)
                fusion[j].add(i)
    
    # Retrieve connected components in the fusion graph.
    visited = set()
    fused_components = []
    for i in range(n_rings):
        if i in visited:
            continue
        stack = [i]
        comp = set()
        while stack:
            cur = stack.pop()
            if cur in comp:
                continue
            comp.add(cur)
            visited.add(cur)
            for neigh in fusion[cur]:
                if neigh not in comp:
                    stack.append(neigh)
        fused_components.append(comp)
    
    # Look for a fused component that has exactly 4 rings:
    # count 3 six-membered rings and 1 five-membered ring.
    steroid_component = None
    for comp in fused_components:
        count6 = sum(1 for idx in comp if len(candidate_rings[idx]) == 6)
        count5 = sum(1 for idx in comp if len(candidate_rings[idx]) == 5)
        if count6 == 3 and count5 == 1:
            steroid_component = comp
            break
    if steroid_component is None:
        return False, "Steroid nucleus (3 six-membered and 1 five-membered fused rings) not found"
    
    # Collect all atom indices from the steroid nucleus.
    nucleus_atoms = set()
    five_membered_rings = []
    for idx in steroid_component:
        ring = candidate_rings[idx]
        nucleus_atoms.update(ring)
        if len(ring) == 5:
            five_membered_rings.append(ring)
    if not five_membered_rings:
        return False, "No 5-membered ring found in steroid nucleus (expected D-ring)"
    
    # Now examine each atom in the five-membered (D) ring.
    # Check for an -OH group attached to a sp3 carbon that is integral to the steroid nucleus.
    # "Integral" means that aside from the oxygen (and implicit hydrogens) every other heavy neighbor must be in the nucleus.
    for ring in five_membered_rings:
        for idx in ring:
            atom = mol.GetAtomWithIdx(idx)
            if atom.GetAtomicNum() != 6 or atom.GetHybridization() != rdchem.HybridizationType.SP3:
                continue
            # Check that aside from the oxygen (for -OH) all heavy neighbors belong to the nucleus.
            outside_neighbors = False
            candidate_O = None
            for nbr in atom.GetNeighbors():
                # Skip hydrogens (they might be implicit)
                if nbr.GetAtomicNum() == 1:
                    continue
                if nbr.GetAtomicNum() == 8:
                    # Look for an oxygen candidate that is single-bonded and carries at least one attached hydrogen.
                    bond = mol.GetBondBetweenAtoms(atom.GetIdx(), nbr.GetIdx())
                    if bond is None or bond.GetBondTypeAsDouble() > 1.0:
                        continue
                    if nbr.GetTotalNumHs() < 1:
                        continue
                    candidate_O = nbr.GetIdx()
                else:
                    # If a heavy neighbor is not in the steroid nucleus, then it might be a substituent.
                    if nbr.GetIdx() not in nucleus_atoms:
                        outside_neighbors = True
                        break
            if outside_neighbors or candidate_O is None:
                continue
            # A candidate -OH on an sp3 carbon in the 5-membered ring (D-ring) is found.
            if atom.GetChiralTag() != rdchem.ChiralType.CHI_UNSPECIFIED:
                reason = ("Steroid nucleus (3 six-membered and 1 five-membered fused rings) found and an -OH "
                          "group is attached on a chiral (likely beta) carbon in the five-membered D-ring "
                          "consistent with a 17β–OH substituent.")
                return True, reason
            else:
                reason = ("Steroid nucleus (3 six-membered and 1 five-membered fused rings) found and an -OH "
                          "group is attached on a carbon in the five-membered D-ring; however, stereochemistry "
                          "is undefined (thus beta configuration is uncertain).")
                return True, reason
    return False, ("No -OH group attached on a steroid-core carbon of the five-membered ring was found "
                   "(expected for 17β–OH substitution)")

# Example usage: (Run as script to test with one positive example)
if __name__ == "__main__":
    # Example positive case: kidjoranin-3-O-beta-digitoxopyranoside
    test_smiles = "[H][C@@]1(C[C@H](O)[C@H](O)[C@@H](C)O1)O[C@H]1CC[C@@]2(C)C(C1)=CC[C@]1(O)[C@]2([H])C[C@@H](OC(=O)\\C=C\\c2ccccc2)[C@]2(C)[C@@](O)(CC[C@]12O)C(C)=O"
    result, explanation = is_17beta_hydroxy_steroid(test_smiles)
    print(result, explanation)


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:35343',
                          'name': '17beta-hydroxy steroid',
                          'definition': 'A 17-hydroxy steroid in which the '
                                        'hydroxy group at position 17 has a '
                                        'beta-configuration.',
                          'parents': ['CHEBI:36838'],
                          'xrefs': [   'KEGG:C03051',
                                       'MetaCyc:17-beta-Hydroxysteroids'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 135,
                           'log_lines_of_code': 4.90527477843843,
                           'indent_by_line': [   1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 3,
                                                 2,
                                                 2,
                                                 3,
                                                 2,
                                                 3,
                                                 2,
                                                 1,
                                                 1,
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 3,
                                                 4,
                                                 4,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 3,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 3,
                                                 4,
                                                 3,
                                                 3,
                                                 3,
                                                 4,
                                                 5,
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 3,
                                                 1,
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 1,
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 3,
                                                 3,
                                                 4,
                                                 3,
                                                 3,
                                                 3,
                                                 3,
                                                 4,
                                                 4,
                                                 5,
                                                 4,
                                                 5,
                                                 5,
                                                 5,
                                                 6,
                                                 5,
                                                 6,
                                                 5,
                                                 4,
                                                 5,
                                                 5,
                                                 6,
                                                 6,
                                                 3,
                                                 4,
                                                 3,
                                                 3,
                                                 4,
                                                 4,
                                                 4,
                                                 4,
                                                 3,
                                                 4,
                                                 4,
                                                 4,
                                                 4,
                                                 1,
                                                 1,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 1],
                           'max_indent': 6,
                           'imports': [   'from rdkit import Chem',
                                          'from rdkit.Chem import rdchem'],
                           'imports_count': 2,
                           'methods_called': [   'intersection',
                                                 'GetIdx',
                                                 'GetHybridization',
                                                 'GetAtomicNum',
                                                 'GetBondTypeAsDouble',
                                                 'MolFromSmiles',
                                                 'GetAtomWithIdx',
                                                 'AtomRings',
                                                 'pop',
                                                 'GetChiralTag',
                                                 'GetBondBetweenAtoms',
                                                 'GetNeighbors',
                                                 'append',
                                                 'update',
                                                 'GetRingInfo',
                                                 'add',
                                                 'GetTotalNumHs'],
                           'methods_called_count': 17,
                           'smarts_strings': [],
                           'smarts_strings_count': 0,
                           'defs': ['is_17beta_hydroxy_steroid(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "No rings found in molecule"',
                                          'False, "No 5- or 6-membered '
                                          '(mostly) carbocyclic rings found '
                                          '(steroid nucleus expected)"',
                                          'False, "Steroid nucleus (3 '
                                          'six-membered and 1 five-membered '
                                          'fused rings) not found"',
                                          'False, "No 5-membered ring found in '
                                          'steroid nucleus (expected D-ring)"',
                                          'True, reason',
                                          'True, reason',
                                          'False, ("No -OH group attached on a '
                                          'steroid-core carbon of the '
                                          'five-membered ring was found "'],
                           'returns_count': 8,
                           'complexity': 7.381054955687685},
    'message': '\n'
               'Attempt failed: F1 score of 0.10693069306930693 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: '
               '[H][C@@]1(C[C@H](O)[C@H](O)[C@@H](C)O1)O[C@H]1CC[C@@]2(C)C(C1)=CC[C@]1(O)[C@]2([H])C[C@@H](OC(=O)\\C=C\\c2ccccc2)[C@]2(C)[C@@](O)(CC[C@]12O)C(C)=O '
               'NAME: kidjoranin-3-O-beta-digitoxopyranoside REASON: CORRECT '
               'Steroid nucleus (3 six-membered and 1 five-membered fused '
               'rings) found and an -OH group is attached on a chiral (likely '
               'beta) carbon in the five-membered D-ring consistent with a '
               '17β–OH substituent.\n'
               ' * SMILES: '
               'C1[C@@]2([C@]3(CC[C@]4([C@]([C@@]3(CC[C@]2(CC(C1)=O)[H])[H])(CC[C@@H]4O)[H])C)[H])C=O '
               'NAME: 19-oxo-5alpha-dihydrotestosterone REASON: CORRECT '
               'Steroid nucleus (3 six-membered and 1 five-membered fused '
               'rings) found and an -OH group is attached on a chiral (likely '
               'beta) carbon in the five-membered D-ring consistent with a '
               '17β–OH substituent.\n'
               ' * SMILES: '
               'C[C@@H]1C[C@@H]2[C@H]3CC[C@@]4(C)[C@@H](CC[C@]4(C)O)[C@@H]3CCC2=CC1=O '
               'NAME: 17beta-hydroxy-2alpha,17-dimethylestr-4-en-3-one REASON: '
               'CORRECT Steroid nucleus (3 six-membered and 1 five-membered '
               'fused rings) found and an -OH group is attached on a chiral '
               '(likely beta) carbon in the five-membered D-ring consistent '
               'with a 17β–OH substituent.\n'
               ' * SMILES: '
               'C1[C@]2([C@]3([C@@](C4=C(C=C(O)C=C4)CC3)(CC[C@@]2([C@@H](O)[C@@H]1O[C@@H]5O[C@@H]([C@H]([C@@H]([C@H]5O)O)O)C(O)=O)C)[H])[H])[H] '
               'NAME: estriol 16-O-(beta-D-glucuronide) REASON: CORRECT '
               'Steroid nucleus (3 six-membered and 1 five-membered fused '
               'rings) found and an -OH group is attached on a chiral (likely '
               'beta) carbon in the five-membered D-ring consistent with a '
               '17β–OH substituent.\n'
               ' * SMILES: '
               '[H][C@]12CCC(=O)C=C1CC[C@]1([H])[C@]2([H])CC[C@]2(C)[C@@H](O)CC[C@@]12[H] '
               'NAME: nandrolone REASON: CORRECT Steroid nucleus (3 '
               'six-membered and 1 five-membered fused rings) found and an -OH '
               'group is attached on a chiral (likely beta) carbon in the '
               'five-membered D-ring consistent with a 17β–OH substituent.\n'
               ' * SMILES: '
               '[H][C@]12CC[C@]3(C)[C@@H](O)CC[C@@]3([H])[C@]1([H])CCc1cc(OC(=O)N(CCCl)CCCl)ccc21 '
               'NAME: estramustine REASON: CORRECT Steroid nucleus (3 '
               'six-membered and 1 five-membered fused rings) found and an -OH '
               'group is attached on a chiral (likely beta) carbon in the '
               'five-membered D-ring consistent with a 17β–OH substituent.\n'
               ' * SMILES: '
               'C[C@]12CC[C@H]3[C@@H](CCC4=CC(=O)CC[C@]34C)[C@@H]1C[C@H](O)[C@@H]2O '
               'NAME: 16beta-hydroxytestosterone REASON: CORRECT Steroid '
               'nucleus (3 six-membered and 1 five-membered fused rings) found '
               'and an -OH group is attached on a chiral (likely beta) carbon '
               'in the five-membered D-ring consistent with a 17β–OH '
               'substituent.\n'
               ' * SMILES: '
               '[H][C@@]12CC[C@H](O)[C@@]1(C)CC[C@]1([H])C3=CC=C(O)C=C3C[C@@H](CCCCCCCCCCC(=O)N(C)CCCC)[C@@]21[H] '
               'NAME: ICI-164384 REASON: CORRECT Steroid nucleus (3 '
               'six-membered and 1 five-membered fused rings) found and an -OH '
               'group is attached on a chiral (likely beta) carbon in the '
               'five-membered D-ring consistent with a 17β–OH substituent.\n'
               ' * SMILES: '
               '[H][C@@]12CCC3=CC(=O)CC[C@]3(C=O)[C@@]1([H])CC[C@]1(C)[C@@H](O)CC[C@@]21[H] '
               'NAME: 19-oxotestosterone REASON: CORRECT Steroid nucleus (3 '
               'six-membered and 1 five-membered fused rings) found and an -OH '
               'group is attached on a chiral (likely beta) carbon in the '
               'five-membered D-ring consistent with a 17β–OH substituent.\n'
               ' * SMILES: '
               '[H][C@@]12C[C@H](O)[C@H](O)[C@@]1(C)CC[C@@]1([H])[C@@]2([H])CC=C2C[C@H](O)CC[C@]12C '
               'NAME: androst-5-ene-3alpha,16beta,17beta-triol REASON: CORRECT '
               'Steroid nucleus (3 six-membered and 1 five-membered fused '
               'rings) found and an -OH group is attached on a chiral (likely '
               'beta) carbon in the five-membered D-ring consistent with a '
               '17β–OH substituent.\n'
               ' * SMILES: '
               'C1=C(OS(O)(=O)=O)C=CC2=C1CC[C@]3([C@@]4(CC[C@]([C@]4(CC[C@@]32[H])C)(C#C)O)[H])[H] '
               'NAME: 17alpha-ethynylestradiol 3-sulfate REASON: CORRECT '
               'Steroid nucleus (3 six-membered and 1 five-membered fused '
               'rings) found and an -OH group is attached on a chiral (likely '
               'beta) carbon in the five-membered D-ring consistent with a '
               '17β–OH substituent.\n'
               ' * SMILES: '
               'C[C@]12CC[C@H]3[C@@H](CCc4cc(OC(=O)c5ccccc5)ccc34)[C@@H]1CC[C@@H]2O '
               'NAME: 17beta-estradiol 3-benzoate REASON: CORRECT Steroid '
               'nucleus (3 six-membered and 1 five-membered fused rings) found '
               'and an -OH group is attached on a chiral (likely beta) carbon '
               'in the five-membered D-ring consistent with a 17β–OH '
               'substituent.\n'
               ' * SMILES: '
               'C[C@@H]1C[C@@H]2[C@H]3CC[C@]4(C)[C@@H](O)CC[C@H]4[C@@H]3CCC2=CC1=O '
               'NAME: 17beta-hydroxy-2alpha-methylestr-4-en-3-one REASON: '
               'CORRECT Steroid nucleus (3 six-membered and 1 five-membered '
               'fused rings) found and an -OH group is attached on a chiral '
               '(likely beta) carbon in the five-membered D-ring consistent '
               'with a 17β–OH substituent.\n'
               ' * SMILES: '
               'C[C@]1(O)CC[C@H]2[C@@H]3CC[C@H]4Cc5[nH]ncc5C[C@]4(C)[C@H]3CC[C@]12C '
               'NAME: stanozolol REASON: CORRECT Steroid nucleus (3 '
               'six-membered and 1 five-membered fused rings) found and an -OH '
               'group is attached on a chiral (likely beta) carbon in the '
               'five-membered D-ring consistent with a 17β–OH substituent.\n'
               ' * SMILES: '
               'C[C@]12CC[C@H]3[C@@H](CCC4=CC(=O)C(O)C[C@]34C)[C@@H]1CC[C@@H]2O '
               'NAME: 2-hydroxytestosterone REASON: CORRECT Steroid nucleus (3 '
               'six-membered and 1 five-membered fused rings) found and an -OH '
               'group is attached on a chiral (likely beta) carbon in the '
               'five-membered D-ring consistent with a 17β–OH substituent.\n'
               ' * SMILES: '
               'C1[C@@]2([C@]3(CC[C@]4([C@]([C@@]3(CC=C2CC(C1)=O)[H])(CC[C@@H]4O)[H])C)[H])C '
               'NAME: 17beta-hydroxy-5-androsten-3-one REASON: CORRECT Steroid '
               'nucleus (3 six-membered and 1 five-membered fused rings) found '
               'and an -OH group is attached on a chiral (likely beta) carbon '
               'in the five-membered D-ring consistent with a 17β–OH '
               'substituent.\n'
               ' * SMILES: '
               'C1C(C=C2[C@](C1)([C@@]3([C@@](CC2)([C@@]4([H])[C@@](CC3)(C)[C@H]([C@@H](C4)O)O)[H])[H])C)=O '
               'NAME: 16alpha-hydroxytestosterone REASON: CORRECT Steroid '
               'nucleus (3 six-membered and 1 five-membered fused rings) found '
               'and an -OH group is attached on a chiral (likely beta) carbon '
               'in the five-membered D-ring consistent with a 17β–OH '
               'substituent.\n'
               ' * SMILES: '
               '[H][C@]12CC[C@]3(C)[C@@H](O)[C@H](O)C[C@@]3([H])[C@]1([H])CCc1cc(O[C@@H]3O[C@@H]([C@@H](O)[C@H](O)[C@H]3O)C(O)=O)ccc21 '
               'NAME: estriol 3-O-(beta-D-glucuronide) REASON: CORRECT Steroid '
               'nucleus (3 six-membered and 1 five-membered fused rings) found '
               'and an -OH group is attached on a chiral (likely beta) carbon '
               'in the five-membered D-ring consistent with a 17β–OH '
               'substituent.\n'
               ' * SMILES: '
               'C1=C2[C@]3(CC[C@]4([C@]([C@@]3(CCC2=C(C(=C1)O)O[C@H]5[C@@H]([C@H]([C@@H]([C@H](O5)C(=O)O)O)O)O)[H])(CC[C@@H]4O)[H])C)[H] '
               'NAME: 4-hydroxy-17beta-estradiol 4-O-(beta-D-glucuronide) '
               'REASON: CORRECT Steroid nucleus (3 six-membered and 1 '
               'five-membered fused rings) found and an -OH group is attached '
               'on a chiral (likely beta) carbon in the five-membered D-ring '
               'consistent with a 17β–OH substituent.\n'
               ' * SMILES: '
               'C1=C2C(C[C@H]([C@]3([C@@]4(CC[C@@H]([C@]4(CC[C@@]32[H])C)O)[H])[H])O)=CC(=C1)O '
               'NAME: 7alpha-hydroxyestradiol REASON: CORRECT Steroid nucleus '
               '(3 six-membered and 1 five-membered fused rings) found and an '
               '-OH group is attached on a chiral (likely beta) carbon in the '
               'five-membered D-ring consistent with a 17β–OH substituent.\n'
               ' * SMILES: '
               '[H][C@@]12CC[C@H](O)[C@@]1(C)CC[C@@]1([H])[C@@]2([H])CC=C2C[C@@H](O)CC[C@]12C '
               'NAME: androst-5-ene-3beta,17beta-diol REASON: CORRECT Steroid '
               'nucleus (3 six-membered and 1 five-membered fused rings) found '
               'and an -OH group is attached on a chiral (likely beta) carbon '
               'in the five-membered D-ring consistent with a 17β–OH '
               'substituent.\n'
               ' * SMILES: '
               '[H][C@@]12CCC3=CC(=O)CC[C@]3(CO)[C@@]1([H])CC[C@]1(C)[C@@H](O)CC[C@@]21[H] '
               'NAME: 19-hydroxytestosterone REASON: CORRECT Steroid nucleus '
               '(3 six-membered and 1 five-membered fused rings) found and an '
               '-OH group is attached on a chiral (likely beta) carbon in the '
               'five-membered D-ring consistent with a 17β–OH substituent.\n'
               ' * SMILES: '
               '[H][C@@]12CC[C@]3([H])[C@]([H])(CC[C@@]4(C)[C@@]3([H])CC[C@]4(C)O)[C@@]1(C)COC(=O)C2 '
               'NAME: oxandrolone REASON: CORRECT Steroid nucleus (3 '
               'six-membered and 1 five-membered fused rings) found and an -OH '
               'group is attached on a chiral (likely beta) carbon in the '
               'five-membered D-ring consistent with a 17β–OH substituent.\n'
               ' * SMILES: '
               'C1[C@]2(CC(CC([C@@]2([C@]3(CC[C@]4([C@]([C@@]3(C1)[H])(CC[C@@H]4O)[H])C)[H])C)=O)=O)[H] '
               'NAME: 17beta-hydroxyandrostan-1,3-dione REASON: CORRECT '
               'Steroid nucleus (3 six-membered and 1 five-membered fused '
               'rings) found and an -OH group is attached on a chiral (likely '
               'beta) carbon in the five-membered D-ring consistent with a '
               '17β–OH substituent.\n'
               ' * SMILES: '
               'C1[C@]2([C@]3([C@@](C4=C(C=C(OS(O)(=O)=O)C(=C4)O)CC3)(CC[C@@]2([C@@H](O)C1)C)[H])[H])[H] '
               'NAME: 2-hydroxy-17beta-estradiol 3-sulfate REASON: CORRECT '
               'Steroid nucleus (3 six-membered and 1 five-membered fused '
               'rings) found and an -OH group is attached on a chiral (likely '
               'beta) carbon in the five-membered D-ring consistent with a '
               '17β–OH substituent.\n'
               'False positives: SMILES: '
               'CO[C@H]1C[C@H](O[C@H]2CC[C@@]3(C)[C@H](CC[C@@H]4[C@@H]3[C@H](O)C[C@]3(C)[C@H](CC[C@]43O)C3=CC(=O)OC3)C2)O[C@@H](C)[C@@H]1O '
               'NAME: Divaricoside REASON: WRONGLY CLASSIFIED Steroid nucleus '
               '(3 six-membered and 1 five-membered fused rings) found and an '
               '-OH group is attached on a chiral (likely beta) carbon in the '
               'five-membered D-ring consistent with a 17β–OH substituent.\n'
               ' * SMILES: '
               'C[C@@H]1C[C@@]2(C)[C@@H](CC[C@H]3[C@@H]4CC[C@H](O)[C@@]4(C)CC[C@H]23)C[C@@H]1O '
               'NAME: 2alpha-Methyl-5alpha-androstane-3alpha,17beta-diol '
               'REASON: WRONGLY CLASSIFIED Steroid nucleus (3 six-membered and '
               '1 five-membered fused rings) found and an -OH group is '
               'attached on a chiral (likely beta) carbon in the five-membered '
               'D-ring consistent with a 17β–OH substituent.\n'
               ' * SMILES: '
               'O=C1C(C2=CC=C3[C@]4([C@]([C@@H]([C@H](C(=O)O)CCC(=C)C(C)C)[C@@H](C4)O)(C)CC=C3[C@@]2(C)CC1)C)(C)C '
               'NAME: '
               '16alpha-hydroxy-3-oxo-24-methyllanosta-5,7,9(11),24(31)-tetraen-21-oic '
               'acid REASON: WRONGLY CLASSIFIED Steroid nucleus (3 '
               'six-membered and 1 five-membered fused rings) found and an -OH '
               'group is attached on a chiral (likely beta) carbon in the '
               'five-membered D-ring consistent with a 17β–OH substituent.\n'
               ' * SMILES: '
               'C1=C2[C@]3(CC[C@]4([C@]([C@@]3(CCC2=C(C(=C1)O)O[C@H]5[C@@H]([C@H]([C@@H]([C@H](O5)C(=O)[O-])O)O)O)[H])(CC[C@@H]4O)[H])C)[H] '
               'NAME: 4-hydroxy-17beta-estradiol 4-O-(beta-D-glucuronide)(1-) '
               'REASON: WRONGLY CLASSIFIED Steroid nucleus (3 six-membered and '
               '1 five-membered fused rings) found and an -OH group is '
               'attached on a chiral (likely beta) carbon in the five-membered '
               'D-ring consistent with a 17β–OH substituent.\n'
               ' * SMILES: '
               'O=C1C2=C([C@@]3([C@@H](O)C[C@@H]([C@]3(C1)C)[C@@H](CC(O)C=C(C(=O)O)C)C)C)[C@@H](O)CC4[C@@]2(CC[C@@H](C4(C)C)O)C '
               'NAME: Ganolucidic acid gamma a REASON: WRONGLY CLASSIFIED '
               'Steroid nucleus (3 six-membered and 1 five-membered fused '
               'rings) found and an -OH group is attached on a chiral (likely '
               'beta) carbon in the five-membered D-ring consistent with a '
               '17β–OH substituent.\n'
               ' * SMILES: '
               'O=C1O[C@@]2(C(=C[C@@H]3O[C@](C[C@@]3(C2)O)(OC)C(=O)OC)C=4C1=C(O)C=C(OC)C4)C '
               'NAME: Xinshengin REASON: WRONGLY CLASSIFIED Steroid nucleus (3 '
               'six-membered and 1 five-membered fused rings) found and an -OH '
               'group is attached on a chiral (likely beta) carbon in the '
               'five-membered D-ring consistent with a 17β–OH substituent.\n'
               ' * SMILES: '
               '[H][C@]12CC[C@]3([H])[C@]([H])(CC[C@]4(C)[C@]([H])(CC[C@]34O)C3=CC(=O)OC3)[C@@]1(C)CC[C@@H](C2)O[C@@H]1O[C@@H](C)[C@H](O[C@@H]2O[C@H](CO)[C@@H](O)[C@H](O)[C@H]2O)[C@@H](OC)[C@H]1O '
               'NAME: digitoxigenin '
               '3-O-[beta-D-glucosyl-(1->4)-alpha-L-acofrioside] REASON: '
               'WRONGLY CLASSIFIED Steroid nucleus (3 six-membered and 1 '
               'five-membered fused rings) found and an -OH group is attached '
               'on a chiral (likely beta) carbon in the five-membered D-ring '
               'consistent with a 17β–OH substituent.\n'
               ' * SMILES: '
               'C[C@@]12[C@]([C@]3([C@](CC1)([C@@]4(C(C(=C3)C)=CC(CC4)=O)[H])[H])[H])(CC[C@@]2(C(C)=O)O)[H] '
               'NAME: nomegestrol REASON: WRONGLY CLASSIFIED Steroid nucleus '
               '(3 six-membered and 1 five-membered fused rings) found and an '
               '-OH group is attached on a chiral (likely beta) carbon in the '
               'five-membered D-ring consistent with a 17β–OH substituent.\n'
               ' * SMILES: '
               '[H][C@@]12CC=C3C[C@H](CC[C@]3(C)[C@@]1([H])CC[C@@]1(C)[C@@]2([H])C[C@H](O[C@@H]2OC[C@H](O)[C@H](O[C@@H]3OC[C@@H](O)[C@H](OC(=O)c4ccc(OC)c(OC)c4)[C@H]3O)[C@H]2OC(C)=O)[C@]1(O)[C@@H](C)C(=O)CCC(C)C)O[C@@H]1O[C@H](CO[C@@H]2O[C@H](CO)[C@@H](O[C@@H]3O[C@H](CO)[C@@H](O)[C@H](O)[C@H]3O)[C@H](O)[C@H]2O)[C@@H](O)[C@H](O)[C@H]1O '
               'NAME: '
               '3beta-[(O-beta-D-glucopyranosyl-(1->4)-O-beta-D-glucopyranosyl-(1->6)-beta-D-glucopyranosyl)oxy]-17alphahydroxy-16beta-[(O-(3-O-3,4-dimethoxybenzoyl-beta-D-xylopyranosyl)-(1->3)-2-O-acetyl-alpha-L-arabinopyranosyl)oxy]cholest-5-en-22-one '
               'REASON: WRONGLY CLASSIFIED Steroid nucleus (3 six-membered and '
               '1 five-membered fused rings) found and an -OH group is '
               'attached on a chiral (likely beta) carbon in the five-membered '
               'D-ring consistent with a 17β–OH substituent.\n'
               ' * SMILES: '
               'O=C1C=C2[C@@]3([C@H](C(C(=O)CC3)(C)C)C[C@@H]4[C@]2(O4)[C@]5([C@]1([C@@H](/C(=C/[C@@H]6OC(=O)[C@H](C6)C)/C)C[C@@H]5O)C)C)C '
               'NAME: Gibbosicolid B REASON: WRONGLY CLASSIFIED Steroid '
               'nucleus (3 six-membered and 1 five-membered fused rings) found '
               'and an -OH group is attached on a chiral (likely beta) carbon '
               'in the five-membered D-ring consistent with a 17β–OH '
               'substituent.\n'
               ' * SMILES: CC12CCC3C(C1CC[C@]2(C#C)O)CCC4=CC5=C(CC34C)C=NO5 '
               'NAME: LSM-6384 REASON: WRONGLY CLASSIFIED Steroid nucleus (3 '
               'six-membered and 1 five-membered fused rings) found and an -OH '
               'group is attached on a chiral (likely beta) carbon in the '
               'five-membered D-ring consistent with a 17β–OH substituent.\n'
               ' * SMILES: '
               'C[C@@]12[C@]([C@]3(C(=CC1)[C@]4(C)C(CC3)=CC(CC4)=O)[H])(CC[C@@]2(C(COC(C)=O)=O)O)[H] '
               'NAME: Anecortave acetate REASON: WRONGLY CLASSIFIED Steroid '
               'nucleus (3 six-membered and 1 five-membered fused rings) found '
               'and an -OH group is attached on a chiral (likely beta) carbon '
               'in the five-membered D-ring consistent with a 17β–OH '
               'substituent.\n'
               ' * SMILES: '
               'C1=C2C(CC[C@]3([C@@]4(CC[C@@H]([C@]4(CC[C@@]32[H])C)O)[H])[H])=CC(=C1)OS([O-])(=O)=O '
               'NAME: 17beta-estradiol 3-sulfate(1-) REASON: WRONGLY '
               'CLASSIFIED Steroid nucleus (3 six-membered and 1 five-membered '
               'fused rings) found and an -OH group is attached on a chiral '
               '(likely beta) carbon in the five-membered D-ring consistent '
               'with a 17β–OH substituent.\n'
               ' * SMILES: '
               'OC12C3C(C4(C(O)(CC3)CC(OC5OC(C(O)C(O)C5O)C)CC4)C)C(O)CC1(C(CC2)C=6COC(=O)C6)C '
               'NAME: Bipindogulomethyloside REASON: WRONGLY CLASSIFIED '
               'Steroid nucleus (3 six-membered and 1 five-membered fused '
               'rings) found and an -OH group is attached on a carbon in the '
               'five-membered D-ring; however, the stereochemistry at that '
               'carbon is undefined (thus beta configuration is uncertain).\n'
               ' * SMILES: '
               'O=C(OC[C@]1(O)[C@@H]2[C@@H](O)C3=CC[C@@H]4[C@@]([C@]3(C2)CC1)(CC[C@H]([C@]4(CO)C)O)C)C '
               'NAME: Aphidicolin A44 REASON: WRONGLY CLASSIFIED Steroid '
               'nucleus (3 six-membered and 1 five-membered fused rings) found '
               'and an -OH group is attached on a chiral (likely beta) carbon '
               'in the five-membered D-ring consistent with a 17β–OH '
               'substituent.\n'
               ' * SMILES: '
               'C1[C@H](O[C@@]2(O[C@H]([C@@H]([C@H]([C@@H]2OC(C)=O)OC)O)C)[H])C[C@]3([H])[C@@](C1)(C)[C@]4(CC[C@@]5(C)[C@]([C@@]64[C@@H](O6)C3)(O)CC[C@@H]5C7=CC(=O)OC7)[H] '
               'NAME: tanghinin REASON: WRONGLY CLASSIFIED Steroid nucleus (3 '
               'six-membered and 1 five-membered fused rings) found and an -OH '
               'group is attached on a chiral (likely beta) carbon in the '
               'five-membered D-ring consistent with a 17β–OH substituent.\n'
               ' * SMILES: '
               'O=C1C2=C([C@]3(CC[C@@H](C([C@@H]3C1)(C)C)O)C)CC[C@]4([C@]2(C[C@@H](O)[C@@H]4[C@H](C(=O)O)CCC(=C)C(C)C)C)C '
               'NAME: '
               '3beta,16alpha-dihydroxy-7-oxo-24-methyllanosta-8,24(31)-dien-21-oic '
               'acid REASON: WRONGLY CLASSIFIED Steroid nucleus (3 '
               'six-membered and 1 five-membered fused rings) found and an -OH '
               'group is attached on a chiral (likely beta) carbon in the '
               'five-membered D-ring consistent with a 17β–OH substituent.\n'
               ' * SMILES: '
               'O[C@@H]1[C@@]2([C@]([C@]3([C@@]([C@@]4([C@](CC3)(C[C@H](O[C@@H]5O[C@@H]([C@@H](O)[C@H](O)[C@H]5O)C(O)=O)CC4)[H])C)(CC2)[H])[H])(CC1)[H])C '
               'NAME: 3-alpha-Androstanediol glucuronide REASON: WRONGLY '
               'CLASSIFIED Steroid nucleus (3 six-membered and 1 five-membered '
               'fused rings) found and an -OH group is attached on a chiral '
               '(likely beta) carbon in the five-membered D-ring consistent '
               'with a 17β–OH substituent.\n'
               ' * SMILES: '
               'C[C@]12CC[C@H]3[C@@H](CCC4=C3CCC(=O)C4)[C@@H]1CC[C@@]2(O)C#C '
               'NAME: Norethynodrel REASON: WRONGLY CLASSIFIED Steroid nucleus '
               '(3 six-membered and 1 five-membered fused rings) found and an '
               '-OH group is attached on a chiral (likely beta) carbon in the '
               'five-membered D-ring consistent with a 17β–OH substituent.\n'
               ' * SMILES: '
               'O[C@@H]1[C@@]2([C@@]([C@H](C1)/C(/C)=C\\C(=O)CC(C)C(O)=O)(CC(=O)C=3[C@@]4([C@](C([C@@H](O)CC4)(C)C)(C[C@H](O)C23)[H])C)C)C '
               'NAME: Ganoderenic acid C REASON: WRONGLY CLASSIFIED Steroid '
               'nucleus (3 six-membered and 1 five-membered fused rings) found '
               'and an -OH group is attached on a chiral (likely beta) carbon '
               'in the five-membered D-ring consistent with a 17β–OH '
               'substituent.\n'
               ' * SMILES: '
               'C1[C@@]2([C@@]([C@@]3(C(C1)=CC(CC3)=O)C)([C@H](C[C@@]4([C@@](CC[C@@]24[H])(O)[C@@H](CO)O)C)O)[H])[H] '
               'NAME: 20beta-dihydrocortisol REASON: WRONGLY CLASSIFIED '
               'Steroid nucleus (3 six-membered and 1 five-membered fused '
               'rings) found and an -OH group is attached on a chiral (likely '
               'beta) carbon in the five-membered D-ring consistent with a '
               '17β–OH substituent.\n'
               ' * SMILES: '
               'O[C@H]1C([C@@]2([C@](C3[C@](C4C(=CC3)C([C@H](O)[C@@H](O)C4)(C)C)(C(=O)C2)C)(C1)C)C)C(O)(C)C(=O)CCC(C)=C '
               'NAME: '
               '(2S,3S,9R,13R,14S,16R)-2,3,16-Trihydroxy-17-[(2R)-2-hydroxy-6-methyl-3-oxohept-6-en-2-yl]-4,4,9,13,14-pentamethyl-1,2,3,7,8,10,12,15,16,17-decahydrocyclopenta[a]phenanthren-11-one '
               'REASON: WRONGLY CLASSIFIED Steroid nucleus (3 six-membered and '
               '1 five-membered fused rings) found and an -OH group is '
               'attached on a chiral (likely beta) carbon in the five-membered '
               'D-ring consistent with a 17β–OH substituent.\n'
               ' * SMILES: '
               'C[C@]1(O)CC[C@H]2[C@@H]3CC=C4C(F)(F)C(=O)CC[C@]4(C)[C@H]3CC[C@]12C '
               'NAME: '
               '4,4-Difluoro-17beta-hydroxy-17alpha-methyl-androst-5-en-3-one '
               'REASON: WRONGLY CLASSIFIED Steroid nucleus (3 six-membered and '
               '1 five-membered fused rings) found and an -OH group is '
               'attached on a chiral (likely beta) carbon in the five-membered '
               'D-ring consistent with a 17β–OH substituent.\n'
               ' * SMILES: '
               'O[C@@]12[C@]([C@]3([C@](CC1)([C@@H](O)CC3)C)[H])(CCC=4[C@]2(C)C=CC(=O)C4)[H] '
               'NAME: 9,17beta-hydroxy-androsta-1,4-dien-3-one REASON: WRONGLY '
               'CLASSIFIED Steroid nucleus (3 six-membered and 1 five-membered '
               'fused rings) found and an -OH group is attached on a chiral '
               '(likely beta) carbon in the five-membered D-ring consistent '
               'with a 17β–OH substituent.\n'
               ' * SMILES: '
               '[H][C@]12CC[C@@]3(C)[C@]([H])([C@H](C)CCC=C(C)C)[C@@H](O)C[C@]3(C)C1=CC[C@@]1([H])C(C)(C)C(=O)CC[C@]21C '
               'NAME: kulinone REASON: WRONGLY CLASSIFIED Steroid nucleus (3 '
               'six-membered and 1 five-membered fused rings) found and an -OH '
               'group is attached on a chiral (likely beta) carbon in the '
               'five-membered D-ring consistent with a 17β–OH substituent.\n'
               'False negatives: NONE\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'O=C(N[C@@H](C(O)(C)C)C)[C@H]([C@@]1([C@@]2([C@@](CC1)(/C(/CCC2)=C/C=C\\3/C[C@@H](O)C[C@H](O)C3=C)[H])C)[H])C',
                                     'name': '1alpha,25-dihydroxy-24-oxo-23-azavitamin '
                                             'D2 / '
                                             '1alpha,25-dihydroxy-24-oxo-23-azaergocalciferol',
                                     'reason': 'Steroid nucleus (3 '
                                               'six-membered and 1 '
                                               'five-membered fused rings) not '
                                               'found'},
                                 {   'smiles': 'CCCCCCCCCCCCCCCCCCC(O)C([O-])=O',
                                     'name': '2-hydroxyarachidate',
                                     'reason': 'No rings found in molecule'},
                                 {   'smiles': 'C[C@@H](CN([C@@H](C)CO)C(=O)NC1=CC=C(C=C1)C(F)(F)F)[C@@H](CN(C)C(=O)C2CCOCC2)OC',
                                     'name': 'N-[(2S,3S)-4-[[(2S)-1-hydroxypropan-2-yl]-[[4-(trifluoromethyl)phenyl]carbamoyl]amino]-2-methoxy-3-methylbutyl]-N-methyloxane-4-carboxamide',
                                     'reason': 'Steroid nucleus (3 '
                                               'six-membered and 1 '
                                               'five-membered fused rings) not '
                                               'found'},
                                 {   'smiles': 'CC(=O)CC\\C=C(/C)CCC=C(C)C',
                                     'name': 'geranyl acetone',
                                     'reason': 'No rings found in molecule'},
                                 {   'smiles': 'O([C@H]1[C@H](O)[C@H](O[C@H](O)[C@H]1O)CO[C@H]2O[C@@H]([C@@H](O)[C@H](O)[C@@H]2O)CO)[C@H]3O[C@@H]([C@@H](O)[C@H](O)[C@@H]3O[C@H]4O[C@@H]([C@@H](O)[C@H](O)[C@@H]4O)CO)CO',
                                     'name': '(2S,3S,4S,5S,6R)-2-[[(2R,3R,4S,5S,6S)-4-[(2R,3S,4S,5S,6R)-4,5-Dihydroxy-6-(hydroxymethyl)-3-[(2R,3S,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-3,5,6-trihydroxyoxan-2-yl]methoxy]-6-(hydroxymethyl)oxane-3,4,5-triol',
                                     'reason': 'Steroid nucleus (3 '
                                               'six-membered and 1 '
                                               'five-membered fused rings) not '
                                               'found'},
                                 {   'smiles': 'O=C(OC1=C(C(O)=C(C(=O)O)C(=C1C)C)C)C2=C(OC)C(=C(OC(=O)C3=C(O)C=C(O)C=C3C)C=C2C)C',
                                     'name': 'Thielavin Z5',
                                     'reason': 'Steroid nucleus (3 '
                                               'six-membered and 1 '
                                               'five-membered fused rings) not '
                                               'found'},
                                 {   'smiles': '[C@@H]1([C@@H]([C@H]([C@@H]([C@H](O1)CO)O)O)NC(C)=O)O[C@@H]2[C@@H]([C@H](C(O[C@@H]2CO)O)O)O',
                                     'name': 'beta-D-GlcpNAc-(1->4)-D-Galp',
                                     'reason': 'Steroid nucleus (3 '
                                               'six-membered and 1 '
                                               'five-membered fused rings) not '
                                               'found'},
                                 {   'smiles': 'CN(C)C(=O)C1=CC=C(C=C1)C2=CC=C(C=C2)[C@@H]3[C@H]4CN(CC(=O)N4[C@H]3CO)C(=O)CC5CC5',
                                     'name': '4-[4-[(6S,7R,8R)-4-(2-cyclopropyl-1-oxoethyl)-8-(hydroxymethyl)-2-oxo-1,4-diazabicyclo[4.2.0]octan-7-yl]phenyl]-N,N-dimethylbenzamide',
                                     'reason': 'Steroid nucleus (3 '
                                               'six-membered and 1 '
                                               'five-membered fused rings) not '
                                               'found'},
                                 {   'smiles': 'CCCCCCCCCCCCCCCCCCCCC=C',
                                     'name': '1-docosene',
                                     'reason': 'No rings found in molecule'},
                                 {   'smiles': 'C([C@@](OC(=O)CCC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)([H])COC(=O)CC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)OC(=O)CCCCC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC',
                                     'name': 'TG(22:5(7Z,10Z,13Z,16Z,19Z)/20:5(5Z,8Z,11Z,14Z,17Z)/22:6(4Z,7Z,10Z,13Z,16Z,19Z))[iso6]',
                                     'reason': 'No rings found in molecule'}],
    'sample_false_negatives': [   {   'smiles': 'C[C@@H]1C[C@@H]2[C@H]3CC[C@@]4(C)[C@@H](CC[C@]4(C)O)[C@@H]3CCC2=CC1=O',
                                      'name': '17beta-hydroxy-2alpha,17-dimethylestr-4-en-3-one',
                                      'reason': 'No -OH group attached on a '
                                                'steroid-core carbon of the '
                                                'five-membered ring was found '
                                                '(expected for 17β–OH '
                                                'substitution)'},
                                  {   'smiles': 'C1=C(OS(O)(=O)=O)C=CC2=C1CC[C@]3([C@@]4(CC[C@]([C@]4(CC[C@@]32[H])C)(C#C)O)[H])[H]',
                                      'name': '17alpha-ethynylestradiol '
                                              '3-sulfate',
                                      'reason': 'No -OH group attached on a '
                                                'steroid-core carbon of the '
                                                'five-membered ring was found '
                                                '(expected for 17β–OH '
                                                'substitution)'},
                                  {   'smiles': 'C[C@]1(O)CC[C@H]2[C@@H]3CC[C@H]4Cc5[nH]ncc5C[C@]4(C)[C@H]3CC[C@]12C',
                                      'name': 'stanozolol',
                                      'reason': 'No -OH group attached on a '
                                                'steroid-core carbon of the '
                                                'five-membered ring was found '
                                                '(expected for 17β–OH '
                                                'substitution)'},
                                  {   'smiles': '[H][C@@]12CC[C@]3([H])[C@]([H])(CC[C@@]4(C)[C@@]3([H])CC[C@]4(C)O)[C@@]1(C)COC(=O)C2',
                                      'name': 'oxandrolone',
                                      'reason': 'No -OH group attached on a '
                                                'steroid-core carbon of the '
                                                'five-membered ring was found '
                                                '(expected for 17β–OH '
                                                'substitution)'},
                                  {   'smiles': 'C[C@]12CC[C@H]3[C@@H](CCC4=CC(=O)CC[C@H]34)[C@@H]1CC[C@@]2(O)C#C',
                                      'name': 'norethisterone',
                                      'reason': 'No -OH group attached on a '
                                                'steroid-core carbon of the '
                                                'five-membered ring was found '
                                                '(expected for 17β–OH '
                                                'substitution)'},
                                  {   'smiles': '[H][C@@]12CCC3=CC(=O)CCC3=C1C=C[C@@]1(C)[C@@]2([H])CC[C@]1(C)O',
                                      'name': '17beta-hydroxy-17-methylestra-4,9,11-trien-3-one',
                                      'reason': 'No -OH group attached on a '
                                                'steroid-core carbon of the '
                                                'five-membered ring was found '
                                                '(expected for 17β–OH '
                                                'substitution)'},
                                  {   'smiles': '[H][C@]12CCC(=O)C=C1CC[C@@]1([H])[C@]3([H])CC[C@@](O)(C#C)[C@@]3(CC)CC(=C)[C@]21[H]',
                                      'name': 'etonogestrel',
                                      'reason': 'No -OH group attached on a '
                                                'steroid-core carbon of the '
                                                'five-membered ring was found '
                                                '(expected for 17β–OH '
                                                'substitution)'},
                                  {   'smiles': '[H][C@]12CCCC=C1CC[C@@]1([H])[C@]3([H])CC[C@@](O)(C#C)[C@@]3(CC)CC(=C)[C@]21[H]',
                                      'name': 'desogestrel',
                                      'reason': 'No -OH group attached on a '
                                                'steroid-core carbon of the '
                                                'five-membered ring was found '
                                                '(expected for 17β–OH '
                                                'substitution)'},
                                  {   'smiles': '[H][C@]12CC[C@H](O)C=C1CC[C@]1([H])[C@]2([H])CC[C@@]2(C)[C@@]1([H])CC[C@@]2(O)C#C',
                                      'name': 'ethynodiol',
                                      'reason': 'No -OH group attached on a '
                                                'steroid-core carbon of the '
                                                'five-membered ring was found '
                                                '(expected for 17β–OH '
                                                'substitution)'},
                                  {   'smiles': 'CC[C@]1(O)CC[C@H]2[C@@H]3CCC4=CCCC[C@@H]4[C@H]3CC[C@]12C',
                                      'name': 'ethylestrenol',
                                      'reason': 'No -OH group attached on a '
                                                'steroid-core carbon of the '
                                                'five-membered ring was found '
                                                '(expected for 17β–OH '
                                                'substitution)'}],
    'attempt': 5,
    'reasoning': 'Below is our improved solution. In our reasoning we '
                 'suspected that our previous “steroid nucleus” detector was '
                 'too liberal. In particular, it would flag any molecule that '
                 'had four fused rings (three 6‐membered and one 5‐membered) '
                 'and then simply look for an –OH on any sp³ carbon in the '
                 '5‐membered ring. That procedure could “catch” –OH groups '
                 'that are not really at the 17–position (or that lie on a '
                 'sugar or other substituent fused to the steroid nucleus) and '
                 'therefore produce false positives. In our new approach we '
                 'still (1) look for the fused steroid nucleus, but (2) once '
                 'we identify the unique five‐membered (D) ring we further '
                 'require that any candidate –OH comes from a carbon that (a) '
                 'is part of the steroid nucleus and (b) has all other '
                 'heavy–atom neighbors coming from the nucleus (except for the '
                 'oxygen). This extra filtering is intended to eliminate –OH '
                 'groups from mis‐attached substituents. Finally, if on the '
                 'candidate carbon we see an explicit chiral tag we assume '
                 '“likely beta” (otherwise the configuration is uncertain).\n'
                 '\n'
                 'Below is our complete code in a single valid Python code '
                 'block.\n'
                 '\n'
                 '------------------------------------------------',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 70,
    'num_false_positives': 983,
    'num_true_negatives': 141236,
    'num_false_negatives': 11,
    'num_negatives': None,
    'precision': 0.06647673314339982,
    'recall': 0.8641975308641975,
    'f1': 0.1234567901234568,
    'accuracy': 0.9930147575544624,
    'negative_predictive_value': 0.9999221222397644}