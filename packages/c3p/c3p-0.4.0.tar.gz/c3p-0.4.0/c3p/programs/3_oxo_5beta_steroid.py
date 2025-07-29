"""
Classifies: CHEBI:1624 3-oxo-5beta-steroid
"""
"""
Classifies: 3-oxo-5beta-steroid, defined as 'Any 3-oxo steroid that has beta- configuration at position 5.' 
Heuristic criteria revised:
  1. Identify all ring systems from the input molecule.
  2. Build a graph of fused rings (rings sharing at least 2 atoms) and search for a connected component
     that has exactly 4 rings and whose ring sizes are exactly three six-membered rings and one five-membered ring.
     (This represents the canonical steroid nucleus, i.e. cyclopentanoperhydrophenanthrene.)
  3. Check that at least one of the carbons in that candidate nucleus bears a double-bonded oxygen (a ketone) 
     – which should be a ring-bound carbonyl (the "3-oxo" feature).
  4. As a proxy for the beta configuration at carbon-5, require that the SMILES string includes at least one "@@" annotation.
     
Note: Since steroid numbering is nontrivial from a SMILES string, these conditions are all heuristic.
"""

from rdkit import Chem
from rdkit.Chem import rdMolDescriptors
from rdkit.Chem.rdchem import BondType

def is_3_oxo_5beta_steroid(smiles: str):
    """
    Determines if a molecule appears to be a 3-oxo-5beta-steroid based on its SMILES string.
    
    The heuristic:
      (a) Parse the molecule and extract all ring systems.
      (b) Build a connectivity graph among rings that share at least 2 atoms. Then search for a connected
          set of rings that has exactly 4 fused rings, consisting of 3 six-membered rings and 1 five-membered ring.
      (c) Check that within the candidate steroid nucleus there is at least one ring-bound ketone (C=O).
      (d) Verify that the original SMILES string contains an explicit chiral tag ("@@") that is assumed to
          indicate the beta configuration at position 5.
    
    Args:
        smiles (str): SMILES string of the molecule.
        
    Returns:
        bool: True if molecule fits the heuristic criteria for a 3-oxo-5beta-steroid, False otherwise.
        str: Explanation for the decision.
    """
    # Parse the SMILES string into a molecule.
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
    
    # Get ring information: each ring is returned as a tuple of atom indices.
    ring_info = mol.GetRingInfo()
    rings = ring_info.AtomRings()
    if not rings:
        return False, "No rings found in the molecule"
    
    # Build a connectivity graph of rings.
    n_rings = len(rings)
    ring_nodes = list(range(n_rings))
    ring_sets = [set(r) for r in rings]  # convert tuples to sets for intersection
    connectivity = {i: set() for i in ring_nodes}
    for i in ring_nodes:
        for j in ring_nodes:
            if i < j and len(ring_sets[i].intersection(ring_sets[j])) >= 2:
                connectivity[i].add(j)
                connectivity[j].add(i)
    
    # Find connected components in the ring graph.
    visited = set()
    components = []
    for node in ring_nodes:
        if node not in visited:
            stack = [node]
            comp = set()
            while stack:
                current = stack.pop()
                if current not in visited:
                    visited.add(current)
                    comp.add(current)
                    stack.extend(list(connectivity[current] - visited))
            components.append(comp)
    
    # Look for a connected component that represents the steroid nucleus:
    # It must have exactly 4 rings, with exactly 3 six-membered rings and 1 five-membered ring.
    candidate_component = None
    for comp in components:
        if len(comp) == 4:
            six_count = 0
            five_count = 0
            for idx in comp:
                ring_size = len(rings[idx])
                if ring_size == 6:
                    six_count += 1
                elif ring_size == 5:
                    five_count += 1
            if six_count == 3 and five_count == 1:
                candidate_component = comp
                break
    if candidate_component is None:
        return False, ("Fused ring system does not match typical steroid nucleus. "
                       "Expected exactly 4 fused rings (3 six-membered and 1 five-membered) but none found.")
    
    # Create the set of atoms that are part of the candidate steroid nucleus.
    candidate_atoms = set()
    for idx in candidate_component:
        candidate_atoms.update(rings[idx])
    
    # Search for a ketone group (C=O) where the carbon is in the candidate nucleus.
    ketone_found = False
    for atom in mol.GetAtoms():
        if atom.GetAtomicNum() == 6 and atom.GetIdx() in candidate_atoms:
            # Check if this carbon is double-bonded to an oxygen.
            for bond in atom.GetBonds():
                # Check the bond type using RDKit's BondType enum.
                if bond.GetBondType() == BondType.DOUBLE:
                    nbr = bond.GetOtherAtom(atom)
                    if nbr.GetAtomicNum() == 8:
                        ketone_found = True
                        break
            if ketone_found:
                break
    if not ketone_found:
        return False, "No ring-bound ketone group found within the candidate steroid nucleus (missing 3-oxo feature)"
    
    # Check for chiral annotation indicating beta configuration.
    # We require that the original SMILES contains the '@@' symbol.
    if "@@" not in smiles:
        return False, "No '@@' chiral annotation found in SMILES (missing beta configuration indicator)"
    
    return True, "Molecule appears to be a 3-oxo steroid with beta configuration based on heuristic criteria"

