"""
Classifies: CHEBI:61051 lipid hydroperoxide
"""
from rdkit import Chem

def is_lipid_hydroperoxide(smiles: str):
    """
    Determines if a molecule is a lipid hydroperoxide based on its SMILES string.
    A lipid hydroperoxide is characterized by the presence of hydroperoxy groups (-OOH) 
    attached to a lipid-like structure, typically devoid of structural complexities like 
    charged groups or extensive cyclic elements.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a lipid hydroperoxide, False otherwise
        str: Reason for classification
    """
    
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
        
    # Look for hydroperoxy group pattern (-OOH)
    hydroperoxy_pattern = Chem.MolFromSmarts("[OX2H]O")
    hydroperoxy_matches = mol.GetSubstructMatches(hydroperoxy_pattern)
    if not hydroperoxy_matches:
        return False, "No hydroperoxy groups found"

    # Consider minimum reasonable carbon atoms threshold to define a lipid
    c_count = sum(1 for atom in mol.GetAtoms() if atom.GetAtomicNum() == 6)
    if c_count < 16:  # Increased to 16 for better alignment with lipid length
        return False, f"Only {c_count} carbon atoms found, potentially too few for lipid structure"

    # Check for presence of carboxylic group and avoid negative charges
    carboxylic_pattern = Chem.MolFromSmarts("C(=O)[O]")
    carboxylic_matches = mol.GetSubstructMatches(carboxylic_pattern)
    if not carboxylic_matches:
        return False, "No carboxylic structures found"
    
    # Exclude charged species
    if any(atom.GetFormalCharge() != 0 for atom in mol.GetAtoms()):
        return False, "Charged species present, excluding for lipid hydroperoxide"

    # Avoid extensive cyclic structures or complex multi-oxygen linkages (heuristically)
    # Such features commonly denote deviation from lipid hydroperoxides
    if mol.GetRingInfo().NumRings() > 1:
        return False, "Multiple rings detected, uncharacteristic of typical lipid hydroperoxides"

    return True, f"Contains {len(hydroperoxy_matches)} hydroperoxy group(s) and lipid-like structure with {c_count} carbon atoms"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:61051',
                          'name': 'lipid hydroperoxide',
                          'definition': 'Any lipid carrying one or more '
                                        'hydroperoxy substituents.',
                          'parents': ['CHEBI:18059', 'CHEBI:35924'],
                          'xrefs': ['KEGG:C01025'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 37,
                           'log_lines_of_code': 3.6109179126442243,
                           'indent_by_line': [   1,
                                                 1,
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
                                                 0,
                                                 1],
                           'max_indent': 2,
                           'imports': ['from rdkit import Chem'],
                           'imports_count': 1,
                           'methods_called': [   'GetFormalCharge',
                                                 'NumRings',
                                                 'GetAtoms',
                                                 'GetSubstructMatches',
                                                 'MolFromSmiles',
                                                 'MolFromSmarts',
                                                 'GetRingInfo',
                                                 'GetAtomicNum'],
                           'methods_called_count': 8,
                           'smarts_strings': ['C(=O)[O]', '[OX2H]O'],
                           'smarts_strings_count': 2,
                           'defs': ['is_lipid_hydroperoxide(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "No hydroperoxy groups '
                                          'found"',
                                          'False, f"Only {c_count} carbon '
                                          'atoms found, potentially too few '
                                          'for lipid structure"',
                                          'False, "No carboxylic structures '
                                          'found"',
                                          'False, "Charged species present, '
                                          'excluding for lipid hydroperoxide"',
                                          'False, "Multiple rings detected, '
                                          'uncharacteristic of typical lipid '
                                          'hydroperoxides"',
                                          'True, f"Contains '
                                          '{len(hydroperoxy_matches)} '
                                          'hydroperoxy group(s) and lipid-like '
                                          'structure with {c_count} carbon '
                                          'atoms"'],
                           'returns_count': 7,
                           'complexity': 4.3221835825288455},
    'message': '\n'
               'Attempt failed: F1 score of 0.6054054054054054 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: '
               'OC(=O)CCCCCCC/C=C\\C\\C=C\\C=C\\C(OO)CC NAME: 16-HpOTrE '
               'REASON: CORRECT Contains 1 hydroperoxy group(s) and lipid-like '
               'structure with 18 carbon atoms\n'
               ' * SMILES: CC\\C=C/C\\C=C/C=C/[C@H](CCCCCCCC(O)=O)OO NAME: '
               '(9S,10E,12Z,15Z)-9-hydroperoxyoctadeca-10,12,15-trienoic acid '
               'REASON: CORRECT Contains 1 hydroperoxy group(s) and lipid-like '
               'structure with 18 carbon atoms\n'
               ' * SMILES: '
               'C(\\C=C/C=C\\C(C/C=C\\CCCCCC(O)=O)OO)=C/C(C/C=C\\CC)OO NAME: '
               '(7Z,11Z,13Z,15E,19Z)-10,17-bis(hydroperoxy)docosapentaenoic '
               'acid REASON: CORRECT Contains 2 hydroperoxy group(s) and '
               'lipid-like structure with 22 carbon atoms\n'
               ' * SMILES: CCCCC\\C=C/C[C@H](OO)\\C=C\\C=C/CCCCCCC(O)=O NAME: '
               '12(S)-HPE(8,10,14)TrE REASON: CORRECT Contains 1 hydroperoxy '
               'group(s) and lipid-like structure with 20 carbon atoms\n'
               ' * SMILES: CCCCC\\C=C/CC(OO)\\C=C\\C=C/CCCCC(O)=O NAME: '
               '10-HPO(6,8,12)TrE REASON: CORRECT Contains 1 hydroperoxy '
               'group(s) and lipid-like structure with 18 carbon atoms\n'
               ' * SMILES: CCCCC\\C=C/C[C@H](OO)\\C=C\\C=C/C\\C=C/CCCC(O)=O '
               'NAME: 12(S)-HPETE REASON: CORRECT Contains 1 hydroperoxy '
               'group(s) and lipid-like structure with 20 carbon atoms\n'
               ' * SMILES: C(CC(=O)O)CCCCC/C=C\\C=C\\[C@H](/C=C\\CCC)OO NAME: '
               '(9Z,11E,13S,14Z)-13-hydroperoxyoctadecatrienoic acid REASON: '
               'CORRECT Contains 1 hydroperoxy group(s) and lipid-like '
               'structure with 18 carbon atoms\n'
               ' * SMILES: CCCCC\\C=C/C[C@@H](OO)\\C=C\\CCCCCCC(O)=O NAME: '
               '(8E,10R,12Z)-10-hydroperoxy-8,12-octadecadienoic acid REASON: '
               'CORRECT Contains 1 hydroperoxy group(s) and lipid-like '
               'structure with 18 carbon atoms\n'
               ' * SMILES: O(O)[C@H](CCCCCC/C=C\\C/C=C(/O)\\C/C=C\\CC)C(O)=O '
               'NAME: 2R-HpOTrE REASON: CORRECT Contains 1 hydroperoxy '
               'group(s) and lipid-like structure with 18 carbon atoms\n'
               ' * SMILES: CCCCC[C@H](OO)\\C=C\\C=C/CCCCCCCC(O)=O NAME: '
               '13(S)-HPODE REASON: CORRECT Contains 1 hydroperoxy group(s) '
               'and lipid-like structure with 18 carbon atoms\n'
               ' * SMILES: O(O)C(CCCCCCCC(O)=O)/C=C/C=C/CCCCC NAME: '
               'E,E-9-HpODE REASON: CORRECT Contains 1 hydroperoxy group(s) '
               'and lipid-like structure with 18 carbon atoms\n'
               ' * SMILES: O1OC\\2CC1C(/C2=C/C(OO)CCCC(O)=O)C/C=C/CCCCC NAME: '
               '5-hydroperoxy-7-[3,5-epidioxy-2-(2-octenyl)-cyclopentyl]-6-heptenoic '
               'acid REASON: CORRECT Contains 1 hydroperoxy group(s) and '
               'lipid-like structure with 19 carbon atoms\n'
               ' * SMILES: OC(CC/C=C\\C/C=C\\C/C=C\\C=C\\C(C/C=C\\CCCCC)OO)=O '
               'NAME: (4Z,7Z,10Z,12E,16Z)-14-hydroperoxydocosapentaenoic acid '
               'REASON: CORRECT Contains 1 hydroperoxy group(s) and lipid-like '
               'structure with 22 carbon atoms\n'
               ' * SMILES: CC\\C=C/C\\C=C/C[C@H](OO)\\C=C\\CCCCCCC(O)=O NAME: '
               '(8E,10S,12Z,15Z)-10-hydroperoxyoctadeca-8,12,15-trienoic acid '
               'REASON: CORRECT Contains 1 hydroperoxy group(s) and lipid-like '
               'structure with 18 carbon atoms\n'
               ' * SMILES: CC\\C=C/C\\C=C/C=C/[C@@H](CCCCCCCC(O)=O)OO NAME: '
               '(9R,10E,12Z,15Z)-9-hydroperoxyoctadeca-10,12,15-trienoic acid '
               'REASON: CORRECT Contains 1 hydroperoxy group(s) and lipid-like '
               'structure with 18 carbon atoms\n'
               ' * SMILES: '
               'OC(CC/C=C\\C/C=C\\CC(\\C=C/C=C\\C=C\\[C@H](C/C=C\\CC)OO)OO)=O '
               'NAME: '
               '(4Z,7Z,11Z,13Z,15E,17S,19Z)-10,17-bis(hydroperoxy)docosahexaenoic '
               'acid REASON: CORRECT Contains 2 hydroperoxy group(s) and '
               'lipid-like structure with 22 carbon atoms\n'
               ' * SMILES: C(C/C=C\\C=C\\[C@H](CCCCC)OO)CCCCCCCC(=O)O NAME: '
               '(15S)-hydroperoxy-(11Z,13E)-icosadienoic acid REASON: CORRECT '
               'Contains 1 hydroperoxy group(s) and lipid-like structure with '
               '20 carbon atoms\n'
               ' * SMILES: [H]C(=CCCCCCCCCC(=O)OC)C1C2CC(OO2)C1C([H])=CC(CC)OO '
               'NAME: methyl '
               '8-[3,5-epidioxy-2-(3-hydroperoxy-1-pentenyl)-cyclopentyl]-octanoate '
               'REASON: CORRECT Contains 1 hydroperoxy group(s) and lipid-like '
               'structure with 22 carbon atoms\n'
               ' * SMILES: '
               'C(CCC(O)=O)/C=C\\C/C=C\\C=C\\[C@H](C[C@H]1[C@@H](CCCCC)O1)OO '
               'NAME: '
               '(12S)-hydroperoxy-(14S,15R)-epoxy-(5Z,8Z,10E)-icosatrienoic '
               'acid REASON: CORRECT Contains 1 hydroperoxy group(s) and '
               'lipid-like structure with 20 carbon atoms\n'
               ' * SMILES: '
               'C(=C\\C=C\\[C@H](CCCCC)OO)\\C=C\\[C@H](C/C=C\\CCCC(O)=O)OO '
               'NAME: 8(S),15(S)-DiHPETE REASON: CORRECT Contains 2 '
               'hydroperoxy group(s) and lipid-like structure with 20 carbon '
               'atoms\n'
               ' * SMILES: C(CCC(O)=O)CCC/C=C\\C(/C=C\\C/C=C\\CCCCC)OO NAME: '
               '(8Z,11Z,14Z)-10-hydroperoxyicosatrienoic acid REASON: CORRECT '
               'Contains 1 hydroperoxy group(s) and lipid-like structure with '
               '20 carbon atoms\n'
               ' * SMILES: C(CCC(O)=O)CCC/C=C\\C/C=C\\C=C\\[C@H](CCCCC)OO '
               'NAME: (8Z,11Z,13E,15S)-15-hydroperoxyicosa-8,11,13-trienoic '
               'acid REASON: CORRECT Contains 1 hydroperoxy group(s) and '
               'lipid-like structure with 20 carbon atoms\n'
               ' * SMILES: C(=C\\[C@H](/C=C\\CCCCC)OO)\\CCCCCCCC(=O)O NAME: '
               '(11S)-11-hydroperoxylinoleic acid REASON: CORRECT Contains 1 '
               'hydroperoxy group(s) and lipid-like structure with 18 carbon '
               'atoms\n'
               ' * SMILES: '
               'C(CC/C=C\\C[C@H](OO)/C=C/C=C\\C=C\\[C@H](C/C=C\\C/C=C\\CC)OO)(O)=O '
               'NAME: '
               '(7S,14S)-bis(hydroperoxy)-(4Z,8E,10Z,12E,16Z,19Z)-docosahexaenoic '
               'acid REASON: CORRECT Contains 2 hydroperoxy group(s) and '
               'lipid-like structure with 22 carbon atoms\n'
               ' * SMILES: '
               'C(CCC)C[C@@H](/C=C/C=C\\C/C=C\\C/C=C\\CCCC(NCC(O)=O)=O)OO '
               'NAME: '
               'N-[(15S)-hydroperoxy-(5Z,8Z,11Z,13E)-icosatetraenoyl]glycine '
               'REASON: CORRECT Contains 1 hydroperoxy group(s) and lipid-like '
               'structure with 22 carbon atoms\n'
               'False positives: SMILES: '
               'C(/C=C\\C=C/C(C/C=C\\C/C=C\\CCC([O-])=O)OO)=C\\[C@H](CCCCC)OO '
               'NAME: '
               '(4Z,7Z,11Z,13Z,15E,17S)-10,17-bis(hydroperoxy)docosapentaenoate '
               'REASON: WRONGLY CLASSIFIED Contains 2 hydroperoxy group(s) and '
               'lipid-like structure with 22 carbon atoms\n'
               ' * SMILES: '
               'O=C(CCC/C=C\\C/C=C\\C/C=C\\C=C\\C(CCCCC)OO)O[C@@H](COP(OCC[NH3+])(=O)[O-])COC(=O)CCCCCCCCCCCCCCCCC '
               'NAME: '
               '1-stearoyl-2-(15-hydroperoxyarachidonoyl)-sn-glycero-3-phosphoethanolamine '
               'zwitterion REASON: WRONGLY CLASSIFIED Contains 1 hydroperoxy '
               'group(s) and lipid-like structure with 43 carbon atoms\n'
               ' * SMILES: '
               'C(CCC[C@@H]([C@@H](/C=C/C=C/C=C\\C=C\\[C@@H](OO)CCCCC)O)O)([O-])=O '
               'NAME: '
               '(5S,6R)-dihydroxy-(15S)-hydroperoxy-(7E,9E,11Z,13E)-icosatetraenoate '
               'REASON: WRONGLY CLASSIFIED Contains 1 hydroperoxy group(s) and '
               'lipid-like structure with 20 carbon atoms\n'
               ' * SMILES: CCCCCCC\\C=C\\C(CCCCCCCC([O-])=O)OO NAME: '
               '9-hydroperoxy-10E-octadecenoate REASON: WRONGLY CLASSIFIED '
               'Contains 1 hydroperoxy group(s) and lipid-like structure with '
               '18 carbon atoms\n'
               ' * SMILES: '
               'CC\\C=C/C\\C=C/CC(OO)\\C=C\\C=C/C\\C=C/C\\C=C/CCC([O-])=O '
               'NAME: 14-HPDHE(1-) REASON: WRONGLY CLASSIFIED Contains 1 '
               'hydroperoxy group(s) and lipid-like structure with 22 carbon '
               'atoms\n'
               ' * SMILES: C(C/C=C\\C=C\\[C@H](CCCCC)OO)CCCCCCCC(=O)[O-] NAME: '
               '(15S)-hydroperoxy-(11Z,13E)-icosadienoate REASON: WRONGLY '
               'CLASSIFIED Contains 1 hydroperoxy group(s) and lipid-like '
               'structure with 20 carbon atoms\n'
               ' * SMILES: '
               '[H][C@@]12C[C@@H](OC(=O)\\C=C/C=C/CCCCC)C=C3[C@H](O[C@@H](OC(C)=O)[C@@]13[C@@H](O)C[C@@H](C)[C@@]2(C)C[C@H](OO)C(=C)C=C)OC(C)=O '
               'NAME: Argutin F REASON: WRONGLY CLASSIFIED Contains 1 '
               'hydroperoxy group(s) and lipid-like structure with 34 carbon '
               'atoms\n'
               ' * SMILES: O(O)[C@H](CCCCC)\\C=C\\CCCCCCCCCC(O)=O NAME: '
               '13R-HpOME(11E) REASON: WRONGLY CLASSIFIED Contains 1 '
               'hydroperoxy group(s) and lipid-like structure with 18 carbon '
               'atoms\n'
               ' * SMILES: C(CCCCCCC/C=C\\[C@H](/C=C\\C/C=C\\CC)OO)(=O)[O-] '
               'NAME: (9Z,11R,12Z,15Z)-11-hydroperoxyoctadecatrienoate REASON: '
               'WRONGLY CLASSIFIED Contains 1 hydroperoxy group(s) and '
               'lipid-like structure with 18 carbon atoms\n'
               ' * SMILES: '
               '[C@@H]1([C@@H]2C[C@H]([C@@H]1/C=C/[C@H](C/C=C\\CC)OO)OO2)C/C=C\\CCCC([O-])=O '
               'NAME: prostaglandin G3(1-) REASON: WRONGLY CLASSIFIED Contains '
               '1 hydroperoxy group(s) and lipid-like structure with 20 carbon '
               'atoms\n'
               ' * SMILES: '
               'O[C@H]1[C@@H]([C@H](C(=O)C1)C/C=C\\CCCC(O)=O)/C=C/[C@@H](OO)CCCCC '
               'NAME: 15S-hydroperoxy-PGE2 REASON: WRONGLY CLASSIFIED Contains '
               '1 hydroperoxy group(s) and lipid-like structure with 20 carbon '
               'atoms\n'
               ' * SMILES: C(CC/C=C\\C/C=C\\C/C=C\\C=C\\C(CCCC(=O)[O-])OO)CC '
               'NAME: 5-HPETE(1-) REASON: WRONGLY CLASSIFIED Contains 1 '
               'hydroperoxy group(s) and lipid-like structure with 20 carbon '
               'atoms\n'
               ' * SMILES: '
               'O1O[C@]2([C@@H]([C@@H]([C@@]1(C2)[H])CCC(O)=O)/C=C/[C@@H](OO)C/C=C\\C/C=C\\C/C=C\\CC)[H] '
               'NAME: 11-Hydroperoxy-H4-neuroprostane REASON: WRONGLY '
               'CLASSIFIED Contains 1 hydroperoxy group(s) and lipid-like '
               'structure with 22 carbon atoms\n'
               ' * SMILES: '
               'C(=C/[C@H](C/C=C\\CCCCC)OO)\\C=C/C/C=C\\CCCC(=O)NCC([O-])=O '
               'NAME: '
               'N-[(12S)-hydroperoxy-(5Z,8Z,10E,14Z)-icosatetraenoyl]glycinate '
               'REASON: WRONGLY CLASSIFIED Contains 1 hydroperoxy group(s) and '
               'lipid-like structure with 22 carbon atoms\n'
               ' * SMILES: [O-]C(CCCCCC\\C=C\\[C@@H](CCCCCCCC)OO)=O NAME: '
               '10(R)-HPOME(1-) REASON: WRONGLY CLASSIFIED Contains 1 '
               'hydroperoxy group(s) and lipid-like structure with 18 carbon '
               'atoms\n'
               ' * SMILES: OC(CCCCCCCC(O)=O)C(O)/C=C/C(OO)CCCCC NAME: '
               '9,10-dihydroxy-13-hydroperoxy-11-octadecenoic acid REASON: '
               'WRONGLY CLASSIFIED Contains 1 hydroperoxy group(s) and '
               'lipid-like structure with 18 carbon atoms\n'
               ' * SMILES: O1OC(CC1C(OO)/C=C/C(OO)CCCCC)/C=C/C=C/CCCC(OC)=O '
               'NAME: Methyl '
               '9,11-epidioxy-12,15-dihydroperoxy-5,7,13-eicosatrienoate '
               'REASON: WRONGLY CLASSIFIED Contains 2 hydroperoxy group(s) and '
               'lipid-like structure with 21 carbon atoms\n'
               ' * SMILES: O(O)C(CCCCCCC(O)=O)/C=C\\CCCCCCCC NAME: 8-HpOME '
               'REASON: WRONGLY CLASSIFIED Contains 1 hydroperoxy group(s) and '
               'lipid-like structure with 18 carbon atoms\n'
               ' * SMILES: '
               'C(CCC[C@@H](/C=C/C=C\\C/C=C\\C=C\\[C@H](CCCCC)OO)OO)([O-])=O '
               'NAME: (5S,15S)-dihydroperoxy-(6E,8Z,11Z,13E)-icosatetraenoate '
               'REASON: WRONGLY CLASSIFIED Contains 2 hydroperoxy group(s) and '
               'lipid-like structure with 20 carbon atoms\n'
               ' * SMILES: '
               'O(O)[C@@H](CCCC([O-])=O)/C=C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC '
               'NAME: 5(S)-HpEPE(1-) REASON: WRONGLY CLASSIFIED Contains 1 '
               'hydroperoxy group(s) and lipid-like structure with 20 carbon '
               'atoms\n'
               ' * SMILES: '
               '[H][C@]12CC[C@@]3(C)[C@@]([H])([C@@H](O)C[C@]3(C)C1=CC[C@@]1([H])C(C)(C)C(=O)CC[C@]21C)[C@@H](C\\C=C\\C(C)(C)OO)C(=O)OC '
               'NAME: meliastatin 3 REASON: WRONGLY CLASSIFIED Contains 1 '
               'hydroperoxy group(s) and lipid-like structure with 31 carbon '
               'atoms\n'
               ' * SMILES: O1OC(CC1C2OOC(C2)/C=C/CCCCCCC(OC)=O)C(OO)CC NAME: '
               'methyl 10,12,13,15-bisepidioxy-16-hydroperoxy-8E-octadecenoate '
               'REASON: WRONGLY CLASSIFIED Contains 1 hydroperoxy group(s) and '
               'lipid-like structure with 19 carbon atoms\n'
               ' * SMILES: O(O)[C@H](CCCCCCC(O)=O)/C=C\\CCCCCCCC NAME: '
               '8R-HpOME REASON: WRONGLY CLASSIFIED Contains 1 hydroperoxy '
               'group(s) and lipid-like structure with 18 carbon atoms\n'
               ' * SMILES: O1OC(CC1C(OO)CCCC(OC)=O)/C=C/C=C/C=C/C(OO)CCCCC '
               'NAME: methyl '
               '6,8-epidioxy-5,15-dihydroperoxy-9,11,13-eicosatrienoate '
               'REASON: WRONGLY CLASSIFIED Contains 2 hydroperoxy group(s) and '
               'lipid-like structure with 21 carbon atoms\n'
               ' * SMILES: '
               'C(/C=C\\C/C=C\\CCCC(=O)[O-])[C@H](/C=C/C=C\\CCCCC)OO NAME: '
               '11(R)-HPETE(1-) REASON: WRONGLY CLASSIFIED Contains 1 '
               'hydroperoxy group(s) and lipid-like structure with 20 carbon '
               'atoms\n'
               'False negatives: NONE\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': '[H][C@@]1(O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O)O[C@@H]1[C@@H](O)[C@@H](O)[C@@H](CO)O[C@H]1OC[C@H]1O[C@@H](OC[C@H]2O[C@@H](OC[C@H](NC(=O)[C@H](O)CCCCCCCCCCCCCCCCCCCCCC)[C@H](O)[C@H](O)CCCCCCCCCCCCCC)[C@H](O)[C@@H](O)[C@H]2O)[C@H](O)[C@@H](O)[C@H]1O',
                                     'name': 'Neurosporaside',
                                     'reason': 'No hydroperoxy groups found'},
                                 {   'smiles': '[O-]C(=O)C1=CN(C2CC2)C2=CC(N3CC[NH2+]CC3)=C(F)C=C2C1=O',
                                     'name': 'ciprofloxacin zwitterion',
                                     'reason': 'No hydroperoxy groups found'},
                                 {   'smiles': 'O=C1NC(=CC2=C1O[C@H]([C@@H](O)CC(C)C)O2)C',
                                     'name': 'Dihydroisoflavipucine',
                                     'reason': 'No hydroperoxy groups found'},
                                 {   'smiles': 'O=C1N2C(C(=O)N([C@@]2(OC)C)C[C@@H](O)C3=CC=CC=C3)=CC4=C1N(C=5C=CC=CC45)C',
                                     'name': 'Marinacarboline K',
                                     'reason': 'No hydroperoxy groups found'},
                                 {   'smiles': 'O1[C@@H](O[C@H]2[C@@H](O)[C@H](O)[C@H](O[C@@H]2OC[C@H]3OC(O)[C@@H](O)[C@@H](O)[C@@H]3O)CO)[C@H](NC(=O)C)[C@@H](O)[C@H](O[C@@H]4O[C@@H]([C@H](O)[C@H](O)[C@H]4O)CO[C@]5(O[C@H]([C@H](NC(=O)C)[C@@H](O)C5)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]1CO',
                                     'name': '(2R,4S,5R,6R)-5-Acetamido-2-[[(2R,3R,4S,5R,6S)-6-[(2R,3S,4R,5R,6S)-5-acetamido-6-[(2S,3S,4S,5S,6R)-4,5-dihydroxy-6-(hydroxymethyl)-2-[[(2R,3S,4S,5S)-3,4,5,6-tetrahydroxyoxan-2-yl]methoxy]oxan-3-yl]oxy-4-hydroxy-2-(hydroxymethyl)oxan-3-yl]oxy-3,4,5-trihydroxyoxan-2-yl]methoxy]-4-hydroxy-6-[(1R,2R)-1,2,3-trihydroxypropyl]oxane-2-carboxylic '
                                             'acid',
                                     'reason': 'No hydroperoxy groups found'},
                                 {   'smiles': 'O(C(=O)CCCCCCC)CCC1=CC=CC=C1',
                                     'name': '2-Phenylethyl octanoate',
                                     'reason': 'No hydroperoxy groups found'},
                                 {   'smiles': 'P(OCC(OC(=O)CCCCCCC/C=C\\CCCCCCCC)COC(=O)CCC/C=C\\C/C=C\\C/C=C\\CCCCCCCC)(OCCNC)(O)=O',
                                     'name': 'PE-NMe(20:3(5Z,8Z,11Z)/18:1(9Z))',
                                     'reason': 'No hydroperoxy groups found'},
                                 {   'smiles': 'O=C1C2=C(OC=3C1=CC=CN3)C(Cl)=CC(=C2)C=4NN=NN4',
                                     'name': 'traxanox',
                                     'reason': 'No hydroperoxy groups found'},
                                 {   'smiles': 'CCCCC(C)CCCCCC(C)CCCCCCCCCC(C)CC(O)=O',
                                     'name': '3,13,19-trimethyltricosanoic '
                                             'acid',
                                     'reason': 'No hydroperoxy groups found'},
                                 {   'smiles': 'COC(CC1=CC[C@]2(C)[C@@H](C)CCC[C@]2(C)C1=O)OC',
                                     'name': 'aignopsane ketal',
                                     'reason': 'No hydroperoxy groups found'}],
    'sample_false_negatives': [   {   'smiles': 'O1OC\\2CC1C(/C2=C/C(OO)CCCC(O)=O)C/C=C/CCCCC',
                                      'name': '5-hydroperoxy-7-[3,5-epidioxy-2-(2-octenyl)-cyclopentyl]-6-heptenoic '
                                              'acid',
                                      'reason': 'Multiple rings detected, '
                                                'uncharacteristic of typical '
                                                'lipid hydroperoxides'},
                                  {   'smiles': '[H]C(=CCCCCCCCCC(=O)OC)C1C2CC(OO2)C1C([H])=CC(CC)OO',
                                      'name': 'methyl '
                                              '8-[3,5-epidioxy-2-(3-hydroperoxy-1-pentenyl)-cyclopentyl]-octanoate',
                                      'reason': 'Multiple rings detected, '
                                                'uncharacteristic of typical '
                                                'lipid hydroperoxides'},
                                  {   'smiles': 'P(=O)(O)(OCCN)OC[C@@H](CO)OC(CCC/C=C\\C[C@H]1[C@@H]2C[C@H]([C@@H]1/C=C/[C@H](CCCCC)OO)OO2)=O',
                                      'name': '2-[(9S,11R)-epidioxy-(15S)-hydroperoxy-(5Z,13E)-prostadienoyl]-sn-glycero-3-phosphoethanolamine',
                                      'reason': 'Multiple rings detected, '
                                                'uncharacteristic of typical '
                                                'lipid hydroperoxides'},
                                  {   'smiles': '[C@@H]1([C@@H]2C[C@H]([C@@H]1/C=C/[C@H](C/C=C\\CC)OO)OO2)C/C=C\\CCCC(O)=O',
                                      'name': 'prostaglandin G3',
                                      'reason': 'Multiple rings detected, '
                                                'uncharacteristic of typical '
                                                'lipid hydroperoxides'},
                                  {   'smiles': 'CCCCC[C@H](OO)\\C=C\\[C@H]1[C@H]2C[C@H](OO2)[C@@H]1C\\C=C/CCCC(=O)OC(CO)CO',
                                      'name': 'prostaglandin G2 2-glyceryl '
                                              'ester',
                                      'reason': 'Multiple rings detected, '
                                                'uncharacteristic of typical '
                                                'lipid hydroperoxides'},
                                  {   'smiles': 'P(=O)([O-])(OCC[N+](C)(C)C)OC[C@@H](CO)OC(CCC/C=C\\C[C@H]1[C@@H]2C[C@H]([C@@H]1/C=C/[C@H](CCCCC)OO)OO2)=O',
                                      'name': '2-[(9S,11R)-epidioxy-(15S)-hydroperoxy-(5Z,13E)-prostadienoyl]-sn-glycero-3- '
                                              'phosphocholine',
                                      'reason': 'Charged species present, '
                                                'excluding for lipid '
                                                'hydroperoxide'}],
    'attempt': 1,
    'reasoning': 'To improve the classification accuracy of lipid '
                 'hydroperoxides, we need to address the false positives '
                 'identified in the previous analysis and enhance the '
                 'specificity of our structural checks. Below are the '
                 'potential issues and suggested improvements:\n'
                 '\n'
                 '1. **Negative Charges**: Some false positives included '
                 'molecules with charged groups, such as carboxylates ([O-]). '
                 'We should exclude molecules with such charges as they '
                 'deviate from the typical neutral lipid hydroperoxide '
                 'structure.\n'
                 '\n'
                 '2. **Complex Structures with Cyclic/Ester Elements**: '
                 'Molecules like "Argutin F" and cyclic esters were '
                 'incorrectly classified. These need exclusion by refining '
                 'structural criteria, perhaps considering only linear or '
                 'narrowly defined branched fatty acids-like structures.\n'
                 '\n'
                 '3. **Epoxides and Other Oxidized Functional Groups**: '
                 'Molecules with additional epoxide or other oxygen-containing '
                 'groups (e.g., epidioxygen bridges) were misclassified. '
                 'Adding specific pattern searches to exclude these could '
                 'improve specificity.\n'
                 '\n'
                 '4. **Count of Hydrogen Peroxy (-OOH) Groups**: We should '
                 'iterate the criteria for hydroperoxy group occurrence more '
                 'precisely, ensuring linear integration with fatty acid '
                 'chains or simple lipid backbones.\n'
                 '\n'
                 '5. **Minimum Carbon Count Refinement**: Previously, at least '
                 '12 carbon atoms were considered, but missed edge cases may '
                 'suggest increasing this threshold to better align with '
                 'observed lipid hydroperoxide structures, which often exhibit '
                 'longer chains typical to lipid classifications.\n'
                 '\n'
                 "Now, let's implement an improved version of the function:",
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 106,
    'num_false_positives': 21,
    'num_true_negatives': 142167,
    'num_false_negatives': 6,
    'num_negatives': None,
    'precision': 0.8346456692913385,
    'recall': 0.9464285714285714,
    'f1': 0.8870292887029287,
    'accuracy': 0.9998102600140548,
    'negative_predictive_value': 0.9999577978941149}