"""
Classifies: CHEBI:33848 polycyclic arene
"""
from rdkit import Chem
from rdkit.Chem import rdMolDescriptors

def is_polycyclic_arene(smiles: str):
    """
    Determines if a molecule is a polycyclic arene based on its SMILES string.
    A polycyclic arene is a hydrocarbon with at least 3 fused rings and no heteroatoms in the ring system.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a polycyclic arene, False otherwise
        str: Reason for classification
    """
    
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check if molecule is a hydrocarbon
    if not all(atom.GetAtomicNum() in [1, 6] for atom in mol.GetAtoms()):
        return False, "Molecule is not a hydrocarbon"

    # Check for at least 3 fused rings
    ring_info = mol.GetRingInfo()
    if len(ring_info.AtomRings()) < 3:
        return False, "Molecule does not contain at least 3 fused rings"

    # Check for heteroatoms in the ring system
    for ring in ring_info.AtomRings():
        for atom_idx in ring:
            atom = mol.GetAtomWithIdx(atom_idx)
            if atom.GetAtomicNum() != 6:
                return False, "Molecule contains heteroatoms in the ring system"

    # Check for aromaticity
    for ring in ring_info.AtomRings():
        ring_mol = Chem.PathToSubmol(mol, ring)
        for atom in ring_mol.GetAtoms():
            if not atom.GetIsAromatic():
                return False, "Molecule is not aromatic"

    # Check for connected ring system
    ring_system = set()
    for ring in ring_info.AtomRings():
        for atom_idx in ring:
            ring_system.add(atom_idx)
    if len(ring_system) < 10:  # Minimum number of atoms in a polycyclic arene
        return False, "Molecule does not have a connected ring system"

    return True, "Molecule is a polycyclic arene"

