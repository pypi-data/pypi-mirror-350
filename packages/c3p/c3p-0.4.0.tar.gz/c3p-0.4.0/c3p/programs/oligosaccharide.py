"""
Classifies: CHEBI:50699 oligosaccharide
"""
"""
Classifies: Oligosaccharide
Definition: A compound in which monosaccharide units are joined by glycosidic linkages.
Heuristic improvements in this version:
  1. Candidate sugar rings are identified as either 5‐membered (furanose) or 6‐membered (pyranose) rings
     that contain exactly one ring oxygen (with allowance for one nitrogen substituting a carbon) and must be
     fully saturated (all bonds inside the ring are single). Additionally, at least two ring carbons are required
     to have exocyclic hydroxyl groups (i.e. an oxygen neighbor that carries at least one hydrogen).
  2. At least two such sugar rings must be found and they must be connected by a glycosidic linkage.
     Two rings are declared “connected” if any atom in one is directly bond‐linked to an atom in the other, or
     if an atom in one ring is attached to an oxygen (with degree 2) that in turn is bonded to an atom in the other ring.
  3. Finally, the sugar rings should account for at least 50% of the molecule’s heavy atoms.
Note: This is a heuristic approach that will not cover all edge cases.
"""

from rdkit import Chem

def is_oligosaccharide(smiles: str):
    """
    Determines if a molecule is an oligosaccharide based on its SMILES string.
    Uses several heuristics:
      - Identify candidate sugar rings of size 5 or 6 that are saturated (all bonds in the ring are single)
        and contain exactly one oxygen (with an allowance for one nitrogen substitution). 
      - Require that at least two of the ring carbons have an exocyclic hydroxyl group.
      - Require that at least two candidate sugar rings are found and that these rings are connected
        via either a direct bond or a bridging (low-degree) oxygen.
      - Verify that the atoms in the rings make up at least 50% of the heavy atoms.
      
    Args:
       smiles (str): SMILES string of the molecule.
       
    Returns:
       bool: True if the molecule is classified as an oligosaccharide.
       str: Reason for the classification.
    """
    
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
    
    # Get all heavy atoms (atomic number > 1)
    heavy_atoms = [atom for atom in mol.GetAtoms() if atom.GetAtomicNum() > 1]
    total_heavy = len(heavy_atoms)
    
    ring_info = mol.GetRingInfo().AtomRings()
    sugar_rings = []  # Each candidate is stored as a set of atom indices
    
    # Loop over each ring in the molecule
    for ring in ring_info:
        if len(ring) not in (5, 6):
            continue
        
        # Check saturation: ensure that every bond connecting two atoms in the ring is a single bond.
        ring_is_saturated = True
        ring_set = set(ring)
        # examine all bonds in the molecule that have both endpoints in the ring
        for bond in mol.GetBonds():
            a_idx = bond.GetBeginAtomIdx()
            b_idx = bond.GetEndAtomIdx()
            if a_idx in ring_set and b_idx in ring_set:
                if bond.GetBondType() != Chem.BondType.SINGLE:
                    ring_is_saturated = False
                    break
        if not ring_is_saturated:
            continue
        
        # Count ring atoms by atomic number: oxygen (8), carbon (6) and nitrogen (7)
        o_count, c_count, n_count = 0, 0, 0
        for idx in ring:
            atomic_num = mol.GetAtomWithIdx(idx).GetAtomicNum()
            if atomic_num == 8:
                o_count += 1
            elif atomic_num == 6:
                c_count += 1
            elif atomic_num == 7:
                n_count += 1
        
        # For a typical sugar ring: exactly one oxygen.
        # For a 6-membered ring (pyranose): expect 1 oxygen and either 5 carbons or 4 carbons plus 1 nitrogen.
        # For a 5-membered ring (furanose): expect 1 oxygen and either 4 carbons or 3 carbons plus 1 nitrogen.
        if len(ring) == 6:
            if not (o_count == 1 and (c_count == 5 or (c_count == 4 and n_count == 1))):
                continue
        elif len(ring) == 5:
            if not (o_count == 1 and (c_count == 4 or (c_count == 3 and n_count == 1))):
                continue
        
        # Additional check: require that at least 2 ring carbons have exocyclic -OH groups.
        hydroxyl_count = 0
        for idx in ring:
            atom = mol.GetAtomWithIdx(idx)
            # Only check for carbons (typical sugar ring atoms except the ring oxygen)
            if atom.GetAtomicNum() != 6:
                continue
            # Look among neighbors that are not in the ring
            for nbr in atom.GetNeighbors():
                if nbr.GetIdx() in ring_set:
                    continue
                # Check if neighbor is oxygen and (heuristically) has at least one attached hydrogen.
                if nbr.GetAtomicNum() == 8 and nbr.GetTotalNumHs() > 0:
                    hydroxyl_count += 1
                    break  # count each ring carbon at most once
        if hydroxyl_count < 2:
            continue
        
        # If all checks pass, add this candidate ring.
        sugar_rings.append(ring_set)
    
    if len(sugar_rings) < 2:
        return False, f"Fewer than 2 candidate sugar rings detected (found {len(sugar_rings)})."
    
    # Build connectivity graph among sugar rings.
    # Two rings are "connected" if:
    #  (a) there is a bond directly between an atom in one ring and an atom in the other, OR
    #  (b) an atom in one ring is attached to an oxygen (with degree == 2) that in turn is bonded to an atom in the other ring.
    n = len(sugar_rings)
    graph = {i: set() for i in range(n)}
    for i in range(n):
        for j in range(i + 1, n):
            connected = False
            # Option (a): direct bond between any two ring atoms.
            for bond in mol.GetBonds():
                a_idx = bond.GetBeginAtomIdx()
                b_idx = bond.GetEndAtomIdx()
                if ((a_idx in sugar_rings[i] and b_idx in sugar_rings[j]) or 
                    (a_idx in sugar_rings[j] and b_idx in sugar_rings[i])):
                    connected = True
                    break
            # Option (b): bridging oxygen with degree 2.
            if not connected:
                for a_idx in sugar_rings[i]:
                    atom_a = mol.GetAtomWithIdx(a_idx)
                    for nbr in atom_a.GetNeighbors():
                        # Only count a bridging oxygen if it is not in the same ring, is oxygen, and its degree is 2.
                        if nbr.GetIdx() in sugar_rings[i]:
                            continue
                        if nbr.GetAtomicNum() != 8 or nbr.GetDegree() != 2:
                            continue
                        # Check if the other neighbor of this oxygen is in ring j.
                        for nbr2 in nbr.GetNeighbors():
                            if nbr2.GetIdx() == a_idx:
                                continue
                            if nbr2.GetIdx() in sugar_rings[j]:
                                connected = True
                                break
                        if connected:
                            break
                    if connected:
                        break
            if connected:
                graph[i].add(j)
                graph[j].add(i)
    
    # Check if all candidate sugar rings form a single connected component.
    visited = set()
    stack = [0]
    while stack:
        node = stack.pop()
        if node in visited:
            continue
        visited.add(node)
        for nbr in graph[node]:
            if nbr not in visited:
                stack.append(nbr)
    if len(visited) != n:
        return False, "Candidate sugar rings are detected but they are not all connected via glycosidic bonds."
    
    # Finally, count the heavy atoms that are part of any sugar ring.
    sugar_atoms = set()
    for ring in sugar_rings:
        sugar_atoms.update(ring)
    fraction = len(sugar_atoms) / total_heavy if total_heavy else 0
    if fraction < 0.5:
        return False, f"Sugar rings detected but they only constitute {fraction*100:.1f}% of heavy atoms; likely a glycoside rather than an oligosaccharide."
    
    return True, "Molecule has multiple connected, saturated sugar rings with characteristic hydroxyls and these rings account for the majority of heavy atoms; likely an oligosaccharide."

