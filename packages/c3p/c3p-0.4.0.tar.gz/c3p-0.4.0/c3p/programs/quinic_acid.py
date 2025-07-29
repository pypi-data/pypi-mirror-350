"""
Classifies: CHEBI:26493 quinic acid
"""
"""
Classifies: Quinic acid – a cyclitol carboxylic acid derivative.
A quinic acid derivative is defined as having an isolated (i.e. non-fused)
saturated cyclohexane ring (all carbons, all single bonds) that displays exactly
one exocyclic carboxyl group (with neutral oxygen atoms) and at least four oxygen substituents.
This heuristic attempts to avoid false positives from fused-ring molecules.
"""
from rdkit import Chem

def is_quinic_acid(smiles: str):
    """
    Determines if a molecule is a quinic acid derivative (cyclitol carboxylic acid derivative)
    based on its SMILES string.
    The algorithm:
      (1) Searches for a saturated cyclohexane (six-carbon) ring.
      (2) Ensures that the ring is not fused with any other ring (i.e. it is isolated).
      (3) Looks for exactly one exocyclic carboxyl group (as defined by a carbon
          that is sp2 and bound to one double-bonded oxygen and one single-bonded oxygen, both neutral).
      (4) Requires at least four oxygen substituents from the ring carbons.
    Args:
        smiles (str): SMILES string of the molecule.
    Returns:
        bool: True if the molecule is recognized as a quinic acid derivative, False otherwise.
        str: A reason describing the outcome.
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
    
    ring_info = mol.GetRingInfo()
    atom_rings = ring_info.AtomRings()
    
    # Helper function to check if a carbon is part of a neutral carboxyl group.
    def is_carboxyl_group(carbon):
        """
        Confirms whether a carbon atom is part of a carboxyl group.
        It must be a carbon (atomic number 6) with at least one double-bonded oxygen and one single-bonded oxygen,
        and the involved oxygens must have a formal charge of zero.
        """
        if carbon.GetAtomicNum() != 6:
            return False
        oxy_double = []
        oxy_single = []
        for nbr in carbon.GetNeighbors():
            if nbr.GetAtomicNum() == 8:
                bond = mol.GetBondBetweenAtoms(carbon.GetIdx(), nbr.GetIdx())
                if bond is None:
                    continue
                if bond.GetBondType() == Chem.BondType.DOUBLE:
                    oxy_double.append(nbr)
                elif bond.GetBondType() == Chem.BondType.SINGLE:
                    oxy_single.append(nbr)
        # Require at least one double and one single bond to oxygen and check formal charges are zero.
        if oxy_double and oxy_single:
            if all(o.GetFormalCharge() == 0 for o in oxy_double + oxy_single):
                return True
        return False

    # Check each ring to find an isolated cyclohexane ring.
    for ring in atom_rings:
        if len(ring) != 6:
            continue  # Only consider six-membered rings.
        
        # Ensure all atoms in the ring are carbons.
        if not all(mol.GetAtomWithIdx(idx).GetAtomicNum() == 6 for idx in ring):
            continue
            
        # Ensure that all bonds within the ring are single and not aromatic.
        ring_is_saturated = True
        n_ring = len(ring)
        for i in range(n_ring):
            idx1 = ring[i]
            idx2 = ring[(i+1) % n_ring]
            bond = mol.GetBondBetweenAtoms(idx1, idx2)
            if bond is None or bond.GetIsAromatic() or bond.GetBondType() != Chem.BondType.SINGLE:
                ring_is_saturated = False
                break
        if not ring_is_saturated:
            continue
            
        # Now check that the cyclohexane ring is isolated (not fused with another ring).
        # For every other ring in the molecule, if it shares 2 or more atoms with our candidate ring, then discard.
        isolated = True
        candidate_set = set(ring)
        for other_ring in atom_rings:
            if set(other_ring) == candidate_set:
                continue  # this is our candidate ring itself
            # If the intersection is 2 or more atoms, assume the candidate ring is fused.
            if len(candidate_set.intersection(other_ring)) >= 2:
                isolated = False
                break
        if not isolated:
            continue

        # Now count substituents on the candidate ring.
        carboxyl_count = 0
        oxy_substituent_count = 0
        # For each carbon in the ring, examine neighbors not in the ring.
        for idx in ring:
            atom = mol.GetAtomWithIdx(idx)
            for nbr in atom.GetNeighbors():
                if nbr.GetIdx() in candidate_set:
                    continue
                bond = mol.GetBondBetweenAtoms(atom.GetIdx(), nbr.GetIdx())
                # If the neighbor is oxygen and connected by a single bond, count it.
                if nbr.GetAtomicNum() == 8 and bond.GetBondType() == Chem.BondType.SINGLE:
                    oxy_substituent_count += 1
                # If the neighbor is carbon, test if it is a carboxyl group.
                elif nbr.GetAtomicNum() == 6:
                    if is_carboxyl_group(nbr):
                        # Also ensure that the attached carboxyl group is neutral.
                        carboxyl_count += 1
        # For a quinic acid derivative, we require exactly one carboxyl group and at least four oxygens.
        if carboxyl_count == 1 and oxy_substituent_count >= 4:
            reason = (f"Contains an isolated saturated cyclohexane ring with {carboxyl_count} carboxyl group and "
                      f"{oxy_substituent_count} oxygen substituents, consistent with a cyclitol carboxylic acid derivative.")
            return True, reason
    
    return False, "No isolated saturated cyclohexane ring with one (neutral) carboxyl group and at least four oxygen substituents found"

# (Optional testing code; remove or uncomment as needed)
# examples = [
#     "COc1cc(ccc1O)\\C=C\\C(=O)O[C@H]1[C@H](O)C[C@@](O)(C[C@H]1O)C(O)=O",  # 4-O-feruloyl-D-quinic acid, correct
#     "O[C@@H]1C[C@@](O)(C[C@@H](O)[C@H]1O)C(O)=O",  # (+)-quinic acid, correct
#     "O[C@@H]1C[C@@](O)(C[C@@H](O)[C@H]1O)C([O-])=O",  # (-)-quinate, should be rejected
# ]
# for smi in examples:
#     result, msg = is_quinic_acid(smi)
#     print(smi, "->", result, msg)


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:26493',
                          'name': 'quinic acid',
                          'definition': 'A cyclitol carboxylic acid.',
                          'parents': ['CHEBI:36123'],
                          'xrefs': [   'PMID:15589483',
                                       'PMID:19952409',
                                       'PMID:23590498'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 78,
                           'log_lines_of_code': 4.356708826689592,
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
                                                 1,
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
                                                 3,
                                                 4,
                                                 4,
                                                 5,
                                                 4,
                                                 5,
                                                 4,
                                                 5,
                                                 2,
                                                 2,
                                                 3,
                                                 4,
                                                 2,
                                                 0,
                                                 1,
                                                 1,
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
                                                 3,
                                                 3,
                                                 3,
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
                                                 3,
                                                 4,
                                                 3,
                                                 3,
                                                 4,
                                                 4,
                                                 2,
                                                 3,
                                                 0,
                                                 1,
                                                 1,
                                                 0],
                           'max_indent': 5,
                           'imports': ['from rdkit import Chem'],
                           'imports_count': 1,
                           'methods_called': [   'MolFromSmiles',
                                                 'append',
                                                 'GetNeighbors',
                                                 'GetFormalCharge',
                                                 'GetIdx',
                                                 'AtomRings',
                                                 'GetBondType',
                                                 'GetRingInfo',
                                                 'GetBondBetweenAtoms',
                                                 'GetAtomWithIdx',
                                                 'intersection',
                                                 'GetIsAromatic',
                                                 'GetAtomicNum'],
                           'methods_called_count': 13,
                           'smarts_strings': [],
                           'smarts_strings_count': 0,
                           'defs': [   'is_quinic_acid(smiles: str):',
                                       'is_carboxyl_group(carbon):'],
                           'defs_count': 2,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False',
                                          'True',
                                          'False',
                                          'False, "No isolated saturated '
                                          'cyclohexane ring with one (neutral) '
                                          'carboxyl group and at least four '
                                          'oxygen substituents found"'],
                           'returns_count': 5,
                           'complexity': 5.8713417653379185},
    'message': '\n'
               'Attempt failed: F1 score of 0.5263157894736842 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: '
               'COc1cc(ccc1O)\\C=C\\C(=O)O[C@H]1[C@H](O)C[C@@](O)(C[C@H]1O)C(O)=O '
               'NAME: 4-O-feruloyl-D-quinic acid REASON: CORRECT Contains a '
               'saturated cyclohexane ring with 1 carboxyl group and 4 oxygen '
               'substituents, consistent with a cyclitol carboxylic acid '
               'derivative.\n'
               ' * SMILES: '
               'C1=CC(OC)=C(C=C1/C=C/C(OC2C(CC(CC2O)(O)C(O)=O)O)=O)O NAME: '
               '1,3,5-trihydroxy-4-{[(2E)-3-(3-hydroxy-4-methoxyphenyl)-2-propenoyl]oxy}cyclohexanecarboxylic '
               'acid REASON: CORRECT Contains a saturated cyclohexane ring '
               'with 1 carboxyl group and 4 oxygen substituents, consistent '
               'with a cyclitol carboxylic acid derivative.\n'
               ' * SMILES: OC1(CC(O)C(O)C(O)C1)C(O)=O NAME: '
               '1,3,4,5-Tetrahydroxycyclohexanecarboxylic acid REASON: CORRECT '
               'Contains a saturated cyclohexane ring with 1 carboxyl group '
               'and 4 oxygen substituents, consistent with a cyclitol '
               'carboxylic acid derivative.\n'
               ' * SMILES: '
               'O([C@@H]1C[C@](O)(C[C@@H](OC(=O)/C=C/C2=CC=C(O)C=C2)[C@@H]1O)C(O)=O)C(=O)/C=C/C3=CC=C(O)C=C3 '
               'NAME: 3,5-di-O-p-coumaroylquinic acid REASON: CORRECT Contains '
               'a saturated cyclohexane ring with 1 carboxyl group and 4 '
               'oxygen substituents, consistent with a cyclitol carboxylic '
               'acid derivative.\n'
               ' * SMILES: '
               'O(C1[C@H](OC(=O)/C=C/C2=CC(O)=C(O)C=C2)CC(O)(C[C@H]1OC(=O)/C=C/C3=CC(O)=C(O)C=C3)C(O)=O)C(=O)/C=C/C4=CC(O)=C(O)C=C4 '
               'NAME: '
               '(3R,5R)-3,4,5-tris{[(2E)-3-(3,4-dihydroxyphenyl)prop-2-enoyl]oxy}-1-hydroxycyclohexane-1-carboxylic '
               'acid REASON: CORRECT Contains a saturated cyclohexane ring '
               'with 1 carboxyl group and 4 oxygen substituents, consistent '
               'with a cyclitol carboxylic acid derivative.\n'
               ' * SMILES: '
               'O(C1CC(O)(CC(O)C1O)C(OCCCC)=O)C(=O)/C=C\\C2=CC(O)=C(O)C=C2 '
               'NAME: Butyl 3-O-caffeoylquinate REASON: CORRECT Contains a '
               'saturated cyclohexane ring with 1 carboxyl group and 4 oxygen '
               'substituents, consistent with a cyclitol carboxylic acid '
               'derivative.\n'
               ' * SMILES: '
               'O(C1(CC(OC(=O)/C=C\\C2=CC(O)=C(O)C=C2)C(O)C(O)C1)C(O)=O)C '
               'NAME: 3-O-Caffeoyl-1-O-methylquinic acid REASON: CORRECT '
               'Contains a saturated cyclohexane ring with 1 carboxyl group '
               'and 4 oxygen substituents, consistent with a cyclitol '
               'carboxylic acid derivative.\n'
               ' * SMILES: '
               'C(=O)(/C=C/C1=CC=C(O)C(O)=C1)O[C@@]2(C[C@@H](O)[C@@H]([C@@H](C2)O)O)C(O)=O '
               'NAME: 1-O-caffeoylquinic acid REASON: CORRECT Contains a '
               'saturated cyclohexane ring with 1 carboxyl group and 4 oxygen '
               'substituents, consistent with a cyclitol carboxylic acid '
               'derivative.\n'
               ' * SMILES: O[C@H]1C[C@@](O)(C[C@H](O)[C@H]1O)C(O)=O NAME: '
               '(+)-quinic acid REASON: CORRECT Contains a saturated '
               'cyclohexane ring with 1 carboxyl group and 4 oxygen '
               'substituents, consistent with a cyclitol carboxylic acid '
               'derivative.\n'
               ' * SMILES: '
               'C=1C=C(C(=CC1/C=C/C(=O)O[C@H]2C[C@@](C[C@H]([C@H]2O)O)(C(=O)O)O)O)O '
               'NAME: '
               '(1S,3S,4R,5R)-3-{[(2E)-3-(3,4-dihydroxyphenyl)-2-propenoyl]oxy}-1,4,5-trihydroxycyclohexanecarboxylic '
               'acid REASON: CORRECT Contains a saturated cyclohexane ring '
               'with 1 carboxyl group and 4 oxygen substituents, consistent '
               'with a cyclitol carboxylic acid derivative.\n'
               ' * SMILES: '
               'C1=CC(=C(C=C1/C=C/C(O[C@@H]2[C@H](O)C[C@](C[C@H]2O)(C(OC)=O)O)=O)O)O '
               'NAME: 4-O-E-caffeoylquinic acid methyl ester REASON: CORRECT '
               'Contains a saturated cyclohexane ring with 1 carboxyl group '
               'and 4 oxygen substituents, consistent with a cyclitol '
               'carboxylic acid derivative.\n'
               ' * SMILES: '
               'O(C1CC(O)(CC(O)C1O)C(O)=O)C(=O)/C=C\\C2=CC(O)=C(O)C=C2 NAME: '
               'trans-Chlorogenic acid REASON: CORRECT Contains a saturated '
               'cyclohexane ring with 1 carboxyl group and 4 oxygen '
               'substituents, consistent with a cyclitol carboxylic acid '
               'derivative.\n'
               ' * SMILES: '
               '[C@@]1(C(OC)=O)(C[C@H]([C@H](O)[C@@H](C1)O)OC(=O)\\C=C\\C2=CC(=C(C=C2)O)O)O '
               'NAME: 3-O-caffeoylquinic acid methyl ester REASON: CORRECT '
               'Contains a saturated cyclohexane ring with 1 carboxyl group '
               'and 4 oxygen substituents, consistent with a cyclitol '
               'carboxylic acid derivative.\n'
               ' * SMILES: '
               'O(C1(C[C@@H](O)C(OC(=O)/C=C/C2=CC(O)=C(O)C=C2)[C@H](O)C1)C(O)=O)C(=O)/C=C/C3=CC(O)=C(O)C=C3 '
               'NAME: 1,4-Di-O-caffeoylquinic acid REASON: CORRECT Contains a '
               'saturated cyclohexane ring with 1 carboxyl group and 4 oxygen '
               'substituents, consistent with a cyclitol carboxylic acid '
               'derivative.\n'
               ' * SMILES: '
               'O(C1C(OC(=O)/C=C/C2=CC(O)=C(O)C=C2)C(O)CC(O)(C1)C(OC)=O)C(=O)/C=C/C3=CC(O)=C(O)C=C3 '
               'NAME: Macranthoin F REASON: CORRECT Contains a saturated '
               'cyclohexane ring with 1 carboxyl group and 4 oxygen '
               'substituents, consistent with a cyclitol carboxylic acid '
               'derivative.\n'
               ' * SMILES: '
               'O([C@@H]1CC(O)(C[C@@H](O)[C@H]1O)C(O)=O)C(=O)/C=C/C2=CC(O)=C(O)C=C2 '
               'NAME: '
               '(3R,4R,5R)-3-[(E)-3-(3,4-Dihydroxyphenyl)prop-2-enoyl]oxy-1,4,5-trihydroxycyclohexane-1-carboxylic '
               'acid REASON: CORRECT Contains a saturated cyclohexane ring '
               'with 1 carboxyl group and 4 oxygen substituents, consistent '
               'with a cyclitol carboxylic acid derivative.\n'
               ' * SMILES: '
               'OC1CC(O)(CC(OC(=O)\\C=C\\c2ccc(O)c(O)c2)C1OC(=O)CCc1ccc(O)c(O)c1)C(O)=O '
               'NAME: Tungtungmadic acid REASON: CORRECT Contains a saturated '
               'cyclohexane ring with 1 carboxyl group and 4 oxygen '
               'substituents, consistent with a cyclitol carboxylic acid '
               'derivative.\n'
               ' * SMILES: '
               'COc1cc(\\C=C\\C(=O)O[C@@H]2C[C@@](O)(C[C@@H](O)[C@H]2O)C(O)=O)ccc1O '
               'NAME: 3-O-feruloyl-D-quinic acid REASON: CORRECT Contains a '
               'saturated cyclohexane ring with 1 carboxyl group and 4 oxygen '
               'substituents, consistent with a cyclitol carboxylic acid '
               'derivative.\n'
               ' * SMILES: O[C@@H]1C[C@@](O)(C[C@@H](O)[C@H]1O)C(O)=O NAME: '
               '(-)-quinic acid REASON: CORRECT Contains a saturated '
               'cyclohexane ring with 1 carboxyl group and 4 oxygen '
               'substituents, consistent with a cyclitol carboxylic acid '
               'derivative.\n'
               ' * SMILES: '
               'O[C@@H]1C[C@](O)(C[C@@H](OC(=O)/C=C/C2=CC=C(O)C=C2)[C@@H]1OC(=O)/C=C/C3=CC=C(O)C=C3)C(O)=O '
               'NAME: 4,5-di-O-p-coumaroylquinic acid REASON: CORRECT Contains '
               'a saturated cyclohexane ring with 1 carboxyl group and 4 '
               'oxygen substituents, consistent with a cyclitol carboxylic '
               'acid derivative.\n'
               ' * SMILES: '
               'COC(=O)[C@@]1(O)C[C@@H](O)[C@H](OC(=O)\\C=C\\c2ccc(O)c(OC)c2)[C@@H](C1)OC(=O)\\C=C\\c1ccc(O)c(O)c1 '
               'NAME: methyl 3,4-dicaffeoylquinate REASON: CORRECT Contains a '
               'saturated cyclohexane ring with 1 carboxyl group and 4 oxygen '
               'substituents, consistent with a cyclitol carboxylic acid '
               'derivative.\n'
               ' * SMILES: '
               'O[C@@H]1C[C@](C[C@@H](OC(=O)\\C=C\\c2ccc(O)c(O)c2)[C@H]1O)(OC(=O)\\C=C\\c1ccc(O)c(O)c1)C(O)=O '
               'NAME: 1,3-dicaffeoylquinic acid REASON: CORRECT Contains a '
               'saturated cyclohexane ring with 1 carboxyl group and 4 oxygen '
               'substituents, consistent with a cyclitol carboxylic acid '
               'derivative.\n'
               ' * SMILES: '
               'C(=O)(/C=C/C1=CC=C(O)C(O)=C1)O[C@@]2(C[C@@H](O)[C@@H]([C@@H](C2)OC(=O)/C=C/C3=CC(=C(O)C=C3)OC)O)C(O)=O '
               'NAME: 1-caffeoyl-5-feruloylquinic acid REASON: CORRECT '
               'Contains a saturated cyclohexane ring with 1 carboxyl group '
               'and 4 oxygen substituents, consistent with a cyclitol '
               'carboxylic acid derivative.\n'
               ' * SMILES: '
               'C1[C@H]([C@H]([C@@H](C[C@@]1(C(=O)O)O)OC(=O)C=CC2=CC(=C(C=C2)O)O)O)O '
               'NAME: '
               '(1S,3R,4R,5R)-3-[3-(3,4-dihydroxyphenyl)-1-oxoprop-2-enoxy]-1,4,5-trihydroxy-1-cyclohexanecarboxylic '
               'acid REASON: CORRECT Contains a saturated cyclohexane ring '
               'with 1 carboxyl group and 4 oxygen substituents, consistent '
               'with a cyclitol carboxylic acid derivative.\n'
               ' * SMILES: '
               'O(C1[C@H](O)CC(O)(C[C@H]1O)C(O)=O)C(=O)/C=C/C2=CC(OC)=C(O)C=C2 '
               'NAME: '
               '(3r,5r)-1,3,5-trihydroxy-4-{[(2e)-3-(4-hydroxy-3-methoxyphenyl)-2-propenoyl]oxy}cyclohexanecarboxylic '
               'acid REASON: CORRECT Contains a saturated cyclohexane ring '
               'with 1 carboxyl group and 4 oxygen substituents, consistent '
               'with a cyclitol carboxylic acid derivative.\n'
               'False positives: SMILES: '
               'O1C23C(C(C4OC4C2O)(C1=O)C)C(C56C3CCC(O)(C5)C(C6)=C)C(O)=O '
               'NAME: Gibberellin A93 REASON: WRONGLY CLASSIFIED Contains a '
               'saturated cyclohexane ring with 1 carboxyl group and 4 oxygen '
               'substituents, consistent with a cyclitol carboxylic acid '
               'derivative.\n'
               ' * SMILES: '
               'Cl[C@]12[C@]34OO[C@H]5[C@]6(O[C@H]6[C@H](C=C5C3=C[C@]1(C[C@]([C@@]47OC(=O)C=8C(O)=CC(=CC8O7)C)(C(=O)OC)C[C@H]2OC)C)O)CC=C(C)C '
               'NAME: Chloropupukeanolide A REASON: WRONGLY CLASSIFIED '
               'Contains a saturated cyclohexane ring with 1 carboxyl group '
               'and 4 oxygen substituents, consistent with a cyclitol '
               'carboxylic acid derivative.\n'
               ' * SMILES: '
               'O1[C@@]2(C[C@@](O)(C[C@@H](OC(=O)/C=C/C3=CC(O)=C(O)C=C3)[C@H]2OC(=O)/C=C/C4=CC(O)=C(O)C=C4)C1=O)[H] '
               'NAME: 3,4-Dicaffeoyl-1,5-quinolactone REASON: WRONGLY '
               'CLASSIFIED Contains a saturated cyclohexane ring with 1 '
               'carboxyl group and 4 oxygen substituents, consistent with a '
               'cyclitol carboxylic acid derivative.\n'
               ' * SMILES: '
               'COc1cc(ccc1O)\\C=C\\C(=O)O[C@H]1[C@H](O)C[C@@](O)(C[C@H]1O)C([O-])=O '
               'NAME: 4-O-feruloyl-D-quinate REASON: WRONGLY CLASSIFIED '
               'Contains a saturated cyclohexane ring with 1 carboxyl group '
               'and 4 oxygen substituents, consistent with a cyclitol '
               'carboxylic acid derivative.\n'
               ' * SMILES: '
               'O=C1C2=C(O)C(C3=C4O[C@@]5(C(=O)OC)[C@@H](OC(=O)C)CCCC5C(C4=C(O)C=C3C)=O)=CC=C2OC67[C@@]1(O)[C@@H](OC6=O)C[C@H]([C@H]7O)C '
               'NAME: Usneaxanthone A REASON: WRONGLY CLASSIFIED Contains a '
               'saturated cyclohexane ring with 1 carboxyl group and 4 oxygen '
               'substituents, consistent with a cyclitol carboxylic acid '
               'derivative.\n'
               ' * SMILES: '
               'C[C@@]12C[C@@H](OC(=O)[C@@H]1CC[C@]1(C)[C@H]2[C@@H]2OC(=O)[C@@]1(O)[C@H]1O[C@@H]21)c1ccoc1 '
               'NAME: Chasmanthin REASON: WRONGLY CLASSIFIED Contains a '
               'saturated cyclohexane ring with 1 carboxyl group and 4 oxygen '
               'substituents, consistent with a cyclitol carboxylic acid '
               'derivative.\n'
               ' * SMILES: '
               'O1C23C(C(C4OC4C2O)(C1=O)C)C(C56C3CCC(C5)C(C6)=C)C(O)=O NAME: '
               'Gibberellin A94 REASON: WRONGLY CLASSIFIED Contains a '
               'saturated cyclohexane ring with 1 carboxyl group and 4 oxygen '
               'substituents, consistent with a cyclitol carboxylic acid '
               'derivative.\n'
               ' * SMILES: '
               'O=C1C2=C(O)C(C3=C(O)C4=C(OC(C(=O)OC)(C5OC(=O)CC5C)CC4=O)C=C3)=CC=C2OC67C1(O)C(OC6=O)CC(C7O)C '
               'NAME: Ergoxanthin REASON: WRONGLY CLASSIFIED Contains a '
               'saturated cyclohexane ring with 1 carboxyl group and 4 oxygen '
               'substituents, consistent with a cyclitol carboxylic acid '
               'derivative.\n'
               ' * SMILES: '
               'O[C@@H]1C[C@](O)(C[C@@H](OC(=O)\\C=C/c2ccc(O)c(O)c2)[C@@H]1O)C(O)=O '
               'NAME: 5-O-cis-caffeoylquinic acid REASON: WRONGLY CLASSIFIED '
               'Contains a saturated cyclohexane ring with 1 carboxyl group '
               'and 4 oxygen substituents, consistent with a cyclitol '
               'carboxylic acid derivative.\n'
               ' * SMILES: '
               'O1[C@@]2(C[C@@](O)(C[C@@H](O)[C@H]2OC(=O)/C=C/C3=CC(OC)=C(O)C=C3)C1=O)[H] '
               'NAME: 4-Feruloyl-1,5-quinolactone REASON: WRONGLY CLASSIFIED '
               'Contains a saturated cyclohexane ring with 1 carboxyl group '
               'and 4 oxygen substituents, consistent with a cyclitol '
               'carboxylic acid derivative.\n'
               ' * SMILES: '
               'COC(=O)[C@@]1(O)C[C@@H](OC(=O)\\C=C\\c2ccc(O)c(O)c2)[C@H](O)[C@@H](C1)OC(=O)\\C=C\\c1ccc(O)c(O)c1 '
               'NAME: methyl 3,5-di-O-caffeoyl quinate REASON: WRONGLY '
               'CLASSIFIED Contains a saturated cyclohexane ring with 1 '
               'carboxyl group and 4 oxygen substituents, consistent with a '
               'cyclitol carboxylic acid derivative.\n'
               ' * SMILES: '
               'O1[C@@]2(C[C@@](O)(C[C@@H](OC(=O)/C=C/C3=CC(O)=C(O)C=C3)[C@H]2O)C1=O)[H] '
               'NAME: 3-Caffeoyl-1,5-quinolactone REASON: WRONGLY CLASSIFIED '
               'Contains a saturated cyclohexane ring with 1 carboxyl group '
               'and 4 oxygen substituents, consistent with a cyclitol '
               'carboxylic acid derivative.\n'
               ' * SMILES: '
               '[H][C@]1(O)[C@H](O)C[C@@](O)(C[C@H]1OC(=O)\\C=C\\c1ccc(O)c(O)c1)C([O-])=O '
               'NAME: trans-5-O-caffeoyl-D-quinate REASON: WRONGLY CLASSIFIED '
               'Contains a saturated cyclohexane ring with 1 carboxyl group '
               'and 4 oxygen substituents, consistent with a cyclitol '
               'carboxylic acid derivative.\n'
               ' * SMILES: O[C@@H]1C[C@@](O)(C[C@@H](O)[C@H]1O)C([O-])=O NAME: '
               '(-)-quinate REASON: WRONGLY CLASSIFIED Contains a saturated '
               'cyclohexane ring with 1 carboxyl group and 4 oxygen '
               'substituents, consistent with a cyclitol carboxylic acid '
               'derivative.\n'
               ' * SMILES: '
               'O[C@@H]1C[C@](O)(C[C@@H](OC(=O)\\C=C\\c2ccc(O)c(O)c2)[C@@H]1O)C(O)=O '
               'NAME: chlorogenic acid REASON: WRONGLY CLASSIFIED Contains a '
               'saturated cyclohexane ring with 1 carboxyl group and 4 oxygen '
               'substituents, consistent with a cyclitol carboxylic acid '
               'derivative.\n'
               ' * SMILES: '
               'O1[C@@]2(C[C@@](O)(C[C@@H](OC(=O)/C=C/C3=CC(OC)=C(O)C=C3)[C@H]2O)C1=O)[H] '
               'NAME: 3-Feruloyl-1,5-quinolactone REASON: WRONGLY CLASSIFIED '
               'Contains a saturated cyclohexane ring with 1 carboxyl group '
               'and 4 oxygen substituents, consistent with a cyclitol '
               'carboxylic acid derivative.\n'
               ' * SMILES: '
               'O[C@@H]1C[C@](C[C@@H](OC(=O)\\C=C\\c2ccc(O)c(O)c2)[C@H]1O)(OC(=O)\\C=C\\c1ccc(O)c(O)c1)C([O-])=O '
               'NAME: 1,3-dicaffeoylquinate REASON: WRONGLY CLASSIFIED '
               'Contains a saturated cyclohexane ring with 1 carboxyl group '
               'and 4 oxygen substituents, consistent with a cyclitol '
               'carboxylic acid derivative.\n'
               ' * SMILES: '
               'O=C1O[C@@]2(O)[C@]3(OC([C@@H]2[C@@]4(OC=C(C4=O)C)[C@H](C3)C)=O)C(=C1)C '
               'NAME: Malettinin D REASON: WRONGLY CLASSIFIED Contains a '
               'saturated cyclohexane ring with 1 carboxyl group and 4 oxygen '
               'substituents, consistent with a cyclitol carboxylic acid '
               'derivative.\n'
               ' * SMILES: '
               'O(C1C[C@@](O)(C[C@@H](O)[C@H]1O)C(OC)=O)C(=O)/C=C/C2=CC(O)=C(O)C=C2 '
               'NAME: Methyl '
               '(1S,4R,5R)-3-[(E)-3-(3,4-dihydroxyphenyl)prop-2-enoyl]oxy-1,4,5-trihydroxycyclohexane-1-carboxylate '
               'REASON: WRONGLY CLASSIFIED Contains a saturated cyclohexane '
               'ring with 1 carboxyl group and 4 oxygen substituents, '
               'consistent with a cyclitol carboxylic acid derivative.\n'
               ' * SMILES: '
               'O=C1OC([C@@]2(C(=C)[C@@]34O[C@@H]3[C@]5(OC([C@]67O[C@@H]([C@H]2OC(=O)/C(=C/C)/CO)[C@@]4([C@@]7(C(=O)O[C@@H]6C)[C@@]5(O)C=O)C)=O)C)C=C1)(C)C '
               'NAME: Talaromytin REASON: WRONGLY CLASSIFIED Contains a '
               'saturated cyclohexane ring with 1 carboxyl group and 4 oxygen '
               'substituents, consistent with a cyclitol carboxylic acid '
               'derivative.\n'
               ' * SMILES: '
               'O[C@@H]1C[C@@](O)(C[C@@H](O)[C@H]1OC(=O)\\C=C\\C1=CC=C(O)C=C1)C(O)=O '
               'NAME: trans-4-p-coumaroylquinic acid REASON: WRONGLY '
               'CLASSIFIED Contains a saturated cyclohexane ring with 1 '
               'carboxyl group and 4 oxygen substituents, consistent with a '
               'cyclitol carboxylic acid derivative.\n'
               ' * SMILES: '
               'O=C1C2=C(O)C(C3=C(O)C4=C(O[C@]56C(=O)O[C@H]([C@@]5(C4=O)O)C[C@@H]([C@@H]6O)C)C=C3)=CC=C2O[C@@]78[C@]1(O)[C@@H](OC7=O)C[C@@H]([C@@H]8O)C '
               'NAME: Ergoflavin REASON: WRONGLY CLASSIFIED Contains a '
               'saturated cyclohexane ring with 1 carboxyl group and 4 oxygen '
               'substituents, consistent with a cyclitol carboxylic acid '
               'derivative.\n'
               ' * SMILES: COC1=CC(\\C=C/C(=O)OC2CC(O)(CC(O)C2O)C(O)=O)=CC=C1O '
               'NAME: cis-3-O-feruloylquinic acid REASON: WRONGLY CLASSIFIED '
               'Contains a saturated cyclohexane ring with 1 carboxyl group '
               'and 4 oxygen substituents, consistent with a cyclitol '
               'carboxylic acid derivative.\n'
               ' * SMILES: '
               'O1[C@@]2(C[C@@](O)(C[C@@H](O)[C@H]2OC(=O)/C=C/C3=CC=C(O)C=C3)C1=O)[H] '
               'NAME: 4-p-Coumaroyl-1,5-quinolactone REASON: WRONGLY '
               'CLASSIFIED Contains a saturated cyclohexane ring with 1 '
               'carboxyl group and 4 oxygen substituents, consistent with a '
               'cyclitol carboxylic acid derivative.\n'
               ' * SMILES: '
               'OC1C[C@@](O)(CC(OC(=O)\\C=C\\C2=CC(O)=C(O)C=C2)C1O)C(O)=O '
               'NAME: 5-O-trans-caffeoylquinic acid REASON: WRONGLY CLASSIFIED '
               'Contains a saturated cyclohexane ring with 1 carboxyl group '
               'and 4 oxygen substituents, consistent with a cyclitol '
               'carboxylic acid derivative.\n'
               'False negatives: NONE\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'C1=CC=C2C(=C1)C(=O)C3=CC=CC=C3C2(CC4=CC(=NC=C4)F)CC5=CC(=NC=C5)F',
                                     'name': '10,10-bis[(2-fluoro-4-pyridinyl)methyl]-9-anthracenone',
                                     'reason': 'No isolated saturated '
                                               'cyclohexane ring with one '
                                               '(neutral) carboxyl group and '
                                               'at least four oxygen '
                                               'substituents found'},
                                 {   'smiles': 'C[C@@H](C1=CC=CC=C1)NC(=O)[C@@H]2[C@H]([C@@H]3CN4C(=CC=C(C4=O)C5=CC=CC=C5F)[C@H]2N3C)CO',
                                     'name': 'LSM-10936',
                                     'reason': 'No isolated saturated '
                                               'cyclohexane ring with one '
                                               '(neutral) carboxyl group and '
                                               'at least four oxygen '
                                               'substituents found'},
                                 {   'smiles': '[H]C(=CC(=O)C(O)=O)C(CC(O)=O)C(O)=O',
                                     'name': '5-oxopent-3-ene-1,2,5-tricarboxylic '
                                             'acid',
                                     'reason': 'No isolated saturated '
                                               'cyclohexane ring with one '
                                               '(neutral) carboxyl group and '
                                               'at least four oxygen '
                                               'substituents found'},
                                 {   'smiles': 'S1N(C2=CC=C(C=C2)C(OCC)=O)C(=O)C=C1',
                                     'name': 'ethyl '
                                             '4-(3-oxo-2,3-dihydroisothiazol-2-yl)benzoate',
                                     'reason': 'No isolated saturated '
                                               'cyclohexane ring with one '
                                               '(neutral) carboxyl group and '
                                               'at least four oxygen '
                                               'substituents found'},
                                 {   'smiles': 'COc1cc(O)c2c(c1)oc1c(O)cccc1c2=O',
                                     'name': 'mesuaxanthone A',
                                     'reason': 'No isolated saturated '
                                               'cyclohexane ring with one '
                                               '(neutral) carboxyl group and '
                                               'at least four oxygen '
                                               'substituents found'},
                                 {   'smiles': 'O([C@@H]1[C@H](O)[C@@H](O[C@@H]([C@H]1O)CO[C@H]2O[C@@H]([C@@H](O)[C@H](O)[C@@H]2O[C@@H]3O[C@@H]([C@@H](O)[C@H](O)[C@H]3NC(=O)C)CO)CO[C@@H]4O[C@@H]([C@@H](O)[C@H](O)[C@H]4NC(=O)C)CO)O[C@H]5[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]5CO)O[C@H]6[C@H](O)[C@@H](NC(=O)C)C(O[C@@H]6CO)O)[C@H]7O[C@@H]([C@@H](O[C@@H]8O[C@@H]([C@@H](O)[C@H](O)[C@H]8NC(=O)C)CO)[C@H](O)[C@@H]7O[C@@H]9O[C@@H]([C@@H](O[C@@H]%10O[C@@H]([C@H](O)[C@H](O)[C@H]%10O)CO)[C@H](O)[C@H]9NC(=O)C)CO)CO',
                                     'name': 'N-[(3R,4R,5S,6R)-5-[(2S,3R,4R,5S,6R)-3-Acetamido-5-[(2S,3S,4S,5R,6R)-6-[[(2S,3S,4S,5S,6R)-3-[(2R,3R,4R,5S,6R)-3-acetamido-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-6-[[(2R,3R,4R,5S,6R)-3-acetamido-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxymethyl]-4,5-dihydroxyoxan-2-yl]oxymethyl]-4-[(2R,3S,4S,5S,6R)-5-[(2R,3R,4R,5S,6R)-3-acetamido-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-3-[(2S,3R,4R,5S,6R)-3-acetamido-4-hydroxy-6-(hydroxymethyl)-5-[(2S,3R,4S,5R,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-3,5-dihydroxyoxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-2,4-dihydroxy-6-(hydroxymethyl)oxan-3-yl]acetamide',
                                     'reason': 'No isolated saturated '
                                               'cyclohexane ring with one '
                                               '(neutral) carboxyl group and '
                                               'at least four oxygen '
                                               'substituents found'},
                                 {   'smiles': 'CCCCCCCC\\C=C/CCCCCCCC(=O)OC[C@H](COP([O-])(=O)OC[C@H]([NH3+])C([O-])=O)OC(=O)CCC\\C=C/C\\C=C/C\\C=C/C\\C=C/CCCCC',
                                     'name': '1-oleoyl-2-arachidonoyl-sn-glycero-3-phospho-L-serine(1-)',
                                     'reason': 'No isolated saturated '
                                               'cyclohexane ring with one '
                                               '(neutral) carboxyl group and '
                                               'at least four oxygen '
                                               'substituents found'},
                                 {   'smiles': 'OC(=Cc1ccccc1)C([O-])=O',
                                     'name': 'enol-phenylpyruvate',
                                     'reason': 'No isolated saturated '
                                               'cyclohexane ring with one '
                                               '(neutral) carboxyl group and '
                                               'at least four oxygen '
                                               'substituents found'},
                                 {   'smiles': '[H][C@]1(CC[C@]2(C)[C@@H](O)CCC(=C)[C@@]12[H])[C@@H](O)C(C)C',
                                     'name': '(1R,3aS,4S,7aR)-1-((S)-1-hydroxy-2-methylpropyl)-3a-methyl-7-methyleneoctahydro-1H-inden-4-ol',
                                     'reason': 'No isolated saturated '
                                               'cyclohexane ring with one '
                                               '(neutral) carboxyl group and '
                                               'at least four oxygen '
                                               'substituents found'},
                                 {   'smiles': 'O1C(C(O)C(O)C(O)C1CO)C=2C(=O)C=3C(O)=C(C4OC(C(O)C(O)C4O)CO)C(O)=CC3OC2C5=CC=C(OC)C=C5',
                                     'name': "3,6-Diglucopyranosyl-5,7-dihydroxy-4'-methoxyflavone",
                                     'reason': 'No isolated saturated '
                                               'cyclohexane ring with one '
                                               '(neutral) carboxyl group and '
                                               'at least four oxygen '
                                               'substituents found'}],
    'sample_false_negatives': [],
    'attempt': 2,
    'reasoning': 'Below is our reasoning before the code:\n'
                 '\n'
                 'We noticed that our previous quinic acid classifier was '
                 '“fooled” by molecules having a saturated cyclohexane ring '
                 'with one carboxyl and several oxygen substituents even '
                 'though that ring was fused to or part of a larger polycyclic '
                 'structure (for example gibberellins). In addition, one '
                 'false‐positive had a “–quinate” structure in which the '
                 'carboxyl group was anionic rather than neutral. To improve '
                 'performance we now add two extra checks. First, when a fully '
                 'saturated six‐membered ring is detected, we require that it '
                 'be “isolated” – that is, none of its carbon atoms are shared '
                 'with another ring (by checking that no other ring shares ≥2 '
                 'atoms with the candidate six‐membered ring). Second, when a '
                 'neighbor carbon is considered a carboxyl group, we further '
                 'check that its attached oxygen atoms are neutral (formal '
                 'charge zero). In this way we avoid misclassifying fused '
                 'rings from non–quinic acid classes and anionic forms of the '
                 'carboxyl group. The following Python code (using RDKit) '
                 'implements these improvements.\n'
                 '\n'
                 'Below is the complete code block:',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 25,
    'num_false_positives': 18,
    'num_true_negatives': 142257,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.5813953488372093,
    'recall': 1.0,
    'f1': 0.7352941176470588,
    'accuracy': 0.9998735066760366,
    'negative_predictive_value': 1.0}