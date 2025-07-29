"""
Classifies: CHEBI:26848 tannin
"""
"""
Classifies: CHEBI:36354 tannin

A tannin is defined as any of a group of astringent polyphenolic vegetable principles or compounds,
chiefly complex glucosides of catechol and pyrogallol. Key features:
- Polyphenolic compounds
- Often contain glucose or gallic acid derivatives
- Multiple phenol/catechol/pyrogallol rings connected by ester or ether linkages
"""

from rdkit import Chem
from rdkit.Chem import AllChem

def is_tannin(smiles: str):
    """
    Determines if a molecule is a tannin based on its SMILES string.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a tannin, False otherwise
        str: Reason for classification
    """

    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Look for polyphenolic structure (multiple phenol/catechol/pyrogallol rings)
    phenol_pattern = Chem.MolFromSmarts("[c;H1]")  # Aromatic ring with 1 attached H
    catechol_pattern = Chem.MolFromSmarts("[c;H0;r5]1:c:c:c:c:c:1")  # Aromatic ring with 2 attached O
    pyrogallol_pattern = Chem.MolFromSmarts("[c;H0;r5]1:c:c(:O):c:c:c:1")  # Aromatic ring with 3 attached O

    phenol_matches = mol.GetSubstructMatches(phenol_pattern)
    catechol_matches = mol.GetSubstructMatches(catechol_pattern)
    pyrogallol_matches = mol.GetSubstructMatches(pyrogallol_pattern)

    if len(phenol_matches) + len(catechol_matches) + len(pyrogallol_matches) < 3:
        return False, "Fewer than 3 phenol/catechol/pyrogallol rings found"

    # Look for glucose or gallic acid derivatives
    glucose_pattern = Chem.MolFromSmarts("OC[C@H]1O[C@H]([C@H]([C@@H]([C@@H]1O)O)O)CO")
    gallic_pattern = Chem.MolFromSmarts("C(=O)c1cc(O)c(O)c(O)c1")

    glucose_matches = mol.GetSubstructMatches(glucose_pattern)
    gallic_matches = mol.GetSubstructMatches(gallic_pattern)

    if not glucose_matches and not gallic_matches:
        return False, "No glucose or gallic acid derivatives found"

    # Look for ester/ether linkages between rings
    ester_pattern = Chem.MolFromSmarts("[O;X2]-[CX3](=[OX1])")
    ether_pattern = Chem.MolFromSmarts("[O;X2]-[#6]")

    ester_matches = mol.GetSubstructMatches(ester_pattern)
    ether_matches = mol.GetSubstructMatches(ether_pattern)

    if not ester_matches and not ether_matches:
        return False, "No ester or ether linkages found between rings"

    return True, "Polyphenolic compound containing glucose/gallic acid derivatives and phenol/catechol/pyrogallol rings connected by ester/ether linkages"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:26848',
                          'name': 'tannin',
                          'definition': 'Any of a group of astringent '
                                        'polyphenolic vegetable principles or '
                                        'compounds, chiefly complex glucosides '
                                        'of catechol and pyrogallol.',
                          'parents': ['CHEBI:26195'],
                          'xrefs': ['Wikipedia:Tannin'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 36,
                           'log_lines_of_code': 3.58351893845611,
                           'indent_by_line': [   1,
                                                 1,
                                                 0,
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
                                                 1,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 0,
                                                 1,
                                                 2,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 0,
                                                 1,
                                                 1,
                                                 0,
                                                 1,
                                                 2,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 0,
                                                 1,
                                                 1,
                                                 0,
                                                 1,
                                                 2,
                                                 0,
                                                 1],
                           'max_indent': 2,
                           'imports': [   'from rdkit import Chem',
                                          'from rdkit.Chem import AllChem'],
                           'imports_count': 2,
                           'methods_called': [   'MolFromSmarts',
                                                 'MolFromSmiles',
                                                 'GetSubstructMatches'],
                           'methods_called_count': 3,
                           'smarts_strings': [   '[c;H1]',
                                                 '[O;X2]-[CX3](=[OX1])',
                                                 'OC[C@H]1O[C@H]([C@H]([C@@H]([C@@H]1O)O)O)CO',
                                                 '[O;X2]-[#6]',
                                                 '[c;H0;r5]1:c:c(:O):c:c:c:1',
                                                 'C(=O)c1cc(O)c(O)c(O)c1',
                                                 '[c;H0;r5]1:c:c:c:c:c:1'],
                           'smarts_strings_count': 7,
                           'defs': ['is_tannin(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "Fewer than 3 '
                                          'phenol/catechol/pyrogallol rings '
                                          'found"',
                                          'False, "No glucose or gallic acid '
                                          'derivatives found"',
                                          'False, "No ester or ether linkages '
                                          'found between rings"',
                                          'True, "Polyphenolic compound '
                                          'containing glucose/gallic acid '
                                          'derivatives and '
                                          'phenol/catechol/pyrogallol rings '
                                          'connected by ester/ether linkages"'],
                           'returns_count': 5,
                           'complexity': 2.9167037876912216},
    'message': None,
    'sample_true_negatives': [   {   'smiles': 'CN(C)CC1=CN(N=N1)CC[C@@H]2CC[C@H]([C@@H](O2)CO)NC(=O)NC3=CC4=C(C=C3)OCO4',
                                     'name': '1-(1,3-benzodioxol-5-yl)-3-[(2R,3R,6S)-6-[2-[4-[(dimethylamino)methyl]-1-triazolyl]ethyl]-2-(hydroxymethyl)-3-oxanyl]urea',
                                     'reason': 'No glucose or gallic acid '
                                               'derivatives found'},
                                 {   'smiles': 'C\\C(CO)=C/CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(CO)=C\\C[C@H]1OC(=O)C=C1CO',
                                     'name': 'Hippolide F',
                                     'reason': 'Fewer than 3 '
                                               'phenol/catechol/pyrogallol '
                                               'rings found'},
                                 {   'smiles': 'O([C@H]1[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]1CO)O[C@H]2[C@H](O)[C@@H](NC(=O)C)C(O[C@@H]2CO)O)[C@@H]3O[C@@H]([C@@H](O)[C@H](O[C@H]4O[C@@H]([C@@H](O)[C@H](O)[C@@H]4O)CO)[C@@H]3O)CO[C@H]5O[C@@H]([C@@H](O)[C@H](O[C@H]6O[C@@H]([C@@H](O)[C@H](O)[C@@H]6O[C@H]7O[C@@H]([C@@H](O)[C@H](O)[C@@H]7O)CO)CO)[C@@H]5O)CO[C@H]8O[C@@H]([C@@H](O)[C@H](O)[C@@H]8O)CO',
                                     'name': 'N-[(3R,4R,5S,6R)-5-[(2S,3R,4R,5S,6R)-3-Acetamido-5-[(2S,3S,4S,5R,6R)-6-[[(2S,3S,4S,5R,6R)-4-[(2R,3S,4S,5S,6R)-4,5-dihydroxy-6-(hydroxymethyl)-3-[(2S,3S,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-3,5-dihydroxy-6-[[(2S,3S,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxymethyl]oxan-2-yl]oxymethyl]-3,5-dihydroxy-4-[(2S,3S,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-2,4-dihydroxy-6-(hydroxymethyl)oxan-3-yl]acetamide',
                                     'reason': 'Fewer than 3 '
                                               'phenol/catechol/pyrogallol '
                                               'rings found'},
                                 {   'smiles': 'O=C1NCC(=O)N2CCC[C@H]2C(N[C@H]1CCC(=O)O)=O',
                                     'name': 'Cyclo-(glycyl-L-prolyl-L-glutamyl)',
                                     'reason': 'Fewer than 3 '
                                               'phenol/catechol/pyrogallol '
                                               'rings found'},
                                 {   'smiles': 'CC[C@@]1(O)C[C@H](O[C@H]2C[C@H]([NH3+])[C@H](O)[C@H](C)O2)c2c(O)c3C(=O)c4c(O)cccc4C(=O)c3c(O)c2[C@H]1C(=O)OC',
                                     'name': 'rhodomycin D(1+)',
                                     'reason': 'No glucose or gallic acid '
                                               'derivatives found'},
                                 {   'smiles': 'O[C@H]1[C@@H](O)[C@@H](O[C@@H]1COP(O)(O)=O)n1cc(F)c(=O)[nH]c1=O',
                                     'name': "5-fluorouridine 5'-monophosphate",
                                     'reason': 'Fewer than 3 '
                                               'phenol/catechol/pyrogallol '
                                               'rings found'},
                                 {   'smiles': 'CCC(=O)O[C@@H]1CC(=O)O[C@@H](CC=CC=C[C@@H]([C@@H](C[C@@H]([C@@H]([C@H]1OC)OC2C(C(C(C(O2)C)OC3CC(C(C(O3)C)OC(=O)CC)(C)O)N(C)C)O)CC=O)C)O)C',
                                     'name': 'propanoic acid '
                                             '[(4R,5S,6S,7R,9R,10R,16R)-6-[[4-(dimethylamino)-3-hydroxy-5-[[4-hydroxy-4,6-dimethyl-5-(1-oxopropoxy)-2-oxanyl]oxy]-6-methyl-2-oxanyl]oxy]-10-hydroxy-5-methoxy-9,16-dimethyl-2-oxo-7-(2-oxoethyl)-1-oxacyclohexadeca-11,13-dien-4-yl] '
                                             'ester',
                                     'reason': 'Fewer than 3 '
                                               'phenol/catechol/pyrogallol '
                                               'rings found'},
                                 {   'smiles': 'C[C@H]1CN([C@@H](COC2=C(C=C(C=C2)NC(=O)C3CC3)C(=O)N(C[C@H]1OC)C)C)C(=O)CN4CCOCC4',
                                     'name': 'N-[(4R,7S,8S)-8-methoxy-4,7,10-trimethyl-5-(2-morpholin-4-ylacetyl)-11-oxo-2-oxa-5,10-diazabicyclo[10.4.0]hexadeca-1(12),13,15-trien-14-yl]cyclopropanecarboxamide',
                                     'reason': 'No glucose or gallic acid '
                                               'derivatives found'},
                                 {   'smiles': 'COC1=CC=CC=C1CNC(=O)C[C@@H]2C[C@@H]3[C@H]([C@H](O2)CO)OC4=C3C=C(C=C4)NC(=O)NC5CCCC5',
                                     'name': '2-[(1R,3S,4aS,9aR)-6-[[(cyclopentylamino)-oxomethyl]amino]-1-(hydroxymethyl)-3,4,4a,9a-tetrahydro-1H-pyrano[3,4-b]benzofuran-3-yl]-N-[(2-methoxyphenyl)methyl]acetamide',
                                     'reason': 'No glucose or gallic acid '
                                               'derivatives found'},
                                 {   'smiles': 'O=C(N[C@@H](CC(=O)N)C(O)=O)[C@@H](NC(=O)[C@@H](N)CC=1C=2C(NC1)=CC=CC2)[C@H](CC)C',
                                     'name': 'Trp-Ile-Asn',
                                     'reason': 'No glucose or gallic acid '
                                               'derivatives found'}],
    'sample_false_negatives': [   {   'smiles': 'O[C@@H]1Cc2c(O)cc(O)c([C@@H]3[C@@H](O)[C@H](Oc4c3c(O)cc(O)c4[C@@H]3[C@@H](O)[C@H](Oc4c3c(O)cc(O)c4[C@@H]3[C@@H](O)[C@H](Oc4c([C@@H]5[C@@H](O)[C@H](Oc6c([C@@H]7[C@@H](O)[C@H](Oc8cc(O)cc(O)c78)c7ccc(O)c(O)c7)c(O)cc(O)c56)c5ccc(O)c(O)c5)c(O)cc(O)c34)c3ccc(O)c(O)c3)c3ccc(O)c(O)c3)c3ccc(O)c(O)c3)c2O[C@@H]1c1ccc(O)c(O)c1',
                                      'name': 'Cinnamtannin A4',
                                      'reason': 'No glucose or gallic acid '
                                                'derivatives found'},
                                  {   'smiles': 'O1C(C(O)C(OC(=O)C=2C=C(OC3OC(C(O)C(O)C3O)C(O)=O)C(O)=C(O)C2)C(O)C1O)CO',
                                      'name': '6-[2,3-dihydroxy-5-({[2,3,5-trihydroxy-6-(hydroxymethyl)oxan-4-yl]oxy}carbonyl)phenoxy]-3,4,5-trihydroxyoxane-2-carboxylic '
                                              'acid',
                                      'reason': 'Fewer than 3 '
                                                'phenol/catechol/pyrogallol '
                                                'rings found'},
                                  {   'smiles': 'O1C(C(O)C(O)C(O)C1OC=2C=C(C=CC2OC(=O)C3=CC=CC=C3)CC=C)C(O)=O',
                                      'name': '6-[2-(benzoyloxy)-5-(prop-2-en-1-yl)phenoxy]-3,4,5-trihydroxyoxane-2-carboxylic '
                                              'acid',
                                      'reason': 'No glucose or gallic acid '
                                                'derivatives found'},
                                  {   'smiles': 'O=C1OC2=C(O)C(O)=CC3=C2C4=C1C=C(O[C@@H]5O[C@@H]([C@@H](O)[C@@H]([C@H]5O)O)CO[C@@H]6O[C@@H]([C@@H](O)[C@@H]([C@H]6O)O)CO)C(=C4OC3=O)O',
                                      'name': 'Ellagic acid di-hexoside',
                                      'reason': 'Fewer than 3 '
                                                'phenol/catechol/pyrogallol '
                                                'rings found'},
                                  {   'smiles': 'O=C(OC1=CC(O)=C(C(=O)O)C(=C1)C)C2=C(O)C=C(O[C@@H]3O[C@H](C(=O)O)[C@@H](O)[C@@H]([C@H]3O)O)C=C2CCCCCCCCCCCCCCC',
                                      'name': 'CRM646-A',
                                      'reason': 'No glucose or gallic acid '
                                                'derivatives found'},
                                  {   'smiles': 'O=C(OC1=CC(O)=C(C(=O)N[C@H](C(=O)O)C)C(=C1)C)C2=C(O[C@H]3O[C@H]([C@H](O)[C@H]([C@@H]3O)O)CO)C=C(OC(=O)C4=C(O)C=C(OC)C=C4C)C=C2C',
                                      'name': 'Amidepsine G',
                                      'reason': 'No glucose or gallic acid '
                                                'derivatives found'},
                                  {   'smiles': 'O[C@@H]1Cc2c(O)cc(O)c([C@@H]3[C@@H](O)[C@H](Oc4c([C@@H]5[C@@H](O)[C@H](Oc6cc(O)cc(O)c56)c5ccc(O)c(O)c5)c(O)cc(O)c34)c3ccc(O)c(O)c3)c2O[C@@H]1c1ccc(O)c(O)c1',
                                      'name': 'procyanidin C1',
                                      'reason': 'No glucose or gallic acid '
                                                'derivatives found'},
                                  {   'smiles': 'COc1c(O)c2oc3ccccc3c(=O)c2c(c1OC)-c1c(OC)c(OC)c(O)c2oc3ccccc3c(=O)c12',
                                      'name': 'hyperidixanthone',
                                      'reason': 'No glucose or gallic acid '
                                                'derivatives found'},
                                  {   'smiles': 'O[C@@H]1Cc2c(O)cc(O)c([C@H]3[C@H](O)[C@H](Oc4cc(O)cc(O)c34)c3ccc(O)c(O)c3)c2O[C@@H]1c1cc(O)c(O)c(O)c1',
                                      'name': '(+)-catechin-(4alpha->8)-(-)-epigallocatechin',
                                      'reason': 'No glucose or gallic acid '
                                                'derivatives found'},
                                  {   'smiles': 'COc1cc2c3c(oc(=O)c4cc(O)c(OC)c(oc2=O)c34)c1OC',
                                      'name': "3,4,3'-Tri-O-methylellagic acid",
                                      'reason': 'Fewer than 3 '
                                                'phenol/catechol/pyrogallol '
                                                'rings found'}],
    'attempt': 0,
    'reasoning': "Here's a Python program to classify chemical entities as "
                 'tannins based on their SMILES strings:',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 54,
    'num_false_positives': 198,
    'num_true_negatives': 141933,
    'num_false_negatives': 115,
    'num_negatives': None,
    'precision': 0.21428571428571427,
    'recall': 0.31952662721893493,
    'f1': 0.2565320665083135,
    'accuracy': 0.9978004216444132,
    'negative_predictive_value': 0.999190414507772}