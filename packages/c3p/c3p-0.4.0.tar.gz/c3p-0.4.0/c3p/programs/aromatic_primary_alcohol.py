"""
Classifies: CHEBI:33857 aromatic primary alcohol
"""
"""
Classifies: CHEBI:134307 aromatic primary alcohol
"""
from rdkit import Chem

def is_aromatic_primary_alcohol(smiles: str):
    """
    Determines if a molecule is an aromatic primary alcohol based on its SMILES string.
    An aromatic primary alcohol has a hydroxyl group (-OH) attached to a primary carbon
    that is directly bonded to an aromatic ring.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is an aromatic primary alcohol, False otherwise
        str: Reason for classification
    """
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Define SMARTS pattern for primary alcohol attached to aromatic carbon
    # [c] is aromatic carbon, [CH2;D2] is methylene group with exactly two bonds (to OH and aromatic carbon)
    pattern = Chem.MolFromSmarts('[c]-[CH2;D2]-[OH]')
    
    # Check for matches
    matches = mol.GetSubstructMatches(pattern)
    
    if matches:
        return True, "Primary alcohol group attached to aromatic carbon"
    else:
        return False, "No primary alcohol group adjacent to aromatic ring found"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:33857',
                          'name': 'aromatic primary alcohol',
                          'definition': 'Any primary alcohol in which the '
                                        'alcoholic hydroxy group is attached '
                                        'to a carbon which is itself bonded to '
                                        'an aromatic ring.',
                          'parents': ['CHEBI:15734', 'CHEBI:33854'],
                          'xrefs': ['KEGG:C03485'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 23,
                           'log_lines_of_code': 3.1354942159291497,
                           'indent_by_line': [   1,
                                                 1,
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
                                                 0,
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
                                                 2],
                           'max_indent': 2,
                           'imports': ['from rdkit import Chem'],
                           'imports_count': 1,
                           'methods_called': [   'GetSubstructMatches',
                                                 'MolFromSmiles',
                                                 'MolFromSmarts'],
                           'methods_called_count': 3,
                           'smarts_strings': ['[c]-[CH2;D2]-[OH]'],
                           'smarts_strings_count': 1,
                           'defs': [   'is_aromatic_primary_alcohol(smiles: '
                                       'str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'True, "Primary alcohol group '
                                          'attached to aromatic carbon"',
                                          'False, "No primary alcohol group '
                                          'adjacent to aromatic ring found"'],
                           'returns_count': 3,
                           'complexity': 2.42709884318583},
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
    'sample_true_negatives': [   {   'smiles': 'OC1=CC=C(C[C@@H](O)[C@@H](O)CC=2C3=C(C=CC=C3)NC2)C=C1',
                                     'name': 'Diolmycin A1',
                                     'reason': 'No primary alcohol group '
                                               'adjacent to aromatic ring '
                                               'found'},
                                 {   'smiles': 'P(OC[C@H](OC(=O)CCCCCCCCCCCCCCCCCCCC)COC(=O)CCCCCCCCC/C=C\\CCCCCCCC)(O)(O)=O',
                                     'name': 'PA(20:1(11Z)/21:0)',
                                     'reason': 'No primary alcohol group '
                                               'adjacent to aromatic ring '
                                               'found'},
                                 {   'smiles': 'CCOC1=CC=C(C=C1)N2C(=C3C(=NN=C(C3=N2)SCCN4CCCC4)C)C',
                                     'name': '2-(4-ethoxyphenyl)-3,4-dimethyl-7-[2-(1-pyrrolidinyl)ethylthio]pyrazolo[3,4-d]pyridazine',
                                     'reason': 'No primary alcohol group '
                                               'adjacent to aromatic ring '
                                               'found'},
                                 {   'smiles': 'OS(=O)(=O)OC1CCC2C(CCC3C4CCCC4CCC23)C1',
                                     'name': 'Steryl sulfate',
                                     'reason': 'No primary alcohol group '
                                               'adjacent to aromatic ring '
                                               'found'},
                                 {   'smiles': 'C[C@@H]1CN(C(=O)C2=C(N=CC(=C2)C3=CCCCC3)O[C@H]1CN(C)C(=O)CC4=CC=NC=C4)[C@@H](C)CO',
                                     'name': 'N-[[(2R,3R)-8-(1-cyclohexenyl)-5-[(2S)-1-hydroxypropan-2-yl]-3-methyl-6-oxo-3,4-dihydro-2H-pyrido[2,3-b][1,5]oxazocin-2-yl]methyl]-N-methyl-2-pyridin-4-ylacetamide',
                                     'reason': 'No primary alcohol group '
                                               'adjacent to aromatic ring '
                                               'found'},
                                 {   'smiles': 'O=C(O)C(=C(C)C)CCC(=O)O',
                                     'name': '2-(1-Methylethylidene)pentanedioic '
                                             'acid',
                                     'reason': 'No primary alcohol group '
                                               'adjacent to aromatic ring '
                                               'found'},
                                 {   'smiles': 'O1C(C(O)C(O)C(OC)C1COC(=O)/C=C/C2=CC(O)=C(O)C=C2)C3=C(O)C4=C(OC(=CC4=O)C5=CC(O)=C(O)C=C5)C=C3O',
                                     'name': "4''-Methyl-6''-(3,4-dihydroxy-E-cinnamoyl)isoorientin",
                                     'reason': 'No primary alcohol group '
                                               'adjacent to aromatic ring '
                                               'found'},
                                 {   'smiles': 'O=C1C2=CC(=O)CC[C@@]2([C@H]3CC[C@]4([C@H]([C@@]53[C@H]1O5)CC[C@@H]4[C@@H](/C=C/[C@@H](C(C)C)C)C)C)C',
                                     'name': 'Talarosterone',
                                     'reason': 'No primary alcohol group '
                                               'adjacent to aromatic ring '
                                               'found'},
                                 {   'smiles': 'C1C[C@@H]([C@@H](O[C@H]1CCNS(=O)(=O)C2=CC=CC=C2Cl)CO)NC(=O)CC3=CN=CC=C3',
                                     'name': 'N-[(2R,3S,6R)-6-[2-[(2-chlorophenyl)sulfonylamino]ethyl]-2-(hydroxymethyl)-3-oxanyl]-2-(3-pyridinyl)acetamide',
                                     'reason': 'No primary alcohol group '
                                               'adjacent to aromatic ring '
                                               'found'},
                                 {   'smiles': 'SC[C@H](NC(=O)[C@@H](N)CC(O)=O)C(=O)N[C@@H](CS)C(O)=O',
                                     'name': 'Asp-Cys-Cys',
                                     'reason': 'No primary alcohol group '
                                               'adjacent to aromatic ring '
                                               'found'}],
    'sample_false_negatives': [   {   'smiles': 'C=1C2=C(C=CC1)SC(=C2)C(=O)N[C@@H](CC(C)C)C(=O)N3CCN(CC3)C(=O)[C@H](CO)NS(C=4C=CC(=CC4Cl)Cl)(=O)=O',
                                      'name': 'GSK1016790A',
                                      'reason': 'No primary alcohol group '
                                                'adjacent to aromatic ring '
                                                'found'}],
    'attempt': 1,
    'reasoning': '</think>\n'
                 '\n'
                 "Okay, let's tackle this problem step by step. The goal is to "
                 'write a Python function using RDKit to determine if a given '
                 'SMILES string represents an aromatic primary alcohol. The '
                 'definition is that the alcoholic hydroxy group is attached '
                 'to a carbon which is bonded to an aromatic ring. \n'
                 '\n'
                 'First, I need to understand the structural requirements. A '
                 'primary alcohol has the hydroxyl (-OH) group attached to a '
                 'carbon that is connected to at most one other carbon. '
                 'Additionally, that carbon must be part of or adjacent to an '
                 'aromatic ring. \n'
                 '\n'
                 'So, the steps I need to check are:\n'
                 '\n'
                 '1. **Check for the presence of a hydroxyl group (-OH):** The '
                 "molecule must have at least one -OH group. But wait, it's "
                 'specifically an alcohol, so the hydroxyl should be an '
                 'alcoholic OH, not part of a carboxylic acid or other group. '
                 'Maybe using a SMARTS pattern to find hydroxyl groups '
                 "attached to a carbon that isn't part of a carbonyl group.\n"
                 '\n'
                 '2. **Identify the carbon attached to the hydroxyl group:** '
                 'This carbon is the one we need to check. It should be a '
                 'primary carbon, meaning it has only one adjacent carbon '
                 '(since primary alcohols have the OH on a carbon connected to '
                 'one other carbon). Wait, primary alcohol definition: the '
                 'carbon with OH is attached to exactly one other carbon. So '
                 "the carbon with OH (let's call it the 'alcohol carbon') "
                 'should have only one neighboring carbon atom. So, the '
                 "alcohol carbon is a CH2OH group? Or maybe CH3-OH but that's "
                 'methanol, which is primary. Wait, primary alcohol is when '
                 "the OH is on a carbon that's connected to only one other "
                 'carbon. So the alcohol carbon has one adjacent carbon. So '
                 'the structure is R-CH2-OH, where R is the rest of the '
                 'molecule. Wait, no: methanol (CH3OH) is primary. Ethanol '
                 '(CH2CH2OH) is primary if the OH is on the end carbon. Wait, '
                 'primary alcohol is when the hydroxyl-bearing carbon has only '
                 'one carbon attached. So methanol (1°), ethanol (the OH is on '
                 'a primary carbon), 1-propanol, etc. So the alcohol carbon '
                 'must have exactly one neighboring carbon. So in SMARTS, that '
                 'would be [CH2]-OH. But wait, the alcohol carbon could be CH3 '
                 "(if it's methanol), which is [CH3]-OH. But in that case, the "
                 "carbon has zero neighboring carbons. Wait, no. Methanol's "
                 'structure is C-O-H. The carbon is connected to three Hs and '
                 'one O. So in that case, the alcohol carbon has no other '
                 'carbons attached. So for primary alcohols, the alcohol '
                 'carbon can have zero or one adjacent carbons? Wait, no. '
                 'Wait, primary, secondary, tertiary refers to the number of '
                 'carbon atoms attached to the alcohol-bearing carbon. '
                 'Primary: one carbon attached (so the alcohol carbon is '
                 'connected to one other carbon). Wait, no: in ethanol '
                 "(CH2CH2OH), the alcohol is on a carbon that's attached to "
                 'two carbons (the adjacent one and the rest). Wait, no: '
                 "ethanol is CH3CH2OH. The OH is on a carbon that's connected "
                 'to two other carbons (the CH3 and another CH2). Wait, no: '
                 'the structure is CH3-CH2-OH. The OH is on the second carbon. '
                 'That carbon is connected to two other carbons (the CH3 and '
                 'the adjacent CH2). Wait, no: in ethanol, the OH is on the '
                 'terminal carbon. The carbon with OH (the second carbon) is '
                 'connected to two other carbons: the first carbon (CH3) and '
                 "the adjacent (but since it's CH2OH, that carbon has two Hs, "
                 'one O, and one connection to the first carbon. Wait, maybe '
                 "I'm getting confused here. Let me clarify:\n"
                 '\n'
                 'Primary alcohol: the carbon bearing the hydroxyl group is '
                 'attached to exactly one other carbon. So, for example, '
                 "methanol is a primary alcohol (but it's attached to zero "
                 "carbons). Wait, that's conflicting. Maybe the IUPAC "
                 'definition is different. Let me check: According to IUPAC, '
                 'primary alcohols have the hydroxyl group attached to a '
                 'primary carbon, which is a carbon atom attached to only one '
                 "other carbon atom. So methanol's carbon is attached to zero "
                 "other carbons, but it's still considered primary. Wait, "
                 "maybe I'm wrong. Let me confirm. \n"
                 '\n'
                 'Wait, actually, the classification is based on how many '
                 'carbon atoms are bonded to the carbon with the hydroxyl '
                 'group. For primary (1°), the carbon is bonded to one other '
                 'carbon; secondary (2°), two; tertiary (3°), three. '
                 "Methanol's carbon has zero, but it's still considered "
                 'primary. Wait, no. Wait, methanol is considered a primary '
                 'alcohol because the hydroxyl-bearing carbon is only '
                 'connected to one carbon (in this case, none, but maybe the '
                 'classification is different). Hmm, this is a problem. Wait, '
                 'maybe the definition here is that a primary alcohol is when '
                 'the hydroxyl group is on a carbon that is at the end of the '
                 "carbon chain. But that's not precise. \n"
                 '\n'
                 'Alternatively, maybe the correct approach is to look for a '
                 'hydroxyl group attached to a carbon that has exactly one '
                 'adjacent carbon (i.e., the carbon with OH is connected to '
                 "one carbon and two hydrogens). Wait, but methanol's carbon "
                 'has no adjacent carbons. So perhaps the initial approach is '
                 'incorrect. \n'
                 '\n'
                 "Wait, the user provided examples. Let's look at some of "
                 'them. For example, 3,4-dimethylbenzyl alcohol: SMILES '
                 'CC1=CC=C(CO)C=C1C. The benzyl alcohol part is the CO group '
                 'attached to the benzene ring. The CO is CH2OH. So the carbon '
                 'with OH (the CH2OH) is attached to the benzene ring. So in '
                 'this case, the alcohol carbon (the CH2) is connected to the '
                 'benzene ring (which is an aromatic carbon) and has one '
                 "adjacent carbon (the benzene ring's carbon). Wait, but the "
                 'benzene ring is a ring of carbons. So the alcohol carbon '
                 "(the CH2OH) is attached to one carbon (the aromatic ring's "
                 'carbon). Therefore, this is a primary alcohol. \n'
                 '\n'
                 'Another example: 2-methylbenzyl alcohol: SMILES '
                 'CC1=C(CO)C=CC=C1. Here, the CO is attached to the benzene '
                 'ring. The alcohol carbon is CH2, connected to the benzene '
                 "carbon (one adjacent carbon) and two hydrogens. So that's a "
                 'primary alcohol. \n'
                 '\n'
                 'So the key points are:\n'
                 '\n'
                 "- The hydroxyl group is on a carbon (let's call it C1) that "
                 'is a primary carbon (i.e., C1 is connected to exactly one '
                 'other carbon atom). \n'
                 '\n'
                 '- That one other carbon (C2) must be part of an aromatic '
                 'ring. \n'
                 '\n'
                 'So the steps to check:\n'
                 '\n'
                 '1. Find all hydroxyl (-OH) groups in the molecule. For each, '
                 "check if it's an alcoholic OH (not part of a carboxylic "
                 'acid, etc.). \n'
                 '\n'
                 '2. For each alcoholic OH, get the attached carbon (C1). \n'
                 '\n'
                 '3. Check that C1 has exactly one neighboring carbon (C2). \n'
                 '\n'
                 '4. Check that C2 is part of an aromatic ring. \n'
                 '\n'
                 'Additionally, need to ensure that the hydroxyl group is not '
                 'part of a more complex structure (like a phenol, which would '
                 "be directly attached to the aromatic ring, but that's a "
                 'different class). Wait, but in the examples, the hydroxyl is '
                 'on a CH2 group attached to the aromatic ring. So the '
                 'structure is Ar-CH2-OH, where Ar is aromatic. Phenol would '
                 'be Ar-OH directly, which is not considered here. \n'
                 '\n'
                 'So the plan is:\n'
                 '\n'
                 '- Use SMARTS patterns to find the -CH2-OH group attached to '
                 'an aromatic carbon. \n'
                 '\n'
                 "But wait, the CH2-OH group's carbon (C1) must be connected "
                 'to exactly one carbon (C2), which is aromatic. \n'
                 '\n'
                 'So the SMARTS pattern could be: [OH]-[CH2]-[c] where [c] is '
                 'an aromatic carbon. \n'
                 '\n'
                 'Wait, but [c] represents any aromatic carbon. So the pattern '
                 'would be [OH]-[CH2]-c. But maybe the connection is not '
                 'directly to the aromatic ring. For example, if the CH2 is '
                 'part of a chain that connects to the aromatic ring. Wait, '
                 'no, the definition says the alcoholic hydroxy group is '
                 'attached to a carbon which is itself bonded to an aromatic '
                 'ring. So the carbon with the OH (C1) must be bonded directly '
                 'to an aromatic carbon (C2). \n'
                 '\n'
                 'So the structure is: C1 (with OH) is connected to C2 '
                 "(aromatic), and C1 has no other carbons attached (since it's "
                 'primary). Wait, no. Because C1 is a primary carbon, it can '
                 'have one adjacent carbon (C2). So C1 is connected to C2 and '
                 'two Hs and the OH. \n'
                 '\n'
                 'So the SMARTS pattern would be [OH]-[CH2]-[c]. \n'
                 '\n'
                 'But wait, the CH2 could be part of a longer chain. For '
                 'example, if the structure is Ar-CH2-CH2-OH, then the OH is '
                 "on a secondary carbon. So that's not a primary alcohol. So "
                 'to ensure that the OH is on a primary carbon, the carbon '
                 'attached to OH (C1) must have only one carbon neighbor (C2), '
                 'which is part of an aromatic ring. \n'
                 '\n'
                 'Therefore, the SMARTS pattern should be: [OH]-[CH2]-[c] '
                 'where the [CH2] has exactly one carbon neighbor (the '
                 'aromatic one). \n'
                 '\n'
                 'In RDKit SMARTS, that can be represented as '
                 '[OH]-[CH2;D1]-[c]. Wait, no. The [CH2;D1] would mean that '
                 'the CH2 has a degree of 1 (only one bond to another atom). '
                 'But in reality, the CH2 is connected to the OH (O), the '
                 'aromatic carbon (C2), and two Hs. So the degree of the CH2 '
                 "is 2 (two bonds: one to O, one to C2). Wait, no. The CH2's "
                 'degree is the number of bonds. The CH2 is connected to O '
                 '(single bond), C2 (single bond), and two Hs. So total of '
                 'four bonds? Wait, no. Carbon can have four bonds. So in '
                 'CH2OH attached to C2, the structure is C2-C(-O-H)(H)(H). So '
                 'the carbon (C1) has bonds to C2, O, and two Hs. So the '
                 'degree (number of neighbors) is 2: C2 and O. Wait, no. The '
                 'degree is the number of connected atoms. The C1 is bonded to '
                 'C2 and O. The Hs are not counted as separate atoms in the '
                 'SMARTS. So the degree of C1 is 2. \n'
                 '\n'
                 'So to find a carbon (C1) that has exactly two neighbors: one '
                 'O (from OH) and one C (C2, which is aromatic). So the SMARTS '
                 'would be [OH]-[CH2]-[c], and the CH2 must have exactly two '
                 'neighbors (O and C). \n'
                 '\n'
                 'But in RDKit, the degree (D) is the number of explicit '
                 'bonds. So [CH2] with degree 2. \n'
                 '\n'
                 'So the SMARTS pattern would be: [OH]-[CH2;D2]-[c]. \n'
                 '\n'
                 'Wait, but the CH2 has two bonds: one to O and one to C. So '
                 'D2. \n'
                 '\n'
                 'But wait, the actual molecule might have the CH2 connected '
                 'to other atoms. For example, if the structure is '
                 'Ar-CH2-O-something else, but in our case, the OH must be '
                 'directly attached. So the correct SMARTS would be '
                 '[OH]-[CH2]-[c], and the CH2 must have exactly two neighbors '
                 '(O and C). \n'
                 '\n'
                 'Alternatively, using the SMARTS [c]-[CH2]-[OH]. \n'
                 '\n'
                 'But how to ensure that the CH2 has only those two '
                 'connections (i.e., no other atoms attached)? \n'
                 '\n'
                 'Wait, the CH2 in this context would have two single bonds: '
                 'one to the aromatic carbon and one to the OH group. The '
                 'remaining two bonds are to hydrogen atoms. So in the SMARTS, '
                 'we can represent this as [c]-[CH2]-[OH], where the CH2 has '
                 'exactly two bonds (to c and OH). \n'
                 '\n'
                 'But in RDKit, the SMARTS [CH2] would match any carbon with '
                 'two hydrogens, regardless of the number of bonds. Wait, no. '
                 'The [CH2] in SMARTS matches a carbon atom with two '
                 'hydrogens. The actual bonds (single, double, etc.) are '
                 'specified. So [CH2] would match a carbon with two Hs, but '
                 'the number of bonds (degree) can vary. \n'
                 '\n'
                 'So to ensure that the CH2 is connected to exactly two atoms '
                 '(the aromatic carbon and the OH), we can use [CH2;D2], which '
                 'means the carbon has two bonds (excluding hydrogens). \n'
                 '\n'
                 'So the SMARTS pattern would be: [c]-[CH2;D2]-[OH]. \n'
                 '\n'
                 'This would match a carbon (CH2) connected to an aromatic '
                 'carbon (c) and an OH group, with exactly two bonds (so no '
                 'other substituents). \n'
                 '\n'
                 'But wait, in the case where the CH2 is part of a ring? For '
                 'example, if the aromatic ring is part of a fused ring system '
                 'and the CH2-OH is attached. But according to the problem '
                 "statement, the examples don't include such cases. \n"
                 '\n'
                 'So, the plan is:\n'
                 '\n'
                 '1. Parse the SMILES into a molecule.\n'
                 '\n'
                 '2. Check if the molecule has at least one hydroxyl group '
                 '(-OH).\n'
                 '\n'
                 "3. For each hydroxyl group, check if it's attached to a CH2 "
                 'group that is directly bonded to an aromatic carbon.\n'
                 '\n'
                 '4. Ensure that the CH2 group has only two bonds (to the '
                 'aromatic carbon and the OH), making it a primary alcohol.\n'
                 '\n'
                 'Additionally, need to make sure that the hydroxyl is not '
                 'part of a carboxylic acid or other group. For example, in a '
                 'carboxylic acid (COOH), the OH is not an alcohol. So we need '
                 'to exclude such cases. \n'
                 '\n'
                 'To do that, the hydroxyl group should not be adjacent to a '
                 'carbonyl group (C=O). So the SMARTS pattern should not match '
                 'if the OH is next to a carbonyl. \n'
                 '\n'
                 'So, perhaps the steps are:\n'
                 '\n'
                 '- Find all OH groups where the attached carbon is not part '
                 'of a carbonyl group.\n'
                 '\n'
                 'So, first, find all OH groups that are alcohols. \n'
                 '\n'
                 'Then, for each such OH group, check if the attached carbon '
                 'is a CH2 connected to an aromatic carbon. \n'
                 '\n'
                 'Putting this together:\n'
                 '\n'
                 'Use a SMARTS pattern that matches [OH] where the carbon is '
                 'not part of a carbonyl. \n'
                 '\n'
                 'The SMARTS for an alcohol OH (not carboxylic acid, etc.) '
                 'would be [OH]-[C;!$(C=O)]. \n'
                 '\n'
                 'Wait, maybe. Because in a carboxylic acid, the OH is '
                 'attached to a carbon that is double-bonded to O. So the '
                 'pattern [OH]-[C;$(C=O)] would match carboxylic acid OH. So '
                 'to exclude that, we can use [OH]-[C;!$(C=O)]. \n'
                 '\n'
                 'But maybe a better way is to ensure that the carbon attached '
                 'to OH is not double-bonded to an oxygen. \n'
                 '\n'
                 'Alternatively, use a SMARTS that matches [OH]-[CX4], which '
                 'is a carbon with four single bonds. But in the case of '
                 'CH2OH, the carbon would have two Hs, one O, and one bond to '
                 "the aromatic carbon. So that's three bonds? Wait, no. The "
                 'carbon would have four bonds: two to H, one to O, and one to '
                 'the aromatic carbon. So valence is correct. \n'
                 '\n'
                 'So the SMARTS pattern could be [OH]-[CX4]-[c], where [CX4] '
                 'is a carbon with four bonds (i.e., saturated). \n'
                 '\n'
                 "But maybe that's not sufficient. Let's think. \n"
                 '\n'
                 'Alternatively, use a SMARTS pattern that finds the structure '
                 '[c]-CH2-OH. \n'
                 '\n'
                 'The SMARTS for that would be [c]-[CH2]-[OH]. \n'
                 '\n'
                 'But this would match any OH attached to a CH2 that is '
                 'connected to an aromatic carbon. However, this might include '
                 'cases where the CH2 has other substituents. For example, if '
                 'the CH2 is part of a larger chain. \n'
                 '\n'
                 'Wait, but according to the definition, the alcohol must be '
                 'primary. So the carbon with OH (C1) must have exactly one '
                 'adjacent carbon (C2), which is the aromatic carbon. \n'
                 '\n'
                 'So, the CH2 must be connected only to the aromatic carbon '
                 'and the OH. Therefore, the degree of C1 (the CH2) should be '
                 '2 (connected to C2 and O). \n'
                 '\n'
                 'So in SMARTS, [c]-[CH2;D2]-[OH]. \n'
                 '\n'
                 'This pattern would match a CH2 group connected to an '
                 'aromatic carbon and an OH, with no other connections. \n'
                 '\n'
                 'This should ensure that the alcohol is primary. \n'
                 '\n'
                 'So the steps in code would be:\n'
                 '\n'
                 '1. Parse the SMILES into a molecule. If invalid, return '
                 'False.\n'
                 '\n'
                 '2. Find all occurrences of the SMARTS pattern '
                 '[c]-[CH2;D2]-[OH].\n'
                 '\n'
                 '3. If at least one match is found, return True. Otherwise, '
                 'False.\n'
                 '\n'
                 'But wait, there could be multiple hydroxyl groups. For '
                 'example, a molecule with two -CH2-OH groups attached to '
                 'aromatic rings. But the definition allows for any primary '
                 'alcohol where the hydroxy group is attached to a carbon '
                 "bonded to an aromatic ring. So as long as there's at least "
                 'one such group, it should return True.\n'
                 '\n'
                 'But also, need to check that the hydroxyl group is indeed an '
                 'alcohol and not part of another functional group. For '
                 'example, if the OH is part of a nitro group or something '
                 'else. But the SMARTS pattern [OH] as a separate group should '
                 'handle that. \n'
                 '\n'
                 'Another consideration: the aromatic ring could be part of a '
                 'heterocycle. For example, pyridine is aromatic. So the '
                 'SMARTS [c] would match any aromatic carbon, including '
                 'heteroaromatics. \n'
                 '\n'
                 'Wait, in RDKit, the [c] atom symbol matches any aromatic '
                 'carbon, but not aromatic nitrogens, etc. So if the aromatic '
                 'ring is a pyridine, the nitrogen is not matched by [c]. So '
                 'the CH2-OH must be attached to an aromatic carbon (like '
                 'benzene, toluene, etc.), not a heteroaromatic atom. But the '
                 'examples include structures like 4-aminopyridine-3-methanol '
                 '(SMILES C=1C=NC=C(C1N)CO), which has the CO (CH2OH) attached '
                 "to a pyridine ring. The pyridine's carbons are aromatic, so "
                 'the [c] would match them. Wait, in pyridine, the carbons '
                 'adjacent to the nitrogen are aromatic carbons. So in this '
                 'case, the CH2OH is attached to a carbon in the pyridine '
                 'ring, which is considered aromatic. So the SMARTS [c] would '
                 'match that. \n'
                 '\n'
                 'Therefore, the SMARTS pattern [c]-[CH2;D2]-[OH] should work '
                 'for such cases. \n'
                 '\n'
                 "Now, let's test this approach against the examples. \n"
                 '\n'
                 'Take the example 3,4-dimethylbenzyl alcohol: SMILES '
                 'CC1=CC=C(CO)C=C1C. The CO here is CH2OH attached to the '
                 'benzene ring. The SMARTS pattern would match this, as the '
                 'CH2 is connected to an aromatic carbon (from the benzene) '
                 'and the OH. \n'
                 '\n'
                 'Another example: 4-(hydroxymethyl)benzoic acid: SMILES '
                 'O=C(O)C1=CC=C(CO)C=C1. Here, the CO is CH2OH attached to the '
                 'benzene ring. The SMARTS would match, so this should return '
                 'True. But wait, the benzoic acid part is a carboxylic acid. '
                 'However, the hydroxyl in the CO (CH2OH) is a separate '
                 'alcohol group. So the code should still identify it as an '
                 'aromatic primary alcohol. \n'
                 '\n'
                 'But wait, in this case, the molecule has a carboxylic acid '
                 'group (O=C(O)-), but the code is looking for the CH2OH '
                 'attached to the aromatic ring. The presence of the '
                 "carboxylic acid shouldn't affect the detection of the "
                 'alcohol group. \n'
                 '\n'
                 'Another example: salicin (SMILES '
                 'OC[C@H]1O[C@@H](Oc2ccccc2CO)[C@H](O)[C@@H](O)[C@@H]1O). This '
                 'has a benzyl alcohol group (the CO attached to the benzene '
                 'ring). The code should detect that. \n'
                 '\n'
                 'So the SMARTS pattern seems correct. \n'
                 '\n'
                 'Now, possible issues:\n'
                 '\n'
                 '- The molecule might have the OH group in a different '
                 'environment, like being part of a hemiacetal or other '
                 'structure. But according to the problem statement, the '
                 "function should return True as long as there's at least one "
                 'primary alcohol group attached to an aromatic carbon. \n'
                 '\n'
                 'Another possible edge case: the CH2OH is part of a ring. For '
                 'example, if the aromatic ring is part of a fused ring system '
                 'where the CH2OH is attached. But the SMARTS pattern should '
                 'still match as long as the CH2 is connected to an aromatic '
                 'carbon. \n'
                 '\n'
                 'Now, implementing this in code:\n'
                 '\n'
                 'The code needs to:\n'
                 '\n'
                 '1. Read the SMILES and create a molecule.\n'
                 '\n'
                 '2. Check if the molecule is valid.\n'
                 '\n'
                 '3. Apply the SMARTS pattern [c]-[CH2;D2]-[OH].\n'
                 '\n'
                 '4. If any matches, return True with the reason.\n'
                 '\n'
                 'But wait, the hydroxyl group could be deprotonated (like in '
                 'a salt), but SMILES usually represents the neutral form. So '
                 'assuming the input SMILES is correct.\n'
                 '\n'
                 'Another consideration: the molecule might have multiple '
                 'hydroxyl groups, but only one of them is the correct primary '
                 'alcohol. The code should still return True.\n'
                 '\n'
                 'Now, writing the code:\n'
                 '\n'
                 'First, import RDKit modules.\n'
                 '\n'
                 'Then, define the function '
                 'is_aromatic_primary_alcohol(smiles: str) -> (bool, str).\n'
                 '\n'
                 'Parse the SMILES into a molecule. If invalid, return False.\n'
                 '\n'
                 'Define the SMARTS pattern: [c]-[CH2;D2]-[OH].\n'
                 '\n'
                 'Check for substructure matches.\n'
                 '\n'
                 'If any matches found, return True. Else, False.\n'
                 '\n'
                 'But wait, the pattern [c]-[CH2;D2]-[OH] might not capture '
                 'all cases. For example, if the CH2 is part of a larger '
                 'substituent but still connected to an aromatic carbon. Wait, '
                 'no, because D2 ensures that the CH2 has exactly two bonds '
                 '(to the aromatic carbon and the OH). So any other '
                 'substituents would increase the degree beyond 2, making the '
                 'pattern not match. \n'
                 '\n'
                 'But wait, the CH2 has two bonds (to O and aromatic C), but '
                 'it can have hydrogen atoms. The D2 refers to the number of '
                 'bonds (excluding hydrogens). So in the case of CH2OH '
                 'attached to an aromatic carbon, the CH2 has two bonds (O and '
                 'C), so D2 is correct. \n'
                 '\n'
                 'Testing this with methanol: SMILES CO. The SMARTS would not '
                 "match because there's no aromatic carbon. So methanol would "
                 'correctly return False.\n'
                 '\n'
                 'Testing with benzyl alcohol (Ph-CH2-OH): SMILES OCCc1ccccc1. '
                 'Wait, the SMILES for benzyl alcohol is C1=CC=CC=C1CCO. Wait, '
                 'no. Benzyl alcohol is typically written as C1=CC=C(C=C1)CO. '
                 'So the SMARTS would match this. \n'
                 '\n'
                 'Another example: 4-(hydroxymethyl)benzaldehyde (SMILES '
                 'O=CC1=CC=C(CO)C=C1). The CH2OH is attached to the benzene '
                 'ring. The SMARTS would match, so it should return True. \n'
                 '\n'
                 'Now, code:\n'
                 '\n'
                 'from rdkit import Chem\n'
                 '\n'
                 'def is_aromatic_primary_alcohol(smiles: str):\n'
                 '    mol = Chem.MolFromSmiles(smiles)\n'
                 '    if mol is None:\n'
                 '        return False, "Invalid SMILES"\n'
                 '    \n'
                 '    # SMARTS pattern for [c]-CH2-OH where CH2 has degree 2 '
                 '(only connected to OH and aromatic carbon)\n'
                 "    pattern = Chem.MolFromSmarts('[c]-[CH2;D2]-[OH]')\n"
                 '    matches = mol.GetSubstructMatches(pattern)\n'
                 '    \n'
                 '    if matches:\n'
                 '        return True, "Primary alcohol group attached to '
                 'aromatic carbon"\n'
                 '    else:\n'
                 '        return False, "No matching primary alcohol group '
                 'found"\n'
                 '\n'
                 'Wait, but the pattern [c]-[CH2;D2]-[OH] might not account '
                 'for stereochemistry or different bond orders. But since the '
                 'bonds in the aromatic ring are aromatic, and the CH2-OH is '
                 'connected via single bonds, the SMARTS should work. \n'
                 '\n'
                 'Testing this code with the example SMILES provided:\n'
                 '\n'
                 'Take 3,4-dimethylbenzyl alcohol: CC1=CC=C(CO)C=C1C. The code '
                 'should find a match. \n'
                 '\n'
                 'Another example: 4-aminopyridine-3-methanol: '
                 'C=1C=NC=C(C1N)CO. The CO is attached to the pyridine ring. '
                 'The code should match. \n'
                 '\n'
                 "But wait, the pyridine's carbons are aromatic, so [c] would "
                 'match them. \n'
                 '\n'
                 'Potential issues:\n'
                 '\n'
                 '- The code might miss cases where the aromatic ring is part '
                 'of a larger system, but the SMARTS should still match as '
                 "long as there's a direct connection. \n"
                 '\n'
                 '- The code might incorrectly identify secondary alcohols if '
                 'the SMARTS is not specific enough. But with D2, it ensures '
                 'the CH2 has only two bonds (to O and aromatic C), making it '
                 'primary. \n'
                 '\n'
                 'Another possible issue: the hydroxyl group could be part of '
                 'a geminal diol (two OH groups on the same carbon), but the '
                 'definition requires a primary alcohol. However, in such a '
                 'case, the carbon would have more than two bonds (e.g., two '
                 'OHs and the aromatic carbon), so D2 would not match. \n'
                 '\n'
                 'Thus, the code should correctly identify primary aromatic '
                 'alcohols. \n'
                 '\n'
                 "In the previous attempt, the user's code had an indentation "
                 'error. The current code should fix that by properly '
                 'indenting the code block. \n'
                 '\n'
                 'Now, the code should correctly parse the SMILES, apply the '
                 'SMARTS pattern, and return True or False based on the '
                 'presence of the primary alcohol attached to an aromatic '
                 'carbon.',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 35,
    'num_false_positives': 788,
    'num_true_negatives': 141476,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.0425273390036452,
    'recall': 0.9722222222222222,
    'f1': 0.08149010477299184,
    'accuracy': 0.9944553759662684,
    'negative_predictive_value': 0.999992931713282}