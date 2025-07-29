"""
Classifies: CHEBI:51689 enone
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_enone(smiles: str):
    """
    Determines if a molecule is an enone based on its SMILES string.
    An enone is an alpha,beta-unsaturated ketone with the general formula R1R2C=CR3-C(=O)R4 (R4 != H)

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is an enone, False otherwise
        str: Reason for classification
    """
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Define SMARTS pattern for the enone motif
    # The pattern now specifies that the carbonyl carbon is not bonded to any H (except via double bond)
    enone_pattern = Chem.MolFromSmarts("[C;!H0]=[C;!H0]-[C](=[O])[C;!H0]")
    
    # Find the enone substructure
    matches = mol.GetSubstructMatches(enone_pattern)
    
    if matches:
        return True, "Contains an alpha,beta-unsaturated ketone (C=C-C=O) motif with R4 != H"
    
    return False, "No alpha,beta-unsaturated ketone (C=C-C=O) motif found."


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:51689',
                          'name': 'enone',
                          'definition': 'An alpha,beta-unsaturated ketone of '
                                        'general formula '
                                        'R(1)R(2)C=CR(3)-C(=O)R(4) (R(4) =/= '
                                        'H) in which the C=O function is '
                                        'conjugated to a C=C double bond at '
                                        'the alpha,beta position.',
                          'parents': ['CHEBI:51721', 'CHEBI:78840'],
                          'xrefs': ['Wikipedia:Enone'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 21,
                           'log_lines_of_code': 3.044522437723423,
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
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 1,
                                                 1],
                           'max_indent': 2,
                           'imports': [   'from rdkit import Chem',
                                          'from rdkit.Chem import AllChem'],
                           'imports_count': 2,
                           'methods_called': [   'MolFromSmiles',
                                                 'MolFromSmarts',
                                                 'GetSubstructMatches'],
                           'methods_called_count': 3,
                           'smarts_strings': [   '[C;!H0]=[C;!H0]-[C](=[O])[C;!H0]'],
                           'smarts_strings_count': 1,
                           'defs': ['is_enone(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'True, "Contains an '
                                          'alpha,beta-unsaturated ketone '
                                          '(C=C-C=O) motif with R4 != H"',
                                          'False, "No alpha,beta-unsaturated '
                                          'ketone (C=C-C=O) motif found."'],
                           'returns_count': 3,
                           'complexity': 2.4089044875446843},
    'message': '\n'
               'Attempt failed: F1 score of 0.09539518900343642 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: '
               'OCC1=CC(=O)C2=C(C)C[C@@H]([C@]3([C@H](C)C(=O)O[C@@]3([C@@]12[H])[H])[H])OC(=O)CC=4C=CC(O)=CC4 '
               'NAME: 11beta,13-dihydrolactucopicrin REASON: CORRECT Contains '
               'an alpha,beta-unsaturated ketone (C=C-C=O) motif with R4 != H\n'
               ' * SMILES: CC1=CC=C(C=C1)\\C(\\[H])=C(/[H])\\C(C2=CC=CC=C2O)=O '
               "NAME: 2'-hydroxy-4-methylchalcone REASON: CORRECT Contains an "
               'alpha,beta-unsaturated ketone (C=C-C=O) motif with R4 != H\n'
               ' * SMILES: '
               'CC(C)=CCOc1cc(O)c(C(C)=O)c(O)c1CC1=C(O)C(C)(CC=C(C)C)C(O)=C(C(C)=O)C1=O '
               'NAME: drummondin E REASON: CORRECT Contains an '
               'alpha,beta-unsaturated ketone (C=C-C=O) motif with R4 != H\n'
               ' * SMILES: '
               '[H][C@@]12CCC3=CC(=O)CC[C@]3(C)[C@@]1([H])CC[C@@]1(C)[C@@]2([H])C[C@H]2OC(C)(O[C@@]12C(C)=O)c1ccccc1 '
               'NAME: 16alpha,17alpha-dihydroxyprogesterone acetophenide '
               'REASON: CORRECT Contains an alpha,beta-unsaturated ketone '
               '(C=C-C=O) motif with R4 != H\n'
               ' * SMILES: '
               'CO[C@H]1CC(=O)C([C@H]2OC(=O)C(=C)[C@@H]2CCC(C)=O)=C1C NAME: '
               '3-O-methyl-isosecotanapartholide REASON: CORRECT Contains an '
               'alpha,beta-unsaturated ketone (C=C-C=O) motif with R4 != H\n'
               ' * SMILES: O=C1C(=C(O)C=C1)C(=O)CCCCCCCCCC NAME: Chrysotrione '
               'B REASON: CORRECT Contains an alpha,beta-unsaturated ketone '
               '(C=C-C=O) motif with R4 != H\n'
               ' * SMILES: '
               '[H][C@@]1(CC[C@@]2([H])[C@]3([H])CCC4=CC(=O)CC[C@]4(C)[C@@]3([H])CC[C@]12C)[C@@H](C)O '
               'NAME: (20R)-20-hydroxypregn-4-en-3-one REASON: CORRECT '
               'Contains an alpha,beta-unsaturated ketone (C=C-C=O) motif with '
               'R4 != H\n'
               ' * SMILES: '
               'C1[C@@]2([C@@]([C@@]3(C(C1)=CC(CC3)=O)C)([C@H](C[C@@]4([C@@](CC[C@@]24[H])(O)[C@@H](CO)O)C)O)[H])[H] '
               'NAME: 20beta-dihydrocortisol REASON: CORRECT Contains an '
               'alpha,beta-unsaturated ketone (C=C-C=O) motif with R4 != H\n'
               ' * SMILES: '
               '[H][C@@]12CC[C@](O)(C(=O)CO)[C@@]1(C)C[C@H](O)[C@@]1(F)[C@@]2([H])CCC2=CC(=O)CC[C@]12C '
               'NAME: fludrocortisone REASON: CORRECT Contains an '
               'alpha,beta-unsaturated ketone (C=C-C=O) motif with R4 != H\n'
               ' * SMILES: '
               'O1C(CCC=C(C)C)(C=CC2=C1C=CC(=C2O)C(=O)/C=C/C3=CC=CC=C3)C NAME: '
               'Spinochalcone B REASON: CORRECT Contains an '
               'alpha,beta-unsaturated ketone (C=C-C=O) motif with R4 != H\n'
               ' * SMILES: O=C1N[C@H](CC(C)C)C(=C1C(=O)C)O NAME: Mutanocyclin '
               'REASON: CORRECT Contains an alpha,beta-unsaturated ketone '
               '(C=C-C=O) motif with R4 != H\n'
               ' * SMILES: '
               '[H][C@@]1(CC[C@@]2([H])[C@]3([H])CCC4=CC(=O)C=C[C@]4(C)[C@@]3([H])CC[C@]12COC(C)=O)[C@H](C)[C@H]1CC(C)=C(C)C(=O)O1 '
               'NAME: minabeolide 2 REASON: CORRECT Contains an '
               'alpha,beta-unsaturated ketone (C=C-C=O) motif with R4 != H\n'
               ' * SMILES: Oc1ccc(cc1)C(=O)\\C=C\\c1ccccc1 NAME: '
               "4'-hydroxychalcone REASON: CORRECT Contains an "
               'alpha,beta-unsaturated ketone (C=C-C=O) motif with R4 != H\n'
               ' * SMILES: '
               'O=C1C=C2[C@@]3([C@]([C@]4([C@@](CC3)(CC[C@](C4)(C(=O)O)C)C)[H])(CC[C@]2(C=5C1=C(C(OC)=C(O)C5)C)C)C)C '
               'NAME: triptohypol B REASON: CORRECT Contains an '
               'alpha,beta-unsaturated ketone (C=C-C=O) motif with R4 != H\n'
               ' * SMILES: '
               'OC1=C(CC(CC=C(C)C)C(C)=C)C(O)=CC(OC)=C1C(=O)/C=C/C2=C(OC)C=C(O)C=C2 '
               'NAME: Kushenol D REASON: CORRECT Contains an '
               'alpha,beta-unsaturated ketone (C=C-C=O) motif with R4 != H\n'
               ' * SMILES: '
               'COc1cc(O)c(\\C=C/C(C)(C)O)c(O)c1C(=O)\\C=C\\c1ccc(O)cc1 NAME: '
               'candidachalcone REASON: CORRECT Contains an '
               'alpha,beta-unsaturated ketone (C=C-C=O) motif with R4 != H\n'
               ' * SMILES: CC(=O)C=Cc1ccccc1 NAME: benzylideneacetone REASON: '
               'CORRECT Contains an alpha,beta-unsaturated ketone (C=C-C=O) '
               'motif with R4 != H\n'
               ' * SMILES: '
               '[H][C@@]1(CC[C@@]2([H])[C@]3([H])CCC4=CC(=O)CC[C@]4(C)[C@@]3([H])[C@@H](C[C@]12C)OC(C)=O)[C@H](C)[C@H]1CC[C@H](C)C(=O)O1 '
               'NAME: minabeolide 8 REASON: CORRECT Contains an '
               'alpha,beta-unsaturated ketone (C=C-C=O) motif with R4 != H\n'
               ' * SMILES: '
               'CC(C)[C@@]12CC[C@@](C)(OO1)C1=C([C@H](C)CC1=O)[C@H]2O NAME: '
               'nardoperoxide REASON: CORRECT Contains an '
               'alpha,beta-unsaturated ketone (C=C-C=O) motif with R4 != H\n'
               ' * SMILES: C(/C=C/C(CCCCC)=O)O NAME: (E)-4-oxonon-2-en-1-ol '
               'REASON: CORRECT Contains an alpha,beta-unsaturated ketone '
               '(C=C-C=O) motif with R4 != H\n'
               ' * SMILES: C=1(C=CC=CC1C(=O)/C=C/C2=CC(=C(C=C2)O)O)O NAME: '
               "2',3,4-trihydroxy-trans-chalcone REASON: CORRECT Contains an "
               'alpha,beta-unsaturated ketone (C=C-C=O) motif with R4 != H\n'
               ' * SMILES: '
               '[H][C@@]12CC[C@@H]3C[C@]1(CC3=C)[C@@H](C(O)=O)[C@@]1([H])C2=CC(=O)C[C@@]1(C)C(O)=O '
               'NAME: gibberellin A51-catabolite REASON: CORRECT Contains an '
               'alpha,beta-unsaturated ketone (C=C-C=O) motif with R4 != H\n'
               ' * SMILES: '
               '[H][C@@]12C[C@@]3([H])C(C)=CC(=O)[C@@H](O)[C@]3(C)[C@@]3([H])[C@@H](O)[C@H](O)[C@]4(OC[C@@]13[C@@]4([H])[C@@H](OC(=O)\\C=C(/C)C(C)C)C(=O)O2)C(=O)OC '
               'NAME: bruceanol D REASON: CORRECT Contains an '
               'alpha,beta-unsaturated ketone (C=C-C=O) motif with R4 != H\n'
               ' * SMILES: '
               '[H][C@@]12CC3=C([C@H](C)[C@]1([H])OC(=O)C(C)=C2)C(=O)C[C@]1(C)[C@@]3([H])C[C@]2(O)C=C3C=CC(=O)OC(C)(C)[C@]3([H])CC[C@@]12[H] '
               'NAME: kadlongilactone B REASON: CORRECT Contains an '
               'alpha,beta-unsaturated ketone (C=C-C=O) motif with R4 != H\n'
               ' * SMILES: COc1cc(\\C=C\\C(=O)c2c(O)cc(O)cc2O)ccc1O NAME: '
               'homoeriodictyol chalcone REASON: CORRECT Contains an '
               'alpha,beta-unsaturated ketone (C=C-C=O) motif with R4 != H\n'
               'False positives: SMILES: '
               'C[C@H]1C[C@@]2(OC(=O)c3ccccc3)[C@H]([C@H]1OC(C)=O)[C@@H](O)\\C(C)=C/C[C@H]1[C@@H](\\C=C(C)\\C2=O)C1(C)C '
               'NAME: '
               '(-)-(6Z,12E,2S,3S,4R,5R,9S,11S,15R)-3-acetoxy-15-benzoyloxylathyra-6,12-dien-5-ol-14-one '
               'REASON: WRONGLY CLASSIFIED Contains an alpha,beta-unsaturated '
               'ketone (C=C-C=O) motif with R4 != H\n'
               ' * SMILES: '
               'O=C1C2=C([C@@]3(CC[C@@H]([C@]3(C1)C)[C@@H](CCC(=O)O)C)C)[C@H]4O[C@@](C2)([C@H](C(=C)C)C4)CCC(=O)OC '
               'NAME: Cochlate B REASON: WRONGLY CLASSIFIED Contains an '
               'alpha,beta-unsaturated ketone (C=C-C=O) motif with R4 != H\n'
               ' * SMILES: '
               'O=C1N(C(=O)[C@H]2N(C(=O)[C@@H](N(C(=O)[C@@H](NC(=O)[C@@H](N(C(=O)[C@@H](C[C@@H](CCCC)C)C)C)C=C(C)C)[C@H](OC(=O)C)C)C)C(C)C)CCC2)[C@@H](C)C=C1 '
               'NAME: Microcolin E REASON: WRONGLY CLASSIFIED Contains an '
               'alpha,beta-unsaturated ketone (C=C-C=O) motif with R4 != H\n'
               ' * SMILES: O(CCCCCCC)C(=O)/C=C/C1=CC=CC=C1 NAME: Heptyl '
               'cinnamate REASON: WRONGLY CLASSIFIED Contains an '
               'alpha,beta-unsaturated ketone (C=C-C=O) motif with R4 != H\n'
               ' * SMILES: '
               'CCC(=O)O[C@@H]1C[C@H]2[C@@H]3CCC4=CC(=O)CC[C@]4(C)[C@H]3CC[C@]2(C)[C@H]1OC(=O)CC '
               'NAME: 16alpha,17beta-Dihydroxyandrost-4-en-3-one dipropionate '
               'REASON: WRONGLY CLASSIFIED Contains an alpha,beta-unsaturated '
               'ketone (C=C-C=O) motif with R4 != H\n'
               ' * SMILES: '
               'O([C@@H]1[C@@H](O)[C@H](O)[C@H](O[C@H]1OC=2C=C3C(O[C@@H]4O[C@@H]([C@@H](O)[C@H](O)[C@H]4O)CO)=CC(O)=CC3=[O+]C2C5=CC(OC)=C(O)C=C5)COC(=O)C=CC6=CC(O)=C(O)C=C6)[C@@H]7O[C@@H]([C@@H](O)[C@H](O)[C@H]7O)COC(=O)C=CC8=CC(OC)=C(O)C=C8 '
               'NAME: Peonidin-3-caffeoyl-feruloyl sophoroside-5-glucoside '
               'REASON: WRONGLY CLASSIFIED Contains an alpha,beta-unsaturated '
               'ketone (C=C-C=O) motif with R4 != H\n'
               ' * SMILES: '
               'O=C1C(=C(O)C(C)=C([C@]1(O)C)O)C(=O)[C@H]2[C@H]3\\C(\\C(=O)[C@]([C@@H]2/C=C/C)(C)C([C@]3(O)C)=O)=C(\\O)/C=C/C=C/C '
               'NAME: Oxosorbiquinol REASON: WRONGLY CLASSIFIED Contains an '
               'alpha,beta-unsaturated ketone (C=C-C=O) motif with R4 != H\n'
               ' * SMILES: '
               'C1(=CC=C(C(=C1)O)O)/C=C/C(O[C@H]2[C@@H]([C@@H](C=C(C2)C(=O)O)O)O)=O '
               'NAME: 5-[(E)-caffeoyl]shikimic acid REASON: WRONGLY CLASSIFIED '
               'Contains an alpha,beta-unsaturated ketone (C=C-C=O) motif with '
               'R4 != H\n'
               ' * SMILES: '
               'O(C1C(OC(=O)/C=C/C2=CC(OC)=C(O)C=C2)C(OC(OCCC3=CC(O)=C(OC)C=C3)C1O)CO)C4OC(C(O)C(O)C4OC5OCC(O)C(O)C5O)C '
               'NAME: Leonoside B REASON: WRONGLY CLASSIFIED Contains an '
               'alpha,beta-unsaturated ketone (C=C-C=O) motif with R4 != H\n'
               ' * SMILES: '
               'O1C23C(O)(C4(CC1(O)C(C2=O)(C(=CC4=O)C(COC5OC(C(O)C(O)C5O)CO)C)C)C)CCC(C3O)C '
               'NAME: Cinncassiol C1 19-glucoside REASON: WRONGLY CLASSIFIED '
               'Contains an alpha,beta-unsaturated ketone (C=C-C=O) motif with '
               'R4 != H\n'
               ' * SMILES: '
               'O=C1C=C2[C@](O)([C@H](O[C@@H](C2)C=CC=CC)O)[C@@H]([C@@]1(O)C)O '
               'NAME: Nigbeauvin C REASON: WRONGLY CLASSIFIED Contains an '
               'alpha,beta-unsaturated ketone (C=C-C=O) motif with R4 != H\n'
               ' * SMILES: '
               'O=C1NC[C@@H](C=CC=CC=C(C)[C@@H]2[C@@H](C=C(C=CC(C1)=O)C)[C@H]3[C@H](C(=O)[C@@H](O)[C@H]([C@@H]3O)O)C=C2)C '
               'NAME: Niizalactam C REASON: WRONGLY CLASSIFIED Contains an '
               'alpha,beta-unsaturated ketone (C=C-C=O) motif with R4 != H\n'
               ' * SMILES: '
               'O=C(C=1NC=CC1)\\C=C(/C=C/C(O)C(O)(CC/C=C(/O)\\C)C)\\C NAME: '
               '(2Z,4E,10E)-6,7,11-trihydroxy-3,7-dimethyl-1-(1H-pyrrol-2-yl)dodeca-2,4,10-trien-1-one '
               'REASON: WRONGLY CLASSIFIED Contains an alpha,beta-unsaturated '
               'ketone (C=C-C=O) motif with R4 != H\n'
               ' * SMILES: [H]C(C(=O)C(Cl)C([O-])=O)=C(Cl)C([O-])=O NAME: '
               '2,5-dichloro-4-oxohex-2-enedioate(2-) REASON: WRONGLY '
               'CLASSIFIED Contains an alpha,beta-unsaturated ketone (C=C-C=O) '
               'motif with R4 != H\n'
               ' * SMILES: [H][C@@]1(OC(=O)C(O)=C1O)[C@@H](O)COP(O)(O)=O NAME: '
               'L-ascorbic acid 6-phosphate REASON: WRONGLY CLASSIFIED '
               'Contains an alpha,beta-unsaturated ketone (C=C-C=O) motif with '
               'R4 != H\n'
               ' * SMILES: '
               'O=C(O[C@H]1[C@]2(O[C@@]([C@@H]1O)(O[C@@H]([C@@]2(O)C(=O)O)C(=O)O)CCC(=C)[C@@H](OC(=O)C)[C@@H](CC3=CC=CC=C3)C)C(=O)O)/C=C/C(CCCC)C '
               'NAME: Squalestatin X1 REASON: WRONGLY CLASSIFIED Contains an '
               'alpha,beta-unsaturated ketone (C=C-C=O) motif with R4 != H\n'
               ' * SMILES: '
               'O=C1/C(=C(\\O)/C=C/C=C/C)/[C@H]2[C@@](O)(C)C([C@@]1([C@H](C(=O)/C=C/C=C/C)[C@H]2[C@@]3(OC(=O)C(=C3O)C)C)C)=O '
               'NAME: Bislongiquinolide REASON: WRONGLY CLASSIFIED Contains an '
               'alpha,beta-unsaturated ketone (C=C-C=O) motif with R4 != H\n'
               ' * SMILES: '
               'F[C@@]12C(=O)CC3([C@@](O)(C)CCC3C1CCC=4C2(CCC(C4)=O)C)C NAME: '
               '(9R,17S)-9-fluoro-17-hydroxy-10,13,17-trimethyl-2,6,7,8,12,14,15,16-octahydro-1H-cyclopenta[a]phenanthrene-3,11-dione '
               'REASON: WRONGLY CLASSIFIED Contains an alpha,beta-unsaturated '
               'ketone (C=C-C=O) motif with R4 != H\n'
               ' * SMILES: CC12CCC(=O)C=C1CCC3C2CCC4(C3CCC4(C)O)C NAME: '
               '17-hydroxy-10,13,17-trimethyl-2,6,7,8,9,11,12,14,15,16-decahydro-1H-cyclopenta[a]phenanthren-3-one '
               'REASON: WRONGLY CLASSIFIED Contains an alpha,beta-unsaturated '
               'ketone (C=C-C=O) motif with R4 != H\n'
               ' * SMILES: FC1=CC(Cl)=C(OCC#C)C=C1N1C(=O)C2=C(CCCC2)C1=O NAME: '
               'S-23142 REASON: WRONGLY CLASSIFIED Contains an '
               'alpha,beta-unsaturated ketone (C=C-C=O) motif with R4 != H\n'
               ' * SMILES: '
               'O1C2(O)C(C(OC(=O)C)CC1CC(O)CC(OC(CC3OC(O)(C(C=CC4OC(C2)C/C(/C4)=C/C(OC)=O)(C)C)C(OC(=O)/C=C/C=C/CCC)/C(/C3)=C/C(OC)=O)C(O)C)=O)(C)C '
               'NAME: Bryo 1 REASON: WRONGLY CLASSIFIED Contains an '
               'alpha,beta-unsaturated ketone (C=C-C=O) motif with R4 != H\n'
               ' * SMILES: O=C1C=C2C=CC(=O)[C@@H]([C@@]2(C)C[C@@]1(O)C(=C)CO)C '
               'NAME: Dihydrobipolaroxin D REASON: WRONGLY CLASSIFIED Contains '
               'an alpha,beta-unsaturated ketone (C=C-C=O) motif with R4 != H\n'
               ' * SMILES: O=C1O[C@@H]([C@@H](O)[C@H](O)[C@H](O)C)C=C1C NAME: '
               'Xylogiblactone B REASON: WRONGLY CLASSIFIED Contains an '
               'alpha,beta-unsaturated ketone (C=C-C=O) motif with R4 != H\n'
               ' * SMILES: '
               'O[C@@H]1C[C@](O)(C[C@@H](OC(=O)\\C=C\\c2ccc(O)cc2)[C@@H]1O)C([O-])=O '
               'NAME: trans-5-O-(4-coumaroyl)-D-quinate REASON: WRONGLY '
               'CLASSIFIED Contains an alpha,beta-unsaturated ketone (C=C-C=O) '
               'motif with R4 != H\n'
               ' * SMILES: '
               'O=C1O[C@@H]2C[C@]3(O)[C@H](OC)CC[C@@H]([C@]3(CC2=C1CO)C)C '
               'NAME: '
               '10alpha,13-dihydroxy-1beta-methoxyeremophil-7(11)-en-12,8beta-olide '
               'REASON: WRONGLY CLASSIFIED Contains an alpha,beta-unsaturated '
               'ketone (C=C-C=O) motif with R4 != H\n'
               'False negatives: SMILES: '
               'C[C@@H]1C[C@@H]2[C@H]3CC[C@]4(C)[C@@H](O)CC[C@H]4[C@@H]3CCC2=CC1=O '
               'NAME: 17beta-hydroxy-2alpha-methylestr-4-en-3-one REASON: '
               'MISSED No alpha,beta-unsaturated ketone (C=C-C=O) motif '
               'found.\n'
               ' * SMILES: '
               '[H][C@@]12CC[C@](O)([C@@H](O)CO)[C@@]1(C)CC(=O)[C@@]1([H])[C@@]2([H])CCC2=CC(=O)C=C[C@]12C '
               'NAME: 20beta-dihydroprednisone REASON: MISSED No '
               'alpha,beta-unsaturated ketone (C=C-C=O) motif found.\n'
               ' * SMILES: '
               'CC1C[C@H]2[C@@H]3CC[C@](O)(C(=O)CO)[C@@]3(C)C[C@H](O)[C@@H]2[C@@]2(C)C=CC(=O)C=C12 '
               'NAME: 6-methylprednisolone REASON: MISSED No '
               'alpha,beta-unsaturated ketone (C=C-C=O) motif found.\n'
               ' * SMILES: CCCCCCCCCCCCCCC[C@@H](O)CC1(CCC2(O1)C=CC(=O)C=C2)OC '
               'NAME: amomol A REASON: MISSED No alpha,beta-unsaturated ketone '
               '(C=C-C=O) motif found.\n'
               ' * SMILES: '
               'C1C([C@H](C([C@]2([H])[C@]1(C)[C@@]3(C(C=C([C@H]([C@]3(CC2)[H])C)C=C)=O)[H])(C)C)O)=O '
               'NAME: (+)-phytocassane D REASON: MISSED No '
               'alpha,beta-unsaturated ketone (C=C-C=O) motif found.\n'
               ' * SMILES: '
               'O(C1=C([C@@]2([C@H](CCC(=C2)C)C(C)C)[H])C(O)=C(C(O)=C1)C(=O)CCC3=CC=CC=C3)C '
               'NAME: Methyllinderatin REASON: MISSED No '
               'alpha,beta-unsaturated ketone (C=C-C=O) motif found.\n'
               ' * SMILES: '
               '[H][C@@]12C[C@@H](O)[C@](O)(C(=O)CO)[C@@]1(C)C[C@H](O)[C@@]1(F)[C@@]2([H])CCC2=CC(=O)C=C[C@]12C '
               'NAME: triamcinolone REASON: MISSED No alpha,beta-unsaturated '
               'ketone (C=C-C=O) motif found.\n'
               ' * SMILES: O=C(C(CCCCCC)CC)/C=C/C NAME: '
               '5-Ethyl-2E-undecen-4-one REASON: MISSED No '
               'alpha,beta-unsaturated ketone (C=C-C=O) motif found.\n'
               ' * SMILES: '
               'C[C@H]1C[C@H]2[C@@H]3CC[C@](O)(C(C)=O)[C@@]3(C)C[C@H](O)[C@]2(F)[C@@]2(C)C=CC(=O)C=C12 '
               'NAME: fluorometholone REASON: MISSED No alpha,beta-unsaturated '
               'ketone (C=C-C=O) motif found.\n'
               ' * SMILES: '
               'OC1=C(C\\C=C(\\CCC=C(C)C)/CO)C(O)=CC(O)=C1C(=O)CCC2=CC=C(O)C=C2 '
               'NAME: '
               '3-(4-hydroxyphenyl)-1-{2,4,6-trihydroxy-3-[(2Z)-4-hydroxy-3-(4-methylpent-3-en-1-yl)but-2-en-1-yl]phenyl}propan-1-one '
               'REASON: MISSED No alpha,beta-unsaturated ketone (C=C-C=O) '
               'motif found.\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'CCN1N=C(N=N1)C2=CC=CC=C2NC(=O)C3=CC=C(C=C3)N4C=NN=N4',
                                     'name': 'N-[2-(2-ethyl-5-tetrazolyl)phenyl]-4-(1-tetrazolyl)benzamide',
                                     'reason': 'No alpha,beta-unsaturated '
                                               'ketone (C=C-C=O) motif found.'},
                                 {   'smiles': 'CCS(=O)(=O)N1CC2(C1)[C@@H]([C@@H](N2C(=O)C3CCCC3)CO)C4=CC=C(C=C4)C=CC',
                                     'name': 'LSM-38092',
                                     'reason': 'No alpha,beta-unsaturated '
                                               'ketone (C=C-C=O) motif found.'},
                                 {   'smiles': 'O=C/1N/C(/C(=O)N\\C1=C\\C2=CC=CC=C2)=C\\C=3N=CNC3C(C=C)(C)C',
                                     'name': 'DeltaPLH',
                                     'reason': 'No alpha,beta-unsaturated '
                                               'ketone (C=C-C=O) motif found.'},
                                 {   'smiles': 'C1CCN(CC1)C(=O)C[C@H]2C[C@@H]3[C@H]([C@@H](O2)CO)OC4=C3C=C(C=C4)NC(=O)CC5CC5',
                                     'name': 'N-[(1S,3R,4aS,9aR)-1-(hydroxymethyl)-3-[2-oxo-2-(1-piperidinyl)ethyl]-3,4,4a,9a-tetrahydro-1H-pyrano[3,4-b]benzofuran-6-yl]-2-cyclopropylacetamide',
                                     'reason': 'No alpha,beta-unsaturated '
                                               'ketone (C=C-C=O) motif found.'},
                                 {   'smiles': 'C[C@H]1C[C@@]2(OC(=O)c3ccccc3)[C@H]([C@H]1OC(C)=O)[C@@H](O)\\C(C)=C/C[C@H]1[C@@H](\\C=C(C)\\C2=O)C1(C)C',
                                     'name': '(-)-(6Z,12E,2S,3S,4R,5R,9S,11S,15R)-3-acetoxy-15-benzoyloxylathyra-6,12-dien-5-ol-14-one',
                                     'reason': 'No alpha,beta-unsaturated '
                                               'ketone (C=C-C=O) motif found.'},
                                 {   'smiles': 'O=C1C(O)=CC=2O[C@]3([C@H](O)C[C@@H]4[C@](OC=5C=C(O)C(C=C(C5C4)C)=O)(CC=CC(C[C@H]3CC2C(=C1)C)(C)C)C)C',
                                     'name': 'Eupenifeldin',
                                     'reason': 'No alpha,beta-unsaturated '
                                               'ketone (C=C-C=O) motif found.'},
                                 {   'smiles': 'O1[C@@H](O[C@@H]2[C@@H](OC[C@H]3O[C@@H](O[C@H]4[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]4CO)O[C@H]5[C@H](O)[C@@H](NC(=O)C)C(O[C@@H]5CO[C@@H]6O[C@H]([C@@H](O)[C@@H](O)[C@@H]6O)C)O)[C@@H](O)[C@@H](O[C@H]7O[C@@H]([C@@H](O)[C@H](O)[C@@H]7O[C@@H]8O[C@@H]([C@@H](O[C@@H]9O[C@@H]([C@H](O)[C@H](O)[C@H]9NC(=O)C)CO)[C@H](O)[C@H]8NC(=O)C)CO)CO)[C@@H]3O)O[C@@H]([C@@H](O)[C@@H]2O)CO)[C@H](NC(=O)C)[C@@H](O[C@@H]%10O[C@H]([C@@H](O)[C@@H](O)[C@@H]%10O)C)[C@H](O[C@@H]%11O[C@@H]([C@H](O)[C@H](O)[C@H]%11NC(=O)C)CO)[C@H]1CO',
                                     'name': 'N-[(3R,4R,5S,6R)-5-[(2S,3R,4R,5S,6R)-3-Acetamido-5-[(2S,3S,4S,5R,6R)-4-[(2R,3S,4S,5S,6R)-3-[(2S,3R,4R,5S,6R)-3-acetamido-5-[(2S,3R,4R,5R,6R)-3-acetamido-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-6-[[(2S,3S,4S,5S,6R)-3-[(2S,3R,4R,5S,6R)-3-acetamido-5-[(2S,3R,4R,5R,6R)-3-acetamido-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-6-(hydroxymethyl)-4-[(2R,3S,4R,5S,6S)-3,4,5-trihydroxy-6-methyloxan-2-yl]oxyoxan-2-yl]oxy-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxymethyl]-3,5-dihydroxyoxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-2,4-dihydroxy-6-[[(2R,3S,4R,5S,6S)-3,4,5-trihydroxy-6-methyloxan-2-yl]oxymethyl]oxan-3-yl]acetamide',
                                     'reason': 'No alpha,beta-unsaturated '
                                               'ketone (C=C-C=O) motif found.'},
                                 {   'smiles': 'CN1C[C@@H]2C[C@H](Cn3c2cccc3=O)[C@H]1CC=C',
                                     'name': 'Tinctorine',
                                     'reason': 'No alpha,beta-unsaturated '
                                               'ketone (C=C-C=O) motif found.'},
                                 {   'smiles': 'CCC1=C2COC(CC2=C3C(=C(OC3=N1)C(=O)C4=CC=CC=C4)N)(C)C',
                                     'name': 'LSM-4563',
                                     'reason': 'No alpha,beta-unsaturated '
                                               'ketone (C=C-C=O) motif found.'},
                                 {   'smiles': 'CN1CCN(CC1)C(=O)C[C@@H]2CC[C@H]3[C@H](O2)COC[C@@H](CN3C(=O)NC4=CC5=C(C=C4)OCO5)O',
                                     'name': '(3R,6aS,8S,10aS)-N-(1,3-benzodioxol-5-yl)-3-hydroxy-8-[2-(4-methyl-1-piperazinyl)-2-oxoethyl]-3,4,6,6a,8,9,10,10a-octahydro-2H-pyrano[2,3-c][1,5]oxazocine-1-carboxamide',
                                     'reason': 'No alpha,beta-unsaturated '
                                               'ketone (C=C-C=O) motif '
                                               'found.'}],
    'sample_false_negatives': [   {   'smiles': 'C[C@@H]1C[C@@H]2[C@H]3CC[C@]4(C)[C@@H](O)CC[C@H]4[C@@H]3CCC2=CC1=O',
                                      'name': '17beta-hydroxy-2alpha-methylestr-4-en-3-one',
                                      'reason': 'No alpha,beta-unsaturated '
                                                'ketone (C=C-C=O) motif '
                                                'found.'},
                                  {   'smiles': 'OCC1=CC(=O)C2=C(C)C[C@@H]([C@]3([C@H](C)C(=O)O[C@@]3([C@@]12[H])[H])[H])OC(=O)CC=4C=CC(O)=CC4',
                                      'name': '11beta,13-dihydrolactucopicrin',
                                      'reason': 'No alpha,beta-unsaturated '
                                                'ketone (C=C-C=O) motif '
                                                'found.'},
                                  {   'smiles': 'C1C([C@H](C([C@]2([H])[C@]1(C)[C@@]3(C(C=C([C@H]([C@]3(CC2)[H])C)C=C)=O)[H])(C)C)O)=O',
                                      'name': '(+)-phytocassane D',
                                      'reason': 'No alpha,beta-unsaturated '
                                                'ketone (C=C-C=O) motif '
                                                'found.'},
                                  {   'smiles': 'CC1=CC=C(C=C1)\\C(\\[H])=C(/[H])\\C(C2=CC=CC=C2O)=O',
                                      'name': "2'-hydroxy-4-methylchalcone",
                                      'reason': 'No alpha,beta-unsaturated '
                                                'ketone (C=C-C=O) motif '
                                                'found.'},
                                  {   'smiles': 'CC(C)=CCOc1cc(O)c(C(C)=O)c(O)c1CC1=C(O)C(C)(CC=C(C)C)C(O)=C(C(C)=O)C1=O',
                                      'name': 'drummondin E',
                                      'reason': 'No alpha,beta-unsaturated '
                                                'ketone (C=C-C=O) motif '
                                                'found.'},
                                  {   'smiles': '[H][C@@]12CCC3=CC(=O)CC[C@]3(C)[C@@]1([H])CC[C@@]1(C)[C@@]2([H])C[C@H]2OC(C)(O[C@@]12C(C)=O)c1ccccc1',
                                      'name': '16alpha,17alpha-dihydroxyprogesterone '
                                              'acetophenide',
                                      'reason': 'No alpha,beta-unsaturated '
                                                'ketone (C=C-C=O) motif '
                                                'found.'},
                                  {   'smiles': 'O(C1=C([C@@]2([C@H](CCC(=C2)C)C(C)C)[H])C(O)=C(C(O)=C1)C(=O)CCC3=CC=CC=C3)C',
                                      'name': 'Methyllinderatin',
                                      'reason': 'No alpha,beta-unsaturated '
                                                'ketone (C=C-C=O) motif '
                                                'found.'},
                                  {   'smiles': 'CO[C@H]1CC(=O)C([C@H]2OC(=O)C(=C)[C@@H]2CCC(C)=O)=C1C',
                                      'name': '3-O-methyl-isosecotanapartholide',
                                      'reason': 'No alpha,beta-unsaturated '
                                                'ketone (C=C-C=O) motif '
                                                'found.'},
                                  {   'smiles': 'O=C1C(=C(O)C=C1)C(=O)CCCCCCCCCC',
                                      'name': 'Chrysotrione B',
                                      'reason': 'No alpha,beta-unsaturated '
                                                'ketone (C=C-C=O) motif '
                                                'found.'},
                                  {   'smiles': '[H][C@@]1(CC[C@@]2([H])[C@]3([H])CCC4=CC(=O)CC[C@]4(C)[C@@]3([H])CC[C@]12C)[C@@H](C)O',
                                      'name': '(20R)-20-hydroxypregn-4-en-3-one',
                                      'reason': 'No alpha,beta-unsaturated '
                                                'ketone (C=C-C=O) motif '
                                                'found.'}],
    'attempt': 2,
    'reasoning': "Okay, let's analyze the previous attempt and the outcomes.\n"
                 '\n'
                 '**Reasoning:**\n'
                 '\n'
                 'The previous code used the SMARTS pattern '
                 '`[C]=[C]-[C](=[O])[!H]` to identify enones. This pattern '
                 'correctly identifies the core `C=C-C=O` motif and ensures '
                 'that the carbonyl carbon is not directly bonded to a '
                 'hydrogen (except through the double bond), which translates '
                 'to R4 != H.\n'
                 'However, the results reveal a low F1 score, with several '
                 'false positives and many false negatives.\n'
                 '\n'
                 '**False Positives:**\n'
                 'The false positives indicate that the current SMARTS pattern '
                 'is too broad, it is matching structures containing other '
                 'carbon-carbon double bonds conjugated to a carbonyl. '
                 'Specifically, the examples suggest problems with:\n'
                 '*   **Conjugated systems beyond the alpha-beta position**: '
                 'The SMARTS match seems to be overly permissive, identifying '
                 'conjugated carbonyl systems, such as extended polyenes, as '
                 'enones. The SMARTS should focus solely on the direct '
                 'alpha-beta relationship.\n'
                 '*   **Esters with conjugated double bonds:** Some false '
                 'positives appear when a carbon-carbon double bond is '
                 'directly conjugated with the carbonyl of an ester (-O-C=O), '
                 'that does not fullfil the definition of enones since the '
                 'carbonyl carbon of the ester is not connected to two other '
                 'carbons. This indicates that we should explicitly enforce a '
                 'carbon at the R4 position.\n'
                 '*   **Ring structures**: Sometimes, the conjugated double '
                 'bond and carbonyl system might be in a ring, and the SMARTS '
                 'does not fully take this into account.\n'
                 '*   **Acid anhydrides and related structures**: The current '
                 'pattern is matching, for instance, structures containing '
                 'multiple carboxyl groups.\n'
                 '\n'
                 '**False Negatives:**\n'
                 'The false negatives show that the pattern is too strict or '
                 'is missing certain forms of enones. Specifically:\n'
                 '*   **Missing various cyclic and acyclic enones**: The '
                 'pattern is missing a large number of canonical enones, so it '
                 'seems like we should allow for more generality in the '
                 'substitutions for the `C=C-C=O` motif.\n'
                 '*   **Stereochemistry:**  The pattern does not consider '
                 'stereochemistry of the double bond.\n'
                 '*   **Explicit hydrogens:** The SMARTS pattern might be too '
                 'strict with explicit hydrogens.\n'
                 '\n'
                 '**Improvements:**\n'
                 '\n'
                 'To address the issues, I will modify the SMARTS pattern and '
                 'introduce additional constraints:\n'
                 '\n'
                 '1.  **Refine SMARTS:** The SMARTS pattern needs to be more '
                 'specific to target the alpha-beta unsaturated ketone, '
                 'explicitly including the requirement of carbons connected to '
                 'the alpha and beta carbons and that the carbonyl carbon '
                 'connects to carbon as R4. Also, we need to allow hydrogens '
                 'to be present on the double bond. We can use the following: '
                 '`[C;!H0]=[C;!H0]-[C](=[O])[C;!H0]`\n'
                 '\n'
                 '2.  **Check for R4 != H**:  The SMARTS `[!H]` check may be '
                 'sufficient, but we can ensure that the carbon atom directly '
                 'bound to the carbonyl is not attached to any hydrogen atom '
                 '(other than via the double bond).\n'
                 '\n'
                 "Let's implement these improvements in the code.",
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 215,
    'num_false_positives': 1007,
    'num_true_negatives': 140361,
    'num_false_negatives': 717,
    'num_negatives': None,
    'precision': 0.17594108019639934,
    'recall': 0.23068669527896996,
    'f1': 0.19962859795728877,
    'accuracy': 0.9878847505270555,
    'negative_predictive_value': 0.9949177050993068}