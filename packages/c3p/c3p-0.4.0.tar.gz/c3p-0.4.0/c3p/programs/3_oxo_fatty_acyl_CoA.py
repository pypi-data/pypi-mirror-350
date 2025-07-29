"""
Classifies: CHEBI:15489 3-oxo-fatty acyl-CoA
"""
#!/usr/bin/env python3
"""
Classifies: 3-oxo-fatty acyl-CoA
An oxo fatty acyl-CoA that results from the formal condensation of the thiol group of coenzyme A 
with the carboxy group of any 3-oxo-fatty acid.
The idea is to find a fatty acyl thioester fragment of the form:
   R–C(=O)–C(R’)–C(=O)S– (where the C(R’) is the 3-oxo carbon)
and then to ensure that the C(R’) is not additionally substituted by an extra carboxyl group.
We also require the presence of the typical CoA adenine fragment.
"""
from rdkit import Chem
from rdkit.Chem import rdMolDescriptors

def is_3_oxo_fatty_acyl_CoA(smiles: str):
    """
    Determines if a molecule is a 3-oxo-fatty acyl-CoA based on its SMILES string.
    
    Criteria:
      1. The molecule must be valid and not contain explicit deprotonated oxygens (i.e. [O-])
         so that we only classify neutral CoA derivatives.
      2. The molecule should contain a 3-oxo fatty acyl thioester fragment. We define a SMARTS pattern
         for a fragment of the form R–C(=O)–C(R’)–C(=O)S, where the central carbon (C(R’)) must be
         aliphatic. (The previous version’s pattern was too loose.)
      3. In any such match the middle carbon must not have an extra carboxyl substituent.
      4. The molecule must also contain a Coenzyme A signature (here we require the adenine fragment).
    
    Args:
      smiles (str): SMILES string representing the molecule.
    
    Returns:
      bool: True if the molecule is classified as a 3-oxo-fatty acyl-CoA, False otherwise.
      str: Explanation for the classification.
    """
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
    
    # Exclude molecules that have explicit deprotonated oxygens (e.g. [O-])
    if "[O-]" in smiles:
        return False, "Contains deprotonated oxygens; expected neutral CoA"
    
    # First, check that the molecule contains a CoA adenine fragment.
    coa_pattern = Chem.MolFromSmarts("n1cnc2ncnc(c12)")
    if not mol.HasSubstructMatch(coa_pattern):
        return False, "Does not contain a Coenzyme A adenine fragment"
    
    # Define a refined SMARTS for the 3-oxo fatty acyl thioester fragment.
    # This pattern looks for a fragment of the form: [#6]-C(=O)-[#6X4]-C(=O)S
    # where the atom tagged as [#6X4] (the middle carbon) should be aliphatic.
    frag_smarts = "[#6:1]-C(=O)-[#6X4:2]-C(=O)S"
    frag_pattern = Chem.MolFromSmarts(frag_smarts)
    matches = mol.GetSubstructMatches(frag_pattern)
    if not matches:
        return False, "Does not contain a 3-oxo fatty acyl thioester substructure"
    
    # For each match, we want to ensure that the middle carbon (tag 2) is not substituted
    # with an extra carboxyl group (e.g. -C(=O)O). In a proper 3-oxo fatty acyl moiety the middle
    # carbon is only part of the two carbonyls.
    #
    # We'll get the middle atom from the match and look at its neighbors (excluding those that
    # are part of the fragment match). If one of them is a carbon that is in a carbonyl (i.e. has a 
    # double bond from that carbon to oxygen), we consider that an extra carboxyl.
    def middle_has_extra_carboxyl(mid_atom, exclude_idxs):
        # Iterate over neighbors of the middle atom that are not in the exclude list.
        for nbr in mid_atom.GetNeighbors():
            if nbr.GetIdx() in exclude_idxs:
                continue
            # Check: if the neighbor is a carbon that itself is doubly bonded to oxygen,
            # then count that as a carboxyl substituent.
            if nbr.GetAtomicNum() == 6:
                for bond in nbr.GetBonds():
                    # bond between nbr and an oxygen that is a double bond
                    if bond.GetBondType() == Chem.BondType.DOUBLE:
                        other = bond.GetOtherAtom(nbr)
                        if other.GetAtomicNum() == 8:
                            return True
        return False

    valid_match_found = False
    for match in matches:
        # match is a tuple of atom indices corresponding to the SMARTS pattern:
        # index0: the first carbon (R group), index1: its carbonyl carbon, 
        # index2: the middle (aliphatic) carbon, index3: the carbonyl carbon of the thioester.
        mid_idx = match[2]
        # Exclude the two atoms that are part of the acyl fragment (index1 and index3)
        exclude = {match[1], match[3]}
        mid_atom = mol.GetAtomWithIdx(mid_idx)
        if middle_has_extra_carboxyl(mid_atom, exclude):
            continue
        else:
            valid_match_found = True
            break

    if not valid_match_found:
        return False, "Contains an acyl thioester-like fragment but with extra carboxyl substitution (e.g. malonyl-type) rather than a 3-oxo fatty acyl group"
    
    # Passed all checks:
    return True, "Contains a valid 3-oxo fatty acyl thioester linked to a Coenzyme A moiety"

