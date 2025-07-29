"""
Classifies: CHEBI:47787 11-oxo steroid
"""
#!/usr/bin/env python
"""
Classifies: 11-oxo steroid
Definition: Any oxo steroid that has an oxo substituent (ketone) at position 11.
This heuristic first detects a steroid nucleus – defined as four fused rings 
(three six-membered and one five-membered) whose union of atoms falls (relaxed) into
a count range—and then identifies the “key” six-membered ring (that is fused to the 
five-membered ring, corresponding to the C ring where C11 is located). Only a ketone 
(C=O) found on or immediately attached to that key ring is accepted.
Note:
  This method is heuristic and may still miss very exotic cases.
"""

from rdkit import Chem
from itertools import combinations

def is_11_oxo_steroid(smiles: str):
    """
    Determines if a molecule is an 11-oxo steroid based on its SMILES string.
    The approach is to first search for a steroid nucleus, defined as a set of 4 fused rings 
    (exactly one five-membered and three six-membered rings) whose union of atom indices falls 
    in a relaxed range. Next, among the nucleus rings the five-membered ring (the D ring) is identified;
    then among the six-membered rings, the one sharing the most atoms with the five-membered ring 
    is selected as the candidate C ring (where the 11-oxo is expected). Finally, we look for a ketone 
    (C=O) group whose carbonyl carbon is either in that candidate ring or directly adjacent to it.
    
    Args:
        smiles (str): SMILES string for the molecule.
        
    Returns:
        bool: True if classified as 11-oxo steroid, False otherwise.
        str: Explanation for the decision.
    """
    # Parse the SMILES string.
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string."
    
    # Get ring information and filter rings to sizes 5 or 6.
    ring_info = mol.GetRingInfo()
    all_rings = ring_info.AtomRings()
    candidate_rings = [set(r) for r in all_rings if len(r) in (5, 6)]
    if len(candidate_rings) < 4:
        return False, "Not enough 5- or 6-membered rings to form a steroid nucleus."
    
    nucleus_atoms = None
    nucleus_ring_combo = None
    # We relax union count to between 14 and 24 atoms and also require at least 12 carbon atoms.
    for ring_combo in combinations(candidate_rings, 4):
        count5 = sum(1 for r in ring_combo if len(r) == 5)
        count6 = sum(1 for r in ring_combo if len(r) == 6)
        if count5 != 1 or count6 != 3:
            continue  # Must have exactly one 5-membered and three 6-membered rings.
        # Check connectivity among these rings: build a graph where each ring is a node.
        nodes = list(ring_combo)
        adj = {i: set() for i in range(4)}
        for i in range(4):
            for j in range(i+1, 4):
                if nodes[i] & nodes[j]:
                    adj[i].add(j)
                    adj[j].add(i)
        visited = set()
        stack = [0]
        while stack:
            node = stack.pop()
            if node in visited:
                continue
            visited.add(node)
            stack.extend(adj[node] - visited)
        if len(visited) != 4:
            continue  # Rings not all fused.
        # Compute union of atoms and check total count.
        union_atoms = set()
        for r in ring_combo:
            union_atoms.update(r)
        if not (14 <= len(union_atoms) <= 24):
            continue
        # Count carbons in the union.
        n_carbons = sum(1 for idx in union_atoms if mol.GetAtomWithIdx(idx).GetAtomicNum() == 6)
        if n_carbons < 12:
            continue
        # We have a candidate nucleus.
        nucleus_atoms = union_atoms
        nucleus_ring_combo = ring_combo
        break
    if nucleus_atoms is None:
        return False, "No steroid nucleus (4 fused rings with appropriate sizes) found."
    
    # Identify the unique five-membered ring among the nucleus rings.
    five_membered = None
    six_membered = []
    for r in nucleus_ring_combo:
        if len(r) == 5:
            five_membered = r
        else:
            six_membered.append(r)
    if five_membered is None or not six_membered:
        # fallback if not identified as expected.
        candidate_key_ring = None
    else:
        # Among the six-membered rings, choose the one sharing the most atoms with the five-membered ring.
        candidate_key_ring = None
        max_shared = 0
        for r in six_membered:
            shared = len(r & five_membered)
            if shared > max_shared:
                max_shared = shared
                candidate_key_ring = r
        # It is possible that no six-membered ring is fused with the five-membered ring;
        # in that case, we fallback to checking all nucleus atoms.
    
    # Prepare a SMARTS for a ketone group.
    # Here the pattern [CX3](=O) finds a carbonyl group (ketone) and we allow any connectivity.
    ketone_smarts = "[CX3](=O)"
    ketone_pat = Chem.MolFromSmarts(ketone_smarts)
    if ketone_pat is None:
        return None, None  # SMARTS creation failed.
    
    ketone_matches = mol.GetSubstructMatches(ketone_pat)
    if not ketone_matches:
        return False, "No ketone (C=O) group detected (required for 11-oxo steroid)."
    
    # Now check for a ketone that is ideally located on the candidate key ring
    # (i.e. the six-membered ring fused with the five-membered ring) or directly attached to it.
    for match in ketone_matches:
        # In our ketone pattern, match[0] is the carbonyl carbon.
        ketone_carbon = match[0]
        in_candidate = False
        if candidate_key_ring is not None:
            if ketone_carbon in candidate_key_ring:
                in_candidate = True
            else:
                # Check if any neighbor of the ketone carbon is in the candidate ring.
                atom = mol.GetAtomWithIdx(ketone_carbon)
                if any(neighbor.GetIdx() in candidate_key_ring for neighbor in atom.GetNeighbors()):
                    in_candidate = True
        # If no candidate key ring was found, fallback to checking whether the ketone is on the nucleus 
        # or attached to any nucleus atom.
        else:
            if ketone_carbon in nucleus_atoms:
                in_candidate = True
            else:
                atom = mol.GetAtomWithIdx(ketone_carbon)
                if any(neighbor.GetIdx() in nucleus_atoms for neighbor in atom.GetNeighbors()):
                    in_candidate = True
        
        if in_candidate:
            return True, ("Steroid nucleus detected and ketone group found on or immediately attached "
                          "to the key nucleus ring (consistent with an 11-oxo steroid).")
    
    return False, ("Ketone group not located on or adjacent to the steroid nucleus's key ring "
                   "(likely not a true 11-oxo steroid).")

