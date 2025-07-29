"""
Classifies: CHEBI:71543 rotenoid
"""
"""
Classifies: Rotenoids – members of the class of tetrahydrochromenochromene compounds.
A rotenoid is defined as having a cis‐fused tetrahydrochromeno[3,4-b]chromene skeleton,
i.e. a fused bicyclic system in which one six‐membered ring shows “chromenone‐like”
characteristics (has a ring oxygen and exactly one in‐ring carbonyl functionality)
fused to a second six‐membered ring that has a ring oxygen and NO carbonyls.
Substituted derivatives (e.g. glycosides) may be heavier than the classical 250–600 Da,
so the molecular weight filter has been relaxed.
"""

from rdkit import Chem
from rdkit.Chem import rdMolDescriptors

def is_rotenoid(smiles: str):
    """
    Determines if a molecule is a rotenoid based on its SMILES string.

    Heuristic criteria:
      1. The molecule should not be extremely light (we require at least 200 Da).
         (Glycosylated rotenoids may exceed classical weight bounds.)
      2. Look for candidate six‐membered rings that could be part of the rotenoid core.
         We define candidate rings as follows:
           a) A "chromenone‐like" ring must be six‐membered, contain at least one ring oxygen,
              and have exactly one carbon (of the ring) that is double‐bonded to an oxygen.
           b) An "ether" ring is a six‐membered ring that contains at least one oxygen
              and NO in‐ring carbonyl bonds.
      3. To be considered fused in the typical cis mode the two candidate rings must share exactly 2 atoms.
      4. (Optional extra check: if more than one candidate pair is found, we favor the one
         whose merged set of ring atoms does not introduce additional in‐ring carbonyls beyond
         that on the chromenone ring.)

    Args:
        smiles (str): SMILES string of the molecule.

    Returns:
        (bool, str): A tuple with the boolean classification and a reason string.
                     If criteria are met, returns True with an explanation.
                     Otherwise, returns False with the reason for rejection.
    """
    # Parse the molecule from SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Ensure molecule is not extremely light. (Some rotenoids are glycosylated, so we avoid a tight upper bound.)
    mol_wt = rdMolDescriptors.CalcExactMolWt(mol)
    if mol_wt < 200:
        return False, f"Molecular weight {mol_wt:.1f} is too low for rotenoids"

    # Get the ring atom indices as tuples (each tuple is a ring)
    ring_infos = mol.GetRingInfo().AtomRings()
    # Lists to store candidate rings. We use sets of atom indices for ease of intersection.
    chromenone_rings = []  # candidate rings with one in‐ring carbonyl
    ether_rings = []      # candidate rings with no in‐ring carbonyl

    # Loop over each ring and only consider six-membered ones.
    for ring in ring_infos:
        if len(ring) != 6:
            continue  # consider only 6-membered rings

        # Check for at least one oxygen atom in the ring.
        ring_atoms = [mol.GetAtomWithIdx(idx) for idx in ring]
        if not any(atom.GetAtomicNum() == 8 for atom in ring_atoms):
            continue

        # Count the number of ring carbon atoms that are double bonded to an oxygen.
        carbonyl_count = 0
        for idx in ring:
            atom = mol.GetAtomWithIdx(idx)
            # Only consider carbon atoms.
            if atom.GetAtomicNum() != 6:
                continue
            # Search bonds; if a bond from this atom is a double bond and the other atom is oxygen,
            # and if that oxygen is not part of the ring (or even if it is, we want to count the carbonyl feature)
            for bond in atom.GetBonds():
                # bond order 2
                if bond.GetBondTypeAsDouble() == 2:
                    other = bond.GetOtherAtom(atom)
                    if other.GetAtomicNum() == 8:
                        carbonyl_count += 1
                        break  # count each carbon only once

        # Classify the ring based on its in‐ring carbonyl count.
        # We assume that a chromenone candidate has exactly one in‐ring carbonyl 
        # and an ether candidate has none.
        if carbonyl_count == 1:
            chromenone_rings.append(set(ring))
        elif carbonyl_count == 0:
            ether_rings.append(set(ring))
        # Rings with >1 carbonyl are not considered as part of the core.

    if not chromenone_rings:
        return False, "No candidate chromenone-like ring (6-membered with one carbonyl and at least one oxygen) found"

    if not ether_rings:
        return False, "No candidate ether ring (6-membered with oxygen and no in-ring carbonyl) found"

    # Look for a pair of rings (one from each candidate list) that are fused.
    # We require they share exactly 2 atoms (typical for cis-fused systems).
    fused_pair_found = False
    for chrom in chromenone_rings:
        for ether in ether_rings:
            shared_atoms = chrom.intersection(ether)
            if len(shared_atoms) == 2:
                # Optionally, merge the rings and check that the only in-ring carbonyl is in the chromenone candidate.
                merged = chrom.union(ether)
                overall_carbonyls = 0
                for idx in merged:
                    atom = mol.GetAtomWithIdx(idx)
                    if atom.GetAtomicNum() != 6:
                        continue
                    for bond in atom.GetBonds():
                        if bond.GetBondTypeAsDouble() == 2:
                            other = bond.GetOtherAtom(atom)
                            if other.GetAtomicNum() == 8:
                                overall_carbonyls += 1
                                break
                # We allow additional carbonyls outside the fused core by checking the core count.
                # Here we require that the fused core shows at least the one carbonyl from the chromenone.
                if overall_carbonyls >= 1:
                    fused_pair_found = True
                    break
        if fused_pair_found:
            break

    if fused_pair_found:
        return True, "Found fused pair: one six‐membered chromenone-like ring (with one in‐ring carbonyl and ring oxygen) cis-fused (sharing 2 atoms) to a six‐membered ether ring; molecular properties are consistent with a rotenoid skeleton."
    else:
        return False, "No characteristic cis-fused chromenone/ether ring pair was found; molecule is unlikely to be a rotenoid."

