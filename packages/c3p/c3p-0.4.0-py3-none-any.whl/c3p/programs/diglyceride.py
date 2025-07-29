"""
Classifies: CHEBI:18035 diglyceride
"""
"""
Classifies: CHEBI:17855 diglyceride
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_diglyceride(smiles: str):
    """
    Determines if a molecule is a diglyceride based on its SMILES string.
    A diglyceride has a glycerol backbone with two fatty acid chains via ester bonds,
    and the third hydroxyl group is either free or substituted with an alkyl group.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a diglyceride, False otherwise
        str: Reason for classification
    """
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for glycerol backbone (three carbons in a row with appropriate bonds)
    glycerol_pattern = Chem.MolFromSmarts("[CH2X4][CHX4][CH2X4]")
    if not mol.HasSubstructMatch(glycerol_pattern):
        return False, "No glycerol backbone found"

    # Check exactly two ester groups attached to the glycerol backbone
    ester_attached_pattern = Chem.MolFromSmarts("[CH2X4,CHX4]-[OX2]-[CX3]=[OX1]")
    ester_attached_matches = mol.GetSubstructMatches(ester_attached_pattern)
    if len(ester_attached_matches) != 2:
        return False, f"Found {len(ester_attached_matches)} ester groups attached to glycerol, need exactly 2"

    # Find the third oxygen in the glycerol (not part of ester groups)
    glycerol_matches = mol.GetSubstructMatches(glycerol_pattern)
    backbone_indices = glycerol_matches[0]  # Take first match
    backbone_carbons = [mol.GetAtomWithIdx(idx) for idx in backbone_indices]

    # Collect all oxygens attached to the backbone carbons
    glycerol_oxygens = []
    for carbon in backbone_carbons:
        for neighbor in carbon.GetNeighbors():
            if neighbor.GetAtomicNum() == 8:
                glycerol_oxygens.append(neighbor)

    # Get oxygen indices from ester groups (match[1] is the ester oxygen in our SMARTS pattern)
    ester_oxygen_indices = {match[1] for match in ester_attached_matches}
    
    # Identify the third oxygen not part of the ester groups
    third_oxygens = [o for o in glycerol_oxygens if o.GetIdx() not in ester_oxygen_indices]
    if len(third_oxygens) != 1:
        return False, "Could not identify third oxygen in glycerol"
    third_oxygen = third_oxygens[0]

    # Check third oxygen is either -OH or O-alkyl
    if third_oxygen.GetDegree() == 1:
        pass  # Valid -OH
    elif third_oxygen.GetDegree() == 2:
        # Check if connected to a carbon (alkyl group)
        other_neighbors = [n for n in third_oxygen.GetNeighbors() if n not in backbone_carbons]
        if not other_neighbors or other_neighbors[0].GetAtomicNum() != 6:
            return False, "Third oxygen is O-alkyl but not connected to carbon"
    else:
        return False, "Third oxygen has invalid bonding"

    # Check oxygen count (3 from glycerol + 2 from ester carbonyls)
    o_count = sum(1 for atom in mol.GetAtoms() if atom.GetAtomicNum() == 8)
    if o_count != 5:
        return False, f"Expected 5 oxygens, found {o_count}"

    # Check molecular weight (typical diglycerides >300 Da)
    mol_wt = rdMolDescriptors.CalcExactMolWt(mol)
    if mol_wt < 300:
        return False, f"Molecular weight too low ({mol_wt:.1f} < 300)"

    # Check carbon count (at least 15)
    c_count = sum(1 for atom in mol.GetAtoms() if atom.GetAtomicNum() == 6)
    if c_count < 15:
        return False, f"Too few carbons ({c_count})"

    # Check rotatable bonds (indicates chain length)
    n_rotatable = rdMolDescriptors.CalcNumRotatableBonds(mol)
    if n_rotatable < 4:
        return False, f"Too few rotatable bonds ({n_rotatable})"

    return True, "Contains glycerol backbone with two ester-linked fatty acids and one hydroxyl/O-alkyl group"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:18035',
                          'name': 'diglyceride',
                          'definition': 'A glyceride that is glycerol in which '
                                        'any two of the hydroxy groups have '
                                        'been acylated. In the structure '
                                        'shown, two of the R groups (positions '
                                        'not specified) are acyl groups while '
                                        'the remaining R group can be either H '
                                        'or an alkyl group.',
                          'parents': ['CHEBI:47778', 'CHEBI:76578'],
                          'xrefs': ['KEGG:C00165', 'LIPID_MAPS_class:LMGL0201'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 67,
                           'log_lines_of_code': 4.204692619390966,
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
                                                 2,
                                                 0,
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
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 3,
                                                 4,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 1,
                                                 0,
                                                 1,
                                                 1,
                                                 2,
                                                 1,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 1,
                                                 2,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 0,
                                                 1],
                           'max_indent': 4,
                           'imports': [   'from rdkit import Chem',
                                          'from rdkit.Chem import AllChem',
                                          'from rdkit.Chem import '
                                          'rdMolDescriptors'],
                           'imports_count': 3,
                           'methods_called': [   'CalcNumRotatableBonds',
                                                 'HasSubstructMatch',
                                                 'GetAtoms',
                                                 'MolFromSmarts',
                                                 'GetSubstructMatches',
                                                 'GetNeighbors',
                                                 'GetDegree',
                                                 'GetAtomWithIdx',
                                                 'GetIdx',
                                                 'MolFromSmiles',
                                                 'CalcExactMolWt',
                                                 'append',
                                                 'GetAtomicNum'],
                           'methods_called_count': 13,
                           'smarts_strings': [   '[CH2X4,CHX4]-[OX2]-[CX3]=[OX1]',
                                                 '[CH2X4][CHX4][CH2X4]'],
                           'smarts_strings_count': 2,
                           'defs': ['is_diglyceride(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "No glycerol backbone found"',
                                          'False, f"Found '
                                          '{len(ester_attached_matches)} ester '
                                          'groups attached to glycerol, need '
                                          'exactly 2"',
                                          'False, "Could not identify third '
                                          'oxygen in glycerol"',
                                          'False, "Third oxygen is O-alkyl but '
                                          'not connected to carbon"',
                                          'False, "Third oxygen has invalid '
                                          'bonding"',
                                          'False, f"Expected 5 oxygens, found '
                                          '{o_count}"',
                                          'False, f"Molecular weight too low '
                                          '({mol_wt:.1f} < 300)"',
                                          'False, f"Too few carbons '
                                          '({c_count})"',
                                          'False, f"Too few rotatable bonds '
                                          '({n_rotatable})"',
                                          'True, "Contains glycerol backbone '
                                          'with two ester-linked fatty acids '
                                          'and one hydroxyl/O-alkyl group"'],
                           'returns_count': 11,
                           'complexity': 6.6409385238781935},
    'message': '\n'
               "Error: 'int' object has no attribute 'GetAtomicNum'\n"
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
    'sample_true_negatives': [   {   'smiles': '[C@](C1=CN=CN=C1)(O)(C=2C=CC=CC2)C=3C=CC(=CC3Cl)Cl',
                                     'name': '(R)-triarimol',
                                     'reason': 'No glycerol backbone found'},
                                 {   'smiles': 'C[C@H]1CN(C(=O)CCCN2C=C(CO[C@H]1CN(C)CC3=C4C(=CC=C3)OCCCO4)N=N2)[C@@H](C)CO',
                                     'name': '(8S,9R)-9-[[3,4-dihydro-2H-1,5-benzodioxepin-6-ylmethyl(methyl)amino]methyl]-6-[(2S)-1-hydroxypropan-2-yl]-8-methyl-10-oxa-1,6,13,14-tetrazabicyclo[10.2.1]pentadeca-12(15),13-dien-5-one',
                                     'reason': 'No glycerol backbone found'},
                                 {   'smiles': 'NCC[C@@H](O)CNCCCC[C@H](N)C([O-])=O',
                                     'name': 'hypusinate',
                                     'reason': 'Found 0 ester groups attached '
                                               'to glycerol, need exactly 2'},
                                 {   'smiles': 'O=C(NCCC(=O)O)[C@@H](N(C1=CC=C(C=2C1=NON2)[N+]([O-])=O)C)CC(=O)O',
                                     'name': 'NBD-N(Me)-DbetaA-OH',
                                     'reason': 'No glycerol backbone found'},
                                 {   'smiles': 'S1C(C=2SC(=CC2)C#CC)=CC=C1C#C/C=C/C=C',
                                     'name': "(E)-5-(hexa-3,5-dien-1-yn-1-yl)-5'-(prop-1-yn-1-yl)-2,2'-bithiophene",
                                     'reason': 'No glycerol backbone found'},
                                 {   'smiles': 'C(CCCCCCCC)CCCCC(N[C@H](C(=O)N[C@H](C(N[C@H](C(N[C@H](C(N[C@H](C(=O)N[C@H](C(=O)O)CCCCN)CCCCN)=O)CCCCN)=O)CCCCN)=O)CO)CSCC(OC(=O)CCCCCCCCCCCCCCC)COC(=O)CCCCCCCCCCCCCCC)=O',
                                     'name': 'N-palmitoyl-S-[2,3-bis(palmitoyloxy)propyl]-Cys-Ser-Lys-Lys-Lys-Lys',
                                     'reason': 'Could not identify third '
                                               'oxygen in glycerol'},
                                 {   'smiles': 'C[C@@H]1CN(S(=O)(=O)C2=C(C=C(C=C2)C#C[C@@H](C)O)O[C@H]1CN(C)CC3=CC=C(C=C3)C4=CC=CC=C4)[C@H](C)CO',
                                     'name': '(2R)-4-[(4R,5R)-2-[(2R)-1-hydroxypropan-2-yl]-4-methyl-5-[[methyl-[(4-phenylphenyl)methyl]amino]methyl]-1,1-dioxo-4,5-dihydro-3H-6,1$l^{6},2-benzoxathiazocin-8-yl]-3-butyn-2-ol',
                                     'reason': 'No glycerol backbone found'},
                                 {   'smiles': 'Cl.OC(=O)CCCCCN1CCN(CC1)C2=CC=CC=C2',
                                     'name': '6-(4-phenylpiperazino)hexanoic '
                                             'acid hydrochloride',
                                     'reason': 'No glycerol backbone found'},
                                 {   'smiles': '[C@]12(CC[C@H]([C@@]3(C([C@@]1(C2(C)C)[H])(C(CC3)C)O)[H])C)[H]',
                                     'name': '5-hydroxy-alpha-gurjunene',
                                     'reason': 'No glycerol backbone found'},
                                 {   'smiles': 'OC(=O)[C@H](CS(O)(=O)=O)OP(O)(O)=O',
                                     'name': '(2R)-O-phospho-3-sulfolactic '
                                             'acid',
                                     'reason': 'No glycerol backbone found'}],
    'sample_false_negatives': [   {   'smiles': 'O(C(=O)CCCCC)[C@@H](CO)COC(=O)CCCCC',
                                      'name': '1,2-dihexanoyl-sn-glycerol',
                                      'reason': 'Molecular weight too low '
                                                '(288.2 < 300)'},
                                  {   'smiles': 'CCCCCCCCCCCCCCCCOC[C@H](CO)OC(=O)CCC\\C=C/C\\C=C/C\\C=C/C\\C=C/CCCCC',
                                      'name': '1-palmityl-2-arachidonoyl-sn-glycerol',
                                      'reason': 'Found 1 ester groups attached '
                                                'to glycerol, need exactly 2'},
                                  {   'smiles': 'P(OCC[N+](C)(C)C)(OCC(O/C=C\\CCCCCCCCCCCCCC)COC(=O)CCCCCCCCCCCCC)([O-])=O',
                                      'name': 'PC(14:0/P-16:0)',
                                      'reason': 'Found 1 ester groups attached '
                                                'to glycerol, need exactly 2'},
                                  {   'smiles': 'O(C(=O)CCCCCCCCC(CC)C)[C@H](COC(=O)CCCCCCC)CO',
                                      'name': 'DG(8:0/a-13:0/0:0)',
                                      'reason': 'Could not identify third '
                                                'oxygen in glycerol'},
                                  {   'smiles': 'CCCCCCCCCCCCCCCCOC[C@H](COP([O-])([O-])=O)OC(=O)CCCCCCC\\C=C/CCCCCCCC',
                                      'name': '1-palmityl-2-oleoyl-sn-glycero-3-phosphate(2-)',
                                      'reason': 'Found 1 ester groups attached '
                                                'to glycerol, need exactly 2'},
                                  {   'smiles': 'P(OCC[N+](C)(C)C)(OCC(O/C=C\\CCCCCCCCCCCCCC)COC(=O)CCCCCCCCCCCCCC)([O-])=O',
                                      'name': 'PC(15:0/P-16:0)',
                                      'reason': 'Found 1 ester groups attached '
                                                'to glycerol, need exactly 2'},
                                  {   'smiles': 'P(OCC[N+](C)(C)C)(OCC(O/C=C\\CCCCCCCCCCCCCCCC)COC(=O)CCCCC/C=C\\C/C=C\\C/C=C\\C/C=C\\CCCCC)([O-])=O',
                                      'name': 'PC(22:4(7Z,10Z,13Z,16Z)/P-18:0)',
                                      'reason': 'Found 1 ester groups attached '
                                                'to glycerol, need exactly 2'},
                                  {   'smiles': 'O(CCC([N+](C)(C)C)C([O-])=O)CC(O)COC(=O)CCCCCCC/C=C\\CCCCCCCC',
                                      'name': '4-[2-hydroxy-3-[(Z)-octadec-9-enoyl]oxypropoxy]-2-(trimethylazaniumyl)butanoate',
                                      'reason': 'Found 1 ester groups attached '
                                                'to glycerol, need exactly 2'},
                                  {   'smiles': 'CCCCCC(=O)OC[C@@H](CO)OC(=O)CCCCC',
                                      'name': '2,3-dihexanoyl-sn-glycerol',
                                      'reason': 'Molecular weight too low '
                                                '(288.2 < 300)'},
                                  {   'smiles': 'C(CCCCCCC/C=C\\CCCCCCCC)(=O)O[C@@H](COP(=O)([O-])[O-])CO/C=C\\CCCCCCCCCCCCCCCC',
                                      'name': '1-[(1Z)-octadecenyl]-2-oleoyl-sn-glycero-3-phosphate(2-)',
                                      'reason': 'Found 1 ester groups attached '
                                                'to glycerol, need exactly 2'}],
    'attempt': 1,
    'reasoning': '',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 624,
    'num_false_positives': 35,
    'num_true_negatives': 141607,
    'num_false_negatives': 34,
    'num_negatives': None,
    'precision': 0.9468892261001517,
    'recall': 0.9483282674772037,
    'f1': 0.9476082004555808,
    'accuracy': 0.9995151089248068,
    'negative_predictive_value': 0.9997599565097677}