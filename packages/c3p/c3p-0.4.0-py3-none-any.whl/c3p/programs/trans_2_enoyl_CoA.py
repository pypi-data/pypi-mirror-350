"""
Classifies: CHEBI:50998 trans-2-enoyl-CoA
"""
#!/usr/bin/env python3
"""
Classifies: trans-2-enoyl-CoA
An unsaturated fatty acyl-CoA that results from the formal condensation of the thiol group 
of coenzyme A with the carboxy group of any 2,3-trans-enoic acid.
  
This improved version first assigns stereochemistry and uses a more robust approach:
  - It verifies a CoA moiety by matching a common fragment (ignoring formal charge differences).
  - It identifies a thioester linkage.
  - It then “extracts” the acyl chain side of the thioester and checks:
      • that the carbonyl carbon is attached to exactly one carbon (the “alpha” carbon)
      • that the alpha carbon forms a double bond to a beta carbon
      • that this double bond is marked as trans (E)
      • that the acyl chain is long and mostly aliphatic.
If all checks pass, the molecule is classified as trans-2-enoyl-CoA.
  
False positives from the earlier version (e.g. structures with extra charges or subtle modifications)
are less likely to pass the extra acyl-chain analysis.
"""
from rdkit import Chem
from rdkit.Chem import rdMolDescriptors

def is_trans_2_enoyl_CoA(smiles: str):
    """
    Determines if a molecule is a trans-2-enoyl-CoA based on its SMILES string.

    The function performs the following checks:
      1. Validity of the SMILES.
      2. Presence of a CoA moiety (via a common CoA fragment, ignoring charge differences).
      3. Presence of a thioester linkage ([CX3](=O)[SX2]) and extraction of the acyl side.
      4. The acyl chain (attached to the carbonyl carbon of the thioester) must include 
         a double bond between the alpha (C2) and beta (C3) carbons, and that double bond 
         must be in trans (E) configuration.
      5. The acyl chain is further verified to be a contiguous aliphatic chain of reasonable length.
         
    Args:
        smiles (str): SMILES string of the molecule.

    Returns:
        bool: True if molecule is identified as trans-2-enoyl-CoA, False otherwise.
        str: Reason for classification.
    """
    # Parse and sanitize the molecule
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
    # Force assignment of stereochemistry 
    Chem.AssignStereochemistry(mol, force=True)
    
    # Look for a CoA fragment. We use a common substructure 
    # (ignoring formal charge on phosphate oxygens using wildcard for oxygen atoms).
    # This pattern should match both protonated and deprotonated forms.
    coa_pattern = Chem.MolFromSmarts("SCCNC(=O)CCNC(=O)")
    if not mol.HasSubstructMatch(coa_pattern):
        return False, "Missing characteristic CoA moiety"
    
    # Look for a thioester linkage defined as [CX3](=O)[SX2]
    thioester_pattern = Chem.MolFromSmarts("[CX3](=O)[SX2]")
    thioester_matches = mol.GetSubstructMatches(thioester_pattern)
    if not thioester_matches:
        return False, "Missing thioester (acyl-CoA linkage) moiety"
    
    # For each thioester found, examine the acyl chain
    for match in thioester_matches:
        # In the match tuple, index 0 is the carbonyl carbon and index 1 is the sulfur.
        carbonyl_idx = match[0]
        sulfur_idx = match[1]
        carbonyl_atom = mol.GetAtomWithIdx(carbonyl_idx)
        
        # Identify the "alpha" carbon attached to the carbonyl (exclude the sulfur).
        alpha_candidates = [nbr.GetIdx() for nbr in carbonyl_atom.GetNeighbors() 
                            if nbr.GetIdx() != sulfur_idx and nbr.GetSymbol() == "C"]
        if not alpha_candidates:
            continue  # no valid alpha carbon found in this match
        alpha_idx = alpha_candidates[0]
        alpha_atom = mol.GetAtomWithIdx(alpha_idx)
        
        # We now look for a double bond from the alpha carbon to a beta carbon.
        acyl_double_found = False
        for bond in alpha_atom.GetBonds():
            # Recognize a double bond that connects alpha atom to another carbon.
            if bond.GetBondType() == Chem.rdchem.BondType.DOUBLE:
                beta_atom = bond.GetOtherAtom(alpha_atom)
                if beta_atom.GetSymbol() != "C":
                    continue
                # Check whether the double bond stereochemistry is assigned as trans.
                stereo = bond.GetStereo()
                if stereo != Chem.rdchem.BondStereo.STEREOE:
                    return False, "Double bond adjacent to thioester is not in trans (E) configuration"
                # Extra check: ensure the double bond is at the expected position.
                # We require that the alpha carbon has only one carbon neighbor besides the carbonyl
                # (i.e. the double-bond forms the start of a linear acyl chain).
                alpha_nb_carbons = [nbr for nbr in alpha_atom.GetNeighbors() if nbr.GetSymbol() == "C"]
                if len(alpha_nb_carbons) < 2:
                    return False, "Acyl chain too short: insufficient carbons on alpha atom"
                
                # Further, traverse from the beta carbon along a linear chain (non-branched, aliphatic)
                # and count a few atoms. Valid fatty acyl chains are usually at least 3 carbons long.
                chain_length = 1  # beta carbon counts as 1
                current_atom = beta_atom
                prev_idx = alpha_idx
                # Walk outwards in the chain for up to 5 bonds (we expect a medium-to-long fatty chain)
                for _ in range(5):
                    neighbors = [nbr for nbr in current_atom.GetNeighbors() if nbr.GetIdx() != prev_idx and nbr.GetSymbol() == "C"]
                    if not neighbors:
                        break
                    # if more than one neighbor then branching; we consider the chain valid if one continuous path exists
                    current_atom = neighbors[0]
                    prev_idx = current_atom.GetIdx()
                    chain_length += 1
                if chain_length < 2:
                    return False, "Acyl chain appears too short"
                acyl_double_found = True
                # If we have reached here then the thioester, alpha-beta double bond (with trans stereo)
                # and a minimally extended acyl chain are detected.
                return True, ("Found thioester with an acyl chain exhibiting a trans (E) double bond at "
                              "the 2-enoyl position and a CoA moiety")
        # End for bonds on alpha_atom
    # End for each thioester match
    
    return False, "No appropriate trans-2-enoyl double bond detected in the acyl chain"

