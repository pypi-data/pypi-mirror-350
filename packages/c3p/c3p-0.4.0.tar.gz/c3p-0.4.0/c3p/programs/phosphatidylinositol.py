"""
Classifies: CHEBI:28874 phosphatidylinositol
"""
"""
Classifies: CHEBI:28874 phosphatidylinositol
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_phosphatidylinositol(smiles: str):
    """
    Determines if a molecule is a phosphatidylinositol based on its SMILES string.
    A phosphatidylinositol has a glycerol backbone with two fatty acid chains and a phosphoinositol group.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a phosphatidylinositol, False otherwise
        str: Reason for classification
    """
    
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Look for glycerol backbone pattern (C-C-C with 2 oxygens attached)
    glycerol_pattern = Chem.MolFromSmarts("[CH2X4][CHX4][CH2X4]")
    if not mol.HasSubstructMatch(glycerol_pattern):
        return False, "No glycerol backbone found"
        
    # Look for 2 ester groups (-O-C(=O)-) for fatty acid chains
    ester_pattern = Chem.MolFromSmarts("[OX2][CX3](=[OX1])")
    ester_matches = mol.GetSubstructMatches(ester_pattern)
    if len(ester_matches) != 2:
        return False, f"Found {len(ester_matches)} ester groups, need exactly 2"

    # Check for phosphoinositol group (phosphate connected to inositol)
    phosphoinositol_pattern = Chem.MolFromSmarts("[OX2]P(=O)([OX2])[OX2][C@H]1[C@H](O)[C@H](O)[C@H](O)[C@H](O)[C@H]1O")
    if not mol.HasSubstructMatch(phosphoinositol_pattern):
        return False, "No phosphoinositol group found"

    # Count rotatable bonds to verify long chains
    n_rotatable = rdMolDescriptors.CalcNumRotatableBonds(mol)
    if n_rotatable < 10:
        return False, "Chains too short to be fatty acids"

    # Check molecular weight - phosphatidylinositol typically >600 Da
    mol_wt = rdMolDescriptors.CalcExactMolWt(mol)
    if mol_wt < 600:
        return False, "Molecular weight too low for phosphatidylinositol"

    # Count carbons and oxygens
    c_count = sum(1 for atom in mol.GetAtoms() if atom.GetAtomicNum() == 6)
    o_count = sum(1 for atom in mol.GetAtoms() if atom.GetAtomicNum() == 8)
    
    if c_count < 20:
        return False, "Too few carbons for phosphatidylinositol"
    if o_count < 8:
        return False, "Must have at least 8 oxygens (2 ester groups and phosphoinositol)"

    return True, "Contains glycerol backbone with 2 fatty acid chains and a phosphoinositol group"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:28874',
                          'name': 'phosphatidylinositol',
                          'definition': 'Any glycerophosphoinositol having one '
                                        'phosphatidyl group esterified to one '
                                        'of the hydroxy groups of inositol.',
                          'parents': ['CHEBI:36315'],
                          'xrefs': [   'DrugBank:DB02144',
                                       'PMID:15634688',
                                       'PMID:15967713',
                                       'PMID:17417879',
                                       'PMID:18189424',
                                       'PMID:19456874',
                                       'PMID:23015060',
                                       'PMID:23118092',
                                       'Wikipedia:Phosphatidylinositol'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': None,
    'message': None,
    'sample_true_negatives': [   {   'smiles': 'OC[C@H]1O[C@H](C[C@@H]1O)N1C=NC2=C1N=CNC[C@H]2O',
                                     'name': 'pentostatin',
                                     'reason': 'No glycerol backbone found'},
                                 {   'smiles': 'O1C(CCC=2C1=CC(OC3OC(C(O)C(O)C3O)C(O)=O)=C(C2OC)C=4C(=O)C=5C(OC4)=CC(O)=C(O)C5)(C)C',
                                     'name': '6-{[6-(6,7-dihydroxy-4-oxo-4H-chromen-3-yl)-5-methoxy-2,2-dimethyl-3,4-dihydro-2H-1-benzopyran-7-yl]oxy}-3,4,5-trihydroxyoxane-2-carboxylic '
                                             'acid',
                                     'reason': 'No glycerol backbone found'},
                                 {   'smiles': 'O=C1O[C@@H]([C@@H](OC)C=CC=C(C[C@@H](C)[C@@H]([C@@H]([C@@H]([C@@H](C=C(C=C1OC)C)C)O)C)O)C)[C@H]([C@@H](O)[C@@H]([C@@]2(O[C@H](/C=C/C)[C@@H](C)[C@@H](C2)OC3OC(C(O)C(C3)O)C)O)C)C',
                                     'name': 'Concanamycin D',
                                     'reason': 'No glycerol backbone found'},
                                 {   'smiles': 'O1[C@@H](O[C@@H]2[C@@H](O)[C@@H](O[C@@H]([C@@H]2O)CO)O[C@H]3[C@H](O)[C@@H](NC(=O)C)C(O[C@@H]3CO)O)[C@H](NC(=O)C)[C@@H](O[C@@H]4O[C@@H]([C@H](O)[C@H](O)[C@H]4O)CO)[C@H](O[C@@H]5O[C@H]([C@@H](O)[C@@H](O)[C@@H]5O)C)[C@H]1CO',
                                     'name': 'N-[(3R,4R,5S,6R)-5-[(2S,3R,4S,5S,6R)-4-[(2S,3R,4R,5S,6R)-3-Acetamido-6-(hydroxymethyl)-4-[(2R,3R,4S,5R,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-5-[(2S,3S,4R,5S,6S)-3,4,5-trihydroxy-6-methyloxan-2-yl]oxyoxan-2-yl]oxy-3,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-2,4-dihydroxy-6-(hydroxymethyl)oxan-3-yl]acetamide',
                                     'reason': 'No glycerol backbone found'},
                                 {   'smiles': 'O=C(O)[C@]1([C@H]2[C@@](OC=3C=C4C5=C(C=CC=C5)NC4=CC3CC2)(CC[C@@H]1O)C)C',
                                     'name': 'Oxiamycin',
                                     'reason': 'No glycerol backbone found'},
                                 {   'smiles': 'C1CCC(C1)CC#CC2=CC=C(C=C2)[C@@H]3[C@@H]4CN(CC(=O)N4[C@@H]3CO)C(=O)C5=CC=C(C=C5)F',
                                     'name': '(6R,7R,8S)-7-[4-(3-cyclopentylprop-1-ynyl)phenyl]-4-[(4-fluorophenyl)-oxomethyl]-8-(hydroxymethyl)-1,4-diazabicyclo[4.2.0]octan-2-one',
                                     'reason': 'Found 0 ester groups, need '
                                               'exactly 2'},
                                 {   'smiles': 'S(=O)(C(SSCCC)CC)CCC',
                                     'name': 'Propyl 1-(propylsulfinyl)propyl '
                                             'disulfide',
                                     'reason': 'No glycerol backbone found'},
                                 {   'smiles': 'ClC=1C(=O)[C@@H]([C@@](O)(C/C=C\\CCCCC)C1)C[C@H](OC(=O)C)[C@@H](OC(=O)C)CCCC(OC)=O',
                                     'name': 'punaglandin 6',
                                     'reason': 'No glycerol backbone found'},
                                 {   'smiles': 'CCCCCCCCCCCCCCCCCCCCCCCC[C@H](O)C(=O)N[C@@H](COP(O)(=O)O[C@H]1[C@H](O)[C@@H](O)[C@H](O)[C@@H](O)[C@H]1O)[C@H](O)[C@@H](O)CCCCCCCCCCCCCC',
                                     'name': 'Ins-1-P-Cer(t18:0/2-OH-26:0)',
                                     'reason': 'No glycerol backbone found'},
                                 {   'smiles': 'CCC(C)(C)C(=O)OC1CC(C=C2C1[C@H]([C@H](C=C2)C)CC[C@@H]3CC(CC(=O)O3)O)C',
                                     'name': '2,2-dimethylbutanoic acid '
                                             '[(7S,8S)-8-[2-[(2R)-4-hydroxy-6-oxo-2-oxanyl]ethyl]-3,7-dimethyl-1,2,3,7,8,8a-hexahydronaphthalen-1-yl] '
                                             'ester',
                                     'reason': 'No phosphoinositol group '
                                               'found'}],
    'sample_false_negatives': [   {   'smiles': 'P(OC1[C@H](O)[C@H](O)C(O)[C@H](O)[C@H]1O)(OC[C@H](OC(=O)CCCCCCC/C=C\\C/C=C\\CCCCC)COC(=O)CCCCCCC/C=C\\C/C=C\\CCCCC)([O-])=O',
                                      'name': '18:2-18:2-PI',
                                      'reason': 'No phosphoinositol group '
                                                'found'},
                                  {   'smiles': 'CCCC(=O)OC[C@H](COP(O)(=O)O[C@H]1[C@H](O)[C@@H](O)[C@H](O)[C@@H](O)[C@H]1O)OC(=O)CCC',
                                      'name': "1,2-dibutyryl-sn-glycero-3-phospho-(1'D-myo-inositol)",
                                      'reason': 'Molecular weight too low for '
                                                'phosphatidylinositol'},
                                  {   'smiles': '[C@@H]1([C@@H]([C@@H](O)[C@H]([C@H]([C@@H]1O)OP(=O)(OCOC(=O)CCC)OCOC(=O)CCC)O)OP(=O)(OCOC(=O)CCC)OCOC(=O)CCC)OP(=O)(OCOC(=O)CCC)OCOC(=O)CCC',
                                      'name': 'D-myo-Ins(1,4,5)P3 '
                                              'hexakis(butyryloxymethyl) ester',
                                      'reason': 'No glycerol backbone found'},
                                  {   'smiles': 'P(OC1[C@H](O)[C@@H](O)C(O)[C@@H](O)[C@H]1O)(OC[C@H](OC(=O)CCCCCCC/C=C\\C/C=C\\C/C=C\\CC)COC(=O)CCCCCCCCCCCCCCCCC)([O-])=O',
                                      'name': '18:0-18:3-PI',
                                      'reason': 'No phosphoinositol group '
                                                'found'},
                                  {   'smiles': 'P(OC1C(O)C(O)C(O)[C@@H](O)C1O)(OC[C@H](OC(=O)CCC(O)/C=C/C(O)=O)COC(=O)CCCCCCCCCCCCCCC)(O)=O',
                                      'name': 'PHHdiA-PI',
                                      'reason': 'Found 3 ester groups, need '
                                                'exactly 2'},
                                  {   'smiles': 'P(OC1C(O)C(O)C(O)[C@@H](O)C1O)(OC[C@H](OC(=O)CCCC(=O)/C=C/C(O)=O)COC(=O)CCCCCCCCCCCCCCC)(O)=O',
                                      'name': 'PKODiA-PI',
                                      'reason': 'Found 3 ester groups, need '
                                                'exactly 2'},
                                  {   'smiles': 'P(OC1C(O)C(O)C(O)[C@@H](O)C1O)(OC[C@H](OC(=O)CCCCCCCC(O)/C=C/C(O)=O)COC(=O)CCCCCCC/C=C\\CCCCCCCC)(O)=O',
                                      'name': 'OHDdiA-PI',
                                      'reason': 'Found 3 ester groups, need '
                                                'exactly 2'},
                                  {   'smiles': 'P(OC1[C@@H](O)[C@H](O)C(O)[C@H](O)[C@@H]1O)(OC[C@H](OC(=O)CCCCC)COC(=O)CCCCC)(O)=O',
                                      'name': 'PtdIns-(1,2-dihexanoyl)',
                                      'reason': 'Molecular weight too low for '
                                                'phosphatidylinositol'},
                                  {   'smiles': 'P(OC1C(O)C(O)C(O)[C@@H](O)C1O)(OC[C@H](OC(=O)CCCCCCCC(O)=O)COC(=O)CCCCCCCCCCCCCCC)(O)=O',
                                      'name': 'PA-PI',
                                      'reason': 'Found 3 ester groups, need '
                                                'exactly 2'},
                                  {   'smiles': 'CCCCCCCC(=O)OC[C@H](COP(O)(=O)O[C@H]1[C@H](O)[C@@H](O)[C@H](O)[C@@H](O)[C@H]1O)OC(=O)CCCCCCC',
                                      'name': '1,2-dioctanoyl-sn-glycero-3-phospho-1D-myo-inositol',
                                      'reason': 'Molecular weight too low for '
                                                'phosphatidylinositol'}],
    'attempt': 0,
    'reasoning': 'To classify chemical entities as phosphatidylinositol, we '
                 'need to identify the key structural features of this class. '
                 'Phosphatidylinositol consists of a glycerol backbone, two '
                 'fatty acid chains attached via ester bonds, and a '
                 'phosphoinositol group attached to the third position of the '
                 'glycerol. The inositol group is a six-membered ring with '
                 'hydroxyl groups, and the phosphate group connects the '
                 'glycerol to the inositol.\n'
                 '\n'
                 'Here is the Python program that classifies a molecule as '
                 'phosphatidylinositol based on its SMILES string:',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 299,
    'num_false_positives': 17,
    'num_true_negatives': 141962,
    'num_false_negatives': 22,
    'num_negatives': None,
    'precision': 0.9462025316455697,
    'recall': 0.9314641744548287,
    'f1': 0.9387755102040817,
    'accuracy': 0.9997259311314125,
    'negative_predictive_value': 0.9998450529637142}