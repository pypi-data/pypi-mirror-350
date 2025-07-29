"""
Classifies: CHEBI:57643 1,2-diacyl-sn-glycero-3-phosphocholine
"""
from rdkit import Chem

def is_1_2_diacyl_sn_glycero_3_phosphocholine(smiles: str):
    """
    Determines if a molecule is a 1,2-diacyl-sn-glycero-3-phosphocholine
    based on its SMILES string.
    
    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a 1,2-diacyl-sn-glycero-3-phosphocholine, False otherwise
        str: Reason for classification
    """
    
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
    
    # Look for glycerol backbone pattern (central CH with two O and rest atoms connected)
    glycerol_backbone_pattern = Chem.MolFromSmarts("[C@H](COC(=O)*)OC(=O)*")
    if not mol.HasSubstructMatch(glycerol_backbone_pattern):
        return False, "No glycerol backbone found"
    
    # Look for phosphocholine group: [O-]P(=O)(OCC[N+](C)(C)C)
    phosphocholine_group_pattern = Chem.MolFromSmarts("[O-]P(=O)(OCC[N+](C)(C)C)")
    if not mol.HasSubstructMatch(phosphocholine_group_pattern):
        return False, "No phosphocholine group found"
    
    # Check for negative charge balance
    net_charge = sum([atom.GetFormalCharge() for atom in mol.GetAtoms()])
    if net_charge != 0:
        return False, f"Net charge imbalance: {net_charge} (expected 0)"
    
    # Check the presence of exactly two ester linkages
    ester_linkage_pattern = Chem.MolFromSmarts("COC(=O)")
    ester_matches = mol.GetSubstructMatches(ester_linkage_pattern)
    if len(ester_matches) != 2:
        return False, f"Found {len(ester_matches)} ester groups, need exactly 2"

    return True, "Contains 1,2-diacyl-sn-glycero-3-phosphocholine features"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:57643',
                          'name': '1,2-diacyl-sn-glycero-3-phosphocholine',
                          'definition': 'The conjugate base of a '
                                        '1,2-diacyl-sn-glycero-3-phosphocholine '
                                        'compound formed by deprotonation of '
                                        'the phosphate OH group.',
                          'parents': [   'CHEBI:35284',
                                         'CHEBI:36313',
                                         'CHEBI:64482'],
                          'xrefs': ['LIPID_MAPS_instance:LMGP01010000'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': None,
    'message': None,
    'sample_true_negatives': [   {   'smiles': 'O=C1C2=C(OC(=C1)C)C3=C(OC)C=C(OC)C=C3C(=C2O)C4=C5OC(=CC(C5=C(O)C=6C4=CC(OC)=CC6OC)=O)C',
                                     'name': 'Isonigerone',
                                     'reason': 'No glycerol backbone found'},
                                 {   'smiles': 'CCCCCCCCCCCCCC(=O)OC[C@H](COP([O-])(=O)OC[C@@H](O)CO)OC(=O)CCCCCCC\\C=C/CCCCCCCC',
                                     'name': '1-myristoyl-2-oleoyl-sn-glycero-3-phosphatidylglycerol(1-)',
                                     'reason': 'No phosphocholine group found'},
                                 {   'smiles': 'C(=C\\C/C=C\\CCCC(NC)=O)\\C/C=C\\C/C=C\\CCCCC',
                                     'name': 'N-methyl arachidonoyl amine',
                                     'reason': 'No glycerol backbone found'},
                                 {   'smiles': 'OC1(O)[C@]23N(CC1)C(N(O)[C@H]([C@@]3(N=C(N2)N)[H])CO)=N',
                                     'name': 'Decarbamoylneosaxitoxin',
                                     'reason': 'No glycerol backbone found'},
                                 {   'smiles': 'S([C@H]1N(C(=O)/C(=C\\C2=CC=C(OCC=C(C)C)C=C2)/N(C1=O)C)C)C',
                                     'name': 'Fusaperazine F',
                                     'reason': 'No glycerol backbone found'},
                                 {   'smiles': 'Oc1ccccc1I',
                                     'name': '2-iodophenol',
                                     'reason': 'No glycerol backbone found'},
                                 {   'smiles': 'O=C1N(CC(=O)N[C@H](C(=O)O[C@H]([C@@H](C(NC(C=C1)=C)=O)C)C(CCCCCCCCCCCCCC)C)C(O)C(=O)N)C',
                                     'name': 'Rakicidin H',
                                     'reason': 'No glycerol backbone found'},
                                 {   'smiles': 'O(C1=C(OC)C=C(C2=C(O)C(OC)=C(C3=CC=CC=C3)C=C2OC)C=C1)C/C=C(/CO)\\C',
                                     'name': 'Prenylterphenyllin F',
                                     'reason': 'No glycerol backbone found'},
                                 {   'smiles': 'O1[C@@H]([C@@H](O)[C@H](O[C@@H]2O[C@@H]([C@@H](O)[C@H](O)[C@H]2O)CO)[C@@H](O)[C@@H]1OC[C@H]3O[C@@H](OC[C@H]4O[C@@H](O)[C@H](O)[C@@H](O)[C@@H]4O)[C@H](O)[C@@H](O)[C@@H]3O)CO[C@@H]5O[C@@H]([C@@H](O)[C@H](O[C@@H]6O[C@@H]([C@@H](O)[C@H](O)[C@H]6O)CO)[C@H]5O)CO[C@@H]7O[C@@H]([C@@H](O)[C@H](O)[C@H]7O)CO',
                                     'name': '(2R,3R,4S,5S,6R)-6-[[(2R,3R,4S,5S,6R)-6-[[(2R,3R,4S,5R,6R)-6-[[(2R,3R,4S,5R,6R)-3,5-Dihydroxy-4-[(2R,3R,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-6-[[(2R,3R,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxymethyl]oxan-2-yl]oxymethyl]-3,5-dihydroxy-4-[(2R,3R,4S,5S,6R)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxyoxan-2-yl]oxymethyl]-3,4,5-trihydroxyoxan-2-yl]oxymethyl]oxane-2,3,4,5-tetrol',
                                     'reason': 'No glycerol backbone found'},
                                 {   'smiles': 'O([C@H]1[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]1CO)O[C@H]2[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]2CO[C@@H]3O[C@H]([C@@H](O)[C@@H](O)[C@@H]3O)C)O)[C@@H]4O[C@@H]([C@@H](O)[C@H](O[C@H]5O[C@@H]([C@@H](O)[C@H](O)[C@@H]5O[C@@H]6O[C@@H]([C@@H](O[C@@H]7O[C@@H]([C@H](O)[C@H](O)[C@H]7O)CO)[C@H](O)[C@@H]6NC(=O)C)CO)CO)[C@@H]4O)CO[C@H]8O[C@@H]([C@@H](O)[C@H](O)[C@@H]8O[C@@H]9O[C@@H]([C@@H](O[C@@H]%10O[C@@H]([C@H](O)[C@H](O)[C@H]%10O)CO)[C@H](O)[C@H]9NC(=O)C)CO)CO',
                                     'name': 'Gal2GlcNAc2Man3GlcNAcFucGlcNAc',
                                     'reason': 'No glycerol backbone found'}],
    'sample_false_negatives': [   {   'smiles': 'P(OCC[N+](C)(C)C)(OCC(OC(=O)CCCCCCCCCCCCC=1OC(CCCCC)=CC1C)COC(=O)CCCCCCCCCCC=2OC(=C(C2C)C)CCCCC)(O)=O',
                                      'name': '(3-{[11-(3,4-dimethyl-5-pentylfuran-2-yl)undecanoyl]oxy}-2-{[13-(3-methyl-5-pentylfuran-2-yl)tridecanoyl]oxy}propoxy)[2-(trimethylazaniumyl)ethoxy]phosphinic '
                                              'acid',
                                      'reason': 'No phosphocholine group '
                                                'found'},
                                  {   'smiles': 'P(OCC[N+](C)(C)C)(OCC(OC(=O)CCCCCCCCCCCCC=1OC(=C(C1C)C)CCCCC)COC(=O)CCCCCCCCCCC=2OC(=C(C2C)C)CCCCC)(O)=O',
                                      'name': 'PC(DiMe(11,5)/DiMe(13,5))',
                                      'reason': 'No phosphocholine group '
                                                'found'},
                                  {   'smiles': 'P(OCC[N+](C)(C)C)(OC[C@@H](OC(=O)CCCCC)COC(=O)CCCCC)(O)=O',
                                      'name': '2-[2,3-Di(hexanoyloxy)propoxy-hydroxyphosphoryl]oxyethyl-trimethylazanium',
                                      'reason': 'No phosphocholine group '
                                                'found'},
                                  {   'smiles': 'P(OCC[N+](C)(C)C)(OCC(OC(=O)CCCCCCCCCCCCC=1OC(=C(C1C)C)CCCCC)COC(=O)CCCCCCCCCCCCC=2OC(CCCCC)=CC2C)(O)=O',
                                      'name': 'PC(MonoMe(13,5)/DiMe(13,5))',
                                      'reason': 'No phosphocholine group '
                                                'found'},
                                  {   'smiles': 'P(OC[C@H](OC(=O)CC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)COC(=O)CCCCCCCCC/C=C\\C/C=C\\CCCCC)(O)(O)=O',
                                      'name': 'PA(20:2(11Z,14Z)/22:6(4Z,7Z,10Z,13Z,16Z,19Z))',
                                      'reason': 'No phosphocholine group '
                                                'found'},
                                  {   'smiles': 'P(OCC[N+](C)(C)C)(OC[C@H](OC(=O)CCCCCCCC(O)=O)COC(=O)CCCCCCCCCCCCCCC)(O)=O',
                                      'name': '1-palmitoyl-2-azelaoylphosphatidylcholine',
                                      'reason': 'No phosphocholine group '
                                                'found'},
                                  {   'smiles': 'P(OCC[N+](C)(C)C)(OCC(OC(=O)CCCCCCCCCCC=1OC(CCCCC)=CC1C)COC(=O)CCCCCCCCCCCCC=2OC(=C(C2C)C)CCCCC)(O)=O',
                                      'name': '(3-{[13-(3,4-dimethyl-5-pentylfuran-2-yl)tridecanoyl]oxy}-2-{[11-(3-methyl-5-pentylfuran-2-yl)undecanoyl]oxy}propoxy)[2-(trimethylazaniumyl)ethoxy]phosphinic '
                                              'acid',
                                      'reason': 'No phosphocholine group '
                                                'found'},
                                  {   'smiles': 'CCCCCCCCCCCCCCCC(=O)OCC(COP(O)(=O)CC[N+](C)(C)C)OC(=O)CCCCCCC\\C=C/CCCCCCCC',
                                      'name': '1-hexadecanoyl-2-[(Z)-octadec-9-enoyl]-sn-glycerol '
                                              '3-(2-trimethylaminoethylphosphonate)',
                                      'reason': 'No phosphocholine group '
                                                'found'},
                                  {   'smiles': 'P(OCC[N+](C)(C)C)(OCC(OC(=O)CCCCCCCCCCC=1OC(=CC1C)CCC)COC(=O)CCCCCCCCCCC=2OC(=C(C2C)C)CCCCC)(O)=O',
                                      'name': 'PC(DiMe(11,5)/MonoMe(11,3))',
                                      'reason': 'No phosphocholine group '
                                                'found'},
                                  {   'smiles': 'P(OCC[N+](C)(C)C)(OCC(OC(=O)CCCCCCCCC=1OC(=C(C1C)C)CCC)COC(=O)CCCCCCCCC=2OC(=C(C2C)C)CCCCC)(O)=O',
                                      'name': '(3-{[9-(3,4-dimethyl-5-pentylfuran-2-yl)nonanoyl]oxy}-2-{[9-(3,4-dimethyl-5-propylfuran-2-yl)nonanoyl]oxy}propoxy)[2-(trimethylazaniumyl)ethoxy]phosphinic '
                                              'acid',
                                      'reason': 'No phosphocholine group '
                                                'found'}],
    'attempt': 0,
    'reasoning': 'To classify the chemical entity '
                 "'1,2-diacyl-sn-glycero-3-phosphocholine', we'll write a "
                 'Python function `is_1_2_diacyl_sn_glycero_3_phosphocholine` '
                 'that will use RDKit to parse and analyze the SMILES string '
                 'to determine if it matches the desired chemical class. This '
                 'class of molecules has some characteristic features:\n'
                 '\n'
                 '1. **Glycerol Backbone:** The structure should contain a '
                 'glycerol backbone with two acyl chains resulting in two '
                 'ester groups.\n'
                 '2. **Phosphocholine Group:** There should be a '
                 'phosphocholine group attached to the third carbon of '
                 'glycerol. This includes a phosphate linked to a choline '
                 'group (trimethylazaniumyl ethoxy group).\n'
                 '3. **Negative Charge:** The conjugate base form means that '
                 'the phosphate is likely deprotonated, carrying a -1 charge.\n'
                 '\n'
                 "Let's go through the steps:\n"
                 '\n'
                 '- Ensure the SMILES string is valid.\n'
                 '- Define SMARTS patterns for glycerol backbone, ester '
                 'groups, and phosphocholine head group.\n'
                 '- Check the presence and correct number of these '
                 'substructures.\n'
                 '- Verify charges to match the conjugate base form.\n'
                 '\n'
                 'The function should return `True` if the molecule matches '
                 'all these checks, otherwise `False` with a reason for the '
                 'failure.\n'
                 '\n'
                 "Here's how the code block will look.",
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 613,
    'num_false_positives': 13,
    'num_true_negatives': 141663,
    'num_false_negatives': 11,
    'num_negatives': None,
    'precision': 0.9792332268370607,
    'recall': 0.9823717948717948,
    'f1': 0.9807999999999999,
    'accuracy': 0.9998313422347154,
    'negative_predictive_value': 0.9999223569603456}