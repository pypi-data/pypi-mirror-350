"""
Classifies: CHEBI:4986 fatty acid methyl ester
"""
"""
Classifies: Fatty acid methyl ester

A fatty acid methyl ester is defined as the carboxylic ester obtained by the formal 
condensation of a fatty acid with methanol. Here we require that the molecule 
(i) contains a methyl ester group as defined by the SMARTS "[CX3](=O)O[CH3]",
(ii) the acyl portion (the group attached to the carbonyl carbon, excluding the ester oxygen) 
    forms a contiguous chain of carbon atoms of at least 3 carbons,
(iii) the chain must not contain aromatic atoms and must be “simple” (i.e. almost all substituents 
    are trivial methyl branches – if any non-carbon substituent is detected the molecule is rejected),
(iv) and the overall molecule is not decorated beyond expectation.
    
If these conditions are met, the function returns True with an explanation.
"""

from rdkit import Chem
from rdkit.Chem import rdMolDescriptors

def is_fatty_acid_methyl_ester(smiles: str):
    """
    Determines if a molecule is a fatty acid methyl ester based on its SMILES string.
    
    The algorithm:
      1. Searches for the methyl ester group via the SMARTS "[CX3](=O)O[CH3]".
      2. For each found ester substructure, it identifies the carbonyl carbon and then 
         the acyl side (the neighbor that is not the carbonyl oxygen).
      3. It then uses a depth-first search (DFS) to find the longest contiguous path 
         of carbon atoms (only aliphatic, non‐aromatic) starting from that acyl atom.
      4. If the chain length is at least 3 carbons then the chain is scrutinized:
           • any substituent (branching off a chain atom, other than the one linking back to the carbonyl)
             is examined. Non‐carbon branches or branches longer than one atom are a sign of extra decoration.
      5. The overall heavy atom count of the molecule is compared to an expected minimum 
         (chain_length + 4) – if there is too much extra functionality the chain is rejected.
    
    Args:
        smiles (str): SMILES string of the molecule.
        
    Returns:
        bool: True if the molecule qualifies as a fatty acid methyl ester, False otherwise.
        str: Explanation for the classification decision.
    """
    
    # Try to parse the SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
    
    # Define the methyl ester SMARTS
    ester_smarts = "[CX3](=O)O[CH3]"
    ester_pattern = Chem.MolFromSmarts(ester_smarts)
    if ester_pattern is None:
        return False, "Error defining ester SMARTS"
    
    ester_matches = mol.GetSubstructMatches(ester_pattern)
    if not ester_matches:
        return False, "No methyl ester group found in the molecule"
    
    # DFS helper: from a given atom, follow bonds to atoms that are carbons, not in a ring, and non aromatic.
    def dfs_longest_chain(atom, visited):
        # Current path includes this atom.
        best_path = [atom.GetIdx()]
        for nbr in atom.GetNeighbors():
            if nbr.GetAtomicNum() != 6:
                continue
            # We want only non-aromatic carbons (i.e. aliphatic chain) 
            # so if this neighbor is marked aromatic, skip it.
            if nbr.GetIsAromatic():
                continue
            if nbr.GetIdx() in visited:
                continue
            new_visited = visited | {nbr.GetIdx()}
            candidate = dfs_longest_chain(nbr, new_visited)
            candidate = [atom.GetIdx()] + candidate
            if len(candidate) > len(best_path):
                best_path = candidate
        return best_path
    
    # Examine each ester match.
    # The SMARTS match returns a tuple: (carbonylC, carbonylO, esterO, methylC)
    for match in ester_matches:
        carbonyl_idx, carbonylO_idx, esterO_idx, methyl_idx = match
        carbonyl_atom = mol.GetAtomWithIdx(carbonyl_idx)
        
        # Identify the acyl neighbor (attached to the carbonyl but not the carbonyl oxygen)
        acyl_neighbor = None
        for nbr in carbonyl_atom.GetNeighbors():
            if nbr.GetIdx() == carbonylO_idx:
                continue
            if nbr.GetAtomicNum() == 6 and not nbr.GetIsAromatic():
                acyl_neighbor = nbr
                break
        if acyl_neighbor is None:
            continue  # try next ester match
        
        # Compute the longest contiguous acyl chain starting from acyl_neighbor.
        visited = {carbonyl_idx}  # exclude the carbonyl carbon
        chain_path = dfs_longest_chain(acyl_neighbor, visited)
        chain_length = len(chain_path)
        
        if chain_length < 3:
            # A minimal fatty acyl fragment should have at least 3 carbons.
            continue
        
        # Check for extra decoration on the acyl chain.
        # For each atom in the chain, check neighbors that are not in the chain and not the carbonyl (for the first atom).
        extra_branch = False
        for i, atom_idx in enumerate(chain_path):
            atom = mol.GetAtomWithIdx(atom_idx)
            for nbr in atom.GetNeighbors():
                # Skip atoms that are part of the main chain.
                if nbr.GetIdx() in chain_path:
                    continue
                # Also allow the carbonyl atom if we are at the first atom.
                if i == 0 and nbr.GetIdx() == carbonyl_idx:
                    continue
                # We allow a trivial (methyl) branch if it is a carbon that itself has no further heavy neighbors.
                if nbr.GetAtomicNum() == 6 and not nbr.GetIsAromatic():
                    # Count heavy neighbors (excluding hydrogens)
                    heavy_nbrs = [a for a in nbr.GetNeighbors() if a.GetAtomicNum() > 1 and a.GetIdx() not in chain_path]
                    if len(heavy_nbrs) > 0:
                        extra_branch = True
                        break
                else:
                    # Any branch that is not carbon is not allowed.
                    extra_branch = True
                    break
            if extra_branch:
                break
        if extra_branch:
            # The chain shows decoration beyond a simple fatty acid
            continue
        
        # Check overall molecule simplicity.
        # Expected heavy atoms: acyl chain (chain_length) + carbonyl carbon (1) + carbonyl oxygen (1) 
        #                    + ester oxygen (1) + methyl carbon (1) = chain_length + 4.
        expected_heavy_atoms = chain_length + 4
        actual_heavy_atoms = mol.GetNumHeavyAtoms()
        # We allow a tolerance of +6 heavy atoms only.
        if actual_heavy_atoms > expected_heavy_atoms + 6:
            continue
        
        # Optionally compute the number of rotatable bonds in the acyl chain.
        rotatable_in_chain = 0
        for j in range(len(chain_path)-1):
            bond = mol.GetBondBetweenAtoms(chain_path[j], chain_path[j+1])
            if bond is None:
                continue
            if bond.GetBondTypeAsDouble() == 1.0 and not bond.IsInRing():
                rotatable_in_chain += 1
        
        overall_rot_bonds = rdMolDescriptors.CalcNumRotatableBonds(mol)
        mol_wt = rdMolDescriptors.CalcExactMolWt(mol)
        
        reason = (f"Found a methyl ester group with an acyl chain of {chain_length} carbon(s); "
                  f"rotatable bonds in chain: {rotatable_in_chain}, overall rotatable bonds: {overall_rot_bonds}, "
                  f"molecule heavy atoms: {actual_heavy_atoms} (expected ~{expected_heavy_atoms}), "
                  f"molecular weight: {mol_wt:.1f} Da")
        return True, reason
    
    return False, "Molecule contains a methyl ester group but the acyl portion does not meet fatty acid criteria"


