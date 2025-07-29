"""
Classifies: CHEBI:139588 alpha-hydroxy ketone
"""
"""
Classifies: CHEBI:2468 alpha-hydroxy ketone
"""
from rdkit import Chem

def is_alpha_hydroxy_ketone(smiles: str):
    """
    Determines if a molecule is an alpha-hydroxy ketone based on its SMILES string.
    An alpha-hydroxy ketone has a ketone group (C=O) with a hydroxyl (-OH) on the adjacent (alpha) carbon.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is an alpha-hydroxy ketone, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Improved SMARTS pattern: ketone with adjacent carbon containing hydroxyl (O with exactly 1 H)
    # [CX3]=O (ketone) adjacent to a carbon connected to [O;H1] (hydroxyl)
    pattern = Chem.MolFromSmarts('[CX3](=O)-[C;!$(C=O)]([O;H1])')
    if not pattern:
        return False, "Invalid SMARTS pattern"

    # Find all matches of the pattern
    matches = mol.GetSubstructMatches(pattern)
    if not matches:
        return False, "No ketone with alpha-hydroxy group detected"

    # Check if any matched ketone is valid (not part of acid/ester/amide)
    for match in matches:
        ketone_carbon = mol.GetAtomWithIdx(match[0])
        # Verify ketone environment (should have 2 carbons attached)
        carbon_neighbors = sum(1 for n in ketone_carbon.GetNeighbors() if n.GetAtomicNum() == 6)
        if carbon_neighbors >= 2:
            # Check alpha carbon's hydroxyl isn't part of conjugated system
            alpha_carbon = mol.GetAtomWithIdx(match[1])
            for bond in alpha_carbon.GetBonds():
                if bond.GetBondType() == Chem.BondType.DOUBLE and bond.GetOtherAtom(alpha_carbon).GetAtomicNum() == 8:
                    continue  # skip conjugated cases
            return True, "Contains ketone with hydroxyl group on adjacent alpha-carbon"

    return False, "No valid ketone with alpha-hydroxy group detected"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:139588',
                          'name': 'alpha-hydroxy ketone',
                          'definition': 'A ketone containing a hydroxy group '
                                        'on the alpha-carbon relative to the '
                                        'C=O group.',
                          'parents': ['CHEBI:17087', 'CHEBI:33822'],
                          'xrefs': [   'PMID:15326516',
                                       'PMID:19908854',
                                       'PMID:20382022',
                                       'PMID:23295224'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 34,
                           'log_lines_of_code': 3.5263605246161616,
                           'indent_by_line': [   1,
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
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 3,
                                                 3,
                                                 4,
                                                 5,
                                                 3,
                                                 0,
                                                 1],
                           'max_indent': 5,
                           'imports': ['from rdkit import Chem'],
                           'imports_count': 1,
                           'methods_called': [   'GetNeighbors',
                                                 'GetOtherAtom',
                                                 'GetBonds',
                                                 'GetBondType',
                                                 'GetSubstructMatches',
                                                 'MolFromSmarts',
                                                 'MolFromSmiles',
                                                 'GetAtomicNum',
                                                 'GetAtomWithIdx'],
                           'methods_called_count': 9,
                           'smarts_strings': ['[CX3](=O)-[C;!$(C=O)]([O;H1])'],
                           'smarts_strings_count': 1,
                           'defs': ['is_alpha_hydroxy_ketone(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "Invalid SMARTS pattern"',
                                          'False, "No ketone with '
                                          'alpha-hydroxy group detected"',
                                          'True, "Contains ketone with '
                                          'hydroxyl group on adjacent '
                                          'alpha-carbon"',
                                          'False, "No valid ketone with '
                                          'alpha-hydroxy group detected"'],
                           'returns_count': 5,
                           'complexity': 4.705272104923233},
    'message': '\n'
               'Attempt failed: F1 score of 0 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: NONE\n'
               'False positives: NONE\n'
               'False negatives: SMILES: '
               'COC(=O)[C@@]12C(=C)[C@@](C)(C[C@@H]3[C@]1(C)CC=C1C(C)(C)C(=O)C[C@@H](O)[C@@]31C)C(=O)[C@](C)(O)C2=O '
               'NAME: berkeleytrione REASON: MISSED No valid ketone with '
               'alpha-hydroxy group detected\n'
               ' * SMILES: '
               '[C@]12(CC=C3[C@@]([C@]1(C[C@H]([C@]4([C@@]2(CC[C@]4(C(=O)C)O)O)C)OC(=O)/C=C(\\C)/C(C)C)[H])(CC[C@@H](C3)O[C@@H]5O[C@@H]([C@@H](O[C@H]6C[C@H](OC)[C@@H]([C@H](O6)C)O[C@@H]7O[C@@H]([C@H]([C@@H](C7)OC)O)C)[C@H](C5)OC)C)C)O '
               'NAME: otophylloside B REASON: MISSED No valid ketone with '
               'alpha-hydroxy group detected\n'
               ' * SMILES: OC1(C(O)=C(C(O)=C(C1=O)C(=O)C(C)C)CC=C(C)C)CC=C(C)C '
               'NAME: Cohumulone REASON: MISSED No valid ketone with '
               'alpha-hydroxy group detected\n'
               ' * SMILES: '
               'CC(=O)[C@@]1(O)CC[C@H]2[C@@H]3CC=C4C[C@@H](O)CC[C@]4(C)[C@H]3CC[C@]12C '
               'NAME: 17alpha-hydroxypregnenolone REASON: MISSED No valid '
               'ketone with alpha-hydroxy group detected\n'
               ' * SMILES: '
               '[H][C@@]12C[C@@H](O)[C@](O)(C(=O)CO)[C@@]1(C)C[C@H](O)[C@@]1([H])[C@@]2([H])CCC2=CC(=O)C=C[C@]12C '
               'NAME: 16alpha-hydroxyprednisolone REASON: MISSED No valid '
               'ketone with alpha-hydroxy group detected\n'
               ' * SMILES: '
               'CC(C)CCC[C@@H](C)CCC[C@@H](C)CCC\\C(C)=C\\CC1(O)C(C)C(=O)c2ccccc2C1=O '
               'NAME: '
               '3-hydroxy-2-methyl-3-phytyl-2,3-dihydro-1,4-naphthoquinone '
               'REASON: MISSED No valid ketone with alpha-hydroxy group '
               'detected\n'
               ' * SMILES: '
               '[H][C@@]12CCC3=CC(=O)CC[C@]3(C)[C@@]1([H])[C@@H](O)C[C@@]1(C)[C@@]2([H])CC[C@]1(O)C(=O)COP(O)(O)=O '
               'NAME: cortisol phosphate REASON: MISSED No valid ketone with '
               'alpha-hydroxy group detected\n'
               ' * SMILES: O=C(C(O)[C@H]1[C@H](C=C[C@@H]([C@H]1O)O)/C=C/C)C '
               'NAME: Arthropsatriol B REASON: MISSED No valid ketone with '
               'alpha-hydroxy group detected\n'
               ' * SMILES: '
               'COc1cc(C)c(O)c(C\\C=C(/C)CC(=O)\\C=C(\\C)CCCC(C)C(=O)C(O)C=C(C)C)c1 '
               'NAME: '
               '(2E,6Z)-13-hydroxy-1-(2-hydroxy-5-methoxy-3-methylphenyl)-3,7,11,15-tetramethylhexadeca-2,6,14-triene-5,12-dione '
               'REASON: MISSED No valid ketone with alpha-hydroxy group '
               'detected\n'
               ' * SMILES: '
               'CC(C)[C@@H]1OC2=C(C[C@H](NC(=O)\\C(NC(=O)[C@H]1NC(=O)[C@@H](NC(=O)[C@H](CC(C)C(Cl)Cl)NC(=O)C(O)O)[C@H](O)CCCN)=C/Cl)C(O)=O)C(=O)C(O)C2 '
               'NAME: victorin C REASON: MISSED No valid ketone with '
               'alpha-hydroxy group detected\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'O=CC1=CC2=C(O[C@H](C2)C(O)(C)C)C=C1',
                                     'name': 'Asperterreusine C',
                                     'reason': 'No ketone with alpha-hydroxy '
                                               'group detected'},
                                 {   'smiles': 'CC1(C)[C@@H]2C[C@@H](OC(=O)c3ccccc3)[C@]3(C)[C@H](CC[C@@]4(C)[C@@H](OC(=O)[C@H]5O[C@@]345)c3ccoc3)[C@@]2(C)C=CC1=O',
                                     'name': '7-deacetyl-7-benzoylgedunin',
                                     'reason': 'No ketone with alpha-hydroxy '
                                               'group detected'},
                                 {   'smiles': 'P(OC[C@H](OC(=O)CCC/C=C\\C/C=C\\C/C=C\\C=C\\C(=O)CCCCC)COC(=O)CCCCCCCCC(C)C)(OC[C@@H](O)COP(O)(O)=O)(O)=O',
                                     'name': 'PGP(i-12:0/20:4(5Z,8Z,11Z,13E)+=O(15))',
                                     'reason': 'No ketone with alpha-hydroxy '
                                               'group detected'},
                                 {   'smiles': 'C[C@@H]1CN([C@H](COC2=C(C=CC(=C2)NC(=O)NC(C)C)C(=O)N(C[C@@H]1OC)C)C)C(=O)COC',
                                     'name': '1-[(5R,6R,9S)-5-methoxy-8-(2-methoxy-1-oxoethyl)-3,6,9-trimethyl-2-oxo-11-oxa-3,8-diazabicyclo[10.4.0]hexadeca-1(12),13,15-trien-14-yl]-3-propan-2-ylurea',
                                     'reason': 'No ketone with alpha-hydroxy '
                                               'group detected'},
                                 {   'smiles': 'C1CCN(CC1)C2=C(C(=CC(=N2)C3=CC=CS3)C(F)(F)F)C#N',
                                     'name': '2-(1-piperidinyl)-6-thiophen-2-yl-4-(trifluoromethyl)-3-pyridinecarbonitrile',
                                     'reason': 'No ketone with alpha-hydroxy '
                                               'group detected'},
                                 {   'smiles': '[H][C@@]1(NC(=O)Cc2cccs2)C(=O)N2C(C(O)=O)=C(COC(C)=O)CS[C@]12[H]',
                                     'name': 'cefalotin',
                                     'reason': 'No ketone with alpha-hydroxy '
                                               'group detected'},
                                 {   'smiles': 'O1C2=C(C/C=C(\\CCC=C(C)C)/C)C(O)=CC(O)=C2C(=O)C3=C1C(O)=CC=C3',
                                     'name': '(E)-4-(3,7-Dimethyl-2,6-octadienyl)-1,3,5-trihydroxyxanthone',
                                     'reason': 'No ketone with alpha-hydroxy '
                                               'group detected'},
                                 {   'smiles': 'P(OC[C@H]1O[C@@H](N2C=CC(=NC2=O)N)C(O)[C@H]1O)(OP(OC[C@H](OC(=O)CCCCCCC/C=C\\C/C=C\\CCCCC)COC(=O)CCCCCCC/C=C\\C/C=C\\C/C=C\\CC)(O)=O)(O)=O',
                                     'name': 'CDP-DG(18:3(9Z,12Z,15Z)/18:2(9Z,12Z))',
                                     'reason': 'No ketone with alpha-hydroxy '
                                               'group detected'},
                                 {   'smiles': 'O1C2=C(C=C(CO)C=C2)C[C@H]1[C@](O)(CO)C',
                                     'name': 'Conielldihydrobenzofuran',
                                     'reason': 'No ketone with alpha-hydroxy '
                                               'group detected'},
                                 {   'smiles': 'O([C@@H]1O[C@@H]([C@@H](O[C@@H]2O[C@H]([C@@H](O)[C@@H](O)[C@@H]2O)C)[C@@H](O[C@@H]3O[C@@H]([C@H](O)[C@H](O)[C@H]3O)CO)[C@H]1NC(=O)C)CO)[C@@H]4[C@@H](O)[C@H](O[C@H]5[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]5CO)O[C@H]6[C@@H](O)[C@H](O[C@@H](O[C@@H]([C@H](O)[C@@H](O)CO)[C@H](O)CO)[C@@H]6O)CO)O[C@@H]([C@@H]4O)CO',
                                     'name': 'N-[(2S,3R,4R,5S,6R)-5-[(2S,3R,4S,5S,6R)-4-[(2S,3R,4R,5S,6R)-3-Acetamido-6-(hydroxymethyl)-4-[(2R,3R,4S,5R,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-5-[(2S,3S,4R,5S,6S)-3,4,5-trihydroxy-6-methyloxan-2-yl]oxyoxan-2-yl]oxy-3,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-2-[(2R,3S,4S,5R,6S)-3,5-dihydroxy-2-(hydroxymethyl)-6-[(2R,3R,4R,5S)-1,2,4,5,6-pentahydroxyhexan-3-yl]oxyoxan-4-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-3-yl]acetamide',
                                     'reason': 'No ketone with alpha-hydroxy '
                                               'group detected'}],
    'sample_false_negatives': [   {   'smiles': 'C=12N=C(N=CC1C3=C(N2[C@@H]4CC[C@H](CC4)C)C=NC=C3)NC=5C=CC6=C(N5)CCN(C6)C(CO)=O',
                                      'name': 'AMG-925',
                                      'reason': 'No valid ketone with '
                                                'alpha-hydroxy group detected'},
                                  {   'smiles': 'C1[C@](C(=O)N1)(CC[C@@H](C(=O)O)N)O',
                                      'name': 'tabtoxinine beta-lactam',
                                      'reason': 'No valid ketone with '
                                                'alpha-hydroxy group detected'},
                                  {   'smiles': 'OC1=CC=CC=CC1=O',
                                      'name': 'tropolone',
                                      'reason': 'No ketone with alpha-hydroxy '
                                                'group detected'},
                                  {   'smiles': 'OC1=CC=CC(O)=C(O)C1=O',
                                      'name': '3,7-dihydroxytropolone',
                                      'reason': 'No ketone with alpha-hydroxy '
                                                'group detected'}],
    'attempt': 2,
    'reasoning': '',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 403,
    'num_false_positives': 2837,
    'num_true_negatives': 139056,
    'num_false_negatives': 4,
    'num_negatives': None,
    'precision': 0.12438271604938271,
    'recall': 0.9901719901719902,
    'f1': 0.22100356457362214,
    'accuracy': 0.9800351370344343,
    'negative_predictive_value': 0.9999712354379404}