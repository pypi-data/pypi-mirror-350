"""
Classifies: CHEBI:35819 branched-chain fatty acid
"""
#!/usr/bin/env python
"""
Classifies: branched-chain fatty acid (BCFA).

A branched-chain fatty acid (BCFA) is a fatty acid (a carboxylic acid with a long aliphatic acyl chain)
that has one or more alkyl substituents (typically a methyl or similarly short branch) on its main chain.
This implementation:
  • Rejects molecules that contain atoms besides carbon and oxygen.
  • Checks that the oxygen count is typical for a fatty acid (either 2 or 3 oxygens).
  • Locates a single carboxyl group (–COOH or deprotonated –COO–).
  • Identifies the alpha carbon (the first carbon attached to the carboxyl carbon).
  • Builds a graph of acyclic (non‐ring) carbon atoms (the fatty acyl chain is assumed acyclic).
  • Uses depth‐first search (DFS) from the alpha carbon to find the longest “main chain”.
  • For each carbon in that main chain, examines neighboring acyclic carbons not on the main chain.
    If such a “branch” is detected and its total number of carbons is short (≤ 3 atoms), it is
    considered a valid alkyl substituent, and the molecule classifies as a BCFA.
    
Note: This is a heuristic approach; different thresholds (minimum main chain length, branch length)
and additional filters (such as rejecting molecules with multiple carboxy groups) can be applied.
"""

from rdkit import Chem

def is_branched_chain_fatty_acid(smiles: str):
    """
    Determines if a molecule is a branched-chain fatty acid (BCFA) based on its SMILES string.
    
    The algorithm:
      1. Parses the molecule and rejects those with atoms besides C and O.
      2. Verifies that the overall oxygen count is what we expect (2 or 3 atoms).
      3. Uses SMARTS to locate a single carboxyl group (-COOH or its deprotonated form).
      4. Finds the alpha carbon (first non-ring carbon attached to the carboxyl carbon).
      5. Constructs a connectivity graph of all acyclic carbon atoms.
      6. Uses DFS to determine the longest acyclic chain (the “main chain”) starting at the alpha carbon.
      7. For each main-chain carbon, any neighboring acyclic carbons that are not part
         of the main chain are explored. If the branch (its total number of carbon atoms)
         is small (≤ 3 atoms), then it is considered an alkyl substituent, and the molecule
         is declared a BCFA.
    
    Args:
        smiles (str): SMILES string of the molecule.
    
    Returns:
        bool: True if molecule is classified as a branched-chain fatty acid, else False.
        str: A brief explanation for the classification decision.
    """
    # Parse the SMILES string.
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
    
    # Step 1: Only allow carbon and oxygen (hydrogens are implicit).
    allowed_atomic_nums = {6, 8}
    for atom in mol.GetAtoms():
        if atom.GetAtomicNum() not in allowed_atomic_nums:
            return False, f"Contains atom {atom.GetSymbol()} (atomic number {atom.GetAtomicNum()}), not typical for a fatty acid"
    
    # Step 2: Check total oxygen count.
    ox_count = sum(1 for atom in mol.GetAtoms() if atom.GetAtomicNum() == 8)
    if ox_count not in {2, 3}:
        return False, f"Oxygen count of {ox_count} not typical for a fatty acid (expected 2 or 3)"
    
    # Step 3: Find the carboxyl group.
    # This SMARTS covers both -COOH and deprotonated -COO–.
    carboxyl_smarts = "[CX3](=O)[OX1H0-,OX2H1]"
    carboxyl_query = Chem.MolFromSmarts(carboxyl_smarts)
    carboxyl_matches = mol.GetSubstructMatches(carboxyl_query)
    if not carboxyl_matches:
        return False, "No carboxyl group found; not a fatty acid"
    if len(carboxyl_matches) != 1:
        return False, "Multiple carboxyl groups detected; not a typical fatty acid"
    # In the SMARTS, the first atom is the carboxyl (carbonyl) carbon.
    carboxyl_C_idx = carboxyl_matches[0][0]
    carboxyl_atom = mol.GetAtomWithIdx(carboxyl_C_idx)
    
    # Step 4: Identify the alpha carbon.
    alpha_carbon_idx = None
    for nbr in carboxyl_atom.GetNeighbors():
        if nbr.GetAtomicNum() == 6 and not nbr.IsInRing():
            alpha_carbon_idx = nbr.GetIdx()
            break
    if alpha_carbon_idx is None:
        return False, "No suitable alpha carbon attached to the carboxyl group; not a fatty acid"
    
    # Step 5: Build the acyclic carbon graph.
    # We only consider carbon atoms that are not in a ring.
    acyclic_carbon_indices = [atom.GetIdx() for atom in mol.GetAtoms() if atom.GetAtomicNum() == 6 and not atom.IsInRing()]
    if not acyclic_carbon_indices:
        return False, "No acyclic carbon atoms found"
    acyclic_carbon_set = set(acyclic_carbon_indices)
    # Build a dictionary mapping each acyclic carbon index to its neighboring acyclic carbons.
    carbon_graph = { idx: [] for idx in acyclic_carbon_set }
    for idx in acyclic_carbon_set:
        atom = mol.GetAtomWithIdx(idx)
        for nbr in atom.GetNeighbors():
            if nbr.GetAtomicNum() == 6 and nbr.GetIdx() in acyclic_carbon_set:
                carbon_graph[idx].append(nbr.GetIdx())
    
    # Step 6: Determine the main (longest) acyclic chain starting at the alpha carbon.
    # We use DFS (disallowing revisiting nodes) to find the longest path.
    def dfs_longest(current, visited):
        longest_path = [current]
        for nbr in carbon_graph.get(current, []):
            if nbr in visited:
                continue
            candidate_path = [current] + dfs_longest(nbr, visited | {nbr})
            if len(candidate_path) > len(longest_path):
                longest_path = candidate_path
        return longest_path

    main_chain = dfs_longest(alpha_carbon_idx, {alpha_carbon_idx})
    if len(main_chain) < 2:
        return False, "Alkyl chain too short to be considered a fatty acid"
    
    # Step 7: For every atom in the main chain, check for branch substituents.
    # A valid branch here is a connected set of acyclic carbons, disjoint from the main chain,
    # with a small total number of carbons (here, we require size <= 3, e.g. methyl, ethyl, or propyl).
    main_chain_set = set(main_chain)
    # Helper: given a starting branch atom, get all connected branch carbons (disallowing main-chain atoms).
    def get_branch_atoms(start):
        branch_atoms = set()
        stack = [start]
        while stack:
            cur = stack.pop()
            if cur in branch_atoms:
                continue
            branch_atoms.add(cur)
            for nb in carbon_graph.get(cur, []):
                if nb in main_chain_set:
                    continue
                if nb not in branch_atoms:
                    stack.append(nb)
        return branch_atoms

    for idx in main_chain:
        for nbr in carbon_graph.get(idx, []):
            if nbr not in main_chain_set:
                branch_atoms = get_branch_atoms(nbr)
                branch_size = len(branch_atoms)
                # For a typical BCFA, the branch (alkyl substituent) is very short.
                if branch_size <= 3:
                    return True, f"Branching detected at main chain carbon atom index {idx} (branch size: {branch_size})"
    
    return False, "No suitable short branching substituents detected on the fatty acyl chain"

