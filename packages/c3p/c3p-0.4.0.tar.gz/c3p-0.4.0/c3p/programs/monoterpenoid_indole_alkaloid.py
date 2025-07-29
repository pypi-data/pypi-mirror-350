"""
Classifies: CHEBI:65323 monoterpenoid indole alkaloid
"""
from rdkit import Chem
from rdkit.Chem import Descriptors

def is_monoterpenoid_indole_alkaloid(smiles: str):
    """
    Determines if a molecule is a monoterpenoid indole alkaloid (MIA) based on its SMILES string.
    
    Args:
        smiles (str): SMILES string of the molecule
    
    Returns:
        bool: True if the molecule is an MIA, False otherwise
        str: Reason for classification
    """
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Look for indole substructure: benzene ring fused to a pyrrole (indole)
    indole_pattern = Chem.MolFromSmarts('c1c[cH]cc2c1[nH]cc2')
    if not mol.HasSubstructMatch(indole_pattern):
        return False, "Indole moiety not found"

    # Look for characteristic terpenoid features (such as cyclized isoprene groups)
    terpene_pattern = Chem.MolFromSmarts('C(C(=O)O)C(C)C')  # Pseudo pattern for terpene linkage
    if not mol.HasSubstructMatch(terpene_pattern):
        return False, "Terpene-like linkage not found"

    # Examine complexity based on molecular weight and presence of oxygen
    is_large = Descriptors.MolWt(mol) > 350  # MIAs are generally large
    has_ester_oxygen = any(atom.GetAtomicNum() == 8 and atom.GetDegree() == 2 for atom in mol.GetAtoms())
    
    # Chiral centers indicating complex natural products
    chiral_centers = Chem.FindMolChiralCenters(mol, includeUnassigned=True)
    
    if not (is_large and has_ester_oxygen and len(chiral_centers) >= 3):
        return False, "Does not meet expected structure complexity for MIAs"

    return True, "Contains indole moiety with complex MIA-specific features and ester linkage"

