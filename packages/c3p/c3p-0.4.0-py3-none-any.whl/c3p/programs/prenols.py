"""
Classifies: CHEBI:26244 prenols
"""
"""
Classifies: Prenols – any alcohol possessing the general formula 
    H-[CH2C(Me)=CHCH2]nOH 
where the carbon skeleton is exclusively composed of one or more isoprene units.
This version tries to “cover” the entire molecule (apart from hydrogens) with isoprene units.
Heuristic steps:
  1. Parse the SMILES string; the molecule must be acyclic.
  2. Only carbon and oxygen atoms are allowed.
  3. At least one free hydroxyl group (–OH not in –C(=O)OH) must be present.
     Moreover, at least one free –OH must be terminal (attached to a primary C).
  4. Count all carbon atoms; the total should be a multiple of five.
  5. Using two SMARTS patterns representing an isoprene unit:
         Pattern1: "[CH3]-[C]([CH3])=[CH]-[CH2]"
         Pattern2: "[CH2]-[C]([CH3])=[CH]-[CH2]"
     we gather all matches and then try to select the maximum number of non–overlapping matches.
  6. We “expect” that number to exactly equal (total_C / 5).
If everything checks, we classify the molecule as a prenol.
"""

from rdkit import Chem

def is_prenols(smiles: str):
    """
    Determines if a molecule is a prenol based on its SMILES string.
    
    A prenol is defined as an alcohol whose carbon skeleton is exclusively
    composed of one or more isoprene units. (Isoprene unit is defined as 
    CH2–C(CH3)=CH–CH2.)
    
    Heuristic steps:
      - The molecule must be valid and acyclic.
      - It must contain only C and O as heavy atoms.
      - It must contain at least one free hydroxyl group (–OH) that is not part
        of a carboxyl.
      - It must have 1 or 2 free (i.e. terminal) hydroxyls.
      - Its total number of carbons should be divisible by 5.
      - It must “contain” n non–overlapping isoprene units (as determined by 
        two SMARTS patterns) where n = (number of carbons)//5.
    
    Args:
      smiles (str): SMILES string of the molecule.
      
    Returns:
      bool: True if molecule is classified as a prenol, False otherwise.
      str: Explanation of the decision.
    """
    
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
    
    # Reject cyclic molecules.
    if mol.GetRingInfo().NumRings() > 0:
        return False, "Molecule is cyclic, not a prenol"
    
    # Reject if any heavy atom is not C (atomic num 6) or O (atomic num 8).
    for atom in mol.GetAtoms():
        if atom.GetAtomicNum() not in (6, 8):
            return False, f"Molecule contains atom {atom.GetSymbol()} not in (C,O)"
    
    # Identify all free hydroxyl groups.
    # We first match any hydroxyl: [OX2H]
    alcohol_pattern = Chem.MolFromSmarts("[OX2H]")
    alcohol_matches = mol.GetSubstructMatches(alcohol_pattern)
    if not alcohol_matches:
        return False, "No hydroxyl (alcohol) group found"
    
    # Exclude those that are part of a carboxyl group: C(=O)[OX2H]
    carboxyl_pattern = Chem.MolFromSmarts("C(=O)[OX2H]")
    carboxyl_matches = mol.GetSubstructMatches(carboxyl_pattern)
    
    # Convert matches to a set of oxygen atom indices that belong to carboxyl.
    carboxyl_oxygens = set()
    for match in carboxyl_matches:
        # match[1] is the oxygen in "O" of the pattern
        carboxyl_oxygens.add(match[1])
    
    # Filter free alcohols (oxygens not in a carboxyl)
    free_alcohols = [match for match in alcohol_matches if match[0] not in carboxyl_oxygens]
    if not free_alcohols:
        return False, "Only carboxylic acid hydroxyl(s) found; no free hydroxyl present"
    
    # Now ensure at least one of the free hydroxyls is “terminal”
    # i.e. the oxygen is attached to a primary carbon (the attached carbon has only one heavy neighbor aside from O).
    terminal_OH_count = 0
    for match in free_alcohols:
        # Each alcohol match gives the oxygen atom index.
        o_atom = mol.GetAtomWithIdx(match[0])
        # Get neighbors – there should be exactly one heavy neighbor.
        neighbors = [nbr for nbr in o_atom.GetNeighbors() if nbr.GetAtomicNum() > 1]  # ignore hydrogens
        if len(neighbors) == 1:
            c_atom = neighbors[0]
            # Check how many heavy neighbors does the carbon have (excluding the oxygen we came from).
            c_neighbors = [nbr for nbr in c_atom.GetNeighbors() if nbr.GetAtomicNum() > 1 and nbr.GetIdx() != o_atom.GetIdx()]
            # In a primary carbon (CH2 or CH3) attached to a chain, typically only one heavy neighbor.
            if len(c_neighbors) == 1:
                terminal_OH_count += 1
    if terminal_OH_count < 1:
        return False, "No terminal (primary) free hydroxyl group found"
    if terminal_OH_count > 2:
        return False, f"Too many terminal free hydroxyl groups found ({terminal_OH_count}); expected 1 or 2"
    
    # Count total number of carbon atoms.
    carbon_atoms = [atom for atom in mol.GetAtoms() if atom.GetAtomicNum() == 6]
    carbon_count = len(carbon_atoms)
    if carbon_count < 5:
        return False, f"Too few carbons ({carbon_count}) to be a prenol"
    if carbon_count % 5 != 0:
        return False, f"Total carbon count ({carbon_count}) is not a multiple of 5; does not match isoprene repeats"
    
    expected_units = carbon_count // 5  # number of isoprene units expected
    
    # Define two SMARTS for an isoprene unit.
    # Pattern1: CH3-C(CH3)=CH-CH2 (chain starts with CH3)
    isoprene_pat1 = Chem.MolFromSmarts("[CH3]-[C]([CH3])=[CH]-[CH2]")
    # Pattern2: CH2-C(CH3)=CH-CH2 (chain starts with CH2)
    isoprene_pat2 = Chem.MolFromSmarts("[CH2]-[C]([CH3])=[CH]-[CH2]")
    
    matches1 = mol.GetSubstructMatches(isoprene_pat1)
    matches2 = mol.GetSubstructMatches(isoprene_pat2)
    
    # Combine the matches (each match is a tuple of atom indices corresponding to the pattern)
    all_matches = list(matches1) + list(matches2)
    if not all_matches:
        return False, "No isoprene unit substructure match found"
    
    # To avoid counting overlapping isoprene units, we determine the maximum set of non-overlapping matches.
    # We use a simple recursive selection algorithm.
    def max_nonoverlapping(matches, used=set(), start=0):
        best = 0
        for i in range(start, len(matches)):
            # if this match overlaps with already used atoms, skip it.
            if set(matches[i]) & used:
                continue
            new_used = used | set(matches[i])
            count = 1 + max_nonoverlapping(matches, new_used, i+1)
            if count > best:
                best = count
        return best
    total_isoprene = max_nonoverlapping(all_matches)
    
    if total_isoprene != expected_units:
        return False, (f"Unexpected number of isoprene units: found {total_isoprene} non-overlapping match(es) "
                       f"but expected {expected_units} (from {carbon_count} carbons)")
    
    return True, (f"Classified as prenol: contains {expected_units} isoprene unit(s), "
                  f"{len(free_alcohols)} free hydroxyl group(s) (with {terminal_OH_count} terminal), "
                  f"and {carbon_count} carbons.")

