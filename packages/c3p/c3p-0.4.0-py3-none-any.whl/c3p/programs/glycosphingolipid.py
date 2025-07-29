"""
Classifies: CHEBI:24402 glycosphingolipid
"""
from rdkit import Chem

def is_glycosphingolipid(smiles: str):
    """
    Determines if a molecule is a glycosphingolipid based on its SMILES string.
    A glycosphingolipid must contain both a sphingoid/ceramide backbone and a carbohydrate residue
    attached via a glycosidic linkage to O-1 of the sphingoid.
    
    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a glycosphingolipid, False otherwise
        str: Reason for classification
    """
    
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # General glycosidic linkage (CHO linkages)
    glycosidic_pattern = Chem.MolFromSmarts("[C][O][*R]") # C linked to an O part of a ring
    if not mol.HasSubstructMatch(glycosidic_pattern):
        return False, "No glycosidic linkage found"

    # General sphingoid base (e.g., base structures of ceramide)
    sphingoid_pattern = Chem.MolFromSmarts("N[C@@H](CO)[C@@H](O)CCCCCCCCCCC")
    if not mol.HasSubstructMatch(sphingoid_pattern):
        return False, "No sphingoid/ceramide backbone found"

    # Both the patterns should be present for the classification as glycosphingolipid
    return True, "Contains sphingoid/ceramide backbone with glycosidic linkage to carbohydrate"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:24402',
                          'name': 'glycosphingolipid',
                          'definition': 'A glycosphingolipid is a glycolipid '
                                        'that is a carbohydrate-containing '
                                        'derivative of a sphingoid or '
                                        'ceramide. It is understood that the '
                                        'carbohydrate residue is attached by a '
                                        'glycosidic linkage to O-1 of the '
                                        'sphingoid.',
                          'parents': ['CHEBI:26739', 'CHEBI:33563'],
                          'xrefs': [   'PMID:18845618',
                                       'PMID:19303901',
                                       'PMID:26954668',
                                       'PMID:26976737',
                                       'PMID:27253729',
                                       'PMID:27325407',
                                       'Wikipedia:Glycosphingolipid'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 24,
                           'log_lines_of_code': 3.1780538303479458,
                           'indent_by_line': [   1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
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
                                                 2,
                                                 0,
                                                 1,
                                                 1],
                           'max_indent': 2,
                           'imports': ['from rdkit import Chem'],
                           'imports_count': 1,
                           'methods_called': [   'MolFromSmarts',
                                                 'HasSubstructMatch',
                                                 'MolFromSmiles'],
                           'methods_called_count': 3,
                           'smarts_strings': [   'N[C@@H](CO)[C@@H](O)CCCCCCCCCCC',
                                                 '[C][O][*R]'],
                           'smarts_strings_count': 2,
                           'defs': ['is_glycosphingolipid(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "No glycosidic linkage '
                                          'found"',
                                          'False, "No sphingoid/ceramide '
                                          'backbone found"',
                                          'True, "Contains sphingoid/ceramide '
                                          'backbone with glycosidic linkage to '
                                          'carbohydrate"'],
                           'returns_count': 4,
                           'complexity': 2.635610766069589},
    'message': '\n'
               'Attempt failed: F1 score of 0 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: NONE\n'
               'False positives: NONE\n'
               'False negatives: SMILES: '
               'CCCCCCCCCCCCCCCCCCCCCC(=O)N[C@@H](CO[C@@H]1O[C@H](CO)[C@H](O)[C@H](O)[C@H]1O)[C@H](O)CCCCCCCCCCCCCCC '
               "NAME: beta-D-galactosyl-(1<->1')-N-docosanoylsphinganine "
               'REASON: MISSED No glycosidic linkage found\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCCCC(=O)N[C@@H](CO[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O)[C@H](O)\\C=C\\CCCCCCCCCCCCC '
               'NAME: beta-D-glucosyl-N-eicosanoylsphingosine REASON: MISSED '
               'No glycosidic linkage found\n'
               ' * SMILES: '
               'O=C(N[C@H]([C@H](O)/C=C/CC/C=C(/CCCCCCCCC)\\C)CO[C@H]1O[C@@H]([C@@H](O)[C@@H]([C@H]1O)O)CO)CCCCCCCCCCCCCCC '
               'NAME: Thraustochytroside B REASON: MISSED No glycosidic '
               'linkage found\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCCCCCCCCC(=O)N[C@@H](CO[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O)[C@H](O)\\C=C\\CCCCCCCCCC(C)C '
               'NAME: '
               'N-pentacosanoyl-1-O-beta-D-glucosyl-15-methylhexadecasphing-4-enine '
               'REASON: MISSED No glycosidic linkage found\n'
               ' * SMILES: '
               'C(CCCCCC(CC)C)CC\\C=C\\[C@@H](O)[C@@H](NC(CCCCCCCCCCCCCCCCCCCCCCCCC)=O)CO[C@@H]1O[C@@H]([C@@H](O)[C@@H]([C@H]1O)O)CO '
               'NAME: '
               "beta-D-glucosyl-(1<->1')-N-hexacosanoyl-14-methylhexadecasphingosine "
               'REASON: MISSED No glycosidic linkage found\n'
               ' * SMILES: '
               'CCCCCCCCCCCCC\\C=C\\[C@@H](O)[C@H](CO[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O)NC(=O)CCCCCCC '
               'NAME: C8 beta-D-glucosyl N-acylsphingosine REASON: MISSED No '
               'glycosidic linkage found\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCCCCCCC(O)C(=O)N[C@@H](COP(O)(=O)O[C@@H]1[C@H](O)[C@H](O)[C@@H](O)[C@H](O)[C@H]1O[C@@H]1O[C@H](COP(O)(=O)O[C@H]2[C@H](O)[C@@H](O)[C@H](O)[C@@H](O)[C@H]2O)[C@@H](O)[C@H](O)[C@@H]1O)[C@H](O)CCCCCCCCCCCCCCC '
               'NAME: Ins-1-P-6-Man-beta1-6-Ins-1-P-Cer(d18:0/2-OH-24:0) '
               'REASON: MISSED No glycosidic linkage found\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCCCCCCCC(=O)N[C@@H](CO[C@@H]1O[C@H](CO)[C@H](O)[C@H](OS(O)(=O)=O)[C@H]1O)[C@H](O)\\C=C\\CCCCCCCCCCCCC '
               'NAME: '
               '1-(3-O-sulfo-beta-D-galactosyl)-N-tetracosanoylsphingosine '
               'REASON: MISSED No glycosidic linkage found\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCCCC(=O)N[C@@H](CO[C@@H]1O[C@H](CO)[C@H](O)[C@H](O)[C@H]1O)[C@H](O)CCCCCCCCCCCCCCC '
               "NAME: beta-D-galactosyl-(1<->1')-N-eicosanoylsphinganine "
               'REASON: MISSED No glycosidic linkage found\n'
               ' * SMILES: '
               'O=C(N[C@H]([C@H](O)/C=C/CC/C=C(/CCCCCCCCCCCC)\\C)CO[C@@H]1O[C@@H]([C@@H](O)[C@@H]([C@H]1O)O)CO)[C@H](O)CCCCCCCCCCCCC '
               'NAME: Allantoside REASON: MISSED No glycosidic linkage found\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'CN(C)C1=CC2=C(C=C1)O[C@@H]3[C@H]2C[C@@H](O[C@H]3CO)CC(=O)NCCN4CCCCC4',
                                     'name': '2-[(1S,3R,4aS,9aR)-6-(dimethylamino)-1-(hydroxymethyl)-3,4,4a,9a-tetrahydro-1H-pyrano[3,4-b]benzofuran-3-yl]-N-[2-(1-piperidinyl)ethyl]acetamide',
                                     'reason': 'No sphingoid/ceramide backbone '
                                               'found'},
                                 {   'smiles': 'C[C@@H](C(=O)O)NC(=O)OC(C)(C)C',
                                     'name': 'N-Boc-L-alanine',
                                     'reason': 'No glycosidic linkage found'},
                                 {   'smiles': 'O=C1C2=C(O)C(=C(O)C=C2C(=O)C=3C1=C(O)C=C(O)C3)/C=C/CCCC',
                                     'name': 'Averythrin',
                                     'reason': 'No glycosidic linkage found'},
                                 {   'smiles': 'O=C(N[C@@H](CC=1NC=NC1)C(O)=O)[C@@H](NC(=O)[C@@H](N)CCC(=O)N)[C@H](CC)C',
                                     'name': 'Gln-Ile-His',
                                     'reason': 'No glycosidic linkage found'},
                                 {   'smiles': 'O1C2C3C(CCC3=C)C(CCC2C(C1=O)=C)=C',
                                     'name': '3,6,9-Trimethylidene-3a,4,5,6a,7,8,9a,9b-octahydroazuleno[4,5-b]furan-2-one',
                                     'reason': 'No sphingoid/ceramide backbone '
                                               'found'},
                                 {   'smiles': 'C1CN(CC2=CC=CC=C21)CCCNC(=O)CN3C(=O)COC4=CC=CC=C43',
                                     'name': 'N-[3-(3,4-dihydro-1H-isoquinolin-2-yl)propyl]-2-(3-oxo-1,4-benzoxazin-4-yl)acetamide',
                                     'reason': 'No sphingoid/ceramide backbone '
                                               'found'},
                                 {   'smiles': 'Cc1c(c[nH]c1C(=O)Nc1c(O)c2ccc(O)c(C)c2oc1=O)C(O)=O',
                                     'name': 'Coumeroic acid',
                                     'reason': 'No glycosidic linkage found'},
                                 {   'smiles': 'O=C1OC(=CC(=C1CCCCCC)O)CC(C)C',
                                     'name': 'Photopyrone A',
                                     'reason': 'No glycosidic linkage found'},
                                 {   'smiles': '[C@H]1(O)[C@@H](O)O[C@H](CS(O)(=O)=O)[C@H]([C@@H]1O)O',
                                     'name': '6-sulfo-alpha-D-quinovose',
                                     'reason': 'No sphingoid/ceramide backbone '
                                               'found'},
                                 {   'smiles': 'SC[C@H](NC(=O)CNC(=O)[C@@H](N)CC(O)=O)C(O)=O',
                                     'name': 'Asp-Gly-Cys',
                                     'reason': 'No glycosidic linkage found'}],
    'sample_false_negatives': [   {   'smiles': 'CCCCCCCCCCCCCCCCCCCC(=O)N[C@@H](CO[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O)[C@H](O)\\C=C\\CCCCCCCCCCCCC',
                                      'name': 'beta-D-glucosyl-N-eicosanoylsphingosine',
                                      'reason': 'No sphingoid/ceramide '
                                                'backbone found'},
                                  {   'smiles': 'O=C(N[C@H]([C@H](O)/C=C/CC/C=C(/CCCCCCCCC)\\C)CO[C@H]1O[C@@H]([C@@H](O)[C@@H]([C@H]1O)O)CO)CCCCCCCCCCCCCCC',
                                      'name': 'Thraustochytroside B',
                                      'reason': 'No sphingoid/ceramide '
                                                'backbone found'},
                                  {   'smiles': 'CCCCCCCCCCCCCCCCCCCCCCCCC(=O)N[C@@H](CO[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O)[C@H](O)\\C=C\\CCCCCCCCCC(C)C',
                                      'name': 'N-pentacosanoyl-1-O-beta-D-glucosyl-15-methylhexadecasphing-4-enine',
                                      'reason': 'No sphingoid/ceramide '
                                                'backbone found'},
                                  {   'smiles': 'C(CCCCCC(CC)C)CC\\C=C\\[C@@H](O)[C@@H](NC(CCCCCCCCCCCCCCCCCCCCCCCCC)=O)CO[C@@H]1O[C@@H]([C@@H](O)[C@@H]([C@H]1O)O)CO',
                                      'name': "beta-D-glucosyl-(1<->1')-N-hexacosanoyl-14-methylhexadecasphingosine",
                                      'reason': 'No sphingoid/ceramide '
                                                'backbone found'},
                                  {   'smiles': 'CCCCCCCCCCCCC\\C=C\\[C@@H](O)[C@H](CO[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O)NC(=O)CCCCCCC',
                                      'name': 'C8 beta-D-glucosyl '
                                              'N-acylsphingosine',
                                      'reason': 'No sphingoid/ceramide '
                                                'backbone found'},
                                  {   'smiles': 'CCCCCCCCCCCCCCCCCCCCCCCC(=O)N[C@@H](CO[C@@H]1O[C@H](CO)[C@H](O)[C@H](OS(O)(=O)=O)[C@H]1O)[C@H](O)\\C=C\\CCCCCCCCCCCCC',
                                      'name': '1-(3-O-sulfo-beta-D-galactosyl)-N-tetracosanoylsphingosine',
                                      'reason': 'No sphingoid/ceramide '
                                                'backbone found'},
                                  {   'smiles': 'O=C(N[C@H]([C@H](O)/C=C/CC/C=C(/CCCCCCCCCCCC)\\C)CO[C@@H]1O[C@@H]([C@@H](O)[C@@H]([C@H]1O)O)CO)[C@H](O)CCCCCCCCCCCCC',
                                      'name': 'Allantoside',
                                      'reason': 'No sphingoid/ceramide '
                                                'backbone found'},
                                  {   'smiles': 'CCCCCCCCCCCCCCCCCCCCC(O)C(=O)N[C@@H](COC1O[C@H](CO)[C@H](O)[C@H](O)[C@H]1O)[C@H](O)\\C=C\\CCCCCCCCCCCCC',
                                      'name': 'N-(2-hydroxybehenoyl)-D-galactosylsphingosine',
                                      'reason': 'No sphingoid/ceramide '
                                                'backbone found'},
                                  {   'smiles': 'C(=C/CCCCCCCCCCCCC)\\[C@@H](O)[C@@H](NC(CCCCCCCCCCCCCCCCCCCCCCCC)=O)CO[C@H]1[C@@H]([C@H]([C@H]([C@H](O1)CO)O[C@@H]2[C@@H]([C@H]([C@H]([C@H](O2)CO)O)O)O)O)O',
                                      'name': 'alpha-D-galactosyl-(1->4)-beta-D-galactosyl-N-(pentacosanoyl)sphingosine',
                                      'reason': 'No sphingoid/ceramide '
                                                'backbone found'},
                                  {   'smiles': 'CCCCCCCCCCCCCCCCCC(=O)N[C@@H](CO[C@@H]1O[C@H](CO)[C@@H](O[C@@H]2O[C@H](CO)[C@H](O[C@@H]3O[C@H](CO)[C@H](O)[C@H](O)[C@H]3NC(C)=O)[C@H](O[C@@]3(C[C@H](O)[C@@H](NC(C)=O)[C@@H](O3)[C@H](O)[C@@H](CO)O[C@@]3(C[C@H](O)[C@@H](NC(C)=O)[C@@H](O3)[C@H](O)[C@@H](CO)O[C@@]3(C[C@H](O)[C@@H](NC(C)=O)[C@@H](O3)[C@H](O)[C@H](O)CO)C(O)=O)C(O)=O)C(O)=O)[C@H]2O)[C@H](O)[C@H]1O)[C@H](O)\\C=C\\CCCCCCCCCCCCC',
                                      'name': "beta-GalNAc-(1->4)-[alpha-Neu5Ac-(2->8)-alpha-Neu5Ac-(2->8)-alpha-Neu5Ac-(2->3)]-beta-Gal-(1->4)-beta-Glc-(1->1')-Cer(d18:1/18:0)",
                                      'reason': 'No sphingoid/ceramide '
                                                'backbone found'}],
    'attempt': 2,
    'reasoning': 'To improve the classification of glycosphingolipids based on '
                 "their SMILES strings, let's analyze the outcomes and "
                 'problems from the previous attempt:\n'
                 '\n'
                 '1. **Reason Analysis**: The error messages indicate that the '
                 'system failed to detect the glycosidic linkage correctly. '
                 'This result could arise due to the specific SMARTS pattern '
                 'used, which may not adequately capture the diversity of '
                 'glycosidic linkages in the given compounds.\n'
                 '\n'
                 '2. **Pattern Matching**: The previous program used a '
                 'carbohydrate moiety pattern that might be too specific. '
                 'Glycosidic linkages can vary, and the presence of only '
                 'pyranose sugars was considered. Therefore, the SMARTS '
                 'pattern for identifying glycosidic linkages should be '
                 'versatile enough to capture different carbohydrates.\n'
                 '\n'
                 '3. **Sphingoid/Ceramide Detection**: The pattern for '
                 'detecting the sphingoid/ceramide backbone might also need '
                 'refining. Glycosphingolipids include sphingomyelin-based '
                 'lipids and ceramides, so the pattern should account for '
                 'variations in chain length and unsaturation.\n'
                 '\n'
                 '### Improved Approach\n'
                 '\n'
                 '1. **General Glycosidic Linkage Detection**: Create a more '
                 'general pattern to capture any glycosidic linkage, which '
                 'could start with a carbon connected to an oxygen link '
                 'leading into a ring.\n'
                 '\n'
                 '2. **Sphingoid Backbone Pattern**: Broaden the search '
                 'pattern for sphingoids to ensure it captures variations in '
                 'chain lengths, presence of hydroxyl groups, and double '
                 'bonds.\n'
                 '\n'
                 '3. **Combination of Patterns**: Ensure logical ANDing of the '
                 'two patterns to increase the reliability of detecting both '
                 'features in a single molecule.\n'
                 '\n'
                 "Given these analyses and improvements, here's the revised "
                 'code:',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 93,
    'num_false_positives': 108,
    'num_true_negatives': 141847,
    'num_false_negatives': 252,
    'num_negatives': None,
    'precision': 0.4626865671641791,
    'recall': 0.26956521739130435,
    'f1': 0.34065934065934067,
    'accuracy': 0.9974701335207309,
    'negative_predictive_value': 0.9982265885051971}