"""
Classifies: CHEBI:61655 steroid saponin
"""
#!/usr/bin/env python
"""
Classifies: Steroid saponin
Definition: Any saponin derived from a hydroxysteroid.
That is, a molecule must contain (1) a steroid (hydroxysteroid) tetracyclic core and 
(2) at least one sugar moiety (a glycoside ring) attached as a substituent.
Our approach uses ring analysis rather than a very specific SMARTS pattern.
"""

from rdkit import Chem
from rdkit.Chem import rdmolops

def is_steroid_saponin(smiles: str):
    """
    Determines if a molecule is a steroid saponin based on its SMILES string.
    
    Our strategy (heuristic):
      1. Parse the SMILES string.
      2. Identify candidate rings that could form a steroid core.
         We look for four fused rings that are made entirely of carbons.
         Furthermore, we require that within that fused set there are three 6-membered rings
         and one 5-membered ring.
      3. Verify that at least one carbon in these rings has an exocyclic –OH group (to meet the
         “hydroxysteroid” requirement).
      4. Look for at least one sugar ring – here defined as a 5- or 6-membered ring that 
         contains exactly one oxygen atom in the ring and at least two exocyclic hydroxyl groups.
    
    Args:
      smiles (str): SMILES string of the molecule.
      
    Returns:
      (bool, str): A tuple where the first element is True if the molecule is classified as a 
                   steroid saponin, and False otherwise; the second element is a message explaining 
                   the reasoning.
    """
    # Parse the SMILES; if invalid, return immediately.
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
    
    # For sugar detection we may need explicit hydrogens.
    mol_with_H = Chem.AddHs(mol)
    
    # Get ring information from the molecule.
    ring_info = mol.GetRingInfo()
    all_rings = ring_info.AtomRings()
    
    # Step 1 — Look for candidate steroid rings:
    # We assume that steroid rings are composed entirely of carbons.
    candidate_rings = []
    for ring in all_rings:
        # Only consider rings that are either 5 or 6 members.
        if len(ring) not in (5, 6):
            continue
        # Check that every atom in the ring is carbon.
        if all(mol.GetAtomWithIdx(idx).GetAtomicNum() == 6 for idx in ring):
            candidate_rings.append(ring)
    
    # Build a graph over candidate rings. Two rings are "fused" if they share at least two atoms.
    ring_graph = {i: set() for i in range(len(candidate_rings))}
    for i in range(len(candidate_rings)):
        for j in range(i+1, len(candidate_rings)):
            shared = set(candidate_rings[i]).intersection(set(candidate_rings[j]))
            if len(shared) >= 2:
                ring_graph[i].add(j)
                ring_graph[j].add(i)
    
    # Now find connected components (clusters) from this graph.
    def dfs(node, visited, comp):
        visited.add(node)
        comp.add(node)
        for neighbor in ring_graph[node]:
            if neighbor not in visited:
                dfs(neighbor, visited, comp)
    
    components = []
    visited = set()
    for node in ring_graph:
        if node not in visited:
            comp = set()
            dfs(node, visited, comp)
            components.append(comp)
    
    steroid_core_found = False
    reason_core = ""
    # Check each component to see if any has exactly 4 rings with the expected size: one 5-membered and three 6-membered.
    for comp in components:
        if len(comp) < 4:
            continue
        # We iterate over all subsets of 4 rings from this component:
        from itertools import combinations
        for subset in combinations(comp, 4):
            ring_sizes = [len(candidate_rings[i]) for i in subset]
            if sorted(ring_sizes) == [5, 6, 6, 6]:
                # Found a candidate steroid nucleus.
                # Now check for at least one hydroxyl (–OH) attached to one of the carbons in these rings.
                hydroxyl_found = False
                # Get all atom indices in these candidate rings.
                core_atoms = set()
                for i in subset:
                    core_atoms.update(candidate_rings[i])
                for idx in core_atoms:
                    atom = mol.GetAtomWithIdx(idx)
                    if atom.GetAtomicNum() != 6:
                        continue
                    # Check neighboring atoms that are not in the core.
                    for nbr in atom.GetNeighbors():
                        if nbr.GetIdx() in core_atoms:
                            continue
                        # Check if the neighbor is oxygen connected via a single bond.
                        if nbr.GetAtomicNum() == 8:
                            bond = mol.GetBondBetweenAtoms(atom.GetIdx(), nbr.GetIdx())
                            if bond is not None and bond.GetBondType().name == "SINGLE":
                                hydroxyl_found = True
                                break
                    if hydroxyl_found:
                        break
                if hydroxyl_found:
                    steroid_core_found = True
                    break
        if steroid_core_found:
            break

    if not steroid_core_found:
        return False, "No steroid (hydroxysteroid) tetracyclic core found"
    
    # Step 2 — Look for at least one sugar ring.
    # We use a similar ring search but now we look for rings that are 5 or 6 members,
    # have exactly one ring oxygen (atomic number 8), and at least two exocyclic hydroxyl groups.
    sugar_found = False
    for ring in all_rings:
        if len(ring) not in (5, 6):
            continue
        # Count atoms in the ring that are oxygen. (Note: we use the original mol.)
        oxy_in_ring = sum(1 for idx in ring if mol.GetAtomWithIdx(idx).GetAtomicNum() == 8)
        if oxy_in_ring != 1:
            continue
        # Now count exocyclic –OH groups attached to ring atoms.
        oh_count = 0
        for idx in ring:
            atom = mol_with_H.GetAtomWithIdx(idx)
            # We expect sugar rings to consist mainly of carbon.
            if atom.GetAtomicNum() != 6:
                continue
            for nbr in atom.GetNeighbors():
                # If the neighbor is not in this ring...
                if nbr.GetIdx() in ring:
                    continue
                # Check if neighboring oxygen is part of an –OH.
                if nbr.GetAtomicNum() == 8:
                    bond = mol_with_H.GetBondBetweenAtoms(atom.GetIdx(), nbr.GetIdx())
                    if bond is not None and bond.GetBondType().name == "SINGLE":
                        # Further check: the oxygen should have at least one hydrogen.
                        # (Counting explicit H atoms attached.)
                        num_H = sum(1 for h in nbr.GetNeighbors() if h.GetAtomicNum() == 1)
                        if num_H >= 1:
                            oh_count += 1
        if oh_count >= 2:
            sugar_found = True
            break

    if not sugar_found:
        return False, "No sugar ring (glycoside) found"
    
    return True, "Molecule contains a hydroxysteroid tetracyclic core with at least one sugar ring attached"