# Example usage (for testing):
if __name__ == "__main__":
    # Use one of the examples (prenol itself: CC(C)=CCO)
    test_smiles = "CC(C)=CCO"
    result, reason = is_prenols(test_smiles)
    print("Result:", result)
    print("Reason:", reason)


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:26244',
                          'name': 'prenols',
                          'definition': 'Any alcohol possessing the general '
                                        'formula H-[CH2C(Me)=CHCH2]nOH in '
                                        'which the carbon skeleton is composed '
                                        'of one or more isoprene units '
                                        '(biogenetic precursors of the '
                                        'isoprenoids).',
                          'parents': ['CHEBI:24913', 'CHEBI:30879'],
                          'xrefs': ['PMID:3113948', 'PMID:4207873'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 111,
                           'log_lines_of_code': 4.709530201312334,
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
                                                 2,
                                                 2,
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
                                                 2,
                                                 3,
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
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
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
                                                 3,
                                                 3,
                                                 3,
                                                 3,
                                                 4,
                                                 1,
                                                 2,
                                                 1,
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
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
                                                 1,
                                                 2,
                                                 2,
                                                 3,
                                                 3,
                                                 4,
                                                 3,
                                                 3,
                                                 3,
                                                 4,
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1],
                           'max_indent': 4,
                           'imports': ['from rdkit import Chem'],
                           'imports_count': 1,
                           'methods_called': [   'GetSymbol',
                                                 'GetIdx',
                                                 'NumRings',
                                                 'GetAtomicNum',
                                                 'MolFromSmiles',
                                                 'GetAtomWithIdx',
                                                 'GetAtoms',
                                                 'MolFromSmarts',
                                                 'GetNeighbors',
                                                 'add',
                                                 'GetRingInfo',
                                                 'GetSubstructMatches'],
                           'methods_called_count': 12,
                           'smarts_strings': [   'C(=O)[OX2H]',
                                                 '[OX2H]',
                                                 '[CH3]-[C]([CH3])=[CH]-[CH2]',
                                                 '[CH2]-[C]([CH3])=[CH]-[CH2]'],
                           'smarts_strings_count': 4,
                           'defs': [   'is_prenols(smiles: str):',
                                       'max_nonoverlapping(matches, '
                                       'used=set(), start=0):'],
                           'defs_count': 2,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "Molecule is cyclic, not a '
                                          'prenol"',
                                          'False, f"Molecule contains atom '
                                          '{atom.GetSymbol()} not in (C,O)"',
                                          'False, "No hydroxyl (alcohol) group '
                                          'found"',
                                          'False, "Only carboxylic acid '
                                          'hydroxyl(s) found; no free hydroxyl '
                                          'present"',
                                          'False, "No terminal (primary) free '
                                          'hydroxyl group found"',
                                          'False, f"Too many terminal free '
                                          'hydroxyl groups found '
                                          '({terminal_OH_count}); expected 1 '
                                          'or 2"',
                                          'False, f"Too few carbons '
                                          '({carbon_count}) to be a prenol"',
                                          'False, f"Total carbon count '
                                          '({carbon_count}) is not a multiple '
                                          'of 5; does not match isoprene '
                                          'repeats"',
                                          'False, "No isoprene unit '
                                          'substructure match found"',
                                          'best',
                                          'False, (f"Unexpected number of '
                                          'isoprene units: found '
                                          '{total_isoprene} non-overlapping '
                                          'match(es) "',
                                          'True, (f"Classified as prenol: '
                                          'contains {expected_units} isoprene '
                                          'unit(s), "'],
                           'returns_count': 13,
                           'complexity': 7.141906040262467},
    'message': '\n'
               'Attempt failed: F1 score of 0.4444444444444445 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: '
               'C(C\\C=C(\\CC\\C=C(\\CC\\C=C(\\CCC=C(C)C)/C)/C)/C)/C(=C\\CO)/C '
               'NAME: (2Z,6E,10E,14E)-geranylfarnesol REASON: CORRECT '
               'Classified as prenol: contains 5 isoprene unit(s), 1 free '
               'hydroxyl(s) and 25 carbons.\n'
               ' * SMILES: '
               'C(/C=C(\\CC/C=C(\\CC/C=C(\\CC/C=C(\\CC/C=C(\\CC/C=C(\\CC/C=C(\\CC/C=C(\\CC/C=C(/CC/C=C(/CCC=C(C)C)\\C)\\C)/C)/C)/C)/C)/C)/C)/C)/C)O '
               'NAME: ditrans,polycis-undecaprenol REASON: CORRECT Classified '
               'as prenol: contains 11 isoprene unit(s), 1 free hydroxyl(s) '
               'and 55 carbons.\n'
               ' * SMILES: '
               'CC(C)=CCC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CO '
               'NAME: solanesol REASON: CORRECT Classified as prenol: contains '
               '9 isoprene unit(s), 1 free hydroxyl(s) and 45 carbons.\n'
               ' * SMILES: C\\C(CO)=C/CC\\C(C)=C\\CC\\C(C)=C\\CO NAME: '
               '(2E,6E,10E)-omega-hydroxyfarnesol REASON: CORRECT Classified '
               'as prenol: contains 3 isoprene unit(s), 2 free hydroxyl(s) and '
               '15 carbons.\n'
               ' * SMILES: CC(C)=CCC\\C(C)=C\\CC\\C(C)=C/CO NAME: '
               '(2-cis,6-trans)-farnesol REASON: CORRECT Classified as prenol: '
               'contains 3 isoprene unit(s), 1 free hydroxyl(s) and 15 '
               'carbons.\n'
               ' * SMILES: '
               'C(/C=C(/CCC=C(C)C)\\C)C\\C(\\C)=C\\CC\\C(\\C)=C\\CC/C(/C)=C/CC\\C(=C\\CO)\\C '
               'NAME: all-trans-hexaprenol REASON: CORRECT Classified as '
               'prenol: contains 6 isoprene unit(s), 1 free hydroxyl(s) and 30 '
               'carbons.\n'
               ' * SMILES: CC(C)=CCC\\C(C)=C\\CO NAME: geraniol REASON: '
               'CORRECT Classified as prenol: contains 2 isoprene unit(s), 1 '
               'free hydroxyl(s) and 10 carbons.\n'
               ' * SMILES: CC(C)=CCC\\C(C)=C\\CC\\C(C)=C\\CO NAME: '
               '(2-trans,6-trans)-farnesol REASON: CORRECT Classified as '
               'prenol: contains 3 isoprene unit(s), 1 free hydroxyl(s) and 15 '
               'carbons.\n'
               ' * SMILES: CC(C)=CCC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CO NAME: '
               '(E,E,E)-geranylgeraniol REASON: CORRECT Classified as prenol: '
               'contains 4 isoprene unit(s), 1 free hydroxyl(s) and 20 '
               'carbons.\n'
               ' * SMILES: '
               'C(C\\C=C(\\CC\\C=C(\\CC\\C=C(\\CCC=C(C)C)/C)/C)/C)/C(=C/CO)/C '
               'NAME: (2E,6E,10E,14E)-geranylfarnesol REASON: CORRECT '
               'Classified as prenol: contains 5 isoprene unit(s), 1 free '
               'hydroxyl(s) and 25 carbons.\n'
               ' * SMILES: C\\C(CO)=C/CC\\C(C)=C\\CO NAME: '
               '(6E)-8-hydroxygeraniol REASON: CORRECT Classified as prenol: '
               'contains 2 isoprene unit(s), 2 free hydroxyl(s) and 10 '
               'carbons.\n'
               ' * SMILES: CC(C)=CCCC(C)=CCCC(C)=CCCC(C)=CCO NAME: '
               'geranylgeraniol REASON: CORRECT Classified as prenol: contains '
               '4 isoprene unit(s), 1 free hydroxyl(s) and 20 carbons.\n'
               ' * SMILES: '
               'C(/C=C(/CC\\C=C(\\CC/C=C(\\C)/CCC=C(C)C)/C)\\C)C\\C(\\C)=C\\CC\\C(\\C)=C\\CC/C(/C)=C/CC\\C(=C\\CO)\\C '
               'NAME: all-trans-octaprenol REASON: CORRECT Classified as '
               'prenol: contains 8 isoprene unit(s), 1 free hydroxyl(s) and 40 '
               'carbons.\n'
               ' * SMILES: '
               'CC(C)=CCC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CO '
               'NAME: all-trans-undecaprenol REASON: CORRECT Classified as '
               'prenol: contains 11 isoprene unit(s), 1 free hydroxyl(s) and '
               '55 carbons.\n'
               ' * SMILES: '
               'OC\\C=C(\\CC\\C=C(\\CC/C=C(\\CC/C=C(\\CC/C=C(\\CC\\C=C(\\CCCC(CCCC(CCCC(C)C)C)C)/C)/C)/C)/C)/C)/C '
               'NAME: '
               '(2E,6E,10Z,14Z,18Z,22E)-3,7,11,15,19,23,27,31,35-Nonamethylhexatriaconta-2,6,10,14,18,22-hexaen-1-ol '
               'REASON: CORRECT Classified as prenol: contains 6 isoprene '
               'unit(s), 1 free hydroxyl(s) and 45 carbons.\n'
               ' * SMILES: '
               'OCC[C@H](CC/C=C(\\CC/C=C(\\CC/C=C(\\CC/C=C(\\CC/C=C(\\CC/C=C(\\CC/C=C(\\CC/C=C(\\CC/C=C(\\CC/C=C(\\CC/C=C(\\CC/C=C(\\CC/C=C(\\CC/C=C(\\CC\\C=C(\\CC/C=C(/CCC=C(C)C)\\C)/C)/C)/C)/C)/C)/C)/C)/C)/C)/C)/C)/C)/C)/C)/C)C '
               'NAME: Dolichol-18 REASON: CORRECT Classified as prenol: '
               'contains 17 isoprene unit(s), 1 free hydroxyl(s) and 90 '
               'carbons.\n'
               ' * SMILES: '
               'OCC[C@H](CC/C=C(\\CC/C=C(\\CC/C=C(\\CC/C=C(\\CC/C=C(\\CC/C=C(\\CC/C=C(\\CC/C=C(\\CC/C=C(\\CC/C=C(\\CC/C=C(\\CC/C=C(\\CC/C=C(\\CC/C=C(\\CC/C=C(\\CC\\C=C(\\CC/C=C(/CCC=C(C)C)\\C)/C)/C)/C)/C)/C)/C)/C)/C)/C)/C)/C)/C)/C)/C)/C)/C)C '
               'NAME: Dolichol-19 REASON: CORRECT Classified as prenol: '
               'contains 18 isoprene unit(s), 1 free hydroxyl(s) and 95 '
               'carbons.\n'
               ' * SMILES: C(=C\\CO)(\\CCC=C(C)C)/C NAME: nerol REASON: '
               'CORRECT Classified as prenol: contains 2 isoprene unit(s), 1 '
               'free hydroxyl(s) and 10 carbons.\n'
               ' * SMILES: CC(C)=CCC\\C(C)=C/CC\\C(C)=C\\CO NAME: '
               '(2-trans,6-cis)-farnesol REASON: CORRECT Classified as prenol: '
               'contains 3 isoprene unit(s), 1 free hydroxyl(s) and 15 '
               'carbons.\n'
               ' * SMILES: CC(C)=CCO NAME: prenol REASON: CORRECT Classified '
               'as prenol: contains 1 isoprene unit(s), 1 free hydroxyl(s) and '
               '5 carbons.\n'
               ' * SMILES: [H]C(CO)=C(C)CCC([H])=C(C)CCC=C(C)C NAME: farnesol '
               'REASON: CORRECT Classified as prenol: contains 3 isoprene '
               'unit(s), 1 free hydroxyl(s) and 15 carbons.\n'
               ' * SMILES: CC(C)=CCC\\C(C)=C/CC\\C(C)=C/CO NAME: '
               '(2-cis,6-cis)-farnesol REASON: CORRECT Classified as prenol: '
               'contains 3 isoprene unit(s), 1 free hydroxyl(s) and 15 '
               'carbons.\n'
               'False positives: SMILES: '
               'CC(C)=CCC\\C(C)=C\\CC\\C(CO)=C\\CC\\C(C)=C\\CO NAME: plaunotol '
               'REASON: WRONGLY CLASSIFIED Classified as prenol: contains 3 '
               'isoprene unit(s), 2 free hydroxyl(s) and 20 carbons.\n'
               ' * SMILES: OCC/C=C(/CC/C=C(/CCCO)\\C)\\C NAME: '
               '(3E,7E)-4,8-dimethyl-undecane-3,7-diene-1,11-diol REASON: '
               'WRONGLY CLASSIFIED Classified as prenol: contains 2 isoprene '
               'unit(s), 2 free hydroxyl(s) and 13 carbons.\n'
               ' * SMILES: '
               'O[C@](/C=C/C/C(=C/CC/C(=C/CO)/C)/C)(CC/C=C(/CO)\\C)C NAME: '
               'Boletinin A REASON: WRONGLY CLASSIFIED Classified as prenol: '
               'contains 3 isoprene unit(s), 3 free hydroxyl(s) and 20 '
               'carbons.\n'
               ' * SMILES: '
               'O(C\\C=C(\\CC\\C=C(\\CC\\C=C(\\CC/C=C(/CO)\\C)/C)/C)/C)C(=O)/C(/C)=C/C(O)=O '
               'NAME: Cavipetin D REASON: WRONGLY CLASSIFIED Classified as '
               'prenol: contains 4 isoprene unit(s), 1 free hydroxyl(s) and 25 '
               'carbons.\n'
               ' * SMILES: CC(C)=CCC\\C(C)=C/CCC(C)(O)C=C NAME: (6Z)-nerolidol '
               'REASON: WRONGLY CLASSIFIED Classified as prenol: contains 2 '
               'isoprene unit(s), 1 free hydroxyl(s) and 15 carbons.\n'
               ' * SMILES: CC(C)=CCC\\C(C)=C\\CC[C@](C)(O)C=C NAME: '
               '(3S,6E)-nerolidol REASON: WRONGLY CLASSIFIED Classified as '
               'prenol: contains 2 isoprene unit(s), 1 free hydroxyl(s) and 15 '
               'carbons.\n'
               ' * SMILES: O[C@H](C(=C)CC/C=C(/CO)\\C)CC/C(=C/CC/C(=C/CO)/C)/C '
               'NAME: Boletinin C REASON: WRONGLY CLASSIFIED Classified as '
               'prenol: contains 3 isoprene unit(s), 3 free hydroxyl(s) and 20 '
               'carbons.\n'
               ' * SMILES: '
               'C\\C(CC\\C=C(/C)CCC=C(CO)CO)=C/CC\\C=C(/C)CC\\C=C(/C)CCC=C(CO)CO '
               'NAME: tetrahydroxysqualene REASON: WRONGLY CLASSIFIED '
               'Classified as prenol: contains 4 isoprene unit(s), 4 free '
               'hydroxyl(s) and 30 carbons.\n'
               ' * SMILES: CC(C)=CC/C=C(\\C)/CCO NAME: trans-isogeraniol '
               'REASON: WRONGLY CLASSIFIED Classified as prenol: contains 2 '
               'isoprene unit(s), 1 free hydroxyl(s) and 10 carbons.\n'
               ' * SMILES: '
               'O=C(OC/C(=C/CC/C(=C/CC/C(=C/CC/C(=C/CO)/C)/C)/C)/C)/C=C/C(=O)O '
               'NAME: Boletinin E REASON: WRONGLY CLASSIFIED Classified as '
               'prenol: contains 4 isoprene unit(s), 1 free hydroxyl(s) and 24 '
               'carbons.\n'
               ' * SMILES: CC(C)=CC/C=C(/C)\\CCO NAME: cis-isogeraniol REASON: '
               'WRONGLY CLASSIFIED Classified as prenol: contains 2 isoprene '
               'unit(s), 1 free hydroxyl(s) and 10 carbons.\n'
               ' * SMILES: [H]C(CCC(C)(O)C=C)=C(C)CCC=C(C)C NAME: nerolidol '
               'REASON: WRONGLY CLASSIFIED Classified as prenol: contains 2 '
               'isoprene unit(s), 1 free hydroxyl(s) and 15 carbons.\n'
               ' * SMILES: OC(CC/C=C(\\CC/C=C(\\CCC=C(C)C)/C)/C)(C)C=C NAME: '
               '(3S,6E,10E)-1,6,10,14-Phytatetraen-3-ol REASON: WRONGLY '
               'CLASSIFIED Classified as prenol: contains 3 isoprene unit(s), '
               '1 free hydroxyl(s) and 20 carbons.\n'
               ' * SMILES: O[C@@H](CCC=C(C)C)C NAME: R-sulcatol REASON: '
               'WRONGLY CLASSIFIED Classified as prenol: contains 1 isoprene '
               'unit(s), 1 free hydroxyl(s) and 8 carbons.\n'
               ' * SMILES: O[C@H](C(=C)CO)CC/C(=C/CC/C(=C/CC/C(=C/CO)/C)/C)/C '
               'NAME: Boletinin D REASON: WRONGLY CLASSIFIED Classified as '
               'prenol: contains 3 isoprene unit(s), 3 free hydroxyl(s) and 20 '
               'carbons.\n'
               ' * SMILES: '
               'O(C\\C=C(\\CC\\C=C(\\CC\\C=C(\\CC/C=C(\\C)/C=O)/C)/C)/C)C(=O)/C(/C)=C/O '
               'NAME: Cavipetin C REASON: WRONGLY CLASSIFIED Classified as '
               'prenol: contains 3 isoprene unit(s), 1 free hydroxyl(s) and 24 '
               'carbons.\n'
               ' * SMILES: OC(=O)/C(/CCC=C(C)C)=C\\CC/C(=C/CC/C(/C)=C/CO)/C '
               'NAME: Isonerylgeraniol-18-oic acid REASON: WRONGLY CLASSIFIED '
               'Classified as prenol: contains 3 isoprene unit(s), 1 free '
               'hydroxyl(s) and 20 carbons.\n'
               ' * SMILES: '
               'O([C@@H](COC/C=C(/CC/C=C(/CC/C=C(/CCCC(C)C)\\C)\\C)\\C)CO)C/C=C(/CC/C=C(/CC/C=C(/CCCC(C)C)\\C)\\C)\\C '
               'NAME: 2,3-di-O-dihydro-14,15-geranylgeranyl glycerol REASON: '
               'WRONGLY CLASSIFIED Classified as prenol: contains 6 isoprene '
               'unit(s), 1 free hydroxyl(s) and 43 carbons.\n'
               ' * SMILES: S(OCC=C(C)C)(O)(=O)=O NAME: '
               '[(3-methylbut-2-en-1-yl)oxy]sulfonic acid REASON: WRONGLY '
               'CLASSIFIED Classified as prenol: contains 1 isoprene unit(s), '
               '1 free hydroxyl(s) and 5 carbons.\n'
               ' * SMILES: '
               'C(/C=C(/CC/C=C(/CCC=C(C)C)\\C)\\C)[C@H](/C=C(/CC/C=C(/CCC=C(C)C)\\C)\\C)O '
               'NAME: (R)-12-hydroxysqualene REASON: WRONGLY CLASSIFIED '
               'Classified as prenol: contains 5 isoprene unit(s), 1 free '
               'hydroxyl(s) and 30 carbons.\n'
               ' * SMILES: O=C(C/C(=C/CC/C(/C)=C/CO)/C)C=C(C)C NAME: '
               '(2E,6E)-1-Hydroxy-2,6,10-farnesatrien-9-one REASON: WRONGLY '
               'CLASSIFIED Classified as prenol: contains 2 isoprene unit(s), '
               '1 free hydroxyl(s) and 15 carbons.\n'
               ' * SMILES: O[C@H](CCC=C(C)C)C NAME: S-sulcatol REASON: WRONGLY '
               'CLASSIFIED Classified as prenol: contains 1 isoprene unit(s), '
               '1 free hydroxyl(s) and 8 carbons.\n'
               ' * SMILES: '
               'O=C([O-])[C@@H]([NH2+]C/C=C(/CC/C=C(/CO)\\C)\\C)CCC(=O)[O-] '
               "NAME: N-(8'-hydroxygeranyl)-L-glutamate(1-) REASON: WRONGLY "
               'CLASSIFIED Classified as prenol: contains 2 isoprene unit(s), '
               '1 free hydroxyl(s) and 15 carbons.\n'
               ' * SMILES: CC(C)=CCC\\C(C)=C\\CC\\C(C)=C\\CCC(C)(O)C=C NAME: '
               'geranyllinalool REASON: WRONGLY CLASSIFIED Classified as '
               'prenol: contains 3 isoprene unit(s), 1 free hydroxyl(s) and 20 '
               'carbons.\n'
               ' * SMILES: '
               'O=C(O)[C@H](OC/C=C(/CC/C=C(/CC/C=C(/CC/C=C(/CO)\\C)\\C)\\C)\\C)[C@@H](C(=O)O)CC(=O)O '
               'NAME: Microporenic acid D REASON: WRONGLY CLASSIFIED '
               'Classified as prenol: contains 4 isoprene unit(s), 1 free '
               'hydroxyl(s) and 26 carbons.\n'
               'False negatives: SMILES: '
               'OC(CCC(O)C(O)(C)C)(CCCC(O)(CCCC(O)(CCCC(O)(CCCC(O)(CCC/C(=C/CC/C(=C/CC/C(=C/CO)/C)/C)/C)C)C)C)C)C '
               'NAME: Glisoprenin F REASON: MISSED Unexpected high number of '
               'carbons (45) relative to detected isoprene unit(s) (3)\n'
               ' * SMILES: '
               'OC(CCC=C(C)C)(CCCC(O)(CCCC(O)(CCCC(O)(CCCC(O)(CCCC(O)(CCCC(O)(CCC/C(=C/CC/C(=C/CO)/C)/C)C)C)C)C)C)C)C '
               'NAME: Bionectin F REASON: MISSED Unexpected high number of '
               'carbons (50) relative to detected isoprene unit(s) (3)\n'
               ' * SMILES: '
               'OC(C(O)CC/C(=C/CC/C(=C/CC/C(=C/CO)/C)/C)/C)(CCCC(O)(CCCC(O)(CCCC(O)(CCCC(O)(CCCC(O)(CCCC(O)(CCCC(O)(CCCC(O)(CCCC(O)(CCCC(O)(CCC=C(C)C)C)C)C)C)C)C)C)C)C)C)C '
               'NAME: SCH 66878 REASON: MISSED Unexpected high number of '
               'carbons (75) relative to detected isoprene unit(s) (4)\n'
               ' * SMILES: '
               'CC(C)=CCC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C/CC\\C(C)=C/CC\\C(C)=C/CC\\C(C)=C/CC\\C(C)=C/CC\\C(C)=C/CC\\C(C)=C/CC\\C(C)=C/COP([O-])(=O)OP([O-])([O-])=O '
               'NAME: ditrans,polycis-undecaprenyl diphosphate(3-) REASON: '
               'MISSED Molecule contains phosphorus, not a prenol\n'
               ' * SMILES: C\\C(CO)=C/CC\\C(C)=C\\C=O NAME: '
               '(6E)-8-hydroxygeranial REASON: MISSED Unexpected high number '
               'of carbons (10) relative to detected isoprene unit(s) (1)\n'
               ' * SMILES: '
               'O1C(CCC1C(O)(C)C)(CCCC(O)(CCCC(O)(CCCC(O)(CCC/C(=C/CC/C(=C/CC/C(=C/CC/C(=C/CO)/C)/C)/C)/C)C)C)C)C '
               'NAME: Glisoprenin B REASON: MISSED Molecule is cyclic, not a '
               'prenol\n'
               ' * SMILES: '
               'CC(C)=CCC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\COP([O-])(=O)OP([O-])([O-])=O '
               'NAME: all-trans-decaprenyl diphosphate(3-) REASON: MISSED '
               'Molecule contains phosphorus, not a prenol\n'
               ' * SMILES: '
               'OC(CCC=C(C)C)(CCCC(O)(CCCC(O)(CCCC(O)(CCCC(O)(CCC/C(=C/CC/C(=C/CC/C(=C/CO)/C)/C)/C)C)C)C)C)C '
               'NAME: SCH 60057 REASON: MISSED Unexpected high number of '
               'carbons (45) relative to detected isoprene unit(s) (4)\n'
               ' * SMILES: '
               'OC(CCC=C(C)C)(CCCC(O)(CCCC(O)(CCCC(O)(CCCC(=CCCC(=CCCC(=CCCC(=CCO)C)C)C)C)C)C)C)C '
               'NAME: Glisoprenin A REASON: MISSED Unexpected high number of '
               'carbons (45) relative to detected isoprene unit(s) (5)\n'
               ' * SMILES: '
               'OC(C(O)CC/C(=C/CO)/C)(CC/C=C(/CC/C=C(/CCCC(O)(CCCC(O)(CCCC(O)(CCCC(O)(CCC(O)C(O)(C)C)C)C)C)C)\\C)\\C)C '
               'NAME: Glisoprenin E REASON: MISSED Unexpected high number of '
               'carbons (45) relative to detected isoprene unit(s) (3)\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'O=C(N[C@@H](C(O)(C)C)C)[C@H]([C@@]1([C@@]2([C@@](CC1)(/C(/CCC2)=C/C=C\\3/C[C@@H](O)C[C@H](O)C3=C)[H])C)[H])C',
                                     'name': '1alpha,25-dihydroxy-24-oxo-23-azavitamin '
                                             'D2 / '
                                             '1alpha,25-dihydroxy-24-oxo-23-azaergocalciferol',
                                     'reason': 'Molecule is cyclic, not a '
                                               'prenol'},
                                 {   'smiles': 'CCCCCCCCCCCCCCCCCCC(O)C([O-])=O',
                                     'name': '2-hydroxyarachidate',
                                     'reason': 'No terminal (primary) free '
                                               'hydroxyl group found'},
                                 {   'smiles': 'C[C@@H](CN([C@@H](C)CO)C(=O)NC1=CC=C(C=C1)C(F)(F)F)[C@@H](CN(C)C(=O)C2CCOCC2)OC',
                                     'name': 'N-[(2S,3S)-4-[[(2S)-1-hydroxypropan-2-yl]-[[4-(trifluoromethyl)phenyl]carbamoyl]amino]-2-methoxy-3-methylbutyl]-N-methyloxane-4-carboxamide',
                                     'reason': 'Molecule is cyclic, not a '
                                               'prenol'},
                                 {   'smiles': 'CC(=O)CC\\C=C(/C)CCC=C(C)C',
                                     'name': 'geranyl acetone',
                                     'reason': 'No hydroxyl (alcohol) group '
                                               'found'},
                                 {   'smiles': 'O([C@H]1[C@H](O)[C@H](O[C@H](O)[C@H]1O)CO[C@H]2O[C@@H]([C@@H](O)[C@H](O)[C@@H]2O)CO)[C@H]3O[C@@H]([C@@H](O)[C@H](O)[C@@H]3O[C@H]4O[C@@H]([C@@H](O)[C@H](O)[C@@H]4O)CO)CO',
                                     'name': '(2S,3S,4S,5S,6R)-2-[[(2R,3R,4S,5S,6S)-4-[(2R,3S,4S,5S,6R)-4,5-Dihydroxy-6-(hydroxymethyl)-3-[(2R,3S,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-3,5,6-trihydroxyoxan-2-yl]methoxy]-6-(hydroxymethyl)oxane-3,4,5-triol',
                                     'reason': 'Molecule is cyclic, not a '
                                               'prenol'},
                                 {   'smiles': 'O=C(OC1=C(C(O)=C(C(=O)O)C(=C1C)C)C)C2=C(OC)C(=C(OC(=O)C3=C(O)C=C(O)C=C3C)C=C2C)C',
                                     'name': 'Thielavin Z5',
                                     'reason': 'Molecule is cyclic, not a '
                                               'prenol'},
                                 {   'smiles': '[C@@H]1([C@@H]([C@H]([C@@H]([C@H](O1)CO)O)O)NC(C)=O)O[C@@H]2[C@@H]([C@H](C(O[C@@H]2CO)O)O)O',
                                     'name': 'beta-D-GlcpNAc-(1->4)-D-Galp',
                                     'reason': 'Molecule is cyclic, not a '
                                               'prenol'},
                                 {   'smiles': 'CN(C)C(=O)C1=CC=C(C=C1)C2=CC=C(C=C2)[C@@H]3[C@H]4CN(CC(=O)N4[C@H]3CO)C(=O)CC5CC5',
                                     'name': '4-[4-[(6S,7R,8R)-4-(2-cyclopropyl-1-oxoethyl)-8-(hydroxymethyl)-2-oxo-1,4-diazabicyclo[4.2.0]octan-7-yl]phenyl]-N,N-dimethylbenzamide',
                                     'reason': 'Molecule is cyclic, not a '
                                               'prenol'},
                                 {   'smiles': 'CCCCCCCCCCCCCCCCCCCCC=C',
                                     'name': '1-docosene',
                                     'reason': 'No hydroxyl (alcohol) group '
                                               'found'},
                                 {   'smiles': 'C([C@@](OC(=O)CCC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)([H])COC(=O)CC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)OC(=O)CCCCC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC',
                                     'name': 'TG(22:5(7Z,10Z,13Z,16Z,19Z)/20:5(5Z,8Z,11Z,14Z,17Z)/22:6(4Z,7Z,10Z,13Z,16Z,19Z))[iso6]',
                                     'reason': 'No hydroxyl (alcohol) group '
                                               'found'}],
    'sample_false_negatives': [   {   'smiles': 'OC(CCC(O)C(O)(C)C)(CCCC(O)(CCCC(O)(CCCC(O)(CCCC(O)(CCC/C(=C/CC/C(=C/CC/C(=C/CO)/C)/C)/C)C)C)C)C)C',
                                      'name': 'Glisoprenin F',
                                      'reason': 'Unexpected number of isoprene '
                                                'units: found 3 '
                                                'non-overlapping match(es) but '
                                                'expected 9 (from 45 carbons)'},
                                  {   'smiles': 'OC(CCC=C(C)C)(CCCC(O)(CCCC(O)(CCCC(O)(CCCC(O)(CCCC(O)(CCCC(O)(CCC/C(=C/CC/C(=C/CO)/C)/C)C)C)C)C)C)C)C',
                                      'name': 'Bionectin F',
                                      'reason': 'Unexpected number of isoprene '
                                                'units: found 3 '
                                                'non-overlapping match(es) but '
                                                'expected 10 (from 50 '
                                                'carbons)'},
                                  {   'smiles': 'OC(C(O)CC/C(=C/CC/C(=C/CC/C(=C/CO)/C)/C)/C)(CCCC(O)(CCCC(O)(CCCC(O)(CCCC(O)(CCCC(O)(CCCC(O)(CCCC(O)(CCCC(O)(CCCC(O)(CCCC(O)(CCC=C(C)C)C)C)C)C)C)C)C)C)C)C)C',
                                      'name': 'SCH 66878',
                                      'reason': 'Unexpected number of isoprene '
                                                'units: found 4 '
                                                'non-overlapping match(es) but '
                                                'expected 15 (from 75 '
                                                'carbons)'},
                                  {   'smiles': 'CC(C)=CCC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C/CC\\C(C)=C/CC\\C(C)=C/CC\\C(C)=C/CC\\C(C)=C/CC\\C(C)=C/CC\\C(C)=C/CC\\C(C)=C/COP([O-])(=O)OP([O-])([O-])=O',
                                      'name': 'ditrans,polycis-undecaprenyl '
                                              'diphosphate(3-)',
                                      'reason': 'Molecule contains atom P not '
                                                'in (C,O)'},
                                  {   'smiles': 'C\\C(CO)=C/CC\\C(C)=C\\C=O',
                                      'name': '(6E)-8-hydroxygeranial',
                                      'reason': 'Unexpected number of isoprene '
                                                'units: found 1 '
                                                'non-overlapping match(es) but '
                                                'expected 2 (from 10 carbons)'},
                                  {   'smiles': 'O1C(CCC1C(O)(C)C)(CCCC(O)(CCCC(O)(CCCC(O)(CCC/C(=C/CC/C(=C/CC/C(=C/CC/C(=C/CO)/C)/C)/C)/C)C)C)C)C',
                                      'name': 'Glisoprenin B',
                                      'reason': 'Molecule is cyclic, not a '
                                                'prenol'},
                                  {   'smiles': 'CC(C)=CCC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\COP([O-])(=O)OP([O-])([O-])=O',
                                      'name': 'all-trans-decaprenyl '
                                              'diphosphate(3-)',
                                      'reason': 'Molecule contains atom P not '
                                                'in (C,O)'},
                                  {   'smiles': 'OC(CCC=C(C)C)(CCCC(O)(CCCC(O)(CCCC(O)(CCCC(O)(CCC/C(=C/CC/C(=C/CC/C(=C/CO)/C)/C)/C)C)C)C)C)C',
                                      'name': 'SCH 60057',
                                      'reason': 'Unexpected number of isoprene '
                                                'units: found 4 '
                                                'non-overlapping match(es) but '
                                                'expected 9 (from 45 carbons)'},
                                  {   'smiles': 'OC(CCC=C(C)C)(CCCC(O)(CCCC(O)(CCCC(O)(CCCC(=CCCC(=CCCC(=CCCC(=CCO)C)C)C)C)C)C)C)C',
                                      'name': 'Glisoprenin A',
                                      'reason': 'Unexpected number of isoprene '
                                                'units: found 5 '
                                                'non-overlapping match(es) but '
                                                'expected 9 (from 45 carbons)'},
                                  {   'smiles': 'OC\\C=C(\\CC\\C=C(\\CC/C=C(\\CC/C=C(\\CC/C=C(\\CC\\C=C(\\CCCC(CCCC(CCCC(C)C)C)C)/C)/C)/C)/C)/C)/C',
                                      'name': '(2E,6E,10Z,14Z,18Z,22E)-3,7,11,15,19,23,27,31,35-Nonamethylhexatriaconta-2,6,10,14,18,22-hexaen-1-ol',
                                      'reason': 'Unexpected number of isoprene '
                                                'units: found 6 '
                                                'non-overlapping match(es) but '
                                                'expected 9 (from 45 '
                                                'carbons)'}],
    'attempt': 3,
    'reasoning': 'We can try to “force‐fit” the chemistry definition by first '
                 'enforcing that (a) the only heavy elements present are '
                 'carbon and oxygen, (b) the molecule is acyclic and bears one '
                 'or two “free” (terminal) –OH(s), and (c) its carbon skeleton '
                 'exactly “fits” the isoprene‐rule (that is, its total number '
                 'of carbon atoms is exactly 5·n, and we can “cover” the '
                 'molecule with n nonoverlapping isoprene units). (Remember '
                 'that an isoprene unit is defined as CH2–C(CH3)=CH–CH2.) In '
                 'the code below we (1) parse the molecule and reject ones '
                 'with rings or alien atoms, (2) require that at least one '
                 'free hydroxyl (not in a carboxyl) be attached to a primary '
                 'carbon, (3) count the total number of carbon atoms and '
                 'require that it be a multiple of 5, (4) use two SMARTS '
                 'patterns (which are allowed to overlap) to get all '
                 'substructure matches for an isoprene unit and then extract a '
                 'maximum set of non‐overlapping matches; the “expected” '
                 'number of isoprene repeats is the total number of carbons '
                 'divided by 5. (If they match, we “score” the molecule as a '
                 'prenol.) Note that this is a heuristic—and our comments (and '
                 'previous outcomes) show that even “real‐world” prenols can '
                 'be tricky—but the improvements below are designed to avoid '
                 'the previous mis–classifications.\n'
                 '\n'
                 'Below is the complete (single) Python code block.\n'
                 '\n'
                 '------------------------------------------------',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 19,
    'num_false_positives': 2,
    'num_true_negatives': 142262,
    'num_false_negatives': 17,
    'num_negatives': None,
    'precision': 0.9047619047619048,
    'recall': 0.5277777777777778,
    'f1': 0.6666666666666666,
    'accuracy': 0.9998664792691497,
    'negative_predictive_value': 0.9998805164500735}