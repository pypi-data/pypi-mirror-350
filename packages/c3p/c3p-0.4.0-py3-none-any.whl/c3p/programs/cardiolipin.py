"""
Classifies: CHEBI:28494 cardiolipin
"""
"""
Classifies: CHEBI:28494 cardiolipin
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_cardiolipin(smiles: str):
    """
    Determines if a molecule is a cardiolipin based on its SMILES string.
    A cardiolipin is a phosphatidylglycerol composed of two molecules of phosphatidic acid covalently linked to a molecule of glycerol.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a cardiolipin, False otherwise
        str: Reason for classification
    """
    
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Look for the central glycerol backbone pattern (C-C-C with 4 oxygens attached)
    glycerol_pattern = Chem.MolFromSmarts("[CH2X4][CHX4][CH2X4]")
    if not mol.HasSubstructMatch(glycerol_pattern):
        return False, "No glycerol backbone found"

    # Look for 4 ester groups (-O-C(=O)-) corresponding to the fatty acid chains
    ester_pattern = Chem.MolFromSmarts("[OX2][CX3](=[OX1])")
    ester_matches = mol.GetSubstructMatches(ester_pattern)
    if len(ester_matches) != 4:
        return False, f"Found {len(ester_matches)} ester groups, need exactly 4"

    # Look for phosphatidic acid groups (glycerol with phosphate and fatty acid chains)
    phosphatidic_acid_pattern = Chem.MolFromSmarts("[CH2X4][CHX4][CH2X4]([OX2][PX4](=[OX1])([OX2])[OX2])")
    phosphatidic_acid_matches = mol.GetSubstructMatches(phosphatidic_acid_pattern)
    if len(phosphatidic_acid_matches) < 2:
        return False, f"Found {len(phosphatidic_acid_matches)} phosphatidic acid groups, need at least 2"

    # Check for fatty acid chains (long carbon chains attached to esters)
    fatty_acid_pattern = Chem.MolFromSmarts("[CX4,CX3]~[CX4,CX3]~[CX4,CX3]~[CX4,CX3]") 
    fatty_acid_matches = mol.GetSubstructMatches(fatty_acid_pattern)
    if len(fatty_acid_matches) < 4:
        return False, f"Missing fatty acid chains, got {len(fatty_acid_matches)}"

    # Count rotatable bonds to verify long chains
    n_rotatable = rdMolDescriptors.CalcNumRotatableBonds(mol)
    if n_rotatable < 10:
        return False, "Chains too short to be fatty acids"

    # Check molecular weight - cardiolipins typically >700 Da
    mol_wt = rdMolDescriptors.CalcExactMolWt(mol)
    if mol_wt < 700:
        return False, "Molecular weight too low for cardiolipin"

    # Count carbons and oxygens
    c_count = sum(1 for atom in mol.GetAtoms() if atom.GetAtomicNum() == 6)
    o_count = sum(1 for atom in mol.GetAtoms() if atom.GetAtomicNum() == 8)
    
    if c_count < 30:
        return False, "Too few carbons for cardiolipin"
    if o_count < 8:
        return False, "Too few oxygens for cardiolipin"

    return True, "Contains glycerol backbone with two phosphatidic acid groups attached via phosphate linkages"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:28494',
                          'name': 'cardiolipin',
                          'definition': 'A phosphatidylglycerol composed of '
                                        'two molecules of phosphatidic acid '
                                        'covalently linked to a molecule of '
                                        'glycerol.',
                          'parents': ['CHEBI:166988', 'CHEBI:17517'],
                          'xrefs': [   'DrugBank:DB03429',
                                       'KEGG:C05980',
                                       'LIPID_MAPS_instance:LMGP12010000',
                                       'PDBeChem:CDN',
                                       'PMID:10540156',
                                       'PMID:11339809',
                                       'PMID:16341241',
                                       'PMID:1694860',
                                       'PMID:17294083',
                                       'PMID:18515061',
                                       'PMID:18790112',
                                       'PMID:19303420',
                                       'PMID:19962311',
                                       'PMID:22819940',
                                       'PMID:2413066',
                                       'PMID:28458255',
                                       'PMID:3196084',
                                       'Wikipedia:Cardiolipin'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': None,
    'message': '\n'
               'Attempt failed: F1 score of 0 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: NONE\n'
               'False positives: NONE\n'
               'False negatives: SMILES: '
               'CCCCC\\C=C/C\\C=C/CCCCCCCC(=O)OC[C@H](COP(O)(=O)OCC(O)COP(O)(=O)OC[C@@H](COC(=O)CCCCCCC\\C=C/C\\C=C/CCCCC)OC(=O)CCCCCCC\\C=C/C\\C=C/CCCCC)OC(=O)CCCCCCC\\C=C/C\\C=C/CCCCC '
               'NAME: tetralinoleoyl cardiolipin REASON: MISSED Found 6 '
               'phosphate groups, need exactly 2\n'
               ' * SMILES: '
               'P(OC[C@H](OC(=O)CCCCCCCCCCCCCCC)COC(=O)CCCCCCC/C=C\\CCCCCCCC)(OC[C@H](O)COP(OC[C@H](OC(=O)CCCCCCC/C=C\\C/C=C\\CCCCC)COC(=O)CCCCCCC/C=C\\C/C=C\\CCCCC)(O)=O)(O)=O '
               "NAME: CL(1'-[18:2(9Z,12Z)/18:2(9Z,12Z)],3'-[18:1(9Z)/16:0]) "
               'REASON: MISSED Found 6 phosphate groups, need exactly 2\n'
               ' * SMILES: '
               'P(OC[C@H](OC(=O)CCCCCCCCCCCCCCCCC)COC(=O)CCCCCCC/C=C\\C/C=C\\CCCCC)(OC[C@@H](O)COP(OC[C@H](OC(=O)CCCCCCCCCCCCCCC)COC(=O)CCCCCCC/C=C\\CCCCCCCC)(O)=O)(O)=O '
               "NAME: CL(1'-[18:2(9Z,12Z)/18:0],3'-[18:1(9Z)/16:0]) REASON: "
               'MISSED Found 6 phosphate groups, need exactly 2\n'
               ' * SMILES: '
               'P(OC[C@H](OC(=O)CCCCCCCCCCCCCCC)COC(=O)CCCCCCC/C=C\\C/C=C\\CCCCC)(OC[C@@H](O)COP(OC[C@H](OC(=O)CCCCCCC/C=C\\CCCCCCCC)COC(=O)CCCCCCC/C=C\\C/C=C\\CCCCC)(O)=O)(O)=O '
               "NAME: CL(1'-[18:2(9Z,12Z)/16:0],3'-[18:2(9Z,12Z)/18:1(9Z)]) "
               'REASON: MISSED Found 6 phosphate groups, need exactly 2\n'
               ' * SMILES: '
               'P(=O)(OC[C@@](COP(=O)(O)OC[C@@](COC(=O)CCCCCCCCCCCCCCC)(OC(=O)CCCCCCCCC/C=C\\CCCCCC)[H])([H])O)(O)OC[C@@](COC(=O)CCCCCCCCCCCCCCC)(OC(=O)CCCCCCCCC/C=C\\CCCCCC)[H] '
               'NAME: '
               "1',3'-bis-[1-hexadecanoyl-2-(11Z-octadecenoyl)-sn-glycero-3-phospho]-sn-glycerol "
               'REASON: MISSED Found 6 phosphate groups, need exactly 2\n'
               ' * SMILES: '
               'P(OC[C@H](OC(=O)CCCCCCCCCCCCCCC)COC(=O)CCCCCCCCCCCCCCC)(OC[C@H](O)COP(OC[C@H](OC(=O)CCCCCCC/C=C\\C/C=C\\CCCCC)COC(=O)CCCCCCCCCCCCCCC)(O)=O)(O)=O '
               "NAME: CL(1'-[16:0/18:2(9Z,12Z)],3'-[16:0/16:0]) REASON: MISSED "
               'Found 6 phosphate groups, need exactly 2\n'
               ' * SMILES: '
               'O(P(OCC(COP(OC[C@@H](COC(CCCCCCCC=CCCCCCC)=O)OC(CCCCCCCC=CCCCCCC)=O)(O)=O)O)(O)=O)C[C@@H](COC(CCCCCCCC=CCCCCCC)=O)OC(CCCCCCCC=CCCCCCC)=O '
               'NAME: tetrahexadec-9-enoyl cardiolipin REASON: MISSED Found 6 '
               'phosphate groups, need exactly 2\n'
               ' * SMILES: '
               'P(OC[C@H](OC(=O)CCCCCCCCCCCCCCCCC)COC(=O)CCCCCCC/C=C\\C/C=C\\CCCCC)(OC[C@H](O)COP(OC[C@H](OC(=O)CCC/C=C\\C/C=C\\C/C=C\\C/C=C\\CCCCC)COC(=O)CCCCCCC/C=C\\CCCCCCCC)(O)=O)(O)=O '
               'NAME: '
               "CL(1'-[18:1(9Z)/20:4(5Z,8Z,11Z,14Z)],3'-[18:2(9Z,12Z)/18:0]) "
               'REASON: MISSED Found 6 phosphate groups, need exactly 2\n'
               ' * SMILES: '
               'P(OC[C@H](OC(=O)CCCCCCCCCCCCCCCCC)COC(=O)CCCCCCCCCCCCCCCCC)(OC[C@@H](O)COP(OC[C@H](OC(=O)CCCCCCCCC/C=C\\CCCCCC)COC(=O)CCCCCCCCCCCCCCC)(O)=O)(O)=O '
               'NAME: CL(16:0/18:1(11Z)/18:0/18:0) REASON: MISSED Found 6 '
               'phosphate groups, need exactly 2\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCC(=O)OC[C@H](COP(O)(=O)OC[C@H](O)COP(O)(=O)OC[C@@H](COC(=O)CCCCCCCCCCCN)OC(=O)CCCCCCCCCCCCCCC)OC(=O)CCCCCCCCCCCCCCC '
               'NAME: 12-aminolauroyl tripalmitoyl cardiolipin REASON: MISSED '
               'Found 6 phosphate groups, need exactly 2\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
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
                                               'exactly 4'},
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
                                     'reason': 'Found 2 ester groups, need '
                                               'exactly 4'}],
    'sample_false_negatives': [],
    'attempt': 1,
    'reasoning': 'The previous program failed because it incorrectly '
                 'identified the number of phosphate groups in cardiolipin '
                 'molecules. The error message indicates that the program '
                 'expected exactly 2 phosphate groups, but the actual '
                 'cardiolipin structures contain more. This suggests that the '
                 'phosphate group pattern matching was too restrictive.\n'
                 '\n'
                 '### Analysis of the Problem:\n'
                 '1. **Phosphate Group Counting**: The program used a pattern '
                 '`[PX4](=[OX1])([OX2])[OX2]` to match phosphate groups, but '
                 'this pattern may not capture all variations of phosphate '
                 'groups in cardiolipin structures. Cardiolipins typically '
                 'have two phosphatidic acid groups, each contributing a '
                 'phosphate group, but the way these groups are connected can '
                 'lead to more complex patterns.\n'
                 '\n'
                 '2. **Structural Complexity**: Cardiolipins are complex '
                 'molecules with multiple ester and phosphate linkages. The '
                 'previous program may have missed some of these linkages due '
                 'to the rigid pattern matching.\n'
                 '\n'
                 '### Proposed Solution:\n'
                 '1. **Relax Phosphate Group Matching**: Instead of strictly '
                 'counting phosphate groups, we should focus on identifying '
                 'the presence of phosphatidic acid groups, which are the key '
                 'components of cardiolipins.\n'
                 '\n'
                 '2. **Use Substructures**: We can use substructure matching '
                 'to identify the presence of two phosphatidic acid groups '
                 'attached to a glycerol backbone.\n'
                 '\n'
                 '3. **Adjust Oxygen Counting**: The number of oxygen atoms '
                 'should be adjusted to account for the additional oxygens in '
                 'the phosphate linkages.\n'
                 '\n'
                 'Here is the revised code:',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 25,
    'num_false_positives': 0,
    'num_true_negatives': 142275,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 1.0,
    'recall': 1.0,
    'f1': 1.0,
    'accuracy': 1.0,
    'negative_predictive_value': 1.0}