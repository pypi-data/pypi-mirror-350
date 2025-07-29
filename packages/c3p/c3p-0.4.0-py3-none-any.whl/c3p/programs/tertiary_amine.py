"""
Classifies: CHEBI:32876 tertiary amine
"""
"""
Classifies: tertiary amine
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_tertiary_amine(smiles: str):
    """
    Determines if a molecule is a tertiary amine based on its SMILES string.
    A tertiary amine is a nitrogen atom bonded to three carbon atoms.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a tertiary amine, False otherwise
        str: Reason for classification
    """
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Get all N atoms
    nitrogen_atoms = [atom for atom in mol.GetAtoms() if atom.GetAtomicNum() == 7]

    if not nitrogen_atoms:
      return False, "No nitrogen atoms found"
    
    # check if each N is bonded to exactly three C's
    found_tertiary_amine = False
    for atom in nitrogen_atoms:
        carbon_neighbors = 0
        for neighbor in atom.GetNeighbors():
            if neighbor.GetAtomicNum() == 6:
                carbon_neighbors += 1
            elif neighbor.GetAtomicNum() == 7 or neighbor.GetAtomicNum() == 8 or neighbor.GetAtomicNum() == 16 or neighbor.GetAtomicNum() == 1: # N,O,S or H
                pass
            else:
                 return False, "Nitrogen atom is not only attached to carbon." # Added check for other heteroatoms/H
        
        if carbon_neighbors == 3:
            found_tertiary_amine = True
        elif carbon_neighbors < 3 or carbon_neighbors > 3:
            return False, "Nitrogen atom is not a tertiary amine"

    if found_tertiary_amine:
       return True, "Tertiary amine"
    else:
        return False, "No tertiary amine found"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:32876',
                          'name': 'tertiary amine',
                          'definition': 'A compound formally derived from '
                                        'ammonia by replacing three hydrogen '
                                        'atoms by hydrocarbyl groups.',
                          'parents': ['CHEBI:32952', 'CHEBI:50996'],
                          'xrefs': ['KEGG:C02196'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 36,
                           'log_lines_of_code': 3.58351893845611,
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
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 3,
                                                 4,
                                                 3,
                                                 4,
                                                 3,
                                                 3,
                                                 2,
                                                 2,
                                                 3,
                                                 2,
                                                 3,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 2],
                           'max_indent': 4,
                           'imports': [   'from rdkit import Chem',
                                          'from rdkit.Chem import AllChem'],
                           'imports_count': 2,
                           'methods_called': [   'MolFromSmiles',
                                                 'GetNeighbors',
                                                 'GetAtomicNum',
                                                 'GetAtoms'],
                           'methods_called_count': 4,
                           'smarts_strings': [],
                           'smarts_strings_count': 0,
                           'defs': ['is_tertiary_amine(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "No nitrogen atoms found"',
                                          'False, "Nitrogen atom is not only '
                                          'attached to carbon." # Added check '
                                          'for other heteroatoms/H',
                                          'False, "Nitrogen atom is not a '
                                          'tertiary amine"',
                                          'True, "Tertiary amine"',
                                          'False, "No tertiary amine found"'],
                           'returns_count': 6,
                           'complexity': 3.716703787691222},
    'message': '\n'
               'Attempt failed: F1 score of 0.003691171947093202 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: CCN(CC)[C@H](C)C(=O)c1ccccc1 NAME: '
               '(R)-diethylpropion REASON: CORRECT Tertiary amine\n'
               ' * SMILES: '
               'COc1cc(C=C)cc2c1c1cc(OC)c3c(O)ccc(C4O[C@H](C)[C@H](OC(C)=O)[C@@H]([C@H]4O)N(C)C)c3c1oc2=O '
               'NAME: ravidomycin REASON: CORRECT Tertiary amine\n'
               ' * SMILES: '
               '[H][C@@]12CC\\C(C)=C\\CC\\C(=C\\CC\\C(C)=C\\[C@]1([H])OC(=O)[C@H]2CN(C)C)C(O)=O '
               'NAME: 17-dimethylaminolobohedleolide REASON: CORRECT Tertiary '
               'amine\n'
               ' * SMILES: CC(CN1c2ccccc2Sc2ccc(cc12)C(C)=O)N(C)C NAME: '
               'aceprometazine REASON: CORRECT Tertiary amine\n'
               ' * SMILES: CN(C)CCOC(C)(c1ccccc1)c1ccccn1 NAME: doxylamine '
               'REASON: CORRECT Tertiary amine\n'
               ' * SMILES: '
               '[Br-].[Br-].[H]C(=Cc1cc[n+](CCC[N+](CC)(CC)CC)cc1)c1ccc(cc1)N(CCCC)CCCC '
               'NAME: FM 1-43 dye REASON: CORRECT Tertiary amine\n'
               ' * SMILES: CN(C)CCO NAME: N,N-dimethylethanolamine REASON: '
               'CORRECT Tertiary amine\n'
               ' * SMILES: CN1CCC(CC1)=C1c2ccccc2CCc2cccnc12 NAME: azatadine '
               'REASON: CORRECT Tertiary amine\n'
               ' * SMILES: CCN(CC)[C@@H](C)C(=O)c1ccccc1 NAME: '
               '(S)-diethylpropion REASON: CORRECT Tertiary amine\n'
               ' * SMILES: COc1ccc2Sc3ccccc3N(C[C@H](C)CN(C)C)c2c1 NAME: '
               'methotrimeprazine REASON: CORRECT Tertiary amine\n'
               ' * SMILES: C[C@H](CN1CCCCC1)Cc1ccc(cc1)C(C)(C)C NAME: '
               '(S)-fenpropidin REASON: CORRECT Tertiary amine\n'
               ' * SMILES: CN(C)CCc1c[nH]c2ccc(CS(=O)(=O)N3CCCC3)cc12 NAME: '
               'almotriptan REASON: CORRECT Tertiary amine\n'
               ' * SMILES: CCCN(CCC)CCc1cccc2NC(=O)Cc12 NAME: ropinirole '
               'REASON: CORRECT Tertiary amine\n'
               ' * SMILES: '
               'CC(C)(C(O)=O)c1ccc(cc1)C(O)CCCN1CCC(CC1)C(O)(c1ccccc1)c1ccccc1 '
               'NAME: fexofenadine REASON: CORRECT Tertiary amine\n'
               ' * SMILES: '
               '[H][C@@]12CC[C@@]3(OC(C)=O)[C@@]4([H])C[C@]5([H])[C@@]6(C)CC[C@H](OC)C5(C4N(CC)C6)[C@]([H])(C1)[C@]3([H])C(=O)O2 '
               'NAME: 8-acetoxyheterophyllisine REASON: CORRECT Tertiary '
               'amine\n'
               ' * SMILES: CCN(CCCc1ccccc1)CCCc1ccccc1 NAME: alverine REASON: '
               'CORRECT Tertiary amine\n'
               ' * SMILES: CCCCN(C)C NAME: N,N-dimethylbutylamine REASON: '
               'CORRECT Tertiary amine\n'
               ' * SMILES: '
               'CCCCN(CCCC)CC(O)c1cc(Cl)cc2\\C(=C/c3ccc(Cl)cc3)c3cc(Cl)ccc3-c12 '
               'NAME: lumefantrine REASON: CORRECT Tertiary amine\n'
               ' * SMILES: CN1CCC(CC1)=C1c2ccccc2C=Cc2ccccc12 NAME: '
               'cyproheptadine REASON: CORRECT Tertiary amine\n'
               ' * SMILES: CN(C)c1ncnc2[nH]cnc12 NAME: '
               'N(6),N(6)-dimethyladenine REASON: CORRECT Tertiary amine\n'
               ' * SMILES: CC(C=C(c1cccs1)c1cccs1)N(C)C NAME: '
               'dimethylthiambutene REASON: CORRECT Tertiary amine\n'
               ' * SMILES: '
               'C1=CC=CC=2SC(=[N+](C12)C)C(=C3C=C(N(C4=CC=CC=C34)C=5C=CC=CC5)N(CCCN(C)C)CCCN(C)C)[H] '
               'NAME: PicoGreen REASON: CORRECT Tertiary amine\n'
               ' * SMILES: CCSC(=O)N(CC(C)C)CC(C)C NAME: Butylate REASON: '
               'CORRECT Tertiary amine\n'
               ' * SMILES: '
               'C1=CC=CC=2SC(=[N+](C12)C)/C=C/3\\C=C(N(C4=CC=CC=C34)C=5C=CC=CC5)N(CCCN(C)C)CCC '
               'NAME: SYBR Green I REASON: CORRECT Tertiary amine\n'
               ' * SMILES: CN(C)CCc1c[nH]c2ccc(O)cc12 NAME: bufotenin REASON: '
               'CORRECT Tertiary amine\n'
               'False positives: SMILES: '
               'CCS(=O)(=O)N1CC2(C1)[C@@H]([C@@H](N2C(=O)C3CCCC3)CO)C4=CC=C(C=C4)C=CC '
               'NAME: LSM-38092 REASON: WRONGLY CLASSIFIED Tertiary amine\n'
               ' * SMILES: '
               'C1CCN(CC1)C(=O)C[C@H]2C[C@@H]3[C@H]([C@@H](O2)CO)OC4=C3C=C(C=C4)NC(=O)CC5CC5 '
               'NAME: '
               'N-[(1S,3R,4aS,9aR)-1-(hydroxymethyl)-3-[2-oxo-2-(1-piperidinyl)ethyl]-3,4,4a,9a-tetrahydro-1H-pyrano[3,4-b]benzofuran-6-yl]-2-cyclopropylacetamide '
               'REASON: WRONGLY CLASSIFIED Tertiary amine\n'
               ' * SMILES: CN1C[C@@H]2C[C@H](Cn3c2cccc3=O)[C@H]1CC=C NAME: '
               'Tinctorine REASON: WRONGLY CLASSIFIED Tertiary amine\n'
               ' * SMILES: '
               'CN1CCN(CC1)C(=O)C[C@@H]2CC[C@H]3[C@H](O2)COC[C@@H](CN3C(=O)NC4=CC5=C(C=C4)OCO5)O '
               'NAME: '
               '(3R,6aS,8S,10aS)-N-(1,3-benzodioxol-5-yl)-3-hydroxy-8-[2-(4-methyl-1-piperazinyl)-2-oxoethyl]-3,4,6,6a,8,9,10,10a-octahydro-2H-pyrano[2,3-c][1,5]oxazocine-1-carboxamide '
               'REASON: WRONGLY CLASSIFIED Tertiary amine\n'
               ' * SMILES: '
               'C[C@@H]1CN([C@@H](COC2=C(C=C(C=C2)NC(=O)C3CCCCC3)C(=O)N(C[C@H]1OC)C)C)CC4=NC=CS4 '
               'NAME: '
               'N-[(4R,7R,8S)-8-methoxy-4,7,10-trimethyl-11-oxo-5-(2-thiazolylmethyl)-2-oxa-5,10-diazabicyclo[10.4.0]hexadeca-1(12),13,15-trien-14-yl]cyclohexanecarboxamide '
               'REASON: WRONGLY CLASSIFIED Tertiary amine\n'
               ' * SMILES: '
               'C[C@H]1CN([C@H](COC2=C(C=C(C=C2)NC(=O)C3CC3)C(=O)N(C[C@@H]1OC)C)C)C(=O)CC4=CC=CC=N4 '
               'NAME: '
               'N-[(4S,7S,8R)-8-methoxy-4,7,10-trimethyl-11-oxo-5-[1-oxo-2-(2-pyridinyl)ethyl]-2-oxa-5,10-diazabicyclo[10.4.0]hexadeca-1(12),13,15-trien-14-yl]cyclopropanecarboxamide '
               'REASON: WRONGLY CLASSIFIED Tertiary amine\n'
               ' * SMILES: Cc1ccc(cc1)C(=O)c1ccc(CC(O)=O)n1C NAME: tolmetin '
               'REASON: WRONGLY CLASSIFIED Tertiary amine\n'
               ' * SMILES: '
               'CCCOC1=CC=C(C=C1)NC(=O)C2CC(=O)N=C(S2)NN=C(C)C=CC3=CC=C(C=C3)N(C)C '
               'NAME: '
               '2-[2-[4-[4-(dimethylamino)phenyl]but-3-en-2-ylidene]hydrazinyl]-4-oxo-N-(4-propoxyphenyl)-5,6-dihydro-1,3-thiazine-6-carboxamide '
               'REASON: WRONGLY CLASSIFIED Tertiary amine\n'
               ' * SMILES: '
               '[I-].[I-].[H]C(=C1C=CN(CCC[N+](C)(C)C)c2ccccc12)c1sc2ccccc2[n+]1C '
               'NAME: To-Pro-1 REASON: WRONGLY CLASSIFIED Tertiary amine\n'
               ' * SMILES: '
               'CC(=O)N[C@@H]1[C@@H](O)[C@@H](OS(O)(=O)=O)[C@@H](COS(O)(=O)=O)OC1OP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1O)n1ccc(=O)[nH]c1=O '
               'NAME: UDP-N-acetyl-D-galactosamine 4,6-bissulfate REASON: '
               'WRONGLY CLASSIFIED Tertiary amine\n'
               ' * SMILES: '
               'O=C1N2[C@@H]3N4C=5C=CC=CC5[C@]3(C[C@H]6[C@]4(CC[C@@H]7[C@@]6(CCCC7(C)C)C)C)C[C@H]2C(=O)N([C@H]1C(C)C)C '
               'NAME: Drimentine I REASON: WRONGLY CLASSIFIED Tertiary amine\n'
               ' * SMILES: CC1=CN2C=CC=C2C=N1 NAME: '
               '3-methylpyrrolo[1,2-a]pyrazine REASON: WRONGLY CLASSIFIED '
               'Tertiary amine\n'
               ' * SMILES: '
               'C[C@@H]1CN(C(=O)C2=CC=CC=C2C3=CC=CC=C3CO[C@H]1CN(C)C(=O)NC4=CC=C(C=C4)F)[C@H](C)CO '
               'NAME: LSM-8749 REASON: WRONGLY CLASSIFIED Tertiary amine\n'
               ' * SMILES: CCOC(=O)C1=CC=C(C=C1)NC(=O)N2CCCCCC2 NAME: '
               '4-[[1-azepanyl(oxo)methyl]amino]benzoic acid ethyl ester '
               'REASON: WRONGLY CLASSIFIED Tertiary amine\n'
               ' * SMILES: '
               'C[C@@H]1CN(C(=O)C2=C(C(=CC=C2)N(C)C)O[C@H]1CN(C)C(=O)NC3CCCCC3)[C@H](C)CO '
               'NAME: '
               '3-cyclohexyl-1-[[(2R,3R)-10-(dimethylamino)-5-[(2R)-1-hydroxypropan-2-yl]-3-methyl-6-oxo-3,4-dihydro-2H-1,5-benzoxazocin-2-yl]methyl]-1-methylurea '
               'REASON: WRONGLY CLASSIFIED Tertiary amine\n'
               ' * SMILES: '
               'C[C@@H]1CN(C(=O)C2=C(N=CC(=C2)C#C[C@H](C)O)O[C@@H]1CN(C)C(=O)NC3=CC=C(C=C3)C(F)(F)F)[C@H](C)CO '
               'NAME: '
               '1-[[(2S,3R)-8-[(3S)-3-hydroxybut-1-ynyl]-5-[(2R)-1-hydroxypropan-2-yl]-3-methyl-6-oxo-3,4-dihydro-2H-pyrido[2,3-b][1,5]oxazocin-2-yl]methyl]-1-methyl-3-[4-(trifluoromethyl)phenyl]urea '
               'REASON: WRONGLY CLASSIFIED Tertiary amine\n'
               ' * SMILES: '
               'C1C2=CC=CC=C2[C@@H]3[C@](C(=O)N1CCS(=O)(=O)C4=CC=CC=C4)(N=C(O3)C5=CC=C(C=C5)OCCCO)CC6=CC=CC=C6 '
               'NAME: '
               '(3aR,10bR)-5-[2-(benzenesulfonyl)ethyl]-2-[4-(3-hydroxypropoxy)phenyl]-3a-(phenylmethyl)-6,10b-dihydrooxazolo[4,5-d][2]benzazepin-4-one '
               'REASON: WRONGLY CLASSIFIED Tertiary amine\n'
               ' * SMILES: '
               'O=C1N(C(=O)[C@H]2N(C(=O)[C@@H](N(C(=O)[C@@H](NC(=O)[C@@H](N(C(=O)[C@@H](C[C@@H](CCCC)C)C)C)C=C(C)C)[C@H](OC(=O)C)C)C)C(C)C)CCC2)[C@@H](C)C=C1 '
               'NAME: Microcolin E REASON: WRONGLY CLASSIFIED Tertiary amine\n'
               ' * SMILES: '
               '[H]C(=C([H])c1cc(c2ccc(cc2[o+]1)N(CC)CC)C(C)(C)C)C([H])=C1N(CCCS([O-])(=O)=O)c2ccc(cc2C1(C)CCCC(O)=O)S([O-])(=O)=O '
               'NAME: DY-681(1-) REASON: WRONGLY CLASSIFIED Tertiary amine\n'
               ' * SMILES: '
               'C[C@H]1CN(C(=O)C2=CC=CC=C2C3=CC=CC=C3CO[C@@H]1CN(C)C(=O)NC4=CC=CC=C4C(F)(F)F)[C@@H](C)CO '
               'NAME: LSM-10338 REASON: WRONGLY CLASSIFIED Tertiary amine\n'
               ' * SMILES: '
               'C1CCN(CC1)CCNC(=O)C[C@@H]2CC[C@H]3[C@H](O2)COC[C@@H](CN3)O '
               'NAME: '
               '2-[(3R,6aS,8S,10aS)-3-hydroxy-1,2,3,4,6,6a,8,9,10,10a-decahydropyrano[2,3-c][1,5]oxazocin-8-yl]-N-[2-(1-piperidinyl)ethyl]acetamide '
               'REASON: WRONGLY CLASSIFIED Tertiary amine\n'
               ' * SMILES: CC[N+]1=C(OC2=CC=CC=C21)C=C3CC(CC(=C3)C)(C)C NAME: '
               '3-ethyl-2-[(3,5,5-trimethyl-1-cyclohex-2-enylidene)methyl]-1,3-benzoxazol-3-ium '
               'REASON: WRONGLY CLASSIFIED Tertiary amine\n'
               ' * SMILES: '
               'CCCN(C)C[C@H]1[C@H](CN(C(=O)C2=C(C=CC(=C2)NC(=O)NC3=CC=C(C=C3)F)O[C@H](CCCCO1)C)[C@H](C)CO)C '
               'NAME: '
               '1-(4-fluorophenyl)-3-[(3S,9R,10S)-12-[(2R)-1-hydroxypropan-2-yl]-3,10-dimethyl-9-[[methyl(propyl)amino]methyl]-13-oxo-2,8-dioxa-12-azabicyclo[12.4.0]octadeca-1(14),15,17-trien-16-yl]urea '
               'REASON: WRONGLY CLASSIFIED Tertiary amine\n'
               ' * SMILES: '
               'CN1CCN(CC1)C2=C(C=C(C=C2)Cl)NC(=O)C3=CC(=CC=C3)S(=O)(=O)N(C)C '
               'NAME: '
               'N-[5-chloro-2-(4-methyl-1-piperazinyl)phenyl]-3-(dimethylsulfamoyl)benzamide '
               'REASON: WRONGLY CLASSIFIED Tertiary amine\n'
               ' * SMILES: '
               'C1CCN(CC1)CCC(=O)NCC[C@@H]2CC[C@@H]([C@H](O2)CO)NC(=O)C3CCOCC3 '
               'NAME: '
               'N-[(2S,3S,6S)-2-(hydroxymethyl)-6-[2-[[1-oxo-3-(1-piperidinyl)propyl]amino]ethyl]-3-oxanyl]-4-oxanecarboxamide '
               'REASON: WRONGLY CLASSIFIED Tertiary amine\n'
               'False negatives: SMILES: O=C(/N=[N+](\\[O-])/C1=CC=C(O)C=C1)N '
               'NAME: 4-hydroxyphenyl-1-ONN-azoxyformamide REASON: MISSED Not '
               'a tertiary amine\n'
               ' * SMILES: '
               'C/C(=C\\CC\\C(\\C)=C\\C[C@]12C(C=C(C([C@H]1O2)OC(C)=O)C)=O)/CCCC(C)(C)O '
               'NAME: yanuthone M REASON: MISSED No nitrogen atoms found\n'
               ' * SMILES: '
               'O=C(O)/C=C/C=C/C1=CC=C(N=[N+]([O-])C2=CC=C(/C=C/C=C/C(=O)N[C@H](C(=O)O)CCC(=O)N)C=C2)C=C1 '
               'NAME: Azoxymycin B REASON: MISSED Not a tertiary amine\n'
               ' * SMILES: '
               'O=C(NC(C(=O)O)CCC(=O)N)/C=C/C=C/C1=CC=C([N+]([O-])=NC2=CC=C(/C=C/C=C/C(=O)NC(C(=O)O)CCC(=O)N)C=C2)C=C1 '
               'NAME: Azoxymycin A REASON: MISSED Not a tertiary amine\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'CCN1N=C(N=N1)C2=CC=CC=C2NC(=O)C3=CC=C(C=C3)N4C=NN=N4',
                                     'name': 'N-[2-(2-ethyl-5-tetrazolyl)phenyl]-4-(1-tetrazolyl)benzamide',
                                     'reason': 'Nitrogen atom is not a '
                                               'tertiary amine'},
                                 {   'smiles': 'CCS(=O)(=O)N1CC2(C1)[C@@H]([C@@H](N2C(=O)C3CCCC3)CO)C4=CC=C(C=C4)C=CC',
                                     'name': 'LSM-38092',
                                     'reason': 'Nitrogen atom is not a '
                                               'tertiary amine'},
                                 {   'smiles': 'O=C/1N/C(/C(=O)N\\C1=C\\C2=CC=CC=C2)=C\\C=3N=CNC3C(C=C)(C)C',
                                     'name': 'DeltaPLH',
                                     'reason': 'Nitrogen atom is not a '
                                               'tertiary amine'},
                                 {   'smiles': 'C1CCN(CC1)C(=O)C[C@H]2C[C@@H]3[C@H]([C@@H](O2)CO)OC4=C3C=C(C=C4)NC(=O)CC5CC5',
                                     'name': 'N-[(1S,3R,4aS,9aR)-1-(hydroxymethyl)-3-[2-oxo-2-(1-piperidinyl)ethyl]-3,4,4a,9a-tetrahydro-1H-pyrano[3,4-b]benzofuran-6-yl]-2-cyclopropylacetamide',
                                     'reason': 'Nitrogen atom is not a '
                                               'tertiary amine'},
                                 {   'smiles': 'C[C@H]1C[C@@]2(OC(=O)c3ccccc3)[C@H]([C@H]1OC(C)=O)[C@@H](O)\\C(C)=C/C[C@H]1[C@@H](\\C=C(C)\\C2=O)C1(C)C',
                                     'name': '(-)-(6Z,12E,2S,3S,4R,5R,9S,11S,15R)-3-acetoxy-15-benzoyloxylathyra-6,12-dien-5-ol-14-one',
                                     'reason': 'No nitrogen atoms found'},
                                 {   'smiles': 'O=C1C(O)=CC=2O[C@]3([C@H](O)C[C@@H]4[C@](OC=5C=C(O)C(C=C(C5C4)C)=O)(CC=CC(C[C@H]3CC2C(=C1)C)(C)C)C)C',
                                     'name': 'Eupenifeldin',
                                     'reason': 'No nitrogen atoms found'},
                                 {   'smiles': 'O1[C@@H](O[C@@H]2[C@@H](OC[C@H]3O[C@@H](O[C@H]4[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]4CO)O[C@H]5[C@H](O)[C@@H](NC(=O)C)C(O[C@@H]5CO[C@@H]6O[C@H]([C@@H](O)[C@@H](O)[C@@H]6O)C)O)[C@@H](O)[C@@H](O[C@H]7O[C@@H]([C@@H](O)[C@H](O)[C@@H]7O[C@@H]8O[C@@H]([C@@H](O[C@@H]9O[C@@H]([C@H](O)[C@H](O)[C@H]9NC(=O)C)CO)[C@H](O)[C@H]8NC(=O)C)CO)CO)[C@@H]3O)O[C@@H]([C@@H](O)[C@@H]2O)CO)[C@H](NC(=O)C)[C@@H](O[C@@H]%10O[C@H]([C@@H](O)[C@@H](O)[C@@H]%10O)C)[C@H](O[C@@H]%11O[C@@H]([C@H](O)[C@H](O)[C@H]%11NC(=O)C)CO)[C@H]1CO',
                                     'name': 'N-[(3R,4R,5S,6R)-5-[(2S,3R,4R,5S,6R)-3-Acetamido-5-[(2S,3S,4S,5R,6R)-4-[(2R,3S,4S,5S,6R)-3-[(2S,3R,4R,5S,6R)-3-acetamido-5-[(2S,3R,4R,5R,6R)-3-acetamido-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-6-[[(2S,3S,4S,5S,6R)-3-[(2S,3R,4R,5S,6R)-3-acetamido-5-[(2S,3R,4R,5R,6R)-3-acetamido-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-6-(hydroxymethyl)-4-[(2R,3S,4R,5S,6S)-3,4,5-trihydroxy-6-methyloxan-2-yl]oxyoxan-2-yl]oxy-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxymethyl]-3,5-dihydroxyoxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-2,4-dihydroxy-6-[[(2R,3S,4R,5S,6S)-3,4,5-trihydroxy-6-methyloxan-2-yl]oxymethyl]oxan-3-yl]acetamide',
                                     'reason': 'Nitrogen atom is not a '
                                               'tertiary amine'},
                                 {   'smiles': 'CCC1=C2COC(CC2=C3C(=C(OC3=N1)C(=O)C4=CC=CC=C4)N)(C)C',
                                     'name': 'LSM-4563',
                                     'reason': 'Nitrogen atom is not a '
                                               'tertiary amine'},
                                 {   'smiles': 'CN1CCN(CC1)C(=O)C[C@@H]2CC[C@H]3[C@H](O2)COC[C@@H](CN3C(=O)NC4=CC5=C(C=C4)OCO5)O',
                                     'name': '(3R,6aS,8S,10aS)-N-(1,3-benzodioxol-5-yl)-3-hydroxy-8-[2-(4-methyl-1-piperazinyl)-2-oxoethyl]-3,4,6,6a,8,9,10,10a-octahydro-2H-pyrano[2,3-c][1,5]oxazocine-1-carboxamide',
                                     'reason': 'Nitrogen atom is not a '
                                               'tertiary amine'},
                                 {   'smiles': 'CC(C(=O)NN=C(C1=CC=CC=C1)C2=CC=CC=C2)NC3CCCCC3',
                                     'name': '2-(cyclohexylamino)-N-[(diphenylmethylene)amino]propanamide',
                                     'reason': 'Nitrogen atom is not a '
                                               'tertiary amine'}],
    'sample_false_negatives': [   {   'smiles': 'CN(C)CCOC(C)(c1ccccc1)c1ccccn1',
                                      'name': 'doxylamine',
                                      'reason': 'Nitrogen atom is not a '
                                                'tertiary amine'},
                                  {   'smiles': 'O=C(/N=[N+](\\[O-])/C1=CC=C(O)C=C1)N',
                                      'name': '4-hydroxyphenyl-1-ONN-azoxyformamide',
                                      'reason': 'Nitrogen atom is not a '
                                                'tertiary amine'},
                                  {   'smiles': '[Br-].[Br-].[H]C(=Cc1cc[n+](CCC[N+](CC)(CC)CC)cc1)c1ccc(cc1)N(CCCC)CCCC',
                                      'name': 'FM 1-43 dye',
                                      'reason': 'Nitrogen atom is not a '
                                                'tertiary amine'},
                                  {   'smiles': 'CN1CCC(CC1)=C1c2ccccc2CCc2cccnc12',
                                      'name': 'azatadine',
                                      'reason': 'Nitrogen atom is not a '
                                                'tertiary amine'},
                                  {   'smiles': 'CN(C)CCc1c[nH]c2ccc(CS(=O)(=O)N3CCCC3)cc12',
                                      'name': 'almotriptan',
                                      'reason': 'Nitrogen atom is not a '
                                                'tertiary amine'},
                                  {   'smiles': 'CCCN(CCC)CCc1cccc2NC(=O)Cc12',
                                      'name': 'ropinirole',
                                      'reason': 'Nitrogen atom is not a '
                                                'tertiary amine'},
                                  {   'smiles': 'CN(C)c1ncnc2[nH]cnc12',
                                      'name': 'N(6),N(6)-dimethyladenine',
                                      'reason': 'Nitrogen atom is not a '
                                                'tertiary amine'},
                                  {   'smiles': 'C/C(=C\\CC\\C(\\C)=C\\C[C@]12C(C=C(C([C@H]1O2)OC(C)=O)C)=O)/CCCC(C)(C)O',
                                      'name': 'yanuthone M',
                                      'reason': 'No nitrogen atoms found'},
                                  {   'smiles': 'CN(C)CCc1c[nH]c2ccc(O)cc12',
                                      'name': 'bufotenin',
                                      'reason': 'Nitrogen atom is not a '
                                                'tertiary amine'},
                                  {   'smiles': 'CN(CCCCC(O)=O)c1ccc(cc1)\\C=C\\c1ccc(cc1)[N+]([O-])=O',
                                      'name': "N-(trans-4'-nitro-4-stilbenyl)-N-methyl-5-aminopentanoic "
                                              'acid',
                                      'reason': 'Nitrogen atom is not a '
                                                'tertiary amine'}],
    'attempt': 3,
    'reasoning': "Okay, let's analyze the previous code and the outcomes to "
                 'figure out how to improve the `is_tertiary_amine` function.\n'
                 '\n'
                 '**Issues with the previous code:**\n'
                 '\n'
                 '1.  **Incorrect Logic:** The previous code had a fundamental '
                 'flaw. It returned `True` immediately upon finding *any* '
                 'nitrogen atom bonded to three carbons. It should have '
                 'checked *all* nitrogen atoms, and return `True` *only if at '
                 'least one nitrogen was a tertiary amine, and none were not*. '
                 'If *any* nitrogen was not a tertiary amine, it should have '
                 'returned `False`.\n'
                 '2.  **False Positives:** The false positives seem to be '
                 'stemming from cases where the nitrogen is part of a ring '
                 'system, or attached to carbonyl groups or other heteroatoms '
                 'besides carbon, making the molecule *not* a tertiary amine, '
                 "according to the prompt's definition. For example, many of "
                 'the false positives have an N atom bonded to a carbon atom '
                 'that is part of a carbonyl group (C=O) or sulfonyl group, '
                 'which is not a pure "hydrocarbyl" (only carbon and hydrogen) '
                 'group as defined by the prompt for a tertiary amine.\n'
                 '3.  **False Negatives**: The false negatives are mostly '
                 'stemming from having a nitrogen in azoxy, nitro groups (N=N+ '
                 'or N+-[O-]) as well as amide or imide (-C(=O)N- and '
                 '-C(=O)NC(=O)-).\n'
                 '\n'
                 '**Proposed Improvements:**\n'
                 '\n'
                 '1.  **Iterate and Check All Nitrogens:** The code should '
                 'iterate through *all* nitrogen atoms. If *any* nitrogen is '
                 '*not* a tertiary amine (three bonds to carbon), the function '
                 'should return `False`.\n'
                 "2.  **Check the nature of the nitrogen's neighbors:** "
                 'explicitly check that *all* neighbors are carbon atoms.\n'
                 '3.  **Return True only when condition is met:** if iteration '
                 'is completed and no nitrogen that is not a tertiary amine '
                 'has been found, then the function should return `True`.\n'
                 '4.  **Reason Strings:** Should return a more informative '
                 'reason string.\n'
                 '5.  **Handle no N atoms**: explicitly state that no N atoms '
                 'were found.\n'
                 '\n'
                 "Here's the improved code:",
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 55,
    'num_false_positives': 6515,
    'num_true_negatives': 135709,
    'num_false_negatives': 21,
    'num_negatives': None,
    'precision': 0.00837138508371385,
    'recall': 0.7236842105263158,
    'f1': 0.016551309058080048,
    'accuracy': 0.9540688685874912,
    'negative_predictive_value': 0.9998452810727179}