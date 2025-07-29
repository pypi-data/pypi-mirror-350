"""
Classifies: CHEBI:26125 phytosterols
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_phytosterols(smiles: str):
    """
    Determines if a molecule is a phytosterol based on its SMILES string.
    Phytosterols are sterols similar to cholesterol which occur in plants 
    and may vary in carbon side chains and/or presence or absence of a double bond.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a phytosterol, False otherwise
        str: Reason for classification
    """
    
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
    
    # Steroid backbone pattern: Tetracyclic
    steroid_pattern = Chem.MolFromSmarts("C1CCC2C1(CCC3C2CCC4C3(CCCC4)C)C")
    if not mol.HasSubstructMatch(steroid_pattern):
        return False, "No tetracyclic steroid backbone found"
    
    # Check for various common side chains and modifications
    # We'll use basic checks here - in practice phytosterols can vary widely
    double_bond_pattern = Chem.MolFromSmarts("C=C")
    if mol.HasSubstructMatch(double_bond_pattern):
        shared_double_bonds = True
    else:
        shared_double_bonds = False
        
    # Represent common side chain variations for phytosterols as SMARTS patterns
    farnesyl_chain_pattern = Chem.MolFromSmarts("C(C)CC=C(C)C")
    if mol.HasSubstructMatch(farnesyl_chain_pattern):
        side_chain_match = True
    else:
        side_chain_match = False

    # Conclusion based on substructure matches
    if shared_double_bonds and side_chain_match:
        return True, "Contains common phytosterol modifications (double bonds and possible farnesyl chain)"
    
    return False, "Lacks distinct side chain modifications typical of phytosterols"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:26125',
                          'name': 'phytosterols',
                          'definition': 'Sterols similar to cholesterol which '
                                        'occur in plants and vary only in '
                                        'carbon side chains and/or presence or '
                                        'absence of a double bond.',
                          'parents': ['CHEBI:15889', 'CHEBI:26124'],
                          'xrefs': ['Wikipedia:Phytosterol'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': None,
    'message': None,
    'sample_true_negatives': [   {   'smiles': 'C[C@@H]1OC(=O)C=C1',
                                     'name': '(S)-5-methylfuran-2(5H)-one',
                                     'reason': 'No tetracyclic steroid '
                                               'backbone found'},
                                 {   'smiles': 'Cc1cccc(c1)C(O)=O',
                                     'name': 'm-toluic acid',
                                     'reason': 'No tetracyclic steroid '
                                               'backbone found'},
                                 {   'smiles': 'CN(C)CC(=O)NC[C@@H]1[C@@H]([C@@H](N1)CO)C2=CC=C(C=C2)C3=CC=CC(=C3)C#N',
                                     'name': 'N-[[(2S,3S,4R)-3-[4-(3-cyanophenyl)phenyl]-4-(hydroxymethyl)-2-azetidinyl]methyl]-2-(dimethylamino)acetamide',
                                     'reason': 'No tetracyclic steroid '
                                               'backbone found'},
                                 {   'smiles': 'C[C@@H]1O[C@@H](OCCCCCCCCCC(=O)CC(O)=O)[C@H](O)C[C@H]1O',
                                     'name': 'bkos#20',
                                     'reason': 'No tetracyclic steroid '
                                               'backbone found'},
                                 {   'smiles': 'C([C@@](COC(CCCCCCCCC/C=C\\CCCCCC)=O)(OC(CCCCCCCCC/C=C\\CCCCCC)=O)[H])OP(=O)(O)OC[C@@](CO)([H])O',
                                     'name': 'PG(18:1(11Z)/18:1(11Z))',
                                     'reason': 'No tetracyclic steroid '
                                               'backbone found'},
                                 {   'smiles': 'O=C(N1C(C(=O)NC(C(=O)NC(C(=O)NC(C(=O)NC(C(=O)NC(CO)CC=2C3=C(C=CC=C3)NC2)CCC(=O)N)(C)C)(C)C)(CC)C)CCC1)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)CNC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C)CC4=CC=CC=C4)(C)C)CO)(C)C)(C)C)CC(C)C)CCC(=O)N)(C)C)(C)C)C)C)(C)C',
                                     'name': 'Chrysospermin B',
                                     'reason': 'No tetracyclic steroid '
                                               'backbone found'},
                                 {   'smiles': 'CC1(C=CC2=C3C(=CC(=C2O1)OC)C(=O)C(=CO3)C4=CC5=C(C=C4OC)OCO5)C',
                                     'name': '6-methoxy-3-(6-methoxy-1,3-benzodioxol-5-yl)-8,8-dimethyl-4-pyrano[2,3-h][1]benzopyranone',
                                     'reason': 'No tetracyclic steroid '
                                               'backbone found'},
                                 {   'smiles': 'O[C@@H]([C@H](NC(=O)[C@@H](N)CCC(O)=O)C(=O)NCC(O)=O)C',
                                     'name': 'Glu-Thr-Gly',
                                     'reason': 'No tetracyclic steroid '
                                               'backbone found'},
                                 {   'smiles': 'O([C@H]1[C@H](O[C@@H]2O[C@H]([C@@H](O)[C@@H](O)[C@@H]2O)C)[C@@H](NC(=O)C)[C@@H](O[C@@H]1CO)O[C@H]3[C@@H](O)[C@H](O)[C@H](O[C@@H]3OC[C@H]4O[C@@H](O[C@H]5[C@H](O)[C@@H](NC(=O)C)C(O[C@@H]5CO)O)[C@@H](O)[C@@H](O)[C@@H]4O)CO)[C@@H]6O[C@@H]([C@H](O)[C@H](O[C@]7(O[C@H]([C@H](NC(=O)C)[C@@H](O)C7)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]6O)CO',
                                     'name': '(2S,4S,5R,6R)-5-Acetamido-2-[(2S,3R,4S,5S,6R)-2-[(2R,3S,4R,5R,6S)-5-acetamido-6-[(2S,3S,4S,5S,6R)-2-[[(2R,3S,4S,5S,6S)-6-[(2R,3S,4R,5R)-5-acetamido-4,6-dihydroxy-2-(hydroxymethyl)oxan-3-yl]oxy-3,4,5-trihydroxyoxan-2-yl]methoxy]-4,5-dihydroxy-6-(hydroxymethyl)oxan-3-yl]oxy-2-(hydroxymethyl)-4-[(2S,3S,4R,5S,6S)-3,4,5-trihydroxy-6-methyloxan-2-yl]oxyoxan-3-yl]oxy-3,5-dihydroxy-6-(hydroxymethyl)oxan-4-yl]oxy-4-hydroxy-6-[(1R,2R)-1,2,3-trihydroxypropyl]oxane-2-carboxylic '
                                             'acid',
                                     'reason': 'No tetracyclic steroid '
                                               'backbone found'},
                                 {   'smiles': 'COCCOC(C)C(O)=O',
                                     'name': '2-(2-methoxyethoxy)propanoic '
                                             'acid',
                                     'reason': 'No tetracyclic steroid '
                                               'backbone found'}],
    'sample_false_negatives': [   {   'smiles': '[H][C@@]12CC=C3C[C@@H](O)CC[C@]3(C)[C@@]1([H])CC[C@@]1(C)[C@@]2([H])CC[C@]1([H])[C@@](C)(O)\\C=C\\[C@@H](CC)C(C)C',
                                      'name': 'leucisterol',
                                      'reason': 'No tetracyclic steroid '
                                                'backbone found'},
                                  {   'smiles': '[H][C@@]1(CC[C@@]2([H])[C@]3([H])CC=C4C[C@@H](O)CC[C@]4(C)[C@@]3([H])CC[C@]12C)[C@H](C)[C@@H](O)C[C@@H](CC)C(C)C',
                                      'name': '(22S)-hydroxysitosterol',
                                      'reason': 'No tetracyclic steroid '
                                                'backbone found'},
                                  {   'smiles': '[C@]1([C@@H](CCCC(C)C)C)([C@]2(CC[C@@]3([C@]4(CC[C@@H](C[C@]4(CC[C@]3([C@@]2(CC1)[H])[H])[H])O)C)[H])C)[H]',
                                      'name': 'coprostanol',
                                      'reason': 'Lacks distinct side chain '
                                                'modifications typical of '
                                                'phytosterols'},
                                  {   'smiles': '[C@]123[C@@]4([C@]([C@@]([C@@H](O)CC4)(C=O)C)(CC[C@]1([C@]5(C)CC[C@@]([C@@]5(C)CC2)([C@@H](CCC(C(C)C)=C)C)[H])[H])[H])C3',
                                      'name': '3beta-hydroxy-24-methylene-9beta-9,19-cyclolanostan-28-al',
                                      'reason': 'Lacks distinct side chain '
                                                'modifications typical of '
                                                'phytosterols'},
                                  {   'smiles': 'C1[C@@]([C@@]2([C@@](C1)(C3=CC[C@@]4([H])[C@H](C=O)[C@@H](O)CC[C@]4(C)[C@]3(CC2)[H])[H])C)([C@H](C)CCC(=C)C(C)C)[H]',
                                      'name': '4alpha-formyl-ergosta-7,24(28)-dien-3beta-ol',
                                      'reason': 'No tetracyclic steroid '
                                                'backbone found'},
                                  {   'smiles': '[H][C@@]1(CC[C@@]2([H])[C@]3([H])CC=C4C[C@@H](O)CC[C@]4(C)[C@@]3([H])CC[C@]12C)[C@H](C)\\C=C\\[C@@H](CC)C(C)C',
                                      'name': 'stigmasterol',
                                      'reason': 'No tetracyclic steroid '
                                                'backbone found'},
                                  {   'smiles': '[H][C@@]1(CC[C@@]2([H])C3=CC=C4C[C@@H](O)CC[C@]4(C)[C@@]3([H])CC[C@]12C)[C@H](C)CC[C@H](C)C(C)C',
                                      'name': 'ergosta-5,7-dien-3beta-ol',
                                      'reason': 'No tetracyclic steroid '
                                                'backbone found'},
                                  {   'smiles': '[C@@]12(CC[C@@H](C[C@@]1(CC[C@@]3([C@@]2(CC[C@]4([C@]3(CC[C@@]4([C@@](CC[C@H](C(C)C)CC)(C)[H])[H])[H])C)[H])[H])[H])O)C',
                                      'name': 'stigmastanol',
                                      'reason': 'Lacks distinct side chain '
                                                'modifications typical of '
                                                'phytosterols'},
                                  {   'smiles': 'O([C@@]1(C(C=2[C@@]([C@@]3(C([C@]4([C@@]([C@](C(C4([H])[H])([H])[H])([C@](C([H])([H])[H])(/C(=C(/[C@](C(C([H])([H])[H])(C([H])([H])[H])[H])(C(C([H])([H])[H])([H])[H])[H])\\[H])/[H])[H])[H])(C(C3([H])[H])([H])[H])C([H])([H])[H])[H])=C(C2[H])[H])[H])(C(C1([H])[H])([H])[H])C([H])([H])[H])([H])[H])[H])[H]',
                                      'name': 'delta7-stigmasterol',
                                      'reason': 'No tetracyclic steroid '
                                                'backbone found'},
                                  {   'smiles': '[C@@]12([C@]3([C@@]([C@@]4(C(C[C@@H](O)CC4)=CC3)C)(CC[C@@]1([C@@]([C@@H](/C=C/[C@@H](C(C)C)C)C)(CC2)[H])C)[H])[H])[H]',
                                      'name': 'brassicasterol',
                                      'reason': 'No tetracyclic steroid '
                                                'backbone found'}],
    'attempt': 0,
    'reasoning': 'To classify chemical entities as phytosterols based on their '
                 'SMILES strings, we need to identify specific structural '
                 'features typically found in phytosterols. Phytosterols are '
                 'sterols found in plants that resemble cholesterol. The key '
                 'structural features of phytosterols include:\n'
                 '\n'
                 '1. Sterol backbone: A tetracyclic structure with the core '
                 'structure similar to cholesterol.\n'
                 '2. Variations in carbon side chains: Different substitutions '
                 'on the rings or the side chains.\n'
                 '3. Presence or absence of a double bond.\n'
                 '\n'
                 'The general approach will be:\n'
                 '- Parse the SMILES string to create an RDKit molecule '
                 'object.\n'
                 '- Check for the presence of a sterol backbone.\n'
                 '- Identify common patterns for phytosterols, like specific '
                 'side-chain variations and the presence or absence of double '
                 'bonds.\n'
                 '- Return whether the molecule is a phytosterol along with a '
                 'reason for the classification.\n'
                 '\n'
                 'The SMILES string is parsed using RDKit, which allows us to '
                 'look for specific substructure patterns.\n'
                 '\n'
                 "Here's how you can implement it in Python using the RDKit "
                 'library:',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 3,
    'num_false_positives': 48,
    'num_true_negatives': 142227,
    'num_false_negatives': 22,
    'num_negatives': None,
    'precision': 0.058823529411764705,
    'recall': 0.12,
    'f1': 0.07894736842105263,
    'accuracy': 0.9995080815179199,
    'negative_predictive_value': 0.9998453416192733}