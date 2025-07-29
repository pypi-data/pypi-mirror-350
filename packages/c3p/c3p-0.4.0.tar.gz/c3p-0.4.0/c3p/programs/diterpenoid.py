"""
Classifies: CHEBI:23849 diterpenoid
"""
"""
Classifies: CHEBI:23849 diterpenoid
"""
from rdkit import Chem
from rdkit.Chem import rdMolDescriptors

def is_diterpenoid(smiles: str):
    """
    Determines if a molecule is a diterpenoid based on its SMILES string.
    A diterpenoid is derived from a diterpene, typically with a C20 skeleton, which may be modified.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a diterpenoid, False otherwise
        str: Reason for classification
    """
    
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Count the number of carbon atoms
    c_count = sum(1 for atom in mol.GetAtoms() if atom.GetAtomicNum() == 6)
    
    # Diterpenoids typically have around 20 carbons, but can vary due to modifications
    if c_count < 15 or c_count > 50:  # Wider range to accommodate modifications
        return False, f"Carbon count ({c_count}) is outside the typical range for diterpenoids"

    # Check molecular weight - diterpenoids typically have a molecular weight between 250 and 800 Da
    mol_wt = rdMolDescriptors.CalcExactMolWt(mol)
    if mol_wt < 250 or mol_wt > 800:  # Wider range
        return False, f"Molecular weight ({mol_wt:.2f} Da) is outside the typical range for diterpenoids"

    # Check for the presence of rings or long carbon chains
    ring_info = mol.GetRingInfo()
    num_rings = ring_info.NumRings()
    
    # Check for rotatable bonds - diterpenoids can be flexible or rigid
    n_rotatable = rdMolDescriptors.CalcNumRotatableBonds(mol)
    
    # Check for common terpenoid features (not all need to be present)
    isoprene_pattern = Chem.MolFromSmarts("[CX4H2][CX4H1]=[CX3H1]")  # More general isoprene pattern
    ring_pattern = Chem.MolFromSmarts("[R]")  # Any ring
    long_chain_pattern = Chem.MolFromSmarts("[CX4]~[CX4]~[CX4]~[CX4]")  # Long carbon chain
    
    has_isoprene = mol.HasSubstructMatch(isoprene_pattern)
    has_rings = mol.HasSubstructMatch(ring_pattern)
    has_long_chain = mol.HasSubstructMatch(long_chain_pattern)
    
    # At least two of these features should be present
    if sum([has_isoprene, has_rings, has_long_chain]) < 2:
        return False, "Insufficient characteristic terpenoid features found"

    return True, "Molecule has characteristics consistent with a diterpenoid (C20 skeleton, terpenoid features, and appropriate size)"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:23849',
                          'name': 'diterpenoid',
                          'definition': 'Any terpenoid derived from a '
                                        'diterpene. The term includes '
                                        'compounds in which the C20 skeleton '
                                        'of the parent diterpene has been '
                                        'rearranged or modified by the removal '
                                        'of one or more skeletal atoms '
                                        '(generally methyl groups).',
                          'parents': ['CHEBI:26873'],
                          'xrefs': ['LIPID_MAPS_class:LMPR0104'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 38,
                           'log_lines_of_code': 3.6375861597263857,
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
                                          'from rdkit.Chem import '
                                          'rdMolDescriptors'],
                           'imports_count': 2,
                           'methods_called': [   'GetRingInfo',
                                                 'HasSubstructMatch',
                                                 'MolFromSmarts',
                                                 'MolFromSmiles',
                                                 'GetAtomicNum',
                                                 'GetAtoms',
                                                 'NumRings',
                                                 'CalcNumRotatableBonds',
                                                 'CalcExactMolWt'],
                           'methods_called_count': 9,
                           'smarts_strings': [   '[CX4H2][CX4H1]=[CX3H1]',
                                                 '[CX4]~[CX4]~[CX4]~[CX4]',
                                                 '[R]'],
                           'smarts_strings_count': 3,
                           'defs': ['is_diterpenoid(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, f"Carbon count ({c_count}) '
                                          'is outside the typical range for '
                                          'diterpenoids"',
                                          'False, f"Molecular weight '
                                          '({mol_wt:.2f} Da) is outside the '
                                          'typical range for diterpenoids"',
                                          'False, "Insufficient characteristic '
                                          'terpenoid features found"',
                                          'True, "Molecule has characteristics '
                                          'consistent with a diterpenoid (C20 '
                                          'skeleton, terpenoid features, and '
                                          'appropriate size)"'],
                           'returns_count': 5,
                           'complexity': 4.127517231945277},
    'message': '\n'
               'Attempt failed: F1 score of 0.8432601880877744 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: '
               'O=C1N[C@@H]([C@@H](O)C2=CC=CC=C2)C(=C1C(=O)CCC(C/C(=C/C(CC(CC)C)C)/C)C)O '
               'NAME: Fusaramin REASON: CORRECT Molecule has characteristics '
               'consistent with a diterpenoid (C20 skeleton, terpenoid '
               'features, and appropriate size)\n'
               ' * SMILES: OC(=O)CCC(CCCC(CCCC(CCCC(C)C)C)C)C NAME: '
               'Homophytanic acid REASON: CORRECT Molecule has characteristics '
               'consistent with a diterpenoid (C20 skeleton, terpenoid '
               'features, and appropriate size)\n'
               ' * SMILES: '
               'O1C(OC(CC/C=C(/CC/C=C(/CC(O)/C=C(\\C)/C(O)=O)\\C)\\CO)(C)C=C)C(O)C(O)C(O)C1CO '
               'NAME: Capsianoside V REASON: CORRECT Molecule has '
               'characteristics consistent with a diterpenoid (C20 skeleton, '
               'terpenoid features, and appropriate size)\n'
               ' * SMILES: '
               'O1[C@]2(O)[C@@]3(O)[C@@H](OC[C@H]2O)O[C@H]4[C@H]3[C@@H]([C@H]1OC)CC[C@@H]5C6=C(C(C)C)C[C@@H]([C@]6(C)CC[C@@]45C)O '
               'NAME: Striatoid A REASON: CORRECT Molecule has characteristics '
               'consistent with a diterpenoid (C20 skeleton, terpenoid '
               'features, and appropriate size)\n'
               ' * SMILES: '
               'O[C@]12[C@@]([C@@]3([C@@]([C@@H](O)C1)([C@@H](C4=C(OC=C4)C3)C(=O)C)[H])[H])([C@@H](OC(=O)C)CCC2(C)C)C '
               'NAME: Caesalpinin N REASON: CORRECT Molecule has '
               'characteristics consistent with a diterpenoid (C20 skeleton, '
               'terpenoid features, and appropriate size)\n'
               ' * SMILES: '
               '[H][C@@]12CC[C@]3([H])[C@]([C@H](O)C1=C)([C@@H]2O)[C@@]1(O)OC(=O)[C@]32[C@H](CCC(C)(C)[C@@]2([H])[C@@H]1O)OC(C)=O '
               'NAME: Isoadenolin L REASON: CORRECT Molecule has '
               'characteristics consistent with a diterpenoid (C20 skeleton, '
               'terpenoid features, and appropriate size)\n'
               ' * SMILES: '
               'O[C@@H]1C2=C[C@H](O)[C@H]3C(CC[C@H]([C@@]3([C@H]2CC[C@@]1(C=C)C)C)O)(C)C '
               'NAME: Aspergiloid D REASON: CORRECT Molecule has '
               'characteristics consistent with a diterpenoid (C20 skeleton, '
               'terpenoid features, and appropriate size)\n'
               ' * SMILES: '
               'C[C@@]12CCC[C@](C)([C@H]1CC[C@@]13C[C@@H](CC[C@@H]21)[C@@](O)(CO)C3)C(O)=O '
               'NAME: Diterpenoid SP-II REASON: CORRECT Molecule has '
               'characteristics consistent with a diterpenoid (C20 skeleton, '
               'terpenoid features, and appropriate size)\n'
               ' * SMILES: '
               'O=C(O[C@@H]1C([C@H]2[C@](C3C(C(C(=C)CC3)CCC(O)=CC(=O)C)(C)CC2)(C)CC1)(C)C)C '
               'NAME: Sartorenol REASON: CORRECT Molecule has characteristics '
               'consistent with a diterpenoid (C20 skeleton, terpenoid '
               'features, and appropriate size)\n'
               ' * SMILES: '
               '[H][C@@]12C[C@@H](CC[C@@]1([H])[C@]1(C)[C@@H](O)CC[C@@](C)(COC(C)=O)[C@@]1([H])[C@H](O)C2=O)C(=C)C=O '
               'NAME: Eriocasin D REASON: CORRECT Molecule has characteristics '
               'consistent with a diterpenoid (C20 skeleton, terpenoid '
               'features, and appropriate size)\n'
               ' * SMILES: '
               'O=CC1=C[C@H](O[C@@H]2OC[C@@H](O)[C@@H]([C@H]2O)O)[C@@]3(CC[C@@]4(C([C@H]3C[C@@H]1OC)=C(C(C)C)CC4)C)C '
               'NAME: Erinacine V REASON: CORRECT Molecule has characteristics '
               'consistent with a diterpenoid (C20 skeleton, terpenoid '
               'features, and appropriate size)\n'
               ' * SMILES: '
               'OC(=O)[C@]1(C2[C@](C3C4(CC(CC3)C(C4)=C)CC2)(CCC1)C)C NAME: '
               '(5R,9S)-5,9-dimethyl-14-methylidenetetracyclo[11.2.1.01,10.04,9]hexadecane-5-carboxylic '
               'acid REASON: CORRECT Molecule has characteristics consistent '
               'with a diterpenoid (C20 skeleton, terpenoid features, and '
               'appropriate size)\n'
               ' * SMILES: '
               'O=C(O)C[C@@H]1O[C@](O)(C(C)(C)[C@H]([C@@H]1C)OC)[C@H](C[C@@H]([C@H](O)[C@]2(O[C@@H]2[C@H](C=C(C)C)C)C)C)C '
               'NAME: Gephyronic acid (hemiketal) REASON: CORRECT Molecule has '
               'characteristics consistent with a diterpenoid (C20 skeleton, '
               'terpenoid features, and appropriate size)\n'
               ' * SMILES: '
               'O1[C@@]2([C@]1(C[C@@H](O)CC2(C)C)C)/C=C/C(/C)=C/C=C/C(/C)=C/C=C/C=C(/CO)\\C '
               'NAME: Persicaxanthin REASON: CORRECT Molecule has '
               'characteristics consistent with a diterpenoid (C20 skeleton, '
               'terpenoid features, and appropriate size)\n'
               ' * SMILES: CC(C)c1cc2CC[C@H]3C(C)(C)CCC[C@]3(C=O)c2cc1O NAME: '
               '(+)-pisiferal REASON: CORRECT Molecule has characteristics '
               'consistent with a diterpenoid (C20 skeleton, terpenoid '
               'features, and appropriate size)\n'
               ' * SMILES: '
               '[H][C@@]12OC(=O)[C@@]3(C)CCC[C@](C)(C4=CC(=O)O[C@H](C(C)C)C4=C1)[C@@]23[H] '
               'NAME: nagilactone F REASON: CORRECT Molecule has '
               'characteristics consistent with a diterpenoid (C20 skeleton, '
               'terpenoid features, and appropriate size)\n'
               ' * SMILES: '
               'C[C@@]1([C@H]2[C@H](C(O)=O)[C@@]34CC(=C)[C@@](O)(C3)CC[C@H]4C2=CC(=O)[C@@H]1O)C(O)=O '
               'NAME: gibberellin A8-catabolite REASON: CORRECT Molecule has '
               'characteristics consistent with a diterpenoid (C20 skeleton, '
               'terpenoid features, and appropriate size)\n'
               ' * SMILES: '
               '[H][C@@]12CC[C@]3(O)C[C@]1(CC3=C)[C@@H](C(O)=O)[C@]1([H])[C@@]3(C)[C@@H](O)C=C[C@@]21OC3=O '
               'NAME: gibberellin A3 REASON: CORRECT Molecule has '
               'characteristics consistent with a diterpenoid (C20 skeleton, '
               'terpenoid features, and appropriate size)\n'
               ' * SMILES: '
               'O=C1[C@@]2([C@H](C3=C([C@H](CO)C)CC[C@@]3(C)CC2)CC=C(C1)C=O)C '
               'NAME: Sarcodonin G REASON: CORRECT Molecule has '
               'characteristics consistent with a diterpenoid (C20 skeleton, '
               'terpenoid features, and appropriate size)\n'
               ' * SMILES: '
               'O1[C@@H](OC)[C@]2([C@]3([C@]4([C@]5(C[C@@](C[C@H]4O)(C(C5=O)=C)[H])C(OC3)=O)[H])CCC[C@]2(C1)C)[H] '
               'NAME: 6-Epiangustifolin REASON: CORRECT Molecule has '
               'characteristics consistent with a diterpenoid (C20 skeleton, '
               'terpenoid features, and appropriate size)\n'
               ' * SMILES: '
               'O1[C@@]2([C@]3([C@]([C@]4([C@@]5([C@H]2O)C[C@@](CC4)(C(C5)=C)[H])[H])(CCC[C@]3(C1=O)CO)C)[H])[H] '
               'NAME: 7beta,18-Dihydroxykaurenolide REASON: CORRECT Molecule '
               'has characteristics consistent with a diterpenoid (C20 '
               'skeleton, terpenoid features, and appropriate size)\n'
               ' * SMILES: CC(C)C1=C(C=CC2=C1CCC3[C@@]2(CCCC3(C)C)C)OC(=O)C '
               'NAME: acetic acid '
               '[(4bS)-4b,8,8-trimethyl-1-propan-2-yl-5,6,7,8a,9,10-hexahydrophenanthren-2-yl] '
               'ester REASON: CORRECT Molecule has characteristics consistent '
               'with a diterpenoid (C20 skeleton, terpenoid features, and '
               'appropriate size)\n'
               ' * SMILES: '
               'O1[C@@]2(O)[C@]3([C@@H](C4=C(C(C)C)CC[C@]4(C)CC3)C[C@@H]1[C@@H](C5O[C@@H](C)[C@H](O5)C)[C@H]2O)C '
               'NAME: Cyahookerin A REASON: CORRECT Molecule has '
               'characteristics consistent with a diterpenoid (C20 skeleton, '
               'terpenoid features, and appropriate size)\n'
               ' * SMILES: CC(/C=C\\C=C(C)\\C=C\\C1=C(C)CCCC1(C)C)=C\\C=O '
               'NAME: 11-cis-retinal REASON: CORRECT Molecule has '
               'characteristics consistent with a diterpenoid (C20 skeleton, '
               'terpenoid features, and appropriate size)\n'
               ' * SMILES: '
               'O=C1N[C@](OC)(CC2=CC=CC=C2)C=C1C(=O)[C@@H]3[C@@H](C(=C[C@]4([C@H]3CC[C@H](C4)C)C)C)/C(=C/C)/C '
               'NAME: Chaetolivacine B REASON: CORRECT Molecule has '
               'characteristics consistent with a diterpenoid (C20 skeleton, '
               'terpenoid features, and appropriate size)\n'
               'False positives: NONE\n'
               'False negatives: SMILES: '
               'P(OCC[N+](C)(C)C)(OC[C@H](OC\\C=C(\\CC\\C=C(\\CC/C=C(/CCC=C(C)C)\\C)/C)/C)COC\\C=C(\\CC\\C=C(\\CC\\C=C(\\CCC=C(C)C)/C)/C)/C)([O-])=O '
               'NAME: '
               '1-(2E,6E,10E,14E-phytatetraenyl)-2-(2E,6E,10E,14E-phytatetraenyl)-sn-glycero-3-phosphocholine '
               'REASON: MISSED Carbon count (48) is outside the typical range '
               'for diterpenoids\n'
               ' * SMILES: '
               'O([C@@H]1[C@@H](O)[C@H](O)[C@H](O[C@H]1OC/C=C(/CC/C=C(/CC/C=C(/CCC=C(C)C)\\C)\\C)\\C)CO[C@@H]2O[C@H]([C@H](OC(=O)C)[C@@H](O)[C@H]2O)C)[C@@H]3O[C@H]([C@H](OC(=O)C)[C@@H](OC(=O)C)[C@H]3OC(=O)C)C '
               'NAME: '
               '[(2s,3r,4s,5r,6r)-6-[[(2r,3s,4s,5r,6r)-3,4-dihydroxy-6-[(2e,6e,10e)-3,7,11,15-tetramethylhexadeca-2,6,10,14-tetraenoxy]-5-[(2s,3r,4r,5s,6s)-3,4,5-triacetyloxy-6-methyloxan-2-yl]oxyoxan-2-yl]methoxy]-4,5-dihydroxy-2-methyloxan-3-yl] '
               'acetate REASON: MISSED Carbon count (46) is outside the '
               'typical range for diterpenoids\n'
               ' * SMILES: '
               'O[C@@H]1[C@@]2([C@]3([C@@](CC2)(C(=CCC[C@@H](CCC(=C3C)[C@H]1O)C)C)[H])[H])C '
               'NAME: Isotrinervidiol REASON: MISSED Too few rotatable bonds '
               'for a typical diterpenoid\n'
               ' * SMILES: '
               'C[C@]12CCC[C@@]3(CN4CCOC14)[C@@H]1CC[C@H]4C[C@@]1(CC[C@H]23)[C@@H](O)C4=C '
               'NAME: Garryine REASON: MISSED Too few rotatable bonds for a '
               'typical diterpenoid\n'
               ' * SMILES: '
               'ClC1=CC(=C(NC)C=C1)C(=O)O[C@@H]2[C@]([C@H]3[C@]([C@@H]4[C@]([C@@H](C5=C(O)C(=O)OC5O)[C@H](C)[C@H](C4)OC)(C)CC3)(C)CC2)(CO)C '
               'NAME: Tiancilactone C REASON: MISSED Carbon count (32) is '
               'outside the typical range for diterpenoids\n'
               ' * SMILES: '
               'O=C1OC(/C(=C/C=C/C(C(O)C2OC2C(C(OC)CC)C)C)/C)C(C=CC(OC(=O)C)C(CCC(C1)O)(O)C)C '
               'NAME: FD-895 REASON: MISSED Carbon count (31) is outside the '
               'typical range for diterpenoids\n'
               ' * SMILES: '
               'O=C1OC(/C=C/C(=C\\C(C/C=C/C(=C/C(C(=O)C(C(O)C(C/C(=C/C)/C)C)C)C)/C)C)/C)CC=C1 '
               'NAME: Anguinomycin C REASON: MISSED Carbon count (31) is '
               'outside the typical range for diterpenoids\n'
               ' * SMILES: '
               'CC[C@H]([C@@H]1O[C@@H]([C@@H](C)[C@H](O)[C@H](C)C(=O)[C@H](CC)[C@H]2O[C@@]3(O[C@@]4(CC[C@](C)(O4)C4CC[C@](O)(CC)[C@H](C)O4)C(=O)C=C3)[C@H](C)C[C@@H]2C)[C@@H](C)C[C@@H]1C)C(O)=O '
               'NAME: A28086B REASON: MISSED Carbon count (43) is outside the '
               'typical range for diterpenoids\n'
               ' * SMILES: '
               'O=C1C2=C(O)C3=C(O)C(C4=C(O)C=5C(O)=C6C(=O)[C@H]7O[C@@]7(C)[C@@H]([C@]6(C)OC5C=C4)OC(=O)CCC(=O)OC)=CC=C3O[C@]2([C@@H](OC(=O)CCC(=O)OC)[C@]8([C@@H]1O8)C)C '
               'NAME: Penicixanthone G REASON: MISSED Carbon count (40) is '
               'outside the typical range for diterpenoids\n'
               ' * SMILES: '
               'O=C1C2=C(O)C3=C(O)C(C4=C(O)C=5C(O)=C6C(=O)[C@H]7O[C@@]7(C)[C@@H]([C@]6(C)OC5C=C4)OC(=O)CCC(=O)O)=CC=C3O[C@]2([C@@H](OC(=O)CCC(=O)OC)[C@]8([C@@H]1O8)C)C '
               'NAME: Penicixanthone H REASON: MISSED Carbon count (39) is '
               'outside the typical range for diterpenoids\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [],
    'sample_false_negatives': [   {   'smiles': 'OC(=O)CCC(CCCC(CCCC(CCCC(C)C)C)C)C',
                                      'name': 'Homophytanic acid',
                                      'reason': 'Insufficient characteristic '
                                                'terpenoid features found'},
                                  {   'smiles': 'P(OCC[N+](C)(C)C)(OC[C@H](OC\\C=C(\\CC\\C=C(\\CC/C=C(/CCC=C(C)C)\\C)/C)/C)COC\\C=C(\\CC\\C=C(\\CC\\C=C(\\CCC=C(C)C)/C)/C)/C)([O-])=O',
                                      'name': '1-(2E,6E,10E,14E-phytatetraenyl)-2-(2E,6E,10E,14E-phytatetraenyl)-sn-glycero-3-phosphocholine',
                                      'reason': 'Molecular weight (801.60 Da) '
                                                'is outside the typical range '
                                                'for diterpenoids'},
                                  {   'smiles': 'O([C@@H]1[C@@H](O)[C@H](O)[C@H](O[C@H]1OC/C=C(/CC/C=C(/CC/C=C(/CCC=C(C)C)\\C)\\C)\\C)CO[C@@H]2O[C@H]([C@H](OC(=O)C)[C@@H](O)[C@H]2O)C)[C@@H]3O[C@H]([C@H](OC(=O)C)[C@@H](OC(=O)C)[C@H]3OC(=O)C)C',
                                      'name': '[(2s,3r,4s,5r,6r)-6-[[(2r,3s,4s,5r,6r)-3,4-dihydroxy-6-[(2e,6e,10e)-3,7,11,15-tetramethylhexadeca-2,6,10,14-tetraenoxy]-5-[(2s,3r,4r,5s,6s)-3,4,5-triacetyloxy-6-methyloxan-2-yl]oxyoxan-2-yl]methoxy]-4,5-dihydroxy-2-methyloxan-3-yl] '
                                              'acetate',
                                      'reason': 'Molecular weight (912.47 Da) '
                                                'is outside the typical range '
                                                'for diterpenoids'},
                                  {   'smiles': 'O=C1C2=C(O)C3=C(O)C(C4=C(O)C=5C(O)=C6C(=O)[C@H]7O[C@@]7(C)[C@@H]([C@]6(C)OC5C=C4)OC(=O)CCC(=O)OC)=CC=C3O[C@]2([C@@H](OC(=O)CCC(=O)OC)[C@]8([C@@H]1O8)C)C',
                                      'name': 'Penicixanthone G',
                                      'reason': 'Molecular weight (806.21 Da) '
                                                'is outside the typical range '
                                                'for diterpenoids'},
                                  {   'smiles': 'OC1=C(C=2C=3C=4C(=C(C=CC4C=CC3)C5=CC=CC=C5)C(=O)C2O)C=6C=7C(=C(C=CC7C=CC6)C8=CC=CC=C8)C1=O',
                                      'name': "3,3'-Bisanigorufone",
                                      'reason': 'Insufficient characteristic '
                                                'terpenoid features found'},
                                  {   'smiles': 'O=C1C(=O)C(=C(C=2OC(C=C(C)C)=CC2CCC/C(=C/CC3=C(O)C=C(C)C=C3O)/C)C(=C1C/C=C(/CC/C=C(/CC(=O)C=C(C)C)\\C)\\C)O)C',
                                      'name': 'Grifolinone B',
                                      'reason': 'Insufficient characteristic '
                                                'terpenoid features found'},
                                  {   'smiles': 'CO[C@@H](C[C@@H]1OC(=O)C[C@@H](O)C[C@H](C)C[C@H](O)[C@H](C)[C@@H](OC)c2coc(n2)-c2coc(n2)-c2coc(\\C=C\\C[C@H](OC)[C@H]1C)n2)[C@@H](C)CCC(=O)[C@H](C)[C@H](OC)[C@H](C)\\C=C\\N(C)C=O',
                                      'name': 'kabiramide D',
                                      'reason': 'Molecular weight (898.49 Da) '
                                                'is outside the typical range '
                                                'for diterpenoids'},
                                  {   'smiles': 'O=C1C(=O)C(=C(C=2OC(C=C(C)C)=CC2CCC/C(=C/CC3=C(O)C=C(C)C=C3O)/C)C(=C1C/C=C(/CC/C=C(/C[C@H](O)C=C(C)C)\\C)\\C)O)C',
                                      'name': '16-Hydroxyalbatrellin',
                                      'reason': 'Insufficient characteristic '
                                                'terpenoid features found'},
                                  {   'smiles': 'O=C/C(=C/C=O)/CC/C=C(/CC/C=C(/CCC=C(C)C)\\C)\\C',
                                      'name': 'Schizostatin',
                                      'reason': 'Insufficient characteristic '
                                                'terpenoid features found'},
                                  {   'smiles': 'CC(CCCC(C)CCC=C(C)C)CCC\\C(C)=C\\COP(O)(=O)OP(O)(O)=O',
                                      'name': 'Tetrahydrogeranylgeranyl '
                                              'diphosphate',
                                      'reason': 'Insufficient characteristic '
                                                'terpenoid features found'}],
    'attempt': 2,
    'reasoning': 'The previous code had a few issues that led to false '
                 "negatives and a lower F1 score. Let's analyze the problems "
                 'and improve the code:\n'
                 '\n'
                 '1. **Carbon Count Range**: The range of 15-30 carbons was '
                 'too restrictive. Some diterpenoids can have more carbons due '
                 'to modifications or side chains.\n'
                 '\n'
                 '2. **Rotatable Bonds**: The requirement of at least 1 '
                 'rotatable bond was too strict. Some diterpenoids can be '
                 'quite rigid.\n'
                 '\n'
                 '3. **Molecular Weight Range**: The range of 250-600 Da was '
                 'too narrow. Some diterpenoids can be larger.\n'
                 '\n'
                 '4. **Terpenoid Features**: The isoprene pattern matching was '
                 'too simplistic and might miss some diterpenoid structures.\n'
                 '\n'
                 "Here's the improved code:",
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 832,
    'num_false_positives': 0,
    'num_true_negatives': 0,
    'num_false_negatives': 100,
    'num_negatives': None,
    'precision': 1.0,
    'recall': 0.8927038626609443,
    'f1': 0.9433106575963719,
    'accuracy': 0.8927038626609443,
    'negative_predictive_value': 0.0}