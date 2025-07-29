"""
Classifies: CHEBI:17984 acyl-CoA
"""
"""
Classifies: Acyl-CoA
Definition: An acyl-CoA is a thioester that results from the formal condensation of
the thiol group of coenzyme A with the carboxy group of any carboxylic acid.
Example structures include pimeloyl-CoA, stearoyl-CoA, etc.
"""

from rdkit import Chem
from rdkit.Chem import rdMolDescriptors

def is_acyl_CoA(smiles: str):
    """
    Determines if a molecule is an acyl-CoA based on its SMILES string.
    
    An acyl-CoA is defined as a thioester (R-C(=O)S-) resulting from the condensation
    of the thiol group of coenzyme A with a carboxylic acid. Its structure should include:
      - A thioester functional group (C(=O)S).
      - A CoA nucleotide part, which may be recognized either by the presence of an adenine
        ring (in varying representations) or by a pantetheine fragment.
      - Multiple phosphate groups (typically at least three phosphorus atoms in the CoA moiety).
    
    Args:
        smiles (str): SMILES string of the molecule.
    
    Returns:
        bool: True if the molecule is classified as an acyl-CoA, False otherwise.
        str: Explanation for the classification.
    """
    # Parse the SMILES using RDKit.
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
    
    # 1. Check for the thioester functional group: a carbonyl directly bound to a sulfur.
    thioester_smarts = "[CX3](=O)[SX2]"
    thioester = Chem.MolFromSmarts(thioester_smarts)
    if not mol.HasSubstructMatch(thioester):
        return False, "No thioester functional group found"
    
    # 2. Check for the CoA nucleotide part.
    # Try to capture the adenine ring with several SMARTS patterns.
    adenine_patterns = [
        "n1cnc2c1ncnc2",      # common adenine representation
        "c1ncnc2ncnc12", 
        "N1C=NC2=C1N=CN=C2N",  
        "c1[nH]c2ncnc(n2)n1"   
    ]
    has_adenine = any(mol.HasSubstructMatch(Chem.MolFromSmarts(pat)) for pat in adenine_patterns)
    
    # Recognize part of the pantetheine fragment which is also common in CoA.
    pantetheine_smarts = "SCCNC(=O)CCNC(=O)"
    pantetheine = Chem.MolFromSmarts(pantetheine_smarts)
    has_pantetheine = mol.HasSubstructMatch(pantetheine)
    
    if not (has_adenine or has_pantetheine):
        return False, "No adenine moiety or pantetheine fragment (CoA nucleotide part) found"
    
    # 3. Check for the presence of phosphate groups.
    # Rather than matching a rigid phosphate SMARTS pattern, we count phosphorus atoms.
    phosphate_count = sum(1 for atom in mol.GetAtoms() if atom.GetAtomicNum() == 15)
    if phosphate_count < 3:
        return False, "Insufficient phosphate groups for a CoA moiety (found {} phosphorus atom(s))".format(phosphate_count)
    
    # If all three key features are detected then classify as acyl-CoA.
    return True, "Molecule contains a thioester linked to a CoA moiety (CoA nucleotide part and sufficient phosphate groups detected)"