# Example usage (testing several provided SMILES):
if __name__ == "__main__":
    test_smiles = [
        "CCCCCC1C(C/C(=C(\\C\\C(=C(\\[H])/CCCCCCC(=O)OC)\\[H])/[H])/[H])O1",  # 13-(3-pentyl-2-oxiranyl)-... (TP)
        "O[C@H](CCCCCCCC(OC)=O)/C=C/C=C/CCCCC",  # 9R-hydroxy-10E,12E-octadecadienoic acid methyl ester (TP)
        "O=C(OC)CCCCCCCCCCCC",  # methyl tridecanoate (TP)
        "O(C(=O)CCC(CCCC)C)C",  # formyl 4-methyl-octanoate (TP)
        "COC(=O)[C@@H]1O[C@@]1(C)CC\\C=C(/C)CC[C@H]1OC1(C)C",  # juvenile hormone III skipped bisepoxide (TP)
        "COC(=O)CCC(=O)CN",  # methyl 5-aminolevulinate (FP expected to be rejected)
        "COC(=O)\\C=C(/C)C(=O)OC",  # Dimethyl citraconate (FP expected to be rejected)
        "O=C(OC)CCC(=O)NCCCCCN(O)C(=O)CC(C)C"  # Tenacibactin A (FP expected to be rejected)
    ]
    
    for sm in test_smiles:
        valid, msg = is_fatty_acid_methyl_ester(sm)
        print(f"SMILES: {sm}\nResult: {valid}\nReason: {msg}\n")


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:4986',
                          'name': 'fatty acid methyl ester',
                          'definition': 'A fatty acid ester that is the '
                                        'carboxylic ester obtained by the '
                                        'formal condensation of a fatty acid '
                                        'with methanol.',
                          'parents': ['CHEBI:25248', 'CHEBI:35748'],
                          'xrefs': [   'KEGG:C03395',
                                       'MetaCyc:Fatty-acid-methyl-esters',
                                       'Wikipedia:Fatty_acid_methyl_ester'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 137,
                           'log_lines_of_code': 4.919980925828125,
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
                                                 2,
                                                 1,
                                                 2,
                                                 2,
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
                                                 4,
                                                 3,
                                                 3,
                                                 3,
                                                 4,
                                                 3,
                                                 4,
                                                 3,
                                                 3,
                                                 3,
                                                 3,
                                                 4,
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
                                                 2,
                                                 3,
                                                 4,
                                                 3,
                                                 4,
                                                 4,
                                                 2,
                                                 3,
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
                                                 2,
                                                 3,
                                                 3,
                                                 4,
                                                 4,
                                                 5,
                                                 4,
                                                 4,
                                                 5,
                                                 4,
                                                 4,
                                                 5,
                                                 5,
                                                 5,
                                                 6,
                                                 6,
                                                 4,
                                                 5,
                                                 5,
                                                 5,
                                                 3,
                                                 4,
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
                                                 2,
                                                 3,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 3,
                                                 4,
                                                 3,
                                                 4,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 1,
                                                 1,
                                                 0,
                                                 0,
                                                 1,
                                                 2,
                                                 2,
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
                                                 2],
                           'max_indent': 6,
                           'imports': [   'from rdkit import Chem',
                                          'from rdkit.Chem import '
                                          'rdMolDescriptors'],
                           'imports_count': 2,
                           'methods_called': [   'CalcNumRotatableBonds',
                                                 'GetNumHeavyAtoms',
                                                 'CalcExactMolWt',
                                                 'GetIdx',
                                                 'GetIsAromatic',
                                                 'GetAtomicNum',
                                                 'GetBondTypeAsDouble',
                                                 'MolFromSmiles',
                                                 'GetAtomWithIdx',
                                                 'MolFromSmarts',
                                                 'GetBondBetweenAtoms',
                                                 'GetNeighbors',
                                                 'IsInRing',
                                                 'GetSubstructMatches'],
                           'methods_called_count': 14,
                           'smarts_strings': ['ester_smarts'],
                           'smarts_strings_count': 1,
                           'defs': [   'is_fatty_acid_methyl_ester(smiles: '
                                       'str):',
                                       'dfs_longest_chain(atom, visited):'],
                           'defs_count': 2,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "Error defining ester '
                                          'SMARTS"',
                                          'False, "No methyl ester group found '
                                          'in the molecule"',
                                          'best_path',
                                          'True, reason',
                                          'False, "Molecule contains a methyl '
                                          'ester group but the acyl portion '
                                          'does not meet fatty acid criteria"'],
                           'returns_count': 6,
                           'complexity': 6.583996185165626},
    'message': '\n'
               'Attempt failed: F1 score of 0.47145488029465926 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: '
               'CCCCCC1C(C/C(=C(\\C\\C(=C(\\[H])/CCCCCCC(=O)OC)\\[H])/[H])/[H])O1 '
               'NAME: 13-(3-pentyl-2-oxiranyl)-(8Z,11Z)-8,11-tridecadienoic '
               'acid methyl ester REASON: CORRECT Found a methyl ester group '
               'with an acyl chain of 19 carbon(s); internal rotatable bonds '
               'in chain: 14, overall rotatable bonds: 15, molecule heavy '
               'atoms: 24 (expected ~23), molecular weight: 336.3 Da\n'
               ' * SMILES: O[C@H](CCCCCCCC(OC)=O)/C=C/C=C/CCCCC NAME: '
               '9R-hydroxy-10E,12E-octadecadienoic acid, methyl ester REASON: '
               'CORRECT Found a methyl ester group with an acyl chain of 17 '
               'carbon(s); internal rotatable bonds in chain: 13, overall '
               'rotatable bonds: 14, molecule heavy atoms: 22 (expected ~21), '
               'molecular weight: 310.3 Da\n'
               ' * SMILES: O=C(OC)CCCCCCCCCCCC NAME: methyl tridecanoate '
               'REASON: CORRECT Found a methyl ester group with an acyl chain '
               'of 12 carbon(s); internal rotatable bonds in chain: 10, '
               'overall rotatable bonds: 11, molecule heavy atoms: 16 '
               '(expected ~16), molecular weight: 228.2 Da\n'
               ' * SMILES: O(C(=O)CCC(CCCC)C)C NAME: formyl 4-methyl-octanoate '
               'REASON: CORRECT Found a methyl ester group with an acyl chain '
               'of 7 carbon(s); internal rotatable bonds in chain: 5, overall '
               'rotatable bonds: 6, molecule heavy atoms: 12 (expected ~11), '
               'molecular weight: 172.1 Da\n'
               ' * SMILES: O(C(=O)CCCCCCCCCCCCC(C)C)C NAME: methyl '
               '14-methylpentadecanoate REASON: CORRECT Found a methyl ester '
               'group with an acyl chain of 14 carbon(s); internal rotatable '
               'bonds in chain: 12, overall rotatable bonds: 13, molecule '
               'heavy atoms: 19 (expected ~18), molecular weight: 270.3 Da\n'
               ' * SMILES: O(C(=O)CCC/C=C\\C/C=C\\C/C=C\\CCCCCCCC)C NAME: '
               'cis-5,8,11-Eicosatrienoic acid methyl ester REASON: CORRECT '
               'Found a methyl ester group with an acyl chain of 19 carbon(s); '
               'internal rotatable bonds in chain: 14, overall rotatable '
               'bonds: 15, molecule heavy atoms: 23 (expected ~23), molecular '
               'weight: 320.3 Da\n'
               ' * SMILES: SC(CC(OC)=O)C NAME: Methyl 3-mercaptobutanoate '
               'REASON: CORRECT Found a methyl ester group with an acyl chain '
               'of 3 carbon(s); internal rotatable bonds in chain: 1, overall '
               'rotatable bonds: 2, molecule heavy atoms: 8 (expected ~7), '
               'molecular weight: 134.0 Da\n'
               ' * SMILES: COC(=O)[C@@H]1O[C@@]1(C)CC\\C=C(/C)CC[C@H]1OC1(C)C '
               'NAME: juvenile hormone III skipped bisepoxide REASON: CORRECT '
               'Found a methyl ester group with an acyl chain of 11 carbon(s); '
               'internal rotatable bonds in chain: 7, overall rotatable bonds: '
               '7, molecule heavy atoms: 20 (expected ~15), molecular weight: '
               '282.2 Da\n'
               ' * SMILES: O1[C@@H]([C@H]1C#CC#CCCC(OC)=O)CCC\\C=C/C=C\\CC '
               'NAME: methyl 8R,9R-epoxy-13Z,15Z-eicosadien-4,6-diynoate '
               'REASON: CORRECT Found a methyl ester group with an acyl chain '
               'of 17 carbon(s); internal rotatable bonds in chain: 10, '
               'overall rotatable bonds: 8, molecule heavy atoms: 22 (expected '
               '~21), molecular weight: 300.2 Da\n'
               ' * SMILES: CCCCC\\C=C/C\\C=C/C=C/C(C\\C=C/CCCC(=O)OC)OO NAME: '
               '8-HPETE methyl ester REASON: CORRECT Found a methyl ester '
               'group with an acyl chain of 19 carbon(s); internal rotatable '
               'bonds in chain: 13, overall rotatable bonds: 15, molecule '
               'heavy atoms: 25 (expected ~23), molecular weight: 350.2 Da\n'
               ' * SMILES: C(CCCCCCCCCC)CCCCCCCC(OC)=O NAME: methyl '
               'nonadecanoate REASON: CORRECT Found a methyl ester group with '
               'an acyl chain of 18 carbon(s); internal rotatable bonds in '
               'chain: 16, overall rotatable bonds: 17, molecule heavy atoms: '
               '22 (expected ~22), molecular weight: 312.3 Da\n'
               ' * SMILES: O=C(OC)CCCCCCCCCCCCCCCCCCCCCCCC NAME: Methyl '
               'pentacosanoate REASON: CORRECT Found a methyl ester group with '
               'an acyl chain of 24 carbon(s); internal rotatable bonds in '
               'chain: 22, overall rotatable bonds: 23, molecule heavy atoms: '
               '28 (expected ~28), molecular weight: 396.4 Da\n'
               ' * SMILES: O(C(=O)CCCC/C=C/CC)C NAME: formyl 6E-nonenoate '
               'REASON: CORRECT Found a methyl ester group with an acyl chain '
               'of 8 carbon(s); internal rotatable bonds in chain: 5, overall '
               'rotatable bonds: 6, molecule heavy atoms: 12 (expected ~12), '
               'molecular weight: 170.1 Da\n'
               ' * SMILES: O(C(=O)CC/C=C\\CCCCC)C NAME: formyl 4Z-decenoate '
               'REASON: CORRECT Found a methyl ester group with an acyl chain '
               'of 9 carbon(s); internal rotatable bonds in chain: 6, overall '
               'rotatable bonds: 7, molecule heavy atoms: 13 (expected ~13), '
               'molecular weight: 184.1 Da\n'
               ' * SMILES: C(CCCCCCCC)CCCCC(OC)=O NAME: methyl tetradecanoate '
               'REASON: CORRECT Found a methyl ester group with an acyl chain '
               'of 13 carbon(s); internal rotatable bonds in chain: 11, '
               'overall rotatable bonds: 12, molecule heavy atoms: 17 '
               '(expected ~17), molecular weight: 242.2 Da\n'
               ' * SMILES: S(C(CC(OC)=O)C)C NAME: Methyl '
               '3-(methylthio)butanoate REASON: CORRECT Found a methyl ester '
               'group with an acyl chain of 3 carbon(s); internal rotatable '
               'bonds in chain: 1, overall rotatable bonds: 3, molecule heavy '
               'atoms: 9 (expected ~7), molecular weight: 148.1 Da\n'
               ' * SMILES: CCCCCCCCCCCCCCCC(=O)OC NAME: Methyl palmitate '
               'REASON: CORRECT Found a methyl ester group with an acyl chain '
               'of 15 carbon(s); internal rotatable bonds in chain: 13, '
               'overall rotatable bonds: 14, molecule heavy atoms: 19 '
               '(expected ~19), molecular weight: 270.3 Da\n'
               ' * SMILES: O=C(OC)CCC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC '
               'NAME: cis-5,8,11,14,17-eicosapentaenoic acid methyl ester '
               'REASON: CORRECT Found a methyl ester group with an acyl chain '
               'of 19 carbon(s); internal rotatable bonds in chain: 12, '
               'overall rotatable bonds: 13, molecule heavy atoms: 23 '
               '(expected ~23), molecular weight: 316.2 Da\n'
               ' * SMILES: O=C(OC)CCCCCCC/C=C\\CCCC NAME: methyl myristoleate '
               'REASON: CORRECT Found a methyl ester group with an acyl chain '
               'of 13 carbon(s); internal rotatable bonds in chain: 10, '
               'overall rotatable bonds: 11, molecule heavy atoms: 17 '
               '(expected ~17), molecular weight: 240.2 Da\n'
               ' * SMILES: O(C(=O)CC(CC(CCCCCCC)C)C)C NAME: formyl '
               '3,5-dimethyl-dodecanoate REASON: CORRECT Found a methyl ester '
               'group with an acyl chain of 11 carbon(s); internal rotatable '
               'bonds in chain: 9, overall rotatable bonds: 10, molecule heavy '
               'atoms: 17 (expected ~15), molecular weight: 242.2 Da\n'
               ' * SMILES: O=C(OC)CCCCCCCCCCCCCCCCCCCCCCC NAME: methyl '
               'tetracosanoate REASON: CORRECT Found a methyl ester group with '
               'an acyl chain of 23 carbon(s); internal rotatable bonds in '
               'chain: 21, overall rotatable bonds: 22, molecule heavy atoms: '
               '27 (expected ~27), molecular weight: 382.4 Da\n'
               ' * SMILES: O=C(OC)CCCCCCCCCCCCCCCCCCCCC NAME: methyl behenate '
               'REASON: CORRECT Found a methyl ester group with an acyl chain '
               'of 21 carbon(s); internal rotatable bonds in chain: 19, '
               'overall rotatable bonds: 20, molecule heavy atoms: 25 '
               '(expected ~25), molecular weight: 354.3 Da\n'
               ' * SMILES: O(C(=O)CCCCCCCCCC=CCCCCCCCC)C NAME: Methyl '
               '11-eicosenoate REASON: CORRECT Found a methyl ester group with '
               'an acyl chain of 19 carbon(s); internal rotatable bonds in '
               'chain: 16, overall rotatable bonds: 17, molecule heavy atoms: '
               '23 (expected ~23), molecular weight: 324.3 Da\n'
               ' * SMILES: O(C(=O)CCCCCC/C=C\\CCCCC(CC)C)C NAME: formyl '
               '14-methyl-8Z-hexadecenoate REASON: CORRECT Found a methyl '
               'ester group with an acyl chain of 15 carbon(s); internal '
               'rotatable bonds in chain: 12, overall rotatable bonds: 13, '
               'molecule heavy atoms: 20 (expected ~19), molecular weight: '
               '282.3 Da\n'
               ' * SMILES: CCCCCCCC\\C=C/CCCCCC(=O)OC NAME: methyl '
               '(Z)-7-hexadecenoate REASON: CORRECT Found a methyl ester group '
               'with an acyl chain of 15 carbon(s); internal rotatable bonds '
               'in chain: 12, overall rotatable bonds: 13, molecule heavy '
               'atoms: 19 (expected ~19), molecular weight: 268.2 Da\n'
               'False positives: SMILES: COC(=O)CCC(=O)CN NAME: methyl '
               '5-aminolevulinate REASON: WRONGLY CLASSIFIED Found a methyl '
               'ester group with an acyl chain of 4 carbon(s); internal '
               'rotatable bonds in chain: 2, overall rotatable bonds: 4, '
               'molecule heavy atoms: 10 (expected ~8), molecular weight: '
               '145.1 Da\n'
               ' * SMILES: COC(=O)\\C=C(/C)C(=O)OC NAME: Dimethyl citraconate '
               'REASON: WRONGLY CLASSIFIED Found a methyl ester group with an '
               'acyl chain of 5 carbon(s); internal rotatable bonds in chain: '
               '2, overall rotatable bonds: 2, molecule heavy atoms: 11 '
               '(expected ~9), molecular weight: 158.1 Da\n'
               ' * SMILES: O=C(OC)/C=C/CC(O)CCCCCC(O)C NAME: Cladosporester A '
               'REASON: WRONGLY CLASSIFIED Found a methyl ester group with an '
               'acyl chain of 11 carbon(s); internal rotatable bonds in chain: '
               '9, overall rotatable bonds: 9, molecule heavy atoms: 17 '
               '(expected ~15), molecular weight: 244.2 Da\n'
               ' * SMILES: O(C(=O)CCCCCCCCC(O)=O)C NAME: Sebacic acid '
               'monomethyl ester REASON: WRONGLY CLASSIFIED Found a methyl '
               'ester group with an acyl chain of 9 carbon(s); internal '
               'rotatable bonds in chain: 7, overall rotatable bonds: 9, '
               'molecule heavy atoms: 15 (expected ~13), molecular weight: '
               '216.1 Da\n'
               ' * SMILES: O(C(=O)\\C=C\\C=C/CCCCC)C NAME: Methyl '
               '(2E,4Z)-decadienoate REASON: WRONGLY CLASSIFIED Found a methyl '
               'ester group with an acyl chain of 9 carbon(s); internal '
               'rotatable bonds in chain: 6, overall rotatable bonds: 6, '
               'molecule heavy atoms: 13 (expected ~13), molecular weight: '
               '182.1 Da\n'
               ' * SMILES: '
               'O1[C@H]([C@@H]1C/C=C\\C/C=C\\CC)[C@H](O)/C=C\\C/C=C\\CCCC(OC)=O '
               'NAME: '
               'Methyl-(10S)-hydroxy-(11S,12S)-epoxy-(5Z,8Z,14Z,17Z)-eicosatetraenoate '
               'REASON: WRONGLY CLASSIFIED Found a methyl ester group with an '
               'acyl chain of 19 carbon(s); internal rotatable bonds in chain: '
               '12, overall rotatable bonds: 13, molecule heavy atoms: 25 '
               '(expected ~23), molecular weight: 348.2 Da\n'
               ' * SMILES: CCCCCCC(=O)OC NAME: Methyl heptanoate REASON: '
               'WRONGLY CLASSIFIED Found a methyl ester group with an acyl '
               'chain of 6 carbon(s); internal rotatable bonds in chain: 4, '
               'overall rotatable bonds: 5, molecule heavy atoms: 10 (expected '
               '~10), molecular weight: 144.1 Da\n'
               ' * SMILES: OC(CCCCC(C/C(/C)=C/C(/C)=C/C(O)=O)C)C(CO)C(OC)=O '
               'NAME: '
               '(2E,4E)-12-Hydroxy-13-(hydroxymethyl)-14-methoxy-3,5,7-trimethyl-14-oxotetradeca-2,4-dienoic '
               'acid REASON: WRONGLY CLASSIFIED Found a methyl ester group '
               'with an acyl chain of 15 carbon(s); internal rotatable bonds '
               'in chain: 11, overall rotatable bonds: 12, molecule heavy '
               'atoms: 25 (expected ~19), molecular weight: 356.2 Da\n'
               ' * SMILES: COC(=O)C(C)O NAME: methyl 2-hydroxypropionate '
               'REASON: WRONGLY CLASSIFIED Found a methyl ester group with an '
               'acyl chain of 3 carbon(s); internal rotatable bonds in chain: '
               '1, overall rotatable bonds: 1, molecule heavy atoms: 7 '
               '(expected ~7), molecular weight: 104.0 Da\n'
               ' * SMILES: O(C(=O)C[C@H](CCC=C(C)C)C)C NAME: '
               '(S)-(-)-Citronellic acid, methyl ester REASON: WRONGLY '
               'CLASSIFIED Found a methyl ester group with an acyl chain of 7 '
               'carbon(s); internal rotatable bonds in chain: 4, overall '
               'rotatable bonds: 5, molecule heavy atoms: 13 (expected ~11), '
               'molecular weight: 184.1 Da\n'
               ' * SMILES: O(C(=O)\\C=C\\C=C/C=C\\CCC)C NAME: formyl '
               '2E,4Z,6Z-decatrienoate REASON: WRONGLY CLASSIFIED Found a '
               'methyl ester group with an acyl chain of 9 carbon(s); internal '
               'rotatable bonds in chain: 5, overall rotatable bonds: 5, '
               'molecule heavy atoms: 13 (expected ~13), molecular weight: '
               '180.1 Da\n'
               ' * SMILES: COC(=O)[C@@H](N)CCC(O)=O NAME: L-glutamate methyl '
               'ester REASON: WRONGLY CLASSIFIED Found a methyl ester group '
               'with an acyl chain of 4 carbon(s); internal rotatable bonds in '
               'chain: 2, overall rotatable bonds: 4, molecule heavy atoms: 11 '
               '(expected ~8), molecular weight: 161.1 Da\n'
               ' * SMILES: O=C1[C@H]([C@@H](CCCCCC(=O)OC)CC1)C/C=C\\CC NAME: '
               '(1S,2S)-3-oxo-2-(2Z-pentenyl)cyclopentane-1-hexanoic acid '
               'methyl ester REASON: WRONGLY CLASSIFIED Found a methyl ester '
               'group with an acyl chain of 15 carbon(s); internal rotatable '
               'bonds in chain: 8, overall rotatable bonds: 9, molecule heavy '
               'atoms: 20 (expected ~19), molecular weight: 280.2 Da\n'
               ' * SMILES: COC(=O)\\C=C(/C)CC\\C=C(/C)CC[C@H]1O[C@]1(C)CO '
               'NAME: 12-trans-Hydroxy juvenile hormone III REASON: WRONGLY '
               'CLASSIFIED Found a methyl ester group with an acyl chain of 11 '
               'carbon(s); internal rotatable bonds in chain: 7, overall '
               'rotatable bonds: 8, molecule heavy atoms: 20 (expected ~15), '
               'molecular weight: 282.2 Da\n'
               ' * SMILES: '
               'ClC1=C[C@@](O)([C@@]([C@@H](OC(=O)C)/C=C\\CCCC(OC)=O)(C1=O)[H])C/C=C\\CCCCC '
               'NAME: punaglandin 8 REASON: WRONGLY CLASSIFIED Found a methyl '
               'ester group with an acyl chain of 19 carbon(s); internal '
               'rotatable bonds in chain: 11, overall rotatable bonds: 13, '
               'molecule heavy atoms: 30 (expected ~23), molecular weight: '
               '440.2 Da\n'
               ' * SMILES: O(C(=O)CCC(=O)C)C NAME: Methyl levulinate REASON: '
               'WRONGLY CLASSIFIED Found a methyl ester group with an acyl '
               'chain of 4 carbon(s); internal rotatable bonds in chain: 2, '
               'overall rotatable bonds: 3, molecule heavy atoms: 9 (expected '
               '~8), molecular weight: 130.1 Da\n'
               ' * SMILES: '
               'CCCC[C@@](C)(O)C\\C=C\\[C@@H]1[C@@H](O)CC(=O)[C@H]1CCCCCCC(=O)OC '
               'NAME: (11S,16R)-misoprostol REASON: WRONGLY CLASSIFIED Found a '
               'methyl ester group with an acyl chain of 19 carbon(s); '
               'internal rotatable bonds in chain: 12, overall rotatable '
               'bonds: 13, molecule heavy atoms: 27 (expected ~23), molecular '
               'weight: 382.3 Da\n'
               ' * SMILES: '
               'C(=C/[C@H](C[C@H](CCCC)C)O)\\[C@@H]1[C@@H](CC(CCCCC(OC)=O)=O)C(C[C@H]1O)=O '
               'NAME: Ornoprostil REASON: WRONGLY CLASSIFIED Found a methyl '
               'ester group with an acyl chain of 20 carbon(s); internal '
               'rotatable bonds in chain: 13, overall rotatable bonds: 14, '
               'molecule heavy atoms: 29 (expected ~24), molecular weight: '
               '410.3 Da\n'
               ' * SMILES: '
               'C(=C/[C@H](C(CCCC)(C)C)O)\\[C@@H]1[C@@H](CCCC/C=C/C(OC)=O)C(C[C@H]1O)=O '
               'NAME: gemeprost REASON: WRONGLY CLASSIFIED Found a methyl '
               'ester group with an acyl chain of 19 carbon(s); internal '
               'rotatable bonds in chain: 12, overall rotatable bonds: 12, '
               'molecule heavy atoms: 28 (expected ~23), molecular weight: '
               '394.3 Da\n'
               ' * SMILES: O=C1C(=C(CCC)O[C@@]1(/C=C/CC[C@H](O)C)C)C(=O)OC '
               'NAME: Gregatin F1 REASON: WRONGLY CLASSIFIED Found a methyl '
               'ester group with an acyl chain of 11 carbon(s); internal '
               'rotatable bonds in chain: 5, overall rotatable bonds: 7, '
               'molecule heavy atoms: 21 (expected ~15), molecular weight: '
               '296.2 Da\n'
               ' * SMILES: '
               'O=C(OC)C/1=C2C(=COC(=C2)C)[C@](\\C1=C/C(=O)[C@@H](CCCCCC)C)(O)C '
               'NAME: Sequoiatone B REASON: WRONGLY CLASSIFIED Found a methyl '
               'ester group with an acyl chain of 14 carbon(s); internal '
               'rotatable bonds in chain: 8, overall rotatable bonds: 8, '
               'molecule heavy atoms: 27 (expected ~18), molecular weight: '
               '374.2 Da\n'
               ' * SMILES: '
               'O(O)C(C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)/C=C\\CCC(OC)=O NAME: '
               'methyl 6-hydroperoxy-4,8,11,14,17-eicosapentaenoate REASON: '
               'WRONGLY CLASSIFIED Found a methyl ester group with an acyl '
               'chain of 19 carbon(s); internal rotatable bonds in chain: 12, '
               'overall rotatable bonds: 14, molecule heavy atoms: 25 '
               '(expected ~23), molecular weight: 348.2 Da\n'
               ' * SMILES: C(C(=O)OC)[C@@H]1[C@H](C(CC1)=O)CCCCC NAME: Methyl '
               'dihydrojasmonate REASON: WRONGLY CLASSIFIED Found a methyl '
               'ester group with an acyl chain of 11 carbon(s); internal '
               'rotatable bonds in chain: 5, overall rotatable bonds: 6, '
               'molecule heavy atoms: 16 (expected ~15), molecular weight: '
               '226.2 Da\n'
               ' * SMILES: O=C(OC)CCC[C@@H](O)C#CC#C[C@@H]1O[C@H]1CO NAME: '
               'Pyranone D REASON: WRONGLY CLASSIFIED Found a methyl ester '
               'group with an acyl chain of 11 carbon(s); internal rotatable '
               'bonds in chain: 6, overall rotatable bonds: 5, molecule heavy '
               'atoms: 18 (expected ~15), molecular weight: 252.1 Da\n'
               ' * SMILES: '
               'O[C@@H]1[C@@H]([C@H]([C@H](O)C1)/C=C/[C@@](O)(CCCCC)C)C/C=C\\CCCC(OC)=O '
               'NAME: 15-methyl-15R-PGF2alpha methyl ester REASON: WRONGLY '
               'CLASSIFIED Found a methyl ester group with an acyl chain of 19 '
               'carbon(s); internal rotatable bonds in chain: 11, overall '
               'rotatable bonds: 12, molecule heavy atoms: 27 (expected ~23), '
               'molecular weight: 382.3 Da\n'
               'False negatives: SMILES: O(C(=O)CCCC1=CC=CC=C1)C NAME: Methyl '
               '4-phenylbutanoate REASON: MISSED Molecule contains a methyl '
               'ester group but the acyl portion does not meet fatty acid '
               'criteria\n'
               ' * SMILES: O(C(=O)CCC(OC)=O)CC NAME: Ethyl methyl_succinate '
               'REASON: MISSED Molecule contains a methyl ester group but the '
               'acyl portion does not meet fatty acid criteria\n'
               ' * SMILES: C1CC2C1C3C2C4C3C5C4C(C5)CCCCCC(OC)=O NAME: methyl '
               '6-(pentacyclo[6.4.0.0(2,7).0(3,6).0(9,12)]dodec-4-yl)hexanoate '
               'REASON: MISSED Molecule contains a methyl ester group but the '
               'acyl portion does not meet fatty acid criteria\n'
               ' * SMILES: S1C(\\C=C\\CC(OC)=O)=CC=C1 NAME: Methyl '
               '(3E)-4-(2-thienyl)-3-butenoate REASON: MISSED Molecule '
               'contains a methyl ester group but the acyl portion does not '
               'meet fatty acid criteria\n'
               ' * SMILES: COC(=O)CCCC(=O)N1CCOCCN(CCOCC1)C(=O)CCCC(=O)OC '
               'NAME: '
               '5-[10-(5-methoxy-1,5-dioxopentyl)-1,7-dioxa-4,10-diazacyclododec-4-yl]-5-oxopentanoic '
               'acid methyl ester REASON: MISSED Molecule contains a methyl '
               'ester group but the acyl portion does not meet fatty acid '
               'criteria\n'
               ' * SMILES: C1CC2C1C3C2C4C3CCC(C4)CCCCCCCC(OC)=O NAME: methyl '
               '8-(tetracyclo[6.4.0.0(2,7).0(3,6)]dodec-10-yl)octanoate '
               'REASON: MISSED Molecule contains a methyl ester group but the '
               'acyl portion does not meet fatty acid criteria\n'
               ' * SMILES: O=C(OC)CCC(=O)NCCCCCN(O)C(=O)CC(C)C NAME: '
               'Tenacibactin A REASON: MISSED Molecule contains a methyl ester '
               'group but the acyl portion does not meet fatty acid criteria\n'
               ' * SMILES: '
               '[C@@]12([C@]3([C@@]([C@]1([C@@]4(CC[C@]24[H])[H])[H])([C@]5([C@@]3(C[C@@H]5CCCCCCCC(OC)=O)[H])[H])[H])[H])[H] '
               'NAME: methyl (+)-pentacycloanammoxate REASON: MISSED Molecule '
               'contains a methyl ester group but the acyl portion does not '
               'meet fatty acid criteria\n'
               ' * SMILES: FC(F)(F)C(OC)(O)CC(OC)=O NAME: Methyl '
               '4,4,4-trifluoro-3-hydroxy-3-methoxybutanoate REASON: MISSED '
               'Molecule contains a methyl ester group but the acyl portion '
               'does not meet fatty acid criteria\n'
               ' * SMILES: COC(=O)CCCCCCC(=O)NN=C[C@H]([C@@H]([C@@H](CO)O)O)O '
               'NAME: LSM-36666 REASON: MISSED Molecule contains a methyl '
               'ester group but the acyl portion does not meet fatty acid '
               'criteria\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'O=C(N[C@@H](C(O)(C)C)C)[C@H]([C@@]1([C@@]2([C@@](CC1)(/C(/CCC2)=C/C=C\\3/C[C@@H](O)C[C@H](O)C3=C)[H])C)[H])C',
                                     'name': '1alpha,25-dihydroxy-24-oxo-23-azavitamin '
                                             'D2 / '
                                             '1alpha,25-dihydroxy-24-oxo-23-azaergocalciferol',
                                     'reason': 'No methyl ester group found in '
                                               'the molecule'},
                                 {   'smiles': 'CCCCCCCCCCCCCCCCCCC(O)C([O-])=O',
                                     'name': '2-hydroxyarachidate',
                                     'reason': 'No methyl ester group found in '
                                               'the molecule'},
                                 {   'smiles': 'C[C@@H](CN([C@@H](C)CO)C(=O)NC1=CC=C(C=C1)C(F)(F)F)[C@@H](CN(C)C(=O)C2CCOCC2)OC',
                                     'name': 'N-[(2S,3S)-4-[[(2S)-1-hydroxypropan-2-yl]-[[4-(trifluoromethyl)phenyl]carbamoyl]amino]-2-methoxy-3-methylbutyl]-N-methyloxane-4-carboxamide',
                                     'reason': 'No methyl ester group found in '
                                               'the molecule'},
                                 {   'smiles': 'CC(=O)CC\\C=C(/C)CCC=C(C)C',
                                     'name': 'geranyl acetone',
                                     'reason': 'No methyl ester group found in '
                                               'the molecule'},
                                 {   'smiles': 'O([C@H]1[C@H](O)[C@H](O[C@H](O)[C@H]1O)CO[C@H]2O[C@@H]([C@@H](O)[C@H](O)[C@@H]2O)CO)[C@H]3O[C@@H]([C@@H](O)[C@H](O)[C@@H]3O[C@H]4O[C@@H]([C@@H](O)[C@H](O)[C@@H]4O)CO)CO',
                                     'name': '(2S,3S,4S,5S,6R)-2-[[(2R,3R,4S,5S,6S)-4-[(2R,3S,4S,5S,6R)-4,5-Dihydroxy-6-(hydroxymethyl)-3-[(2R,3S,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-3,5,6-trihydroxyoxan-2-yl]methoxy]-6-(hydroxymethyl)oxane-3,4,5-triol',
                                     'reason': 'No methyl ester group found in '
                                               'the molecule'},
                                 {   'smiles': 'O=C(OC1=C(C(O)=C(C(=O)O)C(=C1C)C)C)C2=C(OC)C(=C(OC(=O)C3=C(O)C=C(O)C=C3C)C=C2C)C',
                                     'name': 'Thielavin Z5',
                                     'reason': 'No methyl ester group found in '
                                               'the molecule'},
                                 {   'smiles': '[C@@H]1([C@@H]([C@H]([C@@H]([C@H](O1)CO)O)O)NC(C)=O)O[C@@H]2[C@@H]([C@H](C(O[C@@H]2CO)O)O)O',
                                     'name': 'beta-D-GlcpNAc-(1->4)-D-Galp',
                                     'reason': 'No methyl ester group found in '
                                               'the molecule'},
                                 {   'smiles': 'CN(C)C(=O)C1=CC=C(C=C1)C2=CC=C(C=C2)[C@@H]3[C@H]4CN(CC(=O)N4[C@H]3CO)C(=O)CC5CC5',
                                     'name': '4-[4-[(6S,7R,8R)-4-(2-cyclopropyl-1-oxoethyl)-8-(hydroxymethyl)-2-oxo-1,4-diazabicyclo[4.2.0]octan-7-yl]phenyl]-N,N-dimethylbenzamide',
                                     'reason': 'No methyl ester group found in '
                                               'the molecule'},
                                 {   'smiles': 'CCCCCCCCCCCCCCCCCCCCC=C',
                                     'name': '1-docosene',
                                     'reason': 'No methyl ester group found in '
                                               'the molecule'},
                                 {   'smiles': 'C([C@@](OC(=O)CCC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)([H])COC(=O)CC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)OC(=O)CCCCC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC',
                                     'name': 'TG(22:5(7Z,10Z,13Z,16Z,19Z)/20:5(5Z,8Z,11Z,14Z,17Z)/22:6(4Z,7Z,10Z,13Z,16Z,19Z))[iso6]',
                                     'reason': 'No methyl ester group found in '
                                               'the molecule'}],
    'sample_false_negatives': [   {   'smiles': 'CCCCCC1C(C/C(=C(\\C\\C(=C(\\[H])/CCCCCCC(=O)OC)\\[H])/[H])/[H])O1',
                                      'name': '13-(3-pentyl-2-oxiranyl)-(8Z,11Z)-8,11-tridecadienoic '
                                              'acid methyl ester',
                                      'reason': 'Molecule contains a methyl '
                                                'ester group but the acyl '
                                                'portion does not meet fatty '
                                                'acid criteria'},
                                  {   'smiles': 'O[C@H](CCCCCCCC(OC)=O)/C=C/C=C/CCCCC',
                                      'name': '9R-hydroxy-10E,12E-octadecadienoic '
                                              'acid, methyl ester',
                                      'reason': 'Molecule contains a methyl '
                                                'ester group but the acyl '
                                                'portion does not meet fatty '
                                                'acid criteria'},
                                  {   'smiles': 'SC(CC(OC)=O)C',
                                      'name': 'Methyl 3-mercaptobutanoate',
                                      'reason': 'Molecule contains a methyl '
                                                'ester group but the acyl '
                                                'portion does not meet fatty '
                                                'acid criteria'},
                                  {   'smiles': 'COC(=O)[C@@H]1O[C@@]1(C)CC\\C=C(/C)CC[C@H]1OC1(C)C',
                                      'name': 'juvenile hormone III skipped '
                                              'bisepoxide',
                                      'reason': 'Molecule contains a methyl '
                                                'ester group but the acyl '
                                                'portion does not meet fatty '
                                                'acid criteria'},
                                  {   'smiles': 'O1[C@@H]([C@H]1C#CC#CCCC(OC)=O)CCC\\C=C/C=C\\CC',
                                      'name': 'methyl '
                                              '8R,9R-epoxy-13Z,15Z-eicosadien-4,6-diynoate',
                                      'reason': 'Molecule contains a methyl '
                                                'ester group but the acyl '
                                                'portion does not meet fatty '
                                                'acid criteria'},
                                  {   'smiles': 'CCCCC\\C=C/C\\C=C/C=C/C(C\\C=C/CCCC(=O)OC)OO',
                                      'name': '8-HPETE methyl ester',
                                      'reason': 'Molecule contains a methyl '
                                                'ester group but the acyl '
                                                'portion does not meet fatty '
                                                'acid criteria'},
                                  {   'smiles': 'O(C(=O)CCCC1=CC=CC=C1)C',
                                      'name': 'Methyl 4-phenylbutanoate',
                                      'reason': 'Molecule contains a methyl '
                                                'ester group but the acyl '
                                                'portion does not meet fatty '
                                                'acid criteria'},
                                  {   'smiles': 'O(C(=O)CCC(OC)=O)CC',
                                      'name': 'Ethyl methyl_succinate',
                                      'reason': 'Molecule contains a methyl '
                                                'ester group but the acyl '
                                                'portion does not meet fatty '
                                                'acid criteria'},
                                  {   'smiles': 'S(C(CC(OC)=O)C)C',
                                      'name': 'Methyl 3-(methylthio)butanoate',
                                      'reason': 'Molecule contains a methyl '
                                                'ester group but the acyl '
                                                'portion does not meet fatty '
                                                'acid criteria'},
                                  {   'smiles': 'O(OC(C)(C)C)C(CCCCC)/C=C/C=C/CCCCCCCC(OC)=O',
                                      'name': 'methyl '
                                              '13-butylperoxy-9,11-octadecadienoate',
                                      'reason': 'Molecule contains a methyl '
                                                'ester group but the acyl '
                                                'portion does not meet fatty '
                                                'acid criteria'}],
    'attempt': 3,
    'reasoning': 'Below is our revised solution. In our reasoning we noticed '
                 'that basing the fatty acid methyl ester decision solely on '
                 'finding a methyl‐ester SMARTS and then “walking” the chain '
                 'led to both false positives (for molecules whose acyl '
                 'fragment was decorated or unusually short) and false '
                 'negatives (for cases where extra functionality was present '
                 'that invalidated a simple fatty acid “tail”). To improve '
                 'performance we now (1) require a clear methyl ester '
                 'substructure, (2) identify the acyl chain by following only '
                 'carbon atoms not marked aromatic (so that aromatic '
                 'substituents or secondary ester functions are rejected), (3) '
                 'compute a longest‐path for the acyl chain that must be at '
                 'least 3 carbons long, (4) check that any substituents '
                 'branching off this chain are “trivial” (i.e. if they are not '
                 'carbons or are more than a single atom long then we assume '
                 'extra decoration) and (5) finally compare the molecule’s '
                 'heavy atom count to a minimal expected count (chain length + '
                 'four atoms for the “ester” part) so that molecules with '
                 'extra functionality are rejected.\n'
                 '\n'
                 'Below is the complete Python code (using RDKit) in a single '
                 'code block.\n'
                 '\n'
                 '------------------------------------------------',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 77,
    'num_false_positives': 24,
    'num_true_negatives': 142135,
    'num_false_negatives': 64,
    'num_negatives': None,
    'precision': 0.7623762376237624,
    'recall': 0.5460992907801419,
    'f1': 0.6363636363636364,
    'accuracy': 0.9993815881939564,
    'negative_predictive_value': 0.9995499265114381}