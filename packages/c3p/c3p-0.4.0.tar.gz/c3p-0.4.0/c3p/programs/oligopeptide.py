"""
Classifies: CHEBI:25676 oligopeptide
"""
"""
Classifies: Oligopeptide – a peptide containing a relatively small number of amino acids.

This version uses modified heuristics:
  1. It searches for amide (peptide) bonds using the SMARTS "C(=O)N" and then filters out those
     that are in rings (often seen in unrelated chemistry).
  2. It estimates the residue count as (# peptide bonds + 1) and accepts between 2 and 10 residues.
  3. It counts chiral alpha–carbon units using the SMARTS "[C@H](N)" and "[C@@H](N)".
  4. It checks that all peptide-bond atoms (carbonyl carbon and the adjacent amide nitrogen)
     lie in a single fragment.
  5. For 3 or more residues it requires that a contiguous backbone appears
     (via substructure searches for "N[C@H](*)C(=O)N" or its mirror).
  6. It enforces a molecular weight range roughly estimated as (n_residues * 60) < MW < (n_residues * 200)
     (this may help rule out compounds with peptide‐like bonds that are too heavy).
     
Note: This is a heuristic; many molecules are borderline and some failures (false positives/negatives)
may still occur.
"""
from rdkit import Chem
from rdkit.Chem import rdMolDescriptors

