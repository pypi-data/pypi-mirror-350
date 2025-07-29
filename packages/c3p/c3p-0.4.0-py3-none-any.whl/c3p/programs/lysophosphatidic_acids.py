"""
Classifies: CHEBI:32957 lysophosphatidic acids
"""
"""
Classifies: CHEBI:75856 lysophosphatidic acid
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_lysophosphatidic_acids(smiles: str):
    """
    Determines if a molecule is a lysophosphatidic acid based on its SMILES string.
    A lysophosphatidic acid has:
    - A glycerol backbone
    - One fatty acid chain attached via ester bond
    - A phosphate group at the sn-3 position
    - A free hydroxyl group
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a lysophosphatidic acid, False otherwise
        str: Reason for classification
    """
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Look for complete lysophosphatidic acid core structure
    # [OH]-C-C(OH/OR)-C-O-P(=O)(O)(O)
    lpa_pattern = Chem.MolFromSmarts(
        "[OX2H,OX2][CH2X4][CHX4]([OX2H,OX2C])[CH2X4][OX2]P(=[OX1])([OX2H,OX1-])[OX2H,OX1-]"
    )
    if not mol.HasSubstructMatch(lpa_pattern):
        return False, "Missing core lysophosphatidic acid structure"

    # Look for ester group (-O-C(=O)-)
    ester_pattern = Chem.MolFromSmarts("[OX2][CX3](=[OX1])[#6]")
    ester_matches = len(mol.GetSubstructMatches(ester_pattern))
    if ester_matches != 1:
        return False, f"Found {ester_matches} ester groups, need exactly 1"

    # Look for fatty acid chain attached to ester
    # At least 4 carbons in chain
    fatty_chain = Chem.MolFromSmarts("[CX3](=[OX1])[#6]~[#6]~[#6]~[#6]")
    if not mol.HasSubstructMatch(fatty_chain):
        return False, "No suitable fatty acid chain found"

    # Count key atoms to ensure proper composition
    c_count = sum(1 for atom in mol.GetAtoms() if atom.GetAtomicNum() == 6)
    o_count = sum(1 for atom in mol.GetAtoms() if atom.GetAtomicNum() == 8)
    p_count = sum(1 for atom in mol.GetAtoms() if atom.GetAtomicNum() == 15)
    
    if c_count < 5:
        return False, "Too few carbons for lysophosphatidic acid"
    if o_count < 6:
        return False, "Must have at least 6 oxygens"
    if p_count != 1:
        return False, "Must have exactly one phosphorus"

    # Verify at least one free hydroxyl
    hydroxyl = Chem.MolFromSmarts("[OX2H]")
    if not mol.HasSubstructMatch(hydroxyl):
        return False, "No free hydroxyl group found"

    # Check that molecule isn't too complex (to avoid larger phospholipids)
    if len(mol.GetAtoms()) > 100:
        return False, "Molecule too large for lysophosphatidic acid"

    return True, "Contains glycerol backbone with one fatty acid chain and phosphate group"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:32957',
                          'name': 'lysophosphatidic acids',
                          'definition': 'Any monoacylglycerol phosphate '
                                        'obtained by hydrolytic removal of one '
                                        'of the two acyl groups of any '
                                        'phosphatidic acid or derivatives '
                                        'therein.',
                          'parents': ['CHEBI:16961'],
                          'xrefs': ['Wikipedia:Lysophosphatidic_acid'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': None,
    'message': '\n'
               'Attempt failed: F1 score of 0.6758620689655173 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: '
               'CCCCC\\C=C/C\\C=C/C\\C=C/C\\C=C/CCCC(=O)O[C@H](CO)COP(O)(O)=O '
               'NAME: 2-arachidonoyl-sn-glycero-3-phosphate REASON: CORRECT '
               'Contains glycerol backbone with one fatty acid chain and '
               'phosphate group\n'
               ' * SMILES: '
               'P(OCC(O)COC(=O)CCCCCC/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)(O)(O)=O '
               'NAME: LysoPA(20:4(8Z,11Z,14Z,17Z)/0:0) REASON: CORRECT '
               'Contains glycerol backbone with one fatty acid chain and '
               'phosphate group\n'
               ' * SMILES: [H][C@@](O)(COC(=O)CCCCCCC\\C=C/CCCCCC)COP(O)(O)=O '
               'NAME: 1-palmitoleoyl-sn-glycerol 3-phosphate REASON: CORRECT '
               'Contains glycerol backbone with one fatty acid chain and '
               'phosphate group\n'
               ' * SMILES: '
               'CC\\C=C/C\\C=C/C\\C=C/CCCCCCCC(=O)OC[C@@H](O)COP(O)(O)=O NAME: '
               '1-linolenoyl-sn-glycero-3-phosphate REASON: CORRECT Contains '
               'glycerol backbone with one fatty acid chain and phosphate '
               'group\n'
               ' * SMILES: '
               'P(OC[C@H](O)COC(=O)CCCCCCC/C=C\\C/C=C\\CCCC)(O)(O)=O NAME: '
               'PA(17:2(9Z,12Z)/0:0) REASON: CORRECT Contains glycerol '
               'backbone with one fatty acid chain and phosphate group\n'
               ' * SMILES: CCCCCCCC\\C=C/CCCCCCCC(=O)O[C@H](CO)COP(O)(O)=O '
               'NAME: 2-oleoyl-sn-glycero-3-phosphate REASON: CORRECT Contains '
               'glycerol backbone with one fatty acid chain and phosphate '
               'group\n'
               ' * SMILES: O[C@H](COC(=O)CCCCCCCCCCCCCCCCCS)COP(O)(O)=O NAME: '
               '1-(18-mercaptooctadecanoyl)-sn-glycerol 3-phosphate REASON: '
               'CORRECT Contains glycerol backbone with one fatty acid chain '
               'and phosphate group\n'
               ' * SMILES: '
               'O(C[C@H](COP(=O)(O)O)O)C(=O)CCCCCCC/C=C\\C/C=C\\CCCCC NAME: '
               '1-linoleoyl-sn-glycerol 3-phosphate REASON: CORRECT Contains '
               'glycerol backbone with one fatty acid chain and phosphate '
               'group\n'
               ' * SMILES: '
               'P(OCC(O)COC(=O)CCC/C=C\\C/C=C\\C/C=C\\CCCCCCCC)(O)(O)=O NAME: '
               'PA(20:3(5Z,8Z,11Z)/0:0) REASON: CORRECT Contains glycerol '
               'backbone with one fatty acid chain and phosphate group\n'
               ' * SMILES: CCCCC\\C=C/C\\C=C/CCCCCCCC(=O)O[C@H](CO)COP(O)(O)=O '
               'NAME: lysophosphatidic acid 0:0/18:2(9Z,12Z) REASON: CORRECT '
               'Contains glycerol backbone with one fatty acid chain and '
               'phosphate group\n'
               ' * SMILES: CCCCCCCCCCCCCC(=O)OC[C@@H](O)COP(O)(O)=O NAME: '
               '1-myristoyl-sn-glycerol 3-phosphate REASON: CORRECT Contains '
               'glycerol backbone with one fatty acid chain and phosphate '
               'group\n'
               ' * SMILES: P(OC[C@H](O)COC(=O)CCCCCCCCCCCCCCCCCCCC)(O)(O)=O '
               'NAME: 1-heneicosanoyl-glycero-3-phosphate REASON: CORRECT '
               'Contains glycerol backbone with one fatty acid chain and '
               'phosphate group\n'
               ' * SMILES: P(OCC(O)COC(=O)CCCCCCCCCCCCCCCCC)(O)(O)=O NAME: '
               'LysoPA(18:0/0:0) REASON: CORRECT Contains glycerol backbone '
               'with one fatty acid chain and phosphate group\n'
               ' * SMILES: P(OC[C@H](O)COC(=O)CCCCCCCCCCCC)(O)(O)=O NAME: '
               'PA(13:0/0:0) REASON: CORRECT Contains glycerol backbone with '
               'one fatty acid chain and phosphate group\n'
               ' * SMILES: P(OC[C@H](O)COC(=O)CCCCCCCCCCCCCCCCCCCCC)(O)(O)=O '
               'NAME: 1-docosanoyl-glycero-3-phosphate REASON: CORRECT '
               'Contains glycerol backbone with one fatty acid chain and '
               'phosphate group\n'
               ' * SMILES: '
               'P(OC[C@H](O)COC(=O)CCCCCCCCC/C=C\\CCCCCCCCCC)(O)(O)=O NAME: '
               '1-(11Z-docosenoyl)-glycero-3-phosphate REASON: CORRECT '
               'Contains glycerol backbone with one fatty acid chain and '
               'phosphate group\n'
               ' * SMILES: CCCCCCCC\\C=C/CCCCCCCC(=O)OC[C@@H](O)COP(O)(O)=O '
               'NAME: 1-oleoyl-sn-glycerol 3-phosphate REASON: CORRECT '
               'Contains glycerol backbone with one fatty acid chain and '
               'phosphate group\n'
               ' * SMILES: '
               'P(OC[C@H](O)COC(=O)CCCCCCCCCCC/C=C\\C/C=C\\CCCCC)(O)(O)=O '
               'NAME: 1-(13Z,16Z-docosadienoyl)-glycero-3-phosphate REASON: '
               'CORRECT Contains glycerol backbone with one fatty acid chain '
               'and phosphate group\n'
               ' * SMILES: P(OC[C@H](O)COC(=O)CCCCCCCCC/C=C\\CCCCCCCC)(O)(O)=O '
               'NAME: (2R)-2-Hydroxy-3-(phosphonooxy)propyl '
               '(11Z)-11-icosenoate REASON: CORRECT Contains glycerol backbone '
               'with one fatty acid chain and phosphate group\n'
               ' * SMILES: P(OC[C@H](OC(=O)CCCCCCCCCCCCCCC)CO)(O)(O)=O NAME: '
               'LPA(0:0/16:0) REASON: CORRECT Contains glycerol backbone with '
               'one fatty acid chain and phosphate group\n'
               ' * SMILES: '
               'P(OC[C@H](O)COC(=O)CC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)(O)(O)=O '
               'NAME: '
               '1-(4Z,7Z,10Z,13Z,16Z,19Z-docosahexaenoyl)-glycero-3-phosphate '
               'REASON: CORRECT Contains glycerol backbone with one fatty acid '
               'chain and phosphate group\n'
               ' * SMILES: P(OC[C@H](O)COC(=O)CCCCCCCCCCCCCCCCCC)(O)(O)=O '
               'NAME: 1-nonadecanoyl-glycero-3-phosphate REASON: CORRECT '
               'Contains glycerol backbone with one fatty acid chain and '
               'phosphate group\n'
               ' * SMILES: P(OC[C@H](O)COC(=O)CCCCCCC/C=C\\CCCCCCC)(O)(O)=O '
               'NAME: PA(17:1(9Z)/0:0) REASON: CORRECT Contains glycerol '
               'backbone with one fatty acid chain and phosphate group\n'
               ' * SMILES: CCCCCCCCCCCCCCCC(=O)OCC(O)COP(O)(O)=O NAME: '
               '1-palmitoylglycerol 3-phosphate REASON: CORRECT Contains '
               'glycerol backbone with one fatty acid chain and phosphate '
               'group\n'
               ' * SMILES: P(OCC(O)COC(=O)CCCCCCC/C=C\\C/C=C\\CCCCC)(O)(O)=O '
               'NAME: LysoPA(18:2(9Z,12Z)/0:0) REASON: CORRECT Contains '
               'glycerol backbone with one fatty acid chain and phosphate '
               'group\n'
               'False positives: SMILES: NC[C@H](CC[C@H](N)C(O)=O)OP(O)(O)=O '
               'NAME: Phosphoallohydroxy-L-lysine REASON: WRONGLY CLASSIFIED '
               'Contains glycerol backbone with one fatty acid chain and '
               'phosphate group\n'
               ' * SMILES: '
               'P(OC[C@H](OC(=O)CCCCCCCCCCC)CO/C=C\\CCCCCCCCCCCCCCCC)(O)(O)=O '
               'NAME: PA(P-18:0/12:0) REASON: WRONGLY CLASSIFIED Contains '
               'glycerol backbone with one fatty acid chain and phosphate '
               'group\n'
               ' * SMILES: CCCCCCC(CCCCCCCCCCC(O)=O)OP(O)(O)=O NAME: '
               '12-(phosphonooxy)octadecanoic acid REASON: WRONGLY CLASSIFIED '
               'Contains glycerol backbone with one fatty acid chain and '
               'phosphate group\n'
               ' * SMILES: '
               'P(OC[C@H](OC(=O)CCCC/C=C\\C/C=C\\C/C=C\\CCCCC)CO/C=C\\CCCCCCCCCCCCCC)(O)(O)=O '
               'NAME: PA(P-16:0/18:3(6Z,9Z,12Z)) REASON: WRONGLY CLASSIFIED '
               'Contains glycerol backbone with one fatty acid chain and '
               'phosphate group\n'
               ' * SMILES: '
               'P(OC[C@H](OC(=O)CCCC/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)CO/C=C\\CCCCCCCCCCCCCC)(O)(O)=O '
               'NAME: PA(P-16:0/18:4(6Z,9Z,12Z,15Z)) REASON: WRONGLY '
               'CLASSIFIED Contains glycerol backbone with one fatty acid '
               'chain and phosphate group\n'
               ' * SMILES: '
               'P(OC[C@H](OC(=O)CCCCCCCCC/C=C\\CCCCCCCCCC)COCCCCCCCCCCCCCCCCCC)(O)(O)=O '
               'NAME: PA(O-18:0/22:1(11Z)) REASON: WRONGLY CLASSIFIED Contains '
               'glycerol backbone with one fatty acid chain and phosphate '
               'group\n'
               ' * SMILES: '
               'P(OC[C@H](OC(=O)CCCCCCC/C=C\\C/C=C\\CCCCC)CO/C=C\\CCCCCCCCCCCCCC)(O)(O)=O '
               'NAME: PA(P-16:0/18:2(9Z,12Z)) REASON: WRONGLY CLASSIFIED '
               'Contains glycerol backbone with one fatty acid chain and '
               'phosphate group\n'
               ' * SMILES: '
               'C1(CCCCCCCCCCC2C(CCCCCCCCCCCCCCC[C@@H](O)C(C(OC[C@H]3O[C@H](O[C@H]4O[C@@H]([C@@H](O)[C@H](O)[C@H]4O)COP(O)(=O)O)[C@H](O)[C@@H](O)[C@@H]3O)=O)CCCCCCCCCCCCCCCCCCCCCCCCCC)C2)C(C1)CCCCCCCCCCCCCCCCCC '
               "NAME: 6'-O-mycolyltrehalose-6'phosphate REASON: WRONGLY "
               'CLASSIFIED Contains glycerol backbone with one fatty acid '
               'chain and phosphate group\n'
               ' * SMILES: '
               'P(OC[C@H](OC(=O)CCCCCCC/C=C\\C/C=C\\CCCC)CO/C=C\\CCCCCCCCCCCCCC)(O)(O)=O '
               'NAME: PA(P-16:0/17:2(9Z,12Z)) REASON: WRONGLY CLASSIFIED '
               'Contains glycerol backbone with one fatty acid chain and '
               'phosphate group\n'
               ' * SMILES: '
               'P(OC[C@H](OO)COC(=O)CCC/C=C\\C/C=C\\C/C=C\\C/C=C\\CCCCC)(O)(O)=O '
               'NAME: 1-arachidonoyl-2-hydroxy-sn-glycero-3-phosphate REASON: '
               'WRONGLY CLASSIFIED Contains glycerol backbone with one fatty '
               'acid chain and phosphate group\n'
               ' * SMILES: '
               'P(OC[C@H](OC(=O)CCCCCCCCCCCCCCCC)CO/C=C\\CCCCCCCCCCCCCC)(O)(O)=O '
               'NAME: PA(P-16:0/17:0) REASON: WRONGLY CLASSIFIED Contains '
               'glycerol backbone with one fatty acid chain and phosphate '
               'group\n'
               ' * SMILES: '
               'P(OC[C@H](OC(=O)CCCCCCCCC/C=C\\CCCCCCCC)COCCCCCCCCCCCCCCCC)(O)(O)=O '
               'NAME: PA(O-16:0/20:1(11Z)) REASON: WRONGLY CLASSIFIED Contains '
               'glycerol backbone with one fatty acid chain and phosphate '
               'group\n'
               ' * SMILES: '
               'P(OC[C@H](OC(=O)CCCCCCC/C=C\\CCCCCCCCC)COCCCCCCCCCCCCCCCCCC)(O)(O)=O '
               'NAME: PA(O-18:0/19:1(9Z)) REASON: WRONGLY CLASSIFIED Contains '
               'glycerol backbone with one fatty acid chain and phosphate '
               'group\n'
               ' * SMILES: '
               'P(OC[C@H](OC(=O)CCCCCCC/C=C\\CCCCCCC)COCCCCCCCCCCCCCCCCCCCC)(O)(O)=O '
               'NAME: PA(O-20:0/17:1(9Z)) REASON: WRONGLY CLASSIFIED Contains '
               'glycerol backbone with one fatty acid chain and phosphate '
               'group\n'
               ' * SMILES: '
               'C(CCCCCCC/C=C\\CCCCCCCC)(=O)O[C@@H](COP(=O)(O)O)CO/C=C\\CCCCCCCCCCCCCCCC '
               'NAME: 1-[(1Z)-octadecenyl]-2-oleoyl-sn-glycero-3-phosphate '
               'REASON: WRONGLY CLASSIFIED Contains glycerol backbone with one '
               'fatty acid chain and phosphate group\n'
               ' * SMILES: '
               'P(OC[C@H](OC(=O)CCCCCCCCCCCCC)COCCCCCCCCCCCCCCCC)(O)(O)=O '
               'NAME: PA(O-16:0/14:0) REASON: WRONGLY CLASSIFIED Contains '
               'glycerol backbone with one fatty acid chain and phosphate '
               'group\n'
               ' * SMILES: '
               'CC[C@@H]([C@H](C)OC(=O)CCCOP(O)(O)=O)n1ncn(-c2ccc(cc2)N2CCN(CC2)c2ccc(OC[C@@H]3CO[C@](Cn4cncn4)(C3)c3ccc(F)cc3F)cc2)c1=O '
               'NAME: Sch 59884 REASON: WRONGLY CLASSIFIED Contains glycerol '
               'backbone with one fatty acid chain and phosphate group\n'
               ' * SMILES: '
               'P(OC[C@H](OC(=O)CCCC/C=C\\C/C=C\\C/C=C\\CCCCC)COCCCCCCCCCCCCCCCCCC)(O)(O)=O '
               'NAME: PA(O-18:0/18:3(6Z,9Z,12Z)) REASON: WRONGLY CLASSIFIED '
               'Contains glycerol backbone with one fatty acid chain and '
               'phosphate group\n'
               ' * SMILES: '
               'P(OC[C@H](OC(=O)CCCCCCCCCCCCCCCCCCCC)CO/C=C\\CCCCCCCCCCCCCC)(O)(O)=O '
               'NAME: PA(P-16:0/21:0) REASON: WRONGLY CLASSIFIED Contains '
               'glycerol backbone with one fatty acid chain and phosphate '
               'group\n'
               ' * SMILES: '
               'P(=O)(OC1C(=CC=CCC(OC(=O)CC(=C)C(C)CC=CC=CC=CCCC1)CCC(=CC=C)C)C)(O)O '
               'NAME: Difficidin REASON: WRONGLY CLASSIFIED Contains glycerol '
               'backbone with one fatty acid chain and phosphate group\n'
               ' * SMILES: '
               'CCCCCCCC\\C=C/CCCCCCCCOC[C@H](COP(O)(O)=O)OC(=O)CCC\\C=C/C\\C=C/C\\C=C/C\\C=C/CCCCC '
               'NAME: 1-(9Z-octadecenyl)-2-arachidonoyl-sn-glycero-3-phosphate '
               'REASON: WRONGLY CLASSIFIED Contains glycerol backbone with one '
               'fatty acid chain and phosphate group\n'
               ' * SMILES: '
               'P(OC[C@H](OC(=O)CC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)CO/C=C\\CCCCCCCCCCCCCC)(O)(O)=O '
               'NAME: PA(P-16:0/22:6(4Z,7Z,10Z,13Z,16Z,19Z)) REASON: WRONGLY '
               'CLASSIFIED Contains glycerol backbone with one fatty acid '
               'chain and phosphate group\n'
               ' * SMILES: [C@@H]1(C(C(OC1)=O)C(CCCCC(C)C)=O)COP(O)(=O)O NAME: '
               '[(3S)-4-(6-methylheptanoyl)-5-oxooxolan-3-yl]methyl phosphate '
               'REASON: WRONGLY CLASSIFIED Contains glycerol backbone with one '
               'fatty acid chain and phosphate group\n'
               ' * SMILES: CCCCCCC(C\\C=C\\CCCCCCCC(O)=O)OP(O)(O)=O NAME: '
               '(9E)-12-(phosphonooxy)octadecenoic acid REASON: WRONGLY '
               'CLASSIFIED Contains glycerol backbone with one fatty acid '
               'chain and phosphate group\n'
               ' * SMILES: '
               'P(OC[C@H](OC(=O)CCCCC/C=C\\C/C=C\\C/C=C\\C/C=C\\CCCCC)CO/C=C\\CCCCCCCCCCCCCCCCCC)(O)(O)=O '
               'NAME: PA(P-20:0/22:4(7Z,10Z,13Z,16Z)) REASON: WRONGLY '
               'CLASSIFIED Contains glycerol backbone with one fatty acid '
               'chain and phosphate group\n'
               'False negatives: SMILES: '
               'OC[C@@H](COP(O)(=O)OC[C@H](CO)OC(CCCCCCC/C=C\\CCCCCCCC)=O)OC(CCCCCCC/C=C\\CCCCCCCC)=O '
               'NAME: (S,S)-bis(2-oleoylglycero)-1-phosphate REASON: MISSED No '
               'phosphate group found\n'
               ' * SMILES: '
               'OC[C@H](COP(O)(=O)OC[C@@H](CO)OC(CCCCCCC/C=C\\CCCCCCCC)=O)OC(CCCCCCC/C=C\\CCCCCCCC)=O '
               'NAME: (R,R)-bis(2-oleoylglycero)-3-phosphate REASON: MISSED No '
               'phosphate group found\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'Cc1cc(C)c2Cc3c(C)cc(C)c(Cc4c(C)cc(C)c(Cc5c(C)cc(C)c(Cc1c2C)c5C)c4C)c3C',
                                     'name': '4,6,10,12,16,18,22,24,25,26,27,28-dodecamethylcalix[4]arene',
                                     'reason': 'Missing core lysophosphatidic '
                                               'acid structure'},
                                 {   'smiles': 'O=C1C(=C2C=C3[C@]([C@@H](C(C)C)[C@@H]([C@H]3O)OC(=O)C)(C)CC[C@]2(C)CC1)COC(=O)C',
                                     'name': 'Dahliane E',
                                     'reason': 'Missing core lysophosphatidic '
                                               'acid structure'},
                                 {   'smiles': 'O[C@@H]([C@H](NC(=O)[C@@H](N)CCC(O)=O)C(=O)N[C@@H](CC(C)C)C(O)=O)C',
                                     'name': 'Glu-Thr-Leu',
                                     'reason': 'Missing core lysophosphatidic '
                                               'acid structure'},
                                 {   'smiles': 'CCOc1ccc(NC(=O)C(C)O)cc1',
                                     'name': 'p-Lactophenetide',
                                     'reason': 'Missing core lysophosphatidic '
                                               'acid structure'},
                                 {   'smiles': 'O=C1NCC=2C1=C3C(N([C@@H]4O[C@H]([C@@H](O)[C@H]([C@H]4OC)O)C)C5=C3C=CC=C5)=C6NC7=C(C26)C=CC=C7',
                                     'name': "3'-epi-5'-methoxy-K252d",
                                     'reason': 'Missing core lysophosphatidic '
                                               'acid structure'},
                                 {   'smiles': 'O=C(OC1C(O)C(OC(C1O)CO)OCC2OC(OCC(OC(=O)CCCCCCCCCCCCCCC)COC(=O)CCCCCCC/C=C\\C/C=C\\C/C=C\\CC)C(O)C(C2O)O)CCCCCCCCCCCCCCC',
                                     'name': '[(2S)-2-hexadecanoyloxy-3-[(2S,3R,4S,5S,6R)-6-[[(2S,3R,4S,5S,6R)-4-hexadecanoyloxy-3,5-dihydroxy-6-(hydroxymethyl)tetrahydropyran-2-yl]oxymethyl]-3,4,5-trihydroxy-tetrahydropyran-2-yl]oxy-propyl] '
                                             '(9E,12E,15E)-octadeca-9,12,15-trienoate',
                                     'reason': 'Missing core lysophosphatidic '
                                               'acid structure'},
                                 {   'smiles': 'O=C1C2=C(O)C=C(OC)C=C2C(=O)C3=C1[C@@H]([C@@H](O)[C@]([C@@H]3O)(O)C)C',
                                     'name': 'Altersolanol G',
                                     'reason': 'Missing core lysophosphatidic '
                                               'acid structure'},
                                 {   'smiles': '[H][C@]1(O[C@](O)(C[C@H](O)[C@H]1NC(=O)CO)C([O-])=O)[C@H](O)[C@H](O)CO',
                                     'name': 'N-glycoloyl-alpha-neuraminate',
                                     'reason': 'Missing core lysophosphatidic '
                                               'acid structure'},
                                 {   'smiles': 'OC(C(O)C/C=C\\C/C=C\\C/C=C\\CC)C/C=C\\C/C=C\\CCC(O)=O',
                                     'name': '10,11-DiHDPE',
                                     'reason': 'Missing core lysophosphatidic '
                                               'acid structure'},
                                 {   'smiles': '[Na+].[H][C@]12SCC(C)=C(N1C(=O)[C@H]2NC(=O)[C@H](N)c1ccccc1)C([O-])=O',
                                     'name': 'cephalexin sodium',
                                     'reason': 'Missing core lysophosphatidic '
                                               'acid structure'}],
    'sample_false_negatives': [   {   'smiles': 'CCCCC\\C=C/C\\C=C/C\\C=C/C\\C=C/CCCC(=O)O[C@H](CO)COP(O)(O)=O',
                                      'name': '2-arachidonoyl-sn-glycero-3-phosphate',
                                      'reason': 'Missing core lysophosphatidic '
                                                'acid structure'},
                                  {   'smiles': 'CCCCCCCC\\C=C/CCCCCCCC(=O)O[C@H](CO)COP(O)(O)=O',
                                      'name': '2-oleoyl-sn-glycero-3-phosphate',
                                      'reason': 'Missing core lysophosphatidic '
                                                'acid structure'},
                                  {   'smiles': 'CCCCC\\C=C/C\\C=C/CCCCCCCC(=O)O[C@H](CO)COP(O)(O)=O',
                                      'name': 'lysophosphatidic acid '
                                              '0:0/18:2(9Z,12Z)',
                                      'reason': 'Missing core lysophosphatidic '
                                                'acid structure'},
                                  {   'smiles': 'OC[C@@H](COP(O)(=O)OC[C@H](CO)OC(CCCCCCC/C=C\\CCCCCCCC)=O)OC(CCCCCCC/C=C\\CCCCCCCC)=O',
                                      'name': '(S,S)-bis(2-oleoylglycero)-1-phosphate',
                                      'reason': 'Missing core lysophosphatidic '
                                                'acid structure'},
                                  {   'smiles': 'P(OC[C@H](OC(=O)CCCCCCCCCCCCCCC)CO)(O)(O)=O',
                                      'name': 'LPA(0:0/16:0)',
                                      'reason': 'Missing core lysophosphatidic '
                                                'acid structure'},
                                  {   'smiles': 'P(OCC(OC(=O)CCCCCCC/C=C\\C/C=C\\CCCCC)CO)(O)(O)=O',
                                      'name': 'LysoPA(0:0/18:2(9Z,12Z))',
                                      'reason': 'Missing core lysophosphatidic '
                                                'acid structure'},
                                  {   'smiles': 'OC[C@H](COP(O)(=O)OC[C@@H](CO)OC(CCCCCCC/C=C\\CCCCCCCC)=O)OC(CCCCCCC/C=C\\CCCCCCCC)=O',
                                      'name': '(R,R)-bis(2-oleoylglycero)-3-phosphate',
                                      'reason': 'Missing core lysophosphatidic '
                                                'acid structure'},
                                  {   'smiles': 'C([C@@](CO)(OC(CCCCCCCCCCCCCCCCC)=O)[H])OP(O)(=O)O',
                                      'name': 'PA(0:0/18:0)',
                                      'reason': 'Missing core lysophosphatidic '
                                                'acid structure'},
                                  {   'smiles': 'P(OCC(OC(=O)CCC/C=C/C/C=C/C\\C=C\\C\\C=C\\CCCCC)CO)(O)(O)=O',
                                      'name': '1-Lyso-2-arachidonoyl-phosphatidate',
                                      'reason': 'Missing core lysophosphatidic '
                                                'acid structure'},
                                  {   'smiles': 'P(OCC(OC(=O)CCCCCCC/C=C\\CCCCCCCC)CO)(O)(O)=O',
                                      'name': 'LysoPA(0:0/18:1(9Z))',
                                      'reason': 'Missing core lysophosphatidic '
                                                'acid structure'}],
    'attempt': 1,
    'reasoning': 'Let me analyze the issues with the previous code based on '
                 'the outcomes:\n'
                 '\n'
                 '1. False Positives Analysis:\n'
                 '- Many false positives involve phosphate-containing '
                 "molecules that aren't true lysophosphatidic acids\n"
                 '- The code incorrectly classifies molecules with:\n'
                 '  * Phosphate esters in different contexts (like '
                 'phosphoallohydroxy-L-lysine)\n'
                 '  * Complex phospholipids with additional modifications '
                 '(like P-16:0 derivatives)\n'
                 '  * Molecules with phosphate groups but different core '
                 'structures\n'
                 '\n'
                 '2. False Negatives Analysis:\n'
                 '- The code misses some valid bis-glycerophosphates\n'
                 '- The phosphate pattern might be too restrictive\n'
                 '\n'
                 'Key improvements needed:\n'
                 '\n'
                 '1. More specific glycerol backbone pattern:\n'
                 '- Need to ensure the glycerol backbone is directly connected '
                 'to both the phosphate and ester group\n'
                 '- Should specify the correct stereochemistry\n'
                 '\n'
                 '2. Better phosphate group detection:\n'
                 '- Need to ensure the phosphate is specifically attached to '
                 'the glycerol backbone\n'
                 '- Should allow for different phosphate ionization states\n'
                 '\n'
                 '3. More specific connectivity requirements:\n'
                 '- Need to verify that the ester and phosphate are attached '
                 'to specific positions\n'
                 '- Should check for proper arrangement of functional groups\n'
                 '\n'
                 "Here's my improved version:",
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 41,
    'num_false_positives': 9,
    'num_true_negatives': 142240,
    'num_false_negatives': 10,
    'num_negatives': None,
    'precision': 0.82,
    'recall': 0.803921568627451,
    'f1': 0.8118811881188118,
    'accuracy': 0.9998664792691497,
    'negative_predictive_value': 0.9999297012302285}