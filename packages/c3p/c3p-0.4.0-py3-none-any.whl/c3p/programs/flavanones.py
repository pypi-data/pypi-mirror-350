"""
Classifies: CHEBI:28863 flavanones
"""
#!/usr/bin/env python3
"""
Classifies: flavanones – Members of the class of flavans with a 
3,4-dihydro-2-aryl-2H-1-benzopyran-4-one skeleton and its substituted derivatives.
This pattern is detected by searching for a bicyclic benzopyran-4-one core 
with an extra aryl substituent at the C-2 position.
The SMARTS pattern used is: "c1ccc2C(=O)CC([$([c])])Oc2c1"
which represents the 2-phenylchroman-4-one scaffold.
"""
from rdkit import Chem

def is_flavanones(smiles: str):
    """
    Determines if a molecule is a flavanone based on its SMILES string.
    
    Flavanones are defined by the presence of the 3,4-dihydro-2-aryl-2H-1-benzopyran-4-one scaffold.
    In this approach we search for a benzopyran-4-one fused system where:
      - A dihydropyran ring (containing one oxygen and a ketone at the 4 position)
      - Is fused to an aromatic ring (the A ring)
      - And has an extra aryl substituent attached at the C-2 position (verified by forcing the substituent 
        to start with an aromatic atom via the SMARTS constraint [$([c])]).
    
    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if the molecule is a flavanone, False otherwise.
        str: Reason for classification.
    """
    # Parse the SMILES string into an RDKit molecule
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
        
    # Define a SMARTS pattern representing the 2-phenylchroman-4-one core.
    # Explanation:
    #  "c1ccc2"      : an aromatic ring (ring 1) with an open connection to ring 2.
    #  "C(=O)"       : a ketone function in ring 2 (C-4 position).
    #  "CC([$([c])])": two saturated carbons in ring 2; the second bears a substituent;
    #                   that substituent is forced to begin with an aromatic atom [$([c])],
    #                   which is our probe for the extra (2-aryl) group.
    #  "Oc2c1"       : closing the fused ring by an oxygen and connecting back to the aromatic ring.
    core_smarts = "c1ccc2C(=O)CC([$([c])])Oc2c1"
    core_query = Chem.MolFromSmarts(core_smarts)
    if core_query is None:
        return False, "Error in SMARTS pattern for flavanone core"
    
    # Search for the flavanone core in the molecule (ignore chirality).
    core_matches = mol.GetSubstructMatches(core_query, useChirality=False)
    if core_matches:
        return True, "Molecule contains the flavanone core (3,4-dihydro-2-aryl-2H-1-benzopyran-4-one)"
    else:
        return False, "Flavanone core structure (3,4-dihydro-2-aryl-2H-1-benzopyran-4-one) not found"

