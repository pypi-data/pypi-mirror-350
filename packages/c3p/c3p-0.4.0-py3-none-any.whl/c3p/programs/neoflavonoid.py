"""
Classifies: CHEBI:71971 neoflavonoid
"""
"""
Classifies: Neoflavonoid
Definition: Any 1-benzopyran with an aryl substituent at position 4.
A neoflavonoid is defined here as a bicyclic system consisting of:
  - a 6-membered heterocycle (the “pyran” ring) that in its “classic” form contains exactly one oxygen,
    but which in oxidized variants may have lost the ring oxygen and instead show two exocyclic carbonyl (C=O) substituents,
  - fused to a 6-membered benzene ring (all aromatic carbons),
with fusion occurring via exactly 2 atoms. Furthermore, by “numbering” the heterocycle starting from the heteroatom
(or, if none, from a ring carbon bearing a carbonyl), the two fused atoms should be consecutive – so that the next (4–)
position bears an external aryl substituent.
"""

from rdkit import Chem

def order_ring(mol, ring, start_idx, next_idx):
    """
    Given a ring (as a set of atom indices) known to be cyclic,
    return an ordered list of the atoms starting at start_idx, next_idx and following the cycle.
    """
    order = [start_idx, next_idx]
    current = next_idx
    previous = start_idx
    while len(order) < len(ring):
        nbrs = [nbr.GetIdx() for nbr in mol.GetAtomWithIdx(current).GetNeighbors() 
                if nbr.GetIdx() in ring and nbr.GetIdx() != previous]
        if not nbrs:
            break
        next_atom = nbrs[0]
        order.append(next_atom)
        previous, current = current, next_atom
    return order

