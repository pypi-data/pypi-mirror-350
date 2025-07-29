"""
Classifies: CHEBI:35346 11beta-hydroxy steroid
"""
#!/usr/bin/env python3
"""
Classifies: 11β-hydroxy steroid
Defined as: Any 11-hydroxy steroid in which the hydroxy group at position 11 has beta-configuration.
Heuristic approach:
  1. Parse the SMILES string.
  2. Get the molecule’s ring information and filter only rings of size 5 or 6,
     as these are the sizes found in a cyclopentanoperhydrophenanthrene nucleus.
  3. Build a fused ring graph (two rings are fused if they share at least 2 atoms)
     and group rings into connected components.
  4. For each component, require that:
       • it has at least 4 rings,
       • it contains at least 3 six-membered rings and at least one five-membered ring,
       • its union of ring atoms (when counting only carbons) is in the expected range (roughly 15–21 atoms).
  5. If a steroid‐like nucleus is found, then use the SMARTS "[C@@]([OX2H])" to detect beta–oriented –OH.
  6. Finally, require that at least one of these beta –OH groups is on a chiral carbon that is part
     of the steroid nucleus.
This should reduce false positives.
"""

from rdkit import Chem
from rdkit.Chem import rdMolDescriptors

def is_11beta_hydroxy_steroid(smiles: str):
    """
    Determines whether a molecule is an 11β-hydroxy steroid based on its SMILES string.
    
    Returns:
      (True, reason) if the criteria are met,
      (False, reason) if not.
    """
    try:
        mol = Chem.MolFromSmiles(smiles)
        if mol is None:
            return False, "Invalid SMILES string."
    except Exception as e:
        return False, f"Error parsing SMILES: {e}"
    
    # Get all ring information (each ring is a tuple of atom indices)
    all_rings = list(mol.GetRingInfo().AtomRings())
    if not all_rings:
        return False, "No rings detected; not a steroid."
    
    # Filter rings: only consider rings of size 5 or 6 (steroid rings)
    valid_rings = [set(r) for r in all_rings if len(r) in (5,6)]
    if len(valid_rings) < 4:
        return False, f"Only {len(valid_rings)} rings of size 5 or 6 found; a steroid nucleus (>=4 rings) is expected."
    
    # Build fused graph: two rings are fused if they share at least 2 atoms.
    n = len(valid_rings)
    fused_graph = {i: set() for i in range(n)}
    for i in range(n):
        for j in range(i+1, n):
            if len(valid_rings[i] & valid_rings[j]) >= 2:
                fused_graph[i].add(j)
                fused_graph[j].add(i)
    
    # Find connected components among the rings.
    visited = set()
    components = []
    for i in range(n):
        if i not in visited:
            stack = [i]
            comp = set()
            while stack:
                current = stack.pop()
                if current not in visited:
                    visited.add(current)
                    comp.add(current)
                    stack.extend(fused_graph[current] - visited)
            components.append(comp)
    
    # Search for a steroid‐like nucleus in one of the components.
    steroid_cluster_atoms = None
    for comp in components:
        comp_rings = [valid_rings[i] for i in comp]
        if len(comp_rings) < 4:
            continue
        
        # Count ring sizes.
        count6 = sum(1 for ring in comp_rings if len(ring) == 6)
        count5 = sum(1 for ring in comp_rings if len(ring) == 5)
        
        if count6 < 3 or count5 < 1:
            continue
        
        # Combine all atoms (the nucleus)
        comp_atoms = set()
        for ring in comp_rings:
            comp_atoms |= ring
        # Check that the nucleus has a reasonable size:
        # Steroid core usually has about 17 carbon atoms. Allow some wiggle room.
        carbon_atoms = [a.GetIdx() for a in mol.GetAtoms() if a.GetAtomicNum() == 6]
        nucleus_carbons = comp_atoms & set(carbon_atoms)
        if not (15 <= len(nucleus_carbons) <= 21):
            continue
        
        steroid_cluster_atoms = comp_atoms  # record the atom indices involved in the nucleus
        break
    
    if steroid_cluster_atoms is None:
        return False, "No fused steroid nucleus (with >=3 six-membered rings and 1 five-membered ring and appropriate carbon count) detected."
    
    # Look for beta-oriented -OH using SMARTS.
    # [C@@] means chiral carbon with beta configuration; ([OX2H]) means directly bonded -OH.
    beta_oh_smarts = "[C@@]([OX2H])"
    beta_oh_query = Chem.MolFromSmarts(beta_oh_smarts)
    if beta_oh_query is None:
        return False, "Error constructing SMARTS query for beta-oriented hydroxyl group."
    
    matches = mol.GetSubstructMatches(beta_oh_query)
    if not matches:
        return False, "No beta-oriented hydroxyl group (SMARTS '[C@@]([OX2H])') found in the molecule."
    
    # Check that at least one match is on an atom that is in the steroid nucleus.
    for match in matches:
        # match[0] is the chiral carbon
        if match[0] in steroid_cluster_atoms:
            return True, "Steroid nucleus detected (fused rings with appropriate sizes and carbon count) and beta-oriented hydroxyl group found on it."
    
    return False, "Beta-oriented hydroxyl group not located on the identified steroid nucleus."

