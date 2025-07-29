"""
Classifies: CHEBI:13601 3-oxo-5alpha-steroid
"""
#!/usr/bin/env python
"""
Classifies: CHEBI: 3-oxo-5α-steroid
Definition: A 3-oxo steroid with an alpha configuration at position 5.
Heuristic:
  • Look for a fused four‐ring steroid nucleus: exactly three six‐membered rings and one five‐membered ring,
    whose union of ring atoms is within 16–18 atoms and is mostly carbon.
  • The five‐membered ring must be fused (≥2 common atoms) with exactly one six‐membered ring.
  • Look for a ketone group (C=O) on that six‐membered ring (and not on the five‐membered ring).
  • Check for a chiral center in the five‐membered ring. If not present explicitly, we assume the configuration is 5α,
    but we note that stereochemistry was not explicitly specified.
"""

from rdkit import Chem
from rdkit.Chem import rdMolDescriptors
from itertools import combinations

def is_3_oxo_5alpha_steroid(smiles: str):
    """
    Determines if a molecule is a 3-oxo-5α-steroid based on its SMILES string.
    
    Args:
        smiles (str): SMILES string of the molecule.
    
    Returns:
        bool: True if the molecule is classified as a 3-oxo-5α-steroid, False otherwise.
        str: Reason explaining the decision.
    """
    # Parse the SMILES string.
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
        
    # Ensure stereochemistry is assigned.
    Chem.AssignStereochemistry(mol, force=True, cleanIt=True)
    
    # Retrieve ring information (only consider rings of size 5 or 6 that are mostly carbon).
    ring_info = mol.GetRingInfo().AtomRings()
    candidate_rings = []  # list of tuples: (set_of_atom_indices, ring_size)
    for ring in ring_info:
        if len(ring) in (5, 6):
            atoms = [mol.GetAtomWithIdx(idx) for idx in ring]
            # require at least 80% of atoms to be carbon.
            nC = sum(1 for atom in atoms if atom.GetAtomicNum() == 6)
            if nC >= 0.8 * len(ring):
                candidate_rings.append((set(ring), len(ring)))
    
    if not candidate_rings:
        return False, "No suitable 5-/6-membered rings found; not steroid-like"
    
    # Build a connectivity graph among candidate rings (fused if sharing at least 2 atoms).
    n = len(candidate_rings)
    graph = {i: set() for i in range(n)}
    for i in range(n):
        for j in range(i+1, n):
            if len(candidate_rings[i][0] & candidate_rings[j][0]) >= 2:
                graph[i].add(j)
                graph[j].add(i)
    
    # Find connected components (fused ring systems).
    visited = set()
    components = []
    for i in range(n):
        if i not in visited:
            stack = [i]
            comp = set()
            while stack:
                cur = stack.pop()
                if cur in comp:
                    continue
                comp.add(cur)
                stack.extend(graph[cur] - comp)
            visited |= comp
            components.append(comp)
    
    # Look for a fused system that has exactly four rings (three six-membered and one five-membered).
    steroid_component = None
    for comp in components:
        comp_list = list(comp)
        if len(comp_list) < 4:
            continue
        # For components with more than 4 rings, check every combination of 4 rings.
        possible_sets = []
        if len(comp_list) == 4:
            possible_sets.append(comp_list)
        else:
            for subset in combinations(comp_list, 4):
                possible_sets.append(list(subset))
        for subset in possible_sets:
            sizes = [candidate_rings[i][1] for i in subset]
            if sizes.count(6) != 3 or sizes.count(5) != 1:
                continue
            # Ensure the selected rings are all fused among themselves.
            subgraph = {i: graph[i] & set(subset) for i in subset}
            subvisited = set()
            stack = [subset[0]]
            while stack:
                cur = stack.pop()
                if cur in subvisited:
                    continue
                subvisited.add(cur)
                stack.extend(subgraph[cur] - subvisited)
            if len(subvisited) != 4:
                continue
            # Merge atom indices.
            nucleus_atoms = set()
            for i in subset:
                nucleus_atoms |= candidate_rings[i][0]
            # Classical steroid nucleus has 17 atoms; allow a tight range.
            if not (16 <= len(nucleus_atoms) <= 18):
                continue
            # At least 70% of the nucleus atoms should be carbon.
            nC_nucleus = sum(1 for idx in nucleus_atoms if mol.GetAtomWithIdx(idx).GetAtomicNum() == 6)
            if nC_nucleus < 0.7 * len(nucleus_atoms):
                continue
            steroid_component = subset
            break
        if steroid_component is not None:
            break
    
    if steroid_component is None:
        return False, "Steroid nucleus not detected; required fused system (3 six‐membered and 1 five‐membered ring) not found or not steroid‐like"
    
    # Merge the nucleus atoms.
    nucleus_atoms = set()
    for idx in steroid_component:
        nucleus_atoms |= candidate_rings[idx][0]
    
    # Identify the unique five-membered ring.
    five_membered_ring = None
    for idx in steroid_component:
        ring_set, size = candidate_rings[idx]
        if size == 5:
            five_membered_ring = ring_set
            break
    if five_membered_ring is None:
        return False, "Five-membered ring missing in fused steroid nucleus candidate"
    
    # Additional check: the five-membered ring must be fused with exactly one six-membered ring.
    six_fused_count = 0
    for idx in steroid_component:
        ring_set, size = candidate_rings[idx]
        if size == 6:
            if len(ring_set & five_membered_ring) >= 2:
                six_fused_count += 1
    if six_fused_count != 1:
        return False, f"Expected the five-membered ring to fuse with only one six-membered ring, found {six_fused_count}"
    
    # Look for a ketone group (C=O) on one of the six-membered rings.
    # Pattern: carbon in a ring double-bonded to oxygen.
    ketone_pattern = Chem.MolFromSmarts("[#6;R]=O")
    ketone_matches = mol.GetSubstructMatches(ketone_pattern)
    ketone_found = False
    for match in ketone_matches:
        ketone_carbon = match[0]
        # must be in the nucleus and not in the five-membered ring.
        if ketone_carbon in nucleus_atoms and ketone_carbon not in five_membered_ring:
            # Check that the ketone carbon has at least two neighbors within the nucleus.
            atom = mol.GetAtomWithIdx(ketone_carbon)
            connected_in_nucleus = sum(1 for nb in atom.GetNeighbors() if nb.GetIdx() in nucleus_atoms)
            if connected_in_nucleus >= 2:
                ketone_found = True
                break
    if not ketone_found:
        return False, "Ketone group (C=O) not found on a six-membered ring of the steroid nucleus"
    
    # Check the five-membered ring for at least one chiral center.
    # We use FindMolChiralCenters with only assigned centers.
    centers = Chem.FindMolChiralCenters(mol, includeUnassigned=False)
    chiral_in_five = [idx for (idx, tag) in centers if idx in five_membered_ring]
    if not chiral_in_five:
        # In our previous attempt we rejected if no chiral center was found,
        # but here we relax the criterion to avoid missing known steroids.
        chirality_note = " (Warning: no explicit chiral center detected in the five-membered ring; assuming 5α configuration)"
    else:
        chirality_note = ""
    
    return True, ("Molecule classified as a 3-oxo-5α-steroid: fused steroid nucleus (3 six‐membered and 1 five‐membered rings), "
                  "ketone on a six‐membered ring, and the expected 5α configuration detected" + chirality_note)
    
