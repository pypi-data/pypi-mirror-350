"""
Classifies: CHEBI:18303 phosphatidyl-L-serine
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_phosphatidyl_L_serine(smiles: str):
    """
    Determines if a molecule is a phosphatidyl-L-serine based on its SMILES string.
    A phosphatidyl-L-serine has a glycerol backbone, a phosphate group, two fatty acid chains, and an L-serine residue.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a phosphatidyl-L-serine, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for glycerol backbone linked to phosphate
    glycerol_phosphate_pattern = Chem.MolFromSmarts("[CH2X4]-[CHX4]-[CH2X4]-[OX2]-[PX4](=[OX1])")
    if not mol.HasSubstructMatch(glycerol_phosphate_pattern):
        return False, "No glycerol backbone with phosphate group found"
    
    # Check for the specific serine linkage pattern to the phosphate group, allowing for ionic forms.
    serine_phosphate_pattern = Chem.MolFromSmarts("[P]-[O]-[CH2X4]-[CHX4]([NX3])-[CX3](=[OX1])-[OX2]")
    serine_phosphate_pattern_ionic = Chem.MolFromSmarts("[P]([O-])-[O]-[CH2X4]-[CHX4]([NX3])-[CX3](=[OX1])-[OX2]")
    if not (mol.HasSubstructMatch(serine_phosphate_pattern) or mol.HasSubstructMatch(serine_phosphate_pattern_ionic)):
        return False, "No serine phosphate linkage found"
   

    # Check for two ester groups attached to glycerol at the correct position.
    # Updated patterns to explicitly require connection to the glycerol carbons.
    ester1_pattern = Chem.MolFromSmarts("[CH2X4]-[CHX4](-[OX2]-[CX3](=[OX1]))-[CH2X4]")  
    ester2_pattern = Chem.MolFromSmarts("[CH2X4](-[OX2]-[CX3](=[OX1]))-[CHX4]-[CH2X4]")
    ester_matches1 = mol.GetSubstructMatches(ester1_pattern)
    ester_matches2 = mol.GetSubstructMatches(ester2_pattern)
    
    if len(ester_matches1) + len(ester_matches2) != 2:
       return False, f"Found {len(ester_matches1) + len(ester_matches2)} esters attached to the glycerol, need exactly 2"

    # Check for fatty acid chains (long carbon chains attached to esters)
    fatty_acid_pattern = Chem.MolFromSmarts("[CX4,CX3]~[CX4,CX3]~[CX4,CX3]~[CX4,CX3]")
    fatty_acid_matches = mol.GetSubstructMatches(fatty_acid_pattern)
    if len(fatty_acid_matches) < 2:
        return False, f"Missing fatty acid chains, got {len(fatty_acid_matches)}"
    
    # check the length of the fatty acid chains
    n_rotatable = rdMolDescriptors.CalcNumRotatableBonds(mol)
    if n_rotatable < 8:
        return False, "Chains too short to be fatty acids"


    # Count carbons, oxygens, nitrogen and phosphorus
    c_count = sum(1 for atom in mol.GetAtoms() if atom.GetAtomicNum() == 6)
    o_count = sum(1 for atom in mol.GetAtoms() if atom.GetAtomicNum() == 8)
    p_count = sum(1 for atom in mol.GetAtoms() if atom.GetAtomicNum() == 15)
    n_count = sum(1 for atom in mol.GetAtoms() if atom.GetAtomicNum() == 7)


    if c_count < 10:
       return False, "Too few carbons"
    if o_count < 7:
       return False, "Too few oxygens"
    if p_count != 1:
       return False, "Must have exactly 1 phosphorus"
    if n_count != 1:
       return False, "Must have exactly 1 nitrogen"

    return True, "Contains glycerol backbone with phosphate group, serine residue, and 2 fatty acids"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:18303',
                          'name': 'phosphatidyl-L-serine',
                          'definition': 'A class of aminophospholipids in '
                                        'which a phosphatidyl group is '
                                        'esterified to the hydroxy group of '
                                        'serine.',
                          'parents': [   'CHEBI:52565',
                                         'CHEBI:60971',
                                         'CHEBI:84135'],
                          'xrefs': [   'DrugBank:DB00144',
                                       'HMDB:HMDB0014291',
                                       'KEGG:C02737',
                                       'MetaCyc:L-1-PHOSPHATIDYL-SERINE',
                                       'PMID:10540156',
                                       'PMID:15533308',
                                       'PMID:19687511',
                                       'PMID:23543734',
                                       'PMID:3106116',
                                       'PMID:3196084',
                                       'PMID:4153523',
                                       'PMID:8204602',
                                       'PMID:8626656',
                                       'PMID:9677350',
                                       'Patent:EP2322184',
                                       'Patent:HK1046237',
                                       'Patent:US2011098249',
                                       'Wikipedia:Phosphatidylserine'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 52,
                           'log_lines_of_code': 3.9512437185814275,
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
                                                 2,
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
                                                 1,
                                                 0,
                                                 1,
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
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 0,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 0,
                                                 1],
                           'max_indent': 2,
                           'imports': [   'from rdkit import Chem',
                                          'from rdkit.Chem import AllChem',
                                          'from rdkit.Chem import '
                                          'rdMolDescriptors'],
                           'imports_count': 3,
                           'methods_called': [   'GetSubstructMatches',
                                                 'MolFromSmarts',
                                                 'GetAtomicNum',
                                                 'GetAtoms',
                                                 'HasSubstructMatch',
                                                 'MolFromSmiles',
                                                 'CalcNumRotatableBonds'],
                           'methods_called_count': 7,
                           'smarts_strings': [   '[CX4,CX3]~[CX4,CX3]~[CX4,CX3]~[CX4,CX3]',
                                                 '[CH2X4]-[CHX4]-[CH2X4]-[OX2]-[PX4](=[OX1])',
                                                 '[P]-[O]-[CH2X4]-[CHX4]([NX3])-[CX3](=[OX1])-[OX2]',
                                                 '[CH2X4](-[OX2]-[CX3](=[OX1]))-[CHX4]-[CH2X4]',
                                                 '[CH2X4]-[CHX4](-[OX2]-[CX3](=[OX1]))-[CH2X4]',
                                                 '[P]([O-])-[O]-[CH2X4]-[CHX4]([NX3])-[CX3](=[OX1])-[OX2]'],
                           'smarts_strings_count': 6,
                           'defs': ['is_phosphatidyl_L_serine(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "No glycerol backbone with '
                                          'phosphate group found"',
                                          'False, "No serine phosphate linkage '
                                          'found"',
                                          'False, f"Found {len(ester_matches1) '
                                          '+ len(ester_matches2)} esters '
                                          'attached to the glycerol, need '
                                          'exactly 2"',
                                          'False, f"Missing fatty acid chains, '
                                          'got {len(fatty_acid_matches)}"',
                                          'False, "Chains too short to be '
                                          'fatty acids"',
                                          'False, "Too few carbons"',
                                          'False, "Too few oxygens"',
                                          'False, "Must have exactly 1 '
                                          'phosphorus"',
                                          'False, "Must have exactly 1 '
                                          'nitrogen"',
                                          'True, "Contains glycerol backbone '
                                          'with phosphate group, serine '
                                          'residue, and 2 fatty acids"'],
                           'returns_count': 11,
                           'complexity': 4.990248743716285},
    'message': '\n'
               'Attempt failed: F1 score of 0 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: NONE\n'
               'False positives: NONE\n'
               'False negatives: SMILES: '
               'P(OC[C@H](OC(=O)CCCCCCC/C=C\\CCCCCCC)COC(=O)CCCCCCCCC/C=C\\CCCCCCCC)(OC[C@H](N)C(O)=O)(O)=O '
               'NAME: PS(37:2) REASON: MISSED Found 0 esters attached to the '
               'glycerol, need exactly 2\n'
               ' * SMILES: '
               'P(OC[C@H](OC(=O)CCCCCCC/C=C\\CCCCCCCCC)COC(=O)CCCCCCC/C=C\\CCCCC)(OC[C@H](N)C(O)=O)(O)=O '
               'NAME: PS(15:1(9Z)/19:1(9Z)) REASON: MISSED Found 0 esters '
               'attached to the glycerol, need exactly 2\n'
               ' * SMILES: '
               'P(OC[C@H](OC(=O)CCCCCCC/C=C\\C/C=C\\CCCCC)COC(=O)CCCCCCCCCCCC)(OC[C@H](N)C(O)=O)(O)=O '
               'NAME: PS(13:0/18:2(9Z,12Z)) REASON: MISSED Found 0 esters '
               'attached to the glycerol, need exactly 2\n'
               ' * SMILES: '
               'P(OCC(OC(=O)CCCCCCCCCCC=1OC(CCCCC)=CC1C)COC(=O)CCCCCCCCCCC=2OC(=C(C2C)C)CCCCC)(OCC(N)C(O)=O)(O)=O '
               'NAME: PS(DiMe(11,5)/MonoMe(11,5)) REASON: MISSED Found 0 '
               'esters attached to the glycerol, need exactly 2\n'
               ' * SMILES: '
               'P(OC[C@H](OC(=O)CCCCCCCCCCCCC/C=C\\CCCCCCCC)COC(=O)CCCCCCCCCCCCCCCCCCCCC)(OC[C@H](N)C(O)=O)(O)=O '
               'NAME: '
               '(2S)-2-amino-3-({[(2R)-3-(docosanoyloxy)-2-[(15Z)-tetracos-15-enoyloxy]propoxy](hydroxy)phosphoryl}oxy)propanoic '
               'acid REASON: MISSED Found 0 esters attached to the glycerol, '
               'need exactly 2\n'
               ' * SMILES: '
               'P(OC[C@H](OC(=O)CCCCCCCCCCC/C=C\\CCCCCCCC)COC(=O)CCCCCCCCCCCCCC)(OC[C@H](N)C(O)=O)(O)=O '
               'NAME: PS(15:0/22:1(13Z)) REASON: MISSED Found 0 esters '
               'attached to the glycerol, need exactly 2\n'
               ' * SMILES: '
               'P(OC[C@H](OC(=O)CCCCCCC/C=C\\C/C=C\\CCCCC)COC(=O)CCCCCCCCCCCCCCCCCCCCCCC)(OC[C@H]([NH3+])C([O-])=O)([O-])=O '
               'NAME: 24:0-18:2-PS REASON: MISSED No serine phosphate linkage '
               'found\n'
               ' * SMILES: '
               'O(C[C@H](COP(=O)(OC[C@@H](C(O)=O)N)O)OC(CCCCCCC/C=C/CCCCCCCC)=O)C(CCCCCCC/C=C/CCCCCCCC)=O '
               'NAME: 1,2-di-(9E-octadecenoyl)-sn-glycero-3-phosphoserine '
               'REASON: MISSED Found 0 esters attached to the glycerol, need '
               'exactly 2\n'
               ' * SMILES: '
               'P(OC[C@H](OC(=O)CCCCC)COC(=O)CCCCC)(OC[C@H](N)C(O)=O)(O)=O '
               'NAME: PS(6:0/6:0) REASON: MISSED Found 0 esters attached to '
               'the glycerol, need exactly 2\n'
               ' * SMILES: '
               'P(OC[C@H](OC(=O)CCCCCCCCCCCCCCCCCCC)COC(=O)CCC/C=C\\C/C=C\\C/C=C\\C/C=C\\CCCCC)(OC[C@H](N)C(O)=O)(O)=O '
               'NAME: PS(20:4(5Z,8Z,11Z,14Z)/20:0) REASON: MISSED Found 0 '
               'esters attached to the glycerol, need exactly 2\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'CCN1N=C(N=N1)C2=CC=CC=C2NC(=O)C3=CC=C(C=C3)N4C=NN=N4',
                                     'name': 'N-[2-(2-ethyl-5-tetrazolyl)phenyl]-4-(1-tetrazolyl)benzamide',
                                     'reason': 'No glycerol backbone with '
                                               'phosphate group found'},
                                 {   'smiles': 'CCS(=O)(=O)N1CC2(C1)[C@@H]([C@@H](N2C(=O)C3CCCC3)CO)C4=CC=C(C=C4)C=CC',
                                     'name': 'LSM-38092',
                                     'reason': 'No glycerol backbone with '
                                               'phosphate group found'},
                                 {   'smiles': 'O=C/1N/C(/C(=O)N\\C1=C\\C2=CC=CC=C2)=C\\C=3N=CNC3C(C=C)(C)C',
                                     'name': 'DeltaPLH',
                                     'reason': 'No glycerol backbone with '
                                               'phosphate group found'},
                                 {   'smiles': 'C1CCN(CC1)C(=O)C[C@H]2C[C@@H]3[C@H]([C@@H](O2)CO)OC4=C3C=C(C=C4)NC(=O)CC5CC5',
                                     'name': 'N-[(1S,3R,4aS,9aR)-1-(hydroxymethyl)-3-[2-oxo-2-(1-piperidinyl)ethyl]-3,4,4a,9a-tetrahydro-1H-pyrano[3,4-b]benzofuran-6-yl]-2-cyclopropylacetamide',
                                     'reason': 'No glycerol backbone with '
                                               'phosphate group found'},
                                 {   'smiles': 'C[C@H]1C[C@@]2(OC(=O)c3ccccc3)[C@H]([C@H]1OC(C)=O)[C@@H](O)\\C(C)=C/C[C@H]1[C@@H](\\C=C(C)\\C2=O)C1(C)C',
                                     'name': '(-)-(6Z,12E,2S,3S,4R,5R,9S,11S,15R)-3-acetoxy-15-benzoyloxylathyra-6,12-dien-5-ol-14-one',
                                     'reason': 'No glycerol backbone with '
                                               'phosphate group found'},
                                 {   'smiles': 'O=C1C(O)=CC=2O[C@]3([C@H](O)C[C@@H]4[C@](OC=5C=C(O)C(C=C(C5C4)C)=O)(CC=CC(C[C@H]3CC2C(=C1)C)(C)C)C)C',
                                     'name': 'Eupenifeldin',
                                     'reason': 'No glycerol backbone with '
                                               'phosphate group found'},
                                 {   'smiles': 'O1[C@@H](O[C@@H]2[C@@H](OC[C@H]3O[C@@H](O[C@H]4[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]4CO)O[C@H]5[C@H](O)[C@@H](NC(=O)C)C(O[C@@H]5CO[C@@H]6O[C@H]([C@@H](O)[C@@H](O)[C@@H]6O)C)O)[C@@H](O)[C@@H](O[C@H]7O[C@@H]([C@@H](O)[C@H](O)[C@@H]7O[C@@H]8O[C@@H]([C@@H](O[C@@H]9O[C@@H]([C@H](O)[C@H](O)[C@H]9NC(=O)C)CO)[C@H](O)[C@H]8NC(=O)C)CO)CO)[C@@H]3O)O[C@@H]([C@@H](O)[C@@H]2O)CO)[C@H](NC(=O)C)[C@@H](O[C@@H]%10O[C@H]([C@@H](O)[C@@H](O)[C@@H]%10O)C)[C@H](O[C@@H]%11O[C@@H]([C@H](O)[C@H](O)[C@H]%11NC(=O)C)CO)[C@H]1CO',
                                     'name': 'N-[(3R,4R,5S,6R)-5-[(2S,3R,4R,5S,6R)-3-Acetamido-5-[(2S,3S,4S,5R,6R)-4-[(2R,3S,4S,5S,6R)-3-[(2S,3R,4R,5S,6R)-3-acetamido-5-[(2S,3R,4R,5R,6R)-3-acetamido-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-6-[[(2S,3S,4S,5S,6R)-3-[(2S,3R,4R,5S,6R)-3-acetamido-5-[(2S,3R,4R,5R,6R)-3-acetamido-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-6-(hydroxymethyl)-4-[(2R,3S,4R,5S,6S)-3,4,5-trihydroxy-6-methyloxan-2-yl]oxyoxan-2-yl]oxy-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxymethyl]-3,5-dihydroxyoxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-2,4-dihydroxy-6-[[(2R,3S,4R,5S,6S)-3,4,5-trihydroxy-6-methyloxan-2-yl]oxymethyl]oxan-3-yl]acetamide',
                                     'reason': 'No glycerol backbone with '
                                               'phosphate group found'},
                                 {   'smiles': 'CN1C[C@@H]2C[C@H](Cn3c2cccc3=O)[C@H]1CC=C',
                                     'name': 'Tinctorine',
                                     'reason': 'No glycerol backbone with '
                                               'phosphate group found'},
                                 {   'smiles': 'CCC1=C2COC(CC2=C3C(=C(OC3=N1)C(=O)C4=CC=CC=C4)N)(C)C',
                                     'name': 'LSM-4563',
                                     'reason': 'No glycerol backbone with '
                                               'phosphate group found'},
                                 {   'smiles': 'CN1CCN(CC1)C(=O)C[C@@H]2CC[C@H]3[C@H](O2)COC[C@@H](CN3C(=O)NC4=CC5=C(C=C4)OCO5)O',
                                     'name': '(3R,6aS,8S,10aS)-N-(1,3-benzodioxol-5-yl)-3-hydroxy-8-[2-(4-methyl-1-piperazinyl)-2-oxoethyl]-3,4,6,6a,8,9,10,10a-octahydro-2H-pyrano[2,3-c][1,5]oxazocine-1-carboxamide',
                                     'reason': 'No glycerol backbone with '
                                               'phosphate group found'}],
    'sample_false_negatives': [   {   'smiles': 'P(OC[C@H](OC(=O)CCCCCCC/C=C\\C/C=C\\CCCCC)COC(=O)CCCCCCCCCCCCCCCCCCCCCCC)(OC[C@H]([NH3+])C([O-])=O)([O-])=O',
                                      'name': '24:0-18:2-PS',
                                      'reason': 'No serine phosphate linkage '
                                                'found'},
                                  {   'smiles': 'P(OC[C@H](OC(=O)CCCCCCC/C=C\\C/C=C\\C/C=C\\CC)COC(=O)CCCCCCCCCCCCCCCCCCCCC)(OC[C@H]([NH3+])C([O-])=O)([O-])=O',
                                      'name': '22:0-18:3-PS',
                                      'reason': 'No serine phosphate linkage '
                                                'found'},
                                  {   'smiles': 'P(OC[C@H](OC(=O)CCCCCCC/C=C\\C/C=C\\C/C=C\\CC)COC(=O)CCCCCCCCCCC/C=C\\CCCCCCCC)(OC[C@H]([NH3+])C([O-])=O)([O-])=O',
                                      'name': '22:1-18:3-PS',
                                      'reason': 'No serine phosphate linkage '
                                                'found'},
                                  {   'smiles': 'P(OC[C@H](OC(=O)CCCCCCC/C=C\\CCCCCCCC)COC(=O)CCCCCCCCCCCCCCCCCCCCC)(OC[C@H]([NH3+])C([O-])=O)([O-])=O',
                                      'name': '22:0-18:1-PS',
                                      'reason': 'No serine phosphate linkage '
                                                'found'},
                                  {   'smiles': 'P(OC[C@H](OC(=O)CCCCCCC/C=C\\CCCCCCCC)COC(=O)CCCCCCCCCCCCCCCCCCC)(OC[C@H]([NH3+])C([O-])=O)([O-])=O',
                                      'name': '20:0-18:1-PS',
                                      'reason': 'No serine phosphate linkage '
                                                'found'},
                                  {   'smiles': 'P(OC[C@H](OC(=O)CCC)COC(=O)CC)(OC[C@@H](N)C(O)=O)(O)=O',
                                      'name': '1,2-Distearoyl phosphatidyl '
                                              'serine',
                                      'reason': 'Missing fatty acid chains, '
                                                'got 1'},
                                  {   'smiles': 'P(OC[C@H](OC(=O)CCCCCCC/C=C\\C/C=C\\CCCCC)COC(=O)CCCCCCCCCCCCCCCCCCC)(OC[C@H]([NH3+])C([O-])=O)([O-])=O',
                                      'name': '20:0-18:2-PS',
                                      'reason': 'No serine phosphate linkage '
                                                'found'},
                                  {   'smiles': 'P(OC[C@H](OC(=O)CCCCCCC/C=C\\C/C=C\\C/C=C\\CC)COC(=O)CCCCCCCCCCCCCCCCCCC)(OC[C@H]([NH3+])C([O-])=O)([O-])=O',
                                      'name': '20:0-18:3-PS',
                                      'reason': 'No serine phosphate linkage '
                                                'found'},
                                  {   'smiles': 'P(OC[C@H](OC(=O)CCCCCCC/C=C\\C/C=C\\C/C=C\\CC)COC(=O)CCCCCCCCC/C=C\\CCCCCCCC)(OC[C@H]([NH3+])C([O-])=O)([O-])=O',
                                      'name': '20:1-18:3-PS',
                                      'reason': 'No serine phosphate linkage '
                                                'found'},
                                  {   'smiles': 'P(OC1C(O)C(O)C(O)[C@@H](O)C1O)(OC[C@H](OC(=O)CCC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)COC(=O)CCCCCCC/C=C\\C/C=C\\CCCC)(O)=O',
                                      'name': 'PI(17:2(9Z,12Z)/20:5(5Z,8Z,11Z,14Z,17Z))',
                                      'reason': 'No serine phosphate linkage '
                                                'found'}],
    'attempt': 3,
    'reasoning': "Okay, let's analyze the previous attempt and the error "
                 'messages.\n'
                 '\n'
                 '**Problem Analysis:**\n'
                 '\n'
                 'The primary issue seems to stem from the way ester groups '
                 'attached to the glycerol backbone are being identified. The '
                 'previous code attempts to filter ester matches based on the '
                 'glycerol atoms, however, the logic is flawed. Specifically, '
                 'the code tries to iterate through each atom of the glycerol '
                 'substructure match and then their neighbors, but this '
                 'approach does not correctly filter ester oxygens that form '
                 "the connection with the glycerol's carbon atoms. This "
                 'results in counting zero esters in several cases, which is '
                 'incorrect as every given example has two ester bonds.\n'
                 '\n'
                 'Additionally, the code for the serine phosphate linkage '
                 'check appears correct, but the 24:0-18:2-PS example shows '
                 "that ionic forms can also occur, so it's necessary to "
                 'account for both protonated and deprotonated forms.\n'
                 '\n'
                 '**Proposed Improvements:**\n'
                 '\n'
                 '1.  **Refine Ester Detection:** Instead of iterating through '
                 'neighbors, we should construct SMARTS patterns that '
                 'explicitly define the ester linkage to the glycerol. This '
                 'requires more precise SMARTS patterns.\n'
                 '2.  **Handle Ionic forms of phosphate and serine:** Instead '
                 'of relying on specific protonated forms, use more '
                 'generalized patterns that accept different charge states of '
                 'the phosphate and serine group.\n'
                 '3.  **Check fatty acid lengths:** The previous code just '
                 'checked for "long" carbon chains, which isn\'t a good '
                 'measure of fatty acid presence, instead, we can use the '
                 'number of carbons or rotatable bonds again to check this.\n'
                 '\n'
                 "Let's implement these changes in the code.",
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 303,
    'num_false_positives': 9,
    'num_true_negatives': 141973,
    'num_false_negatives': 15,
    'num_negatives': None,
    'precision': 0.9711538461538461,
    'recall': 0.9528301886792453,
    'f1': 0.9619047619047619,
    'accuracy': 0.9998313422347154,
    'negative_predictive_value': 0.9998943572696284}