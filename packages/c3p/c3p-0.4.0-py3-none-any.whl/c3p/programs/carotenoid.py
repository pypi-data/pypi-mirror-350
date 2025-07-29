"""
Classifies: CHEBI:23044 carotenoid
"""
#!/usr/bin/env python3
"""
Classifies: Carotenoid
Definition: Carotenoids are tetraterpenoids (typically having a ~C40 core) derived from psi,psi‐carotene.
They characteristically contain an extended, non‐aromatic conjugated polyene system.
Only atoms C, H, O (and optionally P) are allowed.
This improved version requires:
  – >= 40 carbon atoms in the whole molecule,
  – a molecular weight of at least 400 Da,
  – and an extended, linear conjugated polyene system of at least 10 connected sp² carbons.
"""
from rdkit import Chem
from rdkit.Chem import rdMolDescriptors
from collections import defaultdict, deque

def is_carotenoid(smiles: str):
    """
    Determines if a molecule is a carotenoid based on its SMILES string.
    
    Requirements:
      - Only atoms C, H, O, and optionally P are allowed.
      - Must have a sufficiently large carbon skeleton (>=40 carbons) indicative of a tetraterpenoid core.
      - Must have a molecular weight of at least 400 Da.
      - Must feature an extended, non‐aromatic conjugated polyene system of at least 10 sp² carbons.
    
    Args:
        smiles (str): SMILES string of the molecule.
    
    Returns:
        bool: True if the molecule is classified as a carotenoid, False otherwise.
        str: Explanation for the decision.
    """
    # Parse the SMILES string.
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Allowed atoms are: hydrogen, carbon, oxygen, and phosphorus.
    allowed_atoms = {1, 6, 8, 15}
    for atom in mol.GetAtoms():
        if atom.GetAtomicNum() not in allowed_atoms:
            return False, f"Contains disallowed heteroatom: {atom.GetSymbol()}"

    # Count carbons (this is our first filter: we require at least 40 carbons)
    carbon_count = sum(1 for atom in mol.GetAtoms() if atom.GetAtomicNum() == 6)
    if carbon_count < 40:
        return False, f"Too few carbon atoms ({carbon_count}) to be a carotenoid (expected ~40 in the core)"

    # Check molecular weight (most carotenoids have MW > 400 Da)
    mw = rdMolDescriptors.CalcExactMolWt(mol)
    if mw < 400:
        return False, f"Molecular weight too low ({mw:.1f} Da) for a carotenoid"

    # Identify sp2-hybridized carbon atoms (candidates for the polyene chain)
    sp2_carbon_indices = set()
    for atom in mol.GetAtoms():
        if atom.GetAtomicNum() == 6 and atom.GetHybridization() == Chem.rdchem.HybridizationType.SP2:
            sp2_carbon_indices.add(atom.GetIdx())

    # Build a graph among sp2 carbons. Two nodes are connected if they are bonded by a conjugated bond.
    graph = defaultdict(list)
    for bond in mol.GetBonds():
        a1 = bond.GetBeginAtom()
        a2 = bond.GetEndAtom()
        if a1.GetIdx() in sp2_carbon_indices and a2.GetIdx() in sp2_carbon_indices:
            if bond.GetIsConjugated():
                graph[a1.GetIdx()].append(a2.GetIdx())
                graph[a2.GetIdx()].append(a1.GetIdx())
    # Ensure that isolated sp2 carbons get an empty list entry.
    for idx in sp2_carbon_indices:
        if idx not in graph:
            graph[idx] = []

    if not graph:
        return False, "No conjugated sp2 carbon system detected"

    # Helper function: perform a breadth-first search (BFS) in a given component.
    def bfs(start, component_nodes):
        visited = {start}
        queue = deque([(start, 1)])  # distance: count starting node as 1
        max_distance = 1
        farthest_node = start
        while queue:
            current, dist = queue.popleft()
            if dist > max_distance:
                max_distance = dist
                farthest_node = current
            for neighbor in graph[current]:
                if neighbor in component_nodes and neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, dist + 1))
        return farthest_node, max_distance

    # Identify connected components (subsets) of the conjugated sp2-carbon graph.
    components = []
    seen = set()
    for node in graph:
        if node not in seen:
            comp_nodes = set()
            stack = [node]
            while stack:
                cur = stack.pop()
                if cur not in comp_nodes:
                    comp_nodes.add(cur)
                    for neighbor in graph[cur]:
                        if neighbor not in comp_nodes:
                            stack.append(neighbor)
            seen |= comp_nodes
            components.append(comp_nodes)

    # Among the components, find the longest chain length (the diameter) for a non‐aromatic polyene.
    longest_chain = 0
    for comp in components:
        # Exclude a component if any atom in it is aromatic (we require a non‐aromatic conjugated polyene)
        if any(mol.GetAtomWithIdx(idx).GetIsAromatic() for idx in comp):
            continue
        # For a cyclic component (if every node has degree 2 and size>=3), we take its size.
        is_cycle = all(len(graph[n]) == 2 for n in comp) and (len(comp) >= 3)
        if is_cycle:
            chain_length = len(comp)
        else:
            # Use two passes of BFS to approximate the diameter of the tree-like structure.
            start = next(iter(comp))
            far_node, _ = bfs(start, comp)
            _, chain_length = bfs(far_node, comp)
        if chain_length > longest_chain:
            longest_chain = chain_length

    # Require that the longest conjugated polyene chain has at least 10 sp2 carbons.
    if longest_chain < 10:
        return False, f"No extended conjugated polyene system found (longest chain length = {longest_chain})"

    # If all checks pass, we classify the molecule as a carotenoid.
    msg = (f"Found {carbon_count} carbons, MW {mw:.1f} Da, "
           f"and a conjugated chain of {longest_chain} sp2 carbons consistent with carotenoid structure")
    return True, msg

