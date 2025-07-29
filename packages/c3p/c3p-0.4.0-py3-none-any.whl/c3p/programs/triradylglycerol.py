"""
Classifies: CHEBI:76579 triradylglycerol
"""
"""
Classifies: CHEBI:35741 triradylglycerol
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_triradylglycerol(smiles: str):
    """
    Determines if a molecule is a triradylglycerol based on its SMILES string.
    A triradylglycerol has a glycerol backbone with three substituent groups (acyl, alkyl, or alk-1-enyl) attached via ester bonds.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a triradylglycerol, False otherwise
        str: Reason for classification
    """
    
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Look for glycerol backbone pattern (C-C-C with 3 oxygens attached)
    glycerol_pattern = Chem.MolFromSmarts("[CH2X4][CHX4][CH2X4]")
    if not mol.HasSubstructMatch(glycerol_pattern):
        return False, "No glycerol backbone found"
        
    # Look for 3 ester groups (-O-C(=O)-)
    ester_pattern = Chem.MolFromSmarts("[OX2][CX3](=[OX1])")
    ester_matches = mol.GetSubstructMatches(ester_pattern)
    if len(ester_matches) != 3:
        return False, f"Found {len(ester_matches)} ester groups, need exactly 3"

    # Check for substituent groups (acyl, alkyl, or alk-1-enyl) attached to the glycerol backbone
    # Acyl: -C(=O)-R
    # Alkyl: -C-R
    # Alk-1-enyl: -C=C-R
    substituent_pattern = Chem.MolFromSmarts("[CX4,CX3,CX2]~[CX4,CX3,CX2]~[CX4,CX3,CX2]~[CX4,CX3,CX2]")
    substituent_matches = mol.GetSubstructMatches(substituent_pattern)
    if len(substituent_matches) < 3:
        return False, f"Missing substituent groups, got {len(substituent_matches)}"

    # Count rotatable bonds to verify long chains
    n_rotatable = rdMolDescriptors.CalcNumRotatableBonds(mol)
    if n_rotatable < 6:
        return False, "Chains too short to be substituent groups"

    # Check molecular weight - triradylglycerols typically >400 Da
    mol_wt = rdMolDescriptors.CalcExactMolWt(mol)
    if mol_wt < 400:
        return False, "Molecular weight too low for triradylglycerol"

    # Count carbons and oxygens
    c_count = sum(1 for atom in mol.GetAtoms() if atom.GetAtomicNum() == 6)
    o_count = sum(1 for atom in mol.GetAtoms() if atom.GetAtomicNum() == 8)
    
    if c_count < 15:
        return False, "Too few carbons for triradylglycerol"
    if o_count != 6:
        return False, "Must have exactly 6 oxygens (3 ester groups)"

    return True, "Contains glycerol backbone with 3 substituent groups attached via ester bonds"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:76579',
                          'name': 'triradylglycerol',
                          'definition': 'A glycerol compound having one of '
                                        'three possible substituent groups - '
                                        'either acyl, alkyl, or alk-1-enyl - '
                                        'at each of the three possible '
                                        'positions sn-1, sn-2 or sn-3. has '
                                        'functional parent glycerol '
                                        '(CHEBI:17754), children: triglyceride '
                                        '(CHEBI:17855). Parent: is_a '
                                        'glycerolipid (CHEBI:35741)',
                          'parents': ['CHEBI:35741'],
                          'xrefs': ['LIPID_MAPS_class:LMGL0301'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': None,
    'message': None,
    'sample_true_negatives': [   {   'smiles': 'C1=CC=C2C(=C1)C3=C(C4=C(C=CC=N4)C=C3)NS2(=O)=O',
                                     'name': '5H-quinolino[8,7-c][1,2]benzothiazine '
                                             '6,6-dioxide',
                                     'reason': 'No glycerol backbone found'},
                                 {   'smiles': 'O([C@@H]1C([C@]2([C@@]([C@@]3([C@]([C@]4(C([C@]5([C@@]([C@H](O)C4)(CCC(C5)(C)C)C(O)=O)[H])=CC3)C)(CC2)C)[H])(CC1)C)[H])(C)C)[C@@H]6O[C@@H]([C@@H](O)[C@H](O)[C@H]6O)CO',
                                     'name': 'Echinocystic acid 3-glucoside',
                                     'reason': 'No glycerol backbone found'},
                                 {   'smiles': 'C[C@@H]1CN([C@@H](COC2=C(C=C(C=C2)NS(=O)(=O)C3=CC=CC=C3)C(=O)N(C[C@H]1OC)C)C)C',
                                     'name': 'N-[(4R,7R,8S)-8-methoxy-4,5,7,10-tetramethyl-11-oxo-2-oxa-5,10-diazabicyclo[10.4.0]hexadeca-1(12),13,15-trien-14-yl]benzenesulfonamide',
                                     'reason': 'No glycerol backbone found'},
                                 {   'smiles': 'O=C1O[C@](C(=O)OC)(CC2=CC(=C(O)C=C2)CC(=O)C)C(=C1O)C3=CC=C(OC)C=C3',
                                     'name': 'Versicolactone A',
                                     'reason': 'No glycerol backbone found'},
                                 {   'smiles': 'O=C(N[C@@H](CO)C(O)=O)[C@@H](NC(=O)[C@@H](N)CC=1NC=NC1)CCC(O)=O',
                                     'name': 'His-Glu-Ser',
                                     'reason': 'No glycerol backbone found'},
                                 {   'smiles': 'O=C1N(O)CCOCCNC(=O)CCC(=O)N(O)CCOCCNC(CCC(N(CCOCCNC(CC1)=O)O)=O)=O',
                                     'name': 'Desferrioxamine Et3',
                                     'reason': 'No glycerol backbone found'},
                                 {   'smiles': 'P(OC[C@H](OC(=O)CCCCCCCCC/C=C\\CCCCCC)COC(=O)CCCCCCC/C=C\\C/C=C\\C/C=C\\CC)(OCCN)(O)=O',
                                     'name': 'PE(18:3(9Z,12Z,15Z)/18:1(11Z))',
                                     'reason': 'Found 2 ester groups, need '
                                               'exactly 3'},
                                 {   'smiles': 'S(C[C@H](N)C(=O)N[C@H]1[C@@H](O)C(N2C3=NC=NC(=C3N=C2)N(C)C)OC1CO)C',
                                     'name': 'Cystocin',
                                     'reason': 'No glycerol backbone found'},
                                 {   'smiles': 'COc1cc(O)c(CC=C(C)C)cc1C(=O)[C@@H](O)Cc1ccc(O)cc1',
                                     'name': 'lespeflorin C3',
                                     'reason': 'No glycerol backbone found'},
                                 {   'smiles': 'NC(=O)OP(O)(O)=O',
                                     'name': 'carbamoyl phosphate',
                                     'reason': 'No glycerol backbone found'}],
    'sample_false_negatives': [   {   'smiles': 'CC(=O)OCC(COC(C)=O)OC(C)=O',
                                      'name': 'triacetin',
                                      'reason': 'Missing substituent groups, '
                                                'got 0'},
                                  {   'smiles': 'CCCC(=O)OCC(COC(=O)CCC)OC(=O)CCC',
                                      'name': 'tributyrin',
                                      'reason': 'Molecular weight too low for '
                                                'triradylglycerol'},
                                  {   'smiles': 'C(C(COC(=O)CCCCCCC/C=C\\C[C@@H](CCCCCC)O)OC(=O)CCCCCCC/C=C\\C[C@@H](CCCCCC)O)OC(=O)CCCCCCC/C=C\\C[C@@H](CCCCCC)O',
                                      'name': 'triricinolein',
                                      'reason': 'Must have exactly 6 oxygens '
                                                '(3 ester groups)'},
                                  {   'smiles': 'CCCCCCCCCCCCCCCCOC[C@H](COC(=O)CCCCCCCCCCC)OC(C)=O',
                                      'name': '1-palmityl-2-acetyl-3-lauroyl-sn-glycerol',
                                      'reason': 'Found 2 ester groups, need '
                                                'exactly 3'},
                                  {   'smiles': 'O(CCCCCCCCCCCCCCCCCC)C[C@@H](OC(=O)CCCCCCCCCCCCCC)COC(=O)CCCC/C=C\\C/C=C\\C/C=C\\CCCCC',
                                      'name': '(2R)-3-(Octadecyloxy)-2-(pentadecanoyloxy)propyl '
                                              '(6Z,9Z,12Z)-octadeca-6,9,12-trienoate',
                                      'reason': 'Found 2 ester groups, need '
                                                'exactly 3'},
                                  {   'smiles': 'O(CCCCCCCCCCCCCCCCCC)[C@@H](COC(=O)CCCCCCCCCCCCCC)COC(=O)CCCC/C=C\\C/C=C\\C/C=C\\C/C=C\\CC',
                                      'name': '(2S)-2-(Octadecyloxy)-3-(pentadecanoyloxy)propyl '
                                              '(6Z,9Z,12Z,15Z)-octadeca-6,9,12,15-tetraenoate',
                                      'reason': 'Found 2 ester groups, need '
                                                'exactly 3'},
                                  {   'smiles': 'CCCCCCCCCCCCCCCCOC[C@H](COC(=O)CCCCCCC\\C=C/CCCCCCCC)OC(C)=O',
                                      'name': '1-palmityl-2-acetyl-3-oleoyl-sn-glycerol',
                                      'reason': 'Found 2 ester groups, need '
                                                'exactly 3'},
                                  {   'smiles': 'O(CCCCCCCC/C=C\\CCCCCCCC)CC(COC(CCCCCCC/C=C\\CCCCCCCC)=O)OC(CCCCCCC/C=C\\CCCCCCCC)=O',
                                      'name': '1-[(9Z)-octadecenyl]-2,3-dioleoylglycerol',
                                      'reason': 'Found 2 ester groups, need '
                                                'exactly 3'},
                                  {   'smiles': 'O(CCCCCCCCCCCCCCCCCC)[C@@H](COC(=O)CCCCCCCCCCCCC)COC(=O)CCCCCCC/C=C\\C/C=C\\C/C=C\\CC',
                                      'name': '(2S)-2-(Octadecyloxy)-3-(tetradecanoyloxy)propyl '
                                              '(9Z,12Z,15Z)-octadeca-9,12,15-trienoate',
                                      'reason': 'Found 2 ester groups, need '
                                                'exactly 3'},
                                  {   'smiles': 'CCCCCCCCCCCCCCCCOC[C@H](COC(=O)CCCCCCC)OC(C)=O',
                                      'name': '1-palmityl-2-acetyl-3-capryloyl-sn-glycerol',
                                      'reason': 'Found 2 ester groups, need '
                                                'exactly 3'}],
    'attempt': 0,
    'reasoning': 'To classify a molecule as a triradylglycerol, we need to '
                 'ensure that it has a glycerol backbone with three '
                 'substituent groups (acyl, alkyl, or alk-1-enyl) attached at '
                 'the sn-1, sn-2, and sn-3 positions. The glycerol backbone is '
                 'a key feature, and the substituents should be attached via '
                 'ester bonds.\n'
                 '\n'
                 'Here is the Python program that implements this '
                 'classification:',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 1178,
    'num_false_positives': 6,
    'num_true_negatives': 141096,
    'num_false_negatives': 20,
    'num_negatives': None,
    'precision': 0.9949324324324325,
    'recall': 0.9833055091819699,
    'f1': 0.9890848026868178,
    'accuracy': 0.9998172874209417,
    'negative_predictive_value': 0.9998582726267752}