"""
Classifies: CHEBI:133004 bisbenzylisoquinoline alkaloid
"""
"""
Classifies: Bisbenzylisoquinoline alkaloid
Definition: A benzylisoquinoline alkaloid whose structures are built up of two benzylisoquinoline units 
linked by ether bridges. Additional bridging patterns (direct C–C linking or methylenedioxy groups)
are common.
"""
from rdkit import Chem

def is_bisbenzylisoquinoline_alkaloid(smiles: str):
    """
    Determines if a molecule is a bisbenzylisoquinoline alkaloid based on its SMILES string.
    
    Strategy:
      1. Parse and remove stereochemistry to allow flexible matching.
      2. Use a relaxed SMARTS pattern for a benzylisoquinoline unit. We use the pattern:
             "c1ccc2c(c1)CCNC2"
         This pattern represents an aromatic ring fused to a saturated ring containing nitrogen.
         We count distinct (non-overlapping) occurrences and require at least two.
      3. Check for the presence of bridging groups that link the two units.
         We accept either an aromatic ether bridge (pattern "[a]-O-[a]") or a methylenedioxy bridge
         ("cO[CH2]Oc").
    
    Args:
        smiles (str): SMILES string of the molecule.
        
    Returns:
        bool: True if the molecule is classified as a bisbenzylisoquinoline alkaloid, False otherwise.
        str: Reason for the classification.
    """
    # Parse SMILES string into a molecule object
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
    
    # Remove stereochemical information to be more permissive with the match.
    Chem.RemoveStereochemistry(mol)
    
    # Define a relaxed SMARTS pattern for a benzylisoquinoline unit.
    # This pattern looks for an aromatic ring fused with a saturated ring that contains a nitrogen.
    benzylisoquinoline_smarts = "c1ccc2c(c1)CCNC2"
    benzylisoquinoline_pattern = Chem.MolFromSmarts(benzylisoquinoline_smarts)
    if benzylisoquinoline_pattern is None:
        return False, "Error in benzylisoquinoline SMARTS"
    
    # Get all substructure matches and filter for distinct (non-overlapping) matches.
    iso_matches = mol.GetSubstructMatches(benzylisoquinoline_pattern)
    distinct_units = []
    for match in iso_matches:
        match_set = set(match)
        if not any(match_set & existing for existing in distinct_units):
            distinct_units.append(match_set)
    
    # Require at least 2 distinct benzylisoquinoline units.
    if len(distinct_units) < 2:
        return False, f"Found {len(distinct_units)} benzylisoquinoline unit(s); need at least 2"
    
    # Check for bridging groups linking the two units.
    # Aromatic ether bridge: an oxygen bridging two aromatic atoms.
    aromatic_ether_smarts = "[a]-O-[a]"
    aromatic_ether = Chem.MolFromSmarts(aromatic_ether_smarts)
    
    # Methylenedioxy bridge: pattern representing a -OCH2O- bridge between two aromatic rings.
    methylenedioxy_smarts = "cO[CH2]Oc"
    methylenedioxy = Chem.MolFromSmarts(methylenedioxy_smarts)
    
    has_bridge = mol.HasSubstructMatch(aromatic_ether) or mol.HasSubstructMatch(methylenedioxy)
    if not has_bridge:
        return False, "No bridging group (aromatic ether or methylenedioxy) linking the benzylisoquinoline units found"
    
    # If both conditions are satisfied, we classify the molecule as a bisbenzylisoquinoline alkaloid.
    return True, "Contains at least two benzylisoquinoline units bridged by an appropriate group"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:133004',
                          'name': 'bisbenzylisoquinoline alkaloid',
                          'definition': 'A type of benzylisoquinoline alkaloid '
                                        'whose structures are built up of two '
                                        'benzylisoquinoline units linked by '
                                        'ether bridges. Various structural '
                                        'patterns resulting from additional '
                                        'bridging between the two units by '
                                        'direct carbon-carbon bridging or by '
                                        'methylenedioxy groups are common.',
                          'parents': ['CHEBI:22750'],
                          'xrefs': [   'PMID:1955879',
                                       'PMID:2191354',
                                       'PMID:3323421'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 51,
                           'log_lines_of_code': 3.9318256327243257,
                           'indent_by_line': [   1,
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
                                                 2,
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
                                                 2,
                                                 1,
                                                 1,
                                                 1],
                           'max_indent': 3,
                           'imports': ['from rdkit import Chem'],
                           'imports_count': 1,
                           'methods_called': [   'MolFromSmiles',
                                                 'append',
                                                 'RemoveStereochemistry',
                                                 'HasSubstructMatch',
                                                 'GetSubstructMatches',
                                                 'MolFromSmarts'],
                           'methods_called_count': 6,
                           'smarts_strings': [   'methylenedioxy_smarts',
                                                 'aromatic_ether_smarts',
                                                 'benzylisoquinoline_smarts'],
                           'smarts_strings_count': 3,
                           'defs': [   'is_bisbenzylisoquinoline_alkaloid(smiles: '
                                       'str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "Error in benzylisoquinoline '
                                          'SMARTS"',
                                          'False, f"Found '
                                          '{len(distinct_units)} '
                                          'benzylisoquinoline unit(s); need at '
                                          'least 2"',
                                          'False, "No bridging group (aromatic '
                                          'ether or methylenedioxy) linking '
                                          'the benzylisoquinoline units found"',
                                          'True, "Contains at least two '
                                          'benzylisoquinoline units bridged by '
                                          'an appropriate group"'],
                           'returns_count': 5,
                           'complexity': 3.7863651265448652},
    'message': '\n'
               'Attempt failed: F1 score of 0 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: NONE\n'
               'False positives: NONE\n'
               'False negatives: SMILES: '
               'COc1cc2CCN(C)C(Cc3ccc(Oc4cc(CC5N(C)CCc6cc(OC)c(O)cc56)ccc4O)cc3)c2cc1O '
               'NAME: Magnoline REASON: MISSED Found 0 benzylisoquinoline '
               'unit(s); need at least 2\n'
               ' * SMILES: '
               'COc1ccc2C[C@H]3N(C)CCc4cc(OC)c(Oc5c(OC)c(OC)cc6CCN(C)[C@@H](Cc7ccc(Oc1c2)cc7)c56)cc34 '
               'NAME: Obaberine REASON: MISSED Found 0 benzylisoquinoline '
               'unit(s); need at least 2\n'
               ' * SMILES: '
               'COc1cc2CCN[C@@H](Cc3ccc(Oc4cc(C[C@H]5N(C)CCc6cc(OC)c(O)cc56)ccc4O)cc3)c2cc1O '
               "NAME: 2'-norberbamunine REASON: MISSED Found 0 "
               'benzylisoquinoline unit(s); need at least 2\n'
               ' * SMILES: '
               'COc1cc2CCN(C)[C@H]3Cc4ccc(Oc5cc(C[C@@H]6N(C)CCc7cc(OC)c(O)c(Oc1cc23)c67)ccc5O)cc4 '
               'NAME: (+)-Atherospermoline REASON: MISSED Found 0 '
               'benzylisoquinoline unit(s); need at least 2\n'
               ' * SMILES: '
               'COc1ccc2C[C@@H]3N(C)CCc4c(OC)c(OC)c(OC)c(Oc5cc6[C@H](Cc7ccc(Oc1c2)cc7)N(C)CCc6cc5OC)c34 '
               'NAME: Hernandezine REASON: MISSED Found 0 benzylisoquinoline '
               'unit(s); need at least 2\n'
               ' * SMILES: '
               '[H][C@@]12Cc3ccc(O)c(c3)-c3cc(C[C@]4([H])N(C)CCc5cc(OC)c(OC)c(Oc6cc1c(CCN2C)cc6OC)c45)ccc3OC '
               'NAME: rodiasine REASON: MISSED Found 0 benzylisoquinoline '
               'unit(s); need at least 2\n'
               ' * SMILES: '
               'COc1cc2CCN(C)[C@@H](Cc3ccc(Oc4cc(C[C@H]5N(C)CCc6cc(OC)c(O)cc56)ccc4O)cc3)c2cc1O '
               'NAME: berbamunine REASON: MISSED Found 0 benzylisoquinoline '
               'unit(s); need at least 2\n'
               ' * SMILES: '
               'COc1cc2CCN(C)[C@H]3Cc4ccc(Oc5cc(C[C@H]6NCCc7cc(OC)c(Oc(c1O)c23)cc67)ccc5O)cc4 '
               'NAME: Daphnoline REASON: MISSED Found 0 benzylisoquinoline '
               'unit(s); need at least 2\n'
               ' * SMILES: '
               'COc1cc2CCN(C)[C@H](Cc3ccc(Oc4cc(C[C@H]5N(C)CCc6cc(OC)c(O)cc56)ccc4O)cc3)c2cc1O '
               'NAME: guattegaumerine REASON: MISSED Found 0 '
               'benzylisoquinoline unit(s); need at least 2\n'
               ' * SMILES: '
               'COc1ccc2C[C@@H]3N(C)CCc4cc(OC)c(Oc5c(OC)c(O)cc6CCN(C)[C@H](Cc7ccc(Oc1c2)cc7)c56)cc34 '
               'NAME: Gyrocarpine REASON: MISSED Found 0 benzylisoquinoline '
               'unit(s); need at least 2\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'SC[C@H](N)C(=O)N[C@@H]([C@H](O)C)C(=O)N[C@@H](C)C(O)=O',
                                     'name': 'Cys-Thr-Ala',
                                     'reason': 'Found 0 benzylisoquinoline '
                                               'unit(s); need at least 2'},
                                 {   'smiles': 'OC=1C=C(CC)C=C(C1)C',
                                     'name': '3-Ethyl-5-methylphenol',
                                     'reason': 'Found 0 benzylisoquinoline '
                                               'unit(s); need at least 2'},
                                 {   'smiles': 'BrC1=C(C(=C(OC)C=C1)C(=O)O[C@H]2[C@H](O)[C@H](O[C@H](C2)O[C@H]3[C@H](O)C[C@H](O[C@@H]4[C@H]5C=C[C@H]6CCCCC=C[C@H]7[C@]8(C(=C(OC([C@]6([C@@H]5CCC4)C)=O)C(=O)O8)O)C[C@@H](C)C(=C7)C(=O)O)OC3C)C)C',
                                     'name': 'Bromothricin',
                                     'reason': 'Found 0 benzylisoquinoline '
                                               'unit(s); need at least 2'},
                                 {   'smiles': 'C[C@H](C1=CC=CC=C1)NC(=O)C[C@H]2CC[C@H]3[C@@H](O2)COC4=C(C=C(C=C4)NS(=O)(=O)C5=CC=C(C=C5)Cl)C(=O)N3C',
                                     'name': '2-[(2R,4aS,12aR)-8-[(4-chlorophenyl)sulfonylamino]-5-methyl-6-oxo-2,3,4,4a,12,12a-hexahydropyrano[2,3-c][1,5]benzoxazocin-2-yl]-N-[(1R)-1-phenylethyl]acetamide',
                                     'reason': 'Found 0 benzylisoquinoline '
                                               'unit(s); need at least 2'},
                                 {   'smiles': 'C[N+](C)(C)C[C@@H](CC([O-])=O)OC(=O)C=C',
                                     'name': 'O-acryloyl-L-carnitine',
                                     'reason': 'Found 0 benzylisoquinoline '
                                               'unit(s); need at least 2'},
                                 {   'smiles': 'C[C@@H]1CN([C@H](COC2=C(C=CC(=C2)NC(=O)C3=NC=CN=C3)C(=O)N(C[C@H]1OC)C)C)CCC4=CC=CC=C4',
                                     'name': 'N-[(5S,6R,9S)-5-methoxy-3,6,9-trimethyl-2-oxo-8-(2-phenylethyl)-11-oxa-3,8-diazabicyclo[10.4.0]hexadeca-1(12),13,15-trien-14-yl]pyrazine-2-carboxamide',
                                     'reason': 'Found 0 benzylisoquinoline '
                                               'unit(s); need at least 2'},
                                 {   'smiles': 'N1(C([C@H](C1)NC(/C(/C=2C=CC(OCC[C@@H](C(=O)[O-])[NH3+])=CC2)=N\\O)=O)=O)[C@@H](C(O)=O)C3=CC=C(C=C3)O',
                                     'name': 'isonocardicin A zwitterion',
                                     'reason': 'Found 0 benzylisoquinoline '
                                               'unit(s); need at least 2'},
                                 {   'smiles': 'CC(=O)N1[C@H]([C@@H]([C@H]1CO)C2=CC=C(C=C2)C3=CC=CC(=C3)C#N)CN(C)C(=O)C',
                                     'name': 'N-[[(2R,3S,4S)-1-acetyl-3-[4-(3-cyanophenyl)phenyl]-4-(hydroxymethyl)-2-azetidinyl]methyl]-N-methylacetamide',
                                     'reason': 'Found 0 benzylisoquinoline '
                                               'unit(s); need at least 2'},
                                 {   'smiles': 'C(=O)([C@@H](N)CCC(=O)N[C@@H](C[C@@H]1C(=C)C1)C(O)=O)O',
                                     'name': '(2S,4R)-hypoglycin B',
                                     'reason': 'Found 0 benzylisoquinoline '
                                               'unit(s); need at least 2'},
                                 {   'smiles': 'C(C(NC(C)C)C)C1=CC=C(C=C1)[123I]',
                                     'name': 'Iofetamine hydrochloride I 123',
                                     'reason': 'Found 0 benzylisoquinoline '
                                               'unit(s); need at least 2'}],
    'sample_false_negatives': [   {   'smiles': 'COc1ccc2C[C@H]3[C@H]4C[C@]5([C@H]6Oc1c2[C@@]46CCN3C)N1CCc2ccc(OC)c3Oc4c(O)c(OC)ccc4C(C5=O)=C1c23',
                                      'name': 'Cancentrine',
                                      'reason': 'Found 1 benzylisoquinoline '
                                                'unit(s); need at least 2'},
                                  {   'smiles': 'COc1cc2CCN=C3Cc4ccc(Oc5c(OC)ccc(C[C@H]6N(C)CCc7cc(OC)c(OC)c(Oc1cc23)c67)c5OC)cc4',
                                      'name': 'Calafatimine',
                                      'reason': 'Found 1 benzylisoquinoline '
                                                'unit(s); need at least 2'},
                                  {   'smiles': 'O1C=2C=C3C(=CC2OC)C=CN=C3C(=O)C4=CC=C(OC=5C=C(CC6N(CCC=7C6=C1C(OC)=C(OC)C7)C)C=CC5OC)C=C4',
                                      'name': 'oxofangchirine',
                                      'reason': 'Found 1 benzylisoquinoline '
                                                'unit(s); need at least 2'}],
    'attempt': 3,
    'reasoning': 'Below is my reasoning followed by the complete code:\n'
                 '\n'
                 'We note that the previous approach failed because the SMARTS '
                 'pattern "c1ccc2CCNC2c1" was too rigid. In the molecules '
                 'provided, extra substituents (such as methoxy groups, '
                 'N‐substituents, extra chiral annotations, etc.) cause the '
                 'simple pattern not to match. To improve our detection we can '
                 'relax the pattern by ignoring an explicit orientation of '
                 'substituents on the nitrogen. In our new approach we use a '
                 'SMARTS pattern for a “benzylisoquinoline unit” that looks '
                 'for an aromatic ring fused to a saturated six‐membered ring '
                 'with one nitrogen. In our experience the pattern \n'
                 '  "c1ccc2c(c1)CCNC2"\n'
                 'seems more flexible since it does not require an exact match '
                 'for extra substituents. In addition we gather all matches '
                 'and filter for distinct (non–overlapping) occurrences. '
                 'Finally, we check for the presence of a bridging group such '
                 'as an aromatic ether bridge ([a]-O-[a]) or a methylenedioxy '
                 'bridge ("cO[CH2]Oc"). If at least two benzylisoquinoline '
                 'units are found and a bridging group is present then we '
                 'classify the molecule as a bisbenzylisoquinoline alkaloid.\n'
                 '\n'
                 'Below is the full Python code using RDKit in a single code '
                 'block:',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 29,
    'num_false_positives': 21,
    'num_true_negatives': 142247,
    'num_false_negatives': 3,
    'num_negatives': None,
    'precision': 0.58,
    'recall': 0.90625,
    'f1': 0.7073170731707317,
    'accuracy': 0.9998313422347154,
    'negative_predictive_value': 0.9999789103690685}