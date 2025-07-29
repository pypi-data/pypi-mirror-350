"""
Classifies: CHEBI:47916 flavonoid
"""
"""
Classifies: Flavonoid
Definition: A flavonoid is any member of the 'superclass' flavonoids whose 
skeleton is based on 1-benzopyran with an aryl substituent at position 2.
This heuristic implementation checks for three classical substructures:
  1. Flavone: 2-phenylchromen-4-one scaffold.
  2. Flavanone: A related scaffold with a saturated central ring.
  3. Flavanol: A variant with an –OH substituent on the heterocycle.
Note: Many flavonoids bear additional substituents (e.g. sugars) but if 
the core is present, the molecule is classified as a flavonoid.
"""
from rdkit import Chem

def is_flavonoid(smiles: str):
    """
    Determines if a molecule is (putatively) a flavonoid based on its SMILES string.
    
    This function uses substructure searches with SMARTS queries that capture
    classical flavonoid cores (e.g. flavone, flavanone, flavanol). These patterns
    have an internal benzopyran system with an exocyclic aromatic ring (at position 2).
    
    Args:
        smiles (str): SMILES string for the molecule.
    
    Returns:
        bool: True if the molecule appears to contain a flavonoid scaffold, else False.
        str: Explanation of the classification.
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
    
    # Define SMARTS patterns for typical flavonoid cores.
    # 1. Flavone: 2-phenylchromen-4-one. Example: quercetin aglycone.
    pattern_flavone = Chem.MolFromSmarts("c1ccc(cc1)-c2oc(=O)c3ccccc3c2")
    
    # 2. Flavanone: Similar to flavone but the pyran ring is saturated except for the carbonyl.
    # This pattern represents a 2-phenylchroman-4-one.
    pattern_flavanone = Chem.MolFromSmarts("c1ccc(cc1)-C2CC(=O)c3ccccc3O2")
    
    # 3. Flavanol: Like flavanone but with a hydroxyl instead of carbonyl at position 4.
    # Example: catechin.
    pattern_flavanol = Chem.MolFromSmarts("c1ccc(cc1)-C2CC(O)c3ccccc3O2")
    
    # Try matching each pattern; if one is found, we classify as flavonoid.
    if mol.HasSubstructMatch(pattern_flavone):
        return True, "Molecule contains a flavone (2-phenylchromen-4-one) flavonoid scaffold."
    if mol.HasSubstructMatch(pattern_flavanone):
        return True, "Molecule contains a flavanone (2-phenylchroman-4-one) flavonoid scaffold."
    if mol.HasSubstructMatch(pattern_flavanol):
        return True, "Molecule contains a flavanol (2-phenylchroman-4-ol) flavonoid scaffold."
    
    # If none of the patterns matches, we return False.
    return False, "No recognizable flavonoid scaffold (based on classical flavone/flavanone/flavanol cores) was detected."

# Example usage (for testing)
if __name__ == "__main__":
    # (R)-naringenin is a prototypical flavanone.
    test_smiles = "Oc1ccc(cc1)[C@H]1CC(=O)c2c(O)cc(O)cc2O1"
    result, reason = is_flavonoid(test_smiles)
    print(result, ":", reason)


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:47916',
                          'name': 'flavonoid',
                          'definition': "Any member of the 'superclass' "
                                        'flavonoids whose skeleton is based on '
                                        '1-benzopyran with an aryl substituent '
                                        'at position 2. The term was '
                                        'originally restricted to natural '
                                        'products, but is now also used to '
                                        'describe semi-synthetic and fully '
                                        'synthetic compounds.',
                          'parents': ['CHEBI:72544'],
                          'xrefs': ['KEGG:C01579', 'Wikipedia:Flavonoid'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 36,
                           'log_lines_of_code': 3.58351893845611,
                           'indent_by_line': [   1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
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
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 1,
                                                 2,
                                                 1,
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 1],
                           'max_indent': 2,
                           'imports': ['from rdkit import Chem'],
                           'imports_count': 1,
                           'methods_called': [   'HasSubstructMatch',
                                                 'MolFromSmarts',
                                                 'MolFromSmiles'],
                           'methods_called_count': 3,
                           'smarts_strings': [   'c1ccc(cc1)-C2CC(=O)c3ccccc3O2',
                                                 'c1ccc(cc1)-C2CC(O)c3ccccc3O2',
                                                 'c1ccc(cc1)-c2oc(=O)c3ccccc3c2'],
                           'smarts_strings_count': 3,
                           'defs': ['is_flavonoid(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'True, "Molecule contains a flavone '
                                          '(2-phenylchromen-4-one) flavonoid '
                                          'scaffold."',
                                          'True, "Molecule contains a '
                                          'flavanone (2-phenylchroman-4-one) '
                                          'flavonoid scaffold."',
                                          'True, "Molecule contains a flavanol '
                                          '(2-phenylchroman-4-ol) flavonoid '
                                          'scaffold."',
                                          'False, "No recognizable flavonoid '
                                          'scaffold (based on classical '
                                          'flavone/flavanone/flavanol cores) '
                                          'was detected."'],
                           'returns_count': 5,
                           'complexity': 2.9167037876912216},
    'message': '\n'
               'Attempt failed: F1 score of 0 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: NONE\n'
               'False positives: NONE\n'
               'False negatives: SMILES: '
               'C12=C(C(=CC(=C2C(C(=C(O1)C=3C=CC(=C(C3)O)O)O)=O)O)O)CC=4C5=C(C(=CC4O)O)C(C(=C(O5)C=6C=CC(=C(C6)O)O)O)=O '
               'NAME: 8,8"-methylene-bisquercetin REASON: MISSED No '
               'appropriate exocyclic fully aromatic substituent attached to a '
               'benzopyran core was found.\n'
               ' * SMILES: '
               'C\\C=C(\\C)C(=O)Oc1ccc(cc1O)-c1cc(=O)c2c(O)cc(O[C@@H]3O[C@H](CO)[C@@H](O)[C@H](O)[C@H]3O)cc2o1 '
               'NAME: luteolin '
               "7-O-beta-D-glucoside-4'-(Z-2-methyl-2-butenoate) REASON: "
               'MISSED No appropriate exocyclic fully aromatic substituent '
               'attached to a benzopyran core was found.\n'
               ' * SMILES: Oc1ccc(cc1)[C@H]1CC(=O)c2c(O)cc(O)cc2O1 NAME: '
               '(R)-naringenin REASON: MISSED No appropriate exocyclic fully '
               'aromatic substituent attached to a benzopyran core was found.\n'
               ' * SMILES: '
               'O1C=2C3=C(OC(C=C3)(C)C)C=C(O)C2C(=O)C=4C(OC5=C(C14)C=CC(O)=C5)C=C(C)C '
               'NAME: cyclomorusin A REASON: MISSED No appropriate exocyclic '
               'fully aromatic substituent attached to a benzopyran core was '
               'found.\n'
               ' * SMILES: '
               'O=C([C@H]1C(CC(=C[C@@]1(C=2C=3OC(=C(C(=O)C3C(O)=CC2O)CC=C(C)C)C4=C(O)C=C(O)C=C4)[H])C)C5=C(O)C=C(O)C=C5)C6=C(O)C(=C(O)C=C6)CC=C(C)C '
               'NAME: Albanin G REASON: MISSED No appropriate exocyclic fully '
               'aromatic substituent attached to a benzopyran core was found.\n'
               ' * SMILES: '
               'COc1cc(cc(OC)c1OC)-c1cc(=O)c2c(OC)c(OC)c(OC)c(OC)c2o1 NAME: '
               '2-(3,4,5-trimethoxyphenyl)-5,6,7,8-tetramethoxy-4H-1-benzopyran-4-one '
               'REASON: MISSED No appropriate exocyclic fully aromatic '
               'substituent attached to a benzopyran core was found.\n'
               ' * SMILES: O1C(C(O)CC=2C1=CC(O)=CC2O)C3=CC=C(O)C=C3 NAME: '
               '2-(4-Hydroxyphenyl)-3,4-dihydro-2H-1-benzopyran-3,5,7-triol '
               'REASON: MISSED No appropriate exocyclic fully aromatic '
               'substituent attached to a benzopyran core was found.\n'
               ' * SMILES: '
               'C1=2C(C(=C(OC1=CC(=CC2[O-])O[C@H]3[C@@H]([C@H]([C@@H]([C@H](O3)CO)O)O)O)C4=CC=C(C=C4)O)O)=O '
               'NAME: kaempferol 7-O-beta-D-glucoside(1-) REASON: MISSED No '
               'appropriate exocyclic fully aromatic substituent attached to a '
               'benzopyran core was found.\n'
               ' * SMILES: O[C@@H]1[C@H](Oc2cc(O)cc(O)c2C1=O)c1ccc(O)c(O)c1 '
               'NAME: (+)-taxifolin REASON: MISSED No appropriate exocyclic '
               'fully aromatic substituent attached to a benzopyran core was '
               'found.\n'
               ' * SMILES: O1C(C(O)CC2=C1C=C(OC)C=C2OC)C3=CC(O)=C(OC)C=C3 '
               "NAME: 3,3'-Dihydroxy-4',5,7-trimethoxyflavan REASON: MISSED No "
               'appropriate exocyclic fully aromatic substituent attached to a '
               'benzopyran core was found.\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'O=C(N[C@@H](C(O)(C)C)C)[C@H]([C@@]1([C@@]2([C@@](CC1)(/C(/CCC2)=C/C=C\\3/C[C@@H](O)C[C@H](O)C3=C)[H])C)[H])C',
                                     'name': '1alpha,25-dihydroxy-24-oxo-23-azavitamin '
                                             'D2 / '
                                             '1alpha,25-dihydroxy-24-oxo-23-azaergocalciferol',
                                     'reason': 'No recognizable flavonoid '
                                               'scaffold (based on classical '
                                               'flavone/flavanone/flavanol '
                                               'cores) was detected.'},
                                 {   'smiles': 'CCCCCCCCCCCCCCCCCCC(O)C([O-])=O',
                                     'name': '2-hydroxyarachidate',
                                     'reason': 'No recognizable flavonoid '
                                               'scaffold (based on classical '
                                               'flavone/flavanone/flavanol '
                                               'cores) was detected.'},
                                 {   'smiles': 'C[C@@H](CN([C@@H](C)CO)C(=O)NC1=CC=C(C=C1)C(F)(F)F)[C@@H](CN(C)C(=O)C2CCOCC2)OC',
                                     'name': 'N-[(2S,3S)-4-[[(2S)-1-hydroxypropan-2-yl]-[[4-(trifluoromethyl)phenyl]carbamoyl]amino]-2-methoxy-3-methylbutyl]-N-methyloxane-4-carboxamide',
                                     'reason': 'No recognizable flavonoid '
                                               'scaffold (based on classical '
                                               'flavone/flavanone/flavanol '
                                               'cores) was detected.'},
                                 {   'smiles': 'CC(=O)CC\\C=C(/C)CCC=C(C)C',
                                     'name': 'geranyl acetone',
                                     'reason': 'No recognizable flavonoid '
                                               'scaffold (based on classical '
                                               'flavone/flavanone/flavanol '
                                               'cores) was detected.'},
                                 {   'smiles': 'O([C@H]1[C@H](O)[C@H](O[C@H](O)[C@H]1O)CO[C@H]2O[C@@H]([C@@H](O)[C@H](O)[C@@H]2O)CO)[C@H]3O[C@@H]([C@@H](O)[C@H](O)[C@@H]3O[C@H]4O[C@@H]([C@@H](O)[C@H](O)[C@@H]4O)CO)CO',
                                     'name': '(2S,3S,4S,5S,6R)-2-[[(2R,3R,4S,5S,6S)-4-[(2R,3S,4S,5S,6R)-4,5-Dihydroxy-6-(hydroxymethyl)-3-[(2R,3S,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-3,5,6-trihydroxyoxan-2-yl]methoxy]-6-(hydroxymethyl)oxane-3,4,5-triol',
                                     'reason': 'No recognizable flavonoid '
                                               'scaffold (based on classical '
                                               'flavone/flavanone/flavanol '
                                               'cores) was detected.'},
                                 {   'smiles': 'O=C(OC1=C(C(O)=C(C(=O)O)C(=C1C)C)C)C2=C(OC)C(=C(OC(=O)C3=C(O)C=C(O)C=C3C)C=C2C)C',
                                     'name': 'Thielavin Z5',
                                     'reason': 'No recognizable flavonoid '
                                               'scaffold (based on classical '
                                               'flavone/flavanone/flavanol '
                                               'cores) was detected.'},
                                 {   'smiles': '[C@@H]1([C@@H]([C@H]([C@@H]([C@H](O1)CO)O)O)NC(C)=O)O[C@@H]2[C@@H]([C@H](C(O[C@@H]2CO)O)O)O',
                                     'name': 'beta-D-GlcpNAc-(1->4)-D-Galp',
                                     'reason': 'No recognizable flavonoid '
                                               'scaffold (based on classical '
                                               'flavone/flavanone/flavanol '
                                               'cores) was detected.'},
                                 {   'smiles': 'CN(C)C(=O)C1=CC=C(C=C1)C2=CC=C(C=C2)[C@@H]3[C@H]4CN(CC(=O)N4[C@H]3CO)C(=O)CC5CC5',
                                     'name': '4-[4-[(6S,7R,8R)-4-(2-cyclopropyl-1-oxoethyl)-8-(hydroxymethyl)-2-oxo-1,4-diazabicyclo[4.2.0]octan-7-yl]phenyl]-N,N-dimethylbenzamide',
                                     'reason': 'No recognizable flavonoid '
                                               'scaffold (based on classical '
                                               'flavone/flavanone/flavanol '
                                               'cores) was detected.'},
                                 {   'smiles': 'CCCCCCCCCCCCCCCCCCCCC=C',
                                     'name': '1-docosene',
                                     'reason': 'No recognizable flavonoid '
                                               'scaffold (based on classical '
                                               'flavone/flavanone/flavanol '
                                               'cores) was detected.'},
                                 {   'smiles': 'C([C@@](OC(=O)CCC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)([H])COC(=O)CC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)OC(=O)CCCCC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC',
                                     'name': 'TG(22:5(7Z,10Z,13Z,16Z,19Z)/20:5(5Z,8Z,11Z,14Z,17Z)/22:6(4Z,7Z,10Z,13Z,16Z,19Z))[iso6]',
                                     'reason': 'No recognizable flavonoid '
                                               'scaffold (based on classical '
                                               'flavone/flavanone/flavanol '
                                               'cores) was detected.'}],
    'sample_false_negatives': [   {   'smiles': 'C12=C(C(=CC(=C2C(C(=C(O1)C=3C=CC(=C(C3)O)O)O)=O)O)O)CC=4C5=C(C(=CC4O)O)C(C(=C(O5)C=6C=CC(=C(C6)O)O)O)=O',
                                      'name': '8,8"-methylene-bisquercetin',
                                      'reason': 'No recognizable flavonoid '
                                                'scaffold (based on classical '
                                                'flavone/flavanone/flavanol '
                                                'cores) was detected.'},
                                  {   'smiles': 'C\\C=C(\\C)C(=O)Oc1ccc(cc1O)-c1cc(=O)c2c(O)cc(O[C@@H]3O[C@H](CO)[C@@H](O)[C@H](O)[C@H]3O)cc2o1',
                                      'name': 'luteolin '
                                              "7-O-beta-D-glucoside-4'-(Z-2-methyl-2-butenoate)",
                                      'reason': 'No recognizable flavonoid '
                                                'scaffold (based on classical '
                                                'flavone/flavanone/flavanol '
                                                'cores) was detected.'},
                                  {   'smiles': 'O1C=2C3=C(OC(C=C3)(C)C)C=C(O)C2C(=O)C=4C(OC5=C(C14)C=CC(O)=C5)C=C(C)C',
                                      'name': 'cyclomorusin A',
                                      'reason': 'No recognizable flavonoid '
                                                'scaffold (based on classical '
                                                'flavone/flavanone/flavanol '
                                                'cores) was detected.'},
                                  {   'smiles': 'O=C([C@H]1C(CC(=C[C@@]1(C=2C=3OC(=C(C(=O)C3C(O)=CC2O)CC=C(C)C)C4=C(O)C=C(O)C=C4)[H])C)C5=C(O)C=C(O)C=C5)C6=C(O)C(=C(O)C=C6)CC=C(C)C',
                                      'name': 'Albanin G',
                                      'reason': 'No recognizable flavonoid '
                                                'scaffold (based on classical '
                                                'flavone/flavanone/flavanol '
                                                'cores) was detected.'},
                                  {   'smiles': 'COc1cc(cc(OC)c1OC)-c1cc(=O)c2c(OC)c(OC)c(OC)c(OC)c2o1',
                                      'name': '2-(3,4,5-trimethoxyphenyl)-5,6,7,8-tetramethoxy-4H-1-benzopyran-4-one',
                                      'reason': 'No recognizable flavonoid '
                                                'scaffold (based on classical '
                                                'flavone/flavanone/flavanol '
                                                'cores) was detected.'},
                                  {   'smiles': 'O1C(C(O)CC=2C1=CC(O)=CC2O)C3=CC=C(O)C=C3',
                                      'name': '2-(4-Hydroxyphenyl)-3,4-dihydro-2H-1-benzopyran-3,5,7-triol',
                                      'reason': 'No recognizable flavonoid '
                                                'scaffold (based on classical '
                                                'flavone/flavanone/flavanol '
                                                'cores) was detected.'},
                                  {   'smiles': 'C1=2C(C(=C(OC1=CC(=CC2[O-])O[C@H]3[C@@H]([C@H]([C@@H]([C@H](O3)CO)O)O)O)C4=CC=C(C=C4)O)O)=O',
                                      'name': 'kaempferol '
                                              '7-O-beta-D-glucoside(1-)',
                                      'reason': 'No recognizable flavonoid '
                                                'scaffold (based on classical '
                                                'flavone/flavanone/flavanol '
                                                'cores) was detected.'},
                                  {   'smiles': 'O1C(C(O)CC2=C1C=C(OC)C=C2OC)C3=CC(O)=C(OC)C=C3',
                                      'name': "3,3'-Dihydroxy-4',5,7-trimethoxyflavan",
                                      'reason': 'No recognizable flavonoid '
                                                'scaffold (based on classical '
                                                'flavone/flavanone/flavanol '
                                                'cores) was detected.'},
                                  {   'smiles': 'O[C@@H]1Cc2c(O)cc(O)c([C@H]3[C@@H](O)[C@H](Oc4cc(O)cc(O)c34)c3ccc(O)c(O)c3)c2O[C@@H]1c1ccc(O)c(O)c1',
                                      'name': '(-)-epicatechin-(4alpha->8)-(-)-epicatechin',
                                      'reason': 'No recognizable flavonoid '
                                                'scaffold (based on classical '
                                                'flavone/flavanone/flavanol '
                                                'cores) was detected.'},
                                  {   'smiles': 'OC[C@H]1OC(Oc2cc3oc(cc(=O)c3c(O)c2[C@@H]2O[C@H](CO)[C@@H](O)[C@H](O)[C@H]2O)-c2ccc(O)c(O)c2)[C@H](O)[C@@H](O)[C@@H]1O',
                                      'name': 'isoorientin 7-O-glucoside',
                                      'reason': 'No recognizable flavonoid '
                                                'scaffold (based on classical '
                                                'flavone/flavanone/flavanol '
                                                'cores) was detected.'}],
    'attempt': 5,
    'reasoning': 'Below is one improved solution. In our reasoning we noticed '
                 'that the original approach tried to reassemble the flavonoid '
                 '“core” by examining all rings and then trying to detect an '
                 'external fully aromatic ring attached via a single atom. In '
                 'practice many flavonoid‐structures are decorated with sugars '
                 'and additional substituents so that the “core” is not '
                 'trivially separated from the rest of the molecule. One way '
                 'to improve the procedure is to rely on substructure matching '
                 'via a few “classic” flavonoid SMARTS patterns. For example, '
                 'most flavonoids contain a benzopyran skeleton with an '
                 'aromatic substituent at the 2‐position. In many cases this '
                 'flavonoid substructure is well captured by the patterns for '
                 'flavones, flavanones, or flavanols. (Of course, not every '
                 'flavonoid will match one of these “canonical” patterns, but '
                 'it is a reasonable heuristic.) The code below defines three '
                 'SMARTS queries that capture a flavone substructure (the '
                 '2-phenylchromen-4-one skeleton), a flavanone substructure '
                 '(with a saturated central ring and a carbonyl) and a '
                 'flavanol substructure (a variant with a hydroxyl rather than '
                 'a carbonyl). It then returns True if the input molecule '
                 'contains any one of these motifs, and otherwise explains '
                 'that no recognizable flavonoid scaffold was found.\n'
                 '\n'
                 'Below is the complete Python code:',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 349,
    'num_false_positives': 262,
    'num_true_negatives': 140657,
    'num_false_negatives': 1032,
    'num_negatives': None,
    'precision': 0.5711947626841244,
    'recall': 0.25271542360608257,
    'f1': 0.35040160642570284,
    'accuracy': 0.9909065354884048,
    'negative_predictive_value': 0.9927164423490885}