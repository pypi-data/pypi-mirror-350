"""
Classifies: CHEBI:61703 nonclassic icosanoid
"""
"""
Classifies: Nonclassic Icosanoid
"""
from rdkit import Chem

def is_nonclassic_icosanoid(smiles: str):
    """
    Determines if a molecule is a nonclassic icosanoid based on its SMILES string.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a nonclassic icosanoid, False otherwise
        str: Reason for classification
    """
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
    
    # Check for presence of a central C20 backbone
    carbon_count = sum(1 for atom in mol.GetAtoms() if atom.GetAtomicNum() == 6)
    if carbon_count < 20:
        return False, f"Contains {carbon_count} carbons; requires at least 20 carbons for backbone"
    
    # Check for presence of key functional groups: epoxide, multiple hydroxyls, and carboxylic acid
    # Epoxide pattern with allowance for asymmetric structures if needed
    epoxide_pattern = Chem.MolFromSmarts("[C;R1]1[O;R1][C;R1]1")  
    hydroxyl_pattern = Chem.MolFromSmarts("[OX2H]")  # Hydroxyl groups
    carboxylic_acid_pattern = Chem.MolFromSmarts("C(=O)[OX2H1]")  # Carboxylic acid group
    
    has_epoxide = mol.HasSubstructMatch(epoxide_pattern)
    hydroxyl_count = len(mol.GetSubstructMatches(hydroxyl_pattern))
    has_carboxylic_acid = mol.HasSubstructMatch(carboxylic_acid_pattern)

    # Ensure it has at least one epoxide, at least two hydroxyls, and one carboxylic acid
    if not has_epoxide or hydroxyl_count < 2 or not has_carboxylic_acid:
        return False, "Must contain epoxide group, multiple hydroxyls, and a carboxylic acid group"
    
    # Avoid classic icosanoid motifs
    prostanoid_pattern = Chem.MolFromSmarts("C1=CCCCC1C(=O)O")  # Generalized prostanoids ring
    leukotriene_pattern = Chem.MolFromSmarts("CC(C)(C)C[CX4]")  # Branching pattern specific

    if mol.HasSubstructMatch(prostanoid_pattern) or mol.HasSubstructMatch(leukotriene_pattern):
        return False, "Substructure resembles classic icosanoids (prostanoid or leukotriene patterns detected)"
    
    # If all criteria are met, classify as nonclassic icosanoid
    return True, "Classified as nonclassic icosanoid with adequate C20 backbone and functionalization"

