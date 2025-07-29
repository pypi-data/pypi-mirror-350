"""
Classifies: CHEBI:32952 amine
"""
from rdkit import Chem

def is_amine(smiles: str):
    """
    Determines if a molecule is an amine based on its SMILES string.
    An amine is a compound formally derived from ammonia by replacing one,
    two, or three hydrogen atoms by hydrocarbyl groups.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is an amine, False otherwise
        str: Reason for classification
    """
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
    
    # SMARTS patterns for primary, secondary, tertiary amines:
    primary_amine_pattern = Chem.MolFromSmarts("[NX3;H2][#6]")
    secondary_amine_pattern = Chem.MolFromSmarts("[NX3;H1]([#6])[#6]")
    tertiary_amine_pattern = Chem.MolFromSmarts("[NX3]([#6])([#6])[#6]")
    
    # Exclusion patterns
    amide_pattern = Chem.MolFromSmarts("[NX3][CX3](=O)")
    imine_pattern = Chem.MolFromSmarts("[NX2]=[CX3]")
    nitrile_pattern = Chem.MolFromSmarts("[NX1]#[CX2]")
    
    # If a nitrogen is amide, imine, or nitrile, we exclude it
    if mol.HasSubstructMatch(amide_pattern) or mol.HasSubstructMatch(imine_pattern) or mol.HasSubstructMatch(nitrile_pattern):
        return False, "Structure matches amide, imine, or nitrile, excluding it as an amine"

    # Functions to check if there is any amine pattern match
    def has_amine_structure(pattern):
        matches = mol.GetSubstructMatches(pattern)
        for match in matches:
            if not mol.GetRingInfo().IsAtomInRingOfSize(match[0], 5):
                # Check if the matched nitrogen is part of a ring
                if not mol.GetRingInfo().NumAtomRings(match[0]):
                    return True
        return False
    
    # Check if any primary, secondary, or tertiary amine structure matches
    if has_amine_structure(primary_amine_pattern) or has_amine_structure(secondary_amine_pattern) or has_amine_structure(tertiary_amine_pattern):
        return True, "Contains amine group not part of excluded structures"
    
    return False, "No amine group found, or nitrogen not bonded as required"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:32952',
                          'name': 'amine',
                          'definition': 'A compound formally derived from '
                                        'ammonia by replacing one, two or '
                                        'three hydrogen atoms by hydrocarbyl '
                                        'groups.',
                          'parents': ['CHEBI:50047'],
                          'xrefs': ['KEGG:C00706'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 38,
                           'log_lines_of_code': 3.6375861597263857,
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
                                                 0,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 3,
                                                 4,
                                                 4,
                                                 5,
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 1,
                                                 1],
                           'max_indent': 5,
                           'imports': ['from rdkit import Chem'],
                           'imports_count': 1,
                           'methods_called': [   'MolFromSmiles',
                                                 'GetSubstructMatches',
                                                 'NumAtomRings',
                                                 'IsAtomInRingOfSize',
                                                 'HasSubstructMatch',
                                                 'MolFromSmarts',
                                                 'GetRingInfo'],
                           'methods_called_count': 7,
                           'smarts_strings': [   '[NX3;H2][#6]',
                                                 '[NX3][CX3](=O)',
                                                 '[NX3;H1]([#6])[#6]',
                                                 '[NX2]=[CX3]',
                                                 '[NX3]([#6])([#6])[#6]',
                                                 '[NX1]#[CX2]'],
                           'smarts_strings_count': 6,
                           'defs': [   'is_amine(smiles: str):',
                                       'has_amine_structure(pattern):'],
                           'defs_count': 2,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "Structure matches amide, '
                                          'imine, or nitrile, excluding it as '
                                          'an amine"',
                                          'True',
                                          'False',
                                          'True, "Contains amine group not '
                                          'part of excluded structures"',
                                          'False, "No amine group found, or '
                                          'nitrogen not bonded as required"'],
                           'returns_count': 6,
                           'complexity': 4.727517231945277},
    'message': '\n'
               'Error: Error executing '
               "is_amine('O[C@@H]1[C@@H](N(C)[C@@H](C1)CCCCCC(O)C)CC2=CC=CC=C2'):\n"
               ' tuple index out of range\n'
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
                                     'reason': 'No amine group found, or '
                                               'nitrogen not bonded as '
                                               'required'},
                                 {   'smiles': 'O1C2C34C(C(N(CC3)C)CC5=C4C1=C(OC)C=C5)C=CC2OC',
                                     'name': '6-O-Methylcodeine',
                                     'reason': 'No amine group found, or '
                                               'nitrogen not bonded as '
                                               'required'},
                                 {   'smiles': 'CN1C2=C(C=CC(=C2)OC)C3=C1[C@H](N(CC34CCN(CC4)S(=O)(=O)C5=CC=CS5)CC6CC6)CO',
                                     'name': "[(1S)-2-(cyclopropylmethyl)-7-methoxy-9-methyl-1'-thiophen-2-ylsulfonyl-1-spiro[1,3-dihydropyrido[3,4-b]indole-4,4'-piperidine]yl]methanol",
                                     'reason': 'No amine group found, or '
                                               'nitrogen not bonded as '
                                               'required'},
                                 {   'smiles': 'O(C(=O)CCCCCCCCCCCCCCC)[C@@H](COC(=O)CCCCCCCCCCCCCCCCCCC)COC(=O)CCCCCCC',
                                     'name': 'TG(20:0/16:0/8:0)',
                                     'reason': 'No amine group found, or '
                                               'nitrogen not bonded as '
                                               'required'},
                                 {   'smiles': 'O[C@@H]1CC2[C@](C3=C(C4=NCCC([C@@]4(C)CC3)[C@@H](CCC(C(C)C)C)C)CC2)(C)CC1',
                                     'name': 'UCA-1064-B',
                                     'reason': 'Structure matches amide, '
                                               'imine, or nitrile, excluding '
                                               'it as an amine'},
                                 {   'smiles': 'C1=CC=C(C=C1)N2C(=NN=C2SCC#N)COC3=CC=CC=C3',
                                     'name': '2-[[5-(phenoxymethyl)-4-phenyl-1,2,4-triazol-3-yl]thio]acetonitrile',
                                     'reason': 'Structure matches amide, '
                                               'imine, or nitrile, excluding '
                                               'it as an amine'},
                                 {   'smiles': 'O=C1C=2OC([C@H]3C[C@H](O)C(=C[C@H]3C2C(=O)C=4C1=C(O)C(=C(O)C4)C)C)(C)C',
                                     'name': 'Unnamed naphterpin 1',
                                     'reason': 'No amine group found, or '
                                               'nitrogen not bonded as '
                                               'required'},
                                 {   'smiles': 'O([C@@H]1[C@]2(C([C@@](C1)(CC2)[H])(C)C)C)C(=O)/C=C/C3=CC=C(O)C=C3',
                                     'name': '(1R,4R)-1,7,7-Trimethylbicyclo[2.2.1]heptane-2beta-ol '
                                             '3-(4-hydroxyphenyl)acrylate',
                                     'reason': 'No amine group found, or '
                                               'nitrogen not bonded as '
                                               'required'},
                                 {   'smiles': 'CC1(C)CC[C@@]2(CC[C@]3(C)C(=CC[C@@H]4[C@@]5(C)CC[C@H](O)C(C)(C)[C@@H]5CC[C@@]34C)[C@@H]2C1)C([O-])=O',
                                     'name': 'oleanolate',
                                     'reason': 'No amine group found, or '
                                               'nitrogen not bonded as '
                                               'required'},
                                 {   'smiles': 'C[C@@H]1CN(C(=O)C2=C(N=CC(=C2)C3=CCCCC3)O[C@@H]1CN(C)CC4=CC=C(C=C4)C(=O)O)[C@H](C)CO',
                                     'name': '4-[[[(2S,3R)-8-(1-cyclohexenyl)-5-[(2R)-1-hydroxypropan-2-yl]-3-methyl-6-oxo-3,4-dihydro-2H-pyrido[2,3-b][1,5]oxazocin-2-yl]methyl-methylamino]methyl]benzoic '
                                             'acid',
                                     'reason': 'Structure matches amide, '
                                               'imine, or nitrile, excluding '
                                               'it as an amine'}],
    'sample_false_negatives': [   {   'smiles': 'O[C@@H]1[C@@H](N(C)[C@@H](C1)CCCCCC(O)C)CC2=CC=CC=C2',
                                      'name': 'Preubetain J',
                                      'reason': 'No amine group found, or '
                                                'nitrogen not bonded as '
                                                'required'},
                                  {   'smiles': 'O=C(N[C@H](CO)CC1=CC=CC=C1)/C=C/CCCCC(=O)O',
                                      'name': 'Cordytakaoamide A',
                                      'reason': 'Structure matches amide, '
                                                'imine, or nitrile, excluding '
                                                'it as an amine'},
                                  {   'smiles': 'CO\\C=C\\C(=O)C1=NC2=C3C(C=NC3=C(N)C=C2NC(C)=O)=C1',
                                      'name': 'lymphostin',
                                      'reason': 'Structure matches amide, '
                                                'imine, or nitrile, excluding '
                                                'it as an amine'},
                                  {   'smiles': 'CCOC(=O)NC[C@H](Cc1ccc(OCCc2nc(oc2C)-c2ccccc2)cc1)N\\C(C)=C/C(=O)c1ccc(cc1)C(F)(F)F',
                                      'name': 'GW 6471',
                                      'reason': 'Structure matches amide, '
                                                'imine, or nitrile, excluding '
                                                'it as an amine'},
                                  {   'smiles': 'CCC(C(N)=O)(C(N)=O)c1ccccc1',
                                      'name': 'Phenylethylmalonamide',
                                      'reason': 'Structure matches amide, '
                                                'imine, or nitrile, excluding '
                                                'it as an amine'},
                                  {   'smiles': 'C[C@@H]1CN(C(=O)C2=CC=CC=C2C3=CC=CC=C3CO[C@H]1CN(C)CC4=CC=NC=C4)[C@@H](C)CO',
                                      'name': 'LSM-12472',
                                      'reason': 'Structure matches amide, '
                                                'imine, or nitrile, excluding '
                                                'it as an amine'},
                                  {   'smiles': 'C[C@@H]1CN(C(=O)CC2=C(C=CC(=C2)N(C)C)O[C@H]1CN(C)S(=O)(=O)C3=CC=CS3)[C@H](C)CO',
                                      'name': 'N-[[(2R,3R)-9-(dimethylamino)-5-[(2R)-1-hydroxypropan-2-yl]-3-methyl-6-oxo-2,3,4,7-tetrahydro-1,5-benzoxazonin-2-yl]methyl]-N-methyl-2-thiophenesulfonamide',
                                      'reason': 'Structure matches amide, '
                                                'imine, or nitrile, excluding '
                                                'it as an amine'},
                                  {   'smiles': 'C[C@H]1CN(C(=O)CC2=C(C=CC(=C2)N(C)C)O[C@@H]1CN(C)S(=O)(=O)C3=CC=CS3)[C@@H](C)CO',
                                      'name': 'N-[[(2S,3S)-9-(dimethylamino)-5-[(2S)-1-hydroxypropan-2-yl]-3-methyl-6-oxo-2,3,4,7-tetrahydro-1,5-benzoxazonin-2-yl]methyl]-N-methyl-2-thiophenesulfonamide',
                                      'reason': 'Structure matches amide, '
                                                'imine, or nitrile, excluding '
                                                'it as an amine'},
                                  {   'smiles': 'S1C=C(C(N(C(C)C)C(C)C)CCCCC#N)C=C1',
                                      'name': '6-(Diisopropylamino)-6-(3-thienyl)hexanenitrile',
                                      'reason': 'Structure matches amide, '
                                                'imine, or nitrile, excluding '
                                                'it as an amine'},
                                  {   'smiles': 'CC(C)N(C(C)C)C(=O)SCC(Cl)=C(Cl)Cl',
                                      'name': 'Tri-allate',
                                      'reason': 'Structure matches amide, '
                                                'imine, or nitrile, excluding '
                                                'it as an amine'}],
    'attempt': 5,
    'reasoning': 'The previous code failed due to an error where it attempted '
                 'to access an index of a substructure match that did not '
                 'exist, leading to a "tuple index out of range" issue. Let\'s '
                 'break down the mistakes and propose improvements:\n'
                 '\n'
                 '1. **Atom Index Assumption**: The code assumes that a match '
                 'for the amine pattern exists and tries to access the zeroth '
                 'index without checking whether a match is found. This can '
                 'lead to errors if there are no matches.\n'
                 '\n'
                 '2. **Ring Check Flaw**: The code checks whether the nitrogen '
                 'atom is part of a 5-membered ring with a hard-coded index '
                 'check '
                 '(`mol.GetSubstructMatches(primary_amine_pattern)[0][0]`). '
                 'Instead, we should first verify if a match exists and then '
                 'assess membership in any ring, not just specific sizes.\n'
                 '\n'
                 '3. **Omits Checking All Ring Sizes**: Amine nitrogen atoms '
                 'within rings of any size should be considered carefully '
                 '(e.g., excluded if part of an amide-like structure).\n'
                 '\n'
                 '4. **Simplified Structure Matching**: Instead of excluding '
                 'specific groups like amides or imines based on individual '
                 'pattern matches, we might consider defining what constitutes '
                 'a typical amine more precisely.\n'
                 '\n'
                 "To address these issues, we'll adjust the logic to:\n"
                 '- First verify that pattern matching results exist.\n'
                 '- Consider nitrogen atoms outside of commonly excluded '
                 'groups (amides, nitriles, imines) but not within any ring '
                 "system that's typically non-amine or aromatic.\n"
                 '\n'
                 "Here's the corrected code:",
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 337,
    'num_false_positives': 9964,
    'num_true_negatives': 131655,
    'num_false_negatives': 344,
    'num_negatives': None,
    'precision': 0.032715270362100764,
    'recall': 0.4948604992657856,
    'f1': 0.061373156073574936,
    'accuracy': 0.92756148981026,
    'negative_predictive_value': 0.9973939196509064}