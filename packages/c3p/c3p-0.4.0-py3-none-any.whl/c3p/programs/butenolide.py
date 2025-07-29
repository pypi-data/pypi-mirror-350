"""
Classifies: CHEBI:50523 butenolide
"""
"""
Classifies: CHEBI:30810 butenolide
A gamma-lactone that consists of a 2-furanone skeleton and its substituted derivatives.
"""

from rdkit import Chem
from rdkit.Chem import AllChem

def is_butenolide(smiles: str) -> tuple[bool, str]:
    """
    Determines if a molecule is a butenolide based on its SMILES string.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a butenolide, False otherwise
        str: Reason for classification
    """
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Look for 2-furanone skeleton
    furanone_pattern = Chem.MolFromSmarts("O=C1OCC=C1")
    if not mol.HasSubstructMatch(furanone_pattern):
        return False, "Missing 2-furanone skeleton"

    # Check for substitutions on the furanone ring
    substituted_pattern = Chem.MolFromSmarts("O=C1OC(*)C=C1*")
    if not mol.HasSubstructMatch(substituted_pattern):
        return True, "Unsubstituted 2-furanone skeleton (butenolide)"

    # Check for specific substitutions (optional)
    # ...

    return True, "Contains a substituted 2-furanone skeleton (butenolide)"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:50523',
                          'name': 'butenolide',
                          'definition': 'A gamma-lactone that consists of a '
                                        '2-furanone skeleton and its '
                                        'substituted derivatives.',
                          'parents': ['CHEBI:24129', 'CHEBI:37581'],
                          'xrefs': ['Wikipedia:Butenolide'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 23,
                           'log_lines_of_code': 3.1354942159291497,
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
                                                 0,
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
                                                 0,
                                                 1],
                           'max_indent': 2,
                           'imports': [   'from rdkit import Chem',
                                          'from rdkit.Chem import AllChem'],
                           'imports_count': 2,
                           'methods_called': [   'MolFromSmarts',
                                                 'MolFromSmiles',
                                                 'HasSubstructMatch'],
                           'methods_called_count': 3,
                           'smarts_strings': ['O=C1OC(*)C=C1*', 'O=C1OCC=C1'],
                           'smarts_strings_count': 2,
                           'defs': [   'is_butenolide(smiles: str) -> '
                                       'tuple[bool, str]:'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "Missing 2-furanone '
                                          'skeleton"',
                                          'True, "Unsubstituted 2-furanone '
                                          'skeleton (butenolide)"',
                                          'True, "Contains a substituted '
                                          '2-furanone skeleton (butenolide)"'],
                           'returns_count': 4,
                           'complexity': 2.6270988431858298},
    'message': None,
    'sample_true_negatives': [   {   'smiles': 'C[C@@H](O)CCCCCCCCCCC[C@@H](O)CC(O)=O',
                                     'name': '(3R,15R)-3,15-dihydroxypalmitic '
                                             'acid',
                                     'reason': 'Missing 2-furanone skeleton'},
                                 {   'smiles': 'O1CC(CC2=CC=C(OC)C=C2)C(=O)C3=C1C=C(O)C=C3',
                                     'name': 'Dihydrobonducellin',
                                     'reason': 'Missing 2-furanone skeleton'},
                                 {   'smiles': 'O(C(=O)CCCCC/C=C/C=C)C\\C=C\\CCC',
                                     'name': '(E)-2-Hexenyl '
                                             '(E)-7,9-decadienoate',
                                     'reason': 'Missing 2-furanone skeleton'},
                                 {   'smiles': 'O=C(O[C@H](C[C@H]1O[C@@H]([C@H](C(=O)O)C)CC1)CC)[C@H]([C@H]2O[C@@H](C[C@H](O)CC)CC2)C',
                                     'name': 'Homononactyl homononactate',
                                     'reason': 'Missing 2-furanone skeleton'},
                                 {   'smiles': 'O=C(O)/C=C/C=C/[C@@H]1[C@@H](C(=C[C@H]2[C@H]1[C@H](C[C@H](C2)O)C)C)C(=CCOC(=O)C)C',
                                     'name': 'Carneic acid M',
                                     'reason': 'Missing 2-furanone skeleton'},
                                 {   'smiles': 'O=C1OC(=CC=C1CC(O)(C)C)CC',
                                     'name': '10-hydroxymucidone',
                                     'reason': 'Missing 2-furanone skeleton'},
                                 {   'smiles': 'COC1=C(C=C(C=C1)C=NNC2=C(C(=NC=N2)Cl)N)OC',
                                     'name': '6-chloro-N4-[(3,4-dimethoxyphenyl)methylideneamino]pyrimidine-4,5-diamine',
                                     'reason': 'Missing 2-furanone skeleton'},
                                 {   'smiles': 'c1cc2ccc3cc4ccc5ccc6ccc7cc8ccc1c1c2c3c2c4c5c6c7c2c81',
                                     'name': 'ovalene',
                                     'reason': 'Missing 2-furanone skeleton'},
                                 {   'smiles': 'Cc1cn2c(nc3n(cnc3c2=O)[C@@H]2O[C@H](CO)[C@@H](O)[C@H]2O)[nH]1',
                                     'name': '4-demethylwyosine',
                                     'reason': 'Missing 2-furanone skeleton'},
                                 {   'smiles': 'S(C=1N(C(=NN1)C=2C=CC=NC2)C)CC(=O)NNC(=O)C3=CC=C(OC)C=C3',
                                     'name': 'N-(4-Methoxybenzoyl)-2-{[4-methyl-5-(pyridin-3-yl)-4H-1,2,4-triazol-3-yl]sulfanyl}ethanehydrazonic '
                                             'acid',
                                     'reason': 'Missing 2-furanone skeleton'}],
    'sample_false_negatives': [   {   'smiles': 'O=C1OC(CCCCC[C@H](CC)C)=CC1',
                                      'name': '10-Methyldodec-3-en-4-olide',
                                      'reason': 'Missing 2-furanone skeleton'},
                                  {   'smiles': 'C(C(C1C(C(C(=O)O1)O)O)=N)O',
                                      'name': '3,4-dihydroxy-5-(2-hydroxyethanimidoyl)oxolan-2-one',
                                      'reason': 'Missing 2-furanone skeleton'},
                                  {   'smiles': 'Oc1ccc(\\C=C2\\C=C(OC2=O)c2ccc(O)c(O)c2)cc1O',
                                      'name': '(Z)-3-(3,4-dihydroxybenzylidene)-5-(3,4-dihydroxyphenyl)-2(3H)-furanone',
                                      'reason': 'Missing 2-furanone skeleton'},
                                  {   'smiles': 'Oc1ccc(cc1O)\\C=C1/C=C(OC1=O)c1ccc(O)c(O)c1',
                                      'name': 'BE-23372M',
                                      'reason': 'Missing 2-furanone skeleton'},
                                  {   'smiles': 'O1C(CCCCC)=CCC1=O',
                                      'name': '5-Pentyl-3h-furan-2-one',
                                      'reason': 'Missing 2-furanone skeleton'},
                                  {   'smiles': 'OC(=O)CC1=CCC(=O)O1',
                                      'name': '5-oxo-4,5-dihydro-2-furylacetic '
                                              'acid',
                                      'reason': 'Missing 2-furanone skeleton'},
                                  {   'smiles': 'O.[H][C@@]1(OC(=O)C(=O)C1=O)[C@@H](O)CO',
                                      'name': 'L-dehydroascorbic acid hydrate',
                                      'reason': 'Missing 2-furanone skeleton'},
                                  {   'smiles': 'O[C@@]12[C@@]([C@](CC1)([C@]3(CC(OC3)=O)[H])[H])([C@H](O)C[C@]4(C2CC[C@]5([C@@]4(CC[C@H](O)C5)C)[H])[H])C',
                                      'name': '20, 22-Dihydrodigoxigenin',
                                      'reason': 'Missing 2-furanone skeleton'},
                                  {   'smiles': '[H][C@@]1(OC(=O)C(=O)C1=O)[C@@H](O)CO',
                                      'name': 'L-dehydroascorbic acid',
                                      'reason': 'Missing 2-furanone skeleton'},
                                  {   'smiles': '[H][C@@]1(CC[C@]2(O)[C@]3([H])CC[C@]4(O)C[C@H](C[C@@H](O)[C@]4(CO)[C@@]3([H])[C@H](O)C[C@]12C)O[C@@H]1O[C@@H](C)[C@H](O)[C@@H](O)[C@H]1O)C1COC(=O)C1',
                                      'name': 'dihydroouabain',
                                      'reason': 'Missing 2-furanone skeleton'}],
    'attempt': 0,
    'reasoning': '',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 415,
    'num_false_positives': 908,
    'num_true_negatives': 140967,
    'num_false_negatives': 10,
    'num_negatives': None,
    'precision': 0.31368102796674224,
    'recall': 0.9764705882352941,
    'f1': 0.47482837528604116,
    'accuracy': 0.9935488404778636,
    'negative_predictive_value': 0.9999290664434624}