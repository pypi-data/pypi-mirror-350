"""
Classifies: CHEBI:17962 CDP-diacylglycerol
"""
"""
Classifies: CDP-diacylglycerol
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_CDP_diacylglycerol(smiles: str):
    """
    Determines if a molecule is a CDP-diacylglycerol based on its SMILES string.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a CDP-diacylglycerol, False otherwise
        str: Reason for classification
    """
    
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for cytosine base connected to ribose sugar
    cytidine_patterns = [
        # Various representations of cytidine (cytosine + ribose)
        Chem.MolFromSmarts("[CH2]1[CH]([CH]([OH])[CH]([OH])O1)N2C=CC(=NC2=O)N"),
        Chem.MolFromSmarts("[CH2]1[CH]([CH]([OH])[CH]([OH])O1)n2ccc(N)nc2=O"),
        Chem.MolFromSmarts("OC[C@H]1O[C@@H](N2C=CC(=NC2=O)N)C(O)[C@H]1O"),
        Chem.MolFromSmarts("OC[C@H]1O[C@H](n2ccc(N)nc2=O)[C@H](O)[C@@H]1O")
    ]
    
    has_cytidine = any(mol.HasSubstructMatch(pattern) for pattern in cytidine_patterns if pattern is not None)
    if not has_cytidine:
        return False, "No cytidine moiety found"

    # Check for diphosphate bridge
    diphosphate_patterns = [
        Chem.MolFromSmarts("OP(=O)(O)OP(=O)(O)O"),
        Chem.MolFromSmarts("[OX2]P(=O)([OX2])OP(=O)([OX2])[OX2]"),
        Chem.MolFromSmarts("P(O)(=O)OP(O)(=O)O")
    ]
    has_diphosphate = any(mol.HasSubstructMatch(pattern) for pattern in diphosphate_patterns if pattern is not None)
    if not has_diphosphate:
        return False, "No diphosphate bridge found"

    # Check for glycerol backbone with two ester groups
    glycerol_patterns = [
        Chem.MolFromSmarts("[CH2X4]([OX2]C(=O))[CHX4]([OX2]C(=O))[CH2X4]O"),
        Chem.MolFromSmarts("[CH2]([OX2]C(=O))[CH]([OX2]C(=O))[CH2]OP"),
        Chem.MolFromSmarts("OCC(COC(=O))OC(=O)"),
        Chem.MolFromSmarts("OC[C@H](OC(=O))COC(=O)")
    ]
    has_glycerol = any(mol.HasSubstructMatch(pattern) for pattern in glycerol_patterns if pattern is not None)
    if not has_glycerol:
        return False, "No glycerol backbone with two ester groups found"

    # Count ester groups (should be exactly 2)
    ester_pattern = Chem.MolFromSmarts("[OX2]C(=O)[#6]")
    ester_matches = mol.GetSubstructMatches(ester_pattern)
    if len(ester_matches) != 2:
        return False, f"Found {len(ester_matches)} ester groups, need exactly 2"

    # Check for long carbon chains (fatty acids)
    fatty_acid_pattern = Chem.MolFromSmarts("[CX4,CX3]~[CX4,CX3]~[CX4,CX3]~[CX4,CX3]~[CX4,CX3]")
    fatty_acid_matches = mol.GetSubstructMatches(fatty_acid_pattern)
    if len(fatty_acid_matches) < 2:
        return False, "Missing long carbon chains for fatty acids"

    # Verify complete connectivity
    # The molecule should have all components connected:
    # cytidine-diphosphate-glycerol-fatty_acids
    if len(Chem.GetMolFrags(mol)) > 1:
        return False, "Disconnected fragments found"

    # Count key atoms
    c_count = sum(1 for atom in mol.GetAtoms() if atom.GetAtomicNum() == 6)
    o_count = sum(1 for atom in mol.GetAtoms() if atom.GetAtomicNum() == 8)
    n_count = sum(1 for atom in mol.GetAtoms() if atom.GetAtomicNum() == 7)
    p_count = sum(1 for atom in mol.GetAtoms() if atom.GetAtomicNum() == 15)

    # Basic element count checks
    if c_count < 20:
        return False, "Too few carbons for CDP-diacylglycerol"
    if o_count < 12:
        return False, "Too few oxygens for CDP-diacylglycerol"
    if n_count != 3:
        return False, "Should have exactly 3 nitrogens (cytosine)"
    if p_count != 2:
        return False, "Should have exactly 2 phosphorus atoms"

    # Calculate molecular weight
    mol_wt = rdMolDescriptors.CalcExactMolWt(mol)
    if mol_wt < 800:  # CDP-diacylglycerols are typically >800 Da
        return False, "Molecular weight too low for CDP-diacylglycerol"

    return True, "Contains cytidine diphosphate group connected to glycerol backbone with two fatty acid chains"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:17962',
                          'name': 'CDP-diacylglycerol',
                          'definition': 'A CDP-glycerol having unspecified '
                                        'acyl groups (most commonly fatty acyl '
                                        'groups) at the 1- and 2-positions.',
                          'parents': ['CHEBI:35774'],
                          'xrefs': [   'KEGG:C00269',
                                       'LIPID_MAPS_instance:LMGP13010000',
                                       'PMID:12950685'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': None,
    'message': '\n'
               'Attempt failed: F1 score of 0 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: NONE\n'
               'False positives: NONE\n'
               'False negatives: SMILES: '
               'P(OC[C@H]1O[C@@H](N2C=CC(=NC2=O)N)C(O)[C@H]1O)(OP(OC[C@H](OC(=O)CCCCCCCCCC(C)C)COC(=O)CCCCCCCCCCCCCCCCCCC(C)C)(O)=O)(O)=O '
               'NAME: CDP-DG(I-22:0/I-13:0) REASON: MISSED No ribose sugar '
               'found or not correctly connected to cytosine\n'
               ' * SMILES: '
               'P(OC[C@H]1O[C@@H](N2C=CC(=NC2=O)N)C(O)[C@H]1O)(OP(OC[C@H](OC(=O)CCCCCCCCCCC(CC)C)COC(=O)CCCCCCC/C=C\\C=C/CCCCCC)(O)=O)(O)=O '
               'NAME: CDP-DG(18:2(9Z,11Z)/a-15:0) REASON: MISSED No ribose '
               'sugar found or not correctly connected to cytosine\n'
               ' * SMILES: '
               'P(OC[C@H]1O[C@@H](N2C=CC(=NC2=O)N)C(O)[C@H]1O)(OP(OC[C@H](OC(=O)CCCCCCCCC(C)C)COC(=O)CCCCCCCCC(CC)C)(O)=O)(O)=O '
               'NAME: CDP-DG(a-13:0/i-12:0) REASON: MISSED No ribose sugar '
               'found or not correctly connected to cytosine\n'
               ' * SMILES: '
               'P(OC[C@H]1O[C@@H](N2C=CC(=NC2=O)N)C(O)[C@H]1O)(OP(OC[C@H](OC(=O)CCCCCCCCCCCCCC(C)C)COC(=O)CCCCCCCCCCCCCC(C)C)(O)=O)(O)=O '
               'NAME: '
               '({[(2R)-2,3-bis[(15-methylhexadecanoyl)oxy]propoxy](hydroxy)phosphoryl}oxy)({[(2R,3R,5R)-3,4-dihydroxy-5-(2-hydroxy-4-imino-1,4-dihydropyrimidin-1-yl)oxolan-2-yl]methoxy})phosphinic '
               'acid REASON: MISSED No ribose sugar found or not correctly '
               'connected to cytosine\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCC(=O)OC[C@H](COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1O)n1ccc(N)nc1=O)OC(=O)CC\\C=C/C\\C=C/C\\C=C/C\\C=C/C\\C=C/C\\C=C/CC '
               'NAME: '
               'CDP-1-stearoyl-2-(4Z,7Z,10Z,13Z,16Z,19Z)-docosahexaenoyl-sn-glycerol '
               'REASON: MISSED No ribose sugar found or not correctly '
               'connected to cytosine\n'
               ' * SMILES: '
               'P(OC[C@H]1O[C@@H](N2C=CC(=NC2=O)N)C(O)[C@H]1O)(OP(OC[C@H](OC(=O)CCCCCCCCCCCCC(C)C)COC(=O)CCCCCCC/C=C\\C=C/CCCCCC)(O)=O)(O)=O '
               'NAME: CDP-DG(18:2(9Z,11Z)/i-16:0) REASON: MISSED No ribose '
               'sugar found or not correctly connected to cytosine\n'
               ' * SMILES: '
               'P(OC[C@H]1O[C@@H](N2C=CC(=NC2=O)N)C(O)[C@H]1O)(OP(OC[C@H](OC(=O)CCCCCCC/C=C\\C=C/CCCCCC)COC(=O)CCCCCCCCC(CC)C)(O)=O)(O)=O '
               'NAME: CDP-DG(A-13:0/18:2(9Z,11Z)) REASON: MISSED No ribose '
               'sugar found or not correctly connected to cytosine\n'
               ' * SMILES: '
               'P(OC[C@H]1O[C@@H](N2C=CC(=NC2=O)N)C(O)[C@H]1O)(OP(OC[C@H](OC(=O)CCCCCCCCCCCC(C)C)COC(=O)CCCCCCCCC(CC)C)(O)=O)(O)=O '
               'NAME: CDP-DG(a-13:0/i-15:0) REASON: MISSED No ribose sugar '
               'found or not correctly connected to cytosine\n'
               ' * SMILES: '
               'P(OC[C@H]1O[C@@H](N2C=CC(=NC2=O)N)[C@H](O)[C@@H]1O)(OP(OC[C@H](OC(=O)CCCCCCC[C@H](O)[C@@H](O)C/C=C\\CCCCC)COC(=O)CCCCCCCCCCCCCCCCC(CC)C)(O)=O)(O)=O '
               'NAME: CDP-DG(a-21:0/18:1(12Z)-2OH(9,10)) REASON: MISSED No '
               'ribose sugar found or not correctly connected to cytosine\n'
               ' * SMILES: '
               'P(OC[C@H]1O[C@@H](N2C=CC(=NC2=O)N)[C@H](O)[C@@H]1O)(OP(OC[C@H](OC(=O)CCCCCCCC3OC3C/C=C\\CCCCC)COC(=O)CCCCCCCCC(C)C)(O)=O)(O)=O '
               'NAME: CDP-DG(i-12:0/18:1(12Z)-O(9S,10R)) REASON: MISSED No '
               'ribose sugar found or not correctly connected to cytosine\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'C[C@@H](C1=CC=CC=C1)NC(=O)C[C@H]2CC[C@@H]([C@@H](O2)CO)NC(=O)CN3CCOCC3',
                                     'name': '2-[(2R,5S,6R)-6-(hydroxymethyl)-5-[[2-(4-morpholinyl)-1-oxoethyl]amino]-2-oxanyl]-N-[(1S)-1-phenylethyl]acetamide',
                                     'reason': 'No cytidine moiety found'},
                                 {   'smiles': 'C[N+](C)(C)[C@@H](Cc1c[nH]c(n1)S(=O)C[C@H](NC(=O)CC[C@H]([NH3+])C([O-])=O)C([O-])=O)C([O-])=O',
                                     'name': 'N(alpha)-(L-gamma-glutamyl)-hercynyl-L-cysteine '
                                             'sulfoxide(1-)',
                                     'reason': 'No cytidine moiety found'},
                                 {   'smiles': 'O(C1=CC=2[C@]3([C@](N(CC3)C)(N(C2C=C1)C)[H])C)C(=O)N4CCC=5C(C4)=CC=CC5',
                                     'name': 'quilostigmine',
                                     'reason': 'No cytidine moiety found'},
                                 {   'smiles': 'O[C@@H]1[C@]23[C@@]4(N(C[C@@]([C@]2(C[C@@]4([C@]56[C@]3(CC(=O)[C@](C5)(C([C@H]6O)=C)[H])[H])[H])[H])(CC1)C)CC)[H]',
                                     'name': 'Bullatine G',
                                     'reason': 'No cytidine moiety found'},
                                 {   'smiles': 'NC1=NC=NC2=C1N=CN2[C@@H]3O[C@H](COP(=O)(O)O)[C@@H](OC(=O)[C@@H](N)CCC(O)=O)[C@H]3O',
                                     'name': "3'-L-glutamyl-AMP",
                                     'reason': 'No cytidine moiety found'},
                                 {   'smiles': 'O1C2(C(C3(C(C4(C(CC3OC(=O)C)C(OC(=O)CC4)(C)C)C)CC2)C)CC15C6N(C=7C5=CC=CC7)C(=O)C(N6)C)C',
                                     'name': 'Teraspiridole C_130091',
                                     'reason': 'No cytidine moiety found'},
                                 {   'smiles': 'O(C1[C@@H](OC(=O)C)C(O[C@@H](OC2=C(OC3=C(C2=O)C(O)=CC(O[C@@H]4OC([C@@H](O)[C@H](O)C4O)CO)=C3CC=C(C)C)C5=CC=C(OC)C=C5)[C@H]1O)C)[C@@H]6OC[C@@H](O)[C@H](OC(=O)C)C6O',
                                     'name': 'Sempervirenoside A',
                                     'reason': 'No cytidine moiety found'},
                                 {   'smiles': 'COC[C@]1(C(=O)C2CCN1CC2)CO',
                                     'name': '(2S)-2-(hydroxymethyl)-2-(methoxymethyl)-1-azabicyclo[2.2.2]octan-3-one',
                                     'reason': 'No cytidine moiety found'},
                                 {   'smiles': 'Oc1c(C2CC(Cc3ccccc23)c2ccc(OCc3ccc(cc3)C(F)(F)F)cc2)c(=O)oc2ccccc12',
                                     'name': 'Flocoumafen',
                                     'reason': 'No cytidine moiety found'},
                                 {   'smiles': 'O[C@H]1CC=2C(N(C=3C1=CC=CC3)C(=O)N)=CC=CC2',
                                     'name': '(S)-MHD',
                                     'reason': 'No cytidine moiety found'}],
    'sample_false_negatives': [],
    'attempt': 2,
    'reasoning': 'Let me analyze the previous attempt and propose '
                 'improvements:\n'
                 '\n'
                 '1. Pattern Matching Issues:\n'
                 '- The main issue seems to be with the ribose sugar pattern '
                 'matching. All false negatives were marked with "No ribose '
                 'sugar found or not correctly connected to cytosine"\n'
                 '- The SMARTS patterns for the ribose-cytosine connection may '
                 'be too specific or rigid\n'
                 '- We should consider alternative conformations and '
                 'stereochemistry\n'
                 '\n'
                 '2. Structural Requirements:\n'
                 '- CDP-diacylglycerol has these key components:\n'
                 '  * Cytidine (cytosine + ribose)\n'
                 '  * Diphosphate bridge\n'
                 '  * Glycerol backbone\n'
                 '  * Two fatty acid chains\n'
                 '- We need to make the patterns more flexible while '
                 'maintaining specificity\n'
                 '\n'
                 "Here's my improved version:",
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 40,
    'num_false_positives': 8,
    'num_true_negatives': 142252,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.8333333333333334,
    'recall': 1.0,
    'f1': 0.9090909090909091,
    'accuracy': 0.9999437807449051,
    'negative_predictive_value': 1.0}