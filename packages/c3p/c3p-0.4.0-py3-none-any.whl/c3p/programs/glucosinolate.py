"""
Classifies: CHEBI:24279 glucosinolate
"""
from rdkit import Chem

def is_glucosinolate(smiles: str):
    """
    Determines if a molecule is a glucosinolate based on its SMILES string.
    Glucosinolates are defined by a central C atom bonded to a glycone group via S,
    a sulfonated oxime group via N, and a side-group.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a glucosinolate, False otherwise
        str: Reason for classification
    """

    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Dynamic SMARTS for glycone group (consider stereochemistry flexibly)
    glycone_pattern = Chem.MolFromSmarts("S[C@@H]1O[C@H](CO)[C@H](O)[C@H](O)[C@@H]1O |flex|")
    if not mol.HasSubstructMatch(glycone_pattern):
        return False, "No thioglucoside group found"

    # Pattern for N-sulfooxy group, where N is doubly bonded to central C
    sulfonated_oxime_pattern = Chem.MolFromSmarts("[CX3](=N\\O[S](=O)(=O)[O-])~*")
    if not mol.HasSubstructMatch(sulfonated_oxime_pattern):
        return False, "No sulfonated oxime group connected"

    # Ensure central carbon connectivity accounting for flexibility
    # Central carbon should have both the S-bonded thioglucoside and N-bonded oxime
    central_c_pattern = Chem.MolFromSmarts("[CX3](S)(=N\\O[S](=O)(=O)[O-])~[*]")
    if not mol.HasSubstructMatch(central_c_pattern):
        return False, "Central carbon with required connectivity not found"

    return True, "Molecule contains the defining features of glucosinolate"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:24279',
                          'name': 'glucosinolate',
                          'definition': 'Water-soluble anionic substituted '
                                        'thioglucosides. Glucosinolates have a '
                                        'central C atom which is bonded via an '
                                        'S atom to a glycone group and via an '
                                        'N atom to a sulfonated oxime group, '
                                        'and which also carries a side-group. '
                                        'The side-chain and sulfate group have '
                                        'an anti stereochemical configuration '
                                        'across the C=N double bond.',
                          'parents': ['CHEBI:24401'],
                          'xrefs': [   'KEGG:C17260',
                                       'PMID:17139450',
                                       'PMID:17461791',
                                       'PMID:22405332',
                                       'Wikipedia:Glucosinolate'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': None,
    'message': '\n'
               'Attempt failed: F1 score of 0 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: NONE\n'
               'False positives: NONE\n'
               'False negatives: SMILES: '
               '[C@H]1(O[C@@H]([C@@H](O)[C@@H]([C@H]1O)O)CO)S/C(=N\\OS([O-])(=O)=O)/CCCCS(C)=O '
               'NAME: glucoraphanin(1-) REASON: MISSED Central carbon with '
               'required connectivity not found\n'
               ' * SMILES: '
               'OC[C@H]1O[C@@H](SC(Cc2c[nH]c3ccccc23)=NOS([O-])(=O)=O)[C@H](O)[C@@H](O)[C@@H]1O '
               'NAME: glucobrassicin(1-) REASON: MISSED Central carbon with '
               'required connectivity not found\n'
               ' * SMILES: '
               'COc1cccc2[nH]cc(CC(S[C@@H]3O[C@H](CO)[C@@H](O)[C@H](O)[C@H]3O)=NOS([O-])(=O)=O)c12 '
               'NAME: 4-methoxyglucobrassicin(1-) REASON: MISSED Central '
               'carbon with required connectivity not found\n'
               ' * SMILES: '
               '[C@H]1(O[C@@H]([C@@H](O)[C@@H]([C@H]1O)O)CO)S/C(=N\\OS([O-])(=O)=O)/C(CC)C '
               'NAME: glucocochlearin(1-) REASON: MISSED Central carbon with '
               'required connectivity not found\n'
               ' * SMILES: S(C1OC(C(O)C(O)C1O)CO)\\C(=N\\OS(O)(=O)=O)\\CCCO '
               'NAME: 3-Hydroxypropyl-Glucosinolate REASON: MISSED No '
               'sulfonated oxime group connected\n'
               ' * SMILES: '
               'COn1cc(CC(S[C@@H]2O[C@H](CO)[C@@H](O)[C@H](O)[C@H]2O)=NOS([O-])(=O)=O)c2ccccc12 '
               'NAME: neoglucobrassicin(1-) REASON: MISSED Central carbon with '
               'required connectivity not found\n'
               ' * SMILES: '
               'S(C1OC(C(O)C(O)C1O)CO)C(=NOS(O)(=O)=O)CC=2C3=C(NC2)C=CC=C3OC '
               'NAME: [3,4,5-Trihydroxy-6-(hydroxymethyl)oxan-2-yl] '
               '2-(4-methoxy-1H-indol-3-yl)-N-sulfooxyethanimidothioate '
               'REASON: MISSED No sulfonated oxime group connected\n'
               ' * SMILES: '
               '[C@H]1(O[C@@H]([C@@H](O)[C@@H]([C@H]1O)O)CO)S/C(=N\\OS([O-])(=O)=O)/C[C@H](C=C)O '
               'NAME: (Z)-progoitrin(1-) REASON: MISSED Central carbon with '
               'required connectivity not found\n'
               ' * SMILES: '
               '[C@H]1(S/C(=N\\OS([O-])(=O)=O)/CC=2C3=CC=CC=C3NC2)[C@H](O)[C@H]([C@@H]([C@H](O1)CO)O)O '
               'NAME: (Z)-glucobrassicin(1-) REASON: MISSED Central carbon '
               'with required connectivity not found\n'
               ' * SMILES: '
               '[C@H]1(O[C@@H]([C@@H](O)[C@@H]([C@H]1O)O)CO)SC(=NOS([O-])(=O)=O)C[C@H](C=C)O '
               'NAME: progoitrin(1-) REASON: MISSED Central carbon with '
               'required connectivity not found\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'O=C1C2=C(OC(=C1)C)C3=C(OC)C=C(OC)C=C3C(=C2O)C4=C5OC(=CC(C5=C(O)C=6C4=CC(OC)=CC6OC)=O)C',
                                     'name': 'Isonigerone',
                                     'reason': 'No thioglucoside group found'},
                                 {   'smiles': 'CCCCCCCCCCCCCC(=O)OC[C@H](COP([O-])(=O)OC[C@@H](O)CO)OC(=O)CCCCCCC\\C=C/CCCCCCCC',
                                     'name': '1-myristoyl-2-oleoyl-sn-glycero-3-phosphatidylglycerol(1-)',
                                     'reason': 'No thioglucoside group found'},
                                 {   'smiles': 'C(=C\\C/C=C\\CCCC(NC)=O)\\C/C=C\\C/C=C\\CCCCC',
                                     'name': 'N-methyl arachidonoyl amine',
                                     'reason': 'No thioglucoside group found'},
                                 {   'smiles': 'OC1(O)[C@]23N(CC1)C(N(O)[C@H]([C@@]3(N=C(N2)N)[H])CO)=N',
                                     'name': 'Decarbamoylneosaxitoxin',
                                     'reason': 'No thioglucoside group found'},
                                 {   'smiles': 'S([C@H]1N(C(=O)/C(=C\\C2=CC=C(OCC=C(C)C)C=C2)/N(C1=O)C)C)C',
                                     'name': 'Fusaperazine F',
                                     'reason': 'No thioglucoside group found'},
                                 {   'smiles': 'Oc1ccccc1I',
                                     'name': '2-iodophenol',
                                     'reason': 'No thioglucoside group found'},
                                 {   'smiles': 'O=C1N(CC(=O)N[C@H](C(=O)O[C@H]([C@@H](C(NC(C=C1)=C)=O)C)C(CCCCCCCCCCCCCC)C)C(O)C(=O)N)C',
                                     'name': 'Rakicidin H',
                                     'reason': 'No thioglucoside group found'},
                                 {   'smiles': 'O(C1=C(OC)C=C(C2=C(O)C(OC)=C(C3=CC=CC=C3)C=C2OC)C=C1)C/C=C(/CO)\\C',
                                     'name': 'Prenylterphenyllin F',
                                     'reason': 'No thioglucoside group found'},
                                 {   'smiles': 'O1[C@@H]([C@@H](O)[C@H](O[C@@H]2O[C@@H]([C@@H](O)[C@H](O)[C@H]2O)CO)[C@@H](O)[C@@H]1OC[C@H]3O[C@@H](OC[C@H]4O[C@@H](O)[C@H](O)[C@@H](O)[C@@H]4O)[C@H](O)[C@@H](O)[C@@H]3O)CO[C@@H]5O[C@@H]([C@@H](O)[C@H](O[C@@H]6O[C@@H]([C@@H](O)[C@H](O)[C@H]6O)CO)[C@H]5O)CO[C@@H]7O[C@@H]([C@@H](O)[C@H](O)[C@H]7O)CO',
                                     'name': '(2R,3R,4S,5S,6R)-6-[[(2R,3R,4S,5S,6R)-6-[[(2R,3R,4S,5R,6R)-6-[[(2R,3R,4S,5R,6R)-3,5-Dihydroxy-4-[(2R,3R,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-6-[[(2R,3R,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxymethyl]oxan-2-yl]oxymethyl]-3,5-dihydroxy-4-[(2R,3R,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxymethyl]-3,4,5-trihydroxyoxan-2-yl]oxymethyl]oxane-2,3,4,5-tetrol',
                                     'reason': 'No thioglucoside group found'},
                                 {   'smiles': 'O([C@H]1[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]1CO)O[C@H]2[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]2CO[C@@H]3O[C@H]([C@@H](O)[C@@H](O)[C@@H]3O)C)O)[C@@H]4O[C@@H]([C@@H](O)[C@H](O[C@H]5O[C@@H]([C@@H](O)[C@H](O)[C@@H]5O[C@@H]6O[C@@H]([C@@H](O[C@@H]7O[C@@H]([C@H](O)[C@H](O)[C@H]7O)CO)[C@H](O)[C@@H]6NC(=O)C)CO)CO)[C@@H]4O)CO[C@H]8O[C@@H]([C@@H](O)[C@H](O)[C@@H]8O[C@@H]9O[C@@H]([C@@H](O[C@@H]%10O[C@@H]([C@H](O)[C@H](O)[C@H]%10O)CO)[C@H](O)[C@H]9NC(=O)C)CO)CO',
                                     'name': 'Gal2GlcNAc2Man3GlcNAcFucGlcNAc',
                                     'reason': 'No thioglucoside group found'}],
    'sample_false_negatives': [   {   'smiles': 'S(C1OC(C(O)C(O)C1O)CO)\\C(=N\\OS(O)(=O)=O)\\CCCO',
                                      'name': '3-Hydroxypropyl-Glucosinolate',
                                      'reason': 'No sulfonated oxime group '
                                                'connected'},
                                  {   'smiles': 'S(C1OC(C(O)C(O)C1O)CO)C(=NOS(O)(=O)=O)CC=2C3=C(NC2)C=CC=C3OC',
                                      'name': '[3,4,5-Trihydroxy-6-(hydroxymethyl)oxan-2-yl] '
                                              '2-(4-methoxy-1H-indol-3-yl)-N-sulfooxyethanimidothioate',
                                      'reason': 'No sulfonated oxime group '
                                                'connected'},
                                  {   'smiles': 'S(C1OC(C(O)C(O)C1O)CO)\\C(=N\\OS(O)(=O)=O)\\CC(O)(CC)C',
                                      'name': '{[(e)-(3-hydroxy-3-methyl-1-{[3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]sulfanyl}pentylidene)amino]oxy}sulfonic '
                                              'acid',
                                      'reason': 'No sulfonated oxime group '
                                                'connected'},
                                  {   'smiles': 'S(C1OC(C(O)C(O)C1O)CO)\\C(=N\\OS(O)(=O)=O)\\CCC=C',
                                      'name': '{[(e)-(1-{[3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]sulfanyl}pent-4-en-1-ylidene)amino]oxy}sulfonic '
                                              'acid',
                                      'reason': 'No sulfonated oxime group '
                                                'connected'},
                                  {   'smiles': 'S(C1OC(C(O)C(O)C1O)CO)\\C(=N\\OS(O)(=O)=O)\\CCSC',
                                      'name': '2-(Methylthio)ethyl '
                                              'glucosinolate',
                                      'reason': 'No sulfonated oxime group '
                                                'connected'},
                                  {   'smiles': 'CSCCCCCCCC(S[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O)=NOS(O)(=O)=O',
                                      'name': '7-Methylthioheptyl '
                                              'glucosinolate',
                                      'reason': 'No sulfonated oxime group '
                                                'connected'},
                                  {   'smiles': 'S(C1OC(C(O)C(O)C1O)CO)\\C(=N\\OS(O)(=O)=O)\\CC2=CC=C(OC3OC(C(OC(=O)C)C(O)C3O)C)C=C2',
                                      'name': '{[(e)-[2-(4-{[5-(acetyloxy)-3,4-dihydroxy-6-methyloxan-2-yl]oxy}phenyl)-1-{[3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]sulfanyl}ethylidene]amino]oxy}sulfonic '
                                              'acid',
                                      'reason': 'No sulfonated oxime group '
                                                'connected'},
                                  {   'smiles': 'S(C1OC(C(O)C(O)C1O)CO)\\C(=N\\OS(O)(=O)=O)\\CCC(CC)C',
                                      'name': '3-Methylpentyl glucosinolate',
                                      'reason': 'No sulfonated oxime group '
                                                'connected'},
                                  {   'smiles': 'S(C1OC(C(O)C(O)C1O)CO)\\C(=N\\OS(O)(=O)=O)\\CCC2=CC=CC=C2',
                                      'name': 'Phenethyl glucosinolate',
                                      'reason': 'No sulfonated oxime group '
                                                'connected'},
                                  {   'smiles': 'S(C1OC(C(O)C(O)C1O)CO)\\C(=N\\OS(O)(=O)=O)\\CCCCC2=CC=CC=C2',
                                      'name': '4-Phenylbutyl glucosinolate',
                                      'reason': 'No sulfonated oxime group '
                                                'connected'}],
    'attempt': 2,
    'reasoning': 'The previous code attempted to classify glucosinolates based '
                 'on their defining structural features but failed due to '
                 'incorrect or incomplete pattern identification, which led to '
                 'poor F1 scores and false negatives. \n'
                 '\n'
                 "Upon analyzing the outcomes and the previous code, it's "
                 'evident that:\n'
                 '1. The glycone pattern (thioglucoside group) pattern '
                 'matching is not flexible enough to capture variations.\n'
                 '2. The sulfonated oxime group identification might be '
                 'inaccurate or not flexible enough, as glucosinolates can '
                 'exhibit various conformations and stereochemistries.\n'
                 '3. The central carbon connectivity check might miss diverse '
                 'glucosinolate structures due to an overly specific SMARTS '
                 'pattern.\n'
                 '\n'
                 'To improve, we should:\n'
                 '- Extend pattern matching to account for stereochemistry '
                 'variations in thioglucoside groups.\n'
                 '- Verify the presence of the sulfonated oxime group with '
                 'slightly more relaxed or alternative SMARTS patterns.\n'
                 '- Ensure the central carbon has the correct key bonds, but '
                 'relax strict pattern matching to account for side chains and '
                 'stereochemistry.\n'
                 '- Ensure all patterns correctly align with how '
                 'glucosinolates are typically represented in their SMILES '
                 'format.\n'
                 '\n'
                 "Here's the revised code:",
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 31,
    'num_false_positives': 3,
    'num_true_negatives': 142245,
    'num_false_negatives': 21,
    'num_negatives': None,
    'precision': 0.9117647058823529,
    'recall': 0.5961538461538461,
    'f1': 0.7209302325581395,
    'accuracy': 0.9998313422347154,
    'negative_predictive_value': 0.9998523891864536}