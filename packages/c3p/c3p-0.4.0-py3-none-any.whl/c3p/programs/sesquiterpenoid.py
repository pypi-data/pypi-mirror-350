"""
Classifies: CHEBI:26658 sesquiterpenoid
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_sesquiterpenoid(smiles: str):
    """
    Determines if a molecule is a sesquiterpenoid based on its SMILES string.
    Sesquiterpenoids are characterized by a 15-carbon skeleton derived from three isoprene units.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a sesquiterpenoid, False otherwise
        str: Reason for classification
    """
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # 1. Check for 15 carbon atoms
    c_count = sum(1 for atom in mol.GetAtoms() if atom.GetAtomicNum() == 6)
    if c_count != 15:
        return False, f"Incorrect number of carbons: {c_count} (should be 15)"

    # 2. Check for isoprene units (using SMARTS pattern).  Allow carbons to be CH2 or CH or C.
    #   a basic branched carbon pattern can be used to detect isoprenoid structures.
    isoprene_pattern = Chem.MolFromSmarts("[CX4]([CX4])([CX4])([CX4])")
    isoprene_matches = mol.GetSubstructMatches(isoprene_pattern)
    if len(isoprene_matches) < 2:  # Typically expect at least 2 branched centers
            return False, f"Not branched as expected for isoprene units, only {len(isoprene_matches)} found"

    # 3. Check for cyclic structures (at least one ring).
    ring_info = mol.GetRingInfo()
    if ring_info.NumRings() == 0:
        return False, "No ring structure found"


    return True, "Contains 15 carbons, appears to be built from isoprene units, and contains a ring."


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:26658',
                          'name': 'sesquiterpenoid',
                          'definition': 'Any terpenoid derived from a '
                                        'sesquiterpene. The term includes '
                                        'compounds in which the C15 skeleton '
                                        'of the parent sesquiterpene has been '
                                        'rearranged or modified by the removal '
                                        'of one or more skeletal atoms '
                                        '(generally methyl groups).',
                          'parents': ['CHEBI:26873'],
                          'xrefs': ['LIPID_MAPS_class:LMPR0103'],
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
                                                 1,
                                                 1,
                                                 1,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 0,
                                                 0,
                                                 1],
                           'max_indent': 2,
                           'imports': [   'from rdkit import Chem',
                                          'from rdkit.Chem import AllChem',
                                          'from rdkit.Chem import '
                                          'rdMolDescriptors'],
                           'imports_count': 3,
                           'methods_called': [   'GetSubstructMatches',
                                                 'GetAtomicNum',
                                                 'MolFromSmarts',
                                                 'NumRings',
                                                 'GetAtoms',
                                                 'MolFromSmiles',
                                                 'GetRingInfo'],
                           'methods_called_count': 7,
                           'smarts_strings': ['[CX4]([CX4])([CX4])([CX4])'],
                           'smarts_strings_count': 1,
                           'defs': ['is_sesquiterpenoid(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, f"Incorrect number of '
                                          'carbons: {c_count} (should be 15)"',
                                          'False, f"Not branched as expected '
                                          'for isoprene units, only '
                                          '{len(isoprene_matches)} found"',
                                          'False, "No ring structure found"',
                                          'True, "Contains 15 carbons, appears '
                                          'to be built from isoprene units, '
                                          'and contains a ring."'],
                           'returns_count': 5,
                           'complexity': 3.6664409020350406},
    'message': None,
    'sample_true_negatives': [   {   'smiles': 'CCN1N=C(N=N1)C2=CC=CC=C2NC(=O)C3=CC=C(C=C3)N4C=NN=N4',
                                     'name': 'N-[2-(2-ethyl-5-tetrazolyl)phenyl]-4-(1-tetrazolyl)benzamide',
                                     'reason': 'Incorrect number of carbons: '
                                               '17 (should be 15)'},
                                 {   'smiles': 'CCS(=O)(=O)N1CC2(C1)[C@@H]([C@@H](N2C(=O)C3CCCC3)CO)C4=CC=C(C=C4)C=CC',
                                     'name': 'LSM-38092',
                                     'reason': 'Incorrect number of carbons: '
                                               '23 (should be 15)'},
                                 {   'smiles': 'O=C/1N/C(/C(=O)N\\C1=C\\C2=CC=CC=C2)=C\\C=3N=CNC3C(C=C)(C)C',
                                     'name': 'DeltaPLH',
                                     'reason': 'Incorrect number of carbons: '
                                               '20 (should be 15)'},
                                 {   'smiles': 'C1CCN(CC1)C(=O)C[C@H]2C[C@@H]3[C@H]([C@@H](O2)CO)OC4=C3C=C(C=C4)NC(=O)CC5CC5',
                                     'name': 'N-[(1S,3R,4aS,9aR)-1-(hydroxymethyl)-3-[2-oxo-2-(1-piperidinyl)ethyl]-3,4,4a,9a-tetrahydro-1H-pyrano[3,4-b]benzofuran-6-yl]-2-cyclopropylacetamide',
                                     'reason': 'Incorrect number of carbons: '
                                               '24 (should be 15)'},
                                 {   'smiles': 'C[C@H]1C[C@@]2(OC(=O)c3ccccc3)[C@H]([C@H]1OC(C)=O)[C@@H](O)\\C(C)=C/C[C@H]1[C@@H](\\C=C(C)\\C2=O)C1(C)C',
                                     'name': '(-)-(6Z,12E,2S,3S,4R,5R,9S,11S,15R)-3-acetoxy-15-benzoyloxylathyra-6,12-dien-5-ol-14-one',
                                     'reason': 'Incorrect number of carbons: '
                                               '29 (should be 15)'},
                                 {   'smiles': 'O=C1C(O)=CC=2O[C@]3([C@H](O)C[C@@H]4[C@](OC=5C=C(O)C(C=C(C5C4)C)=O)(CC=CC(C[C@H]3CC2C(=C1)C)(C)C)C)C',
                                     'name': 'Eupenifeldin',
                                     'reason': 'Incorrect number of carbons: '
                                               '33 (should be 15)'},
                                 {   'smiles': 'O1[C@@H](O[C@@H]2[C@@H](OC[C@H]3O[C@@H](O[C@H]4[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]4CO)O[C@H]5[C@H](O)[C@@H](NC(=O)C)C(O[C@@H]5CO[C@@H]6O[C@H]([C@@H](O)[C@@H](O)[C@@H]6O)C)O)[C@@H](O)[C@@H](O[C@H]7O[C@@H]([C@@H](O)[C@H](O)[C@@H]7O[C@@H]8O[C@@H]([C@@H](O[C@@H]9O[C@@H]([C@H](O)[C@H](O)[C@H]9NC(=O)C)CO)[C@H](O)[C@H]8NC(=O)C)CO)CO)[C@@H]3O)O[C@@H]([C@@H](O)[C@@H]2O)CO)[C@H](NC(=O)C)[C@@H](O[C@@H]%10O[C@H]([C@@H](O)[C@@H](O)[C@@H]%10O)C)[C@H](O[C@@H]%11O[C@@H]([C@H](O)[C@H](O)[C@H]%11NC(=O)C)CO)[C@H]1CO',
                                     'name': 'N-[(3R,4R,5S,6R)-5-[(2S,3R,4R,5S,6R)-3-Acetamido-5-[(2S,3S,4S,5R,6R)-4-[(2R,3S,4S,5S,6R)-3-[(2S,3R,4R,5S,6R)-3-acetamido-5-[(2S,3R,4R,5R,6R)-3-acetamido-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-6-[[(2S,3S,4S,5S,6R)-3-[(2S,3R,4R,5S,6R)-3-acetamido-5-[(2S,3R,4R,5R,6R)-3-acetamido-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-6-(hydroxymethyl)-4-[(2R,3S,4R,5S,6S)-3,4,5-trihydroxy-6-methyloxan-2-yl]oxyoxan-2-yl]oxy-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxymethyl]-3,5-dihydroxyoxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-2,4-dihydroxy-6-[[(2R,3S,4R,5S,6S)-3,4,5-trihydroxy-6-methyloxan-2-yl]oxymethyl]oxan-3-yl]acetamide',
                                     'reason': 'Incorrect number of carbons: '
                                               '78 (should be 15)'},
                                 {   'smiles': 'CN1C[C@@H]2C[C@H](Cn3c2cccc3=O)[C@H]1CC=C',
                                     'name': 'Tinctorine',
                                     'reason': 'Not branched as expected for '
                                               'isoprene units, only 1 found'},
                                 {   'smiles': 'CCC1=C2COC(CC2=C3C(=C(OC3=N1)C(=O)C4=CC=CC=C4)N)(C)C',
                                     'name': 'LSM-4563',
                                     'reason': 'Incorrect number of carbons: '
                                               '21 (should be 15)'},
                                 {   'smiles': 'CN1CCN(CC1)C(=O)C[C@@H]2CC[C@H]3[C@H](O2)COC[C@@H](CN3C(=O)NC4=CC5=C(C=C4)OCO5)O',
                                     'name': '(3R,6aS,8S,10aS)-N-(1,3-benzodioxol-5-yl)-3-hydroxy-8-[2-(4-methyl-1-piperazinyl)-2-oxoethyl]-3,4,6,6a,8,9,10,10a-octahydro-2H-pyrano[2,3-c][1,5]oxazocine-1-carboxamide',
                                     'reason': 'Incorrect number of carbons: '
                                               '24 (should be 15)'}],
    'sample_false_negatives': [   {   'smiles': 'O=C1C(C2C(C3[C@](C4(C(C5(C(C(=O)C(C)(C)CC5)CC4)C)CC3)C)(C)CC2)(C)CC1OC(=O)C)(C)C',
                                      'name': '2a-Acetoxy-3,22-stictandione',
                                      'reason': 'Incorrect number of carbons: '
                                                '32 (should be 15)'},
                                  {   'smiles': 'C\\C(CO)=C/CC\\C(C)=C\\CC\\C(C)=C\\CO',
                                      'name': '(2E,6E,10E)-omega-hydroxyfarnesol',
                                      'reason': 'Not branched as expected for '
                                                'isoprene units, only 0 found'},
                                  {   'smiles': 'O(CC1=CC[C@@]2(C[C@@H](O)[C@]([C@H]2CC1)(O)C(C)C)C)C',
                                      'name': '14-O-methyl CAF-603',
                                      'reason': 'Incorrect number of carbons: '
                                                '16 (should be 15)'},
                                  {   'smiles': 'CO[C@H]1CC(=O)C([C@H]2OC(=O)C(=C)[C@@H]2CCC(C)=O)=C1C',
                                      'name': '3-O-methyl-isosecotanapartholide',
                                      'reason': 'Incorrect number of carbons: '
                                                '16 (should be 15)'},
                                  {   'smiles': 'O=C(OC[C@@]12[C@@]3([C@@]4(OC4)[C@H](O[C@@H]1C=C(C)CC2)C[C@H]3OC(=O)/C=C\\C=C\\[C@H](O)[C@H](OC(=O)C)C)C)/C=C(/CCO)\\C',
                                      'name': "13'-Acetyltrichoverrin B",
                                      'reason': 'Incorrect number of carbons: '
                                                '31 (should be 15)'},
                                  {   'smiles': 'O1C=2C=3C([N+]([O-])=C(C2C[C@H]1[C@](O)(/C=C/C=C(/CCC=C(C)C)\\C)C)C)=CC=CC3',
                                      'name': 'Aurachin G',
                                      'reason': 'Incorrect number of carbons: '
                                                '25 (should be 15)'},
                                  {   'smiles': 'OC1=C(C#CC(=C)CC/C=C(/CCC=C(C)C)\\C)C=C(O)C=C1',
                                      'name': 'Pestalotioquinol E',
                                      'reason': 'Incorrect number of carbons: '
                                                '21 (should be 15)'},
                                  {   'smiles': 'C\\C=C(\\C)C(=O)O[C@@H]1\\C=C(C)/[C@@H](O)C[C@H](OC(C)=O)\\C(C)=C/[C@H]2OC(=O)C(=C)[C@H]12',
                                      'name': 'Eupacunin',
                                      'reason': 'Incorrect number of carbons: '
                                                '22 (should be 15)'},
                                  {   'smiles': 'O=C1C(=CC2OC3[C@@]4([C@@]([C@]2([C@@H]1O)C)(C(OC(=O)C)C3)C)OC4)C',
                                      'name': '(S)-7-hydroxytrichothecolone '
                                              'acetate',
                                      'reason': 'Incorrect number of carbons: '
                                                '17 (should be 15)'},
                                  {   'smiles': 'O=C1C=C2[C@]([C@H](CC[C@H]2OC(=O)C(CC(CC(CC)C)C)C)C)(C)C3[C@]1(O3)C(=C)CO',
                                      'name': 'Xylarenone C',
                                      'reason': 'Incorrect number of carbons: '
                                                '26 (should be 15)'}],
    'attempt': 0,
    'reasoning': "Okay, let's break down how to classify sesquiterpenoids.\n"
                 '\n'
                 '**Reasoning:**\n'
                 '\n'
                 'Sesquiterpenoids are a class of terpenes characterized by a '
                 '15-carbon skeleton.  This skeleton is typically assembled '
                 'from three isoprene units (C5H8). They often have cyclic '
                 'structures, but can also be acyclic, and they can have '
                 'various functional groups, including hydroxyls, ketones, '
                 'aldehydes, esters, and epoxides. The core structure is '
                 'important, but various rearrangements and modifications are '
                 'allowed, such as removing methyl groups.\n'
                 '\n'
                 "Therefore, we'll implement the function `is_sesquiterpenoid` "
                 'as follows:\n'
                 '1. **Check for 15 Carbon atoms:** We will verify the '
                 'molecule contains 15 carbon atoms.\n'
                 '2. **Check for Isoprene units:** We will look for patterns '
                 'consistent with isoprene units, such as branched chains of '
                 'carbons.\n'
                 '3. **Consider Cyclic Structures:** Because they are often '
                 'cyclic, we check for the presence of at least one ring '
                 'structure\n'
                 '4. **Allow Modifications:** While we need the 15 carbon '
                 'skeleton as a foundation, the molecule can contain other '
                 'functional groups, which will not be tested specifically.\n'
                 '\n'
                 "Here's the implementation in Python:",
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 858,
    'num_false_positives': 961,
    'num_true_negatives': 138954,
    'num_false_negatives': 1527,
    'num_negatives': None,
    'precision': 0.47168774051676743,
    'recall': 0.35974842767295595,
    'f1': 0.4081826831588963,
    'accuracy': 0.9825158116654954,
    'negative_predictive_value': 0.989130202660858}