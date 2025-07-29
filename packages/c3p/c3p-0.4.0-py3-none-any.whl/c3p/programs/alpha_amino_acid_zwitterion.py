"""
Classifies: CHEBI:78608 alpha-amino-acid zwitterion
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_alpha_amino_acid_zwitterion(smiles: str):
    """
    Determines if a molecule is an alpha-amino-acid zwitterion based on its SMILES string.
    An alpha-amino-acid zwitterion has an amino group and a carboxylate group attached to the same
    chiral alpha carbon, which is also connected to another substituent (e.g., alkyl, aryl, hydroxyl).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is an alpha-amino-acid zwitterion, False otherwise
        str: Reason for classification
    """
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Look for alpha-amino-acid zwitterion pattern
    zwitterion_pattern = Chem.MolFromSmarts("[C@H]([NH3+])([C,c])(C(=O)[O-])")
    zwitterion_matches = mol.GetSubstructMatches(zwitterion_pattern)
    if not zwitterion_matches:
        return False, "No alpha-amino-acid zwitterion pattern found"

    # Check for overall charge neutrality
    mol_charge = AllChem.GetFormalCharge(mol)
    if mol_charge != 0:
        return False, "Molecule is not charge-neutral"

    # Additional checks for alpha-amino-acid zwitterions
    # ...

    return True, "Molecule is an alpha-amino-acid zwitterion"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:78608',
                          'name': 'alpha-amino-acid zwitterion',
                          'definition': 'An amino acid-zwitterion obtained by '
                                        'transfer of a proton from the carboxy '
                                        'to the amino group of any alpha-amino '
                                        'acid; major species at pH 7.3.',
                          'parents': ['CHEBI:35238'],
                          'xrefs': ['MetaCyc:Alpha-Amino-Acids'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 26,
                           'log_lines_of_code': 3.258096538021482,
                           'indent_by_line': [   1,
                                                 1,
                                                 1,
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
                                                 2,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 0,
                                                 1,
                                                 1,
                                                 0,
                                                 1],
                           'max_indent': 2,
                           'imports': [   'from rdkit import Chem',
                                          'from rdkit.Chem import AllChem',
                                          'from rdkit.Chem import '
                                          'rdMolDescriptors'],
                           'imports_count': 3,
                           'methods_called': [   'MolFromSmarts',
                                                 'GetSubstructMatches',
                                                 'GetFormalCharge',
                                                 'MolFromSmiles'],
                           'methods_called_count': 4,
                           'smarts_strings': [   '[C@H]([NH3+])([C,c])(C(=O)[O-])'],
                           'smarts_strings_count': 1,
                           'defs': [   'is_alpha_amino_acid_zwitterion(smiles: '
                                       'str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "No alpha-amino-acid '
                                          'zwitterion pattern found"',
                                          'False, "Molecule is not '
                                          'charge-neutral"',
                                          'True, "Molecule is an '
                                          'alpha-amino-acid zwitterion"'],
                           'returns_count': 4,
                           'complexity': 2.851619307604296},
    'message': '\n'
               'Attempt failed: F1 score of 0 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: NONE\n'
               'False positives: NONE\n'
               'False negatives: SMILES: '
               'C([C@H]([C@H]([C@H](C)O)CO)[NH3+])(=O)[O-] NAME: '
               '(4S)-3(1),4-dihydroxy-L-isoleucine zwitterion REASON: MISSED '
               'Amino and carboxylate groups are not attached to the same '
               'chiral alpha carbon\n'
               ' * SMILES: [O-]C(=O)C([NH2+]C)(C)C NAME: '
               'N-methyl-aminoisobutyrate zwitterion REASON: MISSED Amino and '
               'carboxylate groups are not attached to the same chiral alpha '
               'carbon\n'
               ' * SMILES: O=C([O-])[C@@H]([NH3+])CCCCCSC NAME: '
               'L-trihomomethionine zwitterion REASON: MISSED Amino and '
               'carboxylate groups are not attached to the same chiral alpha '
               'carbon\n'
               ' * SMILES: CC(=O)[C@H]([NH3+])C([O-])=O NAME: '
               'L-2-amino-3-oxobutanoic acid zwitterion REASON: MISSED Amino '
               'and carboxylate groups are not attached to the same chiral '
               'alpha carbon\n'
               ' * SMILES: [C@@H](C(=O)[O-])(C=C)[NH3+] NAME: L-vinylglycine '
               'zwitterion REASON: MISSED Amino and carboxylate groups are not '
               'attached to the same chiral alpha carbon\n'
               ' * SMILES: C(C1[NH2+]CSC1)(=O)[O-] NAME: thioproline '
               'zwitterion REASON: MISSED Amino and carboxylate groups are not '
               'attached to the same chiral alpha carbon\n'
               ' * SMILES: O=C([O-])[C@@H]([NH3+])CCCCCCCSC NAME: '
               'L-pentahomomethionine zwitterion REASON: MISSED Amino and '
               'carboxylate groups are not attached to the same chiral alpha '
               'carbon\n'
               ' * SMILES: COC1=CC=C(C[C@H]([NH3+])C([O-])=O)C=C1 NAME: '
               'O-methyl-L-tyrosine zwitterion REASON: MISSED Amino and '
               'carboxylate groups are not attached to the same chiral alpha '
               'carbon\n'
               ' * SMILES: [NH3+][C@@H](CCC(=O)NCCc1ccc(O)cc1)C([O-])=O NAME: '
               'gamma-glutamyltyramine zwitterion REASON: MISSED Amino and '
               'carboxylate groups are not attached to the same chiral alpha '
               'carbon\n'
               ' * SMILES: C=CCSC[C@@H](C([O-])=O)[NH3+] NAME: S-allylcysteine '
               'zwitterion REASON: MISSED Amino and carboxylate groups are not '
               'attached to the same chiral alpha carbon\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'C[C@@H]1CN(S(=O)(=O)C2=C(C=C(C=C2)Br)O[C@@H]1CN(C)C(=O)NC3CCCC3)[C@H](C)CO',
                                     'name': '1-[[(4R,5S)-8-bromo-2-[(2R)-1-hydroxypropan-2-yl]-4-methyl-1,1-dioxo-4,5-dihydro-3H-6,1$l^{6},2-benzoxathiazocin-5-yl]methyl]-3-cyclopentyl-1-methylurea',
                                     'reason': 'No alpha-amino-acid zwitterion '
                                               'pattern found'},
                                 {   'smiles': 'C=1(C(=C2C(OC(C=3C=CC(O)=CC3)=CC2=O)=C(C1O)[C@@H]4[C@@H]([C@H]([C@@H](CO4)O)O)O)O)[C@H]5OC[C@@H]([C@@H]([C@H]5O)O)O',
                                     'name': '6-C-L-arabinopyranosyl-8-C-D-xylopyranosylapigenin',
                                     'reason': 'No alpha-amino-acid zwitterion '
                                               'pattern found'},
                                 {   'smiles': 'CCC(=O)N(C)C[C@@H]1[C@@H](CN(C(=O)C2=C(O1)N=CC(=C2)C#CC(C)C)[C@@H](C)CO)C',
                                     'name': 'N-[[(2S,3R)-5-[(2S)-1-hydroxypropan-2-yl]-3-methyl-8-(3-methylbut-1-ynyl)-6-oxo-3,4-dihydro-2H-pyrido[2,3-b][1,5]oxazocin-2-yl]methyl]-N-methylpropanamide',
                                     'reason': 'No alpha-amino-acid zwitterion '
                                               'pattern found'},
                                 {   'smiles': 'O([C@@H]1[C@H](O[C@]2(O[C@H]([C@H](NC(=O)CO)[C@@H](O)C2)[C@H](O)[C@H](O)CO)C(O)=O)[C@@H](O)[C@@H](O[C@@H]1CO)O[C@H]3[C@H](O)[C@@H](O)[C@@H](O[C@@H]3CO)O)[C@@H]4O[C@@H]([C@H](O)[C@H](O[C@@H]5O[C@@H]([C@H](O)[C@H](O[C@H]6O[C@@H]([C@H](O)[C@H](O)[C@H]6O)CO)[C@H]5O[C@@H]7O[C@H]([C@@H](O)[C@@H](O)[C@@H]7O)C)CO)[C@H]4NC(=O)C)CO',
                                     'name': '(2S,4S,5R,6R)-2-[(2R,3S,4R,5R,6S)-3-[(2S,3R,4R,5R,6R)-3-Acetamido-5-hydroxy-4-[(2R,3R,4S,5S,6R)-5-hydroxy-6-(hydroxymethyl)-4-[(2R,3R,4S,5R,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-3-[(2S,3S,4R,5S,6S)-3,4,5-trihydroxy-6-methyloxan-2-yl]oxyoxan-2-yl]oxy-6-(hydroxymethyl)oxan-2-yl]oxy-5-hydroxy-2-(hydroxymethyl)-6-[(2R,3S,4R,5R,6R)-4,5,6-trihydroxy-2-(hydroxymethyl)oxan-3-yl]oxyoxan-4-yl]oxy-4-hydroxy-5-[(2-hydroxyacetyl)amino]-6-[(1R,2R)-1,2,3-trihydroxypropyl]oxane-2-carboxylic '
                                             'acid',
                                     'reason': 'No alpha-amino-acid zwitterion '
                                               'pattern found'},
                                 {   'smiles': 'O=C1O[C@@H](CC(=O)N(O)CCC[C@@H](NC(=O)C)C(=O)O[C@@H](CC(=O)N(O)CCC[C@H](C(O[C@@H](CC(N(CCC[C@H]1NC(=O)C)O)=O)C)=O)NC(=O)C)C)C',
                                     'name': 'Vicibactin',
                                     'reason': 'No alpha-amino-acid zwitterion '
                                               'pattern found'},
                                 {   'smiles': 'P(OC[C@H](OC(=O)CCCCCCC/C=C\\CCCCCCCCC)COC(=O)CCCCCCC/C=C\\CCCC)(OCCN)(O)=O',
                                     'name': 'PE(14:1(9Z)/19:1(9Z))',
                                     'reason': 'No alpha-amino-acid zwitterion '
                                               'pattern found'},
                                 {   'smiles': 'C#CC#C',
                                     'name': 'buta-1,3-diyne',
                                     'reason': 'No alpha-amino-acid zwitterion '
                                               'pattern found'},
                                 {   'smiles': 'OC1=C(C=C2[C@H](CCCC2=C1)C)C(CO)C',
                                     'name': 'Hypoxylan A',
                                     'reason': 'No alpha-amino-acid zwitterion '
                                               'pattern found'},
                                 {   'smiles': 'CCCCCC(O)CC(=O)OC(CC([O-])=O)C[N+](C)(C)C',
                                     'name': '3-hydroxyoctanoylcarnitine',
                                     'reason': 'No alpha-amino-acid zwitterion '
                                               'pattern found'},
                                 {   'smiles': 'O=C1C(=O)C=2C(=O)N\\C(\\C2C(=C1/C=C/CCC)O)=C/C',
                                     'name': 'Pyranterrone A',
                                     'reason': 'No alpha-amino-acid zwitterion '
                                               'pattern found'}],
    'sample_false_negatives': [   {   'smiles': '[O-]C(=O)C([NH2+]C)(C)C',
                                      'name': 'N-methyl-aminoisobutyrate '
                                              'zwitterion',
                                      'reason': 'No alpha-amino-acid '
                                                'zwitterion pattern found'},
                                  {   'smiles': 'C(C1[NH2+]CSC1)(=O)[O-]',
                                      'name': 'thioproline zwitterion',
                                      'reason': 'No alpha-amino-acid '
                                                'zwitterion pattern found'},
                                  {   'smiles': 'C[NH2+][C@@H](Cc1c(S)ncn1C)C([O-])=O',
                                      'name': 'ovothiol B zwitterion',
                                      'reason': 'No alpha-amino-acid '
                                                'zwitterion pattern found'},
                                  {   'smiles': '[C@H]1(CCC[NH+]1C)C([O-])=O',
                                      'name': 'N-methylproline zwitterion',
                                      'reason': 'No alpha-amino-acid '
                                                'zwitterion pattern found'},
                                  {   'smiles': 'C[NH+](C)[C@@H](Cc1c(S)ncn1C)C([O-])=O',
                                      'name': 'ovothiol C zwitterion',
                                      'reason': 'No alpha-amino-acid '
                                                'zwitterion pattern found'},
                                  {   'smiles': '[NH3+][C@@H](CC([O-])=O)C([O-])=O',
                                      'name': 'L-aspartate(1-)',
                                      'reason': 'Molecule is not '
                                                'charge-neutral'},
                                  {   'smiles': 'O[C@H]1C[NH2+][C@@H](C1)C([O-])=O',
                                      'name': 'trans-4-hydroxy-L-proline '
                                              'zwitterion',
                                      'reason': 'No alpha-amino-acid '
                                                'zwitterion pattern found'},
                                  {   'smiles': 'O=C([O-])[C@@H](N)[C@@H](C)[NH3+]',
                                      'name': '(2S,3R)-diazaniumylbutanoate '
                                              'zwitterion',
                                      'reason': 'No alpha-amino-acid '
                                                'zwitterion pattern found'},
                                  {   'smiles': 'NC(=O)N[C@H]([NH3+])C([O-])=O',
                                      'name': '(S)-2-ureidoglycine zwitterion',
                                      'reason': 'No alpha-amino-acid '
                                                'zwitterion pattern found'},
                                  {   'smiles': '[C@H]1(C(N(C1)[C@H](C=2C=CC(=CC2)O)C(=O)[O-])=O)NC([C@@H](C3=CC=C(C=C3)OCC[C@H](C([O-])=O)[NH3+])NO)=O',
                                      'name': "2'-N-hydroxynocardicin C(1-)",
                                      'reason': 'Molecule is not '
                                                'charge-neutral'}],
    'attempt': 3,
    'reasoning': 'The previous program failed to correctly classify the '
                 'provided examples of alpha-amino-acid zwitterions due to a '
                 'few limitations in the approach:\n'
                 '\n'
                 '1. **Missed cases with other substituents**: The program '
                 'only checks if the amino and carboxylate groups are attached '
                 'to the same chiral alpha carbon. However, it does not '
                 'account for cases where additional substituents (e.g., side '
                 'chains, functional groups) are present on the alpha carbon. '
                 'Many of the provided examples have additional substituents '
                 'like hydroxy, alkyl, aryl, or heterocyclic groups.\n'
                 '\n'
                 '2. **Lack of specific pattern matching**: The program uses a '
                 'general SMARTS pattern for amino and carboxylate groups, but '
                 'does not explicitly match the specific patterns expected for '
                 'alpha-amino-acid zwitterions. This can lead to false '
                 'positives or missed cases.\n'
                 '\n'
                 '3. **No check for zwitterionic charge balance**: The program '
                 'does not verify if the overall charge of the molecule is '
                 'neutral, as expected for a zwitterion.\n'
                 '\n'
                 'To improve the classification, we can:\n'
                 '\n'
                 '1. Use more specific SMARTS patterns that capture the '
                 'expected structural features of alpha-amino-acid '
                 'zwitterions, including the presence of additional '
                 'substituents on the alpha carbon.\n'
                 '\n'
                 '2. Incorporate checks for the overall charge balance and '
                 'neutrality of the molecule.\n'
                 '\n'
                 '3. Consider additional structural features or molecular '
                 'descriptors that can aid in the classification, such as atom '
                 'counts, molecular weight ranges, or specific functional '
                 'group patterns.\n'
                 '\n'
                 "Here's an improved version of the code that addresses some "
                 'of these limitations:',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 70,
    'num_false_positives': 184,
    'num_true_negatives': 142034,
    'num_false_negatives': 12,
    'num_negatives': None,
    'precision': 0.2755905511811024,
    'recall': 0.8536585365853658,
    'f1': 0.41666666666666663,
    'accuracy': 0.9986226282501757,
    'negative_predictive_value': 0.999915520324402}