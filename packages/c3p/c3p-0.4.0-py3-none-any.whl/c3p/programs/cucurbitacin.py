"""
Classifies: CHEBI:16219 cucurbitacin
"""
"""
Classifies: CHEBI:87070 cucurbitacin
"""
from rdkit import Chem
from rdkit.Chem import Descriptors, rdMolDescriptors

def is_cucurbitacin(smiles: str):
    """
    Determines if a molecule is a cucurbitacin based on its SMILES string.
    Cucurbitacins are tetracyclic triterpenoids derived from cucurbitane.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a cucurbitacin, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES"
    
    # Check for triterpenoid skeleton (approximately 30 carbons)
    c_count = sum(1 for atom in mol.GetAtoms() if atom.GetAtomicNum() == 6)
    if c_count < 25:  # Adjusted for possible substitutions
        return False, f"Too few carbons ({c_count}) for triterpenoid"
    
    # Check for tetracyclic system (4 rings in SSSR)
    sssr = Chem.GetSSSR(mol)
    if len(sssr) < 4:
        return False, f"Only {len(sssr)} rings, need at least 4"
    
    # Check for oxygen-containing groups (hydroxyl, ketone, ester)
    o_count = sum(1 for atom in mol.GetAtoms() if atom.GetAtomicNum() == 8)
    if o_count < 4:
        return False, f"Only {o_count} oxygens, expected multiple oxygen groups"
    
    # Check molecular weight (typical cucurbitacins are >400 Da)
    mol_wt = Descriptors.ExactMolWt(mol)
    if mol_wt < 400:
        return False, f"Molecular weight too low ({mol_wt:.1f} Da)"
    
    # Check for alpha,beta-unsaturated ketone (common feature)
    enone = Chem.MolFromSmarts("C=C(O)C(=O)")
    if not mol.HasSubstructMatch(enone):
        return False, "No alpha,beta-unsaturated ketone detected"
    
    return True, "Tetracyclic triterpenoid with oxygen functional groups"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:16219',
                          'name': 'cucurbitacin',
                          'definition': 'Any one of a class of tetracyclic '
                                        'triterpenoids, formally derived from '
                                        'the triterpene hydrocarbon '
                                        'cucurbitane, developed by some plants '
                                        '(especially those of the family '
                                        'Cucurbitaceaeas) as a defence '
                                        'mechanism against herbivores.',
                          'parents': ['CHEBI:26893'],
                          'xrefs': ['Wikipedia:Cucurbitacin'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 33,
                           'log_lines_of_code': 3.4965075614664802,
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
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 1,
                                                 1],
                           'max_indent': 2,
                           'imports': [   'from rdkit import Chem',
                                          'from rdkit.Chem import Descriptors, '
                                          'rdMolDescriptors'],
                           'imports_count': 2,
                           'methods_called': [   'ExactMolWt',
                                                 'MolFromSmiles',
                                                 'MolFromSmarts',
                                                 'HasSubstructMatch',
                                                 'GetAtoms',
                                                 'GetAtomicNum',
                                                 'GetSSSR'],
                           'methods_called_count': 7,
                           'smarts_strings': ['C=C(O)C(=O)'],
                           'smarts_strings_count': 1,
                           'defs': ['is_cucurbitacin(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES"',
                                          'False, f"Too few carbons '
                                          '({c_count}) for triterpenoid"',
                                          'False, f"Only {len(sssr)} rings, '
                                          'need at least 4"',
                                          'False, f"Only {o_count} oxygens, '
                                          'expected multiple oxygen groups"',
                                          'False, f"Molecular weight too low '
                                          '({mol_wt:.1f} Da)"',
                                          'False, "No alpha,beta-unsaturated '
                                          'ketone detected"',
                                          'True, "Tetracyclic triterpenoid '
                                          'with oxygen functional groups"'],
                           'returns_count': 7,
                           'complexity': 4.099301512293296},
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
    'sample_true_negatives': [   {   'smiles': 'ClC1=C(O)C(=C(O)C=C1C)C(=O)C2=C(C(O)=CC(=C2CC=C(C)C)O)C=O',
                                     'name': 'Pestalone E',
                                     'reason': 'Too few carbons (20) for '
                                               'triterpenoid'},
                                 {   'smiles': 'O1C(CCCC(=O)C=CC1=O)C(=O)C',
                                     'name': '(7E)-2-acetyl-2,3,4,5-tetrahydrooxonine-6,9-dione',
                                     'reason': 'Too few carbons (10) for '
                                               'triterpenoid'},
                                 {   'smiles': 'O1[C@@H](O[C@@H]2[C@@H](O)[C@@H](O[C@@H]([C@@H]2O)CO)O[C@H]3[C@H](O)[C@@H](O)C(O[C@@H]3CO)O)[C@H](NC(=O)C)[C@@H](O[C@@H]4O[C@H]([C@@H](O)[C@@H](O)[C@@H]4O)C)[C@H](O[C@@H]5O[C@@H]([C@H](O)[C@H](O)[C@H]5O)CO[C@]6(O[C@H]([C@H](NC(=O)C)[C@@H](O)C6)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]1CO',
                                     'name': '(2R,4S,5R,6R)-5-Acetamido-2-[[(2R,3R,4S,5R,6S)-6-[(2R,3S,4R,5R,6S)-5-acetamido-6-[(2R,3S,4S,5R,6S)-3,5-dihydroxy-2-(hydroxymethyl)-6-[(2R,3S,4R,5R)-4,5,6-trihydroxy-2-(hydroxymethyl)oxan-3-yl]oxyoxan-4-yl]oxy-2-(hydroxymethyl)-4-[(2S,3S,4R,5S,6S)-3,4,5-trihydroxy-6-methyloxan-2-yl]oxyoxan-3-yl]oxy-3,4,5-trihydroxyoxan-2-yl]methoxy]-4-hydroxy-6-[(1R,2R)-1,2,3-trihydroxypropyl]oxane-2-carboxylic '
                                             'acid',
                                     'reason': 'No alpha,beta-unsaturated '
                                               'ketone detected'},
                                 {   'smiles': 'CN(C)CC1=CC=C(C=C1)C2=NC3=CC=CC4=C3N2CCNC4=O',
                                     'name': 'LSM-1988',
                                     'reason': 'Too few carbons (19) for '
                                               'triterpenoid'},
                                 {   'smiles': 'CCCSP(=S)(OCC)Oc1ccc(Cl)cc1Cl',
                                     'name': 'prothiofos',
                                     'reason': 'Too few carbons (11) for '
                                               'triterpenoid'},
                                 {   'smiles': 'O=C/C(=C/C=C/[C@H]([C@@H]1[C@@]2([C@@](C3=C([C@@]4([C@H](C([C@@H](O)CC4)(C)C)CC3)C)CC2)(C)CC1)C)C)/C',
                                     'name': 'Astraeusin B',
                                     'reason': 'Only 2 oxygens, expected '
                                               'multiple oxygen groups'},
                                 {   'smiles': 'CC12CCC(=O)C=C1CCC3C2(C(CC4(C3CCC4(C)O)C)O)F',
                                     'name': '9-fluoro-11,17-dihydroxy-10,13,17-trimethyl-1,2,6,7,8,11,12,14,15,16-decahydrocyclopenta[a]phenanthren-3-one',
                                     'reason': 'Too few carbons (20) for '
                                               'triterpenoid'},
                                 {   'smiles': 'O=C1C2=C(O)C=C(OC)C=C2C(=O)C3=C1[C@H](O)C[C@]([C@H]3O)(O)C',
                                     'name': '(1R,3R.4S)-4-hydroxyaustrocortilutein',
                                     'reason': 'Too few carbons (16) for '
                                               'triterpenoid'},
                                 {   'smiles': 'O([C@H]1[C@H](O[C@@H]2[C@@H](O)[C@H](O)[C@H](O[C@H]2O)CO)O[C@@H]([C@@H](O)[C@@H]1O)CO)[C@@H]3O[C@@H]([C@@H](O)[C@H](O)[C@H]3O)CO',
                                     'name': 'beta-D-Glcp-(1->2)-beta-D-Glcp-(1->2)-beta-D-Glcp',
                                     'reason': 'Too few carbons (18) for '
                                               'triterpenoid'},
                                 {   'smiles': 'CC(=O)CCCC(O)=O',
                                     'name': '5-oxohexanoic acid',
                                     'reason': 'Too few carbons (6) for '
                                               'triterpenoid'}],
    'sample_false_negatives': [   {   'smiles': 'O(C1C(C=2[C@@]([C@@]3(C([C@]4([C@@]([C@](CC4)([C@@H]([C@H](O)[C@@H](O)[C@@H](O)C(O)(C)C)C)[H])(CC3)C)C)CC2)C)(CC1)[H])(C)C)[C@@H]5O[C@@H]([C@H](O)[C@H](O)[C@H]5O)CO[C@@H]6O[C@@H]([C@H](O)[C@H](O)[C@H]6O)CO',
                                      'name': 'Momorcharaside A',
                                      'reason': 'No alpha,beta-unsaturated '
                                                'ketone detected'},
                                  {   'smiles': 'O([C@@H]1[C@@]([C@@]2([C@](C3[C@@](CC2)([C@@]4(C(=C[C@H]3O)C(C(O[C@@H]5OC[C@@H](OC(=O)C)[C@H](O)[C@H]5O)CC4)(C)C)[H])C)(C1)C)C)([C@@H](CCC=C(C)C)C)[H])[C@@H]6O[C@@H]([C@@H](O)[C@H](O)[C@H]6O)COC(=O)C',
                                      'name': 'Hebevinoside II',
                                      'reason': 'No alpha,beta-unsaturated '
                                                'ketone detected'},
                                  {   'smiles': 'OC1C2C3(C(C(CC3)C(C/C=C/C(OC)(C)C)C)(CCC2(C4C(=C1)C(C(O)CC4)(C)C)C=O)C)C',
                                      'name': '3,7-Dihydroxy-25-methoxycucurbita-5,23-dien-19-al',
                                      'reason': 'No alpha,beta-unsaturated '
                                                'ketone detected'},
                                  {   'smiles': 'O=C1C(C2=CC[C@H]3[C@]4([C@](C(C(O)(C(=O)/C=C/C(OC(=O)C)(C)C)C)[C@@H](C4)OC(=O)CCCCCCC/C=C\\CCCCCCCC)(C)CC([C@]3([C@@H]2C[C@@H]1O)C)=O)C)(C)C',
                                      'name': 'Cucurbitacin B oleyl ester',
                                      'reason': 'No alpha,beta-unsaturated '
                                                'ketone detected'},
                                  {   'smiles': '[H][C@@]12C[C@@H](C)[C@]3([H])[C@@]4(C)CC[C@@]56C[C@@]55CC[C@H](O[C@]7([H])OC[C@H](O)[C@H](O)[C@H]7O)C(C)(C)[C@]5([H])CC[C@@]6([H])[C@]4(C)[C@@H](O)[C@]3(O[C@@H]1C(C)(C)OC(C)=O)O2',
                                      'name': '25-O-acetylcimigenol '
                                              '3-O-alpha-L-arabinopyranoside',
                                      'reason': 'No alpha,beta-unsaturated '
                                                'ketone detected'},
                                  {   'smiles': 'CC(C)(O)\\C=C\\C(=O)[C@](C)(O)[C@H]1[C@H](O)C[C@@]2(C)[C@@H]3CC=C4[C@@H](C[C@@H](O)[C@@H](O)C4(C)C)[C@]3(C)C(=O)C[C@]12C',
                                      'name': 'Cucurbitacin O',
                                      'reason': 'No alpha,beta-unsaturated '
                                                'ketone detected'},
                                  {   'smiles': 'OC1C(C2(C(C3C(C4C(=CC3)C(C(OC5OC(C(O)C(O)C5O)CO)CC4)(C)C)(C(=O)C2)C)(C1)C)C)C(O)(C(O)CCC(OC(=O)C)(C)C)C',
                                      'name': '(3b,16a,20R)-25-Acetoxy-3,16,20,22-tetrahydroxy-5-cucurbiten-11-one '
                                              '3-glucoside',
                                      'reason': 'No alpha,beta-unsaturated '
                                                'ketone detected'},
                                  {   'smiles': 'O([C@H]1[C@H]([C@]2([C@@]([C@@]3([C@](CC2)([C@@]4(C(=C[C@@H]3O)C([C@H](O[C@@H]5OC[C@@H](O)[C@H](O)C5O)CC4)(C)C)[H])C)[H])(C1)C)C)C(CCC=C(C)C)C)[C@@H]6O[C@H]([C@@H](OC(=O)C)[C@H](O)[C@@H]6O)CO',
                                      'name': 'Hebevinoside XII',
                                      'reason': 'No alpha,beta-unsaturated '
                                                'ketone detected'},
                                  {   'smiles': 'O([C@@H]1[C@@]([C@@]2([C@](C3[C@@](CC2)([C@@]4(C(=C[C@H]3O)C(C(O[C@@H]5OC[C@@H](O)[C@H](O)[C@H]5O)CC4)(C)C)[H])C)(C1)C)C)([C@@H](CCC=C(C)C)C)[H])[C@@H]6O[C@@H]([C@@H](OC(=O)C)[C@@H](O)[C@H]6O)COC(=O)C',
                                      'name': 'Hebevinoside VII',
                                      'reason': 'No alpha,beta-unsaturated '
                                                'ketone detected'},
                                  {   'smiles': 'O=C1C(C2=CC[C@H]3[C@]4([C@](C(C(O)(C(=O)/C=C/C(OC(=O)C)(C)C)C)[C@@H](C4)OC(=O)CCCCCCC/C=C\\C/C=C\\CCCCC)(C)CC([C@]3([C@@H]2C[C@@H]1O)C)=O)C)(C)C',
                                      'name': 'Cucurbitacin B linoleyl ester',
                                      'reason': 'No alpha,beta-unsaturated '
                                                'ketone detected'}],
    'attempt': 1,
    'reasoning': '</think>\n'
                 '\n'
                 "Okay, let's try to figure out why the previous code failed. "
                 'The user mentioned an "unexpected indent" error in the code. '
                 'Looking at the previous code, I see that instead of '
                 'providing valid Python code, the assistant pasted a long '
                 "list of SMILES strings, which isn't valid Python. That's "
                 "definitely a problem. The user's example for triglyceride "
                 'had a properly formatted function with imports and logic. '
                 "The mistake here was that the assistant didn't structure the "
                 'code correctly for cucurbitacin.\n'
                 '\n'
                 "So, the main issue was that the previous attempt wasn't "
                 'valid Python code. The assistant included SMILES examples in '
                 'the code block, leading to syntax errors. The correct '
                 'approach is to write a Python function using RDKit to check '
                 'structural features of cucurbitacins.\n'
                 '\n'
                 'Cucurbitacins are tetracyclic triterpenoids derived from '
                 'cucurbitane. The key features to check would be the '
                 'tetracyclic structure (four rings), the presence of '
                 'oxygen-containing functional groups (like hydroxyl, ketone, '
                 'ester), and possibly the molecular formula or specific '
                 'substructures.\n'
                 '\n'
                 'First, parse the SMILES into a molecule. Then, check for the '
                 'cucurbitane skeleton. This might involve matching a specific '
                 'substructure pattern using SMARTS. For example, cucurbitane '
                 'has a specific arrangement of rings and substituents. '
                 'However, defining the exact SMARTS pattern for cucurbitane '
                 'might be complex. Alternatively, check for the number of '
                 'rings and their arrangement.\n'
                 '\n'
                 'Another approach is to count the number of carbons (since '
                 'triterpenoids have 30 carbons) and check for oxygen atoms. '
                 'Also, look for specific functional groups like hydroxyls, '
                 'ketones, or esters. Additionally, the molecular weight could '
                 'be a hint, as triterpenoids are larger molecules.\n'
                 '\n'
                 'But creating an accurate SMARTS pattern for cucurbitane is '
                 'challenging. Maybe using the presence of multiple oxygen '
                 'atoms and a certain number of rings. Alternatively, check '
                 "for a specific core structure that's common in "
                 'cucurbitacins.\n'
                 '\n'
                 'Wait, looking at the example SMILES provided, many have a '
                 'similar core with multiple rings and oxygen atoms. Perhaps '
                 'using a SMARTS pattern that matches the tetracyclic system '
                 'with certain substituents. For example, a pattern that '
                 'includes four fused rings with oxygen atoms attached.\n'
                 '\n'
                 'Alternatively, use the presence of multiple hydroxyl groups '
                 'and ketones. Since cucurbitacins often have several '
                 'oxygen-containing groups, checking for a minimum number of '
                 "oxygen atoms might help. But that's not specific enough.\n"
                 '\n'
                 'The challenge is creating a SMARTS query that accurately '
                 'captures the cucurbitane skeleton. Without a precise SMARTS, '
                 'the function might miss or falsely include compounds. Given '
                 'the complexity, the function might return (None, None) if '
                 "it's too hard. But the user expects an attempt.\n"
                 '\n'
                 'Perhaps start by checking the molecular formula. '
                 'Triterpenoids have 30 carbons (cucurbitane is C30H54). But '
                 'derivatives might have substitutions, so the carbon count '
                 'could vary. Maybe check if the molecule has at least 30 '
                 'carbons. Then check for the tetracyclic structure.\n'
                 '\n'
                 "Alternatively, use RDKit's ring detection. Find if the "
                 'molecule has four fused rings. But how to ensure they form '
                 'the cucurbitane structure?\n'
                 '\n'
                 'This is tricky. Maybe the best approach is to look for a '
                 "specific substructure that's characteristic of "
                 'cucurbitacins. For example, a SMARTS pattern that matches '
                 'the core rings with certain substitutions.\n'
                 '\n'
                 'After some research, cucurbitane has a specific structure: a '
                 '19(10→9β)-abeo-10α-lanost-5-ene. Creating a SMARTS for this '
                 'is difficult. Alternatively, use a simplified pattern that '
                 'matches the four fused rings with certain bridge '
                 'structures.\n'
                 '\n'
                 'Alternatively, check for the presence of multiple hydroxyl '
                 'groups and ketones, along with a certain number of rings. '
                 'For example, requiring at least three rings and multiple '
                 'oxygen atoms.\n'
                 '\n'
                 'Given the time constraints, perhaps proceed with a '
                 'simplified approach. Check for the presence of a tetracyclic '
                 'system (four rings), a certain number of oxygen atoms, and '
                 'molecular weight consistent with triterpenoids.\n'
                 '\n'
                 'So, the steps could be:\n'
                 '\n'
                 '1. Parse the SMILES into a molecule.\n'
                 "2. Check if it's a valid molecule.\n"
                 "3. Check the number of rings. If it's less than four, return "
                 'False.\n'
                 '4. Check for oxygen atoms (like hydroxyls, ketones).\n'
                 '5. Check molecular weight (triterpenoids are around 400-500 '
                 'g/mol).\n'
                 '\n'
                 'But this is very generic and might not be accurate. However, '
                 'given the complexity, this might be the best starting '
                 'point.\n'
                 '\n'
                 'Alternatively, look for a specific substructure. For '
                 'example, a SMARTS pattern that includes four fused rings '
                 'with certain bridgeheads. But creating such a SMARTS is '
                 'challenging.\n'
                 '\n'
                 'Another idea: Check if the molecule has a cucurbitane-like '
                 'core by using a SMARTS pattern that captures part of the '
                 'structure. For example, a pattern with three fused '
                 'six-membered rings and one five-membered ring, or something '
                 'similar.\n'
                 '\n'
                 'Alternatively, look for the presence of a bridge in the '
                 'structure, which is common in cucurbitacins. A bridged '
                 'bicyclic system might be a feature.\n'
                 '\n'
                 'But without a precise SMARTS pattern, this approach might '
                 'not work. Maybe the function can check for the presence of '
                 'multiple oxygen atoms and a certain ring system, then return '
                 'True with a reason, acknowledging the limitations.\n'
                 '\n'
                 'In the example given for triglyceride, they checked for '
                 'specific ester groups and the glycerol backbone. Similarly, '
                 'for cucurbitacin, we need to find a characteristic '
                 'substructure.\n'
                 '\n'
                 'After some consideration, the assistant might proceed with a '
                 'basic check for the tetracyclic system and oxygen content, '
                 "even if it's not perfect. The function would return (None, "
                 "None) if it's too hard, but the user prefers an attempt.\n"
                 '\n'
                 "So, here's a possible approach:\n"
                 '\n'
                 '- Use SMARTS to find a tetracyclic core.\n'
                 '- Check for multiple oxygen atoms (like hydroxyl, ketone '
                 'groups).\n'
                 '- Verify molecular weight is within a certain range.\n'
                 '\n'
                 'But creating the SMARTS for tetracyclic is challenging. '
                 'Maybe count the number of rings and ensure they are fused.\n'
                 '\n'
                 'Alternatively, use the number of SSSR (smallest set of '
                 'smallest rings) to determine if there are four rings. '
                 'However, the exact count might vary based on substituents.\n'
                 '\n'
                 'Given that cucurbitane is a tetracyclic triterpenoid, '
                 'perhaps the molecule should have four rings in its core. '
                 "Let's proceed with that.\n"
                 '\n'
                 'So, the code steps:\n'
                 '\n'
                 '1. Parse the SMILES.\n'
                 '2. Check validity.\n'
                 '3. Get the smallest set of smallest rings (SSSR). If the '
                 'count is less than 4, return False.\n'
                 '4. Check for oxygen atoms (maybe at least 5 oxygen atoms as '
                 'in many examples).\n'
                 '5. Check molecular weight is above 400 (approximate for '
                 'triterpenoids).\n'
                 '\n'
                 'But this is very generic and might lead to false '
                 'positives/negatives. However, given the complexity, this '
                 'might be the best approach possible without a specific '
                 'SMARTS pattern.\n'
                 '\n'
                 'Alternatively, look for a specific arrangement of rings '
                 'using SMARTS. For example, a pattern that includes four '
                 'fused rings with certain bridge connections. But creating '
                 'such a pattern is beyond my current knowledge.\n'
                 '\n'
                 "In the example, the user's previous code had SMILES in the "
                 'code block, causing syntax errors. The correct code should '
                 'have proper Python syntax with RDKit functions.\n'
                 '\n'
                 'So, the corrected code would:\n'
                 '\n'
                 '- Import necessary RDKit modules.\n'
                 '- Define the function is_cucurbitacin.\n'
                 '- Parse the SMILES.\n'
                 '- Check for the core structure using SMARTS (if possible).\n'
                 '- Check other features like oxygen count, molecular weight.\n'
                 '- Return True/False with a reason.\n'
                 '\n'
                 'But without a precise SMARTS, the function might not be '
                 'accurate. However, the user provided examples of '
                 'cucurbitacins, so perhaps a SMARTS can be derived from one '
                 'of them.\n'
                 '\n'
                 'Alternatively, use a SMARTS pattern that matches a common '
                 'substructure in the examples. For instance, a core with '
                 'multiple rings and oxygen atoms.\n'
                 '\n'
                 "For example, looking at cucurbitacin E's SMILES: "
                 '[H][C@@]12CC=C3[C@@]([H])(C=C(O)C(=O)C3(C)C)[C@]1(C)C(=O)C[C@]1(C)[C@]([H])([C@H](O)C[C@@]21C)[C@@](C)(O)C(=O)\\C=C\\C(C)(C)OC(C)=O\n'
                 '\n'
                 'The core has multiple rings and oxygen atoms. A SMARTS '
                 'pattern that captures part of this structure could be '
                 'helpful.\n'
                 '\n'
                 'But creating such a SMARTS requires expertise. '
                 'Alternatively, check for the presence of multiple ketone '
                 'groups (C=O) and hydroxyl groups (-O).\n'
                 '\n'
                 'In conclusion, the code should include checks for:\n'
                 '\n'
                 '- Valid SMILES.\n'
                 '- Presence of a tetracyclic system (possibly via SSSR '
                 'count).\n'
                 '- Multiple oxygen-containing groups.\n'
                 '- Molecular weight in a certain range.\n'
                 '\n'
                 "Here's the code attempt:",
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 14,
    'num_false_positives': 328,
    'num_true_negatives': 141905,
    'num_false_negatives': 53,
    'num_negatives': None,
    'precision': 0.04093567251461988,
    'recall': 0.208955223880597,
    'f1': 0.06845965770171149,
    'accuracy': 0.9973225579761068,
    'negative_predictive_value': 0.9996266501359558}