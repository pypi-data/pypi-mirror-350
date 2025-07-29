"""
Classifies: CHEBI:15734 primary alcohol
"""
from rdkit import Chem

def is_primary_alcohol(smiles: str):
    """
    Determines if a molecule is a primary alcohol based on its SMILES string.
    A primary alcohol is defined as a hydroxyl group (-OH) attached to a saturated carbon,
    which is bonded to either two hydrogen atoms and one carbon atom or three hydrogen atoms.
    
    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a primary alcohol, False otherwise
        str: Reason for classification
    """
    
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
    
    # Define a primary alcohol pattern considering different cases
    primary_alcohol_pattern = Chem.MolFromSmarts("[CX4;H2][CH2][OX2H]")  # Primary alcohol where carbon has two H
    methanol_pattern = Chem.MolFromSmarts("[CH3][OX2H]")                # Methanol (special case)

    # Check for primary alcohol substructure
    if mol.HasSubstructMatch(primary_alcohol_pattern):
        return True, "Contains a primary alcohol group"
    
    # Check for methanol-like structure
    if mol.HasSubstructMatch(methanol_pattern):
        return True, "Contains a methanol-like primary alcohol group"
    
    return False, "Does not contain a primary alcohol group"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:15734',
                          'name': 'primary alcohol',
                          'definition': 'A primary alcohol is a compound in '
                                        'which a hydroxy group, -OH, is '
                                        'attached to a saturated carbon atom '
                                        'which has either three hydrogen atoms '
                                        'attached to it or only one other '
                                        'carbon atom and two hydrogen atoms '
                                        'attached to it.',
                          'parents': ['CHEBI:30879'],
                          'xrefs': ['KEGG:C00226'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 24,
                           'log_lines_of_code': 3.1780538303479458,
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
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 0,
                                                 1,
                                                 1,
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 1,
                                                 1],
                           'max_indent': 2,
                           'imports': ['from rdkit import Chem'],
                           'imports_count': 1,
                           'methods_called': [   'HasSubstructMatch',
                                                 'MolFromSmarts',
                                                 'MolFromSmiles'],
                           'methods_called_count': 3,
                           'smarts_strings': [   '[CX4;H2][CH2][OX2H]',
                                                 '"[CH3][OX2H]")                '
                                                 '# Methanol (special case'],
                           'smarts_strings_count': 2,
                           'defs': ['is_primary_alcohol(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'True, "Contains a primary alcohol '
                                          'group"',
                                          'True, "Contains a methanol-like '
                                          'primary alcohol group"',
                                          'False, "Does not contain a primary '
                                          'alcohol group"'],
                           'returns_count': 4,
                           'complexity': 2.635610766069589},
    'message': '\n'
               'Attempt failed: F1 score of 0.03625659954212026 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: '
               'O=C1N2[C@@]3([C@@]4([C@]5(N(CC4)C\\C(\\[C@](C5)([C@]3(CC1)[H])[H])=C\\CO)O)C=6C2=CC=CC6)[H] '
               'NAME: isopseudostrychnine REASON: CORRECT Contains a primary '
               'alcohol group\n'
               ' * SMILES: '
               'O=C1[C@]([C@@]2([C@@](CC1)(C=3C(CC2)=C(OC)C(=CC3O)C(C)C)C)[H])(CO)C '
               'NAME: triptonoterpenol REASON: CORRECT Contains a primary '
               'alcohol group\n'
               ' * SMILES: '
               '[H][C@@]1(CC[C@@]2([H])[C@]3([H])CCC4=CC(=O)CC[C@]4(C)[C@@]3([H])[C@@H](O)C[C@]12C=O)C(=O)CO '
               'NAME: aldosterone REASON: CORRECT Contains a primary alcohol '
               'group\n'
               ' * SMILES: '
               '[H][C@]12C[C@]3([H])C(=C)C(=O)O[C@@]3([H])[C@@H](O)\\C(C)=C\\CC\\C(C)=C\\CC[C@@]1(CO)O2 '
               'NAME: sinularolide C REASON: CORRECT Contains a primary '
               'alcohol group\n'
               ' * SMILES: S(OCCO)([H])(=O)=O NAME: 2-hydroxyethyl sulfonate '
               'REASON: CORRECT Contains a primary alcohol group\n'
               ' * SMILES: C(O)CCCN(CCCC)N=O NAME: '
               'N-butyl-N-(4-hydroxybutyl)nitrosamine REASON: CORRECT Contains '
               'a primary alcohol group\n'
               ' * SMILES: '
               'COc1ccc([C@@H](O)[C@H](CO)Oc2c(OC)cc(cc2OC)[C@@H]2OC[C@@H]3[C@H]2CO[C@H]3c2cc(OC)c(O)c(OC)c2)c(OC)c1O '
               'NAME: '
               "(-)-(7R,7'R,7''R,8S,8'S,8''S)-4',4''-dihydroxy-3,3',3'',5,5',5''-hexamethoxy-7,9':7',9-diepoxy-4,8''-oxy-8,8'-sesquineolignan-7'',9''-diol "
               'REASON: CORRECT Contains a primary alcohol group\n'
               ' * SMILES: '
               '[H][C@@]12CCC3=CC(=O)C=C[C@]3(C)[C@@]1([H])C(=O)C[C@@]1(C)[C@@]2([H])CC[C@]1(O)C(=O)CO '
               'NAME: prednisone REASON: CORRECT Contains a primary alcohol '
               'group\n'
               ' * SMILES: '
               'C[C@@H]([C@H]1CC[C@H]2[C@@H]3C[C@H]4O[C@]44[C@@H](O)[C@H](CC(=O)[C@]4(C)[C@H]3CC[C@]12C)OS(O)(=O)=O)[C@H]1CC(C)=C(CO)C(=O)O1 '
               'NAME: 2,3-dihydro-3beta-O-sulfate withaferin A REASON: CORRECT '
               'Contains a primary alcohol group\n'
               ' * SMILES: OCCc1ccc(O)c(O)c1 NAME: hydroxytyrosol REASON: '
               'CORRECT Contains a primary alcohol group\n'
               ' * SMILES: OCC(C(O)C)=O NAME: 1,3-dihydroxybutan-2-one REASON: '
               'CORRECT Contains a primary alcohol group\n'
               ' * SMILES: OCCNCCC(O)=O NAME: N-(2-hydroxyethyl)-beta-alanine '
               'REASON: CORRECT Contains a primary alcohol group\n'
               ' * SMILES: CC1=C(CO)C=CC=C1 NAME: 2-methylbenzyl alcohol '
               'REASON: CORRECT Contains a primary alcohol group\n'
               ' * SMILES: OCCCCCCCCCCCCCCCCC[C@@H](O)CC(O)=O NAME: '
               '(3R)-3,20-dihydroxyicosanoic acid REASON: CORRECT Contains a '
               'primary alcohol group\n'
               ' * SMILES: [H]C1(CO)CO1 NAME: glycidol REASON: CORRECT '
               'Contains a primary alcohol group\n'
               ' * SMILES: OCCN1CCOCC1 NAME: 2-(morpholin-4-yl)ethanol REASON: '
               'CORRECT Contains a primary alcohol group\n'
               ' * SMILES: OCCCCCCCCCC=C NAME: 10-undecen-1-ol REASON: CORRECT '
               'Contains a primary alcohol group\n'
               ' * SMILES: OCC1=C2[C@H]([C@@H](C)CC[C@@H]1CO)CC(C2)(C)C NAME: '
               'Tremulenediol A REASON: CORRECT Contains a primary alcohol '
               'group\n'
               ' * SMILES: '
               'OCC1=CC(=O)C2=C(C)C[C@@H]([C@]3(C(=C)C(=O)O[C@@]3([C@@]12[H])[H])[H])O '
               'NAME: lactucin REASON: CORRECT Contains a primary alcohol '
               'group\n'
               ' * SMILES: OCCCCCC\\C=C\\C(O)=O NAME: '
               '(2E)-9-hydroxynon-2-enoic acid REASON: CORRECT Contains a '
               'primary alcohol group\n'
               ' * SMILES: OCCC(CO)=C NAME: 2-methylene-1,4-butanediol REASON: '
               'CORRECT Contains a primary alcohol group\n'
               ' * SMILES: CC/C=C\\CCCCCO NAME: (Z)-non-6-en-1-ol REASON: '
               'CORRECT Contains a primary alcohol group\n'
               ' * SMILES: C(=O)(O)C[C@@H]1[C@@H](C(CC1)=O)C/C=C\\CCO NAME: '
               'tuberonic acid REASON: CORRECT Contains a primary alcohol '
               'group\n'
               ' * SMILES: OCC(=C(CC)[H])[H] NAME: 2-penten-1-ol REASON: '
               'CORRECT Contains a primary alcohol group\n'
               ' * SMILES: '
               'C(C(O)=O)C/C=C\\C/C=C\\C/C=C\\C=C\\[C@@H](C/C=C\\C/C=C\\CCO)O '
               'NAME: '
               '(4Z,7Z,10Z,12E,14R,16Z,19Z)-14,22-dihydroxydocosahexaenoic '
               'acid REASON: CORRECT Contains a primary alcohol group\n'
               'False positives: SMILES: '
               'CN1C2=C(C=CC(=C2)OC)C3=C1[C@H](N(CC34CCN(CC4)S(=O)(=O)C5=CC=CS5)CC6CC6)CO '
               'NAME: '
               "[(1S)-2-(cyclopropylmethyl)-7-methoxy-9-methyl-1'-thiophen-2-ylsulfonyl-1-spiro[1,3-dihydropyrido[3,4-b]indole-4,4'-piperidine]yl]methanol "
               'REASON: WRONGLY CLASSIFIED Contains a primary alcohol group\n'
               ' * SMILES: '
               'C[C@@H]1CN(C(=O)C2=C(N=CC(=C2)C3=CCCCC3)O[C@@H]1CN(C)CC4=CC=C(C=C4)C(=O)O)[C@H](C)CO '
               'NAME: '
               '4-[[[(2S,3R)-8-(1-cyclohexenyl)-5-[(2R)-1-hydroxypropan-2-yl]-3-methyl-6-oxo-3,4-dihydro-2H-pyrido[2,3-b][1,5]oxazocin-2-yl]methyl-methylamino]methyl]benzoic '
               'acid REASON: WRONGLY CLASSIFIED Contains a primary alcohol '
               'group\n'
               ' * SMILES: '
               'CC(C)(O)[C@H]1CC[C@@]2(C)[C@H]1CC[C@]1(CO)[C@@H]2C[C@@H](O)[C@@H]2[C@@]3(C)CCCC(C)(C)[C@@H]3[C@H](O)C[C@@]12C '
               'NAME: hopane-6beta,11alpha,22,27-tetraol REASON: WRONGLY '
               'CLASSIFIED Contains a primary alcohol group\n'
               ' * SMILES: O=C(NCC(O)=O)[C@@H](NC(=O)[C@@H](N)CO)CCCN=C(N)N '
               'NAME: Ser-Arg-Gly REASON: WRONGLY CLASSIFIED Contains a '
               'primary alcohol group\n'
               ' * SMILES: '
               'CN1C2=C(C=CC(=C2)OC)C3=C1[C@@H](N(CC34CCN(CC4)C(=O)CC5=CC=NC=C5)CC6=CC=NC=C6)CO '
               'NAME: '
               "1-[(1R)-1-(hydroxymethyl)-7-methoxy-9-methyl-2-(pyridin-4-ylmethyl)-1'-spiro[1,3-dihydropyrido[3,4-b]indole-4,4'-piperidine]yl]-2-pyridin-4-ylethanone "
               'REASON: WRONGLY CLASSIFIED Contains a primary alcohol group\n'
               ' * SMILES: O(C(=O)CCCCCCCCCCCCCCC)CCCCO NAME: Palmitic acid, '
               '4-hydroxybutyl ester REASON: WRONGLY CLASSIFIED Contains a '
               'primary alcohol group\n'
               ' * SMILES: '
               'C[C@@H]1CN(C(=O)CC2=C(C=CC(=C2)N(C)C)O[C@@H]1CN(C)S(=O)(=O)C3=C(ON=C3C)C)[C@H](C)CO '
               'NAME: '
               'N-[[(2S,3R)-9-(dimethylamino)-5-[(2R)-1-hydroxypropan-2-yl]-3-methyl-6-oxo-2,3,4,7-tetrahydro-1,5-benzoxazonin-2-yl]methyl]-N,3,5-trimethyl-4-isoxazolesulfonamide '
               'REASON: WRONGLY CLASSIFIED Contains a primary alcohol group\n'
               ' * SMILES: '
               'O([C@H]1[C@@H](O)[C@H](O[C@@H](O[C@H]2[C@@H](O)[C@H](OC(O)[C@@H]2NC(=O)C)CO[C@@H]3O[C@@H]([C@@H](O[C@@H]4O[C@@H]([C@H](O)[C@H](O)[C@H]4O[C@@H]5O[C@H]([C@@H](O)[C@@H](O)[C@@H]5O)C)CO)[C@H](O)[C@H]3NC(=O)C)CO)[C@@H]1O)CO[C@@H]6O[C@@H]([C@@H](O[C@@H]7O[C@@H]([C@H](O[C@H]8O[C@@H]([C@@H](O)[C@H](O)[C@H]8NC(=O)C)CO)[C@H](O)[C@H]7O)CO)[C@H](O)[C@H]6NC(=O)C)CO)[C@@H]9O[C@@H]([C@@H](O[C@@H]%10O[C@@H]([C@H](O)[C@H](O)[C@H]%10O[C@@H]%11O[C@H]([C@@H](O)[C@@H](O)[C@@H]%11O)C)CO)[C@H](O)[C@H]9NC(=O)C)CO '
               'NAME: '
               'N-[(2R,3R,4R,5S,6R)-2-[(2R,3R,4R,5R,6S)-6-[(2R,3S,4R,5R,6R)-5-Acetamido-6-[[(2R,3S,4S,5R,6R)-6-[(2R,3R,4R,5R)-5-acetamido-2-[[(2S,3R,4R,5S,6R)-3-acetamido-5-[(2S,3R,4S,5R,6R)-4,5-dihydroxy-6-(hydroxymethyl)-3-[(2S,3S,4R,5S,6S)-3,4,5-trihydroxy-6-methyloxan-2-yl]oxyoxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxymethyl]-3,6-dihydroxyoxan-4-yl]oxy-4-[(2S,3R,4R,5S,6R)-3-acetamido-5-[(2S,3R,4S,5R,6R)-4,5-dihydroxy-6-(hydroxymethyl)-3-[(2S,3S,4R,5S,6S)-3,4,5-trihydroxy-6-methyloxan-2-yl]oxyoxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-3,5-dihydroxyoxan-2-yl]methoxy]-4-hydroxy-2-(hydroxymethyl)oxan-3-yl]oxy-4,5-dihydroxy-2-(hydroxymethyl)oxan-3-yl]oxy-4,5-dihydroxy-6-(hydroxymethyl)oxan-3-yl]acetamide '
               'REASON: WRONGLY CLASSIFIED Contains a primary alcohol group\n'
               ' * SMILES: '
               'O([C@H]1[C@H](O[C@@H]2O[C@H]([C@@H](O)[C@@H](O)[C@@H]2O)C)[C@@H](NC(=O)C)[C@@H](O[C@@H]1CO)O)[C@@H]3O[C@@H]([C@@H](O[C@@H]4O[C@@H]([C@@H](O)[C@H](O)[C@@H]4O[C@@H]5O[C@@H]([C@H](O)[C@H]5O)CO)CO[C@H]6O[C@@H]([C@@H](O)[C@H](O)[C@@H]6O)CO)[C@H](O)[C@H]3NC(=O)C)CO '
               'NAME: '
               'N-[(2S,3R,4R,5S,6R)-2-[(2R,3S,4R,5R,6R)-5-Acetamido-6-hydroxy-2-(hydroxymethyl)-4-[(2S,3S,4R,5S,6S)-3,4,5-trihydroxy-6-methyloxan-2-yl]oxyoxan-3-yl]oxy-5-[(2S,3S,4S,5S,6R)-3-[(2S,3R,4R,5R)-3,4-dihydroxy-5-(hydroxymethyl)oxolan-2-yl]oxy-4,5-dihydroxy-6-[[(2S,3S,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxymethyl]oxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-3-yl]acetamide '
               'REASON: WRONGLY CLASSIFIED Contains a primary alcohol group\n'
               ' * SMILES: '
               'O1[C@@H]([C@@H](O)[C@H](O[C@H]2O[C@@H]([C@@H](O)[C@H](O)[C@@H]2O)CO)[C@H](O)[C@@H]1O[C@H]3[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]3CO)O[C@@H]([C@H](O)[C@@H](NC(=O)C)CO)[C@H](O)CO)CO[C@H]4O[C@@H]([C@@H](O)[C@H](O[C@H]5O[C@@H]([C@@H](O)[C@H](O)[C@@H]5O[C@H]6O[C@@H]([C@@H](O)[C@H](O)[C@@H]6O)CO)CO)[C@@H]4O)CO[C@H]7O[C@@H]([C@@H](O)[C@H](O)[C@@H]7O[C@H]8O[C@@H]([C@@H](O)[C@H](O)[C@@H]8O)CO)CO '
               'NAME: '
               'N-[(2S,3R,4R,5S,6R)-2-[(2R,3S,4R,5S)-5-Acetamido-1,2,4,6-tetrahydroxyhexan-3-yl]oxy-5-[(2S,3S,4S,5R,6R)-6-[[(2S,3S,4S,5R,6R)-4-[(2S,3S,4S,5S,6R)-4,5-dihydroxy-6-(hydroxymethyl)-3-[(2R,3S,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-6-[[(2S,3S,4S,5S,6R)-4,5-dihydroxy-6-(hydroxymethyl)-3-[(2R,3S,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxymethyl]-3,5-dihydroxyoxan-2-yl]oxymethyl]-3,5-dihydroxy-4-[(2R,3S,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-3-yl]acetamide '
               'REASON: WRONGLY CLASSIFIED Contains a primary alcohol group\n'
               ' * SMILES: '
               'O=C1N([C@H](C(=O)N([C@H](C(=O)OC[C@@H](C=C1)NC(=O)[C@@H](NC(=O)C[C@H](O)[C@@H](NC(=O)[C@@H](NC(=O)[C@@H](NC(=O)C/C=C\\CCCCCC)CC2=CC=C(O)C=C2)C(C)C)CO)C(C)C)CC3=CC=C(O)C=C3)C)C(C)C)C '
               'NAME: Thalabetaospiramide A6 REASON: WRONGLY CLASSIFIED '
               'Contains a primary alcohol group\n'
               ' * SMILES: '
               'C[C@H]1CN(C(=O)C2=C(C3=CC=CC=C3CO[C@H]1CN(C)C(=O)CCN(C)C)C4=CC=CC=C4N2C)[C@H](C)CO '
               'NAME: LSM-11210 REASON: WRONGLY CLASSIFIED Contains a primary '
               'alcohol group\n'
               ' * SMILES: '
               'O=C([C@@]1([C@@H]2[C@@H](C=C[C@@H]1C)C[C@](O)(C)CC2)C)CCO '
               'NAME: Peaurantiogriseol C REASON: WRONGLY CLASSIFIED Contains '
               'a primary alcohol group\n'
               ' * SMILES: '
               'O=C[C@]1([C@@H](O)CC[C@]2([C@H]1CCC3=C2CC[C@]4([C@]3(CC[C@@H]4[C@@H](CO)C)C)C)C)C '
               'NAME: Cladosporide A REASON: WRONGLY CLASSIFIED Contains a '
               'primary alcohol group\n'
               ' * SMILES: '
               'C1COCCC1C(=O)N2C[C@@H]3[C@@H]([C@@H](N3CC4=CC=C(C=C4)Cl)CO)C5=CC=CC=C52 '
               'NAME: '
               '[(1R,2aS,8bS)-2-[(4-chlorophenyl)methyl]-1-(hydroxymethyl)-1,2a,3,8b-tetrahydroazeto[2,3-c]quinolin-4-yl]-(4-oxanyl)methanone '
               'REASON: WRONGLY CLASSIFIED Contains a primary alcohol group\n'
               ' * SMILES: '
               'C1(=CC(=CC2=C1C(C3=C(C(=C(C=C3C2=O)O)C(CO)CCOC(C)=O)O)=O)O)O '
               'NAME: versiconol acetate REASON: WRONGLY CLASSIFIED Contains a '
               'primary alcohol group\n'
               ' * SMILES: '
               'O([C@@H]1[C@@H](O)[C@H](O[C@H]2[C@H](O)[C@@H](NC(=O)C)[C@H](O[C@@H]3[C@@H](O)[C@H](O[C@H]4[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]4CO)O[C@@H]5[C@@H](O)[C@@H](O[C@@H]([C@@H]5O)CO)O[C@H]6[C@H](O)[C@@H](O)[C@@H](O[C@@H]6CO)O)O[C@@H]([C@@H]3O)CO)O[C@@H]2CO)O[C@@H]([C@@H]1O)CO)[C@@H]7O[C@@H]([C@@H](O[C@@H]8O[C@@H]([C@H](O)[C@H](O[C@@H]9O[C@@H]([C@@H](O[C@@H]%10O[C@@H]([C@H](O)[C@H](O[C@]%11(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%11)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%10O)CO)[C@H](O)[C@H]9NC(=O)C)CO)[C@H]8O)CO)[C@H](O)[C@H]7NC(=O)C)CO '
               'NAME: '
               '(2S,4S,5R,6R)-5-Acetamido-2-[(2S,3R,4S,5S,6R)-2-[(2R,3S,4R,5R,6S)-5-acetamido-6-[(2S,3R,4S,5S,6R)-2-[(2R,3S,4R,5R,6S)-5-acetamido-6-[(2S,3R,4S,5S,6R)-2-[(2R,3S,4R,5R,6S)-5-acetamido-6-[(2S,3R,4S,5S,6R)-2-[(2R,3S,4R,5R,6S)-5-acetamido-6-[(2R,3S,4S,5R,6S)-3,5-dihydroxy-2-(hydroxymethyl)-6-[(2R,3S,4R,5R,6R)-4,5,6-trihydroxy-2-(hydroxymethyl)oxan-3-yl]oxyoxan-4-yl]oxy-4-hydroxy-2-(hydroxymethyl)oxan-3-yl]oxy-3,5-dihydroxy-6-(hydroxymethyl)oxan-4-yl]oxy-4-hydroxy-2-(hydroxymethyl)oxan-3-yl]oxy-3,5-dihydroxy-6-(hydroxymethyl)oxan-4-yl]oxy-4-hydroxy-2-(hydroxymethyl)oxan-3-yl]oxy-3,5-dihydroxy-6-(hydroxymethyl)oxan-4-yl]oxy-4-hydroxy-2-(hydroxymethyl)oxan-3-yl]oxy-3,5-dihydroxy-6-(hydroxymethyl)oxan-4-yl]oxy-4-hydroxy-6-[(1R,2R)-1,2,3-trihydroxypropyl]oxane-2-carboxylic '
               'acid REASON: WRONGLY CLASSIFIED Contains a primary alcohol '
               'group\n'
               ' * SMILES: '
               'C[C@H]1CCCCO[C@@H]([C@H](CN(C(=O)C2=C(O1)C=CC(=C2)NC(=O)NC3=CC4=C(C=C3)OCO4)[C@@H](C)CO)C)CN(C)C '
               'NAME: '
               '1-(1,3-benzodioxol-5-yl)-3-[(3S,9S,10S)-9-[(dimethylamino)methyl]-12-[(2S)-1-hydroxypropan-2-yl]-3,10-dimethyl-13-oxo-2,8-dioxa-12-azabicyclo[12.4.0]octadeca-1(14),15,17-trien-16-yl]urea '
               'REASON: WRONGLY CLASSIFIED Contains a primary alcohol group\n'
               ' * SMILES: '
               'C1CCC(C1)(C2=CN(N=N2)CC[C@@H]3CC[C@H]([C@H](O3)CO)NS(=O)(=O)C4=CC=C(C=C4)Cl)O '
               'NAME: '
               '4-chloro-N-[(2S,3R,6S)-6-[2-[4-(1-hydroxycyclopentyl)-1-triazolyl]ethyl]-2-(hydroxymethyl)-3-oxanyl]benzenesulfonamide '
               'REASON: WRONGLY CLASSIFIED Contains a primary alcohol group\n'
               ' * SMILES: '
               'O1[C@@H](O[C@H]2[C@@H](O)[C@H](O)[C@H](O[C@@H]2OC[C@H]3O[C@@H](O[C@H]4[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]4CO)O[C@H]5[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]5CO[C@@H]6O[C@H]([C@@H](O)[C@@H](O)[C@@H]6O)C)O)[C@@H](O)[C@@H](O)[C@@H]3O)CO)[C@H](NC(=O)C)[C@@H](O)[C@H](O[C@@H]7O[C@@H]([C@H](O)[C@H](O)[C@H]7O[C@@H]8O[C@H]([C@@H](O)[C@@H](O)[C@@H]8O)C)CO)[C@H]1CO '
               'NAME: '
               'N-[(2R,3R,4R,5S,6R)-5-[(2S,3R,4R,5S,6R)-3-Acetamido-5-[(2S,3S,4S,5S,6R)-6-[[(2S,3S,4S,5S,6R)-3-[(2S,3R,4R,5S,6R)-3-acetamido-5-[(2S,3R,4S,5R,6R)-4,5-dihydroxy-6-(hydroxymethyl)-3-[(2R,3S,4R,5S,6S)-3,4,5-trihydroxy-6-methyloxan-2-yl]oxyoxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxymethyl]-3,4,5-trihydroxyoxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-2,4-dihydroxy-6-[[(2R,3S,4R,5S,6S)-3,4,5-trihydroxy-6-methyloxan-2-yl]oxymethyl]oxan-3-yl]acetamide '
               'REASON: WRONGLY CLASSIFIED Contains a primary alcohol group\n'
               ' * SMILES: '
               'O([C@H]1O[C@@H]([C@@H](O[C@@H]2O[C@@H]([C@@H](O[C@@H]3O[C@@H]([C@H](O)[C@H](O)[C@H]3O)CO)[C@H](O)[C@H]2NC(=O)C)CO)[C@H](O)[C@@H]1O[C@@H]4O[C@@H]([C@@H](O[C@@H]5O[C@@H]([C@H](O)[C@H](O)[C@H]5NC(=O)C)CO)[C@H](O)[C@@H]4NC(=O)C)CO)CO)[C@@H]6[C@H](O)[C@@H](O[C@@H]([C@H]6O)CO[C@H]7O[C@@H]([C@@H](O)[C@H](O)[C@@H]7O[C@@H]8O[C@@H]([C@@H](O[C@@H]9O[C@@H]([C@H](O)[C@H](O[C@H]%10O[C@@H]([C@H](O)[C@H](O)[C@H]%10O)CO)[C@H]9O)CO)[C@H](O)[C@H]8NC(=O)C)CO)CO)O[C@H]%11[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]%11CO)O[C@H]%12[C@H](O)[C@@H](NC(=O)C)C(O[C@@H]%12CO[C@@H]%13O[C@H]([C@@H](O)[C@@H](O)[C@@H]%13O)C)O '
               'NAME: '
               'N-[(3R,4R,5S,6R)-5-[(2S,3R,4R,5S,6R)-3-Acetamido-5-[(2S,3S,4S,5R,6R)-4-[(2R,3S,4S,5S,6R)-3-[(2S,3R,4R,5S,6R)-3-acetamido-5-[(2S,3R,4R,5R,6R)-3-acetamido-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-5-[(2S,3R,4R,5S,6R)-3-acetamido-4-hydroxy-6-(hydroxymethyl)-5-[(2S,3R,4S,5R,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-6-[[(2S,3S,4S,5S,6R)-3-[(2S,3R,4R,5S,6R)-3-acetamido-5-[(2S,3R,4S,5S,6R)-3,5-dihydroxy-6-(hydroxymethyl)-4-[(2R,3R,4S,5R,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxymethyl]-3,5-dihydroxyoxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-2,4-dihydroxy-6-[[(2R,3S,4R,5S,6S)-3,4,5-trihydroxy-6-methyloxan-2-yl]oxymethyl]oxan-3-yl]acetamide '
               'REASON: WRONGLY CLASSIFIED Contains a primary alcohol group\n'
               ' * SMILES: '
               'COC1=CC=CC=C1CNC(=O)C[C@H]2C[C@H]3[C@@H]([C@H](O2)CO)OC4=C3C=C(C=C4)NS(=O)(=O)C5=CC=C(C=C5)F '
               'NAME: '
               '2-[(1R,3R,4aR,9aS)-6-[(4-fluorophenyl)sulfonylamino]-1-(hydroxymethyl)-3,4,4a,9a-tetrahydro-1H-pyrano[3,4-b]benzofuran-3-yl]-N-[(2-methoxyphenyl)methyl]acetamide '
               'REASON: WRONGLY CLASSIFIED Contains a primary alcohol group\n'
               ' * SMILES: '
               'COC(=O)c1cc(O[C@@H]2O[C@H](CO[C@@H]3OC[C@](O)(CO)[C@H]3O)[C@@H](O)[C@H](O)[C@H]2O)ccc1O '
               'NAME: Saccharumoside C REASON: WRONGLY CLASSIFIED Contains a '
               'primary alcohol group\n'
               ' * SMILES: '
               'CC1=CC=C(C=C1)S(=O)(=O)N(C[C@@H](C)[C@@H](CN(C)C(=O)C2=CC3=C(C=C2)OCO3)OC)[C@@H](C)CO '
               'NAME: '
               'N-[(2S,3R)-4-[[(2S)-1-hydroxypropan-2-yl]-(4-methylphenyl)sulfonylamino]-2-methoxy-3-methylbutyl]-N-methyl-1,3-benzodioxole-5-carboxamide '
               'REASON: WRONGLY CLASSIFIED Contains a primary alcohol group\n'
               ' * SMILES: '
               'C[C@@H]1CN(C(=O)C2=C(C=CC(=C2)NC(=O)CN3C=NN=N3)O[C@H]1CN(C)CC4=CC=C(C=C4)C(F)(F)F)[C@@H](C)CO '
               'NAME: '
               'N-[(2R,3R)-5-[(2S)-1-hydroxypropan-2-yl]-3-methyl-2-[[methyl-[[4-(trifluoromethyl)phenyl]methyl]amino]methyl]-6-oxo-3,4-dihydro-2H-1,5-benzoxazocin-8-yl]-2-(1-tetrazolyl)acetamide '
               'REASON: WRONGLY CLASSIFIED Contains a primary alcohol group\n'
               'False negatives: SMILES: [H][C@@]1(CCC(C)=CC1)C(C)(C)O NAME: '
               '(S)-(-)-alpha-terpineol REASON: MISSED Does not contain a '
               'primary alcohol group\n'
               ' * SMILES: Clc1c2COC(=O)c2c(Cl)c(Cl)c1Cl NAME: '
               '4,5,6,7-tetrachloro-2-benzofuran-1(3H)-one REASON: MISSED Does '
               'not contain a primary alcohol group\n'
               ' * SMILES: C[C@@](O)(CCOP(O)(O)=O)CC(O)=O NAME: '
               '(R)-5-phosphomevalonic acid REASON: MISSED Does not contain a '
               'primary alcohol group\n'
               ' * SMILES: OC1C=C(Cl)C(Cl)C=C1Cl NAME: '
               '2,4,5-trichlorocyclohexa-2,5-dien-1-ol REASON: MISSED Does not '
               'contain a primary alcohol group\n'
               ' * SMILES: '
               'C1=CC=C2C(=C1)[C@]34CCN5CC6=CCO[C@H]([C@]([C@]6(C[C@@]35[H])[H])([C@@]4(N2)[H])[H])O '
               'NAME: caracurine VII REASON: MISSED Does not contain a primary '
               'alcohol group\n'
               ' * SMILES: CN=C(C)[C@H](O)c1ccccc1 NAME: '
               '(R)-2-methylimino-1-phenylpropan-1-ol REASON: MISSED Does not '
               'contain a primary alcohol group\n'
               ' * SMILES: [H][C@]1(CCC(C)=CC1)C(C)(C)O NAME: '
               '(R)-(+)-alpha-terpineol REASON: MISSED Does not contain a '
               'primary alcohol group\n'
               ' * SMILES: CC(C)C1(O)CCC(C)=CC1 NAME: 4-terpineol REASON: '
               'MISSED Does not contain a primary alcohol group\n'
               ' * SMILES: CC1=CCC(CC1)C(C)(C)O NAME: alpha-terpineol REASON: '
               'MISSED Does not contain a primary alcohol group\n'
               ' * SMILES: '
               'C1=CC=C2C(=C1)[C@]34CC[NH+]5CC6=CCOC([C@]([C@]6(C[C@@]35[H])[H])([C@@]4(N2C(CC([O-])=O)=O)[H])[H])O '
               'NAME: N-malonamoyl-Wieland-Gumlich aldehyde zwitterion REASON: '
               'MISSED Does not contain a primary alcohol group\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'O1[C@H]([C@@H](O)CC=2C1=CC=CC2)C3=CC=CC=C3',
                                     'name': 'cis-(+)-3-Flavanol',
                                     'reason': 'Does not contain a primary '
                                               'alcohol group'},
                                 {   'smiles': 'O1C2C34C(C(N(CC3)C)CC5=C4C1=C(OC)C=C5)C=CC2OC',
                                     'name': '6-O-Methylcodeine',
                                     'reason': 'Does not contain a primary '
                                               'alcohol group'},
                                 {   'smiles': 'CN1C2=C(C=CC(=C2)OC)C3=C1[C@H](N(CC34CCN(CC4)S(=O)(=O)C5=CC=CS5)CC6CC6)CO',
                                     'name': "[(1S)-2-(cyclopropylmethyl)-7-methoxy-9-methyl-1'-thiophen-2-ylsulfonyl-1-spiro[1,3-dihydropyrido[3,4-b]indole-4,4'-piperidine]yl]methanol",
                                     'reason': 'Does not contain a primary '
                                               'alcohol group'},
                                 {   'smiles': 'O(C(=O)CCCCCCCCCCCCCCC)[C@@H](COC(=O)CCCCCCCCCCCCCCCCCCC)COC(=O)CCCCCCC',
                                     'name': 'TG(20:0/16:0/8:0)',
                                     'reason': 'Does not contain a primary '
                                               'alcohol group'},
                                 {   'smiles': 'O[C@@H]1CC2[C@](C3=C(C4=NCCC([C@@]4(C)CC3)[C@@H](CCC(C(C)C)C)C)CC2)(C)CC1',
                                     'name': 'UCA-1064-B',
                                     'reason': 'Does not contain a primary '
                                               'alcohol group'},
                                 {   'smiles': 'C1=CC=C(C=C1)N2C(=NN=C2SCC#N)COC3=CC=CC=C3',
                                     'name': '2-[[5-(phenoxymethyl)-4-phenyl-1,2,4-triazol-3-yl]thio]acetonitrile',
                                     'reason': 'Does not contain a primary '
                                               'alcohol group'},
                                 {   'smiles': 'O=C1C=2OC([C@H]3C[C@H](O)C(=C[C@H]3C2C(=O)C=4C1=C(O)C(=C(O)C4)C)C)(C)C',
                                     'name': 'Unnamed naphterpin 1',
                                     'reason': 'Does not contain a primary '
                                               'alcohol group'},
                                 {   'smiles': 'O([C@@H]1[C@]2(C([C@@](C1)(CC2)[H])(C)C)C)C(=O)/C=C/C3=CC=C(O)C=C3',
                                     'name': '(1R,4R)-1,7,7-Trimethylbicyclo[2.2.1]heptane-2beta-ol '
                                             '3-(4-hydroxyphenyl)acrylate',
                                     'reason': 'Does not contain a primary '
                                               'alcohol group'},
                                 {   'smiles': 'CC1(C)CC[C@@]2(CC[C@]3(C)C(=CC[C@@H]4[C@@]5(C)CC[C@H](O)C(C)(C)[C@@H]5CC[C@@]34C)[C@@H]2C1)C([O-])=O',
                                     'name': 'oleanolate',
                                     'reason': 'Does not contain a primary '
                                               'alcohol group'},
                                 {   'smiles': 'C[C@@H]1CN(C(=O)C2=C(N=CC(=C2)C3=CCCCC3)O[C@@H]1CN(C)CC4=CC=C(C=C4)C(=O)O)[C@H](C)CO',
                                     'name': '4-[[[(2S,3R)-8-(1-cyclohexenyl)-5-[(2R)-1-hydroxypropan-2-yl]-3-methyl-6-oxo-3,4-dihydro-2H-pyrido[2,3-b][1,5]oxazocin-2-yl]methyl-methylamino]methyl]benzoic '
                                             'acid',
                                     'reason': 'Does not contain a primary '
                                               'alcohol group'}],
    'sample_false_negatives': [   {   'smiles': 'O=C1N2[C@@]3([C@@]4([C@]5(N(CC4)C\\C(\\[C@](C5)([C@]3(CC1)[H])[H])=C\\CO)O)C=6C2=CC=CC6)[H]',
                                      'name': 'isopseudostrychnine',
                                      'reason': 'Does not contain a primary '
                                                'alcohol group'},
                                  {   'smiles': 'O=C1[C@]([C@@]2([C@@](CC1)(C=3C(CC2)=C(OC)C(=CC3O)C(C)C)C)[H])(CO)C',
                                      'name': 'triptonoterpenol',
                                      'reason': 'Does not contain a primary '
                                                'alcohol group'},
                                  {   'smiles': '[H][C@@]1(CC[C@@]2([H])[C@]3([H])CCC4=CC(=O)CC[C@]4(C)[C@@]3([H])[C@@H](O)C[C@]12C=O)C(=O)CO',
                                      'name': 'aldosterone',
                                      'reason': 'Does not contain a primary '
                                                'alcohol group'},
                                  {   'smiles': '[H][C@]12C[C@]3([H])C(=C)C(=O)O[C@@]3([H])[C@@H](O)\\C(C)=C\\CC\\C(C)=C\\CC[C@@]1(CO)O2',
                                      'name': 'sinularolide C',
                                      'reason': 'Does not contain a primary '
                                                'alcohol group'},
                                  {   'smiles': 'COc1ccc([C@@H](O)[C@H](CO)Oc2c(OC)cc(cc2OC)[C@@H]2OC[C@@H]3[C@H]2CO[C@H]3c2cc(OC)c(O)c(OC)c2)c(OC)c1O',
                                      'name': "(-)-(7R,7'R,7''R,8S,8'S,8''S)-4',4''-dihydroxy-3,3',3'',5,5',5''-hexamethoxy-7,9':7',9-diepoxy-4,8''-oxy-8,8'-sesquineolignan-7'',9''-diol",
                                      'reason': 'Does not contain a primary '
                                                'alcohol group'},
                                  {   'smiles': '[H][C@@]12CCC3=CC(=O)C=C[C@]3(C)[C@@]1([H])C(=O)C[C@@]1(C)[C@@]2([H])CC[C@]1(O)C(=O)CO',
                                      'name': 'prednisone',
                                      'reason': 'Does not contain a primary '
                                                'alcohol group'},
                                  {   'smiles': 'C[C@@H]([C@H]1CC[C@H]2[C@@H]3C[C@H]4O[C@]44[C@@H](O)[C@H](CC(=O)[C@]4(C)[C@H]3CC[C@]12C)OS(O)(=O)=O)[C@H]1CC(C)=C(CO)C(=O)O1',
                                      'name': '2,3-dihydro-3beta-O-sulfate '
                                              'withaferin A',
                                      'reason': 'Does not contain a primary '
                                                'alcohol group'},
                                  {   'smiles': 'OCC(C(O)C)=O',
                                      'name': '1,3-dihydroxybutan-2-one',
                                      'reason': 'Does not contain a primary '
                                                'alcohol group'},
                                  {   'smiles': 'CC1=C(CO)C=CC=C1',
                                      'name': '2-methylbenzyl alcohol',
                                      'reason': 'Does not contain a primary '
                                                'alcohol group'},
                                  {   'smiles': '[H]C1(CO)CO1',
                                      'name': 'glycidol',
                                      'reason': 'Does not contain a primary '
                                                'alcohol group'}],
    'attempt': 2,
    'reasoning': 'To address the misclassification of primary alcohols, we '
                 'need to refine the SMARTS pattern used to identify primary '
                 'alcohols. The essential characteristic of a primary alcohol '
                 'is a hydroxyl group (-OH) attached to a saturated carbon '
                 'that is only connected to one other carbon (or none, in the '
                 'case of methanol).\n'
                 '\n'
                 'Upon reviewing the previous attempt, it seems the pattern '
                 'only captured primary alcohols with two hydrogen atoms '
                 'attached ([CX4;H2][OX2H]), which may not cover edge cases or '
                 'certain complexities such as branching or methanol itself.\n'
                 '\n'
                 'Here’s how we can improve the classification:\n'
                 '\n'
                 '1. **Ensure the pattern captures all types of primary '
                 'alcohols**:\n'
                 '   - The primary carbon may have different substitution '
                 'patterns, such as being bonded to another carbon or having '
                 'additional branching.\n'
                 '   - Include methanol in the checks due to its unique case '
                 'with three hydrogens.\n'
                 '\n'
                 '2. **Enhance pattern flexibility**: The pattern needs to '
                 'flexibly capture primary alcohols in various structures, '
                 'possibly by focusing more on the nature of the carbon '
                 '(primary) and the presence of the hydroxyl group.\n'
                 '\n'
                 "Let's write the extended function leveraging these "
                 'improvements:',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 311,
    'num_false_positives': 1511,
    'num_true_negatives': 140000,
    'num_false_negatives': 478,
    'num_negatives': None,
    'precision': 0.1706915477497256,
    'recall': 0.394169835234474,
    'f1': 0.2382229031022597,
    'accuracy': 0.9860224877020379,
    'negative_predictive_value': 0.9965973319665713}