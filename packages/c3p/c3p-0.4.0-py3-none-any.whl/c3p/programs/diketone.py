"""
Classifies: CHEBI:46640 diketone
"""
from rdkit import Chem

def is_diketone(smiles: str):
    """
    Determines if a molecule is a diketone based on its SMILES string.
    A diketone is a molecule containing exactly two ketone (C=O) functionalities.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a diketone, False otherwise
        str: Reason for classification
    """
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Define ketone SMARTS pattern
    # [CX3](=[OX1])([CX4])([CX4])  is a carbon double bonded to oxygen and bonded to two other carbons
    ketone_pattern = Chem.MolFromSmarts("[CX3](=[OX1])([CX4])([CX4])")

    # Find all matches of the ketone pattern
    ketone_matches = mol.GetSubstructMatches(ketone_pattern)
    
    # Check if exactly 2 ketone groups are present
    if len(ketone_matches) == 2:
        return True, "Molecule contains exactly two ketone groups."
    else:
        return False, f"Molecule contains {len(ketone_matches)} ketone group(s), requires exactly two."


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:46640',
                          'name': 'diketone',
                          'definition': 'A compound that contains two ketone '
                                        'functionalities.',
                          'parents': ['CHEBI:17087'],
                          'xrefs': ['Wikipedia:Diketone'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 23,
                           'log_lines_of_code': 3.1354942159291497,
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
                                                 1,
                                                 2,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 1,
                                                 2],
                           'max_indent': 2,
                           'imports': ['from rdkit import Chem'],
                           'imports_count': 1,
                           'methods_called': [   'MolFromSmiles',
                                                 'MolFromSmarts',
                                                 'GetSubstructMatches'],
                           'methods_called_count': 3,
                           'smarts_strings': ['[CX3](=[OX1])([CX4])([CX4])'],
                           'smarts_strings_count': 1,
                           'defs': ['is_diketone(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'True, "Molecule contains exactly '
                                          'two ketone groups."',
                                          'False, f"Molecule contains '
                                          '{len(ketone_matches)} ketone '
                                          'group(s), requires exactly two."'],
                           'returns_count': 3,
                           'complexity': 2.42709884318583},
    'message': '\n'
               'Attempt failed: F1 score of 0.006335983104045057 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: '
               'C1C([C@H](C([C@]2([H])[C@]1(C)[C@@]3(C(C=C([C@H]([C@]3(CC2)[H])C)C=C)=O)[H])(C)C)O)=O '
               'NAME: (+)-phytocassane D REASON: CORRECT Molecule contains '
               'exactly two ketone groups.\n'
               ' * SMILES: O=C(C(C)C)C(=O)C NAME: 4-Methyl-2,3-pentanedione '
               'REASON: CORRECT Molecule contains exactly two ketone groups.\n'
               ' * SMILES: '
               '[H][C@]12N(C)C3=C(C=C(Cl)C(OC)=C3OC)[C@@]1(O)[C@@H](O)[C@@]13SS[C@@](C)(N(C)C1=O)C(=O)N23 '
               'NAME: sporidesmin A REASON: CORRECT Molecule contains exactly '
               'two ketone groups.\n'
               ' * SMILES: O=C(CCCCCCCCCCCCCCCCCCC)CC(=O)CCCCC NAME: '
               'Heptacosane-6,8-dione REASON: CORRECT Molecule contains '
               'exactly two ketone groups.\n'
               ' * SMILES: CC1(C)C(=O)C(=O)c2c1[nH]c1cc(O)ccc21 NAME: '
               'bruceolline H REASON: CORRECT Molecule contains exactly two '
               'ketone groups.\n'
               ' * SMILES: CC(C)[C@H]1OC(=O)[C@H](Cc2ccccc2)N(C)C1=O NAME: '
               'bassiatin REASON: CORRECT Molecule contains exactly two ketone '
               'groups.\n'
               ' * SMILES: O=C1C(CCCCC1)C(=O)C NAME: 2-Acetylcycloheptanone '
               'REASON: CORRECT Molecule contains exactly two ketone groups.\n'
               ' * SMILES: O=C(CCCCCCCCCCC)CC(=O)CCC1=CC(OC)=C(O)C=C1 NAME: '
               '[12]-Gingerdione REASON: CORRECT Molecule contains exactly two '
               'ketone groups.\n'
               ' * SMILES: O=C(CCCCCCCCCCCCCCCCCC)CC(=O)CCC NAME: '
               '4,6-Tetracosanedione REASON: CORRECT Molecule contains exactly '
               'two ketone groups.\n'
               ' * SMILES: O=C(CC(C)C)CC(=O)C NAME: 6-Methylheptan-2,4-dione '
               'REASON: CORRECT Molecule contains exactly two ketone groups.\n'
               ' * SMILES: CC(=O)C(O)C(=O)COP(O)(O)=O NAME: '
               '3-hydroxy-2,4-dioxopentyl phosphate REASON: CORRECT Molecule '
               'contains exactly two ketone groups.\n'
               ' * SMILES: CC(=O)CC(C)=O NAME: acetylacetone REASON: CORRECT '
               'Molecule contains exactly two ketone groups.\n'
               ' * SMILES: COc1ccc(cc1)C1C(=O)c2ccccc2C1=O NAME: anisindione '
               'REASON: CORRECT Molecule contains exactly two ketone groups.\n'
               ' * SMILES: C(CCCCCCCCCCCC(CC(CCCC)=O)=O)C NAME: '
               '5,7-icosanedione REASON: CORRECT Molecule contains exactly two '
               'ketone groups.\n'
               ' * SMILES: CC(=O)C(=O)c1ccccc1 NAME: 1-phenyl-1,2-propanedione '
               'REASON: CORRECT Molecule contains exactly two ketone groups.\n'
               ' * SMILES: O=C(CC(C)C)C(=O)C NAME: 5-Methyl-2,3-hexanedione '
               'REASON: CORRECT Molecule contains exactly two ketone groups.\n'
               ' * SMILES: O=C(CCCCCCCCCCCCCCC)CC(=O)CCC NAME: '
               'Henicosane-4,6-dione REASON: CORRECT Molecule contains exactly '
               'two ketone groups.\n'
               ' * SMILES: O=C(CCCCCCCC)C(=O)C NAME: 2,3-Undecanedione REASON: '
               'CORRECT Molecule contains exactly two ketone groups.\n'
               ' * SMILES: '
               'C1[C@]2(CC(CC([C@@]2([C@]3(CC[C@]4([C@]([C@@]3(C1)[H])(CC[C@@H]4O)[H])C)[H])C)=O)=O)[H] '
               'NAME: 17beta-hydroxyandrostan-1,3-dione REASON: CORRECT '
               'Molecule contains exactly two ketone groups.\n'
               ' * SMILES: O=C(C(=O)c1ccccc1)c1ccccc1 NAME: benzil REASON: '
               'CORRECT Molecule contains exactly two ketone groups.\n'
               ' * SMILES: CC1(C)C2CC(=O)C1(C)C(=O)C2 NAME: bornane-2,6-dione '
               'REASON: CORRECT Molecule contains exactly two ketone groups.\n'
               ' * SMILES: COC(OC)C(=O)C(=O)c1ccccc1 NAME: '
               '3,3-dimethoxy-1-phenylpropane-1,2-dione REASON: CORRECT '
               'Molecule contains exactly two ketone groups.\n'
               ' * SMILES: COc1cc(CCC(=O)CC(=O)\\C=C\\c2ccc(O)c(OC)c2)ccc1O '
               'NAME: dihydrocurcumin REASON: CORRECT Molecule contains '
               'exactly two ketone groups.\n'
               ' * SMILES: CC(=O)C(=O)[C@@H](O)COP(O)(O)=O NAME: '
               '(2S)-2-hydroxy-3,4-diketopentyl phosphate REASON: CORRECT '
               'Molecule contains exactly two ketone groups.\n'
               ' * SMILES: '
               '[H][C@@]1(CC[C@@]2(C)C3=C(CC[C@]12C)[C@@]1(C)CCC(=O)C(C)(C)[C@]1([H])CC3=O)[C@H](C)CCC1OC1(C)CO '
               'NAME: ganoderone C REASON: CORRECT Molecule contains exactly '
               'two ketone groups.\n'
               'False positives: SMILES: '
               'C1CCN(CC1)C(=O)C[C@H]2C[C@@H]3[C@H]([C@@H](O2)CO)OC4=C3C=C(C=C4)NC(=O)CC5CC5 '
               'NAME: '
               'N-[(1S,3R,4aS,9aR)-1-(hydroxymethyl)-3-[2-oxo-2-(1-piperidinyl)ethyl]-3,4,4a,9a-tetrahydro-1H-pyrano[3,4-b]benzofuran-6-yl]-2-cyclopropylacetamide '
               'REASON: WRONGLY CLASSIFIED Molecule contains exactly two '
               'ketone groups.\n'
               ' * SMILES: '
               'CN1CCN(CC1)C(=O)C[C@@H]2CC[C@H]3[C@H](O2)COC[C@@H](CN3C(=O)NC4=CC5=C(C=C4)OCO5)O '
               'NAME: '
               '(3R,6aS,8S,10aS)-N-(1,3-benzodioxol-5-yl)-3-hydroxy-8-[2-(4-methyl-1-piperazinyl)-2-oxoethyl]-3,4,6,6a,8,9,10,10a-octahydro-2H-pyrano[2,3-c][1,5]oxazocine-1-carboxamide '
               'REASON: WRONGLY CLASSIFIED Molecule contains exactly two '
               'ketone groups.\n'
               ' * SMILES: '
               'C[C@@H]1CN([C@@H](COC2=C(C=C(C=C2)NC(=O)C3CCCCC3)C(=O)N(C[C@H]1OC)C)C)CC4=NC=CS4 '
               'NAME: '
               'N-[(4R,7R,8S)-8-methoxy-4,7,10-trimethyl-11-oxo-5-(2-thiazolylmethyl)-2-oxa-5,10-diazabicyclo[10.4.0]hexadeca-1(12),13,15-trien-14-yl]cyclohexanecarboxamide '
               'REASON: WRONGLY CLASSIFIED Molecule contains exactly two '
               'ketone groups.\n'
               ' * SMILES: O=C(O)[C@@H](N)CCC(=O)NC1=CC=C(O)C=C1 NAME: '
               'gamma-L-glutaminyl-4-hydroxybenzene REASON: WRONGLY CLASSIFIED '
               'Molecule contains exactly two ketone groups.\n'
               ' * SMILES: '
               'O1[C@@H]([C@H]([C@@H]([C@H]([C@@H]1OC[C@H](N)C(O)=O)NC(C)=O)O)O)CO '
               'NAME: 3-O-(N-acetyl-beta-D-glucosaminyl)-L-serine REASON: '
               'WRONGLY CLASSIFIED Molecule contains exactly two ketone '
               'groups.\n'
               ' * SMILES: C(=O)(C1=CC=C(C=C1)CCC(O)=O)[C@H]2CC[C@@H](CC2)CN '
               'NAME: rotraxate REASON: WRONGLY CLASSIFIED Molecule contains '
               'exactly two ketone groups.\n'
               ' * SMILES: Cc1ccc(cc1)C(=O)c1ccc(CC(O)=O)n1C NAME: tolmetin '
               'REASON: WRONGLY CLASSIFIED Molecule contains exactly two '
               'ketone groups.\n'
               ' * SMILES: '
               'CCCOC1=CC=C(C=C1)NC(=O)C2CC(=O)N=C(S2)NN=C(C)C=CC3=CC=C(C=C3)N(C)C '
               'NAME: '
               '2-[2-[4-[4-(dimethylamino)phenyl]but-3-en-2-ylidene]hydrazinyl]-4-oxo-N-(4-propoxyphenyl)-5,6-dihydro-1,3-thiazine-6-carboxamide '
               'REASON: WRONGLY CLASSIFIED Molecule contains exactly two '
               'ketone groups.\n'
               ' * SMILES: '
               'O=C1N2[C@@H]3N4C=5C=CC=CC5[C@]3(C[C@H]6[C@]4(CC[C@@H]7[C@@]6(CCCC7(C)C)C)C)C[C@H]2C(=O)N([C@H]1C(C)C)C '
               'NAME: Drimentine I REASON: WRONGLY CLASSIFIED Molecule '
               'contains exactly two ketone groups.\n'
               ' * SMILES: '
               'C[C@@H]1CN(C(=O)C2=CC=CC=C2C3=CC=CC=C3CO[C@H]1CN(C)C(=O)NC4=CC=C(C=C4)F)[C@H](C)CO '
               'NAME: LSM-8749 REASON: WRONGLY CLASSIFIED Molecule contains '
               'exactly two ketone groups.\n'
               ' * SMILES: CCOC(=O)C1=CC=C(C=C1)NC(=O)N2CCCCCC2 NAME: '
               '4-[[1-azepanyl(oxo)methyl]amino]benzoic acid ethyl ester '
               'REASON: WRONGLY CLASSIFIED Molecule contains exactly two '
               'ketone groups.\n'
               ' * SMILES: O=C1NC(C(=O)NC1C(CC)C)CC(C)C NAME: Cyclo-(Leu-Ile) '
               'REASON: WRONGLY CLASSIFIED Molecule contains exactly two '
               'ketone groups.\n'
               ' * SMILES: '
               'C[C@@H]1CN(C(=O)C2=C(C(=CC=C2)N(C)C)O[C@H]1CN(C)C(=O)NC3CCCCC3)[C@H](C)CO '
               'NAME: '
               '3-cyclohexyl-1-[[(2R,3R)-10-(dimethylamino)-5-[(2R)-1-hydroxypropan-2-yl]-3-methyl-6-oxo-3,4-dihydro-2H-1,5-benzoxazocin-2-yl]methyl]-1-methylurea '
               'REASON: WRONGLY CLASSIFIED Molecule contains exactly two '
               'ketone groups.\n'
               ' * SMILES: '
               'C[C@@H]1CN(C(=O)C2=C(N=CC(=C2)C#C[C@H](C)O)O[C@@H]1CN(C)C(=O)NC3=CC=C(C=C3)C(F)(F)F)[C@H](C)CO '
               'NAME: '
               '1-[[(2S,3R)-8-[(3S)-3-hydroxybut-1-ynyl]-5-[(2R)-1-hydroxypropan-2-yl]-3-methyl-6-oxo-3,4-dihydro-2H-pyrido[2,3-b][1,5]oxazocin-2-yl]methyl]-1-methyl-3-[4-(trifluoromethyl)phenyl]urea '
               'REASON: WRONGLY CLASSIFIED Molecule contains exactly two '
               'ketone groups.\n'
               ' * SMILES: '
               'P(OC[C@H](OC(=O)CC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)COC(=O)CCCCCCCCCCCCCCCCCC)(O)(O)=O '
               'NAME: PA(19:0/22:6(4Z,7Z,10Z,13Z,16Z,19Z)) REASON: WRONGLY '
               'CLASSIFIED Molecule contains exactly two ketone groups.\n'
               ' * SMILES: '
               'C[C@H]1CN(C(=O)C2=CC=CC=C2C3=CC=CC=C3CO[C@@H]1CN(C)C(=O)NC4=CC=CC=C4C(F)(F)F)[C@@H](C)CO '
               'NAME: LSM-10338 REASON: WRONGLY CLASSIFIED Molecule contains '
               'exactly two ketone groups.\n'
               ' * SMILES: O=C1C(CC=C(C)C)(CC=C(C)C)C(=O)C(O)=C1O NAME: '
               'Hulupinic acid REASON: WRONGLY CLASSIFIED Molecule contains '
               'exactly two ketone groups.\n'
               ' * SMILES: '
               '[H][C@]1(OC(O)(C[C@H](O)[C@H]1NC(C)=O)C(N)=O)[C@H](O)[C@H](O)CO '
               'NAME: N-acetylneuraminamide REASON: WRONGLY CLASSIFIED '
               'Molecule contains exactly two ketone groups.\n'
               ' * SMILES: '
               'O([C@H]1[C@H](O[C@@H]2O[C@H]([C@@H](O)[C@@H](O)[C@@H]2O)C)[C@@H](NC(=O)C)[C@@H](O[C@@H]1CO)O)[C@@H]3O[C@@H]([C@@H](O[C@@H]4O[C@@H]([C@@H](O)[C@H](O)[C@@H]4O[C@@H]5O[C@@H]([C@H](O)[C@H]5O)CO)CO[C@H]6O[C@@H]([C@@H](O)[C@H](O[C@H]7O[C@@H]([C@@H](O)[C@H](O)[C@@H]7O)CO)[C@@H]6O)CO)[C@H](O)[C@H]3NC(=O)C)CO '
               'NAME: '
               'N-[(2S,3R,4R,5S,6R)-2-[(2R,3S,4R,5R,6R)-5-Acetamido-6-hydroxy-2-(hydroxymethyl)-4-[(2S,3S,4R,5S,6S)-3,4,5-trihydroxy-6-methyloxan-2-yl]oxyoxan-3-yl]oxy-5-[(2S,3S,4S,5S,6R)-3-[(2S,3R,4R,5R)-3,4-dihydroxy-5-(hydroxymethyl)oxolan-2-yl]oxy-6-[[(2S,3S,4S,5R,6R)-3,5-dihydroxy-6-(hydroxymethyl)-4-[(2R,3S,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxymethyl]-4,5-dihydroxyoxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-3-yl]acetamide '
               'REASON: WRONGLY CLASSIFIED Molecule contains exactly two '
               'ketone groups.\n'
               ' * SMILES: '
               'CC(=O)NC1C(O)C(OC2OC(CO)C(O)C(OC3OC(CO)C(O)C(OC4OC(CO)C(O)C(O)C4O)C3NC(C)=O)C2O)C(CO)OC1OC1C(O)C(CO)OC(OC2C(O)C(O)C(O)OC2CO)C1O '
               'NAME: '
               'beta-D-galactopyranosyl-(1->3)-2-acetamido-2-deoxy-beta-D-glucopyranosyl-(1->3)-beta-D-galactopyranosyl-(1->4)-2-acetamido-2-deoxy-beta-D-glucopyranosyl-(1->3)-beta-D-galactopyranosyl-(1->4)-D-glucopyranose '
               'REASON: WRONGLY CLASSIFIED Molecule contains exactly two '
               'ketone groups.\n'
               ' * SMILES: '
               'CCCN(C)C[C@H]1[C@H](CN(C(=O)C2=C(C=CC(=C2)NC(=O)NC3=CC=C(C=C3)F)O[C@H](CCCCO1)C)[C@H](C)CO)C '
               'NAME: '
               '1-(4-fluorophenyl)-3-[(3S,9R,10S)-12-[(2R)-1-hydroxypropan-2-yl]-3,10-dimethyl-9-[[methyl(propyl)amino]methyl]-13-oxo-2,8-dioxa-12-azabicyclo[12.4.0]octadeca-1(14),15,17-trien-16-yl]urea '
               'REASON: WRONGLY CLASSIFIED Molecule contains exactly two '
               'ketone groups.\n'
               ' * SMILES: '
               'C1CCN(CC1)CCC(=O)NCC[C@@H]2CC[C@@H]([C@H](O2)CO)NC(=O)C3CCOCC3 '
               'NAME: '
               'N-[(2S,3S,6S)-2-(hydroxymethyl)-6-[2-[[1-oxo-3-(1-piperidinyl)propyl]amino]ethyl]-3-oxanyl]-4-oxanecarboxamide '
               'REASON: WRONGLY CLASSIFIED Molecule contains exactly two '
               'ketone groups.\n'
               ' * SMILES: '
               'O([C@@H]1[C@@H](O)[C@H](O)[C@H](O[C@H]1OC=2C=C3C(O[C@@H]4O[C@@H]([C@@H](O)[C@H](O)[C@H]4O)CO)=CC(O)=CC3=[O+]C2C5=CC(OC)=C(O)C=C5)COC(=O)C=CC6=CC(O)=C(O)C=C6)[C@@H]7O[C@@H]([C@@H](O)[C@H](O)[C@H]7O)COC(=O)C=CC8=CC(OC)=C(O)C=C8 '
               'NAME: Peonidin-3-caffeoyl-feruloyl sophoroside-5-glucoside '
               'REASON: WRONGLY CLASSIFIED Molecule contains exactly two '
               'ketone groups.\n'
               ' * SMILES: [NH3+]CC[C@@H](O)[C@H](N1CCC1=O)C([O-])=O NAME: '
               'proclavaminic acid zwitterion REASON: WRONGLY CLASSIFIED '
               'Molecule contains exactly two ketone groups.\n'
               ' * SMILES: CC(=O)N[C@@H]1[C@@H](O)[C@H](O)[C@@H](CO)OC1=O '
               'NAME: N-acetyl-D-glucosamino-1,5-lactone REASON: WRONGLY '
               'CLASSIFIED Molecule contains exactly two ketone groups.\n'
               'False negatives: SMILES: Nc1ccccc1C(=O)CC(=O)C(O)=O NAME: '
               '4-(2-aminophenyl)-2,4-dioxobutanoic acid REASON: MISSED '
               'Molecule contains 3 ketone group(s), requires exactly two.\n'
               ' * SMILES: '
               'COC(=O)[C@@]12C(=C)[C@@](C)(C[C@@H]3[C@]1(C)CC=C1C(C)(C)C(=O)C[C@@H](O)[C@@]31C)C(=O)[C@](C)(O)C2=O '
               'NAME: berkeleytrione REASON: MISSED Molecule contains 4 ketone '
               'group(s), requires exactly two.\n'
               ' * SMILES: OC(=O)C(=O)CC(=O)C(O)=O NAME: 2,4-dioxopentanedioic '
               'acid REASON: MISSED Molecule contains 4 ketone group(s), '
               'requires exactly two.\n'
               ' * SMILES: OC[C@H](O)[C@@H](O)C(=O)C(=O)C(O)=O NAME: '
               '2,3-diketogulonic acid REASON: MISSED Molecule contains 3 '
               'ketone group(s), requires exactly two.\n'
               ' * SMILES: '
               'O=C1N([C@@H]([C@H](O)C)C(C1C(=O)[C@@]2([C@@H]3[C@@H](C=C[C@@H]2C)C[C@@H](C)CC3)C)=O)C '
               'NAME: Cryptocin REASON: MISSED Molecule contains 3 ketone '
               'group(s), requires exactly two.\n'
               ' * SMILES: CC(=O)CC(=O)CCc1ccc(NC(=O)CCCC(O)=O)cc1 NAME: '
               '4-[4-(3,5-dioxohexyl)phenylcarbamoyl]butyric acid REASON: '
               'MISSED Molecule contains 4 ketone group(s), requires exactly '
               'two.\n'
               ' * SMILES: OC1C(C(=O)C(C1=O)C(=O)C(CC)C)CC=C(C)C NAME: '
               'Adhumulinic acid REASON: MISSED Molecule contains 3 ketone '
               'group(s), requires exactly two.\n'
               ' * SMILES: '
               'COC(=O)[C@@]12C(=C)[C@@](C)(C[C@H]3[C@]4(C)CC[C@@H](O)C(C)(C)[C@H]4CC[C@]13C)C(=O)[C@](C)(O)C2=O '
               'NAME: berkeleyone A REASON: MISSED Molecule contains 3 ketone '
               'group(s), requires exactly two.\n'
               ' * SMILES: C1(C(=O)C(=O)C(C(=O)C1=O)O)O NAME: '
               '3,6-dihydroxycyclohexane-1,2,4,5-tetrone REASON: MISSED '
               'Molecule contains 4 ketone group(s), requires exactly two.\n'
               ' * SMILES: '
               'O=C1[C@@](O)([C@@H]2[C@H]3C(=O)CC[C@@H]2[C@H]([C@@]1(C3=O)C)C)C '
               'NAME: Penicillone A REASON: MISSED Molecule contains 3 ketone '
               'group(s), requires exactly two.\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'CCN1N=C(N=N1)C2=CC=CC=C2NC(=O)C3=CC=C(C=C3)N4C=NN=N4',
                                     'name': 'N-[2-(2-ethyl-5-tetrazolyl)phenyl]-4-(1-tetrazolyl)benzamide',
                                     'reason': 'Molecule contains 0 ketone '
                                               'group(s), requires exactly '
                                               'two.'},
                                 {   'smiles': 'CCS(=O)(=O)N1CC2(C1)[C@@H]([C@@H](N2C(=O)C3CCCC3)CO)C4=CC=C(C=C4)C=CC',
                                     'name': 'LSM-38092',
                                     'reason': 'Molecule contains 0 ketone '
                                               'group(s), requires exactly '
                                               'two.'},
                                 {   'smiles': 'O=C/1N/C(/C(=O)N\\C1=C\\C2=CC=CC=C2)=C\\C=3N=CNC3C(C=C)(C)C',
                                     'name': 'DeltaPLH',
                                     'reason': 'Molecule contains 0 ketone '
                                               'group(s), requires exactly '
                                               'two.'},
                                 {   'smiles': 'C1CCN(CC1)C(=O)C[C@H]2C[C@@H]3[C@H]([C@@H](O2)CO)OC4=C3C=C(C=C4)NC(=O)CC5CC5',
                                     'name': 'N-[(1S,3R,4aS,9aR)-1-(hydroxymethyl)-3-[2-oxo-2-(1-piperidinyl)ethyl]-3,4,4a,9a-tetrahydro-1H-pyrano[3,4-b]benzofuran-6-yl]-2-cyclopropylacetamide',
                                     'reason': 'Molecule contains 0 ketone '
                                               'group(s), requires exactly '
                                               'two.'},
                                 {   'smiles': 'C[C@H]1C[C@@]2(OC(=O)c3ccccc3)[C@H]([C@H]1OC(C)=O)[C@@H](O)\\C(C)=C/C[C@H]1[C@@H](\\C=C(C)\\C2=O)C1(C)C',
                                     'name': '(-)-(6Z,12E,2S,3S,4R,5R,9S,11S,15R)-3-acetoxy-15-benzoyloxylathyra-6,12-dien-5-ol-14-one',
                                     'reason': 'Molecule contains 0 ketone '
                                               'group(s), requires exactly '
                                               'two.'},
                                 {   'smiles': 'O=C1C(O)=CC=2O[C@]3([C@H](O)C[C@@H]4[C@](OC=5C=C(O)C(C=C(C5C4)C)=O)(CC=CC(C[C@H]3CC2C(=C1)C)(C)C)C)C',
                                     'name': 'Eupenifeldin',
                                     'reason': 'Molecule contains 0 ketone '
                                               'group(s), requires exactly '
                                               'two.'},
                                 {   'smiles': 'O1[C@@H](O[C@@H]2[C@@H](OC[C@H]3O[C@@H](O[C@H]4[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]4CO)O[C@H]5[C@H](O)[C@@H](NC(=O)C)C(O[C@@H]5CO[C@@H]6O[C@H]([C@@H](O)[C@@H](O)[C@@H]6O)C)O)[C@@H](O)[C@@H](O[C@H]7O[C@@H]([C@@H](O)[C@H](O)[C@@H]7O[C@@H]8O[C@@H]([C@@H](O[C@@H]9O[C@@H]([C@H](O)[C@H](O)[C@H]9NC(=O)C)CO)[C@H](O)[C@H]8NC(=O)C)CO)CO)[C@@H]3O)O[C@@H]([C@@H](O)[C@@H]2O)CO)[C@H](NC(=O)C)[C@@H](O[C@@H]%10O[C@H]([C@@H](O)[C@@H](O)[C@@H]%10O)C)[C@H](O[C@@H]%11O[C@@H]([C@H](O)[C@H](O)[C@H]%11NC(=O)C)CO)[C@H]1CO',
                                     'name': 'N-[(3R,4R,5S,6R)-5-[(2S,3R,4R,5S,6R)-3-Acetamido-5-[(2S,3S,4S,5R,6R)-4-[(2R,3S,4S,5S,6R)-3-[(2S,3R,4R,5S,6R)-3-acetamido-5-[(2S,3R,4R,5R,6R)-3-acetamido-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-6-[[(2S,3S,4S,5S,6R)-3-[(2S,3R,4R,5S,6R)-3-acetamido-5-[(2S,3R,4R,5R,6R)-3-acetamido-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-6-(hydroxymethyl)-4-[(2R,3S,4R,5S,6S)-3,4,5-trihydroxy-6-methyloxan-2-yl]oxyoxan-2-yl]oxy-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxymethyl]-3,5-dihydroxyoxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-2,4-dihydroxy-6-[[(2R,3S,4R,5S,6S)-3,4,5-trihydroxy-6-methyloxan-2-yl]oxymethyl]oxan-3-yl]acetamide',
                                     'reason': 'Molecule contains 0 ketone '
                                               'group(s), requires exactly '
                                               'two.'},
                                 {   'smiles': 'CN1C[C@@H]2C[C@H](Cn3c2cccc3=O)[C@H]1CC=C',
                                     'name': 'Tinctorine',
                                     'reason': 'Molecule contains 0 ketone '
                                               'group(s), requires exactly '
                                               'two.'},
                                 {   'smiles': 'CCC1=C2COC(CC2=C3C(=C(OC3=N1)C(=O)C4=CC=CC=C4)N)(C)C',
                                     'name': 'LSM-4563',
                                     'reason': 'Molecule contains 0 ketone '
                                               'group(s), requires exactly '
                                               'two.'},
                                 {   'smiles': 'CN1CCN(CC1)C(=O)C[C@@H]2CC[C@H]3[C@H](O2)COC[C@@H](CN3C(=O)NC4=CC5=C(C=C4)OCO5)O',
                                     'name': '(3R,6aS,8S,10aS)-N-(1,3-benzodioxol-5-yl)-3-hydroxy-8-[2-(4-methyl-1-piperazinyl)-2-oxoethyl]-3,4,6,6a,8,9,10,10a-octahydro-2H-pyrano[2,3-c][1,5]oxazocine-1-carboxamide',
                                     'reason': 'Molecule contains 0 ketone '
                                               'group(s), requires exactly '
                                               'two.'}],
    'sample_false_negatives': [   {   'smiles': 'Nc1ccccc1C(=O)CC(=O)C(O)=O',
                                      'name': '4-(2-aminophenyl)-2,4-dioxobutanoic '
                                              'acid',
                                      'reason': 'Molecule contains 0 ketone '
                                                'group(s), requires exactly '
                                                'two.'},
                                  {   'smiles': 'C1C([C@H](C([C@]2([H])[C@]1(C)[C@@]3(C(C=C([C@H]([C@]3(CC2)[H])C)C=C)=O)[H])(C)C)O)=O',
                                      'name': '(+)-phytocassane D',
                                      'reason': 'Molecule contains 1 ketone '
                                                'group(s), requires exactly '
                                                'two.'},
                                  {   'smiles': 'O=C(C(C)C)C(=O)C',
                                      'name': '4-Methyl-2,3-pentanedione',
                                      'reason': 'Molecule contains 0 ketone '
                                                'group(s), requires exactly '
                                                'two.'},
                                  {   'smiles': '[H][C@]12N(C)C3=C(C=C(Cl)C(OC)=C3OC)[C@@]1(O)[C@@H](O)[C@@]13SS[C@@](C)(N(C)C1=O)C(=O)N23',
                                      'name': 'sporidesmin A',
                                      'reason': 'Molecule contains 0 ketone '
                                                'group(s), requires exactly '
                                                'two.'},
                                  {   'smiles': 'COC(=O)[C@@]12C(=C)[C@@](C)(C[C@@H]3[C@]1(C)CC=C1C(C)(C)C(=O)C[C@@H](O)[C@@]31C)C(=O)[C@](C)(O)C2=O',
                                      'name': 'berkeleytrione',
                                      'reason': 'Molecule contains 3 ketone '
                                                'group(s), requires exactly '
                                                'two.'},
                                  {   'smiles': 'CC1(C)C(=O)C(=O)c2c1[nH]c1cc(O)ccc21',
                                      'name': 'bruceolline H',
                                      'reason': 'Molecule contains 0 ketone '
                                                'group(s), requires exactly '
                                                'two.'},
                                  {   'smiles': 'CC(C)[C@H]1OC(=O)[C@H](Cc2ccccc2)N(C)C1=O',
                                      'name': 'bassiatin',
                                      'reason': 'Molecule contains 0 ketone '
                                                'group(s), requires exactly '
                                                'two.'},
                                  {   'smiles': 'OC(=O)C(=O)CC(=O)C(O)=O',
                                      'name': '2,4-dioxopentanedioic acid',
                                      'reason': 'Molecule contains 0 ketone '
                                                'group(s), requires exactly '
                                                'two.'},
                                  {   'smiles': 'COc1ccc(cc1)C1C(=O)c2ccccc2C1=O',
                                      'name': 'anisindione',
                                      'reason': 'Molecule contains 0 ketone '
                                                'group(s), requires exactly '
                                                'two.'},
                                  {   'smiles': 'OC[C@H](O)[C@@H](O)C(=O)C(=O)C(O)=O',
                                      'name': '2,3-diketogulonic acid',
                                      'reason': 'Molecule contains 0 ketone '
                                                'group(s), requires exactly '
                                                'two.'}],
    'attempt': 1,
    'reasoning': "Okay, let's analyze the previous attempt and the provided "
                 'outcomes to figure out how to improve the `is_diketone` '
                 'function.\n'
                 '\n'
                 '**Analysis of the Previous Attempt**\n'
                 '\n'
                 'The previous code was quite simple: it parsed the SMILES '
                 'string, created a SMARTS pattern for a ketone group ("C=O"), '
                 'and counted how many times this pattern appeared in the '
                 'molecule. If the count was exactly 2, it classified the '
                 'molecule as a diketone.\n'
                 '\n'
                 '**Issues Identified from the Outcomes**\n'
                 '\n'
                 '1.  **False Positives:** The major issue is that a lot of '
                 "molecules were classified as diketones when they shouldn't "
                 'have been. The False positives list contains molecules '
                 'containing more than two carbonyl groups, but not '
                 'necessarily ketone groups.  For example, amides (-C(=O)N-) , '
                 'esters (-C(=O)O-) and other functionalities where one carbon '
                 'is double bonded to an oxygen are being misclassified.\n'
                 '\n'
                 '2.  **False Negatives:** Some molecules containing 2 ketone '
                 'groups are misclassified because they contain more than 2 '
                 'carbonyl groups in total.  This means the logic to count the '
                 'C=O patterns was too simple and not specific enough.  The '
                 'molecule must contains exactly two *ketone* '
                 'functionalities.\n'
                 '\n'
                 '**Hypothesized Improvements**\n'
                 '\n'
                 'To address the false positives and false negatives, we need '
                 'to refine the SMARTS pattern and the logic:\n'
                 '\n'
                 '1.  **More Specific SMARTS for Ketones:**  The previous '
                 'SMARTS `"C=O"` is too general because it matches aldehydes, '
                 'esters, amides, carboxylic acids etc. We need to be more '
                 'specific and look for a carbon double bonded to an oxygen, '
                 'where the carbon is also bonded to two other carbons which '
                 'can be in a ring. The SMARTS for this would be: '
                 '`[CX3](=[OX1])([CX4])([CX4])`\n'
                 '\n'
                 '2.  **Count based on the new pattern:** We should use the '
                 'new SMARTS pattern to count how many ketone groups are '
                 'present in the molecule.\n'
                 '3.  **Handle Errors**: Return appropriate error messages '
                 'when the SMILES string is not valid.\n'
                 '\n'
                 '**Revised Code**\n'
                 '\n'
                 'Based on these points, here is the revised code.',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 73,
    'num_false_positives': 706,
    'num_true_negatives': 141439,
    'num_false_negatives': 82,
    'num_negatives': None,
    'precision': 0.09370988446726572,
    'recall': 0.47096774193548385,
    'f1': 0.15631691648822268,
    'accuracy': 0.9944624033731553,
    'negative_predictive_value': 0.9994205806912049}