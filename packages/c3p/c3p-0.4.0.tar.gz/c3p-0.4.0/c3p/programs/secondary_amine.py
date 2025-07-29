"""
Classifies: CHEBI:32863 secondary amine
"""
"""
Classifies: CHEBI:32877 secondary amine
"""
from rdkit import Chem

def is_secondary_amine(smiles: str):
    """
    Determines if a molecule is a secondary amine based on its SMILES string.
    A secondary amine is a compound formally derived from ammonia by replacing two hydrogen atoms by hydrocarbyl groups.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a secondary amine, False otherwise
        str: Reason for classification
    """
    
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Look for the secondary amine pattern: [N]([C])([C])[H]
    # This pattern matches a nitrogen atom bonded to two carbon atoms and one hydrogen atom
    secondary_amine_pattern = Chem.MolFromSmarts("[NX3;H1]([CX4])([CX4])")
    
    # Check if the molecule contains the secondary amine pattern
    if mol.HasSubstructMatch(secondary_amine_pattern):
        # Exclude cases where the nitrogen is part of an amide, sulfonamide, imine, or other non-secondary amine functional groups
        amide_pattern = Chem.MolFromSmarts("[NX3]([CX3]=[OX1])")
        sulfonamide_pattern = Chem.MolFromSmarts("[NX3]([SX4](=[OX1])=[OX1])")
        imine_pattern = Chem.MolFromSmarts("[NX2]=[CX3]")
        enamine_pattern = Chem.MolFromSmarts("[NX3]([CX3]=[CX3])")
        
        if (mol.HasSubstructMatch(amide_pattern) or 
            mol.HasSubstructMatch(sulfonamide_pattern) or 
            mol.HasSubstructMatch(imine_pattern) or 
            mol.HasSubstructMatch(enamine_pattern)):
            return False, "Nitrogen is part of an amide, sulfonamide, imine, or enamine, not a secondary amine"
        
        return True, "Contains a nitrogen atom bonded to two carbon atoms and one hydrogen atom (secondary amine)"
    else:
        # Check for cases where the nitrogen is part of a ring or bonded to non-carbon atoms
        ring_nitrogen_pattern = Chem.MolFromSmarts("[NX3;H1]([CX4])([CX4])@*")
        if mol.HasSubstructMatch(ring_nitrogen_pattern):
            # Ensure the nitrogen in the ring is not part of an amide, sulfonamide, imine, or enamine
            if (mol.HasSubstructMatch(amide_pattern) or 
                mol.HasSubstructMatch(sulfonamide_pattern) or 
                mol.HasSubstructMatch(imine_pattern) or 
                mol.HasSubstructMatch(enamine_pattern)):
                return False, "Nitrogen in ring is part of an amide, sulfonamide, imine, or enamine, not a secondary amine"
            return True, "Contains a nitrogen atom bonded to two carbon atoms and one hydrogen atom in a ring (secondary amine)"
        
        return False, "No secondary amine pattern found"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:32863',
                          'name': 'secondary amine',
                          'definition': 'A compound formally derived from '
                                        'ammonia by replacing two hydrogen '
                                        'atoms by hydrocarbyl groups.',
                          'parents': ['CHEBI:32952', 'CHEBI:50995'],
                          'xrefs': ['KEGG:C02324'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 41,
                           'log_lines_of_code': 3.713572066704308,
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
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 3,
                                                 3,
                                                 3,
                                                 2,
                                                 2,
                                                 1,
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 3,
                                                 4,
                                                 4,
                                                 4,
                                                 4,
                                                 3,
                                                 2,
                                                 2],
                           'max_indent': 4,
                           'imports': ['from rdkit import Chem'],
                           'imports_count': 1,
                           'methods_called': [   'HasSubstructMatch',
                                                 'MolFromSmarts',
                                                 'MolFromSmiles'],
                           'methods_called_count': 3,
                           'smarts_strings': [   '[NX3;H1]([CX4])([CX4])@*',
                                                 '[NX3;H1]([CX4])([CX4])',
                                                 '[NX3]([SX4](=[OX1])=[OX1])',
                                                 '[NX2]=[CX3]',
                                                 '[NX3]([CX3]=[OX1])',
                                                 '[NX3]([CX3]=[CX3])'],
                           'smarts_strings_count': 6,
                           'defs': ['is_secondary_amine(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "Nitrogen is part of an '
                                          'amide, sulfonamide, imine, or '
                                          'enamine, not a secondary amine"',
                                          'True, "Contains a nitrogen atom '
                                          'bonded to two carbon atoms and one '
                                          'hydrogen atom (secondary amine)"',
                                          'False, "Nitrogen in ring is part of '
                                          'an amide, sulfonamide, imine, or '
                                          'enamine, not a secondary amine"',
                                          'True, "Contains a nitrogen atom '
                                          'bonded to two carbon atoms and one '
                                          'hydrogen atom in a ring (secondary '
                                          'amine)"',
                                          'False, "No secondary amine pattern '
                                          'found"'],
                           'returns_count': 6,
                           'complexity': 3.5427144133408617},
    'message': '\n'
               'Attempt failed: F1 score of 0.026759167492566897 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: CCCCCCCCCCCNCCCCCCCCCCC NAME: '
               'N-undecylundecan-1-amine REASON: CORRECT Contains a nitrogen '
               'atom bonded to two carbon atoms and one hydrogen atom '
               '(secondary amine)\n'
               ' * SMILES: CNCCC=C1c2ccccc2CCc2ccccc12 NAME: nortriptyline '
               'REASON: CORRECT Contains a nitrogen atom bonded to two carbon '
               'atoms and one hydrogen atom (secondary amine)\n'
               ' * SMILES: CCCCNC NAME: N-methylbutylamine REASON: CORRECT '
               'Contains a nitrogen atom bonded to two carbon atoms and one '
               'hydrogen atom (secondary amine)\n'
               ' * SMILES: CC(CCc1ccc(O)cc1)NCCc1ccc(O)c(O)c1 NAME: dobutamine '
               'REASON: CORRECT Contains a nitrogen atom bonded to two carbon '
               'atoms and one hydrogen atom (secondary amine)\n'
               ' * SMILES: CNC1CCCCC1 NAME: N-methylcyclohexylamine REASON: '
               'CORRECT Contains a nitrogen atom bonded to two carbon atoms '
               'and one hydrogen atom (secondary amine)\n'
               ' * SMILES: [H]N(C)C NAME: dimethylamine REASON: CORRECT '
               'Contains a nitrogen atom bonded to two carbon atoms and one '
               'hydrogen atom (secondary amine)\n'
               ' * SMILES: CCNCC NAME: diethylamine REASON: CORRECT Contains a '
               'nitrogen atom bonded to two carbon atoms and one hydrogen atom '
               '(secondary amine)\n'
               ' * SMILES: CC(C)NC[C@@H](O)COc1cccc2ccccc12 NAME: '
               '(R)-(+)-propranolol REASON: CORRECT Contains a nitrogen atom '
               'bonded to two carbon atoms and one hydrogen atom (secondary '
               'amine)\n'
               ' * SMILES: CC(C)NC[C@@H](O)COc1cccc2[nH]ccc12 NAME: '
               '(R)-(+)-pindolol REASON: CORRECT Contains a nitrogen atom '
               'bonded to two carbon atoms and one hydrogen atom (secondary '
               'amine)\n'
               ' * SMILES: CC(C)NCC(O)COc1cccc2ccccc12 NAME: propranolol '
               'REASON: CORRECT Contains a nitrogen atom bonded to two carbon '
               'atoms and one hydrogen atom (secondary amine)\n'
               ' * SMILES: CC(C)NCCN NAME: 2-isopropylaminoethylamine REASON: '
               'CORRECT Contains a nitrogen atom bonded to two carbon atoms '
               'and one hydrogen atom (secondary amine)\n'
               ' * SMILES: [H]C(=O)CCCNCCCN NAME: '
               'N-(3-aminopropyl)-4-aminobutanal REASON: CORRECT Contains a '
               'nitrogen atom bonded to two carbon atoms and one hydrogen atom '
               '(secondary amine)\n'
               ' * SMILES: CC(C)NCC(O)COc1ccc(COCCOC(C)C)cc1 NAME: bisoprolol '
               'REASON: CORRECT Contains a nitrogen atom bonded to two carbon '
               'atoms and one hydrogen atom (secondary amine)\n'
               ' * SMILES: CCC(C)NC NAME: N-methylbutan-2-amine REASON: '
               'CORRECT Contains a nitrogen atom bonded to two carbon atoms '
               'and one hydrogen atom (secondary amine)\n'
               ' * SMILES: C[C@@H](CCc1ccc(O)cc1)NCCc1ccc(O)c(O)c1 NAME: '
               '(S)-dobutamine REASON: CORRECT Contains a nitrogen atom bonded '
               'to two carbon atoms and one hydrogen atom (secondary amine)\n'
               ' * SMILES: C#CCN[C@@H]1CCc2ccccc12 NAME: rasagiline REASON: '
               'CORRECT Contains a nitrogen atom bonded to two carbon atoms '
               'and one hydrogen atom (secondary amine)\n'
               ' * SMILES: S(CCNC1CCCCC1)(O)(=O)=O NAME: '
               'N-cyclohexyl-2-aminoethanesulfonic acid REASON: CORRECT '
               'Contains a nitrogen atom bonded to two carbon atoms and one '
               'hydrogen atom (secondary amine)\n'
               ' * SMILES: C(Cc1ccccc1)NCc1ccccc1 NAME: benethamine REASON: '
               'CORRECT Contains a nitrogen atom bonded to two carbon atoms '
               'and one hydrogen atom (secondary amine)\n'
               ' * SMILES: CC(C)NC[C@H](O)COc1cccc2[nH]ccc12 NAME: '
               '(S)-(-)-pindolol REASON: CORRECT Contains a nitrogen atom '
               'bonded to two carbon atoms and one hydrogen atom (secondary '
               'amine)\n'
               ' * SMILES: CNCC(O)CO NAME: 3-methylamino-1,2-propanediol '
               'REASON: CORRECT Contains a nitrogen atom bonded to two carbon '
               'atoms and one hydrogen atom (secondary amine)\n'
               ' * SMILES: CCCCCCCCNCCCCCCCC NAME: dioctylamine REASON: '
               'CORRECT Contains a nitrogen atom bonded to two carbon atoms '
               'and one hydrogen atom (secondary amine)\n'
               ' * SMILES: C1=CC=C(C=C1)/C=C/C(CCO)NCC2=CC=CC=C2 NAME: '
               '(4E)-3-(benzylamino)-5-phenyl-4-penten-1-ol REASON: CORRECT '
               'Contains a nitrogen atom bonded to two carbon atoms and one '
               'hydrogen atom (secondary amine)\n'
               ' * SMILES: C=1(C(=CC=C(C1)CCN[C@@H](CCC=2C=CC(=CC2)O)C)O)O '
               'NAME: (R)-dobutamine REASON: CORRECT Contains a nitrogen atom '
               'bonded to two carbon atoms and one hydrogen atom (secondary '
               'amine)\n'
               ' * SMILES: O=CCCNCCCCN NAME: 3-[(4-aminobutyl)amino]propanal '
               'REASON: CORRECT Contains a nitrogen atom bonded to two carbon '
               'atoms and one hydrogen atom (secondary amine)\n'
               ' * SMILES: CC(C)NCC(C)(C)N NAME: '
               'N(1)-isopropyl-2-methylpropan-1,2-diamine REASON: CORRECT '
               'Contains a nitrogen atom bonded to two carbon atoms and one '
               'hydrogen atom (secondary amine)\n'
               'False positives: SMILES: '
               'Cl.C1CCC(CC1)c1ccc2n3CCNC4CCCc(c34)c2c1 NAME: tetrindole '
               'hydrochloride REASON: WRONGLY CLASSIFIED Contains a nitrogen '
               'atom bonded to two carbon atoms and one hydrogen atom '
               '(secondary amine)\n'
               ' * SMILES: '
               'CN1C2=C(C=CC(=C2)OC)C3=C1[C@@H](NCC34CN(C4)CC5=C(C=CC(=C5)F)F)CO '
               'NAME: '
               "[(1R)-1'-[(2,5-difluorophenyl)methyl]-7-methoxy-9-methyl-1-spiro[2,3-dihydro-1H-pyrido[3,4-b]indole-4,3'-azetidine]yl]methanol "
               'REASON: WRONGLY CLASSIFIED Contains a nitrogen atom bonded to '
               'two carbon atoms and one hydrogen atom (secondary amine)\n'
               ' * SMILES: COC(=O)C[C@@H]1CC[C@H]2[C@H](O1)COC[C@H](CN2)O '
               'NAME: '
               '2-[(3S,6aS,8S,10aS)-3-hydroxy-1,2,3,4,6,6a,8,9,10,10a-decahydropyrano[2,3-c][1,5]oxazocin-8-yl]acetic '
               'acid methyl ester REASON: WRONGLY CLASSIFIED Contains a '
               'nitrogen atom bonded to two carbon atoms and one hydrogen atom '
               '(secondary amine)\n'
               ' * SMILES: OC(CN1C(CC1)C(O)=O)C(NCCC(O)C(O)=O)C(O)=O NAME: '
               'Isomugineic acid REASON: WRONGLY CLASSIFIED Contains a '
               'nitrogen atom bonded to two carbon atoms and one hydrogen atom '
               '(secondary amine)\n'
               ' * SMILES: '
               'P(OCC(OC(=O)CCCCCCCCC/C=C\\CCCCCC)COC(=O)CCCCCC/C=C\\C/C=C\\C/C=C\\C/C=C\\CC)(OCCNC)(O)=O '
               'NAME: PE-NMe(20:4(8Z,11Z,14Z,17Z)/18:1(11Z)) REASON: WRONGLY '
               'CLASSIFIED Contains a nitrogen atom bonded to two carbon atoms '
               'and one hydrogen atom (secondary amine)\n'
               ' * SMILES: '
               'CCC[C@@H](C)N[C@H](N)c1ccc(cc1)-c1ccc(o1)-c1ccc(cc1)[C@@H](N)N[C@H](C)CCC '
               'NAME: '
               '(S,S)-(furan-2,5-diyldibenzene-4,1-diyl)bis{N-[(1R)-1-methylbutyl]methanediamine} '
               'REASON: WRONGLY CLASSIFIED Contains a nitrogen atom bonded to '
               'two carbon atoms and one hydrogen atom (secondary amine)\n'
               ' * SMILES: Cl.CNCC[C@@H](Oc1cccc2ccccc12)c1cccs1 NAME: '
               '(R)-duloxetine hydrochloride REASON: WRONGLY CLASSIFIED '
               'Contains a nitrogen atom bonded to two carbon atoms and one '
               'hydrogen atom (secondary amine)\n'
               ' * SMILES: COc1cc2CCN[C@H](Cc3ccc(O)cc3)c2cc1O NAME: '
               '(R)-coclaurine REASON: WRONGLY CLASSIFIED Contains a nitrogen '
               'atom bonded to two carbon atoms and one hydrogen atom '
               '(secondary amine)\n'
               ' * SMILES: NCC[C@@H](O)CNCCCC[C@H](N)C([O-])=O NAME: '
               'hypusinate REASON: WRONGLY CLASSIFIED Contains a nitrogen atom '
               'bonded to two carbon atoms and one hydrogen atom (secondary '
               'amine)\n'
               ' * SMILES: '
               'O1[C@@H]([C@H]([C@@H](C1(O)CN[C@@H](CC(C)C)C(O)=O)O)O)CO NAME: '
               'N-(1-Deoxy-1-fructosyl)leucine REASON: WRONGLY CLASSIFIED '
               'Contains a nitrogen atom bonded to two carbon atoms and one '
               'hydrogen atom (secondary amine)\n'
               ' * SMILES: '
               'P(OCC(OC(=O)CCCCCCCCCCCCCCCCC)COC(=O)CCCCCCCCC/C=C\\C/C=C\\CCCCC)(OCCNC)(O)=O '
               'NAME: PE-NMe(20:2(11Z,14Z)/18:0) REASON: WRONGLY CLASSIFIED '
               'Contains a nitrogen atom bonded to two carbon atoms and one '
               'hydrogen atom (secondary amine)\n'
               ' * SMILES: CC(C)NCC(O)COc1ccc(CC(O)=O)cc1 NAME: atenolol acid '
               'REASON: WRONGLY CLASSIFIED Contains a nitrogen atom bonded to '
               'two carbon atoms and one hydrogen atom (secondary amine)\n'
               ' * SMILES: '
               'O1[C@H](O[C@@H]2C(=C[C@H](N[C@H]3[C@H](O)[C@@H](O)[C@@H](O[C@H]4[C@H](O)[C@@H](O)[C@@H](O[C@H]5[C@H](O)[C@@H](O)[C@H](O[C@H]6[C@H](O)[C@@H](O)[C@H](O[C@H]7[C@H](O)[C@@H](O)[C@H](O)O[C@@H]7CO)O[C@@H]6CO)O[C@@H]5CO)O[C@@H]4CO)O[C@@H]3C)[C@@H]([C@H]2O)O)CO)[C@H](O)[C@@H](O)[C@@H]([C@H]1CO)O[C@H]8O[C@@H]([C@@H](N[C@H]9C=C([C@@H](O)[C@@H]([C@H]9O)O)CO)[C@@H]([C@H]8O)O)C '
               'NAME: Acarviostatin II03 REASON: WRONGLY CLASSIFIED Contains a '
               'nitrogen atom bonded to two carbon atoms and one hydrogen atom '
               '(secondary amine)\n'
               ' * SMILES: '
               'O=C(O[C@H]1[C@H](NC)CC[C@]2([C@H]1CC=C3[C@@H]2CC[C@]4([C@H]3CC[C@@H]4[C@@H](/C=C/C5=C(CN(C)CC5)C)C)C)C)C '
               'NAME: 4-acetoxy-plakinamine B REASON: WRONGLY CLASSIFIED '
               'Contains a nitrogen atom bonded to two carbon atoms and one '
               'hydrogen atom (secondary amine)\n'
               ' * SMILES: '
               '[H][C@]12CCNC[C@]1(OC[C@@]2(C(=O)OC)c1cc2ccccc2[nH]1)C=C NAME: '
               'nor-6,7-secoangustilobine A, (rel)- REASON: WRONGLY CLASSIFIED '
               'Contains a nitrogen atom bonded to two carbon atoms and one '
               'hydrogen atom (secondary amine)\n'
               ' * SMILES: CC1(C)N[C@@H](C(O)=O)C(C)(C)S1 NAME: '
               'N,S-isopropylidene-D-penicillamine REASON: WRONGLY CLASSIFIED '
               'Contains a nitrogen atom bonded to two carbon atoms and one '
               'hydrogen atom (secondary amine)\n'
               ' * SMILES: '
               'O1[C@H](O[C@@H]2C(=C[C@H](N[C@H]3[C@H](O)[C@@H](O)[C@@H](O[C@H]4[C@H](O)[C@@H](O)[C@@H](O[C@@H]5C(=C[C@H](N[C@H]6[C@H](O)[C@@H](O)[C@@H](O[C@H]7[C@H](O)[C@@H](O)[C@@H](O[C@H]8[C@H](O)[C@@H](O)[C@H](O[C@H]9[C@H](O)[C@@H](O)[C@H](O[C@H]%10[C@H](O)[C@@H](O)[C@H](O)O[C@@H]%10CO)O[C@@H]9CO)O[C@@H]8CO)O[C@@H]7CO)O[C@@H]6C)[C@@H]([C@H]5O)O)CO)O[C@@H]4CO)O[C@@H]3C)[C@@H]([C@H]2O)O)CO)[C@H](O)[C@@H](O)[C@@H]([C@H]1CO)O[C@H]%11O[C@@H]([C@@H](N[C@H]%12C=C([C@@H](O[C@H]%13O[C@@H]([C@@H](O[C@H]%14O[C@@H]([C@@H](N[C@H]%15C=C([C@@H](O)[C@@H]([C@H]%15O)O)CO)[C@@H]([C@H]%14O)O)C)[C@@H]([C@H]%13O)O)CO)[C@@H]([C@H]%12O)O)CO)[C@@H]([C@H]%11O)O)C '
               'NAME: Acarviostatin IV03 REASON: WRONGLY CLASSIFIED Contains a '
               'nitrogen atom bonded to two carbon atoms and one hydrogen atom '
               '(secondary amine)\n'
               ' * SMILES: CNCCCCC(N)C(O)=O NAME: N(6)-methyllysine REASON: '
               'WRONGLY CLASSIFIED Contains a nitrogen atom bonded to two '
               'carbon atoms and one hydrogen atom (secondary amine)\n'
               ' * SMILES: C(C(NCCCCl)C)C1=CC=CC=C1 NAME: mefenorex REASON: '
               'WRONGLY CLASSIFIED Contains a nitrogen atom bonded to two '
               'carbon atoms and one hydrogen atom (secondary amine)\n'
               ' * SMILES: '
               'C12=C(C(=CC(=N1)C(F)(F)F)[C@@H]([C@]3(CCCCN3)[H])O)C=CC=C2C(F)(F)F.Cl '
               'NAME: Mefloquine hydrochloride REASON: WRONGLY CLASSIFIED '
               'Contains a nitrogen atom bonded to two carbon atoms and one '
               'hydrogen atom (secondary amine)\n'
               ' * SMILES: '
               'C1CCC(CC1)C#CC2=CC=C(C=C2)[C@@H]3[C@@H](N[C@@H]3C#N)CO NAME: '
               '(2S,3S,4R)-3-[4-(2-cyclohexylethynyl)phenyl]-4-(hydroxymethyl)-2-azetidinecarbonitrile '
               'REASON: WRONGLY CLASSIFIED Contains a nitrogen atom bonded to '
               'two carbon atoms and one hydrogen atom (secondary amine)\n'
               ' * SMILES: '
               'C[C@@H](C1=CC(=C(C=C1)Cl)Cl)NC[C@@H](CP(=O)(CC2=CC=CC=C2)O)O '
               'NAME: '
               '[(2S)-3-[[(1S)-1-(3,4-dichlorophenyl)ethyl]amino]-2-hydroxypropyl]-(phenylmethyl)phosphinic '
               'acid REASON: WRONGLY CLASSIFIED Contains a nitrogen atom '
               'bonded to two carbon atoms and one hydrogen atom (secondary '
               'amine)\n'
               ' * SMILES: CC(Oc1cc(cnc1N)-c1cnn(c1)C1CCNCC1)c1c(Cl)ccc(F)c1Cl '
               'NAME: rac-crizotinib REASON: WRONGLY CLASSIFIED Contains a '
               'nitrogen atom bonded to two carbon atoms and one hydrogen atom '
               '(secondary amine)\n'
               ' * SMILES: '
               'C[C@H](Oc1cc(cnc1N)-c1cnn(c1)C1CCNCC1)c1c(Cl)ccc(F)c1Cl NAME: '
               'ent-crizotinib REASON: WRONGLY CLASSIFIED Contains a nitrogen '
               'atom bonded to two carbon atoms and one hydrogen atom '
               '(secondary amine)\n'
               ' * SMILES: '
               'COc1cc(O)c(c2C[C@H](C)N[C@@H](C)c12)-c1c(C)cc(OC)c2c(OC)cccc12 '
               'NAME: Ancistrocladine REASON: WRONGLY CLASSIFIED Contains a '
               'nitrogen atom bonded to two carbon atoms and one hydrogen atom '
               '(secondary amine)\n'
               'False negatives: SMILES: OCC(O)CNc1ccccc1 NAME: PAP REASON: '
               'MISSED No secondary amine pattern found\n'
               ' * SMILES: Brc1c(NC2=NCCN2)ccc2nccnc12 NAME: brimonidine '
               'REASON: MISSED No secondary amine pattern found\n'
               ' * SMILES: c1cc[nH]c1 NAME: 1H-pyrrole REASON: MISSED No '
               'secondary amine pattern found\n'
               ' * SMILES: O=NN1CCCCC1 NAME: N-nitrosopiperidine REASON: '
               'MISSED No secondary amine pattern found\n'
               ' * SMILES: '
               '[H][C@@]12[C@]3(C)CCC[C@]1(C)c1cc4C(=O)C5=C(C(=O)c4cc1C(=O)[C@]2(O)OC3)S(=O)(=O)CCN5 '
               'NAME: alisiaquninone C REASON: MISSED No secondary amine '
               'pattern found\n'
               ' * SMILES: CNC1=C(N=NC(=N1)C2=CC=CC=N2)C3=CC=CC=C3 NAME: '
               'N-methyl-6-phenyl-3-(2-pyridinyl)-1,2,4-triazin-5-amine '
               'REASON: MISSED No secondary amine pattern found\n'
               ' * SMILES: S1C(NC#N)=NN=C1 NAME: amitivir REASON: MISSED No '
               'secondary amine pattern found\n'
               ' * SMILES: O1N=C(NCC2=CN=CC=C2)C=C1C NAME: '
               '5-methyl-n-(pyridin-3-ylmethyl)isoxazol-3-amine REASON: MISSED '
               'No secondary amine pattern found\n'
               ' * SMILES: C1CCC(CC1)CNC2=C(N=NC(=N2)C3=CC=CC=N3)C4=CC=CC=C4 '
               'NAME: '
               'N-(cyclohexylmethyl)-6-phenyl-3-(2-pyridinyl)-1,2,4-triazin-5-amine '
               'REASON: MISSED No secondary amine pattern found\n'
               ' * SMILES: O=C1OC2=CC=C([C@H](O)CNC=3C=C1C=CC3O)C=C2 NAME: '
               'Bagrelactone A REASON: MISSED No secondary amine pattern '
               'found\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'C[C@@H]1CN(C(=O)CC2=C(C=CC(=C2)NC(=O)NC(C)C)O[C@H]1CN(C)S(=O)(=O)C)[C@@H](C)CO',
                                     'name': '1-[(2R,3R)-5-[(2S)-1-hydroxypropan-2-yl]-3-methyl-2-[[methyl(methylsulfonyl)amino]methyl]-6-oxo-2,3,4,7-tetrahydro-1,5-benzoxazonin-9-yl]-3-propan-2-ylurea',
                                     'reason': 'No secondary amine pattern '
                                               'found'},
                                 {   'smiles': '[H][C@@]12C[C@@]3([H])C(C)=CC(=O)[C@@H](O)[C@]3(C)[C@@]3([H])[C@]4(O)OC[C@@]13[C@@](O)([C@@H](O)C(=O)O2)C(=C)[C@H]4O',
                                     'name': 'eurycomanone',
                                     'reason': 'No secondary amine pattern '
                                               'found'},
                                 {   'smiles': 'O1C2C(C3(O)C(C4C(OC5=C(C4)C(OC(C5)C)=O)(CC3)C)(C(=O)C12)C)(C)C',
                                     'name': '8-Hydroxy-2,7,7,11,15-pentamethyl-5,12,16-trioxapentacyclo[9.8.0.0(2),.0,.0(1)(3),(1)]nonadec-13(18)-ene-3,17-dione',
                                     'reason': 'No secondary amine pattern '
                                               'found'},
                                 {   'smiles': 'S1CC(CSC1=S)C=2N=CC=CC2',
                                     'name': '5-(2-Pyridinyl)-1,3-dithiane-2-thione',
                                     'reason': 'No secondary amine pattern '
                                               'found'},
                                 {   'smiles': 'OC(=O)C[C@H](NC(=O)[C@@H]1CCCN1)C(O)=O',
                                     'name': 'Pro-Asp',
                                     'reason': 'Nitrogen is part of an amide, '
                                               'sulfonamide, imine, or '
                                               'enamine, not a secondary '
                                               'amine'},
                                 {   'smiles': 'C1CN(CCN1C2=CC=CC=C2)C(=O)CN3C=NC4=C(C3=O)N=NN4CC5=CC=CC=C5',
                                     'name': '6-[2-oxo-2-(4-phenyl-1-piperazinyl)ethyl]-3-(phenylmethyl)-7-triazolo[4,5-d]pyrimidinone',
                                     'reason': 'No secondary amine pattern '
                                               'found'},
                                 {   'smiles': 'S(=O)(=O)(C1=CC=C(NO)C=C1)C2=CC=C(N)C=C2',
                                     'name': 'dapsone hydroxylamine',
                                     'reason': 'No secondary amine pattern '
                                               'found'},
                                 {   'smiles': 'CC(C)c1nc2nc(N)nc(N)c2nc1C(C)C',
                                     'name': '2,4-diamino-6,7-diisopropylpteridine',
                                     'reason': 'No secondary amine pattern '
                                               'found'},
                                 {   'smiles': 'O=C(N[C@@H](CC=1NC=NC1)C(=O)N[C@@H](CCC(=O)N)C(O)=O)[C@@H](N)CC=2C=3C(NC2)=CC=CC3',
                                     'name': 'Trp-His-Gln',
                                     'reason': 'No secondary amine pattern '
                                               'found'},
                                 {   'smiles': 'CC1=CC=C(C=C1)S(=O)(=O)N(C[C@@H](C)[C@@H](CN(C)C(=O)C2=CC3=C(C=C2)OCO3)OC)[C@@H](C)CO',
                                     'name': 'N-[(2S,3R)-4-[[(2S)-1-hydroxypropan-2-yl]-(4-methylphenyl)sulfonylamino]-2-methoxy-3-methylbutyl]-N-methyl-1,3-benzodioxole-5-carboxamide',
                                     'reason': 'No secondary amine pattern '
                                               'found'}],
    'sample_false_negatives': [   {   'smiles': 'OCC(O)CNc1ccccc1',
                                      'name': 'PAP',
                                      'reason': 'No secondary amine pattern '
                                                'found'},
                                  {   'smiles': 'Brc1c(NC2=NCCN2)ccc2nccnc12',
                                      'name': 'brimonidine',
                                      'reason': 'No secondary amine pattern '
                                                'found'},
                                  {   'smiles': 'c1cc[nH]c1',
                                      'name': '1H-pyrrole',
                                      'reason': 'No secondary amine pattern '
                                                'found'},
                                  {   'smiles': 'O=NN1CCCCC1',
                                      'name': 'N-nitrosopiperidine',
                                      'reason': 'No secondary amine pattern '
                                                'found'},
                                  {   'smiles': '[H][C@@]12[C@]3(C)CCC[C@]1(C)c1cc4C(=O)C5=C(C(=O)c4cc1C(=O)[C@]2(O)OC3)S(=O)(=O)CCN5',
                                      'name': 'alisiaquninone C',
                                      'reason': 'No secondary amine pattern '
                                                'found'},
                                  {   'smiles': 'CNC1=C(N=NC(=N1)C2=CC=CC=N2)C3=CC=CC=C3',
                                      'name': 'N-methyl-6-phenyl-3-(2-pyridinyl)-1,2,4-triazin-5-amine',
                                      'reason': 'No secondary amine pattern '
                                                'found'},
                                  {   'smiles': 'S1C(NC#N)=NN=C1',
                                      'name': 'amitivir',
                                      'reason': 'No secondary amine pattern '
                                                'found'},
                                  {   'smiles': 'O1N=C(NCC2=CN=CC=C2)C=C1C',
                                      'name': '5-methyl-n-(pyridin-3-ylmethyl)isoxazol-3-amine',
                                      'reason': 'No secondary amine pattern '
                                                'found'},
                                  {   'smiles': 'C1CCC(CC1)CNC2=C(N=NC(=N2)C3=CC=CC=N3)C4=CC=CC=C4',
                                      'name': 'N-(cyclohexylmethyl)-6-phenyl-3-(2-pyridinyl)-1,2,4-triazin-5-amine',
                                      'reason': 'No secondary amine pattern '
                                                'found'},
                                  {   'smiles': 'O=C1OC2=CC=C([C@H](O)CNC=3C=C1C=CC3O)C=C2',
                                      'name': 'Bagrelactone A',
                                      'reason': 'No secondary amine pattern '
                                                'found'}],
    'attempt': 2,
    'reasoning': 'The previous code had several issues that led to both false '
                 "positives and false negatives. Let's analyze the problems "
                 'and propose improvements:\n'
                 '\n'
                 '1. **False Positives**:\n'
                 '   - The code incorrectly classified molecules with nitrogen '
                 'atoms in amides, sulfonamides, and other non-secondary amine '
                 'functional groups as secondary amines.\n'
                 '   - The exclusion patterns for amides and sulfonamides were '
                 'not comprehensive enough.\n'
                 '\n'
                 '2. **False Negatives**:\n'
                 '   - The code missed some secondary amines, particularly '
                 'those in rings or with more complex structures.\n'
                 "   - The pattern matching was too restrictive and didn't "
                 'account for all possible secondary amine configurations.\n'
                 '\n'
                 '**Improvements**:\n'
                 '1. **Enhanced Pattern Matching**:\n'
                 '   - Use a more comprehensive pattern to match secondary '
                 'amines, including those in rings and with various '
                 'substituents.\n'
                 '   - Ensure the pattern matches nitrogen atoms bonded to two '
                 'carbon atoms and one hydrogen atom, regardless of the '
                 'surrounding structure.\n'
                 '\n'
                 '2. **Better Exclusion Criteria**:\n'
                 '   - Add more exclusion patterns to prevent '
                 'misclassification of amides, sulfonamides, and other '
                 'non-secondary amine functional groups.\n'
                 '   - Include patterns for imines, enamines, and other '
                 'nitrogen-containing functional groups that are not secondary '
                 'amines.\n'
                 '\n'
                 '3. **Improved Ring Handling**:\n'
                 '   - Modify the pattern to better handle nitrogen atoms in '
                 'rings, ensuring they are correctly identified as secondary '
                 'amines when appropriate.\n'
                 '\n'
                 'Here is the improved code:',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 27,
    'num_false_positives': 1886,
    'num_true_negatives': 140370,
    'num_false_negatives': 17,
    'num_negatives': None,
    'precision': 0.014113957135389441,
    'recall': 0.6136363636363636,
    'f1': 0.027593254982115484,
    'accuracy': 0.9866268446943078,
    'negative_predictive_value': 0.9998789061665254}