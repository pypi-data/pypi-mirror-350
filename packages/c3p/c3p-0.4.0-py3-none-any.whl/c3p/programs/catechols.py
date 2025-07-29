"""
Classifies: CHEBI:33566 catechols
"""
#!/usr/bin/env python3
"""
Classifies: Catechols 
Definition: Any compound containing an o-diphenol component.
A catechol is defined as a six‐membered ring (aromatic or highly conjugated)
bearing two adjacent substituents that are hydroxyl groups (–OH or their deprotonated/esterified form),
wherein the oxygen is directly bound to the ring carbon via a single bond and is not further bonded to a carbon.
Moreover, to avoid classifying complex fused polyphenols as “catechols”, we only accept rings that are not fused to any other ring.
"""

from rdkit import Chem

def is_catechols(smiles: str):
    """
    Determines if a molecule contains a catechol moiety (an o-diphenol component)
    based on its SMILES string.
    
    The algorithm is as follows:
      1. Convert the SMILES to an RDKit molecule.
      2. Obtain all rings in the molecule. For every six‐membered ring, check if it is “isolated” (not fused) 
         by ensuring that none of its atoms appear in any other ring.
      3. For each isolated ring, first check that the ring is sufficiently conjugated: either the ring is aromatic,
         or – if not aromatic – it contains at least 2 double bonds.
      4. Then, for each bond in that ring (i.e. for every adjacent pair of ring atoms, in an ordered cycle),
         check whether both atoms have a qualifying oxygen substituent. 
         A qualifying oxygen is attached with a single bond and is not further bound to any carbon.
      5. If any pair of adjacent ring atoms meets the criteria, the molecule is classified as a catechol.
    
    Args:
        smiles (str): SMILES string of the molecule.
    
    Returns:
        bool: True if the molecule contains a catechol moiety, False otherwise.
        str: Reason for the classification.
    """
    
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
    
    ring_info = mol.GetRingInfo()
    atom_rings = ring_info.AtomRings()
    
    # Helper to decide if an oxygen attached to an atom qualifies.
    def has_qualifying_oxygen(atom):
        for neighbor in atom.GetNeighbors():
            if neighbor.GetAtomicNum() != 8:
                continue
            bond = mol.GetBondBetweenAtoms(atom.GetIdx(), neighbor.GetIdx())
            # Require bond to be single
            if bond is None or bond.GetBondType() != Chem.BondType.SINGLE:
                continue
            qualifies = True
            # The oxygen must not be attached to any carbon besides the aromatic/conjugated atom.
            for nb in neighbor.GetNeighbors():
                if nb.GetIdx() == atom.GetIdx():
                    continue
                if nb.GetAtomicNum() == 6:
                    qualifies = False
                    break
            if qualifies:
                return True
        return False

    # Helper to decide whether an atom is present in any other ring than ring_atoms.
    def is_atom_exclusively_in_ring(atom_idx, ring_atoms):
        count = 0
        for ring in atom_rings:
            if atom_idx in ring:
                # if ring is not exactly our candidate ring, count it
                if set(ring) != set(ring_atoms):
                    return False
                count += 1
        return count == 1  # appears only in this ring

    # Helper to check if a candidate ring (list of atom indices) is isolated (non-fused).
    def is_isolated_ring(ring_atoms):
        for idx in ring_atoms:
            # if this atom appears in any ring that is not exactly ring_atoms, consider ring fused.
            if not is_atom_exclusively_in_ring(idx, ring_atoms):
                return False
        return True

    # Helper to order the atoms in a ring.
    # Since atom_rings is an unordered tuple of indices, we produce an ordering by linking adjacent atoms.
    def order_ring(ring_atoms):
        # Build a simple connectivity map restricted to ring_atoms.
        ring_set = set(ring_atoms)
        connectivity = {i: [] for i in ring_atoms}
        for i in ring_atoms:
            atom = mol.GetAtomWithIdx(i)
            for nbr in atom.GetNeighbors():
                j = nbr.GetIdx()
                if j in ring_set:
                    connectivity[i].append(j)
        # Now pick an arbitrary starting atom and perform a simple cycle traversal.
        ordered = [ring_atoms[0]]
        prev = None
        while len(ordered) < len(ring_atoms):
            current = ordered[-1]
            # choose the neighbor that is not the previous atom
            next_atoms = [n for n in connectivity[current] if n != prev]
            if not next_atoms:
                break  # should not happen in a proper cycle
            ordered.append(next_atoms[0])
            prev = current
        return ordered

    # Helper to count the number of explicit double bonds in a ring.
    def count_double_bonds_in_ring(ordered_ring):
        count = 0
        n = len(ordered_ring)
        # because the ring is cyclic, add bond from last to first
        for i in range(n):
            a1 = ordered_ring[i]
            a2 = ordered_ring[(i+1)%n]
            bond = mol.GetBondBetweenAtoms(a1, a2)
            if bond is not None and bond.GetBondType() == Chem.BondType.DOUBLE:
                count += 1
        return count

    # Now iterate over all rings of exactly 6 atoms.
    for ring in atom_rings:
        if len(ring) != 6:
            continue
        if not is_isolated_ring(ring):
            # Skip rings that are fused into a larger polycyclic system.
            continue
        ordered_ring = order_ring(list(ring))
        # Determine if the ring is considered aromatic or at least conjugated.
        # If any atom in the ring is flagged as aromatic, treat the ring as aromatic.
        is_aromatic_ring = any(mol.GetAtomWithIdx(idx).GetIsAromatic() for idx in ordered_ring)
        if not is_aromatic_ring:
            dbl_bonds = count_double_bonds_in_ring(ordered_ring)
            if dbl_bonds < 2:
                # Not enough conjugation for a catechol moiety.
                continue

        # Now check each adjacent pair in the ring.
        n = len(ordered_ring)
        for i in range(n):
            a1 = mol.GetAtomWithIdx(ordered_ring[i])
            a2 = mol.GetAtomWithIdx(ordered_ring[(i+1)%n])
            # Make sure both atoms are carbons.
            if a1.GetAtomicNum() != 6 or a2.GetAtomicNum() != 6:
                continue
            # Check both atoms for a qualifying oxygen substituent.
            if has_qualifying_oxygen(a1) and has_qualifying_oxygen(a2):
                return True, "Contains o-diphenol (catechol) moiety on a non-fused, six-membered aromatic or conjugated ring"
                
    return False, "No adjacent qualifying hydroxyl substituents found on an isolated six-membered ring"

