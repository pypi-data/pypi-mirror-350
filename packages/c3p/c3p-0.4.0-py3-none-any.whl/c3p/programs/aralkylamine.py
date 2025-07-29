"""
Classifies: CHEBI:18000 aralkylamine
"""
from rdkit import Chem

def is_aralkylamine(smiles: str):
    """
    Determines if a molecule is an aralkylamine based on its SMILES string.
    An aralkylamine is an alkylamine where the alkyl group is substituted by an aromatic group.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        tuple: (bool, str) indicating if it's an aralkylamine and the reason
    """
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Find amine (N) connected to carbon.
    amine_pattern = Chem.MolFromSmarts("[NX3;!$(NC=O)]")
    if not mol.HasSubstructMatch(amine_pattern):
        return False, "No primary, secondary, or tertiary amine group found"

    # Look for aromatic groups directly bonded to an alkyl carbon and connected to an amine.
    aralkylamine_pattern = Chem.MolFromSmarts("[CX4][a]")  # Alkyl carbon attached directly to an aromatic
    if not mol.HasSubstructMatch(aralkylamine_pattern):
        return False, "No alkyl group directly substituted by aromatic group found"

    # Now ensure connection pattern like N-C-C (to ensure we consider the broad range of alkyl connections)
    extended_pattern = Chem.MolFromSmarts("[NX3][CX4][a]")  # N connected to alkyl, then aromatic
    if mol.HasSubstructMatch(extended_pattern):
        return True, "Molecule is an aralkylamine with aromatic substitution on the alkyl side chain"

    return False, "Structure does not match an aralkylamine pattern"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:18000',
                          'name': 'aralkylamine',
                          'definition': 'An alkylamine in which the alkyl '
                                        'group is substituted by an aromatic '
                                        'group.',
                          'parents': ['CHEBI:22331', 'CHEBI:64365'],
                          'xrefs': [   'KEGG:C01890',
                                       'MetaCyc:Arylalkylamines',
                                       'Wikipedia:Arylalkylamine'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 25,
                           'log_lines_of_code': 3.2188758248682006,
                           'indent_by_line': [   1,
                                                 1,
                                                 1,
                                                 0,
                                                 1,
                                                 2,
                                                 0,
                                                 1,
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
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 0,
                                                 1],
                           'max_indent': 2,
                           'imports': ['from rdkit import Chem'],
                           'imports_count': 1,
                           'methods_called': [   'HasSubstructMatch',
                                                 'MolFromSmarts',
                                                 'MolFromSmiles'],
                           'methods_called_count': 3,
                           'smarts_strings': [   '[NX3;!$(NC=O)]',
                                                 '[CX4][a]',
                                                 '[NX3][CX4][a]'],
                           'smarts_strings_count': 3,
                           'defs': ['is_aralkylamine(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "No primary, secondary, or '
                                          'tertiary amine group found"',
                                          'False, "No alkyl group directly '
                                          'substituted by aromatic group '
                                          'found"',
                                          'True, "Molecule is an aralkylamine '
                                          'with aromatic substitution on the '
                                          'alkyl side chain"',
                                          'False, "Structure does not match an '
                                          'aralkylamine pattern"'],
                           'returns_count': 5,
                           'complexity': 2.84377516497364},
    'message': '\n'
               'Attempt failed: F1 score of 0.006144668158090977 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: '
               'O[C@@H]1[C@@H](N(C)[C@@H](C1)CCCCCC(O)C)CC2=CC=CC=C2 NAME: '
               'Preubetain J REASON: CORRECT Molecule is an aralkylamine\n'
               ' * SMILES: C1=CC=C(C=C1)CNC2=NC(=CS2)C3=CN=CC=C3 NAME: '
               'N-(phenylmethyl)-4-(3-pyridinyl)-2-thiazolamine REASON: '
               'CORRECT Molecule is an aralkylamine\n'
               ' * SMILES: NC(C(CCCCCCCCCCCC)CC1=CC=CC=C1)(C)C NAME: '
               '3-benzyl-2-methyl-2-pentadecanamine REASON: CORRECT Molecule '
               'is an aralkylamine\n'
               ' * SMILES: '
               'CCNC(=O)C[C@H]1CC[C@@H]2[C@@H](O1)COC[C@H](CN2CC3=CC=NC=C3)O '
               'NAME: '
               '2-[(3S,6aR,8R,10aR)-3-hydroxy-1-(pyridin-4-ylmethyl)-3,4,6,6a,8,9,10,10a-octahydro-2H-pyrano[2,3-c][1,5]oxazocin-8-yl]-N-ethylacetamide '
               'REASON: CORRECT Molecule is an aralkylamine\n'
               ' * SMILES: '
               'C[C@@H]1CN(C(=O)C2=CC=CC=C2C3=CC=CC=C3CO[C@@H]1CN(C)CC4=CN=CC=C4)[C@H](C)CO '
               'NAME: LSM-9811 REASON: CORRECT Molecule is an aralkylamine\n'
               ' * SMILES: N1[C@H](CN[C@H](C1)CC2=CC=CC=C2)CC3=CC=CC=C3 NAME: '
               'Xenocockiamide A REASON: CORRECT Molecule is an aralkylamine\n'
               ' * SMILES: CC1=CC(=NN1C2=NN=C(N=N2)NCC3=CC=C(C=C3)Cl)C NAME: '
               'N-[(4-chlorophenyl)methyl]-6-(3,5-dimethyl-1-pyrazolyl)-1,2,4,5-tetrazin-3-amine '
               'REASON: CORRECT Molecule is an aralkylamine\n'
               ' * SMILES: NC[C@H](Cl)[C@@H](O)c1c[nH]c(N)n1 NAME: girolline '
               'REASON: CORRECT Molecule is an aralkylamine\n'
               ' * SMILES: FC(F)(F)C=1OC(=CC1CN)C NAME: '
               '[5-Methyl-2-(trifluoromethyl)-3-furyl]methylamine REASON: '
               'CORRECT Molecule is an aralkylamine\n'
               ' * SMILES: O1C(CN2CCCC2)=CC=C1 NAME: 1-Furfurylpyrrolidine '
               'REASON: CORRECT Molecule is an aralkylamine\n'
               ' * SMILES: '
               'C[C@@H]1CN(C(=O)C2=CC=CC=C2C3=CC=CC=C3CO[C@H]1CN(C)CC4=CC=NC=C4)[C@@H](C)CO '
               'NAME: LSM-12472 REASON: CORRECT Molecule is an aralkylamine\n'
               ' * SMILES: NCc1ccccc1 NAME: benzylamine REASON: CORRECT '
               'Molecule is an aralkylamine\n'
               ' * SMILES: C1=COC(=C1)C2=CC(=NC(=N2)NCC3=CC=C(C=C3)Cl)C(F)(F)F '
               'NAME: '
               'N-[(4-chlorophenyl)methyl]-4-(2-furanyl)-6-(trifluoromethyl)-2-pyrimidinamine '
               'REASON: CORRECT Molecule is an aralkylamine\n'
               ' * SMILES: '
               'CCCOP(=O)(C1=CC=C(C=C1)N(C)C)C(C2=CC=C(C=C2)C)NC3=CC=CC=C3 '
               'NAME: '
               '4-[[anilino-(4-methylphenyl)methyl]-propoxyphosphoryl]-N,N-dimethylaniline '
               'REASON: CORRECT Molecule is an aralkylamine\n'
               ' * SMILES: S1C=C(C(N(C(C)C)C(C)C)CCCCC#N)C=C1 NAME: '
               '6-(Diisopropylamino)-6-(3-thienyl)hexanenitrile REASON: '
               'CORRECT Molecule is an aralkylamine\n'
               ' * SMILES: OC[C@H](N)C1=CC=CC=C1 NAME: '
               '(R)-(-)-2-Phenylglycinol REASON: CORRECT Molecule is an '
               'aralkylamine\n'
               ' * SMILES: CN1CC2C(C(C(C(=C2C=C1)C#N)N)(C#N)C#N)C3=CC=CC=C3 '
               'NAME: '
               '6-amino-2-methyl-8-phenyl-1,6,8,8a-tetrahydroisoquinoline-5,7,7-tricarbonitrile '
               'REASON: CORRECT Molecule is an aralkylamine\n'
               ' * SMILES: CC1=CC(=NC(=N1)NCC2=CC=CC=C2)NN=CC3=CC=CC=C3 NAME: '
               '6-methyl-N2-(phenylmethyl)-N4-[(phenylmethylene)amino]pyrimidine-2,4-diamine '
               'REASON: CORRECT Molecule is an aralkylamine\n'
               ' * SMILES: N(CCC1=CC=NC=C1)(CC)CC NAME: '
               'N1,N1-diethyl-2-(4-pyridyl)ethan-1-amine REASON: CORRECT '
               'Molecule is an aralkylamine\n'
               ' * SMILES: '
               'CCNC(=O)C[C@@H]1CC[C@@H]2[C@@H](O1)COC[C@H](CN2CC3=CC=NC=C3)O '
               'NAME: '
               '2-[(3S,6aR,8S,10aR)-3-hydroxy-1-(pyridin-4-ylmethyl)-3,4,6,6a,8,9,10,10a-octahydro-2H-pyrano[2,3-c][1,5]oxazocin-8-yl]-N-ethylacetamide '
               'REASON: CORRECT Molecule is an aralkylamine\n'
               ' * SMILES: CC1=CC=C(O1)C(=O)CCNC2=CC(=CC=C2)Br NAME: '
               '3-(3-bromoanilino)-1-(5-methyl-2-furanyl)-1-propanone REASON: '
               'CORRECT Molecule is an aralkylamine\n'
               ' * SMILES: Cl.Cl.OC[C@@H](N)CC=1NC=NC1 NAME: L-Histidinol '
               'dihydrochloride REASON: CORRECT Molecule is an aralkylamine\n'
               ' * SMILES: '
               'CCNC(=O)C[C@H]1CC[C@@H]2[C@@H](O1)COC[C@@H](CN2CC3=CC=NC=C3)O '
               'NAME: '
               '2-[(3R,6aR,8R,10aR)-3-hydroxy-1-(pyridin-4-ylmethyl)-3,4,6,6a,8,9,10,10a-octahydro-2H-pyrano[2,3-c][1,5]oxazocin-8-yl]-N-ethylacetamide '
               'REASON: CORRECT Molecule is an aralkylamine\n'
               ' * SMILES: S1C(CNC)=CC=C1C2=CC=NC=C2 NAME: '
               'N-methyl-(5-pyrid-4-ylthien-2-yl)methylamine REASON: CORRECT '
               'Molecule is an aralkylamine\n'
               ' * SMILES: N1=C(CN)C=CN=C1 NAME: 4-Aminomethylpyrimidine '
               'REASON: CORRECT Molecule is an aralkylamine\n'
               'False positives: SMILES: '
               'O1C2C34C(C(N(CC3)C)CC5=C4C1=C(OC)C=C5)C=CC2OC NAME: '
               '6-O-Methylcodeine REASON: WRONGLY CLASSIFIED Molecule is an '
               'aralkylamine\n'
               ' * SMILES: '
               'CN1C2=C(C=CC(=C2)OC)C3=C1[C@H](N(CC34CCN(CC4)S(=O)(=O)C5=CC=CS5)CC6CC6)CO '
               'NAME: '
               "[(1S)-2-(cyclopropylmethyl)-7-methoxy-9-methyl-1'-thiophen-2-ylsulfonyl-1-spiro[1,3-dihydropyrido[3,4-b]indole-4,4'-piperidine]yl]methanol "
               'REASON: WRONGLY CLASSIFIED Molecule is an aralkylamine\n'
               ' * SMILES: '
               'C[C@@H]1CN(C(=O)C2=C(N=CC(=C2)C3=CCCCC3)O[C@@H]1CN(C)CC4=CC=C(C=C4)C(=O)O)[C@H](C)CO '
               'NAME: '
               '4-[[[(2S,3R)-8-(1-cyclohexenyl)-5-[(2R)-1-hydroxypropan-2-yl]-3-methyl-6-oxo-3,4-dihydro-2H-pyrido[2,3-b][1,5]oxazocin-2-yl]methyl-methylamino]methyl]benzoic '
               'acid REASON: WRONGLY CLASSIFIED Molecule is an aralkylamine\n'
               ' * SMILES: '
               'C1CN(CCC1NC2=NC(=NC3=CC=CC=C32)C4=CC=CC=C4)CC5=CC=CC=C5 NAME: '
               '2-phenyl-N-[1-(phenylmethyl)-4-piperidinyl]-4-quinazolinamine '
               'REASON: WRONGLY CLASSIFIED Molecule is an aralkylamine\n'
               ' * SMILES: '
               'CN1C2=C(C=CC(=C2)OC)C3=C1[C@@H](N(CC34CCN(CC4)C(=O)CC5=CC=NC=C5)CC6=CC=NC=C6)CO '
               'NAME: '
               "1-[(1R)-1-(hydroxymethyl)-7-methoxy-9-methyl-2-(pyridin-4-ylmethyl)-1'-spiro[1,3-dihydropyrido[3,4-b]indole-4,4'-piperidine]yl]-2-pyridin-4-ylethanone "
               'REASON: WRONGLY CLASSIFIED Molecule is an aralkylamine\n'
               ' * SMILES: '
               'C[C@@H]1CN(C(=O)CC2=C(C=CC(=C2)N(C)C)O[C@@H]1CN(C)S(=O)(=O)C3=C(ON=C3C)C)[C@H](C)CO '
               'NAME: '
               'N-[[(2S,3R)-9-(dimethylamino)-5-[(2R)-1-hydroxypropan-2-yl]-3-methyl-6-oxo-2,3,4,7-tetrahydro-1,5-benzoxazonin-2-yl]methyl]-N,3,5-trimethyl-4-isoxazolesulfonamide '
               'REASON: WRONGLY CLASSIFIED Molecule is an aralkylamine\n'
               ' * SMILES: '
               'C[C@H]1CN(C(=O)C2=C(C3=CC=CC=C3CO[C@H]1CN(C)C(=O)CCN(C)C)C4=CC=CC=C4N2C)[C@H](C)CO '
               'NAME: LSM-11210 REASON: WRONGLY CLASSIFIED Molecule is an '
               'aralkylamine\n'
               ' * SMILES: '
               'Nc1ncnc2n(cnc12)[C@@H]1O[C@H](COP(O)(=O)OC(=O)c2cccc(O)c2O)[C@@H](O)[C@H]1O '
               "NAME: 2,3-dihydroxybenzoyl 5'-adenylate REASON: WRONGLY "
               'CLASSIFIED Molecule is an aralkylamine\n'
               ' * SMILES: '
               'COC1=CC(=CC(=C1)NC(=O)C2=CN=C(O2)N)C(=O)NC3=CC=CC(=C3)C(F)(F)F '
               'NAME: '
               '2-amino-N-[3-methoxy-5-[oxo-[3-(trifluoromethyl)anilino]methyl]phenyl]-5-oxazolecarboxamide '
               'REASON: WRONGLY CLASSIFIED Molecule is an aralkylamine\n'
               ' * SMILES: '
               'C1COCCC1C(=O)N2C[C@@H]3[C@@H]([C@@H](N3CC4=CC=C(C=C4)Cl)CO)C5=CC=CC=C52 '
               'NAME: '
               '[(1R,2aS,8bS)-2-[(4-chlorophenyl)methyl]-1-(hydroxymethyl)-1,2a,3,8b-tetrahydroazeto[2,3-c]quinolin-4-yl]-(4-oxanyl)methanone '
               'REASON: WRONGLY CLASSIFIED Molecule is an aralkylamine\n'
               ' * SMILES: '
               'C[C@H]1CCCCO[C@@H]([C@H](CN(C(=O)C2=C(O1)C=CC(=C2)NC(=O)NC3=CC4=C(C=C3)OCO4)[C@@H](C)CO)C)CN(C)C '
               'NAME: '
               '1-(1,3-benzodioxol-5-yl)-3-[(3S,9S,10S)-9-[(dimethylamino)methyl]-12-[(2S)-1-hydroxypropan-2-yl]-3,10-dimethyl-13-oxo-2,8-dioxa-12-azabicyclo[12.4.0]octadeca-1(14),15,17-trien-16-yl]urea '
               'REASON: WRONGLY CLASSIFIED Molecule is an aralkylamine\n'
               ' * SMILES: C1CN(CCN1)C2=C3C=CC=CC3=NC4=C(N2)C=C(C=C4)Cl NAME: '
               '3-chloro-6-(1-piperazinyl)-5H-benzo[b][1,4]benzodiazepine '
               'REASON: WRONGLY CLASSIFIED Molecule is an aralkylamine\n'
               ' * SMILES: '
               'SC[C@H](NC(=O)[C@@H](N)CCCCN)C(=O)N[C@@H](CC=1NC=NC1)C(O)=O '
               'NAME: Lys-Cys-His REASON: WRONGLY CLASSIFIED Molecule is an '
               'aralkylamine\n'
               ' * SMILES: '
               'CC(=O)NC1=CC=C(C=C1)NC(=S)NC(=O)C2=CC=C(C=C2)C(C)(C)C NAME: '
               'N-[(4-acetamidoanilino)-sulfanylidenemethyl]-4-tert-butylbenzamide '
               'REASON: WRONGLY CLASSIFIED Molecule is an aralkylamine\n'
               ' * SMILES: '
               'COC1=CC=CC=C1CNC(=O)C[C@H]2C[C@H]3[C@@H]([C@H](O2)CO)OC4=C3C=C(C=C4)NS(=O)(=O)C5=CC=C(C=C5)F '
               'NAME: '
               '2-[(1R,3R,4aR,9aS)-6-[(4-fluorophenyl)sulfonylamino]-1-(hydroxymethyl)-3,4,4a,9a-tetrahydro-1H-pyrano[3,4-b]benzofuran-3-yl]-N-[(2-methoxyphenyl)methyl]acetamide '
               'REASON: WRONGLY CLASSIFIED Molecule is an aralkylamine\n'
               ' * SMILES: '
               'CCC(C)C1=CC=CC=C1NC(=O)C2=CC3=C(N2)C(=CC=C3)[N+](=O)[O-] NAME: '
               'N-(2-butan-2-ylphenyl)-7-nitro-1H-indole-2-carboxamide REASON: '
               'WRONGLY CLASSIFIED Molecule is an aralkylamine\n'
               ' * SMILES: '
               'CC1=CC=C(C=C1)S(=O)(=O)N(C[C@@H](C)[C@@H](CN(C)C(=O)C2=CC3=C(C=C2)OCO3)OC)[C@@H](C)CO '
               'NAME: '
               'N-[(2S,3R)-4-[[(2S)-1-hydroxypropan-2-yl]-(4-methylphenyl)sulfonylamino]-2-methoxy-3-methylbutyl]-N-methyl-1,3-benzodioxole-5-carboxamide '
               'REASON: WRONGLY CLASSIFIED Molecule is an aralkylamine\n'
               ' * SMILES: '
               'COC1=CC(=CC(=C1OC)OC)C2=NC3=CC=CC=C3C(=C2)C(=O)N4CCN(CC4)C5=CC=CC=N5 '
               'NAME: '
               '[4-(2-pyridinyl)-1-piperazinyl]-[2-(3,4,5-trimethoxyphenyl)-4-quinolinyl]methanone '
               'REASON: WRONGLY CLASSIFIED Molecule is an aralkylamine\n'
               ' * SMILES: '
               'CN(C)C(=O)C1=NC(=NC=C1)N1CC2=CN(CC3=CC=C(F)C=C3F)N=C2C1 NAME: '
               'ZCAN262 REASON: WRONGLY CLASSIFIED Molecule is an '
               'aralkylamine\n'
               ' * SMILES: '
               'C[C@@H]1CN(C(=O)C2=C(C=CC(=C2)NC(=O)CN3C=NN=N3)O[C@H]1CN(C)CC4=CC=C(C=C4)C(F)(F)F)[C@@H](C)CO '
               'NAME: '
               'N-[(2R,3R)-5-[(2S)-1-hydroxypropan-2-yl]-3-methyl-2-[[methyl-[[4-(trifluoromethyl)phenyl]methyl]amino]methyl]-6-oxo-3,4-dihydro-2H-1,5-benzoxazocin-8-yl]-2-(1-tetrazolyl)acetamide '
               'REASON: WRONGLY CLASSIFIED Molecule is an aralkylamine\n'
               ' * SMILES: '
               'C[C@H](C1=CC=CC=C1)NC(=O)C[C@H]2C[C@@H]3[C@H]([C@H](O2)CO)OC4=C3C=C(C=C4)NS(=O)(=O)C5=CC=C(C=C5)F '
               'NAME: '
               '2-[(1R,3R,4aS,9aR)-6-[(4-fluorophenyl)sulfonylamino]-1-(hydroxymethyl)-3,4,4a,9a-tetrahydro-1H-pyrano[3,4-b]benzofuran-3-yl]-N-[(1R)-1-phenylethyl]acetamide '
               'REASON: WRONGLY CLASSIFIED Molecule is an aralkylamine\n'
               ' * SMILES: '
               'CS(=O)(=O)N1[C@H]2[C@H](CN3C2=CC=C(C3=O)C4=CCCC4)[C@H]([C@@H]1C(=O)NCCC5=CC=NC=C5)CO '
               'NAME: '
               '(2R,3R,3aS,9bS)-7-(1-cyclopentenyl)-3-(hydroxymethyl)-1-methylsulfonyl-6-oxo-N-(2-pyridin-4-ylethyl)-3,3a,4,9b-tetrahydro-2H-pyrrolo[2,3-a]indolizine-2-carboxamide '
               'REASON: WRONGLY CLASSIFIED Molecule is an aralkylamine\n'
               ' * SMILES: '
               'N(C(=O)C1=CC=CS1)C2=C(CN[C@H]3CC[C@@H](CC3)O)C=C(C=C2Br)Br '
               'NAME: neltenexine REASON: WRONGLY CLASSIFIED Molecule is an '
               'aralkylamine\n'
               ' * SMILES: N1(C2=C(C=CC=C2)C(=C1)CN(C)C)C(C=C)(C)C NAME: '
               '3-(dimethylaminomethyl)-1-(1 , 1 -dimethyl-2-propenyl)indole '
               'REASON: WRONGLY CLASSIFIED Molecule is an aralkylamine\n'
               ' * SMILES: '
               'N1([C@H]2[C@@H]([C@@H]([C@H](O2)C[S+](C)C)O)O)C3=C(C(N)=NC=N3)N=C1 '
               "NAME: 5'-(dimethylsulfonio)-5'-deoxyadenosine REASON: WRONGLY "
               'CLASSIFIED Molecule is an aralkylamine\n'
               'False negatives: SMILES: '
               'S1C=CC=C1C(CC[N+]2(CCOCC2)C)(C3=CC=CC=C3)O.[I-] NAME: '
               'Tiemonium iodide REASON: MISSED No primary, secondary, or '
               'tertiary amine group found\n'
               ' * SMILES: CC1=CC=C(O1)C[N+](C)(C)C NAME: '
               'trimethyl-[(5-methyl-2-furanyl)methyl]ammonium REASON: MISSED '
               'No primary, secondary, or tertiary amine group found\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'O1[C@H]([C@@H](O)CC=2C1=CC=CC2)C3=CC=CC=C3',
                                     'name': 'cis-(+)-3-Flavanol',
                                     'reason': 'No primary, secondary, or '
                                               'tertiary amine group found'},
                                 {   'smiles': 'O1C2C34C(C(N(CC3)C)CC5=C4C1=C(OC)C=C5)C=CC2OC',
                                     'name': '6-O-Methylcodeine',
                                     'reason': 'Structure does not match an '
                                               'aralkylamine pattern'},
                                 {   'smiles': 'O(C(=O)CCCCCCCCCCCCCCC)[C@@H](COC(=O)CCCCCCCCCCCCCCCCCCC)COC(=O)CCCCCCC',
                                     'name': 'TG(20:0/16:0/8:0)',
                                     'reason': 'No primary, secondary, or '
                                               'tertiary amine group found'},
                                 {   'smiles': 'O[C@@H]1CC2[C@](C3=C(C4=NCCC([C@@]4(C)CC3)[C@@H](CCC(C(C)C)C)C)CC2)(C)CC1',
                                     'name': 'UCA-1064-B',
                                     'reason': 'No primary, secondary, or '
                                               'tertiary amine group found'},
                                 {   'smiles': 'C1=CC=C(C=C1)N2C(=NN=C2SCC#N)COC3=CC=CC=C3',
                                     'name': '2-[[5-(phenoxymethyl)-4-phenyl-1,2,4-triazol-3-yl]thio]acetonitrile',
                                     'reason': 'No primary, secondary, or '
                                               'tertiary amine group found'},
                                 {   'smiles': 'O=C1C=2OC([C@H]3C[C@H](O)C(=C[C@H]3C2C(=O)C=4C1=C(O)C(=C(O)C4)C)C)(C)C',
                                     'name': 'Unnamed naphterpin 1',
                                     'reason': 'No primary, secondary, or '
                                               'tertiary amine group found'},
                                 {   'smiles': 'O([C@@H]1[C@]2(C([C@@](C1)(CC2)[H])(C)C)C)C(=O)/C=C/C3=CC=C(O)C=C3',
                                     'name': '(1R,4R)-1,7,7-Trimethylbicyclo[2.2.1]heptane-2beta-ol '
                                             '3-(4-hydroxyphenyl)acrylate',
                                     'reason': 'No primary, secondary, or '
                                               'tertiary amine group found'},
                                 {   'smiles': 'CC1(C)CC[C@@]2(CC[C@]3(C)C(=CC[C@@H]4[C@@]5(C)CC[C@H](O)C(C)(C)[C@@H]5CC[C@@]34C)[C@@H]2C1)C([O-])=O',
                                     'name': 'oleanolate',
                                     'reason': 'No primary, secondary, or '
                                               'tertiary amine group found'},
                                 {   'smiles': 'CC(C)(O)[C@H]1CC[C@@]2(C)[C@H]1CC[C@]1(CO)[C@@H]2C[C@@H](O)[C@@H]2[C@@]3(C)CCCC(C)(C)[C@@H]3[C@H](O)C[C@@]12C',
                                     'name': 'hopane-6beta,11alpha,22,27-tetraol',
                                     'reason': 'No primary, secondary, or '
                                               'tertiary amine group found'},
                                 {   'smiles': 'O1C2=C(CC=C(C)C)C(O)=CC(O)=C2C(=O)C=C1C3=CC(OC)=C(O)C(OC)=C3',
                                     'name': 'Baohuosu',
                                     'reason': 'No primary, secondary, or '
                                               'tertiary amine group found'}],
    'sample_false_negatives': [   {   'smiles': 'O[C@@H]1[C@@H](N(C)[C@@H](C1)CCCCCC(O)C)CC2=CC=CC=C2',
                                      'name': 'Preubetain J',
                                      'reason': 'Structure does not match an '
                                                'aralkylamine pattern'},
                                  {   'smiles': 'NC(C(CCCCCCCCCCCC)CC1=CC=CC=C1)(C)C',
                                      'name': '3-benzyl-2-methyl-2-pentadecanamine',
                                      'reason': 'Structure does not match an '
                                                'aralkylamine pattern'},
                                  {   'smiles': 'N1[C@H](CN[C@H](C1)CC2=CC=CC=C2)CC3=CC=CC=C3',
                                      'name': 'Xenocockiamide A',
                                      'reason': 'Structure does not match an '
                                                'aralkylamine pattern'},
                                  {   'smiles': 'NC[C@H](Cl)[C@@H](O)c1c[nH]c(N)n1',
                                      'name': 'girolline',
                                      'reason': 'Structure does not match an '
                                                'aralkylamine pattern'},
                                  {   'smiles': 'CN1CC2C(C(C(C(=C2C=C1)C#N)N)(C#N)C#N)C3=CC=CC=C3',
                                      'name': '6-amino-2-methyl-8-phenyl-1,6,8,8a-tetrahydroisoquinoline-5,7,7-tricarbonitrile',
                                      'reason': 'Structure does not match an '
                                                'aralkylamine pattern'},
                                  {   'smiles': 'N(CCC1=CC=NC=C1)(CC)CC',
                                      'name': 'N1,N1-diethyl-2-(4-pyridyl)ethan-1-amine',
                                      'reason': 'Structure does not match an '
                                                'aralkylamine pattern'},
                                  {   'smiles': 'CC1=CC=C(O1)C(=O)CCNC2=CC(=CC=C2)Br',
                                      'name': '3-(3-bromoanilino)-1-(5-methyl-2-furanyl)-1-propanone',
                                      'reason': 'Structure does not match an '
                                                'aralkylamine pattern'},
                                  {   'smiles': 'Cl.Cl.OC[C@@H](N)CC=1NC=NC1',
                                      'name': 'L-Histidinol dihydrochloride',
                                      'reason': 'Structure does not match an '
                                                'aralkylamine pattern'},
                                  {   'smiles': 'CC1=CC2=NC(SN2N1)NC3=CC=C(C=C3)F',
                                      'name': 'N-(4-fluorophenyl)-6-methyl-2,5-dihydropyrazolo[1,5-b][1,2,4]thiadiazol-2-amine',
                                      'reason': 'No alkyl group directly '
                                                'substituted by aromatic group '
                                                'found'},
                                  {   'smiles': 'N(CCC=1NC=NC1)C',
                                      'name': 'N-alpha-Methylhistamine',
                                      'reason': 'Structure does not match an '
                                                'aralkylamine pattern'}],
    'attempt': 5,
    'reasoning': 'The previous implementation attempted to classify '
                 'aralkylamines by detecting the presence of an amine group '
                 'connected to an alkyl chain, which should be further '
                 'connected to an aromatic group. While this sounds logical, '
                 'the SMARTS pattern used might have been too broad or not '
                 'specific enough to capture all relevant features of an '
                 "aralkylamine structure. Let's analyze the issues and propose "
                 'improvements:\n'
                 '\n'
                 '### Issues:\n'
                 '1. **SMARTS Pattern for Amine**: The use of '
                 '`[NX3;H2,H1,H0;!$(NC=O)]` is correct for finding amines, but '
                 'it might miss certain complex cases where nitrogen is part '
                 'of a larger moiety.\n'
                 '   \n'
                 '2. **Detection of Aromatic Connection**: Simply checking for '
                 'aromatic atoms might not ensure that an aromatic group is '
                 'directly bonded to an alkyl chain which is further connected '
                 'to the nitrogen atom.\n'
                 '   \n'
                 '3. **Broad Connectivity Pattern**: The pattern '
                 '`[NX3][C,c][C,c]*[a]` may not cover some specific ways in '
                 'which the aryl and alkyl groups are connected. \n'
                 '\n'
                 '### Improvements:\n'
                 '- Strengthen the pattern by more explicitly resolving how '
                 'alkyl groups are connected to the aromatic component and '
                 'then to an amine.\n'
                 '- Ensure that the aromatic group is indeed directly attached '
                 'to the alkyl component of the amine, focusing on common '
                 'scenarios for aralkyl bonds.\n'
                 '\n'
                 "Here's how an updated implementation could look:",
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 64,
    'num_false_positives': 8155,
    'num_true_negatives': 134040,
    'num_false_negatives': 41,
    'num_negatives': None,
    'precision': 0.007786835381433264,
    'recall': 0.6095238095238096,
    'f1': 0.015377222489187891,
    'accuracy': 0.9424033731553056,
    'negative_predictive_value': 0.9996942146911195}