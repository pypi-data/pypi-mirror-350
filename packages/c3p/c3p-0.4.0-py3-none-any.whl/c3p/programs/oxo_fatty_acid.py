"""
Classifies: CHEBI:59644 oxo fatty acid
"""
"""
Classifies: Oxo fatty acid
Definition: Any fatty acid containing at least one aldehydic or ketonic group 
            in addition to the carboxylic acid group.
Heuristic criteria used here (improved):
  - Molecule must consist only of C, H, and O.
  - Molecule must be acyclic.
  - There must be at least 5 carbon atoms.
  - The overall carbon skeleton should be “linear enough”: 
      the longest carbon chain must span at least 70% of all carbons.
  - The molecule must contain exactly one carboxylic acid group (SMARTS "[CX3](=O)[OX2H]"),
      and its acid carbon must be an endpoint of the longest chain.
  - There must be at least one additional carbonyl (ketonic or aldehydic) function
      (SMARTS "[#6][CX3](=O)[#6]" or "[#6][CX3H1](=O)") that is not the acid carbon.
      Furthermore, the extra oxo must not lie too “close” (topologically) to the acid (min. path length 3),
      and if it is at a chain endpoint then the longest chain must be at least 10 carbons long.
"""

from rdkit import Chem
from rdkit.Chem import rdMolDescriptors
from collections import deque

def get_longest_carbon_chain(mol):
    """
    Build a graph over carbon atoms and calculate the longest chain (path)
    in terms of number of carbon atoms and return the length and endpoints.
    """
    # Gather indices for all carbons.
    carbon_idx = [atom.GetIdx() for atom in mol.GetAtoms() if atom.GetAtomicNum() == 6]
    if not carbon_idx:
        return 0, set()
    # Build neighbor dictionary for carbons only.
    neighbors = {idx: [] for idx in carbon_idx}
    for bond in mol.GetBonds():
        a1 = bond.GetBeginAtom()
        a2 = bond.GetEndAtom()
        if a1.GetAtomicNum() == 6 and a2.GetAtomicNum() == 6:
            neighbors[a1.GetIdx()].append(a2.GetIdx())
            neighbors[a2.GetIdx()].append(a1.GetIdx())
    
    # For each carbon, do a simple BFS to estimate the farthest carbon.
    def bfs(start_idx):
        visited = {start_idx}
        queue = deque([(start_idx, 0, [start_idx])])
        farthest_node = start_idx
        farthest_dist = 0
        farthest_path = [start_idx]
        while queue:
            node, dist, path = queue.popleft()
            if dist > farthest_dist:
                farthest_dist = dist
                farthest_node = node
                farthest_path = path
            for nb in neighbors[node]:
                if nb not in visited:
                    visited.add(nb)
                    queue.append((nb, dist + 1, path + [nb]))
        return farthest_node, farthest_dist, farthest_path
    
    # Start from an arbitrary carbon.
    start = carbon_idx[0]
    node1, _, _ = bfs(start)
    node2, dist, path = bfs(node1)
    endpoints = {path[0], path[-1]}
    return len(path), endpoints

def is_oxo_fatty_acid(smiles: str):
    """
    Determines if a molecule is an oxo fatty acid based on its SMILES string.
    
    Heuristics (improved):
      - Molecule must contain only C, H, and O.
      - Molecule must be acyclic.
      - Must have at least 5 carbon atoms.
      - Its carbon skeleton must be “linear enough”:
           longest carbon chain must cover at least 70% of all carbons.
      - There must be exactly one carboxylic acid group (SMARTS "[CX3](=O)[OX2H]").
        Furthermore, the acid group’s carbonyl must be at an endpoint of the longest chain.
      - There must be at least one extra carbonyl (ketone or aldehyde) that is not part of the acid.
         For any candidate extra oxo, we require that:
           * Its topological distance (number of bonds) from the acid carbon is >= 3.
           * If the candidate lies at a chain endpoint, then the longest chain must have at least 10 carbons.
    
    Returns:
        (bool, str): Tuple with classification result and reasoning.
    """
    mol = Chem.MolFromSmiles(smiles)
    if not mol:
        return False, "Invalid SMILES string."
    
    # (1) Check that atoms are only C, H, and O.
    for atom in mol.GetAtoms():
        if atom.GetAtomicNum() not in (1, 6, 8):
            return False, "Molecule contains elements other than C, H, and O."
    
    # (2) Require acyclic structure.
    if mol.GetRingInfo().NumRings() > 0:
        return False, "Molecule contains rings and does not appear to be a linear fatty acid."
    
    # (3) Must have a sufficient number of carbons.
    carbon_count = sum(1 for atom in mol.GetAtoms() if atom.GetAtomicNum() == 6)
    if carbon_count < 5:
        return False, f"Molecule contains too few carbons ({carbon_count}) to be a fatty acid."
    
    # (4) Check overall linearity: longest carbon chain covers at least 70% of all carbons.
    longest_chain_len, chain_endpoints = get_longest_carbon_chain(mol)
    if longest_chain_len / carbon_count < 0.70:
        return False, "Molecule appears too branched to be a typical linear fatty acid."
    
    # (5) Identify carboxylic acid group (exactly one).
    acid_smarts = "[CX3](=O)[OX2H]"
    acid_pattern = Chem.MolFromSmarts(acid_smarts)
    acid_matches = mol.GetSubstructMatches(acid_pattern)
    if len(acid_matches) == 0:
        return False, "Molecule does not contain a carboxylic acid group."
    if len(acid_matches) > 1:
        return False, "Molecule contains more than one carboxylic acid group."
    
    # We assume the first matching acid group.
    # The acid carbon is taken as the carbonyl carbon (first atom in the match).
    acid_carbonyl_idx = acid_matches[0][0]
    if acid_carbonyl_idx not in chain_endpoints:
        return False, "The carboxylic acid group is not located at the terminus of the main carbon chain."
    
    # (6) Look for an additional carbonyl (ketone or aldehyde) that is not the acid.
    # Define SMARTS for ketone and aldehyde.
    ketone_smarts = "[#6][CX3](=O)[#6]"
    aldehyde_smarts = "[#6][CX3H1](=O)"
    ketone_pattern = Chem.MolFromSmarts(ketone_smarts)
    aldehyde_pattern = Chem.MolFromSmarts(aldehyde_smarts)
    
    # Helper: require extra carbonyl is not the acid carbon,
    # its shortest path from the acid carbon is at least 3 bonds,
    # and if it lies at an endpoint of the longest chain, then the chain must be long (>=10).
    def candidate_is_valid(carbonyl_idx):
        if carbonyl_idx == acid_carbonyl_idx:
            return False
        # Compute topological distance (number of bonds) between acid carbon and candidate.
        path = Chem.GetShortestPath(mol, acid_carbonyl_idx, carbonyl_idx)
        if len(path) < 3:  # path length counts atoms along the shortest route (so <3 means less than 2 bonds apart)
            return False
        if carbonyl_idx in chain_endpoints and longest_chain_len < 10:
            return False
        return True

    extra_oxo_found = False
    # Try ketone candidates.
    for match in mol.GetSubstructMatches(ketone_pattern):
        # In the ketone pattern the carbonyl is the second atom.
        candidate_idx = match[1]
        if candidate_is_valid(candidate_idx):
            extra_oxo_found = True
            break

    # If no valid ketone, try aldehyde candidates.
    if not extra_oxo_found:
        for match in mol.GetSubstructMatches(aldehyde_pattern):
            candidate_idx = match[0]  # in the aldehyde pattern the carbonyl is the first atom.
            if candidate_is_valid(candidate_idx):
                extra_oxo_found = True
                break

    if not extra_oxo_found:
        return False, "Molecule does not appear to contain an additional (non–acid) aldehydic or ketonic group."
    
    return True, ("Molecule is an oxo fatty acid: it is acyclic, contains only C, H and O, "
                  "has a single carboxylic acid group placed at the end of its carbon skeleton, "
                  "and contains an extra (aldehydic or ketonic) function at a suitable location.")

