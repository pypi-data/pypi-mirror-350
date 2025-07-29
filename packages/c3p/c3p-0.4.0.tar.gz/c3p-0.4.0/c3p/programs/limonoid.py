"""
Classifies: CHEBI:39434 limonoid
"""
from rdkit import Chem
from rdkit.Chem import rdMolDescriptors

def is_limonoid(smiles: str):
    """
    Determines if a molecule is a limonoid based on its SMILES string.
    A limonoid is a triterpenoid that is highly oxygenated and has a prototypical structure
    containing or derived from a 4,4,8-trimethyl-17-furanylsteroid skeleton.
    
    Args:
        smiles (str): SMILES string of the molecule
    
    Returns:
        bool: True if molecule is a limonoid, False otherwise
        str: Reason for classification
    """

    # Parse the SMILES string
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Step 1: Check for at least four rings
    ri = mol.GetRingInfo()
    num_rings = ri.NumRings()
    if num_rings < 4:
        return False, f"Only {num_rings} rings found, need at least 4 rings"

    # Step 2: Check for furan ring
    furan_pattern = Chem.MolFromSmarts('c1ccoc1')
    furan_matches = mol.GetSubstructMatches(furan_pattern)
    if not furan_matches:
        return False, "No furan ring found in molecule"

    # Step 3: Check if furan ring is connected to the ring system
    ring_atom_indices = set()
    for ring in ri.AtomRings():
        ring_atom_indices.update(ring)
    furan_atom_indices = set()
    for match in furan_matches:
        furan_atom_indices.update(match)
    # Find if any atom in the furan ring is connected to any atom in the other rings
    connected = False
    for idx in furan_atom_indices:
        atom = mol.GetAtomWithIdx(idx)
        for neighbor in atom.GetNeighbors():
            if neighbor.GetIdx() in ring_atom_indices and neighbor.GetIdx() not in furan_atom_indices:
                connected = True
                break
        if connected:
            break
    if not connected:
        return False, "Furan ring is not connected to the core ring system"

    # Step 4: Check for high oxygenation (e.g., at least 6 oxygen atoms)
    o_count = sum(1 for atom in mol.GetAtoms() if atom.GetAtomicNum() == 8)
    if o_count < 6:
        return False, f"Not highly oxygenated, only {o_count} oxygen atoms found"

    # Step 5: Check for multiple methyl groups attached to ring carbons
    # Count methyl groups attached to ring carbons
    methyl_count = 0
    for atom in mol.GetAtoms():
        if atom.GetAtomicNum() == 6 and atom.GetDegree() == 1:
            neighbor = atom.GetNeighbors()[0]
            if neighbor.IsInRing():
                methyl_count += 1
    if methyl_count < 3:
        return False, f"Only {methyl_count} methyl groups attached to ring carbons, need at least 3"

    # Step 6: Check for triterpenoid skeleton by counting carbon atoms
    # Triterpenoids typically have around 30 carbon atoms
    c_count = sum(1 for atom in mol.GetAtoms() if atom.GetAtomicNum() == 6)
    if c_count < 25:
        return False, f"Only {c_count} carbon atoms found, likely not a triterpenoid"

    return True, "Molecule is classified as a limonoid"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:39434',
                          'name': 'limonoid',
                          'definition': 'Any triterpenoid that is highly '
                                        'oxygenated and has a prototypical '
                                        'structure either containing or '
                                        'derived from a precursor with a '
                                        '4,4,8-trimethyl-17-furanylsteroid '
                                        "skeleton. The term 'limonoid' comes "
                                        'from limonin, the first '
                                        'tetranortriterpenoid obtained from '
                                        'citrus bitter principles.',
                          'parents': ['CHEBI:36615'],
                          'xrefs': ['PMID:16462017', 'Wikipedia:Limonoid'],
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
               'COC(=O)\\C=C/[C@]1(C)[C@H]2CC[C@@]3(C)[C@@H](OC(=O)[C@H]4O[C@@]34[C@]2(C)[C@]2(O)OC(C)(C)C(=O)[C@]12O)c1ccoc1 '
               'NAME: Harrisonin REASON: MISSED Does not contain fused 6-6-6-5 '
               'ring system\n'
               ' * SMILES: '
               'COC(=O)C[C@H]1[C@@]2(C)C[C@@]3(OC(C)=O)[C@]1(C)[C@H]1CC[C@@]4(C)[C@@H](OC(=O)[C@H](O)C4=C1[C@H](OC(C)=O)[C@@]3(OC(C)=O)[C@H]2OC(=O)C(\\C)=C\\C)c1ccoc1 '
               'NAME: trichagmalin E REASON: MISSED Rings are not properly '
               'fused like steroid nucleus\n'
               ' * SMILES: '
               'CC(=O)O[C@@H]1C[C@H]2C(C)(C)C(=O)C=C[C@]2(C)[C@H]2CC[C@]3(C)OC(=O)C=C3[C@]12C '
               'NAME: beta-nimolactone REASON: MISSED Rings are not properly '
               'fused like steroid nucleus\n'
               ' * SMILES: '
               'CC(=O)O[C@H]1[C@@H]2CC3=C4CC(=O)O[C@H]([C@@]4(CCC3[C@@](C2=O)([C@H](C1(C)C)CC(=O)OC)C)C)C5=COC=C5 '
               'NAME: LSM-4386 REASON: MISSED Rings are not properly fused '
               'like steroid nucleus\n'
               ' * SMILES: '
               'O1[C@@]23[C@]([C@@H](C[C@@]12[H])C=4C=COC4)(CC[C@]5([C@]3(C(=O)C(O)=C6[C@]5(C)C=CC(=O)C6(C)C)C)[H])C '
               'NAME: CEDRELONE REASON: MISSED Rings are not properly fused '
               'like steroid nucleus\n'
               ' * SMILES: '
               'CCC(C)C(=O)O[C@H]1C[C@@H](OC(C)=O)[C@@]2(C)CO[C@H]3[C@H]4O[C@@H]5C[C@@H](c6ccoc6)C(C)=C5[C@@]4(C)[C@H](CC(=O)OC)[C@]1(C)[C@H]23 '
               "NAME: 2',3'-dihydrosalannin REASON: MISSED Does not contain "
               'fused 6-6-6-5 ring system\n'
               ' * SMILES: '
               'CC(=O)O[C@@H]1C[C@H]2C(C)(C)C(=O)C=C[C@]2(C)[C@H]2CC[C@@]3(C)[C@@H](C(=O)[C@H]4O[C@@]34[C@]12C)c1ccoc1 '
               'NAME: epoxyazadiradione REASON: MISSED Rings are not properly '
               'fused like steroid nucleus\n'
               ' * SMILES: '
               'CO[C@H]1C[C@@]2(O)[C@@H](O1)O[C@H]1C[C@@H]2[C@]2(C)O[C@]12[C@@]1(C)[C@@H]2[C@](O)(OC[C@]22[C@H]3[C@@H](OC[C@@]3([C@@H](C[C@@H]2OC(=O)C(\\C)=C\\C)OC(C)=O)C(=O)OC)[C@H]1O)C(=O)OC '
               'NAME: 23-epivepaol REASON: MISSED Rings are not properly fused '
               'like steroid nucleus\n'
               ' * SMILES: '
               '[H][C@@]12C[C@@H](c3ccoc3)[C@]3(C)[C@@H](O)C(=O)[C@@]4([H])[C@@](C)([C@H](O)C[C@@]5([H])[C@@]6(C)[C@@H](OC[C@@]45[C@@H](O)[C@@H](OC(C)=O)[C@H]6OC(C)=O)OC(=O)C(C)C)[C@@]13O2 '
               'NAME: 12-O-deacetyltrichilin H REASON: MISSED Rings are not '
               'properly fused like steroid nucleus\n'
               ' * SMILES: '
               '[H][C@@]12OC=C[C@]1(O)[C@@H]1C[C@H](O2)[C@]2(O[C@@]12C)[C@]1(C)[C@H](O)[C@@H]2OC[C@@]3([C@@H](C[C@@H](OC(=O)C(\\C)=C\\C)[C@@]4(CO[C@](O)(C(=O)OC)[C@@]14[H])[C@@]23[H])OC(C)=O)C(=O)OC '
               'NAME: azadirachtin B REASON: MISSED Rings are not properly '
               'fused like steroid nucleus\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'CNC(=O)CC[C@H](N)C(O)=O',
                                     'name': 'N(5)-methyl-L-glutamine',
                                     'reason': 'Only 0 rings found, need at '
                                               'least 4 rings'},
                                 {   'smiles': 'C[C@H](OP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1O)n1cnc2c1nc(N)[nH]c2=O)C(O)=O',
                                     'name': "L-lactyl-2-diphospho-5'-guanosine",
                                     'reason': 'Only 3 rings found, need at '
                                               'least 4 rings'},
                                 {   'smiles': '[H][C@@]1(CC[C@]2(C)[C@]1([H])CC[C@]1([H])[C@@]3(C)CCCC(C)(C)[C@]3([H])CC[C@@]21C)C(=C)CCC=C(C)C',
                                     'name': 'dammara-20,24-diene',
                                     'reason': 'No furan ring found in '
                                               'molecule'},
                                 {   'smiles': 'O=C1C2=C(O)C3=C(O)C=CC=C3C(=C2C(C(=O)C)C(C1)(O)C)C=4C=5C(C(O)=C6C4C(C(=O)C)C(O)(C)CC6=O)=C(O)C=CC5',
                                     'name': 'A 39183A',
                                     'reason': 'No furan ring found in '
                                               'molecule'},
                                 {   'smiles': 'C[C@H](O)[C@@H](O)C1=Nc2c(NC1)[nH]c(N)nc2=O',
                                     'name': 'L-threo-7,8-dihydrobiopterin',
                                     'reason': 'Only 2 rings found, need at '
                                               'least 4 rings'},
                                 {   'smiles': 'C[C@@H]1CN([C@H](COC2=C(C=C(C=C2)NC(=O)C)C(=O)N(C[C@H]1OC)C)C)CC3=CC=C(C=C3)F',
                                     'name': 'N-[(4S,7R,8S)-5-[(4-fluorophenyl)methyl]-8-methoxy-4,7,10-trimethyl-11-oxo-2-oxa-5,10-diazabicyclo[10.4.0]hexadeca-1(12),13,15-trien-14-yl]acetamide',
                                     'reason': 'Only 3 rings found, need at '
                                               'least 4 rings'},
                                 {   'smiles': 'C(CCN1CCCCC1)(CCN(C(C)C)C(C)=O)(C(N)=O)C2=C(Cl)C=CC=C2',
                                     'name': 'bidisomide',
                                     'reason': 'Only 2 rings found, need at '
                                               'least 4 rings'},
                                 {   'smiles': 'OCCCCCCCCCCC#CC=C',
                                     'name': '13-Tetradece-11-yn-1-ol',
                                     'reason': 'Only 0 rings found, need at '
                                               'least 4 rings'},
                                 {   'smiles': 'C[C@@H]1CCCCO[C@@H]([C@@H](CN(C(=O)C2=C(O1)C=CC(=C2)N(C)C)[C@@H](C)CO)C)CN(C)CC3=CC=C(C=C3)OC',
                                     'name': '(3R,9S,10R)-16-(dimethylamino)-12-[(2S)-1-hydroxypropan-2-yl]-9-[[(4-methoxyphenyl)methyl-methylamino]methyl]-3,10-dimethyl-2,8-dioxa-12-azabicyclo[12.4.0]octadeca-1(14),15,17-trien-13-one',
                                     'reason': 'Only 3 rings found, need at '
                                               'least 4 rings'},
                                 {   'smiles': 'O(CCC12CC3CC(C1)CC(C2)C3)C(=O)CC4=CC=C(OCC(O)CNC(C)C)C=C4',
                                     'name': 'Adaprolol',
                                     'reason': 'No furan ring found in '
                                               'molecule'}],
    'sample_false_negatives': [   {   'smiles': 'CC(=O)O[C@@H]1C[C@H]2C(C)(C)C(=O)C=C[C@]2(C)[C@H]2CC[C@]3(C)OC(=O)C=C3[C@]12C',
                                      'name': 'beta-nimolactone',
                                      'reason': 'No furan ring found in '
                                                'molecule'},
                                  {   'smiles': 'O1[C@@]23[C@]([C@@H](C[C@@]12[H])C=4C=COC4)(CC[C@]5([C@]3(C(=O)C(O)=C6[C@]5(C)C=CC(=O)C6(C)C)C)[H])C',
                                      'name': 'CEDRELONE',
                                      'reason': 'Not highly oxygenated, only 5 '
                                                'oxygen atoms found'},
                                  {   'smiles': 'CO[C@H]1C[C@@]2(O)[C@@H](O1)O[C@H]1C[C@@H]2[C@]2(C)O[C@]12[C@@]1(C)[C@@H]2[C@](O)(OC[C@]22[C@H]3[C@@H](OC[C@@]3([C@@H](C[C@@H]2OC(=O)C(\\C)=C\\C)OC(C)=O)C(=O)OC)[C@H]1O)C(=O)OC',
                                      'name': '23-epivepaol',
                                      'reason': 'No furan ring found in '
                                                'molecule'},
                                  {   'smiles': '[H][C@@]12OC=C[C@]1(O)[C@@H]1C[C@H](O2)[C@]2(O[C@@]12C)[C@]1(C)[C@H](O)[C@@H]2OC[C@@]3([C@@H](C[C@@H](OC(=O)C(\\C)=C\\C)[C@@]4(CO[C@](O)(C(=O)OC)[C@@]14[H])[C@@]23[H])OC(C)=O)C(=O)OC',
                                      'name': 'azadirachtin B',
                                      'reason': 'No furan ring found in '
                                                'molecule'},
                                  {   'smiles': 'CC(=O)O[C@@H]1C[C@H]2C(C)(C)C(=O)C=C[C@]2(C)[C@H]2CC[C@@]3(C)OC(=O)C=C3[C@]12C',
                                      'name': 'alpha-nimolactone',
                                      'reason': 'No furan ring found in '
                                                'molecule'},
                                  {   'smiles': '[H][C@@]12OC=C[C@]1(O)[C@@H]1C[C@H](O2)[C@]2(O[C@@]12C)[C@]1(C)[C@H](O)[C@@H]2OC[C@@]3([C@@H](C[C@H](OC(=O)C(\\C)=C\\C)[C@@]4(CO[C@](O)(C(=O)OC)[C@@]14[H])[C@@]23[H])OC(C)=O)C(=O)OC',
                                      'name': 'azadirachtin A',
                                      'reason': 'No furan ring found in '
                                                'molecule'},
                                  {   'smiles': '[H][C@@]1(CC(O)=O)OC(C)(C)[C@]2([H])CC(=O)[C@]3(C)[C@]([H])(CC[C@@](C)([C@@H](O)c4ccoc4)[C@@]33O[C@@H]3C(O)=O)[C@@]12CO',
                                      'name': 'limonoic acid',
                                      'reason': 'Furan ring is not connected '
                                                'to the core ring system'},
                                  {   'smiles': 'CC(=O)O[C@@H]1C[C@H]2C(C)(C)C(=O)C=C[C@]2(C)[C@H]2CC[C@]3(C)[C@@H](C(=O)C=C3[C@]12C)C1=CCOC1=O',
                                      'name': 'azadiradionolide',
                                      'reason': 'No furan ring found in '
                                                'molecule'},
                                  {   'smiles': 'CC(=O)O[C@@H]1C[C@H]2C(C)(C)C(=O)C=C[C@]2(C)[C@H]2CC[C@@]3(C)[C@@H](C(=O)C=C3[C@]12C)c1ccoc1',
                                      'name': 'azadiradione',
                                      'reason': 'Not highly oxygenated, only 5 '
                                                'oxygen atoms found'},
                                  {   'smiles': 'COC(=O)C[C@H]1[C@@]2(C)[C@H](O[C@@H]3CC(=O)C(C)=C23)[C@@H]2OC[C@@]3(C)[C@H]2[C@]1(C)[C@H](C[C@H]3OC(C)=O)OC(=O)C(\\C)=C\\C',
                                      'name': '17-defurano-17-oxosalannin',
                                      'reason': 'No furan ring found in '
                                                'molecule'}],
    'attempt': 3,
    'reasoning': 'Upon reviewing the previous program and the outcomes, it '
                 'appears that the function is failing to correctly identify '
                 'limonoids due to overly strict or incorrect assumptions '
                 'about their structural features.\n'
                 '\n'
                 '**Issues noted:**\n'
                 '\n'
                 '1. **Detection of the fused ring system**: The code checks '
                 'specifically for a fused 6-6-6-5 ring system similar to a '
                 'steroid nucleus. However, limonoids can have variations in '
                 'their ring systems, and some may not strictly adhere to this '
                 'pattern. This may cause valid limonoids to be missed.\n'
                 '\n'
                 '2. **Ring Fusion Checks**: The method used to determine if '
                 'rings are properly fused may not accurately capture the '
                 'complex ring fusions present in limonoids. Simply counting '
                 'shared atoms between rings may not be sufficient.\n'
                 '\n'
                 '3. **Methyl Substitutions**: The code counts methyl groups '
                 'attached to quaternary carbons (degree 4) in the ring '
                 'system. However, methyl groups in limonoids can be attached '
                 'to tertiary carbons or in different arrangements, leading to '
                 'undercounting.\n'
                 '\n'
                 '4. **Furan Ring Connectivity**: The way the code checks for '
                 'the furan ring being connected to the ring system may not '
                 'account for all possible connectivity patterns present in '
                 'limonoids.\n'
                 '\n'
                 'To improve the program, we can:\n'
                 '\n'
                 '- **Relax strict structural checks** to account for the '
                 'variability in limonoid structures.\n'
                 '- **Use SMARTS patterns** to more accurately identify key '
                 'substructures like the furan ring and triterpenoid '
                 'skeleton.\n'
                 '- **Adjust the methyl group counting** to include methyl '
                 'groups attached to ring carbons regardless of their degree.\n'
                 '- **Ensure that the furan ring connectivity** is checked in '
                 'a way that captures more possible linkages to the core ring '
                 'system.\n'
                 '- **Check for high oxygenation** by setting a reasonable '
                 'threshold for the number of oxygen atoms.\n'
                 '\n'
                 'By making these changes, the function should better identify '
                 'limonoids, including the provided examples.',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 58,
    'num_false_positives': 51,
    'num_true_negatives': 142162,
    'num_false_negatives': 29,
    'num_negatives': None,
    'precision': 0.5321100917431193,
    'recall': 0.6666666666666666,
    'f1': 0.5918367346938775,
    'accuracy': 0.9994378074490513,
    'negative_predictive_value': 0.9997960489763769}