# Note: This classification is based on identifying structural elements typically 
# found in nonclassic icosanoids and may not capture all derivatives.


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:61703',
                          'name': 'nonclassic icosanoid',
                          'definition': 'Any biologically active signalling '
                                        'molecule made by oxygenation of C20 '
                                        'fatty acids other than the classic '
                                        'icosanoids (the leukotrienes and the '
                                        'prostanoids).',
                          'parents': ['CHEBI:23899'],
                          'xrefs': ['PMID:10477044'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 34,
                           'log_lines_of_code': 3.5263605246161616,
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
                                                 1,
                                                 1,
                                                 0,
                                                 1,
                                                 1,
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 0,
                                                 1,
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 0],
                           'max_indent': 2,
                           'imports': ['from rdkit import Chem'],
                           'imports_count': 1,
                           'methods_called': [   'GetAtoms',
                                                 'GetSubstructMatches',
                                                 'HasSubstructMatch',
                                                 'MolFromSmiles',
                                                 'MolFromSmarts',
                                                 'GetAtomicNum'],
                           'methods_called_count': 6,
                           'smarts_strings': [   '[C;R1]1[O;R1][C;R1]1',
                                                 'C(=O)[OX2H1]',
                                                 'CC(C)(C)C[CX4]',
                                                 '[OX2H]',
                                                 'C1=CCCCC1C(=O)O'],
                           'smarts_strings_count': 5,
                           'defs': ['is_nonclassic_icosanoid(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, f"Contains {carbon_count} '
                                          'carbons; requires at least 20 '
                                          'carbons for backbone"',
                                          'False, "Must contain epoxide group, '
                                          'multiple hydroxyls, and a '
                                          'carboxylic acid group"',
                                          'False, "Substructure resembles '
                                          'classic icosanoids (prostanoid or '
                                          'leukotriene patterns detected)"',
                                          'True, "Classified as nonclassic '
                                          'icosanoid with adequate C20 '
                                          'backbone and functionalization"'],
                           'returns_count': 5,
                           'complexity': 3.5052721049232325},
    'message': '\n'
               'Attempt failed: F1 score of 0 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: NONE\n'
               'False positives: NONE\n'
               'False negatives: SMILES: '
               'CCCCC\\C=C/C\\C=C/[C@H](O)[C@H]1O[C@H]1C\\C=C/CCCC(O)=O NAME: '
               '(8S,9S)-epoxy-(10R)-hydroxyicosa-(5Z,11Z,14Z)-trienoic acid '
               'REASON: MISSED Must contain epoxide group, multiple hydroxyls, '
               'and a carboxylic acid group\n'
               ' * SMILES: '
               'O=C(CCC/C=C\\C/C=C\\CC(/C=C/[C@@H]1[C@H](CCCCC)O1)O)O NAME: 11 '
               'hydroxy-(14R,15S)-epoxy-(5Z,8Z,12E)-icosatrienoic acid REASON: '
               'MISSED Must contain epoxide group, multiple hydroxyls, and a '
               'carboxylic acid group\n'
               ' * SMILES: '
               'CCCCC\\C=C/C[C@@H]1O[C@H]1\\C=C\\[C@H](O)C\\C=C/CCCC(O)=O '
               'NAME: (8R)-hydroxy-(11S,12S)-epoxyicosa-(5Z,9E,14Z)-trienoic '
               'acid REASON: MISSED Must contain epoxide group, multiple '
               'hydroxyls, and a carboxylic acid group\n'
               ' * SMILES: C(CCCO)C/C=C\\C/C=C\\CC1C(C/C=C\\CCCC(O)=O)O1 NAME: '
               '8,9-epoxy-20-hydroxy-(5Z,11Z,14Z)-icosatrienoic acid REASON: '
               'MISSED Must contain epoxide group, multiple hydroxyls, and a '
               'carboxylic acid group\n'
               ' * SMILES: '
               'CCCCC[C@H](O)\\C=C\\C=C/C=C/C=C/[C@H](O)[C@@H](O)CCCC(O)=O '
               'NAME: 6-epi-lipoxin A4 REASON: MISSED Must contain epoxide '
               'group, multiple hydroxyls, and a carboxylic acid group\n'
               ' * SMILES: C(CCCO)CC1C(C/C=C\\C/C=C\\C/C=C\\CCCC(O)=O)O1 NAME: '
               '14,15-epoxy-20-hydroxy-(5Z,8Z,11Z)-icosatrienoic acid REASON: '
               'MISSED Must contain epoxide group, multiple hydroxyls, and a '
               'carboxylic acid group\n'
               ' * SMILES: '
               'O[C@@H](CCCC(OC)=O)[C@H](O)/C=C/C=C/C=C\\C=C\\[C@@H](O)CCCCC '
               'NAME: 5(S),6(R)-Lipoxin A4 methyl ester REASON: MISSED Must '
               'contain epoxide group, multiple hydroxyls, and a carboxylic '
               'acid group\n'
               ' * SMILES: '
               'O=C(CCC/C=C\\C/C=C\\C/C=C\\[C@@H]([C@H]1[C@H](CCCCC)O1)O)O '
               'NAME: (13S)-hydroxy-(14S,15S)-epoxy-(5Z,8Z,11Z)-icosatrienoic '
               'acid REASON: MISSED Must contain epoxide group, multiple '
               'hydroxyls, and a carboxylic acid group\n'
               ' * SMILES: '
               'CCCCCC(=O)\\C=C\\C=C/C=C/C=C/[C@@H](O)[C@@H](O)CCCC(O)=O NAME: '
               '15-oxolipoxin A4 REASON: MISSED Must contain epoxide group, '
               'multiple hydroxyls, and a carboxylic acid group\n'
               ' * SMILES: '
               'CCCCC[C@@H](O)[C@H](O)\\C=C\\C=C\\C=C/C=C/[C@@H](O)CCCC(O)=O '
               'NAME: 15-epi-lipoxin B4 REASON: MISSED Must contain epoxide '
               'group, multiple hydroxyls, and a carboxylic acid group\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': '[H][C@@]1(O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O)O[C@@H]1[C@@H](O)[C@@H](O)[C@@H](CO)O[C@H]1OC[C@H]1O[C@@H](OC[C@H]2O[C@@H](OC[C@H](NC(=O)[C@H](O)CCCCCCCCCCCCCCCCCCCCCC)[C@H](O)[C@H](O)CCCCCCCCCCCCCC)[C@H](O)[C@@H](O)[C@H]2O)[C@H](O)[C@@H](O)[C@H]1O',
                                     'name': 'Neurosporaside',
                                     'reason': 'Must contain epoxide group, '
                                               'multiple hydroxyls, and a '
                                               'carboxylic acid group'},
                                 {   'smiles': '[O-]C(=O)C1=CN(C2CC2)C2=CC(N3CC[NH2+]CC3)=C(F)C=C2C1=O',
                                     'name': 'ciprofloxacin zwitterion',
                                     'reason': 'Contains 17 carbons; requires '
                                               'at least 20 carbons for '
                                               'backbone'},
                                 {   'smiles': 'O=C1NC(=CC2=C1O[C@H]([C@@H](O)CC(C)C)O2)C',
                                     'name': 'Dihydroisoflavipucine',
                                     'reason': 'Contains 12 carbons; requires '
                                               'at least 20 carbons for '
                                               'backbone'},
                                 {   'smiles': 'O=C1N2C(C(=O)N([C@@]2(OC)C)C[C@@H](O)C3=CC=CC=C3)=CC4=C1N(C=5C=CC=CC45)C',
                                     'name': 'Marinacarboline K',
                                     'reason': 'Must contain epoxide group, '
                                               'multiple hydroxyls, and a '
                                               'carboxylic acid group'},
                                 {   'smiles': 'O1[C@@H](O[C@H]2[C@@H](O)[C@H](O)[C@H](O[C@@H]2OC[C@H]3OC(O)[C@@H](O)[C@@H](O)[C@@H]3O)CO)[C@H](NC(=O)C)[C@@H](O)[C@H](O[C@@H]4O[C@@H]([C@H](O)[C@H](O)[C@H]4O)CO[C@]5(O[C@H]([C@H](NC(=O)C)[C@@H](O)C5)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]1CO',
                                     'name': '(2R,4S,5R,6R)-5-Acetamido-2-[[(2R,3R,4S,5R,6S)-6-[(2R,3S,4R,5R,6S)-5-acetamido-6-[(2S,3S,4S,5S,6R)-4,5-dihydroxy-6-(hydroxymethyl)-2-[[(2R,3S,4S,5S)-3,4,5,6-tetrahydroxyoxan-2-yl]methoxy]oxan-3-yl]oxy-4-hydroxy-2-(hydroxymethyl)oxan-3-yl]oxy-3,4,5-trihydroxyoxan-2-yl]methoxy]-4-hydroxy-6-[(1R,2R)-1,2,3-trihydroxypropyl]oxane-2-carboxylic '
                                             'acid',
                                     'reason': 'Must contain epoxide group, '
                                               'multiple hydroxyls, and a '
                                               'carboxylic acid group'},
                                 {   'smiles': 'O(C(=O)CCCCCCC)CCC1=CC=CC=C1',
                                     'name': '2-Phenylethyl octanoate',
                                     'reason': 'Contains 16 carbons; requires '
                                               'at least 20 carbons for '
                                               'backbone'},
                                 {   'smiles': 'P(OCC(OC(=O)CCCCCCC/C=C\\CCCCCCCC)COC(=O)CCC/C=C\\C/C=C\\C/C=C\\CCCCCCCC)(OCCNC)(O)=O',
                                     'name': 'PE-NMe(20:3(5Z,8Z,11Z)/18:1(9Z))',
                                     'reason': 'Must contain epoxide group, '
                                               'multiple hydroxyls, and a '
                                               'carboxylic acid group'},
                                 {   'smiles': 'O=C1C2=C(OC=3C1=CC=CN3)C(Cl)=CC(=C2)C=4NN=NN4',
                                     'name': 'traxanox',
                                     'reason': 'Contains 13 carbons; requires '
                                               'at least 20 carbons for '
                                               'backbone'},
                                 {   'smiles': 'CCCCC(C)CCCCCC(C)CCCCCCCCCC(C)CC(O)=O',
                                     'name': '3,13,19-trimethyltricosanoic '
                                             'acid',
                                     'reason': 'Must contain epoxide group, '
                                               'multiple hydroxyls, and a '
                                               'carboxylic acid group'},
                                 {   'smiles': 'COC(CC1=CC[C@]2(C)[C@@H](C)CCC[C@]2(C)C1=O)OC',
                                     'name': 'aignopsane ketal',
                                     'reason': 'Contains 17 carbons; requires '
                                               'at least 20 carbons for '
                                               'backbone'}],
    'sample_false_negatives': [   {   'smiles': 'CCCCC[C@H](O)\\C=C\\C=C/C=C/C=C/[C@H](O)[C@@H](O)CCCC(O)=O',
                                      'name': '6-epi-lipoxin A4',
                                      'reason': 'Must contain epoxide group, '
                                                'multiple hydroxyls, and a '
                                                'carboxylic acid group'},
                                  {   'smiles': 'O[C@@H](CCCC(OC)=O)[C@H](O)/C=C/C=C/C=C\\C=C\\[C@@H](O)CCCCC',
                                      'name': '5(S),6(R)-Lipoxin A4 methyl '
                                              'ester',
                                      'reason': 'Must contain epoxide group, '
                                                'multiple hydroxyls, and a '
                                                'carboxylic acid group'},
                                  {   'smiles': 'CCCCCC(=O)\\C=C\\C=C/C=C/C=C/[C@@H](O)[C@@H](O)CCCC(O)=O',
                                      'name': '15-oxolipoxin A4',
                                      'reason': 'Must contain epoxide group, '
                                                'multiple hydroxyls, and a '
                                                'carboxylic acid group'},
                                  {   'smiles': 'CCCCC[C@@H](O)[C@H](O)\\C=C\\C=C\\C=C/C=C/[C@@H](O)CCCC(O)=O',
                                      'name': '15-epi-lipoxin B4',
                                      'reason': 'Must contain epoxide group, '
                                                'multiple hydroxyls, and a '
                                                'carboxylic acid group'},
                                  {   'smiles': 'C(\\[C@H](CCCC(O)=O)O)=C\\C=C\\C=C\\[C@@H](C\\C=C/C=C/[C@@H](CC)O)O',
                                      'name': 'resolvin E1',
                                      'reason': 'Must contain epoxide group, '
                                                'multiple hydroxyls, and a '
                                                'carboxylic acid group'},
                                  {   'smiles': 'O=C(CCC/C=C\\C/C=C\\C/C=C\\C(C(C(CCCCC)O)O)O)O',
                                      'name': '13,14,15-trihydroxy-(5Z,8Z,11Z)-icosatrienoic '
                                              'acid',
                                      'reason': 'Must contain epoxide group, '
                                                'multiple hydroxyls, and a '
                                                'carboxylic acid group'},
                                  {   'smiles': 'O=C(CCC/C=C\\C/C=C\\CC(C(/C=C/C(CCCCC)O)O)O)O',
                                      'name': '11,12,15-trihydroxy-(5Z,8Z,13E)-icosatrienoic '
                                              'acid',
                                      'reason': 'Must contain epoxide group, '
                                                'multiple hydroxyls, and a '
                                                'carboxylic acid group'},
                                  {   'smiles': 'CCCCC[C@H](O)[C@H](O)\\C=C\\C=C\\C=C/C=C/[C@@H](O)CCCC(O)=O',
                                      'name': 'lipoxin B4',
                                      'reason': 'Must contain epoxide group, '
                                                'multiple hydroxyls, and a '
                                                'carboxylic acid group'},
                                  {   'smiles': 'C(\\C=C/C=C/[C@@H](C/C=C\\CC)O)=C/C=C/C(C(CCCC(=O)O)O)O',
                                      'name': '(7E,9E,11Z,13E,15R,17Z)-5,6,15-trihydroxyicosapentaenoic '
                                              'acid',
                                      'reason': 'Must contain epoxide group, '
                                                'multiple hydroxyls, and a '
                                                'carboxylic acid group'},
                                  {   'smiles': 'C(/C=C\\C=C\\[C@H](CCCCCO)O)=C\\C=C\\[C@H]([C@H](CCCC(=O)O)O)O',
                                      'name': '20-hydroxylipoxin A4',
                                      'reason': 'Must contain epoxide group, '
                                                'multiple hydroxyls, and a '
                                                'carboxylic acid group'}],
    'attempt': 2,
    'reasoning': 'After analyzing the previous program and the errors '
                 'mentioned, we need to ensure the classification criteria are '
                 'met correctly for nonclassic icosanoids. From the outcomes, '
                 'it seems that the presence of specific functional groups '
                 'such as epoxides, hydroxyl groups, and carboxylic acids were '
                 'not adequately captured.\n'
                 '\n'
                 "Here's how we can improve the approach:\n"
                 '\n'
                 '1. **Correct Functional Groups Identification:**\n'
                 '   - Ensure the SMARTS patterns for identifying key '
                 'functional groups are accurate and improve them if necessary '
                 'based on typical structures in nonclassic icosanoids.\n'
                 '\n'
                 '2. **Avoiding Classic Icosanoids:**\n'
                 '   - The logic to avoid classic structures (prostanoids and '
                 'leukotrienes) should be re-evaluated and improved.\n'
                 '\n'
                 '3. **Coverage and Flexibility:**\n'
                 '   - Account for variations among nonclassic icosanoids in '
                 'terms of exact number and arrangement of functional groups '
                 'while ensuring specificity.\n'
                 '\n'
                 "Let's implement these improvements in the code:",
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 12,
    'num_false_positives': 57,
    'num_true_negatives': 142216,
    'num_false_negatives': 15,
    'num_negatives': None,
    'precision': 0.17391304347826086,
    'recall': 0.4444444444444444,
    'f1': 0.25,
    'accuracy': 0.9994940267041462,
    'negative_predictive_value': 0.9998945377589977}