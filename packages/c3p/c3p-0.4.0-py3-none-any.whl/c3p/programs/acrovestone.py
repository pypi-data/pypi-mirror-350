"""
Classifies: CHEBI:2440 acrovestone
"""
"""
Classifies: CHEBI:72099 Acrovestone
A polyphenol that is isolated from Acronychia pedunculata and exhibits moderate antioxidant and antityrosinase activities.
"""
from rdkit import Chem
from rdkit.Chem import rdMolDescriptors, Descriptors

def is_acrovestone(smiles: str):
    """
    Determines if a molecule is an acrovestone based on its SMILES string.
    Acrovestones are polyphenols with moderate antioxidant and antityrosinase activities, isolated from Acronychia pedunculata.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is an acrovestone, False otherwise
        str: Reason for classification
    """
    
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Acrovestones are polyphenolic compounds, so should contain multiple phenol groups
    phenol_pattern = Chem.MolFromSmarts("c1ccc(O)cc1")
    n_phenol_groups = len(mol.GetSubstructMatches(phenol_pattern))
    if n_phenol_groups < 2:
        return False, "Too few phenol groups for acrovestone"

    # Acrovestones often have glycosidic substituents, so look for sugar groups
    has_sugar_groups = any(atom.GetSmarts() in ['OC', 'OCC'] for atom in mol.GetAtoms())
    
    # Calculate common molecular descriptors and properties
    mol_wt = rdMolDescriptors.CalcExactMolWt(mol)
    n_rotatable_bonds = rdMolDescriptors.CalcNumRotatableBonds(mol)
    n_rings = rdMolDescriptors.CalcNumRings(mol)
    n_aromatic_rings = rdMolDescriptors.CalcNumAromaticRings(mol)
    tpsa = Descriptors.TPSA(mol)
    logp = Descriptors.MolLogP(mol)

    # Use a combination of structural features and molecular properties to classify
    if (
        n_phenol_groups >= 2
        and 300 < mol_wt < 800
        and n_rotatable_bonds > 5
        and n_rings >= 3
        and n_aromatic_rings >= 2
        and 100 < tpsa < 200
        and 2 < logp < 6
    ):
        if has_sugar_groups:
            return True, "Polyphenolic structure with glycosidic substituents, consistent with acrovestone"
        else:
            return True, "Polyphenolic structure, consistent with acrovestone"
    else:
        return False, "Structural features and molecular properties not typical of acrovestones"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:2440',
                          'name': 'acrovestone',
                          'definition': 'A polyphenol that is isolated from '
                                        'Acronychia pedunculata and exhibits '
                                        'moderate antioxidant and '
                                        'antityrosinase activities.',
                          'parents': [   'CHEBI:22187',
                                         'CHEBI:26195',
                                         'CHEBI:35618',
                                         'CHEBI:78840'],
                          'xrefs': [   'CAS:24177-16-0',
                                       'KEGG:C09916',
                                       'KNApSAcK:C00002978',
                                       'PMID:12880321',
                                       'PMID:22708987',
                                       'PMID:2506892',
                                       'PMID:2614422',
                                       'Reaxys:2611012'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 43,
                           'log_lines_of_code': 3.7612001156935624,
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
                                                 1,
                                                 2,
                                                 0,
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
                                                 1,
                                                 1,
                                                 0,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 1,
                                                 2,
                                                 3,
                                                 2,
                                                 3,
                                                 1,
                                                 2],
                           'max_indent': 3,
                           'imports': [   'from rdkit import Chem',
                                          'from rdkit.Chem import '
                                          'rdMolDescriptors, Descriptors'],
                           'imports_count': 2,
                           'methods_called': [   'GetAtoms',
                                                 'GetSmarts',
                                                 'CalcNumAromaticRings',
                                                 'MolLogP',
                                                 'CalcExactMolWt',
                                                 'MolFromSmiles',
                                                 'CalcNumRings',
                                                 'MolFromSmarts',
                                                 'CalcNumRotatableBonds',
                                                 'TPSA',
                                                 'GetSubstructMatches'],
                           'methods_called_count': 11,
                           'smarts_strings': ['c1ccc(O)cc1'],
                           'smarts_strings_count': 1,
                           'defs': ['is_acrovestone(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "Too few phenol groups for '
                                          'acrovestone"',
                                          'True, "Polyphenolic structure with '
                                          'glycosidic substituents, consistent '
                                          'with acrovestone"',
                                          'True, "Polyphenolic structure, '
                                          'consistent with acrovestone"',
                                          'False, "Structural features and '
                                          'molecular properties not typical of '
                                          'acrovestones"'],
                           'returns_count': 5,
                           'complexity': 4.752240023138713},
    'message': '\n'
               'Attempt failed: F1 score of 0 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: NONE\n'
               'False positives: NONE\n'
               'False negatives: SMILES: '
               'O=C1C2=C(OC=C1C3=CC=C(O)C=C3)C=C(O)C=C2OC4O[C@H]([C@H](O)[C@H]([C@H]4O)O)C '
               'NAME: Genestein G1 REASON: MISSED No isoflavone backbone '
               'found\n'
               ' * SMILES: '
               'O1C(C(O)C(O)C(O)C1OC2=CC=3OC=C(C(=O)C3C=C2)C4=CC=C(OC)C=C4)COC(=O)CC5CCNCC5 '
               'NAME: Isoflavone base + 1o, 1meo, o-hex+c7h12no REASON: MISSED '
               'No isoflavone backbone found\n'
               ' * SMILES: '
               'O1C(C(O)C(O)C(O)C1OC=2C=C3OC=C(C(=O)C3=C(O)C2)C=4C(O)=CC=CC4)CO '
               'NAME: Isogenistein 7-glucoside REASON: MISSED No isoflavone '
               'backbone found\n'
               ' * SMILES: '
               'S(OC1=CC=2OC=C(C3=CC=C(O[C@H]4O[C@H](C(O)[C@@H](O)C4O)C(O)=O)C=C3)C(=O)C2C=C1)(O)(=O)=O '
               "NAME: daidzein 4'-glucuronide-7-sulfate REASON: MISSED No "
               'isoflavone backbone found\n'
               ' * SMILES: '
               'O([C@H]1[C@H](O)C(O[C@@H](OC2=C(OC)C=C3C(OC=C(C3=O)C4=CC(OC)=C(OC)C=C4)=C2)C1O)CO)[C@@H]5OC([C@@H](O)[C@H](O)C5O)CO '
               'NAME: Cladrastin 7-O-laminaribioside REASON: MISSED No '
               'isoflavone backbone found\n'
               ' * SMILES: '
               'O1C(C(O)C(O)C(O)C1OC2=C3C(OC=C(C3=O)C4=CC(OC)=C(OC)C=C4)=C(C(OC)=C2)C)COC5OC(C(O)C(O)C5O)C(O)=O '
               'NAME: '
               '6-[(6-{[3-(3,4-dimethoxyphenyl)-7-methoxy-8-methyl-4-oxo-4H-chromen-5-yl]oxy}-3,4,5-trihydroxyoxan-2-yl)methoxy]-3,4,5-trihydroxyoxane-2-carboxylic '
               'acid REASON: MISSED No isoflavone backbone found\n'
               ' * SMILES: '
               'O=C1C(C2=CC=C(O)C=C2)=COC3=C1C=CC(=C3)OC4O[C@H]([C@H](O)[C@H]([C@H]4OC)O)C '
               'NAME: Daidzein G3 REASON: MISSED No isoflavone backbone found\n'
               ' * SMILES: '
               'O1C(C(O)C(O)C(O)C1OC2=CC=3OC=C(C(=O)C3C=C2)C4=CC=C(O)C=C4)COC(=O)C '
               'NAME: '
               '[6-[3-(4-Hydroxyphenyl)-4-oxidanylidene-chromen-7-yl]oxy-3,4,5-tris(oxidanyl)oxan-2-yl]methyl '
               'ethanoate REASON: MISSED No isoflavone backbone found\n'
               ' * SMILES: '
               'O1C(C(O)C(O)C(O)C1OC=2C=C3OC=C(C4=CC=C(OC5OCC(O)(C5O)CO)C=C4)C(=O)C3=C(O)C2)CO '
               "NAME: Genistein 7-O-glucoside-4'-O-apioside REASON: MISSED No "
               'isoflavone backbone found\n'
               ' * SMILES: '
               'O1C(C(O)C(O)C(O)C1OC2=CC=3OCC(CC3C=C2)C4=C(O)C=C(OC)C=C4)CO '
               'NAME: Vestitone 7-glucoside REASON: MISSED No isoflavone '
               'backbone found\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n'
               'IMPORTANT NOTE: I do not have 100% confidence in the benchmark '
               'I am using. There may be occasional and systematic mistakes. '
               'Use your best judgment, and if you think the classifications '
               'your program are consistent with your understanding if the '
               'meaning of the chemical class, then you can ignore outliers, '
               'but explain your reasoning in doing so. I have great '
               'confidence in your broad understanding of chemistry and your '
               'ability to translate this into code.',
    'sample_true_negatives': [   {   'smiles': 'CN(C)CC1=CN(N=N1)CC[C@@H]2CC[C@H]([C@@H](O2)CO)NC(=O)NC3=CC4=C(C=C3)OCO4',
                                     'name': '1-(1,3-benzodioxol-5-yl)-3-[(2R,3R,6S)-6-[2-[4-[(dimethylamino)methyl]-1-triazolyl]ethyl]-2-(hydroxymethyl)-3-oxanyl]urea',
                                     'reason': 'Structural features and '
                                               'molecular properties not '
                                               'typical of acrovestones'},
                                 {   'smiles': 'C\\C(CO)=C/CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(CO)=C\\C[C@H]1OC(=O)C=C1CO',
                                     'name': 'Hippolide F',
                                     'reason': 'Too few phenol groups for '
                                               'acrovestone'},
                                 {   'smiles': 'O([C@H]1[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]1CO)O[C@H]2[C@H](O)[C@@H](NC(=O)C)C(O[C@@H]2CO)O)[C@@H]3O[C@@H]([C@@H](O)[C@H](O[C@H]4O[C@@H]([C@@H](O)[C@H](O)[C@@H]4O)CO)[C@@H]3O)CO[C@H]5O[C@@H]([C@@H](O)[C@H](O[C@H]6O[C@@H]([C@@H](O)[C@H](O)[C@@H]6O[C@H]7O[C@@H]([C@@H](O)[C@H](O)[C@@H]7O)CO)CO)[C@@H]5O)CO[C@H]8O[C@@H]([C@@H](O)[C@H](O)[C@@H]8O)CO',
                                     'name': 'N-[(3R,4R,5S,6R)-5-[(2S,3R,4R,5S,6R)-3-Acetamido-5-[(2S,3S,4S,5R,6R)-6-[[(2S,3S,4S,5R,6R)-4-[(2R,3S,4S,5S,6R)-4,5-dihydroxy-6-(hydroxymethyl)-3-[(2S,3S,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-3,5-dihydroxy-6-[[(2S,3S,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxymethyl]oxan-2-yl]oxymethyl]-3,5-dihydroxy-4-[(2S,3S,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-2,4-dihydroxy-6-(hydroxymethyl)oxan-3-yl]acetamide',
                                     'reason': 'Too few phenol groups for '
                                               'acrovestone'},
                                 {   'smiles': 'O=C1NCC(=O)N2CCC[C@H]2C(N[C@H]1CCC(=O)O)=O',
                                     'name': 'Cyclo-(glycyl-L-prolyl-L-glutamyl)',
                                     'reason': 'Too few phenol groups for '
                                               'acrovestone'},
                                 {   'smiles': 'CC[C@@]1(O)C[C@H](O[C@H]2C[C@H]([NH3+])[C@H](O)[C@H](C)O2)c2c(O)c3C(=O)c4c(O)cccc4C(=O)c3c(O)c2[C@H]1C(=O)OC',
                                     'name': 'rhodomycin D(1+)',
                                     'reason': 'Structural features and '
                                               'molecular properties not '
                                               'typical of acrovestones'},
                                 {   'smiles': 'O[C@H]1[C@@H](O)[C@@H](O[C@@H]1COP(O)(O)=O)n1cc(F)c(=O)[nH]c1=O',
                                     'name': "5-fluorouridine 5'-monophosphate",
                                     'reason': 'Too few phenol groups for '
                                               'acrovestone'},
                                 {   'smiles': 'CCC(=O)O[C@@H]1CC(=O)O[C@@H](CC=CC=C[C@@H]([C@@H](C[C@@H]([C@@H]([C@H]1OC)OC2C(C(C(C(O2)C)OC3CC(C(C(O3)C)OC(=O)CC)(C)O)N(C)C)O)CC=O)C)O)C',
                                     'name': 'propanoic acid '
                                             '[(4R,5S,6S,7R,9R,10R,16R)-6-[[4-(dimethylamino)-3-hydroxy-5-[[4-hydroxy-4,6-dimethyl-5-(1-oxopropoxy)-2-oxanyl]oxy]-6-methyl-2-oxanyl]oxy]-10-hydroxy-5-methoxy-9,16-dimethyl-2-oxo-7-(2-oxoethyl)-1-oxacyclohexadeca-11,13-dien-4-yl] '
                                             'ester',
                                     'reason': 'Too few phenol groups for '
                                               'acrovestone'},
                                 {   'smiles': 'C[C@H]1CN([C@@H](COC2=C(C=C(C=C2)NC(=O)C3CC3)C(=O)N(C[C@H]1OC)C)C)C(=O)CN4CCOCC4',
                                     'name': 'N-[(4R,7S,8S)-8-methoxy-4,7,10-trimethyl-5-(2-morpholin-4-ylacetyl)-11-oxo-2-oxa-5,10-diazabicyclo[10.4.0]hexadeca-1(12),13,15-trien-14-yl]cyclopropanecarboxamide',
                                     'reason': 'Too few phenol groups for '
                                               'acrovestone'},
                                 {   'smiles': 'O=C(N[C@@H](CC(=O)N)C(O)=O)[C@@H](NC(=O)[C@@H](N)CC=1C=2C(NC1)=CC=CC2)[C@H](CC)C',
                                     'name': 'Trp-Ile-Asn',
                                     'reason': 'Too few phenol groups for '
                                               'acrovestone'},
                                 {   'smiles': 'N12C([C@@H](NC([C@@]1(CCC2)[H])=O)CC3=C(NC4=C3C=CC(=C4)O)C(C=C)(C)C)=O',
                                     'name': '6-hydroxydeoxybrevianamide E',
                                     'reason': 'Too few phenol groups for '
                                               'acrovestone'}],
    'sample_false_negatives': [   {   'smiles': 'O=C1C2=C(OC=C1C3=CC=C(O)C=C3)C=C(O)C=C2OC4O[C@H]([C@H](O)[C@H]([C@H]4O)O)C',
                                      'name': 'Genestein G1',
                                      'reason': 'Structural features and '
                                                'molecular properties not '
                                                'typical of acrovestones'},
                                  {   'smiles': 'O1C(C(O)C(O)C(O)C1OC2=CC=3OC=C(C(=O)C3C=C2)C4=CC=C(OC)C=C4)COC(=O)CC5CCNCC5',
                                      'name': 'Isoflavone base + 1o, 1meo, '
                                              'o-hex+c7h12no',
                                      'reason': 'Structural features and '
                                                'molecular properties not '
                                                'typical of acrovestones'},
                                  {   'smiles': 'O1C(C(O)C(O)C(O)C1OC=2C=C3OC=C(C(=O)C3=C(O)C2)C=4C(O)=CC=CC4)CO',
                                      'name': 'Isogenistein 7-glucoside',
                                      'reason': 'Structural features and '
                                                'molecular properties not '
                                                'typical of acrovestones'},
                                  {   'smiles': 'S(OC1=CC=2OC=C(C3=CC=C(O[C@H]4O[C@H](C(O)[C@@H](O)C4O)C(O)=O)C=C3)C(=O)C2C=C1)(O)(=O)=O',
                                      'name': 'daidzein '
                                              "4'-glucuronide-7-sulfate",
                                      'reason': 'Structural features and '
                                                'molecular properties not '
                                                'typical of acrovestones'},
                                  {   'smiles': 'O([C@H]1[C@H](O)C(O[C@@H](OC2=C(OC)C=C3C(OC=C(C3=O)C4=CC(OC)=C(OC)C=C4)=C2)C1O)CO)[C@@H]5OC([C@@H](O)[C@H](O)C5O)CO',
                                      'name': 'Cladrastin 7-O-laminaribioside',
                                      'reason': 'Structural features and '
                                                'molecular properties not '
                                                'typical of acrovestones'},
                                  {   'smiles': 'O1C(C(O)C(O)C(O)C1OC2=C3C(OC=C(C3=O)C4=CC(OC)=C(OC)C=C4)=C(C(OC)=C2)C)COC5OC(C(O)C(O)C5O)C(O)=O',
                                      'name': '6-[(6-{[3-(3,4-dimethoxyphenyl)-7-methoxy-8-methyl-4-oxo-4H-chromen-5-yl]oxy}-3,4,5-trihydroxyoxan-2-yl)methoxy]-3,4,5-trihydroxyoxane-2-carboxylic '
                                              'acid',
                                      'reason': 'Structural features and '
                                                'molecular properties not '
                                                'typical of acrovestones'},
                                  {   'smiles': 'O=C1C(C2=CC=C(O)C=C2)=COC3=C1C=CC(=C3)OC4O[C@H]([C@H](O)[C@H]([C@H]4OC)O)C',
                                      'name': 'Daidzein G3',
                                      'reason': 'Structural features and '
                                                'molecular properties not '
                                                'typical of acrovestones'},
                                  {   'smiles': 'O1C(C(O)C(O)C(O)C1OC2=CC=3OC=C(C(=O)C3C=C2)C4=CC=C(O)C=C4)COC(=O)C',
                                      'name': '[6-[3-(4-Hydroxyphenyl)-4-oxidanylidene-chromen-7-yl]oxy-3,4,5-tris(oxidanyl)oxan-2-yl]methyl '
                                              'ethanoate',
                                      'reason': 'Structural features and '
                                                'molecular properties not '
                                                'typical of acrovestones'},
                                  {   'smiles': 'O1C(C(O)C(O)C(O)C1OC=2C=C3OC=C(C4=CC=C(OC5OCC(O)(C5O)CO)C=C4)C(=O)C3=C(O)C2)CO',
                                      'name': 'Genistein '
                                              "7-O-glucoside-4'-O-apioside",
                                      'reason': 'Structural features and '
                                                'molecular properties not '
                                                'typical of acrovestones'},
                                  {   'smiles': 'O1C(C(O)C(O)C(O)C1OC2=CC=3OCC(CC3C=C2)C4=C(O)C=C(OC)C=C4)CO',
                                      'name': 'Vestitone 7-glucoside',
                                      'reason': 'Structural features and '
                                                'molecular properties not '
                                                'typical of acrovestones'}],
    'attempt': 2,
    'reasoning': 'Based on the previous code and the provided outcomes, it '
                 'appears that the program fails to correctly identify several '
                 'known acrovestone structures. The main issue seems to be the '
                 'assumption that acrovestones must have an isoflavone '
                 'backbone, as the program checks for this structural feature '
                 'using the SMARTS pattern '
                 '`"C1=CC(=O)Oc2c1cc(O)c(c2)c3ccc(O)cc3"`.\n'
                 '\n'
                 'However, the examples provided suggest that acrovestones can '
                 'have a broader range of structural scaffolds beyond just '
                 'isoflavones. Many of the false negatives appear to be '
                 'flavonoid or phenolic structures without the specific '
                 'isoflavone backbone.\n'
                 '\n'
                 'To improve the program, we need to broaden our definition of '
                 'acrovestones and consider other structural features and '
                 'molecular properties that are characteristic of this class.\n'
                 '\n'
                 "Here's an improved version of the program that takes a more "
                 'general approach:',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 3,
    'num_false_positives': 2132,
    'num_true_negatives': 140083,
    'num_false_negatives': 82,
    'num_negatives': None,
    'precision': 0.001405152224824356,
    'recall': 0.03529411764705882,
    'f1': 0.002702702702702703,
    'accuracy': 0.9844413211524947,
    'negative_predictive_value': 0.9994149752077908}