"""
Classifies: CHEBI:25409 monoterpenoid
"""
from rdkit import Chem

def is_monoterpenoid(smiles: str):
    """
    Determines if a molecule is a monoterpenoid based on its SMILES string.
    Monoterpenoids are derivatives of monoterpenes, containing a 10-carbon skeleton with potential rearrangements.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if the molecule is a monoterpenoid, False otherwise
        str: Reason for classification
    """
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Monoterpenoid is characterized by having a 10-carbon backbone
    # including cyclic or acyclic structures derived from isoprene units
    monoterpenoid_patterns = [
        Chem.MolFromSmarts("C1CCCCC1"),     # Monocyclic terpenes (like menthane derivatives)
        Chem.MolFromSmarts("C1CCC(C)CC1"),  # Cyclohexane modified by isoprene units
        Chem.MolFromSmarts("C1=CC=CC=C1"),  # Aromatic rings as part of rearrangement
        Chem.MolFromSmarts("C1CCC(C)C1"),   # Simple cyclopentane
        Chem.MolFromSmarts("C2(CC=CC1C2)C1"),  # Bicyclic structures like pinanes
        Chem.MolFromSmarts("C=C(C)C"),      # Acyclic monoterpenes
    ]

    # Functional groups frequently found in monoterpenoids
    functional_group_patterns = [
        Chem.MolFromSmarts("[OX2H]"),       # Hydroxyl group
        Chem.MolFromSmarts("[CX3]=[OX1]"),  # Carbonyl group
        Chem.MolFromSmarts("[CX3](=O)[OX2H1]"),  # Carboxylic acids
        Chem.MolFromSmarts("O=C(O)C"),      # Esters
        Chem.MolFromSmarts("C=CC"),         # Double bonds typical for monoterpenoids
    ]
    
    # Check if the molecule has a monoterpenoid structure and some common functional group modifications
    terpene_match = any(mol.HasSubstructMatch(pattern) for pattern in monoterpenoid_patterns)
    functional_match = any(mol.HasSubstructMatch(pattern) for pattern in functional_group_patterns)

    # Check for carbon count (should closely align with 10 carbons, slight deviations acceptable)
    c_count = sum(1 for atom in mol.GetAtoms() if atom.GetAtomicNum() == 6)

    if terpene_match and functional_match and (9 <= c_count <= 11):
        return True, f"Structure compatible with monoterpenoids: {c_count} carbons, matches patterns."
    
    return False, "Structure is not compatible with typical monoterpenoid patterns."


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:25409',
                          'name': 'monoterpenoid',
                          'definition': 'Any terpenoid derived from a '
                                        'monoterpene. The term includes '
                                        'compounds in which the C10 skeleton '
                                        'of the parent monoterpene has been '
                                        'rearranged or modified by the removal '
                                        'of one or more skeletal atoms '
                                        '(generally methyl groups).',
                          'parents': ['CHEBI:26873'],
                          'xrefs': ['LIPID_MAPS_class:LMPR0102'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 39,
                           'log_lines_of_code': 3.6635616461296463,
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
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 1,
                                                 0,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 0,
                                                 1,
                                                 1,
                                                 0,
                                                 1,
                                                 2,
                                                 1,
                                                 1],
                           'max_indent': 2,
                           'imports': ['from rdkit import Chem'],
                           'imports_count': 1,
                           'methods_called': [   'MolFromSmiles',
                                                 'GetAtomicNum',
                                                 'HasSubstructMatch',
                                                 'MolFromSmarts',
                                                 'GetAtoms'],
                           'methods_called_count': 5,
                           'smarts_strings': [   'O=C(O)C',
                                                 '[OX2H]',
                                                 '"C1CCCCC1"),     # '
                                                 'Monocyclic terpenes (like '
                                                 'menthane derivatives',
                                                 'C1CCC(C)CC1',
                                                 'C=C(C)C',
                                                 'C=CC',
                                                 'C1CCC(C)C1',
                                                 '[CX3]=[OX1]',
                                                 '[CX3](=O)[OX2H1]',
                                                 'C2(CC=CC1C2)C1',
                                                 'C1=CC=CC=C1'],
                           'smarts_strings_count': 11,
                           'defs': ['is_monoterpenoid(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'True, f"Structure compatible with '
                                          'monoterpenoids: {c_count} carbons, '
                                          'matches patterns."',
                                          'False, "Structure is not compatible '
                                          'with typical monoterpenoid '
                                          'patterns."'],
                           'returns_count': 3,
                           'complexity': 2.9327123292259296},
    'message': '\n'
               'Attempt failed: F1 score of 0.1846278975193168 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: '
               'O[C@@]([C@H]1C[C@@H](O)[C@H](C)CC1)(CO)C NAME: '
               '(1R,2R,4R,8S)-(-)-p-menthane-2,8,9-triol REASON: CORRECT '
               'Structure compatible with monoterpenoids: 10 carbons, matches '
               'patterns.\n'
               ' * SMILES: C12CC(C1(C)C)CC=C2C(O)=O NAME: myrtenic acid '
               'REASON: CORRECT Structure compatible with monoterpenoids: 10 '
               'carbons, matches patterns.\n'
               ' * SMILES: C[C@H]1CC[C@@H](C[C@H]1O)C(C)=C NAME: '
               '(-)-neodihydrocarveol REASON: CORRECT Structure compatible '
               'with monoterpenoids: 10 carbons, matches patterns.\n'
               ' * SMILES: C[C@H]1CC[C@@H]([C@H](O)C1)C(C)(C)O NAME: '
               '1alpha,3beta,4beta-p-menthane-3,8-diol REASON: CORRECT '
               'Structure compatible with monoterpenoids: 10 carbons, matches '
               'patterns.\n'
               ' * SMILES: OC1CC(CCC1C)C(O)(CO)C NAME: '
               '(1R,2R,4R,8R)-p-Menthane-2,8,9-triol REASON: CORRECT Structure '
               'compatible with monoterpenoids: 10 carbons, matches patterns.\n'
               ' * SMILES: CC(C)[C@H]1CC[C@H](C)C[C@@H]1O NAME: (+)-menthol '
               'REASON: CORRECT Structure compatible with monoterpenoids: 10 '
               'carbons, matches patterns.\n'
               ' * SMILES: OC(C1CCC(CC1)=C)(C)C NAME: delta-Terpineol REASON: '
               'CORRECT Structure compatible with monoterpenoids: 10 carbons, '
               'matches patterns.\n'
               ' * SMILES: C[C@@H]1CC[C@@H](C[C@H]1O)C(C)=C NAME: '
               '(-)-isodihydrocarveol REASON: CORRECT Structure compatible '
               'with monoterpenoids: 10 carbons, matches patterns.\n'
               ' * SMILES: O[C@@H]1[C@@]2(C[C@@](C(C2=O)(C)C)(C1)[H])C NAME: '
               '6-exo-Hydroxyfenchone REASON: CORRECT Structure compatible '
               'with monoterpenoids: 10 carbons, matches patterns.\n'
               ' * SMILES: C[C@H]1CCC(=C(C)C)C(=O)C1 NAME: (-)-Pulegone '
               'REASON: CORRECT Structure compatible with monoterpenoids: 10 '
               'carbons, matches patterns.\n'
               ' * SMILES: C[C@]12[C@@H]3CC[C@@H](O3)[C@@]1(C)C(=O)OC2=O NAME: '
               'cantharidin REASON: CORRECT Structure compatible with '
               'monoterpenoids: 10 carbons, matches patterns.\n'
               ' * SMILES: O(C(C1CCC(=CC1)C)(C)C)C=O NAME: alpha-Terpineol '
               'formate REASON: CORRECT Structure compatible with '
               'monoterpenoids: 11 carbons, matches patterns.\n'
               ' * SMILES: O[C@@]1([C@@]2(C(C)(C)[C@@H](C1)CC2)C)C NAME: '
               '2-exo-Hydroxy-2-methyl-bornane REASON: CORRECT Structure '
               'compatible with monoterpenoids: 11 carbons, matches patterns.\n'
               ' * SMILES: O=C1CC(CCC1C)C(C)C NAME: Tetrahydrocarvone REASON: '
               'CORRECT Structure compatible with monoterpenoids: 10 carbons, '
               'matches patterns.\n'
               ' * SMILES: [H][C@@]1(CCC(C)=CC1)C(C)(C)O NAME: '
               '(S)-(-)-alpha-terpineol REASON: CORRECT Structure compatible '
               'with monoterpenoids: 10 carbons, matches patterns.\n'
               ' * SMILES: CC1(C)[C@H]2C[C@@H]1C(=C)[C@H](O)C2 NAME: '
               '(-)-trans-pinocarveol REASON: CORRECT Structure compatible '
               'with monoterpenoids: 10 carbons, matches patterns.\n'
               ' * SMILES: CC(CCO)CCC=C(C)C NAME: citronellol REASON: CORRECT '
               'Structure compatible with monoterpenoids: 10 carbons, matches '
               'patterns.\n'
               ' * SMILES: [H][C@]1(CCC(C)=CC1=O)C(C)=C NAME: '
               '(+)-isopiperitenone REASON: CORRECT Structure compatible with '
               'monoterpenoids: 10 carbons, matches patterns.\n'
               ' * SMILES: CC(=C)[C@@H]1CC=C(C)[C@@H](O)C1 NAME: '
               '(-)-trans-carveol REASON: CORRECT Structure compatible with '
               'monoterpenoids: 10 carbons, matches patterns.\n'
               ' * SMILES: CC(CCCC(C)(C)O)C=C NAME: dihydromyrcenol REASON: '
               'CORRECT Structure compatible with monoterpenoids: 10 carbons, '
               'matches patterns.\n'
               ' * SMILES: O=CCC1(C2CC(CC2)C1=C)C NAME: Norbicycloekasantalal '
               'REASON: CORRECT Structure compatible with monoterpenoids: 11 '
               'carbons, matches patterns.\n'
               ' * SMILES: CC(=C)[C@@H]1CCC(=CC1)C(=O)O NAME: '
               '(4R)-4-(1-methylethenyl)-1-cyclohexenecarboxylic acid REASON: '
               'CORRECT Structure compatible with monoterpenoids: 10 carbons, '
               'matches patterns.\n'
               ' * SMILES: O=CCC1(C2(C3C2CC1C3)C)C NAME: Norecasantalal '
               'REASON: CORRECT Structure compatible with monoterpenoids: 11 '
               'carbons, matches patterns.\n'
               ' * SMILES: CC(=C)[C@H]1CC=C(C)[C@H](O)C1 NAME: '
               '(+)-trans-carveol REASON: CORRECT Structure compatible with '
               'monoterpenoids: 10 carbons, matches patterns.\n'
               ' * SMILES: C[C@H](CCO)CCC=C(C)C NAME: (S)-(-)-citronellol '
               'REASON: CORRECT Structure compatible with monoterpenoids: 10 '
               'carbons, matches patterns.\n'
               'False positives: SMILES: OC(=O)C(CCC=C(C)C)C NAME: '
               '2,6-Dimethyl-5-heptenoic acid REASON: WRONGLY CLASSIFIED '
               'Structure compatible with monoterpenoids: 9 carbons, matches '
               'patterns.\n'
               ' * SMILES: C(C(CC([O-])=O)OC(C(C(=O)O)C)=O)[N+](C)(C)C NAME: '
               'O-methylmalonylcarnitine REASON: WRONGLY CLASSIFIED Structure '
               'compatible with monoterpenoids: 11 carbons, matches patterns.\n'
               ' * SMILES: O=C1C=CO[C@]23[C@]1(O2)C(O)CC(C3O)CC NAME: '
               'Epoxynemanione A REASON: WRONGLY CLASSIFIED Structure '
               'compatible with monoterpenoids: 11 carbons, matches patterns.\n'
               ' * SMILES: O=C1C(CC2=C1NCCC2)C NAME: '
               '1,2,3,4,5,6-Hexahydro-6-methyl-7H-cyclopenta[b]pyridin-7-one '
               'REASON: WRONGLY CLASSIFIED Structure compatible with '
               'monoterpenoids: 9 carbons, matches patterns.\n'
               ' * SMILES: O=C(NCC(=O)N[C@@H](C)C(O)=O)[C@@H](N)C(C)C NAME: '
               'Val-Gly-Ala REASON: WRONGLY CLASSIFIED Structure compatible '
               'with monoterpenoids: 10 carbons, matches patterns.\n'
               ' * SMILES: O(C(C)C)C(=O)CC(C)C NAME: Isopropyl '
               '3-methylbutanoate REASON: WRONGLY CLASSIFIED Structure '
               'compatible with monoterpenoids: 8 carbons, matches patterns.\n'
               ' * SMILES: O=C(NC(CC(=O)N)C(O)=O)C(N)CC(C)C NAME: '
               'Leucyl-Asparagine REASON: WRONGLY CLASSIFIED Structure '
               'compatible with monoterpenoids: 10 carbons, matches patterns.\n'
               ' * SMILES: CSCCCC(C(O)C(O)=O)C(O)=O NAME: '
               "3-(3'-Methylthio)propylmalic acid REASON: WRONGLY CLASSIFIED "
               'Structure compatible with monoterpenoids: 8 carbons, matches '
               'patterns.\n'
               ' * SMILES: O([C@@H]1C(O)[C@H](OC)[C@@H](O)C(O)[C@H]1O)C NAME: '
               'Dambonitol REASON: WRONGLY CLASSIFIED Structure compatible '
               'with monoterpenoids: 8 carbons, matches patterns.\n'
               ' * SMILES: [H]C(CCC)=C([H])COC(=O)CC(C)C NAME: 2-hexenyl '
               'isovalerate REASON: WRONGLY CLASSIFIED Structure compatible '
               'with monoterpenoids: 11 carbons, matches patterns.\n'
               ' * SMILES: O=C1OC2CC3CC(C2)CC1C3 NAME: '
               '4-oxahomoadamantan-5-one REASON: WRONGLY CLASSIFIED Structure '
               'compatible with monoterpenoids: 10 carbons, matches patterns.\n'
               ' * SMILES: S([O-])(=O)(=O)CCNC1CCCCC1.[Na+] NAME: '
               'Ethanesulfonic acid, 2-(cyclohexylamino)-, monosodium salt '
               'REASON: WRONGLY CLASSIFIED Structure compatible with '
               'monoterpenoids: 8 carbons, matches patterns.\n'
               ' * SMILES: Nc1ncnc2n(cnc12)[C@@H]1O[C@H](CO)[C@H]1CO NAME: '
               'oxetanocin A REASON: WRONGLY CLASSIFIED Structure compatible '
               'with monoterpenoids: 10 carbons, matches patterns.\n'
               ' * SMILES: OC(=O)C1(C(C(CC1)C(O)=O)(C)C)C NAME: '
               '(+/-)-Camphoric acid REASON: WRONGLY CLASSIFIED Structure '
               'compatible with monoterpenoids: 10 carbons, matches patterns.\n'
               ' * SMILES: C1(CC(C(C(C1)=O)C(=O)CC)=O)C(=O)O NAME: '
               'prohexadione REASON: WRONGLY CLASSIFIED Structure compatible '
               'with monoterpenoids: 10 carbons, matches patterns.\n'
               ' * SMILES: O=C1O[C@@H](C[C@H]2C1=C(O)C[C@@H](O)[C@H]2C)C NAME: '
               '(3R,4aR,5S,6R)-6-hydroxy-5-methylramulosin REASON: WRONGLY '
               'CLASSIFIED Structure compatible with monoterpenoids: 11 '
               'carbons, matches patterns.\n'
               ' * SMILES: O=C(NC)C(C(C)C)(C(C)C)C NAME: '
               'N,2,3-Trimethyl-2-(1-methylethyl)butanamide REASON: WRONGLY '
               'CLASSIFIED Structure compatible with monoterpenoids: 10 '
               'carbons, matches patterns.\n'
               ' * SMILES: [H]C(=O)CC(C)CCCC(C)(C)O NAME: hydroxycitronellal '
               'REASON: WRONGLY CLASSIFIED Structure compatible with '
               'monoterpenoids: 10 carbons, matches patterns.\n'
               ' * SMILES: OC(=O)C1CCC(CC1)C(O)=O NAME: '
               '1,4-cyclohexanedicarboxylic acid REASON: WRONGLY CLASSIFIED '
               'Structure compatible with monoterpenoids: 8 carbons, matches '
               'patterns.\n'
               ' * SMILES: OC(=O)C(CC\\C=C\\C(CC)C)C NAME: '
               '2,7-dimethyl-6-nonenoic acid REASON: WRONGLY CLASSIFIED '
               'Structure compatible with monoterpenoids: 11 carbons, matches '
               'patterns.\n'
               ' * SMILES: C1C2CC3CC1CC(C3=NNC(=S)N)C2 NAME: '
               '(2-adamantylideneamino)thiourea REASON: WRONGLY CLASSIFIED '
               'Structure compatible with monoterpenoids: 11 carbons, matches '
               'patterns.\n'
               " * SMILES: O=C(NCC(C)C)NCC(C)C NAME: N,N'-diisobutylurea "
               'REASON: WRONGLY CLASSIFIED Structure compatible with '
               'monoterpenoids: 9 carbons, matches patterns.\n'
               ' * SMILES: SC[C@H](NC(=O)[C@@H](N)[C@H](CC)C)C(O)=O NAME: '
               'Ile-Cys REASON: WRONGLY CLASSIFIED Structure compatible with '
               'monoterpenoids: 9 carbons, matches patterns.\n'
               ' * SMILES: O=C(NC(C(=N)N)C(C)C)C(N)CCCN NAME: '
               '2,5-diamino-N-(1-amino-1-imino-3-methylbutan-2-yl)pentanamide '
               'REASON: WRONGLY CLASSIFIED Structure compatible with '
               'monoterpenoids: 10 carbons, matches patterns.\n'
               ' * SMILES: CCOC(=O)CC(C)(C)C(C)C NAME: ethyl '
               '3,3,4-trimethylpentanoate REASON: WRONGLY CLASSIFIED Structure '
               'compatible with monoterpenoids: 10 carbons, matches patterns.\n'
               'False negatives: SMILES: C1CO[C@H](C[C@@H]1C)C=C(C)C NAME: '
               '(2R,4R)-rose oxide REASON: MISSED Structure is not compatible '
               'with typical monoterpenoid patterns.\n'
               ' * SMILES: O=C1C(OC)=C(C(=CN)C([C@@]1(CC)C)=O)[C@H](CC)C NAME: '
               'Mycosphine A REASON: MISSED Structure is not compatible with '
               'typical monoterpenoid patterns.\n'
               ' * SMILES: '
               '[N+]([C@@H]1[C@@](CC[C@H]([C@@]1(C=2C=3C(NC2)=CC=CC3)[H])C(C)=C)(C)C=C)#[C-] '
               'NAME: 12-Epi-hapalindole C isoniltrile REASON: MISSED '
               'Structure is not compatible with typical monoterpenoid '
               'patterns.\n'
               ' * SMILES: '
               'CC1(C2CCC1(C(=NNC3=NC(=O)C(=CC4=CC(=CC=C4)Br)S3)C2)C)C NAME: '
               '5-[(3-bromophenyl)methylidene]-2-[2-(4,7,7-trimethyl-3-bicyclo[2.2.1]heptanylidene)hydrazinyl]-4-thiazolone '
               'REASON: MISSED Structure is not compatible with typical '
               'monoterpenoid patterns.\n'
               ' * SMILES: O=C(O)[C@@H](C1=C(CC[C@@H](C(=C1)C)C)C)CCC(=O)O '
               'NAME: Ochracene C REASON: MISSED Structure is not compatible '
               'with typical monoterpenoid patterns.\n'
               ' * SMILES: '
               'OC1(C2C(CC1O)C(=COC2OC3OC(C(O)C(O)C3O)COC(=O)/C=C/C4=CC=C(O)C=C4)C(O)=O)C '
               'NAME: Lippioside I REASON: MISSED Structure is not compatible '
               'with typical monoterpenoid patterns.\n'
               ' * SMILES: OC=1C(C(C)C)=C(C=CC1C(C)C)C NAME: '
               '2,6-Diisopropyl-3-methylphenol REASON: MISSED Structure is not '
               'compatible with typical monoterpenoid patterns.\n'
               ' * SMILES: '
               '[C@@H]1([C@@H]([C@H]([C@@H]([C@H](O1)CO)O)O)O)O[C@@]23[C@]4([C@@](C2)([C@@]5(O[C@]4(O[C@]3(C5)C)[H])OS(O)(=O)=O)[H])COC(C6=CC=CC=C6)=O '
               'NAME: paeoniflorin sulfonate REASON: MISSED Structure is not '
               'compatible with typical monoterpenoid patterns.\n'
               ' * SMILES: O=C(O)/C=C(/CC/C=C(/CCC(=O)OC)\\C)\\C NAME: '
               '(2E,6E)-10-methoxy-3,7-dimethyl-10-oxodeca-2,6-dienoic acid '
               'REASON: MISSED Structure is not compatible with typical '
               'monoterpenoid patterns.\n'
               ' * SMILES: O(C(CCC=C(C)C)(C)C=C)C(=O)CC1=CC=CC=C1 NAME: '
               'Linalyl phenylacetate REASON: MISSED Structure is not '
               'compatible with typical monoterpenoid patterns.\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'O1[C@H]([C@@H](O)CC=2C1=CC=CC2)C3=CC=CC=C3',
                                     'name': 'cis-(+)-3-Flavanol',
                                     'reason': 'Structure is not compatible '
                                               'with typical monoterpenoid '
                                               'patterns.'},
                                 {   'smiles': 'O1C2C34C(C(N(CC3)C)CC5=C4C1=C(OC)C=C5)C=CC2OC',
                                     'name': '6-O-Methylcodeine',
                                     'reason': 'Structure is not compatible '
                                               'with typical monoterpenoid '
                                               'patterns.'},
                                 {   'smiles': 'CN1C2=C(C=CC(=C2)OC)C3=C1[C@H](N(CC34CCN(CC4)S(=O)(=O)C5=CC=CS5)CC6CC6)CO',
                                     'name': "[(1S)-2-(cyclopropylmethyl)-7-methoxy-9-methyl-1'-thiophen-2-ylsulfonyl-1-spiro[1,3-dihydropyrido[3,4-b]indole-4,4'-piperidine]yl]methanol",
                                     'reason': 'Structure is not compatible '
                                               'with typical monoterpenoid '
                                               'patterns.'},
                                 {   'smiles': 'O(C(=O)CCCCCCCCCCCCCCC)[C@@H](COC(=O)CCCCCCCCCCCCCCCCCCC)COC(=O)CCCCCCC',
                                     'name': 'TG(20:0/16:0/8:0)',
                                     'reason': 'Structure is not compatible '
                                               'with typical monoterpenoid '
                                               'patterns.'},
                                 {   'smiles': 'O[C@@H]1CC2[C@](C3=C(C4=NCCC([C@@]4(C)CC3)[C@@H](CCC(C(C)C)C)C)CC2)(C)CC1',
                                     'name': 'UCA-1064-B',
                                     'reason': 'Structure is not compatible '
                                               'with typical monoterpenoid '
                                               'patterns.'},
                                 {   'smiles': 'C1=CC=C(C=C1)N2C(=NN=C2SCC#N)COC3=CC=CC=C3',
                                     'name': '2-[[5-(phenoxymethyl)-4-phenyl-1,2,4-triazol-3-yl]thio]acetonitrile',
                                     'reason': 'Structure is not compatible '
                                               'with typical monoterpenoid '
                                               'patterns.'},
                                 {   'smiles': 'O=C1C=2OC([C@H]3C[C@H](O)C(=C[C@H]3C2C(=O)C=4C1=C(O)C(=C(O)C4)C)C)(C)C',
                                     'name': 'Unnamed naphterpin 1',
                                     'reason': 'Structure is not compatible '
                                               'with typical monoterpenoid '
                                               'patterns.'},
                                 {   'smiles': 'O([C@@H]1[C@]2(C([C@@](C1)(CC2)[H])(C)C)C)C(=O)/C=C/C3=CC=C(O)C=C3',
                                     'name': '(1R,4R)-1,7,7-Trimethylbicyclo[2.2.1]heptane-2beta-ol '
                                             '3-(4-hydroxyphenyl)acrylate',
                                     'reason': 'Structure is not compatible '
                                               'with typical monoterpenoid '
                                               'patterns.'},
                                 {   'smiles': 'CC1(C)CC[C@@]2(CC[C@]3(C)C(=CC[C@@H]4[C@@]5(C)CC[C@H](O)C(C)(C)[C@@H]5CC[C@@]34C)[C@@H]2C1)C([O-])=O',
                                     'name': 'oleanolate',
                                     'reason': 'Structure is not compatible '
                                               'with typical monoterpenoid '
                                               'patterns.'},
                                 {   'smiles': 'C[C@@H]1CN(C(=O)C2=C(N=CC(=C2)C3=CCCCC3)O[C@@H]1CN(C)CC4=CC=C(C=C4)C(=O)O)[C@H](C)CO',
                                     'name': '4-[[[(2S,3R)-8-(1-cyclohexenyl)-5-[(2R)-1-hydroxypropan-2-yl]-3-methyl-6-oxo-3,4-dihydro-2H-pyrido[2,3-b][1,5]oxazocin-2-yl]methyl-methylamino]methyl]benzoic '
                                             'acid',
                                     'reason': 'Structure is not compatible '
                                               'with typical monoterpenoid '
                                               'patterns.'}],
    'sample_false_negatives': [   {   'smiles': 'O=C1C(OC)=C(C(=CN)C([C@@]1(CC)C)=O)[C@H](CC)C',
                                      'name': 'Mycosphine A',
                                      'reason': 'Structure is not compatible '
                                                'with typical monoterpenoid '
                                                'patterns.'},
                                  {   'smiles': '[N+]([C@@H]1[C@@](CC[C@H]([C@@]1(C=2C=3C(NC2)=CC=CC3)[H])C(C)=C)(C)C=C)#[C-]',
                                      'name': '12-Epi-hapalindole C '
                                              'isoniltrile',
                                      'reason': 'Structure is not compatible '
                                                'with typical monoterpenoid '
                                                'patterns.'},
                                  {   'smiles': 'CC1(C2CCC1(C(=NNC3=NC(=O)C(=CC4=CC(=CC=C4)Br)S3)C2)C)C',
                                      'name': '5-[(3-bromophenyl)methylidene]-2-[2-(4,7,7-trimethyl-3-bicyclo[2.2.1]heptanylidene)hydrazinyl]-4-thiazolone',
                                      'reason': 'Structure is not compatible '
                                                'with typical monoterpenoid '
                                                'patterns.'},
                                  {   'smiles': 'O=C(O)[C@@H](C1=C(CC[C@@H](C(=C1)C)C)C)CCC(=O)O',
                                      'name': 'Ochracene C',
                                      'reason': 'Structure is not compatible '
                                                'with typical monoterpenoid '
                                                'patterns.'},
                                  {   'smiles': 'OC1(C2C(CC1O)C(=COC2OC3OC(C(O)C(O)C3O)COC(=O)/C=C/C4=CC=C(O)C=C4)C(O)=O)C',
                                      'name': 'Lippioside I',
                                      'reason': 'Structure is not compatible '
                                                'with typical monoterpenoid '
                                                'patterns.'},
                                  {   'smiles': 'OC=1C(C(C)C)=C(C=CC1C(C)C)C',
                                      'name': '2,6-Diisopropyl-3-methylphenol',
                                      'reason': 'Structure is not compatible '
                                                'with typical monoterpenoid '
                                                'patterns.'},
                                  {   'smiles': '[C@@H]1([C@@H]([C@H]([C@@H]([C@H](O1)CO)O)O)O)O[C@@]23[C@]4([C@@](C2)([C@@]5(O[C@]4(O[C@]3(C5)C)[H])OS(O)(=O)=O)[H])COC(C6=CC=CC=C6)=O',
                                      'name': 'paeoniflorin sulfonate',
                                      'reason': 'Structure is not compatible '
                                                'with typical monoterpenoid '
                                                'patterns.'},
                                  {   'smiles': 'O=C(O)/C=C(/CC/C=C(/CCC(=O)OC)\\C)\\C',
                                      'name': '(2E,6E)-10-methoxy-3,7-dimethyl-10-oxodeca-2,6-dienoic '
                                              'acid',
                                      'reason': 'Structure is not compatible '
                                                'with typical monoterpenoid '
                                                'patterns.'},
                                  {   'smiles': 'O(C(CCC=C(C)C)(C)C=C)C(=O)CC1=CC=CC=C1',
                                      'name': 'Linalyl phenylacetate',
                                      'reason': 'Structure is not compatible '
                                                'with typical monoterpenoid '
                                                'patterns.'},
                                  {   'smiles': 'C(C/C=C/CCC1=CC=C(C(C)C)C=C1)(C)C',
                                      'name': '1-Isopropyl-4-[(3E)-6-methyl-3-hepten-1-yl]benzene',
                                      'reason': 'Structure is not compatible '
                                                'with typical monoterpenoid '
                                                'patterns.'}],
    'attempt': 5,
    'reasoning': 'To improve the classification of monoterpenoids, we need to '
                 'address several issues highlighted by the outcomes:\n'
                 '\n'
                 '1. **Carbons Count Refinement**: Monoterpenoids are expected '
                 'to have a C10 backbone, but rearrangements might lead to '
                 'fewer (due to methyl removal) or slightly more carbons if '
                 'the functional groups are considered. The carbon count '
                 'checks should be stricter to avoid false positives.\n'
                 '\n'
                 '2. **Pattern Matching Improvement**: The initial patterns '
                 'might be too simplistic. We need more specific patterns that '
                 'represent common cyclic and acyclic monoterpenoid structures '
                 'and their modifications.\n'
                 '\n'
                 '3. **Addition of Explicit Checks for Certain Functional '
                 'Groups and Rearrangements**: Many false negatives suggest '
                 'that beyond the generic patterns, specific rearrangements or '
                 "functional modifications weren't properly captured.\n"
                 '\n'
                 "Let's implement a refined version considering these points:",
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 273,
    'num_false_positives': 917,
    'num_true_negatives': 140453,
    'num_false_negatives': 657,
    'num_negatives': None,
    'precision': 0.22941176470588234,
    'recall': 0.29354838709677417,
    'f1': 0.25754716981132075,
    'accuracy': 0.9889388615600844,
    'negative_predictive_value': 0.995344057827227}