"""
Classifies: CHEBI:33521 metal atom
"""
"""
Classifies: metal atom
"""
from rdkit import Chem
import re

def is_metal_atom(smiles: str):
    """
    Determines if a SMILES string represents a metal atom.
    Must be a neutral, unbonded metal atom.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a metal atom, False otherwise
        str: Reason for classification
    """
    
    # List of metal elements
    metal_elements = {
        'Li', 'Na', 'K', 'Rb', 'Cs', 'Fr',  # Alkali metals
        'Be', 'Mg', 'Ca', 'Sr', 'Ba', 'Ra',  # Alkaline earth metals
        'Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn',  # First-row transition metals
        'Y', 'Zr', 'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd',  # Second-row transition metals
        'Hf', 'Ta', 'W', 'Re', 'Os', 'Ir', 'Pt', 'Au', 'Hg',  # Third-row transition metals
        'Rf', 'Db', 'Sg', 'Bh', 'Hs', 'Mt', 'Ds', 'Rg', 'Cn',  # Fourth-row transition metals
        'Al', 'Ga', 'In', 'Sn', 'Tl', 'Pb', 'Bi', 'Po',  # Post-transition metals
        'La', 'Ce', 'Pr', 'Nd', 'Pm', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy',  # Lanthanides
        'Ho', 'Er', 'Tm', 'Yb', 'Lu',  # More lanthanides
        'Ac', 'Th', 'Pa', 'U', 'Np', 'Pu', 'Am', 'Cm', 'Bk', 'Cf',  # Actinides
        'Es', 'Fm', 'Md', 'No', 'Lr'  # More actinides
    }
    
    # Check if SMILES is valid
    if not isinstance(smiles, str):
        return False, "Input must be a string"
    
    # Strict SMILES format for single atom: [<optional_mass>Element]
    # Only allows numbers (isotope) and element symbol inside brackets
    pattern = r'^\[(\d+)?([A-Z][a-z]?)\]$'
    match = re.match(pattern, smiles)
    if not match:
        return False, "Not a single atom SMILES (should be in format [Element] or [massElement])"
    
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
    
    # Check number of atoms
    if mol.GetNumAtoms() != 1:
        return False, "Must contain exactly one atom"
    
    # Get the atom
    atom = mol.GetAtomWithIdx(0)
    symbol = atom.GetSymbol()
    
    # Check if it's a metal
    if symbol not in metal_elements:
        return False, f"{symbol} is not a metal element"
    
    # Check for formal charge - must be neutral
    if atom.GetFormalCharge() != 0:
        return False, f"{symbol} has a formal charge, not a neutral atom"
    
    # Check for implicit or explicit hydrogens
    if atom.GetNumImplicitHs() > 0 or atom.GetNumExplicitHs() > 0:
        return False, f"{symbol} has bonded hydrogens, not a free atom"
    
    # Check for any bonds
    if atom.GetDegree() > 0:
        return False, f"{symbol} has bonds to other atoms"
        
    return True, f"Single atom of metal element {symbol}"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:33521',
                          'name': 'metal atom',
                          'definition': 'An atom of an element that exhibits '
                                        'typical metallic properties, being '
                                        'typically shiny, with high electrical '
                                        'and thermal conductivity.',
                          'parents': ['CHEBI:33250'],
                          'xrefs': [   'KEGG:C00050',
                                       'PMID:21784043',
                                       'Wikipedia:Metal'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': None,
    'message': '\n'
               'Attempt failed: F1 score of 0.7041420118343196 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: [Fm] NAME: fermium REASON: CORRECT '
               'Single atom of metal element Fm\n'
               ' * SMILES: [98Mo] NAME: molybdenum-98 atom REASON: CORRECT '
               'Single atom of metal element Mo\n'
               ' * SMILES: [Cs] NAME: caesium atom REASON: CORRECT Single atom '
               'of metal element Cs\n'
               ' * SMILES: [139La] NAME: lanthanum-139 atom REASON: CORRECT '
               'Single atom of metal element La\n'
               ' * SMILES: [203Po] NAME: polonium-203 atom REASON: CORRECT '
               'Single atom of metal element Po\n'
               ' * SMILES: [216Po] NAME: polonium-216 atom REASON: CORRECT '
               'Single atom of metal element Po\n'
               ' * SMILES: [Po] NAME: polonium atom REASON: CORRECT Single '
               'atom of metal element Po\n'
               ' * SMILES: [210Po] NAME: polonium-210 atom REASON: CORRECT '
               'Single atom of metal element Po\n'
               ' * SMILES: [Rb] NAME: rubidium atom REASON: CORRECT Single '
               'atom of metal element Rb\n'
               ' * SMILES: [Ni] NAME: nickel atom REASON: CORRECT Single atom '
               'of metal element Ni\n'
               ' * SMILES: [Ce] NAME: cerium REASON: CORRECT Single atom of '
               'metal element Ce\n'
               ' * SMILES: [Tm] NAME: thulium atom REASON: CORRECT Single atom '
               'of metal element Tm\n'
               ' * SMILES: [23Na] NAME: sodium-23 atom REASON: CORRECT Single '
               'atom of metal element Na\n'
               ' * SMILES: [95Mo] NAME: molybdenum-95 REASON: CORRECT Single '
               'atom of metal element Mo\n'
               ' * SMILES: [Cn] NAME: copernicium atom REASON: CORRECT Single '
               'atom of metal element Cn\n'
               ' * SMILES: [25Mg] NAME: magnesium-25 atom REASON: CORRECT '
               'Single atom of metal element Mg\n'
               ' * SMILES: [Eu] NAME: europium atom REASON: CORRECT Single '
               'atom of metal element Eu\n'
               ' * SMILES: [7Li] NAME: lithium-7 atom REASON: CORRECT Single '
               'atom of metal element Li\n'
               ' * SMILES: [195Po] NAME: polonium-195 atom REASON: CORRECT '
               'Single atom of metal element Po\n'
               ' * SMILES: [Lu] NAME: lutetium atom REASON: CORRECT Single '
               'atom of metal element Lu\n'
               ' * SMILES: [89Y] NAME: yttrium-89 atom REASON: CORRECT Single '
               'atom of metal element Y\n'
               ' * SMILES: [85Rb] NAME: rubidium-85 atom REASON: CORRECT '
               'Single atom of metal element Rb\n'
               ' * SMILES: [Sr] NAME: strontium atom REASON: CORRECT Single '
               'atom of metal element Sr\n'
               ' * SMILES: [Th] NAME: thorium REASON: CORRECT Single atom of '
               'metal element Th\n'
               ' * SMILES: [Al] NAME: aluminium(0) REASON: CORRECT Single atom '
               'of metal element Al\n'
               'False positives: SMILES: [Cr+3] NAME: chromium(3+) REASON: '
               'WRONGLY CLASSIFIED Single atom of metal element Cr\n'
               ' * SMILES: [Ca++] NAME: calcium(2+) REASON: WRONGLY CLASSIFIED '
               'Single atom of metal element Ca\n'
               ' * SMILES: [La+3] NAME: lanthanum(3+) REASON: WRONGLY '
               'CLASSIFIED Single atom of metal element La\n'
               ' * SMILES: [Cr+6] NAME: chromium(6+) REASON: WRONGLY '
               'CLASSIFIED Single atom of metal element Cr\n'
               ' * SMILES: [Y+3] NAME: yttrium(3+) REASON: WRONGLY CLASSIFIED '
               'Single atom of metal element Y\n'
               ' * SMILES: [Sr++] NAME: strontium(2+) REASON: WRONGLY '
               'CLASSIFIED Single atom of metal element Sr\n'
               ' * SMILES: [H][Sn]([H])([H])[H] NAME: stannane REASON: WRONGLY '
               'CLASSIFIED Single atom of metal element Sn\n'
               ' * SMILES: [H][Be][H] NAME: beryllium dihydride REASON: '
               'WRONGLY CLASSIFIED Single atom of metal element Be\n'
               ' * SMILES: [H][Fe-4]([H])([H])([H])([H])[H] NAME: '
               'hexahydridoferrate(4-) REASON: WRONGLY CLASSIFIED Single atom '
               'of metal element Fe\n'
               ' * SMILES: [9Be] NAME: beryllium-9 REASON: WRONGLY CLASSIFIED '
               'Single atom of metal element Be\n'
               ' * SMILES: [Tl+3] NAME: thallium(3+) REASON: WRONGLY '
               'CLASSIFIED Single atom of metal element Tl\n'
               ' * SMILES: [Cr++] NAME: chromium(2+) REASON: WRONGLY '
               'CLASSIFIED Single atom of metal element Cr\n'
               ' * SMILES: [H][Sn-]([H])[H] NAME: stannanide REASON: WRONGLY '
               'CLASSIFIED Single atom of metal element Sn\n'
               ' * SMILES: [Eu++] NAME: europium(2+) REASON: WRONGLY '
               'CLASSIFIED Single atom of metal element Eu\n'
               ' * SMILES: [In+3] NAME: indium(3+) REASON: WRONGLY CLASSIFIED '
               'Single atom of metal element In\n'
               ' * SMILES: [Li][H] NAME: lithium hydride REASON: WRONGLY '
               'CLASSIFIED Single atom of metal element Li\n'
               ' * SMILES: [203Tl] NAME: thallium-203 REASON: WRONGLY '
               'CLASSIFIED Single atom of metal element Tl\n'
               ' * SMILES: [H][Bi-]([H])([H])[H] NAME: bismuthanuide REASON: '
               'WRONGLY CLASSIFIED Single atom of metal element Bi\n'
               ' * SMILES: [Os+4] NAME: osmium(4+) REASON: WRONGLY CLASSIFIED '
               'Single atom of metal element Os\n'
               ' * SMILES: [Be][H] NAME: hydridoberyllium REASON: WRONGLY '
               'CLASSIFIED Single atom of metal element Be\n'
               ' * SMILES: [Nd+3] NAME: neodymium(3+) REASON: WRONGLY '
               'CLASSIFIED Single atom of metal element Nd\n'
               ' * SMILES: [Tl+] NAME: thallium(1+) REASON: WRONGLY CLASSIFIED '
               'Single atom of metal element Tl\n'
               ' * SMILES: [Li+] NAME: lithium(1+) REASON: WRONGLY CLASSIFIED '
               'Single atom of metal element Li\n'
               ' * SMILES: [Ni+] NAME: nickel(1+) REASON: WRONGLY CLASSIFIED '
               'Single atom of metal element Ni\n'
               ' * SMILES: [Ru+4] NAME: ruthenium(4+) REASON: WRONGLY '
               'CLASSIFIED Single atom of metal element Ru\n'
               'False negatives: NONE\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'Cc1cc(C)c2Cc3c(C)cc(C)c(Cc4c(C)cc(C)c(Cc5c(C)cc(C)c(Cc1c2C)c5C)c4C)c3C',
                                     'name': '4,6,10,12,16,18,22,24,25,26,27,28-dodecamethylcalix[4]arene',
                                     'reason': 'Not a single atom SMILES '
                                               '(should be in format [Element] '
                                               'or [massElement])'},
                                 {   'smiles': 'O=C1C(=C2C=C3[C@]([C@@H](C(C)C)[C@@H]([C@H]3O)OC(=O)C)(C)CC[C@]2(C)CC1)COC(=O)C',
                                     'name': 'Dahliane E',
                                     'reason': 'Not a single atom SMILES '
                                               '(should be in format [Element] '
                                               'or [massElement])'},
                                 {   'smiles': 'O[C@@H]([C@H](NC(=O)[C@@H](N)CCC(O)=O)C(=O)N[C@@H](CC(C)C)C(O)=O)C',
                                     'name': 'Glu-Thr-Leu',
                                     'reason': 'Not a single atom SMILES '
                                               '(should be in format [Element] '
                                               'or [massElement])'},
                                 {   'smiles': 'CCOc1ccc(NC(=O)C(C)O)cc1',
                                     'name': 'p-Lactophenetide',
                                     'reason': 'Not a single atom SMILES '
                                               '(should be in format [Element] '
                                               'or [massElement])'},
                                 {   'smiles': 'O=C1NCC=2C1=C3C(N([C@@H]4O[C@H]([C@@H](O)[C@H]([C@H]4OC)O)C)C5=C3C=CC=C5)=C6NC7=C(C26)C=CC=C7',
                                     'name': "3'-epi-5'-methoxy-K252d",
                                     'reason': 'Not a single atom SMILES '
                                               '(should be in format [Element] '
                                               'or [massElement])'},
                                 {   'smiles': 'O=C(OC1C(O)C(OC(C1O)CO)OCC2OC(OCC(OC(=O)CCCCCCCCCCCCCCC)COC(=O)CCCCCCC/C=C\\C/C=C\\C/C=C\\CC)C(O)C(C2O)O)CCCCCCCCCCCCCCC',
                                     'name': '[(2S)-2-hexadecanoyloxy-3-[(2S,3R,4S,5S,6R)-6-[[(2S,3R,4S,5S,6R)-4-hexadecanoyloxy-3,5-dihydroxy-6-(hydroxymethyl)tetrahydropyran-2-yl]oxymethyl]-3,4,5-trihydroxy-tetrahydropyran-2-yl]oxy-propyl] '
                                             '(9E,12E,15E)-octadeca-9,12,15-trienoate',
                                     'reason': 'Not a single atom SMILES '
                                               '(should be in format [Element] '
                                               'or [massElement])'},
                                 {   'smiles': 'O=C1C2=C(O)C=C(OC)C=C2C(=O)C3=C1[C@@H]([C@@H](O)[C@]([C@@H]3O)(O)C)C',
                                     'name': 'Altersolanol G',
                                     'reason': 'Not a single atom SMILES '
                                               '(should be in format [Element] '
                                               'or [massElement])'},
                                 {   'smiles': '[H][C@]1(O[C@](O)(C[C@H](O)[C@H]1NC(=O)CO)C([O-])=O)[C@H](O)[C@H](O)CO',
                                     'name': 'N-glycoloyl-alpha-neuraminate',
                                     'reason': 'Not a single atom SMILES '
                                               '(should be in format [Element] '
                                               'or [massElement])'},
                                 {   'smiles': 'OC(C(O)C/C=C\\C/C=C\\C/C=C\\CC)C/C=C\\C/C=C\\CCC(O)=O',
                                     'name': '10,11-DiHDPE',
                                     'reason': 'Not a single atom SMILES '
                                               '(should be in format [Element] '
                                               'or [massElement])'},
                                 {   'smiles': '[Na+].[H][C@]12SCC(C)=C(N1C(=O)[C@H]2NC(=O)[C@H](N)c1ccccc1)C([O-])=O',
                                     'name': 'cephalexin sodium',
                                     'reason': 'Not a single atom SMILES '
                                               '(should be in format [Element] '
                                               'or [massElement])'}],
    'sample_false_negatives': [],
    'attempt': 1,
    'reasoning': "Let's analyze what went wrong in the previous attempt:\n"
                 '\n'
                 '1. Main Issue: The program incorrectly classified metal ions '
                 'and metal-containing molecules as metal atoms. Looking at '
                 'the false positives, we see:\n'
                 '   - Metal ions like [Cr+3], [Ca++], [La+3]\n'
                 '   - Metal hydrides like [Li][H], [Be][H]\n'
                 '   - More complex metal compounds like [H][Sn]([H])([H])[H]\n'
                 '\n'
                 '2. The Problem: The current code only checks:\n'
                 "   - If it's a single atom (mol.GetNumAtoms() == 1)\n"
                 '   - If the element is in the metal_elements set\n'
                 '   - Basic SMILES format with regex\n'
                 '\n'
                 "3. What's Missing:\n"
                 '   - No check for formal charges (to exclude ions)\n'
                 '   - No check for bonds (to exclude compounds)\n'
                 '   - The regex pattern allows additional characters after '
                 'the element symbol\n'
                 '\n'
                 "Here's the improved code:",
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 119,
    'num_false_positives': 15,
    'num_true_negatives': 142166,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.8880597014925373,
    'recall': 1.0,
    'f1': 0.9407114624505929,
    'accuracy': 0.9998945888966971,
    'negative_predictive_value': 1.0}