# Example usage:
# Uncomment the following lines to test with a known acyl-CoA molecule (pimeloyl-CoA example)
# test_smiles = "CC(C)(COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12)[C@@H](O)C(=O)NCCC(=O)NCCSC(=O)CCCCCC(O)=O"
# result, reason = is_acyl_CoA(test_smiles)
# print(result, reason)


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:17984',
                          'name': 'acyl-CoA',
                          'definition': 'A thioester that results from the '
                                        'formal condensation of the thiol '
                                        'group of coenzyme A with the carboxy '
                                        'group of any carboxylic acid.',
                          'parents': [   'CHEBI:140325',
                                         'CHEBI:20706',
                                         'CHEBI:231540',
                                         'CHEBI:51277'],
                          'xrefs': [   'KEGG:C00040',
                                       'PMID:11264983',
                                       'PMID:11524729',
                                       'PMID:16495773',
                                       'PMID:21514367',
                                       'PMID:21541677'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 45,
                           'log_lines_of_code': 3.8066624897703196,
                           'indent_by_line': [   1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
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
                                                 2,
                                                 2,
                                                 2,
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
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 0],
                           'max_indent': 2,
                           'imports': [   'from rdkit import Chem',
                                          'from rdkit.Chem import '
                                          'rdMolDescriptors'],
                           'imports_count': 2,
                           'methods_called': [   'MolFromSmiles',
                                                 'MolFromSmarts',
                                                 'HasSubstructMatch',
                                                 'GetAtoms',
                                                 'format',
                                                 'GetAtomicNum'],
                           'methods_called_count': 6,
                           'smarts_strings': [   'thioester_smarts',
                                                 'pantetheine_smarts',
                                                 'pat)) for pat in '
                                                 'adenine_patterns'],
                           'smarts_strings_count': 3,
                           'defs': ['is_acyl_CoA(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "No thioester functional '
                                          'group found"',
                                          'False, "No adenine moiety or '
                                          'pantetheine fragment (CoA '
                                          'nucleotide part) found"',
                                          'False, "Insufficient phosphate '
                                          'groups for a CoA moiety (found {} '
                                          'phosphorus '
                                          'atom(s))".format(phosphate_count)',
                                          'True, "Molecule contains a '
                                          'thioester linked to a CoA moiety '
                                          '(CoA nucleotide part and sufficient '
                                          'phosphate groups detected)"'],
                           'returns_count': 5,
                           'complexity': 3.5613324979540635},
    'message': '\n'
               'Attempt failed: F1 score of 0 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: NONE\n'
               'False positives: NONE\n'
               'False negatives: SMILES: '
               'CC(C)(COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12)[C@@H](O)C(=O)NCCC(=O)NCCSC(=O)CCCCCC(O)=O '
               'NAME: pimeloyl-CoA REASON: MISSED Insufficient phosphate '
               'groups for a CoA moiety\n'
               ' * SMILES: '
               'S(C(=O)CCCCC[C@@H]1[C@@H](C(C=C1)=O)C/C=C\\CC)CCNC(CCNC(=O)[C@@H](C(COP(OP(OC[C@H]2O[C@@H](N3C4=C(C(=NC=N4)N)N=C3)[C@@H]([C@@H]2OP(O)(O)=O)O)(=O)O)(=O)O)(C)C)O)=O '
               'NAME: (9S,13S)-1a,1b-dinor-12-oxo-10,15-phytodienoyl-CoA '
               'REASON: MISSED Insufficient phosphate groups for a CoA moiety\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCCCCCCCCCCC[C@@H](O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12 '
               'NAME: (R)-3-hydroxytriacontanoyl-CoA REASON: MISSED '
               'Insufficient phosphate groups for a CoA moiety\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)N1C=NC2=C1N=CN=C2N '
               'NAME: stearoyl-CoA REASON: MISSED Insufficient phosphate '
               'groups for a CoA moiety\n'
               ' * SMILES: '
               'CCCC\\C=C/CCCCCCCCCC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12 '
               'NAME: (11Z)-hexadec-11-enoyl-CoA REASON: MISSED Insufficient '
               'phosphate groups for a CoA moiety\n'
               ' * SMILES: O=NN1CCNCC1 NAME: N-Mononitrosopiperazine REASON: '
               'MISSED No thioester functional group found\n'
               ' * SMILES: '
               'CC\\C=C/C\\C=C/C\\C=C/C\\C=C/C\\C=C/C\\C=C/CCCCCCCCCCCC[C@@H](O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12 '
               'NAME: '
               '(3R,16Z,19Z,22Z,25Z,28Z,31Z)-3-hydroxytetratriacontahexaenoyl-CoA '
               'REASON: MISSED Insufficient phosphate groups for a CoA moiety\n'
               ' * SMILES: '
               'CCCCC\\C=C/C\\C=C/C\\C=C/C\\C=C/CCCCCCCCCCCCCCCCCCCC(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12 '
               'NAME: (23Z,26Z,29Z,32Z)-3-oxooctatriacontatetraenoyl-CoA '
               'REASON: MISSED Insufficient phosphate groups for a CoA moiety\n'
               ' * SMILES: '
               'CCCCC\\C=C/C\\C=C/CCCC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)N1C=NC2=C1N=CN=C2N '
               'NAME: cis,cis-tetradeca-5,8-dienoyl-CoA REASON: MISSED '
               'Insufficient phosphate groups for a CoA moiety\n'
               ' * SMILES: '
               'C[C@H](CCCC(C)C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12)[C@H]1CC[C@H]2[C@@H]3CCC4=CC(=O)CC[C@]4(C)[C@H]3CC[C@]12C '
               'NAME: Delta(4)-dafachronoyl-CoA REASON: MISSED Insufficient '
               'phosphate groups for a CoA moiety\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'C1=CC=C2C(=C1)C(=O)C3=CC=CC=C3C2(CC4=CC(=NC=C4)F)CC5=CC(=NC=C5)F',
                                     'name': '10,10-bis[(2-fluoro-4-pyridinyl)methyl]-9-anthracenone',
                                     'reason': 'No thioester functional group '
                                               'found'},
                                 {   'smiles': 'C[C@@H](C1=CC=CC=C1)NC(=O)[C@@H]2[C@H]([C@@H]3CN4C(=CC=C(C4=O)C5=CC=CC=C5F)[C@H]2N3C)CO',
                                     'name': 'LSM-10936',
                                     'reason': 'No thioester functional group '
                                               'found'},
                                 {   'smiles': '[H]C(=CC(=O)C(O)=O)C(CC(O)=O)C(O)=O',
                                     'name': '5-oxopent-3-ene-1,2,5-tricarboxylic '
                                             'acid',
                                     'reason': 'No thioester functional group '
                                               'found'},
                                 {   'smiles': 'S1N(C2=CC=C(C=C2)C(OCC)=O)C(=O)C=C1',
                                     'name': 'ethyl '
                                             '4-(3-oxo-2,3-dihydroisothiazol-2-yl)benzoate',
                                     'reason': 'No thioester functional group '
                                               'found'},
                                 {   'smiles': 'COc1cc(O)c2c(c1)oc1c(O)cccc1c2=O',
                                     'name': 'mesuaxanthone A',
                                     'reason': 'No thioester functional group '
                                               'found'},
                                 {   'smiles': 'O([C@@H]1[C@H](O)[C@@H](O[C@@H]([C@H]1O)CO[C@H]2O[C@@H]([C@@H](O)[C@H](O)[C@@H]2O[C@@H]3O[C@@H]([C@@H](O)[C@H](O)[C@H]3NC(=O)C)CO)CO[C@@H]4O[C@@H]([C@@H](O)[C@H](O)[C@H]4NC(=O)C)CO)O[C@H]5[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]5CO)O[C@H]6[C@H](O)[C@@H](NC(=O)C)C(O[C@@H]6CO)O)[C@H]7O[C@@H]([C@@H](O[C@@H]8O[C@@H]([C@@H](O)[C@H](O)[C@H]8NC(=O)C)CO)[C@H](O)[C@@H]7O[C@@H]9O[C@@H]([C@@H](O[C@@H]%10O[C@@H]([C@H](O)[C@H](O)[C@H]%10O)CO)[C@H](O)[C@H]9NC(=O)C)CO)CO',
                                     'name': 'N-[(3R,4R,5S,6R)-5-[(2S,3R,4R,5S,6R)-3-Acetamido-5-[(2S,3S,4S,5R,6R)-6-[[(2S,3S,4S,5S,6R)-3-[(2R,3R,4R,5S,6R)-3-acetamido-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-6-[[(2R,3R,4R,5S,6R)-3-acetamido-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxymethyl]-4,5-dihydroxyoxan-2-yl]oxymethyl]-4-[(2R,3S,4S,5S,6R)-5-[(2R,3R,4R,5S,6R)-3-acetamido-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-3-[(2S,3R,4R,5S,6R)-3-acetamido-4-hydroxy-6-(hydroxymethyl)-5-[(2S,3R,4S,5R,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-3,5-dihydroxyoxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-2,4-dihydroxy-6-(hydroxymethyl)oxan-3-yl]acetamide',
                                     'reason': 'No thioester functional group '
                                               'found'},
                                 {   'smiles': 'CCCCCCCC\\C=C/CCCCCCCC(=O)OC[C@H](COP([O-])(=O)OC[C@H]([NH3+])C([O-])=O)OC(=O)CCC\\C=C/C\\C=C/C\\C=C/C\\C=C/CCCCC',
                                     'name': '1-oleoyl-2-arachidonoyl-sn-glycero-3-phospho-L-serine(1-)',
                                     'reason': 'No thioester functional group '
                                               'found'},
                                 {   'smiles': 'OC(=Cc1ccccc1)C([O-])=O',
                                     'name': 'enol-phenylpyruvate',
                                     'reason': 'No thioester functional group '
                                               'found'},
                                 {   'smiles': '[H][C@]1(CC[C@]2(C)[C@@H](O)CCC(=C)[C@@]12[H])[C@@H](O)C(C)C',
                                     'name': '(1R,3aS,4S,7aR)-1-((S)-1-hydroxy-2-methylpropyl)-3a-methyl-7-methyleneoctahydro-1H-inden-4-ol',
                                     'reason': 'No thioester functional group '
                                               'found'},
                                 {   'smiles': 'O1C(C(O)C(O)C(O)C1CO)C=2C(=O)C=3C(O)=C(C4OC(C(O)C(O)C4O)CO)C(O)=CC3OC2C5=CC=C(OC)C=C5',
                                     'name': "3,6-Diglucopyranosyl-5,7-dihydroxy-4'-methoxyflavone",
                                     'reason': 'No thioester functional group '
                                               'found'}],
    'sample_false_negatives': [   {   'smiles': 'O=NN1CCNCC1',
                                      'name': 'N-Mononitrosopiperazine',
                                      'reason': 'No thioester functional group '
                                                'found'},
                                  {   'smiles': 'O1C(CCC1)C(=O)N2CCNCC2',
                                      'name': '1-(Tetrahydro-2-furoyl)piperazine',
                                      'reason': 'No thioester functional group '
                                                'found'}],
    'attempt': 3,
    'reasoning': 'Below is my reasoning before the code:\n'
                 '\n'
                 'The previous attempt checked for the acyl‐CoA features by '
                 'looking for (a) a thioester (C(=O)S) group, (b) the “CoA '
                 'nucleotide part” by trying to find an adenine ring or a '
                 'specific pantetheine SMARTS, and (c) the presence of '
                 'phosphate groups via a phosphate SMARTS match. However, many '
                 'correct acyl‐CoA structures (for example pimeloyl‐CoA and '
                 'others) were missed because the phosphate detection (using a '
                 'rigid SMARTS pattern "[OP](=O)(O)") did not reliably capture '
                 'the multiple phosphate groups present in the CoA moiety. In '
                 'many valid examples the phosphate groups are represented in '
                 'different formats and—when using substructure matching—may '
                 'count too few matches.\n'
                 '\n'
                 'To improve this, we now count the phosphorus atoms directly '
                 '(atomic number 15) present in the molecule. In a full CoA '
                 'moiety (such as those in acyl‐CoAs) one expects at least '
                 'three phosphorus atoms. We keep the other features '
                 '(thioester check and the adenine/pantetheine fragment) as '
                 'before to strengthen the classification.\n'
                 '\n'
                 'Below is the complete improved Python program.',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 636,
    'num_false_positives': 839,
    'num_true_negatives': 140823,
    'num_false_negatives': 2,
    'num_negatives': None,
    'precision': 0.4311864406779661,
    'recall': 0.9968652037617555,
    'f1': 0.6019876952200662,
    'accuracy': 0.9940899508081518,
    'negative_predictive_value': 0.9999857979762116}