"""
Classifies: CHEBI:35436 D-glucoside
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_D_glucoside(smiles: str):
    """
    Determines if a molecule is a D-glucoside based on its SMILES string.
    A D-glucoside has a beta-D-glucopyranose group linked via a glycosidic bond.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a D-glucoside, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES"
    
    # SMARTS pattern for beta-D-glucopyranose with glycosidic bond
    # Matches the glucopyranose ring with O-linked group at C1
    glucoside_pattern = Chem.MolFromSmarts("[C@H]1([C@@H](O)[C@H](O)[C@@H](O)[C@@H](O1)CO)O[!H]")
    if mol.HasSubstructMatch(glucoside_pattern):
        return True, "Contains beta-D-glucopyranose with glycosidic bond"
    
    # Alternative pattern considering different stereochemistry possibilities
    # Check for any glucopyranose with O-linkage at C1 and correct D-configuration
    # This pattern may need adjustment based on specific examples
    glucoside_pattern2 = Chem.MolFromSmarts("[OX2][C@@H]1[C@H](O)[C@@H](O)[C@H](O)[C@@H](O)[C@H]1O[!H]")
    if mol.HasSubstructMatch(glucoside_pattern2):
        return True, "Contains beta-D-glucopyranose with glycosidic bond"
    
    return False, "No beta-D-glucopyranose with glycosidic bond found"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:35436',
                          'name': 'D-glucoside',
                          'definition': 'Any glucoside in which the glycoside '
                                        'group is derived from D-glucose.',
                          'parents': ['CHEBI:24278'],
                          'xrefs': ['KEGG:C01798'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 24,
                           'log_lines_of_code': 3.1780538303479458,
                           'indent_by_line': [   1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
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
                           'methods_called': [   'MolFromSmiles',
                                                 'HasSubstructMatch',
                                                 'MolFromSmarts'],
                           'methods_called_count': 3,
                           'smarts_strings': [   '[OX2][C@@H]1[C@H](O)[C@@H](O)[C@H](O)[C@@H](O)[C@H]1O[!H]',
                                                 '[C@H]1([C@@H](O)[C@H](O)[C@@H](O)[C@@H](O1)CO)O[!H]'],
                           'smarts_strings_count': 2,
                           'defs': ['is_D_glucoside(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES"',
                                          'True, "Contains '
                                          'beta-D-glucopyranose with '
                                          'glycosidic bond"',
                                          'True, "Contains '
                                          'beta-D-glucopyranose with '
                                          'glycosidic bond"',
                                          'False, "No beta-D-glucopyranose '
                                          'with glycosidic bond found"'],
                           'returns_count': 4,
                           'complexity': 2.635610766069589},
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
                                     'reason': 'No beta-D-glucopyranose with '
                                               'glycosidic bond found'},
                                 {   'smiles': 'P(OC[C@H](OC(=O)CCCCCCCCCCCCCCCCCCCC)COC(=O)CCCCCCCCC/C=C\\CCCCCCCC)(O)(O)=O',
                                     'name': 'PA(20:1(11Z)/21:0)',
                                     'reason': 'No beta-D-glucopyranose with '
                                               'glycosidic bond found'},
                                 {   'smiles': 'CCOC1=CC=C(C=C1)N2C(=C3C(=NN=C(C3=N2)SCCN4CCCC4)C)C',
                                     'name': '2-(4-ethoxyphenyl)-3,4-dimethyl-7-[2-(1-pyrrolidinyl)ethylthio]pyrazolo[3,4-d]pyridazine',
                                     'reason': 'No beta-D-glucopyranose with '
                                               'glycosidic bond found'},
                                 {   'smiles': 'OS(=O)(=O)OC1CCC2C(CCC3C4CCCC4CCC23)C1',
                                     'name': 'Steryl sulfate',
                                     'reason': 'No beta-D-glucopyranose with '
                                               'glycosidic bond found'},
                                 {   'smiles': 'C[C@@H]1CN(C(=O)C2=C(N=CC(=C2)C3=CCCCC3)O[C@H]1CN(C)C(=O)CC4=CC=NC=C4)[C@@H](C)CO',
                                     'name': 'N-[[(2R,3R)-8-(1-cyclohexenyl)-5-[(2S)-1-hydroxypropan-2-yl]-3-methyl-6-oxo-3,4-dihydro-2H-pyrido[2,3-b][1,5]oxazocin-2-yl]methyl]-N-methyl-2-pyridin-4-ylacetamide',
                                     'reason': 'No beta-D-glucopyranose with '
                                               'glycosidic bond found'},
                                 {   'smiles': 'O=C(O)C(=C(C)C)CCC(=O)O',
                                     'name': '2-(1-Methylethylidene)pentanedioic '
                                             'acid',
                                     'reason': 'No beta-D-glucopyranose with '
                                               'glycosidic bond found'},
                                 {   'smiles': 'O1C(C(O)C(O)C(OC)C1COC(=O)/C=C/C2=CC(O)=C(O)C=C2)C3=C(O)C4=C(OC(=CC4=O)C5=CC(O)=C(O)C=C5)C=C3O',
                                     'name': "4''-Methyl-6''-(3,4-dihydroxy-E-cinnamoyl)isoorientin",
                                     'reason': 'No beta-D-glucopyranose with '
                                               'glycosidic bond found'},
                                 {   'smiles': 'O=C1C2=CC(=O)CC[C@@]2([C@H]3CC[C@]4([C@H]([C@@]53[C@H]1O5)CC[C@@H]4[C@@H](/C=C/[C@@H](C(C)C)C)C)C)C',
                                     'name': 'Talarosterone',
                                     'reason': 'No beta-D-glucopyranose with '
                                               'glycosidic bond found'},
                                 {   'smiles': 'C1C[C@@H]([C@@H](O[C@H]1CCNS(=O)(=O)C2=CC=CC=C2Cl)CO)NC(=O)CC3=CN=CC=C3',
                                     'name': 'N-[(2R,3S,6R)-6-[2-[(2-chlorophenyl)sulfonylamino]ethyl]-2-(hydroxymethyl)-3-oxanyl]-2-(3-pyridinyl)acetamide',
                                     'reason': 'No beta-D-glucopyranose with '
                                               'glycosidic bond found'},
                                 {   'smiles': 'SC[C@H](NC(=O)[C@@H](N)CC(O)=O)C(=O)N[C@@H](CS)C(O)=O',
                                     'name': 'Asp-Cys-Cys',
                                     'reason': 'No beta-D-glucopyranose with '
                                               'glycosidic bond found'}],
    'sample_false_negatives': [   {   'smiles': 'OC[C@H]1O[C@@H](O[C@@H](C#N)c2ccc(O)cc2)[C@H](O)[C@@H](O)[C@@H]1O',
                                      'name': '(R)-4-hydroxymandelonitrile '
                                              'beta-D-glucoside',
                                      'reason': 'No beta-D-glucopyranose with '
                                                'glycosidic bond found'},
                                  {   'smiles': 'OC[C@H]1O[C@@H](O[C@H]2O[C@H](CO)[C@@H](O)[C@H](O)[C@H]2O)[C@H](O)[C@@H](O)[C@@H]1O',
                                      'name': 'alpha,beta-trehalose',
                                      'reason': 'No beta-D-glucopyranose with '
                                                'glycosidic bond found'},
                                  {   'smiles': 'CC(\\C=C\\C=C(C)\\C=C\\C1=C(C)C[C@H](CC1(C)C)O[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O)=C/C=C/C=C(C)/C=C/C=C(C)/C=C/C1=C(C)C[C@H](CC1(C)C)O[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O',
                                      'name': 'zeaxanthin '
                                              'bis(beta-D-glucoside)',
                                      'reason': 'No beta-D-glucopyranose with '
                                                'glycosidic bond found'},
                                  {   'smiles': 'C[C@]12CC[C@H]3[C@@H](CCC4=CC(=O)CC[C@]34C)[C@@H]1CC[C@@H]2O[C@H]1O[C@H](CO)[C@@H](O)C(O)C1O',
                                      'name': 'glucosyltestosterone',
                                      'reason': 'No beta-D-glucopyranose with '
                                                'glycosidic bond found'},
                                  {   'smiles': '[H][C@@]12C=CO[C@@H](O[C@]3([H])O[C@H](CO)[C@@H](O)[C@H](O)[C@H]3O)[C@]1([H])C(COC(=O)C1=CC=C(O)C=C1)=C[C@H]2O',
                                      'name': 'agnuside',
                                      'reason': 'No beta-D-glucopyranose with '
                                                'glycosidic bond found'},
                                  {   'smiles': 'CC(\\C=C\\[C@]1(O)[C@@]2(C)CO[C@]1(C)C[C@H](C2)O[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O)=C\\C(O)=O',
                                      'name': 'dihydrophaseic acid '
                                              '4-O-beta-D-glucoside',
                                      'reason': 'No beta-D-glucopyranose with '
                                                'glycosidic bond found'},
                                  {   'smiles': '[H][C@]12C[C@@]3([H])[C@]4([H])CC=C5C[C@H](CC[C@]5(C)[C@@]4([H])CC[C@]3(C)[C@@]1([H])[C@H](C)[C@@]1(CC[C@@H](C)CN1)O2)O[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O',
                                      'name': 'solasodine 3-beta-D-glucoside',
                                      'reason': 'No beta-D-glucopyranose with '
                                                'glycosidic bond found'},
                                  {   'smiles': 'OC(CCCCCCC/C=C\\CCCCCCC(C)O[C@H]1[C@@H]([C@H]([C@@H]([C@H](O1)CO)O)O)O)=O',
                                      'name': '(9Z)-17-hydroxyoctadec-9-enoic '
                                              'acid 17-O-beta-D-glucoside',
                                      'reason': 'No beta-D-glucopyranose with '
                                                'glycosidic bond found'},
                                  {   'smiles': 'C[C@]12CC[C@H]3[C@@H](CC[C@H]4C[C@@H](CC[C@]34C)O[C@H]3O[C@H](CO)[C@@H](O)[C@H](O)[C@H]3O)[C@@H]1CC[C@@H]2O',
                                      'name': '5alpha-androstane-3alpha-glcosyl-17beta-diol',
                                      'reason': 'No beta-D-glucopyranose with '
                                                'glycosidic bond found'},
                                  {   'smiles': 'C1[C@]2([C@]3([C@@]([C@@]4([C@](C[C@@H]([C@@H](C4)O)O)(C(C3)=O)[H])C)(CC[C@@]2([C@](C1)([C@@H]([C@H]([C@@H]([C@H](C(C)C)C)O[C@H]5O[C@@H]([C@H]([C@@H]([C@H]5O)O)O)CO)O)C)[H])C)[H])[H])[H]',
                                      'name': 'castasterone '
                                              '23-O-alpha-D-glucoside',
                                      'reason': 'No beta-D-glucopyranose with '
                                                'glycosidic bond found'}],
    'attempt': 1,
    'reasoning': '</think>\n'
                 '\n'
                 'Okay, I need to create a function called is_D_glucoside that '
                 'checks if a given SMILES string represents a D-glucoside. '
                 'From the definition, a D-glucoside is a glycoside where the '
                 'glycosyl group is derived from D-glucose. \n'
                 '\n'
                 'First, I should recall that glycosides have a sugar part '
                 '(the glycone) linked to another part (the aglycone) via a '
                 'glycosidic bond. For D-glucosides, the glycone is '
                 'D-glucose. \n'
                 '\n'
                 'The key steps would be:\n'
                 '\n'
                 '1. **Identify the presence of a glucose moiety in the '
                 'molecule.** \n'
                 '   - Glucose has a specific structure: a six-membered ring '
                 '(pyranose) with hydroxyl groups in specific positions. In '
                 'the beta-D-glucopyranose form, the hydroxyl at the anomeric '
                 'carbon (C1) is in the axial position (down in Haworth '
                 'projection).\n'
                 '\n'
                 '2. **Check that the glucose is in the D-configuration.**\n'
                 '   - The D-configuration refers to the orientation of the '
                 'hydroxyl group on the chiral center farthest from the '
                 'anomeric carbon (C5 in glucose). In the Fischer projection, '
                 'this hydroxyl is on the right side. In the chair '
                 'conformation, this translates to specific stereochemistry.\n'
                 '\n'
                 '3. **Verify the presence of a glycosidic bond.**\n'
                 '   - The glycosidic bond is formed when the hydroxyl group '
                 'of the anomeric carbon (C1) of glucose reacts with another '
                 'hydroxyl group from the aglycone. This means the glucose '
                 'should be connected via an oxygen atom at the C1 position.\n'
                 '\n'
                 '4. **Ensure that the glucose is in the beta '
                 'configuration.**\n'
                 '   - The beta configuration means the glycosidic bond is '
                 'axial (opposite the plane of the ring). In SMILES notation, '
                 'this is represented by the @@ notation in the hydroxyl '
                 'groups around the ring.\n'
                 '\n'
                 'So, how to translate this into RDKit code?\n'
                 '\n'
                 '- **Step 1: Parse the SMILES and generate the molecule.**\n'
                 '  - Use Chem.MolFromSmiles(). If it fails, return False.\n'
                 '\n'
                 '- **Step 2: Find the glucose moiety.**\n'
                 '  - Look for a six-membered ring (pyranose) with the correct '
                 'substituents. Maybe use a SMARTS pattern that matches the '
                 'beta-D-glucopyranose structure.\n'
                 '\n'
                 '- **Step 3: Check the glycosidic bond.**\n'
                 '  - The glucose should be connected via an oxygen atom at '
                 'the anomeric carbon (C1). So, look for an oxygen atom '
                 'connected to the C1 of the glucose ring.\n'
                 '\n'
                 'Wait, but the glycosidic bond replaces the hydroxyl group on '
                 'C1. So in the glucoside, the C1 is connected via an oxygen '
                 'to the aglycone. So the glucose part would have an O-linkage '
                 'at C1.\n'
                 '\n'
                 'So the SMARTS pattern for the glucose part would be '
                 'something like:\n'
                 '- A six-membered ring (pyranose) with the correct '
                 'stereochemistry at each carbon.\n'
                 '\n'
                 'Alternatively, perhaps using the SMILES for '
                 'beta-D-glucopyranose and looking for it as a substructure. '
                 'But the problem is that in the glycoside, the hydroxyl on C1 '
                 'is replaced by an OR group (where R is the aglycone). So the '
                 'standard glucose structure would have that oxygen connected '
                 'to another part.\n'
                 '\n'
                 'So maybe the SMARTS pattern should match the core glucose '
                 'structure with the correct stereochemistry, and the C1 '
                 'connected via an oxygen to another atom (the aglycone).\n'
                 '\n'
                 'Let me think about the SMARTS for beta-D-glucopyranose. The '
                 'beta configuration means that the C1 hydroxyl is in the '
                 'axial position. In the chair conformation, for '
                 'beta-D-glucopyranose, the hydroxyl groups on C1, C2, C3, and '
                 'C4 are in specific orientations.\n'
                 '\n'
                 'In SMILES, the stereochemistry is denoted using the @ and @@ '
                 'symbols. For beta-D-glucopyranose, the hydroxyl groups on '
                 'C1, C2, C3, and C4 are in specific orientations. For '
                 'example, in the beta configuration, the C1 oxygen is in the '
                 'axial position (down), which in SMILES would be represented '
                 'with certain chiral tags.\n'
                 '\n'
                 'But creating a SMARTS pattern that captures this might be '
                 'tricky. Alternatively, perhaps I can look for the presence '
                 'of a glucopyranose ring with the correct substituents and '
                 'stereochemistry.\n'
                 '\n'
                 'Another approach: The canonical SMILES for '
                 'beta-D-glucopyranose is '
                 'O[C@H]1[C@@H](O)[C@H](O)[C@@H](O)[C@@H](O)CO1. Wait, no. Let '
                 'me get the correct structure.\n'
                 '\n'
                 'Beta-D-glucopyranose has the hydroxyls on C1 (axial), C2 '
                 '(equatorial), C3 (axial?), wait, perhaps I need to look up '
                 'the correct configuration.\n'
                 '\n'
                 'Alternatively, maybe using the InChI or another method. But '
                 "perhaps using RDKit's sugar analysis functions. Wait, RDKit "
                 'has a module called Chem.rdMolDescriptors which has a '
                 'function GetSugarEdges or similar? Maybe not. Alternatively, '
                 'using the Murcko decomposition to find rings.\n'
                 '\n'
                 "Alternatively, here's a plan:\n"
                 '\n'
                 '1. Find all oxygen atoms connected to a six-membered ring '
                 '(to find possible sugar rings).\n'
                 '2. For each such oxygen, check if the ring is a '
                 'glucopyranose with the correct stereochemistry.\n'
                 '3. Ensure that the oxygen is part of a glycosidic bond '
                 '(i.e., connected to another part of the molecule).\n'
                 '\n'
                 'But how to check the stereochemistry?\n'
                 '\n'
                 'Alternatively, create a SMARTS pattern that matches the '
                 'beta-D-glucopyranose moiety with an O-linked group at C1.\n'
                 '\n'
                 'The beta-D-glucopyranose has the following structure in '
                 'SMILES (without the glycosidic bond):\n'
                 '\n'
                 'For beta-D-glucopyranose, the hydroxyl groups are in the '
                 'following positions (Haworth projection):\n'
                 '- C1: down (axial) - beta\n'
                 '- C2: up (equatorial)\n'
                 '- C3: down (axial)\n'
                 '- C4: up (equatorial)\n'
                 '- C5: determines D vs L. For D-glucose, the C5 hydroxyl is '
                 'on the right in Fischer, which in the ring form (pyranose) '
                 'would have the CH2OH group in the up position.\n'
                 '\n'
                 'Wait, perhaps the correct SMILES for beta-D-glucopyranose is '
                 "C1[C@H](O)[C@@H](O)[C@H](O)[C@@H](O)[C@@H](O1)CO. But I'm "
                 'not sure. Alternatively, the actual structure would have the '
                 'anomeric carbon (C1) connected to the oxygen in the ring, '
                 'and the substituents in specific positions.\n'
                 '\n'
                 "Alternatively, here's a SMARTS pattern that might work for "
                 'the beta-D-glucopyranose part with a glycosidic bond:\n'
                 '\n'
                 'The core structure would be a six-membered ring (O in the '
                 'ring) with the substituents in specific positions. The '
                 'anomeric carbon (C1) is connected via an oxygen to the '
                 "aglycone (R-O-R').\n"
                 '\n'
                 'So the SMARTS pattern could be:\n'
                 '\n'
                 '[O;R][C@H]1[C@@H](O)[C@H](O)[C@@H](O)[C@@H](O)[C@H]1O\n'
                 '\n'
                 "Wait, maybe not. Let's think again. The beta-D-glucopyranose "
                 'has the following substituents:\n'
                 '\n'
                 '- C1: OR (glycosidic bond)\n'
                 '- C2: OH (equatorial)\n'
                 '- C3: OH (axial)\n'
                 '- C4: OH (equatorial)\n'
                 "- C5: CH2OH (since it's D-configuration, the C5 hydroxyl is "
                 'in a specific position)\n'
                 '\n'
                 'Wait, perhaps the correct way to represent '
                 'beta-D-glucopyranose in SMILES is:\n'
                 '\n'
                 'O[C@H]1[C@@H](O)[C@H](O)[C@@H](O)[C@H](O)CO1\n'
                 '\n'
                 "But I'm not entirely confident. Alternatively, maybe using a "
                 'SMARTS pattern that captures the stereochemistry at each '
                 'carbon.\n'
                 '\n'
                 'Alternatively, since the exact stereochemistry might vary '
                 '(e.g., different chair conformations), perhaps the best '
                 'approach is to look for a glucopyranose ring with the '
                 'correct substituents and stereochemistry, and then check '
                 "that there's a glycosidic bond at C1.\n"
                 '\n'
                 "Another approach: Use the RDKit's sugar analysis "
                 "functionality. But I'm not sure if that exists. "
                 'Alternatively, break down the molecule into rings and check '
                 'for the glucose structure.\n'
                 '\n'
                 'Alternatively, perhaps the presence of a '
                 'beta-D-glucopyranose can be detected by looking for a '
                 'six-membered oxygen-containing ring (pyranose) with the '
                 'correct substituents and stereochemistry.\n'
                 '\n'
                 "But this might be complicated. Let's look at the example "
                 'SMILES given:\n'
                 '\n'
                 'For example, one of the examples is '
                 "beta-D-glucosyl-(1<->1')-N-docosanoyl-(4E,14Z)-sphingadienine: "
                 'SMILES: '
                 '[C@H]([C@@H](/C=C/CCCCCCCC/C=C\\CCC)O)(NC(CCCCCCCCCCCCCCCCCCCCC)=O)CO[C@@H]1O[C@@H]([C@H]([C@@H]([C@H]1O)O)O)CO\n'
                 '\n'
                 'The glucose part here is '
                 'CO[C@@H]1O[C@@H]([C@H]([C@@H]([C@H]1O)O)O)CO. Wait, maybe '
                 'not. Let me parse this:\n'
                 '\n'
                 'Looking at the part after CO: '
                 '[C@@H]1O[C@@H]([C@H]([C@@H]([C@H]1O)O)O)CO. That seems like '
                 'a glucose ring. Let me break it down:\n'
                 '\n'
                 'The ring is O[C@@H]1... which is part of the ring. The '
                 'structure is:\n'
                 '\n'
                 '- The anomeric carbon (C1) is connected to O (from the CO '
                 'group) and part of the ring. The substituents on the ring '
                 'carbons have specific stereochemistry.\n'
                 '\n'
                 'Alternatively, perhaps the glucose part in the example is '
                 'represented as '
                 "O[C@@H]1[C@H](O)[C@@H](O)[C@H](O)[C@@H](CO)O1. But I'm not "
                 'sure.\n'
                 '\n'
                 'Alternatively, perhaps the key is that the glucose is '
                 'connected via an oxygen at C1 (the anomeric carbon) to the '
                 'aglycone. So the SMARTS pattern would look for a '
                 'six-membered ring (pyranose) where one of the ring oxygens '
                 'is connected to a carbon that has an oxygen connected to '
                 'another atom (the glycosidic bond).\n'
                 '\n'
                 "But how to ensure it's D-glucose? The D configuration refers "
                 'to the configuration at C5 (in glucose), which in the '
                 'pyranose form is part of the ring. Wait, in glucose, the '
                 'pyranose form is a six-membered ring where the oxygen is '
                 'between C5 and C1. So C5 is part of the ring, and the '
                 'configuration at C5 (which determines D vs L) is such that '
                 'the CH2OH group is in a specific position.\n'
                 '\n'
                 'In D-glucose, the C5 hydroxyl (in the linear form) is on the '
                 'right, which in the pyranose form becomes the CH2OH group on '
                 'C5, which is part of the ring. Wait, in the pyranose form, '
                 'C5 is connected to C6 (CH2OH). So the configuration at C5 '
                 '(now part of the ring) determines D vs L. For D-glucose, the '
                 'C5 (in the ring) has the CH2OH group in a specific '
                 'orientation.\n'
                 '\n'
                 'This is getting complicated. Maybe the best approach is to '
                 'create a SMARTS pattern that matches the '
                 'beta-D-glucopyranose structure with the glycosidic bond.\n'
                 '\n'
                 'The SMARTS pattern for beta-D-glucopyranose would have the '
                 'following features:\n'
                 '\n'
                 '- A six-membered ring with oxygen as one of the atoms (the '
                 'ring oxygen).\n'
                 '- The anomeric carbon (C1) is connected to an oxygen that is '
                 'part of the glycosidic bond (i.e., connected to another atom '
                 'outside the ring).\n'
                 '- The stereochemistry at each carbon in the ring matches '
                 'that of beta-D-glucopyranose.\n'
                 '\n'
                 'But how to represent this in SMARTS?\n'
                 '\n'
                 'Alternatively, perhaps the SMARTS can be written as:\n'
                 '\n'
                 '[C@H]1(O[C@@H]([C@H]([C@@H]([C@H]1O)O)O)CO)\n'
                 '\n'
                 "Wait, maybe not. Let's look for the core structure of "
                 'beta-D-glucopyranose with the glycosidic oxygen.\n'
                 '\n'
                 "Alternatively, here's a possible SMARTS pattern for the "
                 'glucose part:\n'
                 '\n'
                 '[O;R][C@@H]1[C@H](O)[C@@H](O)[C@H](O)[C@@H](O)[C@H]1OC\n'
                 '\n'
                 "But I'm not sure. Alternatively, the beta-D-glucopyranose "
                 'with the glycosidic bond would have the following '
                 'structure:\n'
                 '\n'
                 'The anomeric carbon (C1) is connected via an oxygen to the '
                 'aglycone. The other hydroxyl groups are in specific '
                 'positions.\n'
                 '\n'
                 "Alternatively, here's a SMARTS pattern that might capture "
                 'the beta-D-glucopyranose moiety with a glycosidic bond:\n'
                 '\n'
                 '[O][C@@H]1[C@H](O)[C@@H](O)[C@H](O)[C@@H](O)[C@H]1O\n'
                 '\n'
                 "But this doesn't account for the glycosidic bond. Wait, the "
                 'glycosidic oxygen would be connected to the anomeric carbon '
                 '(C1) and the aglycone. So the anomeric carbon would have two '
                 'oxygen attachments: one to the ring oxygen (O in the ring) '
                 'and one to the glycosidic oxygen (O connected to the '
                 'aglycone).\n'
                 '\n'
                 'Wait, in the glucoside, the anomeric carbon (C1) is '
                 'connected to two oxygens: one is part of the ring (O in the '
                 'pyranose ring), and the other is the glycosidic oxygen (O-R, '
                 'where R is the aglycone). So the SMARTS pattern for the '
                 'anomeric carbon would be C([O;R])(O[C@...])... ?\n'
                 '\n'
                 'Alternatively, perhaps the correct SMARTS is:\n'
                 '\n'
                 '[O;R][C@H]1[C@@H](O)[C@H](O)[C@@H](O)[C@@H](O)[C@H]1O[C]\n'
                 '\n'
                 "Wait, maybe not. Let's try to break it down:\n"
                 '\n'
                 'The beta-D-glucopyranose ring has the following structure '
                 '(in chair conformation):\n'
                 '\n'
                 '- C1 (anomeric carbon) is connected to the ring oxygen (O) '
                 'and the glycosidic oxygen (O-R).\n'
                 '- The hydroxyl groups on C2, C3, C4 are in specific '
                 'positions.\n'
                 '- C5 (in the ring) is connected to CH2OH (for D-glucose).\n'
                 '\n'
                 'But in the glycoside, the hydroxyl on C1 is replaced by the '
                 'OR group. So the structure would be:\n'
                 '\n'
                 'O-R-O-C1-C2-C3-C4-C5\n'
                 '\n'
                 'Where C1 is part of the ring. Wait, perhaps the SMILES for '
                 'the glucoside part is O-C1-C(...) where C1 is the anomeric '
                 'carbon.\n'
                 '\n'
                 "Alternatively, here's a possible SMARTS pattern that matches "
                 'the beta-D-glucopyranose with a glycosidic bond:\n'
                 '\n'
                 '[O][C@@H]1[C@H](O)[C@@H](O)[C@H](O)[C@@H](O)[C@H]1O\n'
                 '\n'
                 'But this would match a free glucose, not a glycoside. The '
                 'glycoside would have the O-R group instead of the hydroxyl '
                 'on C1.\n'
                 '\n'
                 'Wait, in the glycoside, the hydroxyl on C1 is replaced by an '
                 'O-R group. So the correct SMARTS for the glucose part would '
                 'have C1 connected to an oxygen that is connected to another '
                 'atom (the aglycone). So the SMARTS would be:\n'
                 '\n'
                 '[O][C@@H]1[C@H](O)[C@@H](O)[C@H](O)[C@@H](O)[C@H]1O[C]\n'
                 '\n'
                 'But how to represent that the O is connected to something '
                 'else? Maybe:\n'
                 '\n'
                 '[O][C@@H]1[C@H](O)[C@@H](O)[C@H](O)[C@@H](O)[C@H]1O[!H]\n'
                 '\n'
                 'Which means the oxygen at C1 is connected to something other '
                 'than hydrogen (i.e., the aglycone).\n'
                 '\n'
                 'Putting this together, the SMARTS pattern would be:\n'
                 '\n'
                 '[OX2][C@@H]1[C@H](O)[C@@H](O)[C@H](O)[C@@H](O)[C@H]1O[!H]\n'
                 '\n'
                 'This pattern matches:\n'
                 '\n'
                 '- An oxygen (OX2, which is a hydroxyl or ether oxygen) '
                 'connected to the anomeric carbon (C1).\n'
                 '- The anomeric carbon is part of a six-membered ring (the '
                 'glucopyranose).\n'
                 '- The stereochemistry at each carbon (C1 to C5) is as in '
                 'beta-D-glucopyranose.\n'
                 '- The oxygen at C1 is connected to something other than '
                 'hydrogen (indicating a glycosidic bond).\n'
                 '\n'
                 "But I'm not sure about the stereochemistry markers. Let me "
                 'check:\n'
                 '\n'
                 'In beta-D-glucopyranose, the hydroxyl groups are arranged as '
                 'follows (using Haworth projection):\n'
                 '\n'
                 '- C1: axial (down) - beta configuration.\n'
                 '- C2: equatorial (up).\n'
                 '- C3: axial (down).\n'
                 '- C4: equatorial (up).\n'
                 "- C5: the CH2OH group is up (since it's D-configuration).\n"
                 '\n'
                 'In SMILES notation, the stereochemistry is denoted with @ '
                 'and @@. For example, the anomeric carbon (C1) in beta '
                 'configuration would have the hydroxyl group in a specific '
                 'orientation.\n'
                 '\n'
                 'Alternatively, perhaps the correct SMARTS for the '
                 'beta-D-glucopyranose moiety with a glycosidic bond is:\n'
                 '\n'
                 'O[C@@H]1[C@H](O)[C@@H](O)[C@H](O)[C@@H](O)[C@H]1OC\n'
                 '\n'
                 "But I'm not sure. Maybe it's better to look for the presence "
                 'of a glucose-like ring with the correct substituents and the '
                 'glycosidic bond.\n'
                 '\n'
                 "Another approach: Use the RDKit's sugar recognition "
                 "functions. However, I'm not sure if RDKit has built-in "
                 'functions for identifying specific monosaccharides. If not, '
                 'creating a custom SMARTS pattern is necessary.\n'
                 '\n'
                 'Alternatively, find all the rings in the molecule and check '
                 'if any of them is a beta-D-glucopyranose with a glycosidic '
                 'bond.\n'
                 '\n'
                 'Putting this together, the steps in code would be:\n'
                 '\n'
                 '1. Parse the SMILES into a molecule.\n'
                 '2. Check for the presence of a beta-D-glucopyranose ring '
                 'with a glycosidic bond.\n'
                 '3. If found, return True; else, return False.\n'
                 '\n'
                 'The code could look something like this:',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 464,
    'num_false_positives': 8738,
    'num_true_negatives': 132963,
    'num_false_negatives': 135,
    'num_negatives': None,
    'precision': 0.05042382090849815,
    'recall': 0.7746243739565943,
    'f1': 0.0946842158963371,
    'accuracy': 0.9376458186929023,
    'negative_predictive_value': 0.9989857097777577}