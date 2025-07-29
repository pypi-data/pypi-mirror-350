"""
Classifies: CHEBI:83970 cardiac glycoside
"""
"""
Classifies: Cardiac glycoside
Definition: Steroid lactones containing sugar residues that act on the contractile force 
            of the cardiac muscles.
This program checks for the presence of:
  1) A steroid nucleus (a fused tetracyclic ring system: roughly 3 six‐membered rings and 1 five‐membered ring)
  2) A lactone ring (approximated as a butenolide / furan-2-one substructure)
  3) At least one sugar residue (detected via a pyranose-like ring pattern, with a looser fallback)
Note: The SMARTS definitions and fused ring detection are approximate and may not capture every nuance.
"""
from rdkit import Chem
from rdkit.Chem import rdMolDescriptors

def is_cardiac_glycoside(smiles: str):
    """
    Determines if a molecule is a cardiac glycoside based on its SMILES string.
    
    Cardiac glycosides are steroid lactones with sugar moieties.
    This function checks for:
      - A steroid nucleus (fused tetracyclic system, using ring-fusion heuristics)
      - A lactone group (butenolide/furan-2-one)
      - At least one sugar residue (pyranose-like ring)

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if the molecule is classified as a cardiac glycoside, False otherwise.
        str: Reason for the classification outcome.
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # (1) Check for a steroid nucleus (fused tetracyclic system)
    # We use the heuristic that a steroid nucleus should contain at least 4 fused rings -
    # with rings of size 5 or 6. Fused rings are defined as rings sharing at least 2 atoms.
    ring_info = mol.GetRingInfo().AtomRings()
    candidate_rings = []
    for ring in ring_info:
        if len(ring) in (5, 6):
            candidate_rings.append(set(ring))
    if len(candidate_rings) < 4:
        return False, "Less than 4 rings of size 5 or 6 found; no steroid nucleus detected"
    
    # Build a simple graph: nodes are ring indices; add an edge if two rings share at least 2 atoms.
    adj = {i: set() for i in range(len(candidate_rings))}
    for i in range(len(candidate_rings)):
        for j in range(i+1, len(candidate_rings)):
            if len(candidate_rings[i].intersection(candidate_rings[j])) >= 2:
                adj[i].add(j)
                adj[j].add(i)
    # Find connected components (via DFS)
    visited = set()
    def dfs(node, comp):
        comp.add(node)
        visited.add(node)
        for nbr in adj[node]:
            if nbr not in visited:
                dfs(nbr, comp)
        return comp
    
    found_steroid = False
    for i in range(len(candidate_rings)):
        if i not in visited:
            comp = dfs(i, set())
            if len(comp) >= 4:
                found_steroid = True
                break
    if not found_steroid:
        return False, "No fused tetracyclic steroid nucleus detected"

    # (2) Check for a lactone group: use a SMARTS for butenolide (furan-2-one)
    lactone_smarts = "O=C1C=CCO1"
    lactone_pattern = Chem.MolFromSmarts(lactone_smarts)
    if not mol.HasSubstructMatch(lactone_pattern):
        return False, "No lactone group (butenolide/furan-2-one) found"
    
    # (3) Check for at least one sugar residue.
    # Primary try: a stereochemically defined pyranose ring
    sugar_smarts = "[C@H]1O[C@@H](O)[C@H](O)[C@@H](O)[C@H](O)[C@H]1"
    sugar_pattern = Chem.MolFromSmarts(sugar_smarts)
    if mol.HasSubstructMatch(sugar_pattern):
        sugar_found = True
    else:
        # Fallback: a looser pattern for a six-membered ring with at least two oxygens.
        sugar_smarts_loose = "O1CC(O)CC(O)C1"
        sugar_pattern_loose = Chem.MolFromSmarts(sugar_smarts_loose)
        sugar_found = mol.HasSubstructMatch(sugar_pattern_loose)
    if not sugar_found:
        return False, "No sugar residue (pyranose-like ring) found"

    # Optionally, check that the molecule's molecular weight is not too low
    mol_wt = rdMolDescriptors.CalcExactMolWt(mol)
    if mol_wt < 300:
        return False, "Molecular weight too low for typical cardiac glycosides"

    return True, "Contains a fused steroid nucleus, a lactone ring, and at least one sugar residue"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:83970',
                          'name': 'cardiac glycoside',
                          'definition': 'Steroid lactones containing sugar '
                                        'residues that act on the contractile '
                                        'force of the cardiac muscles.',
                          'parents': ['CHEBI:24400', 'CHEBI:26766'],
                          'xrefs': ['Wikipedia:Cardiac_glycoside'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 74,
                           'log_lines_of_code': 4.30406509320417,
                           'indent_by_line': [   1,
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
                                                 2,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 3,
                                                 1,
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 3,
                                                 4,
                                                 4,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 4,
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 3,
                                                 3,
                                                 4,
                                                 4,
                                                 1,
                                                 2,
                                                 0,
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
                                                 2,
                                                 1,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 1,
                                                 2,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 0,
                                                 1],
                           'max_indent': 4,
                           'imports': [   'from rdkit import Chem',
                                          'from rdkit.Chem import '
                                          'rdMolDescriptors'],
                           'imports_count': 2,
                           'methods_called': [   'append',
                                                 'intersection',
                                                 'AtomRings',
                                                 'MolFromSmarts',
                                                 'HasSubstructMatch',
                                                 'CalcExactMolWt',
                                                 'add',
                                                 'MolFromSmiles',
                                                 'GetRingInfo'],
                           'methods_called_count': 9,
                           'smarts_strings': [   'lactone_smarts',
                                                 'sugar_smarts_loose',
                                                 'sugar_smarts'],
                           'smarts_strings_count': 3,
                           'defs': [   'is_cardiac_glycoside(smiles: str):',
                                       'dfs(node, comp):'],
                           'defs_count': 2,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "Less than 4 rings of size 5 '
                                          'or 6 found; no steroid nucleus '
                                          'detected"',
                                          'comp',
                                          'False, "No fused tetracyclic '
                                          'steroid nucleus detected"',
                                          'False, "No lactone group '
                                          '(butenolide/furan-2-one) found"',
                                          'False, "No sugar residue '
                                          '(pyranose-like ring) found"',
                                          'False, "Molecular weight too low '
                                          'for typical cardiac glycosides"',
                                          'True, "Contains a fused steroid '
                                          'nucleus, a lactone ring, and at '
                                          'least one sugar residue"'],
                           'returns_count': 8,
                           'complexity': 5.460813018640834},
    'message': '\n'
               'Attempt failed: F1 score of 0 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: NONE\n'
               'False positives: NONE\n'
               'False negatives: SMILES: '
               '[H]C(=O)O[C@H]1C[C@]2(O)[C@]3([H])CC[C@]4([H])C[C@H](CC[C@]4(C)[C@@]3([H])CC[C@]2(C)[C@@]1([H])C1=CC(=O)OC1)O[C@H]1C[C@H](O)[C@H](O[C@H]2C[C@H](O)[C@H](O[C@H]3C[C@H](O)[C@H](O)[C@@H](C)O3)[C@@H](C)O2)[C@@H](C)O1 '
               'NAME: gitaloxin REASON: MISSED No steroid nucleus (fused '
               'tetracyclic system) found\n'
               ' * SMILES: '
               'OC12C3C(C4(C(O)(CC3)CC(OC5OC(C(OC6OC(C(O)C(O)C6O)COC7OC(C(O)C(O)C7O)CO)C(O)C5)C)CC4)C=O)CCC1(C(CC2)C=8COC(=O)C8)C '
               'NAME: Olitoriusin REASON: MISSED No steroid nucleus (fused '
               'tetracyclic system) found\n'
               ' * SMILES: '
               'O[C@@]12[C@@](C)([C@H](CC1)C=3COC(C3)=O)[C@H](O)C[C@]4([C@]2(CC[C@]5([C@]4(C)CC[C@@H](C5)O[C@]6(C[C@H](O)[C@@H]([C@H](O6)C)O[C@]7(C[C@H](O)[C@@H]([C@H](O7)C)O[C@]8(C[C@H](OC(C)=O)[C@@H]([C@H](O8)C)O[C@]9(O[C@H](CO)[C@H]([C@@H]([C@H]9O)O)O)[H])[H])[H])[H])[H])[H])[H] '
               'NAME: lanatoside C REASON: MISSED No steroid nucleus (fused '
               'tetracyclic system) found\n'
               ' * SMILES: '
               'O[C@@]12C3C([C@@]4([C@](O)(CC3)C[C@@H](O[C@@H]5O[C@@H]([C@H](O)[C@H](O)[C@@H]5O)C)C[C@H]4O)CO)C(O)C[C@@]1([C@H](CC2)C=6COC(=O)C6)C '
               'NAME: '
               '3-[(1R,3S,5S,10R,11R,13R,14S,17R)-1,5,11,14-tetrahydroxy-10-(hydroxymethyl)-13-methyl-3-[(2R,3S,4S,5R,6R)-3,4,5-trihydroxy-6-methyloxan-2-yl]oxy-2,3,4,6,7,8,9,11,12,15,16,17-dodecahydro-1H-cyclopenta[a]phenanthren-17-yl]-2H-furan-5-one '
               'REASON: MISSED No steroid nucleus (fused tetracyclic system) '
               'found\n'
               ' * SMILES: '
               '[H][C@]12CC[C@]3([H])[C@]([H])(CC[C@]4(C)[C@]([H])(CC[C@]34O)C3=CC(=O)OC3)[C@@]1(C)CC[C@@H](C2)O[C@@H]1O[C@@H](C)[C@H](O)[C@@H](OC)[C@@H]1O '
               'NAME: neriifolin REASON: MISSED No steroid nucleus (fused '
               'tetracyclic system) found\n'
               ' * SMILES: '
               'O[C@@]12[C@]3([C@@]([C@@]4([C@](O)(CC3)C[C@@H](O[C@@H]5O[C@@H]([C@H](O)[C@@H](O)[C@H]5O)C)CC4)C=O)([C@H](O)C[C@@]1([C@H](CC2)C=6COC(=O)C6)C)[H])[H] '
               'NAME: Canescein REASON: MISSED No steroid nucleus (fused '
               'tetracyclic system) found\n'
               ' * SMILES: '
               'O[C@@]12[C@]3([C@@]([C@@]4([C@](O)(CC3)C[C@@H](O[C@@H]5O[C@@H]([C@@H](O[C@@H]6OC[C@@H](O)[C@H](O)[C@H]6O)[C@@H](O)C5)C)CC4)C=O)(CC[C@@]1([C@H](CC2)C=7COC(=O)C7)C)[H])[H] '
               'NAME: Erychroside REASON: MISSED No steroid nucleus (fused '
               'tetracyclic system) found\n'
               ' * SMILES: '
               'OC12C3C(C4(C(CC3)CC(OC5OC(C(O)C(O)C5OC6OCC(O)C(O)C6O)C)CC4)C)CCC1(C(CC2)C=7COC(=O)C7)C '
               'NAME: Uzarigenin 3-[xylosyl-(1->2)-rhamnoside] REASON: MISSED '
               'No steroid nucleus (fused tetracyclic system) found\n'
               ' * SMILES: '
               'O[C@@]12C3C([C@@]4([C@](CC3)(C[C@@H](O[C@@H]5O[C@H]([C@H](O[C@@H]6O[C@@H]([C@@H](O)[C@H](O)[C@H]6O)CO[C@@H]7O[C@@H]([C@@H](O)[C@H](O)[C@H]7O)CO)[C@@H](OC)[C@@H]5O)C)CC4)[H])C)CC[C@@]1([C@@H](CC2)C=8COC(=O)C8)C '
               'NAME: '
               '3-[(3s,5r,10s,13r,14s,17s)-14-hydroxy-3-[(2r,3s,4s,5s,6s)-3-hydroxy-4-methoxy-6-methyl-5-[(2s,3r,4s,5s,6r)-3,4,5-trihydroxy-6-[[(2r,3r,4s,5s,6r)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxymethyl]oxan-2-yl]oxyoxan-2-yl]oxy-10,13-dimethyl-1,2,3,4,5,6,7,8,9,11,12,15,16,17-tetradecahydrocyclopenta[a]phenanthren-17-yl]-2h-furan-5-one '
               'REASON: MISSED No steroid nucleus (fused tetracyclic system) '
               'found\n'
               ' * SMILES: '
               '[H][C@]12CC[C@]3([H])[C@]([H])(CC[C@]4(C)[C@]([H])(CC[C@]34O)C3=CC(=O)OC3)[C@@]1(C)[C@H](O)C[C@@H](C2)O[C@@H]1O[C@@H](C)[C@@H](O)[C@@H](OC)[C@H]1O '
               'NAME: acovenoside A REASON: MISSED No steroid nucleus (fused '
               'tetracyclic system) found\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'O1C2=C(O)C=C(COC)C=C2C[C@@H](C1(C)C)O',
                                     'name': 'Conoideochromane B',
                                     'reason': 'Less than 4 rings of size 5 or '
                                               '6 found; no steroid nucleus '
                                               'detected'},
                                 {   'smiles': 'P(OC[C@H](OC(=O)CCCCCCC/C=C\\CCCCC)CO/C=C\\CCCCCCCCCCCCCC)(OCCN)(O)=O',
                                     'name': 'PE(P-16:0/15:1(9Z))',
                                     'reason': 'Less than 4 rings of size 5 or '
                                               '6 found; no steroid nucleus '
                                               'detected'},
                                 {   'smiles': 'O=C1C=2C(OC(=C1)C)=C(C3=C4O[C@](O)(CC(C4=C(O)C=5C3=CC(OC)=CC5OC)=O)C)C6=CC(OC)=CC(=C6C2O)OC',
                                     'name': '2-hydroxydihydronigerone',
                                     'reason': 'No fused tetracyclic steroid '
                                               'nucleus detected'},
                                 {   'smiles': 'O([C@@H]1[C@@H](NC(=O)C)[C@@H](O[C@@H]([C@H]1O)CO)OC[C@H]2O[C@@H](O)[C@H](NC(=O)C)[C@@H](O)[C@H]2O)[C@@H]3O[C@@H]([C@H](O)[C@H](O[C@H]4O[C@@H]([C@H](O)[C@H](O)[C@H]4O)CO)[C@H]3O)CO',
                                     'name': 'N-[(2R,3R,4R,5R,6R)-6-[[(2R,3R,4R,5S,6R)-3-Acetamido-4-[(2R,3R,4S,5S,6R)-3,5-dihydroxy-6-(hydroxymethyl)-4-[(2R,3R,4S,5R,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-5-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxymethyl]-2,4,5-trihydroxyoxan-3-yl]acetamide',
                                     'reason': 'No fused tetracyclic steroid '
                                               'nucleus detected'},
                                 {   'smiles': 'O1C(C(O)C(O)C(O)C1OC=2C(O)=C(O)C=C(C2)C=O)COC(=O)C3=CC(O)=C(O)C(O)=C3',
                                     'name': 'Castamollissin',
                                     'reason': 'Less than 4 rings of size 5 or '
                                               '6 found; no steroid nucleus '
                                               'detected'},
                                 {   'smiles': 'S(OC[C@H]1O[C@@H](OC[C@H]2O[C@@H](O[C@@H]([C@@H](O)[C@H](O)CO[C@]3(O[C@H]([C@H](NC(=O)C)[C@@H](O)C3)[C@H](O)[C@H](O)CO)C(O)=O)[C@@H](NC(=O)C)CO)[C@H](O)[C@@H](O)[C@H]2O)[C@H](NC(=O)C)[C@@H](O)[C@@H]1O[C@@H]4O[C@@H]([C@H](O)[C@H](O)[C@H]4O)CO[C@]5(O[C@H]([C@H](NC(=O)C)[C@@H](O)C5)[C@H](O)[C@H](O)CO)C(O)=O)(O)(=O)=O',
                                     'name': '(2R,4S,5R,6R)-5-Acetamido-2-[[(2R,3R,4S,5R,6S)-6-[(2R,3S,4R,5R,6R)-5-acetamido-6-[[(2R,3R,4S,5R,6R)-6-[(2S,3R,4S,5R)-2-acetamido-6-[(2R,4S,5R,6R)-5-acetamido-2-carboxy-4-hydroxy-6-[(1R,2R)-1,2,3-trihydroxypropyl]oxan-2-yl]oxy-1,4,5-trihydroxyhexan-3-yl]oxy-3,4,5-trihydroxyoxan-2-yl]methoxy]-4-hydroxy-2-(sulfooxymethyl)oxan-3-yl]oxy-3,4,5-trihydroxyoxan-2-yl]methoxy]-4-hydroxy-6-[(1R,2R)-1,2,3-trihydroxypropyl]oxane-2-carboxylic '
                                             'acid',
                                     'reason': 'No fused tetracyclic steroid '
                                               'nucleus detected'},
                                 {   'smiles': 'FC(F)(F)C(F)(F)C(F)(F)C(F)(F)C(F)(F)C(F)(F)F',
                                     'name': 'perfluorohexane',
                                     'reason': 'Less than 4 rings of size 5 or '
                                               '6 found; no steroid nucleus '
                                               'detected'},
                                 {   'smiles': 'CC(C)(O)CCC(=O)[C@](C)(O)[C@H]1[C@H](O)C[C@@]2(C)[C@@H]3CC=C4[C@@H](C[C@@H](O)[C@@H](O)C4(C)C)[C@]3(C)C(=O)C[C@]12C',
                                     'name': 'Cucurbitacin P',
                                     'reason': 'No lactone group '
                                               '(butenolide/furan-2-one) '
                                               'found'},
                                 {   'smiles': 'CCCCCCCc1cc(O)cc(=O)o1',
                                     'name': '4-hydroxy-6-heptylpyran-2-one',
                                     'reason': 'Less than 4 rings of size 5 or '
                                               '6 found; no steroid nucleus '
                                               'detected'},
                                 {   'smiles': 'S(O[C@@H]1[C@@H](O)[C@H](O[C@H]2[C@H](O)[C@@H](NC(=O)C)[C@H](O[C@H]3[C@@H](O)[C@H](O[C@@H]4O[C@@H]([C@@H](O[C@@H]5O[C@@H]([C@H](O)[C@H](OS(O)(=O)=O)[C@H]5O)CO)[C@H](O)[C@H]4NC(=O)C)CO)[C@H](O[C@@H]3O[C@H]6[C@H](O)[C@H](O[C@@H](O[C@H]7[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]7CO)O[C@H]8[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]8CO[C@@H]9O[C@H]([C@@H](O)[C@@H](O)[C@@H]9O)C)O)[C@H]6O)CO[C@H]%10O[C@@H]([C@@H](O)[C@H](O)[C@@H]%10O[C@@H]%11O[C@@H]([C@@H](O[C@@H]%12O[C@@H]([C@H](O[C@@H]%13O[C@@H]([C@H](O)[C@H](O)[C@H]%13NC(=O)C)CO)[C@H](O[C@]%14(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%14)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%12O)CO)[C@H](O)[C@H]%11NC(=O)C)CO)CO[C@@H]%15O[C@@H]([C@@H](O[C@@H]%16O[C@@H]([C@H](O)[C@H](O[C@]%17(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%17)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%16O)CO)[C@H](O)[C@H]%15NC(=O)C)CO)CO)O[C@@H]2CO)O[C@@H]([C@@H]1O)CO)(O)(=O)=O',
                                     'name': 'CID 146017241',
                                     'reason': 'No fused tetracyclic steroid '
                                               'nucleus detected'}],
    'sample_false_negatives': [   {   'smiles': '[H]C(=O)O[C@H]1C[C@]2(O)[C@]3([H])CC[C@]4([H])C[C@H](CC[C@]4(C)[C@@]3([H])CC[C@]2(C)[C@@]1([H])C1=CC(=O)OC1)O[C@H]1C[C@H](O)[C@H](O[C@H]2C[C@H](O)[C@H](O[C@H]3C[C@H](O)[C@H](O)[C@@H](C)O3)[C@@H](C)O2)[C@@H](C)O1',
                                      'name': 'gitaloxin',
                                      'reason': 'No sugar residue '
                                                '(pyranose-like ring) found'},
                                  {   'smiles': 'CO[C@H]1C[C@H](O[C@H]2CC[C@@]3(C)[C@H](CC[C@@H]4[C@@H]3[C@H](O)C[C@]3(C)[C@H](CC[C@]43O)C3=CC(=O)OC3)C2)O[C@@H](C)[C@H]1O',
                                      'name': 'Divostroside',
                                      'reason': 'No sugar residue '
                                                '(pyranose-like ring) found'},
                                  {   'smiles': 'O[C@@]12[C@@](C)([C@H](CC1)C3=CC(OC3)=O)[C@H](O)C[C@]4([C@]2(CC[C@]5([C@]4(C)CC[C@@H](C5)O[C@]6(C[C@H](O)[C@@H]([C@H](O6)C)O[C@]7(C[C@H](O)[C@@H]([C@H](O7)C)O[C@]8(C[C@H](O)[C@@H]([C@H](O8)C)OC)[H])[H])[H])[H])[H])[H]',
                                      'name': 'metildigoxin',
                                      'reason': 'No sugar residue '
                                                '(pyranose-like ring) found'},
                                  {   'smiles': 'O[C@@]12[C@]3([C@@]([C@@]4([C@](O)(CC3)C[C@@H](O[C@@H]5O[C@@H]([C@@H](O)[C@@H](OC)C5)C)CC4)C)(CC[C@@]1([C@H](CC2)C=6COC(=O)C6)C)[H])[H]',
                                      'name': 'Periplocymarin',
                                      'reason': 'No sugar residue '
                                                '(pyranose-like ring) found'},
                                  {   'smiles': 'O[C@@]12[C@]3([C@@]([C@]4(C)[C@](CC3)(C[C@H](CC4)O[C@]5(C[C@H](O)[C@@H]([C@H](O5)C)O[C@]6(C[C@H](O)[C@@H]([C@H](O6)C)O[C@]7(C[C@H](O)[C@@H]([C@H](O7)C)OC(C)=O)[H])[H])[H])[H])(C[C@H]([C@]1(C)[C@H](CC2)C=8COC(C8)=O)O)[H])[H]',
                                      'name': 'acetyldigoxin',
                                      'reason': 'No sugar residue '
                                                '(pyranose-like ring) found'},
                                  {   'smiles': '[H][C@]12CC[C@]3([H])[C@]([H])(C[C@@H](O)[C@]4(C)[C@H](CC[C@]34O)C3=CC(=O)OC3)[C@@]1(C)CC[C@@H](C2)O[C@H]1C[C@H](O)[C@H](O)[C@@H](C)O1',
                                      'name': 'digoxigenin monodigitoxoside',
                                      'reason': 'No sugar residue '
                                                '(pyranose-like ring) found'},
                                  {   'smiles': '[H][C@]12CC[C@]3([H])[C@]([H])(C[C@@H](O)[C@]4(C)[C@H](CC[C@]34O)C3=CC(=O)OC3)[C@@]1(C)CC[C@@H](C2)O[C@H]1C[C@H](O)[C@H](O[C@H]2C[C@H](O)[C@H](O[C@H]3C[C@H](O)[C@H](O)[C@@H](C)O3)[C@@H](C)O2)[C@@H](C)O1',
                                      'name': 'digoxin',
                                      'reason': 'No sugar residue '
                                                '(pyranose-like ring) found'},
                                  {   'smiles': 'O[C@@]12[C@]3([C@@]([C@@]4([C@](CC3)(C[C@@H](O[C@@H]5O[C@@H]([C@@H](O[C@@H]6O[C@@H]([C@@H](O)[C@@H](O)C6)C)[C@@H](O)C5)C)CC4)[H])C)(C[C@@H](O)[C@@]1([C@H](CC2)C=7COC(=O)C7)C)[H])[H]',
                                      'name': 'Digoxigenin bisdigitoxoside',
                                      'reason': 'No sugar residue '
                                                '(pyranose-like ring) found'},
                                  {   'smiles': '[H][C@]12CC[C@]3([H])[C@]([H])(C[C@@H](OC(C)=O)[C@]4(C)[C@H](CC[C@]34O)C3=CC(=O)OC3)[C@@]1(C)CC[C@@H](C2)O[C@H]1C[C@H](O)[C@H](O[C@H]2C[C@H](O)[C@H](O[C@H]3C[C@H](O)[C@H](O)[C@@H](C)O3)[C@@H](C)O2)[C@@H](C)O1',
                                      'name': '12-O-acetyldigoxin',
                                      'reason': 'No sugar residue '
                                                '(pyranose-like ring) found'},
                                  {   'smiles': 'CO[C@H]1C[C@H](O[C@H]2CC[C@@]3(C)[C@H](CC[C@@H]4[C@@H]3[C@H](O)C[C@]3(C)[C@H](CC[C@]43O)C3=CC(=O)OC3)C2)O[C@@H](C)[C@@H]1O',
                                      'name': 'Divaricoside',
                                      'reason': 'No sugar residue '
                                                '(pyranose-like ring) found'}],
    'attempt': 2,
    'reasoning': 'Below is our reasoning before the code.\n'
                 '\n'
                 'We analyzed the previous attempt and the output errors. All '
                 'mistakes were “MISSED No steroid nucleus (fused tetracyclic '
                 'system) found.” Our hypothesis was that the original SMARTS '
                 'for a steroid nucleus (i.e. "C1CC2CC3CC(C1)C2CC3") was far '
                 'too simplistic to catch the richly substituted and '
                 'stereochemically‐complex steroid cores found in cardiac '
                 'glycosides. To fix this we now try a more flexible approach. '
                 'First, we obtain all rings (using RDKit’s ring info) and '
                 'select those of size 5 or 6. Then we build a simple “ring '
                 'graph” from those rings, connecting any pair of rings that '
                 'share at least 2 atoms (i.e. an edge between fused rings). '
                 'Finally, if any connected component of rings contains at '
                 'least 4 rings—a rough proxy for the tetracyclic (three '
                 'six‐membered and one five‐membered) steroid nucleus—we '
                 'accept that criterion. The lactone and sugar residue '
                 'detection are done using SMARTS as before. (Note the SMARTS '
                 'we use are approximate and the method is heuristic.) \n'
                 '\n'
                 'Below is the complete Python code block.',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 56,
    'num_false_positives': 23,
    'num_true_negatives': 142191,
    'num_false_negatives': 30,
    'num_negatives': None,
    'precision': 0.7088607594936709,
    'recall': 0.6511627906976745,
    'f1': 0.6787878787878788,
    'accuracy': 0.9996275474349965,
    'negative_predictive_value': 0.9997890606872403}