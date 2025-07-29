"""
Classifies: CHEBI:87691 tetradecanoate ester
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors


def is_tetradecanoate_ester(smiles: str):
    """
    Determines if a molecule is a tetradecanoate ester based on its SMILES string.
    A tetradecanoate ester is an ester of tetradecanoic acid (myristic acid) with an alcohol or phenol.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a tetradecanoate ester, False otherwise
        str: Reason for classification
    """
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for the basic ester group
    ester_pattern = Chem.MolFromSmarts("[CX3](=[OX1])[OX2]")
    if not mol.HasSubstructMatch(ester_pattern):
        return False, "No ester group found"
    
    # Check for the tetradecanoyl group
    # This pattern describes a carbonyl group connected to a chain of 13 carbons:
    # C(=O)-[CH2]-[CH2]-[CH2]-[CH2]-[CH2]-[CH2]-[CH2]-[CH2]-[CH2]-[CH2]-[CH2]-[CH2]-[CH3]
    tetradecanoyl_pattern = Chem.MolFromSmarts("C(=O)-[CH2]-[CH2]-[CH2]-[CH2]-[CH2]-[CH2]-[CH2]-[CH2]-[CH2]-[CH2]-[CH2]-[CH2]-[CH3]")
    if not mol.HasSubstructMatch(tetradecanoyl_pattern):
        return False, "No tetradecanoyl group found"

    #Check that the carbonyl is part of an ester, and that the tetradecanoyl is part of the ester group, not a free acid:
    tetradecanoyl_ester_pattern = Chem.MolFromSmarts("[OX2][CX3](=[OX1])-[CH2]-[CH2]-[CH2]-[CH2]-[CH2]-[CH2]-[CH2]-[CH2]-[CH2]-[CH2]-[CH2]-[CH2]-[CH3]")
    if not mol.HasSubstructMatch(tetradecanoyl_ester_pattern):
        return False, "Tetradecanoyl is not part of an ester group"

    #Verify minimum number of carbons (14 in tetradecanoyl and at least one more carbon in the alcohol chain)
    c_count = sum(1 for atom in mol.GetAtoms() if atom.GetAtomicNum() == 6)
    if c_count < 15:
         return False, "Too few carbons to be a tetradecanoate ester"
    
    # Verify that molecular weight is greater than 200 (to exclude small molecules)
    mol_wt = rdMolDescriptors.CalcExactMolWt(mol)
    if mol_wt < 200:
        return False, "Molecular weight too low for tetradecanoate ester"

    return True, "Contains tetradecanoyl group in an ester linkage"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:87691',
                          'name': 'tetradecanoate ester',
                          'definition': 'A fatty acid ester obtained by '
                                        'condensation of the carboxy group of '
                                        'tetradecanoic acid (also known as '
                                        'myristic acid) with a hydroxy group '
                                        'of an alcohol or phenol.',
                          'parents': ['CHEBI:35748'],
                          'xrefs': ['PMID:26212120'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 36,
                           'log_lines_of_code': 3.58351893845611,
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
                                                 1,
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
                                                 1,
                                                 1,
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
                           'methods_called': [   'CalcExactMolWt',
                                                 'GetAtoms',
                                                 'GetAtomicNum',
                                                 'MolFromSmiles',
                                                 'MolFromSmarts',
                                                 'HasSubstructMatch'],
                           'methods_called_count': 6,
                           'smarts_strings': [   '[CX3](=[OX1])[OX2]',
                                                 '[OX2][CX3](=[OX1])-[CH2]-[CH2]-[CH2]-[CH2]-[CH2]-[CH2]-[CH2]-[CH2]-[CH2]-[CH2]-[CH2]-[CH2]-[CH3]',
                                                 'C(=O)-[CH2]-[CH2]-[CH2]-[CH2]-[CH2]-[CH2]-[CH2]-[CH2]-[CH2]-[CH2]-[CH2]-[CH2]-[CH3]'],
                           'smarts_strings_count': 3,
                           'defs': ['is_tetradecanoate_ester(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "No ester group found"',
                                          'False, "No tetradecanoyl group '
                                          'found"',
                                          'False, "Tetradecanoyl is not part '
                                          'of an ester group"',
                                          'False, "Too few carbons to be a '
                                          'tetradecanoate ester"',
                                          'False, "Molecular weight too low '
                                          'for tetradecanoate ester"',
                                          'True, "Contains tetradecanoyl group '
                                          'in an ester linkage"'],
                           'returns_count': 7,
                           'complexity': 3.9167037876912216},
    'message': None,
    'sample_true_negatives': [   {   'smiles': 'O1[C@@H](OC[C@H]2OC(O)[C@H](NC(=O)C)[C@@H](O)[C@H]2O)[C@H](O)[C@@H](O)[C@@H](O)[C@H]1CO',
                                     'name': 'beta-D-Galp-(1->6)-D-GalpNAc',
                                     'reason': 'No ester group found'},
                                 {   'smiles': 'O1C=2C(C(=CC1=O)CC)=CC=C(OC(=O)C=3OC=CC3)C2',
                                     'name': '(4-Ethyl-2-oxochromen-7-yl) '
                                             'furan-2-carboxylate',
                                     'reason': 'No tetradecanoyl group found'},
                                 {   'smiles': 'CCCNC(=O)[C@H]1[C@@H]([C@H]2CN3C(=CC=C(C3=O)C4=CC=NC=C4)[C@@H]1N2CC5=CC=CC=C5F)CO',
                                     'name': 'LSM-13437',
                                     'reason': 'No ester group found'},
                                 {   'smiles': 'CC1(C)[C@H]2CC[C@]1(CS([O-])(=O)=O)C(=O)C2',
                                     'name': '(R)-camphorsulfonate',
                                     'reason': 'No ester group found'},
                                 {   'smiles': 'P(OC[C@H](OC(=O)CCCCCCCCC/C=C\\C/C=C\\CCCCC)COC(=O)CCCCCCC/C=C\\C/C=C\\CCCCC)(OC[C@H](N)C(O)=O)(O)=O',
                                     'name': 'PS(18:2(9Z,12Z)/20:2(11Z,14Z))',
                                     'reason': 'No tetradecanoyl group found'},
                                 {   'smiles': 'N[C@@H](CCCC(O)=O)C(O)=O',
                                     'name': 'L-2-aminoadipic acid',
                                     'reason': 'No tetradecanoyl group found'},
                                 {   'smiles': 'C(\\CC)=C\\C/C=C\\CC1C(C/C=C\\C/C=C\\CCCC(=O)O)O1',
                                     'name': '(5Z,8Z,14Z,17Z)-11,12-epoxyicosatetraenoic '
                                             'acid',
                                     'reason': 'No tetradecanoyl group found'},
                                 {   'smiles': 'O[C@H]1[C@@H](CCC(=CCCC(=C1)C)C)C(C(O)=O)=C',
                                     'name': '2-[(1S,2R,3E,7E)-2-Hydroxy-4,8-dimethylcyclodeca-3,7-dien-1-yl]prop-2-enoic '
                                             'acid',
                                     'reason': 'No tetradecanoyl group found'},
                                 {   'smiles': 'C1[C@@H]2[C@H]([C@@H]([C@@H](N2CC3=CN=CC=C3)C4=CC=CC(=O)N41)C(=O)NCC5=CC6=C(C=C5)OCO6)CO',
                                     'name': 'LSM-8906',
                                     'reason': 'No ester group found'},
                                 {   'smiles': '[H][C@]1(CC(=O)c2c(O)cc(O)c(C[C@@H](CC=C(C)C)C(C)=C)c2O1)c1c(O)cccc1O',
                                     'name': 'exiguaflavanone A',
                                     'reason': 'No ester group found'}],
    'sample_false_negatives': [],
    'attempt': 0,
    'reasoning': "Okay, let's break down the problem of classifying "
                 'tetradecanoate esters.\n'
                 '\n'
                 '**Understanding Tetradecanoate Esters**\n'
                 '\n'
                 'A tetradecanoate ester is formed when tetradecanoic acid '
                 '(myristic acid) reacts with an alcohol or phenol. Myristic '
                 'acid has 14 carbon atoms, a linear chain, and a carboxylic '
                 'acid group. The key characteristic we need to identify is '
                 'the 13-carbon alkyl chain attached to a carbonyl group that '
                 'is, in turn, connected to an oxygen (the ester bond).  This '
                 "defines the 'tetradecanoyl' part of the molecule. The rest "
                 'of the molecule attached to the ester is variable.\n'
                 '\n'
                 '**Strategy**\n'
                 '\n'
                 '1. **Check for Basic Ester Structure:** The molecule must '
                 'contain an ester group (-C(=O)-O-).\n'
                 '2. **Check for Tetradecanoyl Group:**  Use SMARTS to find '
                 'the 13-carbon chain with terminal carbonyl.\n'
                 '3. **Exclude Free Myristic Acid**: Verify there is no free '
                 'carboxylic acid. Myristic acid should have the carbonyl '
                 'connected to an oxygen, i.e., as part of an ester.\n'
                 '4. **Consider Complexity**:  These esters can be part of '
                 'complex molecules. We should check the minimum number of '
                 'carbons on the main chain to exclude small esters and also '
                 'the molecular weight to exclude small molecules.\n'
                 '5. **Handle failures**: Return (False, "reason") for all '
                 'fail cases.\n'
                 '\n'
                 '**Code Implementation**',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 68,
    'num_false_positives': 526,
    'num_true_negatives': 141706,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.11447811447811448,
    'recall': 1.0,
    'f1': 0.20543806646525684,
    'accuracy': 0.9963035839775123,
    'negative_predictive_value': 1.0}