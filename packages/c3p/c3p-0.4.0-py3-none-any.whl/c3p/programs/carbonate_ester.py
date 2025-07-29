"""
Classifies: CHEBI:46722 carbonate ester
"""
from rdkit import Chem

def is_carbonate_ester(smiles: str):
    """
    Determines if a molecule is a carbonate ester based on its SMILES string.
    A carbonate ester has the functional group O=C(O-)O- attached to organic groups.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if the molecule is a carbonate ester, False otherwise
        str: Reason for classification
    """
    
    # Parse SMILES to get molecule
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Define the SMARTS pattern for a carbonate ester: R-O-C(=O)-O-R'
    carbonate_ester_pattern = Chem.MolFromSmarts("[$([#6;!H0]),$([#1])]OC(=O)O[$([#6;!H0]),$([#1])]")
    
    # Check if the molecule matches the carbonate ester pattern
    if mol.HasSubstructMatch(carbonate_ester_pattern):
        return True, "Contains carbonate ester functional group"
    else:
        return False, "No carbonate ester functional group found"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:46722',
                          'name': 'carbonate ester',
                          'definition': 'Any carbonate that is carbonic acid '
                                        'in which the hydrogens have been '
                                        'replaced by organyl groups.',
                          'parents': ['CHEBI:23016', 'CHEBI:33308'],
                          'xrefs': ['Wikipedia:Carbonate_ester'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': None,
    'message': None,
    'sample_true_negatives': [   {   'smiles': 'C[C@@]12C[C@H]3OC(=O)C(=C)[C@H]3C[C@H]1C(=C)C[C@H](O)C2',
                                     'name': 'Ivalin',
                                     'reason': 'No carbonate ester functional '
                                               'group found'},
                                 {   'smiles': 'C[C@@H]1CN(C(=O)CCCN2C(=CN=N2)CO[C@@H]1CN(C)C(=O)C3=CC4=C(C=C3)C=CN4C)[C@H](C)CO',
                                     'name': 'N-[[(8R,9S)-6-[(2R)-1-hydroxypropan-2-yl]-8-methyl-5-oxo-10-oxa-1,6,14,15-tetrazabicyclo[10.3.0]pentadeca-12,14-dien-9-yl]methyl]-N,1-dimethyl-6-indolecarboxamide',
                                     'reason': 'No carbonate ester functional '
                                               'group found'},
                                 {   'smiles': 'O=C1O[C@H](O)[C@@H]2[C@]13[C@@H](O)[C@@H](OC(=O)[C@H](O)CCCCCCCC)CC([C@@H]3CC=C2C=O)(C)C',
                                     'name': 'Mniopetal B',
                                     'reason': 'No carbonate ester functional '
                                               'group found'},
                                 {   'smiles': 'Oc1ccc(CC2NCCc3cc(O)c(O)cc23)cc1O',
                                     'name': 'norlaudanosoline',
                                     'reason': 'No carbonate ester functional '
                                               'group found'},
                                 {   'smiles': 'O=C(C(C)(C)C(=O)C=CC1=CC(OC)=C(OC)C=C1)C=CC2=CC(OC)=C(OC)C=C2',
                                     'name': '1,7-bis(3,4-dimethoxy '
                                             'phenyl)-4,4-dimethyl-1,6-heptadiene-3,5-dione',
                                     'reason': 'No carbonate ester functional '
                                               'group found'},
                                 {   'smiles': 'O[C@@H]1C=CC=C(CCC([O-])=O)[C@@H]1O',
                                     'name': '3-[(5R,6S)-5,6-dihydroxycyclohexa-1,3-dienyl]propanoate',
                                     'reason': 'No carbonate ester functional '
                                               'group found'},
                                 {   'smiles': 'C[C@H]1CN(S(=O)(=O)C2=C(C=C(C=C2)C#CC3(CCCC3)O)O[C@H]1CN(C)C(=O)CC4=CC=NC=C4)[C@@H](C)CO',
                                     'name': 'N-[[(4S,5R)-8-[2-(1-hydroxycyclopentyl)ethynyl]-2-[(2S)-1-hydroxypropan-2-yl]-4-methyl-1,1-dioxo-4,5-dihydro-3H-6,1$l^{6},2-benzoxathiazocin-5-yl]methyl]-N-methyl-2-pyridin-4-ylacetamide',
                                     'reason': 'No carbonate ester functional '
                                               'group found'},
                                 {   'smiles': 'C[C@H]1CCCCO[C@H]([C@@H](CN(C(=O)C2=C(O1)C=CC(=C2)N(C)C)[C@H](C)CO)C)CN(C)CC3=CC=C(C=C3)C(=O)O',
                                     'name': '4-[[[(3S,9R,10R)-16-(dimethylamino)-12-[(2R)-1-hydroxypropan-2-yl]-3,10-dimethyl-13-oxo-2,8-dioxa-12-azabicyclo[12.4.0]octadeca-1(14),15,17-trien-9-yl]methyl-methylamino]methyl]benzoic '
                                             'acid',
                                     'reason': 'No carbonate ester functional '
                                               'group found'},
                                 {   'smiles': 'Cl/C=C/C(C#C)(C1O[C@H](C(=O)O)[C@@H](O)[C@@H]([C@H]1O)O)CC',
                                     'name': '(2R,3R,4S,5S)-6-[(1E)-1-chloro-3-ethylpent-1-en-4-yn-3-yl]-3,4,5-trihydroxyoxane-2-carboxylic '
                                             'acid',
                                     'reason': 'No carbonate ester functional '
                                               'group found'},
                                 {   'smiles': 'SC[C@H](N)C(=O)N[C@@H](C(C)C)C(=O)N[C@@H](CO)C(O)=O',
                                     'name': 'Cys-Val-Ser',
                                     'reason': 'No carbonate ester functional '
                                               'group found'}],
    'sample_false_negatives': [   {   'smiles': 'CCOC(O)=O',
                                      'name': 'monoethyl carbonate',
                                      'reason': 'No carbonate ester functional '
                                                'group found'},
                                  {   'smiles': 'CCOc1nc2cccc(C(=O)OCc3oc(=O)oc3C)c2n1Cc1ccc(cc1)-c1ccccc1-c1noc(=O)[nH]1',
                                      'name': 'azilsartan medoxomil',
                                      'reason': 'No carbonate ester functional '
                                                'group found'},
                                  {   'smiles': 'CCOC(=O)OC1=C(C(=O)N(C)C11CCN(CC1)OC)C1=C(C)C=C(Cl)C=C1C',
                                      'name': 'spiropidion',
                                      'reason': 'No carbonate ester functional '
                                                'group found'},
                                  {   'smiles': '[H][C@]12[C@H](CC3=CC=CC=C3)NC(=O)[C@]11OC(=O)O\\C=C\\[C@H](C)C(=O)[C@@H](C)C\\C=C\\[C@H]1C=C(C)[C@H]2C',
                                      'name': 'cytochalasin Z16',
                                      'reason': 'No carbonate ester functional '
                                                'group found'},
                                  {   'smiles': 'O=C1OC(=O)C=CO1',
                                      'name': 'Pleurone',
                                      'reason': 'No carbonate ester functional '
                                                'group found'},
                                  {   'smiles': 'CC(C)(C)C(=O)OCOP(=O)(COCCN1C=NC2=C1N=CN=C2N)OCOC(=O)C(C)(C)C',
                                      'name': 'adefovir pivoxil',
                                      'reason': 'No carbonate ester functional '
                                                'group found'},
                                  {   'smiles': '[H]C1(COC(O)=O)c2ccccc2-c2ccccc12',
                                      'name': 'fluoren-9-ylmethyl hydrogen '
                                              'carbonate',
                                      'reason': 'No carbonate ester functional '
                                                'group found'},
                                  {   'smiles': 'CCCC(=C(C(=C(C(=C(CCC1=CC=C(O1)OC(=O)O)[H])[H])[H])[H])[H])[H]',
                                      'name': '5-(undeca-3,5,7-trien-1-yl)-2-furyl '
                                              'hydrogen carbonate',
                                      'reason': 'No carbonate ester functional '
                                                'group found'},
                                  {   'smiles': 'O=C(Oc1ccccc1)Oc1ccccc1',
                                      'name': 'diphenyl carbonate',
                                      'reason': 'No carbonate ester functional '
                                                'group found'}],
    'attempt': 0,
    'reasoning': 'To classify chemical entities as "carbonate esters," we need '
                 'to identify specific structural features in the SMILES '
                 'string that indicate the presence of carbonate ester groups. '
                 'A carbonate ester is characterized by the presence of a '
                 'carbonic acid derivative where the hydrogens are replaced '
                 'with organic groups. The core structure is typically '
                 'represented by the functional group pattern '
                 "`R-O-C(=O)-O-R'`, where `R` and `R'` can be any organic "
                 'groups.\n'
                 '\n'
                 'Steps:\n'
                 '1. Parse the SMILES string to generate a molecule object.\n'
                 '2. Search for the specific structural pattern characteristic '
                 'of carbonate esters.\n'
                 '3. Return True if the pattern exists, indicating the '
                 'presence of a carbonate ester, or return False with an '
                 'explanation if it does not.\n'
                 '\n'
                 "Let's define this program:",
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 15,
    'num_false_positives': 27,
    'num_true_negatives': 142249,
    'num_false_negatives': 9,
    'num_negatives': None,
    'precision': 0.35714285714285715,
    'recall': 0.625,
    'f1': 0.45454545454545453,
    'accuracy': 0.999747013352073,
    'negative_predictive_value': 0.9999367346651858}