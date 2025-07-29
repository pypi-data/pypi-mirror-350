"""
Classifies: CHEBI:47909 3-oxo-Delta(4) steroid
"""
#!/usr/bin/env python3
"""
Classifies: 3-oxo-Delta(4) steroid
Definition: A 3-oxo steroid conjugated to a C=C double bond at the alpha,beta position,
i.e. a steroid (with a fused tetracyclic nucleus) that contains an α,β-unsaturated ketone 
(enone) in one of its six-membered rings.
"""
from rdkit import Chem

def is_3_oxo_Delta_4__steroid(smiles: str):
    """
    Determines if a molecule is a 3-oxo-Delta(4) steroid based on its SMILES string.
    The classification requires:
      (a) A fused steroid nucleus – defined as a connected system of rings (only considering rings of size 5 or 6)
          containing at least 4 rings (typically three six-membered and one five-membered).
      (b) Within one of the six-membered rings of that fused system, an enone motif is present; that is,
          a carbon (in the ring) that has a double bond to an oxygen (C=O), and via a single bond is connected 
          to a second carbon in the ring that, in turn, participates in a C=C double bond with a third carbon (within the same ring).
    Args:
        smiles (str): SMILES string of the molecule.
    Returns:
        bool: True if the molecule is a 3-oxo-Delta(4) steroid, False otherwise.
        str: Explanation of the classification.
    """
    # Parse the SMILES string.
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # ---------------------------
    # 1. Identify candidate rings (only 5- or 6-membered rings).
    # ---------------------------
    ring_info = mol.GetRingInfo()
    all_rings = ring_info.AtomRings()
    candidate_rings = []
    for ring in all_rings:
        if len(ring) in (5, 6):
            candidate_rings.append(set(ring))
    if not candidate_rings:
        return False, "No candidate 5- or 6-membered rings found for steroid nucleus"

    # ---------------------------
    # 2. Build a fused ring graph.
    # Two rings will be considered "fused" if they share at least 2 atoms.
    # ---------------------------
    num = len(candidate_rings)
    graph = {i: set() for i in range(num)}
    for i in range(num):
        for j in range(i+1, num):
            if len(candidate_rings[i] & candidate_rings[j]) >= 2:
                graph[i].add(j)
                graph[j].add(i)

    # Find connected components in the ring graph.
    visited = set()
    fused_components = []
    for i in range(num):
        if i not in visited:
            stack = [i]
            comp = set()
            while stack:
                current = stack.pop()
                if current in comp:
                    continue
                comp.add(current)
                for nbr in graph[current]:
                    if nbr not in comp:
                        stack.append(nbr)
            visited |= comp
            fused_components.append(comp)

    # ---------------------------
    # 3. Look for a fused tetracyclic nucleus.
    # We require at least 4 rings in one connected component with at least three six‐membered rings and one five‐membered ring.
    # ---------------------------
    steroid_component = None
    for comp in fused_components:
        comp_rings = [candidate_rings[i] for i in comp]
        count6 = sum(1 for ring in comp_rings if len(ring) == 6)
        count5 = sum(1 for ring in comp_rings if len(ring) == 5)
        if len(comp_rings) >= 4 and count6 >= 3 and count5 >= 1:
            # Found a candidate steroid nucleus
            steroid_component = comp_rings  # list of sets of atom indices
            break
    if steroid_component is None:
        return False, "Steroid nucleus not found (insufficient fused ring system with 3 six-membered and 1 five-membered rings)"

    # Build a union of all atom indices in the fused steroid nucleus:
    steroid_atoms = set()
    for ring in steroid_component:
        steroid_atoms.update(ring)

    # ---------------------------
    # 4. Look for an enone functionality (α,β-unsaturated ketone) in one six-membered ring of the nucleus.
    # ---------------------------
    # We restrict our search to six-membered rings that are part of the steroid nucleus.
    six_membered_rings = [ring for ring in steroid_component if len(ring)==6]
    enone_found = False
    # Iterate through each six-membered ring
    for ring in six_membered_rings:
        for idx in ring:
            atom = mol.GetAtomWithIdx(idx)
            # Consider only carbon atoms
            if atom.GetAtomicNum() != 6:
                continue
            # Look for a carbonyl: check if this carbon is double-bonded to at least one oxygen.
            carbonyl_oxygens = []
            for bond in atom.GetBonds():
                # check if bond is double and neighbor is oxygen
                if bond.GetBondType() == Chem.rdchem.BondType.DOUBLE:
                    nbr = bond.GetOtherAtom(atom)
                    if nbr.GetAtomicNum() == 8:
                        carbonyl_oxygens.append(nbr.GetIdx())
            if not carbonyl_oxygens:
                continue  # no carbonyl at this carbon

            # Now search for a beta carbon: a neighbor (in the same ring) via a single bond.
            for bond in atom.GetBonds():
                nbr = bond.GetOtherAtom(atom)
                if nbr.GetIdx() not in ring:
                    continue  # must be part of the same ring
                if nbr.GetAtomicNum() != 6:
                    continue  # ensure neighbor is carbon
                # Avoid the carbonyl oxygen connection
                if nbr.GetIdx() in carbonyl_oxygens:
                    continue

                # Now check if this neighbor (the beta carbon) participates in a C=C double bond to another carbon in the same ring.
                for bond2 in nbr.GetBonds():
                    if bond2.GetBondType() != Chem.rdchem.BondType.DOUBLE:
                        continue
                    gamma = bond2.GetOtherAtom(nbr)
                    if gamma.GetIdx() == atom.GetIdx():
                        continue  # skip if going back to original carbonyl carbon
                    if gamma.GetIdx() not in ring:
                        continue  # ensure gamma carbon is in the same ring
                    if gamma.GetAtomicNum() != 6:
                        continue
                    # Found a candidate enone: carbonyl carbon (with double bond O) connected (single bond) to a beta carbon that participates in a double bond with gamma.
                    enone_found = True
                    break
                if enone_found:
                    break
            if enone_found:
                break
        if enone_found:
            break

    if not enone_found:
        return False, "Enone motif not found in a six-membered ring within the steroid nucleus"
    
    return True, "Contains a fused steroid nucleus (3 six-membered and 1 five-membered fused rings) with a 3-oxo/Δ(4) enone motif."

