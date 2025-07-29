"""
Classifies: CHEBI:39418 straight-chain saturated fatty acid
"""
"""
Classifies: straight-chain saturated fatty acids
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_straight_chain_saturated_fatty_acid(smiles: str):
    """
    Determines if a molecule is a straight-chain saturated fatty acid based on its SMILES string.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a straight-chain saturated fatty acid, False otherwise
        str: Reason for classification
    """
    
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for carboxylic acid group
    carboxyl_pattern = Chem.MolFromSmarts("[CX3](=O)[OX2H1]")
    if not mol.HasSubstructMatch(carboxyl_pattern):
        return False, "No carboxylic acid group found"
    
    # Count carboxylic acid groups - should only have one
    carboxyl_matches = mol.GetSubstructMatches(carboxyl_pattern)
    if len(carboxyl_matches) > 1:
        return False, "Multiple carboxylic acid groups found"

    # Check for rings
    if rdMolDescriptors.CalcNumRings(mol) > 0:
        return False, "Contains cyclic structures"
        
    # Get the carboxylic acid carbon
    carboxyl_carbon = mol.GetAtomWithIdx(carboxyl_matches[0][0])
    
    # Traverse the carbon chain from the carboxylic group
    visited = set()
    current = carboxyl_carbon
    chain_length = 0
    
    while current is not None:
        visited.add(current.GetIdx())
        chain_length += 1
        
        # Find next carbon in chain
        next_carbon = None
        for neighbor in current.GetNeighbors():
            if neighbor.GetAtomicNum() == 6 and neighbor.GetIdx() not in visited:
                # Check for branching
                carbon_neighbors = sum(1 for n in neighbor.GetNeighbors() 
                                    if n.GetAtomicNum() == 6)
                if carbon_neighbors > 2:
                    return False, "Branched carbon chain detected"
                next_carbon = neighbor
                break
        current = next_carbon

    # Check minimum chain length (typically 4+ carbons for fatty acids)
    if chain_length < 4:
        return False, "Carbon chain too short for a fatty acid"

    # Check for unsaturation
    double_bond_pattern = Chem.MolFromSmarts("C=C")
    triple_bond_pattern = Chem.MolFromSmarts("C#C")
    if mol.HasSubstructMatch(double_bond_pattern):
        return False, "Contains double bonds (unsaturated)"
    if mol.HasSubstructMatch(triple_bond_pattern):
        return False, "Contains triple bonds (unsaturated)"

    # Check for non C,H,O atoms (excluding deuterium)
    for atom in mol.GetAtoms():
        atomic_num = atom.GetAtomicNum()
        if atomic_num not in [1, 6, 8]:
            if not (atomic_num == 1 and atom.GetIsotope() == 2):  # Allow deuterium
                return False, "Contains elements other than C, H, O (or deuterium)"

    # Check for ether linkages
    ether_pattern = Chem.MolFromSmarts("[CX4]-[OX2]-[CX4]")
    if mol.HasSubstructMatch(ether_pattern):
        return False, "Contains ether linkages"

    # Check for additional oxygen-containing groups
    for atom in mol.GetAtoms():
        if atom.GetAtomicNum() == 8:  # Oxygen atom
            # Skip the carboxylic acid oxygens
            if atom.GetIdx() not in [match[1] for match in carboxyl_matches] and \
               atom.GetIdx() not in [match[2] for match in carboxyl_matches]:
                return False, "Contains additional oxygen-containing groups"

    # All checks passed
    return True, "Straight-chain saturated fatty acid with single carboxylic acid group"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:39418',
                          'name': 'straight-chain saturated fatty acid',
                          'definition': 'Any saturated fatty acid lacking a '
                                        'side-chain.',
                          'parents': ['CHEBI:26607', 'CHEBI:59202'],
                          'xrefs': ['PMID:15644336'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': None,
    'message': '\n'
               'Attempt failed: F1 score of 0.31446540880503143 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: CCCCCC(O)=O NAME: hexanoic acid '
               'REASON: CORRECT Straight-chain saturated fatty acid with '
               'single carboxylic acid group\n'
               ' * SMILES: CCCCCCCCCCCCCC(O)=O NAME: tetradecanoic acid '
               'REASON: CORRECT Straight-chain saturated fatty acid with '
               'single carboxylic acid group\n'
               ' * SMILES: CCCCCCCCCCCCCCCCCCCCCCCCCC(O)=O NAME: hexacosanoic '
               'acid REASON: CORRECT Straight-chain saturated fatty acid with '
               'single carboxylic acid group\n'
               ' * SMILES: '
               '[2H]C([2H])([2H])C([2H])([2H])C([2H])([2H])C([2H])([2H])C([2H])([2H])C([2H])([2H])C([2H])([2H])C([2H])([2H])C([2H])([2H])C([2H])([2H])C([2H])([2H])C([2H])([2H])C([2H])([2H])C([2H])([2H])C([2H])([2H])C(O)=O '
               'NAME: palmitic acid-d31 REASON: CORRECT Straight-chain '
               'saturated fatty acid with single carboxylic acid group\n'
               ' * SMILES: CCCCC(O)=O NAME: valeric acid REASON: CORRECT '
               'Straight-chain saturated fatty acid with single carboxylic '
               'acid group\n'
               ' * SMILES: CCCCCCCC(O)=O NAME: octanoic acid REASON: CORRECT '
               'Straight-chain saturated fatty acid with single carboxylic '
               'acid group\n'
               ' * SMILES: C(CCCCCC)CCC(=O)O NAME: decanoic acid REASON: '
               'CORRECT Straight-chain saturated fatty acid with single '
               'carboxylic acid group\n'
               ' * SMILES: CCCCCCCCCCCCCCCCC(O)=O NAME: heptadecanoic acid '
               'REASON: CORRECT Straight-chain saturated fatty acid with '
               'single carboxylic acid group\n'
               ' * SMILES: CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC(O)=O NAME: '
               'dotriacontanoic acid REASON: CORRECT Straight-chain saturated '
               'fatty acid with single carboxylic acid group\n'
               ' * SMILES: CCCCCCCCCCCCCCCCCCC(O)=O NAME: nonadecanoic acid '
               'REASON: CORRECT Straight-chain saturated fatty acid with '
               'single carboxylic acid group\n'
               ' * SMILES: CCCCCCCCCCCCCCCCCCCCCC(O)=O NAME: docosanoic acid '
               'REASON: CORRECT Straight-chain saturated fatty acid with '
               'single carboxylic acid group\n'
               ' * SMILES: C(CCCCCCCCCCCCCCCC)CCCCCCCCCCC(O)=O NAME: '
               'octacosanoic acid REASON: CORRECT Straight-chain saturated '
               'fatty acid with single carboxylic acid group\n'
               ' * SMILES: CCCCCCCCCCCCCCCCCCCCCCCCCCCCC(O)=O NAME: '
               'nonacosanoic acid REASON: CORRECT Straight-chain saturated '
               'fatty acid with single carboxylic acid group\n'
               ' * SMILES: CCCC(O)=O NAME: butyric acid REASON: CORRECT '
               'Straight-chain saturated fatty acid with single carboxylic '
               'acid group\n'
               ' * SMILES: CCCCCCC(O)=O NAME: heptanoic acid REASON: CORRECT '
               'Straight-chain saturated fatty acid with single carboxylic '
               'acid group\n'
               ' * SMILES: CCCCCCCCCCCCC(O)=O NAME: tridecanoic acid REASON: '
               'CORRECT Straight-chain saturated fatty acid with single '
               'carboxylic acid group\n'
               ' * SMILES: CCCCCCCCCCCCCCCCCCCCCCCCCCCCCC(O)=O NAME: '
               'triacontanoic acid REASON: CORRECT Straight-chain saturated '
               'fatty acid with single carboxylic acid group\n'
               ' * SMILES: CCCCCCCCCCCCCCCCCCCC(O)=O NAME: icosanoic acid '
               'REASON: CORRECT Straight-chain saturated fatty acid with '
               'single carboxylic acid group\n'
               ' * SMILES: CCCCCCCCCCCCCCCCCCCCCCC(O)=O NAME: tricosanoic acid '
               'REASON: CORRECT Straight-chain saturated fatty acid with '
               'single carboxylic acid group\n'
               ' * SMILES: CCCCCCCCCCCCCCCCCCCCC(O)=O NAME: henicosanoic acid '
               'REASON: CORRECT Straight-chain saturated fatty acid with '
               'single carboxylic acid group\n'
               ' * SMILES: CCCCCCCCCCCC(O)=O NAME: dodecanoic acid REASON: '
               'CORRECT Straight-chain saturated fatty acid with single '
               'carboxylic acid group\n'
               ' * SMILES: CCCCCCCCCCCCCCCCCCCCCCCC(O)=O NAME: tetracosanoic '
               'acid REASON: CORRECT Straight-chain saturated fatty acid with '
               'single carboxylic acid group\n'
               ' * SMILES: '
               'C(C(C(C(C(C(C(C(C(C(C(C(C(C(=O)O)([2H])[2H])([2H])[2H])([2H])[2H])([2H])[2H])([2H])[2H])([2H])[2H])([2H])[2H])([2H])[2H])([2H])[2H])([2H])[2H])([2H])[2H])([2H])[2H])([2H])([2H])[2H] '
               'NAME: tetradecanoic-d27 acid REASON: CORRECT Straight-chain '
               'saturated fatty acid with single carboxylic acid group\n'
               ' * SMILES: CCCCCCCCCCCCCCCCCCCCCCCCCCC(O)=O NAME: '
               'heptacosanoic acid REASON: CORRECT Straight-chain saturated '
               'fatty acid with single carboxylic acid group\n'
               ' * SMILES: CCCCCCCCCCCCCCCC(O)=O NAME: hexadecanoic acid '
               'REASON: CORRECT Straight-chain saturated fatty acid with '
               'single carboxylic acid group\n'
               'False positives: SMILES: OC(=O)C1CCC(=O)O1 NAME: '
               '5-oxotetrahydrofuran-2-carboxylic acid REASON: WRONGLY '
               'CLASSIFIED Straight-chain saturated fatty acid with single '
               'carboxylic acid group\n'
               ' * SMILES: OC(=O)C(=O)CC=O NAME: Formylpyruvate REASON: '
               'WRONGLY CLASSIFIED Straight-chain saturated fatty acid with '
               'single carboxylic acid group\n'
               ' * SMILES: O(CCCC)CC(O)=O NAME: Butoxyacetic acid REASON: '
               'WRONGLY CLASSIFIED Straight-chain saturated fatty acid with '
               'single carboxylic acid group\n'
               ' * SMILES: OC(=O)CCCCCCCCCCCCCCCCC([2H])([2H])[2H] NAME: '
               'Stearic acid(d3) REASON: WRONGLY CLASSIFIED Straight-chain '
               'saturated fatty acid with single carboxylic acid group\n'
               ' * SMILES: CCCCCCCCCCCCCCCC(=O)OC(CCCCCCCC)CCCCCCCCC(O)=O '
               'NAME: 10-PAHSA REASON: WRONGLY CLASSIFIED Straight-chain '
               'saturated fatty acid with single carboxylic acid group\n'
               ' * SMILES: CCC(O)=O NAME: propionic acid REASON: WRONGLY '
               'CLASSIFIED Straight-chain saturated fatty acid with single '
               'carboxylic acid group\n'
               ' * SMILES: CCCCCCCCCCCCCCCC(=O)OC(CCCCCCC)CCCCCCCCCC(O)=O '
               'NAME: 11-PAHSA REASON: WRONGLY CLASSIFIED Straight-chain '
               'saturated fatty acid with single carboxylic acid group\n'
               ' * SMILES: OC(=O)COc1ccc(O)cc1 NAME: 4-Hydroxypheoxyacetate '
               'REASON: WRONGLY CLASSIFIED Straight-chain saturated fatty acid '
               'with single carboxylic acid group\n'
               ' * SMILES: [H]C(=O)CC(O)=O NAME: 3-oxopropanoic acid REASON: '
               'WRONGLY CLASSIFIED Straight-chain saturated fatty acid with '
               'single carboxylic acid group\n'
               ' * SMILES: O=C(O)C[C@@H](OC1=C(O)C(O)=CC=C1)C NAME: '
               '3-(2,3-Dihydroxyphenoxy)-butanoic acid REASON: WRONGLY '
               'CLASSIFIED Straight-chain saturated fatty acid with single '
               'carboxylic acid group\n'
               ' * SMILES: COCCOC(C)C(O)=O NAME: 2-(2-methoxyethoxy)propanoic '
               'acid REASON: WRONGLY CLASSIFIED Straight-chain saturated fatty '
               'acid with single carboxylic acid group\n'
               ' * SMILES: COC(=O)CCCC(O)=O NAME: monomethyl glutaric acid '
               'REASON: WRONGLY CLASSIFIED Straight-chain saturated fatty acid '
               'with single carboxylic acid group\n'
               ' * SMILES: OC(=O)CCCCCCCCCCCCCCCCCCCCCCCCCCCCCC NAME: '
               'Hentriacontanoic acid REASON: WRONGLY CLASSIFIED '
               'Straight-chain saturated fatty acid with single carboxylic '
               'acid group\n'
               ' * SMILES: O1C(CCCCCCCC(O)=O)=CC=C1 NAME: 2-furan-octanoic '
               'acid REASON: WRONGLY CLASSIFIED Straight-chain saturated fatty '
               'acid with single carboxylic acid group\n'
               ' * SMILES: O1C(CCCCCC)=CC=C1CCCCCC(O)=O NAME: '
               '5-Hexyl-2-furanhexanoic acid REASON: WRONGLY CLASSIFIED '
               'Straight-chain saturated fatty acid with single carboxylic '
               'acid group\n'
               ' * SMILES: CCCCCCCCC(=O)C(O)=O NAME: 2-oxodecanoic acid '
               'REASON: WRONGLY CLASSIFIED Straight-chain saturated fatty acid '
               'with single carboxylic acid group\n'
               ' * SMILES: CC(O)=O NAME: acetic acid REASON: WRONGLY '
               'CLASSIFIED Straight-chain saturated fatty acid with single '
               'carboxylic acid group\n'
               ' * SMILES: C(CCCCCCCC(C(=O)O)=O)CC NAME: 2-oxododecanoic acid '
               'REASON: WRONGLY CLASSIFIED Straight-chain saturated fatty acid '
               'with single carboxylic acid group\n'
               ' * SMILES: O1C(CCC1CCCCCC)CCCCCCCC(O)=O NAME: '
               '5-Hexyltetrahydro-2-furanoctanoic acid REASON: WRONGLY '
               'CLASSIFIED Straight-chain saturated fatty acid with single '
               'carboxylic acid group\n'
               ' * SMILES: O1C(CCC1=O)CC(O)=O NAME: 3-Hydroxyadipic acid '
               '3,6-lactone REASON: WRONGLY CLASSIFIED Straight-chain '
               'saturated fatty acid with single carboxylic acid group\n'
               ' * SMILES: CCCCCCCCC1OC1CCCCCCCC(O)=O NAME: '
               '9,10-epoxyoctadecanoic acid REASON: WRONGLY CLASSIFIED '
               'Straight-chain saturated fatty acid with single carboxylic '
               'acid group\n'
               ' * SMILES: OC(=O)C1=CC=CO1 NAME: 2-furoic acid REASON: WRONGLY '
               'CLASSIFIED Straight-chain saturated fatty acid with single '
               'carboxylic acid group\n'
               ' * SMILES: OC(=O)c1ccc(O)o1 NAME: 5-hydroxyfuran-2-carboxylic '
               'acid REASON: WRONGLY CLASSIFIED Straight-chain saturated fatty '
               'acid with single carboxylic acid group\n'
               ' * SMILES: O1C(CCCCCCCC(O)=O)=CC=C1CCCC NAME: '
               '5-Butyl-2-furanoctanoic acid REASON: WRONGLY CLASSIFIED '
               'Straight-chain saturated fatty acid with single carboxylic '
               'acid group\n'
               ' * SMILES: O(C(CCCCCCCCCCCC(O)=O)CCC)C(=O)CCCCCCCCCCCCCCC '
               'NAME: FAHFA(16:0/13-O-16:0) REASON: WRONGLY CLASSIFIED '
               'Straight-chain saturated fatty acid with single carboxylic '
               'acid group\n'
               'False negatives: SMILES: C(CCCCCCCCCCCCCCC(O)=O)CCC(C)O NAME: '
               '19-hydroxyicosanoic acid REASON: MISSED Contains hydroxyl '
               'groups on the carbon chain\n'
               ' * SMILES: OCCCCCCCCCC(O)=O NAME: 10-hydroxycapric acid '
               'REASON: MISSED Contains hydroxyl groups on the carbon chain\n'
               ' * SMILES: OC(C)CCCCCCCCCCCCCCCCCCC(=O)O NAME: '
               '20-hydroxyhenicosanoic acid REASON: MISSED Contains hydroxyl '
               'groups on the carbon chain\n'
               ' * SMILES: '
               'C(C[N+](C)(C)C)OP(=O)([O-])OC[C@H](OC)COC(CCCCCCCCCCCCCCC)=O '
               'NAME: 1-hexadecanoyl-2-methyl-sn-glycero-3-phosphocholine '
               'REASON: MISSED No carboxylic acid group found\n'
               ' * SMILES: CC(=O)CCC(O)=O NAME: 4-oxopentanoic acid REASON: '
               'MISSED Contains ketone groups\n'
               ' * SMILES: C[C@@H](O)CCCCCCCCCCCCCCCCCCC(O)=O NAME: '
               '(20R)-20-hydroxyhenicosanoic acid REASON: MISSED Contains '
               'hydroxyl groups on the carbon chain\n'
               ' * SMILES: OCCCCCCCCCCCCC(O)=O NAME: 13-hydroxytridecanoic '
               'acid REASON: MISSED Contains hydroxyl groups on the carbon '
               'chain\n'
               ' * SMILES: OCCCCCCCCCCCCCCC(O)=O NAME: 15-hydroxypentadecanoic '
               'acid REASON: MISSED Contains hydroxyl groups on the carbon '
               'chain\n'
               ' * SMILES: OCCCCCCCCCCCCCCCCCCCC(O)=O NAME: '
               '20-hydroxyicosanoic acid REASON: MISSED Contains hydroxyl '
               'groups on the carbon chain\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'CC(=O)O[C@H]1CC[C@]23C[C@@H]1OO[C@@]2(C)C(=O)CCC3(C)C',
                                     'name': 'Talaperoxide B',
                                     'reason': 'No carboxylic acid group '
                                               'found'},
                                 {   'smiles': 'C1=CC=C(C(=C1)C#CC2=CC=C(C=C2)[C@H]3[C@H](N[C@@H]3C#N)CO)F',
                                     'name': '(2S,3R,4S)-3-[4-[2-(2-fluorophenyl)ethynyl]phenyl]-4-(hydroxymethyl)-2-azetidinecarbonitrile',
                                     'reason': 'No carboxylic acid group '
                                               'found'},
                                 {   'smiles': 'OC(=O)Cc1cn(nc1-c1ccc(Cl)cc1)-c1ccccc1',
                                     'name': 'lonazolac',
                                     'reason': 'Contains cyclic structures'},
                                 {   'smiles': 'C(CCCCCCCC(=O)O)CCCCCCCCC(=O)O',
                                     'name': 'octadecanedioic acid',
                                     'reason': 'Multiple carboxylic acid '
                                               'groups found'},
                                 {   'smiles': 'O1[C@@H]([C@@H](O)[C@H](O)[C@@H](NC(=O)C)[C@@H]1OC[C@H]2OC(O)[C@H](O)[C@@H](O)[C@H]2O)CO[C@@H]3O[C@@H]([C@@H](O)[C@H](O)[C@H]3NC(=O)C)CO',
                                     'name': 'N-[(2R,3R,4R,5S,6R)-2-[[(2R,3S,4R,5R,6R)-5-Acetamido-3,4-dihydroxy-6-[[(2R,3R,4S,5R)-3,4,5,6-tetrahydroxyoxan-2-yl]methoxy]oxan-2-yl]methoxy]-4,5-dihydroxy-6-(hydroxymethyl)oxan-3-yl]acetamide',
                                     'reason': 'No carboxylic acid group '
                                               'found'},
                                 {   'smiles': 'C\\C=C(/C)CC\\C=C(/C)C(=O)OCC(C)(C)CC1=C(O)C(=O)c2ccccc2C1=O',
                                     'name': 'rhinacanthin C',
                                     'reason': 'No carboxylic acid group '
                                               'found'},
                                 {   'smiles': 'COC1=C(C=C2C(=C1)C(=NC=N2)NC3=CC(=C(C(=C3)Br)O)Br)OC',
                                     'name': '2,6-dibromo-4-[(6,7-dimethoxy-4-quinazolinyl)amino]phenol',
                                     'reason': 'No carboxylic acid group '
                                               'found'},
                                 {   'smiles': 'S(=O)(CC1=CC=CC=C1)C',
                                     'name': 'Methyl benzyl sulfoxide',
                                     'reason': 'No carboxylic acid group '
                                               'found'},
                                 {   'smiles': 'C=CCOC1=NS(=O)(=O)c2ccccc12',
                                     'name': 'probenazole',
                                     'reason': 'No carboxylic acid group '
                                               'found'},
                                 {   'smiles': 'C(=O)([C@@H](NC(=O)CC)CCSC)[O-]',
                                     'name': 'N-propanoyl-L-methioninate',
                                     'reason': 'No carboxylic acid group '
                                               'found'}],
    'sample_false_negatives': [   {   'smiles': 'C(CCCCCCCCCCCCCCC(O)=O)CCC(C)O',
                                      'name': '19-hydroxyicosanoic acid',
                                      'reason': 'Contains additional '
                                                'oxygen-containing groups'},
                                  {   'smiles': 'OCCCCCCCCCC(O)=O',
                                      'name': '10-hydroxycapric acid',
                                      'reason': 'Contains additional '
                                                'oxygen-containing groups'},
                                  {   'smiles': 'OC(C)CCCCCCCCCCCCCCCCCCC(=O)O',
                                      'name': '20-hydroxyhenicosanoic acid',
                                      'reason': 'Contains additional '
                                                'oxygen-containing groups'},
                                  {   'smiles': 'C(C[N+](C)(C)C)OP(=O)([O-])OC[C@H](OC)COC(CCCCCCCCCCCCCCC)=O',
                                      'name': '1-hexadecanoyl-2-methyl-sn-glycero-3-phosphocholine',
                                      'reason': 'No carboxylic acid group '
                                                'found'},
                                  {   'smiles': 'CC(=O)CCC(O)=O',
                                      'name': '4-oxopentanoic acid',
                                      'reason': 'Contains additional '
                                                'oxygen-containing groups'},
                                  {   'smiles': 'C[C@@H](O)CCCCCCCCCCCCCCCCCCC(O)=O',
                                      'name': '(20R)-20-hydroxyhenicosanoic '
                                              'acid',
                                      'reason': 'Contains additional '
                                                'oxygen-containing groups'},
                                  {   'smiles': 'OCCCCCCCCCCCCC(O)=O',
                                      'name': '13-hydroxytridecanoic acid',
                                      'reason': 'Contains additional '
                                                'oxygen-containing groups'},
                                  {   'smiles': 'OCCCCCCCCCCCCCCC(O)=O',
                                      'name': '15-hydroxypentadecanoic acid',
                                      'reason': 'Contains additional '
                                                'oxygen-containing groups'},
                                  {   'smiles': 'OCCCCCCCCCCCCCCCCCCCC(O)=O',
                                      'name': '20-hydroxyicosanoic acid',
                                      'reason': 'Contains additional '
                                                'oxygen-containing groups'}],
    'attempt': 1,
    'reasoning': 'Let me analyze the previous outcomes and suggest '
                 'improvements:\n'
                 '\n'
                 '1. Main Issues Identified:\n'
                 '- Many false positives for small molecules like acetic acid '
                 'and propionic acid\n'
                 '- False positives for molecules with ether linkages (like '
                 'butoxyacetic acid)\n'
                 '- False positives for cyclic compounds (like '
                 '5-oxotetrahydrofuran-2-carboxylic acid)\n'
                 '- False positives for molecules with additional functional '
                 'groups\n'
                 '\n'
                 '2. Key Improvements Needed:\n'
                 '- Add minimum chain length requirement (typically fatty '
                 'acids have 4+ carbons)\n'
                 '- Better detection of cyclic structures\n'
                 '- Better detection of ether linkages\n'
                 '- Ensure the carbon chain is continuous\n'
                 '- Improve detection of additional functional groups\n'
                 '\n'
                 "Here's my improved version:",
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 25,
    'num_false_positives': 10,
    'num_true_negatives': 142256,
    'num_false_negatives': 9,
    'num_negatives': None,
    'precision': 0.7142857142857143,
    'recall': 0.7352941176470589,
    'f1': 0.7246376811594202,
    'accuracy': 0.9998664792691497,
    'negative_predictive_value': 0.9999367377780902}