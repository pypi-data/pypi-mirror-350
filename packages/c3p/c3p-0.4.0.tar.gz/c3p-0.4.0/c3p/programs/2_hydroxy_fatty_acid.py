"""
Classifies: CHEBI:10283 2-hydroxy fatty acid
"""
#!/usr/bin/env python3
"""
Classifies: 2-hydroxy fatty acid

Definition:
A 2–hydroxy fatty acid is an acyclic (non–ring) aliphatic molecule that bears
exactly one terminal carboxylic acid group. In addition, the unique carbon attached
to that acid group (the “alpha–carbon”) must carry exactly one hydroxyl (-OH)
substituent. No extra oxygen functionalities (beyond the two oxygens in the acid group
and the single alpha–OH) are allowed. Finally, a saturated fatty acid must have a sufficiently
long carbon chain (non–acid part ≥8 carbons) whereas unsaturated variants (showing C=C)
are allowed to be shorter.
"""

from rdkit import Chem

def is_2_hydroxy_fatty_acid(smiles: str):
    """
    Determines if a molecule qualifies as a 2–hydroxy fatty acid given its SMILES.
    
    The criteria are:
      1) The molecule must be acyclic (i.e. contain no rings).
      2) It must contain exactly one terminal carboxylic acid group (using the SMARTS
         "C(=O)[O;H1]").
      3) The unique (alpha–) carbon attached to the acid carbon must have exactly one
         hydroxyl (-OH) substituent (i.e. one oxygen attached that is hydrogenated).
      4) No other oxygen atoms should be present in the molecule.
      5) The molecule must contain only C, H, and O atoms.
      6) The fatty (non–acid) chain should be predominantly aliphatic.
      7) If the molecule is fully saturated (i.e. no C=C bonds) then the carbon chain
         (all carbons excluding the acid carbon) must be at least 8 atoms long.
         Unsaturated acids (with one or more C=C) are allowed to have shorter chains.
         
    Args:
         smiles (str): SMILES representation of the molecule.
         
    Returns:
         (bool, str): Tuple where the boolean indicates classification as a 2–hydroxy fatty acid,
                      and the reason details the decision.
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # 1. Reject molecules with rings.
    if mol.GetRingInfo().NumRings() > 0:
        return False, "Molecule contains ring(s), not an acyclic fatty acid"

    # 2. Ensure that only allowed elements (C, H, O) are present.
    for atom in mol.GetAtoms():
        if atom.GetSymbol() not in {"C", "H", "O"}:
            return False, f"Atom {atom.GetSymbol()} is not allowed in a typical fatty acid"

    # 3. Identify the terminal carboxylic acid group.
    # Use SMARTS: acid group pattern "C(=O)[O;H1]".
    carboxyl_smarts = "C(=O)[O;H1]"
    carboxyl_query = Chem.MolFromSmarts(carboxyl_smarts)
    carboxyl_matches = mol.GetSubstructMatches(carboxyl_query)
    if not carboxyl_matches:
        return False, "No carboxylic acid group found"

    # Expect exactly one unique acid carbon (atom 0 in each match).
    acid_carbon_idxs = set(match[0] for match in carboxyl_matches)
    if len(acid_carbon_idxs) != 1:
        return False, "Molecule must have exactly one terminal carboxylic acid group"
    acid_carbon_idx = list(acid_carbon_idxs)[0]
    acid_carbon = mol.GetAtomWithIdx(acid_carbon_idx)

    # Verify the acid carbon is terminal: one carbon neighbor and two oxygen neighbors.
    acid_neighbors = acid_carbon.GetNeighbors()
    oxy_neighbors = [nbr for nbr in acid_neighbors if nbr.GetAtomicNum() == 8]
    carbon_neighbors = [nbr for nbr in acid_neighbors if nbr.GetAtomicNum() == 6]
    if len(carbon_neighbors) != 1 or len(oxy_neighbors) != 2:
        return False, "Acid carbon is not terminal (unexpected bonding pattern)"

    # Allowed oxygens: those in the carboxyl group.
    allowed_oxygens = {nbr.GetIdx() for nbr in oxy_neighbors}

    # 4. Identify the alpha carbon (the sole carbon neighbor of the acid carbon).
    alpha_carbon = carbon_neighbors[0]

    # 5. Check alpha carbon has exactly one hydroxyl (-OH) substituent.
    alpha_oh_atoms = []
    for nbr in alpha_carbon.GetNeighbors():
        # Skip the acid carbon
        if nbr.GetIdx() == acid_carbon_idx:
            continue
        # Check if neighbor is oxygen and has at least one hydrogen
        if nbr.GetAtomicNum() == 8 and nbr.GetTotalNumHs() > 0:
            alpha_oh_atoms.append(nbr)
    if len(alpha_oh_atoms) != 1:
        return False, f"Alpha carbon must have exactly one hydroxyl substituent; found {len(alpha_oh_atoms)}"
    alpha_oh = alpha_oh_atoms[0]
    allowed_oxygens.add(alpha_oh.GetIdx())

    # 6. Ensure no unexpected oxygen is present.
    for atom in mol.GetAtoms():
        if atom.GetAtomicNum() == 8:
            if atom.GetIdx() not in allowed_oxygens:
                return False, f"Extra oxygen functionality found at atom index {atom.GetIdx()}"

    # 7. Check that the remainder of the molecule (non–acid part) is predominantly aliphatic.
    # Exclude the acid carbon and its two oxygens.
    excluded_idxs = {acid_carbon_idx} | allowed_oxygens
    non_acid_atoms = [atom for atom in mol.GetAtoms() if atom.GetIdx() not in excluded_idxs]
    if not non_acid_atoms:
        return False, "No carbon chain found outside the acid group"
    n_nonacid = len(non_acid_atoms)
    n_carbons = sum(1 for atom in non_acid_atoms if atom.GetAtomicNum() == 6)
    if n_carbons / n_nonacid < 0.75:
        return False, f"Non–acid part is not aliphatic enough (carbon fraction = {n_carbons/n_nonacid:.2f})"
    
    # 8. Count total number of carbon atoms in the molecule.
    total_carbons = sum(1 for atom in mol.GetAtoms() if atom.GetAtomicNum() == 6)
    # Define the fatty chain length as all carbons except the acid carbon.
    chain_length = total_carbons - 1

    # 9. If molecule is saturated (no C=C), require a minimum chain length.
    # Note: unsaturated acids may be naturally shorter.
    unsaturation = mol.HasSubstructMatch(Chem.MolFromSmarts("C=C"))
    if not unsaturation:
        # For saturated fatty acids, require that the chain (non–acid part) has at least 8 carbons.
        if chain_length < 8:
            return False, f"Saturated fatty acid chain too short ({chain_length} carbons; require at least 8)"
    
    # 10. Compose a reasoning message.
    reason = (f"Found a terminal carboxylic acid group (acid carbon idx {acid_carbon_idx}) with "
              f"an alpha carbon (idx {alpha_carbon.GetIdx()}) bearing a unique hydroxyl substituent, "
              f"and a predominantly aliphatic chain (chain length = {chain_length} carbons"
              f"{', unsaturated' if unsaturation else ', saturated'}), "
              f"classifying the molecule as a 2–hydroxy fatty acid.")
    return True, reason


# Example usage:
if __name__ == "__main__":
    # Example: (2R)-2-hydroxytetradecanoic acid
    test_smiles = "CCCCCCCCCCCC[C@@H](O)C(O)=O"
    result, classification_reason = is_2_hydroxy_fatty_acid(test_smiles)
    print(result, classification_reason)


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:10283',
                          'name': '2-hydroxy fatty acid',
                          'definition': 'Any fatty acid with a hydroxy '
                                        'functional group in the alpha- or '
                                        '2-position.',
                          'parents': ['CHEBI:24654', 'CHEBI:49302'],
                          'xrefs': [   'KEGG:C05102',
                                       'PMID:6423633',
                                       'PMID:9826358'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 103,
                           'log_lines_of_code': 4.634728988229636,
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
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 0,
                                                 1,
                                                 1,
                                                 2,
                                                 0,
                                                 1,
                                                 1,
                                                 2,
                                                 3,
                                                 0,
                                                 1,
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
                                                 0,
                                                 1,
                                                 1,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 3,
                                                 2,
                                                 2,
                                                 3,
                                                 1,
                                                 2,
                                                 1,
                                                 1,
                                                 0,
                                                 1,
                                                 1,
                                                 2,
                                                 3,
                                                 4,
                                                 0,
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
                                                 2,
                                                 2,
                                                 3,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 0,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 1],
                           'max_indent': 4,
                           'imports': ['from rdkit import Chem'],
                           'imports_count': 1,
                           'methods_called': [   'GetAtoms',
                                                 'NumRings',
                                                 'GetNeighbors',
                                                 'MolFromSmiles',
                                                 'HasSubstructMatch',
                                                 'GetRingInfo',
                                                 'GetSubstructMatches',
                                                 'append',
                                                 'GetSymbol',
                                                 'MolFromSmarts',
                                                 'GetAtomWithIdx',
                                                 'GetIdx',
                                                 'GetAtomicNum',
                                                 'add',
                                                 'GetTotalNumHs'],
                           'methods_called_count': 15,
                           'smarts_strings': ['carboxyl_smarts', '"C=C")'],
                           'smarts_strings_count': 2,
                           'defs': ['is_2_hydroxy_fatty_acid(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "Molecule contains ring(s), '
                                          'not an acyclic fatty acid"',
                                          'False, f"Atom {atom.GetSymbol()} is '
                                          'not allowed in a typical fatty '
                                          'acid"',
                                          'False, "No carboxylic acid group '
                                          'found"',
                                          'False, "Molecule must have exactly '
                                          'one terminal carboxylic acid group"',
                                          'False, "Acid carbon is not terminal '
                                          '(unexpected bonding pattern)"',
                                          'False, f"Alpha carbon must have '
                                          'exactly one hydroxyl substituent; '
                                          'found {len(alpha_oh_atoms)}"',
                                          'False, f"Extra oxygen functionality '
                                          'found at atom index '
                                          '{atom.GetIdx()}"',
                                          'False, "No carbon chain found '
                                          'outside the acid group"',
                                          'False, f"Non–acid part is not '
                                          'aliphatic enough (carbon fraction = '
                                          '{n_carbons/n_nonacid:.2f})"',
                                          'False, f"Saturated fatty acid chain '
                                          'too short ({chain_length} carbons; '
                                          'require at least 8)"',
                                          'True, reason'],
                           'returns_count': 12,
                           'complexity': 7.326945797645928},
    'message': '\n'
               'Attempt failed: F1 score of 0.7899159663865547 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: '
               'CCCCC\\C=C/C\\C=C/C\\C=C/C\\C=C/C\\C=C/CCCCCCCCCC(O)C(O)=O '
               'NAME: (12Z,15Z,18Z,21Z,24Z)-2-hydroxytriacontapentaenoic acid '
               'REASON: CORRECT Found a terminal carboxylic acid group (acid '
               'carbon idx 30) with an alpha carbon (idx 28) bearing a unique '
               'hydroxyl substituent, and a predominantly aliphatic chain '
               '(chain length = 29 carbons, carbon fraction = 1.00), '
               'classifying the molecule as a 2-hydroxy fatty acid.\n'
               ' * SMILES: CCCCCCCCCCCC[C@@H](O)C(O)=O NAME: '
               '(2R)-2-hydroxytetradecanoic acid REASON: CORRECT Found a '
               'terminal carboxylic acid group (acid carbon idx 14) with an '
               'alpha carbon (idx 12) bearing a unique hydroxyl substituent, '
               'and a predominantly aliphatic chain (chain length = 13 '
               'carbons, carbon fraction = 1.00), classifying the molecule as '
               'a 2-hydroxy fatty acid.\n'
               ' * SMILES: OC(=O)C(\\O)=C\\C=C NAME: '
               '(2Z)-2-hydroxypenta-2,4-dienoic acid REASON: CORRECT Found a '
               'terminal carboxylic acid group (acid carbon idx 1) with an '
               'alpha carbon (idx 3) bearing a unique hydroxyl substituent, '
               'and a predominantly aliphatic chain (chain length = 4 carbons, '
               'carbon fraction = 1.00), classifying the molecule as a '
               '2-hydroxy fatty acid.\n'
               ' * SMILES: CCCCCCCCCCCCCCCCCCCCC(O)C(O)=O NAME: '
               '2-hydroxybehenic acid REASON: CORRECT Found a terminal '
               'carboxylic acid group (acid carbon idx 22) with an alpha '
               'carbon (idx 20) bearing a unique hydroxyl substituent, and a '
               'predominantly aliphatic chain (chain length = 21 carbons, '
               'carbon fraction = 1.00), classifying the molecule as a '
               '2-hydroxy fatty acid.\n'
               ' * SMILES: '
               'CCCCC\\C=C/C\\C=C/C\\C=C/C\\C=C/CCCCCCCCCCC(O)C(O)=O NAME: '
               '(13Z,16Z,19Z,22Z)-2-hydroxyoctacosatetraenoic acid REASON: '
               'CORRECT Found a terminal carboxylic acid group (acid carbon '
               'idx 28) with an alpha carbon (idx 26) bearing a unique '
               'hydroxyl substituent, and a predominantly aliphatic chain '
               '(chain length = 27 carbons, carbon fraction = 1.00), '
               'classifying the molecule as a 2-hydroxy fatty acid.\n'
               ' * SMILES: C(\\CCCCCCC(C(=O)O)O)=C\\CCCCCCCC NAME: '
               '2-hydroxyoleic acid REASON: CORRECT Found a terminal '
               'carboxylic acid group (acid carbon idx 8) with an alpha carbon '
               '(idx 7) bearing a unique hydroxyl substituent, and a '
               'predominantly aliphatic chain (chain length = 17 carbons, '
               'carbon fraction = 1.00), classifying the molecule as a '
               '2-hydroxy fatty acid.\n'
               ' * SMILES: CCCCCCCCCCCCCC(O)C(O)=O NAME: '
               '2-hydroxypentadecanoic acid REASON: CORRECT Found a terminal '
               'carboxylic acid group (acid carbon idx 15) with an alpha '
               'carbon (idx 13) bearing a unique hydroxyl substituent, and a '
               'predominantly aliphatic chain (chain length = 14 carbons, '
               'carbon fraction = 1.00), classifying the molecule as a '
               '2-hydroxy fatty acid.\n'
               ' * SMILES: CCCCCCCCCCCCCCCCCCCCCCCCCC[C@@H](O)C(O)=O NAME: '
               '(R)-2-hydroxyoctacosanoic acid REASON: CORRECT Found a '
               'terminal carboxylic acid group (acid carbon idx 28) with an '
               'alpha carbon (idx 26) bearing a unique hydroxyl substituent, '
               'and a predominantly aliphatic chain (chain length = 27 '
               'carbons, carbon fraction = 1.00), classifying the molecule as '
               'a 2-hydroxy fatty acid.\n'
               ' * SMILES: C(C)CCCCCC/C=C\\CCCCCCCCCCC(C(=O)O)O NAME: '
               '2-hydroxyerucic acid REASON: CORRECT Found a terminal '
               'carboxylic acid group (acid carbon idx 21) with an alpha '
               'carbon (idx 20) bearing a unique hydroxyl substituent, and a '
               'predominantly aliphatic chain (chain length = 21 carbons, '
               'carbon fraction = 1.00), classifying the molecule as a '
               '2-hydroxy fatty acid.\n'
               ' * SMILES: CC(C)C[C@@H](O)C(O)=O NAME: '
               '(R)-2-hydroxy-4-methylpentanoic acid REASON: CORRECT Found a '
               'terminal carboxylic acid group (acid carbon idx 6) with an '
               'alpha carbon (idx 4) bearing a unique hydroxyl substituent, '
               'and a predominantly aliphatic chain (chain length = 5 carbons, '
               'carbon fraction = 1.00), classifying the molecule as a '
               '2-hydroxy fatty acid.\n'
               ' * SMILES: CC(C)CCCC(C)CCCC(C)CCCC(C)C(O)C(O)=O NAME: '
               '2-hydroxyphytanic acid REASON: CORRECT Found a terminal '
               'carboxylic acid group (acid carbon idx 20) with an alpha '
               'carbon (idx 18) bearing a unique hydroxyl substituent, and a '
               'predominantly aliphatic chain (chain length = 19 carbons, '
               'carbon fraction = 1.00), classifying the molecule as a '
               '2-hydroxy fatty acid.\n'
               ' * SMILES: CCCCCCC[C@@H](O)C(O)=O NAME: (R)-2-hydroxynonanoic '
               'acid REASON: CORRECT Found a terminal carboxylic acid group '
               '(acid carbon idx 9) with an alpha carbon (idx 7) bearing a '
               'unique hydroxyl substituent, and a predominantly aliphatic '
               'chain (chain length = 8 carbons, carbon fraction = 1.00), '
               'classifying the molecule as a 2-hydroxy fatty acid.\n'
               ' * SMILES: C(CCCCCCCC)CCC[C@@H](C(=O)O)O NAME: '
               '(2S)-2-hydroxytetradecanoic acid REASON: CORRECT Found a '
               'terminal carboxylic acid group (acid carbon idx 13) with an '
               'alpha carbon (idx 12) bearing a unique hydroxyl substituent, '
               'and a predominantly aliphatic chain (chain length = 13 '
               'carbons, carbon fraction = 1.00), classifying the molecule as '
               'a 2-hydroxy fatty acid.\n'
               ' * SMILES: CCCCCCCCCCCCCCCCCCCCCC[C@@H](O)C(O)=O NAME: '
               '(R)-2-hydroxylignoceric acid REASON: CORRECT Found a terminal '
               'carboxylic acid group (acid carbon idx 24) with an alpha '
               'carbon (idx 22) bearing a unique hydroxyl substituent, and a '
               'predominantly aliphatic chain (chain length = 23 carbons, '
               'carbon fraction = 1.00), classifying the molecule as a '
               '2-hydroxy fatty acid.\n'
               ' * SMILES: CCCCCCCC\\C=C/CCCCCCCCCCCCC(O)C(O)=O NAME: '
               '2-hydroxynervonic acid REASON: CORRECT Found a terminal '
               'carboxylic acid group (acid carbon idx 24) with an alpha '
               'carbon (idx 22) bearing a unique hydroxyl substituent, and a '
               'predominantly aliphatic chain (chain length = 23 carbons, '
               'carbon fraction = 1.00), classifying the molecule as a '
               '2-hydroxy fatty acid.\n'
               ' * SMILES: CCCCCCCCCCCCCC[C@@H](O)C(O)=O NAME: '
               '(R)-2-hydroxyhexadecanoic acid REASON: CORRECT Found a '
               'terminal carboxylic acid group (acid carbon idx 16) with an '
               'alpha carbon (idx 14) bearing a unique hydroxyl substituent, '
               'and a predominantly aliphatic chain (chain length = 15 '
               'carbons, carbon fraction = 1.00), classifying the molecule as '
               'a 2-hydroxy fatty acid.\n'
               ' * SMILES: OC(CCCCCC/C=C/C/C=C\\C/C=C\\CC)C(O)=O NAME: '
               '2-Hydroxylinolenic acid REASON: CORRECT Found a terminal '
               'carboxylic acid group (acid carbon idx 18) with an alpha '
               'carbon (idx 1) bearing a unique hydroxyl substituent, and a '
               'predominantly aliphatic chain (chain length = 17 carbons, '
               'carbon fraction = 1.00), classifying the molecule as a '
               '2-hydroxy fatty acid.\n'
               ' * SMILES: CCCCCCCCCC[C@@H](O)C(O)=O NAME: (R)-2-hydroxylauric '
               'acid REASON: CORRECT Found a terminal carboxylic acid group '
               '(acid carbon idx 12) with an alpha carbon (idx 10) bearing a '
               'unique hydroxyl substituent, and a predominantly aliphatic '
               'chain (chain length = 11 carbons, carbon fraction = 1.00), '
               'classifying the molecule as a 2-hydroxy fatty acid.\n'
               ' * SMILES: CCCCCCCCCCCCCCCCCCCCCCCCC(O)C(O)=O NAME: '
               '2-hydroxyhexacosanoic acid REASON: CORRECT Found a terminal '
               'carboxylic acid group (acid carbon idx 26) with an alpha '
               'carbon (idx 24) bearing a unique hydroxyl substituent, and a '
               'predominantly aliphatic chain (chain length = 25 carbons, '
               'carbon fraction = 1.00), classifying the molecule as a '
               '2-hydroxy fatty acid.\n'
               ' * SMILES: CCCCCCCCCCCCCCCCCCCCCCC(O)C(O)=O NAME: cerebronic '
               'acid REASON: CORRECT Found a terminal carboxylic acid group '
               '(acid carbon idx 24) with an alpha carbon (idx 22) bearing a '
               'unique hydroxyl substituent, and a predominantly aliphatic '
               'chain (chain length = 23 carbons, carbon fraction = 1.00), '
               'classifying the molecule as a 2-hydroxy fatty acid.\n'
               ' * SMILES: CCCCCCCCCCCCCCCCCCCCCC(O)C(O)=O NAME: '
               '2-hydroxytricosanoic acid REASON: CORRECT Found a terminal '
               'carboxylic acid group (acid carbon idx 23) with an alpha '
               'carbon (idx 21) bearing a unique hydroxyl substituent, and a '
               'predominantly aliphatic chain (chain length = 22 carbons, '
               'carbon fraction = 1.00), classifying the molecule as a '
               '2-hydroxy fatty acid.\n'
               ' * SMILES: C(=O)(C(CCCCCCCC/C=C\\CCCCCCCC)O)O NAME: '
               '2-hydroxygondoic acid REASON: CORRECT Found a terminal '
               'carboxylic acid group (acid carbon idx 0) with an alpha carbon '
               '(idx 2) bearing a unique hydroxyl substituent, and a '
               'predominantly aliphatic chain (chain length = 19 carbons, '
               'carbon fraction = 1.00), classifying the molecule as a '
               '2-hydroxy fatty acid.\n'
               ' * SMILES: CCCCCCCCCCCC(O)C(O)=O NAME: 2-hydroxytridecanoic '
               'acid REASON: CORRECT Found a terminal carboxylic acid group '
               '(acid carbon idx 13) with an alpha carbon (idx 11) bearing a '
               'unique hydroxyl substituent, and a predominantly aliphatic '
               'chain (chain length = 12 carbons, carbon fraction = 1.00), '
               'classifying the molecule as a 2-hydroxy fatty acid.\n'
               ' * SMILES: CC(C)C[C@H](O)C(O)=O NAME: '
               '(S)-2-hydroxy-4-methylpentanoic acid REASON: CORRECT Found a '
               'terminal carboxylic acid group (acid carbon idx 6) with an '
               'alpha carbon (idx 4) bearing a unique hydroxyl substituent, '
               'and a predominantly aliphatic chain (chain length = 5 carbons, '
               'carbon fraction = 1.00), classifying the molecule as a '
               '2-hydroxy fatty acid.\n'
               ' * SMILES: C(CCCCCCC=C(C(=O)O)O)CC NAME: '
               '2-hydroxydodec-2-enoic acid REASON: CORRECT Found a terminal '
               'carboxylic acid group (acid carbon idx 9) with an alpha carbon '
               '(idx 8) bearing a unique hydroxyl substituent, and a '
               'predominantly aliphatic chain (chain length = 11 carbons, '
               'carbon fraction = 1.00), classifying the molecule as a '
               '2-hydroxy fatty acid.\n'
               'False positives: SMILES: O[C@@H]([C@H](CC)C)C(O)=O NAME: '
               'L-Isoleucic acid REASON: WRONGLY CLASSIFIED Found a terminal '
               'carboxylic acid group (acid carbon idx 6) with an alpha carbon '
               '(idx 1) bearing a unique hydroxyl substituent, and a '
               'predominantly aliphatic chain (chain length = 5 carbons, '
               'carbon fraction = 1.00), classifying the molecule as a '
               '2-hydroxy fatty acid.\n'
               ' * SMILES: CCC(O)C(O)=O NAME: 2-hydroxybutyric acid REASON: '
               'WRONGLY CLASSIFIED Found a terminal carboxylic acid group '
               '(acid carbon idx 4) with an alpha carbon (idx 2) bearing a '
               'unique hydroxyl substituent, and a predominantly aliphatic '
               'chain (chain length = 3 carbons, carbon fraction = 1.00), '
               'classifying the molecule as a 2-hydroxy fatty acid.\n'
               ' * SMILES: OC(CCCCCCCCCCCCCCCCCCCC(CC)C)C(O)=O NAME: '
               '2-Hydroxy-22-methyltetracosanoic acid REASON: WRONGLY '
               'CLASSIFIED Found a terminal carboxylic acid group (acid carbon '
               'idx 25) with an alpha carbon (idx 1) bearing a unique hydroxyl '
               'substituent, and a predominantly aliphatic chain (chain length '
               '= 24 carbons, carbon fraction = 1.00), classifying the '
               'molecule as a 2-hydroxy fatty acid.\n'
               ' * SMILES: OC(=O)C(\\O)=C(\\Cl)C=C NAME: '
               '2-Hydroxy-3-chloropenta-2,4-dienoate REASON: WRONGLY '
               'CLASSIFIED Found a terminal carboxylic acid group (acid carbon '
               'idx 1) with an alpha carbon (idx 3) bearing a unique hydroxyl '
               'substituent, and a predominantly aliphatic chain (chain length '
               '= 4 carbons, carbon fraction = 0.80), classifying the molecule '
               'as a 2-hydroxy fatty acid.\n'
               ' * SMILES: CCC(N)(O)C(O)=O NAME: 2-amino-2-hydroxybutanoic '
               'acid REASON: WRONGLY CLASSIFIED Found a terminal carboxylic '
               'acid group (acid carbon idx 5) with an alpha carbon (idx 2) '
               'bearing a unique hydroxyl substituent, and a predominantly '
               'aliphatic chain (chain length = 3 carbons, carbon fraction = '
               '0.75), classifying the molecule as a 2-hydroxy fatty acid.\n'
               ' * SMILES: C\\C=C/C=C(/O)C(O)=O NAME: '
               '2-Hydroxy-cis-hex-2,4-dienoate REASON: WRONGLY CLASSIFIED '
               'Found a terminal carboxylic acid group (acid carbon idx 6) '
               'with an alpha carbon (idx 4) bearing a unique hydroxyl '
               'substituent, and a predominantly aliphatic chain (chain length '
               '= 5 carbons, carbon fraction = 1.00), classifying the molecule '
               'as a 2-hydroxy fatty acid.\n'
               ' * SMILES: CC[C@H](O)C(O)=O NAME: (S)-2-hydroxybutyric acid '
               'REASON: WRONGLY CLASSIFIED Found a terminal carboxylic acid '
               'group (acid carbon idx 4) with an alpha carbon (idx 2) bearing '
               'a unique hydroxyl substituent, and a predominantly aliphatic '
               'chain (chain length = 3 carbons, carbon fraction = 1.00), '
               'classifying the molecule as a 2-hydroxy fatty acid.\n'
               ' * SMILES: CCCC(O)C(O)=O NAME: 2-hydroxypentanoic acid REASON: '
               'WRONGLY CLASSIFIED Found a terminal carboxylic acid group '
               '(acid carbon idx 5) with an alpha carbon (idx 3) bearing a '
               'unique hydroxyl substituent, and a predominantly aliphatic '
               'chain (chain length = 4 carbons, carbon fraction = 1.00), '
               'classifying the molecule as a 2-hydroxy fatty acid.\n'
               ' * SMILES: C(O)(=O)C(CCCCCCCC=C)O NAME: '
               '2-hydroxy-10-undecenoic acid REASON: WRONGLY CLASSIFIED Found '
               'a terminal carboxylic acid group (acid carbon idx 0) with an '
               'alpha carbon (idx 3) bearing a unique hydroxyl substituent, '
               'and a predominantly aliphatic chain (chain length = 10 '
               'carbons, carbon fraction = 1.00), classifying the molecule as '
               'a 2-hydroxy fatty acid.\n'
               ' * SMILES: O[C@H](CCCCCCCCCCCCC)C(O)=O NAME: '
               '2R-hydroxy-pentadecanoic acid REASON: WRONGLY CLASSIFIED Found '
               'a terminal carboxylic acid group (acid carbon idx 15) with an '
               'alpha carbon (idx 1) bearing a unique hydroxyl substituent, '
               'and a predominantly aliphatic chain (chain length = 14 '
               'carbons, carbon fraction = 1.00), classifying the molecule as '
               'a 2-hydroxy fatty acid.\n'
               ' * SMILES: O[C@H](CCCCCC/C=C\\CCCCCCCC)C(O)=O NAME: '
               '2R-hydroxy-oleic acid REASON: WRONGLY CLASSIFIED Found a '
               'terminal carboxylic acid group (acid carbon idx 18) with an '
               'alpha carbon (idx 1) bearing a unique hydroxyl substituent, '
               'and a predominantly aliphatic chain (chain length = 17 '
               'carbons, carbon fraction = 1.00), classifying the molecule as '
               'a 2-hydroxy fatty acid.\n'
               ' * SMILES: CC[C@@H](O)C(O)=O NAME: (R)-2-hydroxybutyric acid '
               'REASON: WRONGLY CLASSIFIED Found a terminal carboxylic acid '
               'group (acid carbon idx 4) with an alpha carbon (idx 2) bearing '
               'a unique hydroxyl substituent, and a predominantly aliphatic '
               'chain (chain length = 3 carbons, carbon fraction = 1.00), '
               'classifying the molecule as a 2-hydroxy fatty acid.\n'
               ' * SMILES: CC(C)(O)C(O)=O NAME: 2-hydroxyisobutyric acid '
               'REASON: WRONGLY CLASSIFIED Found a terminal carboxylic acid '
               'group (acid carbon idx 4) with an alpha carbon (idx 1) bearing '
               'a unique hydroxyl substituent, and a predominantly aliphatic '
               'chain (chain length = 3 carbons, carbon fraction = 1.00), '
               'classifying the molecule as a 2-hydroxy fatty acid.\n'
               ' * SMILES: CC(C)[C@H](O)C(O)=O NAME: '
               '(S)-2-hydroxy-3-methylbutyric acid REASON: WRONGLY CLASSIFIED '
               'Found a terminal carboxylic acid group (acid carbon idx 5) '
               'with an alpha carbon (idx 3) bearing a unique hydroxyl '
               'substituent, and a predominantly aliphatic chain (chain length '
               '= 4 carbons, carbon fraction = 1.00), classifying the molecule '
               'as a 2-hydroxy fatty acid.\n'
               ' * SMILES: C\\C=C/C=C(\\O)C(O)=O NAME: '
               '(2Z,4Z)-2-hydroxyhexa-2,4-dienoic acid REASON: WRONGLY '
               'CLASSIFIED Found a terminal carboxylic acid group (acid carbon '
               'idx 6) with an alpha carbon (idx 4) bearing a unique hydroxyl '
               'substituent, and a predominantly aliphatic chain (chain length '
               '= 5 carbons, carbon fraction = 1.00), classifying the molecule '
               'as a 2-hydroxy fatty acid.\n'
               ' * SMILES: O[C@H](CCCCCC)C(O)=O NAME: (R)-2-Hydroxycaprylic '
               'acid REASON: WRONGLY CLASSIFIED Found a terminal carboxylic '
               'acid group (acid carbon idx 8) with an alpha carbon (idx 1) '
               'bearing a unique hydroxyl substituent, and a predominantly '
               'aliphatic chain (chain length = 7 carbons, carbon fraction = '
               '1.00), classifying the molecule as a 2-hydroxy fatty acid.\n'
               ' * SMILES: OC(C(O)=O)=C(C)C NAME: '
               '2-hydroxy-3-methyl-2-butenoic acid REASON: WRONGLY CLASSIFIED '
               'Found a terminal carboxylic acid group (acid carbon idx 2) '
               'with an alpha carbon (idx 1) bearing a unique hydroxyl '
               'substituent, and a predominantly aliphatic chain (chain length '
               '= 4 carbons, carbon fraction = 1.00), classifying the molecule '
               'as a 2-hydroxy fatty acid.\n'
               ' * SMILES: O=C(O)[C@H](O)C(C)C NAME: '
               '(R)-2-hydroxy-3-methylbutyric acid REASON: WRONGLY CLASSIFIED '
               'Found a terminal carboxylic acid group (acid carbon idx 1) '
               'with an alpha carbon (idx 3) bearing a unique hydroxyl '
               'substituent, and a predominantly aliphatic chain (chain length '
               '= 4 carbons, carbon fraction = 1.00), classifying the molecule '
               'as a 2-hydroxy fatty acid.\n'
               ' * SMILES: CC(C)C(O)C(O)=O NAME: 2-hydroxy-3-methylbutyric '
               'acid REASON: WRONGLY CLASSIFIED Found a terminal carboxylic '
               'acid group (acid carbon idx 5) with an alpha carbon (idx 3) '
               'bearing a unique hydroxyl substituent, and a predominantly '
               'aliphatic chain (chain length = 4 carbons, carbon fraction = '
               '1.00), classifying the molecule as a 2-hydroxy fatty acid.\n'
               ' * SMILES: O[C@@H](CCCCCCCC)C(O)=O NAME: 2S-hydroxy-decanoic '
               'acid REASON: WRONGLY CLASSIFIED Found a terminal carboxylic '
               'acid group (acid carbon idx 10) with an alpha carbon (idx 1) '
               'bearing a unique hydroxyl substituent, and a predominantly '
               'aliphatic chain (chain length = 9 carbons, carbon fraction = '
               '1.00), classifying the molecule as a 2-hydroxy fatty acid.\n'
               ' * SMILES: CSCCC(C(=O)O)O NAME: '
               '2-hydroxy-4-(methylthio)butanoic acid REASON: WRONGLY '
               'CLASSIFIED Found a terminal carboxylic acid group (acid carbon '
               'idx 5) with an alpha carbon (idx 4) bearing a unique hydroxyl '
               'substituent, and a predominantly aliphatic chain (chain length '
               '= 4 carbons, carbon fraction = 0.80), classifying the molecule '
               'as a 2-hydroxy fatty acid.\n'
               ' * SMILES: O[C@H](CCCCCCCC=C)C(O)=O NAME: '
               '2R-hydroxy-10-undecenoic acid REASON: WRONGLY CLASSIFIED Found '
               'a terminal carboxylic acid group (acid carbon idx 11) with an '
               'alpha carbon (idx 1) bearing a unique hydroxyl substituent, '
               'and a predominantly aliphatic chain (chain length = 10 '
               'carbons, carbon fraction = 1.00), classifying the molecule as '
               'a 2-hydroxy fatty acid.\n'
               ' * SMILES: CCCCC(O)C(O)=O NAME: 2-hydroxyhexanoic acid REASON: '
               'WRONGLY CLASSIFIED Found a terminal carboxylic acid group '
               '(acid carbon idx 6) with an alpha carbon (idx 4) bearing a '
               'unique hydroxyl substituent, and a predominantly aliphatic '
               'chain (chain length = 5 carbons, carbon fraction = 1.00), '
               'classifying the molecule as a 2-hydroxy fatty acid.\n'
               ' * SMILES: CCCCCCC(O)C(O)=O NAME: 2-hydroxyoctanoic acid '
               'REASON: WRONGLY CLASSIFIED Found a terminal carboxylic acid '
               'group (acid carbon idx 8) with an alpha carbon (idx 6) bearing '
               'a unique hydroxyl substituent, and a predominantly aliphatic '
               'chain (chain length = 7 carbons, carbon fraction = 1.00), '
               'classifying the molecule as a 2-hydroxy fatty acid.\n'
               ' * SMILES: OC(=CC)C(O)=O NAME: 2-hydroxy-2-butenoic acid '
               'REASON: WRONGLY CLASSIFIED Found a terminal carboxylic acid '
               'group (acid carbon idx 4) with an alpha carbon (idx 1) bearing '
               'a unique hydroxyl substituent, and a predominantly aliphatic '
               'chain (chain length = 3 carbons, carbon fraction = 1.00), '
               'classifying the molecule as a 2-hydroxy fatty acid.\n'
               'False negatives: NONE\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'O=C1OC[C@@H]2O[C@@H](O[C@@H]3[C@@H](OC(=O)CCCCCCCCCCCCCCC)[C@H](C=CCCCC1)[C@H](CCCCC)[C@@H](C3)O)[C@H](O)[C@H]([C@@H]2O)O',
                                     'name': 'Mucorolactone',
                                     'reason': 'Molecule contains ring(s), not '
                                               'an acyclic fatty acid'},
                                 {   'smiles': 'C[C@@H]1CN[C@H](COC2=C(C=CC(=C2)NC(=O)C3=NC4=CC=CC=C4S3)C(=O)N(C[C@H]1OC)C)C',
                                     'name': 'N-[(5S,6R,9S)-5-methoxy-3,6,9-trimethyl-2-oxo-11-oxa-3,8-diazabicyclo[10.4.0]hexadeca-1(12),13,15-trien-14-yl]-1,3-benzothiazole-2-carboxamide',
                                     'reason': 'Molecule contains ring(s), not '
                                               'an acyclic fatty acid'},
                                 {   'smiles': 'COC1=CC=CC(=C1)C2=CC=C(C=C2)[C@@H]3[C@@H]4CN(CC(=O)N4[C@@H]3CO)C(=O)C5=CN=CC=C5',
                                     'name': '(6R,7R,8S)-8-(hydroxymethyl)-7-[4-(3-methoxyphenyl)phenyl]-4-[oxo(3-pyridinyl)methyl]-1,4-diazabicyclo[4.2.0]octan-2-one',
                                     'reason': 'Molecule contains ring(s), not '
                                               'an acyclic fatty acid'},
                                 {   'smiles': 'C(C(/C=C/C=C/C=C/[C@H](CCCC(O)=O)O)=O)/C=C\\CCCCC',
                                     'name': '12-oxo-6-trans-leukotriene B4',
                                     'reason': 'Alpha carbon must have exactly '
                                               'one hydroxyl substituent; '
                                               'found 0'},
                                 {   'smiles': 'O=C1OC(=C(C#C[C@H](COC(=O)C)C)CO)C=C1',
                                     'name': "5'-O-acetylaporpinone A",
                                     'reason': 'Molecule contains ring(s), not '
                                               'an acyclic fatty acid'},
                                 {   'smiles': 'O=C(N1[C@@H](CCC1)C(=O)N[C@@H](CCC(=O)N)C(O)=O)[C@@H](N)[C@H](CC)C',
                                     'name': 'Ile-Pro-Gln',
                                     'reason': 'Molecule contains ring(s), not '
                                               'an acyclic fatty acid'},
                                 {   'smiles': 'O[C@@H]1C=CC=C(CCC(O)=O)[C@@H]1O',
                                     'name': '3-[(5R,6S)-5,6-dihydroxycyclohexa-1,3-dienyl]propanoic '
                                             'acid',
                                     'reason': 'Molecule contains ring(s), not '
                                               'an acyclic fatty acid'},
                                 {   'smiles': 'O=C(OC)/C=C/C(C)(C)C',
                                     'name': '4,4-Dimethyl-pentenoic acid '
                                             'methyl ester',
                                     'reason': 'No carboxylic acid group '
                                               'found'},
                                 {   'smiles': 'CCCCOc1ccc(OCCCN2CCOCC2)cc1',
                                     'name': 'pramocaine',
                                     'reason': 'Molecule contains ring(s), not '
                                               'an acyclic fatty acid'},
                                 {   'smiles': 'OC[C@@H](O)C(=O)[C@H](O)[C@H](O)COP(O)(O)=O',
                                     'name': 'D-arabino-hex-3-ulose '
                                             '6-phosphate',
                                     'reason': 'Atom P is not allowed in a '
                                               'typical fatty acid'}],
    'sample_false_negatives': [   {   'smiles': 'CC(C)C[C@@H](O)C(O)=O',
                                      'name': '(R)-2-hydroxy-4-methylpentanoic '
                                              'acid',
                                      'reason': 'Saturated fatty acid chain '
                                                'too short (5 carbons; require '
                                                'at least 8)'},
                                  {   'smiles': 'CC(C)C[C@H](O)C(O)=O',
                                      'name': '(S)-2-hydroxy-4-methylpentanoic '
                                              'acid',
                                      'reason': 'Saturated fatty acid chain '
                                                'too short (5 carbons; require '
                                                'at least 8)'},
                                  {   'smiles': 'O[C@H]([C@@H](CC)C)C(O)=O',
                                      'name': '(2R,3R)-2-hydroxy-3-methylpentanoic '
                                              'acid',
                                      'reason': 'Saturated fatty acid chain '
                                                'too short (5 carbons; require '
                                                'at least 8)'},
                                  {   'smiles': 'CCC(C)(O)C(O)=O',
                                      'name': '2-hydroxy-2-methylbutyric acid',
                                      'reason': 'Saturated fatty acid chain '
                                                'too short (4 carbons; require '
                                                'at least 8)'},
                                  {   'smiles': 'OC(C(CC)C)C(O)=O',
                                      'name': '2-hydroxy-3-methylpentanoic '
                                              'acid',
                                      'reason': 'Saturated fatty acid chain '
                                                'too short (5 carbons; require '
                                                'at least 8)'},
                                  {   'smiles': 'C(C(C(O)=O)O)C(C)C',
                                      'name': '2-hydroxy-4-methylvaleric acid',
                                      'reason': 'Saturated fatty acid chain '
                                                'too short (5 carbons; require '
                                                'at least 8)'},
                                  {   'smiles': 'CCCCCC(O)C(O)=O',
                                      'name': '2-hydroxyheptanoic acid',
                                      'reason': 'Saturated fatty acid chain '
                                                'too short (6 carbons; require '
                                                'at least 8)'}],
    'attempt': 5,
    'reasoning': 'Below is my reasoning:\n'
                 '\n'
                 '• The previous code checked for a terminal –COOH group and '
                 'exactly one –OH attached to its alpha (2–) carbon. It also '
                 'required that no extra oxygen be present and that most '
                 'non–acid atoms be carbon. However, nearly all false '
                 'positives came from very short-chain molecules (such as '
                 '2–hydroxybutyric acid or L–isoleucic acid) that otherwise '
                 '“look like” a 2–hydroxy fatty acid by the earlier pattern. '
                 'In contrast, most “true” 2–hydroxy fatty acids (even '
                 'unsaturated ones) have a long enough aliphatic chain when '
                 'the molecule is saturated. At the same time, unsaturated '
                 '(conjugated) acids may be allowed even with a very short '
                 'chain.\n'
                 '\n'
                 '• Therefore I add an extra rule: if the molecule does not '
                 'display any C=C (i.e. it is saturated), then its overall '
                 'carbon count (minus the acid carbon) must be at least eight. '
                 'Also, I add a check that the molecule be composed solely of '
                 'C, H, and O (as expected for fatty acids). In this way the '
                 'false positives (which are very short fatty acid–like acids '
                 'or contain additional heteroatoms) will be rejected while '
                 'the true positives pass.\n'
                 '\n'
                 'Below is the complete Python code in a single code block.\n'
                 '\n'
                 '------------------------------------------------',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 40,
    'num_false_positives': 11,
    'num_true_negatives': 142242,
    'num_false_negatives': 7,
    'num_negatives': None,
    'precision': 0.7843137254901961,
    'recall': 0.851063829787234,
    'f1': 0.8163265306122448,
    'accuracy': 0.9998735066760366,
    'negative_predictive_value': 0.9999507905152233}