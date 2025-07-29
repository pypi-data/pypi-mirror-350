"""
Classifies: CHEBI:17855 triglyceride
"""
#!/usr/bin/env python
"""
Classifies: Triglycerides – any glyceride resulting from the condensation of all three hydroxy groups
of glycerol (propane-1,2,3-triol) with fatty acids.
The function is_triglyceride(smiles: str) returns a tuple (bool, str) indicating if the molecule is a triglyceride and why.
"""

from rdkit import Chem

def is_triglyceride(smiles: str):
    """
    Determines if a molecule is a triglyceride based on its SMILES string.
    A triglyceride is defined as a glyceride formed by the condensation of all three hydroxy groups 
    of glycerol with fatty acids. In our heuristic:
      - The molecule must be valid.
      - It should contain only C, H and O atoms.
      - It must contain a glycerol backbone (a consecutive three-carbon chain, i.e. CH2-CH-CH2)
        where each carbon is esterified (has a single oxygen attached that in turn is connected to a carbonyl).
    
    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a triglyceride, False otherwise.
        str: Reason for classification.
    """
    # Parse the SMILES string into an RDKit molecule.
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
    
    # Check that the molecule has only expected atoms: C, H and O.
    # (Triglycerides are composed only of C, H, and O. The presence of others implies a different class.)
    allowed_atomic_nums = {1, 6, 8}
    for atom in mol.GetAtoms():
        if atom.GetAtomicNum() not in allowed_atomic_nums:
            return False, f"Contains atom {atom.GetSymbol()}, not expected in a simple triglyceride"
    
    # Look for a glycerol backbone.
    # We use a simple SMARTS: a chain of three carbons: [CH2][CH][CH2]
    glycerol_smarts = "[CH2][CH][CH2]"
    glycerol_pattern = Chem.MolFromSmarts(glycerol_smarts)
    matches = mol.GetSubstructMatches(glycerol_pattern)
    if not matches:
        return False, "Glycerol backbone (CH2–CH–CH2) not found"
    
    # For each match of the glycerol backbone, check that exactly one ester bond emanates from each carbon.
    # An ester bond here is defined as a bond from a glycerol carbon (C) to an oxygen (O) that 
    # is further connected to a carbonyl carbon (a carbon with a double-bonded oxygen).
    def is_ester_oxygen(oxygen_atom, parent_index):
        # oxygen_atom should be connected to a carbon (the acyl carbon) that has a double-bonded O
        for neighbor in oxygen_atom.GetNeighbors():
            # Exclude the glycerol C from which we came.
            if neighbor.GetIdx() == parent_index:
                continue
            if neighbor.GetAtomicNum() == 6:  # carbon
                # Check if this carbon has at least one double bond to oxygen.
                for bond in neighbor.GetBonds():
                    if bond.GetBondTypeAsDouble() == 2.0:
                        nbr = bond.GetOtherAtom(neighbor)
                        if nbr.GetAtomicNum() == 8:
                            return True
        return False

    # Loop through the glycerol backbone matches. For a valid triglyceride, at least one match must have exactly
    # one appropriately placed (ester) oxygen on each of the three carbons.
    for match in matches:
        ester_count = 0
        valid_match = True
        # For each carbon atom in this glycerol fragment:
        for carbon_idx in match:
            carbon = mol.GetAtomWithIdx(carbon_idx)
            # Find neighbors (outside of the glycerol backbone) that are oxygen.
            oxygen_neighbors = [nbr for nbr in carbon.GetNeighbors() if nbr.GetAtomicNum() == 8 and nbr.GetIdx() not in match]
            # For glycerol esterification, we expect exactly one oxygen neighbor per carbon.
            if len(oxygen_neighbors) != 1:
                valid_match = False
                break
            # Now check that this oxygen is part of an ester bond.
            if not is_ester_oxygen(oxygen_neighbors[0], carbon_idx):
                valid_match = False
                break
            ester_count += 1
        if valid_match and ester_count == 3:
            return True, "Contains a glycerol backbone fully esterified with three fatty acid chains"
    
    return False, "Glycerol backbone with 3 proper ester bonds not found"

