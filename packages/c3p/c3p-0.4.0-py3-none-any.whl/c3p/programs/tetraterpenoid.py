"""
Classifies: CHEBI:26935 tetraterpenoid
"""
"""
Classifies: CHEBI tetraterpenoid
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_tetraterpenoid(smiles: str):
    """
    Determines if a molecule is a tetraterpenoid based on its SMILES string.
    A tetraterpenoid is a terpenoid derived from a tetraterpene.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a tetraterpenoid, False otherwise
        str: Reason for classification
    """
    
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Calculate molecular weight
    mol_wt = rdMolDescriptors.CalcExactMolWt(mol)
    if mol_wt < 500:
        return False, "Molecular weight too low for tetraterpenoid"

    # Check for isoprene units
    isoprene_pattern = Chem.MolFromSmarts("C=C(C)C=C(C)")
    if isoprene_pattern is None:
        return None, "Failed to parse isoprene pattern"
    isoprene_matches = mol.GetSubstructMatches(isoprene_pattern)
    if len(isoprene_matches) < 4:
        return False, f"Found {len(isoprene_matches)} isoprene units, need at least 4"

    # Check for conjugated double bonds
    conjugated_pattern = Chem.MolFromSmarts("C=C/C=C")
    if conjugated_pattern is None:
        return None, "Failed to parse conjugated pattern"
    conjugated_matches = mol.GetSubstructMatches(conjugated_pattern)
    if len(conjugated_matches) < 3:
        return False, f"Found {len(conjugated_matches)} conjugated double bonds, need at least 3"

    # Check for methyl groups
    methyl_pattern = Chem.MolFromSmarts("[CX4H3]")
    if methyl_pattern is None:
        return None, "Failed to parse methyl pattern"
    methyl_matches = mol.GetSubstructMatches(methyl_pattern)
    if len(methyl_matches) < 5:
        return False, f"Found {len(methyl_matches)} methyl groups, need at least 5"

    # Count carbons and oxygens
    c_count = sum(1 for atom in mol.GetAtoms() if atom.GetAtomicNum() == 6)
    o_count = sum(1 for atom in mol.GetAtoms() if atom.GetAtomicNum() == 8)
    
    if c_count < 30:
        return False, "Too few carbons for tetraterpenoid"
    if o_count > 15:
        return False, "Too many oxygens for tetraterpenoid"

    return True, "Contains isoprene units, conjugated double bonds, and methyl groups consistent with tetraterpenoid structure"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:26935',
                          'name': 'tetraterpenoid',
                          'definition': 'Any terpenoid derived from a '
                                        'tetraterpene. The term includes '
                                        'compounds in which the C40 skeleton '
                                        'of the parent tetraterpene has been '
                                        'rearranged or modified by the removal '
                                        'of one or more skeletal atoms '
                                        '(generally methyl groups).',
                          'parents': ['CHEBI:26873'],
                          'xrefs': ['LIPID_MAPS_class:LMPR0107'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': None,
    'message': '\n'
               'Error: Python argument types in\n'
               '    Mol.GetSubstructMatches(Mol, NoneType)\n'
               'did not match C++ signature:\n'
               '    GetSubstructMatches(RDKit::ROMol self, RDKit::MolBundle '
               'query, RDKit::SubstructMatchParameters params)\n'
               '    GetSubstructMatches(RDKit::ROMol self, RDKit::ROMol query, '
               'RDKit::SubstructMatchParameters params)\n'
               '    GetSubstructMatches(RDKit::ROMol self, RDKit::MolBundle '
               'query, bool uniquify=True, bool useChirality=False, bool '
               'useQueryQueryMatches=False, unsigned int maxMatches=1000)\n'
               '    GetSubstructMatches(RDKit::ROMol self, RDKit::ROMol query, '
               'bool uniquify=True, bool useChirality=False, bool '
               'useQueryQueryMatches=False, unsigned int maxMatches=1000)\n'
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
                                     'reason': 'Molecular weight too low for '
                                               'tetraterpenoid'},
                                 {   'smiles': 'C[C@H]1CN(C(=O)C2=C(C=CC(=C2)NC(=O)CC3=CC=CC=C3)O[C@@H]1CN(C)CC4=CC=C(C=C4)C(F)(F)F)[C@@H](C)CO',
                                     'name': 'N-[(2S,3S)-5-[(2S)-1-hydroxypropan-2-yl]-3-methyl-2-[[methyl-[[4-(trifluoromethyl)phenyl]methyl]amino]methyl]-6-oxo-3,4-dihydro-2H-1,5-benzoxazocin-8-yl]-2-phenylacetamide',
                                     'reason': 'Found 0 isoprene units, need '
                                               'at least 4'},
                                 {   'smiles': '[H][C@]12CN3C4=C([C@@H](COC(N)=O)[C@@]3(OC)[C@@]1([H])N2)C(=O)C(NCCSSC1=CC=C(C=C1)[N+]([O-])=O)=C(C)C4=O',
                                     'name': 'BMY-25067',
                                     'reason': 'Found 0 isoprene units, need '
                                               'at least 4'},
                                 {   'smiles': 'O=C1C2=C(O)C(=C(O)C=C2C(=O)C=3C1=C(O)C=C(O)C3)/C=C/CCCC',
                                     'name': 'Averythrin',
                                     'reason': 'Molecular weight too low for '
                                               'tetraterpenoid'},
                                 {   'smiles': 'CC=CC1=CC=C(C=C1)[C@@H]2[C@H]3CN(CC(=O)N3[C@@H]2CO)S(=O)(=O)C4=CC=CC=C4',
                                     'name': 'LSM-41791',
                                     'reason': 'Molecular weight too low for '
                                               'tetraterpenoid'},
                                 {   'smiles': 'CC1=CC2=C(C=C1)N(C3=NC4=CC=CC=C4N=C23)CCN5CCOCC5',
                                     'name': '4-[2-(9-methyl-6-indolo[3,2-b]quinoxalinyl)ethyl]morpholine',
                                     'reason': 'Molecular weight too low for '
                                               'tetraterpenoid'},
                                 {   'smiles': 'CC(C)C[C@H](NC(=O)[C@H](C)N)C(=O)N[C@@H](CC(C)C)C(=O)N[C@@H]([C@@H](C)O)C(O)=O',
                                     'name': 'Ala-Leu-Leu-Thr',
                                     'reason': 'Molecular weight too low for '
                                               'tetraterpenoid'},
                                 {   'smiles': 'O(C=1C(=C(O)C=C(O)C1)C(=O)/C=C/C2=CC=C(O)C=C2)C',
                                     'name': 'Helichrysetin',
                                     'reason': 'Molecular weight too low for '
                                               'tetraterpenoid'},
                                 {   'smiles': 'O([C@H]1[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]1CO)O[C@H]2[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]2CO)O)[C@@H]3O[C@@H]([C@@H](O)[C@H](O[C@H]4O[C@@H]([C@@H](O)[C@H](O)[C@@H]4O)CO)[C@@H]3O)CO[C@H]5O[C@@H]([C@@H](OC6O[C@@H]([C@@H](O)[C@H](O)[C@H]6NC(=O)C)CO)[C@H](O)[C@@H]5O)CO',
                                     'name': 'N-[(2R,3R,4R,5S,6R)-5-[(2S,3R,4R,5S,6R)-3-Acetamido-5-[(2S,3S,4S,5R,6R)-6-[[(2S,3S,4R,5S,6R)-5-[(3R,4R,5S,6R)-3-acetamido-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-3,4-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxymethyl]-3,5-dihydroxy-4-[(2R,3S,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-2,4-dihydroxy-6-(hydroxymethyl)oxan-3-yl]acetamide',
                                     'reason': 'Found 0 isoprene units, need '
                                               'at least 4'},
                                 {   'smiles': 'C[C@H]1CN(C(=O)CCCN2C=C(CO[C@@H]1CN(C)C(=O)C3CC3)N=N2)[C@H](C)CO',
                                     'name': 'N-[[(8S,9S)-6-[(2R)-1-hydroxypropan-2-yl]-8-methyl-5-oxo-10-oxa-1,6,13,14-tetrazabicyclo[10.2.1]pentadeca-12(15),13-dien-9-yl]methyl]-N-methylcyclopropanecarboxamide',
                                     'reason': 'Molecular weight too low for '
                                               'tetraterpenoid'}],
    'sample_false_negatives': [   {   'smiles': 'O(C(CCC/C(=C/C=C/C(=C/C=C/C(=C/C=C/C=C(/CC/C=C(/CC/C=C(/CCC=C(C)C)\\C)\\C)\\C)/C)/C)/C)(C)C)C',
                                      'name': '3,4,11′,12′-tetrahydrospheroidene',
                                      'reason': 'Found 2 isoprene units, need '
                                                'at least 4'},
                                  {   'smiles': 'C(\\CC/C=C(/CCCC(C)(C)O)\\C)(=C/C=C/C(=C/C=C/C=C(/C=C/C=C(/C=C/C=C(/CCCC(C)(C)O)\\C)\\C)\\C)/C)/C',
                                      'name': "1,1'-dihydroxyneurosporene",
                                      'reason': 'Found 3 isoprene units, need '
                                                'at least 4'},
                                  {   'smiles': 'CC(\\C=C\\C=C(/C)C1OC2(C)CC(O)CC(C)(C)C2=C1)=C/C=C/C=C(C)/C=C/C=C(\\C)C1OC2(C)CC(O)CC(C)(C)C2=C1',
                                      'name': 'auroxanthin',
                                      'reason': 'Found 2 isoprene units, need '
                                                'at least 4'},
                                  {   'smiles': 'CC(C)=CCC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\[C@@H]1[C@@H](COP(O)(=O)OP(O)(O)=O)[C@]1(C)CC\\C=C(/C)CC\\C=C(/C)CCC=C(C)C',
                                      'name': '(1R,2R,3R)-prephytoene '
                                              'diphosphate',
                                      'reason': 'Found 0 isoprene units, need '
                                                'at least 4'},
                                  {   'smiles': 'CCC(C)CCCCCCCCCCC(=O)OC[C@H]1O[C@@H](OC(=O)C(\\C)=C\\C=C\\C(C)=C\\C=C\\C(C)=C\\C=C\\C=C(C)\\C=C\\C=C(/C)CCC=C(C)C)[C@H](O)[C@@H](O)[C@@H]1O',
                                      'name': 'staphyloxanthin',
                                      'reason': 'Found 3 isoprene units, need '
                                                'at least 4'},
                                  {   'smiles': 'COC(C)(C)CCC(=O)C(\\C)=C\\C=C\\C(C)=C\\C=C\\C(C)=C\\C=C\\C=C(C)\\C=C\\C=C(C)\\C=C\\c1ccc(C)c(C)c1C',
                                      'name': 'Okenone',
                                      'reason': 'Found 3 isoprene units, need '
                                                'at least 4'},
                                  {   'smiles': 'O[C@@H]1CC([C@H](C(=C1)C)\\C=C\\C(\\C)=C\\C=C\\C(\\C)=C\\C=C\\C=C(\\C=C\\C=C(\\C(=O)CC=2C(C[C@H](O)CC2C)(C)C)/COC(=O)/C=C/CCCCCCCCC)/C)(C)C',
                                      'name': 'Siphonaxanthin ester/ '
                                              'Siphonaxanthin dodecenoate/ '
                                              '(Siphonein)',
                                      'reason': 'Found 3 isoprene units, need '
                                                'at least 4'},
                                  {   'smiles': 'CC(\\C=C\\C=C(/C)C(O)=O)=C/C=C/C=C(C)/C=C/C=C(\\C)C(O)=O',
                                      'name': 'crocetin',
                                      'reason': 'Molecular weight too low for '
                                                'tetraterpenoid'},
                                  {   'smiles': 'OC/C(=C/CC1C(C(C(C)=CC1)/C=C/C(=C/C=C/C(=C/C=C/C=C(/CC/C=C(/CC/C=C(/CCC=C(C)C)\\C)\\C)\\C)/C)/C)(C)C)/C',
                                      'name': 'Nonaprenoxanthin',
                                      'reason': 'Found 2 isoprene units, need '
                                                'at least 4'},
                                  {   'smiles': 'O1C2(C1(CCCC2(C)C)C)\\C=C/C(/C)=C\\C=C\\C(\\C)=C\\C=C/C=C(/C=C/C=C(\\C3OC4(C(C(CCC4)(C)C)=C3)C)/C)\\C',
                                      'name': "(5R,5'R,6S,8'R)-Luteochrome",
                                      'reason': 'Found 3 isoprene units, need '
                                                'at least 4'}],
    'attempt': 2,
    'reasoning': 'Based on the previous program and the outcomes provided, it '
                 'appears that the function `is_tetraterpenoid` is not '
                 'correctly classifying molecules as tetraterpenoids. The '
                 'error message suggests that the `GetSubstructMatches` '
                 'function is being called with a `None` value, which '
                 'indicates that the `Chem.MolFromSmarts` function is not '
                 'successfully parsing the SMARTS string.\n'
                 '\n'
                 'Upon reviewing the code, it seems that the SMARTS strings '
                 'used to define the patterns for isoprene units, conjugated '
                 'double bonds, and methyl groups may be incorrect or too '
                 'specific. Additionally, the thresholds for the number of '
                 'isoprene units, conjugated double bonds, and methyl groups '
                 'may be too strict, causing the function to incorrectly '
                 'classify molecules.\n'
                 '\n'
                 'To improve the function, the following steps can be taken:\n'
                 '\n'
                 '1.  **Verify the SMARTS strings**: Ensure that the SMARTS '
                 'strings used to define the patterns are correct and match '
                 'the expected structures of tetraterpenoids.\n'
                 '2.  **Relax the thresholds**: Consider relaxing the '
                 'thresholds for the number of isoprene units, conjugated '
                 'double bonds, and methyl groups to allow for more '
                 'flexibility in the classification.\n'
                 '3.  **Add additional checks**: Consider adding additional '
                 'checks to verify the presence of other characteristic '
                 'features of tetraterpenoids, such as the presence of '
                 'specific functional groups or ring systems.\n'
                 '4.  **Use more advanced cheminformatics techniques**: '
                 'Consider using more advanced cheminformatics techniques, '
                 'such as machine learning or fingerprint-based approaches, to '
                 'classify molecules as tetraterpenoids.\n'
                 '\n'
                 "Here's an updated version of the code that addresses some of "
                 'these issues:',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 171,
    'num_false_positives': 65,
    'num_true_negatives': 142033,
    'num_false_negatives': 31,
    'num_negatives': None,
    'precision': 0.7245762711864406,
    'recall': 0.8465346534653465,
    'f1': 0.7808219178082192,
    'accuracy': 0.9993253689388616,
    'negative_predictive_value': 0.9997817884896948}