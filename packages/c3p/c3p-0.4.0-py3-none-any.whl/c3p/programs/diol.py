"""
Classifies: CHEBI:23824 diol
"""
"""
Classifies: CHEBI:23824 diol
"""
from rdkit import Chem

def is_diol(smiles: str):
    """
    Determines if a molecule is a diol based on its SMILES string.
    A diol is a compound that contains two hydroxy groups, generally assumed to be, but not necessarily, alcoholic.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a diol, False otherwise
        str: Reason for classification
    """
    
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Define a SMARTS pattern for hydroxyl groups (-OH) that are not part of carboxylic acids or sulfonic acids
    hydroxyl_pattern = Chem.MolFromSmarts("[OX2H;!$(O[C,S]=O)]")
    
    # Find all matches for the hydroxyl pattern
    hydroxyl_matches = mol.GetSubstructMatches(hydroxyl_pattern)
    
    # Count the number of hydroxyl groups
    hydroxyl_count = len(hydroxyl_matches)

    # Check if there are exactly two hydroxyl groups
    if hydroxyl_count == 2:
        return True, "Contains exactly two hydroxyl groups"
    else:
        return False, f"Contains {hydroxyl_count} hydroxyl groups, need exactly 2"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:23824',
                          'name': 'diol',
                          'definition': 'A compound that contains two hydroxy '
                                        'groups, generally assumed to be, but '
                                        'not necessarily, alcoholic. Aliphatic '
                                        'diols are also called glycols.',
                          'parents': ['CHEBI:26191'],
                          'xrefs': ['Wikipedia:Diol'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 24,
                           'log_lines_of_code': 3.1780538303479458,
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
                                                 2,
                                                 1,
                                                 2],
                           'max_indent': 2,
                           'imports': ['from rdkit import Chem'],
                           'imports_count': 1,
                           'methods_called': [   'GetSubstructMatches',
                                                 'MolFromSmiles',
                                                 'MolFromSmarts'],
                           'methods_called_count': 3,
                           'smarts_strings': ['[OX2H;!$(O[C,S]=O)]'],
                           'smarts_strings_count': 1,
                           'defs': ['is_diol(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'True, "Contains exactly two '
                                          'hydroxyl groups"',
                                          'False, f"Contains {hydroxyl_count} '
                                          'hydroxyl groups, need exactly 2"'],
                           'returns_count': 3,
                           'complexity': 2.435610766069589},
    'message': '\n'
               'Attempt failed: F1 score of 0.7839805825242718 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: '
               '[H][C@@]1(CNc2[nH]c(N)nc(=O)c2N1)[C@H](O)[C@H](C)O NAME: '
               '(6R)-L-threo-tetrahydrobiopterin REASON: CORRECT Contains '
               'exactly two hydroxyl groups\n'
               ' * SMILES: '
               'CC(=C)[C@@H]1CC[C@]2(C)CC[C@]3(C)[C@H](CC[C@@H]4[C@@]5(C)[C@H](O)C[C@H](O)C(C)(C)[C@@H]5CC[C@@]34C)[C@@H]12 '
               'NAME: 20(29)-lupene-1beta,3beta-diol REASON: CORRECT Contains '
               'exactly two hydroxyl groups\n'
               ' * SMILES: O1C[C@@H](O)[C@H](O)C1=O NAME: D-threonolactone '
               'REASON: CORRECT Contains exactly two hydroxyl groups\n'
               ' * SMILES: OC1C(O)C(=CC=C1Cl)C(c1ccc(Cl)cc1)C(Cl)(Cl)Cl NAME: '
               'DDT-2,3-dihydrodiol REASON: CORRECT Contains exactly two '
               'hydroxyl groups\n'
               ' * SMILES: '
               '[H][C@]12[C@@H]3CC[C@@]4(C)[C@H](O)C[C@@H](O)[C@H](C)[C@@]34C[C@@]1(C)CCC2(C)C '
               'NAME: conidiogenol REASON: CORRECT Contains exactly two '
               'hydroxyl groups\n'
               ' * SMILES: CCCCCCCCCCC(O)CCCO NAME: 1,4-tetradecanediol '
               'REASON: CORRECT Contains exactly two hydroxyl groups\n'
               ' * SMILES: CC(O)CCCCCCCCCCO NAME: 1,11-dodecanediol REASON: '
               'CORRECT Contains exactly two hydroxyl groups\n'
               ' * SMILES: '
               'C=1(C(C(C(C(C(C)C)=O)=C(C1CC=C(C)C)O)=O)(CC=C(C)C)CC=C(C)C)O '
               'NAME: colupulone REASON: CORRECT Contains exactly two hydroxyl '
               'groups\n'
               ' * SMILES: O[C@H]1Cc2ccccc2C[C@H]1O NAME: '
               'cis-1,2,3,4-tetrahydronaphthalene-2,3-diol REASON: CORRECT '
               'Contains exactly two hydroxyl groups\n'
               ' * SMILES: CC(O)CCCCCCCCO NAME: 1,9-decanediol REASON: CORRECT '
               'Contains exactly two hydroxyl groups\n'
               ' * SMILES: C\\C=C\\C=C\\C1=CC2=C(CO1)C(=O)[C@](C)(O)[C@H](O)C2 '
               'NAME: harziphilone REASON: CORRECT Contains exactly two '
               'hydroxyl groups\n'
               ' * SMILES: '
               'O[C@H](\\C=C\\CCCCCCCCC\\C=C/CCCC\\C=C/CCCCCCC\\C=C\\[C@@H](O)C#C)C#C '
               'NAME: (-)-duryne D REASON: CORRECT Contains exactly two '
               'hydroxyl groups\n'
               ' * SMILES: '
               '[H][C@@]12CCC(=O)[C@H](C)[C@@]1(C)CC[C@@]1([H])[C@@]2(C)CC[C@@]2(C)[C@]3([H])CC(C)(C)CC[C@]3(CO)[C@H](O)C[C@]12C '
               'NAME: celasdin B REASON: CORRECT Contains exactly two hydroxyl '
               'groups\n'
               ' * SMILES: OCCCCCCCCCCCCO NAME: 1,12-dodecanediol REASON: '
               'CORRECT Contains exactly two hydroxyl groups\n'
               ' * SMILES: C\\C=C\\C=C\\C=C\\C(=O)C(C)[C@@H](O)CCO NAME: '
               'lavendiol REASON: CORRECT Contains exactly two hydroxyl '
               'groups\n'
               ' * SMILES: [H][C@]12CC=C(CO)CC[C@]1(C)CC[C@H]2C(C)(C)O NAME: '
               'schisanwilsonene A REASON: CORRECT Contains exactly two '
               'hydroxyl groups\n'
               ' * SMILES: O[C@@H]1COC(=O)[C@@H]1O NAME: erythrono-1,4-lactone '
               'REASON: CORRECT Contains exactly two hydroxyl groups\n'
               ' * SMILES: O[C@@H]1CCCC[C@H]1O NAME: '
               'trans-cyclohexane-1,2-diol REASON: CORRECT Contains exactly '
               'two hydroxyl groups\n'
               ' * SMILES: '
               '[H][C@]12CC(=C)[C@H](O)CC\\C(C)=C\\[C@@H](O)[C@]1([H])C(=C)C(=O)O2 '
               'NAME: tatridin B REASON: CORRECT Contains exactly two hydroxyl '
               'groups\n'
               ' * SMILES: [H]C(CCCCCCCCCCCCC)=C([H])[C@H](O)[C@H](N)CO NAME: '
               '(2R,3S)-2-aminooctadec-4-ene-1,3-diol REASON: CORRECT Contains '
               'exactly two hydroxyl groups\n'
               ' * SMILES: '
               'C=1C(OC2=C(C1)C=C([C@@H](OCC)[C@@H](O)C(O)(C)C)C(=C2)OC)=O '
               'NAME: angelol-J REASON: CORRECT Contains exactly two hydroxyl '
               'groups\n'
               ' * SMILES: OCC(CO)O[N+]([O-])=O NAME: 2-mononitroglycerol '
               'REASON: CORRECT Contains exactly two hydroxyl groups\n'
               ' * SMILES: '
               '[C@]123[C@]4([C@@]([C@@H]5[C@H](C(O)(C)C)[C@H]([C@]4(OC1=O)[H])OC5=O)(O)C[C@]2(O3)[H])C '
               'NAME: picrotin REASON: CORRECT Contains exactly two hydroxyl '
               'groups\n'
               ' * SMILES: CC1=CC=C2C=CC(O)C(O)C2=C1 NAME: '
               '7-methyl-1,2-dihydronaphthalene-1,2-diol REASON: CORRECT '
               'Contains exactly two hydroxyl groups\n'
               ' * SMILES: [H]C(CCCCCCCCCCCCC)=C([H])[C@@H](O)[C@@H](N)CO '
               'NAME: sphing-4-enine REASON: CORRECT Contains exactly two '
               'hydroxyl groups\n'
               'False positives: SMILES: '
               'CC\\C=C/C\\C=C/C\\C=C/C\\C=C/C\\C=C/CCCC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)N1C=NC2=C1N=CN=C2N '
               'NAME: (5Z,8Z,11Z,14Z,17Z)-icosapentaenoyl-CoA(4-) REASON: '
               'WRONGLY CLASSIFIED Contains exactly two hydroxyl groups\n'
               ' * SMILES: O=C1N(C(CC1)C(O)=O)CCC(N)C(O)=O NAME: '
               "(2S,3'S)-alpha-Amino-2-carboxy-5-oxo-1-pyrrolidinebutanoic "
               'acid REASON: WRONGLY CLASSIFIED Contains exactly two hydroxyl '
               'groups\n'
               ' * SMILES: CC(=O)[C@@H](O)[C@H](O)CC(=O)C([O-])=O NAME: '
               '3,7-dideoxy-D-threo-hepto-2,6-diuolosonate REASON: WRONGLY '
               'CLASSIFIED Contains exactly two hydroxyl groups\n'
               ' * SMILES: OC(=O)\\C=C\\C(=C\\C=C\\C=C(/C)\\C=C\\C(O)=O)\\C '
               'NAME: Mycorradicin REASON: WRONGLY CLASSIFIED Contains exactly '
               'two hydroxyl groups\n'
               ' * SMILES: O=C1C=C[C@@H]([C@]1(O)C(O)CCCCCCCCCCCCCC)OC(=O)C '
               'NAME: 4-O-acetyl hygrophorone A14 REASON: WRONGLY CLASSIFIED '
               'Contains exactly two hydroxyl groups\n'
               ' * SMILES: '
               'O=C1OC(C(NC(=O)C(NC(=O)C)CC(C)C)C(=O)NC(C(=O)NC2CCC(N(C(C(N(C(C(NC1C(C)C)=O)CC3=CC=C(O)C=C3)C)=O)CC4=CC=CC=C4)C2=O)O)CCCCN)C '
               'NAME: Cyanopeptolin 920 REASON: WRONGLY CLASSIFIED Contains '
               'exactly two hydroxyl groups\n'
               ' * SMILES: '
               'P(OC[C@H](OC(=O)CCCCCCCCCCCCCCCCCCCC)COC(=O)CCCCCCC/C=C\\C/C=C\\C/C=C\\CC)(OC[C@H](N)C(O)=O)(O)=O '
               'NAME: PS(18:3(9Z,12Z,15Z)/21:0) REASON: WRONGLY CLASSIFIED '
               'Contains exactly two hydroxyl groups\n'
               ' * SMILES: S(=O)(=O)(OC1=CC(O)=CC(=C1)CCCCCCCCCC[C@H](CCC)C)O '
               'NAME: Panosialin wD REASON: WRONGLY CLASSIFIED Contains '
               'exactly two hydroxyl groups\n'
               ' * SMILES: '
               'S1C(=NC(=C1)/C=C(/C2OC(=O)C[C@H](O)C(C(=O)[C@@H]([C@@H](O)[C@H](C(C=CC(=CC2)C)=O)C)C)(C)C)\\C)C '
               'NAME: 9-Keto-10,11-didehydroepothilone D REASON: WRONGLY '
               'CLASSIFIED Contains exactly two hydroxyl groups\n'
               ' * SMILES: '
               'O=C(N[C@@H](CC(=O)N)C(O)=O)[C@@H](NC(=O)[C@@H](N)CC(O)=O)CCC(=O)N '
               'NAME: Asp-Gln-Asn REASON: WRONGLY CLASSIFIED Contains exactly '
               'two hydroxyl groups\n'
               ' * SMILES: '
               'O=C1NC2=C(C(O)=C(/C=C/C3(OC(C(=C)C)CC3)C)C=C2)[C@]([C@H]1OC)(O)C4=CC=C(OC)C=C4 '
               'NAME: Yaequinolone F REASON: WRONGLY CLASSIFIED Contains '
               'exactly two hydroxyl groups\n'
               ' * SMILES: '
               'CC(=O)N[C@@H](Cc1ccc(O)c(c1)\\N=N\\c1ccccc1)C(=O)NCC(=O)NCC(O)=O '
               'NAME: 3-(phenyldiazenyl)-AcTyrGlyGly REASON: WRONGLY '
               'CLASSIFIED Contains exactly two hydroxyl groups\n'
               ' * SMILES: '
               'CCCCC\\C=C/C\\C=C/CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12 '
               'NAME: (3Z,6Z)-dodecadienoyl-CoA(4-) REASON: WRONGLY CLASSIFIED '
               'Contains exactly two hydroxyl groups\n'
               ' * SMILES: '
               'O=C1NC2=C3C(=O)C(O)=C([C@]3(CC[C@]4(C2=C1[C@@H](O)CC4)C)C)C(C)C '
               'NAME: Radianspene K REASON: WRONGLY CLASSIFIED Contains '
               'exactly two hydroxyl groups\n'
               ' * SMILES: '
               'O=C(NCCC1=CC(O)=C(O)C=C1)CCC/C=C/C/C=C/C\\C=C\\C\\C=C\\CCCCC '
               'NAME: '
               'N-[2-(3,4-Dihydroxyphenyl)ethyl]icosa-5,8,11,14-tetraenamide '
               'REASON: WRONGLY CLASSIFIED Contains exactly two hydroxyl '
               'groups\n'
               ' * SMILES: '
               'O=C1OC2=C(C(=CC(=C2C)O)C)OC3=C1C(=CC(=C3COCCC4=CC=CC=C4)O)C '
               'NAME: Simplicildone J REASON: WRONGLY CLASSIFIED Contains '
               'exactly two hydroxyl groups\n'
               ' * SMILES: CC[C@@H]1c2ccc(O)cc2C(C)=C1c1ccc(O)cc1 NAME: '
               '(R)-Indenestrol B REASON: WRONGLY CLASSIFIED Contains exactly '
               'two hydroxyl groups\n'
               ' * SMILES: '
               'O=C1O[C@](OC)(C2=C(O)C=CC(=C2)O)C=C1CC/C=C(/CCC(=O)C(C)C)\\C '
               'NAME: Australeol C REASON: WRONGLY CLASSIFIED Contains exactly '
               'two hydroxyl groups\n'
               ' * SMILES: C[C@H](N)C(=O)N[C@@H](CCC(O)=O)C(O)=O NAME: '
               'L-alanyl-L-glutamic acid REASON: WRONGLY CLASSIFIED Contains '
               'exactly two hydroxyl groups\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCC(=O)OC[C@H](COP(O)(=O)OC[C@H](N)C(O)=O)OC(=O)CCCCCCCCCCCCCCC '
               'NAME: 1,2-dihexadecanoyl-sn-glycero-3-phosphoserine REASON: '
               'WRONGLY CLASSIFIED Contains exactly two hydroxyl groups\n'
               ' * SMILES: '
               'P(OC[C@H](OC(=O)CCCCCCC/C=C\\CCCC)COC(=O)CCCCCCC/C=C\\CCCC)(O)(O)=O '
               'NAME: pa(14:1(9z)/14:1(9z)) REASON: WRONGLY CLASSIFIED '
               'Contains exactly two hydroxyl groups\n'
               ' * SMILES: '
               'FC(F)(CC(C1C2(C(CC1)/C(/CCC2)=C\\C=C/3\\CC(O)CCC3=C)C)C)CC(O)(C)C '
               'NAME: 23,23-difluoro-25-hydroxyvitamin D3 REASON: WRONGLY '
               'CLASSIFIED Contains exactly two hydroxyl groups\n'
               ' * SMILES: '
               'C(=C/[C@H](COC1=CC=CC=C1)O)\\[C@@H]2[C@@H](C/C=C\\CCCC(NS(C)(=O)=O)=O)C(C[C@H]2O)=O '
               'NAME: sulprostone REASON: WRONGLY CLASSIFIED Contains exactly '
               'two hydroxyl groups\n'
               ' * SMILES: OCCN(CCO)CCS([O-])(=O)=O NAME: '
               '2-[bis(2-hydroxyethyl)amino]ethanesulfonate REASON: WRONGLY '
               'CLASSIFIED Contains exactly two hydroxyl groups\n'
               ' * SMILES: [H]C(CC(O)=O)=CC(O)=O NAME: glutaconic acid REASON: '
               'WRONGLY CLASSIFIED Contains exactly two hydroxyl groups\n'
               'False negatives: SMILES: '
               'OCC(CO)OC(CCC/C=C/1\\O[C@]2(C[C@H]([C@@H]([C@]2(C1)[H])/C=C/[C@H](CCCCC)O)O)[H])=O '
               'NAME: prostaglandin I2 2-glyceryl ester REASON: MISSED '
               'Contains 4 hydroxyl groups, need exactly 2\n'
               ' * SMILES: O[C@H]1C=CC=C(/C=C/C(O)=O)[C@H]1O NAME: '
               '(E)-3-[(5S,6R)-5,6-dihydroxycyclohexa-1,3-dienyl]acrylic acid '
               'REASON: MISSED Contains 3 hydroxyl groups, need exactly 2\n'
               ' * SMILES: '
               '[H][C@@]1(CO[C@@H](O[C@@]2([H])CC[C@@]3(C)[C@@]([H])(CC[C@]4(C)[C@]3([H])CC[C@@]35O[C@@H](O)[C@]6([C@H](O)C[C@@]43C)[C@H](CC(C)(C)C[C@@]56[H])OC(=O)CCCCC)C2(C)C)[C@H](O[C@]2([H])O[C@H](CO)[C@@H](O)[C@H](O)[C@H]2O)[C@H]1O)O[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O[C@]1([H])OC[C@@H](O)[C@H](O)[C@H]1O '
               'NAME: capilliposide B REASON: MISSED Contains 13 hydroxyl '
               'groups, need exactly 2\n'
               ' * SMILES: '
               'C(C(O)=O)CC/C=C\\[C@@H](/C=C/C=C\\C/C=C\\C=C\\[C@@H](C/C=C\\CC)O)O '
               'NAME: aspirin-triggered resolvin D5 REASON: MISSED Contains 3 '
               'hydroxyl groups, need exactly 2\n'
               ' * SMILES: '
               'C(C[C@@H](/C=C/C=C\\C/C=C\\C\\C=C/C=C/[C@@H](CC)O)O)CC(=O)O '
               'NAME: resolvin E2 REASON: MISSED Contains 3 hydroxyl groups, '
               'need exactly 2\n'
               ' * SMILES: '
               'C(/C=C/C=C\\C=C\\[C@@H](OO)CCCCC)=C\\[C@H]([C@H](CCCC(O)=O)O)O '
               'NAME: '
               '(5S,6R)-dihydroxy-(15S)-hydroperoxy-(7E,9E,11Z,13E)-icosatetraenoic '
               'acid REASON: MISSED Contains 4 hydroxyl groups, need exactly '
               '2\n'
               ' * SMILES: '
               '[H][C@@]1(CC[C@]2([H])[C@]1(C)CC[C@]1([H])[C@@]34CC[C@@H](C[C@]3(O)[C@H](O)C[C@@]21OC4)OS(O)(=O)=O)[C@H](C)\\C=C\\CC(C)C '
               'NAME: eurysterol B sulfonic acid REASON: MISSED Contains 3 '
               'hydroxyl groups, need exactly 2\n'
               ' * SMILES: OC(=O)C1=CC=C(N1)C(=O)NC1=C(O)C2=CC=C(O)C=C2OC1=O '
               'NAME: cacibiocin A REASON: MISSED Contains 3 hydroxyl groups, '
               'need exactly 2\n'
               ' * SMILES: '
               '[H][C@@]12C[C@@](C[C@H](N)C(O)=O)(O[C@]1([H])[C@H](O)[C@H](O)CO2)C(O)=O '
               'NAME: neodysiherbaine A REASON: MISSED Contains 4 hydroxyl '
               'groups, need exactly 2\n'
               ' * SMILES: OC[C@@H](O)CS(O)(=O)=O NAME: '
               '(2R)-3-sulfopropanediol REASON: MISSED Contains 3 hydroxyl '
               'groups, need exactly 2\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'O=C1N(C(=O)[C@@H](NC(=O)[C@H](NC(=O)C/C=C/[C@H]2O[C@H]2C(=O)CC(C)C)CN(C)C)C(C)C)[C@@H](CC(C)C)C(=C1C)O',
                                     'name': 'Sandarazol B',
                                     'reason': 'Contains 1 hydroxyl groups, '
                                               'need exactly 2'},
                                 {   'smiles': 'ClC1=CC=C(C=2OC(COC(C)(C)C(O)=O)=C(N2)C)C=C1',
                                     'name': 'romazarit',
                                     'reason': 'Contains 0 hydroxyl groups, '
                                               'need exactly 2'},
                                 {   'smiles': 'C[C@H]1CN([C@@H](COC2=C(C=C(C=C2)NC(=O)NC3CCCCC3)C(=O)N(C[C@@H]1OC)C)C)C',
                                     'name': '1-cyclohexyl-3-[(4R,7S,8R)-8-methoxy-4,5,7,10-tetramethyl-11-oxo-2-oxa-5,10-diazabicyclo[10.4.0]hexadeca-1(12),13,15-trien-14-yl]urea',
                                     'reason': 'Contains 0 hydroxyl groups, '
                                               'need exactly 2'},
                                 {   'smiles': 'C[C@H]1CCCCO[C@@H]([C@H](CN(C(=O)C2=C(O1)C=CC(=C2)NS(=O)(=O)C3=CC=CS3)[C@H](C)CO)C)CN(C)C(=O)NC4=CC=CC5=CC=CC=C54',
                                     'name': '1-[[(3S,9S,10S)-12-[(2R)-1-hydroxypropan-2-yl]-3,10-dimethyl-13-oxo-16-(thiophen-2-ylsulfonylamino)-2,8-dioxa-12-azabicyclo[12.4.0]octadeca-1(14),15,17-trien-9-yl]methyl]-1-methyl-3-(1-naphthalenyl)urea',
                                     'reason': 'Contains 1 hydroxyl groups, '
                                               'need exactly 2'},
                                 {   'smiles': 'P(OC[C@@H](COC(CCCCCCCCCCCCCCCC)=O)OC(CCCCCCCCCCCCCCCC)=O)(=O)(OCC[NH3+])[O-]',
                                     'name': '1,2-diheptadecanoyl-sn-glycero-3-phosphoethanolamine '
                                             'zwitterion',
                                     'reason': 'Contains 0 hydroxyl groups, '
                                               'need exactly 2'},
                                 {   'smiles': 'O=C1N(C(CC1)C(O)=O)CCC(N)C(O)=O',
                                     'name': "(2S,3'S)-alpha-Amino-2-carboxy-5-oxo-1-pyrrolidinebutanoic "
                                             'acid',
                                     'reason': 'Contains 0 hydroxyl groups, '
                                               'need exactly 2'},
                                 {   'smiles': 'O1[C@@H]([C@@H](O[C@@H]2O[C@@H]([C@H](O)[C@H](O)[C@H]2O)CO)[C@H](O[C@@H]3O[C@H]([C@@H](O)[C@@H](O)[C@@H]3O)C)[C@@H](NC(=O)C)[C@@H]1OC[C@H]4O[C@H](O)[C@H](NC(=O)C)[C@@H](O[C@@H]5O[C@@H]([C@H](O)[C@H](O)[C@H]5O)CO)[C@H]4O)CO',
                                     'name': 'N-[(2S,3R,4R,5R,6R)-6-[[(2R,3R,4R,5S,6R)-3-Acetamido-6-(hydroxymethyl)-5-[(2S,3R,4S,5R,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-4-[(2S,3S,4R,5S,6S)-3,4,5-trihydroxy-6-methyloxan-2-yl]oxyoxan-2-yl]oxymethyl]-2,5-dihydroxy-4-[(2S,3R,4S,5R,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-3-yl]acetamide',
                                     'reason': 'Contains 14 hydroxyl groups, '
                                               'need exactly 2'},
                                 {   'smiles': 'COC(=O)C1=CC=CC=C1NC(=O)NC2=NC=C(C=C2)Cl',
                                     'name': '2-[[[(5-chloro-2-pyridinyl)amino]-oxomethyl]amino]benzoic '
                                             'acid methyl ester',
                                     'reason': 'Contains 0 hydroxyl groups, '
                                               'need exactly 2'},
                                 {   'smiles': 'O=C(O[C@@H]1[C@@H]2[C@@]3(O)[C@]([C@@H](O)[C@@H]([C@H]3[C@@H](C1)C)O)(C)CC2(C)C)C',
                                     'name': '4beta-acetoxy-9beta-10beta-15alpha-trihydroxyprobotrydial',
                                     'reason': 'Contains 3 hydroxyl groups, '
                                               'need exactly 2'},
                                 {   'smiles': 'ClC(CCCCCCC)CC',
                                     'name': 'Decane, 3-chloro-',
                                     'reason': 'Contains 0 hydroxyl groups, '
                                               'need exactly 2'}],
    'sample_false_negatives': [   {   'smiles': 'OCC(CO)OC(CCC/C=C/1\\O[C@]2(C[C@H]([C@@H]([C@]2(C1)[H])/C=C/[C@H](CCCCC)O)O)[H])=O',
                                      'name': 'prostaglandin I2 2-glyceryl '
                                              'ester',
                                      'reason': 'Contains 4 hydroxyl groups, '
                                                'need exactly 2'},
                                  {   'smiles': '[H][C@@]1(CO[C@@H](O[C@@]2([H])CC[C@@]3(C)[C@@]([H])(CC[C@]4(C)[C@]3([H])CC[C@@]35O[C@@H](O)[C@]6([C@H](O)C[C@@]43C)[C@H](CC(C)(C)C[C@@]56[H])OC(=O)CCCCC)C2(C)C)[C@H](O[C@]2([H])O[C@H](CO)[C@@H](O)[C@H](O)[C@H]2O)[C@H]1O)O[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O[C@]1([H])OC[C@@H](O)[C@H](O)[C@H]1O',
                                      'name': 'capilliposide B',
                                      'reason': 'Contains 13 hydroxyl groups, '
                                                'need exactly 2'},
                                  {   'smiles': 'C(/C=C/C=C\\C=C\\[C@@H](OO)CCCCC)=C\\[C@H]([C@H](CCCC(O)=O)O)O',
                                      'name': '(5S,6R)-dihydroxy-(15S)-hydroperoxy-(7E,9E,11Z,13E)-icosatetraenoic '
                                              'acid',
                                      'reason': 'Contains 3 hydroxyl groups, '
                                                'need exactly 2'},
                                  {   'smiles': '[C@@H]([C@@H]([C@@H](/C=C(/C([C@H]([C@H]([C@@H](CCCC)C)O)C)=O)\\C)OC)O)(C(N/C=C\\C=1C=C(C(=CC1)O)Cl)=O)OCC',
                                      'name': 'chondrochloren B',
                                      'reason': 'Contains 3 hydroxyl groups, '
                                                'need exactly 2'},
                                  {   'smiles': '[H][C@]1(OC[C@@H](O)[C@H](O[C@]2([H])O[C@H](CO)[C@@H](O)[C@H](O)[C@H]2O)[C@H]1O)O[C@H]1CC[C@@]2(C)[C@@]([H])(CC[C@]3(C)[C@]2([H])CC=C2[C@]4([H])CC(C)(C)C[C@@H](OC(=O)c5ccccc5)[C@]4(CO)[C@@H](O)C[C@@]32C)C1(C)C',
                                      'name': 'glochierioside B',
                                      'reason': 'Contains 8 hydroxyl groups, '
                                                'need exactly 2'},
                                  {   'smiles': 'CC1(C)CC[C@]2(CO)[C@H](O)C[C@]3(C)C(=CC[C@@H]4[C@@]5(C)CC[C@H](O[C@@H]6OC[C@H](O[C@@H]7O[C@H](CO)[C@@H](O)[C@H](O)[C@H]7O[C@@H]7OC[C@@H](O)[C@H](O)[C@H]7O)[C@H](O)[C@H]6O[C@@H]6O[C@H](CO)[C@@H](O)[C@H](O)[C@H]6O)C(C)(C)[C@@H]5CC[C@@]34C)[C@@H]2C1',
                                      'name': 'candidoside',
                                      'reason': 'Contains 13 hydroxyl groups, '
                                                'need exactly 2'},
                                  {   'smiles': 'C[C@H]1[C@H](CO[C@@H]2O[C@H](CO)[C@@H](O)[C@H](O)[C@H]2O)[C@H](C[C@]2(C)CC[C@]3(C)C(=CC=C4[C@@]5(C)C[C@@H](O)[C@H](O)C(C)(C)[C@@H]5CC[C@@]34C)[C@H]12)O[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O',
                                      'name': 'clethroidoside H',
                                      'reason': 'Contains 10 hydroxyl groups, '
                                                'need exactly 2'},
                                  {   'smiles': 'OC(CC(O)CCC1=CC(OC)=C(O)C=C1)CCCCC',
                                      'name': '6-Gingediol',
                                      'reason': 'Contains 3 hydroxyl groups, '
                                                'need exactly 2'},
                                  {   'smiles': 'CC(C)[C@@H]1C[C@@H](O)[C@H]2[C@@]1(COC(C)=O)CC[C@@]1(C)[C@@H]3[C@@H](O)C[C@H]4C(C)(C)[C@@H](O[C@@H]5O[C@H](COC(C)=O)[C@@H](O)[C@H](O)[C@H]5O)[C@@H](C[C@]4(C)C3=CC[C@]21C)OC(C)=O',
                                      'name': 'rubianol-e '
                                              "3-O-(6'-O-acetyl)-beta-D-glucopyranoside",
                                      'reason': 'Contains 5 hydroxyl groups, '
                                                'need exactly 2'},
                                  {   'smiles': '[H][C@@]12CCCN1C(=O)[C@]1(O)[C@@H](OCC=C(C)C)c3c4n([C@H](OOC(C)(C)C[C@]4([H])N1C2=O)C=C(C)C)c1cc(OC)ccc31',
                                      'name': 'fumitremorgin A',
                                      'reason': 'Contains 1 hydroxyl groups, '
                                                'need exactly 2'}],
    'attempt': 2,
    'reasoning': 'The previous code correctly identifies molecules with '
                 'exactly two hydroxyl groups as diols. However, the error '
                 'analysis reveals that the program incorrectly classified '
                 'some molecules as diols when they had more than two hydroxyl '
                 'groups, and missed some diols that had exactly two hydroxyl '
                 'groups. The main issue seems to be that the program did not '
                 'account for cases where hydroxyl groups might be part of '
                 'other functional groups (e.g., carboxylic acids, sulfonic '
                 'acids, etc.) or where the hydroxyl groups might be in a '
                 'different form (e.g., -OH attached to a carbonyl group).\n'
                 '\n'
                 'To improve the program, we need to:\n'
                 '1. Ensure that the hydroxyl groups are not part of other '
                 'functional groups like carboxylic acids or sulfonic acids.\n'
                 '2. Consider cases where hydroxyl groups might be in '
                 'different forms (e.g., -OH attached to a carbonyl group).\n'
                 '\n'
                 'Here is the improved code:',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 373,
    'num_false_positives': 100,
    'num_true_negatives': 978,
    'num_false_negatives': 28,
    'num_negatives': None,
    'precision': 0.7885835095137421,
    'recall': 0.9301745635910225,
    'f1': 0.8535469107551488,
    'accuracy': 0.9134550371872887,
    'negative_predictive_value': 0.9721669980119284}