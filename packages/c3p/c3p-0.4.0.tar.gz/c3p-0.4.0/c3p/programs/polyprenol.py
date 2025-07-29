"""
Classifies: CHEBI:26199 polyprenol
"""
#!/usr/bin/env python
"""
Classifies: polyprenol – any member of the class of prenols possessing the general formula
H-[CH2C(Me)=CHCH2]nOH in which n>=2 (i.e. more than one isoprene-like unit).

This improved classifier requires that:
  • The molecule is built exclusively from C, H and O.
  • The molecule is acyclic (a linear isoprenoid backbone) 
    (note: molecules with rings are not accepted even if they contain a long chain).
  • No carbonyl (C=O) groups are present.
  • It contains at least one terminal hydroxyl (-OH) group (on a primary carbon).
  • The longest carbon-only chain is sufficiently long (at least 10 C atoms).
  • The number of isoprene-like units (as judged via SMARTS patterns) is roughly what is expected
    from the length of that carbon chain. (A tolerance of ±1 unit is allowed.)
    
We define three SMARTS fragments for isoprene-like units:
    • alpha unit (terminal at the –OH side): [OH]CC([CH3])=C
    • internal unit: [CH2]C([CH3])=C[CH2]
    • omega unit (terminal at the other end): C([CH3])=C[CH2]O
"""
from rdkit import Chem
from rdkit.Chem import rdMolDescriptors

