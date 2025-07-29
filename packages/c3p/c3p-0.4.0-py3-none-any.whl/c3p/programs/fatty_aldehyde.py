"""
Classifies: CHEBI:35746 fatty aldehyde
"""
"""
Classifies: Fatty Aldehyde
Definition: An aldehyde formally arising from reduction of the carboxylic acid of its corresponding fatty acid,
with a long acyclic chain that is mainly carbon/hydrogen and a terminal aldehyde group.
Improvements:
  • Only allows elements C, H, and O.
  • Requires an acyclic molecular structure.
  • Demands at least 6 carbon atoms.
  • Requires that the non‐H (heavy) atoms are predominantly carbon (fraction ≥ 0.75).
  • Requires exactly one overall carbonyl group ([CX3]=[OX1]) in the molecule.
  • The aldehyde carbon in that carbonyl must be terminal (attached to exactly one carbon).
  • The molecule’s carbon connectivity should be “chain‐like” – the longest chain of connected carbons must account for at least 75% of the total carbons.
"""

from rdkit import Chem
from collections import deque

def is_fatty_aldehyde(smiles: str):
    """
    Determines if a molecule qualifies as a fatty aldehyde.

    Steps:
      1. Parse the SMILES string.
      2. Confirm that only allowed elements (C, H, O) are present.
      3. Check that the molecule is acyclic.
      4. Verify that there are at least 6 carbon atoms.
      5. Confirm that heavy atoms (non-H) are predominantly carbons (fraction ≥ 0.75).
      6. Ensure that the molecule contains exactly one carbonyl group ([CX3]=[OX1]).
      7. Confirm that the carbonyl appears as a terminal aldehyde (the aldehyde carbon is attached to exactly one carbon and is not in a ring).
      8. Compute the longest carbon–chain (using the carbon–atom connectivity) and require that it constitutes at least 75% of all carbon atoms.
    Args:
      smiles (str): SMILES string of the molecule.
    Returns:
      (bool, str): A tuple where the boolean indicates acceptance and the string explains the decision.
    """

    # 1. Parse the SMILES string.
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
    
    # 2. Check allowed elements: only C (6), H (1), and O (8)
    allowed_atomic_nums = {1, 6, 8}  # H, C, O
    for atom in mol.GetAtoms():
        if atom.GetAtomicNum() not in allowed_atomic_nums:
            return False, f"Contains disallowed element: {atom.GetSymbol()}"

    # 3. Ensure the molecule is acyclic.
    if mol.GetRingInfo().NumRings() > 0:
        return False, "Molecule contains ring(s) which is not typical for a fatty aldehyde"
    
    # 4. Count the number of carbon atoms.
    carbon_atoms = [atom for atom in mol.GetAtoms() if atom.GetAtomicNum() == 6]
    n_carbons = len(carbon_atoms)
    if n_carbons < 6:
        return False, f"Not enough carbon atoms ({n_carbons} found; need at least 6) for a fatty chain"

    # 5. Check heavy atom composition (non-H atoms).
    heavy_atoms = [atom for atom in mol.GetAtoms() if atom.GetAtomicNum() > 1]
    if not heavy_atoms:
        return False, "No heavy atoms found"
    carbon_fraction = n_carbons / len(heavy_atoms)
    if carbon_fraction < 0.75:
        return False, f"Molecule has a low carbon fraction ({carbon_fraction:.2f}); it likely contains additional functionalities"

    # 6. Check that there is exactly one carbonyl group overall.
    # Carbonyl SMARTS: any C (sp3 or sp2) double-bonded to oxygen.
    carbonyl_smarts = "[CX3]=[OX1]"
    carbonyl_pattern = Chem.MolFromSmarts(carbonyl_smarts)
    carbonyl_matches = mol.GetSubstructMatches(carbonyl_pattern)
    if len(carbonyl_matches) != 1:
        return False, f"Expected exactly one carbonyl group; found {len(carbonyl_matches)}"
    
    # 7. Check for a terminal aldehyde group.
    # We use a SMARTS that requires one hydrogen on the carbonyl carbon: [CX3H1](=O)
    aldehyde_smarts = "[CX3H1](=O)"
    aldehyde_pattern = Chem.MolFromSmarts(aldehyde_smarts)
    aldehyde_matches = mol.GetSubstructMatches(aldehyde_pattern)
    terminal_aldehyde_count = 0
    for match in aldehyde_matches:
        aldehyde_c = mol.GetAtomWithIdx(match[0])
        # Exclude if the carbonyl carbon is in a ring (it should be terminal and open)
        if aldehyde_c.IsInRing():
            continue
        # Count carbon neighbors (ignoring the oxygen in the C=O).
        carbon_neighbors = [nbr for nbr in aldehyde_c.GetNeighbors() if nbr.GetAtomicNum() == 6]
        if len(carbon_neighbors) == 1:
            terminal_aldehyde_count += 1
    
    if terminal_aldehyde_count != 1:
        return False, f"Expected exactly one terminal aldehyde group; found {terminal_aldehyde_count}"
    
    # 8. Assess the carbon-chain linearity.
    # Build a graph (adjacency list) of the indices of carbon atoms.
    carbon_indices = {atom.GetIdx() for atom in mol.GetAtoms() if atom.GetAtomicNum() == 6}
    carbon_graph = {idx: [] for idx in carbon_indices}
    for bond in mol.GetBonds():
        begin = bond.GetBeginAtomIdx()
        end = bond.GetEndAtomIdx()
        if begin in carbon_indices and end in carbon_indices:
            carbon_graph[begin].append(end)
            carbon_graph[end].append(begin)
    
    # Check that the carbon subgraph is connected.
    visited = set()
    def bfs(start):
        q = deque([start])
        comp = set()
        while q:
            cur = q.popleft()
            if cur in comp:
                continue
            comp.add(cur)
            for nei in carbon_graph[cur]:
                if nei not in comp:
                    q.append(nei)
        return comp

    # Get connected component from an arbitrary carbon.
    comp = bfs(next(iter(carbon_indices)))
    if len(comp) != len(carbon_indices):
        return False, "Carbon atoms are not in a single connected chain (fatty chain expected to be contiguous)"
    
    # Compute the (tree) diameter of the carbon graph.
    # In an acyclic graph (tree), the diameter can be found by two BFS passes.
    def bfs_farthest(start):
        seen = {start: 0}
        q = deque([start])
        farthest_node = start
        max_dist = 0
        while q:
            cur = q.popleft()
            for nei in carbon_graph[cur]:
                if nei not in seen:
                    seen[nei] = seen[cur] + 1
                    if seen[nei] > max_dist:
                        max_dist = seen[nei]
                        farthest_node = nei
                    q.append(nei)
        return farthest_node, max_dist

    # First BFS from any node.
    far_node, _ = bfs_farthest(next(iter(carbon_indices)))
    # Second BFS to get the diameter (distance in bonds; add 1 to get number of atoms on the path).
    _, diameter = bfs_farthest(far_node)
    longest_chain_length = diameter + 1

    # Require that the longest chain accounts for at least 75% of all carbons.
    if longest_chain_length < 0.75 * n_carbons:
        return False, (f"Carbon chain is too branched: longest chain has {longest_chain_length} atoms "
                       f"but molecule has {n_carbons} carbons in total")
    
    return True, "Molecule qualifies as a fatty aldehyde: acyclic, mainly C/H, with a long chain and a single terminal aldehyde group"

