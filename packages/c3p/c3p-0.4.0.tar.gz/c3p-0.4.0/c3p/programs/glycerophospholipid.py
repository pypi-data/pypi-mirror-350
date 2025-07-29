"""
Classifies: CHEBI:37739 glycerophospholipid
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_glycerophospholipid(smiles: str):
    """
    Determines if a molecule is a glycerophospholipid based on its SMILES string.
    A glycerophospholipid is defined as having a glycerol backbone with a phosphate group 
    ester-linked to a terminal carbon of the glycerol backbone.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a glycerophospholipid, False otherwise
        str: Reason for classification
    """
    
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
    
    # Look for glycerol backbone pattern (C-C-C)
    glycerol_pattern = Chem.MolFromSmarts("[CH2X4][CHX4][CH2X4]")
    if not mol.HasSubstructMatch(glycerol_pattern):
        return False, "No glycerol backbone found"

    # Check for phosphate group pattern (P=O(OH)2 or variants with ester linkages)
    phosphate_pattern = Chem.MolFromSmarts("P(=O)(O)(O)")
    if not mol.HasSubstructMatch(phosphate_pattern):
        return False, "No phosphate group found"
    
    # Ensure the phosphate is linked to a terminal carbon of the glycerol backbone
    glycerol_atoms = mol.GetSubstructMatch(glycerol_pattern)
    phosphate_atoms = mol.GetSubstructMatch(phosphate_pattern)

    for glycerol_atom in [glycerol_atoms[0], glycerol_atoms[2]]:  # Check both terminal carbons
        for phosphate_atom in phosphate_atoms:
            if mol.GetBondBetweenAtoms(glycerol_atom, phosphate_atom) is not None:
                # We found a glycerol-phosphate link
                return True, "Contains glycerol backbone with phosphate group attached"
    
    return False, "Phosphate group not ester-linked to glycerol terminal carbon"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:37739',
                          'name': 'glycerophospholipid',
                          'definition': 'Any glycerolipid having a phosphate '
                                        'group ester-linked to a terminal '
                                        'carbon of the glycerol backbone.',
                          'parents': ['CHEBI:16247', 'CHEBI:35741'],
                          'xrefs': ['PMID:17393491'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 31,
                           'log_lines_of_code': 3.4339872044851463,
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
                                                 1,
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
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 0,
                                                 1,
                                                 2,
                                                 3,
                                                 4,
                                                 4,
                                                 1,
                                                 1],
                           'max_indent': 4,
                           'imports': [   'from rdkit import Chem',
                                          'from rdkit.Chem import AllChem'],
                           'imports_count': 2,
                           'methods_called': [   'GetSubstructMatch',
                                                 'HasSubstructMatch',
                                                 'GetBondBetweenAtoms',
                                                 'MolFromSmiles',
                                                 'MolFromSmarts'],
                           'methods_called_count': 5,
                           'smarts_strings': [   '[CH2X4][CHX4][CH2X4]',
                                                 'P(=O)(O)(O)'],
                           'smarts_strings_count': 2,
                           'defs': ['is_glycerophospholipid(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "No glycerol backbone found"',
                                          'False, "No phosphate group found"',
                                          'True, "Contains glycerol backbone '
                                          'with phosphate group attached"',
                                          'False, "Phosphate group not '
                                          'ester-linked to glycerol terminal '
                                          'carbon"'],
                           'returns_count': 5,
                           'complexity': 3.686797440897029},
    'message': None,
    'sample_true_negatives': [   {   'smiles': '[H][C@@]1(O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O)O[C@@H]1[C@@H](O)[C@@H](O)[C@@H](CO)O[C@H]1OC[C@H]1O[C@@H](OC[C@H]2O[C@@H](OC[C@H](NC(=O)[C@H](O)CCCCCCCCCCCCCCCCCCCCCC)[C@H](O)[C@H](O)CCCCCCCCCCCCCC)[C@H](O)[C@@H](O)[C@H]2O)[C@H](O)[C@@H](O)[C@H]1O',
                                     'name': 'Neurosporaside',
                                     'reason': 'No glycerol backbone found'},
                                 {   'smiles': '[O-]C(=O)C1=CN(C2CC2)C2=CC(N3CC[NH2+]CC3)=C(F)C=C2C1=O',
                                     'name': 'ciprofloxacin zwitterion',
                                     'reason': 'No phosphate group found'},
                                 {   'smiles': 'O=C1NC(=CC2=C1O[C@H]([C@@H](O)CC(C)C)O2)C',
                                     'name': 'Dihydroisoflavipucine',
                                     'reason': 'No glycerol backbone found'},
                                 {   'smiles': 'O=C1N2C(C(=O)N([C@@]2(OC)C)C[C@@H](O)C3=CC=CC=C3)=CC4=C1N(C=5C=CC=CC45)C',
                                     'name': 'Marinacarboline K',
                                     'reason': 'No glycerol backbone found'},
                                 {   'smiles': 'O1[C@@H](O[C@H]2[C@@H](O)[C@H](O)[C@H](O[C@@H]2OC[C@H]3OC(O)[C@@H](O)[C@@H](O)[C@@H]3O)CO)[C@H](NC(=O)C)[C@@H](O)[C@H](O[C@@H]4O[C@@H]([C@H](O)[C@H](O)[C@H]4O)CO[C@]5(O[C@H]([C@H](NC(=O)C)[C@@H](O)C5)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]1CO',
                                     'name': '(2R,4S,5R,6R)-5-Acetamido-2-[[(2R,3R,4S,5R,6S)-6-[(2R,3S,4R,5R,6S)-5-acetamido-6-[(2S,3S,4S,5S,6R)-4,5-dihydroxy-6-(hydroxymethyl)-2-[[(2R,3S,4S,5S)-3,4,5,6-tetrahydroxyoxan-2-yl]methoxy]oxan-3-yl]oxy-4-hydroxy-2-(hydroxymethyl)oxan-3-yl]oxy-3,4,5-trihydroxyoxan-2-yl]methoxy]-4-hydroxy-6-[(1R,2R)-1,2,3-trihydroxypropyl]oxane-2-carboxylic '
                                             'acid',
                                     'reason': 'No glycerol backbone found'},
                                 {   'smiles': 'O(C(=O)CCCCCCC)CCC1=CC=CC=C1',
                                     'name': '2-Phenylethyl octanoate',
                                     'reason': 'No glycerol backbone found'},
                                 {   'smiles': 'O=C1C2=C(OC=3C1=CC=CN3)C(Cl)=CC(=C2)C=4NN=NN4',
                                     'name': 'traxanox',
                                     'reason': 'No glycerol backbone found'},
                                 {   'smiles': 'CCCCC(C)CCCCCC(C)CCCCCCCCCC(C)CC(O)=O',
                                     'name': '3,13,19-trimethyltricosanoic '
                                             'acid',
                                     'reason': 'No phosphate group found'},
                                 {   'smiles': 'COC(CC1=CC[C@]2(C)[C@@H](C)CCC[C@]2(C)C1=O)OC',
                                     'name': 'aignopsane ketal',
                                     'reason': 'No glycerol backbone found'},
                                 {   'smiles': 'OC(C=C)(CC/C=C(/CC/C=C(/CCCC(O)(CCCC(O)(CCCC(O)(CCCC(O)(CCCC(O)(CCC=C(C)C)C)C)C)C)C)\\C)\\C)C',
                                     'name': 'Hypsiziprenol-B9',
                                     'reason': 'No glycerol backbone found'}],
    'sample_false_negatives': [   {   'smiles': 'C([C@](COP(O)(=O)OC[C@@](CO/C=C\\CCCCCCCCCCCCCC)(OC(=O)CCCCCCCCCCCCCCCCCC)[H])(N)[H])(=O)O',
                                      'name': 'PS(P-16:0/19:0)',
                                      'reason': 'Phosphate group not '
                                                'ester-linked to glycerol '
                                                'terminal carbon'},
                                  {   'smiles': 'C(C[N+](C)(C)C)OP(=O)([O-])OC[C@H](OC(CCCCCCCCC/C=C\\C/C=C\\C/C=C\\CC)=O)COC(CCCCCCCCCCCCCCC)=O',
                                      'name': '1-hexadecanoyl-2-[(11Z,14Z,17Z)-icosatrienoyl]-sn-glycero-3-phosphocholine',
                                      'reason': 'Phosphate group not '
                                                'ester-linked to glycerol '
                                                'terminal carbon'},
                                  {   'smiles': 'CC\\C=C/C\\C=C/C\\C=C/C\\C=C/C\\C=C/C\\C=C/CCC(=O)NCCOP(O)(=O)OC[C@H](O)CO',
                                      'name': 'N-(4Z,7Z,10Z,13Z,16Z,19Z)-docosahexaenoyl-sn-glycero-3-phosphoethanolamine',
                                      'reason': 'Phosphate group not '
                                                'ester-linked to glycerol '
                                                'terminal carbon'},
                                  {   'smiles': 'C(CN)OP(=O)(O)OC[C@H](OC(CCCCCCCCCCCCCC)=O)COC(=O)CCCCCCCCCCCCCCCCCCCCC',
                                      'name': '1-docosanoyl-2-pentadecanoyl-sn-glycero-3-phosphoethanolamine',
                                      'reason': 'Phosphate group not '
                                                'ester-linked to glycerol '
                                                'terminal carbon'},
                                  {   'smiles': 'C(C[N+](C)(C)C)OP(=O)([O-])OC[C@H](O)COC(CCCCC/C=C\\C/C=C\\C/C=C\\C/C=C\\CCCCC)=O',
                                      'name': '1-[(7Z,10Z,13Z,16Z)-docosatetraenoyl]-sn-glycero-3-phosphocholine',
                                      'reason': 'Phosphate group not '
                                                'ester-linked to glycerol '
                                                'terminal carbon'},
                                  {   'smiles': 'P(OC[C@H]1O[C@@H](N2C=CC(=NC2=O)N)[C@H](O)[C@@H]1O)(OP(OC[C@H](OC(=O)CCCCCCCC3OC3C/C=C\\CCCCC)COC(=O)CCCCCCCCC(C)C)(O)=O)(O)=O',
                                      'name': 'CDP-DG(i-12:0/18:1(12Z)-O(9S,10R))',
                                      'reason': 'Phosphate group not '
                                                'ester-linked to glycerol '
                                                'terminal carbon'},
                                  {   'smiles': 'P1(O[C@H]2[C@H](O)[C@@H](O)[C@H](O)[C@H]([C@@H](O)C[C@@H](O)[C@@H]([C@@H](O)[C@H]2OP(O)(O)=O)/C=C/[C@@H](O)CCCCC)CCCCCCC(OC[C@@H](OC(=O)CCCCCCCCCCCCCCCCC)CO1)=O)(O)=O',
                                      'name': 'PIP(PGF1alpha/18:0)',
                                      'reason': 'Phosphate group not '
                                                'ester-linked to glycerol '
                                                'terminal carbon'},
                                  {   'smiles': 'P(OC[C@H]1O[C@@H](N2C=CC(=NC2=O)N)C(O)[C@H]1O)(OP(OC[C@H](OC(=O)CCCCCCCCCCCCCC(C)C)COC(=O)CCCCCCCCC(C)C)(O)=O)(O)=O',
                                      'name': 'CDP-DG(i-12:0/i-17:0)',
                                      'reason': 'Phosphate group not '
                                                'ester-linked to glycerol '
                                                'terminal carbon'},
                                  {   'smiles': 'O[C@@H]1C/C(=C\\C=C\\2/[C@]3([C@@]([C@](CC3)([C@H](C)C=C[C@@H](C(C)C)C)[H])(CCC2)C)[H])/C([C@@H](O)C1)=C',
                                      'name': '1-octadecyl lysophosphatidic '
                                              'acid',
                                      'reason': 'No phosphate group found'},
                                  {   'smiles': 'P(=O)(O)(OCCN)OC[C@@H](CO)OC(CCC/C=C\\C[C@H]1[C@@H]2C[C@H]([C@@H]1/C=C/[C@H](CCCCC)O)OO2)=O',
                                      'name': '2-[(9S,11R)-epidioxy-(15S)-hydroxy-(5Z,13E)-prostadienoyl]-sn-glycero-3-phosphoethanolamine',
                                      'reason': 'Phosphate group not '
                                                'ester-linked to glycerol '
                                                'terminal carbon'}],
    'attempt': 0,
    'reasoning': 'To classify a molecule as a member of the '
                 'glycerophospholipid class based on its SMILES string, we '
                 'need to identify if the molecule has a glycerol backbone '
                 'with a phosphate group ester-linked to a terminal carbon. '
                 'Glycerophospholipids typically also have two fatty acid '
                 'chains, attached via ester links, on the other carbons of '
                 'the glycerol backbone.\n'
                 '\n'
                 "Here's the plan for the classification function:\n"
                 '\n'
                 '1. **Parse the SMILES string**: Use RDKit to convert the '
                 'SMILES string into a molecule object.\n'
                 '\n'
                 '2. **Check for glycerol backbone**: Identify the pattern for '
                 'a glycerol backbone, which can be represented by C-C-C, '
                 'usually with two ester-linked fatty acid chains.\n'
                 '\n'
                 '3. **Look for a phosphate group**: Check for the presence of '
                 'a phosphate group (P=O with oxygen atoms connected).\n'
                 '\n'
                 '4. **Link phosphate to the glycerol**: Confirm that the '
                 'phosphate group is ester-linked to one of the terminal '
                 'carbons of the glycerol backbone.\n'
                 '\n'
                 '5. **Check for presence of fatty acid chains**: Ensure there '
                 'are other ester linkages that typically represent fatty acid '
                 'chains.\n'
                 '\n'
                 '6. **Validation**: Confirm the characteristic structures '
                 'present meet the criteria of a glycerophospholipid.\n'
                 '\n'
                 "Here's the implementation of the function:",
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 3750,
    'num_false_positives': 502,
    'num_true_negatives': 137923,
    'num_false_negatives': 125,
    'num_negatives': None,
    'precision': 0.8819379115710254,
    'recall': 0.967741935483871,
    'f1': 0.9228497600590623,
    'accuracy': 0.9955938158819395,
    'negative_predictive_value': 0.9990945178488642}