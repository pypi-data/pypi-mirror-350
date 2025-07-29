"""
Classifies: CHEBI:23899 icosanoid
"""
"""
Classifies: CHEBI:36080 icosanoid
"""
from rdkit import Chem
from rdkit.Chem import rdMolDescriptors

def is_icosanoid(smiles: str):
    """
    Determines if a molecule is an icosanoid based on its SMILES string.
    An icosanoid is a signaling molecule derived from the oxidation of C20 essential fatty acids.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is an icosanoid, False otherwise
        str: Reason for classification
    """
    
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for core icosanoid structure (relaxed carbon count)
    c_count = sum(1 for atom in mol.GetAtoms() if atom.GetAtomicNum() == 6)
    if c_count < 16:
        return False, f"Expected at least 16 carbons, found {c_count}"

    # Check for multiple double bonds (relaxed requirement)
    double_bonds = sum(1 for bond in mol.GetBonds() if bond.GetBondType() == Chem.BondType.DOUBLE)
    if double_bonds < 1:
        return False, f"Expected at least 1 double bond, found {double_bonds}"

    # Check for oxygen-containing functional groups (at least 2)
    oxygen_atoms = sum(1 for atom in mol.GetAtoms() if atom.GetAtomicNum() == 8)
    if oxygen_atoms < 2:
        return False, f"Expected at least 2 oxygen atoms, found {oxygen_atoms}"

    # More flexible patterns for characteristic icosanoid structures
    # 1. Cyclopentane ring with oxygen-containing groups (prostaglandin-like)
    prostaglandin_pattern = Chem.MolFromSmarts("[C]1[C][C][C][C]1([C]=O)([OH])")
    # 2. Conjugated polyene system (leukotriene-like)
    leukotriene_pattern = Chem.MolFromSmarts("[C]=[C][C]=[C][C]=[C]")
    # 3. Epoxide structure (common in EETs)
    epoxide_pattern = Chem.MolFromSmarts("[OX2]1[CX4][CX4]1")
    # 4. Hydroperoxide structure (common in HPETEs)
    hydroperoxide_pattern = Chem.MolFromSmarts("[OH][OX2]")
    # 5. Carboxyl group (common in many icosanoids)
    carboxyl_pattern = Chem.MolFromSmarts("[CX3](=O)[OX2H1]")

    has_prostaglandin = mol.HasSubstructMatch(prostaglandin_pattern)
    has_leukotriene = mol.HasSubstructMatch(leukotriene_pattern)
    has_epoxide = mol.HasSubstructMatch(epoxide_pattern)
    has_hydroperoxide = mol.HasSubstructMatch(hydroperoxide_pattern)
    has_carboxyl = mol.HasSubstructMatch(carboxyl_pattern)

    if not (has_prostaglandin or has_leukotriene or has_epoxide or has_hydroperoxide or has_carboxyl):
        return False, "No characteristic icosanoid structural patterns found"

    # Check for specific functional groups (hydroxyl, carboxyl, epoxide, peroxide, ester, ether)
    hydroxyl_pattern = Chem.MolFromSmarts("[OX2H]")
    ester_pattern = Chem.MolFromSmarts("[CX3](=O)[OX2H0]")
    ether_pattern = Chem.MolFromSmarts("[CX4][OX2][CX4]")

    has_hydroxyl = mol.HasSubstructMatch(hydroxyl_pattern)
    has_ester = mol.HasSubstructMatch(ester_pattern)
    has_ether = mol.HasSubstructMatch(ether_pattern)

    if not (has_hydroxyl or has_carboxyl or has_ester or has_ether):
        return False, "No hydroxyl, carboxyl, ester, or ether groups found"

    return True, "Contains characteristic icosanoid structure with multiple double bonds and oxygen-containing functional groups"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:23899',
                          'name': 'icosanoid',
                          'definition': 'Any member of the group of signalling '
                                        'molecules arising from oxidation of '
                                        'the three C20 essential fatty acids '
                                        '(EFAs) icosapentaenoic acid (EPA), '
                                        'arachidonic acid (AA) and '
                                        'dihomo-gamma-linolenic acid (DGLA).',
                          'parents': ['CHEBI:61697'],
                          'xrefs': [   'LIPID_MAPS_class:LMFA03',
                                       'PMID:12697726',
                                       'PMID:16107763',
                                       'PMID:19160658',
                                       'PMID:2657063',
                                       'Wikipedia:Eicosanoid'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 53,
                           'log_lines_of_code': 3.970291913552122,
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
                                                 1,
                                                 1,
                                                 1,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 0,
                                                 1,
                                                 2,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 0,
                                                 1,
                                                 2,
                                                 0,
                                                 1],
                           'max_indent': 2,
                           'imports': [   'from rdkit import Chem',
                                          'from rdkit.Chem import '
                                          'rdMolDescriptors'],
                           'imports_count': 2,
                           'methods_called': [   'GetBonds',
                                                 'HasSubstructMatch',
                                                 'MolFromSmarts',
                                                 'MolFromSmiles',
                                                 'GetAtomicNum',
                                                 'GetAtoms',
                                                 'GetBondType'],
                           'methods_called_count': 7,
                           'smarts_strings': [   '[CX4][OX2][CX4]',
                                                 '[C]1[C][C][C][C]1([C]=O)([OH])',
                                                 '[OX2H]',
                                                 '[OX2]1[CX4][CX4]1',
                                                 '[C]=[C][C]=[C][C]=[C]',
                                                 '[OH][OX2]',
                                                 '[CX3](=O)[OX2H0]',
                                                 '[CX3](=O)[OX2H1]'],
                           'smarts_strings_count': 8,
                           'defs': ['is_icosanoid(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, f"Expected at least 16 '
                                          'carbons, found {c_count}"',
                                          'False, f"Expected at least 1 double '
                                          'bond, found {double_bonds}"',
                                          'False, f"Expected at least 2 oxygen '
                                          'atoms, found {oxygen_atoms}"',
                                          'False, "No characteristic icosanoid '
                                          'structural patterns found"',
                                          'False, "No hydroxyl, carboxyl, '
                                          'ester, or ether groups found"',
                                          'True, "Contains characteristic '
                                          'icosanoid structure with multiple '
                                          'double bonds and oxygen-containing '
                                          'functional groups"'],
                           'returns_count': 7,
                           'complexity': 4.194058382710424},
    'message': '\n'
               'Attempt failed: F1 score of 0.20634920634920637 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: '
               'CCCCCC1OC1C\\C=C/C\\C=C/C\\C=C/CCCC(O)=O NAME: 14,15-EET '
               'REASON: CORRECT Contains characteristic icosanoid structure '
               'with multiple double bonds and oxygen-containing functional '
               'groups\n'
               ' * SMILES: C(CCCO)CC1C(C/C=C\\C/C=C\\C/C=C\\CCCC(O)=O)O1 NAME: '
               '14,15-epoxy-20-hydroxy-(5Z,8Z,11Z)-icosatrienoic acid REASON: '
               'CORRECT Contains characteristic icosanoid structure with '
               'multiple double bonds and oxygen-containing functional groups\n'
               ' * SMILES: CCCCC[C@H](OO)\\C=C\\C=C/C\\C=C/C\\C=C/CCCC(O)=O '
               'NAME: 15(S)-HPETE REASON: CORRECT Contains characteristic '
               'icosanoid structure with multiple double bonds and '
               'oxygen-containing functional groups\n'
               ' * SMILES: O(O)C(C/C=C\\CC)/C=C/C=C\\C/C=C\\C/C=C\\CCCC(O)=O '
               'NAME: 15S-HpEPE REASON: CORRECT Contains characteristic '
               'icosanoid structure with multiple double bonds and '
               'oxygen-containing functional groups\n'
               ' * SMILES: CCCCC\\C=C/C[C@H](OO)\\C=C\\C=C/C\\C=C/CCCC(O)=O '
               'NAME: 12(S)-HPETE REASON: CORRECT Contains characteristic '
               'icosanoid structure with multiple double bonds and '
               'oxygen-containing functional groups\n'
               ' * SMILES: C(CCCO)C/C=C\\C/C=C\\C/C=C\\CC1C(CCCC(O)=O)O1 NAME: '
               '5,6-epoxy-20-hydroxy-(8Z,11Z,14Z)-icosatrienoic acid REASON: '
               'CORRECT Contains characteristic icosanoid structure with '
               'multiple double bonds and oxygen-containing functional groups\n'
               ' * SMILES: '
               'O1O[C@]2([C@@H]([C@@H]([C@@]1(C2)[H])CCC(O)=O)/C=C/[C@@H](OO)C/C=C\\C/C=C\\C/C=C\\CC)[H] '
               'NAME: 11-Hydroperoxy-H4-neuroprostane REASON: CORRECT Contains '
               'characteristic icosanoid structure with multiple double bonds '
               'and oxygen-containing functional groups\n'
               ' * SMILES: '
               'O(O)[C@@H](CCCC(O)=O)/C=C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC NAME: '
               '5S-HpEPE REASON: CORRECT Contains characteristic icosanoid '
               'structure with multiple double bonds and oxygen-containing '
               'functional groups\n'
               ' * SMILES: '
               'CC[C@H]1O[C@H]1C\\C=C/C\\C=C/C\\C=C/C\\C=C/CCCC(O)=O NAME: '
               '17(S),18(R)-EETeTr REASON: CORRECT Contains characteristic '
               'icosanoid structure with multiple double bonds and '
               'oxygen-containing functional groups\n'
               ' * SMILES: '
               'CC[C@@H]1O[C@@H]1C\\C=C/C\\C=C/C\\C=C/C\\C=C/CCCC(O)=O NAME: '
               '17(R),18(S)-EETeTr REASON: CORRECT Contains characteristic '
               'icosanoid structure with multiple double bonds and '
               'oxygen-containing functional groups\n'
               ' * SMILES: '
               'O[C@@H]1[C@@H]([C@H](C(=O)C1)/C=C/[C@@H](OO)CCCCC)C/C=C\\CCCC(O)=O '
               'NAME: 15S-hydroperoxy-PGD2 REASON: CORRECT Contains '
               'characteristic icosanoid structure with multiple double bonds '
               'and oxygen-containing functional groups\n'
               ' * SMILES: '
               'C(CCC)C/C=C\\C[C@@H]1[C@H](C/C=C\\C/C=C\\CCCC(O)=O)O1 NAME: '
               '(11S,12R)-EET REASON: CORRECT Contains characteristic '
               'icosanoid structure with multiple double bonds and '
               'oxygen-containing functional groups\n'
               ' * SMILES: '
               'O[C@H]1[C@@H]([C@H](C(=O)C1)C/C=C\\CCCC(O)=O)/C=C/[C@@H](OO)CCCCC '
               'NAME: 15S-hydroperoxy-PGE2 REASON: CORRECT Contains '
               'characteristic icosanoid structure with multiple double bonds '
               'and oxygen-containing functional groups\n'
               'False positives: NONE\n'
               'False negatives: SMILES: '
               'O=C1[C@@H]([C@H](CC1)/C=C/[C@@H](O)CCCCC)CCCCCCC(O)=O NAME: '
               '11-deoxyprostaglandin E1 REASON: MISSED No characteristic '
               'icosanoid structural patterns found\n'
               ' * SMILES: '
               'O[C@H]1[C@@H]([C@H](C(=O)C1)C/C=C\\CCCC(OC)=O)/C=C/[C@H](O)CCCCC '
               'NAME: 15R-PGE2 methyl ester REASON: MISSED No characteristic '
               'icosanoid structural patterns found\n'
               ' * SMILES: '
               'O(C(C[N+](C)(C)C)CC([O-])=O)C(=O)CCC\\C=C\\CC1/C(/C(=O)C=C1)=C/C=C/CCCCC '
               'NAME: '
               '(5Z)-7-[(1S,5E)-5-[(2E)-Oct-2-en-1-ylidene]-4-oxocyclopent-2-en-1-yl]hept-5-enoylcarnitine '
               'REASON: MISSED Expected 16-22 carbons, found 27\n'
               ' * SMILES: '
               'P(OC[C@H](OC(=O)C/C=C\\C[C@H]1[C@H]([C@H](O)C[C@@H]1O)/C=C/[C@H](O)CCCCC)COC(=O)CCCCCCCCCCCCC)(OC[C@H](N)C(O)=O)(O)=O '
               'NAME: PS(14:0/5-iso PGF2VI) REASON: MISSED Expected 16-22 '
               'carbons, found 38\n'
               ' * SMILES: '
               'CCCCC(C)(CC=C[C@H]1[C@@H](CC(=O)[C@@H]1CCCCCCC(=O)OC)O)O NAME: '
               '7-[(1R,2R,3R)-3-hydroxy-2-(4-hydroxy-4-methyloct-1-enyl)-5-oxocyclopentyl]heptanoic '
               'acid methyl ester REASON: MISSED No characteristic icosanoid '
               'structural patterns found\n'
               ' * SMILES: '
               'N[C@@H](CCC(=O)N[C@@H](CS[C@H]1[C@@H]([C@H](C(C1)=O)/C=C/[C@H](CCCCC)O)C/C=C\\CCCC(=O)O)C(=O)NCC(=O)O)C(=O)O '
               'NAME: (R)-PGJ2-S-glutathione conjugate REASON: MISSED Expected '
               '16-22 carbons, found 30\n'
               ' * SMILES: '
               'O[C@H]1[C@@H]([C@@H](CCCCC(O)=O)C(=O)C1)/C=C/[C@@H](O)CCCCC '
               'NAME: 2,3-Dinor-PGE1 REASON: MISSED No characteristic '
               'icosanoid structural patterns found\n'
               ' * SMILES: '
               'P(OC[C@H](OC(=O)CCCCCC[C@@H]1[C@H]([C@H](O)C[C@@H]1O)/C=C/[C@@H](O)CCCCC)COC(=O)CCCCCCCCCCCCCCCCCCCCCCC)(OC[C@H](N)C(O)=O)(O)=O '
               'NAME: PS(24:0/PGF1alpha) REASON: MISSED Expected 16-22 '
               'carbons, found 50\n'
               ' * SMILES: '
               'S([C@@H]([C@@H](O)CCCC(O)=O)/C=C/C=C/C=C\\C/C=C\\CCCCC)C[C@H](N)C(OC[C@@H](OC(=O)CCCCCCCCCCCCCCCCC(CC)C)COP(OC[C@@H](O)CO)(O)=O)=O '
               'NAME: PG(LTE4/a-21:0) REASON: MISSED Expected 16-22 carbons, '
               'found 50\n'
               ' * SMILES: '
               'C1[C@@H]([C@@H]([C@H]([C@@H]1O)C=C[C@H](COC2=CC(=CC=C2)Cl)O)CC=CCCCC(=O)O)O '
               'NAME: '
               '7-[(1R,2R,3R,5S)-2-[(3R)-4-(3-chlorophenoxy)-3-hydroxybut-1-enyl]-3,5-dihydroxycyclopentyl]-5-heptenoic '
               'acid REASON: MISSED No characteristic icosanoid structural '
               'patterns found\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [],
    'sample_false_negatives': [   {   'smiles': 'O[C@H]1[C@@H]([C@H](C(=O)C1)C/C=C\\CCCC(OC)=O)/C=C/[C@H](O)CCCCC',
                                      'name': '15R-PGE2 methyl ester',
                                      'reason': 'No characteristic icosanoid '
                                                'structural patterns found'},
                                  {   'smiles': 'O(C(C[N+](C)(C)C)CC([O-])=O)C(=O)CCC\\C=C\\CC1/C(/C(=O)C=C1)=C/C=C/CCCCC',
                                      'name': '(5Z)-7-[(1S,5E)-5-[(2E)-Oct-2-en-1-ylidene]-4-oxocyclopent-2-en-1-yl]hept-5-enoylcarnitine',
                                      'reason': 'No characteristic icosanoid '
                                                'structural patterns found'},
                                  {   'smiles': 'CCCCC(C)(CC=C[C@H]1[C@@H](CC(=O)[C@@H]1CCCCCCC(=O)OC)O)O',
                                      'name': '7-[(1R,2R,3R)-3-hydroxy-2-(4-hydroxy-4-methyloct-1-enyl)-5-oxocyclopentyl]heptanoic '
                                              'acid methyl ester',
                                      'reason': 'No characteristic icosanoid '
                                                'structural patterns found'},
                                  {   'smiles': 'P(OCC[N+](C)(C)C)(OC[C@H](OC(=O)CCC/C=C\\C[C@H]1[C@@H](O)CC(O[C@@H]1/C=C/[C@@H](O)CCCCC)O)COC(=O)CCCCCCCCCCCCCCCCCCCCCCC)([O-])=O',
                                      'name': 'PC(24:0/TXB2)',
                                      'reason': 'No characteristic icosanoid '
                                                'structural patterns found'},
                                  {   'smiles': 'P(OC[C@H](OC(=O)CCC\\C=C\\C[C@@H]1[C@H]([C@H](O)C[C@@H]1O)/C=C/[C@@H](O)CCCCC)COC(=O)CCCCCCCCCCCCCCC)(OCC[N+](C)(C)C)([O-])=O',
                                      'name': 'PC(16:0/PGF2alpha)',
                                      'reason': 'No characteristic icosanoid '
                                                'structural patterns found'},
                                  {   'smiles': 'CCCCC[C@H](O)\\C=C\\[C@H]1[C@H](O)C[C@H](O)[C@@H]1C\\C=C/CCCCN(C)C',
                                      'name': 'prostaglandin F2alpha '
                                              'dimethylamine',
                                      'reason': 'No characteristic icosanoid '
                                                'structural patterns found'},
                                  {   'smiles': 'CCCCC\\C=C/C[C@]1(OC(C)=O)C=CC(=O)\\C1=C\\C=C/[C@@H](CCC(=O)OC)OC(C)=O',
                                      'name': 'clavulone I',
                                      'reason': 'No characteristic icosanoid '
                                                'structural patterns found'},
                                  {   'smiles': 'C1[C@@H]([C@H]([C@H]([C@@H]1O)/C=C/[C@H](CCCCC)O[C@@H]2O[C@H](C([O-])=O)[C@H]([C@@H]([C@H]2O)O)O)C/C=C\\CCCC([O-])=O)O',
                                      'name': '8-iso-prostaglandin '
                                              'F2alpha-glucuronide(2-)',
                                      'reason': 'No characteristic icosanoid '
                                                'structural patterns found'},
                                  {   'smiles': 'O1[C@@]2([C@@]([C@](O)([C@]3([C@]4([C@@]([C@@]5([C@@](CC4)(CC=6N=C7C[C@@]8([C@@]9([C@](C=%10[C@@]([C@]%11(O)[C@@](O[C@@]%12(OC[C@@](O)(CC%12)C)[C@H]%11C)(C%10)[H])([C@H](O)C9)C)([C@@H](O)C[C@]8(CC7=NC6C5)[H])[H])[H])C)[H])C)(CC3=O)[H])[H])C2)C)([C@@H]([C@@]1%13OC(CC%13)(C)C)C)[H])[H]',
                                      'name': 'Ritterazine A',
                                      'reason': 'No characteristic icosanoid '
                                                'structural patterns found'},
                                  {   'smiles': 'P(OC[C@H](OC(=O)CCCCCC[C@@H]1[C@H]([C@H](O)CC1=O)/C=C/[C@@H](O)CCCCC)COC(=O)CCCCC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)(O)(O)=O',
                                      'name': 'PA(22:5(7Z,10Z,13Z,16Z,19Z)/PGE1)',
                                      'reason': 'No characteristic icosanoid '
                                                'structural patterns found'}],
    'attempt': 4,
    'reasoning': 'The previous code had several issues that led to a low F1 '
                 'score:\n'
                 '\n'
                 '1. **Carbon Count Restriction**: The code strictly enforced '
                 'a carbon count between 16-22, which excluded many valid '
                 'icosanoids that are derivatives or conjugates with '
                 'additional carbon atoms. This was evident in the false '
                 'negatives where molecules with more than 22 carbons were '
                 'incorrectly rejected.\n'
                 '\n'
                 '2. **Structural Pattern Matching**: The structural patterns '
                 'used for matching (prostaglandin, leukotriene, epoxide, '
                 'hydroperoxide) were too specific and missed many valid '
                 'icosanoid structures. The patterns need to be more flexible '
                 'to capture the diversity of icosanoid structures.\n'
                 '\n'
                 '3. **Functional Group Detection**: The code required at '
                 'least one of hydroxyl, carboxyl, peroxide, or ester groups, '
                 'which might be too restrictive. Some icosanoids might have '
                 'other oxygen-containing functional groups.\n'
                 '\n'
                 '4. **Double Bond Count**: The code required at least one '
                 'double bond, but some icosanoids might have fewer or more '
                 'complex bonding patterns.\n'
                 '\n'
                 'To improve the code, we should:\n'
                 '- Relax the carbon count restriction to allow for '
                 'derivatives and conjugates.\n'
                 '- Use more flexible structural patterns to capture a wider '
                 'range of icosanoid structures.\n'
                 '- Broaden the functional group detection to include more '
                 'oxygen-containing groups.\n'
                 '- Adjust the double bond count requirement to be more '
                 'inclusive.\n'
                 '\n'
                 'Here is the revised code:',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 242,
    'num_false_positives': 0,
    'num_true_negatives': 0,
    'num_false_negatives': 100,
    'num_negatives': None,
    'precision': 1.0,
    'recall': 0.7076023391812866,
    'f1': 0.8287671232876712,
    'accuracy': 0.7076023391812866,
    'negative_predictive_value': 0.0}