# Example usage (this section is only run when executing as script)
if __name__ == "__main__":
    # Replace the following SMILES with any test candidate.
    test_smiles = "CC(=C/C=C/C(=C/C=C/C(=C/C=C/C(=C/C=C/C(=C/C=C/C(=C/C)C)C)C)C)C)C"
    result, reason = is_carotenoid(test_smiles)
    print("Is carotenoid?", result)
    print("Reason:", reason)


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:23044',
                          'name': 'carotenoid',
                          'definition': 'One of a class of tetraterpenoids '
                                        '(C40), formally derived from the '
                                        'acyclic parent, psi,psi-carotene by '
                                        'hydrogenation, dehydrogenation, '
                                        'cyclization, oxidation, or '
                                        'combination of these processes. This '
                                        'class includes carotenes, '
                                        'xanthophylls and certain compounds '
                                        'that arise from rearrangement of the '
                                        'skeleton of psi,psi-carotene or by '
                                        'loss of part of this structure. '
                                        'Retinoids are excluded.',
                          'parents': ['CHEBI:26935'],
                          'xrefs': ['CAS:36-88-4'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 111,
                           'log_lines_of_code': 4.709530201312334,
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
                                                 2,
                                                 3,
                                                 0,
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
                                                 2,
                                                 3,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 4,
                                                 4,
                                                 1,
                                                 1,
                                                 2,
                                                 3,
                                                 0,
                                                 1,
                                                 2,
                                                 0,
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
                                                 4,
                                                 3,
                                                 4,
                                                 5,
                                                 5,
                                                 2,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 3,
                                                 3,
                                                 3,
                                                 4,
                                                 4,
                                                 5,
                                                 5,
                                                 6,
                                                 7,
                                                 3,
                                                 3,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 3,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 2,
                                                 3,
                                                 3,
                                                 3,
                                                 3,
                                                 2,
                                                 3,
                                                 0,
                                                 1,
                                                 1,
                                                 2,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1],
                           'max_indent': 7,
                           'imports': [   'from rdkit import Chem',
                                          'from rdkit.Chem import '
                                          'rdMolDescriptors',
                                          'from collections import '
                                          'defaultdict, deque'],
                           'imports_count': 3,
                           'methods_called': [   'CalcExactMolWt',
                                                 'append',
                                                 'GetSymbol',
                                                 'GetHybridization',
                                                 'GetIdx',
                                                 'GetAtomicNum',
                                                 'MolFromSmiles',
                                                 'GetBonds',
                                                 'GetAtomWithIdx',
                                                 'GetAtoms',
                                                 'pop',
                                                 'GetBeginAtom',
                                                 'add',
                                                 'GetIsConjugated',
                                                 'popleft',
                                                 'GetIsAromatic',
                                                 'GetEndAtom'],
                           'methods_called_count': 17,
                           'smarts_strings': [],
                           'smarts_strings_count': 0,
                           'defs': [   'is_carotenoid(smiles: str):',
                                       'bfs(start, component_nodes):'],
                           'defs_count': 2,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, f"Contains disallowed '
                                          'heteroatom: {atom.GetSymbol()}"',
                                          'False, f"Too few carbon atoms '
                                          '({carbon_count}) to be a carotenoid '
                                          '(expected ~40 in the core)"',
                                          'False, f"Molecular weight too low '
                                          '({mw:.1f} Da) for a carotenoid"',
                                          'False, "No conjugated sp2 carbon '
                                          'system detected"',
                                          'farthest_node, max_distance',
                                          'False, f"No extended conjugated '
                                          'polyene system found (longest chain '
                                          'length = {longest_chain})"',
                                          'True, msg'],
                           'returns_count': 8,
                           'complexity': 7.741906040262466},
    'message': '\n'
               'Attempt failed: F1 score of 0.7469879518072289 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: '
               'O=C1C(=C(/C=C/C(=C/C=C/C(=C/C=C/C=C(/C=C/C=C(/C=C/C=C(/CCCC(OC2OC(C(O)C(C2O)O)COC(=O)C(C(O)CCCCCCCCCCCCCCCCCCCC(/C=C\\CCCCCCCCCCCCCC(=O)O)C)CCCCCCCCCCCCCCCCCCCC)(C)C)\\C)\\C)\\C)/C)/C)C(C)(C)CC1)C '
               "NAME: 1'-[(6-O-Mycoloyl-beta-D-glucopyranosyl) REASON: CORRECT "
               'Found 106 carbons and a conjugated chain of 23 sp2 carbons '
               'consistent with carotenoids\n'
               ' * SMILES: '
               'CO[C@@H]1[C@H](C)O[C@@H](O[C@@H](\\C=C\\C(C)=C\\C=C\\C(C)=C\\C=C\\C(C)=C\\C=C\\C=C(C)\\C=C\\C=C(C)\\C=C\\C2=C(C)C[C@@H](O)CC2(C)C)C(C)(C)O)[C@@H](OC)[C@@H]1O '
               "NAME: (3R,2'S)-Myxol 2'-(2,4-di-O-methyl-alpha-L-fucoside) "
               'REASON: CORRECT Found 48 carbons and a conjugated chain of 24 '
               'sp2 carbons consistent with carotenoids\n'
               ' * SMILES: '
               'O[C@@H]1CC([C@H](C(=C1)C)/C=C/C(/C)=C/C=C/C(/C)=C/C=C/C=C(/C=C/C=C(/C=C/C=2C(C[C@H](O)C(=O)C2C)(C)C)\\C)\\C)(C)C '
               "NAME: Fritschiellaxanthin/ (3S,3'R,6'R)-4-Ketolutein REASON: "
               'CORRECT Found 40 carbons and a conjugated chain of 21 sp2 '
               'carbons consistent with carotenoids\n'
               ' * SMILES: '
               'O[C@H]1CC(C(=C(C1)C)/C=C/C(/C)=C/C=C/C(/C)=C/C=C/C=C(/C=C/C=C(\\C=C\\C=2C(C[C@H](O)CC2C)(C)C)/C)\\C)(C)C '
               "NAME: (3R,3'R,9-cis)-b,b-Carotene-3,3'-diol REASON: CORRECT "
               'Found 40 carbons and a conjugated chain of 22 sp2 carbons '
               'consistent with carotenoids\n'
               ' * SMILES: '
               '[C@@]12(C(C[C@@H](C[C@]1(O2)C)OC(=O)CCCCCCCCCCCCC)(C)C)CC(/C(=C/C=C/C(=C/C=C/C=C(/C=C/C=C(/C=[C@]=C3C(C[C@@H](C[C@@]3(C)O)O)(C)C)\\C)\\C)/C)/C)=O '
               'NAME: Fucoxanthinol 3-myristate REASON: CORRECT Found 54 '
               'carbons and a conjugated chain of 16 sp2 carbons consistent '
               'with carotenoids\n'
               ' * SMILES: '
               'CC(\\C=C\\C=C(C)\\C=C\\C1C(C)=CC(O)CC1(C)C)=C/C=C/C=C(C)/C=C/C=C(C)/C=C/C1C(C)=CC(O)CC1(C)C '
               'NAME: tunaxanthin REASON: CORRECT Found 40 carbons and a '
               'conjugated chain of 18 sp2 carbons consistent with '
               'carotenoids\n'
               ' * SMILES: '
               'OC1CC([C@@H](C(=C1)C)/C=C/C(/C)=C/C=C/C(/C)=C/C=C/C=C(\\C=C\\C=C(\\C=C\\C=2C(C[C@H](O)CC2C)(C)C)/C)/C)(C)C '
               "NAME: (3R,3'R,6'R,13-cis)-b,e-Carotene-3,3'-diol REASON: "
               'CORRECT Found 40 carbons and a conjugated chain of 20 sp2 '
               'carbons consistent with carotenoids\n'
               ' * SMILES: '
               'CO[C@@H]1[C@H](C)O[C@@H](O[C@@H](\\C=C\\C(C)=C\\C=C\\C(C)=C\\C=C\\C(C)=C\\C=C\\C=C(C)\\C=C\\C=C(C)\\C=C\\C2=C(C)CCCC2(C)C)C(C)(C)O)[C@@H](OC)[C@@H]1O '
               "NAME: (2'S)-Deoxymyxol 2'-(2,4-di-O-methyl-alpha-L-fucoside) "
               'REASON: CORRECT Found 48 carbons and a conjugated chain of 24 '
               'sp2 carbons consistent with carotenoids\n'
               ' * SMILES: '
               'O1C(C1CC/C(/C)=C\\C=C\\C(\\C)=C\\C=C\\C(=C/C=C/C=C(/C=C/C=C(\\C=C\\C2C(CCC=C2C)(C)C)/C)\\C)\\C)(C)C '
               'NAME: delta-Carotene-1,2-epoxide REASON: CORRECT Found 40 '
               'carbons and a conjugated chain of 20 sp2 carbons consistent '
               'with carotenoids\n'
               ' * SMILES: '
               'OC([C@H](O)/C=C/C(=C/C=C/C(=C/C=C/C(=C/C=C/C=C(/C=C/C=C(/C=C/C1=C(CC(O)CC1(C)C)C)\\C)\\C)/C)/C)/C)(C)C '
               'NAME: Myxol (II) REASON: CORRECT Found 40 carbons and a '
               'conjugated chain of 24 sp2 carbons consistent with '
               'carotenoids\n'
               ' * SMILES: '
               'O([C@H]1CC(C(=C(C1)C)\\C=C\\C(\\C)=C\\C=C\\C(\\C)=C\\C=C\\C=C(\\C=C\\C=C(\\C=C\\C=2C(C[C@H](O)C(=O)C2C)(C)C)/C)/C)(C)C)[C@@H]3O[C@@H]([C@@H](O)C(O)C3O)CO '
               "NAME: Adonixanthin 3'-beta-D-glucoside/ Adonixanthin "
               "3'-glucoside REASON: CORRECT Found 46 carbons and a conjugated "
               'chain of 23 sp2 carbons consistent with carotenoids\n'
               ' * SMILES: '
               'O=C1C(=C(/C=C/C(=C/C=C/C(=C/C=C/C=C(/C=C/C=C(/C=C/C=C(/C=C/[C@H](O)C(O[C@H]2O[C@H]([C@H](O)[C@H]([C@@H]2O)O)COC(=O)CCCCCCCCCCCC(C)C)(C)C)\\C)\\C)\\C)/C)/C)C(C)(C)CC1)C '
               'NAME: Salinixanthin REASON: CORRECT Found 61 carbons and a '
               'conjugated chain of 25 sp2 carbons consistent with '
               'carotenoids\n'
               ' * SMILES: '
               'CC(\\C=C\\C=C(/C)C1OC2(C)CC(O)CC(C)(C)C2=C1)=C/C=C/C=C(C)/C=C/C=C(\\C)C1OC2(C)CC(O)CC(C)(C)C2=C1 '
               'NAME: auroxanthin REASON: CORRECT Found 40 carbons and a '
               'conjugated chain of 14 sp2 carbons consistent with '
               'carotenoids\n'
               ' * SMILES: '
               'COC(C)(C)C\\C=C\\C(C)=C\\C=C\\C(C)=C\\C=C\\C(C)=C\\C=C\\C=C(C)\\C=C\\C=C(C)\\C=C\\C=C(C)\\C=C\\CC(C)(C)OC '
               'NAME: spirilloxanthin REASON: CORRECT Found 42 carbons and a '
               'conjugated chain of 26 sp2 carbons consistent with '
               'carotenoids\n'
               ' * SMILES: '
               'C=1(C(C[C@@H](C(C1C)=O)O)(C)C)/C=C/C(=C/C=C/C(=C/C=C/C=C(/C=C/C=C(/C=C/C=2C(C[C@@H](CC2C)O)(C)C)\\C)\\C)/C)/C '
               'NAME: adonixanthin REASON: CORRECT Found 40 carbons and a '
               'conjugated chain of 23 sp2 carbons consistent with '
               'carotenoids\n'
               ' * SMILES: '
               'C(=C(/CCC=C(C)C)\\C)\\CC/C(=C/C=C/C(=C/C=C/C=C(/C=C/C=C(/C=C/C=C(/C=C/C(C(OC)(C)C)(O)O)\\C)\\C)\\C)/C)/C '
               'NAME: 2,2-dihydroxyspheroidene REASON: CORRECT Found 41 '
               'carbons and a conjugated chain of 20 sp2 carbons consistent '
               'with carotenoids\n'
               ' * SMILES: '
               'CC(\\C=C\\C1=C(C)CCCC1(C)C)=C/C=C/C(C)=C/C(O)C(O)\\C=C(C)\\C=C\\C=C(C)\\C=C\\C1=C(C)CCCC1(C)C '
               "NAME: 15,15'-dihydroxy-beta-carotene REASON: CORRECT Found 40 "
               'carbons and a conjugated chain of 10 sp2 carbons consistent '
               'with carotenoids\n'
               ' * SMILES: '
               'CC(\\C=C\\C=C(C)\\C=C\\C(=O)[C@]1(C)C[C@@H](O)CC1(C)C)=C/C=C/C=C(C)/C=C/C=C(C)/C=C/C(=O)[C@]1(C)C[C@@H](O)CC1(C)C '
               'NAME: capsorubin REASON: CORRECT Found 40 carbons and a '
               'conjugated chain of 20 sp2 carbons consistent with '
               'carotenoids\n'
               ' * SMILES: '
               'O=C1C(=C(/C=C/C(=C/C=C/C(=C/C=C/C=C(/C=C/C=C(/C=C/C2=C(C[C@@H](O)[C@@H](C2(C)C)O)C)\\C)\\C)/C)/C)C(C)(C)[C@H]([C@@H]1O)O)C '
               'NAME: '
               '(2R,3S,2′R,3′R)-2,3,2′,3′-tetrahydroxy-beta,beta-caroten-4-one '
               'REASON: CORRECT Found 40 carbons and a conjugated chain of 23 '
               'sp2 carbons consistent with carotenoids\n'
               ' * SMILES: '
               'O=C(O)/C(=C/C=C/C(=C/C=C/C(=C/C=C/C(=C/C=C/C=C(/C=C/C=C(/C=C/C1=C(CCCC1(C)C)C)\\C)\\C)/C)/C)/C)/C '
               'NAME: Torularhodin REASON: CORRECT Found 40 carbons and a '
               'conjugated chain of 27 sp2 carbons consistent with '
               'carotenoids\n'
               ' * SMILES: '
               'COC(C)(C)C(=O)\\C=C\\C(C)=C\\C=C\\C(C)=C\\C=C\\C(C)=C\\C=C\\C=C(C)\\C=C\\C=C(/C)CC\\C=C(/C)CCCC(C)(C)O '
               'NAME: Hydroxyspheroidenone REASON: CORRECT Found 41 carbons '
               'and a conjugated chain of 21 sp2 carbons consistent with '
               'carotenoids\n'
               ' * SMILES: '
               'OC/C(=C/CC1C(C(C(C)=CC1)/C=C/C(=C/C=C/C(=C/C=C/C=C(/CC/C=C(/CC/C=C(/CCC=C(C)C)\\C)\\C)\\C)/C)/C)(C)C)/C '
               'NAME: Nonaprenoxanthin REASON: CORRECT Found 45 carbons and a '
               'conjugated chain of 12 sp2 carbons consistent with '
               'carotenoids\n'
               ' * SMILES: '
               'O([C@H]1CC(C(=C(C1=O)C)\\C=C\\C(\\C)=C\\C=C\\C(\\C)=C\\C=C\\C=C(\\C=C\\C=C(\\C=C\\C=2C(C[C@H](O[C@@H]3O[C@@H]([C@@H](O)C(O)C3O)CO)C(=O)C2C)(C)C)/C)/C)(C)C)[C@@H]4O[C@@H]([C@@H](O)C(O)C4O)CO '
               'NAME: Astaxanthin diglucoside/ Astaxanthin beta-D-diglucoside '
               'REASON: CORRECT Found 52 carbons and a conjugated chain of 24 '
               'sp2 carbons consistent with carotenoids\n'
               ' * SMILES: '
               'COC(C)(C)CCC/C(/C)=C/C=C/C(/C)=C/C=C/C(/C)=C/C=C/C=C(\\C)/C=C/C=C(\\C)/C=C/C=C(\\C)/CCCC(C)(C)O[C@]1(O[C@@](COC(C)=O)([C@@H](O)C(O)C1O)[H])[H] '
               'NAME: dihydroxylycopene diglucoside diester REASON: CORRECT '
               'Found 49 carbons and a conjugated chain of 22 sp2 carbons '
               'consistent with carotenoids\n'
               ' * SMILES: '
               'O=C1C(=C(/C=C/C(=C/C=C/C(=C/C=C/C=C(/C=C/C=C(/C=C/C=C(/C=C/[C@@H](OC)C(O)(C)C)\\C)\\C)\\C)/C)/C)C(C)(C)CC1)C '
               "NAME: 2'-methoxy-1'-hydroxy-beta,psi-caroten-4-one REASON: "
               'CORRECT Found 41 carbons and a conjugated chain of 25 sp2 '
               'carbons consistent with carotenoids\n'
               'False positives: SMILES: '
               'O=C(/C(=C/C=C/C=C/C=C/C=C/C[C@H]1O[C@@]2(OC(/C=C/C[C@@H](O)C[C@@H](O)C[C@H](O)C[C@H](O)[C@@H]([C@@H](O)C(C)C)C)C[C@H](C2)O)C[C@H](C1)O)/C)C '
               'NAME: Marinisporolide A REASON: WRONGLY CLASSIFIED Found 39 '
               'carbons and a conjugated chain of 11 sp2 carbons consistent '
               'with carotenoids\n'
               ' * SMILES: '
               'CC(C)=CCC\\C(C)=C/C=C/C(/C)=C/C=C/C(/C)=C/C=C/C=C(\\C)/C=C/C=C(\\C)/C=C/C=C(\\C)CCC=C(C)C '
               'NAME: 5-cis-lycopene REASON: WRONGLY CLASSIFIED Found 40 '
               'carbons and a conjugated chain of 22 sp2 carbons consistent '
               'with carotenoids\n'
               ' * SMILES: '
               'CCC(C)C1OC(=O)\\C=C/C=C/C=C/C=C/C=C/CC(O)CC(O)CC(O)CC(O)CC(O)CC(O)CC(O)CC(O)\\C=C\\C1C '
               'NAME: reedsmycin C REASON: WRONGLY CLASSIFIED Found 36 carbons '
               'and a conjugated chain of 11 sp2 carbons consistent with '
               'carotenoids\n'
               ' * SMILES: '
               'CCCCC\\C=C/C\\C=C/CCCCCCCC(=O)OC\\C=C(C)\\C=C\\C=C(C)\\C=C\\C1=C(C)CCCC1(C)C '
               'NAME: all-trans-retinyl linoleate REASON: WRONGLY CLASSIFIED '
               'Found 38 carbons and a conjugated chain of 10 sp2 carbons '
               'consistent with carotenoids\n'
               ' * SMILES: '
               'O1C2(C1(CC(O)CC2(C)C)C)/C=C/C3=C\\C(\\OC3=O)=C\\C(\\C)=C\\C=C/C=C/C=C(/C#CC=4C(CC(O)CC4C)(C)C)\\C '
               'NAME: Pyrrhoxanthinol REASON: WRONGLY CLASSIFIED Found 37 '
               'carbons and a conjugated chain of 14 sp2 carbons consistent '
               'with carotenoids\n'
               ' * SMILES: '
               'O(C1CC(C(C(O)(C1)C)=C=C/C(/C)=C/C=C/C=C/C=C(/C=C/2\\OC(=O)C(\\C=C\\C3(O)C(CC(=O)C=C3C)(C)C)=C2)\\C)(C)C)C(=O)C '
               'NAME: '
               "(3S,5R,6R,6'S)-6,7-Didehydro-5,6-dihydro-3,5,6'-trihydroxy-13,14,20-trinor-3'-oxo-beta,epsilon-caroten-19',11'-olide "
               '3-acetate REASON: WRONGLY CLASSIFIED Found 39 carbons and a '
               'conjugated chain of 15 sp2 carbons consistent with '
               'carotenoids\n'
               ' * SMILES: '
               'O=C(OC1OC(C(O)C(C1OC(=O)CCCCCCCCCC=CCCCCCC)O)CO)C(=CC=CC(=CC=CC(=CC=CC=C(C=CC=C(C=CC=C(C(=O)O)C)C)C)C)C)C '
               'NAME: '
               '4-[2-O-11Z-octadecenoyl-beta-glucopyranosyl]-4,4′-diapolycopene-4,4′-dioic '
               'acid REASON: WRONGLY CLASSIFIED Found 54 carbons and a '
               'conjugated chain of 24 sp2 carbons consistent with '
               'carotenoids\n'
               ' * SMILES: '
               'O=C1OC(C(C=CC(O)CC(O)CC(O)CC(O)CC(O)CC(O)CC(C(C(CC=CC=CC=CC=CC=C1)O)C)O)C)C(C)C '
               'NAME: Mycoticin A REASON: WRONGLY CLASSIFIED Found 36 carbons '
               'and a conjugated chain of 11 sp2 carbons consistent with '
               'carotenoids\n'
               ' * SMILES: '
               'C1CCC(=C(\\C=C\\C(=C/C=C/C(=C/COC(CCCCCCCCCCCCCCC)=O)/C)\\C)C1(C)C)C '
               'NAME: 9-cis-retinyl hexadecanoate REASON: WRONGLY CLASSIFIED '
               'Found 36 carbons and a conjugated chain of 10 sp2 carbons '
               'consistent with carotenoids\n'
               ' * SMILES: '
               'C=1(C(C[C@@H](CC1C)OC2O[C@@H]([C@H]([C@@H]([C@H]2O)O)O)COC(=O)CCCCCCCCCCCC(C)C)(C)C)/C=C/C(=C/C=C/C(=C/C=C/C=C(/C=C/C=C(/C=C/C=3C(C[C@@H](CC3C)O)(C)C)\\C)\\C)/C)/C '
               'NAME: Thermozeaxanthin-15 REASON: WRONGLY CLASSIFIED Found 61 '
               'carbons and a conjugated chain of 22 sp2 carbons consistent '
               'with carotenoids\n'
               ' * SMILES: '
               'O1[C@]([C@@H](C[C@@H]1CC(=O)C)C)(CC(=O)/C(/C)=C/C=C/C(/C)=C/C=C/C=C(/C=C/C=C(/C#CC=2C(C[C@H](O)CC2C)(C)C)\\C)\\C)C '
               'NAME: Crassostreaxanthin A REASON: WRONGLY CLASSIFIED Found 40 '
               'carbons and a conjugated chain of 15 sp2 carbons consistent '
               'with carotenoids\n'
               ' * SMILES: '
               'O=C(O)C[C@H](OC)\\C=C/C=C/C=C\\C=C\\C=C/[C@@H]([C@H](O)[C@@H]([C@H]1O[C@]2(O[C@@H]([C@H](C)[C@@H](C2)OC)[C@@H]([C@@H](O)[C@H](C/C(=C/CC)/C)C)C)[C@@H](O)C[C@@H]1C)C)C '
               'NAME: Spirangien B REASON: WRONGLY CLASSIFIED Found 42 carbons '
               'and a conjugated chain of 10 sp2 carbons consistent with '
               'carotenoids\n'
               ' * SMILES: '
               'C=1(\\C=C\\C(=C\\C=C\\C(\\C)=C/COC(CCCCCCCCCCCCCCC)=O)\\C)C(C)(C)CCCC1C '
               'NAME: 13-cis-retinyl hexadecanoate REASON: WRONGLY CLASSIFIED '
               'Found 36 carbons and a conjugated chain of 10 sp2 carbons '
               'consistent with carotenoids\n'
               ' * SMILES: '
               'CC(C)=CCC\\C(C)=C\\CC\\C(C)=C\\C=C\\C(C)=C\\C=C/C=C(C)/C=C/C=C(\\C)CC\\C=C(/C)CCC=C(C)C '
               'NAME: 15-cis-zeta-carotene REASON: WRONGLY CLASSIFIED Found 40 '
               'carbons and a conjugated chain of 14 sp2 carbons consistent '
               'with carotenoids\n'
               ' * SMILES: '
               'O=C(O[C@@H]1OC[C@@H](O)[C@@H]([C@H]1OC(=O)CCCCCCCCCCC(C)C)O)/C(=C/C=C/C(=C/C=C/C(=C/C=C/C=C(/C=C/C=C(/C=C/C=C(/C(=O)O)\\C)\\C)\\C)/C)/C)/C '
               'NAME: Diapolycopenedioic acid xylosyl ester REASON: WRONGLY '
               'CLASSIFIED Found 49 carbons and a conjugated chain of 24 sp2 '
               'carbons consistent with carotenoids\n'
               ' * SMILES: '
               'CC(C)=CCC\\C(C)=C\\C=C\\C(C)=C\\C=C\\C=C(C)\\C=C\\C=C(C)\\C=C\\C=C(/C)C(=O)O[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O '
               "NAME: Glycosyl-4,4'-diaponeurosporenoate REASON: WRONGLY "
               'CLASSIFIED Found 36 carbons and a conjugated chain of 19 sp2 '
               'carbons consistent with carotenoids\n'
               ' * SMILES: '
               '[H]C(=CC=C(C)C([H])=CC=C(C)CCC=C(C)CCC=C(C)C)C=C(C)C=C([H])C=C(C)CCC=C(C)CCC=C(C)C '
               'NAME: zeta-carotene REASON: WRONGLY CLASSIFIED Found 40 '
               'carbons and a conjugated chain of 14 sp2 carbons consistent '
               'with carotenoids\n'
               ' * SMILES: '
               'O=C(OC)C(=CC=CC(=CC=CC(=CC=CC=C(C=CC=C(C=CCC(CC1OC(C(O)C(C1O)O)CO)(C)C)C)C)C)C)C '
               'NAME: methyl 5-glucosyl-5,6-dihydro-apo-4,4′-lycopenoate '
               'REASON: WRONGLY CLASSIFIED Found 38 carbons and a conjugated '
               'chain of 21 sp2 carbons consistent with carotenoids\n'
               ' * SMILES: '
               'CC(C)=CCC\\C(C)=C\\CC\\C(C)=C\\C=C\\C(C)=C\\C=C\\C=C(C)\\C=C\\C=C(/C)CC\\C=C(/C)CCC=C(C)C '
               'NAME: all-trans-zeta-carotene REASON: WRONGLY CLASSIFIED Found '
               '40 carbons and a conjugated chain of 14 sp2 carbons consistent '
               'with carotenoids\n'
               ' * SMILES: '
               'CCC(C)C1OC(=O)\\C=C\\C=C\\C=C\\C=C\\C=C\\CC(O)CC(O)CC(O)CC(O)CC(O)CC(O)CC(O)CC(O)\\C=C\\C1C '
               'NAME: reedsmycin A REASON: WRONGLY CLASSIFIED Found 36 carbons '
               'and a conjugated chain of 11 sp2 carbons consistent with '
               'carotenoids\n'
               ' * SMILES: '
               'O1C(/C(=C/C=C/C(=C/C=C/C(=C/C=C/C=C(/C=C/C=C(/C=C/C=C(/C=C/[C@@H](C(O)(C)C)CCC(O)(C)C)\\C)\\C)\\C)/C)/C)/C)C1C(C(O)(C)C)CC=C(C)C '
               "NAME: 3',4'-Epoxymonoanhydrobacterioruberin REASON: WRONGLY "
               'CLASSIFIED Found 50 carbons and a conjugated chain of 24 sp2 '
               'carbons consistent with carotenoids\n'
               ' * SMILES: '
               'OC1(C(CC(=O)CC1C)(C)C)CC(=O)/C(/C)=C/C=C\\C(\\C)=C\\C=C\\C=C(/C=C\\C=C(/C#CC=2C(CC(O)CC2C)(C)C)\\COC(=O)CCCCC)\\C '
               "NAME: 19'-Hexanoyloxymytiloxanthin REASON: WRONGLY CLASSIFIED "
               'Found 46 carbons and a conjugated chain of 15 sp2 carbons '
               'consistent with carotenoids\n'
               ' * SMILES: '
               'O(C\\C=C(\\CC\\C=C(\\CC\\C=C(\\CCC=C(C)C)/C)/C)/C)C(=O)/C=C/C(/C)=C/C=C/C(=C/C=C/C=C(/C=C/C=C(\\C)/C(OC)=O)\\C)/C '
               "NAME: 6-Geranylgeranyl 8'-methyl "
               "6,8'-diapocarotene-6,8'-dioate REASON: WRONGLY CLASSIFIED "
               'Found 43 carbons and a conjugated chain of 18 sp2 carbons '
               'consistent with carotenoids\n'
               ' * SMILES: '
               'O=C1O[C@@H]([C@@H](O)C=CC=CC=CC=CC=C([C@@H](OC[C@H](O)CO)[C@H]([C@@H](C[C@@H](C[C@@H](C[C@@H](C[C@@H](C[C@@H]([C@H]1[C@H](O)CCCCC)O)O)O)O)O)O)O)C)C '
               'NAME: 15-glycidylfilipin III REASON: WRONGLY CLASSIFIED Found '
               '38 carbons and a conjugated chain of 10 sp2 carbons consistent '
               'with carotenoids\n'
               ' * SMILES: '
               'O=C1O[C@H]([C@H]([C@@H](O)C[C@@H](O)C[C@H](O)C[C@H](O)CC=C[C@H](O)C[C@@H](O)C[C@@]2(O[C@H](CC=CC=CC=CC=CC=C1C)C[C@H](O)C2)O)C)C(C)C '
               'NAME: Marinisporolide B REASON: WRONGLY CLASSIFIED Found 38 '
               'carbons and a conjugated chain of 11 sp2 carbons consistent '
               'with carotenoids\n'
               'False negatives: SMILES: '
               'CC(C)=CCC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\[C@H]1[C@H](COP(O)(=O)OP(O)(O)=O)[C@@]1(C)CC\\C=C(/C)CC\\C=C(/C)CCC=C(C)C '
               'NAME: (1S,2S,3S)-prephytoene diphosphate REASON: MISSED No '
               'extended conjugated polyene system found (longest chain length '
               '= 1)\n'
               ' * SMILES: '
               '[H]C(=O)\\C=C\\C=C(C)\\C=C\\C=C(C)\\C=C\\C1=C(C)CCCC1(C)C '
               "NAME: 14'-apo-beta-carotenal REASON: MISSED Too few carbon "
               'atoms (22) to be a carotenoid (expected ~40 in the core)\n'
               ' * SMILES: '
               'C\\C(C=O)=C/C=C/C=C(C)/C=C/C=C(C)/C=C/[C@@]12O[C@]1(C)C[C@@H](O)CC2(C)C '
               'NAME: '
               "(3S,5R,6S)-5,6-epoxy-3-hydroxy-5,6-dihydro-12'-apo-beta-caroten-12'-al "
               'REASON: MISSED Too few carbon atoms (25) to be a carotenoid '
               '(expected ~40 in the core)\n'
               ' * SMILES: '
               'CC(\\C=C\\C=C(C)\\C=C\\c1c(C)ccc(C)c1C)=C/C=C/C=C(C)/C=C/C=C(C)/C=C/c1c(C)ccc(C)c1C '
               'NAME: Isorenieratene REASON: MISSED No extended conjugated '
               'polyene system found (longest chain length = 0)\n'
               ' * SMILES: '
               'S(O[C@H]1CC(C(=C(C1)C)/C=C/C(/C)=C/C=C/C(/C)=C/C=C/C=C(/C=C/C=C(/C=C/C=2C([C@@H](O)[C@H](O)CC2C)(C)C)\\C)\\C)(C)C)(O)(=O)=O '
               'NAME: Caloxanthin sulfate REASON: MISSED Contains disallowed '
               'heteroatom: S\n'
               ' * SMILES: '
               'CC(\\C=C\\C=C(/C)C(O)=O)=C/C=C/C=C(C)/C=C/C=C(\\C)C(O)=O NAME: '
               'crocetin REASON: MISSED Too few carbon atoms (20) to be a '
               'carotenoid (expected ~40 in the core)\n'
               ' * SMILES: '
               'S(O[C@H]1[C@H](O)C(C(=C(C1)C)\\C=C\\C(\\C)=C\\C=C\\C(\\C)=C\\C=C\\C=C(\\C=C\\C=C(\\C=C\\C=2C([C@@H](O)[C@H](O)CC2C)(C)C)/C)/C)(C)C)([O-])(=O)=O.[Na+] '
               'NAME: Nostoxanthin sulfate REASON: MISSED Contains disallowed '
               'heteroatom: S\n'
               ' * SMILES: '
               'S(O[C@H]1[C@H](O)C(C(=C(C1)C)\\C=C\\C(\\C)=C\\C=C\\C(\\C)=C\\C=C\\C=C(\\C=C\\C=C(\\C=C\\C=2C([C@@H](O)[C@H](O)C(=O)C2C)(C)C)/C)/C)(C)C)([O-])(=O)=O.[Na+] '
               'NAME: 4-Ketonostoxanthin 3-sulfate REASON: MISSED Contains '
               'disallowed heteroatom: S\n'
               ' * SMILES: '
               'CC(C)=CCC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\C1C(COP(O)(=O)OP(O)(O)=O)C1(C)CC\\C=C(/C)CC\\C=C(/C)CCC=C(C)C '
               'NAME: prephytoene diphosphate REASON: MISSED No extended '
               'conjugated polyene system found (longest chain length = 1)\n'
               ' * SMILES: '
               'C(\\C=C\\C(OC)=O)(=C\\C=C\\C(=C\\C=C\\C=C(\\C=C\\C=C(\\C=C\\C(=O)O)/C)/C)\\C)/C '
               'NAME: bixin REASON: MISSED Too few carbon atoms (25) to be a '
               'carotenoid (expected ~40 in the core)\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'O=C(N[C@@H](C(O)(C)C)C)[C@H]([C@@]1([C@@]2([C@@](CC1)(/C(/CCC2)=C/C=C\\3/C[C@@H](O)C[C@H](O)C3=C)[H])C)[H])C',
                                     'name': '1alpha,25-dihydroxy-24-oxo-23-azavitamin '
                                             'D2 / '
                                             '1alpha,25-dihydroxy-24-oxo-23-azaergocalciferol',
                                     'reason': 'Contains disallowed '
                                               'heteroatom: N'},
                                 {   'smiles': 'CCCCCCCCCCCCCCCCCCC(O)C([O-])=O',
                                     'name': '2-hydroxyarachidate',
                                     'reason': 'Too few carbon atoms (20) to '
                                               'be a carotenoid (expected ~40 '
                                               'in the core)'},
                                 {   'smiles': 'C[C@@H](CN([C@@H](C)CO)C(=O)NC1=CC=C(C=C1)C(F)(F)F)[C@@H](CN(C)C(=O)C2CCOCC2)OC',
                                     'name': 'N-[(2S,3S)-4-[[(2S)-1-hydroxypropan-2-yl]-[[4-(trifluoromethyl)phenyl]carbamoyl]amino]-2-methoxy-3-methylbutyl]-N-methyloxane-4-carboxamide',
                                     'reason': 'Contains disallowed '
                                               'heteroatom: N'},
                                 {   'smiles': 'CC(=O)CC\\C=C(/C)CCC=C(C)C',
                                     'name': 'geranyl acetone',
                                     'reason': 'Too few carbon atoms (13) to '
                                               'be a carotenoid (expected ~40 '
                                               'in the core)'},
                                 {   'smiles': 'O([C@H]1[C@H](O)[C@H](O[C@H](O)[C@H]1O)CO[C@H]2O[C@@H]([C@@H](O)[C@H](O)[C@@H]2O)CO)[C@H]3O[C@@H]([C@@H](O)[C@H](O)[C@@H]3O[C@H]4O[C@@H]([C@@H](O)[C@H](O)[C@@H]4O)CO)CO',
                                     'name': '(2S,3S,4S,5S,6R)-2-[[(2R,3R,4S,5S,6S)-4-[(2R,3S,4S,5S,6R)-4,5-Dihydroxy-6-(hydroxymethyl)-3-[(2R,3S,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-3,5,6-trihydroxyoxan-2-yl]methoxy]-6-(hydroxymethyl)oxane-3,4,5-triol',
                                     'reason': 'Too few carbon atoms (24) to '
                                               'be a carotenoid (expected ~40 '
                                               'in the core)'},
                                 {   'smiles': 'O=C(OC1=C(C(O)=C(C(=O)O)C(=C1C)C)C)C2=C(OC)C(=C(OC(=O)C3=C(O)C=C(O)C=C3C)C=C2C)C',
                                     'name': 'Thielavin Z5',
                                     'reason': 'Too few carbon atoms (28) to '
                                               'be a carotenoid (expected ~40 '
                                               'in the core)'},
                                 {   'smiles': '[C@@H]1([C@@H]([C@H]([C@@H]([C@H](O1)CO)O)O)NC(C)=O)O[C@@H]2[C@@H]([C@H](C(O[C@@H]2CO)O)O)O',
                                     'name': 'beta-D-GlcpNAc-(1->4)-D-Galp',
                                     'reason': 'Contains disallowed '
                                               'heteroatom: N'},
                                 {   'smiles': 'CN(C)C(=O)C1=CC=C(C=C1)C2=CC=C(C=C2)[C@@H]3[C@H]4CN(CC(=O)N4[C@H]3CO)C(=O)CC5CC5',
                                     'name': '4-[4-[(6S,7R,8R)-4-(2-cyclopropyl-1-oxoethyl)-8-(hydroxymethyl)-2-oxo-1,4-diazabicyclo[4.2.0]octan-7-yl]phenyl]-N,N-dimethylbenzamide',
                                     'reason': 'Contains disallowed '
                                               'heteroatom: N'},
                                 {   'smiles': 'CCCCCCCCCCCCCCCCCCCCC=C',
                                     'name': '1-docosene',
                                     'reason': 'Too few carbon atoms (22) to '
                                               'be a carotenoid (expected ~40 '
                                               'in the core)'},
                                 {   'smiles': 'C([C@@](OC(=O)CCC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)([H])COC(=O)CC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)OC(=O)CCCCC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC',
                                     'name': 'TG(22:5(7Z,10Z,13Z,16Z,19Z)/20:5(5Z,8Z,11Z,14Z,17Z)/22:6(4Z,7Z,10Z,13Z,16Z,19Z))[iso6]',
                                     'reason': 'No extended conjugated polyene '
                                               'system found (longest chain '
                                               'length = 1)'}],
    'sample_false_negatives': [   {   'smiles': 'CC(C)=CCC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\[C@H]1[C@H](COP(O)(=O)OP(O)(O)=O)[C@@]1(C)CC\\C=C(/C)CC\\C=C(/C)CCC=C(C)C',
                                      'name': '(1S,2S,3S)-prephytoene '
                                              'diphosphate',
                                      'reason': 'No extended conjugated '
                                                'polyene system found (longest '
                                                'chain length = 1)'},
                                  {   'smiles': '[H]C(=O)\\C=C\\C=C(C)\\C=C\\C=C(C)\\C=C\\C1=C(C)CCCC1(C)C',
                                      'name': "14'-apo-beta-carotenal",
                                      'reason': 'Too few carbon atoms (22) to '
                                                'be a carotenoid (expected ~40 '
                                                'in the core)'},
                                  {   'smiles': 'C\\C(C=O)=C/C=C/C=C(C)/C=C/C=C(C)/C=C/[C@@]12O[C@]1(C)C[C@@H](O)CC2(C)C',
                                      'name': "(3S,5R,6S)-5,6-epoxy-3-hydroxy-5,6-dihydro-12'-apo-beta-caroten-12'-al",
                                      'reason': 'Too few carbon atoms (25) to '
                                                'be a carotenoid (expected ~40 '
                                                'in the core)'},
                                  {   'smiles': 'CC(\\C=C\\C=C(C)\\C=C\\c1c(C)ccc(C)c1C)=C/C=C/C=C(C)/C=C/C=C(C)/C=C/c1c(C)ccc(C)c1C',
                                      'name': 'Isorenieratene',
                                      'reason': 'No extended conjugated '
                                                'polyene system found (longest '
                                                'chain length = 0)'},
                                  {   'smiles': 'S(O[C@H]1CC(C(=C(C1)C)/C=C/C(/C)=C/C=C/C(/C)=C/C=C/C=C(/C=C/C=C(/C=C/C=2C([C@@H](O)[C@H](O)CC2C)(C)C)\\C)\\C)(C)C)(O)(=O)=O',
                                      'name': 'Caloxanthin sulfate',
                                      'reason': 'Contains disallowed '
                                                'heteroatom: S'},
                                  {   'smiles': 'CC(\\C=C\\C=C(/C)C(O)=O)=C/C=C/C=C(C)/C=C/C=C(\\C)C(O)=O',
                                      'name': 'crocetin',
                                      'reason': 'Too few carbon atoms (20) to '
                                                'be a carotenoid (expected ~40 '
                                                'in the core)'},
                                  {   'smiles': 'S(O[C@H]1[C@H](O)C(C(=C(C1)C)\\C=C\\C(\\C)=C\\C=C\\C(\\C)=C\\C=C\\C=C(\\C=C\\C=C(\\C=C\\C=2C([C@@H](O)[C@H](O)CC2C)(C)C)/C)/C)(C)C)([O-])(=O)=O.[Na+]',
                                      'name': 'Nostoxanthin sulfate',
                                      'reason': 'Contains disallowed '
                                                'heteroatom: S'},
                                  {   'smiles': 'S(O[C@H]1[C@H](O)C(C(=C(C1)C)\\C=C\\C(\\C)=C\\C=C\\C(\\C)=C\\C=C\\C=C(\\C=C\\C=C(\\C=C\\C=2C([C@@H](O)[C@H](O)C(=O)C2C)(C)C)/C)/C)(C)C)([O-])(=O)=O.[Na+]',
                                      'name': '4-Ketonostoxanthin 3-sulfate',
                                      'reason': 'Contains disallowed '
                                                'heteroatom: S'},
                                  {   'smiles': 'CC(C)=CCC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\C1C(COP(O)(=O)OP(O)(O)=O)C1(C)CC\\C=C(/C)CC\\C=C(/C)CCC=C(C)C',
                                      'name': 'prephytoene diphosphate',
                                      'reason': 'No extended conjugated '
                                                'polyene system found (longest '
                                                'chain length = 1)'},
                                  {   'smiles': 'C(\\C=C\\C(OC)=O)(=C\\C=C\\C(=C\\C=C\\C=C(\\C=C\\C=C(\\C=C\\C(=O)O)/C)/C)\\C)/C',
                                      'name': 'bixin',
                                      'reason': 'Too few carbon atoms (25) to '
                                                'be a carotenoid (expected ~40 '
                                                'in the core)'}],
    'attempt': 5,
    'reasoning': 'Below is our reasoning. In the previous version the '
                 'carotenoid‐detection algorithm mainly checked that (a) only '
                 '“allowed” atoms were present, (b) that the overall carbon '
                 'count was “almost enough” (a threshold of ~35 was used), and '
                 '(c) that there was an extended conjugated (sp²) system (with '
                 '≥10 nodes). However, many false positives turned up because '
                 'molecules with “long‐enough” conjugation but with too few '
                 '(or “off‐core”) carbons were accepted (for example, '
                 'glycosylated compounds with a carotenoid‐like tail but a '
                 'total carbon count below 40) while several false negatives '
                 'were produced when the extended conjugation was missing. \n'
                 '\n'
                 'To improve the classification we now:\n'
                 '\u2003• Reject molecules that contain any atoms besides C, '
                 'H, O (and sometimes P).\n'
                 '\u2003• Require that the overall carbon count is at least 40 '
                 '(which is consistent with a tetraterpenoid backbone).\n'
                 '\u2003• Reject molecules with a molecular weight below '
                 '400\u2009Da (most carotenoids fall above this mass).\n'
                 '\u2003• Rebuild the conjugated sp² carbon network and '
                 'require that its longest connected (non‐aromatic) chain has '
                 'ten or more atoms.\n'
                 'In this way, compounds with “fake” carotenoid conjugation '
                 '(or with too few C’s for a C40 core) are rejected, while '
                 'good candidates pass these additional safeguards.\n'
                 '\n'
                 'Below is the complete Python program with one function '
                 'is_carotenoid. \n'
                 '\n'
                 'Below is the single code block in Python:\n'
                 '\n'
                 '------------------------------------------------',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 186,
    'num_false_positives': 78,
    'num_true_negatives': 142021,
    'num_false_negatives': 15,
    'num_negatives': None,
    'precision': 0.7045454545454546,
    'recall': 0.9253731343283582,
    'f1': 0.8,
    'accuracy': 0.9993464511595221,
    'negative_predictive_value': 0.9998943929707962}