# Example usage:
if __name__ == "__main__":
    test_smiles = [
        # True positives
        "O(C(=O)CCCCCCCCCCCCC(C)C)[C@H](COC(=O)CCCCCCCCCCCCCCCCCCC)COC(=O)CCCCCCC",  # TG(8:0/i-16:0/20:0)
        "CCCCCCCC\\C=C/CCCCCCCC(=O)OCC(COC(=O)CCCCCCC\\C=C/CCCCCCCC)OC(=O)CCCCCCC\\C=C/CCCCCCCC",  # triolein
        "CC(=O)OCC(COC(C)=O)OC(C)=O",  # triacetin - small valid triglyceride
        # False positive sample (has phosphorus which is unexpected in a TG)
        "P(OC[C@H](OC(=O)CCCCCCCCCCC/C=C\\C/C=C\\CCCCC)(OC[C@@H](O)COC(=O)CCCCCCCCCCCCC)(O)=O"
    ]
    for smi in test_smiles:
        result, reason = is_triglyceride(smi)
        print(f"SMILES: {smi}\nTriglyceride? {result} ({reason})\n")


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:17855',
                          'name': 'triglyceride',
                          'definition': 'Any glyceride resulting from the '
                                        'condensation of all three hydroxy '
                                        'groups of glycerol '
                                        '(propane-1,2,3-triol) with fatty '
                                        'acids.',
                          'parents': ['CHEBI:47778', 'CHEBI:76579'],
                          'xrefs': [   'KEGG:C00422',
                                       'LIPID_MAPS_class:LMGL0301',
                                       'PMID:2474544'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 81,
                           'log_lines_of_code': 4.394449154672439,
                           'indent_by_line': [   1,
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
                                                 0,
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
                                                 3,
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
                                                 2,
                                                 2,
                                                 3,
                                                 3,
                                                 4,
                                                 3,
                                                 4,
                                                 4,
                                                 5,
                                                 6,
                                                 6,
                                                 7,
                                                 2,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
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
                                                 4,
                                                 3,
                                                 3,
                                                 4,
                                                 4,
                                                 3,
                                                 2,
                                                 3,
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
                           'max_indent': 7,
                           'imports': ['from rdkit import Chem'],
                           'imports_count': 1,
                           'methods_called': [   'MolFromSmiles',
                                                 'MolFromSmarts',
                                                 'GetBonds',
                                                 'GetNeighbors',
                                                 'GetOtherAtom',
                                                 'GetIdx',
                                                 'GetAtoms',
                                                 'GetAtomWithIdx',
                                                 'GetAtomicNum',
                                                 'GetBondTypeAsDouble',
                                                 'GetSymbol',
                                                 'GetSubstructMatches'],
                           'methods_called_count': 12,
                           'smarts_strings': ['glycerol_smarts'],
                           'smarts_strings_count': 1,
                           'defs': [   'is_triglyceride(smiles: str):',
                                       'is_ester_oxygen(oxygen_atom, '
                                       'parent_index):'],
                           'defs_count': 2,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, f"Contains atom '
                                          '{atom.GetSymbol()}, not expected in '
                                          'a simple triglyceride"',
                                          'False, "Glycerol backbone '
                                          '(CH2–CH–CH2) not found"',
                                          'True',
                                          'False',
                                          'True, "Contains a glycerol backbone '
                                          'fully esterified with three fatty '
                                          'acid chains"',
                                          'False, "Glycerol backbone with 3 '
                                          'proper ester bonds not found"'],
                           'returns_count': 7,
                           'complexity': 6.478889830934489},
    'message': '\n'
               'Attempt failed: F1 score of 0.767123287671233 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: '
               'O(C(=O)CCCCCCCCCCCCC(C)C)[C@H](COC(=O)CCCCCCCCCCCCCCCCCCC)COC(=O)CCCCCCC '
               'NAME: TG(8:0/i-16:0/20:0) REASON: CORRECT Contains a glycerol '
               'backbone fully esterified with three fatty acid chains\n'
               ' * SMILES: '
               'O(C(COC(=O)CCCCCCC/C=C\\CCCCCCCC)COC(=O)CCCCCCC/C=C\\CCCCCCCC)C(=O)CCCCCCC/C=C\\C/C=C\\C/C=C\\CC '
               'NAME: TG(18:1(9Z)/18:3(9Z,12Z,15Z)/18:1(9Z)) REASON: CORRECT '
               'Contains a glycerol backbone fully esterified with three fatty '
               'acid chains\n'
               ' * SMILES: '
               'O(C(=O)CCCCCCCCCCCCCCCCCC(C)C)[C@H](COC(=O)CCCCCCCCCCCC)COC(=O)CCCCCCCCC '
               'NAME: TG(10:0/i-21:0/13:0) REASON: CORRECT Contains a glycerol '
               'backbone fully esterified with three fatty acid chains\n'
               ' * SMILES: '
               'O([C@@H](COC(=O)CCCCCCCCCCCCCCCCCCC(C)C)COC(=O)CCCCCCCCC)C(=O)CCCCCCCCC(C)C '
               'NAME: TG(i-22:0/i-12:0/10:0) REASON: CORRECT Contains a '
               'glycerol backbone fully esterified with three fatty acid '
               'chains\n'
               ' * SMILES: '
               'C([C@@](COC(=O)CCCCCCCCCCCCCC)(OC(=O)CCCCCCC/C=C\\CCCCCCCC)[H])OC(CCCCCCC/C=C\\C/C=C\\C/C=C\\CC)=O '
               'NAME: TG(15:0/18:1(9Z)/18:3(9Z,12Z,15Z)) REASON: CORRECT '
               'Contains a glycerol backbone fully esterified with three fatty '
               'acid chains\n'
               ' * SMILES: '
               'O(C(=O)CCCCCCCCCCCCCCCCC)[C@H](COC(=O)CCCCCCC/C=C\\CCCCCC)COC(=O)CCCC/C=C\\C/C=C\\C/C=C\\CCCCC '
               'NAME: TG(16:1(9Z)/18:0/18:3(6Z,9Z,12Z)) REASON: CORRECT '
               'Contains a glycerol backbone fully esterified with three fatty '
               'acid chains\n'
               ' * SMILES: '
               'C([C@@](OC(=O)CCCCCCC/C=C\\C/C=C\\C/C=C\\CC)([H])COC(=O)CC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)OC(=O)CCC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC '
               'NAME: '
               'TG(20:5(5Z,8Z,11Z,14Z,17Z)/18:3(9Z,12Z,15Z)/22:6(4Z,7Z,10Z,13Z,16Z,19Z))[iso6] '
               'REASON: CORRECT Contains a glycerol backbone fully esterified '
               'with three fatty acid chains\n'
               ' * SMILES: '
               'O(C(=O)CCCCCCCCCCCCC)C[C@@H](OC(=O)CCCCCCC/C=C\\CCCC)COC(=O)CCCCCCCCCCC/C=C\\C/C=C\\CCCCC '
               'NAME: TG(14:0/14:1(9Z)/22:2(13Z,16Z)) REASON: CORRECT Contains '
               'a glycerol backbone fully esterified with three fatty acid '
               'chains\n'
               ' * SMILES: '
               'O([C@H](COC(=O)CCCCCCCCC/C=C\\C/C=C\\CCCCC)COC(=O)CCCCCCC/C=C\\CCCC)C(=O)CCCCCCC/C=C\\CCCCCC '
               'NAME: TG(14:1(9Z)/16:1(9Z)/20:2n6) REASON: CORRECT Contains a '
               'glycerol backbone fully esterified with three fatty acid '
               'chains\n'
               ' * SMILES: '
               'O(C(=O)CCCCCCCCCCCCCCCCC)[C@@H](COC(=O)CCCCCCC/C=C\\C/C=C\\CCCCC)COC(=O)CCC/C=C\\C/C=C\\C/C=C\\C/C=C\\CCCCC '
               'NAME: TG(18:2(9Z,12Z)/18:0/20:4(5Z,8Z,11Z,14Z)) REASON: '
               'CORRECT Contains a glycerol backbone fully esterified with '
               'three fatty acid chains\n'
               ' * SMILES: '
               'O(C(=O)CCCCCCC/C=C\\CCCCCC)C[C@H](OC(=O)CCCC/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)COC(=O)CCCCCCC/C=C\\C/C=C\\C/C=C\\CC '
               'NAME: TG(16:1(9Z)/18:4(6Z,9Z,12Z,15Z)/18:3(9Z,12Z,15Z)) '
               'REASON: CORRECT Contains a glycerol backbone fully esterified '
               'with three fatty acid chains\n'
               ' * SMILES: '
               'O(C(=O)CCCCCCCCCCCCCCCCCCC)C[C@H](OC(=O)CCC/C=C\\C/C=C\\C/C=C\\C/C=C\\CCCCC)COC(=O)CCCCCC/C=C\\C/C=C\\C/C=C\\CCCCC '
               'NAME: TG(20:0/20:4(5Z,8Z,11Z,14Z)/20:3n6) REASON: CORRECT '
               'Contains a glycerol backbone fully esterified with three fatty '
               'acid chains\n'
               ' * SMILES: '
               'O(C(=O)CCCCCCCCCCCCCCCCCCC)[C@H](COC(=O)CCCCCCC/C=C\\CCCCCC)COC(=O)CCCCCCC/C=C\\CCCC '
               'NAME: TG(14:1(9Z)/20:0/16:1(9Z)) REASON: CORRECT Contains a '
               'glycerol backbone fully esterified with three fatty acid '
               'chains\n'
               ' * SMILES: '
               'O(C(=O)CCCCCCCCC/C=C\\CCCCCCCC)C[C@H](OC(=O)CCCCCCC/C=C\\C/C=C\\CCCCC)COC(=O)CCCC/C=C\\C/C=C\\C/C=C\\CCCCC '
               'NAME: TG(20:1(11Z)/18:2(9Z,12Z)/18:3(6Z,9Z,12Z)) REASON: '
               'CORRECT Contains a glycerol backbone fully esterified with '
               'three fatty acid chains\n'
               ' * SMILES: '
               'O(C(=O)CCCCCCCCCCCCCCCCCCC)[C@H](COC(=O)CCCCCCCCCCCCCCCCCCC)COC(=O)CCCCCCCCC/C=C\\CCCCCCCC '
               'NAME: TG(20:0/20:0/20:1(11Z))[iso3] REASON: CORRECT Contains a '
               'glycerol backbone fully esterified with three fatty acid '
               'chains\n'
               ' * SMILES: '
               'O(C(=O)CCCCCCCCCCCCC)[C@@H](COC(=O)CCCCCCCCC/C=C\\C/C=C\\CCCCC)COC(=O)CCCCCCC/C=C\\C/C=C\\C/C=C\\CC '
               'NAME: TG(20:2n6/14:0/18:3(9Z,12Z,15Z)) REASON: CORRECT '
               'Contains a glycerol backbone fully esterified with three fatty '
               'acid chains\n'
               ' * SMILES: '
               'O(C(=O)CCCCCCCCCCCCCCCCC)[C@@H](COC(=O)CCCCCCCCC/C=C\\CCCCCCCC)COC(=O)CC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC '
               'NAME: TG(20:1(11Z)/18:0/22:6(4Z,7Z,10Z,13Z,16Z,19Z)) REASON: '
               'CORRECT Contains a glycerol backbone fully esterified with '
               'three fatty acid chains\n'
               ' * SMILES: '
               'O([C@@H](COC(=O)CCCCCCCCC/C=C\\C/C=C\\CCCCC)COC(=O)CCCCCCC/C=C\\C/C=C\\C/C=C\\CC)C(=O)CCCCCCCCC/C=C\\CCCCCC '
               'NAME: TG(20:2n6/18:1(11Z)/18:3(9Z,12Z,15Z)) REASON: CORRECT '
               'Contains a glycerol backbone fully esterified with three fatty '
               'acid chains\n'
               ' * SMILES: '
               'O(C(=O)CCCCCCC/C=C\\CCCCCCCC)C[C@@H](OC(=O)CCCCC/C=C\\C/C=C\\C/C=C\\C/C=C\\CCCCC)COC(=O)CCCCCCC/C=C\\CCCCCC '
               'NAME: TG(16:1(9Z)/22:4(7Z,10Z,13Z,16Z)/18:1(9Z)) REASON: '
               'CORRECT Contains a glycerol backbone fully esterified with '
               'three fatty acid chains\n'
               ' * SMILES: '
               'O(C(=O)CCCCCCCCCCCCCC)C[C@H](OC(=O)CCCCCCCCC/C=C\\CCCCCC)COC(=O)CCC/C=C\\C/C=C\\C/C=C\\CCCCCCCC '
               'NAME: TG(15:0/18:1(11Z)/20:3(5Z,8Z,11Z)) REASON: CORRECT '
               'Contains a glycerol backbone fully esterified with three fatty '
               'acid chains\n'
               ' * SMILES: '
               'O(C(=O)CCCCCCC/C=C\\CCCCCCCC)C[C@@H](OC(=O)CCC/C=C\\C/C=C\\C/C=C\\CCCCCCCC)COC(=O)CCCCCCC/C=C\\CCCCCC '
               'NAME: TG(16:1(9Z)/20:3(5Z,8Z,11Z)/18:1(9Z)) REASON: CORRECT '
               'Contains a glycerol backbone fully esterified with three fatty '
               'acid chains\n'
               ' * SMILES: '
               'O(C(=O)CCCCCCCCCCCCCCCCCCCC)C[C@H](OC(=O)CCCCCCCCCCCC)COC(=O)CCCCCCCCC '
               'NAME: TG(21:0/13:0/10:0) REASON: CORRECT Contains a glycerol '
               'backbone fully esterified with three fatty acid chains\n'
               ' * SMILES: '
               'O(C(=O)CCCCCCCCCCCCCCCCCC)[C@H](COC(=O)CCCCCCC/C=C\\C/C=C\\C/C=C\\CC)COC(=O)CCC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC '
               'NAME: TG(18:3(9Z,12Z,15Z)/19:0/20:5(5Z,8Z,11Z,14Z,17Z))[iso6] '
               'REASON: CORRECT Contains a glycerol backbone fully esterified '
               'with three fatty acid chains\n'
               ' * SMILES: '
               'O([C@H](COC(=O)CCCCCCC/C=C\\CCCCCC)COC(=O)CCCC/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)C(=O)CCCCCCC/C=C\\C/C=C\\C/C=C\\CC '
               'NAME: TG(16:1(9Z)/18:3(9Z,12Z,15Z)/18:4(6Z,9Z,12Z,15Z))[iso6] '
               'REASON: CORRECT Contains a glycerol backbone fully esterified '
               'with three fatty acid chains\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCC(=O)OCC(COC(=O)CCCCCCC\\C=C/CCCCCCCC)OC(=O)CCCCCCC\\C=C/CCCCCCCC '
               'NAME: 1,2-dioleoyl-3-palmitoylglycerol REASON: CORRECT '
               'Contains a glycerol backbone fully esterified with three fatty '
               'acid chains\n'
               'False positives: SMILES: '
               'S(C1[C@H](/C(/C(O)C1)=C\\C[C@@H](O)CCCCC)C/C=C\\CCCC(O)=O)C[C@H](NC(=O)CC[C@@H](N)C(O)=O)C(=O)NCC(O)=O '
               'NAME: S-(11-OH-9-deoxy-delta9,12-PGD2)-glutathione REASON: '
               'WRONGLY CLASSIFIED Contains a glycerol backbone fully '
               'esterified with three fatty acid chains\n'
               ' * SMILES: '
               'P(OC[C@H](OC(=O)CCCCCCCCCCC/C=C\\C/C=C\\CCCCC)COC(=O)CCCCCC/C=C\\C/C=C\\C/C=C\\CCCCC)(OC[C@H](N)C(O)=O)(O)=O '
               'NAME: PS(20:3(8Z,11Z,14Z)/22:2(13Z,16Z)) REASON: WRONGLY '
               'CLASSIFIED Contains a glycerol backbone fully esterified with '
               'three fatty acid chains\n'
               ' * SMILES: '
               'P(OC[C@@H](OC(=O)CCCCCCCCCCCCC)COC(=O)CCCCCCCCCCCCC)(OC[C@@H](O)COC(=O)CCCCCCCCCCCCC)(O)=O '
               'NAME: SLBPA(42:0) REASON: WRONGLY CLASSIFIED Contains a '
               'glycerol backbone fully esterified with three fatty acid '
               'chains\n'
               ' * SMILES: '
               'ClC1=C(C(=C(O)C=C1)C(=O)O[C@H]2[C@H](O)[C@@H](O)[C@H](O[C@@H]3[C@@H](O)[C@@H](O[C@@H]([C@H]3O)C)O[C@@H]4[C@H]5C=CC6[C@@H](C=CC[C@@]7(C=C(C)[C@@H](C[C@]87C(=C(OC([C@]6([C@@H]5[C@@H](C)C[C@H]4C)C)=O)C(=O)O8)O)C[C@H](O)[C@@](O)(C(=O)C)C)C)C)O[C@@H]2C)C '
               'NAME: Phocoenamicin C REASON: WRONGLY CLASSIFIED Contains a '
               'glycerol backbone fully esterified with three fatty acid '
               'chains\n'
               ' * SMILES: '
               '[H][C@]1(O[C@@](O)(C[C@H](O)[C@H]1NC(=O)N1N=NC2C1C1=CC=CC=C1N(CC1=C2C=CC=C1)C(=O)CCNC(=O)[C@@H](CCCCN)NC(=O)[C@@H](CCCCN)NC(=O)[C@@H](CCCCN)NC(=O)[C@@H](CCCCN)NC(=O)[C@@H](CO)NC(=O)[C@@H](CSCC(COC(=O)CCCCCCCCCCCCCCC)OC(=O)CCCCCCCCCCCCCCC)NC(=O)CCCCCCCCCCCCCCC)C(O)=O)[C@H](O)[C@H](O)CO '
               'NAME: ManNAz-DBCO-Pam3CSK4 REASON: WRONGLY CLASSIFIED Contains '
               'a glycerol backbone fully esterified with three fatty acid '
               'chains\n'
               ' * SMILES: '
               'P(OCC[N+](C)(C)C)(OC[C@H](OC(=O)CCCC(O)=O)COC(=O)CCCCCCC/C=C\\CCCCCCCC)([O-])=O '
               'NAME: OG-PC REASON: WRONGLY CLASSIFIED Contains a glycerol '
               'backbone fully esterified with three fatty acid chains\n'
               ' * SMILES: '
               'P(OC[C@H](OC(=O)CCCC(O)=O)COC(=O)CCCCCCC/C=C\\CCCCCCCC)(OC[C@@H](O)CO)(O)=O '
               'NAME: OG-PG REASON: WRONGLY CLASSIFIED Contains a glycerol '
               'backbone fully esterified with three fatty acid chains\n'
               ' * SMILES: '
               'P(OC1C(O)C(O)C(O)[C@@H](O)C1O)(OC[C@H](OC(=O)CCC(=O)/C=C/C(O)=O)COC(=O)CCCCCCCCCCCCCCC)(O)=O '
               'NAME: PKHdiA-PI REASON: WRONGLY CLASSIFIED Contains a glycerol '
               'backbone fully esterified with three fatty acid chains\n'
               ' * SMILES: '
               'P(OC[C@H](OC(=O)CCCCCC/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)COC(=O)CCCCCCCCCCCCC)(OC[C@H](N)C(O)=O)(O)=O '
               'NAME: PS(14:0/20:4(8Z,11Z,14Z,17Z)) REASON: WRONGLY CLASSIFIED '
               'Contains a glycerol backbone fully esterified with three fatty '
               'acid chains\n'
               ' * SMILES: '
               'CCCCC\\C=C/C\\C=C/CCCCCCCC(=O)OC[C@H](COP([O-])(=O)OCC(O)COP([O-])(=O)OC[C@@H](CO)OC(=O)CCCCCCC\\C=C/C\\C=C/CCCCC)OC(=O)CCCCCCC\\C=C/C\\C=C/CCCCC '
               "NAME: 1,2,2'-trilinoleoyl-1'-monolysocardiolipin(2-) REASON: "
               'WRONGLY CLASSIFIED Contains a glycerol backbone fully '
               'esterified with three fatty acid chains\n'
               ' * SMILES: '
               'O=C1OC2=CC=C(CC(NC(=O)C(NC(=O)C(NC(=O)CC(O)CCCCCCCCCCCCCC)CCC(=O)O)CCCN)C(=O)NC(C(=O)NC(C(=O)NC(C(N3C(C(NC(C(NC(C(NC1C(C)C)=O)CC4=CC=C(O)C=C4)=O)CCC(=O)N)=O)CCC3)=O)C(C)C)CCC(=O)O)C(O)C)C=C2 '
               'NAME: SNA-60-367-8 REASON: WRONGLY CLASSIFIED Contains a '
               'glycerol backbone fully esterified with three fatty acid '
               'chains\n'
               ' * SMILES: '
               'P(OC[C@H](OC(=O)CCCCCCCC(=O)/C=C/C=O)COC(=O)CCCCCCCCCCCCCCC)(OC[C@H](N)C(O)=O)(O)=O '
               'NAME: PKODA-PS REASON: WRONGLY CLASSIFIED Contains a glycerol '
               'backbone fully esterified with three fatty acid chains\n'
               ' * SMILES: '
               'P(OC[C@H](OC(=O)CCCCCCC/C=C\\CCCC)COC(=O)CCCC/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)(OC[C@H](N)C(O)=O)(O)=O '
               'NAME: PS(18:4(6Z,9Z,12Z,15Z)/14:1(9Z)) REASON: WRONGLY '
               'CLASSIFIED Contains a glycerol backbone fully esterified with '
               'three fatty acid chains\n'
               ' * SMILES: '
               'O=C1O[C@@H](CC(=O)N[C@H](C(=O)N[C@H](C(=O)N[C@@H](CC(C)C)C(N[C@H](C(N[C@H](C(N[C@H](C(N[C@H]1CC(C)C)=O)CC(C)C)=O)CC(=O)O)=O)C)=O)CC(C)C)CCC(=O)O)CCCCCCCCCCCCC '
               'NAME: '
               '3-[(3S,6S,9S,12S,15S,18S,21S,25R)-9-(carboxymethyl)-12-methyl-3,6,15,18-tetrakis(2-methylpropyl)-2,5,8,11,14,17,20,23-octaoxo-25-tridecyl-1-oxa-4,7,10,13,16,19,22-heptazacyclopentacos-21-yl]propanoic '
               'acid REASON: WRONGLY CLASSIFIED Contains a glycerol backbone '
               'fully esterified with three fatty acid chains\n'
               ' * SMILES: '
               'P(OC[C@H](OC(=O)CCCC(=O)/C=C/C(O)=O)COC(=O)CCCCCCCCCCCCCCC)(OCCN)(O)=O '
               'NAME: PKODiA-PE REASON: WRONGLY CLASSIFIED Contains a glycerol '
               'backbone fully esterified with three fatty acid chains\n'
               ' * SMILES: '
               'O=C(OC(CC1=CC=C(O[C@H]2OC([C@@H](OC)C(C2OC)O[C@H]3OC([C@@H](O)C(C3OC)O[C@H]4OC([C@H](OC(=O)CC)C(C4OC)O[C@@H]5OC([C@@H](OC)C(C5)O)C)C)C)C)C=C1)CC(OC(=O)C(CCC)C)CCCCC(C(OC)CC)C)C(CCC)C '
               'NAME: PGL K5 REASON: WRONGLY CLASSIFIED Contains a glycerol '
               'backbone fully esterified with three fatty acid chains\n'
               ' * SMILES: '
               'P(OC[C@H](OC(=O)CCCCCCC/C=C\\CCCCCC)COC(=O)CCCCCCC/C=C\\CCCCCCCCC)(OC[C@H](N)C(O)=O)(O)=O '
               'NAME: PS(17:0/18:2) REASON: WRONGLY CLASSIFIED Contains a '
               'glycerol backbone fully esterified with three fatty acid '
               'chains\n'
               ' * SMILES: '
               '[H][C@](COP(OC[C@@](COC(CCCCCCCCCCCCCCCCC)=O)(OC(CCCCCCCCCCCCCCC)=O)[H])(=O)O)(C(O)=O)N '
               'NAME: PS(18:0/16:0) REASON: WRONGLY CLASSIFIED Contains a '
               'glycerol backbone fully esterified with three fatty acid '
               'chains\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCC(=O)O[C@H](COC(=O)CCCCCCC\\C=C/CCCCCCCC)COP(O)(=O)OC[C@H](N)C(O)=O '
               'NAME: 1-oleoyl-2-stearoyl-sn-glycero-3-phospho-L-serine '
               'REASON: WRONGLY CLASSIFIED Contains a glycerol backbone fully '
               'esterified with three fatty acid chains\n'
               ' * SMILES: '
               'O([C@H]1[C@H](O)C(O)[C@@H](OC1COC(=O)C)OCC(O)CCCCCCCCCCCCC(O)C(O)=O)[C@@H]2OC([C@@H](O)[C@H](O)C2OC(=O)CC(O)CCC)CO '
               'NAME: Ustilagic acid REASON: WRONGLY CLASSIFIED Contains a '
               'glycerol backbone fully esterified with three fatty acid '
               'chains\n'
               ' * SMILES: '
               'P(OC[C@H](OC(=O)CCCCCCCCCCCCCCCC)COC(=O)CCCCCCC/C=C\\CCCCCCCCC)(OC[C@H](N)C(O)=O)(O)=O '
               'NAME: PS(19:1(9Z)/17:0) REASON: WRONGLY CLASSIFIED Contains a '
               'glycerol backbone fully esterified with three fatty acid '
               'chains\n'
               ' * SMILES: '
               'P(OC[C@H](OC(=O)CCCCCCC/C=C\\CCCCCCC)COC(=O)CCCCCCC/C=C\\CCCCCCC)(OC[C@H](N)C(O)=O)(O)=O '
               'NAME: PS(17:1(9Z)/17:1(9Z)) REASON: WRONGLY CLASSIFIED '
               'Contains a glycerol backbone fully esterified with three fatty '
               'acid chains\n'
               ' * SMILES: '
               'P(OC[C@H](OC(=O)CCCCCCCCC/C=C\\C/C=C\\CCCCC)COC(=O)CCCCCCCCCCCCC)(OC[C@H](N)C(O)=O)(O)=O '
               'NAME: PS(14:0/20:2(11Z,14Z)) REASON: WRONGLY CLASSIFIED '
               'Contains a glycerol backbone fully esterified with three fatty '
               'acid chains\n'
               ' * SMILES: '
               'P(O[C@H]1C(C(O)C(O)[C@@H](O)C1O)C)(OC[C@H](OC(=O)CCCC(O)=O)COC(=O)CCCCCCCCCCCCCCC)(O)=O '
               'NAME: PG-PI REASON: WRONGLY CLASSIFIED Contains a glycerol '
               'backbone fully esterified with three fatty acid chains\n'
               ' * SMILES: '
               'O(C[C@H](COP(=O)(OC[C@@H](C(O)=O)N)O)OC(CCCCCCC/C=C/CCCCCCCC)=O)C(CCCCCCC/C=C/CCCCCCCC)=O '
               'NAME: 1,2-di-(9E-octadecenoyl)-sn-glycero-3-phosphoserine '
               'REASON: WRONGLY CLASSIFIED Contains a glycerol backbone fully '
               'esterified with three fatty acid chains\n'
               'False negatives: SMILES: CC(=O)OCC(COC(C)=O)OC(C)=O NAME: '
               'triacetin REASON: MISSED Molecular weight too low (218.1 Da) '
               'for a typical triglyceride\n'
               ' * SMILES: CCCC(=O)OCC(COC(=O)CCC)OC(=O)CCC NAME: tributyrin '
               'REASON: MISSED Molecular weight too low (302.2 Da) for a '
               'typical triglyceride\n'
               ' * SMILES: '
               'O([C@H](COC(=O)CCCCCCCCC)COC(=O)CCCCCCC)C(=O)CCCCCCC NAME: '
               'TG(8:0/8:0/10:0) REASON: MISSED Molecular weight too low '
               '(498.4 Da) for a typical triglyceride\n'
               ' * SMILES: CCCCCCCC(=O)OCC(COC(=O)CCCCCCC)OC(=O)CCCCCCC NAME: '
               'trioctanoin REASON: MISSED Molecular weight too low (470.4 Da) '
               'for a typical triglyceride\n'
               ' * SMILES: O(C(=O)CCCCCCCCCCCCCCCCC)CC(OC(=O)C)COC(=O)C NAME: '
               '2,3-Diacetoxypropyl stearate REASON: MISSED Molecular weight '
               'too low (442.3 Da) for a typical triglyceride\n'
               ' * SMILES: CCCCCC(=O)OCC(COC(=O)CCCCC)OC(=O)CCCCC NAME: '
               'tricaproin REASON: MISSED Molecular weight too low (386.3 Da) '
               'for a typical triglyceride\n'
               ' * SMILES: '
               'CCCCC\\C=C/C=C/C(=O)OCC=C=CCCCC(=O)OCC(COC(=O)CCCCCCC\\C=C/C\\C=C/C\\C=C/CC)OC(=O)CCCCCCC\\C=C/C\\C=C/C\\C=C/CC '
               'NAME: '
               '1,2-Di-(9Z,12Z,15Z-octadecatrienoyl)-3-(8-(2E,4Z-decadienoyloxy)-5,6-octadienoyl)-sn-glycerol '
               'REASON: MISSED Expected exactly 3 ester bonds, found 4\n'
               ' * SMILES: O(C(=O)CCCCC)C(COC(=O)CCCCCCCCCCCCC)COC(=O)CCCCC '
               'NAME: 1,2-dicaproyl-3-myristoylglycerol REASON: MISSED '
               'Molecular weight too low (498.4 Da) for a typical '
               'triglyceride\n'
               ' * SMILES: O(CC(COC(CC)=O)OC(=O)CC)C(CC)=O NAME: tripropionin '
               'REASON: MISSED Molecular weight too low (260.1 Da) for a '
               'typical triglyceride\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'C1=CC=C2C(=C1)C(=O)C3=CC=CC=C3C2(CC4=CC(=NC=C4)F)CC5=CC(=NC=C5)F',
                                     'name': '10,10-bis[(2-fluoro-4-pyridinyl)methyl]-9-anthracenone',
                                     'reason': 'Contains atom N, not expected '
                                               'in a simple triglyceride'},
                                 {   'smiles': 'C[C@@H](C1=CC=CC=C1)NC(=O)[C@@H]2[C@H]([C@@H]3CN4C(=CC=C(C4=O)C5=CC=CC=C5F)[C@H]2N3C)CO',
                                     'name': 'LSM-10936',
                                     'reason': 'Contains atom N, not expected '
                                               'in a simple triglyceride'},
                                 {   'smiles': '[H]C(=CC(=O)C(O)=O)C(CC(O)=O)C(O)=O',
                                     'name': '5-oxopent-3-ene-1,2,5-tricarboxylic '
                                             'acid',
                                     'reason': 'Glycerol backbone (CH2–CH–CH2) '
                                               'not found'},
                                 {   'smiles': 'S1N(C2=CC=C(C=C2)C(OCC)=O)C(=O)C=C1',
                                     'name': 'ethyl '
                                             '4-(3-oxo-2,3-dihydroisothiazol-2-yl)benzoate',
                                     'reason': 'Contains atom S, not expected '
                                               'in a simple triglyceride'},
                                 {   'smiles': 'COc1cc(O)c2c(c1)oc1c(O)cccc1c2=O',
                                     'name': 'mesuaxanthone A',
                                     'reason': 'Glycerol backbone (CH2–CH–CH2) '
                                               'not found'},
                                 {   'smiles': 'O([C@@H]1[C@H](O)[C@@H](O[C@@H]([C@H]1O)CO[C@H]2O[C@@H]([C@@H](O)[C@H](O)[C@@H]2O[C@@H]3O[C@@H]([C@@H](O)[C@H](O)[C@H]3NC(=O)C)CO)CO[C@@H]4O[C@@H]([C@@H](O)[C@H](O)[C@H]4NC(=O)C)CO)O[C@H]5[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]5CO)O[C@H]6[C@H](O)[C@@H](NC(=O)C)C(O[C@@H]6CO)O)[C@H]7O[C@@H]([C@@H](O[C@@H]8O[C@@H]([C@@H](O)[C@H](O)[C@H]8NC(=O)C)CO)[C@H](O)[C@@H]7O[C@@H]9O[C@@H]([C@@H](O[C@@H]%10O[C@@H]([C@H](O)[C@H](O)[C@H]%10O)CO)[C@H](O)[C@H]9NC(=O)C)CO)CO',
                                     'name': 'N-[(3R,4R,5S,6R)-5-[(2S,3R,4R,5S,6R)-3-Acetamido-5-[(2S,3S,4S,5R,6R)-6-[[(2S,3S,4S,5S,6R)-3-[(2R,3R,4R,5S,6R)-3-acetamido-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-6-[[(2R,3R,4R,5S,6R)-3-acetamido-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxymethyl]-4,5-dihydroxyoxan-2-yl]oxymethyl]-4-[(2R,3S,4S,5S,6R)-5-[(2R,3R,4R,5S,6R)-3-acetamido-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-3-[(2S,3R,4R,5S,6R)-3-acetamido-4-hydroxy-6-(hydroxymethyl)-5-[(2S,3R,4S,5R,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-3,5-dihydroxyoxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-2,4-dihydroxy-6-(hydroxymethyl)oxan-3-yl]acetamide',
                                     'reason': 'Contains atom N, not expected '
                                               'in a simple triglyceride'},
                                 {   'smiles': 'CCCCCCCC\\C=C/CCCCCCCC(=O)OC[C@H](COP([O-])(=O)OC[C@H]([NH3+])C([O-])=O)OC(=O)CCC\\C=C/C\\C=C/C\\C=C/C\\C=C/CCCCC',
                                     'name': '1-oleoyl-2-arachidonoyl-sn-glycero-3-phospho-L-serine(1-)',
                                     'reason': 'Contains atom P, not expected '
                                               'in a simple triglyceride'},
                                 {   'smiles': 'OC(=Cc1ccccc1)C([O-])=O',
                                     'name': 'enol-phenylpyruvate',
                                     'reason': 'Glycerol backbone (CH2–CH–CH2) '
                                               'not found'},
                                 {   'smiles': '[H][C@]1(CC[C@]2(C)[C@@H](O)CCC(=C)[C@@]12[H])[C@@H](O)C(C)C',
                                     'name': '(1R,3aS,4S,7aR)-1-((S)-1-hydroxy-2-methylpropyl)-3a-methyl-7-methyleneoctahydro-1H-inden-4-ol',
                                     'reason': 'Glycerol backbone (CH2–CH–CH2) '
                                               'not found'},
                                 {   'smiles': 'O1C(C(O)C(O)C(O)C1CO)C=2C(=O)C=3C(O)=C(C4OC(C(O)C(O)C4O)CO)C(O)=CC3OC2C5=CC=C(OC)C=C5',
                                     'name': "3,6-Diglucopyranosyl-5,7-dihydroxy-4'-methoxyflavone",
                                     'reason': 'Glycerol backbone (CH2–CH–CH2) '
                                               'not found'}],
    'sample_false_negatives': [],
    'attempt': 1,
    'reasoning': 'We can improve our approach by “anchoring” our '
                 'classification to the chemical connectivity expected in a '
                 'triglyceride. In a true triglyceride the glycerol core (a '
                 '–CH2–CH–CH2– chain) must have exactly three (and only three) '
                 'ester bonds attached. Furthermore, triglycerides normally '
                 'contain only C, H, and O atoms. (Note that very “small” '
                 'triglycerides such as triacetin are valid even though their '
                 'molecular weight is below 500\u2009Da.) In our revised '
                 'version we first check that no extra elements (e.g. P, N, S) '
                 'are present. Then we search for a glycerol backbone using '
                 'the SMARTS pattern "[CH2][CH][CH2]". For each match we '
                 'inspect each of the three carbons to see if it has exactly '
                 'one oxygen attached that in turn connects to a carbonyl '
                 '(i.e. a C(=O) group). Only if one such glycerol fragment is '
                 'found do we classify the molecule as a triglyceride.\n'
                 '\n'
                 'Below is the complete Python code with detailed comments:',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 1185,
    'num_false_positives': 0,
    'num_true_negatives': 141115,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 1.0,
    'recall': 1.0,
    'f1': 1.0,
    'accuracy': 1.0,
    'negative_predictive_value': 1.0}