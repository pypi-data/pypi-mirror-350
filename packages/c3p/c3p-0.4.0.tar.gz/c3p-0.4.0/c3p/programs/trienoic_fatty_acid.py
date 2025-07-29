"""
Classifies: CHEBI:73155 trienoic fatty acid
"""
"""
Classifies: Trienoic fatty acid
Definition: A free (terminal) carboxylic acid with a long, acyclic (unbranched) acyl chain
that contains exactly three carbon–carbon double bonds. In addition, the three double bonds 
should occur in a methylene‐interrupted pattern (i.e. not directly conjugated).
"""

from rdkit import Chem
from rdkit.Chem import rdMolDescriptors

def is_trienoic_fatty_acid(smiles: str):
    """
    Determines if a molecule is a trienoic fatty acid based on its SMILES string.
    The criteria are:
      1. The molecule must be valid.
      2. It must contain exactly one free carboxylic acid group (SMARTS "[CX3](=O)[OX2H1]"),
         where the acid carbon is terminal (bonded to exactly one carbon).
      3. Starting from the acid carbon, the acyl chain is extracted by following the unique
         carbon neighbor (i.e. the chain must be linear and unbranched).
      4. The extracted (acyclic) chain must be sufficiently long (here at least 10 carbons)
         and contain exactly three C=C bonds.
      5. The double bonds must be “methylene‐interrupted” (i.e. no two double bonds occur
         on consecutive bonds along the fatty acyl chain).
      6. The molecular weight must be above a minimal threshold.
    
    Args:
        smiles (str): SMILES string of the molecule.
    
    Returns:
        bool: True if the molecule meets the trienoic fatty acid criteria, False otherwise.
        str: A short reason message.
    """
    # 1. Parse SMILES.
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
    
    # 2. Look for a free carboxylic acid group.
    # SMARTS: carbonyl carbon attached to [OX2H1]
    ca_smarts = "[CX3](=O)[OX2H1]"
    ca_group = Chem.MolFromSmarts(ca_smarts)
    ca_matches = mol.GetSubstructMatches(ca_group)
    if len(ca_matches) == 0:
        return False, "Missing carboxylic acid functional group (COOH)"
    if len(ca_matches) > 1:
        return False, f"Found {len(ca_matches)} carboxylic acid groups; requires exactly 1"
    
    # In the SMARTS, the acid carbon is the first atom.
    acid_carbon_idx = ca_matches[0][0]
    acid_carbon = mol.GetAtomWithIdx(acid_carbon_idx)
    # 2a. Ensure the acid carbon is terminal: it must have exactly one carbon neighbor.
    carbon_neighbors = [nbr for nbr in acid_carbon.GetNeighbors() if nbr.GetAtomicNum() == 6]
    if len(carbon_neighbors) != 1:
        return False, "Carboxylic acid group is not terminal (acid carbon must be bonded to exactly one carbon)"
    
    # 3. Extract the linear acyl chain.
    # Instead of a DFS that may pick a branched route, we follow the unique neighbor chain.
    # Typically, in fatty acids the chain is unbranched. (Branches lead to false hits.)
    chain_atoms = []  # will hold atom indices of the acyl chain (starting at the alpha carbon)
    double_bond_count = 0  # count bonds that are C=C (in the chain)
    double_bond_positions = []  # positions (in chain; bond between chain[i] and chain[i+1])
    
    # Start from the unique neighbor (first carbon of the chain)
    current_atom = carbon_neighbors[0]
    prev_atom = acid_carbon  # To avoid going back
    chain_atoms.append(current_atom.GetIdx())
    # Check the bond between acid group carbon and this carbon (normally not double)
    bond = mol.GetBondBetweenAtoms(prev_atom.GetIdx(), current_atom.GetIdx())
    # (We ignore any unsaturation here, assuming the acid carbon is part of the COOH group.)
    
    # Now iteratively follow the chain.
    pos = 0  # position in the chain list (0 means the bond from acid to first chain carbon is not counted)
    while True:
        # Get carbon neighbors of current_atom except the one we came from.
        nbrs = [nbr for nbr in current_atom.GetNeighbors() if nbr.GetAtomicNum() == 6 and nbr.GetIdx() != prev_atom.GetIdx()]
        # If more than one, the chain is branched.
        if len(nbrs) > 1:
            return False, f"Acyl chain is branched at atom index {current_atom.GetIdx()}; fatty acid chain must be linear"
        if len(nbrs) == 0:
            # End of chain reached.
            break
        # Otherwise, there is exactly one next carbon.
        next_atom = nbrs[0]
        # Check the bond between current_atom and next_atom
        bond = mol.GetBondBetweenAtoms(current_atom.GetIdx(), next_atom.GetIdx())
        if bond is None:
            return False, "Unexpected error: missing bond in acyl chain"
        # If it is a double bond, count it.
        if bond.GetBondType() == Chem.rdchem.BondType.DOUBLE:
            double_bond_count += 1
            double_bond_positions.append(pos)
        # Append next_atom to the chain.
        chain_atoms.append(next_atom.GetIdx())
        # Update for next iteration.
        prev_atom = current_atom
        current_atom = next_atom
        pos += 1
    
    # 4. Require that the chain is long enough.
    if len(chain_atoms) < 10:
        return False, f"Acyl chain too short ({len(chain_atoms)} carbons); must be a long-chain fatty acid"
    
    # 5. The chain must be fully acyclic. (Given the linear follow above and no branching,
    #    we already reject ring participation via branching. But double-check: none of the atoms
    #    in the chain should be in a ring.)
    for idx in chain_atoms:
        if mol.GetAtomWithIdx(idx).IsInRing():
            return False, "Acyl chain contains rings; fatty acid chain must be acyclic"
    
    # 6. There must be exactly three carbon–carbon double bonds along the acyl chain.
    if double_bond_count != 3:
        return False, f"Found {double_bond_count} C=C double bonds along the acyl chain; requires exactly 3 for a trienoic fatty acid"
    
    # 7. Verify that the double bonds occur in a methylene‐interrupted pattern.
    # That is, if d0, d1, d2 are the positions (in our chain, where bond between chain[i] and chain[i+1])
    # then we require that consecutive double bond positions differ by at least 2.
    if len(double_bond_positions) >= 2:
        for i in range(1, len(double_bond_positions)):
            if (double_bond_positions[i] - double_bond_positions[i-1]) < 2:
                return False, "Double bonds are conjugated; they must be separated by a methylene group"
    
    # 8. Overall molecular weight check.
    mol_wt = rdMolDescriptors.CalcExactMolWt(mol)
    if mol_wt < 180:
        return False, f"Molecular weight ({mol_wt:.1f} Da) too low for a fatty acid"
    
    return True, ("Contains one free, terminal carboxylic acid group and an acyclic, unbranched acyl chain "
                  "with exactly 3 C=C bonds in a methylene‐interrupted pattern typical of trienoic fatty acids")

