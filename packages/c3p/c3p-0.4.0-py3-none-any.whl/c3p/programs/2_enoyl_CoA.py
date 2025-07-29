"""
Classifies: CHEBI:19573 2-enoyl-CoA
"""
"""
Classifies: 2-enoyl-CoA
An unsaturated fatty acyl-CoA in which the S-acyl group 
contains a double bond between positions 2 and 3.
"""

from rdkit import Chem

def is_2_enoyl_CoA(smiles: str):
    """
    Determines if a molecule is a 2-enoyl-CoA based on its SMILES string.
    A 2‑enoyl‑CoA is defined as an unsaturated fatty acyl-CoA molecule, 
    where the acyl (fatty acid) moiety contains a double bond between positions 2 and 3
    (i.e., between the α- and β-carbons counting from the carbonyl carbon) 
    and is attached to a CoA scaffold.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if the molecule is a 2‑enoyl‑CoA, False otherwise
        str: Reason for classification
    """
    # Attempt to parse the SMILES string into an RDKit molecule
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # SMARTS to check for the unsaturated acyl group.
    # This pattern seeks a fragment where an sp2 carbon (=CH) is directly connected 
    # to another sp2 carbon which in turn is immediately bonded to a carbonyl carbon (C(=O)S).
    # This effectively tests for a C(=O) group with the α-carbon (C2) double-bonded to the β-carbon (C3).
    unsat_acyl_smarts = "[CH]=[CH]C(=O)S"
    unsat_acyl_pattern = Chem.MolFromSmarts(unsat_acyl_smarts)
    if unsat_acyl_pattern is None:
        return False, "Error building unsaturated acyl SMARTS pattern"
    
    if not mol.HasSubstructMatch(unsat_acyl_pattern):
        return False, "The unsaturated acyl moiety (double bond between positions 2 and 3) was not found"

    # SMARTS to detect a fragment of the CoA (pantetheine) moiety.
    # Most acyl-CoA structures contain a characteristic fragment like "SCCNC(=O)CCNC(=O)"
    # that links the acyl group to the nucleotide portion.
    coa_smarts = "SCCNC(=O)CCNC(=O)"
    coa_pattern = Chem.MolFromSmarts(coa_smarts)
    if coa_pattern is None:
        return False, "Error building CoA SMARTS pattern"
    
    if not mol.HasSubstructMatch(coa_pattern):
        return False, "CoA structural features not found in the molecule"

    return True, "Molecule contains an unsaturated acyl group with a double bond between positions 2 and 3 and a CoA moiety"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:19573',
                          'name': '2-enoyl-CoA',
                          'definition': 'An unsaturated fatty acyl-CoA in '
                                        'which the S-acyl group contains a '
                                        'double bond between positions 2 and '
                                        '3.',
                          'parents': ['CHEBI:51006'],
                          'xrefs': ['KEGG:C00605', 'MetaCyc:D2-ENOYL-COA'],
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
                                                 0,
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
                                                 1],
                           'max_indent': 2,
                           'imports': ['from rdkit import Chem'],
                           'imports_count': 1,
                           'methods_called': [   'MolFromSmiles',
                                                 'HasSubstructMatch',
                                                 'MolFromSmarts'],
                           'methods_called_count': 3,
                           'smarts_strings': [   'unsat_acyl_smarts',
                                                 'coa_smarts'],
                           'smarts_strings_count': 2,
                           'defs': ['is_2_enoyl_CoA(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "Error building unsaturated '
                                          'acyl SMARTS pattern"',
                                          'False, "The unsaturated acyl moiety '
                                          '(double bond between positions 2 '
                                          'and 3) was not found"',
                                          'False, "Error building CoA SMARTS '
                                          'pattern"',
                                          'False, "CoA structural features not '
                                          'found in the molecule"',
                                          'True, "Molecule contains an '
                                          'unsaturated acyl group with a '
                                          'double bond between positions 2 and '
                                          '3 and a CoA moiety"'],
                           'returns_count': 6,
                           'complexity': 3.116703787691222},
    'message': None,
    'sample_true_negatives': [   {   'smiles': 'O=C1OC[C@@H]2O[C@@H](O[C@@H]3[C@@H](OC(=O)CCCCCCCCCCCCCCC)[C@H](C=CCCCC1)[C@H](CCCCC)[C@@H](C3)O)[C@H](O)[C@H]([C@@H]2O)O',
                                     'name': 'Mucorolactone',
                                     'reason': 'The unsaturated acyl moiety '
                                               '(double bond between positions '
                                               '2 and 3) was not found'},
                                 {   'smiles': 'C[C@@H]1CN[C@H](COC2=C(C=CC(=C2)NC(=O)C3=NC4=CC=CC=C4S3)C(=O)N(C[C@H]1OC)C)C',
                                     'name': 'N-[(5S,6R,9S)-5-methoxy-3,6,9-trimethyl-2-oxo-11-oxa-3,8-diazabicyclo[10.4.0]hexadeca-1(12),13,15-trien-14-yl]-1,3-benzothiazole-2-carboxamide',
                                     'reason': 'The unsaturated acyl moiety '
                                               '(double bond between positions '
                                               '2 and 3) was not found'},
                                 {   'smiles': 'COC1=CC=CC(=C1)C2=CC=C(C=C2)[C@@H]3[C@@H]4CN(CC(=O)N4[C@@H]3CO)C(=O)C5=CN=CC=C5',
                                     'name': '(6R,7R,8S)-8-(hydroxymethyl)-7-[4-(3-methoxyphenyl)phenyl]-4-[oxo(3-pyridinyl)methyl]-1,4-diazabicyclo[4.2.0]octan-2-one',
                                     'reason': 'The unsaturated acyl moiety '
                                               '(double bond between positions '
                                               '2 and 3) was not found'},
                                 {   'smiles': 'C(C(/C=C/C=C/C=C/[C@H](CCCC(O)=O)O)=O)/C=C\\CCCCC',
                                     'name': '12-oxo-6-trans-leukotriene B4',
                                     'reason': 'The unsaturated acyl moiety '
                                               '(double bond between positions '
                                               '2 and 3) was not found'},
                                 {   'smiles': 'O=C1OC(=C(C#C[C@H](COC(=O)C)C)CO)C=C1',
                                     'name': "5'-O-acetylaporpinone A",
                                     'reason': 'The unsaturated acyl moiety '
                                               '(double bond between positions '
                                               '2 and 3) was not found'},
                                 {   'smiles': 'O=C(N1[C@@H](CCC1)C(=O)N[C@@H](CCC(=O)N)C(O)=O)[C@@H](N)[C@H](CC)C',
                                     'name': 'Ile-Pro-Gln',
                                     'reason': 'The unsaturated acyl moiety '
                                               '(double bond between positions '
                                               '2 and 3) was not found'},
                                 {   'smiles': 'O[C@@H]1C=CC=C(CCC(O)=O)[C@@H]1O',
                                     'name': '3-[(5R,6S)-5,6-dihydroxycyclohexa-1,3-dienyl]propanoic '
                                             'acid',
                                     'reason': 'The unsaturated acyl moiety '
                                               '(double bond between positions '
                                               '2 and 3) was not found'},
                                 {   'smiles': 'O=C(OC)/C=C/C(C)(C)C',
                                     'name': '4,4-Dimethyl-pentenoic acid '
                                             'methyl ester',
                                     'reason': 'The unsaturated acyl moiety '
                                               '(double bond between positions '
                                               '2 and 3) was not found'},
                                 {   'smiles': 'CCCCOc1ccc(OCCCN2CCOCC2)cc1',
                                     'name': 'pramocaine',
                                     'reason': 'The unsaturated acyl moiety '
                                               '(double bond between positions '
                                               '2 and 3) was not found'},
                                 {   'smiles': 'OC[C@@H](O)C(=O)[C@H](O)[C@H](O)COP(O)(O)=O',
                                     'name': 'D-arabino-hex-3-ulose '
                                             '6-phosphate',
                                     'reason': 'The unsaturated acyl moiety '
                                               '(double bond between positions '
                                               '2 and 3) was not found'}],
    'sample_false_negatives': [   {   'smiles': 'CCCCCCCCCCCC\\C=C(/C)C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12',
                                      'name': '(E)-2-methylpentadec-2-enoyl-CoA',
                                      'reason': 'The unsaturated acyl moiety '
                                                '(double bond between '
                                                'positions 2 and 3) was not '
                                                'found'},
                                  {   'smiles': 'C\\C(CC(O)=O)=C/C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)N1C=NC2=C1N=CN=C2N',
                                      'name': 'trans-3-methylglutaconyl-CoA',
                                      'reason': 'The unsaturated acyl moiety '
                                                '(double bond between '
                                                'positions 2 and 3) was not '
                                                'found'},
                                  {   'smiles': 'CC(C)(COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12)[C@@H](O)C(=O)NCCC(=O)NCCSC(=O)C1=CCCC=C1',
                                      'name': 'cyclohexa-1,5-diene-1-carbonyl-CoA',
                                      'reason': 'The unsaturated acyl moiety '
                                                '(double bond between '
                                                'positions 2 and 3) was not '
                                                'found'},
                                  {   'smiles': 'CC(C)=CCC\\C(CC(O)=O)=C/C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12',
                                      'name': '3-(4-methylpent-3-en-1-yl)pent-2-enedioyl-CoA',
                                      'reason': 'The unsaturated acyl moiety '
                                                '(double bond between '
                                                'positions 2 and 3) was not '
                                                'found'},
                                  {   'smiles': '[C@@H]1(N2C3=C(C(=NC=N3)N)N=C2)O[C@H](COP(OP(OCC(C)([C@H](C(NCCC(NCCSC(C(=CCCC)C)=O)=O)=O)O)C)(=O)O)(=O)O)[C@H]([C@H]1O)OP(O)(O)=O',
                                      'name': '2-methylhexenoyl-CoA',
                                      'reason': 'The unsaturated acyl moiety '
                                                '(double bond between '
                                                'positions 2 and 3) was not '
                                                'found'},
                                  {   'smiles': 'CCCCCCCCCCCCC=C(C)C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12',
                                      'name': '2-methylpentadec-2-enoyl-CoA',
                                      'reason': 'The unsaturated acyl moiety '
                                                '(double bond between '
                                                'positions 2 and 3) was not '
                                                'found'},
                                  {   'smiles': 'CC(C)CCCC(C)CCCC(C)CC\\C=C(/C)C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12',
                                      'name': '(E)-2,3-didehydropristanoyl-CoA',
                                      'reason': 'The unsaturated acyl moiety '
                                                '(double bond between '
                                                'positions 2 and 3) was not '
                                                'found'},
                                  {   'smiles': 'CC(C)(COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12)[C@@H](O)C(=O)NCCC(=O)NCCSC(=O)CC=C',
                                      'name': 'vinylacetyl-CoA',
                                      'reason': 'The unsaturated acyl moiety '
                                                '(double bond between '
                                                'positions 2 and 3) was not '
                                                'found'}],
    'attempt': 0,
    'reasoning': 'Below is my reasoning before the code. For a molecule to be '
                 'a 2‑enoyl‑CoA it must contain two key features. First, its '
                 'acyl (fatty acid) part must be unsaturated – specifically, '
                 'the double bond must occur between the α‐ and β‑carbons '
                 '(i.e. between positions 2 and 3 when counting from the '
                 'carbonyl carbon). In a thioester (as found in acyl‑CoA), the '
                 'acyl group appears as C(=O)S; thus, the leaving group is the '
                 'CoA part and the unsaturation will be visible in the '
                 'fragment “[CH]=[CH]C(=O)S” (when reading the molecule from '
                 'the alkyl side toward the carbonyl). Second, because the '
                 'molecule is a CoA derivative, one expects to see additional '
                 'structural “handles” corresponding to the pantetheine and/or '
                 'adenosine moiety. In our example molecules a recognizable '
                 'fragment is the “SCCNC(=O)CCNC(=O)” portion representing the '
                 'pantetheine arm that attaches the acyl group to the '
                 'nucleotide. I therefore use two SMARTS patterns – one to '
                 'detect the unsaturated acyl moiety (“[CH]=[CH]C(=O)S”) and '
                 'one to detect a common CoA fragment (“SCCNC(=O)CCNC(=O)”). '
                 'If both substructures are found then we classify the '
                 'molecule as a 2‑enoyl‑CoA.\n'
                 '\n'
                 'Below is the complete Python code in a single code block:',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 35,
    'num_false_positives': 207,
    'num_true_negatives': 142050,
    'num_false_negatives': 8,
    'num_negatives': None,
    'precision': 0.1446280991735537,
    'recall': 0.813953488372093,
    'f1': 0.24561403508771928,
    'accuracy': 0.9984891075193254,
    'negative_predictive_value': 0.9999436849737431}