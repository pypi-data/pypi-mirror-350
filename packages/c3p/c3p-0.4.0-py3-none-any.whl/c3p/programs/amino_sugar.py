"""
Classifies: CHEBI:28963 amino sugar
"""
from rdkit import Chem

def is_amino_sugar(smiles: str):
    """
    Determines if a molecule is an amino sugar based on its SMILES string.
    An amino sugar is defined as any sugar having one or more alcoholic hydroxy groups
    replaced by substituted or unsubstituted amino groups.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if the molecule is an amino sugar, False otherwise
        str: Reason for classification
    """
    
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if not mol:
        return False, "Invalid SMILES string"

    # Look for sugar-like ring structures typical of pyranoses (6-membered rings)
    sugar_pattern = Chem.MolFromSmarts("C1[C@H]([O])[C@@H]([O])[C@H]([O])[C@H](O)O1")  # Pyranose ring
    if not mol.HasSubstructMatch(sugar_pattern):
        return False, "No typical sugar-like ring structure found"

    # Look for amino groups, possibly replacing -OH groups in these structures
    amino_pattern = Chem.MolFromSmarts("[CX4;R][NX3;H2,H1,H0]")  # Carbon attached to an NHx in a ring
    if not mol.HasSubstructMatch(amino_pattern):
        return False, "No amino group replacing a hydroxy group found"

    return True, "Contains a sugar-like ring structure with one or more hydroxyl groups replaced by amino groups"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:28963',
                          'name': 'amino sugar',
                          'definition': 'Any sugar having one or more '
                                        'alcoholic hydroxy groups replaced by '
                                        'substituted or unsubstituted amino '
                                        'groups.',
                          'parents': ['CHEBI:63299'],
                          'xrefs': [   'KEGG:C05383',
                                       'PMID:18424273',
                                       'PMID:9056391'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 23,
                           'log_lines_of_code': 3.1354942159291497,
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
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 0,
                                                 1],
                           'max_indent': 2,
                           'imports': ['from rdkit import Chem'],
                           'imports_count': 1,
                           'methods_called': [   'MolFromSmarts',
                                                 'HasSubstructMatch',
                                                 'MolFromSmiles'],
                           'methods_called_count': 3,
                           'smarts_strings': [   '[CX4;R][NX3;H2,H1,H0]',
                                                 'C1[C@H]([O])[C@@H]([O])[C@H]([O])[C@H](O)O1'],
                           'smarts_strings_count': 2,
                           'defs': ['is_amino_sugar(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "No typical sugar-like ring '
                                          'structure found"',
                                          'False, "No amino group replacing a '
                                          'hydroxy group found"',
                                          'True, "Contains a sugar-like ring '
                                          'structure with one or more hydroxyl '
                                          'groups replaced by amino groups"'],
                           'returns_count': 4,
                           'complexity': 2.6270988431858298},
    'message': '\n'
               'Error: exceptions must derive from BaseException\n'
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
    'sample_true_negatives': [   {   'smiles': 'CN(C)C1=CC2=C(C=C1)O[C@@H]3[C@H]2C[C@@H](O[C@H]3CO)CC(=O)NCCN4CCCCC4',
                                     'name': '2-[(1S,3R,4aS,9aR)-6-(dimethylamino)-1-(hydroxymethyl)-3,4,4a,9a-tetrahydro-1H-pyrano[3,4-b]benzofuran-3-yl]-N-[2-(1-piperidinyl)ethyl]acetamide',
                                     'reason': 'No typical sugar-like ring '
                                               'structure found'},
                                 {   'smiles': 'C[C@@H](C(=O)O)NC(=O)OC(C)(C)C',
                                     'name': 'N-Boc-L-alanine',
                                     'reason': 'No typical sugar-like ring '
                                               'structure found'},
                                 {   'smiles': 'O=C1C2=C(O)C(=C(O)C=C2C(=O)C=3C1=C(O)C=C(O)C3)/C=C/CCCC',
                                     'name': 'Averythrin',
                                     'reason': 'No typical sugar-like ring '
                                               'structure found'},
                                 {   'smiles': 'O=C(N[C@@H](CC=1NC=NC1)C(O)=O)[C@@H](NC(=O)[C@@H](N)CCC(=O)N)[C@H](CC)C',
                                     'name': 'Gln-Ile-His',
                                     'reason': 'No typical sugar-like ring '
                                               'structure found'},
                                 {   'smiles': 'O1C2C3C(CCC3=C)C(CCC2C(C1=O)=C)=C',
                                     'name': '3,6,9-Trimethylidene-3a,4,5,6a,7,8,9a,9b-octahydroazuleno[4,5-b]furan-2-one',
                                     'reason': 'No typical sugar-like ring '
                                               'structure found'},
                                 {   'smiles': 'C1CN(CC2=CC=CC=C21)CCCNC(=O)CN3C(=O)COC4=CC=CC=C43',
                                     'name': 'N-[3-(3,4-dihydro-1H-isoquinolin-2-yl)propyl]-2-(3-oxo-1,4-benzoxazin-4-yl)acetamide',
                                     'reason': 'No typical sugar-like ring '
                                               'structure found'},
                                 {   'smiles': 'Cc1c(c[nH]c1C(=O)Nc1c(O)c2ccc(O)c(C)c2oc1=O)C(O)=O',
                                     'name': 'Coumeroic acid',
                                     'reason': 'No typical sugar-like ring '
                                               'structure found'},
                                 {   'smiles': 'O=C1OC(=CC(=C1CCCCCC)O)CC(C)C',
                                     'name': 'Photopyrone A',
                                     'reason': 'No typical sugar-like ring '
                                               'structure found'},
                                 {   'smiles': '[C@H]1(O)[C@@H](O)O[C@H](CS(O)(=O)=O)[C@H]([C@@H]1O)O',
                                     'name': '6-sulfo-alpha-D-quinovose',
                                     'reason': 'No amino group replacing a '
                                               'hydroxy group found'},
                                 {   'smiles': 'SC[C@H](NC(=O)CNC(=O)[C@@H](N)CC(O)=O)C(O)=O',
                                     'name': 'Asp-Gly-Cys',
                                     'reason': 'No typical sugar-like ring '
                                               'structure found'}],
    'sample_false_negatives': [   {   'smiles': 'OC[C@H]1O[C@@H](O)[C@H](NC(=O)CCCCCNc2c(cc(cc2[N+]([O-])=O)[N+]([O-])=O)C(O)=O)[C@@H](O)[C@@H]1O',
                                      'name': 'N-[6-(DNCP-amino)hexanoyl]-beta-D-glucosamine',
                                      'reason': 'No typical sugar-like ring '
                                                'structure found'},
                                  {   'smiles': '[H]C([H])(C=O)[C@@]([H])(N)[C@]([H])(O)[C@]([H])(C)O',
                                      'name': 'acosamine',
                                      'reason': 'No typical sugar-like ring '
                                                'structure found'},
                                  {   'smiles': 'O1C2C(O)(C(O)C13OCC(C(OC(=O)C4=CC=C(O)C=C4)C3)C)C(O)CC(C2)C(OC5C(OC6OC(C(O)C(O)C6NC(=O)C)CO)C(O)C(O)C(O)C5)=O',
                                      'name': 'Phyllanthusol A',
                                      'reason': 'No typical sugar-like ring '
                                                'structure found'},
                                  {   'smiles': '[H][C@]1(O[C@](O)(C[C@H](O)[C@H]1NC(C)=O)C(O)=O)[C@H](O)[C@H](O)CO',
                                      'name': 'N-acetyl-alpha-neuraminic acid',
                                      'reason': 'No typical sugar-like ring '
                                                'structure found'},
                                  {   'smiles': 'O1[C@@H]([C@H](O)[C@@H](O)[C@@H](NC(=O)C)C1O)CO',
                                      'name': 'N-Acetyl-D-Gulosamine',
                                      'reason': 'No typical sugar-like ring '
                                                'structure found'},
                                  {   'smiles': 'CN[C@@H]1[C@@H](O)[C@H](O[C@H]2O[C@@H](CC[C@H]2N)[C@H](C)N)[C@@H](N)[C@H](O)[C@@H]1OC',
                                      'name': 'Fortimicin KR',
                                      'reason': 'No typical sugar-like ring '
                                                'structure found'},
                                  {   'smiles': 'N[C@H]1C(O)O[C@H](COP(O)(O)=O)[C@@H](O)[C@@H]1O',
                                      'name': '2-amino-2-deoxy-D-glucopyranose '
                                              '6-phosphate',
                                      'reason': 'No typical sugar-like ring '
                                                'structure found'},
                                  {   'smiles': 'CC(=O)N[C@@H]1[C@@H](O)[C@H](O)[C@@H](CO)O[C@@H]1OP(O)(=O)OCCCN',
                                      'name': '3-aminopropyl '
                                              'N-acetyl-alpha-D-glucosamine-1-phosphate',
                                      'reason': 'No typical sugar-like ring '
                                                'structure found'},
                                  {   'smiles': 'N[C@H]1CO[C@H](O)[C@H](O)[C@H]1O',
                                      'name': '4-amino-4-deoxy-beta-L-arabinopyranose',
                                      'reason': 'No typical sugar-like ring '
                                                'structure found'},
                                  {   'smiles': 'CC(=O)N[C@@H]1[C@H](O)O[C@H](CO)[C@@H](O)[C@@H]1O',
                                      'name': 'N-acetyl-beta-D-mannosamine',
                                      'reason': 'No typical sugar-like ring '
                                                'structure found'}],
    'attempt': 1,
    'reasoning': 'To classify molecules as amino sugars based on their SMILES '
                 'strings, we need to accurately identify the structural '
                 'features indicative of this chemical class. An amino sugar '
                 'is characterized by having one or more hydroxyl (-OH) groups '
                 'replaced by amino (-NH2, -NHR, -NR2) groups.\n'
                 '\n'
                 'From the initial attempt, the program failed to properly '
                 'identify amino sugars, likely due to an inadequate or overly '
                 "simplified pattern definition. Here's a step-by-step plan to "
                 'improve the detection of amino sugars:\n'
                 '\n'
                 '1. **Validate Input SMILES**: Ensure the input SMILES can be '
                 'correctly parsed into a molecular object.\n'
                 '2. **Identify Sugar Backbone**: Look for typical sugar-like '
                 'structures, which can be complex. Consider cyclic structures '
                 'like pyranoses or furanoses, common in simple sugars.\n'
                 '3. **Identify Amino Substituents**: Specifically check for '
                 'nitrogen atoms attached in positions where hydroxyl groups '
                 'typically exist in sugars.\n'
                 '4. **Substructure Search**: Use SMARTS patterns to identify '
                 'relevant substructures associated with sugars and amino '
                 'substitutions, ensuring these patterns reflect the '
                 'complexity and variability found in amino sugars.\n'
                 '\n'
                 'Using SMARTS queries, we should look for:\n'
                 '- A sugar-like cyclic backbone, commonly depicted as a '
                 'pyranose ring: `C[C@H](O)[C@@H](O)[C@H](O)[C@H](O)CO`\n'
                 '- An amino group replacing a hydroxyl group, particularly '
                 'checking for nitrogen attached to a sugar ring carbon.\n'
                 '\n'
                 'Implement this improved approach in the following code:',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 2672,
    'num_false_positives': 5453,
    'num_true_negatives': 133842,
    'num_false_negatives': 333,
    'num_negatives': None,
    'precision': 0.3288615384615385,
    'recall': 0.8891846921797005,
    'f1': 0.48014375561545375,
    'accuracy': 0.9593394237526353,
    'negative_predictive_value': 0.9975181665735048}