"""
Classifies: CHEBI:35342 17alpha-hydroxy steroid
"""
#!/usr/bin/env python
"""
Classifies: 17alpha-hydroxy steroid
Definition: The alpha-stereoisomer of 17-hydroxy steroid.
Heuristic (improved):
  1. Require a fused steroid nucleus: exactly one 5-membered ring (D-ring)
     and at least 3 six-membered rings (A, B, C). We then build a steroid_core
     as the union of the D-ring and those six-membered rings that share atoms with it.
  2. In the D-ring, look for a candidate carbon (atomic #6) that is:
       - Substituted by an –OH (an oxygen neighbor bearing at least one hydrogen)
       - Chiral (has a defined chiral tag)
       - Has three heavy-atom (non-H) neighbors (besides the hydroxyl oxygen, there
         should be three carbon neighbors as expected for C17)
       - Has at least one heavy neighbor that is not in the steroid_core (this should
         be the exocyclic side chain at C17)
  3. If exactly one candidate is found, report success (including any CIP assignment),
     otherwise report failure.
Note: This heuristic remains simplified, since the full stereochemical assignment
      of steroids can be complex.
"""
from rdkit import Chem
from rdkit.Chem import AllChem, rdMolDescriptors

def is_17alpha_hydroxy_steroid(smiles: str):
    """
    Determines if a molecule belongs to the 17alpha-hydroxy steroid class based on its SMILES string.
    
    Args:
        smiles (str): SMILES string of the molecule.
        
    Returns:
        bool: True if the molecule is classified as a 17alpha-hydroxy steroid, False otherwise.
        str: A reason for the classification decision.
    """
    # Parse the SMILES string:
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
    
    # Force assignment of stereochemistry (including CIP codes) if possible.
    Chem.AssignStereochemistry(mol, force=True, cleanIt=True)
    
    # Get ring information. We require the presence of rings.
    rings = mol.GetRingInfo().AtomRings()
    if not rings:
        return False, "No rings detected – not a steroid"
    
    # Identify the unique 5-membered ring (our D-ring candidate).
    five_membered = [ring for ring in rings if len(ring) == 5]
    if len(five_membered) != 1:
        return False, f"Expected exactly 1 five-membered ring (steroid D-ring), but found {len(five_membered)}"
    
    # Check that there are at least 3 six-membered rings (steroid A, B, C).
    six_membered = [ring for ring in rings if len(ring) == 6]
    if len(six_membered) < 3:
        return False, f"Expected at least 3 six-membered rings (steroid A, B, C), but found {len(six_membered)}"
    
    # Build the fused steroid core: start with the set of atoms in the D-ring,
    # and add any six-membered ring that shares an atom with the D-ring.
    d_ring = five_membered[0]
    steroid_core = set(d_ring)
    for ring in six_membered:
        if set(ring).intersection(steroid_core):
            steroid_core.update(ring)
    # (For our purposes, steroid_core is expected to contain most atoms of the fused steroid nucleus.)
    
    candidate_found = None
    candidate_reason = ""
    
    # Iterate over atoms in the D-ring looking for a candidate C17.
    for atom_idx in d_ring:
        atom = mol.GetAtomWithIdx(atom_idx)
        # Expect a carbon atom in the D-ring.
        if atom.GetAtomicNum() != 6:
            continue
            
        # Look for an -OH group: an oxygen neighbor that itself has at least one hydrogen.
        oh_found = False
        for nbr in atom.GetNeighbors():
            if nbr.GetAtomicNum() == 8 and nbr.GetTotalNumHs() > 0:
                oh_found = True
                break
        if not oh_found:
            continue
        
        # Check that the atom is chiral.
        if atom.GetChiralTag() == Chem.rdchem.ChiralType.CHI_UNSPECIFIED:
            candidate_reason = "Hydroxyl-bearing carbon in D-ring is not stereochemically defined"
            continue
        
        # Count heavy-atom neighbors (ignore hydrogens and the oxygen from the OH group separately).
        heavy_neighbors = [nbr for nbr in atom.GetNeighbors() if nbr.GetAtomicNum() > 1]
        # For a typical C17, expect three carbon neighbors (one from the fused core and one exocyclic).
        if len(heavy_neighbors) != 4:  
            # Typically, C17 in a steroid is bonded to: two ring carbons, one oxygen (the OH), and one exocyclic carbon.
            # Thus heavy neighbor count including oxygen is 4.
            continue
        
        # Now check that at least one heavy neighbor (apart from the oxygen) lies outside the steroid_core.
        exocyclic = False
        for nbr in heavy_neighbors:
            # Skip oxygen neighbor (the -OH)
            if nbr.GetAtomicNum() == 8:
                continue
            if nbr.GetIdx() not in steroid_core:
                exocyclic = True
                break
        if not exocyclic:
            candidate_reason = "Hydroxyl-bearing carbon in D-ring does not show an exocyclic substituent"
            continue
        
        # If we have reached here, candidate meets our criteria.
        # (Optionally report the CIP code if it exists.)
        cip = atom.GetProp('_CIPCode') if atom.HasProp('_CIPCode') else "unknown"
        candidate_found = (atom_idx, cip)
        candidate_reason = f"Found candidate D-ring hydroxyl carbon (likely C17) with CIP '{cip}', attached to exocyclic side-chain"
        break  # Stop after the first candidate found

    if candidate_found is not None:
        return True, candidate_reason
    else:
        return False, f"Steroid nucleus identified but no suitable 17α–OH candidate in the D-ring was detected. {candidate_reason}"

