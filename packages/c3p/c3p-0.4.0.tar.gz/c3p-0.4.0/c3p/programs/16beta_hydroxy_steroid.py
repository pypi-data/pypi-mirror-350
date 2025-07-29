"""
Classifies: CHEBI:17354 16beta-hydroxy steroid
"""
"""
Classifies: CHEBI:16β–hydroxy steroid
Definition: A 16–hydroxy steroid in which the hydroxy group at position 16 has a beta–configuration.
Heuristic improvements over the previous attempt:
  1. We again extract rings of size 5 or 6 and group fused rings.
  2. For each connected component with ≥4 rings we examine all sets of exactly 4 fused rings.
  3. We now require that among these four rings there is exactly one 5–membered ring and exactly three 6–membered rings.
  4. Critically, we require that the union of atoms in the four rings (i.e. the steroid nucleus) contains exactly 17 carbon atoms.
  5. Then—in the candidate D–ring (the only 5–membered ring)—we require that at least one carbon atom, which has defined stereochemistry,
     is directly bound (by a single bond) to an oxygen atom that appears to be a hydroxyl group (i.e. with at least one hydrogen).
     
NOTE: This heuristic still does not capture all steroid variants perfectly but it is tuned to reduce false positives.
"""
from rdkit import Chem
from rdkit.Chem import rdchem
from itertools import combinations