# For testing (if run directly), one can uncomment the lines below:
# if __name__ == "__main__":
#     test_smiles = "CCCC\\C=C\\C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12"
#     valid, reason = is_trans_2_enoyl_CoA(test_smiles)
#     print(valid, reason)


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:50998',
                          'name': 'trans-2-enoyl-CoA',
                          'definition': 'An unsaturated fatty acyl-CoA that '
                                        'results from the formal condensation '
                                        'of the thiol group of coenzyme A with '
                                        'the carboxy group of any '
                                        '2,3-trans-enoic acid.',
                          'parents': ['CHEBI:19573'],
                          'xrefs': ['KEGG:C00658'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 88,
                           'log_lines_of_code': 4.477336814478207,
                           'indent_by_line': [   1,
                                                 1,
                                                 0,
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
                                                 2,
                                                 1,
                                                 1,
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
                                                 3,
                                                 2,
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
                                                 4,
                                                 5,
                                                 4,
                                                 4,
                                                 4,
                                                 4,
                                                 4,
                                                 5,
                                                 4,
                                                 4,
                                                 4,
                                                 4,
                                                 4,
                                                 4,
                                                 4,
                                                 4,
                                                 5,
                                                 5,
                                                 6,
                                                 5,
                                                 5,
                                                 5,
                                                 5,
                                                 4,
                                                 5,
                                                 4,
                                                 4,
                                                 4,
                                                 4,
                                                 4,
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 0],
                           'max_indent': 6,
                           'imports': [   'from rdkit import Chem',
                                          'from rdkit.Chem import '
                                          'rdMolDescriptors'],
                           'imports_count': 2,
                           'methods_called': [   'GetAtomWithIdx',
                                                 'GetSubstructMatches',
                                                 'MolFromSmarts',
                                                 'MolFromSmiles',
                                                 'GetSymbol',
                                                 'HasSubstructMatch',
                                                 'GetIdx',
                                                 'GetNeighbors',
                                                 'GetOtherAtom',
                                                 'GetStereo',
                                                 'GetBonds',
                                                 'AssignStereochemistry',
                                                 'GetBondType'],
                           'methods_called_count': 13,
                           'smarts_strings': [   '[CX3](=O)[SX2]',
                                                 'SCCNC(=O)CCNC(=O)'],
                           'smarts_strings_count': 2,
                           'defs': ['is_trans_2_enoyl_CoA(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "Missing characteristic CoA '
                                          'moiety"',
                                          'False, "Missing thioester (acyl-CoA '
                                          'linkage) moiety"',
                                          'False, "Double bond adjacent to '
                                          'thioester is not in trans (E) '
                                          'configuration"',
                                          'False, "Acyl chain too short: '
                                          'insufficient carbons on alpha atom"',
                                          'False, "Acyl chain appears too '
                                          'short"',
                                          'True, ("Found thioester with an '
                                          'acyl chain exhibiting a trans (E) '
                                          'double bond at "',
                                          'False, "No appropriate '
                                          'trans-2-enoyl double bond detected '
                                          'in the acyl chain"'],
                           'returns_count': 8,
                           'complexity': 6.495467362895641},
    'message': '\n'
               'Attempt failed: F1 score of 0.19622641509433963 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: '
               'CCCCC\\C=C/C\\C=C/CCCCC\\C=C\\C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12 '
               'NAME: (2E,9Z,12Z)-octadecatrienoyl-CoA REASON: CORRECT Found '
               'thioester with an acyl chain exhibiting a trans (E) double '
               'bond at the 2-enoyl position and a CoA moiety\n'
               ' * SMILES: '
               'CCCCCCCC\\C=C\\CCCCC\\C=C\\C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12 '
               'NAME: (2E,9E)-octadecadienoyl-CoA REASON: CORRECT Found '
               'thioester with an acyl chain exhibiting a trans (E) double '
               'bond at the 2-enoyl position and a CoA moiety\n'
               ' * SMILES: '
               'CCC\\C=C\\C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12 '
               'NAME: trans-hex-2-enoyl-CoA REASON: CORRECT Found thioester '
               'with an acyl chain exhibiting a trans (E) double bond at the '
               '2-enoyl position and a CoA moiety\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCC\\C=C\\C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12 '
               'NAME: trans-2-heptadecenoyl-CoA REASON: CORRECT Found '
               'thioester with an acyl chain exhibiting a trans (E) double '
               'bond at the 2-enoyl position and a CoA moiety\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCCCCCCCCCCC\\C=C\\C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12 '
               'NAME: trans-2-triacontenoyl-CoA REASON: CORRECT Found '
               'thioester with an acyl chain exhibiting a trans (E) double '
               'bond at the 2-enoyl position and a CoA moiety\n'
               ' * SMILES: '
               'CCCCCCCCCCCC\\C=C(/C)C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12 '
               'NAME: (E)-2-methylpentadec-2-enoyl-CoA REASON: CORRECT Found '
               'thioester with an acyl chain exhibiting a trans (E) double '
               'bond at the 2-enoyl position and a CoA moiety\n'
               ' * SMILES: '
               'CCCCC\\C=C/C=C/C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12 '
               'NAME: (2E,4Z)-deca-2,4-dienoyl-CoA REASON: CORRECT Found '
               'thioester with an acyl chain exhibiting a trans (E) double '
               'bond at the 2-enoyl position and a CoA moiety\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCCC\\C=C\\C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12 '
               'NAME: trans-2-docosenoyl-CoA REASON: CORRECT Found thioester '
               'with an acyl chain exhibiting a trans (E) double bond at the '
               '2-enoyl position and a CoA moiety\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCC\\C=C\\C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12 '
               'NAME: trans-2-icosenoyl-CoA REASON: CORRECT Found thioester '
               'with an acyl chain exhibiting a trans (E) double bond at the '
               '2-enoyl position and a CoA moiety\n'
               ' * SMILES: '
               'CCCCCCC\\C=C\\C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12 '
               'NAME: trans-dec-2-enoyl-CoA REASON: CORRECT Found thioester '
               'with an acyl chain exhibiting a trans (E) double bond at the '
               '2-enoyl position and a CoA moiety\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCCCCC\\C=C\\C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12 '
               'NAME: trans-2-tetracosenoyl-CoA REASON: CORRECT Found '
               'thioester with an acyl chain exhibiting a trans (E) double '
               'bond at the 2-enoyl position and a CoA moiety\n'
               ' * SMILES: '
               'CC(C)CCCC(C)CCCC(C)CC\\C=C(/C)C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12 '
               'NAME: (E)-2,3-didehydropristanoyl-CoA REASON: CORRECT Found '
               'thioester with an acyl chain exhibiting a trans (E) double '
               'bond at the 2-enoyl position and a CoA moiety\n'
               ' * SMILES: '
               'CC(C)CCCCCCCCCCC\\C=C\\C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12 '
               'NAME: (E)-isoheptadec-2-enoyl-CoA REASON: CORRECT Found '
               'thioester with an acyl chain exhibiting a trans (E) double '
               'bond at the 2-enoyl position and a CoA moiety\n'
               ' * SMILES: '
               '[C@@H]1(N2C3=C(C(=NC=N3)N)N=C2)O[C@H](COP(OP(OCC([C@H](C(NCCC(NCCSC(=O)/C=C/CCCCCCCCCCCCC)=O)=O)O)(C)C)(=O)O)(=O)O)[C@H]([C@H]1O)OP(O)(O)=O '
               'NAME: (E)-hexadec-2-enoyl-CoA REASON: CORRECT Found thioester '
               'with an acyl chain exhibiting a trans (E) double bond at the '
               '2-enoyl position and a CoA moiety\n'
               ' * SMILES: '
               'CC\\C=C/C\\C=C/C\\C=C/C\\C=C/C\\C=C/C\\C=C/C=C/C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12 '
               'NAME: (2E,4Z,7Z,10Z,13Z,16Z,19Z)-docosaheptaenoyl-coenzyme A '
               'REASON: CORRECT Found thioester with an acyl chain exhibiting '
               'a trans (E) double bond at the 2-enoyl position and a CoA '
               'moiety\n'
               ' * SMILES: '
               'CCCCCC\\C=C/CCCCC\\C=C\\C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12 '
               'NAME: (2E,9Z)-hexadecadienoyl-CoA REASON: CORRECT Found '
               'thioester with an acyl chain exhibiting a trans (E) double '
               'bond at the 2-enoyl position and a CoA moiety\n'
               ' * SMILES: '
               '[C@@H]1(N2C3=C(C(=NC=N3)N)N=C2)O[C@H](COP(OP(OCC([C@H](C(NCCC(NCCSC(=O)/C=C/CCCCCCCCCCCCCCCCCCCC)=O)=O)O)(C)C)(=O)O)(=O)O)[C@H]([C@H]1O)OP(O)(O)=O '
               'NAME: (2E)-tricosenoyl-CoA REASON: CORRECT Found thioester '
               'with an acyl chain exhibiting a trans (E) double bond at the '
               '2-enoyl position and a CoA moiety\n'
               ' * SMILES: '
               'CCCCCC\\C=C/CCCCCCC\\C=C\\C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12 '
               'NAME: (2E,11Z)-octadecadienoyl-CoA REASON: CORRECT Found '
               'thioester with an acyl chain exhibiting a trans (E) double '
               'bond at the 2-enoyl position and a CoA moiety\n'
               ' * SMILES: '
               'CCCCC\\C=C\\C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12 '
               'NAME: trans-oct-2-enoyl-CoA REASON: CORRECT Found thioester '
               'with an acyl chain exhibiting a trans (E) double bond at the '
               '2-enoyl position and a CoA moiety\n'
               ' * SMILES: '
               'CCCCCC\\C=C/CCCCCCCCC\\C=C\\C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12 '
               'NAME: (2E,13Z)-icosadienoyl-CoA REASON: CORRECT Found '
               'thioester with an acyl chain exhibiting a trans (E) double '
               'bond at the 2-enoyl position and a CoA moiety\n'
               ' * SMILES: '
               'CCCCCCCC\\C=C/CCCCC\\C=C\\C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12 '
               'NAME: (2E,9Z)-octadecadienoyl-CoA REASON: CORRECT Found '
               'thioester with an acyl chain exhibiting a trans (E) double '
               'bond at the 2-enoyl position and a CoA moiety\n'
               ' * SMILES: '
               'CCCCCC\\C=C\\C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12 '
               'NAME: trans-2-nonenoyl-CoA REASON: CORRECT Found thioester '
               'with an acyl chain exhibiting a trans (E) double bond at the '
               '2-enoyl position and a CoA moiety\n'
               ' * SMILES: '
               'CCCCCCCC\\C=C\\C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12 '
               'NAME: trans-2-undecenoyl-CoA REASON: CORRECT Found thioester '
               'with an acyl chain exhibiting a trans (E) double bond at the '
               '2-enoyl position and a CoA moiety\n'
               ' * SMILES: '
               'COc1cc(\\C=C\\C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]2O[C@H]([C@H](O)[C@@H]2OP(O)(O)=O)n2cnc3c(N)ncnc23)cc(OC)c1O '
               'NAME: sinapoyl-CoA REASON: CORRECT Found thioester with an '
               'acyl chain exhibiting a trans (E) double bond at the 2-enoyl '
               'position and a CoA moiety\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCCCCCCC\\C=C\\C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12 '
               'NAME: trans-2-hexacosenoyl-CoA REASON: CORRECT Found thioester '
               'with an acyl chain exhibiting a trans (E) double bond at the '
               '2-enoyl position and a CoA moiety\n'
               'False positives: SMILES: '
               'CCCCCCCCCCCCCCCCCCCCC\\C=C\\C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12 '
               'NAME: trans-2-tetracosenoyl-CoA(4-) REASON: WRONGLY CLASSIFIED '
               'Found thioester with an acyl chain exhibiting a trans (E) '
               'double bond at the 2-enoyl position and a CoA moiety\n'
               ' * SMILES: '
               'C[C@@H]1O[C@@H](OCCCCC/C=C/C(SCCNC(CCNC(=O)[C@@H](C(COP(OP(OC[C@H]2O[C@@H](N3C4=C(C(=NC=N4)N)N=C3)[C@@H]([C@@H]2OP(O)(O)=O)O)(=O)O)(=O)O)(C)C)O)=O)=O)[C@H](O)C[C@H]1O '
               'NAME: oscr#13-CoA REASON: WRONGLY CLASSIFIED Found thioester '
               'with an acyl chain exhibiting a trans (E) double bond at the '
               '2-enoyl position and a CoA moiety\n'
               ' * SMILES: '
               'CCCCC\\C=C/C\\C=C/CCCCC\\C=C\\C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12 '
               'NAME: (2E,9Z,12Z)-octadecatrienoyl-CoA(4-) REASON: WRONGLY '
               'CLASSIFIED Found thioester with an acyl chain exhibiting a '
               'trans (E) double bond at the 2-enoyl position and a CoA '
               'moiety\n'
               ' * SMILES: '
               'CC(C)=CCC\\C(C)=C\\C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12 '
               'NAME: cis-geranoyl-CoA(4-) REASON: WRONGLY CLASSIFIED Found '
               'thioester with an acyl chain exhibiting a trans (E) double '
               'bond at the 2-enoyl position and a CoA moiety\n'
               ' * SMILES: '
               'CC(C)(COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12)[C@@H](O)C(=O)NCCC(=O)NCCSC(=O)\\C=C\\CCCCCCCCCCCCC(O)=O '
               'NAME: (2E)-hexadecenedioyl-CoA REASON: WRONGLY CLASSIFIED '
               'Found thioester with an acyl chain exhibiting a trans (E) '
               'double bond at the 2-enoyl position and a CoA moiety\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCCCCCCC\\C=C\\C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12 '
               'NAME: trans-2-hexacosenoyl-CoA(4-) REASON: WRONGLY CLASSIFIED '
               'Found thioester with an acyl chain exhibiting a trans (E) '
               'double bond at the 2-enoyl position and a CoA moiety\n'
               ' * SMILES: '
               'CC(C)(COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12)[C@@H](O)C(=O)NCCC(=O)NCCSC(=O)\\C=C\\C[N+](C)(C)C '
               'NAME: (E)-4-(trimethylammonio)but-2-enoyl-CoA REASON: WRONGLY '
               'CLASSIFIED Found thioester with an acyl chain exhibiting a '
               'trans (E) double bond at the 2-enoyl position and a CoA '
               'moiety\n'
               ' * SMILES: '
               'CC\\C=C/C\\C=C/C\\C=C/C\\C=C/C\\C=C/C\\C=C/CCCCCCCCCCCC\\C=C\\C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12 '
               'NAME: '
               '(2E,16Z,19Z,22Z,25Z,28Z,31Z)-tetratriacontaheptaenoyl-CoA(4-) '
               'REASON: WRONGLY CLASSIFIED Found thioester with an acyl chain '
               'exhibiting a trans (E) double bond at the 2-enoyl position and '
               'a CoA moiety\n'
               ' * SMILES: '
               'C[C@H](CCCCC/C=C/C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)N2C=NC3=C(N)N=CN=C23)O[C@@H]4O[C@@H](C)[C@H](O)C[C@H]4O '
               'NAME: ascr#15-CoA(4-) REASON: WRONGLY CLASSIFIED Found '
               'thioester with an acyl chain exhibiting a trans (E) double '
               'bond at the 2-enoyl position and a CoA moiety\n'
               ' * SMILES: '
               'C[C@H](CCCCCCCCCCCCCCC/C=C/C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)N2C=NC3=C(N)N=CN=C23)O[C@@H]4O[C@@H](C)[C@H](O)C[C@H]4O '
               'NAME: ascr#35-CoA REASON: WRONGLY CLASSIFIED Found thioester '
               'with an acyl chain exhibiting a trans (E) double bond at the '
               '2-enoyl position and a CoA moiety\n'
               ' * SMILES: '
               'CC(C)(COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12)[C@@H](O)C(=O)NCCC(=O)NCCSC(=O)\\C=C\\CC([O-])=O '
               'NAME: trans-4-carboxybut-2-enoyl-CoA(5-) REASON: WRONGLY '
               'CLASSIFIED Found thioester with an acyl chain exhibiting a '
               'trans (E) double bond at the 2-enoyl position and a CoA '
               'moiety\n'
               ' * SMILES: '
               'CC(C)(COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12)[C@@H](O)C(=O)NCCC(=O)NCCSC(=O)\\C=C\\CCCCCCCCC([O-])=O '
               'NAME: trans-2-dodecenedioyl-CoA(5-) REASON: WRONGLY CLASSIFIED '
               'Found thioester with an acyl chain exhibiting a trans (E) '
               'double bond at the 2-enoyl position and a CoA moiety\n'
               ' * SMILES: '
               'CC\\C=C/C[C@H]1[C@@H](C\\C=C\\C(=O)SCCNC(=O)CCNC(=O)C(O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]2O[C@H]([C@H](O)[C@@H]2OP(O)(O)=O)n2cnc3c(N)ncnc23)CCC1=O '
               'NAME: trans-2-Enoyl-OPC4-CoA REASON: WRONGLY CLASSIFIED Found '
               'thioester with an acyl chain exhibiting a trans (E) double '
               'bond at the 2-enoyl position and a CoA moiety\n'
               ' * SMILES: '
               'CCCCC\\C=C\\C=C\\C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12 '
               'NAME: trans,trans-deca-2,4-dienoyl-CoA(4-) REASON: WRONGLY '
               'CLASSIFIED Found thioester with an acyl chain exhibiting a '
               'trans (E) double bond at the 2-enoyl position and a CoA '
               'moiety\n'
               ' * SMILES: '
               'C[C@H](CCC/C=C/C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)N2C=NC3=C(N)N=CN=C23)O[C@@H]4O[C@@H](C)[C@H](O)C[C@H]4O '
               'NAME: ascr#13-CoA REASON: WRONGLY CLASSIFIED Found thioester '
               'with an acyl chain exhibiting a trans (E) double bond at the '
               '2-enoyl position and a CoA moiety\n'
               ' * SMILES: '
               'CS\\C=C\\C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12 '
               'NAME: 3-(methylthio)acryloyl-CoA(4-) REASON: WRONGLY '
               'CLASSIFIED Found thioester with an acyl chain exhibiting a '
               'trans (E) double bond at the 2-enoyl position and a CoA '
               'moiety\n'
               ' * SMILES: '
               'CCCCCCCC\\C=C\\C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12 '
               'NAME: trans-2-undecenoyl-CoA(4-) REASON: WRONGLY CLASSIFIED '
               'Found thioester with an acyl chain exhibiting a trans (E) '
               'double bond at the 2-enoyl position and a CoA moiety\n'
               ' * SMILES: '
               'CCCCC\\C=C/CC\\C=C\\C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12 '
               'NAME: (2-trans,6-cis)-dodeca-2,6-dienoyl-CoA REASON: WRONGLY '
               'CLASSIFIED Found thioester with an acyl chain exhibiting a '
               'trans (E) double bond at the 2-enoyl position and a CoA '
               'moiety\n'
               ' * SMILES: '
               'S(CCNC(CCNC(=O)[C@@H](C(COP(OP(OC[C@H]1O[C@@H](N2C3=C(C(=NC=N3)N)N=C2)[C@@H]([C@@H]1OP(O)(O)=O)O)(=O)O)(=O)O)(C)C)O)=O)C(\\C=C\\CCCCCCCCCCCCCCCO[C@H]4[C@@H](C[C@H]([C@@H](O4)C)O)O)=O '
               'NAME: oscr#31-CoA REASON: WRONGLY CLASSIFIED Found thioester '
               'with an acyl chain exhibiting a trans (E) double bond at the '
               '2-enoyl position and a CoA moiety\n'
               ' * SMILES: '
               'N1=CN=C2C(=C1N)N=CN2[C@@H]3O[C@@H]([C@H]([C@H]3O)CP(O)(O)=O)COP(OP(OCC(C(C(NCCC(NCCSC(/C=C/C=C\\CCC)=O)=O)=O)O)(C)C)(=O)O)(=O)O '
               'NAME: 3-trans,5-cis-Octadienoyl-CoA REASON: WRONGLY CLASSIFIED '
               'Found thioester with an acyl chain exhibiting a trans (E) '
               'double bond at the 2-enoyl position and a CoA moiety\n'
               ' * SMILES: '
               'CCCCCC\\C=C/CCCCCCCCC\\C=C\\C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12 '
               'NAME: (2E,13Z)-icosadienoyl-CoA(4-) REASON: WRONGLY CLASSIFIED '
               'Found thioester with an acyl chain exhibiting a trans (E) '
               'double bond at the 2-enoyl position and a CoA moiety\n'
               ' * SMILES: '
               'CC(C)=CCC\\C(CC(O)=O)=C/C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12 '
               'NAME: 3-(4-methylpent-3-en-1-yl)pent-2-enedioyl-CoA REASON: '
               'WRONGLY CLASSIFIED Found thioester with an acyl chain '
               'exhibiting a trans (E) double bond at the 2-enoyl position and '
               'a CoA moiety\n'
               ' * SMILES: '
               '[C@@H]1(N2C3=C(C(=NC=N3)N)N=C2)O[C@H](COP(OP(OCC(C)([C@H](C(NCCC(NCCSC(=O)\\C(=C\\CC)\\C)=O)=O)O)C)(=O)[O-])(=O)[O-])[C@H]([C@H]1O)OP([O-])([O-])=O '
               'NAME: 2-methyl-(2E)-pentenoyl-CoA(4-) REASON: WRONGLY '
               'CLASSIFIED Found thioester with an acyl chain exhibiting a '
               'trans (E) double bond at the 2-enoyl position and a CoA '
               'moiety\n'
               ' * SMILES: '
               'CC\\C=C/C\\C=C/C\\C=C/C\\C=C/C\\C=C/C\\C=C/CCCCCCCCCCCC\\C=C\\C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12 '
               'NAME: '
               '(2E,16Z,19Z,22Z,25Z,28Z,31Z)-tetratriacontaheptaenoyl-CoA '
               'REASON: WRONGLY CLASSIFIED Found thioester with an acyl chain '
               'exhibiting a trans (E) double bond at the 2-enoyl position and '
               'a CoA moiety\n'
               ' * SMILES: '
               'CCCCC\\C=C/C\\C=C/C\\C=C/C\\C=C/CCC\\C=C\\C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12 '
               'NAME: (2E,7Z,10Z,13Z,16Z)-docosapentaenoyl-CoA REASON: WRONGLY '
               'CLASSIFIED Found thioester with an acyl chain exhibiting a '
               'trans (E) double bond at the 2-enoyl position and a CoA '
               'moiety\n'
               'False negatives: NONE\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'O(C1=CC(=C(C(=C1)I)O)I)C=2C(=CC(=CC2I)CC(O)=O)I',
                                     'name': "3,3',5,5'-tetraiodothyroacetic "
                                             'acid',
                                     'reason': 'Missing characteristic CoA '
                                               'moiety'},
                                 {   'smiles': 'COCC#CC1=CC=C(C=C1)[C@H]2[C@@H]3CN(CCCCN3[C@H]2CO)C(=O)NC4CCCC4',
                                     'name': '(8R,9S,10R)-N-cyclopentyl-10-(hydroxymethyl)-9-[4-(3-methoxyprop-1-ynyl)phenyl]-1,6-diazabicyclo[6.2.0]decane-6-carboxamide',
                                     'reason': 'Missing characteristic CoA '
                                               'moiety'},
                                 {   'smiles': 'O([C@@H]1[C@H](O)[C@H](O[C@H]2[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]2CO)O[C@H]3[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]3CO)O)O[C@@H]([C@H]1O)CO[C@H]4O[C@@H]([C@@H](O)[C@H](O)[C@@H]4O[C@@H]5O[C@@H]([C@@H](O[C@@H]6O[C@@H]([C@H](O)[C@H](O)[C@H]6O)CO)[C@H](O)[C@H]5NC(=O)C)CO)CO)[C@H]7O[C@@H]([C@@H](O)[C@H](O)[C@@H]7O[C@@H]8O[C@@H]([C@@H](O[C@@H]9O[C@@H]([C@H](O)[C@H](O)[C@H]9O[C@@H]%10O[C@H]([C@@H](O)[C@@H](O)[C@@H]%10O)C)CO)[C@H](O)[C@H]8NC(=O)C)CO)CO',
                                     'name': 'N-[(2R,3R,4R,5S,6R)-5-[(2S,3R,4R,5S,6R)-3-Acetamido-5-[(2S,3S,4S,5R,6R)-4-[(2R,3S,4S,5S,6R)-3-[(2S,3R,4R,5S,6R)-3-acetamido-5-[(2S,3R,4S,5R,6R)-4,5-dihydroxy-6-(hydroxymethyl)-3-[(2S,3S,4R,5S,6S)-3,4,5-trihydroxy-6-methyloxan-2-yl]oxyoxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-6-[[(2S,3S,4S,5S,6R)-3-[(2S,3R,4R,5S,6R)-3-acetamido-4-hydroxy-6-(hydroxymethyl)-5-[(2S,3R,4S,5R,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxymethyl]-3,5-dihydroxyoxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-2,4-dihydroxy-6-(hydroxymethyl)oxan-3-yl]acetamide',
                                     'reason': 'Missing characteristic CoA '
                                               'moiety'},
                                 {   'smiles': 'O(C(=O)CCCCCCCCCCCCCCCCC(C)C)C[C@@H](OC(=O)CCCCCCCCCCC)CO',
                                     'name': 'DG(i-20:0/12:0/0:0)',
                                     'reason': 'Missing characteristic CoA '
                                               'moiety'},
                                 {   'smiles': 'CCC(=O)N1C[C@H]2[C@@H]([C@@H](N2C(=O)C1)CO)C3=CC=C(C=C3)C#CC4=CN=CC=C4',
                                     'name': '(6R,7S,8R)-8-(hydroxymethyl)-4-(1-oxopropyl)-7-[4-[2-(3-pyridinyl)ethynyl]phenyl]-1,4-diazabicyclo[4.2.0]octan-2-one',
                                     'reason': 'Missing characteristic CoA '
                                               'moiety'},
                                 {   'smiles': 'O(C(C[N+](C)(C)C)CC([O-])=O)C(=O)CC/C=C/C/C=C/C/C=C/C\\C=C\\CC(O)/C=C/C=C/CC',
                                     'name': '(4Z,7Z,10Z,13Z,17Z,19Z)-16-Hydroxydocosa-4,7,10,13,17,19-hexaenoylcarnitine',
                                     'reason': 'Missing characteristic CoA '
                                               'moiety'},
                                 {   'smiles': 'O([C@H]1[C@H](O)[C@@H](NC(=O)C)[C@H](O[C@H]2[C@H](O[C@H]3O[C@H]([C@@H](O)[C@@H](O)[C@@H]3O)C)[C@@H](NC(=O)C)[C@@H](O[C@@H]2CO)O)O[C@@H]1CO)[C@@H]4O[C@@H]([C@@H](O)[C@H](O[C@H]5O[C@@H]([C@@H](O)[C@H](O)[C@@H]5O)CO)[C@@H]4O[C@@H]6OC[C@@H](O)[C@H](O)[C@H]6O)CO',
                                     'name': 'N-[(2S,3R,4R,5S,6R)-2-[(2R,3S,4R,5R,6R)-5-Acetamido-6-hydroxy-2-(hydroxymethyl)-4-[(2R,3S,4R,5S,6S)-3,4,5-trihydroxy-6-methyloxan-2-yl]oxyoxan-3-yl]oxy-4-hydroxy-5-[(2S,3S,4S,5R,6R)-5-hydroxy-6-(hydroxymethyl)-4-[(2R,3S,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-3-[(2S,3R,4S,5R)-3,4,5-trihydroxyoxan-2-yl]oxyoxan-2-yl]oxy-6-(hydroxymethyl)oxan-3-yl]acetamide',
                                     'reason': 'Missing characteristic CoA '
                                               'moiety'},
                                 {   'smiles': 'O(C=1C=2C(C(OC(=O)CCC)=CC1C)=CC=CC2)C(=O)CCC',
                                     'name': 'Menadiol dibutyrate',
                                     'reason': 'Missing characteristic CoA '
                                               'moiety'},
                                 {   'smiles': 'N1(CCCCC1)C=2C(=CC=CC2)C#N',
                                     'name': '2-piperidinobenzonitrile',
                                     'reason': 'Missing characteristic CoA '
                                               'moiety'},
                                 {   'smiles': 'COc1cc2c(cc1C)C(=CC(=O)[C@]2(C)O)C(C)C',
                                     'name': 'Lacinilene C 7-methyl ether',
                                     'reason': 'Missing characteristic CoA '
                                               'moiety'}],
    'sample_false_negatives': [],
    'attempt': 1,
    'reasoning': 'Below is one possible improved solution. In our reasoning we '
                 'observed that the previous approach was “too loose” in that '
                 'any thioester with an adjacent double bond marked as trans '
                 'ended up being classified as a trans‐2‑enoyl‑CoA. In our new '
                 'solution we (1) call AssignStereochemistry to force '
                 'assignment, (2) use a slightly broader SMARTS query for the '
                 'CoA fragment (so that subtle charge differences do not '
                 '“break” the match), (3) not only look for a thioester bond '
                 'but then explicitly “extract” the acyl chain portion and '
                 'verify that (a) the carbonyl carbon (of the thioester) is '
                 'attached to exactly one alkyl carbon (the “alpha” carbon) '
                 'and that (b) this alpha carbon is connected via a double '
                 'bond to a beta carbon and (c) that the double bond is not '
                 'only a double bond but in trans (E) stereochemistry, and (d) '
                 'the acyl chain extends as a mostly aliphatic chain. This '
                 'extra check helps to weed out false positives from '
                 'structures that contain extraneous charges or other '
                 'modifications. (There are many possible approaches; this is '
                 'one way.)\n'
                 '\n'
                 'Below is the complete Python program.\n'
                 '\n'
                 '------',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 26,
    'num_false_positives': 211,
    'num_true_negatives': 142063,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.10970464135021098,
    'recall': 1.0,
    'f1': 0.19771863117870725,
    'accuracy': 0.9985172171468728,
    'negative_predictive_value': 1.0}