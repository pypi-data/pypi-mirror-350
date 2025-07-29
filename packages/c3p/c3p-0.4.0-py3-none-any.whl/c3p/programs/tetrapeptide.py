"""
Classifies: CHEBI:48030 tetrapeptide
"""
from rdkit import Chem

def is_tetrapeptide(smiles: str):
    """
    Determines if a molecule is a tetrapeptide based on its SMILES string.
    A tetrapeptide is any molecule that contains four amino-acid residues connected by peptide linkages.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a tetrapeptide, False otherwise
        str: Reason for classification
    """
    # Parse the SMILES string
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Define a peptide bond pattern: N-C(=O)
    peptide_bond_pattern = Chem.MolFromSmarts("[NX3][CX3](=O)")

    # Define amino acid residue patterns (generic backbone N-C-C)
    residue_pattern = Chem.MolFromSmarts("[NX3][CX4][CX3](=O)")

    # Find matches for peptide bonds and residues
    peptide_bonds = mol.GetSubstructMatches(peptide_bond_pattern)
    residues = mol.GetSubstructMatches(residue_pattern)

    num_peptide_bonds = len(peptide_bonds)
    num_residues = len(residues)

    # For a tetrapeptide, there must be 4 residues and 3 peptide bonds linking them
    if num_residues == 4 and num_peptide_bonds == 3:
        return True, "Contains four amino-acid residues connected by peptide linkages"
    
    # If checks fail
    return False, f"Found {num_residues} residues and {num_peptide_bonds} peptide bonds, requires 4 residues and 3 peptide bonds"

