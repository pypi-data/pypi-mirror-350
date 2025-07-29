"""
Classifies: CHEBI:28966 chlorophyll
"""
"""
Classifies: Chlorophyll – a family of magnesium porphyrins (or chlorins) defined by the presence
of a fused macrocycle that contains a fifth (extra, non‐pyrrole) ring. The rings have various side chains,
most often including a long phytol chain (or exocyclic ester groups in chlorophyllides).
"""

from rdkit import Chem
from rdkit.Chem import rdMolDescriptors

def is_chlorophyll(smiles: str):
    """
    Determines if a molecule is classified as chlorophyll (or chlorophyllide) based on its SMILES string.
    
    The decision uses the following heuristic:
      1. The molecule must be valid and neutral.
      2. The molecule must contain at least one magnesium atom.
      3. The overall fused ring system must comprise at least 5 rings, and at least one should be five-membered.
      4. Count the number of nitrogen atoms present in rings (i.e. part of the macrocycle).
         We require at least 4 such N atoms even if the “direct coordination” to Mg is not obvious.
      5. Finally, to filter out false positives (e.g. magnesium protoporphyrins), we check that the molecule has
         either a “long” acyclic carbon chain (≥10 C atoms outside rings, as a phytol chain) or it shows at least one
         exocyclic ester group ([OX2;!R]-C(=O)) attached to the macrocycle.
         
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if the molecule is classified as chlorophyll (or chlorophyllide), False otherwise.
        str: Explanation for the decision.
    """
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
    
    # Check overall neutrality (sum of formal charges should be zero)
    total_charge = sum(atom.GetFormalCharge() for atom in mol.GetAtoms())
    if total_charge != 0:
        return False, f"Molecule net charge is {total_charge}, expected neutral"

    # Check for magnesium (atomic number 12)
    mg_atoms = [atom for atom in mol.GetAtoms() if atom.GetAtomicNum() == 12]
    if not mg_atoms:
        return False, "No magnesium atom found"

    # Get ring information
    ring_info = mol.GetRingInfo()
    num_rings = ring_info.NumRings()
    if num_rings < 5:
        return False, f"Insufficient number of rings found ({num_rings}); expected at least 5"

    # Get list of all rings (as tuples of atom indices)
    atom_rings = ring_info.AtomRings()
    
    # Check that at least one ring is five-membered.
    if not any(len(ring) == 5 for ring in atom_rings):
        return False, "No five-membered ring (extra fused ring) found"

    # Gather nitrogen atoms that are part of any ring
    ring_nitrogens = set()
    for ring in atom_rings:
        for idx in ring:
            atom = mol.GetAtomWithIdx(idx)
            if atom.GetAtomicNum() == 7:
                ring_nitrogens.add(idx)
    
    if len(ring_nitrogens) < 4:
        return False, f"Only {len(ring_nitrogens)} nitrogen atoms found in rings; expected at least 4"
    
    # OPTIONAL: now check for the presence of a characteristic side chain.
    # We define two mutually exclusive criteria:
    # (a) A long acyclic carbon chain (phytol chain) outside of any ring – we define long as 10 or more connected carbons.
    # (b) At least one exocyclic ester group attached (SMARTS: [OX2;!R]-C(=O)[#6]).
    # (A molecule meeting either (a) or (b) is acceptable.)
    
    # First, identify atoms that belong to any ring.
    ring_atom_idxs = set()
    for ring in atom_rings:
        ring_atom_idxs.update(ring)
    
    # Build an acyclic carbon graph of carbons not in rings
    acyclic_carbons = {atom.GetIdx() for atom in mol.GetAtoms() if atom.GetAtomicNum() == 6 and atom.GetIdx() not in ring_atom_idxs}
    carbon_graph = {idx: set() for idx in acyclic_carbons}
    for bond in mol.GetBonds():
        i = bond.GetBeginAtomIdx()
        j = bond.GetEndAtomIdx()
        if i in acyclic_carbons and j in acyclic_carbons:
            carbon_graph[i].add(j)
            carbon_graph[j].add(i)
            
    # DFS-based search to find longest path in the acyclic carbon subgraph.
    longest_chain = 0
    def dfs(current, visited):
        max_length = 1
        for neighbor in carbon_graph.get(current, []):
            if neighbor not in visited:
                length = 1 + dfs(neighbor, visited | {neighbor})
                if length > max_length:
                    max_length = length
        return max_length

    for start in carbon_graph:
        chain_length = dfs(start, {start})
        if chain_length > longest_chain:
            longest_chain = chain_length

    # Check for exocyclic ester groups (attached to rings but not in rings).
    ester_smarts = "[OX2;!R]-C(=O)[#6]"
    ester_query = Chem.MolFromSmarts(ester_smarts)
    ester_matches = mol.GetSubstructMatches(ester_query)
    
    # Flag whether one of the ester atoms is attached to a ring atom (assume excocyclic if the O is not in a ring but neighbors a ring atom)
    exo_ester_found = False
    for match in ester_matches:
        # match is a tuple of atom indices for the pattern [O;!R]-C(=O)-...
        o_idx = match[0]
        o_atom = mol.GetAtomWithIdx(o_idx)
        # if any neighbor of this O is in a ring, we consider this ester exocyclic to a cyclic system.
        if any(nbr.GetIdx() in ring_atom_idxs for nbr in o_atom.GetNeighbors()):
            exo_ester_found = True
            break

    # Now decide: require at least one of the two criteria is met.
    chain_ok = longest_chain >= 10
    ester_ok = exo_ester_found

    if not (chain_ok or ester_ok):
        chain_comment = f"No long phytol chain detected (longest acyclic carbon chain is {longest_chain} atoms) and no exocyclic ester group found"
    else:
        if chain_ok:
            chain_comment = f"Contains long acyclic chain of {longest_chain} carbons (phytol chain present)"
        else:
            chain_comment = "No long acyclic chain detected but exocyclic ester group(s) present"

    # Construct a reason message that summarizes key features.
    reason = ("Contains magnesium; fused ring system with at least 5 rings (including a five-membered ring); "
              f"found {len(ring_nitrogens)} ring nitrogens; {chain_comment}.")
    
    return True, reason

