"""
Classifies: CHEBI:17517 phosphatidylglycerol
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_phosphatidylglycerol(smiles: str):
    """
    Determines if a molecule is a phosphatidylglycerol based on its SMILES string.
    A phosphatidylglycerol is a glycerol backbone with two fatty acid chains and a
    phosphoglycerol group attached.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a phosphatidylglycerol, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
    
    # Check for the phosphatidylglycerol core structure in one SMARTS pattern
    # This pattern matches the glycerol with two ester groups, a phosphate, and another glycerol.
    # [CH2][CH]([CH2]O[P](=O)(O)-O[CH2][CH](O)[CH2]O)
    pg_core_pattern = Chem.MolFromSmarts("[CH2X4][CHX4]([CH2X4][OX2][P](=[OX1])([OX2])[OX2][CH2X4][CHX4]([OX2])[CH2X4][OX2])")
    if not mol.HasSubstructMatch(pg_core_pattern):
        return False, "Phosphatidylglycerol core not found"

    # Check for two fatty acid chains (long carbon chains attached to esters)
    fatty_acid_pattern = Chem.MolFromSmarts("[CX4,CX3]~[CX4,CX3]~[CX4,CX3]~[CX4,CX3]")
    ester_pattern = Chem.MolFromSmarts("[CX3](=[OX1])[OX2][CX4]")
    ester_matches = mol.GetSubstructMatches(ester_pattern)
    fatty_acid_matches = mol.GetSubstructMatches(fatty_acid_pattern)
    if len(ester_matches) < 2 or len(fatty_acid_matches) < 2:
      return False, f"Must have at least 2 ester groups and 2 fatty acid chains"

    #Check rotatable bonds
    n_rotatable = rdMolDescriptors.CalcNumRotatableBonds(mol)
    if n_rotatable < 8 : #Reduced threshold to 8 to accommodate shorter chains
        return False, "Chains too short to be fatty acids"

    # Check molecular weight - PGs are typically >500 Da, but reducing to allow smaller PGs
    mol_wt = rdMolDescriptors.CalcExactMolWt(mol)
    if mol_wt < 400:
        return False, "Molecular weight too low for phosphatidylglycerol"
    

    # Count phosphorus
    p_count = sum(1 for atom in mol.GetAtoms() if atom.GetAtomicNum() == 15)
    if p_count < 1:
        return False, "Must have at least one phosphorus"

    return True, "Contains glycerol backbone with 2 fatty acid chains and a phosphoglycerol group"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:17517',
                          'name': 'phosphatidylglycerol',
                          'definition': 'A glycerophosphoglycerol that is '
                                        'glycerol in which the hydrogen of one '
                                        'of the primary hydroxy groups has '
                                        'been replaced by a phosphatidyl '
                                        'group.',
                          'parents': ['CHEBI:24360'],
                          'xrefs': ['KEGG:C00344'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 39,
                           'log_lines_of_code': 3.6635616461296463,
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
                                                 2,
                                                 1,
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
                                                 1,
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
                                                 1,
                                                 0,
                                                 1,
                                                 1,
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
                                                 'MolFromSmarts',
                                                 'GetAtomicNum',
                                                 'CalcExactMolWt',
                                                 'GetAtoms',
                                                 'HasSubstructMatch',
                                                 'MolFromSmiles',
                                                 'CalcNumRotatableBonds'],
                           'methods_called_count': 8,
                           'smarts_strings': [   '[CX4,CX3]~[CX4,CX3]~[CX4,CX3]~[CX4,CX3]',
                                                 '[CH2X4][CHX4]([CH2X4][OX2][P](=[OX1])([OX2])[OX2][CH2X4][CHX4]([OX2])[CH2X4][OX2])',
                                                 '[CX3](=[OX1])[OX2][CX4]'],
                           'smarts_strings_count': 3,
                           'defs': ['is_phosphatidylglycerol(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "Phosphatidylglycerol core '
                                          'not found"',
                                          'False, f"Must have at least 2 ester '
                                          'groups and 2 fatty acid chains"',
                                          'False, "Chains too short to be '
                                          'fatty acids"',
                                          'False, "Molecular weight too low '
                                          'for phosphatidylglycerol"',
                                          'False, "Must have at least one '
                                          'phosphorus"',
                                          'True, "Contains glycerol backbone '
                                          'with 2 fatty acid chains and a '
                                          'phosphoglycerol group"'],
                           'returns_count': 7,
                           'complexity': 4.332712329225929},
    'message': '\n'
               'Attempt failed: F1 score of 0.2410351201478743 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: '
               'CCCCCCCCCCCCCCCC(=O)OC[C@H](COP(O)(=O)OC[C@H](O)COP(O)(=O)OC[C@@H](COC(=O)CCCCCCCCCCCN)OC(=O)CCCCCCCCCCCCCCC)OC(=O)CCCCCCCCCCCCCCC '
               'NAME: 12-aminolauroyl tripalmitoyl cardiolipin REASON: CORRECT '
               'Contains glycerol backbone with 2 fatty acid chains and a '
               'phosphoglycerol group\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCC(=O)OCC(COP(O)(=O)OCC(O)CO)OC(=O)CCCCCCCCCCCCCCCCC '
               'NAME: distearoyl phosphatidylglycerol REASON: CORRECT Contains '
               'glycerol backbone with 2 fatty acid chains and a '
               'phosphoglycerol group\n'
               ' * SMILES: '
               'C([C@@](COC(CCCCCCC/C=C\\CCCCCC)=O)(OC(CCCCCCC/C=C\\CCCCCCCC)=O)[H])OP(=O)(O)OC[C@@](CO)([H])O '
               'NAME: PG(16:1(9Z)/18:1(9Z)) REASON: CORRECT Contains glycerol '
               'backbone with 2 fatty acid chains and a phosphoglycerol group\n'
               ' * SMILES: '
               'P(OC[C@H](OC(=O)CCC[C@@H](O)/C=C\\C=C\\C=C\\[C@@H](O)C/C=C\\CCCCC)COC(=O)CCCCCCCCCCCCCCCCC)(OC[C@@H](O)CO)(O)=O '
               'NAME: PG(18:0/20:4(6Z,8E,10E,14Z)-2OH(5S,12R)) REASON: CORRECT '
               'Contains glycerol backbone with 2 fatty acid chains and a '
               'phosphoglycerol group\n'
               ' * SMILES: '
               'P(OC[C@H](OC(=O)CCCCCCC/C=C\\C/C=C\\CCCCC)COC(=O)CCCCCCC/C=C\\CCCCCCC)(OC[C@@H](O)CO)(O)=O '
               'NAME: PG(17:1(9Z)/18:2(9Z,12Z)) REASON: CORRECT Contains '
               'glycerol backbone with 2 fatty acid chains and a '
               'phosphoglycerol group\n'
               ' * SMILES: '
               'P(OC[C@H](OC(=O)CCCCCCCCCCCCCCCCCCCC)COC(=O)CCCCCCCCCCC/C=C\\C/C=C\\CCCCC)(OC[C@@H](O)CO)(O)=O '
               'NAME: PG(22:2(13Z,16Z)/21:0) REASON: CORRECT Contains glycerol '
               'backbone with 2 fatty acid chains and a phosphoglycerol group\n'
               ' * SMILES: '
               'P(OC[C@H](OC(=O)CCCCCCCCCCCCCCCCC)COC(=O)CCCCCCCCCCCCCCCCC)(OC[C@@H](O)COP(OC[C@H](OC(=O)CCCCCCCCC/C=C\\CCCCCC)COC(=O)CCCCCCCCCCCCCCC)(O)=O)(O)=O '
               'NAME: CL(16:0/18:1(11Z)/18:0/18:0) REASON: CORRECT Contains '
               'glycerol backbone with 2 fatty acid chains and a '
               'phosphoglycerol group\n'
               ' * SMILES: '
               'P(OC[C@H](OC(=O)CCCC(O)C(O)C/C=C\\C/C=C\\C/C=C\\CCCCC)COC(=O)CCCCCCCCCCCCCCCCCCCCC(C)C)(OC[C@@H](O)CO)(O)=O '
               'NAME: PG(i-24:0/20:3(8Z,11Z,14Z)-2OH(5,6)) REASON: CORRECT '
               'Contains glycerol backbone with 2 fatty acid chains and a '
               'phosphoglycerol group\n'
               ' * SMILES: '
               'P(OC[C@H](OC(=O)CCCCCCCCCCCCCCCCC)COC(=O)CCCCCCCCCCCC)(OC[C@@H](O)CO)(O)=O '
               'NAME: PG(13:0/18:0) REASON: CORRECT Contains glycerol backbone '
               'with 2 fatty acid chains and a phosphoglycerol group\n'
               ' * SMILES: '
               'P(OC[C@H](OC(=O)CCCCCCC/C=C\\CCCCCC)COC(=O)CCCC/C=C\\C/C=C\\C/C=C\\CCCCC)(OC[C@@H](O)CO)(O)=O '
               'NAME: PG(18:3(6Z,9Z,12Z)/16:1(9Z)) REASON: CORRECT Contains '
               'glycerol backbone with 2 fatty acid chains and a '
               'phosphoglycerol group\n'
               ' * SMILES: '
               'C([C@@](COC(CCCCCCCCCCCCCCCCC)=O)(OC(CCCCCCCCC/C=C\\CCCCCC)=O)[H])OP(=O)(O)OC[C@@](CO)([H])O '
               'NAME: PG(18:0/18:1(11Z)) REASON: CORRECT Contains glycerol '
               'backbone with 2 fatty acid chains and a phosphoglycerol group\n'
               ' * SMILES: '
               'P(OC[C@H](OC(=O)CCCCCCCCCCCCC)COC(=O)CCCCCCC/C=C\\C/C=C\\CCCCC)(OC[C@@H](O)CO)(O)=O '
               'NAME: PG(18:2(9Z,12Z)/14:0) REASON: CORRECT Contains glycerol '
               'backbone with 2 fatty acid chains and a phosphoglycerol group\n'
               ' * SMILES: '
               'P(OC[C@H](OC(=O)CCCCCCCCCCCCC)COC(=O)CCCCCCCCCCCCCCCCC)(OC[C@@H](O)CO)(O)=O '
               'NAME: PG(18:0/14:0) REASON: CORRECT Contains glycerol backbone '
               'with 2 fatty acid chains and a phosphoglycerol group\n'
               ' * SMILES: '
               'P(OC[C@H](OC(=O)CCCCCCC/C=C\\C/C=C\\CCCC)COC(=O)CCCCCCC/C=C\\CCCCCCC)(OC[C@@H](O)CO)(O)=O '
               'NAME: PG(17:1(9Z)/17:2(9Z,12Z)) REASON: CORRECT Contains '
               'glycerol backbone with 2 fatty acid chains and a '
               'phosphoglycerol group\n'
               ' * SMILES: '
               'C([C@@](COC(CCCC/C=C\\C/C=C\\C/C=C\\CCCCC)=O)(OC(CCCCC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)=O)[H])OP(=O)(O)OC[C@@](CO)([H])O '
               'NAME: PG(18:3(6Z,9Z,12Z)/22:5(7Z,10Z,13Z,16Z,19Z)) REASON: '
               'CORRECT Contains glycerol backbone with 2 fatty acid chains '
               'and a phosphoglycerol group\n'
               ' * SMILES: '
               'C([C@@](COC(CCCCCCC/C=C\\CCCCCCCC)=O)(OC(CCCCC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)=O)[H])OP(=O)(O)OC[C@@](CO)([H])O '
               'NAME: PG(18:1(9Z)/22:5(7Z,10Z,13Z,16Z,19Z)) REASON: CORRECT '
               'Contains glycerol backbone with 2 fatty acid chains and a '
               'phosphoglycerol group\n'
               ' * SMILES: '
               'C([C@@](COC(CCCCCCCCC/C=C\\CCCCCC)=O)(OC(CC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)=O)[H])OP(=O)(O)OC[C@@](CO)([H])O '
               'NAME: PG(18:1(11Z)/22:6(4Z,7Z,10Z,13Z,16Z,19Z)) REASON: '
               'CORRECT Contains glycerol backbone with 2 fatty acid chains '
               'and a phosphoglycerol group\n'
               ' * SMILES: '
               'P(OC[C@H](OC(=O)CCCCCCCCCCCCCCCCC)COC(=O)CCCCCCC/C=C\\C/C=C\\C/C=C\\CC)(OC[C@@H](O)COP(O)(O)=O)(O)=O '
               'NAME: '
               '[(2S)-2-Hydroxy-3-({hydroxy[(2R)-3-[(9Z,12Z,15Z)-octadeca-9,12,15-trienoyloxy]-2-(octadecanoyloxy)propoxy]phosphoryl}oxy)propoxy]phosphonic '
               'acid REASON: CORRECT Contains glycerol backbone with 2 fatty '
               'acid chains and a phosphoglycerol group\n'
               ' * SMILES: '
               'P(OC[C@H](OC(=O)CCCCCCCCC/C=C\\CCCCCCCC)COC(=O)CCCCCCC/C=C\\CCCC)(OC[C@@H](O)CO)(O)=O '
               'NAME: PG(14:1(9Z)/20:1(11Z)) REASON: CORRECT Contains glycerol '
               'backbone with 2 fatty acid chains and a phosphoglycerol group\n'
               ' * SMILES: '
               'P(OC[C@H](OC(=O)CC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)COC(=O)CCCC/C=C\\C/C=C\\C/C=C\\CCCCC)(OC[C@@H](O)COP(O)(O)=O)(O)=O '
               'NAME: PGP(18:3(6Z,9Z,12Z)/22:6(4Z,7Z,10Z,13Z,16Z,19Z)) REASON: '
               'CORRECT Contains glycerol backbone with 2 fatty acid chains '
               'and a phosphoglycerol group\n'
               ' * SMILES: '
               'P(OC[C@H](OC(=O)CCCCCCCCCCCCCCCCC)COC(=O)CCC/C=C\\C/C=C\\C/C=C\\C/C=C\\CCCCC)(OC[C@@H](O)COP(OC[C@H](OC(=O)CCCCCCC/C=C\\CCCCCCCC)COC(=O)CCCCCCC/C=C\\CCCCCCCC)(O)=O)(O)=O '
               "NAME: CL(1'-[20:4(5Z,8Z,11Z,14Z)/18:0],3'-[18:1(9Z)/18:1(9Z)]) "
               'REASON: CORRECT Contains glycerol backbone with 2 fatty acid '
               'chains and a phosphoglycerol group\n'
               ' * SMILES: '
               'P(OC[C@H](OC(=O)CCCCCCCCCCC)COC(=O)CCCCCCCCC/C=C\\C/C=C\\CCCCC)(OC[C@@H](O)CO)(O)=O '
               'NAME: PG(20:2(11Z,14Z)/12:0) REASON: CORRECT Contains glycerol '
               'backbone with 2 fatty acid chains and a phosphoglycerol group\n'
               ' * SMILES: '
               'P(OC[C@H](OC(=O)CCCCCCCCC(C)C)COC(=O)CCCCCCCCC(CC)C)(OC[C@@H](O)COP(O)(O)=O)(O)=O '
               'NAME: PGP(a-13:0/i-12:0) REASON: CORRECT Contains glycerol '
               'backbone with 2 fatty acid chains and a phosphoglycerol group\n'
               ' * SMILES: '
               'P(OC([C@](OC(=O)CCCCCCC/C=C\\CCCCCC)(C(OC(=O)CCCCCCCCCCCCCCCC)([2H])[2H])[2H])([2H])[2H])(OCC(O)CO)(O)=O '
               'NAME: '
               '[(2R)-1,1,2,3,3-Pentadeuterio-3-[2,3-dihydroxypropoxy(hydroxy)phosphoryl]oxy-2-[(Z)-hexadec-9-enoyl]oxypropyl] '
               'heptadecanoate REASON: CORRECT Contains glycerol backbone with '
               '2 fatty acid chains and a phosphoglycerol group\n'
               ' * SMILES: '
               'P(OC[C@H](OC(=O)CCCCCCCCCCCCCC)COC(=O)CCCCCCCCCCCCCCCCCC)(OC[C@@H](O)CO)(O)=O '
               'NAME: PG(19:0/15:0) REASON: CORRECT Contains glycerol backbone '
               'with 2 fatty acid chains and a phosphoglycerol group\n'
               'False positives: SMILES: '
               'P(OC[C@H](OC(=O)CC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)COC(=O)CCCCCCCCCCCCCCCCCC)(O)(O)=O '
               'NAME: PA(19:0/22:6(4Z,7Z,10Z,13Z,16Z,19Z)) REASON: WRONGLY '
               'CLASSIFIED Contains glycerol backbone with 2 fatty acid chains '
               'and a phosphoglycerol group\n'
               ' * SMILES: '
               'P(OC[C@H](OC(=O)CCCCCCCCC/C=C\\CCCCCCCCCC)COC(=O)CCCCCCCCCCCC)(OCCN)(O)=O '
               'NAME: PE(13:0/22:1(11Z)) REASON: WRONGLY CLASSIFIED Contains '
               'glycerol backbone with 2 fatty acid chains and a '
               'phosphoglycerol group\n'
               ' * SMILES: '
               '[C@@H]1(C(C(C([C@H](C1O)O)O)O)O)OP(OC[C@@](COC(CCCCCCC/C=C\\C/C=C\\CCCCC)=O)(OC(CCCCCCCCC/C=C\\CCCCCCCC)=O)[H])(O)=O '
               'NAME: PI(18:2(9Z,12Z)/20:1(11Z)) REASON: WRONGLY CLASSIFIED '
               'Contains glycerol backbone with 2 fatty acid chains and a '
               'phosphoglycerol group\n'
               ' * SMILES: '
               'P(OC[C@H](OC(=O)CCCCCCCCCCCCCCCCCCC)COC(=O)CCCCCCCCCCCCC)(O)(O)=O '
               'NAME: PA(14:0/20:0) REASON: WRONGLY CLASSIFIED Contains '
               'glycerol backbone with 2 fatty acid chains and a '
               'phosphoglycerol group\n'
               ' * SMILES: '
               'P(O[C@@H]1C(O)[C@H](OP(O)(O)=O)C(OP(O)(O)=O)C(O)C1O)(OC[C@H](OC(=O)CCCCCCCCCCCCCCC)COC(=O)CCCCCCCCCCCCCCC)(O)=O '
               'NAME: PIP2(16:0/16:0) REASON: WRONGLY CLASSIFIED Contains '
               'glycerol backbone with 2 fatty acid chains and a '
               'phosphoglycerol group\n'
               ' * SMILES: '
               'P(OC[C@H](OC(=O)CCCCCCC/C=C\\CCCC)COC(=O)CCCCCCCCC/C=C\\CCCCCCCC)(OC[C@H](N)C(O)=O)(O)=O '
               'NAME: PS(20:1(11Z)/14:1(9Z)) REASON: WRONGLY CLASSIFIED '
               'Contains glycerol backbone with 2 fatty acid chains and a '
               'phosphoglycerol group\n'
               ' * SMILES: '
               '[C@@H]1(C(C(C([C@H](C1O)O)O)O)O)OP(OC[C@@](COC(CCCCCCCCC/C=C\\CCCCCC)=O)(OC(CCCCCC/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)=O)[H])(O)=O '
               'NAME: PI(18:1(11Z)/20:4(8Z,11Z,14Z,17Z)) REASON: WRONGLY '
               'CLASSIFIED Contains glycerol backbone with 2 fatty acid chains '
               'and a phosphoglycerol group\n'
               ' * SMILES: '
               'P(OC[C@H](OC(=O)CCCCCCCCC/C=C\\C/C=C\\CCCCC)COC(=O)CCCCCCC/C=C\\CCCCCCCC)(OCCN)(O)=O '
               'NAME: PE(18:1(9Z)/20:2(11Z,14Z)) REASON: WRONGLY CLASSIFIED '
               'Contains glycerol backbone with 2 fatty acid chains and a '
               'phosphoglycerol group\n'
               ' * SMILES: '
               '[H][C@](COP(OC[C@@](COC(CCCCCCC/C=C\\CCCCCC)=O)(OC(CCCCCC/C=C\\C/C=C\\C/C=C\\CCCCC)=O)[H])(=O)O)(C(O)=O)N '
               'NAME: PS(16:1(9Z)/20:3(8Z,11Z,14Z)) REASON: WRONGLY CLASSIFIED '
               'Contains glycerol backbone with 2 fatty acid chains and a '
               'phosphoglycerol group\n'
               ' * SMILES: '
               'P(OC[C@H](OC(=O)CCC/C=C\\C/C=C\\C/C=C\\CCCCCCCC)COC(=O)CCCCCCC/C=C\\CCCCCCCC)(OCCN)(O)=O '
               'NAME: PE(18:1(9Z)/20:3(5Z,8Z,11Z)) REASON: WRONGLY CLASSIFIED '
               'Contains glycerol backbone with 2 fatty acid chains and a '
               'phosphoglycerol group\n'
               ' * SMILES: '
               'P(OC[C@H](OC(=O)CCCCCCC/C=C\\C/C=C\\CCCC)COC(=O)CCCCCCCCCCCCCCC)(OCCN)(O)=O '
               'NAME: PE(16:0/17:2(9Z,12Z)) REASON: WRONGLY CLASSIFIED '
               'Contains glycerol backbone with 2 fatty acid chains and a '
               'phosphoglycerol group\n'
               ' * SMILES: '
               'C(C/C=C\\CCCCCCCC)CCCCCCCC(O[C@@H](COP(O[C@H]1[C@@H]([C@H]([C@@H]([C@H]([C@H]1O)O)O)O)O)(=O)O)COC(CCCCCC/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)=O)=O '
               'NAME: '
               '1-[(8Z,11Z,14Z,17Z)-icosatetraenoyl]-2-[(11Z)-icosenoyl]-sn-glycero-3-phospho-1D-myo-inositol '
               'REASON: WRONGLY CLASSIFIED Contains glycerol backbone with 2 '
               'fatty acid chains and a phosphoglycerol group\n'
               ' * SMILES: '
               'P(OC[C@H](OC(=O)CCC/C=C\\C[C@H]1[C@@H](O)CC(O[C@@H]1/C=C/[C@@H](O)CCCCC)O)COC(=O)CCCCCCCCC/C=C\\CCCCCCCC)(OC[C@@H](O)CO)(O)=O '
               'NAME: PG(20:1(11Z)/TXB2) REASON: WRONGLY CLASSIFIED Contains '
               'glycerol backbone with 2 fatty acid chains and a '
               'phosphoglycerol group\n'
               ' * SMILES: '
               'P(OC[C@H](OC(=O)CCCCCCC/C=C\\CCCCCCCC)COC(=O)CCCCCCCCCCCCCC)(O)(O)=O '
               'NAME: PA(15:0/18:1(9Z)) REASON: WRONGLY CLASSIFIED Contains '
               'glycerol backbone with 2 fatty acid chains and a '
               'phosphoglycerol group\n'
               ' * SMILES: '
               'P1(O[C@H]2[C@H](O)[C@@H](O)[C@H](O)[C@H]([C@@H](O)C[C@@H](O)[C@@H]([C@@H](O)[C@H]2O)/C=C/[C@@H](O)CCCCC)CC=CCCCC(O[C@@H](CO1)COC(=O)CCCCCCCCCCC/C=C\\C/C=C\\CCCCC)=O)(O)=O '
               'NAME: PI(22:2(13Z,16Z)/PGF2alpha) REASON: WRONGLY CLASSIFIED '
               'Contains glycerol backbone with 2 fatty acid chains and a '
               'phosphoglycerol group\n'
               ' * SMILES: '
               'P(OC1C(O)C(O)C(O)[C@@H](O)C1O)(OC[C@H](OC(=O)CCCCCCC/C=C\\C/C=C\\C/C=C\\CC)COC(=O)CCCCCCCCC/C=C\\CCCCCCCCCC)(O)=O '
               'NAME: PI(22:1(11Z)/18:3(9Z,12Z,15Z)) REASON: WRONGLY '
               'CLASSIFIED Contains glycerol backbone with 2 fatty acid chains '
               'and a phosphoglycerol group\n'
               ' * SMILES: '
               'P(OC[C@H](OC(=O)CCCC/C=C\\C/C=C\\C/C=C\\CCCCC)COC(=O)CCCCCCCCCCCCCCCCCCC)(OCCN)(O)=O '
               'NAME: PE(20:0/18:3(6Z,9Z,12Z)) REASON: WRONGLY CLASSIFIED '
               'Contains glycerol backbone with 2 fatty acid chains and a '
               'phosphoglycerol group\n'
               ' * SMILES: '
               'P(OC[C@H](OC(=O)CCCCCCCCCCCCCCCCC)COC(=O)CCCCCCCCCCCCCCCCCCCCC)(O)(O)=O '
               'NAME: PA(22:0/18:0) REASON: WRONGLY CLASSIFIED Contains '
               'glycerol backbone with 2 fatty acid chains and a '
               'phosphoglycerol group\n'
               ' * SMILES: '
               'P(OC[C@H](OC(=O)CCCCCCC/C=C\\CCCCCCCCC)COC(=O)CCCCCCCCCCC)(OCCN)(O)=O '
               'NAME: PE(12:0/19:1(9Z)) REASON: WRONGLY CLASSIFIED Contains '
               'glycerol backbone with 2 fatty acid chains and a '
               'phosphoglycerol group\n'
               ' * SMILES: '
               'P(OC[C@H](OC(=O)CCCCCCC/C=C\\CCCC)COC(=O)CCCCCCCCCCCCC)(OC[C@H](N)C(O)=O)(O)=O '
               'NAME: PS(14:0/14:1(9Z)) REASON: WRONGLY CLASSIFIED Contains '
               'glycerol backbone with 2 fatty acid chains and a '
               'phosphoglycerol group\n'
               ' * SMILES: '
               'CCCCCCCCCCCC(OC(COC(CCCCCCCCCCC)=O)COP(=O)(O)OCCN)=O NAME: '
               '1,2-didodecanoyl-sn-glycero-3-phosphoethanolamine REASON: '
               'WRONGLY CLASSIFIED Contains glycerol backbone with 2 fatty '
               'acid chains and a phosphoglycerol group\n'
               ' * SMILES: '
               'P(OC[C@H](OC(=O)CCCCCCCCCCC(C)C)COC(=O)CCCCCCC)(O)(O)=O NAME: '
               'PA(8:0/i-14:0) REASON: WRONGLY CLASSIFIED Contains glycerol '
               'backbone with 2 fatty acid chains and a phosphoglycerol group\n'
               ' * SMILES: '
               'P(OC1C(O)C(O)C(O)[C@@H](O)C1O)(OC[C@H](OC(=O)CCCCCCC/C=C\\C/C=C\\CCCC)COC(=O)CCCCCCC/C=C\\CCCCCC)(O)=O '
               'NAME: PI(16:1(9Z)/17:2(9Z,12Z)) REASON: WRONGLY CLASSIFIED '
               'Contains glycerol backbone with 2 fatty acid chains and a '
               'phosphoglycerol group\n'
               ' * SMILES: '
               'P(OCC(OC(=O)CCCCCCCCC/C=C\\C/C=C\\CCCCC)COC(=O)CCCCCCC/C=C\\C/C=C\\C/C=C\\CC)(OCCNC)(O)=O '
               'NAME: PE-NMe(18:3(9Z,12Z,15Z)/20:2(11Z,14Z)) REASON: WRONGLY '
               'CLASSIFIED Contains glycerol backbone with 2 fatty acid chains '
               'and a phosphoglycerol group\n'
               ' * SMILES: '
               'P(OC[C@H](OC(=O)CC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)COC(=O)CCCC/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)(OCCN)(O)=O '
               'NAME: PE(18:4(6Z,9Z,12Z,15Z)/22:6(4Z,7Z,10Z,13Z,16Z,19Z)) '
               'REASON: WRONGLY CLASSIFIED Contains glycerol backbone with 2 '
               'fatty acid chains and a phosphoglycerol group\n'
               'False negatives: SMILES: '
               'P(OC[C@H](OC(=O)CCCCCCC)COC(=O)CCCCCCC)(OC[C@@H](O)CO)(O)=O '
               'NAME: PG(8:0/8:0) REASON: MISSED Molecular weight too low for '
               'phosphatidylglycerol\n'
               ' * SMILES: '
               'P(OC[C@H](OC(=O)C\\C=C\\CCCCCCCCCCCC)COC(=O)CCCCCCCCCCCCCCC)(OC[C@@H](O)CO)([O-])=O '
               'NAME: 16:0-t16:1-PG REASON: MISSED Found 0 phosphoglycerol '
               'groups, expected at least 1\n'
               ' * SMILES: '
               'CCCCCC(=O)OC[C@H](COP(O)(=O)OC[C@@H](O)CO)OC(=O)CCCCC NAME: '
               "1,2-dihexanoyl-sn-glycero-3-phospho-(1'-sn-glycerol) REASON: "
               'MISSED Molecular weight too low for phosphatidylglycerol\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'CCN1N=C(N=N1)C2=CC=CC=C2NC(=O)C3=CC=C(C=C3)N4C=NN=N4',
                                     'name': 'N-[2-(2-ethyl-5-tetrazolyl)phenyl]-4-(1-tetrazolyl)benzamide',
                                     'reason': 'Phosphatidylglycerol core not '
                                               'found'},
                                 {   'smiles': 'CCS(=O)(=O)N1CC2(C1)[C@@H]([C@@H](N2C(=O)C3CCCC3)CO)C4=CC=C(C=C4)C=CC',
                                     'name': 'LSM-38092',
                                     'reason': 'Phosphatidylglycerol core not '
                                               'found'},
                                 {   'smiles': 'O=C/1N/C(/C(=O)N\\C1=C\\C2=CC=CC=C2)=C\\C=3N=CNC3C(C=C)(C)C',
                                     'name': 'DeltaPLH',
                                     'reason': 'Phosphatidylglycerol core not '
                                               'found'},
                                 {   'smiles': 'C1CCN(CC1)C(=O)C[C@H]2C[C@@H]3[C@H]([C@@H](O2)CO)OC4=C3C=C(C=C4)NC(=O)CC5CC5',
                                     'name': 'N-[(1S,3R,4aS,9aR)-1-(hydroxymethyl)-3-[2-oxo-2-(1-piperidinyl)ethyl]-3,4,4a,9a-tetrahydro-1H-pyrano[3,4-b]benzofuran-6-yl]-2-cyclopropylacetamide',
                                     'reason': 'Phosphatidylglycerol core not '
                                               'found'},
                                 {   'smiles': 'C[C@H]1C[C@@]2(OC(=O)c3ccccc3)[C@H]([C@H]1OC(C)=O)[C@@H](O)\\C(C)=C/C[C@H]1[C@@H](\\C=C(C)\\C2=O)C1(C)C',
                                     'name': '(-)-(6Z,12E,2S,3S,4R,5R,9S,11S,15R)-3-acetoxy-15-benzoyloxylathyra-6,12-dien-5-ol-14-one',
                                     'reason': 'Phosphatidylglycerol core not '
                                               'found'},
                                 {   'smiles': 'O=C1C(O)=CC=2O[C@]3([C@H](O)C[C@@H]4[C@](OC=5C=C(O)C(C=C(C5C4)C)=O)(CC=CC(C[C@H]3CC2C(=C1)C)(C)C)C)C',
                                     'name': 'Eupenifeldin',
                                     'reason': 'Phosphatidylglycerol core not '
                                               'found'},
                                 {   'smiles': 'O1[C@@H](O[C@@H]2[C@@H](OC[C@H]3O[C@@H](O[C@H]4[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]4CO)O[C@H]5[C@H](O)[C@@H](NC(=O)C)C(O[C@@H]5CO[C@@H]6O[C@H]([C@@H](O)[C@@H](O)[C@@H]6O)C)O)[C@@H](O)[C@@H](O[C@H]7O[C@@H]([C@@H](O)[C@H](O)[C@@H]7O[C@@H]8O[C@@H]([C@@H](O[C@@H]9O[C@@H]([C@H](O)[C@H](O)[C@H]9NC(=O)C)CO)[C@H](O)[C@H]8NC(=O)C)CO)CO)[C@@H]3O)O[C@@H]([C@@H](O)[C@@H]2O)CO)[C@H](NC(=O)C)[C@@H](O[C@@H]%10O[C@H]([C@@H](O)[C@@H](O)[C@@H]%10O)C)[C@H](O[C@@H]%11O[C@@H]([C@H](O)[C@H](O)[C@H]%11NC(=O)C)CO)[C@H]1CO',
                                     'name': 'N-[(3R,4R,5S,6R)-5-[(2S,3R,4R,5S,6R)-3-Acetamido-5-[(2S,3S,4S,5R,6R)-4-[(2R,3S,4S,5S,6R)-3-[(2S,3R,4R,5S,6R)-3-acetamido-5-[(2S,3R,4R,5R,6R)-3-acetamido-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-6-[[(2S,3S,4S,5S,6R)-3-[(2S,3R,4R,5S,6R)-3-acetamido-5-[(2S,3R,4R,5R,6R)-3-acetamido-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-6-(hydroxymethyl)-4-[(2R,3S,4R,5S,6S)-3,4,5-trihydroxy-6-methyloxan-2-yl]oxyoxan-2-yl]oxy-4,5-dihydroxy-6-(hydroxymethyl)oxan-2-yl]oxymethyl]-3,5-dihydroxyoxan-2-yl]oxy-4-hydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-2,4-dihydroxy-6-[[(2R,3S,4R,5S,6S)-3,4,5-trihydroxy-6-methyloxan-2-yl]oxymethyl]oxan-3-yl]acetamide',
                                     'reason': 'Phosphatidylglycerol core not '
                                               'found'},
                                 {   'smiles': 'CN1C[C@@H]2C[C@H](Cn3c2cccc3=O)[C@H]1CC=C',
                                     'name': 'Tinctorine',
                                     'reason': 'Phosphatidylglycerol core not '
                                               'found'},
                                 {   'smiles': 'CCC1=C2COC(CC2=C3C(=C(OC3=N1)C(=O)C4=CC=CC=C4)N)(C)C',
                                     'name': 'LSM-4563',
                                     'reason': 'Phosphatidylglycerol core not '
                                               'found'},
                                 {   'smiles': 'CN1CCN(CC1)C(=O)C[C@@H]2CC[C@H]3[C@H](O2)COC[C@@H](CN3C(=O)NC4=CC5=C(C=C4)OCO5)O',
                                     'name': '(3R,6aS,8S,10aS)-N-(1,3-benzodioxol-5-yl)-3-hydroxy-8-[2-(4-methyl-1-piperazinyl)-2-oxoethyl]-3,4,6,6a,8,9,10,10a-octahydro-2H-pyrano[2,3-c][1,5]oxazocine-1-carboxamide',
                                     'reason': 'Phosphatidylglycerol core not '
                                               'found'}],
    'sample_false_negatives': [   {   'smiles': 'P(OC[C@H](OC(=O)C\\C=C\\CCCCCCCCCCCC)COC(=O)CCCCCCCCCCCCCCC)(OC[C@@H](O)CO)([O-])=O',
                                      'name': '16:0-t16:1-PG',
                                      'reason': 'Phosphatidylglycerol core not '
                                                'found'},
                                  {   'smiles': 'P(OC[C@H](OC(=O)CCCCC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)COC(=O)CCCCCCCCCCCCCCCCCCC)(OCCN)(O)=O',
                                      'name': 'PE(20:0/22:5(7Z,10Z,13Z,16Z,19Z))',
                                      'reason': 'Phosphatidylglycerol core not '
                                                'found'}],
    'attempt': 2,
    'reasoning': "Okay, let's analyze the previous attempt and the error "
                 'report to figure out how to improve the '
                 '`is_phosphatidylglycerol` function.\n'
                 '\n'
                 '**Reasoning:**\n'
                 '\n'
                 '1.  **False Positives:** The biggest problem is the large '
                 'number of false positives. This suggests that the current '
                 'criteria are too broad. Many molecules are being incorrectly '
                 'classified as phosphatidylglycerols. The main issue seems to '
                 'be that the code checks for a glycerol backbone, two esters, '
                 'a phosphoglycerol group and long chains independently. The '
                 "code doesn't verify if the phosphoglycerol is connected "
                 "directly to the glycerol backbone, and it doesn't seem to "
                 'care what else is attached to the phosphate. For example, it '
                 'classifies molecules with a phosphate connected to a diol, '
                 'and a separate glycerol with 2 esters (like a PA) as a PG. '
                 'The phosphate can also be connected to a sugar in PIs, or an '
                 'ethanolamine in PEs.\n'
                 '2.  **False Negatives:**\n'
                 '    *   **Molecular Weight Cutoff:** The molecular weight '
                 'cutoff might be too high, causing some smaller PGs to be '
                 'missed like PG(8:0/8:0).\n'
                 '    *   **Incorrect Phosphoglycerol Pattern:** There might '
                 'be an issue with the SMARTS pattern for the phosphoglycerol '
                 "group. Perhaps it's too strict or not specific enough. In "
                 'the specific failed case with the SMILES: '
                 '`P(OC[C@H](OC(=O)C\\C=C\\CCCCCCCCCCCC)COC(=O)CCCCCCCCCCCCCCC)(OC[C@@H](O)CO)([O-])=O` '
                 'the error report states "Found 0 phosphoglycerol groups, '
                 'expected at least 1". Looking at the SMARTS pattern '
                 '`[OX2][P](=[OX1])([OX2])[OX2][CH2X4][CHX4][CH2X4][OX2]` it '
                 'could be that the negative charge on oxygen is causing the '
                 'pattern match to fail (since [OX2] specifically matches O '
                 'and not O-).\n'
                 '3. **Overall Strategy:** The key is to ensure the '
                 'phosphoglycerol group is *directly* attached to the '
                 '*glycerol* backbone. We need to refine the SMARTS pattern '
                 'matching and possibly relax the molecular weight cut-off. A '
                 'better approach is to look for a specific SMARTS pattern '
                 'that includes all parts of the structure in one match. This '
                 'is the key to reduce false positives.\n'
                 '\n'
                 '**Changes to implement:**\n'
                 '\n'
                 '1.  **Refine the SMARTS pattern:** The core improvement will '
                 'be to look for a single SMARTS pattern that captures the '
                 'entire phosphoglycerol-glycerol core.\n'
                 '2.  **Adjust molecular weight cut-off:** Lower the molecular '
                 'weight threshold to allow for smaller PGs to be detected.\n'
                 '3.  **Relax the oxygen count:** PGs can contain slightly '
                 'different number of oxygens depending on the saturation of '
                 'the fatty acids, so the count is not a reliable criteria.\n'
                 '4.  **Remove unnecessary checks**: Carbon count is not '
                 'specific enough, remove.',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 327,
    'num_false_positives': 31,
    'num_true_negatives': 141940,
    'num_false_negatives': 2,
    'num_negatives': None,
    'precision': 0.9134078212290503,
    'recall': 0.993920972644377,
    'f1': 0.9519650655021834,
    'accuracy': 0.9997680955727336,
    'negative_predictive_value': 0.9999859097377802}