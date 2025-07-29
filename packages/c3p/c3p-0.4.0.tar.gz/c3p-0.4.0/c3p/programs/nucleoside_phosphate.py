"""
Classifies: CHEBI:25608 nucleoside phosphate
"""
"""
Classifies: CHEBI:24676 nucleoside phosphate
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_nucleoside_phosphate(smiles: str):
    """
    Determines if a molecule is a nucleoside phosphate based on its SMILES string.
    A nucleoside phosphate consists of a nucleobase, a sugar, and one or more phosphate groups.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a nucleoside phosphate, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # 1. Check for phosphate groups (at least one)
    phosphate_pattern = Chem.MolFromSmarts("[OX2][P](=[OX1])([OX2])([OX2])")
    phosphate_matches = mol.GetSubstructMatches(phosphate_pattern)
    if not phosphate_matches:
         return False, "No phosphate group found"

    # 2. Check for a sugar ring (ribose or deoxyribose or other 5-membered ring with 2 or more OH groups)
    sugar_pattern1 = Chem.MolFromSmarts("C1[CH](O)[CH](O)[CH]([CH2X4,CHX4]O)O1") #ribose, deoxyribose or something similar
    sugar_pattern2 = Chem.MolFromSmarts("C1[CH](O)[CH](O)[CH](C)O1") # another potential ribose-like sugar
    sugar_pattern3 = Chem.MolFromSmarts("C1[CH](O)[CH](O)[CH](C(C)=O)O1") # another potential ribose-like sugar

    if not (mol.HasSubstructMatch(sugar_pattern1) or mol.HasSubstructMatch(sugar_pattern2) or mol.HasSubstructMatch(sugar_pattern3)):
       return False, "No sugar ring found"

    # 3. Check for a nucleobase (pyrimidine or purine)
    # Pyrimidines (cytosine, thymine, uracil)
    pyrimidine_pattern1 = Chem.MolFromSmarts("n1cncc(=O)[nH]1") #cytosine/uracil
    pyrimidine_pattern2 = Chem.MolFromSmarts("n1cc(C)c(=O)[nH]1") #thymine
    # Purines (adenine, guanine, hypoxanthine)
    purine_pattern1 = Chem.MolFromSmarts("n1cnc2c1ncnc2N") #adenine
    purine_pattern2 = Chem.MolFromSmarts("n1cnc2c1nc(=O)n[nH]2") #guanine
    purine_pattern3 = Chem.MolFromSmarts("n1cnc2c1ncnc2O") #hypoxanthine

    if not (mol.HasSubstructMatch(pyrimidine_pattern1) or mol.HasSubstructMatch(pyrimidine_pattern2) or
            mol.HasSubstructMatch(purine_pattern1) or mol.HasSubstructMatch(purine_pattern2) or
            mol.HasSubstructMatch(purine_pattern3)):
      return False, "No nucleobase found"

    # 4. Check that sugar is connected to a phosphate and a nucleobase (difficult without complex substructure matching)

    return True, "Contains a nucleobase, a sugar, and at least one phosphate group"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:25608',
                          'name': 'nucleoside phosphate',
                          'definition': 'A nucleobase-containing molecular '
                                        'entity that is a nucleoside in which '
                                        'one or more of the sugar hydroxy '
                                        'groups has been converted into a '
                                        'mono- or poly-phosphate. The term '
                                        'includes both nucleotides and '
                                        'non-nucleotide nucleoside phosphates.',
                          'parents': [   'CHEBI:25703',
                                         'CHEBI:37734',
                                         'CHEBI:61120'],
                          'xrefs': ['KEGG:C01329'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 37,
                           'log_lines_of_code': 3.6109179126442243,
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
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 0,
                                                 1,
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
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 0,
                                                 1,
                                                 0,
                                                 1],
                           'max_indent': 2,
                           'imports': [   'from rdkit import Chem',
                                          'from rdkit.Chem import AllChem'],
                           'imports_count': 2,
                           'methods_called': [   'MolFromSmiles',
                                                 'MolFromSmarts',
                                                 'HasSubstructMatch',
                                                 'GetSubstructMatches'],
                           'methods_called_count': 4,
                           'smarts_strings': [   '[OX2][P](=[OX1])([OX2])([OX2])',
                                                 'C1[CH](O)[CH](O)[CH](C(C)=O)O1',
                                                 'n1cc(C)c(=O)[nH]1',
                                                 'n1cnc2c1nc(=O)n[nH]2',
                                                 'n1cncc(=O)[nH]1',
                                                 'n1cnc2c1ncnc2N',
                                                 'C1[CH](O)[CH](O)[CH]([CH2X4,CHX4]O)O1',
                                                 'n1cnc2c1ncnc2O',
                                                 'C1[CH](O)[CH](O)[CH](C)O1'],
                           'smarts_strings_count': 9,
                           'defs': ['is_nucleoside_phosphate(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "No phosphate group found"',
                                          'False, "No sugar ring found"',
                                          'False, "No nucleobase found"',
                                          'True, "Contains a nucleobase, a '
                                          'sugar, and at least one phosphate '
                                          'group"'],
                           'returns_count': 5,
                           'complexity': 3.122183582528845},
    'message': None,
    'sample_true_negatives': [   {   'smiles': 'CCN1N=C(N=N1)C2=CC=CC=C2NC(=O)C3=CC=C(C=C3)N4C=NN=N4',
                                     'name': 'N-[2-(2-ethyl-5-tetrazolyl)phenyl]-4-(1-tetrazolyl)benzamide',
                                     'reason': 'No phosphate group found'},
                                 {   'smiles': 'CCS(=O)(=O)N1CC2(C1)[C@@H]([C@@H](N2C(=O)C3CCCC3)CO)C4=CC=C(C=C4)C=CC',
                                     'name': 'LSM-38092',
                                     'reason': 'No phosphate group found'},
                                 {   'smiles': 'O=C/1N/C(/C(=O)N\\C1=C\\C2=CC=CC=C2)=C\\C=3N=CNC3C(C=C)(C)C',
                                     'name': 'DeltaPLH',
                                     'reason': 'No phosphate group found'},
                                 {   'smiles': 'C1CCN(CC1)C(=O)C[C@H]2C[C@@H]3[C@H]([C@@H](O2)CO)OC4=C3C=C(C=C4)NC(=O)CC5CC5',
                                     'name': 'N-[(1S,3R,4aS,9aR)-1-(hydroxymethyl)-3-[2-oxo-2-(1-piperidinyl)ethyl]-3,4,4a,9a-tetrahydro-1H-pyrano[3,4-b]benzofuran-6-yl]-2-cyclopropylacetamide',
                                     'reason': 'No phosphate group found'},
                                 {   'smiles': 'C[C@H]1C[C@@]2(OC(=O)c3ccccc3)[C@H]([C@H]1OC(C)=O)[C@@H](O)\\C(C)=C/C[C@H]1[C@@H](\\C=C(C)\\C2=O)C1(C)C',
                                     'name': '(-)-(6Z,12E,2S,3S,4R,5R,9S,11S,15R)-3-acetoxy-15-benzoyloxylathyra-6,12-dien-5-ol-14-one',
                                     'reason': 'No phosphate group found'},
                                 {   'smiles': 'O=C1C(O)=CC=2O[C@]3([C@H](O)C[C@@H]4[C@](OC=5C=C(O)C(C=C(C5C4)C)=O)(CC=CC(C[C@H]3CC2C(=C1)C)(C)C)C)C',
                                     'name': 'Eupenifeldin',
                                     'reason': 'No phosphate group found'},
                                 {   'smiles': 'O1[C@@H](O[C@@H]2[C@@H](OC[C@H]3O[C@@H](O[C@H]4[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]4CO)O[C@H]5[C@H](O)[C@@H](NC(=O)C)C(O[C@@H]5CO[C@@H]6O[C@H]([C@@H](O)[C@@H](O)[C@@H]6O)C)O)[C@@H](O)[C@@H](O[C@H]7O[C@@H]([C@@H](O)[C@H](O)[C@@H]7O[C@@H]8O[C@@H]([C@@H](O[C@@H]9O[C@@H]([C@H](O)[C@H](O)[C@H]9NC(=O)C)CO)[C@H](O)[C@H]8NC(=O)C)CO)CO)[C@@H]3O)O[C@@H]([C@@H](O)[C@@H]2O)CO)[C@H](NC(=O)C)[C@@H](O[C@@H]%10O[C@H]([C@@H](O)[C@@H](O)[C@@H]%10O)C)[C@H](O[C@@H]%11O[C@@H]([C@H](O)[C@H](O)[C@H]%11NC(=O)C)CO)[C@H]1CO',
                                     'name': 'N-[(3R,4R,5S,6R)-5-[(2S,3R,4R,5S,6R)-3-Acetamido-5-[(2S,3S,4S,5R,6R)-4-[(2R,3S,4S,5S,6R)-3-[(2S,3R,4R,5S,6R)-3-acetamido-5-[(2S,3R,4R,5R,6R)-3-acetamido-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-6-[[(2S,3S,4S,5S,6R)-3-[(2S,3R,4R,5S,6R)-3-acetamido-5-[(2S,3R,4R,5R,6R)-3-acetamido-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-6-(hydroxymethyl)-4-[(2R,3S,4R,5S,6S)-3,4,5-trihydroxy-6-methyloxan-2-yl]oxyoxan-2-yl]oxy-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxymethyl]-3,5-dihydroxyoxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-2,4-dihydroxy-6-[[(2R,3S,4R,5S,6S)-3,4,5-trihydroxy-6-methyloxan-2-yl]oxymethyl]oxan-3-yl]acetamide',
                                     'reason': 'No phosphate group found'},
                                 {   'smiles': 'CN1C[C@@H]2C[C@H](Cn3c2cccc3=O)[C@H]1CC=C',
                                     'name': 'Tinctorine',
                                     'reason': 'No phosphate group found'},
                                 {   'smiles': 'CCC1=C2COC(CC2=C3C(=C(OC3=N1)C(=O)C4=CC=CC=C4)N)(C)C',
                                     'name': 'LSM-4563',
                                     'reason': 'No phosphate group found'},
                                 {   'smiles': 'CN1CCN(CC1)C(=O)C[C@@H]2CC[C@H]3[C@H](O2)COC[C@@H](CN3C(=O)NC4=CC5=C(C=C4)OCO5)O',
                                     'name': '(3R,6aS,8S,10aS)-N-(1,3-benzodioxol-5-yl)-3-hydroxy-8-[2-(4-methyl-1-piperazinyl)-2-oxoethyl]-3,4,6,6a,8,9,10,10a-octahydro-2H-pyrano[2,3-c][1,5]oxazocine-1-carboxamide',
                                     'reason': 'No phosphate group found'}],
    'sample_false_negatives': [   {   'smiles': 'NC1=NC2=C(N=CN2[C@H]2C[C@H](O)[C@@H](COP(O)(=O)OP(O)(=O)OP(O)(O)=O)O2)C(=O)N1',
                                      'name': 'dGTP',
                                      'reason': 'No sugar ring found'},
                                  {   'smiles': 'C[C@H]1O[C@@H](C[C@@H](O)[C@@H]1O)OP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H](C[C@@H]1O)n1cc(C)c(=O)[nH]c1=O',
                                      'name': 'dTDP-D-olivose',
                                      'reason': 'No sugar ring found'},
                                  {   'smiles': 'C[C@H]1O[C@H](OP(O)(=O)OP(O)(=O)OC[C@H]2O[C@H]([C@H](O)[C@@H]2O)n2cnc3c2nc(N)[nH]c3=O)[C@@H](O)[C@@H](O)[C@@H]1NC(C)=O',
                                      'name': 'GDP-N-acetyl-alpha-D-perosamine',
                                      'reason': 'No nucleobase found'},
                                  {   'smiles': 'NC1=NC=NC2=C1N=CN2[C@@H]1O[C@H](COP(O)(O)=O)C(=O)[C@H]1O',
                                      'name': "3'-dehydro-AMP",
                                      'reason': 'No sugar ring found'},
                                  {   'smiles': 'O[C@H]1C[C@@H](O[C@@H]1COP(O)(=O)OP(O)(O)=O)n1ccc(=O)[nH]c1=O',
                                      'name': 'dUDP',
                                      'reason': 'No sugar ring found'},
                                  {   'smiles': 'CNc1ccn([C@@H]2O[C@H](COP(O)(O)=O)[C@@H](O)[C@H]2O)c(=O)n1',
                                      'name': 'N(4)-methylcytidine '
                                              "5'-monophosphate",
                                      'reason': 'No nucleobase found'},
                                  {   'smiles': 'P(=O)(OC[C@H]1O[C@@H](N2C(=O)NC=3C2=NC=NC3N)[C@@H]([C@@H]1O)O)(OC)N',
                                      'name': 'Phosmidosine C',
                                      'reason': 'No phosphate group found'},
                                  {   'smiles': 'N[C@H]1[C@@H](OP(O)(=O)OP(O)(=O)OC[C@H]2O[C@H]([C@H](O)[C@@H]2O)n2ccc(=O)[nH]c2=O)O[C@H](CO)[C@@H](O)[C@@H]1O',
                                      'name': 'UDP-alpha-D-glucosamine',
                                      'reason': 'No nucleobase found'},
                                  {   'smiles': 'Nc1nc2n([C@@H]3O[C@@H]4CO[P@@](S)(=O)O[C@H]4[C@H]3O)c(Br)nc2c(=O)[nH]1',
                                      'name': '(Sp)-8-Br-cGMPS',
                                      'reason': 'No phosphate group found'},
                                  {   'smiles': 'C[C@H]1O[C@@H](C[C@@](C)(O)C1=O)OP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H](C[C@@H]1O)n1cc(C)c(=O)[nH]c1=O',
                                      'name': 'dTDP-3-methyl-4-oxo-2,6-dideoxy-D-glucose',
                                      'reason': 'No sugar ring found'}],
    'attempt': 0,
    'reasoning': "Okay, let's break down how to classify nucleoside "
                 'phosphates.\n'
                 '\n'
                 '**Reasoning:**\n'
                 '\n'
                 'A nucleoside phosphate consists of three main parts:\n'
                 '\n'
                 '1.  **A nucleobase:** This is a nitrogen-containing '
                 'heterocyclic ring (adenine, guanine, cytosine, thymine, '
                 'uracil, and derivatives thereof).\n'
                 '2.  **A sugar:** Usually a ribose or deoxyribose (5-membered '
                 'ring) but other sugars may be present.\n'
                 '3.  **One or more phosphate groups:** These are attached to '
                 "the sugar, typically at the 5' position (but can be 2', 3', "
                 'or other positions).\n'
                 '\n'
                 'Therefore, our strategy is to:\n'
                 '\n'
                 '1.  **Look for phosphate groups:** This is the most '
                 'characteristic feature of a nucleoside phosphate. We can use '
                 'SMARTS to identify P=O groups attached to other oxygen '
                 'atoms.\n'
                 '2.  **Check for a sugar ring:** Look for a 5-membered ring '
                 'with multiple hydroxyl groups and a carbon connected to the '
                 'nucleobase.\n'
                 '3.  **Check for a nucleobase:** Look for the characteristic '
                 'heterocyclic rings found in nucleobases (adenine, guanine, '
                 'etc.). We can use SMARTS to check for different ring types '
                 'with characteristic substitution patterns.\n'
                 '4.  **Verify connection:** Ensure the sugar is connected to '
                 'a phosphate and a nucleobase by checking for the appropriate '
                 'bonds.\n'
                 '5. If any of the requirements are not fulfilled we can fail '
                 'early\n'
                 '\n'
                 '**Code:**',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 822,
    'num_false_positives': 167,
    'num_true_negatives': 140831,
    'num_false_negatives': 480,
    'num_negatives': None,
    'precision': 0.8311425682507584,
    'recall': 0.631336405529954,
    'f1': 0.7175905718027061,
    'accuracy': 0.9954532677442024,
    'negative_predictive_value': 0.9966032368322353}