# Test the function
smiles = "c1ccc-2c(c1)-c1cccc3c4ccccc4cc-2c13"  # benzo[b]fluoranthene
print(is_polycyclic_arene(smiles))


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:33848',
                          'name': 'polycyclic arene',
                          'definition': 'A polycyclic aromatic hydrocarbon.',
                          'parents': ['CHEBI:33658', 'CHEBI:33666'],
                          'xrefs': [   'PMID:15198916',
                                       'PMID:25679824',
                                       'Wikipedia:Polycyclic_aromatic_hydrocarbon'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': None,
    'message': '\n'
               "Error: module 'rdkit.Chem.AllChem' has no attribute "
               "'Aromaticity'\n"
               'Attempt failed: F1 score of 0 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: NONE\n'
               'False positives: NONE\n'
               'False negatives: NONE\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': '[O-]c1ccccc1[O-]',
                                     'name': 'catecholate(2-)',
                                     'reason': 'Molecule is not a hydrocarbon'},
                                 {   'smiles': 'C[C@H]1CN(C(=O)C2=C(C=CC(=C2)NC(=O)CC3=CC=CC=C3)O[C@@H]1CN(C)CC4=CC=C(C=C4)C(F)(F)F)[C@@H](C)CO',
                                     'name': 'N-[(2S,3S)-5-[(2S)-1-hydroxypropan-2-yl]-3-methyl-2-[[methyl-[[4-(trifluoromethyl)phenyl]methyl]amino]methyl]-6-oxo-3,4-dihydro-2H-1,5-benzoxazocin-8-yl]-2-phenylacetamide',
                                     'reason': 'Molecule is not a hydrocarbon'},
                                 {   'smiles': '[H][C@]12CN3C4=C([C@@H](COC(N)=O)[C@@]3(OC)[C@@]1([H])N2)C(=O)C(NCCSSC1=CC=C(C=C1)[N+]([O-])=O)=C(C)C4=O',
                                     'name': 'BMY-25067',
                                     'reason': 'Molecule is not a hydrocarbon'},
                                 {   'smiles': 'O=C1C2=C(O)C(=C(O)C=C2C(=O)C=3C1=C(O)C=C(O)C3)/C=C/CCCC',
                                     'name': 'Averythrin',
                                     'reason': 'Molecule is not a hydrocarbon'},
                                 {   'smiles': 'CC=CC1=CC=C(C=C1)[C@@H]2[C@H]3CN(CC(=O)N3[C@@H]2CO)S(=O)(=O)C4=CC=CC=C4',
                                     'name': 'LSM-41791',
                                     'reason': 'Molecule is not a hydrocarbon'},
                                 {   'smiles': 'CC1=CC2=C(C=C1)N(C3=NC4=CC=CC=C4N=C23)CCN5CCOCC5',
                                     'name': '4-[2-(9-methyl-6-indolo[3,2-b]quinoxalinyl)ethyl]morpholine',
                                     'reason': 'Molecule is not a hydrocarbon'},
                                 {   'smiles': 'CC(C)C[C@H](NC(=O)[C@H](C)N)C(=O)N[C@@H](CC(C)C)C(=O)N[C@@H]([C@@H](C)O)C(O)=O',
                                     'name': 'Ala-Leu-Leu-Thr',
                                     'reason': 'Molecule is not a hydrocarbon'},
                                 {   'smiles': 'O(C=1C(=C(O)C=C(O)C1)C(=O)/C=C/C2=CC=C(O)C=C2)C',
                                     'name': 'Helichrysetin',
                                     'reason': 'Molecule is not a hydrocarbon'},
                                 {   'smiles': 'O([C@H]1[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]1CO)O[C@H]2[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]2CO)O)[C@@H]3O[C@@H]([C@@H](O)[C@H](O[C@H]4O[C@@H]([C@@H](O)[C@H](O)[C@@H]4O)CO)[C@@H]3O)CO[C@H]5O[C@@H]([C@@H](OC6O[C@@H]([C@@H](O)[C@H](O)[C@H]6NC(=O)C)CO)[C@H](O)[C@@H]5O)CO',
                                     'name': 'N-[(2R,3R,4R,5S,6R)-5-[(2S,3R,4R,5S,6R)-3-Acetamido-5-[(2S,3S,4S,5R,6R)-6-[[(2S,3S,4R,5S,6R)-5-[(3R,4R,5S,6R)-3-acetamido-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-3,4-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxymethyl]-3,5-dihydroxy-4-[(2R,3S,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-2,4-dihydroxy-6-(hydroxymethyl)oxan-3-yl]acetamide',
                                     'reason': 'Molecule is not a hydrocarbon'},
                                 {   'smiles': 'C[C@H]1CN(C(=O)CCCN2C=C(CO[C@@H]1CN(C)C(=O)C3CC3)N=N2)[C@H](C)CO',
                                     'name': 'N-[[(8S,9S)-6-[(2R)-1-hydroxypropan-2-yl]-8-methyl-5-oxo-10-oxa-1,6,13,14-tetrazabicyclo[10.2.1]pentadeca-12(15),13-dien-9-yl]methyl]-N-methylcyclopropanecarboxamide',
                                     'reason': 'Molecule is not a '
                                               'hydrocarbon'}],
    'sample_false_negatives': [   {   'smiles': 'Oc1cc2cccc3ccc4cc5ccccc5c1c4c23',
                                      'name': '11-Hydroxybenzo[a]pyrene',
                                      'reason': 'Molecule is not a '
                                                'hydrocarbon'},
                                  {   'smiles': 'Oc1cccc2cc3ccc4cccc5ccc(c12)c3c45',
                                      'name': '10-Hydroxybenzo[a]pyrene',
                                      'reason': 'Molecule is not a '
                                                'hydrocarbon'},
                                  {   'smiles': 'C1C=Cc2cccc3cccc1c23',
                                      'name': 'phenalene',
                                      'reason': 'Molecule is not aromatic'},
                                  {   'smiles': 'c1cc2C=Cc3cccc(c1)c23',
                                      'name': 'acenaphthylene',
                                      'reason': 'Molecule is not aromatic'},
                                  {   'smiles': 'Cc1cc(O)c2c3c1c1c(CO)cc(O)c4c1c1c5c(c(O)cc(O)c5c4=O)c4c(O)cc(O)c(c4c31)c2=O',
                                      'name': 'Pseudohypericin',
                                      'reason': 'Molecule is not a '
                                                'hydrocarbon'},
                                  {   'smiles': 'Oc1c2ccccc2c2ccc3cccc4ccc1c2c34',
                                      'name': '6-Hydroxybenzo[a]pyrene',
                                      'reason': 'Molecule is not a '
                                                'hydrocarbon'},
                                  {   'smiles': 'Oc1c(O)c2c3ccccc3cc3ccc4cccc1c4c23',
                                      'name': '11,12-Dihydroxybenzo[a]pyrene',
                                      'reason': 'Molecule is not a '
                                                'hydrocarbon'},
                                  {   'smiles': 'Cc1ccc2cc3c(ccc4ccccc34)c3CCc1c23',
                                      'name': '3-methylcholanthrene',
                                      'reason': 'Molecule is not aromatic'},
                                  {   'smiles': 'Oc1ccc2ccc3c4ccccc4cc4ccc1c2c34',
                                      'name': '3-Hydroxybenzo[a]pyrene',
                                      'reason': 'Molecule is not a '
                                                'hydrocarbon'},
                                  {   'smiles': 'O=c1c2ccccc2c2ccc3c4c(ccc1c24)c1ccccc1c3=O',
                                      'name': 'Vat Yellow 4',
                                      'reason': 'Molecule is not a '
                                                'hydrocarbon'}],
    'attempt': 1,
    'reasoning': '### Analysis of the Previous Program\n'
                 '\n'
                 'The previous program attempted to classify chemical entities '
                 'as polycyclic arenes based on their SMILES strings. However, '
                 'it encountered an error due to the non-existent '
                 '`Aromaticity` attribute in `rdkit.Chem.AllChem`. '
                 "Additionally, the function's performance was poor, with an "
                 'F1 score of 0, indicating that it failed to correctly '
                 'classify any molecules.\n'
                 '\n'
                 'Upon analyzing the code, several issues can be identified:\n'
                 '\n'
                 '1.  **Incorrect Aromaticity Check**: The '
                 '`AllChem.Aromaticity` function does not exist in RDKit. '
                 'Instead, you can use `Chem.rdchem.Mol.GetAromaticAtoms()` to '
                 'check for aromatic atoms.\n'
                 '2.  **Insufficient Ring System Analysis**: The code only '
                 'checks for the presence of at least three fused rings but '
                 'does not verify if these rings are part of a single, '
                 'connected ring system.\n'
                 '3.  **Lack of Hydrogen Counting**: The code checks if the '
                 'molecule is a hydrocarbon by verifying that all atoms are '
                 'either carbon or hydrogen. However, it does not account for '
                 'the possibility of molecules with no hydrogen atoms (e.g., '
                 'fullerenes).\n'
                 '4.  **No Verification of Aromatic Ring Systems**: The code '
                 'does not check if the ring systems are aromatic, which is a '
                 'crucial characteristic of polycyclic arenes.\n'
                 '\n'
                 '### Improved Code\n'
                 '\n'
                 'To address these issues, a revised version of the code can '
                 'be implemented:',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 51,
    'num_false_positives': 18,
    'num_true_negatives': 142205,
    'num_false_negatives': 26,
    'num_negatives': None,
    'precision': 0.7391304347826086,
    'recall': 0.6623376623376623,
    'f1': 0.6986301369863014,
    'accuracy': 0.9996907940969783,
    'negative_predictive_value': 0.9998171987822626}