def is_polyprenol(smiles: str):
    """
    Determines if a molecule is a polyprenol based on its SMILES string.
    
    A polyprenol should:
       • Be composed solely of C, H and O.
       • Be acyclic.
       • Have no carbonyl (C=O) groups.
       • Possess at least one terminal hydroxyl (-OH) group on a primary carbon.
       • Possess a long carbon chain (at least 10 carbons in the longest chain).
       • Possess a number of isoprene-like repeating units that agrees with the chain length.
       
    Args:
        smiles (str): SMILES string of the molecule.
    
    Returns:
        bool: True if classified as a polyprenol, False otherwise.
        str: Explanation for the decision.
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # 1. Check that molecule is solely built from C, H and O.
    allowed_atomic_nums = {1, 6, 8}
    for atom in mol.GetAtoms():
        if atom.GetAtomicNum() not in allowed_atomic_nums:
            return False, f"Molecule contains atom {atom.GetSymbol()} not allowed (only C, H, O are permitted)."
    
    # 2. Ensure molecule is acyclic.
    if mol.GetRingInfo().NumRings() > 0:
        return False, "Molecule contains rings; expected a linear isoprenoid chain."
    
    # 3. Exclude molecules with carbonyl groups (e.g. acids, esters)
    carbonyl_pat = Chem.MolFromSmarts("[CX3]=[OX1]")
    if mol.HasSubstructMatch(carbonyl_pat):
        return False, "Molecule contains carbonyl (C=O) groups which are not expected for a polyprenol."
    
    # 4. Check for at least one hydroxyl (-OH) group.
    hydroxyl_pat = Chem.MolFromSmarts("[OX2H]")
    if not mol.HasSubstructMatch(hydroxyl_pat):
        return False, "No hydroxyl (-OH) group found."

    # 5. Look for a terminal -OH on a primary carbon.
    terminal_oh_found = False
    for atom in mol.GetAtoms():
        if atom.GetAtomicNum() == 8:  # Oxygen
            # Must have at least one hydrogen -- using GetTotalNumHs.
            if atom.GetTotalNumHs() >= 1:
                # Check that oxygen is attached to exactly one heavy (non-hydrogen) atom.
                heavy_neighbors = [nbr for nbr in atom.GetNeighbors() if nbr.GetAtomicNum() > 1]
                if len(heavy_neighbors) == 1:
                    neigh = heavy_neighbors[0]
                    if neigh.GetAtomicNum() == 6:
                        # Check that this carbon is primary: it must have only one carbon neighbor.
                        carbon_neighbors = [nbr for nbr in neigh.GetNeighbors() if nbr.GetAtomicNum() == 6]
                        if len(carbon_neighbors) == 1:
                            terminal_oh_found = True
                            break
    if not terminal_oh_found:
        return False, "No terminal hydroxyl (-OH) group on a primary carbon found."
    
    # 6. Check that there are a sufficient number of carbon atoms.
    carbon_atoms = [atom for atom in mol.GetAtoms() if atom.GetAtomicNum() == 6]
    n_carbons = len(carbon_atoms)
    if n_carbons < 10:
        return False, f"Too few carbons ({n_carbons}) for a polyprenol structure."
    
    # 7. Count isoprene-like repeating fragments via SMARTS.
    # Note: These SMARTS are heuristic.
    pattern_alpha = Chem.MolFromSmarts("[OH]CC([CH3])=C")
    pattern_internal = Chem.MolFromSmarts("[CH2]C([CH3])=C[CH2]")
    pattern_omega = Chem.MolFromSmarts("C([CH3])=C[CH2]O")
    
    matches_alpha = mol.GetSubstructMatches(pattern_alpha)
    matches_internal = mol.GetSubstructMatches(pattern_internal)
    matches_omega = mol.GetSubstructMatches(pattern_omega)
    total_units = len(matches_alpha) + len(matches_internal) + len(matches_omega)
    if total_units < 2:
        return False, f"Only {total_units} isoprene-like unit(s) detected (need at least 2)."
    
    # 8. Identify the longest carbon-only chain.
    # Build an undirected graph over carbon atoms only.
    carbon_indices = [atom.GetIdx() for atom in mol.GetAtoms() if atom.GetAtomicNum() == 6]
    # Create an adjacency dictionary: key = carbon atom index, value = list of neighbor carbon indices.
    graph = {idx: [] for idx in carbon_indices}
    for idx in carbon_indices:
        atom = mol.GetAtomWithIdx(idx)
        for nbr in atom.GetNeighbors():
            if nbr.GetAtomicNum() == 6:
                graph[idx].append(nbr.GetIdx())
                
    # In a tree (acyclic) the longest chain (diameter) can be found by doing DFS from each terminal node.
    def dfs(start, visited):
        max_length = 1
        for nbr in graph[start]:
            if nbr not in visited:
                length = 1 + dfs(nbr, visited | {nbr})
                if length > max_length:
                    max_length = length
        return max_length

    # Terminal nodes in this carbon graph (degree 1).
    terminal_nodes = [idx for idx, nbrs in graph.items() if len(nbrs) == 1]
    longest_chain = 0
    for node in terminal_nodes:
        chain_length = dfs(node, {node})
        if chain_length > longest_chain:
            longest_chain = chain_length

    if longest_chain < 10:
        return False, f"Longest carbon chain has only {longest_chain} carbons; too short for a polyprenol."
    
    # 9. Estimate expected number of isoprene units.
    # In an ideal polyprenol of formula H-[CH2C(Me)=CHCH2]nOH, the chain has about n repeating 4-carbon units plus 1 extra carbon.
    expected_units = round((longest_chain - 1) / 4)
    # Allow a tolerance of ±1 unit.
    if abs(total_units - expected_units) > 1:
        return False, (f"Mismatch between repeating fragment count ({total_units}) and "
                       f"expected isoprene units (~{expected_units}) based on a {longest_chain}-carbon chain.")
    
    return True, (f"Polyprenol detected with {total_units} isoprene-like unit(s) "
                  f"and a {longest_chain}-carbon backbone (expected ~{expected_units} units), "
                  "with a terminal -OH group.")

# Example usage (you can remove or modify this block when using the function in another project):
if __name__ == "__main__":
    examples = {
        "(E,E,E)-geranylgeraniol": "CC(C)=CCC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CO",
        "(2E,6E,10E)-omega-hydroxyfarnesol": "C\\C(CO)=C/CC\\C(C)=C\\CC\\C(C)=C\\CO",
        "Bionectin F": "OC(CCC=C(C)C)(CCCC(O)(CCCC(O)(CCCC(O)(CCCC(O)(CCCC(O)(CCCC(O)(CCC/C(=C/CC/C(=C/CO)/C)/C)C)C)C)C)C)C)C",
        "Dolichol-19": "OCC[C@H](CC/C=C(\\CC/C=C(\\CC/C=C(\\CC/C=C(\\CC/C=C(\\CC/C=C(\\CC/C=C(\\CC/C=C(\\CC/C=C(\\CC/C=C(\\CC/C=C(\\CC/C=C(\\CC\\C=C(\\CC/C=C(/CCC=C(C)C)\\C)/C)/C)/C)/C)/C)/C)/C)/C)/C)/C)/C)/C",
        "Glisoprenin E": "OC(C(O)CC/C(=C/CO)/C)(CC/C=C(/CC/C=C(/CCCC(O)(CCCC(O)(CCCC(O)(CCCC(O)(CCC(O)C(O)(C)C)C)C)C)C)\\C)\\C)C",
        "geraniol": "CC(C)=CCC\\C(C)=C\\CO",
        "Dolichol-18": "OCC[C@H](CC/C=C(\\CC/C=C(\\CC/C=C(\\CC/C=C(\\CC/C=C(\\CC/C=C(\\CC/C=C(\\CC/C=C(\\CC/C=C(\\CC/C=C(\\CC/C=C(\\CC/C=C(\\CC\\C=C(\\CC/C=C(/CCC=C(C)C)\\C)/C)/C)/C)/C)/C)/C)/C)/C)/C)/C)/C)/C)",
        "Glisoprenin A": "OC(CCC=C(C)C)(CCCC(O)(CCCC(O)(CCCC(O)(CCCC(=CCCC(=CCCC(=CCCC(=CCO)C)C)C)C)C)C)C)C",
        "(2-trans,6-trans)-farnesol": "CC(C)=CCC\\C(C)=C\\CC\\C(C)=C\\CO",
        "farnesol": "[H]C(CO)=C(C)CCC([H])=C(C)CCC=C(C)C",
        "SCH 66878": "OC(C(O)CC/C(=C/CC/C(=C/CC/C(=C/CO)/C)/C)/C)(CCCC(O)(CCCC(O)(CCCC(O)(CCCC(O)(CCCC(O)(CCCC(O)(CCCC(O)(CCCC(O)(CCCC(O)(CCC=C(C)C)C)C)C)C)C)C)C)C)C)C",
        "all-trans-octaprenol": "C(/C=C(/CC\\C=C(\\CC/C=C(\\C)/CCC=C(C)C)/C)\\C)C\\C(\\C)=C\\CC\\C(\\C)=C\\CC/C(/C)=C/CC\\C(=C\\CO)\\C",
        "ditrans,polycis-undecaprenol": "C(/C=C(\\CC/C=C(\\CC/C=C(\\CC/C=C(\\CC/C=C(\\CC/C=C(\\CC/C=C(\\CC/C=C(/CC/C=C(/CCC=C(C)C)\\C)\\C)/C)/C)/C)/C)/C)/C)/C)/C)O",
        "Gymnoprenol A10": "OC(C(O)CO)(CC/C=C(/CC/C=C(/CCCC(O)(CCCC(O)(CCCC(O)(CCCC(O)(CCCC(O)(CCCC(O)(CCC=C(C)C)C)C)C)C)C)C)\\C)\\C)C",
        "(2-cis,6-trans)-farnesol": "CC(C)=CCC\\C(C)=C\\CC\\C(C)=C/CO",
        "Glisoprenin D": "OC(CCC(O)C(O)(C)C)(CCCC(O)(CCCC(O)(CCCC(O)(CCC/C(=C/CC/C(=C/CC/C(=C/CC/C(=C/CO)/C)/C)/C)/C)C)C)C)C",
        "all-trans-undecaprenol": "CC(C)=CCC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CO",
        "nerol": "C(=C\\CO)(\\CCC=C(C)C)/C",
        "(2-cis,6-cis)-farnesol": "CC(C)=CCC\\C(C)=C/CC\\C(C)=C/CO",
        "(2E,6E,10Z,14Z,18Z,22E)-3,7,11,15,19,23,27,31,35-Nonamethylhexatriaconta-2,6,10,14,18,22-hexaen-1-ol": "OC\\C=C(\\CC\\C=C(\\CC/C=C(\\CC/C=C(\\CC/C=C(\\CC\\C=C(\\CCCC(CCCC(CCCC(C)C)C)C)/C)/C)/C)/C)/C)/C",
        "geranylgeraniol": "CC(C)=CCCC(C)=CCCC(C)=CCCC(C)=CCO",
        "(2-trans,6-cis)-farnesol": "CC(C)=CCC\\C(C)=C/CC\\C(C)=C\\CO",
        "Glisoprenin F": "OC(CCC(O)C(O)(C)C)(CCCC(O)(CCCC(O)(CCCC(O)(CCCC(O)(CCC/C(=C/CC/C(=C/CC/C(=C/CO)/C)/C)/C)C)C)C)C)C",
        "all-trans-hexaprenol": "C(/C=C(/CCC=C(C)C)\\C)C\\C(\\C)=C\\CC\\C(\\C)=C\\CC/C(/C)=C/CC\\C(=C\\CO)\\C",
        "SCH 60057": "OC(CCC=C(C)C)(CCCC(O)(CCCC(O)(CCCC(O)(CCCC(O)(CCC/C(=C/CC/C(=C/CC/C(=C/CO)/C)/C)/C)C)C)C)C)C",
        "solanesol": "CC(C)=CCC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CO"
    }
    
    for name, s in examples.items():
        result, explanation = is_polyprenol(s)
        print(f"{name}:\n  Result: {result}\n  Explanation: {explanation}\n")


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:26199',
                          'name': 'polyprenol',
                          'definition': 'Any member of the class of  prenols '
                                        'possessing the general formula '
                                        'H-[CH2C(Me)=CHCH2]nOH in which the '
                                        'carbon skeleton is composed of more '
                                        'than one isoprene units.',
                          'parents': ['CHEBI:26244'],
                          'xrefs': ['KEGG:C06081'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 137,
                           'log_lines_of_code': 4.919980925828125,
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
                                                 2,
                                                 1,
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
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 3,
                                                 3,
                                                 4,
                                                 4,
                                                 4,
                                                 5,
                                                 5,
                                                 6,
                                                 6,
                                                 6,
                                                 7,
                                                 7,
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
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 3,
                                                 4,
                                                 4,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 3,
                                                 4,
                                                 4,
                                                 5,
                                                 2,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 3,
                                                 0,
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
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 2],
                           'max_indent': 7,
                           'imports': [   'from rdkit import Chem',
                                          'from rdkit.Chem import '
                                          'rdMolDescriptors'],
                           'imports_count': 2,
                           'methods_called': [   'MolFromSmiles',
                                                 'MolFromSmarts',
                                                 'HasSubstructMatch',
                                                 'GetNeighbors',
                                                 'append',
                                                 'GetIdx',
                                                 'GetRingInfo',
                                                 'GetAtoms',
                                                 'GetAtomWithIdx',
                                                 'items',
                                                 'NumRings',
                                                 'GetAtomicNum',
                                                 'GetSymbol',
                                                 'GetTotalNumHs',
                                                 'GetSubstructMatches'],
                           'methods_called_count': 15,
                           'smarts_strings': [   '[OH]CC([CH3])=C',
                                                 'C([CH3])=C[CH2]O',
                                                 '[CX3]=[OX1]',
                                                 '[CH2]C([CH3])=C[CH2]',
                                                 '[OX2H]'],
                           'smarts_strings_count': 5,
                           'defs': [   'is_polyprenol(smiles: str):',
                                       'dfs(start, visited):'],
                           'defs_count': 2,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, f"Molecule contains atom '
                                          '{atom.GetSymbol()} not allowed '
                                          '(only C, H, O are permitted)."',
                                          'False, "Molecule contains rings; '
                                          'expected a linear isoprenoid '
                                          'chain."',
                                          'False, "Molecule contains carbonyl '
                                          '(C=O) groups which are not expected '
                                          'for a polyprenol."',
                                          'False, "No hydroxyl (-OH) group '
                                          'found."',
                                          'False, "No terminal hydroxyl (-OH) '
                                          'group on a primary carbon found."',
                                          'False, f"Too few carbons '
                                          '({n_carbons}) for a polyprenol '
                                          'structure."',
                                          'False, f"Only {total_units} '
                                          'isoprene-like unit(s) detected '
                                          '(need at least 2)."',
                                          'max_length',
                                          'False, f"Longest carbon chain has '
                                          'only {longest_chain} carbons; too '
                                          'short for a polyprenol."',
                                          'False, (f"Mismatch between '
                                          'repeating fragment count '
                                          '({total_units}) and "',
                                          'True, (f"Polyprenol detected with '
                                          '{total_units} isoprene-like unit(s) '
                                          '"'],
                           'returns_count': 12,
                           'complexity': 8.183996185165626},
    'message': '\n'
               'Attempt failed: F1 score of 0.4482758620689656 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: '
               'CC(C)=CCC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CO NAME: '
               '(E,E,E)-geranylgeraniol REASON: CORRECT Polyprenol detected '
               'with 4 isoprene-like unit(s) and a terminal -OH group\n'
               ' * SMILES: C\\C(CO)=C/CC\\C(C)=C\\CC\\C(C)=C\\CO NAME: '
               '(2E,6E,10E)-omega-hydroxyfarnesol REASON: CORRECT Polyprenol '
               'detected with 5 isoprene-like unit(s) and a terminal -OH '
               'group\n'
               ' * SMILES: '
               'OC(CCC=C(C)C)(CCCC(O)(CCCC(O)(CCCC(O)(CCCC(O)(CCCC(O)(CCCC(O)(CCC/C(=C/CC/C(=C/CO)/C)/C)C)C)C)C)C)C)C '
               'NAME: Bionectin F REASON: CORRECT Polyprenol detected with 3 '
               'isoprene-like unit(s) and a terminal -OH group\n'
               ' * SMILES: '
               'OCC[C@H](CC/C=C(\\CC/C=C(\\CC/C=C(\\CC/C=C(\\CC/C=C(\\CC/C=C(\\CC/C=C(\\CC/C=C(\\CC/C=C(\\CC/C=C(\\CC/C=C(\\CC/C=C(\\CC/C=C(\\CC/C=C(\\CC/C=C(\\CC\\C=C(\\CC/C=C(/CCC=C(C)C)\\C)/C)/C)/C)/C)/C)/C)/C)/C)/C)/C)/C)/C)/C)/C)/C)/C)C '
               'NAME: Dolichol-19 REASON: CORRECT Polyprenol detected with 17 '
               'isoprene-like unit(s) and a terminal -OH group\n'
               ' * SMILES: '
               'OC(C(O)CC/C(=C/CO)/C)(CC/C=C(/CC/C=C(/CCCC(O)(CCCC(O)(CCCC(O)(CCCC(O)(CCC(O)C(O)(C)C)C)C)C)C)\\C)\\C)C '
               'NAME: Glisoprenin E REASON: CORRECT Polyprenol detected with 4 '
               'isoprene-like unit(s) and a terminal -OH group\n'
               ' * SMILES: CC(C)=CCC\\C(C)=C\\CO NAME: geraniol REASON: '
               'CORRECT Polyprenol detected with 2 isoprene-like unit(s) and a '
               'terminal -OH group\n'
               ' * SMILES: '
               'OCC[C@H](CC/C=C(\\CC/C=C(\\CC/C=C(\\CC/C=C(\\CC/C=C(\\CC/C=C(\\CC/C=C(\\CC/C=C(\\CC/C=C(\\CC/C=C(\\CC/C=C(\\CC/C=C(\\CC/C=C(\\CC/C=C(\\CC\\C=C(\\CC/C=C(/CCC=C(C)C)\\C)/C)/C)/C)/C)/C)/C)/C)/C)/C)/C)/C)/C)/C)/C)/C)C '
               'NAME: Dolichol-18 REASON: CORRECT Polyprenol detected with 16 '
               'isoprene-like unit(s) and a terminal -OH group\n'
               ' * SMILES: '
               'OC(CCC=C(C)C)(CCCC(O)(CCCC(O)(CCCC(O)(CCCC(=CCCC(=CCCC(=CCCC(=CCO)C)C)C)C)C)C)C)C '
               'NAME: Glisoprenin A REASON: CORRECT Polyprenol detected with 5 '
               'isoprene-like unit(s) and a terminal -OH group\n'
               ' * SMILES: CC(C)=CCC\\C(C)=C\\CC\\C(C)=C\\CO NAME: '
               '(2-trans,6-trans)-farnesol REASON: CORRECT Polyprenol detected '
               'with 3 isoprene-like unit(s) and a terminal -OH group\n'
               ' * SMILES: [H]C(CO)=C(C)CCC([H])=C(C)CCC=C(C)C NAME: farnesol '
               'REASON: CORRECT Polyprenol detected with 3 isoprene-like '
               'unit(s) and a terminal -OH group\n'
               ' * SMILES: '
               'OC(C(O)CC/C(=C/CC/C(=C/CC/C(=C/CO)/C)/C)/C)(CCCC(O)(CCCC(O)(CCCC(O)(CCCC(O)(CCCC(O)(CCCC(O)(CCCC(O)(CCCC(O)(CCCC(O)(CCCC(O)(CCC=C(C)C)C)C)C)C)C)C)C)C)C)C)C '
               'NAME: SCH 66878 REASON: CORRECT Polyprenol detected with 4 '
               'isoprene-like unit(s) and a terminal -OH group\n'
               ' * SMILES: '
               'C(/C=C(/CC\\C=C(\\CC/C=C(\\C)/CCC=C(C)C)/C)\\C)C\\C(\\C)=C\\CC\\C(\\C)=C\\CC/C(/C)=C/CC\\C(=C\\CO)\\C '
               'NAME: all-trans-octaprenol REASON: CORRECT Polyprenol detected '
               'with 8 isoprene-like unit(s) and a terminal -OH group\n'
               ' * SMILES: '
               'C(/C=C(\\CC/C=C(\\CC/C=C(\\CC/C=C(\\CC/C=C(\\CC/C=C(\\CC/C=C(\\CC/C=C(\\CC/C=C(/CC/C=C(/CCC=C(C)C)\\C)\\C)/C)/C)/C)/C)/C)/C)/C)/C)O '
               'NAME: ditrans,polycis-undecaprenol REASON: CORRECT Polyprenol '
               'detected with 11 isoprene-like unit(s) and a terminal -OH '
               'group\n'
               ' * SMILES: '
               'OC(C(O)CO)(CC/C=C(/CC/C=C(/CCCC(O)(CCCC(O)(CCCC(O)(CCCC(O)(CCCC(O)(CCCC(O)(CCC=C(C)C)C)C)C)C)C)C)\\C)\\C)C '
               'NAME: Gymnoprenol A10 REASON: CORRECT Polyprenol detected with '
               '2 isoprene-like unit(s) and a terminal -OH group\n'
               ' * SMILES: CC(C)=CCC\\C(C)=C\\CC\\C(C)=C/CO NAME: '
               '(2-cis,6-trans)-farnesol REASON: CORRECT Polyprenol detected '
               'with 3 isoprene-like unit(s) and a terminal -OH group\n'
               ' * SMILES: '
               'OC(CCC(O)C(O)(C)C)(CCCC(O)(CCCC(O)(CCCC(O)(CCC/C(=C/CC/C(=C/CC/C(=C/CC/C(=C/CO)/C)/C)/C)/C)C)C)C)C '
               'NAME: Glisoprenin D REASON: CORRECT Polyprenol detected with 5 '
               'isoprene-like unit(s) and a terminal -OH group\n'
               ' * SMILES: '
               'CC(C)=CCC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CO '
               'NAME: all-trans-undecaprenol REASON: CORRECT Polyprenol '
               'detected with 11 isoprene-like unit(s) and a terminal -OH '
               'group\n'
               ' * SMILES: C(=C\\CO)(\\CCC=C(C)C)/C NAME: nerol REASON: '
               'CORRECT Polyprenol detected with 2 isoprene-like unit(s) and a '
               'terminal -OH group\n'
               ' * SMILES: CC(C)=CCC\\C(C)=C/CC\\C(C)=C/CO NAME: '
               '(2-cis,6-cis)-farnesol REASON: CORRECT Polyprenol detected '
               'with 3 isoprene-like unit(s) and a terminal -OH group\n'
               ' * SMILES: '
               'OC\\C=C(\\CC\\C=C(\\CC/C=C(\\CC/C=C(\\CC/C=C(\\CC\\C=C(\\CCCC(CCCC(CCCC(C)C)C)C)/C)/C)/C)/C)/C)/C '
               'NAME: '
               '(2E,6E,10Z,14Z,18Z,22E)-3,7,11,15,19,23,27,31,35-Nonamethylhexatriaconta-2,6,10,14,18,22-hexaen-1-ol '
               'REASON: CORRECT Polyprenol detected with 7 isoprene-like '
               'unit(s) and a terminal -OH group\n'
               ' * SMILES: CC(C)=CCCC(C)=CCCC(C)=CCCC(C)=CCO NAME: '
               'geranylgeraniol REASON: CORRECT Polyprenol detected with 4 '
               'isoprene-like unit(s) and a terminal -OH group\n'
               ' * SMILES: CC(C)=CCC\\C(C)=C/CC\\C(C)=C\\CO NAME: '
               '(2-trans,6-cis)-farnesol REASON: CORRECT Polyprenol detected '
               'with 3 isoprene-like unit(s) and a terminal -OH group\n'
               ' * SMILES: '
               'OC(CCC(O)C(O)(C)C)(CCCC(O)(CCCC(O)(CCCC(O)(CCCC(O)(CCC/C(=C/CC/C(=C/CC/C(=C/CO)/C)/C)/C)C)C)C)C)C '
               'NAME: Glisoprenin F REASON: CORRECT Polyprenol detected with 4 '
               'isoprene-like unit(s) and a terminal -OH group\n'
               ' * SMILES: '
               'C(/C=C(/CCC=C(C)C)\\C)C\\C(\\C)=C\\CC\\C(\\C)=C\\CC/C(/C)=C/CC\\C(=C\\CO)\\C '
               'NAME: all-trans-hexaprenol REASON: CORRECT Polyprenol detected '
               'with 6 isoprene-like unit(s) and a terminal -OH group\n'
               ' * SMILES: '
               'OC(CCC=C(C)C)(CCCC(O)(CCCC(O)(CCCC(O)(CCCC(O)(CCC/C(=C/CC/C(=C/CC/C(=C/CO)/C)/C)/C)C)C)C)C)C '
               'NAME: SCH 60057 REASON: CORRECT Polyprenol detected with 4 '
               'isoprene-like unit(s) and a terminal -OH group\n'
               'False positives: SMILES: '
               'O=C(O)C(O)C(O)CC(O)/C=C/CC(O)/C=C/CC(O)/C(=C/C(C(O)/C(=C/C(=C\\C(CC(CC)C)C)/CO)/C)C)/C '
               'NAME: Arthrinic acid REASON: WRONGLY CLASSIFIED Polyprenol '
               'detected with 2 isoprene-like unit(s) and a terminal -OH '
               'group\n'
               ' * SMILES: OC/C=C(\\CCC[C@@H](CCC[C@@H](CCCC(C)C)C)C)/C NAME: '
               'cis-Phytol REASON: WRONGLY CLASSIFIED Polyprenol detected with '
               '2 isoprene-like unit(s) and a terminal -OH group\n'
               ' * SMILES: '
               'O=C(O)[C@H](OC/C=C(/CC/C=C(/CC/C=C(/CCC=C(C)C)\\C)\\C)\\C)[C@@H](C(=O)O)CC(=O)O '
               'NAME: Microporenic acid A REASON: WRONGLY CLASSIFIED '
               'Polyprenol detected with 4 isoprene-like unit(s) and a '
               'terminal -OH group\n'
               ' * SMILES: O[C@H](C(=C)CO)CC/C(=C/CC/C(=C/CC/C(=C/CO)/C)/C)/C '
               'NAME: Boletinin D REASON: WRONGLY CLASSIFIED Polyprenol '
               'detected with 4 isoprene-like unit(s) and a terminal -OH '
               'group\n'
               ' * SMILES: C\\C(CO)=C/CC\\C(C)=C\\CO NAME: '
               '(6E)-8-hydroxygeraniol REASON: WRONGLY CLASSIFIED Polyprenol '
               'detected with 4 isoprene-like unit(s) and a terminal -OH '
               'group\n'
               ' * SMILES: CC(C)=CCC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\C(O)=O '
               'NAME: (2E,6E,10E)-geranylgeranic acid REASON: WRONGLY '
               'CLASSIFIED Polyprenol detected with 2 isoprene-like unit(s) '
               'and a terminal -OH group\n'
               ' * SMILES: '
               'O=C(O)C(C(O)/C(=C/C(C(O)/C=C/C(C(O)/C=C/C(C(O)/C(=C/C(CO)CC(CC)C)/C)C)C)C)/C)C '
               'NAME: Cubensic acid REASON: WRONGLY CLASSIFIED Polyprenol '
               'detected with 2 isoprene-like unit(s) and a terminal -OH '
               'group\n'
               ' * SMILES: O[C@H](C(=C)CC/C=C(/CO)\\C)CC/C(=C/CC/C(=C/CO)/C)/C '
               'NAME: Boletinin C REASON: WRONGLY CLASSIFIED Polyprenol '
               'detected with 5 isoprene-like unit(s) and a terminal -OH '
               'group\n'
               ' * SMILES: '
               'O=C(O)[C@H](OC/C=C(/CC/C=C(/CC/C=C(/CC[C@H](O)C(O)(C)C)\\C)\\C)\\C)[C@@H](C(=O)O)CC(=O)O '
               'NAME: Microporenic acid G REASON: WRONGLY CLASSIFIED '
               'Polyprenol detected with 4 isoprene-like unit(s) and a '
               'terminal -OH group\n'
               ' * SMILES: OC(C(O)CC(O)/C(=C/CC/C(=C\\CO)/C)/C)(C)C NAME: '
               'Agripilol D REASON: WRONGLY CLASSIFIED Polyprenol detected '
               'with 3 isoprene-like unit(s) and a terminal -OH group\n'
               ' * SMILES: OCCC(CC/C=C(/CC/C=C(/CCC=C(C)C)\\C)\\C)C NAME: '
               'Geranylcitronellol REASON: WRONGLY CLASSIFIED Polyprenol '
               'detected with 2 isoprene-like unit(s) and a terminal -OH '
               'group\n'
               ' * SMILES: '
               'C\\C(CO)=C/CC\\C(C)=C\\C=C\\C(C)=C\\C=C\\C(C)=C\\C=C\\C=C(C)\\C=C\\C=C(C)\\C=C\\C=C(/C)CC\\C=C(/C)CO '
               'NAME: lycophyll REASON: WRONGLY CLASSIFIED Polyprenol detected '
               'with 4 isoprene-like unit(s) and a terminal -OH group\n'
               ' * SMILES: '
               'O=C(OC/C(=C/CC/C(=C/CC/C(=C/CC/C(=C/CO)/C)/C)/C)/C)/C=C/C(=O)O '
               'NAME: Boletinin E REASON: WRONGLY CLASSIFIED Polyprenol '
               'detected with 5 isoprene-like unit(s) and a terminal -OH '
               'group\n'
               ' * SMILES: '
               'O(C\\C=C(\\CC\\C=C(\\CC\\C=C(\\CC/C=C(\\C)/C=O)/C)/C)/C)C(=O)/C(/C)=C/O '
               'NAME: Cavipetin C REASON: WRONGLY CLASSIFIED Polyprenol '
               'detected with 4 isoprene-like unit(s) and a terminal -OH '
               'group\n'
               ' * SMILES: OCC/C=C(/CC/C=C(/CCCO)\\C)\\C NAME: '
               '(3E,7E)-4,8-dimethyl-undecane-3,7-diene-1,11-diol REASON: '
               'WRONGLY CLASSIFIED Polyprenol detected with 2 isoprene-like '
               'unit(s) and a terminal -OH group\n'
               ' * SMILES: '
               'O=C(O)[C@H](OC/C=C(/CC/C=C(/CCC=C(C)C)\\C)\\C)[C@@H](C(=O)O)CC(=O)O '
               'NAME: Microporenic acid E REASON: WRONGLY CLASSIFIED '
               'Polyprenol detected with 3 isoprene-like unit(s) and a '
               'terminal -OH group\n'
               ' * SMILES: '
               'C(=C(\\CC/C=C(/CC/C=C(/CCC(C)=C)\\C(O)=O)\\CO)/C)\\CO NAME: '
               'smaditerpenic acid C REASON: WRONGLY CLASSIFIED Polyprenol '
               'detected with 2 isoprene-like unit(s) and a terminal -OH '
               'group\n'
               ' * SMILES: '
               'C\\C(CC\\C=C(/C)C(=O)OC\\C=C(/C)CC\\C=C(/C)C(O)=O)=C/CO NAME: '
               '(2E,6E)-8-{[(2E,6E)-8-hydroxy-2,6-dimethylocta-2,6-dienoyl]oxy}-2,6-dimethylocta-2,6-dienoic '
               'acid REASON: WRONGLY CLASSIFIED Polyprenol detected with 5 '
               'isoprene-like unit(s) and a terminal -OH group\n'
               ' * SMILES: '
               'O=C(O)[C@H](OC/C=C(/CC/C=C(/CC/C=C(/CCC=C(C)C)\\C)\\C)\\C)[C@@H](C(=O)O)CC(=O)OC '
               'NAME: Microporenic acid B REASON: WRONGLY CLASSIFIED '
               'Polyprenol detected with 4 isoprene-like unit(s) and a '
               'terminal -OH group\n'
               ' * SMILES: '
               'C(=C\\C=C\\C(=C\\C=C\\C=C(\\C=C\\C=C(\\C=C\\C=C(\\CCC(C/C=C(/CO)\\C)C(C)=C)/C)/C)/C)\\C)(/C=C/C=C(/CCC(C/C=C(/CO)\\C)C(C)=C)\\C)\\C '
               'NAME: flavuxanthin REASON: WRONGLY CLASSIFIED Polyprenol '
               'detected with 4 isoprene-like unit(s) and a terminal -OH '
               'group\n'
               ' * SMILES: OC(CC/C(/C)=C/CO)C(CO)=C NAME: '
               '6-Methyl-2-methylene-6-octene-1,3,8-triol REASON: WRONGLY '
               'CLASSIFIED Polyprenol detected with 2 isoprene-like unit(s) '
               'and a terminal -OH group\n'
               ' * SMILES: '
               'C(=C(\\CC/C=C(/CC/C=C(/CCC=C(C)C)\\C(O)=O)\\COC(=O)C)/C)\\CO '
               'NAME: Smaditerpenic acid E REASON: WRONGLY CLASSIFIED '
               'Polyprenol detected with 2 isoprene-like unit(s) and a '
               'terminal -OH group\n'
               ' * SMILES: OC/C(=C(/CCC=C(C)C)\\C)/C NAME: 2-Methylgeraniol '
               'REASON: WRONGLY CLASSIFIED Polyprenol detected with 4 '
               'isoprene-like unit(s) and a terminal -OH group\n'
               ' * SMILES: '
               'O=C(OC/C(=C/CC[C@](O)([C@@H](O)CC/C(=C/CC/C=C(/CC[C@H](O)[C@@](O)(CC/C=C(/CO)\\C)C)\\C)/C)C)/C)C '
               'NAME: Concentricol C REASON: WRONGLY CLASSIFIED Polyprenol '
               'detected with 5 isoprene-like unit(s) and a terminal -OH '
               'group\n'
               ' * SMILES: '
               'O=C/C(=C/[C@H]([C@@H](O)/C=C/[C@H]([C@@H](O)/C(=C/[C@H]([C@@H](O)/C(=C/[C@H](CO)C[C@@H](CC)C)/C)C)/C)C)C)/C '
               'NAME: Pestalpolyol I REASON: WRONGLY CLASSIFIED Polyprenol '
               'detected with 2 isoprene-like unit(s) and a terminal -OH '
               'group\n'
               'False negatives: SMILES: '
               'O1C(CCC1C(O)(C)C)(CCCC(O)(CCCC(O)(CCCC(O)(CCC/C(=C/CC/C(=C/CC/C(=C/CC/C(=C/CO)/C)/C)/C)/C)C)C)C)C '
               'NAME: Glisoprenin B REASON: MISSED Molecule contains rings; '
               'expected a linear isoprenoid chain\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'C1=CC=C2C(=C1)C(=O)C3=CC=CC=C3C2(CC4=CC(=NC=C4)F)CC5=CC(=NC=C5)F',
                                     'name': '10,10-bis[(2-fluoro-4-pyridinyl)methyl]-9-anthracenone',
                                     'reason': 'Molecule contains atom N not '
                                               'allowed (only C, H, O are '
                                               'permitted).'},
                                 {   'smiles': 'C[C@@H](C1=CC=CC=C1)NC(=O)[C@@H]2[C@H]([C@@H]3CN4C(=CC=C(C4=O)C5=CC=CC=C5F)[C@H]2N3C)CO',
                                     'name': 'LSM-10936',
                                     'reason': 'Molecule contains atom N not '
                                               'allowed (only C, H, O are '
                                               'permitted).'},
                                 {   'smiles': '[H]C(=CC(=O)C(O)=O)C(CC(O)=O)C(O)=O',
                                     'name': '5-oxopent-3-ene-1,2,5-tricarboxylic '
                                             'acid',
                                     'reason': 'Molecule contains carbonyl '
                                               '(C=O) groups which are not '
                                               'expected for a polyprenol.'},
                                 {   'smiles': 'S1N(C2=CC=C(C=C2)C(OCC)=O)C(=O)C=C1',
                                     'name': 'ethyl '
                                             '4-(3-oxo-2,3-dihydroisothiazol-2-yl)benzoate',
                                     'reason': 'Molecule contains atom S not '
                                               'allowed (only C, H, O are '
                                               'permitted).'},
                                 {   'smiles': 'COc1cc(O)c2c(c1)oc1c(O)cccc1c2=O',
                                     'name': 'mesuaxanthone A',
                                     'reason': 'Molecule contains rings; '
                                               'expected a linear isoprenoid '
                                               'chain.'},
                                 {   'smiles': 'O([C@@H]1[C@H](O)[C@@H](O[C@@H]([C@H]1O)CO[C@H]2O[C@@H]([C@@H](O)[C@H](O)[C@@H]2O[C@@H]3O[C@@H]([C@@H](O)[C@H](O)[C@H]3NC(=O)C)CO)CO[C@@H]4O[C@@H]([C@@H](O)[C@H](O)[C@H]4NC(=O)C)CO)O[C@H]5[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]5CO)O[C@H]6[C@H](O)[C@@H](NC(=O)C)C(O[C@@H]6CO)O)[C@H]7O[C@@H]([C@@H](O[C@@H]8O[C@@H]([C@@H](O)[C@H](O)[C@H]8NC(=O)C)CO)[C@H](O)[C@@H]7O[C@@H]9O[C@@H]([C@@H](O[C@@H]%10O[C@@H]([C@H](O)[C@H](O)[C@H]%10O)CO)[C@H](O)[C@H]9NC(=O)C)CO)CO',
                                     'name': 'N-[(3R,4R,5S,6R)-5-[(2S,3R,4R,5S,6R)-3-Acetamido-5-[(2S,3S,4S,5R,6R)-6-[[(2S,3S,4S,5S,6R)-3-[(2R,3R,4R,5S,6R)-3-acetamido-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-6-[[(2R,3R,4R,5S,6R)-3-acetamido-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxymethyl]-4,5-dihydroxyoxan-2-yl]oxymethyl]-4-[(2R,3S,4S,5S,6R)-5-[(2R,3R,4R,5S,6R)-3-acetamido-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-3-[(2S,3R,4R,5S,6R)-3-acetamido-4-hydroxy-6-(hydroxymethyl)-5-[(2S,3R,4S,5R,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-3,5-dihydroxyoxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-2,4-dihydroxy-6-(hydroxymethyl)oxan-3-yl]acetamide',
                                     'reason': 'Molecule contains atom N not '
                                               'allowed (only C, H, O are '
                                               'permitted).'},
                                 {   'smiles': 'CCCCCCCC\\C=C/CCCCCCCC(=O)OC[C@H](COP([O-])(=O)OC[C@H]([NH3+])C([O-])=O)OC(=O)CCC\\C=C/C\\C=C/C\\C=C/C\\C=C/CCCCC',
                                     'name': '1-oleoyl-2-arachidonoyl-sn-glycero-3-phospho-L-serine(1-)',
                                     'reason': 'Molecule contains atom P not '
                                               'allowed (only C, H, O are '
                                               'permitted).'},
                                 {   'smiles': 'OC(=Cc1ccccc1)C([O-])=O',
                                     'name': 'enol-phenylpyruvate',
                                     'reason': 'Molecule contains rings; '
                                               'expected a linear isoprenoid '
                                               'chain.'},
                                 {   'smiles': '[H][C@]1(CC[C@]2(C)[C@@H](O)CCC(=C)[C@@]12[H])[C@@H](O)C(C)C',
                                     'name': '(1R,3aS,4S,7aR)-1-((S)-1-hydroxy-2-methylpropyl)-3a-methyl-7-methyleneoctahydro-1H-inden-4-ol',
                                     'reason': 'Molecule contains rings; '
                                               'expected a linear isoprenoid '
                                               'chain.'},
                                 {   'smiles': 'O1C(C(O)C(O)C(O)C1CO)C=2C(=O)C=3C(O)=C(C4OC(C(O)C(O)C4O)CO)C(O)=CC3OC2C5=CC=C(OC)C=C5',
                                     'name': "3,6-Diglucopyranosyl-5,7-dihydroxy-4'-methoxyflavone",
                                     'reason': 'Molecule contains rings; '
                                               'expected a linear isoprenoid '
                                               'chain.'}],
    'sample_false_negatives': [   {   'smiles': 'C\\C(CO)=C/CC\\C(C)=C\\CC\\C(C)=C\\CO',
                                      'name': '(2E,6E,10E)-omega-hydroxyfarnesol',
                                      'reason': 'Mismatch between repeating '
                                                'fragment count (5) and '
                                                'expected isoprene units (~3) '
                                                'based on a 12-carbon chain.'},
                                  {   'smiles': 'OC(CCC=C(C)C)(CCCC(O)(CCCC(O)(CCCC(O)(CCCC(O)(CCCC(O)(CCCC(O)(CCC/C(=C/CC/C(=C/CO)/C)/C)C)C)C)C)C)C)C',
                                      'name': 'Bionectin F',
                                      'reason': 'Mismatch between repeating '
                                                'fragment count (3) and '
                                                'expected isoprene units (~10) '
                                                'based on a 40-carbon chain.'},
                                  {   'smiles': 'OCC[C@H](CC/C=C(\\CC/C=C(\\CC/C=C(\\CC/C=C(\\CC/C=C(\\CC/C=C(\\CC/C=C(\\CC/C=C(\\CC/C=C(\\CC/C=C(\\CC/C=C(\\CC/C=C(\\CC/C=C(\\CC/C=C(\\CC/C=C(\\CC\\C=C(\\CC/C=C(/CCC=C(C)C)\\C)/C)/C)/C)/C)/C)/C)/C)/C)/C)/C)/C)/C)/C)/C)/C)/C)C',
                                      'name': 'Dolichol-19',
                                      'reason': 'Mismatch between repeating '
                                                'fragment count (17) and '
                                                'expected isoprene units (~19) '
                                                'based on a 76-carbon chain.'},
                                  {   'smiles': 'OC(C(O)CC/C(=C/CO)/C)(CC/C=C(/CC/C=C(/CCCC(O)(CCCC(O)(CCCC(O)(CCCC(O)(CCC(O)C(O)(C)C)C)C)C)C)\\C)\\C)C',
                                      'name': 'Glisoprenin E',
                                      'reason': 'Mismatch between repeating '
                                                'fragment count (4) and '
                                                'expected isoprene units (~9) '
                                                'based on a 36-carbon chain.'},
                                  {   'smiles': 'CC(C)=CCC\\C(C)=C\\CO',
                                      'name': 'geraniol',
                                      'reason': 'Longest carbon chain has only '
                                                '8 carbons; too short for a '
                                                'polyprenol.'},
                                  {   'smiles': 'OCC[C@H](CC/C=C(\\CC/C=C(\\CC/C=C(\\CC/C=C(\\CC/C=C(\\CC/C=C(\\CC/C=C(\\CC/C=C(\\CC/C=C(\\CC/C=C(\\CC/C=C(\\CC/C=C(\\CC/C=C(\\CC/C=C(\\CC\\C=C(\\CC/C=C(/CCC=C(C)C)\\C)/C)/C)/C)/C)/C)/C)/C)/C)/C)/C)/C)/C)/C)/C)/C)C',
                                      'name': 'Dolichol-18',
                                      'reason': 'Mismatch between repeating '
                                                'fragment count (16) and '
                                                'expected isoprene units (~18) '
                                                'based on a 72-carbon chain.'},
                                  {   'smiles': 'OC(CCC=C(C)C)(CCCC(O)(CCCC(O)(CCCC(O)(CCCC(=CCCC(=CCCC(=CCCC(=CCO)C)C)C)C)C)C)C)C',
                                      'name': 'Glisoprenin A',
                                      'reason': 'Mismatch between repeating '
                                                'fragment count (5) and '
                                                'expected isoprene units (~9) '
                                                'based on a 36-carbon chain.'},
                                  {   'smiles': 'OC(C(O)CC/C(=C/CC/C(=C/CC/C(=C/CO)/C)/C)/C)(CCCC(O)(CCCC(O)(CCCC(O)(CCCC(O)(CCCC(O)(CCCC(O)(CCCC(O)(CCCC(O)(CCCC(O)(CCCC(O)(CCC=C(C)C)C)C)C)C)C)C)C)C)C)C)C',
                                      'name': 'SCH 66878',
                                      'reason': 'Mismatch between repeating '
                                                'fragment count (4) and '
                                                'expected isoprene units (~15) '
                                                'based on a 60-carbon chain.'},
                                  {   'smiles': 'O1C(CCC1C(O)(C)C)(CCCC(O)(CCCC(O)(CCCC(O)(CCC/C(=C/CC/C(=C/CC/C(=C/CC/C(=C/CO)/C)/C)/C)/C)C)C)C)C',
                                      'name': 'Glisoprenin B',
                                      'reason': 'Molecule contains rings; '
                                                'expected a linear isoprenoid '
                                                'chain.'},
                                  {   'smiles': 'OC(C(O)CO)(CC/C=C(/CC/C=C(/CCCC(O)(CCCC(O)(CCCC(O)(CCCC(O)(CCCC(O)(CCCC(O)(CCC=C(C)C)C)C)C)C)C)C)\\C)\\C)C',
                                      'name': 'Gymnoprenol A10',
                                      'reason': 'Mismatch between repeating '
                                                'fragment count (2) and '
                                                'expected isoprene units (~10) '
                                                'based on a 40-carbon chain.'}],
    'attempt': 3,
    'reasoning': 'We can see from the previous version that many of the '
                 'false‐positives come from molecules that (although they '
                 'include one or two “isoprene‐like” matches) contain extra '
                 'functionalities not expected for a polyprenol (for example, '
                 'carbonyl groups as in acids) or that the repeating '
                 '“isoprene” chain is not as long as expected. Also one false '
                 'negative (Glisoprenin B) was rejected because of a ring. '
                 '(According to our definition the carbon “backbone” should be '
                 'essentially linear.) In our new version we make several '
                 'changes:\n'
                 '\n'
                 '• First we insist that the molecule is built only from C, H '
                 'and O.\n'
                 '• We check that the molecule is acyclic.\n'
                 '• We require that no carbonyl (C=O) groups are present.\n'
                 '• We then require a terminal –OH (on a primary carbon) as '
                 'before.\n'
                 '• We compute the number of carbons in the longest '
                 'uninterrupted “carbon‐chain” (i.e. the diameter of the '
                 'induced subgraph of C atoms) and require that its length is '
                 'consistent with having many repeating isoprene units '
                 '(roughly one unit for every 4 atoms along that chain).\n'
                 '• We also count three different types of isoprene‐like '
                 'fragments (a terminal “alpha” unit, an “internal” unit, and '
                 'a terminal “omega” unit) using SMARTS and then compare the '
                 'total count with the expected number from the longest '
                 'chain.\n'
                 '\n'
                 'If these conditions are met we classify the molecule as a '
                 'polyprenol; otherwise we return a “False” with an '
                 'explanation. (Note that some cases such as molecules with an '
                 'extra ring or extra functionalities will be excluded.) \n'
                 '\n'
                 'Below is the complete Python code in one code block.\n'
                 '\n'
                 '------------------------------------------------',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 12,
    'num_false_positives': 10,
    'num_true_negatives': 142263,
    'num_false_negatives': 15,
    'num_negatives': None,
    'precision': 0.5454545454545454,
    'recall': 0.4444444444444444,
    'f1': 0.4897959183673469,
    'accuracy': 0.9998243148278285,
    'negative_predictive_value': 0.9998945725973095}