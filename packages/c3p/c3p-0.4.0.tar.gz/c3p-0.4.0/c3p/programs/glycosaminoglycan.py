"""
Classifies: CHEBI:18085 glycosaminoglycan
"""
from rdkit import Chem

def is_glycosaminoglycan(smiles: str):
    """
    Determines if a molecule is a glycosaminoglycan based on its SMILES string.
    A GAG is characterized by having repeating aminomonosaccharide units.
    
    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a glycosaminoglycan, False otherwise
        str: Reason for classification
    """
    
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Defining a pattern for an amino sugar, common in GAGs
    aminomonosaccharide_pattern = Chem.MolFromSmarts("[OX2][CX4][NX3]")
    
    # Check if pattern exists in the molecule
    if mol.HasSubstructMatch(aminomonosaccharide_pattern):
        return True, "Contains aminomonosaccharide units characteristic of GAGs"
    
    return False, "Does not contain recognizable glycosaminoglycan features"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:18085',
                          'name': 'glycosaminoglycan',
                          'definition': 'Any polysaccharide containing a '
                                        'substantial proportion of '
                                        'aminomonosaccharide residues.',
                          'parents': ['CHEBI:22506'],
                          'xrefs': [   'KEGG:C02545',
                                       'Wikipedia:Glycosaminoglycan'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 19,
                           'log_lines_of_code': 2.9444389791664403,
                           'indent_by_line': [   1,
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
                                                 0,
                                                 1,
                                                 1,
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
                           'smarts_strings': ['[OX2][CX4][NX3]'],
                           'smarts_strings_count': 1,
                           'defs': ['is_glycosaminoglycan(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'True, "Contains aminomonosaccharide '
                                          'units characteristic of GAGs"',
                                          'False, "Does not contain '
                                          'recognizable glycosaminoglycan '
                                          'features"'],
                           'returns_count': 3,
                           'complexity': 2.388887795833288},
    'message': None,
    'sample_true_negatives': [   {   'smiles': 'O1[C@H]([C@@H](O)CC=2C1=CC=CC2)C3=CC=CC=C3',
                                     'name': 'cis-(+)-3-Flavanol',
                                     'reason': 'Does not contain recognizable '
                                               'glycosaminoglycan features'},
                                 {   'smiles': 'O1C2C34C(C(N(CC3)C)CC5=C4C1=C(OC)C=C5)C=CC2OC',
                                     'name': '6-O-Methylcodeine',
                                     'reason': 'Does not contain recognizable '
                                               'glycosaminoglycan features'},
                                 {   'smiles': 'CN1C2=C(C=CC(=C2)OC)C3=C1[C@H](N(CC34CCN(CC4)S(=O)(=O)C5=CC=CS5)CC6CC6)CO',
                                     'name': "[(1S)-2-(cyclopropylmethyl)-7-methoxy-9-methyl-1'-thiophen-2-ylsulfonyl-1-spiro[1,3-dihydropyrido[3,4-b]indole-4,4'-piperidine]yl]methanol",
                                     'reason': 'Does not contain recognizable '
                                               'glycosaminoglycan features'},
                                 {   'smiles': 'O(C(=O)CCCCCCCCCCCCCCC)[C@@H](COC(=O)CCCCCCCCCCCCCCCCCCC)COC(=O)CCCCCCC',
                                     'name': 'TG(20:0/16:0/8:0)',
                                     'reason': 'Does not contain recognizable '
                                               'glycosaminoglycan features'},
                                 {   'smiles': 'O[C@@H]1CC2[C@](C3=C(C4=NCCC([C@@]4(C)CC3)[C@@H](CCC(C(C)C)C)C)CC2)(C)CC1',
                                     'name': 'UCA-1064-B',
                                     'reason': 'Does not contain recognizable '
                                               'glycosaminoglycan features'},
                                 {   'smiles': 'C1=CC=C(C=C1)N2C(=NN=C2SCC#N)COC3=CC=CC=C3',
                                     'name': '2-[[5-(phenoxymethyl)-4-phenyl-1,2,4-triazol-3-yl]thio]acetonitrile',
                                     'reason': 'Does not contain recognizable '
                                               'glycosaminoglycan features'},
                                 {   'smiles': 'O=C1C=2OC([C@H]3C[C@H](O)C(=C[C@H]3C2C(=O)C=4C1=C(O)C(=C(O)C4)C)C)(C)C',
                                     'name': 'Unnamed naphterpin 1',
                                     'reason': 'Does not contain recognizable '
                                               'glycosaminoglycan features'},
                                 {   'smiles': 'O([C@@H]1[C@]2(C([C@@](C1)(CC2)[H])(C)C)C)C(=O)/C=C/C3=CC=C(O)C=C3',
                                     'name': '(1R,4R)-1,7,7-Trimethylbicyclo[2.2.1]heptane-2beta-ol '
                                             '3-(4-hydroxyphenyl)acrylate',
                                     'reason': 'Does not contain recognizable '
                                               'glycosaminoglycan features'},
                                 {   'smiles': 'CC1(C)CC[C@@]2(CC[C@]3(C)C(=CC[C@@H]4[C@@]5(C)CC[C@H](O)C(C)(C)[C@@H]5CC[C@@]34C)[C@@H]2C1)C([O-])=O',
                                     'name': 'oleanolate',
                                     'reason': 'Does not contain recognizable '
                                               'glycosaminoglycan features'},
                                 {   'smiles': 'C[C@@H]1CN(C(=O)C2=C(N=CC(=C2)C3=CCCCC3)O[C@@H]1CN(C)CC4=CC=C(C=C4)C(=O)O)[C@H](C)CO',
                                     'name': '4-[[[(2S,3R)-8-(1-cyclohexenyl)-5-[(2R)-1-hydroxypropan-2-yl]-3-methyl-6-oxo-3,4-dihydro-2H-pyrido[2,3-b][1,5]oxazocin-2-yl]methyl-methylamino]methyl]benzoic '
                                             'acid',
                                     'reason': 'Does not contain recognizable '
                                               'glycosaminoglycan features'}],
    'sample_false_negatives': [   {   'smiles': 'S1C2=C3NC(=O)CC(OC)C=CC=CC=CCC(C(C(C(=CCCC(=C3O)C=C2NC(C1)=O)C)O)C)OC(=O)C(NC(=O)C4CCCCC4)C',
                                      'name': 'Thiazinotrienomycin B',
                                      'reason': 'Does not contain recognizable '
                                                'glycosaminoglycan features'},
                                  {   'smiles': 'O=C1O[C@H]([C@@H](O)C=CC(CCC(C=2C=3C(C=4[C@@]1(C=CC(=O)NC4C(=O)C3C=C(C)C2O)C)=O)=O)CC)C',
                                      'name': 'Hygrocin B',
                                      'reason': 'Does not contain recognizable '
                                                'glycosaminoglycan features'},
                                  {   'smiles': 'O=C1N([C@H](C(=O)NCCC[C@@H](C(N([C@H]1C(C)C)C)=O)NC(=O)/C=C/C=C/C(O)C(O)C)C)C',
                                      'name': 'Sclerotiotide H/I/J/K',
                                      'reason': 'Does not contain recognizable '
                                                'glycosaminoglycan features'},
                                  {   'smiles': 'S1C2=C3C(O)=C(NC(=O)CC(OC)C=CC=CC=CCC(C(C(C(=CCC3)C)O)C)OC(=O)C(NC(=O)C4=CCCCC4)C)C=C2N=C1',
                                      'name': 'Thiazinotrienomycin F',
                                      'reason': 'Does not contain recognizable '
                                                'glycosaminoglycan features'},
                                  {   'smiles': 'ClC1=C2NC(=O)C(=CC=CC=C[C@@H]([C@@H](O)CC(=O)C(C)=CC[C@@H](C=C[C@@H]([C@@H]([C@H](C=C(C(C=3C(C1=O)=C(C2=O)C=C(C)C3O)=O)C)C)O)C)O)C)C',
                                      'name': 'Naphthomycin A',
                                      'reason': 'Does not contain recognizable '
                                                'glycosaminoglycan features'},
                                  {   'smiles': 'S1C2=NC(=C1COC)C(=O)NCC(=O)NC(C=3SC=C(N3)C=4SC=C(N4)C5=C(C6=NC(C(NC(C7=NC(C(NC2C(C)C)=O)=C(S7)C)CC(=O)N)=O)=CS6)C=CC(=N5)C=8SC=C(N8)C=9OCC(N9)C(=O)N%10C(C(=O)N)CCC%10)C(O)C%11=CC=CC=C%11',
                                      'name': 'GE2270 B1',
                                      'reason': 'Does not contain recognizable '
                                                'glycosaminoglycan features'},
                                  {   'smiles': 'O=C1NC2=C(O)C(=CC(=C2)O)CCC=C(C(O)C(C)C(CC=CC=CC=CC(C1)OC)OC(=O)C3(NC(=O)C4CCCCC4)CC3)C',
                                      'name': 'Cytotrienin B',
                                      'reason': 'Does not contain recognizable '
                                                'glycosaminoglycan features'},
                                  {   'smiles': 'O=C1N(O)CCCCCNC(=O)CCC(=O)N(O)CCCCCCNC(CCC(N(CCCCCNC(CC1)=O)O)=O)=O',
                                      'name': 'Desferrioxamine X3',
                                      'reason': 'Does not contain recognizable '
                                                'glycosaminoglycan features'},
                                  {   'smiles': 'S1C2=C3C(O)=C(NC(=O)CC(OC)C=CC=CC=CCC(C(C(C(=CCC3)C)O)C)OC(=O)C(NC(=O)C4CCCCC4)C)C=C2N=C1',
                                      'name': 'Thiazinotrienomycin G',
                                      'reason': 'Does not contain recognizable '
                                                'glycosaminoglycan features'},
                                  {   'smiles': 'O=C1NC(CC=CC=C(C=CC=CC(CC(C(C=CC=CC=C1)O)O)O)C)C/C=C/CCC',
                                      'name': 'Aureoverticillactam',
                                      'reason': 'Does not contain recognizable '
                                                'glycosaminoglycan features'}],
    'attempt': 0,
    'reasoning': 'To classify whether a molecule is a glycosaminoglycan (GAG) '
                 "based on its SMILES string, it's essential to identify "
                 'structural features typically found in GAGs. '
                 'Glycosaminoglycans are polysaccharides made of repeating '
                 'disaccharide units containing an amino sugar. Common amino '
                 'sugars in GAGs include glucosamine or galactosamine. '
                 'However, detecting GAGs purely from SMILES can be '
                 'challenging because SMILES might not easily display the '
                 'repeating structure or the specific polysaccharide context.\n'
                 '\n'
                 'To solve this problem, the function can check for the '
                 'presence of an amino sugar motif, such as an oxygen and '
                 'nitrogen attached to adjacent carbon atoms, which is a '
                 'hallmark feature of amino-monosaccharides. In GAGs, these '
                 'motifs are part of larger repeating units.\n'
                 '\n'
                 "Here's how we might implement such a function:",
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 16,
    'num_false_positives': 1495,
    'num_true_negatives': 140559,
    'num_false_negatives': 230,
    'num_negatives': None,
    'precision': 0.010589013898080741,
    'recall': 0.06504065040650407,
    'f1': 0.01821286283437678,
    'accuracy': 0.9878777231201686,
    'negative_predictive_value': 0.9983663496437932}