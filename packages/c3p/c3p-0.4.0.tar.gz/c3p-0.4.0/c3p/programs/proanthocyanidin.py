"""
Classifies: CHEBI:26267 proanthocyanidin
"""
"""
Classifies: proanthocyanidin
Definition: A flavonoid oligomer obtained by the condensation of two or more units of hydroxyflavans
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_proanthocyanidin(smiles: str):
    """
    Determines if a molecule is a proanthocyanidin based on its SMILES string.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a proanthocyanidin, False otherwise
        str: Reason for classification
    """
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Basic molecular properties
    num_atoms = mol.GetNumAtoms()
    if num_atoms < 20:  # Lowered threshold
        return False, "Too small to be a proanthocyanidin"

    # Count key atoms
    num_o = sum(1 for atom in mol.GetAtoms() if atom.GetAtomicNum() == 8)
    if num_o < 4:  # Lowered threshold
        return False, "Insufficient oxygen atoms"

    # Basic flavan unit patterns (more flexible)
    flavan_patterns = [
        # Basic flavan-3-ol core
        "[#6]1-[#6]-[#6]-c2c(O)cc(O)cc2O1",
        # Alternative pattern with different hydroxylation
        "[#6]1-[#6]-[#6]-c2c(O)cc(O)c(O)c2O1",
        # Pattern for gallated units
        "[#6]1-[#6]-[#6]-c2c(O)cc(O)cc2O[#6]1OC(=O)c1cc(O)c(O)c(O)c1"
    ]
    
    total_flavan_matches = 0
    for pattern in flavan_patterns:
        patt = Chem.MolFromSmarts(pattern)
        if patt:
            matches = len(mol.GetSubstructMatches(patt))
            total_flavan_matches += matches

    if total_flavan_matches < 1:
        return False, "No flavan unit found"

    # Check for characteristic linkage patterns
    linkage_patterns = [
        # 4→8 linkage
        "[#6]1-[#6]-[#6]-c2c(-[#6]1)cc(O)c1c2O[#6][#6][#6]c2cc(O)cc(O)c21",
        # 4→6 linkage
        "[#6]1-[#6]-[#6]-c2c(-[#6]1)cc(O)c(-[#6]1-[#6]-[#6]-c3c(-[#6]1)cc(O)cc3O)c2O",
        # 2→O→7 linkage (A-type)
        "[#6]1O[#6]2Oc3cc(O)cc(O)c3[#6][#6]2[#6][#6]1"
    ]
    
    has_linkage = False
    for pattern in linkage_patterns:
        patt = Chem.MolFromSmarts(pattern)
        if patt and mol.HasSubstructMatch(patt):
            has_linkage = True
            break

    # Check for characteristic hydroxylation patterns
    hydroxylation_patterns = [
        # A-ring patterns
        "Oc1cc(O)cc2c1",
        # B-ring patterns (including gallocatechin type)
        "c1c(O)c(O)ccc1",
        "c1c(O)c(O)c(O)cc1",
        # Gallate ester pattern
        "O=C(O)c1cc(O)c(O)c(O)c1"
    ]
    
    hydroxy_matches = 0
    for pattern in hydroxylation_patterns:
        patt = Chem.MolFromSmarts(pattern)
        if patt and mol.HasSubstructMatch(patt):
            hydroxy_matches += 1

    if hydroxy_matches < 2:
        return False, "Missing characteristic hydroxylation patterns"

    # Count aromatic rings
    ring_info = mol.GetRingInfo()
    aromatic_rings = sum(1 for ring in ring_info.AtomRings() 
                        if all(mol.GetAtomWithIdx(i).GetIsAromatic() for i in ring))
    
    if aromatic_rings < 2:  # Need at least one A-ring and one B-ring
        return False, "Insufficient aromatic rings"

    # Calculate molecular weight
    mol_wt = rdMolDescriptors.CalcExactMolWt(mol)
    if mol_wt < 400:  # Lowered threshold
        return False, "Molecular weight too low for proanthocyanidin"

    # Final classification
    if total_flavan_matches >= 2 or (total_flavan_matches >= 1 and has_linkage):
        return True, "Contains flavan units with characteristic linkages and hydroxylation patterns"
    else:
        return False, "Does not meet minimum structural requirements for proanthocyanidin"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:26267',
                          'name': 'proanthocyanidin',
                          'definition': 'A flavonoid oligomer obtained by the '
                                        'the condensation of two or more units '
                                        'of hydroxyflavans.',
                          'parents': ['CHEBI:26848', 'CHEBI:72720'],
                          'xrefs': ['Wikipedia:Proanthocyanidin'],
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
               'O[C@@H]1Cc2c(O)cc(O)c([C@H]3[C@H](OC(=O)c4cc(O)c(O)c(O)c4)[C@H](Oc4cc(O)cc(O)c34)c3ccc(O)c(O)c3)c2O[C@@H]1c1ccc(O)c(O)c1 '
               'NAME: procyanidin B4 3-O-gallate REASON: MISSED Need at least '
               'two flavan units\n'
               ' * SMILES: '
               'O[C@H]1[C@H](Oc2cc(O)cc(O)c2[C@@H]1c1c(O)cc(O)c2C[C@@H](OC(=O)c3cc(O)c(O)c(O)c3)[C@H](Oc12)c1cc(O)c(O)c(O)c1)c1cc(O)c(O)c(O)c1 '
               'NAME: epigallocatechin-(4beta->8)-epigallocatechin-3-O-gallate '
               'REASON: MISSED Need at least two flavan units\n'
               ' * SMILES: '
               'O[C@H]1Cc2c(O)cc(O)c([C@H]3[C@H](OC(=O)c4cc(O)c(O)c(O)c4)[C@H](Oc4cc(O)cc(O)c34)c3ccc(O)c(O)c3)c2O[C@@H]1c1ccc(O)c(O)c1 '
               'NAME: procyanidin B3 3-O-gallate REASON: MISSED Need at least '
               'two flavan units\n'
               ' * SMILES: '
               'COc1cc2oc3c(C)c(=O)cc4oc(cc(c2c2O[C@@H](CCc12)c1ccccc1)c34)-c1ccccc1 '
               'NAME: dracorubin REASON: MISSED Insufficient oxygen atoms for '
               'hydroxyl groups\n'
               ' * SMILES: '
               'O[C@@H]1Cc2c(O)cc(O)c([C@@H]3[C@@H](O)[C@H](Oc4c3c(O)cc(O)c4[C@@H]3[C@@H](O)[C@H](Oc4c3c(O)cc(O)c4[C@@H]3[C@@H](O)[C@H](Oc4c([C@@H]5[C@@H](O)[C@H](Oc6c([C@@H]7[C@@H](O)[C@H](Oc8cc(O)cc(O)c78)c7ccc(O)c(O)c7)c(O)cc(O)c56)c5ccc(O)c(O)c5)c(O)cc(O)c34)c3ccc(O)c(O)c3)c3ccc(O)c(O)c3)c3ccc(O)c(O)c3)c2O[C@@H]1c1ccc(O)c(O)c1 '
               'NAME: Cinnamtannin A4 REASON: MISSED Need at least two flavan '
               'units\n'
               ' * SMILES: '
               'O[C@@H]1Cc2c(O)cc(O)c([C@@H]3[C@@H](O)[C@H](Oc4c([C@@H]5[C@@H](O)[C@H](Oc6cc(O)cc(O)c56)c5ccc(O)c(O)c5)c(O)cc(O)c34)c3ccc(O)c(O)c3)c2O[C@@H]1c1ccc(O)c(O)c1 '
               'NAME: procyanidin C1 REASON: MISSED Need at least two flavan '
               'units\n'
               ' * SMILES: '
               'O[C@H]1Cc2c(O[C@@H]1c1ccc(O)c(O)c1)cc(O)c([C@H]1[C@H](O)[C@H](Oc3cc(O)cc(O)c13)c1ccc(O)c(O)c1)c2O '
               'NAME: procyanidin B6 REASON: MISSED Need at least two flavan '
               'units\n'
               ' * SMILES: '
               'O[C@H]1Cc2c(O)cc(O)c([C@@H]3[C@H](O)[C@H](Oc4cc(O)cc(O)c34)c3cc(O)c(O)c(O)c3)c2O[C@@H]1c1ccc(O)c(O)c1 '
               'NAME: (+)-gallocatechin-(4beta->8)-(+)-catechin REASON: MISSED '
               'Need at least two flavan units\n'
               ' * SMILES: '
               'COc1c(O)cc(cc1O)[C@H]1Oc2c(C[C@@H]1O)c(O)cc(O)c2[C@H]1[C@H](O)[C@H](Oc2cc(O)cc(O)c12)c1cc(O)c(OC)c(O)c1 '
               "NAME: (4alpha->8)-bis-4'-O-methylgallocatechin REASON: MISSED "
               'Need at least two flavan units\n'
               ' * SMILES: '
               'O[C@H]1Cc2c(O)cc(O)c([C@H]3[C@H](O)[C@H](Oc4cc(O)cc(O)c34)c3ccc(O)cc3)c2O[C@@H]1c1ccc(O)cc1 '
               'NAME: afzelechin-(4alpha->8)-afzelechin REASON: MISSED Need at '
               'least two flavan units\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'Cc1cc(C)c2Cc3c(C)cc(C)c(Cc4c(C)cc(C)c(Cc5c(C)cc(C)c(Cc1c2C)c5C)c4C)c3C',
                                     'name': '4,6,10,12,16,18,22,24,25,26,27,28-dodecamethylcalix[4]arene',
                                     'reason': 'Insufficient oxygen atoms'},
                                 {   'smiles': 'O=C1C(=C2C=C3[C@]([C@@H](C(C)C)[C@@H]([C@H]3O)OC(=O)C)(C)CC[C@]2(C)CC1)COC(=O)C',
                                     'name': 'Dahliane E',
                                     'reason': 'No flavan unit found'},
                                 {   'smiles': 'O[C@@H]([C@H](NC(=O)[C@@H](N)CCC(O)=O)C(=O)N[C@@H](CC(C)C)C(O)=O)C',
                                     'name': 'Glu-Thr-Leu',
                                     'reason': 'No flavan unit found'},
                                 {   'smiles': 'CCOc1ccc(NC(=O)C(C)O)cc1',
                                     'name': 'p-Lactophenetide',
                                     'reason': 'Too small to be a '
                                               'proanthocyanidin'},
                                 {   'smiles': 'O=C1NCC=2C1=C3C(N([C@@H]4O[C@H]([C@@H](O)[C@H]([C@H]4OC)O)C)C5=C3C=CC=C5)=C6NC7=C(C26)C=CC=C7',
                                     'name': "3'-epi-5'-methoxy-K252d",
                                     'reason': 'No flavan unit found'},
                                 {   'smiles': 'O=C(OC1C(O)C(OC(C1O)CO)OCC2OC(OCC(OC(=O)CCCCCCCCCCCCCCC)COC(=O)CCCCCCC/C=C\\C/C=C\\C/C=C\\CC)C(O)C(C2O)O)CCCCCCCCCCCCCCC',
                                     'name': '[(2S)-2-hexadecanoyloxy-3-[(2S,3R,4S,5S,6R)-6-[[(2S,3R,4S,5S,6R)-4-hexadecanoyloxy-3,5-dihydroxy-6-(hydroxymethyl)tetrahydropyran-2-yl]oxymethyl]-3,4,5-trihydroxy-tetrahydropyran-2-yl]oxy-propyl] '
                                             '(9E,12E,15E)-octadeca-9,12,15-trienoate',
                                     'reason': 'No flavan unit found'},
                                 {   'smiles': 'O=C1C2=C(O)C=C(OC)C=C2C(=O)C3=C1[C@@H]([C@@H](O)[C@]([C@@H]3O)(O)C)C',
                                     'name': 'Altersolanol G',
                                     'reason': 'No flavan unit found'},
                                 {   'smiles': '[H][C@]1(O[C@](O)(C[C@H](O)[C@H]1NC(=O)CO)C([O-])=O)[C@H](O)[C@H](O)CO',
                                     'name': 'N-glycoloyl-alpha-neuraminate',
                                     'reason': 'No flavan unit found'},
                                 {   'smiles': 'OC(C(O)C/C=C\\C/C=C\\C/C=C\\CC)C/C=C\\C/C=C\\CCC(O)=O',
                                     'name': '10,11-DiHDPE',
                                     'reason': 'No flavan unit found'},
                                 {   'smiles': '[Na+].[H][C@]12SCC(C)=C(N1C(=O)[C@H]2NC(=O)[C@H](N)c1ccccc1)C([O-])=O',
                                     'name': 'cephalexin sodium',
                                     'reason': 'No flavan unit found'}],
    'sample_false_negatives': [   {   'smiles': 'COc1cc2oc3c(C)c(=O)cc4oc(cc(c2c2O[C@@H](CCc12)c1ccccc1)c34)-c1ccccc1',
                                      'name': 'dracorubin',
                                      'reason': 'No flavan unit found'},
                                  {   'smiles': 'O[C@@H]1Cc2c(O)cc(O)c([C@@H]3[C@@H](O)[C@H](Oc4c3c(O)cc(O)c4[C@@H]3[C@@H](O)[C@H](Oc4c3c(O)cc(O)c4[C@@H]3[C@@H](O)[C@H](Oc4c([C@@H]5[C@@H](O)[C@H](Oc6c([C@@H]7[C@@H](O)[C@H](Oc8cc(O)cc(O)c78)c7ccc(O)c(O)c7)c(O)cc(O)c56)c5ccc(O)c(O)c5)c(O)cc(O)c34)c3ccc(O)c(O)c3)c3ccc(O)c(O)c3)c3ccc(O)c(O)c3)c2O[C@@H]1c1ccc(O)c(O)c1',
                                      'name': 'Cinnamtannin A4',
                                      'reason': 'Missing characteristic '
                                                'hydroxylation patterns'},
                                  {   'smiles': 'O[C@@H]1Cc2c(O)cc(O)c([C@@H]3[C@@H](O)[C@H](Oc4c([C@@H]5[C@@H](O)[C@H](Oc6cc(O)cc(O)c56)c5ccc(O)c(O)c5)c(O)cc(O)c34)c3ccc(O)c(O)c3)c2O[C@@H]1c1ccc(O)c(O)c1',
                                      'name': 'procyanidin C1',
                                      'reason': 'Missing characteristic '
                                                'hydroxylation patterns'},
                                  {   'smiles': 'O[C@H]1Cc2c(O[C@@H]1c1ccc(O)c(O)c1)cc(O)c([C@H]1[C@H](O)[C@H](Oc3cc(O)cc(O)c13)c1ccc(O)c(O)c1)c2O',
                                      'name': 'procyanidin B6',
                                      'reason': 'Missing characteristic '
                                                'hydroxylation patterns'},
                                  {   'smiles': 'O[C@H]1Cc2c(O)cc(O)c([C@H]3[C@H](O)[C@H](Oc4cc(O)cc(O)c34)c3ccc(O)cc3)c2O[C@@H]1c1ccc(O)cc1',
                                      'name': 'afzelechin-(4alpha->8)-afzelechin',
                                      'reason': 'Missing characteristic '
                                                'hydroxylation patterns'},
                                  {   'smiles': 'O[C@@H]1Cc2c(O[C@@H]1c1ccc(O)c(O)c1)cc(O)c([C@@H]1[C@@H](O)[C@H](Oc3cc(O)cc(O)c13)c1ccc(O)c(O)c1)c2O',
                                      'name': 'procyanidin B5',
                                      'reason': 'Missing characteristic '
                                                'hydroxylation patterns'},
                                  {   'smiles': 'O[C@@H]1Cc2c(O[C@@H]1c1ccc(O)c(O)c1)cc(O)c([C@H]1[C@H](O)[C@H](Oc3cc(O)cc(O)c13)c1ccc(O)c(O)c1)c2O',
                                      'name': 'procyanidin B8',
                                      'reason': 'Missing characteristic '
                                                'hydroxylation patterns'},
                                  {   'smiles': 'O[C@@H]1Cc2c(O)cc(O)c([C@@H]3[C@@H](O)[C@H](Oc4cc(O)cc(O)c34)c3ccc(O)c(O)c3)c2O[C@@H]1c1ccc(O)c(O)c1',
                                      'name': 'procyanidin B2',
                                      'reason': 'Missing characteristic '
                                                'hydroxylation patterns'},
                                  {   'smiles': 'O[C@H]1Cc2c(O)c([C@H]3[C@H](O)[C@H](Oc4cc(O)ccc34)c3cc(O)c(O)c(O)c3)c(O)c([C@H]3[C@H](O)[C@H](Oc4cc(O)ccc34)c3cc(O)c(O)c(O)c3)c2O[C@@H]1c1ccc(O)c(O)c1',
                                      'name': 'Robinetinidol-(4alpha->8)-catechin-(6->4alpha)-robinetinidol',
                                      'reason': 'Does not meet minimum '
                                                'structural requirements for '
                                                'proanthocyanidin'},
                                  {   'smiles': 'O[C@@H]1Cc2c(O)cc(O)c([C@@H]3[C@@H](O)[C@H](Oc4c3c(O)cc(O)c4[C@@H]3[C@@H](O)[C@H](Oc4c([C@@H]5[C@@H](O)[C@H](Oc6c([C@@H]7[C@@H](O)[C@H](Oc8cc(O)cc(O)c78)c7ccc(O)c(O)c7)c(O)cc(O)c56)c5ccc(O)c(O)c5)c(O)cc(O)c34)c3ccc(O)c(O)c3)c3ccc(O)c(O)c3)c2O[C@@H]1c1ccc(O)c(O)c1',
                                      'name': 'Cinnamtannin A3',
                                      'reason': 'Missing characteristic '
                                                'hydroxylation patterns'}],
    'attempt': 2,
    'reasoning': 'Let me analyze the previous attempt and suggest '
                 'improvements:\n'
                 '\n'
                 '1. The main issue seems to be that the code was too '
                 'restrictive and missed many valid proanthocyanidins. Looking '
                 'at the false negatives, we can see several patterns:\n'
                 '\n'
                 '2. Key observations from failed cases:\n'
                 '- Many structures contain gallate esters (e.g., procyanidin '
                 'B4 3-O-gallate) which were not properly accounted for\n'
                 '- The SMARTS patterns for flavan units and linkages were too '
                 'rigid\n'
                 "- The code didn't properly handle variations in the "
                 'hydroxylation patterns\n'
                 '- Some valid structures were rejected due to overly strict '
                 'ring counting\n'
                 '\n'
                 '3. Improvements needed:\n'
                 '- Make the flavan unit detection more flexible to account '
                 'for variations\n'
                 '- Add patterns for gallate esters\n'
                 '- Relax some of the numerical thresholds\n'
                 '- Better handle different types of interflavanoid linkages '
                 '(4→8, 4→6, and 2→O→7)\n'
                 '- Account for different hydroxylation patterns in the A and '
                 'B rings\n'
                 '\n'
                 "Here's my improved version:",
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 22,
    'num_false_positives': 26,
    'num_true_negatives': 142228,
    'num_false_negatives': 24,
    'num_negatives': None,
    'precision': 0.4583333333333333,
    'recall': 0.4782608695652174,
    'f1': 0.4680851063829787,
    'accuracy': 0.999648629655657,
    'negative_predictive_value': 0.9998312853246352}