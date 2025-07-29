"""
Classifies: CHEBI:15889 sterol
"""
#!/usr/bin/env python
"""
Classifies: Sterol
Definition: Any 3-hydroxy steroid whose skeleton is closely related to cholestan-3-ol.
This implementation:
  1. Parses the SMILES and adds explicit hydrogens.
  2. Retrieves the ring information from RDKit.
  3. Groups ring atoms into fused components.
  4. For each fused component, iterates over all combinations of 4 rings.
     For a candidate steroid nucleus the four rings should have sizes [5,6,6,6] when sorted,
     the union (candidate nucleus) should have between 16 and 19 carbon atoms, and—importantly—
     the four rings must be fused in a steroid‐like pattern. This connectivity is verified by
     requiring that exactly three pairs of rings (out of six possible pairings) share at least
     2 atoms and that the resulting graph (with rings as nodes and fused pairs as edges) is connected.
  5. Finally, at least one carbon in the candidate steroid nucleus must bear an external –OH group.
If all these conditions are met, returns True with explanation; otherwise False.
"""

from rdkit import Chem
from rdkit.Chem import rdMolDescriptors
import itertools

def is_sterol(smiles: str):
    """
    Determines if a molecule is a sterol (a 3-hydroxy steroid) based on its SMILES string.
    
    The algorithm:
       1. Parse the SMILES, and add explicit hydrogens.
       2. Obtain ring information and group rings into fused (connected) components using ring bonds.
       3. For each fused component, consider all combinations of four rings. For each combination:
             a. Check that the sorted ring sizes equal [5,6,6,6].
             b. Compute the union of atoms in these rings and count carbon atoms in it.
                The classical steroid nucleus is expected to have between 16 and 19 carbons.
             c. Verify that the four rings are fused in the proper steroid‐like connectivity.
                We require that exactly three pairs of rings (out of the six possible pairs) share
                at least 2 atoms and that the connectivity graph is connected (i.e. it forms a tree).
             d. Check that at least one carbon of the nucleus is attached to a hydroxyl group –
                that is, an oxygen (with at least one hydrogen) that is not part of the nucleus.
       4. If such a valid candidate is found, return True with an explanation;
          otherwise return False and the most relevant reason.
          
    Args:
        smiles (str): SMILES string of the molecule.
    
    Returns:
        bool: True if classified as a sterol, False otherwise.
        str: Explanation for the decision.
    """
    
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
    
    # Adding explicit hydrogens will help in detecting hydroxyl groups.
    mol = Chem.AddHs(mol)
    
    ring_info = mol.GetRingInfo()
    all_rings = ring_info.AtomRings()
    if not all_rings:
        return False, "No ring system present; cannot be a sterol"
    
    # Get a set of all atom indices that are in some ring.
    ring_atom_idxs = {atom.GetIdx() for atom in mol.GetAtoms() if atom.IsInRing()}
    
    # Build a graph among ring atoms using bonds that are in rings.
    ring_graph = {idx: set() for idx in ring_atom_idxs}
    for bond in mol.GetBonds():
        if bond.IsInRing():
            i1 = bond.GetBeginAtomIdx()
            i2 = bond.GetEndAtomIdx()
            if i1 in ring_graph and i2 in ring_graph:
                ring_graph[i1].add(i2)
                ring_graph[i2].add(i1)
                
    # Find fused (i.e. connected) groups of ring atoms.
    visited = set()
    fused_components = []
    for idx in ring_atom_idxs:
        if idx not in visited:
            comp = set()
            stack = [idx]
            while stack:
                current = stack.pop()
                if current not in visited:
                    visited.add(current)
                    comp.add(current)
                    stack.extend(ring_graph[current] - visited)
            fused_components.append(comp)
    
    candidate_found = False
    candidate_reason = ""
    
    # Go through each fused component and try to find a valid steroid nucleus candidate.
    for comp in fused_components:
        # Select rings completely contained in this fused component.
        comp_rings = [set(r) for r in all_rings if set(r).issubset(comp)]
        if len(comp_rings) < 4:
            continue  # Need at least four rings.
        
        # Iterate over all combinations of four rings.
        for four_rings in itertools.combinations(comp_rings, 4):
            sizes = sorted([len(r) for r in four_rings])
            # Check for classical steroid nucleus: one five-membered and three six-membered rings.
            if sizes != [5, 6, 6, 6]:
                continue
            
            # Connectivity check: there are 4 rings; expect that exactly 3 pairs share at least 2 atoms,
            # and the connectivity graph (rings as nodes, edge if intersection >=2) should be connected.
            edges = []
            for i, j in itertools.combinations(range(4), 2):
                inter = four_rings[i] & four_rings[j]
                if len(inter) >= 2:
                    edges.append((i, j))
            if len(edges) != 3:
                continue  # Not the steroid-like fusion pattern.
            # Build a graph from these four rings and check connectivity.
            conn_graph = {i: set() for i in range(4)}
            for i, j in edges:
                conn_graph[i].add(j)
                conn_graph[j].add(i)
            # Check connectivity by simple DFS.
            stack = [0]
            seen = set()
            while stack:
                node = stack.pop()
                if node not in seen:
                    seen.add(node)
                    stack.extend(conn_graph[node] - seen)
            if len(seen) != 4:
                continue
            
            # Now, candidate nucleus is the union of the four rings.
            nucleus = set().union(*four_rings)
            num_carbons = sum(1 for idx in nucleus if mol.GetAtomWithIdx(idx).GetAtomicNum() == 6)
            if not (16 <= num_carbons <= 19):
                continue
            
            # Look for an external hydroxyl group.
            hydroxyl_found = False
            for atom_idx in nucleus:
                atom = mol.GetAtomWithIdx(atom_idx)
                if atom.GetAtomicNum() != 6:  # Only consider nucleus carbons.
                    continue
                for nbr in atom.GetNeighbors():
                    # External oxygen (not in the nucleus) with at least one hydrogen.
                    if nbr.GetAtomicNum() == 8 and nbr.GetIdx() not in nucleus:
                        if any(n.GetAtomicNum() == 1 for n in nbr.GetNeighbors()):
                            hydroxyl_found = True
                            break
                if hydroxyl_found:
                    break
            
            if hydroxyl_found:
                candidate_found = True
                candidate_reason = ("Found fused steroid nucleus (4 rings with sizes [5,6,6,6] and "
                                    f"approximately {num_carbons} carbons) with an externally attached hydroxyl")
                break  # Found a valid candidate.
            else:
                candidate_reason = ("Fused ring system candidate found with four rings ([5,6,6,6] and ~"
                                    f"{num_carbons} carbons) but missing an attached hydroxyl group")
        if candidate_found:
            break

    if candidate_found:
        return True, candidate_reason
    else:
        if candidate_reason:
            return False, candidate_reason
        else:
            return False, "No steroid nucleus identified with the required ring pattern"