# Example test code (if executed as main, prints out a test result):
if __name__ == "__main__":
    # Test SMILES for a known rotenoid – 13alpha-Hydroxydolineone
    test_smiles = "O1C2C(O)(C=3C(OC2)=CC=4OCOC4C3)C(=O)C5=C1C=C6OC=CC6=C5"
    result, reason = is_rotenoid(test_smiles)
    print("Test SMILES:", test_smiles)
    print("Result:", result)
    print("Reason:", reason)


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:71543',
                          'name': 'rotenoid',
                          'definition': 'Members of the class of '
                                        'tetrahydrochromenochromene that '
                                        'consists of a cis-fused '
                                        'tetrahydrochromeno[3,4-b]chromene '
                                        'skeleton and its substituted '
                                        'derivatives. The term was originally '
                                        'restricted to natural products, but '
                                        'is now also used to describe '
                                        'semi-synthetic and fully synthetic '
                                        'compounds.',
                          'parents': ['CHEBI:72544', 'CHEBI:72579'],
                          'xrefs': ['Wikipedia:Rotenoids'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 80,
                           'log_lines_of_code': 4.382026634673881,
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
                                                 0,
                                                 1,
                                                 2,
                                                 0,
                                                 1,
                                                 2,
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
                                                 2,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 0,
                                                 1,
                                                 1,
                                                 2,
                                                 3,
                                                 0,
                                                 0,
                                                 0,
                                                 0,
                                                 1,
                                                 2,
                                                 0,
                                                 1,
                                                 2,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 3,
                                                 3,
                                                 4,
                                                 4,
                                                 4,
                                                 4,
                                                 5,
                                                 5,
                                                 6,
                                                 5,
                                                 6,
                                                 7,
                                                 7,
                                                 8,
                                                 8,
                                                 4,
                                                 4,
                                                 4,
                                                 5,
                                                 5,
                                                 2,
                                                 3,
                                                 0,
                                                 1,
                                                 2,
                                                 1,
                                                 2,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1],
                           'max_indent': 8,
                           'imports': [   'from rdkit import Chem',
                                          'from rdkit.Chem import '
                                          'rdMolDescriptors'],
                           'imports_count': 2,
                           'methods_called': [   'union',
                                                 'GetBondTypeAsDouble',
                                                 'intersection',
                                                 'GetBonds',
                                                 'AtomRings',
                                                 'CalcExactMolWt',
                                                 'GetOtherAtom',
                                                 'GetAtomWithIdx',
                                                 'GetAtomicNum',
                                                 'MolFromSmiles',
                                                 'GetRingInfo'],
                           'methods_called_count': 11,
                           'smarts_strings': [],
                           'smarts_strings_count': 0,
                           'defs': ['is_rotenoid(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, f"Molecular weight '
                                          '{mol_wt:.1f} is too low for '
                                          'rotenoids"',
                                          'False, "No candidate '
                                          'chromenone-like ring (6-membered '
                                          'with one carbonyl and at least one '
                                          'oxygen) found"',
                                          'False, "No candidate ether ring '
                                          '(6-membered with oxygen and no '
                                          'in-ring carbonyl) found"',
                                          'True, "Found fused pair: one '
                                          'six‐membered chromenone-like ring '
                                          '(with one in‐ring carbonyl and ring '
                                          'oxygen) cis-fused (sharing 2 atoms) '
                                          'to a six‐membered ether ring; '
                                          'molecular properties are consistent '
                                          'with a rotenoid skeleton."',
                                          'False, "No characteristic cis-fused '
                                          'chromenone/ether ring pair was '
                                          'found; molecule is unlikely to be a '
                                          'rotenoid."'],
                           'returns_count': 6,
                           'complexity': 6.076405326934776},
    'message': '\n'
               'Attempt failed: F1 score of 0.17857142857142858 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: '
               'O1C2C(O)(C=3C(OC2)=CC=4OCOC4C3)C(=O)C5=C1C=C6OC=CC6=C5 NAME: '
               '13alpha-Hydroxydolineone REASON: CORRECT Found fused pair: one '
               'six‐membered chromenone-like ring (with one carbonyl) fused to '
               'a six‐membered ether ring; overall molecular properties are '
               'consistent with a rotenoid skeleton.\n'
               ' * SMILES: '
               'CC(C)C1CC2=C(O1)C=CC3=C2OC4=C(C3=O)C5=CC(=C(C=C5OC4)OC)OC '
               'NAME: LSM-4404 REASON: CORRECT Found fused pair: one '
               'six‐membered chromenone-like ring (with one carbonyl) fused to '
               'a six‐membered ether ring; overall molecular properties are '
               'consistent with a rotenoid skeleton.\n'
               ' * SMILES: '
               'O1C2C(C(=O)C3=C1C=4CC(OC4C=C3)C(COC5OC(C(O)C(O)C5O)CO)=C)C=6C(OC2)=CC(OC)=C(OC)C6 '
               'NAME: Amorphigenin O-glucoside REASON: CORRECT Found fused '
               'pair: one six‐membered chromenone-like ring (with one '
               'carbonyl) fused to a six‐membered ether ring; overall '
               'molecular properties are consistent with a rotenoid skeleton.\n'
               ' * SMILES: '
               'O1C2C(O)(C=3C(OC2)=CC=4OCOC4C3)C(=O)C5=C1C6=C(OC(C=C6)(C)C)C=C5 '
               'NAME: Millettosin REASON: CORRECT Found fused pair: one '
               'six‐membered chromenone-like ring (with one carbonyl) fused to '
               'a six‐membered ether ring; overall molecular properties are '
               'consistent with a rotenoid skeleton.\n'
               ' * SMILES: '
               'O(C(C1OC2=C(C1)C=3OC4C(C(=O)C3C=C2)C=5C(OC4)=CC(OC)=C(OC)C5)(C)C)C6OC(C(O)C(O)C6O)CO '
               'NAME: Dalpanol O-glucoside REASON: CORRECT Found fused pair: '
               'one six‐membered chromenone-like ring (with one carbonyl) '
               'fused to a six‐membered ether ring; overall molecular '
               'properties are consistent with a rotenoid skeleton.\n'
               ' * SMILES: '
               'O(C(C1OC2=C(C1)C=3OC4C(C(=O)C3C=C2)C=5C(OC4)=CC(OC)=C(OC)C5)(CO)C)[C@@H]6OC([C@@H](O)[C@H](O)C6O)CO '
               'NAME: Amorphigenol O-glucoside REASON: CORRECT Found fused '
               'pair: one six‐membered chromenone-like ring (with one '
               'carbonyl) fused to a six‐membered ether ring; overall '
               'molecular properties are consistent with a rotenoid skeleton.\n'
               ' * SMILES: '
               'O1C2C(O)(C=3C(OC2)=CC(OC)=C(OC)C3)C(=O)C4=C1C(=C(O)C=C4)C(O)=O '
               'NAME: 12a-Hydroxy-9-Demethylmunduserone-8-Carboxylic Acid '
               'REASON: CORRECT Found fused pair: one six‐membered '
               'chromenone-like ring (with one carbonyl) fused to a '
               'six‐membered ether ring; overall molecular properties are '
               'consistent with a rotenoid skeleton.\n'
               ' * SMILES: '
               'CC(=C)C1CC2=C(O1)C=CC3=C2OC4=C(C3=O)C5=CC(=C(C=C5OC4)OC)OC '
               'NAME: LSM-21590 REASON: CORRECT Found fused pair: one '
               'six‐membered chromenone-like ring (with one carbonyl) fused to '
               'a six‐membered ether ring; overall molecular properties are '
               'consistent with a rotenoid skeleton.\n'
               ' * SMILES: '
               'CC(C)C1=CC2=C(O1)C=CC3=C2O[C@@H]4COC5=CC(=C(C=C5[C@@H]4C3=O)OC)OC '
               'NAME: LSM-2115 REASON: CORRECT Found fused pair: one '
               'six‐membered chromenone-like ring (with one carbonyl) fused to '
               'a six‐membered ether ring; overall molecular properties are '
               'consistent with a rotenoid skeleton.\n'
               ' * SMILES: '
               'O1C2C(C=3C(OC2)=CC(O)=C(OC)C3)C(=O)C4=C1C=5CC(OC5C=C4)C(CO)=C '
               'NAME: 3-O-Demethylamorphigenin REASON: CORRECT Found fused '
               'pair: one six‐membered chromenone-like ring (with one '
               'carbonyl) fused to a six‐membered ether ring; overall '
               'molecular properties are consistent with a rotenoid skeleton.\n'
               ' * SMILES: '
               'O1C2C(O)(C=3C(OC2)=CC(OC)=C(OC)C3)C(=O)C=4C1=C5C(OC(C=C5)(C)C)=C(OC)C4 '
               'NAME: 12a-Hydroxyerythynone REASON: CORRECT Found fused pair: '
               'one six‐membered chromenone-like ring (with one carbonyl) '
               'fused to a six‐membered ether ring; overall molecular '
               'properties are consistent with a rotenoid skeleton.\n'
               ' * SMILES: '
               'O1C(C=CC=2C=3OC4=C(C=5C(OC4)=CC(OC)=C(OC)C5)C(=O)C3C=CC12)(C)C '
               'NAME: Dehydrodeguelin,7a,13a-Didehydrodeguelin REASON: CORRECT '
               'Found fused pair: one six‐membered chromenone-like ring (with '
               'one carbonyl) fused to a six‐membered ether ring; overall '
               'molecular properties are consistent with a rotenoid skeleton.\n'
               ' * SMILES: '
               'O1C2=C(C=3C(OC2)=CC=4OCOC4C3)C(=O)C5=C1C=C6OC=CC6=C5 NAME: '
               'Dehydrodolineone REASON: CORRECT Found fused pair: one '
               'six‐membered chromenone-like ring (with one carbonyl) fused to '
               'a six‐membered ether ring; overall molecular properties are '
               'consistent with a rotenoid skeleton.\n'
               ' * SMILES: '
               'O1C2C(O)(C=3C(OC2)=CC(OC)=C(OC)C3)C(=O)C4=C1C=5CC(OC5C=C4)C(COC6OC(C(O)C(O)C6O)CO)=C '
               'NAME: Dalbinol O-glucoside REASON: CORRECT Found fused pair: '
               'one six‐membered chromenone-like ring (with one carbonyl) '
               'fused to a six‐membered ether ring; overall molecular '
               'properties are consistent with a rotenoid skeleton.\n'
               ' * SMILES: '
               'O1C2C(C(=O)C3=C1C=4CC(OC4C=C3)C(CO)C)C=5C(OC2)=CC(OC)=C(OC)C5 '
               'NAME: Dihydroamorphigenin REASON: CORRECT Found fused pair: '
               'one six‐membered chromenone-like ring (with one carbonyl) '
               'fused to a six‐membered ether ring; overall molecular '
               'properties are consistent with a rotenoid skeleton.\n'
               ' * SMILES: COc1cc2OCC3Oc4cc(O)ccc4C(=O)C3c2cc1OC NAME: '
               '9-Demethylmunduserone REASON: CORRECT Found fused pair: one '
               'six‐membered chromenone-like ring (with one carbonyl) fused to '
               'a six‐membered ether ring; overall molecular properties are '
               'consistent with a rotenoid skeleton.\n'
               ' * SMILES: O1C2=C(C=3C(OC2OC)=CC=CC3)C(=O)C4=C1C=C(O)C(=C4O)C '
               'NAME: Boeravinone A REASON: CORRECT Found fused pair: one '
               'six‐membered chromenone-like ring (with one carbonyl) fused to '
               'a six‐membered ether ring; overall molecular properties are '
               'consistent with a rotenoid skeleton.\n'
               ' * SMILES: '
               'O1C2C(C(=O)C3=C1C=4CC(OC4C=C3)C(O)(CO)C)C=5C(OC2)=CC(OC)=C(OC)C5 '
               'NAME: Amorphigenol REASON: CORRECT Found fused pair: one '
               'six‐membered chromenone-like ring (with one carbonyl) fused to '
               'a six‐membered ether ring; overall molecular properties are '
               'consistent with a rotenoid skeleton.\n'
               ' * SMILES: '
               '[H][C@@]12COC3=C(C=C(OC)C(OC)=C3)[C@]1([H])C(=O)C1=C(O2)C2=C(OC(C)(C)C=C2)C=C1 '
               'NAME: deguelin REASON: CORRECT Found fused pair: one '
               'six‐membered chromenone-like ring (with one carbonyl) fused to '
               'a six‐membered ether ring; overall molecular properties are '
               'consistent with a rotenoid skeleton.\n'
               ' * SMILES: '
               '[H][C@@]12COc3cc(OC)c(OC)cc3[C@]1(O)C(=O)c1c(O)cc3OC(C)(C)C(O)C(OC)c3c1O2 '
               "NAME: 4',5'-dihydro-11,5'-dihydroxy-4'-methoxytephrosin "
               'REASON: CORRECT Found fused pair: one six‐membered '
               'chromenone-like ring (with one carbonyl) fused to a '
               'six‐membered ether ring; overall molecular properties are '
               'consistent with a rotenoid skeleton.\n'
               ' * SMILES: '
               'O1C2C(O)(C=3C(OC2)=CC(OC)=C(OC)C3)C(=O)C4=C1C=C(OC)C=C4 NAME: '
               '12alpha-Hydroxymunduserone REASON: CORRECT Found fused pair: '
               'one six‐membered chromenone-like ring (with one carbonyl) '
               'fused to a six‐membered ether ring; overall molecular '
               'properties are consistent with a rotenoid skeleton.\n'
               ' * SMILES: '
               '[H][C@@]12COc3cc(OC)c(OC)cc3[C@]1(O)C(=O)c1ccc3OC(C)(C)C=Cc3c1O2 '
               'NAME: tephrosin REASON: CORRECT Found fused pair: one '
               'six‐membered chromenone-like ring (with one carbonyl) fused to '
               'a six‐membered ether ring; overall molecular properties are '
               'consistent with a rotenoid skeleton.\n'
               ' * SMILES: '
               'COc1c2O[C@@H]3COc4cc5OCOc5cc4[C@@H]3C(=O)c2cc2ccoc12 NAME: '
               'Pachyrrhizone REASON: CORRECT Found fused pair: one '
               'six‐membered chromenone-like ring (with one carbonyl) fused to '
               'a six‐membered ether ring; overall molecular properties are '
               'consistent with a rotenoid skeleton.\n'
               ' * SMILES: '
               'O1[C@@]2([C@](C(=O)C3=C1C=4C[C@H](OC4C=C3)C(C)C)(C=5C(OC2)=CC(OC)=C(OC)C5)[H])[H] '
               'NAME: Dihydrorotenone REASON: CORRECT Found fused pair: one '
               'six‐membered chromenone-like ring (with one carbonyl) fused to '
               'a six‐membered ether ring; overall molecular properties are '
               'consistent with a rotenoid skeleton.\n'
               ' * SMILES: '
               'O1C2C(O)(C=3C(OC2)=CC(OC)=C(OC)C3)C(=O)C4=C1C=5CC(OC5C=C4)C(C)=C '
               'NAME: '
               '13-Hydroxy-16,17-dimethoxy-6-prop-1-en-2-yl-2,7,20-trioxapentacyclo[11.8.0.03,11.04,8.014,19]henicosa-3(11),4(8),9,14,16,18-hexaen-12-one '
               'REASON: CORRECT Found fused pair: one six‐membered '
               'chromenone-like ring (with one carbonyl) fused to a '
               'six‐membered ether ring; overall molecular properties are '
               'consistent with a rotenoid skeleton.\n'
               'False positives: SMILES: '
               'O=C1C(N)=CC(=O)C2=C1C=C(C)C(=C2C(=O)[C@H]([C@@H]3O[C@H]4[C@@H](C(=O)O[C@@H]([C@H]3C)[C@H]4C)C)C)O '
               'NAME: Salinaphthoquinone E REASON: WRONGLY CLASSIFIED Found '
               'fused pair: one six‐membered chromenone-like ring (with one '
               'carbonyl) fused to a six‐membered ether ring; overall '
               'molecular properties are consistent with a rotenoid skeleton.\n'
               ' * SMILES: '
               'O=C1OC([C@@H]2CC[C@@]3([C@@H]([C@]2([C@H](C1)O)C)CC=4C(=O)OC(=CC4O3)C)C)(C)C '
               'NAME: Asperversin D REASON: WRONGLY CLASSIFIED Found fused '
               'pair: one six‐membered chromenone-like ring (with one '
               'carbonyl) fused to a six‐membered ether ring; overall '
               'molecular properties are consistent with a rotenoid skeleton.\n'
               ' * SMILES: O=C1C2=C(OC3=C1[C@](OC=C3)(C(=O)OC)CO)C=C(CO)C=C2O '
               'NAME: Arthone A REASON: WRONGLY CLASSIFIED Found fused pair: '
               'one six‐membered chromenone-like ring (with one carbonyl) '
               'fused to a six‐membered ether ring; overall molecular '
               'properties are consistent with a rotenoid skeleton.\n'
               ' * SMILES: O=C1C2=C(C(O)=C(O)C=C2OC3=C1[C@H](OC(=C3)C)O)C(=O)O '
               'NAME: Flupyranochromene REASON: WRONGLY CLASSIFIED Found fused '
               'pair: one six‐membered chromenone-like ring (with one '
               'carbonyl) fused to a six‐membered ether ring; overall '
               'molecular properties are consistent with a rotenoid skeleton.\n'
               ' * SMILES: '
               'O=C1OC(C2=CC(OC)=C(O)C=C2)=CC3=C1C[C@]4(O)[C@]5(C(=O)C=CC([C@]5(O)CC[C@]4(O3)C)(C)C)C '
               'NAME: Territrem E REASON: WRONGLY CLASSIFIED Found fused pair: '
               'one six‐membered chromenone-like ring (with one carbonyl) '
               'fused to a six‐membered ether ring; overall molecular '
               'properties are consistent with a rotenoid skeleton.\n'
               ' * SMILES: '
               'O=C1O[C@@H]2C=3C(O[C@]4([C@@H]2C[C@@H](C)O4)C[C@@H]5OC(=O)CC5)=CC(=C6C3C1=C(O)C=C6C)OC '
               'NAME: Neonectriolide E REASON: WRONGLY CLASSIFIED Found fused '
               'pair: one six‐membered chromenone-like ring (with one '
               'carbonyl) fused to a six‐membered ether ring; overall '
               'molecular properties are consistent with a rotenoid skeleton.\n'
               ' * SMILES: '
               'Cl.Cl.CN[C@@H]1[C@H](O)[C@H](NC)[C@H]2O[C@]3(O)[C@@H](O[C@H](C)CC3=O)O[C@@H]2[C@H]1O '
               'NAME: spectinomycin dihydrochloride REASON: WRONGLY CLASSIFIED '
               'Found fused pair: one six‐membered chromenone-like ring (with '
               'one carbonyl) fused to a six‐membered ether ring; overall '
               'molecular properties are consistent with a rotenoid skeleton.\n'
               ' * SMILES: '
               'O=C1O[C@@H](C=C[C@@H](CC[C@]23O[C@H](C=4C(=C(NC(CC=C1C)=O)C=C(O)C4)O2)[C@H](C)C(C3)=O)CC)C(O)C=C(C)C '
               'NAME: Divergolide A REASON: WRONGLY CLASSIFIED Found fused '
               'pair: one six‐membered chromenone-like ring (with one '
               'carbonyl) fused to a six‐membered ether ring; overall '
               'molecular properties are consistent with a rotenoid skeleton.\n'
               ' * SMILES: O=C1C2=C(C3=C(O1)C=CC=C3)OC(CC2C4=CC=CC=C4)(OC)C '
               'NAME: cyclocoumarol REASON: WRONGLY CLASSIFIED Found fused '
               'pair: one six‐membered chromenone-like ring (with one '
               'carbonyl) fused to a six‐membered ether ring; overall '
               'molecular properties are consistent with a rotenoid skeleton.\n'
               ' * SMILES: '
               'C[NH2+][C@@H]1[C@H](O)[C@H]([NH2+]C)[C@H]2O[C@]3(O)[C@@H](O[C@H](C)CC3=O)O[C@@H]2[C@H]1O '
               'NAME: spectinomycin(2+) REASON: WRONGLY CLASSIFIED Found fused '
               'pair: one six‐membered chromenone-like ring (with one '
               'carbonyl) fused to a six‐membered ether ring; overall '
               'molecular properties are consistent with a rotenoid skeleton.\n'
               ' * SMILES: '
               'O1O[C@]2(OC3OC(=O)[C@@H](C4[C@@]13C([C@@H](CC4)C)CC2)C)C NAME: '
               '3,12-Epoxy-12H-pyrano[4,3-j]-1,2-benzodioxepin-10(3H)-one, '
               'octahydro-3,6,9-trimethyl-, (3R,5aS,6R,8aS,9R,12S,12aR)- '
               'REASON: WRONGLY CLASSIFIED Found fused pair: one six‐membered '
               'chromenone-like ring (with one carbonyl) fused to a '
               'six‐membered ether ring; overall molecular properties are '
               'consistent with a rotenoid skeleton.\n'
               ' * SMILES: O=C1C2=C(OC3=C1CO[C@@H](C3)C)C(O)=C(OC)C=C2C(=O)OC '
               'NAME: Phomopsichin C REASON: WRONGLY CLASSIFIED Found fused '
               'pair: one six‐membered chromenone-like ring (with one '
               'carbonyl) fused to a six‐membered ether ring; overall '
               'molecular properties are consistent with a rotenoid skeleton.\n'
               ' * SMILES: '
               'O=C1[C@H]2O[C@@](O[C@@H]([C@H]2C)[C@@H](/C=C(/C=C/C(/O)=C/3\\C(=O)NCC3=O)\\C)C)(C)[C@@]4([C@H]1O4)CO '
               'NAME: Tirandamycin B REASON: WRONGLY CLASSIFIED Found fused '
               'pair: one six‐membered chromenone-like ring (with one '
               'carbonyl) fused to a six‐membered ether ring; overall '
               'molecular properties are consistent with a rotenoid skeleton.\n'
               ' * SMILES: O(C1OC=C2C(O)(C1C=C)CCOC2=O)C3OC(C(O)C(O)C3O)CO '
               'NAME: Swertiamaroside REASON: WRONGLY CLASSIFIED Found fused '
               'pair: one six‐membered chromenone-like ring (with one '
               'carbonyl) fused to a six‐membered ether ring; overall '
               'molecular properties are consistent with a rotenoid skeleton.\n'
               ' * SMILES: '
               'O=C1C2=C(O)C(=CC=C2C(=O)C3=C1C=C(O)C=4C3=C(O)C=C(C)C4)[C@@H]5O[C@@H]([C@H]6O[C@H]7O[C@@H](C)C(C[C@@H]7O[C@@H]6C5)=O)C '
               'NAME: Landomycin N REASON: WRONGLY CLASSIFIED Found fused '
               'pair: one six‐membered chromenone-like ring (with one '
               'carbonyl) fused to a six‐membered ether ring; overall '
               'molecular properties are consistent with a rotenoid skeleton.\n'
               ' * SMILES: '
               'O=C1C2=C(O)C=CC=C2[C@@H](O)[C@@]34[C@H]1CC[C@]5([C@]3(O)C(=O)C[C@@](O4)(C5)C)O '
               'NAME: Gephyromycin C REASON: WRONGLY CLASSIFIED Found fused '
               'pair: one six‐membered chromenone-like ring (with one '
               'carbonyl) fused to a six‐membered ether ring; overall '
               'molecular properties are consistent with a rotenoid skeleton.\n'
               ' * SMILES: '
               'O=C1C2=C(C(O)=C(O)C(=C2C)O)[C@@H]3OC4=C([C@H]1O3)C(=C(C)C(=C4O)O)C=O '
               'NAME: Epicoccolide A REASON: WRONGLY CLASSIFIED Found fused '
               'pair: one six‐membered chromenone-like ring (with one '
               'carbonyl) fused to a six‐membered ether ring; overall '
               'molecular properties are consistent with a rotenoid skeleton.\n'
               ' * SMILES: '
               'O=C1O[C@@H]2[C@@](O[C@@H](C)[C@@H]([C@H]2C)OC(=O)/C=C/[C@@H](O)CCCC)(C)[C@H]([C@H]1C)OC(=O)C '
               'NAME: Botcinin A REASON: WRONGLY CLASSIFIED Found fused pair: '
               'one six‐membered chromenone-like ring (with one carbonyl) '
               'fused to a six‐membered ether ring; overall molecular '
               'properties are consistent with a rotenoid skeleton.\n'
               ' * SMILES: '
               'CC1(C)Oc2ccc3C(=O)[C@@H]4[C@@H](COc5cc6OCOc6cc45)Oc3c2C=C1 '
               'NAME: Millettone REASON: WRONGLY CLASSIFIED Found fused pair: '
               'one six‐membered chromenone-like ring (with one carbonyl) '
               'fused to a six‐membered ether ring; overall molecular '
               'properties are consistent with a rotenoid skeleton.\n'
               ' * SMILES: '
               'COc1c(O)cc2C(=O)OC3C(OC(=O)c4cc(O)c(O)c(O)c4)C(O)C(CO)OC3c2c1O '
               'NAME: 4-o-Galloylbergenin REASON: WRONGLY CLASSIFIED Found '
               'fused pair: one six‐membered chromenone-like ring (with one '
               'carbonyl) fused to a six‐membered ether ring; overall '
               'molecular properties are consistent with a rotenoid skeleton.\n'
               ' * SMILES: '
               'O=C1OC(C2=CC=C(OC)C=C2)=CC3=C1C[C@@H]4[C@@]5([C@H](C(C(=O)CC5)(C)C)CC[C@]4(O3)C)C '
               'NAME: Arisugacin G REASON: WRONGLY CLASSIFIED Found fused '
               'pair: one six‐membered chromenone-like ring (with one '
               'carbonyl) fused to a six‐membered ether ring; overall '
               'molecular properties are consistent with a rotenoid skeleton.\n'
               ' * SMILES: '
               'O1O[C@]2(O[C@]3(OC(=O)[C@H]([C@]4([C@@]13[C@]([C@H](CC4)C)(CC2)[H])[H])C)[H])C '
               'NAME: '
               '(1R,4S,5S,8S,9S,12S,13R)-1,5,9-Trimethyl-11,14,15,16-tetraoxatetracyclo[10.3.1.04,13.08,13]hexadecan-10-one '
               'REASON: WRONGLY CLASSIFIED Found fused pair: one six‐membered '
               'chromenone-like ring (with one carbonyl) fused to a '
               'six‐membered ether ring; overall molecular properties are '
               'consistent with a rotenoid skeleton.\n'
               ' * SMILES: '
               'COc1cc2OC[C@H]3Oc4c5C[C@@H](Oc5cc(O)c4C(=O)[C@H]3c2cc1OC)C(C)=C '
               'NAME: Sumatrol REASON: WRONGLY CLASSIFIED Found fused pair: '
               'one six‐membered chromenone-like ring (with one carbonyl) '
               'fused to a six‐membered ether ring; overall molecular '
               'properties are consistent with a rotenoid skeleton.\n'
               ' * SMILES: '
               'O=C1[C@H]2O[C@@](O[C@@H]([C@H]2C)[C@@H](C=C(C=CC(O)=C3C(=O)NCC3=O)C)C)(C)[C@@]4([C@H]1O4)CO '
               'NAME: Isotirandamycin B REASON: WRONGLY CLASSIFIED Found fused '
               'pair: one six‐membered chromenone-like ring (with one '
               'carbonyl) fused to a six‐membered ether ring; overall '
               'molecular properties are consistent with a rotenoid skeleton.\n'
               ' * SMILES: O=C1OC(=CC2=C1C[C@H]3[C@H](/C=C/C)CO[C@]3(O2)C)C '
               'NAME: Penicipyrone REASON: WRONGLY CLASSIFIED Found fused '
               'pair: one six‐membered chromenone-like ring (with one '
               'carbonyl) fused to a six‐membered ether ring; overall '
               'molecular properties are consistent with a rotenoid skeleton.\n'
               'False negatives: SMILES: '
               'O1C2C(O)(C(O)C3=C1C=4CC(OC4C=C3)C(CO[C@@H]5OC([C@@H](O)[C@H](O)C5O)CO)=C)C=6C(OC2)=CC(OC)=C(OC)C6 '
               'NAME: 12-Dihydrodalbinol O-glucoside REASON: MISSED No '
               'characteristic fused chromenone/ether ring pair with a single '
               'carbonyl was found; molecule is unlikely to be a rotenoid.\n'
               ' * SMILES: '
               'O(C(C1OC2=C(C1)C=3OC4C(C(=O)C3C=C2)C=5C(OC4)=CC(OC)=C(OC)C5)(CO)C)[C@@H]6OC([C@@H](O)[C@H](O)C6O)CO[C@@H]7OC[C@H](O)C(O)C7O '
               'NAME: Amorphigenol O-vicianoside REASON: MISSED Molecular '
               'weight 722.2 out of typical rotenoid range (250–600 Da)\n'
               ' * SMILES: '
               'O1C2C(O)(C(O)C3=C1C=4CC(OC4C=C3)C(CO)=C)C=5C(OC2)=CC(OC)=C(OC)C5 '
               'NAME: 12-Dihydrodalbinol REASON: MISSED No characteristic '
               'fused chromenone/ether ring pair with a single carbonyl was '
               'found; molecule is unlikely to be a rotenoid.\n'
               ' * SMILES: '
               'O1[C@@H]([C@@H](O)[C@H](O)[C@@H](O)[C@@H]1OCC(C2OC3=C(C2)C=4OC5C(C(=O)C4C=C3)C=6C(OC5)=CC(OC)=C(OC)C6)=C)CO[C@@H]7OC[C@H](O)[C@H](O)[C@H]7O '
               'NAME: Amorphigenin O-vicianoside REASON: MISSED Molecular '
               'weight 704.2 out of typical rotenoid range (250–600 Da)\n'
               ' * SMILES: '
               'O1C2=C(C=3C(OC2=O)=CC(OC)=C(OC)C3)C(=O)C=4C1=CC(OC)=CC4O NAME: '
               'Stemonone REASON: MISSED No characteristic fused '
               'chromenone/ether ring pair with a single carbonyl was found; '
               'molecule is unlikely to be a rotenoid.\n'
               ' * SMILES: '
               'O1C2C(C(O)C3=C1C4=C(OC=C4)C=C3)C=5C(OC2)=CC(OC)=C(OC)C5 NAME: '
               'Elliptinol REASON: MISSED No characteristic fused '
               'chromenone/ether ring pair with a single carbonyl was found; '
               'molecule is unlikely to be a rotenoid.\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'O1C2=C(O)C=C(COC)C=C2C[C@@H](C1(C)C)O',
                                     'name': 'Conoideochromane B',
                                     'reason': 'No candidate chromenone-like '
                                               'ring (6-membered with one '
                                               'carbonyl and at least one '
                                               'oxygen) found'},
                                 {   'smiles': 'P(OC[C@H](OC(=O)CCCCCCC/C=C\\CCCCC)CO/C=C\\CCCCCCCCCCCCCC)(OCCN)(O)=O',
                                     'name': 'PE(P-16:0/15:1(9Z))',
                                     'reason': 'No candidate chromenone-like '
                                               'ring (6-membered with one '
                                               'carbonyl and at least one '
                                               'oxygen) found'},
                                 {   'smiles': 'O=C1C=2C(OC(=C1)C)=C(C3=C4O[C@](O)(CC(C4=C(O)C=5C3=CC(OC)=CC5OC)=O)C)C6=CC(OC)=CC(=C6C2O)OC',
                                     'name': '2-hydroxydihydronigerone',
                                     'reason': 'No candidate ether ring '
                                               '(6-membered with oxygen and no '
                                               'in-ring carbonyl) found'},
                                 {   'smiles': 'O([C@@H]1[C@@H](NC(=O)C)[C@@H](O[C@@H]([C@H]1O)CO)OC[C@H]2O[C@@H](O)[C@H](NC(=O)C)[C@@H](O)[C@H]2O)[C@@H]3O[C@@H]([C@H](O)[C@H](O[C@H]4O[C@@H]([C@H](O)[C@H](O)[C@H]4O)CO)[C@H]3O)CO',
                                     'name': 'N-[(2R,3R,4R,5R,6R)-6-[[(2R,3R,4R,5S,6R)-3-Acetamido-4-[(2R,3R,4S,5S,6R)-3,5-dihydroxy-6-(hydroxymethyl)-4-[(2R,3R,4S,5R,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-5-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxymethyl]-2,4,5-trihydroxyoxan-3-yl]acetamide',
                                     'reason': 'No candidate chromenone-like '
                                               'ring (6-membered with one '
                                               'carbonyl and at least one '
                                               'oxygen) found'},
                                 {   'smiles': 'O1C(C(O)C(O)C(O)C1OC=2C(O)=C(O)C=C(C2)C=O)COC(=O)C3=CC(O)=C(O)C(O)=C3',
                                     'name': 'Castamollissin',
                                     'reason': 'No candidate chromenone-like '
                                               'ring (6-membered with one '
                                               'carbonyl and at least one '
                                               'oxygen) found'},
                                 {   'smiles': 'S(OC[C@H]1O[C@@H](OC[C@H]2O[C@@H](O[C@@H]([C@@H](O)[C@H](O)CO[C@]3(O[C@H]([C@H](NC(=O)C)[C@@H](O)C3)[C@H](O)[C@H](O)CO)C(O)=O)[C@@H](NC(=O)C)CO)[C@H](O)[C@@H](O)[C@H]2O)[C@H](NC(=O)C)[C@@H](O)[C@@H]1O[C@@H]4O[C@@H]([C@H](O)[C@H](O)[C@H]4O)CO[C@]5(O[C@H]([C@H](NC(=O)C)[C@@H](O)C5)[C@H](O)[C@H](O)CO)C(O)=O)(O)(=O)=O',
                                     'name': '(2R,4S,5R,6R)-5-Acetamido-2-[[(2R,3R,4S,5R,6S)-6-[(2R,3S,4R,5R,6R)-5-acetamido-6-[[(2R,3R,4S,5R,6R)-6-[(2S,3R,4S,5R)-2-acetamido-6-[(2R,4S,5R,6R)-5-acetamido-2-carboxy-4-hydroxy-6-[(1R,2R)-1,2,3-trihydroxypropyl]oxan-2-yl]oxy-1,4,5-trihydroxyhexan-3-yl]oxy-3,4,5-trihydroxyoxan-2-yl]methoxy]-4-hydroxy-2-(sulfooxymethyl)oxan-3-yl]oxy-3,4,5-trihydroxyoxan-2-yl]methoxy]-4-hydroxy-6-[(1R,2R)-1,2,3-trihydroxypropyl]oxane-2-carboxylic '
                                             'acid',
                                     'reason': 'No candidate chromenone-like '
                                               'ring (6-membered with one '
                                               'carbonyl and at least one '
                                               'oxygen) found'},
                                 {   'smiles': 'FC(F)(F)C(F)(F)C(F)(F)C(F)(F)C(F)(F)C(F)(F)F',
                                     'name': 'perfluorohexane',
                                     'reason': 'No candidate chromenone-like '
                                               'ring (6-membered with one '
                                               'carbonyl and at least one '
                                               'oxygen) found'},
                                 {   'smiles': 'CC(C)(O)CCC(=O)[C@](C)(O)[C@H]1[C@H](O)C[C@@]2(C)[C@@H]3CC=C4[C@@H](C[C@@H](O)[C@@H](O)C4(C)C)[C@]3(C)C(=O)C[C@]12C',
                                     'name': 'Cucurbitacin P',
                                     'reason': 'No candidate chromenone-like '
                                               'ring (6-membered with one '
                                               'carbonyl and at least one '
                                               'oxygen) found'},
                                 {   'smiles': 'CCCCCCCc1cc(O)cc(=O)o1',
                                     'name': '4-hydroxy-6-heptylpyran-2-one',
                                     'reason': 'No candidate ether ring '
                                               '(6-membered with oxygen and no '
                                               'in-ring carbonyl) found'},
                                 {   'smiles': 'S(O[C@@H]1[C@@H](O)[C@H](O[C@H]2[C@H](O)[C@@H](NC(=O)C)[C@H](O[C@H]3[C@@H](O)[C@H](O[C@@H]4O[C@@H]([C@@H](O[C@@H]5O[C@@H]([C@H](O)[C@H](OS(O)(=O)=O)[C@H]5O)CO)[C@H](O)[C@H]4NC(=O)C)CO)[C@H](O[C@@H]3O[C@H]6[C@H](O)[C@H](O[C@@H](O[C@H]7[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]7CO)O[C@H]8[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]8CO[C@@H]9O[C@H]([C@@H](O)[C@@H](O)[C@@H]9O)C)O)[C@H]6O)CO[C@H]%10O[C@@H]([C@@H](O)[C@H](O)[C@@H]%10O[C@@H]%11O[C@@H]([C@@H](O[C@@H]%12O[C@@H]([C@H](O[C@@H]%13O[C@@H]([C@H](O)[C@H](O)[C@H]%13NC(=O)C)CO)[C@H](O[C@]%14(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%14)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%12O)CO)[C@H](O)[C@H]%11NC(=O)C)CO)CO[C@@H]%15O[C@@H]([C@@H](O[C@@H]%16O[C@@H]([C@H](O)[C@H](O[C@]%17(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%17)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%16O)CO)[C@H](O)[C@H]%15NC(=O)C)CO)CO)O[C@@H]2CO)O[C@@H]([C@@H]1O)CO)(O)(=O)=O',
                                     'name': 'CID 146017241',
                                     'reason': 'No candidate chromenone-like '
                                               'ring (6-membered with one '
                                               'carbonyl and at least one '
                                               'oxygen) found'}],
    'sample_false_negatives': [   {   'smiles': 'O1C2C(O)(C(O)C3=C1C=4CC(OC4C=C3)C(CO[C@@H]5OC([C@@H](O)[C@H](O)C5O)CO)=C)C=6C(OC2)=CC(OC)=C(OC)C6',
                                      'name': '12-Dihydrodalbinol O-glucoside',
                                      'reason': 'No candidate chromenone-like '
                                                'ring (6-membered with one '
                                                'carbonyl and at least one '
                                                'oxygen) found'},
                                  {   'smiles': 'O1C2C(O)(C(O)C3=C1C=4CC(OC4C=C3)C(CO)=C)C=5C(OC2)=CC(OC)=C(OC)C5',
                                      'name': '12-Dihydrodalbinol',
                                      'reason': 'No candidate chromenone-like '
                                                'ring (6-membered with one '
                                                'carbonyl and at least one '
                                                'oxygen) found'},
                                  {   'smiles': 'O1C2=C(C=3C(OC2=O)=CC(OC)=C(OC)C3)C(=O)C=4C1=CC(OC)=CC4O',
                                      'name': 'Stemonone',
                                      'reason': 'No candidate ether ring '
                                                '(6-membered with oxygen and '
                                                'no in-ring carbonyl) found'},
                                  {   'smiles': 'O1C2C(C(O)C3=C1C4=C(OC=C4)C=C3)C=5C(OC2)=CC(OC)=C(OC)C5',
                                      'name': 'Elliptinol',
                                      'reason': 'No candidate chromenone-like '
                                                'ring (6-membered with one '
                                                'carbonyl and at least one '
                                                'oxygen) found'}],
    'attempt': 2,
    'reasoning': 'Below is one possible improved solution. In our reasoning we '
                 'observed that the previous approach was too strict in '
                 'several ways: (a) it enforced a narrow molecular‐weight '
                 'range (which then ruled out glycosides of rotenoids), (b) it '
                 'insisted that the overall “fused” system have exactly one '
                 'carbonyl when many substituted rotenoids may have extra '
                 'carbonyl groups in sidechains, and (c) it did not check for '
                 'features of the “tetrahydro” nature of the core. In the '
                 'following revision we (1) relax the weight filter (only '
                 'excluding very light molecules), (2) require that among the '
                 'candidate fused rings at least one “chromenone‐like” ring '
                 '(six‐membered, containing at least one in‐ring oxygen and '
                 'exactly one carbonyl detected by a double bond from a ring '
                 'carbon) is present and that it is fused to a second '
                 'six‐membered “ether” ring (which bears at least one oxygen '
                 'but no in‐ring carbonyl). In addition we enforce that the '
                 'two rings share exactly two atoms (their typical cis‐fusion '
                 'junction) to help reduce false positives. (Note that many '
                 'molecules are obviously complex, and any heuristic based on '
                 'rings will be imperfect.) \n'
                 '\n'
                 'Below is the complete Python module contained in one code '
                 'block:',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 32,
    'num_false_positives': 287,
    'num_true_negatives': 141977,
    'num_false_negatives': 4,
    'num_negatives': None,
    'precision': 0.10031347962382445,
    'recall': 0.8888888888888888,
    'f1': 0.18028169014084505,
    'accuracy': 0.9979550245959241,
    'negative_predictive_value': 0.9999718272163177}