# Example (this block can be commented out when used as a module)
if __name__ == "__main__":
    # Test a chlorophyll a structure (should be True)
    test_smiles = "CCC1=C(C)C2=Cc3c(C=C)c(C)c4C=C5[C@@H](C)[C@H](CCC(=O)OC\\C=C(/C)CCC[C@H](C)CCC[C@H](C)CCCC(C)C)C6=[N+]5[Mg--]5(n34)n3c(=CC1=[N+]25)c(C)c1C(=O)[C@H](C(=O)OC)C6=c31"
    result, reason = is_chlorophyll(test_smiles)
    print(result)
    print(reason)


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:28966',
                          'name': 'chlorophyll',
                          'definition': 'A family of magnesium porphyrins, '
                                        'defined by the presence of a fifth '
                                        'ring beyond the four pyrrole-like '
                                        'rings. The rings can have various '
                                        'side chains which usually include a '
                                        'long phytol chain.',
                          'parents': ['CHEBI:25111'],
                          'xrefs': [   'CAS:1406-65-1',
                                       'COMe:MOL000012',
                                       'KEGG:C01793',
                                       'PMID:29286160'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 113,
                           'log_lines_of_code': 4.727387818712341,
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
                                                 1,
                                                 2,
                                                 0,
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
                                                 3,
                                                 3,
                                                 4,
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
                                                 2,
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
                                                 3,
                                                 1,
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
                                                 2,
                                                 2,
                                                 3,
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
                                                 2,
                                                 3,
                                                 3,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 0,
                                                 1,
                                                 2,
                                                 1,
                                                 2,
                                                 3,
                                                 2,
                                                 3,
                                                 0,
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
                                                 1],
                           'max_indent': 5,
                           'imports': [   'from rdkit import Chem',
                                          'from rdkit.Chem import '
                                          'rdMolDescriptors'],
                           'imports_count': 2,
                           'methods_called': [   'GetEndAtomIdx',
                                                 'GetIdx',
                                                 'NumRings',
                                                 'GetAtomicNum',
                                                 'GetBeginAtomIdx',
                                                 'MolFromSmiles',
                                                 'AtomRings',
                                                 'GetAtomWithIdx',
                                                 'GetAtoms',
                                                 'GetBonds',
                                                 'GetSubstructMatches',
                                                 'MolFromSmarts',
                                                 'get',
                                                 'GetNeighbors',
                                                 'add',
                                                 'update',
                                                 'GetRingInfo',
                                                 'GetFormalCharge'],
                           'methods_called_count': 18,
                           'smarts_strings': ['ester_smarts'],
                           'smarts_strings_count': 1,
                           'defs': [   'is_chlorophyll(smiles: str):',
                                       'dfs(current, visited):'],
                           'defs_count': 2,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, f"Molecule net charge is '
                                          '{total_charge}, expected neutral"',
                                          'False, "No magnesium atom found"',
                                          'False, f"Insufficient number of '
                                          'rings found ({num_rings}); expected '
                                          'at least 5"',
                                          'False, "No five-membered ring '
                                          '(extra fused ring) found"',
                                          'False, f"Only {len(ring_nitrogens)} '
                                          'nitrogen atoms found in rings; '
                                          'expected at least 4"',
                                          'max_length',
                                          'True, reason'],
                           'returns_count': 8,
                           'complexity': 7.545477563742469},
    'message': '\n'
               'Attempt failed: F1 score of 0.7924528301886792 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: '
               'C=12N3C(=CC4=[N+]5C(=CC=6N7C=8C(=C9[N+](=C(C1)[C@H]([C@@H]9CCC(O)=O)C)[Mg-2]753)CC(C8C6CC)=O)C(=C4C)CCC)C(=C2C)C=C '
               'NAME: 12-ethyl-8-propyl-3-vinylbacteriochlorophyllide d '
               'REASON: CORRECT Contains magnesium porphyrin core (Mg '
               'coordinated to >=4 N) and a fused ring system with at least 5 '
               'rings including a five-membered ring. No long phytol chain '
               'detected (longest acyclic carbon chain is 3 atoms)\n'
               ' * SMILES: '
               'C1=2N3C(C=C4[N+]5=C(C=C6N7C8=C(C9=[N+](C(=C1)[C@H]([C@@H]9CCC(OC/C=C(/CCC[C@@H](CCC[C@@H](CCCC(C)C)C)C)\\C)=O)C)[Mg-2]735)[C@@H](C(C8=C6C)=O)C(=O)OC)C(=C4C)C=C)=C(C2C)C=C '
               "NAME: divinylchlorophyll a' REASON: CORRECT Contains magnesium "
               'porphyrin core (Mg coordinated to >=4 N) and a fused ring '
               'system with at least 5 rings including a five-membered ring. '
               'Contains long acyclic chain of 16 carbons (phytol chain '
               'present)\n'
               ' * SMILES: '
               'CC[C@@H]1[C@@H](C)C2=Cc3c(C(C)=O)c(C)c4C=C5[C@@H](C)[C@H](CCC(=O)OC\\C=C(/C)CCC[C@H](C)CCC[C@H](C)CCCC(C)C)C6=[N+]5[Mg--]5(n34)n3c(=CC1=[N+]25)c(C)c1C(=O)[C@H](C(=O)OC)C6=c31 '
               'NAME: bacteriochlorophyll a REASON: CORRECT Contains magnesium '
               'porphyrin core (Mg coordinated to >=4 N) and a fused ring '
               'system with at least 5 rings including a five-membered ring. '
               'Contains long acyclic chain of 16 carbons (phytol chain '
               'present)\n'
               ' * SMILES: '
               'C=12N3C(=CC4=[N+]5C(=CC=6N7C=8C(=C9[N+](=C(C1)[C@H]([C@@H]9CCC(O)=O)C)[Mg-2]753)CC(C8C6C)=O)C(=C4C)CC)C(=C2C)C=C '
               'NAME: 3-vinylbacteriochlorophyllide d REASON: CORRECT Contains '
               'magnesium porphyrin core (Mg coordinated to >=4 N) and a fused '
               'ring system with at least 5 rings including a five-membered '
               'ring. No long phytol chain detected (longest acyclic carbon '
               'chain is 3 atoms)\n'
               ' * SMILES: '
               'C1=2N3C(C=C4[N+]5=C(C=C6N7C8=C(C9=[N+](C(=C1)[C@H]([C@@H]9CCC(OC/C=C(/CCC[C@@H](CCC[C@@H](CCCC(C)C)C)C)\\C)=O)C)[Mg-2]735)[C@@H](C(C8=C6C)=O)C(=O)OC)C(=C4C)CC)=C(C2C)C=C '
               "NAME: chlorophyll a' REASON: CORRECT Contains magnesium "
               'porphyrin core (Mg coordinated to >=4 N) and a fused ring '
               'system with at least 5 rings including a five-membered ring. '
               'Contains long acyclic chain of 16 carbons (phytol chain '
               'present)\n'
               ' * SMILES: '
               'CCC1=C(C)C2=Cc3c(C=C)c(C)c4C=C5[C@@H](C)[C@H](CCC(=O)OC\\C=C(/C)CCC[C@H](C)CCC[C@H](C)CCCC(C)C)C6=[N+]5[Mg--]5(n34)n3c(=CC1=[N+]25)c(C)c1C(=O)[C@H](C(=O)OC)C6=c31 '
               'NAME: chlorophyll a REASON: CORRECT Contains magnesium '
               'porphyrin core (Mg coordinated to >=4 N) and a fused ring '
               'system with at least 5 rings including a five-membered ring. '
               'Contains long acyclic chain of 16 carbons (phytol chain '
               'present)\n'
               ' * SMILES: '
               'COC(=O)[C@H]1C(=O)c2c(C)c3C=C4C(C=C)=C(C=O)C5=[N+]4[Mg--]46n3c2C1=C1[C@@H](CCC(=O)OC\\C=C(/C)CCC[C@H](C)CCC[C@H](C)CCCC(C)C)[C@H](C)C(C=c2c(C)c(C=C)c(=C5)n42)=[N+]61 '
               'NAME: divinyl chlorophyll b REASON: CORRECT Contains magnesium '
               'porphyrin core (Mg coordinated to >=4 N) and a fused ring '
               'system with at least 5 rings including a five-membered ring. '
               'Contains long acyclic chain of 16 carbons (phytol chain '
               'present)\n'
               ' * SMILES: '
               'CCC1=C(C)C2=Cc3c(C=C)c(C)c4C=C5[C@@H](C)[C@H](CCC(=O)OC\\C=C(/C)CC\\C=C(/C)CC\\C=C(/C)CCC=C(C)C)C6=[N+]5[Mg--]5(n34)n3c(=CC1=[N+]25)c(C)c1C(=O)[C@H](C(=O)OC)C6=c31 '
               'NAME: geranylgeranyl-chlorophyll a REASON: CORRECT Contains '
               'magnesium porphyrin core (Mg coordinated to >=4 N) and a fused '
               'ring system with at least 5 rings including a five-membered '
               'ring. Contains long acyclic chain of 16 carbons (phytol chain '
               'present)\n'
               ' * SMILES: '
               'C=12N3C(=CC4=[N+]5C(=CC=6N7C=8C(=C9[N+](=C(C1)[C@H]([C@@H]9CCC(O)=O)C)[Mg-2]753)CC(C8C6CC)=O)C(=C4C)CC)C(=C2C)C=C '
               'NAME: 8,12-diethyl-3-vinylbacteriochlorophyllide d REASON: '
               'CORRECT Contains magnesium porphyrin core (Mg coordinated to '
               '>=4 N) and a fused ring system with at least 5 rings including '
               'a five-membered ring. No long phytol chain detected (longest '
               'acyclic carbon chain is 3 atoms)\n'
               ' * SMILES: '
               'CC[C@@H]1[C@@H](C)C2=Cc3c(C=C)c(C)c4C=C5[C@@H](C)[C@H](CCC(O)=O)C6=[N+]5[Mg--]5(n34)n3c(=CC1=[N+]25)c(C)c1C(=O)[C@H](C(=O)OC)C6=c31 '
               'NAME: 3-vinylbacteriochlorophyllide a REASON: CORRECT Contains '
               'magnesium porphyrin core (Mg coordinated to >=4 N) and a fused '
               'ring system with at least 5 rings including a five-membered '
               'ring. No long phytol chain detected (longest acyclic carbon '
               'chain is 3 atoms)\n'
               ' * SMILES: '
               '[H]C(C)=C1C(C)C2=CC3=C(C(C)=O)C(C)=C4C=C5[C@@H](C)[C@H](CCC(=O)OC\\C=C(/C)CCC[C@H](C)CCC[C@H](C)CCCC(C)C)C6=[N+]5[Mg--]5(N34)N3C(=CC1=[N+]25)C(C)=C1C(=O)[C@H](C(=O)OC)C6=C31 '
               'NAME: bacteriochlorophyll b REASON: CORRECT Contains magnesium '
               'porphyrin core (Mg coordinated to >=4 N) and a fused ring '
               'system with at least 5 rings including a five-membered ring. '
               'Contains long acyclic chain of 16 carbons (phytol chain '
               'present)\n'
               ' * SMILES: '
               'C=12N3C(=CC4=[N+]5C(=CC=6N7C=8C(=C9[N+](=C(C1)[C@H]([C@@H]9CCC(O)=O)C)[Mg-2]735)[C@H](C(C8C6C)=O)C(=O)OC)/C(/[C@H]4C)=C\\C)C(=C2C)C=C '
               'NAME: bacteriochlorophyllide g REASON: CORRECT Contains '
               'magnesium porphyrin core (Mg coordinated to >=4 N) and a fused '
               'ring system with at least 5 rings including a five-membered '
               'ring. No long phytol chain detected (longest acyclic carbon '
               'chain is 3 atoms)\n'
               ' * SMILES: '
               'COC(=O)[C@H]1C(=O)c2c(C)c3=CC4=[N+]5C(=Cc6c(C=C)c(C)c7C=C8[C@@H](C)[C@H](CCC(=O)OC\\C=C(/C)CCC[C@H](C)CCC[C@H](C)CCCC(C)C)C9=[N+]8[Mg--]5(n67)n3c2=C19)C(C)=C4C=C '
               'NAME: divinyl chlorophyll a REASON: CORRECT Contains magnesium '
               'porphyrin core (Mg coordinated to >=4 N) and a fused ring '
               'system with at least 5 rings including a five-membered ring. '
               'Contains long acyclic chain of 16 carbons (phytol chain '
               'present)\n'
               ' * SMILES: '
               'CCC1=C(C)C2=[N+]3C1=Cc1c(C)c4C(=O)[C@H](C(=O)OC)C5=C6C(CCC(O)=O)=C(C)C7=[N+]6[Mg--]3(n1c45)n1c(=C7)c(C)c(C=C)c1=C2 '
               'NAME: protochlorophyllide REASON: CORRECT Contains magnesium '
               'porphyrin core (Mg coordinated to >=4 N) and a fused ring '
               'system with at least 5 rings including a five-membered ring. '
               'No long phytol chain detected (longest acyclic carbon chain is '
               '3 atoms)\n'
               ' * SMILES: '
               'CC(O)C1=C2C=C3C(C)=C(C)C4=[N+]3[Mg--]35N6C(=C4)C(C)=C4C(=O)CC(=C64)C4=[N+]3C([C@@H](C)[C@@H]4CCC(=O)OC\\C=C(/C)CC\\C=C(/C)CCC=C(C)C)=C(C)C(N25)=C1C '
               'NAME: bacteriochlorophyll c REASON: CORRECT Contains magnesium '
               'porphyrin core (Mg coordinated to >=4 N) and a fused ring '
               'system with at least 5 rings including a five-membered ring. '
               'Contains long acyclic chain of 12 carbons (phytol chain '
               'present)\n'
               ' * SMILES: '
               'C=12N3C(=CC4=[N+]5C(=CC=6N7C=8C(=C9[N+](=C(C1)[C@H]([C@@H]9CCC(O)=O)C)[Mg-2]735)[C@H](C(C8C6C)=O)C(=O)OC)[C@@H]([C@H]4C)CC)C(=C2C)C(=O)C '
               'NAME: bacteriochlorophyllide a REASON: CORRECT Contains '
               'magnesium porphyrin core (Mg coordinated to >=4 N) and a fused '
               'ring system with at least 5 rings including a five-membered '
               'ring. No long phytol chain detected (longest acyclic carbon '
               'chain is 3 atoms)\n'
               ' * SMILES: '
               'CCC1=C(C)C2=Cc3c(C=C)c(C)c4C=C5[C@@H](C)[C@H](CCC(O)=O)C6=[N+]5[Mg--]5(n34)n3c(=CC1=[N+]25)c(C)c1C(=O)[C@H](C(=O)OC)C6=c31 '
               'NAME: chlorophyllide a REASON: CORRECT Contains magnesium '
               'porphyrin core (Mg coordinated to >=4 N) and a fused ring '
               'system with at least 5 rings including a five-membered ring. '
               'No long phytol chain detected (longest acyclic carbon chain is '
               '3 atoms)\n'
               ' * SMILES: '
               'COC(=O)[C@H]1C(=O)c2c(C)c3C=C4C(C=C)=C(C)C5=[N+]4[Mg--]46n3c2C1=C1[C@@H](CCC(O)=O)[C@H](C)C(C=c2c(C)c(C=C)c(=C5)n42)=[N+]61 '
               'NAME: divinyl chlorophyllide a REASON: CORRECT Contains '
               'magnesium porphyrin core (Mg coordinated to >=4 N) and a fused '
               'ring system with at least 5 rings including a five-membered '
               'ring. No long phytol chain detected (longest acyclic carbon '
               'chain is 3 atoms)\n'
               ' * SMILES: '
               'CCC1=C(CO)C2=Cc3c(C=C)c(C)c4C=C5[C@@H](C)[C@H](CCC(=O)OC\\C=C(/C)CCC[C@H](C)CCC[C@H](C)CCCC(C)C)C6=[N+]5[Mg--]5(n34)n3c(=CC1=[N+]25)c(C)c1C(=O)[C@H](C(=O)OC)C6=c31 '
               'NAME: 7(1)-hydroxychlorophyll a REASON: CORRECT Contains '
               'magnesium porphyrin core (Mg coordinated to >=4 N) and a fused '
               'ring system with at least 5 rings including a five-membered '
               'ring. Contains long acyclic chain of 16 carbons (phytol chain '
               'present)\n'
               ' * SMILES: '
               'C=12N3C(=CC4=[N+]5C(=CC=6N7C=8C(=C9[N+](=C(C1)[C@H]([C@@H]9CCC(O)=O)C)[Mg-2]735)[C@H](C(C8C6C)=O)C(=O)OC)C(=C4C)CC)C(=C2C)C(O)C '
               'NAME: 3-(1-hydroxyethyl)chlorophyllide a REASON: CORRECT '
               'Contains magnesium porphyrin core (Mg coordinated to >=4 N) '
               'and a fused ring system with at least 5 rings including a '
               'five-membered ring. No long phytol chain detected (longest '
               'acyclic carbon chain is 3 atoms)\n'
               ' * SMILES: '
               'CCC1=C(C=O)C2=Cc3c(C=C)c(C)c4C=C5[C@@H](C)[C@H](CCC(=O)OC\\C=C(/C)CCC[C@H](C)CCC[C@H](C)CCCC(C)C)C6=[N+]5[Mg--]5(n34)n3c(=CC1=[N+]25)c(C)c1C(=O)[C@H](C(=O)OC)C6=c31 '
               'NAME: chlorophyll b REASON: CORRECT Contains magnesium '
               'porphyrin core (Mg coordinated to >=4 N) and a fused ring '
               'system with at least 5 rings including a five-membered ring. '
               'Contains long acyclic chain of 16 carbons (phytol chain '
               'present)\n'
               'False positives: SMILES: '
               'COC(=O)CCc1c(C)c2=CC3=[N]4C(=Cc5c(C=C)c(C)c6C=C7C(C)=C(CCC(O)=O)C8=[N]7[Mg]4(n56)n2c1=C8)C(C)=C3C=C '
               'NAME: magnesium protoporphyrin 13-monomethyl ester REASON: '
               'WRONGLY CLASSIFIED Contains magnesium porphyrin core (Mg '
               'coordinated to >=4 N) and a fused ring system with at least 5 '
               'rings including a five-membered ring. No long phytol chain '
               'detected (longest acyclic carbon chain is 3 atoms)\n'
               ' * SMILES: '
               'CC1=C(CCC(O)=O)C2=[N+]3C1=Cc1c(C)c(C=C)c4C=C5C(C)=C(C=C)C6=[N+]5[Mg--]3(n14)n1c(=C6)c(C)c(CCC(O)=O)c1=C2 '
               'NAME: magnesium protoporphyrin REASON: WRONGLY CLASSIFIED '
               'Contains magnesium porphyrin core (Mg coordinated to >=4 N) '
               'and a fused ring system with at least 5 rings including a '
               'five-membered ring. No long phytol chain detected (longest '
               'acyclic carbon chain is 3 atoms)\n'
               ' * SMILES: '
               'c1ccc2c(c1)C1=Nc3n4c(N=C5c6ccccc6C6=[N]5[Mg]44[N]1=C2N=c1n4c(=N6)c2ccccc12)c1ccccc31 '
               'NAME: magnesium phthalocyanine REASON: WRONGLY CLASSIFIED '
               'Contains magnesium porphyrin core (Mg coordinated to >=4 N) '
               'and a fused ring system with at least 5 rings including a '
               'five-membered ring. No long phytol chain detected (longest '
               'acyclic carbon chain is 0 atoms)\n'
               ' * SMILES: '
               'C=12N3C(=CC4=N5C(=CC=6N7C(C=C8N(=C(C1)C(=C8CCC(O)=O)C)[Mg]735)=C(C6C)C(CC(OC)=O)=O)C(=C4C)C=C)C(=C2C)C=C '
               'NAME: magnesium 13(1)-oxoprotoporphyrin 13-monomethyl ester '
               'REASON: WRONGLY CLASSIFIED Contains magnesium porphyrin core '
               '(Mg coordinated to >=4 N) and a fused ring system with at '
               'least 5 rings including a five-membered ring. No long phytol '
               'chain detected (longest acyclic carbon chain is 3 atoms)\n'
               ' * SMILES: '
               'COC(=O)CC(O)c1c(C)c2=CC3=[N+]4C(=Cc5c(C=C)c(C)c6C=C7C(C)=C(CCC(O)=O)C8=[N+]7[Mg--]4(n56)n2c1=C8)C(C)=C3C=C '
               'NAME: magnesium 13(1)-hydroxyprotoporphyrin 13-monomethyl '
               'ester REASON: WRONGLY CLASSIFIED Contains magnesium porphyrin '
               'core (Mg coordinated to >=4 N) and a fused ring system with at '
               'least 5 rings including a five-membered ring. No long phytol '
               'chain detected (longest acyclic carbon chain is 3 atoms)\n'
               'False negatives: SMILES: '
               'CCC1=C(C)/C2=C/c3c(C=C)c(C)c4\\C=C5/N=C(C(\\C=C\\C(O)=O)=C/5C)C5=c6c(C(=O)C5C(=O)OC)c(C)c(=CC1=N\\2)n6[Mg]n34 '
               'NAME: chlorophyll c1 REASON: MISSED Magnesium is not '
               'coordinated to at least four nitrogen atoms (porphyrin core '
               'missing)\n'
               ' * SMILES: '
               'COC(=O)C1C(=O)c2c(C)c3=CC4=N\\C(=C/c5c(C=C)c(C)c6\\C=C7/N=C(C(\\C=C\\C(O)=O)=C/7C)C1=c2n3[Mg]n56)\\C(C)=C4C=C '
               'NAME: chlorophyll c2 REASON: MISSED Magnesium is not '
               'coordinated to at least four nitrogen atoms (porphyrin core '
               'missing)\n'
               ' * SMILES: '
               'C=12N3C(=CC4=NC(=CC=5N(C=6C(=C7N=C(C1)[C@H]([C@@H]7CCC(O)=O)C)[C@H](C(C6C5C)=O)C(=O)OC)[Mg]3)C(=C4CO)CC)C(=C2C)C=C '
               'NAME: 7(1)-hydroxychlorophyllide a REASON: MISSED Magnesium is '
               'not coordinated to at least four nitrogen atoms (porphyrin '
               'core missing)\n'
               ' * SMILES: '
               '[H]C(=O)c1c(C=C)c2\\C=C3/N=C(C=c4c(C)c5C(=O)[C@H](C(=O)OC)C6=c5n4[Mg]n2c1\\C=C1/N=C6[C@@H](CCC(=O)OC\\C=C(/C)CCC[C@H](C)CCC[C@H](C)CCCC(C)C)[C@@H]1C)C(CC)=C/3C '
               'NAME: chlorophyll f REASON: MISSED Magnesium is not '
               'coordinated to at least four nitrogen atoms (porphyrin core '
               'missing)\n'
               ' * SMILES: '
               'COC(=O)[C@H]1C(=O)c2c(C)c3=CC4=N\\C(=C/c5c(C(C)=O)c(C)c6\\C=C7/N=C([C@@H](CCC(=O)OC\\C=C(/C)CCC[C@H](C)CCC[C@H](C)CCCC(C)C)[C@@H]7C)C1=c2n3[Mg]n56)[C@H](C)C/4=C/C '
               'NAME: (7R,8Z)-bacteriochlorophyll b REASON: MISSED Magnesium '
               'is not coordinated to at least four nitrogen atoms (porphyrin '
               'core missing)\n'
               ' * SMILES: '
               '[H]C(=O)c1c(C)c2\\C=C3/N=C([C@@H](CCC(=O)OC\\C=C(/C)CCC[C@H](C)CCC[C@H](C)CCCC(C)C)[C@@H]3C)C3=c4c(C(=O)[C@@H]3C(=O)OC)c(C)c3=CC5=N\\C(=C/c1n2[Mg]n43)\\C(C)=C5CC '
               'NAME: chlorophyll d REASON: MISSED Magnesium is not '
               'coordinated to at least four nitrogen atoms (porphyrin core '
               'missing)\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'O=C(N[C@@H](C(O)(C)C)C)[C@H]([C@@]1([C@@]2([C@@](CC1)(/C(/CCC2)=C/C=C\\3/C[C@@H](O)C[C@H](O)C3=C)[H])C)[H])C',
                                     'name': '1alpha,25-dihydroxy-24-oxo-23-azavitamin '
                                             'D2 / '
                                             '1alpha,25-dihydroxy-24-oxo-23-azaergocalciferol',
                                     'reason': 'No magnesium atom found'},
                                 {   'smiles': 'CCCCCCCCCCCCCCCCCCC(O)C([O-])=O',
                                     'name': '2-hydroxyarachidate',
                                     'reason': 'Molecule net charge is -1, '
                                               'expected neutral'},
                                 {   'smiles': 'C[C@@H](CN([C@@H](C)CO)C(=O)NC1=CC=C(C=C1)C(F)(F)F)[C@@H](CN(C)C(=O)C2CCOCC2)OC',
                                     'name': 'N-[(2S,3S)-4-[[(2S)-1-hydroxypropan-2-yl]-[[4-(trifluoromethyl)phenyl]carbamoyl]amino]-2-methoxy-3-methylbutyl]-N-methyloxane-4-carboxamide',
                                     'reason': 'No magnesium atom found'},
                                 {   'smiles': 'CC(=O)CC\\C=C(/C)CCC=C(C)C',
                                     'name': 'geranyl acetone',
                                     'reason': 'No magnesium atom found'},
                                 {   'smiles': 'O([C@H]1[C@H](O)[C@H](O[C@H](O)[C@H]1O)CO[C@H]2O[C@@H]([C@@H](O)[C@H](O)[C@@H]2O)CO)[C@H]3O[C@@H]([C@@H](O)[C@H](O)[C@@H]3O[C@H]4O[C@@H]([C@@H](O)[C@H](O)[C@@H]4O)CO)CO',
                                     'name': '(2S,3S,4S,5S,6R)-2-[[(2R,3R,4S,5S,6S)-4-[(2R,3S,4S,5S,6R)-4,5-Dihydroxy-6-(hydroxymethyl)-3-[(2R,3S,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-3,5,6-trihydroxyoxan-2-yl]methoxy]-6-(hydroxymethyl)oxane-3,4,5-triol',
                                     'reason': 'No magnesium atom found'},
                                 {   'smiles': 'O=C(OC1=C(C(O)=C(C(=O)O)C(=C1C)C)C)C2=C(OC)C(=C(OC(=O)C3=C(O)C=C(O)C=C3C)C=C2C)C',
                                     'name': 'Thielavin Z5',
                                     'reason': 'No magnesium atom found'},
                                 {   'smiles': '[C@@H]1([C@@H]([C@H]([C@@H]([C@H](O1)CO)O)O)NC(C)=O)O[C@@H]2[C@@H]([C@H](C(O[C@@H]2CO)O)O)O',
                                     'name': 'beta-D-GlcpNAc-(1->4)-D-Galp',
                                     'reason': 'No magnesium atom found'},
                                 {   'smiles': 'CN(C)C(=O)C1=CC=C(C=C1)C2=CC=C(C=C2)[C@@H]3[C@H]4CN(CC(=O)N4[C@H]3CO)C(=O)CC5CC5',
                                     'name': '4-[4-[(6S,7R,8R)-4-(2-cyclopropyl-1-oxoethyl)-8-(hydroxymethyl)-2-oxo-1,4-diazabicyclo[4.2.0]octan-7-yl]phenyl]-N,N-dimethylbenzamide',
                                     'reason': 'No magnesium atom found'},
                                 {   'smiles': 'CCCCCCCCCCCCCCCCCCCCC=C',
                                     'name': '1-docosene',
                                     'reason': 'No magnesium atom found'},
                                 {   'smiles': 'C([C@@](OC(=O)CCC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)([H])COC(=O)CC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)OC(=O)CCCCC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC',
                                     'name': 'TG(22:5(7Z,10Z,13Z,16Z,19Z)/20:5(5Z,8Z,11Z,14Z,17Z)/22:6(4Z,7Z,10Z,13Z,16Z,19Z))[iso6]',
                                     'reason': 'No magnesium atom found'}],
    'sample_false_negatives': [],
    'attempt': 3,
    'reasoning': 'Below is our reasoning before the code:\n'
                 '\n'
                 '–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––\n'
                 'Our previous attempt looked for “Mg coordinated to ≥4 N” and '
                 'for a fused ring system with at least five rings (including '
                 'one five‐membered ring) and then “optionally” looked for a '
                 'long (≥10‐carbon) side chain. However, when we compared its '
                 'outcomes with the sample structures the following problems '
                 'emerged:\n'
                 ' \n'
                 '• Some molecules (e.g. magnesium protoporphyrins or '
                 'phthalocyanines) have a similar “porphyrin core” and fused '
                 'rings yet are not chlorophyll. Many of these false positives '
                 'had only very short acyclic chains. \n'
                 '• Other chlorophyll variants (e.g. chlorophyll c1/c2 and '
                 'chlorophyll d/f) do not show “Mg coordinated to 4 N” by a '
                 'simple neighbor count because of altered bonding patterns. '
                 'That rule was too strict and led to false negatives.\n'
                 ' \n'
                 'To improve the classification we now use a more '
                 '“macro‐cycle– or chlorin–centered” set of rules. In our '
                 'improved heuristic we require:\n'
                 ' \n'
                 '1. The molecule is valid and neutral.\n'
                 '2. It must contain magnesium.\n'
                 '3. It must have a fused ring system counting at least five '
                 'rings overall and at least one of these rings must be '
                 'five‐membered (our extra, non‐pyrrole ring).\n'
                 '4. Rather than insisting that Mg “directly” be coordinated '
                 'to four nitrogen atoms, we count nitrogen atoms that occur '
                 'in rings of the fused macrocycle (thus allowing for subtle '
                 'variations in connectivity for chlorophyll c/d).\n'
                 '5. Then to help filter out many false positives (which tend '
                 'to lack the characteristic side–chain pattern) we check for '
                 'characteristic side–chains on the macrocycle. In chlorophyll '
                 'this is usually either (a) a relatively long acyclic carbon '
                 'chain (10 or more carbons, as found in many “full” '
                 'chlorophylls) or (b) at least one ester–like moiety (on an '
                 'exocyclic position). (Note that chlorophyllides may lack a '
                 'long phytol chain but still have clear exocyclic ester '
                 'groups.)\n'
                 ' \n'
                 'Together these rules should more closely reproduce the '
                 'expected outcomes. (We recognize that using only heuristics '
                 'and simple SMARTS will not perfectly classify all edge '
                 'cases.) \n'
                 '\n'
                 'Below is the complete Python code (in one code block) that '
                 'implements these ideas.\n'
                 '\n'
                 '–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 27,
    'num_false_positives': 12,
    'num_true_negatives': 142261,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.6923076923076923,
    'recall': 1.0,
    'f1': 0.8181818181818181,
    'accuracy': 0.9999156711173577,
    'negative_predictive_value': 1.0}