# (Optional testing block)
if __name__ == '__main__':
    test_smiles = [
        # True positives:
        "CC(C)C(=O)CC(O)=O",  # 4-methyl-3-oxopentanoic acid
        "CCCC(O)C(=O)CCC(=O)C\\C=C/CCCCCC(O)=O",  # (7Z)-14-hydroxy-10,13-dioxoheptadec-7-enoic acid
        "CCCCCCCCCCCCC(=O)CC(O)=O",  # 3-oxopalmitic acid
        "OC(=O)CCCCCCCCCCCCCCCCCCCCC=O",  # 22-oxodocosanoic acid
        "C(O)(CCC(CCCC\\C=C/C=C\\C=C\\C=C\\CC)=O)=O",  # (9Z,11Z,13E,15E)-4-oxooctadecatetraenoic acid
        "CCC(O)CC(=O)C(O)=O",       # 4-hydroxy-2-oxohexanoic acid
        "CCCCCC\\C=C/CC(=O)\\C=C\\C=C/C\\C=C/CCCC(O)=O",  # 12-oxo-ETE
        "CCCC(=O)C(O)=O",          # 2-oxopentanoic acid
        "CCC(C)(O)C(=O)C(O)=O",     # 3-hydroxy-3-methyl-2-oxopentanoic acid
        "CCCCCC\\C=C/C\\C=C/C\\C=C/C=C/C(=O)CCCC(O)=O",  # 5-oxo-ETE
        "C(C(/C=C/C=C/C=C\\[C@H](CCCC(O)=O)O)=O)/C=C\\CCCCC=O",  # 12,20-dioxoleukotriene B4
        "C(C(O)=O)CCCCC(/C=C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)=O",  # (8E,10Z,13Z,16Z,19Z)-7-oxodocosapentaenoic acid
        "C(CCC/C=C\\C/C=C\\CC(/C=C/C=C\\CCCCC)=O)(=O)O",  # 11-oxo-ETE
        "C(CCCCCCCC)CCCCCCC(CC(O)=O)=O",  # 3-oxooctadecanoic acid
        "CC(C)=CCCC(=O)CC(O)=O",  # 7-methyl-3-oxooct-6-enoic acid
        "C(CCCCCCCC(C(=O)O)=O)CC",  # 2-oxododecanoic acid
        "C(C(/C=C/C=C/C=C/[C@H](CCCC(O)=O)O)=O)/C=C\\CCCCC",  # 12-oxo-6-trans-leukotriene B4
        "CC(C)CCCC(C)CCCC(C)CCC(=O)C(C)C(O)=O",  # 3-oxopristanic acid
        "CCCCCC(=O)\\C=C\\C=C/C=C/C=C/[C@@H](O)[C@@H](O)CCCC(O)=O",  # 15-oxolipoxin A4
        "CC[C@@](C)(O)C(=O)C(O)=O",  # (R)-3-hydroxy-3-methyl-2-oxopentanoic acid
        "O=C(CC(=O)O)CC/C=C/[C@@H](C/C=C\\CCCCC)O",  # (6E,8R,10Z)-8-hydroxy-3-oxohexadeca-6,10-dienoic acid
        "C(CCCC(CCCCCCO)=O)CCCCC(O)=O",  # 16-hydroxy-10-oxohexadecanoic acid
        "CCCCCCCCCCCCCCC(=O)C(O)=O",  # 2-oxohexadecanoic acid
        # (other examples omitted for brevity)
        # False positives examples (expected False):
        "C(CCCCCC(=O)O)C/C=C/CC(/C=C(/C=C/CCO)\\O)=O",  # wrongly classified in previous version
        "O=C(CCCC)CCC(O)=O",  # 4-keto-n-caprylic acid
        "O=C(CCC(O)=O)CC",  # 4-keto-n-caproic acid
    ]
    for smi in test_smiles:
        result, reason = is_oxo_fatty_acid(smi)
        print(f"SMILES: {smi}\nResult: {result}\nReason: {reason}\n")


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:59644',
                          'name': 'oxo fatty acid',
                          'definition': 'Any fatty acid containing at least '
                                        'one aldehydic or ketonic group in '
                                        'addition to the carboxylic acid '
                                        'group.',
                          'parents': ['CHEBI:25754', 'CHEBI:35366'],
                          'xrefs': [   'PMID:6434570',
                                       'PMID:8454196',
                                       'PMID:8638935'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 161,
                           'log_lines_of_code': 5.081404364984463,
                           'indent_by_line': [   1,
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
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 3,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 3,
                                                 4,
                                                 4,
                                                 4,
                                                 3,
                                                 4,
                                                 5,
                                                 5,
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
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
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 1,
                                                 1,
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 1,
                                                 1,
                                                 1,
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
                                                 2,
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
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 3,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 2,
                                                 3,
                                                 2,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 3,
                                                 0,
                                                 1,
                                                 1,
                                                 2,
                                                 3,
                                                 3,
                                                 4,
                                                 4,
                                                 0,
                                                 1,
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 0,
                                                 1,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 1,
                                                 1,
                                                 2,
                                                 2],
                           'max_indent': 5,
                           'imports': [   'from rdkit import Chem',
                                          'from rdkit.Chem import '
                                          'rdMolDescriptors',
                                          'from collections import deque'],
                           'imports_count': 3,
                           'methods_called': [   'append',
                                                 'popleft',
                                                 'GetSubstructMatches',
                                                 'GetAtoms',
                                                 'GetAtomicNum',
                                                 'MolFromSmiles',
                                                 'NumRings',
                                                 'MolFromSmarts',
                                                 'GetIdx',
                                                 'add',
                                                 'GetEndAtom',
                                                 'GetBonds',
                                                 'GetRingInfo',
                                                 'GetShortestPath',
                                                 'GetBeginAtom'],
                           'methods_called_count': 15,
                           'smarts_strings': [   'aldehyde_smarts',
                                                 'ketone_smarts',
                                                 'acid_smarts'],
                           'smarts_strings_count': 3,
                           'defs': [   'get_longest_carbon_chain(mol):',
                                       'bfs(start_idx):',
                                       'candidate_is_valid(carbonyl_idx):'],
                           'defs_count': 3,
                           'returns': [   '0, set()',
                                          'farthest_node, farthest_dist, '
                                          'farthest_path',
                                          'len(path), endpoints',
                                          'False, "Invalid SMILES string."',
                                          'False, "Molecule contains elements '
                                          'other than C, H, and O."',
                                          'False, "Molecule contains rings and '
                                          'does not appear to be a linear '
                                          'fatty acid."',
                                          'False, f"Molecule contains too few '
                                          'carbons ({carbon_count}) to be a '
                                          'fatty acid."',
                                          'False, "Molecule appears too '
                                          'branched to be a typical linear '
                                          'fatty acid."',
                                          'False, "Molecule does not contain a '
                                          'carboxylic acid group."',
                                          'False, "Molecule contains more than '
                                          'one carboxylic acid group."',
                                          'False, "The carboxylic acid group '
                                          'is not located at the terminus of '
                                          'the main carbon chain."',
                                          'False',
                                          'False',
                                          'False',
                                          'True',
                                          'False, "Molecule does not appear to '
                                          'contain an additional (non–acid) '
                                          'aldehydic or ketonic group."',
                                          'True, ("Molecule is an oxo fatty '
                                          'acid: it is acyclic, contains only '
                                          'C, H and O, "'],
                           'returns_count': 17,
                           'complexity': 9.016280872996893},
    'message': '\n'
               'Attempt failed: F1 score of 0.327455919395466 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: CC(C)C(=O)CC(O)=O NAME: '
               '4-methyl-3-oxopentanoic acid REASON: CORRECT Molecule is an '
               'oxo fatty acid: it is acyclic, contains only C, H and O, has a '
               'single carboxylic acid group and an extra (aldehydic or '
               'ketonic) function.\n'
               ' * SMILES: CCCC(O)C(=O)CCC(=O)C\\C=C/CCCCCC(O)=O NAME: '
               '(7Z)-14-hydroxy-10,13-dioxoheptadec-7-enoic acid REASON: '
               'CORRECT Molecule is an oxo fatty acid: it is acyclic, contains '
               'only C, H and O, has a single carboxylic acid group and an '
               'extra (aldehydic or ketonic) function.\n'
               ' * SMILES: CCCCCCCCCCCCCC(=O)CC(O)=O NAME: 3-oxopalmitic acid '
               'REASON: CORRECT Molecule is an oxo fatty acid: it is acyclic, '
               'contains only C, H and O, has a single carboxylic acid group '
               'and an extra (aldehydic or ketonic) function.\n'
               ' * SMILES: OC(=O)CCCCCCCCCCCCCCCCCCCCC=O NAME: '
               '22-oxodocosanoic acid REASON: CORRECT Molecule is an oxo fatty '
               'acid: it is acyclic, contains only C, H and O, has a single '
               'carboxylic acid group and an extra (aldehydic or ketonic) '
               'function.\n'
               ' * SMILES: C(O)(CCC(CCCC\\C=C/C=C\\C=C\\C=C\\CC)=O)=O NAME: '
               '(9Z,11Z,13E,15E)-4-oxooctadecatetraenoic acid REASON: CORRECT '
               'Molecule is an oxo fatty acid: it is acyclic, contains only C, '
               'H and O, has a single carboxylic acid group and an extra '
               '(aldehydic or ketonic) function.\n'
               ' * SMILES: CCC(O)CC(=O)C(O)=O NAME: 4-hydroxy-2-oxohexanoic '
               'acid REASON: CORRECT Molecule is an oxo fatty acid: it is '
               'acyclic, contains only C, H and O, has a single carboxylic '
               'acid group and an extra (aldehydic or ketonic) function.\n'
               ' * SMILES: CCCCC\\C=C/CC(=O)\\C=C\\C=C/C\\C=C/CCCC(O)=O NAME: '
               '12-oxo-ETE REASON: CORRECT Molecule is an oxo fatty acid: it '
               'is acyclic, contains only C, H and O, has a single carboxylic '
               'acid group and an extra (aldehydic or ketonic) function.\n'
               ' * SMILES: CCCC(=O)C(O)=O NAME: 2-oxopentanoic acid REASON: '
               'CORRECT Molecule is an oxo fatty acid: it is acyclic, contains '
               'only C, H and O, has a single carboxylic acid group and an '
               'extra (aldehydic or ketonic) function.\n'
               ' * SMILES: CCC(C)(O)C(=O)C(O)=O NAME: '
               '3-hydroxy-3-methyl-2-oxopentanoic acid REASON: CORRECT '
               'Molecule is an oxo fatty acid: it is acyclic, contains only C, '
               'H and O, has a single carboxylic acid group and an extra '
               '(aldehydic or ketonic) function.\n'
               ' * SMILES: CCCCC\\C=C/C\\C=C/C\\C=C/C=C/C(=O)CCCC(O)=O NAME: '
               '5-oxo-ETE REASON: CORRECT Molecule is an oxo fatty acid: it is '
               'acyclic, contains only C, H and O, has a single carboxylic '
               'acid group and an extra (aldehydic or ketonic) function.\n'
               ' * SMILES: '
               'C(C(/C=C/C=C/C=C\\[C@H](CCCC(O)=O)O)=O)/C=C\\CCCCC=O NAME: '
               '12,20-dioxoleukotriene B4 REASON: CORRECT Molecule is an oxo '
               'fatty acid: it is acyclic, contains only C, H and O, has a '
               'single carboxylic acid group and an extra (aldehydic or '
               'ketonic) function.\n'
               ' * SMILES: C(C(O)=O)CCCCC(/C=C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)=O '
               'NAME: (8E,10Z,13Z,16Z,19Z)-7-oxodocosapentaenoic acid REASON: '
               'CORRECT Molecule is an oxo fatty acid: it is acyclic, contains '
               'only C, H and O, has a single carboxylic acid group and an '
               'extra (aldehydic or ketonic) function.\n'
               ' * SMILES: [H]C(=O)\\C=C\\CCCCCCCCC(O)=O NAME: '
               '12-oxo-trans-10-dodecenoic acid REASON: CORRECT Molecule is an '
               'oxo fatty acid: it is acyclic, contains only C, H and O, has a '
               'single carboxylic acid group and an extra (aldehydic or '
               'ketonic) function.\n'
               ' * SMILES: C(CCC/C=C\\C/C=C\\CC(/C=C/C=C\\CCCCC)=O)(=O)O NAME: '
               '11-oxo-ETE REASON: CORRECT Molecule is an oxo fatty acid: it '
               'is acyclic, contains only C, H and O, has a single carboxylic '
               'acid group and an extra (aldehydic or ketonic) function.\n'
               ' * SMILES: C(CCCCCCCC)CCCCCCC(CC(O)=O)=O NAME: '
               '3-oxooctadecanoic acid REASON: CORRECT Molecule is an oxo '
               'fatty acid: it is acyclic, contains only C, H and O, has a '
               'single carboxylic acid group and an extra (aldehydic or '
               'ketonic) function.\n'
               ' * SMILES: CC(C)=CCCC(=O)CC(O)=O NAME: '
               '7-methyl-3-oxooct-6-enoic acid REASON: CORRECT Molecule is an '
               'oxo fatty acid: it is acyclic, contains only C, H and O, has a '
               'single carboxylic acid group and an extra (aldehydic or '
               'ketonic) function.\n'
               ' * SMILES: C(CCCCCCCC(C(=O)O)=O)CC NAME: 2-oxododecanoic acid '
               'REASON: CORRECT Molecule is an oxo fatty acid: it is acyclic, '
               'contains only C, H and O, has a single carboxylic acid group '
               'and an extra (aldehydic or ketonic) function.\n'
               ' * SMILES: C(C(/C=C/C=C/C=C/[C@H](CCCC(O)=O)O)=O)/C=C\\CCCCC '
               'NAME: 12-oxo-6-trans-leukotriene B4 REASON: CORRECT Molecule '
               'is an oxo fatty acid: it is acyclic, contains only C, H and O, '
               'has a single carboxylic acid group and an extra (aldehydic or '
               'ketonic) function.\n'
               ' * SMILES: CC(C)CCCC(C)CCCC(C)CCC(=O)C(C)C(O)=O NAME: '
               '3-oxopristanic acid REASON: CORRECT Molecule is an oxo fatty '
               'acid: it is acyclic, contains only C, H and O, has a single '
               'carboxylic acid group and an extra (aldehydic or ketonic) '
               'function.\n'
               ' * SMILES: '
               'CCCCCC(=O)\\C=C\\C=C/C=C/C=C/[C@@H](O)[C@@H](O)CCCC(O)=O NAME: '
               '15-oxolipoxin A4 REASON: CORRECT Molecule is an oxo fatty '
               'acid: it is acyclic, contains only C, H and O, has a single '
               'carboxylic acid group and an extra (aldehydic or ketonic) '
               'function.\n'
               ' * SMILES: CC[C@@](C)(O)C(=O)C(O)=O NAME: '
               '(R)-3-hydroxy-3-methyl-2-oxopentanoic acid REASON: CORRECT '
               'Molecule is an oxo fatty acid: it is acyclic, contains only C, '
               'H and O, has a single carboxylic acid group and an extra '
               '(aldehydic or ketonic) function.\n'
               ' * SMILES: O=C(CC(=O)O)CC/C=C/[C@@H](C/C=C\\CCCCC)O NAME: '
               '(6E,8R,10Z)-8-hydroxy-3-oxohexadeca-6,10-dienoic acid REASON: '
               'CORRECT Molecule is an oxo fatty acid: it is acyclic, contains '
               'only C, H and O, has a single carboxylic acid group and an '
               'extra (aldehydic or ketonic) function.\n'
               ' * SMILES: C(CCCC(CCCCCCO)=O)CCCCC(O)=O NAME: '
               '16-hydroxy-10-oxohexadecanoic acid REASON: CORRECT Molecule is '
               'an oxo fatty acid: it is acyclic, contains only C, H and O, '
               'has a single carboxylic acid group and an extra (aldehydic or '
               'ketonic) function.\n'
               ' * SMILES: OC(=O)CCCCC=O NAME: 6-oxohexanoic acid REASON: '
               'CORRECT Molecule is an oxo fatty acid: it is acyclic, contains '
               'only C, H and O, has a single carboxylic acid group and an '
               'extra (aldehydic or ketonic) function.\n'
               ' * SMILES: CCCCCCCCCCCCCCC(=O)C(O)=O NAME: 2-oxohexadecanoic '
               'acid REASON: CORRECT Molecule is an oxo fatty acid: it is '
               'acyclic, contains only C, H and O, has a single carboxylic '
               'acid group and an extra (aldehydic or ketonic) function.\n'
               'False positives: SMILES: '
               'C(CCCCCC(=O)O)C/C=C/CC(/C=C(/C=C/CCO)\\O)=O NAME: '
               '(9E,13Z,15E)-14,18-dihydroxy-12-oxooctadeca-9,13,15-trienoic '
               'acid REASON: WRONGLY CLASSIFIED Molecule is an oxo fatty acid: '
               'it is acyclic, contains only C, H and O, has a single '
               'carboxylic acid group and an extra (aldehydic or ketonic) '
               'function.\n'
               ' * SMILES: O=C(CCCC)CCC(O)=O NAME: 4-keto-n-caprylic acid '
               'REASON: WRONGLY CLASSIFIED Molecule is an oxo fatty acid: it '
               'is acyclic, contains only C, H and O, has a single carboxylic '
               'acid group and an extra (aldehydic or ketonic) function.\n'
               ' * SMILES: O=C(CCC(O)=O)CC NAME: 4-keto-n-caproic acid REASON: '
               'WRONGLY CLASSIFIED Molecule is an oxo fatty acid: it is '
               'acyclic, contains only C, H and O, has a single carboxylic '
               'acid group and an extra (aldehydic or ketonic) function.\n'
               ' * SMILES: C(CCCCCCCCCCCC)CCCCCCC(CC(=O)O)=O NAME: '
               '3-oxodocosanoic acid REASON: WRONGLY CLASSIFIED Molecule is an '
               'oxo fatty acid: it is acyclic, contains only C, H and O, has a '
               'single carboxylic acid group and an extra (aldehydic or '
               'ketonic) function.\n'
               ' * SMILES: O=C(CCCCCCCC)C(=O)CCCCCCCC(O)=O NAME: '
               '9,10-Dioxo-octadecanoic acid REASON: WRONGLY CLASSIFIED '
               'Molecule is an oxo fatty acid: it is acyclic, contains only C, '
               'H and O, has a single carboxylic acid group and an extra '
               '(aldehydic or ketonic) function.\n'
               ' * SMILES: C(/C(=C/C=C(/C(O)=O)\\O)/C)=O NAME: '
               '(2Z,4E)-2-hydroxy-5-methyl-6-oxohexa-2,4-dienoic acid REASON: '
               'WRONGLY CLASSIFIED Molecule is an oxo fatty acid: it is '
               'acyclic, contains only C, H and O, has a single carboxylic '
               'acid group and an extra (aldehydic or ketonic) function.\n'
               ' * SMILES: O=C(CCCCCCCCCCCCCC)CCC(O)=O NAME: 4-keto stearic '
               'acid REASON: WRONGLY CLASSIFIED Molecule is an oxo fatty acid: '
               'it is acyclic, contains only C, H and O, has a single '
               'carboxylic acid group and an extra (aldehydic or ketonic) '
               'function.\n'
               ' * SMILES: CC(=C)C(CCC(C)=O)CC(O)=O NAME: '
               '3-isopropenyl-6-oxoheptanoic acid REASON: WRONGLY CLASSIFIED '
               'Molecule is an oxo fatty acid: it is acyclic, contains only C, '
               'H and O, has a single carboxylic acid group and an extra '
               '(aldehydic or ketonic) function.\n'
               ' * SMILES: OC(=O)CCC/C=C\\C/C=C\\C=C\\C=O NAME: '
               '12-oxo-dodeca-5,8,10-trienoic acid REASON: WRONGLY CLASSIFIED '
               'Molecule is an oxo fatty acid: it is acyclic, contains only C, '
               'H and O, has a single carboxylic acid group and an extra '
               '(aldehydic or ketonic) function.\n'
               ' * SMILES: C(CCCC(O)=O)CCCCCCCCC(C)=O NAME: 14-keto '
               'pentadecanoic acid REASON: WRONGLY CLASSIFIED Molecule is an '
               'oxo fatty acid: it is acyclic, contains only C, H and O, has a '
               'single carboxylic acid group and an extra (aldehydic or '
               'ketonic) function.\n'
               ' * SMILES: O=C(CCCCCCCCC)CCCCCCCC(O)=O NAME: 9-Oxooctadecanoic '
               'acid REASON: WRONGLY CLASSIFIED Molecule is an oxo fatty acid: '
               'it is acyclic, contains only C, H and O, has a single '
               'carboxylic acid group and an extra (aldehydic or ketonic) '
               'function.\n'
               ' * SMILES: C([H])(=O)[C@H](O)[C@@H](O)[C@@H](O)C(O)=O NAME: '
               'L-arabinuronic acid REASON: WRONGLY CLASSIFIED Molecule is an '
               'oxo fatty acid: it is acyclic, contains only C, H and O, has a '
               'single carboxylic acid group and an extra (aldehydic or '
               'ketonic) function.\n'
               ' * SMILES: [H]C(=O)C(\\C)=C(/O)\\C=C(/O)C(O)=O NAME: '
               'cis,cis-2,4-dihydroxy-5-methyl-6-oxo-2,4-hexadienoic acid '
               'REASON: WRONGLY CLASSIFIED Molecule is an oxo fatty acid: it '
               'is acyclic, contains only C, H and O, has a single carboxylic '
               'acid group and an extra (aldehydic or ketonic) function.\n'
               ' * SMILES: O[C@@H](C=O)[C@@H](O)[C@H](O)[C@@H](O)C(O)=O NAME: '
               'aldehydo-L-iduronic acid REASON: WRONGLY CLASSIFIED Molecule '
               'is an oxo fatty acid: it is acyclic, contains only C, H and O, '
               'has a single carboxylic acid group and an extra (aldehydic or '
               'ketonic) function.\n'
               ' * SMILES: O=C(O)CC/C=C/C(=O)CCCCCCCCCCCC NAME: N_12799 '
               'REASON: WRONGLY CLASSIFIED Molecule is an oxo fatty acid: it '
               'is acyclic, contains only C, H and O, has a single carboxylic '
               'acid group and an extra (aldehydic or ketonic) function.\n'
               ' * SMILES: O=C(CCCCCC(O)=O)CCC/C=C/CC NAME: '
               '7-oxo-11E-Tetradecenoic acid REASON: WRONGLY CLASSIFIED '
               'Molecule is an oxo fatty acid: it is acyclic, contains only C, '
               'H and O, has a single carboxylic acid group and an extra '
               '(aldehydic or ketonic) function.\n'
               ' * SMILES: CC[C@H](C)C(=O)C(O)=O NAME: '
               '(S)-3-methyl-2-oxovaleric acid REASON: WRONGLY CLASSIFIED '
               'Molecule is an oxo fatty acid: it is acyclic, contains only C, '
               'H and O, has a single carboxylic acid group and an extra '
               '(aldehydic or ketonic) function.\n'
               ' * SMILES: O=C(CCCCCCCCC(O)=O)C/C=C\\CCCCC NAME: '
               '10-oxo-12(Z)-octadecenoic acid REASON: WRONGLY CLASSIFIED '
               'Molecule is an oxo fatty acid: it is acyclic, contains only C, '
               'H and O, has a single carboxylic acid group and an extra '
               '(aldehydic or ketonic) function.\n'
               ' * SMILES: '
               'O=C(O)/C=C/C/C=C/C=C/C=C\\C=C\\C=C/C=C/C=C/C=C\\C=C\\C=C(\\C(=O)C)/C '
               'NAME: 2-Dehydro-3-deoxylaetiporic acid A REASON: WRONGLY '
               'CLASSIFIED Molecule is an oxo fatty acid: it is acyclic, '
               'contains only C, H and O, has a single carboxylic acid group '
               'and an extra (aldehydic or ketonic) function.\n'
               ' * SMILES: [H]C(=O)[C@@H](O)[C@@H](O)CC(=O)C(O)=O NAME: '
               '(4S,5S)-4,5-dihydroxy-2,6-dioxohexanoic acid REASON: WRONGLY '
               'CLASSIFIED Molecule is an oxo fatty acid: it is acyclic, '
               'contains only C, H and O, has a single carboxylic acid group '
               'and an extra (aldehydic or ketonic) function.\n'
               ' * SMILES: C(O)(=O)CCC/C=C/C/C=C/C=C\\C(=O)[H] NAME: '
               '12-oxo-5E,8E,10Z-dodecatrienoic acid REASON: WRONGLY '
               'CLASSIFIED Molecule is an oxo fatty acid: it is acyclic, '
               'contains only C, H and O, has a single carboxylic acid group '
               'and an extra (aldehydic or ketonic) function.\n'
               ' * SMILES: O=C(CCCCCCCCCCCCCCCCC)CCCCCCCCCC(O)=O NAME: '
               '11-keto-Octacosanoic acid REASON: WRONGLY CLASSIFIED Molecule '
               'is an oxo fatty acid: it is acyclic, contains only C, H and O, '
               'has a single carboxylic acid group and an extra (aldehydic or '
               'ketonic) function.\n'
               ' * SMILES: C(=O)(CC(=O)[C@H](O)[C@H](O)CO)O NAME: '
               '3-dehydro-2-deoxy-D-gluconic acid REASON: WRONGLY CLASSIFIED '
               'Molecule is an oxo fatty acid: it is acyclic, contains only C, '
               'H and O, has a single carboxylic acid group and an extra '
               '(aldehydic or ketonic) function.\n'
               ' * SMILES: O=C(CCCCCCCCCCCCCC(O)=O)CCC NAME: '
               '15-oxo-octadecanoic acid REASON: WRONGLY CLASSIFIED Molecule '
               'is an oxo fatty acid: it is acyclic, contains only C, H and O, '
               'has a single carboxylic acid group and an extra (aldehydic or '
               'ketonic) function.\n'
               ' * SMILES: [H][C@](O)(C=O)[C@@]([H])(O)[C@]([H])(O)C(O)=O '
               'NAME: D-xyluronic acid REASON: WRONGLY CLASSIFIED Molecule is '
               'an oxo fatty acid: it is acyclic, contains only C, H and O, '
               'has a single carboxylic acid group and an extra (aldehydic or '
               'ketonic) function.\n'
               'False negatives: SMILES: '
               'CC\\C(\\C=C\\[C@@H]1OC(=O)C=C[C@@H]1C)=C\\[C@H](C)C\\C=C\\C(\\C)=C\\[C@@H](C)C(=O)[C@@H](C)[C@H](O)[C@@H](C)C\\C(C)=C\\C(O)=O '
               'NAME: leptomycin B REASON: MISSED Molecule contains rings and '
               'does not appear to be a linear fatty acid.\n'
               ' * SMILES: C(CC1C(/C=C/C(CCCCCCCC(O)=O)=O)O1)CCC NAME: '
               '12(13)Ep-9-KODE REASON: MISSED Molecule contains rings and '
               'does not appear to be a linear fatty acid.\n'
               ' * SMILES: CC\\C=C/C[C@@H]1[C@H](CCCCCCCC(O)=O)CCC1=O NAME: '
               '8-[(1R,2R)-3-oxo-2-{(Z)-pent-2-en-1-yl}cyclopentyl]octanoic '
               'acid REASON: MISSED Molecule contains rings and does not '
               'appear to be a linear fatty acid.\n'
               ' * SMILES: CC\\C=C/C[C@H]1[C@@H](CCCCCCCC(O)=O)CCC1=O NAME: '
               '8-[(1S,2S)-3-oxo-2-{(Z)-pent-2-en-1-yl}cyclopentyl]octanoic '
               'acid REASON: MISSED Molecule contains rings and does not '
               'appear to be a linear fatty acid.\n'
               ' * SMILES: C=1C([C@@H](C/C=C\\CC)[C@H](C1)CCCCCC(=O)O)=O NAME: '
               '6-{(1S,5S)-4-oxo-5-[(2Z)-pent-2-en-1-yl]cyclopent-2-en-1-yl}hexanoic '
               'acid REASON: MISSED Molecule contains rings and does not '
               'appear to be a linear fatty acid.\n'
               ' * SMILES: CC\\C=C/CC1C(CCCCCCCC(O)=O)CCC1=O NAME: '
               '8-{3-oxo-2-[(2Z)-pent-2-en-1-yl]cyclopentyl}octanoic acid '
               'REASON: MISSED Molecule contains rings and does not appear to '
               'be a linear fatty acid.\n'
               ' * SMILES: C(CCCCC[C@H]1[C@H](C(CC1)=O)C/C=C\\CC)(O)=O NAME: '
               '(9R,13R)-1a,1b-dinor-10,11-dihydro-12-oxo-15-phytoenoic acid '
               'REASON: MISSED Molecule contains rings and does not appear to '
               'be a linear fatty acid.\n'
               ' * SMILES: '
               'C[C@H](C\\C=C\\C(\\C)=C\\[C@@H](C)C(=O)[C@@H](C)[C@H](O)[C@@H](C)C\\C(C)=C\\C(O)=O)\\C=C(/C)\\C=C\\[C@@H]1OC(=O)C=C[C@@H]1C '
               'NAME: leptomycin A REASON: MISSED Molecule contains rings and '
               'does not appear to be a linear fatty acid.\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'O(C1=CC(=C(C(=C1)I)O)I)C=2C(=CC(=CC2I)CC(O)=O)I',
                                     'name': "3,3',5,5'-tetraiodothyroacetic "
                                             'acid',
                                     'reason': 'Molecule contains elements '
                                               'other than C, H, and O.'},
                                 {   'smiles': 'COCC#CC1=CC=C(C=C1)[C@H]2[C@@H]3CN(CCCCN3[C@H]2CO)C(=O)NC4CCCC4',
                                     'name': '(8R,9S,10R)-N-cyclopentyl-10-(hydroxymethyl)-9-[4-(3-methoxyprop-1-ynyl)phenyl]-1,6-diazabicyclo[6.2.0]decane-6-carboxamide',
                                     'reason': 'Molecule contains elements '
                                               'other than C, H, and O.'},
                                 {   'smiles': 'O([C@@H]1[C@H](O)[C@H](O[C@H]2[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]2CO)O[C@H]3[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]3CO)O)O[C@@H]([C@H]1O)CO[C@H]4O[C@@H]([C@@H](O)[C@H](O)[C@@H]4O[C@@H]5O[C@@H]([C@@H](O[C@@H]6O[C@@H]([C@H](O)[C@H](O)[C@H]6O)CO)[C@H](O)[C@H]5NC(=O)C)CO)CO)[C@H]7O[C@@H]([C@@H](O)[C@H](O)[C@@H]7O[C@@H]8O[C@@H]([C@@H](O[C@@H]9O[C@@H]([C@H](O)[C@H](O)[C@H]9O[C@@H]%10O[C@H]([C@@H](O)[C@@H](O)[C@@H]%10O)C)CO)[C@H](O)[C@H]8NC(=O)C)CO)CO',
                                     'name': 'N-[(2R,3R,4R,5S,6R)-5-[(2S,3R,4R,5S,6R)-3-Acetamido-5-[(2S,3S,4S,5R,6R)-4-[(2R,3S,4S,5S,6R)-3-[(2S,3R,4R,5S,6R)-3-acetamido-5-[(2S,3R,4S,5R,6R)-4,5-dihydroxy-6-(hydroxymethyl)-3-[(2S,3S,4R,5S,6S)-3,4,5-trihydroxy-6-methyloxan-2-yl]oxyoxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-6-[[(2S,3S,4S,5S,6R)-3-[(2S,3R,4R,5S,6R)-3-acetamido-4-hydroxy-6-(hydroxymethyl)-5-[(2S,3R,4S,5R,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxymethyl]-3,5-dihydroxyoxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-2,4-dihydroxy-6-(hydroxymethyl)oxan-3-yl]acetamide',
                                     'reason': 'Molecule contains elements '
                                               'other than C, H, and O.'},
                                 {   'smiles': 'O(C(=O)CCCCCCCCCCCCCCCCC(C)C)C[C@@H](OC(=O)CCCCCCCCCCC)CO',
                                     'name': 'DG(i-20:0/12:0/0:0)',
                                     'reason': 'Molecule appears too branched '
                                               'to be a typical linear fatty '
                                               'acid.'},
                                 {   'smiles': 'CCC(=O)N1C[C@H]2[C@@H]([C@@H](N2C(=O)C1)CO)C3=CC=C(C=C3)C#CC4=CN=CC=C4',
                                     'name': '(6R,7S,8R)-8-(hydroxymethyl)-4-(1-oxopropyl)-7-[4-[2-(3-pyridinyl)ethynyl]phenyl]-1,4-diazabicyclo[4.2.0]octan-2-one',
                                     'reason': 'Molecule contains elements '
                                               'other than C, H, and O.'},
                                 {   'smiles': 'O(C(C[N+](C)(C)C)CC([O-])=O)C(=O)CC/C=C/C/C=C/C/C=C/C\\C=C\\CC(O)/C=C/C=C/CC',
                                     'name': '(4Z,7Z,10Z,13Z,17Z,19Z)-16-Hydroxydocosa-4,7,10,13,17,19-hexaenoylcarnitine',
                                     'reason': 'Molecule contains elements '
                                               'other than C, H, and O.'},
                                 {   'smiles': 'O([C@H]1[C@H](O)[C@@H](NC(=O)C)[C@H](O[C@H]2[C@H](O[C@H]3O[C@H]([C@@H](O)[C@@H](O)[C@@H]3O)C)[C@@H](NC(=O)C)[C@@H](O[C@@H]2CO)O)O[C@@H]1CO)[C@@H]4O[C@@H]([C@@H](O)[C@H](O[C@H]5O[C@@H]([C@@H](O)[C@H](O)[C@@H]5O)CO)[C@@H]4O[C@@H]6OC[C@@H](O)[C@H](O)[C@H]6O)CO',
                                     'name': 'N-[(2S,3R,4R,5S,6R)-2-[(2R,3S,4R,5R,6R)-5-Acetamido-6-hydroxy-2-(hydroxymethyl)-4-[(2R,3S,4R,5S,6S)-3,4,5-trihydroxy-6-methyloxan-2-yl]oxyoxan-3-yl]oxy-4-hydroxy-5-[(2S,3S,4S,5R,6R)-5-hydroxy-6-(hydroxymethyl)-4-[(2R,3S,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-3-[(2S,3R,4S,5R)-3,4,5-trihydroxyoxan-2-yl]oxyoxan-2-yl]oxy-6-(hydroxymethyl)oxan-3-yl]acetamide',
                                     'reason': 'Molecule contains elements '
                                               'other than C, H, and O.'},
                                 {   'smiles': 'O(C=1C=2C(C(OC(=O)CCC)=CC1C)=CC=CC2)C(=O)CCC',
                                     'name': 'Menadiol dibutyrate',
                                     'reason': 'Molecule contains rings and '
                                               'does not appear to be a linear '
                                               'fatty acid.'},
                                 {   'smiles': 'N1(CCCCC1)C=2C(=CC=CC2)C#N',
                                     'name': '2-piperidinobenzonitrile',
                                     'reason': 'Molecule contains elements '
                                               'other than C, H, and O.'},
                                 {   'smiles': 'COc1cc2c(cc1C)C(=CC(=O)[C@]2(C)O)C(C)C',
                                     'name': 'Lacinilene C 7-methyl ether',
                                     'reason': 'Molecule contains rings and '
                                               'does not appear to be a linear '
                                               'fatty acid.'}],
    'sample_false_negatives': [   {   'smiles': 'CCC(O)CC(=O)C(O)=O',
                                      'name': '4-hydroxy-2-oxohexanoic acid',
                                      'reason': 'Molecule does not appear to '
                                                'contain an additional '
                                                '(non–acid) aldehydic or '
                                                'ketonic group.'},
                                  {   'smiles': 'CCCC(=O)C(O)=O',
                                      'name': '2-oxopentanoic acid',
                                      'reason': 'Molecule does not appear to '
                                                'contain an additional '
                                                '(non–acid) aldehydic or '
                                                'ketonic group.'},
                                  {   'smiles': 'CCC(C)(O)C(=O)C(O)=O',
                                      'name': '3-hydroxy-3-methyl-2-oxopentanoic '
                                              'acid',
                                      'reason': 'Molecule does not appear to '
                                                'contain an additional '
                                                '(non–acid) aldehydic or '
                                                'ketonic group.'},
                                  {   'smiles': 'CC\\C(\\C=C\\[C@@H]1OC(=O)C=C[C@@H]1C)=C\\[C@H](C)C\\C=C\\C(\\C)=C\\[C@@H](C)C(=O)[C@@H](C)[C@H](O)[C@@H](C)C\\C(C)=C\\C(O)=O',
                                      'name': 'leptomycin B',
                                      'reason': 'Molecule contains rings and '
                                                'does not appear to be a '
                                                'linear fatty acid.'},
                                  {   'smiles': 'C(CCCCCCCC(C(=O)O)=O)CC',
                                      'name': '2-oxododecanoic acid',
                                      'reason': 'Molecule does not appear to '
                                                'contain an additional '
                                                '(non–acid) aldehydic or '
                                                'ketonic group.'},
                                  {   'smiles': 'CC(C)CCCC(C)CCCC(C)CCC(=O)C(C)C(O)=O',
                                      'name': '3-oxopristanic acid',
                                      'reason': 'The carboxylic acid group is '
                                                'not located at the terminus '
                                                'of the main carbon chain.'},
                                  {   'smiles': 'C(CC1C(/C=C/C(CCCCCCCC(O)=O)=O)O1)CCC',
                                      'name': '12(13)Ep-9-KODE',
                                      'reason': 'Molecule contains rings and '
                                                'does not appear to be a '
                                                'linear fatty acid.'},
                                  {   'smiles': 'CC[C@@](C)(O)C(=O)C(O)=O',
                                      'name': '(R)-3-hydroxy-3-methyl-2-oxopentanoic '
                                              'acid',
                                      'reason': 'Molecule does not appear to '
                                                'contain an additional '
                                                '(non–acid) aldehydic or '
                                                'ketonic group.'},
                                  {   'smiles': 'CC\\C=C/C[C@@H]1[C@H](CCCCCCCC(O)=O)CCC1=O',
                                      'name': '8-[(1R,2R)-3-oxo-2-{(Z)-pent-2-en-1-yl}cyclopentyl]octanoic '
                                              'acid',
                                      'reason': 'Molecule contains rings and '
                                                'does not appear to be a '
                                                'linear fatty acid.'},
                                  {   'smiles': 'CCCCCCCCCCCCCCC(=O)C(O)=O',
                                      'name': '2-oxohexadecanoic acid',
                                      'reason': 'Molecule does not appear to '
                                                'contain an additional '
                                                '(non–acid) aldehydic or '
                                                'ketonic group.'}],
    'attempt': 5,
    'reasoning': 'Below is one solution. In my reasoning I noticed that many '
                 'false‐positives and false‐negatives arose because the '
                 'earlier scheme did not check that the acid group lies at a '
                 'terminus of a “fatty” (i.e. long and mostly linear) carbon '
                 'chain—and that extra carbonyl functions should be both '
                 '“distant enough” from the acid function (so they are not '
                 'just part of an unusual acid motif) and not simply accepted '
                 'when they lie at a chain end in a too‐short molecule. In the '
                 'revised code I (1) confirm that (a) the molecule is composed '
                 'only of C, H and O, (b) it is acyclic and (c) has at least '
                 'five carbons; (2) I compute the longest carbon chain (and '
                 'require that it covers at least 70% of all carbons); (3) I '
                 'require exactly one carboxylic acid group (using a SMARTS) '
                 'and, importantly, that the acid carbon is one endpoint of '
                 'that longest chain; and (4) I then search for an extra '
                 'ketone or aldehyde (using SMARTS patterns) that is not the '
                 'acid carbon and is “distant” (i.e. at least two bonds away) '
                 'from the acid. In addition, if the candidate extra oxo is '
                 'located at one end the chain, we require that the longest '
                 'chain is long (≥10 carbons) to avoid false‐positives on very '
                 'short molecules. This approach seems to improve the F₁ score '
                 'by filtering out many of the false positives while still '
                 'accepting our “true positive” examples.\n'
                 '\n'
                 'Below is the complete Python code:\n'
                 '\n'
                 '------------------------------------------------',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 57,
    'num_false_positives': 207,
    'num_true_negatives': 142020,
    'num_false_negatives': 16,
    'num_negatives': None,
    'precision': 0.2159090909090909,
    'recall': 0.7808219178082192,
    'f1': 0.33827893175074186,
    'accuracy': 0.9984328882642305,
    'negative_predictive_value': 0.9998873525021825}