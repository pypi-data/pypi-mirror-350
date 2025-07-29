"""
Classifies: CHEBI:55465 7-hydroxyisoflavones
"""
"""
Classifies: 7-hydroxyisoflavones
"""
from rdkit import Chem

def is_7_hydroxyisoflavones(smiles: str):
    """
    Determines if a molecule is a 7-hydroxyisoflavone based on its SMILES string.
    A 7-hydroxyisoflavone has a specific isoflavone structure with a hydroxyl group at the 7-position.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if the molecule is a 7-hydroxyisoflavone, False otherwise
        str: Reason for classification
    """
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
    
    # Isoflavone backbone pattern - aromatic rings with characteristic connectivity
    isoflavone_pattern = Chem.MolFromSmarts("Oc1ccc2c(c1)occ(-c1ccccc1)c2=O")
    if not mol.HasSubstructMatch(isoflavone_pattern):
        return False, "No isoflavone backbone with 7-hydroxy group found"

    return True, "Molecule is a 7-hydroxyisoflavone with the correct structure"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:55465',
                          'name': '7-hydroxyisoflavones',
                          'definition': 'A hydroxyisoflavone compound having a '
                                        'hydroxy group at the 7-position.',
                          'parents': ['CHEBI:38755'],
                          'xrefs': ['MetaCyc:7-hydroxyisoflavones'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 18,
                           'log_lines_of_code': 2.8903717578961645,
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
                                                 2,
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
                           'methods_called': [   'HasSubstructMatch',
                                                 'MolFromSmiles',
                                                 'MolFromSmarts'],
                           'methods_called_count': 3,
                           'smarts_strings': ['Oc1ccc2c(c1)occ(-c1ccccc1)c2=O'],
                           'smarts_strings_count': 1,
                           'defs': ['is_7_hydroxyisoflavones(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "No isoflavone backbone with '
                                          '7-hydroxy group found"',
                                          'True, "Molecule is a '
                                          '7-hydroxyisoflavone with the '
                                          'correct structure"'],
                           'returns_count': 3,
                           'complexity': 2.378074351579233},
    'message': None,
    'sample_true_negatives': [   {   'smiles': '[H][C@@]1(O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O)O[C@@H]1[C@@H](O)[C@@H](O)[C@@H](CO)O[C@H]1OC[C@H]1O[C@@H](OC[C@H]2O[C@@H](OC[C@H](NC(=O)[C@H](O)CCCCCCCCCCCCCCCCCCCCCC)[C@H](O)[C@H](O)CCCCCCCCCCCCCC)[C@H](O)[C@@H](O)[C@H]2O)[C@H](O)[C@@H](O)[C@H]1O',
                                     'name': 'Neurosporaside',
                                     'reason': 'No isoflavone backbone with '
                                               '7-hydroxy group found'},
                                 {   'smiles': '[O-]C(=O)C1=CN(C2CC2)C2=CC(N3CC[NH2+]CC3)=C(F)C=C2C1=O',
                                     'name': 'ciprofloxacin zwitterion',
                                     'reason': 'No isoflavone backbone with '
                                               '7-hydroxy group found'},
                                 {   'smiles': 'O=C1NC(=CC2=C1O[C@H]([C@@H](O)CC(C)C)O2)C',
                                     'name': 'Dihydroisoflavipucine',
                                     'reason': 'No isoflavone backbone with '
                                               '7-hydroxy group found'},
                                 {   'smiles': 'O=C1N2C(C(=O)N([C@@]2(OC)C)C[C@@H](O)C3=CC=CC=C3)=CC4=C1N(C=5C=CC=CC45)C',
                                     'name': 'Marinacarboline K',
                                     'reason': 'No isoflavone backbone with '
                                               '7-hydroxy group found'},
                                 {   'smiles': 'O1[C@@H](O[C@H]2[C@@H](O)[C@H](O)[C@H](O[C@@H]2OC[C@H]3OC(O)[C@@H](O)[C@@H](O)[C@@H]3O)CO)[C@H](NC(=O)C)[C@@H](O)[C@H](O[C@@H]4O[C@@H]([C@H](O)[C@H](O)[C@H]4O)CO[C@]5(O[C@H]([C@H](NC(=O)C)[C@@H](O)C5)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]1CO',
                                     'name': '(2R,4S,5R,6R)-5-Acetamido-2-[[(2R,3R,4S,5R,6S)-6-[(2R,3S,4R,5R,6S)-5-acetamido-6-[(2S,3S,4S,5S,6R)-4,5-dihydroxy-6-(hydroxymethyl)-2-[[(2R,3S,4S,5S)-3,4,5,6-tetrahydroxyoxan-2-yl]methoxy]oxan-3-yl]oxy-4-hydroxy-2-(hydroxymethyl)oxan-3-yl]oxy-3,4,5-trihydroxyoxan-2-yl]methoxy]-4-hydroxy-6-[(1R,2R)-1,2,3-trihydroxypropyl]oxane-2-carboxylic '
                                             'acid',
                                     'reason': 'No isoflavone backbone with '
                                               '7-hydroxy group found'},
                                 {   'smiles': 'O(C(=O)CCCCCCC)CCC1=CC=CC=C1',
                                     'name': '2-Phenylethyl octanoate',
                                     'reason': 'No isoflavone backbone with '
                                               '7-hydroxy group found'},
                                 {   'smiles': 'P(OCC(OC(=O)CCCCCCC/C=C\\CCCCCCCC)COC(=O)CCC/C=C\\C/C=C\\C/C=C\\CCCCCCCC)(OCCNC)(O)=O',
                                     'name': 'PE-NMe(20:3(5Z,8Z,11Z)/18:1(9Z))',
                                     'reason': 'No isoflavone backbone with '
                                               '7-hydroxy group found'},
                                 {   'smiles': 'O=C1C2=C(OC=3C1=CC=CN3)C(Cl)=CC(=C2)C=4NN=NN4',
                                     'name': 'traxanox',
                                     'reason': 'No isoflavone backbone with '
                                               '7-hydroxy group found'},
                                 {   'smiles': 'CCCCC(C)CCCCCC(C)CCCCCCCCCC(C)CC(O)=O',
                                     'name': '3,13,19-trimethyltricosanoic '
                                             'acid',
                                     'reason': 'No isoflavone backbone with '
                                               '7-hydroxy group found'},
                                 {   'smiles': 'COC(CC1=CC[C@]2(C)[C@@H](C)CCC[C@]2(C)C1=O)OC',
                                     'name': 'aignopsane ketal',
                                     'reason': 'No isoflavone backbone with '
                                               '7-hydroxy group found'}],
    'sample_false_negatives': [   {   'smiles': 'CC1(C)CCc2c(O)ccc(C3COc4cc(O)cc(O)c4C3=O)c2O1',
                                      'name': 'glyasperin F',
                                      'reason': 'No isoflavone backbone with '
                                                '7-hydroxy group found'},
                                  {   'smiles': 'CC(C)=CCc1c(O)ccc(C2COc3cc(O)cc(O)c3C2=O)c1O',
                                      'name': 'dihydrolicoisoflavone A',
                                      'reason': 'No isoflavone backbone with '
                                                '7-hydroxy group found'}],
    'attempt': 0,
    'reasoning': 'To classify chemical entities as 7-hydroxyisoflavones based '
                 'on their SMILES strings, we need to identify the presence of '
                 'an isoflavone backbone with a hydroxyl group specifically '
                 'located at the 7-position. Isoflavones typically have a '
                 'specific structure, and for this subclass, the hydroxyl '
                 "group on the 7-position is key. Let's break down the steps "
                 'required:\n'
                 '\n'
                 '1. **Parsing the SMILES String**: Convert the SMILES '
                 'representation of the molecule into a molecular graph model '
                 'using RDKit.\n'
                 '\n'
                 '2. **Identifying the Isoflavone Backbone**: An isoflavone '
                 'has a characteristic backbone; it is composed of a '
                 'benzopyrone structure fused with another aromatic ring. This '
                 'can be represented using SMARTS patterns.\n'
                 '\n'
                 '3. **Checking for the 7-Hydroxy Group**: For '
                 '7-hydroxyisoflavones, we need to locate the hydroxyl group '
                 'at the 7-position on the isoflavone backbone. This can also '
                 'be done using SMARTS by identifying the connectivity pattern '
                 'of an aromatic ring with the appropriate substituents.\n'
                 '\n'
                 "Here's an implementation using these concepts:",
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 28,
    'num_false_positives': 328,
    'num_true_negatives': 141942,
    'num_false_negatives': 2,
    'num_negatives': None,
    'precision': 0.07865168539325842,
    'recall': 0.9333333333333333,
    'f1': 0.1450777202072539,
    'accuracy': 0.9976809557273366,
    'negative_predictive_value': 0.9999859099363129}