"""
Classifies: CHEBI:27933 beta-lactam antibiotic
"""
"""
Classifies: CHEBI:27731 beta-lactam antibiotic
"""
from rdkit import Chem

def is_beta_lactam_antibiotic(smiles: str):
    """
    Determines if a molecule is a beta-lactam antibiotic based on its SMILES string.
    A beta-lactam antibiotic contains a beta-lactam ring (a four-membered cyclic amide).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a beta-lactam antibiotic, False otherwise
        str: Reason for classification
    """
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Define SMARTS pattern for the beta-lactam ring (four-membered cyclic amide)
    beta_lactam_pattern = Chem.MolFromSmarts("C1C(=O)N[C]1")

    # Check for substructure match
    if mol.HasSubstructMatch(beta_lactam_pattern):
        return True, "Contains a beta-lactam ring"
    else:
        return False, "Does not contain a beta-lactam ring"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:27933',
                          'name': 'beta-lactam antibiotic',
                          'definition': 'An organonitrogen heterocyclic '
                                        'antibiotic that contains a '
                                        'beta-lactam ring.',
                          'parents': ['CHEBI:25558', 'CHEBI:35627'],
                          'xrefs': [   'KEGG:C03438',
                                       'PMID:19254642',
                                       'PMID:22594007',
                                       'Wikipedia:Beta-lactam_antibiotic'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 20,
                           'log_lines_of_code': 2.995732273553991,
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
                                                 0,
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
                           'methods_called': [   'MolFromSmiles',
                                                 'MolFromSmarts',
                                                 'HasSubstructMatch'],
                           'methods_called_count': 3,
                           'smarts_strings': ['C1C(=O)N[C]1'],
                           'smarts_strings_count': 1,
                           'defs': ['is_beta_lactam_antibiotic(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'True, "Contains a beta-lactam ring"',
                                          'False, "Does not contain a '
                                          'beta-lactam ring"'],
                           'returns_count': 3,
                           'complexity': 2.399146454710798},
    'message': None,
    'sample_true_negatives': [   {   'smiles': 'CCN1N=C(N=N1)C2=CC=CC=C2NC(=O)C3=CC=C(C=C3)N4C=NN=N4',
                                     'name': 'N-[2-(2-ethyl-5-tetrazolyl)phenyl]-4-(1-tetrazolyl)benzamide',
                                     'reason': 'Does not contain a beta-lactam '
                                               'ring'},
                                 {   'smiles': 'CCS(=O)(=O)N1CC2(C1)[C@@H]([C@@H](N2C(=O)C3CCCC3)CO)C4=CC=C(C=C4)C=CC',
                                     'name': 'LSM-38092',
                                     'reason': 'Does not contain a beta-lactam '
                                               'ring'},
                                 {   'smiles': 'O=C/1N/C(/C(=O)N\\C1=C\\C2=CC=CC=C2)=C\\C=3N=CNC3C(C=C)(C)C',
                                     'name': 'DeltaPLH',
                                     'reason': 'Does not contain a beta-lactam '
                                               'ring'},
                                 {   'smiles': 'C1CCN(CC1)C(=O)C[C@H]2C[C@@H]3[C@H]([C@@H](O2)CO)OC4=C3C=C(C=C4)NC(=O)CC5CC5',
                                     'name': 'N-[(1S,3R,4aS,9aR)-1-(hydroxymethyl)-3-[2-oxo-2-(1-piperidinyl)ethyl]-3,4,4a,9a-tetrahydro-1H-pyrano[3,4-b]benzofuran-6-yl]-2-cyclopropylacetamide',
                                     'reason': 'Does not contain a beta-lactam '
                                               'ring'},
                                 {   'smiles': 'C[C@H]1C[C@@]2(OC(=O)c3ccccc3)[C@H]([C@H]1OC(C)=O)[C@@H](O)\\C(C)=C/C[C@H]1[C@@H](\\C=C(C)\\C2=O)C1(C)C',
                                     'name': '(-)-(6Z,12E,2S,3S,4R,5R,9S,11S,15R)-3-acetoxy-15-benzoyloxylathyra-6,12-dien-5-ol-14-one',
                                     'reason': 'Does not contain a beta-lactam '
                                               'ring'},
                                 {   'smiles': 'O=C1C(O)=CC=2O[C@]3([C@H](O)C[C@@H]4[C@](OC=5C=C(O)C(C=C(C5C4)C)=O)(CC=CC(C[C@H]3CC2C(=C1)C)(C)C)C)C',
                                     'name': 'Eupenifeldin',
                                     'reason': 'Does not contain a beta-lactam '
                                               'ring'},
                                 {   'smiles': 'O1[C@@H](O[C@@H]2[C@@H](OC[C@H]3O[C@@H](O[C@H]4[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]4CO)O[C@H]5[C@H](O)[C@@H](NC(=O)C)C(O[C@@H]5CO[C@@H]6O[C@H]([C@@H](O)[C@@H](O)[C@@H]6O)C)O)[C@@H](O)[C@@H](O[C@H]7O[C@@H]([C@@H](O)[C@H](O)[C@@H]7O[C@@H]8O[C@@H]([C@@H](O[C@@H]9O[C@@H]([C@H](O)[C@H](O)[C@H]9NC(=O)C)CO)[C@H](O)[C@H]8NC(=O)C)CO)CO)[C@@H]3O)O[C@@H]([C@@H](O)[C@@H]2O)CO)[C@H](NC(=O)C)[C@@H](O[C@@H]%10O[C@H]([C@@H](O)[C@@H](O)[C@@H]%10O)C)[C@H](O[C@@H]%11O[C@@H]([C@H](O)[C@H](O)[C@H]%11NC(=O)C)CO)[C@H]1CO',
                                     'name': 'N-[(3R,4R,5S,6R)-5-[(2S,3R,4R,5S,6R)-3-Acetamido-5-[(2S,3S,4S,5R,6R)-4-[(2R,3S,4S,5S,6R)-3-[(2S,3R,4R,5S,6R)-3-acetamido-5-[(2S,3R,4R,5R,6R)-3-acetamido-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-6-[[(2S,3S,4S,5S,6R)-3-[(2S,3R,4R,5S,6R)-3-acetamido-5-[(2S,3R,4R,5R,6R)-3-acetamido-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-6-(hydroxymethyl)-4-[(2R,3S,4R,5S,6S)-3,4,5-trihydroxy-6-methyloxan-2-yl]oxyoxan-2-yl]oxy-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxymethyl]-3,5-dihydroxyoxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-2,4-dihydroxy-6-[[(2R,3S,4R,5S,6S)-3,4,5-trihydroxy-6-methyloxan-2-yl]oxymethyl]oxan-3-yl]acetamide',
                                     'reason': 'Does not contain a beta-lactam '
                                               'ring'},
                                 {   'smiles': 'CN1C[C@@H]2C[C@H](Cn3c2cccc3=O)[C@H]1CC=C',
                                     'name': 'Tinctorine',
                                     'reason': 'Does not contain a beta-lactam '
                                               'ring'},
                                 {   'smiles': 'CCC1=C2COC(CC2=C3C(=C(OC3=N1)C(=O)C4=CC=CC=C4)N)(C)C',
                                     'name': 'LSM-4563',
                                     'reason': 'Does not contain a beta-lactam '
                                               'ring'},
                                 {   'smiles': 'CN1CCN(CC1)C(=O)C[C@@H]2CC[C@H]3[C@H](O2)COC[C@@H](CN3C(=O)NC4=CC5=C(C=C4)OCO5)O',
                                     'name': '(3R,6aS,8S,10aS)-N-(1,3-benzodioxol-5-yl)-3-hydroxy-8-[2-(4-methyl-1-piperazinyl)-2-oxoethyl]-3,4,6,6a,8,9,10,10a-octahydro-2H-pyrano[2,3-c][1,5]oxazocine-1-carboxamide',
                                     'reason': 'Does not contain a beta-lactam '
                                               'ring'}],
    'sample_false_negatives': [   {   'smiles': '[H][C@]1(N[C@@H](C([O-])=O)C(C)(C)S1)[C@H](NC(=O)CC1=CC=CC=C1)C(=O)NCCCC',
                                      'name': 'benzylpenicilloyl-butylamine(1-)',
                                      'reason': 'Does not contain a '
                                                'beta-lactam ring'},
                                  {   'smiles': '[H]C(N[C@@H](C([O-])=O)C(C)(C)S)=C1N=C(Cc2ccccc2)OC1=O',
                                      'name': 'benzylpenicillenate',
                                      'reason': 'Does not contain a '
                                                'beta-lactam ring'}],
    'attempt': 0,
    'reasoning': "Okay, let's analyze the requirements for classifying a "
                 'molecule as a beta-lactam antibiotic. The core feature is '
                 'the presence of a beta-lactam ring, which is a four-membered '
                 'lactam (cyclic amide).  We will use SMARTS to define the '
                 'beta-lactam ring and check if it is present in the molecule. '
                 'We do not need to check for other functional groups as they '
                 'are only present in some of the structures. We also do not '
                 'need to check for a minimum number of atoms or molecular '
                 'weight as that is not part of the definition.',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 252,
    'num_false_positives': 189,
    'num_true_negatives': 141857,
    'num_false_negatives': 2,
    'num_negatives': None,
    'precision': 0.5714285714285714,
    'recall': 0.9921259842519685,
    'f1': 0.7251798561151079,
    'accuracy': 0.99865776528461,
    'negative_predictive_value': 0.9999859014937368}