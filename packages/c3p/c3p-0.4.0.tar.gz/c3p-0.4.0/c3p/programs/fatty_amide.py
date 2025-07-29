"""
Classifies: CHEBI:29348 fatty amide
"""
#!/usr/bin/env python3
"""
Classifies: fatty amide

A fatty amide is defined as a monocarboxylic acid amide derived from a fatty acid.
Heuristic improvements in this version:
  1. Identify an amide (C(=O)N) group.
  2. From the carbonyl carbon, exclude the oxygen and the amide nitrogen and choose the acyl candidate.
  3. Walk in a linear (non–branched) manner along eligible (aliphatic, nonaromatic, non‐ring) carbons.
     A qualifying acyl chain must contain at least 4 contiguous carbons.
  4. Verify that the acyl chain accounts for at least a minimum fraction (here 20%) of all heavy atoms.
  5. Check that the substituent attached to the amide N (besides the carbonyl partner) is “small” (fewer than 20 heavy atoms).
If no qualifying amide group is found, the program returns False with an explanation.
"""
from rdkit import Chem

def is_fatty_amide(smiles: str):
    """
    Determines whether the given SMILES string corresponds to a fatty amide.
    The molecule must contain a C(=O)N group where:
      - The substituent on the carbonyl carbon (the acyl portion) is a contiguous linear chain
        of at least 4 aliphatic carbons (nonaromatic, non‐ring) and this chain represents a significant part of the molecule (at least 20% of heavy atoms).
      - Additionally, the substituent on the amide nitrogen (aside from the carbonyl carbon) should be relatively small (<20 heavy atoms).
      
    Args:
      smiles (str): The SMILES string of the molecule.
      
    Returns:
      (bool, str): A tuple of a boolean and an explanatory string.
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
    
    # Build heavy atoms count for later: count atoms with atomic number > 1.
    total_heavy = sum(1 for atom in mol.GetAtoms() if atom.GetAtomicNum() > 1)

    # Define a SMARTS to find an amide group: carbonyl carbon (index 0), carbonyl oxygen (index 1), and amide nitrogen (index 2)
    amide_pattern = Chem.MolFromSmarts("C(=O)N")
    amide_matches = mol.GetSubstructMatches(amide_pattern)
    if not amide_matches:
        return False, "No amide (C(=O)N) functional group found"
    
    # An iterative function to “walk” along a linear chain.
    def linear_chain_length(start_idx, parent_idx):
        """
        Walks (iteratively) from start_idx (attached to parent_idx) along a chain of carbon atoms.
        Only nonaromatic, nonring carbons are allowed. The walk stops if more than one eligible neighbor is encountered.
        Returns (length, chain_atom_indices) where length includes the starting atom.
        """
        chain = [start_idx]
        current_idx = start_idx
        prev_idx = parent_idx
        while True:
            current_atom = mol.GetAtomWithIdx(current_idx)
            # Get eligible neighbors: must be carbon, nonaromatic, not in a ring, and not the one we came from.
            eligible = []
            for nbr in current_atom.GetNeighbors():
                nbr_idx = nbr.GetIdx()
                if nbr_idx == prev_idx:
                    continue
                if nbr.GetAtomicNum() != 6:
                    continue
                if nbr.GetIsAromatic() or nbr.IsInRing():
                    continue
                eligible.append(nbr_idx)
            # For a linear (non‐branched) chain, there should be exactly one eligible neighbor.
            if len(eligible) == 1:
                chain.append(eligible[0])
                prev_idx, current_idx = current_idx, eligible[0]
            else:
                break
        return len(chain), chain

    # A DFS to count the size of the fragment (the amine substituent) attached to the amide nitrogen.
    def count_heavy_atoms(atom_idx, excluded, visited):
        visited = visited | {atom_idx}
        count = 1  # count this atom
        atom = mol.GetAtomWithIdx(atom_idx)
        for nbr in atom.GetNeighbors():
            nbr_idx = nbr.GetIdx()
            if nbr_idx in visited or nbr_idx in excluded:
                continue
            if mol.GetAtomWithIdx(nbr_idx).GetAtomicNum() == 1:  # skip hydrogens
                continue
            count += count_heavy_atoms(nbr_idx, excluded, visited)
        return count

    # We set a threshold for the amine substituent size.
    AMINE_SIZE_THRESHOLD = 20
    # We also require that the acyl chain represents at least this fraction of all heavy atoms.
    ACYL_FRACTION_THRESHOLD = 0.20
    reasons = []
    
    for match in amide_matches:
        carbonyl_idx = match[0]
        oxy_idx = match[1]
        amideN_idx = match[2]
        carbonyl_atom = mol.GetAtomWithIdx(carbonyl_idx)
        # Determine acyl candidate(s): the neighbors of the carbonyl carbon, except the oxygen and the amide nitrogen.
        neighbors = [nbr.GetIdx() for nbr in carbonyl_atom.GetNeighbors()]
        acyl_candidates = [n for n in neighbors if n not in (oxy_idx, amideN_idx)]
        if not acyl_candidates:
            reasons.append("Amide group present but no acyl substituent attached to the carbonyl carbon.")
            continue
        
        acyl_chain_ok = False
        acyl_reason = ""
        for candidate in acyl_candidates:
            candidate_atom = mol.GetAtomWithIdx(candidate)
            # Candidate must be carbon, nonaromatic, and not in a ring.
            if candidate_atom.GetAtomicNum() != 6:
                continue
            if candidate_atom.GetIsAromatic() or candidate_atom.IsInRing():
                continue
            # Walk along the supposed acyl chain.
            chain_length, chain_atoms = linear_chain_length(candidate, carbonyl_idx)
            if chain_length < 4:
                acyl_reason = f"Found amide group but acyl chain only has {chain_length} contiguous aliphatic carbons (need at least 4)."
                continue
            # Check that the chain represents a significant fraction of the molecule.
            if chain_length / total_heavy < ACYL_FRACTION_THRESHOLD:
                acyl_reason = f"Acyl chain ({chain_length} carbons) is too small a fraction of the molecule (fraction {chain_length/total_heavy:.2f}; needed ≥ {ACYL_FRACTION_THRESHOLD})."
                continue
            # If we pass both tests then we have a qualifying acyl chain.
            acyl_chain_ok = True
            acyl_reason = f"Found amide group with an acyl chain of {chain_length} contiguous aliphatic carbons."
            break
        
        if not acyl_chain_ok:
            reasons.append(acyl_reason)
            continue
        
        # Now check the N‐side (amine substituent) size.
        amideN_atom = mol.GetAtomWithIdx(amideN_idx)
        # Exclude the carbonyl carbon.
        n_neighbors = [nbr.GetIdx() for nbr in amideN_atom.GetNeighbors() if nbr.GetIdx() != carbonyl_idx]
        amine_size = 0
        for nbr in n_neighbors:
            amine_size += count_heavy_atoms(nbr, {carbonyl_idx}, set())
        if amine_size > AMINE_SIZE_THRESHOLD:
            reasons.append(f"Acyl chain qualifies, but the amine fragment attached to the amide nitrogen is too large ({amine_size} heavy atoms; threshold {AMINE_SIZE_THRESHOLD}).")
            continue
        
        # If we reach here for any amide match, we classify the molecule as a fatty amide.
        return True, acyl_reason

    if reasons:
        # Return the first encountered reason.
        return False, reasons[0]
    else:
        return False, "No fatty amide (with a qualifying fatty acyl chain) found."

# Example usage:
if __name__ == '__main__':
    test_smiles = [
        "NC(CCCCCCCCCCCCCCC)=O",         # hexadecanamide: expected True
        "O=C(NCCC1=CC=CC=C1)CCCC",         # N-(2-phenylethyl)pentanamide: expected True
        "CCCCCCCC(=O)NCCO",               # N-(octanoyl)ethanolamine: expected True
        "CCCCCCCCCCCC(N)=O",              # dodecanamide: expected True
        "CC\\C=C/C\\C=C/C\\C=C/CCCCCCCC(=O)Nc1ccccc1",  # linolenic acid anilide: expected True
        "O=C(NCC[NH3+])C[C@](CC(=O)NC[C@@H](C([O-])=O)[NH3+])(C([O-])=O)O" # example false positive from peptides
    ]
    for smi in test_smiles:
        flag, reason = is_fatty_amide(smi)
        print(f"SMILES: {smi}\nResult: {flag}\nReason: {reason}\n")


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:29348',
                          'name': 'fatty amide',
                          'definition': 'A monocarboxylic acid amide derived '
                                        'from a fatty acid.',
                          'parents': ['CHEBI:29347', 'CHEBI:61697'],
                          'xrefs': ['KEGG:C02244', 'LIPID_MAPS_class:LMFA08'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 133,
                           'log_lines_of_code': 4.890349128221754,
                           'indent_by_line': [   1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
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
                                                 1,
                                                 1,
                                                 1,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 1,
                                                 1,
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
                                                 3,
                                                 3,
                                                 3,
                                                 3,
                                                 4,
                                                 4,
                                                 5,
                                                 4,
                                                 5,
                                                 4,
                                                 5,
                                                 4,
                                                 3,
                                                 3,
                                                 4,
                                                 4,
                                                 3,
                                                 4,
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
                                                 3,
                                                 4,
                                                 3,
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
                                                 2,
                                                 2,
                                                 2,
                                                 2,
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
                                                 4,
                                                 3,
                                                 4,
                                                 3,
                                                 3,
                                                 3,
                                                 4,
                                                 4,
                                                 3,
                                                 3,
                                                 4,
                                                 4,
                                                 3,
                                                 3,
                                                 3,
                                                 3,
                                                 2,
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
                                                 3,
                                                 2,
                                                 3,
                                                 3,
                                                 2,
                                                 2,
                                                 2,
                                                 0,
                                                 1,
                                                 2,
                                                 2,
                                                 1,
                                                 2,
                                                 0,
                                                 1,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 1,
                                                 1,
                                                 2,
                                                 2],
                           'max_indent': 5,
                           'imports': ['from rdkit import Chem'],
                           'imports_count': 1,
                           'methods_called': [   'GetIdx',
                                                 'GetIsAromatic',
                                                 'GetAtomicNum',
                                                 'MolFromSmiles',
                                                 'GetAtomWithIdx',
                                                 'GetAtoms',
                                                 'MolFromSmarts',
                                                 'GetNeighbors',
                                                 'append',
                                                 'IsInRing',
                                                 'GetSubstructMatches'],
                           'methods_called_count': 11,
                           'smarts_strings': ['C(=O)N'],
                           'smarts_strings_count': 1,
                           'defs': [   'is_fatty_amide(smiles: str):',
                                       'linear_chain_length(start_idx, '
                                       'parent_idx):',
                                       'count_heavy_atoms(atom_idx, excluded, '
                                       'visited):'],
                           'defs_count': 3,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "No amide (C(=O)N) '
                                          'functional group found"',
                                          'len(chain), chain',
                                          'count',
                                          'True, acyl_reason',
                                          'False, reasons[0]',
                                          'False, "No fatty amide (with a '
                                          'qualifying fatty acyl chain) '
                                          'found."'],
                           'returns_count': 7,
                           'complexity': 6.178069825644351},
    'message': '\n'
               'Attempt failed: F1 score of 0.06936026936026936 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: NC(CCCCCCCCCCCCCCC)=O NAME: '
               'hexadecanamide REASON: CORRECT Found amide group with an acyl '
               'chain of 15 contiguous aliphatic carbons.\n'
               ' * SMILES: O=C(NCCC1=CC=CC=C1)CCCC NAME: '
               'N-(2-phenylethyl)pentanamide REASON: CORRECT Found amide group '
               'with an acyl chain of 4 contiguous aliphatic carbons.\n'
               ' * SMILES: CCCCCCCC(=O)NCCO NAME: N-(octanoyl)ethanolamine '
               'REASON: CORRECT Found amide group with an acyl chain of 7 '
               'contiguous aliphatic carbons.\n'
               ' * SMILES: CCCCCCCCCCCC(N)=O NAME: dodecanamide REASON: '
               'CORRECT Found amide group with an acyl chain of 11 contiguous '
               'aliphatic carbons.\n'
               ' * SMILES: CC\\C=C/C\\C=C/C\\C=C/CCCCCCCC(=O)Nc1ccccc1 NAME: '
               'linolenic acid anilide REASON: CORRECT Found amide group with '
               'an acyl chain of 17 contiguous aliphatic carbons.\n'
               ' * SMILES: O=C(NCC(C)C)/C=C/C=C\\CCCCC NAME: '
               '(2E,4Z)-N-Isobutyl-2,4-decadienamide REASON: CORRECT Found '
               'amide group with an acyl chain of 9 contiguous aliphatic '
               'carbons.\n'
               ' * SMILES: O=C(NCCCCN)CCCCCCCCCCCCCCC NAME: '
               'Palmitoylputrescine REASON: CORRECT Found amide group with an '
               'acyl chain of 15 contiguous aliphatic carbons.\n'
               ' * SMILES: CCCCCC=CCC=CCCCCCCCC(=O)N NAME: '
               'octadeca-9,12-dienamide REASON: CORRECT Found amide group with '
               'an acyl chain of 17 contiguous aliphatic carbons.\n'
               ' * SMILES: '
               'O[C@@H]([C@@H](NC(=O)CCCCCCCCCCCCCCC/C=C\\CCCCCCCC)C)\\C=C\\CCCCCCCCCCCCC '
               'NAME: Cer(m18:1(4E)/26:1(17Z)) REASON: CORRECT Found amide '
               'group with an acyl chain of 25 contiguous aliphatic carbons.\n'
               ' * SMILES: CCCCC\\C=C\\C=C\\C(=O)NCC(C)C NAME: pellitorine '
               'REASON: CORRECT Found amide group with an acyl chain of 9 '
               'contiguous aliphatic carbons.\n'
               ' * SMILES: C(CCCCCCCCCC)CCCCC(NCC(O)=O)=O NAME: '
               'N-hexadecanoylglycine REASON: CORRECT Found amide group with '
               'an acyl chain of 15 contiguous aliphatic carbons.\n'
               ' * SMILES: CCCCC\\C=C/C\\C=C/CCCCCCCCCC(=O)NCCO NAME: '
               'N-(11Z,14Z)-eicosadienoylethanolamine REASON: CORRECT Found '
               'amide group with an acyl chain of 19 contiguous aliphatic '
               'carbons.\n'
               ' * SMILES: '
               'CCC(C)\\C=C(/C)[C@H](O)[C@H](C)\\C=C(C)\\C=C\\C=C/C=C/C=C(\\C)C(=O)N[C@@H](C)CO '
               'NAME: Myxalamid A REASON: CORRECT Found amide group with an '
               'acyl chain of 17 contiguous aliphatic carbons.\n'
               ' * SMILES: O=C(NC1CC1)/C=C/CC/C=C\\CC NAME: '
               'N-Cyclopropyl-trans-2-cis-6-nonadienamide REASON: CORRECT '
               'Found amide group with an acyl chain of 8 contiguous aliphatic '
               'carbons.\n'
               ' * SMILES: '
               'C(\\CCCCCCCC(=O)N[C@H](C(O)=O)[C@H](CC)C)=C\\CCCCCCCC NAME: '
               'N-oleoyl-L-isoleucine REASON: CORRECT Found amide group with '
               'an acyl chain of 17 contiguous aliphatic carbons.\n'
               ' * SMILES: O(O)C(CCCCCCC/C=C/C=C/C(=O)NCC(C)C)/C=C/CCCCC NAME: '
               '(2E,4E,14E)-13-Hydroperoxy-N-(2-methylpropyl)icosa-2,4,14-trienamide '
               'REASON: CORRECT Found amide group with an acyl chain of 19 '
               'contiguous aliphatic carbons.\n'
               ' * SMILES: Cl/C=C(/C/C=C/CCC(=O)NCCC(C)C)\\CCC NAME: '
               'Credneramide B REASON: CORRECT Found amide group with an acyl '
               'chain of 9 contiguous aliphatic carbons.\n'
               ' * SMILES: C(\\CCCCCCCC(=O)N[C@H](C(O)=O)CO)=C\\CCCCCCCC NAME: '
               'N-oleoyl-L-serine REASON: CORRECT Found amide group with an '
               'acyl chain of 17 contiguous aliphatic carbons.\n'
               ' * SMILES: CCCCCCCC\\C=C/CCCCCCCCCC(=O)NCCO NAME: '
               'N-gondoylethanolamine REASON: CORRECT Found amide group with '
               'an acyl chain of 19 contiguous aliphatic carbons.\n'
               ' * SMILES: O=C(N[C@H](CO)CC(C)C)\\C(=C/C=C/C)\\C NAME: '
               'Dichotomocej A REASON: CORRECT Found amide group with an acyl '
               'chain of 5 contiguous aliphatic carbons.\n'
               ' * SMILES: C(CCCCC/C=C\\C/C=C\\CCCCC)CCCC(N)=O NAME: '
               '(11Z,14Z)-icosadienamide REASON: CORRECT Found amide group '
               'with an acyl chain of 19 contiguous aliphatic carbons.\n'
               ' * SMILES: CCCCCC=CCC=CCC=CCC=CCCCC(=O)N NAME: '
               'eicosa-5,8,11,14-tetraenamide REASON: CORRECT Found amide '
               'group with an acyl chain of 19 contiguous aliphatic carbons.\n'
               ' * SMILES: C(CCCCCCC(=O)NCC(O)=O)CCCCCCCCCCCCCC NAME: '
               'N-docosanoylglycine REASON: CORRECT Found amide group with an '
               'acyl chain of 21 contiguous aliphatic carbons.\n'
               ' * SMILES: '
               'O=C(N[C@@H]([C@](O)(C(=O)C)C)CO)/C=C/C=C/C(=C/C(CC)C)/C NAME: '
               'Bipolamide A REASON: CORRECT Found amide group with an acyl '
               'chain of 9 contiguous aliphatic carbons.\n'
               ' * SMILES: O=C(N)CCCCCCCCCCC/C=C\\CCCCCCCC NAME: erucamide '
               'REASON: CORRECT Found amide group with an acyl chain of 21 '
               'contiguous aliphatic carbons.\n'
               'False positives: SMILES: '
               'C1=CC(=CC=C1C(=O)NC(CCC(=O)NC(CCC(=O)NC(CCC(=O)O)C(=O)O)C(=O)O)C(=O)O)NCC2=CN=C3C(=N2)C(=O)NC(=N3)N '
               'NAME: Pteropterin REASON: WRONGLY CLASSIFIED Found amide group '
               'with an acyl chain of 4 contiguous aliphatic carbons.\n'
               ' * SMILES: '
               'O=C(NCC[NH3+])C[C@](CC(=O)NC[C@@H](C([O-])=O)[NH3+])(C([O-])=O)O '
               'NAME: '
               '2-[(L-alanin-3-ylcarbamoyl)methyl]-3-(2-aminoethylcarbamoyl)-2-hydroxypropanoate '
               'REASON: WRONGLY CLASSIFIED Found amide group with an acyl '
               'chain of 4 contiguous aliphatic carbons.\n'
               ' * SMILES: '
               'O=C1N(O)CCCCC1NC(=O)C(C(OC(=O)C(NC(=O)C2N=C(C3=C(O)C=CC=C3)OC2C)CCCCN(O)C(=O)/C=C\\CCCCCCCCCC(=O)O)CC)C '
               'NAME: Carboxymycobactin-7 REASON: WRONGLY CLASSIFIED Found '
               'amide group with an acyl chain of 4 contiguous aliphatic '
               'carbons.\n'
               ' * SMILES: '
               'O=C(NC(C(=O)O)CC(=O)N)/C(=C/C=C/C=C/C=C/C=C/C=C/C=C/C=C/[C@H]1N=C(/C=C/C=2NC=CC2)O[C@@H]1C)/C '
               'NAME: DKxanthene 556 REASON: WRONGLY CLASSIFIED Found amide '
               'group with an acyl chain of 16 contiguous aliphatic carbons.\n'
               ' * SMILES: '
               'O=C(N[C@H](C(=O)N[C@@H](CC(O)=O)C(O)=O)CO)[C@@H](N)[C@H](CC)C '
               'NAME: Ile-Ser-Asp REASON: WRONGLY CLASSIFIED Found amide group '
               'with an acyl chain of 4 contiguous aliphatic carbons.\n'
               ' * SMILES: '
               'O=C(N[C@H](C(=O)N[C@@H](C(C)C)C(O)=O)CO)[C@@H](N)CCCCN NAME: '
               'Lys-Ser-Val REASON: WRONGLY CLASSIFIED Found amide group with '
               'an acyl chain of 5 contiguous aliphatic carbons.\n'
               ' * SMILES: '
               'O[C@@H]([C@H](NC(=O)[C@@H](NC(=O)[C@@H](N)[C@H](O)C)CCC(O)=O)C(O)=O)C '
               'NAME: Thr-Glu-Thr REASON: WRONGLY CLASSIFIED Found amide group '
               'with an acyl chain of 4 contiguous aliphatic carbons.\n'
               ' * SMILES: '
               'O=C(NC(C(=O)O)CCC(=O)N)/C=C/C=C/C1=CC=C([N+]([O-])=NC2=CC=C(/C=C/C=C/C(=O)NC(C(=O)O)CCC(=O)N)C=C2)C=C1 '
               'NAME: Azoxymycin A REASON: WRONGLY CLASSIFIED Found amide '
               'group with an acyl chain of 4 contiguous aliphatic carbons.\n'
               ' * SMILES: '
               'C[C@H](CCC(=O)NCCCC(O)=O)[C@H]1CC[C@H]2[C@H]3[C@H](CC[C@]12C)[C@@]4(C)CC[C@@H](O)C[C@H]4CC3=O '
               'NAME: 7-oxo-gamma-aminoisobutyrolithocholic acid REASON: '
               'WRONGLY CLASSIFIED Found amide group with an acyl chain of 4 '
               'contiguous aliphatic carbons.\n'
               ' * SMILES: '
               'O=C(N[C@@H](CC(C)C)C(O)=O)[C@@H](NC(=O)[C@@H](N)CCC(=O)N)CC=1C=2C(NC1)=CC=CC2 '
               'NAME: Gln-Trp-Leu REASON: WRONGLY CLASSIFIED Found amide group '
               'with an acyl chain of 4 contiguous aliphatic carbons.\n'
               ' * SMILES: '
               'O=C(N[C@@H](CC(C)C)C(O)=O)[C@@H](NC(=O)[C@@H](N)C(C)C)CCCN=C(N)N '
               'NAME: Val-Arg-Leu REASON: WRONGLY CLASSIFIED Found amide group '
               'with an acyl chain of 4 contiguous aliphatic carbons.\n'
               ' * SMILES: '
               'O=C(NC(CCCN=C(N)N)C(O)=O)C(NC(=O)C(NC(=O)C1=CC=CC=C1)CC2=CC=CC=C2)CC(C)C '
               'NAME: Phe(benzoyl)-leu-arg REASON: WRONGLY CLASSIFIED Found '
               'amide group with an acyl chain of 4 contiguous aliphatic '
               'carbons.\n'
               ' * SMILES: '
               'O=C(N[C@H](C(=O)N[C@@H](CCC(=O)N)C(O)=O)CO)[C@H]1NCCC1 NAME: '
               'Pro-Ser-Gln REASON: WRONGLY CLASSIFIED Found amide group with '
               'an acyl chain of 4 contiguous aliphatic carbons.\n'
               ' * SMILES: '
               'SC[C@H](NC(=O)[C@@H](N)CCCN=C(N)N)C(=O)N[C@@H](CC(O)=O)C(O)=O '
               'NAME: Arg-Cys-Asp REASON: WRONGLY CLASSIFIED Found amide group '
               'with an acyl chain of 4 contiguous aliphatic carbons.\n'
               ' * SMILES: SC[C@H](N)C(=O)N[C@@H](CC(C)C)C(=O)NCC(O)=O NAME: '
               'Cys-Leu-Gly REASON: WRONGLY CLASSIFIED Found amide group with '
               'an acyl chain of 4 contiguous aliphatic carbons.\n'
               ' * SMILES: '
               'O=C(N[C@@H](CC(=O)N)C(O)=O)[C@@H](NC(=O)[C@@H](N)CO)CCC(O)=O '
               'NAME: Ser-Glu-Asn REASON: WRONGLY CLASSIFIED Found amide group '
               'with an acyl chain of 4 contiguous aliphatic carbons.\n'
               ' * SMILES: '
               'O=C(OC)[C@@H](NC(=O)C[C@@](O)(CC(=O)O[C@H]1[C@H](O)C([C@@H]2CCC3=C([C@]2(C1)C)C[C@H](O)[C@]4([C@]3(CC[C@@H]4[C@@H](CC[C@@H](O)C(O)(C)C)C)C)C)(C)C)C)[C@@H](O)C5=CC=CC=C5 '
               'NAME: Pardinol C REASON: WRONGLY CLASSIFIED Found amide group '
               'with an acyl chain of 4 contiguous aliphatic carbons.\n'
               ' * SMILES: '
               'O=C1O[C@H]([C@H](NC(=O)[C@H](NC(=O)C(O)CC2=CC=C(O)C=C2)CCC(=O)N)C(=O)N[C@H](C(=O)N[C@H]3CC[C@H](N([C@H](C(N([C@H](C(N[C@H]1[C@H](CC)C)=O)CC4=CC=CC=C4)C)=O)C(C)C)C3=O)O)CC5C=CC(O)CC5)C '
               'NAME: Micropeptin KB1046 REASON: WRONGLY CLASSIFIED Found '
               'amide group with an acyl chain of 4 contiguous aliphatic '
               'carbons.\n'
               ' * SMILES: '
               'S(CC[C@H](NC(=O)[C@@H](NC(=O)[C@@H](N)CCSC)CCCN=C(N)N)C(O)=O)C '
               'NAME: Met-Arg-Met REASON: WRONGLY CLASSIFIED Found amide group '
               'with an acyl chain of 4 contiguous aliphatic carbons.\n'
               ' * SMILES: '
               'C[C@@H](O)C(=O)SC[C@H](NC(=O)CC[C@H](N)C(O)=O)C(=O)NCC(O)=O '
               'NAME: (R)-S-lactoylglutathione REASON: WRONGLY CLASSIFIED '
               'Found amide group with an acyl chain of 4 contiguous aliphatic '
               'carbons.\n'
               ' * SMILES: '
               '[H]NCC(NCC(NCC(N[C@H]1CSSC[C@H](NC([C@@H](NC([C@@H](NC([C@@H](NC([C@@H](NC1=O)CC2=CC=C(O)C=C2)=O)CC3=CC=CC=C3)=O)CCC(N)=O)=O)CC(N)=O)=O)C(N4CCC[C@H]4C(N[C@@H](CCCCN)C(NCC(N)=O)=O)=O)=O)=O)=O)=O '
               'NAME: terlipressin REASON: WRONGLY CLASSIFIED Found amide '
               'group with an acyl chain of 5 contiguous aliphatic carbons.\n'
               ' * SMILES: '
               'O=C(N[C@H](C(=O)NC(OC)CC(C)C)CCC(=O)N)[C@@H](NC(=O)C[C@H](O)CCCCCCCCC)CC(=O)N '
               'NAME: Penicimutalide C/D REASON: WRONGLY CLASSIFIED Found '
               'amide group with an acyl chain of 4 contiguous aliphatic '
               'carbons.\n'
               ' * SMILES: CCCCCCCCCCCCCCCCCCCCCCCC(=O)NC(CO)CCCCCCCCCC NAME: '
               'N-(1-hydroxydodecan-2-yl)tetracosanamide REASON: WRONGLY '
               'CLASSIFIED Found amide group with an acyl chain of 23 '
               'contiguous aliphatic carbons.\n'
               ' * SMILES: '
               'O=NN(O)CCC[C@@H](NC(=O)[C@@H](NC(=O)[C@H](NC(=O)[C@H](NC(=O)[C@@H](NC(=O)[C@H](NC(=O)CNC(=O)C[C@H](O)CCCCCCCCCCC)[C@@H](O)C(=O)O)CO)[C@H](O)C)CCCN(O)N=O)CO)C(=O)O '
               'NAME: Megapolibactin F REASON: WRONGLY CLASSIFIED Found amide '
               'group with an acyl chain of 4 contiguous aliphatic carbons.\n'
               ' * SMILES: O=C(NC(CCC(=O)N)C(O)=O)CCCCCCC/C=C/C\\C=C\\CCCCC '
               'NAME: N-Linoleoyl Glutamine REASON: WRONGLY CLASSIFIED Found '
               'amide group with an acyl chain of 17 contiguous aliphatic '
               'carbons.\n'
               'False negatives: SMILES: '
               'CCCC(=O)Nc1ncnc2n(cnc12)[C@@H]1O[C@@H]2COP(O)(=O)O[C@H]2[C@H]1O '
               'NAME: N(6)-butyryl-cAMP REASON: MISSED Found amide group but '
               'acyl chain only has 3 contiguous aliphatic carbons (need at '
               'least 4).\n'
               ' * SMILES: N1C=C(CCNC(CCCCCCC/C=C\\CCCCCCCC)=O)C2=C1C=CC(O)=C2 '
               'NAME: N-oleoylserotonin REASON: MISSED Acyl chain qualifies, '
               'but the amine fragment (36 heavy atoms) is too large '
               '(threshold 20).\n'
               ' * SMILES: '
               'S1C(=N[C@@H](C1)C=C)C[C@H]([C@H](C[C@@H](CCN(C(=O)[C@@H](CC)C)C)C)C)C '
               'NAME: Kalkitoxin REASON: MISSED Found amide group but acyl '
               'chain only has 3 contiguous aliphatic carbons (need at least '
               '4).\n'
               ' * SMILES: O=C1C(NC(=O)/C=C/C=C/CC(C)C)=C[C@](O)(CCC(=O)N)C=C1 '
               'NAME: Daryamide B REASON: MISSED Acyl chain qualifies, but the '
               'amine fragment (26 heavy atoms) is too large (threshold 20).\n'
               ' * SMILES: O=C(N(CCCCN(C)C)CCCCN(C)C)CCCCCC NAME: '
               'N,N-Bis[4-(dimethylamino)butyl]heptanamide REASON: MISSED Acyl '
               'chain qualifies, but the amine fragment (30 heavy atoms) is '
               'too large (threshold 20).\n'
               ' * SMILES: '
               'N1C(C(CCNC(CCC/C=C\\C/C=C\\C/C=C\\C/C=C\\CCCCC)=O)C2=C1C=CC(O)=C2)=O '
               'NAME: N-arachidonoyl-2-oxoserotonin REASON: MISSED \n'
               ' * SMILES: '
               'O=C1N(C(=O)/C=C/CCCCCCCCC)[C@H](CC(C)C)C(=C1C(=O)C)O NAME: '
               'Reutericyclin C REASON: MISSED \n'
               ' * SMILES: '
               'Cl/C=C(\\CN(C(=O)CC/C=C/C[C@@H](OC)CCCCCCC)C)/C/C(/OC)=C\\C(=O)N1C(=O)C=C([C@H]1CO)OC '
               'NAME: Malyngamide R REASON: MISSED Acyl chain qualifies, but '
               'the amine fragment (64 heavy atoms) is too large (threshold '
               '20).\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCCCCCCCCCC(=O)N[C@@H](CO[C@H]1O[C@H](CO)[C@H](O)[C@H](O)[C@H]1O)[C@H](O)[C@H](O)CCCCC '
               'NAME: '
               'N-[(2S,3S,4R)-1-(alpha-D-galactopyranosyloxy)-3,4-dihydroxynonan-2-yl]hexacosanamide '
               'REASON: MISSED Acyl chain qualifies, but the amine fragment '
               '(34 heavy atoms) is too large (threshold 20).\n'
               ' * SMILES: CCN(CC)C(=O)CC(C)C NAME: isovaleryl diethylamide '
               'REASON: MISSED Found amide group but acyl chain only has 3 '
               'contiguous aliphatic carbons (need at least 4).\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'O=C(N[C@@H](C(O)(C)C)C)[C@H]([C@@]1([C@@]2([C@@](CC1)(/C(/CCC2)=C/C=C\\3/C[C@@H](O)C[C@H](O)C3=C)[H])C)[H])C',
                                     'name': '1alpha,25-dihydroxy-24-oxo-23-azavitamin '
                                             'D2 / '
                                             '1alpha,25-dihydroxy-24-oxo-23-azaergocalciferol',
                                     'reason': 'Found amide group but acyl '
                                               'chain only has 2 contiguous '
                                               'aliphatic carbons (need at '
                                               'least 4).'},
                                 {   'smiles': 'CCCCCCCCCCCCCCCCCCC(O)C([O-])=O',
                                     'name': '2-hydroxyarachidate',
                                     'reason': 'No amide (C(=O)N) functional '
                                               'group found'},
                                 {   'smiles': 'C[C@@H](CN([C@@H](C)CO)C(=O)NC1=CC=C(C=C1)C(F)(F)F)[C@@H](CN(C)C(=O)C2CCOCC2)OC',
                                     'name': 'N-[(2S,3S)-4-[[(2S)-1-hydroxypropan-2-yl]-[[4-(trifluoromethyl)phenyl]carbamoyl]amino]-2-methoxy-3-methylbutyl]-N-methyloxane-4-carboxamide',
                                     'reason': ''},
                                 {   'smiles': 'CC(=O)CC\\C=C(/C)CCC=C(C)C',
                                     'name': 'geranyl acetone',
                                     'reason': 'No amide (C(=O)N) functional '
                                               'group found'},
                                 {   'smiles': 'O([C@H]1[C@H](O)[C@H](O[C@H](O)[C@H]1O)CO[C@H]2O[C@@H]([C@@H](O)[C@H](O)[C@@H]2O)CO)[C@H]3O[C@@H]([C@@H](O)[C@H](O)[C@@H]3O[C@H]4O[C@@H]([C@@H](O)[C@H](O)[C@@H]4O)CO)CO',
                                     'name': '(2S,3S,4S,5S,6R)-2-[[(2R,3R,4S,5S,6S)-4-[(2R,3S,4S,5S,6R)-4,5-Dihydroxy-6-(hydroxymethyl)-3-[(2R,3S,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-3,5,6-trihydroxyoxan-2-yl]methoxy]-6-(hydroxymethyl)oxane-3,4,5-triol',
                                     'reason': 'No amide (C(=O)N) functional '
                                               'group found'},
                                 {   'smiles': 'O=C(OC1=C(C(O)=C(C(=O)O)C(=C1C)C)C)C2=C(OC)C(=C(OC(=O)C3=C(O)C=C(O)C=C3C)C=C2C)C',
                                     'name': 'Thielavin Z5',
                                     'reason': 'No amide (C(=O)N) functional '
                                               'group found'},
                                 {   'smiles': '[C@@H]1([C@@H]([C@H]([C@@H]([C@H](O1)CO)O)O)NC(C)=O)O[C@@H]2[C@@H]([C@H](C(O[C@@H]2CO)O)O)O',
                                     'name': 'beta-D-GlcpNAc-(1->4)-D-Galp',
                                     'reason': 'Found amide group but acyl '
                                               'chain only has 1 contiguous '
                                               'aliphatic carbons (need at '
                                               'least 4).'},
                                 {   'smiles': 'CN(C)C(=O)C1=CC=C(C=C1)C2=CC=C(C=C2)[C@@H]3[C@H]4CN(CC(=O)N4[C@H]3CO)C(=O)CC5CC5',
                                     'name': '4-[4-[(6S,7R,8R)-4-(2-cyclopropyl-1-oxoethyl)-8-(hydroxymethyl)-2-oxo-1,4-diazabicyclo[4.2.0]octan-7-yl]phenyl]-N,N-dimethylbenzamide',
                                     'reason': ''},
                                 {   'smiles': 'CCCCCCCCCCCCCCCCCCCCC=C',
                                     'name': '1-docosene',
                                     'reason': 'No amide (C(=O)N) functional '
                                               'group found'},
                                 {   'smiles': 'C([C@@](OC(=O)CCC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)([H])COC(=O)CC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)OC(=O)CCCCC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC',
                                     'name': 'TG(22:5(7Z,10Z,13Z,16Z,19Z)/20:5(5Z,8Z,11Z,14Z,17Z)/22:6(4Z,7Z,10Z,13Z,16Z,19Z))[iso6]',
                                     'reason': 'No amide (C(=O)N) functional '
                                               'group found'}],
    'sample_false_negatives': [   {   'smiles': 'CCCC(=O)Nc1ncnc2n(cnc12)[C@@H]1O[C@@H]2COP(O)(=O)O[C@H]2[C@H]1O',
                                      'name': 'N(6)-butyryl-cAMP',
                                      'reason': 'Found amide group but acyl '
                                                'chain only has 3 contiguous '
                                                'aliphatic carbons (need at '
                                                'least 4).'},
                                  {   'smiles': 'N1C=C(CCNC(CCCCCCC/C=C\\CCCCCCCC)=O)C2=C1C=CC(O)=C2',
                                      'name': 'N-oleoylserotonin',
                                      'reason': 'Acyl chain qualifies, but the '
                                                'amine fragment attached to '
                                                'the amide nitrogen is too '
                                                'large (36 heavy atoms; '
                                                'threshold 20).'},
                                  {   'smiles': 'S1C(=N[C@@H](C1)C=C)C[C@H]([C@H](C[C@@H](CCN(C(=O)[C@@H](CC)C)C)C)C)C',
                                      'name': 'Kalkitoxin',
                                      'reason': 'Found amide group but acyl '
                                                'chain only has 1 contiguous '
                                                'aliphatic carbons (need at '
                                                'least 4).'},
                                  {   'smiles': 'O=C1C(NC(=O)/C=C/C=C/CC(C)C)=C[C@](O)(CCC(=O)N)C=C1',
                                      'name': 'Daryamide B',
                                      'reason': 'Acyl chain qualifies, but the '
                                                'amine fragment attached to '
                                                'the amide nitrogen is too '
                                                'large (26 heavy atoms; '
                                                'threshold 20).'},
                                  {   'smiles': 'O=C(N(CCCCN(C)C)CCCCN(C)C)CCCCCC',
                                      'name': 'N,N-Bis[4-(dimethylamino)butyl]heptanamide',
                                      'reason': 'Acyl chain qualifies, but the '
                                                'amine fragment attached to '
                                                'the amide nitrogen is too '
                                                'large (30 heavy atoms; '
                                                'threshold 20).'},
                                  {   'smiles': 'N1C(C(CCNC(CCC/C=C\\C/C=C\\C/C=C\\C/C=C\\CCCCC)=O)C2=C1C=CC(O)=C2)=O',
                                      'name': 'N-arachidonoyl-2-oxoserotonin',
                                      'reason': ''},
                                  {   'smiles': 'O=C1N(C(=O)/C=C/CCCCCCCCC)[C@H](CC(C)C)C(=C1C(=O)C)O',
                                      'name': 'Reutericyclin C',
                                      'reason': ''},
                                  {   'smiles': 'CCC(C)\\C=C(/C)[C@H](O)[C@H](C)\\C=C(C)\\C=C\\C=C/C=C/C=C(\\C)C(=O)N[C@@H](C)CO',
                                      'name': 'Myxalamid A',
                                      'reason': 'Found amide group but acyl '
                                                'chain only has 1 contiguous '
                                                'aliphatic carbons (need at '
                                                'least 4).'},
                                  {   'smiles': 'Cl/C=C(\\CN(C(=O)CC/C=C/C[C@@H](OC)CCCCCCC)C)/C/C(/OC)=C\\C(=O)N1C(=O)C=C([C@H]1CO)OC',
                                      'name': 'Malyngamide R',
                                      'reason': 'Acyl chain qualifies, but the '
                                                'amine fragment attached to '
                                                'the amide nitrogen is too '
                                                'large (64 heavy atoms; '
                                                'threshold 20).'},
                                  {   'smiles': 'O=C(N[C@H](CO)CC(C)C)\\C(=C/C=C/C)\\C',
                                      'name': 'Dichotomocej A',
                                      'reason': 'Found amide group but acyl '
                                                'chain only has 1 contiguous '
                                                'aliphatic carbons (need at '
                                                'least 4).'}],
    'attempt': 2,
    'reasoning': 'Below is our revised Python program. In our reasoning we '
                 'looked back at the previous approach and noted that although '
                 'it found an amide group and even computed a “longest‐linear '
                 'path” from the carbonyl the following problems remained:\n'
                 '  \n'
                 '• Some amino‐substituents (the N–side group) were “too '
                 'small” to be fatty–acid derivatives. In fatty amides the '
                 'acyl (fatty acid–derived) part is usually a major fraction '
                 'of the molecule. In many false–positive cases the linear '
                 'chain found was only a minor “tail” on a large peptide–like '
                 'fragment. So, in addition to requiring a minimum chainlength '
                 '(at least 4 contiguous, non–branched aliphatic carbons), we '
                 'now also require that the chain accounts for at least a '
                 'modest fraction of the heavy atoms in the molecule.\n'
                 '  \n'
                 '• In the earlier DFS we sometimes “allowed” branching (by '
                 'taking a maximal path) when in fact the fatty acid chain '
                 'should remain linear. Hence, we now use an iterative “walk” '
                 'that stops as soon as more than one eligible neighbor is '
                 'encountered.\n'
                 '  \n'
                 '• We keep the check that the amine substituent (the nitrogen '
                 'side of the amide) should not be too large (here fewer than '
                 '20 heavy atoms). That helps to rule out cases where the '
                 'molecule is actually a peptide or macrocycle with a short '
                 '“acyl” part.\n'
                 '  \n'
                 'The code that follows enacts these improvements. (If no '
                 'amide group matching all our criteria is found the program '
                 'returns (False, <reason>).)\n'
                 '\n'
                 'Below is the complete program in a single Python code block:',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 171,
    'num_false_positives': 1155,
    'num_true_negatives': 140841,
    'num_false_negatives': 133,
    'num_negatives': None,
    'precision': 0.12895927601809956,
    'recall': 0.5625,
    'f1': 0.2098159509202454,
    'accuracy': 0.9909486999297259,
    'negative_predictive_value': 0.9990565636216607}