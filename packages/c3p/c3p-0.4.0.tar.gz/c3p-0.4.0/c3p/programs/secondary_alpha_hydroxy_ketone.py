"""
Classifies: CHEBI:2468 secondary alpha-hydroxy ketone
"""
"""
Classifies: secondary alpha-hydroxy ketone (acyloin)
Definition:
    A secondary α‐hydroxy ketone is an α‐hydroxy ketone in which the carbonyl group and the 
    hydroxy group are linked by a carbon bearing one hydrogen and one organyl group.
    This motif corresponds to R–CH(OH)–C(=O)–R′.
"""

from rdkit import Chem

def is_secondary_alpha_hydroxy_ketone(smiles: str):
    """
    Determines if a molecule is a secondary alpha-hydroxy ketone (acyloin) based on its SMILES string.
    The structure must contain the motif: R–CH(OH)–C(=O)–R′, where the CH bearing -OH is secondary.
    
    Args:
        smiles (str): SMILES string of the molecule.
        
    Returns:
        bool: True if the molecule contains the secondary alpha-hydroxy ketone motif, False otherwise.
        str : Reason for classification.
    """
    # Parse the SMILES string
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Define a SMARTS pattern for the acyloin (secondary alpha-hydroxy ketone) motif.
    # Explanation of the SMARTS:
    #   [C;H1]: a carbon with exactly one hydrogen (making it secondary)
    #   ([OX2H]): bearing an -OH group (O atom with two connections and one hydrogen)
    #   C(=O): next is a carbonyl group
    #   [#6]: the carbonyl carbon is attached to an organic substituent (a carbon atom)
    acyloin_smarts = "[C;H1]([OX2H])C(=O)[#6]"
    acyloin_pattern = Chem.MolFromSmarts(acyloin_smarts)
    
    # Check whether the molecule has at least one match to the acyloin SMARTS pattern.
    if mol.HasSubstructMatch(acyloin_pattern):
        return True, "Molecule contains the secondary alpha-hydroxy ketone (acyloin) motif"
    else:
        return False, "Does not contain the required secondary alpha-hydroxy ketone motif"