# Example test cases (uncomment to run):
# test_smiles = [
#     "[H]C(=CC=O)C(O)CCCCC",    # 4-hydroxynon-2-enal (expected True)
#     "O=CCCCCCCCCC/C=C\\CCCCCCCC",  # 11Z-Eicosenal (expected True)
#     "CCCCCCCCCCCC=O",         # dodecanal (expected True)
#     "O=C/C(=C\\CCCCCC/C=C\\C/C=C\\CCCCC)/CCCCCCCCCCCCC",  # (2Z,10Z,13Z)-2-tridecylnonadeca-2,10,13-trienal (expected True)
# ]
# for s in test_smiles:
#     res, reason = is_fatty_aldehyde(s)
#     print(f"SMILES: {s}\nResult: {res}, Reason: {reason}\n")


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:35746',
                          'name': 'fatty aldehyde',
                          'definition': 'An aldehyde formally arising from '
                                        'reduction of the carboxylic acid '
                                        'group of its corresponding fatty '
                                        'acid, having a carbonyl group at one '
                                        'end of the carbon chain.',
                          'parents': ['CHEBI:59768'],
                          'xrefs': [   'PMID:15210368',
                                       'PMID:21341652',
                                       'PMID:21347727'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 119,
                           'log_lines_of_code': 4.77912349311153,
                           'indent_by_line': [   1,
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
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 0,
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
                                                 0,
                                                 1,
                                                 1,
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
                                                 2,
                                                 2,
                                                 2,
                                                 3,
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
                                                 2,
                                                 2,
                                                 3,
                                                 3,
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
                                                 2,
                                                 0,
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
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 3,
                                                 4,
                                                 5,
                                                 5,
                                                 6,
                                                 6,
                                                 5,
                                                 2,
                                                 0,
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
                                                 0],
                           'max_indent': 6,
                           'imports': [   'from rdkit import Chem',
                                          'from collections import deque'],
                           'imports_count': 2,
                           'methods_called': [   'GetEndAtomIdx',
                                                 'GetSymbol',
                                                 'GetIdx',
                                                 'NumRings',
                                                 'GetAtomicNum',
                                                 'GetBeginAtomIdx',
                                                 'MolFromSmiles',
                                                 'GetAtomWithIdx',
                                                 'GetBonds',
                                                 'GetAtoms',
                                                 'popleft',
                                                 'MolFromSmarts',
                                                 'GetNeighbors',
                                                 'append',
                                                 'GetRingInfo',
                                                 'IsInRing',
                                                 'GetSubstructMatches',
                                                 'add'],
                           'methods_called_count': 18,
                           'smarts_strings': [   'carbonyl_smarts',
                                                 'aldehyde_smarts'],
                           'smarts_strings_count': 2,
                           'defs': [   'is_fatty_aldehyde(smiles: str):',
                                       'bfs(start):',
                                       'bfs_farthest(start):'],
                           'defs_count': 3,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, f"Contains disallowed '
                                          'element: {atom.GetSymbol()}"',
                                          'False, "Molecule contains ring(s) '
                                          'which is not typical for a fatty '
                                          'aldehyde"',
                                          'False, f"Not enough carbon atoms '
                                          '({n_carbons} found; need at least '
                                          '6) for a fatty chain"',
                                          'False, "No heavy atoms found"',
                                          'False, f"Molecule has a low carbon '
                                          'fraction ({carbon_fraction:.2f}); '
                                          'it likely contains additional '
                                          'functionalities"',
                                          'False, f"Expected exactly one '
                                          'carbonyl group; found '
                                          '{len(carbonyl_matches)}"',
                                          'False, f"Expected exactly one '
                                          'terminal aldehyde group; found '
                                          '{terminal_aldehyde_count}"',
                                          'comp',
                                          'False, "Carbon atoms are not in a '
                                          'single connected chain (fatty chain '
                                          'expected to be contiguous)"',
                                          'farthest_node, max_dist',
                                          'False, (f"Carbon chain is too '
                                          'branched: longest chain has '
                                          '{longest_chain_length} atoms "',
                                          'True, "Molecule qualifies as a '
                                          'fatty aldehyde: acyclic, mainly '
                                          'C/H, with a long chain and a single '
                                          'terminal aldehyde group"'],
                           'returns_count': 13,
                           'complexity': 8.955824698622305},
    'message': '\n'
               'Attempt failed: F1 score of 0.8337028824833703 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: [H]C(=CC=O)C(O)CCCCC NAME: '
               '4-hydroxynon-2-enal REASON: CORRECT Molecule qualifies as a '
               'fatty aldehyde: acyclic, mainly C/H, with a long chain and a '
               'single terminal aldehyde group\n'
               ' * SMILES: O=CCCCCCCCCC/C=C\\CCCCCCCC NAME: 11Z-Eicosenal '
               'REASON: CORRECT Molecule qualifies as a fatty aldehyde: '
               'acyclic, mainly C/H, with a long chain and a single terminal '
               'aldehyde group\n'
               ' * SMILES: CCCCCCCCCCCC=O NAME: dodecanal REASON: CORRECT '
               'Molecule qualifies as a fatty aldehyde: acyclic, mainly C/H, '
               'with a long chain and a single terminal aldehyde group\n'
               ' * SMILES: O=C/C(=C\\CCCCCC/C=C\\C/C=C\\CCCCC)/CCCCCCCCCCCCC '
               'NAME: (2Z,10Z,13Z)-2-tridecylnonadeca-2,10,13-trienal REASON: '
               'CORRECT Molecule qualifies as a fatty aldehyde: acyclic, '
               'mainly C/H, with a long chain and a single terminal aldehyde '
               'group\n'
               ' * SMILES: [H]C(=O)C(\\CC)=C\\CCC NAME: (E)-2-ethyl-2-hexenal '
               'REASON: CORRECT Molecule qualifies as a fatty aldehyde: '
               'acyclic, mainly C/H, with a long chain and a single terminal '
               'aldehyde group\n'
               ' * SMILES: O=C/C(=C/CCCCCCCCCCCCCC)/CCCCC/C=C\\C/C=C\\CCCCC '
               'NAME: (2E,8Z,11Z)-2-pentadecylideneheptadeca-8,11-dienal '
               'REASON: CORRECT Molecule qualifies as a fatty aldehyde: '
               'acyclic, mainly C/H, with a long chain and a single terminal '
               'aldehyde group\n'
               ' * SMILES: C(=C\\C/C=C\\CCCCC)\\CCCCCCC=O NAME: '
               '(8Z,11Z)-heptadecadienal REASON: CORRECT Molecule qualifies as '
               'a fatty aldehyde: acyclic, mainly C/H, with a long chain and a '
               'single terminal aldehyde group\n'
               ' * SMILES: O=CCC\\C=C\\CCC/C=C\\CCCC NAME: '
               '4E,9Z-Tetradecadienal REASON: CORRECT Molecule qualifies as a '
               'fatty aldehyde: acyclic, mainly C/H, with a long chain and a '
               'single terminal aldehyde group\n'
               ' * SMILES: OC(CCCC)/C=C/C=O NAME: 4-hydroxy-2-octenal REASON: '
               'CORRECT Molecule qualifies as a fatty aldehyde: acyclic, '
               'mainly C/H, with a long chain and a single terminal aldehyde '
               'group\n'
               ' * SMILES: C(CCCC(=C(CC)[H])[H])=O NAME: oct-5-enal REASON: '
               'CORRECT Molecule qualifies as a fatty aldehyde: acyclic, '
               'mainly C/H, with a long chain and a single terminal aldehyde '
               'group\n'
               ' * SMILES: O=CC=CCCC=CCC NAME: 2,6-nonadienal REASON: CORRECT '
               'Molecule qualifies as a fatty aldehyde: acyclic, mainly C/H, '
               'with a long chain and a single terminal aldehyde group\n'
               ' * SMILES: C(CCCCCCCCCC(C(=O)[H])O)CCCC NAME: '
               '2-hydroxyhexadecanal REASON: CORRECT Molecule qualifies as a '
               'fatty aldehyde: acyclic, mainly C/H, with a long chain and a '
               'single terminal aldehyde group\n'
               ' * SMILES: O=CCCCCC\\C=C\\CCCCCCCC NAME: 7-hexadecenal REASON: '
               'CORRECT Molecule qualifies as a fatty aldehyde: acyclic, '
               'mainly C/H, with a long chain and a single terminal aldehyde '
               'group\n'
               ' * SMILES: O=CCCCCCCC/C=C/CCCCCC NAME: 9-hexadecenal REASON: '
               'CORRECT Molecule qualifies as a fatty aldehyde: acyclic, '
               'mainly C/H, with a long chain and a single terminal aldehyde '
               'group\n'
               ' * SMILES: O=CCC\\C=C\\CCCC NAME: Trans-4-Nonenal REASON: '
               'CORRECT Molecule qualifies as a fatty aldehyde: acyclic, '
               'mainly C/H, with a long chain and a single terminal aldehyde '
               'group\n'
               ' * SMILES: [H]C(=O)C([H])=C([H])CCCC NAME: hept-2-enal REASON: '
               'CORRECT Molecule qualifies as a fatty aldehyde: acyclic, '
               'mainly C/H, with a long chain and a single terminal aldehyde '
               'group\n'
               ' * SMILES: O=C\\C(\\CCCC)=C\\C NAME: 2-Ethylidenehexanal '
               'REASON: CORRECT Molecule qualifies as a fatty aldehyde: '
               'acyclic, mainly C/H, with a long chain and a single terminal '
               'aldehyde group\n'
               ' * SMILES: O=CCC(CC(C)C)C NAME: 3,5-Dimethylhexanal REASON: '
               'CORRECT Molecule qualifies as a fatty aldehyde: acyclic, '
               'mainly C/H, with a long chain and a single terminal aldehyde '
               'group\n'
               ' * SMILES: O=C\\C=C\\C=C\\CCCCCC NAME: 2,4-Undecadienal '
               'REASON: CORRECT Molecule qualifies as a fatty aldehyde: '
               'acyclic, mainly C/H, with a long chain and a single terminal '
               'aldehyde group\n'
               ' * SMILES: O=CCC\\C=C\\C=C\\CCC\\C=C\\CCCC NAME: '
               '4,6,11-hexadecatrienal REASON: CORRECT Molecule qualifies as a '
               'fatty aldehyde: acyclic, mainly C/H, with a long chain and a '
               'single terminal aldehyde group\n'
               ' * SMILES: O=CC/C=C\\CCCCC NAME: (3Z)-nonenal REASON: CORRECT '
               'Molecule qualifies as a fatty aldehyde: acyclic, mainly C/H, '
               'with a long chain and a single terminal aldehyde group\n'
               ' * SMILES: O=C\\C(=C\\C(\\C)=C\\C)\\C NAME: '
               '2,4-Dimethyl-2E,4E-hexadienal REASON: CORRECT Molecule '
               'qualifies as a fatty aldehyde: acyclic, mainly C/H, with a '
               'long chain and a single terminal aldehyde group\n'
               ' * SMILES: O=CCCCCCCC/C=C/C=C\\CCCC NAME: '
               '9E,11Z-Hexadecadienal REASON: CORRECT Molecule qualifies as a '
               'fatty aldehyde: acyclic, mainly C/H, with a long chain and a '
               'single terminal aldehyde group\n'
               ' * SMILES: O=CCCCCCCCC/C=C\\CCCCC NAME: 10Z-Hexadecenal '
               'REASON: CORRECT Molecule qualifies as a fatty aldehyde: '
               'acyclic, mainly C/H, with a long chain and a single terminal '
               'aldehyde group\n'
               ' * SMILES: O=CCCCC=C NAME: 5-Hexenal REASON: CORRECT Molecule '
               'qualifies as a fatty aldehyde: acyclic, mainly C/H, with a '
               'long chain and a single terminal aldehyde group\n'
               'False positives: SMILES: '
               'C(\\C=C\\C=C(C)C)(=C/C=C/C(=C/C=C/C=C(/C=C/C=C(/C=C/C=C(/C=O)\\C)\\C)\\C)/C)/C '
               "NAME: 4,4'-diapolycopen-4-al REASON: WRONGLY CLASSIFIED "
               'Molecule qualifies as a fatty aldehyde: acyclic, mainly C/H, '
               'with a long chain and a single terminal aldehyde group\n'
               ' * SMILES: '
               '[H]C(/C=C/C(=C/C=C/C=C(\\C=C\\C=C(\\C=C\\C=C(\\CCC=C(C)C)/C)/C)/C)/C)=O '
               "NAME: 13-cis-10'-apo-lycopenal REASON: WRONGLY CLASSIFIED "
               'Molecule qualifies as a fatty aldehyde: acyclic, mainly C/H, '
               'with a long chain and a single terminal aldehyde group\n'
               ' * SMILES: [H]C(=O)\\C=C\\C#CC NAME: (E)-hex-2-en-4-ynal '
               'REASON: WRONGLY CLASSIFIED Molecule qualifies as a fatty '
               'aldehyde: acyclic, mainly C/H, with a long chain and a single '
               'terminal aldehyde group\n'
               ' * SMILES: C\\C=C/OCC(C)CC=O NAME: '
               '3-methyl-4-{[(1Z)-prop-1-en-1-yl]oxy}butanal REASON: WRONGLY '
               'CLASSIFIED Molecule qualifies as a fatty aldehyde: acyclic, '
               'mainly C/H, with a long chain and a single terminal aldehyde '
               'group\n'
               ' * SMILES: O=CC(CCCC(CCCC(CCCC(C)C)C)C)=C NAME: '
               '6,10,14-Trimethyl-2-methylenepentadecanal REASON: WRONGLY '
               'CLASSIFIED Molecule qualifies as a fatty aldehyde: acyclic, '
               'mainly C/H, with a long chain and a single terminal aldehyde '
               'group\n'
               ' * SMILES: C\\C(CC\\C=C(/C)C=O)=C/C\\C=C(/C)C=C NAME: '
               'alpha-Sinensal REASON: WRONGLY CLASSIFIED Molecule qualifies '
               'as a fatty aldehyde: acyclic, mainly C/H, with a long chain '
               'and a single terminal aldehyde group\n'
               ' * SMILES: OC(CC/C=C(/CCC=O)\\C)(C)C=C NAME: '
               '8E-Hydroxy-4,8-dimethyl-4,9-decadienal REASON: WRONGLY '
               'CLASSIFIED Molecule qualifies as a fatty aldehyde: acyclic, '
               'mainly C/H, with a long chain and a single terminal aldehyde '
               'group\n'
               ' * SMILES: O=C/C(=C/C=C/C)/[C@@H](O)[C@@H](O)/C=C\\C NAME: '
               '(Z,2E,3R,4S)-2-[(E)-but-2-enylidene]-3,4-dihydroxyhept-5-enal '
               'REASON: WRONGLY CLASSIFIED Molecule qualifies as a fatty '
               'aldehyde: acyclic, mainly C/H, with a long chain and a single '
               'terminal aldehyde group\n'
               ' * SMILES: O=CCC(C(C/C=C(/CC/C=C(\\CC)/C)\\C)C)C NAME: '
               '3,4,7,11-Tetramethyl-6E,10Z-tridecadienal REASON: WRONGLY '
               'CLASSIFIED Molecule qualifies as a fatty aldehyde: acyclic, '
               'mainly C/H, with a long chain and a single terminal aldehyde '
               'group\n'
               ' * SMILES: CCCCCCCCCCCCCCCCCC=O NAME: octadecanal REASON: '
               'WRONGLY CLASSIFIED Molecule qualifies as a fatty aldehyde: '
               'acyclic, mainly C/H, with a long chain and a single terminal '
               'aldehyde group\n'
               ' * SMILES: '
               'O=C\\C=C\\C(=C\\C=C\\C(=C\\C=C\\C=C(\\C=C\\C=C(\\C=C\\C=C(\\CCC=C(C)C)/C)/C)/C)\\C)\\C '
               "NAME: (all-E)-6'-Apo-y-caroten-6'-al REASON: WRONGLY "
               'CLASSIFIED Molecule qualifies as a fatty aldehyde: acyclic, '
               'mainly C/H, with a long chain and a single terminal aldehyde '
               'group\n'
               ' * SMILES: [H]C(=O)\\C=C(\\C)CC\\C=C(/C)CCC=C(C)C NAME: '
               '(2-cis,6-trans)-farnesal REASON: WRONGLY CLASSIFIED Molecule '
               'qualifies as a fatty aldehyde: acyclic, mainly C/H, with a '
               'long chain and a single terminal aldehyde group\n'
               ' * SMILES: O=CC/C(=C/CC=C(C)C)/C NAME: Isocitral REASON: '
               'WRONGLY CLASSIFIED Molecule qualifies as a fatty aldehyde: '
               'acyclic, mainly C/H, with a long chain and a single terminal '
               'aldehyde group\n'
               ' * SMILES: CC(\\C=C\\C=O)=C/C=C/O NAME: '
               '(2E,4E,6E)-7-hydroxy-4-methylhepta-2,4,6-trienal REASON: '
               'WRONGLY CLASSIFIED Molecule qualifies as a fatty aldehyde: '
               'acyclic, mainly C/H, with a long chain and a single terminal '
               'aldehyde group\n'
               ' * SMILES: [H]C(=O)C([H])=CC#CC NAME: hex-2-en-4-ynal REASON: '
               'WRONGLY CLASSIFIED Molecule qualifies as a fatty aldehyde: '
               'acyclic, mainly C/H, with a long chain and a single terminal '
               'aldehyde group\n'
               ' * SMILES: C\\C(CO)=C/C=C/CC=O NAME: '
               '(E,E)-7-hydroxy-6-methylhepta-3,5-dienal REASON: WRONGLY '
               'CLASSIFIED Molecule qualifies as a fatty aldehyde: acyclic, '
               'mainly C/H, with a long chain and a single terminal aldehyde '
               'group\n'
               ' * SMILES: OC(CCCC#C)C=CC=O NAME: 4-hydroxy Nonenal Alkyne '
               'REASON: WRONGLY CLASSIFIED Molecule qualifies as a fatty '
               'aldehyde: acyclic, mainly C/H, with a long chain and a single '
               'terminal aldehyde group\n'
               ' * SMILES: O=C\\C=C(\\CCCC(CCCC(CCCC(C)C)C)C)/C NAME: Phytal '
               'REASON: WRONGLY CLASSIFIED Molecule qualifies as a fatty '
               'aldehyde: acyclic, mainly C/H, with a long chain and a single '
               'terminal aldehyde group\n'
               ' * SMILES: [H]C(=O)CC(C)CCCC(C)(C)O NAME: hydroxycitronellal '
               'REASON: WRONGLY CLASSIFIED Molecule qualifies as a fatty '
               'aldehyde: acyclic, mainly C/H, with a long chain and a single '
               'terminal aldehyde group\n'
               ' * SMILES: CCC(C)(CCCC(C)C=O)OC NAME: '
               '6-methoxy-2,6-dimethyloctanal REASON: WRONGLY CLASSIFIED '
               'Molecule qualifies as a fatty aldehyde: acyclic, mainly C/H, '
               'with a long chain and a single terminal aldehyde group\n'
               ' * SMILES: [H]C(=O)CC(C)CCC=C(C)C NAME: citronellal REASON: '
               'WRONGLY CLASSIFIED Molecule qualifies as a fatty aldehyde: '
               'acyclic, mainly C/H, with a long chain and a single terminal '
               'aldehyde group\n'
               ' * SMILES: CC(C)C(=C)C\\C=C(\\C)C=O NAME: '
               '(2Z)-5-isopropyl-2-methylhexa-2,5-dienal REASON: WRONGLY '
               'CLASSIFIED Molecule qualifies as a fatty aldehyde: acyclic, '
               'mainly C/H, with a long chain and a single terminal aldehyde '
               'group\n'
               ' * SMILES: CC(C)=CCC\\C(C)=C\\C=O NAME: geranial REASON: '
               'WRONGLY CLASSIFIED Molecule qualifies as a fatty aldehyde: '
               'acyclic, mainly C/H, with a long chain and a single terminal '
               'aldehyde group\n'
               ' * SMILES: [H]C(=O)C=C(C)CCC=C(C)CCC=C(C)C NAME: farnesal '
               'REASON: WRONGLY CLASSIFIED Molecule qualifies as a fatty '
               'aldehyde: acyclic, mainly C/H, with a long chain and a single '
               'terminal aldehyde group\n'
               ' * SMILES: O=CCC=C(C)C NAME: 4-methyl-3-Pentenal REASON: '
               'WRONGLY CLASSIFIED Molecule qualifies as a fatty aldehyde: '
               'acyclic, mainly C/H, with a long chain and a single terminal '
               'aldehyde group\n'
               'False negatives: SMILES: O=C/C=C/C=C/C=C/C=C/C=C/C=C/C=O NAME: '
               '2,4,6,8,10,12-tetradeca-1,14-hexenedial REASON: MISSED '
               'Expected exactly one carbonyl group; found 2\n'
               ' * SMILES: O=C/C=C\\C=C\\C=O NAME: (E,E)-2,4-Hexadienedial '
               'REASON: MISSED Expected exactly one carbonyl group; found 2\n'
               ' * SMILES: O=C(CCCCC)CCC=O NAME: 4-Oxononanal REASON: MISSED '
               'Expected exactly one carbonyl group; found 2\n'
               ' * SMILES: O=C(CCCCCCCCCC=C)CC=O NAME: 3-oxo-13-Tetradecenal '
               'REASON: MISSED Expected exactly one carbonyl group; found 2\n'
               ' * SMILES: O=CCCCC/C=C/C=O NAME: 2-octenedial REASON: MISSED '
               'Expected exactly one carbonyl group; found 2\n'
               ' * SMILES: O=CCCCCC=O NAME: Adipaldehyde REASON: MISSED '
               'Expected exactly one carbonyl group; found 2\n'
               ' * SMILES: [H]C(C(C)(C)C)=O NAME: 2,2-dimethylpropanal REASON: '
               'MISSED Not enough carbon atoms (5 found; need at least 6) for '
               'a fatty chain\n'
               ' * SMILES: O=C(CCCCC/C=C\\CCCCCC)CC=O NAME: '
               '3-oxo-9Z-Hexadecenal REASON: MISSED Expected exactly one '
               'carbonyl group; found 2\n'
               ' * SMILES: O=C(CCCCCCCCCCC)CC=O NAME: 3-oxo-Tetradecanal '
               'REASON: MISSED Expected exactly one carbonyl group; found 2\n'
               ' * SMILES: CCCCCCCCCC(=O)CC=O NAME: Decanoyl acetaldehyde '
               'REASON: MISSED Expected exactly one carbonyl group; found 2\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'O=C(N[C@@H](C(O)(C)C)C)[C@H]([C@@]1([C@@]2([C@@](CC1)(/C(/CCC2)=C/C=C\\3/C[C@@H](O)C[C@H](O)C3=C)[H])C)[H])C',
                                     'name': '1alpha,25-dihydroxy-24-oxo-23-azavitamin '
                                             'D2 / '
                                             '1alpha,25-dihydroxy-24-oxo-23-azaergocalciferol',
                                     'reason': 'Contains disallowed element: '
                                               'N'},
                                 {   'smiles': 'CCCCCCCCCCCCCCCCCCC(O)C([O-])=O',
                                     'name': '2-hydroxyarachidate',
                                     'reason': 'Expected exactly one terminal '
                                               'aldehyde group; found 0'},
                                 {   'smiles': 'C[C@@H](CN([C@@H](C)CO)C(=O)NC1=CC=C(C=C1)C(F)(F)F)[C@@H](CN(C)C(=O)C2CCOCC2)OC',
                                     'name': 'N-[(2S,3S)-4-[[(2S)-1-hydroxypropan-2-yl]-[[4-(trifluoromethyl)phenyl]carbamoyl]amino]-2-methoxy-3-methylbutyl]-N-methyloxane-4-carboxamide',
                                     'reason': 'Contains disallowed element: '
                                               'N'},
                                 {   'smiles': 'CC(=O)CC\\C=C(/C)CCC=C(C)C',
                                     'name': 'geranyl acetone',
                                     'reason': 'Expected exactly one terminal '
                                               'aldehyde group; found 0'},
                                 {   'smiles': 'O([C@H]1[C@H](O)[C@H](O[C@H](O)[C@H]1O)CO[C@H]2O[C@@H]([C@@H](O)[C@H](O)[C@@H]2O)CO)[C@H]3O[C@@H]([C@@H](O)[C@H](O)[C@@H]3O[C@H]4O[C@@H]([C@@H](O)[C@H](O)[C@@H]4O)CO)CO',
                                     'name': '(2S,3S,4S,5S,6R)-2-[[(2R,3R,4S,5S,6S)-4-[(2R,3S,4S,5S,6R)-4,5-Dihydroxy-6-(hydroxymethyl)-3-[(2R,3S,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-3,5,6-trihydroxyoxan-2-yl]methoxy]-6-(hydroxymethyl)oxane-3,4,5-triol',
                                     'reason': 'Molecule contains ring(s) '
                                               'which is not typical for a '
                                               'fatty aldehyde'},
                                 {   'smiles': 'O=C(OC1=C(C(O)=C(C(=O)O)C(=C1C)C)C)C2=C(OC)C(=C(OC(=O)C3=C(O)C=C(O)C=C3C)C=C2C)C',
                                     'name': 'Thielavin Z5',
                                     'reason': 'Molecule contains ring(s) '
                                               'which is not typical for a '
                                               'fatty aldehyde'},
                                 {   'smiles': '[C@@H]1([C@@H]([C@H]([C@@H]([C@H](O1)CO)O)O)NC(C)=O)O[C@@H]2[C@@H]([C@H](C(O[C@@H]2CO)O)O)O',
                                     'name': 'beta-D-GlcpNAc-(1->4)-D-Galp',
                                     'reason': 'Contains disallowed element: '
                                               'N'},
                                 {   'smiles': 'CN(C)C(=O)C1=CC=C(C=C1)C2=CC=C(C=C2)[C@@H]3[C@H]4CN(CC(=O)N4[C@H]3CO)C(=O)CC5CC5',
                                     'name': '4-[4-[(6S,7R,8R)-4-(2-cyclopropyl-1-oxoethyl)-8-(hydroxymethyl)-2-oxo-1,4-diazabicyclo[4.2.0]octan-7-yl]phenyl]-N,N-dimethylbenzamide',
                                     'reason': 'Contains disallowed element: '
                                               'N'},
                                 {   'smiles': 'CCCCCCCCCCCCCCCCCCCCC=C',
                                     'name': '1-docosene',
                                     'reason': 'Expected exactly one carbonyl '
                                               'group; found 0'},
                                 {   'smiles': 'C([C@@](OC(=O)CCC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)([H])COC(=O)CC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)OC(=O)CCCCC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC',
                                     'name': 'TG(22:5(7Z,10Z,13Z,16Z,19Z)/20:5(5Z,8Z,11Z,14Z,17Z)/22:6(4Z,7Z,10Z,13Z,16Z,19Z))[iso6]',
                                     'reason': 'Expected exactly one carbonyl '
                                               'group; found 3'}],
    'sample_false_negatives': [   {   'smiles': 'O=C/C=C/C=C/C=C/C=C/C=C/C=C/C=O',
                                      'name': '2,4,6,8,10,12-tetradeca-1,14-hexenedial',
                                      'reason': 'Expected exactly one carbonyl '
                                                'group; found 2'},
                                  {   'smiles': 'O=C/C=C\\C=C\\C=O',
                                      'name': '(E,E)-2,4-Hexadienedial',
                                      'reason': 'Expected exactly one carbonyl '
                                                'group; found 2'},
                                  {   'smiles': 'O=C(CCCCC)CCC=O',
                                      'name': '4-Oxononanal',
                                      'reason': 'Expected exactly one carbonyl '
                                                'group; found 2'},
                                  {   'smiles': 'O=C(CCCCCCCCCC=C)CC=O',
                                      'name': '3-oxo-13-Tetradecenal',
                                      'reason': 'Expected exactly one carbonyl '
                                                'group; found 2'},
                                  {   'smiles': 'O=CCCCC/C=C/C=O',
                                      'name': '2-octenedial',
                                      'reason': 'Expected exactly one carbonyl '
                                                'group; found 2'},
                                  {   'smiles': 'O=CCCCCC=O',
                                      'name': 'Adipaldehyde',
                                      'reason': 'Expected exactly one carbonyl '
                                                'group; found 2'},
                                  {   'smiles': '[H]C(C(C)(C)C)=O',
                                      'name': '2,2-dimethylpropanal',
                                      'reason': 'Not enough carbon atoms (5 '
                                                'found; need at least 6) for a '
                                                'fatty chain'},
                                  {   'smiles': 'O=C(CCCCC/C=C\\CCCCCC)CC=O',
                                      'name': '3-oxo-9Z-Hexadecenal',
                                      'reason': 'Expected exactly one carbonyl '
                                                'group; found 2'},
                                  {   'smiles': 'O=C(CCCCCCCCCCC)CC=O',
                                      'name': '3-oxo-Tetradecanal',
                                      'reason': 'Expected exactly one carbonyl '
                                                'group; found 2'},
                                  {   'smiles': 'CCCCCCCCCC(=O)CC=O',
                                      'name': 'Decanoyl acetaldehyde',
                                      'reason': 'Expected exactly one carbonyl '
                                                'group; found 2'}],
    'attempt': 4,
    'reasoning': 'Below is our step‐by‐step reasoning and the complete Python '
                 'code. In our improved version we still follow the basic '
                 'criteria (allowed elements, acyclic, minimum number of '
                 'carbons, heavy‐atom composition, exactly one carbonyl group '
                 'and that carbonyl being a terminal aldehyde). In addition we '
                 'compute the “longest carbon chain” (by restricting the '
                 'molecule to its carbon–atom graph, which is a tree for an '
                 'acyclic molecule) and require that this chain represents '
                 'most of the carbon skeleton (here we demand that the longest '
                 'chain contains at least 75% of all carbon atoms). This extra '
                 'check helps filter out molecules that are “branched” or '
                 'highly conjugated (for example many carotenoid‐like '
                 'compounds) that were giving false positives in our earlier '
                 'attempt. \n'
                 '\n'
                 'Below is the complete code in a single Python block:\n'
                 '\n'
                 '------------------------------------------------',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 186,
    'num_false_positives': 47,
    'num_true_negatives': 142043,
    'num_false_negatives': 24,
    'num_negatives': None,
    'precision': 0.7982832618025751,
    'recall': 0.8857142857142857,
    'f1': 0.8397291196388261,
    'accuracy': 0.9995010541110331,
    'negative_predictive_value': 0.9998310656239662}