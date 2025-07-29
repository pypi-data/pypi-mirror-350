"""
Classifies: CHEBI:27300 vitamin D
"""
"""
Classifies: CHEBI:17855 vitamin D
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_vitamin_D(smiles: str):
    """
    Determines if a molecule is a vitamin D based on its SMILES string.
    Vitamin D compounds are characterized by a seco-steroid backbone with a conjugated triene system and hydroxyl groups.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a vitamin D, False otherwise
        str: Reason for classification
    """
    
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Look for the seco-steroid backbone with a conjugated triene system
    seco_steroid_pattern = Chem.MolFromSmarts("[C@H]1CC[C@@H]2[C@@]1(CCC/C2=C/C=C3/C[C@@H](O)CCC3=C)")
    if not mol.HasSubstructMatch(seco_steroid_pattern):
        return False, "No seco-steroid backbone with conjugated triene system found"

    # Check for at least one hydroxyl group (typical in vitamin D compounds)
    hydroxyl_pattern = Chem.MolFromSmarts("[OX2H]")
    hydroxyl_matches = mol.GetSubstructMatches(hydroxyl_pattern)
    if len(hydroxyl_matches) < 1:
        return False, "No hydroxyl groups found"

    # Check for a flexible side chain at position 17
    side_chain_pattern = Chem.MolFromSmarts("[C@@H](CCCC(C)C)")
    if not mol.HasSubstructMatch(side_chain_pattern):
        return False, "No flexible side chain at position 17 found"

    # Check molecular weight - vitamin D compounds typically >300 Da
    mol_wt = rdMolDescriptors.CalcExactMolWt(mol)
    if mol_wt < 300:
        return False, "Molecular weight too low for vitamin D"

    # Count carbons and oxygens
    c_count = sum(1 for atom in mol.GetAtoms() if atom.GetAtomicNum() == 6)
    o_count = sum(1 for atom in mol.GetAtoms() if atom.GetAtomicNum() == 8)
    
    if c_count < 20:
        return False, "Too few carbons for vitamin D"
    if o_count < 1:
        return False, "Must have at least one oxygen (hydroxyl group)"

    return True, "Contains seco-steroid backbone with conjugated triene system and hydroxyl groups"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:27300',
                          'name': 'vitamin D',
                          'definition': 'Any member of a group of fat-soluble '
                                        'hydroxy seco-steroids that exhibit '
                                        'biological activity against vitamin D '
                                        'deficiency. Vitamin D  can be '
                                        'obtained from sun exposure, food and '
                                        'supplements and is biologically '
                                        'inactive and converted into the '
                                        'biologically active calcitriol via '
                                        'double hydroxylation in the body.',
                          'parents': ['CHEBI:36853'],
                          'xrefs': ['MetaCyc:Vitamin-D', 'Wikipedia:Vitamin_D'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': None,
    'message': None,
    'sample_true_negatives': [   {   'smiles': 'OC[C@H]1O[C@H](C[C@@H]1O)N1C=NC2=C1N=CNC[C@H]2O',
                                     'name': 'pentostatin',
                                     'reason': 'No seco-steroid backbone with '
                                               'conjugated triene system '
                                               'found'},
                                 {   'smiles': 'O1C(CCC=2C1=CC(OC3OC(C(O)C(O)C3O)C(O)=O)=C(C2OC)C=4C(=O)C=5C(OC4)=CC(O)=C(O)C5)(C)C',
                                     'name': '6-{[6-(6,7-dihydroxy-4-oxo-4H-chromen-3-yl)-5-methoxy-2,2-dimethyl-3,4-dihydro-2H-1-benzopyran-7-yl]oxy}-3,4,5-trihydroxyoxane-2-carboxylic '
                                             'acid',
                                     'reason': 'No seco-steroid backbone with '
                                               'conjugated triene system '
                                               'found'},
                                 {   'smiles': 'O=C1O[C@@H]([C@@H](OC)C=CC=C(C[C@@H](C)[C@@H]([C@@H]([C@@H]([C@@H](C=C(C=C1OC)C)C)O)C)O)C)[C@H]([C@@H](O)[C@@H]([C@@]2(O[C@H](/C=C/C)[C@@H](C)[C@@H](C2)OC3OC(C(O)C(C3)O)C)O)C)C',
                                     'name': 'Concanamycin D',
                                     'reason': 'No seco-steroid backbone with '
                                               'conjugated triene system '
                                               'found'},
                                 {   'smiles': 'O1[C@@H](O[C@@H]2[C@@H](O)[C@@H](O[C@@H]([C@@H]2O)CO)O[C@H]3[C@H](O)[C@@H](NC(=O)C)C(O[C@@H]3CO)O)[C@H](NC(=O)C)[C@@H](O[C@@H]4O[C@@H]([C@H](O)[C@H](O)[C@H]4O)CO)[C@H](O[C@@H]5O[C@H]([C@@H](O)[C@@H](O)[C@@H]5O)C)[C@H]1CO',
                                     'name': 'N-[(3R,4R,5S,6R)-5-[(2S,3R,4S,5S,6R)-4-[(2S,3R,4R,5S,6R)-3-Acetamido-6-(hydroxymethyl)-4-[(2R,3R,4S,5R,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-5-[(2S,3S,4R,5S,6S)-3,4,5-trihydroxy-6-methyloxan-2-yl]oxyoxan-2-yl]oxy-3,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-2,4-dihydroxy-6-(hydroxymethyl)oxan-3-yl]acetamide',
                                     'reason': 'No seco-steroid backbone with '
                                               'conjugated triene system '
                                               'found'},
                                 {   'smiles': 'O=C(O)[C@]1([C@H]2[C@@](OC=3C=C4C5=C(C=CC=C5)NC4=CC3CC2)(CC[C@@H]1O)C)C',
                                     'name': 'Oxiamycin',
                                     'reason': 'No seco-steroid backbone with '
                                               'conjugated triene system '
                                               'found'},
                                 {   'smiles': 'C1CCC(C1)CC#CC2=CC=C(C=C2)[C@@H]3[C@@H]4CN(CC(=O)N4[C@@H]3CO)C(=O)C5=CC=C(C=C5)F',
                                     'name': '(6R,7R,8S)-7-[4-(3-cyclopentylprop-1-ynyl)phenyl]-4-[(4-fluorophenyl)-oxomethyl]-8-(hydroxymethyl)-1,4-diazabicyclo[4.2.0]octan-2-one',
                                     'reason': 'No seco-steroid backbone with '
                                               'conjugated triene system '
                                               'found'},
                                 {   'smiles': 'S(=O)(C(SSCCC)CC)CCC',
                                     'name': 'Propyl 1-(propylsulfinyl)propyl '
                                             'disulfide',
                                     'reason': 'No seco-steroid backbone with '
                                               'conjugated triene system '
                                               'found'},
                                 {   'smiles': 'ClC=1C(=O)[C@@H]([C@@](O)(C/C=C\\CCCCC)C1)C[C@H](OC(=O)C)[C@@H](OC(=O)C)CCCC(OC)=O',
                                     'name': 'punaglandin 6',
                                     'reason': 'No seco-steroid backbone with '
                                               'conjugated triene system '
                                               'found'},
                                 {   'smiles': 'CCCCCCCCCCCCCCCCCCCCCCCC[C@H](O)C(=O)N[C@@H](COP(O)(=O)O[C@H]1[C@H](O)[C@@H](O)[C@H](O)[C@@H](O)[C@H]1O)[C@H](O)[C@@H](O)CCCCCCCCCCCCCC',
                                     'name': 'Ins-1-P-Cer(t18:0/2-OH-26:0)',
                                     'reason': 'No seco-steroid backbone with '
                                               'conjugated triene system '
                                               'found'},
                                 {   'smiles': 'CCC(C)(C)C(=O)OC1CC(C=C2C1[C@H]([C@H](C=C2)C)CC[C@@H]3CC(CC(=O)O3)O)C',
                                     'name': '2,2-dimethylbutanoic acid '
                                             '[(7S,8S)-8-[2-[(2R)-4-hydroxy-6-oxo-2-oxanyl]ethyl]-3,7-dimethyl-1,2,3,7,8,8a-hexahydronaphthalen-1-yl] '
                                             'ester',
                                     'reason': 'No seco-steroid backbone with '
                                               'conjugated triene system '
                                               'found'}],
    'sample_false_negatives': [   {   'smiles': 'O[C@@H]1CC=2[C@H](\\C=C/3\\[C@]4([C@@]([C@](CC4)([C@@H](CCCC(C)C)C)[H])(CCC3)C)[H])CC2CC1',
                                      'name': '(7E)-(3S,6S)-6,19-cyclo-9,10-seco-5(10),7-cholestadien-3-ol',
                                      'reason': 'No seco-steroid backbone with '
                                                'conjugated triene system '
                                                'found'},
                                  {   'smiles': 'OC(CCC[C@H]([C@@]1([C@@]2([C@@](CC1)(/C(/C=C(C2)C#CCO)=C/C=C\\3/C[C@@H](O)C[C@H](O)C3=C)[H])C)[H])C)(C)C',
                                      'name': '1alpha,25-dihydroxy-11-(3-hydroxy-1-propynyl)-9,11-didehydrovitamin '
                                              'D3',
                                      'reason': 'No seco-steroid backbone with '
                                                'conjugated triene system '
                                                'found'},
                                  {   'smiles': 'C(=C\\C1=C(CC[C@]2([C@]1(CC[C@]2([H])[C@](CCCC(C)(C)O)([H])C)[2H])C)[2H])\\C3=C([C@H](C[C@@H](C3)O)O)C([2H])([2H])[2H]',
                                      'name': '9,14,19,19,19-pentadeuterio-1alpha,25-dihydroxyprevitamin '
                                              'D3',
                                      'reason': 'No seco-steroid backbone with '
                                                'conjugated triene system '
                                                'found'},
                                  {   'smiles': 'S(=O)(=O)(\\C=C\\C[C@H](C=1[C@@]2([C@@](CC1)(/C(/CCC2)=C/C=C\\3/C[C@@H](O)C[C@H](O)C3=C)[H])C)C)C(C)(C)C',
                                      'name': 'Lunacalcipol',
                                      'reason': 'No seco-steroid backbone with '
                                                'conjugated triene system '
                                                'found'},
                                  {   'smiles': 'OC(CCC[C@H]([C@@]1([C@@]2([C@@](CC1)(/C(/CCC2)=C/C=C/3\\C[C@@H](O)/C(/[C@H](O)C3)=C/CCOCOC)[H])C)[H])C)(C)C',
                                      'name': "1alpha,25-Dihydroxy-2-[3'-(methoxymethoxy)propylidene]-19-norvitamin "
                                              'D3',
                                      'reason': 'No seco-steroid backbone with '
                                                'conjugated triene system '
                                                'found'},
                                  {   'smiles': 'S(C[C@@H](C=1[C@@]2([C@@](CC1)(/C(/CCC2)=C/C=C/3\\C[C@@H](O)C[C@H](O)C3)[H])C)C)C=4C=C(C(O)(C)C)C=CC4',
                                      'name': 'VD 2656',
                                      'reason': 'No seco-steroid backbone with '
                                                'conjugated triene system '
                                                'found'},
                                  {   'smiles': 'OC(CCC[C@H](C=1[C@@]2([C@@H](CC1)/C(/CCC2)=C/CC3C([C@H](O)CC(O)=C3)=C)C)C)(C)C',
                                      'name': '1,25-Dihydroxy-16-ene-vitamin '
                                              'D3',
                                      'reason': 'No seco-steroid backbone with '
                                                'conjugated triene system '
                                                'found'},
                                  {   'smiles': 'O=C(O)/C(=C\\C[C@H](OC(=O)C)[C@H]([C@@H]1[C@@]2([C@@](C3=C([C@@]4([C@H](C([C@@H](O)CC4)(C)C)CC3)C)CC2)(C)CC1)C)C)/C',
                                      'name': 'Ganocolobetausin H',
                                      'reason': 'No seco-steroid backbone with '
                                                'conjugated triene system '
                                                'found'},
                                  {   'smiles': 'FC(F)(CC[C@H]([C@@]1([C@@]2([C@@](CC1)(/C(/CCC2)=C/C3OOCC4=C3C[C@@H](O)CC4)[H])C)[H])C)C(O)(C)C',
                                      'name': '(6RS)-6,19-epidioxy-24,24-difluoro-25-hydroxy-6,19-dihydrovitamin '
                                              'D3 / '
                                              '(6RS)-6,19-epidioxy-24,24-difluoro-25-hydroxy-6,19-dihydrocholecalciferol',
                                      'reason': 'No seco-steroid backbone with '
                                                'conjugated triene system '
                                                'found'},
                                  {   'smiles': '[C@@](=C1CCC[C@]2([C@]1(CC[C@@]2([C@@](CCCC(C)C)(C)[H])[H])[H])C)=C(C=3C[C@H](CCC3C)O)[H]',
                                      'name': '(3S,6S)-9,10-seco-5(10),6,7-cholestatrien-3-ol',
                                      'reason': 'No seco-steroid backbone with '
                                                'conjugated triene system '
                                                'found'}],
    'attempt': 0,
    'reasoning': 'To classify a molecule as vitamin D, we need to identify key '
                 'structural features that are characteristic of vitamin D '
                 'compounds. These features include:\n'
                 '\n'
                 '1. **Seco-steroid backbone**: A steroid-like structure with '
                 'a broken B-ring (9,10-seco-steroid).\n'
                 '2. **Hydroxy groups**: Presence of hydroxyl groups, '
                 'typically at positions 1, 3, and 25.\n'
                 '3. **Conjugated triene system**: A conjugated triene system '
                 'in the B-ring, which is essential for biological activity.\n'
                 '4. **Side chain**: A flexible side chain at position 17, '
                 'often containing additional hydroxyl groups or other '
                 'functional groups.\n'
                 '\n'
                 'The function `is_vitamin_D` will check for these features '
                 "using RDKit's substructure matching capabilities.",
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 156,
    'num_false_positives': 26,
    'num_true_negatives': 142080,
    'num_false_negatives': 38,
    'num_negatives': None,
    'precision': 0.8571428571428571,
    'recall': 0.8041237113402062,
    'f1': 0.8297872340425533,
    'accuracy': 0.999550245959241,
    'negative_predictive_value': 0.9997326165580714}