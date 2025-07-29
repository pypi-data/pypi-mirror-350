"""
Classifies: CHEBI:48953 cyclohexenones
"""
"""
Classifies: Cyclohexenones
Definition: Any six‐membered alicyclic ketone having one C=C double bond (alkene) in the ring,
with a ketone functionality (C=O) placed on a ring carbon that is directly adjacent (in the ring)
to one of the alkene carbons (ensuring conjugation). We now allow cases where the cyclohexenone
substructure appears even if an atom is shared, provided that no bond (i.e. two adjacent ring atoms)
is shared between two six‐membered rings.
"""
from rdkit import Chem

def is_cyclohexenones(smiles: str):
    """
    Determines if a molecule contains a cyclohexenone substructure based on its SMILES string.

    The algorithm:
      1. Parse the SMILES string.
      2. Get ring information (using GetRingInfo).
      3. Loop over each six‐membered ring:
         a. Ensure all atoms in the ring are carbons and non‐aromatic.
         b. Check if any bond in the ring is shared with another six‐membered ring (fused bond);
            if so, skip this ring.
         c. Count the number of C=C double bonds (alkene bonds) among ring–internal bonds.
            Exactly one such alkene bond is required.
         d. For each ring atom, check its neighbors outside the ring for an oxygen that is double‐bonded.
            Mark these ring atoms as “ketone‐bearing.”
         e. Check conjugation: at least one ketone–bearing ring atom must be adjacent (within the ring)
            to one of the two alkene atoms.
      4. If any ring passes, return True with an explanation; otherwise, return False.

    Returns:
      (bool, str): (True, explanation) if a valid cyclohexenone structure is detected; otherwise (False, explanation).
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    ring_info = mol.GetRingInfo()
    all_rings = ring_info.AtomRings()
    if not all_rings:
        return False, "No rings found in molecule"

    # Gather only six-membered rings (list of tuples of atom indices)
    six_membered_rings = [ring for ring in all_rings if len(ring) == 6]
    if not six_membered_rings:
        return False, "No six-membered rings found in molecule"

    # For helping determine bond fusion, construct a set for each six-membered ring's bonds.
    # Each bond is represented as a frozenset({a_idx, b_idx}) for adjacent atoms in the ring.
    rings_with_bonds = []
    for ring in six_membered_rings:
        # sort the ring into a cyclic order using the ordering from GetRingInfo 
        rset = set(ring)
        bonds = set()
        n = len(ring)
        for i in range(n):
            a = ring[i]
            b = ring[(i+1)%n]
            bonds.add(frozenset((a, b)))
        rings_with_bonds.append((set(ring), bonds))

    # Now process each candidate six-membered ring.
    for ring in six_membered_rings:
        ring_set = set(ring)
        # (a) Check that every atom in the ring is carbon and non‐aromatic.
        atoms_ok = True
        for idx in ring:
            atom = mol.GetAtomWithIdx(idx)
            if atom.GetAtomicNum() != 6 or atom.GetIsAromatic():
                atoms_ok = False
                break
        if not atoms_ok:
            continue

        # (b) Check for bond fusion: for every adjacent pair in the ring, if that bond appears in any other six‐membered ring, consider the bond fused.
        # Flag if any bond is found in more than one ring.
        fused = False
        # First get bonds for this ring.
        bonds_this_ring = set()
        n = len(ring)
        for i in range(n):
            a = ring[i]
            b = ring[(i+1)%n]
            bonds_this_ring.add(frozenset((a, b)))
        # Now check against all other six-membered rings.
        for other_ring_set, other_bonds in rings_with_bonds:
            # Skip comparing the ring with itself
            if other_ring_set == ring_set:
                continue
            # If there is an edge (bond) common to both rings, consider it fused.
            if bonds_this_ring.intersection(other_bonds):
                fused = True
                break
        if fused:
            # Skip fused six-membered rings
            continue

        # (c) Identify ring alkene bonds.
        alkene_bonds = []
        for i in range(n):
            a_idx = ring[i]
            b_idx = ring[(i+1)%n]
            bond = mol.GetBondBetweenAtoms(a_idx, b_idx)
            if bond is None:
                continue
            if bond.GetBondType() == Chem.BondType.DOUBLE:
                # Even though both atoms are carbons per our earlier check, we assume a C=O would not occur inside the ring.
                alkene_bonds.append((a_idx, b_idx))
        if len(alkene_bonds) != 1:
            continue

        # Save the two atom indices involved in the alkene bond
        alkene_atoms = set(alkene_bonds[0])

        # (d) Identify exocyclic ketone functionality.
        # For each ring atom, check for a neighbor not in the ring that is oxygen and double-bonded.
        ketone_atoms = set()
        for idx in ring:
            atom = mol.GetAtomWithIdx(idx)
            for nbr in atom.GetNeighbors():
                if nbr.GetIdx() in ring_set:
                    continue  # only exocyclic groups
                if nbr.GetAtomicNum() == 8:
                    bond = mol.GetBondBetweenAtoms(idx, nbr.GetIdx())
                    if bond and bond.GetBondType() == Chem.BondType.DOUBLE:
                        ketone_atoms.add(idx)
        if not ketone_atoms:
            continue  # no ketone functionality found on the ring

        # (e) Check for conjugation: at least one ketone-bearing ring atom must be adjacent (within the ring)
        # to one of the alkene atoms.
        conjugated = False
        for idx in ketone_atoms:
            # get ring neighbors for this index:
            atom_neighbors_in_ring = []
            for i in range(n):
                if ring[i] == idx:
                    # adjacent vertices in the cyclic order:
                    prev_atom = ring[(i-1)%n]
                    next_atom = ring[(i+1)%n]
                    atom_neighbors_in_ring.extend([prev_atom, next_atom])
            # Check if any neighbor is in the alkene_atoms
            for n_idx in atom_neighbors_in_ring:
                if n_idx in alkene_atoms:
                    conjugated = True
                    break
            if conjugated:
                break

        if conjugated:
            return True, ("Found a six‐membered, non‐aromatic carbon ring with exactly one ring alkene bond and an exocyclic ketone "
                          "group conjugated to the alkene; cyclohexenone substructure detected.")
    return False, "No valid cyclohexenone ring (six‐membered ring with one alkene bond and a conjugated ketone) was found."

# Example test (uncomment to try):
# test_smiles = "O[C@H]1[C@H](O)C(=CC(=O)C1N)CO"  # 2-Aminovalienone example: expected True
# result, reason = is_cyclohexenones(test_smiles)
# print(result, reason)


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:48953',
                          'name': 'cyclohexenones',
                          'definition': 'Any six-membered alicyclic ketone '
                                        'having one double bond in the ring.',
                          'parents': ['CHEBI:36132'],
                          'xrefs': ['PMID:21290509'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 56,
                           'log_lines_of_code': 4.02535169073515,
                           'indent_by_line': [   1,
                                                 1,
                                                 0,
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
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 3,
                                                 3,
                                                 2,
                                                 0,
                                                 1,
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
                                                 3,
                                                 0,
                                                 0,
                                                 0,
                                                 0,
                                                 0,
                                                 0,
                                                 1,
                                                 0],
                           'max_indent': 4,
                           'imports': ['from rdkit import Chem'],
                           'imports_count': 1,
                           'methods_called': [   'GetAtomicNum',
                                                 'MolFromSmiles',
                                                 'AtomRings',
                                                 'GetAtomWithIdx',
                                                 'append',
                                                 'GetRingInfo',
                                                 'add',
                                                 'GetIsAromatic'],
                           'methods_called_count': 8,
                           'smarts_strings': [],
                           'smarts_strings_count': 0,
                           'defs': ['is_cyclohexenones(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "No rings found in molecule"',
                                          'False, "No six-membered rings found '
                                          'in molecule"',
                                          'False, "No valid cyclohexenone ring '
                                          '(six‐membered ring with one alkene '
                                          'bond and a conjugated ketone) was '
                                          'found."'],
                           'returns_count': 4,
                           'complexity': 4.20507033814703},
    'message': '\n'
               'Attempt failed: F1 score of 0.40751879699248117 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: O[C@H]1[C@H](O)C(=CC(=O)C1N)CO NAME: '
               '2-Aminovalienone REASON: CORRECT Found an isolated '
               'six-membered non‐aromatic carbon ring having exactly one ring '
               'alkene bond and a conjugated exocyclic ketone group; '
               'cyclohexenone detected.\n'
               ' * SMILES: O=C1C(OC)=C(N)[C@@H](O)[C@]([C@H]1O)(O)C NAME: '
               '3-amino-4,5,6-trihydroxy-2-methoxy-5-methyl-2-cyclohexen-1-one '
               'REASON: CORRECT Found an isolated six-membered non‐aromatic '
               'carbon ring having exactly one ring alkene bond and a '
               'conjugated exocyclic ketone group; cyclohexenone detected.\n'
               ' * SMILES: O=C1C=C[C@H](/C=C/CCC)[C@H]([C@H]1O)C(=O)C(O)C '
               'NAME: Colletotricone B REASON: CORRECT Found an isolated '
               'six-membered non‐aromatic carbon ring having exactly one ring '
               'alkene bond and a conjugated exocyclic ketone group; '
               'cyclohexenone detected.\n'
               ' * SMILES: '
               'O=C1C=C2C(=COC(=C2)C=3C(=O)C[C@@H](O)CC3C)C=4[C@]1(OC(=O)C4C(=O)CCCCC)C '
               'NAME: Minutellin B REASON: CORRECT Found an isolated '
               'six-membered non‐aromatic carbon ring having exactly one ring '
               'alkene bond and a conjugated exocyclic ketone group; '
               'cyclohexenone detected.\n'
               ' * SMILES: '
               'O=C1C=C([C@@H](O)[C@@H]2[C@]1(O2)C)[C@H]3O[C@@H]3C(O)(C)C '
               'NAME: Acremine I REASON: CORRECT Found an isolated '
               'six-membered non‐aromatic carbon ring having exactly one ring '
               'alkene bond and a conjugated exocyclic ketone group; '
               'cyclohexenone detected.\n'
               ' * SMILES: '
               'O=C1C(NC(=O)/C=C/C=C/C=C/C(CC)C)=C[C@@](O)(/C=C/C=C/C=C/C(=O)NC2=C(O)CCC2=O)[C@@H](C1)O '
               'NAME: Asukamycin D-II REASON: CORRECT Found an isolated '
               'six-membered non‐aromatic carbon ring having exactly one ring '
               'alkene bond and a conjugated exocyclic ketone group; '
               'cyclohexenone detected.\n'
               ' * SMILES: O=C1C(O)=C(OC)C(=O)C2C1(O2)C NAME: Fumigatin oxide '
               'REASON: CORRECT Found an isolated six-membered non‐aromatic '
               'carbon ring having exactly one ring alkene bond and a '
               'conjugated exocyclic ketone group; cyclohexenone detected.\n'
               ' * SMILES: O=C1C=C(OC)[C@@H](OC)[C@H]([C@H]1O)O NAME: '
               'Botrysphone B REASON: CORRECT Found an isolated six-membered '
               'non‐aromatic carbon ring having exactly one ring alkene bond '
               'and a conjugated exocyclic ketone group; cyclohexenone '
               'detected.\n'
               ' * SMILES: O=C1C=C([C@H](O)[C@H]([C@@H]1O)O)COC(=O)C NAME: '
               'Gabosine G REASON: CORRECT Found an isolated six-membered '
               'non‐aromatic carbon ring having exactly one ring alkene bond '
               'and a conjugated exocyclic ketone group; cyclohexenone '
               'detected.\n'
               ' * SMILES: O=C1C=C(OC)[C@H](O)[C@@H]2[C@]1(O2)C/C=C(/CO)\\C '
               'NAME: Sarcosone B REASON: CORRECT Found an isolated '
               'six-membered non‐aromatic carbon ring having exactly one ring '
               'alkene bond and a conjugated exocyclic ketone group; '
               'cyclohexenone detected.\n'
               ' * SMILES: '
               'ClC=1C(=O)[C@H](Cl)[C@@H](O)[C@@]2(C1)O[C@@H](OC)[C@H](C2)NC(=O)/C=C/C(=C/[C@@H](CCCCCC)C)/C '
               'NAME: Gymnastatin B REASON: CORRECT Found an isolated '
               'six-membered non‐aromatic carbon ring having exactly one ring '
               'alkene bond and a conjugated exocyclic ketone group; '
               'cyclohexenone detected.\n'
               ' * SMILES: Cl\\C=C\\CO/N=C(/C1=C(O)CC(CC(SCC)C)CC1=O)\\CC '
               'NAME: mfcd01632327 REASON: CORRECT Found an isolated '
               'six-membered non‐aromatic carbon ring having exactly one ring '
               'alkene bond and a conjugated exocyclic ketone group; '
               'cyclohexenone detected.\n'
               ' * SMILES: Cl/C(=C\\C)/C12OC1(Cl)C(=O)C=C(C2O)OC NAME: '
               'Lachnumon REASON: CORRECT Found an isolated six-membered '
               'non‐aromatic carbon ring having exactly one ring alkene bond '
               'and a conjugated exocyclic ketone group; cyclohexenone '
               'detected.\n'
               ' * SMILES: '
               'O=C1C(NC(=O)/C=C/C=C/C=C/CC(C)C)=C[C@@](O)(/C=C/C=C/C=C/C(=O)NC2=C(O)CCC2=O)[C@H]3[C@@H]1O3 '
               'NAME: EI-1151-3 REASON: CORRECT Found an isolated six-membered '
               'non‐aromatic carbon ring having exactly one ring alkene bond '
               'and a conjugated exocyclic ketone group; cyclohexenone '
               'detected.\n'
               ' * SMILES: '
               'O=C1C(=C2C=C3C(=O)C(O)=C([C@@]3(C)CC[C@]2(C)C[C@H]1O)[C@@H](CO)C)C '
               'NAME: Cercosporene B REASON: CORRECT Found an isolated '
               'six-membered non‐aromatic carbon ring having exactly one ring '
               'alkene bond and a conjugated exocyclic ketone group; '
               'cyclohexenone detected.\n'
               ' * SMILES: O=C1C=C[C@H](C)[C@]2([C@@H]1O)C(=O)OC([C@H]2O)=C '
               'NAME: Mabetaarigenin C REASON: CORRECT Found an isolated '
               'six-membered non‐aromatic carbon ring having exactly one ring '
               'alkene bond and a conjugated exocyclic ketone group; '
               'cyclohexenone detected.\n'
               ' * SMILES: '
               'O1[C@]2(C[C@@H]3[C@@]4([C@](C(C(=O)CC4)(C)C)(CCC3=C)[H])C)[C@]1([C@H](O)C(=CC2=O)CO)[H] '
               'NAME: Macrophorin B REASON: CORRECT Found an isolated '
               'six-membered non‐aromatic carbon ring having exactly one ring '
               'alkene bond and a conjugated exocyclic ketone group; '
               'cyclohexenone detected.\n'
               ' * SMILES: O=C1C=C(OC)[C@H](O)[C@@]([C@H]1OC(=O)C)(O)C NAME: '
               'Xylariacyclone B REASON: CORRECT Found an isolated '
               'six-membered non‐aromatic carbon ring having exactly one ring '
               'alkene bond and a conjugated exocyclic ketone group; '
               'cyclohexenone detected.\n'
               ' * SMILES: O=C1C=C(OC)[C@H](O)[C@H]2[C@@H]1O2 NAME: '
               '(-)-sphaeropsidone REASON: CORRECT Found an isolated '
               'six-membered non‐aromatic carbon ring having exactly one ring '
               'alkene bond and a conjugated exocyclic ketone group; '
               'cyclohexenone detected.\n'
               ' * SMILES: '
               'O=C1C(NC(=O)/C(=C/C(=C/C(CCCC)C)/C)/C)=C[C@@](O)(/C=C/C=C/C=C/C(=O)NC2=C(O)CCC2=O)[C@@H](C1)O '
               'NAME: Manumycin D REASON: CORRECT Found an isolated '
               'six-membered non‐aromatic carbon ring having exactly one ring '
               'alkene bond and a conjugated exocyclic ketone group; '
               'cyclohexenone detected.\n'
               ' * SMILES: O=C1C=C(OC)[C@H](O)[C@@H]2[C@]1(O2)CC=C(C)C NAME: '
               'Sarcosone A REASON: CORRECT Found an isolated six-membered '
               'non‐aromatic carbon ring having exactly one ring alkene bond '
               'and a conjugated exocyclic ketone group; cyclohexenone '
               'detected.\n'
               ' * SMILES: '
               'O=C1C=C([C@@H](O)[C@H]2[C@@]1(O2)C[C@H]3C(=C)CC[C@@H]4[C@@]3(CC[C@H](C4(C)C)O)C)C '
               'NAME: Neomacrophorin VII REASON: CORRECT Found an isolated '
               'six-membered non‐aromatic carbon ring having exactly one ring '
               'alkene bond and a conjugated exocyclic ketone group; '
               'cyclohexenone detected.\n'
               ' * SMILES: '
               'O=C1C=C(C(=O)C2C1(O2)C(OC(=O)C)/C=C(/C=C/C=O)\\C)COC(=O)C '
               'NAME: Flagranone B REASON: CORRECT Found an isolated '
               'six-membered non‐aromatic carbon ring having exactly one ring '
               'alkene bond and a conjugated exocyclic ketone group; '
               'cyclohexenone detected.\n'
               ' * SMILES: O=C1C=C([C@H](O)[C@H]([C@@H]1O)O)CO NAME: Gabosine '
               'I REASON: CORRECT Found an isolated six-membered non‐aromatic '
               'carbon ring having exactly one ring alkene bond and a '
               'conjugated exocyclic ketone group; cyclohexenone detected.\n'
               ' * SMILES: '
               'O=C1C(C2=CC=CC=C2)=C(OC)[C@@H](O)[C@H](C1)C3=CC=CC=C3 NAME: '
               'Cucurbitarin A REASON: CORRECT Found an isolated six-membered '
               'non‐aromatic carbon ring having exactly one ring alkene bond '
               'and a conjugated exocyclic ketone group; cyclohexenone '
               'detected.\n'
               'False positives: SMILES: '
               'O=C1OC2CC3(OC(C(C)C=C3)C(CC)C)OC(C2)CC=C(C(OC4OC(C(O)C(C4)OC)C)C(C=CC=C(C5(C1C=C(C(=O)C5)C)O)C)C)C '
               "NAME: 4'-Deoleandrosyl-6,8a-seco-6,8a-deoxy-5- REASON: WRONGLY "
               'CLASSIFIED Found an isolated six-membered non‐aromatic carbon '
               'ring having exactly one ring alkene bond and a conjugated '
               'exocyclic ketone group; cyclohexenone detected.\n'
               ' * SMILES: O=C1C(OC)=C(C(=CN)C([C@@]1(CC)C)=O)[C@H](CC)C NAME: '
               'Mycosphine A REASON: WRONGLY CLASSIFIED Found an isolated '
               'six-membered non‐aromatic carbon ring having exactly one ring '
               'alkene bond and a conjugated exocyclic ketone group; '
               'cyclohexenone detected.\n'
               ' * SMILES: C[C@@H]1CC(=O)C=C(C)[C@]11CC[C@H](C1)C(C)=C NAME: '
               'solavetivone REASON: WRONGLY CLASSIFIED Found an isolated '
               'six-membered non‐aromatic carbon ring having exactly one ring '
               'alkene bond and a conjugated exocyclic ketone group; '
               'cyclohexenone detected.\n'
               ' * SMILES: O=C1C=C2C=CCC2C(C1O)/C=C(\\C=C\\C(O)CCCCCCC)/C '
               'NAME: Penostatin E REASON: WRONGLY CLASSIFIED Found an '
               'isolated six-membered non‐aromatic carbon ring having exactly '
               'one ring alkene bond and a conjugated exocyclic ketone group; '
               'cyclohexenone detected.\n'
               ' * SMILES: '
               '[C@]12(C=C[C@H](C)[C@@H](C(C)C)O1)C[C@@H]3C[C@H](O2)CC=C([C@H]([C@H](C=CC=C([C@]4([C@H](C(=O)O3)C=C(C(C4)=O)C)O)C)C)O)C '
               'NAME: 6,8a-seco-6,8a-deoxy-5-oxoavermectin "1b" aglycone '
               'REASON: WRONGLY CLASSIFIED Found an isolated six-membered '
               'non‐aromatic carbon ring having exactly one ring alkene bond '
               'and a conjugated exocyclic ketone group; cyclohexenone '
               'detected.\n'
               ' * SMILES: '
               'C=1(C(CCC(C1C)=O)(C)C)/C=C/C(=C/C=C/C(=C/C=C/C=C(/C=C/C=C(/C=C/C=2C(CCC(C2C)O)(C)C)\\C)\\C)/C)/C '
               "NAME: 4'-hydroxyechinenone REASON: WRONGLY CLASSIFIED Found an "
               'isolated six-membered non‐aromatic carbon ring having exactly '
               'one ring alkene bond and a conjugated exocyclic ketone group; '
               'cyclohexenone detected.\n'
               ' * SMILES: '
               'S1S[C@]23N([C@@H]4[C@@H](O)C=C[C@@H]([C@H]4C2)O)C([C@]15N([C@@H]6[C@@H](O)C=CC([C@H]6C5)=O)C3=O)=O '
               'NAME: Brocazine F REASON: WRONGLY CLASSIFIED Found an isolated '
               'six-membered non‐aromatic carbon ring having exactly one ring '
               'alkene bond and a conjugated exocyclic ketone group; '
               'cyclohexenone detected.\n'
               ' * SMILES: '
               '[C@@H]1(N2C3=C(C(=NC=N3)N)N=C2)O[C@H](COP(OP(OCC(C)([C@H](C(NCCC(NCCSC(C4=C([C@@H](CCC4=O)C)CCC([O-])=O)=O)=O)=O)O)C)(=O)[O-])(=O)[O-])[C@H]([C@H]1O)OP([O-])([O-])=O '
               'NAME: '
               '(3E)-2-(2-carboxylatoethyl)-3-methyl-6-oxocyclohex-1-ene-1-carboxyl-CoA(5-) '
               'REASON: WRONGLY CLASSIFIED Found an isolated six-membered '
               'non‐aromatic carbon ring having exactly one ring alkene bond '
               'and a conjugated exocyclic ketone group; cyclohexenone '
               'detected.\n'
               ' * SMILES: '
               '[H][C@]1(O[C@@H](C)[C@H](O)[C@@H](O)[C@H]1O)O[C@@H]1[C@@H](O)[C@H](O)[C@@H](CO)O[C@H]1O[C@H](C)CC[C@@]1([H])C(C)=CC(=O)CC1(C)C '
               'NAME: Gusanlungionoside D REASON: WRONGLY CLASSIFIED Found an '
               'isolated six-membered non‐aromatic carbon ring having exactly '
               'one ring alkene bond and a conjugated exocyclic ketone group; '
               'cyclohexenone detected.\n'
               ' * SMILES: O=C1C[C@@H](C(C)C)CC=C1C NAME: Carvotanacetone '
               'REASON: WRONGLY CLASSIFIED Found an isolated six-membered '
               'non‐aromatic carbon ring having exactly one ring alkene bond '
               'and a conjugated exocyclic ketone group; cyclohexenone '
               'detected.\n'
               ' * SMILES: '
               'O=C1C=C(OC)[C@H]2[C@]3([C@@]14OC(=O)[C@@]3(O)[C@H]5[C@@]4([C@@H]2C(=O)O5)C)C '
               'NAME: (+)-preuisolactone A REASON: WRONGLY CLASSIFIED Found an '
               'isolated six-membered non‐aromatic carbon ring having exactly '
               'one ring alkene bond and a conjugated exocyclic ketone group; '
               'cyclohexenone detected.\n'
               ' * SMILES: '
               'O(C1CC(C(C(O)(C1)C)=C=C/C(/C)=C/C=C/C=C/C=C(/C=C/2\\OC(=O)C(\\C=C\\C3(O)C(CC(=O)C=C3C)(C)C)=C2)\\C)(C)C)C(=O)C '
               'NAME: '
               "(3S,5R,6R,6'S)-6,7-Didehydro-5,6-dihydro-3,5,6'-trihydroxy-13,14,20-trinor-3'-oxo-beta,epsilon-caroten-19',11'-olide "
               '3-acetate REASON: WRONGLY CLASSIFIED Found an isolated '
               'six-membered non‐aromatic carbon ring having exactly one ring '
               'alkene bond and a conjugated exocyclic ketone group; '
               'cyclohexenone detected.\n'
               ' * SMILES: '
               '[H][C@]1(O[C@@H]2O[C@@H](C)[C@@H](NO[C@H]3C[C@H](O)[C@H](SC(=O)c4c(C)c(I)c(O[C@@H]5O[C@@H](C)[C@H](O)[C@@H](OC)[C@H]5O)c(OC)c4OC)[C@@H](C)O3)[C@H](O)[C@H]2O[C@H]2C[C@H](OC)[C@H](CO2)NCC)C#C\\C=C/C#C[C@]2(O)CC(=O)C(NC(=O)OC)=C1/C2=C\\CSSSC '
               'NAME: calicheamicin gamma1(I) REASON: WRONGLY CLASSIFIED Found '
               'an isolated six-membered non‐aromatic carbon ring having '
               'exactly one ring alkene bond and a conjugated exocyclic ketone '
               'group; cyclohexenone detected.\n'
               ' * SMILES: '
               'O=C1OC2=C(C(=O)[C@@H](O)[C@@]([C@H]2OC3=C1C(=CC(=C3C)O)C)(OC)C)C '
               'NAME: Roseopurpurin C REASON: WRONGLY CLASSIFIED Found an '
               'isolated six-membered non‐aromatic carbon ring having exactly '
               'one ring alkene bond and a conjugated exocyclic ketone group; '
               'cyclohexenone detected.\n'
               ' * SMILES: '
               'O=C1C=C([C@@H](O)[C@H]([C@H]1CC=C(CCC=C(CCC(=O)O)C)C)O)C NAME: '
               'Peniginsengin C REASON: WRONGLY CLASSIFIED Found an isolated '
               'six-membered non‐aromatic carbon ring having exactly one ring '
               'alkene bond and a conjugated exocyclic ketone group; '
               'cyclohexenone detected.\n'
               ' * SMILES: '
               'O=C1C=C([C@@H](O)[C@H]2[C@@]1(O2)C[C@H]3C(=C)CC[C@@H]4[C@@]3(CC[C@H](C4(C)C)O)C)COC(=O)[C@H](O)[C@@H](O)C '
               'NAME: Neomacrophorin II REASON: WRONGLY CLASSIFIED Found an '
               'isolated six-membered non‐aromatic carbon ring having exactly '
               'one ring alkene bond and a conjugated exocyclic ketone group; '
               'cyclohexenone detected.\n'
               ' * SMILES: '
               'C=1(C(C[C@@H](C(C1C)=O)O)(C)C)/C=C/C(=C/C=C/C(=C/C=C/C=C(/C=C/C=C(/C=C/C=2C(C[C@@H](CC2C)O)(C)C)\\C)\\C)/C)/C '
               'NAME: adonixanthin REASON: WRONGLY CLASSIFIED Found an '
               'isolated six-membered non‐aromatic carbon ring having exactly '
               'one ring alkene bond and a conjugated exocyclic ketone group; '
               'cyclohexenone detected.\n'
               ' * SMILES: '
               'S([C@@]12N(C(=O)[C@]3(SC)[C@H](O)C4([C@@H](N3C1=O)NC=5C=CC=CC45)O)C6CC=7O[C@@H](C)C(C7C(C6([C@H]2O)O)=O)(C)C)C '
               'NAME: Leporizine C REASON: WRONGLY CLASSIFIED Found an '
               'isolated six-membered non‐aromatic carbon ring having exactly '
               'one ring alkene bond and a conjugated exocyclic ketone group; '
               'cyclohexenone detected.\n'
               ' * SMILES: '
               'O=C1C=C(OC)[C@H](O)[C@@]([C@H]1OC2=C(O)C(=C(O)C(=C2)OC)C)(O)C '
               'NAME: Xylariacyclone A REASON: WRONGLY CLASSIFIED Found an '
               'isolated six-membered non‐aromatic carbon ring having exactly '
               'one ring alkene bond and a conjugated exocyclic ketone group; '
               'cyclohexenone detected.\n'
               ' * SMILES: '
               'O[C@@H]1C(C(=C(C[C@H]1O)C)\\C=C\\C(\\C)=C\\C=C\\C(\\C)=C\\C=C\\C=C(\\C=C\\C=C(\\C=C\\C=2C([C@@H](O)[C@@H](O)C(=O)C2C)(C)C)/C)/C)(C)C '
               'NAME: 4-Ketonostoxanthin REASON: WRONGLY CLASSIFIED Found an '
               'isolated six-membered non‐aromatic carbon ring having exactly '
               'one ring alkene bond and a conjugated exocyclic ketone group; '
               'cyclohexenone detected.\n'
               ' * SMILES: '
               'O=C1C(=C(O)[C@@]2(C=3C(O)=C(C)C(=C(C3O[C@@]2(C1)OCC)C(=O)C)O)C)C(=NCCCC(=O)OCC)C '
               'NAME: Usenamine F REASON: WRONGLY CLASSIFIED Found an isolated '
               'six-membered non‐aromatic carbon ring having exactly one ring '
               'alkene bond and a conjugated exocyclic ketone group; '
               'cyclohexenone detected.\n'
               ' * SMILES: '
               'O=C1C(=C(O)[C@@]2(C=3C(O)=C(C(=O)C)C(=C(C3O[C@]2(C1)OC)C)O)C)C(=O)C '
               'NAME: (-)-placodiolic acid REASON: WRONGLY CLASSIFIED Found an '
               'isolated six-membered non‐aromatic carbon ring having exactly '
               'one ring alkene bond and a conjugated exocyclic ketone group; '
               'cyclohexenone detected.\n'
               ' * SMILES: '
               'CCCC(=O)c1c(C)cc(C)c(C2CC(=O)C(\\C(CC)=N\\OCC)=C(O)C2)c1C '
               'NAME: Butroxydim REASON: WRONGLY CLASSIFIED Found an isolated '
               'six-membered non‐aromatic carbon ring having exactly one ring '
               'alkene bond and a conjugated exocyclic ketone group; '
               'cyclohexenone detected.\n'
               ' * SMILES: '
               'COC(=O)C[C@H]1C(C)(C)C(=O)C=C[C@]1(C)[C@H]1[C@H](OC(C)=O)[C@H](OC(C)=O)[C@@]2(C)[C@@H](C[C@H]3O[C@@]23C1=C)c1ccoc1 '
               'NAME: Toonacilin REASON: WRONGLY CLASSIFIED Found an isolated '
               'six-membered non‐aromatic carbon ring having exactly one ring '
               'alkene bond and a conjugated exocyclic ketone group; '
               'cyclohexenone detected.\n'
               ' * SMILES: O=C1C(=C2[C@@](CC2)(CO)[C@@]3(C1=CC(C)(C)C3)O)C '
               'NAME: Granulone A REASON: WRONGLY CLASSIFIED Found an isolated '
               'six-membered non‐aromatic carbon ring having exactly one ring '
               'alkene bond and a conjugated exocyclic ketone group; '
               'cyclohexenone detected.\n'
               'False negatives: SMILES: O=C1[C@H](CC(CO)=C(C1)O)CC=C(C)C '
               'NAME: '
               '5-hydroxy-4-(hydroxymethyl)-2-(3-methylbut-2-en-1-yl)cyclohex-4-en-1-one '
               'REASON: MISSED No isolated cyclohexenone ring (six-membered '
               'ring with one ring alkene and a conjugated ketone) was found.\n'
               ' * SMILES: '
               'O=C1C=C2[C@@](O)([C@H](O)[C@H]3C=CC=C[C@@H]([C@@H]2C3=O)C)[C@@H]([C@@]1(O)C)O '
               'NAME: Penicanone REASON: MISSED No isolated cyclohexenone ring '
               '(six-membered ring with one ring alkene and a conjugated '
               'ketone) was found.\n'
               ' * SMILES: '
               'O=C1C=C[C@@]2([C@H]3[C@]4([C@@]56[C@@H](C(=O)OC5)[C@@H](O)[C@@](C4)(C)C([C@@]6(C3)CO)=O)CC[C@H]2C1(C)C)C '
               'NAME: Emeridone E REASON: MISSED No isolated cyclohexenone '
               'ring (six-membered ring with one ring alkene and a conjugated '
               'ketone) was found.\n'
               ' * SMILES: '
               'ClC1=C2C(C3=C(C(=O)C)C(O[C@]3(C1=O)C)=O)=COC(=C2)/C=C/C(=C/[C@H](CC)C)/C '
               'NAME: 5-Chloroisorotiorin REASON: MISSED No isolated '
               'cyclohexenone ring (six-membered ring with one ring alkene and '
               'a conjugated ketone) was found.\n'
               ' * SMILES: OC1(C2(C(C(C(O)CC2)(C)C)C(=O)C=C1C)C)CO NAME: '
               '4,7-Dihydroxy-4-(hydroxymethyl)-3,4a,8,8-tetramethyl-5,6,7,8a-tetrahydronaphthalen-1-one '
               'REASON: MISSED No isolated cyclohexenone ring (six-membered '
               'ring with one ring alkene and a conjugated ketone) was found.\n'
               ' * SMILES: CC1CCCC2CC(C(=CC12C)C=O)=O NAME: '
               '10beta-12,13-dinor-8-oxo-6-eremophilen-11-al REASON: MISSED No '
               'isolated cyclohexenone ring (six-membered ring with one ring '
               'alkene and a conjugated ketone) was found.\n'
               ' * SMILES: '
               'O=C1C=C2C(=COC(=C2)C)[C@@H]([C@@]1(O)C)C(=O)[C@H](O)[C@H](CC)C '
               'NAME: Phomopsone A REASON: MISSED No isolated cyclohexenone '
               'ring (six-membered ring with one ring alkene and a conjugated '
               'ketone) was found.\n'
               ' * SMILES: '
               'O=C1C=2C(C=C(/C=C/C)OC2)=CC=3[C@]1(OC(=O)C3C(=O)CCCCC)C NAME: '
               'Rubropunctatine REASON: MISSED No isolated cyclohexenone ring '
               '(six-membered ring with one ring alkene and a conjugated '
               'ketone) was found.\n'
               ' * SMILES: '
               'O=C1C=C2C(=COC(=C2)/C=C/C)C3C1(OC(=O)C3C(=O)CCCCCCC)C NAME: '
               'Monasfluore B REASON: MISSED No isolated cyclohexenone ring '
               '(six-membered ring with one ring alkene and a conjugated '
               'ketone) was found.\n'
               ' * SMILES: '
               'O=C1C=C2[C@@]3([C@H]([C@H](O)CC2)C)C[C@@]1(OC3)C(=C)C NAME: '
               'Penicilleremophilane B REASON: MISSED No isolated '
               'cyclohexenone ring (six-membered ring with one ring alkene and '
               'a conjugated ketone) was found.\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'O=C(N[C@@H](C(O)(C)C)C)[C@H]([C@@]1([C@@]2([C@@](CC1)(/C(/CCC2)=C/C=C\\3/C[C@@H](O)C[C@H](O)C3=C)[H])C)[H])C',
                                     'name': '1alpha,25-dihydroxy-24-oxo-23-azavitamin '
                                             'D2 / '
                                             '1alpha,25-dihydroxy-24-oxo-23-azaergocalciferol',
                                     'reason': 'No valid cyclohexenone ring '
                                               '(six‐membered ring with one '
                                               'alkene bond and a conjugated '
                                               'ketone) was found.'},
                                 {   'smiles': 'CCCCCCCCCCCCCCCCCCC(O)C([O-])=O',
                                     'name': '2-hydroxyarachidate',
                                     'reason': 'No rings found in molecule'},
                                 {   'smiles': 'C[C@@H](CN([C@@H](C)CO)C(=O)NC1=CC=C(C=C1)C(F)(F)F)[C@@H](CN(C)C(=O)C2CCOCC2)OC',
                                     'name': 'N-[(2S,3S)-4-[[(2S)-1-hydroxypropan-2-yl]-[[4-(trifluoromethyl)phenyl]carbamoyl]amino]-2-methoxy-3-methylbutyl]-N-methyloxane-4-carboxamide',
                                     'reason': 'No valid cyclohexenone ring '
                                               '(six‐membered ring with one '
                                               'alkene bond and a conjugated '
                                               'ketone) was found.'},
                                 {   'smiles': 'CC(=O)CC\\C=C(/C)CCC=C(C)C',
                                     'name': 'geranyl acetone',
                                     'reason': 'No rings found in molecule'},
                                 {   'smiles': 'O([C@H]1[C@H](O)[C@H](O[C@H](O)[C@H]1O)CO[C@H]2O[C@@H]([C@@H](O)[C@H](O)[C@@H]2O)CO)[C@H]3O[C@@H]([C@@H](O)[C@H](O)[C@@H]3O[C@H]4O[C@@H]([C@@H](O)[C@H](O)[C@@H]4O)CO)CO',
                                     'name': '(2S,3S,4S,5S,6R)-2-[[(2R,3R,4S,5S,6S)-4-[(2R,3S,4S,5S,6R)-4,5-Dihydroxy-6-(hydroxymethyl)-3-[(2R,3S,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-3,5,6-trihydroxyoxan-2-yl]methoxy]-6-(hydroxymethyl)oxane-3,4,5-triol',
                                     'reason': 'No valid cyclohexenone ring '
                                               '(six‐membered ring with one '
                                               'alkene bond and a conjugated '
                                               'ketone) was found.'},
                                 {   'smiles': 'O=C(OC1=C(C(O)=C(C(=O)O)C(=C1C)C)C)C2=C(OC)C(=C(OC(=O)C3=C(O)C=C(O)C=C3C)C=C2C)C',
                                     'name': 'Thielavin Z5',
                                     'reason': 'No valid cyclohexenone ring '
                                               '(six‐membered ring with one '
                                               'alkene bond and a conjugated '
                                               'ketone) was found.'},
                                 {   'smiles': '[C@@H]1([C@@H]([C@H]([C@@H]([C@H](O1)CO)O)O)NC(C)=O)O[C@@H]2[C@@H]([C@H](C(O[C@@H]2CO)O)O)O',
                                     'name': 'beta-D-GlcpNAc-(1->4)-D-Galp',
                                     'reason': 'No valid cyclohexenone ring '
                                               '(six‐membered ring with one '
                                               'alkene bond and a conjugated '
                                               'ketone) was found.'},
                                 {   'smiles': 'CN(C)C(=O)C1=CC=C(C=C1)C2=CC=C(C=C2)[C@@H]3[C@H]4CN(CC(=O)N4[C@H]3CO)C(=O)CC5CC5',
                                     'name': '4-[4-[(6S,7R,8R)-4-(2-cyclopropyl-1-oxoethyl)-8-(hydroxymethyl)-2-oxo-1,4-diazabicyclo[4.2.0]octan-7-yl]phenyl]-N,N-dimethylbenzamide',
                                     'reason': 'No valid cyclohexenone ring '
                                               '(six‐membered ring with one '
                                               'alkene bond and a conjugated '
                                               'ketone) was found.'},
                                 {   'smiles': 'CCCCCCCCCCCCCCCCCCCCC=C',
                                     'name': '1-docosene',
                                     'reason': 'No rings found in molecule'},
                                 {   'smiles': 'C([C@@](OC(=O)CCC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)([H])COC(=O)CC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)OC(=O)CCCCC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC',
                                     'name': 'TG(22:5(7Z,10Z,13Z,16Z,19Z)/20:5(5Z,8Z,11Z,14Z,17Z)/22:6(4Z,7Z,10Z,13Z,16Z,19Z))[iso6]',
                                     'reason': 'No rings found in molecule'}],
    'sample_false_negatives': [   {   'smiles': 'O=C1[C@H](CC(CO)=C(C1)O)CC=C(C)C',
                                      'name': '5-hydroxy-4-(hydroxymethyl)-2-(3-methylbut-2-en-1-yl)cyclohex-4-en-1-one',
                                      'reason': 'No valid cyclohexenone ring '
                                                '(six‐membered ring with one '
                                                'alkene bond and a conjugated '
                                                'ketone) was found.'},
                                  {   'smiles': 'O=C1C=C2[C@@](O)([C@H](O)[C@H]3C=CC=C[C@@H]([C@@H]2C3=O)C)[C@@H]([C@@]1(O)C)O',
                                      'name': 'Penicanone',
                                      'reason': 'No valid cyclohexenone ring '
                                                '(six‐membered ring with one '
                                                'alkene bond and a conjugated '
                                                'ketone) was found.'},
                                  {   'smiles': 'O=C1C=C[C@@]2([C@H]3[C@]4([C@@]56[C@@H](C(=O)OC5)[C@@H](O)[C@@](C4)(C)C([C@@]6(C3)CO)=O)CC[C@H]2C1(C)C)C',
                                      'name': 'Emeridone E',
                                      'reason': 'No valid cyclohexenone ring '
                                                '(six‐membered ring with one '
                                                'alkene bond and a conjugated '
                                                'ketone) was found.'},
                                  {   'smiles': 'ClC1=C2C(C3=C(C(=O)C)C(O[C@]3(C1=O)C)=O)=COC(=C2)/C=C/C(=C/[C@H](CC)C)/C',
                                      'name': '5-Chloroisorotiorin',
                                      'reason': 'No valid cyclohexenone ring '
                                                '(six‐membered ring with one '
                                                'alkene bond and a conjugated '
                                                'ketone) was found.'},
                                  {   'smiles': 'OC1(C2(C(C(C(O)CC2)(C)C)C(=O)C=C1C)C)CO',
                                      'name': '4,7-Dihydroxy-4-(hydroxymethyl)-3,4a,8,8-tetramethyl-5,6,7,8a-tetrahydronaphthalen-1-one',
                                      'reason': 'No valid cyclohexenone ring '
                                                '(six‐membered ring with one '
                                                'alkene bond and a conjugated '
                                                'ketone) was found.'},
                                  {   'smiles': 'CC1CCCC2CC(C(=CC12C)C=O)=O',
                                      'name': '10beta-12,13-dinor-8-oxo-6-eremophilen-11-al',
                                      'reason': 'No valid cyclohexenone ring '
                                                '(six‐membered ring with one '
                                                'alkene bond and a conjugated '
                                                'ketone) was found.'},
                                  {   'smiles': 'O=C1C=C2C(=COC(=C2)C)[C@@H]([C@@]1(O)C)C(=O)[C@H](O)[C@H](CC)C',
                                      'name': 'Phomopsone A',
                                      'reason': 'No valid cyclohexenone ring '
                                                '(six‐membered ring with one '
                                                'alkene bond and a conjugated '
                                                'ketone) was found.'},
                                  {   'smiles': 'O=C1C=2C(C=C(/C=C/C)OC2)=CC=3[C@]1(OC(=O)C3C(=O)CCCCC)C',
                                      'name': 'Rubropunctatine',
                                      'reason': 'No valid cyclohexenone ring '
                                                '(six‐membered ring with one '
                                                'alkene bond and a conjugated '
                                                'ketone) was found.'},
                                  {   'smiles': 'O=C1C=C2C(=COC(=C2)/C=C/C)C3C1(OC(=O)C3C(=O)CCCCCCC)C',
                                      'name': 'Monasfluore B',
                                      'reason': 'No valid cyclohexenone ring '
                                                '(six‐membered ring with one '
                                                'alkene bond and a conjugated '
                                                'ketone) was found.'},
                                  {   'smiles': 'O=C1C=C2[C@@]3([C@H]([C@H](O)CC2)C)C[C@@]1(OC3)C(=C)C',
                                      'name': 'Penicilleremophilane B',
                                      'reason': 'No valid cyclohexenone ring '
                                                '(six‐membered ring with one '
                                                'alkene bond and a conjugated '
                                                'ketone) was found.'}],
    'attempt': 5,
    'reasoning': 'Below is our reasoning before the code. In the previous '
                 'implementation we checked every atom’s “6‐membered ring '
                 'membership” count to rule out fused rings. It turned out '
                 'that some true cyclohexenone rings were being rejected '
                 'because (a) the rigidity of “each atom must appear in '
                 'exactly one six‐membered ring” was too strict in cases where '
                 'a cyclohexenone substructure appears even in a polycyclic '
                 'environment, and (b) slight differences in how the double '
                 'bond or carbonyl are drawn led to missing the target '
                 'functionality. To improve things we now (1) check the ring '
                 'bonds themselves to see if any bond is “fused” (i.e. shared '
                 'between two six‐membered rings) rather than counting each '
                 'atom’s overall membership, (2) verify that every atom in the '
                 'candidate ring is a non‐aromatic carbon, (3) count exactly '
                 'one ring–internal C=C (alkene) bond (ignoring any C=O bonds '
                 'since those come from exocyclic oxygens), (4) search for '
                 'exocyclic carbonyl (ketone) groups where the oxygen is '
                 'attached as a double‐bond to a ring atom, and (5) require '
                 'that at least one ketone–bearing ring atom is directly '
                 'adjacent (in the ring) to one of the two atoms found in the '
                 'alkene bond (to ensure conjugation). The following code '
                 'reflects this revised approach.\n'
                 '\n'
                 'Now, here is the complete Python code in one block:',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 274,
    'num_false_positives': 631,
    'num_true_negatives': 141231,
    'num_false_negatives': 164,
    'num_negatives': None,
    'precision': 0.3027624309392265,
    'recall': 0.6255707762557078,
    'f1': 0.40804169769173493,
    'accuracy': 0.9944132115249473,
    'negative_predictive_value': 0.9988401287174228}