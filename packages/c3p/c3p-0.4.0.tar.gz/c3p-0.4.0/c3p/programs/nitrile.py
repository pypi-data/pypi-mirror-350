"""
Classifies: CHEBI:18379 nitrile
"""
"""
Classifies: nitrile
"""
from rdkit import Chem

def is_nitrile(smiles: str):
    """
    Determines if a molecule is a nitrile based on its SMILES string.
    A nitrile is a compound having the structure R-C#N, where 'R' can be any substituent except hydrogen.
    The suffix nitrile denotes the triply bound #N atom.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if the molecule is a nitrile, False otherwise
        str: Reason for classification
    """
    # Parse the SMILES string
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Define allowed elements (common in organic molecules)
    allowed_atomic_nums = set([1, 6, 7, 8, 9, 15, 16, 17, 35, 53])  # H, C, N, O, F, P, S, Cl, Br, I

    # Check for disallowed elements (metals, etc.)
    for atom in mol.GetAtoms():
        if atom.GetAtomicNum() not in allowed_atomic_nums:
            return False, "Contains metal or disallowed atoms; likely not an organic nitrile"

    # Define the nitrile SMARTS pattern:
    # [!#1][C]#[N]: Nitrile carbon connected to any atom except hydrogen
    nitrile_pattern = Chem.MolFromSmarts("[!#1][C]#[N]")
    if nitrile_pattern is None:
        return False, "Invalid nitrile SMARTS pattern"

    # Search for nitrile substructure
    if mol.HasSubstructMatch(nitrile_pattern):
        return True, "Contains nitrile group (R-C#N) per definition"
    else:
        return False, "Does not contain nitrile group (R-C#N) per definition"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:18379',
                          'name': 'nitrile',
                          'definition': 'A compound having the structure RC#N; '
                                        'thus a C-substituted derivative of '
                                        'hydrocyanic acid, HC#N. In systematic '
                                        'nomenclature, the suffix nitrile '
                                        'denotes the triply bound #N atom, not '
                                        'the carbon atom attached to it.',
                          'parents': ['CHEBI:23424'],
                          'xrefs': ['KEGG:C00726'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 30,
                           'log_lines_of_code': 3.4011973816621555,
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
                                                 0,
                                                 1,
                                                 1,
                                                 0,
                                                 1,
                                                 1,
                                                 2,
                                                 3,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 0,
                                                 1,
                                                 1,
                                                 2,
                                                 1,
                                                 2],
                           'max_indent': 3,
                           'imports': ['from rdkit import Chem'],
                           'imports_count': 1,
                           'methods_called': [   'MolFromSmarts',
                                                 'HasSubstructMatch',
                                                 'GetAtoms',
                                                 'MolFromSmiles',
                                                 'GetAtomicNum'],
                           'methods_called_count': 5,
                           'smarts_strings': ['[!#1][C]#[N]'],
                           'smarts_strings_count': 1,
                           'defs': ['is_nitrile(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "Contains metal or '
                                          'disallowed atoms; likely not an '
                                          'organic nitrile"',
                                          'False, "Invalid nitrile SMARTS '
                                          'pattern"',
                                          'True, "Contains nitrile group '
                                          '(R-C#N) per definition"',
                                          'False, "Does not contain nitrile '
                                          'group (R-C#N) per definition"'],
                           'returns_count': 5,
                           'complexity': 3.4802394763324314},
    'message': '\n'
               'Attempt failed: F1 score of 0.38080846241027577 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: '
               'C[C@@H](NC(=O)[C@H](C#N)C(C)(C)C)c1ccc(Cl)cc1Cl NAME: '
               '(1R,2S)-diclocymet REASON: CORRECT Contains nitrile group '
               '(R-C#N) per definition\n'
               ' * SMILES: '
               'O1[C@@H]([C@@H](O)[C@H](O)[C@@H](O)[C@@H]1OC(C(C)C#N)C)CO '
               'NAME: '
               '2-methyl-3-[(2R,3R,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxybutanenitrile '
               'REASON: CORRECT Contains nitrile group (R-C#N) per definition\n'
               ' * SMILES: CO\\C=C(\\C(O)=O)c1ccccc1Oc1cc(Oc2ccccc2C#N)ncn1 '
               'NAME: azoxystrobin acid REASON: CORRECT Contains nitrile group '
               '(R-C#N) per definition\n'
               ' * SMILES: C(C[C@@H](C#N)O)CCC NAME: '
               '(2S)-2-hydroxyheptanenitrile REASON: CORRECT Contains nitrile '
               'group (R-C#N) per definition\n'
               ' * SMILES: C1=2C(=CNC1=CC=CC2)CC#N NAME: indole-3-acetonitrile '
               'REASON: CORRECT Contains nitrile group (R-C#N) per definition\n'
               ' * SMILES: CN(C)CCC[C@@]1(OCc2cc(ccc12)C#N)c1ccc(F)cc1 NAME: '
               '(R)-citalopram REASON: CORRECT Contains nitrile group (R-C#N) '
               'per definition\n'
               ' * SMILES: C(CCCCS(C)=O)CCC#N NAME: '
               '1-cyano-8-(methylsulfinyl)heptane REASON: CORRECT Contains '
               'nitrile group (R-C#N) per definition\n'
               ' * SMILES: CCNc1nc(CC)c(s1)C(=O)N[C@@H](C#N)c1cccs1 NAME: '
               '(S)-ethaboxam REASON: CORRECT Contains nitrile group (R-C#N) '
               'per definition\n'
               ' * SMILES: CN1c2ccccc2C(C#N)(C(=O)NCCC(O)=O)c2ccccc12 NAME: '
               '3-{[(9-cyano-10-methyl-9,10-dihydroacridin-9-yl)carbonyl]amino}propanoic '
               'acid REASON: CORRECT Contains nitrile group (R-C#N) per '
               'definition\n'
               ' * SMILES: C=1(C=C([C@@H](C#N)O)C=CC1)OC NAME: '
               '(2S)-2-hydroxy-2-(3-methoxyphenyl)acetonitrile REASON: CORRECT '
               'Contains nitrile group (R-C#N) per definition\n'
               ' * SMILES: '
               'C(CCN1CCC(CC1)N2C3=C(N(C2=O)C(CC)=O)C=CC=C3)(C#N)(C4=CC=CC=C4)C5=CC=CC=C5 '
               'NAME: bezitramide REASON: CORRECT Contains nitrile group '
               '(R-C#N) per definition\n'
               ' * SMILES: '
               'C1CCC(CC1)C(=O)N2C[C@@H]3C([C@H](C2)N3)C4=CC=C(C=C4)C5=CC=C(C=C5)C#N '
               'NAME: '
               '4-[4-[(1S,5R)-3-[cyclohexyl(oxo)methyl]-3,6-diazabicyclo[3.1.1]heptan-7-yl]phenyl]benzonitrile '
               'REASON: CORRECT Contains nitrile group (R-C#N) per definition\n'
               ' * SMILES: '
               'NC(=O)c1cc2cc(ccc2o1)N1CCN(CCCCc2c[nH]c3ccc(cc23)C#N)CC1 NAME: '
               'vilazodone REASON: CORRECT Contains nitrile group (R-C#N) per '
               'definition\n'
               ' * SMILES: N[C@@H](CCC(O)=O)C#N NAME: '
               '(S)-gamma-amino-gamma-cyanobutanoic acid REASON: CORRECT '
               'Contains nitrile group (R-C#N) per definition\n'
               ' * SMILES: '
               'O[C@](CN1N=CN=C1S)(C1=CC=C(F)C=C1F)C(F)(F)C1=CC=C(OC2=CC=C(C=C2)C#N)C=N1 '
               'NAME: (S)-fluoxytioconazole (thiol) REASON: CORRECT Contains '
               'nitrile group (R-C#N) per definition\n'
               ' * SMILES: '
               'CCS(=O)(=O)N1CCCCN2[C@@H](C1)[C@H]([C@@H]2CO)C3=CC=C(C=C3)C4=CC=CC(=C4)C#N '
               'NAME: '
               '3-[4-[(8R,9R,10R)-6-ethylsulfonyl-10-(hydroxymethyl)-1,6-diazabicyclo[6.2.0]decan-9-yl]phenyl]benzonitrile '
               'REASON: CORRECT Contains nitrile group (R-C#N) per definition\n'
               ' * SMILES: '
               'O1[C@@H]([C@H]([C@@H]([C@@H]1N2C(N=C(C=C2)NC(CCCCCCCCCCCCCCC)=O)=O)C#N)O)CO '
               'NAME: sapacitabine REASON: CORRECT Contains nitrile group '
               '(R-C#N) per definition\n'
               ' * SMILES: C1=CC=CC2=C1N3C(=C(N=C3C2=O)C#N)N NAME: '
               '3-amino-9-oxo-9H-imidazo[1,2-a]indole-2-carbonitrile REASON: '
               'CORRECT Contains nitrile group (R-C#N) per definition\n'
               ' * SMILES: '
               'CC1(C)[C@@H](\\C=C(/Cl)C(F)(F)F)[C@H]1C(=O)O[C@H](C#N)c1cccc(Oc2ccccc2)c1 '
               'NAME: gamma-cyhalothrin REASON: CORRECT Contains nitrile group '
               '(R-C#N) per definition\n'
               ' * SMILES: CO\\C=C(\\C(=O)OC)c1ccccc1Oc1cc(Oc2ccccc2C#N)ncn1 '
               'NAME: azoxystrobin REASON: CORRECT Contains nitrile group '
               '(R-C#N) per definition\n'
               ' * SMILES: '
               'C[C@H]1CN(S(=O)(=O)C2=C(C=C(C=C2)C3=CC=CC(=C3)C#N)O[C@H]1CN(C)CC4CC4)[C@H](C)CO '
               'NAME: '
               '3-[(4S,5R)-5-[[cyclopropylmethyl(methyl)amino]methyl]-2-[(2R)-1-hydroxypropan-2-yl]-4-methyl-1,1-dioxo-4,5-dihydro-3H-6,1$l^{6},2-benzoxathiazocin-8-yl]benzonitrile '
               'REASON: CORRECT Contains nitrile group (R-C#N) per definition\n'
               ' * SMILES: N#Cc1cnccn1 NAME: cyanopyrazine REASON: CORRECT '
               'Contains nitrile group (R-C#N) per definition\n'
               ' * SMILES: '
               'C=12C(=CC(=CC1)Cl)NC(NC2=O)=C(C(C=3C=CC(=CC3Cl)Cl)=O)C#N NAME: '
               'ciliobrevin D REASON: CORRECT Contains nitrile group (R-C#N) '
               'per definition\n'
               ' * SMILES: CCN(CC)CCCNC1=C(C(=CC(=N1)C)COC)C#N NAME: '
               '2-[3-(diethylamino)propylamino]-4-(methoxymethyl)-6-methyl-3-pyridinecarbonitrile '
               'REASON: CORRECT Contains nitrile group (R-C#N) per definition\n'
               ' * SMILES: '
               'C1CCN2[C@@H](CN(C1)C(=O)NC3=CC=CC=C3)[C@H]([C@@H]2CO)C4=CC=C(C=C4)C5=CC=CC(=C5)C#N '
               'NAME: '
               '(8R,9R,10R)-9-[4-(3-cyanophenyl)phenyl]-10-(hydroxymethyl)-N-phenyl-1,6-diazabicyclo[6.2.0]decane-6-carboxamide '
               'REASON: CORRECT Contains nitrile group (R-C#N) per definition\n'
               'False positives: SMILES: '
               'CC1=CC=C(C=C1)OCC(=O)NNC(=O)CSC2=NC=C(C(=N2)N)C#N NAME: '
               "N'-[2-[(4-amino-5-cyano-2-pyrimidinyl)thio]-1-oxoethyl]-2-(4-methylphenoxy)acetohydrazide "
               'REASON: WRONGLY CLASSIFIED Contains nitrile group (R-C#N) per '
               'definition\n'
               ' * SMILES: '
               'C[C@@H]1CN(C(=O)C2=CC=CC=C2C3=CC=CC=C3CO[C@@H]1CN(C)S(=O)(=O)C4=CC=C(C=C4)C#N)[C@H](C)CO '
               'NAME: LSM-30641 REASON: WRONGLY CLASSIFIED Contains nitrile '
               'group (R-C#N) per definition\n'
               ' * SMILES: S(C=1C=C(NC(=O)C1C#N)C=2OC=CC2)C NAME: '
               '6-(2-furyl)-2-hydroxy-4-(methylthio)nicotinonitrile REASON: '
               'WRONGLY CLASSIFIED Contains nitrile group (R-C#N) per '
               'definition\n'
               ' * SMILES: COC1=CC=C(C=C1)C2=NC(=C(O2)NCC3=CC=CO3)C#N NAME: '
               '5-(2-furanylmethylamino)-2-(4-methoxyphenyl)-4-oxazolecarbonitrile '
               'REASON: WRONGLY CLASSIFIED Contains nitrile group (R-C#N) per '
               'definition\n'
               ' * SMILES: C1=CC(=CC=C1C=C(C#N)C(=C(C#N)C#N)N)O NAME: '
               '2-amino-4-(4-hydroxyphenyl)buta-1,3-diene-1,1,3-tricarbonitrile '
               'REASON: WRONGLY CLASSIFIED Contains nitrile group (R-C#N) per '
               'definition\n'
               ' * SMILES: '
               'C[C@@H]1CN(C(=O)C2=C(N=CC(=C2)C3=CC=CC(=C3)C#N)O[C@H]1CN(C)C(=O)C4CCOCC4)[C@@H](C)CO '
               'NAME: '
               'N-[[(2R,3R)-8-(3-cyanophenyl)-5-[(2S)-1-hydroxypropan-2-yl]-3-methyl-6-oxo-3,4-dihydro-2H-pyrido[2,3-b][1,5]oxazocin-2-yl]methyl]-N-methyl-4-oxanecarboxamide '
               'REASON: WRONGLY CLASSIFIED Contains nitrile group (R-C#N) per '
               'definition\n'
               ' * SMILES: C1=CSC(=C1)C=C(C#N)C(=O)NC2=NC=CS2 NAME: '
               '2-cyano-N-(2-thiazolyl)-3-thiophen-2-yl-2-propenamide REASON: '
               'WRONGLY CLASSIFIED Contains nitrile group (R-C#N) per '
               'definition\n'
               ' * SMILES: '
               'CCCC#CC1=CC=C(C=C1)[C@@H]2[C@@H](N([C@H]2C#N)S(=O)(=O)C)CO '
               'NAME: '
               '(2R,3S,4R)-4-(hydroxymethyl)-1-methylsulfonyl-3-(4-pent-1-ynylphenyl)-2-azetidinecarbonitrile '
               'REASON: WRONGLY CLASSIFIED Contains nitrile group (R-C#N) per '
               'definition\n'
               ' * SMILES: '
               'C1=CC(=CN=C1)C2=NC(=C(C=C2)C#N)SCC3=CC(=C(C=C3)Cl)Cl NAME: '
               '2-[(3,4-dichlorophenyl)methylthio]-6-(3-pyridinyl)-3-pyridinecarbonitrile '
               'REASON: WRONGLY CLASSIFIED Contains nitrile group (R-C#N) per '
               'definition\n'
               ' * SMILES: O(C(=O)C=1C(=CC=CC1)C#N)C NAME: Methyl '
               '2-cyanobenzoate REASON: WRONGLY CLASSIFIED Contains nitrile '
               'group (R-C#N) per definition\n'
               ' * SMILES: '
               'C1CCC(C1)C(=O)N2[C@@H]([C@H]([C@H]2C#N)C3=CC=CC=C3)CO NAME: '
               '(2S,3S,4S)-1-[cyclopentyl(oxo)methyl]-4-(hydroxymethyl)-3-phenyl-2-azetidinecarbonitrile '
               'REASON: WRONGLY CLASSIFIED Contains nitrile group (R-C#N) per '
               'definition\n'
               ' * SMILES: '
               'C1C[C@@](CC[C@@]1(N2C[C@]([C@@](CC2)(C(=O)O)C=3C=CC=CC3)(C)[H])[H])(C#N)C4=CC=C(C=C4)F '
               'NAME: levocabastine REASON: WRONGLY CLASSIFIED Contains '
               'nitrile group (R-C#N) per definition\n'
               ' * SMILES: '
               'C1CCC2=C(C1)C(=C(S2)NC(=O)CSC3=NNC(=C4C=CC=CC4=O)N3C5=CC=CC=C5)C#N '
               'NAME: '
               'N-(3-cyano-4,5,6,7-tetrahydro-1-benzothiophen-2-yl)-2-[[5-(6-oxo-1-cyclohexa-2,4-dienylidene)-4-phenyl-1H-1,2,4-triazol-3-yl]thio]acetamide '
               'REASON: WRONGLY CLASSIFIED Contains nitrile group (R-C#N) per '
               'definition\n'
               ' * SMILES: CC(C)(C)C1=C(C(=CC(=C1)C=C(C#N)C#N)Br)O NAME: '
               '2-[(3-bromo-5-tert-butyl-4-hydroxyphenyl)methylidene]propanedinitrile '
               'REASON: WRONGLY CLASSIFIED Contains nitrile group (R-C#N) per '
               'definition\n'
               ' * SMILES: C1C(C(=C(NC1=O)SCC2=CC=CC=C2)C#N)C3=CC=CC=C3 NAME: '
               '2-oxo-4-phenyl-6-(phenylmethylthio)-3,4-dihydro-1H-pyridine-5-carbonitrile '
               'REASON: WRONGLY CLASSIFIED Contains nitrile group (R-C#N) per '
               'definition\n'
               ' * SMILES: '
               'C1=CC2=C(C=CC=N2)C(=C1)NC(=O)C(=CC3=CC=C(O3)C4=C(C=CC(=C4)Cl)Cl)C#N '
               'NAME: '
               '2-cyano-3-[5-(2,5-dichlorophenyl)-2-furanyl]-N-(5-quinolinyl)-2-propenamide '
               'REASON: WRONGLY CLASSIFIED Contains nitrile group (R-C#N) per '
               'definition\n'
               ' * SMILES: '
               'C1=CC=C(C=C1)[C@H]2[C@H](N([C@H]2C#N)C(=O)NC3=CC(=CC=C3)F)CO '
               'NAME: '
               '(2R,3R,4S)-2-cyano-N-(3-fluorophenyl)-4-(hydroxymethyl)-3-phenylazetidine-1-carboxamide '
               'REASON: WRONGLY CLASSIFIED Contains nitrile group (R-C#N) per '
               'definition\n'
               ' * SMILES: C1=CC2=C3C(=C1)C=CC4=C3C(=CC(=C4)CC#N)C=C2 NAME: '
               '2-(2-pyrenyl)acetonitrile REASON: WRONGLY CLASSIFIED Contains '
               'nitrile group (R-C#N) per definition\n'
               ' * SMILES: [O-][N+](=O)c1cc2[nH]c(=O)c(=O)[nH]c2cc1C#N NAME: '
               '6-Cyano-7-nitroquinoxaline-2,3-dione REASON: WRONGLY '
               'CLASSIFIED Contains nitrile group (R-C#N) per definition\n'
               ' * SMILES: '
               'COC1=C(C=C(C=C1)C2=NC(=C(C=C2)C#N)SCC(=O)NCC3=CC=CO3)OC NAME: '
               '2-[[3-cyano-6-(3,4-dimethoxyphenyl)-2-pyridinyl]thio]-N-(2-furanylmethyl)acetamide '
               'REASON: WRONGLY CLASSIFIED Contains nitrile group (R-C#N) per '
               'definition\n'
               ' * SMILES: '
               'C[C@H]1CN(C(=O)C2=CC=CC=C2C3=CC=CC=C3CO[C@@H]1CN(C)S(=O)(=O)C4=CC=C(C=C4)C#N)[C@H](C)CO '
               'NAME: LSM-30812 REASON: WRONGLY CLASSIFIED Contains nitrile '
               'group (R-C#N) per definition\n'
               ' * SMILES: O=C(N1C[C@H](N(C2=NC=NC=3NC=CC23)C)[C@H](CC1)C)CC#N '
               'NAME: (3r,4s)-Tofacitinib REASON: WRONGLY CLASSIFIED Contains '
               'nitrile group (R-C#N) per definition\n'
               ' * SMILES: '
               'ClC1=C2C(=CC(=C1)CC#N)[C@@]3(O[C@@H]4O[C@@H]([C@@](O)(C)C([C@H]4O)=O)C)[C@@H](O)C=CC3=C2 '
               'NAME: Cyanosporaside B REASON: WRONGLY CLASSIFIED Contains '
               'nitrile group (R-C#N) per definition\n'
               ' * SMILES: '
               'CN1CC[C@@H]2CC[C@@H]([C@H](O2)COC3=C(C=C(C=C3)C#N)C(=O)N(C[C@@H](CC1=O)C4=CC=CC=C4)C)OC '
               'NAME: LSM-40269 REASON: WRONGLY CLASSIFIED Contains nitrile '
               'group (R-C#N) per definition\n'
               ' * SMILES: CC1=C(C=CC(=C1)Cl)OC2=C(C=CC(=N2)C3=CC=C(C=C3)F)C#N '
               'NAME: '
               '2-(4-chloro-2-methylphenoxy)-6-(4-fluorophenyl)-3-pyridinecarbonitrile '
               'REASON: WRONGLY CLASSIFIED Contains nitrile group (R-C#N) per '
               'definition\n'
               'False negatives: SMILES: CN(Cc1ccc(Cl)nc1)C(C)=NC#N NAME: '
               'acetamiprid REASON: MISSED Does not contain nitrile group '
               '(R-C#N) per definition\n'
               ' * SMILES: Clc1ccc(CN2CCSC2=NC#N)cn1 NAME: thiacloprid REASON: '
               'MISSED Does not contain nitrile group (R-C#N) per definition\n'
               ' * SMILES: C=1(C=NC(=CC1)C(F)(F)F)[C@@H]([S@](C)(=NC#N)=O)C '
               'NAME: (SC,RS)-sulfoxaflor REASON: MISSED Does not contain '
               'nitrile group (R-C#N) per definition\n'
               ' * SMILES: C=1(C=NC(=CC1)C(F)(F)F)C(S(C)(=NC#N)=O)C NAME: '
               '[methyl(oxido){1-[6-(trifluoromethyl)pyridin-3-yl]ethyl}-lambda(6)-sulfanylidene]cyanamide '
               'REASON: MISSED Does not contain nitrile group (R-C#N) per '
               'definition\n'
               ' * SMILES: C=1(C=NC(=CC1)C(F)(F)F)[C@H]([S@@](C)(=NC#N)=O)C '
               'NAME: (RC,SS)-sulfoxaflor REASON: MISSED Does not contain '
               'nitrile group (R-C#N) per definition\n'
               ' * SMILES: '
               'Nc1ccc(cc1)C(=O)NCCN\\C(NCCCOc1cccc(CN2CCCCC2)c1)=N\\C#N NAME: '
               'aminopotentidine REASON: MISSED Does not contain nitrile group '
               '(R-C#N) per definition\n'
               ' * SMILES: N#C[Fe]C#N NAME: Fe(CN)2 REASON: MISSED Does not '
               'contain nitrile group (R-C#N) per definition\n'
               ' * SMILES: CN(Cc1ccc(Cl)nc1)C(\\C)=N/C#N NAME: (Z)-acetamiprid '
               'REASON: MISSED Does not contain nitrile group (R-C#N) per '
               'definition\n'
               ' * SMILES: Clc1ccc(CN2CCS\\C2=N/C#N)cn1 NAME: (Z)-thiacloprid '
               'REASON: MISSED Does not contain nitrile group (R-C#N) per '
               'definition\n'
               ' * SMILES: NC#N NAME: cyanamide REASON: MISSED Does not '
               'contain nitrile group (R-C#N) per definition\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'NCCO[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@@H]1O[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@@H]1O[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@@H]1O',
                                     'name': 'beta-D-Manp-(1->2)-beta-D-Manp-(1->2)-beta-D-Manp-O[CH2]2NH2',
                                     'reason': 'Does not contain nitrile group '
                                               '(R-C#N) per definition'},
                                 {   'smiles': '[H][C@@]12CCC(C)=C[C@@]1([H])C(C)(C)CCCC2=C',
                                     'name': '(1R,6R)-alpha-himachalene',
                                     'reason': 'Does not contain nitrile group '
                                               '(R-C#N) per definition'},
                                 {   'smiles': 'OC1(C2C(CC1OC(=O)C)C(=COC2OC(=O)CC(C)C)COC(=O)CC(C)C)COC(=O)CC(C)C',
                                     'name': '[6-Acetyloxy-7-hydroxy-1-(3-methylbutanoyloxy)-7-(3-methylbutanoyloxymethyl)-4a,5,6,7a-tetrahydro-1H-cyclopenta[c]pyran-4-yl]methyl '
                                             '3-methylbutanoate',
                                     'reason': 'Does not contain nitrile group '
                                               '(R-C#N) per definition'},
                                 {   'smiles': 'O([C@H]1[C@H](O)[C@H](O[C@@H](O[C@H]2[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]2CO)O[C@H]3[C@H](O)[C@@H](NC(=O)C)C(O[C@@H]3CO)O)[C@H]1O)CO[C@H]4O[C@@H]([C@@H](O)[C@H](O)[C@@H]4O[C@@H]5O[C@@H]([C@@H](O[C@@H]6O[C@@H]([C@H](O)[C@H](O)[C@H]6O)CO)[C@H](O)[C@H]5NC(=O)C)CO)CO[C@@H]7O[C@@H]([C@@H](O[C@@H]8O[C@@H]([C@H](O)[C@H](O)[C@H]8O)CO)[C@H](O)[C@H]7NC(=O)C)CO)[C@H]9O[C@@H]([C@@H](O)[C@H](O)[C@@H]9O[C@@H]%10O[C@@H]([C@@H](O[C@@H]%11O[C@@H]([C@H](O)[C@H](O)[C@H]%11O[C@@H]%12O[C@H]([C@@H](O)[C@@H](O)[C@@H]%12O)C)CO)[C@H](O)[C@H]%10NC(=O)C)CO)CO',
                                     'name': 'N-[(3R,4R,5S,6R)-5-[(2S,3R,4R,5S,6R)-3-Acetamido-5-[(2S,3S,4S,5R,6R)-4-[(2R,3S,4S,5S,6R)-3-[(2S,3R,4R,5S,6R)-3-acetamido-5-[(2S,3R,4S,5R,6R)-4,5-dihydroxy-6-(hydroxymethyl)-3-[(2S,3S,4R,5S,6S)-3,4,5-trihydroxy-6-methyloxan-2-yl]oxyoxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-6-[[(2S,3S,4S,5S,6R)-3-[(2R,3R,4R,5S,6R)-3-acetamido-4-hydroxy-6-(hydroxymethyl)-5-[(2S,3R,4S,5R,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-6-[[(2R,3R,4R,5S,6R)-3-acetamido-4-hydroxy-6-(hydroxymethyl)-5-[(2S,3R,4S,5R,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxymethyl]-4,5-dihydroxyoxan-2-yl]oxymethyl]-3,5-dihydroxyoxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-2,4-dihydroxy-6-(hydroxymethyl)oxan-3-yl]acetamide',
                                     'reason': 'Does not contain nitrile group '
                                               '(R-C#N) per definition'},
                                 {   'smiles': 'OC(=O)C(N)C=C',
                                     'name': '2-Amino-3-butenoic acid',
                                     'reason': 'Does not contain nitrile group '
                                               '(R-C#N) per definition'},
                                 {   'smiles': 'O1[C@@H](N2C=C(C(=O)NC2=O)CO)[C@H](O)[C@H](O)[C@H]1CO',
                                     'name': '5-Hydroxymethyluridine',
                                     'reason': 'Does not contain nitrile group '
                                               '(R-C#N) per definition'},
                                 {   'smiles': 'C1C[C@H]([C@H](O[C@H]1CC(=O)N2CCC3=CC=CC=C3C2)CO)NC(=O)C4CCOCC4',
                                     'name': 'N-[(2S,3R,6R)-6-[2-(3,4-dihydro-1H-isoquinolin-2-yl)-2-oxoethyl]-2-(hydroxymethyl)-3-oxanyl]-4-oxanecarboxamide',
                                     'reason': 'Does not contain nitrile group '
                                               '(R-C#N) per definition'},
                                 {   'smiles': 'O(C(C(O)COC=1C=2OC=CC2C=C3C1OC(=O)C=C3)(C)C)C(=O)/C(/C)=C\\C',
                                     'name': 'Tomasin',
                                     'reason': 'Does not contain nitrile group '
                                               '(R-C#N) per definition'},
                                 {   'smiles': 'C([C@H](N)C(=O)O)SS',
                                     'name': '3-disulfanyl-L-alanine',
                                     'reason': 'Does not contain nitrile group '
                                               '(R-C#N) per definition'},
                                 {   'smiles': 'O=C(N[C@@H]([C@H](CC)C)C(O)=O)[C@@H](NC(=O)[C@@H](N)CO)C(C)C',
                                     'name': 'Ser-Val-Ile',
                                     'reason': 'Does not contain nitrile group '
                                               '(R-C#N) per definition'}],
    'sample_false_negatives': [   {   'smiles': 'N#C[Fe]C#N',
                                      'name': 'Fe(CN)2',
                                      'reason': 'Contains metal or disallowed '
                                                'atoms; likely not an organic '
                                                'nitrile'}],
    'attempt': 3,
    'reasoning': 'After analyzing the previous program and the outcomes, I '
                 'observed that the nitrile SMARTS pattern `"[#6][C]#[N]"` '
                 'used in the previous code is too restrictive. It only '
                 'matches nitrile groups where the nitrile carbon is connected '
                 'to a carbon atom, excluding cases where the nitrile carbon '
                 'is connected to heteroatoms such as nitrogen or sulfur, as '
                 'seen in compounds like acetamiprid and sulfoxaflor. \n'
                 '\n'
                 'According to the definition, a nitrile is a compound having '
                 'the structure RC≡N, and the suffix nitrile denotes the '
                 'triply bound `#N` atom, not necessarily the carbon atom '
                 'attached to it. Therefore, any compound containing a nitrile '
                 'group (`C≡N`) should be considered a nitrile, regardless of '
                 'what atom the nitrile carbon is attached to (except '
                 'hydrogen).\n'
                 '\n'
                 'To improve the program, I will:\n'
                 '- Modify the nitrile SMARTS pattern to `"[!#1][C]#[N]"` to '
                 'match any nitrile group where the nitrile carbon is attached '
                 'to any atom except hydrogen.\n'
                 '- Exclude inorganic compounds by ensuring that the molecule '
                 'does not contain any metal atoms. I will define a set of '
                 'allowed elements commonly found in organic molecules and '
                 'check that the molecule only contains these elements.\n'
                 '\n'
                 'Here is the improved code:',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 516,
    'num_false_positives': 1674,
    'num_true_negatives': 140109,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.2356164383561644,
    'recall': 0.9980657640232108,
    'f1': 0.38123383819726636,
    'accuracy': 0.9882290934645116,
    'negative_predictive_value': 0.9999928627506959}