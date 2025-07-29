"""
Classifies: CHEBI:87658 decanoate ester
"""
"""
Classifies: Decanoate ester
A decanoate ester is defined as a fatty acid ester resulting from the formal condensation 
of the carboxy group of decanoic (capric) acid with the hydroxy group of an alcohol or phenol.
Decanoic acid is CH3-(CH2)8-C(=O)OH and thus the ester moiety will contain the acyl fragment:
CH3-(CH2)8-C(=O)O (or its deprotonated form).
"""
from rdkit import Chem

def is_decanoate_ester(smiles: str):
    """
    Determines if a molecule is a decanoate ester based on its SMILES string.
    The method searches for a decanoate acyl fragment:
      CH3-(CH2)8-C(=O)O  (or with a negatively charged oxygen instead of O)
    
    Args:
        smiles (str): SMILES string of the molecule.
        
    Returns:
        bool: True if the decanoate ester substructure is found, False otherwise.
        str: Explanation or reason for the classification.
    """
    # Parse the SMILES string
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Define SMARTS patterns for decanoate ester acyl fragment.
    # The first pattern matches CH3-CH2-CH2-CH2-CH2-CH2-CH2-CH2-CH2-C(=O)O
    # (note: 1 CH3 followed by eight CH2 groups gives 9 carbons; the carbonyl carbon is the 10th).
    decanoate_pattern1 = Chem.MolFromSmarts("[CH3][CH2][CH2][CH2][CH2][CH2][CH2][CH2][CH2]C(=O)O")
    # The second pattern allows for the ester oxygen being deprotonated: [O-]
    decanoate_pattern2 = Chem.MolFromSmarts("[CH3][CH2][CH2][CH2][CH2][CH2][CH2][CH2][CH2]C(=O)[O-]")

    # Check if either pattern is present in the molecule
    if mol.HasSubstructMatch(decanoate_pattern1) or mol.HasSubstructMatch(decanoate_pattern2):
        return True, "Contains decanoate ester moiety (decanoic acyl group detected)"
    else:
        return False, "Decanoate ester fragment not found in the molecule"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:87658',
                          'name': 'decanoate ester',
                          'definition': 'A fatty acid ester resulting from the '
                                        'formal condensation of the carboxy '
                                        'group of decanoic acid (capric acid) '
                                        'with the hydroxy group of an alcohol '
                                        'or phenol.',
                          'parents': ['CHEBI:35748'],
                          'xrefs': ['PMID:23383323'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 25,
                           'log_lines_of_code': 3.2188758248682006,
                           'indent_by_line': [   1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
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
                                                 1,
                                                 1,
                                                 1,
                                                 0,
                                                 1,
                                                 1,
                                                 2,
                                                 1,
                                                 2],
                           'max_indent': 2,
                           'imports': ['from rdkit import Chem'],
                           'imports_count': 1,
                           'methods_called': [   'HasSubstructMatch',
                                                 'MolFromSmarts',
                                                 'MolFromSmiles'],
                           'methods_called_count': 3,
                           'smarts_strings': [   '[CH3][CH2][CH2][CH2][CH2][CH2][CH2][CH2][CH2]C(=O)[O-]',
                                                 '[CH3][CH2][CH2][CH2][CH2][CH2][CH2][CH2][CH2]C(=O)O'],
                           'smarts_strings_count': 2,
                           'defs': ['is_decanoate_ester(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'True, "Contains decanoate ester '
                                          'moiety (decanoic acyl group '
                                          'detected)"',
                                          'False, "Decanoate ester fragment '
                                          'not found in the molecule"'],
                           'returns_count': 3,
                           'complexity': 2.44377516497364},
    'message': None,
    'sample_true_negatives': [   {   'smiles': 'O=C(N1[C@H](CCC1)C(O)=O)[C@@H](NC(=O)[C@@H](N)CC(O)=O)CCC(=O)N',
                                     'name': 'Asp-Gln-Pro',
                                     'reason': 'Decanoate ester fragment not '
                                               'found in the molecule'},
                                 {   'smiles': 'O1C=2C(C(O)=C(CC3=C(O)C=4C(OC3=O)=CC=CC4C)C1=O)=C(C=CC2)C',
                                     'name': 'Gerberinol',
                                     'reason': 'Decanoate ester fragment not '
                                               'found in the molecule'},
                                 {   'smiles': 'O=C(O)/C(=C/[C@H]1C=C(CC[C@@H]1C(C)C)CO)/COC(=O)C',
                                     'name': '3-acetylgliocladic acid',
                                     'reason': 'Decanoate ester fragment not '
                                               'found in the molecule'},
                                 {   'smiles': 'O=C(CCCCCCCCC)C=1C=CC(=NC1)CCCCCCCCC',
                                     'name': '1-(6-Nonylpyridin-3-yl)decan-1-one',
                                     'reason': 'Decanoate ester fragment not '
                                               'found in the molecule'},
                                 {   'smiles': 'CCC(=O)O[C@H]1[C@H](C)O[C@H](C[C@@]1(C)O)O[C@@H]1[C@@H](C)O[C@@H](O[C@H]2[C@@H](CC=O)C[C@@H](C)[C@@H](O)\\C=C\\C=C\\C[C@@H](C)OC(=O)C[C@@H](O)[C@@H]2OC)[C@H](O)[C@H]1N(C)C',
                                     'name': 'Leucomycin A7',
                                     'reason': 'Decanoate ester fragment not '
                                               'found in the molecule'},
                                 {   'smiles': 'C[C@H]1O[C@H](C[C@@H](O)[C@@H]1O)c1ccc2C(=O)C3=C([C@H](O)C[C@]4(O)C[C@@](C)(O)CC(=O)[C@]34O)C(=O)c2c1O',
                                     'name': 'Urdamycinone F',
                                     'reason': 'Decanoate ester fragment not '
                                               'found in the molecule'},
                                 {   'smiles': 'CC(C)=CCC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\COP([O-])(=O)OP([O-])([O-])=O',
                                     'name': 'all-trans-dodecaprenyl '
                                             'diphosphate(3-)',
                                     'reason': 'Decanoate ester fragment not '
                                               'found in the molecule'},
                                 {   'smiles': '[O-][N+](=O)N1CN(CN(CN(C1)[N+]([O-])=O)[N+]([O-])=O)[N+]([O-])=O',
                                     'name': 'octogen',
                                     'reason': 'Decanoate ester fragment not '
                                               'found in the molecule'},
                                 {   'smiles': 'CC(=O)NCCC[NH2+]CCCC[NH2+]CCCNC(C)=O',
                                     'name': 'N(1),N(12)-diacetylsperminium(2+)',
                                     'reason': 'Decanoate ester fragment not '
                                               'found in the molecule'},
                                 {   'smiles': 'C[C@@H]([C@H]1CC[C@H]2[C@H](CCc3cc(O)ccc3C)C(=O)CC[C@]12C)C(O)=O',
                                     'name': '3-hydroxy-9-oxo-9,10-seco-23,24-bisnorchola-1,3,5(10)-trien-22-oic '
                                             'acid',
                                     'reason': 'Decanoate ester fragment not '
                                               'found in the molecule'}],
    'sample_false_negatives': [],
    'attempt': 0,
    'reasoning': 'Below is our reasoning before the code:\n'
                 '\n'
                 'To define a decanoate ester we focus on detecting the ester '
                 'substructure that comes specifically from decanoic (capric) '
                 'acid. Decanoic acid has a linear 10‐carbon chain '
                 '(CH3–(CH2)8–C(=O)OH) so the acyl fragment in an ester will '
                 'be “CH3–(CH2)8–C(=O)O” (or the deprotonated form '
                 '“…C(=O)[O-]”). Our approach is to parse the input SMILES '
                 'using RDKit and then search for this acyl chain substructure '
                 'by using a SMARTS pattern that encodes exactly nine '
                 'contiguous carbon atoms (with the first being a CH3 and the '
                 'next eight as CH2 groups) followed by a carbonyl and an '
                 'ester oxygen. In the code we build two SMARTS patterns (one '
                 'for an –OH and one for an –O- form) and if either of these '
                 'substructure matches is found we classify the molecule as a '
                 'decanoate ester.\n'
                 '\n'
                 'Below is the complete Python code.',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 32,
    'num_false_positives': 149,
    'num_true_negatives': 142119,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.17679558011049723,
    'recall': 1.0,
    'f1': 0.3004694835680751,
    'accuracy': 0.9989529163738581,
    'negative_predictive_value': 1.0}