# Example usage (for debugging/testing):
if __name__ == '__main__':
    test_smiles = [
        "OC(=O)CC(C)=C",                         # isopropenylacetic acid: expected BCFA
        "CCC(C)CCCCCCCCCCCCCCCCCCCCCCCCCCC(O)=O", # 28-methyltriacontanoic acid: expected BCFA
        "OC(=O)CCCCCCCC",                         # linear fatty acid: expected NOT BCFA
        "OC(=O)C(CC)CC",                          # 2-Ethylbutanoic acid: expected BCFA
    ]
    for s in test_smiles:
        result, reason = is_branched_chain_fatty_acid(s)
        print(s, "->", result, ":", reason)


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:35819',
                          'name': 'branched-chain fatty acid',
                          'definition': 'Any fatty acid in which the parent '
                                        'hydrocarbon chain has one or more '
                                        'alkyl substituents; a common '
                                        'component in animal and bacterial '
                                        'lipids. The fatty acyl chain is '
                                        'usually saturated and the substituent '
                                        'a methyl group; however, unsaturated '
                                        'BCFAs are found in marine animals, '
                                        'and branches other than methyl are '
                                        'found in microbial lipids.',
                          'parents': ['CHEBI:35366'],
                          'xrefs': ['KEGG:C05996', 'PMID:18318842'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 116,
                           'log_lines_of_code': 4.7535901911063645,
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
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 3,
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
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 3,
                                                 3,
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
                                                 2,
                                                 3,
                                                 4,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 3,
                                                 4,
                                                 3,
                                                 3,
                                                 4,
                                                 2,
                                                 0,
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
                                                 2,
                                                 2,
                                                 3,
                                                 3,
                                                 4,
                                                 3,
                                                 3,
                                                 4,
                                                 5,
                                                 4,
                                                 5,
                                                 2,
                                                 0,
                                                 1,
                                                 2,
                                                 3,
                                                 4,
                                                 4,
                                                 4,
                                                 4,
                                                 5,
                                                 1,
                                                 1,
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
                           'max_indent': 5,
                           'imports': ['from rdkit import Chem'],
                           'imports_count': 1,
                           'methods_called': [   'GetSymbol',
                                                 'GetNeighbors',
                                                 'add',
                                                 'GetAtoms',
                                                 'MolFromSmarts',
                                                 'IsInRing',
                                                 'GetIdx',
                                                 'pop',
                                                 'get',
                                                 'GetSubstructMatches',
                                                 'GetAtomWithIdx',
                                                 'MolFromSmiles',
                                                 'GetAtomicNum',
                                                 'append'],
                           'methods_called_count': 14,
                           'smarts_strings': ['carboxyl_smarts'],
                           'smarts_strings_count': 1,
                           'defs': [   'is_branched_chain_fatty_acid(smiles: '
                                       'str):',
                                       'dfs_longest(current, visited):',
                                       'get_branch_atoms(start):'],
                           'defs_count': 3,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, f"Contains atom '
                                          '{atom.GetSymbol()} (atomic number '
                                          '{atom.GetAtomicNum()}), not typical '
                                          'for a fatty acid"',
                                          'False, f"Oxygen count of {ox_count} '
                                          'not typical for a fatty acid '
                                          '(expected 2 or 3)"',
                                          'False, "No carboxyl group found; '
                                          'not a fatty acid"',
                                          'False, "Multiple carboxyl groups '
                                          'detected; not a typical fatty acid"',
                                          'False, "No suitable alpha carbon '
                                          'attached to the carboxyl group; not '
                                          'a fatty acid"',
                                          'False, "No acyclic carbon atoms '
                                          'found"',
                                          'longest_path',
                                          'False, "Alkyl chain too short to be '
                                          'considered a fatty acid"',
                                          'branch_atoms',
                                          'True, f"Branching detected at main '
                                          'chain carbon atom index {idx} '
                                          '(branch size: {branch_size})"',
                                          'False, "No suitable short branching '
                                          'substituents detected on the fatty '
                                          'acyl chain"'],
                           'returns_count': 12,
                           'complexity': 7.750718038221272},
    'message': '\n'
               'Attempt failed: F1 score of 0.042767963873024305 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: OC(=O)CC(C)=C NAME: Isopropenylacetic '
               'acid REASON: CORRECT Branching detected at main chain carbon '
               'atom index 3\n'
               ' * SMILES: '
               'C(CCCCCCCCC1C(CCCCCCCCCCC2C(CCCCCCCCCCCCCCCCCCCCC[C@@H](O)[C@H](C(O)=O)CCCCCCCCCCCCCCCCCCCCCCCC)C2)C1)CCCCCCCCC '
               'NAME: '
               '(2R)-2-[(1R)-1-hydroxy-22-{2-[10-(2-octadecylcyclopropyl)decyl]cyclopropyl}docosyl]hexacosanoic '
               'acid REASON: CORRECT Branching detected at main chain carbon '
               'atom index 46\n'
               ' * SMILES: CCC(C)CCCCCCCCCCCCCCCCCCCCCCCCCCC(O)=O NAME: '
               '28-methyltriacontanoic acid REASON: CORRECT Branching detected '
               'at main chain carbon atom index 29\n'
               ' * SMILES: CCC(C)CCCCCCCCCCCCC(O)=O NAME: '
               '14-methylhexadecanoic acid REASON: CORRECT Branching detected '
               'at main chain carbon atom index 15\n'
               ' * SMILES: CC(C)CCCCCCCCCC(O)=O NAME: isotridecanoic acid '
               'REASON: CORRECT Branching detected at main chain carbon atom '
               'index 11\n'
               ' * SMILES: CC(C)CCCCCCCCCCCCCCCCCCCCCCC(O)=O NAME: '
               '24-methylpentacosanoic acid REASON: CORRECT Branching detected '
               'at main chain carbon atom index 24\n'
               ' * SMILES: OC(=O)C(CC)CC NAME: 2-Ethylbutanoic acid REASON: '
               'CORRECT Branching detected at main chain carbon atom index 3\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCCCCCCCC[C@H]([C@H](O)CCCCCCCCCCC[C@@H]1C[C@@H]1CCCCCCCCCCCCCC[C@@H]1C[C@@H]1CCCCCCCCCCCCCCCCCCCC)C(O)=O '
               'NAME: '
               '(2R)-2-{(1R)-1-hydroxy-12-[(1R,2S)-2-{14-[(1R,2S)-2-icosylcyclopropyl]tetradecyl}cyclopropyl]dodecyl}hexacosanoic '
               'acid REASON: CORRECT Branching detected at main chain carbon '
               'atom index 24\n'
               ' * SMILES: OC(=O)C(CCC)CC NAME: alpha-ethyl valeric acid '
               'REASON: CORRECT Branching detected at main chain carbon atom '
               'index 3\n'
               ' * SMILES: CCC(C)CCCCCCCCCCCCCCCCCCC(O)=O NAME: '
               '20-methyldocosanoic acid REASON: CORRECT Branching detected at '
               'main chain carbon atom index 21\n'
               ' * SMILES: C[C@@H](O)CC[C@H](CC(O)=O)C(C)=C NAME: '
               '(3R,6R)-6-hydroxy-3-isopropenylheptanoic acid REASON: CORRECT '
               'Branching detected at main chain carbon atom index 6\n'
               ' * SMILES: CCC(C)C(O)=O NAME: 2-methylbutyric acid REASON: '
               'CORRECT Branching detected at main chain carbon atom index 2\n'
               ' * SMILES: '
               'C\\C(CO)=C/CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\C(O)=O NAME: '
               '(2E,6E,10E,14E)-omega-hydroxygeranylgeranic acid REASON: '
               'CORRECT Branching detected at main chain carbon atom index 19\n'
               ' * SMILES: CC(C)CCCCCCCCCCCCCCCCCCC(O)=O NAME: '
               '20-methylhenicosanoic acid REASON: CORRECT Branching detected '
               'at main chain carbon atom index 20\n'
               ' * SMILES: CC[C@@H](C)C(O)=O NAME: (R)-2-methylbutyric acid '
               'REASON: CORRECT Branching detected at main chain carbon atom '
               'index 2\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCCCCCCC(C(O)CCCCCCCCCCCCCCCCCC1CC1CCCCCCCCCCCCCCCCC(=O)C(C)CCCCCCCCCCCCCCCCCC)C(O)=O '
               'NAME: keto mycolic acid REASON: CORRECT Branching detected at '
               'main chain carbon atom index 22\n'
               ' * SMILES: CCC(C)CCCCCCCCCCCCCCCCCCCCCCC(O)=O NAME: '
               '24-methylhexacosanoic acid REASON: CORRECT Branching detected '
               'at main chain carbon atom index 25\n'
               ' * SMILES: '
               'C(CCCCCC1C(C1)CCCCCCCCCCCCC[C@@H](O)[C@H](C(O)=O)CCCCCCCCCCCCCCCCCCCCCCCC)CCCCCCCC/C=C\\CCCCCCCCCCCCCCCCCCCC '
               'NAME: '
               '(2R)-2-[(1R)-14-{2-[(15Z)-hexatriacont-15-en-1-yl]cyclopropyl}-1-hydroxytetradecyl]hexacosanoic '
               'acid REASON: CORRECT Branching detected at main chain carbon '
               'atom index 24\n'
               ' * SMILES: '
               'C(CCCCCCCCC1C(CCCCCCCCCCC2C(CCCCCCCCCCCCCCCCC[C@@H](O)[C@H](C(O)=O)CCCCCCCCCCCCCCCCCCCCCCCC)C2)C1)CCCCCCCCCC '
               'NAME: '
               '(2R)-2-[(1R)-1-hydroxy-18-{2-[10-(2-nonadecylcyclopropyl)decyl]cyclopropyl}octadecyl]hexacosanoic '
               'acid REASON: CORRECT Branching detected at main chain carbon '
               'atom index 42\n'
               ' * SMILES: CCC(C)CCCCCCCCCCC(O)=O NAME: 12-methyltetradecanoic '
               'acid REASON: CORRECT Branching detected at main chain carbon '
               'atom index 13\n'
               ' * SMILES: CC(C)C[C@@H](O)C(O)=O NAME: '
               '(R)-2-hydroxy-4-methylpentanoic acid REASON: CORRECT Branching '
               'detected at main chain carbon atom index 4\n'
               ' * SMILES: OC(=O)\\C=C\\C(C)C NAME: 4-Methyl-2-pentenoic acid '
               'REASON: CORRECT Branching detected at main chain carbon atom '
               'index 3\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCCCCCCC(C(O)CCCCCCCCCCCCCCCC\\C=C\\CCCCCCCCCCCCCCCCCC(=O)OC(C)CCCCCCCCCCCCCCCCC)C(O)=O '
               'NAME: '
               '(20E)-2-docosyl-3-hydroxy-39-(nonadecan-2-yloxy)-39-oxononatriacont-20-enoic '
               'acid REASON: CORRECT Branching detected at main chain carbon '
               'atom index 22\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCCCCCCCC[C@H]([C@H](O)CCCCCCCCCCC[C@H]1C[C@H]1CCCCCCCCCCCCCC[C@H]1C[C@H]1CCCCCCCCCCCCCCCCCCCC)C(O)=O '
               'NAME: '
               '(2R)-2-{(1R)-1-hydroxy-12-[(1S,2R)-2-{14-[(1S,2R)-2-icosylcyclopropyl]tetradecyl}cyclopropyl]dodecyl}hexacosanoic '
               'acid REASON: CORRECT Branching detected at main chain carbon '
               'atom index 24\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCCCCCCCC[C@H]([C@H](O)CCCCCCCCCCCCCCCC[C@@H]1C[C@@H]1[C@H](C)CCCCCCCCCCCCCCCCCCC(=O)C(C)CCCCCCCCCCCCCCCCCC)C(O)=O '
               'NAME: '
               '(2R)-2-[(1R)-1-hydroxy-17-{(1R,2R)-2-[(2R)-22-methyl-21-oxotetracontan-2-yl]cyclopropyl}heptadecyl]hexacosanoic '
               'acid REASON: CORRECT Branching detected at main chain carbon '
               'atom index 24\n'
               'False positives: SMILES: '
               'O=C(O)/C(=C/[C@H]1C=C(CC[C@@H]1C(C)C)CO)/COC(=O)C NAME: '
               '3-acetylgliocladic acid REASON: WRONGLY CLASSIFIED Branching '
               'detected at main chain carbon atom index 3\n'
               ' * SMILES: '
               'C[C@@H]([C@H]1CC[C@H]2[C@H](CCc3cc(O)ccc3C)C(=O)CC[C@]12C)C(O)=O '
               'NAME: '
               '3-hydroxy-9-oxo-9,10-seco-23,24-bisnorchola-1,3,5(10)-trien-22-oic '
               'acid REASON: WRONGLY CLASSIFIED Branching detected at main '
               'chain carbon atom index 1\n'
               ' * SMILES: COC(=O)CCC(O)=O NAME: monomethyl succinate REASON: '
               'WRONGLY CLASSIFIED Branching detected at main chain carbon '
               'atom index 5\n'
               ' * SMILES: OC(CC([O-])=O)C([O-])=O NAME: malate(2-) REASON: '
               'WRONGLY CLASSIFIED Branching detected at main chain carbon '
               'atom index 2\n'
               ' * SMILES: OCC(=O)[C@@H](O)[C@H](O)[C@H](O)C([O-])=O NAME: '
               'keto-D-fructuronate REASON: WRONGLY CLASSIFIED Branching '
               'detected at main chain carbon atom index 8\n'
               ' * SMILES: OC(=O)CC\\C=C\\C\\C=C\\C\\C=C\\C\\C=C\\CCCCCCCC '
               'NAME: 4,7,10,13-Docosatetraenoic acid REASON: WRONGLY '
               'CLASSIFIED Branching detected at main chain carbon atom index '
               '3\n'
               ' * SMILES: CCCCC\\C=C/C\\C=C/CC(O)C(O)C\\C=C/CCCC([O-])=O '
               'NAME: (5Z,11Z,14Z)-8,9-dihydroxyicosatrienoate REASON: WRONGLY '
               'CLASSIFIED Branching detected at main chain carbon atom index '
               '20\n'
               ' * SMILES: '
               'O=C1OC(=O)C2C(C(C(C)=CC3C2CCC(C3O[C@H]4O[C@H]([C@H](O)C([C@@H]4O)O)C)C)/C=C/C=C/C=C(/CC(CC(O)C(C(=O)O)C)C)\\C)=C5C(=C1C)CC(O)C5C '
               'NAME: Aurantinin C REASON: WRONGLY CLASSIFIED Branching '
               'detected at main chain carbon atom index 40\n'
               ' * SMILES: '
               'C[C@H](CCC(O)=O)[C@H]1CC[C@H]2[C@@H]3CC[C@@H]4C[C@H](O)CC[C@]4(C)[C@H]3C[C@@H](O)[C@]12C '
               'NAME: 12-Epideoxycholic acid REASON: WRONGLY CLASSIFIED '
               'Branching detected at main chain carbon atom index 3\n'
               ' * SMILES: '
               '[O-]C(CC/C=C\\CC/C=C/C=C\\C=C\\[C@H](C/C=C\\C/C=C\\CC)OO)=O '
               'NAME: '
               '(4Z,8E,10Z,12E,14S,16Z,19Z)-14-hydroperoxydocosahexaenoate '
               'REASON: WRONGLY CLASSIFIED Branching detected at main chain '
               'carbon atom index 2\n'
               ' * SMILES: [C@H]1(CCCCCCCC(=O)[O-])[C@@H](CCCCCCCCO)O1 NAME: '
               '(9S,10R)-9,10-epoxy-18-hydroxyoctadecanoate REASON: WRONGLY '
               'CLASSIFIED Branching detected at main chain carbon atom index '
               '7\n'
               ' * SMILES: C[C@@H](O)C([O-])=O NAME: (R)-lactate REASON: '
               'WRONGLY CLASSIFIED Branching detected at main chain carbon '
               'atom index 1\n'
               ' * SMILES: [H]C(CCCCCC)=C([H])CC(O)=O NAME: 3-decenoic acid '
               'REASON: WRONGLY CLASSIFIED Branching detected at main chain '
               'carbon atom index 8\n'
               ' * SMILES: CC(O)CCCCCCCCCCCCCC(O)=O NAME: 15-hydroxypalmitic '
               'acid REASON: WRONGLY CLASSIFIED Branching detected at main '
               'chain carbon atom index 15\n'
               ' * SMILES: '
               'C(CCC([O-])=O)/C=C\\C[C@@H](/C=C/C=C\\C[C@H]1[C@@H](CCCCC)O1)OO '
               'NAME: '
               '(8S)-hydroperoxy-(14S,15R)-epoxy-(5Z,9E,11Z)-icosatrienoate '
               'REASON: WRONGLY CLASSIFIED Branching detected at main chain '
               'carbon atom index 2\n'
               ' * SMILES: O=C1[C@H]([C@H](CC1)CCCCCC(O)=O)CCCCC NAME: '
               '(1S,2S)-3-oxo-2-pentyl-cyclopentanehexanoic acid REASON: '
               'WRONGLY CLASSIFIED Branching detected at main chain carbon '
               'atom index 10\n'
               ' * SMILES: '
               'O[C@@H]1[C@]2([C@]([C@]3([C@](C1)([C@@]4(C(CC3)=CC(=O)C=C4)C)[H])[H])(CC[C@@]2([C@@H](CCC(O)=O)C)[H])[H])C '
               'NAME: 12alpha-Hydroxy-3-oxochola-1,4-dien-24-oic Acid REASON: '
               'WRONGLY CLASSIFIED Branching detected at main chain carbon '
               'atom index 22\n'
               ' * SMILES: CCC1OC1C\\C=C/C\\C=C/C\\C=C/C\\C=C/CCCC(O)=O NAME: '
               '17(18)-EpETE REASON: WRONGLY CLASSIFIED Branching detected at '
               'main chain carbon atom index 19\n'
               ' * SMILES: '
               'O([C@@H]1O[C@@H]([C@@H](O[C@@H]2O[C@@H]([C@@H](O[C@@H]3O[C@@H]([C@@H](O)[C@@H]([C@H]3O)O)CO)[C@@H]([C@H]2O)O)CO)[C@@H]([C@H]1O)O)CO)[C@@H]4[C@H](O[C@@H](O[C@H]([C@@H](CO)O)[C@@H]([C@H](C([O-])=O)O)O)[C@@H]([C@H]4O)O)CO '
               'NAME: D-cellopentaonate REASON: WRONGLY CLASSIFIED Branching '
               'detected at main chain carbon atom index 45\n'
               ' * SMILES: C(=C\\C/C=C\\CCCCC)\\CCCCCC[C@H](C(=O)[O-])OO NAME: '
               '(2R,9Z,12Z)-2-hydroperoxyoctadecadienoate REASON: WRONGLY '
               'CLASSIFIED Branching detected at main chain carbon atom index '
               '16\n'
               ' * SMILES: O[C@@H](CCCCCCCC)CCCCCCC(O)=O NAME: '
               '8S-hydroxy-hexadecanoic acid REASON: WRONGLY CLASSIFIED '
               'Branching detected at main chain carbon atom index 15\n'
               ' * SMILES: OC(=O)CCC#CCCCCC NAME: 4-decynoic acid REASON: '
               'WRONGLY CLASSIFIED Branching detected at main chain carbon '
               'atom index 3\n'
               ' * SMILES: O[C@@H]1C=CC=C(CCC(O)=O)[C@@H]1O NAME: '
               '3-[(5R,6S)-5,6-dihydroxycyclohexa-1,3-dienyl]propanoic acid '
               'REASON: WRONGLY CLASSIFIED Branching detected at main chain '
               'carbon atom index 7\n'
               ' * SMILES: CCCCCCCCCCCCCC[C@@H](O)C(O)=O NAME: '
               '(R)-2-hydroxyhexadecanoic acid REASON: WRONGLY CLASSIFIED '
               'Branching detected at main chain carbon atom index 14\n'
               ' * SMILES: '
               'CC(\\C=C\\[C@@]1(O)C(C)=CC(=O)C[C@]1(C)CO)=C\\C([O-])=O NAME: '
               "(+)-8'-hydroxyabscisate REASON: WRONGLY CLASSIFIED Branching "
               'detected at main chain carbon atom index 16\n'
               'False negatives: SMILES: [O-]C(=O)CCC([N+](C)(C)C)C NAME: '
               '4-aminovaleric acid betaine REASON: MISSED Contains atom N '
               '(atomic number 7), not typical for a fatty acid\n'
               ' * SMILES: OC(=O)C(C(NC(OC)=O)(C)C)(C)C NAME: '
               '3-[(methoxycarbonyl)amino]-2,2,3-trimethylbutanoic acid '
               'REASON: MISSED Contains atom N (atomic number 7), not typical '
               'for a fatty acid\n'
               ' * SMILES: S(CC(CS)C(O)=O)C(=O)C NAME: S-Acetyl '
               'dihydroasparagusic acid REASON: MISSED Contains atom S (atomic '
               'number 16), not typical for a fatty acid\n'
               ' * SMILES: '
               'O=C(NCCCCCN(O)C(=O)CCC(=O)NCCCCCN(O)C(=O)CCC(=O)NCCCCCN(O)C(=O)CCC(=O)O)C(C)C '
               'NAME: Fulvivirgamide B4 REASON: MISSED Contains atom N (atomic '
               'number 7), not typical for a fatty acid\n'
               ' * SMILES: O=C(NC(C(CC)C)COC(=O)C)C(CC(=O)O)C NAME: '
               '4-((1-acetoxy-3-methylpentan-2-yl)amino)-3-methyl-4-oxobutanoic '
               'acid REASON: MISSED Contains atom N (atomic number 7), not '
               'typical for a fatty acid\n'
               ' * SMILES: '
               'O=C1NC(=O)CC(CCCC(=O)/C(=C/C(=C/C(C(O)C(OC)/C=C/CC/C=C/C(O)=O)C)/C)/C)C1 '
               'NAME: '
               '(2E,6E,11E,13E)-18-(2,6-dioxopiperidin-4-yl)-9-hydroxy-8-methoxy-10,12,14-trimethyl-15-oxooctadeca-2,6,11,13-tetraenoic '
               'acid REASON: MISSED Contains atom N (atomic number 7), not '
               'typical for a fatty acid\n'
               ' * SMILES: '
               'O=C(O)CCC(=O)NCCCCCN(O)C(=O)CCC(=O)NCCCCCN(O)C(=O)CC(C)C NAME: '
               'Tenacibactin C REASON: MISSED Contains atom N (atomic number '
               '7), not typical for a fatty acid\n'
               ' * SMILES: '
               '[H][C@@]12[C@H](CCN1CC=C2COC(=O)[C@](O)([C@H](C)O)C(C)(C)O)OC(=O)C(\\C)=C/C '
               'NAME: heliosupine REASON: MISSED Contains atom N (atomic '
               'number 7), not typical for a fatty acid\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'O=C(N1[C@H](CCC1)C(O)=O)[C@@H](NC(=O)[C@@H](N)CC(O)=O)CCC(=O)N',
                                     'name': 'Asp-Gln-Pro',
                                     'reason': 'Contains atom N (atomic number '
                                               '7), not typical for a fatty '
                                               'acid'},
                                 {   'smiles': 'O1C=2C(C(O)=C(CC3=C(O)C=4C(OC3=O)=CC=CC4C)C1=O)=C(C=CC2)C',
                                     'name': 'Gerberinol',
                                     'reason': 'Oxygen count of 6 not typical '
                                               'for a fatty acid (expected 2 '
                                               'or 3)'},
                                 {   'smiles': 'O=C(O)/C(=C/[C@H]1C=C(CC[C@@H]1C(C)C)CO)/COC(=O)C',
                                     'name': '3-acetylgliocladic acid',
                                     'reason': 'Oxygen count of 5 not typical '
                                               'for a fatty acid (expected 2 '
                                               'or 3)'},
                                 {   'smiles': 'O=C(CCCCCCCCC)C=1C=CC(=NC1)CCCCCCCCC',
                                     'name': '1-(6-Nonylpyridin-3-yl)decan-1-one',
                                     'reason': 'Contains atom N (atomic number '
                                               '7), not typical for a fatty '
                                               'acid'},
                                 {   'smiles': 'CCC(=O)O[C@H]1[C@H](C)O[C@H](C[C@@]1(C)O)O[C@@H]1[C@@H](C)O[C@@H](O[C@H]2[C@@H](CC=O)C[C@@H](C)[C@@H](O)\\C=C\\C=C\\C[C@@H](C)OC(=O)C[C@@H](O)[C@@H]2OC)[C@H](O)[C@H]1N(C)C',
                                     'name': 'Leucomycin A7',
                                     'reason': 'Contains atom N (atomic number '
                                               '7), not typical for a fatty '
                                               'acid'},
                                 {   'smiles': 'C[C@H]1O[C@H](C[C@@H](O)[C@@H]1O)c1ccc2C(=O)C3=C([C@H](O)C[C@]4(O)C[C@@](C)(O)CC(=O)[C@]34O)C(=O)c2c1O',
                                     'name': 'Urdamycinone F',
                                     'reason': 'Oxygen count of 11 not typical '
                                               'for a fatty acid (expected 2 '
                                               'or 3)'},
                                 {   'smiles': 'CC(C)=CCC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\COP([O-])(=O)OP([O-])([O-])=O',
                                     'name': 'all-trans-dodecaprenyl '
                                             'diphosphate(3-)',
                                     'reason': 'Contains atom P (atomic number '
                                               '15), not typical for a fatty '
                                               'acid'},
                                 {   'smiles': '[O-][N+](=O)N1CN(CN(CN(C1)[N+]([O-])=O)[N+]([O-])=O)[N+]([O-])=O',
                                     'name': 'octogen',
                                     'reason': 'Contains atom N (atomic number '
                                               '7), not typical for a fatty '
                                               'acid'},
                                 {   'smiles': 'CC(=O)NCCC[NH2+]CCCC[NH2+]CCCNC(C)=O',
                                     'name': 'N(1),N(12)-diacetylsperminium(2+)',
                                     'reason': 'Contains atom N (atomic number '
                                               '7), not typical for a fatty '
                                               'acid'},
                                 {   'smiles': 'C[C@@H]([C@H]1CC[C@H]2[C@H](CCc3cc(O)ccc3C)C(=O)CC[C@]12C)C(O)=O',
                                     'name': '3-hydroxy-9-oxo-9,10-seco-23,24-bisnorchola-1,3,5(10)-trien-22-oic '
                                             'acid',
                                     'reason': 'Oxygen count of 4 not typical '
                                               'for a fatty acid (expected 2 '
                                               'or 3)'}],
    'sample_false_negatives': [   {   'smiles': '[O-]C(=O)CCC([N+](C)(C)C)C',
                                      'name': '4-aminovaleric acid betaine',
                                      'reason': 'Contains atom N (atomic '
                                                'number 7), not typical for a '
                                                'fatty acid'},
                                  {   'smiles': 'CCCCCCCCCCCCCCCCCCCCCCC(C(O)CCCCCCCCCCCCCCCCCC1CC1CCCCCCCCCCCCCCCCC(=O)C(C)CCCCCCCCCCCCCCCCCC)C(O)=O',
                                      'name': 'keto mycolic acid',
                                      'reason': 'Oxygen count of 4 not typical '
                                                'for a fatty acid (expected 2 '
                                                'or 3)'},
                                  {   'smiles': 'CCCCCCCCCCCCCCCCCCCCCCC(C(O)CCCCCCCCCCCCCCCC\\C=C\\CCCCCCCCCCCCCCCCCC(=O)OC(C)CCCCCCCCCCCCCCCCC)C(O)=O',
                                      'name': '(20E)-2-docosyl-3-hydroxy-39-(nonadecan-2-yloxy)-39-oxononatriacont-20-enoic '
                                              'acid',
                                      'reason': 'Oxygen count of 5 not typical '
                                                'for a fatty acid (expected 2 '
                                                'or 3)'},
                                  {   'smiles': 'CCCCCCCCCCCCCCCCCCCCCCCC[C@H]([C@H](O)CCCCCCCCCCCCCCCC[C@@H]1C[C@@H]1[C@H](C)CCCCCCCCCCCCCCCCCCC(=O)C(C)CCCCCCCCCCCCCCCCCC)C(O)=O',
                                      'name': '(2R)-2-[(1R)-1-hydroxy-17-{(1R,2R)-2-[(2R)-22-methyl-21-oxotetracontan-2-yl]cyclopropyl}heptadecyl]hexacosanoic '
                                              'acid',
                                      'reason': 'Oxygen count of 4 not typical '
                                                'for a fatty acid (expected 2 '
                                                'or 3)'},
                                  {   'smiles': 'OC(=O)C(C(NC(OC)=O)(C)C)(C)C',
                                      'name': '3-[(methoxycarbonyl)amino]-2,2,3-trimethylbutanoic '
                                              'acid',
                                      'reason': 'Contains atom N (atomic '
                                                'number 7), not typical for a '
                                                'fatty acid'},
                                  {   'smiles': 'OC(=O)C(CC=C)C(O)=O',
                                      'name': 'Allylmalonic acid',
                                      'reason': 'Oxygen count of 4 not typical '
                                                'for a fatty acid (expected 2 '
                                                'or 3)'},
                                  {   'smiles': 'S(CC(CS)C(O)=O)C(=O)C',
                                      'name': 'S-Acetyl dihydroasparagusic '
                                              'acid',
                                      'reason': 'Contains atom S (atomic '
                                                'number 16), not typical for a '
                                                'fatty acid'},
                                  {   'smiles': 'C(CCCCCCCCC(C)C(O)CCCCCCCCCCCCCCCCC1C(CCCCCCCCCCCCCCCCCC(O)C(C(O)=O)CCCCCCCCCCCCCCCCCCCCCC)C1)CCCCCCCCC',
                                      'name': 'dihydroxy mycolic acid',
                                      'reason': 'Oxygen count of 4 not typical '
                                                'for a fatty acid (expected 2 '
                                                'or 3)'},
                                  {   'smiles': 'O=C(NCCCCCN(O)C(=O)CCC(=O)NCCCCCN(O)C(=O)CCC(=O)NCCCCCN(O)C(=O)CCC(=O)O)C(C)C',
                                      'name': 'Fulvivirgamide B4',
                                      'reason': 'Contains atom N (atomic '
                                                'number 7), not typical for a '
                                                'fatty acid'},
                                  {   'smiles': 'CCCCCCCCCCCCCCCCCCCCCCCC[C@H]([C@H](O)CCCCCCCCCCCCCCC[C@H]1C[C@H]1CCCCCCCCCCCCCCCCCCC(=O)[C@@H](C)CCCCCCCCCCCCCCCCCC)C(O)=O',
                                      'name': '(2R)-2-[(1R)-1-hydroxy-16-{(1S,2R)-2-[(20S)-20-methyl-19-oxooctatriacontyl]cyclopropyl}hexadecyl]hexacosanoic '
                                              'acid',
                                      'reason': 'Oxygen count of 4 not typical '
                                                'for a fatty acid (expected 2 '
                                                'or 3)'}],
    'attempt': 3,
    'reasoning': 'Below is one possible solution. In this version I tried to '
                 '“tighten up” the original algorithm by (1) checking that '
                 'only C and O are present and that the overall oxygen count '
                 'is what one expects for a fatty acid (2) requiring exactly '
                 'one carboxyl group (so that the molecule really is a fatty '
                 'acid) and (3) using the acyclic‐carbon graph to extract a '
                 '“main chain” (the fatty acyl chain, starting at the carbon '
                 'next to the carboxyl group) and then not only “flagging” any '
                 'extra branch but also checking that the branch is relatively '
                 'short (for example, a methyl/ethyl branch). One can then '
                 'more reliably classify molecules as branched‐chain fatty '
                 'acids. (Of course, this is only one heuristic approach among '
                 'many.) \n'
                 '\n'
                 'Below is the complete Python code in one code block:\n'
                 '\n'
                 '------------------------------------------------',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 129,
    'num_false_positives': 2693,
    'num_true_negatives': 139438,
    'num_false_negatives': 40,
    'num_negatives': None,
    'precision': 0.04571226080793763,
    'recall': 0.7633136094674556,
    'f1': 0.08625877632898696,
    'accuracy': 0.9807940969782151,
    'negative_predictive_value': 0.9997132164212277}