"""
Classifies: CHEBI:38757 isoflavones
"""
"""
Classifies: Isoflavones – any isoflavonoid with a 3-aryl-1-benzopyran-4-one (3-aryl-4H-chromen-4-one) skeleton and its substituted derivatives.
"""

from rdkit import Chem

def is_isoflavones(smiles: str):
    """
    Determines if a molecule is an isoflavone 
    (i.e. an isoflavonoid with a 3-aryl-1-benzopyran-4-one skeleton)
    based on its SMILES string.

    Our two-part strategy is:
      1. Identify a benzopyran-4-one (chromen-4-one) core.
         Here we use a SMARTS that is a bit more permissive than the previous attempt.
         The pattern "c1coc2c(c1=O)cccc2" should capture the bicyclic core even if substituted.
      2. Identify an attached phenyl (aromatic benzene) that is linked to the core via a non-ring bond.
         The rationale is that an isoflavone has a 3-aryl substituent attached by a single bond 
         (as opposed to being fused into the core). 

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is classified as an isoflavone, False otherwise.
        str: Reason for the classification decision.
    """
    # Parse the SMILES into an RDKit Mol object.
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
    
    # Define a more permissive SMARTS for the benzopyran-4-one core.
    # This pattern is intended to capture a 1-benzopyran-4-one (chromen-4-one) scaffold
    # even if extra substituents are present on the aromatic rings.
    core_smarts = "c1coc2c(c1=O)cccc2"
    core_query = Chem.MolFromSmarts(core_smarts)
    if core_query is None:
        return False, "Error constructing SMARTS for benzopyran-4-one core"
    
    # Find matches of the core in the molecule.
    core_matches = mol.GetSubstructMatches(core_query)
    if not core_matches:
        return False, "Molecule does not contain the benzopyran-4-one (chromen-4-one) core"
    
    # Collect all atom indices that are in some core match.
    core_atoms = set()
    for match in core_matches:
        core_atoms.update(match)
    
    # Define a SMARTS for a phenyl (benzene) ring.
    phenyl_smarts = "c1ccccc1"
    phenyl_query = Chem.MolFromSmarts(phenyl_smarts)
    if phenyl_query is None:
        return False, "Error constructing SMARTS for phenyl group"
    
    # Find all phenyl substructure matches.
    phenyl_matches = mol.GetSubstructMatches(phenyl_query)
    if not phenyl_matches:
        return False, "Molecule has the core but no phenyl (aryl) substituent found"
    
    # Check if any phenyl ring is attached to the benzopyran-4-one core by a single (non-fused) bond.
    # We iterate over each phenyl match and for each atom in the phenyl, we look for a neighbor that is in the core.
    # We also check that the bond connecting them is NOT in a ring.
    for phenyl in phenyl_matches:
        phenyl_set = set(phenyl)
        for idx in phenyl_set:
            atom = mol.GetAtomWithIdx(idx)
            for nbr in atom.GetNeighbors():
                nbr_idx = nbr.GetIdx()
                # Look for a neighbor that is in the core (but not part of the phenyl ring itself)
                if nbr_idx in core_atoms and nbr_idx not in phenyl_set:
                    bond = mol.GetBondBetweenAtoms(idx, nbr_idx)
                    # Accept only if the attaching bond is not fused (i.e. not in any ring)
                    if bond is not None and not bond.IsInRing():
                        return True, "Molecule contains the benzopyran-4-one core with an appropriately attached (non-fused) aryl substituent"
    
    return False, "Molecule contains the benzopyran-4-one core but lacks a properly attached (non-fused) 3-aryl substituent"

