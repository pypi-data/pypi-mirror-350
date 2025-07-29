"""
Classifies: CHEBI:76983 N-sulfonylurea
"""
"""
Classifies: CHEBI:50123 N-sulfonylurea
"""
from rdkit import Chem
from rdkit.Chem import rdMolDescriptors

def is_N_sulfonylurea(smiles: str):
    """
    Determines if a molecule is an N-sulfonylurea based on its SMILES string.
    An N-sulfonylurea is a urea in which one of the hydrogens attached to a nitrogen
    of the urea group is replaced by a sulfonyl group.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is an N-sulfonylurea, False otherwise
        str: Reason for classification
    """
    
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Look for urea group (-N(C=O)N-)
    urea_pattern = Chem.MolFromSmarts("[NH1]C(=O)N")
    if not mol.HasSubstructMatch(urea_pattern):
        return False, "No urea group found"

    # Look for sulfonyl group (-SO2-)
    sulfonylurea_pattern = Chem.MolFromSmarts("S(=O)(=O)")
    if not mol.HasSubstructMatch(sulfonylurea_pattern):
        return False, "No sulfonyl group found"

    # Check if the molecule contains an N-sulfonylurea group
    nsulfonylurea_pattern = Chem.MolFromSmarts("[NH1]C(=O)N~[S](=O)(=O)")
    if mol.HasSubstructMatch(nsulfonylurea_pattern):
        return True, "Contains an N-sulfonylurea group (urea with a sulfonyl group attached to a nitrogen)"

    return False, "No N-sulfonylurea group found"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:76983',
                          'name': 'N-sulfonylurea',
                          'definition': 'A urea in which one of the hydrogens '
                                        'attached to a nitrogen of the urea '
                                        'group is replaced by a sulfonyl '
                                        'group. The N-sulfonylurea moiety is a '
                                        'key group in various herbicides, as '
                                        'well as in a number of antidiabetic '
                                        'drugs used in the management of type '
                                        '2 diabetis mellitus.',
                          'parents': ['CHEBI:35358', 'CHEBI:47857'],
                          'xrefs': [   'PMID:23237384',
                                       'PMID:23594109',
                                       'PMID:23609875',
                                       'Wikipedia:Sulfonylurea'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 27,
                           'log_lines_of_code': 3.295836866004329,
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
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 0,
                                                 1],
                           'max_indent': 2,
                           'imports': [   'from rdkit import Chem',
                                          'from rdkit.Chem import '
                                          'rdMolDescriptors'],
                           'imports_count': 2,
                           'methods_called': [   'HasSubstructMatch',
                                                 'MolFromSmiles',
                                                 'MolFromSmarts'],
                           'methods_called_count': 3,
                           'smarts_strings': [   'S(=O)(=O)',
                                                 '[NH1]C(=O)N',
                                                 '[NH1]C(=O)N~[S](=O)(=O)'],
                           'smarts_strings_count': 3,
                           'defs': ['is_N_sulfonylurea(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "No urea group found"',
                                          'False, "No sulfonyl group found"',
                                          'True, "Contains an N-sulfonylurea '
                                          'group (urea with a sulfonyl group '
                                          'attached to a nitrogen)"',
                                          'False, "No N-sulfonylurea group '
                                          'found"'],
                           'returns_count': 5,
                           'complexity': 2.859167373200866},
    'message': '\n'
               "Error: module 'rdkit.Chem.AllChem' has no attribute "
               "'FindMolPathMatchingSmarts'\n"
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
               'to improve.\n'
               'IMPORTANT NOTE: I do not have 100% confidence in the benchmark '
               'I am using. There may be occasional and systematic mistakes. '
               'Use your best judgment, and if you think the classifications '
               'your program are consistent with your understanding if the '
               'meaning of the chemical class, then you can ignore outliers, '
               'but explain your reasoning in doing so. I have great '
               'confidence in your broad understanding of chemistry and your '
               'ability to translate this into code.',
    'sample_true_negatives': [   {   'smiles': 'O=C(O)[C@@H](N)CCC1C=CC(N)C=C1',
                                     'name': 'Amiclenomycin',
                                     'reason': 'No urea group found'},
                                 {   'smiles': '[H]C(=O)OP(O)(O)=O',
                                     'name': 'formyl dihydrogen phosphate',
                                     'reason': 'No urea group found'},
                                 {   'smiles': 'O1C(C(O)C(O)C(O)C1OC2=C(O)C=CC(=C2)C(O)=O)C(O)=O',
                                     'name': '6-(5-carboxy-2-hydroxyphenoxy)-3,4,5-trihydroxyoxane-2-carboxylic '
                                             'acid',
                                     'reason': 'No urea group found'},
                                 {   'smiles': 'CC(C)CC#CC1=CC=C(C=C1)[C@@H]2[C@@H]3CN(CC(=O)N3[C@@H]2CO)C(=O)C4=CC(=CC=C4)F',
                                     'name': '(6R,7R,8S)-4-[(3-fluorophenyl)-oxomethyl]-8-(hydroxymethyl)-7-[4-(4-methylpent-1-ynyl)phenyl]-1,4-diazabicyclo[4.2.0]octan-2-one',
                                     'reason': 'No urea group found'},
                                 {   'smiles': '[H][C@@]12CCC3=CC(=O)CC[C@]3(C)[C@@]1([H])CC[C@@]1(C)[C@@]2([H])CC[C@]1(O)C(C)O',
                                     'name': '17,20-dihydroxypregn-4-en-3-one',
                                     'reason': 'No urea group found'},
                                 {   'smiles': 'NCCCCC(CN)CCCN',
                                     'name': '4-(aminomethyl)octane-1,8-diamine',
                                     'reason': 'No urea group found'},
                                 {   'smiles': 'O=C1N[C@@H](CC2=CC=CC=C2)[C@H]3[C@]1(O)[C@@H](/C=C/C[C@@H]([C@H](O)C(=O)C)C)[C@H](O)C(C)=C3C',
                                     'name': 'Cytochalasin Z14',
                                     'reason': 'No urea group found'},
                                 {   'smiles': 'C[C@@H]1CCCCO[C@@H]([C@H](CN(C(=O)C2=C(O1)C=CC(=C2)NS(=O)(=O)C)[C@@H](C)CO)C)CN(C)C(=O)C3CCCCC3',
                                     'name': 'N-[[(3R,9S,10S)-12-[(2S)-1-hydroxypropan-2-yl]-16-(methanesulfonamido)-3,10-dimethyl-13-oxo-2,8-dioxa-12-azabicyclo[12.4.0]octadeca-1(14),15,17-trien-9-yl]methyl]-N-methylcyclohexanecarboxamide',
                                     'reason': 'No urea group found'},
                                 {   'smiles': 'O=C(N[C@@H](CC(O)=O)C(O)=O)[C@@H](NC(=O)[C@@H](N)CCC(O)=O)CC(C)C',
                                     'name': 'Glu-Leu-Asp',
                                     'reason': 'No urea group found'},
                                 {   'smiles': 'CC(O)\\C=C/C\\C=C/C\\C=C/C\\C=C/C\\C=C/CCCC([O-])=O',
                                     'name': '19-HEPE(1-)',
                                     'reason': 'No urea group found'}],
    'sample_false_negatives': [   {   'smiles': 'C=1(N(C(N(N1)C(NS(C2=CC=CC=C2OC(F)(F)F)(=O)=O)=O)=O)C)OC',
                                      'name': 'flucarbazone',
                                      'reason': 'No urea group found'},
                                  {   'smiles': 'S(NC(=O)N1C(N(C(=N1)OC)C)=O)(C2=C(SC=C2C(=O)O)C)(=O)=O',
                                      'name': 'thiencarbazone',
                                      'reason': 'No urea group found'},
                                  {   'smiles': 'C1(=NC(C)=NC(OC)=N1)N(C(=O)NS(C=2C(C(O)=O)=CC=CC2)(=O)=O)C',
                                      'name': 'tribenuron',
                                      'reason': 'No N-sulfonylurea group '
                                                'found'}],
    'attempt': 2,
    'reasoning': 'The previous code attempted to identify N-sulfonylureas by '
                 'first looking for the presence of a urea group (-N(C=O)N-) '
                 'and a sulfonyl group (-SO2-) in the molecule. It then '
                 'checked if the sulfonyl group was directly attached to a '
                 'nitrogen of the urea group. This approach works for cases '
                 'where the sulfonyl group is directly attached to the urea '
                 'nitrogen, but it fails to identify N-sulfonylureas where the '
                 'sulfonyl group is not directly attached but rather connected '
                 'through a linker.\n'
                 '\n'
                 'The issue with the previous code arises from the use of '
                 '`AllChem.FindMolPathMatchingSmarts`, which is not a valid '
                 'function in RDKit. This line of code was likely intended to '
                 'find cases where the sulfonyl group is indirectly attached '
                 'to the urea nitrogen, but the incorrect function call '
                 'resulted in an error and prevented the code from running '
                 'successfully.\n'
                 '\n'
                 'To improve the program and correctly identify '
                 'N-sulfonylureas, we can use a more general approach that '
                 'looks for the presence of both the urea and sulfonyl groups '
                 'in the molecule, without explicitly checking for their '
                 'direct or indirect attachment. This can be achieved by using '
                 'the SMARTS pattern matching capabilities of RDKit.\n'
                 '\n'
                 "Here's an improved version of the code:",
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 33,
    'num_false_positives': 41,
    'num_true_negatives': 142223,
    'num_false_negatives': 3,
    'num_negatives': None,
    'precision': 0.44594594594594594,
    'recall': 0.9166666666666666,
    'f1': 0.6,
    'accuracy': 0.9996907940969783,
    'negative_predictive_value': 0.9999789068102879}