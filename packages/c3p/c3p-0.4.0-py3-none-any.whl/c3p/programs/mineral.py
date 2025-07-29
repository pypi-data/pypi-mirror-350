"""
Classifies: CHEBI:46662 mineral
"""
"""
Classifies: Mineral
"""
from rdkit import Chem
from rdkit.Chem import rdMolDescriptors, Descriptors

def is_mineral(smiles: str):
    """
    Determines if a molecule is a mineral based on its SMILES string.

    Minerals are typically inorganic compounds consisting of metal cations
    and inorganic anions, and are naturally occurring. This function uses
    heuristics to classify minerals based on the absence of organic carbon
    structures and the presence of metal elements.

    Args:
        smiles (str): SMILES string of the molecule.

    Returns:
        bool: True if molecule is likely a mineral, False otherwise.
        str: Reason for classification.
    """
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # List of metal elements (atomic numbers)
    metals = {3,4,11,12,13,19,20,21,22,23,24,25,26,27,28,29,30,31,37,38,39,
              40,41,42,43,44,45,46,47,48,49,55,56,57,72,73,74,75,76,77,78,
              79,80,81,82,83,84,87,88,89,104,105,106,107,108,109,110,111,112}

    # Check for presence of metal elements
    has_metal = any(atom.GetAtomicNum() in metals for atom in mol.GetAtoms())
    if not has_metal:
        return False, "No metal elements detected"

    # Check for absence of organic carbon
    for atom in mol.GetAtoms():
        if atom.GetAtomicNum() == 6:  # Carbon atom
            # If carbon is bonded to hydrogen or carbon, it's likely organic
            neighbors = [nbr.GetAtomicNum() for nbr in atom.GetNeighbors()]
            if 1 in neighbors or 6 in neighbors:
                return False, "Contains organic carbon structures"

    # Check for absence of complex organic functional groups
    organic_functional_groups = ['[CX3]=[OX1]', '[#6]#[#7]', '[#6]=[#7]']
    for fg in organic_functional_groups:
        fg_pattern = Chem.MolFromSmarts(fg)
        if mol.HasSubstructMatch(fg_pattern):
            return False, "Contains organic functional groups"

    # Check for presence of common inorganic anions
    inorganic_anions = ['[O-]S(=O)(=O)[O-]',  # Sulfate
                        'P(=O)([O-])([O-])[O-]',  # Phosphate
                        '[C-]#N',  # Cyanide (to exclude)
                        'C(=O)([O-])[O-]',  # Carbonate
                        '[O-][N+](=O)[O-]',  # Nitrate
                        '[F-]', '[Cl-]', '[Br-]', '[I-]',  # Halides
                        '[O-]',  # Oxide
                        '[S-2]',  # Sulfide
                        '[OH-]',  # Hydroxide
                        '[O-]C(=O)[O-]'  # Oxalate (to exclude)
                        ]
    has_inorganic_anion = False
    for anion in inorganic_anions:
        anion_pattern = Chem.MolFromSmarts(anion)
        if mol.HasSubstructMatch(anion_pattern):
            has_inorganic_anion = True
            break
    if not has_inorganic_anion:
        return False, "No common inorganic anions detected"

    return True, "Likely a mineral (inorganic compound with metal elements and inorganic anions)"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:46662',
                          'name': 'mineral',
                          'definition': 'In general, a mineral is a chemical '
                                        'substance that is normally '
                                        'crystalline formed and has been '
                                        'formed as a result of geological '
                                        'processes. The term also includes '
                                        'metamict substances (naturally '
                                        'occurring, formerly crystalline '
                                        'substances whose crystallinity has '
                                        'been destroyed by ionising radiation) '
                                        'and can include naturally occurring '
                                        'amorphous substances that have never '
                                        "been crystalline ('mineraloids') such "
                                        'as georgite and calciouranoite as '
                                        'well as substances formed by the '
                                        'action of geological processes on '
                                        "bigenic compounds ('biogenic "
                                        "minerals').",
                          'parents': ['CHEBI:59999'],
                          'xrefs': ['Wikipedia:Mineral'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 58,
                           'log_lines_of_code': 4.060443010546419,
                           'indent_by_line': [   1,
                                                 1,
                                                 0,
                                                 1,
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
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 0,
                                                 1,
                                                 1,
                                                 2,
                                                 3,
                                                 3,
                                                 3,
                                                 4,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 3,
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
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 3,
                                                 3,
                                                 1,
                                                 2,
                                                 0,
                                                 1],
                           'max_indent': 4,
                           'imports': [   'from rdkit import Chem',
                                          'from rdkit.Chem import '
                                          'rdMolDescriptors, Descriptors'],
                           'imports_count': 2,
                           'methods_called': [   'MolFromSmiles',
                                                 'HasSubstructMatch',
                                                 'GetAtoms',
                                                 'GetAtomicNum',
                                                 'GetNeighbors',
                                                 'MolFromSmarts'],
                           'methods_called_count': 6,
                           'smarts_strings': ['anion', 'fg'],
                           'smarts_strings_count': 2,
                           'defs': ['is_mineral(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "No metal elements detected"',
                                          'False, "Contains organic carbon '
                                          'structures"',
                                          'False, "Contains organic functional '
                                          'groups"',
                                          'False, "No common inorganic anions '
                                          'detected"',
                                          'True, "Likely a mineral (inorganic '
                                          'compound with metal elements and '
                                          'inorganic anions)"'],
                           'returns_count': 6,
                           'complexity': 4.212088602109284},
    'message': '\n'
               'Attempt failed: F1 score of 0 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: NONE\n'
               'False positives: NONE\n'
               'False negatives: SMILES: [Ca+2].C(=O)([O-])[O-] NAME: calcium '
               'carbonate REASON: MISSED None\n'
               ' * SMILES: [Ba++].[O-][N+]([O-])=O.[O-][N+]([O-])=O NAME: '
               'barium nitrate REASON: MISSED None\n'
               ' * SMILES: '
               '[Ca++].[Ca++].[Ca++].[O-]P([O-])([O-])=O.[O-]P([O-])([O-])=O '
               'NAME: tricalcium bis(phosphate) REASON: MISSED None\n'
               ' * SMILES: P(=O)([O-])([O-])[O-].[Mg+2].[NH4+].O.O.O.O.O.O '
               'NAME: ammonium magnesium phosphate hexahydrate REASON: MISSED '
               'None\n'
               ' * SMILES: Cl[O-].[Ca+2].Cl[O-] NAME: Calcium hypochlorite '
               'REASON: MISSED None\n'
               ' * SMILES: '
               '[Na+].[Na+].[H]OB1O[B-]2(O[H])OB(O[H])O[B-](O[H])(O1)O2 NAME: '
               'disodium tetraborate REASON: MISSED None\n'
               ' * SMILES: [Fe++].[S-][S-] NAME: pyrite REASON: MISSED None\n'
               ' * SMILES: [Mg++].CCC([O-])=O.CCC([O-])=O NAME: magnesium '
               'dipropionate REASON: MISSED None\n'
               ' * SMILES: [Cl-].[Cs+] NAME: caesium chloride REASON: MISSED '
               'None\n'
               ' * SMILES: '
               '[OH-].[OH-].[OH-].[OH-].O=[Si]([O-])O[Si](=O)[O-].[Al+3].[Al+3] '
               'NAME: kaolinite REASON: MISSED None\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'CCOC(=O)CC(C1=CC=CC=C1Cl)NC2=NC(=NC(=N2)N3CCOCC3)N4CCOCC4',
                                     'name': '3-[[4,6-bis(4-morpholinyl)-1,3,5-triazin-2-yl]amino]-3-(2-chlorophenyl)propanoic '
                                             'acid ethyl ester',
                                     'reason': 'No metal elements detected'},
                                 {   'smiles': 'O([C@@H]1[C@@H](O)[C@H](O)[C@H](O[C@]1(C=2C=3OC(=CC(=O)C3C(O)=CC2O)C4=CC(O)=C(O)C=C4)[H])CO)[C@@H]5O[C@H]([C@@H](O)[C@@H](O)[C@@H]5O)CO',
                                     'name': "2''-O-beta-L-Galactopyranosylorientin",
                                     'reason': 'No metal elements detected'},
                                 {   'smiles': 'C[C@@H]1O[C@@H](O[C@@H]2[C@@H](NC(C)=O)[C@@H](O[C@H](CO)[C@H]2O[C@@H]2O[C@H](CO)[C@H](O)[C@H](O)[C@H]2NC(C)=O)O[C@@H]2[C@@H](O)[C@@H](O)O[C@H](CO)[C@@H]2O)[C@@H](O)[C@H](O)[C@@H]1O',
                                     'name': 'beta-D-GalpNAc-(1->4)-[alpha-L-Fucp-(1->3)]-beta-D-GlcpNAc-(1->3)-alpha-D-Galp',
                                     'reason': 'No metal elements detected'},
                                 {   'smiles': 'C[C@H]1CN(C(=O)CC2=C(C=CC(=C2)NC(=O)CCC(F)(F)F)O[C@H]1CN(C)CC3=CC4=C(C=C3)OCO4)[C@@H](C)CO',
                                     'name': 'N-[(2R,3S)-2-[[1,3-benzodioxol-5-ylmethyl(methyl)amino]methyl]-5-[(2S)-1-hydroxypropan-2-yl]-3-methyl-6-oxo-2,3,4,7-tetrahydro-1,5-benzoxazonin-9-yl]-4,4,4-trifluorobutanamide',
                                     'reason': 'No metal elements detected'},
                                 {   'smiles': 'C1CC(C1)C(=O)N[C@@H]2C=C[C@H](O[C@H]2CO)CC(=O)NCCCN3CCOCC3',
                                     'name': 'N-[(2R,3R,6R)-2-(hydroxymethyl)-6-[2-[3-(4-morpholinyl)propylamino]-2-oxoethyl]-3,6-dihydro-2H-pyran-3-yl]cyclobutanecarboxamide',
                                     'reason': 'No metal elements detected'},
                                 {   'smiles': 'O=C1O[C@@H](CC[C@H](O)C=C[C@H](C1)O)C',
                                     'name': 'Decarestrictine C1',
                                     'reason': 'No metal elements detected'},
                                 {   'smiles': '[H]P(O)(=O)OP([H])(O)=O',
                                     'name': 'diphosphonic acid',
                                     'reason': 'No metal elements detected'},
                                 {   'smiles': 'C[C@H]1CN(C(=O)CCCN2C(=CN=N2)CO[C@@H]1CN(C)C(=O)C3=NOC(=C3)C4=CC=CC=C4)[C@H](C)CO',
                                     'name': 'N-[[(8S,9S)-6-[(2R)-1-hydroxypropan-2-yl]-8-methyl-5-oxo-10-oxa-1,6,14,15-tetrazabicyclo[10.3.0]pentadeca-12,14-dien-9-yl]methyl]-N-methyl-5-phenyl-3-isoxazolecarboxamide',
                                     'reason': 'No metal elements detected'},
                                 {   'smiles': 'OCCCCCCC[C@@H](O)CC(O)=O',
                                     'name': '(3R)-3,10-dihydroxydecanoic acid',
                                     'reason': 'No metal elements detected'},
                                 {   'smiles': 'S(=O)(=O)(CC[C@@H]1NC(=O)[C@H](NC(=O)C(N(C(=O)CC[C@@H](NC([C@H]([C@@H](NC([C@@H](NC(C[C@@H](NC1=O)C(=O)O)=O)CCCN=C(N)N)=O)/C=C/C(=C/[C@@H]([C@@H](OC)CC2=CC=CC=C2)C)/C)C)=O)C(=O)O)C)=C)C)C',
                                     'name': '[D-Asp3]MC-M(O2)R',
                                     'reason': 'No metal elements detected'}],
    'sample_false_negatives': [   {   'smiles': '[Ca+2].C(=O)([O-])[O-]',
                                      'name': 'calcium carbonate',
                                      'reason': 'Contains organic functional '
                                                'groups'},
                                  {   'smiles': '[Na+].[Na+].[H]OB1O[B-]2(O[H])OB(O[H])O[B-](O[H])(O1)O2',
                                      'name': 'disodium tetraborate',
                                      'reason': 'No common inorganic anions '
                                                'detected'},
                                  {   'smiles': '[Fe++].[S-][S-]',
                                      'name': 'pyrite',
                                      'reason': 'No common inorganic anions '
                                                'detected'},
                                  {   'smiles': '[Mg++].CCC([O-])=O.CCC([O-])=O',
                                      'name': 'magnesium dipropionate',
                                      'reason': 'Contains organic carbon '
                                                'structures'},
                                  {   'smiles': 'O.O.Cl[Cu]Cl',
                                      'name': 'copper(II) chloride dihydrate',
                                      'reason': 'No common inorganic anions '
                                                'detected'},
                                  {   'smiles': '[Ni]=S=[Ni]=S=[Ni]',
                                      'name': 'heazlewoodite',
                                      'reason': 'No common inorganic anions '
                                                'detected'},
                                  {   'smiles': '[Na+].[Na+].[H]O[H].[H]O[H].[H]O[H].[H]O[H].[H]O[H].[H]O[H].[H]O[H].[H]O[H].[H]OB1O[B-]2(O[H])OB(O[H])O[B-](O[H])(O1)O2',
                                      'name': 'disodium tetraborate '
                                              'octahydrate',
                                      'reason': 'No common inorganic anions '
                                                'detected'},
                                  {   'smiles': 'O1B(O[B-]2(OB(O[B-]1(O[H])O2)O[H])O[H])O[H].[Na+].[Na+].O.O.O.O.O.O.O.O.O.O',
                                      'name': 'disodium tetraborate '
                                              'decahydrate',
                                      'reason': 'No common inorganic anions '
                                                'detected'},
                                  {   'smiles': 'Cl[Cu]Cl.O.O.O.O.O',
                                      'name': 'copper(II) chloride '
                                              'pentahydrate',
                                      'reason': 'No common inorganic anions '
                                                'detected'},
                                  {   'smiles': 'Cl[La](Cl)Cl',
                                      'name': 'lanthanum trichloride',
                                      'reason': 'No common inorganic anions '
                                                'detected'}],
    'attempt': 2,
    'reasoning': 'After analyzing the previous program, it appears that the '
                 'function `is_mineral` did not attempt any classification and '
                 'returned `(None, None)` for all inputs. This led to all true '
                 'positive cases being missed, resulting in a zero F1 score. '
                 'To improve, we can implement a heuristic approach to '
                 'classify minerals based on their SMILES strings.\n'
                 '\n'
                 'Minerals are typically inorganic compounds that are '
                 'naturally occurring and often consist of metal cations '
                 'combined with inorganic anions (like sulfates, phosphates, '
                 'carbonates, etc.). They usually lack organic carbon-hydrogen '
                 'bonds. We can use these characteristics to create a function '
                 'that checks for:\n'
                 '\n'
                 '- Presence of metal elements.\n'
                 '- Absence of organic carbon structures.\n'
                 '- Presence of inorganic anions commonly found in minerals.\n'
                 '\n'
                 'Here is the improved code:',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 28,
    'num_false_positives': 192,
    'num_true_negatives': 142062,
    'num_false_negatives': 18,
    'num_negatives': None,
    'precision': 0.12727272727272726,
    'recall': 0.6086956521739131,
    'f1': 0.21052631578947367,
    'accuracy': 0.9985242445537597,
    'negative_predictive_value': 0.9998733108108108}