# Example usage (for testing purposes):
if __name__ == "__main__":
    # Test with (20S)-20-hydroxypregn-4-en-3-one
    test_smiles = "[H][C@@]1(CC[C@@]2([H])[C@]3([H])CCC4=CC(=O)CC[C@]4(C)[C@@]3([H])CC[C@]12C)[C@H](C)O"
    result, reason = is_3_oxo_Delta_4__steroid(test_smiles)
    print(result, reason)


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:47909',
                          'name': '3-oxo-Delta(4) steroid',
                          'definition': 'A 3-oxo steroid conjugated to a C=C '
                                        'double bond at the alpha,beta '
                                        'position.',
                          'parents': ['CHEBI:47788', 'CHEBI:51689'],
                          'xrefs': [   'KEGG:C00619',
                                       'MetaCyc:3-Oxo-Delta-4-Steroids'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 106,
                           'log_lines_of_code': 4.663439094112067,
                           'indent_by_line': [   1,
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
                                                 2,
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
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 3,
                                                 1,
                                                 2,
                                                 0,
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
                                                 0,
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
                                                 4,
                                                 5,
                                                 6,
                                                 3,
                                                 3,
                                                 0,
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
                                                 3,
                                                 3,
                                                 3,
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
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
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
                                                 6,
                                                 3,
                                                 4,
                                                 0,
                                                 0,
                                                 0,
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
                           'imports': ['from rdkit import Chem'],
                           'imports_count': 1,
                           'methods_called': [   'GetOtherAtom',
                                                 'append',
                                                 'GetIdx',
                                                 'GetAtomicNum',
                                                 'MolFromSmiles',
                                                 'AtomRings',
                                                 'GetAtomWithIdx',
                                                 'pop',
                                                 'GetBonds',
                                                 'add',
                                                 'update',
                                                 'GetBondType',
                                                 'GetRingInfo'],
                           'methods_called_count': 13,
                           'smarts_strings': [],
                           'smarts_strings_count': 0,
                           'defs': ['is_3_oxo_Delta_4__steroid(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "No candidate 5- or '
                                          '6-membered rings found for steroid '
                                          'nucleus"',
                                          'False, "Steroid nucleus not found '
                                          '(insufficient fused ring system '
                                          'with 3 six-membered and 1 '
                                          'five-membered rings)"',
                                          'False, "Enone motif not found in a '
                                          'six-membered ring within the '
                                          'steroid nucleus"',
                                          'True, "Contains a fused steroid '
                                          'nucleus (3 six-membered and 1 '
                                          'five-membered fused rings) with a '
                                          '3-oxo/Δ(4) enone motif."'],
                           'returns_count': 5,
                           'complexity': 5.932687818822414},
    'message': '\n'
               'Attempt failed: F1 score of 0.17259786476868327 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: '
               '[H][C@@]1(CC[C@@]2([H])[C@]3([H])CCC4=CC(=O)CC[C@]4(C)[C@@]3([H])CC[C@]12C)[C@H](C)O '
               'NAME: (20S)-20-hydroxypregn-4-en-3-one REASON: CORRECT '
               'Contains a fused steroid nucleus with a 3-oxo/Δ(4) enone motif '
               'in a six-membered ring.\n'
               ' * SMILES: '
               '[H][C@@]12CCC3=CC(=O)C=C[C@]3(C)[C@@]1([H])[C@@H](O)C[C@@]1(C)[C@@]2([H])C[C@@H](C(=O)OC)[C@]1(O)C(=O)CO '
               'NAME: methyl prednisolone-16alpha-carboxylate REASON: CORRECT '
               'Contains a fused steroid nucleus with a 3-oxo/Δ(4) enone motif '
               'in a six-membered ring.\n'
               ' * SMILES: '
               'C1[C@@]2([C@@]([C@@]3(C(C1)=CC(CC3)=O)C)(CC[C@@]4([C@@](CC[C@@]24[H])([H])C(CO)O)C)[H])[H] '
               'NAME: 4-pregnen-20,21-diol-3-one REASON: CORRECT Contains a '
               'fused steroid nucleus with a 3-oxo/Δ(4) enone motif in a '
               'six-membered ring.\n'
               ' * SMILES: '
               '[H][C@]12CCC(=O)C=C1CC[C@]1([H])[C@]2([H])CC[C@]2(C)[C@@H](O)CC[C@@]12[H] '
               'NAME: nandrolone REASON: CORRECT Contains a fused steroid '
               'nucleus with a 3-oxo/Δ(4) enone motif in a six-membered ring.\n'
               ' * SMILES: '
               'C[C@@H]1C[C@@H]2[C@H]3CC[C@@]4(C)[C@@H](CC[C@]4(C)O)[C@@H]3CCC2=CC1=O '
               'NAME: 17beta-hydroxy-2alpha,17-dimethylestr-4-en-3-one REASON: '
               'CORRECT Contains a fused steroid nucleus with a 3-oxo/Δ(4) '
               'enone motif in a six-membered ring.\n'
               ' * SMILES: '
               '[H][C@@]1(CC[C@@]2([H])[C@]3([H])CCC4=CC(=O)CC[C@]4(C)[C@@]3([H])CC[C@]12C)[C@H](C)CC[C@@H](C)C(C)C '
               'NAME: campest-4-en-3-one REASON: CORRECT Contains a fused '
               'steroid nucleus with a 3-oxo/Δ(4) enone motif in a '
               'six-membered ring.\n'
               ' * SMILES: '
               '[H][C@@]1(CC[C@@]2([H])[C@]3([H])[C@H](O)CC4=CC(=O)CC[C@]4(C)[C@@]3([H])CC[C@]12C)[C@H](C)CC[C@H](O)C(C)C '
               'NAME: (24S)-7alpha,24-dihydroxycholest-4-en-3-one REASON: '
               'CORRECT Contains a fused steroid nucleus with a 3-oxo/Δ(4) '
               'enone motif in a six-membered ring.\n'
               ' * SMILES: '
               '[H][C@@]12CCC3=CC(=O)CC[C@]3(C)[C@@]1([H])CC[C@@]1(C)[C@@]2([H])C[C@H]2OC(C)(C)O[C@@]12C(C)=O '
               'NAME: algestone acetonide REASON: CORRECT Contains a fused '
               'steroid nucleus with a 3-oxo/Δ(4) enone motif in a '
               'six-membered ring.\n'
               ' * SMILES: '
               'C[C@H]1C[C@H]2[C@@H]3CC[C@](OC(C)=O)(C(C)=O)[C@@]3(C)C[C@H](O)[C@]2(F)[C@@]2(C)C=CC(=O)C=C12 '
               'NAME: fluorometholone acetate REASON: CORRECT Contains a fused '
               'steroid nucleus with a 3-oxo/Δ(4) enone motif in a '
               'six-membered ring.\n'
               ' * SMILES: '
               '[H][C@@]12CCC3=CC(=O)CC[C@]3(C)[C@@]1([H])CC[C@@]1(C)[C@@]2([H])C[C@H]2O[C@](C)(O[C@@]12C(C)=O)c1ccccc1 '
               'NAME: algestone acetophenide REASON: CORRECT Contains a fused '
               'steroid nucleus with a 3-oxo/Δ(4) enone motif in a '
               'six-membered ring.\n'
               ' * SMILES: '
               '[H][C@@]12C[C@@H](C)[C@H](C(=O)CO)[C@@]1(C)C[C@H](O)[C@@]1(Cl)[C@@]2([H])C[C@H](F)C2=CC(=O)C=C[C@]12C '
               'NAME: clocortolone REASON: CORRECT Contains a fused steroid '
               'nucleus with a 3-oxo/Δ(4) enone motif in a six-membered ring.\n'
               ' * SMILES: '
               '[H][C@@]12CCC3=C(SCCC(=O)NCCCCCC(=O)NCCCCCC(=O)ON4C(=O)CCC4=O)C(=O)CC[C@]3(C)[C@@]1([H])CC[C@]1(C)[C@H](CC[C@@]21[H])C(C)=O '
               'NAME: 2,5-dioxo-1-pyrrolidinyl '
               '6-(6-{3-[(progesterone-4-yl)thiopropionyl]aminohexanoyl}amino)hexanoate '
               'REASON: CORRECT Contains a fused steroid nucleus with a '
               '3-oxo/Δ(4) enone motif in a six-membered ring.\n'
               ' * SMILES: '
               'C[C@]12CC[C@H]3[C@@H](CCC4=CC(=O)CC[C@]34C)[C@@H]1C[C@H](O)[C@@H]2O '
               'NAME: 16beta-hydroxytestosterone REASON: CORRECT Contains a '
               'fused steroid nucleus with a 3-oxo/Δ(4) enone motif in a '
               'six-membered ring.\n'
               ' * SMILES: '
               '[H][C@@]1(CC[C@@]2([H])[C@]3([H])CCC4=CC(=O)CC[C@]4(C)[C@@]3([H])CC[C@]12C)[C@H](C)OCC(O)=O '
               'NAME: (20S)-20-(carboxymethyl)oxypregn-4-en-3-one REASON: '
               'CORRECT Contains a fused steroid nucleus with a 3-oxo/Δ(4) '
               'enone motif in a six-membered ring.\n'
               ' * SMILES: '
               'C1[C@]2([C@]3([C@@]([C@@]4(C(=CC(CC4)=O)[C@H](C3)C)C)(CC[C@@]2([C@@](C1)(O)C(=O)C)C)[H])[H])[H] '
               'NAME: medroxyprogesterone REASON: CORRECT Contains a fused '
               'steroid nucleus with a 3-oxo/Δ(4) enone motif in a '
               'six-membered ring.\n'
               ' * SMILES: '
               'C1[C@@]2([C@@]([C@@]3(C(C1)=CC(CC3)=O)C)([C@H](C[C@@]4([C@@](CC[C@@]24[H])(O)[C@@H](CO)O)C)O)[H])[H] '
               'NAME: 20beta-dihydrocortisol REASON: CORRECT Contains a fused '
               'steroid nucleus with a 3-oxo/Δ(4) enone motif in a '
               'six-membered ring.\n'
               ' * SMILES: '
               '[H][C@@]1(CC[C@@]2([H])[C@]3([H])CCC4=CC(=O)CC[C@]4(C)[C@@]3([H])CC[C@]12C)[C@H](C)[C@@H](O)[C@H](O)[C@@H](C)C(C)C '
               'NAME: (22R,23R)-22,23-dihydroxycampest-4-en-3-one REASON: '
               'CORRECT Contains a fused steroid nucleus with a 3-oxo/Δ(4) '
               'enone motif in a six-membered ring.\n'
               ' * SMILES: '
               '[H][C@@]12C[C@H](C)[C@](O)(C(=O)COC(C)=O)[C@@]1(C)C[C@H](O)[C@@]1(F)[C@@]2([H])CCC2=CC(=O)C=C[C@]12C '
               'NAME: betamethasone acetate REASON: CORRECT Contains a fused '
               'steroid nucleus with a 3-oxo/Δ(4) enone motif in a '
               'six-membered ring.\n'
               ' * SMILES: '
               '[H][C@@]1(CC[C@@]2([H])[C@]3([H])[C@H](O)CC4=CC(=O)CC[C@]4(C)[C@@]3([H])CC[C@]12C)[C@H](C)CCCC(C)CO '
               'NAME: 7alpha,26-dihydroxycholest-4-en-3-one REASON: CORRECT '
               'Contains a fused steroid nucleus with a 3-oxo/Δ(4) enone motif '
               'in a six-membered ring.\n'
               ' * SMILES: '
               '[H][C@@]12CCC3=CC(=O)CC[C@]3(C)C1=CC[C@]1(C)[C@H](CC[C@@]21[H])C(C)=O '
               'NAME: pregna-4,9(11)-diene-3,20-dione REASON: CORRECT Contains '
               'a fused steroid nucleus with a 3-oxo/Δ(4) enone motif in a '
               'six-membered ring.\n'
               ' * SMILES: '
               '[H][C@@]12C[C@@H](O)[C@](O)(C(=O)CO)[C@@]1(C)C[C@H](O)[C@@]1([H])[C@@]2([H])CCC2=CC(=O)C=C[C@]12C '
               'NAME: 16alpha-hydroxyprednisolone REASON: CORRECT Contains a '
               'fused steroid nucleus with a 3-oxo/Δ(4) enone motif in a '
               'six-membered ring.\n'
               ' * SMILES: '
               '[H][C@@]12CCC3=CC(=O)CC[C@]3(C)[C@@]1([H])[C@H](O)C[C@]1(C)[C@H](CC[C@@]21[H])C(C)=O '
               'NAME: 11alpha-hydroxyprogesterone REASON: CORRECT Contains a '
               'fused steroid nucleus with a 3-oxo/Δ(4) enone motif in a '
               'six-membered ring.\n'
               ' * SMILES: '
               'C[C@@H]([C@H]1CC[C@H]2[C@@H]3CCC4=CC(=O)C=C[C@]4(C)[C@H]3CC[C@]12C)C(O)=O '
               'NAME: 3-oxo-23,24-bisnorchola-1,4-dien-22-oic acid REASON: '
               'CORRECT Contains a fused steroid nucleus with a 3-oxo/Δ(4) '
               'enone motif in a six-membered ring.\n'
               ' * SMILES: '
               '[H][C@@]1(CC[C@@]2([H])[C@]3([H])CCC4=CC(=O)CC[C@]4(C)[C@@]3([H])CC[C@]12C)C(=O)CO '
               'NAME: 11-deoxycorticosterone REASON: CORRECT Contains a fused '
               'steroid nucleus with a 3-oxo/Δ(4) enone motif in a '
               'six-membered ring.\n'
               ' * SMILES: '
               '[H][C@@]12C[C@H](C)[C@](OC(C)=O)(C(=O)COC(C)=O)[C@@]1(C)C[C@H](O)[C@@]1(F)[C@@]2([H])C[C@H](F)C2=CC(=O)C=C[C@]12C '
               'NAME: diflorasone diacetate REASON: CORRECT Contains a fused '
               'steroid nucleus with a 3-oxo/Δ(4) enone motif in a '
               'six-membered ring.\n'
               'False positives: SMILES: '
               'O=C1C2=C(O)C3=C(O)C=C(OC)C4=C3C(=C2C5(O)C6(C1(O)C(O)=C(C(=O)C6)C(=O)N)O5)CC74C(=CCCC7(C)C)C '
               'NAME: Viridicatumtoxin B REASON: WRONGLY CLASSIFIED Contains a '
               'fused steroid nucleus with a 3-oxo/Δ(4) enone motif in a '
               'six-membered ring.\n'
               ' * SMILES: '
               'O=C1[C@@]2([C@]([C@]3([C@@]([C@@]4(C(CC3)=C(O[C@@H]5O[C@@H]([C@@H](O)[C@H](O)[C@H]5O)C(O)=O)C(=O)CC4)C)(CC2)[H])[H])(CC1)[H])C '
               'NAME: 4-Hydroxyandrostenedione glucuronide REASON: WRONGLY '
               'CLASSIFIED Contains a fused steroid nucleus with a 3-oxo/Δ(4) '
               'enone motif in a six-membered ring.\n'
               ' * SMILES: '
               'CC(=O)[C@H]1CC[C@H]2[C@@H]3C[C@H]4OC[C@@]5(CCC(=O)C=C45)[C@H]3CC[C@]12C '
               'NAME: 6beta,19-Epoxypregn-4-ene-3,20-dione REASON: WRONGLY '
               'CLASSIFIED Contains a fused steroid nucleus with a 3-oxo/Δ(4) '
               'enone motif in a six-membered ring.\n'
               ' * SMILES: '
               'O=C1C=C2C(=C(O)C[C@@H]3[C@@]2(CCC(C3(C)C)=O)C)[C@]4([C@]1(C(=CC4=O)[C@@](O)(CC(=O)C[C@@H](C(=O)O)C)C)C)C '
               'NAME: Applanoic acid D REASON: WRONGLY CLASSIFIED Contains a '
               'fused steroid nucleus with a 3-oxo/Δ(4) enone motif in a '
               'six-membered ring.\n'
               ' * SMILES: '
               'O=C1C(OC)=C(C(=O)C=2C1=C(O)C3=C(C(=O)C4(O)C5C3OC4(C(O[C@@H]6O[C@@H]([C@@H](O[C@H]7O[C@@H]([C@@](O)(C(=O)C)[C@H](C7)O)C)CC6)C)C(C5OC8O[C@H]([C@H](O)[C@@H](C8)O)C)O)CCC)C2O)C=9C(OC)=C(OC)C%10=CC=%11CC%12C(O[C@@H]%13O[C@H]([C@H](O)[C@@H](C%13)O)C)C(O)C(C(C%12(C(C%11C(=C%10C9O)O)=O)O)(O)CCC)O[C@@H]%14O[C@@H]([C@@H](O[C@H]%15O[C@@H]([C@@](O)(C(=O)C)[C@H](C%15)O)C)CC%14)C '
               'NAME: Hibarimicin G REASON: WRONGLY CLASSIFIED Contains a '
               'fused steroid nucleus with a 3-oxo/Δ(4) enone motif in a '
               'six-membered ring.\n'
               ' * SMILES: '
               'O=C1C2=C([C@@]3([C@@H](O)C[C@@H]([C@]3(C1)C)[C@@H](CC(O)C=C(C(=O)O)C)C)C)[C@@H](O)CC4[C@@]2(CC[C@@H](C4(C)C)O)C '
               'NAME: Ganolucidic acid gamma a REASON: WRONGLY CLASSIFIED '
               'Contains a fused steroid nucleus with a 3-oxo/Δ(4) enone motif '
               'in a six-membered ring.\n'
               ' * SMILES: '
               'C[C@@]12[C@]([C@]3([C@](CC1)([C@@]4(C(C(=C3)C)=CC(CC4)=O)[H])[H])[H])(CC[C@@]2(C(C)=O)O)[H] '
               'NAME: nomegestrol REASON: WRONGLY CLASSIFIED Contains a fused '
               'steroid nucleus with a 3-oxo/Δ(4) enone motif in a '
               'six-membered ring.\n'
               ' * SMILES: '
               'O1[C@H]2[C@]3([C@]4([C@@]([C@](CC4)([C@@H]([C@@]5(OC(=O)C(=C(C5)C)C)[H])C)[H])(CC[C@@]3([C@@]6([C@@](O)([C@@H]12)CC=CC6=O)C)[H])C)[H])[H] '
               'NAME: Withanolide B REASON: WRONGLY CLASSIFIED Contains a '
               'fused steroid nucleus with a 3-oxo/Δ(4) enone motif in a '
               'six-membered ring.\n'
               ' * SMILES: '
               'O=C1NC2=C(C(=O)C[C@H]3[C@]1([C@@]4([C@](O)(C5=CC(=O)[C@@H]6O[C@]5(OC6(C)C)CC4)CC3)C)C)C=C7C[C@H]8C(C7=C2)=CC(OC8(C)C)(C)C '
               'NAME: Shearinine I REASON: WRONGLY CLASSIFIED Contains a fused '
               'steroid nucleus with a 3-oxo/Δ(4) enone motif in a '
               'six-membered ring.\n'
               ' * SMILES: '
               'O=C1C2=C([C@]3(CCC(C([C@@H]3C1)(C)C)=O)C)CC[C@]4([C@]2(CC[C@@H]4[C@@H](C[C@H]5OC(=O)C(=C5)C)C)C)C '
               'NAME: '
               '(+)-(5alpha,23R,24Z)-lanosta-8,24-dien-3,7-dioxo-23,26-gamma-lactone '
               'REASON: WRONGLY CLASSIFIED Contains a fused steroid nucleus '
               'with a 3-oxo/Δ(4) enone motif in a six-membered ring.\n'
               ' * SMILES: '
               'O=C1C=C2O[C@@H]3C[C@@]4([C@H]([C@@H](OC(=O)C)C[C@]4(C5=C3[C@]2(C)[C@H](C1(C)C)CC5)C)[C@@H](C[C@@H]6OC(=O)C(=C6)C)C)C '
               'NAME: Lepiotaprocerin E REASON: WRONGLY CLASSIFIED Contains a '
               'fused steroid nucleus with a 3-oxo/Δ(4) enone motif in a '
               'six-membered ring.\n'
               ' * SMILES: '
               'O=C1C2=C(C(=O)C[C@@H]3[C@@]2(CC[C@@H](C3(C)C)O)C)[C@@]4(C(=O)C[C@@H]([C@]4([C@@H]1OC(=O)C)C)/C(=C/C(=O)CC(C(=O)O)C)/C)C '
               'NAME: '
               '12b-acetoxy-3b-hydroxy-7,11,15,23-tetraoxo-lanost-8,20E-diene-26-oic '
               'acid REASON: WRONGLY CLASSIFIED Contains a fused steroid '
               'nucleus with a 3-oxo/Δ(4) enone motif in a six-membered ring.\n'
               ' * SMILES: '
               'O=C1C(O)=C(C2=CC=3C(=CC(=CC3O[C@]42[C@@]15[C@H]([C@@H](C)CO4)CC[C@H]5C)O)CO)C '
               'NAME: Rhodatin REASON: WRONGLY CLASSIFIED Contains a fused '
               'steroid nucleus with a 3-oxo/Δ(4) enone motif in a '
               'six-membered ring.\n'
               ' * SMILES: '
               'O=C1C=C2[C@@]3([C@H](C(C(=O)CC3)(C)C)C[C@@H]4[C@]2(O4)[C@]5([C@]1([C@@H](/C(=C/[C@@H]6OC(=O)[C@H](C6)C)/C)C[C@@H]5O)C)C)C '
               'NAME: Gibbosicolid B REASON: WRONGLY CLASSIFIED Contains a '
               'fused steroid nucleus with a 3-oxo/Δ(4) enone motif in a '
               'six-membered ring.\n'
               ' * SMILES: '
               'O=C1C=C2[C@H](CC[C@]3([C@H]2[C@@H](O[C@@H]4O[C@@H]([C@@H](O)[C@@H]([C@H]4O)O)CO)C[C@@H]3[C@@H](/C=C/[C@@H](C(O)(C)C)C)C)C)[C@@]5([C@@H]1C[C@@H](O)CC5)C '
               'NAME: Fomentarol D REASON: WRONGLY CLASSIFIED Contains a fused '
               'steroid nucleus with a 3-oxo/Δ(4) enone motif in a '
               'six-membered ring.\n'
               ' * SMILES: '
               'COC1=C[C@@H](C)[C@@H]2C[C@H]3OC(=O)C[C@H]4[C@@](C)(C[C@@H](O)[C@@H]([C@@]34C)[C@@]2(C)C1=O)C(=O)[C@H]1COC(=O)C1 '
               'NAME: Picrasin A REASON: WRONGLY CLASSIFIED Contains a fused '
               'steroid nucleus with a 3-oxo/Δ(4) enone motif in a '
               'six-membered ring.\n'
               ' * SMILES: '
               'CC(=O)O[C@@H]1C[C@H]2C(C)(C)C(=O)C=C[C@]2(C)[C@H]2CC[C@]3(C)C(=CC(=O)O[C@]3(O)c3ccoc3)[C@]12C '
               'NAME: nimolicinol REASON: WRONGLY CLASSIFIED Contains a fused '
               'steroid nucleus with a 3-oxo/Δ(4) enone motif in a '
               'six-membered ring.\n'
               ' * SMILES: '
               'C[C@@]12[C@]([C@]3(C(=CC1)[C@]4(C)C(CC3)=CC(CC4)=O)[H])(CC[C@@]2(C(COC(C)=O)=O)O)[H] '
               'NAME: Anecortave acetate REASON: WRONGLY CLASSIFIED Contains a '
               'fused steroid nucleus with a 3-oxo/Δ(4) enone motif in a '
               'six-membered ring.\n'
               ' * SMILES: '
               'C[C@]12CC(=O)[C@H]3[C@@H](CCC4=CC(=O)CC[C@]34C)[C@@H]1C[C@@H]1OC(=O)C=C21 '
               'NAME: 16beta-Hydroxy-3,11-dioxopregna-4,17(20)-dien-21-oic '
               'acid, gamma-lactone REASON: WRONGLY CLASSIFIED Contains a '
               'fused steroid nucleus with a 3-oxo/Δ(4) enone motif in a '
               'six-membered ring.\n'
               ' * SMILES: '
               'O1C(C2(O)C=3NC(C4OCC(O)C4O)=CC3C(O)=C(C2=O)C(=O)/C=C/C5=CC=C(O)C=C5)C(O)C(O)C(O)C1CO '
               'NAME: Cartormin REASON: WRONGLY CLASSIFIED Contains a fused '
               'steroid nucleus with a 3-oxo/Δ(4) enone motif in a '
               'six-membered ring.\n'
               ' * SMILES: '
               'C[C@@H]([C@H]1CC[C@H]2[C@@H]3C[C@H]4O[C@]44[C@@H](O)[C@H](CC(=O)[C@]4(C)[C@H]3CC[C@]12C)OS(O)(=O)=O)[C@H]1CC(C)=C(CO)C(=O)O1 '
               'NAME: 2,3-dihydro-3beta-O-sulfate withaferin A REASON: WRONGLY '
               'CLASSIFIED Contains a fused steroid nucleus with a 3-oxo/Δ(4) '
               'enone motif in a six-membered ring.\n'
               ' * SMILES: '
               'C[C@@]12CC[C@@H]3[C@@]4(C)C=CC(=O)C(C)(C)[C@@H]4C[C@@H](OC(=O)c4ccccc4)[C@@]3(C)C1=CC(=O)[C@H]2c1ccoc1 '
               'NAME: 7-benzoylnimbocinol REASON: WRONGLY CLASSIFIED Contains '
               'a fused steroid nucleus with a 3-oxo/Δ(4) enone motif in a '
               'six-membered ring.\n'
               ' * SMILES: '
               'CC(C)(COC(=O)c1ccc2OCOc2c1)CC1=C(O)C(=O)c2ccccc2C1=O NAME: '
               'rhinacanthin D REASON: WRONGLY CLASSIFIED Contains a fused '
               'steroid nucleus with a 3-oxo/Δ(4) enone motif in a '
               'six-membered ring.\n'
               ' * SMILES: '
               'CC(=O)[C@H]1CC[C@H]2[C@@H]3C[C@@H](O)C4=CC(=O)CC[C@]4(C)[C@H]3[C@H](O)C[C@]12C '
               'NAME: 6beta,11alpha-Dihydroxyprogesterone REASON: WRONGLY '
               'CLASSIFIED Contains a fused steroid nucleus with a 3-oxo/Δ(4) '
               'enone motif in a six-membered ring.\n'
               ' * SMILES: '
               'O=C1C2=C([C@]3(CC[C@@H](C([C@@H]3C1)(C)C)O)C)CC[C@]4([C@]2(C[C@@H](O)[C@@H]4[C@H](C(=O)O)CCC(=C)C(C)C)C)C '
               'NAME: '
               '3beta,16alpha-dihydroxy-7-oxo-24-methyllanosta-8,24(31)-dien-21-oic '
               'acid REASON: WRONGLY CLASSIFIED Contains a fused steroid '
               'nucleus with a 3-oxo/Δ(4) enone motif in a six-membered ring.\n'
               'False negatives: SMILES: '
               '[H][C@@]1(CC[C@@]2([H])[C@]3([H])CC4=CC(=O)CC[C@]4(C)[C@@]3([H])CC[C@]12C)[C@H](C)CCCC(C)C '
               'NAME: B-norcholest-4-en-3-one REASON: MISSED Steroid nucleus '
               'not found (insufficient six-membered and/or five-membered '
               'rings)\n'
               ' * SMILES: '
               '[H][C@@]12CCC3=CC(=O)C=C[C@]3(C)[C@@]1([H])CC[C@]1(C)OC(=O)CC[C@@]21[H] '
               'NAME: testolactone REASON: MISSED Steroid nucleus not found '
               '(insufficient six-membered and/or five-membered rings)\n'
               ' * SMILES: '
               '[H][C@@]12CCC3=CC(=O)CC[C@]3(C)[C@@]1([H])CC[C@]1(C)OC(=O)CC[C@@]21[H] '
               'NAME: testololactone REASON: MISSED Steroid nucleus not found '
               '(insufficient six-membered and/or five-membered rings)\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'O=C(N[C@@H](C(O)(C)C)C)[C@H]([C@@]1([C@@]2([C@@](CC1)(/C(/CCC2)=C/C=C\\3/C[C@@H](O)C[C@H](O)C3=C)[H])C)[H])C',
                                     'name': '1alpha,25-dihydroxy-24-oxo-23-azavitamin '
                                             'D2 / '
                                             '1alpha,25-dihydroxy-24-oxo-23-azaergocalciferol',
                                     'reason': 'Steroid nucleus not found '
                                               '(insufficient fused ring '
                                               'system with 3 six-membered and '
                                               '1 five-membered rings)'},
                                 {   'smiles': 'CCCCCCCCCCCCCCCCCCC(O)C([O-])=O',
                                     'name': '2-hydroxyarachidate',
                                     'reason': 'No candidate 5- or 6-membered '
                                               'rings found for steroid '
                                               'nucleus'},
                                 {   'smiles': 'C[C@@H](CN([C@@H](C)CO)C(=O)NC1=CC=C(C=C1)C(F)(F)F)[C@@H](CN(C)C(=O)C2CCOCC2)OC',
                                     'name': 'N-[(2S,3S)-4-[[(2S)-1-hydroxypropan-2-yl]-[[4-(trifluoromethyl)phenyl]carbamoyl]amino]-2-methoxy-3-methylbutyl]-N-methyloxane-4-carboxamide',
                                     'reason': 'Steroid nucleus not found '
                                               '(insufficient fused ring '
                                               'system with 3 six-membered and '
                                               '1 five-membered rings)'},
                                 {   'smiles': 'CC(=O)CC\\C=C(/C)CCC=C(C)C',
                                     'name': 'geranyl acetone',
                                     'reason': 'No candidate 5- or 6-membered '
                                               'rings found for steroid '
                                               'nucleus'},
                                 {   'smiles': 'O([C@H]1[C@H](O)[C@H](O[C@H](O)[C@H]1O)CO[C@H]2O[C@@H]([C@@H](O)[C@H](O)[C@@H]2O)CO)[C@H]3O[C@@H]([C@@H](O)[C@H](O)[C@@H]3O[C@H]4O[C@@H]([C@@H](O)[C@H](O)[C@@H]4O)CO)CO',
                                     'name': '(2S,3S,4S,5S,6R)-2-[[(2R,3R,4S,5S,6S)-4-[(2R,3S,4S,5S,6R)-4,5-Dihydroxy-6-(hydroxymethyl)-3-[(2R,3S,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-3,5,6-trihydroxyoxan-2-yl]methoxy]-6-(hydroxymethyl)oxane-3,4,5-triol',
                                     'reason': 'Steroid nucleus not found '
                                               '(insufficient fused ring '
                                               'system with 3 six-membered and '
                                               '1 five-membered rings)'},
                                 {   'smiles': 'O=C(OC1=C(C(O)=C(C(=O)O)C(=C1C)C)C)C2=C(OC)C(=C(OC(=O)C3=C(O)C=C(O)C=C3C)C=C2C)C',
                                     'name': 'Thielavin Z5',
                                     'reason': 'Steroid nucleus not found '
                                               '(insufficient fused ring '
                                               'system with 3 six-membered and '
                                               '1 five-membered rings)'},
                                 {   'smiles': '[C@@H]1([C@@H]([C@H]([C@@H]([C@H](O1)CO)O)O)NC(C)=O)O[C@@H]2[C@@H]([C@H](C(O[C@@H]2CO)O)O)O',
                                     'name': 'beta-D-GlcpNAc-(1->4)-D-Galp',
                                     'reason': 'Steroid nucleus not found '
                                               '(insufficient fused ring '
                                               'system with 3 six-membered and '
                                               '1 five-membered rings)'},
                                 {   'smiles': 'CN(C)C(=O)C1=CC=C(C=C1)C2=CC=C(C=C2)[C@@H]3[C@H]4CN(CC(=O)N4[C@H]3CO)C(=O)CC5CC5',
                                     'name': '4-[4-[(6S,7R,8R)-4-(2-cyclopropyl-1-oxoethyl)-8-(hydroxymethyl)-2-oxo-1,4-diazabicyclo[4.2.0]octan-7-yl]phenyl]-N,N-dimethylbenzamide',
                                     'reason': 'Steroid nucleus not found '
                                               '(insufficient fused ring '
                                               'system with 3 six-membered and '
                                               '1 five-membered rings)'},
                                 {   'smiles': 'CCCCCCCCCCCCCCCCCCCCC=C',
                                     'name': '1-docosene',
                                     'reason': 'No candidate 5- or 6-membered '
                                               'rings found for steroid '
                                               'nucleus'},
                                 {   'smiles': 'C([C@@](OC(=O)CCC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)([H])COC(=O)CC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)OC(=O)CCCCC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC',
                                     'name': 'TG(22:5(7Z,10Z,13Z,16Z,19Z)/20:5(5Z,8Z,11Z,14Z,17Z)/22:6(4Z,7Z,10Z,13Z,16Z,19Z))[iso6]',
                                     'reason': 'No candidate 5- or 6-membered '
                                               'rings found for steroid '
                                               'nucleus'}],
    'sample_false_negatives': [   {   'smiles': '[H][C@@]1(CC[C@@]2([H])[C@]3([H])CC4=CC(=O)CC[C@]4(C)[C@@]3([H])CC[C@]12C)[C@H](C)CCCC(C)C',
                                      'name': 'B-norcholest-4-en-3-one',
                                      'reason': 'Steroid nucleus not found '
                                                '(insufficient fused ring '
                                                'system with 3 six-membered '
                                                'and 1 five-membered rings)'},
                                  {   'smiles': '[H][C@@]12CCC3=CC(=O)C=C[C@]3(C)[C@@]1([H])CC[C@]1(C)OC(=O)CC[C@@]21[H]',
                                      'name': 'testolactone',
                                      'reason': 'Steroid nucleus not found '
                                                '(insufficient fused ring '
                                                'system with 3 six-membered '
                                                'and 1 five-membered rings)'},
                                  {   'smiles': '[H][C@@]12CCC3=CC(=O)CC[C@]3(C)[C@@]1([H])CC[C@]1(C)OC(=O)CC[C@@]21[H]',
                                      'name': 'testololactone',
                                      'reason': 'Steroid nucleus not found '
                                                '(insufficient fused ring '
                                                'system with 3 six-membered '
                                                'and 1 five-membered rings)'}],
    'attempt': 4,
    'reasoning': 'Below is the complete Python code. In our reasoning we '
                 'realized that the crude “ring‐counting” approach was too '
                 'permissive (allowing unrelated fused ring systems) and in '
                 'some cases too strict (missing steroids whose rings do not '
                 'appear as exactly three six‐membered plus one five‐membered '
                 'rings when examined individually). To improve matters we now '
                 '(a) restrict our search to rings of size 5 or 6, (b) build a '
                 'graph of “fused” rings (rings sharing at least two atoms) '
                 'and then look for a connected component representing a fused '
                 'tetracyclic system (with at least three six‐membered and at '
                 'least one five‐membered ring) and (c) search within the '
                 'six‐membered rings in that fused system for an enone motif '
                 '(a carbon with a C=O bonded to a neighboring carbon that is '
                 'doubly bonded to another carbon, all within the ring). This '
                 'change helps weed out false positives (when nonsteroid fused '
                 'systems mimic parts of the pattern) and catches cases that '
                 'were wrongfully missed. \n'
                 '\n'
                 'Below is the complete code:',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 194,
    'num_false_positives': 1504,
    'num_true_negatives': 140599,
    'num_false_negatives': 3,
    'num_negatives': None,
    'precision': 0.11425206124852769,
    'recall': 0.9847715736040609,
    'f1': 0.20474934036939313,
    'accuracy': 0.9894096978215039,
    'negative_predictive_value': 0.9999786631769108}