def is_16beta_hydroxy_steroid(smiles: str):
    """
    Determines if a molecule is a 16β–hydroxy steroid via an improved heuristic.
    The molecule must possess a fused four–ring system (steroid nucleus) composed of three six–membered rings 
    and one five–membered ring. The union of atoms in these rings must yield exactly 17 carbon atoms.
    In the unique five–membered ring (candidate D–ring) at least one carbon with defined stereochemistry 
    must have a single bond to an oxygen that appears to be an –OH group (has at least one hydrogen).

    Args:
        smiles (str): SMILES string of the molecule.

    Returns:
        bool: True if molecule qualifies as a 16β–hydroxy steroid (by our heuristic), False otherwise.
        str: Explanation for the classification.
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
    
    # First ensure stereochemistry is perceived
    Chem.AssignStereochemistry(mol, force=True)
    
    # Retrieve all ring systems from the molecule and restrict to rings of size 5 or 6.
    ring_info = mol.GetRingInfo()
    all_rings = ring_info.AtomRings()  # Each is a tuple of atom indices.
    rings_5_6 = []
    for ring in all_rings:
        if len(ring) in (5, 6):
            rings_5_6.append(set(ring))
    if not rings_5_6:
        return False, "No rings of size 5 or 6 found; cannot be a steroid nucleus"
    
    # Build a graph where nodes represent rings (from rings_5_6) and edges connect rings sharing >=2 atoms.
    num_rings = len(rings_5_6)
    ring_graph = {i: set() for i in range(num_rings)}
    for i in range(num_rings):
        for j in range(i+1, num_rings):
            if len(rings_5_6[i].intersection(rings_5_6[j])) >= 2:
                ring_graph[i].add(j)
                ring_graph[j].add(i)
    
    # Find connected components of rings.
    seen = set()
    components = []
    for i in range(num_rings):
        if i not in seen:
            stack = [i]
            comp = set()
            while stack:
                current = stack.pop()
                if current not in seen:
                    seen.add(current)
                    comp.add(current)
                    stack.extend(ring_graph[current])
            components.append(comp)
    
    candidate_nucleus = None
    candidate_D_ring = None  # this is the unique 5–membered ring in the nucleus.
    
    # Look in each connected component for a combination of exactly 4 rings with the required properties.
    for comp in components:
        if len(comp) < 4:
            continue
        comp_list = list(comp)
        for comb in combinations(comp_list, 4):
            rings_subset = [rings_5_6[i] for i in comb]
            # Check ring size distribution: exactly 1 five-membered and 3 six-membered rings.
            count5 = sum(1 for ring in rings_subset if len(ring) == 5)
            count6 = sum(1 for ring in rings_subset if len(ring) == 6)
            if count5 != 1 or count6 != 3:
                continue
            # Verify connectivity: each ring in the subset must be fused (share >=2 atoms) with at least one other ring.
            mini_connected = True
            for i in range(4):
                if not any(i != j and len(rings_subset[i].intersection(rings_subset[j])) >= 2 
                           for j in range(4)):
                    mini_connected = False
                    break
            if not mini_connected:
                continue
            # Get the union of all atoms in the candidate nucleus.
            union_atoms = set()
            for ring in rings_subset:
                union_atoms.update(ring)
            # Count carbon atoms among these atoms.
            c_count = sum(1 for idx in union_atoms if mol.GetAtomWithIdx(idx).GetAtomicNum() == 6)
            # For a classical steroid nucleus (cyclopentanoperhydrophenanthrene) there should be exactly 17 carbons.
            if c_count != 17:
                continue
            
            # Identify the candidate D–ring (the only 5-membered ring).
            for ring in rings_subset:
                if len(ring) == 5:
                    # Require that the 5-membered ring is fused with at least one six–membered ring (by >=2 atoms).
                    if not any((len(ring.intersection(other)) >= 2) for other in rings_subset if other is not ring and len(other) == 6):
                        continue
                    candidate_D_ring = ring
                    candidate_nucleus = union_atoms
                    break
            if candidate_nucleus is not None and candidate_D_ring is not None:
                break
        if candidate_nucleus is not None:
            break
    
    if candidate_nucleus is None:
        return False, "No fused 4–ring steroid nucleus (three 6–membered and one 5–membered rings with exactly 17 carbons) found"
    
    # Within the candidate D–ring, look for a carbon (with defined chiral tag) that is directly bonded (single bond)
    # to an oxygen atom that appears to be in an –OH group (has at least one hydrogen).
    found_16beta_oh = False
    for idx in candidate_D_ring:
        atom = mol.GetAtomWithIdx(idx)
        if atom.GetAtomicNum() != 6:
            continue
        # Exclude atoms without a specified chiral center.
        if atom.GetChiralTag() == rdchem.ChiralType.CHI_UNSPECIFIED:
            continue
        # Check neighbors for an oxygen bound by a single bond.
        for nb in atom.GetNeighbors():
            if nb.GetAtomicNum() != 8:
                continue
            bond = mol.GetBondBetweenAtoms(atom.GetIdx(), nb.GetIdx())
            if bond is None or bond.GetBondType() != rdchem.BondType.SINGLE:
                continue
            if nb.GetTotalNumHs() < 1:
                continue
            # If we reach here, this atom represents a chiral center in the D–ring with an –OH.
            found_16beta_oh = True
            break
        if found_16beta_oh:
            break
    
    if not found_16beta_oh:
        return False, "Steroid nucleus found but no chiral carbon with a directly attached –OH in the D–ring was detected"
    
    return True, ("Molecule contains a fused steroid nucleus (three 6–membered and one 5–membered rings with exactly 17 carbons) "
                  "and the candidate D–ring has a chiral carbon bearing an –OH group (heuristic for 16β–hydroxy steroid)")

# Example usage:
if __name__ == '__main__':
    # Test example: 16beta-hydroxytestosterone
    test_smiles = "C[C@]12CC[C@H]3[C@@H](CCC4=CC(=O)CC[C@]34C)[C@@H]1C[C@H](O)[C@@H]2O"
    result, reason = is_16beta_hydroxy_steroid(test_smiles)
    print("Result:", result)
    print("Reason:", reason)


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:17354',
                          'name': '16beta-hydroxy steroid',
                          'definition': 'A 16-hydroxy steroid in which the '
                                        'hydroxy group at position 16 has a '
                                        'beta-configuration.',
                          'parents': ['CHEBI:36840'],
                          'xrefs': [   'KEGG:C03050',
                                       'MetaCyc:16-BETA-HYDROXYSTEROID'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 128,
                           'log_lines_of_code': 4.852030263919617,
                           'indent_by_line': [   1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 0,
                                                 1,
                                                 2,
                                                 0,
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
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 3,
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
                                                 1,
                                                 1,
                                                 2,
                                                 3,
                                                 2,
                                                 2,
                                                 3,
                                                 3,
                                                 3,
                                                 3,
                                                 3,
                                                 4,
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
                                                 4,
                                                 3,
                                                 3,
                                                 3,
                                                 3,
                                                 4,
                                                 3,
                                                 3,
                                                 3,
                                                 4,
                                                 5,
                                                 5,
                                                 6,
                                                 5,
                                                 5,
                                                 5,
                                                 3,
                                                 4,
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
                                                 2,
                                                 2,
                                                 3,
                                                 2,
                                                 2,
                                                 3,
                                                 2,
                                                 2,
                                                 3,
                                                 4,
                                                 3,
                                                 3,
                                                 4,
                                                 3,
                                                 4,
                                                 3,
                                                 3,
                                                 3,
                                                 2,
                                                 3,
                                                 1,
                                                 1,
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1],
                           'max_indent': 6,
                           'imports': [   'from rdkit import Chem',
                                          'from rdkit.Chem import rdchem',
                                          'from itertools import combinations'],
                           'imports_count': 3,
                           'methods_called': [   'GetBondType',
                                                 'extend',
                                                 'update',
                                                 'MolFromSmiles',
                                                 'GetNeighbors',
                                                 'GetTotalNumHs',
                                                 'GetBondBetweenAtoms',
                                                 'GetRingInfo',
                                                 'append',
                                                 'GetAtomWithIdx',
                                                 'AssignStereochemistry',
                                                 'GetChiralTag',
                                                 'GetAtomicNum',
                                                 'AtomRings',
                                                 'GetIdx',
                                                 'intersection',
                                                 'add',
                                                 'pop'],
                           'methods_called_count': 18,
                           'smarts_strings': [],
                           'smarts_strings_count': 0,
                           'defs': ['is_16beta_hydroxy_steroid(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "No rings of size 5 or 6 '
                                          'found; cannot be a steroid nucleus"',
                                          'False, "No fused 4–ring steroid '
                                          'nucleus (three 6–membered and one '
                                          '5–membered rings with exactly 17 '
                                          'carbons) found"',
                                          'False, "Steroid nucleus found but '
                                          'no chiral carbon with a directly '
                                          'attached –OH in the D–ring was '
                                          'detected"',
                                          'True, ("Molecule contains a fused '
                                          'steroid nucleus (three 6–membered '
                                          'and one 5–membered rings with '
                                          'exactly 17 carbons) "'],
                           'returns_count': 5,
                           'complexity': 6.970406052783924},
    'message': '\n'
               'Attempt failed: F1 score of 0.023984010659560292 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: '
               'C[C@]12CC[C@H]3[C@@H](CCC4=CC(=O)CC[C@]34C)[C@@H]1C[C@H](O)[C@@H]2O '
               'NAME: 16beta-hydroxytestosterone REASON: CORRECT Molecule '
               'contains a fused steroid nucleus (3 six–membered and 1 '
               'five–membered rings, ~17 carbons) and the candidate D–ring has '
               'a chiral carbon bearing an –OH group (heuristic for '
               '16β–hydroxy steroid)\n'
               ' * SMILES: '
               '[H][C@]1([C@H](C)CCC[C@H](C)CO)[C@@H](O)[C@H](O)C2[C@]1(C)CCC1[C@@]3(C)CC[C@H](O)CC3[C@H](O)[C@@H](O)[C@@]21O '
               'NAME: '
               '(9xi,14xi,25S)-cholestane-3beta,6beta,7alpha,8,15alpha,16beta,26-heptol '
               'REASON: CORRECT Molecule contains a fused steroid nucleus (3 '
               'six–membered and 1 five–membered rings, ~17 carbons) and the '
               'candidate D–ring has a chiral carbon bearing an –OH group '
               '(heuristic for 16β–hydroxy steroid)\n'
               ' * SMILES: '
               'C[C@@]12C[C@@H](O)C[C@H]1[C@@H]1CCc3cc(O)ccc3[C@H]1CC2 NAME: '
               'estra-1,3,5(10)-triene-3,16beta-diol REASON: CORRECT Molecule '
               'contains a fused steroid nucleus (3 six–membered and 1 '
               'five–membered rings, ~17 carbons) and the candidate D–ring has '
               'a chiral carbon bearing an –OH group (heuristic for '
               '16β–hydroxy steroid)\n'
               ' * SMILES: '
               '[H][C@]1([C@H](C)[C@@H](O)CCC(C)C)[C@@H](O)C[C@@]2([H])[C@]3([H])CC=C4C[C@@H](O)CC[C@]4(C)[C@@]3([H])CC[C@]12C '
               'NAME: (16S,22S)-dihydroxycholesterol REASON: CORRECT Molecule '
               'contains a fused steroid nucleus (3 six–membered and 1 '
               'five–membered rings, ~17 carbons) and the candidate D–ring has '
               'a chiral carbon bearing an –OH group (heuristic for '
               '16β–hydroxy steroid)\n'
               ' * SMILES: '
               '[H][C@]12CC[C@]3([H])[C@]([H])(CC[C@]4(C)[C@]([H])([C@@H](O)C[C@]34O)C3=CC(=O)OC3)[C@]1(CC[C@H](O)C2)C=O '
               'NAME: adonitoxigenin REASON: CORRECT Molecule contains a fused '
               'steroid nucleus (3 six–membered and 1 five–membered rings, ~17 '
               'carbons) and the candidate D–ring has a chiral carbon bearing '
               'an –OH group (heuristic for 16β–hydroxy steroid)\n'
               ' * SMILES: '
               '[H][C@]1([C@H](C)CCC[C@H](C)CO)[C@@H](O)[C@H](O)C2[C@]1(C)CCC1[C@@]3(C)CC[C@H](O)[C@H](O)C3[C@H](O)[C@@H](O)[C@@]21O '
               'NAME: '
               '(9xi,14xi,25S)-cholestane-3beta,4beta,6beta,7alpha,8,15alpha,16beta,26-octol '
               'REASON: CORRECT Molecule contains a fused steroid nucleus (3 '
               'six–membered and 1 five–membered rings, ~17 carbons) and the '
               'candidate D–ring has a chiral carbon bearing an –OH group '
               '(heuristic for 16β–hydroxy steroid)\n'
               ' * SMILES: '
               '[H][C@]1([C@H](C)CCC[C@H](C)CO)[C@@H](O)[C@H](O)C2[C@]1(C)CCC1[C@@]2(O)C[C@H](O)C2C[C@@H](O)CC[C@]12C '
               'NAME: '
               '(9xi,14xi,25S)-cholestane-3beta,6alpha,8,15alpha,16beta,26-hexol '
               'REASON: CORRECT Molecule contains a fused steroid nucleus (3 '
               'six–membered and 1 five–membered rings, ~17 carbons) and the '
               'candidate D–ring has a chiral carbon bearing an –OH group '
               '(heuristic for 16β–hydroxy steroid)\n'
               ' * SMILES: '
               'C1=C2C(CC[C@]3([C@@]4(C[C@@H]([C@@H]([C@]4(CC[C@@]32[H])C)O)O)[H])[H])=CC(=C1)O '
               'NAME: 16beta-hydroxyestradiol REASON: CORRECT Molecule '
               'contains a fused steroid nucleus (3 six–membered and 1 '
               'five–membered rings, ~17 carbons) and the candidate D–ring has '
               'a chiral carbon bearing an –OH group (heuristic for '
               '16β–hydroxy steroid)\n'
               ' * SMILES: '
               '[H][C@]1(O[C@@H](C)[C@@H](OC(C)=O)[C@@H](O)[C@@H]1O)O[C@H]1CC[C@@]2(C)C(C1)=C[C@H](O)[C@]1([H])[C@]2([H])CC[C@@]2(C)[C@@]1([H])C[C@H](O)[C@]2([H])[C@H](C)CCC(=C)C(C)C '
               'NAME: sinularia glycoside REASON: CORRECT Molecule contains a '
               'fused steroid nucleus (3 six–membered and 1 five–membered '
               'rings, ~17 carbons) and the candidate D–ring has a chiral '
               'carbon bearing an –OH group (heuristic for 16β–hydroxy '
               'steroid)\n'
               ' * SMILES: '
               'O[C@]12[C@]3([C@@]([C@]([C@@H](O)[C@@H]3O)([C@@H](CCC[C@@H](CO)C)C)[H])(CC[C@@]1([C@@]4([C@@]([C@@H](O)[C@H]2O)([C@@H](O)[C@@H](O)CC4)[H])C)[H])C)[H] '
               'NAME: '
               '(25S)-5alpha-cholestan-3beta,4beta,6alpha,7beta,8beta,15alpha,16beta,26-octol '
               'REASON: CORRECT Molecule contains a fused steroid nucleus (3 '
               'six–membered and 1 five–membered rings, ~17 carbons) and the '
               'candidate D–ring has a chiral carbon bearing an –OH group '
               '(heuristic for 16β–hydroxy steroid)\n'
               ' * SMILES: '
               'O[C@]12[C@]3([C@@]([C@]([C@@H](O)[C@@H]3O)([C@@H](CCC[C@@H](CO)C)C)[H])(CC[C@@]1([C@@]4([C@@]([C@@H](O)C2)(C[C@@H](O)CC4)[H])C)[H])C)[H] '
               'NAME: '
               '(25S)-5alpha-cholestan-3beta,6alpha,8beta,15alpha,16beat,26-hexol '
               'REASON: CORRECT Molecule contains a fused steroid nucleus (3 '
               'six–membered and 1 five–membered rings, ~17 carbons) and the '
               'candidate D–ring has a chiral carbon bearing an –OH group '
               '(heuristic for 16β–hydroxy steroid)\n'
               ' * SMILES: '
               '[H][C@@]12C[C@H](O)[C@]([H])([C@H](C)C(=O)CCC(C)C)[C@@]1(C)CC[C@@]1([H])[C@@]2([H])CC=C2C[C@@H](O)CC[C@]12C '
               'NAME: (16S)-hydroxy-22-oxocholesterol REASON: CORRECT Molecule '
               'contains a fused steroid nucleus (3 six–membered and 1 '
               'five–membered rings, ~17 carbons) and the candidate D–ring has '
               'a chiral carbon bearing an –OH group (heuristic for '
               '16β–hydroxy steroid)\n'
               ' * SMILES: '
               '[H][C@@]12CCC3C[C@H](OS(O)(=O)=O)[C@H](C[C@]3(C)[C@@]1([H])CC[C@]1(C)[C@@]([H])([C@H](C)C(OC(=O)CCC)C(OC(=O)CCC)C(CC)C(C)C)[C@@H](O)[C@H](OC(C)=O)[C@@]21[H])OS(O)(=O)=O '
               'NAME: clathsterol disulfonic acid REASON: CORRECT Molecule '
               'contains a fused steroid nucleus (3 six–membered and 1 '
               'five–membered rings, ~17 carbons) and the candidate D–ring has '
               'a chiral carbon bearing an –OH group (heuristic for '
               '16β–hydroxy steroid)\n'
               ' * SMILES: '
               '[H][C@@]12C[C@H](O)[C@H](O)[C@@]1(C)CC[C@@]1([H])[C@@]2([H])CC=C2C[C@H](O)CC[C@]12C '
               'NAME: androst-5-ene-3alpha,16beta,17beta-triol REASON: CORRECT '
               'Molecule contains a fused steroid nucleus (3 six–membered and '
               '1 five–membered rings, ~17 carbons) and the candidate D–ring '
               'has a chiral carbon bearing an –OH group (heuristic for '
               '16β–hydroxy steroid)\n'
               ' * SMILES: '
               '[H][C@]12CC[C@]3([H])[C@]([H])(C[C@@H](O)[C@]4(C)[C@]([H])([C@@H](O)C[C@]34O)C3=CC(=O)OC3)[C@@]1(C)CC[C@H](O)C2 '
               'NAME: diginatigenin REASON: CORRECT Molecule contains a fused '
               'steroid nucleus (3 six–membered and 1 five–membered rings, ~17 '
               'carbons) and the candidate D–ring has a chiral carbon bearing '
               'an –OH group (heuristic for 16β–hydroxy steroid)\n'
               ' * SMILES: '
               '[H][C@]12CC[C@]3([H])[C@]([H])(CC[C@]4(C)[C@]([H])([C@@H](O)C[C@]34O)C3=CC(=O)OC3)[C@@]1(C)CC[C@H](O)C2 '
               'NAME: gitoxigenin REASON: CORRECT Molecule contains a fused '
               'steroid nucleus (3 six–membered and 1 five–membered rings, ~17 '
               'carbons) and the candidate D–ring has a chiral carbon bearing '
               'an –OH group (heuristic for 16β–hydroxy steroid)\n'
               ' * SMILES: '
               'C1[C@]2([C@]3([C@@](C4=C(C=C(O)C=C4)CC3)(CC[C@@]2(C(=O)[C@H]1O)C)[H])[H])[H] '
               'NAME: 16beta-hydroxyestrone REASON: CORRECT Molecule contains '
               'a fused steroid nucleus (3 six–membered and 1 five–membered '
               'rings, ~17 carbons) and the candidate D–ring has a chiral '
               'carbon bearing an –OH group (heuristic for 16β–hydroxy '
               'steroid)\n'
               ' * SMILES: '
               '[H][C@]12CC[C@]3([H])[C@]([H])(CC[C@]4(C)[C@]([H])([C@@H](O)C[C@]34O)C3=CC(=O)OC3)[C@@]1(C)CC[C@@H](C2)OC(C)=O '
               'NAME: gitoxigenin 3-acetate REASON: CORRECT Molecule contains '
               'a fused steroid nucleus (3 six–membered and 1 five–membered '
               'rings, ~17 carbons) and the candidate D–ring has a chiral '
               'carbon bearing an –OH group (heuristic for 16β–hydroxy '
               'steroid)\n'
               'False positives: SMILES: '
               'C[C@@]12CCC[C@](C)([C@H]1CC[C@@]13C[C@@H](CC[C@@H]21)[C@](O)(CO)C3)C(O)=O '
               'NAME: 16beta,17-dihydroxy-ent-kaurane-19-oic acid REASON: '
               'WRONGLY CLASSIFIED Molecule contains a fused steroid nucleus '
               '(3 six–membered and 1 five–membered rings, ~17 carbons) and '
               'the candidate D–ring has a chiral carbon bearing an –OH group '
               '(heuristic for 16β–hydroxy steroid)\n'
               ' * SMILES: '
               '[H][C@]12CC[C@]3(C)[C@@H](O)CC[C@@]3([H])[C@]1([H])CCc1cc(OC(=O)N(CCCl)CCCl)ccc21 '
               'NAME: estramustine REASON: WRONGLY CLASSIFIED Molecule '
               'contains a fused steroid nucleus (3 six–membered and 1 '
               'five–membered rings, ~17 carbons) and the candidate D–ring has '
               'a chiral carbon bearing an –OH group (heuristic for '
               '16β–hydroxy steroid)\n'
               ' * SMILES: '
               '[H][C@@]12C[C@H](O)[C@@]3([H])C(C)(C)[C@@H](O)CC[C@@]33C[C@@]13CC[C@]1(C)[C@]([H])([C@@H](O)C[C@@]21C)[C@@]1(C)CC[C@H](O1)C(C)(C)O '
               'NAME: cycloastragenol REASON: WRONGLY CLASSIFIED Molecule '
               'contains a fused steroid nucleus (3 six–membered and 1 '
               'five–membered rings, ~17 carbons) and the candidate D–ring has '
               'a chiral carbon bearing an –OH group (heuristic for '
               '16β–hydroxy steroid)\n'
               ' * SMILES: '
               '[H][C@@]12CCC3CC(=O)CC[C@]3(C)[C@@]1([H])C(=O)C[C@@]1(C)[C@@]2([H])CC[C@]1(O)C(=O)CO '
               'NAME: 4,5-dihydrocortisone REASON: WRONGLY CLASSIFIED Molecule '
               'contains a fused steroid nucleus (3 six–membered and 1 '
               'five–membered rings, ~17 carbons) and the candidate D–ring has '
               'a chiral carbon bearing an –OH group (heuristic for '
               '16β–hydroxy steroid)\n'
               ' * SMILES: '
               'O[C@@]12[C@]3([C@@]([C@@]4([C@](O)(CC3)C[C@@H](O[C@@H]5O[C@H]([C@H](O)[C@@H](O)[C@H]5O)C)C[C@H]4O)CO)([C@H](O)C[C@@]1([C@H](CC2)C=6COC(=O)C6)C)[H])[H].O '
               'NAME: 11,15>]Heptadec-14-yl]-5-hydrofuran-2-one, hydrate '
               'REASON: WRONGLY CLASSIFIED Molecule contains a fused steroid '
               'nucleus (3 six–membered and 1 five–membered rings, ~17 '
               'carbons) and the candidate D–ring has a chiral carbon bearing '
               'an –OH group (heuristic for 16β–hydroxy steroid)\n'
               ' * SMILES: '
               'CC(=O)OCC(=O)[C@@]1(O)CC[C@H]2[C@@H]3CCC4=CC(=O)C=C[C@]4(C)[C@H]3[C@@H](O)C[C@]12C '
               'NAME: Prednisolone acetate REASON: WRONGLY CLASSIFIED Molecule '
               'contains a fused steroid nucleus (3 six–membered and 1 '
               'five–membered rings, ~17 carbons) and the candidate D–ring has '
               'a chiral carbon bearing an –OH group (heuristic for '
               '16β–hydroxy steroid)\n'
               ' * SMILES: '
               'C[C@]12CC[C@H]3[C@@H](CCC4=CCCC[C@H]34)[C@@H]1CC[C@@]2(O)C#C '
               'NAME: Lynestrenol REASON: WRONGLY CLASSIFIED Molecule contains '
               'a fused steroid nucleus (3 six–membered and 1 five–membered '
               'rings, ~17 carbons) and the candidate D–ring has a chiral '
               'carbon bearing an –OH group (heuristic for 16β–hydroxy '
               'steroid)\n'
               ' * SMILES: '
               '[H][C@@]12CCC3=CC(=O)CC[C@]3(C)[C@@]1([H])CC[C@]1(C)[C@H]([C@H](O)C[C@@]21[H])C(C)=O '
               'NAME: 16alpha-hydroxyprogesterone REASON: WRONGLY CLASSIFIED '
               'Molecule contains a fused steroid nucleus (3 six–membered and '
               '1 five–membered rings, ~17 carbons) and the candidate D–ring '
               'has a chiral carbon bearing an –OH group (heuristic for '
               '16β–hydroxy steroid)\n'
               ' * SMILES: '
               'O1[C@]23C([C@]4([C@@]1(O)[C@@]([C@H]2OC(=O)C)(C(OC(=O)C)C(C4CC(OC)=O)(C)C)[H])C)CC[C@@]5(C3=CC(O[C@H]5C=6C=COC6)=O)C '
               'NAME: XYLOCARPUS A REASON: WRONGLY CLASSIFIED Molecule '
               'contains a fused steroid nucleus (3 six–membered and 1 '
               'five–membered rings, ~17 carbons) and the candidate D–ring has '
               'a chiral carbon bearing an –OH group (heuristic for '
               '16β–hydroxy steroid)\n'
               ' * SMILES: '
               '[Na+].[H][C@@]12CC[C@](O)(C(=O)COC(=O)CCC([O-])=O)[C@@]1(C)C[C@H](O)[C@@]1([H])[C@@]2([H])CCC2=CC(=O)C=C[C@]12C '
               'NAME: prednisolone sodium succinate REASON: WRONGLY CLASSIFIED '
               'Molecule contains a fused steroid nucleus (3 six–membered and '
               '1 five–membered rings, ~17 carbons) and the candidate D–ring '
               'has a chiral carbon bearing an –OH group (heuristic for '
               '16β–hydroxy steroid)\n'
               ' * SMILES: '
               'O[C@]12[C@@]([C@](CC1)([C@@](O)([C@H](O)CCC(O)(C)C)C)[H])(C[C@@H](O)[C@@]3([C@@]4([C@@](C[C@@H](O)[C@@H](O)C4)(C(=O)C=C23)[H])C)[H])C '
               'NAME: Turkesterone REASON: WRONGLY CLASSIFIED Molecule '
               'contains a fused steroid nucleus (3 six–membered and 1 '
               'five–membered rings, ~17 carbons) and the candidate D–ring has '
               'a chiral carbon bearing an –OH group (heuristic for '
               '16β–hydroxy steroid)\n'
               ' * SMILES: '
               '[H][C@@]12CC[C@]3(C)[C@]([H])(C[C@@H](OC(C)=O)[C@]4(C)C5=C([C@H](O)OC5=O)[C@@H](C[C@@]34[H])OC)[C@@]1(C)CCCC2(C)C '
               'NAME: '
               'rel-(3R,4R,5aS,5bR,7aS,11aS,11bR,13R,13aS)-3-hydroxy-4-methoxy-5b,8,8,11a,13a-pentamethyl-1-oxo-1,3,4,5,5a,5b,6,7,7a,8,9,10,11,11a,11b,12,13,13a-octadecahydrochryseno[2,1-c]furan-13-yl '
               'acetate REASON: WRONGLY CLASSIFIED Molecule contains a fused '
               'steroid nucleus (3 six–membered and 1 five–membered rings, ~17 '
               'carbons) and the candidate D–ring has a chiral carbon bearing '
               'an –OH group (heuristic for 16β–hydroxy steroid)\n'
               ' * SMILES: '
               '[H][C@@]12CC=C3C[C@H](CC[C@]3(C)[C@@]1([H])CC[C@@]1(C)[C@@]2([H])C[C@H](O[C@@H]2OC[C@H](O)[C@H](O[C@@H]3OC[C@@H](O)[C@H](O)[C@H]3OC(=O)c3ccc(OC)c(OC)c3)[C@H]2OC(C)=O)[C@]1(O)[C@@H](C)C(=O)CCC(C)C)O[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O '
               'NAME: '
               '3beta-[(beta-D-glucopyranosyl)oxy]-17alpha-hydroxy-16beta-[(O-(2-O-3,4-dimethoxybenzoyl-beta-D-xylopyranosyl)-(1->3)-2-O-acetyl-alpha-L-arabinopyranosyl)oxy]cholest-5-en-22-one '
               'REASON: WRONGLY CLASSIFIED Molecule contains a fused steroid '
               'nucleus (3 six–membered and 1 five–membered rings, ~17 '
               'carbons) and the candidate D–ring has a chiral carbon bearing '
               'an –OH group (heuristic for 16β–hydroxy steroid)\n'
               ' * SMILES: O[C@H]1CN2Cc3cc4OCOc4cc3[C@]11C=C[C@H](O)C[C@H]21 '
               'NAME: Hamayne REASON: WRONGLY CLASSIFIED Molecule contains a '
               'fused steroid nucleus (3 six–membered and 1 five–membered '
               'rings, ~17 carbons) and the candidate D–ring has a chiral '
               'carbon bearing an –OH group (heuristic for 16β–hydroxy '
               'steroid)\n'
               ' * SMILES: '
               '[H][C@@]12CC[C@]3(O)C[C@@H](O)C[C@@H](O)[C@]3(CO)[C@@]1([H])[C@H](O)C[C@]1(C)[C@H](CC[C@]21O)C1=CC(=O)OC1 '
               'NAME: ouabagenin REASON: WRONGLY CLASSIFIED Molecule contains '
               'a fused steroid nucleus (3 six–membered and 1 five–membered '
               'rings, ~17 carbons) and the candidate D–ring has a chiral '
               'carbon bearing an –OH group (heuristic for 16β–hydroxy '
               'steroid)\n'
               ' * SMILES: '
               '[H][C@@]12CCC3=CC(=O)CC[C@]3(C)[C@@]1([H])[C@@H](O)C[C@@]1(C)[C@@]2([H])CC[C@]1(O)C(=O)COC(=O)CCCCC '
               'NAME: hydrocortisone caproate REASON: WRONGLY CLASSIFIED '
               'Molecule contains a fused steroid nucleus (3 six–membered and '
               '1 five–membered rings, ~17 carbons) and the candidate D–ring '
               'has a chiral carbon bearing an –OH group (heuristic for '
               '16β–hydroxy steroid)\n'
               ' * SMILES: '
               'C[C@H](O)[C@]1(O)CC[C@@]2(O)[C@]1(C)[C@H](O)C[C@@H]1[C@@]3(C)CC[C@H](O)CC3=CC[C@@]21O '
               'NAME: Sarcostin REASON: WRONGLY CLASSIFIED Molecule contains a '
               'fused steroid nucleus (3 six–membered and 1 five–membered '
               'rings, ~17 carbons) and the candidate D–ring has a chiral '
               'carbon bearing an –OH group (heuristic for 16β–hydroxy '
               'steroid)\n'
               ' * SMILES: '
               'C[C@]12CC[C@H]3[C@@H](CCC4=CC(=O)C=C[C@]34C)[C@]1(O)CCC2=O '
               'NAME: 14-Hydroxyandrosta-1,4-diene-3,17-dione REASON: WRONGLY '
               'CLASSIFIED Molecule contains a fused steroid nucleus (3 '
               'six–membered and 1 five–membered rings, ~17 carbons) and the '
               'candidate D–ring has a chiral carbon bearing an –OH group '
               '(heuristic for 16β–hydroxy steroid)\n'
               ' * SMILES: '
               '[H+].[Cl-].[H][C@@]12CCC3=CC(=O)CC[C@]3(C)[C@@]1([H])[C@@H](O)C[C@@]1(C)[C@@]2([H])CC[C@]1(O)C(=O)COC(=O)CN(CC)CC '
               'NAME: hydrocortamate hydrochloride REASON: WRONGLY CLASSIFIED '
               'Molecule contains a fused steroid nucleus (3 six–membered and '
               '1 five–membered rings, ~17 carbons) and the candidate D–ring '
               'has a chiral carbon bearing an –OH group (heuristic for '
               '16β–hydroxy steroid)\n'
               ' * SMILES: '
               'O=C1C2=C(C(=O)C[C@@H]3[C@@]2(CCC(C3(C)C)=O)C)[C@@]4([C@H](O)C[C@@H]([C@]4(C1)C)[C@@H](CC(=O)C[C@@H](C(=O)O)C)C)C '
               'NAME: Ganoweberianic acid A REASON: WRONGLY CLASSIFIED '
               'Molecule contains a fused steroid nucleus (3 six–membered and '
               '1 five–membered rings, ~17 carbons) and the candidate D–ring '
               'has a chiral carbon bearing an –OH group (heuristic for '
               '16β–hydroxy steroid)\n'
               ' * SMILES: '
               'C[C@@]12C[C@H](O)C[C@H]1[C@@H]1CC=C3C[C@@H](O)CC[C@]3(C)[C@H]1CC2 '
               'NAME: 5-Androstene-3beta,16alpha-diol REASON: WRONGLY '
               'CLASSIFIED Molecule contains a fused steroid nucleus (3 '
               'six–membered and 1 five–membered rings, ~17 carbons) and the '
               'candidate D–ring has a chiral carbon bearing an –OH group '
               '(heuristic for 16β–hydroxy steroid)\n'
               ' * SMILES: '
               'O=C(O)[C@@H]([C@@H]1[C@@]2([C@@]([C@]34OO[C@@]5(C([C@@H](O)CC[C@@]5(C3=CC2)C)(C)C)C=C4)(C)C[C@H]1O)C)CCC(=C)C(C)C '
               'NAME: 5alpha,8alpha-peroxydehydrotumulosic acid REASON: '
               'WRONGLY CLASSIFIED Molecule contains a fused steroid nucleus '
               '(3 six–membered and 1 five–membered rings, ~17 carbons) and '
               'the candidate D–ring has a chiral carbon bearing an –OH group '
               '(heuristic for 16β–hydroxy steroid)\n'
               ' * SMILES: '
               'ClC1=C2[C@]([C@@]3([C@]([C@]4([C@@]([C@@](O)(CC4)C)(CC3)C)[H])(CC2)[H])[H])(C)C=CC1=O '
               'NAME: 4-Chloromethandienone REASON: WRONGLY CLASSIFIED '
               'Molecule contains a fused steroid nucleus (3 six–membered and '
               '1 five–membered rings, ~17 carbons) and the candidate D–ring '
               'has a chiral carbon bearing an –OH group (heuristic for '
               '16β–hydroxy steroid)\n'
               ' * SMILES: '
               'O1C2=C(C=C(O)C3=C2[C@@]4(OC=5C=CC=C(C5[C@@]3(O)[C@H]4C)O)O[C@@H](C1(C)C)COC)C '
               'NAME: Cytorhizin C REASON: WRONGLY CLASSIFIED Molecule '
               'contains a fused steroid nucleus (3 six–membered and 1 '
               'five–membered rings, ~17 carbons) and the candidate D–ring has '
               'a chiral carbon bearing an –OH group (heuristic for '
               '16β–hydroxy steroid)\n'
               ' * SMILES: '
               'CC1CC(=O)CC2=C1[C@H]1CC[C@@]3(C)[C@@H](CC[C@]3(C)O)[C@@H]1CC2 '
               'NAME: 17beta-Hydroxy-1,17-dimethylestr-5(10)-en-3-one REASON: '
               'WRONGLY CLASSIFIED Molecule contains a fused steroid nucleus '
               '(3 six–membered and 1 five–membered rings, ~17 carbons) and '
               'the candidate D–ring has a chiral carbon bearing an –OH group '
               '(heuristic for 16β–hydroxy steroid)\n'
               'False negatives: SMILES: O1[C@]2/3C(=NCC[C@H]12)C=C\\C3=C/C '
               'NAME: Abikoviromycin REASON: MISSED No fused 4–ring steroid '
               'nucleus (3 six–membered + 1 five–membered with ~17 carbons) '
               'found\n'
               ' * SMILES: O1C2/3C(=NCCC12)C=C\\C3=C/C NAME: Latumcidin '
               'REASON: MISSED No fused 4–ring steroid nucleus (3 six–membered '
               '+ 1 five–membered with ~17 carbons) found\n'
               ' * SMILES: '
               'O1[C@@]23[C@@]4([C@@](CC1(O)CC4)(CC=C2[C@]56OCCN(C[C@@]5(C[C@H]3O)C(=CC6)[C@@H](O)C)C)[H])C '
               'NAME: '
               '(1R,5R,6S,11S,12R,14R)-22-[(1S)-1-Hydroxyethyl]-6,16-dimethyl-10,19-dioxa-16-azahexacyclo[12.5.3.15,9.01,14.02,11.06,11]tricosa-2,21-diene-9,12-diol '
               'REASON: MISSED Steroid nucleus found but no chiral carbon with '
               'an attached –OH in the 5–membered ring (D–ring) was detected\n'
               ' * SMILES: '
               'O=C(OC(/C=C\\1/C=C(C)C=2C13OC3CCN2)C(OC(=O)C)C)C(C)C NAME: '
               'Kobutimycin A REASON: MISSED No fused 4–ring steroid nucleus '
               '(3 six–membered + 1 five–membered with ~17 carbons) found\n'
               ' * SMILES: CN1[C@H]2CC3CC1C(C2O3)O NAME: LSM-1903 REASON: '
               'MISSED No fused 4–ring steroid nucleus (3 six–membered + 1 '
               'five–membered with ~17 carbons) found\n'
               ' * SMILES: '
               'O1C23C4(C(CC1(O)CC4)CC=C2C56OCCN(CC5(CC3O)C(=CC6)C(O)C)C)C '
               'NAME: Batrachotoxinin A REASON: MISSED Steroid nucleus found '
               'but no chiral carbon with an attached –OH in the 5–membered '
               'ring (D–ring) was detected\n'
               ' * SMILES: '
               'O1[C@]2([C@H]([C@](O)(C(=O)N[C@@H]2C)C1=O)/C=C/C(O)CCCCCCC)[H] '
               'NAME: Awajanomycin REASON: MISSED No fused 4–ring steroid '
               'nucleus (3 six–membered + 1 five–membered with ~17 carbons) '
               'found\n'
               ' * SMILES: '
               'O=C(OC(/C=C\\1/C=C(C)C=2C13OC3CCN2)C(OC(=O)C)C)C(CC)C NAME: '
               'Kobutimycin B REASON: MISSED No fused 4–ring steroid nucleus '
               '(3 six–membered + 1 five–membered with ~17 carbons) found\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'O=C1OC[C@@H]2O[C@@H](O[C@@H]3[C@@H](OC(=O)CCCCCCCCCCCCCCC)[C@H](C=CCCCC1)[C@H](CCCCC)[C@@H](C3)O)[C@H](O)[C@H]([C@@H]2O)O',
                                     'name': 'Mucorolactone',
                                     'reason': 'No fused 4–ring steroid '
                                               'nucleus (three 6–membered and '
                                               'one 5–membered rings with '
                                               'exactly 17 carbons) found'},
                                 {   'smiles': 'C[C@@H]1CN[C@H](COC2=C(C=CC(=C2)NC(=O)C3=NC4=CC=CC=C4S3)C(=O)N(C[C@H]1OC)C)C',
                                     'name': 'N-[(5S,6R,9S)-5-methoxy-3,6,9-trimethyl-2-oxo-11-oxa-3,8-diazabicyclo[10.4.0]hexadeca-1(12),13,15-trien-14-yl]-1,3-benzothiazole-2-carboxamide',
                                     'reason': 'No fused 4–ring steroid '
                                               'nucleus (three 6–membered and '
                                               'one 5–membered rings with '
                                               'exactly 17 carbons) found'},
                                 {   'smiles': 'COC1=CC=CC(=C1)C2=CC=C(C=C2)[C@@H]3[C@@H]4CN(CC(=O)N4[C@@H]3CO)C(=O)C5=CN=CC=C5',
                                     'name': '(6R,7R,8S)-8-(hydroxymethyl)-7-[4-(3-methoxyphenyl)phenyl]-4-[oxo(3-pyridinyl)methyl]-1,4-diazabicyclo[4.2.0]octan-2-one',
                                     'reason': 'No fused 4–ring steroid '
                                               'nucleus (three 6–membered and '
                                               'one 5–membered rings with '
                                               'exactly 17 carbons) found'},
                                 {   'smiles': 'C(C(/C=C/C=C/C=C/[C@H](CCCC(O)=O)O)=O)/C=C\\CCCCC',
                                     'name': '12-oxo-6-trans-leukotriene B4',
                                     'reason': 'No rings of size 5 or 6 found; '
                                               'cannot be a steroid nucleus'},
                                 {   'smiles': 'O=C1OC(=C(C#C[C@H](COC(=O)C)C)CO)C=C1',
                                     'name': "5'-O-acetylaporpinone A",
                                     'reason': 'No fused 4–ring steroid '
                                               'nucleus (three 6–membered and '
                                               'one 5–membered rings with '
                                               'exactly 17 carbons) found'},
                                 {   'smiles': 'O=C(N1[C@@H](CCC1)C(=O)N[C@@H](CCC(=O)N)C(O)=O)[C@@H](N)[C@H](CC)C',
                                     'name': 'Ile-Pro-Gln',
                                     'reason': 'No fused 4–ring steroid '
                                               'nucleus (three 6–membered and '
                                               'one 5–membered rings with '
                                               'exactly 17 carbons) found'},
                                 {   'smiles': 'O[C@@H]1C=CC=C(CCC(O)=O)[C@@H]1O',
                                     'name': '3-[(5R,6S)-5,6-dihydroxycyclohexa-1,3-dienyl]propanoic '
                                             'acid',
                                     'reason': 'No fused 4–ring steroid '
                                               'nucleus (three 6–membered and '
                                               'one 5–membered rings with '
                                               'exactly 17 carbons) found'},
                                 {   'smiles': 'O=C(OC)/C=C/C(C)(C)C',
                                     'name': '4,4-Dimethyl-pentenoic acid '
                                             'methyl ester',
                                     'reason': 'No rings of size 5 or 6 found; '
                                               'cannot be a steroid nucleus'},
                                 {   'smiles': 'CCCCOc1ccc(OCCCN2CCOCC2)cc1',
                                     'name': 'pramocaine',
                                     'reason': 'No fused 4–ring steroid '
                                               'nucleus (three 6–membered and '
                                               'one 5–membered rings with '
                                               'exactly 17 carbons) found'},
                                 {   'smiles': 'OC[C@@H](O)C(=O)[C@H](O)[C@H](O)COP(O)(O)=O',
                                     'name': 'D-arabino-hex-3-ulose '
                                             '6-phosphate',
                                     'reason': 'No rings of size 5 or 6 found; '
                                               'cannot be a steroid nucleus'}],
    'sample_false_negatives': [   {   'smiles': 'O1[C@]2/3C(=NCC[C@H]12)C=C\\C3=C/C',
                                      'name': 'Abikoviromycin',
                                      'reason': 'No fused 4–ring steroid '
                                                'nucleus (three 6–membered and '
                                                'one 5–membered rings with '
                                                'exactly 17 carbons) found'},
                                  {   'smiles': 'O1C2/3C(=NCCC12)C=C\\C3=C/C',
                                      'name': 'Latumcidin',
                                      'reason': 'No fused 4–ring steroid '
                                                'nucleus (three 6–membered and '
                                                'one 5–membered rings with '
                                                'exactly 17 carbons) found'},
                                  {   'smiles': 'O1[C@@]23[C@@]4([C@@](CC1(O)CC4)(CC=C2[C@]56OCCN(C[C@@]5(C[C@H]3O)C(=CC6)[C@@H](O)C)C)[H])C',
                                      'name': '(1R,5R,6S,11S,12R,14R)-22-[(1S)-1-Hydroxyethyl]-6,16-dimethyl-10,19-dioxa-16-azahexacyclo[12.5.3.15,9.01,14.02,11.06,11]tricosa-2,21-diene-9,12-diol',
                                      'reason': 'Steroid nucleus found but no '
                                                'chiral carbon with a directly '
                                                'attached –OH in the D–ring '
                                                'was detected'},
                                  {   'smiles': 'O=C(OC(/C=C\\1/C=C(C)C=2C13OC3CCN2)C(OC(=O)C)C)C(C)C',
                                      'name': 'Kobutimycin A',
                                      'reason': 'No fused 4–ring steroid '
                                                'nucleus (three 6–membered and '
                                                'one 5–membered rings with '
                                                'exactly 17 carbons) found'},
                                  {   'smiles': 'CN1[C@H]2CC3CC1C(C2O3)O',
                                      'name': 'LSM-1903',
                                      'reason': 'No fused 4–ring steroid '
                                                'nucleus (three 6–membered and '
                                                'one 5–membered rings with '
                                                'exactly 17 carbons) found'},
                                  {   'smiles': 'O1C23C4(C(CC1(O)CC4)CC=C2C56OCCN(CC5(CC3O)C(=CC6)C(O)C)C)C',
                                      'name': 'Batrachotoxinin A',
                                      'reason': 'Steroid nucleus found but no '
                                                'chiral carbon with a directly '
                                                'attached –OH in the D–ring '
                                                'was detected'},
                                  {   'smiles': 'O1[C@]2([C@H]([C@](O)(C(=O)N[C@@H]2C)C1=O)/C=C/C(O)CCCCCCC)[H]',
                                      'name': 'Awajanomycin',
                                      'reason': 'No fused 4–ring steroid '
                                                'nucleus (three 6–membered and '
                                                'one 5–membered rings with '
                                                'exactly 17 carbons) found'},
                                  {   'smiles': 'O=C(OC(/C=C\\1/C=C(C)C=2C13OC3CCN2)C(OC(=O)C)C)C(CC)C',
                                      'name': 'Kobutimycin B',
                                      'reason': 'No fused 4–ring steroid '
                                                'nucleus (three 6–membered and '
                                                'one 5–membered rings with '
                                                'exactly 17 carbons) found'}],
    'attempt': 4,
    'reasoning': 'Below is our reasoning. In our previous attempt the '
                 'heuristic was built in several steps: (1) finding rings of '
                 'sizes 5 and 6 and grouping together “fused” rings into '
                 'connected components; (2) then iterating over combinations '
                 'of four rings (expecting three six‐membered and one '
                 'five‐membered) whose union would roughly contain the '
                 'classical steroid nucleus (around 17 carbon atoms); (3) and '
                 'finally checking that in the unique 5–membered ring (D–ring) '
                 'at least one chiral carbon bears a hydroxyl group. That '
                 'approach produced many false positives because many '
                 'non‐steroids (and some modified natural products) also '
                 'contain fused rings and even a chiral –OH. One potential '
                 'improvement is to “tighten” our definition of the steroid '
                 'nucleus by requiring that the union of atoms from the four '
                 'rings contain exactly 17 carbon atoms (or a very narrow '
                 'range) instead of a broad range. This helps weed out fused '
                 'systems that are merely similar to steroids. In addition we '
                 'retain the connectivity tests (requiring proper fusion) and '
                 'the check on the D–ring for a chiral center bound to an –OH '
                 '(with at least one H on the oxygen). Such modifications '
                 'should reduce false positives while still flagging true '
                 '16β–hydroxy steroids.\n'
                 '\n'
                 'Below is the complete Python program that implements this '
                 'improved heuristic.\n'
                 '\n'
                 '--------------------------------',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 18,
    'num_false_positives': 1231,
    'num_true_negatives': 141043,
    'num_false_negatives': 8,
    'num_negatives': None,
    'precision': 0.014411529223378704,
    'recall': 0.6923076923076923,
    'f1': 0.02823529411764706,
    'accuracy': 0.991293042867182,
    'negative_predictive_value': 0.9999432829260338}