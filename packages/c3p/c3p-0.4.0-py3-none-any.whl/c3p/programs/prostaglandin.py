"""
Classifies: CHEBI:26333 prostaglandin
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_prostaglandin(smiles: str):
    """
    Determines if a molecule is a prostaglandin based on its SMILES string.
    Prostaglandins are derived from prostanoic acid, a C20 fatty acid with a cyclopentane ring.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a prostaglandin, False otherwise
        str: Reason for classification
    """
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # 1. Check for cyclopentane ring with attached chains
    cyclopentane_pattern = Chem.MolFromSmarts("[C]1[C][C][C][C]1")  #Basic 5 member ring
    if not mol.HasSubstructMatch(cyclopentane_pattern):
        return False, "No cyclopentane ring found"

    #2. Check for a carboxyl acid group
    carboxyl_pattern = Chem.MolFromSmarts("C(=O)O")
    if not mol.HasSubstructMatch(carboxyl_pattern):
        return False, "No carboxyl group found"

    #3. Check for 20 carbons
    c_count = sum(1 for atom in mol.GetAtoms() if atom.GetAtomicNum() == 6)
    if c_count != 20:
        return False, f"Not 20 carbons, found {c_count}"
    
    #4. Check for at least one double bond
    double_bond_pattern = Chem.MolFromSmarts("[C]=[C]")
    if not mol.HasSubstructMatch(double_bond_pattern):
        return False, "No double bond found"

    # 5. Check for 4-6 oxygens
    o_count = sum(1 for atom in mol.GetAtoms() if atom.GetAtomicNum() == 8)
    if o_count < 4 or o_count > 6:
        return False, f"Oxygen count is not between 4 and 6, found {o_count}"

    return True, "Meets basic prostaglandin criteria"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:26333',
                          'name': 'prostaglandin',
                          'definition': 'Naturally occurring compounds derived '
                                        'from the parent C20 acid, prostanoic '
                                        'acid.',
                          'parents': ['CHEBI:26347'],
                          'xrefs': [   'CAS:11000-26-3',
                                       'LIPID_MAPS_class:LMFA0301'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 34,
                           'log_lines_of_code': 3.5263605246161616,
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
                                                 2,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
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
                                                 1],
                           'max_indent': 2,
                           'imports': [   'from rdkit import Chem',
                                          'from rdkit.Chem import AllChem',
                                          'from rdkit.Chem import '
                                          'rdMolDescriptors'],
                           'imports_count': 3,
                           'methods_called': [   'MolFromSmarts',
                                                 'GetAtomicNum',
                                                 'GetAtoms',
                                                 'HasSubstructMatch',
                                                 'MolFromSmiles'],
                           'methods_called_count': 5,
                           'smarts_strings': [   'C(=O)O',
                                                 '[C]1[C][C][C][C]1',
                                                 '[C]=[C]'],
                           'smarts_strings_count': 3,
                           'defs': ['is_prostaglandin(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "No cyclopentane ring found"',
                                          'False, "No carboxyl group found"',
                                          'False, f"Not 20 carbons, found '
                                          '{c_count}"',
                                          'False, "No double bond found"',
                                          'False, f"Oxygen count is not '
                                          'between 4 and 6, found {o_count}"',
                                          'True, "Meets basic prostaglandin '
                                          'criteria"'],
                           'returns_count': 7,
                           'complexity': 3.7052721049232327},
    'message': None,
    'sample_true_negatives': [   {   'smiles': 'CCN1N=C(N=N1)C2=CC=CC=C2NC(=O)C3=CC=C(C=C3)N4C=NN=N4',
                                     'name': 'N-[2-(2-ethyl-5-tetrazolyl)phenyl]-4-(1-tetrazolyl)benzamide',
                                     'reason': 'No cyclopentane ring found'},
                                 {   'smiles': 'CCS(=O)(=O)N1CC2(C1)[C@@H]([C@@H](N2C(=O)C3CCCC3)CO)C4=CC=C(C=C4)C=CC',
                                     'name': 'LSM-38092',
                                     'reason': 'No carboxyl group found'},
                                 {   'smiles': 'O=C/1N/C(/C(=O)N\\C1=C\\C2=CC=CC=C2)=C\\C=3N=CNC3C(C=C)(C)C',
                                     'name': 'DeltaPLH',
                                     'reason': 'No cyclopentane ring found'},
                                 {   'smiles': 'C1CCN(CC1)C(=O)C[C@H]2C[C@@H]3[C@H]([C@@H](O2)CO)OC4=C3C=C(C=C4)NC(=O)CC5CC5',
                                     'name': 'N-[(1S,3R,4aS,9aR)-1-(hydroxymethyl)-3-[2-oxo-2-(1-piperidinyl)ethyl]-3,4,4a,9a-tetrahydro-1H-pyrano[3,4-b]benzofuran-6-yl]-2-cyclopropylacetamide',
                                     'reason': 'No cyclopentane ring found'},
                                 {   'smiles': 'C[C@H]1C[C@@]2(OC(=O)c3ccccc3)[C@H]([C@H]1OC(C)=O)[C@@H](O)\\C(C)=C/C[C@H]1[C@@H](\\C=C(C)\\C2=O)C1(C)C',
                                     'name': '(-)-(6Z,12E,2S,3S,4R,5R,9S,11S,15R)-3-acetoxy-15-benzoyloxylathyra-6,12-dien-5-ol-14-one',
                                     'reason': 'Not 20 carbons, found 29'},
                                 {   'smiles': 'O=C1C(O)=CC=2O[C@]3([C@H](O)C[C@@H]4[C@](OC=5C=C(O)C(C=C(C5C4)C)=O)(CC=CC(C[C@H]3CC2C(=C1)C)(C)C)C)C',
                                     'name': 'Eupenifeldin',
                                     'reason': 'No cyclopentane ring found'},
                                 {   'smiles': 'O1[C@@H](O[C@@H]2[C@@H](OC[C@H]3O[C@@H](O[C@H]4[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]4CO)O[C@H]5[C@H](O)[C@@H](NC(=O)C)C(O[C@@H]5CO[C@@H]6O[C@H]([C@@H](O)[C@@H](O)[C@@H]6O)C)O)[C@@H](O)[C@@H](O[C@H]7O[C@@H]([C@@H](O)[C@H](O)[C@@H]7O[C@@H]8O[C@@H]([C@@H](O[C@@H]9O[C@@H]([C@H](O)[C@H](O)[C@H]9NC(=O)C)CO)[C@H](O)[C@H]8NC(=O)C)CO)CO)[C@@H]3O)O[C@@H]([C@@H](O)[C@@H]2O)CO)[C@H](NC(=O)C)[C@@H](O[C@@H]%10O[C@H]([C@@H](O)[C@@H](O)[C@@H]%10O)C)[C@H](O[C@@H]%11O[C@@H]([C@H](O)[C@H](O)[C@H]%11NC(=O)C)CO)[C@H]1CO',
                                     'name': 'N-[(3R,4R,5S,6R)-5-[(2S,3R,4R,5S,6R)-3-Acetamido-5-[(2S,3S,4S,5R,6R)-4-[(2R,3S,4S,5S,6R)-3-[(2S,3R,4R,5S,6R)-3-acetamido-5-[(2S,3R,4R,5R,6R)-3-acetamido-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-6-[[(2S,3S,4S,5S,6R)-3-[(2S,3R,4R,5S,6R)-3-acetamido-5-[(2S,3R,4R,5R,6R)-3-acetamido-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-6-(hydroxymethyl)-4-[(2R,3S,4R,5S,6S)-3,4,5-trihydroxy-6-methyloxan-2-yl]oxyoxan-2-yl]oxy-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxymethyl]-3,5-dihydroxyoxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-2,4-dihydroxy-6-[[(2R,3S,4R,5S,6S)-3,4,5-trihydroxy-6-methyloxan-2-yl]oxymethyl]oxan-3-yl]acetamide',
                                     'reason': 'No cyclopentane ring found'},
                                 {   'smiles': 'CN1C[C@@H]2C[C@H](Cn3c2cccc3=O)[C@H]1CC=C',
                                     'name': 'Tinctorine',
                                     'reason': 'No cyclopentane ring found'},
                                 {   'smiles': 'CCC1=C2COC(CC2=C3C(=C(OC3=N1)C(=O)C4=CC=CC=C4)N)(C)C',
                                     'name': 'LSM-4563',
                                     'reason': 'No cyclopentane ring found'},
                                 {   'smiles': 'CN1CCN(CC1)C(=O)C[C@@H]2CC[C@H]3[C@H](O2)COC[C@@H](CN3C(=O)NC4=CC5=C(C=C4)OCO5)O',
                                     'name': '(3R,6aS,8S,10aS)-N-(1,3-benzodioxol-5-yl)-3-hydroxy-8-[2-(4-methyl-1-piperazinyl)-2-oxoethyl]-3,4,6,6a,8,9,10,10a-octahydro-2H-pyrano[2,3-c][1,5]oxazocine-1-carboxamide',
                                     'reason': 'No cyclopentane ring found'}],
    'sample_false_negatives': [   {   'smiles': 'OCC(CO)OC(CCC/C=C/1\\O[C@]2(C[C@H]([C@@H]([C@]2(C1)[H])/C=C/[C@H](CCCCC)O)O)[H])=O',
                                      'name': 'prostaglandin I2 2-glyceryl '
                                              'ester',
                                      'reason': 'Not 20 carbons, found 23'},
                                  {   'smiles': 'C(\\[C@H]1[C@@H](CC([C@@H]1C/C=C\\CCCC(OC(CO)CO)=O)=O)O)=C/[C@H](CCCCC)O',
                                      'name': 'prostaglandin E2 2-glyceryl '
                                              'ester',
                                      'reason': 'Not 20 carbons, found 23'},
                                  {   'smiles': 'CC(C)OC(=O)CCC\\C=C/C[C@H]1[C@@H](O)C[C@@H](O)[C@@H]1\\C=C\\C(F)(F)COc1ccccc1',
                                      'name': 'tafluprost',
                                      'reason': 'Not 20 carbons, found 25'},
                                  {   'smiles': 'O[C@@H]1C[C@H](O)[C@H](C\\C=C/CCCC(O)=O)[C@H]1CCC(=O)CCCCC(O)=O',
                                      'name': '13,14-dihydro-15-oxo-20-carboxy-PGF2alpha',
                                      'reason': 'Oxygen count is not between 4 '
                                                'and 6, found 7'},
                                  {   'smiles': 'C(CCC(O)=O)/C=C\\C[C@@H]1\\C(\\C(C=C1)=O)=C/C=C/C/C=C\\CC',
                                      'name': '15-deoxy-Delta(12,14)-prostaglandin '
                                              'J3',
                                      'reason': 'No cyclopentane ring found'},
                                  {   'smiles': '[C@@H]1(C(C=C[C@@H]1/C=C/[C@H](C/C=C\\CC)O)=O)C/C=C\\CCCC(=O)O',
                                      'name': 'prostaglandin A3',
                                      'reason': 'No cyclopentane ring found'},
                                  {   'smiles': 'C(CCC(O)=O)/C=C\\C[C@@H]1/C(/C(C=C1)=O)=C\\C[C@H](C/C=C\\CC)O',
                                      'name': 'Delta(12)-prostaglandin J3',
                                      'reason': 'No cyclopentane ring found'},
                                  {   'smiles': 'CCCCCCCCCCCCCCCCCCCCCCCCCCCCC(O)=O',
                                      'name': 'nonacosanoic acid',
                                      'reason': 'No cyclopentane ring found'},
                                  {   'smiles': 'C(O)CCCCCC[C@@H]1[C@H]([C@@H](C[C@@H]1O)O)/C=C/[C@H](CCCCC)O',
                                      'name': 'prostaglandin F1alpha alcohol',
                                      'reason': 'No carboxyl group found'},
                                  {   'smiles': 'CCCCC\\C=C\\C=C1\\C=CC(=O)[C@@H]1C\\C=C/CCCC(O)=O',
                                      'name': '15-deoxy-Delta(12,14)-prostaglandin '
                                              'A2',
                                      'reason': 'No cyclopentane ring found'}],
    'attempt': 0,
    'reasoning': "Okay, let's analyze the characteristics of prostaglandins "
                 'and devise a strategy for identifying them from SMILES '
                 'strings.\n'
                 '\n'
                 '**Prostaglandin Characteristics:**\n'
                 '\n'
                 '1.  **Prostanoic Acid Core:** They are all derived from '
                 'prostanoic acid, a C20 fatty acid with a cyclopentane ring.\n'
                 '2.  **Cyclopentane Ring:** They all possess a central '
                 'five-membered ring (cyclopentane), often with substituents.\n'
                 '3.  **Carboxylic Acid Group:** They have a carboxylic acid '
                 'group (COOH) at the end of a fatty acid chain.\n'
                 '4.  **Variations in Substituents:**  The variations between '
                 'prostaglandins arise from different substituents on the '
                 'cyclopentane ring (e.g., hydroxyl groups -OH, keto groups '
                 '=O) and the presence of double bonds.\n'
                 '5.  **C=C double bonds.** Most prostaglandins have at least '
                 'one double bond in either chain or the ring.\n'
                 '6.  **Carbon count.** Prostaglandins have 20 carbons.\n'
                 '7.  **Oxygen count.** Prostaglandins usually contain 4-6 '
                 'oxygens.\n'
                 '\n'
                 '**Strategy:**\n'
                 '\n'
                 "1.  **Basic Skeleton Check:** We'll look for the core "
                 'cyclopentane ring with a chain and a carboxylic acid group.\n'
                 '2.  **Carbon Count:** Check for 20 carbons.\n'
                 '3.  **Double Bond Count:** Check for at least one double '
                 'bond.\n'
                 '4.  **Oxygen Count:** Check for 4-6 oxygens.\n'
                 '5.  **Substituent Analysis:** Checking for specific '
                 'substituents can refine the classification but is not '
                 'required for the basic classification. This would need '
                 "substructure matching, which is expensive. We'll not enforce "
                 'this in the first go.',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 30,
    'num_false_positives': 189,
    'num_true_negatives': 142044,
    'num_false_negatives': 37,
    'num_negatives': None,
    'precision': 0.136986301369863,
    'recall': 0.44776119402985076,
    'f1': 0.20979020979020976,
    'accuracy': 0.9984118060435699,
    'negative_predictive_value': 0.999739585166208}