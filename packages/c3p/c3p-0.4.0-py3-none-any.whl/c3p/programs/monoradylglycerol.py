"""
Classifies: CHEBI:76575 monoradylglycerol
"""
"""
Classifies: monoradylglycerol
Definition: Any lipid that is glycerol bearing a single acyl, alkyl or alk-1-enyl substituent (and nothing else).
Approach: 
  1. Find a glycerol-like backbone candidate defined as three sp3 carbons (in a linear array, with
     the two end carbons not directly bonded) each having exactly one oxygen neighbor not in the backbone.
  2. Among the three oxygen neighbors, exactly two must be “free” (i.e. have at least one implicit hydrogen)
     and one “substituted” (i.e. no H attached).
  3. The substituted oxygen should be attached to a carbon (the “anchor”). We then check the nature of the link:
     if this oxygen–carbon bond is an ester (the anchor bears a double‐bonded oxygen, i.e. a carbonyl) then we label
     the substituent as acyl (which allows shorter chains, e.g. acetate), otherwise it is assumed to be an alkyl linkage,
     and we require a minimum substituent (alkyl) chain length (here, chosen to be ≥8 carbons) in order to avoid mis‐classification.
  4. We perform a DFS from the substituent anchor (walking only over carbon atoms and aborting if any ring is encountered)
     to “collect” the chain. In addition, for an ester the carbonyl oxygen is added.
  5. Finally we “assemble” the candidate fragment (glycerol backbone carbons, its three oxygen substituents, 
     the substituent chain and, if appropriate, the carbonyl oxygen) and require that the set of heavy atoms in the candidate 
     exactly equals the heavy atoms in the molecule.
  
Due to the heuristic nature of this approach (and limitations in our choices for SMARTS/DFS) a molecule that is too “exotic”
may not be recognized. In that case (or if an unexpected error occurs) the function returns (None, None).
"""
from rdkit import Chem

