"""
Classifies: CHEBI:50477 butyrate ester
"""
"""
Classifies: butyrate ester

Definition: Any carboxylic ester where the carboxylic acid component is butyric acid.
"""

from rdkit import Chem

def is_butyrate_ester(smiles: str):
    """
    Determines if a molecule is a butyrate ester based on its SMILES string.
    A butyrate ester is any carboxylic ester where the carboxylic acid component is butyric acid.
    
    Args:
        smiles (str): SMILES string of the molecule
    
    Returns:
        bool: True if molecule is a butyrate ester, False otherwise
        str: Reason for classification
    """
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Define SMARTS pattern for butyrate ester
    # Pattern: [CH3][CH2][CH2][C](=O)O[Any Atom]
    butyrate_ester_pattern = Chem.MolFromSmarts("[CH3][CH2][CH2][C](=O)O[*]")
    if butyrate_ester_pattern is None:
        return False, "Failed to create butyrate ester pattern"

    # Check if the molecule has the butyrate ester substructure
    if mol.HasSubstructMatch(butyrate_ester_pattern):
        return True, "Contains butyrate ester group"
    else:
        return False, "Does not contain butyrate ester group"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:50477',
                          'name': 'butyrate ester',
                          'definition': 'Any carboxylic ester where the '
                                        'carboxylic acid component is butyric '
                                        'acid.',
                          'parents': ['CHEBI:33308', 'CHEBI:35748'],
                          'xrefs': ['PMID:23383323'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 23,
                           'log_lines_of_code': 3.1354942159291497,
                           'indent_by_line': [   1,
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
                                                 2,
                                                 1,
                                                 2],
                           'max_indent': 2,
                           'imports': ['from rdkit import Chem'],
                           'imports_count': 1,
                           'methods_called': [   'MolFromSmiles',
                                                 'MolFromSmarts',
                                                 'HasSubstructMatch'],
                           'methods_called_count': 3,
                           'smarts_strings': ['[CH3][CH2][CH2][C](=O)O[*]'],
                           'smarts_strings_count': 1,
                           'defs': ['is_butyrate_ester(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "Failed to create butyrate '
                                          'ester pattern"',
                                          'True, "Contains butyrate ester '
                                          'group"',
                                          'False, "Does not contain butyrate '
                                          'ester group"'],
                           'returns_count': 4,
                           'complexity': 2.6270988431858298},
    'message': '\n'
               'Attempt failed: F1 score of 0 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: NONE\n'
               'False positives: NONE\n'
               'False negatives: SMILES: '
               'CCCC(=O)OC[C@H]1OC(O)[C@H](NC(C)=O)[C@@H](O[C@H](C)C(=O)N[C@@H](C)C(=O)N[C@H](CCC(=O)ON2C(=O)C3C4CC(C=C4)C3C2=O)C(N)=O)[C@@H]1O '
               'NAME: 6-O-butyryl-N-acetylmuramyl-L-alanyl-D-isoglutamine '
               'N-hydroxy-5-norbornene-2,3-dicarboxylmidyl ester REASON: '
               'MISSED Does not contain butyrate ester group\n'
               ' * SMILES: '
               '[H][C@@]12C[C@@H](OC(=O)CCC)C=C3[C@H](O[C@@H](OC(C)=O)[C@@]13[C@@H](O)[C@H](OC(C)=O)[C@@H](C)[C@@]2(C)CCC(=C)C=C)OC(C)=O '
               'NAME: caseanigrescen A REASON: MISSED Does not contain '
               'butyrate ester group\n'
               ' * SMILES: '
               '[H][C@]12C[C@](C)(O)[C@@H](O)CC[C@@](C)(OC(=O)CCC)[C@]([H])(O1)[C@]1([H])[C@]([H])(CC=C(C)[C@]21[H])C(C)C '
               'NAME: Hirsutalin E REASON: MISSED Does not contain butyrate '
               'ester group\n'
               ' * SMILES: '
               'CCCC(=O)OCN([C@H](C[C@@H](OC(C)=O)c1nc(cs1)C(=O)N[C@H](C[C@H](C)C(O)=O)Cc1ccccc1)C(C)C)C(=O)[C@@H](NC(=O)[C@H]1CCCCN1C)[C@@H](C)CC '
               'NAME: Tubulysin E REASON: MISSED Does not contain butyrate '
               'ester group\n'
               ' * SMILES: '
               '[H][C@]12C[C@](C)(O)[C@@H](O)CC[C@@](C)(OC(=O)CCC)[C@]([H])(O1)[C@]1([H])[C@]([H])(CCC(=C)[C@]21[H])[C@@H](C)COC(C)=O '
               'NAME: Hirsutalin H, (rel)- REASON: MISSED Does not contain '
               'butyrate ester group\n'
               ' * SMILES: '
               'CCCC(=O)O[C@H]1[C@H](C)O[C@H](C[C@@]1(C)O)O[C@@H]1[C@@H](C)O[C@@H](O[C@H]2[C@@H](CC=O)C[C@@H](C)[C@@H](O)\\C=C\\C=C\\C[C@@H](C)OC(=O)C[C@@H](O)[C@@H]2OC)[C@H](O)[C@H]1N(C)C '
               'NAME: Leucomycin A5 REASON: MISSED Does not contain butyrate '
               'ester group\n'
               ' * SMILES: '
               '[H][C@@]12CCC3C[C@H](OS(O)(=O)=O)[C@H](C[C@]3(C)[C@@]1([H])CC[C@]1(C)[C@@]([H])([C@H](C)C(OC(=O)CCC)C(OC(=O)CCC)C(CC)C(C)C)[C@@H](O)[C@H](OC(C)=O)[C@@]21[H])OS(O)(=O)=O '
               'NAME: clathsterol disulfonic acid REASON: MISSED Does not '
               'contain butyrate ester group\n'
               ' * SMILES: CCCC(=O)OC(C)CC NAME: sec-butyl butyrate REASON: '
               'MISSED Does not contain butyrate ester group\n'
               ' * SMILES: CCCC(=O)OCCc1ccccc1 NAME: phenethyl butyrate '
               'REASON: MISSED Does not contain butyrate ester group\n'
               ' * SMILES: CCCC(=O)O[C@H](CC([O-])=O)C[N+](C)(C)C NAME: '
               'O-butanoyl-L-carnitine REASON: MISSED Does not contain '
               'butyrate ester group\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'CCOC(=O)CC(C1=CC=CC=C1Cl)NC2=NC(=NC(=N2)N3CCOCC3)N4CCOCC4',
                                     'name': '3-[[4,6-bis(4-morpholinyl)-1,3,5-triazin-2-yl]amino]-3-(2-chlorophenyl)propanoic '
                                             'acid ethyl ester',
                                     'reason': 'Does not contain butyrate '
                                               'ester group'},
                                 {   'smiles': 'O([C@@H]1[C@@H](O)[C@H](O)[C@H](O[C@]1(C=2C=3OC(=CC(=O)C3C(O)=CC2O)C4=CC(O)=C(O)C=C4)[H])CO)[C@@H]5O[C@H]([C@@H](O)[C@@H](O)[C@@H]5O)CO',
                                     'name': "2''-O-beta-L-Galactopyranosylorientin",
                                     'reason': 'Does not contain butyrate '
                                               'ester group'},
                                 {   'smiles': 'C[C@@H]1O[C@@H](O[C@@H]2[C@@H](NC(C)=O)[C@@H](O[C@H](CO)[C@H]2O[C@@H]2O[C@H](CO)[C@H](O)[C@H](O)[C@H]2NC(C)=O)O[C@@H]2[C@@H](O)[C@@H](O)O[C@H](CO)[C@@H]2O)[C@@H](O)[C@H](O)[C@@H]1O',
                                     'name': 'beta-D-GalpNAc-(1->4)-[alpha-L-Fucp-(1->3)]-beta-D-GlcpNAc-(1->3)-alpha-D-Galp',
                                     'reason': 'Does not contain butyrate '
                                               'ester group'},
                                 {   'smiles': 'C[C@H]1CN(C(=O)CC2=C(C=CC(=C2)NC(=O)CCC(F)(F)F)O[C@H]1CN(C)CC3=CC4=C(C=C3)OCO4)[C@@H](C)CO',
                                     'name': 'N-[(2R,3S)-2-[[1,3-benzodioxol-5-ylmethyl(methyl)amino]methyl]-5-[(2S)-1-hydroxypropan-2-yl]-3-methyl-6-oxo-2,3,4,7-tetrahydro-1,5-benzoxazonin-9-yl]-4,4,4-trifluorobutanamide',
                                     'reason': 'Does not contain butyrate '
                                               'ester group'},
                                 {   'smiles': 'C1CC(C1)C(=O)N[C@@H]2C=C[C@H](O[C@H]2CO)CC(=O)NCCCN3CCOCC3',
                                     'name': 'N-[(2R,3R,6R)-2-(hydroxymethyl)-6-[2-[3-(4-morpholinyl)propylamino]-2-oxoethyl]-3,6-dihydro-2H-pyran-3-yl]cyclobutanecarboxamide',
                                     'reason': 'Does not contain butyrate '
                                               'ester group'},
                                 {   'smiles': 'O=C1O[C@@H](CC[C@H](O)C=C[C@H](C1)O)C',
                                     'name': 'Decarestrictine C1',
                                     'reason': 'Does not contain butyrate '
                                               'ester group'},
                                 {   'smiles': '[H]P(O)(=O)OP([H])(O)=O',
                                     'name': 'diphosphonic acid',
                                     'reason': 'Does not contain butyrate '
                                               'ester group'},
                                 {   'smiles': 'C[C@H]1CN(C(=O)CCCN2C(=CN=N2)CO[C@@H]1CN(C)C(=O)C3=NOC(=C3)C4=CC=CC=C4)[C@H](C)CO',
                                     'name': 'N-[[(8S,9S)-6-[(2R)-1-hydroxypropan-2-yl]-8-methyl-5-oxo-10-oxa-1,6,14,15-tetrazabicyclo[10.3.0]pentadeca-12,14-dien-9-yl]methyl]-N-methyl-5-phenyl-3-isoxazolecarboxamide',
                                     'reason': 'Does not contain butyrate '
                                               'ester group'},
                                 {   'smiles': 'OCCCCCCC[C@@H](O)CC(O)=O',
                                     'name': '(3R)-3,10-dihydroxydecanoic acid',
                                     'reason': 'Does not contain butyrate '
                                               'ester group'},
                                 {   'smiles': 'S(=O)(=O)(CC[C@@H]1NC(=O)[C@H](NC(=O)C(N(C(=O)CC[C@@H](NC([C@H]([C@@H](NC([C@@H](NC(C[C@@H](NC1=O)C(=O)O)=O)CCCN=C(N)N)=O)/C=C/C(=C/[C@@H]([C@@H](OC)CC2=CC=CC=C2)C)/C)C)=O)C(=O)O)C)=C)C)C',
                                     'name': '[D-Asp3]MC-M(O2)R',
                                     'reason': 'Does not contain butyrate '
                                               'ester group'}],
    'sample_false_negatives': [   {   'smiles': 'C(CCCOC(C(CC)C)=O)CC',
                                      'name': 'hexyl 2-methylbutanoate',
                                      'reason': 'Does not contain butyrate '
                                                'ester group'},
                                  {   'smiles': 'O[C@@](C([N+](CC(=O)CCC)(C)C)([2H])[2H])(CC([O-])=O)[2H]',
                                      'name': 'butyryl-L-carnitine-d3',
                                      'reason': 'Does not contain butyrate '
                                                'ester group'}],
    'attempt': 2,
    'reasoning': 'The previous code attempted to identify butyrate esters by '
                 'fragmenting the molecule at ester bonds and then checking if '
                 'any of the acyl fragments matched a butyryl group '
                 '(CCCC(=O)). However, this approach has several issues:\n'
                 '\n'
                 '1. **Complexity of Fragmentation**: Fragmenting molecules, '
                 'especially large and complex ones, can be error-prone. The '
                 '`FragmentOnBonds` function may not handle complex '
                 'ester-containing molecules correctly, leading to missed '
                 'matches.\n'
                 '\n'
                 '2. **Substructure Matching Limitations**: The code relies on '
                 'matching the acyl fragment exactly to the butyryl group. In '
                 'complex molecules, the acyl fragment might have additional '
                 'substituents or stereochemistry that prevent a direct '
                 'match.\n'
                 '\n'
                 '3. **Inefficient Ester Pattern**: The ester pattern '
                 '`"C(=O)O[C;!$(C(=O))]"` might not match all ester groups, '
                 'especially in molecules where esters are part of rings or '
                 'have unusual connectivity.\n'
                 '\n'
                 '**Improvement Strategy**:\n'
                 '\n'
                 '- **Direct Substructure Matching**: Instead of fragmenting '
                 'the molecule, we can define a SMARTS pattern that directly '
                 'represents the butyrate ester group and use substructure '
                 'matching to identify its presence.\n'
                 '\n'
                 '- **Define a Robust SMARTS Pattern**: The butyrate ester '
                 'group can be defined as four carbons in a chain connected to '
                 'a carbonyl group and an oxygen atom (the ester linkage). The '
                 'pattern should account for any substituents attached to the '
                 'ester oxygen.\n'
                 '\n'
                 '- **Simplify the Approach**: By using `HasSubstructMatch`, '
                 'we can efficiently check for the presence of the butyrate '
                 'ester group without complex fragmentation logic.\n'
                 '\n'
                 '**Updated Code**:\n'
                 '\n'
                 'Below is the improved code that implements these changes:',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 45,
    'num_false_positives': 112,
    'num_true_negatives': 142141,
    'num_false_negatives': 2,
    'num_negatives': None,
    'precision': 0.28662420382165604,
    'recall': 0.9574468085106383,
    'f1': 0.44117647058823534,
    'accuracy': 0.9991988756148981,
    'negative_predictive_value': 0.9999859296623822}