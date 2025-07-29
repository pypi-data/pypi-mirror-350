"""
Classifies: CHEBI:24128 furanocoumarin
"""
#!/usr/bin/env python
"""
Classifies: Any furochromene that consists of a furan ring fused with a coumarin (furanocoumarin)
The function is_furanocoumarin uses improved SMARTS patterns for the coumarin (benzopyrone) core
and verifies that an aromatic furan ring is fused (sharing >=2 atoms) with the coumarin core.
"""

from rdkit import Chem

def is_furanocoumarin(smiles: str):
    """
    Determines if a molecule is a furanocoumarin based on its SMILES string.
    A furanocoumarin is defined as a coumarin (benzopyrone) with a fused furan ring.
    This function searches for the coumarin core (using one of two SMARTS variations to be more tolerant)
    and for an aromatic furan ring. Then it checks whether a furan match shares at least two atoms 
    with any coumarin match, which is our proxy for fusion.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if the molecule is classified as a furanocoumarin, False otherwise.
        str: Reason for classification.
    """
    # Parse SMILES string into a molecule
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Define two SMARTS patterns for the coumarin (benzopyrone) core.
    # The first is the classic pattern and the second a slight variation to catch substituted or fused cases.
    coumarin_smarts_list = [
        "c1ccc2oc(=O)cc2c1",   # common representation
        "c1ccc2c(c1)oc(=O)cc2"  # variation (ring order swapped)
    ]
    
    coumarin_matches = []
    for smarts in coumarin_smarts_list:
        pattern = Chem.MolFromSmarts(smarts)
        if pattern is None:
            continue
        matches = mol.GetSubstructMatches(pattern)
        if matches:
            coumarin_matches.extend(matches)
    if not coumarin_matches:
        return False, "Coumarin (benzopyrone) core not found"
    
    # Define a SMARTS pattern for an aromatic furan ring.
    # Furan is a five-membered ring with one oxygen atom.
    furan_smarts = "c1ccoc1"
    furan_pattern = Chem.MolFromSmarts(furan_smarts)
    if furan_pattern is None:
        return False, "Invalid furan SMARTS pattern"
    
    furan_matches = mol.GetSubstructMatches(furan_pattern)
    if not furan_matches:
        return False, "Furan ring not found"
    
    # Check for fusion: require that at least one furan match and one coumarin match share
    # two or more atoms. This is our proxy for the rings being fused.
    fusion_found = False
    for c_match in coumarin_matches:
        set_c = set(c_match)
        for f_match in furan_matches:
            set_f = set(f_match)
            common_atoms = set_c.intersection(set_f)
            if len(common_atoms) >= 2:
                fusion_found = True
                break
        if fusion_found:
            break

    if not fusion_found:
        return False, "Coumarin core and furan ring not properly fused"
    
    return True, "Contains a coumarin (benzopyrone) core fused with a furan ring (furanocoumarin)"


