"""
Classifies: CHEBI:35757 monocarboxylic acid anion
"""
#!/usr/bin/env python3
"""
Classifies: Monocarboxylic acid anion
Definition: A carboxylic acid anion formed when the carboxyl group of a monocarboxylic acid is deprotonated.
That is, the molecule should have exactly one deprotonated carboxyl (CO2–) group with the proper connectivity,
an overall formal charge of -1, and no other atoms in the molecule should be charged.
Extra connectivity checks are performed to ensure that the carboxylate carbon is attached to exactly two oxygen atoms
(with one oxygen double‐bonded and neutral, and one single‐bonded bearing the -1 charge) and one R‐group.
"""

from rdkit import Chem

def is_monocarboxylic_acid_anion(smiles: str):
    """
    Determines if a molecule is a monocarboxylic acid anion based on its SMILES string.
    
    Criteria:
      1. The SMILES must parse.
      2. It must contain exactly one deprotonated carboxylate group. We locate that group via the SMARTS:
           "[#6X3](=O)[O-]"
         which requires that the carboxyl carbon (#6) is trigonal (X3), has a double bond to one oxygen,
         and a single bond to an oxygen carrying a -1 charge.
      3. The overall formal charge of the molecule must be -1.
      4. No atom outside the matched carboxylate group may carry a nonzero formal charge.
      5. Extra connectivity is checked: the carboxyl carbon should have exactly 3 neighbors,
         exactly two of which are oxygens. Furthermore, one of these oxygens should be connected via a double bond
         (carbonyl oxygen, formal charge 0) and the other via a single bond (deprotonated oxygen, formal charge -1).
    
    Args:
        smiles (str): SMILES string of the molecule.

    Returns:
        (bool, str): Tuple where the boolean indicates if the molecule is classified as a monocarboxylic acid anion,
                     and the string provides an explanation.
    """
    # Parse the SMILES string.
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Define the SMARTS pattern for a deprotonated carboxylate group.
    carboxylate_smarts = "[#6X3](=O)[O-]"
    carboxylate_pattern = Chem.MolFromSmarts(carboxylate_smarts)
    if carboxylate_pattern is None:
        return False, "Error creating SMARTS for carboxylate group"

    # Find all matches for the carboxylate pattern.
    matches = mol.GetSubstructMatches(carboxylate_pattern)
    if len(matches) == 0:
        return False, "No deprotonated carboxyl (carboxylate) group found"
    if len(matches) > 1:
        return False, f"Found {len(matches)} carboxylate groups; molecule is not a monocarboxylic acid anion"

    # Check overall formal charge.
    total_charge = sum(atom.GetFormalCharge() for atom in mol.GetAtoms())
    if total_charge != -1:
        return False, f"Expected overall charge of -1 for a monocarboxylate anion, found charge = {total_charge}"

    # Identify the atoms involved in the carboxylate group.
    # We expect the SMARTS match to return a tuple: (carboxyl carbon, carbonyl oxygen, deprotonated oxygen)
    match = matches[0]
    if len(match) != 3:
        return False, "Unexpected match size for carboxylate group; expected 3 atoms"
    carboxyl_idx, oxy1_idx, oxy2_idx = match
    carboxyl_atom = mol.GetAtomWithIdx(carboxyl_idx)
    oxy1_atom = mol.GetAtomWithIdx(oxy1_idx)
    oxy2_atom = mol.GetAtomWithIdx(oxy2_idx)

    # Extra connectivity check: carboxyl carbon should have exactly 3 neighbors.
    if carboxyl_atom.GetDegree() != 3:
        return False, (f"Carboxyl carbon (atom idx {carboxyl_idx}) does not have 3 neighbors; "
                       "unexpected connectivity for a simple acid group")
    
    # Among its neighbors, exactly two must be oxygens.
    o_neighbors = [nbr for nbr in carboxyl_atom.GetNeighbors() if nbr.GetAtomicNum() == 8]
    if len(o_neighbors) != 2:
        return False, "The carboxyl carbon does not have exactly 2 oxygen neighbors"
    
    # Check bond types to the oxygen neighbors:
    # One oxygen should be connected via a double bond (the carbonyl oxygen, expected to have formal charge 0)
    # and the other via a single bond (the deprotonated oxygen, expected to have formal charge -1).
    bond1 = mol.GetBondBetweenAtoms(carboxyl_idx, oxy1_idx)
    bond2 = mol.GetBondBetweenAtoms(carboxyl_idx, oxy2_idx)
    if bond1 is None or bond2 is None:
        return False, "Bond information missing for carboxylate group"

    # Identify the double vs single bond.
    # RDKit represents bond types as Chem.BondType.DOUBLE and .SINGLE.
    if bond1.GetBondType() == Chem.BondType.DOUBLE and bond2.GetBondType() == Chem.BondType.SINGLE:
        carbonyl_oxygen = oxy1_atom
        deprot_oxygen = oxy2_atom
    elif bond2.GetBondType() == Chem.BondType.DOUBLE and bond1.GetBondType() == Chem.BondType.SINGLE:
        carbonyl_oxygen = oxy2_atom
        deprot_oxygen = oxy1_atom
    else:
        return False, "The bonds from carboxyl carbon to oxygen atoms do not display the expected single/double pattern"

    # Check the formal charges on the oxygens: carbonyl oxygen should be neutral (0) and the deprotonated oxygen -1.
    if carbonyl_oxygen.GetFormalCharge() != 0:
        return False, "Carbonyl oxygen has an unexpected formal charge (expected 0)"
    if deprot_oxygen.GetFormalCharge() != -1:
        return False, "Deprotonated oxygen does not have a formal charge of -1"

    # Now check that no other atoms (outside the carboxylate group) carry a nonzero formal charge.
    carboxylate_atom_ids = set(match)
    for atom in mol.GetAtoms():
        if atom.GetFormalCharge() != 0 and atom.GetIdx() not in carboxylate_atom_ids:
            return False, ("Additional charged atoms found outside the deprotonated carboxyl group, "
                           "indicating presence of other ionizable groups")
    
    # Passed all tests.
    return True, ("The molecule contains exactly one deprotonated carboxyl group (with proper connectivity), "
                  "an overall charge of -1, and no other charged atoms, consistent with a monocarboxylic acid anion")