# Example usage (for testing):
if __name__ == "__main__":
    # Test with one known sterol: (25R)-3beta,4beta-dihydroxycholest-5-en-26-oic acid
    test_smiles = "C[C@H](CCC[C@@H](C)C(O)=O)[C@H]1CC[C@H]2[C@@H]3CC=C4[C@@H](O)[C@@H](O)CC[C@]4(C)[C@H]3CC[C@]12C"
    result, explanation = is_sterol(test_smiles)
    print("Is sterol:", result)
    print("Reason:", explanation)


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:15889',
                          'name': 'sterol',
                          'definition': 'Any 3-hydroxy steroid whose skeleton '
                                        'is closely related to cholestan-3-ol '
                                        '(additional carbon atoms may be '
                                        'present in the side chain).',
                          'parents': ['CHEBI:36834'],
                          'xrefs': [   'KEGG:C00370',
                                       'LIPID_MAPS_class:LMST01',
                                       'MetaCyc:Sterols',
                                       'Wikipedia:Sterol'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 135,
                           'log_lines_of_code': 4.90527477843843,
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
                                                 3,
                                                 3,
                                                 3,
                                                 4,
                                                 4,
                                                 4,
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
                                                 5,
                                                 3,
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
                                                 3,
                                                 3,
                                                 4,
                                                 3,
                                                 3,
                                                 3,
                                                 3,
                                                 3,
                                                 4,
                                                 4,
                                                 5,
                                                 3,
                                                 4,
                                                 3,
                                                 3,
                                                 3,
                                                 4,
                                                 4,
                                                 3,
                                                 3,
                                                 3,
                                                 3,
                                                 4,
                                                 4,
                                                 5,
                                                 5,
                                                 3,
                                                 4,
                                                 3,
                                                 3,
                                                 3,
                                                 3,
                                                 3,
                                                 4,
                                                 3,
                                                 3,
                                                 3,
                                                 3,
                                                 4,
                                                 4,
                                                 5,
                                                 4,
                                                 5,
                                                 5,
                                                 6,
                                                 7,
                                                 7,
                                                 4,
                                                 5,
                                                 3,
                                                 3,
                                                 4,
                                                 4,
                                                 4,
                                                 4,
                                                 3,
                                                 4,
                                                 4,
                                                 2,
                                                 3,
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
                                                 1],
                           'max_indent': 7,
                           'imports': [   'from rdkit import Chem',
                                          'from rdkit.Chem import '
                                          'rdMolDescriptors',
                                          'import itertools'],
                           'imports_count': 3,
                           'methods_called': [   'MolFromSmiles',
                                                 'AddHs',
                                                 'IsInRing',
                                                 'GetAtomWithIdx',
                                                 'extend',
                                                 'issubset',
                                                 'pop',
                                                 'GetAtomicNum',
                                                 'add',
                                                 'GetIdx',
                                                 'GetBeginAtomIdx',
                                                 'append',
                                                 'GetEndAtomIdx',
                                                 'combinations',
                                                 'GetAtoms',
                                                 'GetRingInfo',
                                                 'AtomRings',
                                                 'GetBonds',
                                                 'union',
                                                 'GetNeighbors'],
                           'methods_called_count': 20,
                           'smarts_strings': [],
                           'smarts_strings_count': 0,
                           'defs': ['is_sterol(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "No ring system present; '
                                          'cannot be a sterol"',
                                          'True, candidate_reason',
                                          'False, candidate_reason',
                                          'False, "No steroid nucleus '
                                          'identified with the required ring '
                                          'pattern"'],
                           'returns_count': 5,
                           'complexity': 7.581054955687685},
    'message': '\n'
               'Attempt failed: F1 score of 0.04691191360107999 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: '
               'C[C@H](CCC[C@@H](C)C(O)=O)[C@H]1CC[C@H]2[C@@H]3CC=C4[C@@H](O)[C@@H](O)CC[C@]4(C)[C@H]3CC[C@]12C '
               'NAME: (25R)-3beta,4beta-dihydroxycholest-5-en-26-oic acid '
               'REASON: CORRECT Found fused steroid nucleus (4 rings with '
               'sizes [5,6,6,6] and approximately 17 carbons) with an '
               'externally attached hydroxyl\n'
               ' * SMILES: '
               'CC(C)CCC[C@@H](C)[C@H]1CC[C@H]2C3=C(CC[C@]12C)[C@@]1(C)CC[C@H](O)[C@@](C)(CO)[C@@H]1CC3 '
               'NAME: '
               '4alpha-hydroxymethyl-4beta-methyl-5alpha-8-cholesten-3beta-ol '
               'REASON: CORRECT Found fused steroid nucleus (4 rings with '
               'sizes [5,6,6,6] and approximately 17 carbons) with an '
               'externally attached hydroxyl\n'
               ' * SMILES: '
               'CC(C)CCC[C@@H](C)[C@H]1CC[C@@]2(C=O)C3=C(CC[C@]12C)[C@@]1(C)CC[C@H](O)C(C)(C)[C@@H]1CC3 '
               'NAME: 3beta-hydroxylanost-8-en-32-al REASON: CORRECT Found '
               'fused steroid nucleus (4 rings with sizes [5,6,6,6] and '
               'approximately 17 carbons) with an externally attached '
               'hydroxyl\n'
               ' * SMILES: '
               '[H][C@@]1(CC[C@@]2([H])[C@]3([H])CC=C4C[C@@H](O)CC[C@]4(C)[C@@]3([H])CC[C@]12C)[C@H](C)[C@@H](O)CCC(C)C '
               'NAME: (22S)-22-hydroxycholesterol REASON: CORRECT Found fused '
               'steroid nucleus (4 rings with sizes [5,6,6,6] and '
               'approximately 17 carbons) with an externally attached '
               'hydroxyl\n'
               ' * SMILES: '
               'C1[C@@]2([C@]3(CC[C@]4([C@]([C@@]3(C(C=C2C[C@H](C1)O)=O)[H])(CC[C@@]4([C@H](C)CCCC(C)(C)O)[H])[H])C)[H])C '
               'NAME: 7-keto-25-hydroxycholesterol REASON: CORRECT Found fused '
               'steroid nucleus (4 rings with sizes [5,6,6,6] and '
               'approximately 17 carbons) with an externally attached '
               'hydroxyl\n'
               ' * SMILES: '
               '[H][C@@]1(CC[C@@]2([H])[C@]3([H])[C@H](O)C=C4C[C@@H](O)CC[C@]4(C)[C@@]3([H])CC[C@]12C)[C@H](C)CCCC(C)C '
               'NAME: 7alpha-hydroxycholesterol REASON: CORRECT Found fused '
               'steroid nucleus (4 rings with sizes [5,6,6,6] and '
               'approximately 17 carbons) with an externally attached '
               'hydroxyl\n'
               ' * SMILES: '
               '[H][C@@]12CC=C3C[C@@H](O)CC[C@]3(C)[C@@]1([H])CC[C@@]1(C)[C@@]2([H])CC[C@]1([H])[C@@](C)(O)\\C=C\\[C@@H](CC)C(C)C '
               'NAME: leucisterol REASON: CORRECT Found fused steroid nucleus '
               '(4 rings with sizes [5,6,6,6] and approximately 17 carbons) '
               'with an externally attached hydroxyl\n'
               ' * SMILES: '
               'C[C@H](CC[C@@H]1OC1(C)C)[C@H]1CC[C@H]2[C@@H]3[C@H](O)C=C4C[C@@H](O)CC[C@]4(C)[C@H]3CC[C@]12C '
               'NAME: (24S,25)-epoxy-7alpha-hydroxycholesterol REASON: CORRECT '
               'Found fused steroid nucleus (4 rings with sizes [5,6,6,6] and '
               'approximately 17 carbons) with an externally attached '
               'hydroxyl\n'
               ' * SMILES: '
               '[H][C@@]1(CC[C@@]2([H])[C@]3([H])CC=C4C[C@@H](O)CC[C@]4(C)[C@@]3([H])CC[C@]12C)[C@H](C)CCCC(C)(C)O '
               'NAME: 25-hydroxycholesterol REASON: CORRECT Found fused '
               'steroid nucleus (4 rings with sizes [5,6,6,6] and '
               'approximately 17 carbons) with an externally attached '
               'hydroxyl\n'
               ' * SMILES: '
               'O([C@@]1(C(C=2[C@@]([C@@]3(C([C@]4([C@@]([C@](C(C4([H])[H])([H])[H])([C@](C([H])([H])[H])(/C(=C(/[C@](C(C([H])([H])[H])(C([H])([H])[H])[H])(C(C([H])([H])[H])([H])[H])[H])\\[H])/[H])[H])[H])(C(C3([H])[H])([H])[H])C([H])([H])[H])[H])=C(C2[H])[H])[H])(C(C1([H])[H])([H])[H])C([H])([H])[H])([H])[H])[H])[H] '
               'NAME: delta7-stigmasterol REASON: CORRECT Found fused steroid '
               'nucleus (4 rings with sizes [5,6,6,6] and approximately 17 '
               'carbons) with an externally attached hydroxyl\n'
               ' * SMILES: '
               '[H][C@@]1(CC[C@@]2([H])[C@]3([H])C[C@@H]4O[C@@]44C[C@@H](O)CC[C@]4(C)[C@@]3([H])CC[C@]12C)[C@H](C)CCCC(C)C '
               'NAME: 5,6alpha-epoxy-5alpha-cholestan-3beta-ol REASON: CORRECT '
               'Found fused steroid nucleus (4 rings with sizes [5,6,6,6] and '
               'approximately 17 carbons) with an externally attached '
               'hydroxyl\n'
               ' * SMILES: '
               'C1[C@@]2([C@]3(CC[C@]4([C@]([C@@]3(C(C=C2C[C@H](C1)O)=O)[H])(CC[C@@]4([C@H](C)CCC[C@@H](C)C(O)=O)[H])[H])C)[H])C '
               'NAME: (25R)-3beta-hydroxycholest-5-en-7-one-26-oic acid '
               'REASON: CORRECT Found fused steroid nucleus (4 rings with '
               'sizes [5,6,6,6] and approximately 17 carbons) with an '
               'externally attached hydroxyl\n'
               ' * SMILES: '
               '[H][C@@]1(CC[C@@]2([H])C3=CC[C@@]4([H])C[C@@H](O)CC[C@]4(C)[C@@]3([H])CC[C@]12C)[C@H](C)CC\\C(=C\\C)C(C)C '
               'NAME: avenasterol REASON: CORRECT Found fused steroid nucleus '
               '(4 rings with sizes [5,6,6,6] and approximately 17 carbons) '
               'with an externally attached hydroxyl\n'
               ' * SMILES: '
               'CC(C)CCC[C@@H](C)[C@H]1CC[C@H]2C3=C(CC[C@]12C)[C@@]1(C)CC[C@H](O)C(C)(C)[C@@H]1CC3 '
               'NAME: 4,4-dimethyl-5alpha-cholest-8-en-3beta-ol REASON: '
               'CORRECT Found fused steroid nucleus (4 rings with sizes '
               '[5,6,6,6] and approximately 17 carbons) with an externally '
               'attached hydroxyl\n'
               ' * SMILES: '
               'C1[C@@]2(C=3CC[C@]4([C@](C3CC[C@]2(C([C@H](C1)O)(C)C)[H])(CC[C@@]4([C@H](C)CC/C=C(\\C)/C([O-])=O)[H])C)C)C '
               'NAME: 3beta-hydroxy-lanosta-8, 24-dien-26-oate REASON: CORRECT '
               'Found fused steroid nucleus (4 rings with sizes [5,6,6,6] and '
               'approximately 17 carbons) with an externally attached '
               'hydroxyl\n'
               ' * SMILES: '
               'C1=C2[C@@]3(CC[C@@]([C@]3(CC[C@@]2([C@]4(CC[C@H](O)[C@H]([C@@]4(C1)[H])CO)C)[H])C)([C@@H](CCCC(C)C)C)[H])[H] '
               'NAME: 4alpha-hydroxymethyl-5alpha-cholest-7-en-3beta-ol '
               'REASON: CORRECT Found fused steroid nucleus (4 rings with '
               'sizes [5,6,6,6] and approximately 17 carbons) with an '
               'externally attached hydroxyl\n'
               ' * SMILES: '
               'CC(C)C(=C)CC[C@@H](C)[C@H]1CC[C@H]2C3=C(CC[C@]12C)[C@@]1(C)CC[C@H](O)C(C)(C)[C@@H]1CC3 '
               'NAME: 4,4-dimethyl-5alpha-ergosta-8,24(28)-dien-3beta-ol '
               'REASON: CORRECT Found fused steroid nucleus (4 rings with '
               'sizes [5,6,6,6] and approximately 17 carbons) with an '
               'externally attached hydroxyl\n'
               ' * SMILES: '
               '[H][C@@]12CC=C3C(CC[C@]4(C)[C@]([H])(CC[C@@]34[H])[C@H](C)CCC(=C)C(C)C)[C@@]1(C)CC[C@H](O)C2 '
               'NAME: 9xi-episterol REASON: CORRECT Found fused steroid '
               'nucleus (4 rings with sizes [5,6,6,6] and approximately 17 '
               'carbons) with an externally attached hydroxyl\n'
               ' * SMILES: '
               'CC(C)CCC[C@@H](C)[C@H]1CC[C@H]2C3=C(CC[C@]12C)[C@@]1(C)CC[C@H](O)[C@@H](C=O)[C@@H]1CC3 '
               'NAME: 4alpha-formyl-5alpha-cholest-8-en-3beta-ol REASON: '
               'CORRECT Found fused steroid nucleus (4 rings with sizes '
               '[5,6,6,6] and approximately 17 carbons) with an externally '
               'attached hydroxyl\n'
               ' * SMILES: '
               '[C@]123[C@@]4([C@]([C@@]([C@@H](O)CC4)(C=O)C)(CC[C@]1([C@]5(C)CC[C@@]([C@@]5(C)CC2)([C@@H](CCC(C(C)C)=C)C)[H])[H])[H])C3 '
               'NAME: '
               '3beta-hydroxy-24-methylene-9beta-9,19-cyclolanostan-28-al '
               'REASON: CORRECT Found fused steroid nucleus (4 rings with '
               'sizes [5,6,6,6] and approximately 17 carbons) with an '
               'externally attached hydroxyl\n'
               ' * SMILES: '
               'C1[C@@]2(C=3CC[C@]4([C@](C3CC[C@]2(C([C@H](C1)O)(C)C)[H])(CC[C@@]4([C@H](C)CCC(C(C)C)=C)[H])C)C)C '
               'NAME: eburicol REASON: CORRECT Found fused steroid nucleus (4 '
               'rings with sizes [5,6,6,6] and approximately 17 carbons) with '
               'an externally attached hydroxyl\n'
               ' * SMILES: '
               'CC(C)CCC[C@@H](C)[C@H]1CC[C@H]2[C@@H]3CC=C4[C@@H](O)[C@@H](O)CC[C@]4(C)[C@H]3CC[C@]12C '
               'NAME: 4beta-hydroxycholesterol REASON: CORRECT Found fused '
               'steroid nucleus (4 rings with sizes [5,6,6,6] and '
               'approximately 17 carbons) with an externally attached '
               'hydroxyl\n'
               ' * SMILES: '
               '[H][C@@]12C[C@H](O)[C@]([H])([C@H](C)C(=O)CCC(C)C)[C@@]1(C)CC[C@@]1([H])[C@@]2([H])CC=C2C[C@@H](O)CC[C@]12C '
               'NAME: (16S)-hydroxy-22-oxocholesterol REASON: CORRECT Found '
               'fused steroid nucleus (4 rings with sizes [5,6,6,6] and '
               'approximately 17 carbons) with an externally attached '
               'hydroxyl\n'
               ' * SMILES: '
               '[H][C@@]1(CC[C@@]2([H])[C@]3([H])CC=C4C[C@@H](O)CC[C@]4(C)[C@@]3([H])CC[C@]12C)[C@H](C)CCC=C(C)C '
               'NAME: desmosterol REASON: CORRECT Found fused steroid nucleus '
               '(4 rings with sizes [5,6,6,6] and approximately 17 carbons) '
               'with an externally attached hydroxyl\n'
               ' * SMILES: '
               '[H][C@@]1(CC[C@@]2([H])[C@]3([H])CC=C4C[C@@H](O)CC[C@]4(C)[C@@]3([H])CC[C@]12C)[C@H](C)CC\\C(=C\\C)C(C)C '
               'NAME: isofucosterol REASON: CORRECT Found fused steroid '
               'nucleus (4 rings with sizes [5,6,6,6] and approximately 17 '
               'carbons) with an externally attached hydroxyl\n'
               'False positives: SMILES: '
               'S1S[C@@H]2[C@H](O)[C@H]3N4[C@]1(C(=O)N5[C@@H]6[C@@H](O)[C@@H](OC)[C@@H]7S[C@@]5(C4=O)C[C@H]6C7=O)C[C@H]3C(C2)=O '
               'NAME: Amphiepicoccin G REASON: WRONGLY CLASSIFIED Found fused '
               'steroid nucleus (4 rings with sizes [5,6,6,6] and '
               'approximately 17 carbons) with an externally attached '
               'hydroxyl\n'
               ' * SMILES: '
               'O[C@@H]1C([C@]2([C@@](C=3C([C@]4([C@@]([C@](CC4)([C@@H](CC/C=C(\\C)/C(O)=O)C)[H])(CC3)C)C)=CC2)(CC1)C)[H])(C)C '
               'NAME: Ganoderic acid Y REASON: WRONGLY CLASSIFIED Found fused '
               'steroid nucleus (4 rings with sizes [5,6,6,6] and '
               'approximately 17 carbons) with an externally attached '
               'hydroxyl\n'
               ' * SMILES: '
               'O[C@]1([C@H]2C[C@@]3([C@@]4([C@H]([C@@](CCC4)(CO)C)CC[C@H]3C2)C)CC1)CO '
               'NAME: 3-deoxyaphidicolin REASON: WRONGLY CLASSIFIED Found '
               'fused steroid nucleus (4 rings with sizes [5,6,6,6] and '
               'approximately 16 carbons) with an externally attached '
               'hydroxyl\n'
               ' * SMILES: '
               'C1[C@@H]([C@@H](C[C@@]2([C@]1([C@@H]3[C@@H](CC2)[C@]4(CC[C@@H]([C@]4(CC3)C)C5=COC(C=C5)=O)O)C=O)O)OC(=O)C)OC(=O)C '
               'NAME: '
               '(2beta,3beta,5beta)-2,3-diacetoxy-5,14-dihydroxy-19-oxobufa-20,22-dienolide '
               'REASON: WRONGLY CLASSIFIED Found fused steroid nucleus (4 '
               'rings with sizes [5,6,6,6] and approximately 17 carbons) with '
               'an externally attached hydroxyl\n'
               ' * SMILES: '
               'O=C1N[C@]2(OC=3C=C(C)C=C4C3C2=C(O)C=C4)C5=C1C=CC=C5OC NAME: '
               '(+)-pratensilin B REASON: WRONGLY CLASSIFIED Found fused '
               'steroid nucleus (4 rings with sizes [5,6,6,6] and '
               'approximately 18 carbons) with an externally attached '
               'hydroxyl\n'
               ' * SMILES: '
               'O=C1C=2C=3C(=C4C5=C(C(O)=C(C6=C5C3[C@@]7([C@]6(O[C@H](C7)C)C(=O)C)[C@@H](C2O)OC)OC)C(=O)C=C4OC)C(=C1)OC '
               'NAME: Phaeosphaerin B REASON: WRONGLY CLASSIFIED Found fused '
               'steroid nucleus (4 rings with sizes [5,6,6,6] and '
               'approximately 19 carbons) with an externally attached '
               'hydroxyl\n'
               ' * SMILES: '
               'O=C1C2=C([C@]3([C@H]4O[C@H]4[C@@H](C=5C3=C1OC5)O)C)CC[C@]6([C@H]2CC[C@@H]6C(=O)C)C '
               'NAME: Epoxyvirone REASON: WRONGLY CLASSIFIED Found fused '
               'steroid nucleus (4 rings with sizes [5,6,6,6] and '
               'approximately 17 carbons) with an externally attached '
               'hydroxyl\n'
               ' * SMILES: '
               '[C@H]1([C@]2([C@]3([C@@](C4=C(C=C(O)C=C4)CC3)(CC[C@@]2(C(=O)C1)C)[H])[H])[H])O '
               'NAME: 15alpha-hydroxyestrone REASON: WRONGLY CLASSIFIED Found '
               'fused steroid nucleus (4 rings with sizes [5,6,6,6] and '
               'approximately 17 carbons) with an externally attached '
               'hydroxyl\n'
               ' * SMILES: '
               '[H][C@@]1(CC[C@@]2([H])C3=C(C(=O)C[C@]12C)[C@@]1(C)CC[C@@H](O)[C@](C)(O)[C@]1([H])C[C@@H]3O)[C@H](C)CCC(=C)C(C)C(O)=O '
               'NAME: antcin K REASON: WRONGLY CLASSIFIED Found fused steroid '
               'nucleus (4 rings with sizes [5,6,6,6] and approximately 17 '
               'carbons) with an externally attached hydroxyl\n'
               ' * SMILES: '
               'O=C1C2=C(C(=O)CC[C@@]2([C@]34CC[C@]([C@H](C[C@@H]3C1)C4)(O)COC(=O)C)C)C '
               'NAME: Aphidicolin A68 REASON: WRONGLY CLASSIFIED Found fused '
               'steroid nucleus (4 rings with sizes [5,6,6,6] and '
               'approximately 16 carbons) with an externally attached '
               'hydroxyl\n'
               ' * SMILES: '
               'O[C@@H]1CC=2[C@@]([C@@]3([C@]([C@]4([C@](CC3)(C(=CC4)[C@H](C)/C=C/C(O)=O)C)[H])(CC2)[H])[H])(CC1)C '
               'NAME: (22E)-3beta-Hydroxychola-5,16,22-trien-24-oic Acid '
               'REASON: WRONGLY CLASSIFIED Found fused steroid nucleus (4 '
               'rings with sizes [5,6,6,6] and approximately 17 carbons) with '
               'an externally attached hydroxyl\n'
               ' * SMILES: '
               'C1=C2C(CC[C@]3([C@@]4(CCC[C@]4(CC[C@@]32[H])C)[H])[H])=CC(=C1)O '
               'NAME: estra-1,3,5(10)-trien-3-ol REASON: WRONGLY CLASSIFIED '
               'Found fused steroid nucleus (4 rings with sizes [5,6,6,6] and '
               'approximately 17 carbons) with an externally attached '
               'hydroxyl\n'
               ' * SMILES: '
               'O=C(O[C@@H]1C([C@H]2[C@](C=3C([C@]4([C@]([C@@H]([C@H](C(=O)O)CCC(=C)C(C)C)[C@@H](C4)O)(C)CC3)C)=CC2)(C)CC1)(C)C)C5=CC=C(O)C=C5 '
               'NAME: 3beta-p-hydroxybenzoyldehydrotumulosic acid REASON: '
               'WRONGLY CLASSIFIED Found fused steroid nucleus (4 rings with '
               'sizes [5,6,6,6] and approximately 17 carbons) with an '
               'externally attached hydroxyl\n'
               ' * SMILES: '
               'O=C1N([C@@]2(OC=3C=C(C)C=C4C3C2=C(O)C=C4)C5=C1C=CC=C5OC)CCO '
               'NAME: (-)-pratensilin C REASON: WRONGLY CLASSIFIED Found fused '
               'steroid nucleus (4 rings with sizes [5,6,6,6] and '
               'approximately 18 carbons) with an externally attached '
               'hydroxyl\n'
               ' * SMILES: '
               'O=C1O[C@@H]2C[C@@]3(O[C@H](/C(=C/C)/C)[C@@H](C)C[C@H]3O)O[C@@H](C2)CC=C(C[C@H](C=CC=C4[C@]5([C@H]1C=C([C@@H](O)C5OC4)COC(=O)CC6=COC=C6)O)C)C '
               'NAME: VM48642 REASON: WRONGLY CLASSIFIED Found fused steroid '
               'nucleus (4 rings with sizes [5,6,6,6] and approximately 17 '
               'carbons) with an externally attached hydroxyl\n'
               ' * SMILES: '
               'O1C2=C3C(=C(O)C=C2C)C[C@@H]4C(C)(C)OC([C@H]4[C@@H]3C=5[C@@H]1C[C@](O)(C)[C@H](C5)O)(C)C '
               'NAME: Bisacremine G REASON: WRONGLY CLASSIFIED Found fused '
               'steroid nucleus (4 rings with sizes [5,6,6,6] and '
               'approximately 17 carbons) with an externally attached '
               'hydroxyl\n'
               ' * SMILES: '
               'C[C@@]12[C@]([C@]3([C@](CC1)(C4=C(CC3)C=C(C=C4)OC5CCCC5)[H])[H])(C[C@H]([C@@H]2O)O)[H] '
               'NAME: quinestradol REASON: WRONGLY CLASSIFIED Found fused '
               'steroid nucleus (4 rings with sizes [5,6,6,6] and '
               'approximately 17 carbons) with an externally attached '
               'hydroxyl\n'
               ' * SMILES: '
               'O1[C@@]23[C@@]4([C@@](CC1(O)CC4)(CC=C2[C@]56OCCN(C[C@@]5(C[C@H]3O)C(=CC6)[C@@H](O)C)C)[H])C '
               'NAME: '
               '(1R,5R,6S,11S,12R,14R)-22-[(1S)-1-Hydroxyethyl]-6,16-dimethyl-10,19-dioxa-16-azahexacyclo[12.5.3.15,9.01,14.02,11.06,11]tricosa-2,21-diene-9,12-diol '
               'REASON: WRONGLY CLASSIFIED Found fused steroid nucleus (4 '
               'rings with sizes [5,6,6,6] and approximately 16 carbons) with '
               'an externally attached hydroxyl\n'
               ' * SMILES: '
               'O1CC2=C([C@@](O)(CC)C1=O)C=C3N(CC=4C3=NC=5C(C4CC)=CC=CC5)C2=O '
               'NAME: 7-ethylcamptothecin REASON: WRONGLY CLASSIFIED Found '
               'fused steroid nucleus (4 rings with sizes [5,6,6,6] and '
               'approximately 17 carbons) with an externally attached '
               'hydroxyl\n'
               ' * SMILES: '
               'O[C@@H]1[C@@]2([C@@]([C@](C1)([C@@H](C[C@@H](/C=C(\\C)/C([O-])=O)O)C)[H])(CC=C3C2=CCC4[C@@]3(CCC(=O)C4(C)C)C)C)C '
               'NAME: ganoderate Jc REASON: WRONGLY CLASSIFIED Found fused '
               'steroid nucleus (4 rings with sizes [5,6,6,6] and '
               'approximately 17 carbons) with an externally attached '
               'hydroxyl\n'
               ' * SMILES: '
               'FC12[C@]([C@]3([C@@]([C@](O)([C@@H](C3)C)C(=O)COC(=O)C(C)(C)C)(C[C@@H]1O)C)[H])(C[C@H](F)C=4[C@]2(C)C=CC(=O)C4)[H].OC=1C(=CC=CC1)C(O)=O '
               'NAME: Losalen REASON: WRONGLY CLASSIFIED Found fused steroid '
               'nucleus (4 rings with sizes [5,6,6,6] and approximately 17 '
               'carbons) with an externally attached hydroxyl\n'
               ' * SMILES: '
               'C[C@]1(O)CC[C@H]2[C@@H]3CCC4=CC(=O)C(O)=C[C@]4(C)[C@H]3CC[C@]12C '
               'NAME: 2,17beta-Dihydroxy-17-methylandrosta-1,4-dien-3-one '
               'REASON: WRONGLY CLASSIFIED Found fused steroid nucleus (4 '
               'rings with sizes [5,6,6,6] and approximately 17 carbons) with '
               'an externally attached hydroxyl\n'
               ' * SMILES: '
               'Cc1cc(O)c2C(=O)C3=C(O)C4C(O)C5C6C(O)C(C(O)=C7C(=O)c8c(O)cc(C)cc8C(=O)C467)C35C(=O)c2c1 '
               'NAME: Rugulosin REASON: WRONGLY CLASSIFIED Found fused steroid '
               'nucleus (4 rings with sizes [5,6,6,6] and approximately 16 '
               'carbons) with an externally attached hydroxyl\n'
               ' * SMILES: '
               'O=C(O)[C@@H]([C@@H]1[C@@]2([C@@](C3=C([C@@]4(C(C([C@@H](O)CC4)(C)C)C[C@H]3OC5OC(C(O)C(C5O)O)CO)C)CC2)(C)CC1)C)CCC(=C)C(C)C '
               'NAME: Laetiposide A REASON: WRONGLY CLASSIFIED Found fused '
               'steroid nucleus (4 rings with sizes [5,6,6,6] and '
               'approximately 17 carbons) with an externally attached '
               'hydroxyl\n'
               ' * SMILES: '
               'O[C@H]1[C@]2([C@]([C@]3([C@@]([C@@]4([C@@]([C@@H](O)C3)(C([C@@H](O)CC4)(C)C)[H])C)(C1)[H])C)(CC[C@@]2([C@@](O[C@@H]5O[C@@H]([C@@H](O)[C@H](O)[C@H]5O)CO[C@@H]6O[C@H]([C@H](O)[C@H]6O)CO)(CCC=C(C)C)C)[H])C)[H] '
               'NAME: Ginsenoside F5 REASON: WRONGLY CLASSIFIED Found fused '
               'steroid nucleus (4 rings with sizes [5,6,6,6] and '
               'approximately 17 carbons) with an externally attached '
               'hydroxyl\n'
               'False negatives: SMILES: '
               '[H][C@@]1(CC[C@@]2(C)C3=C(CC[C@]12C)[C@@]1(C)CCC(=O)C(C)(C)C1CC3=O)[C@H](C)C[C@H](O)\\C=C(/C)C(O)=O '
               'NAME: hainanic acid A REASON: MISSED Fused ring system '
               'candidate found with four rings ([5,6,6,6] and ~17 carbons) '
               'but missing an attached hydroxyl group\n'
               ' * SMILES: '
               'CC1=CN(C=N1)C1=CCC2C3CC=C4C[C@H](CC[C@]4(C)C3CC[C@]12C)NC(=O)C1=CC=C(F)C=C1 '
               'NAME: YXG-158 REASON: MISSED Fused ring system candidate found '
               'with four rings ([5,6,6,6] and ~17 carbons) but missing an '
               'attached hydroxyl group\n'
               ' * SMILES: '
               '[H][C@]12CC[C@@]3([H])[C@]4([H])CCC\\C(=C/CO)[C@@]4(C)CC(=O)[C@]3([H])[C@@]1(C)CC[C@@H](O)C2 '
               'NAME: 3alpha,21-dihydroxy-D-homo-5beta-pregn-17a(20)-en-11-one '
               'REASON: MISSED No steroid nucleus identified with the required '
               'ring pattern\n'
               ' * SMILES: '
               '[H][C@@]1(O[C@H]2CC[C@@]3(C)C(C2)=CC[C@]2([H])[C@]3([H])CC[C@]3(C)[C@]([H])(CC[C@@]23[H])[C@H](C)\\C=C\\[C@@H](CC)C(C)C)O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O '
               'NAME: stigmasterol 3-O-beta-D-glucoside REASON: MISSED Fused '
               'ring system candidate found with four rings ([5,6,6,6] and ~17 '
               'carbons) but missing an attached hydroxyl group\n'
               ' * SMILES: '
               '[H][C@@]1(CC[C@@]2([H])[C@]3([H])C=C4C[C@@H](O)CC[C@]4(C)[C@@]3([H])CC[C@]12C)[C@H](C)CCCC(C)C '
               'NAME: B-norcholesterol REASON: MISSED No steroid nucleus '
               'identified with the required ring pattern\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'C[NH+]1CCC(CC1)N1CCN(CC1)C(=O)[C@@H](CC1=CC2=C(NN=C2)C(C)=C1)NC(=O)N1CCC(CC1)C1=CC2=C(NC1=O)C=CC=C2',
                                     'name': 'zavegepant(1+)',
                                     'reason': 'No steroid nucleus identified '
                                               'with the required ring '
                                               'pattern'},
                                 {   'smiles': 'CC1=CC=CC(=C1)C(=O)NNC(=O)C2=C(C3=CC=CC=C3N(C2=O)C)O',
                                     'name': "4-hydroxy-1-methyl-N'-[(3-methylphenyl)-oxomethyl]-2-oxo-3-quinolinecarbohydrazide",
                                     'reason': 'No steroid nucleus identified '
                                               'with the required ring '
                                               'pattern'},
                                 {   'smiles': 'C[C@H]1CN(C(=O)C2=C(C=CC(=C2)NC(=O)CCCN(C)C)O[C@@H]1CN(C)C(=O)NC3CCCCC3)[C@H](C)CO',
                                     'name': 'N-[(2S,3S)-2-[[[(cyclohexylamino)-oxomethyl]-methylamino]methyl]-5-[(2R)-1-hydroxypropan-2-yl]-3-methyl-6-oxo-3,4-dihydro-2H-1,5-benzoxazocin-8-yl]-4-(dimethylamino)butanamide',
                                     'reason': 'No steroid nucleus identified '
                                               'with the required ring '
                                               'pattern'},
                                 {   'smiles': 'O1C(OC2(C=3OC=4C(C(=O)C3)=C(OC)C(OC)=C(OC)C4)C=CC(=O)C=C2)C(O)C(O)C(O)C1C(O)=O',
                                     'name': '3,4,5-trihydroxy-6-{[4-oxo-1-(5,6,7-trimethoxy-4-oxo-4H-chromen-2-yl)cyclohexa-2,5-dien-1-yl]oxy}oxane-2-carboxylic '
                                             'acid',
                                     'reason': 'No steroid nucleus identified '
                                               'with the required ring '
                                               'pattern'},
                                 {   'smiles': 'O=C(N[C@@H]1C(OC2(C1)[C@H]3O[C@H]3C(O)(CC(=O)C)[C@@H]4[C@H]2O4)O)/C=C\\C(CC(CCCCCC)C)C',
                                     'name': 'Penicimutanolone',
                                     'reason': 'No steroid nucleus identified '
                                               'with the required ring '
                                               'pattern'},
                                 {   'smiles': 'O(C(=O)CCCCCCCCCCCCCCCCC)C[C@@H](OC(=O)CCCCCCC/C=C\\CCCC)COC(=O)CCCCCCCCCCCCCCC',
                                     'name': 'TG(16:0/14:1(9Z)/18:0)',
                                     'reason': 'No ring system present; cannot '
                                               'be a sterol'},
                                 {   'smiles': 'O1C(O)C(C(C1)CC2=CC=3OCOC3C=C2)CC4=CC(OC)=C(OC)C=C4',
                                     'name': "(8R,8'R,9S)-9-Hydroxy-3,4-dimethoxy-3',4'-methylenoxy-9,9'-epoxylignan",
                                     'reason': 'No steroid nucleus identified '
                                               'with the required ring '
                                               'pattern'},
                                 {   'smiles': 'CCCCCCCCCCCCCCCC(=O)OC[C@H](COP(O)(=O)O[C@H]1[C@H](O)[C@@H](O)[C@H](O)[C@@H](O)[C@H]1O)OC(=O)CCCCCCCCCCC',
                                     'name': '1-palmitoyl-2-lauroyl-sn-glycero-3-phospho-1D-myo-inositol',
                                     'reason': 'No steroid nucleus identified '
                                               'with the required ring '
                                               'pattern'},
                                 {   'smiles': 'O=C1C2=C([C@@H](O)CC1)[C@@H]([C@H](O)CCC)OC2',
                                     'name': 'Phomopsiketone F',
                                     'reason': 'No steroid nucleus identified '
                                               'with the required ring '
                                               'pattern'},
                                 {   'smiles': 'C1CC(C1)CN(C[C@H]2[C@H]([C@H](N2)CO)C3=CC=CC=C3)C(=O)C4=CC=C(C=C4)F',
                                     'name': 'N-(cyclobutylmethyl)-4-fluoro-N-[[(2R,3R,4S)-4-(hydroxymethyl)-3-phenyl-2-azetidinyl]methyl]benzamide',
                                     'reason': 'No steroid nucleus identified '
                                               'with the required ring '
                                               'pattern'}],
    'sample_false_negatives': [   {   'smiles': '[H][C@@]1(CC[C@@]2(C)C3=C(CC[C@]12C)[C@@]1(C)CCC(=O)C(C)(C)C1CC3=O)[C@H](C)C[C@H](O)\\C=C(/C)C(O)=O',
                                      'name': 'hainanic acid A',
                                      'reason': 'Fused ring system candidate '
                                                'found with four rings '
                                                '([5,6,6,6] and ~17 carbons) '
                                                'but missing an attached '
                                                'hydroxyl group'},
                                  {   'smiles': 'CC1=CN(C=N1)C1=CCC2C3CC=C4C[C@H](CC[C@]4(C)C3CC[C@]12C)NC(=O)C1=CC=C(F)C=C1',
                                      'name': 'YXG-158',
                                      'reason': 'Fused ring system candidate '
                                                'found with four rings '
                                                '([5,6,6,6] and ~17 carbons) '
                                                'but missing an attached '
                                                'hydroxyl group'},
                                  {   'smiles': '[H][C@]12CC[C@@]3([H])[C@]4([H])CCC\\C(=C/CO)[C@@]4(C)CC(=O)[C@]3([H])[C@@]1(C)CC[C@@H](O)C2',
                                      'name': '3alpha,21-dihydroxy-D-homo-5beta-pregn-17a(20)-en-11-one',
                                      'reason': 'No steroid nucleus identified '
                                                'with the required ring '
                                                'pattern'},
                                  {   'smiles': '[H][C@@]1(O[C@H]2CC[C@@]3(C)C(C2)=CC[C@]2([H])[C@]3([H])CC[C@]3(C)[C@]([H])(CC[C@@]23[H])[C@H](C)\\C=C\\[C@@H](CC)C(C)C)O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O',
                                      'name': 'stigmasterol '
                                              '3-O-beta-D-glucoside',
                                      'reason': 'Fused ring system candidate '
                                                'found with four rings '
                                                '([5,6,6,6] and ~17 carbons) '
                                                'but missing an attached '
                                                'hydroxyl group'},
                                  {   'smiles': '[H][C@@]1(CC[C@@]2([H])[C@]3([H])C=C4C[C@@H](O)CC[C@]4(C)[C@@]3([H])CC[C@]12C)[C@H](C)CCCC(C)C',
                                      'name': 'B-norcholesterol',
                                      'reason': 'No steroid nucleus identified '
                                                'with the required ring '
                                                'pattern'}],
    'attempt': 3,
    'reasoning': 'Below is our reasoning and improved solution. In our '
                 'previous attempt the candidate nucleus was defined merely by '
                 'finding four rings having sizes [5,6,6,6] (characteristic of '
                 'a steroid‐like fused ring system) and about 17 carbons in '
                 'total, plus a nearby –OH group. However, some non‐steroid '
                 'structures also matched that crude criterion. In our new '
                 'version we add an extra “connectivity” check on the four '
                 'rings: we require that the candidate four‑ring set shows the '
                 'proper pattern of ring–ring fusions (i.e. exactly three '
                 '“edges” connecting the four rings where each fused pair '
                 'shares at least two atoms, and the connectivity graph is a '
                 'tree). This extra test helps reduce false positives by '
                 'ensuring that the four rings are fused in a way closely '
                 'matching the cholestane skeleton. (We still allow some '
                 'tolerance on the total carbon count.) \n'
                 '\n'
                 'Below is the complete Python code in a single code block:',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 139,
    'num_false_positives': 4292,
    'num_true_negatives': 137864,
    'num_false_negatives': 5,
    'num_negatives': None,
    'precision': 0.03136989392913563,
    'recall': 0.9652777777777778,
    'f1': 0.06076502732240437,
    'accuracy': 0.9698032326071679,
    'negative_predictive_value': 0.9999637336892268}