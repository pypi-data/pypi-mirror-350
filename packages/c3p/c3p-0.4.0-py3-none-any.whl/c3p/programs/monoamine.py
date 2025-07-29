"""
Classifies: CHEBI:63534 monoamine
"""
from rdkit import Chem

def is_monoamine(smiles: str):
    """
    Determines if a molecule is a monoamine based on its SMILES string.
    A monoamine contains one amino group connected to an aromatic ring by a two-carbon chain.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a monoamine, False otherwise
        str: Reason for classification
    """
    
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Enhanced SMARTS pattern for monoamine: Aromatic ring bonded through two carbons (aliphatic) to an amino group
    monoamine_pattern = Chem.MolFromSmarts("a-!@[CH2]-[CH2]-[NH2]")

    # Check for substructure matches
    if mol.HasSubstructMatch(monoamine_pattern):
        return True, "Contains amino group connected to an aromatic ring by a two-carbon chain"
    else:
        return False, "Does not contain the required monoamine structure"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:63534',
                          'name': 'monoamine',
                          'definition': 'An aralylamino compound which '
                                        'contains one amino group connected to '
                                        'an aromatic ring by a two-carbon '
                                        'chain. Monoamines are derived from '
                                        'aromatic amino acids like '
                                        'phenylalanine, tyrosine, tryptophan, '
                                        'and the thyroid hormones by the '
                                        'action of aromatic amino acid '
                                        'decarboxylase enzymes.',
                          'parents': ['CHEBI:64365'],
                          'xrefs': [   'PMID:21822758',
                                       'PMID:21993877',
                                       'PMID:22005599',
                                       'PMID:22082101',
                                       'PMID:22153577',
                                       'PMID:22213370',
                                       'PMID:22218931',
                                       'PMID:22342987',
                                       'PMID:22371656'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 20,
                           'log_lines_of_code': 2.995732273553991,
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
                                                 0,
                                                 1,
                                                 1,
                                                 2,
                                                 1,
                                                 2],
                           'max_indent': 2,
                           'imports': ['from rdkit import Chem'],
                           'imports_count': 1,
                           'methods_called': [   'HasSubstructMatch',
                                                 'MolFromSmiles',
                                                 'MolFromSmarts'],
                           'methods_called_count': 3,
                           'smarts_strings': ['a-!@[CH2]-[CH2]-[NH2]'],
                           'smarts_strings_count': 1,
                           'defs': ['is_monoamine(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'True, "Contains amino group '
                                          'connected to an aromatic ring by a '
                                          'two-carbon chain"',
                                          'False, "Does not contain the '
                                          'required monoamine structure"'],
                           'returns_count': 3,
                           'complexity': 2.399146454710798},
    'message': '\n'
               'Attempt failed: F1 score of 0.00359126872790528 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: C1=C(C(=CC(=C1O)O)[N+](=O)[O-])CCN '
               'NAME: 4-(2-aminoethyl)-5-nitrobenzene-1,2-diol REASON: CORRECT '
               'Contains amino group connected to an aromatic ring by a '
               'two-carbon chain\n'
               ' * SMILES: CNCC(O)C1=CC(O)=C(O)C=C1 NAME: '
               '4-[1-hydroxy-2-(methylamino)ethyl]benzene-1,2-diol REASON: '
               'CORRECT Contains amino group connected to an aromatic ring by '
               'a two-carbon chain\n'
               ' * SMILES: N[C@@H](CSc1cc(C[C@H](N)C(O)=O)cc(O)c1O)C(O)=O '
               'NAME: Cysteinyldopa REASON: CORRECT Contains amino group '
               'connected to an aromatic ring by a two-carbon chain\n'
               ' * SMILES: NCC(O)c1ccc(O)c(O)c1 NAME: noradrenaline REASON: '
               'CORRECT Contains amino group connected to an aromatic ring by '
               'a two-carbon chain\n'
               ' * SMILES: CC(C)NC[C@H](O)c1ccc(O)c(O)c1 NAME: L-isoprenaline '
               'REASON: CORRECT Contains amino group connected to an aromatic '
               'ring by a two-carbon chain\n'
               ' * SMILES: OC1=C(O)C=C(CCN)C=C1O NAME: 5-Hydroxydopamine '
               'REASON: CORRECT Contains amino group connected to an aromatic '
               'ring by a two-carbon chain\n'
               ' * SMILES: CNC[C@@H](O)c1ccc(O)c(O)c1 NAME: (S)-adrenaline '
               'REASON: CORRECT Contains amino group connected to an aromatic '
               'ring by a two-carbon chain\n'
               ' * SMILES: OC(=O)C1CC(=C\\C=N/CCc2ccc(O)c(O)c2)/C=C(N1)C(O)=O '
               'NAME: Miraxanthin-V REASON: CORRECT Contains amino group '
               'connected to an aromatic ring by a two-carbon chain\n'
               ' * SMILES: O[C@@H](CNCCCCc1ccc(O)cc1)c1ccc(O)c(O)c1 NAME: '
               'arbutamine REASON: CORRECT Contains amino group connected to '
               'an aromatic ring by a two-carbon chain\n'
               ' * SMILES: CC(CCc1ccc(O)cc1)NCCc1ccc(O)c(O)c1 NAME: dobutamine '
               'REASON: CORRECT Contains amino group connected to an aromatic '
               'ring by a two-carbon chain\n'
               ' * SMILES: C[C@@H](CCc1ccc(O)cc1)NCCc1ccc(O)c(O)c1 NAME: '
               '(S)-dobutamine REASON: CORRECT Contains amino group connected '
               'to an aromatic ring by a two-carbon chain\n'
               ' * SMILES: C=1(C=C(C(=CC1)O)OC)C(O)CN NAME: Normetanephrine '
               'REASON: CORRECT Contains amino group connected to an aromatic '
               'ring by a two-carbon chain\n'
               ' * SMILES: C1=CC(=C(C(=C1CCN)O)O)O NAME: '
               '4-(2-aminoethyl)benzene-1,2,3-triol REASON: CORRECT Contains '
               'amino group connected to an aromatic ring by a two-carbon '
               'chain\n'
               ' * SMILES: S(OC1=C(O)C=C([C@@H](O)CNC)C=C1)(O)(=O)=O NAME: '
               'Epinephrine sulfate REASON: CORRECT Contains amino group '
               'connected to an aromatic ring by a two-carbon chain\n'
               ' * SMILES: NC[C@@H](O)c1ccc(O)c(O)c1 NAME: (S)-noradrenaline '
               'REASON: CORRECT Contains amino group connected to an aromatic '
               'ring by a two-carbon chain\n'
               ' * SMILES: [C@@H]([C@@H](N)C)(O)C1=CC(O)=C(C=C1)O NAME: '
               'alpha-methylnoradrenaline REASON: CORRECT Contains amino group '
               'connected to an aromatic ring by a two-carbon chain\n'
               ' * SMILES: NCCc1ccc(O)c(O)c1 NAME: dopamine REASON: CORRECT '
               'Contains amino group connected to an aromatic ring by a '
               'two-carbon chain\n'
               ' * SMILES: C=1(C=C(C(O)=CC1)O)CCN.Cl NAME: Dopamine '
               'hydrochloride REASON: CORRECT Contains amino group connected '
               'to an aromatic ring by a two-carbon chain\n'
               ' * SMILES: C=1(C(=CC=C(C1)CCN[C@@H](CCC=2C=CC(=CC2)O)C)O)O '
               'NAME: (R)-dobutamine REASON: CORRECT Contains amino group '
               'connected to an aromatic ring by a two-carbon chain\n'
               ' * SMILES: NCCc1ccc(O)cc1 NAME: tyramine REASON: CORRECT '
               'Contains amino group connected to an aromatic ring by a '
               'two-carbon chain\n'
               ' * SMILES: C[N+](C)(C)CCc1ccc(O)c(O)c1 NAME: Coryneine REASON: '
               'CORRECT Contains amino group connected to an aromatic ring by '
               'a two-carbon chain\n'
               ' * SMILES: CC(N)C(O)c1ccc(O)c(O)c1 NAME: Nordephrine REASON: '
               'CORRECT Contains amino group connected to an aromatic ring by '
               'a two-carbon chain\n'
               ' * SMILES: CNC[C@H](O)c1ccc(O)c(O)c1 NAME: (R)-adrenaline '
               'REASON: CORRECT Contains amino group connected to an aromatic '
               'ring by a two-carbon chain\n'
               ' * SMILES: C(CNCCCCCCNCCC1=CC=CC=C1)C2=CC(O)=C(C=C2)O NAME: '
               'dopexamine REASON: CORRECT Contains amino group connected to '
               'an aromatic ring by a two-carbon chain\n'
               ' * SMILES: S(OC1=C(O)C=C([C@@H](O)CN)C=C1)(O)(=O)=O NAME: '
               'Norepinephrine sulfate REASON: CORRECT Contains amino group '
               'connected to an aromatic ring by a two-carbon chain\n'
               'False positives: SMILES: '
               'O=C1N2C(C(=O)N([C@@]2(OC)C)C[C@@H](O)C3=CC=CC=C3)=CC4=C1N(C=5C=CC=CC45)C '
               'NAME: Marinacarboline K REASON: WRONGLY CLASSIFIED Contains '
               'amino group connected to an aromatic ring by a two-carbon '
               'chain\n'
               ' * SMILES: '
               'CN1C[C@@]2(C=C)C3C[C@H]4OC[C@@H]3[C@@H]1[C@@H]2[C@@]41C(=O)Nc2ccccc12 '
               'NAME: Gelsemine REASON: WRONGLY CLASSIFIED Contains amino '
               'group connected to an aromatic ring by a two-carbon chain\n'
               ' * SMILES: '
               'S1C2=NC(C1)C=C(C(=O)N[C@H](C(=O)N([C@H](C(=O)N(C)[C@H](C(N([C@H](C(O[C@@H](C[C@H](C[C@@H]([C@@H]2C)O)C)C(C)(C)C)=O)C)C)=O)C(C)C)C)C)CC3=CC=C(OC)C=C3)C '
               'NAME: Apratoxin G REASON: WRONGLY CLASSIFIED Contains amino '
               'group connected to an aromatic ring by a two-carbon chain\n'
               ' * SMILES: '
               'O=C1C(OC)=C(C(=O)C2=C1[C@@H](N3C[C@H]4CC=5C([C@@H]([C@@H]3C2)N4C)=C(O)C(OC)=C(C)C5)CNC(=O)[C@@H](N)C)C '
               'NAME: Safracin A REASON: WRONGLY CLASSIFIED Contains amino '
               'group connected to an aromatic ring by a two-carbon chain\n'
               ' * SMILES: '
               'CCC(=O)N(C)C[C@@H]1[C@H]([C@@H](N1C(=O)C)CO)C2=CC=C(C=C2)C3=CC=CC=C3F '
               'NAME: '
               'N-[[(2S,3R,4R)-1-acetyl-3-[4-(2-fluorophenyl)phenyl]-4-(hydroxymethyl)-2-azetidinyl]methyl]-N-methylpropanamide '
               'REASON: WRONGLY CLASSIFIED Contains amino group connected to '
               'an aromatic ring by a two-carbon chain\n'
               ' * SMILES: '
               'S(CC[C@H](NC(=O)[C@@H](N)CC1=CC=C(O)C=C1)C(=O)N[C@@H](CC(C)C)C(O)=O)C '
               'NAME: Tyr-Met-Leu REASON: WRONGLY CLASSIFIED Contains amino '
               'group connected to an aromatic ring by a two-carbon chain\n'
               ' * SMILES: CC(=O)N[C@H](Cc1ccccc1)C(O)=O NAME: '
               'N-acetyl-D-phenylalanine REASON: WRONGLY CLASSIFIED Contains '
               'amino group connected to an aromatic ring by a two-carbon '
               'chain\n'
               ' * SMILES: '
               'N[C@@H](Cc1c[nH]c2ccccc12)C(=O)N[C@@H](CC(O)=O)C(=O)N[C@@H](CO)C(O)=O '
               'NAME: Trp-Asp-Ser REASON: WRONGLY CLASSIFIED Contains amino '
               'group connected to an aromatic ring by a two-carbon chain\n'
               ' * SMILES: '
               'CCS(=O)(=O)N1[C@@H]([C@@H]([C@H]1C#N)C2=CC=C(C=C2)C#CC3=CC=CC=C3F)CO '
               'NAME: '
               '(2S,3R,4S)-1-ethylsulfonyl-3-[4-[2-(2-fluorophenyl)ethynyl]phenyl]-4-(hydroxymethyl)-2-azetidinecarbonitrile '
               'REASON: WRONGLY CLASSIFIED Contains amino group connected to '
               'an aromatic ring by a two-carbon chain\n'
               ' * SMILES: '
               'O=C1N[C@@]2(C3=C(N=C(C)C=C3)C=4C=CC(=CC4[C@@H]2O)C(=O)C)O[C@H]1C '
               'NAME: Actinobenzoquinoline REASON: WRONGLY CLASSIFIED Contains '
               'amino group connected to an aromatic ring by a two-carbon '
               'chain\n'
               ' * SMILES: O=C1N[C@H](C(=O)NC1CC=2C3=C(C(=CC=C3)CC=C(C)C)NC2)C '
               'NAME: Terezine D REASON: WRONGLY CLASSIFIED Contains amino '
               'group connected to an aromatic ring by a two-carbon chain\n'
               ' * SMILES: '
               'C1C[C@@H]([C@H](O[C@H]1CC(=O)N2CCC3=CC=CC=C3C2)CO)NC(=O)NC4=C(C=CC(=C4)F)F '
               'NAME: '
               '1-(2,5-difluorophenyl)-3-[(2S,3S,6R)-6-[2-(3,4-dihydro-1H-isoquinolin-2-yl)-2-oxoethyl]-2-(hydroxymethyl)-3-oxanyl]urea '
               'REASON: WRONGLY CLASSIFIED Contains amino group connected to '
               'an aromatic ring by a two-carbon chain\n'
               ' * SMILES: '
               'CCOC(=O)OC1=C(C=C(C=C1OC)C(=O)O[C@@H]2C[C@@H]3CN4CCC5=C([C@H]4C[C@@H]3[C@@H]([C@H]2OC)C(=O)OC)NC6=C5C=CC(=C6)OC)OC '
               'NAME: Syrosingopine REASON: WRONGLY CLASSIFIED Contains amino '
               'group connected to an aromatic ring by a two-carbon chain\n'
               ' * SMILES: '
               'CN1CCC2=C(C1)C=C(C(=N2)SCC3=C(C(C(=C(O3)N)C#N)C4=CC=C(C=C4)F)C(=O)OC)C#N '
               'NAME: '
               '6-amino-5-cyano-2-[[(3-cyano-6-methyl-7,8-dihydro-5H-1,6-naphthyridin-2-yl)thio]methyl]-4-(4-fluorophenyl)-4H-pyran-3-carboxylic '
               'acid methyl ester REASON: WRONGLY CLASSIFIED Contains amino '
               'group connected to an aromatic ring by a two-carbon chain\n'
               ' * SMILES: '
               'COC1=CC2=C(C=C1)C3=C(N2)[C@H](N(CC34CN(C4)CC5=C(C=CC(=C5)F)F)CC6CC6)CO '
               'NAME: '
               "[(1S)-2-(cyclopropylmethyl)-1'-[(2,5-difluorophenyl)methyl]-7-methoxy-1-spiro[3,9-dihydro-1H-pyrido[3,4-b]indole-4,3'-azetidine]yl]methanol "
               'REASON: WRONGLY CLASSIFIED Contains amino group connected to '
               'an aromatic ring by a two-carbon chain\n'
               ' * SMILES: '
               'CC1=CC=CC(=C1)C2=NN=C(O2)SCC(=O)NCCC3=CC(=C(C=C3)OC)OC NAME: '
               'N-[2-(3,4-dimethoxyphenyl)ethyl]-2-[[5-(3-methylphenyl)-1,3,4-oxadiazol-2-yl]thio]acetamide '
               'REASON: WRONGLY CLASSIFIED Contains amino group connected to '
               'an aromatic ring by a two-carbon chain\n'
               ' * SMILES: '
               'CC[C@@]12C=CCN3CCC=4C5=CC=CC=C5N(C4[C@]13[H])[C@](C2)(C(=O)OC)O '
               'NAME: 14,15-dehydrovincamine REASON: WRONGLY CLASSIFIED '
               'Contains amino group connected to an aromatic ring by a '
               'two-carbon chain\n'
               ' * SMILES: '
               '[H][C@]12SCC(COC(C)=O)=C(N1C(=O)[C@H]2NC(=O)[C@H](N)c1ccccc1)C(O)=O '
               'NAME: cefaloglycin REASON: WRONGLY CLASSIFIED Contains amino '
               'group connected to an aromatic ring by a two-carbon chain\n'
               ' * SMILES: NCCCC(=O)NC(Cc1c[nH]cn1)C(O)=O NAME: homocarnosine '
               'REASON: WRONGLY CLASSIFIED Contains amino group connected to '
               'an aromatic ring by a two-carbon chain\n'
               ' * SMILES: '
               'CC=CC1=CC=C(C=C1)[C@@H]2[C@H](N(C23CN(C3)C(=O)NC4CCCCC4)C(=O)C)CO '
               'NAME: LSM-39204 REASON: WRONGLY CLASSIFIED Contains amino '
               'group connected to an aromatic ring by a two-carbon chain\n'
               ' * SMILES: O=C1N[C@H](C(=O)N[C@H]1CC2=CC=CC=C2)CCC(=O)N NAME: '
               'Cyclo(S-Phe-S-Gln) REASON: WRONGLY CLASSIFIED Contains amino '
               'group connected to an aromatic ring by a two-carbon chain\n'
               ' * SMILES: O=C1N2CC3CC(CN(C3)C(=O)C)C2=CC=C1 NAME: '
               'N-Acetylcytisine REASON: WRONGLY CLASSIFIED Contains amino '
               'group connected to an aromatic ring by a two-carbon chain\n'
               ' * SMILES: '
               'CC[C@H]1CN2CCC1C[C@H]2[C@@H](C3=C4C=C(C=CC4=NC=C3)OC)O NAME: '
               '(R)-[(2S,5R)-5-ethyl-1-azabicyclo[2.2.2]octan-2-yl]-(6-methoxy-4-quinolinyl)methanol '
               'REASON: WRONGLY CLASSIFIED Contains amino group connected to '
               'an aromatic ring by a two-carbon chain\n'
               ' * SMILES: '
               'COCC(=O)NC1=CC2=C(C=C1)O[C@H]3[C@@H]2C[C@H](O[C@@H]3CO)CC(=O)NCCC4=CC=CC=C4 '
               'NAME: '
               '2-[(1R,3S,4aR,9aS)-1-(hydroxymethyl)-6-[(2-methoxy-1-oxoethyl)amino]-3,4,4a,9a-tetrahydro-1H-pyrano[3,4-b]benzofuran-3-yl]-N-(2-phenylethyl)acetamide '
               'REASON: WRONGLY CLASSIFIED Contains amino group connected to '
               'an aromatic ring by a two-carbon chain\n'
               ' * SMILES: '
               'CC(C)NC(=O)N1C[C@@H]2[C@H]([C@@H](N2C(=O)C1)CO)C3=CC=C(C=C3)C=CC4=CC=CC=C4 '
               'NAME: LSM-40882 REASON: WRONGLY CLASSIFIED Contains amino '
               'group connected to an aromatic ring by a two-carbon chain\n'
               'False negatives: SMILES: '
               'COc1cc(ccc1OCCCN1CCC(CC1)c1noc2cc(F)ccc12)C(C)=O NAME: '
               'iloperidone REASON: MISSED Does not contain the required '
               'monoamine structure\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': '[H][C@@]1(O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O)O[C@@H]1[C@@H](O)[C@@H](O)[C@@H](CO)O[C@H]1OC[C@H]1O[C@@H](OC[C@H]2O[C@@H](OC[C@H](NC(=O)[C@H](O)CCCCCCCCCCCCCCCCCCCCCC)[C@H](O)[C@H](O)CCCCCCCCCCCCCC)[C@H](O)[C@@H](O)[C@H]2O)[C@H](O)[C@@H](O)[C@H]1O',
                                     'name': 'Neurosporaside',
                                     'reason': 'Does not contain the required '
                                               'monoamine structure'},
                                 {   'smiles': '[O-]C(=O)C1=CN(C2CC2)C2=CC(N3CC[NH2+]CC3)=C(F)C=C2C1=O',
                                     'name': 'ciprofloxacin zwitterion',
                                     'reason': 'Does not contain the required '
                                               'monoamine structure'},
                                 {   'smiles': 'O=C1NC(=CC2=C1O[C@H]([C@@H](O)CC(C)C)O2)C',
                                     'name': 'Dihydroisoflavipucine',
                                     'reason': 'Does not contain the required '
                                               'monoamine structure'},
                                 {   'smiles': 'O=C1N2C(C(=O)N([C@@]2(OC)C)C[C@@H](O)C3=CC=CC=C3)=CC4=C1N(C=5C=CC=CC45)C',
                                     'name': 'Marinacarboline K',
                                     'reason': 'Does not contain the required '
                                               'monoamine structure'},
                                 {   'smiles': 'O1[C@@H](O[C@H]2[C@@H](O)[C@H](O)[C@H](O[C@@H]2OC[C@H]3OC(O)[C@@H](O)[C@@H](O)[C@@H]3O)CO)[C@H](NC(=O)C)[C@@H](O)[C@H](O[C@@H]4O[C@@H]([C@H](O)[C@H](O)[C@H]4O)CO[C@]5(O[C@H]([C@H](NC(=O)C)[C@@H](O)C5)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]1CO',
                                     'name': '(2R,4S,5R,6R)-5-Acetamido-2-[[(2R,3R,4S,5R,6S)-6-[(2R,3S,4R,5R,6S)-5-acetamido-6-[(2S,3S,4S,5S,6R)-4,5-dihydroxy-6-(hydroxymethyl)-2-[[(2R,3S,4S,5S)-3,4,5,6-tetrahydroxyoxan-2-yl]methoxy]oxan-3-yl]oxy-4-hydroxy-2-(hydroxymethyl)oxan-3-yl]oxy-3,4,5-trihydroxyoxan-2-yl]methoxy]-4-hydroxy-6-[(1R,2R)-1,2,3-trihydroxypropyl]oxane-2-carboxylic '
                                             'acid',
                                     'reason': 'Does not contain the required '
                                               'monoamine structure'},
                                 {   'smiles': 'O(C(=O)CCCCCCC)CCC1=CC=CC=C1',
                                     'name': '2-Phenylethyl octanoate',
                                     'reason': 'Does not contain the required '
                                               'monoamine structure'},
                                 {   'smiles': 'P(OCC(OC(=O)CCCCCCC/C=C\\CCCCCCCC)COC(=O)CCC/C=C\\C/C=C\\C/C=C\\CCCCCCCC)(OCCNC)(O)=O',
                                     'name': 'PE-NMe(20:3(5Z,8Z,11Z)/18:1(9Z))',
                                     'reason': 'Does not contain the required '
                                               'monoamine structure'},
                                 {   'smiles': 'O=C1C2=C(OC=3C1=CC=CN3)C(Cl)=CC(=C2)C=4NN=NN4',
                                     'name': 'traxanox',
                                     'reason': 'Does not contain the required '
                                               'monoamine structure'},
                                 {   'smiles': 'CCCCC(C)CCCCCC(C)CCCCCCCCCC(C)CC(O)=O',
                                     'name': '3,13,19-trimethyltricosanoic '
                                             'acid',
                                     'reason': 'Does not contain the required '
                                               'monoamine structure'},
                                 {   'smiles': 'COC(CC1=CC[C@]2(C)[C@@H](C)CCC[C@]2(C)C1=O)OC',
                                     'name': 'aignopsane ketal',
                                     'reason': 'Does not contain the required '
                                               'monoamine structure'}],
    'sample_false_negatives': [   {   'smiles': 'CNCC(O)C1=CC(O)=C(O)C=C1',
                                      'name': '4-[1-hydroxy-2-(methylamino)ethyl]benzene-1,2-diol',
                                      'reason': 'Does not contain the required '
                                                'monoamine structure'},
                                  {   'smiles': 'N[C@@H](CSc1cc(C[C@H](N)C(O)=O)cc(O)c1O)C(O)=O',
                                      'name': 'Cysteinyldopa',
                                      'reason': 'Does not contain the required '
                                                'monoamine structure'},
                                  {   'smiles': 'NCC(O)c1ccc(O)c(O)c1',
                                      'name': 'noradrenaline',
                                      'reason': 'Does not contain the required '
                                                'monoamine structure'},
                                  {   'smiles': 'CC(C)NC[C@H](O)c1ccc(O)c(O)c1',
                                      'name': 'L-isoprenaline',
                                      'reason': 'Does not contain the required '
                                                'monoamine structure'},
                                  {   'smiles': 'CNC[C@@H](O)c1ccc(O)c(O)c1',
                                      'name': '(S)-adrenaline',
                                      'reason': 'Does not contain the required '
                                                'monoamine structure'},
                                  {   'smiles': 'OC(=O)C1CC(=C\\C=N/CCc2ccc(O)c(O)c2)/C=C(N1)C(O)=O',
                                      'name': 'Miraxanthin-V',
                                      'reason': 'Does not contain the required '
                                                'monoamine structure'},
                                  {   'smiles': 'O[C@@H](CNCCCCc1ccc(O)cc1)c1ccc(O)c(O)c1',
                                      'name': 'arbutamine',
                                      'reason': 'Does not contain the required '
                                                'monoamine structure'},
                                  {   'smiles': 'CC(CCc1ccc(O)cc1)NCCc1ccc(O)c(O)c1',
                                      'name': 'dobutamine',
                                      'reason': 'Does not contain the required '
                                                'monoamine structure'},
                                  {   'smiles': 'C[C@@H](CCc1ccc(O)cc1)NCCc1ccc(O)c(O)c1',
                                      'name': '(S)-dobutamine',
                                      'reason': 'Does not contain the required '
                                                'monoamine structure'},
                                  {   'smiles': 'C=1(C=C(C(=CC1)O)OC)C(O)CN',
                                      'name': 'Normetanephrine',
                                      'reason': 'Does not contain the required '
                                                'monoamine structure'}],
    'attempt': 1,
    'reasoning': 'The task is to classify whether a given SMILES string '
                 'corresponds to a monoamine. The definition of a monoamine is '
                 'a compound with one amino group connected to an aromatic '
                 'ring by a two-carbon chain. Based on the outcomes, it '
                 'appears the previous SMARTS pattern did not accurately '
                 'capture the monoamine substructure, resulting in many '
                 'misclassifications.\n'
                 '\n'
                 '### Analysis and Hypothesis:\n'
                 '1. **SMARTS Pattern**: \n'
                 '   - The previous pattern `[$(cc)]CCN` might be too '
                 'simplistic. It does not account for various complexities '
                 'such as the possible orientations and types of aromatic '
                 'rings, or potential substituents on the two-carbon chain.\n'
                 '\n'
                 '2. **False Positives**: \n'
                 '   - Compounds might have been wrongly classified due to '
                 'complex structures containing substructures that loosely fit '
                 'the defined pattern without fulfilling the precise '
                 'definition of a monoamine.\n'
                 '\n'
                 '3. **False Negatives**: \n'
                 '   - Compounds with correct monoamine structures may have '
                 'not matched due to limitations in the SMARTS pattern in '
                 'identifying certain configurations.\n'
                 '\n'
                 '4. **Aromaticity**: \n'
                 '   - The parser may need a robust method to ensure the '
                 "aromatic ring is indeed classified as such by RDKit's "
                 'perception.\n'
                 '\n'
                 '5. **Enhancement**:\n'
                 '   - A more accurate SMARTS pattern should reflect the '
                 'intended structure, possibly needing adjustments such as '
                 'specifying ring-related constraints.\n'
                 '   - Consider edge cases like multiple aromatic '
                 'functionalities and presence of additional heteroatoms that '
                 'can influence aromatic bonding.\n'
                 '\n'
                 '### Improved Approach:\n'
                 '- **Pattern Improvement**: Expand the pattern to consider '
                 'more specific aromatic bonds, use stereochemistry where '
                 'important, explicitly specify carbon types, and verify the '
                 'presence of exactly one amino group.\n'
                 '- **Molecule Confirmation**: Validate if RDKit recognizes '
                 'the aromaticity correctly and use additional checks for the '
                 'aromatic ring.\n'
                 '\n'
                 '### Revised Code:',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 7,
    'num_false_positives': 73,
    'num_true_negatives': 142194,
    'num_false_negatives': 26,
    'num_negatives': None,
    'precision': 0.0875,
    'recall': 0.21212121212121213,
    'f1': 0.1238938053097345,
    'accuracy': 0.9993042867182009,
    'negative_predictive_value': 0.9998171846435101}