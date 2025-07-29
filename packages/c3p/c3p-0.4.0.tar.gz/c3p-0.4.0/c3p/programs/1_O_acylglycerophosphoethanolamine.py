"""
Classifies: CHEBI:55493 1-O-acylglycerophosphoethanolamine
"""
"""
Classifies: 1-O-acylglycerophosphoethanolamine
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_1_O_acylglycerophosphoethanolamine(smiles: str):
    """
    Determines if a molecule is a 1-O-acylglycerophosphoethanolamine based on its SMILES string.
    These compounds have:
    - A glycerol backbone
    - An acyl group (ester) at sn-1 position
    - A hydroxyl at sn-2 position
    - A phosphoethanolamine group at sn-3 position
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a 1-O-acylglycerophosphoethanolamine, False otherwise
        str: Reason for classification
    """
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for glycerol backbone connected to correct groups
    # [CH2X4]-[CHX4]-[CH2X4] where:
    # - One CH2 has ester (sn-1)
    # - CH has OH (sn-2)
    # - Other CH2 has phosphate (sn-3)
    glycerol_pattern = Chem.MolFromSmarts("[CH2X4][CHX4][CH2X4]")
    if not mol.HasSubstructMatch(glycerol_pattern):
        return False, "No glycerol backbone found"

    # Check for phosphoethanolamine group with primary amine
    # -P(=O)(O)-O-CH2-CH2-NH2/NH3+
    phosphoethanolamine = Chem.MolFromSmarts("[PX4](=O)([OH,O-])[OX2][CH2X4][CH2X4][NH2X3,NH3X4+]")
    if not mol.HasSubstructMatch(phosphoethanolamine):
        return False, "No phosphoethanolamine group with primary amine found"

    # Exclude phosphocholine (N(CH3)3+)
    phosphocholine = Chem.MolFromSmarts("[NX4+](C)(C)(C)")
    if mol.HasSubstructMatch(phosphocholine):
        return False, "Contains quaternary amine (phosphocholine) instead of primary amine"

    # Check for single ester group at sn-1
    # R-C(=O)-O-CH2- connected to glycerol
    ester_pattern = Chem.MolFromSmarts("[CX3](=[OX1])[OX2][CH2X4][CHX4]([OX2H1])[CH2X4]O")
    if not mol.HasSubstructMatch(ester_pattern):
        return False, "No ester group at sn-1 position found"
    
    # Count ester groups - should only be one
    ester_matches = len(mol.GetSubstructMatches(Chem.MolFromSmarts("[CX3](=[OX1])[OX2]")))
    if ester_matches != 1:
        return False, f"Found {ester_matches} ester groups, should be exactly 1"

    # Exclude vinyl ethers (plasmalogens)
    vinyl_ether = Chem.MolFromSmarts("[OX2][CH2X4][CHX4]([OX2H1])[CH2X4]O[CH2X3]=[CH1X3]")
    if mol.HasSubstructMatch(vinyl_ether):
        return False, "Contains vinyl ether (plasmalogen) instead of ester at sn-1"

    # Exclude N-acylated versions
    n_acyl = Chem.MolFromSmarts("[NX3][CX3]=[OX1]")
    if mol.HasSubstructMatch(n_acyl):
        return False, "Contains N-acylation"

    # Verify basic composition
    p_count = sum(1 for atom in mol.GetAtoms() if atom.GetAtomicNum() == 15)
    o_count = sum(1 for atom in mol.GetAtoms() if atom.GetAtomicNum() == 8)
    n_count = sum(1 for atom in mol.GetAtoms() if atom.GetAtomicNum() == 7)

    if p_count != 1:
        return False, f"Should have exactly 1 phosphorus, found {p_count}"
    if o_count < 5:
        return False, f"Should have at least 5 oxygens, found {o_count}"
    if n_count != 1:
        return False, f"Should have exactly 1 nitrogen, found {n_count}"

    # Check for acyl chain length - should be at least 4 carbons
    carbon_chain = Chem.MolFromSmarts("[CX4,CX3]~[CX4,CX3]~[CX4,CX3]~[CX4,CX3]")
    if not mol.HasSubstructMatch(carbon_chain):
        return False, "Acyl chain too short"

    return True, "Contains glycerol backbone with phosphoethanolamine group and single acyl substituent at sn-1"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:55493',
                          'name': '1-O-acylglycerophosphoethanolamine',
                          'definition': 'A glycerophosphoethanolamine having '
                                        'an unspecified O-acyl substituent at '
                                        'the 1-position of the glycerol '
                                        'fragment.',
                          'parents': ['CHEBI:64574'],
                          'xrefs': ['PMID:16341241'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': None,
    'message': '\n'
               'Attempt failed: F1 score of 0.35064935064935066 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: '
               'P(OC[C@H](O)COC(=O)CCCCCCC/C=C\\C/C=C\\CCCC)(OCCN)(O)=O NAME: '
               'PE(17:2(9Z,12Z)/0:0) REASON: CORRECT Contains glycerol '
               'backbone with phosphoethanolamine group and single acyl '
               'substituent\n'
               ' * SMILES: C(CN)OP(=O)(O)OC[C@H](O)COC(CCCCCCCCCCCCCCCCCCC)=O '
               'NAME: 1-icosanoyl-sn-glycero-3-phosphoethanolamine REASON: '
               'CORRECT Contains glycerol backbone with phosphoethanolamine '
               'group and single acyl substituent\n'
               ' * SMILES: [C@@H](COC(=O)CCCCCCCCCCCCCCC)(COP(OCCN)(=O)O)O '
               'NAME: 1-hexadecanoyl-sn-glycero-3-phosphoethanolamine REASON: '
               'CORRECT Contains glycerol backbone with phosphoethanolamine '
               'group and single acyl substituent\n'
               ' * SMILES: '
               'P(OC[C@H](O)COC(=O)CC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CCCCC)(OCCN)(O)=O '
               'NAME: LysoPE(22:5(4Z,7Z,10Z,13Z,16Z)/0:0) REASON: CORRECT '
               'Contains glycerol backbone with phosphoethanolamine group and '
               'single acyl substituent\n'
               ' * SMILES: CCCCCCCCCCCCCCCCCC(=O)OC[C@@H](O)COP(O)(=O)OCCN '
               'NAME: 1-stearoyl-sn-glycero-3-phosphoethanolamine REASON: '
               'CORRECT Contains glycerol backbone with phosphoethanolamine '
               'group and single acyl substituent\n'
               ' * SMILES: P(OC[C@H](O)COC(=O)CCCCCCC/C=C\\CCCCC)(OCCN)(O)=O '
               'NAME: PE(15:1(9Z)/0:0) REASON: CORRECT Contains glycerol '
               'backbone with phosphoethanolamine group and single acyl '
               'substituent\n'
               ' * SMILES: P(OC[C@H](O)COC(=O)CCCCCCCCCCCC)(OCCN)(O)=O NAME: '
               'PE(13:0/0:0) REASON: CORRECT Contains glycerol backbone with '
               'phosphoethanolamine group and single acyl substituent\n'
               ' * SMILES: '
               'CCCCC\\C=C/C\\C=C/C\\C=C/C\\C=C/CCCC(=O)OC[C@@H](O)COP(O)(=O)OCCN '
               'NAME: 1-arachidonoyl-sn-glycero-3-phosphoethanolamine REASON: '
               'CORRECT Contains glycerol backbone with phosphoethanolamine '
               'group and single acyl substituent\n'
               ' * SMILES: '
               'CCCCC\\C=C/C\\C=C/CCCCCCCC(=O)OC[C@@H](O)COP(O)(=O)OCCN NAME: '
               '1-linoleoyl-sn-glycero-3-phosphoethanolamine REASON: CORRECT '
               'Contains glycerol backbone with phosphoethanolamine group and '
               'single acyl substituent\n'
               ' * SMILES: P(OCC(O)COC(=O)CCCCCCCC=CCC=CCCCCC)(OCCN)(O)=O '
               'NAME: '
               '[3-[2-Aminoethoxy(hydroxy)phosphoryl]oxy-2-hydroxypropyl] '
               'octadeca-9,12-dienoate REASON: CORRECT Contains glycerol '
               'backbone with phosphoethanolamine group and single acyl '
               'substituent\n'
               ' * SMILES: '
               '[H][C@@](O)(COC(=O)CCCCCC\\C=C/C\\C=C/C\\C=C/C\\C=C/CC)COP(O)(=O)OCCN '
               'NAME: lysophosphatidylethanolamine (20:4(8Z,11Z,14Z,17Z)/0:0) '
               'REASON: CORRECT Contains glycerol backbone with '
               'phosphoethanolamine group and single acyl substituent\n'
               ' * SMILES: '
               'C([C@@](COC(CCCCCCCCC/C=C\\CCCCCC)=O)(O)[H])OP(=O)(O)OCCN '
               'NAME: PE(18:1(11Z)/0:0) REASON: CORRECT Contains glycerol '
               'backbone with phosphoethanolamine group and single acyl '
               'substituent\n'
               ' * SMILES: '
               'P(OCC(O)COC(=O)CCCCCCCC/C=C\\C/C=C\\C/C=C\\CCCCC)(OCCN)(O)=O '
               'NAME: LPE 22:3 REASON: CORRECT Contains glycerol backbone with '
               'phosphoethanolamine group and single acyl substituent\n'
               ' * SMILES: '
               'P(OC[C@H](O)COC(=O)CCCC/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)(OCCN)(O)=O '
               'NAME: PE(18:4(6Z,9Z,12Z,15Z)/0:0) REASON: CORRECT Contains '
               'glycerol backbone with phosphoethanolamine group and single '
               'acyl substituent\n'
               ' * SMILES: '
               'P(OC[C@H](O)COC(=O)CCCCCCCC1C(C1)CCCCCC)(OCC[NH3+])([O-])=O '
               'NAME: LPE(17:1/0:0) REASON: CORRECT Contains glycerol backbone '
               'with phosphoethanolamine group and single acyl substituent\n'
               ' * SMILES: CCCCCCCCCCCCCCCCC(=O)OC[C@@H](O)COP(O)(=O)OCCN '
               'NAME: 1-heptadecanoyl-sn-glycero-3-phosphoethanolamine REASON: '
               'CORRECT Contains glycerol backbone with phosphoethanolamine '
               'group and single acyl substituent\n'
               ' * SMILES: P(OC[C@H](O)COC(=O)CCCCCCCCCCCCCC)(OCCN)(O)=O NAME: '
               'LysoPE(15:0/0:0) REASON: CORRECT Contains glycerol backbone '
               'with phosphoethanolamine group and single acyl substituent\n'
               ' * SMILES: P(OC[C@H](O)COC(=O)CCCCCCC/C=C\\CCCCCCC)(OCCN)(O)=O '
               'NAME: PE(17:1(9Z)/0:0) REASON: CORRECT Contains glycerol '
               'backbone with phosphoethanolamine group and single acyl '
               'substituent\n'
               ' * SMILES: '
               'P(OC[C@H](O)COC(=O)CCCCCCCCC/C=C\\CCCCCCCCCC)(OCCN)(O)=O NAME: '
               'PE(22:1(11Z)/0:0) REASON: CORRECT Contains glycerol backbone '
               'with phosphoethanolamine group and single acyl substituent\n'
               ' * SMILES: '
               'P(OC[C@H](O)COC(=O)CCCCCCC/C=C\\C/C=C\\C/C=C\\CC)(OCCN)(O)=O '
               'NAME: LysoPE(18:3(9Z,12Z,15Z)/0:0) REASON: CORRECT Contains '
               'glycerol backbone with phosphoethanolamine group and single '
               'acyl substituent\n'
               ' * SMILES: '
               'P(OC[C@H](O)COC(=O)CCCCCCCCC/C=C\\C/C=C\\C/C=C\\CC)(OCCN)(O)=O '
               'NAME: LysoPE(20:3(11Z,14Z,17Z)/0:0) REASON: CORRECT Contains '
               'glycerol backbone with phosphoethanolamine group and single '
               'acyl substituent\n'
               ' * SMILES: '
               '[H][C@@](O)(COC(=O)CC\\C=C/C\\C=C/C\\C=C/C\\C=C/C\\C=C/C\\C=C/CC)COP(O)(=O)OCCN '
               'NAME: lysophosphatidylethanolamine '
               '(22:6(4Z,7Z,10Z,13Z,16Z,19Z)/0:0) REASON: CORRECT Contains '
               'glycerol backbone with phosphoethanolamine group and single '
               'acyl substituent\n'
               ' * SMILES: '
               'P(OC[C@H](O)COC(=O)CCCCCCCCCCCCCCCCCCCCC)(OCCN)(O)=O NAME: '
               'LysoPE(22:0/0:0) REASON: CORRECT Contains glycerol backbone '
               'with phosphoethanolamine group and single acyl substituent\n'
               ' * SMILES: '
               'P(OCC(O)COC(=O)CCCCCCCC=CCCCCCCCC)(OCC[NH3+])([O-])=O NAME: '
               '2-Azaniumylethyl (2-hydroxy-3-octadec-9-enoyloxypropyl) '
               'phosphate REASON: CORRECT Contains glycerol backbone with '
               'phosphoethanolamine group and single acyl substituent\n'
               ' * SMILES: CCCCCCCC\\C=C/CCCCCCCC(=O)OC[C@@H](O)COP(O)(=O)OCCN '
               'NAME: 1-oleoyl-sn-glycero-3-phosphoethanolamine REASON: '
               'CORRECT Contains glycerol backbone with phosphoethanolamine '
               'group and single acyl substituent\n'
               'False positives: SMILES: '
               'P(OC[C@H](OC(=O)CCCCCCC/C=C\\C/C=C\\C/C=C\\CC)CO/C=C\\CCCCCC/C=C\\CCCCCCCC)(OCCN)(O)=O '
               'NAME: PE(P-18:1(9Z)/18:3(9Z,12Z,15Z)) REASON: WRONGLY '
               'CLASSIFIED Contains glycerol backbone with phosphoethanolamine '
               'group and single acyl substituent\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCC\\C=C/OC[C@H](COP(O)(=O)OCCN)OC(=O)CCCCCCC\\C=C/CCCCCCCC '
               'NAME: '
               '1-(1Z-octadecenyl)-2-(9Z-octadecenoyl)-sn-glycero-3-phosphoethanolamine '
               'REASON: WRONGLY CLASSIFIED Contains glycerol backbone with '
               'phosphoethanolamine group and single acyl substituent\n'
               ' * SMILES: '
               'C(CCCCCCC/C=C\\CCCCCCCC)(=O)O[C@@H](COP(=O)(OCCN)O)CO/C=C\\CCCCCCCCCCCCCC '
               'NAME: '
               '1-(1Z-hexadecenyl)-2-oleoyl-sn-glycero-3-phosphoethanolamine '
               'REASON: WRONGLY CLASSIFIED Contains glycerol backbone with '
               'phosphoethanolamine group and single acyl substituent\n'
               ' * SMILES: '
               'P(OC[C@H](O/C=C\\CCCCCCCCCCCCCC)COC(=O)CCCCCCCCCCCCCC)(OCCN)(O)=O '
               'NAME: '
               '(2-Aminoethoxy)[(2R)-2-[(1Z)-hexadec-1-en-1-yloxy]-3-(pentadecanoyloxy)propoxy]phosphinic '
               'acid REASON: WRONGLY CLASSIFIED Contains glycerol backbone '
               'with phosphoethanolamine group and single acyl substituent\n'
               ' * SMILES: '
               'C(C[N+](C)(C)C)OP(=O)([O-])OC[C@](COC(=O)CCCCCCCCCCCCC)([H])O '
               'NAME: 1-myristoyl-sn-glycero-3-phosphocholine REASON: WRONGLY '
               'CLASSIFIED Contains glycerol backbone with phosphoethanolamine '
               'group and single acyl substituent\n'
               ' * SMILES: '
               'C(C[N+](C)(C)C)OP(=O)([O-])OC[C@H](O)COC(CCCCC/C=C\\C/C=C\\C/C=C\\C/C=C\\CCCCC)=O '
               'NAME: '
               '1-[(7Z,10Z,13Z,16Z)-docosatetraenoyl]-sn-glycero-3-phosphocholine '
               'REASON: WRONGLY CLASSIFIED Contains glycerol backbone with '
               'phosphoethanolamine group and single acyl substituent\n'
               ' * SMILES: '
               'C([C@@](COC(CCC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)=O)(O)[H])OP([O-])(=O)OCC[N+](C)(C)C '
               'NAME: LysoPC(20:5(5Z,8Z,11Z,14Z,17Z)) REASON: WRONGLY '
               'CLASSIFIED Contains glycerol backbone with phosphoethanolamine '
               'group and single acyl substituent\n'
               ' * SMILES: '
               'P(OC[C@H](OC(=O)CCCCCCC/C=C\\CCCCC)CO/C=C\\CCCCCCCCCCCCCCCC)(OCCN)(O)=O '
               'NAME: PE(P-18:0/15:1(9Z)) REASON: WRONGLY CLASSIFIED Contains '
               'glycerol backbone with phosphoethanolamine group and single '
               'acyl substituent\n'
               ' * SMILES: '
               'CCCCCCCC\\C=C/CCCCCCCC(=O)OC[C@@H](O)COP([O-])(=O)OCC[NH3+] '
               'NAME: 1-oleoyl-sn-glycero-3-phosphoethanolamine zwitterion '
               'REASON: WRONGLY CLASSIFIED Contains glycerol backbone with '
               'phosphoethanolamine group and single acyl substituent\n'
               ' * SMILES: '
               '[O-]C(CCCCCCCC(=O)O[C@@H](COP(=O)(OCC[N+](C)(C)C)[O-])CO)=O '
               'NAME: 2-azelaoyl-sn-glycero-3-phosphocholine(1-) REASON: '
               'WRONGLY CLASSIFIED Contains glycerol backbone with '
               'phosphoethanolamine group and single acyl substituent\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCC(=O)OC[C@@H](O)COP(O)(=O)OCC[N+](C)(C)C NAME: '
               '1-O-palmitoyl-sn-glycero-3-phosphocholine REASON: WRONGLY '
               'CLASSIFIED Contains glycerol backbone with phosphoethanolamine '
               'group and single acyl substituent\n'
               ' * SMILES: '
               'P(OC[C@H](OC(=O)CCCCCCC/C=C\\CCCCCCCCC)CO/C=C\\CCCCCCCCCCCCCCCC)(OCCN)(O)=O '
               'NAME: PE(P-18:0/19:1(9Z)) REASON: WRONGLY CLASSIFIED Contains '
               'glycerol backbone with phosphoethanolamine group and single '
               'acyl substituent\n'
               ' * SMILES: '
               'C([C@@](CO)(OC(CCCCCCCCCCC/C=C\\C/C=C\\CCCCC)=O)[H])OP(=O)(O)OCCN '
               'NAME: PE(0:0/22:2(13Z,16Z)) REASON: WRONGLY CLASSIFIED '
               'Contains glycerol backbone with phosphoethanolamine group and '
               'single acyl substituent\n'
               ' * SMILES: '
               'P(OCC[N+](C)(C)C)(OC[C@H](O)COC(=O)CCCCCCCCCCCC)([O-])=O NAME: '
               'PC(13:0/0:0) REASON: WRONGLY CLASSIFIED Contains glycerol '
               'backbone with phosphoethanolamine group and single acyl '
               'substituent\n'
               ' * SMILES: '
               'P(OC[C@@H](CO/C=C\\CCCCCCCCCCCCCCCC)OC(=O)CCCCCCCCCCCCCCC)(=O)(OCCN)O '
               'NAME: '
               '1-(1Z-octadecenyl)-2-hexadecanoyl-sn-glycero-3-phosphoethanolamine '
               'REASON: WRONGLY CLASSIFIED Contains glycerol backbone with '
               'phosphoethanolamine group and single acyl substituent\n'
               ' * SMILES: '
               'P(OC[C@H](OC(=O)CCCC/C=C\\C/C=C\\C/C=C\\CCCCC)CO/C=C\\CCCCCC/C=C\\CCCCCCCC)(OCCN)(O)=O '
               'NAME: PE(P-18:1(9Z)/18:3(6Z,9Z,12Z)) REASON: WRONGLY '
               'CLASSIFIED Contains glycerol backbone with phosphoethanolamine '
               'group and single acyl substituent\n'
               ' * SMILES: '
               'C([C@@](CO/C=C\\CCCCCC/C=C\\CCCCCCCC)(OC(CCCCCCC/C=C\\C/C=C\\CCCCC)=O)[H])OP(=O)(O)OCCN '
               'NAME: PE(P-18:1(9Z)/18:2(9Z,12Z)) REASON: WRONGLY CLASSIFIED '
               'Contains glycerol backbone with phosphoethanolamine group and '
               'single acyl substituent\n'
               ' * SMILES: CCCCCC(=O)OC[C@@H](O)COP([O-])(=O)OCC[N+](C)(C)C '
               'NAME: 1-hexanoyl-sn-glycero-3-phosphocholine REASON: WRONGLY '
               'CLASSIFIED Contains glycerol backbone with phosphoethanolamine '
               'group and single acyl substituent\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCCCC(=O)NCCOP([O-])(=O)OC[C@H](O)COC(=O)CCCCCCC\\C=C/CCCCCCCC '
               'NAME: '
               'N-icosanoyl-1-oleoyl-sn-glycero-3-phosphoethanolamine(1-) '
               'REASON: WRONGLY CLASSIFIED Contains glycerol backbone with '
               'phosphoethanolamine group and single acyl substituent\n'
               ' * SMILES: '
               'CCCCCC\\C=C\\CCCCCCCC(=O)OC[C@@H](O)COP([O-])(=O)OCC[N+](C)(C)C '
               'NAME: 1-[(9E)-hexadecenoyl]-sn-glycero-3-phosphocholine '
               'REASON: WRONGLY CLASSIFIED Contains glycerol backbone with '
               'phosphoethanolamine group and single acyl substituent\n'
               ' * SMILES: '
               'P(OCC[N+](C)(C)C)(OCC(OC(=O)CCCCCCCC(O)/C=C/C=C\\CCCCC)CO/C=C\\CCCCCCCCCCCCCC)([O-])=O '
               'NAME: Pc(16:1e/9-hode) REASON: WRONGLY CLASSIFIED Contains '
               'glycerol backbone with phosphoethanolamine group and single '
               'acyl substituent\n'
               ' * SMILES: '
               '[C@@H](COC(=O)CCCCCCCCCCCCCCC)(COP(OCC[N+](C)(C)C)(=O)[O-])O '
               'NAME: 1-hexadecanoyl-sn-glycero-3-phosphocholine REASON: '
               'WRONGLY CLASSIFIED Contains glycerol backbone with '
               'phosphoethanolamine group and single acyl substituent\n'
               ' * SMILES: '
               'P(OC[C@H](O/C=C\\CCCCCCCCCCCCCC)COC(=O)CC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CCCCC)(OCCN)(O)=O '
               'NAME: PE(22:5(4Z,7Z,10Z,13Z,16Z)/P-16:0) REASON: WRONGLY '
               'CLASSIFIED Contains glycerol backbone with phosphoethanolamine '
               'group and single acyl substituent\n'
               ' * SMILES: '
               'P(OC[C@H](OC(=O)CCCC/C=C\\C/C=C\\C/C=C\\CCCCC)CO/C=C\\CCCCCCCC/C=C\\CCCCCC)(OCCN)(O)=O '
               'NAME: PE(P-18:1(11Z)/18:3(6Z,9Z,12Z)) REASON: WRONGLY '
               'CLASSIFIED Contains glycerol backbone with phosphoethanolamine '
               'group and single acyl substituent\n'
               ' * SMILES: '
               'CCCCCCCC\\C=C/CCCCCCCC(=O)NCCOP([O-])(=O)OC[C@H](O)COC(=O)CCCCCCC\\C=C/CCCCCCCC '
               'NAME: N,1-dioleoyl-sn-glycero-3-phosphoethanolamine(1-) '
               'REASON: WRONGLY CLASSIFIED Contains glycerol backbone with '
               'phosphoethanolamine group and single acyl substituent\n'
               'False negatives: NONE\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'C1C=C(N=C2N1NN=N2)C3=CC=CC=C3',
                                     'name': '5-phenyl-1,7-dihydrotetrazolo[1,5-a]pyrimidine',
                                     'reason': 'No glycerol backbone found'},
                                 {   'smiles': 'O(C(=O)CCCCCCCCCCC/C=C\\CCCCCCCC)[C@H](COC(=O)CCCCCCCCC/C=C\\CCCCCC)COC(=O)CCCCCCC/C=C\\CCCC',
                                     'name': 'TG(14:1(9Z)/22:1(13Z)/18:1(11Z))',
                                     'reason': 'No phosphoethanolamine group '
                                               'with primary amine found'},
                                 {   'smiles': 'CC(=O)N[C@H]1[C@H](O)O[C@H](CO)[C@@H](O[C@@H]2O[C@H](CO)[C@@H](O[C@@H]3O[C@H](CO[C@H]4O[C@H](CO[C@H]5O[C@H](CO)[C@@H](O)[C@H](O)[C@@H]5O)[C@@H](O)[C@H](O[C@H]5O[C@H](CO)[C@@H](O)[C@H](O)[C@@H]5O)[C@@H]4O)[C@@H](O)[C@H](O[C@H]4O[C@H](CO)[C@@H](O)[C@H](O)[C@@H]4O[C@@H]4O[C@H](CO)[C@@H](O)[C@H](O)[C@H]4NC(C)=O)[C@@H]3O)[C@H](O)[C@H]2NC(C)=O)[C@@H]1O',
                                     'name': 'beta-D-GlcpNAc-(1->2)-alpha-D-Manp-(1->3)-{alpha-D-Manp-(1->3)-[alpha-D-Manp-(1->6)]-alpha-D-Manp-(1->6)}-beta-D-Manp-(1->4)-beta-GlcpNAc-(1->4)-beta-D-GlcpNAc',
                                     'reason': 'No glycerol backbone found'},
                                 {   'smiles': '[C@@]12([C@@]([C@]([C@@H](CC1)C)(CCC(CC)C)C)(CCC[C@@H]2C)[H])C',
                                     'name': 'clerodane',
                                     'reason': 'No phosphoethanolamine group '
                                               'with primary amine found'},
                                 {   'smiles': 'S(O[C@@H]1[C@H](O)[C@@H](O)[C@H](O[C@@H]([C@@H](O)[C@H](O)CO[C@]2(O[C@H]([C@H](NC(=O)C)[C@@H](O)C2)[C@H](O)[C@H](O)CO)C(O)=O)[C@@H](NC(=O)C)CO)O[C@@H]1CO)(O)(=O)=O',
                                     'name': '(2R,4S,5R,6R)-5-Acetamido-2-[(2R,3S,4R,5S)-5-acetamido-4-[(2R,3R,4R,5R,6R)-3,4-dihydroxy-6-(hydroxymethyl)-5-sulfooxyoxan-2-yl]oxy-2,3,6-trihydroxyhexoxy]-4-hydroxy-6-[(1R,2R)-1,2,3-trihydroxypropyl]oxane-2-carboxylic '
                                             'acid',
                                     'reason': 'No glycerol backbone found'},
                                 {   'smiles': 'O=C(NC(CC(C)C)C(=O)N[C@@H](CCCN=C(N)N)C=O)C(NC(=O)CC)CC(C)C',
                                     'name': 'Leupeptin Pr-LL',
                                     'reason': 'No glycerol backbone found'},
                                 {   'smiles': 'COC1=CC=C(C=C1)CCNC(=O)C(=C2C3=CC=CC=C3C(=N2)NC(=O)C4=CC=CS4)C#N',
                                     'name': 'N-[3-[1-cyano-2-[2-(4-methoxyphenyl)ethylamino]-2-oxoethylidene]-1-isoindolyl]-2-thiophenecarboxamide',
                                     'reason': 'No glycerol backbone found'},
                                 {   'smiles': 'O=C1O[C@@H](CC=2C1=C(OC)C(O)=CC2)CCC[C@@H](O)C',
                                     'name': 'Penicimarin C',
                                     'reason': 'No phosphoethanolamine group '
                                               'with primary amine found'},
                                 {   'smiles': 'CO[C@@H]1[C@@H]2[C@@H](C[C@@H]3[C@@](O2)([C@H]([C@@H]([C@H](O3)C(=O)OC)O)O)O)OC1N4C=NC5=C4N=CN=C5N',
                                     'name': 'LSM-4497',
                                     'reason': 'No glycerol backbone found'},
                                 {   'smiles': 'C[C@@H]1[C@H](O)CCC2=CC[C@H](C[C@]12C)C(C)=C',
                                     'name': '1-deoxycapsidiol',
                                     'reason': 'No phosphoethanolamine group '
                                               'with primary amine found'}],
    'sample_false_negatives': [],
    'attempt': 1,
    'reasoning': 'Let me analyze the previous outcomes and suggest '
                 'improvements:\n'
                 '\n'
                 '1. The main issue seems to be false positives - the program '
                 'is incorrectly classifying many phosphocholine lipids (PC) '
                 'and plasmalogen PEs (PE-P) as '
                 '1-O-acylglycerophosphoethanolamine.\n'
                 '\n'
                 '2. Key observations from false positives:\n'
                 '- Many have N(CH3)3+ groups (phosphocholine) instead of NH2 '
                 'groups\n'
                 '- Several have vinyl ether bonds (plasmalogens) at the sn-1 '
                 'position instead of ester bonds\n'
                 '- Some have additional modifications like N-acylation\n'
                 '\n'
                 '3. Suggested improvements:\n'
                 '\n'
                 'a) Add specific check for primary amine (-NH2 or -NH3+) and '
                 'exclude quaternary amines:\n'
                 '- Replace current nitrogen check with more specific SMARTS '
                 'pattern\n'
                 '- Explicitly exclude N(CH3)3+ groups\n'
                 '\n'
                 'b) Better specify the position of the acyl group:\n'
                 '- Need to ensure the ester is at sn-1 position \n'
                 '- Can use more specific SMARTS pattern connecting glycerol '
                 'backbone to ester\n'
                 '\n'
                 'c) Exclude vinyl ethers:\n'
                 '- Add negative check for O-C=C pattern characteristic of '
                 'plasmalogens\n'
                 '- Ensure O-C(=O) pattern is at sn-1\n'
                 '\n'
                 'd) Exclude N-acylated versions:\n'
                 '- Add negative check for N-C(=O) pattern\n'
                 '\n'
                 "Here's my improved version:",
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 27,
    'num_false_positives': 16,
    'num_true_negatives': 142257,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.627906976744186,
    'recall': 1.0,
    'f1': 0.7714285714285715,
    'accuracy': 0.9998875614898103,
    'negative_predictive_value': 1.0}