# Example usage (for testing):
if __name__ == "__main__":
    test_smiles = [
        # Jurubine
        "O1[C@@]2([C@@]([C@@]3([C@]([C@]4([C@@]([C@@]5([C@@](CC4)(C[C@@H](N)CC5)[H])C)(CC3)[H])[H])(C2)[H])C)([C@@H]([C@@]1(O)CC[C@H](CO[C@@H]6O[C@@H]([C@@H](O)C(O)C6O)CO)C)C)[H])[H]",
        # Asparagoside B
        "O1[C@@]2([C@@]([C@@]3([C@]([C@]4([C@@]([C@@]5([C@](CC4)(C[C@@H](O)CC5)[H])C)(CC3)[H])[H])(C2)[H])C)([C@@H]([C@@]1(O)CC[C@@H](CO[C@@H]6O[C@@H]([C@@H](O)[C@H](O)[C@H]6O)CO)C)C)[H])[H]",
        # ginsenoside Re
        "C[C@@H]1O[C@@H](O[C@@H]2[C@@H](O)[C@H](O)[C@@H](CO)O[C@H]2O[C@H]2C[C@]3(C)[C@H](C[C@@H](O)[C@@H]4[C@H](CC[C@@]34C)[C@](C)(CCC=C(C)C)O[C@@H]3O[C@H](CO)[C@@H](O)[C@H](O)[C@H]3O)[C@@]3(C)CC[C@H](O)C(C)(C)[C@H]23)[C@H](O)[C@H](O)[C@H]1O",
        # 17-beta-Estradiol glucuronide
        "O([C@@H]1[C@@]2(C(C3C(CC2)C4=C(CC3)C=C(O)C=C4)CC1)C)[C@@H]5O[C@@H]([C@@H](O)[C@H](O)[C@H]5O)C(O)=O"
    ]
    for smi in test_smiles:
        result, reason = is_steroid_saponin(smi)
        print("SMILES:", smi)
        print("Is steroid saponin?", result)
        print("Reason:", reason)
        print("-----")


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:61655',
                          'name': 'steroid saponin',
                          'definition': 'Any saponin derived from a '
                                        'hydroxysteroid.',
                          'parents': ['CHEBI:26605', 'CHEBI:35341'],
                          'xrefs': [   'PMID:18486659',
                                       'PMID:20346608',
                                       'PMID:20846658'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 154,
                           'log_lines_of_code': 5.0369526024136295,
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
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 3,
                                                 2,
                                                 2,
                                                 3,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 3,
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
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 3,
                                                 3,
                                                 3,
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
                                                 3,
                                                 4,
                                                 4,
                                                 4,
                                                 4,
                                                 4,
                                                 4,
                                                 5,
                                                 4,
                                                 5,
                                                 5,
                                                 6,
                                                 5,
                                                 5,
                                                 6,
                                                 7,
                                                 6,
                                                 6,
                                                 7,
                                                 7,
                                                 8,
                                                 8,
                                                 5,
                                                 6,
                                                 4,
                                                 5,
                                                 5,
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
                                                 3,
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
                                                 4,
                                                 4,
                                                 5,
                                                 4,
                                                 4,
                                                 5,
                                                 5,
                                                 6,
                                                 6,
                                                 6,
                                                 6,
                                                 7,
                                                 2,
                                                 3,
                                                 3,
                                                 0,
                                                 1,
                                                 2,
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
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2],
                           'max_indent': 8,
                           'imports': [   'from rdkit import Chem',
                                          'from rdkit.Chem import rdmolops'],
                           'imports_count': 2,
                           'methods_called': [   'GetBondType',
                                                 'GetNeighbors',
                                                 'GetRingInfo',
                                                 'AtomRings',
                                                 'add',
                                                 'GetIdx',
                                                 'AddHs',
                                                 'update',
                                                 'intersection',
                                                 'GetAtomWithIdx',
                                                 'MolFromSmiles',
                                                 'GetAtomicNum',
                                                 'append',
                                                 'GetBondBetweenAtoms'],
                           'methods_called_count': 14,
                           'smarts_strings': [],
                           'smarts_strings_count': 0,
                           'defs': [   'is_steroid_saponin(smiles: str):',
                                       'dfs(node, visited, comp):'],
                           'defs_count': 2,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "No steroid (hydroxysteroid) '
                                          'tetracyclic core found"',
                                          'False, "No sugar ring (glycoside) '
                                          'found"',
                                          'True, "Molecule contains a '
                                          'hydroxysteroid tetracyclic core '
                                          'with at least one sugar ring '
                                          'attached"'],
                           'returns_count': 4,
                           'complexity': 6.607390520482726},
    'message': '\n'
               'Attempt failed: F1 score of 0 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: NONE\n'
               'False positives: NONE\n'
               'False negatives: SMILES: '
               'O1[C@@]2([C@@]([C@@]3([C@]([C@]4([C@@]([C@@]5([C@@](CC4)(C[C@@H](N)CC5)[H])C)(CC3)[H])[H])(C2)[H])C)([C@@H]([C@@]1(O)CC[C@H](CO[C@@H]6O[C@@H]([C@@H](O)C(O)C6O)CO)C)C)[H])[H] '
               'NAME: Jurubine REASON: MISSED No steroid (hydroxysteroid) '
               'tetracyclic core found\n'
               ' * SMILES: '
               'O1[C@@]2([C@@]([C@@]3([C@]([C@]4([C@@]([C@@]5([C@](CC4)(C[C@@H](O)CC5)[H])C)(CC3)[H])[H])(C2)[H])C)([C@@H]([C@@]1(O)CC[C@@H](CO[C@@H]6O[C@@H]([C@@H](O)[C@H](O)[C@H]6O)CO)C)C)[H])[H] '
               'NAME: Asparagoside B REASON: MISSED No steroid '
               '(hydroxysteroid) tetracyclic core found\n'
               ' * SMILES: '
               'C[C@@H]1O[C@@H](O[C@@H]2[C@@H](O)[C@H](O)[C@@H](CO)O[C@H]2O[C@H]2C[C@]3(C)[C@H](C[C@@H](O)[C@@H]4[C@H](CC[C@@]34C)[C@](C)(CCC=C(C)C)O[C@@H]3O[C@H](CO)[C@@H](O)[C@H](O)[C@H]3O)[C@@]3(C)CC[C@H](O)C(C)(C)[C@H]23)[C@H](O)[C@H](O)[C@H]1O '
               'NAME: ginsenoside Re REASON: MISSED No steroid '
               '(hydroxysteroid) tetracyclic core found\n'
               ' * SMILES: '
               'C[C@@H]([C@H]1CC[C@H]2[C@@H]3CC=C4C[C@H](CC(=O)[C@]4(CO)[C@H]3CC[C@]12C)O[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O)[C@H]1CC(C)=C(CO)C(=O)O1 '
               'NAME: withalongolide I REASON: MISSED No steroid '
               '(hydroxysteroid) tetracyclic core found\n'
               ' * SMILES: '
               'O([C@@H]1[C@@H]([C@@]2([C@]([C@]3([C@@]([C@@]4([C@@]([C@@H](O[C@@H]5OC([C@@H](O)[C@H](O)C5O)CO)C3)(C[C@@H](O[C@@H]6OC([C@@H](O)[C@H](O)C6O)CO)CC4)[H])C)(CC2)[H])[H])(C1)[H])C)CC)[C@@]7(OC[C@@H](CC7O)C)C '
               'NAME: '
               '3-O-(Glcb)-6-O-(Glcb)-(25R)-5alpha-spirostan-3beta,6alpha,23S-triol '
               'REASON: MISSED No steroid (hydroxysteroid) tetracyclic core '
               'found\n'
               ' * SMILES: '
               'O1[C@H](O)[C@]2([C@]3(C([C@@]4(C(CC3)C([C@@H](O[C@@H]5O[C@@H]([C@@H](O)[C@H](O)[C@H]5O)CO[C@@H]6O[C@H]([C@H](O)[C@@H](O)[C@H]6O)C)CC4)(C)C)C)CC[C@@]2([C@]7([C@@]1([C@H](OC7=O)CC=C(C)C)C)[H])[H])C)C '
               'NAME: Mabiogenin 3-[rhamnosyl-(1->6)-glucoside] REASON: MISSED '
               'No steroid (hydroxysteroid) tetracyclic core found\n'
               ' * SMILES: '
               'O([C@@H]1[C@@]2(C(C3C(CC2)C4=C(CC3)C=C(O)C=C4)CC1)C)[C@@H]5O[C@@H]([C@@H](O)[C@H](O)[C@H]5O)C(O)=O '
               'NAME: 17-beta-Estradiol glucuronide REASON: MISSED No steroid '
               '(hydroxysteroid) tetracyclic core found\n'
               ' * SMILES: '
               'C[C@H]1[C@H]2[C@H](C[C@H]3[C@@H]4CC=C5C[C@H](CC[C@]5(C)[C@H]4CC[C@]23C)O[C@@H]2O[C@H](CO)[C@@H](O[C@@H]3O[C@H](CO)[C@@H](O)[C@H](O)[C@H]3O)[C@H](O)[C@H]2O[C@@H]2O[C@@H](C)[C@H](O)[C@@H](O)[C@H]2O)O[C@]11CC[C@@](C)(CO)O1 '
               'NAME: 26-desglucoavenacoside A REASON: MISSED No steroid '
               '(hydroxysteroid) tetracyclic core found\n'
               ' * SMILES: '
               'O([C@@H]1[C@@H]([C@@]2([C@]([C@]3([C@@]([C@@]4(C(=CC3)C[C@@H](O[C@@H]5OC([C@@H](O)[C@H](O)C5O[C@@H]6OC([C@H](O)C(O)[C@@H]6O)C)CO)CC4)C)(CC2)[H])[H])(C1)[H])C)CC)C(CC[C@H](CO[C@@H]7OC([C@@H](O)[C@H](O)C7O)CO)C)=C '
               'NAME: '
               '3-O-(Rhaa1-2Glcb)-26-O-(Glcb)-(25R)-furosta-5,20(22)-dien-3beta,26-diol '
               'REASON: MISSED No steroid (hydroxysteroid) tetracyclic core '
               'found\n'
               ' * SMILES: '
               'O1C2C(C3(C(C4C(C5(C(CC4)CC(OC6OC(C(O)C(OC7OC(C(O)C(O)C7O)CO)C6OC8OC(C(O)C(O)C8O)C)CO)CC5)C)CC3)C2)C)C(C1(OC)CCC(COC9OC(C(O)C(O)C9O)CO)C)C '
               'NAME: (3b,5a,22x,25S)-Furostane-22-methoxy-3,26-diol '
               '3-[rhamnosyl-(1->2)-[glucosyl-(1->3)]-glucoside] 26-glucoside '
               'REASON: MISSED No steroid (hydroxysteroid) tetracyclic core '
               'found\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'O=C(N1[C@H](CCC1)C(O)=O)[C@@H](NC(=O)[C@@H](N)CC(O)=O)CCC(=O)N',
                                     'name': 'Asp-Gln-Pro',
                                     'reason': 'No steroid (hydroxysteroid) '
                                               'tetracyclic core found'},
                                 {   'smiles': 'O1C=2C(C(O)=C(CC3=C(O)C=4C(OC3=O)=CC=CC4C)C1=O)=C(C=CC2)C',
                                     'name': 'Gerberinol',
                                     'reason': 'No steroid (hydroxysteroid) '
                                               'tetracyclic core found'},
                                 {   'smiles': 'O=C(O)/C(=C/[C@H]1C=C(CC[C@@H]1C(C)C)CO)/COC(=O)C',
                                     'name': '3-acetylgliocladic acid',
                                     'reason': 'No steroid (hydroxysteroid) '
                                               'tetracyclic core found'},
                                 {   'smiles': 'O=C(CCCCCCCCC)C=1C=CC(=NC1)CCCCCCCCC',
                                     'name': '1-(6-Nonylpyridin-3-yl)decan-1-one',
                                     'reason': 'No steroid (hydroxysteroid) '
                                               'tetracyclic core found'},
                                 {   'smiles': 'CCC(=O)O[C@H]1[C@H](C)O[C@H](C[C@@]1(C)O)O[C@@H]1[C@@H](C)O[C@@H](O[C@H]2[C@@H](CC=O)C[C@@H](C)[C@@H](O)\\C=C\\C=C\\C[C@@H](C)OC(=O)C[C@@H](O)[C@@H]2OC)[C@H](O)[C@H]1N(C)C',
                                     'name': 'Leucomycin A7',
                                     'reason': 'No steroid (hydroxysteroid) '
                                               'tetracyclic core found'},
                                 {   'smiles': 'C[C@H]1O[C@H](C[C@@H](O)[C@@H]1O)c1ccc2C(=O)C3=C([C@H](O)C[C@]4(O)C[C@@](C)(O)CC(=O)[C@]34O)C(=O)c2c1O',
                                     'name': 'Urdamycinone F',
                                     'reason': 'No steroid (hydroxysteroid) '
                                               'tetracyclic core found'},
                                 {   'smiles': 'CC(C)=CCC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\COP([O-])(=O)OP([O-])([O-])=O',
                                     'name': 'all-trans-dodecaprenyl '
                                             'diphosphate(3-)',
                                     'reason': 'No steroid (hydroxysteroid) '
                                               'tetracyclic core found'},
                                 {   'smiles': '[O-][N+](=O)N1CN(CN(CN(C1)[N+]([O-])=O)[N+]([O-])=O)[N+]([O-])=O',
                                     'name': 'octogen',
                                     'reason': 'No steroid (hydroxysteroid) '
                                               'tetracyclic core found'},
                                 {   'smiles': 'CC(=O)NCCC[NH2+]CCCC[NH2+]CCCNC(C)=O',
                                     'name': 'N(1),N(12)-diacetylsperminium(2+)',
                                     'reason': 'No steroid (hydroxysteroid) '
                                               'tetracyclic core found'},
                                 {   'smiles': 'C[C@@H]([C@H]1CC[C@H]2[C@H](CCc3cc(O)ccc3C)C(=O)CC[C@]12C)C(O)=O',
                                     'name': '3-hydroxy-9-oxo-9,10-seco-23,24-bisnorchola-1,3,5(10)-trien-22-oic '
                                             'acid',
                                     'reason': 'No steroid (hydroxysteroid) '
                                               'tetracyclic core found'}],
    'sample_false_negatives': [   {   'smiles': 'O1[C@H](O)[C@]2([C@]3(C([C@@]4(C(CC3)C([C@@H](O[C@@H]5O[C@@H]([C@@H](O)[C@H](O)[C@H]5O)CO[C@@H]6O[C@H]([C@H](O)[C@@H](O)[C@H]6O)C)CC4)(C)C)C)CC[C@@]2([C@]7([C@@]1([C@H](OC7=O)CC=C(C)C)C)[H])[H])C)C',
                                      'name': 'Mabiogenin '
                                              '3-[rhamnosyl-(1->6)-glucoside]',
                                      'reason': 'No steroid (hydroxysteroid) '
                                                'tetracyclic core found'},
                                  {   'smiles': 'O1[C@@H](OC[C@@]2([C@@H]3C=CC4=C[C@](C=C)(C)CC[C@@H]4[C@]3(C[C@H]([C@@H]2O)O)C)C)[C@@H](O)[C@H](O)[C@@H]([C@H]1CO[C@H]5O[C@@H]([C@@H](O)[C@@H]([C@H]5O)O)CO)O',
                                      'name': 'Virescenoside R1',
                                      'reason': 'No steroid (hydroxysteroid) '
                                                'tetracyclic core found'},
                                  {   'smiles': 'O=C(O[C@@H]1[C@@H](O[C@@H]2O[C@@H]([C@@H](O)[C@@H]([C@H]2NC(=O)C)O)CO)[C@@H](O)[C@H](O[C@@H]3[C@@H](O)C([C@H]4CC[C@@]5([C@@H]([C@@]4(C3)C)CC=C([C@@H]5CC[C@H](N)C(=O)O)C)C)(C)C)O[C@H]1C)C6=CC(O)=CC=C6',
                                      'name': 'Brasilicardin B',
                                      'reason': 'No steroid (hydroxysteroid) '
                                                'tetracyclic core found'},
                                  {   'smiles': 'O=C1[C@]2(O)[C@@H]([C@]3(C[C@@H](O)[C@@H]([C@@]([C@@H]3[C@H]1O)(CO[C@@H]4O[C@@H]([C@@H](O)[C@H]([C@@H]4O)O)CO)C)O)C)CC[C@@](C2)(C=C)C',
                                      'name': 'Virescenoside Z9',
                                      'reason': 'No steroid (hydroxysteroid) '
                                                'tetracyclic core found'},
                                  {   'smiles': 'O(C1C(C2C(C3C(C4(C(C5C(CC4)(CCC(C5)=C)C(OC6OC(C(O)C(O)C6O)CO)=O)=CC3)C)(CC2)C)(CC1O)C)(C)C(O)=O)C7OC(C(O)C(O)C7O)C(O)=O',
                                      'name': '(2b,3b)-Dihydroxy-30-nor-12,20(29)-oleanadiene-28-glucopyranosyloxy-23-oic '
                                              'acid 3-glucuronide',
                                      'reason': 'No steroid (hydroxysteroid) '
                                                'tetracyclic core found'},
                                  {   'smiles': 'O=C1C2=C(C(=O)C3=C1[C@@]4(O)[C@](O)([C@H](OC(=O)C)C(C)=C[C@@H]4O[C@@H]5O[C@H]([C@@H](O)[C@@H](C5)OC)C)[C@H]([C@H]3O)OC(=O)C)C(O)=C([C@@H]6O[C@@H]([C@@H](O)[C@@H](C6)O[C@@H]7O[C@@H]([C@@H](O[C@@H]8O[C@@H]([C@@H](NC(=O)N)CC8)C)[C@](C7)(O)C)C)C)C=C2',
                                      'name': 'P371A2',
                                      'reason': 'No steroid (hydroxysteroid) '
                                                'tetracyclic core found'},
                                  {   'smiles': 'O1[C@@H](OC[C@]2([C@@H](O)[C@H](O)C[C@]3([C@H]2[C@H](O)C=C4[C@@H]3CC[C@@](C4)(C=C)C)C)C)[C@@H](O)[C@H](O)[C@@H]([C@H]1CO)O',
                                      'name': 'Virescenoside N',
                                      'reason': 'No steroid (hydroxysteroid) '
                                                'tetracyclic core found'},
                                  {   'smiles': 'O1[C@H](OC[C@]2([C@@H](O)[C@H](O)C[C@]3([C@H]2CC=C4[C@@H]3CC[C@@](C4)(C=C)C)C)C)[C@H](O)[C@@H](O)[C@@H]([C@H]1CO[C@@H]5O[C@@H]([C@@H](O)[C@H]([C@@H]5O)O)CO)O',
                                      'name': 'Virescenoside R',
                                      'reason': 'No steroid (hydroxysteroid) '
                                                'tetracyclic core found'},
                                  {   'smiles': 'O=C(O)C1OC(OC[C@]2([C@@H](O)CC[C@]3([C@H]2C[C@@H](O)C=4[C@@H]3CC[C@@](C4)(C=C)C)C)C)C(O)C(C1O)O',
                                      'name': 'Virescenoside Z6',
                                      'reason': 'No steroid (hydroxysteroid) '
                                                'tetracyclic core found'},
                                  {   'smiles': 'O=C1C2=C[C@@](C=C)(CC[C@@H]2[C@]3(C[C@@H](O)[C@@H]([C@@]([C@@H]3C1)(CO[C@@H]4O[C@@H]([C@@H](O)[C@H]([C@@H]4O)O)CO)C)O)C)C',
                                      'name': 'Virescenoside V',
                                      'reason': 'No steroid (hydroxysteroid) '
                                                'tetracyclic core found'}],
    'attempt': 1,
    'reasoning': 'Below is one possible solution. In our revised approach we '
                 'decided not to rely on one very‐specific SMARTS pattern but '
                 'rather to analyze the molecule’s ring systems. First we look '
                 'for a set of four fused rings that (a) are built exclusively '
                 'from carbon (as expected for a steroid skeleton) and (b) '
                 'have the expected ring size distribution (three six‐membered '
                 'rings and one five‐membered ring). We then require that at '
                 'least one ring carbon carries an –OH substituent (to catch '
                 '“hydroxysteroid” cores). Finally we scan the molecule for at '
                 'least one sugar ring (a cyclic structure of 5–6 atoms that '
                 'contains exactly one ring oxygen and at least two exocyclic '
                 '–OH groups). (Of course, any heuristic is imperfect.) \n'
                 '\n'
                 'Below is the complete Python code in one block:\n'
                 '\n'
                 '------------------------------------------------',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 238,
    'num_false_positives': 540,
    'num_true_negatives': 141485,
    'num_false_negatives': 37,
    'num_negatives': None,
    'precision': 0.3059125964010283,
    'recall': 0.8654545454545455,
    'f1': 0.45204178537511874,
    'accuracy': 0.9959451862262825,
    'negative_predictive_value': 0.9997385565495117}