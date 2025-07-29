"""
Classifies: CHEBI:61905 short-chain fatty acyl-CoA
"""
from rdkit import Chem

def is_short_chain_fatty_acyl_CoA(smiles: str):
    """
    Determines if a molecule is a short-chain fatty acyl-CoA based on its SMILES string.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a short-chain fatty acyl-CoA, False otherwise
        str: Reason for classification
    """
    
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Look for Coenzyme A specific fragments
    coA_pattern = Chem.MolFromSmarts("OP(=O)(O)OC[C@H]1O[C@H]([C@@H](O)[C@H]1OP(=O)(O)O)n1cnc2c(N)ncnc12")
    if not mol.HasSubstructMatch(coA_pattern):
        return False, "Coenzyme A structure not found"

    # Look for thioester linkage: S-C(=O) for fatty acyl attachment
    thioester_pattern = Chem.MolFromSmarts("S-[CX3](=O)-[C]")
    thioester_matches = mol.GetSubstructMatches(thioester_pattern)
    if not thioester_matches:
        return False, "No thioester linkage found"

    # Check for acyl chain length from 2 to 6 carbons
    for match in thioester_matches:
        acyl_start = match[2]  # Start checking from the carbon in the S-C(=O)-C linkage
        chain_length = 1  # Start counting from the carbon in the thioester linkage
        
        queue = [acyl_start]
        visited = set(queue)
        
        while queue:
            atom_idx = queue.pop(0)
            atom = mol.GetAtomWithIdx(atom_idx)

            for neighbor in atom.GetNeighbors():
                n_idx = neighbor.GetIdx()
                
                # Traverse only through unvisited carbon atoms, skip others
                if n_idx not in visited and mol.GetAtomWithIdx(n_idx).GetAtomicNum() == 6:
                    chain_length += 1
                    visited.add(n_idx)
                    queue.append(n_idx)

        # Validate short chain length
        if 2 <= chain_length <= 6:
            return True, "Contains Coenzyme A linked with a short-chain fatty acid"

    return False, "No short-chain fatty acid attached to CoA"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:61905',
                          'name': 'short-chain fatty acyl-CoA',
                          'definition': 'A fatty acyl-CoA that results from '
                                        'the formal condensation of the thiol '
                                        'group of coenzyme A with the carboxy '
                                        'group of any short-chain fatty acid.',
                          'parents': ['CHEBI:37554'],
                          'xrefs': [   'PMID:20371198',
                                       'PMID:20376488',
                                       'PMID:20429031'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 31,
                           'log_lines_of_code': 3.4339872044851463,
                           'indent_by_line': [   1,
                                                 1,
                                                 0,
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
                                                 1,
                                                 2,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
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
                                                 3,
                                                 3,
                                                 0,
                                                 0,
                                                 0,
                                                 0,
                                                 1],
                           'max_indent': 3,
                           'imports': ['from rdkit import Chem'],
                           'imports_count': 1,
                           'methods_called': [   'GetSubstructMatches',
                                                 'MolFromSmarts',
                                                 'pop',
                                                 'GetAtomWithIdx',
                                                 'MolFromSmiles',
                                                 'HasSubstructMatch'],
                           'methods_called_count': 6,
                           'smarts_strings': [   'S-[CX3](=O)-[C]',
                                                 'OP(=O)(O)OC[C@H]1O[C@H]([C@@H](O)[C@H]1OP(=O)(O)O)n1cnc2c(N)ncnc12'],
                           'smarts_strings_count': 2,
                           'defs': [   'is_short_chain_fatty_acyl_CoA(smiles: '
                                       'str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "Coenzyme A structure not '
                                          'found"',
                                          'False, "No thioester linkage found"',
                                          'False, "No short-chain fatty acid '
                                          'attached to CoA"'],
                           'returns_count': 4,
                           'complexity': 3.4867974408970293},
    'message': '\n'
               'Attempt failed: F1 score of 0 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: NONE\n'
               'False positives: NONE\n'
               'False negatives: SMILES: '
               'CC(C)C=CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12 '
               'NAME: 4-methylpent-2-enoyl-CoA REASON: MISSED No short-chain '
               'fatty acid attached to CoA\n'
               ' * SMILES: '
               '[C@@H]1(N2C3=C(C(=NC=N3)N)N=C2)O[C@H](COP(OP(OCC(C)([C@H](C(NCCC(NCCSC(CC(CC)O)=O)=O)=O)O)C)(=O)[O-])(=O)[O-])[C@H]([C@H]1O)OP([O-])([O-])=O '
               'NAME: 3-hydroxypentanoyl-CoA(4-) REASON: MISSED No short-chain '
               'fatty acid attached to CoA\n'
               ' * SMILES: '
               '[C@@H]1(N2C3=C(C(=NC=N3)N)N=C2)O[C@H](COP(OP(OCC(C)([C@H](C(NCCC(NCCSC(C[C@@H](CC)O)=O)=O)=O)O)C)(=O)[O-])(=O)[O-])[C@H]([C@H]1O)OP([O-])([O-])=O '
               'NAME: (R)-3-hydroxypentanoyl-CoA(4-) REASON: MISSED No '
               'short-chain fatty acid attached to CoA\n'
               ' * SMILES: '
               'CC(=C)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12 '
               'NAME: 3-methylbut-3-enoyl-CoA REASON: MISSED No short-chain '
               'fatty acid attached to CoA\n'
               ' * SMILES: '
               'CC(C)C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12 '
               'NAME: isobutyryl-CoA REASON: MISSED No short-chain fatty acid '
               'attached to CoA\n'
               ' * SMILES: '
               '[C@@H]1(N2C3=C(C(=NC=N3)N)N=C2)O[C@H](COP(OP(OCC(C)([C@H](C(NCCC(NCCSC(C(C(C)C)O)=O)=O)=O)O)C)(=O)O)(=O)O)[C@H]([C@H]1O)OP(O)(O)=O '
               'NAME: 2-hydroxyisovaleryl-CoA REASON: MISSED No short-chain '
               'fatty acid attached to CoA\n'
               ' * SMILES: '
               '[C@@H]1(N2C3=C(C(=NC=N3)N)N=C2)O[C@H](COP(OP(OCC(C)([C@H](C(NCCC(NCCSC(=O)CCC(C)C)=O)=O)O)C)(=O)O)(=O)O)[C@H]([C@H]1O)OP(O)(O)=O '
               'NAME: 4-methylpentanoyl-CoA REASON: MISSED No short-chain '
               'fatty acid attached to CoA\n'
               ' * SMILES: '
               'CC\\C=C\\C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12 '
               'NAME: (2E)-pentenoyl-CoA REASON: MISSED No short-chain fatty '
               'acid attached to CoA\n'
               ' * SMILES: '
               'C[C@H](N)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12 '
               'NAME: L-3-aminobutanoyl-CoA REASON: MISSED No short-chain '
               'fatty acid attached to CoA\n'
               ' * SMILES: '
               '[C@@H]1(N2C3=C(C(=NC=N3)N)N=C2)O[C@H](COP(OP(OCC(C)([C@H](C(NCCC(NCCSC(C(CC)O)=O)=O)=O)O)C)(=O)O)(=O)O)[C@H]([C@H]1O)OP(O)(O)=O '
               'NAME: 2-hydroxybutanoyl-CoA REASON: MISSED No short-chain '
               'fatty acid attached to CoA\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'CCCCCCCCCCCCCCCCCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12',
                                     'name': '3-oxotetracosanoyl-CoA(4-)',
                                     'reason': 'No short-chain fatty acid '
                                               'attached to CoA'},
                                 {   'smiles': 'CNC(NCCSCc1csc(CN(C)C)n1)=C[N+]([O-])=O',
                                     'name': 'nizatidine',
                                     'reason': 'Coenzyme A structure not '
                                               'found'},
                                 {   'smiles': 'O=C1C=CC(O)C([C@]12O[C@@H](O)[C@H](C2)NC(=O)/C=C/CCCCCCCCCO)O',
                                     'name': 'Isariotin L',
                                     'reason': 'Coenzyme A structure not '
                                               'found'},
                                 {   'smiles': 'O=C1N([C@H](C(=O)N[C@H](C(=O)NCCC(O[C@H](C(N2[C@H](C(N[C@H]1CC3=CC=CC=C3)=O)CCC2)=O)CC(C)C)=O)CC(C)C)C(C)C)C',
                                     'name': 'Desmethylisaridin C1',
                                     'reason': 'Coenzyme A structure not '
                                               'found'},
                                 {   'smiles': 'O[C@H]([C@H](CCC(O)=O)C(O)=O)C(O)=O',
                                     'name': '(-)-homoisocitric acid',
                                     'reason': 'Coenzyme A structure not '
                                               'found'},
                                 {   'smiles': 'O=C1O[C@@H](C)C=C1CCC[C@H](CC)C',
                                     'name': '(5S,S)-5-methyl-3-(4-methylhexyl)furan-2(5H)-one',
                                     'reason': 'Coenzyme A structure not '
                                               'found'},
                                 {   'smiles': 'CCCCCCCCCCCCCCCCCCCCCCCC(=O)N[C@@H](CO[C@@H]1O[C@H](CO)[C@@H](O[C@@H]2O[C@H](CO)[C@H](O[C@H]3O[C@H](CO)[C@H](O)[C@H](O)[C@H]3O)[C@H](O)[C@H]2O)[C@H](O)[C@H]1O)[C@H](O)\\C=C\\CCCCCCCCCCCCC',
                                     'name': "alpha-D-Gal-(1->4)-beta-D-Gal-(1->4)-beta-D-Glc-(1<->1')-Cer(d18:1/24:0)",
                                     'reason': 'Coenzyme A structure not '
                                               'found'},
                                 {   'smiles': 'S(O[C@@H]1[C@H](O)[C@@H](NC(=O)C)[C@H](O[C@H]2[C@H](O)[C@@H](NC(=O)C)[C@H](O[C@@H]3[C@@H](O[C@@H]4[C@H](O)[C@H](O[C@H]5[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]5CO)O[C@H]6[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]6CO)O)O[C@@H]([C@H]4O)CO[C@H]7O[C@@H]([C@@H](O)[C@H](O)[C@@H]7O[C@@H]8O[C@@H]([C@@H](O[C@@H]9O[C@@H]([C@H](OS(O)(=O)=O)[C@H](O)[C@H]9NC(=O)C)CO)[C@H](O)[C@H]8NC(=O)C)CO)CO)O[C@@H]([C@@H](O)[C@@H]3O)CO)O[C@@H]2CO)O[C@@H]1CO)(O)(=O)=O',
                                     'name': '[(2R,3R,4R,5R,6S)-5-Acetamido-6-[(2R,3S,4R,5R,6S)-5-acetamido-6-[(2S,3S,4S,5S,6R)-2-[[(2R,3R,4S,5S,6S)-6-[(2R,3S,4R,5R,6S)-5-acetamido-6-[(2R,3S,4R,5R,6R)-5-acetamido-4,6-dihydroxy-2-(hydroxymethyl)oxan-3-yl]oxy-4-hydroxy-2-(hydroxymethyl)oxan-3-yl]oxy-4-[(2R,3S,4S,5S,6R)-3-[(2S,3R,4R,5S,6R)-3-acetamido-5-[(2S,3R,4R,5R,6R)-3-acetamido-4-hydroxy-6-(hydroxymethyl)-5-sulfooxyoxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-3,5-dihydroxyoxan-2-yl]methoxy]-4,5-dihydroxy-6-(hydroxymethyl)oxan-3-yl]oxy-4-hydroxy-2-(hydroxymethyl)oxan-3-yl]oxy-4-hydroxy-2-(hydroxymethyl)oxan-3-yl] '
                                             'hydrogen sulfate',
                                     'reason': 'Coenzyme A structure not '
                                               'found'},
                                 {   'smiles': 'O([C@H]1[C@H](O)[C@H](O[C@@H]2O[C@@H]([C@@H](O[C@@H]3O[C@@H]([C@H](O)[C@H](O)[C@H]3O)CO[C@]4(O[C@H]([C@H](NC(=O)C)[C@@H](O)C4)[C@H](O)[C@H](O)CO)C(O)=O)[C@H](O)[C@H]2NC(=O)C)CO)[C@H](O[C@@H]1CO)O[C@H]5[C@H](O)[C@H](O[C@@H](O[C@H]6[C@H](O)[C@@H](NC(=O)C)C(O[C@@H]6CO)O)[C@H]5O)CO[C@H]7O[C@@H]([C@@H](O)[C@H](O)[C@@H]7O[C@@H]8O[C@@H]([C@@H](O[C@@H]9O[C@@H]([C@H](O)[C@H](O)[C@H]9O)CO[C@]%10(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%10)[C@H](O)[C@H](O)CO)C(O)=O)[C@H](O)[C@H]8NC(=O)C)CO)CO[C@@H]%11O[C@@H]([C@@H](O[C@@H]%12O[C@@H]([C@H](O)[C@H](O[C@]%13(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%13)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%12O)CO)[C@H](O)[C@H]%11NC(=O)C)CO)[C@@H]%14O[C@@H]([C@@H](O[C@@H]%15O[C@@H]([C@H](O)[C@H](O[C@]%16(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%16)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%15O)CO)[C@H](O)[C@H]%14NC(=O)C)CO',
                                     'name': 'CID 71297936',
                                     'reason': 'Coenzyme A structure not '
                                               'found'},
                                 {   'smiles': 'CNC(=O)Oc1cc(C)cc(C)c1C',
                                     'name': '2,3,5-trimethylphenyl '
                                             'methylcarbamate',
                                     'reason': 'Coenzyme A structure not '
                                               'found'}],
    'sample_false_negatives': [   {   'smiles': 'CC(C)C=CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12',
                                      'name': '4-methylpent-2-enoyl-CoA',
                                      'reason': 'No short-chain fatty acid '
                                                'attached to CoA'},
                                  {   'smiles': '[C@@H]1(N2C3=C(C(=NC=N3)N)N=C2)O[C@H](COP(OP(OCC(C)([C@H](C(NCCC(NCCSC(=O)CCC(C)C)=O)=O)O)C)(=O)O)(=O)O)[C@H]([C@H]1O)OP(O)(O)=O',
                                      'name': '4-methylpentanoyl-CoA',
                                      'reason': 'No short-chain fatty acid '
                                                'attached to CoA'},
                                  {   'smiles': 'COc1cc(ccc1O)C(O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12',
                                      'name': '3-hydroxy-3-(4-hydroxy-3-methoxyphenyl)propanoyl-CoA',
                                      'reason': 'No short-chain fatty acid '
                                                'attached to CoA'},
                                  {   'smiles': 'CC(C)C[C@@H](O)C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12',
                                      'name': '(R)-2-hydroxy-4-methylpentanoyl-CoA',
                                      'reason': 'No short-chain fatty acid '
                                                'attached to CoA'}],
    'attempt': 3,
    'reasoning': 'To improve the classification of short-chain fatty '
                 "acyl-CoAs, let's carefully analyze the requirements. A "
                 'short-chain fatty acyl-CoA is characterized by a fatty acyl '
                 'group attached to Coenzyme A via a thioester linkage. The '
                 'fatty acid should be short-chain, typically consisting of 2 '
                 'to 6 carbon atoms.\n'
                 '\n'
                 'In the previous implementation:\n'
                 '1. **Coenzyme A Detection:** It correctly checked for the '
                 'Coenzyme A structure, which includes specific structural '
                 'motifs like ribose phosphodiester and adenine.\n'
                 '2. **Thioester Linkage Detection:** It correctly identified '
                 'the thioester linkage `S-C(=O)`, which is crucial for fatty '
                 'acyl-CoA.\n'
                 '3. **Chain Length Calculation:** The code aimed to calculate '
                 'the carbon chain length starting from the carbon atom '
                 'directly engaged in the thioester linkage. However, the '
                 'method of traversal might need improvement to ensure only '
                 'the intended acyl chain length is measured, excluding '
                 'branches or additional structures not part of the main '
                 'chain.\n'
                 '\n'
                 'Improvements to address:\n'
                 '- Ensure that the traversal only includes the straight-chain '
                 'carbons of the fatty acid without mistakenly counting side '
                 'branches or other parts of CoA.\n'
                 '- Precisely differentiate the acyl chain from the rest of '
                 'the molecular structure, especially when numerous branch '
                 'points or rings are present near the thioester linkage.\n'
                 '\n'
                 'Based on these points, the revised code should more '
                 'accurately track the main chain from the thioester carbon, '
                 'moving linearly through carbon atoms:',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 26,
    'num_false_positives': 148,
    'num_true_negatives': 142122,
    'num_false_negatives': 4,
    'num_negatives': None,
    'precision': 0.14942528735632185,
    'recall': 0.8666666666666667,
    'f1': 0.25490196078431376,
    'accuracy': 0.9989318341531974,
    'negative_predictive_value': 0.9999718559587971}