def is_monoradylglycerol(smiles: str):
    """
    Determines if a molecule is a monoradylglycerol based on its SMILES string.
    
    The algorithm attempts to find a glycerol backbone candidate (three sp3 carbons in a row,
    each bearing one oxygen substituent) with exactly two free –OH groups and one substituted oxygen.
    The substituted oxygen must be attached to one carbon (the substituent anchor) from which we traverse a chain.
    If the substituent anchor has a double-bonded oxygen (ester linkage), we allow a short chain (min length 2),
    otherwise (ether linkage) we require a longer chain (min length 8). Finally, we require that the candidate fragment
    exactly equals the entire set of heavy atoms of the molecule.
    
    Args:
       smiles (str): SMILES string of the molecule.
       
    Returns:
       bool: True if the candidate fragment matches the entire molecule.
       str: Reason for the classification.
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
    
    # Helper: DFS to traverse contiguous chain of carbons (no rings allowed)
    def dfs_chain(atom, blocked_ids, visited):
        if atom.GetAtomicNum() != 6:
            return set()
        if atom.IsInRing():
            return None  # abort branch: rings not allowed
        visited.add(atom.GetIdx())
        chain_set = {atom.GetIdx()}
        for nbr in atom.GetNeighbors():
            if nbr.GetIdx() in blocked_ids or nbr.GetIdx() in visited:
                continue
            if nbr.GetAtomicNum() == 6:
                result = dfs_chain(nbr, blocked_ids, visited)
                if result is None:
                    return None
                chain_set.update(result)
        return chain_set

    # Iterate over potential candidate middle carbons in a glycerol backbone.
    for atom in mol.GetAtoms():
        # Look for sp3 carbons only.
        if atom.GetAtomicNum() != 6 or atom.GetHybridization().name != "SP3":
            continue
        # Candidate middle carbon must have exactly two sp3 carbon neighbors.
        nbr_carbons = [nbr for nbr in atom.GetNeighbors() 
                       if nbr.GetAtomicNum() == 6 and nbr.GetHybridization().name == "SP3"]
        if len(nbr_carbons) != 2:
            continue
        # Ensure terminal carbons are not directly bonded (to force a chain, not a cycle)
        if mol.GetBondBetweenAtoms(nbr_carbons[0].GetIdx(), nbr_carbons[1].GetIdx()):
            continue

        backbone = [nbr_carbons[0], atom, nbr_carbons[1]]
        backbone_ids = set(a.GetIdx() for a in backbone)
        
        # For a glycerol backbone, each backbone carbon must have exactly one oxygen neighbor (not in backbone)
        oxygen_neighbors = []
        valid_backbone = True
        for carbon in backbone:
            oxygens = [nbr for nbr in carbon.GetNeighbors() 
                       if nbr.GetAtomicNum() == 8 and nbr.GetIdx() not in backbone_ids]
            if len(oxygens) != 1:
                valid_backbone = False
                break
            oxygen_neighbors.append(oxygens[0])
        if not valid_backbone:
            continue
        
        # Count free -OH (oxygen with at least one hydrogen) vs substituted oxygen (with no H)
        free_OH_count = 0
        substituted_index = -1
        for idx, o_atom in enumerate(oxygen_neighbors):
            # GetTotalNumHs works whether hydrogens are explicit or implicit.
            if o_atom.GetTotalNumHs() > 0:
                free_OH_count += 1
            else:
                substituted_index = idx
        # For monoradylglycerol, exactly two must be free OH and one is substituted.
        if free_OH_count != 2 or substituted_index < 0:
            continue

        # Focus on the substituted oxygen.
        sub_o = oxygen_neighbors[substituted_index]
        # Find its connection to the backbone (should be only one).
        parent_carbon = None
        for nbr in sub_o.GetNeighbors():
            if nbr.GetIdx() in backbone_ids:
                parent_carbon = nbr
                break
        if parent_carbon is None:
            continue
        
        # Identify substituent anchor: the non-backbone neighbor of the substituted oxygen.
        sub_neighbors = [nbr for nbr in sub_o.GetNeighbors() if nbr.GetIdx() not in backbone_ids]
        if len(sub_neighbors) != 1:
            continue
        sub_anchor = sub_neighbors[0]
        if sub_anchor.GetAtomicNum() != 6:
            continue

        # Determine linkage type. For an ester (acyl chain), the substituent oxygen is linked to a carbonyl.
        # In that case, sub_anchor should have at least one neighbor (other than sub_o) which is oxygen
        # and connected by a double bond.
        is_acyl = False
        for nbr in sub_anchor.GetNeighbors():
            if nbr.GetIdx() == sub_o.GetIdx():
                continue
            if nbr.GetAtomicNum() == 8:
                bond = mol.GetBondBetweenAtoms(sub_anchor.GetIdx(), nbr.GetIdx())
                if bond is not None and bond.GetBondTypeAsDouble() == 2.0:
                    is_acyl = True
                    carbonyl_o = nbr  # record the carbonyl oxygen
                    break

        # Now traverse the substituent chain starting at sub_anchor.
        visited = set()
        chain_set = dfs_chain(sub_anchor, blocked_ids=backbone_ids, visited=visited)
        if chain_set is None:
            continue  # ring encountered – reject candidate
        
        # Define minimum chain length (number of carbon atoms in substituent) depending on linkage type.
        if is_acyl:
            MIN_CHAIN_LENGTH = 2  # even acetate (2 carbons) is allowed
        else:
            MIN_CHAIN_LENGTH = 8  # reject short alkyl chains (e.g. 6-carbon chain is not acceptable here)
        if len(chain_set) < MIN_CHAIN_LENGTH:
            continue

        # For ester linkage, also include the carbonyl oxygen if not already in the chain.
        extra_atoms = set()
        if is_acyl:
            if carbonyl_o.GetIdx() not in chain_set:
                extra_atoms.add(carbonyl_o.GetIdx())

        # Assemble candidate fragment: backbone carbons, all three oxygen neighbors, substituent chain carbons and (if ester) the carbonyl O.
        candidate_atom_ids = set()
        candidate_atom_ids.update(backbone_ids)
        for o in oxygen_neighbors:
            candidate_atom_ids.add(o.GetIdx())
        candidate_atom_ids.update(chain_set)
        candidate_atom_ids.update(extra_atoms)
        
        # Get heavy-atom indices of whole molecule.
        all_heavy_atom_ids = set(a.GetIdx() for a in mol.GetAtoms() if a.GetAtomicNum() > 1)
        
        # To accept candidate, the candidate fragment must account for ALL heavy atoms.
        if candidate_atom_ids == all_heavy_atom_ids:
            # Determine substitution position (1,2, or 3)
            pos = substituted_index + 1
            chain_type = "acyl" if is_acyl else "alkyl/alk-1-enyl"
            reason = (f"Found glycerol backbone (atoms {', '.join(str(a.GetIdx()) for a in backbone)}) with substitution "
                      f"at position {pos} via {chain_type} linkage; substituent chain length = {len(chain_set)}; free -OH groups = 2.")
            return True, reason
        # If candidate fragment does not equal full molecule, try next candidate.
    return False, "No glycerol backbone with one substituted oxygen (and two free –OH groups) forming an isolated candidate fragment was found."

# Example usage:
if __name__ == '__main__':
    test_smiles = [
        # True positives (should be classified as monoradylglycerol)
        "O=C(OC[C@@H](O)CO)CCCCCCC/C=C(\\CCCCCCCC)/C",  # 2,3-dihydroxypropyl (Z)-10-methyloctadec-9-enoate
        "CCCCCCCC(=O)OCC(O)CO",                         # 1-monooctanoylglycerol
        "CCCCCCCCCCCCCCCCCC(=O)OC[C@H](O)CO",           # 3-stearoyl-sn-glycerol
        "O(C(=O)CCCCCCCCCCC/C=C\\C/C=C\\CCCCC)C[C@@H](O)CO",  # MG(22:2(13Z,16Z)/0:0/0:0)
        "O(C[C@@H](O)CO)C(=O)C",                        # (R)-glycerol 1-acetate
        "CCCCCCCCCCCCCCCCCOC[C@@H](O)CO",               # 1-O-octadecyl-sn-glycerol
        # False positives (should not be classified as monoradylglycerol)
        "O(CCCCCC)C(CO)CO",                             # 2-Hexylglycerol (linkage is ether but chain too short: 6 carbons)
        # False negatives (should be monoradylglycerol but might be missed if backbone not recognized)
        "O=C(CCC/C=C\\C\\C=C/C=C/C(C/C=C\\CCCCC)OO)OC(CO)CO",  # 12-HPETE 2-glyceryl ester
    ]
    
    for s in test_smiles:
        result, reason = is_monoradylglycerol(s)
        print(f"SMILES: {s}\nResult: {result}\nReason: {reason}\n")


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:76575',
                          'name': 'monoradylglycerol',
                          'definition': 'Any lipid that is glycerol bearing a '
                                        'single acyl, alkyl or alk-1-enyl '
                                        'substituent at an unspecified '
                                        'position.',
                          'parents': ['CHEBI:35741'],
                          'xrefs': ['LIPID_MAPS_class:LMGL0101'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 64,
                           'log_lines_of_code': 4.1588830833596715,
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
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 3,
                                                 2,
                                                 3,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 4,
                                                 3,
                                                 4,
                                                 4,
                                                 5,
                                                 4,
                                                 2,
                                                 0,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 3,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 2,
                                                 2,
                                                 3,
                                                 0,
                                                 0,
                                                 0,
                                                 0,
                                                 0,
                                                 0,
                                                 0,
                                                 0,
                                                 0,
                                                 0,
                                                 0,
                                                 0,
                                                 1,
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
                                                 2,
                                                 2,
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 2],
                           'max_indent': 5,
                           'imports': ['from rdkit import Chem'],
                           'imports_count': 1,
                           'methods_called': [   'GetHybridization',
                                                 'GetNeighbors',
                                                 'GetBondBetweenAtoms',
                                                 'GetAtoms',
                                                 'add',
                                                 'GetAtomicNum',
                                                 'update',
                                                 'IsInRing',
                                                 'MolFromSmiles',
                                                 'GetIdx'],
                           'methods_called_count': 10,
                           'smarts_strings': [],
                           'smarts_strings_count': 0,
                           'defs': [   'is_monoradylglycerol(smiles: str):',
                                       'dfs_chain(atom, blocked_ids, '
                                       'visited):'],
                           'defs_count': 2,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'set()',
                                          'None  # abort branch: rings not '
                                          'allowed',
                                          'None',
                                          'chain_set',
                                          'False, "No glycerol backbone with '
                                          'one substituted oxygen (and two '
                                          'free –OH groups) forming an '
                                          'isolated candidate fragment was '
                                          'found."'],
                           'returns_count': 6,
                           'complexity': 5.431776616671934},
    'message': '\n'
               'Attempt failed: F1 score of 0.7999999999999999 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: '
               'O=C(OC[C@@H](O)CO)CCCCCCC/C=C(\\CCCCCCCC)/C NAME: '
               '2,3-dihydroxypropyl (Z)-10-methyloctadec-9-enoate REASON: '
               'CORRECT Found glycerol backbone (atoms 3, 4, 6) with '
               'substitution at position 1; substituent chain length = 19, '
               'free -OH groups = 2.\n'
               ' * SMILES: CCCCCCCC(=O)OCC(O)CO NAME: 1-monooctanoylglycerol '
               'REASON: CORRECT Found glycerol backbone (atoms 10, 11, 13) '
               'with substitution at position 1; substituent chain length = 8, '
               'free -OH groups = 2.\n'
               ' * SMILES: CCCCCCCCCCCCCCCCCC(=O)OC[C@H](O)CO NAME: '
               '3-stearoyl-sn-glycerol REASON: CORRECT Found glycerol backbone '
               '(atoms 20, 21, 23) with substitution at position 1; '
               'substituent chain length = 18, free -OH groups = 2.\n'
               ' * SMILES: O(C(=O)CCCCCCCCCCC/C=C\\C/C=C\\CCCCC)C[C@@H](O)CO '
               'NAME: MG(22:2(13Z,16Z)/0:0/0:0) REASON: CORRECT Found glycerol '
               'backbone (atoms 24, 25, 27) with substitution at position 1; '
               'substituent chain length = 22, free -OH groups = 2.\n'
               ' * SMILES: '
               'C([C@@](COC(CCCC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)=O)(O)[H])O '
               'NAME: MG(24:6(6Z,9Z,12Z,15Z,18Z,21Z)/0:0/0:0) REASON: CORRECT '
               'Found glycerol backbone (atoms 0, 1, 2) with substitution at '
               'position 3; substituent chain length = 24, free -OH groups = '
               '2.\n'
               ' * SMILES: OCC(OC(=O)CCCCCCC/C=C/CCCCCCCC)CO NAME: '
               '2-[(9E)-9-octadecenoyl]glycerol REASON: CORRECT Found glycerol '
               'backbone (atoms 1, 2, 23) with substitution at position 2; '
               'substituent chain length = 18, free -OH groups = 2.\n'
               ' * SMILES: CCCCCCCC\\C=C/CCCCCCCC(=O)OCC(O)CO NAME: '
               '1-oleoylglycerol REASON: CORRECT Found glycerol backbone '
               '(atoms 20, 21, 23) with substitution at position 1; '
               'substituent chain length = 18, free -OH groups = 2.\n'
               ' * SMILES: O(C[C@@H](O)CO)C(=O)C NAME: (R)-glycerol 1-acetate '
               'REASON: CORRECT Found glycerol backbone (atoms 1, 2, 4) with '
               'substitution at position 1; substituent chain length = 2, free '
               '-OH groups = 2.\n'
               ' * SMILES: CCCCC\\C=C/C\\C=C/CCCCCCCC(=O)OC[C@H](O)CO NAME: '
               '3-linoleoyl-sn-glycerol REASON: CORRECT Found glycerol '
               'backbone (atoms 20, 21, 23) with substitution at position 1; '
               'substituent chain length = 18, free -OH groups = 2.\n'
               ' * SMILES: CCCCCCCCCCCC(=O)OC(CO)CO NAME: 2-lauroylglycerol '
               'REASON: CORRECT Found glycerol backbone (atoms 15, 14, 17) '
               'with substitution at position 2; substituent chain length = '
               '12, free -OH groups = 2.\n'
               ' * SMILES: CCCCCCCCCCCCCC(=O)OC(CO)CO NAME: '
               '2-tetradecanoylglycerol REASON: CORRECT Found glycerol '
               'backbone (atoms 17, 16, 19) with substitution at position 2; '
               'substituent chain length = 14, free -OH groups = 2.\n'
               ' * SMILES: O(CC(O)CO)C(=O)C(C)=CC NAME: Glyceryl '
               'methylmethacrylate REASON: CORRECT Found glycerol backbone '
               '(atoms 1, 2, 4) with substitution at position 1; substituent '
               'chain length = 5, free -OH groups = 2.\n'
               ' * SMILES: CCCCCCCCCC(=O)OC[C@H](O)CO NAME: '
               '3-decanoyl-sn-glycerol REASON: CORRECT Found glycerol backbone '
               '(atoms 12, 13, 15) with substitution at position 1; '
               'substituent chain length = 10, free -OH groups = 2.\n'
               ' * SMILES: C(CCCCCCCCCCCC(OCC(CO)O)=O)CCCCCCC NAME: '
               '1-icosanoylglycerol REASON: CORRECT Found glycerol backbone '
               '(atoms 14, 15, 16) with substitution at position 1; '
               'substituent chain length = 20, free -OH groups = 2.\n'
               ' * SMILES: '
               'O(C[C@@H](O)CO)C(=O)CC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CCCCC '
               'NAME: MG(22:5(4Z,7Z,10Z,13Z,16Z)/0:0/0:0) REASON: CORRECT '
               'Found glycerol backbone (atoms 1, 2, 4) with substitution at '
               'position 1; substituent chain length = 22, free -OH groups = '
               '2.\n'
               ' * SMILES: O=C(OC[C@@H](O)CO)CCCCCCCCCCCCCCCC(C)C NAME: '
               'AKD-2B1 REASON: CORRECT Found glycerol backbone (atoms 3, 4, '
               '6) with substitution at position 1; substituent chain length = '
               '19, free -OH groups = 2.\n'
               ' * SMILES: CCCCCCCCCCCCCCCC(=O)OC[C@H](O)CO NAME: '
               '3-palmitoyl-sn-glycerol REASON: CORRECT Found glycerol '
               'backbone (atoms 18, 19, 21) with substitution at position 1; '
               'substituent chain length = 16, free -OH groups = 2.\n'
               ' * SMILES: OCC(COC(CCCCCCCCC/C=C\\CCCCCCCC)=O)O NAME: '
               '1-(11Z-icosenoyl)glycerol REASON: CORRECT Found glycerol '
               'backbone (atoms 1, 2, 3) with substitution at position 3; '
               'substituent chain length = 20, free -OH groups = 2.\n'
               ' * SMILES: O(C(=O)CCCCCCCCCCC(C)C)CC(O)CO NAME: '
               '2,3-dihydroxypropyl 12-methyltridecanoate REASON: CORRECT '
               'Found glycerol backbone (atoms 16, 17, 19) with substitution '
               'at position 1; substituent chain length = 14, free -OH groups '
               '= 2.\n'
               ' * SMILES: CCCCC\\C=C/C\\C=C/CCCCCCCC(=O)OC(CO)CO NAME: '
               '2-linoleoylglycerol REASON: CORRECT Found glycerol backbone '
               '(atoms 21, 20, 23) with substitution at position 2; '
               'substituent chain length = 18, free -OH groups = 2.\n'
               ' * SMILES: CC(C)CCCCC=CCCCCCCCC(=O)OCC(CO)O NAME: '
               '15-methyl-9-hexadecenoic acid 2,3-dihydroxypropyl ester '
               'REASON: CORRECT Found glycerol backbone (atoms 19, 20, 21) '
               'with substitution at position 1; substituent chain length = '
               '17, free -OH groups = 2.\n'
               ' * SMILES: CCCCCCCCCCCCCCCCCCOC[C@@H](O)CO NAME: '
               '1-O-octadecyl-sn-glycerol REASON: CORRECT Found glycerol '
               'backbone (atoms 19, 20, 22) with substitution at position 1; '
               'substituent chain length = 18, free -OH groups = 2.\n'
               ' * SMILES: CCCC(=O)OCC(O)CO NAME: monobutyrin REASON: CORRECT '
               'Found glycerol backbone (atoms 6, 7, 9) with substitution at '
               'position 1; substituent chain length = 4, free -OH groups = '
               '2.\n'
               ' * SMILES: CC\\C=C/C\\C=C/C\\C=C/CCCCCCCC(=O)OC[C@H](O)CO '
               'NAME: 3-alpha-linolenoyl-sn-glycerol REASON: CORRECT Found '
               'glycerol backbone (atoms 20, 21, 23) with substitution at '
               'position 1; substituent chain length = 18, free -OH groups = '
               '2.\n'
               ' * SMILES: O=C(OCC(O)CO)CCCCCCCCCCCCCCC(CC)C NAME: AKD-2B2 '
               'REASON: CORRECT Found glycerol backbone (atoms 3, 4, 6) with '
               'substitution at position 1; substituent chain length = 19, '
               'free -OH groups = 2.\n'
               'False positives: SMILES: O(CCCCCC)C(CO)CO NAME: '
               '2-Hexylglycerol REASON: WRONGLY CLASSIFIED Found glycerol '
               'backbone (atoms 8, 7, 10) with substitution at position 2; '
               'substituent chain length = 6, free -OH groups = 2.\n'
               ' * SMILES: O(C(=O)CCCCCCCCC/C=C\\CCCCCCCC)C(CO)CO NAME: '
               'MG(0:0/20:1(11Z)/0:0) REASON: WRONGLY CLASSIFIED Found '
               'glycerol backbone (atoms 23, 22, 25) with substitution at '
               'position 2; substituent chain length = 20, free -OH groups = '
               '2.\n'
               ' * SMILES: O(C(CO)CO)C(=O)CCC/C=C\\C/C=C\\C/C=C\\CCCCCCCC '
               'NAME: MG(0:0/20:3(5Z,8Z,11Z)/0:0) REASON: WRONGLY CLASSIFIED '
               'Found glycerol backbone (atoms 2, 1, 4) with substitution at '
               'position 2; substituent chain length = 20, free -OH groups = '
               '2.\n'
               ' * SMILES: '
               'O(C(=O)CCCCCC/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)C[C@@H](O)CO NAME: '
               'MG(20:4(8Z,11Z,14Z,17Z)/0:0/0:0) REASON: WRONGLY CLASSIFIED '
               'Found glycerol backbone (atoms 22, 23, 25) with substitution '
               'at position 1; substituent chain length = 20, free -OH groups '
               '= 2.\n'
               ' * SMILES: '
               'O(C[C@@H](O)CO)\\C=C\\C=C\\C=C\\C=C\\C=C\\CCCCCCCCCCC NAME: '
               '1-O-(1E,3E,5E,7E,9E-heneicosapentenyl)-sn-glycerol REASON: '
               'WRONGLY CLASSIFIED Found glycerol backbone (atoms 1, 2, 4) '
               'with substitution at position 1; substituent chain length = '
               '21, free -OH groups = 2.\n'
               ' * SMILES: O(C(=O)CCCCCCCCC/C=C\\C/C=C\\CCCCC)C[C@@H](O)CO '
               'NAME: MG(20:2(11Z,14Z)/0:0/0:0) REASON: WRONGLY CLASSIFIED '
               'Found glycerol backbone (atoms 22, 23, 25) with substitution '
               'at position 1; substituent chain length = 20, free -OH groups '
               '= 2.\n'
               ' * SMILES: CCCCCCCCCCCCCCCCOCC(O)CO NAME: 1-O-palmitylglycerol '
               'REASON: WRONGLY CLASSIFIED Found glycerol backbone (atoms 17, '
               '18, 20) with substitution at position 1; substituent chain '
               'length = 16, free -OH groups = 2.\n'
               ' * SMILES: '
               'O(C(C(O)([2H])[2H])(C(O)([2H])[2H])[2H])C(=O)CCC/C=C\\C/C=C\\C/C=C\\C/C=C\\CCCCC '
               'NAME: 2-arachidonoyl glycerol-d5 REASON: WRONGLY CLASSIFIED '
               'Found glycerol backbone (atoms 2, 1, 6) with substitution at '
               'position 2; substituent chain length = 20, free -OH groups = '
               '2.\n'
               ' * SMILES: CCCCCCCCCCCCCCCCCCOCC(O)CO NAME: batilol REASON: '
               'WRONGLY CLASSIFIED Found glycerol backbone (atoms 19, 20, 22) '
               'with substitution at position 1; substituent chain length = '
               '18, free -OH groups = 2.\n'
               ' * SMILES: CCCCCC=CCC=CCC=CCC=CCCCC(=O)OC(CO)CO NAME: '
               'eicosa-5,8,11,14-tetraenoic acid 1,3-dihydroxypropan-2-yl '
               'ester REASON: WRONGLY CLASSIFIED Found glycerol backbone '
               '(atoms 23, 22, 25) with substitution at position 2; '
               'substituent chain length = 20, free -OH groups = 2.\n'
               ' * SMILES: O(C(=O)CCCCCCCCC/C=C\\C/C=C\\C/C=C\\CC)C(CO)CO '
               'NAME: MG(0:0/20:3(11Z,14Z,17Z)/0:0) REASON: WRONGLY CLASSIFIED '
               'Found glycerol backbone (atoms 23, 22, 25) with substitution '
               'at position 2; substituent chain length = 20, free -OH groups '
               '= 2.\n'
               ' * SMILES: O(CCCCCCCCCCCCCC)CC(O)CO NAME: '
               '1-O-Tetradecylglycerol REASON: WRONGLY CLASSIFIED Found '
               'glycerol backbone (atoms 15, 16, 18) with substitution at '
               'position 1; substituent chain length = 14, free -OH groups = '
               '2.\n'
               ' * SMILES: O(CCCCCC)C[C@@H](O)CO NAME: 1-Hexylglycerol REASON: '
               'WRONGLY CLASSIFIED Found glycerol backbone (atoms 7, 8, 10) '
               'with substitution at position 1; substituent chain length = 6, '
               'free -OH groups = 2.\n'
               ' * SMILES: C(CCCCCCCC)CCCOCC(O)CO NAME: 1-O-dodecylglycerol '
               'REASON: WRONGLY CLASSIFIED Found glycerol backbone (atoms 13, '
               '14, 16) with substitution at position 1; substituent chain '
               'length = 12, free -OH groups = 2.\n'
               ' * SMILES: '
               'O(C[C@@H](O)CO)\\C=C\\C=C\\C=C\\C=C\\C=C\\CCCCCCCCCC NAME: '
               '1-O-(1E,3E,5E,7E,9E-eicosapentenyl)-sn-glycerol REASON: '
               'WRONGLY CLASSIFIED Found glycerol backbone (atoms 1, 2, 4) '
               'with substitution at position 1; substituent chain length = '
               '20, free -OH groups = 2.\n'
               ' * SMILES: O(/C=C\\CCCCCCCCCCCCCCCC)C[C@@H](O)CO NAME: '
               'MG(P-18:0e/0:0/0:0) REASON: WRONGLY CLASSIFIED Found glycerol '
               'backbone (atoms 19, 20, 22) with substitution at position 1; '
               'substituent chain length = 18, free -OH groups = 2.\n'
               ' * SMILES: O(C(=O)CCCCCCCCC/C=C\\C/C=C\\CCCCC)C(CO)CO NAME: '
               'MG(0:0/20:2(11Z,14Z)/0:0) REASON: WRONGLY CLASSIFIED Found '
               'glycerol backbone (atoms 23, 22, 25) with substitution at '
               'position 2; substituent chain length = 20, free -OH groups = '
               '2.\n'
               ' * SMILES: CCCCCCCC\\C=C/CCCCCCCCOCC(O)CO NAME: '
               '(9Z)-1-O-octadec-9-enyl glycerol REASON: WRONGLY CLASSIFIED '
               'Found glycerol backbone (atoms 19, 20, 22) with substitution '
               'at position 1; substituent chain length = 18, free -OH groups '
               '= 2.\n'
               ' * SMILES: '
               'O(C(=O)CCCC/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)C[C@@H](O)CO NAME: '
               'MG(18:4(6Z,9Z,12Z,15Z)/0:0/0:0) REASON: WRONGLY CLASSIFIED '
               'Found glycerol backbone (atoms 20, 21, 23) with substitution '
               'at position 1; substituent chain length = 18, free -OH groups '
               '= 2.\n'
               ' * SMILES: O(C(=O)CCCCCC/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)C(CO)CO '
               'NAME: MG(0:0/20:4(8Z,11Z,14Z,17Z)/0:0) REASON: WRONGLY '
               'CLASSIFIED Found glycerol backbone (atoms 23, 22, 25) with '
               'substitution at position 2; substituent chain length = 20, '
               'free -OH groups = 2.\n'
               ' * SMILES: O(CCC\\C=C\\C(=O)CCCCCCCCCC)C[C@@H](O)CO NAME: '
               'Ceratodictyol A REASON: WRONGLY CLASSIFIED Found glycerol '
               'backbone (atoms 18, 19, 21) with substitution at position 1; '
               'substituent chain length = 16, free -OH groups = 2.\n'
               ' * SMILES: O=C(OC[C@@H](O)CO)CCCCCCC/C=C/C=C/C(=O)CCCCC NAME: '
               '2,3-dihydroxypropyl (9E,11E)-13-oxooctadeca-9,11-dienoate '
               'REASON: WRONGLY CLASSIFIED Found glycerol backbone (atoms 3, '
               '4, 6) with substitution at position 1; substituent chain '
               'length = 18, free -OH groups = 2.\n'
               ' * SMILES: CCCCC\\C=C/C\\C=C/C\\C=C/C\\C=C/CCCCOC(CO)CO NAME: '
               '2-arachidonyl glyceryl ether REASON: WRONGLY CLASSIFIED Found '
               'glycerol backbone (atoms 22, 21, 24) with substitution at '
               'position 2; substituent chain length = 20, free -OH groups = '
               '2.\n'
               ' * SMILES: O(C(=O)CCCCCC/C=C\\C/C=C\\C/C=C\\CCCCC)C[C@@H](O)CO '
               'NAME: MG(20:3(8Z,11Z,14Z)/0:0/0:0) REASON: WRONGLY CLASSIFIED '
               'Found glycerol backbone (atoms 22, 23, 25) with substitution '
               'at position 1; substituent chain length = 20, free -OH groups '
               '= 2.\n'
               'False negatives: SMILES: '
               'O=C(CCC/C=C\\C\\C=C/C=C/C(C/C=C\\CCCCC)OO)OC(CO)CO NAME: '
               '12-HPETE 2-glyceryl ester REASON: MISSED No glycerol backbone '
               'with one substituted oxygen (and two free –OH groups) forming '
               'an isolated candidate fragment was found.\n'
               ' * SMILES: '
               'O=C(CCC/C=C\\C/C=C\\C\\C=C/C=C/[C@H](CCCCC)OO)OC(CO)CO NAME: '
               '15(S)-HPETE 2-glyceryl ester REASON: MISSED No glycerol '
               'backbone with one substituted oxygen (and two free –OH groups) '
               'forming an isolated candidate fragment was found.\n'
               ' * SMILES: '
               '[H][C@@]12CC[C@]3(CC1=C)C=CC(=O)[C@@](C)(CCC(=O)OCC(O)CO)[C@]3([H])C2 '
               'NAME: Platencinic acid glycerol ester REASON: MISSED No '
               'glycerol backbone with one substituted oxygen (and two free '
               '–OH groups) forming an isolated candidate fragment was found.\n'
               ' * SMILES: '
               'OCC(CO)OC(CCC/C=C/1\\O[C@]2(C[C@H]([C@@H]([C@]2(C1)[H])/C=C/[C@H](CCCCC)O)O)[H])=O '
               'NAME: prostaglandin I2 2-glyceryl ester REASON: MISSED No '
               'glycerol backbone with one substituted oxygen (and two free '
               '–OH groups) forming an isolated candidate fragment was found.\n'
               ' * SMILES: C(CCC)CC1C(C/C=C\\C/C=C\\C/C=C\\CCCC(OC(CO)CO)=O)O1 '
               'NAME: 2-glyceryl 14,15-epoxy-(5Z,8Z,11Z)-icosatrienoate '
               'REASON: MISSED No glycerol backbone with one substituted '
               'oxygen (and two free –OH groups) forming an isolated candidate '
               'fragment was found.\n'
               ' * SMILES: O=C(OC[C@@H](O)CO)CC1=CC=CC=C1 NAME: '
               '1-O-(phenylacetyl)glycerol REASON: MISSED No glycerol backbone '
               'with one substituted oxygen (and two free –OH groups) forming '
               'an isolated candidate fragment was found.\n'
               ' * SMILES: '
               'C(\\[C@H]1[C@@H](CC([C@@H]1C/C=C\\CCCC(OC(CO)CO)=O)=O)O)=C/[C@H](CCCCC)O '
               'NAME: prostaglandin E2 2-glyceryl ester REASON: MISSED No '
               'glycerol backbone with one substituted oxygen (and two free '
               '–OH groups) forming an isolated candidate fragment was found.\n'
               ' * SMILES: '
               'CCCCC\\C=C\\C=C1/[C@@H](C\\C=C/CCCC(=O)OC(CO)CO)C=CC1=O NAME: '
               '15-deoxy-Delta(12,14)-prostaglandin J2-2-glyceryl ester '
               'REASON: MISSED No glycerol backbone with one substituted '
               'oxygen (and two free –OH groups) forming an isolated candidate '
               'fragment was found.\n'
               ' * SMILES: '
               'CCCCC[C@H](OO)\\C=C\\[C@H]1[C@H]2C[C@H](OO2)[C@@H]1C\\C=C/CCCC(=O)OC(CO)CO '
               'NAME: prostaglandin G2 2-glyceryl ester REASON: MISSED No '
               'glycerol backbone with one substituted oxygen (and two free '
               '–OH groups) forming an isolated candidate fragment was found.\n'
               ' * SMILES: O=C(OCC(O)CO)/C=C/C1=CC(OC)=C(O)C=C1 NAME: '
               '1-feruloyl-sn-glycerol REASON: MISSED No glycerol backbone '
               'with one substituted oxygen (and two free –OH groups) forming '
               'an isolated candidate fragment was found.\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'O1C2=C(O)C=C(COC)C=C2C[C@@H](C1(C)C)O',
                                     'name': 'Conoideochromane B',
                                     'reason': 'No glycerol backbone with one '
                                               'substituted oxygen (and two '
                                               'free –OH groups) forming an '
                                               'isolated candidate fragment '
                                               'was found.'},
                                 {   'smiles': 'P(OC[C@H](OC(=O)CCCCCCC/C=C\\CCCCC)CO/C=C\\CCCCCCCCCCCCCC)(OCCN)(O)=O',
                                     'name': 'PE(P-16:0/15:1(9Z))',
                                     'reason': 'No glycerol backbone with one '
                                               'substituted oxygen (and two '
                                               'free –OH groups) forming an '
                                               'isolated candidate fragment '
                                               'was found.'},
                                 {   'smiles': 'O=C1C=2C(OC(=C1)C)=C(C3=C4O[C@](O)(CC(C4=C(O)C=5C3=CC(OC)=CC5OC)=O)C)C6=CC(OC)=CC(=C6C2O)OC',
                                     'name': '2-hydroxydihydronigerone',
                                     'reason': 'No glycerol backbone with one '
                                               'substituted oxygen (and two '
                                               'free –OH groups) forming an '
                                               'isolated candidate fragment '
                                               'was found.'},
                                 {   'smiles': 'O([C@@H]1[C@@H](NC(=O)C)[C@@H](O[C@@H]([C@H]1O)CO)OC[C@H]2O[C@@H](O)[C@H](NC(=O)C)[C@@H](O)[C@H]2O)[C@@H]3O[C@@H]([C@H](O)[C@H](O[C@H]4O[C@@H]([C@H](O)[C@H](O)[C@H]4O)CO)[C@H]3O)CO',
                                     'name': 'N-[(2R,3R,4R,5R,6R)-6-[[(2R,3R,4R,5S,6R)-3-Acetamido-4-[(2R,3R,4S,5S,6R)-3,5-dihydroxy-6-(hydroxymethyl)-4-[(2R,3R,4S,5R,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-5-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxymethyl]-2,4,5-trihydroxyoxan-3-yl]acetamide',
                                     'reason': 'No glycerol backbone with one '
                                               'substituted oxygen (and two '
                                               'free –OH groups) forming an '
                                               'isolated candidate fragment '
                                               'was found.'},
                                 {   'smiles': 'O1C(C(O)C(O)C(O)C1OC=2C(O)=C(O)C=C(C2)C=O)COC(=O)C3=CC(O)=C(O)C(O)=C3',
                                     'name': 'Castamollissin',
                                     'reason': 'No glycerol backbone with one '
                                               'substituted oxygen (and two '
                                               'free –OH groups) forming an '
                                               'isolated candidate fragment '
                                               'was found.'},
                                 {   'smiles': 'S(OC[C@H]1O[C@@H](OC[C@H]2O[C@@H](O[C@@H]([C@@H](O)[C@H](O)CO[C@]3(O[C@H]([C@H](NC(=O)C)[C@@H](O)C3)[C@H](O)[C@H](O)CO)C(O)=O)[C@@H](NC(=O)C)CO)[C@H](O)[C@@H](O)[C@H]2O)[C@H](NC(=O)C)[C@@H](O)[C@@H]1O[C@@H]4O[C@@H]([C@H](O)[C@H](O)[C@H]4O)CO[C@]5(O[C@H]([C@H](NC(=O)C)[C@@H](O)C5)[C@H](O)[C@H](O)CO)C(O)=O)(O)(=O)=O',
                                     'name': '(2R,4S,5R,6R)-5-Acetamido-2-[[(2R,3R,4S,5R,6S)-6-[(2R,3S,4R,5R,6R)-5-acetamido-6-[[(2R,3R,4S,5R,6R)-6-[(2S,3R,4S,5R)-2-acetamido-6-[(2R,4S,5R,6R)-5-acetamido-2-carboxy-4-hydroxy-6-[(1R,2R)-1,2,3-trihydroxypropyl]oxan-2-yl]oxy-1,4,5-trihydroxyhexan-3-yl]oxy-3,4,5-trihydroxyoxan-2-yl]methoxy]-4-hydroxy-2-(sulfooxymethyl)oxan-3-yl]oxy-3,4,5-trihydroxyoxan-2-yl]methoxy]-4-hydroxy-6-[(1R,2R)-1,2,3-trihydroxypropyl]oxane-2-carboxylic '
                                             'acid',
                                     'reason': 'No glycerol backbone with one '
                                               'substituted oxygen (and two '
                                               'free –OH groups) forming an '
                                               'isolated candidate fragment '
                                               'was found.'},
                                 {   'smiles': 'FC(F)(F)C(F)(F)C(F)(F)C(F)(F)C(F)(F)C(F)(F)F',
                                     'name': 'perfluorohexane',
                                     'reason': 'No glycerol backbone with one '
                                               'substituted oxygen (and two '
                                               'free –OH groups) forming an '
                                               'isolated candidate fragment '
                                               'was found.'},
                                 {   'smiles': 'CC(C)(O)CCC(=O)[C@](C)(O)[C@H]1[C@H](O)C[C@@]2(C)[C@@H]3CC=C4[C@@H](C[C@@H](O)[C@@H](O)C4(C)C)[C@]3(C)C(=O)C[C@]12C',
                                     'name': 'Cucurbitacin P',
                                     'reason': 'No glycerol backbone with one '
                                               'substituted oxygen (and two '
                                               'free –OH groups) forming an '
                                               'isolated candidate fragment '
                                               'was found.'},
                                 {   'smiles': 'CCCCCCCc1cc(O)cc(=O)o1',
                                     'name': '4-hydroxy-6-heptylpyran-2-one',
                                     'reason': 'No glycerol backbone with one '
                                               'substituted oxygen (and two '
                                               'free –OH groups) forming an '
                                               'isolated candidate fragment '
                                               'was found.'},
                                 {   'smiles': 'S(O[C@@H]1[C@@H](O)[C@H](O[C@H]2[C@H](O)[C@@H](NC(=O)C)[C@H](O[C@H]3[C@@H](O)[C@H](O[C@@H]4O[C@@H]([C@@H](O[C@@H]5O[C@@H]([C@H](O)[C@H](OS(O)(=O)=O)[C@H]5O)CO)[C@H](O)[C@H]4NC(=O)C)CO)[C@H](O[C@@H]3O[C@H]6[C@H](O)[C@H](O[C@@H](O[C@H]7[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]7CO)O[C@H]8[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]8CO[C@@H]9O[C@H]([C@@H](O)[C@@H](O)[C@@H]9O)C)O)[C@H]6O)CO[C@H]%10O[C@@H]([C@@H](O)[C@H](O)[C@@H]%10O[C@@H]%11O[C@@H]([C@@H](O[C@@H]%12O[C@@H]([C@H](O[C@@H]%13O[C@@H]([C@H](O)[C@H](O)[C@H]%13NC(=O)C)CO)[C@H](O[C@]%14(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%14)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%12O)CO)[C@H](O)[C@H]%11NC(=O)C)CO)CO[C@@H]%15O[C@@H]([C@@H](O[C@@H]%16O[C@@H]([C@H](O)[C@H](O[C@]%17(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%17)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%16O)CO)[C@H](O)[C@H]%15NC(=O)C)CO)CO)O[C@@H]2CO)O[C@@H]([C@@H]1O)CO)(O)(=O)=O',
                                     'name': 'CID 146017241',
                                     'reason': 'No glycerol backbone with one '
                                               'substituted oxygen (and two '
                                               'free –OH groups) forming an '
                                               'isolated candidate fragment '
                                               'was found.'}],
    'sample_false_negatives': [   {   'smiles': 'O=C(CCC/C=C\\C\\C=C/C=C/C(C/C=C\\CCCCC)OO)OC(CO)CO',
                                      'name': '12-HPETE 2-glyceryl ester',
                                      'reason': 'No glycerol backbone with one '
                                                'substituted oxygen (and two '
                                                'free –OH groups) forming an '
                                                'isolated candidate fragment '
                                                'was found.'},
                                  {   'smiles': 'O=C(CCC/C=C\\C/C=C\\C\\C=C/C=C/[C@H](CCCCC)OO)OC(CO)CO',
                                      'name': '15(S)-HPETE 2-glyceryl ester',
                                      'reason': 'No glycerol backbone with one '
                                                'substituted oxygen (and two '
                                                'free –OH groups) forming an '
                                                'isolated candidate fragment '
                                                'was found.'},
                                  {   'smiles': '[H][C@@]12CC[C@]3(CC1=C)C=CC(=O)[C@@](C)(CCC(=O)OCC(O)CO)[C@]3([H])C2',
                                      'name': 'Platencinic acid glycerol ester',
                                      'reason': 'No glycerol backbone with one '
                                                'substituted oxygen (and two '
                                                'free –OH groups) forming an '
                                                'isolated candidate fragment '
                                                'was found.'},
                                  {   'smiles': 'OCC(CO)OC(CCC/C=C/1\\O[C@]2(C[C@H]([C@@H]([C@]2(C1)[H])/C=C/[C@H](CCCCC)O)O)[H])=O',
                                      'name': 'prostaglandin I2 2-glyceryl '
                                              'ester',
                                      'reason': 'No glycerol backbone with one '
                                                'substituted oxygen (and two '
                                                'free –OH groups) forming an '
                                                'isolated candidate fragment '
                                                'was found.'},
                                  {   'smiles': 'C(CCC)CC1C(C/C=C\\C/C=C\\C/C=C\\CCCC(OC(CO)CO)=O)O1',
                                      'name': '2-glyceryl '
                                              '14,15-epoxy-(5Z,8Z,11Z)-icosatrienoate',
                                      'reason': 'No glycerol backbone with one '
                                                'substituted oxygen (and two '
                                                'free –OH groups) forming an '
                                                'isolated candidate fragment '
                                                'was found.'},
                                  {   'smiles': 'O=C(OC[C@@H](O)CO)CC1=CC=CC=C1',
                                      'name': '1-O-(phenylacetyl)glycerol',
                                      'reason': 'No glycerol backbone with one '
                                                'substituted oxygen (and two '
                                                'free –OH groups) forming an '
                                                'isolated candidate fragment '
                                                'was found.'},
                                  {   'smiles': 'C(\\[C@H]1[C@@H](CC([C@@H]1C/C=C\\CCCC(OC(CO)CO)=O)=O)O)=C/[C@H](CCCCC)O',
                                      'name': 'prostaglandin E2 2-glyceryl '
                                              'ester',
                                      'reason': 'No glycerol backbone with one '
                                                'substituted oxygen (and two '
                                                'free –OH groups) forming an '
                                                'isolated candidate fragment '
                                                'was found.'},
                                  {   'smiles': 'CCCCC\\C=C\\C=C1/[C@@H](C\\C=C/CCCC(=O)OC(CO)CO)C=CC1=O',
                                      'name': '15-deoxy-Delta(12,14)-prostaglandin '
                                              'J2-2-glyceryl ester',
                                      'reason': 'No glycerol backbone with one '
                                                'substituted oxygen (and two '
                                                'free –OH groups) forming an '
                                                'isolated candidate fragment '
                                                'was found.'},
                                  {   'smiles': 'CCCCC[C@H](OO)\\C=C\\[C@H]1[C@H]2C[C@H](OO2)[C@@H]1C\\C=C/CCCC(=O)OC(CO)CO',
                                      'name': 'prostaglandin G2 2-glyceryl '
                                              'ester',
                                      'reason': 'No glycerol backbone with one '
                                                'substituted oxygen (and two '
                                                'free –OH groups) forming an '
                                                'isolated candidate fragment '
                                                'was found.'},
                                  {   'smiles': 'O=C(OCC(O)CO)/C=C/C1=CC(OC)=C(O)C=C1',
                                      'name': '1-feruloyl-sn-glycerol',
                                      'reason': 'No glycerol backbone with one '
                                                'substituted oxygen (and two '
                                                'free –OH groups) forming an '
                                                'isolated candidate fragment '
                                                'was found.'}],
    'attempt': 4,
    'reasoning': 'Below is one possible solution. In our reasoning we noted '
                 'that the original approach correctly found many true '
                 'positives but sometimes “over‐matched” (or “under‐matched”) '
                 'molecules that should not be classified as a '
                 'monoradylglycerol. One hypothesis was that besides finding a '
                 'contiguous glycerol backbone (three sp³ carbons connected in '
                 'a line, each having one oxygen neighbor) and checking that '
                 'exactly one of those oxygens “lacks” an H (and so is '
                 'substituted), we must also further “characterize” the '
                 'substituent. In our improved version we (1) check that the '
                 'substituent oxygen is attached to exactly one non‐backbone '
                 'neighbor (the “anchor”), (2) decide if the linkage is ester '
                 '(acyl) or ether (alkyl or alk‑1‑enyl) by checking if the '
                 'anchor bears a double‐bonded O (a carbonyl) and then (3) '
                 'require different minimal chain‐lengths (for acyl we allow '
                 'shorter chains such as acetate, whereas for an ether we '
                 'require a “lipid‐sized” alkyl chain). Finally we “assemble” '
                 'the candidate fragment and require that the candidate '
                 'accounts for all heavy atoms. (Of course, this is only one '
                 'of several possible heuristic approaches.) \n'
                 '\n'
                 'Below is the complete program in one code block.\n'
                 '\n'
                 '------------------------------------------------',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 84,
    'num_false_positives': 20,
    'num_true_negatives': 142178,
    'num_false_negatives': 18,
    'num_negatives': None,
    'precision': 0.8076923076923077,
    'recall': 0.8235294117647058,
    'f1': 0.8155339805825242,
    'accuracy': 0.9997329585382994,
    'negative_predictive_value': 0.9998734141607359}