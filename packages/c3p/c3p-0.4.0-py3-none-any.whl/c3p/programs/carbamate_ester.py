"""
Classifies: CHEBI:23003 carbamate ester
"""
"""
Classifies: carbamate ester
"""
from rdkit import Chem

def is_carbamate_ester(smiles: str):
    """
    Determines if a molecule is a carbamate ester based on its SMILES string.
    A carbamate ester has the general structure -[N]-C(=O)-O-, where nitrogen may have substituents.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a carbamate ester, False otherwise
        str: Reason for classification
    """
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # SMARTS pattern for carbamate ester group
    carbamate_pattern = Chem.MolFromSmarts("[N]-C(=O)-[O]")
    # SMARTS pattern for amides
    amide_pattern = Chem.MolFromSmarts("[N]-C(=O)-[C]")

    # Check for amides
    if mol.HasSubstructMatch(amide_pattern):
        return False, "Contains an amide, not a carbamate"
    
    #Check for the carbamate pattern
    if mol.HasSubstructMatch(carbamate_pattern):
         return True, "Contains a carbamate ester group"
    else:
        return False, "Does not contain a carbamate ester group"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:23003',
                          'name': 'carbamate ester',
                          'definition': 'Any ester of carbamic acid or its '
                                        'N-substituted derivatives.',
                          'parents': ['CHEBI:33308'],
                          'xrefs': ['Wikipedia:Carbamate'],
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
                                                 0,
                                                 1,
                                                 1,
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2],
                           'max_indent': 2,
                           'imports': ['from rdkit import Chem'],
                           'imports_count': 1,
                           'methods_called': [   'MolFromSmiles',
                                                 'MolFromSmarts',
                                                 'HasSubstructMatch'],
                           'methods_called_count': 3,
                           'smarts_strings': ['[N]-C(=O)-[C]', '[N]-C(=O)-[O]'],
                           'smarts_strings_count': 2,
                           'defs': ['is_carbamate_ester(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "Contains an amide, not a '
                                          'carbamate"',
                                          'True, "Contains a carbamate ester '
                                          'group"',
                                          'False, "Does not contain a '
                                          'carbamate ester group"'],
                           'returns_count': 4,
                           'complexity': 2.6437751649736403},
    'message': '\n'
               'Attempt failed: F1 score of 0 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: NONE\n'
               'False positives: NONE\n'
               'False negatives: SMILES: '
               'C=1(C=CC([N+](=O)[O-])=CC1)OC([C@@H](NC(OC(C)(C)C)=O)CC(N)=O)=O '
               'NAME: Boc-Asn-OPhNO2 REASON: MISSED Contains an amide, not a '
               'carbamate\n'
               ' * SMILES: '
               '[H][C@]12OCC[C@@]1([H])[C@H](CO2)OC(=O)N[C@@H](Cc1ccccc1)[C@H](O)CN(CC(C)C)S(=O)(=O)c1ccc(N)cc1 '
               'NAME: darunavir REASON: MISSED Contains an amide, not a '
               'carbamate\n'
               ' * SMILES: '
               '[H][C@]12N\\C(N[C@]1([H])C(=O)NC[C@H]2O)=N/[C@@H]1O[C@H](CO)[C@H](OC(N)=O)[C@@H](O)[C@H]1NC(=O)C[C@@H](N)CCCN '
               'NAME: streptothricin F REASON: MISSED Contains an amide, not a '
               'carbamate\n'
               ' * SMILES: COC(=O)CC(NC(=O)C(NC(=O)OC(C)C)C(C)C)c1ccc(Cl)cc1 '
               'NAME: methyl '
               '3-(4-chlorophenyl)-3-{[N-(isopropoxycarbonyl)valyl]amino}propanoate '
               'REASON: MISSED Contains an amide, not a carbamate\n'
               ' * SMILES: CNC(=O)Oc1cc(C)c(C)c(C)c1 NAME: '
               '3,4,5-trimethylphenyl methylcarbamate REASON: MISSED Contains '
               'an amide, not a carbamate\n'
               ' * SMILES: CCN(C(=O)Oc1cccc(NC(=O)OC(C)C)c1)c1ccccc1 NAME: '
               'Phenisopham REASON: MISSED Contains an amide, not a carbamate\n'
               ' * SMILES: CCOC(=O)Nc1ccc(NCc2ccc(F)cc2)cc1N NAME: ezogabine '
               'REASON: MISSED Contains an amide, not a carbamate\n'
               ' * SMILES: NC(=O)OC1(CCCCC1)C#C NAME: ethinamate REASON: '
               'MISSED Contains an amide, not a carbamate\n'
               ' * SMILES: '
               'CC[C@H]1[C@@H](O)[C@H](C)C\\C(C)=C\\C=C\\[C@H](OC)[C@H](OC(=O)\\C(OC)=C\\C(\\C)=C\\[C@@H](C)[C@H]1O)[C@@H](C)[C@@H](O)[C@H](C)[C@H]1C[C@@H](O[C@H]2C[C@@H](O)[C@H](OC(N)=O)[C@@H](C)O2)[C@H](C)[C@H](O1)\\C=C\\C '
               'NAME: 21-deoxyconcanamycin A REASON: MISSED Contains an amide, '
               'not a carbamate\n'
               ' * SMILES: '
               'COC(=O)N[C@@H](C(Cc1c(C)nc2n(C)c3n(cnc3c(=O)n12)[C@@H]1O[C@H](CO)[C@@H](O)[C@H]1O)OO)C(=O)OC '
               'NAME: wybutoxosine REASON: MISSED Contains an amide, not a '
               'carbamate\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'CCN1N=C(N=N1)C2=CC=CC=C2NC(=O)C3=CC=C(C=C3)N4C=NN=N4',
                                     'name': 'N-[2-(2-ethyl-5-tetrazolyl)phenyl]-4-(1-tetrazolyl)benzamide',
                                     'reason': 'Does not contain a carbamate '
                                               'ester group'},
                                 {   'smiles': 'CCS(=O)(=O)N1CC2(C1)[C@@H]([C@@H](N2C(=O)C3CCCC3)CO)C4=CC=C(C=C4)C=CC',
                                     'name': 'LSM-38092',
                                     'reason': 'Contains an amide, not a '
                                               'carbamate'},
                                 {   'smiles': 'O=C/1N/C(/C(=O)N\\C1=C\\C2=CC=CC=C2)=C\\C=3N=CNC3C(C=C)(C)C',
                                     'name': 'DeltaPLH',
                                     'reason': 'Does not contain a carbamate '
                                               'ester group'},
                                 {   'smiles': 'C1CCN(CC1)C(=O)C[C@H]2C[C@@H]3[C@H]([C@@H](O2)CO)OC4=C3C=C(C=C4)NC(=O)CC5CC5',
                                     'name': 'N-[(1S,3R,4aS,9aR)-1-(hydroxymethyl)-3-[2-oxo-2-(1-piperidinyl)ethyl]-3,4,4a,9a-tetrahydro-1H-pyrano[3,4-b]benzofuran-6-yl]-2-cyclopropylacetamide',
                                     'reason': 'Contains an amide, not a '
                                               'carbamate'},
                                 {   'smiles': 'C[C@H]1C[C@@]2(OC(=O)c3ccccc3)[C@H]([C@H]1OC(C)=O)[C@@H](O)\\C(C)=C/C[C@H]1[C@@H](\\C=C(C)\\C2=O)C1(C)C',
                                     'name': '(-)-(6Z,12E,2S,3S,4R,5R,9S,11S,15R)-3-acetoxy-15-benzoyloxylathyra-6,12-dien-5-ol-14-one',
                                     'reason': 'Does not contain a carbamate '
                                               'ester group'},
                                 {   'smiles': 'O=C1C(O)=CC=2O[C@]3([C@H](O)C[C@@H]4[C@](OC=5C=C(O)C(C=C(C5C4)C)=O)(CC=CC(C[C@H]3CC2C(=C1)C)(C)C)C)C',
                                     'name': 'Eupenifeldin',
                                     'reason': 'Does not contain a carbamate '
                                               'ester group'},
                                 {   'smiles': 'O1[C@@H](O[C@@H]2[C@@H](OC[C@H]3O[C@@H](O[C@H]4[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]4CO)O[C@H]5[C@H](O)[C@@H](NC(=O)C)C(O[C@@H]5CO[C@@H]6O[C@H]([C@@H](O)[C@@H](O)[C@@H]6O)C)O)[C@@H](O)[C@@H](O[C@H]7O[C@@H]([C@@H](O)[C@H](O)[C@@H]7O[C@@H]8O[C@@H]([C@@H](O[C@@H]9O[C@@H]([C@H](O)[C@H](O)[C@H]9NC(=O)C)CO)[C@H](O)[C@H]8NC(=O)C)CO)CO)[C@@H]3O)O[C@@H]([C@@H](O)[C@@H]2O)CO)[C@H](NC(=O)C)[C@@H](O[C@@H]%10O[C@H]([C@@H](O)[C@@H](O)[C@@H]%10O)C)[C@H](O[C@@H]%11O[C@@H]([C@H](O)[C@H](O)[C@H]%11NC(=O)C)CO)[C@H]1CO',
                                     'name': 'N-[(3R,4R,5S,6R)-5-[(2S,3R,4R,5S,6R)-3-Acetamido-5-[(2S,3S,4S,5R,6R)-4-[(2R,3S,4S,5S,6R)-3-[(2S,3R,4R,5S,6R)-3-acetamido-5-[(2S,3R,4R,5R,6R)-3-acetamido-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-6-[[(2S,3S,4S,5S,6R)-3-[(2S,3R,4R,5S,6R)-3-acetamido-5-[(2S,3R,4R,5R,6R)-3-acetamido-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-6-(hydroxymethyl)-4-[(2R,3S,4R,5S,6S)-3,4,5-trihydroxy-6-methyloxan-2-yl]oxyoxan-2-yl]oxy-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxymethyl]-3,5-dihydroxyoxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-2,4-dihydroxy-6-[[(2R,3S,4R,5S,6S)-3,4,5-trihydroxy-6-methyloxan-2-yl]oxymethyl]oxan-3-yl]acetamide',
                                     'reason': 'Contains an amide, not a '
                                               'carbamate'},
                                 {   'smiles': 'CN1C[C@@H]2C[C@H](Cn3c2cccc3=O)[C@H]1CC=C',
                                     'name': 'Tinctorine',
                                     'reason': 'Does not contain a carbamate '
                                               'ester group'},
                                 {   'smiles': 'CCC1=C2COC(CC2=C3C(=C(OC3=N1)C(=O)C4=CC=CC=C4)N)(C)C',
                                     'name': 'LSM-4563',
                                     'reason': 'Does not contain a carbamate '
                                               'ester group'},
                                 {   'smiles': 'CN1CCN(CC1)C(=O)C[C@@H]2CC[C@H]3[C@H](O2)COC[C@@H](CN3C(=O)NC4=CC5=C(C=C4)OCO5)O',
                                     'name': '(3R,6aS,8S,10aS)-N-(1,3-benzodioxol-5-yl)-3-hydroxy-8-[2-(4-methyl-1-piperazinyl)-2-oxoethyl]-3,4,6,6a,8,9,10,10a-octahydro-2H-pyrano[2,3-c][1,5]oxazocine-1-carboxamide',
                                     'reason': 'Contains an amide, not a '
                                               'carbamate'}],
    'sample_false_negatives': [   {   'smiles': 'C=1(C=CC([N+](=O)[O-])=CC1)OC([C@@H](NC(OC(C)(C)C)=O)CC(N)=O)=O',
                                      'name': 'Boc-Asn-OPhNO2',
                                      'reason': 'Contains an amide, not a '
                                                'carbamate'},
                                  {   'smiles': '[H][C@]12N\\C(N[C@]1([H])C(=O)NC[C@H]2O)=N/[C@@H]1O[C@H](CO)[C@H](OC(N)=O)[C@@H](O)[C@H]1NC(=O)C[C@@H](N)CCCN',
                                      'name': 'streptothricin F',
                                      'reason': 'Contains an amide, not a '
                                                'carbamate'},
                                  {   'smiles': 'COC(=O)CC(NC(=O)C(NC(=O)OC(C)C)C(C)C)c1ccc(Cl)cc1',
                                      'name': 'methyl '
                                              '3-(4-chlorophenyl)-3-{[N-(isopropoxycarbonyl)valyl]amino}propanoate',
                                      'reason': 'Contains an amide, not a '
                                                'carbamate'},
                                  {   'smiles': 'OCn1c2ccc(Cl)cc2oc1=O',
                                      'name': '6-chloro-3-(hydroxymethyl)benzoxazolin-2-one',
                                      'reason': 'Does not contain a carbamate '
                                                'ester group'},
                                  {   'smiles': 'CO[C@@H]1\\C=C\\C=C(C)\\Cc2cc(OC)c(Cl)c(c2)N(C)C(=O)C[C@H](OC(=O)[C@H](C)N(C)C(C)=O)[C@]2(C)O[C@H]2[C@H](C)[C@@H]2C[C@@]1(O)NC(=O)O2',
                                      'name': 'maytansine',
                                      'reason': 'Contains an amide, not a '
                                                'carbamate'},
                                  {   'smiles': 'N1(C(O[C@@H]([C@@H]1C)C2=CC(=CC(=C2)C(F)(F)F)C(F)(F)F)=O)C(=O)CC=3C4=C(C=CC=C4)C=CC3',
                                      'name': 'tarocin A',
                                      'reason': 'Contains an amide, not a '
                                                'carbamate'},
                                  {   'smiles': 'CCOC(=O)N(C)C(=O)CSP(=S)(OCC)OCC',
                                      'name': 'mecarbam',
                                      'reason': 'Contains an amide, not a '
                                                'carbamate'},
                                  {   'smiles': 'CC(C)OC(=O)N[C@@H](C(C)C)C(=O)N[C@H](C)c1nc2ccc(F)cc2s1',
                                      'name': 'benthiavalicarb-isopropyl',
                                      'reason': 'Contains an amide, not a '
                                                'carbamate'},
                                  {   'smiles': 'CON=C(C1=CC=CO1)C(=O)NC2C3N(C2=O)C(=C(CS3)COC(=O)N)C(=O)O',
                                      'name': '3-(carbamoyloxymethyl)-7-[[2-(2-furanyl)-2-methoxyimino-1-oxoethyl]amino]-8-oxo-5-thia-1-azabicyclo[4.2.0]oct-2-ene-2-carboxylic '
                                              'acid',
                                      'reason': 'Contains an amide, not a '
                                                'carbamate'},
                                  {   'smiles': 'COC(=O)[C@H](NC(=O)[C@H](NC(=O)OC(C)(C)C)c1cc(Cl)c(O)c(Cl)c1)c1cc(I)c(O)c(I)c1',
                                      'name': 'N-Boc-D-4-HO-3,5-Cl2-PhGly-D-4-HO-3,5-I2-PhGly-OMe',
                                      'reason': 'Contains an amide, not a '
                                                'carbamate'}],
    'attempt': 2,
    'reasoning': "Okay, let's analyze the previous attempt and the reported "
                 'errors.\n'
                 '\n'
                 '**Reasoning:**\n'
                 '\n'
                 'The core issue seems to be that the previous code '
                 'incorrectly identified *amides* as carbamate esters and '
                 'vice-versa. This likely stems from the fact that both amides '
                 'and carbamates share the -N-C(=O)- motif. The previous '
                 "attempt tried to exclude amides but didn't do it correctly; "
                 'it only checked for amides if the carbon was bound to an '
                 'oxygen that was in the substructure match. Additionally, the '
                 'previous code did not check the whole molecule after finding '
                 'one carbamate group, which is not a problem because we only '
                 'need one carbamate group to be present to classify a '
                 'molecule as a carbamate ester.\n'
                 '\n'
                 'The problem is that amides have the N-C(=O)-C motif while '
                 'carbamate esters have N-C(=O)-O. The previous code is '
                 'missing the carbon after the carbonyl in the amide pattern, '
                 'that is why it thinks that amides are carbamates and does '
                 'not detect them properly. The exclusion of ring nitrogens '
                 'from the carbamate pattern is not necessary, as I realized '
                 'that I can use the SMARTS "[N]-C(=O)-[O]" which should catch '
                 'both cyclic and non-cyclic carbamates.\n'
                 '\n'
                 'Therefore, the solution is to change the SMARTS pattern for '
                 'amides to `[N]-C(=O)-[C]`, so it correctly detects amides, '
                 'and to check for them before checking for carbamates. Also, '
                 'the amide check must be done differently by searching for '
                 '[N]-C(=O)-C.\n'
                 '\n'
                 '**Revised Strategy:**\n'
                 '1.  **Parse SMILES:** Convert the SMILES string to an RDKit '
                 'molecule object.\n'
                 '2.  **Check for Amides:** Search the molecule for the '
                 'presence of an amide group using the SMARTS `[N]-C(=O)-[C]`. '
                 "If found, it's NOT a carbamate, and we return `False`.\n"
                 '3.  **Check for Carbamate Esters:** If no amides are found, '
                 'Search for a carbamate ester using SMARTS pattern '
                 '`[N]-C(=O)-[O]`.\n'
                 '4.  **Return Result:** If the carbamate ester pattern is '
                 'found, return `True` with a positive reason, otherwise, '
                 '`False` with a negative reason.',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 191,
    'num_false_positives': 563,
    'num_true_negatives': 141493,
    'num_false_negatives': 53,
    'num_negatives': None,
    'precision': 0.253315649867374,
    'recall': 0.7827868852459017,
    'f1': 0.38276553106212424,
    'accuracy': 0.995671117357695,
    'negative_predictive_value': 0.9996255634210787}