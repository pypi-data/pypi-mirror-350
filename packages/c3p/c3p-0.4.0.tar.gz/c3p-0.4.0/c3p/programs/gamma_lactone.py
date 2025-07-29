"""
Classifies: CHEBI:37581 gamma-lactone
"""
from rdkit import Chem

def is_gamma_lactone(smiles: str):
    """
    Determines if a molecule is a gamma-lactone based on its SMILES string.
    A gamma-lactone is characterized by the presence of a five-membered lactone ring; various substituents and 
    structural variations such as double bonds or stereochemistry centers are considered.
    
    Args:
        smiles (str): SMILES string of the molecule.

    Returns:
        bool: True if the molecule is a gamma-lactone, False otherwise.
        str: Explanation for the classification decision.
    """

    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Define a comprehensive SMARTS pattern for gamma-lactone structure
    # Pattern is flexible to allow various substitutions and structural flexibilities
    gamma_lactone_patterns = [
        Chem.MolFromSmarts("O=C1OCC=C1"),   # Open double bond lactone
        Chem.MolFromSmarts("O=C1OCCC1"),    # Basic lactone
        Chem.MolFromSmarts("O=C1OC=C[CH2]1"), # Lactone with alternative ring saturation
        Chem.MolFromSmarts("O=C1OC(=O)C=C1"),  # Highly oxidized lactone
        Chem.MolFromSmarts("O=C1OC(C)=CC1")  # Substituted gamma lactone
        # More patterns can be added if other configurations are frequently found
    ]

    for pattern in gamma_lactone_patterns:
        if mol.HasSubstructMatch(pattern):
            return True, "Contains a five-membered lactone ring characteristic of gamma-lactones"

    return False, "No five-membered lactone ring found"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:37581',
                          'name': 'gamma-lactone',
                          'definition': 'A lactone having a five-membered '
                                        'lactone ring.',
                          'parents': ['CHEBI:25000'],
                          'xrefs': ['PMID:18789684'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 28,
                           'log_lines_of_code': 3.332204510175204,
                           'indent_by_line': [   1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 0,
                                                 1,
                                                 2,
                                                 2,
                                                 1,
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
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 1,
                                                 0,
                                                 1,
                                                 2,
                                                 3,
                                                 0,
                                                 1],
                           'max_indent': 3,
                           'imports': ['from rdkit import Chem'],
                           'imports_count': 1,
                           'methods_called': [   'HasSubstructMatch',
                                                 'MolFromSmiles',
                                                 'MolFromSmarts'],
                           'methods_called_count': 3,
                           'smarts_strings': [   'O=C1OCC=C1',
                                                 'O=C1OC(=O)C=C1',
                                                 'O=C1OCCC1',
                                                 'O=C1OC(C)=CC1',
                                                 'O=C1OC=C[CH2]1'],
                           'smarts_strings_count': 5,
                           'defs': ['is_gamma_lactone(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'True, "Contains a five-membered '
                                          'lactone ring characteristic of '
                                          'gamma-lactones"',
                                          'False, "No five-membered lactone '
                                          'ring found"'],
                           'returns_count': 3,
                           'complexity': 2.666440902035041},
    'message': '\n'
               'Attempt failed: F1 score of 0.10137457044673541 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: CCCCCCC[C@H]1CCC(=O)O1 NAME: '
               'gamma-undecanolactone REASON: CORRECT Contains a five-membered '
               'lactone ring characteristic of gamma-lactones\n'
               ' * SMILES: CCCCC[C@H]1CCC(=O)O1 NAME: gamma-nonanolactone '
               'REASON: CORRECT Contains a five-membered lactone ring '
               'characteristic of gamma-lactones\n'
               ' * SMILES: O=C1O[C@H](C=2OC([C@H](OC)C)=CC2)CC1 NAME: '
               '5-{5-[(R)-1-methoxyethyl]furan-2-yl}dihydrofuran-2(3H)-one '
               'REASON: CORRECT Contains a five-membered lactone ring '
               'characteristic of gamma-lactones\n'
               ' * SMILES: O1C(CCC1=O)(CCCC)CCCC NAME: '
               '5,5-Dibutyl-4,5-dihydro-2(3H)furanone REASON: CORRECT Contains '
               'a five-membered lactone ring characteristic of gamma-lactones\n'
               ' * SMILES: '
               'COC(=O)CCc1c(C)c2=CC3=[N+]4C(=Cc5c(C)c(C=C)c6C=C7[N+]8=C(C=c1n2[Fe--]48n56)[C@]1(CCC(=O)O1)[C@@]7(C)O)C(C=C)=C3C '
               'NAME: cis-heme d hydroxychlorin gamma-spirolactone methyl '
               'ester REASON: CORRECT Contains a five-membered lactone ring '
               'characteristic of gamma-lactones\n'
               ' * SMILES: C1(OC(=O)CC1)CCCCCC NAME: gamma-decalactone REASON: '
               'CORRECT Contains a five-membered lactone ring characteristic '
               'of gamma-lactones\n'
               ' * SMILES: '
               'CC(C)(COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12)[C@@H](O)C(=O)NCCC(=O)NCCSC(=O)CC1CCC(=O)O1 '
               'NAME: 5-oxo-furan-2-acetyl-CoA REASON: CORRECT Contains a '
               'five-membered lactone ring characteristic of gamma-lactones\n'
               ' * SMILES: O1C(CCC1=O)C/C=C/CCCCC NAME: '
               'Dihydro-5-(2-octenyl)-2(3H)-furanone REASON: CORRECT Contains '
               'a five-membered lactone ring characteristic of gamma-lactones\n'
               ' * SMILES: C=1C(=CC(=C(C1O)O)O)CC2CCC(O2)=O NAME: '
               "5-(3',4',5'-trihydroxyphenyl)-gamma-valerolactone REASON: "
               'CORRECT Contains a five-membered lactone ring characteristic '
               'of gamma-lactones\n'
               ' * SMILES: O=C1O[C@H](C=2OC([C@H](O)C)=CC2)CC1 NAME: '
               '5-[5-(1-Hydroxyethyl)furan-2-yl]dihydrofuran-2(3H)-one REASON: '
               'CORRECT Contains a five-membered lactone ring characteristic '
               'of gamma-lactones\n'
               ' * SMILES: O=C1O[C@@H](CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC)CC1 '
               'NAME: (S)-4-hentriacontyl-dihydrofuran-2-one REASON: CORRECT '
               'Contains a five-membered lactone ring characteristic of '
               'gamma-lactones\n'
               ' * SMILES: O=C1O[C@@H]([C@H](OC(=O)CC2=CC=CC=C2)C)CC1 NAME: '
               '1-(5-oxotetrahydrofuran-2-yl)ethyl 2-phenylacetate REASON: '
               'CORRECT Contains a five-membered lactone ring characteristic '
               'of gamma-lactones\n'
               ' * SMILES: O=C1O[C@@H](CCCCC(C)C)CC1 NAME: '
               '9-Methyldecano-4-lactone REASON: CORRECT Contains a '
               'five-membered lactone ring characteristic of gamma-lactones\n'
               ' * SMILES: O1C(CCC1=O)CC/C=C/CC=C NAME: '
               '7E,10-undecadien-4-olide REASON: CORRECT Contains a '
               'five-membered lactone ring characteristic of gamma-lactones\n'
               ' * SMILES: O1[C@H](CCCCCC)CCC1=O NAME: (R)-gamma-Decalactone '
               'REASON: CORRECT Contains a five-membered lactone ring '
               'characteristic of gamma-lactones\n'
               ' * SMILES: O=C1O[C@]([C@@]2(CC=C(C)[C@H](C2)O)C)(C)CC1 NAME: '
               'Isopolisin B REASON: CORRECT Contains a five-membered lactone '
               'ring characteristic of gamma-lactones\n'
               ' * SMILES: '
               '[H][C@]12CC[C@]3(C)[C@]([H])(CC[C@@]3(C)[C@@]1([H])CC[C@@]([H])([C@](C)(O)CO)[C@@]1(CCC(=O)O1)C2)[C@H](C)C(O)=O '
               'NAME: lancifodilactone F REASON: CORRECT Contains a '
               'five-membered lactone ring characteristic of gamma-lactones\n'
               ' * SMILES: O=C1O[C@@H](CCCCCC(C)C)CC1 NAME: '
               '10-Methylundecan-4-olide REASON: CORRECT Contains a '
               'five-membered lactone ring characteristic of gamma-lactones\n'
               ' * SMILES: C(C=1C=C(C(=CC1)O)OS(O)(=O)=O)C2CCC(O2)=O NAME: '
               "5-(3',4'-dihydroxyphenyl)-gamma-valerolactone 3'-O-sulfate "
               'REASON: CORRECT Contains a five-membered lactone ring '
               'characteristic of gamma-lactones\n'
               ' * SMILES: O=C1O[C@]([C@@H]2CC=C(C(=O)O)CC2)(C)CC1 NAME: '
               'Polisin A REASON: CORRECT Contains a five-membered lactone '
               'ring characteristic of gamma-lactones\n'
               ' * SMILES: '
               'C=1(C=C(C=CC1)CC2CCC(O2)=O)O[C@H]3[C@@H]([C@H]([C@@H]([C@H](O3)C(O)=O)O)O)O '
               'NAME: '
               "5-(3'-hydroxyphenyl)-gamma-valerolactone-3'-O-beta-D-glucuronide "
               'REASON: CORRECT Contains a five-membered lactone ring '
               'characteristic of gamma-lactones\n'
               ' * SMILES: O1C(CCC1=O)C(O)C NAME: Sherry lactone REASON: '
               'CORRECT Contains a five-membered lactone ring characteristic '
               'of gamma-lactones\n'
               ' * SMILES: '
               'Cc1c(C=C)c2C=C3[N+]4=C(C=c5c(CCC(O)=O)c(C)c6=CC7=[N+]8C(=Cc1n2[Fe--]48n56)C(C=C)=C7C)[C@@]1(CCC(=O)O1)[C@@]3(C)O '
               'NAME: trans-heme d hydroxychlorin gamma-spirolactone REASON: '
               'CORRECT Contains a five-membered lactone ring characteristic '
               'of gamma-lactones\n'
               " * SMILES: C=C1CCC(=O)O1 NAME: alpha'-angelica lactone REASON: "
               'CORRECT Contains a five-membered lactone ring characteristic '
               'of gamma-lactones\n'
               ' * SMILES: O=C1O[C@H](CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC)CC1 '
               'NAME: Acrocarpunilactone REASON: CORRECT Contains a '
               'five-membered lactone ring characteristic of gamma-lactones\n'
               'False positives: SMILES: '
               'O=C1O[C@]([C@@H](O)CC/C(=C/CC/C(=C/CC2=C(O)C=CC(=C2)C(=O)O)/C)/C)(C)CC1 '
               'NAME: Erythrolic acid C REASON: WRONGLY CLASSIFIED Contains a '
               'five-membered lactone ring characteristic of gamma-lactones\n'
               ' * SMILES: SC1C2C(C3(CCC(C=C3C1)=O)C)CCC4(C2CCC45OC(=O)CC5)C '
               'NAME: 7 -thiospironolactone REASON: WRONGLY CLASSIFIED '
               'Contains a five-membered lactone ring characteristic of '
               'gamma-lactones\n'
               ' * SMILES: '
               'CC(=O)O[C@H](CC\\C(C)=C\\[C@@H](O)C\\C(C)=C\\CCc1ccoc1)[C@]1(C)CCC(=O)O1 '
               'NAME: 15-acetylirciformonin B REASON: WRONGLY CLASSIFIED '
               'Contains a five-membered lactone ring characteristic of '
               'gamma-lactones\n'
               ' * SMILES: '
               'O=C1C2=C(O)C=C(C)C=C2[C@H](O)[C@]34[C@]1(O)C(=O)[C@H](C=5C=6O[C@@](C(=O)OC)([C@H]7OC(=O)CC7)CC(C6C(=CC5C3)O)=O)C=C4 '
               'NAME: Xanthoquinodin B8 REASON: WRONGLY CLASSIFIED Contains a '
               'five-membered lactone ring characteristic of gamma-lactones\n'
               ' * SMILES: O=C1O[C@H]([C@H](O)/C=C/C(O)CCCCCC)CC1 NAME: '
               'Pseudonocardide E REASON: WRONGLY CLASSIFIED Contains a '
               'five-membered lactone ring characteristic of gamma-lactones\n'
               ' * SMILES: '
               'O=C1C=C2C(C3C(C4C(C5(OC(=O)CC5)CC4)(C)CC3)CC2)(C)CC1 NAME: '
               "10,13-dimethylspiro[2,6,7,8,9,11,12,14,15,16-decahydro-1H-cyclopenta[a]phenanthrene-17,5'-oxolane]-2',3-dione "
               'REASON: WRONGLY CLASSIFIED Contains a five-membered lactone '
               'ring characteristic of gamma-lactones\n'
               ' * SMILES: '
               'O=C1C2=C(O)C3=C(O)C=C(C)C=C3[C@@H]([C@]24C=C[C@H]1C5=C(O)C6=C(O[C@@](C(=O)OC)([C@H]7OC(=O)CC7)CC6=O)C=C5C4)O '
               'NAME: Xanthoquinodin A4 REASON: WRONGLY CLASSIFIED Contains a '
               'five-membered lactone ring characteristic of gamma-lactones\n'
               ' * SMILES: C1(=C(C(=C(C(=C1O)C)C)O)C)CCC2(CCC(=O)O2)C NAME: '
               'alpha-tocopheronolactone REASON: WRONGLY CLASSIFIED Contains a '
               'five-membered lactone ring characteristic of gamma-lactones\n'
               ' * SMILES: O=C1O[C@H](C(=O)[C@H](O)/C=C\\CCCCCC)CC1 NAME: '
               'Pseudonocardide F REASON: WRONGLY CLASSIFIED Contains a '
               'five-membered lactone ring characteristic of gamma-lactones\n'
               ' * SMILES: O=C1O[C@]([C@H]2C[C@H](O)[C@H](C)CC2)(C)CC1 NAME: '
               'Polisin C REASON: WRONGLY CLASSIFIED Contains a five-membered '
               'lactone ring characteristic of gamma-lactones\n'
               ' * SMILES: '
               'O=C1OC(CC[C@H](OC(=O)/C=C/[C@@H](O)CC[C@H](O)C)C)CC1 NAME: '
               'Seco-Dihydropyrenophorin-1,4-lactone REASON: WRONGLY '
               'CLASSIFIED Contains a five-membered lactone ring '
               'characteristic of gamma-lactones\n'
               ' * SMILES: '
               'O=C1O[C@H]([C@@H](O)[C@@H]2O[C@H]2[C@H](O)/C=C\\C#CC#CC#C)CC1 '
               'NAME: Collimonin A REASON: WRONGLY CLASSIFIED Contains a '
               'five-membered lactone ring characteristic of gamma-lactones\n'
               ' * SMILES: '
               'CC12CCC(=O)C=C1CC(C3C24C(O4)CC5(C3CCC56CCC(=O)O6)C)C(=O)OC '
               'NAME: LSM-1524 REASON: WRONGLY CLASSIFIED Contains a '
               'five-membered lactone ring characteristic of gamma-lactones\n'
               ' * SMILES: '
               'C=1C(=CC(=C(C1)OC2[C@@H](O)O[C@H]([C@@H]([C@H]2O)O)C(O)=O)OC)CC3CCC(O3)=O '
               'NAME: '
               "5-(3',4'-Dihydroxyphenyl)-gamma-valerolactone-3'-O-methyl-4'-O-glucuronide "
               'REASON: WRONGLY CLASSIFIED Contains a five-membered lactone '
               'ring characteristic of gamma-lactones\n'
               ' * SMILES: '
               'O=C1C2=C(O[C@@](C1)(C(=O)OC)[C@H]3OC(=O)CC3)C(C4=C(O)C5=C(O[C@](C(=O)OC)([C@H](O)CCC(=O)OC)CC5=O)C=C4C)=C(C)C=C2O '
               'NAME: Noduliprevenone REASON: WRONGLY CLASSIFIED Contains a '
               'five-membered lactone ring characteristic of gamma-lactones\n'
               ' * SMILES: '
               'O=C1C2=C([C@@]3(C(=O)C[C@@H]([C@]3(C1)C)C4(OC(=O)CC4)C)C)[C@@H](O)C[C@@H]5[C@@]2(CC[C@@H](C5(C)C)O)C '
               'NAME: Ganolactone B REASON: WRONGLY CLASSIFIED Contains a '
               'five-membered lactone ring characteristic of gamma-lactones\n'
               ' * SMILES: O1[C@@]([C@H](O)CCCCCC)(CCC1=O)[H] NAME: '
               '5R-hydroxy-4R-decanolide REASON: WRONGLY CLASSIFIED Contains a '
               'five-membered lactone ring characteristic of gamma-lactones\n'
               ' * SMILES: '
               'O=C1C2=C(O[C@]([C@]1(O)CC(=O)C)([C@H]3OC(=O)CC3)C)C=C(CO)C=C2O '
               'NAME: Lachnone E REASON: WRONGLY CLASSIFIED Contains a '
               'five-membered lactone ring characteristic of gamma-lactones\n'
               ' * SMILES: '
               'S(=O)(C1C(O)C2=CC(=O)CCC2(C)C3C1C4C(C5(OC(=O)CC5)CC4)(C)CC3)C '
               'NAME: '
               "5-hydroxy-4-methanesulfinyl-9a,11a-dimethyl-3,3a,3b,4,5,8,9,9b,10,11-decahydro-2H-spiro[cyclopenta[a]phenanthrene-1,2'-oxolane]-5',7-dione "
               'REASON: WRONGLY CLASSIFIED Contains a five-membered lactone '
               'ring characteristic of gamma-lactones\n'
               ' * SMILES: '
               'S(=O)(=O)(C1C2C(C3(CCC(C=C3C1)=O)C)CCC4(C2CCC45OC(=O)CC5)C)C '
               'NAME: '
               "4-methanesulfonyl-9a,11a-dimethyl-3,3a,3b,4,5,8,9,9b,10,11-decahydro-2H-spiro[cyclopenta[a]phenanthrene-1,2'-oxolane]-5',7-dione "
               'REASON: WRONGLY CLASSIFIED Contains a five-membered lactone '
               'ring characteristic of gamma-lactones\n'
               ' * SMILES: [O-]C(=O)[C@@H]1CCC(=O)O1 NAME: '
               '(S)-alpha-hydroxyglutarate-gamma-lactone REASON: WRONGLY '
               'CLASSIFIED Contains a five-membered lactone ring '
               'characteristic of gamma-lactones\n'
               ' * SMILES: '
               '[H][C@]12CC[C@@]3(C)[C@@]([H])([C@@H]4C[C@@H]4[C@@]33CCC(=O)O3)[C@]1([H])[C@H]1C[C@H]1C1=CC(=O)CC[C@]21C '
               'NAME: drospirenone REASON: WRONGLY CLASSIFIED Contains a '
               'five-membered lactone ring characteristic of gamma-lactones\n'
               ' * SMILES: O1C(CC(O)CCCCCCC)CCC1=O NAME: '
               '6-hydroxy-4-tridecanolide REASON: WRONGLY CLASSIFIED Contains '
               'a five-membered lactone ring characteristic of gamma-lactones\n'
               ' * SMILES: '
               'O([C@]1(C/C=C\\CCCCC)/C(/C(=O)C=C1)=C\\C=C\\[C@@H]2OC(=O)CC2)C(=O)C '
               'NAME: clavulolactone II REASON: WRONGLY CLASSIFIED Contains a '
               'five-membered lactone ring characteristic of gamma-lactones\n'
               ' * SMILES: O=C1C(=C(C)[C@]2([C@@H]1CCCC)OC(=O)CC2)C NAME: '
               '(-)-(4S,8S)-foedanolide REASON: WRONGLY CLASSIFIED Contains a '
               'five-membered lactone ring characteristic of gamma-lactones\n'
               'False negatives: SMILES: '
               'CO[C@H]1[C@H](O[C@@H]2OC=C([C@H]3[C@@H]4O[C@@H]4[C@]4(OC(=O)C(=C4)C(=O)c4ccc(OC)c(O)c4)[C@@H]23)C(=O)OC)O[C@H](CO)[C@@H](O)[C@@H]1O '
               'NAME: citrifolinoside REASON: MISSED No five-membered lactone '
               'ring found\n'
               ' * SMILES: O=C1OCC(=C1/C=C/C=C/C)[C@@H](O)C NAME: Kobifuranone '
               'B REASON: MISSED No five-membered lactone ring found\n'
               ' * SMILES: O=C1O/C(=C\\CC)/C=C1CCCO NAME: Bombardolide B '
               'REASON: MISSED No five-membered lactone ring found\n'
               ' * SMILES: '
               'O=C1OCC=2[C@]13[C@]([C@@]4(O)CC(C)(C)C[C@H]4C2)(C)C3 NAME: '
               '2a,13-Dihydroxy-marasm-7(8)-en-5-oic acid REASON: MISSED No '
               'five-membered lactone ring found\n'
               ' * SMILES: O=C1O[C@@H](CCOC(=O)C)C=C1CCC NAME: '
               'Pregaliellactone E REASON: MISSED No five-membered lactone '
               'ring found\n'
               ' * SMILES: '
               '[H][C@]12CC[C@]3([H])[C@]([H])(C[C@@H](O)[C@]4(C)[C@H](CC[C@]34O)C3=CC(=O)OC3)[C@@]1(C)CC[C@@H](C2)O[C@H]1C[C@H](O)[C@H](O)[C@@H](C)O1 '
               'NAME: digoxigenin monodigitoxoside REASON: MISSED No '
               'five-membered lactone ring found\n'
               ' * SMILES: '
               '[P@]1(=O)(OC(=C2C(=O)OC[C@@H]2CO1)C)OCCCCCCCCCCCCC(O)CCC NAME: '
               'Cyclipostin B REASON: MISSED No five-membered lactone ring '
               'found\n'
               ' * SMILES: '
               '[H]C(=O)O[C@H]1C[C@]2(O)[C@]3([H])CC[C@]4([H])C[C@H](CC[C@]4(C)[C@@]3([H])CC[C@]2(C)[C@@]1([H])C1=CC(=O)OC1)O[C@H]1C[C@H](O)[C@H](O[C@H]2C[C@H](O)[C@H](O[C@H]3C[C@H](O)[C@H](O)[C@@H](C)O3)[C@@H](C)O2)[C@@H](C)O1 '
               'NAME: gitaloxin REASON: MISSED No five-membered lactone ring '
               'found\n'
               ' * SMILES: '
               'O1[C@]2([C@]([C@@H](C1=O)C)([C@@H](OC(=O)C)CC(=C3[C@@]2(C(=CC3=O)C)[H])C)[H])[H] '
               'NAME: Matricarin REASON: MISSED No five-membered lactone ring '
               'found\n'
               ' * SMILES: ClC(C=1C(=O)O[C@H](C1)[C@@H](O)C)C(O)C NAME: '
               '8-Chloro-9-hydroxy-8,9-deoxyasperlactone REASON: MISSED No '
               'five-membered lactone ring found\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': '[H][C@@]1(O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O)O[C@@H]1[C@@H](O)[C@@H](O)[C@@H](CO)O[C@H]1OC[C@H]1O[C@@H](OC[C@H]2O[C@@H](OC[C@H](NC(=O)[C@H](O)CCCCCCCCCCCCCCCCCCCCCC)[C@H](O)[C@H](O)CCCCCCCCCCCCCC)[C@H](O)[C@@H](O)[C@H]2O)[C@H](O)[C@@H](O)[C@H]1O',
                                     'name': 'Neurosporaside',
                                     'reason': 'No five-membered lactone ring '
                                               'found'},
                                 {   'smiles': '[O-]C(=O)C1=CN(C2CC2)C2=CC(N3CC[NH2+]CC3)=C(F)C=C2C1=O',
                                     'name': 'ciprofloxacin zwitterion',
                                     'reason': 'No five-membered lactone ring '
                                               'found'},
                                 {   'smiles': 'O=C1NC(=CC2=C1O[C@H]([C@@H](O)CC(C)C)O2)C',
                                     'name': 'Dihydroisoflavipucine',
                                     'reason': 'No five-membered lactone ring '
                                               'found'},
                                 {   'smiles': 'O=C1N2C(C(=O)N([C@@]2(OC)C)C[C@@H](O)C3=CC=CC=C3)=CC4=C1N(C=5C=CC=CC45)C',
                                     'name': 'Marinacarboline K',
                                     'reason': 'No five-membered lactone ring '
                                               'found'},
                                 {   'smiles': 'O1[C@@H](O[C@H]2[C@@H](O)[C@H](O)[C@H](O[C@@H]2OC[C@H]3OC(O)[C@@H](O)[C@@H](O)[C@@H]3O)CO)[C@H](NC(=O)C)[C@@H](O)[C@H](O[C@@H]4O[C@@H]([C@H](O)[C@H](O)[C@H]4O)CO[C@]5(O[C@H]([C@H](NC(=O)C)[C@@H](O)C5)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]1CO',
                                     'name': '(2R,4S,5R,6R)-5-Acetamido-2-[[(2R,3R,4S,5R,6S)-6-[(2R,3S,4R,5R,6S)-5-acetamido-6-[(2S,3S,4S,5S,6R)-4,5-dihydroxy-6-(hydroxymethyl)-2-[[(2R,3S,4S,5S)-3,4,5,6-tetrahydroxyoxan-2-yl]methoxy]oxan-3-yl]oxy-4-hydroxy-2-(hydroxymethyl)oxan-3-yl]oxy-3,4,5-trihydroxyoxan-2-yl]methoxy]-4-hydroxy-6-[(1R,2R)-1,2,3-trihydroxypropyl]oxane-2-carboxylic '
                                             'acid',
                                     'reason': 'No five-membered lactone ring '
                                               'found'},
                                 {   'smiles': 'O(C(=O)CCCCCCC)CCC1=CC=CC=C1',
                                     'name': '2-Phenylethyl octanoate',
                                     'reason': 'No five-membered lactone ring '
                                               'found'},
                                 {   'smiles': 'P(OCC(OC(=O)CCCCCCC/C=C\\CCCCCCCC)COC(=O)CCC/C=C\\C/C=C\\C/C=C\\CCCCCCCC)(OCCNC)(O)=O',
                                     'name': 'PE-NMe(20:3(5Z,8Z,11Z)/18:1(9Z))',
                                     'reason': 'No five-membered lactone ring '
                                               'found'},
                                 {   'smiles': 'O=C1C2=C(OC=3C1=CC=CN3)C(Cl)=CC(=C2)C=4NN=NN4',
                                     'name': 'traxanox',
                                     'reason': 'No five-membered lactone ring '
                                               'found'},
                                 {   'smiles': 'CCCCC(C)CCCCCC(C)CCCCCCCCCC(C)CC(O)=O',
                                     'name': '3,13,19-trimethyltricosanoic '
                                             'acid',
                                     'reason': 'No five-membered lactone ring '
                                               'found'},
                                 {   'smiles': 'COC(CC1=CC[C@]2(C)[C@@H](C)CCC[C@]2(C)C1=O)OC',
                                     'name': 'aignopsane ketal',
                                     'reason': 'No five-membered lactone ring '
                                               'found'}],
    'sample_false_negatives': [   {   'smiles': 'OC1=CC=C2C3(OC(C4=C3C=CC=C4)=O)C=5C(OC2=C1O)=C(C(=CC5)O)O',
                                      'name': 'gallein',
                                      'reason': 'No five-membered lactone ring '
                                                'found'},
                                  {   'smiles': 'CC1(C)C(=O)Oc2ccc(OS(C)(=O)=O)cc12',
                                      'name': 'ethofumesate-2-keto',
                                      'reason': 'No five-membered lactone ring '
                                                'found'},
                                  {   'smiles': '[H][C@]12CC[C@](C)(O)[C@@H](CC3=CC(=O)C=C(OC)C3=O)[C@]1(C)CC[C@@]1([H])[C@]3(C)CCC[C@]21COC3=O',
                                      'name': 'strongylophorine-26',
                                      'reason': 'No five-membered lactone ring '
                                                'found'},
                                  {   'smiles': 'CC\\C=C1/OC(=O)c2c1cc(O)c(O)c2C',
                                      'name': 'purpurester B',
                                      'reason': 'No five-membered lactone ring '
                                                'found'},
                                  {   'smiles': 'Clc1c2COC(=O)c2c(Cl)c(Cl)c1Cl',
                                      'name': '4,5,6,7-tetrachloro-2-benzofuran-1(3H)-one',
                                      'reason': 'No five-membered lactone ring '
                                                'found'},
                                  {   'smiles': 'Oc1ccc(cc1O)\\C=C1/C=C(OC1=O)c1ccc(O)c(O)c1',
                                      'name': 'BE-23372M',
                                      'reason': 'No five-membered lactone ring '
                                                'found'},
                                  {   'smiles': 'O=C1OCc2ccccc12',
                                      'name': '2-benzofuran-1(3H)-one',
                                      'reason': 'No five-membered lactone ring '
                                                'found'},
                                  {   'smiles': 'C\\C=C\\c1c(O)c(O)cc2OC(=O)[C@](C)(NC(=O)\\C=C\\C(O)=O)c12',
                                      'name': 'fumimycin',
                                      'reason': 'No five-membered lactone ring '
                                                'found'},
                                  {   'smiles': '[H]C(OCC)=C1N=C(OC1=O)c1ccco1',
                                      'name': '4-(ethoxymethylene)-2-(2-furyl)oxazol-5-one',
                                      'reason': 'No five-membered lactone ring '
                                                'found'},
                                  {   'smiles': 'C[C@@H](O)[C@@H]1N\\C(OC1=O)=N/c1ncnc2n(cnc12)[C@@H]1O[C@H](CO)[C@@H](O)[C@H]1O',
                                      'name': 'cyclic '
                                              'N(6)-threonylcarbamoyladenosine',
                                      'reason': 'No five-membered lactone ring '
                                                'found'}],
    'attempt': 3,
    'reasoning': 'The previous attempt to identify gamma-lactones based on '
                 'their SMILES strings appears to have shortcomings in its '
                 'SMARTS pattern definition. The pattern exclusively searches '
                 'for an unsubstituted and aliphatic five-membered ring, '
                 'whereas gamma-lactones in reality can have substituents and '
                 'may also feature double bonds or additional functionalities. '
                 'Additionally, the pattern used might not account for '
                 'aromatic characteristics and might not capture variations in '
                 'stereochemistry or expanded/literally translated SMILES for '
                 'some lactone structures.\n'
                 '\n'
                 'To improve the classification:\n'
                 '\n'
                 '1. **SMARTS Pattern Expansion**: Revise the SMARTS pattern '
                 'to account for variations such as double bonds in the '
                 'five-membered ring, stereo-centers, and aromaticity. '
                 'Incorporating a more flexible pattern allows identification '
                 'of various forms of lactone rings.\n'
                 '   \n'
                 '2. **Comprehensive Substructure Search**: Implement checks '
                 'for multiple possible configurations of the gamma-lactone '
                 'that can arise due to different functional groups or ring '
                 'junctions.\n'
                 '\n'
                 '3. **Iterative Testing**: Conduct iterative testing using '
                 'known true and false SMILES to refine the SMARTS pattern and '
                 'clarify decision logic.\n'
                 '\n'
                 "Here's the revised code that addresses these points:",
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 942,
    'num_false_positives': 2606,
    'num_true_negatives': 138721,
    'num_false_negatives': 31,
    'num_negatives': None,
    'precision': 0.26550169109357385,
    'recall': 0.9681397738951696,
    'f1': 0.4167219641672196,
    'accuracy': 0.9814687280393535,
    'negative_predictive_value': 0.9997765797970479}