# Optional: Test examples can be added here if run as a script. 
# For instance:
# if __name__ == '__main__':
#     test_smiles = "O[C@H](C(=O)c1ccccc1)c1ccccc1"  # (S)-benzoin example
#     result, reason = is_secondary_alpha_hydroxy_ketone(test_smiles)
#     print(result, reason)


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:2468',
                          'name': 'secondary alpha-hydroxy ketone',
                          'definition': 'An alpha-hydroxy ketone in which the '
                                        'carbonyl group and the hydroxy group '
                                        'are linked by a carbon bearing one '
                                        'hydrogen and one organyl group. '
                                        'Secondary alpha-hydroxy ketones are '
                                        'also known as acyloins, and are '
                                        'formally derived from reductive '
                                        'coupling of two carboxylic acid '
                                        'groups.',
                          'parents': ['CHEBI:139588', 'CHEBI:35681'],
                          'xrefs': ['Wikipedia:Acyloin'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 26,
                           'log_lines_of_code': 3.258096538021482,
                           'indent_by_line': [   1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
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
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 1,
                                                 2,
                                                 0],
                           'max_indent': 2,
                           'imports': ['from rdkit import Chem'],
                           'imports_count': 1,
                           'methods_called': [   'HasSubstructMatch',
                                                 'MolFromSmarts',
                                                 'MolFromSmiles'],
                           'methods_called_count': 3,
                           'smarts_strings': ['acyloin_smarts'],
                           'smarts_strings_count': 1,
                           'defs': [   'is_secondary_alpha_hydroxy_ketone(smiles: '
                                       'str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'True, "Molecule contains the '
                                          'secondary alpha-hydroxy ketone '
                                          '(acyloin) motif"',
                                          'False, "Does not contain the '
                                          'required secondary alpha-hydroxy '
                                          'ketone motif"'],
                           'returns_count': 3,
                           'complexity': 2.4516193076042962},
    'message': None,
    'sample_true_negatives': [   {   'smiles': 'O=C(N[C@@H](C(O)(C)C)C)[C@H]([C@@]1([C@@]2([C@@](CC1)(/C(/CCC2)=C/C=C\\3/C[C@@H](O)C[C@H](O)C3=C)[H])C)[H])C',
                                     'name': '1alpha,25-dihydroxy-24-oxo-23-azavitamin '
                                             'D2 / '
                                             '1alpha,25-dihydroxy-24-oxo-23-azaergocalciferol',
                                     'reason': 'Does not contain the required '
                                               'secondary alpha-hydroxy ketone '
                                               'motif'},
                                 {   'smiles': 'CCCCCCCCCCCCCCCCCCC(O)C([O-])=O',
                                     'name': '2-hydroxyarachidate',
                                     'reason': 'Does not contain the required '
                                               'secondary alpha-hydroxy ketone '
                                               'motif'},
                                 {   'smiles': 'C[C@@H](CN([C@@H](C)CO)C(=O)NC1=CC=C(C=C1)C(F)(F)F)[C@@H](CN(C)C(=O)C2CCOCC2)OC',
                                     'name': 'N-[(2S,3S)-4-[[(2S)-1-hydroxypropan-2-yl]-[[4-(trifluoromethyl)phenyl]carbamoyl]amino]-2-methoxy-3-methylbutyl]-N-methyloxane-4-carboxamide',
                                     'reason': 'Does not contain the required '
                                               'secondary alpha-hydroxy ketone '
                                               'motif'},
                                 {   'smiles': 'CC(=O)CC\\C=C(/C)CCC=C(C)C',
                                     'name': 'geranyl acetone',
                                     'reason': 'Does not contain the required '
                                               'secondary alpha-hydroxy ketone '
                                               'motif'},
                                 {   'smiles': 'O([C@H]1[C@H](O)[C@H](O[C@H](O)[C@H]1O)CO[C@H]2O[C@@H]([C@@H](O)[C@H](O)[C@@H]2O)CO)[C@H]3O[C@@H]([C@@H](O)[C@H](O)[C@@H]3O[C@H]4O[C@@H]([C@@H](O)[C@H](O)[C@@H]4O)CO)CO',
                                     'name': '(2S,3S,4S,5S,6R)-2-[[(2R,3R,4S,5S,6S)-4-[(2R,3S,4S,5S,6R)-4,5-Dihydroxy-6-(hydroxymethyl)-3-[(2R,3S,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-3,5,6-trihydroxyoxan-2-yl]methoxy]-6-(hydroxymethyl)oxane-3,4,5-triol',
                                     'reason': 'Does not contain the required '
                                               'secondary alpha-hydroxy ketone '
                                               'motif'},
                                 {   'smiles': 'O=C(OC1=C(C(O)=C(C(=O)O)C(=C1C)C)C)C2=C(OC)C(=C(OC(=O)C3=C(O)C=C(O)C=C3C)C=C2C)C',
                                     'name': 'Thielavin Z5',
                                     'reason': 'Does not contain the required '
                                               'secondary alpha-hydroxy ketone '
                                               'motif'},
                                 {   'smiles': '[C@@H]1([C@@H]([C@H]([C@@H]([C@H](O1)CO)O)O)NC(C)=O)O[C@@H]2[C@@H]([C@H](C(O[C@@H]2CO)O)O)O',
                                     'name': 'beta-D-GlcpNAc-(1->4)-D-Galp',
                                     'reason': 'Does not contain the required '
                                               'secondary alpha-hydroxy ketone '
                                               'motif'},
                                 {   'smiles': 'CN(C)C(=O)C1=CC=C(C=C1)C2=CC=C(C=C2)[C@@H]3[C@H]4CN(CC(=O)N4[C@H]3CO)C(=O)CC5CC5',
                                     'name': '4-[4-[(6S,7R,8R)-4-(2-cyclopropyl-1-oxoethyl)-8-(hydroxymethyl)-2-oxo-1,4-diazabicyclo[4.2.0]octan-7-yl]phenyl]-N,N-dimethylbenzamide',
                                     'reason': 'Does not contain the required '
                                               'secondary alpha-hydroxy ketone '
                                               'motif'},
                                 {   'smiles': 'CCCCCCCCCCCCCCCCCCCCC=C',
                                     'name': '1-docosene',
                                     'reason': 'Does not contain the required '
                                               'secondary alpha-hydroxy ketone '
                                               'motif'},
                                 {   'smiles': 'C([C@@](OC(=O)CCC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)([H])COC(=O)CC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)OC(=O)CCCCC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC',
                                     'name': 'TG(22:5(7Z,10Z,13Z,16Z,19Z)/20:5(5Z,8Z,11Z,14Z,17Z)/22:6(4Z,7Z,10Z,13Z,16Z,19Z))[iso6]',
                                     'reason': 'Does not contain the required '
                                               'secondary alpha-hydroxy ketone '
                                               'motif'}],
    'sample_false_negatives': [   {   'smiles': 'O=C1C=CC(C1(O)CO)=O',
                                      'name': 'G2201-C',
                                      'reason': 'Does not contain the required '
                                                'secondary alpha-hydroxy '
                                                'ketone motif'},
                                  {   'smiles': 'OC1(C(O)=C(C(O)=C(C1=O)C(=O)CC(C)C)CC=C(C)C)CC=C(C)C',
                                      'name': '(R)-Humulone',
                                      'reason': 'Does not contain the required '
                                                'secondary alpha-hydroxy '
                                                'ketone motif'},
                                  {   'smiles': 'O=C1C=C(N)C[C@@]1(O)C=C',
                                      'name': 'Myrothenone B',
                                      'reason': 'Does not contain the required '
                                                'secondary alpha-hydroxy '
                                                'ketone motif'},
                                  {   'smiles': 'O=C1C=C[C@@H]([C@]1(O)C(=O)CCCCCCCCCCCC)O',
                                      'name': 'Hygrophorone D12',
                                      'reason': 'Does not contain the required '
                                                'secondary alpha-hydroxy '
                                                'ketone motif'},
                                  {   'smiles': 'O=C1/C(/C(=O)[C@]2([C@H]3C(=C(O)C(=C([C@]3(O[C@]2([C@]1(O)C)O)C)O)C)C(=O)CC/C=C/C)C)=C(/O)\\C=C\\C=C\\C',
                                      'name': '10,11-dihydrobisvertinolone',
                                      'reason': 'Does not contain the required '
                                                'secondary alpha-hydroxy '
                                                'ketone motif'},
                                  {   'smiles': 'O=C1[C@]2(O)[C@@H]([C@@](C(=O)/C=C/OC)(C)[C@H]([C@@]1(O)C)[C@H](CC)C)[C@@H](C[C@](C2)(O)C)C',
                                      'name': '10-Hydroxy-18-methoxybetaenone',
                                      'reason': 'Does not contain the required '
                                                'secondary alpha-hydroxy '
                                                'ketone motif'},
                                  {   'smiles': 'O=C1NC(=C(C)C)C([C@]1(O)C/C=C/CC(O)C)=O',
                                      'name': 'Cladosporiumin D',
                                      'reason': 'Does not contain the required '
                                                'secondary alpha-hydroxy '
                                                'ketone motif'},
                                  {   'smiles': 'O=C1C=C(C#N)C[C@]1(O)C=C',
                                      'name': 'Homothallin II',
                                      'reason': 'Does not contain the required '
                                                'secondary alpha-hydroxy '
                                                'ketone motif'},
                                  {   'smiles': 'O=C1C=C[C@H]([C@]1(O)C(=O)CCCCCCCCCCCC)OC(=O)C',
                                      'name': '4-O-acetyl hygrophorone C12',
                                      'reason': 'Does not contain the required '
                                                'secondary alpha-hydroxy '
                                                'ketone motif'},
                                  {   'smiles': 'O=C1C=C(NC(=O)OC)C[C@@]1(O)C=C',
                                      'name': '(5R) '
                                              '5-hydroxy-3-[(methoxycarbonyl)amino]-5-vinyl-2-cyclopenten-1-one',
                                      'reason': 'Does not contain the required '
                                                'secondary alpha-hydroxy '
                                                'ketone motif'}],
    'attempt': 0,
    'reasoning': 'Below is the reasoning behind the approach. We need to '
                 'identify the acyloin (secondary α‐hydroxy ketone) motif. By '
                 'definition, the structure should contain the fragment '
                 'R–CH(OH)–C(=O)–R′. In this fragment the carbon bearing the '
                 '–OH group (the α‐carbon) must be secondary. That means it '
                 'must have exactly one hydrogen (CH) and be bound to the '
                 'hydroxy group and a carbonyl group (i.e. –C(=O)–) as well as '
                 'exactly one additional “organyl” substituent. We can capture '
                 'this pattern using a SMARTS string. One suitable SMARTS is '
                 '"[C;H1]([OX2H])C(=O)[#6]" where:\n'
                 '• "[C;H1]" forces the α‐carbon to be a carbon atom with '
                 'exactly one hydrogen.\n'
                 '• "([OX2H])" requires that an –OH group is attached.\n'
                 '• "C(=O)" matches the neighboring carbonyl unit.\n'
                 '• "[#6]" ensures that the carbonyl carbon is attached to '
                 'another carbon (an organic substituent).\n'
                 'We then check if the provided SMILES string yields a '
                 'molecule containing this substructure. If the match is found '
                 'we return True with an appropriate explanation. Otherwise, '
                 'we return False with a corresponding reason.\n'
                 '\n'
                 'Below is the Python code implementation.',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 162,
    'num_false_positives': 1098,
    'num_true_negatives': 141008,
    'num_false_negatives': 32,
    'num_negatives': None,
    'precision': 0.12857142857142856,
    'recall': 0.8350515463917526,
    'f1': 0.22283356258596973,
    'accuracy': 0.9920590302178496,
    'negative_predictive_value': 0.9997731140102099}