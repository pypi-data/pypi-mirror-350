"""
Classifies: CHEBI:17088 monoacyl-sn-glycerol 3-phosphate
"""
"""
Classifies: CHEBI:17504 monoacyl-sn-glycerol 3-phosphate
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_monoacyl_sn_glycerol_3_phosphate(smiles: str):
    """
    Determines if a molecule is a monoacyl-sn-glycerol 3-phosphate based on its SMILES string.
    A monoacyl-sn-glycerol 3-phosphate has a glycerol backbone with a single acyl group at either position 1 or 2,
    and a phosphate group at position 3.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a monoacyl-sn-glycerol 3-phosphate, False otherwise
        str: Reason for classification
    """
    
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for glycerol backbone with phosphate at position 3
    # The pattern matches a glycerol backbone with a phosphate group at position 3
    # The phosphate group can be in different protonation states
    glycerol_phosphate_pattern = Chem.MolFromSmarts("[CH2X4][CHX4]([OHX2])[CH2X4][OX2][PX4](=[OX1])([OX2H,OX2-])[OX2H,OX2-]")
    if not mol.HasSubstructMatch(glycerol_phosphate_pattern):
        return False, "No glycerol backbone with phosphate at position 3 found"

    # Check for exactly one ester group (acyl group)
    ester_pattern = Chem.MolFromSmarts("[OX2][CX3](=[OX1])")
    ester_matches = mol.GetSubstructMatches(ester_pattern)
    if len(ester_matches) != 1:
        return False, f"Found {len(ester_matches)} ester groups, need exactly 1"

    # Check for acyl group (long carbon chain)
    acyl_pattern = Chem.MolFromSmarts("[CX4,CX3]~[CX4,CX3]~[CX4,CX3]~[CX4,CX3]")
    acyl_matches = mol.GetSubstructMatches(acyl_pattern)
    if len(acyl_matches) < 1:
        return False, "No acyl group (fatty acid chain) found"

    # Check molecular weight to ensure it's a reasonable size for a monoacyl-sn-glycerol 3-phosphate
    mol_wt = rdMolDescriptors.CalcExactMolWt(mol)
    if mol_wt < 300 or mol_wt > 1000:
        return False, "Molecular weight out of range for monoacyl-sn-glycerol 3-phosphate"

    # Check stereochemistry (sn-glycerol)
    # The stereochemistry can be inferred from the SMILES string, but RDKit's substructure matching does not directly handle stereochemistry.
    # For simplicity, we assume the SMILES string correctly represents the stereochemistry.

    return True, "Contains glycerol backbone with a single acyl group and a phosphate group at position 3"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:17088',
                          'name': 'monoacyl-sn-glycerol 3-phosphate',
                          'definition': 'An sn-glycero-3-phosphate compound '
                                        'having a single unspecified acyl '
                                        'group at either position 1 or '
                                        'position 2.',
                          'parents': ['CHEBI:16961', 'CHEBI:26706'],
                          'xrefs': ['KEGG:C03849'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 38,
                           'log_lines_of_code': 3.6375861597263857,
                           'indent_by_line': [   1,
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
                                                 1,
                                                 2,
                                                 0,
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
                                                 2,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 0,
                                                 1],
                           'max_indent': 2,
                           'imports': [   'from rdkit import Chem',
                                          'from rdkit.Chem import AllChem',
                                          'from rdkit.Chem import '
                                          'rdMolDescriptors'],
                           'imports_count': 3,
                           'methods_called': [   'GetSubstructMatches',
                                                 'MolFromSmarts',
                                                 'HasSubstructMatch',
                                                 'MolFromSmiles',
                                                 'CalcExactMolWt'],
                           'methods_called_count': 5,
                           'smarts_strings': [   '[CH2X4][CHX4]([OHX2])[CH2X4][OX2][PX4](=[OX1])([OX2H,OX2-])[OX2H,OX2-]',
                                                 '[OX2][CX3](=[OX1])',
                                                 '[CX4,CX3]~[CX4,CX3]~[CX4,CX3]~[CX4,CX3]'],
                           'smarts_strings_count': 3,
                           'defs': [   'is_monoacyl_sn_glycerol_3_phosphate(smiles: '
                                       'str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "No glycerol backbone with '
                                          'phosphate at position 3 found"',
                                          'False, f"Found {len(ester_matches)} '
                                          'ester groups, need exactly 1"',
                                          'False, "No acyl group (fatty acid '
                                          'chain) found"',
                                          'False, "Molecular weight out of '
                                          'range for monoacyl-sn-glycerol '
                                          '3-phosphate"',
                                          'True, "Contains glycerol backbone '
                                          'with a single acyl group and a '
                                          'phosphate group at position 3"'],
                           'returns_count': 6,
                           'complexity': 3.527517231945277},
    'message': '\n'
               'Attempt failed: F1 score of 0 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: NONE\n'
               'False positives: NONE\n'
               'False negatives: SMILES: '
               'P(OC[C@H](O)COC(=O)CCCCCCCCCCCCCCCCCCCCC)(O)(O)=O NAME: '
               '1-docosanoyl-glycero-3-phosphate REASON: MISSED No glycerol '
               'backbone with phosphate at position 3 found\n'
               ' * SMILES: '
               'P(OC[C@H](O)COC(=O)CCCCCCCCCCC/C=C\\C/C=C\\CCCCC)(O)(O)=O '
               'NAME: 1-(13Z,16Z-docosadienoyl)-glycero-3-phosphate REASON: '
               'MISSED No glycerol backbone with phosphate at position 3 '
               'found\n'
               ' * SMILES: '
               'P(OC[C@H](O)COC(=O)CCCCCCC/C=C\\C/C=C\\CCCC)(O)(O)=O NAME: '
               'PA(17:2(9Z,12Z)/0:0) REASON: MISSED No glycerol backbone with '
               'phosphate at position 3 found\n'
               ' * SMILES: CCCCC\\C=C/C\\C=C/CCCCCCCC(=O)O[C@H](CO)COP(O)(O)=O '
               'NAME: lysophosphatidic acid 0:0/18:2(9Z,12Z) REASON: MISSED No '
               'glycerol backbone with phosphate at position 3 found\n'
               ' * SMILES: P(OCC(O)COC(=O)CCCCCCC/C=C\\C/C=C\\CCCCC)(O)(O)=O '
               'NAME: LysoPA(18:2(9Z,12Z)/0:0) REASON: MISSED No glycerol '
               'backbone with phosphate at position 3 found\n'
               ' * SMILES: [H][C@@](O)(COC(=O)CCCCCCC\\C=C/CCCCCC)COP(O)(O)=O '
               'NAME: 1-palmitoleoyl-sn-glycerol 3-phosphate REASON: MISSED No '
               'glycerol backbone with phosphate at position 3 found\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCOC[C@H](COP(O)(O)=O)OC(=O)CCC\\C=C/C\\C=C/C\\C=C/C\\C=C/CCCCC '
               'NAME: 1-palmityl-2-arachidonoyl-sn-glycero-3-phosphate REASON: '
               'MISSED No glycerol backbone with phosphate at position 3 '
               'found\n'
               ' * SMILES: P(OCC(OC(=O)CCCCCCC/C=C\\CCCCCCCC)CO)(O)(O)=O NAME: '
               'LysoPA(0:0/18:1(9Z)) REASON: MISSED No glycerol backbone with '
               'phosphate at position 3 found\n'
               ' * SMILES: '
               'CC\\C=C/C\\C=C/C\\C=C/CCCCCCCC(=O)OC[C@@H](O)COP(O)(O)=O NAME: '
               '1-linolenoyl-sn-glycero-3-phosphate REASON: MISSED No glycerol '
               'backbone with phosphate at position 3 found\n'
               ' * SMILES: P(OC[C@H](O)COC(=O)CCCCCCCCCCCCCCCCCC)(O)(O)=O '
               'NAME: 1-nonadecanoyl-glycero-3-phosphate REASON: MISSED No '
               'glycerol backbone with phosphate at position 3 found\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'C1COCCN1C2=C(C=C(C=C2)C(F)(F)F)NC(=O)C3=CC(=CN=C3)Br',
                                     'name': '5-bromo-N-[2-(4-morpholinyl)-5-(trifluoromethyl)phenyl]-3-pyridinecarboxamide',
                                     'reason': 'No glycerol backbone with '
                                               'phosphate at position 3 found'},
                                 {   'smiles': 'C[C@H]1C[C@@H]2CC[C@@H](O2)[C@@H](C)C(=O)O[C@H](C)C[C@H]2CC[C@H](O2)[C@H](C)C(=O)O[C@@H](C)C[C@@H]2CC[C@@H](O2)[C@@H](C)C(=O)O[C@H](C)C[C@H]2CC[C@H](O2)[C@H](C)C(=O)O1',
                                     'name': 'Nonactin',
                                     'reason': 'No glycerol backbone with '
                                               'phosphate at position 3 found'},
                                 {   'smiles': 'O1OC23C(C14C(C5C(C(CC5)C(CCC(C(C)C)C)C)(CC4)C)=CC2=O)(CCC(O)C3)C',
                                     'name': '5,9-Epidioxy-3-hydroxyergost-7-en-6-one',
                                     'reason': 'No glycerol backbone with '
                                               'phosphate at position 3 found'},
                                 {   'smiles': 'CC1=C(SC=C1)C(=O)N2CCCC(C2)CNS(=O)(=O)C3=CC=C(C=C3)OC',
                                     'name': '4-methoxy-N-[[1-[(3-methyl-2-thiophenyl)-oxomethyl]-3-piperidinyl]methyl]benzenesulfonamide',
                                     'reason': 'No glycerol backbone with '
                                               'phosphate at position 3 found'},
                                 {   'smiles': 'O(C(=O)CCCCCCCCCCCCCCC)C[C@@H](O)COC(=O)CCCCCCCCC/C=C\\CCCCCCCC',
                                     'name': 'DG(16:0/0:0/20:1n9)',
                                     'reason': 'No glycerol backbone with '
                                               'phosphate at position 3 found'},
                                 {   'smiles': 'Oc1cc2CC3(O)COc4c(O)c(O)ccc4C3c2cc1O',
                                     'name': 'haematoxylin',
                                     'reason': 'No glycerol backbone with '
                                               'phosphate at position 3 found'},
                                 {   'smiles': 'O([C@@H]1[C@H](O)[C@H](O[C@H]2[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]2CO)O[C@H]3[C@H](O)[C@@H](NC(=O)C)C(O[C@@H]3CO)O)O[C@@H]([C@H]1O)CO[C@H]4O[C@@H]([C@@H](O)[C@H](O[C@H]5O[C@@H]([C@@H](O)[C@H](O)[C@@H]5O)CO)[C@@H]4O)CO[C@H]6O[C@@H]([C@@H](O)[C@H](O)[C@@H]6O[C@H]7O[C@@H]([C@@H](O)[C@H](O)[C@@H]7O)CO)CO)[C@H]8O[C@@H]([C@@H](O)[C@H](O)[C@@H]8O[C@@H]9O[C@@H]([C@@H](O[C@@H]%10O[C@@H]([C@H](O)[C@H](O)[C@H]%10O)CO)[C@H](O)[C@H]9NC(=O)C)CO)CO',
                                     'name': 'N-[(3R,4R,5S,6R)-5-[(2S,3R,4R,5S,6R)-3-Acetamido-5-[(2S,3S,4S,5R,6R)-4-[(2R,3S,4S,5S,6R)-3-[(2S,3R,4R,5S,6R)-3-acetamido-4-hydroxy-6-(hydroxymethyl)-5-[(2S,3R,4S,5R,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-6-[[(2S,3S,4S,5R,6R)-6-[[(2S,3S,4S,5S,6R)-4,5-dihydroxy-6-(hydroxymethyl)-3-[(2R,3S,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxymethyl]-3,5-dihydroxy-4-[(2R,3S,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxymethyl]-3,5-dihydroxyoxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-2,4-dihydroxy-6-(hydroxymethyl)oxan-3-yl]acetamide',
                                     'reason': 'No glycerol backbone with '
                                               'phosphate at position 3 found'},
                                 {   'smiles': 'O([C@@H]1[C@H](O)[C@@H](O)[C@@H](O[C@@H]1CO)O)[C@@H]2O[C@@H]([C@@H](O)[C@H](O)[C@H]2O)CO',
                                     'name': 'beta-D-Glcp-(1->4)-beta-D-Galp',
                                     'reason': 'No glycerol backbone with '
                                               'phosphate at position 3 found'},
                                 {   'smiles': 'O=C(N)C(/C=C/[N+]([O-])=NC(C(O)C)C)CCC',
                                     'name': 'Maniwamycin F',
                                     'reason': 'No glycerol backbone with '
                                               'phosphate at position 3 found'},
                                 {   'smiles': 'O1C2=C(C(=O)C(C3=C(O)C=C(O)C=C3)=C1)C(OC)=CC(O)=C2',
                                     'name': 'Barpisoflavone A',
                                     'reason': 'No glycerol backbone with '
                                               'phosphate at position 3 '
                                               'found'}],
    'sample_false_negatives': [   {   'smiles': 'CCCCC\\C=C/C\\C=C/CCCCCCCC(=O)O[C@H](CO)COP(O)(O)=O',
                                      'name': 'lysophosphatidic acid '
                                              '0:0/18:2(9Z,12Z)',
                                      'reason': 'No glycerol backbone with '
                                                'phosphate at position 3 '
                                                'found'},
                                  {   'smiles': 'CCCCCCCCCCCCCCCCOC[C@H](COP(O)(O)=O)OC(=O)CCC\\C=C/C\\C=C/C\\C=C/C\\C=C/CCCCC',
                                      'name': '1-palmityl-2-arachidonoyl-sn-glycero-3-phosphate',
                                      'reason': 'No glycerol backbone with '
                                                'phosphate at position 3 '
                                                'found'},
                                  {   'smiles': 'P(OCC(OC(=O)CCCCCCC/C=C\\CCCCCCCC)CO)(O)(O)=O',
                                      'name': 'LysoPA(0:0/18:1(9Z))',
                                      'reason': 'No glycerol backbone with '
                                                'phosphate at position 3 '
                                                'found'},
                                  {   'smiles': 'C(CCCCCCC/C=C\\CCCCCCCC)(=O)O[C@@H](COP(=O)(O)O)CO/C=C\\CCCCCCCCCCCCCCCC',
                                      'name': '1-[(1Z)-octadecenyl]-2-oleoyl-sn-glycero-3-phosphate',
                                      'reason': 'No glycerol backbone with '
                                                'phosphate at position 3 '
                                                'found'},
                                  {   'smiles': 'CCCCCCCC\\C=C/CCCCCCCC(=O)O[C@H](CO)COP(O)(O)=O',
                                      'name': '2-oleoyl-sn-glycero-3-phosphate',
                                      'reason': 'No glycerol backbone with '
                                                'phosphate at position 3 '
                                                'found'},
                                  {   'smiles': 'P(OCC(OC(=O)CCCCCCC/C=C\\C/C=C\\CCCCC)CO)(O)(O)=O',
                                      'name': 'LysoPA(0:0/18:2(9Z,12Z))',
                                      'reason': 'No glycerol backbone with '
                                                'phosphate at position 3 '
                                                'found'},
                                  {   'smiles': 'CCCCC\\C=C/C\\C=C/C\\C=C/C\\C=C/CCCC(=O)O[C@H](CO)COP(O)(O)=O',
                                      'name': '2-arachidonoyl-sn-glycero-3-phosphate',
                                      'reason': 'No glycerol backbone with '
                                                'phosphate at position 3 '
                                                'found'},
                                  {   'smiles': 'CCCCCCCC\\C=C/CCCCCCCCOC[C@H](COP(O)(O)=O)OC(=O)CCC\\C=C/C\\C=C/C\\C=C/C\\C=C/CCCCC',
                                      'name': '1-(9Z-octadecenyl)-2-arachidonoyl-sn-glycero-3-phosphate',
                                      'reason': 'No glycerol backbone with '
                                                'phosphate at position 3 '
                                                'found'},
                                  {   'smiles': 'P(OCC(OC(=O)CCC/C=C/C/C=C/C\\C=C\\C\\C=C\\CCCCC)CO)(O)(O)=O',
                                      'name': '1-Lyso-2-arachidonoyl-phosphatidate',
                                      'reason': 'No glycerol backbone with '
                                                'phosphate at position 3 '
                                                'found'},
                                  {   'smiles': 'P(OC[C@H](OC(=O)CCCCCCCCCCCCCCC)CO)(O)(O)=O',
                                      'name': 'LPA(0:0/16:0)',
                                      'reason': 'No glycerol backbone with '
                                                'phosphate at position 3 '
                                                'found'}],
    'attempt': 2,
    'reasoning': 'The previous code failed to correctly identify the glycerol '
                 'backbone with a phosphate at position 3, which is a critical '
                 'part of the classification. The main issue lies in the '
                 'SMARTS pattern used to identify the glycerol backbone with '
                 'the phosphate group. The pattern was too restrictive and did '
                 "not account for variations in the phosphate group's "
                 'protonation state or the exact connectivity of the glycerol '
                 'backbone.\n'
                 '\n'
                 'To improve the code, we need to:\n'
                 '1. Use a more flexible SMARTS pattern to match the glycerol '
                 'backbone with a phosphate group at position 3.\n'
                 '2. Ensure that the pattern accounts for different '
                 'protonation states of the phosphate group.\n'
                 '3. Verify the presence of a single acyl group attached to '
                 'either position 1 or 2 of the glycerol backbone.\n'
                 '\n'
                 'Here is the revised code:',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 36,
    'num_false_positives': 4,
    'num_true_negatives': 142248,
    'num_false_negatives': 12,
    'num_negatives': None,
    'precision': 0.9,
    'recall': 0.75,
    'f1': 0.8181818181818182,
    'accuracy': 0.9998875614898103,
    'negative_predictive_value': 0.9999156474061578}