# Example usage:
if __name__ == "__main__":
    # Example SMILES for 3-oxoadipyl-CoA:
    smiles_example = ("CC(C)(COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1"
                      "OP(O)(O)=O)n1cnc2c(N)ncnc12)[C@@H](O)C(=O)NCCC(=O)NCCSC(=O)"
                      "CC(=O)CCC(O)=O")
    result, reason = is_3_oxo_fatty_acyl_CoA(smiles_example)
    print(result, reason)


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:15489',
                          'name': '3-oxo-fatty acyl-CoA',
                          'definition': 'An oxo fatty acyl-CoA that results '
                                        'from the formal condensation of the '
                                        'thiol group of coenzyme A with the '
                                        'carboxy group of any 3-oxo-fatty '
                                        'acid..',
                          'parents': ['CHEBI:61903'],
                          'xrefs': [   'KEGG:C00264',
                                       'PMID:11315193',
                                       'PMID:11418601',
                                       'PMID:11879205',
                                       'PMID:7957058',
                                       'PMID:8541311'],
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
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 3,
                                                 4,
                                                 3,
                                                 3,
                                                 3,
                                                 4,
                                                 5,
                                                 5,
                                                 6,
                                                 6,
                                                 7,
                                                 2,
                                                 0,
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
                                                 3,
                                                 2,
                                                 3,
                                                 3,
                                                 0,
                                                 1,
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1],
                           'max_indent': 7,
                           'imports': [   'from rdkit import Chem',
                                          'from rdkit.Chem import '
                                          'rdMolDescriptors'],
                           'imports_count': 2,
                           'methods_called': [   'GetBondType',
                                                 'GetNeighbors',
                                                 'MolFromSmiles',
                                                 'HasSubstructMatch',
                                                 'GetOtherAtom',
                                                 'GetSubstructMatches',
                                                 'MolFromSmarts',
                                                 'GetIdx',
                                                 'GetBonds',
                                                 'GetAtomicNum',
                                                 'GetAtomWithIdx'],
                           'methods_called_count': 11,
                           'smarts_strings': ['frag_smarts', 'n1cnc2ncnc(c12)'],
                           'smarts_strings_count': 2,
                           'defs': [   'is_3_oxo_fatty_acyl_CoA(smiles: str):',
                                       'middle_has_extra_carboxyl(mid_atom, '
                                       'exclude_idxs):'],
                           'defs_count': 2,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "Contains deprotonated '
                                          'oxygens; expected neutral CoA"',
                                          'False, "Does not contain a Coenzyme '
                                          'A adenine fragment"',
                                          'False, "Does not contain a 3-oxo '
                                          'fatty acyl thioester substructure"',
                                          'True',
                                          'False',
                                          'False, "Contains an acyl '
                                          'thioester-like fragment but with '
                                          'extra carboxyl substitution (e.g. '
                                          'malonyl-type) rather than a 3-oxo '
                                          'fatty acyl group"',
                                          'True, "Contains a valid 3-oxo fatty '
                                          'acyl thioester linked to a Coenzyme '
                                          'A moiety"'],
                           'returns_count': 8,
                           'complexity': 6.478889830934489},
    'message': '\n'
               'Attempt failed: F1 score of 0.6555555555555556 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: '
               'CC(C)(COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12)[C@@H](O)C(=O)NCCC(=O)NCCSC(=O)CC(=O)CCC(O)=O '
               'NAME: 3-oxoadipyl-CoA REASON: CORRECT Contains a 3-oxo fatty '
               'acyl thioester linked to a coenzyme A moiety\n'
               ' * SMILES: '
               'CCCCCCCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12 '
               'NAME: 3-oxotetradecanoyl-CoA REASON: CORRECT Contains a 3-oxo '
               'fatty acyl thioester linked to a coenzyme A moiety\n'
               ' * SMILES: '
               'CC(C)CCCCCCCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12 '
               'NAME: 3-oxoisoheptadecanoyl-CoA REASON: CORRECT Contains a '
               '3-oxo fatty acyl thioester linked to a coenzyme A moiety\n'
               ' * SMILES: '
               'CC\\C=C/C\\C=C/C\\C=C/C\\C=C/C\\C=C/CCCCCCCCCCCCCCCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12 '
               'NAME: (23Z,26Z,29Z,32Z,35Z)-3-oxooctatriacontapentaenoyl-CoA '
               'REASON: CORRECT Contains a 3-oxo fatty acyl thioester linked '
               'to a coenzyme A moiety\n'
               ' * SMILES: '
               'CCCCC\\C=C/C\\C=C/CCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12 '
               'NAME: (9Z,12Z)-3-oxolinoleoyl-CoA REASON: CORRECT Contains a '
               '3-oxo fatty acyl thioester linked to a coenzyme A moiety\n'
               ' * SMILES: '
               'CCCCC\\C=C/C\\C=C/C\\C=C/C\\C=C/CCCCCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12 '
               'NAME: (13Z,16Z,19Z,22Z)-3-oxooctacosatetraenoyl-CoA REASON: '
               'CORRECT Contains a 3-oxo fatty acyl thioester linked to a '
               'coenzyme A moiety\n'
               ' * SMILES: '
               'CCCCCC\\C=C/CCCCCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12 '
               'NAME: (13Z)-3-oxoicosenoyl-CoA REASON: CORRECT Contains a '
               '3-oxo fatty acyl thioester linked to a coenzyme A moiety\n'
               ' * SMILES: '
               'CCCCC\\C=C/C\\C=C/C\\C=C/CCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12 '
               'NAME: (10Z,13Z,16Z)-3-oxodocosatrienoyl-CoA REASON: CORRECT '
               'Contains a 3-oxo fatty acyl thioester linked to a coenzyme A '
               'moiety\n'
               ' * SMILES: '
               'CC(C)CCCC(C)CCCC(C)CCC(=O)C(C)C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12 '
               'NAME: 3-oxopristanoyl-CoA REASON: CORRECT Contains a 3-oxo '
               'fatty acyl thioester linked to a coenzyme A moiety\n'
               ' * SMILES: '
               'CCCC\\C=C/C\\C=C/C\\C=C/CCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12 '
               'NAME: (9Z,12Z,15Z)-3-oxoicosatrienoyl-CoA REASON: CORRECT '
               'Contains a 3-oxo fatty acyl thioester linked to a coenzyme A '
               'moiety\n'
               ' * SMILES: '
               'CC\\C=C/C\\C=C/C\\C=C/C\\C=C/C\\C=C/CCCCCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12 '
               'NAME: (13Z,16Z,19Z,22Z,25Z)-3-oxooctacosapentaenoyl-CoA '
               'REASON: CORRECT Contains a 3-oxo fatty acyl thioester linked '
               'to a coenzyme A moiety\n'
               ' * SMILES: '
               'CCCCC\\C=C/C\\C=C/CCCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12 '
               'NAME: (11Z,14Z)-3-oxoicosa-11,14-dienoyl-CoA REASON: CORRECT '
               'Contains a 3-oxo fatty acyl thioester linked to a coenzyme A '
               'moiety\n'
               ' * SMILES: '
               'CC(=C)C1CCC(C(=O)C1)C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12 '
               'NAME: 4-isopropenyl-2-oxocyclohexane-1-carbonyl-CoA REASON: '
               'CORRECT Contains a 3-oxo fatty acyl thioester linked to a '
               'coenzyme A moiety\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCCCCCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)N1C=NC2=C1N=CN=C2N '
               'NAME: 3-oxo-octacosanoyl-CoA REASON: CORRECT Contains a 3-oxo '
               'fatty acyl thioester linked to a coenzyme A moiety\n'
               ' * SMILES: '
               'CC(C)CCCCCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12 '
               'NAME: 3-oxoisopentadecanoyl-CoA REASON: CORRECT Contains a '
               '3-oxo fatty acyl thioester linked to a coenzyme A moiety\n'
               ' * SMILES: '
               'CC\\C=C/C\\C=C/C\\C=C/CCCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12 '
               'NAME: (11Z,14Z,17Z)-3-oxoicosatrienoyl-CoA REASON: CORRECT '
               'Contains a 3-oxo fatty acyl thioester linked to a coenzyme A '
               'moiety\n'
               ' * SMILES: '
               'CCCCC\\C=C/C\\C=C/C\\C=C/C\\C=C/CCCCCCCCCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12 '
               'NAME: (17Z,20Z,23Z,26Z)-3-oxodotriacontatetraenoyl-CoA REASON: '
               'CORRECT Contains a 3-oxo fatty acyl thioester linked to a '
               'coenzyme A moiety\n'
               ' * SMILES: '
               'CCCC\\C=C/CCCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12 '
               'NAME: (11Z)-3-oxohexadecenoyl-CoA REASON: CORRECT Contains a '
               '3-oxo fatty acyl thioester linked to a coenzyme A moiety\n'
               ' * SMILES: '
               'CCCCC\\C=C/C\\C=C/C\\C=C/C\\C=C/CCCCCCCCCCCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12 '
               'NAME: (19Z,22Z,25Z,28Z)-3-oxotetratriacontatetraenoyl-CoA '
               'REASON: CORRECT Contains a 3-oxo fatty acyl thioester linked '
               'to a coenzyme A moiety\n'
               ' * SMILES: '
               'CCCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12 '
               'NAME: 3-oxodecanoyl-CoA REASON: CORRECT Contains a 3-oxo fatty '
               'acyl thioester linked to a coenzyme A moiety\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12 '
               'NAME: 3-oxotetracosanoyl-CoA REASON: CORRECT Contains a 3-oxo '
               'fatty acyl thioester linked to a coenzyme A moiety\n'
               ' * SMILES: '
               'CC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)N1C=NC2=C1N=CN=C2N '
               'NAME: acetoacetyl-CoA REASON: CORRECT Contains a 3-oxo fatty '
               'acyl thioester linked to a coenzyme A moiety\n'
               ' * SMILES: '
               'CC\\C=C/C\\C=C/C\\C=C/CCCCCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12 '
               'NAME: (13Z,16Z,19Z)-3-oxodocosatrienoyl-CoA REASON: CORRECT '
               'Contains a 3-oxo fatty acyl thioester linked to a coenzyme A '
               'moiety\n'
               ' * SMILES: '
               'CC(C(C)=O)C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12 '
               'NAME: 2-methylacetoacetyl-CoA REASON: CORRECT Contains a 3-oxo '
               'fatty acyl thioester linked to a coenzyme A moiety\n'
               ' * SMILES: '
               'CC\\C=C/C\\C=C/C\\C=C/C\\C=C/C\\C=C/C\\C=C/CCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12 '
               'NAME: (6Z,9Z,12Z,15Z,18Z,21Z)-3-oxotetracosahexaenoyl-CoA '
               'REASON: CORRECT Contains a 3-oxo fatty acyl thioester linked '
               'to a coenzyme A moiety\n'
               'False positives: SMILES: '
               'CC(C(O)=O)C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12 '
               'NAME: methylmalonyl-CoA REASON: WRONGLY CLASSIFIED Contains a '
               '3-oxo fatty acyl thioester linked to a coenzyme A moiety\n'
               ' * SMILES: '
               'C[C@H](CCCCCCCCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)N2C=NC3=C(N)N=CN=C23)O[C@@H]4O[C@@H](C)[C@H](O)C[C@H]4O '
               'NAME: bkas#30-CoA REASON: WRONGLY CLASSIFIED Contains a 3-oxo '
               'fatty acyl thioester linked to a coenzyme A moiety\n'
               ' * SMILES: '
               'S(CCNC(=O)CCNC(=O)C(O)C(COP(OP(OCC1OC(N2C3=NC=NC(N)=C3N=C2)C(O)C1O)(O)=O)(O)=O)(C)C)C(=O)C(C)C(O)=O '
               'NAME: '
               '3-({2-[(3-{[4-({[({[5-(6-amino-9H-purin-9-yl)-3,4-dihydroxyoxolan-2-yl]methoxy}(hydroxy)phosphoryl)oxy](hydroxy)phosphoryl}oxy)-1,2-dihydroxy-3,3-dimethylbutylidene]amino}-1-hydroxypropylidene)amino]ethyl}sulfanyl)-2-methyl-3-oxopropanoic '
               'acid REASON: WRONGLY CLASSIFIED Contains a 3-oxo fatty acyl '
               'thioester linked to a coenzyme A moiety\n'
               ' * SMILES: '
               'C[C@H](CCCCCCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)N2C=NC3=C(N)N=CN=C23)O[C@@H]4O[C@@H](C)[C@H](O)C[C@H]4O '
               'NAME: bkas#26-CoA REASON: WRONGLY CLASSIFIED Contains a 3-oxo '
               'fatty acyl thioester linked to a coenzyme A moiety\n'
               ' * SMILES: '
               'CCC(C(O)=O)C(=O)SCCNC(=O)CCNC(=O)C(O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12 '
               'NAME: Ethylmalonyl-CoA REASON: WRONGLY CLASSIFIED Contains a '
               '3-oxo fatty acyl thioester linked to a coenzyme A moiety\n'
               ' * SMILES: '
               'C[C@@H]1O[C@@H](OCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]2O[C@H]([C@H](O)[C@@H]2OP(O)(O)=O)N3C=NC4=C(N)N=CN=C34)[C@H](O)C[C@H]1O '
               'NAME: bkos#12-CoA REASON: WRONGLY CLASSIFIED Contains a 3-oxo '
               'fatty acyl thioester linked to a coenzyme A moiety\n'
               ' * SMILES: '
               'CC(C)(COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12)[C@@H](O)C(=O)NCCC(=O)NCCSC(=O)CC(=O)CCCCCCCCCCC(O)=O '
               'NAME: 3-oxotetradecanedioyl-CoA REASON: WRONGLY CLASSIFIED '
               'Contains a 3-oxo fatty acyl thioester linked to a coenzyme A '
               'moiety\n'
               ' * SMILES: '
               'CC(C)(COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12)[C@@H](O)C(=O)NCCC(=O)NCCSC(=O)CC(=O)CCCCCCC(O)=O '
               'NAME: 3-oxodecanedioyl-CoA REASON: WRONGLY CLASSIFIED Contains '
               'a 3-oxo fatty acyl thioester linked to a coenzyme A moiety\n'
               ' * SMILES: '
               'S(CCNC(=O)CCNC(=O)C(O)C(COP(OP(OC[C@H]1O[C@@H](N2C3=NC=NC(N)=C3N=C2)[C@H](O)[C@@H]1OP(O)(O)=O)(O)=O)(O)=O)(C)C)C(=O)CC=O '
               'NAME: Malonyl-CoA semialdehyde REASON: WRONGLY CLASSIFIED '
               'Contains a 3-oxo fatty acyl thioester linked to a coenzyme A '
               'moiety\n'
               ' * SMILES: '
               'CC(C)(COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12)[C@@H](O)C(=O)NCCC(=O)NCCSC(=O)CC(=O)C=Cc1ccc(O)cc1 '
               'NAME: (4-coumaroyl)acetyl-CoA REASON: WRONGLY CLASSIFIED '
               'Contains a 3-oxo fatty acyl thioester linked to a coenzyme A '
               'moiety\n'
               ' * SMILES: '
               '[H][C@@](C)(CCC(=O)C(C)C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12)[C@@]1([H])CC[C@@]2([H])[C@]3([H])[C@H](O)C[C@]4([H])C[C@H](O)CC[C@]4(C)[C@@]3([H])CC[C@]12C '
               'NAME: '
               '3alpha,7alpha-dihydroxy-24-oxo-5beta-cholestan-26-oyl-CoA '
               'REASON: WRONGLY CLASSIFIED Contains a 3-oxo fatty acyl '
               'thioester linked to a coenzyme A moiety\n'
               ' * SMILES: '
               'C[C@H](CCCCCCCCCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)N2C=NC3=C(N)N=CN=C23)O[C@@H]4O[C@@H](C)[C@H](O)C[C@H]4O '
               'NAME: bkas#32-CoA REASON: WRONGLY CLASSIFIED Contains a 3-oxo '
               'fatty acyl thioester linked to a coenzyme A moiety\n'
               ' * SMILES: '
               'S(CCNC(=O)CCNC(=O)[C@H](O)C(COP(OP(OC[C@H]1O[C@@H](N2C3=NC=NC(N)=C3N=C2)[C@H](O)[C@@H]1OP(O)(O)=O)(O)=O)(O)=O)(C)C)C(=O)CC(=O)C/C=C/CC(O)=O '
               'NAME: 3-oxo-8-carboxy-5-octenoyl-CoA REASON: WRONGLY '
               'CLASSIFIED Contains a 3-oxo fatty acyl thioester linked to a '
               'coenzyme A moiety\n'
               ' * SMILES: '
               'C[C@H](CCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)N2C=NC3=C(N)N=CN=C23)O[C@@H]4O[C@@H](C)[C@H](O)C[C@H]4O '
               'NAME: bkas#1-CoA REASON: WRONGLY CLASSIFIED Contains a 3-oxo '
               'fatty acyl thioester linked to a coenzyme A moiety\n'
               ' * SMILES: '
               '[C@@H]1(N2C3=C(C(=NC=N3)N)N=C2)O[C@H](COP(OP(OCC(C(C(NCCC(NCCSC(=O)CC(=O)/C=C/C4=CC=C(C(=C4)OC)O)=O)=O)O)(C)C)(=O)O)(=O)O)[C@H]([C@H]1O)OP(O)(O)=O '
               'NAME: trans-feruloylacetyl-CoA REASON: WRONGLY CLASSIFIED '
               'Contains a 3-oxo fatty acyl thioester linked to a coenzyme A '
               'moiety\n'
               ' * SMILES: '
               'C[C@@H]1O[C@@H](OCCCCCCCCCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]2O[C@H]([C@H](O)[C@@H]2OP(O)(O)=O)N3C=NC4=C(N)N=CN=C34)[C@H](O)C[C@H]1O '
               'NAME: bkos#28-CoA REASON: WRONGLY CLASSIFIED Contains a 3-oxo '
               'fatty acyl thioester linked to a coenzyme A moiety\n'
               ' * SMILES: '
               'C[C@H](CCCCCCCCCCCCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)N2C=NC3=C(N)N=CN=C23)O[C@@H]4O[C@@H](C)[C@H](O)C[C@H]4O '
               'NAME: bkas#38-CoA REASON: WRONGLY CLASSIFIED Contains a 3-oxo '
               'fatty acyl thioester linked to a coenzyme A moiety\n'
               ' * SMILES: '
               'C[C@@H](O[C@@H]1O[C@@H](C)[C@H](O)C[C@H]1O)C(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]2O[C@H]([C@H](O)[C@@H]2OP(O)(O)=O)N3C=NC4=C(N)N=CN=C34 '
               'NAME: bkas#9-CoA REASON: WRONGLY CLASSIFIED Contains a 3-oxo '
               'fatty acyl thioester linked to a coenzyme A moiety\n'
               ' * SMILES: '
               'CC(C)(COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)N1C=NC2=C1N=CN=C2N)[C@@H](O)C(=O)NCCC(=O)NCCSC(=O)[C@@H](CC(O)=O)C(=O)C1=CC=CC=C1 '
               'NAME: (S)-2-benzoylsuccinyl-CoA REASON: WRONGLY CLASSIFIED '
               'Contains a 3-oxo fatty acyl thioester linked to a coenzyme A '
               'moiety\n'
               ' * SMILES: '
               'C[C@@H]1O[C@@H](OCCC(=O)CC(SCCNC(CCNC(=O)[C@@H](C(COP(OP(OC[C@H]2O[C@@H](N3C4=C(C(=NC=N4)N)N=C3)[C@@H]([C@@H]2OP(O)(O)=O)O)(=O)O)(=O)O)(C)C)O)=O)=O)[C@H](O)C[C@H]1O '
               'NAME: bkos#9-CoA REASON: WRONGLY CLASSIFIED Contains a 3-oxo '
               'fatty acyl thioester linked to a coenzyme A moiety\n'
               ' * SMILES: '
               'CC(C)(COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12)[C@@H](O)C(=O)NCCC(=O)NCCSC(=O)CC(N)=O '
               'NAME: malonamoyl-CoA REASON: WRONGLY CLASSIFIED Contains a '
               '3-oxo fatty acyl thioester linked to a coenzyme A moiety\n'
               ' * SMILES: '
               'CC(C)(COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12)[C@@H](O)C(=O)NCCC(=O)NCCSC(=O)CC(O)=O '
               'NAME: malonyl-CoA REASON: WRONGLY CLASSIFIED Contains a 3-oxo '
               'fatty acyl thioester linked to a coenzyme A moiety\n'
               ' * SMILES: '
               'COC(=O)CC(=O)SCCNC(=O)CCNC(=O)C(O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12 '
               'NAME: malonyl-CoA methyl ester REASON: WRONGLY CLASSIFIED '
               'Contains a 3-oxo fatty acyl thioester linked to a coenzyme A '
               'moiety\n'
               ' * SMILES: '
               'C[C@H](CCCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)N2C=NC3=C(N)N=CN=C23)O[C@@H]4O[C@@H](C)[C@H](O)C[C@H]4O '
               'NAME: bkas#20-CoA REASON: WRONGLY CLASSIFIED Contains a 3-oxo '
               'fatty acyl thioester linked to a coenzyme A moiety\n'
               ' * SMILES: '
               'CC(C)(COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12)[C@@H](O)C(=O)NCCC(=O)NCCSC(=O)CC(=O)c1ccccc1 '
               'NAME: benzoylacetyl-CoA REASON: WRONGLY CLASSIFIED Contains a '
               '3-oxo fatty acyl thioester linked to a coenzyme A moiety\n'
               'False negatives: NONE\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'O=C1OC[C@@H]2O[C@@H](O[C@@H]3[C@@H](OC(=O)CCCCCCCCCCCCCCC)[C@H](C=CCCCC1)[C@H](CCCCC)[C@@H](C3)O)[C@H](O)[C@H]([C@@H]2O)O',
                                     'name': 'Mucorolactone',
                                     'reason': 'Does not contain a Coenzyme A '
                                               'adenine fragment'},
                                 {   'smiles': 'C[C@@H]1CN[C@H](COC2=C(C=CC(=C2)NC(=O)C3=NC4=CC=CC=C4S3)C(=O)N(C[C@H]1OC)C)C',
                                     'name': 'N-[(5S,6R,9S)-5-methoxy-3,6,9-trimethyl-2-oxo-11-oxa-3,8-diazabicyclo[10.4.0]hexadeca-1(12),13,15-trien-14-yl]-1,3-benzothiazole-2-carboxamide',
                                     'reason': 'Does not contain a Coenzyme A '
                                               'adenine fragment'},
                                 {   'smiles': 'COC1=CC=CC(=C1)C2=CC=C(C=C2)[C@@H]3[C@@H]4CN(CC(=O)N4[C@@H]3CO)C(=O)C5=CN=CC=C5',
                                     'name': '(6R,7R,8S)-8-(hydroxymethyl)-7-[4-(3-methoxyphenyl)phenyl]-4-[oxo(3-pyridinyl)methyl]-1,4-diazabicyclo[4.2.0]octan-2-one',
                                     'reason': 'Does not contain a Coenzyme A '
                                               'adenine fragment'},
                                 {   'smiles': 'C(C(/C=C/C=C/C=C/[C@H](CCCC(O)=O)O)=O)/C=C\\CCCCC',
                                     'name': '12-oxo-6-trans-leukotriene B4',
                                     'reason': 'Does not contain a Coenzyme A '
                                               'adenine fragment'},
                                 {   'smiles': 'O=C1OC(=C(C#C[C@H](COC(=O)C)C)CO)C=C1',
                                     'name': "5'-O-acetylaporpinone A",
                                     'reason': 'Does not contain a Coenzyme A '
                                               'adenine fragment'},
                                 {   'smiles': 'O=C(N1[C@@H](CCC1)C(=O)N[C@@H](CCC(=O)N)C(O)=O)[C@@H](N)[C@H](CC)C',
                                     'name': 'Ile-Pro-Gln',
                                     'reason': 'Does not contain a Coenzyme A '
                                               'adenine fragment'},
                                 {   'smiles': 'O[C@@H]1C=CC=C(CCC(O)=O)[C@@H]1O',
                                     'name': '3-[(5R,6S)-5,6-dihydroxycyclohexa-1,3-dienyl]propanoic '
                                             'acid',
                                     'reason': 'Does not contain a Coenzyme A '
                                               'adenine fragment'},
                                 {   'smiles': 'O=C(OC)/C=C/C(C)(C)C',
                                     'name': '4,4-Dimethyl-pentenoic acid '
                                             'methyl ester',
                                     'reason': 'Does not contain a Coenzyme A '
                                               'adenine fragment'},
                                 {   'smiles': 'CCCCOc1ccc(OCCCN2CCOCC2)cc1',
                                     'name': 'pramocaine',
                                     'reason': 'Does not contain a Coenzyme A '
                                               'adenine fragment'},
                                 {   'smiles': 'OC[C@@H](O)C(=O)[C@H](O)[C@H](O)COP(O)(O)=O',
                                     'name': 'D-arabino-hex-3-ulose '
                                             '6-phosphate',
                                     'reason': 'Does not contain a Coenzyme A '
                                               'adenine fragment'}],
    'sample_false_negatives': [   {   'smiles': 'CC(C)(COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12)[C@@H](O)C(=O)NCCC(=O)NCCSC(=O)C1=CCCCC1=O',
                                      'name': '6-oxocyclohex-1-ene-1-carbonyl-CoA',
                                      'reason': 'Does not contain a 3-oxo '
                                                'fatty acyl thioester '
                                                'substructure'}],
    'attempt': 2,
    'reasoning': 'Below is one approach. In our previous code the key 3‑oxo '
                 'acyl fragment was defined rather loosely (using a SMARTS '
                 'pattern that matched any [CX3](=O)[#6]C(=O)S fragment). That '
                 'pattern was overly permissive so that many CoA “derivatives” '
                 '(such as malonyl-, methylmalonyl‐, or additional substituted '
                 '“bkas‐” compounds) also matched. To improve the '
                 'classification we can\n'
                 '\n'
                 '•\u2003Require that the thioester linkage is preceded by a '
                 'carbonyl (i.e. the “3‑oxo” part) with exactly one '
                 'intervening aliphatic carbon (which in an acyl chain '
                 'corresponds to R–CO–CHR–CO–S–CoA).  \n'
                 '•\u2003Then, inspect the “middle” carbon (marked CHR) to '
                 'reject cases where additional carboxyl substituents are '
                 'attached (as in methylmalonyl-CoA or ethylmalonyl-CoA).  \n'
                 '•\u2003Still require that the CoA moiety is present (by '
                 'looking for a typical adenine fragment) and reject SMILES '
                 'with deprotonated phosphates.\n'
                 '\n'
                 'One solution is to define a more refined SMARTS pattern for '
                 'the acyl fragment (here we chose\u2003'
                 '"[#6:1]-C(=O)-[#6X4:2]-C(=O)S") and then, for any match, '
                 'check that the middle (aliphatic) carbon (atom tagged “2”) '
                 'does not have an extra carboxyl group attached. (In '
                 'methylmalonyl-CoA the central carbon is additionally '
                 'substituted by –C(=O)O.)  \n'
                 '\n'
                 'Below is the complete Python code (contained in one single '
                 'code block) that implements this strategy.\n'
                 '\n'
                 'Below is the code:',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 58,
    'num_false_positives': 47,
    'num_true_negatives': 142194,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.5523809523809524,
    'recall': 0.9830508474576272,
    'f1': 0.7073170731707318,
    'accuracy': 0.9996626844694307,
    'negative_predictive_value': 0.9999929674039172}