# Example usage:
if __name__ == '__main__':
    test_smiles = [
        "O=C1C2=C([C@@]3(C(=O)C[C@@H]([C@]3(C1)C)C(=C)CCC(=O)O)C)[C@@H](O)C[C@@H]4[C@@]2(CCC(C4(C)C)=O)",  # 20(21)-dehydrolucidenic acid A (TP)
        "C1[C@@]2([C@@]([C@@]3(C(C1)=CC(CC3)=O)C)(C(C[C@@]4(C)[C@@]2([H])CC[C@@H]4O)=O)[H])[H]",  # 11-oxotestosterone (TP)
        "[H][C@]12CC[C@@]3([H])[C@]4([H])CCC\\C(=C/CO)[C@@]4(C)CC(=O)[C@]3([H])[C@@]1(C)CC[C@@H](O)C2",  # Previously false negative (should be TP)
        "[H][C@]12C[C@@]1([H])[C@]1(C)[C@@H](O)C(=O)\\C(=C(\\C)C(=O)OC)[C@@]3([H])C1=C2C[C@@]1([H])[C@@]2(C)[C@]4([H])C[C@]4([H])[C@](O)(C\\C(C)=C\\C(=O)OC)[C@@]2([H])CC2=C(CO)C(=O)O[C@]312",  # cortistatin D (false positive)
    ]
    for smi in test_smiles:
        res, reason = is_11_oxo_steroid(smi)
        print("SMILES:", smi)
        print("Result:", res)
        print("Reason:", reason)
        print("-----")


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:47787',
                          'name': '11-oxo steroid',
                          'definition': 'Any oxo steroid that has an oxo '
                                        'substituent at position 11.',
                          'parents': ['CHEBI:35789'],
                          'xrefs': ['KEGG:C01985'],
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
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 4,
                                                 5,
                                                 5,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 3,
                                                 4,
                                                 3,
                                                 3,
                                                 2,
                                                 3,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 2,
                                                 3,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 1,
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 3,
                                                 2,
                                                 3,
                                                 1,
                                                 2,
                                                 2,
                                                 1,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 3,
                                                 4,
                                                 4,
                                                 2,
                                                 2,
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
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 4,
                                                 3,
                                                 4,
                                                 4,
                                                 4,
                                                 5,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 4,
                                                 3,
                                                 4,
                                                 4,
                                                 5,
                                                 2,
                                                 2,
                                                 3,
                                                 3,
                                                 1,
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
                                                 2,
                                                 2,
                                                 2,
                                                 2],
                           'max_indent': 5,
                           'imports': [   'from rdkit import Chem',
                                          'from itertools import combinations'],
                           'imports_count': 2,
                           'methods_called': [   'update',
                                                 'append',
                                                 'GetIdx',
                                                 'GetAtomicNum',
                                                 'MolFromSmiles',
                                                 'AtomRings',
                                                 'GetAtomWithIdx',
                                                 'pop',
                                                 'MolFromSmarts',
                                                 'GetNeighbors',
                                                 'add',
                                                 'extend',
                                                 'GetRingInfo',
                                                 'GetSubstructMatches'],
                           'methods_called_count': 14,
                           'smarts_strings': ['ketone_smarts'],
                           'smarts_strings_count': 1,
                           'defs': ['is_11_oxo_steroid(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string."',
                                          'False, "Not enough 5- or 6-membered '
                                          'rings to form a steroid nucleus."',
                                          'False, "No steroid nucleus (4 fused '
                                          'rings with appropriate sizes) '
                                          'found."',
                                          'None, None  # SMARTS creation '
                                          'failed.',
                                          'False, "No ketone (C=O) group '
                                          'detected (required for 11-oxo '
                                          'steroid)."',
                                          'True, ("Steroid nucleus detected '
                                          'and ketone group found on or '
                                          'immediately attached "',
                                          'False, ("Ketone group not located '
                                          'on or adjacent to the steroid '
                                          'nucleus\'s key ring "'],
                           'returns_count': 7,
                           'complexity': 6.383996185165625},
    'message': '\n'
               'Attempt failed: F1 score of 0.013786969090504779 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: '
               'O=C1C2=C([C@@]3(C(=O)C[C@@H]([C@]3(C1)C)C(=C)CCC(=O)O)C)[C@@H](O)C[C@@H]4[C@@]2(CCC(C4(C)C)=O)C '
               'NAME: 20(21)-dehydrolucidenic acid A REASON: CORRECT Steroid '
               'nucleus detected along with a ketone group on the nucleus '
               '(consistent with 11-oxo steroid).\n'
               ' * SMILES: '
               'O=C1C2=C([C@@]3(C(=O)C[C@@H]([C@]3(C1)C)C(=C)CCC(=O)OC)C)[C@@H](O)C[C@@H]4[C@@]2(CCC(C4(C)C)=O)C '
               'NAME: methyl 20(21)-dehydrolucidenate A REASON: CORRECT '
               'Steroid nucleus detected along with a ketone group on the '
               'nucleus (consistent with 11-oxo steroid).\n'
               ' * SMILES: '
               'C1[C@@]2([C@@]([C@@]3(C(C1)=CC(CC3)=O)C)(C(C[C@@]4(C)[C@@]2([H])CC[C@@H]4O)=O)[H])[H] '
               'NAME: 11-oxotestosterone REASON: CORRECT Steroid nucleus '
               'detected along with a ketone group on the nucleus (consistent '
               'with 11-oxo steroid).\n'
               ' * SMILES: '
               'C[C@]12CC(=O)[C@H]3[C@@H](CCC4=CC(=O)CC[C@]34C)[C@@H]1CC[C@]2(O)C(=O)C=O '
               'NAME: 21-dehydrocortisone REASON: CORRECT Steroid nucleus '
               'detected along with a ketone group on the nucleus (consistent '
               'with 11-oxo steroid).\n'
               ' * SMILES: '
               'C1[C@@]2([C@@]([C@@]3(C(C1)=CC(CC3)=O)C)(C(C[C@@]4(C)[C@@]2([H])CCC4=O)=O)[H])[H] '
               'NAME: adrenosterone REASON: CORRECT Steroid nucleus detected '
               'along with a ketone group on the nucleus (consistent with '
               '11-oxo steroid).\n'
               ' * SMILES: '
               'COC(=O)C(C)C(=C)CC[C@@H](C)[C@H]1CC[C@H]2C3=C(C(=O)C[C@]12C)[C@@]1(C)CCC(=O)[C@@H](C)[C@@H]1CC3=O '
               'NAME: zhankuic acid A methyl ester REASON: CORRECT Steroid '
               'nucleus detected along with a ketone group on the nucleus '
               '(consistent with 11-oxo steroid).\n'
               ' * SMILES: '
               '[H][C@@]12CC[C@](O)([C@H](O)CO)[C@@]1(C)CC(=O)[C@@]1([H])[C@@]2([H])CCC2=CC(=O)C=C[C@]12C '
               'NAME: 20alpha-dihydroprednisone REASON: CORRECT Steroid '
               'nucleus detected along with a ketone group on the nucleus '
               '(consistent with 11-oxo steroid).\n'
               ' * SMILES: '
               '[H][C@]12CC[C@@]3([H])[C@]4([H])CC[C@](O)(C(=O)CO)[C@@]4(C)CC(=O)[C@]3([H])[C@@]1(C)CCC(=O)C2 '
               'NAME: 17,21-dihydroxy-5beta-pregnane-3,11,20-trione REASON: '
               'CORRECT Steroid nucleus detected and ketone group is '
               'immediately attached to the nucleus (consistent with 11-oxo '
               'steroid).\n'
               ' * SMILES: '
               '[H][C@@]12CC[C@](O)([C@@H](O)CO)[C@@]1(C)CC(=O)[C@@]1([H])[C@@]2([H])CCC2=CC(=O)C=C[C@]12C '
               'NAME: 20beta-dihydroprednisone REASON: CORRECT Steroid nucleus '
               'detected along with a ketone group on the nucleus (consistent '
               'with 11-oxo steroid).\n'
               ' * SMILES: '
               'O=C1[C@@H]2[C@@]([C@]34CC[C@]([C@H](C[C@@H]3C1)C4)(O)CO)(CC[C@@H]5[C@]2(COC(O5)(C)C)C)C '
               'NAME: Aphidicolin A3 REASON: CORRECT Steroid nucleus detected '
               'along with a ketone group on the nucleus (consistent with '
               '11-oxo steroid).\n'
               ' * SMILES: '
               '[H][C@@]12CC[C@@]3([H])[C@]4([H])CC[C@](O)(C(=O)CO)[C@@]4(C)CC(=O)[C@]3([H])[C@@]1(C)CCC(=O)C2 '
               'NAME: 4,5alpha-dihydrocortisone REASON: CORRECT Steroid '
               'nucleus detected and ketone group is immediately attached to '
               'the nucleus (consistent with 11-oxo steroid).\n'
               ' * SMILES: '
               '[H][C@@]12CC[C@](O)([C@H](O)CO)[C@@]1(C)CC(=O)[C@@]1([H])[C@@]2([H])CCC2=CC(=O)CC[C@]12C '
               'NAME: 20beta-hydroxycortisone REASON: CORRECT Steroid nucleus '
               'detected along with a ketone group on the nucleus (consistent '
               'with 11-oxo steroid).\n'
               ' * SMILES: '
               '[H][C@@]12CC[C@](O)(C(=O)CO)[C@@]1(C)CC(=O)[C@@]1([H])[C@@]2([H])C[C@@H](O)C2=CC(=O)C=C[C@]12C '
               'NAME: 6beta-hydroxyprednisone REASON: CORRECT Steroid nucleus '
               'detected and ketone group is immediately attached to the '
               'nucleus (consistent with 11-oxo steroid).\n'
               ' * SMILES: '
               'O=C1C2=C(C(=O)C[C@@H]3[C@@]2(CCC(C3(C)C)=O)C)[C@@]4(C(=O)C[C@@H]([C@]4(C1)C)C(=C)CCC(=O)OC)C '
               'NAME: Ganodernoid C REASON: CORRECT Steroid nucleus detected '
               'along with a ketone group on the nucleus (consistent with '
               '11-oxo steroid).\n'
               ' * SMILES: '
               '[H][C@@]12CCC3=CC(=O)CC[C@]3(C)[C@@]1([H])C(=O)C[C@@]1(C)[C@@]2([H])CC[C@]1(O)C(=O)CO '
               'NAME: cortisone REASON: CORRECT Steroid nucleus detected along '
               'with a ketone group on the nucleus (consistent with 11-oxo '
               'steroid).\n'
               ' * SMILES: '
               'O=C1C2=C(C(=O)[C@H](O)[C@]3([C@]2(O)C[C@@H]4O[C@H]([C@H]([C@H]34)C)[C@H](O)[C@@H](C(C)C)C)C)[C@]5(CC[C@@H](CC5=C1)O)C '
               'NAME: Asperfloroid REASON: CORRECT Steroid nucleus detected '
               'along with a ketone group on the nucleus (consistent with '
               '11-oxo steroid).\n'
               ' * SMILES: '
               'O=C1C=C2C=CC3=C4[C@]5([C@@H]([C@H](C)[C@@H](C5)[C@@H](O)[C@@H](C(C)C)C)CC4)CC([C@]3([C@@]2(C)CC1)O)=O '
               'NAME: Emesterone B REASON: CORRECT Steroid nucleus detected '
               'along with a ketone group on the nucleus (consistent with '
               '11-oxo steroid).\n'
               ' * SMILES: '
               '[H][C@@]12CCC3CC(=O)CC[C@]3(C)[C@@]1([H])C(=O)C[C@@]1(C)[C@@]2([H])CC[C@]1(O)C(=O)CO '
               'NAME: 4,5-dihydrocortisone REASON: CORRECT Steroid nucleus '
               'detected along with a ketone group on the nucleus (consistent '
               'with 11-oxo steroid).\n'
               ' * SMILES: '
               'C[C@]12CC(=O)[C@H]3[C@@H](CC[C@@H]4C[C@@H](O)CC[C@]34C)[C@@H]1CC(N)=N2 '
               'NAME: RU 5135 REASON: CORRECT Steroid nucleus detected along '
               'with a ketone group on the nucleus (consistent with 11-oxo '
               'steroid).\n'
               ' * SMILES: '
               'O[C@@H]1[C@@]2([C@@]([C@@](C1)([H])[C@@H](C[C@@H](/C=C(/C(=O)O)\\C)O)C)(CC(=O)C3=C2CC[C@@]4([C@@]3(CCC(=O)C4(C)C)C)[H])C)C '
               'NAME: ganolucidic acid D REASON: CORRECT Steroid nucleus '
               'detected along with a ketone group on the nucleus (consistent '
               'with 11-oxo steroid).\n'
               ' * SMILES: '
               '[H][C@@]12CC[C@](O)(C(=O)CO)[C@@]1(C)CC(=O)[C@@]1([H])[C@@]2([H])C=CC2=CC(=O)C=C[C@]12C '
               'NAME: Delta(6)-prednisone REASON: CORRECT Steroid nucleus '
               'detected and ketone group is immediately attached to the '
               'nucleus (consistent with 11-oxo steroid).\n'
               ' * SMILES: '
               'O=C1C2=C([C@@]3(C(=O)C[C@@H]([C@]3(C1)C)C(=C)CCC(=O)O)C)[C@@H](O)C[C@@H]4[C@@]2(CC[C@@H](C4(C)C)O)C '
               'NAME: 20(21)-dehydrolucidenic acid N REASON: CORRECT Steroid '
               'nucleus detected along with a ketone group on the nucleus '
               '(consistent with 11-oxo steroid).\n'
               ' * SMILES: '
               '[H][C@@]12CC[C@](O)(C(=O)CO)[C@@]1(C)CC(=O)[C@@]1([H])[C@@]2([H])C[C@H](O)C2=CC(=O)C=C[C@]12C '
               'NAME: 6alpha-hydroxyprednisone REASON: CORRECT Steroid nucleus '
               'detected and ketone group is immediately attached to the '
               'nucleus (consistent with 11-oxo steroid).\n'
               ' * SMILES: '
               'COC(=O)\\C=C1\\CC[C@H]2[C@@H]3CCC4=CC(=O)CC[C@]4(C)[C@H]3C(=O)C[C@]12C '
               'NAME: (17Z)-3,11-dioxopregna-4,17(20)-dien-21-oic acid methyl '
               'ester REASON: CORRECT Steroid nucleus detected along with a '
               'ketone group on the nucleus (consistent with 11-oxo steroid).\n'
               ' * SMILES: '
               'C1[C@@]2([C@@]([C@@]3(C([C@@H]1O)=CC(CC3)=O)C)(C(C[C@@]4([C@@](CC[C@@]24[H])(O)C(CO)=O)C)=O)[H])[H] '
               'NAME: 6beta-hydroxycortisone REASON: CORRECT Steroid nucleus '
               'detected along with a ketone group on the nucleus (consistent '
               'with 11-oxo steroid).\n'
               'False positives: SMILES: '
               '[H][C@@]12CC(=O)[C@](O)(c3ccc4ccncc4c3)[C@@]1(C)CC=C1C=C3[C@@H](O)[C@H](O)[C@H](C[C@]33CC[C@]21O3)N(C)C '
               'NAME: cortistatin D REASON: WRONGLY CLASSIFIED Steroid nucleus '
               'detected along with a ketone group on the nucleus (consistent '
               'with 11-oxo steroid).\n'
               ' * SMILES: '
               'O=C1C2=C(O)C=3C(=O)C=C(OC)C(C3C=C2C(=O)C4=C1C5=C(C(=O)OC5)C(=C4)OC)=O '
               'NAME: Paramagnetoquinone B REASON: WRONGLY CLASSIFIED Steroid '
               'nucleus detected along with a ketone group on the nucleus '
               '(consistent with 11-oxo steroid).\n'
               ' * SMILES: '
               'C[C@H](CCC(=O)NCCCC(O)=O)[C@H]1CC[C@H]2[C@H]3[C@H](CC[C@]12C)[C@@]4(C)CC[C@@H](O)C[C@H]4CC3=O '
               'NAME: 7-oxo-gamma-aminoisobutyrolithocholic acid REASON: '
               'WRONGLY CLASSIFIED Steroid nucleus detected along with a '
               'ketone group on the nucleus (consistent with 11-oxo steroid).\n'
               ' * SMILES: '
               'O=C1[C@@]2(C=C3C(=O)OC[C@@]43[C@]1([C@H]5O[C@H]6CC(=O)C([C@H]7[C@]6([C@@]5(O)[C@@]4(C2)CC7)C)(C)C)C)C '
               'NAME: Emeridone D REASON: WRONGLY CLASSIFIED Steroid nucleus '
               'detected along with a ketone group on the nucleus (consistent '
               'with 11-oxo steroid).\n'
               ' * SMILES: '
               '[H][C@]12C[C@@]1([H])[C@]1(C)[C@@H](O)C(=O)\\C(=C(\\C)C(=O)OC)[C@@]3([H])C1=C2C[C@@]1([H])[C@@]2(C)[C@]4([H])C[C@]4([H])[C@](O)(C\\C(C)=C\\C(=O)OC)[C@@]2([H])CC2=C(CO)C(=O)O[C@]312 '
               'NAME: shizukaol C REASON: WRONGLY CLASSIFIED Steroid nucleus '
               'detected along with a ketone group on the nucleus (consistent '
               'with 11-oxo steroid).\n'
               ' * SMILES: '
               '[C@@]123[C@@]4([C@]5([C@@](CC1=O)(C(CN([C@H](C2)O)C)=CCO[C@]5(CC(N4C6=C3C=CC=C6)=O)[H])[H])[H])[H] '
               'NAME: 5-hydroxyvomicine REASON: WRONGLY CLASSIFIED Steroid '
               'nucleus detected along with a ketone group on the nucleus '
               '(consistent with 11-oxo steroid).\n'
               ' * SMILES: '
               'O=C1C2=C(O)C3=C(O)C=C(OC)C4=C3C(=C2C5(O)C6(C1(O)C(O)=C(C(=O)C6)C(=O)N)O5)CC74C(=CCCC7(C)C)C '
               'NAME: Viridicatumtoxin B REASON: WRONGLY CLASSIFIED Steroid '
               'nucleus detected along with a ketone group on the nucleus '
               '(consistent with 11-oxo steroid).\n'
               ' * SMILES: '
               'O1[C@]23[C@@]([C@@]4([C@@](OC5=C(C4)C(OC)=C6C(=C5C)COC6=O)(C[C@H]2O)C)[H])([C@H](OC(=O)C)C[C@@]1(OC3(C)C)OC)C '
               'NAME: Austalide D REASON: WRONGLY CLASSIFIED Steroid nucleus '
               'detected and ketone group is immediately attached to the '
               'nucleus (consistent with 11-oxo steroid).\n'
               ' * SMILES: '
               'O=C1C(C2C3(C4(C3)C(C5(C(CC4)(C(CC5)C(CC(O)/C=C(/C)\\C(O)=O)C)C)C)CC2)CC1)(C)C '
               'NAME: 23-Hydroxy-3-oxocycloart-24-en-26-oic acid REASON: '
               'WRONGLY CLASSIFIED Steroid nucleus detected along with a '
               'ketone group on the nucleus (consistent with 11-oxo steroid).\n'
               ' * SMILES: '
               'O=C1[C@@]2([C@]([C@]3([C@@]([C@@]4(C(CC3)=C(O[C@@H]5O[C@@H]([C@@H](O)[C@H](O)[C@H]5O)C(O)=O)C(=O)CC4)C)(CC2)[H])[H])(CC1)[H])C '
               'NAME: 4-Hydroxyandrostenedione glucuronide REASON: WRONGLY '
               'CLASSIFIED Steroid nucleus detected along with a ketone group '
               'on the nucleus (consistent with 11-oxo steroid).\n'
               ' * SMILES: '
               '[H][C@]12C[C@@H](OC(=O)\\C=C\\c3cc(OC)c(OC)c(OC)c3)[C@H](OC)[C@@H](C(=O)OC)[C@@]1([H])C[C@@]1([H])N(CCc3c1[nH]c1cc(OC)ccc31)C2 '
               'NAME: rescinnamine REASON: WRONGLY CLASSIFIED Steroid nucleus '
               'detected and ketone group is immediately attached to the '
               'nucleus (consistent with 11-oxo steroid).\n'
               ' * SMILES: '
               'C/C=C\\1/C2CC[N@+]3(CC[C@]4(C5=CC=CC=C5NC4=C2C(=O)OC)[C@@]13[H])[O-] '
               'NAME: Condylocarpine N-oxide REASON: WRONGLY CLASSIFIED '
               'Steroid nucleus detected and ketone group is immediately '
               'attached to the nucleus (consistent with 11-oxo steroid).\n'
               ' * SMILES: '
               'CC(=O)OCC(=O)[C@H]1CC[C@H]2C3=CC=C4C[C@H](CC[C@]4(C)C3=CC[C@]12C)OC(C)=O '
               'NAME: 3beta,21-Dihydroxy-pregna-5,7,9(11)-trien-20-one '
               'diacetate REASON: WRONGLY CLASSIFIED Steroid nucleus detected '
               'and ketone group is immediately attached to the nucleus '
               '(consistent with 11-oxo steroid).\n'
               ' * SMILES: '
               'O=C1[C@@]2([C@@]3([C@H](/C(=C(/C(=O)O)\\CCC=C(C)C)/[C@H](C3)OC(=O)C)CC[C@H]2[C@]4(CCC([C@H]([C@@H]4[C@@H]1OC(=O)C)C)=O)C)C)C '
               'NAME: 1,2-Dihydrohelvolic acid REASON: WRONGLY CLASSIFIED '
               'Steroid nucleus detected along with a ketone group on the '
               'nucleus (consistent with 11-oxo steroid).\n'
               ' * SMILES: '
               'CC(=O)[C@H]1CC[C@H]2[C@@H]3C[C@H]4OC[C@@]5(CCC(=O)C=C45)[C@H]3CC[C@]12C '
               'NAME: 6beta,19-Epoxypregn-4-ene-3,20-dione REASON: WRONGLY '
               'CLASSIFIED Steroid nucleus detected and ketone group is '
               'immediately attached to the nucleus (consistent with 11-oxo '
               'steroid).\n'
               ' * SMILES: '
               'O=C1C(C2=CC=C3[C@]4([C@]([C@@H]([C@H](C(=O)O)CCC(=C)C(C)C)[C@@H](C4)O)(C)CC=C3[C@@]2(C)CC1)C)(C)C '
               'NAME: '
               '16alpha-hydroxy-3-oxo-24-methyllanosta-5,7,9(11),24(31)-tetraen-21-oic '
               'acid REASON: WRONGLY CLASSIFIED Steroid nucleus detected along '
               'with a ketone group on the nucleus (consistent with 11-oxo '
               'steroid).\n'
               ' * SMILES: '
               'C1C[C@@H](C([C@@]2([C@@]1([C@]3([C@](CC2)([C@]4([C@@](C(=C3)C)(C(C(=C4O)C)=O)C)C(OC)=O)C)[H])CO)[H])(C)C)OC(C)=O '
               'NAME: andrastin B REASON: WRONGLY CLASSIFIED Steroid nucleus '
               'detected and ketone group is immediately attached to the '
               'nucleus (consistent with 11-oxo steroid).\n'
               ' * SMILES: '
               'CC(C)C[C@H]1C2=C(C[C@@H]3N1C(=O)[C@@H](NC3=O)CCC(=O)OC(C)(C)C)C4=C(N2)C=C(C=C4)OC '
               'NAME: LSM-6260 REASON: WRONGLY CLASSIFIED Steroid nucleus '
               'detected along with a ketone group on the nucleus (consistent '
               'with 11-oxo steroid).\n'
               ' * SMILES: '
               'O=C1C=C2C(=C(O)C[C@@H]3[C@@]2(CCC(C3(C)C)=O)C)[C@]4([C@]1(C(=CC4=O)[C@@](O)(CC(=O)C[C@@H](C(=O)O)C)C)C)C '
               'NAME: Applanoic acid D REASON: WRONGLY CLASSIFIED Steroid '
               'nucleus detected along with a ketone group on the nucleus '
               '(consistent with 11-oxo steroid).\n'
               ' * SMILES: '
               'O=C1C(C2C(C3=C(C4(C(C(CC4)C(CC/C=C(\\C)/C(O)=O)C)(CC3)C)C)CC2)(CC1)C)(C)C '
               'NAME: Isomasticadienonic acid REASON: WRONGLY CLASSIFIED '
               'Steroid nucleus detected along with a ketone group on the '
               'nucleus (consistent with 11-oxo steroid).\n'
               ' * SMILES: '
               'O=C1C(OC)=C(C(=O)C=2C1=C(O)C3=C(C(=O)C4(O)C5C3OC4(C(O[C@@H]6O[C@@H]([C@@H](O[C@H]7O[C@@H]([C@@](O)(C(=O)C)[C@H](C7)O)C)CC6)C)C(C5OC8O[C@H]([C@H](O)[C@@H](C8)O)C)O)CCC)C2O)C=9C(OC)=C(OC)C%10=CC=%11CC%12C(O[C@@H]%13O[C@H]([C@H](O)[C@@H](C%13)O)C)C(O)C(C(C%12(C(C%11C(=C%10C9O)O)=O)O)(O)CCC)O[C@@H]%14O[C@@H]([C@@H](O[C@H]%15O[C@@H]([C@@](O)(C(=O)C)[C@H](C%15)O)C)CC%14)C '
               'NAME: Hibarimicin G REASON: WRONGLY CLASSIFIED Steroid nucleus '
               'detected along with a ketone group on the nucleus (consistent '
               'with 11-oxo steroid).\n'
               ' * SMILES: '
               'O=C1N2C(OC(C2(CO)C)=O)(CC=3C1=C(O)C4=C5C(=O)C6=C(OC=7C=C(OC)C(=CC7C6=O)OC)C(C5=CC=C4C3)=O)C '
               'NAME: Citreamicin n REASON: WRONGLY CLASSIFIED Steroid nucleus '
               'detected along with a ketone group on the nucleus (consistent '
               'with 11-oxo steroid).\n'
               ' * SMILES: '
               'O=C1C2=C([C@@]3([C@@H](O)C[C@@H]([C@]3(C1)C)[C@@H](CC(O)C=C(C(=O)O)C)C)C)[C@@H](O)CC4[C@@]2(CC[C@@H](C4(C)C)O)C '
               'NAME: Ganolucidic acid gamma a REASON: WRONGLY CLASSIFIED '
               'Steroid nucleus detected along with a ketone group on the '
               'nucleus (consistent with 11-oxo steroid).\n'
               ' * SMILES: '
               'OC12C(C3(C(C4(C(CC3)C(C(=O)CC4)(C)C)C)CC1)C)(CC5OC(CC(C25O)C)C(O)C(O)(C)C)C '
               'NAME: '
               '6-(1,2-dihydroxy-2-methylpropyl)-9,10-dihydroxy-1,2,8,14,18,18-hexamethyl-5-oxapentacyclo[11.8.0.02,10.04,9.014,19]henicosan-17-one '
               'REASON: WRONGLY CLASSIFIED Steroid nucleus detected along with '
               'a ketone group on the nucleus (consistent with 11-oxo '
               'steroid).\n'
               ' * SMILES: '
               'O=C1O[C@@]2(C(=C[C@@H]3O[C@](C[C@@]3(C2)O)(OC)C(=O)OC)C=4C1=C(O)C=C(OC)C4)C '
               'NAME: Xinshengin REASON: WRONGLY CLASSIFIED Steroid nucleus '
               'detected and ketone group is immediately attached to the '
               'nucleus (consistent with 11-oxo steroid).\n'
               'False negatives: SMILES: '
               '[H][C@]12CC[C@@]3([H])[C@]4([H])CCC\\C(=C/CO)[C@@]4(C)CC(=O)[C@]3([H])[C@@]1(C)CC[C@@H](O)C2 '
               'NAME: 3alpha,21-dihydroxy-D-homo-5beta-pregn-17a(20)-en-11-one '
               'REASON: MISSED No steroid nucleus (4 fused rings with '
               'appropriate sizes) found.\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'O=C(N[C@@H](C(O)(C)C)C)[C@H]([C@@]1([C@@]2([C@@](CC1)(/C(/CCC2)=C/C=C\\3/C[C@@H](O)C[C@H](O)C3=C)[H])C)[H])C',
                                     'name': '1alpha,25-dihydroxy-24-oxo-23-azavitamin '
                                             'D2 / '
                                             '1alpha,25-dihydroxy-24-oxo-23-azaergocalciferol',
                                     'reason': 'Not enough 5- or 6-membered '
                                               'rings to form a steroid '
                                               'nucleus.'},
                                 {   'smiles': 'CCCCCCCCCCCCCCCCCCC(O)C([O-])=O',
                                     'name': '2-hydroxyarachidate',
                                     'reason': 'Not enough 5- or 6-membered '
                                               'rings to form a steroid '
                                               'nucleus.'},
                                 {   'smiles': 'C[C@@H](CN([C@@H](C)CO)C(=O)NC1=CC=C(C=C1)C(F)(F)F)[C@@H](CN(C)C(=O)C2CCOCC2)OC',
                                     'name': 'N-[(2S,3S)-4-[[(2S)-1-hydroxypropan-2-yl]-[[4-(trifluoromethyl)phenyl]carbamoyl]amino]-2-methoxy-3-methylbutyl]-N-methyloxane-4-carboxamide',
                                     'reason': 'Not enough 5- or 6-membered '
                                               'rings to form a steroid '
                                               'nucleus.'},
                                 {   'smiles': 'CC(=O)CC\\C=C(/C)CCC=C(C)C',
                                     'name': 'geranyl acetone',
                                     'reason': 'Not enough 5- or 6-membered '
                                               'rings to form a steroid '
                                               'nucleus.'},
                                 {   'smiles': 'O([C@H]1[C@H](O)[C@H](O[C@H](O)[C@H]1O)CO[C@H]2O[C@@H]([C@@H](O)[C@H](O)[C@@H]2O)CO)[C@H]3O[C@@H]([C@@H](O)[C@H](O)[C@@H]3O[C@H]4O[C@@H]([C@@H](O)[C@H](O)[C@@H]4O)CO)CO',
                                     'name': '(2S,3S,4S,5S,6R)-2-[[(2R,3R,4S,5S,6S)-4-[(2R,3S,4S,5S,6R)-4,5-Dihydroxy-6-(hydroxymethyl)-3-[(2R,3S,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-3,5,6-trihydroxyoxan-2-yl]methoxy]-6-(hydroxymethyl)oxane-3,4,5-triol',
                                     'reason': 'No steroid nucleus (4 fused '
                                               'rings with appropriate sizes) '
                                               'found.'},
                                 {   'smiles': 'O=C(OC1=C(C(O)=C(C(=O)O)C(=C1C)C)C)C2=C(OC)C(=C(OC(=O)C3=C(O)C=C(O)C=C3C)C=C2C)C',
                                     'name': 'Thielavin Z5',
                                     'reason': 'Not enough 5- or 6-membered '
                                               'rings to form a steroid '
                                               'nucleus.'},
                                 {   'smiles': '[C@@H]1([C@@H]([C@H]([C@@H]([C@H](O1)CO)O)O)NC(C)=O)O[C@@H]2[C@@H]([C@H](C(O[C@@H]2CO)O)O)O',
                                     'name': 'beta-D-GlcpNAc-(1->4)-D-Galp',
                                     'reason': 'Not enough 5- or 6-membered '
                                               'rings to form a steroid '
                                               'nucleus.'},
                                 {   'smiles': 'CN(C)C(=O)C1=CC=C(C=C1)C2=CC=C(C=C2)[C@@H]3[C@H]4CN(CC(=O)N4[C@H]3CO)C(=O)CC5CC5',
                                     'name': '4-[4-[(6S,7R,8R)-4-(2-cyclopropyl-1-oxoethyl)-8-(hydroxymethyl)-2-oxo-1,4-diazabicyclo[4.2.0]octan-7-yl]phenyl]-N,N-dimethylbenzamide',
                                     'reason': 'Not enough 5- or 6-membered '
                                               'rings to form a steroid '
                                               'nucleus.'},
                                 {   'smiles': 'CCCCCCCCCCCCCCCCCCCCC=C',
                                     'name': '1-docosene',
                                     'reason': 'Not enough 5- or 6-membered '
                                               'rings to form a steroid '
                                               'nucleus.'},
                                 {   'smiles': 'C([C@@](OC(=O)CCC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)([H])COC(=O)CC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)OC(=O)CCCCC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC',
                                     'name': 'TG(22:5(7Z,10Z,13Z,16Z,19Z)/20:5(5Z,8Z,11Z,14Z,17Z)/22:6(4Z,7Z,10Z,13Z,16Z,19Z))[iso6]',
                                     'reason': 'Not enough 5- or 6-membered '
                                               'rings to form a steroid '
                                               'nucleus.'}],
    'sample_false_negatives': [   {   'smiles': '[H][C@]12CC[C@@]3([H])[C@]4([H])CCC\\C(=C/CO)[C@@]4(C)CC(=O)[C@]3([H])[C@@]1(C)CC[C@@H](O)C2',
                                      'name': '3alpha,21-dihydroxy-D-homo-5beta-pregn-17a(20)-en-11-one',
                                      'reason': 'No steroid nucleus (4 fused '
                                                'rings with appropriate sizes) '
                                                'found.'},
                                  {   'smiles': 'O=C1[C@@H]2[C@@]([C@]34CC[C@]([C@H](C[C@@H]3C1)C4)(O)CO)(CC[C@@H]5[C@]2(COC(O5)(C)C)C)C',
                                      'name': 'Aphidicolin A3',
                                      'reason': 'Ketone group not located on '
                                                'or adjacent to the steroid '
                                                "nucleus's key ring (likely "
                                                'not a true 11-oxo steroid).'}],
    'attempt': 3,
    'reasoning': 'Below is our reasoning and then the full program in one '
                 'Python code block.\n'
                 '\n'
                 '─────────────────────────────\n'
                 '\n'
                 'We observed that our previous approach was catching many '
                 'steroids that do have a ketone group but sometimes in the '
                 '“wrong” position (false‐positives) and was also missing a '
                 'steroid nucleus in some cases (false‐negatives). In our '
                 'revised approach we (1) still search for four fused rings '
                 '(three 6‐membered and one 5‐membered) but relax the allowed '
                 'union‐atom count a bit and (2) try to “localize” the '
                 'expected 11‐oxo position by first identifying the 5‐membered '
                 'ring (which in steroids is the D ring) and then selecting '
                 'among the six‐membered rings the one that is fused to it '
                 '(the C ring, where the C11 position is normally located). '
                 'Then we only accept a ketone group if its carbonyl carbon is '
                 'either part of that “key” six‐membered ring or is '
                 'immediately attached to it. We hope that this improved '
                 'heuristic reduces false positives (when a ketone is on a '
                 'different region) and false negatives (by slightly relaxing '
                 'the nucleus criteria).\n'
                 '\n'
                 '─────────────────────────────\n'
                 '\n'
                 'Below is the complete Python code:',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 30,
    'num_false_positives': 2177,
    'num_true_negatives': 140091,
    'num_false_negatives': 2,
    'num_negatives': None,
    'precision': 0.01359311282283643,
    'recall': 0.9375,
    'f1': 0.026797677534613668,
    'accuracy': 0.9846872803935348,
    'negative_predictive_value': 0.9999857237692105}