# Example usage (can be removed if used as a module)
if __name__ == "__main__":
    # Example: xanthine-8-carboxylate should be classified as a monocarboxylic acid anion.
    test_smiles = "[O-]C(=O)c1nc2[nH]c(=O)[nH]c(=O)c2[nH]1"
    result, reason = is_monocarboxylic_acid_anion(test_smiles)
    print(result, reason)


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:35757',
                          'name': 'monocarboxylic acid anion',
                          'definition': 'A carboxylic acid anion formed when '
                                        'the carboxy group of a monocarboxylic '
                                        'acid is deprotonated.',
                          'parents': ['CHEBI:29067'],
                          'xrefs': ['KEGG:C00060'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 90,
                           'log_lines_of_code': 4.499809670330265,
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
                                                 2,
                                                 0,
                                                 1,
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
                                                 1,
                                                 2,
                                                 0,
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
                                                 2,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 0,
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
                                                 1,
                                                 1,
                                                 2,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 1,
                                                 2,
                                                 2,
                                                 1,
                                                 2,
                                                 0,
                                                 1,
                                                 1,
                                                 2,
                                                 1,
                                                 2,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 3,
                                                 3,
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
                           'max_indent': 3,
                           'imports': ['from rdkit import Chem'],
                           'imports_count': 1,
                           'methods_called': [   'GetFormalCharge',
                                                 'GetIdx',
                                                 'GetAtomicNum',
                                                 'MolFromSmiles',
                                                 'GetAtomWithIdx',
                                                 'GetAtoms',
                                                 'MolFromSmarts',
                                                 'GetDegree',
                                                 'GetNeighbors',
                                                 'GetBondBetweenAtoms',
                                                 'GetBondType',
                                                 'GetSubstructMatches'],
                           'methods_called_count': 12,
                           'smarts_strings': ['carboxylate_smarts'],
                           'smarts_strings_count': 1,
                           'defs': [   'is_monocarboxylic_acid_anion(smiles: '
                                       'str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "Error creating SMARTS for '
                                          'carboxylate group"',
                                          'False, "No deprotonated carboxyl '
                                          '(carboxylate) group found"',
                                          'False, f"Found {len(matches)} '
                                          'carboxylate groups; molecule is not '
                                          'a monocarboxylic acid anion"',
                                          'False, f"Expected overall charge of '
                                          '-1 for a monocarboxylate anion, '
                                          'found charge = {total_charge}"',
                                          'False, "Unexpected match size for '
                                          'carboxylate group; expected 3 '
                                          'atoms"',
                                          'False, (f"Carboxyl carbon (atom idx '
                                          '{carboxyl_idx}) does not have 3 '
                                          'neighbors; "',
                                          'False, "The carboxyl carbon does '
                                          'not have exactly 2 oxygen '
                                          'neighbors"',
                                          'False, "Bond information missing '
                                          'for carboxylate group"',
                                          'False, "The bonds from carboxyl '
                                          'carbon to oxygen atoms do not '
                                          'display the expected single/double '
                                          'pattern"',
                                          'False, "Carbonyl oxygen has an '
                                          'unexpected formal charge (expected '
                                          '0)"',
                                          'False, "Deprotonated oxygen does '
                                          'not have a formal charge of -1"',
                                          'False, ("Additional charged atoms '
                                          'found outside the deprotonated '
                                          'carboxyl group, "',
                                          'True, ("The molecule contains '
                                          'exactly one deprotonated carboxyl '
                                          'group (with proper connectivity), '
                                          '"'],
                           'returns_count': 14,
                           'complexity': 6.899961934066053},
    'message': '\n'
               'Attempt failed: F1 score of 0.8044141817328011 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: '
               '[O-]C(=O)c1nc2[nH]c(=O)[nH]c(=O)c2[nH]1 NAME: '
               'xanthine-8-carboxylate REASON: CORRECT The molecule contains '
               'exactly one deprotonated carboxyl group (with proper '
               'connectivity) and an overall charge of -1 with no other '
               'charged atoms, consistent with a monocarboxylic acid anion\n'
               ' * SMILES: CCCCCCCCCCCCCCCCCCC(O)C([O-])=O NAME: '
               '2-hydroxyarachidate REASON: CORRECT The molecule contains '
               'exactly one deprotonated carboxyl group (with proper '
               'connectivity) and an overall charge of -1 with no other '
               'charged atoms, consistent with a monocarboxylic acid anion\n'
               ' * SMILES: C=1C=CC=C2NC(=C(C12)CC(=O)[O-])O NAME: '
               '2-hydroxy-(indol-3-yl)acetate REASON: CORRECT The molecule '
               'contains exactly one deprotonated carboxyl group (with proper '
               'connectivity) and an overall charge of -1 with no other '
               'charged atoms, consistent with a monocarboxylic acid anion\n'
               ' * SMILES: COc1cc(C([O-])=O)c2cccc(C)c2c1 NAME: '
               '3-methoxy-5-methyl-1-naphthoate REASON: CORRECT The molecule '
               'contains exactly one deprotonated carboxyl group (with proper '
               'connectivity) and an overall charge of -1 with no other '
               'charged atoms, consistent with a monocarboxylic acid anion\n'
               ' * SMILES: OC[C@@H](O)[C@@H](O)[C@H](O)[C@@H](O)C([O-])=O '
               'NAME: D-gluconate REASON: CORRECT The molecule contains '
               'exactly one deprotonated carboxyl group (with proper '
               'connectivity) and an overall charge of -1 with no other '
               'charged atoms, consistent with a monocarboxylic acid anion\n'
               ' * SMILES: CCCCCCCCCCCCC\\C=C\\C([O-])=O NAME: '
               '(E)-hexadec-2-enoate REASON: CORRECT The molecule contains '
               'exactly one deprotonated carboxyl group (with proper '
               'connectivity) and an overall charge of -1 with no other '
               'charged atoms, consistent with a monocarboxylic acid anion\n'
               ' * SMILES: C1(C([O-])=O)=CC=C(Br)C=C1 NAME: 4-bromobenzoate '
               'REASON: CORRECT The molecule contains exactly one deprotonated '
               'carboxyl group (with proper connectivity) and an overall '
               'charge of -1 with no other charged atoms, consistent with a '
               'monocarboxylic acid anion\n'
               ' * SMILES: C(=O)(C1=CC(=C(C=C1)O)O)[O-] NAME: '
               '3,4-dihydroxybenzoate REASON: CORRECT The molecule contains '
               'exactly one deprotonated carboxyl group (with proper '
               'connectivity) and an overall charge of -1 with no other '
               'charged atoms, consistent with a monocarboxylic acid anion\n'
               ' * SMILES: CCCC\\C=C/CCCCCCCCCCCC([O-])=O NAME: '
               '(13Z)-octadecenoate REASON: CORRECT The molecule contains '
               'exactly one deprotonated carboxyl group (with proper '
               'connectivity) and an overall charge of -1 with no other '
               'charged atoms, consistent with a monocarboxylic acid anion\n'
               ' * SMILES: CCCCCCCCCCCCCCCCCCCCCCCCCC([O-])=O NAME: cerotate '
               'REASON: CORRECT The molecule contains exactly one deprotonated '
               'carboxyl group (with proper connectivity) and an overall '
               'charge of -1 with no other charged atoms, consistent with a '
               'monocarboxylic acid anion\n'
               ' * SMILES: '
               'C1(C)(CO)CCCC(=C1\\C=C\\C(=C\\C=C\\C(=C\\C(=O)[O-])\\C)\\C)C '
               'NAME: all-trans-16-hydroxyretinoate REASON: CORRECT The '
               'molecule contains exactly one deprotonated carboxyl group '
               '(with proper connectivity) and an overall charge of -1 with no '
               'other charged atoms, consistent with a monocarboxylic acid '
               'anion\n'
               ' * SMILES: C(CCCCCCCCCC(CC([O-])=O)=O)CCCCCCCCCCCCCCCCC NAME: '
               '3-oxotriacontanoate(1-) REASON: CORRECT The molecule contains '
               'exactly one deprotonated carboxyl group (with proper '
               'connectivity) and an overall charge of -1 with no other '
               'charged atoms, consistent with a monocarboxylic acid anion\n'
               ' * SMILES: O[C@H](C([O-])=O)c1ccc(O)cc1 NAME: '
               '(S)-4-hydroxymandelate REASON: CORRECT The molecule contains '
               'exactly one deprotonated carboxyl group (with proper '
               'connectivity) and an overall charge of -1 with no other '
               'charged atoms, consistent with a monocarboxylic acid anion\n'
               ' * SMILES: '
               'C1[C@@]2([C@]3(C[C@@H]([C@]4([C@]([C@@]3(CC[C@@]2(CC(C1)=O)[H])[H])(CC[C@@]4([C@@H](CCC([O-])=O)C)[H])[H])C)O)[H])C '
               'NAME: 12alpha-hydroxy-3-oxo-5beta-cholan-24-oate REASON: '
               'CORRECT The molecule contains exactly one deprotonated '
               'carboxyl group (with proper connectivity) and an overall '
               'charge of -1 with no other charged atoms, consistent with a '
               'monocarboxylic acid anion\n'
               ' * SMILES: CC(C)(O)C([O-])=O NAME: 2-hydroxyisobutyrate '
               'REASON: CORRECT The molecule contains exactly one deprotonated '
               'carboxyl group (with proper connectivity) and an overall '
               'charge of -1 with no other charged atoms, consistent with a '
               'monocarboxylic acid anion\n'
               ' * SMILES: COc1ccc(C([O-])=O)c(NC(=O)c2ccccc2)c1 NAME: '
               'N-benzoyl-4-methoxyanthranilate REASON: CORRECT The molecule '
               'contains exactly one deprotonated carboxyl group (with proper '
               'connectivity) and an overall charge of -1 with no other '
               'charged atoms, consistent with a monocarboxylic acid anion\n'
               ' * SMILES: O[C@H]1C=CC=C(CCC([O-])=O)[C@H]1O NAME: '
               '3-[(5S,6R)-5,6-dihydroxycyclohexa-1,3-dienyl]propanoate '
               'REASON: CORRECT The molecule contains exactly one deprotonated '
               'carboxyl group (with proper connectivity) and an overall '
               'charge of -1 with no other charged atoms, consistent with a '
               'monocarboxylic acid anion\n'
               ' * SMILES: CCCCC\\C=C/C\\C=C/C\\C=C/C=C/[C@H](CCCC([O-])=O)OO '
               'NAME: 5(S)-HPETE(1-) REASON: CORRECT The molecule contains '
               'exactly one deprotonated carboxyl group (with proper '
               'connectivity) and an overall charge of -1 with no other '
               'charged atoms, consistent with a monocarboxylic acid anion\n'
               ' * SMILES: C(CCCCCCCC)C[C@H](C([O-])=O)OO NAME: '
               '(2R)-2-hydroperoxydodecanoate REASON: CORRECT The molecule '
               'contains exactly one deprotonated carboxyl group (with proper '
               'connectivity) and an overall charge of -1 with no other '
               'charged atoms, consistent with a monocarboxylic acid anion\n'
               ' * SMILES: Cc1cc(C)cc(c1)C([O-])=O NAME: 3,5-dimethylbenzoate '
               'REASON: CORRECT The molecule contains exactly one deprotonated '
               'carboxyl group (with proper connectivity) and an overall '
               'charge of -1 with no other charged atoms, consistent with a '
               'monocarboxylic acid anion\n'
               ' * SMILES: '
               'C12=C(NCC(=N1)CNC3=CC=C(C([O-])=O)C(=C3)O)N=C(N)NC2=O NAME: '
               '2-hydroxy-7,8-dihydropteroate REASON: CORRECT The molecule '
               'contains exactly one deprotonated carboxyl group (with proper '
               'connectivity) and an overall charge of -1 with no other '
               'charged atoms, consistent with a monocarboxylic acid anion\n'
               ' * SMILES: '
               'O1[C@@]([C@@H]([C@@H](CO)O)O)([C@H](O)[C@@H](O)C[C@]1(C([O-])=O)O)[H] '
               'NAME: 3-deoxy-D-glycero-beta-D-galacto-nonulosonate REASON: '
               'CORRECT The molecule contains exactly one deprotonated '
               'carboxyl group (with proper connectivity) and an overall '
               'charge of -1 with no other charged atoms, consistent with a '
               'monocarboxylic acid anion\n'
               ' * SMILES: '
               'C1[C@@]2([C@]3(CC([C@]4([C@]([C@@]3(C(C[C@@]2(C[C@@H](C1)O)[H])=O)[H])(CC[C@@]4([C@@H](CCC([O-])=O)C)[H])[H])C)=O)[H])C '
               'NAME: 7,12-dioxolithocholate REASON: CORRECT The molecule '
               'contains exactly one deprotonated carboxyl group (with proper '
               'connectivity) and an overall charge of -1 with no other '
               'charged atoms, consistent with a monocarboxylic acid anion\n'
               ' * SMILES: CCCCCCC\\C=C\\CCCCCCCCC([O-])=O NAME: '
               '(10E)-octadecenoate REASON: CORRECT The molecule contains '
               'exactly one deprotonated carboxyl group (with proper '
               'connectivity) and an overall charge of -1 with no other '
               'charged atoms, consistent with a monocarboxylic acid anion\n'
               ' * SMILES: C(CCCCCCCCCCCCCCC([O-])=O)CCC(C)O NAME: '
               '19-hydroxyicosanoate REASON: CORRECT The molecule contains '
               'exactly one deprotonated carboxyl group (with proper '
               'connectivity) and an overall charge of -1 with no other '
               'charged atoms, consistent with a monocarboxylic acid anion\n'
               'False positives: SMILES: C1(=CC=C(C=C1NC(C)=O)C([O-])=O)O '
               'NAME: 3-acetamido-4-hydroxybenzoate REASON: WRONGLY CLASSIFIED '
               'The molecule contains exactly one deprotonated carboxyl group '
               '(with proper connectivity) and an overall charge of -1 with no '
               'other charged atoms, consistent with a monocarboxylic acid '
               'anion\n'
               ' * SMILES: [O-]C(=O)OON=O NAME: nitrosoperoxycarbonate(1-) '
               'REASON: WRONGLY CLASSIFIED The molecule contains exactly one '
               'deprotonated carboxyl group (with proper connectivity) and an '
               'overall charge of -1 with no other charged atoms, consistent '
               'with a monocarboxylic acid anion\n'
               ' * SMILES: C([O-])(=O)/C=C/C=1C=C(C(O)=CC1)N NAME: '
               '(E)-3-aminocoumarate REASON: WRONGLY CLASSIFIED The molecule '
               'contains exactly one deprotonated carboxyl group (with proper '
               'connectivity) and an overall charge of -1 with no other '
               'charged atoms, consistent with a monocarboxylic acid anion\n'
               ' * SMILES: [O-]C(=O)[C@H]1CCC(=O)N1 NAME: 5-oxo-D-prolinate '
               'REASON: WRONGLY CLASSIFIED The molecule contains exactly one '
               'deprotonated carboxyl group (with proper connectivity) and an '
               'overall charge of -1 with no other charged atoms, consistent '
               'with a monocarboxylic acid anion\n'
               ' * SMILES: '
               'C[C@@H]([C@H]1CC[C@H]2[C@@H]3CCC4=CC(=O)CC[C@]4(C)[C@H]3CC[C@]12C)C([O-])=O '
               'NAME: 3-oxo-23,24-bisnorchol-4-en-22-oate REASON: WRONGLY '
               'CLASSIFIED The molecule contains exactly one deprotonated '
               'carboxyl group (with proper connectivity) and an overall '
               'charge of -1 with no other charged atoms, consistent with a '
               'monocarboxylic acid anion\n'
               ' * SMILES: C(=O)([C@@H](NC(=O)CC)CCSC)[O-] NAME: '
               'N-propanoyl-L-methioninate REASON: WRONGLY CLASSIFIED The '
               'molecule contains exactly one deprotonated carboxyl group '
               '(with proper connectivity) and an overall charge of -1 with no '
               'other charged atoms, consistent with a monocarboxylic acid '
               'anion\n'
               ' * SMILES: '
               'C[C@H](CCCCCCCCC/C=C/C([O-])=O)O[C@@H]1O[C@@H](C)[C@H](O)C[C@H]1O '
               'NAME: ascr#23(1-) REASON: WRONGLY CLASSIFIED The molecule '
               'contains exactly one deprotonated carboxyl group (with proper '
               'connectivity) and an overall charge of -1 with no other '
               'charged atoms, consistent with a monocarboxylic acid anion\n'
               ' * SMILES: CC(C)=CCNc1ncn(CC[C@H](N)C([O-])=O)c2ncnc12 NAME: '
               'discadenine(1-) REASON: WRONGLY CLASSIFIED The molecule '
               'contains exactly one deprotonated carboxyl group (with proper '
               'connectivity) and an overall charge of -1 with no other '
               'charged atoms, consistent with a monocarboxylic acid anion\n'
               ' * SMILES: OC(=O)C(=O)C([O-])=O NAME: oxomalonate(1-) REASON: '
               'WRONGLY CLASSIFIED The molecule contains exactly one '
               'deprotonated carboxyl group (with proper connectivity) and an '
               'overall charge of -1 with no other charged atoms, consistent '
               'with a monocarboxylic acid anion\n'
               ' * SMILES: '
               '[H][C@]12SCC(C)=C(N1C(=O)[C@H]2NC(=O)[C@H](N)c1ccc(O)cc1)C([O-])=O '
               'NAME: cefadroxil(1-) REASON: WRONGLY CLASSIFIED The molecule '
               'contains exactly one deprotonated carboxyl group (with proper '
               'connectivity) and an overall charge of -1 with no other '
               'charged atoms, consistent with a monocarboxylic acid anion\n'
               ' * SMILES: '
               'C(O)C(=O)[C@@H](O)[C@H](O)[C@H](O)[C@@H](O)[C@@H](O)C(=O)[O-] '
               'NAME: L-glycero-L-galacto-octuluronate REASON: WRONGLY '
               'CLASSIFIED The molecule contains exactly one deprotonated '
               'carboxyl group (with proper connectivity) and an overall '
               'charge of -1 with no other charged atoms, consistent with a '
               'monocarboxylic acid anion\n'
               ' * SMILES: N[C@@H](CCC(N)=O)C([O-])=O NAME: L-glutaminate '
               'REASON: WRONGLY CLASSIFIED The molecule contains exactly one '
               'deprotonated carboxyl group (with proper connectivity) and an '
               'overall charge of -1 with no other charged atoms, consistent '
               'with a monocarboxylic acid anion\n'
               ' * SMILES: '
               'C[C@@H]1O[C@@H](OCCCCCCCCCC(=O)CC([O-])=O)[C@H](O)C[C@H]1O '
               'NAME: bkos#20(1-) REASON: WRONGLY CLASSIFIED The molecule '
               'contains exactly one deprotonated carboxyl group (with proper '
               'connectivity) and an overall charge of -1 with no other '
               'charged atoms, consistent with a monocarboxylic acid anion\n'
               ' * SMILES: '
               '[H][C@]1(O[C@@](C[C@H](O)[C@H]1NC(C)=O)(O[C@@H]1[C@@H](O)[C@@H](O[C@H](CO)[C@@H]1O[C@@H]1O[C@H](CO)[C@H](O)[C@H](O[C@@H]2O[C@H](CO)[C@H](O)[C@H](O)[C@H]2O)[C@H]1NC(C)=O)O[C@H]1[C@H](O)[C@@H](O)[C@H](OC[C@H](NC(=O)CCCCCCCCCCCCCCCCC)[C@H](O)\\C=C\\CCCCCCCCCCCCC)O[C@@H]1CO)C([O-])=O)[C@H](O)[C@H](O)CO '
               'NAME: ganglioside GM1(1-) REASON: WRONGLY CLASSIFIED The '
               'molecule contains exactly one deprotonated carboxyl group '
               '(with proper connectivity) and an overall charge of -1 with no '
               'other charged atoms, consistent with a monocarboxylic acid '
               'anion\n'
               ' * SMILES: OC(=O)c1ccccc1-c1ccccc1C([O-])=O NAME: '
               'diphenate(1-) REASON: WRONGLY CLASSIFIED The molecule contains '
               'exactly one deprotonated carboxyl group (with proper '
               'connectivity) and an overall charge of -1 with no other '
               'charged atoms, consistent with a monocarboxylic acid anion\n'
               ' * SMILES: '
               'C[C@H](CCCC(C)C([O-])=O)[C@H]1CC[C@H]2[C@@H]3CCC4=CC(=O)CC[C@]4(C)[C@H]3CC[C@]12C '
               'NAME: Delta(4)-dafachronate REASON: WRONGLY CLASSIFIED The '
               'molecule contains exactly one deprotonated carboxyl group '
               '(with proper connectivity) and an overall charge of -1 with no '
               'other charged atoms, consistent with a monocarboxylic acid '
               'anion\n'
               ' * SMILES: '
               'C=1[C@@]2([C@@](C[C@H](O)[C@]2(C(=O)[O-])NC(CS(N)(=O)=O)=O)(C(C(N)=O)=CN1)[H])[H] '
               'NAME: didehydrodemethylaltemicidin REASON: WRONGLY CLASSIFIED '
               'The molecule contains exactly one deprotonated carboxyl group '
               '(with proper connectivity) and an overall charge of -1 with no '
               'other charged atoms, consistent with a monocarboxylic acid '
               'anion\n'
               ' * SMILES: CSCC[C@@H](N)C([O-])=O NAME: D-methioninate REASON: '
               'WRONGLY CLASSIFIED The molecule contains exactly one '
               'deprotonated carboxyl group (with proper connectivity) and an '
               'overall charge of -1 with no other charged atoms, consistent '
               'with a monocarboxylic acid anion\n'
               ' * SMILES: C(CCCCCCCCCC)CCCCC(N[C@H](C([O-])=O)O)=O NAME: '
               'N-hexadecanoyl-(2S)-hydroxyglycinate REASON: WRONGLY '
               'CLASSIFIED The molecule contains exactly one deprotonated '
               'carboxyl group (with proper connectivity) and an overall '
               'charge of -1 with no other charged atoms, consistent with a '
               'monocarboxylic acid anion\n'
               ' * SMILES: CC(=O)NCC([O-])=O NAME: N-acetylglycinate REASON: '
               'WRONGLY CLASSIFIED The molecule contains exactly one '
               'deprotonated carboxyl group (with proper connectivity) and an '
               'overall charge of -1 with no other charged atoms, consistent '
               'with a monocarboxylic acid anion\n'
               ' * SMILES: CC[C@@H](C)[C@@H](N)C([O-])=O NAME: D-isoleucinate '
               'REASON: WRONGLY CLASSIFIED The molecule contains exactly one '
               'deprotonated carboxyl group (with proper connectivity) and an '
               'overall charge of -1 with no other charged atoms, consistent '
               'with a monocarboxylic acid anion\n'
               ' * SMILES: N[C@@H](C[SeH])C([O-])=O NAME: '
               'L-selenocysteinate(1-) REASON: WRONGLY CLASSIFIED The molecule '
               'contains exactly one deprotonated carboxyl group (with proper '
               'connectivity) and an overall charge of -1 with no other '
               'charged atoms, consistent with a monocarboxylic acid anion\n'
               ' * SMILES: '
               'N[C@@H](C(=O)N[C@H]1[C@H]2CCC(Cl)=C(N2C1=O)C([O-])=O)c1ccccc1 '
               'NAME: loracarbef anion REASON: WRONGLY CLASSIFIED The molecule '
               'contains exactly one deprotonated carboxyl group (with proper '
               'connectivity) and an overall charge of -1 with no other '
               'charged atoms, consistent with a monocarboxylic acid anion\n'
               ' * SMILES: '
               'C12=C(C(C(C3=CC=C(O[C@H]4[C@@H]([C@H]([C@@H]([C@H](O4)C([O-])=O)O)O)O)C=C3)=CO1)=O)C(=CC(=C2)OC)O '
               "NAME: prunetin-4'-O-beta-D-glucuronide(1-) REASON: WRONGLY "
               'CLASSIFIED The molecule contains exactly one deprotonated '
               'carboxyl group (with proper connectivity) and an overall '
               'charge of -1 with no other charged atoms, consistent with a '
               'monocarboxylic acid anion\n'
               ' * SMILES: NC(CCS)C([O-])=O NAME: homocysteinate REASON: '
               'WRONGLY CLASSIFIED The molecule contains exactly one '
               'deprotonated carboxyl group (with proper connectivity) and an '
               'overall charge of -1 with no other charged atoms, consistent '
               'with a monocarboxylic acid anion\n'
               'False negatives: SMILES: '
               '[H][C@]12SC(C)(C)[C@@H](N1C(=O)[C@H]2NC(=O)C(C([O-])=O)c1ccccc1)C([O-])=O '
               'NAME: carbenicillin(2-) REASON: MISSED Found 2 carboxylate '
               'groups; molecule is not a monocarboxylic acid anion\n'
               ' * SMILES: '
               'O[C@H](COP([O-])([O-])=O)[C@@H](O)C(=O)CNc1ccccc1C([O-])=O '
               'NAME: 1-(2-carboxylatophenylamino)-1-deoxy-D-ribulose '
               '5-phosphate(3-) REASON: MISSED Expected overall charge of -1 '
               'for a monocarboxylate anion, found charge = -3\n'
               ' * SMILES: O[C@H](COP([O-])([O-])=O)[C@@H](O)CC(=O)C([O-])=O '
               'NAME: 2-dehydro-3-deoxy-6-phosphonato-D-gluconate(3-) REASON: '
               'MISSED Expected overall charge of -1 for a monocarboxylate '
               'anion, found charge = -3\n'
               ' * SMILES: '
               'CO[C@H]1O[C@H](COS([O-])(=O)=O)[C@@H](O[C@@H]2O[C@H]([C@@H](O[C@H]3O[C@H](COS([O-])(=O)=O)[C@@H](O[C@@H]4O[C@@H]([C@@H](O[C@H]5O[C@H](COS([O-])(=O)=O)[C@@H](O)[C@H](O)[C@H]5NS([O-])(=O)=O)[C@H](O)[C@H]4O)C([O-])=O)[C@H](OS([O-])(=O)=O)[C@H]3NS([O-])(=O)=O)[C@H](O)[C@H]2OS([O-])(=O)=O)C([O-])=O)[C@H](O)[C@H]1NS([O-])(=O)=O '
               'NAME: fondaparinux(10-) REASON: MISSED Found 2 carboxylate '
               'groups; molecule is not a monocarboxylic acid anion\n'
               ' * SMILES: '
               'O[C@@H]1[C@@H](COP(O)(=O)OP(O)(=O)OC2O[C@H]([C@@H](O)[C@H](O)[C@H]2O)C(O)=O)O[C@H]([C@@H]1O)n1ccc(=O)[nH]c1=O '
               'NAME: UDP-L-iduronic acid REASON: MISSED No deprotonated '
               'carboxyl (carboxylate) group found\n'
               ' * SMILES: '
               'O(C[C@@H]([C@@H]([C@H](C([O-])=O)O)O)O)P([O-])(=O)[O-] NAME: '
               '5-phospho-L-arabinonate(3-) REASON: MISSED Expected overall '
               'charge of -1 for a monocarboxylate anion, found charge = -3\n'
               ' * SMILES: '
               'Oc1c(OC(OC(C=O)C([O-])=O)C=O)ccc2occ(-c3ccccc3OS([O-])(=O)=O)c(=O)c12 '
               'NAME: '
               '2-[1-({5-hydroxy-4-oxo-3-[2-(sulfonatooxy)phenyl]-4H-chromen-6-yl}oxy)-2-oxoethoxy]-3-oxopropanoate '
               'REASON: MISSED Expected overall charge of -1 for a '
               'monocarboxylate anion, found charge = -2\n'
               ' * SMILES: C[C@@](O)(CCOP([O-])([O-])=O)CC([O-])=O NAME: '
               '(R)-5-phosphonatomevalonate(3-) REASON: MISSED Expected '
               'overall charge of -1 for a monocarboxylate anion, found charge '
               '= -3\n'
               ' * SMILES: '
               '[H][C@]12C[C@@H](C)C[C@@H](C)[C@]1([H])[C@@H](\\C([O-])=C1\\C(=O)N[C@@H](C[C@](C)(O)C([O-])=O)C1=O)[C@]([H])(C=C2)C(\\C)=C\\C '
               'NAME: sch 210972(2-) REASON: MISSED Expected overall charge of '
               '-1 for a monocarboxylate anion, found charge = -2\n'
               ' * SMILES: '
               'CC(=O)N[C@H]1C(O)O[C@H](COS([O-])(=O)=O)[C@H](O)[C@@H]1O[C@@H]1OC(=C[C@H](O)[C@H]1O)C([O-])=O '
               'NAME: '
               '2-acetamido-2-deoxy-3-O-(4-deoxy-alpha-L-threo-hex-4-enopyranosyluronate)-6-O-sulfonato-D-galactopyranose(2-) '
               'REASON: MISSED Expected overall charge of -1 for a '
               'monocarboxylate anion, found charge = -2\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'O=C(N[C@@H](C(O)(C)C)C)[C@H]([C@@]1([C@@]2([C@@](CC1)(/C(/CCC2)=C/C=C\\3/C[C@@H](O)C[C@H](O)C3=C)[H])C)[H])C',
                                     'name': '1alpha,25-dihydroxy-24-oxo-23-azavitamin '
                                             'D2 / '
                                             '1alpha,25-dihydroxy-24-oxo-23-azaergocalciferol',
                                     'reason': 'No deprotonated carboxyl '
                                               '(carboxylate) group found'},
                                 {   'smiles': 'C[C@@H](CN([C@@H](C)CO)C(=O)NC1=CC=C(C=C1)C(F)(F)F)[C@@H](CN(C)C(=O)C2CCOCC2)OC',
                                     'name': 'N-[(2S,3S)-4-[[(2S)-1-hydroxypropan-2-yl]-[[4-(trifluoromethyl)phenyl]carbamoyl]amino]-2-methoxy-3-methylbutyl]-N-methyloxane-4-carboxamide',
                                     'reason': 'No deprotonated carboxyl '
                                               '(carboxylate) group found'},
                                 {   'smiles': 'CC(=O)CC\\C=C(/C)CCC=C(C)C',
                                     'name': 'geranyl acetone',
                                     'reason': 'No deprotonated carboxyl '
                                               '(carboxylate) group found'},
                                 {   'smiles': 'O([C@H]1[C@H](O)[C@H](O[C@H](O)[C@H]1O)CO[C@H]2O[C@@H]([C@@H](O)[C@H](O)[C@@H]2O)CO)[C@H]3O[C@@H]([C@@H](O)[C@H](O)[C@@H]3O[C@H]4O[C@@H]([C@@H](O)[C@H](O)[C@@H]4O)CO)CO',
                                     'name': '(2S,3S,4S,5S,6R)-2-[[(2R,3R,4S,5S,6S)-4-[(2R,3S,4S,5S,6R)-4,5-Dihydroxy-6-(hydroxymethyl)-3-[(2R,3S,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-3,5,6-trihydroxyoxan-2-yl]methoxy]-6-(hydroxymethyl)oxane-3,4,5-triol',
                                     'reason': 'No deprotonated carboxyl '
                                               '(carboxylate) group found'},
                                 {   'smiles': 'O=C(OC1=C(C(O)=C(C(=O)O)C(=C1C)C)C)C2=C(OC)C(=C(OC(=O)C3=C(O)C=C(O)C=C3C)C=C2C)C',
                                     'name': 'Thielavin Z5',
                                     'reason': 'No deprotonated carboxyl '
                                               '(carboxylate) group found'},
                                 {   'smiles': '[C@@H]1([C@@H]([C@H]([C@@H]([C@H](O1)CO)O)O)NC(C)=O)O[C@@H]2[C@@H]([C@H](C(O[C@@H]2CO)O)O)O',
                                     'name': 'beta-D-GlcpNAc-(1->4)-D-Galp',
                                     'reason': 'No deprotonated carboxyl '
                                               '(carboxylate) group found'},
                                 {   'smiles': 'CN(C)C(=O)C1=CC=C(C=C1)C2=CC=C(C=C2)[C@@H]3[C@H]4CN(CC(=O)N4[C@H]3CO)C(=O)CC5CC5',
                                     'name': '4-[4-[(6S,7R,8R)-4-(2-cyclopropyl-1-oxoethyl)-8-(hydroxymethyl)-2-oxo-1,4-diazabicyclo[4.2.0]octan-7-yl]phenyl]-N,N-dimethylbenzamide',
                                     'reason': 'No deprotonated carboxyl '
                                               '(carboxylate) group found'},
                                 {   'smiles': 'CCCCCCCCCCCCCCCCCCCCC=C',
                                     'name': '1-docosene',
                                     'reason': 'No deprotonated carboxyl '
                                               '(carboxylate) group found'},
                                 {   'smiles': 'C([C@@](OC(=O)CCC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)([H])COC(=O)CC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)OC(=O)CCCCC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC',
                                     'name': 'TG(22:5(7Z,10Z,13Z,16Z,19Z)/20:5(5Z,8Z,11Z,14Z,17Z)/22:6(4Z,7Z,10Z,13Z,16Z,19Z))[iso6]',
                                     'reason': 'No deprotonated carboxyl '
                                               '(carboxylate) group found'},
                                 {   'smiles': 'CCCCC\\C=C/C\\C=C/CCCCCCCCCC(=O)NCCO',
                                     'name': 'N-(11Z,14Z)-eicosadienoylethanolamine',
                                     'reason': 'No deprotonated carboxyl '
                                               '(carboxylate) group found'}],
    'sample_false_negatives': [   {   'smiles': '[H][C@]12SC(C)(C)[C@@H](N1C(=O)[C@H]2NC(=O)C(C([O-])=O)c1ccccc1)C([O-])=O',
                                      'name': 'carbenicillin(2-)',
                                      'reason': 'Found 2 carboxylate groups; '
                                                'molecule is not a '
                                                'monocarboxylic acid anion'},
                                  {   'smiles': 'O[C@H](COP([O-])([O-])=O)[C@@H](O)C(=O)CNc1ccccc1C([O-])=O',
                                      'name': '1-(2-carboxylatophenylamino)-1-deoxy-D-ribulose '
                                              '5-phosphate(3-)',
                                      'reason': 'Expected overall charge of -1 '
                                                'for a monocarboxylate anion, '
                                                'found charge = -3'},
                                  {   'smiles': 'O[C@H](COP([O-])([O-])=O)[C@@H](O)CC(=O)C([O-])=O',
                                      'name': '2-dehydro-3-deoxy-6-phosphonato-D-gluconate(3-)',
                                      'reason': 'Expected overall charge of -1 '
                                                'for a monocarboxylate anion, '
                                                'found charge = -3'},
                                  {   'smiles': 'CO[C@H]1O[C@H](COS([O-])(=O)=O)[C@@H](O[C@@H]2O[C@H]([C@@H](O[C@H]3O[C@H](COS([O-])(=O)=O)[C@@H](O[C@@H]4O[C@@H]([C@@H](O[C@H]5O[C@H](COS([O-])(=O)=O)[C@@H](O)[C@H](O)[C@H]5NS([O-])(=O)=O)[C@H](O)[C@H]4O)C([O-])=O)[C@H](OS([O-])(=O)=O)[C@H]3NS([O-])(=O)=O)[C@H](O)[C@H]2OS([O-])(=O)=O)C([O-])=O)[C@H](O)[C@H]1NS([O-])(=O)=O',
                                      'name': 'fondaparinux(10-)',
                                      'reason': 'Found 2 carboxylate groups; '
                                                'molecule is not a '
                                                'monocarboxylic acid anion'},
                                  {   'smiles': 'O[C@@H]1[C@@H](COP(O)(=O)OP(O)(=O)OC2O[C@H]([C@@H](O)[C@H](O)[C@H]2O)C(O)=O)O[C@H]([C@@H]1O)n1ccc(=O)[nH]c1=O',
                                      'name': 'UDP-L-iduronic acid',
                                      'reason': 'No deprotonated carboxyl '
                                                '(carboxylate) group found'},
                                  {   'smiles': 'O(C[C@@H]([C@@H]([C@H](C([O-])=O)O)O)O)P([O-])(=O)[O-]',
                                      'name': '5-phospho-L-arabinonate(3-)',
                                      'reason': 'Expected overall charge of -1 '
                                                'for a monocarboxylate anion, '
                                                'found charge = -3'},
                                  {   'smiles': 'Oc1c(OC(OC(C=O)C([O-])=O)C=O)ccc2occ(-c3ccccc3OS([O-])(=O)=O)c(=O)c12',
                                      'name': '2-[1-({5-hydroxy-4-oxo-3-[2-(sulfonatooxy)phenyl]-4H-chromen-6-yl}oxy)-2-oxoethoxy]-3-oxopropanoate',
                                      'reason': 'Expected overall charge of -1 '
                                                'for a monocarboxylate anion, '
                                                'found charge = -2'},
                                  {   'smiles': 'C[C@@](O)(CCOP([O-])([O-])=O)CC([O-])=O',
                                      'name': '(R)-5-phosphonatomevalonate(3-)',
                                      'reason': 'Expected overall charge of -1 '
                                                'for a monocarboxylate anion, '
                                                'found charge = -3'},
                                  {   'smiles': '[H][C@]12C[C@@H](C)C[C@@H](C)[C@]1([H])[C@@H](\\C([O-])=C1\\C(=O)N[C@@H](C[C@](C)(O)C([O-])=O)C1=O)[C@]([H])(C=C2)C(\\C)=C\\C',
                                      'name': 'sch 210972(2-)',
                                      'reason': 'Expected overall charge of -1 '
                                                'for a monocarboxylate anion, '
                                                'found charge = -2'},
                                  {   'smiles': 'CC(=O)N[C@H]1C(O)O[C@H](COS([O-])(=O)=O)[C@H](O)[C@@H]1O[C@@H]1OC(=C[C@H](O)[C@H]1O)C([O-])=O',
                                      'name': '2-acetamido-2-deoxy-3-O-(4-deoxy-alpha-L-threo-hex-4-enopyranosyluronate)-6-O-sulfonato-D-galactopyranose(2-)',
                                      'reason': 'Expected overall charge of -1 '
                                                'for a monocarboxylate anion, '
                                                'found charge = -2'}],
    'attempt': 3,
    'reasoning': 'Below is one possible solution. In our reasoning we noticed '
                 'that the previous approach picked up any –CO2– fragment that '
                 'looked “carboxylate‐like” and then only checked the overall '
                 '–1 charge plus that no other atom carried a charge. However, '
                 'many of the “false‐positive” examples had exactly one '
                 'matching –CO2– fragment but are not, in fact, the simple '
                 'deprotonated form of a monocarboxylic acid. We therefore add '
                 'extra checks on the connectivity of the carboxylate group. '
                 'First, after finding the unique match for the SMARTS pattern '
                 '“[#6X3](=O)[O-]” (which identifies a carboxylate with a '
                 'trigonal carbon bound to a double‐bonded oxygen and a '
                 'single‐bonded oxygen carrying –1), we verify that the '
                 'carboxyl carbon has exactly three neighbors but that exactly '
                 'two of these are oxygens. Then we inspect the bonds: one '
                 'oxygen must be bonded via a double bond (the carbonyl '
                 'oxygen, with formal charge 0) and the other by a single bond '
                 '(the deprotonated oxygen, with charge –1). Finally, we '
                 're‐confirm that the overall formal charge is exactly –1 and '
                 'that no other atoms outside the carboxylate group carry a '
                 'formal charge. (In practice there is always a trade‐off '
                 'between rejecting borderline cases and over‐filtering; but '
                 'we hope these extra connectivity checks help the classifier '
                 'improve its F1 score.) \n'
                 '\n'
                 'Below is the complete Python code block using RDKit. \n'
                 '\n'
                 '------------------------------------------------',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 1713,
    'num_false_positives': 610,
    'num_true_negatives': 139757,
    'num_false_negatives': 220,
    'num_negatives': None,
    'precision': 0.7374085234610418,
    'recall': 0.8861872736678738,
    'f1': 0.8049812030075187,
    'accuracy': 0.9941672522839072,
    'negative_predictive_value': 0.9984283132228866}