"""
Classifies: CHEBI:36249 bile acid conjugate
"""
"""
Classifies: Bile acid conjugate
Definition:
  Any bile acid (i.e. a molecule with a cholanic/steroid core – typically a fused system
  of three six-membered rings and one five-membered ring) conjugated to a functional group
  that gives additional hydrophilicity or charge (e.g. glycine, taurine, sulfate, glucuronate,
  sugars, or coenzyme A).
  
This implementation uses a heuristic method:
  1. Detect the steroid core by examining the ring systems.
  2. Look for one or more conjugation groups using common SMARTS patterns.
"""

from rdkit import Chem

def is_bile_acid_conjugate(smiles: str):
    """
    Determines if a molecule (given as a SMILES string) is a bile acid conjugate.
    It uses a heuristic for the steroid (cholanic) nucleus based on ring counts 
    (expecting 3 six-membered rings and 1 five-membered ring) and then searches 
    for common conjugation groups using SMARTS patterns.
    
    Args:
        smiles (str): SMILES string of the molecule.
        
    Returns:
        bool: True if the molecule is a bile acid conjugate, False otherwise.
        str: Reason for the classification.
    """
    # Parse the SMILES string into an RDKit molecule
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
    
    # --- Step 1. Check for a steroid (cholanic acid) nucleus ---
    # Bile acids have a tetracyclic fused ring system: three cyclohexane rings and one cyclopentane ring.
    # We use RDKit's ring information as a heuristic.
    ring_info = mol.GetRingInfo()
    rings = ring_info.AtomRings()
    
    if len(rings) < 4:
        return False, "Less than 4 rings detected – steroid nucleus likely missing"
    
    # Count how many rings have 5 atoms and how many have 6 atoms.
    count_5 = sum(1 for ring in rings if len(ring) == 5)
    count_6 = sum(1 for ring in rings if len(ring) == 6)
    if count_5 < 1 or count_6 < 3:
        return False, ("Detected rings do not match the expected pattern for a steroid nucleus "
                       "(expect at least one 5-membered ring and three 6-membered rings)")
    
    # --- Step 2. Check for conjugation groups ---
    # Define a list of SMARTS patterns for functional groups used for bile acid conjugation.
    # These include generic amide bonds (common for amino acid conjugates), taurine and sulfate conjugates,
    # glucuronate, and sugar moieties.
    conjugation_smarts = {
        "generic amide (e.g. amino acid conjugation)": "C(=O)N",
        "taurine conjugation (anionic)": "NCCS(=O)(=O)[O-]",
        "taurine conjugation (neutral)": "NCCS(=O)(=O)O",
        "sulfate conjugation": "S(=O)(=O)[O-]",
        "glucuronate": "O[C@@H]1[C@H](O)[C@@H](O)[C@H](O)[C@@H](O)C(=O)[O-]1",
        "sugar (e.g. glucose)": "OC1OC(O)C(O)C(O)C1O"
        # Note: Additional patterns (e.g., for coenzyme A) can be included here as needed.
    }
    
    found_conjugation = False
    matched_groups = []
    for desc, smart in conjugation_smarts.items():
        pattern = Chem.MolFromSmarts(smart)
        if pattern is None:
            continue  # Skip invalid SMARTS
        if mol.HasSubstructMatch(pattern):
            found_conjugation = True
            matched_groups.append(desc)
            
    if not found_conjugation:
        return False, "No recognized conjugation group detected"
    
    # If both a steroid nucleus and at least one conjugation group are found,
    # we classify the molecule as a bile acid conjugate.
    reason = ("Steroid nucleus detected (heuristic: >=1 five-membered and >=3 six-membered rings) "
              "with conjugation group(s): " + ", ".join(matched_groups))
    return True, reason

