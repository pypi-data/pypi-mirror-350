"""
Classifies: CHEBI:16337 phosphatidic acid
"""
"""
Classifies: Phosphatidic acid (PA)
Definition:
  A derivative of glycerol in which one hydroxy group (commonly but not necessarily primary) is esterified with phosphoric acid 
  and the other two are esterified with fatty acids.
Improvements in this version:
  - Identify a phosphate group by checking for a P atom with ≥3 oxygen neighbors and exactly one oxygen that attaches to a carbon (the phosphate ester).
  - Exclude phosphate groups that carry any explicit negative formal charge on the P or one of its immediate oxygen neighbors.
  - Identify fatty acid ester groups with the substructure "OC(=O)" while filtering out any bridging oxygens attached directly to phosphorus.
  - For each fatty acid ester find the glycerol carbon (avoiding the carbonyl carbon with a C=O) and then try to identify the phosphate-derived glycerol carbon.
  - Verify that the three candidate glycerol carbons (2 from FA esters and 1 from the phosphate ester) are distinct and contiguous (graph distance ≤2).
  - Do a basic molecular weight sanity check.
"""

from rdkit import Chem
from rdkit.Chem import rdMolDescriptors

def is_phosphatidic_acid(smiles: str):
    """
    Determines if a molecule is a phosphatidic acid (PA) based on its SMILES string.
    PA is a glycerol derivative where one hydroxy is esterified with phosphoric acid and the other two with fatty acids.
    
    Args:
      smiles (str): Input SMILES for the molecule.
    
    Returns:
      bool: True if the molecule qualifies as a phosphatidic acid, otherwise False.
      str: Explanation for the classification decision.
    """
    # Parse the SMILES string.
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
    
    # -------------------------
    # Criterion 1: Identify a suitable phosphate group.
    # Look for a phosphorus (P) atom that has at least three oxygen neighbors.
    # Among those oxygens, exactly one should connect to a carbon (the phosphate–glycerol bridging).
    # Also, none of the atoms in the phosphate head (P and its O neighbors) should carry a negative formal charge.
    valid_P_atom = None
    for atom in mol.GetAtoms():
        if atom.GetSymbol() != "P":
            continue
        # Check formal charge on the phosphorus.
        if atom.GetFormalCharge() < 0:
            continue
        
        oxy_neighbors = [nbr for nbr in atom.GetNeighbors() if nbr.GetSymbol() == "O"]
        if len(oxy_neighbors) < 3:
            continue
        
        # Eliminate any phosphate group with any negatively charged oxygen neighbor.
        neg_charge = False
        for o in oxy_neighbors:
            if o.GetFormalCharge() < 0:
                neg_charge = True
                break
        if neg_charge:
            continue
        
        # Count among these oxygens how many are attached to at least one carbon (other than the P).
        o_attached_to_C = 0
        for o in oxy_neighbors:
            for nbr2 in o.GetNeighbors():
                if nbr2.GetIdx() == atom.GetIdx():
                    continue
                if nbr2.GetSymbol() == "C":
                    o_attached_to_C += 1
                    break
        if o_attached_to_C == 1:
            valid_P_atom = atom
            break
    if valid_P_atom is None:
        return False, "No phosphate group found with ≥3 oxygen neighbors (all neutral) and exactly one oxygen attached to a carbon"
    
    # -------------------------
    # Criterion 2: Identify fatty acid ester (FA) groups.
    # Look for the substructure "OC(=O)". Then make sure that the bridging oxygen is not directly attached to phosphorus.
    fa_pattern = Chem.MolFromSmarts("OC(=O)")
    fa_matches = mol.GetSubstructMatches(fa_pattern)
    fa_candidates = []    # To collect candidate glycerol carbon indices (from the FA ester linkage)
    bridging_O_indices = set()  # To mark oxygens used in FA linkages.
    
    for match in fa_matches:
        # Each match is a tuple: (bridging O, carbonyl C, carbonyl O)
        bridging_O_idx = match[0]
        bridging_O = mol.GetAtomWithIdx(bridging_O_idx)
        # Skip if bridging oxygen is bonded to any phosphorus.
        if any(nbr.GetSymbol() == "P" for nbr in bridging_O.GetNeighbors()):
            continue
        
        # From the bridging O, choose a neighbor that is a carbon and is not the carbonyl carbon.
        candidate = None
        for nbr in bridging_O.GetNeighbors():
            if nbr.GetSymbol() != "C":
                continue
            # Distinguish the glycerol carbon from the carbonyl carbon by checking for a double bonded oxygen.
            has_double_bond_oxygen = False
            for nbr2 in nbr.GetNeighbors():
                if nbr2.GetIdx() == bridging_O.GetIdx():
                    continue
                bond = mol.GetBondBetweenAtoms(nbr.GetIdx(), nbr2.GetIdx())
                if nbr2.GetSymbol() == "O" and bond is not None and bond.GetBondType() == Chem.rdchem.BondType.DOUBLE:
                    has_double_bond_oxygen = True
                    break
            if not has_double_bond_oxygen:
                candidate = nbr.GetIdx()
                break
        if candidate is not None:
            fa_candidates.append(candidate)
            bridging_O_indices.add(bridging_O_idx)
    if len(fa_candidates) != 2:
        return False, f"Found {len(fa_candidates)} fatty acid ester group(s) after filtering; expected exactly 2."
    
    # -------------------------
    # Criterion 3: Identify the glycerol carbon from the phosphate ester.
    # Look at the P atom’s oxygen neighbors (excluding those already used for FA ester linkages)
    # and find candidate oxygens that lead to a carbon.
    phospho_candidate_list = []
    for o in valid_P_atom.GetNeighbors():
        if o.GetSymbol() != "O":
            continue
        if o.GetIdx() in bridging_O_indices:
            continue
        # For each such oxygen, if it leads to a carbon (other than the P) then add that carbon as candidate.
        for nbr in o.GetNeighbors():
            if nbr.GetIdx() == valid_P_atom.GetIdx():
                continue
            if nbr.GetSymbol() == "C":
                phospho_candidate_list.append(nbr.GetIdx())
                break   # Taking the first carbon is sufficient for this oxygen.
                
    # We expect the phosphate ester to contribute exactly one glycerol carbon.
    # But if more than one candidate is found, test each one by forming a set with the two FA candidates.
    candidate_found = None
    dmat = Chem.GetDistanceMatrix(mol)
    for pc in phospho_candidate_list:
        glycerol_set = set(fa_candidates)
        glycerol_set.add(pc)
        if len(glycerol_set) != 3:
            continue
        # Check connectivity: graph distance between any two glycerol candidates must be ≤ 2.
        distances_ok = True
        for a in glycerol_set:
            for b in glycerol_set:
                if a == b:
                    continue
                if dmat[a][b] > 2:
                    distances_ok = False
                    break
            if not distances_ok:
                break
        if distances_ok:
            candidate_found = pc
            break
    if candidate_found is None:
        return False, "Could not find a single phosphate-derived glycerol carbon that connects with the two FA ester glycerol carbons within a graph distance of 2."
    
    # Now the three glycerol carbons are the two from FA ester groups and candidate_found.
    glycerol_set = set(fa_candidates)
    glycerol_set.add(candidate_found)
    if len(glycerol_set) != 3:
        return False, "Fatty acid ester groups and the phosphate ester do not attach to three distinct glycerol carbons."
    
    # -------------------------
    # Criterion 4: (Optional) Molecular weight sanity check.
    mol_wt = rdMolDescriptors.CalcExactMolWt(mol)
    if mol_wt < 300:
        return False, f"Molecular weight ({mol_wt:.1f} Da) is too low for a phosphatidic acid"
    
    return True, "Contains a phosphate group (with neutral head) and exactly two fatty acid esters attached to a connected three‐carbon glycerol backbone"

