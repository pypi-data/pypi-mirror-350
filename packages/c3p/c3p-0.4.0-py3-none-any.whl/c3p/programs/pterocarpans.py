"""
Classifies: CHEBI:26377 pterocarpans
"""
"""
Classifies: CHEBI:51811 pterocarpan
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_pterocarpans(smiles: str):
    """
    Determines if a molecule is a pterocarpan based on its SMILES string.
    Pterocarpans are members of the class of benzofurochromene with a
    6a,11a-dihydro-6H-[1]benzofuro[3,2-c]chromene skeleton and its substituted derivatives.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a pterocarpan, False otherwise
        str: Reason for classification
    """
    
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Look for pterocarpan scaffold pattern
    scaffold_pattern = Chem.MolFromSmarts("[C@]12Oc3ccccc3[C@@]1(O)COc1ccccc21")
    if mol.HasSubstructMatch(scaffold_pattern):
        # Check for fused rings
        fused_rings = AllChem.GetSymmSSSR(mol)
        if len(fused_rings) >= 4:
            return True, "Contains the pterocarpan scaffold with required fused rings"
        else:
            return False, "Does not have enough fused rings"
    else:
        # Check for substituted pterocarpan scaffold
        substituted_pattern = Chem.MolFromSmarts("[C@]12Oc3c(*)cccc3[C@@]1(O)COc1c(**)cccc21")
        if mol.HasSubstructMatch(substituted_pattern):
            fused_rings = AllChem.GetSymmSSSR(mol)
            if len(fused_rings) >= 4:
                return True, "Contains a substituted pterocarpan scaffold with required fused rings"
            else:
                return False, "Does not have enough fused rings"
        else:
            return False, "Does not contain the pterocarpan scaffold"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:26377',
                          'name': 'pterocarpans',
                          'definition': 'Members of the class of '
                                        'benzofurochromene with a '
                                        '6a,11a-dihydro-6H-[1]benzofuro[3,2-c]chromene '
                                        'skeleton and its substituted '
                                        'derivatives. They generally bear '
                                        'structural resemblance to '
                                        'isoflavanoids that possess antibiotic '
                                        'activity and are produced by plant '
                                        'tissues in response to infection. '
                                        'They are the 3,4-dihydroderivatives '
                                        'of coumestans.',
                          'parents': ['CHEBI:38834', 'CHEBI:72544'],
                          'xrefs': [   'MetaCyc:PTEROCARPANS',
                                       'Wikipedia:Pterocarpan'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 34,
                           'log_lines_of_code': 3.5263605246161616,
                           'indent_by_line': [   1,
                                                 1,
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
                                                 2,
                                                 2,
                                                 3,
                                                 2,
                                                 3,
                                                 1,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 3,
                                                 4,
                                                 3,
                                                 4,
                                                 2,
                                                 3],
                           'max_indent': 4,
                           'imports': [   'from rdkit import Chem',
                                          'from rdkit.Chem import AllChem'],
                           'imports_count': 2,
                           'methods_called': [   'MolFromSmiles',
                                                 'MolFromSmarts',
                                                 'HasSubstructMatch',
                                                 'GetSymmSSSR'],
                           'methods_called_count': 4,
                           'smarts_strings': [   '[C@]12Oc3ccccc3[C@@]1(O)COc1ccccc21',
                                                 '[C@]12Oc3c(*)cccc3[C@@]1(O)COc1c(**)cccc21'],
                           'smarts_strings_count': 2,
                           'defs': ['is_pterocarpans(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'True, "Contains the pterocarpan '
                                          'scaffold with required fused rings"',
                                          'False, "Does not have enough fused '
                                          'rings"',
                                          'True, "Contains a substituted '
                                          'pterocarpan scaffold with required '
                                          'fused rings"',
                                          'False, "Does not have enough fused '
                                          'rings"',
                                          'False, "Does not contain the '
                                          'pterocarpan scaffold"'],
                           'returns_count': 6,
                           'complexity': 3.7052721049232327},
    'message': '\n'
               'Attempt failed: F1 score of 0 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: NONE\n'
               'False positives: NONE\n'
               'False negatives: SMILES: '
               'C12=CC3=C(C(=C1C=CC(O2)(C)C)OC)C4C(CO3)C=5C(=CC(=C(C5)OC)O)O4 '
               'NAME: desmodin REASON: MISSED Does not contain the pterocarpan '
               'scaffold\n'
               ' * SMILES: '
               '[H][C@@]12COc3c(CC=C(C)C)c(O)ccc3[C@]1([H])Oc1c(CC=C(C)C)c(O)c(C)cc21 '
               'NAME: lespeflorin G5 REASON: MISSED Does not contain the '
               'pterocarpan scaffold\n'
               ' * SMILES: '
               '[H][C@@]12Oc3cc(O)ccc3[C@]1(O)COc1cc(O)c(CC=C(C)C)cc21 NAME: '
               '(6aS,11aS)-2-dimethylallyl-3,6a,9-trihydroxypterocarpan '
               'REASON: MISSED Does not contain the required hydroxyl oxygen '
               'atoms\n'
               ' * SMILES: O1C2C(C=3C1=CC=4OCOC4C3)COC5=C2C=C6C(OC=C6)=C5 '
               'NAME: Neodulin REASON: MISSED Does not contain the pterocarpan '
               'scaffold\n'
               ' * SMILES: '
               'O1[C@@]2([C@](O)(C3=C1C=C(O)C=C3)COC4=C2C=C5C(OC(=C5)C(O)(C)C)=C4)[H] '
               'NAME: Glyceofuran REASON: MISSED Does not contain the required '
               'hydroxyl oxygen atoms\n'
               ' * SMILES: '
               'O1C2C(O)(C3=C1C=C4C(OC(C=C4)(C)C)=C3)COC5=C2C=CC(O)=C5 NAME: '
               '6alpha-Hydroxyphaseollin REASON: MISSED Does not contain the '
               'required hydroxyl oxygen atoms\n'
               ' * SMILES: '
               'O1[C@@]2([C@](C3=C1C=C(O)C=C3)(COC4=C2C=CC(OC)=C4)[H])[H] '
               'NAME: Isomedicarpin REASON: MISSED Does not contain the '
               'pterocarpan scaffold\n'
               ' * SMILES: O1C2C(C3=C1C=C(OC)C=C3)COC4=C2C=CC(O)=C4O NAME: '
               '3,4-Dihydroxy-9-methoxypterocarpan REASON: MISSED Does not '
               'contain the pterocarpan scaffold\n'
               ' * SMILES: '
               'O1[C@@]2([C@](C3=C1C=C4OC(C=CC4=C3)(C)C)(COC5=C2C(OC)=C(C(O)=C5)CC=C(C)C)[H])[H] '
               'NAME: Kanzonol F REASON: MISSED Does not contain the '
               'pterocarpan scaffold\n'
               ' * SMILES: O1C2C(C=3C1=CC(OC)=C(O)C3)COC4=C2C=CC(O)=C4 NAME: '
               '3,8-Dihydroxy-9-methoxypterocarpan REASON: MISSED Does not '
               'contain the pterocarpan scaffold\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n'
               'IMPORTANT NOTE: I do not have 100% confidence in the benchmark '
               'I am using. There may be occasional and systematic mistakes. '
               'Use your best judgment, and if you think the classifications '
               'your program are consistent with your understanding if the '
               'meaning of the chemical class, then you can ignore outliers, '
               'but explain your reasoning in doing so. I have great '
               'confidence in your broad understanding of chemistry and your '
               'ability to translate this into code.',
    'sample_true_negatives': [   {   'smiles': 'N[C@@H](CC1=CC=C(F)C=C1)C(O)=O',
                                     'name': '4-fluorophenyl-L-alanine',
                                     'reason': 'Does not contain the '
                                               'pterocarpan scaffold'},
                                 {   'smiles': 'CC1=CC(=C(C=C1)C(=O)NN=C2CCC3=CC=CC=C32)C',
                                     'name': 'N-(2,3-dihydroinden-1-ylideneamino)-2,4-dimethylbenzamide',
                                     'reason': 'Does not contain the '
                                               'pterocarpan scaffold'},
                                 {   'smiles': 'O1[C@@]2([C@]34[C@@]([C@@]([C@]5([C@@]3(C(=C6[C@@]5([C@@](O)(CC[C@@]7([C@@]6(OC(=O)[C@H]7C)[H])[H])C)[H])C)[H])[H])([C@@H]2O)[H])([C@@]1(CC[C@@]8([C@@]4(OC(=O)[C@H]8C)[H])[H])C)[H])C',
                                     'name': 'Anabsin',
                                     'reason': 'Does not contain the '
                                               'pterocarpan scaffold'},
                                 {   'smiles': 'S1C2=N[C@@H](C1)C(=O)N[C@@H](C=3SCC(N3)C(=O)N([C@@H](C(=O)N[C@H](C(=O)N[C@@H]([C@H](C(O[C@H](C(N([C@H](C(N4[C@H](C(N([C@@H]2CC5=CC=CC=C5)C)=O)CCC4)=O)C(C)C)C)=O)CC6=CC=CC=C6)=O)C)C)C(C)C)CC7=CC=CC=C7)C)C',
                                     'name': 'Grabetaypeptolide G',
                                     'reason': 'Does not contain the '
                                               'pterocarpan scaffold'},
                                 {   'smiles': 'P(OC1C(O)C(O)C(O)[C@@H](O)C1O)(OC[C@H](OC(=O)CCCCCCC/C=C\\C/C=C\\C/C=C\\CC)COC(=O)CCCCCCCCCCC)(O)=O',
                                     'name': 'PI(12:0/18:3(9Z,12Z,15Z))',
                                     'reason': 'Does not contain the '
                                               'pterocarpan scaffold'},
                                 {   'smiles': 'ClC1=CC=2N(C3=C(CCC2C=C1)C(O[C@@H]4O[C@@H]([C@@H](O)[C@H](O)[C@H]4O)C(O)=O)=CC=C3)CCCN(C)C',
                                     'name': 'Hydroxyclomipramine glucuronide',
                                     'reason': 'Does not contain the '
                                               'pterocarpan scaffold'},
                                 {   'smiles': 'O=C(OC)CCC(=O)C=1OC([C@H](O)C)=CC1',
                                     'name': 'methyl '
                                             '5-[(1R)-1-hydroxyethyl]-gamma-oxofuran-2-butanoate',
                                     'reason': 'Does not contain the '
                                               'pterocarpan scaffold'},
                                 {   'smiles': 'Oc1c(cc(cc1[N+]([O-])=O)[N+]([O-])=O)[N+]([O-])=O',
                                     'name': 'picric acid',
                                     'reason': 'Does not contain the '
                                               'pterocarpan scaffold'},
                                 {   'smiles': 'CCOP(O)(=O)OP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1O)n1ccc(=O)[nH]c1=O',
                                     'name': 'ethyl-UTP',
                                     'reason': 'Does not contain the '
                                               'pterocarpan scaffold'},
                                 {   'smiles': 'O=C1NCC2=C1C=C(OC)C(=C2OC)OCC=C(CCC=C(CC[C@H](O)C(O)(C)C)C)C',
                                     'name': 'Emeriphenolicin C',
                                     'reason': 'Does not contain the '
                                               'pterocarpan scaffold'}],
    'sample_false_negatives': [   {   'smiles': 'C12=CC3=C(C(=C1C=CC(O2)(C)C)OC)C4C(CO3)C=5C(=CC(=C(C5)OC)O)O4',
                                      'name': 'desmodin',
                                      'reason': 'Does not contain the '
                                                'pterocarpan scaffold'},
                                  {   'smiles': '[H][C@@]12COc3c(CC=C(C)C)c(O)ccc3[C@]1([H])Oc1c(CC=C(C)C)c(O)c(C)cc21',
                                      'name': 'lespeflorin G5',
                                      'reason': 'Does not contain the '
                                                'pterocarpan scaffold'},
                                  {   'smiles': 'O1C2C(C=3C1=CC=4OCOC4C3)COC5=C2C=C6C(OC=C6)=C5',
                                      'name': 'Neodulin',
                                      'reason': 'Does not contain the '
                                                'pterocarpan scaffold'},
                                  {   'smiles': 'O1[C@@]2([C@](C3=C1C=C(O)C=C3)(COC4=C2C=CC(OC)=C4)[H])[H]',
                                      'name': 'Isomedicarpin',
                                      'reason': 'Does not contain the '
                                                'pterocarpan scaffold'},
                                  {   'smiles': 'O1C2C(C3=C1C=C(OC)C=C3)COC4=C2C=CC(O)=C4O',
                                      'name': '3,4-Dihydroxy-9-methoxypterocarpan',
                                      'reason': 'Does not contain the '
                                                'pterocarpan scaffold'},
                                  {   'smiles': 'O1[C@@]2([C@](C3=C1C=C4OC(C=CC4=C3)(C)C)(COC5=C2C(OC)=C(C(O)=C5)CC=C(C)C)[H])[H]',
                                      'name': 'Kanzonol F',
                                      'reason': 'Does not contain the '
                                                'pterocarpan scaffold'},
                                  {   'smiles': 'O1C2C(C=3C1=CC(OC)=C(O)C3)COC4=C2C=CC(O)=C4',
                                      'name': '3,8-Dihydroxy-9-methoxypterocarpan',
                                      'reason': 'Does not contain the '
                                                'pterocarpan scaffold'},
                                  {   'smiles': '[H][C@@]12COc3cc(O)ccc3[C@]1([H])Oc1c(CC=C(C)C)c(OC)ccc21',
                                      'name': 'sandwicensin',
                                      'reason': 'Does not contain the '
                                                'pterocarpan scaffold'},
                                  {   'smiles': 'O1[C@@]2([C@](C3=C1C=C(OC)C=C3)(COC4=C2C=CC(O)=C4CC=C(C)C)[H])[H]',
                                      'name': 'Licoagrocarpin',
                                      'reason': 'Does not contain the '
                                                'pterocarpan scaffold'},
                                  {   'smiles': 'O1C2C(C3=C1C=C(OC)C=C3)COC=4C2=CC(OC)=C(OC)C4',
                                      'name': '2,3,9-Trimethoxypterocarpan',
                                      'reason': 'Does not contain the '
                                                'pterocarpan scaffold'}],
    'attempt': 3,
    'reasoning': 'After analyzing the previous program and the outcomes, it '
                 'appears that the issues are:\n'
                 '\n'
                 '1. The SMARTS pattern for the pterocarpan scaffold is too '
                 'specific and restrictive. It only matches the unsubstituted '
                 'pterocarpan scaffold, which means it will miss many '
                 'substituted derivatives.\n'
                 '\n'
                 '2. The program relies too heavily on checking for specific '
                 'substitution patterns, which can lead to missed cases where '
                 'the substitution patterns are different.\n'
                 '\n'
                 '3. The program checks for the presence of ether and hydroxyl '
                 'oxygen atoms, but some of the false negatives indicate that '
                 'this check might be too strict.\n'
                 '\n'
                 '4. The program checks for structural similarity to '
                 'isoflavanoids and coumestans, but these checks may not be '
                 'necessary or reliable for identifying pterocarpans.\n'
                 '\n'
                 '5. The molecular weight and rotatable bond checks might not '
                 'be reliable or necessary for identifying pterocarpans.\n'
                 '\n'
                 'To improve the program, we should focus on identifying the '
                 'core structural features that define a pterocarpan, and use '
                 'more flexible SMARTS patterns to match these features. '
                 'Additionally, we should remove unnecessary checks that may '
                 'introduce false negatives.\n'
                 '\n'
                 "Here's an improved version of the program:",
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 18,
    'num_false_positives': 1,
    'num_true_negatives': 142211,
    'num_false_negatives': 70,
    'num_negatives': None,
    'precision': 0.9473684210526315,
    'recall': 0.20454545454545456,
    'f1': 0.33644859813084116,
    'accuracy': 0.9995010541110331,
    'negative_predictive_value': 0.9995080158278337}