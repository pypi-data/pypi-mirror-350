"""
Classifies: CHEBI:16158 steroid sulfate
"""
#!/usr/bin/env python
"""
Classifies: steroid sulfate
Definition: A sulfuric ester obtained by the formal condensation of a hydroxy group 
of any steroid with sulfuric acid. For our purposes a valid steroid sulfate must have a sulfate ester group (either anionic or neutral) 
that is attached either directly or via one intervening saturated (sp3 non‐aromatic) linker to a steroid nucleus. 
Our heuristic for a steroid nucleus is a fused polycyclic system composed solely
of 5‐ and 6‐membered rings with at least four rings (and with at least one 5‐membered ring and three 6‐membered rings).
"""

from rdkit import Chem
from rdkit.Chem import rdchem

def is_steroid_sulfate(smiles: str):
    """
    Determines if a molecule is a steroid sulfate based on its SMILES string.
    
    Process:
    1. Parse the molecule.
    2. Identify a candidate steroid nucleus:
       - Extract all rings of size 5 or 6.
       - Group rings that are fused (share at least one atom, merging also indirect fusion).
       - Accept if any fused group contains at least 4 rings overall with at least 1 five‐membered ring and 3 six‐membered rings.
    3. Identify sulfate ester attachment oxygens:
       - Look for O atoms that are single-bonded to a S atom.
       - The sulfur must be “sulfate‐like” (bonded to at least three oxygens).
    4. For each candidate attachment oxygen, check connectivity:
       - If the oxygen’s neighbor (other than the sulfate S) is in the nucleus, accept.
       - Otherwise, if that neighbor is sp3, non‐aromatic and has any neighbor that belongs to the steroid nucleus, accept.
       
    Args:
        smiles (str): SMILES string of the molecule.
        
    Returns:
        bool: True if the molecule is classified as a steroid sulfate; False otherwise.
        str: Explanation of the classification decision.
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
    
    # ----- Step 1: Identify candidate steroid nucleus -----
    ring_info = mol.GetRingInfo()
    all_rings = ring_info.AtomRings()
    if not all_rings:
        return False, "No rings found; not a steroid nucleus"
    
    # Consider only rings of size 5 or 6.
    rings_5_or_6 = [set(ring) for ring in all_rings if len(ring) in (5, 6)]
    if not rings_5_or_6:
        return False, "No 5- or 6-membered rings found; not a steroid nucleus"
    
    # Group fused rings (rings sharing at least one atom)
    fused_groups = []
    for ring in rings_5_or_6:
        merged = False
        for group in fused_groups:
            if ring & group:  # if they share at least one atom
                group.update(ring)
                merged = True
                break
        if not merged:
            fused_groups.append(set(ring))
    # Merge indirectly fused groups in a second pass.
    merged_any = True
    while merged_any:
        merged_any = False
        new_groups = []
        while fused_groups:
            grp = fused_groups.pop()
            found = False
            for idx, other in enumerate(new_groups):
                if grp & other:
                    new_groups[idx] = other.union(grp)
                    found = True
                    merged_any = True
                    break
            if not found:
                new_groups.append(grp)
        fused_groups = new_groups

    # Next, from all rings, count which fused groups yield a steroid nucleus prediction.
    steroid_candidate = None
    for group in fused_groups:
        # Count rings (from our rings_5_or_6) that are fully contained in this group.
        contained_rings = [ring for ring in rings_5_or_6 if ring.issubset(group)]
        if len(contained_rings) >= 4:
            count_5 = sum(1 for ring in contained_rings if len(ring)==5)
            count_6 = sum(1 for ring in contained_rings if len(ring)==6)
            if count_5 >= 1 and count_6 >= 3:
                steroid_candidate = group
                break
    if steroid_candidate is None:
        return False, ("No fused tetracyclic (steroid) nucleus found "
                       "(requires at least 4 fused rings with at least 1 five-membered and 3 six-membered rings)")
    nucleus_atoms = steroid_candidate  # set of atom indices in the nucleus
    
    # ----- Step 2: Identify sulfate ester attachment oxygens -----
    candidate_oxy_indices = []
    for atom in mol.GetAtoms():
        if atom.GetAtomicNum() != 8:
            continue  # not oxygen
        # Check if bonded to a sulfur
        for nbr in atom.GetNeighbors():
            if nbr.GetAtomicNum() == 16:  # sulfur
                bond = mol.GetBondBetweenAtoms(atom.GetIdx(), nbr.GetIdx())
                # must be a single bond
                if bond.GetBondType() != rdchem.BondType.SINGLE:
                    continue
                # Check that this sulfur is “sulfate-like”
                # Count oxygen neighbors of the sulfur.
                oxy_count = 0
                for snbr in nbr.GetNeighbors():
                    if snbr.GetAtomicNum() == 8:
                        oxy_count += 1
                if oxy_count < 3:
                    continue
                # Make sure our oxygen is not one that is double-bonded to S.
                if bond.GetBondTypeAsDouble() >= 2.0:
                    continue
                candidate_oxy_indices.append(atom.GetIdx())
                break  # no need to check additional neighbors for this oxygen

    if not candidate_oxy_indices:
        return False, "No sulfate ester attachment oxygen found"
    
    # ----- Step 3: Check connectivity from candidate oxygen to the steroid nucleus -----
    attached_found = False
    for oxy_idx in candidate_oxy_indices:
        oxy_atom = mol.GetAtomWithIdx(oxy_idx)
        # Look at neighbors other than the sulfur (usually there is only one such neighbor)
        for nbr in oxy_atom.GetNeighbors():
            if nbr.GetAtomicNum() == 16:
                continue  # skip the sulfate sulfur neighbor
            # Case 1: Direct attachment of the oxygen to an atom in the nucleus.
            if nbr.GetIdx() in nucleus_atoms:
                attached_found = True
                break
            # Case 2: One-linker attachment.
            # The oxygen is attached to a linker atom that is not in the nucleus but that linker must be sp3 and non-aromatic.
            # Then that linker should be attached to at least one nucleus atom.
            if nbr.GetHybridization() != rdchem.HybridizationType.SP3 or nbr.GetIsAromatic():
                continue
            for nn in nbr.GetNeighbors():
                if nn.GetIdx() == oxy_idx:
                    continue
                if nn.GetIdx() in nucleus_atoms:
                    attached_found = True
                    break
            if attached_found:
                break
        if attached_found:
            break

    if not attached_found:
        return False, "Sulfate group not attached (even via one saturated linker) to the steroid nucleus"
    
    return True, "Contains sulfate ester group attached (directly or via one saturated linker) to steroid nucleus (fused tetracyclic system)"

# Example usage (testing with sample SMILES):
if __name__ == "__main__":
    test_smiles = [
        # True positives:
        "[Na+].C[C@]12CC[C@H]3C(=CCc4cc(OS([O-])(=O)=O)ccc34)[C@@H]1CCC2=O",  # equilin sodium sulfate
        "C[C@]12CC[C@@H]3[C@H]([C@H]1CCC2=O)CCC4=C3C=CC(=C4)OS(=O)(=O)O",  # sulfuric acid ester example
        "S(O[C@H]1C[C@@]2([C@@]3([C@]([C@]4([C@](CC3)([C@H]([C@@H](O)[C@H]4O)C=C)C)[H])(CC[C@]2([C@@H](O)[C@H]1O)[H])[H])[H])C)(O)(=O)=O",  # Ptilosteroid A
        # False negatives (should be steroid sulfate):
        "S(OCC(=O)[C@@H]1[C@@]2([C@]([C@]3([C@@]([C@@]4(C(=CC3)C[C@@H](O)CC4)C)(CC2)[H])[H])(CC1)[H])C)(O)(=O)=O",  # 21-hydroxypregnenolone monosulfate
        # Molecules that are NOT steroid sulfates (should be rejected):
        "O[S](=O)(=O)O",  # pure sulfate group
        "CCCC",         # non-cyclic aliphatic
    ]
    for smi in test_smiles:
        result, reason = is_steroid_sulfate(smi)
        print("SMILES:", smi)
        print("Result:", result, "|", reason)
        print("-"*80)


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:16158',
                          'name': 'steroid sulfate',
                          'definition': 'A sulfuric ester obtained by the '
                                        'formal condensation of a hydroxy '
                                        'group of any steroid with sulfuric '
                                        'acid.',
                          'parents': [   'CHEBI:25704',
                                         'CHEBI:26819',
                                         'CHEBI:47880'],
                          'xrefs': ['KEGG:C02590'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 148,
                           'log_lines_of_code': 4.997212273764115,
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
                                                 2,
                                                 3,
                                                 4,
                                                 4,
                                                 4,
                                                 2,
                                                 3,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 3,
                                                 3,
                                                 4,
                                                 5,
                                                 5,
                                                 5,
                                                 5,
                                                 3,
                                                 4,
                                                 2,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 3,
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
                                                 1,
                                                 2,
                                                 3,
                                                 2,
                                                 2,
                                                 3,
                                                 4,
                                                 4,
                                                 4,
                                                 5,
                                                 4,
                                                 4,
                                                 4,
                                                 4,
                                                 5,
                                                 6,
                                                 4,
                                                 5,
                                                 4,
                                                 4,
                                                 5,
                                                 4,
                                                 4,
                                                 0,
                                                 1,
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 4,
                                                 3,
                                                 3,
                                                 4,
                                                 4,
                                                 3,
                                                 3,
                                                 3,
                                                 3,
                                                 4,
                                                 3,
                                                 4,
                                                 5,
                                                 4,
                                                 5,
                                                 5,
                                                 3,
                                                 4,
                                                 2,
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
                                                 2,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 2,
                                                 2],
                           'max_indent': 6,
                           'imports': [   'from rdkit import Chem',
                                          'from rdkit.Chem import rdchem'],
                           'imports_count': 2,
                           'methods_called': [   'union',
                                                 'GetBondType',
                                                 'GetHybridization',
                                                 'GetAtoms',
                                                 'issubset',
                                                 'update',
                                                 'MolFromSmiles',
                                                 'GetNeighbors',
                                                 'GetIsAromatic',
                                                 'GetBondBetweenAtoms',
                                                 'append',
                                                 'GetRingInfo',
                                                 'GetBondTypeAsDouble',
                                                 'GetIdx',
                                                 'GetAtomWithIdx',
                                                 'GetAtomicNum',
                                                 'AtomRings',
                                                 'pop'],
                           'methods_called_count': 18,
                           'smarts_strings': [],
                           'smarts_strings_count': 0,
                           'defs': ['is_steroid_sulfate(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "No rings found; not a '
                                          'steroid nucleus"',
                                          'False, "No 5- or 6-membered rings '
                                          'found; not a steroid nucleus"',
                                          'False, ("No fused tetracyclic '
                                          '(steroid) nucleus found "',
                                          'False, "No sulfate ester attachment '
                                          'oxygen found"',
                                          'False, "Sulfate group not attached '
                                          '(even via one saturated linker) to '
                                          'the steroid nucleus"',
                                          'True, "Contains sulfate ester group '
                                          'attached (directly or via one '
                                          'saturated linker) to steroid '
                                          'nucleus (fused tetracyclic '
                                          'system)"'],
                           'returns_count': 7,
                           'complexity': 7.399442454752823},
    'message': '\n'
               'Attempt failed: F1 score of 0.5576923076923077 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: '
               '[Na+].C[C@]12CC[C@H]3C(=CCc4cc(OS([O-])(=O)=O)ccc34)[C@@H]1CCC2=O '
               'NAME: equilin sodium sulfate REASON: CORRECT Contains sulfate '
               'ester group attached (directly or via a short linker) to '
               'steroid nucleus (fused tetracyclic system)\n'
               ' * SMILES: '
               'C[C@]12CC[C@@H]3[C@H]([C@H]1CCC2=O)CCC4=C3C=CC(=C4)OS(=O)(=O)O '
               'NAME: sulfuric acid '
               '[(8R,9R,13S,14R)-13-methyl-17-oxo-7,8,9,11,12,14,15,16-octahydro-6H-cyclopenta[a]phenanthren-3-yl] '
               'ester REASON: CORRECT Contains sulfate ester group attached '
               '(directly or via a short linker) to steroid nucleus (fused '
               'tetracyclic system)\n'
               ' * SMILES: '
               'S(O[C@H]1C[C@@]2([C@@]3([C@]([C@]4([C@](CC3)([C@H]([C@@H](O)[C@H]4O)C=C)C)[H])(CC[C@]2([C@@H](O)[C@H]1O)[H])[H])[H])C)(O)(=O)=O '
               'NAME: Ptilosteroid A REASON: CORRECT Contains sulfate ester '
               'group attached (directly or via a short linker) to steroid '
               'nucleus (fused tetracyclic system)\n'
               ' * SMILES: '
               'S(O[C@H]1C[C@@]2([C@@](C3C(C4[C@](CC3)(C(=O)CC4)C)CC2)(CC1)C)[H])(O)(=O)=O '
               'NAME: Etiocholanolone sulfate REASON: CORRECT Contains sulfate '
               'ester group attached (directly or via a short linker) to '
               'steroid nucleus (fused tetracyclic system)\n'
               ' * SMILES: '
               '[H][C@@]1(CC[C@]2([H])[C@]1(C)CC[C@]1([H])[C@@]34CC[C@@H](C[C@]3(O)[C@H](O)C[C@@]21OC4)OS(O)(=O)=O)[C@H](C)CCCC(C)C '
               'NAME: eurysterol A sulfonic acid REASON: CORRECT Contains '
               'sulfate ester group attached (directly or via a short linker) '
               'to steroid nucleus (fused tetracyclic system)\n'
               ' * SMILES: '
               'C[C@@H]([C@H]1CC[C@H]2[C@@H]3C[C@H]4O[C@]44[C@@H](O)[C@H](CC(=O)[C@]4(C)[C@H]3CC[C@]12C)OS(O)(=O)=O)[C@H]1CC(C)=C(CO)C(=O)O1 '
               'NAME: 2,3-dihydro-3beta-O-sulfate withaferin A REASON: CORRECT '
               'Contains sulfate ester group attached (directly or via a short '
               'linker) to steroid nucleus (fused tetracyclic system)\n'
               ' * SMILES: '
               '[Na+].[H][C@]12CC[C@]3(C)C(=O)CC[C@@]3([H])[C@]1([H])CCc1cc(OS([O-])(=O)=O)ccc21 '
               'NAME: estrone sodium sulfate REASON: CORRECT Contains sulfate '
               'ester group attached (directly or via a short linker) to '
               'steroid nucleus (fused tetracyclic system)\n'
               ' * SMILES: '
               'S(OC1=C(O)C2=C(C3C(C4[C@@](CC3)(C(=O)CC4)C)CC2)C=C1)(O)(=O)=O '
               'NAME: 4-Hydroxyestrone sulfate REASON: CORRECT Contains '
               'sulfate ester group attached (directly or via a short linker) '
               'to steroid nucleus (fused tetracyclic system)\n'
               ' * SMILES: '
               'S(O[C@H]1C[C@@]2([C@@]([C@@]3([C@]([C@]4([C@](CC3)([C@H](CC4)C(=O)C)C)[H])(CC2)[H])[H])(CC1)C)[H])(O)(=O)=O '
               'NAME: 3alpha-Hydroxy-5beta-pregnane-20-one sulfate REASON: '
               'CORRECT Contains sulfate ester group attached (directly or via '
               'a short linker) to steroid nucleus (fused tetracyclic system)\n'
               ' * SMILES: '
               'C1[C@@]2([C@@]([C@@]3([C@](C[C@@H](OS(O)(=O)=O)CC3)(C1)[H])C)(CC[C@@]4(C(CC[C@@]24[H])=O)C)[H])[H] '
               'NAME: epiandrosterone sulfate REASON: CORRECT Contains sulfate '
               'ester group attached (directly or via a short linker) to '
               'steroid nucleus (fused tetracyclic system)\n'
               ' * SMILES: '
               'C1[C@@]2([C@]3(CC[C@]4([C@]([C@@]3(CC[C@]2(C[C@H](C1)OS(O)(=O)=O)[H])[H])(CC[C@]4([H])[C@@H](OS(O)(=O)=O)C)[H])C)[H])C '
               'NAME: 5alpha-pregnane-3beta,20alpha-diol disulfate REASON: '
               'CORRECT Contains sulfate ester group attached (directly or via '
               'a short linker) to steroid nucleus (fused tetracyclic system)\n'
               ' * SMILES: '
               'C1[C@]2([C@]3([C@@](C4=C(C=C(OS(O)(=O)=O)C(=C4)O)CC3)(CC[C@@]2([C@@H](O)C1)C)[H])[H])[H] '
               'NAME: 2-hydroxy-17beta-estradiol 3-sulfate REASON: CORRECT '
               'Contains sulfate ester group attached (directly or via a short '
               'linker) to steroid nucleus (fused tetracyclic system)\n'
               ' * SMILES: '
               'C1[C@@]2([C@]3(C[C@@H]([C@]4([C@]([C@@]3(CC[C@@]2(C[C@@H](C1)OS(O)(=O)=O)[H])[H])(CC[C@@]4([C@@H](CCC(NCC(O)=O)=O)C)[H])[H])C)O)[H])C '
               'NAME: glycodeoxycholic acid 3-sulfate REASON: CORRECT Contains '
               'sulfate ester group attached (directly or via a short linker) '
               'to steroid nucleus (fused tetracyclic system)\n'
               ' * SMILES: '
               'C1[C@@]2([C@@]([C@@]3(C(C[C@@H](OS(O)(=O)=O)CC3)=C1)C)(CC[C@]4([C@]2(C[C@H](C4=O)O)[H])C)[H])[H] '
               'NAME: 16alpha-hydroxydehydroepiandrosterone 3-sulfate REASON: '
               'CORRECT Contains sulfate ester group attached (directly or via '
               'a short linker) to steroid nucleus (fused tetracyclic system)\n'
               ' * SMILES: '
               'S(OC1=CC2=C(C3C(C4[C@]([C@H](O)CC4)(CC3)C)CC2)C=C1)(O)(=O)=O '
               'NAME: beta-Estradiol 3-sulfate REASON: CORRECT Contains '
               'sulfate ester group attached (directly or via a short linker) '
               'to steroid nucleus (fused tetracyclic system)\n'
               ' * SMILES: '
               'C1[C@@]2([C@]3(CC[C@]4(C)[C@](CC[C@]4([C@@]3(CC=C2C[C@H](C1)OS(O)(=O)=O)[H])[H])(C(C)=O)O)[H])C '
               'NAME: 17alpha-hydroxypregnenolone 3-sulfate REASON: CORRECT '
               'Contains sulfate ester group attached (directly or via a short '
               'linker) to steroid nucleus (fused tetracyclic system)\n'
               ' * SMILES: OS(=O)(=O)OC1CCC2C(CCC3C4CCCC4CCC23)C1 NAME: Steryl '
               'sulfate REASON: CORRECT Contains sulfate ester group attached '
               '(directly or via a short linker) to steroid nucleus (fused '
               'tetracyclic system)\n'
               ' * SMILES: '
               'S(O[C@H]1C[C@@]2([C@@]([C@@]3([C@]([C@]4([C@](CC3)(C(=O)CC4)C)[H])(CC2)[H])[H])(CC1)C)[H])(O)(=O)=O '
               'NAME: 5beta-Androstan-3alpha-ol-17-one sulfate REASON: CORRECT '
               'Contains sulfate ester group attached (directly or via a short '
               'linker) to steroid nucleus (fused tetracyclic system)\n'
               ' * SMILES: '
               'C1[C@@]2([C@@]([C@@]3([C@](C[C@H](O)CC3)(C1)[H])C)(CC[C@@]4([C@H](CC[C@@]24[H])OS(O)(=O)=O)C)[H])[H] '
               'NAME: (3alpha,5alpha,17beta)-3-hydroxyandrostan-17-yl sulfate '
               'REASON: CORRECT Contains sulfate ester group attached '
               '(directly or via a short linker) to steroid nucleus (fused '
               'tetracyclic system)\n'
               ' * SMILES: '
               '[C@@H]1(OS(O)(=O)=O)[C@]2(CC[C@]3([C@]([C@@]2(CC1)[H])(CC[C@@]4([C@@]3(CC[C@@H](C4)O)C)[H])[H])[H])C '
               'NAME: (3beta,5alpha,17beta)-3-hydroxyandrostan-17-yl sulfate '
               'REASON: CORRECT Contains sulfate ester group attached '
               '(directly or via a short linker) to steroid nucleus (fused '
               'tetracyclic system)\n'
               ' * SMILES: '
               'C1[C@@]2([C@@]([C@@]3(C(=C[C@@H](OS(O)(=O)=O)CC3)C1)C)(CC[C@@]4([C@H](CC[C@@]24[H])OS(O)(=O)=O)C)[H])[H] '
               'NAME: 4-androstene-3beta,17beta-diol disulfate REASON: CORRECT '
               'Contains sulfate ester group attached (directly or via a short '
               'linker) to steroid nucleus (fused tetracyclic system)\n'
               ' * SMILES: '
               'C1[C@@]2([C@@]([C@@]3(C(C[C@@H](OS(O)(=O)=O)CC3)=C1)C)(CC[C@]4([C@]2(CCC4=O)[H])C)[H])[H] '
               'NAME: dehydroepiandrosterone sulfate REASON: CORRECT Contains '
               'sulfate ester group attached (directly or via a short linker) '
               'to steroid nucleus (fused tetracyclic system)\n'
               ' * SMILES: '
               'C1C2=CC(CC[C@@]2([C@]3(CC[C@]4([C@]([C@@]3(C1)[H])(CC[C@H]4OS(=O)([O-])=O)[H])C)[H])C)=O '
               'NAME: epitestosterone sulfate(1-) REASON: CORRECT Contains '
               'sulfate ester group attached (directly or via a short linker) '
               'to steroid nucleus (fused tetracyclic system)\n'
               ' * SMILES: '
               'S(O[C@@H]1CC=2[C@@]([C@@]3([C@]([C@]4([C@](CC3)(C(=CC4)C5=C[N+]([O-])=CC=C5)C)[H])(CC2)[H])[H])(CC1)C)(O)(=O)=O '
               'NAME: N-Oxide abiraterone sulfate REASON: CORRECT Contains '
               'sulfate ester group attached (directly or via a short linker) '
               'to steroid nucleus (fused tetracyclic system)\n'
               ' * SMILES: '
               'S(OC1CC=2[C@@]([C@@]3([C@]([C@]4([C@](CC3)(C(=CC4)C=5C=CC=NC5)C)[H])(CC2)[H])[H])(CC1)C)(O)(=O)=O '
               'NAME: Abiraterone sulfate REASON: CORRECT Contains sulfate '
               'ester group attached (directly or via a short linker) to '
               'steroid nucleus (fused tetracyclic system)\n'
               'False positives: SMILES: '
               'S(O[C@H]1[C@@H](O)[C@@]2([C@@]([C@@]3(C(C4[C@@]([C@](CC4)([C@@H](CCCC(C)C)COS(O)(=O)=O)[H])([C@H](O)[C@@H]3O)C)CC2)[H])(CC1)C)[H])(O)(=O)=O '
               'NAME: '
               '5beta-cholestan-3alpha,4alpha,11beta,12beta,21-pentol-3,21-disulphate '
               'REASON: WRONGLY CLASSIFIED Contains sulfate ester group '
               'attached (directly or via a short linker) to steroid nucleus '
               '(fused tetracyclic system)\n'
               ' * SMILES: '
               'O(S([O-])(=O)=O)[C@@H]1CC=2[C@]([C@]3(CC[C@]4([C@]([C@@]3(CC2)[H])(CC[C@@]4([C@H](C)CCCC(C)C)[H])[H])C)[H])(C)CC1 '
               'NAME: cholesterol sulfate(1-) REASON: WRONGLY CLASSIFIED '
               'Contains sulfate ester group attached (directly or via a short '
               'linker) to steroid nucleus (fused tetracyclic system)\n'
               ' * SMILES: '
               'C1[C@]2([C@]3([C@@](C4=C(C=C(OS([O-])(=O)=O)C(=C4)O)CC3)(CC[C@@]2([C@@H](O)C1)C)[H])[H])[H] '
               'NAME: 2-hydroxy-17beta-estradiol 3-sulfate(1-) REASON: WRONGLY '
               'CLASSIFIED Contains sulfate ester group attached (directly or '
               'via a short linker) to steroid nucleus (fused tetracyclic '
               'system)\n'
               ' * SMILES: '
               'C1[C@@]2([C@]3(C[C@@H]([C@]4([C@]([C@@]3(CC[C@@]2(C[C@@H](C1)OS(=O)(=O)[O-])[H])[H])(CC[C@@]4([C@@H](CCC(NCC([O-])=O)=O)C)[H])[H])C)O)[H])C '
               'NAME: 3alpha-sulfoglycodeoxycholate(2-) REASON: WRONGLY '
               'CLASSIFIED Contains sulfate ester group attached (directly or '
               'via a short linker) to steroid nucleus (fused tetracyclic '
               'system)\n'
               ' * SMILES: '
               'S(O[C@H]1C[C@@]2([C@@]([C@@]3([C@]([C@]4([C@@]([C@](CC4)([C@@H](CCC(=O)NCCS(O)(=O)=O)C)[H])([C@@H](O)C3)C)[H])([C@H](O)C2)[H])[H])(CC1)C)[H])(O)(=O)=O '
               'NAME: Taurocholic acid 3-sulfate REASON: WRONGLY CLASSIFIED '
               'Contains sulfate ester group attached (directly or via a short '
               'linker) to steroid nucleus (fused tetracyclic system)\n'
               ' * SMILES: '
               'C1[C@H](C[C@@]2([C@](C1)([C@@]3([C@@]([C@@H]([C@H]2O)OS([O-])(=O)=O)([C@@]4([H])[C@@](CC3)(C)[C@](CC4)([C@@H](CCC(NCCS([O-])(=O)=O)=O)C)[H])[H])[H])C)[H])O '
               'NAME: tauro-alpha-muricholate 7-sulfate(2-) REASON: WRONGLY '
               'CLASSIFIED Contains sulfate ester group attached (directly or '
               'via a short linker) to steroid nucleus (fused tetracyclic '
               'system)\n'
               ' * SMILES: '
               '[H+].[H+].CC1Nc2c(cc3c(Oc4c(c5=NC(C)C(C)(C)c5cc4=C3c3ccc(cc3)C(=O)ON3C(=O)CCC3=O)S([O-])(=O)=O)c2S([O-])(=O)=O)C1(C)C '
               'NAME: Alexa Fluor 532 REASON: WRONGLY CLASSIFIED Contains '
               'sulfate ester group attached (directly or via a short linker) '
               'to steroid nucleus (fused tetracyclic system)\n'
               ' * SMILES: '
               'CC1(C)c2cc(CC(=O)ON3C(=O)CCC3=O)ccc2N2CCC3OC4CC[N+]5=C(C4=CC3=C12)C(C)(C)c1cc(ccc51)S([O-])(=O)=O '
               'NAME: Cy3B dye NHS ester REASON: WRONGLY CLASSIFIED Contains '
               'sulfate ester group attached (directly or via a short linker) '
               'to steroid nucleus (fused tetracyclic system)\n'
               ' * SMILES: '
               'S1C(=O)C=2C=CC(=C3C2C1=C4C(=C3)C=C[C@H]([C@@H]4OS(=O)(=O)[O-])O)N5[C@H]6C7=C(C=CC=C7)[C@H]8[C@@H](C5)[C@@H]6C(=CC8=O)C '
               'NAME: sulfosungeidine E REASON: WRONGLY CLASSIFIED Contains '
               'sulfate ester group attached (directly or via a short linker) '
               'to steroid nucleus (fused tetracyclic system)\n'
               ' * SMILES: '
               'S(OC1=C2OC3C45C(C(N(CC4)C)CC(=C52)C=C1)CCC3=O)(O)(=O)=O NAME: '
               'Hydromorphone-3-sulphate REASON: WRONGLY CLASSIFIED Contains '
               'sulfate ester group attached (directly or via a short linker) '
               'to steroid nucleus (fused tetracyclic system)\n'
               ' * SMILES: '
               'C12=[N+]3C(=NC=4N5C(N=C6[N+]7=C(N=C8N(C(=N1)C9=CC=CC=C89)[Cu-2]357)C%10=C(C=CC=C6%10)S([O-])(=O)=O)=C%11C=CC=CC4%11)C%12=C(C=CC=C2%12)S([O-])(=O)=O.N(C(NC=1C=CC=CC1C)=[NH2+])C=2C(=CC=CC2)C.N(C(NC=1C=CC=CC1C)=[NH2+])C=2C(=CC=CC2)C '
               'NAME: Luxol fast blue MBS REASON: WRONGLY CLASSIFIED Contains '
               'sulfate ester group attached (directly or via a short linker) '
               'to steroid nucleus (fused tetracyclic system)\n'
               ' * SMILES: '
               '[C@@]12([C@]3([C@](CC[C@@]1([C@@]4(C(C[C@H](CC4)OS([O-])(=O)=O)=CC2)C)[H])([C@](CC3)([C@H](C)CC[C@@H](C(C)C)OS([O-])(=O)=O)[H])C)[H])[H] '
               'NAME: (24S)-hydroxycholesterol 3,24-disulfate(2-) REASON: '
               'WRONGLY CLASSIFIED Contains sulfate ester group attached '
               '(directly or via a short linker) to steroid nucleus (fused '
               'tetracyclic system)\n'
               ' * SMILES: '
               'C1[C@@]2([C@]3(CC[C@]4([C@]([C@@]3(CC[C@@]2(C[C@@H](C1)OS([O-])(=O)=O)[H])[H])(CC[C@@]4([C@H](C)CCC([O-])=O)[H])[H])C)[H])C '
               'NAME: lithocholate sulfate(2-) REASON: WRONGLY CLASSIFIED '
               'Contains sulfate ester group attached (directly or via a short '
               'linker) to steroid nucleus (fused tetracyclic system)\n'
               ' * SMILES: '
               'C1C[C@@H](CC2C[C@H](O)[C@]3([C@@]4(CC[C@H]([C@@H](CCC(=O)O)C)[C@@]4(C)CC[C@@]3([C@@]12C)[H])[H])[H])OS(=O)(=O)O '
               'NAME: Ursodeoxycholic acid 3-sulfate REASON: WRONGLY '
               'CLASSIFIED Contains sulfate ester group attached (directly or '
               'via a short linker) to steroid nucleus (fused tetracyclic '
               'system)\n'
               ' * SMILES: '
               'S(O[C@@H]1[C@]2([C@]([C@]3([C@@]([C@@]4([C@](C[C@H]3O)(C[C@H](O)CC4)[H])C)(C1)[H])[H])(CC[C@@]2([C@@H](CCC(=O)NCC(O)=O)C)[H])[H])C)(O)(=O)=O '
               'NAME: '
               'N-[(3a,5b,7a,12a)-3,7-dihydroxy-24-oxo-12-(sulfoxy)cholan-24-yl]-Glycine '
               'REASON: WRONGLY CLASSIFIED Contains sulfate ester group '
               'attached (directly or via a short linker) to steroid nucleus '
               '(fused tetracyclic system)\n'
               ' * SMILES: '
               '[H][C@]12CC[C@@]3([H])[C@]4([H])CC[C@]([H])([C@H](C)CCC(=O)NCCS([O-])(=O)=O)[C@@]4(C)CC[C@]3([H])[C@@]1(C)CC[C@H](C2)OS([O-])(=O)=O '
               'NAME: taurolithocholic acid sulfate(2-) REASON: WRONGLY '
               'CLASSIFIED Contains sulfate ester group attached (directly or '
               'via a short linker) to steroid nucleus (fused tetracyclic '
               'system)\n'
               ' * SMILES: '
               'O([C@H]1[C@@H]([C@H]([C@@H]([C@H](O1)C([O-])=O)O)O)O)C2=CC3=C([C@@]4([C@]([C@]5([C@@]([C@@H](OS([O-])(=O)=O)CC5)(CC4)C)[H])(CC3)[H])[H])C=C2 '
               'NAME: 17beta-estradiol 3-O-(beta-D-glucuronide) 17-sulfate '
               '(2-) REASON: WRONGLY CLASSIFIED Contains sulfate ester group '
               'attached (directly or via a short linker) to steroid nucleus '
               '(fused tetracyclic system)\n'
               ' * SMILES: '
               'C1[C@@]2([C@]3(C[C@@H]([C@]4([C@]([C@@]3([C@@H](C[C@@]2(C[C@@H](C1)O)[H])OS([O-])(=O)=O)[H])(CC[C@]4([H])[C@@H](CCC(NCCS([O-])(=O)=O)=O)C)[H])C)O)[H])C '
               'NAME: taurocholate 7-sulfate(2-) REASON: WRONGLY CLASSIFIED '
               'Contains sulfate ester group attached (directly or via a short '
               'linker) to steroid nucleus (fused tetracyclic system)\n'
               ' * SMILES: '
               'C1[C@@]2([C@]3(C[C@@H]([C@]4([C@]([C@@]3([C@@H](C[C@@]2(C[C@@H](C1)O)[H])OS([O-])(=O)=O)[H])(CC[C@]4([H])[C@@H](CCC(NCC([O-])=O)=O)C)[H])C)O)[H])C '
               'NAME: glycocholate 7-sulfate(2-) REASON: WRONGLY CLASSIFIED '
               'Contains sulfate ester group attached (directly or via a short '
               'linker) to steroid nucleus (fused tetracyclic system)\n'
               ' * SMILES: '
               'S(=O)(=O)(O[C@@H]1C([C@H]2[C@](C=3C([C@H]4[C@]([C@@H]([C@@H](CCC(=C)C(C)C)C)CC4)(C)[C@H](C3)OC)=CC2)(C)C[C@H]1O)(C)C)O '
               'NAME: A-108836 REASON: WRONGLY CLASSIFIED Contains sulfate '
               'ester group attached (directly or via a short linker) to '
               'steroid nucleus (fused tetracyclic system)\n'
               ' * SMILES: '
               'C1[C@@]2([C@]3(C[C@@H]([C@]4([C@]([C@@]3([C@@H](C[C@@]2(C[C@@H](C1)O)[H])OS([O-])(=O)=O)[H])(CC[C@]4([H])[C@@H](CCC([O-])=O)C)[H])C)O)[H])C '
               'NAME: cholate 7-sulfate(2-) REASON: WRONGLY CLASSIFIED '
               'Contains sulfate ester group attached (directly or via a short '
               'linker) to steroid nucleus (fused tetracyclic system)\n'
               ' * SMILES: '
               '[C@@H]1(CC[C@@]2([C@]3(CC[C@@]4([C@H](CC[C@]4([C@@]3(CC=C2C1)[H])[H])[C@@H](CCC(=O)[O-])C)C)[H])C)OS(=O)(=O)[O-] '
               'NAME: 3beta-sulfo-5-cholenoate(2-) REASON: WRONGLY CLASSIFIED '
               'Contains sulfate ester group attached (directly or via a short '
               'linker) to steroid nucleus (fused tetracyclic system)\n'
               ' * SMILES: '
               '[C@@]12([C@]3([C@](CC[C@@]1([C@@]4(C(C[C@H](CC4)OS([O-])(=O)=O)=CC2)C)[H])([C@](CC3)([C@H](C)CC[C@@H](C(C)C)O)[H])C)[H])[H] '
               'NAME: (24S)-hydroxycholesterol 3-sulfate(1-) REASON: WRONGLY '
               'CLASSIFIED Contains sulfate ester group attached (directly or '
               'via a short linker) to steroid nucleus (fused tetracyclic '
               'system)\n'
               ' * SMILES: '
               '[H][C@@]12CCC3C[C@H](OS([O-])(=O)=O)[C@H](C[C@]3(C)[C@@]1([H])CC[C@]1(C)[C@@]([H])([C@H](C)C(OC(=O)CCC)C(OC(=O)CCC)C(CC)C(C)C)[C@@H](O)[C@H](OC(C)=O)[C@@]21[H])OS([O-])(=O)=O '
               'NAME: clathsterol(2-) REASON: WRONGLY CLASSIFIED Contains '
               'sulfate ester group attached (directly or via a short linker) '
               'to steroid nucleus (fused tetracyclic system)\n'
               ' * SMILES: '
               '[H][C@@]1(CC[C@@]2([H])[C@]3([H])C[C@H](OS([O-])(=O)=O)[C@@]4([H])C[C@H](OS([O-])(=O)=O)[C@H](C[C@]4(C)[C@@]3([H])CC[C@]12C)OS([O-])(=O)=O)[C@H](C)CCC(C)C(C)(C)CC '
               'NAME: halistanol sulfate F(3-) REASON: WRONGLY CLASSIFIED '
               'Contains sulfate ester group attached (directly or via a short '
               'linker) to steroid nucleus (fused tetracyclic system)\n'
               'False negatives: SMILES: '
               'S(OCC(=O)[C@@H]1[C@@]2([C@]([C@]3([C@@]([C@@]4(C(=CC3)C[C@@H](O)CC4)C)(CC2)[H])[H])(CC1)[H])C)(O)(=O)=O '
               'NAME: 21-hydroxypregnenolone monosulfate REASON: MISSED '
               'Sulfate group not attached (even via one saturated linker) to '
               'the steroid nucleus\n'
               ' * SMILES: '
               '[H][C@@]12C[C@H](O)CC[C@]1(C)C1C[C@H](O)[C@]3(C)[C@]([H])(CC[C@@]3([H])[C@]1([H])[C@H](O)C2)[C@H](C)CC[C@@H](O)C(CO)COS(O)(=O)=O '
               'NAME: 5beta-scymnol sulfate REASON: MISSED Sulfate group not '
               'attached (even via one saturated linker) to the steroid '
               'nucleus\n'
               ' * SMILES: '
               '[H][C@@]12C[C@H](O)CC[C@]1(C)[C@@]1([H])C[C@H](O)[C@]3(C)[C@]([H])(CC[C@@]3([H])[C@]1([H])[C@H](O)C2)[C@H](C)CCCC(CO)COS(O)(=O)=O '
               'NAME: 5beta-cyprinol sulfate REASON: MISSED Sulfate group not '
               'attached (even via one saturated linker) to the steroid '
               'nucleus\n'
               ' * SMILES: '
               '[H][C@@]12CCC3=CC(=O)CC[C@]3(C)[C@@]1([H])[C@@H](O)C[C@@]1(C)[C@@]2([H])CC[C@]1(O)C(=O)COS(O)(=O)=O '
               'NAME: cortisol 21-sulfate REASON: MISSED Sulfate group not '
               'attached (even via one saturated linker) to the steroid '
               'nucleus\n'
               ' * SMILES: '
               '[C@@]12([C@]3([C@](CC[C@@]1([C@@]4(C(C[C@H](CC4)O)=CC2)C)[H])([C@](CC3)([C@H](C)CC[C@@H](C(C)C)OS(O)(=O)=O)[H])C)[H])[H] '
               'NAME: (24S)-hydroxycholesterol 24-sulfate REASON: MISSED '
               'Sulfate group not attached (even via one saturated linker) to '
               'the steroid nucleus\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'O=C1OC[C@@H]2O[C@@H](O[C@@H]3[C@@H](OC(=O)CCCCCCCCCCCCCCC)[C@H](C=CCCCC1)[C@H](CCCCC)[C@@H](C3)O)[C@H](O)[C@H]([C@@H]2O)O',
                                     'name': 'Mucorolactone',
                                     'reason': 'No fused tetracyclic (steroid) '
                                               'nucleus found (requires at '
                                               'least 4 fused rings with at '
                                               'least 1 five-membered and 3 '
                                               'six-membered rings)'},
                                 {   'smiles': 'C[C@@H]1CN[C@H](COC2=C(C=CC(=C2)NC(=O)C3=NC4=CC=CC=C4S3)C(=O)N(C[C@H]1OC)C)C',
                                     'name': 'N-[(5S,6R,9S)-5-methoxy-3,6,9-trimethyl-2-oxo-11-oxa-3,8-diazabicyclo[10.4.0]hexadeca-1(12),13,15-trien-14-yl]-1,3-benzothiazole-2-carboxamide',
                                     'reason': 'No fused tetracyclic (steroid) '
                                               'nucleus found (requires at '
                                               'least 4 fused rings with at '
                                               'least 1 five-membered and 3 '
                                               'six-membered rings)'},
                                 {   'smiles': 'COC1=CC=CC(=C1)C2=CC=C(C=C2)[C@@H]3[C@@H]4CN(CC(=O)N4[C@@H]3CO)C(=O)C5=CN=CC=C5',
                                     'name': '(6R,7R,8S)-8-(hydroxymethyl)-7-[4-(3-methoxyphenyl)phenyl]-4-[oxo(3-pyridinyl)methyl]-1,4-diazabicyclo[4.2.0]octan-2-one',
                                     'reason': 'No fused tetracyclic (steroid) '
                                               'nucleus found (requires at '
                                               'least 4 fused rings with at '
                                               'least 1 five-membered and 3 '
                                               'six-membered rings)'},
                                 {   'smiles': 'C(C(/C=C/C=C/C=C/[C@H](CCCC(O)=O)O)=O)/C=C\\CCCCC',
                                     'name': '12-oxo-6-trans-leukotriene B4',
                                     'reason': 'No rings found; not a steroid '
                                               'nucleus'},
                                 {   'smiles': 'O=C1OC(=C(C#C[C@H](COC(=O)C)C)CO)C=C1',
                                     'name': "5'-O-acetylaporpinone A",
                                     'reason': 'No fused tetracyclic (steroid) '
                                               'nucleus found (requires at '
                                               'least 4 fused rings with at '
                                               'least 1 five-membered and 3 '
                                               'six-membered rings)'},
                                 {   'smiles': 'O=C(N1[C@@H](CCC1)C(=O)N[C@@H](CCC(=O)N)C(O)=O)[C@@H](N)[C@H](CC)C',
                                     'name': 'Ile-Pro-Gln',
                                     'reason': 'No fused tetracyclic (steroid) '
                                               'nucleus found (requires at '
                                               'least 4 fused rings with at '
                                               'least 1 five-membered and 3 '
                                               'six-membered rings)'},
                                 {   'smiles': 'O[C@@H]1C=CC=C(CCC(O)=O)[C@@H]1O',
                                     'name': '3-[(5R,6S)-5,6-dihydroxycyclohexa-1,3-dienyl]propanoic '
                                             'acid',
                                     'reason': 'No fused tetracyclic (steroid) '
                                               'nucleus found (requires at '
                                               'least 4 fused rings with at '
                                               'least 1 five-membered and 3 '
                                               'six-membered rings)'},
                                 {   'smiles': 'O=C(OC)/C=C/C(C)(C)C',
                                     'name': '4,4-Dimethyl-pentenoic acid '
                                             'methyl ester',
                                     'reason': 'No rings found; not a steroid '
                                               'nucleus'},
                                 {   'smiles': 'CCCCOc1ccc(OCCCN2CCOCC2)cc1',
                                     'name': 'pramocaine',
                                     'reason': 'No fused tetracyclic (steroid) '
                                               'nucleus found (requires at '
                                               'least 4 fused rings with at '
                                               'least 1 five-membered and 3 '
                                               'six-membered rings)'},
                                 {   'smiles': 'OC[C@@H](O)C(=O)[C@H](O)[C@H](O)COP(O)(O)=O',
                                     'name': 'D-arabino-hex-3-ulose '
                                             '6-phosphate',
                                     'reason': 'No rings found; not a steroid '
                                               'nucleus'}],
    'sample_false_negatives': [   {   'smiles': 'S(OCC(=O)[C@@H]1[C@@]2([C@]([C@]3([C@@]([C@@]4(C(=CC3)C[C@@H](O)CC4)C)(CC2)[H])[H])(CC1)[H])C)(O)(=O)=O',
                                      'name': '21-hydroxypregnenolone '
                                              'monosulfate',
                                      'reason': 'Sulfate group not attached '
                                                '(even via one saturated '
                                                'linker) to the steroid '
                                                'nucleus'},
                                  {   'smiles': '[H][C@@]12C[C@H](O)CC[C@]1(C)C1C[C@H](O)[C@]3(C)[C@]([H])(CC[C@@]3([H])[C@]1([H])[C@H](O)C2)[C@H](C)CC[C@@H](O)C(CO)COS(O)(=O)=O',
                                      'name': '5beta-scymnol sulfate',
                                      'reason': 'Sulfate group not attached '
                                                '(even via one saturated '
                                                'linker) to the steroid '
                                                'nucleus'},
                                  {   'smiles': '[H][C@@]12C[C@H](O)CC[C@]1(C)[C@@]1([H])C[C@H](O)[C@]3(C)[C@]([H])(CC[C@@]3([H])[C@]1([H])[C@H](O)C2)[C@H](C)CCCC(CO)COS(O)(=O)=O',
                                      'name': '5beta-cyprinol sulfate',
                                      'reason': 'Sulfate group not attached '
                                                '(even via one saturated '
                                                'linker) to the steroid '
                                                'nucleus'},
                                  {   'smiles': '[H][C@@]12CCC3=CC(=O)CC[C@]3(C)[C@@]1([H])[C@@H](O)C[C@@]1(C)[C@@]2([H])CC[C@]1(O)C(=O)COS(O)(=O)=O',
                                      'name': 'cortisol 21-sulfate',
                                      'reason': 'Sulfate group not attached '
                                                '(even via one saturated '
                                                'linker) to the steroid '
                                                'nucleus'},
                                  {   'smiles': '[C@@]12([C@]3([C@](CC[C@@]1([C@@]4(C(C[C@H](CC4)O)=CC2)C)[H])([C@](CC3)([C@H](C)CC[C@@H](C(C)C)OS(O)(=O)=O)[H])C)[H])[H]',
                                      'name': '(24S)-hydroxycholesterol '
                                              '24-sulfate',
                                      'reason': 'Sulfate group not attached '
                                                '(even via one saturated '
                                                'linker) to the steroid '
                                                'nucleus'}],
    'attempt': 4,
    'reasoning': 'Below is one possible improved solution. One important '
                 'change is that instead of relying solely on “shortest‐path” '
                 'searches between the sulfate attachment oxygen and any '
                 'nucleus atom, the code instead explicitly inspects the '
                 'immediate (and one‐bond‐removed) neighbors of a candidate '
                 'sulfate oxygen. In our approach we first identify a '
                 'candidate steroid nucleus (using the fused–ring heuristic as '
                 'before), then we loop over each oxygen that is bonded via a '
                 'single bond to a sulfur that in turn is “sulfate‐like” '
                 '(bound to at least three oxygens). For each such candidate '
                 'oxygen we require either that the oxygen’s only non–sulfur '
                 'neighbor is directly in the nucleus or that that neighbor '
                 '(which must be sp³ and non‐aromatic) in turn is directly '
                 'bonded to at least one nucleus atom. (In our testing this '
                 'catches cases such as 21‐hydroxypregnenolone monosulfate '
                 'while rejecting molecules whose sulfate groups are “far '
                 'away” from the fused ring core.) \n'
                 '\n'
                 'Below is the complete code in one Python block:\n'
                 '\n'
                 '------------------------------------------------',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 58,
    'num_false_positives': 80,
    'num_true_negatives': 142157,
    'num_false_negatives': 5,
    'num_negatives': None,
    'precision': 0.42028985507246375,
    'recall': 0.9206349206349206,
    'f1': 0.5771144278606966,
    'accuracy': 0.9994026704146171,
    'negative_predictive_value': 0.9999648288572193}