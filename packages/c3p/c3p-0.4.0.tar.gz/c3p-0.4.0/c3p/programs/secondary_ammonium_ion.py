"""
Classifies: CHEBI:137419 secondary ammonium ion
"""
"""
Classifies: CHEBI:39143 secondary ammonium ion
"""
from rdkit import Chem

def is_secondary_ammonium_ion(smiles: str):
    """
    Determines if a molecule is a secondary ammonium ion based on its SMILES string.
    A secondary ammonium ion has a nitrogen atom with +1 charge bonded to exactly two carbons (protonated secondary amine).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a secondary ammonium ion, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Iterate through all nitrogen atoms
    for atom in mol.GetAtoms():
        # Check for positively charged nitrogen
        if atom.GetAtomicNum() == 7 and atom.GetFormalCharge() == 1:
            # Count carbon neighbors
            carbon_count = sum(1 for neighbor in atom.GetNeighbors() 
                              if neighbor.GetAtomicNum() == 6)
            
            # Secondary ammonium has exactly two carbon neighbors
            if carbon_count == 2:
                return True, "Positively charged nitrogen with two carbon substituents"
    
    return False, "No secondary ammonium group (N+ with two carbons) found"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:137419',
                          'name': 'secondary ammonium ion',
                          'definition': 'An organic cation obtained by '
                                        'protonation of any secondary amino '
                                        'compound; major species at pH 7.3.',
                          'parents': ['CHEBI:25697', 'CHEBI:35274'],
                          'xrefs': ['MetaCyc:Secondary-Amines'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 23,
                           'log_lines_of_code': 3.1354942159291497,
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
                                                 2,
                                                 0,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 3,
                                                 3,
                                                 3,
                                                 3,
                                                 3,
                                                 3,
                                                 4,
                                                 1,
                                                 1],
                           'max_indent': 4,
                           'imports': ['from rdkit import Chem'],
                           'imports_count': 1,
                           'methods_called': [   'GetFormalCharge',
                                                 'GetNeighbors',
                                                 'MolFromSmiles',
                                                 'GetAtomicNum',
                                                 'GetAtoms'],
                           'methods_called_count': 5,
                           'smarts_strings': [],
                           'smarts_strings_count': 0,
                           'defs': ['is_secondary_ammonium_ion(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'True, "Positively charged nitrogen '
                                          'with two carbon substituents"',
                                          'False, "No secondary ammonium group '
                                          '(N+ with two carbons) found"'],
                           'returns_count': 3,
                           'complexity': 3.22709884318583},
    'message': None,
    'sample_true_negatives': [   {   'smiles': 'OC[C@H]1O[C@@H](Oc2ccc(\\C=C\\C(=O)OC[C@H]3O[C@@H](Oc4cc5c(O[C@@H]6O[C@H](COC(=O)CC(O)=O)[C@@H](O)[C@H](O)[C@H]6O)cc(O)cc5[o+]c4-c4ccc(O)c(O)c4)[C@H](O[C@@H]4OC[C@@H](O)[C@H](O)[C@H]4O)[C@@H](O)[C@@H]3O)cc2)[C@H](O)[C@@H](O)[C@@H]1O',
                                     'name': 'cyanidin '
                                             '3-O-[6-O-(4-O-beta-D-glucosyl-p-coumaroyl)-2-O-(beta-D-xylosyl)-beta-D-glucosyl]-5-O-(6-O-malonyl-beta-D-glucoside)',
                                     'reason': 'No secondary ammonium group '
                                               '(N+ with two carbons) found'},
                                 {   'smiles': 'C1=CC(=NC2=C1C(=CC(=N2)C(F)(F)F)C(F)(F)F)NN',
                                     'name': '[5,7-bis(trifluoromethyl)-1,8-naphthyridin-2-yl]hydrazine',
                                     'reason': 'No secondary ammonium group '
                                               '(N+ with two carbons) found'},
                                 {   'smiles': 'C[C@H]1CN(S(=O)(=O)C2=C(C=C(C=C2)C#CCC(C)C)O[C@@H]1CN(C)C(=O)CC3=CN=CC=C3)[C@@H](C)CO',
                                     'name': 'N-[[(4S,5S)-2-[(2S)-1-hydroxypropan-2-yl]-4-methyl-8-(4-methylpent-1-ynyl)-1,1-dioxo-4,5-dihydro-3H-6,1$l^{6},2-benzoxathiazocin-5-yl]methyl]-N-methyl-2-(3-pyridinyl)acetamide',
                                     'reason': 'No secondary ammonium group '
                                               '(N+ with two carbons) found'},
                                 {   'smiles': 'O1C2=C(C3=C(OC)C=4C(C=C3OC)=CC=5OC(=CC(=O)C5C4O)C)C6=C(C(O)=C2C(=O)C=C1C)C(OC)=CC(OC)=C6',
                                     'name': 'aurasperone A',
                                     'reason': 'No secondary ammonium group '
                                               '(N+ with two carbons) found'},
                                 {   'smiles': 'O[C@]1([C@@H](OC)C(=O)NC2=C1C(O)=C(C=C2)/C=C/C(=C)C)C3=CC=C(OC)C=C3',
                                     'name': 'yaequinolone E',
                                     'reason': 'No secondary ammonium group '
                                               '(N+ with two carbons) found'},
                                 {   'smiles': 'CC1=C(C=CC(=C1)F)S(=O)(=O)NC2=CC=CC=C2C(=O)NCC3=CN=CC=C3',
                                     'name': '2-[(4-fluoro-2-methylphenyl)sulfonylamino]-N-(3-pyridinylmethyl)benzamide',
                                     'reason': 'No secondary ammonium group '
                                               '(N+ with two carbons) found'},
                                 {   'smiles': 'CC1=C(C=CC(=C1)O)N=CC2CCCC2=O',
                                     'name': 'LSM-27175',
                                     'reason': 'No secondary ammonium group '
                                               '(N+ with two carbons) found'},
                                 {   'smiles': 'O(CC(C1C2(C(CC1)/C(/CCC2)=C/C=C\\3/CC(O)CC(O)C3=C)C)C)C=4C=C(C=CC4)C(O)(C)C',
                                     'name': '(1R,3S,5Z)-5-[(2Z)-2-[(1R,3Ar,7aS)-1-[(2S)-1-[3-(2-hydroxypropan-2-yl)phenoxy]propan-2-yl]-7a-methyl-2,3,3a,5,6,7-hexahydro-1H-inden-4-ylidene]ethylidene]-4-methylidenecyclohexane-1,3-diol',
                                     'reason': 'No secondary ammonium group '
                                               '(N+ with two carbons) found'},
                                 {   'smiles': 'O1[C@@H]([C@H](N(CC=2N(C=CN2)C)C(=O)C1)CO)C3=CC=C(NC(=O)C(C)C)C=C3',
                                     'name': 'N-(4-{(2r,3r)-3-(hydroxymethyl)-4-[(1-methyl-1h-imidazol-2-yl)methyl]-5-oxo-2-morpholinyl}phenyl)-2-methylpropanamide',
                                     'reason': 'No secondary ammonium group '
                                               '(N+ with two carbons) found'},
                                 {   'smiles': 'O=C1OC(C2=CC=C(OC)C=C2)=CC3=C1C[C@]4(O)[C@@]5([C@](O)(C([C@H](OC(=O)C)C[C@@H]5O)(C)C)CC[C@]4(O3)C)C',
                                     'name': 'Arisugacin H',
                                     'reason': 'No secondary ammonium group '
                                               '(N+ with two carbons) found'}],
    'sample_false_negatives': [   {   'smiles': 'C(CC[NH3+])CC[NH+](C)C',
                                      'name': 'N,N-dimethyl-cadaverine(+2)',
                                      'reason': 'No secondary ammonium group '
                                                '(N+ with two carbons) found'}],
    'attempt': 0,
    'reasoning': '',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 26,
    'num_false_positives': 100,
    'num_true_negatives': 16765,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.20634920634920634,
    'recall': 0.9629629629629629,
    'f1': 0.3398692810457516,
    'accuracy': 0.9940208382666351,
    'negative_predictive_value': 0.9999403554813313}