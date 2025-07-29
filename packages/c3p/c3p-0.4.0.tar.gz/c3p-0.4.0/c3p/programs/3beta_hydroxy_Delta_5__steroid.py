"""
Classifies: CHEBI:1722 3beta-hydroxy-Delta(5)-steroid
"""
#!/usr/bin/env python
"""
Classifies: 3β-hydroxy-Δ(5)-steroid

A compound is considered to be a 3β-hydroxy-Δ(5)-steroid if it contains:
  1. A fused steroid nucleus – heuristically defined as a single (largest) fused ring system
     composed of exactly four rings, with three six-membered rings and one five-membered ring.
  2. A hydroxyl group (–OH) attached to a carbon in the fused system that is connected on at least 
     two sides to other atoms in the fused system (approximating the 3β-OH group).
  3. At least one double bond between two carbons that are both part of the fused system (approximating 
     the Δ(5) double bond).

Note: This heuristic approach may miss some edge cases or include some false positives.
"""

from rdkit import Chem
from rdkit.Chem import AllChem

def is_3beta_hydroxy_Delta_5__steroid(smiles: str):
    """
    Determines if a molecule is a 3β-hydroxy-Δ(5)-steroid based on heuristic structural features.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if the molecule fits the desired steroid class, False otherwise.
        str: Explanation for the classification decision.
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
    
    # Get ring information (list of tuples of atom indices in each ring)
    ring_atoms = mol.GetRingInfo().AtomRings()
    if not ring_atoms:
        return False, "No rings found"
    
    # Build connectivity graph among rings: two rings are connected in a fused system if they share at least 2 atoms
    n_rings = len(ring_atoms)
    ring_graph = {i: set() for i in range(n_rings)}
    for i in range(n_rings):
        for j in range(i+1, n_rings):
            shared = set(ring_atoms[i]).intersection(ring_atoms[j])
            if len(shared) >= 2:
                ring_graph[i].add(j)
                ring_graph[j].add(i)
    
    # Find connected components of rings (each component represents a candidate fused ring system)
    visited = set()
    components = []
    for i in range(n_rings):
        if i not in visited:
            stack = [i]
            comp = set()
            while stack:
                cur = stack.pop()
                if cur not in visited:
                    visited.add(cur)
                    comp.add(cur)
                    stack.extend(ring_graph[cur] - visited)
            components.append(comp)
    
    if not components:
        return False, "No fused ring system found"
    
    # Choose the largest fused ring system (by union of atom indices)
    largest_comp_atoms = set()
    largest_comp = None
    for comp in components:
        atoms_in_comp = set()
        for rid in comp:
            atoms_in_comp.update(ring_atoms[rid])
        if len(atoms_in_comp) > len(largest_comp_atoms):
            largest_comp_atoms = atoms_in_comp
            largest_comp = comp

    # Now count how many rings (from the candidate fused system) are entirely contained in the large fused system.
    # We require exactly 4 rings in the fused system with the required size:
    comp_rings = []
    for rid in largest_comp:
        ring = ring_atoms[rid]
        # Only consider rings all of whose atoms are in the fused union; they should be.
        if set(ring).issubset(largest_comp_atoms):
            comp_rings.append(ring)

    if len(comp_rings) != 4:
        return False, ("Fused ring system does not have exactly 4 rings (found {} rings); "
                       "steroid nucleus expected to be composed of 4 fused rings".format(len(comp_rings)))
    
    # Count six-membered and five-membered rings
    six_membered = sum(1 for ring in comp_rings if len(ring)==6)
    five_membered = sum(1 for ring in comp_rings if len(ring)==5)
    if six_membered != 3 or five_membered != 1:
        return False, ("Fused ring system does not match steroid nucleus ring sizes "
                       "(expected 3 six-membered and 1 five-membered, found {} six-membered and {} five-membered)"
                       .format(six_membered, five_membered))
    
    # Look for a hydroxyl group on a carbon that is part of the fused system.
    # For each carbon in the fused system, check if it has an –OH attached.
    valid_hydroxyl_found = False
    for idx in largest_comp_atoms:
        atom = mol.GetAtomWithIdx(idx)
        if atom.GetAtomicNum() != 6:  # only consider carbons
            continue
        # Count neighbors that are in the fused ring system
        ring_neighbors = sum(1 for nbr in atom.GetNeighbors() if nbr.GetIdx() in largest_comp_atoms)
        # Look for an –OH attached to this carbon
        for nbr in atom.GetNeighbors():
            if nbr.GetAtomicNum() == 8:
                # Ensure the oxygen is in an OH group: it should have at least one attached hydrogen.
                # (Using GetTotalNumHs as a proxy.)
                if nbr.GetTotalNumHs() >= 1:
                    # We assume that if the carbon is part of the fused system and is connected to another fused atom (at least two),
                    # then an –OH here is likely the 3β-hydroxyl.
                    if ring_neighbors >= 2:
                        valid_hydroxyl_found = True
                        break
        if valid_hydroxyl_found:
            break
    if not valid_hydroxyl_found:
        return False, "No valid 3β-hydroxyl group found on a carbon of the fused steroid nucleus"
    
    # Look for a double bond (i.e. bond order = 2) inside the fused ring system.
    fused_double_bond_found = False
    for bond in mol.GetBonds():
        if bond.GetBondType() == Chem.BondType.DOUBLE:
            a1 = bond.GetBeginAtomIdx()
            a2 = bond.GetEndAtomIdx()
            if a1 in largest_comp_atoms and a2 in largest_comp_atoms:
                fused_double_bond_found = True
                break
    if not fused_double_bond_found:
        return False, "No double bond found within the fused ring system (Δ(5) double bond expected)"
    
    return True, "Molecule contains a steroid nucleus (3 six-membered and 1 five-membered fused rings), a 3β-hydroxyl group, and a Δ(5) double bond"


# Example usage (if run as a script):
if __name__ == "__main__":
    # Cholesterol is a typical 3β-hydroxy-Δ(5)-steroid.
    cholesterol_smiles = "C1[C@@]2([C@]3(CC[C@]4([C@]([C@@]3(CC=C2C[C@H](C1)O)[H])" \
                          "(CC[C@@]4([C@H](C)CCCC(C)C)[H])[H])C)[H])C"
    result, reason = is_3beta_hydroxy_Delta_5__steroid(cholesterol_smiles)
    print("Cholesterol classification:", result)
    print("Reason:", reason)


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:1722',
                          'name': '3beta-hydroxy-Delta(5)-steroid',
                          'definition': 'Any 3beta-hydroxy-steroid that '
                                        'contains a double bond between '
                                        'positions 5 and 6.',
                          'parents': ['CHEBI:36836'],
                          'xrefs': [   'KEGG:C03836',
                                       'MetaCyc:3b-hydroxy-D5-steroids'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 110,
                           'log_lines_of_code': 4.700480365792417,
                           'indent_by_line': [   1,
                                                 1,
                                                 0,
                                                 1,
                                                 2,
                                                 0,
                                                 1,
                                                 2,
                                                 2,
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
                                                 1,
                                                 2,
                                                 3,
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
                                                 5,
                                                 5,
                                                 3,
                                                 1,
                                                 1,
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 3,
                                                 2,
                                                 3,
                                                 3,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 0,
                                                 1,
                                                 2,
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 2,
                                                 1,
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
                                                 2,
                                                 3,
                                                 4,
                                                 4,
                                                 4,
                                                 5,
                                                 5,
                                                 5,
                                                 6,
                                                 6,
                                                 2,
                                                 3,
                                                 1,
                                                 2,
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
                                                 1,
                                                 2,
                                                 1,
                                                 1,
                                                 0,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1],
                           'max_indent': 6,
                           'imports': [   'from rdkit import Chem',
                                          'from rdkit.Chem import AllChem'],
                           'imports_count': 2,
                           'methods_called': [   'append',
                                                 'GetEndAtomIdx',
                                                 'GetRingInfo',
                                                 'GetAtomicNum',
                                                 'GetBondType',
                                                 'format',
                                                 'issubset',
                                                 'GetTotalNumHs',
                                                 'MolFromSmiles',
                                                 'GetIdx',
                                                 'AtomRings',
                                                 'add',
                                                 'pop',
                                                 'extend',
                                                 'GetBeginAtomIdx',
                                                 'GetBonds',
                                                 'update',
                                                 'GetNeighbors',
                                                 'GetAtomWithIdx',
                                                 'intersection'],
                           'methods_called_count': 20,
                           'smarts_strings': [],
                           'smarts_strings_count': 0,
                           'defs': [   'is_3beta_hydroxy_Delta_5__steroid(smiles: '
                                       'str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "No rings found"',
                                          'False, "No fused ring system found"',
                                          'False, ("Fused ring system does not '
                                          'have exactly 4 rings (found {} '
                                          'rings); "',
                                          'False, ("Fused ring system does not '
                                          'match steroid nucleus ring sizes "',
                                          'False, "No valid 3β-hydroxyl group '
                                          'found on a carbon of the fused '
                                          'steroid nucleus"',
                                          'False, "No double bond found within '
                                          'the fused ring system (Δ(5) double '
                                          'bond expected)"',
                                          'True, "Molecule contains a steroid '
                                          'nucleus (3 six-membered and 1 '
                                          'five-membered fused rings), a '
                                          '3β-hydroxyl group, and a Δ(5) '
                                          'double bond"'],
                           'returns_count': 8,
                           'complexity': 7.940096073158483},
    'message': '\n'
               'Attempt failed: F1 score of 0.04353999053478467 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: '
               '[H][C@@]1(CC[C@@]2([H])[C@]3([H])CC=C4C[C@@H](O)CC[C@]4(C)[C@@]3([H])CC[C@]12C)[C@H](C)[C@@H](O)C[C@@H](CC)C(C)C '
               'NAME: (22S)-hydroxysitosterol REASON: CORRECT Molecule '
               'contains a steroid nucleus with a 3β-hydroxyl group and a Δ(5) '
               'double bond\n'
               ' * SMILES: '
               '[H][C@]1([C@H](C)[C@@H](O)CCC(C)C)[C@@H](O)C[C@@]2([H])[C@]3([H])CC=C4C[C@@H](O)CC[C@]4(C)[C@@]3([H])CC[C@]12C '
               'NAME: (16S,22S)-dihydroxycholesterol REASON: CORRECT Molecule '
               'contains a steroid nucleus with a 3β-hydroxyl group and a Δ(5) '
               'double bond\n'
               ' * SMILES: '
               '[H][C@@]12CC=C3C[C@@H](O)CC[C@]3(C)[C@@]1([H])CC[C@]1(C)[C@H]([C@H](O)C[C@@]21[H])C(C)=O '
               'NAME: 16alpha-hydroxypregnenolone REASON: CORRECT Molecule '
               'contains a steroid nucleus with a 3β-hydroxyl group and a Δ(5) '
               'double bond\n'
               ' * SMILES: '
               '[H][C@@]1(CC[C@@]2([H])C3=CC=C4C[C@@H](O)CC[C@]4(C)[C@@]3([H])CC[C@]12C)[C@H](C)CCCC(C)C '
               'NAME: cholesta-5,7-dien-3beta-ol REASON: CORRECT Molecule '
               'contains a steroid nucleus with a 3β-hydroxyl group and a Δ(5) '
               'double bond\n'
               ' * SMILES: '
               '[H][C@@]12CC=C3C[C@@H](O)CC[C@]3(C)[C@@]1([H])CC[C@@]1(C)[C@@]2([H])CC[C@]1([H])[C@@](C)(O)\\C=C\\[C@@H](CC)C(C)C '
               'NAME: leucisterol REASON: CORRECT Molecule contains a steroid '
               'nucleus with a 3β-hydroxyl group and a Δ(5) double bond\n'
               ' * SMILES: '
               'CC[C@H](CC[C@@H](C)[C@H]1CC[C@H]2[C@@H]3[C@H](O)C=C4C[C@@H](O)CC[C@]4(C)[C@H]3CC[C@]12C)C(C)C '
               'NAME: stigmast-5-ene-3beta,7alpha-diol REASON: CORRECT '
               'Molecule contains a steroid nucleus with a 3β-hydroxyl group '
               'and a Δ(5) double bond\n'
               ' * SMILES: '
               'O[C@@H]1CC=2[C@@]([C@@]3([C@]([C@]4([C@@]([C@](CC4)([C@H](C)/C=C/[C@H](CC)C)[H])(CC3)C)[H])(CC2)[H])[H])(CC1)C '
               'NAME: 27-nor-(24S)-methylcholest-5,22E-dien-3beta-ol REASON: '
               'CORRECT Molecule contains a steroid nucleus with a 3β-hydroxyl '
               'group and a Δ(5) double bond\n'
               ' * SMILES: '
               'C1[C@@]2([C@]3(CC[C@]4([C@]([C@@]3(CC=C2C[C@H](C1)O)[H])(CC[C@@]4([C@H](C)CCCC(C)C)[H])[H])C)[H])C '
               'NAME: cholesterol REASON: CORRECT Molecule contains a steroid '
               'nucleus with a 3β-hydroxyl group and a Δ(5) double bond\n'
               ' * SMILES: '
               'C1[C@@]2([C@]3(CC[C@]4(C)[C@@H](C(C)=O)CC[C@]4([C@@]3([C@@H](C=C2C[C@H](C1)O)O)[H])[H])[H])C '
               'NAME: 7alpha-hydroxypregnenolone REASON: CORRECT Molecule '
               'contains a steroid nucleus with a 3β-hydroxyl group and a Δ(5) '
               'double bond\n'
               ' * SMILES: '
               '[C@@]12([C@]3([C@](CC[C@@]1([C@@]4(C(C[C@H](CC4)O)=CC2)C)[H])([C@](CC3)([C@H](C)CC[C@@H](C(C)C)OS(O)(=O)=O)[H])C)[H])[H] '
               'NAME: (24S)-hydroxycholesterol 24-sulfate REASON: CORRECT '
               'Molecule contains a steroid nucleus with a 3β-hydroxyl group '
               'and a Δ(5) double bond\n'
               ' * SMILES: '
               '[H][C@@]1(CC[C@@]2([H])[C@]3([H])[C@H](O)C=C4C[C@@H](O)CC[C@]4(C)[C@@]3([H])CC[C@]12C)[C@H](C)CC[C@H](O)C(C)C '
               'NAME: (24S)-7alpha,24-dihydroxycholesterol REASON: CORRECT '
               'Molecule contains a steroid nucleus with a 3β-hydroxyl group '
               'and a Δ(5) double bond\n'
               ' * SMILES: '
               'CC(C)[C@@H](O)CC[C@@H](C)[C@H]1CC[C@H]2[C@@H]3CC=C4[C@@H](O)[C@@H](O)CC[C@]4(C)[C@H]3CC[C@]12C '
               'NAME: 4beta,24S-dihydroxycholesterol REASON: CORRECT Molecule '
               'contains a steroid nucleus with a 3β-hydroxyl group and a Δ(5) '
               'double bond\n'
               ' * SMILES: '
               'CC(CO)[C@@H](O)CC[C@@H](C)[C@H]1CC[C@H]2[C@@H]3CC=C4C[C@@H](O)CC[C@]4(C)[C@H]3CC[C@]12C '
               'NAME: (24S,26)-dihydroxycholesterol REASON: CORRECT Molecule '
               'contains a steroid nucleus with a 3β-hydroxyl group and a Δ(5) '
               'double bond\n'
               ' * SMILES: '
               '[H][C@@]12CC=C3C[C@@H](O)CC[C@]3(C)[C@@]1([H])CC[C@]1(C)C(=CC[C@@]21[H])c1cccnc1 '
               'NAME: abiraterone REASON: CORRECT Molecule contains a steroid '
               'nucleus with a 3β-hydroxyl group and a Δ(5) double bond\n'
               ' * SMILES: '
               'CC(C)CCC[C@@H](C)[C@H]1CC[C@H]2[C@@H]3[C@H](O)C=C4[C@@H](O)[C@@H](O)CC[C@]4(C)[C@H]3CC[C@]12C '
               'NAME: 4beta,7alpha-dihydroxycholesterol REASON: CORRECT '
               'Molecule contains a steroid nucleus with a 3β-hydroxyl group '
               'and a Δ(5) double bond\n'
               ' * SMILES: '
               'C1[C@]2([C@@]3(CC[C@]4([C@](C3=CC=C2C[C@H](C1)O)(CC[C@@]4([C@@H](CCCC(C)C)C)[H])[H])C)[H])C '
               'NAME: lumisterol 3 REASON: CORRECT Molecule contains a steroid '
               'nucleus with a 3β-hydroxyl group and a Δ(5) double bond\n'
               ' * SMILES: '
               '[H][C@@]1(CC[C@@]2([H])[C@]3([H])CC=C4C[C@@H](O)CC[C@]4(C)[C@@]3([H])CC[C@]12C)[C@H](C)CCC=C(C)C '
               'NAME: desmosterol REASON: CORRECT Molecule contains a steroid '
               'nucleus with a 3β-hydroxyl group and a Δ(5) double bond\n'
               ' * SMILES: '
               'C[C@H](CCC[C@@H](C)C(O)=O)[C@H]1CC[C@H]2[C@@H]3CC=C4C[C@@H](O)CC[C@]4(C)[C@H]3CC[C@]12C '
               'NAME: (25R)-3beta-hydroxycholest-5-en-26-oic acid REASON: '
               'CORRECT Molecule contains a steroid nucleus with a 3β-hydroxyl '
               'group and a Δ(5) double bond\n'
               ' * SMILES: '
               'O[C@@H]1CC=2[C@@]([C@@]3([C@]([C@]4([C@@]([C@](CC4)([C@@H](CCC(C)C)C)[H])(CC3)C)[H])(CC2)[H])[H])(CC1)C '
               'NAME: 24-Norcholesterol REASON: CORRECT Molecule contains a '
               'steroid nucleus with a 3β-hydroxyl group and a Δ(5) double '
               'bond\n'
               ' * SMILES: '
               '[H][C@@]1(CC[C@@]2([H])C3=CC=C4C[C@@H](O)CC[C@]4(C)[C@@]3([H])CC[C@]12C)[C@H](C)\\C=C\\[C@H](C)C(C)C '
               'NAME: ergosterol REASON: CORRECT Molecule contains a steroid '
               'nucleus with a 3β-hydroxyl group and a Δ(5) double bond\n'
               ' * SMILES: '
               '[H][C@@]1(CC[C@@]2([H])[C@]3([H])CC=C4C[C@@H](O)CC[C@]4(C)[C@@]3([H])CC[C@]12C)[C@H](C)CC[C@@H](C)C(C)C '
               'NAME: campesterol REASON: CORRECT Molecule contains a steroid '
               'nucleus with a 3β-hydroxyl group and a Δ(5) double bond\n'
               ' * SMILES: '
               '[H][C@]12C[C@@H](OC(=O)c3ccccc3)[C@]3(C)[C@@](O)(CC[C@]3(O)[C@]1([H])CC=C1C[C@@H](O)CC[C@]21C)C(C)=O '
               'NAME: calotropone REASON: CORRECT Molecule contains a steroid '
               'nucleus with a 3β-hydroxyl group and a Δ(5) double bond\n'
               ' * SMILES: '
               'C[C@H](CCC[C@@H](C)C(O)=O)[C@H]1CC[C@H]2[C@@H]3CC=C4[C@@H](O)[C@@H](O)CC[C@]4(C)[C@H]3CC[C@]12C '
               'NAME: (25R)-3beta,4beta-dihydroxycholest-5-en-26-oic acid '
               'REASON: CORRECT Molecule contains a steroid nucleus with a '
               '3β-hydroxyl group and a Δ(5) double bond\n'
               ' * SMILES: '
               '[H][C@]12C[C@@]3([H])[C@]4([H])CC=C5C[C@@H](O)CC[C@]5(C)[C@@]4([H])CC[C@]3(C)[C@@]1(O)[C@H](C)[C@@]1(CC[C@@H](C)CO1)O2 '
               'NAME: pennogenin REASON: CORRECT Molecule contains a steroid '
               'nucleus with a 3β-hydroxyl group and a Δ(5) double bond\n'
               ' * SMILES: '
               'CC(C)CC[C@@H](O)[C@@H](C)[C@H]1CC[C@H]2[C@@H]3[C@H](O)C=C4C[C@@H](O)CC[C@]4(C)[C@H]3CC[C@]12C '
               'NAME: (7alpha,22R)-dihydroxycholesterol REASON: CORRECT '
               'Molecule contains a steroid nucleus with a 3β-hydroxyl group '
               'and a Δ(5) double bond\n'
               'False positives: SMILES: '
               'O1C23C(CCC4(C5(C(C6(C(CC5)C(C(O)CC6)(C)C)C)C(=O)C=C42)C)C)(CCC(C3)(C1=O)C)C '
               'NAME: Isoglabrolide REASON: WRONGLY CLASSIFIED Molecule '
               'contains a steroid nucleus with a 3β-hydroxyl group and a Δ(5) '
               'double bond\n'
               ' * SMILES: '
               '[H][C@]12C\\C=C\\C\\C(C)=C\\[C@@]3(C)C=C([C@@H](CC)C[C@]33OC(=O)C(C(=O)[C@@]1(CC)[C@]1([H])CC[C@H](C)[C@]([H])(O[C@H]4C[C@H](O)[C@H](NC(=O)c5[nH]c(Cl)cc5Cl)[C@@H](C)O4)[C@@]1([H])C=C2)=C3O)C(O)=O '
               'NAME: decatromicin B REASON: WRONGLY CLASSIFIED Molecule '
               'contains a steroid nucleus with a 3β-hydroxyl group and a Δ(5) '
               'double bond\n'
               ' * SMILES: '
               'C1(CC(C([C@]2([C@]1([C@@]3([C@@]([C@@H](C2)O)(C=4[C@@](CC3)([C@@](CC4)([C@@H]5C[C@@H](O[C@H]5OC(C)=O)[C@H]6C(C)(C)O6)[H])C)C)[H])C)[H])(C)C)=O)OC(C)=O '
               'NAME: (21S)-1,21-diacetoxy-apo-melianone REASON: WRONGLY '
               'CLASSIFIED Molecule contains a steroid nucleus with a '
               '3β-hydroxyl group and a Δ(5) double bond\n'
               ' * SMILES: '
               'O[C@@H]1C=2[C@]3([C@@]([C@](CC3=O)([C@@H](CC(=O)C[C@@H](C)C(O)=O)C)[H])(CC(=O)C2[C@@]4([C@](C([C@@H](O)CC4)(C)C)(C1)[H])C)C)C '
               'NAME: Ganoderic acid B REASON: WRONGLY CLASSIFIED Molecule '
               'contains a steroid nucleus with a 3β-hydroxyl group and a Δ(5) '
               'double bond\n'
               ' * SMILES: '
               'O=C1OCC(C1C)(O)C(=O)C[C@H]([C@@H]2[C@@]3([C@@](C4=C([C@@]5([C@H](C([C@H](OC(=O)CC(=O)OC)CC5)(C)C)CC4)C)CC3)(C)CC2)C)C '
               'NAME: Hexatenuin C REASON: WRONGLY CLASSIFIED Molecule '
               'contains a steroid nucleus with a 3β-hydroxyl group and a Δ(5) '
               'double bond\n'
               ' * SMILES: '
               'O=C1C2=C(C(=O)C[C@@H]3[C@@]2(CC[C@@H](C3(C)C)O)C)[C@@]4(C(=O)CC([C@]4(C1)C)=C(CC(=O)CC(C(=O)O)C)C)C '
               'NAME: 3beta-hydroxyganodernoid D REASON: WRONGLY CLASSIFIED '
               'Molecule contains a steroid nucleus with a 3β-hydroxyl group '
               'and a Δ(5) double bond\n'
               ' * SMILES: '
               'O=C1O[C@@H]2C[C@]3(O[C@@H](C2)CC=C(C[C@H](C=CC=C4[C@]5([C@H]1C=C([C@@H](O)[C@H]5OC4)COC(=O)CC)O)C)C)O[C@@H]([C@@H](C)CC3)C '
               'NAME: Milbemycin alpha22 REASON: WRONGLY CLASSIFIED Molecule '
               'contains a steroid nucleus with a 3β-hydroxyl group and a Δ(5) '
               'double bond\n'
               ' * SMILES: '
               'O=C1N2[C@@H](C(=O)N[C@@]13O[C@@]4(NC=5C=C6OC(C)(C)C=CC6=CC5[C@@]4(C3)O)C(C=C)(C)C)CCC2 '
               'NAME: Asperversiamide I REASON: WRONGLY CLASSIFIED Molecule '
               'contains a steroid nucleus with a 3β-hydroxyl group and a Δ(5) '
               'double bond\n'
               ' * SMILES: '
               'OC1C(C2C(C3C(C4(C(C(=C3)C)(C(O)=C(C4=O)C)C)C(OC)=O)(CC2)C)(CC1)CO)(C)C '
               'NAME: MCULE-1046953863 REASON: WRONGLY CLASSIFIED Molecule '
               'contains a steroid nucleus with a 3β-hydroxyl group and a Δ(5) '
               'double bond\n'
               ' * SMILES: '
               'O=C1C=C2[C@@](CC[C@@H](C2)O)(C)[C@@H]3[C@@H]1[C@H]4[C@]([C@@H]([C@@H](/C=C/[C@@H](C(C)C)C)C)CC4)(C)CC3 '
               'NAME: (22E)-3b-Hydroxy-ergosta-5,22-dien-7-one REASON: WRONGLY '
               'CLASSIFIED Molecule contains a steroid nucleus with a '
               '3β-hydroxyl group and a Δ(5) double bond\n'
               ' * SMILES: '
               'CCC\\C=C\\C=C\\C=C\\C(=O)O[C@@H]1[C@@H](C)[C@@]23OC4(O[C@H]([C@@H]2[C@@H]2O[C@]2(CO)[C@@H](O)[C@@]2(O)[C@H]3C=C(C)C2=O)[C@]1(O4)C(C)=C)c1ccccc1 '
               'NAME: Gniditrin REASON: WRONGLY CLASSIFIED Molecule contains a '
               'steroid nucleus with a 3β-hydroxyl group and a Δ(5) double '
               'bond\n'
               ' * SMILES: '
               'O=C(OC[C@]1(O)[C@@H]2[C@@H](O)C3=CC[C@@H]4[C@@]([C@]3(C2)CC1)(CC[C@H]([C@]4(CO)C)O)C)C '
               'NAME: Aphidicolin A44 REASON: WRONGLY CLASSIFIED Molecule '
               'contains a steroid nucleus with a 3β-hydroxyl group and a Δ(5) '
               'double bond\n'
               ' * SMILES: '
               '[H][C@]12CC[C@@]3(C)[C@@]([H])(C[C@H](O)[C@]3([H])[C@@](C)(O)CC[C@@H](CC)C(C)C)[C@]1([H])[C@H](O)C=C1C[C@@H](O)CC[C@]21C '
               'NAME: (20S)-5-Stigmastene-3beta,7alpha,16beta,20-tetrol '
               'REASON: WRONGLY CLASSIFIED Molecule contains a steroid nucleus '
               'with a 3β-hydroxyl group and a Δ(5) double bond\n'
               ' * SMILES: '
               'O1[C@@]2([C@@]([C@@]3([C@]([C@]4([C@](CC3)([C@@]5(C(=CC4)C[C@@H](O)[C@H](O)C5)C)[H])[H])(C2)[H])C)([C@@H]([C@]16OC[C@@H](C(O)C6)C)C)[H])[H] '
               'NAME: Karatavegenin C REASON: WRONGLY CLASSIFIED Molecule '
               'contains a steroid nucleus with a 3β-hydroxyl group and a Δ(5) '
               'double bond\n'
               ' * SMILES: '
               '[H][C@@]12C[C@H](O)CC[C@]1(C)[C@@]1([H])C[C@H](O)[C@]3(C)[C@]([H])(CC[C@@]3([H])[C@]1([H])C=C2)[C@H](C)CCC(O)=O '
               'NAME: 3alpha,12alpha-dihydroxy-5beta-chol-6-en-24-oic acid '
               'REASON: WRONGLY CLASSIFIED Molecule contains a steroid nucleus '
               'with a 3β-hydroxyl group and a Δ(5) double bond\n'
               ' * SMILES: '
               'O=C(O)/C(=C\\CC[C@H]([C@@H]1[C@@]2([C@@](C=3C([C@@]4([C@H](C([C@H](O)CC4)(C)C)CC3)C)=C[C@H]2O[C@@H]5O[C@@H]([C@@H](O)[C@@H]([C@H]5O)O)CO)(C)CC1)C)C)/C '
               'NAME: Oligoporin B REASON: WRONGLY CLASSIFIED Molecule '
               'contains a steroid nucleus with a 3β-hydroxyl group and a Δ(5) '
               'double bond\n'
               ' * SMILES: '
               'C1CC(C2[C@](C1)(C3[C@@](CC2)(C4[C@]([C@H](C3)O)([C@@H]5C(=CC4)CO[C@H]5O)C)C)C)(C)C '
               'NAME: (+)-Desoxyscalarin REASON: WRONGLY CLASSIFIED Molecule '
               'contains a steroid nucleus with a 3β-hydroxyl group and a Δ(5) '
               'double bond\n'
               ' * SMILES: '
               '[C@@]12([C@](CC[C@@H]([C@]13OC=4[C@](C3)(C(=C(C(C4C)=O)C(=O)[O-])C)C)C)([H])C([C@H](CC2)O)(C)C)C '
               'NAME: asnovolin H(1-) REASON: WRONGLY CLASSIFIED Molecule '
               'contains a steroid nucleus with a 3β-hydroxyl group and a Δ(5) '
               'double bond\n'
               ' * SMILES: '
               'C[C@@]12C[C@H](O)[C@@H]3[C@@]4(C)C=CC(=O)OC(C)(C)[C@@H]4CC(=O)[C@@]3(C)[C@]11O[C@@H]1C(=O)O[C@H]2c1ccoc1 '
               'NAME: Zapoterin REASON: WRONGLY CLASSIFIED Molecule contains a '
               'steroid nucleus with a 3β-hydroxyl group and a Δ(5) double '
               'bond\n'
               ' * SMILES: '
               '[H][C@@]12CC[C@](O)(C(=O)CO)[C@@]1(C)CC(=O)[C@@]1([H])[C@@]2([H])C=CC2=CC(=O)C=C[C@]12C '
               'NAME: Delta(6)-prednisone REASON: WRONGLY CLASSIFIED Molecule '
               'contains a steroid nucleus with a 3β-hydroxyl group and a Δ(5) '
               'double bond\n'
               ' * SMILES: '
               'O=C1C(=C2O[C@H]3[C@H](O)[C@@H]4C([C@@H](OC(=O)C)CC[C@]4([C@@H]5C=C([C@@]1([C@]2(C(=O)OC)[C@@]35C)C)C)C=O)(C)C)C '
               'NAME: Andrastone C REASON: WRONGLY CLASSIFIED Molecule '
               'contains a steroid nucleus with a 3β-hydroxyl group and a Δ(5) '
               'double bond\n'
               ' * SMILES: '
               'O=C1[C@@]2(C(C(=O)C)=CC[C@H]2C3=CCC=4[C@@]([C@H]3C1)([C@@H](O)[C@H](O)[C@H](C4)O)C)C '
               'NAME: Terresterone B REASON: WRONGLY CLASSIFIED Molecule '
               'contains a steroid nucleus with a 3β-hydroxyl group and a Δ(5) '
               'double bond\n'
               ' * SMILES: '
               'O=C1[C@@]23C(=O)N[C@@](C2)(OC)CC4=CC=C(O[C@H]5[C@@H]6[C@@H]1[C@@](C=C(C)[C@H]6[C@@]7(C[C@H](C)C[C@@H]([C@@H]57)C)C)(C)[C@@H](C3)O)C=C4 '
               'NAME: Pyrrospirone C REASON: WRONGLY CLASSIFIED Molecule '
               'contains a steroid nucleus with a 3β-hydroxyl group and a Δ(5) '
               'double bond\n'
               ' * SMILES: '
               'C1[C@H](O)C(C)(C)[C@]2([C@@](C1)(C)[C@]3(CC[C@@]4([C@](C3=CC2)(C)CC[C@]5([C@]4(CC[C@@H]5C(C)C)[H])C)C)[H])[H] '
               'NAME: motiol REASON: WRONGLY CLASSIFIED Molecule contains a '
               'steroid nucleus with a 3β-hydroxyl group and a Δ(5) double '
               'bond\n'
               ' * SMILES: '
               'ClC1=C(C(=C(O)C=C1)C(=O)O[C@H]2[C@H](O)[C@@H](O)[C@H](O[C@@H]3[C@@H](O)[C@@H](O[C@@H]([C@H]3O)C)O[C@@H]4[C@H]5C=CC6[C@@H](C=CC[C@@]7(C=C(C)[C@@H](C[C@]87C(=C(OC([C@]6([C@@H]5[C@@H](C)C[C@H]4C)C)=O)C(=O)O8)O)C[C@H](O)[C@@](O)(C(=O)C)C)C)C)O[C@@H]2C)C '
               'NAME: Phocoenamicin C REASON: WRONGLY CLASSIFIED Molecule '
               'contains a steroid nucleus with a 3β-hydroxyl group and a Δ(5) '
               'double bond\n'
               'False negatives: NONE\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'C1=CC=C2C(=C1)C(=O)C3=CC=CC=C3C2(CC4=CC(=NC=C4)F)CC5=CC(=NC=C5)F',
                                     'name': '10,10-bis[(2-fluoro-4-pyridinyl)methyl]-9-anthracenone',
                                     'reason': 'Fused ring system does not '
                                               'have exactly 4 rings (found 3 '
                                               'rings); steroid nucleus '
                                               'expected to be composed of 4 '
                                               'fused rings'},
                                 {   'smiles': 'C[C@@H](C1=CC=CC=C1)NC(=O)[C@@H]2[C@H]([C@@H]3CN4C(=CC=C(C4=O)C5=CC=CC=C5F)[C@H]2N3C)CO',
                                     'name': 'LSM-10936',
                                     'reason': 'Fused ring system does not '
                                               'have exactly 4 rings (found 3 '
                                               'rings); steroid nucleus '
                                               'expected to be composed of 4 '
                                               'fused rings'},
                                 {   'smiles': '[H]C(=CC(=O)C(O)=O)C(CC(O)=O)C(O)=O',
                                     'name': '5-oxopent-3-ene-1,2,5-tricarboxylic '
                                             'acid',
                                     'reason': 'No rings found'},
                                 {   'smiles': 'S1N(C2=CC=C(C=C2)C(OCC)=O)C(=O)C=C1',
                                     'name': 'ethyl '
                                             '4-(3-oxo-2,3-dihydroisothiazol-2-yl)benzoate',
                                     'reason': 'Fused ring system does not '
                                               'have exactly 4 rings (found 1 '
                                               'rings); steroid nucleus '
                                               'expected to be composed of 4 '
                                               'fused rings'},
                                 {   'smiles': 'COc1cc(O)c2c(c1)oc1c(O)cccc1c2=O',
                                     'name': 'mesuaxanthone A',
                                     'reason': 'Fused ring system does not '
                                               'have exactly 4 rings (found 3 '
                                               'rings); steroid nucleus '
                                               'expected to be composed of 4 '
                                               'fused rings'},
                                 {   'smiles': 'O([C@@H]1[C@H](O)[C@@H](O[C@@H]([C@H]1O)CO[C@H]2O[C@@H]([C@@H](O)[C@H](O)[C@@H]2O[C@@H]3O[C@@H]([C@@H](O)[C@H](O)[C@H]3NC(=O)C)CO)CO[C@@H]4O[C@@H]([C@@H](O)[C@H](O)[C@H]4NC(=O)C)CO)O[C@H]5[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]5CO)O[C@H]6[C@H](O)[C@@H](NC(=O)C)C(O[C@@H]6CO)O)[C@H]7O[C@@H]([C@@H](O[C@@H]8O[C@@H]([C@@H](O)[C@H](O)[C@H]8NC(=O)C)CO)[C@H](O)[C@@H]7O[C@@H]9O[C@@H]([C@@H](O[C@@H]%10O[C@@H]([C@H](O)[C@H](O)[C@H]%10O)CO)[C@H](O)[C@H]9NC(=O)C)CO)CO',
                                     'name': 'N-[(3R,4R,5S,6R)-5-[(2S,3R,4R,5S,6R)-3-Acetamido-5-[(2S,3S,4S,5R,6R)-6-[[(2S,3S,4S,5S,6R)-3-[(2R,3R,4R,5S,6R)-3-acetamido-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-6-[[(2R,3R,4R,5S,6R)-3-acetamido-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxymethyl]-4,5-dihydroxyoxan-2-yl]oxymethyl]-4-[(2R,3S,4S,5S,6R)-5-[(2R,3R,4R,5S,6R)-3-acetamido-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-3-[(2S,3R,4R,5S,6R)-3-acetamido-4-hydroxy-6-(hydroxymethyl)-5-[(2S,3R,4S,5R,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-3,5-dihydroxyoxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-2,4-dihydroxy-6-(hydroxymethyl)oxan-3-yl]acetamide',
                                     'reason': 'Fused ring system does not '
                                               'have exactly 4 rings (found 1 '
                                               'rings); steroid nucleus '
                                               'expected to be composed of 4 '
                                               'fused rings'},
                                 {   'smiles': 'CCCCCCCC\\C=C/CCCCCCCC(=O)OC[C@H](COP([O-])(=O)OC[C@H]([NH3+])C([O-])=O)OC(=O)CCC\\C=C/C\\C=C/C\\C=C/C\\C=C/CCCCC',
                                     'name': '1-oleoyl-2-arachidonoyl-sn-glycero-3-phospho-L-serine(1-)',
                                     'reason': 'No rings found'},
                                 {   'smiles': 'OC(=Cc1ccccc1)C([O-])=O',
                                     'name': 'enol-phenylpyruvate',
                                     'reason': 'Fused ring system does not '
                                               'have exactly 4 rings (found 1 '
                                               'rings); steroid nucleus '
                                               'expected to be composed of 4 '
                                               'fused rings'},
                                 {   'smiles': '[H][C@]1(CC[C@]2(C)[C@@H](O)CCC(=C)[C@@]12[H])[C@@H](O)C(C)C',
                                     'name': '(1R,3aS,4S,7aR)-1-((S)-1-hydroxy-2-methylpropyl)-3a-methyl-7-methyleneoctahydro-1H-inden-4-ol',
                                     'reason': 'Fused ring system does not '
                                               'have exactly 4 rings (found 2 '
                                               'rings); steroid nucleus '
                                               'expected to be composed of 4 '
                                               'fused rings'},
                                 {   'smiles': 'O1C(C(O)C(O)C(O)C1CO)C=2C(=O)C=3C(O)=C(C4OC(C(O)C(O)C4O)CO)C(O)=CC3OC2C5=CC=C(OC)C=C5',
                                     'name': "3,6-Diglucopyranosyl-5,7-dihydroxy-4'-methoxyflavone",
                                     'reason': 'Fused ring system does not '
                                               'have exactly 4 rings (found 2 '
                                               'rings); steroid nucleus '
                                               'expected to be composed of 4 '
                                               'fused rings'}],
    'sample_false_negatives': [   {   'smiles': '[H][C@]12C[C@@]3([H])[C@]4([H])CC=C5C[C@@H](O)CC[C@]5(C)[C@@]4([H])CC[C@]3(C)[C@@]1(O)[C@H](C)[C@@]1(CC[C@@H](C)CO1)O2',
                                      'name': 'pennogenin',
                                      'reason': 'Fused ring system does not '
                                                'have exactly 4 rings (found 5 '
                                                'rings); steroid nucleus '
                                                'expected to be composed of 4 '
                                                'fused rings'},
                                  {   'smiles': '[H][C@]12CC[C@H](C)CN1[C@@]1([H])C[C@@]3([H])[C@]4([H])CC=C5C[C@@H](O)CC[C@]5(C)[C@@]4([H])CC[C@]3(C)[C@@]1([H])[C@@H]2C',
                                      'name': 'solanidine',
                                      'reason': 'Fused ring system does not '
                                                'have exactly 4 rings (found 6 '
                                                'rings); steroid nucleus '
                                                'expected to be composed of 4 '
                                                'fused rings'},
                                  {   'smiles': 'C1[C@]2([C@]3(C[C@H](C1)O)[C@H]([C@H](C4=C2CC[C@]5([C@@]4(C(C[C@@H]5[C@@H](/C=C/[C@@H](C(C)C)C)C)=O)O)C)O)O3)C',
                                      'name': '(22E,24R)-5alpha,6alpha-epoxy3beta,7alpha,14beta-trihydroxy-ergosta-8,22,dien-15-one',
                                      'reason': 'Fused ring system does not '
                                                'have exactly 4 rings (found 5 '
                                                'rings); steroid nucleus '
                                                'expected to be composed of 4 '
                                                'fused rings'},
                                  {   'smiles': 'C1[C@@]2([C@]3(CC[C@]4(C)[C@@]5(C(C)=O)[C@@H](C[C@]4([C@@]3(CC=C2C[C@H](C1)O)[H])[H])O5)[H])C',
                                      'name': '3beta-hydroxy-16alpha,17alpha-epoxypregnenolone',
                                      'reason': 'Fused ring system does not '
                                                'have exactly 4 rings (found 5 '
                                                'rings); steroid nucleus '
                                                'expected to be composed of 4 '
                                                'fused rings'},
                                  {   'smiles': '[H][C@]12C[C@@]3([H])[C@]4([H])CC=C5C[C@@H](O)CC[C@]5(C)[C@@]4([H])CC[C@]3(C)[C@@]1([H])[C@H](C)[C@@](O)(CCC(C)C)O2',
                                      'name': '(22R)-furost-5-en-3beta,22-diol',
                                      'reason': 'Fused ring system does not '
                                                'have exactly 4 rings (found 5 '
                                                'rings); steroid nucleus '
                                                'expected to be composed of 4 '
                                                'fused rings'},
                                  {   'smiles': '[H][C@]12C[C@@]3([H])[C@]4([H])CC=C5C[C@@H](O)CC[C@]5(C)[C@@]4([H])CC[C@]3(C)[C@@]1([H])[C@H](C)[C@@]1(CC[C@@](C)(CO)O1)O2',
                                      'name': 'nuatigenin',
                                      'reason': 'Fused ring system does not '
                                                'have exactly 4 rings (found 5 '
                                                'rings); steroid nucleus '
                                                'expected to be composed of 4 '
                                                'fused rings'}],
    'attempt': 1,
    'reasoning': 'Below is one possible solution. I changed our approach from '
                 'simply counting rings by “size” to trying to identify a '
                 'fused ring‐system that resembles the steroid nucleus. In '
                 'brief, the function first gathers all rings from the '
                 'molecule and then groups together those rings that share two '
                 'or more atoms (a common definition of a fused system). Then '
                 'it checks whether the largest fused system comprises exactly '
                 'four rings—and among those, three are six‐membered and one '
                 'is five‐membered. Next it requires that one of the carbons '
                 'in that fused system bears an –OH group and that that carbon '
                 'is “deeply embedded” (i.e. bonded to at least two other '
                 'atoms from the steroid nucleus). Finally it looks for at '
                 'least one double bond within the fused system (our '
                 'approximation for the Δ(5) double bond). (Of course, these '
                 'heuristics are not perfect; they attempt to capture the key '
                 'features while reducing the false positives seen before.) \n'
                 '\n'
                 'Below is the complete Python code:',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 86,
    'num_false_positives': 2018,
    'num_true_negatives': 140190,
    'num_false_negatives': 6,
    'num_negatives': None,
    'precision': 0.0408745247148289,
    'recall': 0.9347826086956522,
    'f1': 0.07832422586520947,
    'accuracy': 0.985776528460998,
    'negative_predictive_value': 0.9999572027732603}