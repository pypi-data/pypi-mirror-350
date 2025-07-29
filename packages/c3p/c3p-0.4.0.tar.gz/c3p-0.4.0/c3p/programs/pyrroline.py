"""
Classifies: CHEBI:23763 pyrroline
"""
"""
Classifies: CHEBI:36437 pyrroline
"""
from rdkit import Chem

def is_pyrroline(smiles: str):
    """
    Determines if a molecule is a pyrroline based on its SMILES string.
    A pyrroline is a dihydropyrrole: a 5-membered monocyclic compound with one double bond and at least one nitrogen atom.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a pyrroline, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES"
    
    # Check for exactly one ring and it's 5-membered
    ring_info = mol.GetRingInfo()
    num_rings = len(ring_info.AtomRings())
    if num_rings != 1:
        return False, f"Found {num_rings} rings (must be monocyclic)"
    
    ring_atoms = ring_info.AtomRings()[0]
    ring_size = len(ring_atoms)
    if ring_size != 5:
        return False, f"Ring size is {ring_size} (must be 5-membered)"
    
    # Check for exactly one double bond in the ring
    ring_bonds = []
    for bond in mol.GetBonds():
        if bond.GetBeginAtomIdx() in ring_atoms and bond.GetEndAtomIdx() in ring_atoms:
            ring_bonds.append(bond)
    
    double_bonds = sum(1 for bond in ring_bonds if bond.GetBondType() == Chem.BondType.DOUBLE)
    if double_bonds != 1:
        return False, f"Found {double_bonds} double bonds in ring (needs 1)"
    
    # Check for at least one nitrogen in the ring
    has_nitrogen = any(mol.GetAtomWithIdx(idx).GetAtomicNum() == 7 for idx in ring_atoms)
    if not has_nitrogen:
        return False, "No nitrogen atom in the ring"
    
    # Ensure it's a heterocycle (no carbon-only rings)
    # Already checked for nitrogen, so this is covered
    
    return True, "5-membered monocyclic ring with one double bond and a nitrogen"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:23763',
                          'name': 'pyrroline',
                          'definition': 'Any organic heteromonocyclic compound '
                                        'with a structure based on a '
                                        'dihydropyrrole.',
                          'parents': ['CHEBI:25693', 'CHEBI:38101'],
                          'xrefs': ['Wikipedia:Pyrroline'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 36,
                           'log_lines_of_code': 3.58351893845611,
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
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 3,
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
                                                 1],
                           'max_indent': 3,
                           'imports': ['from rdkit import Chem'],
                           'imports_count': 1,
                           'methods_called': [   'GetBondType',
                                                 'GetAtomicNum',
                                                 'AtomRings',
                                                 'MolFromSmiles',
                                                 'GetBonds',
                                                 'GetRingInfo',
                                                 'GetBeginAtomIdx',
                                                 'GetAtomWithIdx',
                                                 'append',
                                                 'GetEndAtomIdx'],
                           'methods_called_count': 10,
                           'smarts_strings': [],
                           'smarts_strings_count': 0,
                           'defs': ['is_pyrroline(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES"',
                                          'False, f"Found {num_rings} rings '
                                          '(must be monocyclic)"',
                                          'False, f"Ring size is {ring_size} '
                                          '(must be 5-membered)"',
                                          'False, f"Found {double_bonds} '
                                          'double bonds in ring (needs 1)"',
                                          'False, "No nitrogen atom in the '
                                          'ring"',
                                          'True, "5-membered monocyclic ring '
                                          'with one double bond and a '
                                          'nitrogen"'],
                           'returns_count': 6,
                           'complexity': 4.7167037876912215},
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
    'sample_true_negatives': [   {   'smiles': 'O=C1NC=C2[C@@]3(O)[C@@H](O)[C@@H](OC2=C1OC(=O)[C@H]4[C@H]5[C@H](C=C[C@H]4C)C[C@H](C)CC5)[C@@H](O)CC3',
                                     'name': 'Arthpyrone D',
                                     'reason': 'Found 5 rings (must be '
                                               'monocyclic)'},
                                 {   'smiles': 'CCN(CC)S(=O)(=O)C1=CC=CC(=C1)C(=O)NC2=CC(=CC(=C2)C)C',
                                     'name': '3-(diethylsulfamoyl)-N-(3,5-dimethylphenyl)benzamide',
                                     'reason': 'Found 2 rings (must be '
                                               'monocyclic)'},
                                 {   'smiles': 'O=C1[C@@]([C@H]2[C@]([C@@H]3C(C[C@](C=C)(C)CC3)=CC2)(C)CC1)(CO[C@@H]4O[C@H](C(=O)O)[C@@H](O)[C@H]([C@@H]4O)O)C',
                                     'name': 'Virescenoside Z4',
                                     'reason': 'Found 4 rings (must be '
                                               'monocyclic)'},
                                 {   'smiles': 'C[C@H]1CN(C(=O)CCCN2C(=CN=N2)CO[C@@H]1CN(C)C(=O)NC3=CC=CC(=C3)C(F)(F)F)[C@@H](C)CO',
                                     'name': '1-[[(8S,9S)-6-[(2S)-1-hydroxypropan-2-yl]-8-methyl-5-oxo-10-oxa-1,6,14,15-tetrazabicyclo[10.3.0]pentadeca-12,14-dien-9-yl]methyl]-1-methyl-3-[3-(trifluoromethyl)phenyl]urea',
                                     'reason': 'Found 3 rings (must be '
                                               'monocyclic)'},
                                 {   'smiles': 'O([C@H]1[C@@H](O)[C@H](O[C@@H]2O[C@@H]([C@@H](O[C@@H]3O[C@@H]([C@H](O)[C@H](O[C@H]4O[C@@H]([C@H](O)[C@H](O)[C@H]4O)CO)[C@H]3O)CO)[C@H](O)[C@H]2NC(=O)C)CO)[C@H](O[C@@H]1O[C@H]5[C@H](O)[C@H](O[C@@H](O[C@H]6[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]6CO)O[C@H]7[C@H](O)[C@@H](NC(=O)C)C(O[C@@H]7CO[C@@H]8O[C@H]([C@@H](O)[C@@H](O)[C@@H]8O)C)O)[C@H]5O)CO[C@H]9O[C@@H]([C@@H](O)[C@H](O)[C@@H]9O[C@@H]%10O[C@@H]([C@@H](O[C@@H]%11O[C@@H]([C@H](O)[C@H](O[C@]%12(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%12)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%11O)CO)[C@H](O)[C@H]%10NC(=O)C)CO)CO)CO)[C@@H]%13O[C@@H]([C@@H](O[C@@H]%14O[C@@H]([C@H](O)[C@H](O[C@]%15(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%15)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%14O)CO)[C@H](O)[C@@H]%13NC(=O)C)CO',
                                     'name': 'CID 91846694',
                                     'reason': 'Found 15 rings (must be '
                                               'monocyclic)'},
                                 {   'smiles': 'CCOC(=O)NCC(C)(C)CNC(=O)OCC',
                                     'name': 'N-[3-(ethoxycarbonylamino)-2,2-dimethylpropyl]carbamic '
                                             'acid ethyl ester',
                                     'reason': 'Found 0 rings (must be '
                                               'monocyclic)'},
                                 {   'smiles': 'S1C(=NC(=C1)/C=C/C(OC)C(/C(/OC)=C\\C(=O)OC)C)C2N=C(C3(OC3)C)SC2',
                                     'name': 'Melithiazol K',
                                     'reason': 'Found 3 rings (must be '
                                               'monocyclic)'},
                                 {   'smiles': 'CCCCC\\C=C/C\\C=C/CCCCCC(=O)O[C@@H](CO[C@@H]1O[C@H](CO)[C@H](O)[C@H](O)[C@H]1O)COC(=O)CCCCC\\C=C/C\\C=C/C\\C=C/CC',
                                     'name': '(2S)-1-O-(7Z,10Z,13Z)-hexadecatrienoyl-2-O-(7Z,10Z)-hexadecadienoyl-3-O-beta-D-galactopyranosyl-sn-glycerol',
                                     'reason': 'Ring size is 6 (must be '
                                               '5-membered)'},
                                 {   'smiles': 'CC(C)(C)OC(=O)N[C@H]1CCCCCC=C[C@@H]2C[C@]2(NC(=O)[C@@H]3C[C@H](CN3C1=O)OC(=O)N4CC5=C(C4)C(=CC=C5)F)CNS(=O)(=O)C6CC6',
                                     'name': 'LSM-5352',
                                     'reason': 'Found 6 rings (must be '
                                               'monocyclic)'},
                                 {   'smiles': 'O=C1O[C@@H]2C[C@@]3(O[C@H](/C(=C/C)/C)[C@@H](C)C[C@H]3O)O[C@@H](C2)CC=C(C[C@H](C=CC=C4[C@]5([C@H]1C=C([C@@H](O)C5OC4)COC(=O)CC6=COC=C6)O)C)C',
                                     'name': 'VM48642',
                                     'reason': 'Found 6 rings (must be '
                                               'monocyclic)'}],
    'sample_false_negatives': [   {   'smiles': 'CC1=CC=C(C=C1)N2C(=C(C(=O)C2=CC3=CC=C(C=C3)O)C(=O)OC)C',
                                      'name': '5-[(4-hydroxyphenyl)methylidene]-2-methyl-1-(4-methylphenyl)-4-oxo-3-pyrrolecarboxylic '
                                              'acid methyl ester',
                                      'reason': 'Found 3 rings (must be '
                                                'monocyclic)'},
                                  {   'smiles': 'O=C1NCC(C1=C(O)C2(C3C(C=C(C2CCC(C(O)C(=CCC(O)C=CC(C(O)C=CCC(O)C=CCC(O)CC4N(C(=N)N)CCC4)C)C)C)C)C(O)C(O)CC3)C)=O',
                                      'name': 'TPU-0037A',
                                      'reason': 'Found 4 rings (must be '
                                                'monocyclic)'},
                                  {   'smiles': 'Clc1ccc(COc2ccc(cc2)N2C(=O)C3=C(CCCC3)C2=O)cc1',
                                      'name': 'MK-129',
                                      'reason': 'Found 4 rings (must be '
                                                'monocyclic)'},
                                  {   'smiles': 'O=C1NCC(C1=C(O)C2(C3C(C=C(C2CCC(C(O)C(=CCC(O)C=CC(C(O)C=CCC(O)C=CCC(O)CC4N(C(=N)N)CCC4)C)C)C)C)C(O)CCC3)C)=O',
                                      'name': 'TPU-0037C',
                                      'reason': 'Found 4 rings (must be '
                                                'monocyclic)'},
                                  {   'smiles': 'O=C1N(OC)C(=C)C2=C1[C@H](O)[C@](O)(C)[C@@H](O2)CCCCCCC',
                                      'name': 'Phyllostictine A',
                                      'reason': 'Found 2 rings (must be '
                                                'monocyclic)'},
                                  {   'smiles': '[H][C@]12CC[C@H](C)C[C@]1(C)C=C(C)[C@@H]([C@@H]2C(=O)C1=C\\C(NC1=O)=C\\C1=CC=C(O)C=C1)C(\\C)=C\\C(C)CC',
                                      'name': 'talaroconvolutin A',
                                      'reason': 'Found 4 rings (must be '
                                                'monocyclic)'},
                                  {   'smiles': 'O=C1NCCC[C@@H]2NC(=O)C(C2=O)=C(O)C=C[C@@H]3[C@@H](CC=C1)[C@H]4[C@@H]([C@H]5[C@@H](C(CC)=C[C@H]5C4)CO)CC3',
                                      'name': 'Pactamide D',
                                      'reason': 'Found 5 rings (must be '
                                                'monocyclic)'},
                                  {   'smiles': 'CCN1C2C(C(=NC2NC3=CC=CC=C31)OC)C4=CC=CC=C4',
                                      'name': '4-ethyl-2-methoxy-3-phenyl-3,3a,9,9a-tetrahydropyrrolo[2,3-b]quinoxaline',
                                      'reason': 'Found 4 rings (must be '
                                                'monocyclic)'},
                                  {   'smiles': 'OC1=C2[N+](=CC=C1)[C@@H](/C=C(/C=C/C3CC3)\\C)[C@@H]([C@]2(O)C)O',
                                      'name': 'Cyclizidine F',
                                      'reason': 'Found 3 rings (must be '
                                                'monocyclic)'},
                                  {   'smiles': 'O=C1NCC(C1=C(O)[C@@]2([C@H]3[C@@H](C=C([C@H]2CCC(C(O)/C(=C/CC(O)/C=C/C(C(O)/C=C/CC(O)/C(=C/CC(O)CC4N(C(=N)N)CCC4)/C)C)/C)C)C)[C@H](O)[C@H](O)CC3)C)=O',
                                      'name': 'Lydicamycin',
                                      'reason': 'Found 4 rings (must be '
                                                'monocyclic)'}],
    'attempt': 1,
    'reasoning': '</think>\n'
                 '\n'
                 "Okay, let's try to figure out why the previous code didn't "
                 'work. The error message was "unexpected indent" which '
                 "usually means there's a spacing issue in the code. Looking "
                 'at the previous code, I notice that the examples provided '
                 'after the problem description are just a list of SMILES '
                 "strings and names, but they aren't part of the actual code. "
                 "However, the user's previous attempt included a code block "
                 'that might have had incorrect indentation or structure.\n'
                 '\n'
                 'The main goal is to create a function called `is_pyrroline` '
                 'that checks if a SMILES string represents a pyrroline. '
                 'Pyrrolines are dihydropyrroles, which are 5-membered rings '
                 'with one double bond and one NH group. So the key is to '
                 'identify that structure.\n'
                 '\n'
                 'First, I need to make sure the molecule is a 5-membered '
                 "ring. Then, check that it's a heterocycle with at least one "
                 'nitrogen. Also, there should be exactly one double bond in '
                 'the ring to account for the dihydro part (since pyrrole is '
                 'fully unsaturated, dihydropyrrole would have one double '
                 'bond).\n'
                 '\n'
                 'Possible steps:\n'
                 '1. Parse the SMILES into a molecule.\n'
                 "2. Check if it's a single ring with 5 members.\n"
                 '3. Ensure the ring is fully saturated except for one double '
                 'bond.\n'
                 "4. Verify there's at least one nitrogen in the ring.\n"
                 "5. Make sure it's a monocyclic compound (no fused rings).\n"
                 '\n'
                 'Wait, but some examples might have substituents. The problem '
                 'states "any organic heteromonocyclic compound based on '
                 'dihydropyrrole," so substituents are allowed as long as the '
                 'core ring is correct.\n'
                 '\n'
                 'So the plan is:\n'
                 '- Use RDKit to find rings in the molecule.\n'
                 "- Check if there's exactly one 5-membered ring.\n"
                 '- In that ring, count the number of double bonds (should be '
                 '1).\n'
                 '- Check that the ring contains at least one nitrogen.\n'
                 '- Ensure the molecule is monocyclic (no other rings).\n'
                 '\n'
                 'Let me structure the code accordingly. Also, handle invalid '
                 'SMILES and make sure the function returns a boolean and a '
                 'reason.\n'
                 '\n'
                 'Potential issues in previous code: Maybe the SMARTS pattern '
                 "was incorrect, or the code had syntax errors. Let's use the "
                 'correct SMARTS for a 5-membered ring with one double bond '
                 'and a nitrogen.\n'
                 '\n'
                 'Testing with example SMILES like "C1CC=CN1" (2-pyrroline) '
                 "should match. Let's ensure the code captures that.\n"
                 '\n'
                 'Another consideration: The ring might have substituents, so '
                 'the SMARTS should focus on the ring atoms. Using '
                 '`GetRingInfo()` in RDKit can help identify the rings and '
                 'their sizes.\n'
                 '\n'
                 'So, putting it all together:',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 44,
    'num_false_positives': 120,
    'num_true_negatives': 142074,
    'num_false_negatives': 62,
    'num_negatives': None,
    'precision': 0.2682926829268293,
    'recall': 0.41509433962264153,
    'f1': 0.32592592592592595,
    'accuracy': 0.9987210119465917,
    'negative_predictive_value': 0.9995637980525693}