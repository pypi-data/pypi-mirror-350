"""
Classifies: CHEBI:65061 2,5-diketopiperazines
"""
"""
Classifies: 2,5-diketopiperazines (any piperazinone that has a piperazine-2,5-dione skeleton)

This module defines a function is_2_5_diketopiperazines that determines whether a molecule,
given by its SMILES string, contains a 2,5-diketopiperazine core. The core is defined by the pattern:
    N - C(=O) - C - N - C(=O) - C
arranged as a six-membered ring.
"""

from rdkit import Chem

def has_carbonyl(mol, atom):
    """
    Check if the specified carbon atom is part of a carbonyl group.
    That is, does it have at least one neighboring oxygen connected by a double bond?

    Args:
        mol (rdkit.Chem.Mol): The molecule to which the atom belongs.
        atom (rdkit.Chem.Atom): The atom to check.

    Returns:
        bool: True if a double-bonded oxygen is found, False otherwise.
    """
    if atom.GetSymbol() != "C":
        return False
    # Loop through all neighbors of the atom
    for neighbor in atom.GetNeighbors():
        # Get the bond between the two atoms via the molecule
        bond = mol.GetBondBetweenAtoms(atom.GetIdx(), neighbor.GetIdx())
        if neighbor.GetSymbol() == "O" and bond and bond.GetBondType() == Chem.rdchem.BondType.DOUBLE:
            return True
    return False

def check_ring_pattern(mol, atoms):
    """
    Given a list of 6 atoms in order around a ring, check if they match the pattern:
    [N, C(=O), C (non-carbonyl), N, C(=O), C (non-carbonyl)].

    Args:
        mol (rdkit.Chem.Mol): The molecule.
        atoms (list of rdkit.Chem.Atom): List of atoms in the ring (ordered).

    Returns:
        bool: True if the atoms match the desired pattern, False otherwise.
    """
    # Position 0: Must be nitrogen
    if atoms[0].GetSymbol() != "N":
        return False
    # Position 1: Must be a carbonyl carbon (C with a double-bonded oxygen)
    if not (atoms[1].GetSymbol() == "C" and has_carbonyl(mol, atoms[1])):
        return False
    # Position 2: Must be a carbon that is not a carbonyl
    if atoms[2].GetSymbol() != "C" or has_carbonyl(mol, atoms[2]):
        return False
    # Position 3: Must be nitrogen
    if atoms[3].GetSymbol() != "N":
        return False
    # Position 4: Must be a carbonyl carbon
    if not (atoms[4].GetSymbol() == "C" and has_carbonyl(mol, atoms[4])):
        return False
    # Position 5: Must be a carbon that is not a carbonyl
    if atoms[5].GetSymbol() != "C" or has_carbonyl(mol, atoms[5]):
        return False
    return True

