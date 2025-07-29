"""
Classifies: CHEBI:39410 1,2,4-triazines
"""
"""
Classifies chemical entities of the class 1,2,4-triazines.
Definition: Any compound with a 1,2,4-triazine skeleton is characterized by a six-membered ring,
composed solely of carbon and nitrogen atoms (exactly three of each), and in which some cyclic permutation 
(forward or reverse) of the connectivity gives the pattern: N, N, C, N, C, C.
Additionally, we require that the 1,2,4-triazine ring is not fused with another ring.
"""

from rdkit import Chem

def is_1_2_4_triazines(smiles: str):
    """
    Determines if a molecule contains a 1,2,4-triazine skeleton based on its SMILES string.
    
    The skeleton is defined as a six-membered ring having exactly three nitrogens and three carbons,
    for which some cyclic permutation (forward or reverse) of the atoms (based solely on atomic number)
    matches the pattern [7, 7, 6, 7, 6, 6] (i.e. [N, N, C, N, C, C]). In addition, only non-fused (isolated)
    rings are accepted.
    
    Args:
        smiles (str): SMILES string of the molecule.
    
    Returns:
        bool: True if a 1,2,4-triazine core is found, False otherwise.
        str: Reason describing the classification outcome.
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
    
    # Get general ring information
    ring_info = mol.GetRingInfo()
    atom_rings = ring_info.AtomRings()  # each ring is a tuple of atom indices
    bond_rings = ring_info.BondRings()  # each ring is a tuple of bond indices

    # Helper: given the set/list of atom indices for a ring,
    # return an ordered list of its atoms (in connectivity order).
    def get_ordered_ring(mol, ring_indices):
        ring_set = set(ring_indices)
        # Build a dictionary: each atom idx -> list of neighbor indices that are also in the ring.
        neigh_dict = {}
        for idx in ring_indices:
            atom = mol.GetAtomWithIdx(idx)
            neighs = [nbr.GetIdx() for nbr in atom.GetNeighbors() if nbr.GetIdx() in ring_set]
            neigh_dict[idx] = neighs

        # Try to build an ordered cycle starting with the first atom
        start = ring_indices[0]
        if len(neigh_dict[start]) != 2:
            return None  # not a proper cycle
        for first in neigh_dict[start]:
            ordered = [start, first]
            while True:
                current = ordered[-1]
                prev = ordered[-2]
                # Among neighbors of current in the ring, choose one that is not prev
                next_atom = None
                for nbr in neigh_dict[current]:
                    if nbr != prev:
                        next_atom = nbr
                        break
                if next_atom is None:
                    break
                # if we returned to the start, break out (cycle complete)
                if next_atom == start:
                    break
                ordered.append(next_atom)
                if len(ordered) > len(ring_indices):
                    break
            if len(ordered) == len(ring_indices):
                # Return the list of atom objects in this order
                return [mol.GetAtomWithIdx(idx) for idx in ordered]
        return None

    # Given an ordered list of atoms from the ring, check if some cyclic permutation (forwards or reversed)
    # matches the pattern [7, 7, 6, 7, 6, 6] (N=7, C=6).
    def matches_pattern(ordered_atoms):
        pattern = [7, 7, 6, 7, 6, 6]
        n = len(pattern)
        # Check forward rotations:
        for r in range(n):
            rotated = [ordered_atoms[(r + i) % n] for i in range(n)]
            if all(rotated[i].GetAtomicNum() == pattern[i] for i in range(n)):
                return True
        # Check reversed rotations:
        reversed_atoms = list(reversed(ordered_atoms))
        for r in range(n):
            rotated = [reversed_atoms[(r + i) % n] for i in range(n)]
            if all(rotated[i].GetAtomicNum() == pattern[i] for i in range(n)):
                return True
        return False

    # Helper to check if a ring is "isolated", i.e. not fused.
    # Here we check that none of its bonds appear in any other ring.
    def is_ring_isolated(ordered_atoms):
        n = len(ordered_atoms)
        for i in range(n):
            a1 = ordered_atoms[i]
            a2 = ordered_atoms[(i+1) % n]
            bond = mol.GetBondBetweenAtoms(a1.GetIdx(), a2.GetIdx())
            if bond is None:
                return False
            bond_idx = bond.GetIdx()
            # Count in how many ring bond lists this bond index appears.
            count = sum(1 for ring in bond_rings if bond_idx in ring)
            if count > 1:
                # This bond is shared with another ring (fused)
                return False
        return True

    # Iterate over all six-membered rings in the molecule.
    for ring in atom_rings:
        if len(ring) != 6:
            continue  # only consider six-membered rings
        ordered_atoms = get_ordered_ring(mol, list(ring))
        if ordered_atoms is None or len(ordered_atoms) != 6:
            continue
        
        # Check atomic composition: exactly three nitrogens and three carbons
        atomic_nums = [atom.GetAtomicNum() for atom in ordered_atoms]
        if atomic_nums.count(7) != 3 or atomic_nums.count(6) != 3:
            continue

        # Check if the ring (ignoring aromaticity flags) matches the cyclic permutation pattern.
        if not matches_pattern(ordered_atoms):
            continue

        # Only accept rings that are isolated (non-fused)
        if not is_ring_isolated(ordered_atoms):
            continue

        return True, "Found 1,2,4-triazine ring pattern"
    
    return False, "No 1,2,4-triazine ring pattern found"

# Example usage (for debugging/verification):
if __name__ == '__main__':
    # List a few SMILES strings from the provided examples:
    test_smiles = [
        "C1=CC=C(C=C1)C2=CN=NC(=N2)C3=CC=CC=N3",  # 5-phenyl-3-(2-pyridinyl)-1,2,4-triazine (TP) -> expected True
        "CC1=NNC(=O)N(C1)\\N=C\\c1cccnc1",         # pymetrozine -> expected True
        "CN(C)C1=CC=C(C=C1)NC(=O)CN2C(=O)C3=CC4=CC=CC=C4N3C=N2"  # false positive example -> expected False
    ]
    for sm in test_smiles:
        result, reason = is_1_2_4_triazines(sm)
        print(f"SMILES: {sm}\nResult: {result}, Reason: {reason}\n")


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:39410',
                          'name': '1,2,4-triazines',
                          'definition': 'Any compound with a 1,2,4-triazine '
                                        'skeleton, in which nitrogen atoms '
                                        'replace carbon at positions 1, 2 and '
                                        '4 of the core benzene ring structure.',
                          'parents': ['CHEBI:38102'],
                          'xrefs': ['PMID:20194696'],
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
                                                 0,
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
                                                 0,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 3,
                                                 4,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 3,
                                                 4,
                                                 2,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 3,
                                                 3,
                                                 3,
                                                 3,
                                                 4,
                                                 3,
                                                 3,
                                                 3,
                                                 3,
                                                 4,
                                                 4,
                                                 2,
                                                 0,
                                                 1,
                                                 1,
                                                 2,
                                                 3,
                                                 2,
                                                 2,
                                                 3,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 0,
                                                 0,
                                                 0,
                                                 1,
                                                 1,
                                                 0,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 2,
                                                 1,
                                                 1,
                                                 2,
                                                 2],
                           'max_indent': 4,
                           'imports': ['from rdkit import Chem'],
                           'imports_count': 1,
                           'methods_called': [   'GetIdx',
                                                 'GetAtomicNum',
                                                 'MolFromSmiles',
                                                 'GetAtomWithIdx',
                                                 'AtomRings',
                                                 'GetBondBetweenAtoms',
                                                 'GetNeighbors',
                                                 'BondRings',
                                                 'GetRingInfo',
                                                 'count'],
                           'methods_called_count': 10,
                           'smarts_strings': [],
                           'smarts_strings_count': 0,
                           'defs': [   'is_1_2_4_triazines(smiles: str):',
                                       'get_ordered_ring(mol, ring_indices):',
                                       'matches_pattern(ordered_atoms):',
                                       'is_ring_isolated(ordered_atoms):'],
                           'defs_count': 4,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'True',
                                          'True',
                                          'False',
                                          'False',
                                          'False',
                                          'True',
                                          'False, "No 1,2,4-triazine ring '
                                          'pattern found"'],
                           'returns_count': 8,
                           'complexity': 6.086163359768663},
    'message': '\n'
               'Attempt failed: F1 score of 0.3546099290780142 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: C1=CC=C(C=C1)C2=CN=NC(=N2)C3=CC=CC=N3 '
               'NAME: 5-phenyl-3-(2-pyridinyl)-1,2,4-triazine REASON: CORRECT '
               'Found 1,2,4-triazine ring pattern\n'
               ' * SMILES: CSc1nnc(c(=O)n1N)C(C)(C)C NAME: metribuzin REASON: '
               'CORRECT Found 1,2,4-triazine ring pattern\n'
               ' * SMILES: Cc1nnc(-c2ccccc2)c(=O)n1N NAME: metamitron REASON: '
               'CORRECT Found 1,2,4-triazine ring pattern\n'
               ' * SMILES: N1=C(C)C(NC(N1)=O)=O NAME: 6-azathymine REASON: '
               'CORRECT Found 1,2,4-triazine ring pattern\n'
               ' * SMILES: CC1=NN2C(=NC1=O)NNC2=S NAME: '
               '6-methyl-3-sulfanylidene-1,2-dihydro-[1,2,4]triazolo[4,3-b][1,2,4]triazin-7-one '
               'REASON: CORRECT Found 1,2,4-triazine ring pattern\n'
               ' * SMILES: '
               'OS(=O)(=O)c1ccc(cc1)-c1nnc(nc1-c1ccc(cc1)S(O)(=O)=O)-c1ccccn1 '
               'NAME: ferrozine free acid REASON: CORRECT Found 1,2,4-triazine '
               'ring pattern\n'
               ' * SMILES: '
               'N1=C(C)C(NC(N1[C@@H]2O[C@H](COP(O)(=O)O)[C@H](C2)O)=O)=O NAME: '
               "6-azathymidine 5'-monophosphate REASON: CORRECT Found "
               '1,2,4-triazine ring pattern\n'
               ' * SMILES: c1cnncn1 NAME: 1,2,4-triazine REASON: CORRECT Found '
               '1,2,4-triazine ring pattern\n'
               ' * SMILES: Cc1nnc(-c2ccccc2)c(=O)[nH]1 NAME: '
               'metamitron-desamino REASON: CORRECT Found 1,2,4-triazine ring '
               'pattern\n'
               ' * SMILES: FC(F)(F)C=1C=CC(=NC1)C2=NC(=C(N=N2)C)C NAME: '
               '5,6-dimethyl-3-[5-(trifluoromethyl)pyridin-2-yl]-1,2,4-triazine '
               'REASON: CORRECT Found 1,2,4-triazine ring pattern\n'
               ' * SMILES: Nc1nnc(c(N)n1)-c1cccc(Cl)c1Cl NAME: lamotrigine '
               'REASON: CORRECT Found 1,2,4-triazine ring pattern\n'
               ' * SMILES: CC1=NNC(=NC1=O)NN=C(C)C(=O)O NAME: '
               '2-[(6-methyl-5-oxo-2H-1,2,4-triazin-3-yl)hydrazinylidene]propanoic '
               'acid REASON: CORRECT Found 1,2,4-triazine ring pattern\n'
               ' * SMILES: C1=CC=C(C=C1)C2=CN=C(N=N2)C3=CC=CC=N3 NAME: '
               '6-phenyl-3-(2-pyridinyl)-1,2,4-triazine REASON: CORRECT Found '
               '1,2,4-triazine ring pattern\n'
               ' * SMILES: '
               'N=1N(C(NC(C1)=O)=O)[C@@H]2O[C@@H]([C@H]([C@H]2OC(=O)C)OC(C)=O)COC(C)=O '
               'NAME: azaribine REASON: CORRECT Found 1,2,4-triazine ring '
               'pattern\n'
               ' * SMILES: CC1=CC(=NN1C2=NC(=CN=N2)C3=CC=CC=C3)C NAME: '
               '3-(3,5-dimethyl-1-pyrazolyl)-5-phenyl-1,2,4-triazine REASON: '
               'CORRECT Found 1,2,4-triazine ring pattern\n'
               ' * SMILES: [C@@H]1(N2C(NC(=O)C(=N2)C)=O)O[C@H](CO)[C@H](C1)O '
               'NAME: 6-azathymidine REASON: CORRECT Found 1,2,4-triazine ring '
               'pattern\n'
               ' * SMILES: O=C1N=C2N(C(=O)N(C2=NN1C)C)C NAME: '
               '2-methyl-fervenulone REASON: CORRECT Found 1,2,4-triazine ring '
               'pattern\n'
               ' * SMILES: '
               '[H][C@]12SCC(CSc3nc(=O)c(=O)[nH]n3C)=C(N1C(=O)[C@H]2NC(=O)C(=N/OC)\\c1csc(N)n1)C(O)=O '
               'NAME: ceftriaxone REASON: CORRECT Found 1,2,4-triazine ring '
               'pattern\n'
               ' * SMILES: O=c1cn[nH]c(=O)[nH]1 NAME: 6-azauracil REASON: '
               'CORRECT Found 1,2,4-triazine ring pattern\n'
               ' * SMILES: N=1C(=C(N=NC1C=2N=CC=CC2)C3=CC=CC=C3)C4=CC=CC=C4 '
               'NAME: 5,6-diphenyl-3-(2-pyridyl)-1,2,4-triazine REASON: '
               'CORRECT Found 1,2,4-triazine ring pattern\n'
               ' * SMILES: '
               'CC1=CC(=C(O1)C)C2=NC(=C(N=N2)C3=CC=CC=C3)C4=CC=CC=C4 NAME: '
               '3-(2,5-dimethyl-3-furanyl)-5,6-diphenyl-1,2,4-triazine REASON: '
               'CORRECT Found 1,2,4-triazine ring pattern\n'
               ' * SMILES: C1=CC=C(C=C1)C2=C(N=NC(=N2)C3=CC=NC=C3)C4=CC=CC=C4 '
               'NAME: 5,6-diphenyl-3-pyridin-4-yl-1,2,4-triazine REASON: '
               'CORRECT Found 1,2,4-triazine ring pattern\n'
               ' * SMILES: OC[C@H]1O[C@H]([C@H](O)[C@@H]1O)n1ncc(=O)[nH]c1=O '
               'NAME: 6-azauridine REASON: CORRECT Found 1,2,4-triazine ring '
               'pattern\n'
               ' * SMILES: '
               'C1=CC=C(C=C1)C2=CC=C(C=C2)CNC3=C(N=NC(=N3)C4=CC=CC=N4)C5=CC=CC=C5 '
               'NAME: ML228 REASON: CORRECT Found 1,2,4-triazine ring pattern\n'
               ' * SMILES: O(C1=CC=2N3N=CC=C3N=NC2C=C1)C(=O)N(C)C NAME: '
               'Benzo[E]pyrazolo[5,1-c][1,2,4]triazin-8-yl '
               'N,N-dimethylcarbamate REASON: CORRECT Found 1,2,4-triazine '
               'ring pattern\n'
               'False positives: SMILES: '
               'CN(C)C1=CC=C(C=C1)NC(=O)CN2C(=O)C3=CC4=CC=CC=C4N3C=N2 NAME: '
               'N-[4-(dimethylamino)phenyl]-2-(1-oxo-[1,2,4]triazino[4,5-a]indol-2-yl)acetamide '
               'REASON: WRONGLY CLASSIFIED Found 1,2,4-triazine ring pattern\n'
               ' * SMILES: CC1=CC=C(C=C1)C(=O)CSC2=NN3C(=O)C(=NN=C3S2)C(C)(C)C '
               'NAME: '
               '3-tert-butyl-7-[[2-(4-methylphenyl)-2-oxoethyl]thio]-[1,3,4]thiadiazolo[2,3-c][1,2,4]triazin-4-one '
               'REASON: WRONGLY CLASSIFIED Found 1,2,4-triazine ring pattern\n'
               ' * SMILES: CCOC(=O)C1=NNC(=S)NC1=O NAME: '
               '5-oxo-3-sulfanylidene-2H-1,2,4-triazine-6-carboxylic acid '
               'ethyl ester REASON: WRONGLY CLASSIFIED Found 1,2,4-triazine '
               'ring pattern\n'
               ' * SMILES: C1CC(OC1)CSC2=NC(=C(N=N2)C3=CC=CC=C3)C4=CC=CC=C4 '
               'NAME: 3-(2-oxolanylmethylthio)-5,6-diphenyl-1,2,4-triazine '
               'REASON: WRONGLY CLASSIFIED Found 1,2,4-triazine ring pattern\n'
               ' * SMILES: '
               'CC1=CC(=CC=C1)NC(=O)CSC2=NC(=C(N=N2)C3=CC=CO3)C4=CC=CO4 NAME: '
               '2-[[5,6-bis(2-furanyl)-1,2,4-triazin-3-yl]thio]-N-(3-methylphenyl)acetamide '
               'REASON: WRONGLY CLASSIFIED Found 1,2,4-triazine ring pattern\n'
               ' * SMILES: '
               'CC1=NN(C(=O)C2=CC3=C(N12)C=CC(=C3)OC)CC(=O)NCCCOC(C)C NAME: '
               '2-(8-methoxy-4-methyl-1-oxo-[1,2,4]triazino[4,5-a]indol-2-yl)-N-(3-propan-2-yloxypropyl)acetamide '
               'REASON: WRONGLY CLASSIFIED Found 1,2,4-triazine ring pattern\n'
               ' * SMILES: N1=CN=C2C(=N1)NC(NC2=O)=O NAME: '
               '1,6-didemethyltoxoflavin REASON: WRONGLY CLASSIFIED Found '
               '1,2,4-triazine ring pattern\n'
               ' * SMILES: CCN1C2=CC=CC=C2C3=C1N=C(N=N3)SCCCN4C5=CC=CC=C5NC4=O '
               'NAME: '
               '3-[3-[(5-ethyl-[1,2,4]triazino[5,6-b]indol-3-yl)thio]propyl]-1H-benzimidazol-2-one '
               'REASON: WRONGLY CLASSIFIED Found 1,2,4-triazine ring pattern\n'
               ' * SMILES: CCCCOC(=O)C(C)NC1=NNC(=S)NC1=O NAME: '
               '2-[(5-oxo-3-sulfanylidene-2H-1,2,4-triazin-6-yl)amino]propanoic '
               'acid butyl ester REASON: WRONGLY CLASSIFIED Found '
               '1,2,4-triazine ring pattern\n'
               ' * SMILES: CNC1=C(N=NC(=N1)C2=CC=CC=N2)C3=CC=CC=C3 NAME: '
               'N-methyl-6-phenyl-3-(2-pyridinyl)-1,2,4-triazin-5-amine '
               'REASON: WRONGLY CLASSIFIED Found 1,2,4-triazine ring pattern\n'
               ' * SMILES: C1COCCN1C2=NC(=C(N=N2)C3=CC=CC=C3)C4=CC=CC=C4 NAME: '
               '4-(5,6-diphenyl-1,2,4-triazin-3-yl)morpholine REASON: WRONGLY '
               'CLASSIFIED Found 1,2,4-triazine ring pattern\n'
               ' * SMILES: CC1=NN=C2N(C1=O)N=C(S2)SCC3=CC(=CC=C3)Cl NAME: '
               '7-[(3-chlorophenyl)methylthio]-3-methyl-[1,3,4]thiadiazolo[2,3-c][1,2,4]triazin-4-one '
               'REASON: WRONGLY CLASSIFIED Found 1,2,4-triazine ring pattern\n'
               ' * SMILES: '
               '[C@H]1(O[C@H](COP([O-])(=O)[O-])[C@H]([C@H]1O)O)N2C(NC(C=N2)=O)=O '
               "NAME: 6-azauridine 5'-monophosphate(2-) REASON: WRONGLY "
               'CLASSIFIED Found 1,2,4-triazine ring pattern\n'
               ' * SMILES: c1ccc2nncnc2c1 NAME: 1,2,4-benzotriazine REASON: '
               'WRONGLY CLASSIFIED Found 1,2,4-triazine ring pattern\n'
               ' * SMILES: '
               '[H+].[Na+].[O-]S(=O)(=O)c1ccc(cc1)-c1nnc(nc1-c1ccc(cc1)S([O-])(=O)=O)-c1ccccn1 '
               'NAME: ferrozine monosodium salt REASON: WRONGLY CLASSIFIED '
               'Found 1,2,4-triazine ring pattern\n'
               ' * SMILES: '
               'CCC1=NN(C(=O)C2=CC3=C(N21)C=CO3)C(C)C(=O)NC(C)CCC4=CC=CO4 '
               'NAME: '
               '2-(1-ethyl-4-oxo-3-furo[3,4]pyrrolo[3,5-c][1,2,4]triazinyl)-N-[4-(2-furanyl)butan-2-yl]propanamide '
               'REASON: WRONGLY CLASSIFIED Found 1,2,4-triazine ring pattern\n'
               ' * SMILES: '
               '[H]C(=O)CN1C(=O)C(=O)NN=C1S\\C=C\\C1=C(N2C(=O)[C@@H](NC(=O)C(=N/OC)\\C3=CSC(N)=N3)[C@@]2([H])SC1)C(O)=O '
               'NAME: ceftiolene REASON: WRONGLY CLASSIFIED Found '
               '1,2,4-triazine ring pattern\n'
               ' * SMILES: '
               'CC1=NNC(=NC1=O)SCC(=O)N2CCN(CC2)S(=O)(=O)C3=CC=C(C=C3)Cl NAME: '
               '3-[[2-[4-(4-chlorophenyl)sulfonyl-1-piperazinyl]-2-oxoethyl]thio]-6-methyl-2H-1,2,4-triazin-5-one '
               'REASON: WRONGLY CLASSIFIED Found 1,2,4-triazine ring pattern\n'
               ' * SMILES: '
               'CC1=CC=C(C=C1)CNC2=C(N=NC(=N2)C3=CC=CC=N3)C4=CC=CC=C4 NAME: '
               'N-[(4-methylphenyl)methyl]-6-phenyl-3-(2-pyridinyl)-1,2,4-triazin-5-amine '
               'REASON: WRONGLY CLASSIFIED Found 1,2,4-triazine ring pattern\n'
               ' * SMILES: '
               'C1=CC(=CC=C1C(C#N)C2=C(C=C(C=C2Cl)N3C(=O)NC(=O)C=N3)Cl)Cl '
               'NAME: '
               '2-(4-chlorophenyl)-2-[2,6-dichloro-4-(3,5-dioxo-1,2,4-triazin-2-yl)phenyl]acetonitrile '
               'REASON: WRONGLY CLASSIFIED Found 1,2,4-triazine ring pattern\n'
               ' * SMILES: '
               'C1=CC=C2C(=C1)C3=C(N2)N=C(N=N3)SCC(=O)NC4=CC=CC(=C4)C(F)(F)F '
               'NAME: '
               '2-(5H-[1,2,4]triazino[5,6-b]indol-3-ylthio)-N-[3-(trifluoromethyl)phenyl]acetamide '
               'REASON: WRONGLY CLASSIFIED Found 1,2,4-triazine ring pattern\n'
               ' * SMILES: '
               'ClC1=C(Cl)C=CC=C1C2=N[N+](=C(N)N=C2N)C3O[C@H](C(=O)O)[C@@H](O)[C@@H]([C@H]3O)O '
               'NAME: '
               '3,5-diamino-2-[(3S,4R,5R,6R)-6-carboxy-3,4,5-trihydroxyoxan-2-yl]-6-(2,3-dichlorophenyl)-1,2lambda5,4-triazin-2-ylium '
               'REASON: WRONGLY CLASSIFIED Found 1,2,4-triazine ring pattern\n'
               ' * SMILES: CC1=CC=CC2=C1NC3=C2N=NC(=N3)SCC=C NAME: '
               '6-methyl-3-(prop-2-enylthio)-5H-[1,2,4]triazino[5,6-b]indole '
               'REASON: WRONGLY CLASSIFIED Found 1,2,4-triazine ring pattern\n'
               ' * SMILES: '
               'CN(C1=CC=CC=C1)C(=O)COC2=NC(=C(N=N2)C3=CC=CS3)C4=CC=CS4 NAME: '
               '2-[(5,6-dithiophen-2-yl-1,2,4-triazin-3-yl)oxy]-N-methyl-N-phenylacetamide '
               'REASON: WRONGLY CLASSIFIED Found 1,2,4-triazine ring pattern\n'
               ' * SMILES: CCCCOC(=O)CNC1=NNC(=NC1=O)SCC(=O)OCC NAME: '
               '2-[[3-[(2-ethoxy-2-oxoethyl)thio]-5-oxo-2H-1,2,4-triazin-6-yl]amino]acetic '
               'acid butyl ester REASON: WRONGLY CLASSIFIED Found '
               '1,2,4-triazine ring pattern\n'
               'False negatives: SMILES: CC1=NNC(=O)N(C1)\\N=C\\c1cccnc1 NAME: '
               'pymetrozine REASON: MISSED No 1,2,4-triazine ring pattern '
               'found\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'O=C(N[C@@H](C(O)(C)C)C)[C@H]([C@@]1([C@@]2([C@@](CC1)(/C(/CCC2)=C/C=C\\3/C[C@@H](O)C[C@H](O)C3=C)[H])C)[H])C',
                                     'name': '1alpha,25-dihydroxy-24-oxo-23-azavitamin '
                                             'D2 / '
                                             '1alpha,25-dihydroxy-24-oxo-23-azaergocalciferol',
                                     'reason': 'No 1,2,4-triazine ring pattern '
                                               'found'},
                                 {   'smiles': 'CCCCCCCCCCCCCCCCCCC(O)C([O-])=O',
                                     'name': '2-hydroxyarachidate',
                                     'reason': 'No 1,2,4-triazine ring pattern '
                                               'found'},
                                 {   'smiles': 'C[C@@H](CN([C@@H](C)CO)C(=O)NC1=CC=C(C=C1)C(F)(F)F)[C@@H](CN(C)C(=O)C2CCOCC2)OC',
                                     'name': 'N-[(2S,3S)-4-[[(2S)-1-hydroxypropan-2-yl]-[[4-(trifluoromethyl)phenyl]carbamoyl]amino]-2-methoxy-3-methylbutyl]-N-methyloxane-4-carboxamide',
                                     'reason': 'No 1,2,4-triazine ring pattern '
                                               'found'},
                                 {   'smiles': 'CC(=O)CC\\C=C(/C)CCC=C(C)C',
                                     'name': 'geranyl acetone',
                                     'reason': 'No 1,2,4-triazine ring pattern '
                                               'found'},
                                 {   'smiles': 'O([C@H]1[C@H](O)[C@H](O[C@H](O)[C@H]1O)CO[C@H]2O[C@@H]([C@@H](O)[C@H](O)[C@@H]2O)CO)[C@H]3O[C@@H]([C@@H](O)[C@H](O)[C@@H]3O[C@H]4O[C@@H]([C@@H](O)[C@H](O)[C@@H]4O)CO)CO',
                                     'name': '(2S,3S,4S,5S,6R)-2-[[(2R,3R,4S,5S,6S)-4-[(2R,3S,4S,5S,6R)-4,5-Dihydroxy-6-(hydroxymethyl)-3-[(2R,3S,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-3,5,6-trihydroxyoxan-2-yl]methoxy]-6-(hydroxymethyl)oxane-3,4,5-triol',
                                     'reason': 'No 1,2,4-triazine ring pattern '
                                               'found'},
                                 {   'smiles': 'O=C(OC1=C(C(O)=C(C(=O)O)C(=C1C)C)C)C2=C(OC)C(=C(OC(=O)C3=C(O)C=C(O)C=C3C)C=C2C)C',
                                     'name': 'Thielavin Z5',
                                     'reason': 'No 1,2,4-triazine ring pattern '
                                               'found'},
                                 {   'smiles': '[C@@H]1([C@@H]([C@H]([C@@H]([C@H](O1)CO)O)O)NC(C)=O)O[C@@H]2[C@@H]([C@H](C(O[C@@H]2CO)O)O)O',
                                     'name': 'beta-D-GlcpNAc-(1->4)-D-Galp',
                                     'reason': 'No 1,2,4-triazine ring pattern '
                                               'found'},
                                 {   'smiles': 'CN(C)C(=O)C1=CC=C(C=C1)C2=CC=C(C=C2)[C@@H]3[C@H]4CN(CC(=O)N4[C@H]3CO)C(=O)CC5CC5',
                                     'name': '4-[4-[(6S,7R,8R)-4-(2-cyclopropyl-1-oxoethyl)-8-(hydroxymethyl)-2-oxo-1,4-diazabicyclo[4.2.0]octan-7-yl]phenyl]-N,N-dimethylbenzamide',
                                     'reason': 'No 1,2,4-triazine ring pattern '
                                               'found'},
                                 {   'smiles': 'CCCCCCCCCCCCCCCCCCCCC=C',
                                     'name': '1-docosene',
                                     'reason': 'No 1,2,4-triazine ring pattern '
                                               'found'},
                                 {   'smiles': 'C([C@@](OC(=O)CCC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)([H])COC(=O)CC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)OC(=O)CCCCC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC',
                                     'name': 'TG(22:5(7Z,10Z,13Z,16Z,19Z)/20:5(5Z,8Z,11Z,14Z,17Z)/22:6(4Z,7Z,10Z,13Z,16Z,19Z))[iso6]',
                                     'reason': 'No 1,2,4-triazine ring pattern '
                                               'found'}],
    'sample_false_negatives': [   {   'smiles': 'CC1=NN2C(=NC1=O)NNC2=S',
                                      'name': '6-methyl-3-sulfanylidene-1,2-dihydro-[1,2,4]triazolo[4,3-b][1,2,4]triazin-7-one',
                                      'reason': 'No 1,2,4-triazine ring '
                                                'pattern found'},
                                  {   'smiles': 'O=C1N=C2N(C(=O)N(C2=NN1C)C)C',
                                      'name': '2-methyl-fervenulone',
                                      'reason': 'No 1,2,4-triazine ring '
                                                'pattern found'},
                                  {   'smiles': 'O(C1=CC=2N3N=CC=C3N=NC2C=C1)C(=O)N(C)C',
                                      'name': 'Benzo[E]pyrazolo[5,1-c][1,2,4]triazin-8-yl '
                                              'N,N-dimethylcarbamate',
                                      'reason': 'No 1,2,4-triazine ring '
                                                'pattern found'}],
    'attempt': 4,
    'reasoning': 'Below is one possible solution. In my reasoning I noticed '
                 'that the previous approach’s strict aromaticity check and '
                 'lack of “ring isolation” testing led to many false positives '
                 '(for example in fused systems) while missing some rings (for '
                 'example in pymetrozine, where one of the ring bonds is not '
                 'flagged aromatic due to a keto substituent). To improve the '
                 'classifier I now (1) extract all six‐membered rings and '
                 'order their atoms, (2) verify that the ring contains exactly '
                 'three nitrogens and three carbons and that some cyclic '
                 'permutation (in either forward or reverse order) matches the '
                 'sequence [N, N, C, N, C, C] (using atomic numbers '
                 '7,7,6,7,6,6), and (3) reject rings that are “fused” (i.e. '
                 'share any bond with another ring). (A fused ring is '
                 'identified here by checking every bond making up the '
                 'candidate ring and counting how many times that bond appears '
                 'among all the molecule’s ring “bond lists”.) This way we '
                 'reject many false positives while still “catching” rings '
                 'like that in pymetrozine which may not meet a strict '
                 'aromaticity requirement. \n'
                 '\n'
                 'Below is the complete Python code:\n'
                 '\n'
                 '------------------------------------------------',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 23,
    'num_false_positives': 40,
    'num_true_negatives': 142234,
    'num_false_negatives': 3,
    'num_negatives': None,
    'precision': 0.36507936507936506,
    'recall': 0.8846153846153846,
    'f1': 0.5168539325842696,
    'accuracy': 0.9996978215038651,
    'negative_predictive_value': 0.9999789084415448}