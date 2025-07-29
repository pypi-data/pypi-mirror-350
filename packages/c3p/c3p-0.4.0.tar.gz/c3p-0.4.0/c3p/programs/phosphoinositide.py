"""
Classifies: CHEBI:18179 phosphoinositide
"""
"""
Classifies: CHEBI:18179 phosphoinositide
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_phosphoinositide(smiles: str):
    """
    Determines if a molecule is a phosphoinositide based on its SMILES string.
    A phosphoinositide is a phosphatidylinositol that is phosphorylated at one or more of the hydroxy groups of inositol.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a phosphoinositide, False otherwise
        str: Reason for classification
    """
    
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check molecular weight - phosphoinositides are typically >600 Da
    mol_wt = rdMolDescriptors.CalcExactMolWt(mol)
    if mol_wt < 600:
        return False, "Molecular weight too low for phosphoinositide"

    # Look for glycerol backbone pattern (C-C-C with 3 oxygens attached)
    glycerol_pattern = Chem.MolFromSmarts("[CH2X4][CHX4][CH2X4]")
    if not mol.HasSubstructMatch(glycerol_pattern):
        return False, "No glycerol backbone found"
        
    # Look for 2 ester groups (-O-C(=O)-) for fatty acid chains
    ester_pattern = Chem.MolFromSmarts("[OX2][CX3](=[OX1])")
    ester_matches = mol.GetSubstructMatches(ester_pattern)
    if len(ester_matches) < 2:
        return False, f"Found {len(ester_matches)} ester groups, need at least 2 for fatty acid chains"

    # Look for phosphate group attached to glycerol (P-O-C)
    phosphate_glycerol_pattern = Chem.MolFromSmarts("[PX4](=[OX1])([OX2][CX4])[OX2]")
    if not mol.HasSubstructMatch(phosphate_glycerol_pattern):
        return False, "No phosphate group attached to glycerol backbone"

    # Look for inositol ring (6-membered ring with 6 oxygens, no stereochemistry requirement)
    inositol_pattern = Chem.MolFromSmarts("[C]1([C]([C]([C]([C]([C]1O)O)O)O)O)O")
    if not mol.HasSubstructMatch(inositol_pattern):
        return False, "No inositol ring found"

    # Look for phosphate groups attached to inositol (more flexible pattern)
    phosphate_inositol_pattern = Chem.MolFromSmarts("[PX4](=[OX1])([OX2][C]1[C]([C]([C]([C]([C]1O)O)O)O)O)[OX2]")
    phosphate_inositol_matches = mol.GetSubstructMatches(phosphate_inositol_pattern)
    
    # Must have at least one phosphate on inositol
    if len(phosphate_inositol_matches) < 1:
        return False, "No phosphorylation on inositol ring"
    
    # Count total phosphate groups (should be at least 2: one on glycerol, one on inositol)
    total_phosphates = len(mol.GetSubstructMatches(Chem.MolFromSmarts("[PX4](=[OX1])([OX2])[OX2]")))
    if total_phosphates < 2:
        return False, f"Found only {total_phosphates} phosphate groups, need at least 2"

    # Check element counts
    c_count = sum(1 for atom in mol.GetAtoms() if atom.GetAtomicNum() == 6)
    o_count = sum(1 for atom in mol.GetAtoms() if atom.GetAtomicNum() == 8)
    p_count = sum(1 for atom in mol.GetAtoms() if atom.GetAtomicNum() == 15)
    
    if c_count < 20:
        return False, "Too few carbons for phosphoinositide"
    if o_count < 10:
        return False, "Too few oxygens for phosphoinositide"
    if p_count < 2:
        return False, "Too few phosphorus atoms for phosphoinositide"

    return True, "Contains glycerol backbone with 2 fatty acid chains, phosphate groups, and phosphorylated inositol ring"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:18179',
                          'name': 'phosphoinositide',
                          'definition': 'Any phosphatidylinositol that is '
                                        'phosphorylated at one or more of the '
                                        'hydroxy groups of inositol.',
                          'parents': ['CHEBI:28874'],
                          'xrefs': [   'PMID:10782093',
                                       'PMID:15269334',
                                       'PMID:17035995',
                                       'PMID:19154715'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 55,
                           'log_lines_of_code': 4.007333185232471,
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
                                                 2,
                                                 0,
                                                 1,
                                                 1,
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
                                                 2,
                                                 1,
                                                 2,
                                                 0,
                                                 1],
                           'max_indent': 2,
                           'imports': [   'from rdkit import Chem',
                                          'from rdkit.Chem import AllChem',
                                          'from rdkit.Chem import '
                                          'rdMolDescriptors'],
                           'imports_count': 3,
                           'methods_called': [   'GetSubstructMatches',
                                                 'GetAtomicNum',
                                                 'HasSubstructMatch',
                                                 'MolFromSmarts',
                                                 'GetAtoms',
                                                 'CalcExactMolWt',
                                                 'MolFromSmiles'],
                           'methods_called_count': 7,
                           'smarts_strings': [   '"[PX4](=[OX1])([OX2])[OX2]"))',
                                                 '[OX2][CX3](=[OX1])',
                                                 '[PX4](=[OX1])([OX2][CX4])[OX2]',
                                                 '[PX4](=[OX1])([OX2][C]1[C]([C]([C]([C]([C]1O)O)O)O)O)[OX2]',
                                                 '[CH2X4][CHX4][CH2X4]',
                                                 '[C]1([C]([C]([C]([C]([C]1O)O)O)O)O)O'],
                           'smarts_strings_count': 6,
                           'defs': ['is_phosphoinositide(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "Molecular weight too low '
                                          'for phosphoinositide"',
                                          'False, "No glycerol backbone found"',
                                          'False, f"Found {len(ester_matches)} '
                                          'ester groups, need at least 2 for '
                                          'fatty acid chains"',
                                          'False, "No phosphate group attached '
                                          'to glycerol backbone"',
                                          'False, "No inositol ring found"',
                                          'False, "No phosphorylation on '
                                          'inositol ring"',
                                          'False, f"Found only '
                                          '{total_phosphates} phosphate '
                                          'groups, need at least 2"',
                                          'False, "Too few carbons for '
                                          'phosphoinositide"',
                                          'False, "Too few oxygens for '
                                          'phosphoinositide"',
                                          'False, "Too few phosphorus atoms '
                                          'for phosphoinositide"',
                                          'True, "Contains glycerol backbone '
                                          'with 2 fatty acid chains, phosphate '
                                          'groups, and phosphorylated inositol '
                                          'ring"'],
                           'returns_count': 12,
                           'complexity': 5.201466637046495},
    'message': '\n'
               'Attempt failed: F1 score of 0.3398692810457516 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: '
               'CCCCCCCCCCCCCCCCCC(=O)OC[C@H](COP(O)(=O)O[C@@H]1[C@H](O)[C@H](OP(O)(O)=O)[C@@H](OP(O)(O)=O)[C@H](OP(O)(O)=O)[C@H]1O)OC(=O)CCC\\C=C/C\\C=C/C\\C=C/C\\C=C/CCCCC '
               'NAME: '
               '1-stearoyl-2-arachidonoyl-sn-glycero-3-phospho-(1D-myo-inositol '
               '3,4,5-triphosphate) REASON: CORRECT Contains glycerol backbone '
               'with 2 fatty acid chains, a phosphate group, and '
               'phosphorylated inositol ring\n'
               ' * SMILES: '
               'O=C(CCC/C=C\\C/C=C\\C/C=C\\C/C=C\\CCCCC)O[C@@H](COP(O[C@H]1[C@@H]([C@H]([C@@H]([C@H]([C@H]1O)O)OP(O)(=O)O)O)O)(=O)O)COC(=O)CCCCCCCCCCCCCCCCC '
               'NAME: '
               '1-stearoyl-2-arachidonoyl-sn-glycero-3-phospho-1D-myo-inositol '
               '4-phosphate REASON: CORRECT Contains glycerol backbone with 2 '
               'fatty acid chains, a phosphate group, and phosphorylated '
               'inositol ring\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCC(=O)OC[C@H](COP(O)(=O)O[C@@H]1[C@H](O)[C@H](O)[C@@H](O)[C@H](OP(O)(O)=O)[C@H]1O)OC(=O)CCC\\C=C/C\\C=C/C\\C=C/C\\C=C/CCCCC '
               'NAME: '
               '1-stearoyl-2-arachidonoyl-sn-glycero-3-phospho-1D-myo-inositol '
               '5-phosphate REASON: CORRECT Contains glycerol backbone with 2 '
               'fatty acid chains, a phosphate group, and phosphorylated '
               'inositol ring\n'
               ' * SMILES: '
               'CCCCCCCC(=O)OC[C@H](COP(O)(=O)O[C@H]1[C@H](O)[C@@H](O)[C@H](OP(O)(O)=O)[C@@H](OP(O)(O)=O)[C@H]1O)OC(=O)CCCCCCC '
               'NAME: '
               '1,2-dioctanoyl-sn-glycero-3-phospho-(1D-myo-inositol-3,4-bisphosphate) '
               'REASON: CORRECT Contains glycerol backbone with 2 fatty acid '
               'chains, a phosphate group, and phosphorylated inositol ring\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCC(=O)OC[C@H](COP(O)(=O)O[C@@H]1[C@H](O)[C@H](O)[C@@H](O)[C@H](OP(O)(O)=O)[C@H]1O)OC(=O)CCCCCCCCCCCCCCC '
               'NAME: '
               '1,2-dipalmitoyl-sn-glycero-3-phospho-(1D-myo-inositol-5-phosphate) '
               'REASON: CORRECT Contains glycerol backbone with 2 fatty acid '
               'chains, a phosphate group, and phosphorylated inositol ring\n'
               ' * SMILES: '
               'P(O[C@@H]1C(O)[C@H](OP(O)(O)=O)C(OP(O)(O)=O)C(O)C1O)(OC[C@H](OC(=O)CCCCCCC/C=C\\C/C=C\\CCCCC)COC(=O)CCCCCCC/C=C\\C/C=C\\CCCCC)(O)=O '
               'NAME: PIP2(18:2/18:2) REASON: CORRECT Contains glycerol '
               'backbone with 2 fatty acid chains, a phosphate group, and '
               'phosphorylated inositol ring\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCC(=O)OC[C@H](COP(O)(=O)O[C@@H]1[C@H](O)[C@H](O)[C@@H](OP(O)(O)=O)[C@H](O)[C@H]1O)OC(=O)CCCCCCC\\C=C/CCCCCCCC '
               'NAME: 1-stearoyl-2-oleoyl-sn-glycero-3-phospho-1D-myo-inositol '
               '4-phosphate REASON: CORRECT Contains glycerol backbone with 2 '
               'fatty acid chains, a phosphate group, and phosphorylated '
               'inositol ring\n'
               ' * SMILES: '
               'CCCCCCCC(=O)OC[C@H](COP(O)(=O)O[C@@H]1[C@H](O)[C@H](O)[C@@H](O)[C@H](OP(O)(O)=O)[C@H]1O)OC(=O)CCCCCCC '
               'NAME: '
               "1,2-dioctanoyl-sn-glycero-3-phospho-(1'-myo-inositol-5'-phosphate) "
               'REASON: CORRECT Contains glycerol backbone with 2 fatty acid '
               'chains, a phosphate group, and phosphorylated inositol ring\n'
               ' * SMILES: '
               'CCCCCCCC(=O)OC[C@H](COP(O)(=O)O[C@H]1[C@H](O)[C@@H](O)[C@H](O)[C@@H](OP(O)(O)=O)[C@H]1O)OC(=O)CCCCCCC '
               'NAME: '
               "1,2-dioctanoyl-sn-glycero-3-phospho-(1D-myo-inositol-3'-phosphate) "
               'REASON: CORRECT Contains glycerol backbone with 2 fatty acid '
               'chains, a phosphate group, and phosphorylated inositol ring\n'
               ' * SMILES: '
               '[C@@H]1(C(C(C([C@H](C1O)OP(=O)(O)O)OP(=O)(O)O)O)O)OP(OC[C@@](COC(CCCCCCCCCCCCCCC)=O)(OC(CCCCCCCCCCCCCCCCC)=O)[H])(O)=O '
               "NAME: PIP2[3',4'](16:0/18:0) REASON: CORRECT Contains glycerol "
               'backbone with 2 fatty acid chains, a phosphate group, and '
               'phosphorylated inositol ring\n'
               ' * SMILES: '
               'P(O[C@@H]1C(O)[C@H](OP(O)(O)=O)C(OP(O)(O)=O)C(O)C1O)(OC[C@H](OC(=O)CCCCCCCCCCCCCCC)COC(=O)CCCCCCCCCCCCCCC)(O)=O '
               'NAME: PIP2(16:0/16:0) REASON: CORRECT Contains glycerol '
               'backbone with 2 fatty acid chains, a phosphate group, and '
               'phosphorylated inositol ring\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCC(=O)OC[C@H](COP(O)(=O)O[C@@H]1[C@H](O)[C@H](O)[C@@H](OP(O)(O)=O)[C@H](O)[C@H]1O)OC(=O)CCCCCCCCCCCCCCC '
               'NAME: '
               '1,2-dihexadecanoyl-sn-glycero-3-phospho-(1D-myo-inositol-4-phosphate) '
               'REASON: CORRECT Contains glycerol backbone with 2 fatty acid '
               'chains, a phosphate group, and phosphorylated inositol ring\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCC(=O)OC[C@H](COP(O)(=O)O[C@H]1[C@H](O)[C@@H](O)[C@H](O)[C@@H](OP(O)(O)=O)[C@H]1O)OC(=O)CCCCCCCCCCCCCCC '
               'NAME: '
               "1,2-dipalmitoyl-sn-glycero-3-phospho-(1'D-myo-inositol-3'-phosphate) "
               'REASON: CORRECT Contains glycerol backbone with 2 fatty acid '
               'chains, a phosphate group, and phosphorylated inositol ring\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCC(=O)OC[C@H](COP(O)(=O)O[C@H]1[C@H](O)[C@@H](OP(O)(O)=O)[C@H](O)[C@@H](OP(O)(O)=O)[C@H]1O)OC(=O)CCCCCCCCCCCCCCC '
               'NAME: '
               "1,2-dipalmitoyl-sn-glycero-3-phospho-(1'D-myo-inositol-3',5'-bisphosphate) "
               'REASON: CORRECT Contains glycerol backbone with 2 fatty acid '
               'chains, a phosphate group, and phosphorylated inositol ring\n'
               ' * SMILES: '
               '[C@@H]1(C(C(C([C@H](C1O)OP(=O)(O)O)O)O)O)OP(OC[C@](COC(CCCCCCCCCCCCCCCCC)=O)([H])OC(CCCCCCCCCCCCCCC)=O)(O)=O '
               'NAME: PIP(18:0/16:0) REASON: CORRECT Contains glycerol '
               'backbone with 2 fatty acid chains, a phosphate group, and '
               'phosphorylated inositol ring\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCC(=O)OC[C@H](COP(O)(=O)O[C@H]1[C@H](O)[C@@H](O)[C@H](OP(O)(O)=O)[C@@H](OP(O)(O)=O)[C@H]1O)OC(=O)CCCCCCCCCCCCCCC '
               'NAME: '
               '1,2-dihexadecanoyl-sn-glycero-3-phospho-(1D-myo-inositol-3,4-bisphosphate) '
               'REASON: CORRECT Contains glycerol backbone with 2 fatty acid '
               'chains, a phosphate group, and phosphorylated inositol ring\n'
               ' * SMILES: '
               'CCCCCCCC(=O)OC[C@H](COP(O)(=O)O[C@@H]1[C@H](O)[C@H](O)[C@@H](OP(O)(O)=O)[C@H](OP(O)(O)=O)[C@H]1O)OC(=O)CCCCCCC '
               'NAME: '
               '1,2-dioctanoyl-sn-glycero-3-phospho-(1D-myo-inositol-4,5-bisphosphate) '
               'REASON: CORRECT Contains glycerol backbone with 2 fatty acid '
               'chains, a phosphate group, and phosphorylated inositol ring\n'
               ' * SMILES: '
               'O(C[C@](COP(O)(=O)O[C@H]1C(C(C([C@H](C1O)OP(=O)(O)O)O)O)O)(OC(CCC/C=C\\C/C=C\\C/C=C\\C/C=C\\CCCCC)=O)[H])C(CCCCCCCCC/C=C\\CCCCCC)=O '
               'NAME: PIP(18:1(11Z)/20:4(5Z,8Z,11Z,14Z)) REASON: CORRECT '
               'Contains glycerol backbone with 2 fatty acid chains, a '
               'phosphate group, and phosphorylated inositol ring\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCC(=O)OC[C@H](COP(O)(=O)O[C@@H]1[C@H](O)[C@H](OP(O)(O)=O)[C@@H](OP(O)(O)=O)[C@H](OP(O)(O)=O)[C@H]1O)OC(=O)CCCCCCCCCCCCCCC '
               'NAME: '
               '1,2-dihexadecanoyl-sn-glycero-3-phospho-(1D-myo-inositol-3,4,5-trisphosphate) '
               'REASON: CORRECT Contains glycerol backbone with 2 fatty acid '
               'chains, a phosphate group, and phosphorylated inositol ring\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCC(=O)OC[C@H](COP(O)(=O)O[C@@H]1[C@H](O)[C@H](O)[C@@H](OP(O)(O)=O)[C@H](OP(O)(O)=O)[C@H]1O)OC(=O)CCC\\C=C/C\\C=C/C\\C=C/C\\C=C/CCCCC '
               'NAME: '
               '1-stearoyl-2-arachidonoyl-sn-glycero-3-phospho-1D-myo-inositol '
               '4,5-biphosphate REASON: CORRECT Contains glycerol backbone '
               'with 2 fatty acid chains, a phosphate group, and '
               'phosphorylated inositol ring\n'
               ' * SMILES: '
               'CCCCC\\C=C/C\\C=C/CCCCCCCC(=O)OC[C@H](COP(O)(=O)O[C@@H]1[C@H](O)[C@H](O)[C@@H](O)[C@H](OP(O)(O)=O)[C@H]1O)OC(=O)CCCCCCC\\C=C/C\\C=C/CCCCC '
               'NAME: 1,2-dilinoleoyl-sn-glycero-3-phospho-1D-myo-inositol '
               '5-phosphate REASON: CORRECT Contains glycerol backbone with 2 '
               'fatty acid chains, a phosphate group, and phosphorylated '
               'inositol ring\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCC(=O)OC[C@H](COP(O)(=O)O[C@@H]1[C@H](O)[C@H](O)[C@@H](O)[C@H](OP(O)(O)=O)[C@H]1O)OC(=O)CCCCCCC\\C=C/CCCCCCCC '
               'NAME: 1-stearoyl-2-oleoyl-sn-glycero-3-phospho-1D-myo-inositol '
               '5-phosphate REASON: CORRECT Contains glycerol backbone with 2 '
               'fatty acid chains, a phosphate group, and phosphorylated '
               'inositol ring\n'
               ' * SMILES: '
               '[C@@H]1([C@@H]([C@@H]([C@@H]([C@H]([C@@H]1O)OP(O)(=O)O)O)O)OP(OC[C@@H](COC(=O)CCCCCCC)OC(=O)CCCCCCC)(=O)O)O '
               'NAME: '
               '1,2-dioctanoyl-sn-glycero-3-phospho-(1D-myo-inositol-4-phosphate) '
               'REASON: CORRECT Contains glycerol backbone with 2 fatty acid '
               'chains, a phosphate group, and phosphorylated inositol ring\n'
               ' * SMILES: '
               'CCCCCCCC(=O)OC[C@H](COP(O)(=O)O[C@H]1[C@H](O)[C@@H](OP(O)(O)=O)[C@H](O)[C@@H](OP(O)(O)=O)[C@H]1O)OC(=O)CCCCCCC '
               'NAME: '
               '1,2-dioctanoyl-sn-glycero-3-phospho-(1D-myo-inositol-3,5-bisphosphate) '
               'REASON: CORRECT Contains glycerol backbone with 2 fatty acid '
               'chains, a phosphate group, and phosphorylated inositol ring\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCC(=O)OC[C@H](COP(O)(=O)O[C@@H]1[C@H](O)[C@H](O)[C@@H](OP(O)(O)=O)[C@H](OP(O)(O)=O)[C@H]1O)OC(=O)CCCCCCCCCCCCCCC '
               'NAME: '
               '1,2-dihexadecanoyl-sn-glycero-3-phospho-(1D-myo-inositol-4,5-bisphosphate) '
               'REASON: CORRECT Contains glycerol backbone with 2 fatty acid '
               'chains, a phosphate group, and phosphorylated inositol ring\n'
               'False positives: SMILES: '
               '[C@@H]1(C(C(C([C@H](C1O)O)O)O)O)OP(OC[C@@](COC(CCCCCCC/C=C\\C/C=C\\CCCCC)=O)(OC(CCCCCCCCCCCCCCC)=O)[H])(O)=O '
               'NAME: PI(18:2(9Z,12Z)/16:0) REASON: WRONGLY CLASSIFIED '
               'Contains glycerol backbone with 2 fatty acid chains, a '
               'phosphate group, and phosphorylated inositol ring\n'
               ' * SMILES: '
               'O([C@@H]1[C@@H]([C@@H]([C@H]([C@@H]([C@H]1O[C@@H]2[C@H]([C@H]([C@@H]([C@H](O2)COC(=O)CCCCCCCCCCCCCCC)O)O)O)OC(CCCCCCCCCCCCCCC)=O)O)O)O[C@@H]3[C@H]([C@H]([C@@H]([C@H](O3)CO)O)O)O)P(=O)(O)OC[C@@H](COC(CCCCCCCC[C@H](CCCCCCCC)C)=O)OC(CCCCCCCCCCCCCCC)=O '
               'NAME: '
               '2-O-alpha-D-mannosyl-1-O-{1-O-[(10S)-10-methyloctadecanoyl]-2-O-palmitoyl-sn-glycero-3-phosphono}-5-O-palmitoyl-6-O-(6-O-palmitoyl-alpha-D-mannosyl)-1D-myo-inositol '
               'REASON: WRONGLY CLASSIFIED Contains glycerol backbone with 2 '
               'fatty acid chains, a phosphate group, and phosphorylated '
               'inositol ring\n'
               ' * SMILES: '
               'P(OC1C(O)C(O)C(O)[C@@H](O)C1O)(OC[C@H](OC(=O)CCCCCCC/C=C\\C/C=C\\CCCCC)COC(=O)CCCCCCCCCCCCC)(O)=O '
               'NAME: PI(14:0/18:2(9Z,12Z)) REASON: WRONGLY CLASSIFIED '
               'Contains glycerol backbone with 2 fatty acid chains, a '
               'phosphate group, and phosphorylated inositol ring\n'
               ' * SMILES: '
               '[C@@H]1(C(C(C([C@H](C1O)O)O)O)O)OP(OC[C@@](COC(CCCCCCCCC/C=C\\CCCCCC)=O)(OC(CCC/C=C\\C/C=C\\C/C=C\\CCCCCCCC)=O)[H])(O)=O '
               'NAME: PI(18:1(11Z)/20:3(5Z,8Z,11Z)) REASON: WRONGLY CLASSIFIED '
               'Contains glycerol backbone with 2 fatty acid chains, a '
               'phosphate group, and phosphorylated inositol ring\n'
               ' * SMILES: '
               'P(O[C@H]1[C@H](O[C@H]2OC([C@@H](O)C(O)[C@H]2O)CO)C(O)[C@H](O)C(O)C1O)(OC[C@H](OC(=O)CCCCCCC/C=C\\C/C=C\\CCC)COC(=O)CCCCCCCCCCCCCCC)(O)=O '
               'NAME: PIM1(16:0/16:2(9Z,12Z)) REASON: WRONGLY CLASSIFIED '
               'Contains glycerol backbone with 2 fatty acid chains, a '
               'phosphate group, and phosphorylated inositol ring\n'
               ' * SMILES: '
               'P(OC1C(O)C(O)C(O)[C@@H](O)C1O)(OC[C@H](OC(=O)CCCCCCCCCCC/C=C\\C/C=C\\CCCCC)COC(=O)CCCCCCC/C=C\\CCCCCCCC)(O)=O '
               'NAME: PI(18:1(9Z)/22:2(13Z,16Z)) REASON: WRONGLY CLASSIFIED '
               'Contains glycerol backbone with 2 fatty acid chains, a '
               'phosphate group, and phosphorylated inositol ring\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCC(=O)OC[C@H](COP([O-])(=O)O[C@@H]1[C@H](O)[C@H](O)[C@@H](O)[C@H](OP([O-])([O-])=O)[C@H]1O)OC(=O)CCCCCCC\\C=C/CCCCCCCC '
               'NAME: 1-stearoyl-2-oleoyl-sn-glycero-3-phospho-1D-myo-inositol '
               '5-phosphate(3-) REASON: WRONGLY CLASSIFIED Contains glycerol '
               'backbone with 2 fatty acid chains, a phosphate group, and '
               'phosphorylated inositol ring\n'
               ' * SMILES: '
               '[C@@H]1(C(C(C([C@H](C1O)O)O)O)O)OP(OC[C@@](COC(CCCCCC/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)=O)(OC(CCCCCCCCCCCCCCC)=O)[H])(O)=O '
               'NAME: PI(20:4(8Z,11Z,14Z,17Z)/16:0) REASON: WRONGLY CLASSIFIED '
               'Contains glycerol backbone with 2 fatty acid chains, a '
               'phosphate group, and phosphorylated inositol ring\n'
               ' * SMILES: '
               '[C@@H]1(C(C(C([C@H](C1O)O)O)O)O)OP(OC[C@@](COC(CCCCCCCCCCCCCCCCC)=O)(OC(CCCCCCCCCCCCCCCCC)=O)[H])(O)=O '
               'NAME: PI(18:0/18:0) REASON: WRONGLY CLASSIFIED Contains '
               'glycerol backbone with 2 fatty acid chains, a phosphate group, '
               'and phosphorylated inositol ring\n'
               ' * SMILES: '
               'P(OC1C(O)C(O)C(O)[C@@H](O)C1O)(OC[C@H](OC(=O)CCCCCCC/C=C\\CCCCCCC)COC(=O)CCC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)(O)=O '
               'NAME: PI(20:5(5Z,8Z,11Z,14Z,17Z)/17:1(9Z)) REASON: WRONGLY '
               'CLASSIFIED Contains glycerol backbone with 2 fatty acid '
               'chains, a phosphate group, and phosphorylated inositol ring\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCC(=O)OC[C@H](COP(O)(=O)O[C@H]1[C@H](O)[C@@H](O)[C@H](O)[C@@H](O)[C@H]1O)OC(=O)CCCCCCC\\C=C/C\\C=C/CCCCC '
               'NAME: '
               '1-hexadecanoyl-2-(9Z,12Z-octadecadienoyl)-sn-glycero-3-phospho-D-myo-inositol '
               'REASON: WRONGLY CLASSIFIED Contains glycerol backbone with 2 '
               'fatty acid chains, a phosphate group, and phosphorylated '
               'inositol ring\n'
               ' * SMILES: '
               'P(OC1C(O)C(O)C(O)[C@@H](O)C1O)(OC[C@H](OC(=O)CCCCCCC/C=C\\CCCCCCCCC)COC(=O)CCCCCCCCCCCCCC)(O)=O '
               'NAME: PI(15:0/19:1(9Z)) REASON: WRONGLY CLASSIFIED Contains '
               'glycerol backbone with 2 fatty acid chains, a phosphate group, '
               'and phosphorylated inositol ring\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCC(=O)OCC(COP(O)(=O)O[C@@H]1[C@H](O[C@H]2O[C@H](CO)[C@@H](O)[C@H](O)[C@@H]2O)[C@H](O)[C@@H](O)[C@H](O)[C@H]1O[C@H]1O[C@H](CO[C@H]2O[C@H](CO[C@H]3O[C@H](CO)[C@@H](O)[C@H](O)[C@@H]3O[C@H]3O[C@H](CO)[C@@H](O)[C@H](O)[C@@H]3O[C@H]3O[C@H](CO)[C@@H](O)[C@H](O)[C@@H]3O)[C@@H](O)[C@H](O)[C@@H]2O)[C@@H](O)[C@H](O)[C@@H]1O)OC(=O)CCCCCCCC(C)CCCCCCCCCC '
               'NAME: PIM6 REASON: WRONGLY CLASSIFIED Contains glycerol '
               'backbone with 2 fatty acid chains, a phosphate group, and '
               'phosphorylated inositol ring\n'
               ' * SMILES: '
               'C(\\CCCCCCCC(O[C@@H](COP(O[C@H]1[C@@H]([C@H]([C@@H]([C@H]([C@H]1O)O)O)O)O)(=O)O)COC(=O)CCCCCCCCCCC/C=C\\C/C=C\\CCCCC)=O)=C\\C/C=C\\CCCCC '
               'NAME: '
               '1-[(13Z,16Z)-docosadienoyl]-2-linoleoyl-sn-glycero-3-phospho-1D-myo-inositol '
               'REASON: WRONGLY CLASSIFIED Contains glycerol backbone with 2 '
               'fatty acid chains, a phosphate group, and phosphorylated '
               'inositol ring\n'
               ' * SMILES: '
               'P(OC1C(O)C(O)C(O)[C@@H](O)C1O)(OC[C@H](OC(=O)CCCCCCCCCCCCCCCCCCCC)COC(=O)CCCCCCC/C=C\\CCCCCC)(O)=O '
               'NAME: PI(16:1(9Z)/21:0) REASON: WRONGLY CLASSIFIED Contains '
               'glycerol backbone with 2 fatty acid chains, a phosphate group, '
               'and phosphorylated inositol ring\n'
               ' * SMILES: '
               'P(OC1C(O)C(O)C(O)[C@@H](O)C1O)(OC[C@H](OC(=O)CCCCCCCCC/C=C\\CCCCCCCC)COC(=O)CCCCCCC/C=C\\CCCCCCC)(O)=O '
               'NAME: PI(37:2) REASON: WRONGLY CLASSIFIED Contains glycerol '
               'backbone with 2 fatty acid chains, a phosphate group, and '
               'phosphorylated inositol ring\n'
               ' * SMILES: '
               'C(CCCCCCCCCCC)CCCCCCCC(O[C@@H](COP(O[C@H]1[C@@H]([C@H]([C@@H]([C@H]([C@H]1O)O)O)O)O)(=O)O)COC(CCCCCC/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)=O)=O '
               'NAME: '
               '1-[(8Z,11Z,14Z,17Z)-icosatetraenoyl]-2-icosanoyl-sn-glycero-3-phospho-1D-myo-inositol '
               'REASON: WRONGLY CLASSIFIED Contains glycerol backbone with 2 '
               'fatty acid chains, a phosphate group, and phosphorylated '
               'inositol ring\n'
               ' * SMILES: '
               'P(OC1C(O)C(O)C(O)[C@@H](O)C1O)(OC[C@H](OC(=O)CCCCCCC/C=C\\C/C=C\\C/C=C\\CC)COC(=O)CCCCCCCCC/C=C\\CCCCCCCCCC)(O)=O '
               'NAME: PI(22:1(11Z)/18:3(9Z,12Z,15Z)) REASON: WRONGLY '
               'CLASSIFIED Contains glycerol backbone with 2 fatty acid '
               'chains, a phosphate group, and phosphorylated inositol ring\n'
               ' * SMILES: '
               'P(OC1[C@H](O)[C@H](O)C(O)[C@H](O)[C@H]1O)(OC[C@H](OC(=O)CC/C=C\\C/C=C\\C\\C=C/C=C/C(O)C/C=C\\C/C=C\\CC)COC(=O)CCCCCCCCCCCCCCC)(O)=O '
               'NAME: PI(16:0/22:6(4Z,7Z,10Z,12E,16Z,19Z)-OH(14)) REASON: '
               'WRONGLY CLASSIFIED Contains glycerol backbone with 2 fatty '
               'acid chains, a phosphate group, and phosphorylated inositol '
               'ring\n'
               ' * SMILES: '
               '[C@@H]1(C(C(C([C@H](C1O)O)O)O)O)OP(OC[C@@](COC(CCCCCCCC/C=C\\C/C=C\\C/C=C\\CCCCC)=O)(OC(CCCC/C=C\\C/C=C\\C/C=C\\CCCCC)=O)[H])(O)=O '
               'NAME: PI(22:3(10Z,13Z,16Z)/18:3(6Z,9Z,12Z)) REASON: WRONGLY '
               'CLASSIFIED Contains glycerol backbone with 2 fatty acid '
               'chains, a phosphate group, and phosphorylated inositol ring\n'
               ' * SMILES: '
               'CCCC(=O)OC[C@H](COP([O-])(=O)O[C@H]1[C@H](O)[C@@H](O)[C@H](O)[C@@H](O)[C@H]1O)OC(=O)CCC '
               'NAME: '
               "1,2-dibutyryl-sn-glycero-3-phospho-(1'D-myo-inositol)(1-) "
               'REASON: WRONGLY CLASSIFIED Contains glycerol backbone with 2 '
               'fatty acid chains, a phosphate group, and phosphorylated '
               'inositol ring\n'
               ' * SMILES: '
               'P(OC1C(O)C(O)C(O)[C@@H](O)C1O)(OC[C@H](OC(=O)CCCCCCCCC/C=C\\CCCCCCCCCC)COC(=O)CCCCCCCCC/C=C\\C/C=C\\CCCCC)(O)=O '
               'NAME: PI(20:2(11Z,14Z)/22:1(11Z)) REASON: WRONGLY CLASSIFIED '
               'Contains glycerol backbone with 2 fatty acid chains, a '
               'phosphate group, and phosphorylated inositol ring\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCC(=O)OC[C@H](COP([O-])(=O)O[C@@H]1[C@H](O)[C@H](O)[C@@H](OP([O-])([O-])=O)[C@H](O)[C@H]1O)OC(=O)CCC\\C=C/C\\C=C/C\\C=C/C\\C=C/CCCCC '
               'NAME: '
               '1-stearoyl-2-arachidonoyl-sn-glycero-3-phospho-1D-myo-inositol '
               '4-phosphate(3-) REASON: WRONGLY CLASSIFIED Contains glycerol '
               'backbone with 2 fatty acid chains, a phosphate group, and '
               'phosphorylated inositol ring\n'
               ' * SMILES: '
               'P(OC1C(O)C(O)C(O)[C@@H](O)C1O)(OC[C@H](OC(=O)CCCCCCCC(O)/C=C/C(O)=O)COC(=O)CCCCCCCCCCCCCCC)(O)=O '
               'NAME: PHDdiA-PI REASON: WRONGLY CLASSIFIED Contains glycerol '
               'backbone with 2 fatty acid chains, a phosphate group, and '
               'phosphorylated inositol ring\n'
               ' * SMILES: '
               'P(OC1C(O)C(O)C(O)[C@@H](O)C1O)(OC[C@H](OC(=O)CCCCCCC/C=C\\C/C=C\\CCCC)COC(=O)CCCCCCC/C=C\\CCCCCC)(O)=O '
               'NAME: PI(16:1(9Z)/17:2(9Z,12Z)) REASON: WRONGLY CLASSIFIED '
               'Contains glycerol backbone with 2 fatty acid chains, a '
               'phosphate group, and phosphorylated inositol ring\n'
               'False negatives: SMILES: '
               '[C@@H]1([C@@H]([C@@H](O)[C@H]([C@H]([C@@H]1O)OP(=O)(OCOC(=O)CCC)OCOC(=O)CCC)O)OP(=O)(OCOC(=O)CCC)OCOC(=O)CCC)OP(=O)(OCOC(=O)CCC)OCOC(=O)CCC '
               'NAME: D-myo-Ins(1,4,5)P3 hexakis(butyryloxymethyl) ester '
               'REASON: MISSED No glycerol backbone found\n'
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
    'sample_true_negatives': [   {   'smiles': 'C(C(COC(=O)CCCCCCC/C=C\\C[C@@H](CCCCCC)O)OC(=O)CCCCCCC/C=C\\C[C@@H](CCCCCC)O)OC(=O)CCCCCCC/C=C\\C[C@@H](CCCCCC)O',
                                     'name': 'triricinolein',
                                     'reason': 'No phosphate group attached to '
                                               'glycerol backbone'},
                                 {   'smiles': 'CC(Cl)(Cl)C(O)=O',
                                     'name': 'Dalapon',
                                     'reason': 'Molecular weight too low for '
                                               'phosphoinositide'},
                                 {   'smiles': 'CC(C)C#CC1=CC=C(C=C1)[C@@H]2[C@H]3CN(CC(=O)N3[C@H]2CO)S(=O)(=O)C4=CC=CC=C4',
                                     'name': '(6S,7R,8R)-4-(benzenesulfonyl)-8-(hydroxymethyl)-7-[4-(3-methylbut-1-ynyl)phenyl]-1,4-diazabicyclo[4.2.0]octan-2-one',
                                     'reason': 'Molecular weight too low for '
                                               'phosphoinositide'},
                                 {   'smiles': 'O=C(N[C@@H](CC=1C=2C(NC1)=CC=CC2)C(O)=O)[C@@H](NC(=O)CN)CCC(=O)N',
                                     'name': 'Gly-Gln-Trp',
                                     'reason': 'Molecular weight too low for '
                                               'phosphoinositide'},
                                 {   'smiles': 'O=C(N1CCN(CC1)C=2N=CC(CCC)=CN2)C3=NOC(=C3)C',
                                     'name': '(5-methyl-3-isoxazolyl)[4-(5-propyl-2-pyrimidinyl)piperazino]methanone',
                                     'reason': 'Molecular weight too low for '
                                               'phosphoinositide'},
                                 {   'smiles': 'O1C2C(C(C1=O)C)CCC(=CCC(O)C(=C2)C)CO',
                                     'name': '3,14-Dihydroxy-11,13-dihydrocostunolide',
                                     'reason': 'Molecular weight too low for '
                                               'phosphoinositide'},
                                 {   'smiles': 'CSc1cc2CCN(C(=O)Nc3cccnc3)c2cc1C(F)(F)F',
                                     'name': 'SB 221284',
                                     'reason': 'Molecular weight too low for '
                                               'phosphoinositide'},
                                 {   'smiles': '[C@H]1(CC/C(/C)=C/COP(OP(=O)(O)O)(=O)O)C(C)=CC[C@@]2([C@]1(C)CCCC2(C)C)[H]',
                                     'name': '(5S,9S,10S,13E)-labda-7,13-dien-15-yl '
                                             'diphosphate',
                                     'reason': 'Molecular weight too low for '
                                               'phosphoinositide'},
                                 {   'smiles': 'CC1(C)CC[C@@]2(CC[C@]3(C)[C@H](C[C@@H](O)[C@@H]4[C@@]5(C)CC[C@@H](O)C(C)(C)[C@@H]5CC[C@@]34C)C2=C1)C(O)=O',
                                     'name': 'fatsicarpain E',
                                     'reason': 'Molecular weight too low for '
                                               'phosphoinositide'},
                                 {   'smiles': 'C1CC1C#CC2=CC=C(C=C2)[C@H]3[C@H](N([C@@H]3C#N)C(=O)CC4=CC=CC=N4)CO',
                                     'name': '(2S,3R,4S)-3-[4-(2-cyclopropylethynyl)phenyl]-4-(hydroxymethyl)-1-[1-oxo-2-(2-pyridinyl)ethyl]-2-azetidinecarbonitrile',
                                     'reason': 'Molecular weight too low for '
                                               'phosphoinositide'}],
    'sample_false_negatives': [   {   'smiles': '[C@@H]1([C@@H]([C@@H](O)[C@H]([C@H]([C@@H]1O)OP(=O)(OCOC(=O)CCC)OCOC(=O)CCC)O)OP(=O)(OCOC(=O)CCC)OCOC(=O)CCC)OP(=O)(OCOC(=O)CCC)OCOC(=O)CCC',
                                      'name': 'D-myo-Ins(1,4,5)P3 '
                                              'hexakis(butyryloxymethyl) ester',
                                      'reason': 'No glycerol backbone found'}],
    'attempt': 1,
    'reasoning': 'The previous code had a good foundation but missed some key '
                 'aspects of phosphoinositide classification, leading to both '
                 "false positives and false negatives. Let's analyze the "
                 'issues and improve the code:\n'
                 '\n'
                 '1. **False Positives**: The main issue was that the code was '
                 'too permissive in accepting molecules that had the basic '
                 'structure (glycerol backbone, fatty acids, phosphate, '
                 "inositol) but weren't actually phosphorylated on the "
                 'inositol ring. This led to misclassification of regular '
                 'phosphatidylinositols as phosphoinositides.\n'
                 '\n'
                 '2. **False Negatives**: The code missed some valid '
                 'phosphoinositides because:\n'
                 '   - The inositol pattern was too strict (required exact '
                 'stereochemistry)\n'
                 '   - The phosphate attachment pattern was too specific\n'
                 "   - It didn't account for different phosphorylation "
                 'patterns on the inositol ring\n'
                 '\n'
                 '3. **Improvements**:\n'
                 '   - Make inositol pattern more flexible (ignore '
                 'stereochemistry)\n'
                 '   - Better detection of phosphate groups on inositol\n'
                 '   - Add checks for minimum number of phosphate groups\n'
                 '   - Add molecular weight and element count checks\n'
                 '   - Improve pattern matching for fatty acid chains\n'
                 '\n'
                 "Here's the improved code:",
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 26,
    'num_false_positives': 15,
    'num_true_negatives': 142258,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.6341463414634146,
    'recall': 0.9629629629629629,
    'f1': 0.7647058823529412,
    'accuracy': 0.9998875614898103,
    'negative_predictive_value': 0.9999929705677673}