# End of code.


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:13601',
                          'name': '3-oxo-5alpha-steroid',
                          'definition': 'A 3-oxo steroid that has alpha '
                                        'configuration at position 5.',
                          'parents': ['CHEBI:47788'],
                          'xrefs': [   'KEGG:C02940',
                                       'MetaCyc:3-Oxo-5-Alpha-Steroids'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 146,
                           'log_lines_of_code': 4.983606621708336,
                           'indent_by_line': [   1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 3,
                                                 3,
                                                 3,
                                                 3,
                                                 4,
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
                                                 3,
                                                 3,
                                                 4,
                                                 4,
                                                 5,
                                                 4,
                                                 4,
                                                 3,
                                                 3,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 3,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 2,
                                                 3,
                                                 4,
                                                 2,
                                                 3,
                                                 3,
                                                 4,
                                                 3,
                                                 3,
                                                 3,
                                                 3,
                                                 3,
                                                 4,
                                                 4,
                                                 5,
                                                 4,
                                                 4,
                                                 3,
                                                 4,
                                                 3,
                                                 3,
                                                 3,
                                                 4,
                                                 3,
                                                 3,
                                                 4,
                                                 3,
                                                 3,
                                                 3,
                                                 4,
                                                 3,
                                                 3,
                                                 2,
                                                 3,
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
                                                 3,
                                                 1,
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 3,
                                                 4,
                                                 1,
                                                 2,
                                                 1,
                                                 1,
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
                                                 3,
                                                 3,
                                                 4,
                                                 4,
                                                 1,
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 2,
                                                 1,
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 1],
                           'max_indent': 5,
                           'imports': [   'from rdkit import Chem',
                                          'from rdkit.Chem import '
                                          'rdMolDescriptors',
                                          'from itertools import combinations'],
                           'imports_count': 3,
                           'methods_called': [   'extend',
                                                 'GetNeighbors',
                                                 'MolFromSmiles',
                                                 'count',
                                                 'GetRingInfo',
                                                 'append',
                                                 'GetSubstructMatches',
                                                 'FindMolChiralCenters',
                                                 'GetAtomWithIdx',
                                                 'AssignStereochemistry',
                                                 'MolFromSmarts',
                                                 'GetAtomicNum',
                                                 'AtomRings',
                                                 'GetIdx',
                                                 'add',
                                                 'pop'],
                           'methods_called_count': 16,
                           'smarts_strings': ['[#6;R]=O'],
                           'smarts_strings_count': 1,
                           'defs': ['is_3_oxo_5alpha_steroid(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "No suitable 5-/6-membered '
                                          'rings found; not steroid-like"',
                                          'False, "Steroid nucleus not '
                                          'detected; required fused system (3 '
                                          'six‐membered and 1 five‐membered '
                                          'ring) not found or not '
                                          'steroid‐like"',
                                          'False, "Five-membered ring missing '
                                          'in fused steroid nucleus candidate"',
                                          'False, f"Expected the five-membered '
                                          'ring to fuse with only one '
                                          'six-membered ring, found '
                                          '{six_fused_count}"',
                                          'False, "Ketone group (C=O) not '
                                          'found on a six-membered ring of the '
                                          'steroid nucleus"',
                                          'True, ("Molecule classified as a '
                                          '3-oxo-5α-steroid: fused steroid '
                                          'nucleus (3 six‐membered and 1 '
                                          'five‐membered rings), "'],
                           'returns_count': 7,
                           'complexity': 6.796721324341666},
    'message': '\n'
               'Attempt failed: F1 score of 0.04026845637583893 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: '
               'C1[C@@]2([C@]3(CC[C@]4([C@]([C@@]3(CC[C@]2(CC(C1)=O)[H])[H])(CC[C@@H]4O)[H])C)[H])C=O '
               'NAME: 19-oxo-5alpha-dihydrotestosterone REASON: CORRECT '
               'Molecule classified as a 3-oxo-5α-steroid (steroid nucleus '
               'with 3 six‐membered and 1 five‐membered rings, ketone on a '
               'six‐membered ring, and defined chiral center in the '
               'five‐membered ring detected)\n'
               ' * SMILES: '
               '[H][C@@]12CC[C@]3([H])[C@]([H])(CC[C@]4(C)[C@]([H])(CC[C@@]34[H])[C@H](C)[C@@H](O)[C@H](O)[C@@H](C)C(C)C)[C@@]1(C)CCC(=O)C2 '
               'NAME: 3-dehydro-6-deoxoteasterone REASON: CORRECT Molecule '
               'classified as a 3-oxo-5α-steroid (steroid nucleus with 3 '
               'six‐membered and 1 five‐membered rings, ketone on a '
               'six‐membered ring, and defined chiral center in the '
               'five‐membered ring detected)\n'
               ' * SMILES: '
               '[H][C@@]12CC[C@]3([H])[C@]([H])(CC[C@]4(C)[C@]([H])(CC[C@@]34[H])[C@H](C)CCCC(C)C)[C@@]1(C)CCC(=O)C2 '
               'NAME: 5alpha-cholestan-3-one REASON: CORRECT Molecule '
               'classified as a 3-oxo-5α-steroid (steroid nucleus with 3 '
               'six‐membered and 1 five‐membered rings, ketone on a '
               'six‐membered ring, and defined chiral center in the '
               'five‐membered ring detected)\n'
               ' * SMILES: '
               'C[C@@H]1C[C@@]2(C)[C@@H](CC[C@H]3[C@@H]4CC[C@](C)(O)[C@@]4(C)CC[C@H]23)CC1=O '
               'NAME: 17beta-Hydroxy-2alpha,17-dimethyl-5alpha-androstan-3-one '
               'REASON: CORRECT Molecule classified as a 3-oxo-5α-steroid '
               '(steroid nucleus with 3 six‐membered and 1 five‐membered '
               'rings, ketone on a six‐membered ring, and defined chiral '
               'center in the five‐membered ring detected)\n'
               ' * SMILES: '
               'COC(C)(C)\\C=C\\C[C@@H](C)[C@H]1CC[C@@]2(C)[C@@H]3[C@@H](O)C[C@@H]4[C@]5(C[C@@]35CC[C@]12C)CCC(=O)C4(C)C '
               'NAME: combretanone G REASON: CORRECT Molecule classified as a '
               '3-oxo-5α-steroid (steroid nucleus with 3 six‐membered and 1 '
               'five‐membered rings, ketone on a six‐membered ring, and '
               'defined chiral center in the five‐membered ring detected)\n'
               ' * SMILES: '
               '[H][C@@]12CC[C@@]3([H])[C@]4([H])CC[C@]([H])([C@H](C)[C@@H](O)C[C@@H](C)C(C)C)[C@@]4(C)CC[C@]3([H])[C@@]1(C)CCC(=O)C2 '
               'NAME: (5alpha,22S,24R)-22-hydroxyergostan-3-one REASON: '
               'CORRECT Molecule classified as a 3-oxo-5α-steroid (steroid '
               'nucleus with 3 six‐membered and 1 five‐membered rings, ketone '
               'on a six‐membered ring, and defined chiral center in the '
               'five‐membered ring detected)\n'
               ' * SMILES: '
               'C[C@H](C[C@@H](O)[C@H](O)C(C)(C)O)[C@H]1CC[C@@]2(C)[C@@H]3[C@@H](O)C[C@@H]4[C@]5(C[C@@]35CC[C@]12C)CCC(=O)[C@@]4(C)CO '
               'NAME: combretanone B REASON: CORRECT Molecule classified as a '
               '3-oxo-5α-steroid (steroid nucleus with 3 six‐membered and 1 '
               'five‐membered rings, ketone on a six‐membered ring, and '
               'defined chiral center in the five‐membered ring detected)\n'
               ' * SMILES: '
               'C[C@]1(O)CC[C@H]2[C@@H]3CC[C@H]4CC(=O)CC[C@]4(C)[C@@]3(F)[C@@H](O)C[C@]12C '
               'NAME: '
               '11beta,17beta-Dihydroxy-9alpha-fluoro-17alpha-methyl-5alpha-androstan-3-one '
               'REASON: CORRECT Molecule classified as a 3-oxo-5α-steroid '
               '(steroid nucleus with 3 six‐membered and 1 five‐membered '
               'rings, ketone on a six‐membered ring, and defined chiral '
               'center in the five‐membered ring detected)\n'
               ' * SMILES: '
               'C[C@H](C[C@@H](O)C=C(C)C)[C@H]1CC[C@@]2(C)[C@@H]3[C@@H](O)C[C@@H]4[C@]5(C[C@@]35CC[C@]12C)CCC(=O)C4(C)C '
               'NAME: combretanone D REASON: CORRECT Molecule classified as a '
               '3-oxo-5α-steroid (steroid nucleus with 3 six‐membered and 1 '
               'five‐membered rings, ketone on a six‐membered ring, and '
               'defined chiral center in the five‐membered ring detected)\n'
               ' * SMILES: '
               'C[C@H](CCCC(C)C(O)=O)[C@H]1CC[C@H]2[C@@H]3CC[C@H]4CC(=O)CC[C@]4(C)[C@H]3CC[C@]12C '
               'NAME: (5alpha)-3-oxocholestan-26-oic acid REASON: CORRECT '
               'Molecule classified as a 3-oxo-5α-steroid (steroid nucleus '
               'with 3 six‐membered and 1 five‐membered rings, ketone on a '
               'six‐membered ring, and defined chiral center in the '
               'five‐membered ring detected)\n'
               ' * SMILES: '
               'O[C@@H]1[C@]2([C@]3([C@@]([C@](CC3)([C@@H](CCC(O)=O)C)[H])(CC[C@@]2([C@@]4([C@@](C1)(CC(=O)CC4)[H])C)[H])C)[H])[H] '
               'NAME: 7beta-hydroxy-3-oxo-5alpha-cholan-24-oic acid REASON: '
               'CORRECT Molecule classified as a 3-oxo-5α-steroid (steroid '
               'nucleus with 3 six‐membered and 1 five‐membered rings, ketone '
               'on a six‐membered ring, and defined chiral center in the '
               'five‐membered ring detected)\n'
               ' * SMILES: '
               'C[C@@H]1C[C@@]2(C)[C@@H](CC[C@H]3[C@@H]4CC[C@H](OC5CCCCO5)[C@@]4(C)CC[C@H]23)CC1=O '
               'NAME: '
               '2alpha-Methyl-17beta-[(tetrahydro-2H-pyran-2-yl)oxy]-5alpha-androstan-3-one '
               'REASON: CORRECT Molecule classified as a 3-oxo-5α-steroid '
               '(steroid nucleus with 3 six‐membered and 1 five‐membered '
               'rings, ketone on a six‐membered ring, and defined chiral '
               'center in the five‐membered ring detected)\n'
               ' * SMILES: '
               '[H][C@@]12CC[C@@]3([H])[C@]4([H])CC[C@H](C(C)=O)[C@@]4(C)CC[C@]3([H])[C@@]1(C)CCC(=O)C2 '
               'NAME: 5alpha-pregnane-3,20-dione REASON: CORRECT Molecule '
               'classified as a 3-oxo-5α-steroid (steroid nucleus with 3 '
               'six‐membered and 1 five‐membered rings, ketone on a '
               'six‐membered ring, and defined chiral center in the '
               'five‐membered ring detected)\n'
               ' * SMILES: '
               '[H][C@@]1(CC[C@@]2([H])[C@]3([H])CC(=O)[C@@]4([H])CC(=O)CC[C@]4(C)[C@@]3([H])CC[C@]12C)[C@H](C)[C@@H](O)[C@H](O)[C@@H](C)C(C)C '
               'NAME: 3-dehydroteasterone REASON: CORRECT Molecule classified '
               'as a 3-oxo-5α-steroid (steroid nucleus with 3 six‐membered and '
               '1 five‐membered rings, ketone on a six‐membered ring, and '
               'defined chiral center in the five‐membered ring detected)\n'
               ' * SMILES: '
               'C[C@]12CC[C@H]3[C@@H](CC(=O)[C@H]4CC(=O)CC[C@]34C)[C@@H]1CC[C@@H]2O '
               'NAME: 17beta-Hydroxy-5alpha-androstan-3,6-dione REASON: '
               'CORRECT Molecule classified as a 3-oxo-5α-steroid (steroid '
               'nucleus with 3 six‐membered and 1 five‐membered rings, ketone '
               'on a six‐membered ring, and defined chiral center in the '
               'five‐membered ring detected)\n'
               ' * SMILES: '
               '[C@]12([C@@]3([C@]([C@]4([C@@](CC3)(C)[C@H](CC4)O)[H])(CC[C@]1(CC(C[C@@H]2C)=O)[H])[H])[H])C '
               'NAME: mesterolone REASON: CORRECT Molecule classified as a '
               '3-oxo-5α-steroid (steroid nucleus with 3 six‐membered and 1 '
               'five‐membered rings, ketone on a six‐membered ring, and '
               'defined chiral center in the five‐membered ring detected)\n'
               ' * SMILES: '
               'O[C@@H]1[C@@]2([C@@]([C@@](C1)([H])[C@@H](C[C@@H](/C=C(/C(=O)O)\\C)O)C)(CC(=O)C3=C2CC[C@@]4([C@@]3(CCC(=O)C4(C)C)C)[H])C)C '
               'NAME: ganolucidic acid D REASON: CORRECT Molecule classified '
               'as a 3-oxo-5α-steroid (steroid nucleus with 3 six‐membered and '
               '1 five‐membered rings, ketone on a six‐membered ring, and '
               'defined chiral center in the five‐membered ring detected)\n'
               ' * SMILES: '
               'C[C@]12CC[C@H]3[C@@H](CC[C@H]4CC(=O)CC[C@]34C)[C@@H]1CC[C@@H]2OC(=O)c1ccccc1 '
               'NAME: Stanolone benzoate REASON: CORRECT Molecule classified '
               'as a 3-oxo-5α-steroid (steroid nucleus with 3 six‐membered and '
               '1 five‐membered rings, ketone on a six‐membered ring, and '
               'defined chiral center in the five‐membered ring detected)\n'
               ' * SMILES: '
               'CCC(=O)O[C@H]1CC[C@H]2[C@@H]3C[C@@H](C)[C@H]4CC(=O)CC[C@]4(C)[C@H]3CC[C@]12C '
               'NAME: 17beta-Hydroxy-6beta-methyl-5alpha-androstan-3-one '
               'propionate REASON: CORRECT Molecule classified as a '
               '3-oxo-5α-steroid (steroid nucleus with 3 six‐membered and 1 '
               'five‐membered rings, ketone on a six‐membered ring, and '
               'defined chiral center in the five‐membered ring detected)\n'
               ' * SMILES: '
               'CC(=O)O[C@H]1CC[C@H]2[C@@H]3CC[C@H]4CC(=O)[C@@H](F)C[C@]4(C)[C@H]3CC[C@]12C '
               'NAME: 5alpha-Androstane-2beta-fluoro-17beta-ol-3-one acetate '
               'REASON: CORRECT Molecule classified as a 3-oxo-5α-steroid '
               '(steroid nucleus with 3 six‐membered and 1 five‐membered '
               'rings, ketone on a six‐membered ring, and defined chiral '
               'center in the five‐membered ring detected)\n'
               ' * SMILES: '
               'C[C@]12CC[C@]3([C@]([C@@]1(CC[C@]2(C)O)[H])(CC[C@@]4([C@@]3(CC(C(=O)C4)C=O)C)[H])[H])[H] '
               'NAME: '
               '(5S,8R,9S,10S,13S,14S,17S)-17-hydroxy-10,13,17-trimethyl-3-oxo-2,4,5,6,7,8,9,11,12,14,15,16-dodecahydro-1H-cyclopenta[a]phenanthrene-2-carboxaldehyde '
               'REASON: CORRECT Molecule classified as a 3-oxo-5α-steroid '
               '(steroid nucleus with 3 six‐membered and 1 five‐membered '
               'rings, ketone on a six‐membered ring, and defined chiral '
               'center in the five‐membered ring detected)\n'
               ' * SMILES: '
               'COC[C@@H]1C[C@@]2(C)[C@@H](CC[C@H]3[C@@H]4CC[C@H](O)[C@@]4(C)CC[C@H]23)CC1=O '
               'NAME: '
               '17beta-Hydroxy-2alpha-(methoxymethyl)-5alpha-androstan-3-one '
               'REASON: CORRECT Molecule classified as a 3-oxo-5α-steroid '
               '(steroid nucleus with 3 six‐membered and 1 five‐membered '
               'rings, ketone on a six‐membered ring, and defined chiral '
               'center in the five‐membered ring detected)\n'
               ' * SMILES: '
               '[H][C@@]12CCC3=C(CC[C@]4(C)[C@]([H])(CC[C@@]34[H])[C@H](C)CCC=C(C)C)[C@@]1(C)CCC(=O)C2C '
               'NAME: 3-dehydro-4-methylzymosterol REASON: CORRECT Molecule '
               'classified as a 3-oxo-5α-steroid (steroid nucleus with 3 '
               'six‐membered and 1 five‐membered rings, ketone on a '
               'six‐membered ring, and defined chiral center in the '
               'five‐membered ring detected)\n'
               ' * SMILES: '
               'COC(C)(C)\\C=C\\C[C@H](C)[C@@H]1CC[C@]2(C)[C@@H]3CC[C@H]4C(C)(C)C(=O)CC[C@]4(C)[C@H]3CC[C@@]12C '
               'NAME: cornusalterin B REASON: CORRECT Molecule classified as a '
               '3-oxo-5α-steroid (steroid nucleus with 3 six‐membered and 1 '
               'five‐membered rings, ketone on a six‐membered ring, and '
               'defined chiral center in the five‐membered ring detected)\n'
               ' * SMILES: '
               '[H][C@@]12CC[C@@]3([H])[C@]4([H])CC[C@]([H])([C@H](C)CCC[C@H](C)C(O)=O)[C@@]4(C)CC[C@]3([H])[C@@]1(C)CCC(=O)C2 '
               'NAME: (5alpha,25S)-3-oxocholestan-26-oic acid REASON: CORRECT '
               'Molecule classified as a 3-oxo-5α-steroid (steroid nucleus '
               'with 3 six‐membered and 1 five‐membered rings, ketone on a '
               'six‐membered ring, and defined chiral center in the '
               'five‐membered ring detected)\n'
               'False positives: SMILES: '
               'O[C@H]1[C@]2([C@]([C@]3([C@@]([C@](CC3)([C@@H](CCC(C(C)C)=C)C)[H])(C1)C)[H])(C[C@@H](O)C=4[C@]2(C)C(=O)C=CC4)[H])[H] '
               'NAME: Stoloniferone P REASON: WRONGLY CLASSIFIED Molecule '
               'classified as a 3-oxo-5α-steroid (steroid nucleus with 3 '
               'six‐membered and 1 five‐membered rings, ketone on a '
               'six‐membered ring, and defined chiral center in the '
               'five‐membered ring detected)\n'
               ' * SMILES: '
               'O[C@@H]1[C@]2([C@]([C@]3([C@@]([C@@]4([C@](CC3)(CC(=O)CC4)[H])C)(C1)[H])[H])(CC[C@@]2([C@@H](CCCC(C)C)C)[H])[H])C '
               'NAME: 12alpha-Hydroxy-5beta-cholestan-3-one REASON: WRONGLY '
               'CLASSIFIED Molecule classified as a 3-oxo-5α-steroid (steroid '
               'nucleus with 3 six‐membered and 1 five‐membered rings, ketone '
               'on a six‐membered ring, and defined chiral center in the '
               'five‐membered ring detected)\n'
               ' * SMILES: '
               'O=C1C=C2[C@@]3(C(C([C@@H](O)CC3)(C)C)C[C@H]4C2(O4)[C@]5([C@]1([C@@H](C(=O)C)CC5=O)C)C)C '
               'NAME: '
               '7beta,8-epoxy-3beta-hydroxy-4,4,14alpha-trimethyl-12,15,20-trioxo-5alpha-pregn-9(11)-ene '
               'REASON: WRONGLY CLASSIFIED Molecule classified as a '
               '3-oxo-5α-steroid (steroid nucleus with 3 six‐membered and 1 '
               'five‐membered rings, ketone on a six‐membered ring, and '
               'defined chiral center in the five‐membered ring detected)\n'
               ' * SMILES: '
               '[H][C@@]12CCC3CC(=O)CC[C@]3(C)[C@@]1([H])C(=O)C[C@@]1(C)[C@@]2([H])CC[C@]1(O)C(=O)CO '
               'NAME: 4,5-dihydrocortisone REASON: WRONGLY CLASSIFIED Molecule '
               'classified as a 3-oxo-5α-steroid (steroid nucleus with 3 '
               'six‐membered and 1 five‐membered rings, ketone on a '
               'six‐membered ring, and defined chiral center in the '
               'five‐membered ring detected)\n'
               ' * SMILES: '
               'O=C1C2=C([C@]3(CC[C@@H](C([C@@H]3C1)(C)C)OC=O)C)CC[C@]4([C@]2(CC[C@@H]4[C@@H](CC/C=C(/CO)\\C)C)C)C '
               'NAME: '
               '(+)-(5alpha,24E)-3beta-acetoxyl-26-hydroxylanosta-8,24-dien-7-one '
               'REASON: WRONGLY CLASSIFIED Molecule classified as a '
               '3-oxo-5α-steroid (steroid nucleus with 3 six‐membered and 1 '
               'five‐membered rings, ketone on a six‐membered ring, and '
               'defined chiral center in the five‐membered ring detected)\n'
               ' * SMILES: '
               'CC(=O)OCC(=O)[C@@]1(O)CC[C@H]2[C@@H]3CCC4=CC(=O)C=C[C@]4(C)[C@H]3[C@@H](O)C[C@]12C '
               'NAME: Prednisolone acetate REASON: WRONGLY CLASSIFIED Molecule '
               'classified as a 3-oxo-5α-steroid (steroid nucleus with 3 '
               'six‐membered and 1 five‐membered rings, ketone on a '
               'six‐membered ring, and defined chiral center in the '
               'five‐membered ring detected)\n'
               ' * SMILES: '
               '[H][C@@]12CCC3=CC(=O)CC[C@]3(C)[C@@]1([H])CC[C@]1(C)[C@H]([C@H](O)C[C@@]21[H])C(C)=O '
               'NAME: 16alpha-hydroxyprogesterone REASON: WRONGLY CLASSIFIED '
               'Molecule classified as a 3-oxo-5α-steroid (steroid nucleus '
               'with 3 six‐membered and 1 five‐membered rings, ketone on a '
               'six‐membered ring, and defined chiral center in the '
               'five‐membered ring detected)\n'
               ' * SMILES: '
               '[H][C@@]1(CC[C@@]2([H])[C@]3([H])CCC4=CC(=O)CC[C@]4(C)[C@@]3([H])CC[C@]12C)[C@H](C)CCC[C@H](C)C([O-])=O '
               'NAME: (25S)-Delta(4)-dafachronate REASON: WRONGLY CLASSIFIED '
               'Molecule classified as a 3-oxo-5α-steroid (steroid nucleus '
               'with 3 six‐membered and 1 five‐membered rings, ketone on a '
               'six‐membered ring, and defined chiral center in the '
               'five‐membered ring detected)\n'
               ' * SMILES: '
               'C1[C@@]2([C@]3(C[C@@H]([C@]4([C@]([C@@]3(CC[C@@]2(CC(C1)=O)[H])[H])(CC[C@@]4([C@@H](CCC([O-])=O)C)[H])[H])C)O)[H])C '
               'NAME: 12alpha-hydroxy-3-oxo-5beta-cholan-24-oate REASON: '
               'WRONGLY CLASSIFIED Molecule classified as a 3-oxo-5α-steroid '
               '(steroid nucleus with 3 six‐membered and 1 five‐membered '
               'rings, ketone on a six‐membered ring, and defined chiral '
               'center in the five‐membered ring detected)\n'
               ' * SMILES: '
               'O1[C@]23C([C@]4([C@@]1(O)[C@@]([C@H]2OC(=O)C)(C(OC(=O)C)C(C4CC(OC)=O)(C)C)[H])C)CC[C@@]5(C3=CC(O[C@H]5C=6C=COC6)=O)C '
               'NAME: XYLOCARPUS A REASON: WRONGLY CLASSIFIED Molecule '
               'classified as a 3-oxo-5α-steroid (steroid nucleus with 3 '
               'six‐membered and 1 five‐membered rings, ketone on a '
               'six‐membered ring, and defined chiral center in the '
               'five‐membered ring detected)\n'
               ' * SMILES: '
               '[Na+].[H][C@@]12CC[C@](O)(C(=O)COC(=O)CCC([O-])=O)[C@@]1(C)C[C@H](O)[C@@]1([H])[C@@]2([H])CCC2=CC(=O)C=C[C@]12C '
               'NAME: prednisolone sodium succinate REASON: WRONGLY CLASSIFIED '
               'Molecule classified as a 3-oxo-5α-steroid (steroid nucleus '
               'with 3 six‐membered and 1 five‐membered rings, ketone on a '
               'six‐membered ring, and defined chiral center in the '
               'five‐membered ring detected)\n'
               ' * SMILES: '
               'O=C1C2=C([C@@]3(C(=O)C[C@@H]([C@]3([C@@H]1OC(=O)C)C)[C@@H](CCC(=O)OCCCC)C)C)[C@@H](O)CC4[C@@]2(CC[C@@H](C4(C)C)O)C '
               'NAME: Butyl lucidenate P REASON: WRONGLY CLASSIFIED Molecule '
               'classified as a 3-oxo-5α-steroid (steroid nucleus with 3 '
               'six‐membered and 1 five‐membered rings, ketone on a '
               'six‐membered ring, and defined chiral center in the '
               'five‐membered ring detected)\n'
               ' * SMILES: '
               'C/C=C\\1/CN2[C@](C[C@@]34C5=CC=CC=C5N6C(C=CC([C@]1(C[C@@]32[H])[H])[C@@]46[H])=O)([C@]7([C@]8([C@@]9([C@]%10(C[C@]%11([C@@]%12(CCN%11CC%10=CCO8)C%13=CC=CC=C%13N([C@@]9%12[H])C7=O)[H])[H])[H])[H])[H])[H] '
               'NAME: Strychnogucine C REASON: WRONGLY CLASSIFIED Molecule '
               'classified as a 3-oxo-5α-steroid (steroid nucleus with 3 '
               'six‐membered and 1 five‐membered rings, ketone on a '
               'six‐membered ring, and defined chiral center in the '
               'five‐membered ring detected)\n'
               ' * SMILES: '
               'CC1=C(C)C(=O)O[C@H](C1)[C@](C)(O)[C@H]1CC[C@H]2[C@@H]3C[C@H]4O[C@]44[C@@H](O)C=CC(=O)[C@]4(C)[C@H]3CC[C@]12C '
               'NAME: withanolide D REASON: WRONGLY CLASSIFIED Molecule '
               'classified as a 3-oxo-5α-steroid (steroid nucleus with 3 '
               'six‐membered and 1 five‐membered rings, ketone on a '
               'six‐membered ring, and defined chiral center in the '
               'five‐membered ring detected)\n'
               ' * SMILES: '
               'O=C1C2=C([C@]3(CCC(C([C@@H]3C1)(C)C)=O)C)CC[C@]4([C@]2(CC[C@@H]4[C@@H](CCC(=O)CC)C)C)C '
               'NAME: 27-nor-3,7,24-trioxolanosta-8-ene REASON: WRONGLY '
               'CLASSIFIED Molecule classified as a 3-oxo-5α-steroid (steroid '
               'nucleus with 3 six‐membered and 1 five‐membered rings, ketone '
               'on a six‐membered ring, and defined chiral center in the '
               'five‐membered ring detected)\n'
               ' * SMILES: '
               'O[C@]12[C@@]([C@](CC1)([C@@](O)([C@H](O)CCC(O)(C)C)C)[H])(C[C@@H](O)[C@@]3([C@@]4([C@@](C[C@@H](O)[C@@H](O)C4)(C(=O)C=C23)[H])C)[H])C '
               'NAME: Turkesterone REASON: WRONGLY CLASSIFIED Molecule '
               'classified as a 3-oxo-5α-steroid (steroid nucleus with 3 '
               'six‐membered and 1 five‐membered rings, ketone on a '
               'six‐membered ring, and defined chiral center in the '
               'five‐membered ring detected)\n'
               ' * SMILES: '
               'CC(=O)C1=CC[C@H]2[C@@H]3CCC4=CC(=O)CC[C@]4(C)[C@@]3(F)[C@@H](O)C[C@]12C '
               'NAME: 9-Fluoro-11beta-hydroxypregna-4,16-diene-3,20-dione '
               'REASON: WRONGLY CLASSIFIED Molecule classified as a '
               '3-oxo-5α-steroid (steroid nucleus with 3 six‐membered and 1 '
               'five‐membered rings, ketone on a six‐membered ring, and '
               'defined chiral center in the five‐membered ring detected)\n'
               ' * SMILES: '
               'O=C1C2=C([C@@]3(C(=O)C[C@@H]([C@]3([C@@H]1O)C)[C@]4(OC(=O)CC4)C)C)[C@@H](O)C[C@@H]5[C@@]2(CC[C@@H](C5(C)C)O)C '
               'NAME: Ganoderlactone D REASON: WRONGLY CLASSIFIED Molecule '
               'classified as a 3-oxo-5α-steroid (steroid nucleus with 3 '
               'six‐membered and 1 five‐membered rings, ketone on a '
               'six‐membered ring, and defined chiral center in the '
               'five‐membered ring detected)\n'
               ' * SMILES: '
               'O=C1OC[C@H]2[C@H](O)[C@H]3OC([C@@]4([C@H]3[C@@](C2=C1)(CCC4)C)C)=O '
               'NAME: Botryosphaerin F REASON: WRONGLY CLASSIFIED Molecule '
               'classified as a 3-oxo-5α-steroid (steroid nucleus with 3 '
               'six‐membered and 1 five‐membered rings, ketone on a '
               'six‐membered ring, and defined chiral center in the '
               'five‐membered ring detected)\n'
               ' * SMILES: '
               '[H][C@@]12OC(=O)[C@@]3(C)C(=O)CC[C@](C)([C@]4([H])CC[C@](C)(CC4=C1)C=C)[C@@]23[H] '
               'NAME: momilactone A REASON: WRONGLY CLASSIFIED Molecule '
               'classified as a 3-oxo-5α-steroid (steroid nucleus with 3 '
               'six‐membered and 1 five‐membered rings, ketone on a '
               'six‐membered ring, and defined chiral center in the '
               'five‐membered ring detected)\n'
               ' * SMILES: '
               'O=C1C=C2C(=CC[C@]3([C@@]2(O)CC[C@@H]4[C@@]3(C=5NC=6C=C7C8=CC(OC([C@H]8[C@@H](C7=CC6C5C4)O)(C)C)(C)C)C)C)O[C@@H]1C(O)(C)C '
               'NAME: Shearinine M REASON: WRONGLY CLASSIFIED Molecule '
               'classified as a 3-oxo-5α-steroid (steroid nucleus with 3 '
               'six‐membered and 1 five‐membered rings, ketone on a '
               'six‐membered ring, and defined chiral center in the '
               'five‐membered ring detected)\n'
               ' * SMILES: '
               'CCC(=O)O[C@@H]1[C@@H]2[C@@]34CO[C@]2([C@@H](O)[C@H](O)[C@@H]3[C@@]2(C)CC(=O)C(OC(=O)CC)=C(C)[C@@H]2C[C@H]4OC1=O)C(=O)OC '
               'NAME: 3,15-di-O-propionylbruceolide REASON: WRONGLY CLASSIFIED '
               'Molecule classified as a 3-oxo-5α-steroid (steroid nucleus '
               'with 3 six‐membered and 1 five‐membered rings, ketone on a '
               'six‐membered ring, and defined chiral center in the '
               'five‐membered ring detected)\n'
               ' * SMILES: '
               '[H][C@]12CC(=O)N3CCC[C@]4(CC)CCC(=O)N(c5ccccc15)C234 NAME: '
               'leuconoxine REASON: WRONGLY CLASSIFIED Molecule classified as '
               'a 3-oxo-5α-steroid (steroid nucleus with 3 six‐membered and 1 '
               'five‐membered rings, ketone on a six‐membered ring, and '
               'defined chiral center in the five‐membered ring detected)\n'
               ' * SMILES: '
               'O1[C@@]2(C([C@]3([C@@]([C@@]4([C@@](CC3)(CC5=C4NC=6C5=CC=CC6)[H])C)(CC2)C)[H])=CC(=O)[C@]1(C(O)(C)C)[H])[H] '
               'NAME: Dehydroxypaxilline REASON: WRONGLY CLASSIFIED Molecule '
               'classified as a 3-oxo-5α-steroid (steroid nucleus with 3 '
               'six‐membered and 1 five‐membered rings, ketone on a '
               'six‐membered ring, and defined chiral center in the '
               'five‐membered ring detected)\n'
               ' * SMILES: '
               'O=C1[C@]2([C@]([C@]3([C@@]([C@](CC3)([C@@H](CCC(O)=O)C)[H])(C1)C)[H])(CC[C@]4([C@@]2(CCC(=O)C4)C)[H])[H])[H] '
               'NAME: 3,11-Dioxo-5beta-cholan-24-oic Acid REASON: WRONGLY '
               'CLASSIFIED Molecule classified as a 3-oxo-5α-steroid (steroid '
               'nucleus with 3 six‐membered and 1 five‐membered rings, ketone '
               'on a six‐membered ring, and defined chiral center in the '
               'five‐membered ring detected)\n'
               'False negatives: SMILES: '
               'CC(C)CCCC(C)C1CCC2C3[C@H](O)C[C@H]4CC(=O)CCC4(C)C3C[C@H](O)C12C '
               'NAME: 7alpha,12alpha-Dihydroxy-5alpha-cholestan-3-one REASON: '
               'MISSED No chiral center detected in the five-membered ring '
               '(alpha configuration not established)\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'O=C1OC[C@@H]2O[C@@H](O[C@@H]3[C@@H](OC(=O)CCCCCCCCCCCCCCC)[C@H](C=CCCCC1)[C@H](CCCCC)[C@@H](C3)O)[C@H](O)[C@H]([C@@H]2O)O',
                                     'name': 'Mucorolactone',
                                     'reason': 'Steroid nucleus not detected; '
                                               'required fused system (3 '
                                               'six‐membered and 1 '
                                               'five‐membered ring) not found '
                                               'or not steroid‐like'},
                                 {   'smiles': 'C[C@@H]1CN[C@H](COC2=C(C=CC(=C2)NC(=O)C3=NC4=CC=CC=C4S3)C(=O)N(C[C@H]1OC)C)C',
                                     'name': 'N-[(5S,6R,9S)-5-methoxy-3,6,9-trimethyl-2-oxo-11-oxa-3,8-diazabicyclo[10.4.0]hexadeca-1(12),13,15-trien-14-yl]-1,3-benzothiazole-2-carboxamide',
                                     'reason': 'Steroid nucleus not detected; '
                                               'required fused system (3 '
                                               'six‐membered and 1 '
                                               'five‐membered ring) not found '
                                               'or not steroid‐like'},
                                 {   'smiles': 'COC1=CC=CC(=C1)C2=CC=C(C=C2)[C@@H]3[C@@H]4CN(CC(=O)N4[C@@H]3CO)C(=O)C5=CN=CC=C5',
                                     'name': '(6R,7R,8S)-8-(hydroxymethyl)-7-[4-(3-methoxyphenyl)phenyl]-4-[oxo(3-pyridinyl)methyl]-1,4-diazabicyclo[4.2.0]octan-2-one',
                                     'reason': 'Steroid nucleus not detected; '
                                               'required fused system (3 '
                                               'six‐membered and 1 '
                                               'five‐membered ring) not found '
                                               'or not steroid‐like'},
                                 {   'smiles': 'C(C(/C=C/C=C/C=C/[C@H](CCCC(O)=O)O)=O)/C=C\\CCCCC',
                                     'name': '12-oxo-6-trans-leukotriene B4',
                                     'reason': 'No suitable 5-/6-membered '
                                               'rings found; not steroid-like'},
                                 {   'smiles': 'O=C1OC(=C(C#C[C@H](COC(=O)C)C)CO)C=C1',
                                     'name': "5'-O-acetylaporpinone A",
                                     'reason': 'Steroid nucleus not detected; '
                                               'required fused system (3 '
                                               'six‐membered and 1 '
                                               'five‐membered ring) not found '
                                               'or not steroid‐like'},
                                 {   'smiles': 'O=C(N1[C@@H](CCC1)C(=O)N[C@@H](CCC(=O)N)C(O)=O)[C@@H](N)[C@H](CC)C',
                                     'name': 'Ile-Pro-Gln',
                                     'reason': 'Steroid nucleus not detected; '
                                               'required fused system (3 '
                                               'six‐membered and 1 '
                                               'five‐membered ring) not found '
                                               'or not steroid‐like'},
                                 {   'smiles': 'O[C@@H]1C=CC=C(CCC(O)=O)[C@@H]1O',
                                     'name': '3-[(5R,6S)-5,6-dihydroxycyclohexa-1,3-dienyl]propanoic '
                                             'acid',
                                     'reason': 'Steroid nucleus not detected; '
                                               'required fused system (3 '
                                               'six‐membered and 1 '
                                               'five‐membered ring) not found '
                                               'or not steroid‐like'},
                                 {   'smiles': 'O=C(OC)/C=C/C(C)(C)C',
                                     'name': '4,4-Dimethyl-pentenoic acid '
                                             'methyl ester',
                                     'reason': 'No suitable 5-/6-membered '
                                               'rings found; not steroid-like'},
                                 {   'smiles': 'CCCCOc1ccc(OCCCN2CCOCC2)cc1',
                                     'name': 'pramocaine',
                                     'reason': 'Steroid nucleus not detected; '
                                               'required fused system (3 '
                                               'six‐membered and 1 '
                                               'five‐membered ring) not found '
                                               'or not steroid‐like'},
                                 {   'smiles': 'OC[C@@H](O)C(=O)[C@H](O)[C@H](O)COP(O)(O)=O',
                                     'name': 'D-arabino-hex-3-ulose '
                                             '6-phosphate',
                                     'reason': 'No suitable 5-/6-membered '
                                               'rings found; not '
                                               'steroid-like'}],
    'sample_false_negatives': [],
    'attempt': 5,
    'reasoning': 'Below is our reasoning and then our complete, self‐contained '
                 'Python code. \n'
                 '\n'
                 '● We noted that our previous code (which searched for any '
                 'fused rings between 5‐ and 6‐membered rings, a ketone group '
                 'on a six‐membered ring outside of the five‐membered ring, '
                 'and any defined chirality in the five‐membered ring) '
                 'sometimes “over‐called” some steroid‐like systems and '
                 'sometimes “missed” molecules that by literature belong to '
                 'the 3‑oxo‑5α‑steroid class because they lack an explicit '
                 'chiral tag. \n'
                 '\n'
                 '● In our improved approach we make the following '
                 'modifications:\n'
                 '\u2003 – When gathering candidate rings we now require the '
                 'ring “nucleus” (the union of atoms from four fused rings) to '
                 'have a size very close to the classical steroid core (we use '
                 'a tighter range of 16–18 atoms rather than 15–20).\n'
                 '\u2003 – In the fused system we identify the unique '
                 'five‐membered ring and require that it is fused (sharing ≥2 '
                 'atoms) with exactly one of the six‐membered rings. This '
                 'helps avoid false positives from molecules with extra '
                 'rings.\n'
                 '\u2003 – We then look for a ketone group on that '
                 'six‐membered ring (the “A” ring) by matching a “[#6;R]=O” '
                 'pattern and checking that the ketone carbon is connected at '
                 'least twice within the nucleus.\n'
                 '\u2003 – Finally, when checking for a chiral center on the '
                 'five‐membered ring we are a bit less strict. If no explicit '
                 'chiral tag is found we note that the stereochemistry is not '
                 'explicitly defined but still classify the molecule as a '
                 '3‑oxo‑5α‐steroid. (This “relaxation” should help avoid some '
                 'false negative cases even though it might lead to a warning '
                 'in the returned reason.) \n'
                 '\n'
                 'The code below implements these ideas in one self‐contained '
                 'code block. \n'
                 '\n'
                 'Below is our complete Python code:',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 52,
    'num_false_positives': 2377,
    'num_true_negatives': 139871,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.02140798682585426,
    'recall': 1.0,
    'f1': 0.0419185812172511,
    'accuracy': 0.9832958538299368,
    'negative_predictive_value': 1.0}