# Example usage (for testing):
if __name__ == '__main__':
    examples = [
        # True positives:
        ("[C@@H]1([C@@H]([C@H]([C@@H]([C@H](O1)CO)O)O)O)O[C@H]2/C(/[C@](C(=CO2)C(=O)OC)([H])CC(=O)OCCC=3C=CC(=C(C3)O)O)=C/C", "oleuropein"),
        ("C1=CC(=C(C(=C1O)O)[N+]([O-])=O)C", "4-methyl-3-nitrocatechol"),
        ("C1(=CC=C(C=C1O)[N+]([O-])=O)O", "4-nitrocatechol"),
        ("C=1(C=CC(=C(C1)O)O)/C=C/C(OCC)=O", "ethyl trans-caffeate"),
        ("OC[C@H]1O[C@@H](OCCc2ccc(O)c(O)c2)[C@H](OC(=O)Cc2ccc(O)cc2)[C@@H](O)[C@@H]1O", "ternstroside B"),
        ("S(OC1=C(O)C=C([C@@H](O)CN)C=C1)(O)(=O)=O", "Norepinephrine sulfate"),
        ("OC1C(O)c2c(O)cc(O)cc2OC1c1cc(O)c(O)c(O)c1", "flavan-3,3',4,4',5,5',7-heptol"),
        ("COc1cc(-c2ccc(O)cc2)c(OC)c2oc3cc(O)c(O)cc3c12", "candidusin A"),
        ("O=C1OC(=CC2=C1C3(OC(C)=CC3=O)C(C4=CC(O)=C(O)C=C4)O2)/C=C/C5=CC(O)=C(O)C=C5", "Inoscavin A"),
        ("O=C1OC(=CC(=C1C(C=2C(=O)OC(/C=C/C3=CC(O)=C(O)C=C3)=CC2O)C)O)/C=C/C4=CC(O)=C(O)C=C4", "Pinillidine"),
        ("CC(C)c1cccc(O)c1O", "3-isopropylcatechol"),
        ("O[C@@H](CC\\C=C\\c1ccc(O)cc1)CCc1ccc(O)c(O)c1", "(-)-(3S)-1-(3,4-dihydroxyphenyl)-7-(4-hydroxyphenyl)-(6E)-6-hepten-3-ol"),
        # False negative example (should be detected):
        ("O[C@H]1C=CC=C[C@H]1O", "cis-cyclohexa-3,5-diene-1,2-diol"),
    ]
    for smi, name in examples:
        result, reason = is_catechols(smi)
        print(f"NAME: {name}\nSMILES: {smi}\nResult: {result} -> {reason}\n{'-'*80}")


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:33566',
                          'name': 'catechols',
                          'definition': 'Any compound containing an o-diphenol '
                                        'component.',
                          'parents': ['CHEBI:33570'],
                          'xrefs': ['KEGG:C15571'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 134,
                           'log_lines_of_code': 4.897839799950911,
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
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 3,
                                                 4,
                                                 3,
                                                 3,
                                                 3,
                                                 4,
                                                 3,
                                                 3,
                                                 3,
                                                 4,
                                                 5,
                                                 4,
                                                 5,
                                                 5,
                                                 3,
                                                 4,
                                                 2,
                                                 0,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 3,
                                                 4,
                                                 4,
                                                 5,
                                                 4,
                                                 2,
                                                 0,
                                                 1,
                                                 1,
                                                 2,
                                                 3,
                                                 3,
                                                 4,
                                                 2,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 3,
                                                 4,
                                                 4,
                                                 5,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 3,
                                                 3,
                                                 3,
                                                 4,
                                                 3,
                                                 3,
                                                 2,
                                                 0,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 3,
                                                 3,
                                                 3,
                                                 4,
                                                 2,
                                                 0,
                                                 1,
                                                 1,
                                                 2,
                                                 3,
                                                 2,
                                                 3,
                                                 3,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 3,
                                                 4,
                                                 4,
                                                 0,
                                                 0,
                                                 1,
                                                 0,
                                                 1,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 1,
                                                 1,
                                                 2,
                                                 2],
                           'max_indent': 5,
                           'imports': ['from rdkit import Chem'],
                           'imports_count': 1,
                           'methods_called': [   'GetIdx',
                                                 'GetAtomicNum',
                                                 'MolFromSmiles',
                                                 'AtomRings',
                                                 'GetAtomWithIdx',
                                                 'GetBondBetweenAtoms',
                                                 'GetNeighbors',
                                                 'append',
                                                 'GetBondType',
                                                 'GetRingInfo',
                                                 'GetIsAromatic'],
                           'methods_called_count': 11,
                           'smarts_strings': [],
                           'smarts_strings_count': 0,
                           'defs': [   'is_catechols(smiles: str):',
                                       'has_qualifying_oxygen(atom):',
                                       'is_atom_exclusively_in_ring(atom_idx, '
                                       'ring_atoms):',
                                       'is_isolated_ring(ring_atoms):',
                                       'order_ring(ring_atoms):',
                                       'count_double_bonds_in_ring(ordered_ring):'],
                           'defs_count': 6,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'True',
                                          'False',
                                          'False',
                                          'count == 1  # appears only in this '
                                          'ring',
                                          'False',
                                          'True',
                                          'ordered',
                                          'count',
                                          'False, "No adjacent qualifying '
                                          'hydroxyl substituents found on an '
                                          'isolated six-membered ring"'],
                           'returns_count': 10,
                           'complexity': 7.379567959990183},
    'message': '\n'
               'Attempt failed: F1 score of 0.20018945374171138 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: '
               '[C@@H]1([C@@H]([C@H]([C@@H]([C@H](O1)CO)O)O)O)O[C@H]2/C(/[C@](C(=CO2)C(=O)OC)([H])CC(=O)OCCC=3C=CC(=C(C3)O)O)=C/C '
               'NAME: oleuropein REASON: CORRECT Contains o-diphenol '
               '(catechol) moiety on a six-membered aromatic ring\n'
               ' * SMILES: C1=CC(=C(C(=C1O)O)[N+]([O-])=O)C NAME: '
               '4-methyl-3-nitrocatechol REASON: CORRECT Contains o-diphenol '
               '(catechol) moiety on a six-membered aromatic ring\n'
               ' * SMILES: C1(=CC=C(C=C1O)[N+]([O-])=O)O NAME: 4-nitrocatechol '
               'REASON: CORRECT Contains o-diphenol (catechol) moiety on a '
               'six-membered aromatic ring\n'
               ' * SMILES: C=1(C=CC(=C(C1)O)O)/C=C/C(OCC)=O NAME: ethyl '
               'trans-caffeate REASON: CORRECT Contains o-diphenol (catechol) '
               'moiety on a six-membered aromatic ring\n'
               ' * SMILES: '
               'OC[C@H]1O[C@@H](OCCc2ccc(O)c(O)c2)[C@H](OC(=O)Cc2ccc(O)cc2)[C@@H](O)[C@@H]1O '
               'NAME: ternstroside B REASON: CORRECT Contains o-diphenol '
               '(catechol) moiety on a six-membered aromatic ring\n'
               ' * SMILES: S(OC1=C(O)C=C([C@@H](O)CN)C=C1)(O)(=O)=O NAME: '
               'Norepinephrine sulfate REASON: CORRECT Contains o-diphenol '
               '(catechol) moiety on a six-membered aromatic ring\n'
               ' * SMILES: OC1C(O)c2c(O)cc(O)cc2OC1c1cc(O)c(O)c(O)c1 NAME: '
               "flavan-3,3',4,4',5,5',7-heptol REASON: CORRECT Contains "
               'o-diphenol (catechol) moiety on a six-membered aromatic ring\n'
               ' * SMILES: COc1cc(-c2ccc(O)cc2)c(OC)c2oc3cc(O)c(O)cc3c12 NAME: '
               'candidusin A REASON: CORRECT Contains o-diphenol (catechol) '
               'moiety on a six-membered aromatic ring\n'
               ' * SMILES: '
               'O=C1OC(=CC2=C1C3(OC(C)=CC3=O)C(C4=CC(O)=C(O)C=C4)O2)/C=C/C5=CC(O)=C(O)C=C5 '
               'NAME: Inoscavin A REASON: CORRECT Contains o-diphenol '
               '(catechol) moiety on a six-membered aromatic ring\n'
               ' * SMILES: '
               'O=C1OC(=CC(=C1C(C=2C(=O)OC(/C=C/C3=CC(O)=C(O)C=C3)=CC2O)C)O)/C=C/C4=CC(O)=C(O)C=C4 '
               'NAME: Pinillidine REASON: CORRECT Contains o-diphenol '
               '(catechol) moiety on a six-membered aromatic ring\n'
               ' * SMILES: CC(C)c1cccc(O)c1O NAME: 3-isopropylcatechol REASON: '
               'CORRECT Contains o-diphenol (catechol) moiety on a '
               'six-membered aromatic ring\n'
               ' * SMILES: O[C@@H](CC\\C=C\\c1ccc(O)cc1)CCc1ccc(O)c(O)c1 NAME: '
               '(-)-(3S)-1-(3,4-dihydroxyphenyl)-7-(4-hydroxyphenyl)-(6E)-6-hepten-3-ol '
               'REASON: CORRECT Contains o-diphenol (catechol) moiety on a '
               'six-membered aromatic ring\n'
               ' * SMILES: COC1OC(C)=Cc2oc3cc(O)c(O)c(C(O)=O)c3c(=O)c12 NAME: '
               '7,8-dihydroxy-1-methoxy-3-methyl-10-oxo-1H,10H-pyrano[4,3-b]chromene-9-carboxylic '
               'acid REASON: CORRECT Contains o-diphenol (catechol) moiety on '
               'a six-membered aromatic ring\n'
               ' * SMILES: C=1(C=CC=CC1C(=O)/C=C/C2=CC(=C(C=C2)O)O)O NAME: '
               "2',3,4-trihydroxy-trans-chalcone REASON: CORRECT Contains "
               'o-diphenol (catechol) moiety on a six-membered aromatic ring\n'
               ' * SMILES: CN(C)CCC1=CC=CC=C1\\N=N\\C1=CC=C(O)C(O)=C1 NAME: '
               'trans-azodopa REASON: CORRECT Contains o-diphenol (catechol) '
               'moiety on a six-membered aromatic ring\n'
               ' * SMILES: CCCCCCCCCCCCCCCc1cc(C)c(C)c(O)c1O NAME: '
               '5,6-dimethyl-3-pentadecylcatechol REASON: CORRECT Contains '
               'o-diphenol (catechol) moiety on a six-membered aromatic ring\n'
               ' * SMILES: '
               'OC1=C(O)C=CC=C1CCCC/C=C\\C/C=C\\CCCCCCCC2=C(O)C(O)=CC=C2 NAME: '
               'Gerronemin F REASON: CORRECT Contains o-diphenol (catechol) '
               'moiety on a six-membered aromatic ring\n'
               ' * SMILES: '
               'O[C@@H]([C@@H](O)[C@@](O)(C(=O)/C=C/C1=CC(O)=C(O)C=C1)C(O)=O)[C@@](O)(C(=O)/C=C/C2=CC(O)=C(O)C=C2)C(O)=O '
               'NAME: 2,5-dicaffeoylaltraric acid REASON: CORRECT Contains '
               'o-diphenol (catechol) moiety on a six-membered aromatic ring\n'
               ' * SMILES: C1=CC(=C(C=C1C=C(C#N)C#N)O)O NAME: '
               '2-[(3,4-dihydroxyphenyl)methylidene]propanedinitrile REASON: '
               'CORRECT Contains o-diphenol (catechol) moiety on a '
               'six-membered aromatic ring\n'
               ' * SMILES: C(CNCCCCCCNCCC1=CC=CC=C1)C2=CC(O)=C(C=C2)O NAME: '
               'dopexamine REASON: CORRECT Contains o-diphenol (catechol) '
               'moiety on a six-membered aromatic ring\n'
               ' * SMILES: OC(C(O)=O)c1ccc(O)c(O)c1 NAME: '
               '3,4-dihydroxymandelic acid REASON: CORRECT Contains o-diphenol '
               '(catechol) moiety on a six-membered aromatic ring\n'
               ' * SMILES: '
               'OC[C@H]1O[C@H]([C@H](O)[C@@H](O)[C@@H]1O)c1c(O)cc(O)c(C(=O)CCc2ccc(O)c(O)c2)c1O '
               'NAME: aspalathin REASON: CORRECT Contains o-diphenol '
               '(catechol) moiety on a six-membered aromatic ring\n'
               ' * SMILES: '
               'OC1=CC=C(\\C=C\\C(=O)NCCCN(CCCCNC(=O)\\C=C\\C2=CC(O)=C(O)C=C2)C(=O)\\C=C\\C2=CC(O)=C(O)C=C2)C=C1O '
               'NAME: N(1),N(5),N(10)-tris-(E)-caffeoyl spermidine REASON: '
               'CORRECT Contains o-diphenol (catechol) moiety on a '
               'six-membered aromatic ring\n'
               ' * SMILES: '
               'OC1=CC=CC(C(=O)NC2=CC(NC(=O)C3=C(O)C(O)=CC=C3)=CC=C2)=C1O '
               'NAME: MST-312 REASON: CORRECT Contains o-diphenol (catechol) '
               'moiety on a six-membered aromatic ring\n'
               ' * SMILES: C(C(NCCC=1C=CC(=C(C1)O)O)=O)CCCCCCCCCCCCCC NAME: '
               'N-palmitoyl dopamine REASON: CORRECT Contains o-diphenol '
               '(catechol) moiety on a six-membered aromatic ring\n'
               'False positives: SMILES: '
               'Oc1ccc(cc1OS([O-])(=O)=O)-c1oc2cc([O-])cc(O)c2c(=O)c1OS([O-])(=O)=O '
               "NAME: quercetin 3,3'-bissulfate(3-) REASON: WRONGLY CLASSIFIED "
               'Contains o-diphenol (catechol) moiety on a six-membered '
               'aromatic ring\n'
               ' * SMILES: O=C1C2=C(O)C(O)=C(OC)C(=C2C(=O)C=3C1=C(OC3)C)O '
               'NAME: Isofuranonaphthoquinone E REASON: WRONGLY CLASSIFIED '
               'Contains o-diphenol (catechol) moiety on a six-membered '
               'aromatic ring\n'
               ' * SMILES: '
               'O1C([C@@H](O)C(O)C(O)[C@@H]1OC2=CC(C=3OC4=CC(O[C@@H]5O[C@H]([C@@H](O)C(O)C5O)C(O)=O)=CC(O)=C4C(=O)C3)=CC(O)=C2O)C(O)=O '
               "NAME: Tricetin 7,3'-diglucuronide REASON: WRONGLY CLASSIFIED "
               'Contains o-diphenol (catechol) moiety on a six-membered '
               'aromatic ring\n'
               ' * SMILES: '
               'S(OC=1C(O)=CC(C2OC3=C(C(=O)C2O)C(O)=C(O)C(O)=C3)=CC1O)(O)(=O)=O '
               'NAME: '
               '[2,6-dihydroxy-4-(3,5,6,7-tetrahydroxy-4-oxo-3,4-dihydro-2H-1-benzopyran-2-yl)phenyl]oxidanesulfonic '
               'acid REASON: WRONGLY CLASSIFIED Contains o-diphenol (catechol) '
               'moiety on a six-membered aromatic ring\n'
               ' * SMILES: '
               'O1C([C@H](O)[C@@H](O)[C@@H](O)[C@H]1CO)C=2C=3O[C@@H]([C@H](O)CC3C(O)=CC2O)C4=CC(O)=C(O)C=C4 '
               'NAME: (-)-Epicatechin 8-C-galactoside REASON: WRONGLY '
               'CLASSIFIED Contains o-diphenol (catechol) moiety on a '
               'six-membered aromatic ring\n'
               ' * SMILES: '
               'O1C([C@@H](O)[C@H](O)C(O)[C@@H]1OC=2C=3C[C@@H](OC(=O)C4=CC=CC=C4)[C@H](OC3C=C(O)C2)C5=CC(O)=C(O)C=C5)CO '
               'NAME: epicatechin 5-O-beta-D-glucopyranoside-3-benzoate '
               'REASON: WRONGLY CLASSIFIED Contains o-diphenol (catechol) '
               'moiety on a six-membered aromatic ring\n'
               ' * SMILES: '
               'S(OC=1C=C(C(=O)CCC2=C(OC)C3=C(OC(C=C3)(C)C)C=C2)C=CC1O)(O)(=O)=O '
               'NAME: '
               '{2-hydroxy-5-[3-(5-methoxy-2,2-dimethyl-2H-chromen-6-yl)propanoyl]phenyl}oxidanesulfonic '
               'acid REASON: WRONGLY CLASSIFIED Contains o-diphenol (catechol) '
               'moiety on a six-membered aromatic ring\n'
               ' * SMILES: '
               'O1C2=C([C@H](C=3C=4O[C@@H]([C@H](O)[C@H](C4C(O)=CC3O)C=5C=6O[C@@H]([C@@H](O)CC6C(O)=CC5O)C7=CC(O)=C(O)C=C7)C8=CC(O)=C(O)C=C8)[C@@H](O)[C@H]1C9=CC(O)=C(O)C=C9)C(O)=CC(O)=C2[C@H]%10C%11=C(O[C@@H]([C@@H]%10O)C%12=CC(O)=C(O)C=C%12)C=C(O)C=C%11O '
               'NAME: arecatannin a2 REASON: WRONGLY CLASSIFIED Contains '
               'o-diphenol (catechol) moiety on a six-membered aromatic ring\n'
               ' * SMILES: '
               'O=C1OC2=C(C(O)=C(O)C=C2C=3C1=C(O)C=C(OC)C3)C4=C(O)C(O)=CC5=C4C6=C(C(O)=CC(=C6)OC)C(O5)=O '
               'NAME: Verrulactone B REASON: WRONGLY CLASSIFIED Contains '
               'o-diphenol (catechol) moiety on a six-membered aromatic ring\n'
               ' * SMILES: '
               'O1C(C(O)C(O)C(O)C1OC=2C(=[O+]C=3C(C2)=C(O)C=C(O)C3)C4=CC(O)=C(O)C(O)=C4)COC(=O)/C=C/C5=CC=C(O)C=C5 '
               'NAME: Delphinidin 3-(6-p-coumaroylgalactoside) REASON: WRONGLY '
               'CLASSIFIED Contains o-diphenol (catechol) moiety on a '
               'six-membered aromatic ring\n'
               ' * SMILES: COc1cc(cc(O)c1O)-c1cc(=O)c2c(O)cc(O)cc2o1 NAME: '
               "3'-O-methyltricetin REASON: WRONGLY CLASSIFIED Contains "
               'o-diphenol (catechol) moiety on a six-membered aromatic ring\n'
               ' * SMILES: '
               'O1[C@@H](OC=2C=3CC[C@H](OC3C=C(O)C2)C4=CC(O)=C(O)C=C4)C(O)[C@@H](O)[C@H](O)C1 '
               'NAME: Viscutin 3 REASON: WRONGLY CLASSIFIED Contains '
               'o-diphenol (catechol) moiety on a six-membered aromatic ring\n'
               ' * SMILES: O=C1O[C@@H]([C@@H](O)C=2C1=C(O)C(O)=CC2)C NAME: '
               'Asperochrin F REASON: WRONGLY CLASSIFIED Contains o-diphenol '
               '(catechol) moiety on a six-membered aromatic ring\n'
               ' * SMILES: O=C(CC1=C(C(OC)=C(O)C(=C1)O)C=O)C NAME: Reticulone '
               'REASON: WRONGLY CLASSIFIED Contains o-diphenol (catechol) '
               'moiety on a six-membered aromatic ring\n'
               ' * SMILES: '
               'Oc1cc(cc(O)c1O)C1CCc2c(O)cc(OC(=O)c3cc(O)c(O)c(O)c3)cc2O1 '
               'NAME: 7-O-galloyltricetiflavan REASON: WRONGLY CLASSIFIED '
               'Contains o-diphenol (catechol) moiety on a six-membered '
               'aromatic ring\n'
               ' * SMILES: '
               'O1[C@@H](CC(=O)C2=C1C(O)=C(O)C=C2O)C3=CC(CC=C(C)C)=C(O)C=C3 '
               'NAME: Flowerone REASON: WRONGLY CLASSIFIED Contains o-diphenol '
               '(catechol) moiety on a six-membered aromatic ring\n'
               ' * SMILES: '
               'O=C1C2=C(C(O)=C(O)C=C2OC=C1C3=C(C=4OC5=C(C(=C(O)C(=C5)O)C(=O)O)C(C4C=C3C(=O)C)=O)C(=O)C)C(=O)O '
               'NAME: Vinaxanthone REASON: WRONGLY CLASSIFIED Contains '
               'o-diphenol (catechol) moiety on a six-membered aromatic ring\n'
               ' * SMILES: '
               'OC[C@H]1O[C@@H](Oc2cc(O)c3C(=O)C(Oc3c2)=Cc2cc(O)c(O)c(O)c2)[C@H](O)[C@@H](O)[C@@H]1O '
               'NAME: bracteatin 6-O-beta-glucoside REASON: WRONGLY CLASSIFIED '
               'Contains o-diphenol (catechol) moiety on a six-membered '
               'aromatic ring\n'
               ' * SMILES: O=C1OCC=2C=C(OC)C(=C(C2C=3C1=C(O)C=C(OC)C3)O)O '
               'NAME: Ulocladol REASON: WRONGLY CLASSIFIED Contains o-diphenol '
               '(catechol) moiety on a six-membered aromatic ring\n'
               ' * SMILES: '
               '[H][C@]12C[C@H](C)[C@@H](CO[C@@H]3O[C@H](COC(=O)\\C=C\\c4ccc(O)c(O)c4)[C@@H](O)[C@H](O)[C@H]3O)[C@@]1([H])[C@H](CO)C(=O)O2 '
               "NAME: gelsemiol-6'-trans-caffeoyl-1-glucoside REASON: WRONGLY "
               'CLASSIFIED Contains o-diphenol (catechol) moiety on a '
               'six-membered aromatic ring\n'
               ' * SMILES: '
               'O1[C@@H]([C@@H](O)C(OC(=O)/C=C/C2=CC=C(O)C=C2)C(O)[C@@H]1OC3=C(OC=4C(C3=O)=C(O)C=C(O)C4)C5=CC(O)=C(O)C=C5)COC(=O)/C=C/C6=CC=C(O)C=C6 '
               "NAME: Quercetin 3-(3'',6''-di-p-coumarylglucoside) REASON: "
               'WRONGLY CLASSIFIED Contains o-diphenol (catechol) moiety on a '
               'six-membered aromatic ring\n'
               ' * SMILES: O=C1C2=C(OC(=C1)C)C3=C(C(O)=C(O)C=C3OC2)C(=O)O '
               'NAME: Citromycetin REASON: WRONGLY CLASSIFIED Contains '
               'o-diphenol (catechol) moiety on a six-membered aromatic ring\n'
               ' * SMILES: C1=CC(=C(C=C1C=CC(=O)C2=C(C=C(C=C2)O)O)O)O NAME: '
               '1-(2,4-dihydroxyphenyl)-3-(3,4-dihydroxyphenyl)-2-propen-1-one '
               'REASON: WRONGLY CLASSIFIED Contains o-diphenol (catechol) '
               'moiety on a six-membered aromatic ring\n'
               ' * SMILES: '
               'O1C([C@@H](O)C(O)C(O)[C@@H]1OC2=C(OC=3C(C2=O)=C(O)C=C(O)C3)C=4C=C(OC)C(O)=C(O)C4)CO[C@@H]5OC([C@H](O)[C@H](O)C5O)C '
               'NAME: Laricitrin 3-rutinoside REASON: WRONGLY CLASSIFIED '
               'Contains o-diphenol (catechol) moiety on a six-membered '
               'aromatic ring\n'
               ' * SMILES: O=C1OC2=C(C(=CC(=C2)O)C)OC3=C1C(=CC(=C3O)O)C NAME: '
               'Botryorhodine E REASON: WRONGLY CLASSIFIED Contains o-diphenol '
               '(catechol) moiety on a six-membered aromatic ring\n'
               'False negatives: SMILES: O[C@H]1C=CC=C[C@H]1O NAME: '
               'cis-cyclohexa-3,5-diene-1,2-diol REASON: MISSED No adjacent '
               'qualifying hydroxyl substituents found on a six-membered '
               'aromatic ring\n'
               ' * SMILES: '
               'CCCCC(=O)c1c(O)cc(O)cc1O[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O '
               'NAME: 1-[(pentanoyl)-phloroglucinyl]-beta-D-glucopyranoside '
               'REASON: MISSED No adjacent qualifying hydroxyl substituents '
               'found on a six-membered aromatic ring\n'
               ' * SMILES: O[C@H]1C=CC=C[C@@H]1O NAME: '
               '(1S,2S)-cyclohexa-3,5-diene-1,2-diol REASON: MISSED No '
               'adjacent qualifying hydroxyl substituents found on a '
               'six-membered aromatic ring\n'
               ' * SMILES: O(C)C1=C(O)C=CC(C(O)CNC)=C1 NAME: Metanephrine '
               'REASON: MISSED No adjacent qualifying hydroxyl substituents '
               'found on a six-membered aromatic ring\n'
               ' * SMILES: '
               'C=1(C=C(C=C(C1)O)CCCCC(O[C@H]2[C@@H]([C@H]([C@@H]([C@H](O2)C(O)=O)O)O)O)=O)O '
               "NAME: 5-(3',5'-dihydroxyphenyl)-valeric acid-O-glucuronide "
               'REASON: MISSED No adjacent qualifying hydroxyl substituents '
               'found on a six-membered aromatic ring\n'
               ' * SMILES: Oc1cccc(O)c1S(O)(=O)=O NAME: '
               '2,6-dihydroxybenzenesulfonic acid REASON: MISSED No adjacent '
               'qualifying hydroxyl substituents found on a six-membered '
               'aromatic ring\n'
               ' * SMILES: C=1(C=C(C(=CC1)O)OC)C(O)CN NAME: Normetanephrine '
               'REASON: MISSED No adjacent qualifying hydroxyl substituents '
               'found on a six-membered aromatic ring\n'
               ' * SMILES: Oc1ccc(O)c(c1)S(O)(=O)=O NAME: '
               '2,5-dihydroxybenzenesulfonic acid REASON: MISSED No adjacent '
               'qualifying hydroxyl substituents found on a six-membered '
               'aromatic ring\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'O=C(N[C@@H](C(O)(C)C)C)[C@H]([C@@]1([C@@]2([C@@](CC1)(/C(/CCC2)=C/C=C\\3/C[C@@H](O)C[C@H](O)C3=C)[H])C)[H])C',
                                     'name': '1alpha,25-dihydroxy-24-oxo-23-azavitamin '
                                             'D2 / '
                                             '1alpha,25-dihydroxy-24-oxo-23-azaergocalciferol',
                                     'reason': 'No adjacent qualifying '
                                               'hydroxyl substituents found on '
                                               'an isolated six-membered ring'},
                                 {   'smiles': 'CCCCCCCCCCCCCCCCCCC(O)C([O-])=O',
                                     'name': '2-hydroxyarachidate',
                                     'reason': 'No adjacent qualifying '
                                               'hydroxyl substituents found on '
                                               'an isolated six-membered ring'},
                                 {   'smiles': 'C[C@@H](CN([C@@H](C)CO)C(=O)NC1=CC=C(C=C1)C(F)(F)F)[C@@H](CN(C)C(=O)C2CCOCC2)OC',
                                     'name': 'N-[(2S,3S)-4-[[(2S)-1-hydroxypropan-2-yl]-[[4-(trifluoromethyl)phenyl]carbamoyl]amino]-2-methoxy-3-methylbutyl]-N-methyloxane-4-carboxamide',
                                     'reason': 'No adjacent qualifying '
                                               'hydroxyl substituents found on '
                                               'an isolated six-membered ring'},
                                 {   'smiles': 'CC(=O)CC\\C=C(/C)CCC=C(C)C',
                                     'name': 'geranyl acetone',
                                     'reason': 'No adjacent qualifying '
                                               'hydroxyl substituents found on '
                                               'an isolated six-membered ring'},
                                 {   'smiles': 'O([C@H]1[C@H](O)[C@H](O[C@H](O)[C@H]1O)CO[C@H]2O[C@@H]([C@@H](O)[C@H](O)[C@@H]2O)CO)[C@H]3O[C@@H]([C@@H](O)[C@H](O)[C@@H]3O[C@H]4O[C@@H]([C@@H](O)[C@H](O)[C@@H]4O)CO)CO',
                                     'name': '(2S,3S,4S,5S,6R)-2-[[(2R,3R,4S,5S,6S)-4-[(2R,3S,4S,5S,6R)-4,5-Dihydroxy-6-(hydroxymethyl)-3-[(2R,3S,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-3,5,6-trihydroxyoxan-2-yl]methoxy]-6-(hydroxymethyl)oxane-3,4,5-triol',
                                     'reason': 'No adjacent qualifying '
                                               'hydroxyl substituents found on '
                                               'an isolated six-membered ring'},
                                 {   'smiles': 'O=C(OC1=C(C(O)=C(C(=O)O)C(=C1C)C)C)C2=C(OC)C(=C(OC(=O)C3=C(O)C=C(O)C=C3C)C=C2C)C',
                                     'name': 'Thielavin Z5',
                                     'reason': 'No adjacent qualifying '
                                               'hydroxyl substituents found on '
                                               'an isolated six-membered ring'},
                                 {   'smiles': '[C@@H]1([C@@H]([C@H]([C@@H]([C@H](O1)CO)O)O)NC(C)=O)O[C@@H]2[C@@H]([C@H](C(O[C@@H]2CO)O)O)O',
                                     'name': 'beta-D-GlcpNAc-(1->4)-D-Galp',
                                     'reason': 'No adjacent qualifying '
                                               'hydroxyl substituents found on '
                                               'an isolated six-membered ring'},
                                 {   'smiles': 'CN(C)C(=O)C1=CC=C(C=C1)C2=CC=C(C=C2)[C@@H]3[C@H]4CN(CC(=O)N4[C@H]3CO)C(=O)CC5CC5',
                                     'name': '4-[4-[(6S,7R,8R)-4-(2-cyclopropyl-1-oxoethyl)-8-(hydroxymethyl)-2-oxo-1,4-diazabicyclo[4.2.0]octan-7-yl]phenyl]-N,N-dimethylbenzamide',
                                     'reason': 'No adjacent qualifying '
                                               'hydroxyl substituents found on '
                                               'an isolated six-membered ring'},
                                 {   'smiles': 'CCCCCCCCCCCCCCCCCCCCC=C',
                                     'name': '1-docosene',
                                     'reason': 'No adjacent qualifying '
                                               'hydroxyl substituents found on '
                                               'an isolated six-membered ring'},
                                 {   'smiles': 'C([C@@](OC(=O)CCC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)([H])COC(=O)CC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)OC(=O)CCCCC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC',
                                     'name': 'TG(22:5(7Z,10Z,13Z,16Z,19Z)/20:5(5Z,8Z,11Z,14Z,17Z)/22:6(4Z,7Z,10Z,13Z,16Z,19Z))[iso6]',
                                     'reason': 'No adjacent qualifying '
                                               'hydroxyl substituents found on '
                                               'an isolated six-membered '
                                               'ring'}],
    'sample_false_negatives': [   {   'smiles': 'COc1cc(-c2ccc(O)cc2)c(OC)c2oc3cc(O)c(O)cc3c12',
                                      'name': 'candidusin A',
                                      'reason': 'No adjacent qualifying '
                                                'hydroxyl substituents found '
                                                'on an isolated six-membered '
                                                'ring'},
                                  {   'smiles': 'COC1OC(C)=Cc2oc3cc(O)c(O)c(C(O)=O)c3c(=O)c12',
                                      'name': '7,8-dihydroxy-1-methoxy-3-methyl-10-oxo-1H,10H-pyrano[4,3-b]chromene-9-carboxylic '
                                              'acid',
                                      'reason': 'No adjacent qualifying '
                                                'hydroxyl substituents found '
                                                'on an isolated six-membered '
                                                'ring'},
                                  {   'smiles': 'Oc1ccc-2c(OCC(=O)Cc3cc(O)c(O)cc-23)c1',
                                      'name': 'protosappanin A',
                                      'reason': 'No adjacent qualifying '
                                                'hydroxyl substituents found '
                                                'on an isolated six-membered '
                                                'ring'},
                                  {   'smiles': 'CC\\C=C1/OC(=O)c2c1cc(O)c(O)c2C',
                                      'name': 'purpurester B',
                                      'reason': 'No adjacent qualifying '
                                                'hydroxyl substituents found '
                                                'on an isolated six-membered '
                                                'ring'},
                                  {   'smiles': '[H][C@]12CC[C@]3(C)C(=O)CC[C@@]3([H])[C@]1([H])CCc1cc(O)c(O)cc21',
                                      'name': '2-hydroxyestrone',
                                      'reason': 'No adjacent qualifying '
                                                'hydroxyl substituents found '
                                                'on an isolated six-membered '
                                                'ring'},
                                  {   'smiles': 'Oc1cc2CCCN(Cc2cc1O)C(=S)NCCc1ccc(Cl)cc1',
                                      'name': 'capsazepine',
                                      'reason': 'No adjacent qualifying '
                                                'hydroxyl substituents found '
                                                'on an isolated six-membered '
                                                'ring'},
                                  {   'smiles': 'C1CNCC(C2=C1C=C(C(=C2)O)O)C3=CC=CC=C3',
                                      'name': '1-phenyl-2,3,4,5-tetrahydro-1H-3-benzazepine-7,8-diol',
                                      'reason': 'No adjacent qualifying '
                                                'hydroxyl substituents found '
                                                'on an isolated six-membered '
                                                'ring'},
                                  {   'smiles': 'CCCCC(=O)c1c(O)cc(O)cc1O[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O',
                                      'name': '1-[(pentanoyl)-phloroglucinyl]-beta-D-glucopyranoside',
                                      'reason': 'No adjacent qualifying '
                                                'hydroxyl substituents found '
                                                'on an isolated six-membered '
                                                'ring'},
                                  {   'smiles': 'C1CC([C@]2([C@](C1)(C3=C(CC2)C=C(C(=C3O)O)C(C)C)C(=O)O)[H])(C)C',
                                      'name': 'carnosic acid',
                                      'reason': 'No adjacent qualifying '
                                                'hydroxyl substituents found '
                                                'on an isolated six-membered '
                                                'ring'},
                                  {   'smiles': 'C1=C(C(C)C)C(=C(C2=C1C(C[C@@]3([C@@]2(CCCC3(C)C)C)[H])=O)O)O',
                                      'name': '11-hydroxysugiol',
                                      'reason': 'No adjacent qualifying '
                                                'hydroxyl substituents found '
                                                'on an isolated six-membered '
                                                'ring'}],
    'attempt': 4,
    'reasoning': 'Below is our improved solution. In our reasoning we noticed '
                 'that the previous algorithm simply iterated over every '
                 'aromatic bond and looked for qualifying oxygens. That led to '
                 'two kinds of mistakes. On the one hand, many polyphenolic '
                 'compounds (for example, flavonoids with multiple, fused '
                 'rings) were being “flagged” as catechols even though the '
                 'catechol‐style moiety was part of a fused ring system. On '
                 'the other hand, compounds that are drawn with non‐aromatic '
                 '(but conjugated) six‐membered rings (for example, the '
                 'cis‐cyclohexa‑3,5‑diene‑1,2‑diol) were being missed. \n'
                 '\n'
                 'To address these problems we now do the following:\n'
                 ' \n'
                 '1. We iterate over all six‐membered rings in the '
                 'molecule.  \n'
                 '2. We exclude “fused” rings (i.e. if any atom in the '
                 'candidate ring is also a member of another ring – as happens '
                 'in polyphenols). This generally selects only isolated '
                 'benzene‐like rings (or six‐membered conjugated rings) which '
                 'are the hallmark of simple catechols.  \n'
                 '3. For each candidate ring we “order” its atoms by following '
                 'bonds that appear in that ring. Then for each ring bond '
                 '(i.e. for each pair of adjacent ring atoms) we check whether '
                 'both atoms have a qualifying oxygen substituent. In our '
                 'helper we require that the oxygen be bound by a single bond '
                 'and not further connected to a carbon.  \n'
                 '4. Finally, we accept the candidate ring if it is either '
                 'aromatic (as determined by RDKit) OR if it is non‐aromatic '
                 'but shows at least two double bonds (i.e. it is conjugated '
                 'enough to be considered “catechol‐like”).  \n'
                 '\n'
                 'This approach is an attempt to approximately mimic the '
                 'chemical “intuition” needed for such classification.\n'
                 '\n'
                 'Below is the complete Python code.\n'
                 '\n'
                 '------------------------------------------------',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 296,
    'num_false_positives': 1971,
    'num_true_negatives': 140004,
    'num_false_negatives': 29,
    'num_negatives': None,
    'precision': 0.1305690339655933,
    'recall': 0.9107692307692308,
    'f1': 0.22839506172839505,
    'accuracy': 0.9859451862262825,
    'negative_predictive_value': 0.9997929059578814}