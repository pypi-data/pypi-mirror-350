"""
Classifies: CHEBI:18310 alkane
"""
"""
Classifies: CHEBI:18310 alkane
"""
from rdkit import Chem

def is_alkane(smiles: str):
    """
    Determines if a molecule is an alkane based on its SMILES string.
    An alkane is an acyclic, fully saturated hydrocarbon with the general formula CnH2n+2.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is an alkane, False otherwise
        str: Reason for classification
    """
    
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for rings
    if mol.GetRingInfo().NumRings() > 0:
        return False, "Molecule contains rings"

    # Check for non-carbon and non-hydrogen atoms
    for atom in mol.GetAtoms():
        if atom.GetAtomicNum() not in [1, 6]:  # Only allow H (1) and C (6)
            return False, "Molecule contains non-carbon and non-hydrogen atoms"

    # Check for unsaturation (double or triple bonds)
    if any(bond.GetBondType() not in [Chem.BondType.SINGLE] for bond in mol.GetBonds()):
        return False, "Molecule contains double or triple bonds"

    # Calculate the total number of hydrogens (explicit + implicit)
    h_count = 0
    for atom in mol.GetAtoms():
        h_count += atom.GetTotalNumHs()  # This includes implicit hydrogens

    # Check the general formula CnH2n+2
    c_count = sum(1 for atom in mol.GetAtoms() if atom.GetAtomicNum() == 6)
    
    if h_count != 2 * c_count + 2:
        return False, f"Molecule does not follow the general formula CnH2n+2 (C{c_count}H{h_count})"

    return True, "Molecule is an acyclic, fully saturated hydrocarbon following the general formula CnH2n+2"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:18310',
                          'name': 'alkane',
                          'definition': 'An acyclic branched or unbranched '
                                        'hydrocarbon having the general '
                                        'formula CnH2n+2, and therefore '
                                        'consisting entirely of hydrogen atoms '
                                        'and saturated carbon atoms.',
                          'parents': ['CHEBI:24632', 'CHEBI:33653'],
                          'xrefs': ['KEGG:C01371'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 32,
                           'log_lines_of_code': 3.4657359027997265,
                           'indent_by_line': [   1,
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
                                                 1,
                                                 1,
                                                 2,
                                                 0,
                                                 1,
                                                 1,
                                                 2,
                                                 0,
                                                 1,
                                                 1,
                                                 2,
                                                 3,
                                                 0,
                                                 1,
                                                 1,
                                                 2,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 0,
                                                 1],
                           'max_indent': 3,
                           'imports': ['from rdkit import Chem'],
                           'imports_count': 1,
                           'methods_called': [   'GetTotalNumHs',
                                                 'GetRingInfo',
                                                 'GetAtoms',
                                                 'GetBonds',
                                                 'NumRings',
                                                 'GetAtomicNum',
                                                 'MolFromSmiles',
                                                 'GetBondType'],
                           'methods_called_count': 8,
                           'smarts_strings': [],
                           'smarts_strings_count': 0,
                           'defs': ['is_alkane(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "Molecule contains rings"',
                                          'False, "Molecule contains '
                                          'non-carbon and non-hydrogen atoms"',
                                          'False, "Molecule contains double or '
                                          'triple bonds"',
                                          'False, f"Molecule does not follow '
                                          'the general formula CnH2n+2 '
                                          '(C{c_count}H{h_count})"',
                                          'True, "Molecule is an acyclic, '
                                          'fully saturated hydrocarbon '
                                          'following the general formula '
                                          'CnH2n+2"'],
                           'returns_count': 6,
                           'complexity': 4.293147180559945},
    'message': '\n'
               'Attempt failed: F1 score of 0 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: NONE\n'
               'False positives: NONE\n'
               'False negatives: SMILES: '
               'C(C(C(C)C)C)(CCCCCCCCCCCCCCCCCCCCCCCCCC)C NAME: '
               '2,3,4-Trimethyltriacontane REASON: MISSED Molecule does not '
               'follow the general formula CnH2n+2 (C33H0)\n'
               ' * SMILES: CCCCCCCCCCCC(C)C NAME: 2-methyltridecane REASON: '
               'MISSED Molecule does not follow the general formula CnH2n+2 '
               '(C14H0)\n'
               ' * SMILES: C(CCCCCCCCC)CCCCC(C)C NAME: 2-methyl-Hexadecane '
               'REASON: MISSED Molecule does not follow the general formula '
               'CnH2n+2 (C17H0)\n'
               ' * SMILES: CC(CC(C)(C)C)CC(C)(C)C NAME: '
               '2,2,4,6,6-pentamethylheptane REASON: MISSED Molecule does not '
               'follow the general formula CnH2n+2 (C12H0)\n'
               ' * SMILES: C(CC(C)C)(CCCCCC)C NAME: Decane, 2,4-dimethyl- '
               'REASON: MISSED Molecule does not follow the general formula '
               'CnH2n+2 (C12H0)\n'
               ' * SMILES: CCCC(C)CC(C)CC NAME: 3,5-dimethyloctane REASON: '
               'MISSED Molecule does not follow the general formula CnH2n+2 '
               '(C10H0)\n'
               ' * SMILES: CCCCC(C)CC NAME: 3-Methylheptane REASON: MISSED '
               'Molecule does not follow the general formula CnH2n+2 (C8H0)\n'
               ' * SMILES: CCC(CC)CC NAME: 3-ethylpentane REASON: MISSED '
               'Molecule does not follow the general formula CnH2n+2 (C7H0)\n'
               ' * SMILES: C(CCCCCCCCCCCC)(CCCCCCCCCCC)C NAME: '
               '12-Methyltetracosane REASON: MISSED Molecule does not follow '
               'the general formula CnH2n+2 (C25H0)\n'
               ' * SMILES: C(CC(CC)C)(C)(C)C NAME: 2,2,4-Trimethylhexane '
               'REASON: MISSED Molecule does not follow the general formula '
               'CnH2n+2 (C9H0)\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'C1COCCN1C2=C(C=C(C=C2)C(F)(F)F)NC(=O)C3=CC(=CN=C3)Br',
                                     'name': '5-bromo-N-[2-(4-morpholinyl)-5-(trifluoromethyl)phenyl]-3-pyridinecarboxamide',
                                     'reason': 'Molecule contains rings'},
                                 {   'smiles': 'C[C@H]1C[C@@H]2CC[C@@H](O2)[C@@H](C)C(=O)O[C@H](C)C[C@H]2CC[C@H](O2)[C@H](C)C(=O)O[C@@H](C)C[C@@H]2CC[C@@H](O2)[C@@H](C)C(=O)O[C@H](C)C[C@H]2CC[C@H](O2)[C@H](C)C(=O)O1',
                                     'name': 'Nonactin',
                                     'reason': 'Molecule contains rings'},
                                 {   'smiles': 'O1OC23C(C14C(C5C(C(CC5)C(CCC(C(C)C)C)C)(CC4)C)=CC2=O)(CCC(O)C3)C',
                                     'name': '5,9-Epidioxy-3-hydroxyergost-7-en-6-one',
                                     'reason': 'Molecule contains rings'},
                                 {   'smiles': 'CC1=C(SC=C1)C(=O)N2CCCC(C2)CNS(=O)(=O)C3=CC=C(C=C3)OC',
                                     'name': '4-methoxy-N-[[1-[(3-methyl-2-thiophenyl)-oxomethyl]-3-piperidinyl]methyl]benzenesulfonamide',
                                     'reason': 'Molecule contains rings'},
                                 {   'smiles': 'O(C(=O)CCCCCCCCCCCCCCC)C[C@@H](O)COC(=O)CCCCCCCCC/C=C\\CCCCCCCC',
                                     'name': 'DG(16:0/0:0/20:1n9)',
                                     'reason': 'Molecule contains non-carbon '
                                               'and non-hydrogen atoms'},
                                 {   'smiles': 'Oc1cc2CC3(O)COc4c(O)c(O)ccc4C3c2cc1O',
                                     'name': 'haematoxylin',
                                     'reason': 'Molecule contains rings'},
                                 {   'smiles': 'O([C@@H]1[C@H](O)[C@H](O[C@H]2[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]2CO)O[C@H]3[C@H](O)[C@@H](NC(=O)C)C(O[C@@H]3CO)O)O[C@@H]([C@H]1O)CO[C@H]4O[C@@H]([C@@H](O)[C@H](O[C@H]5O[C@@H]([C@@H](O)[C@H](O)[C@@H]5O)CO)[C@@H]4O)CO[C@H]6O[C@@H]([C@@H](O)[C@H](O)[C@@H]6O[C@H]7O[C@@H]([C@@H](O)[C@H](O)[C@@H]7O)CO)CO)[C@H]8O[C@@H]([C@@H](O)[C@H](O)[C@@H]8O[C@@H]9O[C@@H]([C@@H](O[C@@H]%10O[C@@H]([C@H](O)[C@H](O)[C@H]%10O)CO)[C@H](O)[C@H]9NC(=O)C)CO)CO',
                                     'name': 'N-[(3R,4R,5S,6R)-5-[(2S,3R,4R,5S,6R)-3-Acetamido-5-[(2S,3S,4S,5R,6R)-4-[(2R,3S,4S,5S,6R)-3-[(2S,3R,4R,5S,6R)-3-acetamido-4-hydroxy-6-(hydroxymethyl)-5-[(2S,3R,4S,5R,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-6-[[(2S,3S,4S,5R,6R)-6-[[(2S,3S,4S,5S,6R)-4,5-dihydroxy-6-(hydroxymethyl)-3-[(2R,3S,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxymethyl]-3,5-dihydroxy-4-[(2R,3S,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxymethyl]-3,5-dihydroxyoxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-2,4-dihydroxy-6-(hydroxymethyl)oxan-3-yl]acetamide',
                                     'reason': 'Molecule contains rings'},
                                 {   'smiles': 'O([C@@H]1[C@H](O)[C@@H](O)[C@@H](O[C@@H]1CO)O)[C@@H]2O[C@@H]([C@@H](O)[C@H](O)[C@H]2O)CO',
                                     'name': 'beta-D-Glcp-(1->4)-beta-D-Galp',
                                     'reason': 'Molecule contains rings'},
                                 {   'smiles': 'O=C(N)C(/C=C/[N+]([O-])=NC(C(O)C)C)CCC',
                                     'name': 'Maniwamycin F',
                                     'reason': 'Molecule contains non-carbon '
                                               'and non-hydrogen atoms'},
                                 {   'smiles': 'O1C2=C(C(=O)C(C3=C(O)C=C(O)C=C3)=C1)C(OC)=CC(O)=C2',
                                     'name': 'Barpisoflavone A',
                                     'reason': 'Molecule contains rings'}],
    'sample_false_negatives': [   {   'smiles': 'C(CCCCCCCC(=O)O)CCCCCCCCC(=O)O',
                                      'name': 'octadecanedioic acid',
                                      'reason': 'Molecule contains non-carbon '
                                                'and non-hydrogen atoms'}],
    'attempt': 1,
    'reasoning': 'The previous code failed because it incorrectly calculated '
                 'the hydrogen count (`h_count`) from the SMILES string. In '
                 'SMILES, hydrogen atoms are often implicit (not explicitly '
                 'written), so counting them directly from the SMILES string '
                 'will not give the correct number of hydrogens. Instead, we '
                 "need to use RDKit's functionality to calculate the total "
                 'number of hydrogens for each atom, including implicit '
                 'hydrogens.\n'
                 '\n'
                 'Here’s the improved version of the code:',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 110,
    'num_false_positives': 3,
    'num_true_negatives': 142186,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.9734513274336283,
    'recall': 0.990990990990991,
    'f1': 0.9821428571428571,
    'accuracy': 0.9999718903724526,
    'negative_predictive_value': 0.9999929670082356}