# Example usage:
if __name__ == "__main__":
    # Test with one of the known furanocoumarins - for instance, Isobergapten
    test_smiles = "COc1cc2occc2c2oc(=O)ccc12"
    result, reason = is_furanocoumarin(test_smiles)
    print(result, ":", reason)


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:24128',
                          'name': 'furanocoumarin',
                          'definition': 'Any furochromene that consists of a '
                                        'furan ring fused with a coumarin. The '
                                        'fusion may occur in different ways in '
                                        'give several isomers.',
                          'parents': ['CHEBI:39432'],
                          'xrefs': ['Wikipedia:Furocoumarin'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 61,
                           'log_lines_of_code': 4.110873864173311,
                           'indent_by_line': [   1,
                                                 1,
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
                                                 2,
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 3,
                                                 2,
                                                 2,
                                                 3,
                                                 1,
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 3,
                                                 3,
                                                 3,
                                                 4,
                                                 4,
                                                 2,
                                                 3,
                                                 0,
                                                 1,
                                                 2,
                                                 1,
                                                 1,
                                                 0,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 1],
                           'max_indent': 4,
                           'imports': ['from rdkit import Chem'],
                           'imports_count': 1,
                           'methods_called': [   'MolFromSmiles',
                                                 'MolFromSmarts',
                                                 'intersection',
                                                 'extend',
                                                 'GetSubstructMatches'],
                           'methods_called_count': 5,
                           'smarts_strings': ['smarts', 'furan_smarts'],
                           'smarts_strings_count': 2,
                           'defs': ['is_furanocoumarin(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "Coumarin (benzopyrone) core '
                                          'not found"',
                                          'False, "Invalid furan SMARTS '
                                          'pattern"',
                                          'False, "Furan ring not found"',
                                          'False, "Coumarin core and furan '
                                          'ring not properly fused"',
                                          'True, "Contains a coumarin '
                                          '(benzopyrone) core fused with a '
                                          'furan ring (furanocoumarin)"'],
                           'returns_count': 6,
                           'complexity': 4.022174772834662},
    'message': '\n'
               'Attempt failed: F1 score of 0 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: NONE\n'
               'False positives: SMILES: '
               'O=C1OC2=CC3=NC=4C(C(=O)O)=CC=CC4N(C3=CC2=C1C5=CC=CC=C5)CC=C(CCC=C(C)C)C '
               'NAME: Benthocyanin A REASON: WRONGLY CLASSIFIED Contains a '
               'coumarin core fused with a furan ring (furanocoumarin)\n'
               ' * SMILES: '
               'O=C1OC2=C(C3=NC=4C=CC=CC4N(C3=CC2=C1C5=CC=CC=C5)C/C=C(\\CCC=C(C)C)/C)C(=O)O '
               'NAME: Benthocyanin B REASON: WRONGLY CLASSIFIED Contains a '
               'coumarin core fused with a furan ring (furanocoumarin)\n'
               'False negatives: SMILES: COc1cc2occc2c2oc(=O)ccc12 NAME: '
               'Isobergapten REASON: MISSED Coumarin (benzopyrone) core not '
               'found\n'
               ' * SMILES: '
               'O1C(CC=2C1=C(C(O)=C3C2OC(=O)C=C3CCC)C(=O)C(CC)C)C(O)(C)C NAME: '
               'MAB 4 REASON: MISSED Coumarin (benzopyrone) core not found\n'
               ' * SMILES: '
               'O1C(OC(C(O)COC2=C3OC=CC3=C(OC)C4=C2OC(=O)C=C4)(C)C)C(O)C(O)C(O)C1CO '
               "NAME: (R)-Byakangelicin 3'-glucoside REASON: MISSED Coumarin "
               '(benzopyrone) core not found\n'
               ' * SMILES: O1C2=C(C=C3C(OC(=O)C=C3)=C2OCC=C)C=C1 NAME: '
               '8-allyloxypsoralen REASON: MISSED Coumarin (benzopyrone) core '
               'not found\n'
               ' * SMILES: '
               'S(OCC(O)(C1OC2=C(C1OC(=O)/C(/C)=C/C)C=3OC(=O)C=CC3C=C2)C)(O)(=O)=O '
               'NAME: '
               '[2-hydroxy-2-(9-{[(2E)-2-methylbut-2-enoyl]oxy}-2-oxo-2H,8H,9H-furo[2,3-h]chromen-8-yl)propoxy]sulfonic '
               'acid REASON: MISSED Coumarin (benzopyrone) core not found\n'
               ' * SMILES: '
               'O1C2=C(C(OC)=C3C(OC(=O)C(=C3O)C4=CC=C(OC)C=C4)=C2OC)C=C1C(C)=C '
               'NAME: Thonningine B REASON: MISSED Coumarin (benzopyrone) core '
               'not found\n'
               ' * SMILES: CC(C)=CCc1c2ccoc2c(O)c2oc(=O)ccc12 NAME: '
               'Alloimperatorin REASON: MISSED Coumarin (benzopyrone) core not '
               'found\n'
               ' * SMILES: CC(C)(O)C1Cc2c(O1)ccc1ccc(=O)oc21 NAME: '
               'columbianetin REASON: MISSED Coumarin (benzopyrone) core not '
               'found\n'
               ' * SMILES: '
               'C[C@@H]1c2c(O[C@]1(C)CCC\\C(C)=C\\C(=O)C=C(C)C)c1ccc(O)cc1oc2=O '
               'NAME: fukanefuromarin B REASON: MISSED Coumarin (benzopyrone) '
               'core not found\n'
               ' * SMILES: '
               'O(C(C1OC2=C(C1)C=C3C(OC(=O)C=C3)=C2O)(C)C)C4OC(C(O)C(O)C4O)COC(=O)/C=C/C5=CC(OC)=C(O)C(OC)=C5 '
               "NAME: (R)-Rutaretin 1'-(6''-sinapoylglucoside) REASON: MISSED "
               'Coumarin (benzopyrone) core not found\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'C1=CC=C2C(=C1)C(=O)C3=CC=CC=C3C2(CC4=CC(=NC=C4)F)CC5=CC(=NC=C5)F',
                                     'name': '10,10-bis[(2-fluoro-4-pyridinyl)methyl]-9-anthracenone',
                                     'reason': 'Coumarin (benzopyrone) core '
                                               'not found'},
                                 {   'smiles': 'C[C@@H](C1=CC=CC=C1)NC(=O)[C@@H]2[C@H]([C@@H]3CN4C(=CC=C(C4=O)C5=CC=CC=C5F)[C@H]2N3C)CO',
                                     'name': 'LSM-10936',
                                     'reason': 'Coumarin (benzopyrone) core '
                                               'not found'},
                                 {   'smiles': '[H]C(=CC(=O)C(O)=O)C(CC(O)=O)C(O)=O',
                                     'name': '5-oxopent-3-ene-1,2,5-tricarboxylic '
                                             'acid',
                                     'reason': 'Coumarin (benzopyrone) core '
                                               'not found'},
                                 {   'smiles': 'S1N(C2=CC=C(C=C2)C(OCC)=O)C(=O)C=C1',
                                     'name': 'ethyl '
                                             '4-(3-oxo-2,3-dihydroisothiazol-2-yl)benzoate',
                                     'reason': 'Coumarin (benzopyrone) core '
                                               'not found'},
                                 {   'smiles': 'COc1cc(O)c2c(c1)oc1c(O)cccc1c2=O',
                                     'name': 'mesuaxanthone A',
                                     'reason': 'Coumarin (benzopyrone) core '
                                               'not found'},
                                 {   'smiles': 'O([C@@H]1[C@H](O)[C@@H](O[C@@H]([C@H]1O)CO[C@H]2O[C@@H]([C@@H](O)[C@H](O)[C@@H]2O[C@@H]3O[C@@H]([C@@H](O)[C@H](O)[C@H]3NC(=O)C)CO)CO[C@@H]4O[C@@H]([C@@H](O)[C@H](O)[C@H]4NC(=O)C)CO)O[C@H]5[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]5CO)O[C@H]6[C@H](O)[C@@H](NC(=O)C)C(O[C@@H]6CO)O)[C@H]7O[C@@H]([C@@H](O[C@@H]8O[C@@H]([C@@H](O)[C@H](O)[C@H]8NC(=O)C)CO)[C@H](O)[C@@H]7O[C@@H]9O[C@@H]([C@@H](O[C@@H]%10O[C@@H]([C@H](O)[C@H](O)[C@H]%10O)CO)[C@H](O)[C@H]9NC(=O)C)CO)CO',
                                     'name': 'N-[(3R,4R,5S,6R)-5-[(2S,3R,4R,5S,6R)-3-Acetamido-5-[(2S,3S,4S,5R,6R)-6-[[(2S,3S,4S,5S,6R)-3-[(2R,3R,4R,5S,6R)-3-acetamido-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-6-[[(2R,3R,4R,5S,6R)-3-acetamido-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxymethyl]-4,5-dihydroxyoxan-2-yl]oxymethyl]-4-[(2R,3S,4S,5S,6R)-5-[(2R,3R,4R,5S,6R)-3-acetamido-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-3-[(2S,3R,4R,5S,6R)-3-acetamido-4-hydroxy-6-(hydroxymethyl)-5-[(2S,3R,4S,5R,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-3,5-dihydroxyoxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-2,4-dihydroxy-6-(hydroxymethyl)oxan-3-yl]acetamide',
                                     'reason': 'Coumarin (benzopyrone) core '
                                               'not found'},
                                 {   'smiles': 'CCCCCCCC\\C=C/CCCCCCCC(=O)OC[C@H](COP([O-])(=O)OC[C@H]([NH3+])C([O-])=O)OC(=O)CCC\\C=C/C\\C=C/C\\C=C/C\\C=C/CCCCC',
                                     'name': '1-oleoyl-2-arachidonoyl-sn-glycero-3-phospho-L-serine(1-)',
                                     'reason': 'Coumarin (benzopyrone) core '
                                               'not found'},
                                 {   'smiles': 'OC(=Cc1ccccc1)C([O-])=O',
                                     'name': 'enol-phenylpyruvate',
                                     'reason': 'Coumarin (benzopyrone) core '
                                               'not found'},
                                 {   'smiles': '[H][C@]1(CC[C@]2(C)[C@@H](O)CCC(=C)[C@@]12[H])[C@@H](O)C(C)C',
                                     'name': '(1R,3aS,4S,7aR)-1-((S)-1-hydroxy-2-methylpropyl)-3a-methyl-7-methyleneoctahydro-1H-inden-4-ol',
                                     'reason': 'Coumarin (benzopyrone) core '
                                               'not found'},
                                 {   'smiles': 'O1C(C(O)C(O)C(O)C1CO)C=2C(=O)C=3C(O)=C(C4OC(C(O)C(O)C4O)CO)C(O)=CC3OC2C5=CC=C(OC)C=C5',
                                     'name': "3,6-Diglucopyranosyl-5,7-dihydroxy-4'-methoxyflavone",
                                     'reason': 'Coumarin (benzopyrone) core '
                                               'not found'}],
    'sample_false_negatives': [   {   'smiles': 'O1C(CC=2C1=C(C(O)=C3C2OC(=O)C=C3CCC)C(=O)C(CC)C)C(O)(C)C',
                                      'name': 'MAB 4',
                                      'reason': 'Furan ring not found'},
                                  {   'smiles': 'S(OCC(O)(C1OC2=C(C1OC(=O)/C(/C)=C/C)C=3OC(=O)C=CC3C=C2)C)(O)(=O)=O',
                                      'name': '[2-hydroxy-2-(9-{[(2E)-2-methylbut-2-enoyl]oxy}-2-oxo-2H,8H,9H-furo[2,3-h]chromen-8-yl)propoxy]sulfonic '
                                              'acid',
                                      'reason': 'Furan ring not found'},
                                  {   'smiles': 'CC(C)(O)C1Cc2c(O1)ccc1ccc(=O)oc21',
                                      'name': 'columbianetin',
                                      'reason': 'Furan ring not found'},
                                  {   'smiles': 'C[C@@H]1c2c(O[C@]1(C)CCC\\C(C)=C\\C(=O)C=C(C)C)c1ccc(O)cc1oc2=O',
                                      'name': 'fukanefuromarin B',
                                      'reason': 'Furan ring not found'},
                                  {   'smiles': 'O(C(C1OC2=C(C1)C=C3C(OC(=O)C=C3)=C2O)(C)C)C4OC(C(O)C(O)C4O)COC(=O)/C=C/C5=CC(OC)=C(O)C(OC)=C5',
                                      'name': '(R)-Rutaretin '
                                              "1'-(6''-sinapoylglucoside)",
                                      'reason': 'Furan ring not found'},
                                  {   'smiles': 'O(C([C@]1(OC2=C([C@H]1O)C=3OC(=O)C=CC3C=C2)[H])(C)C)[C@@H]4O[C@@H]([C@@H](O)[C@H](O)[C@H]4O)CO',
                                      'name': 'Apterin',
                                      'reason': 'Furan ring not found'},
                                  {   'smiles': 'O1[C@@H](CC2=C1C=C3OC(=O)C=CC3=C2)C(O[C@@H]4O[C@@H]([C@@H](O)[C@H](O)[C@H]4O)CO)(C)C',
                                      'name': 'marmesinin',
                                      'reason': 'Furan ring not found'},
                                  {   'smiles': 'CC(=O)OC(C)(C)[C@@H]1Cc2cc3cc(c(=O)oc3cc2O1)C(C)(C)C=C',
                                      'name': 'Rutamarin',
                                      'reason': 'Furan ring not found'},
                                  {   'smiles': 'C[C@@H]1c2c(O[C@]1(C)CC\\C=C(/C)CC(=O)C=C(C)C)c1ccc(O)cc1oc2=O',
                                      'name': '(2R*,3R*)-2,3-dihydro-7-hydroxy-2,3-dimethyl-2-[4,8-dimethyl-3(E)-7-nonadien-6-onyl]furo[3,2-c]coumarin',
                                      'reason': 'Furan ring not found'},
                                  {   'smiles': 'O1C(CC2=C1C=C3OC(=O)C(C(C)(C)C=C)=CC3=C2)C(C)=C',
                                      'name': 'exo-Dehydrochalepin',
                                      'reason': 'Furan ring not found'}],
    'attempt': 2,
    'reasoning': 'Below is our detailed reasoning and revised code. In our '
                 'previous attempt the coumarin SMARTS was too strict. Many '
                 'true furanocoumarins (for example, isobergapten and related '
                 'derivatives) have extra fused rings or substituents that '
                 'break an exact match to "c1ccc2oc(=O)cc2c1". We therefore '
                 'improve our detection by (1) trying two coumarin SMARTS '
                 'variants (which often pick up slightly different '
                 'representation of the coumarin (benzopyrone) core) and (2) '
                 'ensuring that the furan ring (using a simple “c1ccoc1” '
                 'match) is fused (sharing at least two atoms) with the '
                 'coumarin core. This fusion requirement is intended to be '
                 'stringent enough to avoid mis‐classifying unrelated '
                 'compounds (the false positives) while hopefully catching the '
                 'diverse true furanocoumarins.\n'
                 '\n'
                 'Below is the complete program in a single Python code '
                 'block:\n'
                 '\n'
                 '------------------------------------------------',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 74,
    'num_false_positives': 52,
    'num_true_negatives': 142083,
    'num_false_negatives': 91,
    'num_negatives': None,
    'precision': 0.5873015873015873,
    'recall': 0.4484848484848485,
    'f1': 0.5085910652920963,
    'accuracy': 0.9989950808151792,
    'negative_predictive_value': 0.9993599392293949}