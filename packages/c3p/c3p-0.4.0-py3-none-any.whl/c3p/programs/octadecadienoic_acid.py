"""
Classifies: CHEBI:25627 octadecadienoic acid
"""
"""
Classifies: octadecadienoic acid
Definition: Any straight-chain, C18 polyunsaturated fatty acid having two C=C double bonds
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def get_main_chain(mol, carboxyl_carbon):
    """Helper function to find the main carbon chain starting from carboxyl group"""
    visited = set()
    best_chain = []
    
    def dfs(atom, current_chain):
        nonlocal best_chain
        visited.add(atom.GetIdx())
        current_chain.append(atom.GetIdx())
        
        # If this chain is longer than our best chain, update best chain
        if len(current_chain) > len(best_chain):
            best_chain = current_chain[:]
            
        # Explore neighbors
        for bond in atom.GetBonds():
            next_atom = bond.GetOtherAtom(atom)
            if next_atom.GetIdx() not in visited and next_atom.GetAtomicNum() == 6:
                dfs(next_atom, current_chain)
                
        visited.remove(atom.GetIdx())
        current_chain.pop()
    
    start_atom = mol.GetAtomWithIdx(carboxyl_carbon)
    dfs(start_atom, [])
    return best_chain

def is_octadecadienoic_acid(smiles: str):
    """
    Determines if a molecule is an octadecadienoic acid based on its SMILES string.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is an octadecadienoic acid, False otherwise
        str: Reason for classification
    """
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
    
    # Check for allowed atoms (C, H, O only)
    for atom in mol.GetAtoms():
        if atom.GetAtomicNum() not in {1, 6, 8}:
            return False, "Contains atoms other than C, H, and O"
    
    # Check for carboxylic acid group
    carboxyl_pattern = Chem.MolFromSmarts("[CX3](=[OX1])[OX2H1]")
    if not mol.HasSubstructMatch(carboxyl_pattern):
        return False, "No carboxylic acid group found"
    
    carboxyl_matches = mol.GetSubstructMatches(carboxyl_pattern)
    carboxyl_carbon = carboxyl_matches[0][0]
    
    # Get main chain
    main_chain = get_main_chain(mol, carboxyl_carbon)
    
    # Verify chain length
    if len(main_chain) != 18:
        return False, f"Main chain has {len(main_chain)} carbons, must be exactly 18"
    
    # Create a submolecule containing only the main chain
    chain_atoms = set(main_chain)
    chain_bonds = set()
    for bond in mol.GetBonds():
        if bond.GetBeginAtomIdx() in chain_atoms and bond.GetEndAtomIdx() in chain_atoms:
            chain_bonds.add(bond.GetIdx())
    
    # Count double bonds in main chain
    double_bond_count = 0
    for bond_idx in chain_bonds:
        bond = mol.GetBondWithIdx(bond_idx)
        if bond.GetBondType() == Chem.BondType.DOUBLE:
            double_bond_count += 1
    
    if double_bond_count != 2:
        return False, f"Contains {double_bond_count} C=C double bonds in main chain, must be exactly 2"
    
    # Check for branching in main chain
    for atom_idx in main_chain:
        atom = mol.GetAtomWithIdx(atom_idx)
        non_h_neighbors = [n for n in atom.GetNeighbors() if n.GetAtomicNum() != 1]
        chain_neighbors = [n for n in non_h_neighbors if n.GetIdx() in chain_atoms]
        
        # For carbons in main chain (except ends), should have exactly 2 carbon neighbors in chain
        if atom_idx != main_chain[0] and atom_idx != main_chain[-1]:
            carbon_chain_neighbors = [n for n in chain_neighbors if n.GetAtomicNum() == 6]
            if len(carbon_chain_neighbors) != 2:
                return False, "Not a straight chain structure"
    
    # Check for rings
    if rdMolDescriptors.CalcNumRings(mol) > 0:
        return False, "Contains rings, must be acyclic"
    
    return True, "C18 straight-chain fatty acid with 2 C=C double bonds"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:25627',
                          'name': 'octadecadienoic acid',
                          'definition': 'Any straight-chain, C18 '
                                        'polyunsaturated fatty acid having two '
                                        'C=C double bonds.',
                          'parents': [   'CHEBI:140949',
                                         'CHEBI:15904',
                                         'CHEBI:26208',
                                         'CHEBI:36326',
                                         'CHEBI:53339',
                                         'CHEBI:59202'],
                          'xrefs': ['CAS:26764-25-0', 'PMID:6794350'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': None,
    'message': '\n'
               'Attempt failed: F1 score of 0.5154639175257733 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: CC/C=C\\C/C=C\\CC(C(CCCCCCCC(O)=O)O)O '
               'NAME: 9,10-DiHODE REASON: CORRECT C18 straight-chain fatty '
               'acid with 2 C=C double bonds\n'
               ' * SMILES: O(C(CCCCCCC(O)=O)/C=C/C=C/C(O)CCCCC)C NAME: '
               '8-Methoxy-13-hydroxy-9,11-octadecadienoic acid REASON: CORRECT '
               'C18 straight-chain fatty acid with 2 C=C double bonds\n'
               ' * SMILES: C(O)(=O)CCCC/C=C/C/C=C/CCCCCCCC NAME: '
               '6E,9E-octadecadienoic acid REASON: CORRECT C18 straight-chain '
               'fatty acid with 2 C=C double bonds\n'
               ' * SMILES: [H]C(CCCCCCCC(O)=O)=CC([H])=CCCCCCC NAME: '
               'octadeca-9,11-dienoic acid REASON: CORRECT C18 straight-chain '
               'fatty acid with 2 C=C double bonds\n'
               ' * SMILES: O=C(CCCCCC)C=CC=CC(=O)CCCCCC(O)=O NAME: '
               'Dioxooctadecadienoic acid REASON: CORRECT C18 straight-chain '
               'fatty acid with 2 C=C double bonds\n'
               ' * SMILES: OC(=O)CCCCCCCCCCCCC=CCC=C NAME: '
               '14,17-Octadecadienoic acid REASON: CORRECT C18 straight-chain '
               'fatty acid with 2 C=C double bonds\n'
               ' * SMILES: OC(CCCCC(O)=O)C(O)C/C=C\\C/C=C\\CCCCC NAME: '
               'gamma-6,7-DiHODE REASON: CORRECT C18 straight-chain fatty acid '
               'with 2 C=C double bonds\n'
               ' * SMILES: OC(CCCCCC)/C=C/C=C/CCCCCCC(O)=O NAME: '
               '12-Hydroxy-8,10-octadecadienoic acid REASON: CORRECT C18 '
               'straight-chain fatty acid with 2 C=C double bonds\n'
               ' * SMILES: O=C(CCCCCCCC(O)=O)C=CC=CCCCCC NAME: '
               '9-Oxooctadeca-10,12-dienoic acid REASON: CORRECT C18 '
               'straight-chain fatty acid with 2 C=C double bonds\n'
               ' * SMILES: OC(=O)CCCCCCCCCC/C=C/CC/C=C/C NAME: '
               '12E,16E-octadecadienoic acid REASON: CORRECT C18 '
               'straight-chain fatty acid with 2 C=C double bonds\n'
               ' * SMILES: O[C@@H](CCCCCCCC(O)=O)\\C=C\\C=C\\CCCCC NAME: '
               '9S-hydroxy-10E,12E-octadecadienoic acid REASON: CORRECT C18 '
               'straight-chain fatty acid with 2 C=C double bonds\n'
               ' * SMILES: CCCCC\\C=C\\C\\C=C/CCCCCCCC(O)=O NAME: '
               '(9Z,12E)-octadecadienoic acid REASON: CORRECT C18 '
               'straight-chain fatty acid with 2 C=C double bonds\n'
               ' * SMILES: C(CC=[C@@]=C([H])CCCC(O)=O)CCCCCCCCC NAME: '
               '(S)-laballenic acid REASON: CORRECT C18 straight-chain fatty '
               'acid with 2 C=C double bonds\n'
               ' * SMILES: '
               'O[C@@H](CCCCCCCC(O)=O)/C=C/[C@@H](O)[C@@H](O)C/C=C\\CC NAME: '
               'Malyngic acid REASON: CORRECT C18 straight-chain fatty acid '
               'with 2 C=C double bonds\n'
               ' * SMILES: OC(CCCCCCCC(O)=O)/C=C/C(O)C(O)C/C=C/CC NAME: '
               '9,12,13,TriHODE REASON: CORRECT C18 straight-chain fatty acid '
               'with 2 C=C double bonds\n'
               ' * SMILES: OC(CCCCCCCC(O)=O)C(O)/C=C/C(O)C/C=C\\CC NAME: '
               '(11E,15Z)-9,10,13-trihydroxyoctadeca-11,15-dienoic acid '
               'REASON: CORRECT C18 straight-chain fatty acid with 2 C=C '
               'double bonds\n'
               ' * SMILES: OC(=O)CCCCCCCCCCC/C=C/CCC=C NAME: '
               '13E,17-Octadecadienoic acid REASON: CORRECT C18 straight-chain '
               'fatty acid with 2 C=C double bonds\n'
               ' * SMILES: OC(CCCCC(O)=O)CC/C=C\\C/C=C\\CCCCC NAME: 6-HODE '
               'REASON: CORRECT C18 straight-chain fatty acid with 2 C=C '
               'double bonds\n'
               ' * SMILES: CCCCCC=CCC=CCCCCCCCC(=O)O NAME: '
               'octadeca-9,12-dienoic acid REASON: CORRECT C18 straight-chain '
               'fatty acid with 2 C=C double bonds\n'
               ' * SMILES: OC(=O)CCCCCCC/C=C/CCCC/C=C/CC NAME: Mangiferic acid '
               'REASON: CORRECT C18 straight-chain fatty acid with 2 C=C '
               'double bonds\n'
               ' * SMILES: O[C@H](CCC)C/C=C\\C/C=C\\CCCCCCCC(O)=O NAME: '
               'Avenoleic acid REASON: CORRECT C18 straight-chain fatty acid '
               'with 2 C=C double bonds\n'
               ' * SMILES: O(O)C(CCCCC)\\C=C\\C=C\\CCCCCCCC(O)=O NAME: '
               'E,E-13-HpODE REASON: CORRECT C18 straight-chain fatty acid '
               'with 2 C=C double bonds\n'
               ' * SMILES: OC(CCCCC)C(O)C/C=C\\C/C=C\\CCCCC(O)=O NAME: '
               'gamma-12,13-DiHODE REASON: CORRECT C18 straight-chain fatty '
               'acid with 2 C=C double bonds\n'
               ' * SMILES: '
               'O[C@@H](CCCCCCCC(O)=O)[C@H](O)[C@H](O)/C=C\\C/C=C\\CC NAME: '
               '9S,10S,11R-trihydroxy-12Z,15Z-octadecadienoic acid REASON: '
               'CORRECT C18 straight-chain fatty acid with 2 C=C double bonds\n'
               ' * SMILES: OC(=O)CCC/C=C\\CC/C=C\\CCCCCCCC NAME: Taxoleic acid '
               'REASON: CORRECT C18 straight-chain fatty acid with 2 C=C '
               'double bonds\n'
               'False positives: SMILES: OC(=O)CCC/C=C\\CCCC/C=C\\CCCCCC NAME: '
               '5Z,11Z-octadecadienoic acid REASON: WRONGLY CLASSIFIED C18 '
               'straight-chain fatty acid with 2 C=C double bonds\n'
               ' * SMILES: OC(=O)CC\\C=C\\CC\\C=C\\CCCCCCCCC NAME: '
               '4E,8E-octadecadienoic acid REASON: WRONGLY CLASSIFIED C18 '
               'straight-chain fatty acid with 2 C=C double bonds\n'
               ' * SMILES: OC(=O)CCC\\C=C\\CCC\\C=C\\CCCCCCC NAME: '
               '5,10-octadecadienoic acid REASON: WRONGLY CLASSIFIED C18 '
               'straight-chain fatty acid with 2 C=C double bonds\n'
               ' * SMILES: OC(=O)CCCCCC/C=C/CC\\C=C\\CCCCC NAME: '
               '8,12-octadecadienoic acid REASON: WRONGLY CLASSIFIED C18 '
               'straight-chain fatty acid with 2 C=C double bonds\n'
               ' * SMILES: OC(=O)C\\C=C\\CC\\C=C\\CCCCCCCCCC NAME: '
               '3E,7E-octadecadienoic acid REASON: WRONGLY CLASSIFIED C18 '
               'straight-chain fatty acid with 2 C=C double bonds\n'
               ' * SMILES: OC(=O)CCCC/C=C/C=C/CCCCCCCCC NAME: 6, '
               '8-octadecadienoic acid REASON: WRONGLY CLASSIFIED C18 '
               'straight-chain fatty acid with 2 C=C double bonds\n'
               ' * SMILES: OC(=O)CCCCC/C=C\\C/C=C\\CCCCCCC NAME: '
               '7Z,10Z-octadecadienoic acid REASON: WRONGLY CLASSIFIED C18 '
               'straight-chain fatty acid with 2 C=C double bonds\n'
               ' * SMILES: CC/C=C\\CC(C(C/C=C\\CCCCCCCC(O)=O)O)O NAME: '
               '12,13-DiHODE REASON: WRONGLY CLASSIFIED C18 straight-chain '
               'fatty acid with 2 C=C double bonds\n'
               ' * SMILES: OC(=O)/C=C\\C/C=C\\CCCCCCCCCCCC NAME: '
               '2Z,5Z-octadecadienoic acid REASON: WRONGLY CLASSIFIED C18 '
               'straight-chain fatty acid with 2 C=C double bonds\n'
               ' * SMILES: OC(CCCCC(O)=O)/C=C/C=C\\C#CC#CC#CC#C NAME: '
               '6-hydroxy-7E,9Z-Octadecadiene-11,13,15,17-tetraynoic acid '
               'REASON: WRONGLY CLASSIFIED C18 straight-chain fatty acid with '
               '2 C=C double bonds\n'
               ' * SMILES: OC(=O)C/C=C\\CCCCCCC/C=C\\CCCCC NAME: '
               '3Z,12Z-octadecadienoic acid REASON: WRONGLY CLASSIFIED C18 '
               'straight-chain fatty acid with 2 C=C double bonds\n'
               ' * SMILES: O=C(O)CCCCCC[C@@H](O)/C=C/C=C/C(=O)CCCCC NAME: '
               '8-hydroxy-13-oxo-9E,11E-octa-decadienoic acid REASON: WRONGLY '
               'CLASSIFIED C18 straight-chain fatty acid with 2 C=C double '
               'bonds\n'
               ' * SMILES: C(=CCCCCCCCC(O)=O)C=CC(CCCCC)=O NAME: '
               '13-oxo-9,11-octadecadienoic acid REASON: WRONGLY CLASSIFIED '
               'C18 straight-chain fatty acid with 2 C=C double bonds\n'
               ' * SMILES: OC(=O)CCCCCCCC#C\\C=C\\CCCCC=C NAME: '
               '11E,17-Octadecadien-9-ynoic acid REASON: WRONGLY CLASSIFIED '
               'C18 straight-chain fatty acid with 2 C=C double bonds\n'
               ' * SMILES: OC(=O)CCCCCCCC#CC#C/C=C\\CCC=C NAME: '
               '13Z,17-Octadecadiene-9,11-diynoic acid REASON: WRONGLY '
               'CLASSIFIED C18 straight-chain fatty acid with 2 C=C double '
               'bonds\n'
               ' * SMILES: OC(=O)CCCCCCCCC/C=C\\CC/C=C\\CC NAME: '
               '11Z,15Z-octadecadienoic acid REASON: WRONGLY CLASSIFIED C18 '
               'straight-chain fatty acid with 2 C=C double bonds\n'
               ' * SMILES: C(=C\\[C@@H](/C=C\\CCCCC)OO)\\CCCCCCCC(=O)O NAME: '
               '(11R)-11-hydroperoxylinoleic acid REASON: WRONGLY CLASSIFIED '
               'C18 straight-chain fatty acid with 2 C=C double bonds\n'
               ' * SMILES: OC(=O)C/C=C\\CC/C=C\\CCCCCCCCCC NAME: '
               '3Z,7Z-octadecadienoic acid REASON: WRONGLY CLASSIFIED C18 '
               'straight-chain fatty acid with 2 C=C double bonds\n'
               ' * SMILES: OC(=O)CCCCCCC/C=C\\CC#C/C=C\\CCC NAME: '
               'Dehydrocrepenynic acid REASON: WRONGLY CLASSIFIED C18 '
               'straight-chain fatty acid with 2 C=C double bonds\n'
               ' * SMILES: O=C(O)CCCCCCC/C=C/C=C\\C(=O)CCCCC NAME: '
               '(9E,11Z)-13-Oxo-9,11-octadecadienoic acid REASON: WRONGLY '
               'CLASSIFIED C18 straight-chain fatty acid with 2 C=C double '
               'bonds\n'
               ' * SMILES: O=C(O)CCCCCCCC(=O)/C=C/C=C/[C@@H](O)CCCC NAME: '
               '(14RS)-(10E,12E)-14-hydroxy-9-oxo-10,12-octadecadienoic acid '
               'REASON: WRONGLY CLASSIFIED C18 straight-chain fatty acid with '
               '2 C=C double bonds\n'
               ' * SMILES: CCCCC\\C=C/C=C/[C@H](CCCCCCCC(O)=O)OO NAME: '
               '9(S)-HPODE REASON: WRONGLY CLASSIFIED C18 straight-chain fatty '
               'acid with 2 C=C double bonds\n'
               ' * SMILES: OC(=O)CCCC\\C=C\\CCCC/C=C/CCCCC NAME: '
               '6E,12E-octadecadienoic acid REASON: WRONGLY CLASSIFIED C18 '
               'straight-chain fatty acid with 2 C=C double bonds\n'
               ' * SMILES: C(=C\\C/C=C\\CCCCC)\\CCCCCCC(C(=O)O)O NAME: '
               '2-hydroxylinoleic acid REASON: WRONGLY CLASSIFIED C18 '
               'straight-chain fatty acid with 2 C=C double bonds\n'
               ' * SMILES: O=C(O)CCCCCCC(O)\\C=C/C=C/C(O)CCCCC NAME: '
               'Filoboletic acid REASON: WRONGLY CLASSIFIED C18 straight-chain '
               'fatty acid with 2 C=C double bonds\n'
               'False negatives: SMILES: C(O)(=O)CCCCCCC/C=C\\C/C=C\\CCCCCF '
               'NAME: 18-fluoro-9Z,12Z-octadecadienoic acid REASON: MISSED '
               'Contains atoms other than C, H, and O\n'
               ' * SMILES: OC(CCCCC)/C=C/C(=O)CCCCCCCCC(O)=O NAME: '
               '(11E)-13-hydroxy-10-oxo-11-octadecenoic acid REASON: MISSED '
               'Contains 1 C=C double bonds, must be exactly 2\n'
               ' * SMILES: CCCCC\\C=C/C\\C(=C/CCCCCCCC(O)=O)[N+]([O-])=O NAME: '
               '10-Nitro-9Z,12Z-octadecadienoic acid REASON: MISSED Contains '
               'atoms other than C, H, and O\n'
               ' * SMILES: CCCCC\\C=C(/C\\C=C/CCCCCCCC(O)=O)[N+]([O-])=O NAME: '
               '12-Nitro-9Z,12Z-octadecadienoic acid REASON: MISSED Contains '
               'atoms other than C, H, and O\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'C[C@H]1CN(C(=O)C2=C(C3=CC=CC=C3CO[C@@H]1CN(C)C(=O)NC4=CC=C(C=C4)OC)C5=CC=CC=C5N2C)[C@H](C)CO',
                                     'name': 'LSM-30659',
                                     'reason': 'Contains atoms other than C, '
                                               'H, and O'},
                                 {   'smiles': 'c1c[nH+]c[nH]1',
                                     'name': 'imidazolium cation',
                                     'reason': 'Contains atoms other than C, '
                                               'H, and O'},
                                 {   'smiles': 'ClC=1C(O)=C2O[C@@]([C@H](NC(=O)[C@@H](NC(=O)[C@@H](NC)[C@@H](O)C(=C2)C1)C(C)=C)C(=O)N3[C@@H](C=CC3)C(=O)N/C(=C(/CC)\\C)/C(=O)N/C(=C/C(O)=O)/C(O)=O)(CC)C',
                                     'name': 'Phomopsin A',
                                     'reason': 'Contains atoms other than C, '
                                               'H, and O'},
                                 {   'smiles': 'ClC(Cl)[C@H](O)CC=1OC(=O)C=2C(O)=CC(=CC2C1)O',
                                     'name': 'Desmethyldichlorodiaportin',
                                     'reason': 'Contains atoms other than C, '
                                               'H, and O'},
                                 {   'smiles': 'ClC=1C(=C(O)C2=C(C1O)C(=O)C=CC2=O)CC=C(C)C',
                                     'name': 'Chlorosesamone',
                                     'reason': 'Contains atoms other than C, '
                                               'H, and O'},
                                 {   'smiles': 'CCCCC[C@H]1O[C@H]1C\\C=C/CCCCCCCC(O)=O',
                                     'name': '(+)-vernolic acid',
                                     'reason': 'Contains 1 C=C double bonds in '
                                               'main chain, must be exactly 2'},
                                 {   'smiles': 'O(C1C(O)C(OC(OC=2C3=C(C=CC2)C=C(C(=C3O)C(=O)C)C)C1O)CO)C4OC(C(O)C(O)C4O)CO',
                                     'name': 'Orientaloside',
                                     'reason': 'No carboxylic acid group '
                                               'found'},
                                 {   'smiles': 'O(C1=C(C=CC=C1C(O)=O)C)C(=O)C',
                                     'name': 'CRESOPYRINE',
                                     'reason': 'Main chain has 7 carbons, must '
                                               'be exactly 18'},
                                 {   'smiles': 'C[C@H]1CN(S(=O)(=O)C2=C(C=C(C=C2)C#CC3=CC=NC=C3)O[C@@H]1CN(C)C(=O)NC4=CC5=C(C=C4)OCO5)[C@@H](C)CO',
                                     'name': '3-(1,3-benzodioxol-5-yl)-1-[[(4S,5S)-2-[(2S)-1-hydroxypropan-2-yl]-4-methyl-1,1-dioxo-8-(2-pyridin-4-ylethynyl)-4,5-dihydro-3H-6,1$l^{6},2-benzoxathiazocin-5-yl]methyl]-1-methylurea',
                                     'reason': 'Contains atoms other than C, '
                                               'H, and O'},
                                 {   'smiles': 'O1C2C3C(CCC3=C)C(CCC2C(C1=O)=C)=C',
                                     'name': '3,6,9-Trimethylidene-3a,4,5,6a,7,8,9a,9b-octahydroazuleno[4,5-b]furan-2-one',
                                     'reason': 'No carboxylic acid group '
                                               'found'}],
    'sample_false_negatives': [   {   'smiles': 'C(O)(=O)CCCCCCC/C=C\\C/C=C\\CCCCCF',
                                      'name': '18-fluoro-9Z,12Z-octadecadienoic '
                                              'acid',
                                      'reason': 'Contains atoms other than C, '
                                                'H, and O'},
                                  {   'smiles': 'OC(CCCCC)/C=C/C(=O)CCCCCCCCC(O)=O',
                                      'name': '(11E)-13-hydroxy-10-oxo-11-octadecenoic '
                                              'acid',
                                      'reason': 'Contains 1 C=C double bonds '
                                                'in main chain, must be '
                                                'exactly 2'},
                                  {   'smiles': 'CCCCC\\C=C/C\\C(=C/CCCCCCCC(O)=O)[N+]([O-])=O',
                                      'name': '10-Nitro-9Z,12Z-octadecadienoic '
                                              'acid',
                                      'reason': 'Contains atoms other than C, '
                                                'H, and O'},
                                  {   'smiles': 'CCCCC\\C=C(/C\\C=C/CCCCCCCC(O)=O)[N+]([O-])=O',
                                      'name': '12-Nitro-9Z,12Z-octadecadienoic '
                                              'acid',
                                      'reason': 'Contains atoms other than C, '
                                                'H, and O'}],
    'attempt': 3,
    'reasoning': 'Let me analyze the previous attempt and its issues:\n'
                 '\n'
                 '1. False Positives Analysis:\n'
                 '- The program incorrectly classified many octadecadienoic '
                 "acid isomers that shouldn't be included\n"
                 '- Most false positives were different positional isomers of '
                 'octadecadienoic acid\n'
                 '- This suggests we need to be more specific about the '
                 'positions of the double bonds\n'
                 '\n'
                 '2. False Negatives Analysis:\n'
                 '- The program rejected molecules with fluorine or nitrogen '
                 'atoms, which was actually correct\n'
                 '- It missed some valid structures that had two double bonds '
                 'but were counted incorrectly\n'
                 '- Some oxidized forms were incorrectly rejected\n'
                 '\n'
                 '3. Main Issues:\n'
                 "- The double bond counting was too simplistic and didn't "
                 'properly handle conjugated systems\n'
                 '- The chain length calculation might have been incorrect in '
                 'some cases\n'
                 "- The program didn't properly verify that the molecule was "
                 'truly straight-chain\n'
                 '\n'
                 "Here's how we can improve:\n"
                 '\n'
                 '1. Better chain analysis:\n'
                 '- Use a more robust method to identify and follow the main '
                 'carbon chain\n'
                 "- Ensure we're properly counting carbons in the main chain "
                 'only\n'
                 '\n'
                 '2. Improved double bond detection:\n'
                 '- Use a more sophisticated method to count double bonds\n'
                 '- Verify that double bonds are in the main chain\n'
                 '- Handle conjugated systems properly\n'
                 '\n'
                 '3. Better structural verification:\n'
                 '- Add checks to ensure the chain is truly linear\n'
                 '- Better handle substituents while maintaining the '
                 'straight-chain requirement\n'
                 '\n'
                 "Here's my improved version:",
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 50,
    'num_false_positives': 89,
    'num_true_negatives': 142157,
    'num_false_negatives': 4,
    'num_negatives': None,
    'precision': 0.3597122302158273,
    'recall': 0.9259259259259259,
    'f1': 0.5181347150259067,
    'accuracy': 0.9993464511595221,
    'negative_predictive_value': 0.9999718628878526}