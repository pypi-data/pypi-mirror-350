"""
Classifies: CHEBI:50563 iridoid monoterpenoid
"""
"""
Classifies: Iridoid monoterpenoid (and secoiridoid derivatives)
Definition:
  Iridoid monoterpenoids are biosynthetically derived from isoprene units and 
  typically possess a fused bicyclic core – a cyclopentane ring fused to a six-membered 
  oxygen heterocycle. In some cases, ring opening (secoiridoids) is observed.
  
  Our algorithm has two stages:
    Stage 1 – Fused bicyclic core detection.
      * Look for one 5-membered ring that is composed only of nonaromatic carbons.
      * Look for one 6-membered ring that contains exactly one (nonaromatic) oxygen 
        and five carbons (all nonaromatic).
      * The two rings must share exactly 2 atoms.
      * Moreover, the two shared atoms must be connected (i.e. they are consecutive in 
        the atom order in both rings) so that the fusion is “real”.
    Stage 2 – Rescue for secoiridoids.
      * Look for any nonaromatic cyclopentane (5-membered, all carbons) that carries at 
        least 2 exocyclic carbonyl substituents.
"""

from rdkit import Chem

def is_iridoid_monoterpenoid(smiles: str):
    """
    Determines if a molecule is an iridoid monoterpenoid / secoiridoid derivative
    based on its SMILES string.
    
    Args:
      smiles (str): SMILES string of the molecule.
      
    Returns:
      (bool, str): Tuple; whether classified as iridoid monoterpenoid and the reason.
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
    
    ring_info = mol.GetRingInfo().AtomRings()
    if not ring_info:
        return False, "No rings found in the molecule"

    # Helper function to check if in a ring ordering the two indices are adjacent.
    def are_adjacent_in_ring(ring_tuple, a, b):
        n = len(ring_tuple)
        for i in range(n):
            # Using wrap-around (neighbor indices in ring)
            if (ring_tuple[i] == a and ring_tuple[(i+1)%n] == b) or \
               (ring_tuple[i] == b and ring_tuple[(i+1)%n] == a):
                return True
        return False

    # Stage 1: Check for fused bicyclic core.
    # Iterate over all pairs of rings with sizes 5 and 6.
    for i in range(len(ring_info)):
        for j in range(i+1, len(ring_info)):
            ring1 = ring_info[i]
            ring2 = ring_info[j]
            size1, size2 = len(ring1), len(ring2)
            if sorted([size1, size2]) != [5, 6]:
                continue

            # Identify which ring is 5-membered and which is 6-membered.
            if size1 == 5:
                ring5 = ring1
                order5 = ring1  # preserving order
                ring6 = ring2
                order6 = ring2
            else:
                ring5 = ring2
                order5 = ring2
                ring6 = ring1
                order6 = ring1

            # Check that the 5-membered ring:
            valid_ring5 = True
            for idx in ring5:
                atom = mol.GetAtomWithIdx(idx)
                # Must be carbon, not aromatic. (We allow any sp3 or even non-specified hybridization.)
                if atom.GetAtomicNum() != 6 or atom.GetIsAromatic():
                    valid_ring5 = False
                    break
            if not valid_ring5:
                continue

            # Check the 6-membered ring: count oxygen and carbon atoms.
            count_C = 0
            count_O = 0
            valid_ring6 = True
            for idx in ring6:
                atom = mol.GetAtomWithIdx(idx)
                # Disallow aromatic atoms.
                if atom.GetIsAromatic():
                    valid_ring6 = False
                    break
                if atom.GetAtomicNum() == 6:
                    count_C += 1
                elif atom.GetAtomicNum() == 8:
                    count_O += 1
                else:
                    valid_ring6 = False
                    break
            if not valid_ring6 or count_C != 5 or count_O != 1:
                continue

            # Check for exactly two shared atoms.
            shared_atoms = set(ring5).intersection(set(ring6))
            if len(shared_atoms) != 2:
                continue

            # Check that the two shared atoms are consecutive in both rings.
            shared_atoms = list(shared_atoms)
            if not (are_adjacent_in_ring(order5, shared_atoms[0], shared_atoms[1]) and
                    are_adjacent_in_ring(order6, shared_atoms[0], shared_atoms[1])):
                continue

            reason = ("Found fused bicyclic core: a 5-membered cyclopentane (nonaromatic, all C) and "
                      "a 6-membered oxygen heterocycle (1 O and 5 C, nonaromatic) share exactly 2 atoms, "
                      "with the shared atoms bonded in both rings.")
            return True, reason

    # Stage 2: Rescue for secoiridoids.
    # Look for any 5-membered ring made entirely of nonaromatic carbons.
    for ring in ring_info:
        if len(ring) != 5:
            continue
        if not all(mol.GetAtomWithIdx(idx).GetAtomicNum() == 6 and 
                   not mol.GetAtomWithIdx(idx).GetIsAromatic()
                   for idx in ring):
            continue
        
        # For each atom in the ring, check exocyclic bonds that are carbonyls.
        carbonyl_count = 0
        # Use a set to avoid double-counting the same substituent.
        counted_substituents = set()
        for idx in ring:
            atom = mol.GetAtomWithIdx(idx)
            for nbr in atom.GetNeighbors():
                if nbr.GetIdx() in ring:
                    continue
                bond = mol.GetBondBetweenAtoms(idx, nbr.GetIdx())
                if bond is None or bond.GetBondType() != Chem.BondType.DOUBLE:
                    continue
                # The neighbor should be a carbon that is doubly bound to oxygen.
                if nbr.GetAtomicNum() != 6:
                    continue
                for nbr2 in nbr.GetNeighbors():
                    if nbr2.GetIdx() == idx:
                        continue
                    bond2 = mol.GetBondBetweenAtoms(nbr.GetIdx(), nbr2.GetIdx())
                    if bond2 is not None and bond2.GetBondType() == Chem.BondType.DOUBLE and nbr2.GetAtomicNum() == 8:
                        # Count only if this exocyclic carbon (nbr) has not been already counted.
                        if nbr.GetIdx() not in counted_substituents:
                            carbonyl_count += 1
                            counted_substituents.add(nbr.GetIdx())
                        break  # count each substituent only once
        if carbonyl_count >= 2:
            reason = ("Found cyclopentane ring (all nonaromatic C) with {} exocyclic carbonyl substituents, "
                      "suggestive of a secoiridoid skeleton.".format(carbonyl_count))
            return True, reason

    return False, "No fused iridoid or secoiridoid core detected based on our heuristics."

# Example usage for testing:
if __name__ == "__main__":
    examples = [
        # True positive examples (should be classified as iridoid monoterpenoid)
        ("O1C(OC)C2C([C@H](OC)C[C@@]2(O)C)CC1OC", "Mioporosidegenin"),
        ("O1[C@@H]2C=C(CC[C@]23[C@@H](CC[C@H]3C)[C@](C1)(O)C)C", "Cordycepol A"),
        # Secoiridoid rescue example:
        ("CC1CCC(C(C)C=O)C1C=O", "iridodial"),
        # Examples known to be iridoid monoterpenoids / secoiridoids (false negatives previously):
        ("[C@@H]1([C@@H]([C@H]([C@@H]([C@H](O1)CO)O)O)O)O[C@H]2/C(/[C@](C(=CO2)C(=O)OC)([H])CC(=O)OCCC=3C=CC(=C(C3)O)O)=C/C", "oleuropein"),
        ("[C@]12([C@@]([C@H](CC1)C)(C(OC=C2C)=O)[H])[H]", "cis-trans-nepetalactone"),
    ]
    
    for smi, name in examples:
        flag, msg = is_iridoid_monoterpenoid(smi)
        print(f"{name}: {flag} => {msg}")


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:50563',
                          'name': 'iridoid monoterpenoid',
                          'definition': 'One of a class of monoterpenoids '
                                        'biosynthesized from isoprene and '
                                        'often intermediates in the '
                                        'biosynthesis of alkaloids. Iridoids '
                                        'usually consist of a cyclopentane '
                                        'ring fused to a six-membered oxygen '
                                        'heterocycle; cleavage of a bond in '
                                        'the cyclopentane ring gives rise to '
                                        'the subclass known as secoiridoids.',
                          'parents': ['CHEBI:25409'],
                          'xrefs': ['Wikipedia:Iridoid'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 84,
                           'log_lines_of_code': 4.430816798843313,
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
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 0,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 3,
                                                 3,
                                                 3,
                                                 4,
                                                 2,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 3,
                                                 3,
                                                 3,
                                                 3,
                                                 4,
                                                 0,
                                                 0,
                                                 0,
                                                 0,
                                                 0,
                                                 0,
                                                 0,
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
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 3,
                                                 4,
                                                 5,
                                                 4,
                                                 4,
                                                 5,
                                                 4,
                                                 4,
                                                 5,
                                                 4,
                                                 5,
                                                 6,
                                                 5,
                                                 5,
                                                 6,
                                                 6,
                                                 7,
                                                 7,
                                                 6,
                                                 2,
                                                 3,
                                                 3,
                                                 3,
                                                 0,
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
                                                 1,
                                                 2,
                                                 2],
                           'max_indent': 7,
                           'imports': ['from rdkit import Chem'],
                           'imports_count': 1,
                           'methods_called': [   'GetIdx',
                                                 'GetAtomicNum',
                                                 'MolFromSmiles',
                                                 'GetAtomWithIdx',
                                                 'AtomRings',
                                                 'GetBondBetweenAtoms',
                                                 'GetNeighbors',
                                                 'add',
                                                 'format',
                                                 'GetBondType',
                                                 'GetRingInfo',
                                                 'GetIsAromatic'],
                           'methods_called_count': 12,
                           'smarts_strings': [],
                           'smarts_strings_count': 0,
                           'defs': [   'is_iridoid_monoterpenoid(smiles: str):',
                                       'are_adjacent_in_ring(ring_tuple, a, '
                                       'b):'],
                           'defs_count': 2,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "No rings found in the '
                                          'molecule"',
                                          'True',
                                          'False',
                                          'True, reason',
                                          'False, "No fused iridoid or '
                                          'secoiridoid core detected based on '
                                          'our heuristics."'],
                           'returns_count': 6,
                           'complexity': 6.286163359768663},
    'message': '\n'
               'Attempt failed: F1 score of 0.017467248908296946 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: O1C(OC)C2C([C@H](OC)C[C@@]2(O)C)CC1OC '
               'NAME: Mioporosidegenin REASON: CORRECT Found fused bicyclic '
               'core: a 5-membered cyclopentane (nonaromatic, sp3 carbons) and '
               'a 6-membered ring with one oxygen (5C+1O, nonaromatic) share '
               'exactly 2 atoms.\n'
               ' * SMILES: '
               'O1[C@@H]2C=C(CC[C@]23[C@@H](CC[C@H]3C)[C@](C1)(O)C)C NAME: '
               'Cordycepol A REASON: CORRECT Found fused bicyclic core: a '
               '5-membered cyclopentane (nonaromatic, sp3 carbons) and a '
               '6-membered ring with one oxygen (5C+1O, nonaromatic) share '
               'exactly 2 atoms.\n'
               'False positives: SMILES: '
               'OC12C(C3(C(C4(C(CC3)C(C(=O)CC4)(C)C)C)CC1)C)(CC5OC(CC(C25O)C)C(O)C(O)(C)C)C '
               'NAME: '
               '6-(1,2-dihydroxy-2-methylpropyl)-9,10-dihydroxy-1,2,8,14,18,18-hexamethyl-5-oxapentacyclo[11.8.0.02,10.04,9.014,19]henicosan-17-one '
               'REASON: WRONGLY CLASSIFIED Found fused bicyclic core: a '
               '5-membered cyclopentane (nonaromatic, sp3 carbons) and a '
               '6-membered ring with one oxygen (5C+1O, nonaromatic) share '
               'exactly 2 atoms.\n'
               ' * SMILES: '
               'O=C1C(O)=C(C2=CC=3C(=CC(=CC3O[C@]42[C@@]15[C@H]([C@@H](C)CO4)CC[C@H]5C)O)CO)C '
               'NAME: Rhodatin REASON: WRONGLY CLASSIFIED Found fused bicyclic '
               'core: a 5-membered cyclopentane (nonaromatic, sp3 carbons) and '
               'a 6-membered ring with one oxygen (5C+1O, nonaromatic) share '
               'exactly 2 atoms.\n'
               ' * SMILES: '
               'O=C1O[C@]2(O[C@H]3[C@@H]([C@]4(CCC5=C([C@@]4(C3)C)CC[C@@H]6[C@@]5(CC[C@H](C6(C)C)OC(=O)CC(=O)O)C)C)[C@@H](C2)C)C(=C1C)C '
               'NAME: Hexatenuin A REASON: WRONGLY CLASSIFIED Found fused '
               'bicyclic core: a 5-membered cyclopentane (nonaromatic, sp3 '
               'carbons) and a 6-membered ring with one oxygen (5C+1O, '
               'nonaromatic) share exactly 2 atoms.\n'
               ' * SMILES: '
               'O=C1OC([C@@H]2CCC=3[C@]4([C@@]5([C@@H]([C@@H]([C@]6(OC(=O)C(C)=CC6)OC5)C)CC4)CCC3C=C2C=C1)C)(C)C '
               'NAME: Ganodermalactone F REASON: WRONGLY CLASSIFIED Found '
               'fused bicyclic core: a 5-membered cyclopentane (nonaromatic, '
               'sp3 carbons) and a 6-membered ring with one oxygen (5C+1O, '
               'nonaromatic) share exactly 2 atoms.\n'
               ' * SMILES: '
               '[H][C@]12NC(=[NH2+])N[C@@]1(O)[C@@]1([H])[C@H](CNC(=O)c3cc(Br)c(Br)[nH]3)[C@@H](CNC(=O)c3cc(Br)c(Br)[nH]3)[C@H](O)[C@@]11NC(=[NH2+])N[C@@]1([H])O2 '
               'NAME: massadine(2+) REASON: WRONGLY CLASSIFIED Found fused '
               'bicyclic core: a 5-membered cyclopentane (nonaromatic, sp3 '
               'carbons) and a 6-membered ring with one oxygen (5C+1O, '
               'nonaromatic) share exactly 2 atoms.\n'
               ' * SMILES: '
               'O=C1[C@@]23C(=O)N[C@H]([C@@H]2[C@H](C)C(=C[C@@H]3C=C(CCCC([C@H]4[C@H]1[C@]56C7=C(C)C([C@]4(O)[C@]5(O[C@@H]8[C@H](O)CCC(C)=C[C@@H]9[C@]%10(C([C@@H]%11[C@@H]7O[C@@H]6[C@H]%118)=O)C(=O)N[C@H]([C@@H]%10[C@H](C)C(=C9)C)CC(C)C)O)=O)=O)C)C)CC(C)C '
               'NAME: Amichalasine B REASON: WRONGLY CLASSIFIED Found fused '
               'bicyclic core: a 5-membered cyclopentane (nonaromatic, sp3 '
               'carbons) and a 6-membered ring with one oxygen (5C+1O, '
               'nonaromatic) share exactly 2 atoms.\n'
               ' * SMILES: '
               'O=C(O[C@H]1[C@]2([C@@]3(O)[C@@H]([C@@H](OC)O[C@H]2OC)[C@H](C)C[C@@H]([C@H]3C1(C)C)O)C)C '
               'NAME: '
               '7a-acetoxy-15-methoxy-10-O-methyl-deacetyldihydrobotrydial '
               'REASON: WRONGLY CLASSIFIED Found fused bicyclic core: a '
               '5-membered cyclopentane (nonaromatic, sp3 carbons) and a '
               '6-membered ring with one oxygen (5C+1O, nonaromatic) share '
               'exactly 2 atoms.\n'
               ' * SMILES: '
               'O=C1OC2C3(C4(C5C(C(O)(C)CC4)CC3(O)C(C2)O5)COC(=O)C6C7(C(C(=CCC=C1)OCC7)O)O6)C '
               "NAME: 2',3'-Epoxymyrothecine A REASON: WRONGLY CLASSIFIED "
               'Found fused bicyclic core: a 5-membered cyclopentane '
               '(nonaromatic, sp3 carbons) and a 6-membered ring with one '
               'oxygen (5C+1O, nonaromatic) share exactly 2 atoms.\n'
               ' * SMILES: '
               'O=C1[C@@](O)(C[C@@H](C(O)=C2[C@@]34[C@H]1[C@@H](OC)[C@H]5[C@H](O)[C@@](O3)([C@@H](C)C[C@@]45OC2=O)C)C)C '
               'NAME: Abybetaomicin P REASON: WRONGLY CLASSIFIED Found fused '
               'bicyclic core: a 5-membered cyclopentane (nonaromatic, sp3 '
               'carbons) and a 6-membered ring with one oxygen (5C+1O, '
               'nonaromatic) share exactly 2 atoms.\n'
               ' * SMILES: '
               '[H][C@@]12C[C@@H](OC(=O)\\C=C/C)[C@@]3(C)[C@]1(O)CO[C@@]1([H])[C@H](O)C(C)=C[C@@]([H])(O2)[C@@]31C '
               'NAME: Trichothecene analogue REASON: WRONGLY CLASSIFIED Found '
               'fused bicyclic core: a 5-membered cyclopentane (nonaromatic, '
               'sp3 carbons) and a 6-membered ring with one oxygen (5C+1O, '
               'nonaromatic) share exactly 2 atoms.\n'
               ' * SMILES: '
               'O=C1OC[C@@]23[C@@]4([C@@]5(O)[C@H](O[C@@H]2[C@H](C(C)=CC3)C5)C[C@H]4OC(=O)C=CCC[C@]6([C@@H](C(=C1)CCO6)O)C(=O)C)C '
               'NAME: Myrothecine I REASON: WRONGLY CLASSIFIED Found fused '
               'bicyclic core: a 5-membered cyclopentane (nonaromatic, sp3 '
               'carbons) and a 6-membered ring with one oxygen (5C+1O, '
               'nonaromatic) share exactly 2 atoms.\n'
               ' * SMILES: '
               '[H][C@@]12C[C@@H](C)[C@]3([H])[C@@]4(C)CC[C@@]56C[C@@]55CC[C@H](O[C@]7([H])OC[C@@H](O)[C@H](O)[C@H]7O[C@]7([H])O[C@H](CO)[C@@H](O)[C@H](O)[C@H]7O)C(C)(C)[C@]5([H])CC[C@@]6([H])[C@]4(C)[C@@H](O)[C@]3(O[C@@H]1C(C)(C)O)O2 '
               'NAME: cimifoetiside B REASON: WRONGLY CLASSIFIED Found fused '
               'bicyclic core: a 5-membered cyclopentane (nonaromatic, sp3 '
               'carbons) and a 6-membered ring with one oxygen (5C+1O, '
               'nonaromatic) share exactly 2 atoms.\n'
               ' * SMILES: '
               'O=C1[C@H](C[C@H](C(O)=C2[C@]34[C@@H]1[C@H](O)C5[C@H](O)C(O3)[C@H](C)C[C@]45OC2=O)C)C '
               'NAME: Abybetaomicin K REASON: WRONGLY CLASSIFIED Found fused '
               'bicyclic core: a 5-membered cyclopentane (nonaromatic, sp3 '
               'carbons) and a 6-membered ring with one oxygen (5C+1O, '
               'nonaromatic) share exactly 2 atoms.\n'
               ' * SMILES: '
               'O=C(C=C(C)C)C[C@@H](C1=C[C@@H]2O[C@]3(C)C[C@@]4([C@@]15[C@]2(C[C@H]3[C@H]4C(CO)=CC5)C)O)C '
               'NAME: Bipolarolide A REASON: WRONGLY CLASSIFIED Found fused '
               'bicyclic core: a 5-membered cyclopentane (nonaromatic, sp3 '
               'carbons) and a 6-membered ring with one oxygen (5C+1O, '
               'nonaromatic) share exactly 2 atoms.\n'
               ' * SMILES: '
               'O=C1OC[C@]23[C@@]4([C@@]5(O)[C@H](O[C@@H]2[C@@H]([C@](O)(C)CC3)C5)C[C@H]4OC(=O)C=CCC[C@@]67[C@@H](C(=C1)CCO6)O[C@H](O)[C@@H]7O)C '
               'NAME: Dihydromyrothecine C REASON: WRONGLY CLASSIFIED Found '
               'fused bicyclic core: a 5-membered cyclopentane (nonaromatic, '
               'sp3 carbons) and a 6-membered ring with one oxygen (5C+1O, '
               'nonaromatic) share exactly 2 atoms.\n'
               ' * SMILES: '
               'O1C23OC(C1CC(C3C4(C(C=5C6(C7(C6)C(C(C(O[C@@H]8OC[C@@H](O)[C@H](O)[C@H]8O)CC7)(C)C)CC5)CC4)(C2O)C)C)C)C(O)(C)C '
               'NAME: '
               '(2S,3R,4S,5R)-2-[[2-hydroxy-22-(2-hydroxypropan-2-yl)-3,8,8,17,19-pentamethyl-23,24-dioxaheptacyclo[19.2.1.01,18.03,17.04,14.07,12.012,14]tetracos-4-en-9-yl]oxy]oxane-3,4,5-triol '
               'REASON: WRONGLY CLASSIFIED Found fused bicyclic core: a '
               '5-membered cyclopentane (nonaromatic, sp3 carbons) and a '
               '6-membered ring with one oxygen (5C+1O, nonaromatic) share '
               'exactly 2 atoms.\n'
               ' * SMILES: '
               'C[C@H]1[C@H]2[C@@H](C[C@@]3(C)[C@@H]4CC=C5[C@@H](C=C(O[C@@H]6O[C@H](CO)[C@@H](O)[C@H](O)[C@H]6O)C(=O)C5(C)C)[C@]4(C)C(=O)C[C@]23C)O[C@@]2(O)CC(C)(C)O[C@@]12O '
               'NAME: '
               '(16alpha,20S,22S,23S)-16,23:22,25-diepoxy-2,22,23-trihydroxycucurbita-1,5-diene-3,11-dione '
               '2-O-beta-D-glucopyranoside REASON: WRONGLY CLASSIFIED Found '
               'fused bicyclic core: a 5-membered cyclopentane (nonaromatic, '
               'sp3 carbons) and a 6-membered ring with one oxygen (5C+1O, '
               'nonaromatic) share exactly 2 atoms.\n'
               ' * SMILES: '
               'O=C1C(=C[C@H]2O[C@H]3[C@]4(CO[C@H]1[C@@]2([C@]4([C@H](OC(=O)C=CC)C3)C)C)O)C '
               'NAME: Trichothecrotocin K REASON: WRONGLY CLASSIFIED Found '
               'fused bicyclic core: a 5-membered cyclopentane (nonaromatic, '
               'sp3 carbons) and a 6-membered ring with one oxygen (5C+1O, '
               'nonaromatic) share exactly 2 atoms.\n'
               ' * SMILES: '
               'O=C1[C@@](O)(C[C@@H](C(O)=C2[C@@]34[C@H]1[C@@H](O)[C@H]5[C@H](O)[C@@](O3)([C@@H](CO)C[C@@]45OC2=O)C)C)C '
               'NAME: Abybetaomicin R REASON: WRONGLY CLASSIFIED Found fused '
               'bicyclic core: a 5-membered cyclopentane (nonaromatic, sp3 '
               'carbons) and a 6-membered ring with one oxygen (5C+1O, '
               'nonaromatic) share exactly 2 atoms.\n'
               ' * SMILES: '
               'O1C2C34C5(OC6C2C(C1C3=C(C(=O)C5(O)C7C4C(=O)C89C(C(NC8=O)CC(C)C)C(C(=CC9C=C(CCC(=O)C7=O)C)C)C)C)C(=O)C%10%11C(C(NC%10=O)CC(C)C)C(C(=CC%11C=C(CCC6O)C)C)C)O '
               'NAME: Amichalasine A REASON: WRONGLY CLASSIFIED Found fused '
               'bicyclic core: a 5-membered cyclopentane (nonaromatic, sp3 '
               'carbons) and a 6-membered ring with one oxygen (5C+1O, '
               'nonaromatic) share exactly 2 atoms.\n'
               ' * SMILES: '
               '[H][C@]1(OC[C@@H](O)[C@H](O)[C@H]1O)O[C@H]1CC[C@]23C[C@]22C[C@@H](OC(C)=O)[C@]4(C)[C@@]5([H])[C@H](C)C[C@@]6(OC[C@@]7(C)O[C@@]67[H])O[C@@]5([H])C[C@@]4(C)[C@]2([H])CC[C@@]3([H])C1(C)C '
               'NAME: 23-epi-26-deoxyactein REASON: WRONGLY CLASSIFIED Found '
               'fused bicyclic core: a 5-membered cyclopentane (nonaromatic, '
               'sp3 carbons) and a 6-membered ring with one oxygen (5C+1O, '
               'nonaromatic) share exactly 2 atoms.\n'
               ' * SMILES: '
               'S([C@H]1[C@@H]2[C@]34OC(=O)C(=C3O[C@@]([C@H]2O)(C)[C@H](C4)C)C(=O)CC[C@@H](C(C1)=O)C)[C@@H]5[C@H]6C(=O)[C@H](CCC(=C7[C@]68O[C@@]9([C@H]([C@H]5[C@@]8(OC7=O)C[C@@H]9C)O)C)O)C '
               'NAME: Neoabybetaomicin G REASON: WRONGLY CLASSIFIED Found '
               'fused bicyclic core: a 5-membered cyclopentane (nonaromatic, '
               'sp3 carbons) and a 6-membered ring with one oxygen (5C+1O, '
               'nonaromatic) share exactly 2 atoms.\n'
               ' * SMILES: '
               'O=C(O[C@@H]1[C@@H]2[C@@]3(O)[C@](CO[C@@H]([C@H]3[C@@H](C1)C)OCC4=C(C=CC5=C4[C@](CC5(C)C)(CO)C)C)(C)CC2(C)C)C '
               'NAME: Hypocriol F REASON: WRONGLY CLASSIFIED Found fused '
               'bicyclic core: a 5-membered cyclopentane (nonaromatic, sp3 '
               'carbons) and a 6-membered ring with one oxygen (5C+1O, '
               'nonaromatic) share exactly 2 atoms.\n'
               ' * SMILES: '
               'O1C23OC(CC(O)(C3C4C(C5(C(C6(C(CC5)C(C(OC7OCC(O)C(OC8OC(C(O)C(O)C8O)CO)C7OC9OC(C(O)C(O)C9O)C)CC6)(C)C)C)CC4)C)(C2)C1)C)C=C(C)C '
               'NAME: Hoduloside III REASON: WRONGLY CLASSIFIED Found fused '
               'bicyclic core: a 5-membered cyclopentane (nonaromatic, sp3 '
               'carbons) and a 6-membered ring with one oxygen (5C+1O, '
               'nonaromatic) share exactly 2 atoms.\n'
               ' * SMILES: '
               'CC(=O)O[C@@H]1[C@@H](CO)O[C@@H](O[C@H]2[C@@H](O)CO[C@@H](O[C@H]3CC[C@@]4(C)[C@@H](CC[C@]5(C)[C@@H]4CC[C@@H]4[C@@H]6[C@]7(C[C@@]54CO7)O[C@H](C[C@]6(C)O)C=C(C)C)C3(C)C)[C@@H]2OC(C)=O)[C@H](O)[C@H]1O[C@@H]1OC[C@@H](O)[C@H](O)[C@H]1O '
               'NAME: Colubrinoside REASON: WRONGLY CLASSIFIED Found fused '
               'bicyclic core: a 5-membered cyclopentane (nonaromatic, sp3 '
               'carbons) and a 6-membered ring with one oxygen (5C+1O, '
               'nonaromatic) share exactly 2 atoms.\n'
               'False negatives: SMILES: '
               '[H][C@]12C[C@H](C)[C@@H](CO[C@@H]3O[C@H](COC(=O)\\C=C\\c4ccc(O)c(O)c4)[C@@H](O)[C@H](O)[C@H]3O)[C@@]1([H])[C@H](CO)C(=O)O2 '
               "NAME: gelsemiol-6'-trans-caffeoyl-1-glucoside REASON: MISSED "
               'No fused iridoid or secoiridoid core detected based on our '
               'heuristics.\n'
               ' * SMILES: '
               '[C@@H]1([C@@H]([C@H]([C@@H]([C@H](O1)CO)O)O)O)O[C@H]2/C(/[C@](C(=CO2)C(=O)OC)([H])CC(=O)OCCC=3C=CC(=C(C3)O)O)=C/C '
               'NAME: oleuropein REASON: MISSED No fused iridoid or '
               'secoiridoid core detected based on our heuristics.\n'
               ' * SMILES: [C@]12([C@@]([C@H](CC1)C)(C(OC=C2C)=O)[H])[H] NAME: '
               'cis-trans-nepetalactone REASON: MISSED No fused iridoid or '
               'secoiridoid core detected based on our heuristics.\n'
               ' * SMILES: CC1CCC(C(C)C=O)C1C=O NAME: iridodial REASON: MISSED '
               'No fused iridoid or secoiridoid core detected based on our '
               'heuristics.\n'
               ' * SMILES: '
               'O[C@@]12[C@@]([C@@](O)([C@@H](OC(=O)/C=C/C3=CC=C(O)C=C3)C1)C)(C(OC=C2C(OC)=O)O[C@@H]4O[C@@H]([C@@H](O)[C@H](O)[C@H]4O)CO)[H] '
               'NAME: Methyl '
               '(1s,4ar,6s,7r,7as)-1-(beta-d-glucopyranosyloxy)-4a,7-dihydroxy-6-{[(2e)-3-(4-hydroxyphenyl)-2-propenoyl]oxy}-7-methyl-1,4a,5,6,7,7a-hexahydrocyclopenta[c]pyran-4-carboxylate '
               'REASON: MISSED No fused iridoid or secoiridoid core detected '
               'based on our heuristics.\n'
               ' * SMILES: '
               'O[C@H]1/C(/[C@](C(=CO1)C(=O)OC)([H])CC(=O)OCCC=2C=CC(=C(C2)O)O)=C/C '
               'NAME: oleuropein aglycone REASON: MISSED No fused iridoid or '
               'secoiridoid core detected based on our heuristics.\n'
               ' * SMILES: '
               'O=C(O)/C=C(/CC[C@@]1(C(=C(CO)[C@@H]([C@@]1(O)C)C)C)C)\\C NAME: '
               'Hisunic acid REASON: MISSED No fused iridoid or secoiridoid '
               'core detected based on our heuristics.\n'
               ' * SMILES: '
               'O=C(OC)CC/C(=C/C1C(O)CC2OCC(C(C2C1)/C=C/C(C)C)CCC=3OC=CC3)/C '
               'NAME: (4E)-methyl 13-((16-(furan-3-yl) '
               'ethyl)-octahydro-7-hydroxy-4-((E)-23-methylbut-21-enyl)-2H-chromen-6-yl)-4-methylpent-4-enoate '
               'REASON: MISSED No fused iridoid or secoiridoid core detected '
               'based on our heuristics.\n'
               ' * SMILES: '
               'O=C1NCCC[C@@H]2NC(=O)C(C2=O)=C(O)C=C[C@H]3[C@H](CC=C1)[C@H]4C=C[C@H]5[C@H](C(=O)C)[C@@H](C[C@@H]5[C@H]4C3)C '
               'NAME: Clifednamide A REASON: MISSED No fused iridoid or '
               'secoiridoid core detected based on our heuristics.\n'
               ' * SMILES: '
               '[H][C@@]12C=CO[C@@H](O[C@]3([H])O[C@H](CO)[C@@H](O)[C@H](O)[C@H]3O)[C@]1([H])C(COC(=O)C1=CC=C(O)C=C1)=C[C@H]2O '
               'NAME: agnuside REASON: MISSED No fused iridoid or secoiridoid '
               'core detected based on our heuristics.\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'O=C(N[C@@H](C(O)(C)C)C)[C@H]([C@@]1([C@@]2([C@@](CC1)(/C(/CCC2)=C/C=C\\3/C[C@@H](O)C[C@H](O)C3=C)[H])C)[H])C',
                                     'name': '1alpha,25-dihydroxy-24-oxo-23-azavitamin '
                                             'D2 / '
                                             '1alpha,25-dihydroxy-24-oxo-23-azaergocalciferol',
                                     'reason': 'No fused iridoid or '
                                               'secoiridoid core detected '
                                               'based on our heuristics.'},
                                 {   'smiles': 'CCCCCCCCCCCCCCCCCCC(O)C([O-])=O',
                                     'name': '2-hydroxyarachidate',
                                     'reason': 'No rings found in the '
                                               'molecule'},
                                 {   'smiles': 'C[C@@H](CN([C@@H](C)CO)C(=O)NC1=CC=C(C=C1)C(F)(F)F)[C@@H](CN(C)C(=O)C2CCOCC2)OC',
                                     'name': 'N-[(2S,3S)-4-[[(2S)-1-hydroxypropan-2-yl]-[[4-(trifluoromethyl)phenyl]carbamoyl]amino]-2-methoxy-3-methylbutyl]-N-methyloxane-4-carboxamide',
                                     'reason': 'No fused iridoid or '
                                               'secoiridoid core detected '
                                               'based on our heuristics.'},
                                 {   'smiles': 'CC(=O)CC\\C=C(/C)CCC=C(C)C',
                                     'name': 'geranyl acetone',
                                     'reason': 'No rings found in the '
                                               'molecule'},
                                 {   'smiles': 'O([C@H]1[C@H](O)[C@H](O[C@H](O)[C@H]1O)CO[C@H]2O[C@@H]([C@@H](O)[C@H](O)[C@@H]2O)CO)[C@H]3O[C@@H]([C@@H](O)[C@H](O)[C@@H]3O[C@H]4O[C@@H]([C@@H](O)[C@H](O)[C@@H]4O)CO)CO',
                                     'name': '(2S,3S,4S,5S,6R)-2-[[(2R,3R,4S,5S,6S)-4-[(2R,3S,4S,5S,6R)-4,5-Dihydroxy-6-(hydroxymethyl)-3-[(2R,3S,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-3,5,6-trihydroxyoxan-2-yl]methoxy]-6-(hydroxymethyl)oxane-3,4,5-triol',
                                     'reason': 'No fused iridoid or '
                                               'secoiridoid core detected '
                                               'based on our heuristics.'},
                                 {   'smiles': 'O=C(OC1=C(C(O)=C(C(=O)O)C(=C1C)C)C)C2=C(OC)C(=C(OC(=O)C3=C(O)C=C(O)C=C3C)C=C2C)C',
                                     'name': 'Thielavin Z5',
                                     'reason': 'No fused iridoid or '
                                               'secoiridoid core detected '
                                               'based on our heuristics.'},
                                 {   'smiles': '[C@@H]1([C@@H]([C@H]([C@@H]([C@H](O1)CO)O)O)NC(C)=O)O[C@@H]2[C@@H]([C@H](C(O[C@@H]2CO)O)O)O',
                                     'name': 'beta-D-GlcpNAc-(1->4)-D-Galp',
                                     'reason': 'No fused iridoid or '
                                               'secoiridoid core detected '
                                               'based on our heuristics.'},
                                 {   'smiles': 'CN(C)C(=O)C1=CC=C(C=C1)C2=CC=C(C=C2)[C@@H]3[C@H]4CN(CC(=O)N4[C@H]3CO)C(=O)CC5CC5',
                                     'name': '4-[4-[(6S,7R,8R)-4-(2-cyclopropyl-1-oxoethyl)-8-(hydroxymethyl)-2-oxo-1,4-diazabicyclo[4.2.0]octan-7-yl]phenyl]-N,N-dimethylbenzamide',
                                     'reason': 'No fused iridoid or '
                                               'secoiridoid core detected '
                                               'based on our heuristics.'},
                                 {   'smiles': 'CCCCCCCCCCCCCCCCCCCCC=C',
                                     'name': '1-docosene',
                                     'reason': 'No rings found in the '
                                               'molecule'},
                                 {   'smiles': 'C([C@@](OC(=O)CCC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)([H])COC(=O)CC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)OC(=O)CCCCC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC',
                                     'name': 'TG(22:5(7Z,10Z,13Z,16Z,19Z)/20:5(5Z,8Z,11Z,14Z,17Z)/22:6(4Z,7Z,10Z,13Z,16Z,19Z))[iso6]',
                                     'reason': 'No rings found in the '
                                               'molecule'}],
    'sample_false_negatives': [   {   'smiles': '[H][C@]12C[C@H](C)[C@@H](CO[C@@H]3O[C@H](COC(=O)\\C=C\\c4ccc(O)c(O)c4)[C@@H](O)[C@H](O)[C@H]3O)[C@@]1([H])[C@H](CO)C(=O)O2',
                                      'name': "gelsemiol-6'-trans-caffeoyl-1-glucoside",
                                      'reason': 'No fused iridoid or '
                                                'secoiridoid core detected '
                                                'based on our heuristics.'},
                                  {   'smiles': '[C@@H]1([C@@H]([C@H]([C@@H]([C@H](O1)CO)O)O)O)O[C@H]2/C(/[C@](C(=CO2)C(=O)OC)([H])CC(=O)OCCC=3C=CC(=C(C3)O)O)=C/C',
                                      'name': 'oleuropein',
                                      'reason': 'No fused iridoid or '
                                                'secoiridoid core detected '
                                                'based on our heuristics.'},
                                  {   'smiles': 'CC1CCC(C(C)C=O)C1C=O',
                                      'name': 'iridodial',
                                      'reason': 'No fused iridoid or '
                                                'secoiridoid core detected '
                                                'based on our heuristics.'},
                                  {   'smiles': 'O[C@H]1/C(/[C@](C(=CO1)C(=O)OC)([H])CC(=O)OCCC=2C=CC(=C(C2)O)O)=C/C',
                                      'name': 'oleuropein aglycone',
                                      'reason': 'No fused iridoid or '
                                                'secoiridoid core detected '
                                                'based on our heuristics.'},
                                  {   'smiles': 'O=C(O)/C=C(/CC[C@@]1(C(=C(CO)[C@@H]([C@@]1(O)C)C)C)C)\\C',
                                      'name': 'Hisunic acid',
                                      'reason': 'No fused iridoid or '
                                                'secoiridoid core detected '
                                                'based on our heuristics.'},
                                  {   'smiles': 'O=C(OC)CC/C(=C/C1C(O)CC2OCC(C(C2C1)/C=C/C(C)C)CCC=3OC=CC3)/C',
                                      'name': '(4E)-methyl '
                                              '13-((16-(furan-3-yl) '
                                              'ethyl)-octahydro-7-hydroxy-4-((E)-23-methylbut-21-enyl)-2H-chromen-6-yl)-4-methylpent-4-enoate',
                                      'reason': 'No fused iridoid or '
                                                'secoiridoid core detected '
                                                'based on our heuristics.'},
                                  {   'smiles': 'O=C1NCCC[C@@H]2NC(=O)C(C2=O)=C(O)C=C[C@H]3[C@H](CC=C1)[C@H]4C=C[C@H]5[C@H](C(=O)C)[C@@H](C[C@@H]5[C@H]4C3)C',
                                      'name': 'Clifednamide A',
                                      'reason': 'No fused iridoid or '
                                                'secoiridoid core detected '
                                                'based on our heuristics.'},
                                  {   'smiles': 'O=C1[C@H](C([C@@H](C1)CC(O)O)(C)C)C',
                                      'name': '(2s,4s)-Alpha-Campholinic Acid',
                                      'reason': 'No fused iridoid or '
                                                'secoiridoid core detected '
                                                'based on our heuristics.'},
                                  {   'smiles': 'C12=C3[C@H]([C@@H]4C(CC[C@@]4(C3)C)(C)C)CC[C@]1([C@H](C)CC2)C',
                                      'name': 'Cattleyene',
                                      'reason': 'No fused iridoid or '
                                                'secoiridoid core detected '
                                                'based on our heuristics.'},
                                  {   'smiles': 'O=C1C2=C3C(=C(O)[C@@]4(O)C(C)(C)[C@H](CC4=C3C(C2=O)=O)C)C(=C1)C',
                                      'name': 'Peniciphenalenin A',
                                      'reason': 'No fused iridoid or '
                                                'secoiridoid core detected '
                                                'based on our heuristics.'}],
    'attempt': 4,
    'reasoning': 'Below is our reasoning and the new code. In our analysis of '
                 'the previous solution we noted that the “fused bicyclic '
                 'core” detection was too “loose” so that many large, complex '
                 'molecules ended up having two rings that incidentally share '
                 'two atoms even though they are not true iridoid cores. In '
                 'addition the ordering of the shared atoms (that is, that the '
                 'shared bond really belongs to both fused rings) was not '
                 'confirmed. We therefore take two steps:\n'
                 '  \n'
                 '1. In Stage 1 we iterate over all pairs of rings (from '
                 'RDKit’s GetRingInfo) where one ring is 5‑membered '
                 '(cyclopentane) and the other is 6‑membered '
                 '(tetrahydropyran). In addition to checking that the '
                 'five‐ring contains only nonaromatic carbons and that the '
                 'six‐ring contains exactly one oxygen (and otherwise carbons, '
                 'and no aromatics), we also check that the two shared atoms '
                 '(exactly two) appear as a bonded pair (i.e. consecutive in '
                 'the ring order) in both rings.\n'
                 '  \n'
                 '2. In Stage 2 we “rescue” secoiridoid candidates. That is, '
                 'we search for a 5‑membered nonaromatic (all‐carbon) ring '
                 '(candidate cyclopentane) that carries at least two exocyclic '
                 'carbonyl substituents (which we identify by a double bond '
                 'from a ring carbon to an exocyclic carbon that itself is '
                 'doubly bonded to oxygen).\n'
                 '\n'
                 'Below is the complete code block in Python.\n'
                 '\n'
                 '------------------------------------------------',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 48,
    'num_false_positives': 371,
    'num_true_negatives': 141820,
    'num_false_negatives': 61,
    'num_negatives': None,
    'precision': 0.11455847255369929,
    'recall': 0.44036697247706424,
    'f1': 0.1818181818181818,
    'accuracy': 0.996964160224877,
    'negative_predictive_value': 0.9995700622352535}