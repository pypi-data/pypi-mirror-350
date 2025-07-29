"""
Classifies: CHEBI:26607 saturated fatty acid
"""
"""
Classifies: Saturated fatty acid

A saturated fatty acid is defined here as a molecule that:
  - Contains only C, H, and O atoms.
  - Contains exactly one carboxylic acid group defined as [CX3](=O)[OX2H].
  - Has no carbon–carbon multiple bonds.
  - Contains no additional carbonyl groups (C=O bonds between C and O) outside the acid group if the molecule has 7 or more carbons.
  - Does not have an -OH substituent on the alpha carbon (the carbon directly bonded to the acid carbon).
  - May have a single additional hydroxyl group at the end of the chain (the ω‐position). Any extra oxygen-containing functionality (e.g. non‐terminal –OH, keto, methoxy) is disallowed.
  
Note: Unlike the previous attempt, we do not reject molecules solely on the basis of ring structures.
"""

from rdkit import Chem

def is_saturated_fatty_acid(smiles: str):
    """
    Determines if a molecule is a saturated fatty acid based on its SMILES string.
    The molecule must:
      - Contain only C, H, and O atoms.
      - Have exactly one carboxylic acid group (SMARTS: [CX3](=O)[OX2H]).
      - Have no carbon–carbon double or triple bonds.
      - In molecules with 7 or more carbons, have no additional carbonyl groups (C=O) beyond that in the acid.
      - Not have an -OH substituent on the alpha carbon (the carbon directly bonded to the acid carbon).
      - Optionally have one extra (terminal) hydroxyl group at the opposite omega (ω) end.
      
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if the molecule is classified as a saturated fatty acid, False otherwise.
        str: Explanation/reason for the decision.
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
    
    # (1) Allowed atoms: only H (1), C (6), and O (8)
    allowed_atomic_nums = {1, 6, 8}
    for atom in mol.GetAtoms():
        if atom.GetAtomicNum() not in allowed_atomic_nums:
            return False, "Contains atoms other than C, H, and O"
    
    # (2) Identify the carboxylic acid group.
    acid_smarts = "[CX3](=O)[OX2H]"
    acid_pattern = Chem.MolFromSmarts(acid_smarts)
    acid_matches = mol.GetSubstructMatches(acid_pattern)
    if not acid_matches:
        return False, "No carboxylic acid group found"
    if len(acid_matches) != 1:
        return False, "More than one carboxylic acid group found"
    
    # Record acid group atom indices.
    acid_match = acid_matches[0]
    acid_carbon_idx = acid_match[0]       # the carboxyl carbon
    acid_carbonyl_oxygen_idx = acid_match[1]  # the allowed carbonyl oxygen
    acid_oh_oxygen_idx = acid_match[2]     # the hydroxyl oxygen of the COOH
    
    # (3) Check for any carbon-to-carbon multiple bonds.
    for bond in mol.GetBonds():
        if bond.GetBondType() in [Chem.rdchem.BondType.DOUBLE, Chem.rdchem.BondType.TRIPLE]:
            a1 = bond.GetBeginAtom()
            a2 = bond.GetEndAtom()
            if a1.GetAtomicNum() == 6 and a2.GetAtomicNum() == 6:
                return False, "Contains carbon-to-carbon multiple bonds"
    
    # (4) Count carbons in the molecule.
    total_carbons = sum(1 for atom in mol.GetAtoms() if atom.GetAtomicNum() == 6)
    
    # (5) Check for additional carbonyl groups (C=O bonds between C and O, not part of the acid group).
    # For molecules with 7 or more carbons, any extra C=O (double bonds: C=O) will lead to rejection.
    if total_carbons >= 7:
        for bond in mol.GetBonds():
            if bond.GetBondType() == Chem.rdchem.BondType.DOUBLE:
                a1 = bond.GetBeginAtom()
                a2 = bond.GetEndAtom()
                # We look for a C=O bond:
                if (a1.GetAtomicNum(), a2.GetAtomicNum()) in [(6,8), (8,6)]:
                    idxs = {bond.GetBeginAtomIdx(), bond.GetEndAtomIdx()}
                    # Allow if this is the acid carbonyl
                    if {acid_carbon_idx, acid_carbonyl_oxygen_idx} == idxs:
                        continue
                    else:
                        return False, "Contains additional carbonyl group(s) beyond the carboxylic acid"
    
    # (6) Check that the acid group is terminal in the sense that there is no -OH on the alpha carbon.
    acid_carbon = mol.GetAtomWithIdx(acid_carbon_idx)
    for neighbor in acid_carbon.GetNeighbors():
        # Skip the neighbor that is the carbonyl oxygen.
        if neighbor.GetIdx() == acid_carbonyl_oxygen_idx:
            continue
        # For the remaining neighbor (alpha carbon), check if it bears an -OH group.
        for subnbr in neighbor.GetNeighbors():
            if subnbr.GetAtomicNum() == 8:
                bond = mol.GetBondBetweenAtoms(neighbor.GetIdx(), subnbr.GetIdx())
                if bond and bond.GetBondType() == Chem.rdchem.BondType.SINGLE:
                    # If the oxygen has at least one explicit hydrogen, treat it as an -OH.
                    if subnbr.GetTotalNumHs() > 0:
                        return False, "Contains an alpha-hydroxyl group adjacent to the carboxylic acid"
    
    # (7) Check for any extra oxygen functionality (outside the acid group).
    # Allowed extra oxygen: one terminal hydroxyl group (at the ω-end), defined as an -OH on a carbon that is terminal (has exactly one neighboring carbon).
    # Gather oxygen indices that are not part of the acid group.
    acid_atom_idxs = {acid_carbon_idx, acid_carbonyl_oxygen_idx, acid_oh_oxygen_idx}
    extra_oxygen_idxs = [atom.GetIdx() for atom in mol.GetAtoms() 
                           if atom.GetAtomicNum() == 8 and atom.GetIdx() not in acid_atom_idxs]
    
    allowed_terminal_oh_count = 0
    for oidx in extra_oxygen_idxs:
        oxy = mol.GetAtomWithIdx(oidx)
        # We expect these oxygens to be in a hydroxyl group (i.e. bonded by a single bond to a carbon and having at least one H)
        if oxy.GetDegree() != 1 or oxy.GetTotalNumHs() < 1:
            return False, "Contains extra oxygen functionality that is not a terminal hydroxyl group"
        # Get the carbon to which this oxygen is attached.
        nbr = oxy.GetNeighbors()[0]
        if nbr.GetAtomicNum() != 6:
            return False, "Extra oxygen is not attached to a carbon"
        # Check that the carbon is terminal (only one carbon neighbor among heavy atoms).
        carbon_neighbors = [a for a in nbr.GetNeighbors() if a.GetAtomicNum() == 6]
        if len(carbon_neighbors) != 1:
            return False, "Contains an extra hydroxyl group on a non-terminal carbon"
        allowed_terminal_oh_count += 1
        if allowed_terminal_oh_count > 1:
            return False, "More than one terminal hydroxyl group found"
    
    # Passed all checks.
    return True, ("Molecule has exactly one carboxylic acid group, only C/H/O atoms, no carbon–carbon multiple bonds, "
                  "no disallowed additional carbonyl or alpha‐OH groups, and at most one terminal extra hydroxyl group")

# Example usage (you may add more SMILES strings to test):
if __name__ == '__main__':
    test_smiles = [
        "OCCCCCCCCCCCCCCCCCCCC(O)=O",      # 20-hydroxyicosanoic acid (should be True)
        "CC(C)C(C)C(O)=O",                 # 2,3-dimethylbutyric acid (should be True)
        "CC(=O)CCC(O)=O",                  # 4-oxopentanoic acid (allowed for a short chain)
        "CCCCCCCCCCCCCCCC(O)=O",           # tridecanoic acid (should be True)
        "C[C@@H](O)CCCCCCCCC[C@@H](O)CC(O)=O",  # Example that should be rejected (extra –OH on non-terminal carbons)
        "CCCCCCCC[C@H]1CCC[C@@H]1CCCCCCC(O)=O",  # lactobacillic acid variant with ring (should be True now)
    ]
    for sm in test_smiles:
        result, reason = is_saturated_fatty_acid(sm)
        print(f"SMILES: {sm}\n -> {result}, Reason: {reason}\n")


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:26607',
                          'name': 'saturated fatty acid',
                          'definition': 'Any fatty acid containing no carbon '
                                        'to carbon multiple bonds. Known to '
                                        'produce adverse biological effects '
                                        'when ingested to excess.',
                          'parents': ['CHEBI:35366'],
                          'xrefs': [   'PMID:16492686',
                                       'PMID:19763019',
                                       'PMID:20237329'],
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
                                                 2,
                                                 3,
                                                 3,
                                                 3,
                                                 4,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 3,
                                                 4,
                                                 4,
                                                 4,
                                                 4,
                                                 5,
                                                 5,
                                                 5,
                                                 6,
                                                 5,
                                                 6,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 3,
                                                 2,
                                                 2,
                                                 3,
                                                 4,
                                                 4,
                                                 5,
                                                 5,
                                                 6,
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
                                                 3,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 2,
                                                 2,
                                                 3,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
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
                           'max_indent': 6,
                           'imports': ['from rdkit import Chem'],
                           'imports_count': 1,
                           'methods_called': [   'MolFromSmiles',
                                                 'MolFromSmarts',
                                                 'GetBonds',
                                                 'GetNeighbors',
                                                 'GetDegree',
                                                 'GetIdx',
                                                 'GetBondType',
                                                 'GetEndAtom',
                                                 'GetEndAtomIdx',
                                                 'GetBeginAtom',
                                                 'GetAtoms',
                                                 'GetAtomWithIdx',
                                                 'GetBondBetweenAtoms',
                                                 'GetAtomicNum',
                                                 'GetBeginAtomIdx',
                                                 'GetTotalNumHs',
                                                 'GetSubstructMatches'],
                           'methods_called_count': 17,
                           'smarts_strings': ['acid_smarts'],
                           'smarts_strings_count': 1,
                           'defs': ['is_saturated_fatty_acid(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "Contains atoms other than '
                                          'C, H, and O"',
                                          'False, "No carboxylic acid group '
                                          'found"',
                                          'False, "More than one carboxylic '
                                          'acid group found"',
                                          'False, "Contains carbon-to-carbon '
                                          'multiple bonds"',
                                          'False, "Contains additional '
                                          'carbonyl group(s) beyond the '
                                          'carboxylic acid"',
                                          'False, "Contains an alpha-hydroxyl '
                                          'group adjacent to the carboxylic '
                                          'acid"',
                                          'False, "Contains extra oxygen '
                                          'functionality that is not a '
                                          'terminal hydroxyl group"',
                                          'False, "Extra oxygen is not '
                                          'attached to a carbon"',
                                          'False, "Contains an extra hydroxyl '
                                          'group on a non-terminal carbon"',
                                          'False, "More than one terminal '
                                          'hydroxyl group found"',
                                          'True, ("Molecule has exactly one '
                                          'carboxylic acid group, only C/H/O '
                                          'atoms, no carbon–carbon multiple '
                                          'bonds, "'],
                           'returns_count': 12,
                           'complexity': 8.141906040262466},
    'message': '\n'
               'Attempt failed: F1 score of 0.25641025641025644 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: OCCCCCCCCCCCCCCCCCCCC(O)=O NAME: '
               '20-hydroxyicosanoic acid REASON: CORRECT Molecule has a single '
               'carboxylic acid group, only C/H/O atoms, no rings, no '
               'carbon–carbon unsaturation, and no disallowed additional '
               'carbonyl or alpha‐OH groups\n'
               ' * SMILES: CC(C)C(C)C(O)=O NAME: 2,3-dimethylbutyric acid '
               'REASON: CORRECT Molecule has a single carboxylic acid group, '
               'only C/H/O atoms, no rings, no carbon–carbon unsaturation, and '
               'no disallowed additional carbonyl or alpha‐OH groups\n'
               ' * SMILES: CC(=O)CCC(O)=O NAME: 4-oxopentanoic acid REASON: '
               'CORRECT Molecule has a single carboxylic acid group, only '
               'C/H/O atoms, no rings, no carbon–carbon unsaturation, and no '
               'disallowed additional carbonyl or alpha‐OH groups\n'
               ' * SMILES: CCCCCCCCCCCCC(O)=O NAME: tridecanoic acid REASON: '
               'CORRECT Molecule has a single carboxylic acid group, only '
               'C/H/O atoms, no rings, no carbon–carbon unsaturation, and no '
               'disallowed additional carbonyl or alpha‐OH groups\n'
               ' * SMILES: CC(C)CCCCCCCCCC(O)=O NAME: isotridecanoic acid '
               'REASON: CORRECT Molecule has a single carboxylic acid group, '
               'only C/H/O atoms, no rings, no carbon–carbon unsaturation, and '
               'no disallowed additional carbonyl or alpha‐OH groups\n'
               ' * SMILES: OCCCCCCCCCCCCC(O)=O NAME: 13-hydroxytridecanoic '
               'acid REASON: CORRECT Molecule has a single carboxylic acid '
               'group, only C/H/O atoms, no rings, no carbon–carbon '
               'unsaturation, and no disallowed additional carbonyl or '
               'alpha‐OH groups\n'
               ' * SMILES: CCCC(C)C(O)=O NAME: 2-methylvaleric acid REASON: '
               'CORRECT Molecule has a single carboxylic acid group, only '
               'C/H/O atoms, no rings, no carbon–carbon unsaturation, and no '
               'disallowed additional carbonyl or alpha‐OH groups\n'
               ' * SMILES: CCCCCCCCCCCCCCC[C@H](C)C(O)=O NAME: '
               '(2S)-2-methylheptadecanoic acid REASON: CORRECT Molecule has a '
               'single carboxylic acid group, only C/H/O atoms, no rings, no '
               'carbon–carbon unsaturation, and no disallowed additional '
               'carbonyl or alpha‐OH groups\n'
               ' * SMILES: CCC(C)CCCCCCCCCCC(O)=O NAME: 12-methyltetradecanoic '
               'acid REASON: CORRECT Molecule has a single carboxylic acid '
               'group, only C/H/O atoms, no rings, no carbon–carbon '
               'unsaturation, and no disallowed additional carbonyl or '
               'alpha‐OH groups\n'
               ' * SMILES: OC(CCCCCCCCCCCCCCCC(C)C)=O NAME: '
               '17-methyloctadecanoic acid REASON: CORRECT Molecule has a '
               'single carboxylic acid group, only C/H/O atoms, no rings, no '
               'carbon–carbon unsaturation, and no disallowed additional '
               'carbonyl or alpha‐OH groups\n'
               ' * SMILES: CCCCCCCCCCCCCCCC(O)=O NAME: hexadecanoic acid '
               'REASON: CORRECT Molecule has a single carboxylic acid group, '
               'only C/H/O atoms, no rings, no carbon–carbon unsaturation, and '
               'no disallowed additional carbonyl or alpha‐OH groups\n'
               ' * SMILES: OC(C)CCCCCCCCCCCCCCCCCCC(=O)O NAME: '
               '20-hydroxyhenicosanoic acid REASON: CORRECT Molecule has a '
               'single carboxylic acid group, only C/H/O atoms, no rings, no '
               'carbon–carbon unsaturation, and no disallowed additional '
               'carbonyl or alpha‐OH groups\n'
               ' * SMILES: CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC(O)=O NAME: '
               'dotriacontanoic acid REASON: CORRECT Molecule has a single '
               'carboxylic acid group, only C/H/O atoms, no rings, no '
               'carbon–carbon unsaturation, and no disallowed additional '
               'carbonyl or alpha‐OH groups\n'
               ' * SMILES: CC(C)CCCCCCCCCCCCCCCCCCC(O)=O NAME: '
               '20-methylhenicosanoic acid REASON: CORRECT Molecule has a '
               'single carboxylic acid group, only C/H/O atoms, no rings, no '
               'carbon–carbon unsaturation, and no disallowed additional '
               'carbonyl or alpha‐OH groups\n'
               ' * SMILES: C(O)(=O)CCCCCCCCC(CCC(C)C)C NAME: '
               '10,13-dimethyltetradecanoic acid REASON: CORRECT Molecule has '
               'a single carboxylic acid group, only C/H/O atoms, no rings, no '
               'carbon–carbon unsaturation, and no disallowed additional '
               'carbonyl or alpha‐OH groups\n'
               ' * SMILES: CC(C)CCCCCCCCCCC(O)=O NAME: isomyristic acid '
               'REASON: CORRECT Molecule has a single carboxylic acid group, '
               'only C/H/O atoms, no rings, no carbon–carbon unsaturation, and '
               'no disallowed additional carbonyl or alpha‐OH groups\n'
               ' * SMILES: C(CCCCCC(CCC)C)CCCCC(O)=O NAME: '
               '12-methylpentadecanoic acid REASON: CORRECT Molecule has a '
               'single carboxylic acid group, only C/H/O atoms, no rings, no '
               'carbon–carbon unsaturation, and no disallowed additional '
               'carbonyl or alpha‐OH groups\n'
               ' * SMILES: C([C@@H](CCC[C@H](CCC[C@H](CCCC(C)C)C)C)C)(=O)O '
               'NAME: (2R,6S,10S)-2,6,10,14-pristanic acid REASON: CORRECT '
               'Molecule has a single carboxylic acid group, only C/H/O atoms, '
               'no rings, no carbon–carbon unsaturation, and no disallowed '
               'additional carbonyl or alpha‐OH groups\n'
               ' * SMILES: CCC(C)C(O)=O NAME: 2-methylbutyric acid REASON: '
               'CORRECT Molecule has a single carboxylic acid group, only '
               'C/H/O atoms, no rings, no carbon–carbon unsaturation, and no '
               'disallowed additional carbonyl or alpha‐OH groups\n'
               ' * SMILES: CC(C)CCCCCCCCCCCCCCCCCCCCCCCCC(O)=O NAME: '
               '26-methylheptacosanoic acid REASON: CORRECT Molecule has a '
               'single carboxylic acid group, only C/H/O atoms, no rings, no '
               'carbon–carbon unsaturation, and no disallowed additional '
               'carbonyl or alpha‐OH groups\n'
               ' * SMILES: CCC(C)CCCCCCCCCCCCCCCCCCC(O)=O NAME: '
               '20-methyldocosanoic acid REASON: CORRECT Molecule has a single '
               'carboxylic acid group, only C/H/O atoms, no rings, no '
               'carbon–carbon unsaturation, and no disallowed additional '
               'carbonyl or alpha‐OH groups\n'
               ' * SMILES: CCC(C)CCCCCCCCCCCCCCCCC(O)=O NAME: '
               '18-methylicosanoic acid REASON: CORRECT Molecule has a single '
               'carboxylic acid group, only C/H/O atoms, no rings, no '
               'carbon–carbon unsaturation, and no disallowed additional '
               'carbonyl or alpha‐OH groups\n'
               ' * SMILES: CCC(C)CCCCCCCCCCCCCCCCCCCCC(O)=O NAME: '
               '22-methyltetracosanoic acid REASON: CORRECT Molecule has a '
               'single carboxylic acid group, only C/H/O atoms, no rings, no '
               'carbon–carbon unsaturation, and no disallowed additional '
               'carbonyl or alpha‐OH groups\n'
               ' * SMILES: CC(C)(C)CC(O)=O NAME: 3,3-dimethylbutyric acid '
               'REASON: CORRECT Molecule has a single carboxylic acid group, '
               'only C/H/O atoms, no rings, no carbon–carbon unsaturation, and '
               'no disallowed additional carbonyl or alpha‐OH groups\n'
               ' * SMILES: OCCCCCCCCCCCCCCC(O)=O NAME: 15-hydroxypentadecanoic '
               'acid REASON: CORRECT Molecule has a single carboxylic acid '
               'group, only C/H/O atoms, no rings, no carbon–carbon '
               'unsaturation, and no disallowed additional carbonyl or '
               'alpha‐OH groups\n'
               'False positives: SMILES: C[C@@H](O)CCCCCCCCC[C@@H](O)CC(O)=O '
               'NAME: (3R,13R)-3,13-dihydroxymyristic acid REASON: WRONGLY '
               'CLASSIFIED Molecule has a single carboxylic acid group, only '
               'C/H/O atoms, no rings, no carbon–carbon unsaturation, and no '
               'disallowed additional carbonyl or alpha‐OH groups\n'
               ' * SMILES: O(C(=O)CC(O)=O)C NAME: 3-Methoxy-3-oxopropanoic '
               'acid REASON: WRONGLY CLASSIFIED Molecule has a single '
               'carboxylic acid group, only C/H/O atoms, no rings, no '
               'carbon–carbon unsaturation, and no disallowed additional '
               'carbonyl or alpha‐OH groups\n'
               ' * SMILES: [H]C(=O)[C@@H](O)[C@@H](O)CC(=O)C(O)=O NAME: '
               '(4S,5S)-4,5-dihydroxy-2,6-dioxohexanoic acid REASON: WRONGLY '
               'CLASSIFIED Molecule has a single carboxylic acid group, only '
               'C/H/O atoms, no rings, no carbon–carbon unsaturation, and no '
               'disallowed additional carbonyl or alpha‐OH groups\n'
               ' * SMILES: '
               'C(O)(=O)[C@H]([C@H]([C@H](C[C@H](CCCCCCCCCCCCCCCCCC)C)C)O)C '
               'NAME: Mycolipanolic acid (C27) REASON: WRONGLY CLASSIFIED '
               'Molecule has a single carboxylic acid group, only C/H/O atoms, '
               'no rings, no carbon–carbon unsaturation, and no disallowed '
               'additional carbonyl or alpha‐OH groups\n'
               ' * SMILES: OC(=O)CCC(CCCCCCCC(C)C)C NAME: '
               '4,12-dimethyl-tridecanoic acid REASON: WRONGLY CLASSIFIED '
               'Molecule has a single carboxylic acid group, only C/H/O atoms, '
               'no rings, no carbon–carbon unsaturation, and no disallowed '
               'additional carbonyl or alpha‐OH groups\n'
               ' * SMILES: OC(=O)CCCCCCCCCC(CCCCC)C NAME: '
               '11-methyl-hexadecanoic acid REASON: WRONGLY CLASSIFIED '
               'Molecule has a single carboxylic acid group, only C/H/O atoms, '
               'no rings, no carbon–carbon unsaturation, and no disallowed '
               'additional carbonyl or alpha‐OH groups\n'
               ' * SMILES: OC(=O)C(CCC(CCCCCCC)C)C NAME: '
               '2,5-dimethyl-dodecanoic acid REASON: WRONGLY CLASSIFIED '
               'Molecule has a single carboxylic acid group, only C/H/O atoms, '
               'no rings, no carbon–carbon unsaturation, and no disallowed '
               'additional carbonyl or alpha‐OH groups\n'
               ' * SMILES: OC(=O)C[C@@H](C[C@H](CCCCCCC)C)C NAME: '
               '3R,5S-Dimethyldodecanoic acid REASON: WRONGLY CLASSIFIED '
               'Molecule has a single carboxylic acid group, only C/H/O atoms, '
               'no rings, no carbon–carbon unsaturation, and no disallowed '
               'additional carbonyl or alpha‐OH groups\n'
               ' * SMILES: OC(=O)CC(CC(CCCCCCCCC)C)C NAME: '
               '3,5-dimethyl-tetradecanoic acid REASON: WRONGLY CLASSIFIED '
               'Molecule has a single carboxylic acid group, only C/H/O atoms, '
               'no rings, no carbon–carbon unsaturation, and no disallowed '
               'additional carbonyl or alpha‐OH groups\n'
               ' * SMILES: CCCCC[C@H](O)CCCCCCCCCC(O)=O NAME: jalapinolic acid '
               'REASON: WRONGLY CLASSIFIED Molecule has a single carboxylic '
               'acid group, only C/H/O atoms, no rings, no carbon–carbon '
               'unsaturation, and no disallowed additional carbonyl or '
               'alpha‐OH groups\n'
               ' * SMILES: OC[C@@H](C)C(O)=O NAME: (R)-3-Hydroxyisobutyric '
               'acid REASON: WRONGLY CLASSIFIED Molecule has a single '
               'carboxylic acid group, only C/H/O atoms, no rings, no '
               'carbon–carbon unsaturation, and no disallowed additional '
               'carbonyl or alpha‐OH groups\n'
               ' * SMILES: O(C(OCC)C)C(C)C(O)=O NAME: '
               '2-(1-Ethoxyethoxy)propanoic acid REASON: WRONGLY CLASSIFIED '
               'Molecule has a single carboxylic acid group, only C/H/O atoms, '
               'no rings, no carbon–carbon unsaturation, and no disallowed '
               'additional carbonyl or alpha‐OH groups\n'
               ' * SMILES: OCCCCCCCCCCCCCCCC(O)CC(O)=O NAME: '
               '3,18-dihydroxyoctadecanoic acid REASON: WRONGLY CLASSIFIED '
               'Molecule has a single carboxylic acid group, only C/H/O atoms, '
               'no rings, no carbon–carbon unsaturation, and no disallowed '
               'additional carbonyl or alpha‐OH groups\n'
               ' * SMILES: O=C(O)C[C@@H](OC)CCCCCCCCCCCCCCCCCCCCC NAME: '
               '3-Methoxytetracosanoic acid REASON: WRONGLY CLASSIFIED '
               'Molecule has a single carboxylic acid group, only C/H/O atoms, '
               'no rings, no carbon–carbon unsaturation, and no disallowed '
               'additional carbonyl or alpha‐OH groups\n'
               ' * SMILES: OCCCCCCCCCCCCCCCC[C@@H](O)CC(O)=O NAME: '
               '(3R)-3,19-dihydroxynonadecanoic acid REASON: WRONGLY '
               'CLASSIFIED Molecule has a single carboxylic acid group, only '
               'C/H/O atoms, no rings, no carbon–carbon unsaturation, and no '
               'disallowed additional carbonyl or alpha‐OH groups\n'
               ' * SMILES: OC(=O)CCCCC(CCCCCCCC(CCCC)C)C NAME: '
               '6,14-dimethyl-octadecanoic acid REASON: WRONGLY CLASSIFIED '
               'Molecule has a single carboxylic acid group, only C/H/O atoms, '
               'no rings, no carbon–carbon unsaturation, and no disallowed '
               'additional carbonyl or alpha‐OH groups\n'
               ' * SMILES: CC(O)CCCCCCCCCCCCCC(O)=O NAME: 15-hydroxypalmitic '
               'acid REASON: WRONGLY CLASSIFIED Molecule has a single '
               'carboxylic acid group, only C/H/O atoms, no rings, no '
               'carbon–carbon unsaturation, and no disallowed additional '
               'carbonyl or alpha‐OH groups\n'
               ' * SMILES: OC(=O)CCC(CC(CCC)C)C NAME: 4,6-Dimethylnonanoic '
               'acid REASON: WRONGLY CLASSIFIED Molecule has a single '
               'carboxylic acid group, only C/H/O atoms, no rings, no '
               'carbon–carbon unsaturation, and no disallowed additional '
               'carbonyl or alpha‐OH groups\n'
               ' * SMILES: CCCC(=O)CC(O)=O NAME: 3-oxohexanoic acid REASON: '
               'WRONGLY CLASSIFIED Molecule has a single carboxylic acid '
               'group, only C/H/O atoms, no rings, no carbon–carbon '
               'unsaturation, and no disallowed additional carbonyl or '
               'alpha‐OH groups\n'
               ' * SMILES: OC(CCC(O)=O)C NAME: 4-hydroxy-valeric acid REASON: '
               'WRONGLY CLASSIFIED Molecule has a single carboxylic acid '
               'group, only C/H/O atoms, no rings, no carbon–carbon '
               'unsaturation, and no disallowed additional carbonyl or '
               'alpha‐OH groups\n'
               ' * SMILES: O(C(CCCCCCCCCC(O)=O)CCCCCCC)C NAME: '
               '11-methoxy-octadecanoic acid REASON: WRONGLY CLASSIFIED '
               'Molecule has a single carboxylic acid group, only C/H/O atoms, '
               'no rings, no carbon–carbon unsaturation, and no disallowed '
               'additional carbonyl or alpha‐OH groups\n'
               ' * SMILES: CCCCCCCCCCCCC(C)(O)C(O)CC(O)=O NAME: '
               '3,4-dihydroxy-4-methylhexadecanoic acid REASON: WRONGLY '
               'CLASSIFIED Molecule has a single carboxylic acid group, only '
               'C/H/O atoms, no rings, no carbon–carbon unsaturation, and no '
               'disallowed additional carbonyl or alpha‐OH groups\n'
               ' * SMILES: OC(=O)[C@@H](C[C@@H](CCCCCCCCCCCCCCCCCC)C)C NAME: '
               'Mycocerosic acid (C24) REASON: WRONGLY CLASSIFIED Molecule has '
               'a single carboxylic acid group, only C/H/O atoms, no rings, no '
               'carbon–carbon unsaturation, and no disallowed additional '
               'carbonyl or alpha‐OH groups\n'
               ' * SMILES: OC(=O)CC(CCCCCCCCCCC)C NAME: 3-methyl-tetradecanoic '
               'acid REASON: WRONGLY CLASSIFIED Molecule has a single '
               'carboxylic acid group, only C/H/O atoms, no rings, no '
               'carbon–carbon unsaturation, and no disallowed additional '
               'carbonyl or alpha‐OH groups\n'
               ' * SMILES: OC(=O)C(CC)(CC)C NAME: 2-ethyl-2-methyl-butanoic '
               'acid REASON: WRONGLY CLASSIFIED Molecule has a single '
               'carboxylic acid group, only C/H/O atoms, no rings, no '
               'carbon–carbon unsaturation, and no disallowed additional '
               'carbonyl or alpha‐OH groups\n'
               'False negatives: SMILES: CCCCCC[C@H]1C[C@H]1CCCCCCCCCC(O)=O '
               'NAME: lactobacillic acid REASON: MISSED Contains ring '
               'structures\n'
               ' * SMILES: CCCCCCCC[C@H]1CCC[C@@H]1CCCCCCC(O)=O NAME: '
               'prostanoic acid REASON: MISSED Contains ring structures\n'
               ' * SMILES: '
               '[C@@]12([C@]3([C@@]([C@]1([C@@]4(CC[C@]24[H])[H])[H])([C@]5([C@@]3(C[C@@H]5CCCCCCCC(O)=O)[H])[H])[H])[H])[H] '
               'NAME: (+)-pentacycloanammoxic acid REASON: MISSED Contains '
               'ring structures\n'
               ' * SMILES: CCCCCCC1CC1CCCCCCCCCC(O)=O NAME: '
               '11,12-methyleneoctadecanoic acid REASON: MISSED Contains ring '
               'structures\n'
               ' * SMILES: '
               'C(C[N+](C)(C)C)OP(=O)([O-])OC[C@H](OC)COC(CCCCCCCCCCCCCCC)=O '
               'NAME: 1-hexadecanoyl-2-methyl-sn-glycero-3-phosphocholine '
               'REASON: MISSED Contains atoms other than C, H, and O\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'C1=CC=C2C(=C1)C(=O)C3=CC=CC=C3C2(CC4=CC(=NC=C4)F)CC5=CC(=NC=C5)F',
                                     'name': '10,10-bis[(2-fluoro-4-pyridinyl)methyl]-9-anthracenone',
                                     'reason': 'Contains atoms other than C, '
                                               'H, and O'},
                                 {   'smiles': 'C[C@@H](C1=CC=CC=C1)NC(=O)[C@@H]2[C@H]([C@@H]3CN4C(=CC=C(C4=O)C5=CC=CC=C5F)[C@H]2N3C)CO',
                                     'name': 'LSM-10936',
                                     'reason': 'Contains atoms other than C, '
                                               'H, and O'},
                                 {   'smiles': '[H]C(=CC(=O)C(O)=O)C(CC(O)=O)C(O)=O',
                                     'name': '5-oxopent-3-ene-1,2,5-tricarboxylic '
                                             'acid',
                                     'reason': 'More than one carboxylic acid '
                                               'group found'},
                                 {   'smiles': 'S1N(C2=CC=C(C=C2)C(OCC)=O)C(=O)C=C1',
                                     'name': 'ethyl '
                                             '4-(3-oxo-2,3-dihydroisothiazol-2-yl)benzoate',
                                     'reason': 'Contains atoms other than C, '
                                               'H, and O'},
                                 {   'smiles': 'COc1cc(O)c2c(c1)oc1c(O)cccc1c2=O',
                                     'name': 'mesuaxanthone A',
                                     'reason': 'No carboxylic acid group '
                                               'found'},
                                 {   'smiles': 'O([C@@H]1[C@H](O)[C@@H](O[C@@H]([C@H]1O)CO[C@H]2O[C@@H]([C@@H](O)[C@H](O)[C@@H]2O[C@@H]3O[C@@H]([C@@H](O)[C@H](O)[C@H]3NC(=O)C)CO)CO[C@@H]4O[C@@H]([C@@H](O)[C@H](O)[C@H]4NC(=O)C)CO)O[C@H]5[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]5CO)O[C@H]6[C@H](O)[C@@H](NC(=O)C)C(O[C@@H]6CO)O)[C@H]7O[C@@H]([C@@H](O[C@@H]8O[C@@H]([C@@H](O)[C@H](O)[C@H]8NC(=O)C)CO)[C@H](O)[C@@H]7O[C@@H]9O[C@@H]([C@@H](O[C@@H]%10O[C@@H]([C@H](O)[C@H](O)[C@H]%10O)CO)[C@H](O)[C@H]9NC(=O)C)CO)CO',
                                     'name': 'N-[(3R,4R,5S,6R)-5-[(2S,3R,4R,5S,6R)-3-Acetamido-5-[(2S,3S,4S,5R,6R)-6-[[(2S,3S,4S,5S,6R)-3-[(2R,3R,4R,5S,6R)-3-acetamido-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-6-[[(2R,3R,4R,5S,6R)-3-acetamido-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxymethyl]-4,5-dihydroxyoxan-2-yl]oxymethyl]-4-[(2R,3S,4S,5S,6R)-5-[(2R,3R,4R,5S,6R)-3-acetamido-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-3-[(2S,3R,4R,5S,6R)-3-acetamido-4-hydroxy-6-(hydroxymethyl)-5-[(2S,3R,4S,5R,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-3,5-dihydroxyoxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-2,4-dihydroxy-6-(hydroxymethyl)oxan-3-yl]acetamide',
                                     'reason': 'Contains atoms other than C, '
                                               'H, and O'},
                                 {   'smiles': 'CCCCCCCC\\C=C/CCCCCCCC(=O)OC[C@H](COP([O-])(=O)OC[C@H]([NH3+])C([O-])=O)OC(=O)CCC\\C=C/C\\C=C/C\\C=C/C\\C=C/CCCCC',
                                     'name': '1-oleoyl-2-arachidonoyl-sn-glycero-3-phospho-L-serine(1-)',
                                     'reason': 'Contains atoms other than C, '
                                               'H, and O'},
                                 {   'smiles': 'OC(=Cc1ccccc1)C([O-])=O',
                                     'name': 'enol-phenylpyruvate',
                                     'reason': 'No carboxylic acid group '
                                               'found'},
                                 {   'smiles': '[H][C@]1(CC[C@]2(C)[C@@H](O)CCC(=C)[C@@]12[H])[C@@H](O)C(C)C',
                                     'name': '(1R,3aS,4S,7aR)-1-((S)-1-hydroxy-2-methylpropyl)-3a-methyl-7-methyleneoctahydro-1H-inden-4-ol',
                                     'reason': 'No carboxylic acid group '
                                               'found'},
                                 {   'smiles': 'O1C(C(O)C(O)C(O)C1CO)C=2C(=O)C=3C(O)=C(C4OC(C(O)C(O)C4O)CO)C(O)=CC3OC2C5=CC=C(OC)C=C5',
                                     'name': "3,6-Diglucopyranosyl-5,7-dihydroxy-4'-methoxyflavone",
                                     'reason': 'No carboxylic acid group '
                                               'found'}],
    'sample_false_negatives': [   {   'smiles': 'CC(=O)CCC(O)=O',
                                      'name': '4-oxopentanoic acid',
                                      'reason': 'Contains extra oxygen '
                                                'functionality that is not a '
                                                'terminal hydroxyl group'},
                                  {   'smiles': 'OC(C)CCCCCCCCCCCCCCCCCCC(=O)O',
                                      'name': '20-hydroxyhenicosanoic acid',
                                      'reason': 'Contains an extra hydroxyl '
                                                'group on a non-terminal '
                                                'carbon'},
                                  {   'smiles': 'C(CCCCCCCCCCCCCCC(O)=O)CCC(C)O',
                                      'name': '19-hydroxyicosanoic acid',
                                      'reason': 'Contains an extra hydroxyl '
                                                'group on a non-terminal '
                                                'carbon'},
                                  {   'smiles': 'C[C@@H](O)CCCCCCCCCCCCCCCCCCC(O)=O',
                                      'name': '(20R)-20-hydroxyhenicosanoic '
                                              'acid',
                                      'reason': 'Contains an extra hydroxyl '
                                                'group on a non-terminal '
                                                'carbon'},
                                  {   'smiles': 'C(C[N+](C)(C)C)OP(=O)([O-])OC[C@H](OC)COC(CCCCCCCCCCCCCCC)=O',
                                      'name': '1-hexadecanoyl-2-methyl-sn-glycero-3-phosphocholine',
                                      'reason': 'Contains atoms other than C, '
                                                'H, and O'}],
    'attempt': 3,
    'reasoning': 'Below is one complete Python solution. In my reasoning I '
                 're‐examined the previous code and the outcomes. In the '
                 'previous version the following problems were noted:\n'
                 '\n'
                 '• It rejected molecules that contained rings—even though '
                 'many “saturated fatty acids” (such as certain '
                 'cyclopropane‐containing acids) are considered valid if they '
                 'do not have any C–C multiple bonds.\n'
                 '\n'
                 '• It did not “look” closely enough at any oxygen outside the '
                 'carboxylic acid group. Many false positives were compounds '
                 'that contained “extra” –OH or keto groups (for long chains) '
                 'at positions other than the terminal (ω) end. In our '
                 'improved version, if additional carbonyl groups occur in '
                 'long chain (≥7 carbon) molecules they are rejected, and only '
                 'one extra –OH (on a terminal carbon only) is allowed.\n'
                 '\n'
                 '• The check for an “alpha‐OH” substituent adjacent to the '
                 'carboxylic acid was maintained.\n'
                 '\n'
                 'The following code reflects these improvements: \n'
                 '\u2003\n'
                 '------------------------------------------------',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 85,
    'num_false_positives': 268,
    'num_true_negatives': 141942,
    'num_false_negatives': 5,
    'num_negatives': None,
    'precision': 0.24079320113314448,
    'recall': 0.9444444444444444,
    'f1': 0.3837471783295711,
    'accuracy': 0.9980815179198875,
    'negative_predictive_value': 0.9999647755852537}