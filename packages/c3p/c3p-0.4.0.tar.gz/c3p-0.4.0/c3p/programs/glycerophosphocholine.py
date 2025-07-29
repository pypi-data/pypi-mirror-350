"""
Classifies: CHEBI:36313 glycerophosphocholine
"""
"""
Classifies: glycerophosphocholine
Definition: The glycerol phosphate ester of a phosphocholine.
A true glycerophosphocholine should contain (i) a phosphocholine headgroup – i.e.
an oxygen-bridged phosphate with a two-carbon chain ending in a trimethylammonium group –
and (ii) that phosphate must be connected via an oxygen (typically on a primary CH2-bearing carbon)
to a short glycerol (or glycerol-like) fragment. In many phospholipids (e.g. diacyl phosphatidylcholines)
the glycerol bears two acyl chains, but those are considered false positives here.
This heuristic method uses SMARTS patterns that capture (a) the ideal non-acylated glycerophosphocholine
and (b) variants with exactly one acyl ester substituent on the glycerol.
Note: This method is heuristic and may not perfectly capture all valid (or invalid) cases.
"""

from rdkit import Chem

def is_glycerophosphocholine(smiles: str):
    """
    Determines whether a molecule (given as a SMILES string) is a glycerophosphocholine.
    
    The approach is to look for a substructure that unites the required elements:
      (a) a phosphocholine headgroup: an oxygen-linked phosphate that is further connected to a 
          two-carbon chain terminating with a trimethylammonium,
      (b) connectivity to a glycerol or glycerol-like backbone—that is, a three-carbon fragment where
          the phosphate is esterified to one of the primary (CH2) groups, and at most one acyl (ester) group 
          is present on the glycerol.
      
    We define three SMARTS patterns:
      1. A fully “free” glycerol backbone (i.e. no acyl chain).
         The SMARTS below expresses the connectivity:
           HO-CH2–CHOH–CH2–O–P(=O)(O)–O–CH2CH2–N⁺(C)(C)C
         as: "OCC(O)CO[P](=O)(O)OCC[N+](C)(C)C"
      2. A lysophosphatidylcholine pattern with an acyl at the sn-1 position:
           Acyl at sn-1 means the leftmost hydroxyl (i.e. HO– becomes O–C(=O)...)
         Pattern: "OC(=O)OCC(O)CO[P](=O)(O)OCC[N+](C)(C)C"
      3. A lysophosphatidylcholine pattern with an acyl at the sn-2 position:
           Acyl at sn-2 means the central hydroxyl is acylated.
         Pattern: "OCC(OC(=O)*)CO[P](=O)(O)OCC[N+](C)(C)C"
    
    If any of these patterns are found, we accept the molecule as a glycerophosphocholine.
    
    Args:
        smiles (str): SMILES string of the molecule.
        
    Returns:
        bool: True if the molecule is accepted as glycerophosphocholine, otherwise False.
        str: Reason for the classification.
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
    
    # List of SMARTS patterns to match the glycerophosphocholine connectivity.
    # Pattern 1: fully free glycerol backbone.
    pattern_free = "OCC(O)CO[P](=O)(O)OCC[N+](C)(C)C"
    # Pattern 2: lysophosphatidylcholine with one acyl chain at position sn-1.
    pattern_lyso_sn1 = "OC(=O)OCC(O)CO[P](=O)(O)OCC[N+](C)(C)C"
    # Pattern 3: lysophosphatidylcholine with one acyl chain at position sn-2.
    # In the SMARTS below, the '*' after OC(=O) allows for any carbon chain.
    pattern_lyso_sn2 = "OCC(OC(=O)*)CO[P](=O)(O)OCC[N+](C)(C)C"
    
    patterns = [
        (pattern_free, "Found free glycerol backbone connectivity"),
        (pattern_lyso_sn1, "Found lysophosphatidylcholine connectivity (acyl at sn-1)"),
        (pattern_lyso_sn2, "Found lysophosphatidylcholine connectivity (acyl at sn-2)")
    ]
    
    for patt_str, explanation in patterns:
        patt = Chem.MolFromSmarts(patt_str)
        if patt is None:
            continue
        if mol.HasSubstructMatch(patt):
            return True, explanation
    
    return False, "Glycerophosphocholine connectivity not found; either phosphocholine headgroup or proper glycerol linkage is missing or has too many acyl substitutions."

# Example usage:
if __name__ == "__main__":
    # Test with one example provided.
    test_smiles = "P(OC[C@@H](CO)OC(CCCCCCC/C=C\\CC(CCCCCC)O)=O)(=O)(OCC[N+](C)(C)C)[O-]"
    result, reason = is_glycerophosphocholine(test_smiles)
    print(result, reason)


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:36313',
                          'name': 'glycerophosphocholine',
                          'definition': 'The glycerol phosphate ester of a '
                                        'phosphocholine. A nutrient with many '
                                        'different roles in human health.',
                          'parents': ['CHEBI:36700', 'CHEBI:37739'],
                          'xrefs': ['PMID:8467564'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 53,
                           'log_lines_of_code': 3.970291913552122,
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
                                                 2,
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 3,
                                                 2,
                                                 3,
                                                 1,
                                                 1,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 1],
                           'max_indent': 3,
                           'imports': ['from rdkit import Chem'],
                           'imports_count': 1,
                           'methods_called': [   'HasSubstructMatch',
                                                 'MolFromSmarts',
                                                 'MolFromSmiles'],
                           'methods_called_count': 3,
                           'smarts_strings': ['patt_str'],
                           'smarts_strings_count': 1,
                           'defs': ['is_glycerophosphocholine(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'True, explanation',
                                          'False, "Glycerophosphocholine '
                                          'connectivity not found; either '
                                          'phosphocholine headgroup or proper '
                                          'glycerol linkage is missing or has '
                                          'too many acyl substitutions."'],
                           'returns_count': 3,
                           'complexity': 2.7940583827104244},
    'message': '\n'
               'Attempt failed: F1 score of 0 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: NONE\n'
               'False positives: NONE\n'
               'False negatives: SMILES: '
               'P(OCC[N+](C)(C)C)(OCC(OC(=O)CCCCCCCCCCCCC=1OC(CCCCC)=CC1C)COC(=O)CCCCCCCCCCC=2OC(=C(C2C)C)CCCCC)(O)=O '
               'NAME: '
               '(3-{[11-(3,4-dimethyl-5-pentylfuran-2-yl)undecanoyl]oxy}-2-{[13-(3-methyl-5-pentylfuran-2-yl)tridecanoyl]oxy}propoxy)[2-(trimethylazaniumyl)ethoxy]phosphinic '
               'acid REASON: MISSED Glycerol backbone connectivity not found '
               '(phosphate not linked via an oxygen to a primary CH2 carbon '
               'with a glycerol-like environment)\n'
               ' * SMILES: '
               'P(OC[C@@H](CO)OC(CCCCCCC/C=C\\CC(CCCCCC)O)=O)(=O)(OCC[N+](C)(C)C)[O-] '
               'NAME: '
               '2-[(9Z)-12-hydroxyoctadec-9-enoyl]-sn-glycero-3-phosphocholine '
               'REASON: MISSED Glycerol backbone connectivity not found '
               '(phosphate not linked via an oxygen to a primary CH2 carbon '
               'with a glycerol-like environment)\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCC(=O)OCC(COP([O-])(=O)OCC[N+](C)(C)C)OC(=O)CCCC(=O)\\C=C\\C(O)=O '
               'NAME: '
               '1-Palmitoyl-2-(5-keto-6-octendioyl)-sn-glycero-3-phosphatidylcholine '
               'REASON: MISSED Glycerol backbone connectivity not found '
               '(phosphate not linked via an oxygen to a primary CH2 carbon '
               'with a glycerol-like environment)\n'
               ' * SMILES: '
               'C([C@@](COC(CCC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)=O)(OC(CCCCCCCCC/C=C\\CCCCCC)=O)[H])OP([O-])(=O)OCC[N+](C)(C)C '
               'NAME: PC(20:5(5Z,8Z,11Z,14Z,17Z)/18:1(11Z)) REASON: MISSED '
               'Glycerol backbone connectivity not found (phosphate not linked '
               'via an oxygen to a primary CH2 carbon with a glycerol-like '
               'environment)\n'
               ' * SMILES: '
               'C([C@@](COC(CCC/C=C\\C/C=C\\C/C=C\\C/C=C\\CCCCC)=O)(OC(CCCCCCCCCCCCCCCCC)=O)[H])OP([O-])(=O)OCC[N+](C)(C)C '
               'NAME: PC(20:4(5Z,8Z,11Z,14Z)/18:0) REASON: MISSED Glycerol '
               'backbone connectivity not found (phosphate not linked via an '
               'oxygen to a primary CH2 carbon with a glycerol-like '
               'environment)\n'
               ' * SMILES: '
               'C([C@](CO/C=C\\CCCCCCCC/C=C\\CCCCCC)([H])OC(CCCCCCCCCCCCCCCCC)=O)OP([O-])(=O)OCC[N+](C)(C)C '
               'NAME: PC(P-18:1(11Z)/18:0) REASON: MISSED Glycerol backbone '
               'connectivity not found (phosphate not linked via an oxygen to '
               'a primary CH2 carbon with a glycerol-like environment)\n'
               ' * SMILES: '
               'P(OCC[N+](C)(C)C)(OCC(OC(=O)C)COCCCCCCCCC=CCCCCCCCC)(O)=O '
               'NAME: '
               '1-O-(cis-9-Octadecenyl)-2-O-acetyl-sn-glycero-3-phosphocholine '
               'REASON: MISSED Glycerol backbone connectivity not found '
               '(phosphate not linked via an oxygen to a primary CH2 carbon '
               'with a glycerol-like environment)\n'
               ' * SMILES: '
               'C([C@@](COC(CC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CCCCC)=O)(OC(CCCCCCC/C=C\\CCCC)=O)[H])OP([O-])(=O)OCC[N+](C)(C)C '
               'NAME: PC(22:5(4Z,7Z,10Z,13Z,16Z)/14:1(9Z)) REASON: MISSED '
               'Glycerol backbone connectivity not found (phosphate not linked '
               'via an oxygen to a primary CH2 carbon with a glycerol-like '
               'environment)\n'
               ' * SMILES: '
               'P(OCC[N+](C)(C)C)(OC[C@H](OC(=O)CCCCC/C=C\\C/C=C\\C/C=C\\C/C=C\\CCCCC)COC(=O)CC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)([O-])=O '
               'NAME: PC(22:6(4Z,7Z,10Z,13Z,16Z,19Z)/22:4(7Z,10Z,13Z,16Z)) '
               'REASON: MISSED Glycerol backbone connectivity not found '
               '(phosphate not linked via an oxygen to a primary CH2 carbon '
               'with a glycerol-like environment)\n'
               ' * SMILES: '
               'C([C@@](CO/C=C\\CCCCCCCCCCCCCCCC)(OC(CCCCCC/C=C\\C/C=C\\C/C=C\\CCCCC)=O)[H])OP([O-])(=O)OCC[N+](C)(C)C '
               'NAME: PC(P-18:0/20:3(8Z,11Z,14Z)) REASON: MISSED Glycerol '
               'backbone connectivity not found (phosphate not linked via an '
               'oxygen to a primary CH2 carbon with a glycerol-like '
               'environment)\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'O=C(N[C@@H](C(O)(C)C)C)[C@H]([C@@]1([C@@]2([C@@](CC1)(/C(/CCC2)=C/C=C\\3/C[C@@H](O)C[C@H](O)C3=C)[H])C)[H])C',
                                     'name': '1alpha,25-dihydroxy-24-oxo-23-azavitamin '
                                             'D2 / '
                                             '1alpha,25-dihydroxy-24-oxo-23-azaergocalciferol',
                                     'reason': 'Glycerophosphocholine '
                                               'connectivity not found; either '
                                               'phosphocholine headgroup or '
                                               'proper glycerol linkage is '
                                               'missing or has too many acyl '
                                               'substitutions.'},
                                 {   'smiles': 'CCCCCCCCCCCCCCCCCCC(O)C([O-])=O',
                                     'name': '2-hydroxyarachidate',
                                     'reason': 'Glycerophosphocholine '
                                               'connectivity not found; either '
                                               'phosphocholine headgroup or '
                                               'proper glycerol linkage is '
                                               'missing or has too many acyl '
                                               'substitutions.'},
                                 {   'smiles': 'C[C@@H](CN([C@@H](C)CO)C(=O)NC1=CC=C(C=C1)C(F)(F)F)[C@@H](CN(C)C(=O)C2CCOCC2)OC',
                                     'name': 'N-[(2S,3S)-4-[[(2S)-1-hydroxypropan-2-yl]-[[4-(trifluoromethyl)phenyl]carbamoyl]amino]-2-methoxy-3-methylbutyl]-N-methyloxane-4-carboxamide',
                                     'reason': 'Glycerophosphocholine '
                                               'connectivity not found; either '
                                               'phosphocholine headgroup or '
                                               'proper glycerol linkage is '
                                               'missing or has too many acyl '
                                               'substitutions.'},
                                 {   'smiles': 'CC(=O)CC\\C=C(/C)CCC=C(C)C',
                                     'name': 'geranyl acetone',
                                     'reason': 'Glycerophosphocholine '
                                               'connectivity not found; either '
                                               'phosphocholine headgroup or '
                                               'proper glycerol linkage is '
                                               'missing or has too many acyl '
                                               'substitutions.'},
                                 {   'smiles': 'O([C@H]1[C@H](O)[C@H](O[C@H](O)[C@H]1O)CO[C@H]2O[C@@H]([C@@H](O)[C@H](O)[C@@H]2O)CO)[C@H]3O[C@@H]([C@@H](O)[C@H](O)[C@@H]3O[C@H]4O[C@@H]([C@@H](O)[C@H](O)[C@@H]4O)CO)CO',
                                     'name': '(2S,3S,4S,5S,6R)-2-[[(2R,3R,4S,5S,6S)-4-[(2R,3S,4S,5S,6R)-4,5-Dihydroxy-6-(hydroxymethyl)-3-[(2R,3S,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-3,5,6-trihydroxyoxan-2-yl]methoxy]-6-(hydroxymethyl)oxane-3,4,5-triol',
                                     'reason': 'Glycerophosphocholine '
                                               'connectivity not found; either '
                                               'phosphocholine headgroup or '
                                               'proper glycerol linkage is '
                                               'missing or has too many acyl '
                                               'substitutions.'},
                                 {   'smiles': 'O=C(OC1=C(C(O)=C(C(=O)O)C(=C1C)C)C)C2=C(OC)C(=C(OC(=O)C3=C(O)C=C(O)C=C3C)C=C2C)C',
                                     'name': 'Thielavin Z5',
                                     'reason': 'Glycerophosphocholine '
                                               'connectivity not found; either '
                                               'phosphocholine headgroup or '
                                               'proper glycerol linkage is '
                                               'missing or has too many acyl '
                                               'substitutions.'},
                                 {   'smiles': '[C@@H]1([C@@H]([C@H]([C@@H]([C@H](O1)CO)O)O)NC(C)=O)O[C@@H]2[C@@H]([C@H](C(O[C@@H]2CO)O)O)O',
                                     'name': 'beta-D-GlcpNAc-(1->4)-D-Galp',
                                     'reason': 'Glycerophosphocholine '
                                               'connectivity not found; either '
                                               'phosphocholine headgroup or '
                                               'proper glycerol linkage is '
                                               'missing or has too many acyl '
                                               'substitutions.'},
                                 {   'smiles': 'CN(C)C(=O)C1=CC=C(C=C1)C2=CC=C(C=C2)[C@@H]3[C@H]4CN(CC(=O)N4[C@H]3CO)C(=O)CC5CC5',
                                     'name': '4-[4-[(6S,7R,8R)-4-(2-cyclopropyl-1-oxoethyl)-8-(hydroxymethyl)-2-oxo-1,4-diazabicyclo[4.2.0]octan-7-yl]phenyl]-N,N-dimethylbenzamide',
                                     'reason': 'Glycerophosphocholine '
                                               'connectivity not found; either '
                                               'phosphocholine headgroup or '
                                               'proper glycerol linkage is '
                                               'missing or has too many acyl '
                                               'substitutions.'},
                                 {   'smiles': 'CCCCCCCCCCCCCCCCCCCCC=C',
                                     'name': '1-docosene',
                                     'reason': 'Glycerophosphocholine '
                                               'connectivity not found; either '
                                               'phosphocholine headgroup or '
                                               'proper glycerol linkage is '
                                               'missing or has too many acyl '
                                               'substitutions.'},
                                 {   'smiles': 'C([C@@](OC(=O)CCC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)([H])COC(=O)CC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)OC(=O)CCCCC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC',
                                     'name': 'TG(22:5(7Z,10Z,13Z,16Z,19Z)/20:5(5Z,8Z,11Z,14Z,17Z)/22:6(4Z,7Z,10Z,13Z,16Z,19Z))[iso6]',
                                     'reason': 'Glycerophosphocholine '
                                               'connectivity not found; either '
                                               'phosphocholine headgroup or '
                                               'proper glycerol linkage is '
                                               'missing or has too many acyl '
                                               'substitutions.'}],
    'sample_false_negatives': [   {   'smiles': 'CCCCCCCCCCCCCCCCSC[C@H](COP(O)(=O)OCC[N+](C)(C)C)OP(O)(=O)CCCCCCCCCCCCCCCC',
                                      'name': '1-S-hexadecyl-2-O-[hexadecyl(hydroxy)phosphoryl]-1-thio-sn-glycero-3-phosphocholine',
                                      'reason': 'Glycerophosphocholine '
                                                'connectivity not found; '
                                                'either phosphocholine '
                                                'headgroup or proper glycerol '
                                                'linkage is missing or has too '
                                                'many acyl substitutions.'},
                                  {   'smiles': 'CCCCCCCCCCCCCCCC(=O)OCC(COP(O)(=O)CC[N+](C)(C)C)OC(=O)CCCCCCC\\C=C/CCCCCCCC',
                                      'name': '1-hexadecanoyl-2-[(Z)-octadec-9-enoyl]-sn-glycerol '
                                              '3-(2-trimethylaminoethylphosphonate)',
                                      'reason': 'Glycerophosphocholine '
                                                'connectivity not found; '
                                                'either phosphocholine '
                                                'headgroup or proper glycerol '
                                                'linkage is missing or has too '
                                                'many acyl substitutions.'},
                                  {   'smiles': 'P(OC[C@H](OC(=O)CC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)COC(=O)CCCCCCCCC/C=C\\C/C=C\\CCCCC)(O)(O)=O',
                                      'name': 'PA(20:2(11Z,14Z)/22:6(4Z,7Z,10Z,13Z,16Z,19Z))',
                                      'reason': 'Glycerophosphocholine '
                                                'connectivity not found; '
                                                'either phosphocholine '
                                                'headgroup or proper glycerol '
                                                'linkage is missing or has too '
                                                'many acyl substitutions.'},
                                  {   'smiles': 'C(CCCCCCCCCCCC)CCCSC[C@@H](NC(CCCCCCCCCCCCCCC)=O)COP(OCC[N+](C)(C)C)(=O)[O-]',
                                      'name': 'thioetheramide PC',
                                      'reason': 'Glycerophosphocholine '
                                                'connectivity not found; '
                                                'either phosphocholine '
                                                'headgroup or proper glycerol '
                                                'linkage is missing or has too '
                                                'many acyl substitutions.'}],
    'attempt': 4,
    'reasoning': 'Below is one possible solution. In our reasoning we '
                 'recognized that many of the failures came from trying to '
                 '“re‐build” the glycerol connectivity by walking along bonds. '
                 'In our improved approach we instead try to capture the '
                 'entire connectivity (phosphate‐ester–glycerol–choline) with '
                 'one or two SMARTS patterns. Recall that a “true” '
                 'glycerophosphocholine must (i) contain a phosphocholine '
                 'headgroup (–O–P(=O)(O)–O–CH₂CH₂N⁺(C)(C)C) and (ii) have that '
                 'phosphorus linked via an oxygen to a short glycerol-like '
                 'fragment. (In lysophosphatidylcholines a single acyl '
                 'substitution may occur on glycerol; however, if two acyl '
                 'chains are present the molecule is likely a diacyl '
                 'phosphatidylcholine and should be rejected.) \n'
                 '\n'
                 'Our solution uses three patterns:\n'
                 '1. A strict pattern for “non‐acylated” glycerophosphocholine '
                 'where the entire glycerol unit is free '
                 '(HOCH₂–CHOH–CH₂–O–P…),\n'
                 '2. A pattern for a lysophosphatidylcholine in which an acyl '
                 '(–C(=O)… group) is present at the sn-1 position, and \n'
                 '3. A pattern for a lysophosphatidylcholine in which the acyl '
                 'chain is at the sn-2 position.\n'
                 '\n'
                 'If one of the patterns is found, we return True with an '
                 'explanation; otherwise we return False. (Note that this is a '
                 'heuristic and it is possible that some molecules of interest '
                 'are not caught or some false positives occur.) \n'
                 '\n'
                 'Below is the complete Python code using RDKit in a single '
                 'code block.\n'
                 '\n'
                 'Below is the code:\n'
                 '\n'
                 '-----',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 1010,
    'num_false_positives': 49,
    'num_true_negatives': 141237,
    'num_false_negatives': 4,
    'num_negatives': None,
    'precision': 0.9537299338999056,
    'recall': 0.9960552268244576,
    'f1': 0.9744331886155331,
    'accuracy': 0.9996275474349965,
    'negative_predictive_value': 0.9999716796114443}