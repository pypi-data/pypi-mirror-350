"""
Classifies: CHEBI:62499 methyl-branched fatty acid
"""
"""
Classifies: CHEBI:27718 Methyl-branched fatty acid
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_methyl_branched_fatty_acid(smiles: str):
    """
    Determines if a molecule is a methyl-branched fatty acid based on its SMILES string.
    A methyl-branched fatty acid is a branched-chain fatty acid containing methyl branches only.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a methyl-branched fatty acid, False otherwise
        str: Reason for classification
    """
    
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check if molecule contains only C, H, and O atoms
    allowed_atoms = [6, 1, 8]  # C, H, O
    if any(atom.GetAtomicNum() not in allowed_atoms for atom in mol.GetAtoms()):
        return False, "Molecule contains atoms other than C, H, and O"

    # Check for carboxylic acid group
    carboxyl_pattern = Chem.MolFromSmarts("C(=O)O")
    carboxyl_match = mol.GetSubstructMatch(carboxyl_pattern)
    if not carboxyl_match:
        return False, "No carboxylic acid group found"

    # Check for linear carbon chain
    linear_chain_pattern = Chem.MolFromSmarts("CC(C)CCCC")
    linear_chain_match = mol.GetSubstructMatches(linear_chain_pattern)
    if not linear_chain_match:
        return False, "No linear carbon chain found"

    # Check for methyl branches
    methyl_branch_pattern = Chem.MolFromSmarts("CC")
    methyl_branch_matches = mol.GetSubstructMatches(methyl_branch_pattern)
    if not methyl_branch_matches:
        return False, "No methyl branches found"

    # Check if all branches are methyl groups
    for match in methyl_branch_matches:
        atom = mol.GetAtomWithIdx(match[0])
        neighbors = [mol.GetAtomWithIdx(n.GetIdx()) for n in atom.GetNeighbors()]
        if any(n.GetAtomicNum() != 6 for n in neighbors):
            return False, "Found non-methyl branching groups"

    return True, "Contains a linear carbon chain with methyl branches and a carboxylic acid group"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:62499',
                          'name': 'methyl-branched fatty acid',
                          'definition': 'Any branched-chain fatty acid '
                                        'containing methyl branches only.',
                          'parents': ['CHEBI:35819'],
                          'xrefs': [   'PMID:17030019',
                                       'PMID:19747846',
                                       'PMID:19933331'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 39,
                           'log_lines_of_code': 3.6635616461296463,
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
                                                 1,
                                                 2,
                                                 0,
                                                 1,
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
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 0,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 0,
                                                 1],
                           'max_indent': 3,
                           'imports': [   'from rdkit import Chem',
                                          'from rdkit.Chem import AllChem'],
                           'imports_count': 2,
                           'methods_called': [   'GetSubstructMatches',
                                                 'MolFromSmarts',
                                                 'GetIdx',
                                                 'GetAtoms',
                                                 'GetSubstructMatch',
                                                 'GetNeighbors',
                                                 'GetAtomWithIdx',
                                                 'GetAtomicNum',
                                                 'MolFromSmiles'],
                           'methods_called_count': 9,
                           'smarts_strings': ['CC', 'CC(C)CCCC', 'C(=O)O'],
                           'smarts_strings_count': 3,
                           'defs': [   'is_methyl_branched_fatty_acid(smiles: '
                                       'str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "Molecule contains atoms '
                                          'other than C, H, and O"',
                                          'False, "No carboxylic acid group '
                                          'found"',
                                          'False, "No linear carbon chain '
                                          'found"',
                                          'False, "No methyl branches found"',
                                          'False, "Found non-methyl branching '
                                          'groups"',
                                          'True, "Contains a linear carbon '
                                          'chain with methyl branches and a '
                                          'carboxylic acid group"'],
                           'returns_count': 7,
                           'complexity': 4.732712329225929},
    'message': '\n'
               'Error: Error executing '
               "is_methyl_branched_fatty_acid('CCC\\\\C(=C/CC)C(O)=O'):\n"
               " 'Atom' object has no attribute 'GetDegreeWithPattern'\n"
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
    'sample_true_negatives': [   {   'smiles': 'CC1=CC=CC=C1S(=O)(=O)N[C@@H]2CC[C@@H](O[C@H]2CO)CCN3C=C(N=N3)C4=CC=C(C=C4)F',
                                     'name': 'N-[(2R,3R,6R)-6-[2-[4-(4-fluorophenyl)-1-triazolyl]ethyl]-2-(hydroxymethyl)-3-oxanyl]-2-methylbenzenesulfonamide',
                                     'reason': 'Molecule contains atoms other '
                                               'than C, H, and O'},
                                 {   'smiles': 'CC(=NNC(=O)C1=CC=CC=C1N)CC(=O)NC2=CC3=C(C=C2)OCO3',
                                     'name': '2-amino-N-[[4-(1,3-benzodioxol-5-ylamino)-4-oxobutan-2-ylidene]amino]benzamide',
                                     'reason': 'Molecule contains atoms other '
                                               'than C, H, and O'},
                                 {   'smiles': 'O=C(NS(CC=1C=CC=CC1C(OC)=O)(=O)=O)NC2=NC(=CC(=N2)OC)OC',
                                     'name': 'bensulfuron-methyl',
                                     'reason': 'Molecule contains atoms other '
                                               'than C, H, and O'},
                                 {   'smiles': '[H]C(C(=O)C(Cl)C(O)=O)=C(Cl)C(O)=O',
                                     'name': '2,5-dichloro-4-oxohex-2-enedioic '
                                             'acid',
                                     'reason': 'Molecule contains atoms other '
                                               'than C, H, and O'},
                                 {   'smiles': 'CC1(C)O[C@]2(C)CC[C@H]1C[C@H]2O',
                                     'name': '2-endo-hydroxy-1,8-cineole',
                                     'reason': 'No carboxylic acid group '
                                               'found'},
                                 {   'smiles': 'O=C1O[C@@H](C[C@H]2[C@@H]1[C@@H](O)CCC2)C',
                                     'name': '(3R,4aS,8S,8aR)-8-hydroxy-3-rnethyl-3,4,4a,5,6,7,8,8a-octahydro-1H-2-benzopyran-1-one',
                                     'reason': 'Found non-methyl branching '
                                               'groups'},
                                 {   'smiles': 'CCCCCCCCCCCCCC(C)=O',
                                     'name': '2-Pentadecanone',
                                     'reason': 'No carboxylic acid group '
                                               'found'},
                                 {   'smiles': 'O=C1C=2C(OC(=C1)C)=C(C3=C4O[C@](O)(CC(C4=C(O)C=5C3=CC(OC)=CC5OC)=O)C)C6=CC(OC)=CC(=C6C2O)OC',
                                     'name': '2-hydroxydihydronigerone',
                                     'reason': 'No carboxylic acid group '
                                               'found'},
                                 {   'smiles': 'C[C@H]1CN([C@@H](COC2=C(C=C(C=C2)NC(=O)C3CC3)C(=O)N(C[C@H]1OC)C)C)CC4=CC=CC=C4',
                                     'name': 'N-[(4R,7S,8S)-8-methoxy-4,7,10-trimethyl-11-oxo-5-(phenylmethyl)-2-oxa-5,10-diazabicyclo[10.4.0]hexadeca-1(12),13,15-trien-14-yl]cyclopropanecarboxamide',
                                     'reason': 'Molecule contains atoms other '
                                               'than C, H, and O'},
                                 {   'smiles': 'C[C@@H]1CN([C@@H](COC2=C(C=C(C=C2)NC(=O)C3CCCCC3)C(=O)N(C[C@@H]1OC)C)C)CC4=NC=CS4',
                                     'name': 'N-[(4R,7R,8R)-8-methoxy-4,7,10-trimethyl-11-oxo-5-(2-thiazolylmethyl)-2-oxa-5,10-diazabicyclo[10.4.0]hexadeca-1(12),13,15-trien-14-yl]cyclohexanecarboxamide',
                                     'reason': 'Molecule contains atoms other '
                                               'than C, H, and O'}],
    'sample_false_negatives': [   {   'smiles': 'CCC\\C(=C/CC)C(O)=O',
                                      'name': '2-n-Propyl-2-pentenoic acid',
                                      'reason': 'No linear carbon chain found'},
                                  {   'smiles': 'CC(C)CCCC(C)CCCC(C)CCC(=O)C(C)C(O)=O',
                                      'name': '3-oxopristanic acid',
                                      'reason': 'Found non-methyl branching '
                                                'groups'},
                                  {   'smiles': '[H][C@@]12[C@H](CCN1CC=C2COC(=O)[C@](O)([C@H](C)O)C(C)(C)O)OC(=O)C(\\C)=C/C',
                                      'name': 'heliosupine',
                                      'reason': 'Molecule contains atoms other '
                                                'than C, H, and O'},
                                  {   'smiles': 'OC(=O)C(CCCC(C)C)C',
                                      'name': '2,6-dimethylheptanoic acid',
                                      'reason': 'Found non-methyl branching '
                                                'groups'},
                                  {   'smiles': '[H]C(C)=C(C)C(O)=O',
                                      'name': '2-methylbut-2-enoic acid',
                                      'reason': 'No linear carbon chain found'},
                                  {   'smiles': 'CCCC(CC=C)C(O)=O',
                                      'name': '2-n-Propyl-4-pentenoic acid',
                                      'reason': 'No linear carbon chain found'},
                                  {   'smiles': 'CC(C)=CCC\\C(C)=C\\C(O)=O',
                                      'name': 'geranic acid',
                                      'reason': 'No linear carbon chain found'},
                                  {   'smiles': 'OC(=O)/C=C\\C(C)(C)C',
                                      'name': '4,4-dimethyl-2Z-pentenoic acid',
                                      'reason': 'No linear carbon chain found'},
                                  {   'smiles': 'O=C(O)[C@H](C(=C)C)CCC(=O)OC',
                                      'name': 'Pentanedioic acid '
                                              '2-(1-methylethenyl)-5-methyl '
                                              'ester',
                                      'reason': 'No linear carbon chain found'},
                                  {   'smiles': 'OC(=O)CC(CC(O)=O)C(C)=C',
                                      'name': '3-Isopropenylpentanedioic acid',
                                      'reason': 'No linear carbon chain '
                                                'found'}],
    'attempt': 3,
    'reasoning': 'The previous code attempted to classify methyl-branched '
                 'fatty acids by checking for the presence of a carboxylic '
                 'acid group, methyl branches, and ensuring that all branching '
                 'groups are methyl groups. However, the error message '
                 'suggests that the issue lies with the `GetDegreeWithPattern` '
                 'method, which is not a valid method for the `Atom` class in '
                 'RDKit.\n'
                 '\n'
                 'To improve the program, we can take a different approach to '
                 'identify methyl-branched fatty acids. Instead of checking '
                 'for the degree of each atom with a specific pattern, we can '
                 'look for the presence of a linear carbon chain with methyl '
                 'branches and a carboxylic acid group at one end.\n'
                 '\n'
                 "Here's the updated program:",
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 33,
    'num_false_positives': 214,
    'num_true_negatives': 141992,
    'num_false_negatives': 61,
    'num_negatives': None,
    'precision': 0.13360323886639677,
    'recall': 0.35106382978723405,
    'f1': 0.1935483870967742,
    'accuracy': 0.9980674631061138,
    'negative_predictive_value': 0.9995705828106412}