# Example usage:
smiles = "C/C=C\1/CN2CC[C@]34C5=CC(C=6C=C7C(=CC6OC)[C@]89CCN%10C/C(=C\C)/[C@](CCC8%10N7C)([C@]9(C(=O)OC)[H])[H])=C(C=C5N(C)[C@]4(C2C[C@@]1([C@@]3(C(=O)OC)[H])[H])[H])OC"
print(is_monoterpenoid_indole_alkaloid(smiles))


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:65323',
                          'name': 'monoterpenoid indole alkaloid',
                          'definition': 'A terpenoid indole alkaloid which is '
                                        'biosynthesised from L-tryptophan and '
                                        'diisoprenoid (usually secolaganin) '
                                        'building blocks.',
                          'parents': ['CHEBI:65321'],
                          'xrefs': [   'PMID:18280746',
                                       'PMID:20717879',
                                       'PMID:21425787',
                                       'PMID:22679912'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 28,
                           'log_lines_of_code': 3.332204510175204,
                           'indent_by_line': [   1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
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
                                                 1,
                                                 1,
                                                 2,
                                                 0,
                                                 1,
                                                 0],
                           'max_indent': 2,
                           'imports': [   'from rdkit import Chem',
                                          'from rdkit.Chem import Descriptors'],
                           'imports_count': 2,
                           'methods_called': [   'GetDegree',
                                                 'FindMolChiralCenters',
                                                 'GetAtoms',
                                                 'MolWt',
                                                 'HasSubstructMatch',
                                                 'MolFromSmiles',
                                                 'MolFromSmarts',
                                                 'GetAtomicNum'],
                           'methods_called_count': 8,
                           'smarts_strings': [   'C(C(=O)O)C(C)C',
                                                 'c1c[cH]cc2c1[nH]cc2'],
                           'smarts_strings_count': 2,
                           'defs': [   'is_monoterpenoid_indole_alkaloid(smiles: '
                                       'str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "Indole moiety not found"',
                                          'False, "Terpene-like linkage not '
                                          'found"',
                                          'False, "Does not meet expected '
                                          'structure complexity for MIAs"',
                                          'True, "Contains indole moiety with '
                                          'complex MIA-specific features and '
                                          'ester linkage"'],
                           'returns_count': 5,
                           'complexity': 3.8664409020350403},
    'message': '\n'
               'Attempt failed: F1 score of 0.04901960784313725 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: '
               'C=C[C@]1(CN2CCC=3C=4C=CC(=C([C@]5(CCCN5C)[H])C4NC3[C@@]2(C[C@@]1(C[C@]6(C7=C(CCN6C)C8=CC=CC=C8N7)[H])[H])[H])O)[H] '
               'NAME: Strychnopentamine REASON: CORRECT Contains indole moiety '
               'and exhibits complexity indicative of monoterpenoid indole '
               'alkaloids\n'
               ' * SMILES: '
               'C=C[C@]1(CN2CCC=3C=4C=CC(=CC4NC3[C@@]2(C[C@@]1(C[C@@]5(C6=C(CCN5C)C7=CC=CC=C7N6)[H])[H])[H])O)[H] '
               'NAME: 11-hydroxyusambarine REASON: CORRECT Contains indole '
               'moiety and exhibits complexity indicative of monoterpenoid '
               'indole alkaloids\n'
               ' * SMILES: '
               'C=C[C@]1(CN2CC[C@]3(C=4C=CC(=CC4N=C3O)O)[C@@]2(C[C@@]1(C[C@]5(C6=C(CCN5C)C7=CC=CC=C7N6)[H])[H])[H])[H] '
               'NAME: Strychnofoline REASON: CORRECT Contains indole moiety '
               'and exhibits complexity indicative of monoterpenoid indole '
               'alkaloids\n'
               ' * SMILES: '
               '[H][C@]12CN3CCC4=C(NC5=C4C=CC=C5)[C@]3([H])C[C@]1([H])C(=CO[C@H]2C)C(=O)OC '
               'NAME: ajmalicine REASON: CORRECT Contains indole moiety and '
               'exhibits complexity indicative of monoterpenoid indole '
               'alkaloids\n'
               ' * SMILES: '
               'CO[C@H]1[C@@H](C[C@@H]2CN3CCC4=C([C@H]3C[C@@H]2[C@@H]1C(=O)OC)NC5=C4C=CC(=C5)OC)OC(=O)C=CC6=CC(=C(C(=C6)OC)OC)OC '
               'NAME: '
               '(1R,15S,17R,18R,19S,20S)-6,18-dimethoxy-17-[1-oxo-3-(3,4,5-trimethoxyphenyl)prop-2-enoxy]-1,3,11,12,14,15,16,17,18,19,20,21-dodecahydroyohimban-19-carboxylic '
               'acid methyl ester REASON: CORRECT Contains indole moiety and '
               'exhibits complexity indicative of monoterpenoid indole '
               'alkaloids\n'
               ' * SMILES: '
               'C=C[C@H]1CN2CCC3(C=4C=CC(=C([C@H]5CCCN5C)C4N=C3O)O)[C@@]2(C[C@@]1(C[C@]6(C7=C(CCN6C)C8=CC=CC=C8N7)[H])[H])[H] '
               'NAME: Strychnophylline REASON: CORRECT Contains indole moiety '
               'and exhibits complexity indicative of monoterpenoid indole '
               'alkaloids\n'
               ' * SMILES: '
               'COC(=O)C1[C@H](CC[C@@H]2[C@@H]1C[C@H]3C4=C(CCN3C2)C5=CC=CC=C5N4)O '
               'NAME: '
               '(1S,15R,18S,20S)-18-hydroxy-1,3,11,12,14,15,16,17,18,19,20,21-dodecahydroyohimban-19-carboxylic '
               'acid methyl ester REASON: CORRECT Contains indole moiety and '
               'exhibits complexity indicative of monoterpenoid indole '
               'alkaloids\n'
               ' * SMILES: '
               'C[C@@H]1[C@@H](C=O)[C@@]2(C[C@]3(C4=C(CCN3C(C2=CO1)=O)C5=CC=CC=C5N4)[H])[H] '
               'NAME: Naucleidinal REASON: CORRECT Contains indole moiety and '
               'exhibits complexity indicative of monoterpenoid indole '
               'alkaloids\n'
               ' * SMILES: '
               'C=C[C@]1(CN2CCC=3C4=CC=CC=C4NC3[C@@]2(C[C@@]1(/C(=C(\\OC)/[H])/C(=O)OC)[H])[H])[H] '
               'NAME: Corynantheine REASON: CORRECT Contains indole moiety and '
               'exhibits complexity indicative of monoterpenoid indole '
               'alkaloids\n'
               ' * SMILES: '
               'CC[C@@]1(CN2CC[C@@]34C5=CC=CC=C5N6[C@]4([C@@](CO[C@]6([C@@]([C@]/7(CC=8C9=C(C=C[N+]8C\\C7=C\\C)C=%10C=CC=CC%10N9)[H])(C(=O)OC)[H])[H])([C@]1(C[C@@]32[H])[H])[H])[H])[H] '
               "NAME: 3',4',5',6'-tetradehydrogeissospermine REASON: CORRECT "
               'Contains indole moiety and exhibits complexity indicative of '
               'monoterpenoid indole alkaloids\n'
               ' * SMILES: '
               '[H][C@@]12N3CC[C@@]11c4cc(c(OC)cc4N(C)[C@@]1([H])[C@](O)([C@H](O)[C@]2(CC)C=CC3)C(N)=O)[C@]1(C[C@@H]2C[N@](CCc3c1[nH]c1ccccc31)C[C@](O)(CC)C2)C(=O)OC '
               'NAME: vindesine REASON: CORRECT Contains indole moiety and '
               'exhibits complexity indicative of monoterpenoid indole '
               'alkaloids\n'
               ' * SMILES: '
               'CCC1=C[C@@H]2CN(C1)Cc1c([nH]c3ccccc13)[C@@](C2)(C(=O)OC)c1cc2c(cc1OC)N(C)[C@@H]1[C@]22CCN3CC=C[C@](CC)([C@@H]23)[C@@H](OC(C)=O)[C@]1(O)C(=O)OC '
               'NAME: vinorelbine REASON: CORRECT Contains indole moiety and '
               'exhibits complexity indicative of monoterpenoid indole '
               'alkaloids\n'
               ' * SMILES: '
               'C=C[C@@](CO)([C@]1(CC[N@@+]2(C)CCC=3C4=CC=CC=C4NC3[C@@]2(C1)[H])[H])[H] '
               'NAME: N4-methylantirhine REASON: CORRECT Contains indole '
               'moiety and exhibits complexity indicative of monoterpenoid '
               'indole alkaloids\n'
               ' * SMILES: '
               '[H][C@@]12CC[C@H](O)[C@]([H])(C(O)=O)[C@@]1([H])C[C@]1([H])N(CCc3c1[nH]c1ccccc31)C2 '
               'NAME: yohimbic acid REASON: CORRECT Contains indole moiety and '
               'exhibits complexity indicative of monoterpenoid indole '
               'alkaloids\n'
               ' * SMILES: '
               'CO[C@H]1[C@@H](C[C@@H]2CN3CCc4c([nH]c5ccccc45)[C@H]3C[C@@H]2[C@@H]1C(=O)OC)OC(=O)c1cc(OC)c(OC)c(OC)c1 '
               'NAME: deserpidine REASON: CORRECT Contains indole moiety and '
               'exhibits complexity indicative of monoterpenoid indole '
               'alkaloids\n'
               ' * SMILES: '
               'C/C=C\\1/C[N+]=2C=CC=3C=4C=CC=CC4NC3C2C[C@@]1(C5=CN6C7=CC=CC=C7[C@]89CCN%10C\\C(=C\\C)\\[C@](C[C@@]8%10[H])([C@@]([C@@H]5O)([C@@]96[H])[H])[H])[H] '
               "NAME: 3',4',5',6'-tetradehydrolongicaudatine Y REASON: CORRECT "
               'Contains indole moiety and exhibits complexity indicative of '
               'monoterpenoid indole alkaloids\n'
               ' * SMILES: '
               'C[C@H]1[C@@H]2CN3CCC4=C(C3C[C@@H]2C(=CO1)C(=O)OC)NC5=CC=CC=C45 '
               'NAME: LSM-6418 REASON: CORRECT Contains indole moiety and '
               'exhibits complexity indicative of monoterpenoid indole '
               'alkaloids\n'
               ' * SMILES: '
               'CO[C@H]1[C@@H](C[C@@H]2CN3CCC4=C([C@@H]3C[C@H]2[C@@H]1C(=O)OC)NC5=C4C=CC(=C5)OC)OC(=O)C6=CC(=C(C(=C6)OC)OC)OC '
               'NAME: '
               '(1S,15S,17R,18R,19S,20R)-6,18-dimethoxy-17-[oxo-(3,4,5-trimethoxyphenyl)methoxy]-1,3,11,12,14,15,16,17,18,19,20,21-dodecahydroyohimban-19-carboxylic '
               'acid methyl ester REASON: CORRECT Contains indole moiety and '
               'exhibits complexity indicative of monoterpenoid indole '
               'alkaloids\n'
               ' * SMILES: '
               'CC[C@@]1(C[C@@H]2C[C@@](C3=C(CCN(C2)C1)C4=CC=CC=C4N3)(C5=C(C=C6C(=C5)[C@]78CCN9[C@H]7[C@](C=CC9)([C@H]([C@@]([C@@H]8N6C=O)(C(=O)OC)O)OC(=O)C)CC)OC)C(=O)OC)O '
               'NAME: LSM-15607 REASON: CORRECT Contains indole moiety and '
               'exhibits complexity indicative of monoterpenoid indole '
               'alkaloids\n'
               ' * SMILES: '
               '[H][C@]12N(CCC3=C1NC4=C3C=CC=C4)C[C@]5([C@](C2)([C@@H](C(OC)=O)[C@@H](O)CC5)[H])[H] '
               'NAME: pseudoyohimbine REASON: CORRECT Contains indole moiety '
               'and exhibits complexity indicative of monoterpenoid indole '
               'alkaloids\n'
               ' * SMILES: '
               'CC[C@@]1(C[C@@]2(C[C@@]3(C4=C(CCN(C2)[C@]13[H])C5=CC(=C(C=C5N4)OC)[C@]6(C[C@]7([C@H](CC)CN(C)[C@@](CC=8C9=CC=CC=C9NC86)(C7C(=O)OC)[H])[H])O)C(=O)OC)[H])[H] '
               'NAME: 3-R,S-hydroxytabernaelegantine A REASON: CORRECT '
               'Contains indole moiety and exhibits complexity indicative of '
               'monoterpenoid indole alkaloids\n'
               ' * SMILES: '
               '[H][C@]12C[C@@H](O)[C@H](OC)[C@@H](C(O)=O)[C@@]1([H])C[C@@]1([H])N(CCc3c1[nH]c1cc(OC)ccc31)C2 '
               'NAME: reserpic acid REASON: CORRECT Contains indole moiety and '
               'exhibits complexity indicative of monoterpenoid indole '
               'alkaloids\n'
               ' * SMILES: '
               '[H][C@]12CC[C@H](O)[C@@H](C(=O)OC)[C@@]1([H])C[C@]1([H])N(CCc3c1[nH]c1ccccc31)C2 '
               'NAME: rauwolscine REASON: CORRECT Contains indole moiety and '
               'exhibits complexity indicative of monoterpenoid indole '
               'alkaloids\n'
               ' * SMILES: '
               '[H][C@@]12C[C@@]3([H])C(=CN1CCC1=C2NC2=C1C=CC=C2)[C@H](C)OC=C3C(=O)OC '
               'NAME: cathenamine REASON: CORRECT Contains indole moiety and '
               'exhibits complexity indicative of monoterpenoid indole '
               'alkaloids\n'
               ' * SMILES: '
               'COC=1C=CC=2C=3CCN4C[C@@]5(CC[C@@]([C@@]([C@]5(C[C@]4(C3NC2C1)[H])[H])(C(=O)OC)[H])(O)[H])[H] '
               'NAME: 11-methoxyyohimbine REASON: CORRECT Contains indole '
               'moiety and exhibits complexity indicative of monoterpenoid '
               'indole alkaloids\n'
               'False positives: SMILES: '
               'ClC1=C2C(=CC3=C1NC=4C=CC=CC34)[C@@]5([C@H]([C@](C(=O)O)([C@@H](O)CC5)C)CC2)C '
               'NAME: Chloroxiamycin REASON: WRONGLY CLASSIFIED Contains '
               'indole moiety and exhibits complexity indicative of '
               'monoterpenoid indole alkaloids\n'
               ' * SMILES: '
               'N[C@@H](Cc1c[nH]c2ccccc12)C(=O)N[C@@H](CC(O)=O)C(=O)N[C@@H](CO)C(O)=O '
               'NAME: Trp-Asp-Ser REASON: WRONGLY CLASSIFIED Contains indole '
               'moiety and exhibits complexity indicative of monoterpenoid '
               'indole alkaloids\n'
               ' * SMILES: '
               'O=C1C=C2[C@@]3(CC[C@]4([C@H]2CCC5=C4C=C6NC=7C=CC=CC7C6=C5)C)O[C@@H]1C(O3)(C)C '
               'NAME: Shearilicine REASON: WRONGLY CLASSIFIED Contains indole '
               'moiety and exhibits complexity indicative of monoterpenoid '
               'indole alkaloids\n'
               ' * SMILES: '
               'C[C@H](CCCC([O-])=O)O[C@@H]1O[C@@H](C)[C@@H](C[C@H]1O)OC(=O)C1=CNC2=C1C=CC=C2 '
               'NAME: icas#12(1-) REASON: WRONGLY CLASSIFIED Contains indole '
               'moiety and exhibits complexity indicative of monoterpenoid '
               'indole alkaloids\n'
               ' * SMILES: '
               'S(CC[C@H](NC(=O)[C@@H](N)C(C)C)C(=O)N[C@@H](CC=1C=2C(NC1)=CC=CC2)C(O)=O)C '
               'NAME: Val-Met-Trp REASON: WRONGLY CLASSIFIED Contains indole '
               'moiety and exhibits complexity indicative of monoterpenoid '
               'indole alkaloids\n'
               ' * SMILES: '
               'O=C(N[C@@H](CC=1C=2C(NC1)=CC=CC2)C(=O)N[C@@H](C)C(O)=O)[C@@H](N)CC=3C=4C(NC3)=CC=CC4 '
               'NAME: Trp-Trp-Ala REASON: WRONGLY CLASSIFIED Contains indole '
               'moiety and exhibits complexity indicative of monoterpenoid '
               'indole alkaloids\n'
               ' * SMILES: '
               'O1[C@]23[C@]4([C@@]([C@@]5([C@@](CC4)(CC6=C5NC=7C6=CC=CC7)[H])C)(CC[C@@]3(O[C@@](C[C@@]12[H])(C(O)(C)C)[H])[H])C)[H] '
               'NAME: Terpendole B REASON: WRONGLY CLASSIFIED Contains indole '
               'moiety and exhibits complexity indicative of monoterpenoid '
               'indole alkaloids\n'
               ' * SMILES: '
               'C(N[C@H](C(N[C@H](C(N[C@H](C(N[C@H](C(=O)N[C@H](C(N[C@H](C(N[C@H](C(N[C@H](C(=O)N1[C@H](C(=O)O)CCC1)CC(C)C)=O)CCCCN)=O)CC=2C=CC=CC2)=O)CC3=CNC4=C3C=CC=C4)CC(=O)O)=O)CCCNC(=N)N)=O)CC5=CNC6=C5C=CC=C6)=O)C(C)C)([C@H](CCC(=O)N)NC(=O)[C@H]7N(CCC7)C([C@@H](N)C(CC)C)=O)=O '
               'NAME: IPQVWRDWFKLP REASON: WRONGLY CLASSIFIED Contains indole '
               'moiety and exhibits complexity indicative of monoterpenoid '
               'indole alkaloids\n'
               ' * SMILES: '
               'O=C1[C@@H]([C@@]2([C@H]([C@]3([C@@H]([C@]([C@H](C)CC3)(CC=4C5=C(C=CC=C5)NC4)C)CC2)C)CC1)C)C '
               'NAME: Radarin C REASON: WRONGLY CLASSIFIED Contains indole '
               'moiety and exhibits complexity indicative of monoterpenoid '
               'indole alkaloids\n'
               ' * SMILES: '
               'O1[C@@]2(C([C@]3([C@@]([C@@]4([C@@](CC3)(CC5=C4NC=6C5=CC=CC6)[H])C)(CC2)C)[H])=CC(=O)[C@]1(C(O)(C)C)[H])[H] '
               'NAME: Dehydroxypaxilline REASON: WRONGLY CLASSIFIED Contains '
               'indole moiety and exhibits complexity indicative of '
               'monoterpenoid indole alkaloids\n'
               ' * SMILES: '
               'CCCCCCCCCC(=O)N[C@@H](Cc1c[nH]c2ccccc12)C(=O)N[C@@H](CC(N)=O)C(=O)N[C@@H](CC(O)=O)C(=O)N[C@H]1[C@@H](C)OC(=O)[C@H](CC(=O)c2ccccc2N)NC(=O)[C@@H](NC(=O)[C@@H](CO)NC(=O)CNC(=O)[C@H](CC(O)=O)NC(=O)[C@@H](C)NC(=O)[C@H](CC(O)=O)NC(=O)[C@H](CCCN)NC(=O)CNC1=O)[C@H](C)CC(O)=O '
               'NAME: daptomycin REASON: WRONGLY CLASSIFIED Contains indole '
               'moiety and exhibits complexity indicative of monoterpenoid '
               'indole alkaloids\n'
               ' * SMILES: '
               'O=C(N[C@@H]([C@H](O)C)C(O)=O)[C@@H](NC(=O)CN)CC=1C=2C(NC1)=CC=CC2 '
               'NAME: Gly-Trp-Thr REASON: WRONGLY CLASSIFIED Contains indole '
               'moiety and exhibits complexity indicative of monoterpenoid '
               'indole alkaloids\n'
               ' * SMILES: '
               'O=C1[C@H](N[C@H](C(=O)O)CC2=CC=C(O)C=C2)CCC(O)=NCCCC[C@@H]3N=C(O)[C@@H](N=C([C@H]([C@H](OC(C[C@H]4C(=N[C@H](C(=N[C@H]1CCC(=O)OC[C@H](N=C(O)[C@H]5N(C(=O)[C@@H](N=C3O)CC6=CC=C(O)C=C6)CCC5)C(O)=N4)O)CC=7C8=C(C=CC=C8)NC7)O)=O)C)N=C(O)[C@@H](N=C(O)[C@@H](N=C(O)C)CC9=CC=C(O)C=C9)CO)O)CC(C)C '
               'NAME: Microviridin LH1667 REASON: WRONGLY CLASSIFIED Contains '
               'indole moiety and exhibits complexity indicative of '
               'monoterpenoid indole alkaloids\n'
               ' * SMILES: '
               'O=C(N1[C@@H](CCC1)C(O)=O)[C@H]2N(CCC2)C(=O)[C@@H](N)CC=3C=4C(NC3)=CC=CC4 '
               'NAME: Trp-Pro-Pro REASON: WRONGLY CLASSIFIED Contains indole '
               'moiety and exhibits complexity indicative of monoterpenoid '
               'indole alkaloids\n'
               ' * SMILES: '
               'C1=CC=CC=2NC=C(C12)CC(O[C@H]3[C@@H]([C@H]([C@@H]([C@H](O3)C(O)=O)O)O)O)=O '
               'NAME: Indole-3-acetic-acid-O-glucuronide REASON: WRONGLY '
               'CLASSIFIED Contains indole moiety and exhibits complexity '
               'indicative of monoterpenoid indole alkaloids\n'
               ' * SMILES: '
               'CC(C)C[C@H](NP(O)(=O)O[C@@H]1O[C@@H](C)[C@H](O)[C@@H](O)[C@H]1O)C(=O)N[C@@H](Cc1c[nH]c2ccccc12)C(O)=O '
               'NAME: phosphoramidon REASON: WRONGLY CLASSIFIED Contains '
               'indole moiety and exhibits complexity indicative of '
               'monoterpenoid indole alkaloids\n'
               ' * SMILES: '
               'N(C([C@@H](N[H])CC(O)=O)=O)[C@@H](CC1=CC=C(OS(=O)(=O)O)C=C1)C(N[C@@H](CCSC)C(NCC(N[C@@H](CC2=CNC3=C2C=CC=C3)C(N[C@@H](CCSC)C(N[C@@H](CC(O)=O)C(N[C@@H](CC4=CC=CC=C4)C(N)=O)=O)=O)=O)=O)=O)=O '
               'NAME: sincalide REASON: WRONGLY CLASSIFIED Contains indole '
               'moiety and exhibits complexity indicative of monoterpenoid '
               'indole alkaloids\n'
               ' * SMILES: '
               'O=C1[C@@]23C(=O)NC([C@@H]2C(C)=C([C@H]([C@@H]3C=CC[C@@H](C[C@H]([C@@H](C1)O)O)C)O)C)CC=4C5=C(C=CC=C5)NC4 '
               'NAME: Cytochalasin Y REASON: WRONGLY CLASSIFIED Contains '
               'indole moiety and exhibits complexity indicative of '
               'monoterpenoid indole alkaloids\n'
               ' * SMILES: '
               'CC[C@H](C)[C@H](N(C)C)C(=O)N[C@@H](C(C)C)C(=O)N[C@@H]1C(=O)N[C@@H](Cc2c[nH]c3ccccc23)C(=O)NCC(=O)c2ccc(OC1(C)C)cc2 '
               'NAME: Hymenocardine REASON: WRONGLY CLASSIFIED Contains indole '
               'moiety and exhibits complexity indicative of monoterpenoid '
               'indole alkaloids\n'
               ' * SMILES: '
               'SC[C@H](NC(=O)[C@@H](NC(=O)[C@@H](N)CCCN=C(N)N)CC=1C=2C(NC1)=CC=CC2)C(O)=O '
               'NAME: Arg-Trp-Cys REASON: WRONGLY CLASSIFIED Contains indole '
               'moiety and exhibits complexity indicative of monoterpenoid '
               'indole alkaloids\n'
               ' * SMILES: '
               'O=C1N[C@@H]2[C@](O)(NC([C@@H]2OC)=O)CC(=O)N(CC(=O)N[C@@H](C(=O)NCC(NC[C@H](CC(N[C@@H]([C@@H]1O)[C@H](O)[C@@H](O)C/C=C/C=C/C3=CC=CC=C3)=O)O)=O)CC=4C5=C(C=CC=C5)NC4)C '
               'NAME: Pedein B REASON: WRONGLY CLASSIFIED Contains indole '
               'moiety and exhibits complexity indicative of monoterpenoid '
               'indole alkaloids\n'
               ' * SMILES: '
               'O=C(N[C@@H]([C@H](CC)C)C(=O)N[C@@H](CC=1C=2C(NC1)=CC=CC2)C(O)=O)[C@@H](NC(=O)[C@@H](NC(=O)[C@@H](NC(=O)[C@@H](N)CC=3NC=NC3)CC(C)C)CC(O)=O)[C@H](CC)C '
               'NAME: His-leu-asp-ile-ile-trp REASON: WRONGLY CLASSIFIED '
               'Contains indole moiety and exhibits complexity indicative of '
               'monoterpenoid indole alkaloids\n'
               ' * SMILES: '
               'O=C1O[C@@H]([C@H](NC(=O)[C@@H](NC(=O)CCCCC)CC(=O)O)C(=O)N[C@H](C(=O)N[C@H]2CC[C@H](N([C@H](C(N([C@H](C(N[C@H]1C(C)C)=O)CC=3C4=C(C=CC=C4)NC3)C)=O)[C@H](CC)C)C2=O)O)CCCN=C(N)N)C '
               'NAME: Micropeptin SF995 REASON: WRONGLY CLASSIFIED Contains '
               'indole moiety and exhibits complexity indicative of '
               'monoterpenoid indole alkaloids\n'
               ' * SMILES: '
               'O=C(N[C@@H](CC=1C=2C(NC1)=CC=CC2)C(O)=O)[C@@H](NC(=O)[C@@H](N)CC=3NC=NC3)CC(O)=O '
               'NAME: His-Asp-Trp REASON: WRONGLY CLASSIFIED Contains indole '
               'moiety and exhibits complexity indicative of monoterpenoid '
               'indole alkaloids\n'
               ' * SMILES: '
               'O=C1N2[C@H](C(=O)N[C@H]1CC3=C(NC4=C3C=CC(=C4)OC)C(=O)[C@H]5OC5(C)C)CCC2 '
               'NAME: 19S,20-epoxy-18-oxotryprostatin A REASON: WRONGLY '
               'CLASSIFIED Contains indole moiety and exhibits complexity '
               'indicative of monoterpenoid indole alkaloids\n'
               'False negatives: SMILES: '
               'C/C=C\\1/CN2CC[C@]34C5=CC(C=6C=C7C(=CC6OC)[C@]89CCN%10C/C(=C\\C)/[C@](CCC8%10N7C)([C@]9(C(=O)OC)[H])[H])=C(C=C5N(C)[C@]4(C2C[C@@]1([C@@]3(C(=O)OC)[H])[H])[H])OC '
               'NAME: Desoxycabufiline REASON: MISSED Indole moiety not found\n'
               ' * SMILES: '
               'C12=C(C=CC=C1)NC=3[C@]([C@@]4(/C(/CN(CC4)CCC32)=C\\C)[H])(C(=O)OC)COC(C)=O '
               'NAME: O-acetyl-15alpha-stemmadenine REASON: MISSED Does not '
               'meet the expected structure complexity of MIAs\n'
               ' * SMILES: '
               'C/C=C\\1/CN2CC[C@@]34C5=CC=CC=C5N6[C@]4(C(=CC([C@]7(C[C@@]89C%10=CC=CC=C%10N%11C(C=C[C@@]([C@]/%12(C[C@@]8(N7C\\C%12=C\\C)[H])[H])([C@@]9%11[H])[H])=O)[H])C6=O)[C@]1(C[C@@]32[H])[H])[H] '
               'NAME: Isosungucine REASON: MISSED Indole moiety not found\n'
               ' * SMILES: '
               'CC[C@]1(C[C@]2(C[C@]3(C4=C(CCN(C2)C13)C5=CC(=C(C=C5N4)OC)OC)C(=O)OC)[H])[H] '
               'NAME: Conopharyngine REASON: MISSED Indole moiety not found\n'
               ' * SMILES: '
               '[C@@]123[C@@]4([C@]5([C@@](CC1=O)(C(CN([C@H](C2)O)C)=CCO[C@]5(CC(N4C6=C3C=CC=C6)=O)[H])[H])[H])[H] '
               'NAME: 5-hydroxyvomicine REASON: MISSED Indole moiety not '
               'found\n'
               ' * SMILES: '
               'C/C=C\\1/C[N@+]2(C)CC[C@@]34C5=CC=CC=C5NC4=C(C=O)[C@]1(C[C@@]32[H])[H] '
               'NAME: C-fluorocurarine REASON: MISSED Indole moiety not found\n'
               ' * SMILES: '
               'COC=1C=CC2=C(C1)[C@@]34CCN5C(C=C[C@@]65CC[C@]4([C@H]3C6)N2C(=O)OC)=O '
               'NAME: Lundurine A REASON: MISSED Indole moiety not found\n'
               ' * SMILES: '
               'C/C=C\\1/CN(C)[C@]2(CC=3C4=CC=CC=C4N(C)C3C(CC1C2C(=O)OC)=O)[H] '
               'NAME: Ochropamine REASON: MISSED Indole moiety not found\n'
               ' * SMILES: '
               'CC[C@@]12C=CCN3CCC=4C5=CC=CC=C5N(C4[C@]13[H])[C@](C2)(C(=O)OC)O '
               'NAME: 14,15-dehydrovincamine REASON: MISSED Indole moiety not '
               'found\n'
               ' * SMILES: '
               'C=CC1C2C[C@]3([C@@]45C(C6=CC=CC=C6N4)[C@@](CN3)(O[C@@](C25C(=O)OC)(O[C@]1(O[C@@H]7[C@H]([C@@H]([C@H]([C@H](CO)O7)O)O)O)[H])[H])[H])[H] '
               'NAME: Cymoside REASON: MISSED Indole moiety not found\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': '[H][C@@]1(O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O)O[C@@H]1[C@@H](O)[C@@H](O)[C@@H](CO)O[C@H]1OC[C@H]1O[C@@H](OC[C@H]2O[C@@H](OC[C@H](NC(=O)[C@H](O)CCCCCCCCCCCCCCCCCCCCCC)[C@H](O)[C@H](O)CCCCCCCCCCCCCC)[C@H](O)[C@@H](O)[C@H]2O)[C@H](O)[C@@H](O)[C@H]1O',
                                     'name': 'Neurosporaside',
                                     'reason': 'Indole moiety not found'},
                                 {   'smiles': '[O-]C(=O)C1=CN(C2CC2)C2=CC(N3CC[NH2+]CC3)=C(F)C=C2C1=O',
                                     'name': 'ciprofloxacin zwitterion',
                                     'reason': 'Indole moiety not found'},
                                 {   'smiles': 'O=C1NC(=CC2=C1O[C@H]([C@@H](O)CC(C)C)O2)C',
                                     'name': 'Dihydroisoflavipucine',
                                     'reason': 'Indole moiety not found'},
                                 {   'smiles': 'O=C1N2C(C(=O)N([C@@]2(OC)C)C[C@@H](O)C3=CC=CC=C3)=CC4=C1N(C=5C=CC=CC45)C',
                                     'name': 'Marinacarboline K',
                                     'reason': 'Indole moiety not found'},
                                 {   'smiles': 'O1[C@@H](O[C@H]2[C@@H](O)[C@H](O)[C@H](O[C@@H]2OC[C@H]3OC(O)[C@@H](O)[C@@H](O)[C@@H]3O)CO)[C@H](NC(=O)C)[C@@H](O)[C@H](O[C@@H]4O[C@@H]([C@H](O)[C@H](O)[C@H]4O)CO[C@]5(O[C@H]([C@H](NC(=O)C)[C@@H](O)C5)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]1CO',
                                     'name': '(2R,4S,5R,6R)-5-Acetamido-2-[[(2R,3R,4S,5R,6S)-6-[(2R,3S,4R,5R,6S)-5-acetamido-6-[(2S,3S,4S,5S,6R)-4,5-dihydroxy-6-(hydroxymethyl)-2-[[(2R,3S,4S,5S)-3,4,5,6-tetrahydroxyoxan-2-yl]methoxy]oxan-3-yl]oxy-4-hydroxy-2-(hydroxymethyl)oxan-3-yl]oxy-3,4,5-trihydroxyoxan-2-yl]methoxy]-4-hydroxy-6-[(1R,2R)-1,2,3-trihydroxypropyl]oxane-2-carboxylic '
                                             'acid',
                                     'reason': 'Indole moiety not found'},
                                 {   'smiles': 'O(C(=O)CCCCCCC)CCC1=CC=CC=C1',
                                     'name': '2-Phenylethyl octanoate',
                                     'reason': 'Indole moiety not found'},
                                 {   'smiles': 'P(OCC(OC(=O)CCCCCCC/C=C\\CCCCCCCC)COC(=O)CCC/C=C\\C/C=C\\C/C=C\\CCCCCCCC)(OCCNC)(O)=O',
                                     'name': 'PE-NMe(20:3(5Z,8Z,11Z)/18:1(9Z))',
                                     'reason': 'Indole moiety not found'},
                                 {   'smiles': 'O=C1C2=C(OC=3C1=CC=CN3)C(Cl)=CC(=C2)C=4NN=NN4',
                                     'name': 'traxanox',
                                     'reason': 'Indole moiety not found'},
                                 {   'smiles': 'CCCCC(C)CCCCCC(C)CCCCCCCCCC(C)CC(O)=O',
                                     'name': '3,13,19-trimethyltricosanoic '
                                             'acid',
                                     'reason': 'Indole moiety not found'},
                                 {   'smiles': 'COC(CC1=CC[C@]2(C)[C@@H](C)CCC[C@]2(C)C1=O)OC',
                                     'name': 'aignopsane ketal',
                                     'reason': 'Indole moiety not found'}],
    'sample_false_negatives': [   {   'smiles': 'C/C=C\\1/CN2CC[C@]34C5=CC(C=6C=C7C(=CC6OC)[C@]89CCN%10C/C(=C\\C)/[C@](CCC8%10N7C)([C@]9(C(=O)OC)[H])[H])=C(C=C5N(C)[C@]4(C2C[C@@]1([C@@]3(C(=O)OC)[H])[H])[H])OC',
                                      'name': 'Desoxycabufiline',
                                      'reason': 'Indole moiety not found'},
                                  {   'smiles': 'C=C[C@]1(CN2CCC=3C=4C=CC(=C([C@]5(CCCN5C)[H])C4NC3[C@@]2(C[C@@]1(C[C@]6(C7=C(CCN6C)C8=CC=CC=C8N7)[H])[H])[H])O)[H]',
                                      'name': 'Strychnopentamine',
                                      'reason': 'Terpene-like linkage not '
                                                'found'},
                                  {   'smiles': 'C/C=C\\1/CN2CC[C@@]34C5=CC=CC=C5N6[C@]4(C(=CC([C@]7(C[C@@]89C%10=CC=CC=C%10N%11C(C=C[C@@]([C@]/%12(C[C@@]8(N7C\\C%12=C\\C)[H])[H])([C@@]9%11[H])[H])=O)[H])C6=O)[C@]1(C[C@@]32[H])[H])[H]',
                                      'name': 'Isosungucine',
                                      'reason': 'Indole moiety not found'},
                                  {   'smiles': 'CC[C@]1(C[C@]2(C[C@]3(C4=C(CCN(C2)C13)C5=CC(=C(C=C5N4)OC)OC)C(=O)OC)[H])[H]',
                                      'name': 'Conopharyngine',
                                      'reason': 'Indole moiety not found'},
                                  {   'smiles': '[C@@]123[C@@]4([C@]5([C@@](CC1=O)(C(CN([C@H](C2)O)C)=CCO[C@]5(CC(N4C6=C3C=CC=C6)=O)[H])[H])[H])[H]',
                                      'name': '5-hydroxyvomicine',
                                      'reason': 'Indole moiety not found'},
                                  {   'smiles': 'C/C=C\\1/C[N@+]2(C)CC[C@@]34C5=CC=CC=C5NC4=C(C=O)[C@]1(C[C@@]32[H])[H]',
                                      'name': 'C-fluorocurarine',
                                      'reason': 'Indole moiety not found'},
                                  {   'smiles': 'COC=1C=CC2=C(C1)[C@@]34CCN5C(C=C[C@@]65CC[C@]4([C@H]3C6)N2C(=O)OC)=O',
                                      'name': 'Lundurine A',
                                      'reason': 'Indole moiety not found'},
                                  {   'smiles': 'C/C=C\\1/CN(C)[C@]2(CC=3C4=CC=CC=C4N(C)C3C(CC1C2C(=O)OC)=O)[H]',
                                      'name': 'Ochropamine',
                                      'reason': 'Indole moiety not found'},
                                  {   'smiles': 'CC[C@@]12C=CCN3CCC=4C5=CC=CC=C5N(C4[C@]13[H])[C@](C2)(C(=O)OC)O',
                                      'name': '14,15-dehydrovincamine',
                                      'reason': 'Indole moiety not found'},
                                  {   'smiles': 'C=CC1C2C[C@]3([C@@]45C(C6=CC=CC=C6N4)[C@@](CN3)(O[C@@](C25C(=O)OC)(O[C@]1(O[C@@H]7[C@H]([C@@H]([C@H]([C@H](CO)O7)O)O)O)[H])[H])[H])[H]',
                                      'name': 'Cymoside',
                                      'reason': 'Indole moiety not found'}],
    'attempt': 3,
    'reasoning': 'To improve the classification of monoterpenoid indole '
                 'alkaloids (MIAs), we need to address the issues from the '
                 'previous attempt by more accurately identifying the chemical '
                 'features of MIAs. We faced two main categories of issues:\n'
                 '\n'
                 '1. **False Positives**: Compounds without the defining '
                 'characteristic structure of MIAs were erroneously classified '
                 'as such. This likely results from overly broad criteria, '
                 'such as the presence of an indole moiety, which can appear '
                 'in many molecules not related to MIAs.\n'
                 '\n'
                 '2. **False Negatives**: Genuine MIAs were incorrectly '
                 'classified as not being MIAs. This suggests that the '
                 'criteria for detection were too strict or overlooked key '
                 'structural features of MIAs.\n'
                 '\n'
                 'Given these issues, we should enhance our detection approach '
                 'by including more specific structural features '
                 'characteristic of MIAs:\n'
                 '\n'
                 '- **Indole Moiety**: Check for an indole moiety, which is '
                 'essential but not sufficient for MIA classification.\n'
                 '- **Terpenoid Characteristics**: Ensure the presence of '
                 'structural features akin to a diisoprenoid linkage, such as '
                 'cyclized structures commonly associated with terpenoids.\n'
                 '- **Oxygen-containing Functional Groups**: Verify the '
                 'presence of specific functional groups (e.g., esters) from '
                 'known metabolic paths like from L-tryptophan and '
                 'secolaganin.\n'
                 '- **Chirality**: Consider the specific chiral centers, which '
                 'could be indicative of MIAs due to their natural '
                 'biosynthesis.\n'
                 '\n'
                 "We'll update the code as follows to incorporate these "
                 'detailed checks:',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 37,
    'num_false_positives': 81,
    'num_true_negatives': 142028,
    'num_false_negatives': 154,
    'num_negatives': None,
    'precision': 0.3135593220338983,
    'recall': 0.193717277486911,
    'f1': 0.2394822006472492,
    'accuracy': 0.9983485593815882,
    'negative_predictive_value': 0.9989168811804588}