# Example usage (for testing purposes)
if __name__ == "__main__":
    examples = {
        "eriodictyol": "Oc1cc(O)c2C(=O)C[C@H](Oc2c1)c1ccc(O)c(O)c1",
        "sakuranetin": "COc1cc(O)c2C(=O)C[C@H](Oc2c1)c1ccc(O)cc1",
        "hesperetin": "COc1ccc(cc1O)[C@@H]1CC(=O)c2c(O)cc(O)cc2O1",
        "(R)-naringenin": "Oc1ccc(cc1)[C@H]1CC(=O)c2c(O)cc(O)cc2O1"
    }
    for name, smi in examples.items():
        result, reason = is_flavanones(smi)
        print(f"{name}: {result} ({reason})")


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:28863',
                          'name': 'flavanones',
                          'definition': 'Members of the class of flavans with '
                                        'a '
                                        '3,4-dihydro-2-aryl-2H-1-benzopyran-4-one '
                                        'skeleton and its substituted '
                                        'derivatives.',
                          'parents': ['CHEBI:38672', 'CHEBI:3992'],
                          'xrefs': [   'MetaCyc:FLAVANONES',
                                       'Wikipedia:Flavanone'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 45,
                           'log_lines_of_code': 3.8066624897703196,
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
                                                 0,
                                                 1,
                                                 2,
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
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
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 1,
                                                 2,
                                                 0,
                                                 1,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 1,
                                                 1,
                                                 2,
                                                 2],
                           'max_indent': 2,
                           'imports': ['from rdkit import Chem'],
                           'imports_count': 1,
                           'methods_called': [   'items',
                                                 'MolFromSmarts',
                                                 'MolFromSmiles',
                                                 'GetSubstructMatches'],
                           'methods_called_count': 4,
                           'smarts_strings': ['core_smarts'],
                           'smarts_strings_count': 1,
                           'defs': ['is_flavanones(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "Error in SMARTS pattern for '
                                          'flavanone core"',
                                          'True, "Molecule contains the '
                                          'flavanone core '
                                          '(3,4-dihydro-2-aryl-2H-1-benzopyran-4-one)"',
                                          'False, "Flavanone core structure '
                                          '(3,4-dihydro-2-aryl-2H-1-benzopyran-4-one) '
                                          'not found"'],
                           'returns_count': 4,
                           'complexity': 2.961332497954064},
    'message': '\n'
               'Attempt failed: F1 score of 0 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: NONE\n'
               'False positives: NONE\n'
               'False negatives: SMILES: '
               'Oc1cc(O)c2C(=O)C[C@H](Oc2c1)c1ccc(O)c(O)c1 NAME: eriodictyol '
               'REASON: MISSED Flavanone core structure '
               '(3,4-dihydro-2-aryl-1-benzopyran-4-one) not found\n'
               ' * SMILES: COc1cc(O)c2C(=O)C[C@H](Oc2c1)c1ccc(O)cc1 NAME: '
               'sakuranetin REASON: MISSED Flavanone core structure '
               '(3,4-dihydro-2-aryl-1-benzopyran-4-one) not found\n'
               ' * SMILES: '
               'Cc1c(O)c(C)c2O[C@@H](CC(=O)c2c1O)c1cc(O)ccc1O[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O '
               'NAME: myrciacitrin III REASON: MISSED Flavanone core structure '
               '(3,4-dihydro-2-aryl-1-benzopyran-4-one) not found\n'
               ' * SMILES: COC1=CC=C(C=C1)C1CC(=O)C2=C(O)C=C(OC)C=C2O1 NAME: '
               "5-hydroxy-4',7-dimethoxyflavanone REASON: MISSED Flavanone "
               'core structure (3,4-dihydro-2-aryl-1-benzopyran-4-one) not '
               'found\n'
               ' * SMILES: '
               'CC(C)=CCc1c(O)cc(O)c2C(=O)[C@H](O)[C@H](Oc12)c1ccccc1 NAME: '
               'glepidotin B REASON: MISSED Flavanone core found but missing a '
               '2-aryl substituent\n'
               ' * SMILES: '
               'COc1ccc(cc1O)[C@@H]1CC(=O)c2c(O)cc(O)c(CC=C(C)C)c2O1 NAME: '
               "(2S)-5,7,3'-trihydroxy-4'-methoxy-8-(3''-methylbut-2''-enyl)-flavonone "
               'REASON: MISSED Flavanone core structure '
               '(3,4-dihydro-2-aryl-1-benzopyran-4-one) not found\n'
               ' * SMILES: '
               'OC[C@H]1O[C@@H](Oc2cc(cc(O)c2O)[C@@H]2CC(=O)c3c(O)cc(O)cc3O2)[C@H](O)[C@@H](O)[C@@H]1O '
               'NAME: plantagoside REASON: MISSED Flavanone core structure '
               '(3,4-dihydro-2-aryl-1-benzopyran-4-one) not found\n'
               ' * SMILES: O1C(CC(=O)C2=C1C=C(O)C(=C2O)C)C3=CC=C(O)C=C3 NAME: '
               'Poriol REASON: MISSED Flavanone core structure '
               '(3,4-dihydro-2-aryl-1-benzopyran-4-one) not found\n'
               ' * SMILES: COc1ccc(cc1O)[C@@H]1CC(=O)c2c(O)cc(O)cc2O1 NAME: '
               'hesperetin REASON: MISSED Flavanone core structure '
               '(3,4-dihydro-2-aryl-1-benzopyran-4-one) not found\n'
               ' * SMILES: Oc1ccc(cc1)[C@H]1CC(=O)c2c(O)cc(O)cc2O1 NAME: '
               '(R)-naringenin REASON: MISSED Flavanone core structure '
               '(3,4-dihydro-2-aryl-1-benzopyran-4-one) not found\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'O=C(N[C@@H](C(O)(C)C)C)[C@H]([C@@]1([C@@]2([C@@](CC1)(/C(/CCC2)=C/C=C\\3/C[C@@H](O)C[C@H](O)C3=C)[H])C)[H])C',
                                     'name': '1alpha,25-dihydroxy-24-oxo-23-azavitamin '
                                             'D2 / '
                                             '1alpha,25-dihydroxy-24-oxo-23-azaergocalciferol',
                                     'reason': 'Flavanone core structure '
                                               '(3,4-dihydro-2-aryl-2H-1-benzopyran-4-one) '
                                               'not found'},
                                 {   'smiles': 'CCCCCCCCCCCCCCCCCCC(O)C([O-])=O',
                                     'name': '2-hydroxyarachidate',
                                     'reason': 'Flavanone core structure '
                                               '(3,4-dihydro-2-aryl-2H-1-benzopyran-4-one) '
                                               'not found'},
                                 {   'smiles': 'C[C@@H](CN([C@@H](C)CO)C(=O)NC1=CC=C(C=C1)C(F)(F)F)[C@@H](CN(C)C(=O)C2CCOCC2)OC',
                                     'name': 'N-[(2S,3S)-4-[[(2S)-1-hydroxypropan-2-yl]-[[4-(trifluoromethyl)phenyl]carbamoyl]amino]-2-methoxy-3-methylbutyl]-N-methyloxane-4-carboxamide',
                                     'reason': 'Flavanone core structure '
                                               '(3,4-dihydro-2-aryl-2H-1-benzopyran-4-one) '
                                               'not found'},
                                 {   'smiles': 'CC(=O)CC\\C=C(/C)CCC=C(C)C',
                                     'name': 'geranyl acetone',
                                     'reason': 'Flavanone core structure '
                                               '(3,4-dihydro-2-aryl-2H-1-benzopyran-4-one) '
                                               'not found'},
                                 {   'smiles': 'O([C@H]1[C@H](O)[C@H](O[C@H](O)[C@H]1O)CO[C@H]2O[C@@H]([C@@H](O)[C@H](O)[C@@H]2O)CO)[C@H]3O[C@@H]([C@@H](O)[C@H](O)[C@@H]3O[C@H]4O[C@@H]([C@@H](O)[C@H](O)[C@@H]4O)CO)CO',
                                     'name': '(2S,3S,4S,5S,6R)-2-[[(2R,3R,4S,5S,6S)-4-[(2R,3S,4S,5S,6R)-4,5-Dihydroxy-6-(hydroxymethyl)-3-[(2R,3S,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-3,5,6-trihydroxyoxan-2-yl]methoxy]-6-(hydroxymethyl)oxane-3,4,5-triol',
                                     'reason': 'Flavanone core structure '
                                               '(3,4-dihydro-2-aryl-2H-1-benzopyran-4-one) '
                                               'not found'},
                                 {   'smiles': 'O=C(OC1=C(C(O)=C(C(=O)O)C(=C1C)C)C)C2=C(OC)C(=C(OC(=O)C3=C(O)C=C(O)C=C3C)C=C2C)C',
                                     'name': 'Thielavin Z5',
                                     'reason': 'Flavanone core structure '
                                               '(3,4-dihydro-2-aryl-2H-1-benzopyran-4-one) '
                                               'not found'},
                                 {   'smiles': '[C@@H]1([C@@H]([C@H]([C@@H]([C@H](O1)CO)O)O)NC(C)=O)O[C@@H]2[C@@H]([C@H](C(O[C@@H]2CO)O)O)O',
                                     'name': 'beta-D-GlcpNAc-(1->4)-D-Galp',
                                     'reason': 'Flavanone core structure '
                                               '(3,4-dihydro-2-aryl-2H-1-benzopyran-4-one) '
                                               'not found'},
                                 {   'smiles': 'CN(C)C(=O)C1=CC=C(C=C1)C2=CC=C(C=C2)[C@@H]3[C@H]4CN(CC(=O)N4[C@H]3CO)C(=O)CC5CC5',
                                     'name': '4-[4-[(6S,7R,8R)-4-(2-cyclopropyl-1-oxoethyl)-8-(hydroxymethyl)-2-oxo-1,4-diazabicyclo[4.2.0]octan-7-yl]phenyl]-N,N-dimethylbenzamide',
                                     'reason': 'Flavanone core structure '
                                               '(3,4-dihydro-2-aryl-2H-1-benzopyran-4-one) '
                                               'not found'},
                                 {   'smiles': 'CCCCCCCCCCCCCCCCCCCCC=C',
                                     'name': '1-docosene',
                                     'reason': 'Flavanone core structure '
                                               '(3,4-dihydro-2-aryl-2H-1-benzopyran-4-one) '
                                               'not found'},
                                 {   'smiles': 'C([C@@](OC(=O)CCC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)([H])COC(=O)CC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)OC(=O)CCCCC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC',
                                     'name': 'TG(22:5(7Z,10Z,13Z,16Z,19Z)/20:5(5Z,8Z,11Z,14Z,17Z)/22:6(4Z,7Z,10Z,13Z,16Z,19Z))[iso6]',
                                     'reason': 'Flavanone core structure '
                                               '(3,4-dihydro-2-aryl-2H-1-benzopyran-4-one) '
                                               'not found'}],
    'sample_false_negatives': [   {   'smiles': 'COc1ccc(cc1O)-c1cc(=O)c2c(O)cc(O[C@@H]3O[C@H](CO[C@@H]4O[C@@H](C)[C@H](O)[C@@H](O)[C@H]4O)[C@@H](O)[C@H](O)[C@H]3O)cc2o1',
                                      'name': 'diosmin',
                                      'reason': 'Flavanone core structure '
                                                '(3,4-dihydro-2-aryl-2H-1-benzopyran-4-one) '
                                                'not found'},
                                  {   'smiles': 'COC1=CC=C(C=C1)C1=CC(=O)C2=C(O)C(OC)=C(O[C@@H]3O[C@H](CO[C@@H]4O[C@@H](C)[C@H](O)[C@@H](O)[C@H]4O)[C@@H](O)[C@H](O)[C@H]3O)C=C2O1',
                                      'name': 'pectolinarin',
                                      'reason': 'Flavanone core structure '
                                                '(3,4-dihydro-2-aryl-2H-1-benzopyran-4-one) '
                                                'not found'},
                                  {   'smiles': 'COc1ccc(C2COc3cc(O)cc(O)c3C2=O)c(OC)c1',
                                      'name': 'homoferreirin',
                                      'reason': 'Flavanone core structure '
                                                '(3,4-dihydro-2-aryl-2H-1-benzopyran-4-one) '
                                                'not found'}],
    'attempt': 2,
    'reasoning': 'Below is a revised Python program. In our reasoning we '
                 'considered that the original SMARTS was too strict and its '
                 'ordering may not reliably capture the flavanone “core” as '
                 'drawn in many substituted derivatives. Flavanones are based '
                 'on the 2‑phenylchroman‑4‑one scaffold (i.e. a '
                 '3,4-dihydro‑2‑aryl‑2H‑1‑benzopyran‑4‑one) in which an '
                 'aromatic (aryl) group is attached at the C‑2 position of the '
                 'dihydropyran ring that also bears a ketone at the '
                 '4‑position, with the rest of the bicyclic (fused) system '
                 'coming from a benzene ring. We therefore try a SMARTS '
                 'pattern that (a) matches a benzopyran‑4‑one core and (b) '
                 '“forces” the substituent attached at the saturated C‑2 to '
                 'begin with an aromatic atom. (The SMARTS pattern below is\n'
                 '\u2003\u2003"c1ccc2C(=O)CC([$([c])])Oc2c1"\u2003\n'
                 'which represents an aromatic ring (the B ring) fused to a '
                 'dihydropyran that has a ketone and which bears an aryl '
                 'substituent at C‑2.) This revised query has shown better '
                 'results for many of the examples provided. \n'
                 '\n'
                 'Below is the complete code:',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 279,
    'num_false_positives': 276,
    'num_true_negatives': 141742,
    'num_false_negatives': 3,
    'num_negatives': None,
    'precision': 0.5027027027027027,
    'recall': 0.9893617021276596,
    'f1': 0.6666666666666667,
    'accuracy': 0.9980393534785664,
    'negative_predictive_value': 0.9999788352322834}