def is_neoflavonoid(smiles: str):
    """
    Determines if a molecule is a neoflavonoid.
    Strategy:
      1. Parse the molecule and get all 6-membered rings.
      2. Identify:
         - Candidate heterocycles: rings that either contain exactly one oxygen (classic pyran)
           or (if no oxygen is present) have at least 2 ring carbons bearing exocyclic carbonyl groups.
         - Candidate benzene rings: aromatic 6-membered rings composed entirely of carbons.
      3. For each candidate heterocycle and benzene ring pair that share exactly 2 atoms
         (and neither fused atom is oxygen), try to order (rotate) the ring so that the two fused atoms occur consecutively.
         If found, identify the next ring position (the candidate pos4).
      4. At the candidate pos4, verify that at least one neighbor not in the heterocycle is an aromatic carbon,
         and that this neighbor is part of a benzene ring that is fully external (disjoint from the heterocycle).
    Args:
       smiles (str): SMILES representation of the molecule.
    Returns:
       (bool, str): Tuple of classification result and explanation.
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
        
    ring_info = mol.GetRingInfo()
    all_rings = ring_info.AtomRings()  # list of tuples of atom indices

    candidate_heterocycles = []  # list of tuples: (set(ring), start_atom)
    candidate_benzenes = []      # list of sets of atom indices

    # Identify candidate benzene rings and heterocycles among all 6-membered rings.
    for ring in all_rings:
        if len(ring) != 6:
            continue
        atoms = [mol.GetAtomWithIdx(idx) for idx in ring]
        # Benzene: All atoms must be carbon and aromatic.
        if all(a.GetAtomicNum() == 6 and a.GetIsAromatic() for a in atoms):
            candidate_benzenes.append(set(ring))
        # Check heterocycle candidate:
        # Option A: “Classic” pyran case: exactly one oxygen in the ring.
        o_count = sum(1 for a in atoms if a.GetAtomicNum() == 8)
        if o_count == 1:
            # Use the single oxygen as the start atom.
            for idx in ring:
                if mol.GetAtomWithIdx(idx).GetAtomicNum() == 8:
                    candidate_heterocycles.append((set(ring), idx))
                    break
        # Option B: Oxidized variant: no oxygen in the ring but at least two ring carbons that bear an exocyclic carbonyl.
        elif o_count == 0:
            carbonyl_sites = []
            for idx in ring:
                atom = mol.GetAtomWithIdx(idx)
                if atom.GetAtomicNum() != 6:
                    continue
                for nbr in atom.GetNeighbors():
                    if nbr.GetIdx() in ring:
                        continue
                    bond = mol.GetBondBetweenAtoms(atom.GetIdx(), nbr.GetIdx())
                    if (nbr.GetAtomicNum() == 8 and bond is not None and 
                        bond.GetBondTypeAsDouble() == 2.0):
                        carbonyl_sites.append(idx)
                        break
            if len(set(carbonyl_sites)) >= 2:
                # Pick one of the carbonyl-bearing carbons as the start atom.
                start_atom = list(set(carbonyl_sites))[0]
                candidate_heterocycles.append((set(ring), start_atom))
                
    if not candidate_heterocycles:
        return False, "No 6-membered heterocycle candidate found (neither classic pyran nor oxidized variant detected)"
    if not candidate_benzenes:
        return False, "No 6-membered aromatic benzene ring found"
        
    # For checking external aryl substituents,
    # we define a helper that verifies that a neighbor (attached to candidate pos4)
    # is part of a benzene ring that does not share any atoms with the heterocycle.
    def has_external_benzene(neighbor, hetero_ring):
        if not (neighbor.GetIsAromatic() and neighbor.GetAtomicNum() == 6):
            return False
        # Check if neighbor belongs to any 6-membered aromatic ring that is fully external to the heterocycle.
        for benz in candidate_benzenes:
            # The candidate benzene must contain this neighbor
            if neighbor.GetIdx() in benz:
                # Ensure the benzene ring is disjoint from the heterocycle.
                if hetero_ring.intersection(benz):
                    continue
                else:
                    return True
        return False

    # For each candidate heterocycle and benzene pair, check fusion and substituent.
    for hetero_ring, start_atom in candidate_heterocycles:
        for benz_ring in candidate_benzenes:
            shared_atoms = hetero_ring.intersection(benz_ring)
            if len(shared_atoms) != 2:
                continue  # need exactly 2 fused atoms
            # Reject if any fused atom is oxygen.
            if any(mol.GetAtomWithIdx(idx).GetAtomicNum() == 8 for idx in shared_atoms):
                continue

            # Try ordering the heterocycle.
            start_atom_obj = mol.GetAtomWithIdx(start_atom)
            ring_neighbors = [nbr.GetIdx() for nbr in start_atom_obj.GetNeighbors() if nbr.GetIdx() in hetero_ring]
            if not ring_neighbors:
                continue
            valid_order_found = False
            candidate_pos4 = None
            for nbr in ring_neighbors:
                order = order_ring(mol, hetero_ring, start_atom, nbr)
                if len(order) != 6:
                    continue
                # Because the ring is cyclic, we try every rotation.
                n = len(order)
                for i in range(n):
                    # Let fused pair be order[i] and order[(i+1)%n].
                    pair = {order[i], order[(i+1) % n]}
                    if pair == shared_atoms:
                        # Then candidate pos4 is the next atom in order.
                        candidate_pos4 = order[(i+2) % n]
                        valid_order_found = True
                        break
                if valid_order_found:
                    break
            if not valid_order_found:
                continue

            # Now, verify the candidate pos4 has an external substituent.
            pos4_atom = mol.GetAtomWithIdx(candidate_pos4)
            # Check that at least one neighbor (via a single bond) is an aromatic carbon belonging to an external benzene.
            for nbr in pos4_atom.GetNeighbors():
                if nbr.GetIdx() in hetero_ring:
                    continue
                if has_external_benzene(nbr, hetero_ring):
                    return True, ("Found neoflavonoid core: a 1-benzopyran (or oxidized variant) fused with a benzene ring "
                                  "and with an external aryl substituent attached at the 4–position.")
    return False, "No suitable candidate 1-benzopyran (or oxidized variant) with an external aryl substituent at the 4–position was identified"


# Example usage for testing:
if __name__ == "__main__":
    # Test one of the provided SMILES strings.
    test_smiles = "CC1=CC(=CC2=C1C(CC3(O2)CC(NC(=S)N3)(C)C)C4=CC=C(C=C4)OC)O"  # 7'-hydroxy-4'-(4-methoxyphenyl)-... thione
    result, reason = is_neoflavonoid(test_smiles)
    print("Is neoflavonoid?", result)
    print("Reason:", reason)


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:71971',
                          'name': 'neoflavonoid',
                          'definition': 'Any 1-benzopyran with an aryl '
                                        'substituent at position 4. The term '
                                        'was originally restricted to natural '
                                        'products, but is now also used to '
                                        'describe semi-synthetic and fully '
                                        'synthetic compounds.',
                          'parents': [   'CHEBI:26004',
                                         'CHEBI:38443',
                                         'CHEBI:72544'],
                          'xrefs': ['Wikipedia:Neoflavonoid'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 112,
                           'log_lines_of_code': 4.718498871295094,
                           'indent_by_line': [   1,
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
                                                 2,
                                                 2,
                                                 2,
                                                 1,
                                                 0,
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
                                                 2,
                                                 1,
                                                 1,
                                                 0,
                                                 1,
                                                 1,
                                                 0,
                                                 1,
                                                 1,
                                                 2,
                                                 3,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 3,
                                                 4,
                                                 5,
                                                 5,
                                                 2,
                                                 2,
                                                 3,
                                                 3,
                                                 4,
                                                 4,
                                                 5,
                                                 4,
                                                 5,
                                                 6,
                                                 5,
                                                 5,
                                                 6,
                                                 6,
                                                 6,
                                                 3,
                                                 4,
                                                 4,
                                                 4,
                                                 4,
                                                 1,
                                                 2,
                                                 1,
                                                 2,
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 3,
                                                 2,
                                                 2,
                                                 3,
                                                 3,
                                                 4,
                                                 4,
                                                 5,
                                                 4,
                                                 5,
                                                 2,
                                                 0,
                                                 1,
                                                 1,
                                                 2,
                                                 3,
                                                 3,
                                                 4,
                                                 3,
                                                 3,
                                                 4,
                                                 0,
                                                 0,
                                                 1,
                                                 0,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1],
                           'max_indent': 6,
                           'imports': ['from rdkit import Chem'],
                           'imports_count': 1,
                           'methods_called': [   'append',
                                                 'GetIsAromatic',
                                                 'GetBondTypeAsDouble',
                                                 'intersection',
                                                 'AtomRings',
                                                 'GetAtomWithIdx',
                                                 'GetNeighbors',
                                                 'GetAtomicNum',
                                                 'GetBondBetweenAtoms',
                                                 'MolFromSmiles',
                                                 'GetRingInfo',
                                                 'GetIdx'],
                           'methods_called_count': 12,
                           'smarts_strings': [],
                           'smarts_strings_count': 0,
                           'defs': [   'order_ring(mol, ring, start_idx, '
                                       'next_idx):',
                                       'has_external_benzene(neighbor, '
                                       'hetero_ring):'],
                           'defs_count': 2,
                           'returns': [   'an ordered list of the atoms '
                                          'starting at start_idx, next_idx and '
                                          'following the cycle.',
                                          'order',
                                          'False, "Invalid SMILES string"',
                                          'False, "No 6-membered heterocycle '
                                          'candidate found (neither classic '
                                          'pyran nor oxidized variant '
                                          'detected)"',
                                          'False, "No 6-membered aromatic '
                                          'benzene ring found"',
                                          'False',
                                          'True',
                                          'False',
                                          'False, "No suitable candidate '
                                          '1-benzopyran (or oxidized variant) '
                                          'with an external aryl substituent '
                                          'at the 4–position was identified"'],
                           'returns_count': 9,
                           'complexity': 6.743699774259019},
    'message': '\n'
               'Attempt failed: F1 score of 0.17549668874172186 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: '
               'CC1=CC(=CC2=C1C(CC3(O2)CC(NC(=S)N3)(C)C)C4=CC=C(C=C4)OC)O '
               'NAME: '
               "7'-hydroxy-4'-(4-methoxyphenyl)-4,4,5'-trimethyl-2-spiro[1,3-diazinane-6,2'-3,4-dihydro-2H-1-benzopyran]thione "
               'REASON: CORRECT Found neoflavonoid core: a 1-benzopyran (or '
               'oxidized variant) fused to a benzene ring with a candidate '
               'aryl substituent at the 4–position.\n'
               ' * SMILES: '
               'O1C2=C(C(O)=C(C(O)=C2/C=C/C(C)C)C(=O)CCC)C(C3=CC=CC=C3)=CC1=O '
               'NAME: '
               "6-Butyryl-5,7-dihydroxy-8-(3',3'-dimethylallyl)-4-phenylcoumarin "
               'REASON: CORRECT Found neoflavonoid core: a 1-benzopyran (or '
               'oxidized variant) fused to a benzene ring with a candidate '
               'aryl substituent at the 4–position.\n'
               ' * SMILES: '
               'S(OC=1C=C(C=2C3=C(OC(=O)C2)C4=C(OC(C=C4)(C)C)C=C3O)C=CC1)(O)(=O)=O '
               'NAME: '
               '3-(5-hydroxy-8,8-dimethyl-2-oxo-2h,8h-pyrano[2,3-f]chromen-4-yl)phenyl '
               'hydrogen sulfate REASON: CORRECT Found neoflavonoid core: a '
               '1-benzopyran (or oxidized variant) fused to a benzene ring '
               'with a candidate aryl substituent at the 4–position.\n'
               ' * SMILES: '
               'O1C(CC(C2=C1C=C(O)C3=C2N(C4=C(C3=O)C=CC=C4O)C)C5=C6OC(C=CC6=C7N(C8=C(C(=O)C7=C5O)C=CC=C8O)C)(C)C)(C)C '
               'NAME: Bis(5-hydroxynoracronycine) REASON: CORRECT Found '
               'neoflavonoid core: a 1-benzopyran (or oxidized variant) fused '
               'to a benzene ring with a candidate aryl substituent at the '
               '4–position.\n'
               ' * SMILES: '
               'ClC1=C(O)C(=C(C(=O)OC)C=C1OC)C(=O)C2=C(O)C(C=3C4=C(OC(C3)(C)C)C(=CC(=C4)O)CC=C(C)C)=C(C)C=C2O '
               'NAME: Pestaloficiol U REASON: CORRECT Found neoflavonoid core: '
               'a 1-benzopyran (or oxidized variant) fused to a benzene ring '
               'with a candidate aryl substituent at the 4–position.\n'
               ' * SMILES: '
               'CC[C@H](C)C(=O)c1c(O)c(CC=C(C)C)c2oc(=O)cc(-c3ccccc3)c2c1O '
               'NAME: Mammea A/AB, (-)- REASON: CORRECT Found neoflavonoid '
               'core: a 1-benzopyran (or oxidized variant) fused to a benzene '
               'ring with a candidate aryl substituent at the 4–position.\n'
               ' * SMILES: O1C=2C(C(C3=CC=CC=C3)=CC1=O)=C(O)C=C(O)C2 NAME: '
               'Serratin REASON: CORRECT Found neoflavonoid core: a '
               '1-benzopyran (or oxidized variant) fused to a benzene ring '
               'with a candidate aryl substituent at the 4–position.\n'
               ' * SMILES: '
               'O1C(CC=2C1=C(C(O)=C3C2OC(=O)C=C3C4=CC=CC=C4)C(=O)C(C)C)C(O)(C)C '
               'NAME: '
               '1,2-Dihydro-5-hydroxy-2-(1-hydroxy-1-methylethyl)-4-(isobutyryl)-6-phenylfurano[2,3-h][1]benzopyran-8-one '
               'REASON: CORRECT Found neoflavonoid core: a 1-benzopyran (or '
               'oxidized variant) fused to a benzene ring with a candidate '
               'aryl substituent at the 4–position.\n'
               ' * SMILES: '
               'O1[C@]2(O)[C@@]([C@H](C3=C1C(=C(O)C4=C3O[C@@H](CC4=O)C5=CC=CC=C5)C)C6=CC=CC=C6)(C(=O)C(C(=O)C2(C)C)(C)C)[H] '
               'NAME: Leucadenone B REASON: CORRECT Found neoflavonoid core: a '
               '1-benzopyran (or oxidized variant) fused to a benzene ring '
               'with a candidate aryl substituent at the 4–position.\n'
               ' * SMILES: '
               'O=C(C1=C(O)C(=CC=C1O)[C@@H]2C3=C(O[C@@H](C2)C)C=CC=C3OC)CCC '
               'NAME: Nodulisporin H REASON: CORRECT Found neoflavonoid core: '
               'a 1-benzopyran (or oxidized variant) fused to a benzene ring '
               'with a candidate aryl substituent at the 4–position.\n'
               ' * SMILES: '
               'CC(C)CC(=O)c1c(O)c(CC=C(C)C)c2oc(=O)cc(-c3ccccc3)c2c1O NAME: '
               'Mammea A/AA REASON: CORRECT Found neoflavonoid core: a '
               '1-benzopyran (or oxidized variant) fused to a benzene ring '
               'with a candidate aryl substituent at the 4–position.\n'
               ' * SMILES: '
               'O1C2=C(C(C3=CC(OC)=C(OC)C=C3)=CC1=O)C(OC)=CC(OC)=C2O NAME: '
               "8-Hydroxy-5,7,3',4'-tetramethoxy-4-phenylcoumarin REASON: "
               'CORRECT Found neoflavonoid core: a 1-benzopyran (or oxidized '
               'variant) fused to a benzene ring with a candidate aryl '
               'substituent at the 4–position.\n'
               ' * SMILES: COC1=C(C=C2C(=CC(=O)OC2=C1OC)C3=CC=CC=C3)O NAME: '
               '6-hydroxy-7,8-dimethoxy-4-phenyl-1-benzopyran-2-one REASON: '
               'CORRECT Found neoflavonoid core: a 1-benzopyran (or oxidized '
               'variant) fused to a benzene ring with a candidate aryl '
               'substituent at the 4–position.\n'
               ' * SMILES: COc1ccc(cc1O)-c1cc(=O)oc2cc(OC)c(O)cc12 NAME: '
               'melannein REASON: CORRECT Found neoflavonoid core: a '
               '1-benzopyran (or oxidized variant) fused to a benzene ring '
               'with a candidate aryl substituent at the 4–position.\n'
               ' * SMILES: O1C2=C(C(C3=CC(O)=C(OC)C=C3)=CC1=O)C(OC)=CC(OC)=C2 '
               "NAME: 3'-Hydroxy-5,7,4'-trimethoxy-4-phenylcoumarin REASON: "
               'CORRECT Found neoflavonoid core: a 1-benzopyran (or oxidized '
               'variant) fused to a benzene ring with a candidate aryl '
               'substituent at the 4–position.\n'
               ' * SMILES: '
               'O1C(CC=2C1=C(C(O)=C3C2OC(=O)C=C3C4=CC=CC=C4)C(=O)CCC)C(O)(C)C '
               'NAME: Mammea A/AC cyclo F REASON: CORRECT Found neoflavonoid '
               'core: a 1-benzopyran (or oxidized variant) fused to a benzene '
               'ring with a candidate aryl substituent at the 4–position.\n'
               ' * SMILES: '
               'O1[C@H]([C@H](C(=O)C=2C1=C3C(OC(=O)C=C3C4=CC=CC=C4)=C5C2OC(C=C5)(C)C)C)C '
               'NAME: Tomentolide A REASON: CORRECT Found neoflavonoid core: a '
               '1-benzopyran (or oxidized variant) fused to a benzene ring '
               'with a candidate aryl substituent at the 4–position.\n'
               ' * SMILES: '
               'O1C(C=CC=2C1=C(C(O)=C3C2OC(=O)C=C3C4=CC=CC=C4)C(=O)CCC)(C)C '
               'NAME: 6-Butyryl-5-hydroxy-4-phenylseselin REASON: CORRECT '
               'Found neoflavonoid core: a 1-benzopyran (or oxidized variant) '
               'fused to a benzene ring with a candidate aryl substituent at '
               'the 4–position.\n'
               ' * SMILES: '
               'O1C(CC=2C1=C(C(O)=C3C2OC(=O)C=C3C4=CC=CC=C4)C(=O)CC(C)C)C(O)(C)C '
               'NAME: Cyclomammeisin REASON: CORRECT Found neoflavonoid core: '
               'a 1-benzopyran (or oxidized variant) fused to a benzene ring '
               'with a candidate aryl substituent at the 4–position.\n'
               ' * SMILES: '
               'CC(C)CC(=O)c1c(O)c(CC=C(C)C)c(O)c2c(cc(=O)oc12)-c1ccccc1 NAME: '
               'Mammea A/BA REASON: CORRECT Found neoflavonoid core: a '
               '1-benzopyran (or oxidized variant) fused to a benzene ring '
               'with a candidate aryl substituent at the 4–position.\n'
               ' * SMILES: '
               'O1C(C(C(=O)C2=C1C3=C(OC(C=C3)(C)C)C4=C2OC(=O)C=C4C5=CC=CC=C5)C)C '
               'NAME: cis-and-trans-Inophyllolide REASON: CORRECT Found '
               'neoflavonoid core: a 1-benzopyran (or oxidized variant) fused '
               'to a benzene ring with a candidate aryl substituent at the '
               '4–position.\n'
               ' * SMILES: O=C1OC2=C(O)C=C(C)C=C2C(=C1O)C3=CC=C(O)C=C3 NAME: '
               '3,8-dihydroxy-4-(4-hydroxyphenyl)-6-methylcoumarin REASON: '
               'CORRECT Found neoflavonoid core: a 1-benzopyran (or oxidized '
               'variant) fused to a benzene ring with a candidate aryl '
               'substituent at the 4–position.\n'
               ' * SMILES: '
               'O=C(OC)C1=C(C(O)=CC(=C1)OC)C(=O)C2=C(O)C(C=3C4=C(OC(C3)(C)C)C(=CC(=C4)O)CC=C(C)C)=C(C)C=C2O '
               'NAME: Pestaloficiol L REASON: CORRECT Found neoflavonoid core: '
               'a 1-benzopyran (or oxidized variant) fused to a benzene ring '
               'with a candidate aryl substituent at the 4–position.\n'
               ' * SMILES: '
               'O1[C@]2(O)[C@]([C@@H](C3=C1C(=C(O)C4=C3O[C@@H](CC4=O)C5=CC=CC=C5)C)C6=CC=CC=C6)(C(=O)C(C(=O)C2(C)C)(C)C)[H] '
               'NAME: Leucadenone C REASON: CORRECT Found neoflavonoid core: a '
               '1-benzopyran (or oxidized variant) fused to a benzene ring '
               'with a candidate aryl substituent at the 4–position.\n'
               ' * SMILES: '
               'O1C2=C(C(O)=C(C(O)=C2CC=C(C)C)C(=O)C(C)C)C(C3=CC=CC=C3)=CC1=O '
               'NAME: Mesuol REASON: CORRECT Found neoflavonoid core: a '
               '1-benzopyran (or oxidized variant) fused to a benzene ring '
               'with a candidate aryl substituent at the 4–position.\n'
               'False positives: SMILES: '
               'C1=CC(=CC(=C1)O)N2C(=O)C3=C4C(=CC=C5C4=C(C=C3)C(=O)N(C5=O)C6=CC(=CC=C6)O)C2=O '
               'NAME: LSM-16285 REASON: WRONGLY CLASSIFIED Found neoflavonoid '
               'core: a 1-benzopyran (or oxidized variant) fused to a benzene '
               'ring with a candidate aryl substituent at the 4–position.\n'
               ' * SMILES: ClC1=C(OC)C(O)=C2OC(=O)C3=C(C2=C1C)C=C(OC)C=C3O '
               'NAME: Penicilliumolide D REASON: WRONGLY CLASSIFIED Found '
               'neoflavonoid core: a 1-benzopyran (or oxidized variant) fused '
               'to a benzene ring with a candidate aryl substituent at the '
               '4–position.\n'
               ' * SMILES: '
               'O=C1C2=C(O)C(OC)=C(OC)C=3C2=C(C(O)=C(CC=C(C)C)C3C)C([C@@]1(O)CC(=O)C)=O '
               'NAME: Flaviphenalenone A REASON: WRONGLY CLASSIFIED Found '
               'neoflavonoid core: a 1-benzopyran (or oxidized variant) fused '
               'to a benzene ring with a candidate aryl substituent at the '
               '4–position.\n'
               ' * SMILES: '
               'O1C([C@H](O)[C@H](O)C(O)[C@@H]1OC=2C=3C(C4=CC=C(O)C=C4)=CC(OC3C=C(OC)C2)=O)CO '
               "NAME: 5,4'-Dihydroxy-7-methoxy-4-phenylcoumarin "
               '5-O-galactoside REASON: WRONGLY CLASSIFIED Found neoflavonoid '
               'core: a 1-benzopyran (or oxidized variant) fused to a benzene '
               'ring with a candidate aryl substituent at the 4–position.\n'
               ' * SMILES: '
               '[Cl-].CN(C)c1ccc2c(-c3ccccc3)c3ccc(cc3oc2c1)=[N+](C)C NAME: '
               'tetramethylrosamine chloride REASON: WRONGLY CLASSIFIED Found '
               'neoflavonoid core: a 1-benzopyran (or oxidized variant) fused '
               'to a benzene ring with a candidate aryl substituent at the '
               '4–position.\n'
               ' * SMILES: '
               '[Cl-].CN(C)c1ccc2c(-c3ccc(CCl)cc3)c3ccc(cc3oc2c1)=[N+](C)C '
               'NAME: mitoTracker Orange REASON: WRONGLY CLASSIFIED Found '
               'neoflavonoid core: a 1-benzopyran (or oxidized variant) fused '
               'to a benzene ring with a candidate aryl substituent at the '
               '4–position.\n'
               ' * SMILES: '
               'ClC1=C2OC([C@H]3CC=4C([C@@H]3C2=C(OC)C(=C1C)Cl)=C(C(O)=CC4O)C=O)(C)C '
               'NAME: Pestalachloride C REASON: WRONGLY CLASSIFIED Found '
               'neoflavonoid core: a 1-benzopyran (or oxidized variant) fused '
               'to a benzene ring with a candidate aryl substituent at the '
               '4–position.\n'
               ' * SMILES: '
               'CNc1ccc(c(C(O)=O)c1N)-c1c2cc(F)c(O)cc2oc2cc(=O)c(F)cc12 NAME: '
               'DAF-FM dye REASON: WRONGLY CLASSIFIED Found neoflavonoid core: '
               'a 1-benzopyran (or oxidized variant) fused to a benzene ring '
               'with a candidate aryl substituent at the 4–position.\n'
               ' * SMILES: '
               'O=C1C=2C3=C(C(O)=CC(=C3C(O)=CC2O)C)C([C@@]1(O)CC(=O)C)=O NAME: '
               '9-demethyl FR-901235 REASON: WRONGLY CLASSIFIED Found '
               'neoflavonoid core: a 1-benzopyran (or oxidized variant) fused '
               'to a benzene ring with a candidate aryl substituent at the '
               '4–position.\n'
               ' * SMILES: '
               'O[C@H]1[C@H](Oc2cc(O)cc(O)c2[C@H]1c1c(O)cc(O)c2C[C@@H](OC(=O)c3cc(O)c(O)c(O)c3)[C@H](Oc12)c1ccc(O)c(O)c1)c1ccc(O)c(O)c1 '
               "NAME: (-)-epicatechin-(4alpha->8)-(-)-epicatechin-3'-O-gallate "
               'REASON: WRONGLY CLASSIFIED Found neoflavonoid core: a '
               '1-benzopyran (or oxidized variant) fused to a benzene ring '
               'with a candidate aryl substituent at the 4–position.\n'
               ' * SMILES: '
               'O[C@H]1Cc2c(O)cc(O)c([C@H]3[C@H](O)[C@H](Oc4cc(O)ccc34)c3ccc(O)c(O)c3)c2O[C@@H]1c1ccc(O)c(O)c1 '
               'NAME: fisetinidol-(4alpha,8)-catechin REASON: WRONGLY '
               'CLASSIFIED Found neoflavonoid core: a 1-benzopyran (or '
               'oxidized variant) fused to a benzene ring with a candidate '
               'aryl substituent at the 4–position.\n'
               ' * SMILES: '
               'O1C2=C(C(CC1=O)C3=CC=CC=C3)C(O)=CC(O)=C2C(=O)CCC4=CC=CC=C4 '
               'NAME: Calomelanol D-1 REASON: WRONGLY CLASSIFIED Found '
               'neoflavonoid core: a 1-benzopyran (or oxidized variant) fused '
               'to a benzene ring with a candidate aryl substituent at the '
               '4–position.\n'
               ' * SMILES: '
               'O=C1C2=C(O)C(OC)=C(O)C=3C2=C(C(O)=C(O)C3C)C([C@@]1(O)C(C(=O)C)(C)C)=O '
               'NAME: Sculezonone B REASON: WRONGLY CLASSIFIED Found '
               'neoflavonoid core: a 1-benzopyran (or oxidized variant) fused '
               'to a benzene ring with a candidate aryl substituent at the '
               '4–position.\n'
               ' * SMILES: '
               'O=C1C(=O)C2=C(O)C=CC=C2C=3C1=C(O)C(=C(C(=O)CCC(C)C)C3)C NAME: '
               'Piloquinone REASON: WRONGLY CLASSIFIED Found neoflavonoid '
               'core: a 1-benzopyran (or oxidized variant) fused to a benzene '
               'ring with a candidate aryl substituent at the 4–position.\n'
               ' * SMILES: '
               'O=C1OC2=C(C(O)=C(O)C=C2C=3C1=C(O)C=C(OC)C3)C4=C(O)C(O)=CC5=C4C6=C(C(O)=CC(=C6)OC)C(O5)=O '
               'NAME: Verrulactone B REASON: WRONGLY CLASSIFIED Found '
               'neoflavonoid core: a 1-benzopyran (or oxidized variant) fused '
               'to a benzene ring with a candidate aryl substituent at the '
               '4–position.\n'
               ' * SMILES: '
               'ClC1=C2OC([C@H]3CC=4C([C@H]3C2=C(OC)C(=C1C)Cl)=C(C(O)=CC4O)C=O)(C)C '
               'NAME: (+/-)-pestalachloride D REASON: WRONGLY CLASSIFIED Found '
               'neoflavonoid core: a 1-benzopyran (or oxidized variant) fused '
               'to a benzene ring with a candidate aryl substituent at the '
               '4–position.\n'
               ' * SMILES: '
               'COC1=C(C=C(C=C1)C2C3=C(C=C(C=C3)O)OC4=C2C(=N)N(C=N4)CC5=CC=CO5)OC '
               'NAME: '
               '5-(3,4-dimethoxyphenyl)-3-(2-furanylmethyl)-4-imino-5H-[1]benzopyrano[2,3-d]pyrimidin-8-ol '
               'REASON: WRONGLY CLASSIFIED Found neoflavonoid core: a '
               '1-benzopyran (or oxidized variant) fused to a benzene ring '
               'with a candidate aryl substituent at the 4–position.\n'
               ' * SMILES: '
               'O1C2(C=3C(C1=O)=CC=CC3)C4=C(OC5=C2C=CC(O)=C5)C=C(OC6=CC=C(O)C=C6)C=C4 '
               'NAME: HPF REASON: WRONGLY CLASSIFIED Found neoflavonoid core: '
               'a 1-benzopyran (or oxidized variant) fused to a benzene ring '
               'with a candidate aryl substituent at the 4–position.\n'
               ' * SMILES: '
               'O1C(OC2=C3C(CC(OC3=C4CC(O)C(OC4=C2)C5=CC(O)=C(O)C=C5)=O)C6=CC(OC)=C(O)C=C6)C(O)C(O)C(O)C1CO '
               'NAME: '
               '12-(3,4-dihydroxyphenyl)-13-hydroxy-6-(4-hydroxy-3-methoxyphenyl)-8-{[3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy}-3,11-dioxatricyclo[8.4.0.0?,?]tetradeca-1,7,9-trien-4-one '
               'REASON: WRONGLY CLASSIFIED Found neoflavonoid core: a '
               '1-benzopyran (or oxidized variant) fused to a benzene ring '
               'with a candidate aryl substituent at the 4–position.\n'
               ' * SMILES: '
               'O[C@H]1Cc2c(O)cc(O)c([C@@H]3[C@@H](OC(=O)c4cc(O)c(O)c(O)c4)[C@H](Oc4cc(O)cc(O)c34)c3ccc(O)c(O)c3)c2O[C@@H]1c1ccc(O)c(O)c1 '
               'NAME: procyanidin B1 3-O-gallate REASON: WRONGLY CLASSIFIED '
               'Found neoflavonoid core: a 1-benzopyran (or oxidized variant) '
               'fused to a benzene ring with a candidate aryl substituent at '
               'the 4–position.\n'
               ' * SMILES: '
               'O[C@H]1Cc2c(O)cc(O)c([C@@H]3[C@@H](O)[C@H](Oc4cc(O)cc(O)c34)c3ccc(O)c(O)c3)c2O[C@@H]1c1cc(O)c(O)c(O)c1 '
               'NAME: (-)-epicatechin-(4beta->8)-(+)-gallocatechin REASON: '
               'WRONGLY CLASSIFIED Found neoflavonoid core: a 1-benzopyran (or '
               'oxidized variant) fused to a benzene ring with a candidate '
               'aryl substituent at the 4–position.\n'
               ' * SMILES: '
               'C1=2C(=C(C=C3C(N(C(C(=CC=C1)C23)=O)C=4C=CC(=C(C4)C(=O)[O-])O)=O)S([O-])(=O)=O)N.[Na+].[Na+] '
               'NAME: Chrome fast yellow 8GL REASON: WRONGLY CLASSIFIED Found '
               'neoflavonoid core: a 1-benzopyran (or oxidized variant) fused '
               'to a benzene ring with a candidate aryl substituent at the '
               '4–position.\n'
               ' * SMILES: '
               'O1C([C@H](O)[C@@H](O)[C@H](O)[C@H]1CO)C2=C(O)C=3[C@@]([C@@H](O)[C@H](OC3C=C2O)C4=CC(O)=C(O)C=C4)(C=5C=6O[C@@H]([C@H](O)CC6C(O)=CC5O)C7=CC(O)=C(O)C=C7)[H] '
               'NAME: 6-Glucopyranosylprocyanidin B2 REASON: WRONGLY '
               'CLASSIFIED Found neoflavonoid core: a 1-benzopyran (or '
               'oxidized variant) fused to a benzene ring with a candidate '
               'aryl substituent at the 4–position.\n'
               ' * SMILES: '
               'Cc1ccc(N(CC(O)=O)CC(O)=O)c(OCCOc2cc(ccc2N(CC(O)=O)CC(O)=O)-c2c3cc(Cl)c(O)cc3oc3cc(=O)c(Cl)cc23)c1 '
               'NAME: Fluo-3 REASON: WRONGLY CLASSIFIED Found neoflavonoid '
               'core: a 1-benzopyran (or oxidized variant) fused to a benzene '
               'ring with a candidate aryl substituent at the 4–position.\n'
               ' * SMILES: '
               'CN1c2cc3Oc4cc5=[N+](C)C(C)(C)C=C(C)c5cc4=C(c3cc2C(C)=CC1(C)C)c1ccc(NC(=O)c2ccc(CCl)cc2)cc1C([O-])=O '
               'NAME: CellTracker red CMTPX 5-isomer REASON: WRONGLY '
               'CLASSIFIED Found neoflavonoid core: a 1-benzopyran (or '
               'oxidized variant) fused to a benzene ring with a candidate '
               'aryl substituent at the 4–position.\n'
               'False negatives: SMILES: '
               'COC1=CC(=O)C(=CC1=O)[C@@H](C=C)c1ccc(OC)c(O)c1 NAME: '
               "S-3'-hydroxy-4,4'-dimethoxydalbergione REASON: MISSED No "
               'suitable candidate 1-benzopyran (or oxidized variant) with an '
               'external aryl substituent at the 4–position was identified\n'
               ' * SMILES: O(C=1C(=O)C=C([C@H](C2=CC=C(O)C=C2)C=C)C(=O)C1)C '
               "NAME: (S)-4'-Hydroxy-4-methoxydalbergione REASON: MISSED No "
               'suitable candidate 1-benzopyran (or oxidized variant) with an '
               'external aryl substituent at the 4–position was identified\n'
               ' * SMILES: O(C=1C(=O)C=C(C(C2=CC=C(O)C=C2)C=C)C(=O)C1)C NAME: '
               "Dalbergione, 4-methoxy-4'-hydroxy- REASON: MISSED No suitable "
               'candidate 1-benzopyran (or oxidized variant) with an external '
               'aryl substituent at the 4–position was identified\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'O1C2=C(O)C=C(COC)C=C2C[C@@H](C1(C)C)O',
                                     'name': 'Conoideochromane B',
                                     'reason': 'No suitable candidate '
                                               '1-benzopyran (or oxidized '
                                               'variant) with an external aryl '
                                               'substituent at the 4–position '
                                               'was identified'},
                                 {   'smiles': 'P(OC[C@H](OC(=O)CCCCCCC/C=C\\CCCCC)CO/C=C\\CCCCCCCCCCCCCC)(OCCN)(O)=O',
                                     'name': 'PE(P-16:0/15:1(9Z))',
                                     'reason': 'No 6-membered heterocycle '
                                               'candidate found (neither '
                                               'classic pyran nor oxidized '
                                               'variant detected)'},
                                 {   'smiles': 'O=C1C=2C(OC(=C1)C)=C(C3=C4O[C@](O)(CC(C4=C(O)C=5C3=CC(OC)=CC5OC)=O)C)C6=CC(OC)=CC(=C6C2O)OC',
                                     'name': '2-hydroxydihydronigerone',
                                     'reason': 'No suitable candidate '
                                               '1-benzopyran (or oxidized '
                                               'variant) with an external aryl '
                                               'substituent at the 4–position '
                                               'was identified'},
                                 {   'smiles': 'O([C@@H]1[C@@H](NC(=O)C)[C@@H](O[C@@H]([C@H]1O)CO)OC[C@H]2O[C@@H](O)[C@H](NC(=O)C)[C@@H](O)[C@H]2O)[C@@H]3O[C@@H]([C@H](O)[C@H](O[C@H]4O[C@@H]([C@H](O)[C@H](O)[C@H]4O)CO)[C@H]3O)CO',
                                     'name': 'N-[(2R,3R,4R,5R,6R)-6-[[(2R,3R,4R,5S,6R)-3-Acetamido-4-[(2R,3R,4S,5S,6R)-3,5-dihydroxy-6-(hydroxymethyl)-4-[(2R,3R,4S,5R,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-5-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxymethyl]-2,4,5-trihydroxyoxan-3-yl]acetamide',
                                     'reason': 'No 6-membered aromatic benzene '
                                               'ring found'},
                                 {   'smiles': 'O1C(C(O)C(O)C(O)C1OC=2C(O)=C(O)C=C(C2)C=O)COC(=O)C3=CC(O)=C(O)C(O)=C3',
                                     'name': 'Castamollissin',
                                     'reason': 'No suitable candidate '
                                               '1-benzopyran (or oxidized '
                                               'variant) with an external aryl '
                                               'substituent at the 4–position '
                                               'was identified'},
                                 {   'smiles': 'S(OC[C@H]1O[C@@H](OC[C@H]2O[C@@H](O[C@@H]([C@@H](O)[C@H](O)CO[C@]3(O[C@H]([C@H](NC(=O)C)[C@@H](O)C3)[C@H](O)[C@H](O)CO)C(O)=O)[C@@H](NC(=O)C)CO)[C@H](O)[C@@H](O)[C@H]2O)[C@H](NC(=O)C)[C@@H](O)[C@@H]1O[C@@H]4O[C@@H]([C@H](O)[C@H](O)[C@H]4O)CO[C@]5(O[C@H]([C@H](NC(=O)C)[C@@H](O)C5)[C@H](O)[C@H](O)CO)C(O)=O)(O)(=O)=O',
                                     'name': '(2R,4S,5R,6R)-5-Acetamido-2-[[(2R,3R,4S,5R,6S)-6-[(2R,3S,4R,5R,6R)-5-acetamido-6-[[(2R,3R,4S,5R,6R)-6-[(2S,3R,4S,5R)-2-acetamido-6-[(2R,4S,5R,6R)-5-acetamido-2-carboxy-4-hydroxy-6-[(1R,2R)-1,2,3-trihydroxypropyl]oxan-2-yl]oxy-1,4,5-trihydroxyhexan-3-yl]oxy-3,4,5-trihydroxyoxan-2-yl]methoxy]-4-hydroxy-2-(sulfooxymethyl)oxan-3-yl]oxy-3,4,5-trihydroxyoxan-2-yl]methoxy]-4-hydroxy-6-[(1R,2R)-1,2,3-trihydroxypropyl]oxane-2-carboxylic '
                                             'acid',
                                     'reason': 'No 6-membered aromatic benzene '
                                               'ring found'},
                                 {   'smiles': 'FC(F)(F)C(F)(F)C(F)(F)C(F)(F)C(F)(F)C(F)(F)F',
                                     'name': 'perfluorohexane',
                                     'reason': 'No 6-membered heterocycle '
                                               'candidate found (neither '
                                               'classic pyran nor oxidized '
                                               'variant detected)'},
                                 {   'smiles': 'CC(C)(O)CCC(=O)[C@](C)(O)[C@H]1[C@H](O)C[C@@]2(C)[C@@H]3CC=C4[C@@H](C[C@@H](O)[C@@H](O)C4(C)C)[C@]3(C)C(=O)C[C@]12C',
                                     'name': 'Cucurbitacin P',
                                     'reason': 'No 6-membered heterocycle '
                                               'candidate found (neither '
                                               'classic pyran nor oxidized '
                                               'variant detected)'},
                                 {   'smiles': 'CCCCCCCc1cc(O)cc(=O)o1',
                                     'name': '4-hydroxy-6-heptylpyran-2-one',
                                     'reason': 'No 6-membered aromatic benzene '
                                               'ring found'},
                                 {   'smiles': 'S(O[C@@H]1[C@@H](O)[C@H](O[C@H]2[C@H](O)[C@@H](NC(=O)C)[C@H](O[C@H]3[C@@H](O)[C@H](O[C@@H]4O[C@@H]([C@@H](O[C@@H]5O[C@@H]([C@H](O)[C@H](OS(O)(=O)=O)[C@H]5O)CO)[C@H](O)[C@H]4NC(=O)C)CO)[C@H](O[C@@H]3O[C@H]6[C@H](O)[C@H](O[C@@H](O[C@H]7[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]7CO)O[C@H]8[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]8CO[C@@H]9O[C@H]([C@@H](O)[C@@H](O)[C@@H]9O)C)O)[C@H]6O)CO[C@H]%10O[C@@H]([C@@H](O)[C@H](O)[C@@H]%10O[C@@H]%11O[C@@H]([C@@H](O[C@@H]%12O[C@@H]([C@H](O[C@@H]%13O[C@@H]([C@H](O)[C@H](O)[C@H]%13NC(=O)C)CO)[C@H](O[C@]%14(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%14)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%12O)CO)[C@H](O)[C@H]%11NC(=O)C)CO)CO[C@@H]%15O[C@@H]([C@@H](O[C@@H]%16O[C@@H]([C@H](O)[C@H](O[C@]%17(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%17)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%16O)CO)[C@H](O)[C@H]%15NC(=O)C)CO)CO)O[C@@H]2CO)O[C@@H]([C@@H]1O)CO)(O)(=O)=O',
                                     'name': 'CID 146017241',
                                     'reason': 'No 6-membered aromatic benzene '
                                               'ring found'}],
    'sample_false_negatives': [   {   'smiles': 'CC1=CC(=CC2=C1C(CC3(O2)CC(NC(=S)N3)(C)C)C4=CC=C(C=C4)OC)O',
                                      'name': "7'-hydroxy-4'-(4-methoxyphenyl)-4,4,5'-trimethyl-2-spiro[1,3-diazinane-6,2'-3,4-dihydro-2H-1-benzopyran]thione",
                                      'reason': 'No suitable candidate '
                                                '1-benzopyran (or oxidized '
                                                'variant) with an external '
                                                'aryl substituent at the '
                                                '4–position was identified'},
                                  {   'smiles': 'O1C(CC(C2=C1C=C(O)C3=C2N(C4=C(C3=O)C=CC=C4O)C)C5=C6OC(C=CC6=C7N(C8=C(C(=O)C7=C5O)C=CC=C8O)C)(C)C)(C)C',
                                      'name': 'Bis(5-hydroxynoracronycine)',
                                      'reason': 'No suitable candidate '
                                                '1-benzopyran (or oxidized '
                                                'variant) with an external '
                                                'aryl substituent at the '
                                                '4–position was identified'},
                                  {   'smiles': 'O1[C@]2(O)[C@@]([C@H](C3=C1C(=C(O)C4=C3O[C@@H](CC4=O)C5=CC=CC=C5)C)C6=CC=CC=C6)(C(=O)C(C(=O)C2(C)C)(C)C)[H]',
                                      'name': 'Leucadenone B',
                                      'reason': 'No suitable candidate '
                                                '1-benzopyran (or oxidized '
                                                'variant) with an external '
                                                'aryl substituent at the '
                                                '4–position was identified'},
                                  {   'smiles': 'COC1=C(C=C2C(=CC(=O)OC2=C1OC)C3=CC=CC=C3)O',
                                      'name': '6-hydroxy-7,8-dimethoxy-4-phenyl-1-benzopyran-2-one',
                                      'reason': 'No suitable candidate '
                                                '1-benzopyran (or oxidized '
                                                'variant) with an external '
                                                'aryl substituent at the '
                                                '4–position was identified'},
                                  {   'smiles': 'COc1ccc(cc1O)-c1cc(=O)oc2cc(OC)c(O)cc12',
                                      'name': 'melannein',
                                      'reason': 'No suitable candidate '
                                                '1-benzopyran (or oxidized '
                                                'variant) with an external '
                                                'aryl substituent at the '
                                                '4–position was identified'},
                                  {   'smiles': 'CC(C)CC(=O)c1c(O)c(CC=C(C)C)c(O)c2c(cc(=O)oc12)-c1ccccc1',
                                      'name': 'Mammea A/BA',
                                      'reason': 'No suitable candidate '
                                                '1-benzopyran (or oxidized '
                                                'variant) with an external '
                                                'aryl substituent at the '
                                                '4–position was identified'},
                                  {   'smiles': 'O=C1OC2=C(O)C=C(C)C=C2C(=C1O)C3=CC=C(O)C=C3',
                                      'name': '3,8-dihydroxy-4-(4-hydroxyphenyl)-6-methylcoumarin',
                                      'reason': 'No suitable candidate '
                                                '1-benzopyran (or oxidized '
                                                'variant) with an external '
                                                'aryl substituent at the '
                                                '4–position was identified'},
                                  {   'smiles': 'COC1=CC(=O)C(=CC1=O)[C@@H](C=C)c1ccc(OC)c(O)c1',
                                      'name': "S-3'-hydroxy-4,4'-dimethoxydalbergione",
                                      'reason': 'No suitable candidate '
                                                '1-benzopyran (or oxidized '
                                                'variant) with an external '
                                                'aryl substituent at the '
                                                '4–position was identified'},
                                  {   'smiles': 'O1[C@]2(O)[C@]([C@@H](C3=C1C(=C(O)C4=C3O[C@@H](CC4=O)C5=CC=CC=C5)C)C6=CC=CC=C6)(C(=O)C(C(=O)C2(C)C)(C)C)[H]',
                                      'name': 'Leucadenone C',
                                      'reason': 'No suitable candidate '
                                                '1-benzopyran (or oxidized '
                                                'variant) with an external '
                                                'aryl substituent at the '
                                                '4–position was identified'},
                                  {   'smiles': 'O(C=1C(=O)C=C([C@H](C2=CC=C(O)C=C2)C=C)C(=O)C1)C',
                                      'name': "(S)-4'-Hydroxy-4-methoxydalbergione",
                                      'reason': 'No suitable candidate '
                                                '1-benzopyran (or oxidized '
                                                'variant) with an external '
                                                'aryl substituent at the '
                                                '4–position was identified'}],
    'attempt': 5,
    'reasoning': 'Below is our revised solution with extensive inline '
                 'comments. In our reasoning we noticed that the previous code '
                 '– though able to flag many “neoflavonoid‐like” cores – was '
                 'overly permissive in that it simply looked for two shared '
                 'atoms between a candidate 6‐membered “heterocycle” and a '
                 'benzene ring and then checked that one atom (the candidate '
                 '“4–position”) bore an aromatic neighbor. This produced false '
                 'positives from molecules that merely had a fused ring system '
                 'with extra aromatic rings. In our revision we (1) re‐use the '
                 'ring–ordering helper but now try all rotations of the '
                 'heterocycle so that the fused pair (two atoms shared with '
                 'the benzene) can be detected anywhere in the cyclic order, '
                 'and (2) we more carefully demand that the substituent '
                 'departing from the candidate “4–position” is attached via a '
                 'single bond and is part of an external benzene (i.e. a '
                 'benzene ring that is fully disjoint from the heterocycle). '
                 'In addition, small tweaks (such as testing both the classic '
                 'ring oxygen and oxidized variants) have been retained. We '
                 'hope these improvements reduce false positives and catch the '
                 'previously “missed” structures.\n'
                 '\n'
                 'Below is the complete code in one Python block:\n'
                 '\n'
                 '------------------------------------------------',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 38,
    'num_false_positives': 208,
    'num_true_negatives': 142036,
    'num_false_negatives': 18,
    'num_negatives': None,
    'precision': 0.15447154471544716,
    'recall': 0.6785714285714286,
    'f1': 0.25165562913907286,
    'accuracy': 0.9984118060435699,
    'negative_predictive_value': 0.9998732876230166}