# Example usage:
if __name__ == "__main__":
    # Test one of the provided true positive SMILES (phosphatidic acid with two FA esters and a phosphate ester).
    test_smiles = "P(OC[C@H](OC(=O)CCCCCCCCCCCCC)COC(=O)CCCCCCCCC/C=C\\CCCCCCCC)(O)(O)=O"
    result, reason = is_phosphatidic_acid(test_smiles)
    print("Is phosphatidic acid?", result)
    print("Reason:", reason)


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:16337',
                          'name': 'phosphatidic acid',
                          'definition': 'A derivative of glycerol in which one '
                                        'hydroxy group, commonly but not '
                                        'necessarily primary, is esterified '
                                        'with phosphoric acid and the other '
                                        'two are esterified with fatty acids.',
                          'parents': ['CHEBI:37739'],
                          'xrefs': ['KEGG:C00416'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 144,
                           'log_lines_of_code': 4.969813299576001,
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
                                                 3,
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
                                                 2,
                                                 3,
                                                 4,
                                                 4,
                                                 2,
                                                 3,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 4,
                                                 5,
                                                 4,
                                                 5,
                                                 5,
                                                 2,
                                                 3,
                                                 3,
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
                                                 4,
                                                 3,
                                                 3,
                                                 3,
                                                 4,
                                                 5,
                                                 4,
                                                 4,
                                                 5,
                                                 5,
                                                 3,
                                                 4,
                                                 4,
                                                 2,
                                                 3,
                                                 3,
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
                                                 3,
                                                 2,
                                                 3,
                                                 2,
                                                 2,
                                                 3,
                                                 4,
                                                 3,
                                                 4,
                                                 4,
                                                 4,
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
                                                 4,
                                                 5,
                                                 4,
                                                 5,
                                                 5,
                                                 3,
                                                 4,
                                                 2,
                                                 3,
                                                 3,
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
                                                 1],
                           'max_indent': 5,
                           'imports': [   'from rdkit import Chem',
                                          'from rdkit.Chem import '
                                          'rdMolDescriptors'],
                           'imports_count': 2,
                           'methods_called': [   'GetDistanceMatrix',
                                                 'GetBondType',
                                                 'CalcExactMolWt',
                                                 'GetAtoms',
                                                 'GetNeighbors',
                                                 'MolFromSmiles',
                                                 'GetBondBetweenAtoms',
                                                 'GetSubstructMatches',
                                                 'append',
                                                 'GetFormalCharge',
                                                 'GetSymbol',
                                                 'GetIdx',
                                                 'MolFromSmarts',
                                                 'GetAtomWithIdx',
                                                 'add'],
                           'methods_called_count': 15,
                           'smarts_strings': ['OC(=O)'],
                           'smarts_strings_count': 1,
                           'defs': ['is_phosphatidic_acid(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "No phosphate group found '
                                          'with ≥3 oxygen neighbors (all '
                                          'neutral) and exactly one oxygen '
                                          'attached to a carbon"',
                                          'False, f"Found {len(fa_candidates)} '
                                          'fatty acid ester group(s) after '
                                          'filtering; expected exactly 2."',
                                          'False, "Could not find a single '
                                          'phosphate-derived glycerol carbon '
                                          'that connects with the two FA ester '
                                          'glycerol carbons within a graph '
                                          'distance of 2."',
                                          'False, "Fatty acid ester groups and '
                                          'the phosphate ester do not attach '
                                          'to three distinct glycerol '
                                          'carbons."',
                                          'False, f"Molecular weight '
                                          '({mol_wt:.1f} Da) is too low for a '
                                          'phosphatidic acid"',
                                          'True, "Contains a phosphate group '
                                          '(with neutral head) and exactly two '
                                          'fatty acid esters attached to a '
                                          'connected three‐carbon glycerol '
                                          'backbone"'],
                           'returns_count': 7,
                           'complexity': 6.593962659915201},
    'message': '\n'
               'Attempt failed: F1 score of 0.872289156626506 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: '
               'P(OC[C@H](OC(=O)CCCCCCCCCCCCC)COC(=O)CCCCCCCCC/C=C\\CCCCCCCC)(O)(O)=O '
               'NAME: PA(20:1(11Z)/14:0) REASON: CORRECT Contains a phosphate '
               'group and exactly two fatty acid esters attached to a '
               'connected three-carbon glycerol backbone\n'
               ' * SMILES: '
               'P(OC[C@H](OC(=O)CCCCCCC/C=C\\CCCC)COC(=O)CCCCCCCCCCC/C=C\\C/C=C\\CCCCC)(O)(O)=O '
               'NAME: PA(22:2(13Z,16Z)/14:1(9Z)) REASON: CORRECT Contains a '
               'phosphate group and exactly two fatty acid esters attached to '
               'a connected three-carbon glycerol backbone\n'
               ' * SMILES: '
               'P(OC[C@H](OC(=O)CCCCCCCCCCCCCCCCC)COC(=O)CCCCCCC/C=C\\CCCCCC)(O)(O)=O '
               'NAME: PA(16:1(9Z)/18:0) REASON: CORRECT Contains a phosphate '
               'group and exactly two fatty acid esters attached to a '
               'connected three-carbon glycerol backbone\n'
               ' * SMILES: '
               'P(OC[C@H](OC(=O)CCCCCCCCCCC/C=C\\CCCCCCCC)COC(=O)CCCCCCC/C=C\\CCCCCCCC)(O)(O)=O '
               'NAME: '
               '[(2R)-2-[(13Z)-docos-13-enoyloxy]-3-[(9Z)-octadec-9-enoyloxy]propoxy]phosphonic '
               'acid REASON: CORRECT Contains a phosphate group and exactly '
               'two fatty acid esters attached to a connected three-carbon '
               'glycerol backbone\n'
               ' * SMILES: '
               'P(OC[C@H](OC(=O)CCCCCCC/C=C\\CCCCC)COC(=O)CCCCCCCCCCCCCCCCCCCCC)(O)(O)=O '
               'NAME: PA(22:0/15:1(9Z)) REASON: CORRECT Contains a phosphate '
               'group and exactly two fatty acid esters attached to a '
               'connected three-carbon glycerol backbone\n'
               ' * SMILES: '
               'P(OC[C@H](OC(=O)CCCCCCCCCCCCC/C=C\\CCCCCCCC)COC(=O)CCCC(O)C(O)C/C=C\\C/C=C\\C/C=C\\CCCCC)(O)(O)=O '
               'NAME: PA(20:3(8Z,11Z,14Z)-2OH(5,6)/24:1(15Z)) REASON: CORRECT '
               'Contains a phosphate group and exactly two fatty acid esters '
               'attached to a connected three-carbon glycerol backbone\n'
               ' * SMILES: '
               'P(OC[C@H](OC(=O)CCCCCCC/C=C\\CCCCCC)COC(=O)CCCCCCCCCCCCCCCCCC)(O)(O)=O '
               'NAME: PA(19:0/16:1(9Z)) REASON: CORRECT Contains a phosphate '
               'group and exactly two fatty acid esters attached to a '
               'connected three-carbon glycerol backbone\n'
               ' * SMILES: '
               '[C@](COC(=O)CCCCCCCCCCC)(OC(=O)CCC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)([H])COP(O)(O)=O '
               'NAME: PA(12:0/20:5(5Z,8Z,11Z,14Z,17Z)) REASON: CORRECT '
               'Contains a phosphate group and exactly two fatty acid esters '
               'attached to a connected three-carbon glycerol backbone\n'
               ' * SMILES: '
               'P(OC[C@H](OC(=O)CCCCCCCCCCCCCCCCCCC)COC(=O)CCCCCCCCCCCCC)(O)(O)=O '
               'NAME: PA(14:0/20:0) REASON: CORRECT Contains a phosphate group '
               'and exactly two fatty acid esters attached to a connected '
               'three-carbon glycerol backbone\n'
               ' * SMILES: '
               'P(OC[C@H](OC(=O)CCCCCCCCCCCCCCCCCCCC)COC(=O)CCCCCCCCC/C=C\\CCCCCCCC)(O)(O)=O '
               'NAME: PA(20:1(11Z)/21:0) REASON: CORRECT Contains a phosphate '
               'group and exactly two fatty acid esters attached to a '
               'connected three-carbon glycerol backbone\n'
               ' * SMILES: '
               'P(OC[C@H](OC(=O)CCCCCCC/C=C\\C/C=C\\CCCCC)COC(=O)CCCCCCCCCCCC)(O)(O)=O '
               'NAME: PA(13:0/18:2(9Z,12Z)) REASON: CORRECT Contains a '
               'phosphate group and exactly two fatty acid esters attached to '
               'a connected three-carbon glycerol backbone\n'
               ' * SMILES: '
               'P(OC[C@H](OC(=O)CCCCCC/C=C\\C/C=C\\C/C=C\\CCCCC)COC(=O)CCCCCCCCCCCCC)(O)(O)=O '
               'NAME: PA(14:0/20:3(8Z,11Z,14Z)) REASON: CORRECT Contains a '
               'phosphate group and exactly two fatty acid esters attached to '
               'a connected three-carbon glycerol backbone\n'
               ' * SMILES: '
               'P(OC[C@H](OC(=O)CCCC/C=C\\C/C=C\\C/C=C\\CCCCC)COC(=O)CCCCCCC/C=C\\CCCCCCCC)(O)(O)=O '
               'NAME: PA(18:1(9Z)/18:3(6Z,9Z,12Z)) REASON: CORRECT Contains a '
               'phosphate group and exactly two fatty acid esters attached to '
               'a connected three-carbon glycerol backbone\n'
               ' * SMILES: '
               'P(OC[C@H](OC(=O)CC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)COC(=O)CCCCCCC/C=C\\C/C=C\\CCCC)(O)(O)=O '
               'NAME: PA(17:2(9Z,12Z)/22:6(4Z,7Z,10Z,13Z,16Z,19Z)) REASON: '
               'CORRECT Contains a phosphate group and exactly two fatty acid '
               'esters attached to a connected three-carbon glycerol backbone\n'
               ' * SMILES: '
               'P(OC[C@H](OC(=O)CCCCCCCCCCCCC)COC(=O)CCCCCCCCCCCCCCCCC)(O)(O)=O '
               'NAME: PA(18:0/14:0) REASON: CORRECT Contains a phosphate group '
               'and exactly two fatty acid esters attached to a connected '
               'three-carbon glycerol backbone\n'
               ' * SMILES: '
               'P(OC[C@H](OC(=O)CC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)COC(=O)CCCC/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)(O)(O)=O '
               'NAME: Pa(18:4(6z,9z,12z,15z)/22:6(4z,7z,10z,13z,16z,19z)) '
               'REASON: CORRECT Contains a phosphate group and exactly two '
               'fatty acid esters attached to a connected three-carbon '
               'glycerol backbone\n'
               ' * SMILES: '
               'P(OC[C@H](OC(=O)CCCCC/C=C\\C/C=C\\C/C=C\\C/C=C\\CCCCC)COC(=O)CCCCCCCCCCCCCCCCCCCC)(O)(O)=O '
               'NAME: PA(21:0/22:4(7Z,10Z,13Z,16Z)) REASON: CORRECT Contains a '
               'phosphate group and exactly two fatty acid esters attached to '
               'a connected three-carbon glycerol backbone\n'
               ' * SMILES: '
               'P(OC[C@H](OC(=O)CCC(O)/C=C/C=O)COC(=O)CCCCCCCCCCCCCCC)(O)(O)=O '
               'NAME: PHOHA-PA REASON: CORRECT Contains a phosphate group and '
               'exactly two fatty acid esters attached to a connected '
               'three-carbon glycerol backbone\n'
               ' * SMILES: '
               'P(OC[C@H](OC(=O)CCC[C@@H](O)/C=C\\C=C\\C=C\\[C@@H](O)C/C=C\\CCCCC)COC(=O)CCCCCCCCCCCCCCCC)(O)(O)=O '
               'NAME: PA(17:0/20:4(6Z,8E,10E,14Z)-2OH(5S,12R)) REASON: CORRECT '
               'Contains a phosphate group and exactly two fatty acid esters '
               'attached to a connected three-carbon glycerol backbone\n'
               ' * SMILES: '
               'P(OC[C@H](OC(=O)CCCCCCCCCCCCCCCC)COC(=O)CCCCCCCCCCCCCCCC)(O)(O)=O '
               'NAME: PA(17:0/17:0) REASON: CORRECT Contains a phosphate group '
               'and exactly two fatty acid esters attached to a connected '
               'three-carbon glycerol backbone\n'
               ' * SMILES: '
               'P(OC[C@H](OC(=O)CCCCCCC/C=C\\CCCCCCC)COC(=O)CCCCCCCCCCCCCCC)(O)(O)=O '
               'NAME: PA(16:0/17:1(9Z)) REASON: CORRECT Contains a phosphate '
               'group and exactly two fatty acid esters attached to a '
               'connected three-carbon glycerol backbone\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCC(=O)OC[C@H](COP(O)(O)=O)OC(=O)CCCCCCCCCCCCCCC '
               'NAME: 1-heptadecanoyl-2-palmitoyl-sn-glycero-3-phosphate '
               'REASON: CORRECT Contains a phosphate group and exactly two '
               'fatty acid esters attached to a connected three-carbon '
               'glycerol backbone\n'
               ' * SMILES: '
               'P(OC[C@H](OC(=O)CCCCCCCCCCC/C=C\\CCCCCCCC)COC(=O)CCCCCCCCCCCCCCCCCCCCCCC)(O)(O)=O '
               'NAME: '
               '[(2R)-2-[(13Z)-docos-13-enoyloxy]-3-(tetracosanoyloxy)propoxy]phosphonic '
               'acid REASON: CORRECT Contains a phosphate group and exactly '
               'two fatty acid esters attached to a connected three-carbon '
               'glycerol backbone\n'
               ' * SMILES: '
               'P(OC[C@H](OC(=O)CCCCCCCCC/C=C\\C/C=C\\CCCCC)COC(=O)CCCCCCC/C=C\\C/C=C\\C/C=C\\CC)(O)(O)=O '
               'NAME: PA(18:3(9Z,12Z,15Z)/20:2(11Z,14Z)) REASON: CORRECT '
               'Contains a phosphate group and exactly two fatty acid esters '
               'attached to a connected three-carbon glycerol backbone\n'
               ' * SMILES: '
               'O(C(COP(=O)(O)O)COC(=O)CCCCCCCC=CCCCCCCCC)C(=O)CCCCCCCC=CCCCCCCCC '
               'NAME: 1,2-bis(octadec-9-enoyl)phosphatidic acid REASON: '
               'CORRECT Contains a phosphate group and exactly two fatty acid '
               'esters attached to a connected three-carbon glycerol backbone\n'
               'False positives: SMILES: '
               'CCCCCCCCCCCCCCCC(=O)O[C@H](COC(=O)CCCCCCC\\C=C/CCCCCCCC)COP([O-])([O-])=O '
               'NAME: 1-oleoyl-2-palmitoyl-sn-glycero-3-phosphate(2-) REASON: '
               'WRONGLY CLASSIFIED Contains a phosphate group and exactly two '
               'fatty acid esters attached to a connected three-carbon '
               'glycerol backbone\n'
               ' * SMILES: '
               'P(OC[C@H](OC(=O)CCCCCCCCCCCCCCCCC)COC(=O)C/C=C\\C[C@H]1[C@H]([C@H](O)C[C@@H]1O)/C=C/[C@H](O)CCCCC)(O)(O)=O '
               'NAME: PA(5-iso PGF2VI/18:0) REASON: WRONGLY CLASSIFIED '
               'Contains a phosphate group and exactly two fatty acid esters '
               'attached to a connected three-carbon glycerol backbone\n'
               ' * SMILES: '
               'P(OC[C@H](OC(=O)CCCCCCCCCCCCCCCCCCCCC(CC)C)COC(=O)CCCCCC[C@@H]1[C@H]([C@H](O)C[C@@H]1O)/C=C/[C@@H](O)CCCCC)(O)(O)=O '
               'NAME: PA(PGF1alpha/a-25:0) REASON: WRONGLY CLASSIFIED Contains '
               'a phosphate group and exactly two fatty acid esters attached '
               'to a connected three-carbon glycerol backbone\n'
               ' * SMILES: '
               'CCCCCCCCCC(=O)OC[C@H](COP([O-])([O-])=O)OC(=O)CCCCCCCCC NAME: '
               '1,2-dicapryl-sn-glycero-3-phosphate(2-) REASON: WRONGLY '
               'CLASSIFIED Contains a phosphate group and exactly two fatty '
               'acid esters attached to a connected three-carbon glycerol '
               'backbone\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCC(=O)O[C@H](COC(=O)CCCCCCC\\C=C/CCCCCCCC)COP([O-])([O-])=O '
               'NAME: 1-oleoyl-2-stearoyl-sn-glycero-3-phosphate(2-) REASON: '
               'WRONGLY CLASSIFIED Contains a phosphate group and exactly two '
               'fatty acid esters attached to a connected three-carbon '
               'glycerol backbone\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCC(=O)OC[C@H](COP([O-])([O-])=O)OC(=O)CC\\C=C/C\\C=C/C\\C=C/C\\C=C/C\\C=C/C\\C=C/CC '
               'NAME: '
               '1-stearoyl-2-(4Z,7Z,10Z,13Z,16Z,19Z)-docosahexaenoyl-sn-glycero-3-phosphate(2-) '
               'REASON: WRONGLY CLASSIFIED Contains a phosphate group and '
               'exactly two fatty acid esters attached to a connected '
               'three-carbon glycerol backbone\n'
               ' * SMILES: '
               'P(OC[C@H](OC(=O)CCCCCCCCCCCCC)COC(=O)CCCC(O)/C=C/C=C/C\\C=C\\CCCCCCCC)(O)(O)=O '
               'NAME: PA(20:3(6,8,11)-OH(5)/14:0) REASON: WRONGLY CLASSIFIED '
               'Contains a phosphate group and exactly two fatty acid esters '
               'attached to a connected three-carbon glycerol backbone\n'
               ' * SMILES: '
               'P(=O)([O-])([O-])OC[C@H](OC(CCCC=O)=O)COC(=O)CCCCCCCCCCCCCCC '
               'NAME: 1-palmitoyl-2-(5-oxovaleroyl)-sn-glycero-3-phosphate(2-) '
               'REASON: WRONGLY CLASSIFIED Contains a phosphate group and '
               'exactly two fatty acid esters attached to a connected '
               'three-carbon glycerol backbone\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCC(=O)OC[C@H](COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1O)n1ccc(N)nc1=O)OC(=O)CCCCCCC\\C=C/CCCCCCCC '
               'NAME: CDP-1-stearoyl-2-oleoyl-sn-glycerol(2-) REASON: WRONGLY '
               'CLASSIFIED Contains a phosphate group and exactly two fatty '
               'acid esters attached to a connected three-carbon glycerol '
               'backbone\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCC(=O)OC[C@H](COP([O-])([O-])=O)OC(=O)CCCCCCCCCCCCCCCCC '
               'NAME: 1,2-dioctadecanoyl-sn-glycerol-3-phosphate(2-) REASON: '
               'WRONGLY CLASSIFIED Contains a phosphate group and exactly two '
               'fatty acid esters attached to a connected three-carbon '
               'glycerol backbone\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCC(=O)OC[C@H](COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1O)n1ccc(N)nc1=O)OC(=O)CCCCCCC\\C=C/CCCCCCCC '
               'NAME: CDP-1-stearoyl-2-oleoyl-sn-glycerol REASON: WRONGLY '
               'CLASSIFIED Contains a phosphate group and exactly two fatty '
               'acid esters attached to a connected three-carbon glycerol '
               'backbone\n'
               ' * SMILES: '
               'CCCCCCCC\\C=C/CCCCCCCC(=O)OC[C@H](COP([O-])([O-])=O)OC(=O)CCC\\C=C/C\\C=C/C\\C=C/C\\C=C/CCCCC '
               'NAME: 1-oleoyl-2-arachidonoyl-sn-glycero-3-phosphate(2-) '
               'REASON: WRONGLY CLASSIFIED Contains a phosphate group and '
               'exactly two fatty acid esters attached to a connected '
               'three-carbon glycerol backbone\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCC(=O)O[C@H](COC(=O)CCCCCCC\\C=C/CCCCCCCC)COP([O-])([O-])=O '
               'NAME: 1-oleoyl-2-pentadecanoyl-sn-glycero-3-phosphate(2-) '
               'REASON: WRONGLY CLASSIFIED Contains a phosphate group and '
               'exactly two fatty acid esters attached to a connected '
               'three-carbon glycerol backbone\n'
               ' * SMILES: '
               'CCCCC\\C=C/C\\C=C/C\\C=C/C\\C=C/CCCC(=O)OC[C@H](COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1O)n1ccc(N)nc1=O)OC(=O)CCC\\C=C/C\\C=C/C\\C=C/C\\C=C/CCCCC '
               'NAME: CDP-1,2-diarachidonoyl-sn-glycerol REASON: WRONGLY '
               'CLASSIFIED Contains a phosphate group and exactly two fatty '
               'acid esters attached to a connected three-carbon glycerol '
               'backbone\n'
               ' * SMILES: '
               'CCCCCCCC(=O)OC[C@H](COP(O)(=O)OP(O)(O)=O)OC(=O)CCCCCCC NAME: '
               '1,2-dioctanoyl-sn-glycerol 3-diphosphate REASON: WRONGLY '
               'CLASSIFIED Contains a phosphate group and exactly two fatty '
               'acid esters attached to a connected three-carbon glycerol '
               'backbone\n'
               ' * SMILES: '
               'O(C[C@@H](COC(CCCCCCCCCCCCCCCCC)=O)OC(CCCCCCCCCCCCCCCCC)=O)P(OP(OC[C@H]1O[C@H]([C@H](O)[C@@H]1O)N2C(N=C(C=C2)N)=O)(=O)O)(=O)O '
               "NAME: 1,2-dioctadecanoyl-sn-glycero-3-cytidine 5'-diphosphate "
               'REASON: WRONGLY CLASSIFIED Contains a phosphate group and '
               'exactly two fatty acid esters attached to a connected '
               'three-carbon glycerol backbone\n'
               ' * SMILES: '
               '[C@@H](COC(CCCCCCC/C=C\\CCCCCCCC)=O)(COP([O-])(=O)[O-])OC(CC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)=O '
               'NAME: '
               '1-oleoyl-2-[(4Z,7Z,10Z,13Z,16Z,19Z)-docosahexaenoyl]-sn-glycero-3-phosphate(2-) '
               'REASON: WRONGLY CLASSIFIED Contains a phosphate group and '
               'exactly two fatty acid esters attached to a connected '
               'three-carbon glycerol backbone\n'
               ' * SMILES: '
               'CCCCCCCC\\C=C/CCCCCCCC(=O)OC[C@H](COP([O-])([O-])=O)OC(=O)CCCCCCC\\C=C/C\\C=C/CCCCC '
               'NAME: 1-oleoyl-2-linoleoyl-sn-glycero-3-phosphate(2-) REASON: '
               'WRONGLY CLASSIFIED Contains a phosphate group and exactly two '
               'fatty acid esters attached to a connected three-carbon '
               'glycerol backbone\n'
               ' * SMILES: '
               'O(C[C@@H](COC(CCCCCCCCCC=CCCCCCC)=O)OC(CCCCCCCCCC=CCCCCCC)=O)P(OP(OC[C@H]1O[C@H]([C@H](O)[C@@H]1O)N2C(N=C(C=C2)N)=O)(=O)O)(=O)O '
               'NAME: 1,2-dioctadec-11-enoyl-sn-glycero-3-cytidine '
               "5'-diphosphate REASON: WRONGLY CLASSIFIED Contains a phosphate "
               'group and exactly two fatty acid esters attached to a '
               'connected three-carbon glycerol backbone\n'
               ' * SMILES: '
               'CC\\C=C/C\\C=C/C\\C=C/C\\C=C/C\\C=C/C\\C=C/CCC(=O)OC[C@H](COP([O-])([O-])=O)OC(=O)CC\\C=C/C\\C=C/C\\C=C/C\\C=C/C\\C=C/C\\C=C/CC '
               'NAME: '
               '1,2-di[(4Z,7Z,10Z,13Z,16Z,19Z)-docosahexaenoyl]-sn-glycero-3-phosphate(2-) '
               'REASON: WRONGLY CLASSIFIED Contains a phosphate group and '
               'exactly two fatty acid esters attached to a connected '
               'three-carbon glycerol backbone\n'
               ' * SMILES: '
               'P(OC[C@H](OC(=O)CCC[C@@H](O)[C@H](O)C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)COC(=O)CCCCCCCCCCCCCCCCCCCCC(CC)C)(O)(O)=O '
               'NAME: PA(a-25:0/20:4(8Z,11Z,14Z,17Z)-2OH(5S,6R)) REASON: '
               'WRONGLY CLASSIFIED Contains a phosphate group and exactly two '
               'fatty acid esters attached to a connected three-carbon '
               'glycerol backbone\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCC(=O)OC[C@H](COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1O)n1ccc(N)nc1=O)OC(=O)CC\\C=C/C\\C=C/C\\C=C/C\\C=C/C\\C=C/C\\C=C/CC '
               'NAME: '
               'CDP-1-stearoyl-2-(4Z,7Z,10Z,13Z,16Z,19Z)-docosahexaenoyl-sn-glycerol '
               'REASON: WRONGLY CLASSIFIED Contains a phosphate group and '
               'exactly two fatty acid esters attached to a connected '
               'three-carbon glycerol backbone\n'
               ' * SMILES: '
               '[H][C@@](COC(=O)CCCCCCC\\C=C/CCCCCC)(COP([O-])([O-])=O)OC(=O)CCCCCCC\\C=C/CCCCCC '
               'NAME: 1,2-di-[(9Z)-hexadecenoyl]-sn-glycero-3-phosphate(2-) '
               'REASON: WRONGLY CLASSIFIED Contains a phosphate group and '
               'exactly two fatty acid esters attached to a connected '
               'three-carbon glycerol backbone\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCC(=O)OC[C@H](COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1O)n1ccc(N)nc1=O)OC(=O)CCC\\C=C/C\\C=C/C\\C=C/C\\C=C/CCCCC '
               'NAME: CDP-1-palmitoyl-2-arachidonoyl-sn-glycerol REASON: '
               'WRONGLY CLASSIFIED Contains a phosphate group and exactly two '
               'fatty acid esters attached to a connected three-carbon '
               'glycerol backbone\n'
               ' * SMILES: '
               'P(OC[C@H](OC(=O)CCC\\C=C\\C[C@@H]1[C@H]([C@H](O)C[C@@H]1O)/C=C/[C@@H](O)CCCCC)COC(=O)CCCCCCCCCCCC)(O)(O)=O '
               'NAME: PA(13:0/PGF2alpha) REASON: WRONGLY CLASSIFIED Contains a '
               'phosphate group and exactly two fatty acid esters attached to '
               'a connected three-carbon glycerol backbone\n'
               'False negatives: SMILES: '
               'CCCCCCCCCCCCCCCC(=O)OCC(COP(O)(=O)OCC(O)COP(O)(O)=O)OC(=O)CCCCCCC\\C=C/CCCCCCCC '
               'NAME: '
               '1-hexadecanoyl-2-[(Z)-octadec-9-enoyl]-sn-glycero-3-phospho-sn-glycerol '
               '3-phosphate REASON: MISSED The three candidate glycerol '
               'carbons are not sufficiently connected (graph distance >2)\n'
               ' * SMILES: '
               'CCCCC\\C=C/C\\C=C/C\\C=C/CCCCC(=O)OC[C@@H](O)COP(O)(O)=O NAME: '
               '1-(gamma-linolenoyl)-sn-glycero-3-phosphate REASON: MISSED '
               'Found 1 fatty acid ester group(s) after filtering; expected '
               'exactly 2.\n'
               ' * SMILES: O1C(C1)COC(=O)CCCC=CCC=CCC=CCC=CCCCCC NAME: '
               'O-Arachidonoyl Glycidol REASON: MISSED No phosphate group '
               'found with >=3 oxygen neighbors and exactly one oxygen '
               'attached to a carbon\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'O=C1OC[C@@H]2O[C@@H](O[C@@H]3[C@@H](OC(=O)CCCCCCCCCCCCCCC)[C@H](C=CCCCC1)[C@H](CCCCC)[C@@H](C3)O)[C@H](O)[C@H]([C@@H]2O)O',
                                     'name': 'Mucorolactone',
                                     'reason': 'No phosphate group found with '
                                               '≥3 oxygen neighbors (all '
                                               'neutral) and exactly one '
                                               'oxygen attached to a carbon'},
                                 {   'smiles': 'C[C@@H]1CN[C@H](COC2=C(C=CC(=C2)NC(=O)C3=NC4=CC=CC=C4S3)C(=O)N(C[C@H]1OC)C)C',
                                     'name': 'N-[(5S,6R,9S)-5-methoxy-3,6,9-trimethyl-2-oxo-11-oxa-3,8-diazabicyclo[10.4.0]hexadeca-1(12),13,15-trien-14-yl]-1,3-benzothiazole-2-carboxamide',
                                     'reason': 'No phosphate group found with '
                                               '≥3 oxygen neighbors (all '
                                               'neutral) and exactly one '
                                               'oxygen attached to a carbon'},
                                 {   'smiles': 'COC1=CC=CC(=C1)C2=CC=C(C=C2)[C@@H]3[C@@H]4CN(CC(=O)N4[C@@H]3CO)C(=O)C5=CN=CC=C5',
                                     'name': '(6R,7R,8S)-8-(hydroxymethyl)-7-[4-(3-methoxyphenyl)phenyl]-4-[oxo(3-pyridinyl)methyl]-1,4-diazabicyclo[4.2.0]octan-2-one',
                                     'reason': 'No phosphate group found with '
                                               '≥3 oxygen neighbors (all '
                                               'neutral) and exactly one '
                                               'oxygen attached to a carbon'},
                                 {   'smiles': 'C(C(/C=C/C=C/C=C/[C@H](CCCC(O)=O)O)=O)/C=C\\CCCCC',
                                     'name': '12-oxo-6-trans-leukotriene B4',
                                     'reason': 'No phosphate group found with '
                                               '≥3 oxygen neighbors (all '
                                               'neutral) and exactly one '
                                               'oxygen attached to a carbon'},
                                 {   'smiles': 'O=C1OC(=C(C#C[C@H](COC(=O)C)C)CO)C=C1',
                                     'name': "5'-O-acetylaporpinone A",
                                     'reason': 'No phosphate group found with '
                                               '≥3 oxygen neighbors (all '
                                               'neutral) and exactly one '
                                               'oxygen attached to a carbon'},
                                 {   'smiles': 'O=C(N1[C@@H](CCC1)C(=O)N[C@@H](CCC(=O)N)C(O)=O)[C@@H](N)[C@H](CC)C',
                                     'name': 'Ile-Pro-Gln',
                                     'reason': 'No phosphate group found with '
                                               '≥3 oxygen neighbors (all '
                                               'neutral) and exactly one '
                                               'oxygen attached to a carbon'},
                                 {   'smiles': 'O[C@@H]1C=CC=C(CCC(O)=O)[C@@H]1O',
                                     'name': '3-[(5R,6S)-5,6-dihydroxycyclohexa-1,3-dienyl]propanoic '
                                             'acid',
                                     'reason': 'No phosphate group found with '
                                               '≥3 oxygen neighbors (all '
                                               'neutral) and exactly one '
                                               'oxygen attached to a carbon'},
                                 {   'smiles': 'O=C(OC)/C=C/C(C)(C)C',
                                     'name': '4,4-Dimethyl-pentenoic acid '
                                             'methyl ester',
                                     'reason': 'No phosphate group found with '
                                               '≥3 oxygen neighbors (all '
                                               'neutral) and exactly one '
                                               'oxygen attached to a carbon'},
                                 {   'smiles': 'CCCCOc1ccc(OCCCN2CCOCC2)cc1',
                                     'name': 'pramocaine',
                                     'reason': 'No phosphate group found with '
                                               '≥3 oxygen neighbors (all '
                                               'neutral) and exactly one '
                                               'oxygen attached to a carbon'},
                                 {   'smiles': 'OC[C@@H](O)C(=O)[C@H](O)[C@H](O)COP(O)(O)=O',
                                     'name': 'D-arabino-hex-3-ulose '
                                             '6-phosphate',
                                     'reason': 'Found 0 fatty acid ester '
                                               'group(s) after filtering; '
                                               'expected exactly 2.'}],
    'sample_false_negatives': [   {   'smiles': 'CCCCCCCCCCCCCCCC(=O)OCC(COP(O)(=O)OCC(O)COP(O)(O)=O)OC(=O)CCCCCCC\\C=C/CCCCCCCC',
                                      'name': '1-hexadecanoyl-2-[(Z)-octadec-9-enoyl]-sn-glycero-3-phospho-sn-glycerol '
                                              '3-phosphate',
                                      'reason': 'Could not find a single '
                                                'phosphate-derived glycerol '
                                                'carbon that connects with the '
                                                'two FA ester glycerol carbons '
                                                'within a graph distance of '
                                                '2.'},
                                  {   'smiles': 'CCCCC\\C=C/C\\C=C/C\\C=C/CCCCC(=O)OC[C@@H](O)COP(O)(O)=O',
                                      'name': '1-(gamma-linolenoyl)-sn-glycero-3-phosphate',
                                      'reason': 'Found 1 fatty acid ester '
                                                'group(s) after filtering; '
                                                'expected exactly 2.'},
                                  {   'smiles': 'P(OC[C@H](OC(=O)CCCCC/C=C\\C/C=C\\C/C=C\\CC)COC(=O)CCCCCCC/C=C\\C/C=C\\C/C=C\\CC)([O-])([O-])=O',
                                      'name': '18:3-16:3-PA',
                                      'reason': 'No phosphate group found with '
                                                '≥3 oxygen neighbors (all '
                                                'neutral) and exactly one '
                                                'oxygen attached to a carbon'},
                                  {   'smiles': 'O1C(C1)COC(=O)CCCC=CCC=CCC=CCC=CCCCCC',
                                      'name': 'O-Arachidonoyl Glycidol',
                                      'reason': 'No phosphate group found with '
                                                '≥3 oxygen neighbors (all '
                                                'neutral) and exactly one '
                                                'oxygen attached to a carbon'}],
    'attempt': 4,
    'reasoning': 'Below is our final Python solution. First, note that we '
                 're‐examined the previous work and noticed several potential '
                 'pitfalls. For example, the earlier code looked for a '
                 'phosphate P having ≥3 O neighbors and exactly one of these O '
                 'atoms attached to a carbon. Likewise, it detected fatty‐acid '
                 'ester groups via a strict “OC(=O)” SMARTS. However, many '
                 '“mis‐classifications” occurred because (a) many real PA '
                 'structures now are drawn in their protonated (neutral) form '
                 'while some “false‐positive” examples carry explicit negative '
                 'charges on the phosphate and (b) sometimes there can be more '
                 'than one candidate oxygen from the phosphate group. In this '
                 'version we (1) check that none of the atoms within the '
                 'phosphate “head” carry a negative formal charge (thus '
                 'eliminating some of the ionized false positives), (2) allow '
                 'for more than one candidate glycerol carbon from the '
                 'phosphate group by testing which one yields a contiguous '
                 'trio of carbons (the two fatty‐acid ester glycerol carbons '
                 'plus that candidate) and (3) use the “OC(=O)” SMARTS but '
                 'also filter out bridging oxygens attached to phosphorus. '
                 'With these improvements our function should better “hone in” '
                 'on the defined class. \n'
                 '\n'
                 'Below is the complete code in one Python block:',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 361,
    'num_false_positives': 48,
    'num_true_negatives': 141887,
    'num_false_negatives': 4,
    'num_negatives': None,
    'precision': 0.882640586797066,
    'recall': 0.989041095890411,
    'f1': 0.9328165374677004,
    'accuracy': 0.9996345748418833,
    'negative_predictive_value': 0.9999718093466111}