# Example usage (for testing):
if __name__ == '__main__':
    # Test with one example: 10,12,14-octadecatrienoic acid.
    test_smiles = "OC(=O)CCCCCCCC/C=C/C=C/C=C/CCC"
    result, reason = is_trienoic_fatty_acid(test_smiles)
    print(result, reason)


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:73155',
                          'name': 'trienoic fatty acid',
                          'definition': 'Any polyunsaturated fatty acid that '
                                        'contains three double bonds.',
                          'parents': ['CHEBI:26208', 'CHEBI:53339'],
                          'xrefs': ['PMID:11115886'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 108,
                           'log_lines_of_code': 4.68213122712422,
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
                                                 2,
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
                                                 2,
                                                 2,
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
                                                 3,
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
                                                 3,
                                                 4,
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
                                                 1],
                           'max_indent': 4,
                           'imports': [   'from rdkit import Chem',
                                          'from rdkit.Chem import '
                                          'rdMolDescriptors'],
                           'imports_count': 2,
                           'methods_called': [   'IsInRing',
                                                 'GetBondType',
                                                 'append',
                                                 'MolFromSmarts',
                                                 'CalcExactMolWt',
                                                 'GetAtomWithIdx',
                                                 'GetSubstructMatches',
                                                 'GetAtomicNum',
                                                 'GetBondBetweenAtoms',
                                                 'GetNeighbors',
                                                 'MolFromSmiles',
                                                 'GetIdx'],
                           'methods_called_count': 12,
                           'smarts_strings': ['ca_smarts'],
                           'smarts_strings_count': 1,
                           'defs': ['is_trienoic_fatty_acid(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "Missing carboxylic acid '
                                          'functional group (COOH)"',
                                          'False, f"Found {len(ca_matches)} '
                                          'carboxylic acid groups; requires '
                                          'exactly 1"',
                                          'False, "Carboxylic acid group is '
                                          'not terminal (acid carbon must be '
                                          'bonded to exactly one carbon)"',
                                          'False, f"Acyl chain is branched at '
                                          'atom index {current_atom.GetIdx()}; '
                                          'fatty acid chain must be linear"',
                                          'False, "Unexpected error: missing '
                                          'bond in acyl chain"',
                                          'False, f"Acyl chain too short '
                                          '({len(chain_atoms)} carbons); must '
                                          'be a long-chain fatty acid"',
                                          'False, "Acyl chain contains rings; '
                                          'fatty acid chain must be acyclic"',
                                          'False, f"Found {double_bond_count} '
                                          'C=C double bonds along the acyl '
                                          'chain; requires exactly 3 for a '
                                          'trienoic fatty acid"',
                                          'False, "Double bonds are '
                                          'conjugated; they must be separated '
                                          'by a methylene group"',
                                          'False, f"Molecular weight '
                                          '({mol_wt:.1f} Da) too low for a '
                                          'fatty acid"',
                                          'True, ("Contains one free, terminal '
                                          'carboxylic acid group and an '
                                          'acyclic, unbranched acyl chain "'],
                           'returns_count': 12,
                           'complexity': 6.736426245424843},
    'message': '\n'
               'Attempt failed: F1 score of 0.611764705882353 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: '
               'C(CCCCCCC/C=C\\[C@H](/C=C\\C/C=C\\CC)OO)(=O)O NAME: '
               '(9Z,11R,12Z,15Z)-11-hydroperoxyoctadecatrienoic acid REASON: '
               'CORRECT Contains one free, terminal carboxylic acid group and '
               'a long acyclic acyl chain with exactly 3 carbon–carbon double '
               'bonds typical of trienoic fatty acids\n'
               ' * SMILES: CC\\C=C/C\\C=C/C=C/[C@@H](CCCCCCCC(O)=O)OO NAME: '
               '(9R,10E,12Z,15Z)-9-hydroperoxyoctadeca-10,12,15-trienoic acid '
               'REASON: CORRECT Contains one free, terminal carboxylic acid '
               'group and a long acyclic acyl chain with exactly 3 '
               'carbon–carbon double bonds typical of trienoic fatty acids\n'
               ' * SMILES: OC(=O)CCCCCCCC/C=C/C=C/C=C/CCC NAME: '
               '10,12,14-octadecatrienoic acid REASON: CORRECT Contains one '
               'free, terminal carboxylic acid group and a long acyclic acyl '
               'chain with exactly 3 carbon–carbon double bonds typical of '
               'trienoic fatty acids\n'
               ' * SMILES: CCCCC\\C=C/C\\C=C/C\\C=C/CCCCC(O)=O NAME: '
               'gamma-linolenic acid REASON: CORRECT Contains one free, '
               'terminal carboxylic acid group and a long acyclic acyl chain '
               'with exactly 3 carbon–carbon double bonds typical of trienoic '
               'fatty acids\n'
               ' * SMILES: OC(=O)CCCCCCC/C=C\\C/C=C\\C/C=C/CC NAME: '
               '9Z,12Z,15E-octadecatrienoic acid REASON: CORRECT Contains one '
               'free, terminal carboxylic acid group and a long acyclic acyl '
               'chain with exactly 3 carbon–carbon double bonds typical of '
               'trienoic fatty acids\n'
               ' * SMILES: C(CC=[C@]=C(CCCC(O)=O)[H])CCCCCC\\C=C\\C NAME: '
               '(S)-lamenallenic acid REASON: CORRECT Contains one free, '
               'terminal carboxylic acid group and a long acyclic acyl chain '
               'with exactly 3 carbon–carbon double bonds typical of trienoic '
               'fatty acids\n'
               ' * SMILES: OC(=O)CCCCCCC/C=C\\C\\C=C\\C=C\\C(OO)CC NAME: '
               '16-HpOTrE REASON: CORRECT Contains one free, terminal '
               'carboxylic acid group and a long acyclic acyl chain with '
               'exactly 3 carbon–carbon double bonds typical of trienoic fatty '
               'acids\n'
               ' * SMILES: CCCCCCCC[C@H](OO)\\C=C\\C=C/C\\C=C/CCCC(O)=O NAME: '
               '12(S)-HPE(5,8,10)TrE REASON: CORRECT Contains one free, '
               'terminal carboxylic acid group and a long acyclic acyl chain '
               'with exactly 3 carbon–carbon double bonds typical of trienoic '
               'fatty acids\n'
               ' * SMILES: CCCCC\\C=C/C\\C=C/CCCC\\C=C/CCCC(O)=O NAME: '
               '(5Z,11Z,14Z)-icosatrienoic acid REASON: CORRECT Contains one '
               'free, terminal carboxylic acid group and a long acyclic acyl '
               'chain with exactly 3 carbon–carbon double bonds typical of '
               'trienoic fatty acids\n'
               ' * SMILES: C(CCC(O)=O)CCC\\C=C/C=C/[C@H](C/C=C\\CCCCC)O NAME: '
               '12(S)-HETrE REASON: CORRECT Contains one free, terminal '
               'carboxylic acid group and a long acyclic acyl chain with '
               'exactly 3 carbon–carbon double bonds typical of trienoic fatty '
               'acids\n'
               ' * SMILES: OC(=O)CCCC#CCC=CCC=CCC=CCCCCC NAME: '
               '8,11,14-icosatrien-5-ynoic acid REASON: CORRECT Contains one '
               'free, terminal carboxylic acid group and a long acyclic acyl '
               'chain with exactly 3 carbon–carbon double bonds typical of '
               'trienoic fatty acids\n'
               ' * SMILES: '
               'C(CCC)C[C@H]([C@@H](C/C=C\\C/C=C\\C/C=C\\CCCC(O)=O)O)O NAME: '
               '(5Z,8Z,11Z,14R,15R)-14,15-dihydroxyicosatrienoic acid REASON: '
               'CORRECT Contains one free, terminal carboxylic acid group and '
               'a long acyclic acyl chain with exactly 3 carbon–carbon double '
               'bonds typical of trienoic fatty acids\n'
               ' * SMILES: O[C@@H]([C@H](O)/C=C\\C=C\\CCCCC(O)=O)/C=C\\CCCCC '
               'NAME: Dihydroxy-octadecatrienoate REASON: CORRECT Contains one '
               'free, terminal carboxylic acid group and a long acyclic acyl '
               'chain with exactly 3 carbon–carbon double bonds typical of '
               'trienoic fatty acids\n'
               ' * SMILES: C(CCC(O)=O)CCCCCC/C=C\\C/C=C\\C/C=C\\CC NAME: '
               'all-cis-icosa-11,14,17-trienoic acid REASON: CORRECT Contains '
               'one free, terminal carboxylic acid group and a long acyclic '
               'acyl chain with exactly 3 carbon–carbon double bonds typical '
               'of trienoic fatty acids\n'
               ' * SMILES: [H]C(C)=CCCC([H])=CCCC([H])=CC(O)=O NAME: '
               'dodeca-2,6,10-trienoic acid REASON: CORRECT Contains one free, '
               'terminal carboxylic acid group and a long acyclic acyl chain '
               'with exactly 3 carbon–carbon double bonds typical of trienoic '
               'fatty acids\n'
               ' * SMILES: '
               'C(CCC)C/C=C\\C[C@@H]([C@H](C/C=C\\C/C=C\\CCCC(O)=O)O)O NAME: '
               '(5Z,8Z,11S,12S,14Z)-11,12-dihydroxyicosatrienoic acid REASON: '
               'CORRECT Contains one free, terminal carboxylic acid group and '
               'a long acyclic acyl chain with exactly 3 carbon–carbon double '
               'bonds typical of trienoic fatty acids\n'
               ' * SMILES: OC(=O)CCCCC/C=C\\C=C/C/C=C\\CCCCC NAME: '
               '7Z,9Z,12Z-octadecatrienoic acid REASON: CORRECT Contains one '
               'free, terminal carboxylic acid group and a long acyclic acyl '
               'chain with exactly 3 carbon–carbon double bonds typical of '
               'trienoic fatty acids\n'
               ' * SMILES: CC/C=C/C/C=C/C=C/C(CCCCCCCC(=O)O)O NAME: '
               '(9S,10E,12Z,15Z)-9-Hydroxy-10,12,15-octadecatrienoic acid '
               'REASON: CORRECT Contains one free, terminal carboxylic acid '
               'group and a long acyclic acyl chain with exactly 3 '
               'carbon–carbon double bonds typical of trienoic fatty acids\n'
               ' * SMILES: OC(=O)CCCCCC/C=C/C=C/C=C/CCCCC NAME: beta-calendic '
               'acid REASON: CORRECT Contains one free, terminal carboxylic '
               'acid group and a long acyclic acyl chain with exactly 3 '
               'carbon–carbon double bonds typical of trienoic fatty acids\n'
               ' * SMILES: CCCC\\C=C/C=C/C=C\\CCCCCCCC(O)=O NAME: '
               '(9Z,11E,13Z)-octadecatrienoic acid REASON: CORRECT Contains '
               'one free, terminal carboxylic acid group and a long acyclic '
               'acyl chain with exactly 3 carbon–carbon double bonds typical '
               'of trienoic fatty acids\n'
               ' * SMILES: C(\\C=C/CCCCCCCC(=O)O)=C/C(C/C=C\\CC)OO NAME: '
               '(9Z,11E,15Z)-13-hydroperoxyoctadecatrienoic acid REASON: '
               'CORRECT Contains one free, terminal carboxylic acid group and '
               'a long acyclic acyl chain with exactly 3 carbon–carbon double '
               'bonds typical of trienoic fatty acids\n'
               ' * SMILES: '
               'CCCCC[C@H](O)CC\\C=C/C=C/C=C/[C@@H](O)[C@@H](O)CCCC(O)=O NAME: '
               '13,14-dihydrolipoxin A4 REASON: CORRECT Contains one free, '
               'terminal carboxylic acid group and a long acyclic acyl chain '
               'with exactly 3 carbon–carbon double bonds typical of trienoic '
               'fatty acids\n'
               ' * SMILES: CCC=CCC=CCC=CCCCCCCCC(=O)O NAME: '
               'octadeca-9,12,15-trienoic acid REASON: CORRECT Contains one '
               'free, terminal carboxylic acid group and a long acyclic acyl '
               'chain with exactly 3 carbon–carbon double bonds typical of '
               'trienoic fatty acids\n'
               ' * SMILES: [H]C(CCC)=CCC=C([H])C=C([H])CCCCCCCC(O)=O NAME: '
               '9,11,14-octadecatrienoic acid REASON: CORRECT Contains one '
               'free, terminal carboxylic acid group and a long acyclic acyl '
               'chain with exactly 3 carbon–carbon double bonds typical of '
               'trienoic fatty acids\n'
               ' * SMILES: O(O)C(CCCCCCCC(O)=O)/C=C/C=C/C/C=C\\CC NAME: '
               '9-HpOTrE REASON: CORRECT Contains one free, terminal '
               'carboxylic acid group and a long acyclic acyl chain with '
               'exactly 3 carbon–carbon double bonds typical of trienoic fatty '
               'acids\n'
               'False positives: SMILES: '
               'CCCCCC/C=C\\C/C=C\\C/C=C\\CCCCCCCC(O)=O NAME: Vaneic acid '
               'REASON: WRONGLY CLASSIFIED Contains one free, terminal '
               'carboxylic acid group and a long acyclic acyl chain with '
               'exactly 3 carbon–carbon double bonds typical of trienoic fatty '
               'acids\n'
               ' * SMILES: CC\\C=C/C\\C=C/C\\C=C/CCCCCCCCCCCC(O)=O NAME: '
               '(13Z,16Z,19Z)-docosatrienoic acid REASON: WRONGLY CLASSIFIED '
               'Contains one free, terminal carboxylic acid group and a long '
               'acyclic acyl chain with exactly 3 carbon–carbon double bonds '
               'typical of trienoic fatty acids\n'
               ' * SMILES: CCCCC[C@H](O)\\C=C\\C(O)C(O)C\\C=C/C\\C=C/CCCC(O)=O '
               'NAME: 11,12,15-THETA REASON: WRONGLY CLASSIFIED Contains one '
               'free, terminal carboxylic acid group and a long acyclic acyl '
               'chain with exactly 3 carbon–carbon double bonds typical of '
               'trienoic fatty acids\n'
               ' * SMILES: O=C(O)/C=C/C=C/C(=C/[C@H](CC)C)/C NAME: '
               '(2E,4E,6E)-6,8-dimethyldeca-2,4,6-trienoic acid REASON: '
               'WRONGLY CLASSIFIED Contains one free, terminal carboxylic acid '
               'group and a long acyclic acyl chain with exactly 3 '
               'carbon–carbon double bonds typical of trienoic fatty acids\n'
               ' * SMILES: '
               'O=C(O)/C(=C/C/C=C(\\CO)/CC/C=C(/CO)\\C)/CC(=O)C1=C(O)C=CC(=C1)O '
               'NAME: Zizhine N REASON: WRONGLY CLASSIFIED Contains one free, '
               'terminal carboxylic acid group and a long acyclic acyl chain '
               'with exactly 3 carbon–carbon double bonds typical of trienoic '
               'fatty acids\n'
               ' * SMILES: '
               'C([C@H](CC/C=C/C=C\\[C@H](CCCC(O)=O)O)O)/C=C\\CCCCC(O)(O)O '
               'NAME: 10,11-dihydro-20,20,20-trihydroxyleukotriene B4 REASON: '
               'WRONGLY CLASSIFIED Contains one free, terminal carboxylic acid '
               'group and a long acyclic acyl chain with exactly 3 '
               'carbon–carbon double bonds typical of trienoic fatty acids\n'
               ' * SMILES: '
               'CC(C\\C=C\\C=C\\CCC(=C)CC(C)C\\C(C)=C\\C(O)=O)CC(=O)CC(O)CNC(=O)C(C)C(C)OC(N)=O '
               'NAME: kalimantacin B REASON: WRONGLY CLASSIFIED Contains one '
               'free, terminal carboxylic acid group and a long acyclic acyl '
               'chain with exactly 3 carbon–carbon double bonds typical of '
               'trienoic fatty acids\n'
               ' * SMILES: CCCCCC(O)\\C=C\\C=C/C\\C=C/CCCCC(O)=O NAME: '
               '13-hydroxy-6Z,9Z,11E-octadecatrienoic acid REASON: WRONGLY '
               'CLASSIFIED Contains one free, terminal carboxylic acid group '
               'and a long acyclic acyl chain with exactly 3 carbon–carbon '
               'double bonds typical of trienoic fatty acids\n'
               ' * SMILES: '
               'C(=C(\\CC/C=C(/CC/C=C(/CCC(C)=C)\\C(O)=O)\\COC(=O)C)/C)\\CO '
               'NAME: Smaditerpenic acid F REASON: WRONGLY CLASSIFIED Contains '
               'one free, terminal carboxylic acid group and a long acyclic '
               'acyl chain with exactly 3 carbon–carbon double bonds typical '
               'of trienoic fatty acids\n'
               ' * SMILES: '
               'OC(=O)\\C=C(\\C[C@@H](CC(CC\\C=C\\C=C\\CC(C)C)=C)C)/C NAME: '
               '16:3(2E,10E,12E)(3Me,5Me[R],7My,15Me) REASON: WRONGLY '
               'CLASSIFIED Contains one free, terminal carboxylic acid group '
               'and a long acyclic acyl chain with exactly 3 carbon–carbon '
               'double bonds typical of trienoic fatty acids\n'
               ' * SMILES: CC\\C=C/C\\C=C/C[C@H](OO)\\C=C\\CCCCCCC(O)=O NAME: '
               '(8E,10S,12Z,15Z)-10-hydroperoxyoctadeca-8,12,15-trienoic acid '
               'REASON: WRONGLY CLASSIFIED Contains one free, terminal '
               'carboxylic acid group and a long acyclic acyl chain with '
               'exactly 3 carbon–carbon double bonds typical of trienoic fatty '
               'acids\n'
               ' * SMILES: '
               'C(=C(\\CC/C=C(/CC/C=C(/CCC(C)=C)\\C(O)=O)\\CO)/C)\\CO NAME: '
               'smaditerpenic acid C REASON: WRONGLY CLASSIFIED Contains one '
               'free, terminal carboxylic acid group and a long acyclic acyl '
               'chain with exactly 3 carbon–carbon double bonds typical of '
               'trienoic fatty acids\n'
               ' * SMILES: OC(=O)CCC/C=C\\CC/C=C\\CCCCC(C/C=C\\C(CCCC(C)C)C)C '
               'NAME: 24:3(5Z,9Z,17Z)(15Me,19Me,23Me) REASON: WRONGLY '
               'CLASSIFIED Contains one free, terminal carboxylic acid group '
               'and a long acyclic acyl chain with exactly 3 carbon–carbon '
               'double bonds typical of trienoic fatty acids\n'
               ' * SMILES: CC\\C=C/CC(O)\\C=C\\C=C/CCCCCCCC(O)=O NAME: '
               '13-HOTrE REASON: WRONGLY CLASSIFIED Contains one free, '
               'terminal carboxylic acid group and a long acyclic acyl chain '
               'with exactly 3 carbon–carbon double bonds typical of trienoic '
               'fatty acids\n'
               ' * SMILES: CCCCC\\C=C/C[C@@H](O)\\C=C\\C=C/CCC(O)=O NAME: '
               'tetranor-12R-HETE REASON: WRONGLY CLASSIFIED Contains one '
               'free, terminal carboxylic acid group and a long acyclic acyl '
               'chain with exactly 3 carbon–carbon double bonds typical of '
               'trienoic fatty acids\n'
               ' * SMILES: CC\\C=C/C\\C=C/C\\C=C/CCCCCC[C@@H](O)C(O)=O NAME: '
               '(R)-2-hydroxy-alpha-linolenic acid REASON: WRONGLY CLASSIFIED '
               'Contains one free, terminal carboxylic acid group and a long '
               'acyclic acyl chain with exactly 3 carbon–carbon double bonds '
               'typical of trienoic fatty acids\n'
               ' * SMILES: OC(=O)CCC/C=C\\CC/C=C\\C/C=C\\CCC(CC)C NAME: '
               '16-methyl-octadeca-5Z,9Z,12Z-trienoic acid REASON: WRONGLY '
               'CLASSIFIED Contains one free, terminal carboxylic acid group '
               'and a long acyclic acyl chain with exactly 3 carbon–carbon '
               'double bonds typical of trienoic fatty acids\n'
               ' * SMILES: '
               'C(=C\\[C@H](C[C@@H](C[C@H](CC(O)=O)N)O)OC)/C=C/C=C/CCCCC NAME: '
               '(3R,5R,7S,8E,10E,12E)-3-amino-5-hydroxy-7-methoxyoctadeca-8,10,12-trienoic '
               'acid REASON: WRONGLY CLASSIFIED Contains one free, terminal '
               'carboxylic acid group and a long acyclic acyl chain with '
               'exactly 3 carbon–carbon double bonds typical of trienoic fatty '
               'acids\n'
               ' * SMILES: CCC=CCC=CCC=CCCCCCCCCCCCC(=O)O NAME: '
               'docosa-13,16,19-trienoic acid REASON: WRONGLY CLASSIFIED '
               'Contains one free, terminal carboxylic acid group and a long '
               'acyclic acyl chain with exactly 3 carbon–carbon double bonds '
               'typical of trienoic fatty acids\n'
               ' * SMILES: '
               'O(C(=O)CCCCCCCCCCCCCCC)[C@H](/C=C\\CCCCCCCC(O)=O)/C=C\\C/C=C\\CC '
               'NAME: Mayolene-16 REASON: WRONGLY CLASSIFIED Contains one '
               'free, terminal carboxylic acid group and a long acyclic acyl '
               'chain with exactly 3 carbon–carbon double bonds typical of '
               'trienoic fatty acids\n'
               ' * SMILES: OC(=O)CCCC/C=C/C=C/C#CC#C/C=C\\C NAME: '
               '6E,8E,14Z-Hexadecatriene-10,12-diynoic acid REASON: WRONGLY '
               'CLASSIFIED Contains one free, terminal carboxylic acid group '
               'and a long acyclic acyl chain with exactly 3 carbon–carbon '
               'double bonds typical of trienoic fatty acids\n'
               ' * SMILES: O=C(CCCCCCCC(O)=O)/C=C/C=C\\C/C=C\\CC NAME: '
               '9-OxoOTrE REASON: WRONGLY CLASSIFIED Contains one free, '
               'terminal carboxylic acid group and a long acyclic acyl chain '
               'with exactly 3 carbon–carbon double bonds typical of trienoic '
               'fatty acids\n'
               ' * SMILES: OC(=O)CCC/C=C\\CCCCCC/C=C\\C/C=C\\CCCCC NAME: '
               'Eranthic acid REASON: WRONGLY CLASSIFIED Contains one free, '
               'terminal carboxylic acid group and a long acyclic acyl chain '
               'with exactly 3 carbon–carbon double bonds typical of trienoic '
               'fatty acids\n'
               ' * SMILES: CCCCCCC/C=C\\C/C=C\\C/C=C\\CCCC(O)=O NAME: Coreynic '
               'acid REASON: WRONGLY CLASSIFIED Contains one free, terminal '
               'carboxylic acid group and a long acyclic acyl chain with '
               'exactly 3 carbon–carbon double bonds typical of trienoic fatty '
               'acids\n'
               ' * SMILES: O=C(O)/C=C/C=C/[C@@H](O)C/C=C/CCC[C@H](O)C NAME: '
               '(6S,13R)-6,13-dihydroxy-2E,4E,8E-tetradecatrienoic acid '
               'REASON: WRONGLY CLASSIFIED Contains one free, terminal '
               'carboxylic acid group and a long acyclic acyl chain with '
               'exactly 3 carbon–carbon double bonds typical of trienoic fatty '
               'acids\n'
               'False negatives: SMILES: '
               'O=C(CCC/C=C\\C/C=C\\CC(/C=C/[C@@H]1[C@H](CCCCC)O1)O)O NAME: 11 '
               'hydroxy-(14R,15S)-epoxy-(5Z,8Z,12E)-icosatrienoic acid REASON: '
               'MISSED Acyl chain contains rings; fatty acid chain must be '
               'acyclic\n'
               ' * SMILES: CCCCC\\C=C/C\\C=C/C\\C=C/CC1OC1CCCC(O)=O NAME: '
               '5,6-EET REASON: MISSED Acyl chain contains rings; fatty acid '
               'chain must be acyclic\n'
               ' * SMILES: '
               'CCCCC\\C=C/C[C@@H]1O[C@H]1\\C=C\\[C@H](O)C\\C=C/CCCC(O)=O '
               'NAME: (8R)-hydroxy-(11S,12S)-epoxyicosa-(5Z,9E,14Z)-trienoic '
               'acid REASON: MISSED Acyl chain contains rings; fatty acid '
               'chain must be acyclic\n'
               ' * SMILES: '
               'C\\C(CO)=C/CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\C(O)=O NAME: '
               '(2E,6E,10E,14E)-omega-hydroxygeranylgeranic acid REASON: '
               'MISSED Found 4 C=C double bonds along the acyl chain; requires '
               'exactly 3 for a trienoic fatty acid\n'
               ' * SMILES: [H]C(\\C=C/CCCCCCCC(O)=O)=C1O[C@H]1C\\C=C/CC NAME: '
               '(9Z,13S,15Z)-12,13-epoxyoctadeca-9,11,15-trienoic acid REASON: '
               'MISSED Acyl chain contains rings; fatty acid chain must be '
               'acyclic\n'
               ' * SMILES: '
               'O=C(CCC/C=C\\C/C=C\\C/C=C\\C([C@@H]1[C@H](CCCCC)O1)O)O NAME: '
               '13-hydroxy-(14R,15S)-epoxy-(5Z,8Z,11Z)-icosatrienoic acid '
               'REASON: MISSED Acyl chain contains rings; fatty acid chain '
               'must be acyclic\n'
               ' * SMILES: C(CCCO)C/C=C\\C/C=C\\CC1C(C/C=C\\CCCC(O)=O)O1 NAME: '
               '8,9-epoxy-20-hydroxy-(5Z,11Z,14Z)-icosatrienoic acid REASON: '
               'MISSED Acyl chain contains rings; fatty acid chain must be '
               'acyclic\n'
               ' * SMILES: '
               'C(CCC(O)=O)/C=C\\C/C=C\\C=C\\[C@H](C[C@H]1[C@@H](CCCCC)O1)OO '
               'NAME: '
               '(12S)-hydroperoxy-(14S,15R)-epoxy-(5Z,8Z,10E)-icosatrienoic '
               'acid REASON: MISSED Acyl chain contains rings; fatty acid '
               'chain must be acyclic\n'
               ' * SMILES: '
               'C(CCCC)[C@H]1[C@H](\\C=C\\[C@H](C/C=C\\C/C=C\\CCCC(O)=O)O)O1 '
               'NAME: 11(S)-hydroxy-14(S),15(S)-hepoxilin A3 REASON: MISSED '
               'Acyl chain contains rings; fatty acid chain must be acyclic\n'
               ' * SMILES: CCCCC\\C=C/CC1OC1C\\C=C/C\\C=C/CCCC(O)=O NAME: '
               '11,12-EET REASON: MISSED Acyl chain contains rings; fatty acid '
               'chain must be acyclic\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'O1C2=C(O)C=C(COC)C=C2C[C@@H](C1(C)C)O',
                                     'name': 'Conoideochromane B',
                                     'reason': 'Missing carboxylic acid '
                                               'functional group (COOH)'},
                                 {   'smiles': 'P(OC[C@H](OC(=O)CCCCCCC/C=C\\CCCCC)CO/C=C\\CCCCCCCCCCCCCC)(OCCN)(O)=O',
                                     'name': 'PE(P-16:0/15:1(9Z))',
                                     'reason': 'Missing carboxylic acid '
                                               'functional group (COOH)'},
                                 {   'smiles': 'O=C1C=2C(OC(=C1)C)=C(C3=C4O[C@](O)(CC(C4=C(O)C=5C3=CC(OC)=CC5OC)=O)C)C6=CC(OC)=CC(=C6C2O)OC',
                                     'name': '2-hydroxydihydronigerone',
                                     'reason': 'Missing carboxylic acid '
                                               'functional group (COOH)'},
                                 {   'smiles': 'O([C@@H]1[C@@H](NC(=O)C)[C@@H](O[C@@H]([C@H]1O)CO)OC[C@H]2O[C@@H](O)[C@H](NC(=O)C)[C@@H](O)[C@H]2O)[C@@H]3O[C@@H]([C@H](O)[C@H](O[C@H]4O[C@@H]([C@H](O)[C@H](O)[C@H]4O)CO)[C@H]3O)CO',
                                     'name': 'N-[(2R,3R,4R,5R,6R)-6-[[(2R,3R,4R,5S,6R)-3-Acetamido-4-[(2R,3R,4S,5S,6R)-3,5-dihydroxy-6-(hydroxymethyl)-4-[(2R,3R,4S,5R,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-5-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxymethyl]-2,4,5-trihydroxyoxan-3-yl]acetamide',
                                     'reason': 'Missing carboxylic acid '
                                               'functional group (COOH)'},
                                 {   'smiles': 'O1C(C(O)C(O)C(O)C1OC=2C(O)=C(O)C=C(C2)C=O)COC(=O)C3=CC(O)=C(O)C(O)=C3',
                                     'name': 'Castamollissin',
                                     'reason': 'Missing carboxylic acid '
                                               'functional group (COOH)'},
                                 {   'smiles': 'S(OC[C@H]1O[C@@H](OC[C@H]2O[C@@H](O[C@@H]([C@@H](O)[C@H](O)CO[C@]3(O[C@H]([C@H](NC(=O)C)[C@@H](O)C3)[C@H](O)[C@H](O)CO)C(O)=O)[C@@H](NC(=O)C)CO)[C@H](O)[C@@H](O)[C@H]2O)[C@H](NC(=O)C)[C@@H](O)[C@@H]1O[C@@H]4O[C@@H]([C@H](O)[C@H](O)[C@H]4O)CO[C@]5(O[C@H]([C@H](NC(=O)C)[C@@H](O)C5)[C@H](O)[C@H](O)CO)C(O)=O)(O)(=O)=O',
                                     'name': '(2R,4S,5R,6R)-5-Acetamido-2-[[(2R,3R,4S,5R,6S)-6-[(2R,3S,4R,5R,6R)-5-acetamido-6-[[(2R,3R,4S,5R,6R)-6-[(2S,3R,4S,5R)-2-acetamido-6-[(2R,4S,5R,6R)-5-acetamido-2-carboxy-4-hydroxy-6-[(1R,2R)-1,2,3-trihydroxypropyl]oxan-2-yl]oxy-1,4,5-trihydroxyhexan-3-yl]oxy-3,4,5-trihydroxyoxan-2-yl]methoxy]-4-hydroxy-2-(sulfooxymethyl)oxan-3-yl]oxy-3,4,5-trihydroxyoxan-2-yl]methoxy]-4-hydroxy-6-[(1R,2R)-1,2,3-trihydroxypropyl]oxane-2-carboxylic '
                                             'acid',
                                     'reason': 'Found 2 carboxylic acid '
                                               'groups; requires exactly 1'},
                                 {   'smiles': 'FC(F)(F)C(F)(F)C(F)(F)C(F)(F)C(F)(F)C(F)(F)F',
                                     'name': 'perfluorohexane',
                                     'reason': 'Missing carboxylic acid '
                                               'functional group (COOH)'},
                                 {   'smiles': 'CC(C)(O)CCC(=O)[C@](C)(O)[C@H]1[C@H](O)C[C@@]2(C)[C@@H]3CC=C4[C@@H](C[C@@H](O)[C@@H](O)C4(C)C)[C@]3(C)C(=O)C[C@]12C',
                                     'name': 'Cucurbitacin P',
                                     'reason': 'Missing carboxylic acid '
                                               'functional group (COOH)'},
                                 {   'smiles': 'CCCCCCCc1cc(O)cc(=O)o1',
                                     'name': '4-hydroxy-6-heptylpyran-2-one',
                                     'reason': 'Missing carboxylic acid '
                                               'functional group (COOH)'},
                                 {   'smiles': 'S(O[C@@H]1[C@@H](O)[C@H](O[C@H]2[C@H](O)[C@@H](NC(=O)C)[C@H](O[C@H]3[C@@H](O)[C@H](O[C@@H]4O[C@@H]([C@@H](O[C@@H]5O[C@@H]([C@H](O)[C@H](OS(O)(=O)=O)[C@H]5O)CO)[C@H](O)[C@H]4NC(=O)C)CO)[C@H](O[C@@H]3O[C@H]6[C@H](O)[C@H](O[C@@H](O[C@H]7[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]7CO)O[C@H]8[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]8CO[C@@H]9O[C@H]([C@@H](O)[C@@H](O)[C@@H]9O)C)O)[C@H]6O)CO[C@H]%10O[C@@H]([C@@H](O)[C@H](O)[C@@H]%10O[C@@H]%11O[C@@H]([C@@H](O[C@@H]%12O[C@@H]([C@H](O[C@@H]%13O[C@@H]([C@H](O)[C@H](O)[C@H]%13NC(=O)C)CO)[C@H](O[C@]%14(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%14)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%12O)CO)[C@H](O)[C@H]%11NC(=O)C)CO)CO[C@@H]%15O[C@@H]([C@@H](O[C@@H]%16O[C@@H]([C@H](O)[C@H](O[C@]%17(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%17)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%16O)CO)[C@H](O)[C@H]%15NC(=O)C)CO)CO)O[C@@H]2CO)O[C@@H]([C@@H]1O)CO)(O)(=O)=O',
                                     'name': 'CID 146017241',
                                     'reason': 'Found 2 carboxylic acid '
                                               'groups; requires exactly 1'}],
    'sample_false_negatives': [   {   'smiles': 'O=C(CCC/C=C\\C/C=C\\CC(/C=C/[C@@H]1[C@H](CCCCC)O1)O)O',
                                      'name': '11 '
                                              'hydroxy-(14R,15S)-epoxy-(5Z,8Z,12E)-icosatrienoic '
                                              'acid',
                                      'reason': 'Acyl chain contains rings; '
                                                'fatty acid chain must be '
                                                'acyclic'},
                                  {   'smiles': 'C(CC=[C@]=C(CCCC(O)=O)[H])CCCCCC\\C=C\\C',
                                      'name': '(S)-lamenallenic acid',
                                      'reason': 'Double bonds are conjugated; '
                                                'they must be separated by a '
                                                'methylene group'},
                                  {   'smiles': 'CCCCC\\C=C/C\\C=C/C\\C=C/CC1OC1CCCC(O)=O',
                                      'name': '5,6-EET',
                                      'reason': 'Acyl chain contains rings; '
                                                'fatty acid chain must be '
                                                'acyclic'},
                                  {   'smiles': 'CCCCC\\C=C/C[C@@H]1O[C@H]1\\C=C\\[C@H](O)C\\C=C/CCCC(O)=O',
                                      'name': '(8R)-hydroxy-(11S,12S)-epoxyicosa-(5Z,9E,14Z)-trienoic '
                                              'acid',
                                      'reason': 'Acyl chain contains rings; '
                                                'fatty acid chain must be '
                                                'acyclic'},
                                  {   'smiles': 'C\\C(CO)=C/CC\\C(C)=C\\CC\\C(C)=C\\CC\\C(C)=C\\C(O)=O',
                                      'name': '(2E,6E,10E,14E)-omega-hydroxygeranylgeranic '
                                              'acid',
                                      'reason': 'Acyl chain is branched at '
                                                'atom index 17; fatty acid '
                                                'chain must be linear'},
                                  {   'smiles': '[H]C(\\C=C/CCCCCCCC(O)=O)=C1O[C@H]1C\\C=C/CC',
                                      'name': '(9Z,13S,15Z)-12,13-epoxyoctadeca-9,11,15-trienoic '
                                              'acid',
                                      'reason': 'Acyl chain contains rings; '
                                                'fatty acid chain must be '
                                                'acyclic'},
                                  {   'smiles': 'O=C(CCC/C=C\\C/C=C\\C/C=C\\C([C@@H]1[C@H](CCCCC)O1)O)O',
                                      'name': '13-hydroxy-(14R,15S)-epoxy-(5Z,8Z,11Z)-icosatrienoic '
                                              'acid',
                                      'reason': 'Acyl chain contains rings; '
                                                'fatty acid chain must be '
                                                'acyclic'},
                                  {   'smiles': 'C(CCCO)C/C=C\\C/C=C\\CC1C(C/C=C\\CCCC(O)=O)O1',
                                      'name': '8,9-epoxy-20-hydroxy-(5Z,11Z,14Z)-icosatrienoic '
                                              'acid',
                                      'reason': 'Acyl chain contains rings; '
                                                'fatty acid chain must be '
                                                'acyclic'},
                                  {   'smiles': 'C(CCC(O)=O)/C=C\\C/C=C\\C=C\\[C@H](C[C@H]1[C@@H](CCCCC)O1)OO',
                                      'name': '(12S)-hydroperoxy-(14S,15R)-epoxy-(5Z,8Z,10E)-icosatrienoic '
                                              'acid',
                                      'reason': 'Acyl chain contains rings; '
                                                'fatty acid chain must be '
                                                'acyclic'},
                                  {   'smiles': 'C(CCCC)[C@H]1[C@H](\\C=C\\[C@H](C/C=C\\C/C=C\\CCCC(O)=O)O)O1',
                                      'name': '11(S)-hydroxy-14(S),15(S)-hepoxilin '
                                              'A3',
                                      'reason': 'Acyl chain contains rings; '
                                                'fatty acid chain must be '
                                                'acyclic'}],
    'attempt': 5,
    'reasoning': 'Below is one way to improve the classifier. In our reasoning '
                 'we noted that the “old” code used a DFS to grab the '
                 '“longest” carbon path starting at the acid carbon. However, '
                 'many false positives arose because the algorithm allowed any '
                 'branched or “global‐long” chain to be taken even if it did '
                 'not represent the linear acyl (fatty acid) backbone. Also, '
                 'we need to rule out cases in which consecutive double bonds '
                 'occur in a conjugated system rather than the typical '
                 '(methylene–interrupted) pattern. One way to address both '
                 'issues is to require that the carboxylic acid group be '
                 '“free” and terminal, then follow the one carbon neighbor '
                 'from the acid carbon. At every step we insist that the next '
                 'carbon is unique (i.e. no branching) so that we extract a '
                 'simple linear chain. Finally we count the number of C=C '
                 'bonds along that chain and also check that the unsaturations '
                 'occur in a methylene‐interrupted pattern (i.e. not '
                 '“conjugated”). This tends to remove some false positives. '
                 '(Note that without a “gold‐standard” routine the problem '
                 'remains challenging; our code represents one reasonable '
                 'approach.) \n'
                 '\n'
                 'Below is a single Python code block (using RDKit) that '
                 'implements the function is_trienoic_fatty_acid.\n'
                 '\n'
                 '--------------------------------------------------------------------------------',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 100,
    'num_false_positives': 72,
    'num_true_negatives': 142091,
    'num_false_negatives': 37,
    'num_negatives': None,
    'precision': 0.5813953488372093,
    'recall': 0.7299270072992701,
    'f1': 0.6472491909385113,
    'accuracy': 0.9992340126493324,
    'negative_predictive_value': 0.9997396712822245}