# Example usage in debug mode
smiles = "C[C@H](N)C(=O)N[C@@H](Cc1ccccc1)C(=O)N[C@@H](CC(O)=O)C(=O)N[C@@H](CC(O)=O)C(O)=O"
result = is_tetrapeptide(smiles)
print(result)


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:48030',
                          'name': 'tetrapeptide',
                          'definition': 'Any molecule that contains four '
                                        'amino-acid residues connected by '
                                        'peptide linkages.',
                          'parents': ['CHEBI:25676'],
                          'xrefs': ['KEGG:C01960'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 27,
                           'log_lines_of_code': 3.295836866004329,
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
                                                 2,
                                                 0,
                                                 1,
                                                 1,
                                                 0,
                                                 1,
                                                 1,
                                                 0,
                                                 1,
                                                 1,
                                                 1,
                                                 0,
                                                 1,
                                                 1,
                                                 0,
                                                 1,
                                                 1,
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 0],
                           'max_indent': 2,
                           'imports': ['from rdkit import Chem'],
                           'imports_count': 1,
                           'methods_called': [   'GetSubstructMatches',
                                                 'MolFromSmiles',
                                                 'MolFromSmarts'],
                           'methods_called_count': 3,
                           'smarts_strings': [   '[NX3][CX3](=O)',
                                                 '[NX3][CX4][CX3](=O)'],
                           'smarts_strings_count': 2,
                           'defs': ['is_tetrapeptide(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'True, "Contains four amino-acid '
                                          'residues connected by peptide '
                                          'linkages"',
                                          'False, f"Found {num_residues} '
                                          'residues and {num_peptide_bonds} '
                                          'peptide bonds, requires 4 residues '
                                          'and 3 peptide bonds"'],
                           'returns_count': 3,
                           'complexity': 2.4591673732008656},
    'message': '\n'
               'Attempt failed: F1 score of 0.001445086705202312 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: '
               'C[C@H](N)C(=O)N[C@@H](C)C(=O)N1CCC[C@H]1C(=O)N1CCC[C@H]1C(O)=O '
               'NAME: Ala-Ala-Pro-Pro REASON: CORRECT Contains four amino-acid '
               'residues connected by peptide linkages\n'
               ' * SMILES: '
               'CC(C)[C@H](NC(=O)[C@@H](N)CC(O)=O)C(=O)N1CCC[C@H]1C(=O)N1CCC[C@H]1C(O)=O '
               'NAME: Asp-Val-Pro-Pro REASON: CORRECT Contains four amino-acid '
               'residues connected by peptide linkages\n'
               ' * SMILES: '
               'CC(C)[C@H](NC(=O)[C@H](C)N)C(=O)N1CCC[C@H]1C(=O)N1CCC[C@H]1C(O)=O '
               'NAME: Ala-Val-Pro-Pro REASON: CORRECT Contains four amino-acid '
               'residues connected by peptide linkages\n'
               'False positives: SMILES: '
               'C1[C@H]2[C@@H]([C@H]([C@H](N2C(=O)C3=NC=CN=C3)C4=CC=CC(=O)N41)C(=O)NCC5=CC(=CC(=C5)F)F)CO '
               'NAME: LSM-9991 REASON: WRONGLY CLASSIFIED Contains four '
               'amino-acid residues connected by peptide linkages\n'
               ' * SMILES: C1CN(CCC1C(=O)N)C2CC(=O)N(C2=O)C3=CC(=CC=C3)F NAME: '
               '1-[1-(3-fluorophenyl)-2,5-dioxo-3-pyrrolidinyl]-4-piperidinecarboxamide '
               'REASON: WRONGLY CLASSIFIED Contains four amino-acid residues '
               'connected by peptide linkages\n'
               ' * SMILES: '
               'C[C@@H]1CN(C(=O)C2=CC=CC=C2C3=CC=CC=C3CO[C@@H]1CN(C)C(=O)N[C@H](C)C4=CC=CC=C4)[C@H](C)CO '
               'NAME: LSM-12452 REASON: WRONGLY CLASSIFIED Contains four '
               'amino-acid residues connected by peptide linkages\n'
               ' * SMILES: '
               'C[C@H]1CN(C(=O)C2=CC=CC=C2C3=CC=CC=C3CO[C@@H]1CN(C)C(=O)N[C@@H](C)C(C)C)[C@H](C)CO '
               'NAME: LSM-12655 REASON: WRONGLY CLASSIFIED Contains four '
               'amino-acid residues connected by peptide linkages\n'
               ' * SMILES: '
               'O=C1N2C(=NC3=C1C=CC=C3)[C@@H](NC([C@H]2C[C@@]4(O)C5=C(C=CC=C5)N6[C@H]4NC(C)(C)C6=O)=O)C(C)C '
               'NAME: Scequinadoline B REASON: WRONGLY CLASSIFIED Contains '
               'four amino-acid residues connected by peptide linkages\n'
               ' * SMILES: '
               'C[C@@H]1CN([C@@H](COC2=C(C=CC(=C2)NC(=O)C3=CC=CC=C3)C(=O)N(C[C@H]1OC)C)C)C(=O)C '
               'NAME: '
               'N-[(5S,6R,9R)-8-acetyl-5-methoxy-3,6,9-trimethyl-2-oxo-11-oxa-3,8-diazabicyclo[10.4.0]hexadeca-1(12),13,15-trien-14-yl]benzamide '
               'REASON: WRONGLY CLASSIFIED Contains four amino-acid residues '
               'connected by peptide linkages\n'
               ' * SMILES: '
               'C[C@H]1CN(C(=O)CC2=C(C=CC(=C2)NC(=O)NC3CCCCC3)O[C@H]1CN(C)S(=O)(=O)C4=CC=C(C=C4)Cl)[C@@H](C)CO '
               'NAME: '
               '1-[(2R,3S)-2-[[(4-chlorophenyl)sulfonyl-methylamino]methyl]-5-[(2S)-1-hydroxypropan-2-yl]-3-methyl-6-oxo-2,3,4,7-tetrahydro-1,5-benzoxazonin-9-yl]-3-cyclohexylurea '
               'REASON: WRONGLY CLASSIFIED Contains four amino-acid residues '
               'connected by peptide linkages\n'
               ' * SMILES: '
               'C[C@H]1CN(C(=O)C2=C(N=CC(=C2)C3=CCCC3)O[C@H]1CN(C)C(=O)NC4=CC(=CC=C4)F)[C@H](C)CO '
               'NAME: '
               '1-[[(2R,3S)-8-(1-cyclopentenyl)-5-[(2R)-1-hydroxypropan-2-yl]-3-methyl-6-oxo-3,4-dihydro-2H-pyrido[2,3-b][1,5]oxazocin-2-yl]methyl]-3-(3-fluorophenyl)-1-methylurea '
               'REASON: WRONGLY CLASSIFIED Contains four amino-acid residues '
               'connected by peptide linkages\n'
               ' * SMILES: '
               'O=C1N2[C@H](C3O[C@](C(N3[C@@H]1[C@@H](CC)C)=O)(NC(=O)[C@@H]4C=C5C6=C7C(NC=C7CC5N(C4)C)=CC=C6)C(C)C)CCC2 '
               "NAME: 5'-epi-beta-ergokryptine REASON: WRONGLY CLASSIFIED "
               'Contains four amino-acid residues connected by peptide '
               'linkages\n'
               ' * SMILES: '
               'C[C@H]1CN([C@@H](COC2=C(C=CC(=C2)NC(=O)COC)C(=O)N(C[C@@H]1OC)C)C)C(=O)CC3CC3 '
               'NAME: '
               'N-[(5R,6S,9R)-8-(2-cyclopropyl-1-oxoethyl)-5-methoxy-3,6,9-trimethyl-2-oxo-11-oxa-3,8-diazabicyclo[10.4.0]hexadeca-1(12),13,15-trien-14-yl]-2-methoxyacetamide '
               'REASON: WRONGLY CLASSIFIED Contains four amino-acid residues '
               'connected by peptide linkages\n'
               ' * SMILES: '
               'C[C@@H](CN([C@@H](C)CO)C(=O)NC1=CC=C(C=C1)C(F)(F)F)[C@H](CN(C)C(=O)C2CC2)OC '
               'NAME: '
               'N-[(2R,3S)-4-[[(2S)-1-hydroxypropan-2-yl]-[[4-(trifluoromethyl)phenyl]carbamoyl]amino]-2-methoxy-3-methylbutyl]-N-methylcyclopropanecarboxamide '
               'REASON: WRONGLY CLASSIFIED Contains four amino-acid residues '
               'connected by peptide linkages\n'
               ' * SMILES: '
               'C[C@H]1CN([C@H](COC2=C(C=CC(=C2)NC(=O)COC)C(=O)N(C[C@H]1OC)C)C)C(=O)CC3CC3 '
               'NAME: '
               'N-[(5S,6S,9S)-8-(2-cyclopropyl-1-oxoethyl)-5-methoxy-3,6,9-trimethyl-2-oxo-11-oxa-3,8-diazabicyclo[10.4.0]hexadeca-1(12),13,15-trien-14-yl]-2-methoxyacetamide '
               'REASON: WRONGLY CLASSIFIED Contains four amino-acid residues '
               'connected by peptide linkages\n'
               ' * SMILES: '
               'C[C@@H]1CN(C(=O)C2=C(C=CC(=C2)NC(=O)NC3=CC=C(C=C3)OC)O[C@@H]1CN(C)CC4=CC5=C(C=C4)OCO5)[C@@H](C)CO '
               'NAME: '
               '1-[(2S,3R)-2-[[1,3-benzodioxol-5-ylmethyl(methyl)amino]methyl]-5-[(2S)-1-hydroxypropan-2-yl]-3-methyl-6-oxo-3,4-dihydro-2H-1,5-benzoxazocin-8-yl]-3-(4-methoxyphenyl)urea '
               'REASON: WRONGLY CLASSIFIED Contains four amino-acid residues '
               'connected by peptide linkages\n'
               ' * SMILES: '
               'C[C@@H]1CN([C@@H](COC2=C(C=CC(=C2)NC(=O)C3CCC3)C(=O)N(C[C@@H]1OC)C)C)C(=O)CN(C)C '
               'NAME: '
               'N-[(5R,6R,9R)-8-[2-(dimethylamino)-1-oxoethyl]-5-methoxy-3,6,9-trimethyl-2-oxo-11-oxa-3,8-diazabicyclo[10.4.0]hexadeca-1(12),13,15-trien-14-yl]cyclobutanecarboxamide '
               'REASON: WRONGLY CLASSIFIED Contains four amino-acid residues '
               'connected by peptide linkages\n'
               ' * SMILES: '
               'C[C@@H]1CN(C(=O)CCCN2C=C(CO[C@H]1CN(C)C(=O)NC3=CC=C(C=C3)N4CCCCC4)N=N2)[C@@H](C)CO '
               'NAME: '
               '1-[[(8R,9R)-6-[(2S)-1-hydroxypropan-2-yl]-8-methyl-5-oxo-10-oxa-1,6,13,14-tetrazabicyclo[10.2.1]pentadeca-12(15),13-dien-9-yl]methyl]-1-methyl-3-[4-(1-piperidinyl)phenyl]urea '
               'REASON: WRONGLY CLASSIFIED Contains four amino-acid residues '
               'connected by peptide linkages\n'
               ' * SMILES: '
               'CCCNC(=O)N(C)C[C@@H]1[C@@H](CN(C(=O)C2=CC(=CN=C2O1)Br)[C@H](C)CO)C '
               'NAME: '
               '1-[[(2S,3R)-8-bromo-5-[(2R)-1-hydroxypropan-2-yl]-3-methyl-6-oxo-3,4-dihydro-2H-pyrido[2,3-b][1,5]oxazocin-2-yl]methyl]-1-methyl-3-propylurea '
               'REASON: WRONGLY CLASSIFIED Contains four amino-acid residues '
               'connected by peptide linkages\n'
               ' * SMILES: '
               'CN1[C@@H]2CC[C@H](O[C@H]2COC3=C(C1=O)C=C(C=C3)NC(=O)CC4=CC=CS4)CC(=O)N[C@H]5CCN(C5)CC6=CC=CC=C6 '
               'NAME: '
               '2-[(2S,4aR,12aR)-5-methyl-6-oxo-8-[(2-thiophen-2-ylacetyl)amino]-2,3,4,4a,12,12a-hexahydropyrano[2,3-c][1,5]benzoxazocin-2-yl]-N-[(3S)-1-benzylpyrrolidin-3-yl]acetamide '
               'REASON: WRONGLY CLASSIFIED Contains four amino-acid residues '
               'connected by peptide linkages\n'
               ' * SMILES: '
               'C[C@H]1CN([C@@H](COC2=C(C=CC(=C2)NC(=O)C)C(=O)N(C[C@H]1OC)C)C)C(=O)C3CCC3 '
               'NAME: '
               'N-[(5S,6S,9R)-8-[cyclobutyl(oxo)methyl]-5-methoxy-3,6,9-trimethyl-2-oxo-11-oxa-3,8-diazabicyclo[10.4.0]hexadeca-1(12),13,15-trien-14-yl]acetamide '
               'REASON: WRONGLY CLASSIFIED Contains four amino-acid residues '
               'connected by peptide linkages\n'
               ' * SMILES: '
               'C[C@H]1CN(C(=O)C2=C(C3=CC=CC=C3CO[C@H]1CN(C)C(=O)NC4CCCCC4)C5=CC=CC=C5N2C)[C@@H](C)CO '
               'NAME: LSM-10923 REASON: WRONGLY CLASSIFIED Contains four '
               'amino-acid residues connected by peptide linkages\n'
               ' * SMILES: '
               'C[C@@H]1CN([C@H](COC2=C(C=CC(=C2)NC(=O)C3=CC=CC=C3)C(=O)N(C[C@@H]1OC)C)C)C(=O)C '
               'NAME: '
               'N-[(5R,6R,9S)-8-acetyl-5-methoxy-3,6,9-trimethyl-2-oxo-11-oxa-3,8-diazabicyclo[10.4.0]hexadeca-1(12),13,15-trien-14-yl]benzamide '
               'REASON: WRONGLY CLASSIFIED Contains four amino-acid residues '
               'connected by peptide linkages\n'
               ' * SMILES: '
               'C[C@H]1CN(C(=O)C2=C(C=CC(=C2)NC(=O)NC3=CC=CC4=CC=CC=C43)O[C@@H]1CN(C)CC5=CC=NC=C5)[C@@H](C)CO '
               'NAME: '
               '1-[(2S,3S)-5-[(2S)-1-hydroxypropan-2-yl]-3-methyl-2-[[methyl(pyridin-4-ylmethyl)amino]methyl]-6-oxo-3,4-dihydro-2H-1,5-benzoxazocin-8-yl]-3-(1-naphthalenyl)urea '
               'REASON: WRONGLY CLASSIFIED Contains four amino-acid residues '
               'connected by peptide linkages\n'
               ' * SMILES: '
               'OC(C1CCCCC1)CNN2C(CCCCCCC(O)=O)C(=O)N(C2=O)CC3=CC=CC=C3 NAME: '
               'BW A868C REASON: WRONGLY CLASSIFIED Contains four amino-acid '
               'residues connected by peptide linkages\n'
               ' * SMILES: '
               'C[C@@H]1CN(C(=O)C2=C(C=CC(=C2)NS(=O)(=O)C)O[C@H]1CN(C)C(=O)NC3=CC=C(C=C3)C(F)(F)F)[C@H](C)CO '
               'NAME: '
               '1-[[(2R,3R)-5-[(2R)-1-hydroxypropan-2-yl]-8-(methanesulfonamido)-3-methyl-6-oxo-3,4-dihydro-2H-1,5-benzoxazocin-2-yl]methyl]-1-methyl-3-[4-(trifluoromethyl)phenyl]urea '
               'REASON: WRONGLY CLASSIFIED Contains four amino-acid residues '
               'connected by peptide linkages\n'
               ' * SMILES: '
               'C[C@@H]1CCCCO[C@H]([C@H](CN(C(=O)C2=C(O1)C=CC(=C2)NC(=O)NC3=CC4=C(C=C3)OCO4)[C@H](C)CO)C)CN(C)CC5CC5 '
               'NAME: '
               '1-(1,3-benzodioxol-5-yl)-3-[(3R,9R,10S)-9-[[cyclopropylmethyl(methyl)amino]methyl]-12-[(2R)-1-hydroxypropan-2-yl]-3,10-dimethyl-13-oxo-2,8-dioxa-12-azabicyclo[12.4.0]octadeca-1(14),15,17-trien-16-yl]urea '
               'REASON: WRONGLY CLASSIFIED Contains four amino-acid residues '
               'connected by peptide linkages\n'
               ' * SMILES: '
               'CCCC#CC1=CC2=C(N=C1)O[C@H]([C@@H](CN(C2=O)[C@H](C)CO)C)CN(C)C(=O)NC3=CC(=CC=C3)F '
               'NAME: '
               '3-(3-fluorophenyl)-1-[[(2R,3R)-5-[(2R)-1-hydroxypropan-2-yl]-3-methyl-6-oxo-8-pent-1-ynyl-3,4-dihydro-2H-pyrido[2,3-b][1,5]oxazocin-2-yl]methyl]-1-methylurea '
               'REASON: WRONGLY CLASSIFIED Contains four amino-acid residues '
               'connected by peptide linkages\n'
               'False negatives: SMILES: '
               'C[C@@H](O)[C@H](NC(=O)[C@H](C)N)C(=O)N[C@@H](C)C(=O)N1CCC[C@H]1C(O)=O '
               'NAME: Ala-Thr-Ala-Pro REASON: MISSED Does not have expected '
               'terminal amidic capping groups\n'
               ' * SMILES: '
               'NC(CCCCNC(=O)CCCCCNC(=O)c1ccc(o1)[N+]([O-])=O)C(=O)NCCCCC(N)C(=O)NCCCCC(N)C(=O)NC(CCCCNC(=O)CCCc1c[nH]c2ccccc12)C(N)=O '
               'NAME: '
               'N(6)-[N(6)-(N(6)-{6-[(5-nitro-2-furoyl)amino]hexanoyl}lysyl)lysyl]lysyl-N(6)-[4-(indol-3-yl)butanoyl]lysinamide '
               'REASON: MISSED Found 7 peptide bonds, requires exactly 3 to be '
               'a tetrapeptide\n'
               ' * SMILES: '
               'N[C@@H](CCC(O)=O)C(=O)N[C@@H](CCC(O)=O)C(=O)N[C@@H](CCC(N)=O)C(=O)N[C@@H](Cc1c[nH]c2ccccc12)C(O)=O '
               'NAME: Glu-Glu-Gln-Trp REASON: MISSED Found 4 peptide bonds, '
               'requires exactly 3 to be a tetrapeptide\n'
               ' * SMILES: '
               'C[C@H](N(C)C(=O)[C@H](CCCNC(N)=N)NC(=O)[C@H](CC1CCCCC1)NC(C)=O)C(=O)NC1CCc2cccc3CC(N(C1=O)c23)C(=O)NC(CO)CO '
               'NAME: Ac-Cha-Arg-MeAla-Haic-NHCH(CH2OH)2 REASON: MISSED Found '
               '6 peptide bonds, requires exactly 3 to be a tetrapeptide\n'
               ' * SMILES: '
               'C[C@@H](O)[C@H](NC(=O)[C@@H](N)CCC(O)=O)C(=O)N[C@@H]([C@@H](C)O)C(=O)N[C@@H](Cc1ccc(O)cc1)C(O)=O '
               'NAME: Glu-Thr-Thr-Tyr REASON: MISSED Does not have expected '
               'terminal amidic capping groups\n'
               ' * SMILES: '
               '[H][C@@]1(O[C@H](OC[C@H](NC(=O)CNC(C)=O)C(=O)NCC(=O)N[C@@H](OC(C)C)C(O)=O)[C@@H](O)[C@@H](O)[C@@H]1O)[C@H](O)CO '
               'NAME: AcGly-Ser(O-L-alpha-D-Hep)-Gly-Leu REASON: MISSED Found '
               '4 peptide bonds, requires exactly 3 to be a tetrapeptide\n'
               ' * SMILES: '
               'CC(C)C[C@@H](N)[C@H](O)C(=O)N[C@@H](C(C)C)C(=O)N[C@@H](C(C)C)C(=O)N[C@@H](CC(O)=O)C(O)=O '
               'NAME: amastatin REASON: MISSED Does not have expected terminal '
               'amidic capping groups\n'
               ' * SMILES: '
               'N([C@H](C(=O)N[C@H](C(=O)O)CC=1NC=NC1)CCC(=O)N)C([C@H](CS)NC([C@H](CCCNC(=N)N)N)=O)=O '
               'NAME: Asn-Cys-Gln-His REASON: MISSED Found 4 peptide bonds, '
               'requires exactly 3 to be a tetrapeptide\n'
               ' * SMILES: '
               'CC(C)C[C@H](NC(=O)[C@@H](N)CC(O)=O)C(=O)N[C@@H](Cc1ccccc1)C(=O)N[C@@H](C(C)C)C(O)=O '
               'NAME: Asp-Leu-Phe-Val REASON: MISSED Does not have expected '
               'terminal amidic capping groups\n'
               ' * SMILES: '
               'CC(=O)N[C@@H](CCC(N)=O)C(=O)N[C@H](Cc1ccccc1)C(=O)N[C@@H](Cc1c[nH]cn1)C(=O)N1CCC[C@@H]1C(N)=O '
               'NAME: Ac-Gln-D-Phe-His-D-Pro-NH2 REASON: MISSED Found 6 '
               'peptide bonds, requires exactly 3 to be a tetrapeptide\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'O1C(COC(=O)C)=CC=C1',
                                     'name': 'Furfuryl acetate',
                                     'reason': 'Found 0 residues and 0 peptide '
                                               'bonds, requires 4 residues and '
                                               '3 peptide bonds'},
                                 {   'smiles': 'O=C1N[C@@H](C(=O)N[C@H](C(=O)N[C@@H](C(=O)O)CC(=O)N[C@@H](CCCN=C(N)N)C(N[C@H]([C@@H](C(N[C@H](CCC(NC1=C)=O)C(=O)O)=O)C)/C=C/C(=C/[C@@H]([C@@H](OC)CC2=CC=CC=C2)C)/C)=O)CC(C)C)CO',
                                     'name': '[D-Ser1,D-Asp3,Dha7]MC-LR',
                                     'reason': 'Found 5 residues and 7 peptide '
                                               'bonds, requires 4 residues and '
                                               '3 peptide bonds'},
                                 {   'smiles': 'COC1=CC=C(C=C1)NC(=O)N[C@H]2CC[C@@H](O[C@H]2CO)CC(=O)NCC3=CC=CC=N3',
                                     'name': '2-[(2R,5S,6R)-6-(hydroxymethyl)-5-[[(4-methoxyanilino)-oxomethyl]amino]-2-oxanyl]-N-(2-pyridinylmethyl)acetamide',
                                     'reason': 'Found 0 residues and 3 peptide '
                                               'bonds, requires 4 residues and '
                                               '3 peptide bonds'},
                                 {   'smiles': 'O=[N+]([O-])C1=CC=C(/C=C(/C=C(/C=C/C=2OC(OC)=C(C)C(C2C)=O)\\C)\\C)C=C1',
                                     'name': 'Dehydrodeoxyaureothin',
                                     'reason': 'Found 0 residues and 0 peptide '
                                               'bonds, requires 4 residues and '
                                               '3 peptide bonds'},
                                 {   'smiles': 'C1CNCCNCCCN(CCNC1)CC2=CC=C(C=C2)CN3CCCNCCNCCCNCC3',
                                     'name': 'plerixafor',
                                     'reason': 'Found 0 residues and 0 peptide '
                                               'bonds, requires 4 residues and '
                                               '3 peptide bonds'},
                                 {   'smiles': 'O=C(C[C@@H]1O[C@H](CC[C@H]1O)C)C',
                                     'name': 'Decarestrictine L',
                                     'reason': 'Found 0 residues and 0 peptide '
                                               'bonds, requires 4 residues and '
                                               '3 peptide bonds'},
                                 {   'smiles': 'O=C1OC(=CC2=C1C[C@@H]3[C@@]4([C@H](C(C)(C)O[C@H]4CC(=O)OC)[C@@H](C[C@]3(O2)C)OC(=O)C)C)C',
                                     'name': 'Asperversin A',
                                     'reason': 'Found 0 residues and 0 peptide '
                                               'bonds, requires 4 residues and '
                                               '3 peptide bonds'},
                                 {   'smiles': 'O=C1OC(CC=2C1=C(O)C3=C(O)C(C4=C(O)C5=C(O)C=6C(=O)OC(CC(=O)C)CC6C=C5C=C4OC)=C(OC)C=C3C2)CC(=O)C',
                                     'name': 'SC-30532',
                                     'reason': 'Found 0 residues and 0 peptide '
                                               'bonds, requires 4 residues and '
                                               '3 peptide bonds'},
                                 {   'smiles': 'C([C@H](NC(CC[C@H](N)C(=O)O)=O)C(O)=O)S[C@H](\\C=C\\C=C\\C=C/C/C=C\\CCCCC)[C@@H](O)CCCC(=O)O',
                                     'name': 'leukotriene F4',
                                     'reason': 'Found 2 residues and 1 peptide '
                                               'bonds, requires 4 residues and '
                                               '3 peptide bonds'},
                                 {   'smiles': 'C1(=C(C=C2C(=C1)[C@@]34[C@@]([NH+](C2)CC3)(CC(CC4)=O)[H])O)OC',
                                     'name': '(4aS,10bR)-oxomaritidine(1+)',
                                     'reason': 'Found 0 residues and 0 peptide '
                                               'bonds, requires 4 residues and '
                                               '3 peptide bonds'}],
    'sample_false_negatives': [   {   'smiles': 'NC(CCCCNC(=O)CCCCCNC(=O)c1ccc(o1)[N+]([O-])=O)C(=O)NCCCCC(N)C(=O)NCCCCC(N)C(=O)NC(CCCCNC(=O)CCCc1c[nH]c2ccccc12)C(N)=O',
                                      'name': 'N(6)-[N(6)-(N(6)-{6-[(5-nitro-2-furoyl)amino]hexanoyl}lysyl)lysyl]lysyl-N(6)-[4-(indol-3-yl)butanoyl]lysinamide',
                                      'reason': 'Found 4 residues and 7 '
                                                'peptide bonds, requires 4 '
                                                'residues and 3 peptide bonds'},
                                  {   'smiles': 'N[C@@H](CCC(O)=O)C(=O)N[C@@H](CCC(O)=O)C(=O)N[C@@H](CCC(N)=O)C(=O)N[C@@H](Cc1c[nH]c2ccccc12)C(O)=O',
                                      'name': 'Glu-Glu-Gln-Trp',
                                      'reason': 'Found 4 residues and 4 '
                                                'peptide bonds, requires 4 '
                                                'residues and 3 peptide bonds'},
                                  {   'smiles': 'C[C@H](N(C)C(=O)[C@H](CCCNC(N)=N)NC(=O)[C@H](CC1CCCCC1)NC(C)=O)C(=O)NC1CCc2cccc3CC(N(C1=O)c23)C(=O)NC(CO)CO',
                                      'name': 'Ac-Cha-Arg-MeAla-Haic-NHCH(CH2OH)2',
                                      'reason': 'Found 5 residues and 6 '
                                                'peptide bonds, requires 4 '
                                                'residues and 3 peptide bonds'},
                                  {   'smiles': '[H][C@@]1(O[C@H](OC[C@H](NC(=O)CNC(C)=O)C(=O)NCC(=O)N[C@@H](OC(C)C)C(O)=O)[C@@H](O)[C@@H](O)[C@@H]1O)[C@H](O)CO',
                                      'name': 'AcGly-Ser(O-L-alpha-D-Hep)-Gly-Leu',
                                      'reason': 'Found 4 residues and 4 '
                                                'peptide bonds, requires 4 '
                                                'residues and 3 peptide bonds'},
                                  {   'smiles': 'CC(C)C[C@@H](N)[C@H](O)C(=O)N[C@@H](C(C)C)C(=O)N[C@@H](C(C)C)C(=O)N[C@@H](CC(O)=O)C(O)=O',
                                      'name': 'amastatin',
                                      'reason': 'Found 3 residues and 3 '
                                                'peptide bonds, requires 4 '
                                                'residues and 3 peptide bonds'},
                                  {   'smiles': 'N([C@H](C(=O)N[C@H](C(=O)O)CC=1NC=NC1)CCC(=O)N)C([C@H](CS)NC([C@H](CCCNC(=N)N)N)=O)=O',
                                      'name': 'Asn-Cys-Gln-His',
                                      'reason': 'Found 4 residues and 4 '
                                                'peptide bonds, requires 4 '
                                                'residues and 3 peptide bonds'},
                                  {   'smiles': 'CC(=O)N[C@@H](CCC(N)=O)C(=O)N[C@H](Cc1ccccc1)C(=O)N[C@@H](Cc1c[nH]cn1)C(=O)N1CCC[C@@H]1C(N)=O',
                                      'name': 'Ac-Gln-D-Phe-His-D-Pro-NH2',
                                      'reason': 'Found 4 residues and 6 '
                                                'peptide bonds, requires 4 '
                                                'residues and 3 peptide bonds'},
                                  {   'smiles': 'C(=O)([C@@H](N)CC(=O)N)N[C@H](C(=O)N[C@@H](CCC(=O)N)C(N1[C@H](C(=O)O)CCC1)=O)CCSC',
                                      'name': 'Asn-Met-Gln-Pro',
                                      'reason': 'Found 4 residues and 5 '
                                                'peptide bonds, requires 4 '
                                                'residues and 3 peptide bonds'},
                                  {   'smiles': 'C[C@H](N)C(=O)N[C@H](CCC(=O)N[C@H](CCC[C@H](N)C(O)=O)C(=O)N[C@H](C)C(O)=O)C(O)=O',
                                      'name': 'L-Ala-gamma-D-Glu-meso-Dap-D-Ala',
                                      'reason': 'Found 5 residues and 3 '
                                                'peptide bonds, requires 4 '
                                                'residues and 3 peptide bonds'},
                                  {   'smiles': 'CSCC[C@H](NC(=O)[C@@H]1Cc2ccccc2CN1C(=O)[C@@H](NC(=O)[C@H](CC1CCCCC1)NC(C)=O)C1CCN(CC1)C(N)=N)C(N)=O',
                                      'name': 'Ac-Cha-Gpg-Tic-Met-NH2',
                                      'reason': 'Found 4 residues and 5 '
                                                'peptide bonds, requires 4 '
                                                'residues and 3 peptide '
                                                'bonds'}],
    'attempt': 2,
    'reasoning': "In analyzing the previous implementation's outcomes, it "
                 'appears that several challenges contributed to its failure '
                 'to correctly classify tetrapeptides:\n'
                 '\n'
                 '1. **Inaccurate Peptide Bond Counting:** The previous code '
                 'uses a pattern to detect peptide bonds (\\[C](=O)-\\[N]), '
                 'which captures simple amide linkages. However, various '
                 'configurations, such as cyclic peptides, may cause incorrect '
                 'counts.\n'
                 '\n'
                 '2. **Capping Group Verification:** The validation for '
                 'capping groups relies on atoms with three bonds including '
                 'nitrogen (degree 3), which may not be accurate for all '
                 'tetrapeptides. Some tetrapeptides may be cyclic or have '
                 'different terminal modifications.\n'
                 '\n'
                 '3. **Peptide Length and Configuration:** The code does not '
                 'account for the exact linear arrangement of four amino acids '
                 'connected specifically by peptide bonds, leading to '
                 'misclassifications when other similar structures are '
                 'present.\n'
                 '\n'
                 '4. **Cyclic Structure Handling:** Tetrapeptides with cyclic '
                 'structures or specific cyclizations could be ignored or '
                 'falsely classified.\n'
                 '\n'
                 '5. **More Rigorous Bond and Group Matching:** The approach '
                 'lacks robust criteria for identifying specific linear or '
                 'cyclic peptide chains without error due to incomplete '
                 'structural representation in SMILES.\n'
                 '\n'
                 '### Improvements:\n'
                 '- Utilize SMARTS that accurately determine amino acid '
                 'residues.\n'
                 '- Increase rigor in identifying exact linear or '
                 'appropriately cyclic peptide structure, verifying '
                 'sequentialness.\n'
                 '- Enhance terminal group detection to accommodate common '
                 'modifications in natural/conventional synthesis.\n'
                 '\n'
                 "Here's a refined version:",
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 52,
    'num_false_positives': 77,
    'num_true_negatives': 142121,
    'num_false_negatives': 50,
    'num_negatives': None,
    'precision': 0.40310077519379844,
    'recall': 0.5098039215686274,
    'f1': 0.4502164502164502,
    'accuracy': 0.9991075193253689,
    'negative_predictive_value': 0.9996483108369498}