"""
Classifies: CHEBI:16749 1-phosphatidyl-1D-myo-inositol
"""
"""
Classifies: 1-phosphatidyl-1D-myo-inositol
Definition:
    A phosphatidylinositol in which the inositol moiety is the 1D-myo isomer 
    and the phosphatidyl group is located at its position 1.
    
Heuristics in this implementation:
1. Look for at least two ester bonds (simplified as the C(=O)O substructure).
2. Identify a candidate inositol moiety by finding a six-membered ring composed entirely of carbons
   in which the substituents are mostly –OH groups. In genuine 1-phosphatidyl-1D-myo-inositol,
   one of the ring carbons (position 1) carries a phosphatidyl substituent (an oxygen connected to phosphorus)
   and the other 5 carbons have free hydroxyl groups.
   
Note: This is a heuristic approach (using substructure and ring substitution counts) and does not truly
validate stereochemistry. Real stereochemical validation of an inositol isomer is very complex.
"""

from rdkit import Chem

def is_1_phosphatidyl_1D_myo_inositol(smiles: str):
    """
    Determines if a molecule is a 1-phosphatidyl-1D-myo-inositol based on its SMILES string.
    
    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a 1-phosphatidyl-1D-myo-inositol, False otherwise.
        str: Explanation for the classification result.
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
        
    # --- Criterion 1: Check for diacylglycerol ester bonds ---
    # We expect at least 2 ester bonds (C(=O)O) as part of the phosphatidyl (diacylglycerol) group.
    ester_smarts = "C(=O)O"
    ester_pattern = Chem.MolFromSmarts(ester_smarts)
    ester_matches = mol.GetSubstructMatches(ester_pattern)
    if len(ester_matches) < 2:
        return False, f"Found only {len(ester_matches)} ester bond(s); at least 2 are required for the phosphatidyl moiety"
        
    # --- Criterion 2: Inspect six-membered rings for an inositol headgroup ---
    # In 1-phosphatidyl-1D-myo-inositol the inositol ring should be a cyclohexane with 6 carbons,
    # where 5 of these carbons are substituted with free hydroxyl groups (-OH, i.e. oxygen with at least one hydrogen),
    # and 1 carbon (the 1-position) is substituted with an oxygen that connects to a phosphorus atom.
    ring_info = mol.GetRingInfo().AtomRings()
    candidate_found = False
    
    # Loop over all rings in the molecule.
    for ring in ring_info:
        if len(ring) != 6:
            continue  # Only interested in six-membered rings
        # Ensure all atoms in the ring are carbons.
        if not all(mol.GetAtomWithIdx(idx).GetAtomicNum() == 6 for idx in ring):
            continue
            
        free_oh_count = 0
        phospho_sub_count = 0
        # For each carbon atom in the ring, inspect its neighbors not in the ring.
        for idx in ring:
            atom = mol.GetAtomWithIdx(idx)
            # Get indices of atoms in the ring (for quick checking).
            ring_atom_set = set(ring)
            # Flag to note if this carbon has a substituent that is a phosphate connection.
            has_phospho = False
            # Also count free -OH if present.
            has_free_oh = False
            for nbr in atom.GetNeighbors():
                if nbr.GetIdx() in ring_atom_set:
                    continue
                if nbr.GetAtomicNum() == 8:
                    # Check if this oxygen is attached to a phosphorus (phospho substituent)
                    attached_to_P = any(nbr2.GetAtomicNum() == 15 for nbr2 in nbr.GetNeighbors() if nbr2.GetIdx() != atom.GetIdx())
                    # Check if oxygen has (at least one) hydrogen attached.
                    # Note: GetTotalNumHs() returns the total number of (implicit+explicit) hydrogens.
                    has_h = nbr.GetTotalNumHs() > 0
                    if attached_to_P:
                        has_phospho = True
                    elif has_h:
                        has_free_oh = True
            if has_phospho:
                phospho_sub_count += 1
            elif has_free_oh:
                free_oh_count += 1
        # For genuine 1-phosphatidyl-1D-myo-inositol we expect exactly 1 phospho substitution and 5 free -OH.
        if phospho_sub_count == 1 and free_oh_count == 5:
            candidate_found = True
            break  # Found a candidate inositol ring
            
    if not candidate_found:
        return False, "No six-membered inositol ring with 1 phosphate substituent and 5 free hydroxyls found"
        
    # If both criteria are met the molecule is considered to belong to the class.
    return True, "Molecule contains a candidate 1D-myo-inositol headgroup (with 1 phospho and 5 free OH groups) and at least 2 ester bonds consistent with a phosphatidyl moiety"


# Example usage (this part can be removed or commented out when used as a module):
if __name__ == "__main__":
    # A test SMILES string from one of the correct cases
    test_smiles = "CCCCCCCC\\C=C/CCCCCCCC(=O)OC[C@H](COP(O)(=O)O[C@H]1[C@H](O)[C@@H](O)[C@H](O)[C@@H](O)[C@H]1O)OC(=O)CCCCCCC\\C=C/C\\C=C/CCCCC"
    result, reason = is_1_phosphatidyl_1D_myo_inositol(test_smiles)
    print("Classification:", result)
    print("Reason:", reason)


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:16749',
                          'name': '1-phosphatidyl-1D-myo-inositol',
                          'definition': 'A phosphatidylinositol in which the '
                                        'inositol moiety is the 1D-myo isomer '
                                        'and the phosphatidyl group is located '
                                        'at its position 1.',
                          'parents': ['CHEBI:28874'],
                          'xrefs': ['KEGG:C01194', 'PMID:28600633'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 72,
                           'log_lines_of_code': 4.276666119016055,
                           'indent_by_line': [   1,
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
                                                 2,
                                                 2,
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
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
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
                                                 3,
                                                 3,
                                                 3,
                                                 3,
                                                 3,
                                                 3,
                                                 3,
                                                 3,
                                                 4,
                                                 5,
                                                 4,
                                                 5,
                                                 5,
                                                 5,
                                                 5,
                                                 5,
                                                 5,
                                                 6,
                                                 5,
                                                 6,
                                                 3,
                                                 4,
                                                 3,
                                                 4,
                                                 2,
                                                 2,
                                                 3,
                                                 3,
                                                 3,
                                                 1,
                                                 2,
                                                 2,
                                                 1,
                                                 1,
                                                 0,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1],
                           'max_indent': 6,
                           'imports': ['from rdkit import Chem'],
                           'imports_count': 1,
                           'methods_called': [   'GetNeighbors',
                                                 'MolFromSmiles',
                                                 'GetRingInfo',
                                                 'GetSubstructMatches',
                                                 'MolFromSmarts',
                                                 'GetAtomWithIdx',
                                                 'GetIdx',
                                                 'GetAtomicNum',
                                                 'AtomRings',
                                                 'GetTotalNumHs'],
                           'methods_called_count': 10,
                           'smarts_strings': ['ester_smarts'],
                           'smarts_strings_count': 1,
                           'defs': [   'is_1_phosphatidyl_1D_myo_inositol(smiles: '
                                       'str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, f"Found only '
                                          '{len(ester_matches)} ester bond(s); '
                                          'at least 2 are required for the '
                                          'phosphatidyl moiety"',
                                          'False, "No six-membered inositol '
                                          'ring with 1 phosphate substituent '
                                          'and 5 free hydroxyls found"',
                                          'True, "Molecule contains a '
                                          'candidate 1D-myo-inositol headgroup '
                                          '(with 1 phospho and 5 free OH '
                                          'groups) and at least 2 ester bonds '
                                          'consistent with a phosphatidyl '
                                          'moiety"'],
                           'returns_count': 4,
                           'complexity': 5.055333223803212},
    'message': '\n'
               'Attempt failed: F1 score of 0.13012048192771086 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: '
               'C(CCCCCCCC(O[C@@H](COP(O[C@H]1[C@@H]([C@H]([C@@H]([C@H]([C@H]1O)O)O)O)O)(=O)O)COC(=O)CCCCCCCC/C=C\\C/C=C\\C/C=C\\CCCCC)=O)CCCCCCC '
               'NAME: '
               '1-[(10Z,13Z,16Z)-docosatrienoyl]-2-hexadecanoyl-sn-glycero-3-phospho-1D-myo-inositol '
               'REASON: CORRECT Molecule contains a phosphate group linked to '
               'a 6-membered carbon (inositol) ring and at least 2 ester bonds '
               'consistent with a phosphatidyl moiety\n'
               ' * SMILES: '
               'C(C/C=C\\CCCCCCCC)CCCCCCCC(O[C@@H](COP(O[C@H]1[C@@H]([C@H]([C@@H]([C@H]([C@H]1O)O)O)O)O)(=O)O)COC(CCCCCC/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)=O)=O '
               'NAME: '
               '1-[(8Z,11Z,14Z,17Z)-icosatetraenoyl]-2-[(11Z)-icosenoyl]-sn-glycero-3-phospho-1D-myo-inositol '
               'REASON: CORRECT Molecule contains a phosphate group linked to '
               'a 6-membered carbon (inositol) ring and at least 2 ester bonds '
               'consistent with a phosphatidyl moiety\n'
               ' * SMILES: '
               'C(CCCCCCCCC)CCCCCCCC(O[C@@H](COP(O[C@H]1[C@@H]([C@H]([C@@H]([C@H]([C@H]1O)O)O)O)O)(=O)O)COC(CCCCCC/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)=O)=O '
               'NAME: '
               '1-[(8Z,11Z,14Z,17Z)-icosatetraenoyl]-2-octadecanoyl-sn-glycero-3-phospho-1D-myo-inositol '
               'REASON: CORRECT Molecule contains a phosphate group linked to '
               'a 6-membered carbon (inositol) ring and at least 2 ester bonds '
               'consistent with a phosphatidyl moiety\n'
               ' * SMILES: '
               '[C@@H]1([C@@H]([C@@H]([C@@H]([C@H]([C@@H]1O)O)O)O)OP(OC[C@@H](COC(CCCCCCCCCCCCCCC)=O)OC(CCCCCCC/C=C\\C/C=C\\CCC)=O)(=O)O)O '
               'NAME: PI(16:0/16:2(9ZZ,12Z)) REASON: CORRECT Molecule contains '
               'a phosphate group linked to a 6-membered carbon (inositol) '
               'ring and at least 2 ester bonds consistent with a phosphatidyl '
               'moiety\n'
               ' * SMILES: '
               'CCCCCCCC\\C=C/CCCCCCCC(=O)OC[C@H](COP(O)(=O)O[C@H]1[C@H](O)[C@@H](O)[C@H](O)[C@@H](O)[C@H]1O)OC(=O)CCC\\C=C/C\\C=C/C\\C=C/C\\C=C/CCCCC '
               'NAME: '
               '1-oleoyl-2-arachidonoyl-sn-glycero-3-phospho-1D-myo-inositol '
               'REASON: CORRECT Molecule contains a phosphate group linked to '
               'a 6-membered carbon (inositol) ring and at least 2 ester bonds '
               'consistent with a phosphatidyl moiety\n'
               ' * SMILES: '
               'C(\\CCCCCCCC(O[C@@H](COP(O[C@H]1[C@@H]([C@H]([C@@H]([C@H]([C@H]1O)O)O)O)O)(=O)O)COC(=O)CCCCCCCC/C=C\\C/C=C\\C/C=C\\CCCCC)=O)=C\\C/C=C\\CCC '
               'NAME: '
               '1-[(10Z,13Z,16Z)-docosatrienoyl]-2-[(9Z,12Z)-hexadecadienoyl]-sn-glycero-3-phospho-1D-myo-inositol '
               'REASON: CORRECT Molecule contains a phosphate group linked to '
               'a 6-membered carbon (inositol) ring and at least 2 ester bonds '
               'consistent with a phosphatidyl moiety\n'
               ' * SMILES: '
               '[C@@H](OC(CCC/C=C\\C/C=C\\C/C=C\\C/C=C\\CCCCC)=O)(COC(=O)CCCCCCCCCCCCCCC)COP(O[C@H]1[C@@H]([C@H]([C@@H]([C@H]([C@H]1O)O)O)O)O)(=O)O '
               'NAME: '
               '1-hexadecanoyl-2-(5Z,8Z,11Z,14Z-icosatetraenoyl)-sn-glycero-3-phospho-D-myo-inositol '
               'REASON: CORRECT Molecule contains a phosphate group linked to '
               'a 6-membered carbon (inositol) ring and at least 2 ester bonds '
               'consistent with a phosphatidyl moiety\n'
               ' * SMILES: '
               'C(\\CCCCCCCC(O[C@@H](COP(O[C@H]1[C@@H]([C@H]([C@@H]([C@H]([C@H]1O)O)O)O)O)(=O)O)COC(=O)CCCCCCCC/C=C\\C/C=C\\C/C=C\\CCCCC)=O)=C\\C/C=C\\CCCCC '
               'NAME: '
               '1-[(10Z,13Z,16Z)-docosatrienoyl]-2-linoleoyl-sn-glycero-3-phospho-1D-myo-inositol '
               'REASON: CORRECT Molecule contains a phosphate group linked to '
               'a 6-membered carbon (inositol) ring and at least 2 ester bonds '
               'consistent with a phosphatidyl moiety\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCC(=O)OC[C@H](COP(O)(=O)O[C@H]1[C@H](O)[C@@H](O)[C@H](O)[C@@H](O)[C@H]1O)OC(=O)CCCCCCC\\C=C/C\\C=C/CCCCC '
               'NAME: '
               '1-hexadecanoyl-2-(9Z,12Z-octadecadienoyl)-sn-glycero-3-phospho-D-myo-inositol '
               'REASON: CORRECT Molecule contains a phosphate group linked to '
               'a 6-membered carbon (inositol) ring and at least 2 ester bonds '
               'consistent with a phosphatidyl moiety\n'
               ' * SMILES: '
               '[C@@H]1([C@@H]([C@@H]([C@@H]([C@H]([C@@H]1O)O)O)O)OP(OC[C@@H](COC(CCCCCCCCCCCCCCC)=O)OC(CCCCCCC/C=C\\CCCCCCCC)=O)(=O)O)O '
               'NAME: '
               '1-hexadecanoyl-2-(9Z-octadecenoyl)-sn-glycero-3-phospho-D-myo-inositol '
               'REASON: CORRECT Molecule contains a phosphate group linked to '
               'a 6-membered carbon (inositol) ring and at least 2 ester bonds '
               'consistent with a phosphatidyl moiety\n'
               ' * SMILES: '
               '[C@](COC(=O)CCCCCCC/C=C\\CCCCCCC)(COP(O[C@H]1C(C(C([C@H](C1O)O)O)O)O)(O)=O)(OC(=O)CCCCC/C=C\\C/C=C\\C/C=C\\C/C=C\\CCCCC)[H] '
               'NAME: '
               "1-(9Z-heptadecenoyl)-2-(7Z,10Z,13Z,16Z-docosatetraenoyl)-glycero-3-phospho-(1'-myo-inositol) "
               'REASON: CORRECT Molecule contains a phosphate group linked to '
               'a 6-membered carbon (inositol) ring and at least 2 ester bonds '
               'consistent with a phosphatidyl moiety\n'
               ' * SMILES: '
               'CCCCC\\C=C/C\\C=C/CCCCCCCC(=O)OC[C@H](COP(O)(=O)O[C@H]1[C@H](O)[C@@H](O)[C@H](O)[C@@H](O)[C@H]1O)OC(=O)CCCCCCC\\C=C/C\\C=C/CCCCC '
               'NAME: 1,2-dilinoleoyl-sn-glycero-3-phospho-1D-myo-inositol '
               'REASON: CORRECT Molecule contains a phosphate group linked to '
               'a 6-membered carbon (inositol) ring and at least 2 ester bonds '
               'consistent with a phosphatidyl moiety\n'
               ' * SMILES: '
               '[C@](COC(=O)CCCCCCC/C=C\\C/C=C\\CCCC)(COP(O[C@H]1C(C(C([C@H](C1O)O)O)O)O)(O)=O)(OC(=O)CCCCC/C=C\\C/C=C\\C/C=C\\C/C=C\\CCCCC)[H] '
               'NAME: '
               "1-(9Z,12Z-heptadecadienoyl)-2-(7Z,10Z,13Z,16Z-docosatetraenoyl)-glycero-3-phospho-(1'-myo-inositol) "
               'REASON: CORRECT Molecule contains a phosphate group linked to '
               'a 6-membered carbon (inositol) ring and at least 2 ester bonds '
               'consistent with a phosphatidyl moiety\n'
               ' * SMILES: '
               'CCCC(=O)OC[C@H](COP(O)(=O)O[C@H]1[C@H](O)[C@@H](O)[C@H](O)[C@@H](O)[C@H]1O)OC(=O)CCC '
               "NAME: 1,2-dibutyryl-sn-glycero-3-phospho-(1'D-myo-inositol) "
               'REASON: CORRECT Molecule contains a phosphate group linked to '
               'a 6-membered carbon (inositol) ring and at least 2 ester bonds '
               'consistent with a phosphatidyl moiety\n'
               ' * SMILES: '
               '[C@@H]1(C(C(C([C@H](C1O)O)O)O)O)OP(OC[C@@](COC(CCCCCCC/C=C\\CCCCCCCC)=O)(OC(CCCCCCCCCCCCCCC)=O)[H])(O)=O '
               'NAME: PI(18:1(9Z)/16:0) REASON: CORRECT Molecule contains a '
               'phosphate group linked to a 6-membered carbon (inositol) ring '
               'and at least 2 ester bonds consistent with a phosphatidyl '
               'moiety\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCC(=O)OC[C@H](COP(O)(=O)O[C@H]1[C@H](O)[C@@H](O)[C@H](O)[C@@H](O)[C@H]1O)OC(=O)CCC\\C=C/C\\C=C/C\\C=C/C\\C=C/CCCCC '
               'NAME: '
               '1-stearoyl-2-arachidonoyl-sn-glycero-3-phospho-1D-myo-inositol '
               'REASON: CORRECT Molecule contains a phosphate group linked to '
               'a 6-membered carbon (inositol) ring and at least 2 ester bonds '
               'consistent with a phosphatidyl moiety\n'
               ' * SMILES: '
               'C(CCCCCCCCCCC)CCCCCCCC(O[C@@H](COP(O[C@H]1[C@@H]([C@H]([C@@H]([C@H]([C@H]1O)O)O)O)O)(=O)O)COC(CCCCCC/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)=O)=O '
               'NAME: '
               '1-[(8Z,11Z,14Z,17Z)-icosatetraenoyl]-2-icosanoyl-sn-glycero-3-phospho-1D-myo-inositol '
               'REASON: CORRECT Molecule contains a phosphate group linked to '
               'a 6-membered carbon (inositol) ring and at least 2 ester bonds '
               'consistent with a phosphatidyl moiety\n'
               ' * SMILES: '
               'P(OC1C(O)C(O)C(O)[C@@H](O)C1O)(OC[C@H](OC(=O)CCC/C=C\\C/C=C\\C/C=C\\C/C=C\\CCCCC)COC(=O)CCCCCCCCCCCCCCCC)(O)=O '
               'NAME: PI(17:0/20:4) REASON: CORRECT Molecule contains a '
               'phosphate group linked to a 6-membered carbon (inositol) ring '
               'and at least 2 ester bonds consistent with a phosphatidyl '
               'moiety\n'
               ' * SMILES: '
               '[C@](COC(=O)CCCCCCCCCCCC)(COP(O[C@H]1C(C(C([C@H](C1O)O)O)O)O)(O)=O)(OC(=O)CCCCCCCCCCC/C=C\\C/C=C\\CCCCC)[H] '
               'NAME: '
               "1-tridecanoyl-2-(13Z,16Z-docosadienoyl)-glycero-3-phospho-(1'-myo-inositol) "
               'REASON: CORRECT Molecule contains a phosphate group linked to '
               'a 6-membered carbon (inositol) ring and at least 2 ester bonds '
               'consistent with a phosphatidyl moiety\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCC(=O)O[C@H](COC(=O)CCC\\C=C/C\\C=C/C\\C=C/C\\C=C/C\\C=C/CCCC)COP(O)(=O)O[C@H]1[C@H](O)[C@@H](O)[C@H](O)[C@@H](O)[C@H]1O '
               'NAME: '
               '1-(5Z,8Z,11Z,14Z,17Z)-docosapent-5,8,11,14,17-enoyl-2-stearoyl-sn-glycero-3-phospho-1D-myo-inositol '
               'REASON: CORRECT Molecule contains a phosphate group linked to '
               'a 6-membered carbon (inositol) ring and at least 2 ester bonds '
               'consistent with a phosphatidyl moiety\n'
               ' * SMILES: '
               'C(\\CCCCCCCC(O[C@@H](COP(O[C@H]1[C@@H]([C@H]([C@@H]([C@H]([C@H]1O)O)O)O)O)(=O)O)COC(=O)CCCCCCCCCCC/C=C\\C/C=C\\CCCCC)=O)=C\\C/C=C\\CCCCC '
               'NAME: '
               '1-[(13Z,16Z)-docosadienoyl]-2-linoleoyl-sn-glycero-3-phospho-1D-myo-inositol '
               'REASON: CORRECT Molecule contains a phosphate group linked to '
               'a 6-membered carbon (inositol) ring and at least 2 ester bonds '
               'consistent with a phosphatidyl moiety\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCC(=O)OC[C@H](COP(O)(=O)O[C@H]1[C@H](O)[C@@H](O)[C@H](O)[C@@H](O)[C@H]1O)OC(=O)CCCCCCCCCCC '
               'NAME: '
               '1-palmitoyl-2-lauroyl-sn-glycero-3-phospho-1D-myo-inositol '
               'REASON: CORRECT Molecule contains a phosphate group linked to '
               'a 6-membered carbon (inositol) ring and at least 2 ester bonds '
               'consistent with a phosphatidyl moiety\n'
               ' * SMILES: '
               'CCCCCCCC(=O)OC[C@H](COP(O)(=O)O[C@H]1[C@H](O)[C@@H](O)[C@H](O)[C@@H](O)[C@H]1O)OC(=O)CCCCCCC '
               'NAME: 1,2-dioctanoyl-sn-glycero-3-phospho-1D-myo-inositol '
               'REASON: CORRECT Molecule contains a phosphate group linked to '
               'a 6-membered carbon (inositol) ring and at least 2 ester bonds '
               'consistent with a phosphatidyl moiety\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCC(=O)OC[C@H](COP(O)(=O)O[C@H]1[C@H](O)[C@@H](O)[C@H](O)[C@@H](O)[C@H]1O)OC(=O)CCCCCCC\\C=C/CCCCCCCC '
               'NAME: 1-stearoyl-2-oleoyl-sn-glycero-3-phospho-1D-myo-inositol '
               'REASON: CORRECT Molecule contains a phosphate group linked to '
               'a 6-membered carbon (inositol) ring and at least 2 ester bonds '
               'consistent with a phosphatidyl moiety\n'
               ' * SMILES: '
               'C(CCCCCCCC(O[C@@H](COP(O[C@H]1[C@@H]([C@H]([C@@H]([C@H]([C@H]1O)O)O)O)O)(=O)O)COC(=O)CCCCCCCCCCC/C=C\\C/C=C\\CCCCC)=O)CCCCCCC '
               'NAME: '
               '1-[(13Z,16Z)-docosadienoyl]-2-hexadecanoyl-sn-glycero-3-phospho-1D-myo-inositol '
               'REASON: CORRECT Molecule contains a phosphate group linked to '
               'a 6-membered carbon (inositol) ring and at least 2 ester bonds '
               'consistent with a phosphatidyl moiety\n'
               'False positives: SMILES: '
               'P(O[C@H]1C(C(O)C(O)[C@@H](O)C1O)C)(OC[C@H](OC(=O)CCC(O)=O)COC(=O)CCCCCCCCCCCCCCC)(O)=O '
               'NAME: PS-PI REASON: WRONGLY CLASSIFIED Molecule contains a '
               'phosphate group linked to a 6-membered carbon (inositol) ring '
               'and at least 2 ester bonds consistent with a phosphatidyl '
               'moiety\n'
               ' * SMILES: '
               '[C@@H]1(C(C(C([C@H](C1O)O)O)O)O)OP(OC[C@@](COC(CCC/C=C\\C/C=C\\C/C=C\\C/C=C\\CCCCC)=O)(OC(CCCCCCC/C=C\\CCCCCCCC)=O)[H])(O)=O '
               'NAME: PI(20:4(5Z,8Z,11Z,14Z)/18:1(9Z)) REASON: WRONGLY '
               'CLASSIFIED Molecule contains a phosphate group linked to a '
               '6-membered carbon (inositol) ring and at least 2 ester bonds '
               'consistent with a phosphatidyl moiety\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCC(=O)OC[C@H](COP([O-])(=O)O[C@@H]1[C@H](O)[C@H](O)[C@@H](O)[C@H](OP([O-])([O-])=O)[C@H]1O)OC(=O)CCCCCCC\\C=C/CCCCCCCC '
               'NAME: 1-stearoyl-2-oleoyl-sn-glycero-3-phospho-1D-myo-inositol '
               '5-phosphate(3-) REASON: WRONGLY CLASSIFIED Molecule contains a '
               'phosphate group linked to a 6-membered carbon (inositol) ring '
               'and at least 2 ester bonds consistent with a phosphatidyl '
               'moiety\n'
               ' * SMILES: '
               'P(OC1C(O)C(O)C(O)[C@@H](O)C1O)(OC[C@H](OC(=O)CCCCCCCCCCCCCC)COC(=O)CCCCCCCCC/C=C\\CCCCCCCCCC)(O)=O '
               'NAME: PI(22:1(11Z)/15:0) REASON: WRONGLY CLASSIFIED Molecule '
               'contains a phosphate group linked to a 6-membered carbon '
               '(inositol) ring and at least 2 ester bonds consistent with a '
               'phosphatidyl moiety\n'
               ' * SMILES: '
               '[C@@H]1(C(C(C([C@H](C1O)O)O)O)O)OP(OC[C@@](COC(CCCCCCC/C=C\\CCCCCCCC)=O)(OC(CCCCCCC/C=C\\C/C=C\\C/C=C\\CC)=O)[H])(O)=O '
               'NAME: PI(18:1(9Z)/18:3(9Z,12Z,15Z)) REASON: WRONGLY CLASSIFIED '
               'Molecule contains a phosphate group linked to a 6-membered '
               'carbon (inositol) ring and at least 2 ester bonds consistent '
               'with a phosphatidyl moiety\n'
               ' * SMILES: '
               'P(OC1C(O)C(O)C(O)[C@@H](O)C1O)(OC[C@H](OC(=O)CC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)COC(=O)CCCCCCC/C=C\\C/C=C\\CCCC)(O)=O '
               'NAME: PI(17:2(9Z,12Z)/22:6(4Z,7Z,10Z,13Z,16Z,19Z)) REASON: '
               'WRONGLY CLASSIFIED Molecule contains a phosphate group linked '
               'to a 6-membered carbon (inositol) ring and at least 2 ester '
               'bonds consistent with a phosphatidyl moiety\n'
               ' * SMILES: '
               'P(OC1C(O)C(O)C(O)[C@@H](O)C1O)(OC[C@H](OC(=O)CCCCCCC/C=C\\CCCCCC)COC(=O)CCCCCCCCCCCC)(O)=O '
               'NAME: PI(13:0/16:1(9Z)) REASON: WRONGLY CLASSIFIED Molecule '
               'contains a phosphate group linked to a 6-membered carbon '
               '(inositol) ring and at least 2 ester bonds consistent with a '
               'phosphatidyl moiety\n'
               ' * SMILES: '
               'P(O[C@H]1[C@H](O[C@H]2OC([C@@H](O)C(O)[C@H]2O)CO)C(O)[C@H](O)C(O)C1O)(OC[C@H](OC(=O)CCCCCCC/C=C\\CCCCCCCC)COC(=O)CCCCCCCCCCCCCCCC)(O)=O '
               'NAME: PIM1(17:0/18:1(9Z)) REASON: WRONGLY CLASSIFIED Molecule '
               'contains a phosphate group linked to a 6-membered carbon '
               '(inositol) ring and at least 2 ester bonds consistent with a '
               'phosphatidyl moiety\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCC(=O)OC[C@H](COP(O)(=O)O[C@@H]1[C@H](O)[C@H](OP(O)(O)=O)[C@@H](OP(O)(O)=O)[C@H](OP(O)(O)=O)[C@H]1O)OC(=O)CCCCCCCCCCCCCCC '
               'NAME: '
               '1,2-dihexadecanoyl-sn-glycero-3-phospho-(1D-myo-inositol-3,4,5-trisphosphate) '
               'REASON: WRONGLY CLASSIFIED Molecule contains a phosphate group '
               'linked to a 6-membered carbon (inositol) ring and at least 2 '
               'ester bonds consistent with a phosphatidyl moiety\n'
               ' * SMILES: '
               'P(OC1C(O)C(O)C(O)[C@@H](O)C1O)(OC[C@H](OC(=O)CCCCCCC/C=C\\CCCCCCC)COC(=O)CCCCCCC/C=C\\CCCCC)(O)=O '
               'NAME: PI(15:1(9Z)/17:1(9Z)) REASON: WRONGLY CLASSIFIED '
               'Molecule contains a phosphate group linked to a 6-membered '
               'carbon (inositol) ring and at least 2 ester bonds consistent '
               'with a phosphatidyl moiety\n'
               ' * SMILES: '
               'P(OC1C(O)C(O)C(O)[C@@H](O)C1O)(OC[C@H](OC(=O)CCCCCCCCCCCCCCCCCCCC)COC(=O)CCCCCCCCCCCCCCC)(O)=O '
               'NAME: PI(16:0/21:0) REASON: WRONGLY CLASSIFIED Molecule '
               'contains a phosphate group linked to a 6-membered carbon '
               '(inositol) ring and at least 2 ester bonds consistent with a '
               'phosphatidyl moiety\n'
               ' * SMILES: '
               '[C@@H]1(C(C(C([C@H](C1O)O)O)O)O)OP(OC[C@@](COC(CCCCCCCC/C=C\\C/C=C\\C/C=C\\CCCCC)=O)(OC(CCCC/C=C\\C/C=C\\C/C=C\\CCCCC)=O)[H])(O)=O '
               'NAME: PI(22:3(10Z,13Z,16Z)/18:3(6Z,9Z,12Z)) REASON: WRONGLY '
               'CLASSIFIED Molecule contains a phosphate group linked to a '
               '6-membered carbon (inositol) ring and at least 2 ester bonds '
               'consistent with a phosphatidyl moiety\n'
               ' * SMILES: '
               'P(OC1C(O)C(O)C(O)[C@@H](O)C1O)(OC[C@H](OC(=O)CCCCCCCCCCC)COC(=O)CCCCCCCCCCCC)(O)=O '
               'NAME: PI(13:0/12:0) REASON: WRONGLY CLASSIFIED Molecule '
               'contains a phosphate group linked to a 6-membered carbon '
               '(inositol) ring and at least 2 ester bonds consistent with a '
               'phosphatidyl moiety\n'
               ' * SMILES: '
               'P(O[C@H]1[C@H](O[C@H]2OC([C@@H](O)C(O)[C@H]2O)CO)C(O)[C@H](O)C(O)C1O)(OC[C@H](OC(=O)CCCCCCC/C=C\\C/C=C\\CCC)COC(=O)CCCCCCCCCCCCCCC)(O)=O '
               'NAME: PIM1(16:0/16:2(9Z,12Z)) REASON: WRONGLY CLASSIFIED '
               'Molecule contains a phosphate group linked to a 6-membered '
               'carbon (inositol) ring and at least 2 ester bonds consistent '
               'with a phosphatidyl moiety\n'
               ' * SMILES: '
               'CCCCC\\C=C/C\\C=C/CCCCCCCC(=O)OC[C@H](COP([O-])(=O)O[C@H]1[C@H](O)[C@@H](O)[C@H](O)[C@@H](O)[C@H]1O)OC(=O)CCCCCCC\\C=C/C\\C=C/CCCCC '
               'NAME: 1,2-dilinoleoyl-sn-glycero-3-phospho-1D-myo-inositol(1-) '
               'REASON: WRONGLY CLASSIFIED Molecule contains a phosphate group '
               'linked to a 6-membered carbon (inositol) ring and at least 2 '
               'ester bonds consistent with a phosphatidyl moiety\n'
               ' * SMILES: '
               '[C@@H]1(C(C(C([C@H](C1O)O)O)O)O)OP(OC[C@@](COC(CCCCC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)=O)(OC(CCCCCCCCCCCCCCCCC)=O)[H])(O)=O '
               'NAME: PI(22:5(7Z,10Z,13Z,16Z,19Z)/18:0) REASON: WRONGLY '
               'CLASSIFIED Molecule contains a phosphate group linked to a '
               '6-membered carbon (inositol) ring and at least 2 ester bonds '
               'consistent with a phosphatidyl moiety\n'
               ' * SMILES: '
               'P(OC1C(O)C(O)C(O)[C@@H](O)C1O)(OC[C@H](OC(=O)CCCCCCCCCCC/C=C\\C/C=C\\CCCCC)COC(=O)CCCCCCCCCCCCC)(O)=O '
               'NAME: PI(14:0/22:2(13Z,16Z)) REASON: WRONGLY CLASSIFIED '
               'Molecule contains a phosphate group linked to a 6-membered '
               'carbon (inositol) ring and at least 2 ester bonds consistent '
               'with a phosphatidyl moiety\n'
               ' * SMILES: '
               'P(OC1C(O)C(O)C(O)[C@@H](O)C1O)(OC[C@H](OC(=O)CCCCCCCCCCCCCCC)COC(=O)CCCC/C=C\\C/C=C\\C/C=C\\CCCCC)(O)=O '
               'NAME: PI(18:3(6Z,9Z,12Z)/16:0) REASON: WRONGLY CLASSIFIED '
               'Molecule contains a phosphate group linked to a 6-membered '
               'carbon (inositol) ring and at least 2 ester bonds consistent '
               'with a phosphatidyl moiety\n'
               ' * SMILES: '
               '[C@@H]1(C(C(C([C@H](C1O)O)O)O)O)OP(OC[C@@](COC(CCCCCCC/C=C\\C/C=C\\CCCCC)=O)(OC(CCC/C=C\\C/C=C\\C/C=C\\CCCCCCCC)=O)[H])(O)=O '
               'NAME: PI(18:2(9Z,12Z)/20:3(5Z,8Z,11Z)) REASON: WRONGLY '
               'CLASSIFIED Molecule contains a phosphate group linked to a '
               '6-membered carbon (inositol) ring and at least 2 ester bonds '
               'consistent with a phosphatidyl moiety\n'
               ' * SMILES: '
               'CCCCCCCC(=O)OC[C@H](COP(O)(=O)O[C@@H]1[C@H](O)[C@H](O)[C@@H](O)[C@H](OP(O)(O)=O)[C@H]1O)OC(=O)CCCCCCC '
               'NAME: '
               "1,2-dioctanoyl-sn-glycero-3-phospho-(1'-myo-inositol-5'-phosphate) "
               'REASON: WRONGLY CLASSIFIED Molecule contains a phosphate group '
               'linked to a 6-membered carbon (inositol) ring and at least 2 '
               'ester bonds consistent with a phosphatidyl moiety\n'
               ' * SMILES: '
               'P(OC1C(O)C(O)C(O)[C@@H](O)C1O)(OC[C@H](OC(=O)CCCCCCCCC/C=C\\CCCCCCCC)COC(=O)CCCCCCCCCCC/C=C\\C/C=C\\CCCCC)(O)=O '
               'NAME: PI(22:2(13Z,16Z)/20:1(11Z)) REASON: WRONGLY CLASSIFIED '
               'Molecule contains a phosphate group linked to a 6-membered '
               'carbon (inositol) ring and at least 2 ester bonds consistent '
               'with a phosphatidyl moiety\n'
               ' * SMILES: '
               'CCCCCCCC(=O)OC[C@H](COP(O)(=O)O[C@H]1[C@H](O)[C@@H](OP(O)(O)=O)[C@H](O)[C@@H](OP(O)(O)=O)[C@H]1O)OC(=O)CCCCCCC '
               'NAME: '
               '1,2-dioctanoyl-sn-glycero-3-phospho-(1D-myo-inositol-3,5-bisphosphate) '
               'REASON: WRONGLY CLASSIFIED Molecule contains a phosphate group '
               'linked to a 6-membered carbon (inositol) ring and at least 2 '
               'ester bonds consistent with a phosphatidyl moiety\n'
               ' * SMILES: '
               'P(OC1C(O)C(O)C(O)C(O)C1O)(OCC(OC(=O)CCC/C=C\\CC2OC2C/C=C\\C/C=C\\CCCCC)COC(=O)CCCCCCCCCCCCCCCCC)(O)=O '
               'NAME: Pi(18:0/8,9-eet) REASON: WRONGLY CLASSIFIED Molecule '
               'contains a phosphate group linked to a 6-membered carbon '
               '(inositol) ring and at least 2 ester bonds consistent with a '
               'phosphatidyl moiety\n'
               ' * SMILES: '
               'P(O[C@@H]1C(O)[C@H](OP(O)(O)=O)C(O)C(O)C1O)(OC[C@H](OC(=O)CCCCCCCCCCCCCCC)COC(=O)CCCCCCC/C=C\\C/C=C\\CCCCC)(O)=O '
               'NAME: '
               '{[(1R,3S)-3-({[(2R)-2-(hexadecanoyloxy)-3-[(9Z,12Z)-octadeca-9,12-dienoyloxy]propoxy](hydroxy)phosphoryl}oxy)-2,4,5,6-tetrahydroxycyclohexyl]oxy}phosphonic '
               'acid REASON: WRONGLY CLASSIFIED Molecule contains a phosphate '
               'group linked to a 6-membered carbon (inositol) ring and at '
               'least 2 ester bonds consistent with a phosphatidyl moiety\n'
               ' * SMILES: '
               '[C@@H]1([C@@H]([C@@H]([C@@H]([C@H]([C@@H]1O)OP(O)(=O)O)O)O)OP(OC[C@@H](COC(=O)CCCCCCC)OC(=O)CCCCCCC)(=O)O)O '
               'NAME: '
               '1,2-dioctanoyl-sn-glycero-3-phospho-(1D-myo-inositol-4-phosphate) '
               'REASON: WRONGLY CLASSIFIED Molecule contains a phosphate group '
               'linked to a 6-membered carbon (inositol) ring and at least 2 '
               'ester bonds consistent with a phosphatidyl moiety\n'
               'False negatives: NONE\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'O=C1OC[C@@H]2O[C@@H](O[C@@H]3[C@@H](OC(=O)CCCCCCCCCCCCCCC)[C@H](C=CCCCC1)[C@H](CCCCC)[C@@H](C3)O)[C@H](O)[C@H]([C@@H]2O)O',
                                     'name': 'Mucorolactone',
                                     'reason': 'No six-membered inositol ring '
                                               'with 1 phosphate substituent '
                                               'and 5 free hydroxyls found'},
                                 {   'smiles': 'C[C@@H]1CN[C@H](COC2=C(C=CC(=C2)NC(=O)C3=NC4=CC=CC=C4S3)C(=O)N(C[C@H]1OC)C)C',
                                     'name': 'N-[(5S,6R,9S)-5-methoxy-3,6,9-trimethyl-2-oxo-11-oxa-3,8-diazabicyclo[10.4.0]hexadeca-1(12),13,15-trien-14-yl]-1,3-benzothiazole-2-carboxamide',
                                     'reason': 'Found only 0 ester bond(s); at '
                                               'least 2 are required for the '
                                               'phosphatidyl moiety'},
                                 {   'smiles': 'COC1=CC=CC(=C1)C2=CC=C(C=C2)[C@@H]3[C@@H]4CN(CC(=O)N4[C@@H]3CO)C(=O)C5=CN=CC=C5',
                                     'name': '(6R,7R,8S)-8-(hydroxymethyl)-7-[4-(3-methoxyphenyl)phenyl]-4-[oxo(3-pyridinyl)methyl]-1,4-diazabicyclo[4.2.0]octan-2-one',
                                     'reason': 'Found only 0 ester bond(s); at '
                                               'least 2 are required for the '
                                               'phosphatidyl moiety'},
                                 {   'smiles': 'C(C(/C=C/C=C/C=C/[C@H](CCCC(O)=O)O)=O)/C=C\\CCCCC',
                                     'name': '12-oxo-6-trans-leukotriene B4',
                                     'reason': 'Found only 1 ester bond(s); at '
                                               'least 2 are required for the '
                                               'phosphatidyl moiety'},
                                 {   'smiles': 'O=C1OC(=C(C#C[C@H](COC(=O)C)C)CO)C=C1',
                                     'name': "5'-O-acetylaporpinone A",
                                     'reason': 'No six-membered inositol ring '
                                               'with 1 phosphate substituent '
                                               'and 5 free hydroxyls found'},
                                 {   'smiles': 'O=C(N1[C@@H](CCC1)C(=O)N[C@@H](CCC(=O)N)C(O)=O)[C@@H](N)[C@H](CC)C',
                                     'name': 'Ile-Pro-Gln',
                                     'reason': 'Found only 1 ester bond(s); at '
                                               'least 2 are required for the '
                                               'phosphatidyl moiety'},
                                 {   'smiles': 'O[C@@H]1C=CC=C(CCC(O)=O)[C@@H]1O',
                                     'name': '3-[(5R,6S)-5,6-dihydroxycyclohexa-1,3-dienyl]propanoic '
                                             'acid',
                                     'reason': 'Found only 1 ester bond(s); at '
                                               'least 2 are required for the '
                                               'phosphatidyl moiety'},
                                 {   'smiles': 'O=C(OC)/C=C/C(C)(C)C',
                                     'name': '4,4-Dimethyl-pentenoic acid '
                                             'methyl ester',
                                     'reason': 'Found only 1 ester bond(s); at '
                                               'least 2 are required for the '
                                               'phosphatidyl moiety'},
                                 {   'smiles': 'CCCCOc1ccc(OCCCN2CCOCC2)cc1',
                                     'name': 'pramocaine',
                                     'reason': 'Found only 0 ester bond(s); at '
                                               'least 2 are required for the '
                                               'phosphatidyl moiety'},
                                 {   'smiles': 'OC[C@@H](O)C(=O)[C@H](O)[C@H](O)COP(O)(O)=O',
                                     'name': 'D-arabino-hex-3-ulose '
                                             '6-phosphate',
                                     'reason': 'Found only 0 ester bond(s); at '
                                               'least 2 are required for the '
                                               'phosphatidyl moiety'}],
    'sample_false_negatives': [],
    'attempt': 1,
    'reasoning': 'We can “improve” the previous heuristic by not only checking '
                 'that there is a phosphate attached to a six‐membered carbon '
                 'ring and two ester bonds but also by “inspecting” the ring '
                 'in more detail. In a bona fide '
                 '1‑phosphatidyl‑1D‑myo‑inositol the six‐membered ring (the '
                 'inositol headgroup) is a cyclohexane in which every carbon '
                 'bears an –OH group (so six –OH groups in myo‑inositol). When '
                 'one –OH (by convention the 1‑position) is substituted with a '
                 'phosphatidyl group, the ring then has five free hydroxyl '
                 'groups and exactly one phosphate substituent. (Extra '
                 'phosphate substituents or an inositol ring missing the '
                 'appropriate –OH pattern would be clues that the structure is '
                 'not “1‑phosphatidyl‑1D‑myo‑inositol”.)\n'
                 '\n'
                 'The new approach is to:\n'
                 '1. Parse the molecule.\n'
                 '2. Count the ester bonds (using a SMARTS for C(=O)O) as a '
                 'proxy for the diacyl-glycerol part.\n'
                 '3. Loop over the six‐membered rings formed entirely of '
                 'carbons. For each such ring, inspect all substitutions on '
                 'the ring atoms. For each ring carbon we count:\n'
                 '\u2003\u2003– a “free –OH” (an oxygen neighbor not attached '
                 'to a phosphorus that also has at least one hydrogen) and\n'
                 '\u2003\u2003– a “phospho‐substituent” (an oxygen neighbor '
                 'that is attached to a phosphorus).\n'
                 'Then we require that one ring has exactly one '
                 'phospho‐substituent and five free hydroxyls.\n'
                 'If such a ring is found and there are at least two ester '
                 'bonds, we call the molecule '
                 '“1‑phosphatidyl‑1D‑myo‑inositol”. (Otherwise we reject it.)\n'
                 '\n'
                 'Below is the complete Python code (with comments) that '
                 'implements this improved heuristic. (Remember that because '
                 'this is a simplified “heuristic” approach based on '
                 'substructure matching, it is not perfect.) \n'
                 '\n'
                 'Below is the single code block in Python:\n'
                 '\n'
                 '------------------------------------------------',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 27,
    'num_false_positives': 275,
    'num_true_negatives': 141998,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.08940397350993377,
    'recall': 1.0,
    'f1': 0.16413373860182373,
    'accuracy': 0.9980674631061138,
    'negative_predictive_value': 1.0}