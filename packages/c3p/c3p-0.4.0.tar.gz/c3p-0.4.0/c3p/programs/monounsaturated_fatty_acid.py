"""
Classifies: CHEBI:25413 monounsaturated fatty acid
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_monounsaturated_fatty_acid(smiles: str):
    """
    Determines if a molecule is a monounsaturated fatty acid (MUFA) based on its SMILES string.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if the molecule is a MUFA, False otherwise
        str: Reason for classification
    """
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for carboxylic acid group
    carboxyl_pattern = Chem.MolFromSmarts("C(=O)[O,OH]")
    if not mol.HasSubstructMatch(carboxyl_pattern):
      return False, "No carboxylic acid group found"
    
    # Count double and triple bonds
    num_double_bonds = len(mol.GetSubstructMatches(Chem.MolFromSmarts("C=C")))
    num_triple_bonds = len(mol.GetSubstructMatches(Chem.MolFromSmarts("C#C")))

    total_unsaturations = num_double_bonds + num_triple_bonds
    
    if total_unsaturations != 1:
        return False, f"Molecule has {total_unsaturations} double/triple bonds, should have exactly 1"
      
    # Get the number of carbons in the fatty acid chain (number of carbons - those in the carboxyl group)
    c_count = sum(1 for atom in mol.GetAtoms() if atom.GetAtomicNum() == 6)
    
    #check for rings
    ring_info = mol.GetRingInfo()
    if ring_info.NumRings() > 1:
         return False, "Contains more than one ring."
    
    if ring_info.NumRings() == 1:
        ring_atoms = set(ring_info.AtomRings()[0])
        if not len(ring_atoms) == 3:
            return False, "Ring contains more than 3 atoms"
            
    # Check for fatty acid chain length
    if c_count < 10 or c_count > 30 :
        return False, f"Carbon chain length ({c_count}) is not within range [10-30] for a fatty acid"
    
    # Check that every other bond is a single bond, this is complicated, but might work.
    saturated_pattern = Chem.MolFromSmarts("C-C")
    saturated_matches = len(mol.GetSubstructMatches(saturated_pattern))
    
    if num_double_bonds == 1:
      carbon_count_single_bonds = c_count -1
    elif num_triple_bonds ==1:
      carbon_count_single_bonds = c_count -2
    else:
      return False, f"No unsaturation identified"
    
    if saturated_matches != carbon_count_single_bonds -1 :
        return False, f"Chain has more than 1 unsaturated bond: {saturated_matches} bonds found, {carbon_count_single_bonds -1} expected"
            
    return True, "Monounsaturated fatty acid identified"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:25413',
                          'name': 'monounsaturated fatty acid',
                          'definition': 'Any fatty acid with one double or '
                                        'triple bond in the fatty acid chain '
                                        'and singly bonded carbon atoms in the '
                                        'rest of the chain. MUFAs have '
                                        'positive effects on the '
                                        'cardiovascular system, and in '
                                        'diabetes treatment.',
                          'parents': ['CHEBI:27208'],
                          'xrefs': ['PMID:10584045', 'PMID:12936956'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 47,
                           'log_lines_of_code': 3.8501476017100584,
                           'indent_by_line': [   1,
                                                 1,
                                                 0,
                                                 1,
                                                 2,
                                                 0,
                                                 1,
                                                 2,
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 3,
                                                 3,
                                                 1,
                                                 1,
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 3,
                                                 1],
                           'max_indent': 3,
                           'imports': [   'from rdkit import Chem',
                                          'from rdkit.Chem import AllChem',
                                          'from rdkit.Chem import '
                                          'rdMolDescriptors'],
                           'imports_count': 3,
                           'methods_called': [   'GetSubstructMatches',
                                                 'MolFromSmarts',
                                                 'GetAtomicNum',
                                                 'NumRings',
                                                 'GetAtoms',
                                                 'AtomRings',
                                                 'HasSubstructMatch',
                                                 'MolFromSmiles',
                                                 'GetRingInfo'],
                           'methods_called_count': 9,
                           'smarts_strings': [   '"C=C"))',
                                                 'C-C',
                                                 '"C#C"))',
                                                 'C(=O)[O,OH]'],
                           'smarts_strings_count': 4,
                           'defs': [   'is_monounsaturated_fatty_acid(smiles: '
                                       'str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "No carboxylic acid group '
                                          'found"',
                                          'False, f"Molecule has '
                                          '{total_unsaturations} double/triple '
                                          'bonds, should have exactly 1"',
                                          'False, "Contains more than one '
                                          'ring."',
                                          'False, "Ring contains more than 3 '
                                          'atoms"',
                                          'False, f"Carbon chain length '
                                          '({c_count}) is not within range '
                                          '[10-30] for a fatty acid"',
                                          'False, f"No unsaturation '
                                          'identified"',
                                          'False, f"Chain has more than 1 '
                                          'unsaturated bond: '
                                          '{saturated_matches} bonds found, '
                                          '{carbon_count_single_bonds -1} '
                                          'expected"',
                                          'True, "Monounsaturated fatty acid '
                                          'identified"'],
                           'returns_count': 9,
                           'complexity': 5.170029520342012},
    'message': None,
    'sample_true_negatives': [   {   'smiles': 'CCN1N=C(N=N1)C2=CC=CC=C2NC(=O)C3=CC=C(C=C3)N4C=NN=N4',
                                     'name': 'N-[2-(2-ethyl-5-tetrazolyl)phenyl]-4-(1-tetrazolyl)benzamide',
                                     'reason': 'No carboxylic acid group '
                                               'found'},
                                 {   'smiles': 'CCS(=O)(=O)N1CC2(C1)[C@@H]([C@@H](N2C(=O)C3CCCC3)CO)C4=CC=C(C=C4)C=CC',
                                     'name': 'LSM-38092',
                                     'reason': 'No carboxylic acid group '
                                               'found'},
                                 {   'smiles': 'O=C/1N/C(/C(=O)N\\C1=C\\C2=CC=CC=C2)=C\\C=3N=CNC3C(C=C)(C)C',
                                     'name': 'DeltaPLH',
                                     'reason': 'No carboxylic acid group '
                                               'found'},
                                 {   'smiles': 'C1CCN(CC1)C(=O)C[C@H]2C[C@@H]3[C@H]([C@@H](O2)CO)OC4=C3C=C(C=C4)NC(=O)CC5CC5',
                                     'name': 'N-[(1S,3R,4aS,9aR)-1-(hydroxymethyl)-3-[2-oxo-2-(1-piperidinyl)ethyl]-3,4,4a,9a-tetrahydro-1H-pyrano[3,4-b]benzofuran-6-yl]-2-cyclopropylacetamide',
                                     'reason': 'No carboxylic acid group '
                                               'found'},
                                 {   'smiles': 'C[C@H]1C[C@@]2(OC(=O)c3ccccc3)[C@H]([C@H]1OC(C)=O)[C@@H](O)\\C(C)=C/C[C@H]1[C@@H](\\C=C(C)\\C2=O)C1(C)C',
                                     'name': '(-)-(6Z,12E,2S,3S,4R,5R,9S,11S,15R)-3-acetoxy-15-benzoyloxylathyra-6,12-dien-5-ol-14-one',
                                     'reason': 'Molecule has 2 double/triple '
                                               'bonds, should have exactly 1'},
                                 {   'smiles': 'O=C1C(O)=CC=2O[C@]3([C@H](O)C[C@@H]4[C@](OC=5C=C(O)C(C=C(C5C4)C)=O)(CC=CC(C[C@H]3CC2C(=C1)C)(C)C)C)C',
                                     'name': 'Eupenifeldin',
                                     'reason': 'No carboxylic acid group '
                                               'found'},
                                 {   'smiles': 'O1[C@@H](O[C@@H]2[C@@H](OC[C@H]3O[C@@H](O[C@H]4[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]4CO)O[C@H]5[C@H](O)[C@@H](NC(=O)C)C(O[C@@H]5CO[C@@H]6O[C@H]([C@@H](O)[C@@H](O)[C@@H]6O)C)O)[C@@H](O)[C@@H](O[C@H]7O[C@@H]([C@@H](O)[C@H](O)[C@@H]7O[C@@H]8O[C@@H]([C@@H](O[C@@H]9O[C@@H]([C@H](O)[C@H](O)[C@H]9NC(=O)C)CO)[C@H](O)[C@H]8NC(=O)C)CO)CO)[C@@H]3O)O[C@@H]([C@@H](O)[C@@H]2O)CO)[C@H](NC(=O)C)[C@@H](O[C@@H]%10O[C@H]([C@@H](O)[C@@H](O)[C@@H]%10O)C)[C@H](O[C@@H]%11O[C@@H]([C@H](O)[C@H](O)[C@H]%11NC(=O)C)CO)[C@H]1CO',
                                     'name': 'N-[(3R,4R,5S,6R)-5-[(2S,3R,4R,5S,6R)-3-Acetamido-5-[(2S,3S,4S,5R,6R)-4-[(2R,3S,4S,5S,6R)-3-[(2S,3R,4R,5S,6R)-3-acetamido-5-[(2S,3R,4R,5R,6R)-3-acetamido-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-6-[[(2S,3S,4S,5S,6R)-3-[(2S,3R,4R,5S,6R)-3-acetamido-5-[(2S,3R,4R,5R,6R)-3-acetamido-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-6-(hydroxymethyl)-4-[(2R,3S,4R,5S,6S)-3,4,5-trihydroxy-6-methyloxan-2-yl]oxyoxan-2-yl]oxy-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxymethyl]-3,5-dihydroxyoxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-2,4-dihydroxy-6-[[(2R,3S,4R,5S,6S)-3,4,5-trihydroxy-6-methyloxan-2-yl]oxymethyl]oxan-3-yl]acetamide',
                                     'reason': 'No carboxylic acid group '
                                               'found'},
                                 {   'smiles': 'CN1C[C@@H]2C[C@H](Cn3c2cccc3=O)[C@H]1CC=C',
                                     'name': 'Tinctorine',
                                     'reason': 'No carboxylic acid group '
                                               'found'},
                                 {   'smiles': 'CCC1=C2COC(CC2=C3C(=C(OC3=N1)C(=O)C4=CC=CC=C4)N)(C)C',
                                     'name': 'LSM-4563',
                                     'reason': 'No carboxylic acid group '
                                               'found'},
                                 {   'smiles': 'CN1CCN(CC1)C(=O)C[C@@H]2CC[C@H]3[C@H](O2)COC[C@@H](CN3C(=O)NC4=CC5=C(C=C4)OCO5)O',
                                     'name': '(3R,6aS,8S,10aS)-N-(1,3-benzodioxol-5-yl)-3-hydroxy-8-[2-(4-methyl-1-piperazinyl)-2-oxoethyl]-3,4,6,6a,8,9,10,10a-octahydro-2H-pyrano[2,3-c][1,5]oxazocine-1-carboxamide',
                                     'reason': 'No carboxylic acid group '
                                               'found'}],
    'sample_false_negatives': [   {   'smiles': 'C(/C=C/CCC)(O)=O',
                                      'name': '(2E)-hexenoic acid',
                                      'reason': 'Carbon chain length (6) is '
                                                'not within range [10-30] for '
                                                'a fatty acid'},
                                  {   'smiles': 'CCCCCCCCC1=C(CCCCCCC(O)=O)C1',
                                      'name': 'malvalic acid',
                                      'reason': 'Chain has more than 1 '
                                                'unsaturated bond: 17 bonds '
                                                'found, 16 expected'},
                                  {   'smiles': 'CCCC\\C=C\\C(O)=O',
                                      'name': '(E)-hept-2-enoic acid',
                                      'reason': 'Carbon chain length (7) is '
                                                'not within range [10-30] for '
                                                'a fatty acid'},
                                  {   'smiles': 'C(CCCCC[C@H]1[C@H](C(CC1)=O)C/C=C\\CC)(O)=O',
                                      'name': '(9R,13R)-1a,1b-dinor-10,11-dihydro-12-oxo-15-phytoenoic '
                                              'acid',
                                      'reason': 'Ring contains more than 3 '
                                                'atoms'},
                                  {   'smiles': 'CCC/C(=C/C(O)=O)/C',
                                      'name': '(2E)-3-methylhex-2-enoic acid',
                                      'reason': 'Carbon chain length (7) is '
                                                'not within range [10-30] for '
                                                'a fatty acid'},
                                  {   'smiles': 'OC(=O)CC=C(C)C',
                                      'name': '4-methylpent-3-enoic acid',
                                      'reason': 'Carbon chain length (6) is '
                                                'not within range [10-30] for '
                                                'a fatty acid'},
                                  {   'smiles': 'CCCCCCCCCCCC#CCCCCC(O)=O',
                                      'name': 'tariric acid',
                                      'reason': 'Chain has more than 1 '
                                                'unsaturated bond: 16 bonds '
                                                'found, 15 expected'},
                                  {   'smiles': 'OC[C@H]1O[C@@H](O[C@@H]2[C@@H](O)[C@H](O)[C@@H](CO)O[C@H]2OCCCCCCCC\\C=C/CCCCCCCC([O-])=O)[C@H](O)[C@@H](O)[C@@H]1O',
                                      'name': '(9Z)-18-hydroxyoctadec-9-enoate '
                                              '18-O-sophoroside',
                                      'reason': 'Contains more than one ring.'},
                                  {   'smiles': '[H]C(CC)=CC(O)=O',
                                      'name': 'pent-2-enoic acid',
                                      'reason': 'Carbon chain length (5) is '
                                                'not within range [10-30] for '
                                                'a fatty acid'},
                                  {   'smiles': '[H]C(CCCC)=CC(O)=O',
                                      'name': '2-heptenoic acid',
                                      'reason': 'Carbon chain length (7) is '
                                                'not within range [10-30] for '
                                                'a fatty acid'}],
    'attempt': 0,
    'reasoning': "Okay, let's analyze the characteristics of a monounsaturated "
                 'fatty acid (MUFA) and devise a strategy to classify them '
                 'using RDKit.\n'
                 '\n'
                 '**Characteristics of a MUFA:**\n'
                 '\n'
                 '1.  **Fatty Acid Backbone:** It has a long hydrocarbon chain '
                 '(typically 12-24 carbons).\n'
                 '2.  **Carboxylic Acid Group:** It contains a -COOH '
                 '(carboxyl) group at one end.\n'
                 '3.  **One Double or Triple Bond:** It possesses exactly one '
                 'double or triple bond (unsaturation) within the hydrocarbon '
                 'chain.\n'
                 '4.  **Single Bonds Elsewhere:** All other carbon-carbon '
                 'bonds in the chain must be single bonds.\n'
                 '\n'
                 '**Classification Strategy:**\n'
                 '\n'
                 '1.  **Parse SMILES:** Convert the SMILES string into an '
                 'RDKit molecule object. Handle potential invalid SMILES.\n'
                 '2.  **Check Carboxylic Acid:** Verify the presence of a '
                 'carboxylic acid group (-C(=O)O or -COOH).\n'
                 '3.  **Count Unsaturations:** Count the total number of '
                 'double and triple bonds. Ensure there is exactly one.\n'
                 '4.  **Check Chain Length:** Verify that the carbon chain is '
                 'within the typical length of a fatty acid (10-24 carbons).\n'
                 '5.  **Verify No Other Unsaturation:** Ensure that there are '
                 'no other double/triple bonds within the chain besides the '
                 'one we identified earlier.\n'
                 '6.  **Check for Rings** There should be no other rings '
                 'besides the cyclopropane ring.',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 154,
    'num_false_positives': 377,
    'num_true_negatives': 141718,
    'num_false_negatives': 51,
    'num_negatives': None,
    'precision': 0.2900188323917137,
    'recall': 0.751219512195122,
    'f1': 0.4184782608695652,
    'accuracy': 0.9969922698524245,
    'negative_predictive_value': 0.9996402598593487}