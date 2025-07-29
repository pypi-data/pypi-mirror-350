"""
Classifies: CHEBI:52603 1-acyl-sn-glycero-3-phosphoserine
"""
from rdkit import Chem

def is_1_acyl_sn_glycero_3_phosphoserine(smiles: str):
    """
    Determines if a molecule is a 1-acyl-sn-glycero-3-phosphoserine based on its SMILES string.
    This includes a glycerol backbone with an acyl chain at the 1-hydroxy position and a phosphoserine group.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a 1-acyl-sn-glycero-3-phosphoserine, False otherwise
        str: Reason for classification
    """
    
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Look for a glycerol backbone with a defined structure linked by stereochemistry
    glycerol_pattern = Chem.MolFromSmarts("O[C@@H](CO[P](=O)(O)OC[C@H](N)C(=O)O)CO")
    if not mol.HasSubstructMatch(glycerol_pattern):
        return False, "No glycerol backbone with correct stereochemistry found"
    
    # Check for the presence and correct placement of the phosphoserine group
    phosphoserine_pattern = Chem.MolFromSmarts("P(=O)(O)OC[C@H](N)C(=O)O")
    if not mol.HasSubstructMatch(phosphoserine_pattern):
        return False, "No phosphoserine group found"

    # Look for acyl chain pattern with ester linkage
    acyl_pattern = Chem.MolFromSmarts("C(=O)OC[C@H](O)")  # Focus on ester linkage, possibly allowing different chain orientations
    acyl_match = mol.GetSubstructMatch(acyl_pattern)
    if not acyl_match:
        return False, "No acyl chain linked to the glycerol 1-hydroxy position"

    return True, "Contains glycerol backbone with acyl chain and attached phosphoserine group"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:52603',
                          'name': '1-acyl-sn-glycero-3-phosphoserine',
                          'definition': 'An sn-glycerophosphoserine compound '
                                        'having an acyl substituent at the '
                                        '1-hydroxy position.',
                          'parents': ['CHEBI:68510'],
                          'xrefs': ['PMID:16341241'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 27,
                           'log_lines_of_code': 3.295836866004329,
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
                                                 1],
                           'max_indent': 2,
                           'imports': ['from rdkit import Chem'],
                           'imports_count': 1,
                           'methods_called': [   'GetSubstructMatch',
                                                 'HasSubstructMatch',
                                                 'MolFromSmiles',
                                                 'MolFromSmarts'],
                           'methods_called_count': 4,
                           'smarts_strings': [   'P(=O)(O)OC[C@H](N)C(=O)O',
                                                 'O[C@@H](CO[P](=O)(O)OC[C@H](N)C(=O)O)CO',
                                                 'C(=O)OC[C@H](O)'],
                           'smarts_strings_count': 3,
                           'defs': [   'is_1_acyl_sn_glycero_3_phosphoserine(smiles: '
                                       'str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "No glycerol backbone with '
                                          'correct stereochemistry found"',
                                          'False, "No phosphoserine group '
                                          'found"',
                                          'False, "No acyl chain linked to the '
                                          'glycerol 1-hydroxy position"',
                                          'True, "Contains glycerol backbone '
                                          'with acyl chain and attached '
                                          'phosphoserine group"'],
                           'returns_count': 5,
                           'complexity': 3.0591673732008657},
    'message': '\n'
               'Attempt failed: F1 score of 0 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: NONE\n'
               'False positives: NONE\n'
               'False negatives: SMILES: '
               'P(OC[C@H](O)COC(=O)CCCCCCCCCCCCCCC)(OC[C@H](N)C(O)=O)(O)=O '
               'NAME: PS(16:0/0:0) REASON: MISSED No acyl chain linked to the '
               'glycerol 1-hydroxy position\n'
               ' * SMILES: '
               'P(OC[C@H](O)COC(=O)CCC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)(OC[C@H](N)C(O)=O)(O)=O '
               'NAME: PS(20:5(5Z,8Z,11Z,14Z,17Z)/0:0) REASON: MISSED No acyl '
               'chain linked to the glycerol 1-hydroxy position\n'
               ' * SMILES: '
               'P(OC[C@H](O)COC(=O)CCCC/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)(OC[C@H](N)C(O)=O)(O)=O '
               'NAME: PS(18:4(6Z,9Z,12Z,15Z)/0:0) REASON: MISSED No acyl chain '
               'linked to the glycerol 1-hydroxy position\n'
               ' * SMILES: '
               'P(OC[C@H](O)COC(=O)CCCCC/C=C\\C/C=C\\C/C=C\\C/C=C\\CCCCC)(OC[C@H](N)C(O)=O)(O)=O '
               'NAME: PS(22:4(7Z,10Z,13Z,16Z)/0:0) REASON: MISSED No acyl '
               'chain linked to the glycerol 1-hydroxy position\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCC(=O)OC[C@@H](O)COP(O)(=O)OC[C@H](N)C(O)=O '
               'NAME: 1-heptadecanoyl-sn-glycero-3-phosphoserine REASON: '
               'MISSED No acyl chain linked to the glycerol 1-hydroxy '
               'position\n'
               ' * SMILES: '
               'P(OC[C@H](O)COC(=O)CCCCCCC/C=C\\CCCCC)(OC[C@H](N)C(O)=O)(O)=O '
               'NAME: PS(15:1(9Z)/0:0) REASON: MISSED No acyl chain linked to '
               'the glycerol 1-hydroxy position\n'
               ' * SMILES: '
               'CCCCCCCC\\C=C/CCCCCCCC(=O)OC[C@@H](O)COP(O)(=O)OC[C@H](N)C(O)=O '
               'NAME: 1-O-oleoyl-sn-glycero-3-phosphoserine REASON: MISSED No '
               'acyl chain linked to the glycerol 1-hydroxy position\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCC(=O)OC[C@@H](O)COP(O)(=O)OC[C@H](N)C(O)=O '
               'NAME: 1-stearoyl-sn-glycero-3-phosphoserine REASON: MISSED No '
               'acyl chain linked to the glycerol 1-hydroxy position\n'
               ' * SMILES: '
               'P(OC[C@H](O)COC(=O)CCCCCCCCC/C=C\\CCCCCCCCCC)(OC[C@H](N)C(O)=O)(O)=O '
               'NAME: PS(22:1(11Z)/0:0) REASON: MISSED No acyl chain linked to '
               'the glycerol 1-hydroxy position\n'
               ' * SMILES: '
               'P(OC[C@H](O)COC(=O)CCCCCCC/C=C\\CCCC)(OC[C@H](N)C(O)=O)(O)=O '
               'NAME: PS(14:1(9Z)/0:0) REASON: MISSED No acyl chain linked to '
               'the glycerol 1-hydroxy position\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': '[H][C@@]1(O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O)O[C@@H]1[C@@H](O)[C@@H](O)[C@@H](CO)O[C@H]1OC[C@H]1O[C@@H](OC[C@H]2O[C@@H](OC[C@H](NC(=O)[C@H](O)CCCCCCCCCCCCCCCCCCCCCC)[C@H](O)[C@H](O)CCCCCCCCCCCCCC)[C@H](O)[C@@H](O)[C@H]2O)[C@H](O)[C@@H](O)[C@H]1O',
                                     'name': 'Neurosporaside',
                                     'reason': 'No glycerol backbone with '
                                               'correct stereochemistry found'},
                                 {   'smiles': '[O-]C(=O)C1=CN(C2CC2)C2=CC(N3CC[NH2+]CC3)=C(F)C=C2C1=O',
                                     'name': 'ciprofloxacin zwitterion',
                                     'reason': 'No glycerol backbone with '
                                               'correct stereochemistry found'},
                                 {   'smiles': 'O=C1NC(=CC2=C1O[C@H]([C@@H](O)CC(C)C)O2)C',
                                     'name': 'Dihydroisoflavipucine',
                                     'reason': 'No glycerol backbone with '
                                               'correct stereochemistry found'},
                                 {   'smiles': 'O=C1N2C(C(=O)N([C@@]2(OC)C)C[C@@H](O)C3=CC=CC=C3)=CC4=C1N(C=5C=CC=CC45)C',
                                     'name': 'Marinacarboline K',
                                     'reason': 'No glycerol backbone with '
                                               'correct stereochemistry found'},
                                 {   'smiles': 'O1[C@@H](O[C@H]2[C@@H](O)[C@H](O)[C@H](O[C@@H]2OC[C@H]3OC(O)[C@@H](O)[C@@H](O)[C@@H]3O)CO)[C@H](NC(=O)C)[C@@H](O)[C@H](O[C@@H]4O[C@@H]([C@H](O)[C@H](O)[C@H]4O)CO[C@]5(O[C@H]([C@H](NC(=O)C)[C@@H](O)C5)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]1CO',
                                     'name': '(2R,4S,5R,6R)-5-Acetamido-2-[[(2R,3R,4S,5R,6S)-6-[(2R,3S,4R,5R,6S)-5-acetamido-6-[(2S,3S,4S,5S,6R)-4,5-dihydroxy-6-(hydroxymethyl)-2-[[(2R,3S,4S,5S)-3,4,5,6-tetrahydroxyoxan-2-yl]methoxy]oxan-3-yl]oxy-4-hydroxy-2-(hydroxymethyl)oxan-3-yl]oxy-3,4,5-trihydroxyoxan-2-yl]methoxy]-4-hydroxy-6-[(1R,2R)-1,2,3-trihydroxypropyl]oxane-2-carboxylic '
                                             'acid',
                                     'reason': 'No glycerol backbone with '
                                               'correct stereochemistry found'},
                                 {   'smiles': 'O(C(=O)CCCCCCC)CCC1=CC=CC=C1',
                                     'name': '2-Phenylethyl octanoate',
                                     'reason': 'No glycerol backbone with '
                                               'correct stereochemistry found'},
                                 {   'smiles': 'P(OCC(OC(=O)CCCCCCC/C=C\\CCCCCCCC)COC(=O)CCC/C=C\\C/C=C\\C/C=C\\CCCCCCCC)(OCCNC)(O)=O',
                                     'name': 'PE-NMe(20:3(5Z,8Z,11Z)/18:1(9Z))',
                                     'reason': 'No glycerol backbone with '
                                               'correct stereochemistry found'},
                                 {   'smiles': 'O=C1C2=C(OC=3C1=CC=CN3)C(Cl)=CC(=C2)C=4NN=NN4',
                                     'name': 'traxanox',
                                     'reason': 'No glycerol backbone with '
                                               'correct stereochemistry found'},
                                 {   'smiles': 'CCCCC(C)CCCCCC(C)CCCCCCCCCC(C)CC(O)=O',
                                     'name': '3,13,19-trimethyltricosanoic '
                                             'acid',
                                     'reason': 'No glycerol backbone with '
                                               'correct stereochemistry found'},
                                 {   'smiles': 'COC(CC1=CC[C@]2(C)[C@@H](C)CCC[C@]2(C)C1=O)OC',
                                     'name': 'aignopsane ketal',
                                     'reason': 'No glycerol backbone with '
                                               'correct stereochemistry '
                                               'found'}],
    'sample_false_negatives': [],
    'attempt': 2,
    'reasoning': "To diagnose the failure, let's review the previous code and "
                 'analyze the outcomes. The task is to identify whether a '
                 'given SMILES represents a 1-acyl-sn-glycero-3-phosphoserine. '
                 'The previous code implemented substructure searches for '
                 'stereochemistry-aware glycerol backbones, phosphoserine '
                 'groups, and acyl linkages.\n'
                 '\n'
                 '### Observations on Failure:\n'
                 '- **No acyl chain linked to the glycerol 1-hydroxy '
                 'position**: The main error suggests that the program is not '
                 'correctly identifying the acyl linkage.\n'
                 '- The acyl linkage pattern using `C(=O)O[C@H](O)` might not '
                 'match all configurations due to potential variations in acyl '
                 'chains (e.g., chiral centers, chain branching) or '
                 'differences between explicit and implicit hydrogen handling '
                 'in RDKit.\n'
                 '\n'
                 '### Improvement Steps:\n'
                 '1. **Refine the Acyl Group Detection**:\n'
                 '   - Enhance the acyl detection by being more inclusive of '
                 'orientation or configuration, such as considering both '
                 'stereochemistry and chain length variation.\n'
                 '   - Consider a more general pattern for the acyl linkage, '
                 'checking only for the ester bond to the glycerol hydroxyl '
                 'group without the chiral constraint.\n'
                 '2. **Ensure Complete Structure Coverage**:\n'
                 '   - Double-check the entire glycerol backbone and '
                 'phosphoserine substructure pattern, potentially increasing '
                 'specificity around the hydroxy and acyl connecting groups.\n'
                 '\n'
                 'Here is the revised code:',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 26,
    'num_false_positives': 353,
    'num_true_negatives': 141921,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.06860158311345646,
    'recall': 1.0,
    'f1': 0.12839506172839504,
    'accuracy': 0.9975193253689388,
    'negative_predictive_value': 1.0}