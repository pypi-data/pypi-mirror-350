"""
Classifies: CHEBI:20706 6-aminopurines
"""
"""
Classifies: CHEBI:26947 6-aminopurines
A 6-aminopurine is any compound having 6-aminopurine (adenine) as part of its structure.
"""
from rdkit import Chem
from rdkit.Chem import rdMolDescriptors

def is_6_aminopurines(smiles: str):
    """
    Determines if a molecule contains a 6-aminopurine (adenine) moiety based on its SMILES string.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule contains a 6-aminopurine moiety, False otherwise
        str: Reason for classification
    """
    
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
    
    # Check for presence of 6-aminopurine ring system
    adenine_pattern = Chem.MolFromSmarts("n1cnc2c(N)ncnc12")
    has_adenine = mol.HasSubstructMatch(adenine_pattern)
    
    if not has_adenine:
        return False, "Does not contain 6-aminopurine (adenine) moiety"
    
    # Count nitrogens to verify purine
    n_count = sum(1 for atom in mol.GetAtoms() if atom.GetAtomicNum() == 7)
    if n_count < 5:
        return False, "Too few nitrogens for purine system"
    
    # Check for CoA or phosphate attachments (common in metabolites)
    has_coa = mol.HasSubstructMatch(Chem.MolFromSmarts("C(=O)SCCNC(=O)CCNC(=O)[C@@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12"))
    has_phosphate = any(atom.GetDegree() == 4 and atom.GetAtomicNum() == 8 for atom in mol.GetAtoms())
    
    # Verify mass range (optional)
    mol_wt = rdMolDescriptors.CalcExactMolWt(mol)
    if mol_wt < 200 or mol_wt > 1500:
        return False, "Molecular weight out of typical range for 6-aminopurine metabolite"
    
    if has_coa or has_phosphate:
        return True, "Contains 6-aminopurine (adenine) moiety with CoA or phosphate attachment"
    else:
        return True, "Contains 6-aminopurine (adenine) moiety"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:20706',
                          'name': '6-aminopurines',
                          'definition': 'Any compound having 6-aminopurine '
                                        '(adenine) as part of its structure.',
                          'parents': ['CHEBI:22527'],
                          'xrefs': [   'PMID:1646334',
                                       'PMID:18524423',
                                       'PMID:7342604'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 32,
                           'log_lines_of_code': 3.4657359027997265,
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
                                                 2,
                                                 1,
                                                 1,
                                                 2,
                                                 1,
                                                 2],
                           'max_indent': 2,
                           'imports': [   'from rdkit import Chem',
                                          'from rdkit.Chem import '
                                          'rdMolDescriptors'],
                           'imports_count': 2,
                           'methods_called': [   'MolFromSmiles',
                                                 'CalcExactMolWt',
                                                 'GetDegree',
                                                 'HasSubstructMatch',
                                                 'MolFromSmarts',
                                                 'GetAtoms',
                                                 'GetAtomicNum'],
                           'methods_called_count': 7,
                           'smarts_strings': [   'n1cnc2c(N)ncnc12',
                                                 '"C(=O)SCCNC(=O)CCNC(=O)[C@@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12")'],
                           'smarts_strings_count': 2,
                           'defs': ['is_6_aminopurines(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "Does not contain '
                                          '6-aminopurine (adenine) moiety"',
                                          'False, "Too few nitrogens for '
                                          'purine system"',
                                          'False, "Molecular weight out of '
                                          'typical range for 6-aminopurine '
                                          'metabolite"',
                                          'True, "Contains 6-aminopurine '
                                          '(adenine) moiety with CoA or '
                                          'phosphate attachment"',
                                          'True, "Contains 6-aminopurine '
                                          '(adenine) moiety"'],
                           'returns_count': 6,
                           'complexity': 3.893147180559945},
    'message': '\n'
               "Error: name 'is_6_aminopurines' is not defined\n"
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
    'sample_true_negatives': [   {   'smiles': 'Cl.CN(Cc1ccc(cc1)C(C)(C)C)Cc1cccc2ccccc12',
                                     'name': 'butenafine hydrochloride',
                                     'reason': 'Does not contain 6-aminopurine '
                                               '(adenine) moiety'},
                                 {   'smiles': 'CCOC1=CC=CC=C1N2CCN(CC2)C(=S)NC(=O)C34CC5CC(C3)CC(C5)C4',
                                     'name': 'N-[[4-(2-ethoxyphenyl)-1-piperazinyl]-sulfanylidenemethyl]-1-adamantanecarboxamide',
                                     'reason': 'Does not contain 6-aminopurine '
                                               '(adenine) moiety'},
                                 {   'smiles': 'OC(=O)C1=CC2=CC(O)=C(O)C=C2C(=N1)C(=O)C1=CC=C(O)C(O)=C1',
                                     'name': 'NBI-31772',
                                     'reason': 'Does not contain 6-aminopurine '
                                               '(adenine) moiety'},
                                 {   'smiles': '[NH3+]CCC[C@@H]([NH3+])CC([O-])=O',
                                     'name': '(3R)-3,6-diammoniohexanoate(1+)',
                                     'reason': 'Does not contain 6-aminopurine '
                                               '(adenine) moiety'},
                                 {   'smiles': 'Cl.Cl.O[C@H](CNCCCl)[C@@H](O)[C@H](O)[C@H](O)CNCCCl',
                                     'name': 'Mannomustine dihydrochloride',
                                     'reason': 'Does not contain 6-aminopurine '
                                               '(adenine) moiety'},
                                 {   'smiles': 'N[C@@H](CCC(=O)NCC(O)=O)C(O)=O',
                                     'name': 'gamma-Glu-Gly',
                                     'reason': 'Does not contain 6-aminopurine '
                                               '(adenine) moiety'},
                                 {   'smiles': 'CC(C)(C)[S@](=O)N1CC2=CC(=NC(=C2[C@@H]1CCO)C3=CC=CC(=C3)C4=CN=CC=C4)C(=O)NCCC5=CC=NC=C5',
                                     'name': '(3S)-2-[(S)-tert-butylsulfinyl]-3-(2-hydroxyethyl)-N-(2-pyridin-4-ylethyl)-4-(3-pyridin-3-ylphenyl)-1,3-dihydropyrrolo[3,4-c]pyridine-6-carboxamide',
                                     'reason': 'Does not contain 6-aminopurine '
                                               '(adenine) moiety'},
                                 {   'smiles': '[H][C@@]12C=C(CC[C@@]1(C)CCCC2=C)C(C)C',
                                     'name': '5alpha,10beta-sibirene',
                                     'reason': 'Does not contain 6-aminopurine '
                                               '(adenine) moiety'},
                                 {   'smiles': 'CC(C([O-])=O)c1cccc(Oc2ccccc2)c1',
                                     'name': 'fenoprofen(1-)',
                                     'reason': 'Does not contain 6-aminopurine '
                                               '(adenine) moiety'},
                                 {   'smiles': 'O=C1[C@@]23C(=O)N[C@H]([C@@H]2[C@H](C)C(=C[C@@H]3C=C(CCC([C@H](CC1)O)=O)C)C)CC(C)C',
                                     'name': 'Aspochalasin M',
                                     'reason': 'Does not contain 6-aminopurine '
                                               '(adenine) moiety'}],
    'sample_false_negatives': [   {   'smiles': 'O1C(CCC1)C(=O)N2CCNCC2',
                                      'name': '1-(Tetrahydro-2-furoyl)piperazine',
                                      'reason': 'Does not contain '
                                                '6-aminopurine (adenine) '
                                                'moiety'},
                                  {   'smiles': 'O=C(OC)N1C2=NC=NC(=C2N=C1)N',
                                      'name': '6-aminopurine-9-carboxylic acid '
                                              'methyl ester',
                                      'reason': 'Molecular weight out of '
                                                'typical range for '
                                                '6-aminopurine metabolite'},
                                  {   'smiles': 'C=1N=C(C=2N=CNC2N1)NCO',
                                      'name': '6-hydroxymethyladenine',
                                      'reason': 'Molecular weight out of '
                                                'typical range for '
                                                '6-aminopurine metabolite'},
                                  {   'smiles': 'NC1=NC(O)=NC2=C1N=C(O)N2',
                                      'name': '2,8-dihydroxyadenine',
                                      'reason': 'Molecular weight out of '
                                                'typical range for '
                                                '6-aminopurine metabolite'},
                                  {   'smiles': 'Nc1ncnc2[nH]cnc12',
                                      'name': 'adenine',
                                      'reason': 'Molecular weight out of '
                                                'typical range for '
                                                '6-aminopurine metabolite'},
                                  {   'smiles': 'C=12C(=NC=NC1N)NC(=N2)O',
                                      'name': '8-hydroxyadenine',
                                      'reason': 'Molecular weight out of '
                                                'typical range for '
                                                '6-aminopurine metabolite'},
                                  {   'smiles': 'C=12C(=NC=NC1N)NC(N2)=O',
                                      'name': '8-oxoadenine',
                                      'reason': 'Molecular weight out of '
                                                'typical range for '
                                                '6-aminopurine metabolite'},
                                  {   'smiles': 'Cn1cnc(N)c2ncnc12',
                                      'name': '3-methyladenine',
                                      'reason': 'Molecular weight out of '
                                                'typical range for '
                                                '6-aminopurine metabolite'},
                                  {   'smiles': 'CNc1ncnc2[nH]cnc12',
                                      'name': '6-methyladenine',
                                      'reason': 'Molecular weight out of '
                                                'typical range for '
                                                '6-aminopurine metabolite'},
                                  {   'smiles': 'Cn1cnc2c(N)ncnc12',
                                      'name': '9-methyladenine',
                                      'reason': 'Molecular weight out of '
                                                'typical range for '
                                                '6-aminopurine metabolite'}],
    'attempt': 1,
    'reasoning': 'The previous code attempts to classify molecules as '
                 '6-aminopurines, which are compounds containing the '
                 '6-aminopurine (adenine) moiety. However, the code was not '
                 'executed, resulting in the error "name \'is_6_aminopurines\' '
                 'is not defined". This error occurred because the function '
                 'name in the code is `is_6_aminopurine` (singular), while the '
                 'expected function name is `is_6_aminopurines` (plural).\n'
                 '\n'
                 'To fix this issue and improve the code, we need to update '
                 'the function name to match the expected name. Additionally, '
                 'we can incorporate some of the commented-out lines to add '
                 'additional checks and improve the classification accuracy.\n'
                 '\n'
                 "Here's the updated code:",
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 664,
    'num_false_positives': 1573,
    'num_true_negatives': 140049,
    'num_false_negatives': 14,
    'num_negatives': None,
    'precision': 0.29682610639248996,
    'recall': 0.9793510324483776,
    'f1': 0.4555746140651802,
    'accuracy': 0.9888475052705552,
    'negative_predictive_value': 0.9999000449797592}