# Example usage:
if __name__ == '__main__':
    # Example: alpha-mannobiose (a disaccharide)
    test_smiles = "OC[C@H]1O[C@@H](O[C@@H]2[C@@H](CO)O[C@H](O)[C@@H](O)[C@H]2O)[C@@H](O)[C@@H](O)[C@@H]1O"
    valid, reason = is_oligosaccharide(test_smiles)
    print(valid, reason)


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:50699',
                          'name': 'oligosaccharide',
                          'definition': 'A compound in which monosaccharide '
                                        'units are joined by glycosidic '
                                        'linkages. The term is commonly used '
                                        'to refer to a defined structure as '
                                        'opposed to a polymer of unspecified '
                                        'length or a homologous mixture. When '
                                        'the linkages are of other types the '
                                        'compounds are regarded as '
                                        'oligosaccharide analogues.',
                          'parents': ['CHEBI:16646', 'CHEBI:167559'],
                          'xrefs': ['KEGG:C00930'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 146,
                           'log_lines_of_code': 4.983606621708336,
                           'indent_by_line': [   1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
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
                                                 1,
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
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 3,
                                                 3,
                                                 4,
                                                 5,
                                                 5,
                                                 2,
                                                 3,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 3,
                                                 4,
                                                 3,
                                                 4,
                                                 3,
                                                 4,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 4,
                                                 2,
                                                 3,
                                                 4,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 3,
                                                 3,
                                                 4,
                                                 3,
                                                 3,
                                                 4,
                                                 5,
                                                 4,
                                                 4,
                                                 5,
                                                 5,
                                                 2,
                                                 3,
                                                 2,
                                                 2,
                                                 2,
                                                 1,
                                                 1,
                                                 2,
                                                 1,
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
                                                 4,
                                                 4,
                                                 4,
                                                 5,
                                                 5,
                                                 5,
                                                 3,
                                                 3,
                                                 4,
                                                 5,
                                                 5,
                                                 6,
                                                 6,
                                                 7,
                                                 6,
                                                 7,
                                                 6,
                                                 6,
                                                 7,
                                                 8,
                                                 7,
                                                 8,
                                                 8,
                                                 6,
                                                 7,
                                                 5,
                                                 6,
                                                 3,
                                                 4,
                                                 4,
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
                                                 3,
                                                 4,
                                                 1,
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 1,
                                                 1,
                                                 2,
                                                 1,
                                                 1,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 1],
                           'max_indent': 8,
                           'imports': ['from rdkit import Chem'],
                           'imports_count': 1,
                           'methods_called': [   'GetBondType',
                                                 'GetNeighbors',
                                                 'GetBonds',
                                                 'GetTotalNumHs',
                                                 'GetRingInfo',
                                                 'AtomRings',
                                                 'GetDegree',
                                                 'add',
                                                 'GetAtoms',
                                                 'GetIdx',
                                                 'update',
                                                 'pop',
                                                 'GetEndAtomIdx',
                                                 'GetBeginAtomIdx',
                                                 'GetAtomWithIdx',
                                                 'MolFromSmiles',
                                                 'GetAtomicNum',
                                                 'append'],
                           'methods_called_count': 18,
                           'smarts_strings': [],
                           'smarts_strings_count': 0,
                           'defs': ['is_oligosaccharide(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, f"Fewer than 2 candidate '
                                          'sugar rings detected (found '
                                          '{len(sugar_rings)})."',
                                          'False, "Candidate sugar rings are '
                                          'detected but they are not all '
                                          'connected via glycosidic bonds."',
                                          'False, f"Sugar rings detected but '
                                          'they only constitute '
                                          '{fraction*100:.1f}% of heavy atoms; '
                                          'likely a glycoside rather than an '
                                          'oligosaccharide."',
                                          'True, "Molecule has multiple '
                                          'connected, saturated sugar rings '
                                          'with characteristic hydroxyls and '
                                          'these rings account for the '
                                          'majority of heavy atoms; likely an '
                                          'oligosaccharide."'],
                           'returns_count': 5,
                           'complexity': 7.396721324341667},
    'message': '\n'
               'Attempt failed: F1 score of 0.4249345705448489 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: '
               'OC[C@H]1O[C@@H](O[C@@H]2[C@@H](CO)O[C@H](O)[C@@H](O)[C@H]2O)[C@@H](O)[C@@H](O)[C@@H]1O '
               'NAME: alpha-mannobiose REASON: CORRECT Molecule has multiple '
               'connected sugar rings that constitute the majority of heavy '
               'atoms; likely an oligosaccharide.\n'
               ' * SMILES: '
               'O([C@@H]1[C@@H](O)[C@H](O[C@@H]2[C@@H](O)[C@H](O[C@@H]3[C@@H](O)[C@@H](O[C@@H]([C@H]3O)CO)O[C@H]4[C@H](O)[C@H](O[C@H](O)[C@@H]4O)CO)O[C@@H]([C@H]2O)CO)O[C@@H]([C@H]1O)CO)[C@@H]5O[C@@H]([C@@H](O)[C@H](O[C@@H]6O[C@@H]([C@@H](O)[C@H](O[C@@H]7O[C@@H]([C@@H](O)[C@H](O)[C@H]7O)CO)[C@H]6O)CO)[C@H]5O)CO '
               'NAME: '
               '(2S,3R,4S,5R,6R)-4-[(2S,3R,4S,5R,6R)-4-[(2S,3R,4S,5R,6R)-4-[(2S,3R,4S,5R,6R)-4-[(2S,3R,4S,5R,6R)-4-[(2S,3R,4S,5R,6R)-3,5-Dihydroxy-6-(hydroxymethyl)-4-[(2S,3R,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-3,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-3,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-3,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-3,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-6-(hydroxymethyl)oxane-2,3,5-triol '
               'REASON: CORRECT Molecule has multiple connected sugar rings '
               'that constitute the majority of heavy atoms; likely an '
               'oligosaccharide.\n'
               ' * SMILES: '
               'O([C@@H]1[C@H](O)[C@@H](O[C@H]2[C@@H](O)[C@H](O)[C@H](O[C@@H]2O[C@H]3[C@@H](O)[C@H](O)[C@H](OC3O)CO)CO)O[C@@H]([C@H]1O)CO)[C@H]4O[C@@H]([C@@H](O)[C@H](O)[C@@H]4O[C@H]5O[C@@H]([C@@H](O)[C@H](O)[C@@H]5O[C@H]6O[C@@H]([C@@H](O)[C@H](O)[C@@H]6O)CO)CO)CO '
               'NAME: '
               '(3S,4S,5S,6R)-3-[(2R,3S,4S,5S,6R)-3-[(2R,3S,4S,5R,6R)-4-[(2R,3S,4S,5S,6R)-3-[(2R,3S,4S,5S,6R)-4,5-Dihydroxy-6-(hydroxymethyl)-3-[(2R,3S,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-3,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-6-(hydroxymethyl)oxane-2,4,5-triol '
               'REASON: CORRECT Molecule has multiple connected sugar rings '
               'that constitute the majority of heavy atoms; likely an '
               'oligosaccharide.\n'
               ' * SMILES: '
               'OC[C@H]1O[C@@H](O[C@@H]2[C@@H](CO)O[C@@H](O[C@H]3[C@H](O)[C@@H](O)[C@@H](O)O[C@@H]3CO)[C@@H](O)[C@H]2O[C@H]2O[C@@H]([C@@H](O)[C@H](O)[C@H]2O)C(O)=O)[C@H](O)[C@@H](O)[C@@H]1O '
               'NAME: '
               'beta-D-Glcp-(1->4)-[alpha-D-GlcpA-(1->3)]-beta-D-Manp-(1->4)-alpha-D-Glcp '
               'REASON: CORRECT Molecule has multiple connected sugar rings '
               'that constitute the majority of heavy atoms; likely an '
               'oligosaccharide.\n'
               ' * SMILES: '
               'O([C@@H]1[C@@H](NC(=O)C)[C@@H](O[C@@H]2[C@@H](O[C@@H]3O[C@H]([C@@H](O)[C@@H](O)[C@@H]3O)C)C(O[C@@H]([C@@H]2O)CO)O)O[C@@H]([C@@H]1O)CO)[C@H]4O[C@@H]([C@@H](O)[C@H](O[C@@H]5O[C@H]([C@@H](O)[C@@H](O)[C@@H]5O)C)[C@H]4NC(=O)C)CO '
               'NAME: '
               'N-[(2R,3R,4R,5R,6R)-4-[(2S,3R,4R,5S,6R)-3-Acetamido-5-hydroxy-6-(hydroxymethyl)-4-[(2S,3S,4R,5S,6S)-3,4,5-trihydroxy-6-methyloxan-2-yl]oxyoxan-2-yl]oxy-2-[(3R,4S,5S,6R)-2,5-dihydroxy-6-(hydroxymethyl)-3-[(2S,3S,4R,5S,6S)-3,4,5-trihydroxy-6-methyloxan-2-yl]oxyoxan-4-yl]oxy-5-hydroxy-6-(hydroxymethyl)oxan-3-yl]acetamide '
               'REASON: CORRECT Molecule has multiple connected sugar rings '
               'that constitute the majority of heavy atoms; likely an '
               'oligosaccharide.\n'
               ' * SMILES: '
               'O([C@H]1O[C@@H]([C@@H](O)[C@H](O)[C@H]1O[C@H]2O[C@@H]([C@@H](O)[C@H](O)[C@H]2O)CO)CO)[C@H]3[C@H](O)[C@H](OC(O)[C@@H]3O)CO '
               'NAME: '
               '(3R,4S,5R,6R)-4-[(2R,3R,4S,5S,6R)-4,5-Dihydroxy-6-(hydroxymethyl)-3-[(2R,3R,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-6-(hydroxymethyl)oxane-2,3,5-triol '
               'REASON: CORRECT Molecule has multiple connected sugar rings '
               'that constitute the majority of heavy atoms; likely an '
               'oligosaccharide.\n'
               ' * SMILES: '
               'C[C@@H]1O[C@@H](O[C@@H]2[C@@H](O)[C@@H](O)[C@@H](CO)O[C@H]2O[C@@H]2[C@@H](CO)O[C@@H](O)[C@H](O)[C@H]2O)[C@@H](O)[C@H](O)[C@@H]1O '
               'NAME: alpha-L-Fucp-(1->2)-beta-D-Galp-(1->4)-beta-D-Glcp '
               'REASON: CORRECT Molecule has multiple connected sugar rings '
               'that constitute the majority of heavy atoms; likely an '
               'oligosaccharide.\n'
               ' * SMILES: '
               'C1([C@@H]([C@H]([C@@H]([C@H](O1)CO)O)O[C@H]2[C@@H]([C@H]([C@@H]([C@H](O2)CO)O)O[C@H]3[C@@H]([C@H]([C@@H]([C@H](O3)CO)O)O[C@H]4[C@@H]([C@H]([C@@H]([C@H](O4)CO)O)O[C@H]5[C@@H]([C@H]([C@@H]([C@H](O5)CO)O)O[C@H]6[C@@H]([C@H]([C@@H]([C@H](O6)CO)O)O)O)O)O)O)O)O)O '
               'NAME: laminarihexaose REASON: CORRECT Molecule has multiple '
               'connected sugar rings that constitute the majority of heavy '
               'atoms; likely an oligosaccharide.\n'
               ' * SMILES: '
               'O([C@H]1[C@@H](O)[C@H](O)[C@@H](O[C@H]1C)O)[C@@H]2O[C@@H]([C@@H](O)[C@H](O)[C@H]2O)CO '
               'NAME: beta-D-Glcp-(1->4)-alpha-L-Fucp REASON: CORRECT Molecule '
               'has multiple connected sugar rings that constitute the '
               'majority of heavy atoms; likely an oligosaccharide.\n'
               ' * SMILES: '
               'O1[C@@H]([C@@H](O[C@@H]2O[C@@H]([C@H](O)[C@H](O)[C@H]2O)CO)[C@H](O)[C@@H](O)[C@@H]1O[C@H]3[C@H](O)[C@H](OC(O)[C@@H]3O)CO)CO '
               'NAME: beta-D-Galp-(1->4)-beta-D-Glcp-(1->3)-D-Glcp REASON: '
               'CORRECT Molecule has multiple connected sugar rings that '
               'constitute the majority of heavy atoms; likely an '
               'oligosaccharide.\n'
               ' * SMILES: '
               'O([C@@H]1[C@@H](O)C(O[C@@H]2[C@@H](O)C(O[C@@H]3[C@H](O)[C@@H](O)C(O[C@@H]3CO)O[C@H]4[C@H](O)[C@@H](O)C(O[C@@H]4CO)O)O[C@@H]([C@@H]2O)CO)O[C@@H]([C@@H]1O)CO)C5O[C@@H]([C@H](O)[C@H](OC6O[C@@H]([C@H](O)[C@H](OC7O[C@@H]([C@H](O)[C@H](OC8O[C@@H]([C@H](O)[C@H](O)[C@H]8O)CO)[C@H]7O)CO)[C@H]6O)CO)[C@H]5O)CO '
               'NAME: '
               '(3R,4S,5R,6R)-2-[(3R,4S,5S,6R)-2-[(3R,4S,5S,6R)-2-[(3R,4S,5S,6R)-2-[(3R,4S,5S,6R)-2-[(3R,4S,5S,6R)-2-[(2R,3R,4R,5R)-4,5-Dihydroxy-2-(hydroxymethyl)-6-[(2R,3S,4R,5R)-4,5,6-trihydroxy-2-(hydroxymethyl)oxan-3-yl]oxyoxan-3-yl]oxy-3,5-dihydroxy-6-(hydroxymethyl)oxan-4-yl]oxy-3,5-dihydroxy-6-(hydroxymethyl)oxan-4-yl]oxy-3,5-dihydroxy-6-(hydroxymethyl)oxan-4-yl]oxy-3,5-dihydroxy-6-(hydroxymethyl)oxan-4-yl]oxy-3,5-dihydroxy-6-(hydroxymethyl)oxan-4-yl]oxy-6-(hydroxymethyl)oxane-3,4,5-triol '
               'REASON: CORRECT Molecule has multiple connected sugar rings '
               'that constitute the majority of heavy atoms; likely an '
               'oligosaccharide.\n'
               ' * SMILES: '
               'O([C@@H]1[C@@H](O)[C@@H](O[C@@H]([C@@H]1O)CO)O[C@H]2[C@H](O)[C@@H](O)[C@@H](OC2)O)[C@@H]3O[C@@H]([C@H](O)[C@H](O[C@@H]4OC(=C(O)[C@H](O)[C@H]4O)C(O)=O)[C@H]3O)CO '
               'NAME: '
               '(2R,3R,4R)-2-[(2S,3R,4S,5S,6R)-2-[(2R,3S,4S,5R,6S)-3,5-Dihydroxy-2-(hydroxymethyl)-6-[(3R,4R,5R,6R)-4,5,6-trihydroxyoxan-3-yl]oxyoxan-4-yl]oxy-3,5-dihydroxy-6-(hydroxymethyl)oxan-4-yl]oxy-3,4,5-trihydroxy-3,4-dihydro-2H-pyran-6-carboxylic '
               'acid REASON: CORRECT Molecule has multiple connected sugar '
               'rings that constitute the majority of heavy atoms; likely an '
               'oligosaccharide.\n'
               ' * SMILES: '
               'OC[C@H]1O[C@H](O[C@@H]2[C@@H](O)C(O)O[C@H](CO)[C@H]2O)[C@H](O)[C@@H](O)[C@@H]1O '
               'NAME: nigerose REASON: CORRECT Molecule has multiple connected '
               'sugar rings that constitute the majority of heavy atoms; '
               'likely an oligosaccharide.\n'
               ' * SMILES: '
               'O([C@@H]1[C@@H](O[C@@H]2O[C@H]([C@@H](O)[C@@H](O)[C@@H]2O)C)[C@H](O[C@@H]([C@@H]1O)CO)O)[C@H]3O[C@@H]([C@H](O)[C@H](O)[C@H]3O)CO '
               'NAME: alpha-L-Fucp-(1->2)-[alpha-D-Galp-(1->3)]-alpha-D-Galp '
               'REASON: CORRECT Molecule has multiple connected sugar rings '
               'that constitute the majority of heavy atoms; likely an '
               'oligosaccharide.\n'
               ' * SMILES: '
               'O([C@@H]1[C@@H](O[C@H]2O[C@@H]([C@@H](O)[C@H](O)[C@H]2O)CO)[C@H](O[C@@H]([C@@H]1O)CO)O)[C@H]3O[C@@H]([C@@H](O)[C@H](O)[C@@H]3O)CO '
               'NAME: '
               '(2R,3S,4S,5S,6R)-2-[(2S,3R,4S,5S,6R)-2,5-Dihydroxy-6-(hydroxymethyl)-3-[(2R,3R,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-4-yl]oxy-6-(hydroxymethyl)oxane-3,4,5-triol '
               'REASON: CORRECT Molecule has multiple connected sugar rings '
               'that constitute the majority of heavy atoms; likely an '
               'oligosaccharide.\n'
               ' * SMILES: '
               'O[C@@H]1CO[C@@H](O[C@@H]2CO[C@@H](O[C@@H]3CO[C@@H](O[C@@H]4COC(O)[C@H](O)[C@H]4O)[C@H](O)[C@H]3O)[C@H](O)[C@H]2O)[C@H](O)[C@H]1O '
               'NAME: xylotetraose REASON: CORRECT Molecule has multiple '
               'connected sugar rings that constitute the majority of heavy '
               'atoms; likely an oligosaccharide.\n'
               ' * SMILES: '
               'O([C@H]1[C@H](O)[C@H](O)[C@H](O[C@H]2[C@H](O)[C@H](O)[C@@H](O[C@@H]2CO)O[C@H]3[C@H](O)[C@H](O)C(O[C@@H]3CO)O)O[C@@H]1CO)[C@@H]4O[C@@H]([C@@H](O[C@@H]5O[C@@H]([C@@H](O)[C@H](O)[C@@H]5O)CO)[C@H](O)[C@@H]4O)CO '
               'NAME: '
               '(2S,3S,4S,5S,6R)-2-[(2R,3S,4R,5S,6S)-6-[(2R,3S,4R,5S,6S)-6-[(2R,3S,4R,5S,6S)-4,5-Dihydroxy-2-(hydroxymethyl)-6-[(2R,3S,4R,5S)-4,5,6-trihydroxy-2-(hydroxymethyl)oxan-3-yl]oxyoxan-3-yl]oxy-4,5-dihydroxy-2-(hydroxymethyl)oxan-3-yl]oxy-4,5-dihydroxy-2-(hydroxymethyl)oxan-3-yl]oxy-6-(hydroxymethyl)oxane-3,4,5-triol '
               'REASON: CORRECT Molecule has multiple connected sugar rings '
               'that constitute the majority of heavy atoms; likely an '
               'oligosaccharide.\n'
               ' * SMILES: '
               'O([C@H]1[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]1CO)O[C@@H]2[C@@H](O)[C@@H](O[C@@H]([C@@H]2O)CO)O[C@H]3[C@H](O)[C@@H](O)[C@@H](O[C@@H]3CO)O)[C@@H]4O[C@@H]([C@H](O)[C@H](O[C@H]5O[C@@H]([C@H](O)[C@H](O)[C@H]5O)CO)[C@H]4O[C@H]6O[C@@H]([C@H](O)[C@H](O)[C@H]6O)C)CO '
               'NAME: '
               'N-[(2S,3R,4R,5S,6R)-2-[(2R,3S,4S,5R,6S)-3,5-Dihydroxy-2-(hydroxymethyl)-6-[(2R,3S,4R,5R,6R)-4,5,6-trihydroxy-2-(hydroxymethyl)oxan-3-yl]oxyoxan-4-yl]oxy-4-hydroxy-5-[(2S,3R,4S,5S,6R)-5-hydroxy-6-(hydroxymethyl)-4-[(2R,3R,4S,5R,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-3-[(2R,3R,4S,5R,6R)-3,4,5-trihydroxy-6-methyloxan-2-yl]oxyoxan-2-yl]oxy-6-(hydroxymethyl)oxan-3-yl]acetamide '
               'REASON: CORRECT Molecule has multiple connected sugar rings '
               'that constitute the majority of heavy atoms; likely an '
               'oligosaccharide.\n'
               ' * SMILES: '
               'O([C@H]1[C@H](O)[C@H](O[C@@H](O)[C@@H]1O)CO)[C@H]2OC[C@@H](O)[C@H](O[C@H]3OC[C@@H](O)[C@H](O)[C@H]3O)[C@H]2O '
               'NAME: '
               'alpha-D-Xylopyranosyl-(1->3)-alpha-D-Xylopyranosyl-(1->3)-beta-D-Glucopyranose '
               'REASON: CORRECT Molecule has multiple connected sugar rings '
               'that constitute the majority of heavy atoms; likely an '
               'oligosaccharide.\n'
               ' * SMILES: '
               'O([C@@H]1[C@@H](O[C@@H]2O[C@@H]([C@H](O)[C@H](O)[C@H]2O)CO)[C@@H](O[C@@H]([C@H]1O)CO)O)[C@@H]3O[C@@H]([C@@H](O)[C@H](O)[C@H]3O)CO '
               'NAME: '
               '(2S,3R,4S,5S,6R)-2-[(2R,3R,4S,5R,6R)-2,5-Dihydroxy-6-(hydroxymethyl)-3-[(2S,3R,4S,5R,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-4-yl]oxy-6-(hydroxymethyl)oxane-3,4,5-triol '
               'REASON: CORRECT Molecule has multiple connected sugar rings '
               'that constitute the majority of heavy atoms; likely an '
               'oligosaccharide.\n'
               ' * SMILES: '
               'O([C@@H]1[C@@H](O)C(O[C@@H]([C@H]1O)CO)O[C@@H]2[C@@H](O)[C@H](O)[C@H](O[C@H]2O)CO)[C@H]3O[C@@H]([C@@H](O)[C@H](O)[C@H]3O)CO '
               'NAME: alpha-D-Glcp-(1->3)-?-D-Glcp-(1->2)-beta-D-Glcp REASON: '
               'CORRECT Molecule has multiple connected sugar rings that '
               'constitute the majority of heavy atoms; likely an '
               'oligosaccharide.\n'
               ' * SMILES: '
               'O([C@@H]1[C@@H](NC(=O)C)[C@@H](O[C@@H]([C@H]1O[C@@H]2O[C@H]([C@@H](O)[C@@H](O)[C@@H]2O)C)CO)O[C@@H]3[C@@H](O)[C@@H](O[C@@H]([C@@H]3O)CO)O[C@H]4[C@H](O)[C@@H](O)[C@@H](O[C@@H]4CO)O)[C@@H]5O[C@@H]([C@H](O)[C@H](O[C@@H]6O[C@@H]([C@@H](O)[C@H](O[C@@H]7O[C@@H]([C@H](O)[C@H](O)[C@H]7O)CO)[C@H]6NC(=O)C)CO)[C@H]5O)CO '
               'NAME: '
               'N-[(2S,3R,4R,5S,6R)-2-[(2R,3R,4S,5S,6R)-2-[(2S,3R,4R,5S,6R)-3-Acetamido-2-[(2R,3S,4S,5R,6S)-3,5-dihydroxy-2-(hydroxymethyl)-6-[(2R,3S,4R,5R,6R)-4,5,6-trihydroxy-2-(hydroxymethyl)oxan-3-yl]oxyoxan-4-yl]oxy-6-(hydroxymethyl)-5-[(2S,3S,4R,5S,6S)-3,4,5-trihydroxy-6-methyloxan-2-yl]oxyoxan-4-yl]oxy-3,5-dihydroxy-6-(hydroxymethyl)oxan-4-yl]oxy-5-hydroxy-6-(hydroxymethyl)-4-[(2R,3R,4S,5R,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-3-yl]acetamide '
               'REASON: CORRECT Molecule has multiple connected sugar rings '
               'that constitute the majority of heavy atoms; likely an '
               'oligosaccharide.\n'
               ' * SMILES: '
               'O([C@@H]1[C@@H](O)[C@H](O[C@H]2[C@@H](O)[C@H](O[C@@H](O[C@H]3[C@H](O)[C@@H](O)[C@@H](OC3)O)[C@@H]2O)CO)O[C@@H]([C@@H]1O)CO)[C@@H]4O[C@@H]([C@@H](O[C@H]5O[C@@H]([C@H](O)[C@H](O)[C@H]5NC(=O)C)CO)[C@H](O)[C@H]4O)C(O)=O '
               'NAME: '
               '(2S,3S,4R,5R,6R)-3-[(2R,3R,4R,5R,6R)-3-Acetamido-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-6-[(2S,3R,4S,5S,6R)-2-[(2R,3S,4S,5R,6S)-3,5-dihydroxy-2-(hydroxymethyl)-6-[(3R,4R,5R,6R)-4,5,6-trihydroxyoxan-3-yl]oxyoxan-4-yl]oxy-3,5-dihydroxy-6-(hydroxymethyl)oxan-4-yl]oxy-4,5-dihydroxyoxane-2-carboxylic '
               'acid REASON: CORRECT Molecule has multiple connected sugar '
               'rings that constitute the majority of heavy atoms; likely an '
               'oligosaccharide.\n'
               ' * SMILES: '
               'OC[C@H]1OC(O)[C@H](O)[C@@H](O[C@H]2OC[C@@H](O)[C@H](O)[C@H]2O)[C@@H]1O '
               'NAME: alpha-D-Xylp-(1->3)-D-Glcp REASON: CORRECT Molecule has '
               'multiple connected sugar rings that constitute the majority of '
               'heavy atoms; likely an oligosaccharide.\n'
               ' * SMILES: '
               'O([C@@H]1[C@@H](O)[C@H](O[C@H]2[C@H](O[C@@H]3O[C@H]([C@@H](O)[C@@H](O)[C@@H]3O)C)[C@@H](O)C(O[C@@H]2CO)O)O[C@@H]([C@@H]1O)CO)[C@@H]4O[C@@H]([C@@H](O[C@@H]5O[C@@H]([C@H](O)[C@H](O)[C@H]5O[C@@H]6O[C@H]([C@@H](O)[C@@H](O)[C@@H]6O)C)CO)[C@H](O)[C@H]4NC(=O)C)CO '
               'NAME: '
               'N-[(2S,3R,4R,5S,6R)-5-[(2S,3R,4S,5R,6R)-4,5-Dihydroxy-6-(hydroxymethyl)-3-[(2S,3S,4R,5S,6S)-3,4,5-trihydroxy-6-methyloxan-2-yl]oxyoxan-2-yl]oxy-2-[(2S,3R,4S,5S,6R)-2-[(2R,3R,4R,5R)-5,6-dihydroxy-2-(hydroxymethyl)-4-[(2S,3S,4R,5S,6S)-3,4,5-trihydroxy-6-methyloxan-2-yl]oxyoxan-3-yl]oxy-3,5-dihydroxy-6-(hydroxymethyl)oxan-4-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-3-yl]acetamide '
               'REASON: CORRECT Molecule has multiple connected sugar rings '
               'that constitute the majority of heavy atoms; likely an '
               'oligosaccharide.\n'
               'False positives: SMILES: O=C1OC(=CC2=C1C(O)C(O)C(O2)C)C=CC '
               'NAME: Radicinol REASON: WRONGLY CLASSIFIED Molecule has '
               'multiple connected sugar rings that constitute the majority of '
               'heavy atoms; likely an oligosaccharide.\n'
               ' * SMILES: '
               'COc1cc2O[C@H]3O[C@H]4O[C@H]4[C@H]3c2c2oc(=O)c3C(=O)CCc3c12 '
               'NAME: Aflatoxin B1-endo-8,9-epoxide REASON: WRONGLY CLASSIFIED '
               'Molecule has multiple connected sugar rings that constitute '
               'the majority of heavy atoms; likely an oligosaccharide.\n'
               ' * SMILES: O=C1O[C@@H](C=CC)[C@H]2C1=C[C@@H](O)[C@@H](C=CC)O2 '
               'NAME: Waol A REASON: WRONGLY CLASSIFIED Molecule has multiple '
               'connected sugar rings that constitute the majority of heavy '
               'atoms; likely an oligosaccharide.\n'
               ' * SMILES: '
               'C[C@@H]1O[C@@H](O[C@@H]2[C@@H](O)[C@@H](O)[C@@H](CO)O[C@H]2O[C@H]2[C@H](O)[C@@H](CO)OC(O)[C@@H]2NC(C)=O)[C@@H](O)[C@H](O)[C@@H]1O '
               'NAME: alpha-L-Fucp-(1->2)-beta-D-Galp-(1->3)-D-GlcpNAc REASON: '
               'WRONGLY CLASSIFIED Molecule has multiple connected sugar rings '
               'that constitute the majority of heavy atoms; likely an '
               'oligosaccharide.\n'
               ' * SMILES: O=C1OC2=C(CO[C@H](C2)C[C@H](O)C)C(=C1)OC NAME: '
               'Phomopsinone B REASON: WRONGLY CLASSIFIED Molecule has '
               'multiple connected sugar rings that constitute the majority of '
               'heavy atoms; likely an oligosaccharide.\n'
               ' * SMILES: '
               'COC[C@H]1O[C@@H](OC)[C@H](N)[C@@H](O[C@@H]2O[C@H](C)[C@@H](O)C[C@@H]2O)[C@H]1O '
               'NAME: beta-D-Tyvp-(1->3)-beta-D-GalpN6,OMe2 REASON: WRONGLY '
               'CLASSIFIED Molecule has multiple connected sugar rings that '
               'constitute the majority of heavy atoms; likely an '
               'oligosaccharide.\n'
               ' * SMILES: '
               'COc1cc2O[C@H]3O[C@@H](O)[C@H](O)[C@H]3c2c2oc(=O)c3C(=O)CCc3c12 '
               'NAME: Aflatoxin B1 diol REASON: WRONGLY CLASSIFIED Molecule '
               'has multiple connected sugar rings that constitute the '
               'majority of heavy atoms; likely an oligosaccharide.\n'
               ' * SMILES: '
               'O([C@H]1[C@H](O)[C@H](O[C@@H](O)[C@@H]1N)CO)[C@@H]2O[C@@H]([C@H](O)[C@H](O)[C@H]2O)CO '
               'NAME: beta-D-Galp-(1->3)-beta-D-GlcpN REASON: WRONGLY '
               'CLASSIFIED Molecule has multiple connected sugar rings that '
               'constitute the majority of heavy atoms; likely an '
               'oligosaccharide.\n'
               ' * SMILES: O1C=2C3=C(OC=C3)C=CC2C(=O)C=C1C=4C(OC)=CC=CC4 NAME: '
               '2-(2-Methoxyphenyl)-4H-furo[2,3-h]-1-benzopyran-4-one REASON: '
               'WRONGLY CLASSIFIED Molecule has multiple connected sugar rings '
               'that constitute the majority of heavy atoms; likely an '
               'oligosaccharide.\n'
               ' * SMILES: '
               'O([C@@H]1[C@@H](NC(=O)C)C(O[C@@H]([C@H]1O)CO)O)[C@@H]2O[C@H]([C@@H](O[C@@H]3O[C@@H]([C@H](O)[C@H](O)[C@H]3O)CO)[C@@H](O)[C@@H]2O)C '
               'NAME: '
               'N-[(3R,4R,5S,6R)-4-[(2S,3S,4S,5S,6S)-3,4-Dihydroxy-6-methyl-5-[(2S,3R,4S,5R,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-2,5-dihydroxy-6-(hydroxymethyl)oxan-3-yl]acetamide '
               'REASON: WRONGLY CLASSIFIED Molecule has multiple connected '
               'sugar rings that constitute the majority of heavy atoms; '
               'likely an oligosaccharide.\n'
               ' * SMILES: O=C1C2=C(CO[C@H]3[C@@H]2[C@H](O)CCO3)CC1 NAME: '
               '4R*,7S*,11S*,2H-3,4,4a,5a,7,8-hexhydro-4-hydroxy-pyrano[2,3-b]cyclopenta[d]pyran-9(6H)-one '
               'REASON: WRONGLY CLASSIFIED Molecule has multiple connected '
               'sugar rings that constitute the majority of heavy atoms; '
               'likely an oligosaccharide.\n'
               ' * SMILES: '
               'O1[C@@H](O[C@@H]2[C@@H](NC(=O)C)[C@H](O[C@@H]([C@@H]2O)CO)O)[C@H](O[C@@H]3O[C@H]([C@@H](O)[C@@H](O)[C@@H]3O)C)[C@@H](O)[C@@H](O[C@@H]4O[C@@H]([C@H](O)[C@H](O)[C@H]4O)CO)[C@H]1CO '
               'NAME: '
               'N-[(2S,3R,4R,5R,6R)-2,5-Dihydroxy-4-[(2R,3R,4S,5R,6R)-4-hydroxy-6-(hydroxymethyl)-5-[(2S,3R,4S,5R,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-3-[(2S,3S,4R,5S,6S)-3,4,5-trihydroxy-6-methyloxan-2-yl]oxyoxan-2-yl]oxy-6-(hydroxymethyl)oxan-3-yl]acetamide '
               'REASON: WRONGLY CLASSIFIED Molecule has multiple connected '
               'sugar rings that constitute the majority of heavy atoms; '
               'likely an oligosaccharide.\n'
               ' * SMILES: O1C=2C3=C(OC=C3)C=CC2C(=O)C=C1C4=CC(OC)=CC=C4 NAME: '
               'Cauliflorin A REASON: WRONGLY CLASSIFIED Molecule has multiple '
               'connected sugar rings that constitute the majority of heavy '
               'atoms; likely an oligosaccharide.\n'
               ' * SMILES: '
               '[Na+].O=C([O-])C(C(OC)C(C1OC2(OC(C3OC(C4OC(C5OC(O)(C(C)CC5C)CO)CC4C)(CC)CC3)(C)CC2)CC(C1C)O)C)C '
               'NAME: Monensin sodium salt REASON: WRONGLY CLASSIFIED Molecule '
               'has multiple connected sugar rings that constitute the '
               'majority of heavy atoms; likely an oligosaccharide.\n'
               ' * SMILES: '
               'O1C([C@H](O)[C@@]2([C@]1(OC=3C2=C4OC(=CC(=O)C4=C(OC)C3)C5=CC=CC=C5)[H])[H])(C)C '
               'NAME: Multijuginol REASON: WRONGLY CLASSIFIED Molecule has '
               'multiple connected sugar rings that constitute the majority of '
               'heavy atoms; likely an oligosaccharide.\n'
               ' * SMILES: '
               '[NH3+][C@H]1[C@H](O)[C@@H](CO)O[C@@H](O[C@H]2O[C@H](CO)[C@@H](O)[C@H]([NH3+])[C@H]2O)[C@@H]1O '
               "NAME: 3,3'-neotrehalosadiamine(2+) REASON: WRONGLY CLASSIFIED "
               'Molecule has multiple connected sugar rings that constitute '
               'the majority of heavy atoms; likely an oligosaccharide.\n'
               ' * SMILES: O=C1C2=C(OC3=C1COC(=C3)C)C=C(O)C(=C2)O NAME: '
               'Myxotrichin C REASON: WRONGLY CLASSIFIED Molecule has multiple '
               'connected sugar rings that constitute the majority of heavy '
               'atoms; likely an oligosaccharide.\n'
               ' * SMILES: '
               'C[C@@H]1O[C@@H](O[C@H]2[C@@H](O[C@H](CO)[C@H](O)[C@@H]2O[C@H]2O[C@H](CO)[C@H](O)[C@H](O[C@@H]3O[C@H](CO)[C@H](O)[C@H](O)[C@H]3O)[C@H]2NC(C)=O)O[C@H]2[C@H](O)[C@@H](O)C(O)O[C@@H]2CO)[C@@H](O)[C@H](O)[C@@H]1O '
               'NAME: '
               'alpha-L-Fucp-(1->2)-[beta-D-Galp-(1->3)-alpha-D-GalpNAc-(1->3)]-beta-D-Galp-(1->4)-D-Glcp '
               'REASON: WRONGLY CLASSIFIED Molecule has multiple connected '
               'sugar rings that constitute the majority of heavy atoms; '
               'likely an oligosaccharide.\n'
               ' * SMILES: O=C1CCC2(O1)OC(=O)c1ccccc21 NAME: Spirodilactone '
               'REASON: WRONGLY CLASSIFIED Molecule has multiple connected '
               'sugar rings that constitute the majority of heavy atoms; '
               'likely an oligosaccharide.\n'
               ' * SMILES: '
               'C[C@@H]1O[C@@H](O[C@H]2[C@H](O)[C@H](O)[C@H](C)O[C@H]2O[C@H]2[C@H](O)[C@H](O)[C@H](C)O[C@H]2O[C@H]2[C@H](O)[C@H](O)[C@H](C)O[C@H]2OCCCCCCN)[C@@H](O)[C@H](O)[C@@H]1O '
               'NAME: '
               'alpha-L-Fucp-(1->2)-alpha-L-Fucp-(1->2)-alpha-L-Fucp-(1->2)-alpha-L-FucpO[CH2]6NH2 '
               'REASON: WRONGLY CLASSIFIED Molecule has multiple connected '
               'sugar rings that constitute the majority of heavy atoms; '
               'likely an oligosaccharide.\n'
               ' * SMILES: COc1cc(=O)oc2[C@@H](C)[C@H](C)O[C@@H](O)c12 NAME: '
               'isochlamydosporol REASON: WRONGLY CLASSIFIED Molecule has '
               'multiple connected sugar rings that constitute the majority of '
               'heavy atoms; likely an oligosaccharide.\n'
               ' * SMILES: '
               'O([C@@H]1[C@H](O)[C@H](O[C@H]2[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]2CO)O[C@H]3[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]3CO)O)O[C@@H]([C@H]1O)CO)[C@H]4O[C@@H]([C@@H](O)[C@H](O)[C@@H]4O[C@H]5O[C@@H]([C@@H](O)[C@H](O)[C@@H]5O[C@H]6O[C@@H]([C@@H](O)[C@H](O)[C@@H]6O[C@H]7O[C@@H]([C@@H](O)[C@H](O[C@H]8O[C@@H]([C@@H](O)[C@H](O)[C@H]8O[C@H]9O[C@@H]([C@@H](O)[C@H](O)[C@H]9O)CO)CO)[C@H]7O)CO)CO)CO)CO '
               'NAME: '
               'N-[(2R,3R,4R,5S,6R)-5-[(2S,3R,4R,5S,6R)-3-Acetamido-5-[(2S,3S,4S,5R,6R)-4-[(2R,3S,4S,5S,6R)-3-[(2R,3S,4S,5S,6R)-3-[(2R,3S,4S,5S,6R)-3-[(2R,3R,4S,5R,6R)-4-[(2R,3R,4S,5S,6R)-4,5-dihydroxy-6-(hydroxymethyl)-3-[(2R,3R,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-3,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-3,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-2,4-dihydroxy-6-(hydroxymethyl)oxan-3-yl]acetamide '
               'REASON: WRONGLY CLASSIFIED Molecule has multiple connected '
               'sugar rings that constitute the majority of heavy atoms; '
               'likely an oligosaccharide.\n'
               ' * SMILES: '
               'C123C45[C@@H](OC([C@@H]4O)=O)O[C@]1([C@]6([C@@H](C(=O)O[C@]6([C@@H]2O)[H])C)[H])C(=O)O[C@@]3([C@@H]([C@]5(C(C)(C)C)[H])O)[H] '
               'NAME: Ginkgolide M REASON: WRONGLY CLASSIFIED Molecule has '
               'multiple connected sugar rings that constitute the majority of '
               'heavy atoms; likely an oligosaccharide.\n'
               ' * SMILES: '
               'O([C@@H]1[C@@H](O)[C@@H](O[C@@H]2[C@@H](O)[C@@H](O[C@@H]3[C@@H](O)[C@H](O[C@@H]([C@H]3O)CO)O[C@H]4[C@H](O)[C@H](OC(O)[C@@H]4O)CO)O[C@@H]([C@H]2O)CO)O[C@@H]([C@H]1O)CO)[C@H]5O[C@@H]([C@@H](O)[C@H](O[C@H]6O[C@@H]([C@@H](O)[C@H](O[C@H]7O[C@@H]([C@@H](O)[C@H](O)[C@H]7O)CO)[C@H]6O)CO)[C@H]5O)CO '
               'NAME: '
               '(3R,4S,5R,6R)-4-[(2R,3R,4S,5R,6R)-4-[(2R,3R,4S,5R,6R)-4-[(2R,3R,4S,5R,6R)-4-[(2R,3R,4S,5R,6R)-4-[(2R,3R,4S,5R,6R)-3,5-Dihydroxy-6-(hydroxymethyl)-4-[(2R,3R,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-3,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-3,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-3,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-3,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-6-(hydroxymethyl)oxane-2,3,5-triol '
               'REASON: WRONGLY CLASSIFIED Molecule has multiple connected '
               'sugar rings that constitute the majority of heavy atoms; '
               'likely an oligosaccharide.\n'
               ' * SMILES: COc1ccc-2c(OCc3c-2oc2c4C=CC(C)(C)Oc4c(O)cc32)c1 '
               'NAME: lespeflorin H2 REASON: WRONGLY CLASSIFIED Molecule has '
               'multiple connected sugar rings that constitute the majority of '
               'heavy atoms; likely an oligosaccharide.\n'
               'False negatives: SMILES: '
               'O1[C@@H](O[C@H]2[C@@H](O)[C@H](O[C@H](O)[C@@H]2O)CO)[C@H](NC(=O)C)[C@@H](O[C@@H]3O[C@@H]([C@H](O)[C@H](O)[C@H]3O)CO)[C@@H](O)[C@H]1CO[C@@H]4O[C@@H]([C@@H](O)[C@H](O)[C@H]4NC(=O)C)CO '
               'NAME: '
               'N-[(2R,3R,4R,5S,6R)-2-[[(2R,3R,4R,5R,6S)-5-Acetamido-3-hydroxy-6-[(2S,3R,4S,5S,6R)-2,3,5-trihydroxy-6-(hydroxymethyl)oxan-4-yl]oxy-4-[(2R,3R,4S,5R,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]methoxy]-4,5-dihydroxy-6-(hydroxymethyl)oxan-3-yl]acetamide '
               'REASON: MISSED Candidate sugar rings are detected but they are '
               'not all connected via glycosidic bonds.\n'
               ' * SMILES: '
               'O1[C@@H]([C@@H](O)[C@H](O[C@@H]2O[C@@H]([C@@H](O)[C@H](O)[C@H]2O)CO)[C@@H](O)[C@@H]1OC[C@H]3O[C@@H](OC[C@H]4O[C@@H](O)[C@H](O)[C@@H](O)[C@@H]4O)[C@H](O)[C@@H](O)[C@@H]3O)CO[C@@H]5O[C@@H]([C@@H](O)[C@H](O[C@@H]6O[C@@H]([C@@H](O)[C@H](O)[C@H]6O)CO)[C@H]5O)CO[C@@H]7O[C@@H]([C@@H](O)[C@H](O)[C@H]7O)CO '
               'NAME: '
               '(2R,3R,4S,5S,6R)-6-[[(2R,3R,4S,5S,6R)-6-[[(2R,3R,4S,5R,6R)-6-[[(2R,3R,4S,5R,6R)-3,5-Dihydroxy-4-[(2R,3R,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-6-[[(2R,3R,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxymethyl]oxan-2-yl]oxymethyl]-3,5-dihydroxy-4-[(2R,3R,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxymethyl]-3,4,5-trihydroxyoxan-2-yl]oxymethyl]oxane-2,3,4,5-tetrol '
               'REASON: MISSED Candidate sugar rings are detected but they are '
               'not all connected via glycosidic bonds.\n'
               ' * SMILES: '
               'O([C@H]1[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]1CO)OC[C@@H](O)[C@H](O)[C@H](O[C@@H]2O[C@@H]([C@H](O)[C@H](O)[C@H]2O)CO)[C@@H](NC(=O)C)CO)[C@@H]3O[C@@H]([C@H](O)[C@H](O[C@@H]4O[C@@H]([C@H](O)[C@H](O)[C@H]4O)CO)[C@H]3O)CO '
               'NAME: '
               'N-[(2R,3R,4R,5S,6R)-2-[(2R,3S,4R,5S)-5-Acetamido-2,3,6-trihydroxy-4-[(2S,3R,4S,5R,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyhexoxy]-5-[(2S,3R,4S,5S,6R)-3,5-dihydroxy-6-(hydroxymethyl)-4-[(2S,3R,4S,5R,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-3-yl]acetamide '
               'REASON: MISSED Candidate sugar rings are detected but they are '
               'not all connected via glycosidic bonds.\n'
               ' * SMILES: '
               'O([C@@H]1[C@@H](O)[C@H](O[C@H]2[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]2CO)OC[C@@H](O)[C@H](O)[C@H](O[C@@H]3O[C@@H]([C@H](O)[C@H](O)[C@H]3O)CO)[C@@H](NC(=O)C)CO)O[C@@H]([C@@H]1O)CO)[C@@H]4O[C@@H]([C@@H](O)[C@H](O[C@@H]5O[C@@H]([C@H](O)[C@H](O)[C@H]5O)CO)[C@H]4NC(=O)C)CO '
               'NAME: '
               'N-[(2R,3R,4R,5S,6R)-5-[(2S,3R,4S,5S,6R)-4-[(2S,3R,4R,5S,6R)-3-Acetamido-5-hydroxy-6-(hydroxymethyl)-4-[(2R,3R,4S,5R,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-3,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-2-[(2R,3S,4R,5S)-5-acetamido-2,3,6-trihydroxy-4-[(2R,3R,4S,5R,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyhexoxy]-4-hydroxy-6-(hydroxymethyl)oxan-3-yl]acetamide '
               'REASON: MISSED Candidate sugar rings are detected but they are '
               'not all connected via glycosidic bonds.\n'
               ' * SMILES: '
               'O([C@@H]1[C@@H](O)[C@H](O)[C@H](O[C@@H]1O[C@@H]2[C@@H](O)[C@@H](O)[C@H](O[C@@H]2O)CO)CO)[C@H]3O[C@@H]([C@@H](O)[C@H](O)[C@H]3NC(=O)C)CO '
               'NAME: '
               'N-[(2R,3R,4R,5S,6R)-2-[(2R,3R,4S,5S,6R)-4,5-Dihydroxy-6-(hydroxymethyl)-2-[(2S,3R,4S,5R,6R)-2,4,5-trihydroxy-6-(hydroxymethyl)oxan-3-yl]oxyoxan-3-yl]oxy-4,5-dihydroxy-6-(hydroxymethyl)oxan-3-yl]acetamide '
               'REASON: MISSED Sugar rings detected but they only constitute '
               '48.6% of heavy atoms; likely a glycoside rather than an '
               'oligosaccharide.\n'
               ' * SMILES: '
               'O([C@H]1[C@H](O[C@@H](O)[C@H](O)[C@H]1O)CO[C@@H]2O[C@@H]([C@@H](O)[C@H](O)[C@H]2NC(=O)C)CO)[C@@H]3O[C@@H]([C@@H](O)[C@H](O)[C@H]3NC(=O)C)CO '
               'NAME: '
               'N-[(2R,3R,4R,5S,6R)-2-[[(2R,3R,4R,5R,6R)-3-[(2S,3R,4R,5S,6R)-3-Acetamido-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-4,5,6-trihydroxyoxan-2-yl]methoxy]-4,5-dihydroxy-6-(hydroxymethyl)oxan-3-yl]acetamide '
               'REASON: MISSED Candidate sugar rings are detected but they are '
               'not all connected via glycosidic bonds.\n'
               ' * SMILES: '
               'ClC1=C(O)C(=C(C)C=C1O)C(=O)O[C@H]2[C@H](O[C@@H]3O[C@H]([C@H](OC)[C@](C3)([N+](=O)[O-])C)C)C[C@H](O[C@H]4[C@H](O)C[C@@]5(O[C@@]6([C@H](O)[C@H](O[C@H]7[C@@H](OC)[C@H](O[C@H]([C@@H]7O)O[C@H]8[C@H](O)[C@H](OC)[C@H](O[C@@H]9OC[C@@H]%10O[C@]%11(O[C@H]%10[C@H]9O)OC[C@@H](OC(=O)C%12=C(O)C=C(O)C=C%12C)[C@H]%13[C@H]%11OCO%13)O[C@@H]8COC)C)O[C@@H]([C@H]6O5)C)C)O[C@@H]4C)O[C@@H]2C '
               'NAME: Sch 58769 REASON: MISSED Sugar rings detected but they '
               'only constitute 44.0% of heavy atoms; likely a glycoside '
               'rather than an oligosaccharide.\n'
               ' * SMILES: '
               'O([C@H]1[C@@H](O)[C@H](O)[C@H](OC1O)CO[C@H]2O[C@@H]([C@@H](O)[C@H](O)[C@@H]2O)CO)[C@H]3O[C@@H]([C@@H](O)[C@H](O)[C@@H]3O)CO '
               'NAME: alpha-D-Manp-(1->2)-[alpha-D-Manp-(1->6)]-D-Manp REASON: '
               'MISSED Candidate sugar rings are detected but they are not all '
               'connected via glycosidic bonds.\n'
               ' * SMILES: '
               'O([C@H]1[C@H](O)[C@H](O[C@@H](O[C@@H]([C@H](O)[C@@H](O)CO)[C@H](O)CO)[C@@H]1O)CO)[C@@H]2O[C@@H]([C@@H](O[C@@H]3O[C@@H]([C@@H](O)[C@H](O)[C@H]3O)CO)[C@H](O)[C@H]2O)CO '
               'NAME: '
               '(2S,3R,4R,5R)-4-[(2S,3R,4S,5R,6R)-4-[(2S,3R,4R,5S,6R)-3,4-Dihydroxy-6-(hydroxymethyl)-5-[(2S,3R,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-3,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyhexane-1,2,3,5,6-pentol '
               'REASON: MISSED Sugar rings detected but they only constitute '
               '40.0% of heavy atoms; likely a glycoside rather than an '
               'oligosaccharide.\n'
               ' * SMILES: '
               'O([C@H]1[C@H](O)[C@@H](O)[C@H](O[C@@H]1CO)O[C@H]2[C@H](O)[C@@H](O)[C@H](O[C@@H]2CO)OC[C@H]3O[C@H](O[C@H]4[C@H](O)[C@@H](O)[C@H](O[C@@H]4CO)O[C@H]5[C@H](O)[C@@H](O)C(O[C@@H]5CO)O)[C@H](O)[C@@H](O)[C@@H]3O)[C@H]6O[C@@H]([C@@H](O[C@H]7O[C@@H]([C@@H](O)[C@H](O)[C@H]7O)CO[C@H]8O[C@@H]([C@@H](O)[C@H](O)[C@H]8O)CO)[C@H](O)[C@H]6O)CO '
               'NAME: '
               '(2S,3R,4S,5S,6R)-2-[[(2R,3S,4S,5R,6R)-6-[(2R,3S,4R,5R,6R)-6-[(2R,3S,4R,5R,6R)-6-[(2R,3S,4R,5R,6S)-6-[[(2R,3S,4S,5R,6R)-6-[(2R,3S,4R,5R,6R)-4,5-Dihydroxy-2-(hydroxymethyl)-6-[(2R,3S,4R,5R)-4,5,6-trihydroxy-2-(hydroxymethyl)oxan-3-yl]oxyoxan-3-yl]oxy-3,4,5-trihydroxyoxan-2-yl]methoxy]-4,5-dihydroxy-2-(hydroxymethyl)oxan-3-yl]oxy-4,5-dihydroxy-2-(hydroxymethyl)oxan-3-yl]oxy-4,5-dihydroxy-2-(hydroxymethyl)oxan-3-yl]oxy-3,4,5-trihydroxyoxan-2-yl]methoxy]-6-(hydroxymethyl)oxane-3,4,5-triol '
               'REASON: MISSED Candidate sugar rings are detected but they are '
               'not all connected via glycosidic bonds.\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'O=C(N1[C@H](CCC1)C(O)=O)[C@@H](NC(=O)[C@@H](N)CC(O)=O)CCC(=O)N',
                                     'name': 'Asp-Gln-Pro',
                                     'reason': 'Fewer than 2 candidate sugar '
                                               'rings detected (found 0).'},
                                 {   'smiles': 'O1C=2C(C(O)=C(CC3=C(O)C=4C(OC3=O)=CC=CC4C)C1=O)=C(C=CC2)C',
                                     'name': 'Gerberinol',
                                     'reason': 'Fewer than 2 candidate sugar '
                                               'rings detected (found 0).'},
                                 {   'smiles': 'O=C(O)/C(=C/[C@H]1C=C(CC[C@@H]1C(C)C)CO)/COC(=O)C',
                                     'name': '3-acetylgliocladic acid',
                                     'reason': 'Fewer than 2 candidate sugar '
                                               'rings detected (found 0).'},
                                 {   'smiles': 'O=C(CCCCCCCCC)C=1C=CC(=NC1)CCCCCCCCC',
                                     'name': '1-(6-Nonylpyridin-3-yl)decan-1-one',
                                     'reason': 'Fewer than 2 candidate sugar '
                                               'rings detected (found 0).'},
                                 {   'smiles': 'CCC(=O)O[C@H]1[C@H](C)O[C@H](C[C@@]1(C)O)O[C@@H]1[C@@H](C)O[C@@H](O[C@H]2[C@@H](CC=O)C[C@@H](C)[C@@H](O)\\C=C\\C=C\\C[C@@H](C)OC(=O)C[C@@H](O)[C@@H]2OC)[C@H](O)[C@H]1N(C)C',
                                     'name': 'Leucomycin A7',
                                     'reason': 'Fewer than 2 candidate sugar '
                                               'rings detected (found 0).'},
                                 {   'smiles': 'C[C@H]1O[C@H](C[C@@H](O)[C@@H]1O)c1ccc2C(=O)C3=C([C@H](O)C[C@]4(O)C[C@@](C)(O)CC(=O)[C@]34O)C(=O)c2c1O',
                                     'name': 'Urdamycinone F',
                                     'reason': 'Fewer than 2 candidate sugar '
                                               'rings detected (found 1).'},
                                 {   'smiles': 'CC(C)=CCC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\COP([O-])(=O)OP([O-])([O-])=O',
                                     'name': 'all-trans-dodecaprenyl '
                                             'diphosphate(3-)',
                                     'reason': 'Fewer than 2 candidate sugar '
                                               'rings detected (found 0).'},
                                 {   'smiles': '[O-][N+](=O)N1CN(CN(CN(C1)[N+]([O-])=O)[N+]([O-])=O)[N+]([O-])=O',
                                     'name': 'octogen',
                                     'reason': 'Fewer than 2 candidate sugar '
                                               'rings detected (found 0).'},
                                 {   'smiles': 'CC(=O)NCCC[NH2+]CCCC[NH2+]CCCNC(C)=O',
                                     'name': 'N(1),N(12)-diacetylsperminium(2+)',
                                     'reason': 'Fewer than 2 candidate sugar '
                                               'rings detected (found 0).'},
                                 {   'smiles': 'C[C@@H]([C@H]1CC[C@H]2[C@H](CCc3cc(O)ccc3C)C(=O)CC[C@]12C)C(O)=O',
                                     'name': '3-hydroxy-9-oxo-9,10-seco-23,24-bisnorchola-1,3,5(10)-trien-22-oic '
                                             'acid',
                                     'reason': 'Fewer than 2 candidate sugar '
                                               'rings detected (found 0).'}],
    'sample_false_negatives': [   {   'smiles': 'O1[C@@H](O[C@H]2[C@@H](O)[C@H](O[C@H](O)[C@@H]2O)CO)[C@H](NC(=O)C)[C@@H](O[C@@H]3O[C@@H]([C@H](O)[C@H](O)[C@H]3O)CO)[C@@H](O)[C@H]1CO[C@@H]4O[C@@H]([C@@H](O)[C@H](O)[C@H]4NC(=O)C)CO',
                                      'name': 'N-[(2R,3R,4R,5S,6R)-2-[[(2R,3R,4R,5R,6S)-5-Acetamido-3-hydroxy-6-[(2S,3R,4S,5S,6R)-2,3,5-trihydroxy-6-(hydroxymethyl)oxan-4-yl]oxy-4-[(2R,3R,4S,5R,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]methoxy]-4,5-dihydroxy-6-(hydroxymethyl)oxan-3-yl]acetamide',
                                      'reason': 'Candidate sugar rings are '
                                                'detected but they are not all '
                                                'connected via glycosidic '
                                                'bonds.'},
                                  {   'smiles': 'O1[C@@H]([C@@H](O)[C@H](O[C@@H]2O[C@@H]([C@@H](O)[C@H](O)[C@H]2O)CO)[C@@H](O)[C@@H]1OC[C@H]3O[C@@H](OC[C@H]4O[C@@H](O)[C@H](O)[C@@H](O)[C@@H]4O)[C@H](O)[C@@H](O)[C@@H]3O)CO[C@@H]5O[C@@H]([C@@H](O)[C@H](O[C@@H]6O[C@@H]([C@@H](O)[C@H](O)[C@H]6O)CO)[C@H]5O)CO[C@@H]7O[C@@H]([C@@H](O)[C@H](O)[C@H]7O)CO',
                                      'name': '(2R,3R,4S,5S,6R)-6-[[(2R,3R,4S,5S,6R)-6-[[(2R,3R,4S,5R,6R)-6-[[(2R,3R,4S,5R,6R)-3,5-Dihydroxy-4-[(2R,3R,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-6-[[(2R,3R,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxymethyl]oxan-2-yl]oxymethyl]-3,5-dihydroxy-4-[(2R,3R,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxymethyl]-3,4,5-trihydroxyoxan-2-yl]oxymethyl]oxane-2,3,4,5-tetrol',
                                      'reason': 'Candidate sugar rings are '
                                                'detected but they are not all '
                                                'connected via glycosidic '
                                                'bonds.'},
                                  {   'smiles': 'O([C@H]1[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]1CO)OC[C@@H](O)[C@H](O)[C@H](O[C@@H]2O[C@@H]([C@H](O)[C@H](O)[C@H]2O)CO)[C@@H](NC(=O)C)CO)[C@@H]3O[C@@H]([C@H](O)[C@H](O[C@@H]4O[C@@H]([C@H](O)[C@H](O)[C@H]4O)CO)[C@H]3O)CO',
                                      'name': 'N-[(2R,3R,4R,5S,6R)-2-[(2R,3S,4R,5S)-5-Acetamido-2,3,6-trihydroxy-4-[(2S,3R,4S,5R,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyhexoxy]-5-[(2S,3R,4S,5S,6R)-3,5-dihydroxy-6-(hydroxymethyl)-4-[(2S,3R,4S,5R,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-3-yl]acetamide',
                                      'reason': 'Candidate sugar rings are '
                                                'detected but they are not all '
                                                'connected via glycosidic '
                                                'bonds.'},
                                  {   'smiles': 'O([C@@H]1[C@@H](O)[C@H](O[C@H]2[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]2CO)OC[C@@H](O)[C@H](O)[C@H](O[C@@H]3O[C@@H]([C@H](O)[C@H](O)[C@H]3O)CO)[C@@H](NC(=O)C)CO)O[C@@H]([C@@H]1O)CO)[C@@H]4O[C@@H]([C@@H](O)[C@H](O[C@@H]5O[C@@H]([C@H](O)[C@H](O)[C@H]5O)CO)[C@H]4NC(=O)C)CO',
                                      'name': 'N-[(2R,3R,4R,5S,6R)-5-[(2S,3R,4S,5S,6R)-4-[(2S,3R,4R,5S,6R)-3-Acetamido-5-hydroxy-6-(hydroxymethyl)-4-[(2R,3R,4S,5R,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-3,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-2-[(2R,3S,4R,5S)-5-acetamido-2,3,6-trihydroxy-4-[(2R,3R,4S,5R,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyhexoxy]-4-hydroxy-6-(hydroxymethyl)oxan-3-yl]acetamide',
                                      'reason': 'Candidate sugar rings are '
                                                'detected but they are not all '
                                                'connected via glycosidic '
                                                'bonds.'},
                                  {   'smiles': 'O([C@@H]1[C@@H](O)[C@H](O)[C@H](O[C@@H]1O[C@@H]2[C@@H](O)[C@@H](O)[C@H](O[C@@H]2O)CO)CO)[C@H]3O[C@@H]([C@@H](O)[C@H](O)[C@H]3NC(=O)C)CO',
                                      'name': 'N-[(2R,3R,4R,5S,6R)-2-[(2R,3R,4S,5S,6R)-4,5-Dihydroxy-6-(hydroxymethyl)-2-[(2S,3R,4S,5R,6R)-2,4,5-trihydroxy-6-(hydroxymethyl)oxan-3-yl]oxyoxan-3-yl]oxy-4,5-dihydroxy-6-(hydroxymethyl)oxan-3-yl]acetamide',
                                      'reason': 'Sugar rings detected but they '
                                                'only constitute 48.6% of '
                                                'heavy atoms; likely a '
                                                'glycoside rather than an '
                                                'oligosaccharide.'},
                                  {   'smiles': 'O([C@H]1[C@H](O[C@@H](O)[C@H](O)[C@H]1O)CO[C@@H]2O[C@@H]([C@@H](O)[C@H](O)[C@H]2NC(=O)C)CO)[C@@H]3O[C@@H]([C@@H](O)[C@H](O)[C@H]3NC(=O)C)CO',
                                      'name': 'N-[(2R,3R,4R,5S,6R)-2-[[(2R,3R,4R,5R,6R)-3-[(2S,3R,4R,5S,6R)-3-Acetamido-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-4,5,6-trihydroxyoxan-2-yl]methoxy]-4,5-dihydroxy-6-(hydroxymethyl)oxan-3-yl]acetamide',
                                      'reason': 'Candidate sugar rings are '
                                                'detected but they are not all '
                                                'connected via glycosidic '
                                                'bonds.'},
                                  {   'smiles': 'OC[C@H]1O[C@@H](O[C@@H]2[C@@H](CO)O[C@@H](O[C@H]3[C@H](O)[C@@H](O)[C@@H](O)O[C@@H]3CO)[C@@H](O)[C@H]2O[C@H]2O[C@@H]([C@@H](O)[C@H](O)[C@H]2O)C(O)=O)[C@H](O)[C@@H](O)[C@@H]1O',
                                      'name': 'beta-D-Glcp-(1->4)-[alpha-D-GlcpA-(1->3)]-beta-D-Manp-(1->4)-alpha-D-Glcp',
                                      'reason': 'Candidate sugar rings are '
                                                'detected but they are not all '
                                                'connected via glycosidic '
                                                'bonds.'},
                                  {   'smiles': 'O([C@@H]1[C@@H](NC(=O)C)[C@@H](O[C@@H]2[C@@H](O[C@@H]3O[C@H]([C@@H](O)[C@@H](O)[C@@H]3O)C)C(O[C@@H]([C@@H]2O)CO)O)O[C@@H]([C@@H]1O)CO)[C@H]4O[C@@H]([C@@H](O)[C@H](O[C@@H]5O[C@H]([C@@H](O)[C@@H](O)[C@@H]5O)C)[C@H]4NC(=O)C)CO',
                                      'name': 'N-[(2R,3R,4R,5R,6R)-4-[(2S,3R,4R,5S,6R)-3-Acetamido-5-hydroxy-6-(hydroxymethyl)-4-[(2S,3S,4R,5S,6S)-3,4,5-trihydroxy-6-methyloxan-2-yl]oxyoxan-2-yl]oxy-2-[(3R,4S,5S,6R)-2,5-dihydroxy-6-(hydroxymethyl)-3-[(2S,3S,4R,5S,6S)-3,4,5-trihydroxy-6-methyloxan-2-yl]oxyoxan-4-yl]oxy-5-hydroxy-6-(hydroxymethyl)oxan-3-yl]acetamide',
                                      'reason': 'Candidate sugar rings are '
                                                'detected but they are not all '
                                                'connected via glycosidic '
                                                'bonds.'},
                                  {   'smiles': 'ClC1=C(O)C(=C(C)C=C1O)C(=O)O[C@H]2[C@H](O[C@@H]3O[C@H]([C@H](OC)[C@](C3)([N+](=O)[O-])C)C)C[C@H](O[C@H]4[C@H](O)C[C@@]5(O[C@@]6([C@H](O)[C@H](O[C@H]7[C@@H](OC)[C@H](O[C@H]([C@@H]7O)O[C@H]8[C@H](O)[C@H](OC)[C@H](O[C@@H]9OC[C@@H]%10O[C@]%11(O[C@H]%10[C@H]9O)OC[C@@H](OC(=O)C%12=C(O)C=C(O)C=C%12C)[C@H]%13[C@H]%11OCO%13)O[C@@H]8COC)C)O[C@@H]([C@H]6O5)C)C)O[C@@H]4C)O[C@@H]2C',
                                      'name': 'Sch 58769',
                                      'reason': 'Fewer than 2 candidate sugar '
                                                'rings detected (found 0).'},
                                  {   'smiles': 'O([C@H]1[C@@H](O)[C@H](O)[C@H](OC1O)CO[C@H]2O[C@@H]([C@@H](O)[C@H](O)[C@@H]2O)CO)[C@H]3O[C@@H]([C@@H](O)[C@H](O)[C@@H]3O)CO',
                                      'name': 'alpha-D-Manp-(1->2)-[alpha-D-Manp-(1->6)]-D-Manp',
                                      'reason': 'Candidate sugar rings are '
                                                'detected but they are not all '
                                                'connected via glycosidic '
                                                'bonds.'}],
    'attempt': 2,
    'reasoning': 'Below is one possible improved solution. In this version we '
                 'still begin by “mining” the molecule for candidate sugar '
                 'rings but add two extra checks: (1) each candidate ring must '
                 'be saturated—that is, every bond between ring atoms must be '
                 'a single bond (this helps weed out aromatic or unsaturated '
                 'rings that mistakenly match the basic criteria) and (2) at '
                 'least a couple of the ring carbons must have an exocyclic '
                 '–OH substituent (a typical signature of sugar rings). In '
                 'addition the bridging check now only “counts” an oxygen if '
                 'it is a candidate glycosidic linker (i.e. if its degree is '
                 '2, so that it is not a longer substituent). Finally, we '
                 'require that at least two sugar rings are found, that they '
                 'are all connected (directly or via a bridging oxygen) and '
                 'that the atoms in these rings account for at least 50% of '
                 'the molecule’s heavy atoms. (Keep in mind that any heuristic '
                 'is not perfect and some false positives/negatives may still '
                 'arise.) \n'
                 '\n'
                 'Below is the complete code in one Python code block:\n'
                 '\n'
                 '------------------------------------------------',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 690,
    'num_false_positives': 149,
    'num_true_negatives': 139830,
    'num_false_negatives': 1631,
    'num_negatives': None,
    'precision': 0.8224076281287247,
    'recall': 0.2972856527358897,
    'f1': 0.4367088607594936,
    'accuracy': 0.9874912157413914,
    'negative_predictive_value': 0.9884703204416765}