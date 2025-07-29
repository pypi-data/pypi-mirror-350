"""
Classifies: CHEBI:166828 saccharolipid
"""
"""
Classifies: CHEBI saccharolipid (Lipids that contain a carbohydrate moiety.)

This version improves on the previous strategy by:
  1. Defining a sugar ring as a non‐aromatic 5– or 6–membered ring composed solely of C and O (and containing at least one O).
  2. For each sugar ring, examining all bonds (from ring atoms to external atoms) to see if the ring is covalently attached to a long alkyl (acyl) chain.
     – Strategy A: if attached via an oxygen (as in an ester bond sugar–O–C(=O)–R) then follow from the carbonyl carbon’s non‐carbonyl neighbor.
     – Strategy B: if attached directly (a C–C bond) then follow that chain.
     
A helper function “longest_alkyl_chain” is defined that obeys strict criteria:
   • Only sp3 (non‐aromatic) carbon atoms not belonging to any ring are included.
   • The search is limited to a contiguous segment (ignoring branches) using recursion.

If any sugar ring is found to have an attachment (via either strategy) to an acyl chain of at least 7 contiguous carbon atoms, the molecule is classified as a saccharolipid.
"""

from rdkit import Chem

def is_saccharolipid(smiles: str):
    """
    Determines if a molecule is a saccharolipid based on its SMILES string.
    A saccharolipid is defined as a lipid with a carbohydrate (sugar) moiety that is covalently attached
    (by an ester or direct C–C bond) to a long aliphatic chain (>= 7 contiguous sp3 non‐aromatic carbons).
    
    Args:
        smiles (str): SMILES string of the molecule.
    
    Returns:
        bool: True if saccharolipid, False otherwise.
        str: Reason for the classification.
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
    
    # ---------------------------------------------------------------------
    # Step 1. Identify candidate sugar rings.
    # Our sugar ring is defined as a 5- or 6-membered ring, all atoms are C or O,
    # at least one oxygen is present, and no atom is aromatic.
    ring_info = mol.GetRingInfo()
    sugar_rings = []
    for ring in ring_info.AtomRings():
        if len(ring) not in [5, 6]:
            continue
        atoms = [mol.GetAtomWithIdx(idx) for idx in ring]
        # Accept only rings with atoms that are carbon (6) or oxygen (8),
        # and require at least one oxygen.
        atomic_nums = [atom.GetAtomicNum() for atom in atoms]
        if all(num in (6,8) for num in atomic_nums) and any(num == 8 for num in atomic_nums):
            if not any(atom.GetIsAromatic() for atom in atoms):
                # Save as a set for fast membership test
                sugar_rings.append(set(ring))
    if not sugar_rings:
        return False, "No carbohydrate (sugar) moiety (non‐aromatic 5- or 6-membered ring of C/O) detected"
    
    # ---------------------------------------------------------------------
    # Helper: recursively find the longest chain of contiguous sp3, non-aromatic, non-ring carbons.
    def longest_alkyl_chain(atom_idx, exclude, visited=None):
        """
        Returns the length (number of carbons) of the longest contiguous chain starting
        from the given atom (which should be an sp3 carbon, non-ring) and not traversing atoms in 'exclude'.
        """
        if visited is None:
            visited = set()
        visited.add(atom_idx)
        atom = mol.GetAtomWithIdx(atom_idx)
        max_length = 1  # count the starting atom
        for nb in atom.GetNeighbors():
            nb_idx = nb.GetIdx()
            # Only follow if neighbor is carbon, not aromatic, sp3 and not in any ring.
            if nb_idx in visited or nb_idx in exclude:
                continue
            if (nb.GetAtomicNum() == 6 and 
                not nb.GetIsAromatic() and 
                nb.GetHybridization().name == "SP3" and
                not nb.IsInRing()):
                length = 1 + longest_alkyl_chain(nb_idx, exclude, visited.copy())
                if length > max_length:
                    max_length = length
        return max_length

    MIN_CHAIN_LENGTH = 7  # the threshold for a long acyl chain

    # ---------------------------------------------------------------------
    # Strategy evaluation: For each sugar ring, check all bonds from a ring atom to an external atom.
    found_attachment = False
    for ring in sugar_rings:
        for idx in ring:
            sugar_atom = mol.GetAtomWithIdx(idx)
            for nb in sugar_atom.GetNeighbors():
                nb_idx = nb.GetIdx()
                if nb_idx in ring:
                    continue  # neighbor is part of the sugar ring
                
                # Strategy A: Attachment via oxygen (as in an ester bond sugar–O–C(=O)–R)
                if nb.GetAtomicNum() == 8 and (not nb.GetIsAromatic()):
                    # nb is an oxygen bridging the sugar ring.
                    # Look at its neighbors (besides the sugar_atom) to see if one is a carbonyl carbon.
                    for o_nb in nb.GetNeighbors():
                        if o_nb.GetIdx() == idx:
                            continue
                        if o_nb.GetAtomicNum() == 6:
                            # Check if o_nb (the candidate carbonyl carbon) has a double-bonded oxygen.
                            has_carbonyl = False
                            for c_nb in o_nb.GetNeighbors():
                                # Look for an oxygen with a double bond to o_nb.
                                if c_nb.GetAtomicNum() == 8:
                                    bond = mol.GetBondBetweenAtoms(o_nb.GetIdx(), c_nb.GetIdx())
                                    if bond is not None and bond.GetBondTypeAsDouble() == 2.0:
                                        has_carbonyl = True
                                        break
                            if has_carbonyl:
                                # Now (in a typical ester) the acyl chain comes off o_nb (but not via its double-bonded oxygens).
                                # So check each neighbor of o_nb other than nb and sugar_atom:
                                for acyl_candidate in o_nb.GetNeighbors():
                                    candidate_idx = acyl_candidate.GetIdx()
                                    if candidate_idx in (nb.GetIdx(), idx):
                                        continue
                                    # We require candidate to be a carbon with sp3 geometry (i.e. part of the alkyl chain).
                                    if (acyl_candidate.GetAtomicNum() == 6 and 
                                        not acyl_candidate.GetIsAromatic() and 
                                        acyl_candidate.GetHybridization().name == "SP3" and
                                        not acyl_candidate.IsInRing()):
                                        chain_length = longest_alkyl_chain(candidate_idx, exclude=ring)
                                        if chain_length >= MIN_CHAIN_LENGTH:
                                            found_attachment = True
                                            break
                                if found_attachment:
                                    break
                    if found_attachment:
                        break
                # Strategy B: Direct C–C bond from sugar to an external aliphatic carbon.
                if nb.GetAtomicNum() == 6 and (not nb.GetIsAromatic()) and (nb.GetHybridization().name == "SP3") and (not nb.IsInRing()):
                    chain_length = longest_alkyl_chain(nb_idx, exclude=ring)
                    if chain_length >= MIN_CHAIN_LENGTH:
                        found_attachment = True
                        break
            if found_attachment:
                break
        if found_attachment:
            break

    if not found_attachment:
        return False, "Sugar moiety not covalently attached to a long acyl chain (>=7 contiguous sp3 carbons) by ester or direct C–C bond"
    else:
        return True, "Molecule contains a carbohydrate ring attached to a long acyl (lipid) chain"

# Example usage:
if __name__ == "__main__":
    # One example saccharolipid (taken from supplied examples)
    example_smiles = "CCCCCCCCCCCCC(=O)O[C@H]1[C@H](O)[C@@H](CO)O[C@H](O[C@H]2O[C@H](CO)[C@@H](O)[C@H](O)[C@H]2OS(O)(=O)=O)[C@@H]1OC(=O)CCCCCCCCCCCCCCC"
    result, reason = is_saccharolipid(example_smiles)
    print("Is saccharolipid?", result)
    print("Reason:", reason)


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:166828',
                          'name': 'saccharolipid',
                          'definition': 'Lipids that contain a carbohydrate '
                                        'moiety.',
                          'parents': ['CHEBI:18059'],
                          'xrefs': ['Wikipedia:Saccharolipid'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 124,
                           'log_lines_of_code': 4.820281565605037,
                           'indent_by_line': [   1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 1,
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
                                                 2,
                                                 3,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 4,
                                                 4,
                                                 1,
                                                 2,
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
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 3,
                                                 3,
                                                 4,
                                                 3,
                                                 4,
                                                 4,
                                                 4,
                                                 4,
                                                 4,
                                                 5,
                                                 2,
                                                 0,
                                                 1,
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
                                                 5,
                                                 4,
                                                 4,
                                                 4,
                                                 5,
                                                 5,
                                                 5,
                                                 6,
                                                 7,
                                                 6,
                                                 7,
                                                 7,
                                                 7,
                                                 8,
                                                 8,
                                                 9,
                                                 9,
                                                 10,
                                                 10,
                                                 7,
                                                 8,
                                                 8,
                                                 8,
                                                 9,
                                                 9,
                                                 10,
                                                 9,
                                                 9,
                                                 10,
                                                 10,
                                                 10,
                                                 10,
                                                 10,
                                                 11,
                                                 11,
                                                 8,
                                                 9,
                                                 5,
                                                 6,
                                                 4,
                                                 4,
                                                 5,
                                                 5,
                                                 6,
                                                 6,
                                                 3,
                                                 4,
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
                                                 1],
                           'max_indent': 11,
                           'imports': ['from rdkit import Chem'],
                           'imports_count': 1,
                           'methods_called': [   'copy',
                                                 'GetBondBetweenAtoms',
                                                 'GetAtomWithIdx',
                                                 'MolFromSmiles',
                                                 'GetIdx',
                                                 'GetAtomicNum',
                                                 'add',
                                                 'IsInRing',
                                                 'GetBondTypeAsDouble',
                                                 'append',
                                                 'GetRingInfo',
                                                 'GetNeighbors',
                                                 'GetIsAromatic',
                                                 'AtomRings',
                                                 'GetHybridization'],
                           'methods_called_count': 15,
                           'smarts_strings': [],
                           'smarts_strings_count': 0,
                           'defs': [   'is_saccharolipid(smiles: str):',
                                       'longest_alkyl_chain(atom_idx, exclude, '
                                       'visited=None):'],
                           'defs_count': 2,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "No carbohydrate (sugar) '
                                          'moiety (non‐aromatic 5- or '
                                          '6-membered ring of C/O) detected"',
                                          'max_length',
                                          'False, "Sugar moiety not covalently '
                                          'attached to a long acyl chain (>=7 '
                                          'contiguous sp3 carbons) by ester or '
                                          'direct C–C bond"',
                                          'True, "Molecule contains a '
                                          'carbohydrate ring attached to a '
                                          'long acyl (lipid) chain"'],
                           'returns_count': 5,
                           'complexity': 7.564056313121007},
    'message': '\n'
               'Attempt failed: F1 score of 0 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: NONE\n'
               'False positives: SMILES: '
               'O=C1O[C@@H](C(=O)OC)[C@@H](C1=C)CCCCCCC NAME: Pestalolide B '
               'REASON: WRONGLY CLASSIFIED Molecule contains a carbohydrate '
               'ring attached to a long acyl (lipid) chain\n'
               ' * SMILES: '
               'O1C(C1CC/C=C\\CCCCCCCCCCCCC2=CC(OC2=O)C)CCCCCCCCCCCC NAME: '
               'Epoxymurin B REASON: WRONGLY CLASSIFIED Molecule contains a '
               'carbohydrate ring attached to a long acyl (lipid) chain\n'
               ' * SMILES: '
               'O=C1O[C@H](CCCCCCCCCCCCC[C@H](OC2OC(C(O)C(C2O)OC3OC(C(O)C(C3O)O)CO)CO)C)[C@H](C1=C)C(=O)O '
               'NAME: (18R)-O-B-D-glucopyranosyl-(1-3)-B-D-glucopyranoside of '
               'murolic acid REASON: WRONGLY CLASSIFIED Molecule contains a '
               'carbohydrate ring attached to a long acyl (lipid) chain\n'
               ' * SMILES: O=C1O[C@H](CCCCCCCCCCCCCC(=O)C)C(C1C)C(=O)O NAME: '
               'Dihydromuronic acid REASON: WRONGLY CLASSIFIED Molecule '
               'contains a carbohydrate ring attached to a long acyl (lipid) '
               'chain\n'
               ' * SMILES: '
               'O1[C@](CC[C@@]1([C@H](O)CCCCCCCCCCC)[H])([C@H](O)CCCCCCCCCC[C@H]2OC(=O)[C@H](C2)CC(=O)C)[H] '
               'NAME: cis-Murisolinone REASON: WRONGLY CLASSIFIED Molecule '
               'contains a carbohydrate ring attached to a long acyl (lipid) '
               'chain\n'
               ' * SMILES: O=C1OC(CCCCCCCCCC(C)(C)C)C(C1C)C(=O)O NAME: '
               'Neodihydroprotolichesterinic acid REASON: WRONGLY CLASSIFIED '
               'Molecule contains a carbohydrate ring attached to a long acyl '
               '(lipid) chain\n'
               ' * SMILES: CCCCCCCCCCCCCCCCC(C(CCCCCCCCCCCCC1=CC(C)OC1=O)O)O '
               'NAME: artemoin D REASON: WRONGLY CLASSIFIED Molecule contains '
               'a carbohydrate ring attached to a long acyl (lipid) chain\n'
               ' * SMILES: '
               'Cl/C=C(\\CC1=CC=CC=C1)/C[C@H](O)CC[C@H](C[C@H]([C@H]2OC(=O)C=C(C2)OC)C)C '
               'NAME: Trichophycin B REASON: WRONGLY CLASSIFIED Molecule '
               'contains a carbohydrate ring attached to a long acyl (lipid) '
               'chain\n'
               ' * SMILES: '
               'O=C1N(OC)C(=C)C2=C1[C@H](O)[C@](O)(CO)[C@@H](O2)CCCCCCC NAME: '
               'Phyllostictine C REASON: WRONGLY CLASSIFIED Molecule contains '
               'a carbohydrate ring attached to a long acyl (lipid) chain\n'
               ' * SMILES: '
               'P(=O)(OP(=O)(O)O)(O[C@@H]1C(C2(O[C@H]([C@@H](C)[C@@H](C2)O)C/C=C/C=3N=C([C@H](CCNC(=O)[C@@H](O)[C@@H](O)[C@@H](N(C)C)COC)C)OC3)O[C@@H]1[C@@H](OC)C[C@H](O)[C@@H]([C@H](O)[C@@H](/C=C(/C(=C/C=C/C(=C\\[N+]#[C-])/C)/C)\\C)C)C)(C)C)O '
               'NAME: Phosphocalyculin A REASON: WRONGLY CLASSIFIED Molecule '
               'contains a carbohydrate ring attached to a long acyl (lipid) '
               'chain\n'
               ' * SMILES: '
               'O=C1O[C@@H](C(=O)O)[C@@]([C@H]1CCCCCCCCCCCC)(O)C(=O)O NAME: '
               'Cinatrin D REASON: WRONGLY CLASSIFIED Molecule contains a '
               'carbohydrate ring attached to a long acyl (lipid) chain\n'
               ' * SMILES: '
               'O=C\\1N(C(C)C(/C1=C(\\O)/C(=C/C(CC(CC(O)C(O)C(C(O)C(C(O)C(C(O)CC(O)C(C(O)C(C(O)CC(O)CC(O)CC(O)C(O)C(O)C(O)C(O)C[C@H]2O[C@](O)([C@@H](O)[C@H]([C@@H]2O)O)CC(O)CCCCCCCCC)C)C)C)C)C)C)C)/C)=O)C '
               'NAME: Aflastatin A REASON: WRONGLY CLASSIFIED Molecule '
               'contains a carbohydrate ring attached to a long acyl (lipid) '
               'chain\n'
               ' * SMILES: O1C(CCCCCCCCCCCC)CCC1=O NAME: '
               '5-Dodecyldihydro-2(3H)-furanone REASON: WRONGLY CLASSIFIED '
               'Molecule contains a carbohydrate ring attached to a long acyl '
               '(lipid) chain\n'
               ' * SMILES: O1[C@](CC[C@H](C1=O)C)(CCCCCCCCC)CO NAME: '
               'Malyngolide REASON: WRONGLY CLASSIFIED Molecule contains a '
               'carbohydrate ring attached to a long acyl (lipid) chain\n'
               ' * SMILES: '
               'O=C1C2=C(O[C@H]([C@@H](O)CCCCCC)C[C@H]2OC)[C@@H](O)CC1 NAME: '
               '4-epi-7-O-methylkoninginin D REASON: WRONGLY CLASSIFIED '
               'Molecule contains a carbohydrate ring attached to a long acyl '
               '(lipid) chain\n'
               ' * SMILES: '
               'O=C1O[C@@](C(=O)O)(CCCCCCCCCCCC)[C@@]([C@H]1O)(O)C(=O)O NAME: '
               'Cinatrin C1 REASON: WRONGLY CLASSIFIED Molecule contains a '
               'carbohydrate ring attached to a long acyl (lipid) chain\n'
               ' * SMILES: CC1C=C(CCCCCCCCCCCCCCCCC(C(CCCCCCCCCCCC)O)O)C(=O)O1 '
               'NAME: artemoin B REASON: WRONGLY CLASSIFIED Molecule contains '
               'a carbohydrate ring attached to a long acyl (lipid) chain\n'
               ' * SMILES: '
               'OC(CCCCCCCCCCCCCCC)C(O)CC/C=C\\CCCC(O)CCCCCC(O)CC1=CC(OC1=O)C '
               'NAME: Muricatenol REASON: WRONGLY CLASSIFIED Molecule contains '
               'a carbohydrate ring attached to a long acyl (lipid) chain\n'
               ' * SMILES: C1C(OC(CC1)CCCCCCCCCCCCCCC)=O NAME: meadowlactone '
               'REASON: WRONGLY CLASSIFIED Molecule contains a carbohydrate '
               'ring attached to a long acyl (lipid) chain\n'
               ' * SMILES: O1[C@@H](CCCCCCCC)C(C(C1=O)=C)C(O)=O NAME: '
               '(-)-trans-C75 REASON: WRONGLY CLASSIFIED Molecule contains a '
               'carbohydrate ring attached to a long acyl (lipid) chain\n'
               ' * SMILES: O=C1C=C(CCO)O[C@]1(CCCCCCCCCCCC)C NAME: '
               'Annulofuranone REASON: WRONGLY CLASSIFIED Molecule contains a '
               'carbohydrate ring attached to a long acyl (lipid) chain\n'
               ' * SMILES: '
               '[H][C@]12CC(=O)O[C@@]1(C)C[C@](C)(CCCCCCCC\\C=C\\C=C\\c1ccccc1)OO2 '
               'NAME: plakortolide P REASON: WRONGLY CLASSIFIED Molecule '
               'contains a carbohydrate ring attached to a long acyl (lipid) '
               'chain\n'
               ' * SMILES: O=C1C=C(CCCCCCC)O[C@@]1(O)CCCCCC NAME: '
               'Pseudopyronine B REASON: WRONGLY CLASSIFIED Molecule contains '
               'a carbohydrate ring attached to a long acyl (lipid) chain\n'
               ' * SMILES: '
               'O1C(C1CCCCCCCCCCCCC2=CC(OC2=O)C)CCC3OC3CC/C=C/CCCCCCCCCC NAME: '
               'Dieporeticenin REASON: WRONGLY CLASSIFIED Molecule contains a '
               'carbohydrate ring attached to a long acyl (lipid) chain\n'
               ' * SMILES: '
               'O=C1OC(=O)CC(=C1CCCCCCCCCCCCCCC=2C(=O)OC(C2C)=O)C(=O)O NAME: '
               'Skeletocutin A REASON: WRONGLY CLASSIFIED Molecule contains a '
               'carbohydrate ring attached to a long acyl (lipid) chain\n'
               'False negatives: SMILES: '
               'CCCCCCCCCCC[C@@H](O)CC(=O)N[C@H]1[C@@H](OP(O)(O)=O)O[C@H](CO[C@@H]2O[C@H](CO[C@@]3(C[C@@H](O[C@@]4(C[C@@H](O[C@@]5(C[C@@H](O)[C@@H](O)[C@H](O5)[C@H](O)CO)C(O)=O)[C@@H](O)[C@H](O4)[C@H](O)CO[C@@]4(C[C@@H](O)[C@@H](O)[C@H](O4)[C@H](O)CO)C(O)=O)C(O)=O)[C@@H](O)[C@H](O3)[C@H](O)CO)C(O)=O)[C@@H](OP(O)(O)=O)[C@H](OC(=O)C[C@H](O)CCCCCCCCCCC)[C@H]2NC(=O)C[C@H](O)CCCCCCCCCCC)[C@@H](O)[C@@H]1OC(=O)C[C@H](O)CCCCCCCCCCC '
               'NAME: '
               'alpha-Kdo-(2->8)-[alpha-Kdo-(2->4)]-alpha-Kdo-(2->4)-alpha-Kdo-(2->6)-lipid '
               'IVA REASON: MISSED Sugar (carbohydrate) moiety not covalently '
               'attached to a long acyl chain (>=7 contiguous aliphatic '
               'carbons) by ester or direct C–C bond\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCC[C@@H](O)[C@H](C)C[C@H](C)C[C@H](C)C[C@H](C)C[C@H](C)C[C@H](C)C[C@H](C)C[C@H](C)C(=O)O[C@H]1[C@H](O)[C@@H](CO)O[C@H](O[C@H]2O[C@H](CO)[C@@H](O)[C@H](O)[C@H]2OS([O-])(=O)=O)[C@@H]1OC(=O)CCCCCCCCCCCCCCC '
               'NAME: SL1278 REASON: MISSED Sugar (carbohydrate) moiety not '
               'covalently attached to a long acyl chain (>=7 contiguous '
               'aliphatic carbons) by ester or direct C–C bond\n'
               ' * SMILES: '
               '[C@H]1([C@@H]([C@H]([C@@H]([C@H](O1)CO)O)O)OS(=O)([O-])=O)O[C@@H]2[C@@H]([C@H]([C@@H]([C@H](O2)CO)O)O)OC(CCCCCCCCCCCCCCCCC)=O '
               "NAME: 2-O-sulfo-2'-O-stearoyl-alpha,alpha-trehalose(1-) "
               'REASON: MISSED Sugar (carbohydrate) moiety not covalently '
               'attached to a long acyl chain (>=7 contiguous aliphatic '
               'carbons) by ester or direct C–C bond\n'
               ' * SMILES: '
               '[C@H]1([C@H]([C@H]([C@@H]([C@H](O1)[C@H](CO)O)O)O)O)OC[C@@H]([C@H]2O[C@@H]([C@H]([C@H]([C@@H]2OP(O)(=O)O)O[C@@H]3[C@@H]([C@H]([C@@H]([C@H](O3)CO[C@@H]4[C@@H]([C@H]([C@H]([C@H](O4)CO)O)O)O)O)O)O)O)O[C@@H]5[C@@H]([C@H](O[C@@H]([C@H]5OP(=O)(O)O)[C@H](CO)O)O[C@@H]6[C@@H](C[C@](O[C@@]6([C@@H](CO)O)[H])(OC[C@@H]7[C@@H](OP(=O)(O)O)[C@H](OC(=O)C[C@@H](CCCCCCCCCCC)OC(=O)CCCCCCCCCCCCC)[C@@H](NC(=O)C[C@@H](CCCCCCCCCCC)OC(=O)CCCCCCCCCCC)[C@H](OC[C@@H]8[C@H]([C@@H]([C@H]([C@H](O8)OP(=O)(O)O)NC(=O)C[C@@H](CCCCCCCCCCC)O)OC(=O)C[C@@H](CCCCCCCCCCC)O)O)O7)C(O)=O)O[C@]9(C(O)=O)C[C@@H](O)[C@H]([C@](O9)([C@H](O)CO)[H])O)O)O '
               'NAME: '
               'galactosyl-glucosyl-heptosyl-(phosphoheptosyl)2-(KDO)2-lipid A '
               'REASON: MISSED Sugar (carbohydrate) moiety not covalently '
               'attached to a long acyl chain (>=7 contiguous aliphatic '
               'carbons) by ester or direct C–C bond\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCC(=O)O[C@H](CCCCCCCCCCC)CC(=O)O[C@@H]1[C@@H](NC(=O)C[C@@H](CCCCCCCCCCC)OC(=O)CCCCCCCCCCC)[C@H](OC[C@H]2O[C@H](OP(O)(=O)OP(O)(=O)OCCN)[C@H](NC(=O)C[C@H](O)CCCCCCCCCCC)[C@@H](OC(=O)C[C@H](O)CCCCCCCCCCC)[C@@H]2O)O[C@H](CO[C@@]2(C[C@@H](O)[C@@H](O[C@H]3O[C@H]([C@@H](O)CO)[C@@H](O[C@@H]4O[C@H](CO)[C@@H](O[C@@H]5O[C@H](CO)[C@H](O)[C@H](O[C@@H]6O[C@H](CO)[C@@H](O[C@@H]7O[C@H](CO)[C@H](O)[C@H](O)[C@H]7O)[C@H](O)[C@H]6NC(C)=O)[C@H]5O)[C@H](O)[C@H]4O)[C@H](O[C@H]4O[C@H]([C@@H](O)CO)[C@@H](O)[C@H](OP(O)(=O)OCCN)[C@@H]4O[C@H]4O[C@H](CO)[C@@H](O)[C@H](O)[C@H]4NC(C)=O)[C@@H]3O)[C@H](O2)[C@H](O)CO)C(O)=O)[C@H]1OP(O)(=O)OP(O)(O)=O '
               'NAME: '
               'beta-D-Galp-(1->4)-beta-D-GlcpNAc-(1->3)-beta-D-Galp-(1->4)-beta-D-Glcp-(1->4)-[alpha-D-GlcpNAc-(1->2)-3-PEA-L-alpha-D-Hepp-(1->3)]-L-alpha-D-Hepp-(1->5)-alpha-Kdo-(2->6)-(de-O-acylated '
               'lipid A) REASON: MISSED Sugar (carbohydrate) moiety not '
               'covalently attached to a long acyl chain (>=7 contiguous '
               'aliphatic carbons) by ester or direct C–C bond\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCC(=O)O[C@H](CCCCCCCCCCC)CC(=O)O[C@@H]1[C@@H](NC(=O)C[C@@H](CCCCCCCCCCC)OC(=O)CCCCCCCCCCC)[C@H](OC[C@H]2O[C@H](OP(O)(O)=O)[C@H](NC(=O)C[C@H](O)CCCCCCCCCCC)[C@@H](OC(=O)C[C@H](O)CCCCCCCCCCC)[C@@H]2O)O[C@H](CO)[C@H]1OP(O)(=O)OP(O)(=O)OCCN '
               "NAME: lipid A 4'-(2-aminoethyl diphosphate) REASON: MISSED "
               'Sugar (carbohydrate) moiety not covalently attached to a long '
               'acyl chain (>=7 contiguous aliphatic carbons) by ester or '
               'direct C–C bond\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCC[C@@H](C)\\C=C(/C)C(=O)O[C@H]1[C@H](O)[C@@H](CO)O[C@H](O[C@H]2O[C@H](CO)[C@@H](O)[C@H](O)[C@H]2OS(O)(=O)=O)[C@@H]1OC(=O)CCCCCCCCCCCCCCC '
               'NAME: '
               "3-O-[(2E,4R)-2,4-dimethyldocos-2-enoyl]-2-O-palmitoyl-2'-O-sulfo-alpha,alpha-trehalose "
               'REASON: MISSED Sugar (carbohydrate) moiety not covalently '
               'attached to a long acyl chain (>=7 contiguous aliphatic '
               'carbons) by ester or direct C–C bond\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCC(=O)O[C@H](CCCCCCCCCCC)CC(=O)O[C@@H]1[C@@H](NC(=O)C[C@@H](CCCCCCCCCCC)OC(=O)CCCCCCCCCCC)[C@H](OC[C@H]2O[C@H](OP(O)(=O)OP(O)(=O)OCCN)[C@H](NC(=O)C[C@H](O)CCCCCCCCCCC)[C@@H](OC(=O)C[C@H](O)CCCCCCCCCCC)[C@@H]2O)O[C@H](CO[C@@]2(C[C@@H](O)[C@@H](O[C@H]3O[C@H]([C@@H](O)CO)[C@@H](O)[C@H](O[C@H]4O[C@H]([C@@H](O)CO)[C@@H](O)[C@H](OP(O)(=O)OCCN)[C@@H]4O[C@H]4O[C@H](CO)[C@@H](O)[C@H](O)[C@H]4NC(C)=O)[C@@H]3O)[C@H](O2)[C@H](O)CO)C(O)=O)[C@H]1OP(O)(=O)OP(O)(O)=O '
               'NAME: '
               'alpha-D-GlcpNAc-(1->2)-3-PEA-L-alpha-D-Hepp-(1->3)-L-alpha-D-Hepp-(1->5)-alpha-Kdo-(2->6)-(de-O-acylated '
               'lipid A) REASON: MISSED Sugar (carbohydrate) moiety not '
               'covalently attached to a long acyl chain (>=7 contiguous '
               'aliphatic carbons) by ester or direct C–C bond\n'
               ' * SMILES: '
               '[H][C@@]1(O[C@@](C[C@@H](O)[C@H]1O)(O[C@@H]1C[C@@](OC[C@H]2O[C@@H](OC[C@H]3O[C@H](OP(O)(O)=O)[C@H](NC(=O)C[C@H](O)CCCCCCCCCCC)[C@@H](OC(=O)C[C@H](O)CCCCCCCCCCC)[C@@H]3O)[C@H](NC(=O)C[C@@H](CCCCCCCCCCC)OC(=O)CCCCCCCCCCC)[C@@H](OC(=O)C[C@@H](CCCCCCCCCCC)OC(=O)CCCCCCCCCCCCC)[C@@H]2OP(O)(O)=O)(O[C@]([H])([C@H](O)CO)[C@@H]1O[C@H]1O[C@H]([C@@H](O)CO)[C@@H](O)[C@H](O)[C@@H]1O)C(O)=O)C(O)=O)[C@H](O)CO '
               'NAME: heptosyl-(KDO)2-lipid A REASON: MISSED Sugar '
               '(carbohydrate) moiety not covalently attached to a long acyl '
               'chain (>=7 contiguous aliphatic carbons) by ester or direct '
               'C–C bond\n'
               ' * SMILES: '
               '[H][C@@]1(O[C@@](C[C@@H](O)[C@H]1O)(O[C@@H]1C[C@@](OC[C@H]2O[C@@H](OC[C@H]3O[C@H](OP(O)(O)=O)[C@H](NC(=O)C[C@H](O)CCCCCCCCCCC)[C@@H](OC(=O)C[C@H](O)CCCCCCCCCCC)[C@@H]3O)[C@H](NC(=O)C[C@@H](CCCCCCCCCCC)OC(=O)CCCCCCCCCCC)[C@@H](OC(=O)C[C@@H](CCCCCCCCCCC)OC(=O)CCCCCCCCCCCCC)[C@@H]2OP(O)(O)=O)(O[C@]([H])([C@H](O)CO)[C@@H]1O[C@H]1O[C@H](CO[C@@H]2O[C@H](CO)[C@@H](O)[C@H](O)[C@H]2O[C@H]2O[C@H](CO)[C@@H](O[C@@H]3O[C@H](CO)[C@H](O[C@H]4O[C@H](CO)[C@H](O)[C@H](O)[C@H]4O)[C@H](O)[C@H]3O)[C@H](O)[C@H]2O)[C@@H](O[C@@H]2O[C@H](CO)[C@@H](O)[C@H](O)[C@H]2O[C@H]2O[C@H](CO)[C@@H](O[C@@H]3O[C@H](CO)[C@H](O[C@H]4O[C@H](CO)[C@H](O)[C@H](O)[C@H]4O)[C@H](O)[C@H]3O)[C@H](O)[C@H]2NC(C)=O)[C@H](O[C@@H]2O[C@H](CO)[C@@H](O)[C@H](O)[C@H]2O)[C@H]1O)C(O)=O)C(O)=O)[C@H](O)CO '
               'NAME: '
               'alpha-D-Gal-(1->4)-beta-D-Gal-(1->4)-alpha-D-GlcNAc-(1->2)-beta-D-Glc-(1->4)-[beta-D-Glc-(1->3)]-[alpha-D-Gal-(1->4)-beta-D-Gal-(1->4)-alpha-D-Glc-(1->2)-beta-D-Glc-(1->6)]-alpha-D-Glc-(1->5)-[alpha-D-Kdo-(2->4)]-alpha-D-Kdo-(2->6)-Lipid '
               'A REASON: MISSED Sugar (carbohydrate) moiety not covalently '
               'attached to a long acyl chain (>=7 contiguous aliphatic '
               'carbons) by ester or direct C–C bond\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': '[H][C@@]12CCC3=C(C(=O)C[C@]4(C)[C@]([H])(CC[C@@]34[H])[C@H](C)CCC(=C)C(C)C)[C@@]1(C)CCC(=O)[C@H]2C',
                                     'name': 'Camphoratin H',
                                     'reason': 'No carbohydrate (sugar) moiety '
                                               '(non‐aromatic 5- or 6-membered '
                                               'ring of C/O) detected'},
                                 {   'smiles': 'OC1CC=2C(C3C(C4C(C(CC4)C(C)/C=C\\C(C)C)(CC3)C)CC2)(CC1)C',
                                     'name': '(3beta,22E)-26,27-Dinorergosta-5,22-dien-3-ol',
                                     'reason': 'No carbohydrate (sugar) moiety '
                                               '(non‐aromatic 5- or 6-membered '
                                               'ring of C/O) detected'},
                                 {   'smiles': 'COc1ccc(cc1)[C@@H]1CC(=O)c2c(O)c(C)c(O)c(C)c2O1',
                                     'name': 'matteucinol',
                                     'reason': 'No carbohydrate (sugar) moiety '
                                               '(non‐aromatic 5- or 6-membered '
                                               'ring of C/O) detected'},
                                 {   'smiles': 'O=C(N[C@@H](CC=1C=2C(NC1)=CC=CC2)C(=O)N[C@@H](C)C(O)=O)[C@@H](N)C(C)C',
                                     'name': 'Val-Trp-Ala',
                                     'reason': 'No carbohydrate (sugar) moiety '
                                               '(non‐aromatic 5- or 6-membered '
                                               'ring of C/O) detected'},
                                 {   'smiles': 'C[C@@H]1O[C@@H](OCCCCCCCC[C@@H](O)CC(O)=O)[C@H](O)C[C@H]1OC(=O)c1c[nH]c2ccccc12',
                                     'name': 'ibho#18',
                                     'reason': 'Sugar moiety not covalently '
                                               'attached to a long acyl chain '
                                               '(>=7 contiguous sp3 carbons) '
                                               'by ester or direct C–C bond'},
                                 {   'smiles': 'O([C@H]1[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]1CO)O[C@H]2[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]2CO)O)[C@@H]3O[C@@H]([C@@H](O)[C@H](O)[C@@H]3O)CO[C@H]4O[C@@H]([C@@H](O)[C@H](O)[C@@H]4O[C@@H]5O[C@@H]([C@@H](O[C@@H]6O[C@@H]([C@H](O)[C@H](O)[C@H]6O)CO)[C@H](O)[C@H]5NC(=O)C)CO)CO',
                                     'name': 'N-[(2R,3R,4R,5S,6R)-5-[(2S,3R,4R,5S,6R)-3-Acetamido-5-[(2S,3S,4S,5S,6R)-6-[[(2S,3S,4S,5S,6R)-3-[(2S,3R,4R,5S,6R)-3-acetamido-4-hydroxy-6-(hydroxymethyl)-5-[(2S,3R,4S,5R,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxymethyl]-3,4,5-trihydroxyoxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-2,4-dihydroxy-6-(hydroxymethyl)oxan-3-yl]acetamide',
                                     'reason': 'Sugar moiety not covalently '
                                               'attached to a long acyl chain '
                                               '(>=7 contiguous sp3 carbons) '
                                               'by ester or direct C–C bond'},
                                 {   'smiles': 'OC=1C=2N=C(C=CC2C=CC1)C',
                                     'name': '2-Methylquinolin-8-ol',
                                     'reason': 'No carbohydrate (sugar) moiety '
                                               '(non‐aromatic 5- or 6-membered '
                                               'ring of C/O) detected'},
                                 {   'smiles': 'O([C@@H]1O[C@@H]([C@H](O)[C@H](O)[C@H]1O[C@@H]2O[C@H]([C@@H](O)[C@@H](O)[C@@H]2O)C)CO)[C@@H]3C[C@@H](NC(=O)C)C(O[C@@H]3CO)O',
                                     'name': 'N-[(3R,5R,6R)-5-[(2R,3R,4S,5R,6R)-4,5-Dihydroxy-6-(hydroxymethyl)-3-[(2S,3S,4R,5S,6S)-3,4,5-trihydroxy-6-methyloxan-2-yl]oxyoxan-2-yl]oxy-2-hydroxy-6-(hydroxymethyl)oxan-3-yl]acetamide',
                                     'reason': 'Sugar moiety not covalently '
                                               'attached to a long acyl chain '
                                               '(>=7 contiguous sp3 carbons) '
                                               'by ester or direct C–C bond'},
                                 {   'smiles': 'O([C@H]1[C@@H](O)[C@H](O[C@@H](O[C@@H]2[C@@H](NC(=O)C)C(O[C@@H]([C@@H]2O)CO[C@@H]3O[C@@H]([C@@H](O)[C@H](O)[C@H]3NC(=O)C)CO)O)[C@@H]1O)CO[C@@H]4O[C@@H]([C@@H](O[C@@H]5O[C@@H]([C@H](O[C@H]6O[C@@H]([C@@H](O)[C@H](O)[C@H]6NC(=O)C)CO)[C@H](O)[C@H]5O)CO)[C@H](O)[C@H]4NC(=O)C)CO)[C@@H]7O[C@@H]([C@@H](O[C@@H]8O[C@@H]([C@H](O)[C@H](O)[C@H]8O[C@@H]9O[C@H]([C@@H](O)[C@@H](O)[C@@H]9O)C)CO)[C@H](O)[C@H]7NC(=O)C)CO',
                                     'name': 'N-[(2R,3R,4R,5S,6R)-2-[[(2R,3R,4R,5R)-5-Acetamido-4-[(2R,3R,4S,5S,6R)-6-[[(2R,3R,4R,5S,6R)-3-acetamido-5-[(2S,3R,4R,5R,6R)-5-[(2R,3R,4R,5S,6R)-3-acetamido-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-3,4-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxymethyl]-4-[(2S,3R,4R,5S,6R)-3-acetamido-5-[(2S,3R,4S,5R,6R)-4,5-dihydroxy-6-(hydroxymethyl)-3-[(2S,3S,4R,5S,6S)-3,4,5-trihydroxy-6-methyloxan-2-yl]oxyoxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-3,5-dihydroxyoxan-2-yl]oxy-3,6-dihydroxyoxan-2-yl]methoxy]-4,5-dihydroxy-6-(hydroxymethyl)oxan-3-yl]acetamide',
                                     'reason': 'Sugar moiety not covalently '
                                               'attached to a long acyl chain '
                                               '(>=7 contiguous sp3 carbons) '
                                               'by ester or direct C–C bond'},
                                 {   'smiles': 'S(CC[C@H](NC(=O)[C@@H](NC(=O)[C@@H](N)CCSC)CC=1C=2C(NC1)=CC=CC2)C(O)=O)C',
                                     'name': 'Met-Trp-Met',
                                     'reason': 'No carbohydrate (sugar) moiety '
                                               '(non‐aromatic 5- or 6-membered '
                                               'ring of C/O) detected'}],
    'sample_false_negatives': [   {   'smiles': 'CCCCCCCCCCCC(=O)CC(=O)N[C@H]1[C@H](O[C@H](CO[C@@H]2O[C@H](COC)[C@@H](OP(O)(O)=O)[C@H](OCC[C@@H](CCCCCCC)OC)[C@H]2NC(=O)CCCCCCCCC\\C=C/CCCCCC)[C@@H](O)[C@@H]1OCCCCCCCCCC)OP(O)(O)=O',
                                      'name': 'eritoran',
                                      'reason': 'Sugar moiety not covalently '
                                                'attached to a long acyl chain '
                                                '(>=7 contiguous sp3 carbons) '
                                                'by ester or direct C–C bond'},
                                  {   'smiles': 'OC[C@@H](O)C(=C)C(=O)OC[C@H]1OC(O)[C@H](O)[C@@H](O)[C@@H]1O',
                                      'name': '6-tuliposide B',
                                      'reason': 'Sugar moiety not covalently '
                                                'attached to a long acyl chain '
                                                '(>=7 contiguous sp3 carbons) '
                                                'by ester or direct C–C bond'},
                                  {   'smiles': 'O(C(C(CCCCCCCCCCCCCCCCCCCCCC)O)=O)[C@H](CCCCCCCCCCCCCCC)CC(N[C@H]1[C@@H](O[C@@H]([C@H]([C@@H]1O)OP(=O)(O)O)CO)OC[C@H]2O[C@@H]([C@@H]([C@H]([C@@H]2O)O)NC(C[C@@H](CCCCCCCCCCCCCCC)OC(C(O)CCCCCCCCCCCCCCCCCCCCCC)=O)=O)OP(=O)(O)O)=O',
                                      'name': 'lipid A-F',
                                      'reason': 'Sugar moiety not covalently '
                                                'attached to a long acyl chain '
                                                '(>=7 contiguous sp3 carbons) '
                                                'by ester or direct C–C bond'},
                                  {   'smiles': 'CCCCCCCCCCCCCCCCCCCCCCCCCCCCCC(O)C(CCCCCCCCCCCCCC)C(=O)OC[C@H]1OC(O)[C@H](O)[C@@H](O)[C@@H]1O',
                                      'name': 'glucose 6-monomycolate (C46)',
                                      'reason': 'Sugar moiety not covalently '
                                                'attached to a long acyl chain '
                                                '(>=7 contiguous sp3 carbons) '
                                                'by ester or direct C–C bond'},
                                  {   'smiles': 'O1[C@@H]([C@@H](O)[C@H](O)[C@@H](O)[C@@H]1O[C@@H]/2OC=C(C(\\C2=C/C)CC(OC[C@H]3O[C@@H](OCCC4=CC=C(O)C=C4)[C@H](O)[C@@H](O)[C@@H]3O)=O)C(OC)=O)CO',
                                      'name': 'Nuezhenide',
                                      'reason': 'Sugar moiety not covalently '
                                                'attached to a long acyl chain '
                                                '(>=7 contiguous sp3 carbons) '
                                                'by ester or direct C–C bond'},
                                  {   'smiles': 'CC(=O)OC[C@H]1O[C@@H](O)[C@H](O)[C@@H](O)[C@@H]1O',
                                      'name': '6-O-acetyl-beta-D-glucose',
                                      'reason': 'Sugar moiety not covalently '
                                                'attached to a long acyl chain '
                                                '(>=7 contiguous sp3 carbons) '
                                                'by ester or direct C–C bond'}],
    'attempt': 3,
    'reasoning': 'Below is one proposed revised solution. In our reasoning we '
                 'noted that the original attempt used two “strategies” but '
                 'its chain‐traversal routine was too “loose” (or too '
                 '“brittle”) in both finding long alkyl chains and excluding '
                 'sugar atoms. In our new solution we (1) restrict the sugar '
                 'definition to non‐aromatic 5– or 6–membered rings that '
                 'contain only carbon and oxygen and at least one oxygen, (2) '
                 'write a helper (recursive) routine that only “walks” along '
                 'contiguous sp³, non‐aromatic, non‐ring carbons (excluding '
                 'atoms known to be part of a sugar ring), and (3) modify the '
                 'two strategies. In “Strategy A” the code looks for an ester '
                 'linkage (pattern sugar–O–C(=O)–R) and then follows out from '
                 'the acyl “R” group (ignoring the sp² carbonyl carbon) to see '
                 'if a chain of at least seven carbons can be found. In '
                 '“Strategy B” the code looks directly for a C–C bond from the '
                 'sugar ring to an sp³ carbon that starts a long, linear alkyl '
                 'chain. (Of course, no single heuristic is perfect; further '
                 'refinements may be needed so that the false‐positive and '
                 'false‐negative rates are improved.) \n'
                 '\n'
                 'Below is the complete Python code block using rdkit:\n'
                 '\n'
                 '------------------------------------------------',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 60,
    'num_false_positives': 470,
    'num_true_negatives': 141764,
    'num_false_negatives': 6,
    'num_negatives': None,
    'precision': 0.11320754716981132,
    'recall': 0.9090909090909091,
    'f1': 0.20134228187919462,
    'accuracy': 0.9966549543218552,
    'negative_predictive_value': 0.99995767792904}