"""
Classifies: CHEBI:35759 1-monoglyceride
"""
"""
Classifies: 1-monoglyceride
Definition: A monoglyceride in which the acyl substituent is located at position 1
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_1_monoglyceride(smiles: str):
    """
    Determines if a molecule is a 1-monoglyceride based on its SMILES string.
    A 1-monoglyceride has:
    - A glycerol backbone (3 carbons)
    - An ester group at position 1
    - Hydroxyl groups at positions 2 and 3
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        tuple: (bool, str) - (is_1_monoglyceride, reason)
    """
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Define pattern for 1-monoglyceride:
    # [#6]-C(=O)-O-CH2-CH(OH)-CH2OH
    # This pattern captures the essential features:
    # - Ester group at position 1
    # - Hydroxyl groups at positions 2 and 3
    # - Carbon chain attached to the carbonyl
    pattern = Chem.MolFromSmarts("[#6]-C(=O)-O-[CH2X4]-[CH1X4](-[OX2H1])-[CH2X4]-[OX2H1]")
    
    if pattern is None:
        return False, "Invalid SMARTS pattern"
        
    if not mol.HasSubstructMatch(pattern):
        return False, "Does not match 1-monoglyceride pattern"

    # Count ester groups (-O-C(=O)-)
    ester_pattern = Chem.MolFromSmarts("[OX2][CX3](=[OX1])")
    if ester_pattern is None:
        return False, "Invalid ester SMARTS pattern"
    
    ester_matches = mol.GetSubstructMatches(ester_pattern)
    if len(ester_matches) != 1:
        return False, f"Found {len(ester_matches)} ester groups, need exactly 1"

    # Count hydroxyl groups
    hydroxyl_pattern = Chem.MolFromSmarts("[OX2H1]")
    if hydroxyl_pattern is None:
        return False, "Invalid hydroxyl SMARTS pattern"
    
    hydroxyl_matches = mol.GetSubstructMatches(hydroxyl_pattern)
    if len(hydroxyl_matches) != 2:
        return False, f"Found {len(hydroxyl_matches)} hydroxyl groups, need exactly 2"

    # Verify carbon chain length (should be at least 2 carbons in acyl group)
    acyl_pattern = Chem.MolFromSmarts("[CX3](=[OX1])-[#6]-[#6]")
    if acyl_pattern is None:
        return False, "Invalid acyl SMARTS pattern"
        
    if not mol.HasSubstructMatch(acyl_pattern):
        return False, "Acyl chain too short"

    return True, "Contains glycerol backbone with one ester bond at position 1 and two free hydroxyl groups"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:35759',
                          'name': '1-monoglyceride',
                          'definition': 'A monoglyceride in which the acyl '
                                        'substituent is located at position 1.',
                          'parents': ['CHEBI:17408', 'CHEBI:76575'],
                          'xrefs': ['KEGG:C01885'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': None,
    'message': '\n'
               'Error: Python argument types in\n'
               '    Mol.HasSubstructMatch(Mol, NoneType)\n'
               'did not match C++ signature:\n'
               '    HasSubstructMatch(RDKit::ROMol self, RDKit::MolBundle '
               'query, RDKit::SubstructMatchParameters params=True)\n'
               '    HasSubstructMatch(RDKit::ROMol self, RDKit::ROMol query, '
               'RDKit::SubstructMatchParameters params)\n'
               '    HasSubstructMatch(RDKit::ROMol self, RDKit::MolBundle '
               'query, bool recursionPossible=True, bool useChirality=False, '
               'bool useQueryQueryMatches=False)\n'
               '    HasSubstructMatch(RDKit::ROMol self, RDKit::ROMol query, '
               'bool recursionPossible=True, bool useChirality=False, bool '
               'useQueryQueryMatches=False)\n'
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
    'sample_true_negatives': [   {   'smiles': 'O1C(C1CC#CC#CC(OC(=O)C)C=C)CCCCCC=C',
                                     'name': 'Ginsenoyne F',
                                     'reason': 'Does not match 1-monoglyceride '
                                               'pattern'},
                                 {   'smiles': 'OC(=O)C1=CC=C(N1)C(=O)NC1=C(O)C2=CC=C(O)C=C2OC1=O',
                                     'name': 'cacibiocin A',
                                     'reason': 'Does not match 1-monoglyceride '
                                               'pattern'},
                                 {   'smiles': 'S(OC)C(=O)C1=NC(C(SC)=O)=CC=C1',
                                     'name': '6-[(methoxythio)carbonyl]pyridine-2-monothiocarboxylic '
                                             'acid S-methyl ester',
                                     'reason': 'Does not match 1-monoglyceride '
                                               'pattern'},
                                 {   'smiles': 'S1(=O)(=O)C(C(C(=O)[O-])C2C1CC2=O)(C)C.S1C(C(C(=O)[O-])N2C1C(NC(=O)C(N)C3=CC=CC=C3)C2=O)(C)C.[Na+].[Na+]',
                                     'name': 'Ampicillin Sodium Mixture With '
                                             'Sulbactam Sodium',
                                     'reason': 'Does not match 1-monoglyceride '
                                               'pattern'},
                                 {   'smiles': 'CN(C)C1=CC2=C(C=C1)O[C@H]3[C@@H]2C[C@@H](O[C@H]3CO)CC(=O)NCC4=CC=C(C=C4)OC',
                                     'name': '2-[(1S,3R,4aR,9aS)-6-(dimethylamino)-1-(hydroxymethyl)-3,4,4a,9a-tetrahydro-1H-pyrano[3,4-b]benzofuran-3-yl]-N-[(4-methoxyphenyl)methyl]acetamide',
                                     'reason': 'Does not match 1-monoglyceride '
                                               'pattern'},
                                 {   'smiles': 'O=C(N[C@@H]([C@H](CC)C)C(O)=O)[C@@H](NC(=O)[C@@H](N)CC=1C=2C(NC1)=CC=CC2)CC=3C=4C(NC3)=CC=CC4',
                                     'name': 'Trp-Trp-Ile',
                                     'reason': 'Does not match 1-monoglyceride '
                                               'pattern'},
                                 {   'smiles': '[H][C@]1(O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O)Oc1c[nH]c2ccc(Br)c(Cl)c12',
                                     'name': '5-bromo-4-chloro-3-indolyl '
                                             'beta-D-glucoside',
                                     'reason': 'Does not match 1-monoglyceride '
                                               'pattern'},
                                 {   'smiles': 'C[N+]1=CC=C(C=C1)C2=CC(=C(C=C2)O)OC',
                                     'name': '2-methoxy-4-(1-methyl-4-pyridin-1-iumyl)phenol',
                                     'reason': 'Does not match 1-monoglyceride '
                                               'pattern'},
                                 {   'smiles': 'CC(C)CN(C1CCS(=O)(=O)C1)C(=O)COC(=O)C2=CC3=C(S2)CCC3',
                                     'name': '5,6-dihydro-4H-cyclopenta[b]thiophene-2-carboxylic '
                                             'acid '
                                             '[2-[(1,1-dioxo-3-thiolanyl)-(2-methylpropyl)amino]-2-oxoethyl] '
                                             'ester',
                                     'reason': 'Does not match 1-monoglyceride '
                                               'pattern'},
                                 {   'smiles': 'O[C@@H]([C@H](NC(=O)[C@@H](N)C)C(=O)N[C@@H](CC(C)C)C(O)=O)C',
                                     'name': 'Ala-Thr-Leu',
                                     'reason': 'Does not match 1-monoglyceride '
                                               'pattern'}],
    'sample_false_negatives': [   {   'smiles': 'O(C[C@@H](O)CO)C(=O)C',
                                      'name': '(R)-glycerol 1-acetate',
                                      'reason': 'Acyl chain too short'},
                                  {   'smiles': 'C(\\[C@H]1[C@@H](CC([C@@H]1C/C=C\\CCCC(=O)OCC(CO)O)=O)O)=C/[C@H](CCCCC)O',
                                      'name': 'prostaglandin E2 1-glyceryl '
                                              'ester',
                                      'reason': 'Found 4 hydroxyl groups, need '
                                                'exactly 2'},
                                  {   'smiles': 'O=C1OC(/C(=C/C(=O)OC[C@H](O)CO)/C)=CC(=C1)OC',
                                      'name': 'Pestalotiopyrone I',
                                      'reason': 'Acyl chain too short'},
                                  {   'smiles': 'O=C(OCC(O)CO)/C=C/C(O)C(O)/C=C/C',
                                      'name': 'Musacin A',
                                      'reason': 'Found 4 hydroxyl groups, need '
                                                'exactly 2'},
                                  {   'smiles': '[C@@H]1(/C=C/[C@@H](O)CCCCC)[C@H]([C@H](C[C@H]1O)O)C/C=C\\CCCC(=O)OCC(CO)O',
                                      'name': 'prostaglandin F2alpha '
                                              '1-glyceryl ester',
                                      'reason': 'Found 5 hydroxyl groups, need '
                                                'exactly 2'},
                                  {   'smiles': 'O=C(OC[C@@H](O)CO)/C=C/CCCCCCC(=O)OC',
                                      'name': 'Cladosporester C',
                                      'reason': 'Found 2 ester groups, need '
                                                'exactly 1'},
                                  {   'smiles': 'O=C(OCC(O)CO)/C=C/C1=CC(OC)=C(O)C=C1',
                                      'name': '1-feruloyl-sn-glycerol',
                                      'reason': 'Found 3 hydroxyl groups, need '
                                                'exactly 2'}],
    'attempt': 2,
    'reasoning': "Let's analyze what went wrong and improve the program:\n"
                 '\n'
                 '1. The main error occurred because one of the SMARTS '
                 'patterns (mono_1_pattern) was invalid. The dots in the '
                 'SMARTS pattern were causing issues, and the multi-line '
                 'string format might have introduced unwanted whitespace.\n'
                 '\n'
                 '2. The approach to check for the 1-monoglyceride pattern was '
                 'too complex with multiple separate patterns. We should '
                 'simplify it to a single, well-defined pattern.\n'
                 '\n'
                 "3. We need to ensure we're correctly identifying position 1 "
                 'of the glycerol backbone.\n'
                 '\n'
                 '4. The pattern matching should account for both '
                 'stereochemistry variations since we have examples of both R '
                 'and S configurations.\n'
                 '\n'
                 "Here's an improved version:",
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 59,
    'num_false_positives': 6,
    'num_true_negatives': 142228,
    'num_false_negatives': 7,
    'num_negatives': None,
    'precision': 0.9076923076923077,
    'recall': 0.8939393939393939,
    'f1': 0.900763358778626,
    'accuracy': 0.9999086437104708,
    'negative_predictive_value': 0.9999507856715998}