def is_2_5_diketopiperazines(smiles: str):
    """
    Determines if a molecule is a 2,5-diketopiperazine based on its SMILES string.
    A 2,5-diketopiperazine has a six-membered ring with the connectivity:
        N - C(=O) - C - N - C(=O) - C,
    where the two carbons in positions 1 and 4 are carbonyl centers (i.e., have a double-bonded oxygen).

    The function checks all six-membered rings in the molecule and all rotations (and their reversals)
    to see if one of them matches the specified pattern.

    Args:
        smiles (str): SMILES string of the molecule.

    Returns:
        bool: True if the molecule has a 2,5-diketopiperazine skeleton, False otherwise.
        str: Explanation of the classification.
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
    
    ring_info = mol.GetRingInfo()
    atom_rings = ring_info.AtomRings()  # Tuples of atom indices forming rings.
    
    # Check each six-membered ring for the 2,5-diketopiperazine pattern.
    for ring in atom_rings:
        if len(ring) != 6:
            continue  # Only interested in six-membered rings.
        ring_atoms = [mol.GetAtomWithIdx(idx) for idx in ring]
        # Because the ring is cyclic, test all cyclic rotations and their reverse orders.
        for start in range(6):
            # Forward ordering
            forward = [ring_atoms[(start + i) % 6] for i in range(6)]
            if check_ring_pattern(mol, forward):
                return True, "Molecule contains a 2,5-diketopiperazine skeleton (ring indices: {})".format(ring)
            # Reverse ordering (to account for opposite direction around the ring)
            reverse = [ring_atoms[(start - i) % 6] for i in range(6)]
            if check_ring_pattern(mol, reverse):
                return True, "Molecule contains a 2,5-diketopiperazine skeleton (ring indices: {})".format(ring)
    
    return False, "Molecule does not contain the required piperazine-2,5-dione skeleton"

# Example usage (you can uncomment these lines to test a couple of cases):
# test_smiles = [
#     "O=C1CNC(=O)CN1",  # Simplest 2,5-diketopiperazine, expected: True
#     "CC1C(=O)NC(=O)N1",  # Not a six-membered ring as required, expected: False
# ]
# for smi in test_smiles:
#     result, reason = is_2_5_diketopiperazines(smi)
#     print(smi, result, reason)


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:65061',
                          'name': '2,5-diketopiperazines',
                          'definition': 'Any piperazinone that has a '
                                        'piperazine-2,5-dione skeleton.',
                          'parents': [   'CHEBI:24613',
                                         'CHEBI:46761',
                                         'CHEBI:46846'],
                          'xrefs': ['Wikipedia:Diketopiperazine'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 80,
                           'log_lines_of_code': 4.382026634673881,
                           'indent_by_line': [   1,
                                                 1,
                                                 1,
                                                 0,
                                                 1,
                                                 2,
                                                 2,
                                                 0,
                                                 1,
                                                 2,
                                                 1,
                                                 1,
                                                 2,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 1,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 0,
                                                 1,
                                                 2,
                                                 2,
                                                 0,
                                                 1,
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 1,
                                                 1,
                                                 2,
                                                 1,
                                                 1,
                                                 2,
                                                 1,
                                                 1,
                                                 2,
                                                 1,
                                                 1,
                                                 2,
                                                 1,
                                                 1,
                                                 2,
                                                 1,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 1,
                                                 0,
                                                 1,
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
                                                 1,
                                                 1,
                                                 2,
                                                 3,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 3,
                                                 3,
                                                 4,
                                                 3,
                                                 3,
                                                 3,
                                                 4,
                                                 1,
                                                 1,
                                                 0],
                           'max_indent': 4,
                           'imports': ['from rdkit import Chem'],
                           'imports_count': 1,
                           'methods_called': [   'GetBondType',
                                                 'AtomRings',
                                                 'GetSymbol',
                                                 'format',
                                                 'GetAtomWithIdx',
                                                 'GetNeighbors',
                                                 'GetBondBetweenAtoms',
                                                 'MolFromSmiles',
                                                 'GetRingInfo',
                                                 'GetIdx'],
                           'methods_called_count': 10,
                           'smarts_strings': [],
                           'smarts_strings_count': 0,
                           'defs': ['has_carbonyl(mol, atom):'],
                           'defs_count': 1,
                           'returns': [   'False',
                                          'True',
                                          'False',
                                          'False',
                                          'False',
                                          'False',
                                          'False',
                                          'False',
                                          'False',
                                          'True',
                                          'False, "Invalid SMILES string"',
                                          'True, "Molecule contains a '
                                          '2,5-diketopiperazine skeleton (ring '
                                          'indices: {})".format(ring)',
                                          'True, "Molecule contains a '
                                          '2,5-diketopiperazine skeleton (ring '
                                          'indices: {})".format(ring)',
                                          'False, "Molecule does not contain '
                                          'the required piperazine-2,5-dione '
                                          'skeleton"'],
                           'returns_count': 14,
                           'complexity': 6.676405326934775},
    'message': '\n'
               'Error: Error executing '
               "is_2_5_diketopiperazines('S1S[C@]23N([C@@H]4[C@@H](O)C=C[C@@H]([C@H]4C2)O)C([C@]15N([C@@H]6[C@@H](O)C=C[C@@H]([C@H]6C5)O)C3=O)=O'):\n"
               " 'Atom' object has no attribute 'GetBondBetweenAtoms'\n"
               'Attempt failed: F1 score of 0 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: NONE\n'
               'False positives: NONE\n'
               'False negatives: NONE\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'O1C2=C(O)C=C(COC)C=C2C[C@@H](C1(C)C)O',
                                     'name': 'Conoideochromane B',
                                     'reason': 'Molecule does not contain the '
                                               'required piperazine-2,5-dione '
                                               'skeleton'},
                                 {   'smiles': 'P(OC[C@H](OC(=O)CCCCCCC/C=C\\CCCCC)CO/C=C\\CCCCCCCCCCCCCC)(OCCN)(O)=O',
                                     'name': 'PE(P-16:0/15:1(9Z))',
                                     'reason': 'Molecule does not contain the '
                                               'required piperazine-2,5-dione '
                                               'skeleton'},
                                 {   'smiles': 'O=C1C=2C(OC(=C1)C)=C(C3=C4O[C@](O)(CC(C4=C(O)C=5C3=CC(OC)=CC5OC)=O)C)C6=CC(OC)=CC(=C6C2O)OC',
                                     'name': '2-hydroxydihydronigerone',
                                     'reason': 'Molecule does not contain the '
                                               'required piperazine-2,5-dione '
                                               'skeleton'},
                                 {   'smiles': 'O([C@@H]1[C@@H](NC(=O)C)[C@@H](O[C@@H]([C@H]1O)CO)OC[C@H]2O[C@@H](O)[C@H](NC(=O)C)[C@@H](O)[C@H]2O)[C@@H]3O[C@@H]([C@H](O)[C@H](O[C@H]4O[C@@H]([C@H](O)[C@H](O)[C@H]4O)CO)[C@H]3O)CO',
                                     'name': 'N-[(2R,3R,4R,5R,6R)-6-[[(2R,3R,4R,5S,6R)-3-Acetamido-4-[(2R,3R,4S,5S,6R)-3,5-dihydroxy-6-(hydroxymethyl)-4-[(2R,3R,4S,5R,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-5-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxymethyl]-2,4,5-trihydroxyoxan-3-yl]acetamide',
                                     'reason': 'Molecule does not contain the '
                                               'required piperazine-2,5-dione '
                                               'skeleton'},
                                 {   'smiles': 'O1C(C(O)C(O)C(O)C1OC=2C(O)=C(O)C=C(C2)C=O)COC(=O)C3=CC(O)=C(O)C(O)=C3',
                                     'name': 'Castamollissin',
                                     'reason': 'Molecule does not contain the '
                                               'required piperazine-2,5-dione '
                                               'skeleton'},
                                 {   'smiles': 'S(OC[C@H]1O[C@@H](OC[C@H]2O[C@@H](O[C@@H]([C@@H](O)[C@H](O)CO[C@]3(O[C@H]([C@H](NC(=O)C)[C@@H](O)C3)[C@H](O)[C@H](O)CO)C(O)=O)[C@@H](NC(=O)C)CO)[C@H](O)[C@@H](O)[C@H]2O)[C@H](NC(=O)C)[C@@H](O)[C@@H]1O[C@@H]4O[C@@H]([C@H](O)[C@H](O)[C@H]4O)CO[C@]5(O[C@H]([C@H](NC(=O)C)[C@@H](O)C5)[C@H](O)[C@H](O)CO)C(O)=O)(O)(=O)=O',
                                     'name': '(2R,4S,5R,6R)-5-Acetamido-2-[[(2R,3R,4S,5R,6S)-6-[(2R,3S,4R,5R,6R)-5-acetamido-6-[[(2R,3R,4S,5R,6R)-6-[(2S,3R,4S,5R)-2-acetamido-6-[(2R,4S,5R,6R)-5-acetamido-2-carboxy-4-hydroxy-6-[(1R,2R)-1,2,3-trihydroxypropyl]oxan-2-yl]oxy-1,4,5-trihydroxyhexan-3-yl]oxy-3,4,5-trihydroxyoxan-2-yl]methoxy]-4-hydroxy-2-(sulfooxymethyl)oxan-3-yl]oxy-3,4,5-trihydroxyoxan-2-yl]methoxy]-4-hydroxy-6-[(1R,2R)-1,2,3-trihydroxypropyl]oxane-2-carboxylic '
                                             'acid',
                                     'reason': 'Molecule does not contain the '
                                               'required piperazine-2,5-dione '
                                               'skeleton'},
                                 {   'smiles': 'FC(F)(F)C(F)(F)C(F)(F)C(F)(F)C(F)(F)C(F)(F)F',
                                     'name': 'perfluorohexane',
                                     'reason': 'Molecule does not contain the '
                                               'required piperazine-2,5-dione '
                                               'skeleton'},
                                 {   'smiles': 'CC(C)(O)CCC(=O)[C@](C)(O)[C@H]1[C@H](O)C[C@@]2(C)[C@@H]3CC=C4[C@@H](C[C@@H](O)[C@@H](O)C4(C)C)[C@]3(C)C(=O)C[C@]12C',
                                     'name': 'Cucurbitacin P',
                                     'reason': 'Molecule does not contain the '
                                               'required piperazine-2,5-dione '
                                               'skeleton'},
                                 {   'smiles': 'CCCCCCCc1cc(O)cc(=O)o1',
                                     'name': '4-hydroxy-6-heptylpyran-2-one',
                                     'reason': 'Molecule does not contain the '
                                               'required piperazine-2,5-dione '
                                               'skeleton'},
                                 {   'smiles': 'S(O[C@@H]1[C@@H](O)[C@H](O[C@H]2[C@H](O)[C@@H](NC(=O)C)[C@H](O[C@H]3[C@@H](O)[C@H](O[C@@H]4O[C@@H]([C@@H](O[C@@H]5O[C@@H]([C@H](O)[C@H](OS(O)(=O)=O)[C@H]5O)CO)[C@H](O)[C@H]4NC(=O)C)CO)[C@H](O[C@@H]3O[C@H]6[C@H](O)[C@H](O[C@@H](O[C@H]7[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]7CO)O[C@H]8[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]8CO[C@@H]9O[C@H]([C@@H](O)[C@@H](O)[C@@H]9O)C)O)[C@H]6O)CO[C@H]%10O[C@@H]([C@@H](O)[C@H](O)[C@@H]%10O[C@@H]%11O[C@@H]([C@@H](O[C@@H]%12O[C@@H]([C@H](O[C@@H]%13O[C@@H]([C@H](O)[C@H](O)[C@H]%13NC(=O)C)CO)[C@H](O[C@]%14(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%14)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%12O)CO)[C@H](O)[C@H]%11NC(=O)C)CO)CO[C@@H]%15O[C@@H]([C@@H](O[C@@H]%16O[C@@H]([C@H](O)[C@H](O[C@]%17(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%17)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%16O)CO)[C@H](O)[C@H]%15NC(=O)C)CO)CO)O[C@@H]2CO)O[C@@H]([C@@H]1O)CO)(O)(=O)=O',
                                     'name': 'CID 146017241',
                                     'reason': 'Molecule does not contain the '
                                               'required piperazine-2,5-dione '
                                               'skeleton'}],
    'sample_false_negatives': [],
    'attempt': 3,
    'reasoning': 'Below is our reasoning before showing the complete updated '
                 'code:\n'
                 '\n'
                 'One likely issue in the previous code was that the helper '
                 'function "has_carbonyl" was trying to call '
                 'GetBondBetweenAtoms on an atom instead of on the molecule. '
                 'In RDKit the GetBondBetweenAtoms method belongs to the '
                 'molecule class, not on an individual atom. To fix this, we '
                 'update has_carbonyl so that it accepts the molecule (or uses '
                 'atom.GetOwningMol() if available) and then calls '
                 'mol.GetBondBetweenAtoms with the indices of the two atoms. '
                 'We also update the check_ring_pattern function so that it '
                 'too receives the molecule for this purpose. Finally, we keep '
                 'the same logic for scanning over six‐membered rings and '
                 'testing all rotations (and their reverse orders) for the '
                 'pattern:\n'
                 '\u2003\u2003N – C(=O) – C – N – C(=O) – C\n'
                 '\n'
                 'Below is the complete Python code block that incorporates '
                 'these improvements:',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 53,
    'num_false_positives': 816,
    'num_true_negatives': 141431,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.06098964326812428,
    'recall': 1.0,
    'f1': 0.11496746203904555,
    'accuracy': 0.9942656359803232,
    'negative_predictive_value': 1.0}