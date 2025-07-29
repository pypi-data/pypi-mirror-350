"""
Classifies: CHEBI:33916 aldopentose
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_aldopentose(smiles: str):
    """
    Determines if a molecule is an aldopentose based on its SMILES string.
    An aldopentose is a pentose with a (potential) aldehyde group at one end.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is an aldopentose, False otherwise
        str: Reason for classification
    """
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Count carbons and oxygens
    c_count = sum(1 for atom in mol.GetAtoms() if atom.GetAtomicNum() == 6)
    o_count = sum(1 for atom in mol.GetAtoms() if atom.GetAtomicNum() == 8)
    
    # Must have exactly 5 carbons
    if c_count != 5:
        return False, f"Must have exactly 5 carbons, found {c_count}"
    
    # Should have 5 oxygens (4 hydroxyls + 1 ring oxygen or aldehyde oxygen)
    if o_count != 5:
        return False, f"Must have exactly 5 oxygens, found {o_count}"

    # Check for cyclic sugar patterns
    furanose_pattern = Chem.MolFromSmarts("[C]1[O][C]([C][C]1)")  # 5-membered ring
    pyranose_pattern = Chem.MolFromSmarts("[C]1[O][C]([C][C][C]1)")  # 6-membered ring
    
    # Check for aldehyde pattern (for open chain forms)
    aldehyde_pattern = Chem.MolFromSmarts("[CH1](=O)")
    
    is_furanose = mol.HasSubstructMatch(furanose_pattern)
    is_pyranose = mol.HasSubstructMatch(pyranose_pattern)
    has_aldehyde = mol.HasSubstructMatch(aldehyde_pattern)
    
    if not (is_furanose or is_pyranose or has_aldehyde):
        return False, "Must be either a furanose, pyranose, or contain an aldehyde group"

    # Check for appropriate hydroxyl pattern
    hydroxyl_pattern = Chem.MolFromSmarts("[OH1]")
    hydroxyl_count = len(mol.GetSubstructMatches(hydroxyl_pattern))
    
    # Should have 4 or 5 hydroxyls (4 in cyclic form, 5 in open form)
    if hydroxyl_count not in [4, 5]:
        return False, f"Must have 4-5 hydroxyl groups, found {hydroxyl_count}"

    # Additional check for open chain form
    if has_aldehyde:
        # Verify it's a straight chain with hydroxyls
        chain_pattern = Chem.MolFromSmarts("[CH1](=O)[CH1][CH1][CH1][CH2]")
        if not mol.HasSubstructMatch(chain_pattern):
            return False, "Open chain form must have correct carbon backbone"
    
    # If we've made it here, it's an aldopentose
    form = "furanose" if is_furanose else "pyranose" if is_pyranose else "open chain"
    return True, f"Aldopentose in {form} form with correct number of carbons, oxygens, and hydroxyls"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:33916',
                          'name': 'aldopentose',
                          'definition': 'A pentose with a (potential) aldehyde '
                                        'group at one end.',
                          'parents': ['CHEBI:15693', 'CHEBI:25901'],
                          'xrefs': ['PMID:10723607'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': None,
    'message': None,
    'sample_true_negatives': [   {   'smiles': 'Cc1cc(C)c2Cc3c(C)cc(C)c(Cc4c(C)cc(C)c(Cc5c(C)cc(C)c(Cc1c2C)c5C)c4C)c3C',
                                     'name': '4,6,10,12,16,18,22,24,25,26,27,28-dodecamethylcalix[4]arene',
                                     'reason': 'Must have exactly 5 carbons, '
                                               'found 40'},
                                 {   'smiles': 'O=C1C(=C2C=C3[C@]([C@@H](C(C)C)[C@@H]([C@H]3O)OC(=O)C)(C)CC[C@]2(C)CC1)COC(=O)C',
                                     'name': 'Dahliane E',
                                     'reason': 'Must have exactly 5 carbons, '
                                               'found 24'},
                                 {   'smiles': 'O[C@@H]([C@H](NC(=O)[C@@H](N)CCC(O)=O)C(=O)N[C@@H](CC(C)C)C(O)=O)C',
                                     'name': 'Glu-Thr-Leu',
                                     'reason': 'Must have exactly 5 carbons, '
                                               'found 15'},
                                 {   'smiles': 'CCOc1ccc(NC(=O)C(C)O)cc1',
                                     'name': 'p-Lactophenetide',
                                     'reason': 'Must have exactly 5 carbons, '
                                               'found 11'},
                                 {   'smiles': 'O=C1NCC=2C1=C3C(N([C@@H]4O[C@H]([C@@H](O)[C@H]([C@H]4OC)O)C)C5=C3C=CC=C5)=C6NC7=C(C26)C=CC=C7',
                                     'name': "3'-epi-5'-methoxy-K252d",
                                     'reason': 'Must have exactly 5 carbons, '
                                               'found 27'},
                                 {   'smiles': 'O=C(OC1C(O)C(OC(C1O)CO)OCC2OC(OCC(OC(=O)CCCCCCCCCCCCCCC)COC(=O)CCCCCCC/C=C\\C/C=C\\C/C=C\\CC)C(O)C(C2O)O)CCCCCCCCCCCCCCC',
                                     'name': '[(2S)-2-hexadecanoyloxy-3-[(2S,3R,4S,5S,6R)-6-[[(2S,3R,4S,5S,6R)-4-hexadecanoyloxy-3,5-dihydroxy-6-(hydroxymethyl)tetrahydropyran-2-yl]oxymethyl]-3,4,5-trihydroxy-tetrahydropyran-2-yl]oxy-propyl] '
                                             '(9E,12E,15E)-octadeca-9,12,15-trienoate',
                                     'reason': 'Must have exactly 5 carbons, '
                                               'found 65'},
                                 {   'smiles': 'O=C1C2=C(O)C=C(OC)C=C2C(=O)C3=C1[C@@H]([C@@H](O)[C@]([C@@H]3O)(O)C)C',
                                     'name': 'Altersolanol G',
                                     'reason': 'Must have exactly 5 carbons, '
                                               'found 17'},
                                 {   'smiles': '[H][C@]1(O[C@](O)(C[C@H](O)[C@H]1NC(=O)CO)C([O-])=O)[C@H](O)[C@H](O)CO',
                                     'name': 'N-glycoloyl-alpha-neuraminate',
                                     'reason': 'Must have exactly 5 carbons, '
                                               'found 11'},
                                 {   'smiles': 'OC(C(O)C/C=C\\C/C=C\\C/C=C\\CC)C/C=C\\C/C=C\\CCC(O)=O',
                                     'name': '10,11-DiHDPE',
                                     'reason': 'Must have exactly 5 carbons, '
                                               'found 22'},
                                 {   'smiles': '[Na+].[H][C@]12SCC(C)=C(N1C(=O)[C@H]2NC(=O)[C@H](N)c1ccccc1)C([O-])=O',
                                     'name': 'cephalexin sodium',
                                     'reason': 'Must have exactly 5 carbons, '
                                               'found 16'}],
    'sample_false_negatives': [   {   'smiles': '[H]C(=O)[C@@](O)(CO)[C@H](O)[C@H](O)CO',
                                      'name': 'D-hamamelose',
                                      'reason': 'Must have exactly 5 carbons, '
                                                'found 6'},
                                  {   'smiles': 'OC[C@]1(O)[C@H](O)OC[C@@H](O)[C@H]1O',
                                      'name': 'beta-D-hamamelose',
                                      'reason': 'Must have exactly 5 carbons, '
                                                'found 6'}],
    'attempt': 0,
    'reasoning': "Let me help create a program to classify aldopentoses. Let's "
                 'break this down:\n'
                 '\n'
                 '1. An aldopentose is a monosaccharide that:\n'
                 '   - Has 5 carbons (pentose)\n'
                 '   - Contains an aldehyde group (or potential aldehyde in '
                 'cyclic form)\n'
                 '   - Can exist in both open-chain and cyclic forms\n'
                 '\n'
                 '2. Key characteristics to check:\n'
                 '   - Must have exactly 5 carbons\n'
                 '   - Must have the right number of oxygens (typically 5)\n'
                 '   - Must either have an aldehyde group or be in a cyclic '
                 'form that could open to form an aldehyde\n'
                 '   - Should have appropriate hydroxyl groups\n'
                 '\n'
                 "Here's the implementation:",
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 41,
    'num_false_positives': 10,
    'num_true_negatives': 142247,
    'num_false_negatives': 2,
    'num_negatives': None,
    'precision': 0.803921568627451,
    'recall': 0.9534883720930233,
    'f1': 0.8723404255319148,
    'accuracy': 0.9999156711173577,
    'negative_predictive_value': 0.9999859401472067}