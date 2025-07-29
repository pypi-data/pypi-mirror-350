"""
Classifies: CHEBI:134363 tertiary amine oxide
"""
from rdkit import Chem

def is_tertiary_amine_oxide(smiles: str):
    """
    Determines if a molecule is a tertiary amine oxide based on its SMILES string.
    
    A tertiary amine oxide consists of an N-oxide where there are three organic groups bonded to the nitrogen atom.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a tertiary amine oxide, False otherwise
        str: Reason for classification
    """
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Refined pattern to match a nitrogen with a positive charge bonded to three carbons and one oxygen with negatively charged oxygen (N+ with C and O-)
    tertiary_amine_oxide_pattern = Chem.MolFromSmarts("[N+X4]([CX4,a])([CX4,a])([CX4,a])[OX1-]")
    
    if mol.HasSubstructMatch(tertiary_amine_oxide_pattern):
        return True, "Molecule contains a tertiary amine oxide group"

    return False, "Molecule does not contain a tertiary amine oxide group"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:134363',
                          'name': 'tertiary amine oxide',
                          'definition': 'An N-oxide where there are three '
                                        'organic groups bonded to the nitrogen '
                                        'atom.',
                          'parents': ['CHEBI:35580'],
                          'xrefs': [   'Patent:EP0545208',
                                       'Patent:EP0757983',
                                       'Patent:EP0866058',
                                       'Patent:EP1068179',
                                       'Patent:US4206204',
                                       'Patent:WO9950236'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': None,
    'message': '\n'
               'Attempt failed: F1 score of 0.5546218487394958 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: '
               'O=C1N2[C@@]3([C@@]4([C@]5([N+](CC4)(C\\C(\\[C@](C5)(C3=CC1)[H])=C\\CO)[O-])[H])C=6C2=CC=CC6)[H] '
               'NAME: isostrychnine N-oxide REASON: CORRECT Molecule contains '
               'a tertiary amine oxide group\n'
               ' * SMILES: '
               '[H][C@]1(C[N+]2([O-])CC[C@@]34C(Nc5ccccc35)=C(C(=O)OC)[C@@]1([H])C[C@]24[H])C(C)=O '
               'NAME: (-)-Alstolucine C REASON: CORRECT Molecule contains a '
               'tertiary amine oxide group\n'
               ' * SMILES: '
               'C[N+]1([C@@H]2CC(C[C@H]1[C@H]3[C@@H]2O3)OC(=O)[C@H](CO)C4=CC=CC=C4)[O-] '
               'NAME: LSM-1606 REASON: CORRECT Molecule contains a tertiary '
               'amine oxide group\n'
               ' * SMILES: '
               '[C@@]1([C@@H](C)O)(O)C(O[C@H]2[C@@]3([N+](CC=C3COC([C@]([C@@H](C1)C)(C)O)=O)(CC2)[O-])[H])=O '
               'NAME: jacoline N-oxide REASON: CORRECT Molecule contains a '
               'tertiary amine oxide group\n'
               ' * SMILES: '
               '[C@@]12([N+]3(CC[C@H]1OC(/C(/CC(=C)[C@@](C(OCC2=CC3)=O)(CO)O)=C\\C)=O)[O-])[H] '
               'NAME: riddelliine N-oxide REASON: CORRECT Molecule contains a '
               'tertiary amine oxide group\n'
               ' * SMILES: C[N+](C)([O-])C NAME: trimethylamine N-oxide '
               'REASON: CORRECT Molecule contains a tertiary amine oxide '
               'group\n'
               ' * SMILES: '
               'O=C1N2[C@@]3([C@@]4([C@]5([N+](CC4)(C\\C(\\[C@](C5)(C3=CC1)[H])=C\\CO)[O-])[H])C=6C2=CC(=C(C6)OC)OC)[H] '
               'NAME: isobrucine N-oxide REASON: CORRECT Molecule contains a '
               'tertiary amine oxide group\n'
               ' * SMILES: C[N+]1([O-])CCC(=CC1)c1ccccc1 NAME: '
               '1-methyl-4-phenyl-1,2,3,6-tetrahydropyridine N-oxide REASON: '
               'CORRECT Molecule contains a tertiary amine oxide group\n'
               ' * SMILES: '
               '[H][C@@]12CC[C@H](C)C[N@+]1([O-])[C@@H](CC[C@H]2C)c1ccoc1 '
               'NAME: nupharidine REASON: CORRECT Molecule contains a tertiary '
               'amine oxide group\n'
               ' * SMILES: C[N@@+]1([O-])CC[C@@H](CC1)[Si](C)(C)c1ccccc1 NAME: '
               'trans-4-(dimethylphenylsilyl)-N-methylpiperidine N-oxide '
               'REASON: CORRECT Molecule contains a tertiary amine oxide '
               'group\n'
               ' * SMILES: '
               '[H][C@]12C[C@@]3([H])[C@]45C[C@@]([H])([C@@]1([H])COC4=Nc1cc4OCOc4c(OC)c51)[N+]3([O-])C\\C2=C/COC '
               'NAME: Gardfloramine-N(4)-oxide REASON: CORRECT Molecule '
               'contains a tertiary amine oxide group\n'
               ' * SMILES: '
               '[H][C@]12[C@H](C)\\C(O[C@]11CCC[N+]3([O-])CCC[C@@H](O1)[C@@]23[H])=C1OC(=O)C(C)=C\\1OC '
               'NAME: stemocurtisine N-oxide REASON: CORRECT Molecule contains '
               'a tertiary amine oxide group\n'
               ' * SMILES: '
               'C[N+]1([C@@H]2CC(C[C@H]1[C@H]3[C@H]2O3)OC(=O)[C@H](CO)C4=CC=CC=C4)[O-] '
               'NAME: LSM-5030 REASON: CORRECT Molecule contains a tertiary '
               'amine oxide group\n'
               ' * SMILES: '
               '[H][C@]12C[C@@]3([H])[C@]45C[C@@]([H])([C@@]1([H])COC4=Nc1c(OC)cc(OC)c(OC)c51)[N+]3([O-])C\\C2=C/COC '
               'NAME: gardneramine-N(4)-oxide REASON: CORRECT Molecule '
               'contains a tertiary amine oxide group\n'
               ' * SMILES: '
               'C[N+]1(CCC2=CC(=C(C=C2[C@@H]1CC3=CC(=C(C=C3)OC)O)O)OC)[O-] '
               'NAME: '
               '(1S)-1-[(3-hydroxy-4-methoxyphenyl)methyl]-6-methoxy-2-methyl-2-oxido-3,4-dihydro-1H-isoquinolin-2-ium-7-ol '
               'REASON: CORRECT Molecule contains a tertiary amine oxide '
               'group\n'
               ' * SMILES: '
               '[H][C@@]12[C@@H](CC[N+]1([O-])CC=C2COC(=O)[C@](O)(C(C)C)[C@H](C)O)OC(=O)C(\\C)=C\\C '
               'NAME: symphytine oxide REASON: CORRECT Molecule contains a '
               'tertiary amine oxide group\n'
               ' * SMILES: '
               'C=1(C=CC=CC1)/C(=C(/C=2C=CC=CC2)\\C=3C=CC(=CC3)OCC[N+]([O-])(C)C)/CC '
               'NAME: tamoxifen N-oxide REASON: CORRECT Molecule contains a '
               'tertiary amine oxide group\n'
               ' * SMILES: C(CCCCCCCC)CCC[N+](C)([O-])C NAME: '
               'dodecyldimethylamine N-oxide REASON: CORRECT Molecule contains '
               'a tertiary amine oxide group\n'
               ' * SMILES: OC(=O)CCCC(=O)Nc1ccc(CC[N+]2([O-])CCCCC2)cc1 NAME: '
               '5-({4-[2-(1-oxidopiperidin-1-yl)ethyl]phenyl}amino)-5-oxopentanoic '
               'acid REASON: CORRECT Molecule contains a tertiary amine oxide '
               'group\n'
               ' * SMILES: C1=CC([C@]2([N@+](CCC2)([O-])C)[H])=CN=C1 NAME: '
               "trans-(S)-nicotine N(1')-oxide REASON: CORRECT Molecule "
               'contains a tertiary amine oxide group\n'
               ' * SMILES: C1=CC([C@]2([N@@+](CCC2)([O-])C)[H])=CN=C1 NAME: '
               "cis-(S)-nicotine N(1')-oxide REASON: CORRECT Molecule contains "
               'a tertiary amine oxide group\n'
               ' * SMILES: C[N+](C)([O-])CCCN1c2ccccc2Sc2ccc(Cl)cc12 NAME: '
               'chlorpromazine N-oxide REASON: CORRECT Molecule contains a '
               'tertiary amine oxide group\n'
               ' * SMILES: '
               '[C@@]12([N+]3(CC[C@H]1OC(/C(/CC(=C)[C@](C(OCC2=CC3)=O)(OC(=O)C)C)=C\\C)=O)[O-])[H] '
               'NAME: acetylseneciphylline N-oxide REASON: CORRECT Molecule '
               'contains a tertiary amine oxide group\n'
               ' * SMILES: C([N+](C)([O-])C)CCCCCCCCC NAME: '
               'decylamine-N,N-dimethyl-N-oxide REASON: CORRECT Molecule '
               'contains a tertiary amine oxide group\n'
               ' * SMILES: '
               '[H]\\C(C)=C1/C[C@@H](C)[C@@](C)(O)C(=O)OCC2=CC[N+]3([O-])CC[C@@]([H])(OC1=O)[C@@]23[H] '
               'NAME: senecionine N-oxide REASON: CORRECT Molecule contains a '
               'tertiary amine oxide group\n'
               'False positives: SMILES: '
               'COC([C@@H]1C[C@@]23CCC[N+]4(CCC5(C6=CC=CC=C6N(C(=O)OC)[C@]15CC2)[C@]34[H])[O-])=O '
               'NAME: Pleiocarpoline REASON: WRONGLY CLASSIFIED Molecule '
               'contains a tertiary amine oxide group\n'
               ' * SMILES: '
               'O=C1N([C@]23[C@H](C(C)(C)[C@@]4(C2)C(=O)NC5=C4C=CC6=C5C(=O)CC(O6)(C)C)C[C@]17[N+]([O-])(C[C@@H](C7)C)C3)C '
               'NAME: Mangrovamide B REASON: WRONGLY CLASSIFIED Molecule '
               'contains a tertiary amine oxide group\n'
               ' * SMILES: CN(C)(=O)CCCC1(OCc2cc(ccc12)C#N)c1ccc(F)cc1 NAME: '
               'Citalopram N-oxide REASON: WRONGLY CLASSIFIED Molecule '
               'contains a tertiary amine oxide group\n'
               ' * SMILES: '
               '[O-][N+]12[C@@]([C@@H](O)CC1)(C(=CC2)COC(=O)[C@](O)(C(C)C)[C@H](OC)C)[H] '
               'NAME: Heliotrine n-oxide REASON: WRONGLY CLASSIFIED Molecule '
               'contains a tertiary amine oxide group\n'
               ' * SMILES: '
               'ClC=1C(NC(=O)C=2SC(NC=3N=C(N=C(N4CC[N+]([O-])(CC4)CCO)C3)C)=NC2)=C(C=CC1)C '
               'NAME: Dasatinib n-oxide REASON: WRONGLY CLASSIFIED Molecule '
               'contains a tertiary amine oxide group\n'
               ' * SMILES: '
               '[O-][N@@+]12[C@@]3([C@H]([C@@](C[C@]1(C=4NC=5C(C4C3)=CC=CC5)[H])(/C(/C2)=C\\C)[H])C(OC)=O)[H] '
               'NAME: Pericyclivine-N-oxide REASON: WRONGLY CLASSIFIED '
               'Molecule contains a tertiary amine oxide group\n'
               ' * SMILES: '
               '[O-][N+]1([C@@]2(C=3C(CC1)=CC(OC)=C(OC)C3OC=4C=C5C(N(CCC5=CC4OC)C)CC6=CC=C(OC=7C=C(C2)C=CC7OC)C=C6)[H])C '
               'NAME: Fenfangjine A REASON: WRONGLY CLASSIFIED Molecule '
               'contains a tertiary amine oxide group\n'
               ' * SMILES: '
               'S(=O)(=O)(CCC1=CC=2C(C[C@@H]3[N+]([O-])(CCC3)C)=CNC2C=C1)C4=CC=CC=C4 '
               'NAME: Eletriptan N-oxide REASON: WRONGLY CLASSIFIED Molecule '
               'contains a tertiary amine oxide group\n'
               ' * SMILES: [O-][N+]12C(C(O)CC1)C(=CC2)COC(=O)C(O)(C(C)C)C(O)C '
               'NAME: Heliotridine viridiflorate N-oxide REASON: WRONGLY '
               'CLASSIFIED Molecule contains a tertiary amine oxide group\n'
               ' * SMILES: '
               'C/C=C\\1/C2CC[N@+]3(CC[C@]4(C5=CC=CC=C5NC4=C2C(=O)OC)[C@@]13[H])[O-] '
               'NAME: Condylocarpine N-oxide REASON: WRONGLY CLASSIFIED '
               'Molecule contains a tertiary amine oxide group\n'
               ' * SMILES: C(CC[N+](C)(C)[O-])=C1C=2C(CCC3=C1C=CC=C3)=CC=CC2 '
               'NAME: amitriptylinoxide REASON: WRONGLY CLASSIFIED Molecule '
               'contains a tertiary amine oxide group\n'
               ' * SMILES: '
               'O[C@@]12C34N(=O)(CCC1)CCC[C@]3(O)C(=O)C[C@@]2(C[C@](C4)(C)[H])[H] '
               'NAME: Lycoposerramine F REASON: WRONGLY CLASSIFIED Molecule '
               'contains a tertiary amine oxide group\n'
               ' * SMILES: '
               'O=C1N[C@H](C(=O)N[C@H]1CCCN(O)C(=O)/C=C(/CCOC(=O)[C@@H]([N+]([O-])(C)C)CCCN(O)C(=O)/C=C(/CCO[C@@H]2O[C@@H]([C@@H](O)[C@@H]([C@@H]2O)O)CO)\\C)\\C)CCCN(O)C(=O)/C=C(/CCO[C@@H]3O[C@@H]([C@@H](O)[C@@H]([C@@H]3O)O)CO)\\C '
               'NAME: Metachelin A REASON: WRONGLY CLASSIFIED Molecule '
               'contains a tertiary amine oxide group\n'
               ' * SMILES: '
               'O1CC=2C(/C(=C\\CC[N+]([O-])(C)C)/C=3C1=CC=CC3)=CC=CC2 NAME: '
               'Doxepin N-oxide REASON: WRONGLY CLASSIFIED Molecule contains a '
               'tertiary amine oxide group\n'
               ' * SMILES: '
               '[O-][N@+]12[C@]34N5C(=O)C[C@]3(CC[C@]4([C@](CC1)(C=6C5=CC(OC)=C(OC)C6)[H])[H])C=CC2 '
               'NAME: '
               '(1R,5R,8S,16S,17S)-11,12-Dimethoxy-5-oxido-15-aza-5-azoniahexacyclo[13.4.2.01,16.05,16.08,17.09,14]henicosa-2,9,11,13-tetraen-21-one '
               'REASON: WRONGLY CLASSIFIED Molecule contains a tertiary amine '
               'oxide group\n'
               ' * SMILES: ClC1=CC=2N(CCC[N+]([O-])(C)C)C=3C(CCC2C=C1)=CC=CC3 '
               'NAME: Clomipramine N-oxide REASON: WRONGLY CLASSIFIED Molecule '
               'contains a tertiary amine oxide group\n'
               ' * SMILES: '
               'C(CC[N@@+]1([O-])CC[C@](CC1)(O)C2=CC=C(C=C2)Cl)(C(N(C)C)=O)(C3=CC=CC=C3)C4=CC=CC=C4 '
               'NAME: loperamide oxide REASON: WRONGLY CLASSIFIED Molecule '
               'contains a tertiary amine oxide group\n'
               ' * SMILES: [O-][N+]12CC(CCC1)(CCC3=NC=4C(C3(O)CC2)=CC=CC4)CC '
               'NAME: Rhazidigenine Nb-oxide REASON: WRONGLY CLASSIFIED '
               'Molecule contains a tertiary amine oxide group\n'
               ' * SMILES: '
               'OC1C2([N+]([O-])(CCC=3C2=CC(O)=C(OC)C3)C)CC4=C1C=5OCOC5C=C4 '
               'NAME: Fumaritine N-oxide REASON: WRONGLY CLASSIFIED Molecule '
               'contains a tertiary amine oxide group\n'
               ' * SMILES: [O-][N+]12C([C@@H](CC1)COC(=O)C(O)(C(C)C)C(O)C)CCC2 '
               'NAME: '
               '[(1R)-4-Oxido-2,3,5,6,7,8-hexahydro-1H-pyrrolizin-4-ium-1-yl]methyl '
               '2-hydroxy-2-(1-hydroxyethyl)-3-methylbutanoate REASON: WRONGLY '
               'CLASSIFIED Molecule contains a tertiary amine oxide group\n'
               ' * SMILES: [O-][N+](CCC=1C2=C(NC1)C=CC(OC)=C2)(C)C NAME: '
               '5-Methoxy-N,N-dimethyl-tryptamine Nb-oxide REASON: WRONGLY '
               'CLASSIFIED Molecule contains a tertiary amine oxide group\n'
               ' * SMILES: [O-][N+]1(CC2N(C3=NC=CC=C3CC4=C2C=CC=C4)CC1)C NAME: '
               'Mirtazapine-N-oxide REASON: WRONGLY CLASSIFIED Molecule '
               'contains a tertiary amine oxide group\n'
               ' * SMILES: [O-][N+]1(C2CCC1CC(OC(=O)/C(/C)=C/C)C2)C NAME: '
               '3alpha-Tigloyloxytropane N-oxide REASON: WRONGLY CLASSIFIED '
               'Molecule contains a tertiary amine oxide group\n'
               ' * SMILES: '
               'S(=O)(=O)(N1CC[N+]([O-])(CC1)CC)C2=CC(=C(OCC)C=C2)C=3NC(=O)C=4N(N3)C(=NC4C)CCC '
               'NAME: Vardenafil N-oxide REASON: WRONGLY CLASSIFIED Molecule '
               'contains a tertiary amine oxide group\n'
               ' * SMILES: '
               'O=C(N1[C@@H](C(=O)N[C@H](C(=O)N[C@@H](C(=O)NC(C(=O)N[C@H](C(=O)N[C@H](C(=O)NC(C(=O)NC(C(=O)NCCC(=O)N[C@H](C[N+]([O-])(C)C)C)(C)C)(C)C)CC(C)C)CC(C)C)(C)C)[C@@H](O)C(C)C)CC(C)C)C[C@@H](C1)C)/C=C\\[C@@H](CC)C '
               'NAME: Leucinostatin H REASON: WRONGLY CLASSIFIED Molecule '
               'contains a tertiary amine oxide group\n'
               'False negatives: SMILES: '
               'CN(C)CCC[N+]1(C2=CC=CC=C2SC3=C1C=C(C=C3)Cl)[O-] NAME: '
               '3-(2-chloro-10-oxido-10-phenothiazin-10-iumyl)-N,N-dimethyl-1-propanamine '
               'REASON: MISSED Molecule does not contain a tertiary amine '
               'oxide group\n'
               ' * SMILES: CN(C)(=O)c1ccccc1 NAME: N,N-dimethylaniline N-oxide '
               'REASON: MISSED Molecule does not contain a tertiary amine '
               'oxide group\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'C[C@@H]1OC(=O)C=C1',
                                     'name': '(S)-5-methylfuran-2(5H)-one',
                                     'reason': 'Molecule does not contain a '
                                               'tertiary amine oxide group'},
                                 {   'smiles': 'Cc1cccc(c1)C(O)=O',
                                     'name': 'm-toluic acid',
                                     'reason': 'Molecule does not contain a '
                                               'tertiary amine oxide group'},
                                 {   'smiles': 'CN(C)CC(=O)NC[C@@H]1[C@@H]([C@@H](N1)CO)C2=CC=C(C=C2)C3=CC=CC(=C3)C#N',
                                     'name': 'N-[[(2S,3S,4R)-3-[4-(3-cyanophenyl)phenyl]-4-(hydroxymethyl)-2-azetidinyl]methyl]-2-(dimethylamino)acetamide',
                                     'reason': 'Molecule does not contain a '
                                               'tertiary amine oxide group'},
                                 {   'smiles': 'C[C@@H]1O[C@@H](OCCCCCCCCCC(=O)CC(O)=O)[C@H](O)C[C@H]1O',
                                     'name': 'bkos#20',
                                     'reason': 'Molecule does not contain a '
                                               'tertiary amine oxide group'},
                                 {   'smiles': 'C([C@@](COC(CCCCCCCCC/C=C\\CCCCCC)=O)(OC(CCCCCCCCC/C=C\\CCCCCC)=O)[H])OP(=O)(O)OC[C@@](CO)([H])O',
                                     'name': 'PG(18:1(11Z)/18:1(11Z))',
                                     'reason': 'Molecule does not contain a '
                                               'tertiary amine oxide group'},
                                 {   'smiles': 'O=C(N1C(C(=O)NC(C(=O)NC(C(=O)NC(C(=O)NC(C(=O)NC(CO)CC=2C3=C(C=CC=C3)NC2)CCC(=O)N)(C)C)(C)C)(CC)C)CCC1)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)CNC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C(NC(=O)C)CC4=CC=CC=C4)(C)C)CO)(C)C)(C)C)CC(C)C)CCC(=O)N)(C)C)(C)C)C)C)(C)C',
                                     'name': 'Chrysospermin B',
                                     'reason': 'Molecule does not contain a '
                                               'tertiary amine oxide group'},
                                 {   'smiles': 'CC1(C=CC2=C3C(=CC(=C2O1)OC)C(=O)C(=CO3)C4=CC5=C(C=C4OC)OCO5)C',
                                     'name': '6-methoxy-3-(6-methoxy-1,3-benzodioxol-5-yl)-8,8-dimethyl-4-pyrano[2,3-h][1]benzopyranone',
                                     'reason': 'Molecule does not contain a '
                                               'tertiary amine oxide group'},
                                 {   'smiles': 'O[C@@H]([C@H](NC(=O)[C@@H](N)CCC(O)=O)C(=O)NCC(O)=O)C',
                                     'name': 'Glu-Thr-Gly',
                                     'reason': 'Molecule does not contain a '
                                               'tertiary amine oxide group'},
                                 {   'smiles': 'O([C@H]1[C@H](O[C@@H]2O[C@H]([C@@H](O)[C@@H](O)[C@@H]2O)C)[C@@H](NC(=O)C)[C@@H](O[C@@H]1CO)O[C@H]3[C@@H](O)[C@H](O)[C@H](O[C@@H]3OC[C@H]4O[C@@H](O[C@H]5[C@H](O)[C@@H](NC(=O)C)C(O[C@@H]5CO)O)[C@@H](O)[C@@H](O)[C@@H]4O)CO)[C@@H]6O[C@@H]([C@H](O)[C@H](O[C@]7(O[C@H]([C@H](NC(=O)C)[C@@H](O)C7)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]6O)CO',
                                     'name': '(2S,4S,5R,6R)-5-Acetamido-2-[(2S,3R,4S,5S,6R)-2-[(2R,3S,4R,5R,6S)-5-acetamido-6-[(2S,3S,4S,5S,6R)-2-[[(2R,3S,4S,5S,6S)-6-[(2R,3S,4R,5R)-5-acetamido-4,6-dihydroxy-2-(hydroxymethyl)oxan-3-yl]oxy-3,4,5-trihydroxyoxan-2-yl]methoxy]-4,5-dihydroxy-6-(hydroxymethyl)oxan-3-yl]oxy-2-(hydroxymethyl)-4-[(2S,3S,4R,5S,6S)-3,4,5-trihydroxy-6-methyloxan-2-yl]oxyoxan-3-yl]oxy-3,5-dihydroxy-6-(hydroxymethyl)oxan-4-yl]oxy-4-hydroxy-6-[(1R,2R)-1,2,3-trihydroxypropyl]oxane-2-carboxylic '
                                             'acid',
                                     'reason': 'Molecule does not contain a '
                                               'tertiary amine oxide group'},
                                 {   'smiles': 'COCCOC(C)C(O)=O',
                                     'name': '2-(2-methoxyethoxy)propanoic '
                                             'acid',
                                     'reason': 'Molecule does not contain a '
                                               'tertiary amine oxide group'}],
    'sample_false_negatives': [],
    'attempt': 2,
    'reasoning': 'In the previous implementation of the '
                 '`is_tertiary_amine_oxide` function, the key approach was to '
                 'detect an N-oxide with three organic groups bonded to the '
                 'nitrogen. The SMARTS pattern used was limited and captured '
                 'only simple configurations, leading to a low F1 score. The '
                 'false positives and false negatives indicate the need for a '
                 'more comprehensive pattern.\n'
                 '\n'
                 '### Analysis:\n'
                 '1. **False Negatives**: The previous function failed to '
                 'catch molecules like `N,N-dimethylaniline N-oxide`, implying '
                 'the patterns did not adequately recognize tertiary amine '
                 'oxides with aromatic or diverse organic attachments.\n'
                 '   \n'
                 '2. **False Positives**: This suggests that some molecules '
                 'without the requisite amine oxide structure were incorrectly '
                 'classified, possibly due to inappropriate pattern '
                 'specificity.\n'
                 '\n'
                 '### Improvements:\n'
                 '- Refine SMARTS patterns to consider:\n'
                 '  - **Three organic attachments**: These can be either alkyl '
                 'or aryl (aromatic).\n'
                 '  - **N-oxide group**: Ensure specificity for this moiety '
                 'without capturing secondary or quaternary amines by '
                 'mistake.\n'
                 '  - Consider secondary nitrogen oxidation cases '
                 '(N[+](C)(C)[O-]), as long as they fit the tertiary amine '
                 'structure.\n'
                 '\n'
                 "Let's improve the code accordingly.",
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 35,
    'num_false_positives': 51,
    'num_true_negatives': 142214,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.4069767441860465,
    'recall': 1.0,
    'f1': 0.5785123966942148,
    'accuracy': 0.9996416022487702,
    'negative_predictive_value': 1.0}