"""
Classifies: CHEBI:13248 anilide
"""
"""
Classifies: anilide
"""
from rdkit import Chem

def is_anilide(smiles: str):
    """
    Determines if a molecule is an anilide based on its SMILES string.
    An anilide is any aromatic amide obtained by acylation of aniline,
    meaning it has an amide group where the nitrogen is directly attached
    to a benzene ring (aromatic ring of six carbons).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is an anilide, False otherwise
        str: Reason for classification
    """
    
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
    
    # Define SMARTS pattern for anilide
    # Pattern explanation:
    # - [NX3H]: Amide nitrogen (three-coordinate nitrogen with one hydrogen)
    # - [CX3](=O): Carbonyl carbon (double-bonded to oxygen)
    # - [$(c1ccccc1)]: Benzene ring (six aromatic carbons in a ring)
    anilide_pattern = Chem.MolFromSmarts("[#6;a]1:[#6;a]:[#6;a]:[#6;a]:[#6;a]:[#6;a]:1[NX3H1][CX3](=O)[#6]")
    
    if mol.HasSubstructMatch(anilide_pattern):
        return True, "Contains an anilide moiety (amide nitrogen attached to benzene ring)"
    else:
        return False, "Does not contain an anilide moiety"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:13248',
                          'name': 'anilide',
                          'definition': 'Any aromatic amide obtained by '
                                        'acylation of aniline.',
                          'parents': ['CHEBI:22712', 'CHEBI:62733'],
                          'xrefs': [   'KEGG:C01402',
                                       'PMID:23535982',
                                       'PMID:23968552',
                                       'PMID:24273122',
                                       'PMID:6205897'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 25,
                           'log_lines_of_code': 3.2188758248682006,
                           'indent_by_line': [   1,
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
                                                 2,
                                                 1,
                                                 2],
                           'max_indent': 2,
                           'imports': ['from rdkit import Chem'],
                           'imports_count': 1,
                           'methods_called': [   'HasSubstructMatch',
                                                 'MolFromSmarts',
                                                 'MolFromSmiles'],
                           'methods_called_count': 3,
                           'smarts_strings': [   '[#6;a]1:[#6;a]:[#6;a]:[#6;a]:[#6;a]:[#6;a]:1[NX3H1][CX3](=O)[#6]'],
                           'smarts_strings_count': 1,
                           'defs': ['is_anilide(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'True, "Contains an anilide moiety '
                                          '(amide nitrogen attached to benzene '
                                          'ring)"',
                                          'False, "Does not contain an anilide '
                                          'moiety"'],
                           'returns_count': 3,
                           'complexity': 2.44377516497364},
    'message': '\n'
               'Attempt failed: F1 score of 0.04228222109016811 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: '
               'ClC1=C(O)C(NC(=O)/C(=C/C(=C/[C@@H](CCCC)C)/C)/C)=CC(=C1/C=C/C=C/C=C/C(=O)NC2=C(O)CCC2=O)O '
               'NAME: Chinikomycin A REASON: CORRECT Contains an anilide '
               'moiety (amide nitrogen attached to benzene ring)\n'
               ' * SMILES: CC1=C(C=C(C=C1)NC(=O)C2CCCN(C2)C3=NC=CC=N3)F NAME: '
               'N-(3-fluoro-4-methylphenyl)-1-(2-pyrimidinyl)-3-piperidinecarboxamide '
               'REASON: CORRECT Contains an anilide moiety (amide nitrogen '
               'attached to benzene ring)\n'
               ' * SMILES: '
               'CC1=C(C=C(C=C1)NC(=O)COC2=C(C=C(C=C2)C=NNC(=S)N)OC)C NAME: '
               '2-[4-[(carbamothioylhydrazinylidene)methyl]-2-methoxyphenoxy]-N-(3,4-dimethylphenyl)acetamide '
               'REASON: CORRECT Contains an anilide moiety (amide nitrogen '
               'attached to benzene ring)\n'
               ' * SMILES: COC1=CC=CC=C1NC(=O)CSC(=O)N NAME: carbamothioic '
               'acid S-[2-(2-methoxyanilino)-2-oxoethyl] ester REASON: CORRECT '
               'Contains an anilide moiety (amide nitrogen attached to benzene '
               'ring)\n'
               ' * SMILES: '
               'C1=CC(=C(C(=C1)Cl)CC(=O)OCC(=O)NC2=CC=C(C=C2)OC(F)(F)F)Cl '
               'NAME: 2-(2,6-dichlorophenyl)acetic acid '
               '[2-oxo-2-[4-(trifluoromethoxy)anilino]ethyl] ester REASON: '
               'CORRECT Contains an anilide moiety (amide nitrogen attached to '
               'benzene ring)\n'
               ' * SMILES: CC1=CC(=CC(=C1)NC(=O)CN2C(=CC(=C(C2=O)C#N)COC)C)C '
               'NAME: '
               '2-[3-cyano-4-(methoxymethyl)-6-methyl-2-oxo-1-pyridinyl]-N-(3,5-dimethylphenyl)acetamide '
               'REASON: CORRECT Contains an anilide moiety (amide nitrogen '
               'attached to benzene ring)\n'
               ' * SMILES: Cc1nc(C)c(s1)C(=O)Nc1ccccc1 NAME: Metsulfovax '
               'REASON: CORRECT Contains an anilide moiety (amide nitrogen '
               'attached to benzene ring)\n'
               ' * SMILES: CCC1=CC=C(C=C1)NC(=O)CCN2C=CC=C2 NAME: '
               'N-(4-ethylphenyl)-3-(1-pyrrolyl)propanamide REASON: CORRECT '
               'Contains an anilide moiety (amide nitrogen attached to benzene '
               'ring)\n'
               ' * SMILES: '
               'C1=C(C=C(C=C1Cl)NC(CSC=2N=C(C=CN2)C=3N=C(SC3)C4=CC=CC=C4)=O)Cl '
               'NAME: '
               'N-(3,5-Dichlorophenyl)-2-[4-(2-phenyl-1,3-thiazol-4-yl)pyrimidin-2-yl]sulfanylacetamide '
               'REASON: CORRECT Contains an anilide moiety (amide nitrogen '
               'attached to benzene ring)\n'
               ' * SMILES: CC(=O)NC1=CC=C(C=C1)CC(=O)O NAME: Actarit REASON: '
               'CORRECT Contains an anilide moiety (amide nitrogen attached to '
               'benzene ring)\n'
               ' * SMILES: O=C(NC1=CC=C(C2CCCCC2)C=C1)C=CC(O)=O NAME: '
               '4-(4-Cyclohexylanilino)-4-oxobut-2-enoic acid REASON: CORRECT '
               'Contains an anilide moiety (amide nitrogen attached to benzene '
               'ring)\n'
               ' * SMILES: '
               'CN1[C@@H]2CC[C@@H](O[C@@H]2COC3=C(C1=O)C=C(C=C3)NC(=O)C4CCOCC4)CC(=O)NC5=CC(=CC=C5)OC '
               'NAME: '
               'N-[(2R,4aR,12aS)-2-[2-(3-methoxyanilino)-2-oxoethyl]-5-methyl-6-oxo-2,3,4,4a,12,12a-hexahydropyrano[2,3-c][1,5]benzoxazocin-8-yl]-4-oxanecarboxamide '
               'REASON: CORRECT Contains an anilide moiety (amide nitrogen '
               'attached to benzene ring)\n'
               ' * SMILES: '
               'CC1=CC(=CC=C1)NC(=O)COC2=CC=C(C=C2)C=CC3=C(C(=O)NC(=O)N3)[N+](=O)[O-] '
               'NAME: '
               'N-(3-methylphenyl)-2-[4-[2-(5-nitro-2,4-dioxo-1H-pyrimidin-6-yl)ethenyl]phenoxy]acetamide '
               'REASON: CORRECT Contains an anilide moiety (amide nitrogen '
               'attached to benzene ring)\n'
               ' * SMILES: C1=CC(=CC(=C1)Cl)NC(=O)C(=CC2=CN=CC=C2)C#N NAME: '
               'N-(3-chlorophenyl)-2-cyano-3-(3-pyridinyl)-2-propenamide '
               'REASON: CORRECT Contains an anilide moiety (amide nitrogen '
               'attached to benzene ring)\n'
               ' * SMILES: '
               'CN(C)C1=CC=C(C=C1)C=C2CCCC(=C2N3CCOCC3)C(=O)NC4=CC(=C(C(=C4)OC)OC)OC '
               'NAME: '
               '3-[[4-(dimethylamino)phenyl]methylidene]-2-(4-morpholinyl)-N-(3,4,5-trimethoxyphenyl)-1-cyclohexenecarboxamide '
               'REASON: CORRECT Contains an anilide moiety (amide nitrogen '
               'attached to benzene ring)\n'
               ' * SMILES: CC1=C(C=C(C=C1)NC(=O)COC2=CC=CC=C2C=O)Cl NAME: '
               'N-(3-chloro-4-methylphenyl)-2-(2-formylphenoxy)acetamide '
               'REASON: CORRECT Contains an anilide moiety (amide nitrogen '
               'attached to benzene ring)\n'
               ' * SMILES: '
               'O=C(OC)/C=C/C(=C/C(C(O)C1=C(O)C(NC(=O)C)=CC(=C1)O)C)/C NAME: '
               'NFAT-68 REASON: CORRECT Contains an anilide moiety (amide '
               'nitrogen attached to benzene ring)\n'
               ' * SMILES: O=C(NC1=C(O)C=C(COC)C(=C1)O)C NAME: '
               '2,5-Dihydroxy-4-methoxymethyl-acetanilide REASON: CORRECT '
               'Contains an anilide moiety (amide nitrogen attached to benzene '
               'ring)\n'
               ' * SMILES: O(C(C)(C)C)C1=CC=C(C=C1)NC(C)=O NAME: butacetin '
               'REASON: CORRECT Contains an anilide moiety (amide nitrogen '
               'attached to benzene ring)\n'
               ' * SMILES: CC(=NNC(=O)C1=CC2=C(C=C1)OCO2)C3=CC(=CC=C3)NC(=O)C '
               'NAME: '
               'N-[1-(3-acetamidophenyl)ethylideneamino]-1,3-benzodioxole-5-carboxamide '
               'REASON: CORRECT Contains an anilide moiety (amide nitrogen '
               'attached to benzene ring)\n'
               ' * SMILES: '
               'CCCNC(=O)NC1=CC2=C(C=C1)OC[C@@H]3[C@H](CC[C@@H](O3)CC(=O)NC4=CC=CC=C4C)N(C2=O)C '
               'NAME: '
               '2-[(2R,4aS,12aS)-5-methyl-6-oxo-8-(propylcarbamoylamino)-2,3,4,4a,12,12a-hexahydropyrano[2,3-c][1,5]benzoxazocin-2-yl]-N-(2-methylphenyl)acetamide '
               'REASON: CORRECT Contains an anilide moiety (amide nitrogen '
               'attached to benzene ring)\n'
               ' * SMILES: CC1=CC(=C(C(=C1)C)NC(=O)CC(=NNC(=O)OC(C)(C)C)C)C '
               'NAME: '
               'N-[[4-oxo-4-(2,4,6-trimethylanilino)butan-2-ylidene]amino]carbamic '
               'acid tert-butyl ester REASON: CORRECT Contains an anilide '
               'moiety (amide nitrogen attached to benzene ring)\n'
               ' * SMILES: '
               'N(C(COC1=CC=C(C=C1)OCCCC)=O)(CCN(CC)CC)C2=C(OCC)C=CC(=C2)OCC '
               'NAME: fenoxedil REASON: CORRECT Contains an anilide moiety '
               '(amide nitrogen attached to benzene ring)\n'
               ' * SMILES: CCN1C(=NN=C1SCC(=O)NC2=CC=C(C=C2)NC(=O)C)C3CC3 '
               'NAME: '
               'N-(4-acetamidophenyl)-2-[(5-cyclopropyl-4-ethyl-1,2,4-triazol-3-yl)thio]acetamide '
               'REASON: CORRECT Contains an anilide moiety (amide nitrogen '
               'attached to benzene ring)\n'
               ' * SMILES: C1COC(=CO1)C(=O)OCC(=O)NC2=CC=C(C=C2)C#N NAME: '
               '2,3-dihydro-1,4-dioxin-5-carboxylic acid '
               '[2-(4-cyanoanilino)-2-oxoethyl] ester REASON: CORRECT Contains '
               'an anilide moiety (amide nitrogen attached to benzene ring)\n'
               'False positives: SMILES: '
               'CC1=CC(=CC=C1)S(=O)(=O)N[C@@H]2CC[C@H](O[C@@H]2CO)CCNC(=O)NC3=C(C=CC(=C3)F)F '
               'NAME: '
               '1-(2,5-difluorophenyl)-3-[2-[(2S,5R,6S)-6-(hydroxymethyl)-5-[(3-methylphenyl)sulfonylamino]-2-oxanyl]ethyl]urea '
               'REASON: WRONGLY CLASSIFIED Contains an anilide moiety (amide '
               'nitrogen attached to benzene ring)\n'
               ' * SMILES: '
               'C[C@@H]1CN(C(=O)C2=C(C=CC(=C2)NC(=O)NC3=CC4=C(C=C3)OCO4)O[C@H]1CN(C)CC5CCCCC5)[C@@H](C)CO '
               'NAME: '
               '1-(1,3-benzodioxol-5-yl)-3-[(2R,3R)-2-[[cyclohexylmethyl(methyl)amino]methyl]-5-[(2S)-1-hydroxypropan-2-yl]-3-methyl-6-oxo-3,4-dihydro-2H-1,5-benzoxazocin-8-yl]urea '
               'REASON: WRONGLY CLASSIFIED Contains an anilide moiety (amide '
               'nitrogen attached to benzene ring)\n'
               ' * SMILES: '
               'CCC(=O)NC1=CC2=C(C=C1)C(=O)N(C[C@@H]([C@@H](CN([C@@H](CO2)C)C(=O)COC)C)OC)C '
               'NAME: '
               'N-[(5R,6R,9R)-5-methoxy-8-(2-methoxy-1-oxoethyl)-3,6,9-trimethyl-2-oxo-11-oxa-3,8-diazabicyclo[10.4.0]hexadeca-1(12),13,15-trien-14-yl]propanamide '
               'REASON: WRONGLY CLASSIFIED Contains an anilide moiety (amide '
               'nitrogen attached to benzene ring)\n'
               ' * SMILES: '
               'COc1cc2CCN(C(=O)Nc3cc(F)cc(c3)-c3cccnc3)c2cc1C(F)(F)F NAME: SB '
               '228357 REASON: WRONGLY CLASSIFIED Contains an anilide moiety '
               '(amide nitrogen attached to benzene ring)\n'
               ' * SMILES: '
               'CCC(=O)NC1=CC2=C(C=C1)C(=O)N(C[C@@H]([C@@H](CN([C@@H](CO2)C)CC3CCCCC3)C)OC)C '
               'NAME: '
               'N-[(5R,6R,9R)-8-(cyclohexylmethyl)-5-methoxy-3,6,9-trimethyl-2-oxo-11-oxa-3,8-diazabicyclo[10.4.0]hexadeca-1(12),13,15-trien-14-yl]propanamide '
               'REASON: WRONGLY CLASSIFIED Contains an anilide moiety (amide '
               'nitrogen attached to benzene ring)\n'
               ' * SMILES: '
               'C1CCC(CC1)NC(=O)NC2=CC3=C(C=C2)O[C@H]4[C@@H]3C[C@H](O[C@@H]4CO)CC(=O)NCC5=CN=CC=C5 '
               'NAME: '
               '2-[(1R,3S,4aR,9aS)-6-[[(cyclohexylamino)-oxomethyl]amino]-1-(hydroxymethyl)-3,4,4a,9a-tetrahydro-1H-pyrano[3,4-b]benzofuran-3-yl]-N-(3-pyridinylmethyl)acetamide '
               'REASON: WRONGLY CLASSIFIED Contains an anilide moiety (amide '
               'nitrogen attached to benzene ring)\n'
               ' * SMILES: Cc1cccc(C)c1NC(=O)c1ccc(N)cc1 NAME: LY201116 '
               'REASON: WRONGLY CLASSIFIED Contains an anilide moiety (amide '
               'nitrogen attached to benzene ring)\n'
               ' * SMILES: '
               'CCCN(C)C[C@H]1[C@H](CN(C(=O)C2=C(C=CC(=C2)NC(=O)NC(C)C)O[C@@H](CCCCO1)C)[C@H](C)CO)C '
               'NAME: '
               '1-[(3R,9R,10S)-12-[(2R)-1-hydroxypropan-2-yl]-3,10-dimethyl-9-[[methyl(propyl)amino]methyl]-13-oxo-2,8-dioxa-12-azabicyclo[12.4.0]octadeca-1(14),15,17-trien-16-yl]-3-propan-2-ylurea '
               'REASON: WRONGLY CLASSIFIED Contains an anilide moiety (amide '
               'nitrogen attached to benzene ring)\n'
               ' * SMILES: '
               'CCOC1=CC=C(C=C1)N(CC(=O)NC2=CC=CC=C2OC)S(=O)(=O)C3=CC=CC=C3 '
               'NAME: '
               '2-[N-(benzenesulfonyl)-4-ethoxyanilino]-N-(2-methoxyphenyl)acetamide '
               'REASON: WRONGLY CLASSIFIED Contains an anilide moiety (amide '
               'nitrogen attached to benzene ring)\n'
               ' * SMILES: '
               'CC1=C(N=C2N1C=CC=N2)C3=CC(=CC=C3)NC(=O)C4=C(ON=C4C5=CC=CC=C5Cl)C '
               'NAME: '
               '3-(2-chlorophenyl)-5-methyl-N-[3-(3-methyl-2-imidazo[1,2-a]pyrimidinyl)phenyl]-4-isoxazolecarboxamide '
               'REASON: WRONGLY CLASSIFIED Contains an anilide moiety (amide '
               'nitrogen attached to benzene ring)\n'
               ' * SMILES: '
               'C[C@H]1CN([C@@H](COC2=C(C=CC(=C2)NC(=O)C)C(=O)N(C[C@@H]1OC)C)C)CC3=CN=CN=C3 '
               'NAME: '
               'N-[(5R,6S,9R)-5-methoxy-3,6,9-trimethyl-2-oxo-8-(5-pyrimidinylmethyl)-11-oxa-3,8-diazabicyclo[10.4.0]hexadeca-1(12),13,15-trien-14-yl]acetamide '
               'REASON: WRONGLY CLASSIFIED Contains an anilide moiety (amide '
               'nitrogen attached to benzene ring)\n'
               ' * SMILES: '
               'C[C@@H]1CN(C(=O)C2=C(C(=CC=C2)N(C)C)O[C@@H]1CN(C)CC3=CC=C(C=C3)C(=O)NC4=CC=CC=C4N)[C@H](C)CO '
               'NAME: '
               'N-(2-aminophenyl)-4-[[[(2S,3R)-10-(dimethylamino)-5-[(2R)-1-hydroxypropan-2-yl]-3-methyl-6-oxo-3,4-dihydro-2H-1,5-benzoxazocin-2-yl]methyl-methylamino]methyl]benzamide '
               'REASON: WRONGLY CLASSIFIED Contains an anilide moiety (amide '
               'nitrogen attached to benzene ring)\n'
               ' * SMILES: '
               'C1CC1CC(=O)NC2=CC3=C(C=C2)O[C@@H]4[C@H]3C[C@@H](O[C@@H]4CO)CC(=O)NCC(F)(F)F '
               'NAME: '
               'N-[(1R,3R,4aS,9aR)-1-(hydroxymethyl)-3-[2-oxo-2-(2,2,2-trifluoroethylamino)ethyl]-3,4,4a,9a-tetrahydro-1H-pyrano[3,4-b]benzofuran-6-yl]-2-cyclopropylacetamide '
               'REASON: WRONGLY CLASSIFIED Contains an anilide moiety (amide '
               'nitrogen attached to benzene ring)\n'
               ' * SMILES: '
               'C[C@@H]1CN[C@@H](COC2=C(C=C(C=C2)NC(=O)C3=CC=C(C=C3)OC4=CC=CC=C4)C(=O)N(C[C@H]1OC)C)C '
               'NAME: '
               'N-[(4R,7R,8S)-8-methoxy-4,7,10-trimethyl-11-oxo-2-oxa-5,10-diazabicyclo[10.4.0]hexadeca-1(12),13,15-trien-14-yl]-4-phenoxybenzamide '
               'REASON: WRONGLY CLASSIFIED Contains an anilide moiety (amide '
               'nitrogen attached to benzene ring)\n'
               ' * SMILES: '
               'COC1=CC=C(C=C1)NC(=O)N[C@H]2CC[C@H](O[C@H]2CO)CCNC(=O)CCN3CCCCC3 '
               'NAME: '
               'N-[2-[(2S,5S,6R)-6-(hydroxymethyl)-5-[[(4-methoxyanilino)-oxomethyl]amino]-2-oxanyl]ethyl]-3-(1-piperidinyl)propanamide '
               'REASON: WRONGLY CLASSIFIED Contains an anilide moiety (amide '
               'nitrogen attached to benzene ring)\n'
               ' * SMILES: '
               'C[C@H]1CN(C(=O)C2=C(C(=CC=C2)NC(=O)C3CCOCC3)O[C@H]1CN(C)C(=O)NC4=CC=CC5=CC=CC=C54)[C@H](C)CO '
               'NAME: '
               'N-[(2R,3S)-5-[(2R)-1-hydroxypropan-2-yl]-3-methyl-2-[[methyl-[(1-naphthalenylamino)-oxomethyl]amino]methyl]-6-oxo-3,4-dihydro-2H-1,5-benzoxazocin-10-yl]-4-oxanecarboxamide '
               'REASON: WRONGLY CLASSIFIED Contains an anilide moiety (amide '
               'nitrogen attached to benzene ring)\n'
               ' * SMILES: '
               'C1CCC(C1)NC(=O)NC2=CC3=C(C=C2)O[C@H]4[C@@H]3C[C@@H](O[C@H]4CO)CC(=O)NCC5=CC=CC=C5F '
               'NAME: '
               '2-[(1S,3R,4aR,9aS)-6-[[(cyclopentylamino)-oxomethyl]amino]-1-(hydroxymethyl)-3,4,4a,9a-tetrahydro-1H-pyrano[3,4-b]benzofuran-3-yl]-N-[(2-fluorophenyl)methyl]acetamide '
               'REASON: WRONGLY CLASSIFIED Contains an anilide moiety (amide '
               'nitrogen attached to benzene ring)\n'
               ' * SMILES: '
               'CCN1CCN(CC1)C(=O)CC2=CC=C(C=C2)NC3=NC=C(C(=N3)NC4=CC=C(C=C4)C(=O)NC5=CC=CC=C5Cl)F '
               'NAME: '
               'N-(2-chlorophenyl)-4-[[2-[4-[2-(4-ethyl-1-piperazinyl)-2-oxoethyl]anilino]-5-fluoro-4-pyrimidinyl]amino]benzamide '
               'REASON: WRONGLY CLASSIFIED Contains an anilide moiety (amide '
               'nitrogen attached to benzene ring)\n'
               ' * SMILES: '
               'C[C@H]1CN[C@@H](COC2=C(C=CC(=C2)NC(=O)NC3=CC(=CC=C3)F)C(=O)N(C[C@@H]1OC)C)C '
               'NAME: '
               '1-(3-fluorophenyl)-3-[(5R,6S,9R)-5-methoxy-3,6,9-trimethyl-2-oxo-11-oxa-3,8-diazabicyclo[10.4.0]hexadeca-1(12),13,15-trien-14-yl]urea '
               'REASON: WRONGLY CLASSIFIED Contains an anilide moiety (amide '
               'nitrogen attached to benzene ring)\n'
               ' * SMILES: '
               'C[C@H]1CCCCO[C@@H]([C@@H](CN(C(=O)C2=C(O1)C=CC(=C2)NC(=O)C3=CC=CC=C3)[C@@H](C)CO)C)CN(C)C(=O)NC(C)C '
               'NAME: '
               'N-[(3S,9S,10R)-12-[(2S)-1-hydroxypropan-2-yl]-3,10-dimethyl-9-[[methyl-[oxo-(propan-2-ylamino)methyl]amino]methyl]-13-oxo-2,8-dioxa-12-azabicyclo[12.4.0]octadeca-1(14),15,17-trien-16-yl]benzamide '
               'REASON: WRONGLY CLASSIFIED Contains an anilide moiety (amide '
               'nitrogen attached to benzene ring)\n'
               ' * SMILES: '
               'CCC(=O)N[C@H]1CC[C@@H](O[C@@H]1CO)CCNC(=O)NC2=CC=C(C=C2)C(F)(F)F '
               'NAME: '
               'N-[(2S,3S,6R)-2-(hydroxymethyl)-6-[2-[[oxo-[4-(trifluoromethyl)anilino]methyl]amino]ethyl]-3-oxanyl]propanamide '
               'REASON: WRONGLY CLASSIFIED Contains an anilide moiety (amide '
               'nitrogen attached to benzene ring)\n'
               ' * SMILES: '
               'C[C@H]1CCCCO[C@H]([C@H](CN(C(=O)C2=C(O1)C=CC(=C2)NC(=O)C3=CC=NC=C3)[C@@H](C)CO)C)CN(C)C(=O)C4CCCCC4 '
               'NAME: '
               'N-[(3S,9R,10S)-9-[[[cyclohexyl(oxo)methyl]-methylamino]methyl]-12-[(2S)-1-hydroxypropan-2-yl]-3,10-dimethyl-13-oxo-2,8-dioxa-12-azabicyclo[12.4.0]octadeca-1(14),15,17-trien-16-yl]-4-pyridinecarboxamide '
               'REASON: WRONGLY CLASSIFIED Contains an anilide moiety (amide '
               'nitrogen attached to benzene ring)\n'
               ' * SMILES: '
               'C[C@@H]1CCCCO[C@H]([C@@H](CN(C(=O)C2=C(O1)C=CC(=C2)NC(=O)NC3=C(ON=C3C)C)[C@H](C)CO)C)CN(C)C '
               'NAME: '
               '1-[(3R,9R,10R)-9-[(dimethylamino)methyl]-12-[(2R)-1-hydroxypropan-2-yl]-3,10-dimethyl-13-oxo-2,8-dioxa-12-azabicyclo[12.4.0]octadeca-1(14),15,17-trien-16-yl]-3-(3,5-dimethyl-4-isoxazolyl)urea '
               'REASON: WRONGLY CLASSIFIED Contains an anilide moiety (amide '
               'nitrogen attached to benzene ring)\n'
               ' * SMILES: CCOCN(C(=O)CS(O)(=O)=O)c1c(C)cccc1CC NAME: '
               'acetochlor ESA REASON: WRONGLY CLASSIFIED Contains an anilide '
               'moiety (amide nitrogen attached to benzene ring)\n'
               ' * SMILES: '
               'CN(C)C(=O)C[C@@H]1C[C@H]2[C@@H]([C@@H](O1)CO)OC3=C2C=C(C=C3)NC(=O)C4=CC5=C(C=C4)OCO5 '
               'NAME: '
               'N-[(1S,3S,4aR,9aS)-3-[2-(dimethylamino)-2-oxoethyl]-1-(hydroxymethyl)-3,4,4a,9a-tetrahydro-1H-pyrano[3,4-b]benzofuran-6-yl]-1,3-benzodioxole-5-carboxamide '
               'REASON: WRONGLY CLASSIFIED Contains an anilide moiety (amide '
               'nitrogen attached to benzene ring)\n'
               'False negatives: NONE\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'C1=CC=CC=2NC=C(C12)CC(O[C@H]3[C@@H]([C@H]([C@@H]([C@H](O3)C(O)=O)O)O)O)=O',
                                     'name': 'Indole-3-acetic-acid-O-glucuronide',
                                     'reason': 'Does not contain an anilide '
                                               'moiety'},
                                 {   'smiles': 'C1=C(C=C(C2=C1OC(=C(C2=O)O[C@H]3[C@@H]([C@H]([C@@H]([C@H](O3)CO)O)O)O[C@H]4[C@@H]([C@H]([C@@H]([C@H](O4)CO)O)O)O)C5=CC=C(C(=C5)O)O)O)[O-]',
                                     'name': 'quercetin '
                                             '3-O-beta-D-glucosyl-(1->2)-beta-D-glucoside(1-)',
                                     'reason': 'Does not contain an anilide '
                                               'moiety'},
                                 {   'smiles': 'O[C@@H]1C2([C@]([C@]3([C@@](C4([C@](C[C@H]3O)(C[C@H](O)CC4)[H])C)(C1)[H])[H])(CC[C@@H]2C(CCCC(O)(CO)C)C)[H])C',
                                     'name': '(3R,5S,7R,8R,9S,10S,12S,13R,14S,17R)-17-((2R)-6,7-Dihydroxy-6-methylheptan-2-yl)-10,13-dimethylhexadecahydro-1H-cyclopenta[a]phenanthrene-3,7,12-triol',
                                     'reason': 'Does not contain an anilide '
                                               'moiety'},
                                 {   'smiles': 'O=C(N[C@@H](CC1=CC=C(O)C=C1)C(O)=O)[C@@H](NC(=O)[C@@H](N)C(C)C)CCCN=C(N)N',
                                     'name': 'Val-Arg-Tyr',
                                     'reason': 'Does not contain an anilide '
                                               'moiety'},
                                 {   'smiles': 'O=C1N2C(=NC3=C1C=CC=C3)[C@](O)(NC([C@@H]2CC4=CC=CC=C4)=O)CC',
                                     'name': 'Aspamide G',
                                     'reason': 'Does not contain an anilide '
                                               'moiety'},
                                 {   'smiles': 'C1C=CCC2C1C(=O)N(C2=O)C3=NNC(=N3)C4=CC=CC=C4',
                                     'name': '2-(5-phenyl-1H-1,2,4-triazol-3-yl)-3a,4,7,7a-tetrahydroisoindole-1,3-dione',
                                     'reason': 'Does not contain an anilide '
                                               'moiety'},
                                 {   'smiles': 'N12[C@@]3([C@](C[C@H]1C(N([C@H](C2=O)C)[C@@H](C(=O)OCC)CCC=4C=CC=CC4)=O)(CCC3)[H])[H]',
                                     'name': 'ramipril dioxopiperazine',
                                     'reason': 'Does not contain an anilide '
                                               'moiety'},
                                 {   'smiles': 'C=1(C(=CC=2C=CC=CC2N1)C(O)=O)C=3NC(C(N3)(C)C(C)C)=O',
                                     'name': '2-[4-methyl-5-oxo-4-(propan-2-yl)-4,5-dihydro-1H-imidazol-2-yl]quinoline-3-carboxylic '
                                             'acid',
                                     'reason': 'Does not contain an anilide '
                                               'moiety'},
                                 {   'smiles': 'COC1=CC=CC=C1C2=NN=C3N2NC(S3)C4=CC(=C(C=C4)O)OC',
                                     'name': '2-methoxy-4-[3-(2-methoxyphenyl)-5,6-dihydro-[1,2,4]triazolo[3,4-b][1,3,4]thiadiazol-6-yl]phenol',
                                     'reason': 'Does not contain an anilide '
                                               'moiety'},
                                 {   'smiles': 'CCC(=O)N[C@H]1C=C[C@@H](O[C@H]1CO)CC(=O)NCC2=CC(=CC(=C2)F)F',
                                     'name': 'N-[(2R,3S,6S)-6-[2-[(3,5-difluorophenyl)methylamino]-2-oxoethyl]-2-(hydroxymethyl)-3,6-dihydro-2H-pyran-3-yl]propanamide',
                                     'reason': 'Does not contain an anilide '
                                               'moiety'}],
    'sample_false_negatives': [   {   'smiles': 'N(C(COC1=CC=C(C=C1)OCCCC)=O)(CCN(CC)CC)C2=C(OCC)C=CC(=C2)OCC',
                                      'name': 'fenoxedil',
                                      'reason': 'Does not contain an anilide '
                                                'moiety'},
                                  {   'smiles': 'CCC(=O)N(c1ccccc1)C1(CCN(CCc2cccs2)CC1)COC',
                                      'name': 'sufentanil',
                                      'reason': 'Does not contain an anilide '
                                                'moiety'},
                                  {   'smiles': 'COc1ccsc1CN(C(=O)CCl)c1c(C)cccc1C',
                                      'name': 'Thenylchlor',
                                      'reason': 'Does not contain an anilide '
                                                'moiety'},
                                  {   'smiles': 'CC(C)N(C(=O)CS(O)(=O)=O)c1ccccc1',
                                      'name': 'propachlor ESA',
                                      'reason': 'Does not contain an anilide '
                                                'moiety'},
                                  {   'smiles': 'CCC(=O)N(C1CCNCC1)c1ccccc1',
                                      'name': 'norfentanyl',
                                      'reason': 'Does not contain an anilide '
                                                'moiety'},
                                  {   'smiles': 'O=C(N(C1=CC=C(C=C1)C)C)C(C)C',
                                      'name': '2-NMC',
                                      'reason': 'Does not contain an anilide '
                                                'moiety'},
                                  {   'smiles': 'CCCOCCN(C(=O)CCl)c1c(CC)cccc1CC',
                                      'name': 'Pretilachlor',
                                      'reason': 'Does not contain an anilide '
                                                'moiety'},
                                  {   'smiles': 'CCC(=O)N(C1CCN(CCc2cccs2)CC1C)c1ccccc1',
                                      'name': '3-methylthiofentanyl',
                                      'reason': 'Does not contain an anilide '
                                                'moiety'},
                                  {   'smiles': 'CN(C1=CC=CC=C1)C(=O)COC2=NC(=C(N=N2)C3=CC=CS3)C4=CC=CS4',
                                      'name': '2-[(5,6-dithiophen-2-yl-1,2,4-triazin-3-yl)oxy]-N-methyl-N-phenylacetamide',
                                      'reason': 'Does not contain an anilide '
                                                'moiety'},
                                  {   'smiles': 'FC=1C(N(C2CCN(CC2)CCC3=CC=CC=C3)C(=O)COC)=CC=CC1',
                                      'name': 'Ocfentanil',
                                      'reason': 'Does not contain an anilide '
                                                'moiety'}],
    'attempt': 2,
    'reasoning': 'Upon analyzing the previous code and outcomes, it appears '
                 'that the function is misclassifying certain molecules as '
                 'anilides when they are not, leading to a high number of '
                 'false positives and a low F1 score. The primary issue seems '
                 'to be with the specificity of the pattern used to identify '
                 'anilides.\n'
                 '\n'
                 '**Problems Identified:**\n'
                 '\n'
                 '1. **Overly Broad SMARTS Pattern**: The previous code checks '
                 'for an amide group where the nitrogen is attached to any '
                 'aromatic carbon, which can include heteroaromatic rings and '
                 'non-benzene aromatic systems. This broad pattern matches '
                 'compounds that are not true anilides.\n'
                 '\n'
                 '2. **Ring Membership of Nitrogen**: The code attempts to '
                 'exclude cases where the nitrogen is in a 5- or 6-membered '
                 "ring but doesn't account for larger rings or cases where the "
                 'nitrogen is part of a bicyclic system, leading to incorrect '
                 'classifications.\n'
                 '\n'
                 '3. **Benzene Ring Verification**: The method for verifying '
                 'that the aromatic ring is a benzene ring (six-membered ring '
                 'of carbons) may not be robust, potentially misidentifying '
                 'rings that contain heteroatoms or are fused with other '
                 'rings.\n'
                 '\n'
                 '**Improvements:**\n'
                 '\n'
                 '- **Define a Specific SMARTS Pattern**: Create a SMARTS '
                 'pattern that specifically matches anilides by ensuring the '
                 'amide nitrogen is directly attached to a benzene ring '
                 'composed entirely of carbon atoms.\n'
                 '\n'
                 '- **Exclude Nitrogen in Rings**: Ensure that the amide '
                 'nitrogen is not part of any ring system.\n'
                 '\n'
                 "- **Accurate Benzene Ring Detection**: Use RDKit's ability "
                 'to identify aromatic rings and confirm that they are benzene '
                 'rings without heteroatoms.\n'
                 '\n'
                 '- **Avoid Matching Heteroaromatic Systems**: Make sure that '
                 'heteroaromatic rings are not incorrectly identified as '
                 'benzene rings.\n'
                 '\n'
                 'By implementing these improvements, the function should more '
                 'accurately classify anilides, reducing false positives and '
                 'improving the F1 score.\n'
                 '\n'
                 'Here is the improved code:',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 222,
    'num_false_positives': 6982,
    'num_true_negatives': 135069,
    'num_false_negatives': 27,
    'num_negatives': None,
    'precision': 0.030816213214880622,
    'recall': 0.891566265060241,
    'f1': 0.05957332617737824,
    'accuracy': 0.950744905130007,
    'negative_predictive_value': 0.9998001421211583}