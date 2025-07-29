"""
Classifies: CHEBI:38077 polypyrrole
"""
"""
Classifies: CHEBI:52236 polypyrrole
A compound composed of two or more pyrrole units.
"""
from rdkit import Chem
from rdkit.Chem import rdMolDescriptors

def is_polypyrrole(smiles: str):
    """
    Determines if a molecule is a polypyrrole based on its SMILES string.
    A polypyrrole is a compound composed of two or more pyrrole units.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a polypyrrole, False otherwise
        str: Reason for classification
    """
    
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Look for pyrrole substructure
    pyrrole_pattern = Chem.MolFromSmarts("c1ccnc1")
    pyrrole_matches = mol.GetSubstructMatches(pyrrole_pattern)
    
    # Require at least two pyrrole units
    if len(pyrrole_matches) < 2:
        return False, "Less than two pyrrole units found"
    
    # Count number of nitrogen atoms
    n_nitrogens = sum(1 for atom in mol.GetAtoms() if atom.GetAtomicNum() == 7)
    
    # Require at least two nitrogen atoms (from pyrrole units)
    if n_nitrogens < 2:
        return False, "Less than two nitrogen atoms found"
    
    # Check for conjugated ring system
    conjugated_rings = []
    ring_info = mol.GetRingInfo()
    for ring in ring_info.AtomRings():
        bond_orders = [mol.GetBondBetweenAtoms(ring[i], ring[i-1]).GetBondTypeAsDouble() for i in range(len(ring))]
        if sum(bond_orders) % 2 == 0 and any(order == 2 for order in bond_orders):
            conjugated_rings.append(ring)
    
    if not conjugated_rings:
        return False, "No conjugated ring system found"
    
    # Check molecular weight - polypyrroles typically >100 Da
    mol_wt = rdMolDescriptors.CalcExactMolWt(mol)
    if mol_wt < 100:
        return False, "Molecular weight too low for polypyrrole"
    
    return True, "Contains two or more pyrrole units in a conjugated ring system"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:38077',
                          'name': 'polypyrrole',
                          'definition': 'A compound composed of two or more '
                                        'pyrrole units.',
                          'parents': ['CHEBI:38101'],
                          'xrefs': ['Beilstein:8538310'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 38,
                           'log_lines_of_code': 3.6375861597263857,
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
                                                 1,
                                                 2,
                                                 0,
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
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 3,
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
                           'max_indent': 3,
                           'imports': [   'from rdkit import Chem',
                                          'from rdkit.Chem import '
                                          'rdMolDescriptors'],
                           'imports_count': 2,
                           'methods_called': [   'GetBondTypeAsDouble',
                                                 'MolFromSmarts',
                                                 'AtomRings',
                                                 'CalcExactMolWt',
                                                 'GetAtoms',
                                                 'GetAtomicNum',
                                                 'GetBondBetweenAtoms',
                                                 'append',
                                                 'GetRingInfo',
                                                 'MolFromSmiles',
                                                 'GetSubstructMatches'],
                           'methods_called_count': 11,
                           'smarts_strings': ['c1ccnc1'],
                           'smarts_strings_count': 1,
                           'defs': ['is_polypyrrole(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "Less than two pyrrole units '
                                          'found"',
                                          'False, "Less than two nitrogen '
                                          'atoms found"',
                                          'False, "No conjugated ring system '
                                          'found"',
                                          'False, "Molecular weight too low '
                                          'for polypyrrole"',
                                          'True, "Contains two or more pyrrole '
                                          'units in a conjugated ring system"'],
                           'returns_count': 6,
                           'complexity': 4.927517231945277},
    'message': '\n'
               'Error: Error executing '
               "is_polypyrrole('[Zn+2].O=C(O)CCC=1C=2N=C(C1C)C=C3NC(=CC=4NC(C=C5N=C(C2)C(=C5CCC(=O)O)C)=C(C4CCC(=O)O)C)C(=C3CCC(=O)O)C'):\n"
               " 'RingInfo' object has no attribute 'IsCycleConjugated'\n"
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
               'to improve.\n'
               'IMPORTANT NOTE: I do not have 100% confidence in the benchmark '
               'I am using. There may be occasional and systematic mistakes. '
               'Use your best judgment, and if you think the classifications '
               'your program are consistent with your understanding if the '
               'meaning of the chemical class, then you can ignore outliers, '
               'but explain your reasoning in doing so. I have great '
               'confidence in your broad understanding of chemistry and your '
               'ability to translate this into code.',
    'sample_true_negatives': [   {   'smiles': '[H][C@@]1(CC[C@@]2(C)C3=C(CC[C@]12C)[C@@]1(C)CCC(=O)C(C)(C)[C@]1([H])CC3)[C@@H](CC[C@H](O)C(C)(C)O)C(O)=O',
                                     'name': 'fomitopinic acid A',
                                     'reason': 'Less than two pyrrole units '
                                               'found'},
                                 {   'smiles': '[Cn]',
                                     'name': 'copernicium atom',
                                     'reason': 'Less than two pyrrole units '
                                               'found'},
                                 {   'smiles': 'C1=C[C@@H]([C@H](O[C@@H]1CC(=O)NCCC2=CC=NC=C2)CO)NC(=O)C3=CC=C(C=C3)F',
                                     'name': '4-fluoro-N-[(2S,3S,6R)-2-(hydroxymethyl)-6-[2-oxo-2-(2-pyridin-4-ylethylamino)ethyl]-3,6-dihydro-2H-pyran-3-yl]benzamide',
                                     'reason': 'Less than two pyrrole units '
                                               'found'},
                                 {   'smiles': 'O=C(O)/C=C/C=C/C=C/[C@@H]1[C@@H](C(=C[C@H]2[C@H]1CC=C(C2)C)C)[C@]3(O[C@@H]3[C@@H](CC)C)C',
                                     'name': 'Pyrenulic acid A',
                                     'reason': 'Less than two pyrrole units '
                                               'found'},
                                 {   'smiles': 'O([C@@H]1[C@H](O)[C@H](O[C@H]2[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]2CO)O[C@H]3[C@H](O)[C@@H](NC(=O)C)C(O[C@@H]3CO)O)O[C@@H]([C@H]1O)CO[C@H]4O[C@@H]([C@@H](O)[C@H](O)[C@@H]4O)CO)[C@H]5O[C@@H]([C@@H](O)[C@H](O)[C@@H]5O[C@@H]6O[C@@H]([C@@H](O)[C@H](O[C@@H]7O[C@@H]([C@H](O)[C@H](O)[C@H]7O)CO)[C@H]6NC(=O)C)CO)CO',
                                     'name': 'N-[(3R,4R,5S,6R)-5-[(2S,3R,4R,5S,6R)-3-Acetamido-5-[(2S,3S,4S,5R,6R)-4-[(2R,3S,4S,5S,6R)-3-[(2S,3R,4R,5S,6R)-3-acetamido-5-hydroxy-6-(hydroxymethyl)-4-[(2R,3R,4S,5R,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxy-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-3,5-dihydroxy-6-[[(2S,3S,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxymethyl]oxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-2,4-dihydroxy-6-(hydroxymethyl)oxan-3-yl]acetamide',
                                     'reason': 'Less than two pyrrole units '
                                               'found'},
                                 {   'smiles': 'C1=CC=C(C(=C1CC)NC(CCl)=O)C',
                                     'name': 'N-(2-ethyl-6-methylphenyl)-2-chloroacetamide',
                                     'reason': 'Less than two pyrrole units '
                                               'found'},
                                 {   'smiles': 'CCCCCCCCCCCCCCCC(=O)OC[C@H](COP(O)(=O)OCCN)OC(=O)CCCCCCCCC\\C=C/CCCCCC',
                                     'name': '1-hexadecanoyl-2-(11Z-octadecenoyl)-sn-glycero-3-phosphoethanolamine',
                                     'reason': 'Less than two pyrrole units '
                                               'found'},
                                 {   'smiles': 'C1(C2=C(C(=CC(=C2)C(O)=O)O)O)=C(C(=CC(=C1)C(=O)O)OC)O',
                                     'name': "5,6,6'-trihydroxy-5'-methoxy[biphenyl]-3,3'-dicarboxylic "
                                             'acid',
                                     'reason': 'Less than two pyrrole units '
                                               'found'},
                                 {   'smiles': 'O=C1NC2=CC(O)=CC(=C2)CCC=C([C@@H](O)[C@@H](C)[C@H](CC=CC=CC=C[C@@H](C1)OC)OC(=O)[C@@H](NC(=O)C3=CCCCC3)C)C',
                                     'name': 'Trienomycin D',
                                     'reason': 'Less than two pyrrole units '
                                               'found'},
                                 {   'smiles': 'Nc1nc2n(cnc2c(=O)[nH]1)[C@@H]1O[C@H](COP(O)(=O)OP(O)(=O)OC2O[C@H](CO)[C@@H](O)[C@H](O)[C@@H]2O)[C@@H](O)[C@H]1O',
                                     'name': 'GDP-D-mannose',
                                     'reason': 'Less than two pyrrole units '
                                               'found'}],
    'sample_false_negatives': [   {   'smiles': 'C1=CC(=Cc2ccc[nH]2)N=C1',
                                      'name': 'dipyrrin',
                                      'reason': 'Less than two pyrrole units '
                                                'found'},
                                  {   'smiles': 'C[C@@]1(CCC(O)=O)[C@@H](CC(O)=O)C2=C3N4C(=CC5=[N+]6C(C[C@]7(C)N8C(=CC1=[N+]2[Co--]468)C(CCC(O)=O)=C7CC(O)=O)=C(CCC(O)=O)[C@]5(C)CC(O)=O)[C@@H](CCC(O)=O)[C@]3(C)CC(O)=O',
                                      'name': 'cobalt-precorrin-5B',
                                      'reason': 'Less than two pyrrole units '
                                                'found'},
                                  {   'smiles': '[Zn+2].O=C(O)CCC=1C=2N=C(C1C)C=C3NC(=CC=4NC(C=C5N=C(C2)C(=C5CCC(=O)O)C)=C(C4CCC(=O)O)C)C(=C3CCC(=O)O)C',
                                      'name': 'Zincmethylphyrin I',
                                      'reason': 'No conjugated ring system '
                                                'found'},
                                  {   'smiles': '[H][C@]12N=C(C(C)C3=N[C@@](C)(CC4=C(CCC(O)=O)[C@](C)(CC(O)=O)C(/C=C5\\N[C@]1(C)[C@@](C)(CC(O)=O)[C@@H]5CCC(O)=O)=N4)C(C)=C3CCC(O)=O)[C@](C)(CCC(O)=O)[C@H]2CC(O)=O',
                                      'name': 'precorrin-7',
                                      'reason': 'Less than two pyrrole units '
                                                'found'},
                                  {   'smiles': 'C1=C2C(=C(C(N2)=CC3=NC(C(=C3C)CC)=CC=4NC(=C(C4C)CCC(=O)O)C=C5N=C1C(=C5CCC(=O)O)C)CC)C',
                                      'name': 'mesoporphyrin IX',
                                      'reason': 'No conjugated ring system '
                                                'found'},
                                  {   'smiles': 'COC(=O)CCc1c(C)c2cc3nc(cc4[nH]c(cc5nc(cc1[nH]2)c(CCC(O)=O)c5C)[C@]1(C)[C@H](C(=O)OC)C(=CC=C41)C(=O)OC)c(C)c3C=C',
                                      'name': '(2R,2(1)S)8-ethenyl-2(1),2(2)-bis(methoxycarbonyl)-13-(3-methoxy-3-oxopropyl)-2,7,12,18-tetramethyl-2,2(1)-dihydrobenzo[b]porphyrin-17-propanoic '
                                              'acid',
                                      'reason': 'Less than two pyrrole units '
                                                'found'},
                                  {   'smiles': 'C1(=CC=2NC(=C(C2C)CCC(=O)O)C=C3NC(C(=C3CCC(=O)O)C)=O)NC(C(=C1C)C=C)=O',
                                      'name': 'biotripyrrin-b',
                                      'reason': 'Less than two pyrrole units '
                                                'found'},
                                  {   'smiles': 'OC(=O)CCc1c2Cc3[nH]c(Cc4[nH]c(Cc5[nH]c(Cc([nH]2)c1CC(O)=O)c(CCC(O)=O)c5CC(O)=O)c(CCC(O)=O)c4CC(O)=O)c(CC(O)=O)c3CCC(O)=O',
                                      'name': 'uroporphyrinogen III',
                                      'reason': 'No conjugated ring system '
                                                'found'},
                                  {   'smiles': '[H][C@@]12[C@H](CC(O)=O)[C@@](C)(CCC(O)=O)C3=C(C)C4=[N+]5C(=CC6=[N+]7C(=C(C)C8=[N+]([C@]1(C)[C@@](C)(CC(O)=O)[C@@H]8CCC(O)=O)[Co--]57N23)[C@@](C)(CC(N)=O)[C@@H]6CCC(O)=O)C(C)(C)[C@@H]4CCC(O)=O',
                                      'name': 'cob(II)yrinic acid c monoamide',
                                      'reason': 'Less than two pyrrole units '
                                                'found'},
                                  {   'smiles': 'OC=1CC2=C3NC([C@H]([C@@H]3CCC(O)=O)C)=CC4=NC(C(=C4C)C(O)C)=CC5=NC(=CC=6N=C2C1C6CC)C(CC(C)C)=C5C',
                                      'name': '12-Ethyl-8-isobutylbacteriochlorophyllide '
                                              'D',
                                      'reason': 'Less than two pyrrole units '
                                                'found'}],
    'attempt': 1,
    'reasoning': "Based on the error message `'RingInfo' object has no "
                 "attribute 'IsCycleConjugated'`, it seems that the "
                 '`IsCycleConjugated` method is not available in the version '
                 'of RDKit you are using. This method is used to check if a '
                 'ring system is conjugated, which is one of the criteria for '
                 'classifying a molecule as a polypyrrole.\n'
                 '\n'
                 'To improve the program, we need to find an alternative way '
                 'to check for conjugation in the ring system. One approach '
                 'could be to check if the bonds in the ring system are '
                 'alternating between single and double bonds, which is a '
                 'characteristic of a conjugated system.\n'
                 '\n'
                 'Additionally, the program could be improved by considering '
                 'other structural features of polypyrroles, such as the '
                 'presence of a linear backbone or cross-linking between '
                 'pyrrole units.\n'
                 '\n'
                 "As for the outcomes, it's difficult to assess the accuracy "
                 'of the program without having access to the benchmark '
                 "dataset. However, if the program's classifications align "
                 'with your understanding of polypyrroles, and the reasoning '
                 "behind the program is sound, you can trust the program's "
                 'output over the benchmark, especially if the benchmark is '
                 'known to have occasional mistakes.\n'
                 '\n'
                 "Here's an improved version of the program that checks for "
                 'alternating single and double bonds in the ring system:',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 83,
    'num_false_positives': 117,
    'num_true_negatives': 141900,
    'num_false_negatives': 200,
    'num_negatives': None,
    'precision': 0.415,
    'recall': 0.29328621908127206,
    'f1': 0.3436853002070393,
    'accuracy': 0.9977723120168658,
    'negative_predictive_value': 0.9985925404644617}