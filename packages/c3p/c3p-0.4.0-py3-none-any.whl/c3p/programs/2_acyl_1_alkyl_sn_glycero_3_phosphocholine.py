"""
Classifies: CHEBI:36702 2-acyl-1-alkyl-sn-glycero-3-phosphocholine
"""
"""
Classifies: 2-acyl-1-alkyl-sn-glycero-3-phosphocholine
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_2_acyl_1_alkyl_sn_glycero_3_phosphocholine(smiles: str):
    """
    Determines if a molecule is a 2-acyl-1-alkyl-sn-glycero-3-phosphocholine based on its SMILES string.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a 2-acyl-1-alkyl-sn-glycero-3-phosphocholine, False otherwise
        str: Reason for classification
    """
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for complete phosphocholine group structure
    phosphocholine = Chem.MolFromSmarts("[O][P](=[O])([O-])OCC[N+](C)(C)C")
    if not mol.HasSubstructMatch(phosphocholine):
        return False, "No phosphocholine group found"
    
    # Count phosphocholine groups - should be exactly one
    phosphocholine_matches = len(mol.GetSubstructMatches(phosphocholine))
    if phosphocholine_matches != 1:
        return False, f"Found {phosphocholine_matches} phosphocholine groups, need exactly 1"

    # Check for glycerol backbone with correct stereochemistry and substitution pattern
    # [C@H] ensures the sn-glycero configuration
    glycerol_pattern = Chem.MolFromSmarts("[CH2X4]-[OX2]-[#6].[CH2X4]-[OX2]-[PX4].[C@H](-[OX2]-[CX3]=O)")
    if not mol.HasSubstructMatch(glycerol_pattern):
        return False, "Missing correct glycerol backbone structure with required substitution pattern"

    # Check for ether linkage at position 1 (any alkyl)
    ether_pattern = Chem.MolFromSmarts("[CH2X4]-[OX2]-[CX4]")
    if not mol.HasSubstructMatch(ether_pattern):
        return False, "No alkyl ether found at position 1"

    # Check for acyl group at position 2 (includes formyl)
    acyl_pattern = Chem.MolFromSmarts("[OX2]-[CX3](=[OX1])")
    acyl_matches = mol.GetSubstructMatches(acyl_pattern)
    if not acyl_matches:
        return False, "No acyl group found at position 2"

    # Verify correct connectivity
    glycerol_matches = mol.GetSubstructMatches(glycerol_pattern)
    if not glycerol_matches:
        return False, "Incorrect connectivity in glycerol backbone"

    # Check stereochemistry
    chiral_centers = Chem.FindMolChiralCenters(mol)
    if not any('@' in smiles for match in chiral_centers):
        return False, "Missing or incorrect stereochemistry"

    # Verify minimum size requirements
    n_carbons = sum(1 for atom in mol.GetAtoms() if atom.GetAtomicNum() == 6)
    if n_carbons < 8:  # Minimum size considering the basic structure
        return False, "Molecule too small for expected structure"

    # Check for required number of oxygens
    n_oxygens = sum(1 for atom in mol.GetAtoms() if atom.GetAtomicNum() == 8)
    if n_oxygens < 6:  # 1 ether + 2 acyl + 3 phosphate
        return False, "Insufficient oxygen atoms for required functional groups"

    return True, "Contains glycerol backbone with alkyl ether at position 1, acyl group at position 2, and phosphocholine at position 3"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:36702',
                          'name': '2-acyl-1-alkyl-sn-glycero-3-phosphocholine',
                          'definition': 'An '
                                        'alkyl,acyl-sn-glycero-3-phosphocholine '
                                        'in which unspecified alkyl and acyl '
                                        'groups are located at positions 1 and '
                                        '2 respectively.',
                          'parents': [   'CHEBI:35284',
                                         'CHEBI:68489',
                                         'CHEBI:78186'],
                          'xrefs': ['KEGG:C05212'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': None,
    'message': '\n'
               'Attempt failed: F1 score of 0.5312500000000001 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: '
               'CCCCCCCCCCCCCCCCOC[C@H](COP([O-])(=O)OCC[N+](C)(C)C)OC(=O)CCCCCCC\\C=C/CCCCCCCCCC '
               'NAME: '
               '1-hexadecyl-2-[(9Z)-eicosenoyl]-sn-glycero-3-phosphocholine '
               'REASON: CORRECT Contains glycerol backbone with alkyl ether at '
               'position 1, acyl group at position 2, and phosphocholine at '
               'position 3\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCOC[C@H](COP([O-])(=O)OCC[N+](C)(C)C)OC(=O)CCCCCCC\\C=C/CCCCCCCC '
               'NAME: '
               '1-tetradecyl-2-[(9Z)-octadecenoyl]-sn-glycero-3-phosphocholine '
               'REASON: CORRECT Contains glycerol backbone with alkyl ether at '
               'position 1, acyl group at position 2, and phosphocholine at '
               'position 3\n'
               ' * SMILES: '
               'CCCCCCCCCCCCOC[C@H](COP([O-])(=O)OCC[N+](C)(C)C)OC(C)=O NAME: '
               '1-dodecyl-2-acetyl-sn-glycero-3-phosphocholine REASON: CORRECT '
               'Contains glycerol backbone with alkyl ether at position 1, '
               'acyl group at position 2, and phosphocholine at position 3\n'
               ' * SMILES: '
               'P(OC[C@@H](COCCCCCCCCCCCCCCCCCC)OC(C)=O)(=O)(OCC[N+](C)(C)C)[O-] '
               'NAME: 2-O-acetyl-1-O-octadecyl-sn-glycero-3-phosphocholine '
               'REASON: CORRECT Contains glycerol backbone with alkyl ether at '
               'position 1, acyl group at position 2, and phosphocholine at '
               'position 3\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCCOC[C@H](COP([O-])(=O)OCC[N+](C)(C)C)OC(=O)CCCCCCCCCCC\\C=C/C\\C=C/CCCCC '
               'NAME: '
               '1-octadecyl-2-[(13Z,16Z)-docosadienoyl]-sn-glycero-3-phosphocholine '
               'REASON: CORRECT Contains glycerol backbone with alkyl ether at '
               'position 1, acyl group at position 2, and phosphocholine at '
               'position 3\n'
               ' * SMILES: '
               'C([C@@](COCCCCCCCCCCCCCCCC)(OC(CCCCCCC/C=C\\CCCCCCCCC)=O)[H])OP(OCC[N+](C)(C)C)(=O)[O-] '
               'NAME: 1-hexadecyl-2-(9Z-nonadecenoyl)-glycero-3-phosphocholine '
               'REASON: CORRECT Contains glycerol backbone with alkyl ether at '
               'position 1, acyl group at position 2, and phosphocholine at '
               'position 3\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCOC[C@H](COP([O-])(=O)OCC[N+](C)(C)C)OC(=O)CCCCCCCCC\\C=C/C\\C=C/CCCCC '
               'NAME: '
               '1-hexadecyl-2-[(11Z,14Z)-eicosadienoyl]-sn-glycero-3-phosphocholine '
               'REASON: CORRECT Contains glycerol backbone with alkyl ether at '
               'position 1, acyl group at position 2, and phosphocholine at '
               'position 3\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCOC[C@H](COP([O-])(=O)OCC[N+](C)(C)C)OC(=O)CC\\C=C/C\\C=C/C\\C=C/C\\C=C/C\\C=C/C\\C=C/CC '
               'NAME: '
               '1-hexadecyl-2-[(4Z,7Z,10Z,13Z,16Z,19Z)-docosahexaenoyl]-sn-glycero-3-phosphocholine '
               'REASON: CORRECT Contains glycerol backbone with alkyl ether at '
               'position 1, acyl group at position 2, and phosphocholine at '
               'position 3\n'
               ' * SMILES: '
               '[H][C@@](COCCCCCCCCCCCCCCCCCC)(COP([O-])(=O)OCC[N+](C)(C)C)OC(=O)CCCCCCCCCCCCCCCCCCC '
               'NAME: 1-octadecyl-2-icosanoyl-sn-glycero-3-phosphocholine '
               'REASON: CORRECT Contains glycerol backbone with alkyl ether at '
               'position 1, acyl group at position 2, and phosphocholine at '
               'position 3\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCCCCCCCCOC[C@H](COP([O-])(=O)OCC[N+](C)(C)C)OC(=O)CCCCCC\\C=C/C\\C=C/C\\C=C/C\\C=C/CC '
               'NAME: '
               '1-tetracosyl-2-[(8Z,11Z,14Z,17Z)-icosatetraenoyl]-sn-glycero-3-phosphocholine '
               'REASON: CORRECT Contains glycerol backbone with alkyl ether at '
               'position 1, acyl group at position 2, and phosphocholine at '
               'position 3\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCCCCCC(=O)O[C@H](COCCCCCCCCCCCCCCCCCCCC)COP([O-])(=O)OCC[N+](C)(C)C '
               'NAME: 1-eicosyl-2-docosanoyl-sn-glycero-3-phosphocholine '
               'REASON: CORRECT Contains glycerol backbone with alkyl ether at '
               'position 1, acyl group at position 2, and phosphocholine at '
               'position 3\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCOC[C@H](COP([O-])(=O)OCC[N+](C)(C)C)OC(=O)CCC '
               'NAME: 1-hexadecyl-2-butanoyl-sn-glycero-3-phosphocholine '
               'REASON: CORRECT Contains glycerol backbone with alkyl ether at '
               'position 1, acyl group at position 2, and phosphocholine at '
               'position 3\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCCCCCC(=O)O[C@H](COCCCCCCCCCCCCCCCCCC)COP([O-])(=O)OCC[N+](C)(C)C '
               'NAME: 1-octadecyl-2-docosanoyl-sn-glycero-3-phosphocholine '
               'REASON: CORRECT Contains glycerol backbone with alkyl ether at '
               'position 1, acyl group at position 2, and phosphocholine at '
               'position 3\n'
               ' * SMILES: '
               'C(C[N+](C)(C)C)OP(=O)([O-])OC[C@H](OC(=O)C)COCCCCCCCCCCCCCCC '
               'NAME: 1-pentadecyl-2-acetyl-sn-glycero-3-phosphocholine '
               'REASON: CORRECT Contains glycerol backbone with alkyl ether at '
               'position 1, acyl group at position 2, and phosphocholine at '
               'position 3\n'
               ' * SMILES: '
               'C(C[N+](C)(C)C)OP(=O)([O-])OC[C@H](OC(=O)C)COCCCCCCCC/C=C\\CCCCCC '
               'NAME: '
               '1-[(9Z)-hexadecenyl]-2-acetyl-sn-glycero-3-phosphocholine '
               'REASON: CORRECT Contains glycerol backbone with alkyl ether at '
               'position 1, acyl group at position 2, and phosphocholine at '
               'position 3\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCCCCCC(=O)O[C@H](COCCCCCCCCCCCCCCCC)COP([O-])(=O)OCC[N+](C)(C)C '
               'NAME: 1-hexadecyl-2-docosanoyl-sn-glycero-3-phosphocholine '
               'REASON: CORRECT Contains glycerol backbone with alkyl ether at '
               'position 1, acyl group at position 2, and phosphocholine at '
               'position 3\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCOC[C@H](COP([O-])(=O)OCC[N+](C)(C)C)OC(=O)CCCCCCC\\C=C/CCCCCCCC '
               'NAME: 1-O-hexadecyl-2-oleoyl-sn-glycero-3-phosphocholine '
               'REASON: CORRECT Contains glycerol backbone with alkyl ether at '
               'position 1, acyl group at position 2, and phosphocholine at '
               'position 3\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCCOC[C@H](COP([O-])(=O)OCC[N+](C)(C)C)OC(=O)CCCCC\\C=C/C\\C=C/C\\C=C/C\\C=C/CCCCC '
               'NAME: '
               '1-octadecyl-2-[(7Z,10Z,13Z,16Z)-docosatetraenoyl]-sn-glycero-3-phosphocholine '
               'REASON: CORRECT Contains glycerol backbone with alkyl ether at '
               'position 1, acyl group at position 2, and phosphocholine at '
               'position 3\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCCOC[C@H](COP([O-])(=O)OCC[N+](C)(C)C)OC(=O)CCCCCC\\C=C/C\\C=C/C\\C=C/CCCCC '
               'NAME: '
               '1-octadecyl-2-[(8Z,11Z,14Z)-eicosatrienoyl]-sn-glycero-3-phosphocholine '
               'REASON: CORRECT Contains glycerol backbone with alkyl ether at '
               'position 1, acyl group at position 2, and phosphocholine at '
               'position 3\n'
               ' * SMILES: '
               'P(OC[C@@H](COCCCCCCCCCCCCCCCC)OC(CCC/C=C\\C/C=C\\C/C=C\\C/C=C\\CCCCC)=O)(=O)(OCC[N+](C)(C)C)[O-] '
               'NAME: 1-O-hexadecyl-2-arachidonoyl-sn-glycero-3-phosphocholine '
               'REASON: CORRECT Contains glycerol backbone with alkyl ether at '
               'position 1, acyl group at position 2, and phosphocholine at '
               'position 3\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCCCCCCOC[C@H](COP([O-])(=O)OCC[N+](C)(C)C)OC(=O)CCCCCCCC\\C=C/C\\C=C/C\\C=C/CCCCC '
               'NAME: '
               '1-docosyl-2-[(10Z,13Z,16Z)-docosatrienoyl]-sn-glycero-3-phosphocholine '
               'REASON: CORRECT Contains glycerol backbone with alkyl ether at '
               'position 1, acyl group at position 2, and phosphocholine at '
               'position 3\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCCOC[C@H](COP([O-])(=O)OCC[N+](C)(C)C)OC(=O)CCCCCCCCCCCCCCC '
               'NAME: 1-O-octadecyl-2-palmitoyl-sn-glycero-3-phosphocholine '
               'REASON: CORRECT Contains glycerol backbone with alkyl ether at '
               'position 1, acyl group at position 2, and phosphocholine at '
               'position 3\n'
               ' * SMILES: '
               'C(C[N+](C)(C)C)OP(=O)([O-])OC[C@H](OC(CCCCO)=O)COCCCCCCCCCCCCCCCC '
               'NAME: '
               '1-O-hexadecyl-2-(5-hydroxyvaleroyl)-sn-glycero-3-phosphocholine '
               'REASON: CORRECT Contains glycerol backbone with alkyl ether at '
               'position 1, acyl group at position 2, and phosphocholine at '
               'position 3\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCCOC[C@H](COP([O-])(=O)OCC[N+](C)(C)C)OC(=O)CCCCCCCCC\\C=C/C\\C=C/CCCCC '
               'NAME: '
               '1-octadecyl-2-[(11Z,14Z)-eicosadienoyl]-sn-glycero-3-phosphocholine '
               'REASON: CORRECT Contains glycerol backbone with alkyl ether at '
               'position 1, acyl group at position 2, and phosphocholine at '
               'position 3\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCCCCC(=O)O[C@H](COCCCCCCCCCCCCCCCC)COP([O-])(=O)OCC[N+](C)(C)C '
               'NAME: 1-hexadecyl-2-eicosanoyl-sn-glycero-3-phosphocholine '
               'REASON: CORRECT Contains glycerol backbone with alkyl ether at '
               'position 1, acyl group at position 2, and phosphocholine at '
               'position 3\n'
               'False positives: SMILES: '
               'P(OCC[N+]1(CCCC1)C)(OC[C@H](OC(=O)C)COCCCCCCCCCCCCCCCC)([O-])=O '
               'NAME: Pyrrolidinium, '
               '1-[(7r)-7-(acetyloxy)-4-hydroxy-4-oxido-3,5,9-trioxa-4-phosphapentacos-1-yl]-1-methyl-, '
               'inner salt REASON: WRONGLY CLASSIFIED Contains glycerol '
               'backbone with alkyl ether at position 1, acyl group at '
               'position 2, and phosphocholine at position 3\n'
               ' * SMILES: '
               'O(C[C@](COP([O-])(=O)OCC[N+](C)(C)C)(OC(CCCCCCCCCCC/C=C\\C/C=C\\CCCCC)=O)[H])CCCCCCCCCCCC/C=C\\C/C=C\\CCCCC '
               'NAME: PC(o-22:2(13Z,16Z)/22:2(13Z,16Z)) REASON: WRONGLY '
               'CLASSIFIED Contains glycerol backbone with alkyl ether at '
               'position 1, acyl group at position 2, and phosphocholine at '
               'position 3\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCOC[C@H](COP([O-])(=O)OCC[N+](C)(C)C)OC(=O)CCC([O-])=O '
               'NAME: 1-hexadecyl-2-succinyl-sn-glycero-3-phosphocholine(1-) '
               'REASON: WRONGLY CLASSIFIED Contains glycerol backbone with '
               'alkyl ether at position 1, acyl group at position 2, and '
               'phosphocholine at position 3\n'
               ' * SMILES: '
               'O(C[C@](COP([O-])(=O)OCC[N+](C)(C)C)(OC(CCCCCCCCCCCCCCCCCCC)=O)[H])CCCCCCCC/C=C\\C/C=C\\CCCCC '
               'NAME: PC(o-18:2(9Z,12Z)/20:0) REASON: WRONGLY CLASSIFIED '
               'Contains glycerol backbone with alkyl ether at position 1, '
               'acyl group at position 2, and phosphocholine at position 3\n'
               ' * SMILES: '
               'P(OCC[N+](C)(C)C)(OCC(OC(=O)CCCC)COCCCCCCCC/C=C\\CCC)([O-])=O '
               'NAME: PC O-18:1 REASON: WRONGLY CLASSIFIED Contains glycerol '
               'backbone with alkyl ether at position 1, acyl group at '
               'position 2, and phosphocholine at position 3\n'
               ' * SMILES: '
               'P(OCC[N+](C)(C)C)(OC[C@H](OC(=O)CCC/C=C\\C/C=C\\C/C=C\\C/C=C\\CCCCC)COCCCCCCCCCCCC/C=C\\CCCCCCCC)([O-])=O '
               'NAME: PC(o-22:1(13Z)/20:4(8Z,11Z,14Z,17Z)) REASON: WRONGLY '
               'CLASSIFIED Contains glycerol backbone with alkyl ether at '
               'position 1, acyl group at position 2, and phosphocholine at '
               'position 3\n'
               ' * SMILES: '
               'O(C[C@](COP([O-])(=O)OCC[N+](C)(C)C)(OC(CCCCCCC/C=C\\C/C=C\\CCCCC)=O)[H])CCCCCCCCCCCCCCCCCC '
               'NAME: PC(o-18:0/18:2(9Z,12Z)) REASON: WRONGLY CLASSIFIED '
               'Contains glycerol backbone with alkyl ether at position 1, '
               'acyl group at position 2, and phosphocholine at position 3\n'
               ' * SMILES: '
               'CCCCCCCCCCCCCCCCOC[C@H](COP([O-])(=O)OCC[N+](C)(C)C)OC(=O)CCCC([O-])=O '
               'NAME: 1-hexadecyl-2-glutaryl-sn-glycero-3-phosphocholine(1-) '
               'REASON: WRONGLY CLASSIFIED Contains glycerol backbone with '
               'alkyl ether at position 1, acyl group at position 2, and '
               'phosphocholine at position 3\n'
               ' * SMILES: '
               'P(OCC[N+](C)(C)C)(OC[C@H](OC(=O)C)COCCCCCCCCCC/C=C\\CCCC)([O-])=O '
               'NAME: PC(O-16:1(11Z)/2:0) REASON: WRONGLY CLASSIFIED Contains '
               'glycerol backbone with alkyl ether at position 1, acyl group '
               'at position 2, and phosphocholine at position 3\n'
               ' * SMILES: '
               'O(C[C@](COP([O-])(=O)OCC[N+](C)(C)C)(OC(CCCCCCCCCCCCCCCCC)=O)[H])CCCCCCCC/C=C\\CCCCCCCC '
               'NAME: PC(o-18:1(9Z)/18:0) REASON: WRONGLY CLASSIFIED Contains '
               'glycerol backbone with alkyl ether at position 1, acyl group '
               'at position 2, and phosphocholine at position 3\n'
               ' * SMILES: '
               'P(OCC[N+](C)(C)C)(OC[C@H](OC(=O)CCCCCCCCCCCCCCCCCCCC)COCCCCCCCCCCCCCCCCCCCC)([O-])=O '
               'NAME: PC(O-20:0/21:0) REASON: WRONGLY CLASSIFIED Contains '
               'glycerol backbone with alkyl ether at position 1, acyl group '
               'at position 2, and phosphocholine at position 3\n'
               ' * SMILES: '
               'P(OCC[N+](C)(C)C)(OC[C@H](OC(=O)CCCCCCCCCCCCCCCC)COCCCCCCCCCCCCCCCC)([O-])=O '
               'NAME: PC(O-16:0/17:0) REASON: WRONGLY CLASSIFIED Contains '
               'glycerol backbone with alkyl ether at position 1, acyl group '
               'at position 2, and phosphocholine at position 3\n'
               ' * SMILES: '
               'P(OCC[N+](C)(C)C)(OCC(OC(=O)CCC=CCC=CCC=CCC=CCC=CCC=CCC)COCCCCCCCCCCCCCCCC)([O-])=O '
               'NAME: '
               '2-O-(4,7,10,13,16,19-Docosahexaenoyl)-1-O-hexadecylglycero-3-phosphocholine '
               'REASON: WRONGLY CLASSIFIED Contains glycerol backbone with '
               'alkyl ether at position 1, acyl group at position 2, and '
               'phosphocholine at position 3\n'
               ' * SMILES: '
               'P(OCC[N+](C)(C)C)(OC[C@H](OC(=O)CCCC)COCCCCCCCCCCCCCCCC)([O-])=O '
               'NAME: PC(O-16:0/5:0) REASON: WRONGLY CLASSIFIED Contains '
               'glycerol backbone with alkyl ether at position 1, acyl group '
               'at position 2, and phosphocholine at position 3\n'
               ' * SMILES: '
               'P(OCC[N+](C)(C)C)(OC[C@H](OC(=O)CCCCCCCCCCCCCCCCCCCCC)COCCCCCCCCCCCCCCCCCCC)([O-])=O '
               'NAME: PC(O-19:0/22:0) REASON: WRONGLY CLASSIFIED Contains '
               'glycerol backbone with alkyl ether at position 1, acyl group '
               'at position 2, and phosphocholine at position 3\n'
               ' * SMILES: '
               'O(C[C@](COP([O-])(=O)OCC[N+](C)(C)C)(OC(CCCCCCC/C=C\\C/C=C\\C/C=C\\CC)=O)[H])CCCCCCCCCCCCCCCCCCCC '
               'NAME: PC(o-20:0/18:3(9Z,12Z,15Z)) REASON: WRONGLY CLASSIFIED '
               'Contains glycerol backbone with alkyl ether at position 1, '
               'acyl group at position 2, and phosphocholine at position 3\n'
               ' * SMILES: '
               'C(=O)(CCCCCCCC([O-])=O)O[C@@H](COP(=O)(OCC[N+](C)(C)C)[O-])COCCCCCCCCCCCCCCCC '
               'NAME: '
               '1-O-hexadecyl-2-(8-carboxyoctanoyl)-sn-glycero-3-phosphocholine(1-) '
               'REASON: WRONGLY CLASSIFIED Contains glycerol backbone with '
               'alkyl ether at position 1, acyl group at position 2, and '
               'phosphocholine at position 3\n'
               ' * SMILES: '
               'O(C[C@](COP([O-])(=O)OCC[N+](C)(C)C)(OC(CCCCCCCCCCCCCCCCCCCCCCC)=O)[H])CCCCCCCC/C=C\\C/C=C\\CCCCC '
               'NAME: PC(o-18:2(9Z,12Z)/24:0) REASON: WRONGLY CLASSIFIED '
               'Contains glycerol backbone with alkyl ether at position 1, '
               'acyl group at position 2, and phosphocholine at position 3\n'
               ' * SMILES: '
               'O(C[C@](COP([O-])(=O)OCC[N+](C)(C)C)(OC(CCCCCCCCC/C=C\\CCCCCCCC)=O)[H])CCCCCCCC/C=C\\CCCCCCCC '
               'NAME: PC(o-18:1(9Z)/20:1(11Z)) REASON: WRONGLY CLASSIFIED '
               'Contains glycerol backbone with alkyl ether at position 1, '
               'acyl group at position 2, and phosphocholine at position 3\n'
               ' * SMILES: '
               'P(OCC[N+](C)(C)C)(OCC(OC(=O)CC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\C=C\\C(O)CC)COCCCCCCCCCCCCCCCCCC)([O-])=O '
               'NAME: Pc(18:0e/20-hdohe) REASON: WRONGLY CLASSIFIED Contains '
               'glycerol backbone with alkyl ether at position 1, acyl group '
               'at position 2, and phosphocholine at position 3\n'
               ' * SMILES: '
               'P(OCC[N+](C)(C)C)(OC[C@H](OC(=O)C)COCCCCCCCC/C=C\\C/C=C\\CCCCC)([O-])=O '
               'NAME: PC(O-18:2(9Z,12Z)/2:0) REASON: WRONGLY CLASSIFIED '
               'Contains glycerol backbone with alkyl ether at position 1, '
               'acyl group at position 2, and phosphocholine at position 3\n'
               ' * SMILES: '
               'O(C[C@](COP([O-])(=O)OCC[N+](C)(C)C)(OC(CCCCCCCCCCCCCCCCC)=O)[H])CCCCCCCC/C=C\\CCCCCC '
               'NAME: PC(o-16:1(9Z)/18:0) REASON: WRONGLY CLASSIFIED Contains '
               'glycerol backbone with alkyl ether at position 1, acyl group '
               'at position 2, and phosphocholine at position 3\n'
               ' * SMILES: '
               'O(C[C@](COP([O-])(=O)OCC[N+](C)(C)C)(OC(CCCCCCCC/C=C\\C/C=C\\C/C=C\\CCCCC)=O)[H])CCCCCCCCCCCC/C=C\\CCCCCCCC '
               'NAME: PC(o-22:1(13Z)/22:3(10Z,13Z,16Z)) REASON: WRONGLY '
               'CLASSIFIED Contains glycerol backbone with alkyl ether at '
               'position 1, acyl group at position 2, and phosphocholine at '
               'position 3\n'
               ' * SMILES: '
               'O(C[C@](COP([O-])(=O)OCC[N+](C)(C)C)(OC(CCCCCCCCCCC/C=C\\C/C=C\\CCCCC)=O)[H])CCCCCCCCCCCC/C=C\\CCCCCCCC '
               'NAME: PC(o-22:1(13Z)/22:2(13Z,16Z)) REASON: WRONGLY CLASSIFIED '
               'Contains glycerol backbone with alkyl ether at position 1, '
               'acyl group at position 2, and phosphocholine at position 3\n'
               ' * SMILES: '
               'P(OCC[N+](C)(C)C)(OC[C@H](OC(=O)C)COCCCCCCCC/C=C\\CCCCCCCC)([O-])=O '
               'NAME: PC(18:1(9Z)e/2:0) REASON: WRONGLY CLASSIFIED Contains '
               'glycerol backbone with alkyl ether at position 1, acyl group '
               'at position 2, and phosphocholine at position 3\n'
               'False negatives: SMILES: '
               'CCCCCCCCCCCCCCCCOC[C@H](COP([O-])(=O)OCC[N+](C)(C)C)OC(=O)CCC(O)=O '
               'NAME: 1-hexadecyl-2-succinyl-sn-glycero-3-phosphocholine '
               'REASON: MISSED Found 2 ester groups, need exactly 1\n'
               ' * SMILES: '
               'C(OP(=O)(OCC[N+](C)(C)C)[O-])[C@@H](COC)OC(CCCCCCCCCCCCCCC)=O '
               'NAME: 1-methyl-2-hexadecanoyl-sn-glycero-3-phosphocholine '
               'REASON: MISSED No long-chain alkyl ether found at position 1\n'
               ' * SMILES: '
               'C(C[N+](C)(C)C)OP(=O)([O-])OC[C@H](OC(=O)[H])COCCCCCCCCCCCCCCCC '
               'NAME: 1-hexadecyl-2-formyl-sn-glycero-3-phosphocholine REASON: '
               'MISSED Found 0 ester groups, need exactly 1\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'CCOC(=O)C1=C2CN(C(=O)C3=C(N2C=N1)C=CC(=C3)N=[N+]=[N-])C',
                                     'name': '8-azido-5-methyl-6-oxo-4H-imidazo[1,5-a][1,4]benzodiazepine-3-carboxylic '
                                             'acid ethyl ester',
                                     'reason': 'No phosphocholine group found'},
                                 {   'smiles': 'CCCN(C)C[C@H]1[C@@H](CN(S(=O)(=O)C2=C(O1)C=C(C=C2)C#CCC3CCCC3)[C@@H](C)CO)C',
                                     'name': '(2S)-2-[(4R,5R)-8-(3-cyclopentylprop-1-ynyl)-4-methyl-5-[[methyl(propyl)amino]methyl]-1,1-dioxo-4,5-dihydro-3H-6,1$l^{6},2-benzoxathiazocin-2-yl]-1-propanol',
                                     'reason': 'No phosphocholine group found'},
                                 {   'smiles': 'O=C(N[C@@H](CCC(=O)N)C(O)=O)[C@@H](NC(=O)[C@@H](N)CC1=CC=CC=C1)[C@H](CC)C',
                                     'name': 'Phe-Ile-Gln',
                                     'reason': 'No phosphocholine group found'},
                                 {   'smiles': 'C1CCN2[C@H](CN(C1)CC3CCOCC3)[C@@H]([C@@H]2CO)C4=CC=C(C=C4)C#CC5=CC=CC=C5F',
                                     'name': '[(8S,9S,10R)-9-[4-[2-(2-fluorophenyl)ethynyl]phenyl]-6-(4-oxanylmethyl)-1,6-diazabicyclo[6.2.0]decan-10-yl]methanol',
                                     'reason': 'No phosphocholine group found'},
                                 {   'smiles': 'O=C1N[C@H](C(=O)N[C@H](C(=O)O)CC2=CC=CC=C2)CCC(=O)NCCCC[C@@H]3NC(=O)[C@H](CC(C)C)NC([C@H]([C@H](OC(C[C@H]4C(N[C@H](C(N[C@H]1CCC(=O)OC[C@H](NC(=O)[C@H]5N(C(=O)[C@H](CC6=CC=C(O)C=C6)NC3=O)CCC5)C(=O)N4)=O)CC=7C8=C(C=CC=C8)NC7)=O)=O)C)NC(=O)[C@@H](N)C(C)C)=O',
                                     'name': 'Microviridin M',
                                     'reason': 'No phosphocholine group found'},
                                 {   'smiles': 'O=C1O[C@H](C(=O)N[C@H](C(=O)O[C@H](C(=O)N([C@@H](C(N[C@@H](C(N([C@H]1C)C)=O)C)=O)CC2=CC=CC=C2)C)CC(C)C)C)C(C)C',
                                     'name': 'Guangomide B',
                                     'reason': 'No phosphocholine group found'},
                                 {   'smiles': 'C=1C(=C(C=C2C1CC[NH+]3C[C@@H]([C@@](C[C@@]23[H])([H])C[C@@]4([H])[NH2+]CCC=5C4=CC(=C(C5)O)OC)CC)OC)OC',
                                     'name': 'cephaeline(2+)',
                                     'reason': 'No phosphocholine group found'},
                                 {   'smiles': 'O=C1NCC[C@H](O)C[C@H](NC(=O)[C@@H](NC(=O)/C=C/C=C/CCCCCCCCC)[C@H](O)C)C(N[C@H](C=C1)C)=O',
                                     'name': 'Glidobactin C',
                                     'reason': 'No phosphocholine group found'},
                                 {   'smiles': '[K+].[O-][N+]([O-])=O',
                                     'name': 'potassium nitrate',
                                     'reason': 'No phosphocholine group found'},
                                 {   'smiles': 'O=C1NCC2=C1C=C(O)C3=C2OC4(C5(C(C(C(O)CC5)(C)C)CCC4C)C)C3',
                                     'name': 'Stachybotrylactam',
                                     'reason': 'No phosphocholine group '
                                               'found'}],
    'sample_false_negatives': [],
    'attempt': 2,
    'reasoning': 'Let me analyze the issues with the previous code:\n'
                 '\n'
                 '1. False Positives Analysis:\n'
                 '- Many of the false positives are actually valid structures '
                 'but with different nomenclature (e.g., '
                 'PC(o-18:2(9Z,12Z)/24:0)). This suggests our core detection '
                 'is working.\n'
                 "- The main issue isn't with incorrect detection but rather "
                 'with being too permissive.\n'
                 '\n'
                 '2. False Negatives Analysis:\n'
                 '- The formyl group case was missed because we were too '
                 'strict with the ester pattern.\n'
                 '- The methyl case was missed because our alkyl ether pattern '
                 'was too specific.\n'
                 '- The succinyl case was incorrectly rejected due to finding '
                 'multiple ester groups.\n'
                 '\n'
                 "Here's how we can improve:\n"
                 '\n'
                 '1. Make the ester pattern more inclusive to catch formyl '
                 'groups by modifying the SMARTS pattern\n'
                 '2. Make the alkyl ether pattern more flexible to catch '
                 'methyl groups\n'
                 '3. Modify the ester group check to allow for additional '
                 'ester groups in the acyl chain\n'
                 '4. Add stereochemistry check for '
                 'sn-glycero-3-phosphocholine\n'
                 '5. Make the glycerol backbone pattern more specific\n'
                 '\n'
                 "Here's the improved code:",
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 37,
    'num_false_positives': 51,
    'num_true_negatives': 142212,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.42045454545454547,
    'recall': 1.0,
    'f1': 0.5920000000000001,
    'accuracy': 0.9996416022487702,
    'negative_predictive_value': 1.0}