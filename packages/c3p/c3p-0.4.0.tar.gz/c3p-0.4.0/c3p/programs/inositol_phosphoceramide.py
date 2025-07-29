"""
Classifies: CHEBI:60245 inositol phosphoceramide
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_inositol_phosphoceramide(smiles: str):
    """
    Determines if a molecule is an inositol phosphoceramide based on its SMILES string.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is an inositol phosphoceramide, False otherwise
        str: Reason for classification
    """
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for inositol ring (cyclohexane with 6 OH groups)
    # More flexible pattern that matches myo-inositol core
    inositol_pattern = Chem.MolFromSmarts("[OX2][CH]1[CH]([OX2])[CH]([OX2])[CH]([OX2])[CH]([OX2])[CH]1[OX2]")
    if not mol.HasSubstructMatch(inositol_pattern):
        return False, "No inositol ring found"

    # Check for phosphodiester bridge
    # Pattern matches P(=O)(O)(OR)(OR) where R can be C or H
    phosphodiester_pattern = Chem.MolFromSmarts("[OX2][P](=[OX1])([OX2])[OX2]")
    phosphate_matches = len(mol.GetSubstructMatches(phosphodiester_pattern))
    if phosphate_matches == 0:
        return False, "No phosphodiester bridge found"
    if phosphate_matches > 1:
        return False, "Multiple phosphate groups found"

    # Check for ceramide core structure (more flexible pattern)
    # Matches both regular and hydroxylated ceramides
    ceramide_pattern = Chem.MolFromSmarts("[NX3H][CX3](=[OX1])[CX4]")
    if not mol.HasSubstructMatch(ceramide_pattern):
        return False, "No ceramide core structure found"

    # Check for long alkyl chains characteristic of ceramides
    alkyl_chain_pattern = Chem.MolFromSmarts("CCCCCCCC")  # At least 8 carbons in chain
    alkyl_chains = len(mol.GetSubstructMatches(alkyl_chain_pattern))
    if alkyl_chains < 2:
        return False, "Missing long alkyl chains characteristic of ceramides"

    # Check for proper connectivity between components
    # More flexible pattern that captures the essential P-O linkages
    connectivity_pattern = Chem.MolFromSmarts("[CH1]1([OX2][P](=[OX1])([OX2])[OX2]CC[NH])[CH]([OX2])[CH]([OX2])[CH]([OX2])[CH]([OX2])[CH]1[OX2]")
    if not mol.HasSubstructMatch(connectivity_pattern):
        return False, "Missing required connectivity between inositol and ceramide"

    # Count key atoms to verify overall composition
    c_count = sum(1 for atom in mol.GetAtoms() if atom.GetAtomicNum() == 6)
    o_count = sum(1 for atom in mol.GetAtoms() if atom.GetAtomicNum() == 8)
    n_count = sum(1 for atom in mol.GetAtoms() if atom.GetAtomicNum() == 7)
    p_count = sum(1 for atom in mol.GetAtoms() if atom.GetAtomicNum() == 15)

    # Verify basic composition requirements
    if c_count < 20:
        return False, "Carbon count too low for ceramide chains"
    if o_count < 8:  # 6 from inositol, 1 from amide, minimum 1 from phosphate
        return False, "Insufficient oxygen atoms"
    if n_count != 1:
        return False, "Must contain exactly one nitrogen (ceramide)"
    if p_count != 1:
        return False, "Must contain exactly one phosphorus"

    # Check for optional mannose residue
    mannose_pattern = Chem.MolFromSmarts("O[CH]1O[CH](CO)[CH](O)[CH](O)[CH]1O")
    has_mannose = mol.HasSubstructMatch(mannose_pattern)

    base_description = "Contains inositol ring with phosphodiester-linked ceramide"
    if has_mannose:
        return True, f"{base_description} and mannose residue"
    return True, base_description


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:60245',
                          'name': 'inositol phosphoceramide',
                          'definition': 'A phosphosphingolipid in which an '
                                        'inositol residue and the ceramide '
                                        'moiety are linked via a '
                                        'phosphodiester bridge. The ceramide '
                                        'moiety contains substituents R(1) and '
                                        'R(2) which vary with different '
                                        'sphingoid bases and fatty acyl '
                                        'moieties.',
                          'parents': ['CHEBI:35786'],
                          'xrefs': ['PMID:9804825'],
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
               'CCCCCCCCCCCCCCCCCCCCC[C@@H](O)[C@H](O)C(=O)N[C@@H](COP(O)(=O)O[C@H]1[C@H](O)[C@@H](O)[C@H](O)[C@@H](O)[C@H]1O)[C@H](O)[C@H](O)CCCCCCCCCCCCCC '
               'NAME: Ins-1-P-Cer(t18:0/2,3-OH-24:0) REASON: MISSED Incorrect '
               'connectivity between inositol and ceramide\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCCCCCCC(O)C(=O)N[C@@H](COP(O)(=O)O[C@@H]1[C@H](O)[C@H](O)[C@@H](O)[C@H](O)[C@H]1O[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@@H]1O)[C@H](O)C(O)CCCCCCCCCCCCCC '
               'NAME: Man-beta1-6-Ins-1-P-Cer(t18:0/2-OH-24:0) REASON: MISSED '
               'Incorrect connectivity between inositol and ceramide\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCCCCCCC(O)C(=O)N[C@@H](COP(O)(=O)O[C@@H]1[C@H](O)[C@H](O)[C@@H](O)[C@H](O)[C@H]1OC1O[C@H](CO)[C@@H](O)[C@H](O)[C@@H]1O)[C@H](O)C(O)CCCCCCCCCCCCCCCC '
               'NAME: Man-1-6-Ins-1-P-Cer(t20:0/2-OH-24:0) REASON: MISSED '
               'Incorrect connectivity between inositol and ceramide\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCCCCCCCCCC(=O)N[C@@H](COP(O)(=O)O[C@H]1[C@H](O)[C@@H](O)[C@H](O)[C@@H](O)[C@H]1O)[C@H](O)CCCCCCCCCCCCCCC '
               'NAME: Ins-1-P-Cer(d18:0/26:0) REASON: MISSED Incorrect '
               'connectivity between inositol and ceramide\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCCCCCCCC(=O)N[C@@H](COP(O)(=O)O[C@H]1[C@H](O)[C@@H](O)[C@H](O)[C@@H](O)[C@H]1O)[C@H](O)CCCCCCCCCCCCCCC '
               'NAME: Ins-1-P-Cer(d18:0/24:0) REASON: MISSED Incorrect '
               'connectivity between inositol and ceramide\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCCCCCCCCC(O)C(=O)N[C@@H](COP(O)(=O)O[C@@H]1[C@H](O)[C@H](O)[C@@H](O)[C@H](O)[C@H]1OC1O[C@H](CO)[C@@H](O)[C@H](O)[C@@H]1O)[C@H](O)C(O)CCCCCCCCCCCCCC '
               'NAME: Man-1-6-Ins-1-P-Cer(t18:0/2-OH-26:0) REASON: MISSED '
               'Incorrect connectivity between inositol and ceramide\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCCCCCCCCCC(=O)N[C@@H](COP(O)(=O)O[C@@H]1[C@H](O)[C@H](O)[C@@H](O)[C@H](O)[C@H]1OC1O[C@H](CO)[C@@H](O)[C@H](O)[C@@H]1O)[C@H](O)CCCCCCCCCCCCCCC '
               'NAME: Man-1-6-Ins-1-P-Cer(d18:0/26:0) REASON: MISSED Incorrect '
               'connectivity between inositol and ceramide\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCCCCCCCC(=O)N[C@@H](COP(O)(=O)O[C@H]1[C@H](O)[C@@H](O)[C@H](O)[C@@H](O)[C@H]1O)[C@H](O)[C@@H](O)CCCCCCCCCCCCCC '
               'NAME: Ins-1-P-Cer(t18:0/24:0) REASON: MISSED Incorrect '
               'connectivity between inositol and ceramide\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCCCCCCCC(O)C(O)C(=O)N[C@@H](COP(O)(=O)O[C@@H]1[C@H](O)[C@H](O)[C@@H](O)[C@H](O)[C@H]1OC1O[C@H](CO)[C@@H](O)[C@H](O)[C@@H]1O)[C@H](O)C(O)CCCCCCCCCCCCCC '
               'NAME: Man-1-6-Ins-1-P-Cer(t18:0/2,3-OH-26:0) REASON: MISSED '
               'Incorrect connectivity between inositol and ceramide\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCCCCCC(O)C(O)C(=O)N[C@@H](COP(O)(=O)O[C@H]1[C@H](O)[C@@H](O)[C@H](O)[C@@H](O)[C@H]1O)[C@H](O)C(O)CCCCCCCCCCCCCCCC '
               'NAME: Ins-1-P-Cer(t20:0/2,3-OH-24:0) REASON: MISSED Incorrect '
               'connectivity between inositol and ceramide\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'C1C=C(N=C2N1NN=N2)C3=CC=CC=C3',
                                     'name': '5-phenyl-1,7-dihydrotetrazolo[1,5-a]pyrimidine',
                                     'reason': 'No inositol ring found'},
                                 {   'smiles': 'O(C(=O)CCCCCCCCCCC/C=C\\CCCCCCCC)[C@H](COC(=O)CCCCCCCCC/C=C\\CCCCCC)COC(=O)CCCCCCC/C=C\\CCCC',
                                     'name': 'TG(14:1(9Z)/22:1(13Z)/18:1(11Z))',
                                     'reason': 'No inositol ring found'},
                                 {   'smiles': 'CC(=O)N[C@H]1[C@H](O)O[C@H](CO)[C@@H](O[C@@H]2O[C@H](CO)[C@@H](O[C@@H]3O[C@H](CO[C@H]4O[C@H](CO[C@H]5O[C@H](CO)[C@@H](O)[C@H](O)[C@@H]5O)[C@@H](O)[C@H](O[C@H]5O[C@H](CO)[C@@H](O)[C@H](O)[C@@H]5O)[C@@H]4O)[C@@H](O)[C@H](O[C@H]4O[C@H](CO)[C@@H](O)[C@H](O)[C@@H]4O[C@@H]4O[C@H](CO)[C@@H](O)[C@H](O)[C@H]4NC(C)=O)[C@@H]3O)[C@H](O)[C@H]2NC(C)=O)[C@@H]1O',
                                     'name': 'beta-D-GlcpNAc-(1->2)-alpha-D-Manp-(1->3)-{alpha-D-Manp-(1->3)-[alpha-D-Manp-(1->6)]-alpha-D-Manp-(1->6)}-beta-D-Manp-(1->4)-beta-GlcpNAc-(1->4)-beta-D-GlcpNAc',
                                     'reason': 'No inositol ring found'},
                                 {   'smiles': '[C@@]12([C@@]([C@]([C@@H](CC1)C)(CCC(CC)C)C)(CCC[C@@H]2C)[H])C',
                                     'name': 'clerodane',
                                     'reason': 'No inositol ring found'},
                                 {   'smiles': 'S(O[C@@H]1[C@H](O)[C@@H](O)[C@H](O[C@@H]([C@@H](O)[C@H](O)CO[C@]2(O[C@H]([C@H](NC(=O)C)[C@@H](O)C2)[C@H](O)[C@H](O)CO)C(O)=O)[C@@H](NC(=O)C)CO)O[C@@H]1CO)(O)(=O)=O',
                                     'name': '(2R,4S,5R,6R)-5-Acetamido-2-[(2R,3S,4R,5S)-5-acetamido-4-[(2R,3R,4R,5R,6R)-3,4-dihydroxy-6-(hydroxymethyl)-5-sulfooxyoxan-2-yl]oxy-2,3,6-trihydroxyhexoxy]-4-hydroxy-6-[(1R,2R)-1,2,3-trihydroxypropyl]oxane-2-carboxylic '
                                             'acid',
                                     'reason': 'No inositol ring found'},
                                 {   'smiles': 'O=C(NC(CC(C)C)C(=O)N[C@@H](CCCN=C(N)N)C=O)C(NC(=O)CC)CC(C)C',
                                     'name': 'Leupeptin Pr-LL',
                                     'reason': 'No inositol ring found'},
                                 {   'smiles': 'COC1=CC=C(C=C1)CCNC(=O)C(=C2C3=CC=CC=C3C(=N2)NC(=O)C4=CC=CS4)C#N',
                                     'name': 'N-[3-[1-cyano-2-[2-(4-methoxyphenyl)ethylamino]-2-oxoethylidene]-1-isoindolyl]-2-thiophenecarboxamide',
                                     'reason': 'No inositol ring found'},
                                 {   'smiles': 'O=C1O[C@@H](CC=2C1=C(OC)C(O)=CC2)CCC[C@@H](O)C',
                                     'name': 'Penicimarin C',
                                     'reason': 'No inositol ring found'},
                                 {   'smiles': 'CO[C@@H]1[C@@H]2[C@@H](C[C@@H]3[C@@](O2)([C@H]([C@@H]([C@H](O3)C(=O)OC)O)O)O)OC1N4C=NC5=C4N=CN=C5N',
                                     'name': 'LSM-4497',
                                     'reason': 'No inositol ring found'},
                                 {   'smiles': 'C[C@@H]1[C@H](O)CCC2=CC[C@H](C[C@]12C)C(C)=C',
                                     'name': '1-deoxycapsidiol',
                                     'reason': 'No inositol ring found'}],
    'sample_false_negatives': [],
    'attempt': 2,
    'reasoning': 'Let me analyze the previous attempt and suggest '
                 'improvements:\n'
                 '\n'
                 '1. The main issue appears to be with detecting the correct '
                 'connectivity between components. All examples were rejected '
                 'due to "Incorrect connectivity between inositol and '
                 'ceramide", suggesting our connectivity pattern was too '
                 'strict or incorrect.\n'
                 '\n'
                 '2. Looking at the example structures, I notice:\n'
                 '   - They all have an inositol ring with 6 OH groups\n'
                 '   - A phosphodiester bridge connects position 1 of inositol '
                 'to ceramide\n'
                 '   - The ceramide portion has variable chain lengths and '
                 'hydroxylation patterns\n'
                 '   - Some structures have an optional mannose residue\n'
                 '\n'
                 '3. Key improvements needed:\n'
                 '   - More flexible connectivity pattern between inositol and '
                 'ceramide\n'
                 '   - Better handling of stereochemistry\n'
                 '   - More precise detection of the phosphodiester linkage '
                 'position\n'
                 '   - Better handling of variable ceramide structures (t18:0, '
                 'd18:0, etc.)\n'
                 '\n'
                 "Here's my improved solution:",
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 33,
    'num_false_positives': 5,
    'num_true_negatives': 142262,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.868421052631579,
    'recall': 1.0,
    'f1': 0.9295774647887324,
    'accuracy': 0.9999648629655657,
    'negative_predictive_value': 1.0}