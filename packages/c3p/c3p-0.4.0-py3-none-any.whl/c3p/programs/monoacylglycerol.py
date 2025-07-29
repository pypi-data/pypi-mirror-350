"""
Classifies: CHEBI:17408 monoacylglycerol
"""
"""
Classifies: monoacylglycerol
A glyceride in which any one of the R groups (position not specified) is an acyl group 
while the remaining two R groups can be either H or alkyl groups.
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_monoacylglycerol(smiles: str):
    """
    Determines if a molecule is a monoacylglycerol based on its SMILES string.
    A monoacylglycerol has a glycerol backbone with one fatty acid chain attached via an ester bond.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a monoacylglycerol, False otherwise
        str: Reason for classification
    """
    
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for phosphate groups - exclude phospholipids
    phosphate_pattern = Chem.MolFromSmarts("[PX4]")
    if mol.HasSubstructMatch(phosphate_pattern):
        return False, "Contains phosphate group - not a monoacylglycerol"

    # More comprehensive glycerol backbone patterns
    glycerol_patterns = [
        # Basic pattern with any position ester
        "[OX2,OH1]-[CH2X4]-[CHX4]-[CH2X4]-[OX2,OH1]",
        # 1- or 3-position ester
        "[CX3](=[OX1])[OX2]-[CH2X4]-[CHX4](-[OX2,OH1])-[CH2X4]-[OX2,OH1]",
        # 2-position ester
        "[OX2,OH1]-[CH2X4]-[CHX4](-[OX2][CX3]=[OX1])-[CH2X4]-[OX2,OH1]"
    ]
    
    has_glycerol = False
    for pattern in glycerol_patterns:
        if mol.HasSubstructMatch(Chem.MolFromSmarts(pattern)):
            has_glycerol = True
            break
            
    if not has_glycerol:
        return False, "No glycerol backbone found"

    # Look for exactly one ester group (-O-C(=O)-)
    ester_pattern = Chem.MolFromSmarts("[OX2][CX3](=[OX1])[#6]")
    ester_matches = mol.GetSubstructMatches(ester_pattern)
    if len(ester_matches) != 1:
        return False, f"Found {len(ester_matches)} ester groups, need exactly 1"

    # Count free or alkylated hydroxyl groups
    oh_pattern = Chem.MolFromSmarts("[OX2H1,OX2][CH2X4,CHX4]-[CHX4]-[CH2X4]")
    oh_matches = mol.GetSubstructMatches(oh_pattern)
    if len(oh_matches) < 2:
        return False, "Insufficient free or substituted hydroxyl groups"

    # Verify no other complex modifications
    complex_pattern = Chem.MolFromSmarts("[N,S,P,F,Cl,Br,I]")
    if mol.HasSubstructMatch(complex_pattern):
        return False, "Contains non-standard atoms or groups"

    # Basic element counts
    c_count = sum(1 for atom in mol.GetAtoms() if atom.GetAtomicNum() == 6)
    o_count = sum(1 for atom in mol.GetAtoms() if atom.GetAtomicNum() == 8)
    
    if c_count < 5:
        return False, "Too few carbons for monoacylglycerol"
    if o_count != 4:  # Must have exactly 4 oxygens
        return False, "Must have exactly 4 oxygens (1 ester + 2 hydroxyls)"

    # Check for reasonable molecular weight
    mol_wt = rdMolDescriptors.CalcExactMolWt(mol)
    if mol_wt < 120 or mol_wt > 1000:
        return False, "Molecular weight outside reasonable range for monoacylglycerol"

    # Verify acyl chain connection - multiple patterns to catch all positions
    acyl_patterns = [
        # 1- or 3-position
        "[CX3](=[OX1])[OX2]-[CH2X4]-[CHX4](-[OX2,OH1])-[CH2X4]-[OX2,OH1]",
        # 2-position
        "[OX2,OH1]-[CH2X4]-[CHX4](-[OX2][CX3]=[OX1])-[CH2X4]-[OX2,OH1]",
        # Alternative patterns
        "[CX3](=[OX1])[OX2]-[CH2X4,CHX4]-[CH1X4](-[OX2,OH1])-[CH2X4]-[OX2,OH1]",
        "[OX2,OH1]-[CH2X4]-[CH1X4](-[OX2][CX3]=[OX1])-[CH2X4]-[OX2,OH1]"
    ]
    
    for pattern in acyl_patterns:
        if mol.HasSubstructMatch(Chem.MolFromSmarts(pattern)):
            return True, "Contains glycerol backbone with one acyl group attached via ester bond"

    return False, "Acyl chain not properly connected to glycerol backbone"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:17408',
                          'name': 'monoacylglycerol',
                          'definition': 'A glyceride in which any one of the R '
                                        'groups (position not specified) is an '
                                        'acyl group while the remaining two R '
                                        'groups can be either H or alkyl '
                                        'groups.',
                          'parents': ['CHEBI:47778'],
                          'xrefs': [   'KEGG:C15590',
                                       'MetaCyc:Monoacylglycerols',
                                       'Wikipedia:Monoglyceride'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': None,
    'message': '\n'
               'Attempt failed: F1 score of 0.5035460992907801 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: CCCCCCCCCCCCCCCCCC(=O)OCC(O)CO NAME: '
               'rac-1-monostearoylglycerol REASON: CORRECT Contains glycerol '
               'backbone with one acyl group attached via ester bond\n'
               ' * SMILES: CCCCCCCCCCCCCCCC(=O)OCC(O)CO NAME: '
               'rac-1-monopalmitoylglycerol REASON: CORRECT Contains glycerol '
               'backbone with one acyl group attached via ester bond\n'
               ' * SMILES: O1C(C1C/C=C\\CCCCC)CCCCCCCC(OC[C@@H](O)CO)=O NAME: '
               'MG(18:1(12Z)-O(9S,10R)/0:0/0:0) REASON: CORRECT Contains '
               'glycerol backbone with one acyl group attached via ester bond\n'
               ' * SMILES: '
               '[H][C@@]12CC[C@]3(CC1=C)C=CC(=O)[C@@](C)(CCC(=O)OCC(O)CO)[C@]3([H])C2 '
               'NAME: Platencinic acid glycerol ester REASON: CORRECT Contains '
               'glycerol backbone with one acyl group attached via ester bond\n'
               ' * SMILES: O1C(CCC1CC(=O)C)C(C)C(OCC(O)CO)=O NAME: '
               '2,3-dihydroxypropyl 2-[5-(2-oxopropyl)oxolan-2-yl]propanoate '
               'REASON: CORRECT Contains glycerol backbone with one acyl group '
               'attached via ester bond\n'
               ' * SMILES: CCCCCCCCCCCCCCCC(=O)OC[C@H](O)CO NAME: '
               '3-palmitoyl-sn-glycerol REASON: CORRECT Contains glycerol '
               'backbone with one acyl group attached via ester bond\n'
               ' * SMILES: CC\\C=C/C\\C=C/C\\C=C/CCCCCCCC(=O)OC[C@@H](O)CO '
               'NAME: 1-alpha-linolenoyl-sn-glycerol REASON: CORRECT Contains '
               'glycerol backbone with one acyl group attached via ester bond\n'
               ' * SMILES: CC\\C=C/C\\C=C/C\\C=C/CCCCCCCC(=O)OC[C@H](O)CO '
               'NAME: 3-alpha-linolenoyl-sn-glycerol REASON: CORRECT Contains '
               'glycerol backbone with one acyl group attached via ester bond\n'
               ' * SMILES: CCCCCCCCCCCCCCCCCC(=O)OC[C@@H](O)CO NAME: '
               '1-stearoyl-sn-glycerol REASON: CORRECT Contains glycerol '
               'backbone with one acyl group attached via ester bond\n'
               ' * SMILES: CCCCCCCC(=O)OCC(O)CO NAME: 1-monooctanoylglycerol '
               'REASON: CORRECT Contains glycerol backbone with one acyl group '
               'attached via ester bond\n'
               ' * SMILES: '
               'CCCCC\\C=C/C\\C=C/C\\C=C/C\\C=C/CCCC(=O)OC[C@H](O)CO NAME: '
               '3-arachidonoyl-sn-glycerol REASON: CORRECT Contains glycerol '
               'backbone with one acyl group attached via ester bond\n'
               ' * SMILES: CCCCCCCCCC(=O)OC[C@@H](O)CO NAME: '
               '1-decanoyl-sn-glycerol REASON: CORRECT Contains glycerol '
               'backbone with one acyl group attached via ester bond\n'
               ' * SMILES: O=C1OC(/C(=C/C(=O)OC[C@H](O)CO)/C)=CC(=C1)OC NAME: '
               'Pestalotiopyrone I REASON: CORRECT Contains glycerol backbone '
               'with one acyl group attached via ester bond\n'
               ' * SMILES: CCCCCCCCCC(=O)OCC(O)CO NAME: '
               'rac-1-monodecanoylglycerol REASON: CORRECT Contains glycerol '
               'backbone with one acyl group attached via ester bond\n'
               ' * SMILES: '
               'CCCCC\\C=C/C\\C=C/C\\C=C/C\\C=C/CCCC(=O)OC[C@@H](O)CO NAME: '
               '1-arachidonoyl-sn-glycerol REASON: CORRECT Contains glycerol '
               'backbone with one acyl group attached via ester bond\n'
               ' * SMILES: '
               'C([C@@](COC(CCCC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)=O)(O)[H])O '
               'NAME: MG(24:6(6Z,9Z,12Z,15Z,18Z,21Z)/0:0/0:0) REASON: CORRECT '
               'Contains glycerol backbone with one acyl group attached via '
               'ester bond\n'
               ' * SMILES: CCCCCCCCCCCC(=O)OC[C@@H](O)CO NAME: '
               '1-lauroyl-sn-glycerol REASON: CORRECT Contains glycerol '
               'backbone with one acyl group attached via ester bond\n'
               ' * SMILES: '
               'C(=C\\C/C=C\\C/C=C\\CCCCCC(OCC(CO)O)=O)\\C/C=C\\CCCCC NAME: '
               '1-(all-cis-docosa-7,10,13,16-tetraenoyl)glycerol REASON: '
               'CORRECT Contains glycerol backbone with one acyl group '
               'attached via ester bond\n'
               ' * SMILES: '
               'C(\\C/C=C\\C/C=C\\C/C=C\\CC)=C\\C/C=C\\C/C=C\\CCC(=O)OCC(CO)O '
               'NAME: 1-(all-cis-docosa-4,7,10,13,16,19-hexaenoyl)-glycerol '
               'REASON: CORRECT Contains glycerol backbone with one acyl group '
               'attached via ester bond\n'
               ' * SMILES: CCCCC\\C=C/C\\C=C/CCCCCCCC(=O)OC[C@H](O)CO NAME: '
               '3-linoleoyl-sn-glycerol REASON: CORRECT Contains glycerol '
               'backbone with one acyl group attached via ester bond\n'
               ' * SMILES: '
               'O(C[C@@H](O)CO)C(=O)CC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CCCCC '
               'NAME: MG(22:5(4Z,7Z,10Z,13Z,16Z)/0:0/0:0) REASON: CORRECT '
               'Contains glycerol backbone with one acyl group attached via '
               'ester bond\n'
               ' * SMILES: CC\\C=C/C\\C=C/C\\C=C/CCCCCCCC(=O)OCC(O)CO NAME: '
               '1-alpha-linolenoylglycerol REASON: CORRECT Contains glycerol '
               'backbone with one acyl group attached via ester bond\n'
               ' * SMILES: O(C(=O)CCCCCCCCCCC/C=C\\C/C=C\\CCCCC)C[C@@H](O)CO '
               'NAME: MG(22:2(13Z,16Z)/0:0/0:0) REASON: CORRECT Contains '
               'glycerol backbone with one acyl group attached via ester bond\n'
               ' * SMILES: O(C(=O)CCCCCCCCCCCCCC)C[C@@H](O)CO NAME: '
               'MG(15:0/0:0/0:0) REASON: CORRECT Contains glycerol backbone '
               'with one acyl group attached via ester bond\n'
               ' * SMILES: OC(CO)COC(=O)CCCCCCC/C=C/CCCCCCCC NAME: '
               '1-[(9E)-octadecenoyl]glycerol REASON: CORRECT Contains '
               'glycerol backbone with one acyl group attached via ester bond\n'
               'False positives: SMILES: '
               'P(OC1C(O)C(O)C(O)[C@@H](O)C1O)(OC[C@H](O)COC(=O)CCC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)(O)=O '
               'NAME: PI(20:5(5Z,8Z,11Z,14Z,17Z)/0:0) REASON: WRONGLY '
               'CLASSIFIED Contains glycerol backbone with one acyl group '
               'attached via ester bond\n'
               ' * SMILES: '
               'P(OCCNC1OC(C(O)C(O)C1O)CO)(OC[C@H](O)COC(=O)CCCCCCCCCCCCCCC)(O)=O '
               'NAME: Hexosyl lpe 16:0 REASON: WRONGLY CLASSIFIED Contains '
               'glycerol backbone with one acyl group attached via ester bond\n'
               ' * SMILES: [C@]1([C@@](C(OC1)=O)([C@@H](CCCCCCC)O)[H])(CO)[H] '
               'NAME: SCB2 REASON: WRONGLY CLASSIFIED Contains glycerol '
               'backbone with one acyl group attached via ester bond\n'
               ' * SMILES: O=C(OCC(O)CO)CCCCCCCC/C=C/CC(O)CCCC NAME: '
               'Penicilloitin B REASON: WRONGLY CLASSIFIED Contains glycerol '
               'backbone with one acyl group attached via ester bond\n'
               ' * SMILES: '
               '[H][C@@](COP(O)(=O)OC[C@@](COC(=O)CCCCCCC/C=C\\C/C=C\\CCCCC)(O)[H])(CO)O '
               'NAME: PG(18:2(9Z,12Z)/0:0) REASON: WRONGLY CLASSIFIED Contains '
               'glycerol backbone with one acyl group attached via ester bond\n'
               ' * SMILES: [P@]1(=O)(OC(=C2C(=O)OC[C@@H]2CO1)C)OC NAME: '
               'Cyclophostin REASON: WRONGLY CLASSIFIED Contains glycerol '
               'backbone with one acyl group attached via ester bond\n'
               ' * SMILES: P1(O[C@H](COC(=O)CCCCCCCCCCCCCCCCC)CO1)(O)=O NAME: '
               'CPA(18:0) REASON: WRONGLY CLASSIFIED Contains glycerol '
               'backbone with one acyl group attached via ester bond\n'
               ' * SMILES: '
               'P(OC1C(O)C(O)C(O)[C@@H](O)C1O)(OC[C@H](O)COC(=O)CCCCCCCCCCCCCCCCCCCC)(O)=O '
               'NAME: PI(21:0/0:0) REASON: WRONGLY CLASSIFIED Contains '
               'glycerol backbone with one acyl group attached via ester bond\n'
               ' * SMILES: '
               'P(OC[C@H](O)COC(=O)CCCCCCC/C=C\\CCCCC)(OC[C@@H](O)CO)(O)=O '
               'NAME: PG(15:1(9Z)/0:0) REASON: WRONGLY CLASSIFIED Contains '
               'glycerol backbone with one acyl group attached via ester bond\n'
               ' * SMILES: '
               'P(OC[C@H](O)COC(=O)CCCCC/C=C\\C/C=C\\C/C=C\\C/C=C\\CCCCC)(OC[C@@H](O)CO)(O)=O '
               'NAME: PG(22:4(7Z,10Z,13Z,16Z)/0:0) REASON: WRONGLY CLASSIFIED '
               'Contains glycerol backbone with one acyl group attached via '
               'ester bond\n'
               ' * SMILES: O(CC(O)CO)C(=O)C1=CC(O)=C(O)C(O)=C1 NAME: '
               '1-O-Galloylglycerol REASON: WRONGLY CLASSIFIED Contains '
               'glycerol backbone with one acyl group attached via ester bond\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCC(=O)OC[C@@H](O)COP([O-])(=O)OC[C@@H](O)CO '
               "NAME: 1-octadecanoyl-sn-glycero-3-phospho-(1'-sn-glycerol)(1-) "
               'REASON: WRONGLY CLASSIFIED Contains glycerol backbone with one '
               'acyl group attached via ester bond\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCC(=O)OC[C@@H](O)COP([O-])(=O)O[C@H]1[C@H](O)[C@@H](O)[C@H](O)[C@@H](O)[C@H]1O '
               'NAME: 1-hexadecanoyl-sn--glycero-3-phospho-D-myo-inositol(1-) '
               'REASON: WRONGLY CLASSIFIED Contains glycerol backbone with one '
               'acyl group attached via ester bond\n'
               ' * SMILES: '
               'P(OC1C(O)C(O)C(O)[C@@H](O)C1O)(OC[C@H](O)COC(=O)CCCCCCC/C=C\\CCCCCC)(O)=O '
               'NAME: PI(16:1(9Z)/0:0) REASON: WRONGLY CLASSIFIED Contains '
               'glycerol backbone with one acyl group attached via ester bond\n'
               ' * SMILES: '
               'C(C/C=C\\C/C=C\\C/C=C\\C/C=C\\CCCCC)CC(=O)OC[C@H](COP(O[C@H]1[C@@H]([C@H]([C@@H]([C@H]([C@H]1O)O)O)O)O)(=O)[O-])O '
               'NAME: 1-arachidonoyl-sn-glycero-3-phospho-1D-myo-inositol(1-) '
               'REASON: WRONGLY CLASSIFIED Contains glycerol backbone with one '
               'acyl group attached via ester bond\n'
               ' * SMILES: '
               'P(OC[C@H](O)COC(=O)CCCCCCC/C=C\\C/C=C\\C/C=C\\CC)(OC[C@@H](O)CO)(O)=O '
               'NAME: PG(18:3(9Z,12Z,15Z)/0:0) REASON: WRONGLY CLASSIFIED '
               'Contains glycerol backbone with one acyl group attached via '
               'ester bond\n'
               ' * SMILES: '
               'P1(=O)(OC(=C2C(=O)OC[C@@H]2CO1)C)OCCCCCCCCCCCCCC(C)C NAME: '
               'Cyclipostin P2 REASON: WRONGLY CLASSIFIED Contains glycerol '
               'backbone with one acyl group attached via ester bond\n'
               ' * SMILES: '
               '[C@](COC(=O)CC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)(COP(O[C@H]1C(C(C([C@H](C1O)O)O)O)O)(O)=O)(O)[H] '
               'NAME: '
               "1-(4Z,7Z,10Z,13Z,16Z,19Z-docosahexaenoyl)-glycero-3-phospho-(1'-myo-inositol) "
               'REASON: WRONGLY CLASSIFIED Contains glycerol backbone with one '
               'acyl group attached via ester bond\n'
               ' * SMILES: '
               '[C@](COC(=O)CCCC/C=C\\C/C=C\\C/C=C\\CCCCC)(COP(O[C@H]1C(C(C([C@H](C1O)O)O)O)O)(O)=O)(O)[H] '
               'NAME: PI(18:3(6Z,9Z,12Z)/0:0) REASON: WRONGLY CLASSIFIED '
               'Contains glycerol backbone with one acyl group attached via '
               'ester bond\n'
               ' * SMILES: '
               'P(OC1C(O)C(O)C(O)[C@@H](O)C1O)(OC[C@H](O)COC(=O)CCCCCCCCC/C=C\\C/C=C\\CCCCC)(O)=O '
               'NAME: PI(20:2(11Z,14Z)/0:0) REASON: WRONGLY CLASSIFIED '
               'Contains glycerol backbone with one acyl group attached via '
               'ester bond\n'
               ' * SMILES: '
               'O=C1C2=C(O)C(=C(C)C=C2[C@@H]([C@@H]3C4=C(C(=O)C5=C3C=C(C)C=C5O)C(O)=CC(=C4)OC)C=6C1=C(O)C=C(O)C6)C(=O)OC[C@@H](O)CO '
               "NAME: (10S,10'R)-wentibianthrone A REASON: WRONGLY CLASSIFIED "
               'Contains glycerol backbone with one acyl group attached via '
               'ester bond\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCC(=O)OC[C@@H](O)COP([O-])(=O)OC[C@@H](O)CO '
               "NAME: 1-hexadecanoyl-sn-glycero-3-phospho-(1'-sn-glycerol)(1-) "
               'REASON: WRONGLY CLASSIFIED Contains glycerol backbone with one '
               'acyl group attached via ester bond\n'
               ' * SMILES: '
               'O=C(OCC(O)CO[C@@H]1O[C@@H]([C@@H](O)[C@@H]([C@H]1O)O)CO[C@@H]2O[C@@H]([C@@H](O)[C@@H]([C@H]2O)O)CO)CCCCCCCCCCCCCC '
               'NAME: Ieodoglycolipid REASON: WRONGLY CLASSIFIED Contains '
               'glycerol backbone with one acyl group attached via ester bond\n'
               ' * SMILES: '
               '[P@]1(=O)(OC(=C2C(=O)OC[C@H]2CO1)CCCC)OCCCCCCCCCCCCCC NAME: '
               'Salinipostin B REASON: WRONGLY CLASSIFIED Contains glycerol '
               'backbone with one acyl group attached via ester bond\n'
               ' * SMILES: '
               'CCCCCCCC\\C=C/CCCCCCCC(=O)OC[C@@H](O)COP([O-])(=O)OC[C@@H](O)CO '
               'NAME: '
               "1-(9Z-octadecenoyl)-sn-glycero-3-phospho-(1'-sn-glycerol)(1-) "
               'REASON: WRONGLY CLASSIFIED Contains glycerol backbone with one '
               'acyl group attached via ester bond\n'
               'False negatives: SMILES: CCCCCCCCCC(=O)OC(CO)CO NAME: '
               '2-decanoylglycerol REASON: MISSED Acyl chain not properly '
               'connected to glycerol backbone\n'
               ' * SMILES: '
               'O=C(CCC/C=C\\C/C=C\\C\\C=C/C=C/[C@H](CCCCC)OO)OC(CO)CO NAME: '
               '15(S)-HPETE 2-glyceryl ester REASON: MISSED Acyl chain not '
               'properly connected to glycerol backbone\n'
               ' * SMILES: '
               'O(C(=O)CCCC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CCC)C(CO)CO '
               'NAME: MG(0:0/24:6(6Z,9Z,12Z,15Z,18Z,21Z)/0:0) REASON: MISSED '
               'Acyl chain not properly connected to glycerol backbone\n'
               ' * SMILES: CCCCC\\C=C/C\\C=C/CCCCCCCC(=O)OC(CO)CO NAME: '
               '2-linoleoylglycerol REASON: MISSED Acyl chain not properly '
               'connected to glycerol backbone\n'
               ' * SMILES: O(C(CO)CO)C(=O)CCCC/C=C\\C/C=C\\C/C=C\\C/C=C\\CC '
               'NAME: MG(0:0/18:4(6Z,9Z,12Z,15Z)/0:0) REASON: MISSED Acyl '
               'chain not properly connected to glycerol backbone\n'
               ' * SMILES: CC\\C=C/C\\C=C/C\\C=C/CCCCCCCC(=O)OC(CO)CO NAME: '
               '2-alpha-linolenoylglycerol REASON: MISSED Acyl chain not '
               'properly connected to glycerol backbone\n'
               ' * SMILES: CCCCCCCCCCCCCCCCOCC(O)COC(=O)CCCCCCC\\C=C/CCCCCCCC '
               'NAME: 1-O-palmityl-3-oleoylglycerol REASON: MISSED '
               'Insufficient hydroxyl or alkoxy groups\n'
               ' * SMILES: '
               'CC\\C=C/C\\C=C/C\\C=C/C\\C=C/C\\C=C/CCCC(=O)OC(CO)CO NAME: '
               '2-[(5Z,8Z,11Z,14Z,17Z)-eicosapentaenoyl]-sn-glycerol REASON: '
               'MISSED Acyl chain not properly connected to glycerol backbone\n'
               ' * SMILES: O=C(OC[C@@H](O)CO)/C=C/CCCCCCC(=O)OC NAME: '
               'Cladosporester C REASON: MISSED Found 2 ester groups, need '
               'exactly 1\n'
               ' * SMILES: CCCCCCCCCCCC(=O)OC(CO)CO NAME: 2-lauroylglycerol '
               'REASON: MISSED Acyl chain not properly connected to glycerol '
               'backbone\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'C[C@@H](C1=CC=CC=C1)NC(=O)C[C@H]2CC[C@@H]([C@@H](O2)CO)NC(=O)CN3CCOCC3',
                                     'name': '2-[(2R,5S,6R)-6-(hydroxymethyl)-5-[[2-(4-morpholinyl)-1-oxoethyl]amino]-2-oxanyl]-N-[(1S)-1-phenylethyl]acetamide',
                                     'reason': 'No glycerol backbone found'},
                                 {   'smiles': 'C[N+](C)(C)[C@@H](Cc1c[nH]c(n1)S(=O)C[C@H](NC(=O)CC[C@H]([NH3+])C([O-])=O)C([O-])=O)C([O-])=O',
                                     'name': 'N(alpha)-(L-gamma-glutamyl)-hercynyl-L-cysteine '
                                             'sulfoxide(1-)',
                                     'reason': 'No glycerol backbone found'},
                                 {   'smiles': 'O(C1=CC=2[C@]3([C@](N(CC3)C)(N(C2C=C1)C)[H])C)C(=O)N4CCC=5C(C4)=CC=CC5',
                                     'name': 'quilostigmine',
                                     'reason': 'No glycerol backbone found'},
                                 {   'smiles': 'O[C@@H]1[C@]23[C@@]4(N(C[C@@]([C@]2(C[C@@]4([C@]56[C@]3(CC(=O)[C@](C5)(C([C@H]6O)=C)[H])[H])[H])[H])(CC1)C)CC)[H]',
                                     'name': 'Bullatine G',
                                     'reason': 'No glycerol backbone found'},
                                 {   'smiles': 'NC1=NC=NC2=C1N=CN2[C@@H]3O[C@H](COP(=O)(O)O)[C@@H](OC(=O)[C@@H](N)CCC(O)=O)[C@H]3O',
                                     'name': "3'-L-glutamyl-AMP",
                                     'reason': 'Contains phosphate group - not '
                                               'a monoacylglycerol'},
                                 {   'smiles': 'O1C2(C(C3(C(C4(C(CC3OC(=O)C)C(OC(=O)CC4)(C)C)C)CC2)C)CC15C6N(C=7C5=CC=CC7)C(=O)C(N6)C)C',
                                     'name': 'Teraspiridole C_130091',
                                     'reason': 'No glycerol backbone found'},
                                 {   'smiles': 'O(C1[C@@H](OC(=O)C)C(O[C@@H](OC2=C(OC3=C(C2=O)C(O)=CC(O[C@@H]4OC([C@@H](O)[C@H](O)C4O)CO)=C3CC=C(C)C)C5=CC=C(OC)C=C5)[C@H]1O)C)[C@@H]6OC[C@@H](O)[C@H](OC(=O)C)C6O',
                                     'name': 'Sempervirenoside A',
                                     'reason': 'No glycerol backbone found'},
                                 {   'smiles': 'COC[C@]1(C(=O)C2CCN1CC2)CO',
                                     'name': '(2S)-2-(hydroxymethyl)-2-(methoxymethyl)-1-azabicyclo[2.2.2]octan-3-one',
                                     'reason': 'No glycerol backbone found'},
                                 {   'smiles': 'Oc1c(C2CC(Cc3ccccc23)c2ccc(OCc3ccc(cc3)C(F)(F)F)cc2)c(=O)oc2ccccc12',
                                     'name': 'Flocoumafen',
                                     'reason': 'No glycerol backbone found'},
                                 {   'smiles': 'O[C@H]1CC=2C(N(C=3C1=CC=CC3)C(=O)N)=CC=CC2',
                                     'name': '(S)-MHD',
                                     'reason': 'No glycerol backbone found'}],
    'sample_false_negatives': [   {   'smiles': 'O=C(CCC/C=C\\C/C=C\\C\\C=C/C=C/[C@H](CCCCC)OO)OC(CO)CO',
                                      'name': '15(S)-HPETE 2-glyceryl ester',
                                      'reason': 'Must have exactly 4 oxygens '
                                                '(1 ester + 2 hydroxyls)'},
                                  {   'smiles': 'O1C(C1C/C=C\\CCCCC)CCCCCCCC(OC[C@@H](O)CO)=O',
                                      'name': 'MG(18:1(12Z)-O(9S,10R)/0:0/0:0)',
                                      'reason': 'Must have exactly 4 oxygens '
                                                '(1 ester + 2 hydroxyls)'},
                                  {   'smiles': '[H][C@@]12CC[C@]3(CC1=C)C=CC(=O)[C@@](C)(CCC(=O)OCC(O)CO)[C@]3([H])C2',
                                      'name': 'Platencinic acid glycerol ester',
                                      'reason': 'Must have exactly 4 oxygens '
                                                '(1 ester + 2 hydroxyls)'},
                                  {   'smiles': 'O1C(CCC1CC(=O)C)C(C)C(OCC(O)CO)=O',
                                      'name': '2,3-dihydroxypropyl '
                                              '2-[5-(2-oxopropyl)oxolan-2-yl]propanoate',
                                      'reason': 'Must have exactly 4 oxygens '
                                                '(1 ester + 2 hydroxyls)'},
                                  {   'smiles': 'O=C1OC(/C(=C/C(=O)OC[C@H](O)CO)/C)=CC(=C1)OC',
                                      'name': 'Pestalotiopyrone I',
                                      'reason': 'Must have exactly 4 oxygens '
                                                '(1 ester + 2 hydroxyls)'},
                                  {   'smiles': 'O=C(OC[C@@H](O)CO)/C=C/CCCCCCC(=O)OC',
                                      'name': 'Cladosporester C',
                                      'reason': 'Found 2 ester groups, need '
                                                'exactly 1'},
                                  {   'smiles': 'C(\\[C@H]1[C@@H](CC([C@@H]1C/C=C\\CCCC(=O)OCC(CO)O)=O)O)=C/[C@H](CCCCC)O',
                                      'name': 'prostaglandin E2 1-glyceryl '
                                              'ester',
                                      'reason': 'Must have exactly 4 oxygens '
                                                '(1 ester + 2 hydroxyls)'},
                                  {   'smiles': 'O=C(CCC/C=C\\C\\C=C/C=C/C(C/C=C\\CCCCC)OO)OC(CO)CO',
                                      'name': '12-HPETE 2-glyceryl ester',
                                      'reason': 'Must have exactly 4 oxygens '
                                                '(1 ester + 2 hydroxyls)'},
                                  {   'smiles': 'O(C(=O)CCCCCCC/C=C\\CCCCCCCC)CC(O)COCC(O)CO',
                                      'name': 'Diglyceryl monooleate',
                                      'reason': 'Must have exactly 4 oxygens '
                                                '(1 ester + 2 hydroxyls)'},
                                  {   'smiles': 'C(\\[C@H]1[C@@H](CC([C@@H]1C/C=C\\CCCC(OC(CO)CO)=O)=O)O)=C/[C@H](CCCCC)O',
                                      'name': 'prostaglandin E2 2-glyceryl '
                                              'ester',
                                      'reason': 'Must have exactly 4 oxygens '
                                                '(1 ester + 2 hydroxyls)'}],
    'attempt': 3,
    'reasoning': 'Looking at the outcomes, here are the key issues with the '
                 'previous code:\n'
                 '\n'
                 '1. False Positives: The code incorrectly classified many '
                 'phospholipids and other complex glycerol derivatives. This '
                 'suggests we need better discrimination between '
                 'monoacylglycerols and other glycerol-containing compounds.\n'
                 '\n'
                 '2. False Negatives: The code missed several valid '
                 'monoacylglycerols, particularly those with the acyl group at '
                 'the 2-position (middle carbon). This suggests our acyl chain '
                 'connection patterns were too restrictive.\n'
                 '\n'
                 "Here's how we can improve:\n"
                 '\n'
                 '1. Add explicit checks to exclude phosphate groups '
                 '(phospholipids were a major source of false positives)\n'
                 '2. Improve the glycerol backbone pattern to better handle '
                 'all possible positions of the acyl group\n'
                 '3. Add better validation of the remaining hydroxyl groups\n'
                 '4. Add explicit checks to exclude compounds with multiple '
                 'ester groups or other complex modifications\n'
                 '5. Make the acyl chain connection patterns more flexible to '
                 'catch all valid positions\n'
                 '\n'
                 "Here's the improved code:",
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 91,
    'num_false_positives': 20,
    'num_true_negatives': 142169,
    'num_false_negatives': 20,
    'num_negatives': None,
    'precision': 0.8198198198198198,
    'recall': 0.8198198198198198,
    'f1': 0.8198198198198198,
    'accuracy': 0.9997189037245257,
    'negative_predictive_value': 0.9998593421432037}