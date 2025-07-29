"""
Classifies: CHEBI:192499 anthoxanthin
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_anthoxanthin(smiles: str):
    """
    Determines if a molecule is an anthoxanthin based on its SMILES string.
    Anthoxanthins are a type of flavonoid pigments, with a benzopyran-4-one core.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is an anthoxanthin, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # 1. Core benzopyran-4-one structure (flavone or flavonol)
    # Flavone (C=O at position 4):
    flavone_core_pattern = Chem.MolFromSmarts("c1ccc(-c2cc(=O)c3ccccc3o2)cc1") # more precise
    # Flavonol (C=O at position 4, and OH at position 3):
    flavonol_core_pattern = Chem.MolFromSmarts("c1ccc(-c2c(O)cc(=O)c3ccccc3o2)cc1")

    if not (mol.HasSubstructMatch(flavone_core_pattern) or mol.HasSubstructMatch(flavonol_core_pattern)):
        return False, "No benzopyran-4-one core structure found"
    
    # 2. Check for Hydroxyl and Methoxy groups. Count how many. At least one of each
    num_hydroxyls = len(mol.GetSubstructMatches(Chem.MolFromSmarts("[OH]")))
    num_methoxys = len(mol.GetSubstructMatches(Chem.MolFromSmarts("OC")))

    if num_hydroxyls == 0 and num_methoxys == 0:
        return False, "No hydroxyl or methoxy groups found"

    # 3. Check for glycosylation (O-C-O outside of the core pattern)
    glycoside_pattern = Chem.MolFromSmarts("O-C-O")
    core_match = mol.GetSubstructMatch(flavone_core_pattern) if mol.HasSubstructMatch(flavone_core_pattern) else mol.GetSubstructMatch(flavonol_core_pattern)
    if core_match:
      core_atoms = set(core_match)
      glycoside_matches = [match for match in mol.GetSubstructMatches(glycoside_pattern) if not set(match) <= core_atoms]
      if len(glycoside_matches) > 0:
         return True, "Benzopyran-4-one core structure with hydroxyl and/or methoxy, and possible glycosylation found"

    # 4. Check if additional aromatic rings are present
    aromatic_rings = Chem.MolFromSmarts("c1ccccc1")
    num_aromatic_rings = len(mol.GetSubstructMatches(aromatic_rings))

    if num_aromatic_rings >= 2:
        return True, "Benzopyran-4-one core structure with hydroxyl and/or methoxy and additional aromatic ring found"
    
    return True, "Benzopyran-4-one core structure with hydroxyl and/or methoxy found"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:192499',
                          'name': 'anthoxanthin',
                          'definition': 'are a type of flavonoid pigments in '
                                        'plants. Anthoxanthins are '
                                        'water-soluble pigments which range in '
                                        'color from white or colorless to a '
                                        'creamy to yellow, often on petals of '
                                        'flowers.',
                          'parents': ['CHEBI:47916'],
                          'xrefs': [   'Wikipedia:https://en.wikipedia.org/wiki/Anthoxanthin'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 38,
                           'log_lines_of_code': 3.6375861597263857,
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
                                                 1,
                                                 0,
                                                 1,
                                                 2,
                                                 1,
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
                                                 1,
                                                 1,
                                                 1,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 0,
                                                 1,
                                                 2,
                                                 1,
                                                 1],
                           'max_indent': 2,
                           'imports': [   'from rdkit import Chem',
                                          'from rdkit.Chem import AllChem',
                                          'from rdkit.Chem import '
                                          'rdMolDescriptors'],
                           'imports_count': 3,
                           'methods_called': [   'GetSubstructMatches',
                                                 'MolFromSmarts',
                                                 'HasSubstructMatch',
                                                 'MolFromSmiles',
                                                 'GetSubstructMatch'],
                           'methods_called_count': 5,
                           'smarts_strings': [   '"OC"))',
                                                 '"[OH]"))',
                                                 'c1ccccc1',
                                                 'O-C-O',
                                                 'c1ccc(-c2c(O)cc(=O)c3ccccc3o2)cc1',
                                                 'c1ccc(-c2cc(=O)c3ccccc3o2)cc1'],
                           'smarts_strings_count': 6,
                           'defs': ['is_anthoxanthin(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "No benzopyran-4-one core '
                                          'structure found"',
                                          'False, "No hydroxyl or methoxy '
                                          'groups found"',
                                          'True, "Benzopyran-4-one core '
                                          'structure with hydroxyl and/or '
                                          'methoxy, and possible glycosylation '
                                          'found"',
                                          'True, "Benzopyran-4-one core '
                                          'structure with hydroxyl and/or '
                                          'methoxy and additional aromatic '
                                          'ring found"',
                                          'True, "Benzopyran-4-one core '
                                          'structure with hydroxyl and/or '
                                          'methoxy found"'],
                           'returns_count': 6,
                           'complexity': 3.527517231945277},
    'message': None,
    'sample_true_negatives': [   {   'smiles': 'CCN1N=C(N=N1)C2=CC=CC=C2NC(=O)C3=CC=C(C=C3)N4C=NN=N4',
                                     'name': 'N-[2-(2-ethyl-5-tetrazolyl)phenyl]-4-(1-tetrazolyl)benzamide',
                                     'reason': 'No benzopyran-4-one core '
                                               'structure found'},
                                 {   'smiles': 'CCS(=O)(=O)N1CC2(C1)[C@@H]([C@@H](N2C(=O)C3CCCC3)CO)C4=CC=C(C=C4)C=CC',
                                     'name': 'LSM-38092',
                                     'reason': 'No benzopyran-4-one core '
                                               'structure found'},
                                 {   'smiles': 'O=C/1N/C(/C(=O)N\\C1=C\\C2=CC=CC=C2)=C\\C=3N=CNC3C(C=C)(C)C',
                                     'name': 'DeltaPLH',
                                     'reason': 'No benzopyran-4-one core '
                                               'structure found'},
                                 {   'smiles': 'C1CCN(CC1)C(=O)C[C@H]2C[C@@H]3[C@H]([C@@H](O2)CO)OC4=C3C=C(C=C4)NC(=O)CC5CC5',
                                     'name': 'N-[(1S,3R,4aS,9aR)-1-(hydroxymethyl)-3-[2-oxo-2-(1-piperidinyl)ethyl]-3,4,4a,9a-tetrahydro-1H-pyrano[3,4-b]benzofuran-6-yl]-2-cyclopropylacetamide',
                                     'reason': 'No benzopyran-4-one core '
                                               'structure found'},
                                 {   'smiles': 'C[C@H]1C[C@@]2(OC(=O)c3ccccc3)[C@H]([C@H]1OC(C)=O)[C@@H](O)\\C(C)=C/C[C@H]1[C@@H](\\C=C(C)\\C2=O)C1(C)C',
                                     'name': '(-)-(6Z,12E,2S,3S,4R,5R,9S,11S,15R)-3-acetoxy-15-benzoyloxylathyra-6,12-dien-5-ol-14-one',
                                     'reason': 'No benzopyran-4-one core '
                                               'structure found'},
                                 {   'smiles': 'O=C1C(O)=CC=2O[C@]3([C@H](O)C[C@@H]4[C@](OC=5C=C(O)C(C=C(C5C4)C)=O)(CC=CC(C[C@H]3CC2C(=C1)C)(C)C)C)C',
                                     'name': 'Eupenifeldin',
                                     'reason': 'No benzopyran-4-one core '
                                               'structure found'},
                                 {   'smiles': 'O1[C@@H](O[C@@H]2[C@@H](OC[C@H]3O[C@@H](O[C@H]4[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]4CO)O[C@H]5[C@H](O)[C@@H](NC(=O)C)C(O[C@@H]5CO[C@@H]6O[C@H]([C@@H](O)[C@@H](O)[C@@H]6O)C)O)[C@@H](O)[C@@H](O[C@H]7O[C@@H]([C@@H](O)[C@H](O)[C@@H]7O[C@@H]8O[C@@H]([C@@H](O[C@@H]9O[C@@H]([C@H](O)[C@H](O)[C@H]9NC(=O)C)CO)[C@H](O)[C@H]8NC(=O)C)CO)CO)[C@@H]3O)O[C@@H]([C@@H](O)[C@@H]2O)CO)[C@H](NC(=O)C)[C@@H](O[C@@H]%10O[C@H]([C@@H](O)[C@@H](O)[C@@H]%10O)C)[C@H](O[C@@H]%11O[C@@H]([C@H](O)[C@H](O)[C@H]%11NC(=O)C)CO)[C@H]1CO',
                                     'name': 'N-[(3R,4R,5S,6R)-5-[(2S,3R,4R,5S,6R)-3-Acetamido-5-[(2S,3S,4S,5R,6R)-4-[(2R,3S,4S,5S,6R)-3-[(2S,3R,4R,5S,6R)-3-acetamido-5-[(2S,3R,4R,5R,6R)-3-acetamido-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-6-[[(2S,3S,4S,5S,6R)-3-[(2S,3R,4R,5S,6R)-3-acetamido-5-[(2S,3R,4R,5R,6R)-3-acetamido-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-6-(hydroxymethyl)-4-[(2R,3S,4R,5S,6S)-3,4,5-trihydroxy-6-methyloxan-2-yl]oxyoxan-2-yl]oxy-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxymethyl]-3,5-dihydroxyoxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-2,4-dihydroxy-6-[[(2R,3S,4R,5S,6S)-3,4,5-trihydroxy-6-methyloxan-2-yl]oxymethyl]oxan-3-yl]acetamide',
                                     'reason': 'No benzopyran-4-one core '
                                               'structure found'},
                                 {   'smiles': 'CN1C[C@@H]2C[C@H](Cn3c2cccc3=O)[C@H]1CC=C',
                                     'name': 'Tinctorine',
                                     'reason': 'No benzopyran-4-one core '
                                               'structure found'},
                                 {   'smiles': 'CCC1=C2COC(CC2=C3C(=C(OC3=N1)C(=O)C4=CC=CC=C4)N)(C)C',
                                     'name': 'LSM-4563',
                                     'reason': 'No benzopyran-4-one core '
                                               'structure found'},
                                 {   'smiles': 'CN1CCN(CC1)C(=O)C[C@@H]2CC[C@H]3[C@H](O2)COC[C@@H](CN3C(=O)NC4=CC5=C(C=C4)OCO5)O',
                                     'name': '(3R,6aS,8S,10aS)-N-(1,3-benzodioxol-5-yl)-3-hydroxy-8-[2-(4-methyl-1-piperazinyl)-2-oxoethyl]-3,4,6,6a,8,9,10,10a-octahydro-2H-pyrano[2,3-c][1,5]oxazocine-1-carboxamide',
                                     'reason': 'No benzopyran-4-one core '
                                               'structure found'}],
    'sample_false_negatives': [   {   'smiles': 'C1(OC2=CC(O)=C3C(OC=C(C3=O)C4=CC=C(O)C=C4)=C2)OC(COC(C)=O)C(O)C(O)C1O',
                                      'name': "6''-O-acetylgenistin",
                                      'reason': 'No benzopyran-4-one core '
                                                'structure found'},
                                  {   'smiles': 'OC[C@@]1(O)CO[C@@H](OC[C@H]2O[C@H]([C@H](O)[C@@H](O)[C@@H]2O)c2c(O)ccc3c2occ(-c2ccc(O)cc2)c3=O)[C@@H]1O',
                                      'name': 'mirificin',
                                      'reason': 'No benzopyran-4-one core '
                                                'structure found'},
                                  {   'smiles': 'O[C@@H]1[C@@H](O)[C@@H](O[C@@H]([C@H]1O)C(O)=O)Oc1cc(O)c2C(=O)C[C@@H](Oc2c1)c1ccc(O)c(O)c1',
                                      'name': '(2R)-eriodictoyl-7-O-beta-D-glucopyranosiduronic '
                                              'acid',
                                      'reason': 'No benzopyran-4-one core '
                                                'structure found'},
                                  {   'smiles': 'O=c1cc(oc2ccccc12)-c1ccccc1',
                                      'name': 'flavone',
                                      'reason': 'No hydroxyl or methoxy groups '
                                                'found'},
                                  {   'smiles': 'OC[C@H]1O[C@@H](Oc2cc(O)c3C(=O)C[C@H](Oc3c2[C@@H]2OC[C@H](O)[C@H](O)[C@H]2O)c2ccc(O)cc2)[C@H](O)[C@@H](O)[C@@H]1O',
                                      'name': '8-C-alpha-L-arabinopyranosyl-7-O-beta-D-glucopyranosylnaringenin',
                                      'reason': 'No benzopyran-4-one core '
                                                'structure found'},
                                  {   'smiles': 'COC1=CC2OC(=CC(=O)C2C(O)=C1[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O)c1ccc(O)c(O)c1',
                                      'name': 'swertiajaponin',
                                      'reason': 'No benzopyran-4-one core '
                                                'structure found'},
                                  {   'smiles': 'Oc1ccc(cc1)[C@H]1Oc2cc(O)cc(O)c2C(=O)[C@@H]1[C@H]1[C@@H](Oc2cc(O)cc(O)c2C1=O)c1ccc(O)cc1',
                                      'name': 'isochamaejasmin',
                                      'reason': 'No benzopyran-4-one core '
                                                'structure found'},
                                  {   'smiles': 'C[C@@H]1O[C@H](O[C@@H]2[C@@H](O)[C@H](O)[C@@H](CO)O[C@H]2Oc2ccc3C(=O)CC(Oc3c2)c2ccccc2)[C@H](O)[C@H](O)[C@H]1O',
                                      'name': '7-hydroxyflavanone '
                                              '7-O-[beta-L-rhamnosyl-(1->2)-beta-D-glucoside]',
                                      'reason': 'No benzopyran-4-one core '
                                                'structure found'},
                                  {   'smiles': '[C@H]1(C=2C3=C(C(C(C4=CC=C(O)C=C4)=CO3)=O)C=CC2[O-])[C@@H]([C@H]([C@H](O)[C@@H](CO)O1)O)O',
                                      'name': 'puerarin(1-)',
                                      'reason': 'No benzopyran-4-one core '
                                                'structure found'}],
    'attempt': 0,
    'reasoning': "Okay, let's outline a plan to classify anthoxanthins using "
                 'their SMILES strings.\n'
                 '\n'
                 'Anthoxanthins are a subclass of flavonoids, characterized by '
                 'a flavone or flavonol (benzopyran-4-one) core structure. '
                 'They typically have hydroxyl groups (-OH) and methoxy groups '
                 '(-OCH3) substitutions, and can be glycosylated.\n'
                 "Here's the strategy:\n"
                 '\n'
                 '1.  **Core Structure:** Identify the benzopyran-4-one '
                 '(flavone/flavonol) skeleton. We can use SMARTS patterns for '
                 'this. This will be the most important step.\n'
                 '2.  **Hydroxyl and Methoxy Groups:** Check for the presence '
                 'of multiple -OH and -OCH3 groups. While not strictly unique, '
                 "they're common in anthoxanthins.\n"
                 '3.  **Glycosylation:** Anthoxanthins are frequently found as '
                 'glycosides. Look for sugar moieties connected to the core '
                 'structure. This might be difficult to be very precise, so we '
                 'will try to search for a O-C-O pattern outside of the '
                 'flavone core.\n'
                 '4. **Additional aromatic rings:** Some of the examples show '
                 'additional aromatic rings attached to the main flavone '
                 'scaffold\n'
                 '5.  **Reasoning:** Provide a clear reason for classification '
                 'based on whether the core structure and other characteristic '
                 'features were identified.\n'
                 '\n'
                 "Let's put this into code.",
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 508,
    'num_false_positives': 1070,
    'num_true_negatives': 140713,
    'num_false_negatives': 9,
    'num_negatives': None,
    'precision': 0.32192648922686945,
    'recall': 0.9825918762088974,
    'f1': 0.48496420047732697,
    'accuracy': 0.9924174279690794,
    'negative_predictive_value': 0.999936044115348}