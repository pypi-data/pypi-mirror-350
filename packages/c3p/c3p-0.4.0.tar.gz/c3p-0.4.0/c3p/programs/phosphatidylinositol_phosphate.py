"""
Classifies: CHEBI:28765 phosphatidylinositol phosphate
"""
"""
Classifies: Phosphatidylinositol phosphate
A phosphatidylinositol phosphate (PIP, PIP2, PIP3, etc.) is a phosphoinositide that
contains a (myo-)inositol head group that is substituted by at least two phosphate groups:
one that links the inositol to the glycerol backbone and at least one extra phosphate
on the ring to distinguish it from plain phosphatidylinositol (PI). Additionally,
the molecule should contain at least two acyl chains (via ester bonds) and have a high
molecular weight.
"""

from rdkit import Chem
from rdkit.Chem import rdMolDescriptors

def is_phosphatidylinositol_phosphate(smiles: str):
    """
    Determines if a molecule is a phosphatidylinositol phosphate (PIP/PIP2/PIP3) based on its SMILES string.
    
    The classifier checks that:
      0. The molecule does not contain any negative formal charges.
      1. It contains a myo-inositol head group (based on the canonical inositol pattern).
      2. At least two distinct phosphorus atoms are directly attached to inositol (one being the linking phosphate
         which connects the inositol to a glycerol backbone, and at least one extra phosphate on the ring).
      3. At least one of the phosphate groups attached to the inositol shows “linking” behavior, meaning it is bound
         via an oxygen to a carbon atom that is not part of the inositol.
      4. The molecule contains at least two acyl ester groups (fatty acid chains attached via ester bonds) that are not
         part of any phosphate group.
      5. The molecular weight is above a lower threshold typical for these lipids.
    
    Args:
        smiles (str): SMILES string of the molecule.
    
    Returns:
        bool: True if the molecule is classified as a phosphatidylinositol phosphate, False otherwise.
        str: Reason for the classification decision.
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
    
    # 0. Reject molecules with any negative formal charges (to avoid deprotonated/salt forms).
    for atom in mol.GetAtoms():
        if atom.GetFormalCharge() < 0:
            return False, "Molecule has negative formal charges; likely drawn as a salt form"
    
    # 1. Locate the myo-inositol head group.
    # Use the canonical myo-inositol structure: OC1C(O)C(O)C(O)C(O)C1O
    inositol = Chem.MolFromSmiles("OC1C(O)C(O)C(O)C(O)C1O")
    inositol_matches = mol.GetSubstructMatches(inositol)
    if not inositol_matches:
        return False, "Inositol head group not found"
    # For our purposes, use the first matching fragment.
    inositol_atom_indices = set(inositol_matches[0])
    
    # 2. Collect all P atoms directly attached to any inositol oxygen.
    # We also record from which oxygen they are attached.
    p_attach = {}  # p_idx -> list of inositol oxygen indices that attach to it
    for idx in inositol_atom_indices:
        atom = mol.GetAtomWithIdx(idx)
        # Only consider oxygen atoms (the –OH groups on inositol)
        if atom.GetSymbol() != "O":
            continue
        for nbr in atom.GetNeighbors():
            if nbr.GetSymbol() == "P":
                p_idx = nbr.GetIdx()
                p_attach.setdefault(p_idx, []).append(idx)
    
    # For a PIP family member we expect at least two distinct phosphate groups on inositol:
    if len(p_attach) < 2:
        return False, "No extra phosphate substituent on the inositol head found (only %d phosphate group(s) attached)" % len(p_attach)
    
    # 3. For at least one of these phosphorus atoms, check for linking phosphate behavior.
    linking_found = False
    for p_idx, o_list in p_attach.items():
        p_atom = mol.GetAtomWithIdx(p_idx)
        # Look at all oxygen neighbors of this phosphorus.
        for o_neigh in p_atom.GetNeighbors():
            # Skip if this oxygen is one of the ones attached to the inositol.
            if o_neigh.GetIdx() in inositol_atom_indices:
                continue
            if o_neigh.GetSymbol() != "O":
                continue
            # Check if this oxygen is further bound to a carbon that is not part of the inositol.
            for second_neigh in o_neigh.GetNeighbors():
                if second_neigh.GetSymbol() == "C" and second_neigh.GetIdx() not in inositol_atom_indices:
                    linking_found = True
                    break
            if linking_found:
                break
        if linking_found:
            break

    if not linking_found:
        return False, "Linking phosphate connecting inositol to glycerol backbone not found"
    
    # 4. Count acyl ester groups.
    # We define acyl ester groups as an oxygen (not involved in any phosphate) bridging a carbonyl group.
    acyl_count = 0
    seen_ester_bonds = set()
    for bond in mol.GetBonds():
        if bond.GetBondType() != Chem.BondType.SINGLE:
            continue
        a1 = bond.GetBeginAtom()
        a2 = bond.GetEndAtom()
        # Identify candidate pair: one atom must be oxygen and the other carbon.
        if a1.GetSymbol() == "O" and a2.GetSymbol() == "C":
            oxygen = a1
            carbon = a2
        elif a2.GetSymbol() == "O" and a1.GetSymbol() == "C":
            oxygen = a2
            carbon = a1
        else:
            continue
        
        # Exclude oxygen if it is bonded to any phosphorus (likely part of a phosphate group).
        if any(nb.GetSymbol() == "P" for nb in oxygen.GetNeighbors()):
            continue
        
        # Confirm that the carbon is part of a carbonyl (has a double bond to an oxygen aside from the ester oxygen).
        carbonyl_found = False
        for nbr in carbon.GetNeighbors():
            if nbr.GetIdx() == oxygen.GetIdx():
                continue
            if nbr.GetSymbol() != "O":
                continue
            bond_co = mol.GetBondBetweenAtoms(carbon.GetIdx(), nbr.GetIdx())
            if bond_co is not None and bond_co.GetBondType() == Chem.BondType.DOUBLE:
                carbonyl_found = True
                break
        if carbonyl_found:
            bond_id = tuple(sorted([oxygen.GetIdx(), carbon.GetIdx()]))
            if bond_id not in seen_ester_bonds:
                seen_ester_bonds.add(bond_id)
                acyl_count += 1

    if acyl_count < 2:
        return False, "Found only %d acyl ester group(s); need at least 2" % acyl_count

    # 5. Check molecular weight (typically these lipids have a high molecular weight).
    mw = rdMolDescriptors.CalcExactMolWt(mol)
    if mw < 500:
        return False, "Molecular weight too low (%.1f Da) for a phosphatidylinositol phosphate" % mw

    return True, "Molecule contains a phosphorylated inositol head (with linking and extra phosphate), and at least two acyl chains"


# Example usage (for testing):
if __name__ == "__main__":
    # Test with a known example: 1,2-dioctanoyl-sn-glycero-3-phospho-(1D-myo-inositol-3,4-bisphosphate)
    test_smiles = "CCCCCCCC(=O)OC[C@H](COP(O)(=O)O[C@H]1[C@H](O)[C@@H](O)[C@H](OP(O)(O)=O)[C@@H](OP(O)(O)=O)[C@H]1O)OC(=O)CCCCCCCC"
    result, reason = is_phosphatidylinositol_phosphate(test_smiles)
    print(result, reason)


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:28765',
                          'name': 'phosphatidylinositol phosphate',
                          'definition': 'Any member of the phosphoinositide '
                                        'family of compounds, of which seven '
                                        'occur naturally.',
                          'parents': ['CHEBI:18179'],
                          'xrefs': ['PMID:16441841', 'PMID:2538726'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 118,
                           'log_lines_of_code': 4.770684624465665,
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
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 2,
                                                 3,
                                                 4,
                                                 4,
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
                                                 2,
                                                 3,
                                                 3,
                                                 4,
                                                 3,
                                                 4,
                                                 3,
                                                 3,
                                                 4,
                                                 5,
                                                 5,
                                                 3,
                                                 4,
                                                 2,
                                                 3,
                                                 0,
                                                 1,
                                                 2,
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
                                                 2,
                                                 2,
                                                 3,
                                                 3,
                                                 2,
                                                 3,
                                                 3,
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
                                                 3,
                                                 4,
                                                 3,
                                                 3,
                                                 4,
                                                 4,
                                                 2,
                                                 3,
                                                 3,
                                                 4,
                                                 4,
                                                 0,
                                                 1,
                                                 2,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 0,
                                                 1,
                                                 0,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 1],
                           'max_indent': 5,
                           'imports': [   'from rdkit import Chem',
                                          'from rdkit.Chem import '
                                          'rdMolDescriptors'],
                           'imports_count': 2,
                           'methods_called': [   'CalcExactMolWt',
                                                 'GetSymbol',
                                                 'GetIdx',
                                                 'MolFromSmiles',
                                                 'GetAtomWithIdx',
                                                 'GetSubstructMatches',
                                                 'GetAtoms',
                                                 'GetBonds',
                                                 'GetBeginAtom',
                                                 'GetBondBetweenAtoms',
                                                 'GetNeighbors',
                                                 'append',
                                                 'setdefault',
                                                 'items',
                                                 'GetBondType',
                                                 'add',
                                                 'GetFormalCharge',
                                                 'GetEndAtom'],
                           'methods_called_count': 18,
                           'smarts_strings': [],
                           'smarts_strings_count': 0,
                           'defs': [   'is_phosphatidylinositol_phosphate(smiles: '
                                       'str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "Molecule has negative '
                                          'formal charges; likely drawn as a '
                                          'salt form"',
                                          'False, "Inositol head group not '
                                          'found"',
                                          'False, "No extra phosphate '
                                          'substituent on the inositol head '
                                          'found (only %d phosphate group(s) '
                                          'attached)" % len(p_attach)',
                                          'False, "Linking phosphate '
                                          'connecting inositol to glycerol '
                                          'backbone not found"',
                                          'False, "Found only %d acyl ester '
                                          'group(s); need at least 2" % '
                                          'acyl_count',
                                          'False, "Molecular weight too low '
                                          '(%.1f Da) for a '
                                          'phosphatidylinositol phosphate" % '
                                          'mw',
                                          'True, "Molecule contains a '
                                          'phosphorylated inositol head (with '
                                          'linking and extra phosphate), and '
                                          'at least two acyl chains"'],
                           'returns_count': 8,
                           'complexity': 7.354136924893133},
    'message': '\n'
               'Attempt failed: F1 score of 0.7761194029850746 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: '
               'CCCCCCCC(=O)OC[C@H](COP(O)(=O)O[C@H]1[C@H](O)[C@@H](O)[C@H](OP(O)(O)=O)[C@@H](OP(O)(O)=O)[C@H]1O)OC(=O)CCCCCCC '
               'NAME: '
               '1,2-dioctanoyl-sn-glycero-3-phospho-(1D-myo-inositol-3,4-bisphosphate) '
               'REASON: CORRECT Molecule contains a phosphorylated inositol '
               'head (with linking and extra phosphate), and at least two acyl '
               'chains\n'
               ' * SMILES: '
               'CCCCCCCC(=O)OC[C@H](COP(O)(=O)O[C@H]1[C@H](O)[C@@H](OP(O)(O)=O)[C@H](O)[C@@H](OP(O)(O)=O)[C@H]1O)OC(=O)CCCCCCC '
               'NAME: '
               '1,2-dioctanoyl-sn-glycero-3-phospho-(1D-myo-inositol-3,5-bisphosphate) '
               'REASON: CORRECT Molecule contains a phosphorylated inositol '
               'head (with linking and extra phosphate), and at least two acyl '
               'chains\n'
               ' * SMILES: '
               '[C@@H]1(C(C(C([C@H](C1O)OP(=O)(O)O)OP(=O)(O)O)O)O)OP(OC[C@@](COC(CCCCCCCCCCCCCCC)=O)(OC(CCCCCCCCCCCCCCCCC)=O)[H])(O)=O '
               "NAME: PIP2[3',4'](16:0/18:0) REASON: CORRECT Molecule contains "
               'a phosphorylated inositol head (with linking and extra '
               'phosphate), and at least two acyl chains\n'
               ' * SMILES: '
               'P(O[C@@H]1C(O)[C@H](OP(O)(O)=O)C(OP(O)(O)=O)C(O)C1O)(OC[C@H](OC(=O)CCCCCCC/C=C\\C/C=C\\CCCCC)COC(=O)CCCCCCC/C=C\\C/C=C\\CCCCC)(O)=O '
               'NAME: PIP2(18:2/18:2) REASON: CORRECT Molecule contains a '
               'phosphorylated inositol head (with linking and extra '
               'phosphate), and at least two acyl chains\n'
               ' * SMILES: '
               'CCCCCCCC(=O)OC[C@H](COP(O)(=O)O[C@H]1[C@H](O)[C@@H](O)[C@H](O)[C@@H](OP(O)(O)=O)[C@H]1O)OC(=O)CCCCCCC '
               'NAME: '
               "1,2-dioctanoyl-sn-glycero-3-phospho-(1D-myo-inositol-3'-phosphate) "
               'REASON: CORRECT Molecule contains a phosphorylated inositol '
               'head (with linking and extra phosphate), and at least two acyl '
               'chains\n'
               ' * SMILES: '
               'CCCCCCCC(=O)OC[C@H](COP(O)(=O)O[C@@H]1[C@H](O)[C@H](O)[C@@H](O)[C@H](OP(O)(O)=O)[C@H]1O)OC(=O)CCCCCCC '
               'NAME: '
               "1,2-dioctanoyl-sn-glycero-3-phospho-(1'-myo-inositol-5'-phosphate) "
               'REASON: CORRECT Molecule contains a phosphorylated inositol '
               'head (with linking and extra phosphate), and at least two acyl '
               'chains\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCC(=O)OC[C@H](COP(O)(=O)O[C@@H]1[C@H](O)[C@H](O)[C@@H](O)[C@H](OP(O)(O)=O)[C@H]1O)OC(=O)CCCCCCC\\C=C/CCCCCCCC '
               'NAME: 1-stearoyl-2-oleoyl-sn-glycero-3-phospho-1D-myo-inositol '
               '5-phosphate REASON: CORRECT Molecule contains a phosphorylated '
               'inositol head (with linking and extra phosphate), and at least '
               'two acyl chains\n'
               ' * SMILES: '
               'CCCCC\\C=C/C\\C=C/CCCCCCCC(=O)OC[C@H](COP(O)(=O)O[C@@H]1[C@H](O)[C@H](O)[C@@H](O)[C@H](OP(O)(O)=O)[C@H]1O)OC(=O)CCCCCCC\\C=C/C\\C=C/CCCCC '
               'NAME: 1,2-dilinoleoyl-sn-glycero-3-phospho-1D-myo-inositol '
               '5-phosphate REASON: CORRECT Molecule contains a phosphorylated '
               'inositol head (with linking and extra phosphate), and at least '
               'two acyl chains\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCC(=O)OC[C@H](COP(O)(=O)O[C@H]1[C@H](O)[C@@H](O)[C@H](O)[C@@H](OP(O)(O)=O)[C@H]1O)OC(=O)CCCCCCCCCCCCCCC '
               'NAME: '
               "1,2-dipalmitoyl-sn-glycero-3-phospho-(1'D-myo-inositol-3'-phosphate) "
               'REASON: CORRECT Molecule contains a phosphorylated inositol '
               'head (with linking and extra phosphate), and at least two acyl '
               'chains\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCC(=O)OC[C@H](COP(O)(=O)O[C@H]1[C@H](O)[C@@H](O)[C@H](OP(O)(O)=O)[C@@H](OP(O)(O)=O)[C@H]1O)OC(=O)CCCCCCCCCCCCCCC '
               'NAME: '
               '1,2-dihexadecanoyl-sn-glycero-3-phospho-(1D-myo-inositol-3,4-bisphosphate) '
               'REASON: CORRECT Molecule contains a phosphorylated inositol '
               'head (with linking and extra phosphate), and at least two acyl '
               'chains\n'
               ' * SMILES: '
               'CCCCCCCC(=O)OC[C@H](COP(O)(=O)O[C@@H]1[C@H](O)[C@H](OP(O)(O)=O)[C@@H](OP(O)(O)=O)[C@H](OP(O)(O)=O)[C@H]1O)OC(=O)CCCCCCC '
               'NAME: '
               '1,2-dioctanoyl-sn-glycero-3-phospho-(1D-myo-inositol-3,4,5-trisphosphate) '
               'REASON: CORRECT Molecule contains a phosphorylated inositol '
               'head (with linking and extra phosphate), and at least two acyl '
               'chains\n'
               ' * SMILES: '
               '[C@@H]1(C(C(C([C@H](C1O)OP(=O)(O)O)O)O)O)OP(OC[C@](COC(CCCCCCCCCCCCCCCCC)=O)([H])OC(CCCCCCCCCCCCCCC)=O)(O)=O '
               'NAME: PIP(18:0/16:0) REASON: CORRECT Molecule contains a '
               'phosphorylated inositol head (with linking and extra '
               'phosphate), and at least two acyl chains\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCC(=O)OC[C@H](COP(O)(=O)O[C@@H]1[C@H](O)[C@H](O)[C@@H](OP(O)(O)=O)[C@H](O)[C@H]1O)OC(=O)CCCCCCCCCCCCCCC '
               'NAME: '
               '1,2-dihexadecanoyl-sn-glycero-3-phospho-(1D-myo-inositol-4-phosphate) '
               'REASON: CORRECT Molecule contains a phosphorylated inositol '
               'head (with linking and extra phosphate), and at least two acyl '
               'chains\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCC(=O)OC[C@H](COP(O)(=O)O[C@@H]1[C@H](O)[C@H](OP(O)(O)=O)[C@@H](OP(O)(O)=O)[C@H](OP(O)(O)=O)[C@H]1O)OC(=O)CCC\\C=C/C\\C=C/C\\C=C/C\\C=C/CCCCC '
               'NAME: '
               '1-stearoyl-2-arachidonoyl-sn-glycero-3-phospho-(1D-myo-inositol '
               '3,4,5-triphosphate) REASON: CORRECT Molecule contains a '
               'phosphorylated inositol head (with linking and extra '
               'phosphate), and at least two acyl chains\n'
               ' * SMILES: '
               'CCCCCCCC(=O)OC[C@H](COP(O)(=O)O[C@@H]1[C@H](O)[C@H](O)[C@@H](OP(O)(O)=O)[C@H](OP(O)(O)=O)[C@H]1O)OC(=O)CCCCCCC '
               'NAME: '
               '1,2-dioctanoyl-sn-glycero-3-phospho-(1D-myo-inositol-4,5-bisphosphate) '
               'REASON: CORRECT Molecule contains a phosphorylated inositol '
               'head (with linking and extra phosphate), and at least two acyl '
               'chains\n'
               ' * SMILES: '
               '[C@@H]1([C@@H]([C@@H]([C@@H]([C@H]([C@@H]1O)OP(O)(=O)O)O)O)OP(OC[C@@H](COC(=O)CCCCCCC)OC(=O)CCCCCCC)(=O)O)O '
               'NAME: '
               '1,2-dioctanoyl-sn-glycero-3-phospho-(1D-myo-inositol-4-phosphate) '
               'REASON: CORRECT Molecule contains a phosphorylated inositol '
               'head (with linking and extra phosphate), and at least two acyl '
               'chains\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCC(=O)OC[C@H](COP(O)(=O)O[C@@H]1[C@H](O)[C@H](O)[C@@H](OP(O)(O)=O)[C@H](OP(O)(O)=O)[C@H]1O)OC(=O)CCCCCCCCCCCCCCC '
               'NAME: '
               '1,2-dihexadecanoyl-sn-glycero-3-phospho-(1D-myo-inositol-4,5-bisphosphate) '
               'REASON: CORRECT Molecule contains a phosphorylated inositol '
               'head (with linking and extra phosphate), and at least two acyl '
               'chains\n'
               ' * SMILES: '
               'O(C[C@](COP(O)(=O)O[C@H]1C(C(C([C@H](C1O)OP(=O)(O)O)O)O)O)(OC(CCC/C=C\\C/C=C\\C/C=C\\C/C=C\\CCCCC)=O)[H])C(CCCCCCCCC/C=C\\CCCCCC)=O '
               'NAME: PIP(18:1(11Z)/20:4(5Z,8Z,11Z,14Z)) REASON: CORRECT '
               'Molecule contains a phosphorylated inositol head (with linking '
               'and extra phosphate), and at least two acyl chains\n'
               ' * SMILES: '
               'P(O[C@@H]1C(O)[C@H](OP(O)(O)=O)C(OP(O)(O)=O)C(O)C1O)(OC[C@H](OC(=O)CCCCCCCCCCCCCCC)COC(=O)CCCCCCCCCCCCCCC)(O)=O '
               'NAME: PIP2(16:0/16:0) REASON: CORRECT Molecule contains a '
               'phosphorylated inositol head (with linking and extra '
               'phosphate), and at least two acyl chains\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCC(=O)OC[C@H](COP(O)(=O)O[C@@H]1[C@H](O)[C@H](O)[C@@H](O)[C@H](OP(O)(O)=O)[C@H]1O)OC(=O)CCC\\C=C/C\\C=C/C\\C=C/C\\C=C/CCCCC '
               'NAME: '
               '1-stearoyl-2-arachidonoyl-sn-glycero-3-phospho-1D-myo-inositol '
               '5-phosphate REASON: CORRECT Molecule contains a phosphorylated '
               'inositol head (with linking and extra phosphate), and at least '
               'two acyl chains\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCC(=O)OC[C@H](COP(O)(=O)O[C@@H]1[C@H](O)[C@H](O)[C@@H](OP(O)(O)=O)[C@H](OP(O)(O)=O)[C@H]1O)OC(=O)CCC\\C=C/C\\C=C/C\\C=C/C\\C=C/CCCCC '
               'NAME: '
               '1-stearoyl-2-arachidonoyl-sn-glycero-3-phospho-1D-myo-inositol '
               '4,5-biphosphate REASON: CORRECT Molecule contains a '
               'phosphorylated inositol head (with linking and extra '
               'phosphate), and at least two acyl chains\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCC(=O)OC[C@H](COP(O)(=O)O[C@@H]1[C@H](O)[C@H](O)[C@@H](OP(O)(O)=O)[C@H](O)[C@H]1O)OC(=O)CCCCCCC\\C=C/CCCCCCCC '
               'NAME: 1-stearoyl-2-oleoyl-sn-glycero-3-phospho-1D-myo-inositol '
               '4-phosphate REASON: CORRECT Molecule contains a phosphorylated '
               'inositol head (with linking and extra phosphate), and at least '
               'two acyl chains\n'
               ' * SMILES: '
               'O=C(CCC/C=C\\C/C=C\\C/C=C\\C/C=C\\CCCCC)O[C@@H](COP(O[C@H]1[C@@H]([C@H]([C@@H]([C@H]([C@H]1O)O)OP(O)(=O)O)O)O)(=O)O)COC(=O)CCCCCCCCCCCCCCCCC '
               'NAME: '
               '1-stearoyl-2-arachidonoyl-sn-glycero-3-phospho-1D-myo-inositol '
               '4-phosphate REASON: CORRECT Molecule contains a phosphorylated '
               'inositol head (with linking and extra phosphate), and at least '
               'two acyl chains\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCC(=O)OC[C@H](COP(O)(=O)O[C@@H]1[C@H](O)[C@H](OP(O)(O)=O)[C@@H](OP(O)(O)=O)[C@H](OP(O)(O)=O)[C@H]1O)OC(=O)CCCCCCCCCCCCCCC '
               'NAME: '
               '1,2-dihexadecanoyl-sn-glycero-3-phospho-(1D-myo-inositol-3,4,5-trisphosphate) '
               'REASON: CORRECT Molecule contains a phosphorylated inositol '
               'head (with linking and extra phosphate), and at least two acyl '
               'chains\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCC(=O)OC[C@H](COP(O)(=O)O[C@@H]1[C@H](O)[C@H](O)[C@@H](O)[C@H](OP(O)(O)=O)[C@H]1O)OC(=O)CCCCCCCCCCCCCCC '
               'NAME: '
               '1,2-dipalmitoyl-sn-glycero-3-phospho-(1D-myo-inositol-5-phosphate) '
               'REASON: CORRECT Molecule contains a phosphorylated inositol '
               'head (with linking and extra phosphate), and at least two acyl '
               'chains\n'
               'False positives: SMILES: '
               'P(O[C@@H]1C(O)[C@H](OP(O)(O)=O)C(O)C(O)C1O)(OC[C@H](OC(=O)CCCCCCCCCCCCCCC)COC(=O)CCCCCCC/C=C\\CCCCCC)(O)=O '
               'NAME: PIP(16:1(9Z)/18:0) REASON: WRONGLY CLASSIFIED Molecule '
               'contains a phosphorylated inositol head (with linking and '
               'extra phosphate), and at least two acyl chains\n'
               ' * SMILES: '
               'P(O[C@@H]1C(O)[C@H](OP(O)(O)=O)C(O)C(O)C1O)(OC[C@H](OC(=O)CCCCCCCCCCCCCCCCC)COC(=O)CCCCCCCCC/C=C\\CCCCCC)(O)=O '
               'NAME: PIP(18:1(11Z)/18:0) REASON: WRONGLY CLASSIFIED Molecule '
               'contains a phosphorylated inositol head (with linking and '
               'extra phosphate), and at least two acyl chains\n'
               ' * SMILES: '
               'P(O[C@@H]1C(O)[C@H](OP(O)(O)=O)C(O)C(O)C1O)(OC[C@H](OC(=O)CCCCCCC/C=C\\CCCCCCCC)COC(=O)CCCCCCCCCCCCCCCCC)(O)=O '
               'NAME: '
               '{[(1R,5S)-2,3,4,6-tetrahydroxy-5-({hydroxy[(2R)-2-[(9Z)-octadec-9-enoyloxy]-3-(octadecanoyloxy)propoxy]phosphoryl}oxy)cyclohexyl]oxy}phosphonic '
               'acid REASON: WRONGLY CLASSIFIED Molecule contains a '
               'phosphorylated inositol head (with linking and extra '
               'phosphate), and at least two acyl chains\n'
               ' * SMILES: '
               'P(O[C@@H]1C(O)[C@H](OP(O)(O)=O)C(O)C(O)C1O)(OC[C@H](OC(=O)CCCCCCCCC/C=C\\CCCCCCCC)COC(=O)CCCCCCC/C=C\\C/C=C\\CCCCC)(O)=O '
               'NAME: '
               '{[(1R,5S)-2,3,4,6-tetrahydroxy-5-({hydroxy[(2R)-2-[(11Z)-icos-11-enoyloxy]-3-[(9Z,12Z)-octadeca-9,12-dienoyloxy]propoxy]phosphoryl}oxy)cyclohexyl]oxy}phosphonic '
               'acid REASON: WRONGLY CLASSIFIED Molecule contains a '
               'phosphorylated inositol head (with linking and extra '
               'phosphate), and at least two acyl chains\n'
               ' * SMILES: '
               'P(O[C@@H]1C(O)[C@H](OP(O)(O)=O)C(O)C(O)C1O)(OC[C@H](OC(=O)CCCCCCCCC/C=C\\C/C=C\\CCCCC)COC(=O)CCCCCCCCCCCCCCC)(O)=O '
               'NAME: PIP(16:0/20:2(11Z,14Z)) REASON: WRONGLY CLASSIFIED '
               'Molecule contains a phosphorylated inositol head (with linking '
               'and extra phosphate), and at least two acyl chains\n'
               ' * SMILES: '
               'P(O[C@@H]1C(O)[C@H](OP(O)(O)=O)C(O)C(O)C1O)(OC[C@H](OC(=O)CCCCCCCCCCC/C=C\\C/C=C\\CCCCC)COC(=O)CCCCCCCCCCCCCCC)(O)=O '
               'NAME: PIP(16:0/22:2(13Z,16Z)) REASON: WRONGLY CLASSIFIED '
               'Molecule contains a phosphorylated inositol head (with linking '
               'and extra phosphate), and at least two acyl chains\n'
               ' * SMILES: '
               'P(O[C@@H]1C(O)[C@H](OP(O)(O)=O)C(O)C(O)C1O)(OC[C@H](OC(=O)CCCCCCC/C=C\\C/C=C\\C/C=C\\CC)COC(=O)CCCCCCCCCCCCCCCCC)(O)=O '
               'NAME: PIP(18:0/18:3(9Z,12Z,15Z)) REASON: WRONGLY CLASSIFIED '
               'Molecule contains a phosphorylated inositol head (with linking '
               'and extra phosphate), and at least two acyl chains\n'
               ' * SMILES: '
               'P(O[C@@H]1C(O)[C@H](OP(O)(O)=O)C(O)C(O)C1O)(OC[C@H](OC(=O)CCCCCCCCCCCCCCC)COC(=O)CCCCCCC/C=C\\C/C=C\\CCCCC)(O)=O '
               'NAME: '
               '{[(1R,3S)-3-({[(2R)-2-(hexadecanoyloxy)-3-[(9Z,12Z)-octadeca-9,12-dienoyloxy]propoxy](hydroxy)phosphoryl}oxy)-2,4,5,6-tetrahydroxycyclohexyl]oxy}phosphonic '
               'acid REASON: WRONGLY CLASSIFIED Molecule contains a '
               'phosphorylated inositol head (with linking and extra '
               'phosphate), and at least two acyl chains\n'
               ' * SMILES: '
               'P(O[C@@H]1C(O)[C@H](OP(O)(O)=O)C(O)C(O)C1O)(OC[C@H](OC(=O)CCC/C=C\\C/C=C\\C/C=C\\C/C=C\\CCCCC)COC(=O)CCCCCCCCCCCCCCCC)(O)=O '
               "NAME: PIP[3'](17:0/20:4(5Z,8Z,11Z,14Z)) REASON: WRONGLY "
               'CLASSIFIED Molecule contains a phosphorylated inositol head '
               '(with linking and extra phosphate), and at least two acyl '
               'chains\n'
               ' * SMILES: '
               'P(O[C@@H]1C(O)[C@H](OP(O)(O)=O)C(O)C(O)C1O)(OC[C@H](OC(=O)CCCCCCC/C=C\\CCCCCC)COC(=O)CCCCCCC/C=C\\CCCCCC)(O)=O '
               'NAME: PIP(16:1(9Z)/16:1(9Z)) REASON: WRONGLY CLASSIFIED '
               'Molecule contains a phosphorylated inositol head (with linking '
               'and extra phosphate), and at least two acyl chains\n'
               ' * SMILES: '
               'P(OC1C(O)C(OP(O)(O)=O)C(O)C(O)C1O)(OCC(OC(=O)CCCCC)COC(=O)CCCCC)(O)=O '
               'NAME: 1-(1,2-dihexanoylphosphatidyl)inositol-5-phosphate '
               'REASON: WRONGLY CLASSIFIED Molecule contains a phosphorylated '
               'inositol head (with linking and extra phosphate), and at least '
               'two acyl chains\n'
               ' * SMILES: '
               'P(O[C@@H]1C(O)[C@H](OP(O)(O)=O)C(O)C(O)C1O)(OC[C@H](OC(=O)CCCCCCCCC/C=C\\CCCCCC)COC(=O)CCCCCCCCCCCCCCCCC)(O)=O '
               'NAME: PIP(18:0/18:1(11Z)) REASON: WRONGLY CLASSIFIED Molecule '
               'contains a phosphorylated inositol head (with linking and '
               'extra phosphate), and at least two acyl chains\n'
               ' * SMILES: '
               'P(O[C@@H]1C(O)[C@H](OP(O)(O)=O)C(O)C(O)C1O)(OC[C@H](OC(=O)CCCCCCC/C=C\\C/C=C\\CCCCC)COC(=O)CCCCCCCCCCCCCCCCC)(O)=O '
               'NAME: '
               '{[(1R,5S)-2,3,4,6-tetrahydroxy-5-({hydroxy[(2R)-2-[(9Z,12Z)-octadeca-9,12-dienoyloxy]-3-(octadecanoyloxy)propoxy]phosphoryl}oxy)cyclohexyl]oxy}phosphonic '
               'acid REASON: WRONGLY CLASSIFIED Molecule contains a '
               'phosphorylated inositol head (with linking and extra '
               'phosphate), and at least two acyl chains\n'
               ' * SMILES: '
               'P(OC1C(O)C(O)C(OP(O)(O)=O)[C@@H](O)C1O)(OC[C@H](OC(=O)CCC/C=C\\C/C=C\\C/C=C\\C/C=C\\CCCCC)COC(=O)CCCCCCCCCCCCCCCC)(O)=O '
               "NAME: PIP[4'](17:0/20:4(5Z,8Z,11Z,14Z)) REASON: WRONGLY "
               'CLASSIFIED Molecule contains a phosphorylated inositol head '
               '(with linking and extra phosphate), and at least two acyl '
               'chains\n'
               'False negatives: SMILES: '
               '[C@@H]1([C@@H]([C@@H](O)[C@H]([C@H]([C@@H]1O)OP(=O)(OCOC(=O)CCC)OCOC(=O)CCC)O)OP(=O)(OCOC(=O)CCC)OCOC(=O)CCC)OP(=O)(OCOC(=O)CCC)OCOC(=O)CCC '
               'NAME: D-myo-Ins(1,4,5)P3 hexakis(butyryloxymethyl) ester '
               'REASON: MISSED No extra phosphate substituent on the inositol '
               'head found; likely a plain PI rather than PIP/PIP2/PIP3\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'O=C(N[C@@H](C(O)(C)C)C)[C@H]([C@@]1([C@@]2([C@@](CC1)(/C(/CCC2)=C/C=C\\3/C[C@@H](O)C[C@H](O)C3=C)[H])C)[H])C',
                                     'name': '1alpha,25-dihydroxy-24-oxo-23-azavitamin '
                                             'D2 / '
                                             '1alpha,25-dihydroxy-24-oxo-23-azaergocalciferol',
                                     'reason': 'Inositol head group not found'},
                                 {   'smiles': 'CCCCCCCCCCCCCCCCCCC(O)C([O-])=O',
                                     'name': '2-hydroxyarachidate',
                                     'reason': 'Molecule has negative formal '
                                               'charges; likely drawn as a '
                                               'salt form'},
                                 {   'smiles': 'C[C@@H](CN([C@@H](C)CO)C(=O)NC1=CC=C(C=C1)C(F)(F)F)[C@@H](CN(C)C(=O)C2CCOCC2)OC',
                                     'name': 'N-[(2S,3S)-4-[[(2S)-1-hydroxypropan-2-yl]-[[4-(trifluoromethyl)phenyl]carbamoyl]amino]-2-methoxy-3-methylbutyl]-N-methyloxane-4-carboxamide',
                                     'reason': 'Inositol head group not found'},
                                 {   'smiles': 'CC(=O)CC\\C=C(/C)CCC=C(C)C',
                                     'name': 'geranyl acetone',
                                     'reason': 'Inositol head group not found'},
                                 {   'smiles': 'O([C@H]1[C@H](O)[C@H](O[C@H](O)[C@H]1O)CO[C@H]2O[C@@H]([C@@H](O)[C@H](O)[C@@H]2O)CO)[C@H]3O[C@@H]([C@@H](O)[C@H](O)[C@@H]3O[C@H]4O[C@@H]([C@@H](O)[C@H](O)[C@@H]4O)CO)CO',
                                     'name': '(2S,3S,4S,5S,6R)-2-[[(2R,3R,4S,5S,6S)-4-[(2R,3S,4S,5S,6R)-4,5-Dihydroxy-6-(hydroxymethyl)-3-[(2R,3S,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-3,5,6-trihydroxyoxan-2-yl]methoxy]-6-(hydroxymethyl)oxane-3,4,5-triol',
                                     'reason': 'Inositol head group not found'},
                                 {   'smiles': 'O=C(OC1=C(C(O)=C(C(=O)O)C(=C1C)C)C)C2=C(OC)C(=C(OC(=O)C3=C(O)C=C(O)C=C3C)C=C2C)C',
                                     'name': 'Thielavin Z5',
                                     'reason': 'Inositol head group not found'},
                                 {   'smiles': '[C@@H]1([C@@H]([C@H]([C@@H]([C@H](O1)CO)O)O)NC(C)=O)O[C@@H]2[C@@H]([C@H](C(O[C@@H]2CO)O)O)O',
                                     'name': 'beta-D-GlcpNAc-(1->4)-D-Galp',
                                     'reason': 'Inositol head group not found'},
                                 {   'smiles': 'CN(C)C(=O)C1=CC=C(C=C1)C2=CC=C(C=C2)[C@@H]3[C@H]4CN(CC(=O)N4[C@H]3CO)C(=O)CC5CC5',
                                     'name': '4-[4-[(6S,7R,8R)-4-(2-cyclopropyl-1-oxoethyl)-8-(hydroxymethyl)-2-oxo-1,4-diazabicyclo[4.2.0]octan-7-yl]phenyl]-N,N-dimethylbenzamide',
                                     'reason': 'Inositol head group not found'},
                                 {   'smiles': 'CCCCCCCCCCCCCCCCCCCCC=C',
                                     'name': '1-docosene',
                                     'reason': 'Inositol head group not found'},
                                 {   'smiles': 'C([C@@](OC(=O)CCC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)([H])COC(=O)CC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)OC(=O)CCCCC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC',
                                     'name': 'TG(22:5(7Z,10Z,13Z,16Z,19Z)/20:5(5Z,8Z,11Z,14Z,17Z)/22:6(4Z,7Z,10Z,13Z,16Z,19Z))[iso6]',
                                     'reason': 'Inositol head group not '
                                               'found'}],
    'sample_false_negatives': [],
    'attempt': 4,
    'reasoning': 'Below is one possible solution. In our reasoning we noticed '
                 'that the previous classifier tried to tell “extra‐phosphate” '
                 'from the “linking phosphate” by “inspecting each inositol '
                 'oxygen’s P neighbour.” However, some true PIP/PIP2/PIP3 '
                 'molecules (including protected derivatives) were rejected '
                 'because only one of the phosphate groups was recognized. To '
                 'improve matters we instead (1) first locate a canonical '
                 'myo‐inositol head group, (2) then collect all phosphorus '
                 'atoms directly bound to any of its –OH’s, and (3) require '
                 'that at least two distinct phosphorous atoms are attached to '
                 'inositol (one of which we assume is the linking phosphate '
                 'and at least one extra phosphate is present). In addition, '
                 'we re‐examine each phosphate attached to inositol to see '
                 'whether at least one of its non‐inositol oxygen neighbours '
                 '“leads out” (i.e. is bound to a carbon atom not in the '
                 'inositol fragment) so we can be more confident that a '
                 'phosphate is indeed bridging to the glycerol backbone. '
                 'Finally we check that at least two acyl ester groups '
                 '(typically from the two fatty acid chains) are present and '
                 'that the molecular weight is high enough. (Our hypothesis is '
                 'that by “counting” the number of different phosphorus atoms '
                 'at the inositol head (and checking one of them shows '
                 'linking) we avoid false positives [plain PI may only have '
                 'one phosphate] and catch even some protected phosphates.) \n'
                 '\n'
                 'Below is the complete code in one Python block:\n'
                 '\n'
                 '------------------------------------------------',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 27,
    'num_false_positives': 14,
    'num_true_negatives': 142259,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.6585365853658537,
    'recall': 1.0,
    'f1': 0.7941176470588235,
    'accuracy': 0.999901616303584,
    'negative_predictive_value': 1.0}