# Example usage and tests.
if __name__ == "__main__":
    # A few test SMILES examples (including some from the provided list)
    test_smiles_list = [
        # prednisolone phosphate
        "C[C@@]12C[C@@H]([C@]3([C@]([C@]2([H])CC[C@@]1(C(COP(=O)(O)O)=O)O)(CCC=4[C@]3(C)C=CC(C4)=O)[H])[H])O",
        # 5beta-dihydroaldosterone
        "C[C@]12CCC(=O)C[C@H]1CC[C@H]1[C@@H]3CC[C@H](C(=O)CO)[C@]3(C[C@H](O)[C@H]21)C=O",
        # withalongolide C
        "C[C@@H]([C@H]1CC[C@H]2[C@@H]3C[C@H]4O[C@]44[C@@H](O)C=CC(=O)[C@]4(C)[C@H]3[C@@H](O)C[C@]12C)[C@H]1CC(C)=C(CO)C(=O)O1",
        # A false positive example (a carbohydrate or non-steroid fused ring system)
        "CO[C@H]1C[C@H](O[C@H]2CC[C@@]3(C)[C@H](CC[C@@H]4[C@@H]3[C@H](O)C[C@]3(C)[C@H](CC[C@]43O)C3=CC(=O)OC3)C2)O[C@@H](C)[C@@H]1O"
    ]
    
    for sm in test_smiles_list:
        result, reason = is_11beta_hydroxy_steroid(sm)
        print("SMILES:", sm)
        print("Result:", result)
        print("Reason:", reason)
        print("-" * 80)


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:35346',
                          'name': '11beta-hydroxy steroid',
                          'definition': 'Any 11-hydroxy steroid in which the '
                                        'hydroxy group at position 11 has '
                                        'beta- configuration.',
                          'parents': ['CHEBI:36841'],
                          'xrefs': ['KEGG:C01058'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 99,
                           'log_lines_of_code': 4.59511985013459,
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
                                                 3,
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
                                                 2,
                                                 3,
                                                 4,
                                                 4,
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
                                                 5,
                                                 5,
                                                 5,
                                                 3,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 3,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 2,
                                                 2,
                                                 2,
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
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 3,
                                                 1,
                                                 1,
                                                 0,
                                                 1,
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
                                                 1,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2],
                           'max_indent': 5,
                           'imports': [   'from rdkit import Chem',
                                          'from rdkit.Chem import '
                                          'rdMolDescriptors'],
                           'imports_count': 2,
                           'methods_called': [   'append',
                                                 'GetIdx',
                                                 'GetAtomicNum',
                                                 'MolFromSmiles',
                                                 'AtomRings',
                                                 'pop',
                                                 'GetAtoms',
                                                 'MolFromSmarts',
                                                 'add',
                                                 'extend',
                                                 'GetRingInfo',
                                                 'GetSubstructMatches'],
                           'methods_called_count': 12,
                           'smarts_strings': ['beta_oh_smarts'],
                           'smarts_strings_count': 1,
                           'defs': ['is_11beta_hydroxy_steroid(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string."',
                                          'False, f"Error parsing SMILES: {e}"',
                                          'False, "No rings detected; not a '
                                          'steroid."',
                                          'False, f"Only {len(valid_rings)} '
                                          'rings of size 5 or 6 found; a '
                                          'steroid nucleus (>=4 rings) is '
                                          'expected."',
                                          'False, "No fused steroid nucleus '
                                          '(with >=3 six-membered rings and 1 '
                                          'five-membered ring and appropriate '
                                          'carbon count) detected."',
                                          'False, "Error constructing SMARTS '
                                          'query for beta-oriented hydroxyl '
                                          'group."',
                                          'False, "No beta-oriented hydroxyl '
                                          "group (SMARTS '[C@@]([OX2H])') "
                                          'found in the molecule."',
                                          'True, "Steroid nucleus detected '
                                          '(fused rings with appropriate sizes '
                                          'and carbon count) and beta-oriented '
                                          'hydroxyl group found on it."',
                                          'False, "Beta-oriented hydroxyl '
                                          'group not located on the identified '
                                          'steroid nucleus."'],
                           'returns_count': 9,
                           'complexity': 6.319023970026918},
    'message': '\n'
               'Attempt failed: F1 score of 0.02492539933298227 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: '
               'C[C@@]12C[C@@H]([C@]3([C@]([C@]2([H])CC[C@@]1(C(COP(=O)(O)O)=O)O)(CCC=4[C@]3(C)C=CC(C4)=O)[H])[H])O '
               'NAME: prednisolone phosphate REASON: CORRECT Steroid nucleus '
               'detected (fused cluster with requisite rings) and '
               'beta-oriented hydroxyl group found on it.\n'
               ' * SMILES: '
               'C[C@]12CCC(=O)C[C@H]1CC[C@H]1[C@@H]3CC[C@H](C(=O)CO)[C@]3(C[C@H](O)[C@H]21)C=O '
               'NAME: 5beta-dihydroaldosterone REASON: CORRECT Steroid nucleus '
               'detected (fused cluster with requisite rings) and '
               'beta-oriented hydroxyl group found on it.\n'
               ' * SMILES: '
               'C[C@@H]([C@H]1CC[C@H]2[C@@H]3C[C@H]4O[C@]44[C@@H](O)C=CC(=O)[C@]4(C)[C@H]3[C@@H](O)C[C@]12C)[C@H]1CC(C)=C(CO)C(=O)O1 '
               'NAME: withalongolide C REASON: CORRECT Steroid nucleus '
               'detected (fused cluster with requisite rings) and '
               'beta-oriented hydroxyl group found on it.\n'
               ' * SMILES: '
               '[H][C@@]12CCC3=CC(=O)C=C[C@]3(C)[C@@]1([H])[C@@H](O)C[C@@]1(C)[C@@]2([H])C[C@@H](C(=O)OC)[C@]1(O)C(=O)CO '
               'NAME: methyl prednisolone-16alpha-carboxylate REASON: CORRECT '
               'Steroid nucleus detected (fused cluster with requisite rings) '
               'and beta-oriented hydroxyl group found on it.\n'
               ' * SMILES: '
               '[H][C@@]12CCC3=CC(=O)C=C[C@]3(C)[C@@]1(F)[C@@H](O)C[C@@]1(C)[C@@]2([H])C[C@H]2OC3(CCCC3)O[C@@]12C(=O)COC(C)=O '
               'NAME: amcinonide REASON: CORRECT Steroid nucleus detected '
               '(fused cluster with requisite rings) and beta-oriented '
               'hydroxyl group found on it.\n'
               ' * SMILES: '
               '[H][C@@]12CC[C@](O)(C(=O)CO)[C@]1(C[C@H](O)[C@@]1([H])[C@@]2([H])CCC2=CC(=O)CC[C@]12C)C=O '
               'NAME: 18-oxocortisol REASON: CORRECT Steroid nucleus detected '
               '(fused cluster with requisite rings) and beta-oriented '
               'hydroxyl group found on it.\n'
               ' * SMILES: '
               'CC(=O)OCC(=O)[C@@]1(O)CC[C@H]2[C@@H]3C[C@H](F)C4=CC(=O)CC[C@]4(C)[C@H]3[C@@H](O)C[C@]12C '
               'NAME: 6alpha-fluoro-17-hydroxycorticosterone 21-acetate '
               'REASON: CORRECT Steroid nucleus detected (fused cluster with '
               'requisite rings) and beta-oriented hydroxyl group found on '
               'it.\n'
               ' * SMILES: '
               '[H][C@@]12C[C@@H](C)[C@](O)(C(=O)CO)[C@@]1(C)C[C@H](O)[C@@]1([H])[C@@]2([H])[C@H](Cl)CC2=CC(=O)C=C[C@]12C '
               'NAME: alclometasone REASON: CORRECT Steroid nucleus detected '
               '(fused cluster with requisite rings) and beta-oriented '
               'hydroxyl group found on it.\n'
               ' * SMILES: '
               '[H][C@@]12CC=C3C[C@@H](O)CC[C@]3(C)[C@@]1([H])[C@@H](O)C[C@@]1(C)[C@@]2([H])CC[C@]1(O)C(=O)CO '
               'NAME: 11beta,17alpha,21-trihydroxypregnenolone REASON: CORRECT '
               'Steroid nucleus detected (fused cluster with requisite rings) '
               'and beta-oriented hydroxyl group found on it.\n'
               ' * SMILES: '
               'C[C@H]1C[C@H]2[C@@H]3CC[C@](OC(C)=O)(C(C)=O)[C@@]3(C)C[C@H](O)[C@]2(F)[C@@]2(C)C=CC(=O)C=C12 '
               'NAME: fluorometholone acetate REASON: CORRECT Steroid nucleus '
               'detected (fused cluster with requisite rings) and '
               'beta-oriented hydroxyl group found on it.\n'
               ' * SMILES: '
               '[H][C@@]12CCC3=CC(=O)CC[C@]3(C)[C@@]1([H])[C@@H](O)C[C@@]1(C)[C@@]2([H])CC[C@]1(O)C(=O)CS '
               'NAME: tixocortol REASON: CORRECT Steroid nucleus detected '
               '(fused cluster with requisite rings) and beta-oriented '
               'hydroxyl group found on it.\n'
               ' * SMILES: '
               '[H][C@@]12C[C@@H](C)[C@](O)(C(=O)SCF)[C@@]1(C)C[C@H](O)[C@@]1(F)[C@@]2([H])C[C@H](F)C2=CC(=O)C=C[C@]12C '
               'NAME: fluticasone REASON: CORRECT Steroid nucleus detected '
               '(fused cluster with requisite rings) and beta-oriented '
               'hydroxyl group found on it.\n'
               ' * SMILES: '
               '[H][C@@]12C[C@@H](C)[C@H](C(=O)CO)[C@@]1(C)C[C@H](O)[C@@]1(Cl)[C@@]2([H])C[C@H](F)C2=CC(=O)C=C[C@]12C '
               'NAME: clocortolone REASON: CORRECT Steroid nucleus detected '
               '(fused cluster with requisite rings) and beta-oriented '
               'hydroxyl group found on it.\n'
               ' * SMILES: '
               '[H][C@@]12C[C@H](C)[C@](O)(C(=O)CO)[C@@]1(C)C[C@H](O)[C@@]1(F)[C@@]2([H])C[C@H](F)C2=CC(=O)C=C[C@]12C '
               'NAME: diflorasone REASON: CORRECT Steroid nucleus detected '
               '(fused cluster with requisite rings) and beta-oriented '
               'hydroxyl group found on it.\n'
               ' * SMILES: '
               'C1C(C=C2[C@](C1)([C@@]3([C@@](CC2)([C@]4([C@](C[C@@H]3O)([C@](CC4)(C(C)=O)O)C)[H])[H])[H])C)=O '
               'NAME: 21-deoxycortisol REASON: CORRECT Steroid nucleus '
               'detected (fused cluster with requisite rings) and '
               'beta-oriented hydroxyl group found on it.\n'
               ' * SMILES: '
               '[H][C@@]12C[C@@H](C)[C@](O)(C(=O)CO)[C@@]1(C)C[C@H](O)[C@@]1(F)[C@@]2([H])C[C@H](F)C2=CC(=O)C=C[C@]12C '
               'NAME: flumethasone REASON: CORRECT Steroid nucleus detected '
               '(fused cluster with requisite rings) and beta-oriented '
               'hydroxyl group found on it.\n'
               ' * SMILES: '
               'C[C@H]1C[C@H]2[C@@H]3CC[C@](O)(C(C)=O)[C@@]3(C)C[C@H](O)[C@]2(F)[C@@]2(C)C=CC(=O)C=C12 '
               'NAME: fluorometholone REASON: CORRECT Steroid nucleus detected '
               '(fused cluster with requisite rings) and beta-oriented '
               'hydroxyl group found on it.\n'
               ' * SMILES: '
               'C1C(C[C@@]2([C@](C1)([C@@]3([C@@](CC2)([C@@]4([H])[C@@](C[C@@H]3O)(C)[C@](CC4)(C(CO)=O)O)[H])[H])C)[H])=O '
               'NAME: 5beta-dihydrocortisol REASON: CORRECT Steroid nucleus '
               'detected (fused cluster with requisite rings) and '
               'beta-oriented hydroxyl group found on it.\n'
               ' * SMILES: '
               'C1[C@@]2([C@@]([C@@]3(C(C1)=CC(CC3)=O)C)([C@H](C[C@@]4([C@@](CC[C@@]24[H])(O)[C@@H](CO)O)C)O)[H])[H] '
               'NAME: 20beta-dihydrocortisol REASON: CORRECT Steroid nucleus '
               'detected (fused cluster with requisite rings) and '
               'beta-oriented hydroxyl group found on it.\n'
               ' * SMILES: '
               'C[C@H]1C[C@H]2[C@@H]3CC[C@](O)(C(=O)COC(C)=O)[C@@]3(C)C[C@H](O)[C@@H]2[C@@]2(C)C=CC(=O)C=C12 '
               'NAME: methylprednisolone acetate REASON: CORRECT Steroid '
               'nucleus detected (fused cluster with requisite rings) and '
               'beta-oriented hydroxyl group found on it.\n'
               ' * SMILES: '
               'C1=CC(C=C2[C@]1([C@@]3([C@@](CC2)([C@]4([C@](C[C@@H]3O)([C@]([C@@H](C4)C)(C(CO)=O)O)C)[H])[H])F)C)=O '
               'NAME: dexamethasone REASON: CORRECT Steroid nucleus detected '
               '(fused cluster with requisite rings) and beta-oriented '
               'hydroxyl group found on it.\n'
               ' * SMILES: '
               '[H][C@@]12C[C@H](C)[C@](O)(C(=O)COC(C)=O)[C@@]1(C)C[C@H](O)[C@@]1(F)[C@@]2([H])CCC2=CC(=O)C=C[C@]12C '
               'NAME: betamethasone acetate REASON: CORRECT Steroid nucleus '
               'detected (fused cluster with requisite rings) and '
               'beta-oriented hydroxyl group found on it.\n'
               ' * SMILES: '
               '[H][C@@]12CCC3=CC(=O)CC[C@]3(C)[C@@]1([H])[C@@H](O)C[C@@]1(C)[C@@]2([H])CC[C@]1(O)C(=O)COC(=O)CN(CC)CC '
               'NAME: hydrocortamate REASON: CORRECT Steroid nucleus detected '
               '(fused cluster with requisite rings) and beta-oriented '
               'hydroxyl group found on it.\n'
               ' * SMILES: '
               '[H][C@@]12C[C@@H](O)[C@](O)(C(=O)CO)[C@@]1(C)C[C@H](O)[C@@]1([H])[C@@]2([H])CCC2=CC(=O)C=C[C@]12C '
               'NAME: 16alpha-hydroxyprednisolone REASON: CORRECT Steroid '
               'nucleus detected (fused cluster with requisite rings) and '
               'beta-oriented hydroxyl group found on it.\n'
               ' * SMILES: '
               '[H][C@@]12C[C@H](C)[C@](O)(C(=O)CO)[C@@]1(C)C[C@H](O)[C@@]1(F)[C@@]2([H])CCC2=CC(=O)C=C[C@]12C '
               'NAME: betamethasone REASON: CORRECT Steroid nucleus detected '
               '(fused cluster with requisite rings) and beta-oriented '
               'hydroxyl group found on it.\n'
               'False positives: SMILES: '
               'CO[C@H]1C[C@H](O[C@H]2CC[C@@]3(C)[C@H](CC[C@@H]4[C@@H]3[C@H](O)C[C@]3(C)[C@H](CC[C@]43O)C3=CC(=O)OC3)C2)O[C@@H](C)[C@@H]1O '
               'NAME: Divaricoside REASON: WRONGLY CLASSIFIED Steroid nucleus '
               'detected (fused cluster with requisite rings) and '
               'beta-oriented hydroxyl group found on it.\n'
               ' * SMILES: '
               '[C@]1([C@@H](CCC(C(C)C)CC)C)([C@]2(CC[C@@]3([C@]4(CC[C@@H](C[C@]4(CC[C@]3([C@@]2(CC1)[H])[H])[H])O)C)[H])C)[H] '
               'NAME: 24-ethylcoprostanol REASON: WRONGLY CLASSIFIED Steroid '
               'nucleus detected (fused cluster with requisite rings) and '
               'beta-oriented hydroxyl group found on it.\n'
               ' * SMILES: '
               '[H][C@@]12CC(=O)[C@](O)(c3ccc4ccncc4c3)[C@@]1(C)CC=C1C=C3[C@@H](O)[C@H](O)[C@H](C[C@]33CC[C@]21O3)N(C)C '
               'NAME: cortistatin D REASON: WRONGLY CLASSIFIED Steroid nucleus '
               'detected (fused cluster with requisite rings) and '
               'beta-oriented hydroxyl group found on it.\n'
               ' * SMILES: '
               'C[C@H](CCC(=O)NCCCC(O)=O)[C@H]1CC[C@H]2[C@H]3[C@H](CC[C@]12C)[C@@]4(C)CC[C@@H](O)C[C@H]4CC3=O '
               'NAME: 7-oxo-gamma-aminoisobutyrolithocholic acid REASON: '
               'WRONGLY CLASSIFIED Steroid nucleus detected (fused cluster '
               'with requisite rings) and beta-oriented hydroxyl group found '
               'on it.\n'
               ' * SMILES: '
               'O=C1[C@@]2(C=C3C(=O)OC[C@@]43[C@]1([C@H]5O[C@H]6CC(=O)C([C@H]7[C@]6([C@@]5(O)[C@@]4(C2)CC7)C)(C)C)C)C '
               'NAME: Emeridone D REASON: WRONGLY CLASSIFIED Steroid nucleus '
               'detected (fused cluster with requisite rings) and '
               'beta-oriented hydroxyl group found on it.\n'
               ' * SMILES: '
               'C[C@@H]1C[C@@]2(C)[C@@H](CC[C@H]3[C@@H]4CC[C@H](O)[C@@]4(C)CC[C@H]23)C[C@@H]1O '
               'NAME: 2alpha-Methyl-5alpha-androstane-3alpha,17beta-diol '
               'REASON: WRONGLY CLASSIFIED Steroid nucleus detected (fused '
               'cluster with requisite rings) and beta-oriented hydroxyl group '
               'found on it.\n'
               ' * SMILES: '
               '[H][C@]12C[C@@]1([H])[C@]1(C)[C@@H](O)C(=O)\\C(=C(\\C)C(=O)OC)[C@@]3([H])C1=C2C[C@@]1([H])[C@@]2(C)[C@]4([H])C[C@]4([H])[C@](O)(C\\C(C)=C\\C(=O)OC)[C@@]2([H])CC2=C(CO)C(=O)O[C@]312 '
               'NAME: shizukaol C REASON: WRONGLY CLASSIFIED Steroid nucleus '
               'detected (fused cluster with requisite rings) and '
               'beta-oriented hydroxyl group found on it.\n'
               ' * SMILES: '
               '[C@]123[C@]([H])([C@@]4(C)[C@@](C5=C(CC4)OC=C5)(CC1)[H])CC[C@H](C2)[C@@](C3)(O)CO '
               'NAME: cafestol REASON: WRONGLY CLASSIFIED Steroid nucleus '
               'detected (fused cluster with requisite rings) and '
               'beta-oriented hydroxyl group found on it.\n'
               ' * SMILES: '
               '[C@@]123[C@@]4([C@]5([C@@](CC1=O)(C(CN([C@H](C2)O)C)=CCO[C@]5(CC(N4C6=C3C=CC=C6)=O)[H])[H])[H])[H] '
               'NAME: 5-hydroxyvomicine REASON: WRONGLY CLASSIFIED Steroid '
               'nucleus detected (fused cluster with requisite rings) and '
               'beta-oriented hydroxyl group found on it.\n'
               ' * SMILES: '
               'O=C1C2=C(O)C3=C(O)C=C(OC)C4=C3C(=C2C5(O)C6(C1(O)C(O)=C(C(=O)C6)C(=O)N)O5)CC74C(=CCCC7(C)C)C '
               'NAME: Viridicatumtoxin B REASON: WRONGLY CLASSIFIED Steroid '
               'nucleus detected (fused cluster with requisite rings) and '
               'beta-oriented hydroxyl group found on it.\n'
               ' * SMILES: '
               'O=C(OC)[C@@H](NC(=O)C[C@@](O)(CC(=O)O[C@H]1[C@H](O)C([C@@H]2CCC3=C([C@]2(C1)C)C[C@H](O)[C@]4([C@]3(CC[C@@H]4[C@@H](CC[C@@H](O)C(O)(C)C)C)C)C)(C)C)C)[C@@H](O)C5=CC=CC=C5 '
               'NAME: Pardinol C REASON: WRONGLY CLASSIFIED Steroid nucleus '
               'detected (fused cluster with requisite rings) and '
               'beta-oriented hydroxyl group found on it.\n'
               ' * SMILES: '
               'OC12C3(C(O)(C(O)C=C1C4C(C(CC4)C(C)/C=C(/C(C(C)C)C)\\C)(CC2)C)CC(O)CC3)C '
               'NAME: '
               '(3beta,5alpha,6beta,9alpha,22E,24R)-23-Methylergosta-7,22-diene-3,5,6,9-tetrol '
               'REASON: WRONGLY CLASSIFIED Steroid nucleus detected (fused '
               'cluster with requisite rings) and beta-oriented hydroxyl group '
               'found on it.\n'
               ' * SMILES: '
               'O1[C@]23[C@@]([C@@]4([C@@](OC5=C(C4)C(OC)=C6C(=C5C)COC6=O)(C[C@H]2O)C)[H])([C@H](OC(=O)C)C[C@@]1(OC3(C)C)OC)C '
               'NAME: Austalide D REASON: WRONGLY CLASSIFIED Steroid nucleus '
               'detected (fused cluster with requisite rings) and '
               'beta-oriented hydroxyl group found on it.\n'
               ' * SMILES: '
               'OC1C2C(C3(C(C4(C(CC3)C(C(OC5OC(C(O)C(O)C5OC6OC(C(O)C(O)C6O)CO)COC(=O)C)CC4)(C)C)C)C1)C)(CCC2C(OC7OC(C(O)C(O)C7O)CO)(CCC=C(C)C)C)C '
               'NAME: Quinquenoside III REASON: WRONGLY CLASSIFIED Steroid '
               'nucleus detected (fused cluster with requisite rings) and '
               'beta-oriented hydroxyl group found on it.\n'
               ' * SMILES: '
               'O[C@@H]1[C@]2([C@]([C@]3([C@@]([C@@]4([C@](CC3)(C[C@H](O)CC4)[H])C)(C1)[H])[H])(CC[C@@]2([C@@H](CCO)C)[H])[H])C '
               'NAME: 24-Nor-5beta-cholane-3alpha,12alpha,23-triol REASON: '
               'WRONGLY CLASSIFIED Steroid nucleus detected (fused cluster '
               'with requisite rings) and beta-oriented hydroxyl group found '
               'on it.\n'
               ' * SMILES: '
               'O=C1C(C2=CC=C3[C@]4([C@]([C@@H]([C@H](C(=O)O)CCC(=C)C(C)C)[C@@H](C4)O)(C)CC=C3[C@@]2(C)CC1)C)(C)C '
               'NAME: '
               '16alpha-hydroxy-3-oxo-24-methyllanosta-5,7,9(11),24(31)-tetraen-21-oic '
               'acid REASON: WRONGLY CLASSIFIED Steroid nucleus detected '
               '(fused cluster with requisite rings) and beta-oriented '
               'hydroxyl group found on it.\n'
               ' * SMILES: '
               'C1C[C@@H](C([C@@]2([C@@]1([C@]3([C@](CC2)([C@]4([C@@](C(=C3)C)(C(C(=C4O)C)=O)C)C(OC)=O)C)[H])CO)[H])(C)C)OC(C)=O '
               'NAME: andrastin B REASON: WRONGLY CLASSIFIED Steroid nucleus '
               'detected (fused cluster with requisite rings) and '
               'beta-oriented hydroxyl group found on it.\n'
               ' * SMILES: '
               '[H][C@@]12CC[C@]3(C)[C@]([H])(CC[C@]45OC[C@@]6(CC[C@](C)(CO)C[C@@]46[H])[C@H](O)C[C@@]35C)[C@@]1(C)CC[C@H](O)C2(C)C '
               'NAME: (3beta,16alpha)-13,28-epoxyoleanane-3,16,30-triol '
               'REASON: WRONGLY CLASSIFIED Steroid nucleus detected (fused '
               'cluster with requisite rings) and beta-oriented hydroxyl group '
               'found on it.\n'
               ' * SMILES: '
               'O1[C@@]23[C@@]([C@@H]4C([C@H]5[C@]([C@@H]([C@@H](/C=C/[C@@H](C(C)C)C)C)CC5)(C)CC4)=C[C@@H]2O)(CC[C@@H]([C@H]13)O)C '
               'NAME: Gargalol A REASON: WRONGLY CLASSIFIED Steroid nucleus '
               'detected (fused cluster with requisite rings) and '
               'beta-oriented hydroxyl group found on it.\n'
               ' * SMILES: '
               'O(C1C2C(C3C(C4(C(C(CC4)C5(OC(CC5)C(O)(C)C)C)C(O)C3)C)(C1)C)(CCC(O)C2(C)C)C)C6OC(C(O)C(O)C6OC7OCC(O)C(O)C7O)COC8OC(C(O)C(O)C8O)CO '
               'NAME: Vinaginsenoside R6 REASON: WRONGLY CLASSIFIED Steroid '
               'nucleus detected (fused cluster with requisite rings) and '
               'beta-oriented hydroxyl group found on it.\n'
               ' * SMILES: '
               'C1[C@@]2(C=3CC[C@]4(C(C3CC[C@]2(C([C@H](C1)O)(C)C)[H])=CC[C@@]4([C@H](C)CCC(C(C)C)=C)[H])C)C '
               'NAME: '
               '4,4,24-trimethyl-5alpha-cholesta-8,14,24(28)-triene-3beta-ol '
               'REASON: WRONGLY CLASSIFIED Steroid nucleus detected (fused '
               'cluster with requisite rings) and beta-oriented hydroxyl group '
               'found on it.\n'
               ' * SMILES: '
               'O=C1C=C2C(=C(O)C[C@@H]3[C@@]2(CCC(C3(C)C)=O)C)[C@]4([C@]1(C(=CC4=O)[C@@](O)(CC(=O)C[C@@H](C(=O)O)C)C)C)C '
               'NAME: Applanoic acid D REASON: WRONGLY CLASSIFIED Steroid '
               'nucleus detected (fused cluster with requisite rings) and '
               'beta-oriented hydroxyl group found on it.\n'
               ' * SMILES: '
               '[H][C@@]1(CC[C@@]2([H])[C@]3([H])CC=C4C[C@@H](O)CC[C@]4(C)[C@@]3([H])CC[C@]12C)[C@H](C)[C@@H](O)C[C@@H](CC)C(C)C '
               'NAME: (22S)-hydroxysitosterol REASON: WRONGLY CLASSIFIED '
               'Steroid nucleus detected (fused cluster with requisite rings) '
               'and beta-oriented hydroxyl group found on it.\n'
               ' * SMILES: '
               'C1[C@@]2([C@]3(C[C@@H]([C@]4([C@]([C@@]3([C@H](C[C@@]2(C[C@@H](C1)O)[H])O)[H])(CC[C@]4([H])[C@@H](CCC(NCCS([O-])(=O)=O)=O)C)[H])C)O)[H])C '
               'NAME: tauroursocholate REASON: WRONGLY CLASSIFIED Steroid '
               'nucleus detected (fused cluster with requisite rings) and '
               'beta-oriented hydroxyl group found on it.\n'
               ' * SMILES: '
               'O=C1C(OC)=C(C(=O)C=2C1=C(O)C3=C(C(=O)C4(O)C5C3OC4(C(O[C@@H]6O[C@@H]([C@@H](O[C@H]7O[C@@H]([C@@](O)(C(=O)C)[C@H](C7)O)C)CC6)C)C(C5OC8O[C@H]([C@H](O)[C@@H](C8)O)C)O)CCC)C2O)C=9C(OC)=C(OC)C%10=CC=%11CC%12C(O[C@@H]%13O[C@H]([C@H](O)[C@@H](C%13)O)C)C(O)C(C(C%12(C(C%11C(=C%10C9O)O)=O)O)(O)CCC)O[C@@H]%14O[C@@H]([C@@H](O[C@H]%15O[C@@H]([C@@](O)(C(=O)C)[C@H](C%15)O)C)CC%14)C '
               'NAME: Hibarimicin G REASON: WRONGLY CLASSIFIED Steroid nucleus '
               'detected (fused cluster with requisite rings) and '
               'beta-oriented hydroxyl group found on it.\n'
               'False negatives: NONE\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'O=C(N[C@@H](C(O)(C)C)C)[C@H]([C@@]1([C@@]2([C@@](CC1)(/C(/CCC2)=C/C=C\\3/C[C@@H](O)C[C@H](O)C3=C)[H])C)[H])C',
                                     'name': '1alpha,25-dihydroxy-24-oxo-23-azavitamin '
                                             'D2 / '
                                             '1alpha,25-dihydroxy-24-oxo-23-azaergocalciferol',
                                     'reason': 'Only 3 rings of size 5 or 6 '
                                               'found; a steroid nucleus (>=4 '
                                               'rings) is expected.'},
                                 {   'smiles': 'CCCCCCCCCCCCCCCCCCC(O)C([O-])=O',
                                     'name': '2-hydroxyarachidate',
                                     'reason': 'No rings detected; not a '
                                               'steroid.'},
                                 {   'smiles': 'C[C@@H](CN([C@@H](C)CO)C(=O)NC1=CC=C(C=C1)C(F)(F)F)[C@@H](CN(C)C(=O)C2CCOCC2)OC',
                                     'name': 'N-[(2S,3S)-4-[[(2S)-1-hydroxypropan-2-yl]-[[4-(trifluoromethyl)phenyl]carbamoyl]amino]-2-methoxy-3-methylbutyl]-N-methyloxane-4-carboxamide',
                                     'reason': 'Only 2 rings of size 5 or 6 '
                                               'found; a steroid nucleus (>=4 '
                                               'rings) is expected.'},
                                 {   'smiles': 'CC(=O)CC\\C=C(/C)CCC=C(C)C',
                                     'name': 'geranyl acetone',
                                     'reason': 'No rings detected; not a '
                                               'steroid.'},
                                 {   'smiles': 'O([C@H]1[C@H](O)[C@H](O[C@H](O)[C@H]1O)CO[C@H]2O[C@@H]([C@@H](O)[C@H](O)[C@@H]2O)CO)[C@H]3O[C@@H]([C@@H](O)[C@H](O)[C@@H]3O[C@H]4O[C@@H]([C@@H](O)[C@H](O)[C@@H]4O)CO)CO',
                                     'name': '(2S,3S,4S,5S,6R)-2-[[(2R,3R,4S,5S,6S)-4-[(2R,3S,4S,5S,6R)-4,5-Dihydroxy-6-(hydroxymethyl)-3-[(2R,3S,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-3,5,6-trihydroxyoxan-2-yl]methoxy]-6-(hydroxymethyl)oxane-3,4,5-triol',
                                     'reason': 'No fused steroid nucleus (with '
                                               '>=3 six-membered rings and 1 '
                                               'five-membered ring and '
                                               'appropriate carbon count) '
                                               'detected.'},
                                 {   'smiles': 'O=C(OC1=C(C(O)=C(C(=O)O)C(=C1C)C)C)C2=C(OC)C(=C(OC(=O)C3=C(O)C=C(O)C=C3C)C=C2C)C',
                                     'name': 'Thielavin Z5',
                                     'reason': 'Only 3 rings of size 5 or 6 '
                                               'found; a steroid nucleus (>=4 '
                                               'rings) is expected.'},
                                 {   'smiles': '[C@@H]1([C@@H]([C@H]([C@@H]([C@H](O1)CO)O)O)NC(C)=O)O[C@@H]2[C@@H]([C@H](C(O[C@@H]2CO)O)O)O',
                                     'name': 'beta-D-GlcpNAc-(1->4)-D-Galp',
                                     'reason': 'Only 2 rings of size 5 or 6 '
                                               'found; a steroid nucleus (>=4 '
                                               'rings) is expected.'},
                                 {   'smiles': 'CN(C)C(=O)C1=CC=C(C=C1)C2=CC=C(C=C2)[C@@H]3[C@H]4CN(CC(=O)N4[C@H]3CO)C(=O)CC5CC5',
                                     'name': '4-[4-[(6S,7R,8R)-4-(2-cyclopropyl-1-oxoethyl)-8-(hydroxymethyl)-2-oxo-1,4-diazabicyclo[4.2.0]octan-7-yl]phenyl]-N,N-dimethylbenzamide',
                                     'reason': 'Only 3 rings of size 5 or 6 '
                                               'found; a steroid nucleus (>=4 '
                                               'rings) is expected.'},
                                 {   'smiles': 'CCCCCCCCCCCCCCCCCCCCC=C',
                                     'name': '1-docosene',
                                     'reason': 'No rings detected; not a '
                                               'steroid.'},
                                 {   'smiles': 'C([C@@](OC(=O)CCC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)([H])COC(=O)CC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)OC(=O)CCCCC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC',
                                     'name': 'TG(22:5(7Z,10Z,13Z,16Z,19Z)/20:5(5Z,8Z,11Z,14Z,17Z)/22:6(4Z,7Z,10Z,13Z,16Z,19Z))[iso6]',
                                     'reason': 'No rings detected; not a '
                                               'steroid.'}],
    'sample_false_negatives': [],
    'attempt': 5,
    'reasoning': 'Below is my reasoning, followed by the complete Python '
                 'code.\n'
                 '\n'
                 'We saw that the previous heuristic almost worked but also '
                 'picked up many false‐positives. In our revised approach we '
                 'try to be more “steroid‐specific” by not only building a '
                 'fused ring graph but then restricting the rings to only '
                 'those of sizes 5 or 6 (as the steroid nucleus is the '
                 'cyclopentanoperhydrophenanthrene system) and then checking '
                 'that the union of the atoms in the fused cluster (and '
                 'especially the carbon atoms) falls in a narrow range '
                 '(roughly17, allowing some variation). This extra size/count '
                 'check should reduce cases where other types of fused rings '
                 'are mis‐interpreted as steroid nuclei. We then only accept a '
                 'beta–OH (using the SMARTS "[C@@]([OX2H])") if its carbon '
                 'lies within the identified steroid nucleus. (Note that many '
                 'steroids already have defined stereochemistry; we hope that '
                 'this extra filtering based on the ring atom count helps with '
                 'false positives.) \n'
                 '\n'
                 'Below is the complete code.\n'
                 '\n'
                 '------------------------------------------------',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 71,
    'num_false_positives': 4761,
    'num_true_negatives': 137468,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.014693708609271524,
    'recall': 1.0,
    'f1': 0.02896186008566184,
    'accuracy': 0.9665425158116655,
    'negative_predictive_value': 1.0}