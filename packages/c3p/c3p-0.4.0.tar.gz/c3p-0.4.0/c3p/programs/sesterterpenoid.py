"""
Classifies: CHEBI:26660 sesterterpenoid
"""
from rdkit import Chem
from rdkit.Chem import rdMolDescriptors

def is_sesterterpenoid(smiles: str):
    """
    Determines if a molecule is a sesterterpenoid based on its SMILES string.
    A sesterterpenoid is derived from a sesterterpene, showcasing a modified C25 backbone, 
    rearranged or involving additional ring structures and diverse functional groups.

    Args:
        smiles (str): SMILES string of the molecule.

    Returns:
        bool: True if the molecule is a sesterterpenoid, False otherwise.
        str: Reason for classification.
    """
    
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string."
    
    # Count carbon atoms
    c_count = sum(1 for atom in mol.GetAtoms() if atom.GetAtomicNum() == 6)

    # Widely allow for structural variability in sesterterpenoids
    if c_count < 20 or c_count > 40:
        return False, f"Carbon count of {c_count} is outside the expanded range typical for sesterterpenoids."

    # Check for rings; sesterterpenoids frequently have multiple rings
    ring_count = mol.GetRingInfo().NumRings()
    if ring_count < 1:
        return False, "Contains less than 1 ring, uncommon for sesterterpenoids."

    # Check for modified isoprene-like structures or large frameworks
    isoprene_pattern = Chem.MolFromSmarts("C=C(C)C")
    modified_structure_count = len(mol.GetSubstructMatches(isoprene_pattern))

    if modified_structure_count < 2:
        return False, "Lacks enough recognized isoprene-like structural units for sesterterpenoids."

    # Check cyclic motifs separately
    cyclohexane_pattern = Chem.MolFromSmarts("C1CCCCC1")
    cyclopentane_pattern = Chem.MolFromSmarts("C1CCCC1")

    if len(mol.GetSubstructMatches(cyclohexane_pattern)) < 1 and len(mol.GetSubstructMatches(cyclopentane_pattern)) < 1:
        return False, "Missing key cyclic motifs common in terpenoids."

    # Functional group diversity; check for common sesterterpenoid traits
    oxygen_pattern = Chem.MolFromSmarts("[OX2H]")
    oxygen_matches = len(mol.GetSubstructMatches(oxygen_pattern))
    
    if oxygen_matches == 0:
        return False, "No hydroxyl groups which are often present in sesterterpenoid moieties."

    # If all checks are satisfied, classify as sesterterpenoid
    return True, "Molecule exhibits a modified terpenoid backbone with requisite structural diversity typical of a sesterterpenoid."


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:26660',
                          'name': 'sesterterpenoid',
                          'definition': 'Any terpenoid derived from a '
                                        'sesterterpene. The term includes '
                                        'compounds in which the C25 skeleton '
                                        'of the parent sesterterpene has been '
                                        'rearranged or modified by the removal '
                                        'of one or more skeletal atoms '
                                        '(generally methyl groups). Sometimes '
                                        'sesterterpenoids are erroneously '
                                        'referred to as sesterpenoids.',
                          'parents': ['CHEBI:26873'],
                          'xrefs': ['LIPID_MAPS_class:LMPR0105'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 40,
                           'log_lines_of_code': 3.6888794541139363,
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
                                                 1,
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 0,
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
                                                 1,
                                                 0,
                                                 1,
                                                 2,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 0,
                                                 1,
                                                 2,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 0,
                                                 1,
                                                 1],
                           'max_indent': 2,
                           'imports': [   'from rdkit import Chem',
                                          'from rdkit.Chem import '
                                          'rdMolDescriptors'],
                           'imports_count': 2,
                           'methods_called': [   'MolFromSmiles',
                                                 'GetAtomicNum',
                                                 'GetSubstructMatches',
                                                 'NumRings',
                                                 'MolFromSmarts',
                                                 'GetAtoms',
                                                 'GetRingInfo'],
                           'methods_called_count': 7,
                           'smarts_strings': [   '[OX2H]',
                                                 'C1CCCCC1',
                                                 'C=C(C)C',
                                                 'C1CCCC1'],
                           'smarts_strings_count': 4,
                           'defs': ['is_sesterterpenoid(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string."',
                                          'False, f"Carbon count of {c_count} '
                                          'is outside the expanded range '
                                          'typical for sesterterpenoids."',
                                          'False, "Contains less than 1 ring, '
                                          'uncommon for sesterterpenoids."',
                                          'False, "Lacks enough recognized '
                                          'isoprene-like structural units for '
                                          'sesterterpenoids."',
                                          'False, "Missing key cyclic motifs '
                                          'common in terpenoids."',
                                          'False, "No hydroxyl groups which '
                                          'are often present in '
                                          'sesterterpenoid moieties."',
                                          'True, "Molecule exhibits a modified '
                                          'terpenoid backbone with requisite '
                                          'structural diversity typical of a '
                                          'sesterterpenoid."'],
                           'returns_count': 7,
                           'complexity': 4.1377758908227875},
    'message': '\n'
               'Error: Error executing '
               "is_sesterterpenoid('CC(\\\\C=C\\\\C=C(C)\\\\C=C\\\\[C@@]1(O)C(C)(C)CCC[C@@]1(C)O)=C/C=C/C=C(C)/C=C/C(O)=O'):\n"
               ' Python argument types in\n'
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
    'sample_true_negatives': [   {   'smiles': 'O1[C@H]([C@@H](O)CC=2C1=CC=CC2)C3=CC=CC=C3',
                                     'name': 'cis-(+)-3-Flavanol',
                                     'reason': 'Carbon count of 15 is outside '
                                               'the expanded range typical for '
                                               'sesterterpenoids.'},
                                 {   'smiles': 'O1C2C34C(C(N(CC3)C)CC5=C4C1=C(OC)C=C5)C=CC2OC',
                                     'name': '6-O-Methylcodeine',
                                     'reason': 'Carbon count of 19 is outside '
                                               'the expanded range typical for '
                                               'sesterterpenoids.'},
                                 {   'smiles': 'CN1C2=C(C=CC(=C2)OC)C3=C1[C@H](N(CC34CCN(CC4)S(=O)(=O)C5=CC=CS5)CC6CC6)CO',
                                     'name': "[(1S)-2-(cyclopropylmethyl)-7-methoxy-9-methyl-1'-thiophen-2-ylsulfonyl-1-spiro[1,3-dihydropyrido[3,4-b]indole-4,4'-piperidine]yl]methanol",
                                     'reason': 'Lacks enough recognized '
                                               'isoprene-like structural units '
                                               'for sesterterpenoids.'},
                                 {   'smiles': 'O(C(=O)CCCCCCCCCCCCCCC)[C@@H](COC(=O)CCCCCCCCCCCCCCCCCCC)COC(=O)CCCCCCC',
                                     'name': 'TG(20:0/16:0/8:0)',
                                     'reason': 'Carbon count of 47 is outside '
                                               'the expanded range typical for '
                                               'sesterterpenoids.'},
                                 {   'smiles': 'C1=CC=C(C=C1)N2C(=NN=C2SCC#N)COC3=CC=CC=C3',
                                     'name': '2-[[5-(phenoxymethyl)-4-phenyl-1,2,4-triazol-3-yl]thio]acetonitrile',
                                     'reason': 'Carbon count of 17 is outside '
                                               'the expanded range typical for '
                                               'sesterterpenoids.'},
                                 {   'smiles': 'O=C1C=2OC([C@H]3C[C@H](O)C(=C[C@H]3C2C(=O)C=4C1=C(O)C(=C(O)C4)C)C)(C)C',
                                     'name': 'Unnamed naphterpin 1',
                                     'reason': 'Missing key cyclic motifs '
                                               'common in terpenoids.'},
                                 {   'smiles': 'O([C@@H]1[C@]2(C([C@@](C1)(CC2)[H])(C)C)C)C(=O)/C=C/C3=CC=C(O)C=C3',
                                     'name': '(1R,4R)-1,7,7-Trimethylbicyclo[2.2.1]heptane-2beta-ol '
                                             '3-(4-hydroxyphenyl)acrylate',
                                     'reason': 'Carbon count of 19 is outside '
                                               'the expanded range typical for '
                                               'sesterterpenoids.'},
                                 {   'smiles': 'CC1(C)CC[C@@]2(CC[C@]3(C)C(=CC[C@@H]4[C@@]5(C)CC[C@H](O)C(C)(C)[C@@H]5CC[C@@]34C)[C@@H]2C1)C([O-])=O',
                                     'name': 'oleanolate',
                                     'reason': 'Lacks enough recognized '
                                               'isoprene-like structural units '
                                               'for sesterterpenoids.'},
                                 {   'smiles': 'C[C@@H]1CN(C(=O)C2=C(N=CC(=C2)C3=CCCCC3)O[C@@H]1CN(C)CC4=CC=C(C=C4)C(=O)O)[C@H](C)CO',
                                     'name': '4-[[[(2S,3R)-8-(1-cyclohexenyl)-5-[(2R)-1-hydroxypropan-2-yl]-3-methyl-6-oxo-3,4-dihydro-2H-pyrido[2,3-b][1,5]oxazocin-2-yl]methyl-methylamino]methyl]benzoic '
                                             'acid',
                                     'reason': 'Lacks enough recognized '
                                               'isoprene-like structural units '
                                               'for sesterterpenoids.'},
                                 {   'smiles': 'CC(C)(O)[C@H]1CC[C@@]2(C)[C@H]1CC[C@]1(CO)[C@@H]2C[C@@H](O)[C@@H]2[C@@]3(C)CCCC(C)(C)[C@@H]3[C@H](O)C[C@@]12C',
                                     'name': 'hopane-6beta,11alpha,22,27-tetraol',
                                     'reason': 'Lacks enough recognized '
                                               'isoprene-like structural units '
                                               'for sesterterpenoids.'}],
    'sample_false_negatives': [   {   'smiles': 'O([C@H]([C@H](C[C@H](C[C@H](CC)C)C)C)[C@H](/C=C(/[C@@H](O)[C@H](/C=C(/[C@@H](O)[C@H](/C=C(/[C@@H](O)[C@@H](C)C(O)=O)\\C)C)\\C)C)\\C)C)[C@@H]1O[C@@H]([C@@H](O)[C@H](O)[C@@H]1O)CO',
                                      'name': 'Bionectriol D',
                                      'reason': 'Missing key cyclic motifs '
                                                'common in terpenoids.'},
                                  {   'smiles': 'O=C1C=2C(=CC[C@H]3[C@@H]([C@H](/C=C\\C=C(C)C)C)CC[C@@]3(CC2[C@@H](C1)C)C)C=O',
                                      'name': '21-dehydroophiobolin U',
                                      'reason': 'No hydroxyl groups which are '
                                                'often present in '
                                                'sesterterpenoid moieties.'},
                                  {   'smiles': 'O=C1C(=C(C[C@H]([C@]2(C(=O)[C@@]3(C(=O)OC)[C@@]4([C@H]([C@@]5(C=O)[C@@H](C([C@@H](OC(=O)C)CC5)(C)C)CC4)C=C([C@]3(C2=O)C)C)C)C)C)O[C@@]1(/C=C/C=C/CC)C)C(=O)OC',
                                      'name': 'Isopenicin A',
                                      'reason': 'Carbon count of 44 is outside '
                                                'the expanded range typical '
                                                'for sesterterpenoids.'},
                                  {   'smiles': 'O=C1OC23C(C=C(C(OC4OC(C(NC(=O)C)C(C4)(O)C)C)C(C)C=C(C5C(C(=C1C2=O)O)(C6C(C(OC7OC(C(OC8OC(C(OC9OC(C(O)C(C9)O)C)C(C8)OC%10OC(C(O)CC%10)C)C)CC7)C)C(C)CC6C)C=C5)C)C)C)C=CC(C3)CC',
                                      'name': 'Saccharosacrin D',
                                      'reason': 'Carbon count of 67 is outside '
                                                'the expanded range typical '
                                                'for sesterterpenoids.'},
                                  {   'smiles': 'O=C(O)[C@@H]([C@@]1(O[C@@]([C@@H](CC)[C@H]([C@@H]1C)O)([C@@H]([C@@H](O)[C@H](C(=O)[C@H]([C@H]2O[C@@]([C@@]3(O[C@]([C@@H](O)CCC)(CC)C[C@H]3C)O)(C)C[C@@H]2C)CC)C)C)C)O)CC',
                                      'name': 'Inostamycin',
                                      'reason': 'Lacks enough recognized '
                                                'isoprene-like structural '
                                                'units for sesterterpenoids.'},
                                  {   'smiles': 'O=[N+]([O-])[C@@]1([C@@H](NOC(=O)C)[C@H](O[C@H](C1)O[C@@H]2C(=C[C@@H]3C=C(C=O)[C@H](C)C[C@]34OC(=O)C(C4=O)=C([C@@]5([C@H](C(=CC2)C)C=C[C@@H]6[C@@H](O[C@@H]7O[C@H]([C@H](O)[C@@H](C7)O[C@@H]8O[C@H]([C@H](O[C@H]9O[C@H]([C@H](OC)[C@@H](C9)O)C)[C@@H](C8)O)C)C)[C@@H](C)C[C@@H]([C@@H]56)C)C)O)C)C)C',
                                      'name': 'Lobophorin H',
                                      'reason': 'Carbon count of 61 is outside '
                                                'the expanded range typical '
                                                'for sesterterpenoids.'},
                                  {   'smiles': '[H][C@@]12CC[C@@]3(C)C4=CC[C@@]5(C)CCC(C)(C)C[C@@]5([H])[C@]4(C)CC[C@]3([H])[C@@]1(C)CCC(=O)C2(C)C',
                                      'name': 'taraxerone',
                                      'reason': 'Lacks enough recognized '
                                                'isoprene-like structural '
                                                'units for sesterterpenoids.'},
                                  {   'smiles': 'O=C1C=C(C)[C@@H]2[C@H]1C(=CC[C@H]3/C(=C(/C=C/C=C(C)C)\\C)/CC[C@@]3(C2)C)C=O',
                                      'name': '14,15-dehydro-6-epi-ophiobolin '
                                              'G',
                                      'reason': 'No hydroxyl groups which are '
                                                'often present in '
                                                'sesterterpenoid moieties.'},
                                  {   'smiles': 'O=C1[C@H]2C(=CC[C@H]3[C@@H]([C@H](C=CC(OC)C(O)(C)C)C)CC[C@@]3(C[C@@H]2[C@@](C1)(O)C)C)C=O',
                                      'name': 'Ophiobolin S',
                                      'reason': 'Lacks enough recognized '
                                                'isoprene-like structural '
                                                'units for sesterterpenoids.'},
                                  {   'smiles': 'O=C([C@@H]([C@H]1O[C@@]([C@@]23O[C@@](CC)([C@@H](O2)C)C[C@H]3C)(C)C[C@@H]1C)CC)[C@H]([C@@H](O)[C@@H]([C@H]4O[C@](O)([C@H](C)C[C@@H]4C)CC)C)C',
                                      'name': 'X-14889-D',
                                      'reason': 'Lacks enough recognized '
                                                'isoprene-like structural '
                                                'units for sesterterpenoids.'}],
    'attempt': 5,
    'reasoning': 'The previous attempt to classify sesterterpenoids had a '
                 'logical structure but encountered an error due to the misuse '
                 'of the `Chem.MolFromSmarts` function. The pattern provided '
                 'for cyclic motifs as `C1CCCCC1 | C1CCCC1` is incorrect '
                 'because `Chem.MolFromSmarts` requires a single valid SMARTS '
                 'pattern at a time, and the use of the pipe character was '
                 "syntactically incorrect for SMARTS. Let's fix that and break "
                 'the problem down step-by-step:\n'
                 '\n'
                 '1. **Parse SMILES**: Convert the SMILES string into a '
                 'molecule object using RDKit.\n'
                 '\n'
                 '2. **Carbon Atom Count**: Ensure the molecule has a carbon '
                 'atom count that suggests a backbone derived from a '
                 'sesterterpene (commonly around 25 carbons, but vary from '
                 'slightly below as rearrangements can modify the count).\n'
                 '\n'
                 '3. **Ring Count**: Sesterterpenoids often feature multiple '
                 'ring structures. Verify a decent number of rings (usually >1 '
                 'due to cyclic motifs present).\n'
                 '\n'
                 '4. **Isoprene Units**: Check for isoprene units, the '
                 'building blocks of terpenes (C=C-C-C units); ensure enough '
                 'units suggest a complex backbone.\n'
                 '\n'
                 '5. **Cyclic Motifs**: Search for common cyclic structures '
                 'separately:\n'
                 '   - Cyclohexane (`C1CCCCC1`)\n'
                 '   - Cyclopentane (`C1CCCC1`)\n'
                 '\n'
                 '6. **Functional Groups**: Detect frequent functional groups '
                 'like hydroxyl groups, indicating the presence of various '
                 'alcohols or ether modifications.\n'
                 '\n'
                 'Here’s the corrected program:',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 94,
    'num_false_positives': 3165,
    'num_true_negatives': 138867,
    'num_false_negatives': 174,
    'num_negatives': None,
    'precision': 0.028843203436637006,
    'recall': 0.35074626865671643,
    'f1': 0.053303090445137515,
    'accuracy': 0.9765354884047787,
    'negative_predictive_value': 0.9987485705655167}