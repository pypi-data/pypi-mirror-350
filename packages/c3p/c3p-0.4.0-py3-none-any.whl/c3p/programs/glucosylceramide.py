"""
Classifies: CHEBI:36500 glucosylceramide
"""
from rdkit import Chem

def is_glucosylceramide(smiles: str):
    """
    Determines if a molecule is a glucosylceramide based on its SMILES string.
    A glucosylceramide contains a glucose moiety, a sphingosine backbone, and a long fatty acid chain.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a glucosylceramide, False otherwise
        str: Reason for classification
    """
    
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for β-D-glucose moiety using revised pattern
    glucose_pattern = Chem.MolFromSmarts("C(O[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O)")
    if not mol.HasSubstructMatch(glucose_pattern):
        return False, "No β-D-glucose moiety found"

    # Check for amide linkage attached to a long chain (not precise but helps identify linkage point)
    amide_pattern = Chem.MolFromSmarts("NC(=O)CCCCCCCCCCCCCCCCCCC")
    if not mol.HasSubstructMatch(amide_pattern):
        return False, "No amide linkage to a long fatty acid chain found"

    # Check for sphingosine backbone pattern (N-alkylated amine with long chain and specific OH groups)
    sphingosine_patterns = [
        Chem.MolFromSmarts("[NX3]C[C@H](O)CO"), # Basic pattern to identify the common N-linkage
    ]
    if not any(mol.HasSubstructMatch(pat) for pat in sphingosine_patterns):
        return False, "No sphingosine backbone found"

    return True, "Contains glucose moiety linked to a sphingosine-like backbone with a fatty acid chain"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:36500',
                          'name': 'glucosylceramide',
                          'definition': 'Any of the cerebrosides in which the '
                                        'monosaccharide head group is glucose.',
                          'parents': ['CHEBI:23079', 'CHEBI:62941'],
                          'xrefs': ['PMID:16758576'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 28,
                           'log_lines_of_code': 3.332204510175204,
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
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 0,
                                                 1,
                                                 1,
                                                 2,
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
                           'smarts_strings': [   'NC(=O)CCCCCCCCCCCCCCCCCCC',
                                                 'C(O[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O)',
                                                 '[NX3]C[C@H](O)CO'],
                           'smarts_strings_count': 3,
                           'defs': ['is_glucosylceramide(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "No β-D-glucose moiety '
                                          'found"',
                                          'False, "No amide linkage to a long '
                                          'fatty acid chain found"',
                                          'False, "No sphingosine backbone '
                                          'found"',
                                          'True, "Contains glucose moiety '
                                          'linked to a sphingosine-like '
                                          'backbone with a fatty acid chain"'],
                           'returns_count': 5,
                           'complexity': 2.8664409020350408},
    'message': '\n'
               'Attempt failed: F1 score of 0 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: NONE\n'
               'False positives: NONE\n'
               'False negatives: SMILES: '
               'C(CCCCCC(CC)C)CC\\C=C\\[C@@H](O)[C@@H](NC(CCCCCCCCCCCCCCCCCCCCCC)=O)CO[C@@H]1O[C@@H]([C@@H](O)[C@@H]([C@H]1O)O)CO '
               'NAME: '
               "beta-D-glucosyl-(1<->1')-N-tricosanoyl-14-methylhexadecasphingosine "
               'REASON: MISSED No β-D-glucose moiety found\n'
               ' * SMILES: '
               'C(CCCCCCC(C)C)CCCC[C@@H](O)[C@@H](NC(CCCCCCCCCCCCCCCCCCCCCC)=O)CO[C@@H]1O[C@@H]([C@@H](O)[C@@H]([C@H]1O)O)CO '
               'NAME: '
               "beta-D-glucosyl-(1<->1')-N-tricosanoyl-15-methylhexadecasphinganine "
               'REASON: MISSED No β-D-glucose moiety found\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCCCC(=O)N[C@@H](CO[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O)[C@H](O)\\C=C\\CCCCCCCCCC(C)C '
               'NAME: '
               'N-icosanoyl-1-O-beta-D-glucosyl-15-methylhexadecasphing-4-enine '
               'REASON: MISSED No β-D-glucose moiety found\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCCCCCCCCC(O)C(=O)N[C@@H](CO[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O)[C@H](O)\\C=C\\CCCCCCCCCC(C)C '
               'NAME: '
               'N-(2-hydroxyhexacosanoyl)-1-O-beta-D-glucosyl-15-methylhexadecasphing-4-enine '
               'REASON: MISSED No β-D-glucose moiety found\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCCCCC(O)C(=O)N[C@@H](CO[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O)[C@H](O)\\C=C\\CCCCCCCCCC(C)C '
               'NAME: '
               'N-(2-hydroxydocosanoyl)-1-O-beta-D-glucosyl-15-methylhexadecasphing-4-enine '
               'REASON: MISSED No β-D-glucose moiety found\n'
               ' * SMILES: '
               'CCCCCCCCCCCCC\\C=C\\[C@@H](O)[C@H](CO[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O)NC(=O)CCCCCCCCCCCCCCC\\C=C/CCCCCCCC '
               'NAME: beta-D-glucosyl-N-[(17Z)-hexacosenoyl]sphingosine '
               'REASON: MISSED No β-D-glucose moiety found\n'
               ' * SMILES: '
               '[C@H]1([C@H](O[C@@H](OC[C@@H]([C@@H](CCCCCCCCCCCCCCC)O)OC(CCCCCCCCCCCCC/C=C\\CCCCCCCC)=O)[C@@H]([C@H]1O)O)CO)O '
               'NAME: '
               "beta-D-glucosyl-(1<->1')-N-[(15Z)-tetracosenoyl]sphinganine "
               'REASON: MISSED No β-D-glucose moiety found\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCC(=O)N[C@@H](CO[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O)[C@H](O)[C@H](O)CCCCCCCCCCC(C)C '
               'NAME: '
               'N-octadecanoyl-1-O-beta-D-glucosyl-4-hydroxy-15-methylhexadecasphinganine '
               'REASON: MISSED No β-D-glucose moiety found\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCCCCCCCCC(=O)N[C@@H](CO[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O)[C@H](O)\\C=C\\CCCCCCCCCC(C)C '
               'NAME: '
               'N-pentacosanoyl-1-O-beta-D-glucosyl-15-methylhexadecasphing-4-enine '
               'REASON: MISSED No β-D-glucose moiety found\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCCCCCCCCCCC(O)C(=O)N[C@@H](CO[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O)[C@H](O)[C@H](O)CCCCCCCCCCC(C)C '
               'NAME: '
               'N-(2-hydroxyoctacosanoyl)-1-O-beta-D-glucosyl-4-hydroxy-15-methylhexadecasphinganine '
               'REASON: MISSED No β-D-glucose moiety found\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'O1C(COC(=O)C)=CC=C1',
                                     'name': 'Furfuryl acetate',
                                     'reason': 'No β-D-glucose moiety found'},
                                 {   'smiles': 'O=C1N[C@@H](C(=O)N[C@H](C(=O)N[C@@H](C(=O)O)CC(=O)N[C@@H](CCCN=C(N)N)C(N[C@H]([C@@H](C(N[C@H](CCC(NC1=C)=O)C(=O)O)=O)C)/C=C/C(=C/[C@@H]([C@@H](OC)CC2=CC=CC=C2)C)/C)=O)CC(C)C)CO',
                                     'name': '[D-Ser1,D-Asp3,Dha7]MC-LR',
                                     'reason': 'No β-D-glucose moiety found'},
                                 {   'smiles': 'COC1=CC=C(C=C1)NC(=O)N[C@H]2CC[C@@H](O[C@H]2CO)CC(=O)NCC3=CC=CC=N3',
                                     'name': '2-[(2R,5S,6R)-6-(hydroxymethyl)-5-[[(4-methoxyanilino)-oxomethyl]amino]-2-oxanyl]-N-(2-pyridinylmethyl)acetamide',
                                     'reason': 'No β-D-glucose moiety found'},
                                 {   'smiles': 'O=[N+]([O-])C1=CC=C(/C=C(/C=C(/C=C/C=2OC(OC)=C(C)C(C2C)=O)\\C)\\C)C=C1',
                                     'name': 'Dehydrodeoxyaureothin',
                                     'reason': 'No β-D-glucose moiety found'},
                                 {   'smiles': 'C1CNCCNCCCN(CCNC1)CC2=CC=C(C=C2)CN3CCCNCCNCCCNCC3',
                                     'name': 'plerixafor',
                                     'reason': 'No β-D-glucose moiety found'},
                                 {   'smiles': 'O=C(C[C@@H]1O[C@H](CC[C@H]1O)C)C',
                                     'name': 'Decarestrictine L',
                                     'reason': 'No β-D-glucose moiety found'},
                                 {   'smiles': 'O=C1OC(=CC2=C1C[C@@H]3[C@@]4([C@H](C(C)(C)O[C@H]4CC(=O)OC)[C@@H](C[C@]3(O2)C)OC(=O)C)C)C',
                                     'name': 'Asperversin A',
                                     'reason': 'No β-D-glucose moiety found'},
                                 {   'smiles': 'O=C1OC(CC=2C1=C(O)C3=C(O)C(C4=C(O)C5=C(O)C=6C(=O)OC(CC(=O)C)CC6C=C5C=C4OC)=C(OC)C=C3C2)CC(=O)C',
                                     'name': 'SC-30532',
                                     'reason': 'No β-D-glucose moiety found'},
                                 {   'smiles': 'C([C@H](NC(CC[C@H](N)C(=O)O)=O)C(O)=O)S[C@H](\\C=C\\C=C\\C=C/C/C=C\\CCCCC)[C@@H](O)CCCC(=O)O',
                                     'name': 'leukotriene F4',
                                     'reason': 'No β-D-glucose moiety found'},
                                 {   'smiles': 'C1(=C(C=C2C(=C1)[C@@]34[C@@]([NH+](C2)CC3)(CC(CC4)=O)[H])O)OC',
                                     'name': '(4aS,10bR)-oxomaritidine(1+)',
                                     'reason': 'No β-D-glucose moiety found'}],
    'sample_false_negatives': [   {   'smiles': 'C(CCCCCC(CC)C)CC\\C=C\\[C@@H](O)[C@@H](NC(CCCCCCCCCCCCCCCCCCCCCC)=O)CO[C@@H]1O[C@@H]([C@@H](O)[C@@H]([C@H]1O)O)CO',
                                      'name': "beta-D-glucosyl-(1<->1')-N-tricosanoyl-14-methylhexadecasphingosine",
                                      'reason': 'No sphingosine backbone '
                                                'found'},
                                  {   'smiles': 'C(CCCCCCC(C)C)CCCC[C@@H](O)[C@@H](NC(CCCCCCCCCCCCCCCCCCCCCC)=O)CO[C@@H]1O[C@@H]([C@@H](O)[C@@H]([C@H]1O)O)CO',
                                      'name': "beta-D-glucosyl-(1<->1')-N-tricosanoyl-15-methylhexadecasphinganine",
                                      'reason': 'No sphingosine backbone '
                                                'found'},
                                  {   'smiles': 'CCCCCCCCCCCCCCCCCCCC(=O)N[C@@H](CO[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O)[C@H](O)\\C=C\\CCCCCCCCCC(C)C',
                                      'name': 'N-icosanoyl-1-O-beta-D-glucosyl-15-methylhexadecasphing-4-enine',
                                      'reason': 'No sphingosine backbone '
                                                'found'},
                                  {   'smiles': 'CCCCCCCCCCCCCCCCCCCCCCCCC(O)C(=O)N[C@@H](CO[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O)[C@H](O)\\C=C\\CCCCCCCCCC(C)C',
                                      'name': 'N-(2-hydroxyhexacosanoyl)-1-O-beta-D-glucosyl-15-methylhexadecasphing-4-enine',
                                      'reason': 'No sphingosine backbone '
                                                'found'},
                                  {   'smiles': 'CCCCCCCCCCCCCCCCCCCCC(O)C(=O)N[C@@H](CO[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O)[C@H](O)\\C=C\\CCCCCCCCCC(C)C',
                                      'name': 'N-(2-hydroxydocosanoyl)-1-O-beta-D-glucosyl-15-methylhexadecasphing-4-enine',
                                      'reason': 'No sphingosine backbone '
                                                'found'},
                                  {   'smiles': 'CCCCCCCCCCCCC\\C=C\\[C@@H](O)[C@H](CO[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O)NC(=O)CCCCCCCCCCCCCCC\\C=C/CCCCCCCC',
                                      'name': 'beta-D-glucosyl-N-[(17Z)-hexacosenoyl]sphingosine',
                                      'reason': 'No amide linkage to a long '
                                                'fatty acid chain found'},
                                  {   'smiles': '[C@H]1([C@H](O[C@@H](OC[C@@H]([C@@H](CCCCCCCCCCCCCCC)O)OC(CCCCCCCCCCCCC/C=C\\CCCCCCCC)=O)[C@@H]([C@H]1O)O)CO)O',
                                      'name': "beta-D-glucosyl-(1<->1')-N-[(15Z)-tetracosenoyl]sphinganine",
                                      'reason': 'No amide linkage to a long '
                                                'fatty acid chain found'},
                                  {   'smiles': 'CCCCCCCCCCCCCCCCCC(=O)N[C@@H](CO[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O)[C@H](O)[C@H](O)CCCCCCCCCCC(C)C',
                                      'name': 'N-octadecanoyl-1-O-beta-D-glucosyl-4-hydroxy-15-methylhexadecasphinganine',
                                      'reason': 'No amide linkage to a long '
                                                'fatty acid chain found'},
                                  {   'smiles': 'CCCCCCCCCCCCCCCCCCCCCCCCC(=O)N[C@@H](CO[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O)[C@H](O)\\C=C\\CCCCCCCCCC(C)C',
                                      'name': 'N-pentacosanoyl-1-O-beta-D-glucosyl-15-methylhexadecasphing-4-enine',
                                      'reason': 'No sphingosine backbone '
                                                'found'},
                                  {   'smiles': 'CCCCCCCCCCCCC\\C=C\\[C@@H](O)[C@H](COC1O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O)NC(=O)CCCCC',
                                      'name': 'D-glucosyl-N-hexanoylsphingosine',
                                      'reason': 'No amide linkage to a long '
                                                'fatty acid chain found'}],
    'attempt': 3,
    'reasoning': 'Upon reviewing the previous implementation and the '
                 'associated test outcomes, several key observations and '
                 'potential sources for improvement have been identified:\n'
                 '\n'
                 '1. **β-D-Glucose Moiety Detection**: The primary issue stems '
                 'from the β-D-glucose pattern not being correctly identified '
                 'for the given SMILES strings. The SMARTS pattern used might '
                 'not adequately capture the specific stereochemistry or '
                 'connectivity observed in all examples of glucosylceramides.\n'
                 '\n'
                 '2. **Amide Linkage and Sphingosine Backbone**: The previous '
                 'code attempts to identify a sphingosine backbone, but this '
                 'needs to be more flexible to accommodate variations. '
                 'Glucosylceramides often have structural variations, '
                 'especially in the hydrocarbon chains and possible double '
                 'bonds.\n'
                 '\n'
                 '3. **Fatty Acid Chain Length Requirement**: The code checks '
                 'for a generic long chain without explicitly linking it to '
                 'the amide properly. This checking might be too generic or '
                 'overlook connectedness with the identified amide nitrogen.\n'
                 '\n'
                 '**Improvement Strategy**:\n'
                 '\n'
                 '- **Refine the Glucose Moiety Pattern**: Use a β-D-glucose '
                 'pattern that more accurately reflects the expected '
                 'connectivity in glucosylceramides.\n'
                 '- **A More Flexible Backbone Identification**: Refine or '
                 'widen pattern matching for the sphingosine backbone to '
                 'account for variations.\n'
                 '- **Explicit Long Chain Identification**: Ensure that the '
                 'long chain is appropriately linked via the amide group to '
                 'the sphingosine.\n'
                 '\n'
                 'Here is the revised program:',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 14,
    'num_false_positives': 102,
    'num_true_negatives': 142118,
    'num_false_negatives': 66,
    'num_negatives': None,
    'precision': 0.1206896551724138,
    'recall': 0.175,
    'f1': 0.14285714285714285,
    'accuracy': 0.9988193956430077,
    'negative_predictive_value': 0.9995358127496765}