def is_oligopeptide(smiles: str):
    """
    Determines whether the given molecule (via its SMILES) is a small peptide (oligopeptide).

    Heuristics used:
      - Search for amide (peptide) bonds (SMARTS "C(=O)N"), but ignore those that are in rings.
      - Estimate residue count as (number of peptide bonds + 1); allow between 2 and 10 residues.
      - Count alpha–carbon centers (matches to "[C@H](N)" and "[C@@H](N)").
         For dipeptides, require exactly 2; for larger chains, require at least 2.
      - Ensure all peptide bond atoms (carbonyl C and amide N) lie in a single fragment.
      - For peptides with ≥3 residues, require that a backbone motif is found, for example
            "N[C@H](*)C(=O)N" or "N[C@@H](*)C(=O)N".
      - Check that the molecular weight roughly falls in the expected range:
            lower bound = n_residues * 60 Da, upper bound = n_residues * 200 Da.
      
    Args:
        smiles (str): SMILES string of the molecule.
      
    Returns:
        bool: True if the molecule is classified as an oligopeptide, False otherwise.
        str: Explanation of the decision.
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
    
    # Step 1. Find "peptide" (amide) bonds via SMARTS "C(=O)N"
    pb_smarts = Chem.MolFromSmarts("C(=O)N")
    all_pb_matches = mol.GetSubstructMatches(pb_smarts)
    
    # Only consider peptide bonds whose carbonyl C and the adjacent N are not in a ring.
    pb_matches = []
    for match in all_pb_matches:
        # In our SMARTS, match[0] is the carbonyl carbon; match[2] is the attached N.
        # (match[1] corresponds to the oxygen, but we ignore it here)
        c_atom = mol.GetAtomWithIdx(match[0])
        n_atom = mol.GetAtomWithIdx(match[2])
        if c_atom.IsInRing() or n_atom.IsInRing():
            continue
        pb_matches.append(match)
    
    n_pbonds = len(pb_matches)
    if n_pbonds == 0:
        return False, "No peptide (amide) bonds found (or none outside ring systems)"
    
    n_residues = n_pbonds + 1
    if n_residues < 2:
        return False, "Too few peptide bonds to form a peptide (need at least 2 residues)"
    if n_residues > 10:
        return False, f"Found {n_residues} amino acid residues which is too many for an oligopeptide"

    # Step 2. Count alpha–carbon centers (with declared chirality) using SMARTS.
    alpha1 = Chem.MolFromSmarts("[C@H](N)")
    alpha2 = Chem.MolFromSmarts("[C@@H](N)")
    alpha_set = set()
    for m in mol.GetSubstructMatches(alpha1):
        # m[0] is the chiral carbon.
        alpha_set.add(m[0])
    for m in mol.GetSubstructMatches(alpha2):
        alpha_set.add(m[0])
    n_alpha = len(alpha_set)
    if n_residues == 2 and n_alpha != 2:
        return False, f"For a dipeptide, exactly 2 alpha–carbon centers are expected; found {n_alpha}"
    if n_residues >= 3 and n_alpha < 2:
        return False, f"Expected at least 2 alpha–carbon centers; found {n_alpha}"
    
    # Step 3. Check that all atoms involved in peptide bonds are in one contiguous fragment.
    pb_atom_idxs = set()
    for m in pb_matches:
        pb_atom_idxs.add(m[0])  # carbonyl carbon
        pb_atom_idxs.add(m[2])  # amide nitrogen
    frags = Chem.GetMolFrags(mol, asMols=False)
    count_frag_with_pb = sum(1 for frag in frags if any(a in frag for a in pb_atom_idxs))
    if count_frag_with_pb > 1:
        return False, "Peptide-bond atoms are not contained in a single contiguous fragment"
    
    # Step 4. For peptides with ≥3 residues, look for a contiguous backbone motif.
    if n_residues >= 3:
        bb_smarts1 = Chem.MolFromSmarts("N[C@H](*)C(=O)N")
        bb_smarts2 = Chem.MolFromSmarts("N[C@@H](*)C(=O)N")
        if not (mol.HasSubstructMatch(bb_smarts1) or mol.HasSubstructMatch(bb_smarts2)):
            return False, "Peptide-bond connectivity does not appear contiguous (backbone motif missing)"
    
    # Step 5. Check molecular weight.
    mol_wt = rdMolDescriptors.CalcExactMolWt(mol)
    min_expected = n_residues * 60
    max_expected = n_residues * 200  # a bit looser than before to allow variability
    if mol_wt < min_expected:
        return False, (f"Molecular weight ({mol_wt:.1f} Da) is too low for a {n_residues}-residue peptide "
                       f"(expected at least {min_expected} Da)")
    if mol_wt > max_expected:
        return False, (f"Molecular weight ({mol_wt:.1f} Da) is too high for a {n_residues}-residue peptide "
                       f"(expected at most {max_expected} Da)")
    
    # Additional property: count rotatable bonds.
    n_rotatable = rdMolDescriptors.CalcNumRotatableBonds(mol)
    
    reason = (f"Detected {n_pbonds} peptide bond(s) (≈{n_residues} residue(s)), {n_rotatable} rotatable bond(s), "
              f"{n_alpha} alpha–carbon center(s), and MW of {mol_wt:.1f} Da. "
              "Peptide bond atoms are in a single fragment and a contiguous backbone motif is detected. "
              "This is consistent with an oligopeptide.")
    
    return True, reason

# For local testing one might do:
if __name__ == "__main__":
    # Example: Leu-Trp dipeptide
    test_smiles = "CC(C)C[C@H](N)C(=O)N[C@@H](Cc1c[nH]c2ccccc12)C(O)=O"
    result, explanation = is_oligopeptide(test_smiles)
    print(result, explanation)


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:25676',
                          'name': 'oligopeptide',
                          'definition': 'A peptide containing a relatively '
                                        'small number of amino acids.',
                          'parents': ['CHEBI:16670'],
                          'xrefs': ['Wikipedia:Oligopeptide'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 92,
                           'log_lines_of_code': 4.5217885770490405,
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
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 1,
                                                 1,
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
                                                 2,
                                                 2,
                                                 1,
                                                 2,
                                                 1,
                                                 1,
                                                 2,
                                                 1,
                                                 2,
                                                 1,
                                                 1,
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
                                                 2,
                                                 2,
                                                 2,
                                                 3,
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
                                                 1],
                           'max_indent': 3,
                           'imports': [   'from rdkit import Chem',
                                          'from rdkit.Chem import '
                                          'rdMolDescriptors'],
                           'imports_count': 2,
                           'methods_called': [   'CalcNumRotatableBonds',
                                                 'GetMolFrags',
                                                 'CalcExactMolWt',
                                                 'MolFromSmiles',
                                                 'GetAtomWithIdx',
                                                 'HasSubstructMatch',
                                                 'MolFromSmarts',
                                                 'append',
                                                 'IsInRing',
                                                 'GetSubstructMatches',
                                                 'add'],
                           'methods_called_count': 11,
                           'smarts_strings': [   'N[C@H](*)C(=O)N',
                                                 'N[C@@H](*)C(=O)N',
                                                 'C(=O)N',
                                                 '[C@H](N)',
                                                 '[C@@H](N)'],
                           'smarts_strings_count': 5,
                           'defs': ['is_oligopeptide(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "No peptide (amide) bonds '
                                          'found (or none outside ring '
                                          'systems)"',
                                          'False, "Too few peptide bonds to '
                                          'form a peptide (need at least 2 '
                                          'residues)"',
                                          'False, f"Found {n_residues} amino '
                                          'acid residues which is too many for '
                                          'an oligopeptide"',
                                          'False, f"For a dipeptide, exactly 2 '
                                          'alpha–carbon centers are expected; '
                                          'found {n_alpha}"',
                                          'False, f"Expected at least 2 '
                                          'alpha–carbon centers; found '
                                          '{n_alpha}"',
                                          'False, "Peptide-bond atoms are not '
                                          'contained in a single contiguous '
                                          'fragment"',
                                          'False, "Peptide-bond connectivity '
                                          'does not appear contiguous '
                                          '(backbone motif missing)"',
                                          'False, (f"Molecular weight '
                                          '({mol_wt:.1f} Da) is too low for a '
                                          '{n_residues}-residue peptide "',
                                          'False, (f"Molecular weight '
                                          '({mol_wt:.1f} Da) is too high for a '
                                          '{n_residues}-residue peptide "',
                                          'True, reason'],
                           'returns_count': 11,
                           'complexity': 6.104357715409808},
    'message': '\n'
               'Attempt failed: F1 score of 0.16444629475437136 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: '
               'O=C(NC(CC=1NC=NC1)C(O)=O)C(N)CCCN=C(N)N NAME: '
               'Arginyl-Histidine REASON: CORRECT Detected 1 peptide bond(s) '
               '(≈2 residue(s)), 9 rotatable bond(s), 2 alpha–carbon '
               'center(s), and MW of 311.2 Da. The peptide-bond atoms form a '
               'single contiguous linear chain. This is consistent with an '
               'oligopeptide.\n'
               ' * SMILES: CC(C)C[C@H](N)C(=O)N[C@@H](Cc1c[nH]c2ccccc12)C(O)=O '
               'NAME: Leu-Trp REASON: CORRECT Detected 1 peptide bond(s) (≈2 '
               'residue(s)), 7 rotatable bond(s), 2 alpha–carbon center(s), '
               'and MW of 317.2 Da. The peptide-bond atoms form a single '
               'contiguous linear chain. This is consistent with an '
               'oligopeptide.\n'
               ' * SMILES: OC1CC(N(C1)C(=O)C(N)C(C)C)C(O)=O NAME: '
               'Valyl-Hydroxyproline REASON: CORRECT Detected 1 peptide '
               'bond(s) (≈2 residue(s)), 3 rotatable bond(s), 2 alpha–carbon '
               'center(s), and MW of 230.1 Da. The peptide-bond atoms form a '
               'single contiguous linear chain. This is consistent with an '
               'oligopeptide.\n'
               ' * SMILES: CSCC[C@H](N)C(=O)N[C@@H](CCC(O)=O)C(O)=O NAME: '
               'Met-Glu REASON: CORRECT Detected 1 peptide bond(s) (≈2 '
               'residue(s)), 9 rotatable bond(s), 2 alpha–carbon center(s), '
               'and MW of 278.1 Da. The peptide-bond atoms form a single '
               'contiguous linear chain. This is consistent with an '
               'oligopeptide.\n'
               ' * SMILES: N[C@@H](Cc1c[nH]cn1)C(=O)N[C@@H](CO)C(O)=O NAME: '
               'His-Ser REASON: CORRECT Detected 1 peptide bond(s) (≈2 '
               'residue(s)), 6 rotatable bond(s), 2 alpha–carbon center(s), '
               'and MW of 242.1 Da. The peptide-bond atoms form a single '
               'contiguous linear chain. This is consistent with an '
               'oligopeptide.\n'
               ' * SMILES: NC(=N)NCCC[C@H](NC(=O)[C@@H]1CCCN1)C(O)=O NAME: '
               'Pro-Arg REASON: CORRECT Detected 1 peptide bond(s) (≈2 '
               'residue(s)), 7 rotatable bond(s), 2 alpha–carbon center(s), '
               'and MW of 271.2 Da. The peptide-bond atoms form a single '
               'contiguous linear chain. This is consistent with an '
               'oligopeptide.\n'
               ' * SMILES: C(=O)([C@@H](NC(=O)CC[C@@H](C(=O)O)N)[C@H](O)C)O '
               'NAME: L-gamma-Glu-L-Thr REASON: CORRECT Detected 1 peptide '
               'bond(s) (≈2 residue(s)), 7 rotatable bond(s), 2 alpha–carbon '
               'center(s), and MW of 248.1 Da. The peptide-bond atoms form a '
               'single contiguous linear chain. This is consistent with an '
               'oligopeptide.\n'
               ' * SMILES: CSCC[C@H](NC(=O)[C@@H](N)C(C)C)C(O)=O NAME: Val-Met '
               'REASON: CORRECT Detected 1 peptide bond(s) (≈2 residue(s)), 7 '
               'rotatable bond(s), 2 alpha–carbon center(s), and MW of 248.1 '
               'Da. The peptide-bond atoms form a single contiguous linear '
               'chain. This is consistent with an oligopeptide.\n'
               ' * SMILES: CC(C)C[C@H](N)C(=O)N[C@@H](CS)C(O)=O NAME: Leu-Cys '
               'REASON: CORRECT Detected 1 peptide bond(s) (≈2 residue(s)), 6 '
               'rotatable bond(s), 2 alpha–carbon center(s), and MW of 234.1 '
               'Da. The peptide-bond atoms form a single contiguous linear '
               'chain. This is consistent with an oligopeptide.\n'
               ' * SMILES: N[C@@H](Cc1ccc(O)cc1)C(=O)N[C@@H](CCC(O)=O)C(O)=O '
               'NAME: Tyr-Glu REASON: CORRECT Detected 1 peptide bond(s) (≈2 '
               'residue(s)), 8 rotatable bond(s), 2 alpha–carbon center(s), '
               'and MW of 310.1 Da. The peptide-bond atoms form a single '
               'contiguous linear chain. This is consistent with an '
               'oligopeptide.\n'
               ' * SMILES: C(=O)([C@@H](N)CC1=CC=CC=C1)N[C@H](C(=O)O)CC(C)C '
               'NAME: Phe-Leu REASON: CORRECT Detected 1 peptide bond(s) (≈2 '
               'residue(s)), 7 rotatable bond(s), 2 alpha–carbon center(s), '
               'and MW of 278.2 Da. The peptide-bond atoms form a single '
               'contiguous linear chain. This is consistent with an '
               'oligopeptide.\n'
               ' * SMILES: N[C@H](C(=O)N[C@H](C(=O)O)CCCCN)[C@@H](C)CC NAME: '
               'Ile-Lys REASON: CORRECT Detected 1 peptide bond(s) (≈2 '
               'residue(s)), 9 rotatable bond(s), 2 alpha–carbon center(s), '
               'and MW of 259.2 Da. The peptide-bond atoms form a single '
               'contiguous linear chain. This is consistent with an '
               'oligopeptide.\n'
               ' * SMILES: OC(=O)C(NC(=O)C(N)CO)CCCCN NAME: Seryllysine '
               'REASON: CORRECT Detected 1 peptide bond(s) (≈2 residue(s)), 8 '
               'rotatable bond(s), 2 alpha–carbon center(s), and MW of 233.1 '
               'Da. The peptide-bond atoms form a single contiguous linear '
               'chain. This is consistent with an oligopeptide.\n'
               ' * SMILES: O=C(NC(CC(O)=O)C(O)=O)C(N)CC(O)=O NAME: '
               'Aspartyl-Aspartate REASON: CORRECT Detected 1 peptide bond(s) '
               '(≈2 residue(s)), 7 rotatable bond(s), 2 alpha–carbon '
               'center(s), and MW of 248.1 Da. The peptide-bond atoms form a '
               'single contiguous linear chain. This is consistent with an '
               'oligopeptide.\n'
               ' * SMILES: O=C(N1C(CCC1)C(O)=O)C([N+](C)(C)C)C NAME: DL-Tmap '
               'REASON: CORRECT Detected 1 peptide bond(s) (≈2 residue(s)), 3 '
               'rotatable bond(s), 2 alpha–carbon center(s), and MW of 229.2 '
               'Da. The peptide-bond atoms form a single contiguous linear '
               'chain. This is consistent with an oligopeptide.\n'
               ' * SMILES: '
               'C1=CC=CC(=C1)CC[C@H](N[C@H](C(N2C(N(C[C@H]2C(O)=O)C)=O)=O)C)C(=O)OCC '
               'NAME: imidapril REASON: CORRECT Detected 3 peptide bond(s) (≈4 '
               'residue(s)), 9 rotatable bond(s), 3 alpha–carbon center(s), '
               'and MW of 405.2 Da. The peptide-bond atoms form a single '
               'contiguous linear chain. This is consistent with an '
               'oligopeptide.\n'
               ' * SMILES: O=C(NC(C(CC)C)C([O-])=O)C([NH3+])C(C)C NAME: '
               '2-[(2-Azaniumyl-3-methylbutanoyl)amino]-3-methylpentanoate '
               'REASON: CORRECT Detected 1 peptide bond(s) (≈2 residue(s)), 6 '
               'rotatable bond(s), 2 alpha–carbon center(s), and MW of 230.2 '
               'Da. The peptide-bond atoms form a single contiguous linear '
               'chain. This is consistent with an oligopeptide.\n'
               ' * SMILES: OC1CC(N(C1)C(=O)C(N)CCCN=C(N)N)C(O)=O NAME: '
               'Arginyl-Hydroxyproline REASON: CORRECT Detected 1 peptide '
               'bond(s) (≈2 residue(s)), 6 rotatable bond(s), 2 alpha–carbon '
               'center(s), and MW of 287.2 Da. The peptide-bond atoms form a '
               'single contiguous linear chain. This is consistent with an '
               'oligopeptide.\n'
               ' * SMILES: C[C@H](NC(=O)[C@@H](N)Cc1ccccc1)C(O)=O NAME: '
               'Phe-Ala REASON: CORRECT Detected 1 peptide bond(s) (≈2 '
               'residue(s)), 5 rotatable bond(s), 2 alpha–carbon center(s), '
               'and MW of 236.1 Da. The peptide-bond atoms form a single '
               'contiguous linear chain. This is consistent with an '
               'oligopeptide.\n'
               ' * SMILES: CSCC[C@H](N)C(=O)N1CCC[C@H]1C(O)=O NAME: Met-Pro '
               'REASON: CORRECT Detected 1 peptide bond(s) (≈2 residue(s)), 5 '
               'rotatable bond(s), 2 alpha–carbon center(s), and MW of 246.1 '
               'Da. The peptide-bond atoms form a single contiguous linear '
               'chain. This is consistent with an oligopeptide.\n'
               ' * SMILES: NCCCC[C@H](NC(=O)[C@@H](N)CCC(O)=O)C(O)=O NAME: '
               'Glu-Lys REASON: CORRECT Detected 1 peptide bond(s) (≈2 '
               'residue(s)), 10 rotatable bond(s), 2 alpha–carbon center(s), '
               'and MW of 275.1 Da. The peptide-bond atoms form a single '
               'contiguous linear chain. This is consistent with an '
               'oligopeptide.\n'
               ' * SMILES: C[C@@H](O)[C@H](N)C(=O)N[C@@H](Cc1ccccc1)C(O)=O '
               'NAME: Thr-Phe REASON: CORRECT Detected 1 peptide bond(s) (≈2 '
               'residue(s)), 6 rotatable bond(s), 2 alpha–carbon center(s), '
               'and MW of 266.1 Da. The peptide-bond atoms form a single '
               'contiguous linear chain. This is consistent with an '
               'oligopeptide.\n'
               ' * SMILES: '
               'C(=O)([C@@H](N)CC=1C=CC(=CC1)O)N[C@H](C(=O)O)CC(=O)O NAME: '
               'Tyr-Asp REASON: CORRECT Detected 1 peptide bond(s) (≈2 '
               'residue(s)), 7 rotatable bond(s), 2 alpha–carbon center(s), '
               'and MW of 296.1 Da. The peptide-bond atoms form a single '
               'contiguous linear chain. This is consistent with an '
               'oligopeptide.\n'
               ' * SMILES: '
               'C(=O)([C@@H](N)CC=1C=CC(=CC1)O)N[C@H](C(=O)O)[C@H](O)C NAME: '
               'Tyr-Thr REASON: CORRECT Detected 1 peptide bond(s) (≈2 '
               'residue(s)), 6 rotatable bond(s), 2 alpha–carbon center(s), '
               'and MW of 282.1 Da. The peptide-bond atoms form a single '
               'contiguous linear chain. This is consistent with an '
               'oligopeptide.\n'
               ' * SMILES: O=C(NC(CC(C)C)C(O)=O)C(N)CC=1NC=NC1 NAME: '
               'Histidinyl-Leucine REASON: CORRECT Detected 1 peptide bond(s) '
               '(≈2 residue(s)), 7 rotatable bond(s), 2 alpha–carbon '
               'center(s), and MW of 268.2 Da. The peptide-bond atoms form a '
               'single contiguous linear chain. This is consistent with an '
               'oligopeptide.\n'
               'False positives: SMILES: '
               'CN1[C@H]([C@H]2CCN([C@H]2C3=C1C=CC(=C3)Br)C(=O)NC4=CC=C(C=C4)OC)CO '
               'NAME: '
               '(3aS,4R,9bR)-8-bromo-4-(hydroxymethyl)-N-(4-methoxyphenyl)-5-methyl-3,3a,4,9b-tetrahydro-2H-pyrrolo[3,2-c]quinoline-1-carboxamide '
               'REASON: WRONGLY CLASSIFIED Detected 2 peptide bond(s) (≈3 '
               'residue(s)), 3 rotatable bond(s), 2 alpha–carbon center(s), '
               'and MW of 445.1 Da. The peptide-bond atoms form a single '
               'contiguous linear chain. This is consistent with an '
               'oligopeptide.\n'
               ' * SMILES: '
               'C1=CC=C(C=C1)[C@@H]2[C@@H](N([C@@H]2C#N)C(=O)C3=CC=CC=C3F)CO '
               'NAME: '
               '(2S,3S,4R)-1-[(2-fluorophenyl)-oxomethyl]-4-(hydroxymethyl)-3-phenyl-2-azetidinecarbonitrile '
               'REASON: WRONGLY CLASSIFIED Detected 1 peptide bond(s) (≈2 '
               'residue(s)), 3 rotatable bond(s), 2 alpha–carbon center(s), '
               'and MW of 310.1 Da. The peptide-bond atoms form a single '
               'contiguous linear chain. This is consistent with an '
               'oligopeptide.\n'
               ' * SMILES: '
               'C[C@H]1CN(S(=O)(=O)C2=C(C=C(C=C2)C#C[C@@H](C)O)O[C@H]1CN(C)C(=O)NC(C)C)[C@@H](C)CO '
               'NAME: '
               '1-[[(4S,5R)-8-[(3R)-3-hydroxybut-1-ynyl]-2-[(2S)-1-hydroxypropan-2-yl]-4-methyl-1,1-dioxo-4,5-dihydro-3H-6,1$l^{6},2-benzoxathiazocin-5-yl]methyl]-1-methyl-3-propan-2-ylurea '
               'REASON: WRONGLY CLASSIFIED Detected 2 peptide bond(s) (≈3 '
               'residue(s)), 5 rotatable bond(s), 2 alpha–carbon center(s), '
               'and MW of 481.2 Da. The peptide-bond atoms form a single '
               'contiguous linear chain. This is consistent with an '
               'oligopeptide.\n'
               ' * SMILES: '
               'O=C1C2=C(NC=O)C=CC=C2C(C)(C)[C@H]3[C@H]1[C@@H]([N+]#[C-])[C@@](C=C)(CC3)C '
               'NAME: Hapalonamide H REASON: WRONGLY CLASSIFIED Detected 1 '
               'peptide bond(s) (≈2 residue(s)), 3 rotatable bond(s), 2 '
               'alpha–carbon center(s), and MW of 336.2 Da. The peptide-bond '
               'atoms form a single contiguous linear chain. This is '
               'consistent with an oligopeptide.\n'
               ' * SMILES: C[C@@H](CO)NC(=O)CC[C@H](N)C(O)=O NAME: '
               'N-(gamma-L-glutamyl)-L-alaninol REASON: WRONGLY CLASSIFIED '
               'Detected 1 peptide bond(s) (≈2 residue(s)), 6 rotatable '
               'bond(s), 2 alpha–carbon center(s), and MW of 204.1 Da. The '
               'peptide-bond atoms form a single contiguous linear chain. This '
               'is consistent with an oligopeptide.\n'
               ' * SMILES: '
               'C[C@H]1CN(S(=O)(=O)C2=C(C=C(C=C2)C#C[C@H](C)O)O[C@H]1CN(C)C(=O)NC(C)C)[C@H](C)CO '
               'NAME: '
               '1-[[(4S,5R)-8-[(3S)-3-hydroxybut-1-ynyl]-2-[(2R)-1-hydroxypropan-2-yl]-4-methyl-1,1-dioxo-4,5-dihydro-3H-6,1$l^{6},2-benzoxathiazocin-5-yl]methyl]-1-methyl-3-propan-2-ylurea '
               'REASON: WRONGLY CLASSIFIED Detected 2 peptide bond(s) (≈3 '
               'residue(s)), 5 rotatable bond(s), 2 alpha–carbon center(s), '
               'and MW of 481.2 Da. The peptide-bond atoms form a single '
               'contiguous linear chain. This is consistent with an '
               'oligopeptide.\n'
               ' * SMILES: '
               'COC1=CC=CC=C1NC(=O)N2[C@@H]([C@@H]([C@@H]2C#N)C3=CC=CC=C3)CO '
               'NAME: '
               '(2R,3R,4S)-2-cyano-4-(hydroxymethyl)-N-(2-methoxyphenyl)-3-phenylazetidine-1-carboxamide '
               'REASON: WRONGLY CLASSIFIED Detected 2 peptide bond(s) (≈3 '
               'residue(s)), 4 rotatable bond(s), 2 alpha–carbon center(s), '
               'and MW of 337.1 Da. The peptide-bond atoms form a single '
               'contiguous linear chain. This is consistent with an '
               'oligopeptide.\n'
               ' * SMILES: N[C@@H](CCC[C@H](NC(=O)CCC(O)=O)C(O)=O)C(O)=O NAME: '
               'N-succinyl-LL-2,6-diaminopimelic acid REASON: WRONGLY '
               'CLASSIFIED Detected 1 peptide bond(s) (≈2 residue(s)), 10 '
               'rotatable bond(s), 2 alpha–carbon center(s), and MW of 290.1 '
               'Da. The peptide-bond atoms form a single contiguous linear '
               'chain. This is consistent with an oligopeptide.\n'
               ' * SMILES: C1(=CNC2=C1C=CC=C2)CC3=CN4[C@H](C(N3)=O)CCC4 NAME: '
               '(S)-3-(indol-3-ylmethyl)-6,7,8,8a-tetrahydropyrrolo[1,2-a]pyrazin-1-one '
               'REASON: WRONGLY CLASSIFIED Detected 1 peptide bond(s) (≈2 '
               'residue(s)), 2 rotatable bond(s), 2 alpha–carbon center(s), '
               'and MW of 267.1 Da. The peptide-bond atoms form a single '
               'contiguous linear chain. This is consistent with an '
               'oligopeptide.\n'
               ' * SMILES: '
               'C1CCN2[C@H](CN(C1)C(=O)NC3=CC(=CC=C3)F)[C@@H]([C@@H]2CO)C4=CC=C(C=C4)C#CC5=CN=CC=C5 '
               'NAME: '
               '(8S,9S,10R)-N-(3-fluorophenyl)-10-(hydroxymethyl)-9-[4-[2-(3-pyridinyl)ethynyl]phenyl]-1,6-diazabicyclo[6.2.0]decane-6-carboxamide '
               'REASON: WRONGLY CLASSIFIED Detected 2 peptide bond(s) (≈3 '
               'residue(s)), 3 rotatable bond(s), 2 alpha–carbon center(s), '
               'and MW of 484.2 Da. The peptide-bond atoms form a single '
               'contiguous linear chain. This is consistent with an '
               'oligopeptide.\n'
               ' * SMILES: SC[C@H](N)C(=O)N[C@@H]([C@@H](O)C)C(O)=O NAME: '
               'Cys-Thr REASON: WRONGLY CLASSIFIED Detected 1 peptide bond(s) '
               '(≈2 residue(s)), 5 rotatable bond(s), 2 alpha–carbon '
               'center(s), and MW of 222.1 Da. The peptide-bond atoms form a '
               'single contiguous linear chain. This is consistent with an '
               'oligopeptide.\n'
               ' * SMILES: '
               'C1[C@@H]2[C@@H]([C@H](N2CC3=CC=NC=C3)CO)C4=CC=CC=C4N1C(=O)NC5=CC=CC=C5Cl '
               'NAME: '
               '(1S,2aS,8bS)-N-(2-chlorophenyl)-1-(hydroxymethyl)-2-(pyridin-4-ylmethyl)-1,2a,3,8b-tetrahydroazeto[2,3-c]quinoline-4-carboxamide '
               'REASON: WRONGLY CLASSIFIED Detected 2 peptide bond(s) (≈3 '
               'residue(s)), 4 rotatable bond(s), 2 alpha–carbon center(s), '
               'and MW of 434.2 Da. The peptide-bond atoms form a single '
               'contiguous linear chain. This is consistent with an '
               'oligopeptide.\n'
               ' * SMILES: '
               'C[C@]1(Cn2ccnn2)[C@@H](N2[C@@H](CC2=O)S1(=O)=O)C(O)=O NAME: '
               'tazobactam REASON: WRONGLY CLASSIFIED Detected 1 peptide '
               'bond(s) (≈2 residue(s)), 3 rotatable bond(s), 2 alpha–carbon '
               'center(s), and MW of 300.1 Da. The peptide-bond atoms form a '
               'single contiguous linear chain. This is consistent with an '
               'oligopeptide.\n'
               ' * SMILES: '
               'CC(C)NC(=O)N1CC[C@@H]2[C@H]1C3=C(C=CC(=C3)C#CC4=CC=CC=C4)N([C@@H]2CO)C '
               'NAME: '
               '(3aR,4S,9bS)-4-(hydroxymethyl)-5-methyl-8-(2-phenylethynyl)-N-propan-2-yl-3,3a,4,9b-tetrahydro-2H-pyrrolo[3,2-c]quinoline-1-carboxamide '
               'REASON: WRONGLY CLASSIFIED Detected 2 peptide bond(s) (≈3 '
               'residue(s)), 2 rotatable bond(s), 3 alpha–carbon center(s), '
               'and MW of 403.2 Da. The peptide-bond atoms form a single '
               'contiguous linear chain. This is consistent with an '
               'oligopeptide.\n'
               ' * SMILES: CC1NC(=O)NC1CCCCCC([O-])=O NAME: dethiobiotin(1-) '
               'REASON: WRONGLY CLASSIFIED Detected 2 peptide bond(s) (≈3 '
               'residue(s)), 6 rotatable bond(s), 2 alpha–carbon center(s), '
               'and MW of 213.1 Da. The peptide-bond atoms form a single '
               'contiguous linear chain. This is consistent with an '
               'oligopeptide.\n'
               ' * SMILES: '
               'CO[C@]12[C@H]3N[C@H]3CN1C1=C([C@H]2COC(N)=O)C(=O)C(O)=C(C)C1=O '
               'NAME: 7-demethylmitomycin A REASON: WRONGLY CLASSIFIED '
               'Detected 1 peptide bond(s) (≈2 residue(s)), 3 rotatable '
               'bond(s), 2 alpha–carbon center(s), and MW of 335.1 Da. The '
               'peptide-bond atoms form a single contiguous linear chain. This '
               'is consistent with an oligopeptide.\n'
               ' * SMILES: '
               'CN1[C@H]([C@@H]2CCN([C@@H]2C3=C1C=CC(=C3)C4=CC=C(C=C4)C#N)C(=O)NC5=CC(=CC=C5)F)CO '
               'NAME: '
               '(3aR,4R,9bS)-8-(4-cyanophenyl)-N-(3-fluorophenyl)-4-(hydroxymethyl)-5-methyl-3,3a,4,9b-tetrahydro-2H-pyrrolo[3,2-c]quinoline-1-carboxamide '
               'REASON: WRONGLY CLASSIFIED Detected 2 peptide bond(s) (≈3 '
               'residue(s)), 3 rotatable bond(s), 2 alpha–carbon center(s), '
               'and MW of 456.2 Da. The peptide-bond atoms form a single '
               'contiguous linear chain. This is consistent with an '
               'oligopeptide.\n'
               ' * SMILES: '
               'CC(C)NC(=O)N1CC2(C1)[C@@H]([C@H](N2CCC(F)(F)F)CO)C3=CC=CC=C3 '
               'NAME: '
               '(2S,3R)-2-(hydroxymethyl)-3-phenyl-N-propan-2-yl-1-(3,3,3-trifluoropropyl)-1,6-diazaspiro[3.3]heptane-6-carboxamide '
               'REASON: WRONGLY CLASSIFIED Detected 2 peptide bond(s) (≈3 '
               'residue(s)), 5 rotatable bond(s), 2 alpha–carbon center(s), '
               'and MW of 385.2 Da. The peptide-bond atoms form a single '
               'contiguous linear chain. This is consistent with an '
               'oligopeptide.\n'
               ' * SMILES: '
               'COC1=CC=CC=C1NC(=O)N2CCCCN3[C@@H](C2)[C@@H]([C@H]3CO)C4=CC=C(C=C4)C5=CC=CC(=C5)C#N '
               'NAME: '
               '(8R,9S,10S)-9-[4-(3-cyanophenyl)phenyl]-10-(hydroxymethyl)-N-(2-methoxyphenyl)-1,6-diazabicyclo[6.2.0]decane-6-carboxamide '
               'REASON: WRONGLY CLASSIFIED Detected 2 peptide bond(s) (≈3 '
               'residue(s)), 5 rotatable bond(s), 2 alpha–carbon center(s), '
               'and MW of 496.2 Da. The peptide-bond atoms form a single '
               'contiguous linear chain. This is consistent with an '
               'oligopeptide.\n'
               ' * SMILES: '
               'CC(C)NC(=O)N1[C@H]([C@H](C12CN(C2)CC3=CC(=CC(=C3)F)F)C4=CC=CC=C4)CO '
               'NAME: '
               '(2R,3R)-6-[(3,5-difluorophenyl)methyl]-2-(hydroxymethyl)-3-phenyl-N-propan-2-yl-1,6-diazaspiro[3.3]heptane-1-carboxamide '
               'REASON: WRONGLY CLASSIFIED Detected 2 peptide bond(s) (≈3 '
               'residue(s)), 5 rotatable bond(s), 2 alpha–carbon center(s), '
               'and MW of 415.2 Da. The peptide-bond atoms form a single '
               'contiguous linear chain. This is consistent with an '
               'oligopeptide.\n'
               ' * SMILES: '
               'C1[C@H]2[C@H]([C@H](N2CC3=CC=CC=C3Cl)CO)C4=CC=CC=C4N1C(=O)NC5=CC=CC=C5 '
               'NAME: '
               '(1S,2aR,8bR)-2-[(2-chlorophenyl)methyl]-1-(hydroxymethyl)-N-phenyl-1,2a,3,8b-tetrahydroazeto[2,3-c]quinoline-4-carboxamide '
               'REASON: WRONGLY CLASSIFIED Detected 2 peptide bond(s) (≈3 '
               'residue(s)), 4 rotatable bond(s), 2 alpha–carbon center(s), '
               'and MW of 433.2 Da. The peptide-bond atoms form a single '
               'contiguous linear chain. This is consistent with an '
               'oligopeptide.\n'
               ' * SMILES: '
               'C1CCC(C1)NC(=O)N2[C@@H]3CNC[C@H]2C3C4=CC=C(C=C4)C5=CN=CC=C5 '
               'NAME: '
               '(1S,5R)-N-cyclopentyl-7-[4-(3-pyridinyl)phenyl]-3,6-diazabicyclo[3.1.1]heptane-6-carboxamide '
               'REASON: WRONGLY CLASSIFIED Detected 2 peptide bond(s) (≈3 '
               'residue(s)), 3 rotatable bond(s), 3 alpha–carbon center(s), '
               'and MW of 362.2 Da. The peptide-bond atoms form a single '
               'contiguous linear chain. This is consistent with an '
               'oligopeptide.\n'
               ' * SMILES: C1[C@@H]2[C@@H]([C@H](N2C(=O)CN1)CO)C3=CC=C(C=C3)Br '
               'NAME: '
               '(6S,7S,8S)-7-(4-bromophenyl)-8-(hydroxymethyl)-1,4-diazabicyclo[4.2.0]octan-2-one '
               'REASON: WRONGLY CLASSIFIED Detected 1 peptide bond(s) (≈2 '
               'residue(s)), 2 rotatable bond(s), 2 alpha–carbon center(s), '
               'and MW of 310.0 Da. The peptide-bond atoms form a single '
               'contiguous linear chain. This is consistent with an '
               'oligopeptide.\n'
               ' * SMILES: '
               'C1OC2=C(O1)C=C(C=C2)C(=O)N3[C@@H]([C@@H]([C@@H]3C#N)C4=CC=CC=C4)CO '
               'NAME: '
               '(2R,3R,4S)-1-[1,3-benzodioxol-5-yl(oxo)methyl]-4-(hydroxymethyl)-3-phenyl-2-azetidinecarbonitrile '
               'REASON: WRONGLY CLASSIFIED Detected 1 peptide bond(s) (≈2 '
               'residue(s)), 3 rotatable bond(s), 2 alpha–carbon center(s), '
               'and MW of 336.1 Da. The peptide-bond atoms form a single '
               'contiguous linear chain. This is consistent with an '
               'oligopeptide.\n'
               ' * SMILES: '
               'CN1[C@@H]2CN(C3=CC=CC=C3[C@@H]2[C@@H]1CO)C(=O)C4=CC=C(C=C4)F '
               'NAME: '
               '[(1R,2aS,8bS)-1-(hydroxymethyl)-2-methyl-1,2a,3,8b-tetrahydroazeto[2,3-c]quinolin-4-yl]-(4-fluorophenyl)methanone '
               'REASON: WRONGLY CLASSIFIED Detected 1 peptide bond(s) (≈2 '
               'residue(s)), 2 rotatable bond(s), 2 alpha–carbon center(s), '
               'and MW of 326.1 Da. The peptide-bond atoms form a single '
               'contiguous linear chain. This is consistent with an '
               'oligopeptide.\n'
               'False negatives: SMILES: '
               'O=C(N[C@@H](CC(C)C)C(O)=O)[C@@H](NC(=O)[C@@H](N)CC1=CC=CC=C1)CC=2NC=NC2 '
               'NAME: Phe-His-Leu REASON: MISSED Peptide bond connectivity is '
               'not linear; expected a chain of 2 bonds but longest path found '
               'has 1 bonds\n'
               ' * SMILES: '
               'N([C@H](C(N[C@H](C(N[C@H](C(N[C@H](C(CF)=O)CC(=O)OC)=O)C(C)C)=O)CCC(OC)=O)=O)CC(OC)=O)C(OCC=1C=CC=CC1)=O '
               'NAME: Z-DEVD-FMK REASON: MISSED Peptide bond connectivity is '
               'not linear; expected a chain of 4 bonds but longest path found '
               'has 1 bonds\n'
               ' * SMILES: '
               'O=C(N[C@@H](CC=1C=2C(NC1)=CC=CC2)C(O)=O)[C@@H](NC(=O)[C@@H](N)CCCN=C(N)N)CC(C)C '
               'NAME: Arg-Leu-Trp REASON: MISSED Peptide bond connectivity is '
               'not linear; expected a chain of 2 bonds but longest path found '
               'has 1 bonds\n'
               ' * SMILES: NCC(N1[C@@H](CCC1)C(=O)NC=2C=CC3=C(C2)C=CC=C3)=O '
               'NAME: glycyl-L-proline 2-naphthylamide REASON: MISSED Expected '
               'at least 2 alpha–carbon centers; found 1\n'
               ' * SMILES: '
               'S1C(=NC(=C1)C(=O)N[C@H](C(=O)O)CCC(=O)N)[C@H]2N(C(=O)[C@@H](NC(=O)[C@@H](NC(=O)/C(/N3C(=O)N[C@H](C3=O)CC4=CC=C(O)C=C4)=C/C)C)CCCN=C(N)N)CCC2 '
               'NAME: Pseudovibriamide A2 REASON: MISSED Peptide bond '
               'connectivity is not linear; expected a chain of 8 bonds but '
               'longest path found has 3 bonds\n'
               ' * SMILES: '
               'O=C1N2[C@@H](C(=O)N[C@H](C(=O)N[C@H](C(=O)NCC(=O)N[C@H](C(=O)NCC(N[C@@H](C(N[C@@H](C(N3[C@H](C(N[C@@H]([C@@H]1NC(=O)[C@@H](NC(=O)C/C=C\\CCCCCCC(C)C)CC(=O)N)C)=O)CCC3)=O)C(C)C)=O)[C@H](N)C)=O)CC(=O)O)CC(=O)O)[C@@H](C(=O)O)C)CCCC2 '
               'NAME: Friulimicin A REASON: MISSED Found 14 amino acid '
               'residues which is too many for an oligopeptide\n'
               ' * SMILES: '
               'O=C(NCC(=O)N[C@@H](CCC(O)=O)C(O)=O)[C@@H](N)CC=1NC=NC1 NAME: '
               'His-Gly-Glu REASON: MISSED Peptide bond connectivity is not '
               'linear; expected a chain of 2 bonds but longest path found has '
               '1 bonds\n'
               ' * SMILES: '
               'O=C(N[C@@H](CCCN=C(N)N)C(=O)N[C@@H](CC1=CC=C(O)C=C1)C(O)=O)[C@@H](N)CC(C)C '
               'NAME: Leu-Arg-Tyr REASON: MISSED Peptide bond connectivity is '
               'not linear; expected a chain of 2 bonds but longest path found '
               'has 1 bonds\n'
               ' * SMILES: O=C(NCC(O)=O)[C@@H](NC(=O)CN)CC=1NC=NC1 NAME: '
               'Gly-His-Gly REASON: MISSED Expected at least 2 alpha–carbon '
               'centers; found 1\n'
               ' * SMILES: '
               'S1C(=NC(=C1)C(=O)N[C@@H](CC2=CC=CC=C2)C[C@@H](C(=O)O)C)[C@H](O)C[C@@H](N(C(=O)[C@@H](NC(=O)[C@@H]3N(CCCC3)C)[C@H](CC)C)COC(=O)CCC)C(C)C '
               'NAME: Desacetyltubulysin E REASON: MISSED Peptide bond '
               'connectivity is not linear; expected a chain of 3 bonds but '
               'longest path found has 1 bonds\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'O=C(N[C@@H](C(O)(C)C)C)[C@H]([C@@]1([C@@]2([C@@](CC1)(/C(/CCC2)=C/C=C\\3/C[C@@H](O)C[C@H](O)C3=C)[H])C)[H])C',
                                     'name': '1alpha,25-dihydroxy-24-oxo-23-azavitamin '
                                             'D2 / '
                                             '1alpha,25-dihydroxy-24-oxo-23-azaergocalciferol',
                                     'reason': 'For a dipeptide, exactly 2 '
                                               'alpha–carbon centers are '
                                               'expected; found 1'},
                                 {   'smiles': 'CCCCCCCCCCCCCCCCCCC(O)C([O-])=O',
                                     'name': '2-hydroxyarachidate',
                                     'reason': 'No peptide (amide) bonds found '
                                               '(or none outside ring '
                                               'systems)'},
                                 {   'smiles': 'C[C@@H](CN([C@@H](C)CO)C(=O)NC1=CC=C(C=C1)C(F)(F)F)[C@@H](CN(C)C(=O)C2CCOCC2)OC',
                                     'name': 'N-[(2S,3S)-4-[[(2S)-1-hydroxypropan-2-yl]-[[4-(trifluoromethyl)phenyl]carbamoyl]amino]-2-methoxy-3-methylbutyl]-N-methyloxane-4-carboxamide',
                                     'reason': 'Expected at least 2 '
                                               'alpha–carbon centers; found 1'},
                                 {   'smiles': 'CC(=O)CC\\C=C(/C)CCC=C(C)C',
                                     'name': 'geranyl acetone',
                                     'reason': 'No peptide (amide) bonds found '
                                               '(or none outside ring '
                                               'systems)'},
                                 {   'smiles': 'O([C@H]1[C@H](O)[C@H](O[C@H](O)[C@H]1O)CO[C@H]2O[C@@H]([C@@H](O)[C@H](O)[C@@H]2O)CO)[C@H]3O[C@@H]([C@@H](O)[C@H](O)[C@@H]3O[C@H]4O[C@@H]([C@@H](O)[C@H](O)[C@@H]4O)CO)CO',
                                     'name': '(2S,3S,4S,5S,6R)-2-[[(2R,3R,4S,5S,6S)-4-[(2R,3S,4S,5S,6R)-4,5-Dihydroxy-6-(hydroxymethyl)-3-[(2R,3S,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-3,5,6-trihydroxyoxan-2-yl]methoxy]-6-(hydroxymethyl)oxane-3,4,5-triol',
                                     'reason': 'No peptide (amide) bonds found '
                                               '(or none outside ring '
                                               'systems)'},
                                 {   'smiles': 'O=C(OC1=C(C(O)=C(C(=O)O)C(=C1C)C)C)C2=C(OC)C(=C(OC(=O)C3=C(O)C=C(O)C=C3C)C=C2C)C',
                                     'name': 'Thielavin Z5',
                                     'reason': 'No peptide (amide) bonds found '
                                               '(or none outside ring '
                                               'systems)'},
                                 {   'smiles': '[C@@H]1([C@@H]([C@H]([C@@H]([C@H](O1)CO)O)O)NC(C)=O)O[C@@H]2[C@@H]([C@H](C(O[C@@H]2CO)O)O)O',
                                     'name': 'beta-D-GlcpNAc-(1->4)-D-Galp',
                                     'reason': 'For a dipeptide, exactly 2 '
                                               'alpha–carbon centers are '
                                               'expected; found 1'},
                                 {   'smiles': 'CN(C)C(=O)C1=CC=C(C=C1)C2=CC=C(C=C2)[C@@H]3[C@H]4CN(CC(=O)N4[C@H]3CO)C(=O)CC5CC5',
                                     'name': '4-[4-[(6S,7R,8R)-4-(2-cyclopropyl-1-oxoethyl)-8-(hydroxymethyl)-2-oxo-1,4-diazabicyclo[4.2.0]octan-7-yl]phenyl]-N,N-dimethylbenzamide',
                                     'reason': 'Molecular weight (461.2 Da) is '
                                               'too high for a 2-residue '
                                               'peptide (expected at most 400 '
                                               'Da)'},
                                 {   'smiles': 'CCCCCCCCCCCCCCCCCCCCC=C',
                                     'name': '1-docosene',
                                     'reason': 'No peptide (amide) bonds found '
                                               '(or none outside ring '
                                               'systems)'},
                                 {   'smiles': 'C([C@@](OC(=O)CCC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)([H])COC(=O)CC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)OC(=O)CCCCC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC',
                                     'name': 'TG(22:5(7Z,10Z,13Z,16Z,19Z)/20:5(5Z,8Z,11Z,14Z,17Z)/22:6(4Z,7Z,10Z,13Z,16Z,19Z))[iso6]',
                                     'reason': 'No peptide (amide) bonds found '
                                               '(or none outside ring '
                                               'systems)'}],
    'sample_false_negatives': [   {   'smiles': 'NCC(N1[C@@H](CCC1)C(=O)NC=2C=CC3=C(C2)C=CC=C3)=O',
                                      'name': 'glycyl-L-proline '
                                              '2-naphthylamide',
                                      'reason': 'For a dipeptide, exactly 2 '
                                                'alpha–carbon centers are '
                                                'expected; found 1'},
                                  {   'smiles': 'O=C1N2[C@@H](C(=O)N[C@H](C(=O)N[C@H](C(=O)NCC(=O)N[C@H](C(=O)NCC(N[C@@H](C(N[C@@H](C(N3[C@H](C(N[C@@H]([C@@H]1NC(=O)[C@@H](NC(=O)C/C=C\\CCCCCCC(C)C)CC(=O)N)C)=O)CCC3)=O)C(C)C)=O)[C@H](N)C)=O)CC(=O)O)CC(=O)O)[C@@H](C(=O)O)C)CCCC2',
                                      'name': 'Friulimicin A',
                                      'reason': 'Molecular weight (1288.7 Da) '
                                                'is too high for a 4-residue '
                                                'peptide (expected at most 800 '
                                                'Da)'},
                                  {   'smiles': 'O=C(NCC(O)=O)[C@@H](NC(=O)CN)CC=1NC=NC1',
                                      'name': 'Gly-His-Gly',
                                      'reason': 'Expected at least 2 '
                                                'alpha–carbon centers; found '
                                                '1'},
                                  {   'smiles': 'S1CC2=C(O)C=C(O)C=C2C(=O)OC[C@@H](C(N[C@@H](C1)C(=O)N[C@H](C(=O)O)C)=O)NC(=O)[C@H]3N(C(=O)[C@@H](N)C)CC[C@H]3O',
                                      'name': 'Cyclothialidine B',
                                      'reason': 'Molecular weight (611.2 Da) '
                                                'is too high for a 3-residue '
                                                'peptide (expected at most 600 '
                                                'Da)'},
                                  {   'smiles': 'OC(=O)[C@@H](NC(=O)CNC(=O)CN)CCCCN',
                                      'name': 'Gly-Gly-Lys',
                                      'reason': 'Expected at least 2 '
                                                'alpha–carbon centers; found '
                                                '1'},
                                  {   'smiles': 'O=C(N[C@@H](CCC(O)=O)C(O)=O)[C@H]1N(CCC1)C(=O)[C@@H](N)CC2=CC=CC=C2',
                                      'name': 'Phe-Pro-Glu',
                                      'reason': 'For a dipeptide, exactly 2 '
                                                'alpha–carbon centers are '
                                                'expected; found 3'},
                                  {   'smiles': 'CC(C)[C@H](NC(=O)[C@@H](N)CC(O)=O)C(=O)N1CCC[C@H]1C(=O)N1CCC[C@H]1C(O)=O',
                                      'name': 'Asp-Val-Pro-Pro',
                                      'reason': 'For a dipeptide, exactly 2 '
                                                'alpha–carbon centers are '
                                                'expected; found 4'},
                                  {   'smiles': 'O=C(N[C@@H](CC1=CC=CC=C1)C(O)=O)[C@H]2N(CCC2)C(=O)[C@@H](N)CC3=CC=CC=C3',
                                      'name': 'Phe-Pro-Phe',
                                      'reason': 'For a dipeptide, exactly 2 '
                                                'alpha–carbon centers are '
                                                'expected; found 3'},
                                  {   'smiles': 'S(CC[C@H](NC(=O)[C@H]1N(CCC1)C(=O)[C@@H](N)C)C(O)=O)C',
                                      'name': 'Ala-Pro-Met',
                                      'reason': 'For a dipeptide, exactly 2 '
                                                'alpha–carbon centers are '
                                                'expected; found 3'},
                                  {   'smiles': 'OC1CC(N(C1)C(=O)C(N)C(C)C)C(O)=O',
                                      'name': 'Valyl-Hydroxyproline',
                                      'reason': 'No peptide (amide) bonds '
                                                'found (or none outside ring '
                                                'systems)'}],
    'attempt': 5,
    'reasoning': 'Below is one possibility. In my reasoning I decided to '
                 'remove the DFS‐based “linearity” test (which was too strict) '
                 'and instead require that (a) all the “peptide” bonds (found '
                 'by matching the amide SMARTS “C(=O)N”) are in one fragment '
                 'and outside rings (to avoid many false‐positive amide bonds) '
                 'and (b) if more than two residues are present then at least '
                 'one contiguous backbone fragment (matched by '
                 '“N[C@H](*)C(=O)N” or its mirror) is found. I also tightened '
                 'the molecular‐weight range (which depends on residue count) '
                 'to help weed out larger nonpeptide molecules. (There are '
                 'many borderline cases, so this heuristic may still '
                 'misclassify some edge molecules.) \n'
                 '\n'
                 'The code is given below:\n'
                 '\n'
                 '----------------------------------------------------------------',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 2651,
    'num_false_positives': 6318,
    'num_true_negatives': 132387,
    'num_false_negatives': 944,
    'num_negatives': None,
    'precision': 0.2955736425465492,
    'recall': 0.737413073713491,
    'f1': 0.4219993632601083,
    'accuracy': 0.9489669711876317,
    'negative_predictive_value': 0.9929198760978317}