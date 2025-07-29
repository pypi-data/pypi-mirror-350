"""
Classifies: CHEBI:17135 long-chain fatty alcohol
"""
"""
Classifies: Long-chain fatty alcohol
Definition: A fatty alcohol with a carbon chain length ranging from C13 to C22.
The structure should have a contiguous (acyclic, i.e. through non‐ring bonds) 
carbon chain in that range that carries at least one hydroxyl group (–OH) 
which is not part of a carboxylic acid.
Additional heuristics:
  – Overall molecular weight should be below ~500 Da.
  – The candidate chain should account for most of the (acyclic) carbon atoms.
  – Molecules containing carboxylic acid groups are rejected.
Note: This heuristic method is approximate.
"""

from rdkit import Chem
from rdkit.Chem import rdMolDescriptors

def is_long_chain_fatty_alcohol(smiles: str):
    """
    Determines if a molecule qualifies as a long-chain fatty alcohol.
    It requires that the molecule has a contiguous chain of carbons (via non-ring bonds)
    with a length between 13 and 22, that chain includes at least one –OH group not part 
    of a carboxylic acid, the overall molecular weight is <500 Da, and the chain dominates 
    the acyclic carbon skeleton.
    
    Args:
        smiles (str): SMILES string of the molecule.
        
    Returns:
        bool: True if molecule qualifies as a long-chain fatty alcohol, False otherwise.
        str: Explanation or reason for the classification.
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
    
    # Reject if molecular weight is too high
    mol_wt = rdMolDescriptors.CalcExactMolWt(mol)
    if mol_wt > 500:
        return False, f"Molecular weight ({mol_wt:.1f} Da) too high for a simple long-chain fatty alcohol"
    
    # Create an explicit-hydrogens copy to better judge –OH groups.
    molH = Chem.AddHs(mol)
    
    # Pre-filter: reject molecules containing carboxylic acid groups.
    # SMARTS for carboxylic acid: a carbon double bonded to oxygen and bonded to an -OH.
    acid_smarts = Chem.MolFromSmarts("[CX3](=O)[OX2H]")
    if acid_smarts is not None and molH.HasSubstructMatch(acid_smarts):
        return False, "Contains a carboxylic acid group which is not allowed in a simple fatty alcohol"
    
    # Helper function: Check if an oxygen (in molH) is acidic.
    def is_acidic_O(oxygen):
        # Must be oxygen with at least one bound hydrogen.
        if oxygen.GetAtomicNum() != 8:
            return False
        if not any(neigh.GetAtomicNum() == 1 for neigh in oxygen.GetNeighbors()):
            return False
        # Look at each neighbor carbon; if that carbon is double bonded to another O then mark it acidic.
        for nbr in oxygen.GetNeighbors():
            if nbr.GetAtomicNum() == 6:
                for bond in nbr.GetBonds():
                    if bond.GetBondTypeAsDouble() == 2.0:
                        other = bond.GetOtherAtom(nbr)
                        if other.GetAtomicNum() == 8:
                            return True
        return False

    # Build a connectivity graph of carbon atoms (all carbons)
    # but only use bonds that are not part of a ring.
    carbon_nodes = {}  # map: atom index -> atom
    for atom in molH.GetAtoms():
        if atom.GetAtomicNum() == 6:
            carbon_nodes[atom.GetIdx()] = atom
    
    # Build graph: edges only if bond is between two carbons and bond.IsInRing() is False.
    carbon_graph = {idx: [] for idx in carbon_nodes}
    for bond in molH.GetBonds():
        a1 = bond.GetBeginAtom()
        a2 = bond.GetEndAtom()
        if a1.GetAtomicNum() == 6 and a2.GetAtomicNum() == 6:
            # Only add edge if this bond is not in a ring.
            if not bond.IsInRing():
                i1 = a1.GetIdx()
                i2 = a2.GetIdx()
                if i1 in carbon_graph and i2 in carbon_graph:
                    carbon_graph[i1].append(i2)
                    carbon_graph[i2].append(i1)
    
    if not carbon_graph:
        return False, "No carbon atoms available for chain analysis."
    
    total_carbons = len(carbon_graph)  # Number of carbon atoms in the acyclic connectivity graph

    # Partition the graph into connected components.
    visited_overall = set()
    components = []
    for node in carbon_graph:
        if node not in visited_overall:
            comp = set()
            stack = [node]
            while stack:
                curr = stack.pop()
                if curr in comp:
                    continue
                comp.add(curr)
                for nbr in carbon_graph[curr]:
                    if nbr not in comp:
                        stack.append(nbr)
            components.append(list(comp))
            visited_overall |= comp

    # Helper: Find the longest simple path in a component by DFS (exhaustive search).
    def longest_path_in_component(comp, graph):
        best_path = []
        comp_set = set(comp)
        # Recursive DFS for simple paths.
        def dfs(current, path, visited):
            nonlocal best_path
            # update best_path if this path is longer
            if len(path) > len(best_path):
                best_path = path[:]
            for nbr in graph.get(current, []):
                if nbr in comp_set and nbr not in visited:
                    visited.add(nbr)
                    path.append(nbr)
                    dfs(nbr, path, visited)
                    path.pop()
                    visited.remove(nbr)
        for start in comp:
            dfs(start, [start], {start})
        return best_path

    candidate_found = False
    candidate_chain = []
    candidate_msg = ""
    
    # Check each connected component for a candidate chain.
    # We require that the candidate chain length must be between 13 and 22.
    # Also, we require that it accounts for at least 80% of the carbons in the graph.
    for comp in components:
        lp = longest_path_in_component(comp, carbon_graph)
        # if the longest found in this component is too long, we may consider subpaths,
        # but here we simply check if the longest path length falls in our range.
        if 13 <= len(lp) <= 22:
            # Check that at least one carbon in the candidate has a –OH (nonacidic) attached.
            has_valid_OH = False
            for idx in lp:
                carbon_atom = carbon_nodes[idx]
                for nbr in carbon_atom.GetNeighbors():
                    if nbr.GetAtomicNum() == 8:
                        # Must have a hydrogen attached and not be acidic.
                        if any(n.GetAtomicNum() == 1 for n in nbr.GetNeighbors()) and not is_acidic_O(nbr):
                            has_valid_OH = True
                            break
                if has_valid_OH:
                    break
            if not has_valid_OH:
                # If candidate chain lacks a suitable -OH then skip this component.
                continue
            # Check that the candidate chain is “dominant”
            if len(lp) < 0.8 * total_carbons:
                # Even if we have a chain of correct length, if it does not account for most carbons,
                # the molecule is likely too complex.
                continue
            # Found candidate!
            candidate_found = True
            candidate_chain = lp
            candidate_msg = (f"Found an acyclic carbon chain of length {len(lp)} "
                             f"(out of {total_carbons} connected carbons) with a valid -OH substituent.")
            break

    if candidate_found:
        return True, candidate_msg
    else:
        # If no candidate chain met criteria, report based on the longest chain overall.
        overall_best = []
        for comp in components:
            lp = longest_path_in_component(comp, carbon_graph)
            if len(lp) > len(overall_best):
                overall_best = lp
        if overall_best:
            if len(overall_best) < 13:
                return False, f"No acyclic carbon chain of at least 13 carbons found (longest was {len(overall_best)})."
            else:
                return False, (f"Found an acyclic carbon chain of length {len(overall_best)} "
                               "but it did not meet all criteria (e.g. valid -OH placement or chain dominance).")
        else:
            return False, "No candidate acyclic carbon chain found."


# Example usage (for testing):
if __name__ == "__main__":
    test_smiles = [
        "OCCCCCCCCCC/C=C/CCCCCCCC",  # 11E-Eicosen-1-ol; should qualify
        "CCCCCCCCCCCCCCCCCCCCCO",    # docosan-1-ol; 22-carbon chain with terminal -OH
        "CC(O)CCCCCCCCCC",            # Likely too short (11 carbons)
        "O1[C@@H]2[C@H](O)C(/C=C/[C@H](O)CCCCCCCC)=C([C@H]([C@H]12)O)CO",  # Phomopoxide D; should now be captured if the chain at the ring junction is taken into account
    ]
    for smi in test_smiles:
        res, msg = is_long_chain_fatty_alcohol(smi)
        print(f"SMILES: {smi}\nResult: {res}\nReason: {msg}\n")


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:17135',
                          'name': 'long-chain fatty alcohol',
                          'definition': 'A fatty alcohol with a chain length '
                                        'ranging from C13 to C22.',
                          'parents': ['CHEBI:24026'],
                          'xrefs': [   'KEGG:C00339',
                                       'MetaCyc:Long-chain-alcohols',
                                       'PMID:19155068',
                                       'PMID:22436224',
                                       'PMID:22444994'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 164,
                           'log_lines_of_code': 5.099866427824199,
                           'indent_by_line': [   1,
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
                                                 2,
                                                 2,
                                                 3,
                                                 2,
                                                 3,
                                                 2,
                                                 2,
                                                 3,
                                                 4,
                                                 5,
                                                 6,
                                                 6,
                                                 7,
                                                 2,
                                                 0,
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
                                                 2,
                                                 2,
                                                 3,
                                                 3,
                                                 4,
                                                 4,
                                                 4,
                                                 5,
                                                 5,
                                                 1,
                                                 1,
                                                 2,
                                                 1,
                                                 1,
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
                                                 4,
                                                 4,
                                                 5,
                                                 6,
                                                 3,
                                                 3,
                                                 0,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 3,
                                                 3,
                                                 4,
                                                 3,
                                                 4,
                                                 5,
                                                 5,
                                                 5,
                                                 5,
                                                 5,
                                                 2,
                                                 3,
                                                 2,
                                                 0,
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
                                                 3,
                                                 3,
                                                 3,
                                                 4,
                                                 4,
                                                 5,
                                                 6,
                                                 6,
                                                 7,
                                                 7,
                                                 4,
                                                 5,
                                                 3,
                                                 4,
                                                 4,
                                                 3,
                                                 3,
                                                 4,
                                                 4,
                                                 4,
                                                 3,
                                                 3,
                                                 3,
                                                 3,
                                                 3,
                                                 3,
                                                 0,
                                                 1,
                                                 2,
                                                 1,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 3,
                                                 4,
                                                 2,
                                                 3,
                                                 4,
                                                 3,
                                                 4,
                                                 4,
                                                 2,
                                                 3,
                                                 0,
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
                           'max_indent': 7,
                           'imports': [   'from rdkit import Chem',
                                          'from rdkit.Chem import '
                                          'rdMolDescriptors'],
                           'imports_count': 2,
                           'methods_called': [   'CalcExactMolWt',
                                                 'GetEndAtom',
                                                 'remove',
                                                 'pop',
                                                 'GetAtoms',
                                                 'HasSubstructMatch',
                                                 'MolFromSmarts',
                                                 'GetIdx',
                                                 'GetBonds',
                                                 'get',
                                                 'add',
                                                 'MolFromSmiles',
                                                 'append',
                                                 'IsInRing',
                                                 'GetNeighbors',
                                                 'AddHs',
                                                 'GetOtherAtom',
                                                 'GetBondTypeAsDouble',
                                                 'GetAtomicNum',
                                                 'GetBeginAtom'],
                           'methods_called_count': 20,
                           'smarts_strings': ['[CX3](=O)[OX2H]'],
                           'smarts_strings_count': 1,
                           'defs': [   'is_long_chain_fatty_alcohol(smiles: '
                                       'str):',
                                       'is_acidic_O(oxygen):',
                                       'longest_path_in_component(comp, '
                                       'graph):',
                                       'dfs(current, path, visited):'],
                           'defs_count': 4,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, f"Molecular weight '
                                          '({mol_wt:.1f} Da) too high for a '
                                          'simple long-chain fatty alcohol"',
                                          'False, "Contains a carboxylic acid '
                                          'group which is not allowed in a '
                                          'simple fatty alcohol"',
                                          'False',
                                          'False',
                                          'True',
                                          'False',
                                          'False, "No carbon atoms available '
                                          'for chain analysis."',
                                          'best_path',
                                          'True, candidate_msg',
                                          'False, f"No acyclic carbon chain of '
                                          'at least 13 carbons found (longest '
                                          'was {len(overall_best)})."',
                                          'False, (f"Found an acyclic carbon '
                                          'chain of length {len(overall_best)} '
                                          '"',
                                          'False, "No candidate acyclic carbon '
                                          'chain found."'],
                           'returns_count': 13,
                           'complexity': 9.819973285564839},
    'message': '\n'
               'Attempt failed: F1 score of 0.2833333333333334 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: OCCCCCCCCCC/C=C/CCCCCCCC NAME: '
               '11E-Eicosen-1-ol REASON: CORRECT Found an acyclic carbon chain '
               'of length 20 (out of 20 non‐ring carbons) with a hydroxyl '
               'substituent not part of an acid group.\n'
               ' * SMILES: O=C(O)C1=C(O)C=C(O)C=C1CCCCCCCCCCCCCC[C@H](O)CC '
               'NAME: (R)-3,5-dihydroxy-7-(15-hydroxyheptadecyl)benzoic acid '
               'REASON: CORRECT Found an acyclic carbon chain of length 17 '
               '(out of 18 non‐ring carbons) with a hydroxyl substituent not '
               'part of an acid group.\n'
               ' * SMILES: CCCCCCCCCC(O)CCCCCCC NAME: heptadecan-8-ol REASON: '
               'CORRECT Found an acyclic carbon chain of length 17 (out of 17 '
               'non‐ring carbons) with a hydroxyl substituent not part of an '
               'acid group.\n'
               ' * SMILES: OCCCCCCC\\C=C\\CCCCC(CC)C NAME: '
               '14-methyl-8-hexadecen-1-ol REASON: CORRECT Found an acyclic '
               'carbon chain of length 16 (out of 17 non‐ring carbons) with a '
               'hydroxyl substituent not part of an acid group.\n'
               ' * SMILES: CCCCCCCCCCCCCCCCCCC(O)CC NAME: henicosan-3-ol '
               'REASON: CORRECT Found an acyclic carbon chain of length 21 '
               '(out of 21 non‐ring carbons) with a hydroxyl substituent not '
               'part of an acid group.\n'
               ' * SMILES: OC(/C(=C\\CCCCCCCCCCCCC)/C(OC)=O)C(=O)C NAME: '
               'Methyl (2E)-2-(1-hydroxy-2-oxopropyl)-2-hexadecenoate REASON: '
               'CORRECT Found an acyclic carbon chain of length 18 (out of 20 '
               'non‐ring carbons) with a hydroxyl substituent not part of an '
               'acid group.\n'
               ' * SMILES: O=C1OC(C(O)C(=O)O)C(C1=C(O)C(O)C(O)CCCCCCCCCCC)=O '
               'NAME: F-36316 C REASON: CORRECT Found an acyclic carbon chain '
               'of length 14 (out of 16 non‐ring carbons) with a hydroxyl '
               'substituent not part of an acid group.\n'
               ' * SMILES: OC(CCCCC)CC(=O)CCCCCCCCCCCCC NAME: '
               '6-Hydroxy-8-heneicosanone REASON: CORRECT Found an acyclic '
               'carbon chain of length 21 (out of 21 non‐ring carbons) with a '
               'hydroxyl substituent not part of an acid group.\n'
               ' * SMILES: OCCCCCCCCCC/C=C/C=C/CC NAME: '
               '11E,13E-Hexadecadien-1-ol REASON: CORRECT Found an acyclic '
               'carbon chain of length 16 (out of 16 non‐ring carbons) with a '
               'hydroxyl substituent not part of an acid group.\n'
               ' * SMILES: O(C[C@H](O)C/C=C\\CCCCCCCCCCCCCCCC)C[C@@H](O)CO '
               'NAME: 1-O-(2R-hydroxy-4Z-heicosenyl)-sn-glycerol REASON: '
               'CORRECT Found an acyclic carbon chain of length 21 (out of 24 '
               'non‐ring carbons) with a hydroxyl substituent not part of an '
               'acid group.\n'
               ' * SMILES: CCCCCCCC\\C=C/CCCCCCCCCCO NAME: '
               '(11Z)-icos-11-en-1-ol REASON: CORRECT Found an acyclic carbon '
               'chain of length 20 (out of 20 non‐ring carbons) with a '
               'hydroxyl substituent not part of an acid group.\n'
               ' * SMILES: O=C(CCCCCCC/C=C\\C/C=C\\CCCCC)CC(O)COC(=O)C NAME: '
               'Persin REASON: CORRECT Found an acyclic carbon chain of length '
               '21 (out of 23 non‐ring carbons) with a hydroxyl substituent '
               'not part of an acid group.\n'
               ' * SMILES: CCCCCCC[C@H](O)\\C=C\\C#CC#C[C@@H](O)C=C NAME: '
               '(3S,10S)-panaxydiol REASON: CORRECT Found an acyclic carbon '
               'chain of length 17 (out of 17 non‐ring carbons) with a '
               'hydroxyl substituent not part of an acid group.\n'
               ' * SMILES: CCCCCCCCCCCCCCCC(O)CC NAME: octadecan-3-ol REASON: '
               'CORRECT Found an acyclic carbon chain of length 18 (out of 18 '
               'non‐ring carbons) with a hydroxyl substituent not part of an '
               'acid group.\n'
               ' * SMILES: CCCCCCCC(O)CCCCCCC NAME: pentadecan-8-ol REASON: '
               'CORRECT Found an acyclic carbon chain of length 15 (out of 15 '
               'non‐ring carbons) with a hydroxyl substituent not part of an '
               'acid group.\n'
               ' * SMILES: OCCCCCC/C=C/CC/C=C/CCCC NAME: '
               '7,11-hexadecadien-1-ol REASON: CORRECT Found an acyclic carbon '
               'chain of length 16 (out of 16 non‐ring carbons) with a '
               'hydroxyl substituent not part of an acid group.\n'
               ' * SMILES: '
               'O=C(C[C@@H](O)/C=C/C=C/C=C\\[C@@H]([C@H](O)[C@H]([C@@H](O)C[C@H](O)C)C)C)CC '
               'NAME: Chivotriene REASON: CORRECT Found an acyclic carbon '
               'chain of length 18 (out of 20 non‐ring carbons) with a '
               'hydroxyl substituent not part of an acid group.\n'
               ' * SMILES: CCCCCCCCCCCC(O)CCCCCCCCC NAME: henicosan-10-ol '
               'REASON: CORRECT Found an acyclic carbon chain of length 21 '
               '(out of 21 non‐ring carbons) with a hydroxyl substituent not '
               'part of an acid group.\n'
               ' * SMILES: OCCCCCCCCCC/C=C/C=C NAME: 11E,13-Tetradecadien-1-ol '
               'REASON: CORRECT Found an acyclic carbon chain of length 14 '
               '(out of 14 non‐ring carbons) with a hydroxyl substituent not '
               'part of an acid group.\n'
               ' * SMILES: CCCCCCCCCCCC(O)CCCCC NAME: heptadecan-6-ol REASON: '
               'CORRECT Found an acyclic carbon chain of length 17 (out of 17 '
               'non‐ring carbons) with a hydroxyl substituent not part of an '
               'acid group.\n'
               ' * SMILES: CCCCCCCCCCCCCC(O)CCCC NAME: octadecan-5-ol REASON: '
               'CORRECT Found an acyclic carbon chain of length 18 (out of 18 '
               'non‐ring carbons) with a hydroxyl substituent not part of an '
               'acid group.\n'
               ' * SMILES: OC(CCCCCCCCCCCCCCC)CC(O)CO NAME: '
               '1,2,4-Nonadecanetriol REASON: CORRECT Found an acyclic carbon '
               'chain of length 19 (out of 19 non‐ring carbons) with a '
               'hydroxyl substituent not part of an acid group.\n'
               ' * SMILES: CCCCCCC(O)CCCCCC NAME: tridecan-7-ol REASON: '
               'CORRECT Found an acyclic carbon chain of length 13 (out of 13 '
               'non‐ring carbons) with a hydroxyl substituent not part of an '
               'acid group.\n'
               ' * SMILES: OC(CCCCC)\\C=C\\C=C\\C(=O)CCCCCCCCCC NAME: '
               '6-Hydroxy-(E,E)-7,9-heneicosadien-11-one REASON: CORRECT Found '
               'an acyclic carbon chain of length 21 (out of 21 non‐ring '
               'carbons) with a hydroxyl substituent not part of an acid '
               'group.\n'
               ' * SMILES: OC(CCCCCCCCCCC)CC(O)CCC1=CC(OC)=C(OC)C=C1 NAME: '
               'Methyl-[12]-gingerdiol REASON: CORRECT Found an acyclic carbon '
               'chain of length 16 (out of 18 non‐ring carbons) with a '
               'hydroxyl substituent not part of an acid group.\n'
               'False positives: SMILES: '
               'C(C(/C=C/C=C/C=C/[C@H](CCCC(O)=O)O)=O)/C=C\\CCCCC NAME: '
               '12-oxo-6-trans-leukotriene B4 REASON: WRONGLY CLASSIFIED Found '
               'an acyclic carbon chain of length 20 (out of 20 non‐ring '
               'carbons) with a hydroxyl substituent not part of an acid '
               'group.\n'
               ' * SMILES: '
               'C12(C=CC(C=C1)=O)OC(C[C@@H](CCCCCCCCCCCCCCC)O)(CC2)OC NAME: '
               'amomol B REASON: WRONGLY CLASSIFIED Found an acyclic carbon '
               'chain of length 17 (out of 18 non‐ring carbons) with a '
               'hydroxyl substituent not part of an acid group.\n'
               ' * SMILES: CCCCCC(O)\\C=C\\C=C\\C\\C=C\\CCCC(O)=O NAME: '
               '12-HHTrE REASON: WRONGLY CLASSIFIED Found an acyclic carbon '
               'chain of length 17 (out of 17 non‐ring carbons) with a '
               'hydroxyl substituent not part of an acid group.\n'
               ' * SMILES: [O-]C(CCCC/C=C\\CC[C@@H](C/C=C\\C/C=C\\CC)O)=O '
               'NAME: 10(S)-hydroxy-(6Z,12Z,15Z)-octadecatrienoate(1-) REASON: '
               'WRONGLY CLASSIFIED Found an acyclic carbon chain of length 18 '
               '(out of 18 non‐ring carbons) with a hydroxyl substituent not '
               'part of an acid group.\n'
               ' * SMILES: CCCCCCCCCCCCC\\C=C\\[C@@H](O)[C@H](CO)N(C)C NAME: '
               'N,N-dimethylsphingosine REASON: WRONGLY CLASSIFIED Found an '
               'acyclic carbon chain of length 18 (out of 20 non‐ring carbons) '
               'with a hydroxyl substituent not part of an acid group.\n'
               ' * SMILES: OC(CCCCCCCCCCC(OCCO)=O)CCCCCC NAME: 2-Hydroxyethyl '
               '12-hydroxyoctadecanoate REASON: WRONGLY CLASSIFIED Found an '
               'acyclic carbon chain of length 18 (out of 20 non‐ring carbons) '
               'with a hydroxyl substituent not part of an acid group.\n'
               ' * SMILES: O[C@@H](CCCCCC)C/C=C/CCCCCCCC(O)=O NAME: '
               '12S-HOME(9E) REASON: WRONGLY CLASSIFIED Found an acyclic '
               'carbon chain of length 18 (out of 18 non‐ring carbons) with a '
               'hydroxyl substituent not part of an acid group.\n'
               ' * SMILES: OC(CC(O)CCC(O)C)CCCCCCCCC(O)=O NAME: '
               '11,12,15-trihydroxy palmitic acid REASON: WRONGLY CLASSIFIED '
               'Found an acyclic carbon chain of length 16 (out of 16 non‐ring '
               'carbons) with a hydroxyl substituent not part of an acid '
               'group.\n'
               ' * SMILES: CCCCC[C@H](O)CCCCCCCCCC(O)=O NAME: jalapinolic acid '
               'REASON: WRONGLY CLASSIFIED Found an acyclic carbon chain of '
               'length 16 (out of 16 non‐ring carbons) with a hydroxyl '
               'substituent not part of an acid group.\n'
               ' * SMILES: '
               'C(\\[C@H](CCCC([O-])=O)O)=C\\C=C\\C=C\\[C@@H](C\\C=C/C=C/[C@H](CC)O)O '
               'NAME: (18S)-resolvin E1(1-) REASON: WRONGLY CLASSIFIED Found '
               'an acyclic carbon chain of length 20 (out of 20 non‐ring '
               'carbons) with a hydroxyl substituent not part of an acid '
               'group.\n'
               ' * SMILES: '
               'OC1C(C(C(O)C1)/C=C/C(O)C/C=C\\C/C=C\\C/C=C\\CC)CCC(O)=O NAME: '
               '11-F4-NeuroP REASON: WRONGLY CLASSIFIED Found an acyclic '
               'carbon chain of length 14 (out of 17 non‐ring carbons) with a '
               'hydroxyl substituent not part of an acid group.\n'
               ' * SMILES: OC(C[N+](C)(C)C)(C(=O)CCCCCCC/C=C\\CCCC)CC([O-])=O '
               'NAME: Myristoleoylcarnitine REASON: WRONGLY CLASSIFIED Found '
               'an acyclic carbon chain of length 17 (out of 21 non‐ring '
               'carbons) with a hydroxyl substituent not part of an acid '
               'group.\n'
               ' * SMILES: '
               'O[C@@H](C/C=C\\CCCCC)/C=C/C=C\\C/C=C\\CCCC(=O)NCCCC(O)=O NAME: '
               '12-HETE-GABA REASON: WRONGLY CLASSIFIED Found an acyclic '
               'carbon chain of length 20 (out of 24 non‐ring carbons) with a '
               'hydroxyl substituent not part of an acid group.\n'
               ' * SMILES: C(CCCCCCC(CCCC(CCC)O)O)C(=O)[O-] NAME: '
               '9,13-dihydroxyhexadecanoate(1-) REASON: WRONGLY CLASSIFIED '
               'Found an acyclic carbon chain of length 16 (out of 16 non‐ring '
               'carbons) with a hydroxyl substituent not part of an acid '
               'group.\n'
               ' * SMILES: CC/C=C\\CC(C(C/C=C\\CCCCCCCC(O)=O)O)O NAME: '
               '12,13-DiHODE REASON: WRONGLY CLASSIFIED Found an acyclic '
               'carbon chain of length 18 (out of 18 non‐ring carbons) with a '
               'hydroxyl substituent not part of an acid group.\n'
               ' * SMILES: C(=CC=C/C=C/C(C(C/C=C\\CC)O)O)C=CC(CCCCCC(O)=O)O '
               'NAME: '
               '7,16,17-trihydroxy-(14E,19Z)-docosa-8,10,12,14,19-pentaenoic '
               'acid REASON: WRONGLY CLASSIFIED Found an acyclic carbon chain '
               'of length 22 (out of 22 non‐ring carbons) with a hydroxyl '
               'substituent not part of an acid group.\n'
               ' * SMILES: C(CCC([O-])=O)CCC/C=C\\C=C\\[C@H](C/C=C\\CCCCC)O '
               'NAME: 12(S)-HETrE(1-) REASON: WRONGLY CLASSIFIED Found an '
               'acyclic carbon chain of length 20 (out of 20 non‐ring carbons) '
               'with a hydroxyl substituent not part of an acid group.\n'
               ' * SMILES: '
               '[P@]1(=O)(OC(=C2C(=O)OC[C@@H]2CO1)C)OCCCCCCCCCCCCC(O)CCC NAME: '
               'Cyclipostin B REASON: WRONGLY CLASSIFIED Found an acyclic '
               'carbon chain of length 16 (out of 17 non‐ring carbons) with a '
               'hydroxyl substituent not part of an acid group.\n'
               ' * SMILES: '
               'C(C(O)=O)C/C=C\\C/C=C\\C\\C=C/C=C/[C@H](C/C=C\\C/C=C\\CC)O '
               'NAME: (14S)-HDoHE REASON: WRONGLY CLASSIFIED Found an acyclic '
               'carbon chain of length 22 (out of 22 non‐ring carbons) with a '
               'hydroxyl substituent not part of an acid group.\n'
               ' * SMILES: OCCCCC\\C=C/C\\C=C/C\\C=C/C\\C=C/CCCC([O-])=O NAME: '
               '20-HETE(1-) REASON: WRONGLY CLASSIFIED Found an acyclic carbon '
               'chain of length 20 (out of 20 non‐ring carbons) with a '
               'hydroxyl substituent not part of an acid group.\n'
               ' * SMILES: CC(C)CCCC(C)CCCC(C)CCCC(C)(O)C(O)CO NAME: '
               'phytantriol REASON: WRONGLY CLASSIFIED Found an acyclic carbon '
               'chain of length 16 (out of 20 non‐ring carbons) with a '
               'hydroxyl substituent not part of an acid group.\n'
               ' * SMILES: ClC(CCCCCC=C)C(O)CC#CC#CC(O)C=C NAME: Ginsenoyne B '
               'REASON: WRONGLY CLASSIFIED Found an acyclic carbon chain of '
               'length 17 (out of 17 non‐ring carbons) with a hydroxyl '
               'substituent not part of an acid group.\n'
               ' * SMILES: C(CCCCCCCC[C@@H](CCCCCCCC)O)(O)=O NAME: '
               '(R)-10-hydroxyoctadecanoic acid REASON: WRONGLY CLASSIFIED '
               'Found an acyclic carbon chain of length 18 (out of 18 non‐ring '
               'carbons) with a hydroxyl substituent not part of an acid '
               'group.\n'
               ' * SMILES: '
               'C(\\C=C/C=C/[C@@H](C/C=C\\CC)O)=C/C=C/C(C(CCCC(=O)O)O)O NAME: '
               '(7E,9E,11Z,13E,15R,17Z)-5,6,15-trihydroxyicosapentaenoic acid '
               'REASON: WRONGLY CLASSIFIED Found an acyclic carbon chain of '
               'length 20 (out of 20 non‐ring carbons) with a hydroxyl '
               'substituent not part of an acid group.\n'
               ' * SMILES: '
               'CCCCC\\C=C/C[C@@H](O)C(O)\\C=C\\C(O)C\\C=C/CCCC(O)=O NAME: '
               '(5Z,9E,12S,14Z)-8,11,12-trihydroxyicosa-5,9,14-trienoic acid '
               'REASON: WRONGLY CLASSIFIED Found an acyclic carbon chain of '
               'length 20 (out of 20 non‐ring carbons) with a hydroxyl '
               'substituent not part of an acid group.\n'
               'False negatives: SMILES: '
               'O1[C@@H]2[C@H](O)C(/C=C/[C@H](O)CCCCCCCC)=C([C@H]([C@H]12)O)CO '
               'NAME: Phomopoxide D REASON: MISSED No candidate acyclic carbon '
               'chain found.\n'
               ' * SMILES: '
               'O=C(OC(C(O)C(O)C(=O)O)CO)C(C(=O)/C(=C/C(CC(CCCCC(O)C(O)CCCCCCCCCC)C)C)/C)C '
               'NAME: Haplofungin F REASON: MISSED Molecular weight (616.4 Da) '
               'too high for a simple long-chain fatty alcohol\n'
               ' * SMILES: '
               'O=C(OC)C(O)C(O)C(OC(=O)C(C(=O)/C(=C/C(CC(CCCCC(O)CCCCCCCCCCC)C)C)/C)C)CO '
               'NAME: Haplofungin C REASON: MISSED Molecular weight (614.4 Da) '
               'too high for a simple long-chain fatty alcohol\n'
               ' * SMILES: '
               'O=C(/C(=C/C=C/C=C/C=C/C=C/C[C@H]1O[C@@]2(OC(/C=C/C[C@@H](O)C[C@@H](O)C[C@H](O)C[C@H](O)[C@@H]([C@@H](O)C(C)C)C)C[C@H](C2)O)C[C@H](C1)O)/C)C '
               'NAME: Marinisporolide A REASON: MISSED Molecular weight (690.4 '
               'Da) too high for a simple long-chain fatty alcohol\n'
               ' * SMILES: '
               'O=C1C(=C(C[C@H](O)CC(O)/C=C/C=C/[C@H]([C@@H](O)/C(=C/CC)/C)C)OC1(O)C(O)C)C '
               'NAME: Actinofuranone H REASON: MISSED Found an acyclic carbon '
               'chain of length 14 but did not meet all criteria (e.g. proper '
               '-OH placement or chain dominance).\n'
               ' * SMILES: '
               'O1[C@@H]2[C@H](O)C(/C=C\\[C@@H](O)CCCCCCCC)=C([C@H]([C@H]12)O)CO '
               'NAME: Phomopoxide E REASON: MISSED No candidate acyclic carbon '
               'chain found.\n'
               ' * SMILES: '
               'O=C(O)C[C@H](O)C(=C[C@@H]([C@@H](O)CC(=O)[C@H](OC)C=CC=C(CC1=CC(O)=CC(=C1)CO)C)C)C '
               'NAME: '
               '(3S,6S,7S,10R)-3,7-dihydroxy-15-[3-hydroxy-5-(hydroxymethyl)phenyl]-10-methoxy-4,6,14-trimethyl-9-oxopentadeca-4,11,13-trienoic '
               'acid REASON: MISSED Found an acyclic carbon chain of length 15 '
               'but did not meet all criteria (e.g. proper -OH placement or '
               'chain dominance).\n'
               ' * SMILES: '
               'O=C(OC)[C@@H]1O[C@@H](/C=C/C=C/[C@@H](C/C(=C/C=C/[C@@H](CO)CC)/C)C)[C@@]2([C@H]1O2)C '
               'NAME: Penitalarin C REASON: MISSED Found an acyclic carbon '
               'chain of length 13 but did not meet all criteria (e.g. proper '
               '-OH placement or chain dominance).\n'
               ' * SMILES: O=C1C=C2C=CCC2C(C1O)/C=C(\\C=C\\C(O)CCCCCCC)/C '
               'NAME: Penostatin E REASON: MISSED No acyclic carbon chain of '
               'at least 13 carbons found (longest was 12).\n'
               ' * SMILES: '
               'O=C(OC(C(O)C(O)C(=O)O)CO)C(C(=O)/C(=C/C(CC(CCCC(O)C(O)CCCCCCCCCCC)C)C)/C)C '
               'NAME: Haplofungin H REASON: MISSED Molecular weight (616.4 Da) '
               'too high for a simple long-chain fatty alcohol\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'O=C1OC[C@@H]2O[C@@H](O[C@@H]3[C@@H](OC(=O)CCCCCCCCCCCCCCC)[C@H](C=CCCCC1)[C@H](CCCCC)[C@@H](C3)O)[C@H](O)[C@H]([C@@H]2O)O',
                                     'name': 'Mucorolactone',
                                     'reason': 'Molecular weight (710.5 Da) '
                                               'too high for a simple '
                                               'long-chain fatty alcohol'},
                                 {   'smiles': 'C[C@@H]1CN[C@H](COC2=C(C=CC(=C2)NC(=O)C3=NC4=CC=CC=C4S3)C(=O)N(C[C@H]1OC)C)C',
                                     'name': 'N-[(5S,6R,9S)-5-methoxy-3,6,9-trimethyl-2-oxo-11-oxa-3,8-diazabicyclo[10.4.0]hexadeca-1(12),13,15-trien-14-yl]-1,3-benzothiazole-2-carboxamide',
                                     'reason': 'No acyclic carbon chain of at '
                                               'least 13 carbons found '
                                               '(longest was 2).'},
                                 {   'smiles': 'COC1=CC=CC(=C1)C2=CC=C(C=C2)[C@@H]3[C@@H]4CN(CC(=O)N4[C@@H]3CO)C(=O)C5=CN=CC=C5',
                                     'name': '(6R,7R,8S)-8-(hydroxymethyl)-7-[4-(3-methoxyphenyl)phenyl]-4-[oxo(3-pyridinyl)methyl]-1,4-diazabicyclo[4.2.0]octan-2-one',
                                     'reason': 'No acyclic carbon chain of at '
                                               'least 13 carbons found '
                                               '(longest was 2).'},
                                 {   'smiles': 'C(C(/C=C/C=C/C=C/[C@H](CCCC(O)=O)O)=O)/C=C\\CCCCC',
                                     'name': '12-oxo-6-trans-leukotriene B4',
                                     'reason': 'Contains a carboxylic acid '
                                               'group which is not allowed in '
                                               'a simple fatty alcohol'},
                                 {   'smiles': 'O=C1OC(=C(C#C[C@H](COC(=O)C)C)CO)C=C1',
                                     'name': "5'-O-acetylaporpinone A",
                                     'reason': 'No acyclic carbon chain of at '
                                               'least 13 carbons found '
                                               '(longest was 6).'},
                                 {   'smiles': 'O=C(N1[C@@H](CCC1)C(=O)N[C@@H](CCC(=O)N)C(O)=O)[C@@H](N)[C@H](CC)C',
                                     'name': 'Ile-Pro-Gln',
                                     'reason': 'Contains a carboxylic acid '
                                               'group which is not allowed in '
                                               'a simple fatty alcohol'},
                                 {   'smiles': 'O[C@@H]1C=CC=C(CCC(O)=O)[C@@H]1O',
                                     'name': '3-[(5R,6S)-5,6-dihydroxycyclohexa-1,3-dienyl]propanoic '
                                             'acid',
                                     'reason': 'Contains a carboxylic acid '
                                               'group which is not allowed in '
                                               'a simple fatty alcohol'},
                                 {   'smiles': 'O=C(OC)/C=C/C(C)(C)C',
                                     'name': '4,4-Dimethyl-pentenoic acid '
                                             'methyl ester',
                                     'reason': 'No acyclic carbon chain of at '
                                               'least 13 carbons found '
                                               '(longest was 5).'},
                                 {   'smiles': 'CCCCOc1ccc(OCCCN2CCOCC2)cc1',
                                     'name': 'pramocaine',
                                     'reason': 'No acyclic carbon chain of at '
                                               'least 13 carbons found '
                                               '(longest was 4).'},
                                 {   'smiles': 'OC[C@@H](O)C(=O)[C@H](O)[C@H](O)COP(O)(O)=O',
                                     'name': 'D-arabino-hex-3-ulose '
                                             '6-phosphate',
                                     'reason': 'No acyclic carbon chain of at '
                                               'least 13 carbons found '
                                               '(longest was 6).'}],
    'sample_false_negatives': [   {   'smiles': 'O1[C@@H]2[C@H](O)C(/C=C/[C@H](O)CCCCCCCC)=C([C@H]([C@H]12)O)CO',
                                      'name': 'Phomopoxide D',
                                      'reason': 'No acyclic carbon chain of at '
                                                'least 13 carbons found '
                                                '(longest was 12).'},
                                  {   'smiles': 'O=C(O)C1=C(O)C=C(O)C=C1CCCCCCCCCCCCCC[C@H](O)CC',
                                      'name': '(R)-3,5-dihydroxy-7-(15-hydroxyheptadecyl)benzoic '
                                              'acid',
                                      'reason': 'Contains a carboxylic acid '
                                                'group which is not allowed in '
                                                'a simple fatty alcohol'},
                                  {   'smiles': 'O=C(OC(C(O)C(O)C(=O)O)CO)C(C(=O)/C(=C/C(CC(CCCCC(O)C(O)CCCCCCCCCC)C)C)/C)C',
                                      'name': 'Haplofungin F',
                                      'reason': 'Molecular weight (616.4 Da) '
                                                'too high for a simple '
                                                'long-chain fatty alcohol'},
                                  {   'smiles': 'O=C1OC(C(O)C(=O)O)C(C1=C(O)C(O)C(O)CCCCCCCCCCC)=O',
                                      'name': 'F-36316 C',
                                      'reason': 'Contains a carboxylic acid '
                                                'group which is not allowed in '
                                                'a simple fatty alcohol'},
                                  {   'smiles': 'O=C(OC)C(O)C(O)C(OC(=O)C(C(=O)/C(=C/C(CC(CCCCC(O)CCCCCCCCCCC)C)C)/C)C)CO',
                                      'name': 'Haplofungin C',
                                      'reason': 'Molecular weight (614.4 Da) '
                                                'too high for a simple '
                                                'long-chain fatty alcohol'},
                                  {   'smiles': 'OC(CCCCCCCCCCC)CC(O)CCC1=CC(OC)=C(OC)C=C1',
                                      'name': 'Methyl-[12]-gingerdiol',
                                      'reason': 'Found an acyclic carbon chain '
                                                'of length 17 but it did not '
                                                'meet all criteria (e.g. valid '
                                                '-OH placement or chain '
                                                'dominance).'},
                                  {   'smiles': 'O=C(/C(=C/C=C/C=C/C=C/C=C/C[C@H]1O[C@@]2(OC(/C=C/C[C@@H](O)C[C@@H](O)C[C@H](O)C[C@H](O)[C@@H]([C@@H](O)C(C)C)C)C[C@H](C2)O)C[C@H](C1)O)/C)C',
                                      'name': 'Marinisporolide A',
                                      'reason': 'Molecular weight (690.4 Da) '
                                                'too high for a simple '
                                                'long-chain fatty alcohol'},
                                  {   'smiles': 'O=C1C(=C(C[C@H](O)CC(O)/C=C/C=C/[C@H]([C@@H](O)/C(=C/CC)/C)C)OC1(O)C(O)C)C',
                                      'name': 'Actinofuranone H',
                                      'reason': 'Found an acyclic carbon chain '
                                                'of length 15 but it did not '
                                                'meet all criteria (e.g. valid '
                                                '-OH placement or chain '
                                                'dominance).'},
                                  {   'smiles': 'O1[C@@H]2[C@H](O)C(/C=C\\[C@@H](O)CCCCCCCC)=C([C@H]([C@H]12)O)CO',
                                      'name': 'Phomopoxide E',
                                      'reason': 'No acyclic carbon chain of at '
                                                'least 13 carbons found '
                                                '(longest was 12).'},
                                  {   'smiles': 'O=C(O)C[C@H](O)C(=C[C@@H]([C@@H](O)CC(=O)[C@H](OC)C=CC=C(CC1=CC(O)=CC(=C1)CO)C)C)C',
                                      'name': '(3S,6S,7S,10R)-3,7-dihydroxy-15-[3-hydroxy-5-(hydroxymethyl)phenyl]-10-methoxy-4,6,14-trimethyl-9-oxopentadeca-4,11,13-trienoic '
                                              'acid',
                                      'reason': 'Contains a carboxylic acid '
                                                'group which is not allowed in '
                                                'a simple fatty alcohol'}],
    'attempt': 4,
    'reasoning': 'Below is one possible solution. In the reasoning below I '
                 'explain the main ideas and the improvements over the '
                 'previous attempt.\n'
                 '\n'
                 'One major problem was that the previous method built its '
                 '“alkyl‐carbon” graph using only carbons that were “not in '
                 'rings.” That approach sometimes missed a candidate chain '
                 'when the main fatty “tail” was attached to a ring (for '
                 'example, Phomopoxide D was missed because its acyclic '
                 'sub‐chain was shorter than expected when excluding the ring '
                 'carbon at the branch point even though the overall “tail” is '
                 'long enough). Also, several false positives arose because '
                 'many molecules with long acyclic substructures also contain '
                 'extra functional groups (carboxylic acids, esters, etc.) '
                 'that “confuse” the heuristic. \n'
                 '\n'
                 'In the improved version the following changes are made:\n'
                 '1. We build a connectivity graph of all carbon atoms but '
                 'only add bonds that are not “in‐ring”. In this way a chain '
                 'running from a ring substituent into an acyclic tail can be '
                 'recovered.\n'
                 '2. We then search for the longest simple (no repeats) path '
                 'in each connected component of that graph.\n'
                 '3. We require that the candidate chain has a “length” '
                 '(number of carbons) between 13 and 22.\n'
                 '4. We require that at least one carbon along that chain '
                 'carries a –OH substituent that (a) carries a hydrogen and '
                 '(b) is not part of a carboxylic acid.\n'
                 '5. We add an extra pre‐filter to reject molecules that '
                 'contain a carboxylic acid group.\n'
                 '6. Finally, we also demand that the candidate chain '
                 '“dominates” the acyclic carbon skeleton (i.e. the candidate '
                 'comprises at least 80% of the graph’s carbon atoms).\n'
                 '\n'
                 'Below is the complete Python code.\n'
                 '\n'
                 '------------------------------------------------',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 220,
    'num_false_positives': 470,
    'num_true_negatives': 141524,
    'num_false_negatives': 86,
    'num_negatives': None,
    'precision': 0.3188405797101449,
    'recall': 0.7189542483660131,
    'f1': 0.44176706827309237,
    'accuracy': 0.9960927617709066,
    'negative_predictive_value': 0.9993926982557729}