# Example usage (for testing – remove or comment when using as module):
if __name__ == "__main__":
    # Test with one example SMILES (17α-hydroxypregnenolone)
    test_smiles = "CC(=O)[C@@]1(O)CC[C@H]2[C@@H]3CC=C4C[C@@H](O)CC[C@]4(C)[C@H]3CC[C@]12C"
    result, reason = is_17alpha_hydroxy_steroid(test_smiles)
    print(result, reason)


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:35342',
                          'name': '17alpha-hydroxy steroid',
                          'definition': 'The alpha-stereoisomer of 17-hydroxy '
                                        'steroid.',
                          'parents': ['CHEBI:36838'],
                          'xrefs': ['KEGG:C03336'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 87,
                           'log_lines_of_code': 4.465908118654584,
                           'indent_by_line': [   1,
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
                                                 1,
                                                 2,
                                                 3,
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
                                                 3,
                                                 3,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 4,
                                                 4,
                                                 2,
                                                 3,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 3,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 3,
                                                 3,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 3,
                                                 4,
                                                 3,
                                                 4,
                                                 4,
                                                 2,
                                                 3,
                                                 3,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 0,
                                                 1,
                                                 2,
                                                 1,
                                                 2,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 1],
                           'max_indent': 4,
                           'imports': [   'from rdkit import Chem',
                                          'from rdkit.Chem import AllChem, '
                                          'rdMolDescriptors'],
                           'imports_count': 2,
                           'methods_called': [   'HasProp',
                                                 'GetNeighbors',
                                                 'GetTotalNumHs',
                                                 'GetChiralTag',
                                                 'GetRingInfo',
                                                 'AtomRings',
                                                 'GetAtomicNum',
                                                 'GetIdx',
                                                 'update',
                                                 'GetProp',
                                                 'intersection',
                                                 'GetAtomWithIdx',
                                                 'MolFromSmiles',
                                                 'AssignStereochemistry'],
                           'methods_called_count': 14,
                           'smarts_strings': [],
                           'smarts_strings_count': 0,
                           'defs': ['is_17alpha_hydroxy_steroid(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "No rings detected – not a '
                                          'steroid"',
                                          'False, f"Expected exactly 1 '
                                          'five-membered ring (steroid '
                                          'D-ring), but found '
                                          '{len(five_membered)}"',
                                          'False, f"Expected at least 3 '
                                          'six-membered rings (steroid A, B, '
                                          'C), but found {len(six_membered)}"',
                                          'True, candidate_reason',
                                          'False, f"Steroid nucleus identified '
                                          'but no suitable 17α–OH candidate in '
                                          'the D-ring was detected. '
                                          '{candidate_reason}"'],
                           'returns_count': 6,
                           'complexity': 5.893181623730916},
    'message': '\n'
               'Attempt failed: F1 score of 0.023529411764705882 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: '
               'C1[C@@]2([C@@]([C@]3(CCC(C=C3[C@@H]1O)=O)C)(CC[C@]4([C@]2(C[C@H]([C@]4(O)C(C)=O)O)[H])C)[H])[H] '
               'NAME: 6beta,16alpha,17alpha-trihydroxyprogesterone REASON: '
               'CORRECT Found steroid nucleus with D-ring hydroxyl carbon '
               "having CIP 'S' (α)\n"
               ' * SMILES: '
               '[H][C@@]12CC(O)[C@](O)(C(=O)CO)[C@@]1(C)C[C@H](O)[C@@]1([H])[C@@]2([H])CCC2=CC(=O)C=C[C@]12C '
               'NAME: 16-hydroxyprednisolone REASON: CORRECT Found steroid '
               "nucleus with D-ring hydroxyl carbon having CIP 'S' (α)\n"
               ' * SMILES: '
               '[C@H]([C@@]1(O)CC[C@]2([C@@]3(C[C@H]([C@]4(CC=CC(=O)[C@@]4([C@]3(CC[C@@]21C)[H])C)O)O)[H])[H])([C@@]5(OC(C(=C(C5)C)CO)=O)[H])C '
               'NAME: 5alpha,6beta,17alpha,27-tetrahydroxywithanolide REASON: '
               'CORRECT Found steroid nucleus with D-ring hydroxyl carbon '
               "having CIP 'S' (α)\n"
               ' * SMILES: '
               'C1[C@@]2([C@]3(CC[C@]4(C)[C@]([C@@H](C[C@]4([C@@]3(CC=C2C[C@H](C1)O)[H])[H])O)(C(=O)C)O)[H])C '
               'NAME: 16alpha,17alpha-dihydroxypregnenolone REASON: CORRECT '
               'Found steroid nucleus with D-ring hydroxyl carbon having CIP '
               "'S' (α)\n"
               ' * SMILES: '
               'C12=CC=C(C=C1CC[C@@]3([C@@]2(CC[C@]4([C@]3(C[C@H]([C@H]4O)O)[H])C)[H])[H])O '
               'NAME: 17-epiestriol REASON: CORRECT Found steroid nucleus with '
               "D-ring hydroxyl carbon having CIP 'S' (α)\n"
               ' * SMILES: '
               '[C@]123[C@@]([C@]4(CC[C@]5([C@]([C@@]4(C[C@H]1O2)[H])(CC[C@@]5([C@H](C)[C@@]6(OC(=O)C(=C(C6)C)CO[C@@H]7O[C@@H]([C@@H](O)[C@H](O)[C@H]7O)CO)[H])O)[H])C)[H])(C(=O)C=C[C@@H]3O)C '
               'NAME: 17alpha-sitoindoside IX REASON: CORRECT Found steroid '
               "nucleus with D-ring hydroxyl carbon having CIP 'S' (α)\n"
               ' * SMILES: '
               '[H][C@@]1(CC(C)=C(C)C(=O)O1)[C@@H](C)[C@@]1(O)CC[C@@]2([H])[C@]3([H])C[C@@]4([H])O[C@]44[C@@H](O)C=CC(=O)[C@]4(C)[C@@]3([H])CC[C@]12C '
               'NAME: tubocapsanolide F REASON: CORRECT Found steroid nucleus '
               "with D-ring hydroxyl carbon having CIP 'S' (α)\n"
               ' * SMILES: '
               'O[C@H]1[C@H](O)[C@H](O[C@H]([C@@H]1O)OCC=2C(O[C@@]([C@H]([C@@]3(O)CC[C@]4([C@@]5(C[C@H]([C@]6(CC=CC(=O)[C@@]6([C@]5(CC[C@@]43C)[H])C)O)O)[H])[H])C)(CC2C)[H])=O)CO '
               'NAME: 5alpha,6beta,17alpha-trihydroxywithanolide '
               '27-O-beta-D-glucoside REASON: CORRECT Found steroid nucleus '
               "with D-ring hydroxyl carbon having CIP 'S' (α)\n"
               ' * SMILES: '
               'O[C@H]1[C@H](O)[C@H](O[C@H]([C@@H]1O)OCC=2C(O[C@@]([C@H]([C@@]3(O)CC[C@]4([C@@]5([C@H]6[C@@H]([C@]7(CC=CC(=O)[C@@]7([C@]5(CC[C@@]43C)[H])C)O)O6)[H])[H])C)(CC2C)[H])=O)CO '
               'NAME: withanone 27-O-beta-D-glucoside REASON: CORRECT Found '
               "steroid nucleus with D-ring hydroxyl carbon having CIP 'S' "
               '(α)\n'
               ' * SMILES: '
               '[H][C@@]12C[C@@H](O)[C@](O)(C(=O)CO)[C@@]1(C)C[C@H](O)[C@@]1(F)[C@@]2([H])CCC2=CC(=O)C=C[C@]12C '
               'NAME: triamcinolone REASON: CORRECT Found steroid nucleus with '
               "D-ring hydroxyl carbon having CIP 'S' (α)\n"
               ' * SMILES: '
               '[H][C@@]12C[C@@H](O)[C@](O)(C(=O)CO)[C@@]1(C)C[C@H](O)[C@@]1([H])[C@@]2([H])CCC2=CC(=O)C=C[C@]12C '
               'NAME: 16alpha-hydroxyprednisolone REASON: CORRECT Found '
               "steroid nucleus with D-ring hydroxyl carbon having CIP 'S' "
               '(α)\n'
               'False positives: SMILES: '
               'C[C@]12CC[C@H]3[C@@H](CCc4cc(OCC=C)ccc34)[C@@H]1C[C@H](O)[C@@H]2O '
               'NAME: 3-(Allyloxy)estra-1,3,5(10)-triene-16beta,17beta-diol '
               'REASON: WRONGLY CLASSIFIED Found steroid nucleus with D-ring '
               "hydroxyl carbon having CIP 'S' (α)\n"
               ' * SMILES: '
               'O=C1C=C2C(=CC(=O)OC2(C)C)[C@]3([C@@H]4[C@@]1([C@H]5C(=O)[C@@H](O[C@@H]6[C@@]5(O)[C@](C(=O)O6)(C)C4)C)C)OC3 '
               'NAME: Chrysogenolide F REASON: WRONGLY CLASSIFIED Found '
               "steroid nucleus with D-ring hydroxyl carbon having CIP 'S' "
               '(α)\n'
               ' * SMILES: '
               'O=C1O[C@@H]2C[C@H]3[C@H](C(C=C)=CC[C@@H]3[C@@]4([C@@]2([C@@]1([C@H](O)CC4)C)O)C)C '
               'NAME: Hawaiinolide F REASON: WRONGLY CLASSIFIED Found steroid '
               "nucleus with D-ring hydroxyl carbon having CIP 'S' (α)\n"
               ' * SMILES: '
               'O=C1O[C@@H]2C[C@@]3(O[C@H](C(=CC)C)[C@@H](C)C[C@H]3O)O[C@@H](C2)CC=C(C[C@H](C=CC=C4[C@]5([C@H]1C=C([C@@H](OC)[C@H]5OC4)C)O)C)C '
               'NAME: VM-44864 REASON: WRONGLY CLASSIFIED Found steroid '
               "nucleus with D-ring hydroxyl carbon having CIP 'S' (α)\n"
               ' * SMILES: '
               'O=C1C=C2[C@H](CC[C@]3([C@H]2C[C@H](O)[C@@H]3[C@@H](CC[C@@H](C(O)(C)C)C)C)C)[C@@]4([C@H]1C[C@H](O)CC4)C '
               'NAME: Psathergosterol C REASON: WRONGLY CLASSIFIED Found '
               "steroid nucleus with D-ring hydroxyl carbon having CIP 'S' "
               '(α)\n'
               ' * SMILES: '
               'C[C@]12CC[C@H]3[C@@H](CCC4=CC(=O)CC[C@]34C)[C@@H]1[C@@H](O)C[C@@H]2O '
               'NAME: 15alpha-hydroxytestosterone REASON: WRONGLY CLASSIFIED '
               'Found steroid nucleus with D-ring hydroxyl carbon having CIP '
               "'S' (α)\n"
               ' * SMILES: '
               'O=C(O)/C(=C/CC[C@H]([C@@H]1[C@@]2([C@@](C=3C([C@@]4([C@H](C([C@@H](O)CC4)(C)C)CC3)C)=CC2)(C)[C@H](C1)O)C)C)/C '
               'NAME: 15-hydroxy-ganoderic acid S REASON: WRONGLY CLASSIFIED '
               'Found steroid nucleus with D-ring hydroxyl carbon having CIP '
               "'S' (α)\n"
               ' * SMILES: '
               'O[C@]12[C@@](C(CC1)[C@@](O)([C@H](O)C[C@@H](C(C)C)C)C)(CCC3[C@@]4(C(C[C@@H](O)[C@@H](O)C4)C(=O)C=C23)C)C '
               'NAME: '
               '(2beta,3beta,9epsilon,17epsilon,22R)-2,3,14,20,22-Pentahydroxyergost-7-en-6-one '
               'REASON: WRONGLY CLASSIFIED Found steroid nucleus with D-ring '
               "hydroxyl carbon having CIP 'S' (α)\n"
               ' * SMILES: '
               'CC1C[C@@]2(C)C(CC[C@H]3[C@@H]4CC[C@](C)(O)[C@@]4(C)C[C@H](O)[C@]23F)=CC1=O '
               'NAME: '
               '9-Fluoro-11beta,17beta-dihydroxy-2,17-dimethylandrost-4-en-3-one '
               'REASON: WRONGLY CLASSIFIED Found steroid nucleus with D-ring '
               "hydroxyl carbon having CIP 'S' (α)\n"
               ' * SMILES: '
               'O=C1C2=C(O)C=CC=C2C3([C@@]1(O)C(=O)OC)OC=4C=5C(C=CC4)=CC=CC5O3 '
               'NAME: Palmarumycin B8 REASON: WRONGLY CLASSIFIED Found steroid '
               "nucleus with D-ring hydroxyl carbon having CIP 'S' (α)\n"
               ' * SMILES: '
               'O=C1C2=C([C@@]3([C@@H](O)C[C@@H]([C@]3(C1)C)[C@@H](CC(=O)C(O)C(C(=O)OC)C)C)C)CCC4[C@@]2(CC[C@@H](C4(C)C)O)C '
               'NAME: Resinacein R REASON: WRONGLY CLASSIFIED Found steroid '
               "nucleus with D-ring hydroxyl carbon having CIP 'S' (α)\n"
               ' * SMILES: '
               'O=C1OC([C@]2(C(=C3[C@@]([C@]45C(=C)[C@]([C@@H]3OC(=O)C)(OC([C@@]4(O)[C@H](C)OC5=O)=O)C)(C)CC2)C)C=C1)(C)C '
               'NAME: Austin REASON: WRONGLY CLASSIFIED Found steroid nucleus '
               "with D-ring hydroxyl carbon having CIP 'S' (α)\n"
               ' * SMILES: '
               'O([C@@H]1[C@H](O[C@H](OC[C@@H]2O[C@@H]([C@@H](O)[C@@H]2O)CO)[C@@H](O)[C@H]1O)CO[C@H]3O[C@@H]([C@@H](O)[C@H](O)[C@@H]3O[C@H]4O[C@@H]([C@@H](O)[C@H](O)[C@@H]4O[C@H]5O[C@@H]([C@@H](O)[C@H](O)[C@@H]5O)CO)CO)CO)[C@@H]6O[C@@H]([C@H](O)[C@H](O)[C@H]6NC(=O)C)CO '
               'NAME: '
               'N-[(2S,3R,4R,5R,6R)-2-[(2R,3S,4R,5S,6S)-6-[[(2S,3S,4S,5R)-3,4-Dihydroxy-5-(hydroxymethyl)oxolan-2-yl]methoxy]-2-[[(2S,3S,4S,5S,6R)-3-[(2R,3S,4S,5S,6R)-4,5-dihydroxy-6-(hydroxymethyl)-3-[(2R,3S,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxymethyl]-4,5-dihydroxyoxan-3-yl]oxy-4,5-dihydroxy-6-(hydroxymethyl)oxan-3-yl]acetamide '
               'REASON: WRONGLY CLASSIFIED Found steroid nucleus with D-ring '
               "hydroxyl carbon having CIP 'S' (α)\n"
               ' * SMILES: '
               'O=C1[C@]2(O)[C@]3([C@@H](C(CCC3)(C)C)CC[C@@]24C[C@]([C@H]1O)(O)[C@@](O)(CO)C4)C '
               'NAME: Phlebiakauranol alcohol REASON: WRONGLY CLASSIFIED Found '
               "steroid nucleus with D-ring hydroxyl carbon having CIP 'S' "
               '(α)\n'
               ' * SMILES: '
               'O[C@]1([C@@]2([C@]([C@]3([C@@]([C@@]4(C(=CC3)C[C@@H](O)CC4)C)(CC2)[H])[H])(CC1)[H])C)[C@@H]([C@@H](O)CC(C(C)C)=C)C '
               'NAME: 24-methylene-cholest-5-en-3beta,17alpha,22S-triol '
               'REASON: WRONGLY CLASSIFIED Found steroid nucleus with D-ring '
               "hydroxyl carbon having CIP 'S' (α)\n"
               ' * SMILES: '
               'C[C@@]12CCC[C@](C)([C@H]1CC[C@@]13C[C@@H](CC[C@@H]21)C(=C)[C@@H]3O)C(O)=O '
               'NAME: Grandifloric acid REASON: WRONGLY CLASSIFIED Found '
               "steroid nucleus with D-ring hydroxyl carbon having CIP 'S' "
               '(α)\n'
               ' * SMILES: '
               'O=C1C([C@H]2[C@](C3=C([C@]4([C@]([C@@H]([C@@H](CC/C=C(/C(=O)O)\\C)C)C[C@@H]4O)(C)CC3)C)[C@@H](C2)OC(=O)C)(C)CC1)(C)C '
               'NAME: '
               '(24E)-7alpha-acetoxy-15alpha-hydroxy-3-oxolanosta-8,24-dien-26-oic '
               'acid REASON: WRONGLY CLASSIFIED Found steroid nucleus with '
               "D-ring hydroxyl carbon having CIP 'S' (α)\n"
               ' * SMILES: '
               '[C@@]12(C3=CC=C[C@@H](CC(=CC[C@]4(O[C@@]5(C[C@H](C4)OC([C@]1([H])C=C(C)[C@H]([C@@]2([H])OC3)O)=O)O[C@@H]([C@H]([C@H](C5)O)C)/C(/C)=C/C)[H])C)C)O '
               'NAME: LL-F28249 beta REASON: WRONGLY CLASSIFIED Found steroid '
               "nucleus with D-ring hydroxyl carbon having CIP 'S' (α)\n"
               ' * SMILES: '
               'C1[C@@]2([C@]3(CC[C@]4([C@]([C@@]3(CC=C2CC(C1)=O)[H])(CC[C@@H]4O)[H])C)[H])C '
               'NAME: 17beta-hydroxy-5-androsten-3-one REASON: WRONGLY '
               'CLASSIFIED Found steroid nucleus with D-ring hydroxyl carbon '
               "having CIP 'S' (α)\n"
               ' * SMILES: '
               'Cc1cc(O)cc2CC[C@H]3[C@@H]4CC[C@H](O)[C@@]4(C)CC[C@@H]3c12 '
               'NAME: 1-Methylestra-1,3,5(10)-triene-3,17beta-diol REASON: '
               'WRONGLY CLASSIFIED Found steroid nucleus with D-ring hydroxyl '
               "carbon having CIP 'S' (α)\n"
               ' * SMILES: '
               '[H][C@]12CC[C@@]3(C)[C@]([H])([C@H](C)CCC(OO)C(C)=C)[C@@H](O)C[C@]3(C)C1=CC[C@@]1([H])C(C)(C)C(=O)CC[C@]21C '
               'NAME: Meliasenin L, (rel)- REASON: WRONGLY CLASSIFIED Found '
               "steroid nucleus with D-ring hydroxyl carbon having CIP 'S' "
               '(α)\n'
               ' * SMILES: '
               '[H][C@@]12CC=C3C[C@H](CC[C@]3(C)[C@@]1([H])CC[C@@]1(C)[C@@]2([H])C[C@H](O[C@@H]2OC[C@H](O)[C@H](O[C@@H]3OC[C@@H](O)[C@H](O)[C@H]3O)[C@H]2OC(C)=O)[C@]1(O)[C@@H](C)C(=O)CCC(C)C)O[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O '
               'NAME: '
               '3beta-[(beta-D-glucopyranosyl)oxy]-17alpha-hydroxy-16beta-[(O-beta-D-xylopyranosyl)-(1->3)-2-O-acetyl-alpha-L-arabinopyranosyloxy]cholest-5-en-22-one '
               'REASON: WRONGLY CLASSIFIED Found steroid nucleus with D-ring '
               "hydroxyl carbon having CIP 'S' (α)\n"
               ' * SMILES: '
               'O1C([C@@H](O)[C@H](O)C(O)[C@@H]1OC=2C=C3OC(=C(OC)C(=O)C3=C(O)C2)C4=CC(O)=C(O)C=C4)CO[C@@H]5O[C@H](C(O)[C@@H]5O)CO '
               'NAME: Quercetin 3-methyl ether '
               '7-alpha-L-arabinofuranosyl-(1->6)-glucoside REASON: WRONGLY '
               'CLASSIFIED Found steroid nucleus with D-ring hydroxyl carbon '
               "having CIP 'S' (α)\n"
               ' * SMILES: '
               'O=C1C2=C([C@@]3([C@@H](O)C[C@@H]([C@]3(C1)C)[C@@H](CC(=O)C(O)C(C(=O)O)C)C)C)[C@@H](O)C[C@@H]4[C@@]2(CC[C@@H](C4(C)C)O)C '
               'NAME: '
               '3beta,7beta,15alpha,24-tetrahydroxy-11,23-dioxolanost-8-en-26-oic '
               'acid REASON: WRONGLY CLASSIFIED Found steroid nucleus with '
               "D-ring hydroxyl carbon having CIP 'S' (α)\n"
               ' * SMILES: '
               'C1=C2C(CC[C@]3([C@@]4(CC[C@@H]([C@]4(CC[C@@]32[H])C)O)[H])[H])=CC(=C1)OS([O-])(=O)=O '
               'NAME: 17beta-estradiol 3-sulfate(1-) REASON: WRONGLY '
               'CLASSIFIED Found steroid nucleus with D-ring hydroxyl carbon '
               "having CIP 'S' (α)\n"
               'False negatives: SMILES: '
               '[H][C@@]12C[C@H](C)[C@](O)(C(=O)CO)[C@@]1(C)C[C@H](O)[C@@]1(F)[C@@]2([H])CCC2=CC(=O)C=C[C@]12C '
               'NAME: betamethasone REASON: MISSED Steroid nucleus identified '
               'but no 17α–OH group detected. D-ring hydroxyl carbon has CIP '
               "'R' which does not match expected 'S' for alpha\n"
               ' * SMILES: '
               '[H][C@@]12CCC3=CC(=O)C=C[C@]3(C)[C@@]1([H])[C@@H](O)C[C@@]1(C)[C@@]2([H])CC[C@]1(O)C(=O)OCCl '
               'NAME: loteprednol REASON: MISSED Steroid nucleus identified '
               'but no 17α–OH group detected. D-ring hydroxyl carbon has CIP '
               "'R' which does not match expected 'S' for alpha\n"
               ' * SMILES: '
               '[H][C@@]12CC[C@](O)(C(=O)CO)[C@@]1(C)C[C@H](O)[C@@]1([H])[C@@]2([H])C[C@H](O)C2=CC(=O)C=C[C@]12C '
               'NAME: 6alpha-hydroxyprednisolone REASON: MISSED Steroid '
               'nucleus identified but no 17α–OH group detected. D-ring '
               "hydroxyl carbon has CIP 'R' which does not match expected 'S' "
               'for alpha\n'
               ' * SMILES: '
               'C[C@]12CC[C@H]3[C@@H](CCC4=CC(=O)CC[C@]34C)[C@@H]1CC[C@H]2O '
               'NAME: epitestosterone REASON: MISSED Steroid nucleus '
               'identified but no 17α–OH group detected. D-ring hydroxyl '
               "carbon has CIP 'R' which does not match expected 'S' for "
               'alpha\n'
               ' * SMILES: '
               '[H][C@@]12CC=C3C[C@@H](O)CC[C@]3(C)[C@@]1([H])CC[C@@]1(C)[C@@]2([H])CC[C@]1(O)C(=O)CO '
               'NAME: 17alpha,21-dihydroxypregnenolone REASON: MISSED Steroid '
               'nucleus identified but no 17α–OH group detected. D-ring '
               "hydroxyl carbon has CIP 'R' which does not match expected 'S' "
               'for alpha\n'
               ' * SMILES: '
               '[H][C@]12C[C@@]3([H])[C@]4([H])CC=C5C[C@@H](O)CC[C@]5(C)[C@@]4([H])CC[C@]3(C)[C@@]1(O)[C@H](C)[C@@]1(CC[C@@H](C)CO1)O2 '
               'NAME: pennogenin REASON: MISSED Expected 1 five-membered ring '
               '(steroid D-ring), but found 2\n'
               ' * SMILES: '
               'CC1C[C@H]2[C@@H]3CC[C@](O)(C(=O)CO)[C@@]3(C)C[C@H](O)[C@@H]2[C@@]2(C)C=CC(=O)C=C12 '
               'NAME: 6-methylprednisolone REASON: MISSED Steroid nucleus '
               'identified but no 17α–OH group detected. D-ring hydroxyl '
               "carbon has CIP 'R' which does not match expected 'S' for "
               'alpha\n'
               ' * SMILES: '
               'C1[C@]2([C@]3([C@@]([C@@]4(C(=CC(CC4)=O)[C@H](C3)C)C)(CC[C@@]2([C@@](C1)(O)C(=O)C)C)[H])[H])[H] '
               'NAME: medroxyprogesterone REASON: MISSED Steroid nucleus '
               'identified but no 17α–OH group detected. D-ring hydroxyl '
               "carbon has CIP 'R' which does not match expected 'S' for "
               'alpha\n'
               ' * SMILES: '
               '[H][C@]12CC[C@@]3([H])[C@]4([H])CC[C@](O)(C(=O)CO)[C@@]4(C)CC(=O)[C@]3([H])[C@@]1(C)CCC(=O)C2 '
               'NAME: 17,21-dihydroxy-5beta-pregnane-3,11,20-trione REASON: '
               'MISSED Steroid nucleus identified but no 17α–OH group '
               "detected. D-ring hydroxyl carbon has CIP 'R' which does not "
               "match expected 'S' for alpha\n"
               ' * SMILES: '
               '[H][C@@]12CC[C@](O)([C@@H](O)CO)[C@@]1(C)C[C@H](O)[C@@]1([H])[C@@]2([H])CCC2=CC(=O)C=C[C@]12C '
               'NAME: 20beta-dihydroprednisolone REASON: MISSED Steroid '
               'nucleus identified but no 17α–OH group detected. D-ring '
               "hydroxyl carbon has CIP 'R' which does not match expected 'S' "
               'for alpha\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'O=C(N1[C@H](CCC1)C(O)=O)[C@@H](NC(=O)[C@@H](N)CC(O)=O)CCC(=O)N',
                                     'name': 'Asp-Gln-Pro',
                                     'reason': 'Expected at least 3 '
                                               'six-membered rings (steroid A, '
                                               'B, C), but found 0'},
                                 {   'smiles': 'O1C=2C(C(O)=C(CC3=C(O)C=4C(OC3=O)=CC=CC4C)C1=O)=C(C=CC2)C',
                                     'name': 'Gerberinol',
                                     'reason': 'Expected exactly 1 '
                                               'five-membered ring (steroid '
                                               'D-ring), but found 0'},
                                 {   'smiles': 'O=C(O)/C(=C/[C@H]1C=C(CC[C@@H]1C(C)C)CO)/COC(=O)C',
                                     'name': '3-acetylgliocladic acid',
                                     'reason': 'Expected exactly 1 '
                                               'five-membered ring (steroid '
                                               'D-ring), but found 0'},
                                 {   'smiles': 'O=C(CCCCCCCCC)C=1C=CC(=NC1)CCCCCCCCC',
                                     'name': '1-(6-Nonylpyridin-3-yl)decan-1-one',
                                     'reason': 'Expected exactly 1 '
                                               'five-membered ring (steroid '
                                               'D-ring), but found 0'},
                                 {   'smiles': 'CCC(=O)O[C@H]1[C@H](C)O[C@H](C[C@@]1(C)O)O[C@@H]1[C@@H](C)O[C@@H](O[C@H]2[C@@H](CC=O)C[C@@H](C)[C@@H](O)\\C=C\\C=C\\C[C@@H](C)OC(=O)C[C@@H](O)[C@@H]2OC)[C@H](O)[C@H]1N(C)C',
                                     'name': 'Leucomycin A7',
                                     'reason': 'Expected exactly 1 '
                                               'five-membered ring (steroid '
                                               'D-ring), but found 0'},
                                 {   'smiles': 'C[C@H]1O[C@H](C[C@@H](O)[C@@H]1O)c1ccc2C(=O)C3=C([C@H](O)C[C@]4(O)C[C@@](C)(O)CC(=O)[C@]34O)C(=O)c2c1O',
                                     'name': 'Urdamycinone F',
                                     'reason': 'Expected exactly 1 '
                                               'five-membered ring (steroid '
                                               'D-ring), but found 0'},
                                 {   'smiles': 'CC(C)=CCC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\COP([O-])(=O)OP([O-])([O-])=O',
                                     'name': 'all-trans-dodecaprenyl '
                                             'diphosphate(3-)',
                                     'reason': 'No rings detected – not a '
                                               'steroid'},
                                 {   'smiles': '[O-][N+](=O)N1CN(CN(CN(C1)[N+]([O-])=O)[N+]([O-])=O)[N+]([O-])=O',
                                     'name': 'octogen',
                                     'reason': 'Expected exactly 1 '
                                               'five-membered ring (steroid '
                                               'D-ring), but found 0'},
                                 {   'smiles': 'CC(=O)NCCC[NH2+]CCCC[NH2+]CCCNC(C)=O',
                                     'name': 'N(1),N(12)-diacetylsperminium(2+)',
                                     'reason': 'No rings detected – not a '
                                               'steroid'},
                                 {   'smiles': 'C[C@@H]([C@H]1CC[C@H]2[C@H](CCc3cc(O)ccc3C)C(=O)CC[C@]12C)C(O)=O',
                                     'name': '3-hydroxy-9-oxo-9,10-seco-23,24-bisnorchola-1,3,5(10)-trien-22-oic '
                                             'acid',
                                     'reason': 'Expected at least 3 '
                                               'six-membered rings (steroid A, '
                                               'B, C), but found 2'}],
    'sample_false_negatives': [   {   'smiles': 'C[C@]12CC[C@H]3[C@@H](CCC4=CC(=O)CC[C@]34C)[C@@H]1CC[C@H]2O',
                                      'name': 'epitestosterone',
                                      'reason': 'Steroid nucleus identified '
                                                'but no suitable 17α–OH '
                                                'candidate in the D-ring was '
                                                'detected. '},
                                  {   'smiles': '[H][C@]12C[C@@]3([H])[C@]4([H])CC=C5C[C@@H](O)CC[C@]5(C)[C@@]4([H])CC[C@]3(C)[C@@]1(O)[C@H](C)[C@@]1(CC[C@@H](C)CO1)O2',
                                      'name': 'pennogenin',
                                      'reason': 'Expected exactly 1 '
                                                'five-membered ring (steroid '
                                                'D-ring), but found 2'},
                                  {   'smiles': 'C[C@]12CC[C@H]3[C@@H](CC[C@@H]4CC(=O)CC[C@]34C)[C@@H]1CC[C@H]2O',
                                      'name': '5beta-dihydroepitestosterone',
                                      'reason': 'Steroid nucleus identified '
                                                'but no suitable 17α–OH '
                                                'candidate in the D-ring was '
                                                'detected. '},
                                  {   'smiles': 'C12=CC=C(C=C1CC[C@@]3([C@@]2(CC[C@]4([C@]3(C[C@H]([C@H]4O)O)[H])C)[H])[H])O',
                                      'name': '17-epiestriol',
                                      'reason': 'Steroid nucleus identified '
                                                'but no suitable 17α–OH '
                                                'candidate in the D-ring was '
                                                'detected. '},
                                  {   'smiles': '[H][C@@]1(CC[C@@]2(C)C(C1)=CC[C@]1([H])[C@]2([H])CC[C@@]2(C)[C@@]1([H])C[C@]1([H])O[C@]3(CC[C@@H](C)CO3)[C@@H](C)[C@]21O)O[C@@H]1O[C@H](CO)[C@@H](O)[C@]([H])(O[C@@H]2O[C@@H](C)[C@H](O)[C@@H](O)[C@H]2O)[C@H]1O',
                                      'name': 'mannioside A',
                                      'reason': 'Expected exactly 1 '
                                                'five-membered ring (steroid '
                                                'D-ring), but found 2'},
                                  {   'smiles': '[H][C@]12CC[C@]3(C)[C@H](O)CC[C@@]3([H])[C@]1([H])CCc1cc(O)ccc21',
                                      'name': '17alpha-estradiol',
                                      'reason': 'Steroid nucleus identified '
                                                'but no suitable 17α–OH '
                                                'candidate in the D-ring was '
                                                'detected. '}],
    'attempt': 2,
    'reasoning': 'Below is our revised Python solution. In our reasoning we '
                 'noted that the original heuristic depended solely on (and '
                 'assumed a specific) CIP “S” assignment on a '
                 'hydroxyl‐substituted carbon in the unique five‐membered (D) '
                 'ring. However, many false negatives (as well as some false '
                 'positives) were caused because (a) some known 17α–OH '
                 'steroids ended up with a CIP label “R” and (b) similar –OH '
                 'groups in a fused system (that is not the 17–OH) were being '
                 'picked up. To improve things we now do the following:\n'
                 '\n'
                 '1. We first insist that the molecule contains a fused '
                 'steroid nucleus as approximated by one five–membered ring '
                 'plus (at least) three six–membered rings. We then “fuse” '
                 '(merge) the atoms of the five–membered ring with those '
                 'six–membered rings that share an atom; the resulting set is '
                 'our candidate “steroid_core.”\n'
                 '\n'
                 '2. In the five–membered ring (presumed to be ring D) we '
                 'search for a carbon atom that is (a) bound to an –OH group, '
                 '(b) chiral (so that stereochemistry is defined), (c) has '
                 'exactly three heavy–atom neighbors (excluding the –OH '
                 'oxygen) as expected for C17 in classical steroids, and (d) '
                 'is attached to at least one neighbor outside the '
                 'steroid_core (the exocyclic side chain at C17).\n'
                 '\n'
                 'If exactly one such candidate is found, we judge that the '
                 'molecule is a 17α–hydroxy steroid (recognizing that our '
                 'previous CIP–based filter alone was not sufficient). '
                 'Otherwise we reject the molecule. (Note that the CIP code is '
                 'still reported if present but is no longer used alone to '
                 'decide the outcome.)\n'
                 '\n'
                 'Below is the single Python code block implementing this '
                 'revised heuristic:\n'
                 '\n'
                 '------------------------------------------------',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 80,
    'num_false_positives': 388,
    'num_true_negatives': 141826,
    'num_false_negatives': 6,
    'num_negatives': None,
    'precision': 0.17094017094017094,
    'recall': 0.9302325581395349,
    'f1': 0.2888086642599278,
    'accuracy': 0.9972312016865776,
    'negative_predictive_value': 0.9999576964295787}