# Example usage: (uncomment the following lines to test)
if __name__ == "__main__":
    # A test SMILES for 17beta-hydroxy-5beta-estran-3-one
    test_smiles = "C[C@]12CC[C@H]3[C@@H](CC[C@@H]4CC(=O)CC[C@H]34)[C@@H]1CC[C@@H]2O"
    result, reason = is_3_oxo_5beta_steroid(test_smiles)
    print(result, reason)


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:1624',
                          'name': '3-oxo-5beta-steroid',
                          'definition': 'Any 3-oxo steroid that has beta- '
                                        'configuration at position 5.',
                          'parents': ['CHEBI:136889', 'CHEBI:47788'],
                          'xrefs': [   'KEGG:C02797',
                                       'MetaCyc:3-Oxo-5-Beta-Steroids'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 96,
                           'log_lines_of_code': 4.564348191467836,
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
                                                 2,
                                                 3,
                                                 3,
                                                 3,
                                                 4,
                                                 4,
                                                 5,
                                                 4,
                                                 5,
                                                 3,
                                                 4,
                                                 4,
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
                                                 3,
                                                 3,
                                                 4,
                                                 4,
                                                 5,
                                                 5,
                                                 6,
                                                 6,
                                                 3,
                                                 4,
                                                 1,
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 1,
                                                 1,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 1],
                           'max_indent': 6,
                           'imports': [   'from rdkit import Chem',
                                          'from rdkit.Chem import '
                                          'rdMolDescriptors',
                                          'from rdkit.Chem.rdchem import '
                                          'BondType'],
                           'imports_count': 3,
                           'methods_called': [   'MolFromSmiles',
                                                 'GetRingInfo',
                                                 'extend',
                                                 'GetOtherAtom',
                                                 'pop',
                                                 'GetAtomicNum',
                                                 'AtomRings',
                                                 'add',
                                                 'GetIdx',
                                                 'GetBonds',
                                                 'GetAtoms',
                                                 'update',
                                                 'GetBondType',
                                                 'intersection',
                                                 'append'],
                           'methods_called_count': 15,
                           'smarts_strings': [],
                           'smarts_strings_count': 0,
                           'defs': ['is_3_oxo_5beta_steroid(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "No rings found in the '
                                          'molecule"',
                                          'False, ("Fused ring system does not '
                                          'match typical steroid nucleus. "',
                                          'False, "No ring-bound ketone group '
                                          'found within the candidate steroid '
                                          'nucleus (missing 3-oxo feature)"',
                                          'False, "No \'@@\' chiral annotation '
                                          'found in SMILES (missing beta '
                                          'configuration indicator)"',
                                          'True, "Molecule appears to be a '
                                          '3-oxo steroid with beta '
                                          'configuration based on heuristic '
                                          'criteria"'],
                           'returns_count': 6,
                           'complexity': 6.512869638293568},
    'message': '\n'
               'Attempt failed: F1 score of 0.01348314606741573 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: '
               'C[C@]12CC[C@H]3[C@@H](CC[C@@H]4CC(=O)CC[C@H]34)[C@@H]1CC[C@@H]2O '
               'NAME: 17beta-hydroxy-5beta-estran-3-one REASON: CORRECT '
               'Molecule appears to be a 3-oxo steroid with beta configuration '
               'based on heuristic criteria\n'
               ' * SMILES: '
               'C[C@]12CC[C@H]3[C@@H](CC[C@@H]4CC(=O)CC[C@]34C)[C@@H]1CC[C@@H]2C(=O)CO '
               'NAME: 5beta-dihydrodeoxycorticosterone REASON: CORRECT '
               'Molecule appears to be a 3-oxo steroid with beta configuration '
               'based on heuristic criteria\n'
               ' * SMILES: '
               'CC(=O)[C@H]1CC[C@H]2[C@@H]3CC[C@@H]4CC(=O)CC[C@]4(C)[C@H]3C=C[C@]12C '
               'NAME: 5beta-pregn-11-ene-3,20-dione REASON: CORRECT Molecule '
               'appears to be a 3-oxo steroid with beta configuration based on '
               'heuristic criteria\n'
               ' * SMILES: '
               '[H][C@@]12CC(=O)CC[C@]1(C)[C@@]1([H])CC(=O)[C@]3(C)[C@]([H])(CC[C@@]3([H])[C@]1([H])C(=O)C2)[C@H](C)CCC(O)=O '
               'NAME: 3,7,12-trioxo-5beta-cholanic acid REASON: CORRECT '
               'Molecule appears to be a 3-oxo steroid with beta configuration '
               'based on heuristic criteria\n'
               ' * SMILES: '
               '[H][C@]12C[C@@H](O)[C@@]3([H])[C@]4([H])CC[C@]([H])([C@H](C)CCC(O)C(C)C)[C@@]4(C)CC[C@]3([H])[C@@]1(C)CCC(=O)C2 '
               'NAME: 7alpha,24-dihydroxy-5beta-cholestan-3-one REASON: '
               'CORRECT Molecule appears to be a 3-oxo steroid with beta '
               'configuration based on heuristic criteria\n'
               ' * SMILES: '
               'C1[C@@]2([C@]3(CC([C@]4([C@]([C@@]3([C@H](C[C@@]2(CC(C1)=O)[H])O)[H])(CC[C@]4([H])[C@@H](CCC(O)=O)C)[H])C)=O)[H])C '
               'NAME: 7beta-hydroxy-3,12-dioxo-5beta-cholanic acid REASON: '
               'CORRECT Molecule appears to be a 3-oxo steroid with beta '
               'configuration based on heuristic criteria\n'
               ' * SMILES: '
               '[H][C@]12CC[C@]3([H])[C@]([H])(CC[C@]4(C)[C@]([H])(CC[C@@]34[H])[C@H](C)CCCC(C)C)[C@@]1(C)CCC(=O)C2 '
               'NAME: 5beta-cholestan-3-one REASON: CORRECT Molecule appears '
               'to be a 3-oxo steroid with beta configuration based on '
               'heuristic criteria\n'
               ' * SMILES: '
               '[H][C@]12C[C@@H](O)[C@@]3([H])[C@]4([H])CC[C@]([H])([C@H](C)CCCC(C)C)[C@@]4(C)[C@@H](O)C[C@]3([H])[C@@]1(C)CCC(=O)C2 '
               'NAME: 7alpha,12alpha-dihydroxy-5beta-cholestan-3-one REASON: '
               'CORRECT Molecule appears to be a 3-oxo steroid with beta '
               'configuration based on heuristic criteria\n'
               ' * SMILES: '
               '[H][C@]12C[C@@H](O)[C@@]3([H])[C@]4([H])CC[C@]([H])([C@H](C)CCCC(C)CO)[C@@]4(C)CC[C@]3([H])[C@@]1(C)CCC(=O)C2 '
               'NAME: 7alpha,26-dihydroxy-5beta-cholestan-3-one REASON: '
               'CORRECT Molecule appears to be a 3-oxo steroid with beta '
               'configuration based on heuristic criteria\n'
               ' * SMILES: '
               '[C@@]12([C@@]([C@@]3([C@@](CC(=O)CC3)(CC1)[H])C)(CC[C@]4(C)[C@H](CC[C@@]24[H])O)[H])[H] '
               'NAME: 5beta-dihydrotestosterone REASON: CORRECT Molecule '
               'appears to be a 3-oxo steroid with beta configuration based on '
               'heuristic criteria\n'
               ' * SMILES: '
               'C[C@]12CCC(=O)C[C@H]1CC[C@H]1[C@@H]3CC[C@H](C(=O)CO)[C@]3(C[C@H](O)[C@H]21)C=O '
               'NAME: 5beta-dihydroaldosterone REASON: CORRECT Molecule '
               'appears to be a 3-oxo steroid with beta configuration based on '
               'heuristic criteria\n'
               ' * SMILES: '
               '[H][C@]12C[C@@H](O)[C@@]3([H])[C@]4([H])CC[C@]([H])([C@H](C)CCC(O)C(C)C)[C@@]4(C)[C@@H](O)C[C@]3([H])[C@@]1(C)CCC(=O)C2 '
               'NAME: 7alpha,12alpha,24-trihydroxy-5beta-cholestan-3-one '
               'REASON: CORRECT Molecule appears to be a 3-oxo steroid with '
               'beta configuration based on heuristic criteria\n'
               ' * SMILES: '
               'C1[C@@]2([C@]3(CC[C@]4([C@]([C@@]3(CC[C@@]2(CC(C1)=O)[H])[H])(CC[C@]4([H])[C@@H](O)C)[H])C)[H])C '
               'NAME: 5beta-pregnan-20alpha-ol-3-one REASON: CORRECT Molecule '
               'appears to be a 3-oxo steroid with beta configuration based on '
               'heuristic criteria\n'
               ' * SMILES: '
               'CC(=O)[C@H]1CC[C@H]2[C@@H]3CC[C@@H]4CC(=O)CC[C@]4(C)[C@H]3C[C@H](O)[C@]12C '
               'NAME: 12alpha-Hydroxy-5beta-pregnane-3,20-dione REASON: '
               'CORRECT Molecule appears to be a 3-oxo steroid with beta '
               'configuration based on heuristic criteria\n'
               ' * SMILES: '
               'C[C@]12CC[C@H]3[C@@H](CC[C@@H]4CC(=O)CC[C@]34C)[C@@H]1CC[C@H]2O '
               'NAME: 5beta-dihydroepitestosterone REASON: CORRECT Molecule '
               'appears to be a 3-oxo steroid with beta configuration based on '
               'heuristic criteria\n'
               ' * SMILES: '
               '[H][C@]12C[C@@H](O)[C@]3([H])[C@]([H])(CC[C@]4(C)[C@]([H])(CC[C@@]34[H])[C@H](C)CCCC(C)C)[C@@]1(C)CCC(=O)C2 '
               'NAME: 7alpha-hydroxy-5beta-cholestan-3-one REASON: CORRECT '
               'Molecule appears to be a 3-oxo steroid with beta configuration '
               'based on heuristic criteria\n'
               ' * SMILES: '
               'C1C(C[C@@]2([C@](C1)([C@@]3([C@@](CC2)([C@@]4([H])[C@@](C[C@@H]3O)(C)[C@](CC4)(C(CO)=O)O)[H])[H])C)[H])=O '
               'NAME: 5beta-dihydrocortisol REASON: CORRECT Molecule appears '
               'to be a 3-oxo steroid with beta configuration based on '
               'heuristic criteria\n'
               ' * SMILES: '
               'C1[C@@]2([C@]3(C[C@@H]([C@]4([C@]([C@@]3([C@@H](C[C@@]2(CC(C1)=O)[H])O)[H])(CC[C@@]4([C@@H](CCC(O)=O)C)[H])[H])C)O)[H])C '
               'NAME: 7alpha,12alpha-dihydroxy-3-oxo-5beta-cholan-24-oic acid '
               'REASON: CORRECT Molecule appears to be a 3-oxo steroid with '
               'beta configuration based on heuristic criteria\n'
               ' * SMILES: '
               '[H][C@]12C[C@@H](O)[C@@]3([H])[C@]4([H])CC[C@]([H])([C@H](C)CC[C@H](O)C(C)C)[C@@]4(C)CC[C@]3([H])[C@@]1(C)CCC(=O)C2 '
               'NAME: (24S)-7alpha,24-dihydroxy-5beta-cholestan-3-one REASON: '
               'CORRECT Molecule appears to be a 3-oxo steroid with beta '
               'configuration based on heuristic criteria\n'
               ' * SMILES: '
               'C1[C@@]2([C@]3(C[C@@H]([C@]4([C@]([C@@]3(CC[C@@]2(CC(C1)=O)[H])[H])(CC[C@@]4([C@@H](CCC(O)=O)C)[H])[H])C)O)[H])C '
               'NAME: 12alpha-hydroxy-3-oxo-5beta-cholan-24-oic acid REASON: '
               'CORRECT Molecule appears to be a 3-oxo steroid with beta '
               'configuration based on heuristic criteria\n'
               ' * SMILES: '
               '[H][C@]12CC[C@@]3([H])[C@]4([H])CCC(=O)[C@@]4(C)CC[C@]3([H])[C@@]1(C)CCC(=O)C2 '
               'NAME: 5beta-androstane-3,17-dione REASON: CORRECT Molecule '
               'appears to be a 3-oxo steroid with beta configuration based on '
               'heuristic criteria\n'
               ' * SMILES: '
               'C1[C@@]2([C@]3(CC[C@]4([C@]([C@@]3([C@@H](C[C@@]2(CC(C1)=O)[H])O)[H])(CC[C@@]4([C@@H](CCC(O)=O)C)[H])[H])C)[H])C '
               'NAME: 7alpha-hydroxy-3-oxo-5beta-cholan-24-oic acid REASON: '
               'CORRECT Molecule appears to be a 3-oxo steroid with beta '
               'configuration based on heuristic criteria\n'
               ' * SMILES: '
               'C[C@]12C[C@H](O)[C@H]3[C@@H](CC[C@@H]4CC(=O)CC[C@]34C)[C@@H]1CC[C@@H]2C(=O)CO '
               'NAME: 5beta-dihydrocorticosterone REASON: CORRECT Molecule '
               'appears to be a 3-oxo steroid with beta configuration based on '
               'heuristic criteria\n'
               ' * SMILES: '
               'CC(=O)[C@H]1CC[C@H]2[C@@H]3CC[C@@H]4CC(=O)CC[C@]4(C)[C@H]3[C@@H]3O[C@@H]3[C@]12C '
               'NAME: 11alpha,12alpha-Epoxy-5beta-pregnane-3,20-dione REASON: '
               'CORRECT Molecule appears to be a 3-oxo steroid with beta '
               'configuration based on heuristic criteria\n'
               ' * SMILES: '
               '[H][C@]12CC[C@@]3([H])[C@]4([H])CC[C@](O)(C(=O)CO)[C@@]4(C)CC(=O)[C@]3([H])[C@@]1(C)CCC(=O)C2 '
               'NAME: 17,21-dihydroxy-5beta-pregnane-3,11,20-trione REASON: '
               'CORRECT Molecule appears to be a 3-oxo steroid with beta '
               'configuration based on heuristic criteria\n'
               'False positives: SMILES: '
               'S1S[C@@H]2[C@H](O)[C@H]3N4[C@]1(C(=O)N5[C@@H]6[C@@H](O)[C@@H](OC)[C@@H]7S[C@@]5(C4=O)C[C@H]6C7=O)C[C@H]3C(C2)=O '
               'NAME: Amphiepicoccin G REASON: WRONGLY CLASSIFIED Molecule '
               'appears to be a 3-oxo steroid with beta configuration based on '
               'heuristic criteria\n'
               ' * SMILES: '
               'O=C1[C@@]23OC(C=4CCOC4[C@@H]2C)[C@@H]3[C@H](O)C(C1)(C)C NAME: '
               'Stereumone A REASON: WRONGLY CLASSIFIED Molecule appears to be '
               'a 3-oxo steroid with beta configuration based on heuristic '
               'criteria\n'
               ' * SMILES: '
               'C1[C@@H]([C@@H](C[C@@]2([C@]1([C@@H]3[C@@H](CC2)[C@]4(CC[C@@H]([C@]4(CC3)C)C5=COC(C=C5)=O)O)C=O)O)OC(=O)C)OC(=O)C '
               'NAME: '
               '(2beta,3beta,5beta)-2,3-diacetoxy-5,14-dihydroxy-19-oxobufa-20,22-dienolide '
               'REASON: WRONGLY CLASSIFIED Molecule appears to be a 3-oxo '
               'steroid with beta configuration based on heuristic criteria\n'
               ' * SMILES: '
               'O=C1C=2C=3C(=C4C5=C(C(O)=C(C6=C5C3[C@@]7([C@]6(O[C@H](C7)C)C(=O)C)[C@@H](C2O)OC)OC)C(=O)C=C4OC)C(=C1)OC '
               'NAME: Phaeosphaerin B REASON: WRONGLY CLASSIFIED Molecule '
               'appears to be a 3-oxo steroid with beta configuration based on '
               'heuristic criteria\n'
               ' * SMILES: '
               'O=C1C2=C([C@]3([C@H]4O[C@H]4[C@@H](C=5C3=C1OC5)O)C)CC[C@]6([C@H]2CC[C@@H]6C(=O)C)C '
               'NAME: Epoxyvirone REASON: WRONGLY CLASSIFIED Molecule appears '
               'to be a 3-oxo steroid with beta configuration based on '
               'heuristic criteria\n'
               ' * SMILES: '
               '[C@H]1([C@]2([C@]3([C@@](C4=C(C=C(O)C=C4)CC3)(CC[C@@]2(C(=O)C1)C)[H])[H])[H])O '
               'NAME: 15alpha-hydroxyestrone REASON: WRONGLY CLASSIFIED '
               'Molecule appears to be a 3-oxo steroid with beta configuration '
               'based on heuristic criteria\n'
               ' * SMILES: '
               '[H][C@@]1(CC[C@@]2([H])C3=C(C(=O)C[C@]12C)[C@@]1(C)CC[C@@H](O)[C@](C)(O)[C@]1([H])C[C@@H]3O)[C@H](C)CCC(=C)C(C)C(O)=O '
               'NAME: antcin K REASON: WRONGLY CLASSIFIED Molecule appears to '
               'be a 3-oxo steroid with beta configuration based on heuristic '
               'criteria\n'
               ' * SMILES: '
               'O=C1C2=C(C(=O)CC[C@@]2([C@]34CC[C@]([C@H](C[C@@H]3C1)C4)(O)COC(=O)C)C)C '
               'NAME: Aphidicolin A68 REASON: WRONGLY CLASSIFIED Molecule '
               'appears to be a 3-oxo steroid with beta configuration based on '
               'heuristic criteria\n'
               ' * SMILES: '
               'O=C1O[C@H]2CC3=C4[C@@H]([C@@]5([C@H](C([C@H](OC(=O)C)CC5)(C)C)CC4)C)CC[C@@]3([C@H]2[C@H]1CC(=O)C=C(C)C)C '
               'NAME: Tricholimbrin B REASON: WRONGLY CLASSIFIED Molecule '
               'appears to be a 3-oxo steroid with beta configuration based on '
               'heuristic criteria\n'
               ' * SMILES: '
               'O=C1C([C@H]2[C@](C3=C([C@]4([C@]([C@@H]([C@@H](CC/C=C(/C(=O)O)\\C)C)C[C@@H]4OC(=O)C)(C)CC3)C)CC2)(C)CC1)(C)C '
               'NAME: (24E)-15alpha-acetoxy-3-oxolanosta-8,24-dien-26-oic acid '
               'REASON: WRONGLY CLASSIFIED Molecule appears to be a 3-oxo '
               'steroid with beta configuration based on heuristic criteria\n'
               ' * SMILES: '
               'S1S[C@@]23N([C@H]4NC=5C=CC=CC5C4([C@@H]2O)[C@@]67C8=C(C=CC=C8)N[C@@H]6N9C(=O)[C@]%10(C(O)C)SS[C@@]9([C@H]7O)C(=O)N%10C)C([C@]1(N(C)C3=O)C(O)C)=O '
               'NAME: Verticillin D REASON: WRONGLY CLASSIFIED Molecule '
               'appears to be a 3-oxo steroid with beta configuration based on '
               'heuristic criteria\n'
               ' * SMILES: '
               'O1CC2=C([C@@](O)(CC)C1=O)C=C3N(CC=4C3=NC=5C(C4CC)=CC=CC5)C2=O '
               'NAME: 7-ethylcamptothecin REASON: WRONGLY CLASSIFIED Molecule '
               'appears to be a 3-oxo steroid with beta configuration based on '
               'heuristic criteria\n'
               ' * SMILES: '
               'O[C@@H]1[C@@]2([C@@]([C@](C1)([C@@H](C[C@@H](/C=C(\\C)/C([O-])=O)O)C)[H])(CC=C3C2=CCC4[C@@]3(CCC(=O)C4(C)C)C)C)C '
               'NAME: ganoderate Jc REASON: WRONGLY CLASSIFIED Molecule '
               'appears to be a 3-oxo steroid with beta configuration based on '
               'heuristic criteria\n'
               ' * SMILES: '
               'FC12[C@]([C@]3([C@@]([C@](O)([C@@H](C3)C)C(=O)COC(=O)C(C)(C)C)(C[C@@H]1O)C)[H])(C[C@H](F)C=4[C@]2(C)C=CC(=O)C4)[H].OC=1C(=CC=CC1)C(O)=O '
               'NAME: Losalen REASON: WRONGLY CLASSIFIED Molecule appears to '
               'be a 3-oxo steroid with beta configuration based on heuristic '
               'criteria\n'
               ' * SMILES: '
               'C[C@]1(O)CC[C@H]2[C@@H]3CCC4=CC(=O)C(O)=C[C@]4(C)[C@H]3CC[C@]12C '
               'NAME: 2,17beta-Dihydroxy-17-methylandrosta-1,4-dien-3-one '
               'REASON: WRONGLY CLASSIFIED Molecule appears to be a 3-oxo '
               'steroid with beta configuration based on heuristic criteria\n'
               ' * SMILES: '
               'O=C1C2=C(O)C=CC3=C2C(=C4C5=C(C(O)=CC=C5)[C@@H]([C@@H]([C@@H]34)OC)OC)CC1 '
               'NAME: 6bS, 7R, 8S)-7-methoxy-4, 8, 9-trihydroxy-1, 6b, 7, '
               '8-tetrahydro-2H-benzo[j]fluoranthen-3-one REASON: WRONGLY '
               'CLASSIFIED Molecule appears to be a 3-oxo steroid with beta '
               'configuration based on heuristic criteria\n'
               ' * SMILES: '
               'C1=C2C(=CC(=C1Cl)Br)C3=C(N2)C([C@]4([C@@]5(C3)C[NH+]6[C@](C4)(CCC6)C(N5)=O)[H])(C)C '
               'NAME: (+)-malbrancheamide D(1+) REASON: WRONGLY CLASSIFIED '
               'Molecule appears to be a 3-oxo steroid with beta configuration '
               'based on heuristic criteria\n'
               ' * SMILES: '
               'O=C1N2C(=NC3=C1C=CC=C3)C(=O)C(C)(C)[C@]4([C@@H]2C[C@@]5(C6=C(C=CC=C6)N7[C@H]5NC(C)(C)C7=O)O4)O '
               'NAME: Scedapin D REASON: WRONGLY CLASSIFIED Molecule appears '
               'to be a 3-oxo steroid with beta configuration based on '
               'heuristic criteria\n'
               ' * SMILES: '
               '[C@@]1(C(O[C@@]2([C@](O)([C@@]34[C@H](OC(C)=O)[C@@]([H])([C@H]([C@H]([C@@]3([C@@H](OC(=O)C)[C@H]2OC(C)=O)COC(=O)C)OC(=O)C)OC(C)=O)[C@@](COC(C5=C([C@H]1C)C=CN=C5)=O)(C)O4)C)[H])=O)(C)O '
               'NAME: wilfordinine B REASON: WRONGLY CLASSIFIED Molecule '
               'appears to be a 3-oxo steroid with beta configuration based on '
               'heuristic criteria\n'
               ' * SMILES: '
               'O=C1[C@]2(C(=C3[C@@]([C@@]4([C@](CC3)(C[C@H](O)CC4)[H])C)(C1)[H])CC[C@@]2([C@@H](CCC(O)=O)C)[H])C '
               'NAME: 3alpha-Hydroxy-12-oxo-5beta-chol-8(14)-en-24-oic Acid '
               'REASON: WRONGLY CLASSIFIED Molecule appears to be a 3-oxo '
               'steroid with beta configuration based on heuristic criteria\n'
               ' * SMILES: '
               '[H][C@@]1(CC[C@@]2([H])[C@]3([H])CCC4=CC(=O)CC[C@]4(C)[C@@]3([H])CC[C@]12C)[C@@H](C)O '
               'NAME: (20R)-20-hydroxypregn-4-en-3-one REASON: WRONGLY '
               'CLASSIFIED Molecule appears to be a 3-oxo steroid with beta '
               'configuration based on heuristic criteria\n'
               ' * SMILES: '
               'CC(C)=C[C@H]1C[C@H](CO1)[C@@H]1CC[C@]2(C)C3=CC[C@H]4C(C)(C)C(=O)CC[C@]4(C)[C@H]3CC[C@@]12C '
               'NAME: deoxyflindissone REASON: WRONGLY CLASSIFIED Molecule '
               'appears to be a 3-oxo steroid with beta configuration based on '
               'heuristic criteria\n'
               ' * SMILES: '
               '[H][C@@]12C[C@@H](C)[C@H](C(=O)COC(=O)C(C)(C)C)[C@@]1(C)C[C@H](O)[C@@]1(Cl)[C@@]2([H])C[C@H](F)C2=CC(=O)C=C[C@]12C '
               'NAME: clocortolone pivalate REASON: WRONGLY CLASSIFIED '
               'Molecule appears to be a 3-oxo steroid with beta configuration '
               'based on heuristic criteria\n'
               ' * SMILES: '
               'C[C@@]12[C@]([C@]3([C@]([C@H](C1)O)([C@]4(C)C(CC3)=CC(C=C4)=O)[H])[H])(CC[C@@]2(C(CN5CCN(CC5)C)=O)O)[H] '
               'NAME: mazipredone REASON: WRONGLY CLASSIFIED Molecule appears '
               'to be a 3-oxo steroid with beta configuration based on '
               'heuristic criteria\n'
               ' * SMILES: '
               'O=C1[C@]2([C@@](CC[C@@]2([C@@H](CCC(O)=O)C)[H])(C=3C([C@@]4([C@](CC3)(C[C@H](O)CC4)[H])C)=C1)[H])C '
               'NAME: 3alpha-Hydroxy-12-oxo-5beta-chola-7,9(11)-dien-24-oic '
               'Acid REASON: WRONGLY CLASSIFIED Molecule appears to be a 3-oxo '
               'steroid with beta configuration based on heuristic criteria\n'
               'False negatives: NONE\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'C[NH+]1CCC(CC1)N1CCN(CC1)C(=O)[C@@H](CC1=CC2=C(NN=C2)C(C)=C1)NC(=O)N1CCC(CC1)C1=CC2=C(NC1=O)C=CC=C2',
                                     'name': 'zavegepant(1+)',
                                     'reason': 'Fused ring system does not '
                                               'match typical steroid nucleus. '
                                               'Expected exactly 4 fused rings '
                                               '(3 six-membered and 1 '
                                               'five-membered) but none '
                                               'found.'},
                                 {   'smiles': 'CC1=CC=CC(=C1)C(=O)NNC(=O)C2=C(C3=CC=CC=C3N(C2=O)C)O',
                                     'name': "4-hydroxy-1-methyl-N'-[(3-methylphenyl)-oxomethyl]-2-oxo-3-quinolinecarbohydrazide",
                                     'reason': 'Fused ring system does not '
                                               'match typical steroid nucleus. '
                                               'Expected exactly 4 fused rings '
                                               '(3 six-membered and 1 '
                                               'five-membered) but none '
                                               'found.'},
                                 {   'smiles': 'C[C@H]1CN(C(=O)C2=C(C=CC(=C2)NC(=O)CCCN(C)C)O[C@@H]1CN(C)C(=O)NC3CCCCC3)[C@H](C)CO',
                                     'name': 'N-[(2S,3S)-2-[[[(cyclohexylamino)-oxomethyl]-methylamino]methyl]-5-[(2R)-1-hydroxypropan-2-yl]-3-methyl-6-oxo-3,4-dihydro-2H-1,5-benzoxazocin-8-yl]-4-(dimethylamino)butanamide',
                                     'reason': 'Fused ring system does not '
                                               'match typical steroid nucleus. '
                                               'Expected exactly 4 fused rings '
                                               '(3 six-membered and 1 '
                                               'five-membered) but none '
                                               'found.'},
                                 {   'smiles': 'O1C(OC2(C=3OC=4C(C(=O)C3)=C(OC)C(OC)=C(OC)C4)C=CC(=O)C=C2)C(O)C(O)C(O)C1C(O)=O',
                                     'name': '3,4,5-trihydroxy-6-{[4-oxo-1-(5,6,7-trimethoxy-4-oxo-4H-chromen-2-yl)cyclohexa-2,5-dien-1-yl]oxy}oxane-2-carboxylic '
                                             'acid',
                                     'reason': 'Fused ring system does not '
                                               'match typical steroid nucleus. '
                                               'Expected exactly 4 fused rings '
                                               '(3 six-membered and 1 '
                                               'five-membered) but none '
                                               'found.'},
                                 {   'smiles': 'O=C(N[C@@H]1C(OC2(C1)[C@H]3O[C@H]3C(O)(CC(=O)C)[C@@H]4[C@H]2O4)O)/C=C\\C(CC(CCCCCC)C)C',
                                     'name': 'Penicimutanolone',
                                     'reason': 'Fused ring system does not '
                                               'match typical steroid nucleus. '
                                               'Expected exactly 4 fused rings '
                                               '(3 six-membered and 1 '
                                               'five-membered) but none '
                                               'found.'},
                                 {   'smiles': 'O(C(=O)CCCCCCCCCCCCCCCCC)C[C@@H](OC(=O)CCCCCCC/C=C\\CCCC)COC(=O)CCCCCCCCCCCCCCC',
                                     'name': 'TG(16:0/14:1(9Z)/18:0)',
                                     'reason': 'No rings found in the '
                                               'molecule'},
                                 {   'smiles': 'O1C(O)C(C(C1)CC2=CC=3OCOC3C=C2)CC4=CC(OC)=C(OC)C=C4',
                                     'name': "(8R,8'R,9S)-9-Hydroxy-3,4-dimethoxy-3',4'-methylenoxy-9,9'-epoxylignan",
                                     'reason': 'Fused ring system does not '
                                               'match typical steroid nucleus. '
                                               'Expected exactly 4 fused rings '
                                               '(3 six-membered and 1 '
                                               'five-membered) but none '
                                               'found.'},
                                 {   'smiles': 'CCCCCCCCCCCCCCCC(=O)OC[C@H](COP(O)(=O)O[C@H]1[C@H](O)[C@@H](O)[C@H](O)[C@@H](O)[C@H]1O)OC(=O)CCCCCCCCCCC',
                                     'name': '1-palmitoyl-2-lauroyl-sn-glycero-3-phospho-1D-myo-inositol',
                                     'reason': 'Fused ring system does not '
                                               'match typical steroid nucleus. '
                                               'Expected exactly 4 fused rings '
                                               '(3 six-membered and 1 '
                                               'five-membered) but none '
                                               'found.'},
                                 {   'smiles': 'O=C1C2=C([C@@H](O)CC1)[C@@H]([C@H](O)CCC)OC2',
                                     'name': 'Phomopsiketone F',
                                     'reason': 'Fused ring system does not '
                                               'match typical steroid nucleus. '
                                               'Expected exactly 4 fused rings '
                                               '(3 six-membered and 1 '
                                               'five-membered) but none '
                                               'found.'},
                                 {   'smiles': 'C1CC(C1)CN(C[C@H]2[C@H]([C@H](N2)CO)C3=CC=CC=C3)C(=O)C4=CC=C(C=C4)F',
                                     'name': 'N-(cyclobutylmethyl)-4-fluoro-N-[[(2R,3R,4S)-4-(hydroxymethyl)-3-phenyl-2-azetidinyl]methyl]benzamide',
                                     'reason': 'Fused ring system does not '
                                               'match typical steroid nucleus. '
                                               'Expected exactly 4 fused rings '
                                               '(3 six-membered and 1 '
                                               'five-membered) but none '
                                               'found.'}],
    'sample_false_negatives': [   {   'smiles': 'CC(=O)[C@H]1CC[C@H]2[C@@H]3CC[C@@H]4CC(=O)CC[C@]4(C)[C@H]3[C@@H]3O[C@@H]3[C@]12C',
                                      'name': '11alpha,12alpha-Epoxy-5beta-pregnane-3,20-dione',
                                      'reason': 'Fused ring system does not '
                                                'match typical steroid '
                                                'nucleus. Expected exactly 4 '
                                                'fused rings (3 six-membered '
                                                'and 1 five-membered) but none '
                                                'found.'}],
    'attempt': 2,
    'reasoning': 'We can try to improve the algorithm by “forcing” a stricter '
                 'interpretation of what the steroid nucleus should be. In the '
                 'previous attempt the code simply examined the largest fused '
                 'ring system (with ≥4 rings) and counted the number of 6‐ and '
                 '5‐membered rings. However, many molecules (even '
                 'non‐steroids) may have a fused ring system that has extra '
                 'rings (or extra chiral markers) so that the presence of any '
                 '“@@” annotation plus a ring bound ketone is not enough. One '
                 'idea is to search among the fused ring systems for one that '
                 'has exactly four rings and, within that system, exactly '
                 'three 6‐membered rings and one 5‐membered ring (the classic '
                 'cyclopentanoperhydrophenanthrene core). Also, rather than '
                 'relying on a “GetBondTypeAsDouble” call, we can check for a '
                 'bond whose type is DOUBLE (using RDKit’s bond type enum) and '
                 'require that the carbon bearing that double bond is part of '
                 'our candidate steroid nucleus. Finally, rather than using '
                 'any “@@” marker from the entire SMILES, by combining all '
                 'these requirements (a distinct four–ring fused system plus '
                 'an internal ketone plus at least one chiral marker) we hope '
                 'to reduce the false positives. \n'
                 '\n'
                 'Below is one implementation that incorporates these ideas. '
                 '(Note that these steps are all heuristic and may not catch '
                 '100% of cases.) \n'
                 '\n'
                 'Below is the single Python code block:',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 26,
    'num_false_positives': 2085,
    'num_true_negatives': 140188,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.01231643770724775,
    'recall': 0.9629629629629629,
    'f1': 0.02432179607109448,
    'accuracy': 0.9853408292340127,
    'negative_predictive_value': 0.9999928667727139}