# Example usage (for testing purposes):
if __name__ == "__main__":
    # Example SMILES from the provided list (taurocholic acid is given as one example)
    smiles_examples = [
        "[H][C@@]12C[C@H](O)CC[C@]1(C)[C@@]1([H])C[C@H](O)[C@]3(C)[C@]([H])(CC[C@@]3([H])[C@]1([H])[C@H](O)C2)[C@H](C)CCC(=O)NCCS(O)(=O)=O",  # taurocholic acid
        "[C@]12([C@]([C@]3([C@]([C@@H]([C@@H](CCC(NCCS(=O)(=O)O)=O)C)CC3)(C)CC1)[H])([C@H]([C@H](O)[C@]4([C@@]2(CC[C@H](C4)O)C)[H])O)[H])[H]"  # tauro-omega-muricholic acid
    ]
    for s in smiles_examples:
        result, reason = is_bile_acid_conjugate(s)
        print("SMILES:", s)
        print("Classification:", result)
        print("Reason:", reason)
        print("----------")


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:36249',
                          'name': 'bile acid conjugate',
                          'definition': 'Any bile acid conjugated to a '
                                        'functional group that gives '
                                        'additional hydrophilicity or charge '
                                        'to the molecule. Molecules used for '
                                        'conjugation are: glycine, taurine '
                                        '(and other amino acids); sulfuric '
                                        "acid (for which the term ''sulfate'' "
                                        'may be used); glucuronic acid (for '
                                        "which the term ''glucuronate'' may be "
                                        'used); glucose and other uncharged '
                                        'sugars; and coenzyme A.',
                          'parents': ['CHEBI:36078'],
                          'xrefs': [   'PMID:19619630',
                                       'PMID:35224661',
                                       'PMID:36396870',
                                       'PMID:37071431'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 68,
                           'log_lines_of_code': 4.219507705176107,
                           'indent_by_line': [   1,
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
                                                 2,
                                                 1,
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
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 3,
                                                 2,
                                                 3,
                                                 3,
                                                 3,
                                                 1,
                                                 2,
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
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2],
                           'max_indent': 3,
                           'imports': ['from rdkit import Chem'],
                           'imports_count': 1,
                           'methods_called': [   'items',
                                                 'GetRingInfo',
                                                 'AtomRings',
                                                 'HasSubstructMatch',
                                                 'MolFromSmarts',
                                                 'join',
                                                 'MolFromSmiles',
                                                 'append'],
                           'methods_called_count': 8,
                           'smarts_strings': ['smart'],
                           'smarts_strings_count': 1,
                           'defs': ['is_bile_acid_conjugate(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "Less than 4 rings detected '
                                          '– steroid nucleus likely missing"',
                                          'False, ("Detected rings do not '
                                          'match the expected pattern for a '
                                          'steroid nucleus "',
                                          'False, "No recognized conjugation '
                                          'group detected"',
                                          'True, reason'],
                           'returns_count': 5,
                           'complexity': 4.243901541035221},
    'message': '\n'
               'Attempt failed: F1 score of 0 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: NONE\n'
               'False positives: NONE\n'
               'False negatives: SMILES: '
               '[H][C@@]12C[C@H](O)CC[C@]1(C)[C@@]1([H])C[C@H](O)[C@]3(C)[C@]([H])(CC[C@@]3([H])[C@]1([H])[C@H](O)C2)[C@H](C)CCC(=O)NCCS(O)(=O)=O '
               'NAME: taurocholic acid REASON: MISSED No steroid nucleus '
               '(cholanic acid core) detected\n'
               ' * SMILES: '
               '[C@]12([C@]([C@]3([C@]([C@@H]([C@@H](CCC(NCCS(=O)(=O)O)=O)C)CC3)(C)CC1)[H])([C@H]([C@H](O)[C@]4([C@@]2(CC[C@H](C4)O)C)[H])O)[H])[H] '
               'NAME: tauro-omega-muricholic acid REASON: MISSED No steroid '
               'nucleus (cholanic acid core) detected\n'
               ' * SMILES: '
               'O[C@@H]1[C@]2([C@]([C@]3([C@@]([C@@]4([C@](C[C@H]3O)(C[C@H](O)CC4)[H])C)(C1)[H])[H])(CC[C@@]2([C@@H](CCC(=O)NCC(=O)NCC(O)=O)C)[H])[H])C '
               'NAME: '
               '((4R)-4-((3R,5S,7R,9S,10S,12S,13R,14S,17R)-3,7,12-Trihydroxy-10,13-dimethylhexadecahydro-1H-cyclopenta[a]phenanthren-17-yl)pentanoyl)glycylglycine '
               'REASON: MISSED No steroid nucleus (cholanic acid core) '
               'detected\n'
               ' * SMILES: '
               'S(O)(=O)(=O)CCC(NC(=O)CC[C@H]([C@@]1([C@@]2([C@]([C@]3([C@@]([C@@]4([C@](C[C@H]3O)(C[C@H](O)CC4)[H])C)(CC2)[H])[H])(CC1)[H])C)[H])C)C(O)=O '
               'NAME: '
               '((4R)-4-((3R,5S,7R,9S,10S,12S,13R,14S,17R)-3,7,12-Trihydroxy-10,13-dimethylhexadecahydro-1H-cyclopenta[a]phenanthren-17-yl)pentanoyl)valine '
               'REASON: MISSED No steroid nucleus (cholanic acid core) '
               'detected\n'
               ' * SMILES: '
               'C1[C@@]2([C@]3(CC[C@]4([C@]([C@@]3([C@H]([C@H]([C@@]2(C[C@@H](C1)O)[H])O)O)[H])(CC[C@@]4([C@@H](CCC(NCCS(O)(=O)=O)=O)C)[H])[H])C)[H])C '
               'NAME: tauro-beta-muricholic acid REASON: MISSED No steroid '
               'nucleus (cholanic acid core) detected\n'
               ' * SMILES: '
               '[H][C@]12CC[C@@]3([H])[C@]4([H])CC[C@]([H])([C@H](C)CCC(=O)NCC(O)=O)[C@@]4(C)CC[C@]3([H])[C@@]1(C)CC[C@@H](O)C2 '
               'NAME: glycolithocholic acid REASON: MISSED No steroid nucleus '
               '(cholanic acid core) detected\n'
               ' * SMILES: '
               'S(O)(=O)(=O)CCNC(=O)CC[C@H]([C@@]1([C@@]2([C@]([C@]3([C@@]([C@@]4([C@](CC3)(C([C@H](O)C(C4)([2H])[2H])([2H])[2H])[H])C)(C[C@@H]2O)[H])[H])(CC1)[H])C)[H])C '
               'NAME: taurodeoxycholic acid-d4 REASON: MISSED No steroid '
               'nucleus (cholanic acid core) detected\n'
               ' * SMILES: '
               '[H][C@@]12C[C@H](O)CC[C@]1(C)[C@@]1([H])CC[C@]3(C)[C@]([H])(CC[C@@]3([H])[C@]1([H])[C@H](O)C2)[C@H](C)CCC(=O)NCCS(O)(=O)=O '
               'NAME: taurochenodeoxycholic acid REASON: MISSED No steroid '
               'nucleus (cholanic acid core) detected\n'
               ' * SMILES: '
               'C(CNC(CC[C@H]([C@H]1CCC2C3[C@@H](C[C@]4(C[C@@H](CC[C@@]4(C3C[C@@H]([C@]12C)O)C)O)[H])O)C)=O)S(=O)(=O)O '
               'NAME: taurallocholic acid REASON: MISSED No steroid nucleus '
               '(cholanic acid core) detected\n'
               ' * SMILES: '
               'S(O)(=O)(=O)CCNC(=O)CC[C@H]([C@@]1([C@@]2([C@]([C@]3([C@@]([C@@]4([C@]([C@H](O)C3)(C[C@H](O)CC4)[H])C)(CC2)[H])[H])(CC1)[H])C)[H])C '
               'NAME: Tauromurocholate REASON: MISSED No steroid nucleus '
               '(cholanic acid core) detected\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'O=C(N1[C@H](CCC1)C(O)=O)[C@@H](NC(=O)[C@@H](N)CC(O)=O)CCC(=O)N',
                                     'name': 'Asp-Gln-Pro',
                                     'reason': 'Less than 4 rings detected – '
                                               'steroid nucleus likely '
                                               'missing'},
                                 {   'smiles': 'O1C=2C(C(O)=C(CC3=C(O)C=4C(OC3=O)=CC=CC4C)C1=O)=C(C=CC2)C',
                                     'name': 'Gerberinol',
                                     'reason': 'Detected rings do not match '
                                               'the expected pattern for a '
                                               'steroid nucleus (expect at '
                                               'least one 5-membered ring and '
                                               'three 6-membered rings)'},
                                 {   'smiles': 'O=C(O)/C(=C/[C@H]1C=C(CC[C@@H]1C(C)C)CO)/COC(=O)C',
                                     'name': '3-acetylgliocladic acid',
                                     'reason': 'Less than 4 rings detected – '
                                               'steroid nucleus likely '
                                               'missing'},
                                 {   'smiles': 'O=C(CCCCCCCCC)C=1C=CC(=NC1)CCCCCCCCC',
                                     'name': '1-(6-Nonylpyridin-3-yl)decan-1-one',
                                     'reason': 'Less than 4 rings detected – '
                                               'steroid nucleus likely '
                                               'missing'},
                                 {   'smiles': 'CCC(=O)O[C@H]1[C@H](C)O[C@H](C[C@@]1(C)O)O[C@@H]1[C@@H](C)O[C@@H](O[C@H]2[C@@H](CC=O)C[C@@H](C)[C@@H](O)\\C=C\\C=C\\C[C@@H](C)OC(=O)C[C@@H](O)[C@@H]2OC)[C@H](O)[C@H]1N(C)C',
                                     'name': 'Leucomycin A7',
                                     'reason': 'Less than 4 rings detected – '
                                               'steroid nucleus likely '
                                               'missing'},
                                 {   'smiles': 'C[C@H]1O[C@H](C[C@@H](O)[C@@H]1O)c1ccc2C(=O)C3=C([C@H](O)C[C@]4(O)C[C@@](C)(O)CC(=O)[C@]34O)C(=O)c2c1O',
                                     'name': 'Urdamycinone F',
                                     'reason': 'Detected rings do not match '
                                               'the expected pattern for a '
                                               'steroid nucleus (expect at '
                                               'least one 5-membered ring and '
                                               'three 6-membered rings)'},
                                 {   'smiles': 'CC(C)=CCC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\COP([O-])(=O)OP([O-])([O-])=O',
                                     'name': 'all-trans-dodecaprenyl '
                                             'diphosphate(3-)',
                                     'reason': 'Less than 4 rings detected – '
                                               'steroid nucleus likely '
                                               'missing'},
                                 {   'smiles': '[O-][N+](=O)N1CN(CN(CN(C1)[N+]([O-])=O)[N+]([O-])=O)[N+]([O-])=O',
                                     'name': 'octogen',
                                     'reason': 'Less than 4 rings detected – '
                                               'steroid nucleus likely '
                                               'missing'},
                                 {   'smiles': 'CC(=O)NCCC[NH2+]CCCC[NH2+]CCCNC(C)=O',
                                     'name': 'N(1),N(12)-diacetylsperminium(2+)',
                                     'reason': 'Less than 4 rings detected – '
                                               'steroid nucleus likely '
                                               'missing'},
                                 {   'smiles': 'C[C@@H]([C@H]1CC[C@H]2[C@H](CCc3cc(O)ccc3C)C(=O)CC[C@]12C)C(O)=O',
                                     'name': '3-hydroxy-9-oxo-9,10-seco-23,24-bisnorchola-1,3,5(10)-trien-22-oic '
                                             'acid',
                                     'reason': 'Less than 4 rings detected – '
                                               'steroid nucleus likely '
                                               'missing'}],
    'sample_false_negatives': [],
    'attempt': 2,
    'reasoning': 'Below is my reasoning before the code:\n'
                 '\n'
                 'The previous program tried to detect a steroid (cholanic) '
                 'nucleus by using a strict SMARTS pattern. However, many bile '
                 'acids (even well‐known ones like taurocholic acid) were '
                 'missed because the pattern was too narrowly defined. To '
                 'improve detection we can use a heuristic based on ring '
                 'counts since bile acids have the classic tetracyclic steroid '
                 'core (three six‐membered rings fused to one five‐membered '
                 'ring). In the new code we first use RDKit’s ring information '
                 'to require that the molecule has at least four rings, '
                 'including at least one 5‐membered ring and three 6‐membered '
                 'rings. (This is a heuristic so that unusual bile acids might '
                 'be missed but it should capture most standard bile acid '
                 'cores.) Then, we look for conjugation groups using a set of '
                 'relaxed SMARTS patterns (e.g. for generic amide bonds, '
                 'taurine, sulfate, glucuronate, or sugar conjugations). If '
                 'the molecule passes both checks we classify it as a bile '
                 'acid conjugate.\n'
                 '\n'
                 'Below is the complete Python code.',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 97,
    'num_false_positives': 7633,
    'num_true_negatives': 134570,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.012548512289780078,
    'recall': 1.0,
    'f1': 0.024785997189216813,
    'accuracy': 0.9463598032326072,
    'negative_predictive_value': 1.0}