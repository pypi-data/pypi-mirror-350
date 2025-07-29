"""
Classifies: CHEBI:37141 organobromine compound
"""
"""
Classifies: CHEBI:39277 organobromine compound
"""
from rdkit import Chem

def is_organobromine_compound(smiles: str):
    """
    Determines if a molecule is an organobromine compound based on its SMILES string.
    An organobromine compound is defined as a compound containing at least one carbon-bromine bond.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is an organobromine compound, False otherwise
        str: Reason for classification
    """
    
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for the presence of bromine atoms
    bromine_atoms = [atom for atom in mol.GetAtoms() if atom.GetAtomicNum() == 35]  # Atomic number of bromine is 35
    if not bromine_atoms:
        return False, "No bromine atoms found"

    # Check if any bromine atom is bonded to a carbon atom, directly or indirectly
    for bromine_atom in bromine_atoms:
        # Get all atoms connected to the bromine atom, directly or indirectly
        connected_atoms = Chem.GetMolFrags(mol, asMols=False, sanitizeFrags=False)
        for fragment in connected_atoms:
            if bromine_atom.GetIdx() in fragment:
                # Check if any carbon atom is in the same fragment as the bromine atom
                for atom_idx in fragment:
                    atom = mol.GetAtomWithIdx(atom_idx)
                    if atom.GetAtomicNum() == 6:  # Atomic number of carbon is 6
                        return True, "Contains at least one carbon-bromine bond"

    return False, "No carbon-bromine bonds found"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:37141',
                          'name': 'organobromine compound',
                          'definition': 'A compound containing at least one '
                                        'carbon-bromine bond.',
                          'parents': ['CHEBI:17792', 'CHEBI:22928'],
                          'xrefs': [   'MetaCyc:Bromide',
                                       'Wikipedia:Organobromine_compound'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 29,
                           'log_lines_of_code': 3.367295829986474,
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
                                                 2,
                                                 2,
                                                 2,
                                                 3,
                                                 4,
                                                 4,
                                                 5,
                                                 5,
                                                 6,
                                                 0,
                                                 1],
                           'max_indent': 6,
                           'imports': ['from rdkit import Chem'],
                           'imports_count': 1,
                           'methods_called': [   'GetIdx',
                                                 'MolFromSmiles',
                                                 'GetAtomWithIdx',
                                                 'GetAtomicNum',
                                                 'GetMolFrags',
                                                 'GetAtoms'],
                           'methods_called_count': 6,
                           'smarts_strings': [],
                           'smarts_strings_count': 0,
                           'defs': ['is_organobromine_compound(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "No bromine atoms found"',
                                          'True, "Contains at least one '
                                          'carbon-bromine bond"',
                                          'False, "No carbon-bromine bonds '
                                          'found"'],
                           'returns_count': 4,
                           'complexity': 4.073459165997295},
    'message': '\n'
               'Attempt failed: F1 score of 0.3346007604562737 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: C(Br)(Br)C(=O)O NAME: dibromoacetic '
               'acid REASON: CORRECT Contains at least one carbon-bromine '
               'bond\n'
               ' * SMILES: '
               'CNC(=O)c1ccc(C)c(c1)-n1c(C)cc(OCc2ccc(F)cc2F)c(Br)c1=O NAME: '
               'PH 797804 REASON: CORRECT Contains at least one carbon-bromine '
               'bond\n'
               ' * SMILES: '
               'CCCCCCCCc1ccc(cc1)-c1c(-c2ccc(CCCCCCCC)cc2)c(-c2ccc(Br)cc2)c2-c3cccc4cccc(-c2c1-c1ccc(Br)cc1)c34 '
               'NAME: '
               '7,10-bis(4-bromophenyl)-8,9-bis(4-octylphenyl)fluoranthene '
               'REASON: CORRECT Contains at least one carbon-bromine bond\n'
               ' * SMILES: '
               'O\\N=C1/Cc2cc(Br)c(Oc3cc(C\\C(C(=O)NCCc4cc(Br)c(O)c(Oc5ccc(CCNC1=O)cc5Br)c4)=N/O)cc(Br)c3O)c(Br)c2 '
               'NAME: (E,E)-bastadin 19 REASON: CORRECT Contains at least one '
               'carbon-bromine bond\n'
               ' * SMILES: '
               'CC1(C)[C@@H](C(Br)C(Br)(Br)Br)[C@H]1C(=O)O[C@H](C#N)c1cccc(Oc2ccccc2)c1 '
               'NAME: tralomethrin REASON: CORRECT Contains at least one '
               'carbon-bromine bond\n'
               ' * SMILES: C=1C=C(C2=C(C1N3C(=NN=C3Br)SCC(O)=O)C=CC=C2)C4CC4 '
               'NAME: lesinurad REASON: CORRECT Contains at least one '
               'carbon-bromine bond\n'
               ' * SMILES: '
               'Nc1ncnc2n(cc(Br)c12)[C@@H]1O[C@@H]2CO[P@@](S)(=O)O[C@H]2[C@H]1O '
               'NAME: (Sp)-7-bromo-7-deaza-cAMPS REASON: CORRECT Contains at '
               'least one carbon-bromine bond\n'
               ' * SMILES: '
               'CC(=O)OC(C)(C)[C@H]1CC[C@](O1)(C)[C@H](CC[C@@](C)([C@]2(CC[C@@]3([C@@](O2)(CC[C@@](O3)([C@@]4(CC[C@H](C(O4)(C)C)Br)C)[H])C)[H])[H])O)O '
               'NAME: thyrsiferyl 23-acetate REASON: CORRECT Contains at least '
               'one carbon-bromine bond\n'
               ' * SMILES: C1([C@H](Br)[C@H](O)CC(=C)[C@]12C=CC(=O)CC2)(C)C '
               "NAME: ma'ilione REASON: CORRECT Contains at least one "
               'carbon-bromine bond\n'
               ' * SMILES: C=1(C=C(C(=C(C1)Br)O)O)Br NAME: 3,5-dibromocatechol '
               'REASON: CORRECT Contains at least one carbon-bromine bond\n'
               ' * SMILES: C1(=C(NC2=C1C=C(C=C2)Br)Br)Br NAME: '
               '2,3,5-tribromoindole REASON: CORRECT Contains at least one '
               'carbon-bromine bond\n'
               ' * SMILES: '
               'C(=O)(C1=C(C(=CC=C1)N(C(C2=CC=CC=C2)=O)C)F)NC3=C(C=C(C=C3Br)C(C(F)(F)F)(C(F)(F)F)F)C(F)(F)F '
               'NAME: broflanilide REASON: CORRECT Contains at least one '
               'carbon-bromine bond\n'
               ' * SMILES: '
               '[H][C@@]1(O[C@H](CO)[C@@H](O)[C@H](O)[C@@H]1O)Oc1c[nH]c2ccc(Br)c(Cl)c12 '
               'NAME: 5-bromo-4-chloro-3-indolyl alpha-D-mannoside REASON: '
               'CORRECT Contains at least one carbon-bromine bond\n'
               ' * SMILES: '
               'FC1=CC=C(C=C1)C(=O)N(CC1CC1)C1=C(F)C(=CC=C1)C(=O)NC1=C(C=C(C=C1Br)C(F)(C(F)(F)F)C(F)(F)F)C(F)(F)F '
               'NAME: cyproflanilide REASON: CORRECT Contains at least one '
               'carbon-bromine bond\n'
               ' * SMILES: Brc1cccc(Br)c1 NAME: 1,3-dibromobenzene REASON: '
               'CORRECT Contains at least one carbon-bromine bond\n'
               ' * SMILES: '
               'COC1=C(Br)[C@H](O)[C@]2(CC(=NO2)C(=O)NCCCCNC(=O)C2=NO[C@]3(C2)C=C(Br)C(=O)[C@H](Br)[C@H]3O)C=C1Br '
               'NAME: (+)-aplysinillin REASON: CORRECT Contains at least one '
               'carbon-bromine bond\n'
               ' * SMILES: '
               'Nc1ncnc2n(cc(Br)c12)[C@@H]1O[C@@H]2CO[P@](S)(=O)O[C@H]2[C@H]1O '
               'NAME: (Rp)-7-bromo-7-deaza-cAMPS REASON: CORRECT Contains at '
               'least one carbon-bromine bond\n'
               ' * SMILES: CC1(C)OC=2C3=CC=CC=C3C(C(C2CC1Br)=O)=O NAME: '
               '3-bromo-beta-lapachone REASON: CORRECT Contains at least one '
               'carbon-bromine bond\n'
               ' * SMILES: C=1(C=C(C(=C(C1)Br)O)O)C(O)=O NAME: '
               '3-bromo-4,5-dihydroxybenzoic acid REASON: CORRECT Contains at '
               'least one carbon-bromine bond\n'
               ' * SMILES: CC[C@H](C)n1c(=O)[nH]c(C)c(Br)c1=O NAME: '
               '(S)-bromacil REASON: CORRECT Contains at least one '
               'carbon-bromine bond\n'
               ' * SMILES: Brc1cccnc1 NAME: 3-bromopyridine REASON: CORRECT '
               'Contains at least one carbon-bromine bond\n'
               ' * SMILES: NC(=O)c1cc(Br)c(O)c(Br)c1 NAME: '
               '3,5-dibromo-4-hydroxybenzamide REASON: CORRECT Contains at '
               'least one carbon-bromine bond\n'
               ' * SMILES: OC(=O)CCCCCBr NAME: 6-bromohexanoic acid REASON: '
               'CORRECT Contains at least one carbon-bromine bond\n'
               ' * SMILES: BrCC1CO1 NAME: epibromohydrin REASON: CORRECT '
               'Contains at least one carbon-bromine bond\n'
               ' * SMILES: OC(=O)CNC(=O)\\C=C\\CCCCCCCCCC=C(Br)Br NAME: '
               'motualevic acid A REASON: CORRECT Contains at least one '
               'carbon-bromine bond\n'
               'False positives: SMILES: '
               'CC1=CC(=C(N1CCOC)C)C(=O)COC(=O)C2=CC=C(O2)Br NAME: '
               '5-bromo-2-furancarboxylic acid '
               '[2-[1-(2-methoxyethyl)-2,5-dimethyl-3-pyrrolyl]-2-oxoethyl] '
               'ester REASON: WRONGLY CLASSIFIED Contains at least one '
               'carbon-bromine bond\n'
               ' * SMILES: C1CCN(C1)C2CCN(CC2)C(=O)C3=CC(=CN=C3)Br NAME: '
               '(5-bromo-3-pyridinyl)-[4-(1-pyrrolidinyl)-1-piperidinyl]methanone '
               'REASON: WRONGLY CLASSIFIED Contains at least one '
               'carbon-bromine bond\n'
               ' * SMILES: '
               'OC(/C=C/C(O)=O)=O.C1=C(C=C2C(=C1)C3=C4N2[C@](C[C@]5([C@@]4(N(CC3)CCC5)[H])CC)(C(=O)OC)O)Br '
               'NAME: Brovincamine fumarate REASON: WRONGLY CLASSIFIED '
               'Contains at least one carbon-bromine bond\n'
               ' * SMILES: '
               'CCCNC(=O)N(C)C[C@@H]1[C@H](CN(C(=O)C2=CC(=CN=C2O1)Br)[C@H](C)CO)C '
               'NAME: '
               '1-[[(2S,3S)-8-bromo-5-[(2R)-1-hydroxypropan-2-yl]-3-methyl-6-oxo-3,4-dihydro-2H-pyrido[2,3-b][1,5]oxazocin-2-yl]methyl]-1-methyl-3-propylurea '
               'REASON: WRONGLY CLASSIFIED Contains at least one '
               'carbon-bromine bond\n'
               ' * SMILES: '
               'C[C@@H]1CN(C(=O)C2=CC(=CN=C2O[C@H]1CN(C)C(=O)NC3=CC=CC=C3F)Br)[C@H](C)CO '
               'NAME: '
               '1-[[(2R,3R)-8-bromo-5-[(2R)-1-hydroxypropan-2-yl]-3-methyl-6-oxo-3,4-dihydro-2H-pyrido[2,3-b][1,5]oxazocin-2-yl]methyl]-3-(2-fluorophenyl)-1-methylurea '
               'REASON: WRONGLY CLASSIFIED Contains at least one '
               'carbon-bromine bond\n'
               ' * SMILES: '
               'C[C@@H]1CN(S(=O)(=O)C2=C(C=C(C=C2)Br)O[C@H]1CN(C)C(=O)C3CC3)[C@@H](C)CO '
               'NAME: '
               'N-[[(4R,5R)-8-bromo-2-[(2S)-1-hydroxypropan-2-yl]-4-methyl-1,1-dioxo-4,5-dihydro-3H-6,1$l^{6},2-benzoxathiazocin-5-yl]methyl]-N-methylcyclopropanecarboxamide '
               'REASON: WRONGLY CLASSIFIED Contains at least one '
               'carbon-bromine bond\n'
               ' * SMILES: '
               'BrC1=CC=C(\\C(=N\\OCC)\\C2CCN(C3(CCN(CC3)C(=O)C=4C(=[N+]([O-])C=CC4C)C)C)CC2)C=C1 '
               'NAME: Ancriviroc REASON: WRONGLY CLASSIFIED Contains at least '
               'one carbon-bromine bond\n'
               ' * SMILES: '
               'NCCCCNC(=O)[C@@]1(O)[C@H](c2c[nH]c3cc(Br)ccc23)[C@@](O)(Cc2c[nH]c3cc(Br)ccc23)C(=O)N1CCCCNC(N)=N '
               'NAME: Eusynstyelamide E REASON: WRONGLY CLASSIFIED Contains at '
               'least one carbon-bromine bond\n'
               ' * SMILES: '
               'CCOC(=O)[C@H](C(C)C)N(C)C(=O)[C@@H]1CCCN1C(=O)[C@@H](OC(=O)[C@H](C(C)C)N(C)C(=O)[C@@H](NC(=O)[C@@H](C)[C@H](O)CCCC#CBr)C(C)C)C(C)C '
               'NAME: Veraguamide L REASON: WRONGLY CLASSIFIED Contains at '
               'least one carbon-bromine bond\n'
               ' * SMILES: BrC1=CC(C[C@@H](C([O-])=O)[NH3+])=CC=C1O NAME: '
               '3-bromo-L-tyrosine zwitterion REASON: WRONGLY CLASSIFIED '
               'Contains at least one carbon-bromine bond\n'
               ' * SMILES: BrC=1C(=CC(Br)=C(Br)C1Br)C(O)=O NAME: '
               '2,3,4,5-Tetrabromobenzoic acid REASON: WRONGLY CLASSIFIED '
               'Contains at least one carbon-bromine bond\n'
               ' * SMILES: C1COC2=C(O1)C=CC(=C2)C(=O)NN=CC3=CC=C(O3)Br NAME: '
               'N-[(5-bromo-2-furanyl)methylideneamino]-2,3-dihydro-1,4-benzodioxin-6-carboxamide '
               'REASON: WRONGLY CLASSIFIED Contains at least one '
               'carbon-bromine bond\n'
               ' * SMILES: '
               'O.O.O.[Na+].[Na+].Nc1c(CC([O-])=O)cccc1C(=O)c1ccc(Br)cc1.Nc1c(CC([O-])=O)cccc1C(=O)c1ccc(Br)cc1 '
               'NAME: bromfenac sodium salt sesquihydrate REASON: WRONGLY '
               'CLASSIFIED Contains at least one carbon-bromine bond\n'
               ' * SMILES: '
               'C1=CC=C(C=C1)C(=O)NC2=CC=C(C=C2)C(=O)NNC(=O)C3=CC=C(O3)Br '
               'NAME: '
               'N-[4-[[[(5-bromo-2-furanyl)-oxomethyl]hydrazo]-oxomethyl]phenyl]benzamide '
               'REASON: WRONGLY CLASSIFIED Contains at least one '
               'carbon-bromine bond\n'
               ' * SMILES: C=1(C=C(CNC2CC[C@@H](CC2)O)C(N)=C(C1)Br)Br.Cl NAME: '
               'Ambroxol hydrochloride REASON: WRONGLY CLASSIFIED Contains at '
               'least one carbon-bromine bond\n'
               ' * SMILES: '
               'CN1C2=C(C(=O)NC1=O)N(C(=N2)NN=CC(=CC3=CC=CC=C3)Br)CCO NAME: '
               '8-[2-(2-bromo-3-phenylprop-2-enylidene)hydrazinyl]-7-(2-hydroxyethyl)-3-methylpurine-2,6-dione '
               'REASON: WRONGLY CLASSIFIED Contains at least one '
               'carbon-bromine bond\n'
               ' * SMILES: CC[N+]1=CC=CC=C1Br NAME: '
               '2-bromo-1-ethylpyridin-1-ium REASON: WRONGLY CLASSIFIED '
               'Contains at least one carbon-bromine bond\n'
               ' * SMILES: '
               'C\\C(=N/NC(=O)C(NC(=O)C1=CC=CC=C1)C1=NNC(=O)C2=CC=CC=C12)C1=CC=CC(Br)=C1 '
               'NAME: AC-55541 REASON: WRONGLY CLASSIFIED Contains at least '
               'one carbon-bromine bond\n'
               ' * SMILES: '
               'C[C@H]1CN(C(=O)C2=CC(=CN=C2O[C@H]1CN(C)C(=O)C3CCCCC3)Br)[C@@H](C)CO '
               'NAME: '
               'N-[[(2R,3S)-8-bromo-5-[(2S)-1-hydroxypropan-2-yl]-3-methyl-6-oxo-3,4-dihydro-2H-pyrido[2,3-b][1,5]oxazocin-2-yl]methyl]-N-methylcyclohexanecarboxamide '
               'REASON: WRONGLY CLASSIFIED Contains at least one '
               'carbon-bromine bond\n'
               ' * SMILES: CCOC1=CC2=C(C=C1)N(C(=N2)SCC(=O)C3=CC=C(S3)Br)C '
               'NAME: '
               '1-(5-bromo-2-thiophenyl)-2-[(5-ethoxy-1-methyl-2-benzimidazolyl)thio]ethanone '
               'REASON: WRONGLY CLASSIFIED Contains at least one '
               'carbon-bromine bond\n'
               ' * SMILES: '
               'CN1[C@H]([C@H]2CCN([C@H]2C3=C1C=CC(=C3)Br)C(=O)C4CCCCC4)CO '
               'NAME: '
               '[(3aS,4R,9bR)-8-bromo-4-(hydroxymethyl)-5-methyl-3,3a,4,9b-tetrahydro-2H-pyrrolo[3,2-c]quinolin-1-yl]-cyclohexylmethanone '
               'REASON: WRONGLY CLASSIFIED Contains at least one '
               'carbon-bromine bond\n'
               ' * SMILES: '
               'BrC1=CC2=C(NC([C@]2(O)C=3C4=C(C(O)=CC=C4)NC3)=O)C=C1 NAME: '
               '5-bromometagenediindole C REASON: WRONGLY CLASSIFIED Contains '
               'at least one carbon-bromine bond\n'
               ' * SMILES: COC1=CC=C(C=C1)CC2=NN3C(=NN=C3S2)C4=CC=CC=C4Br '
               'NAME: '
               '3-(2-bromophenyl)-6-[(4-methoxyphenyl)methyl]-[1,2,4]triazolo[3,4-b][1,3,4]thiadiazole '
               'REASON: WRONGLY CLASSIFIED Contains at least one '
               'carbon-bromine bond\n'
               ' * SMILES: C1=C(C=C(C2=NC(=O)C(=C21)NNC(=S)N)Br)Br NAME: '
               '[(5,7-dibromo-2-oxo-3-indolyl)amino]thiourea REASON: WRONGLY '
               'CLASSIFIED Contains at least one carbon-bromine bond\n'
               ' * SMILES: COC1=C(C(=CC(=C1)C2=NC3=CC=CC=C3S2)Br)OCC(=O)O '
               'NAME: '
               '2-[4-(1,3-benzothiazol-2-yl)-2-bromo-6-methoxyphenoxy]acetic '
               'acid REASON: WRONGLY CLASSIFIED Contains at least one '
               'carbon-bromine bond\n'
               'False negatives: SMILES: BrN1C(=O)CCC1=O NAME: '
               'N-bromosuccinimide REASON: MISSED No carbon-bromine bonds '
               'found\n'
               ' * SMILES: Brn1ccc2ccccc12 NAME: 1-bromoindole REASON: MISSED '
               'No carbon-bromine bonds found\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'C[C@@H](O)[C@H](NC(=O)Nc1ncnc2n(cnc12)[C@@H]1O[C@H](COP(O)(O)=O)[C@@H](O)[C@H]1O)C(O)=O',
                                     'name': 'N(6)-L-threonylcarbamoyladenine '
                                             "5'-monophosphate",
                                     'reason': 'No bromine atoms found'},
                                 {   'smiles': 'COC(=O)\\C=C/NC(=O)c1cc2c3cccc(O)c3[nH]c2c(n1)C(C)=O',
                                     'name': 'dichotomide V',
                                     'reason': 'No bromine atoms found'},
                                 {   'smiles': 'O=C1OC(CC=2C1=C(O)C=3C4=C(O)C=5C(=O)C6=C(C(O)=CC=C6)C(C5C(=C4[C@H](OC(=O)CC)CC3C2)OC)=O)C',
                                     'name': 'Hexaricin E',
                                     'reason': 'No bromine atoms found'},
                                 {   'smiles': 'S(CC[C@H](NC(=O)[C@@H](N)CO)C(=O)N[C@@H](CC(=O)N)C(O)=O)C',
                                     'name': 'Ser-Met-Asn',
                                     'reason': 'No bromine atoms found'},
                                 {   'smiles': 'O1C2=C(C=CC(O)=C2)C(=O)C=C1',
                                     'name': '7-Hydroxy-4-chromone',
                                     'reason': 'No bromine atoms found'},
                                 {   'smiles': 'O=C1C2=C(OC3=C1[C@H](C(=O)OC)[C@@H](O)CC3)C=C(CO)C=C2O',
                                     'name': 'Engyodontiumone E',
                                     'reason': 'No bromine atoms found'},
                                 {   'smiles': 'O=C1OC[C@H](NC(=O)[C@@H](NC(=O)CNC(=O)[C@@H](NC(=O)CCCCCCCC(C)C)[C@H](O)C)C)C(=O)N[C@@H](CC=2NC=NC2)C(N[C@H](C(N[C@H]1CCC(=O)N)=O)CCC(=O)N)=O',
                                     'name': 'N-[(2S,3R)-1-[[2-[[(2S)-1-[[(3S,6S,9S,12S)-3,6-bis(3-amino-3-oxopropyl)-9-(1H-imidazol-5-ylmethyl)-2,5,8,11-tetraoxo-1-oxa-4,7,10-triazacyclotridec-12-yl]amino]-1-oxopropan-2-yl]amino]-2-oxoethyl]amino]-3-hydroxy-1-oxobutan-2-yl]-9-methyldecanamide',
                                     'reason': 'No bromine atoms found'},
                                 {   'smiles': 'CCc1cccc(C)c1N([C@H](C)COC)C(=O)C(O)=O',
                                     'name': '(R)-metolachlor OXA',
                                     'reason': 'No bromine atoms found'},
                                 {   'smiles': 'COC(=O)[C@H]1[C@@H]([C@H]2CN3C(=CC=C(C3=O)C=CC4=CC=CC=C4)[C@@H]1N2CC5=CC=CC=C5F)CO',
                                     'name': 'LSM-10741',
                                     'reason': 'No bromine atoms found'},
                                 {   'smiles': 'O1[C@@H](O)[C@H]2C(CO)=C3C([C@@H]1C2)([C@@H](O)CC(C3)(C)C)C',
                                     'name': 'Irlactin B',
                                     'reason': 'No bromine atoms found'}],
    'sample_false_negatives': [],
    'attempt': 1,
    'reasoning': 'The previous code correctly identifies molecules with '
                 'carbon-bromine bonds, but it fails to classify some '
                 'molecules that should be considered organobromine compounds. '
                 'The main issue is that the code only checks for direct '
                 'carbon-bromine bonds, but it misses cases where the bromine '
                 'is bonded to a carbon atom indirectly through other atoms or '
                 'functional groups.\n'
                 '\n'
                 'To improve the classification, we need to ensure that the '
                 'code correctly identifies all cases where a bromine atom is '
                 'bonded to a carbon atom, either directly or indirectly. This '
                 'can be achieved by checking the entire molecular structure '
                 'for any carbon-bromine bond, regardless of the bond type or '
                 'intermediate atoms.\n'
                 '\n'
                 'Here’s the improved code:',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 310,
    'num_false_positives': 1225,
    'num_true_negatives': 140765,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.20195439739413681,
    'recall': 1.0,
    'f1': 0.33604336043360433,
    'accuracy': 0.991391426563598,
    'negative_predictive_value': 1.0}