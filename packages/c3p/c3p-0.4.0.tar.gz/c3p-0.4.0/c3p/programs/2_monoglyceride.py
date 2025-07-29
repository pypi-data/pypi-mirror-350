"""
Classifies: CHEBI:17389 2-monoglyceride
"""
"""
Classifies: CHEBI:174752 2-monoglyceride
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_2_monoglyceride(smiles: str):
    """
    Determines if a molecule is a 2-monoglyceride based on its SMILES string.
    A 2-monoglyceride has a single fatty acid esterified at the second position of the glycerol backbone.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a 2-monoglyceride, False otherwise
        str: Reason for classification
    """
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
    
    # Check for exactly one ester group (O-C=O)
    ester_pattern = Chem.MolFromSmarts("[OX2][CX3](=[OX1])")
    ester_matches = mol.GetSubstructMatches(ester_pattern)
    if len(ester_matches) != 1:
        return False, f"Found {len(ester_matches)} ester groups, expected 1"
    
    # Check glycerol backbone with ester on C2 and hydroxyls on C1 and C3
    # SMARTS pattern: [CH2]([OH])[CH](O-C=O)[CH2]([OH])
    # More precise pattern to ensure ester is on central carbon with two hydroxyls
    glycerol_pattern = Chem.MolFromSmarts("[CH2]([OH])[CH]([OX2][C](=[OX1])[!O])[CH2]([OH])")
    if not mol.HasSubstructMatch(glycerol_pattern):
        return False, "Glycerol backbone with ester on C2 and hydroxyls on C1/C3 not found"
    
    return True, "Single ester group on C2 of glycerol with hydroxyls on C1 and C3"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:17389',
                          'name': '2-monoglyceride',
                          'definition': 'A monoglyceride in which the acyl '
                                        'substituent is located at position 2.',
                          'parents': ['CHEBI:17408', 'CHEBI:76575'],
                          'xrefs': ['KEGG:C02112'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 25,
                           'log_lines_of_code': 3.2188758248682006,
                           'indent_by_line': [   1,
                                                 1,
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
                                                 1,
                                                 2,
                                                 1,
                                                 1],
                           'max_indent': 2,
                           'imports': [   'from rdkit import Chem',
                                          'from rdkit.Chem import AllChem'],
                           'imports_count': 2,
                           'methods_called': [   'GetSubstructMatches',
                                                 'MolFromSmiles',
                                                 'MolFromSmarts',
                                                 'HasSubstructMatch'],
                           'methods_called_count': 4,
                           'smarts_strings': [   '[OX2][CX3](=[OX1])',
                                                 '[CH2]([OH])[CH]([OX2][C](=[OX1])[!O])[CH2]([OH])'],
                           'smarts_strings_count': 2,
                           'defs': ['is_2_monoglyceride(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, f"Found {len(ester_matches)} '
                                          'ester groups, expected 1"',
                                          'False, "Glycerol backbone with '
                                          'ester on C2 and hydroxyls on C1/C3 '
                                          'not found"',
                                          'True, "Single ester group on C2 of '
                                          'glycerol with hydroxyls on C1 and '
                                          'C3"'],
                           'returns_count': 4,
                           'complexity': 2.84377516497364},
    'message': '\n'
               'Error: unexpected indent (<string>, line 1)\n'
               'Attempt failed: F1 score of 0 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: NONE\n'
               'False positives: NONE\n'
               'False negatives: NONE\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'CC1CCN(CC1)CCCOC2=C(C=C(C=C2)Cl)Br',
                                     'name': '1-[3-(2-bromo-4-chlorophenoxy)propyl]-4-methylpiperidine',
                                     'reason': 'Found 0 ester groups, expected '
                                               '1'},
                                 {   'smiles': 'O([C@H]1[C@H](O[C@H](C)C(=O)N[C@@H](C)C(=O)N[C@H](CCC(=O)N)C(O)=O)[C@@H](NC(=O)C)[C@@H](O[C@@H]1CO)O)[C@@H]2O[C@@H]([C@@H](O)[C@H](O)[C@H]2N)CO',
                                     'name': 'Glucosaminylmuramyl-2-alanine-D-isoglutamine',
                                     'reason': 'Glycerol backbone with ester '
                                               'on C2 and hydroxyls on C1/C3 '
                                               'not found'},
                                 {   'smiles': 'O([C@H]1[C@@H](O[C@@H]2[C@@H](O)[C@H](O)[C@H](O[C@@H]2O[C@@H]3[C@@H](O)[C@H](O)[C@H](OC3O)CO)CO)O[C@@H]([C@@H](O)[C@@H]1O)CO)[C@H]4O[C@@H]([C@@H](O)[C@H](O)[C@H]4O[C@H]5O[C@@H]([C@@H](O)[C@H](O)[C@H]5O[C@H]6O[C@@H]([C@@H](O)[C@H](O)[C@H]6O)CO)CO)CO',
                                     'name': '(3R,4S,5S,6R)-3-[(2R,3R,4S,5S,6R)-3-[(2R,3R,4S,5S,6R)-3-[(2R,3R,4S,5S,6R)-3-[(2R,3R,4S,5S,6R)-4,5-Dihydroxy-6-(hydroxymethyl)-3-[(2R,3R,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-6-(hydroxymethyl)oxane-2,4,5-triol',
                                     'reason': 'Found 0 ester groups, expected '
                                               '1'},
                                 {   'smiles': 'O=C1C=C([C@@H](O)[C@@H]2[C@]1(O2)C[C@H]3C(=C)CC[C@@H]4[C@@]3(CCC[C@]4(CO)C)C)CO',
                                     'name': '13-hydroxylmacrophorin A',
                                     'reason': 'Found 0 ester groups, expected '
                                               '1'},
                                 {   'smiles': '[H][C@@]12CCC(=O)[C@@]1(C)CC[C@@]1([H])[C@@]2([H])[C@@H](O)C=C2C[C@@H](O)CC[C@]12C',
                                     'name': '7beta-hydroxydehydroepiandrosterone',
                                     'reason': 'Found 0 ester groups, expected '
                                               '1'},
                                 {   'smiles': 'O(C=1C(=CC(=CC1Br)Br)Br)C=2C=CC(=CC2Br)Br',
                                     'name': '2,4-dibromophenyl '
                                             '2,4,6-tribromophenyl ether',
                                     'reason': 'Found 0 ester groups, expected '
                                               '1'},
                                 {   'smiles': 'C1C[C@H]([C@H](O[C@H]1CC(=O)NCC2=CC3=C(C=C2)OCO3)CO)NS(=O)(=O)C4=CC=CC(=C4)F',
                                     'name': 'N-(1,3-benzodioxol-5-ylmethyl)-2-[(2R,5R,6S)-5-[(3-fluorophenyl)sulfonylamino]-6-(hydroxymethyl)-2-oxanyl]acetamide',
                                     'reason': 'Found 0 ester groups, expected '
                                               '1'},
                                 {   'smiles': 'C=1(C(=CC=CC1Cl)Cl)C=2C(=C(C=CC2)O)O',
                                     'name': "2',6'-dichlorobiphenyl-2,3-diol",
                                     'reason': 'Found 0 ester groups, expected '
                                               '1'},
                                 {   'smiles': 'O([C@H]1[C@H](O)[C@H](O[C@@H](O[C@H]2[C@H](O)[C@@H](NC(=O)C)C(O[C@@H]2CO)O)[C@H]1O)CO[C@H]3O[C@@H]([C@@H](O)[C@H](O[C@H]4O[C@@H]([C@@H](O)[C@H](O)[C@@H]4O)CO)[C@@H]3O)CO[C@H]5O[C@@H]([C@@H](O)[C@H](O)[C@@H]5O[C@H]6O[C@@H]([C@@H](O)[C@H](O)[C@@H]6O)CO)CO)[C@H]7O[C@@H]([C@@H](O)[C@H](O)[C@@H]7O[C@H]8O[C@@H]([C@@H](O)[C@H](O)[C@@H]8O[C@H]9O[C@@H]([C@@H](O)[C@H](O[C@H]%10O[C@@H]([C@@H](O)[C@H](O)[C@H]%10O)CO)[C@@H]9O)CO)CO)CO',
                                     'name': 'N-[(3R,4R,5S,6R)-5-[(2S,3S,4S,5R,6R)-4-[(2R,3S,4S,5S,6R)-3-[(2R,3S,4S,5S,6R)-3-[(2R,3S,4S,5R,6R)-3,5-Dihydroxy-6-(hydroxymethyl)-4-[(2R,3R,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-6-[[(2S,3S,4S,5R,6R)-6-[[(2S,3S,4S,5S,6R)-4,5-dihydroxy-6-(hydroxymethyl)-3-[(2R,3S,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxymethyl]-3,5-dihydroxy-4-[(2R,3S,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxymethyl]-3,5-dihydroxyoxan-2-yl]oxy-2,4-dihydroxy-6-(hydroxymethyl)oxan-3-yl]acetamide',
                                     'reason': 'Found 0 ester groups, expected '
                                               '1'},
                                 {   'smiles': '[H][C@@]12CC(C)(C)CC[C@@]1(CC[C@]1(C)C2=CC[C@]2([H])[C@@]3(C)CC[C@H](O)C(C)(C)[C@]3([H])CC[C@@]12C)C(O)=O',
                                     'name': 'oleanolic acid',
                                     'reason': 'Glycerol backbone with ester '
                                               'on C2 and hydroxyls on C1/C3 '
                                               'not found'}],
    'sample_false_negatives': [],
    'attempt': 1,
    'reasoning': '</think>\n'
                 '\n'
                 'Okay, I need to create a function called is_2_monoglyceride '
                 'that checks if a given SMILES string is a 2-monoglyceride. '
                 'Let me think about the structure of a 2-monoglyceride. From '
                 "the definition, it's a monoglyceride where the acyl group is "
                 'attached to the second carbon of the glycerol backbone.\n'
                 '\n'
                 'So, the glycerol backbone has three carbons. In a '
                 'monoglyceride, only one of the three hydroxyl groups is '
                 'esterified with a fatty acid. For the 2-monoglyceride '
                 'specifically, that ester must be on the central carbon '
                 '(position 2) of the glycerol.\n'
                 '\n'
                 'First, I need to identify the glycerol structure in the '
                 'molecule. Glycerol is HOCH2-CHOH-CH2OH. When esterified at '
                 'position 2, the structure becomes HOCH2-C(OOCR)-CH2OH, where '
                 'R is the fatty acid chain.\n'
                 '\n'
                 'So, the key features to check are:\n'
                 '1. Presence of a glycerol backbone (three carbons with two '
                 'hydroxyl groups and one ester group).\n'
                 '2. Exactly one ester group attached to the central carbon of '
                 'the glycerol.\n'
                 '3. The other two hydroxyl groups on the terminal carbons '
                 'should be free (not esterified).\n'
                 '\n'
                 'Let me break this down step by step.\n'
                 '\n'
                 '1. **Parsing the SMILES**: Convert the SMILES string to an '
                 "RDKit molecule. If it's invalid, return False.\n"
                 '\n'
                 '2. **Identify the glycerol backbone**: Look for a '
                 'three-carbon chain where the middle carbon is connected to '
                 'an ester group. The terminal carbons should have hydroxyl '
                 'groups (or other substituents, but in monoglycerides, they '
                 'should be -OH).\n'
                 '\n'
                 '3. **Check ester count**: There should be exactly one ester '
                 'group in the molecule. Monoglycerides have only one fatty '
                 'acid chain.\n'
                 '\n'
                 '4. **Position of the ester**: The ester must be on the '
                 "central carbon of the glycerol. So, the ester's oxygen "
                 'should be connected to the middle carbon.\n'
                 '\n'
                 '5. **Fatty acid chain**: The ester should be part of a '
                 'carboxylic acid (like RCO-O-...). The chain should be a '
                 'certain length, but maybe just checking for the presence of '
                 'the ester is enough here.\n'
                 '\n'
                 'Potential issues:\n'
                 '- How to accurately determine the position of the ester. '
                 'Using SMARTS patterns might help here.\n'
                 '- Ensuring that the other two hydroxyls are present and not '
                 'esterified.\n'
                 '\n'
                 'Let me try to construct a SMARTS pattern for the glycerol '
                 'backbone with an ester on the central carbon. The glycerol '
                 'part would be C-O-C(CO)CO, but maybe more precisely:\n'
                 '\n'
                 'The central carbon (position 2) has an ester group. The '
                 'ester is O-R-C(=O)-O-C. Wait, the ester group is O-C(=O)-R. '
                 'So the structure around the central carbon would be: '
                 'C-O-C(=O)-R, and the other two carbons (positions 1 and 3) '
                 'have hydroxyl groups.\n'
                 '\n'
                 'So the SMARTS pattern could be something like '
                 '[CH2]([OH])-[C](=[O])-[OX2]-[CH2]([OH]). Wait, no. Let me '
                 'think again. The central carbon (C2) is connected to the '
                 'ester group. The ester is O-C(=O)-R. So the central carbon '
                 'would have an oxygen connected to the carbonyl group.\n'
                 '\n'
                 'Wait, the correct structure for the ester on C2 would be: '
                 "the central carbon (C2) is connected to an oxygen that's "
                 'part of an ester. The ester group is O-C(=O)-R. So the '
                 "central carbon's connectivity would be: C-O-C(=O)-R. But the "
                 "glycerol's C2 is connected to two other carbons (C1 and C3) "
                 'and the ester oxygen.\n'
                 '\n'
                 'So the SMARTS pattern for the central part would be:\n'
                 '\n'
                 '[CH2]-[C](-[OX2]-C(=O)-*)-[CH2]\n'
                 '\n'
                 'But the hydroxyl groups on C1 and C3 need to be present. '
                 "Wait, no—since it's a monoglyceride, the other two hydroxyls "
                 '(on C1 and C3) should be free. So the terminal carbons (C1 '
                 'and C3) should each have at least one hydroxyl group.\n'
                 '\n'
                 'So the SMARTS pattern for the glycerol backbone with ester '
                 'on C2 could be:\n'
                 '\n'
                 '[CH2]([OH])-[C]([OX2]C(=O)*)-[CH2]([OH])\n'
                 '\n'
                 "But RDKit's SMARTS might need to be adjusted. Let me try to "
                 'write this correctly.\n'
                 '\n'
                 'Alternatively, perhaps match the glycerol backbone where the '
                 'central carbon has an ester group, and the other two carbons '
                 'have hydroxyls.\n'
                 '\n'
                 'So:\n'
                 '\n'
                 'C1: CH2OH\n'
                 'C2: COOR (ester)\n'
                 'C3: CH2OH\n'
                 '\n'
                 'But in the actual structure, the ester is attached via an '
                 'oxygen. So the structure would be:\n'
                 '\n'
                 'C1: CH2OH\n'
                 'C2: O-C(=O)-R connected to the central carbon\n'
                 'C3: CH2OH\n'
                 '\n'
                 'So the SMARTS pattern could be:\n'
                 '\n'
                 '[CH2]([OH])[CH]([OX2][C](=O)[!O])[CH2]([OH])\n'
                 '\n'
                 'Wait, the central carbon (C2) is connected to C1 and C3 '
                 '(each CH2OH), and also to an oxygen that is part of an ester '
                 'group. The ester group is O-C(=O)-R. So the oxygen attached '
                 'to C2 is connected to a carbonyl group.\n'
                 '\n'
                 'So maybe:\n'
                 '\n'
                 '[CH2]([OH])[CH]([OX2][C](=[OX1])[CX4,CX3])[CH2]([OH])\n'
                 '\n'
                 'This would match the central carbon (CH) connected to two '
                 "CH2OH groups and an oxygen that's part of an ester "
                 '(O-C(=O)-R). The [CX4,CX3] is to match the next atom in the '
                 'chain (could be a carbon with single or double bonds).\n'
                 '\n'
                 'Additionally, there should be only one ester group in the '
                 "molecule. So we can check that there's exactly one ester "
                 'group.\n'
                 '\n'
                 'Putting this together:\n'
                 '\n'
                 '1. Check that the molecule has the glycerol backbone with '
                 'ester on C2 using the SMARTS pattern.\n'
                 "2. Ensure there's exactly one ester group in the molecule.\n"
                 '3. Check that the other two hydroxyl groups are present '
                 '(maybe via substructure matching for -OH groups on the '
                 'terminal carbons).\n'
                 '\n'
                 'Potential edge cases:\n'
                 '- The hydroxyl groups might be in different protonation '
                 'states (e.g., O- vs OH), but SMILES usually represents them '
                 'as -OH.\n'
                 '- The fatty acid chain could vary in length and '
                 "unsaturation, but the function shouldn't depend on that as "
                 "long as it's an ester.\n"
                 '\n'
                 "Another approach: Find all ester groups. If there's exactly "
                 "one, check that it's attached to the central carbon of the "
                 'glycerol.\n'
                 '\n'
                 'So steps:\n'
                 '\n'
                 '1. Parse the SMILES into a molecule.\n'
                 '2. Check for validity.\n'
                 '3. Find all ester groups (O-C=O). If count != 1, return '
                 'False.\n'
                 '4. Check that the ester is attached to the central carbon of '
                 'a glycerol backbone.\n'
                 '   - The glycerol backbone is three carbons in a row: '
                 'C-C-C.\n'
                 '   - The ester oxygen is on the middle carbon.\n'
                 '   - The other two carbons have hydroxyl groups.\n'
                 '\n'
                 'So, the SMARTS pattern for the glycerol with ester on C2 '
                 'could be:\n'
                 '\n'
                 '[CH2]([OH])[CH]([OX2][C](=O)*)[CH2]([OH])\n'
                 '\n'
                 'But I need to make sure that the ester oxygen is attached to '
                 "the middle carbon. Let's test this.\n"
                 '\n'
                 'Alternatively, use a SMARTS pattern that matches the entire '
                 'structure. For example:\n'
                 '\n'
                 '*C-O-C(=O)-R where the C is the middle carbon of the '
                 'glycerol.\n'
                 '\n'
                 'But putting it all together:\n'
                 '\n'
                 'The SMARTS pattern for the glycerol part would be:\n'
                 '\n'
                 '[CH2]([OH])-[CH](-[OX2]-C(=O)-[!O])-[CH2]([OH])\n'
                 '\n'
                 'This would match the three-carbon chain where the middle '
                 'carbon is connected to an ester oxygen, and the terminal '
                 'carbons have hydroxyls.\n'
                 '\n'
                 'So, the code steps:\n'
                 '\n'
                 '- Check if the molecule has exactly one ester group.\n'
                 '- Check if the ester is attached to the middle carbon of the '
                 'glycerol backbone.\n'
                 '- Ensure the other two carbons have hydroxyl groups.\n'
                 '\n'
                 'Another way: Use SMARTS to find the specific substructure.\n'
                 '\n'
                 'The complete SMARTS pattern for the 2-monoglyceride would '
                 'be:\n'
                 '\n'
                 '[CH2]([OH])[CH]([OX2][C](=[OX1])[CX4,CX3])[CH2]([OH])\n'
                 '\n'
                 'This pattern matches the glycerol backbone where the middle '
                 'carbon is attached to an ester group, and the two ends have '
                 'hydroxyls.\n'
                 '\n'
                 'Additionally, the molecule should have only one ester '
                 'group.\n'
                 '\n'
                 'So, in code:\n'
                 '\n'
                 'mol = Chem.MolFromSmiles(smiles)\n'
                 'if not mol:\n'
                 '    return False, "Invalid SMILES"\n'
                 '\n'
                 '# Check for exactly one ester group\n'
                 'ester_pattern = Chem.MolFromSmarts("[OX2][CX3](=[OX1])")\n'
                 'esters = mol.GetSubstructMatches(ester_pattern)\n'
                 'if len(esters) != 1:\n'
                 '    return False, f"Expected 1 ester group, found '
                 '{len(esters)}"\n'
                 '\n'
                 '# Check the glycerol structure with ester on C2\n'
                 'glycerol_pattern = '
                 'Chem.MolFromSmarts("[CH2]([OH])[CH]([OX2][C](=[OX1])[!O])[CH2]([OH])")\n'
                 'if not mol.HasSubstructMatch(glycerol_pattern):\n'
                 '    return False, "Glycerol backbone with ester on C2 not '
                 'found"\n'
                 '\n'
                 '# Also check that the ester is the only one and attached '
                 'correctly\n'
                 '# Maybe check the rest of the molecule for other esters? But '
                 'already checked len(esters) ==1\n'
                 '\n'
                 'But wait, the ester_pattern might match more than once if '
                 'there are other carbonyl groups. Wait, the ester_pattern is '
                 "looking for O-C(=O), which is the ester group. So if there's "
                 "exactly one, and the glycerol pattern is present, then it's "
                 'a 2-monoglyceride.\n'
                 '\n'
                 'Potential issues: The hydroxyl groups might not be explicit '
                 'in the SMILES. For example, if the SMILES uses implicit '
                 "hydrogens, but RDKit's substructure matching should handle "
                 'that.\n'
                 '\n'
                 'Testing with example SMILES:\n'
                 '\n'
                 'Take "CCCCCCCCCC(=O)OC(CO)CO" (2-decanoylglycerol). The '
                 'glycerol part is OC(CO)CO, with the ester on the central C.\n'
                 '\n'
                 'In the SMARTS pattern, the central C is connected to '
                 'O-C(=O), and the two CH2 groups have OH.\n'
                 '\n'
                 'Another example: '
                 '"O=C(CCC/C=C\\C\\C=C/C=C/C(C/C=C\\CCCCC)OO)OC(CO)CO" '
                 '(12-HPETE 2-glyceryl ester). The ester is on the central C '
                 'of OC(CO)CO.\n'
                 '\n'
                 'So the SMARTS pattern should match these.\n'
                 '\n'
                 'But what about if there are other oxygen atoms not part of '
                 'the ester? The code checks for exactly one ester group, so '
                 "that's okay.\n"
                 '\n'
                 'So putting it all together:\n'
                 '\n'
                 'The function will:\n'
                 '\n'
                 '1. Check for valid SMILES.\n'
                 '2. Check for exactly one ester group.\n'
                 '3. Check that the ester is on the central carbon of the '
                 'glycerol backbone with two hydroxyls on the terminals.\n'
                 '\n'
                 'Now, code:',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 34,
    'num_false_positives': 13,
    'num_true_negatives': 142253,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.723404255319149,
    'recall': 1.0,
    'f1': 0.8395061728395062,
    'accuracy': 0.9999086437104708,
    'negative_predictive_value': 1.0}