# Example usage (for testing purposes):
if __name__ == "__main__":
    # Test with daidzein (an isoflavone) SMILES
    test_smiles = "Oc1ccc(cc1)-c1coc2cc(O)ccc2c1=O"
    result, reason = is_isoflavones(test_smiles)
    print("Result:", result)
    print("Reason:", reason)


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:38757',
                          'name': 'isoflavones',
                          'definition': 'Any isoflavonoid with a '
                                        '3-aryl-1-benzopyran-4-one '
                                        '(3-aryl-4H-chromen-4-one) skeleton '
                                        'and its substituted derivatives.',
                          'parents': ['CHEBI:3992', 'CHEBI:50753'],
                          'xrefs': ['MetaCyc:Isoflavones'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 66,
                           'log_lines_of_code': 4.189654742026425,
                           'indent_by_line': [   1,
                                                 1,
                                                 1,
                                                 1,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
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
                                                 1,
                                                 1,
                                                 1,
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
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 3,
                                                 3,
                                                 4,
                                                 4,
                                                 4,
                                                 5,
                                                 5,
                                                 5,
                                                 6,
                                                 1,
                                                 1,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1],
                           'max_indent': 6,
                           'imports': ['from rdkit import Chem'],
                           'imports_count': 1,
                           'methods_called': [   'GetNeighbors',
                                                 'MolFromSmarts',
                                                 'GetIdx',
                                                 'update',
                                                 'IsInRing',
                                                 'GetSubstructMatches',
                                                 'GetAtomWithIdx',
                                                 'MolFromSmiles',
                                                 'GetBondBetweenAtoms'],
                           'methods_called_count': 9,
                           'smarts_strings': ['phenyl_smarts', 'core_smarts'],
                           'smarts_strings_count': 2,
                           'defs': ['is_isoflavones(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "Error constructing SMARTS '
                                          'for benzopyran-4-one core"',
                                          'False, "Molecule does not contain '
                                          'the benzopyran-4-one '
                                          '(chromen-4-one) core"',
                                          'False, "Error constructing SMARTS '
                                          'for phenyl group"',
                                          'False, "Molecule has the core but '
                                          'no phenyl (aryl) substituent found"',
                                          'True, "Molecule contains the '
                                          'benzopyran-4-one core with an '
                                          'appropriately attached (non-fused) '
                                          'aryl substituent"',
                                          'False, "Molecule contains the '
                                          'benzopyran-4-one core but lacks a '
                                          'properly attached (non-fused) '
                                          '3-aryl substituent"'],
                           'returns_count': 7,
                           'complexity': 5.437930948405286},
    'message': '\n'
               'Attempt failed: F1 score of 0 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: NONE\n'
               'False positives: SMILES: '
               'O=C1OC2=C(C3=NC=4C=CC=CC4N(C3=CC2=C1C5=CC=CC=C5)C/C=C(\\CCC=C(C)C)/C)C(=O)O '
               'NAME: Benthocyanin B REASON: WRONGLY CLASSIFIED Molecule '
               'contains the benzopyran-4-one core with an attached aryl '
               'substituent\n'
               ' * SMILES: '
               'O=C1OC2=CC3=NC=4C(C(=O)O)=CC=CC4N(C3=CC2=C1C5=CC=CC=C5)CC=C(CCC=C(C)C)C '
               'NAME: Benthocyanin A REASON: WRONGLY CLASSIFIED Molecule '
               'contains the benzopyran-4-one core with an attached aryl '
               'substituent\n'
               'False negatives: SMILES: '
               'CC(C)=CCc1c(O)ccc(c1O)-c1coc2cc(O)cc(O)c2c1=O NAME: '
               'licoisoflavone A REASON: MISSED Molecule does not contain the '
               '1-benzopyran-4-one (benzopyranone) core\n'
               ' * SMILES: '
               'COC1=C(CC=C(C)C)C(=C(O)C=C1O)C1=COC2=CC(O)=CC=C2C1=O NAME: '
               'kwakhurin REASON: MISSED Molecule does not contain the '
               '1-benzopyran-4-one (benzopyranone) core\n'
               ' * SMILES: '
               'CC(C)=CCc1c(O)c(CC(O)C(C)=C)c(O)c2c1occ(-c1ccc(O)c(O)c1)c2=O '
               'NAME: millewanin G REASON: MISSED Molecule does not contain '
               'the 1-benzopyran-4-one (benzopyranone) core\n'
               ' * SMILES: O1C=2C(C(=O)C(C3=C(O)C=C(OC)C=C3)=C1)=C(O)C=C(OC)C2 '
               "NAME: 2',5-Dihydroxy-4',7-dimethoxyisoflavone REASON: MISSED "
               'Molecule does not contain the 1-benzopyran-4-one '
               '(benzopyranone) core\n'
               ' * SMILES: '
               'O1C2=C(CC=C(C)C)C(O)=CC(O)=C2C(=O)C(C3=CC=C(OC)C=C3)=C1 NAME: '
               'Gancaonin M REASON: MISSED Molecule does not contain the '
               '1-benzopyran-4-one (benzopyranone) core\n'
               ' * SMILES: '
               'O1C2=C(C/C=C(/CO)\\C)C(O)=CC(O)=C2C(=O)C(C3=C(O)C=C(O)C=C3)=C1 '
               'NAME: 2,3-Dehydrokievitol REASON: MISSED Molecule does not '
               'contain the 1-benzopyran-4-one (benzopyranone) core\n'
               ' * SMILES: COc1c(O)cc(cc1CC=C(C)C)-c1coc2cc(O)ccc2c1=O NAME: '
               'erylatissin A REASON: MISSED Molecule does not contain the '
               '1-benzopyran-4-one (benzopyranone) core\n'
               ' * SMILES: '
               'BrC1=C2OC=C(C3=CC(Br)=C(O)C(=C3)Br)C(C2=CC(=C1OC)O)=O NAME: '
               'Maduraktermol K REASON: MISSED Molecule does not contain the '
               '1-benzopyran-4-one (benzopyranone) core\n'
               ' * SMILES: O1C2=C(C(=O)C(C3=CC=4OCOC4C=C3)=C1)C=CC=5OCOC25 '
               'NAME: Maximaisoflavone A REASON: MISSED Molecule does not '
               'contain the 1-benzopyran-4-one (benzopyranone) core\n'
               ' * SMILES: COc1cc(cc(OC)c1OC)-c1coc2cc3OCOc3c(OC)c2c1=O NAME: '
               'Irisflorentin REASON: MISSED Molecule does not contain the '
               '1-benzopyran-4-one (benzopyranone) core\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'O=C(N1[C@H](CCC1)C(O)=O)[C@@H](NC(=O)[C@@H](N)CC(O)=O)CCC(=O)N',
                                     'name': 'Asp-Gln-Pro',
                                     'reason': 'Molecule does not contain the '
                                               'benzopyran-4-one '
                                               '(chromen-4-one) core'},
                                 {   'smiles': 'O1C=2C(C(O)=C(CC3=C(O)C=4C(OC3=O)=CC=CC4C)C1=O)=C(C=CC2)C',
                                     'name': 'Gerberinol',
                                     'reason': 'Molecule does not contain the '
                                               'benzopyran-4-one '
                                               '(chromen-4-one) core'},
                                 {   'smiles': 'O=C(O)/C(=C/[C@H]1C=C(CC[C@@H]1C(C)C)CO)/COC(=O)C',
                                     'name': '3-acetylgliocladic acid',
                                     'reason': 'Molecule does not contain the '
                                               'benzopyran-4-one '
                                               '(chromen-4-one) core'},
                                 {   'smiles': 'O=C(CCCCCCCCC)C=1C=CC(=NC1)CCCCCCCCC',
                                     'name': '1-(6-Nonylpyridin-3-yl)decan-1-one',
                                     'reason': 'Molecule does not contain the '
                                               'benzopyran-4-one '
                                               '(chromen-4-one) core'},
                                 {   'smiles': 'CCC(=O)O[C@H]1[C@H](C)O[C@H](C[C@@]1(C)O)O[C@@H]1[C@@H](C)O[C@@H](O[C@H]2[C@@H](CC=O)C[C@@H](C)[C@@H](O)\\C=C\\C=C\\C[C@@H](C)OC(=O)C[C@@H](O)[C@@H]2OC)[C@H](O)[C@H]1N(C)C',
                                     'name': 'Leucomycin A7',
                                     'reason': 'Molecule does not contain the '
                                               'benzopyran-4-one '
                                               '(chromen-4-one) core'},
                                 {   'smiles': 'C[C@H]1O[C@H](C[C@@H](O)[C@@H]1O)c1ccc2C(=O)C3=C([C@H](O)C[C@]4(O)C[C@@](C)(O)CC(=O)[C@]34O)C(=O)c2c1O',
                                     'name': 'Urdamycinone F',
                                     'reason': 'Molecule does not contain the '
                                               'benzopyran-4-one '
                                               '(chromen-4-one) core'},
                                 {   'smiles': 'CC(C)=CCC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\COP([O-])(=O)OP([O-])([O-])=O',
                                     'name': 'all-trans-dodecaprenyl '
                                             'diphosphate(3-)',
                                     'reason': 'Molecule does not contain the '
                                               'benzopyran-4-one '
                                               '(chromen-4-one) core'},
                                 {   'smiles': '[O-][N+](=O)N1CN(CN(CN(C1)[N+]([O-])=O)[N+]([O-])=O)[N+]([O-])=O',
                                     'name': 'octogen',
                                     'reason': 'Molecule does not contain the '
                                               'benzopyran-4-one '
                                               '(chromen-4-one) core'},
                                 {   'smiles': 'CC(=O)NCCC[NH2+]CCCC[NH2+]CCCNC(C)=O',
                                     'name': 'N(1),N(12)-diacetylsperminium(2+)',
                                     'reason': 'Molecule does not contain the '
                                               'benzopyran-4-one '
                                               '(chromen-4-one) core'},
                                 {   'smiles': 'C[C@@H]([C@H]1CC[C@H]2[C@H](CCc3cc(O)ccc3C)C(=O)CC[C@]12C)C(O)=O',
                                     'name': '3-hydroxy-9-oxo-9,10-seco-23,24-bisnorchola-1,3,5(10)-trien-22-oic '
                                             'acid',
                                     'reason': 'Molecule does not contain the '
                                               'benzopyran-4-one '
                                               '(chromen-4-one) core'}],
    'sample_false_negatives': [   {   'smiles': 'O=C1C=2C3=C(O)C=C(C)C=C3C=CC2OC4=C1C=CC(=C4O)[C@@H]5O[C@H]([C@@H](N(C)C)CC5)C',
                                      'name': 'Monacyclinone G',
                                      'reason': 'Molecule contains the '
                                                'benzopyran-4-one core but '
                                                'lacks a properly attached '
                                                '(non-fused) 3-aryl '
                                                'substituent'},
                                  {   'smiles': 'CC(C)=CCc1c(O)ccc(C2COc3cc(O)cc(O)c3C2=O)c1O',
                                      'name': 'dihydrolicoisoflavone A',
                                      'reason': 'Molecule does not contain the '
                                                'benzopyran-4-one '
                                                '(chromen-4-one) core'},
                                  {   'smiles': 'C=1(C=C(C=CC1O)CC(CCC(OS(=O)(O)=O)=O)O)O',
                                      'name': '4-hydroxy-5-(dihydroxyphenyl)-valeric '
                                              'acid-O-sulphate',
                                      'reason': 'Molecule does not contain the '
                                                'benzopyran-4-one '
                                                '(chromen-4-one) core'},
                                  {   'smiles': 'C=1(C=C(C=C(C1O)O)CC2OC(CC2)=O)OC3[C@@H]([C@H]([C@@H]([C@H](O3)C(O)=O)O)O)O',
                                      'name': "5-(3',4',5'-Trihydroxyphenyl)-gamma-valerolactone-3'-O-glucuronide",
                                      'reason': 'Molecule does not contain the '
                                                'benzopyran-4-one '
                                                '(chromen-4-one) core'},
                                  {   'smiles': 'COC1=CC(=O)C(=CC1=O)c1coc2cc(O)ccc2c1=O',
                                      'name': 'bowdichione',
                                      'reason': 'Molecule contains the '
                                                'benzopyran-4-one core but '
                                                'lacks a properly attached '
                                                '(non-fused) 3-aryl '
                                                'substituent'},
                                  {   'smiles': 'C=1(C2C(C=CC1O)C(C(=CO2)C=3C=CC(=CC3)O)=O)[C@@H]4O[C@@H]([C@H](C([C@H]4O)=O)O)CO',
                                      'name': "3''-oxopuearin",
                                      'reason': 'Molecule does not contain the '
                                                'benzopyran-4-one '
                                                '(chromen-4-one) core'},
                                  {   'smiles': 'C=1(C(=C(C=CC1)O)O)OS(=O)(=O)O',
                                      'name': 'Pyrogallol-1-O-sulphate',
                                      'reason': 'Molecule does not contain the '
                                                'benzopyran-4-one '
                                                '(chromen-4-one) core'},
                                  {   'smiles': 'CC1(C)CCc2c(O)ccc(C3COc4cc(O)cc(O)c4C3=O)c2O1',
                                      'name': 'glyasperin F',
                                      'reason': 'Molecule does not contain the '
                                                'benzopyran-4-one '
                                                '(chromen-4-one) core'},
                                  {   'smiles': 'C=1(C=C(C=CC1O)CC(CCC(OCOS(=O)(=O)O)=O)O)O',
                                      'name': '4-Hydroxy-5-(dihydroxyphenyl)-valeric '
                                              'acid-O-methyl-O-sulphate',
                                      'reason': 'Molecule does not contain the '
                                                'benzopyran-4-one '
                                                '(chromen-4-one) core'}],
    'attempt': 2,
    'reasoning': 'Below is my reasoning before the code:\n'
                 '\n'
                 'One probable reason for the previous failure is that the '
                 'SMARTS used to “find” the benzopyran‐4‐one core was too '
                 'strict and did not capture many isoflavone derivatives. '
                 'Furthermore, simply requiring that a phenyl ring be directly '
                 'bonded to any core atom allows mis‐classification of '
                 'molecules in which the “aryl” part is actually fused to the '
                 'core (as in the benthocyanins). To improve on this, we use a '
                 'more permissive SMARTS for the benzopyran-4-one '
                 '(chromen-4-one) scaffold – for example, one that accepts '
                 'extra substituents on the core ring system. Moreover, when '
                 'looking for the 3-aryl substitution we now require that the '
                 'substituent phenyl ring is attached by a bond that is NOT '
                 'part of any ring (thus ruling out cases where the phenyl '
                 'appears as a fused component of the core).\n'
                 '\n'
                 'Below is the complete improved Python program.',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 181,
    'num_false_positives': 1755,
    'num_true_negatives': 140355,
    'num_false_negatives': 9,
    'num_negatives': None,
    'precision': 0.09349173553719008,
    'recall': 0.9526315789473684,
    'f1': 0.1702728127939793,
    'accuracy': 0.9876036542515811,
    'negative_predictive_value': 0.999935880995127}