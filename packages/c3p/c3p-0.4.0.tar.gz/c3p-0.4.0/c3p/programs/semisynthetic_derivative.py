"""
Classifies: CHEBI:72588 semisynthetic derivative
"""
from rdkit import Chem
from rdkit.Chem import rdMolDescriptors

def is_semisynthetic_derivative(smiles: str):
    """
    Determines if a molecule is classified as a semisynthetic derivative.
    It attempts to identify natural product cores with significant synthetic modifications.
    
    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if the molecule is classified as semisynthetic, False otherwise
        str: Reason for classification
    """
    
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Diverse natural product core patterns (more coverage)
    core_patterns = [
        Chem.MolFromSmarts("C1=CC=CC=C1"),  # Simple benzene ring
        Chem.MolFromSmarts("C1CCC(CC1)C(=O)O"),  # Cyclohexane carboxylic acid
        Chem.MolFromSmarts("O=C1CC[C@H](N)C2C=CC=CC12"),  # Indole-like
        Chem.MolFromSmarts("C1NC2=C(O1)C=CC=C2"),  # Pyrrolopyridine
        Chem.MolFromSmarts("[#6]1[#6][#6][#6][#6][#6][#6][#6]1"),  # Generic polycyclic structure
    ]
    
    # Broad synthetic modification patterns
    synthetic_patterns = [
        Chem.MolFromSmarts("Cl"),  # Chlorine substitution
        Chem.MolFromSmarts("[C,c][C](=O)[O,N,c]"),  # Amide/ester
        Chem.MolFromSmarts("[C,c]N=[N+]=[N-]"),  # Azide introduction
        Chem.MolFromSmarts("[C,c]S(=O)(=O)[O,N]"),  # Sulfonamide/sulfone
        Chem.MolFromSmarts("[C,c]F"),  # Fluorination
        Chem.MolFromSmarts("[C,c][N+]([O-])=O"),  # Nitro group
        Chem.MolFromSmarts("Br"),  # Bromination
    ]
    
    # Check for natural core patterns
    core_matches = any(mol.HasSubstructMatch(pattern) for pattern in core_patterns)
    
    # Check for synthetic modifications
    synthetic_matches = any(mol.HasSubstructMatch(pattern) for pattern in synthetic_patterns)
    
    # Estimate chemical complexity - an indicator of a synthetic modification
    num_rotatable_bonds = rdMolDescriptors.CalcNumRotatableBonds(mol)
    num_rings = rdMolDescriptors.CalcNumRings(mol)
    
    # Evaluate complexity and make a decision
    if core_matches and synthetic_matches:
        reason = "Molecule has natural product-like core with synthetic modifications"
        return True, reason
    
    if num_rings > 3 and num_rotatable_bonds > 5:
        reason = "Molecule shows structural complexity typical of semisynthetic derivatives"
        return True, reason
    
    return False, "No characteristic semisynthetic derivative patterns detected"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:72588',
                          'name': 'semisynthetic derivative',
                          'definition': 'Any organic molecular entity derived '
                                        'from a natural product by partial '
                                        'chemical synthesis.',
                          'parents': ['CHEBI:50860'],
                          'xrefs': ['Wikipedia:Semisynthesis'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 46,
                           'log_lines_of_code': 3.828641396489095,
                           'indent_by_line': [   1,
                                                 1,
                                                 1,
                                                 1,
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
                                                 2,
                                                 2,
                                                 2,
                                                 2,
                                                 2,
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
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 1,
                                                 1,
                                                 2,
                                                 2,
                                                 1,
                                                 1],
                           'max_indent': 2,
                           'imports': [   'from rdkit import Chem',
                                          'from rdkit.Chem import '
                                          'rdMolDescriptors'],
                           'imports_count': 2,
                           'methods_called': [   'CalcNumRotatableBonds',
                                                 'CalcNumRings',
                                                 'MolFromSmarts',
                                                 'MolFromSmiles',
                                                 'HasSubstructMatch'],
                           'methods_called_count': 5,
                           'smarts_strings': [   'C1=CC=CC=C1',
                                                 'C1NC2=C(O1)C=CC=C2',
                                                 'Br',
                                                 '[C,c][N+]([O-])=O',
                                                 '[C,c][C](=O)[O,N,c]',
                                                 '[C,c]N=[N+]=[N-]',
                                                 'C1CCC(CC1)C(=O)O',
                                                 'Cl',
                                                 '[C,c]F',
                                                 '[#6]1[#6][#6][#6][#6][#6][#6][#6]1',
                                                 '[C,c]S(=O)(=O)[O,N]',
                                                 'O=C1CC[C@H](N)C2C=CC=CC12'],
                           'smarts_strings_count': 12,
                           'defs': [   'is_semisynthetic_derivative(smiles: '
                                       'str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'True, reason',
                                          'True, reason',
                                          'False, "No characteristic '
                                          'semisynthetic derivative patterns '
                                          'detected"'],
                           'returns_count': 4,
                           'complexity': 3.165728279297819},
    'message': '\n'
               'Attempt failed: F1 score of 0.0006570062415592947 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: '
               'C=1(C(=CC=C(C1)C(C(N[C@]2([C@@]3(N(C2=O)[C@](C(S3)(C)C)(C(O)=O)[H])[H])[H])=O)OC)Cl)Cl '
               'NAME: clometocillin REASON: CORRECT Molecule has natural '
               'product-like core with synthetic modifications\n'
               ' * SMILES: '
               '[C@@H]1([C@@H]([C@H]([C@@H]([C@H](O1)COC(=O)C)O)O)O)O[C@@]23[C@]4([C@@](C2)([C@@]5(O[C@]4(O[C@]3(C5)C)[H])O)[H])COC(C6=CC=CC=C6)=O '
               "NAME: 6'-O-acetylpaeoniflorin REASON: CORRECT Molecule has "
               'natural product-like core with synthetic modifications\n'
               ' * SMILES: '
               'CN[C@H](CC(C)C)C(=O)N[C@@H]1[C@H](O)c2ccc(Oc3cc4cc(Oc5ccc(cc5Cl)[C@@H](O[C@H]5C[C@](C)(N)[C@@H](O)[C@H](C)O5)[C@@H]5NC(=O)[C@H](NC(=O)[C@@H]4NC(=O)[C@H](CC(N)=O)NC1=O)c1ccc(O)c(c1)-c1c(O)cc(O)cc1[C@H](NC5=O)C(O)=O)c3O[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O[C@H]1C[C@](C)(NCc3ccc(cc3)-c3ccc(Cl)cc3)[C@@H](O)[C@H](C)O1)c(Cl)c2 '
               'NAME: oritavancin REASON: CORRECT Molecule has natural '
               'product-like core with synthetic modifications\n'
               ' * SMILES: '
               'C=1C(=C(C2=C(C1NC(=O)C(C)=CC=C[C@@H]([C@@H](OC(N)=O)C(C)=C[C@@H]([C@H]([C@H](C[C@@H](C2)C)OC)O)C)OC)O)NCC=C)O '
               'NAME: retaspimycin REASON: CORRECT Molecule has natural '
               'product-like core with synthetic modifications\n'
               ' * SMILES: '
               'CC(C)C[C@@H]1N(C)C(=O)[C@@H](C)OC(=O)[C@H](CC(C)C)N(C)C(=O)[C@@H](Cc2ccc(cc2)N2CCOCC2)OC(=O)[C@H](CC(C)C)N(C)C(=O)[C@@H](C)OC(=O)[C@H](CC(C)C)N(C)C(=O)[C@@H](Cc2ccc(cc2)N2CCOCC2)OC1=O '
               'NAME: emodepside REASON: CORRECT Molecule has natural '
               'product-like core with synthetic modifications\n'
               ' * SMILES: '
               'N12C[C@@](C[C@H](C1)C[C@](C(=O)OC)(C3=C(C=C4C(=C3)[C@]56[C@@H]7[C@]([C@@]([C@@]([C@@]5(N4C)[H])(C(=O)OC)O)([H])OC(C)=O)(C=CCN7CC6)CC)OC)C=8NC=9C(=CC=CC9)C8C2)(C(C)(F)F)[H] '
               'NAME: vinflunine REASON: CORRECT Molecule has natural '
               'product-like core with synthetic modifications\n'
               ' * SMILES: '
               'C1=2C(=C(C=3O[C@]4(C(C3C1=C(C(=C(C2O)NC(C(=CC=C[C@@H]([C@@H]([C@H]([C@H]([C@H]([C@@H]([C@@H]([C@H](C=CO4)OC)C)OC(C)=O)C)O)C)OP(=O)(O)O)C)C)=O)/C=N/N5CCN(CC5)C)O)=O)C)C)O '
               'NAME: 21-phosphorifampicin REASON: CORRECT Molecule has '
               'natural product-like core with synthetic modifications\n'
               ' * SMILES: '
               '[H][C@@]12Cc3c[nH]c4cccc(c34)[C@@]1([H])C[C@H](CN2C)C(=O)N[C@]1(C)O[C@]2(O)N([C@@H](Cc3ccccc3)C(=O)N3CCC[C@@]23[H])C1=O '
               'NAME: dihydroergotamine REASON: CORRECT Molecule has natural '
               'product-like core with synthetic modifications\n'
               ' * SMILES: '
               'C12=C(C(=C(C=C1OCC(C2=O)CC=3C=CC(=C(C3)OC(=O)[C@@H](NC(OC(C)(C)C)=O)CC=4C=CC=CC4)OC)OC)OC)OC '
               'NAME: SH-11037 REASON: CORRECT Molecule has natural '
               'product-like core with synthetic modifications\n'
               ' * SMILES: '
               '[C@@]12(N(C[C@@H](C1)O)C([C@H]([C@@H](C)O)NC(=O)[C@](C[C@H]([C@@H](NCCN)NC([C@@H]3[C@H](CCN3C([C@H]([C@@H](CCN)O)NC(=O)[C@H]([C@@H]([C@H](C4=CC=C(C=C4)O)O)O)NC2=O)=O)O)=O)O)(NC(CCCCCCCC[C@H](C[C@H](CC)C)C)=O)[H])=O)[H] '
               'NAME: caspofungin REASON: CORRECT Molecule has natural '
               'product-like core with synthetic modifications\n'
               ' * SMILES: '
               'CN[C@@H]1c2ccc(O)c(Oc3cc(O)c(Cl)c(c3)[C@@H]3NC(=O)[C@@H](Cc4ccc(Oc5cc6cc(Oc7ccc(cc7Cl)[C@@H](O)[C@@H]7NC(=O)[C@H](NC(=O)[C@@H]6NC3=O)c3ccc(O)c(c3)-c3c(O[C@H]6O[C@H](CO)[C@@H](O)[C@H](O)[C@@H]6O)cc(O)cc3[C@H](NC7=O)C(=O)NCCCN(C)C)c5O[C@@H]3O[C@@H]([C@@H](O)[C@H](O)[C@H]3NC(=O)CCCCCCCCC(C)C)C(O)=O)cc4)NC1=O)c2 '
               'NAME: dalbavancin REASON: CORRECT Molecule has natural '
               'product-like core with synthetic modifications\n'
               ' * SMILES: '
               '[H][C@]12SCC(C)=C(N1C(=O)[C@H]2NC(=O)[C@H](N)c1ccccc1)C(O)=O '
               'NAME: cephalexin REASON: CORRECT Molecule has natural '
               'product-like core with synthetic modifications\n'
               ' * SMILES: '
               'C=1C=CC=C(C1)CC(N[C@]2([C@@]3(N(C2=O)[C@](C(S3)(C)C)(C(OCOC(=O)C)=O)[H])[H])[H])=O '
               'NAME: penamecillin REASON: CORRECT Molecule has natural '
               'product-like core with synthetic modifications\n'
               ' * SMILES: '
               '[H][C@]12SC(C)(C)[C@@H](N1C(=O)[C@H]2NC(=O)c1c(C)onc1-c1ccccc1Cl)C(O)=O '
               'NAME: cloxacillin REASON: CORRECT Molecule has natural '
               'product-like core with synthetic modifications\n'
               ' * SMILES: '
               'CO[C@H]1\\C=C\\O[C@@]2(C)Oc3c(C)c(O)c4c(O)c(NC(=O)\\C(C)=C/C=C/[C@H](C)[C@H](O)[C@@H](C)[C@@H](O)[C@@H](C)[C@H](OC(C)=O)[C@@H]1C)c(\\C=N\\N1CCN(C)CC1)c(O)c4c3C2=O '
               'NAME: rifampicin REASON: CORRECT Molecule has natural '
               'product-like core with synthetic modifications\n'
               ' * SMILES: '
               '[H][C@]12SCC(C=CC)=C(N1C(=O)[C@@]2([H])NC(=O)[C@H](N)c1ccc(O)cc1)C(O)=O '
               'NAME: cefprozil REASON: CORRECT Molecule has natural '
               'product-like core with synthetic modifications\n'
               ' * SMILES: '
               '[H][C@]12SCC(CSc3nnnn3C)=C(N1C(=O)[C@H]2NC(=O)[C@H](O)c1ccccc1)C(O)=O '
               'NAME: cefamandole REASON: CORRECT Molecule has natural '
               'product-like core with synthetic modifications\n'
               ' * SMILES: '
               'CCCCCOc1ccc(cc1)-c1ccc(cc1)-c1ccc(cc1)C(=O)N[C@H]1C[C@@H](O)[C@@H](O)NC(=O)[C@@H]2[C@@H](O)[C@@H](C)CN2C(=O)[C@@H](NC(=O)[C@@H](NC(=O)[C@@H]2C[C@@H](O)CN2C(=O)[C@@H](NC1=O)[C@@H](C)O)[C@H](O)[C@@H](O)c1ccc(O)cc1)[C@@H](C)O '
               'NAME: anidulafungin REASON: CORRECT Molecule has natural '
               'product-like core with synthetic modifications\n'
               'False positives: SMILES: '
               'CN(C)C(=O)C[C@H]1CC[C@@H]2[C@@H](O1)COC[C@@H](CN2C(=O)NC3=CC(=CC=C3)OC)O '
               'NAME: '
               '(3R,6aR,8R,10aR)-8-[2-(dimethylamino)-2-oxoethyl]-3-hydroxy-N-(3-methoxyphenyl)-3,4,6,6a,8,9,10,10a-octahydro-2H-pyrano[2,3-c][1,5]oxazocine-1-carboxamide '
               'REASON: WRONGLY CLASSIFIED Molecule has natural product-like '
               'core with synthetic modifications\n'
               ' * SMILES: '
               'C[C@H]1CN(C(=O)C2=C(C3=CC=CC=C3CO[C@H]1CN(C)S(=O)(=O)C4=CC=CC=C4C#N)C5=CC=CC=C5N2C)[C@@H](C)CO '
               'NAME: LSM-9464 REASON: WRONGLY CLASSIFIED Molecule has natural '
               'product-like core with synthetic modifications\n'
               ' * SMILES: '
               'CC1=CC=CC=C1S(=O)(=O)N2C[C@@H](COC[C@H]3[C@H]2CC[C@@H](O3)CC(=O)NCC4=CC=CC=C4Cl)O '
               'NAME: '
               '2-[(3S,6aR,8R,10aR)-3-hydroxy-1-(2-methylphenyl)sulfonyl-3,4,6,6a,8,9,10,10a-octahydro-2H-pyrano[2,3-c][1,5]oxazocin-8-yl]-N-[(2-chlorophenyl)methyl]acetamide '
               'REASON: WRONGLY CLASSIFIED Molecule has natural product-like '
               'core with synthetic modifications\n'
               ' * SMILES: '
               'C[C@H]1CN([C@H](COC2=C(C=C(C=C2)NC(=O)C)C(=O)N(C[C@H]1OC)C)C)C(=O)C3=NC=CN=C3 '
               'NAME: '
               'N-[(4S,7S,8S)-8-methoxy-4,7,10-trimethyl-11-oxo-5-[oxo(2-pyrazinyl)methyl]-2-oxa-5,10-diazabicyclo[10.4.0]hexadeca-1(12),13,15-trien-14-yl]acetamide '
               'REASON: WRONGLY CLASSIFIED Molecule has natural product-like '
               'core with synthetic modifications\n'
               ' * SMILES: '
               'C1CCN(CC1)CCNC(=O)C[C@@H]2CC[C@H]3[C@H](O2)COC[C@H](CN3S(=O)(=O)C4=CC=CC=C4)O '
               'NAME: '
               '2-[(3S,6aS,8S,10aS)-1-(benzenesulfonyl)-3-hydroxy-3,4,6,6a,8,9,10,10a-octahydro-2H-pyrano[2,3-c][1,5]oxazocin-8-yl]-N-[2-(1-piperidinyl)ethyl]acetamide '
               'REASON: WRONGLY CLASSIFIED Molecule has natural product-like '
               'core with synthetic modifications\n'
               ' * SMILES: OC1CC(N(C1)C(=O)C(N)CC2=CC=CC=C2)C(O)=O NAME: '
               'Phenylalanyl-Hydroxyproline REASON: WRONGLY CLASSIFIED '
               'Molecule has natural product-like core with synthetic '
               'modifications\n'
               ' * SMILES: O(C(C)C(O)=O)C1=CC=C(OC)C=C1 NAME: '
               '(S)-2-(4-Methoxyphenoxy)propanoic acid REASON: WRONGLY '
               'CLASSIFIED Molecule has natural product-like core with '
               'synthetic modifications\n'
               ' * SMILES: '
               'CN1C=C(N=C1)S(=O)(=O)N[C@@H]2C=C[C@H](O[C@@H]2CO)CC(=O)NC3=CC=C(C=C3)C4=CC=CC=C4 '
               'NAME: '
               '2-[(2S,3R,6R)-2-(hydroxymethyl)-3-[(1-methyl-4-imidazolyl)sulfonylamino]-3,6-dihydro-2H-pyran-6-yl]-N-(4-phenylphenyl)acetamide '
               'REASON: WRONGLY CLASSIFIED Molecule has natural product-like '
               'core with synthetic modifications\n'
               ' * SMILES: O=C(NC(CC(=O)N)C(O)=O)C(N)CC1=CC=CC=C1 NAME: '
               'Phenylalanyl-Asparagine REASON: WRONGLY CLASSIFIED Molecule '
               'has natural product-like core with synthetic modifications\n'
               ' * SMILES: CC1=CC(=CC(=C1C(=O)OC)O)OC NAME: '
               '2-hydroxy-4-methoxy-6-methylbenzoic acid methyl ester REASON: '
               'WRONGLY CLASSIFIED Molecule has natural product-like core with '
               'synthetic modifications\n'
               ' * SMILES: O(C=1C=C(CC(=O)C(O)=O)C(O)=CC1O)C NAME: '
               '3-(2,4-dihydroxy-5-methoxyphenyl)-2-oxopropanoic acid REASON: '
               'WRONGLY CLASSIFIED Molecule has natural product-like core with '
               'synthetic modifications\n'
               ' * SMILES: '
               'O=C1N([C@H](C(=O)NCC(=O)N[C@H](C(=O)N[C@H](C(=O)N[C@H](C(=O)N([C@H](C(NCC(N[C@H](C(N([C@H](C(N[C@H]1C(CC)C)=O)C(O)C)C)=O)CC(C)C)=O)=O)C(C)C)C)C(C)C)CO)C(CC)C)CC2=CC=CC=C2)C '
               'NAME: Auyuittuqamide C REASON: WRONGLY CLASSIFIED Molecule has '
               'natural product-like core with synthetic modifications\n'
               ' * SMILES: '
               'C1CCN(CC1)CCNC(=O)C[C@@H]2C[C@@H]3[C@H]([C@H](O2)CO)OC4=C3C=C(C=C4)NC(=O)CC5CC5 '
               'NAME: '
               'N-[(1R,3S,4aS,9aR)-1-(hydroxymethyl)-3-[2-oxo-2-[2-(1-piperidinyl)ethylamino]ethyl]-3,4,4a,9a-tetrahydro-1H-pyrano[3,4-b]benzofuran-6-yl]-2-cyclopropylacetamide '
               'REASON: WRONGLY CLASSIFIED Molecule has natural product-like '
               'core with synthetic modifications\n'
               ' * SMILES: '
               'C[C@@H]1CN(C(=O)C2=C(N=CC(=C2)C#CC3=CN=CC=C3)O[C@H]1CN(C)S(=O)(=O)C4=CC=CC=C4F)[C@H](C)CO '
               'NAME: '
               '2-fluoro-N-[[(2R,3R)-5-[(2R)-1-hydroxypropan-2-yl]-3-methyl-6-oxo-8-[2-(3-pyridinyl)ethynyl]-3,4-dihydro-2H-pyrido[2,3-b][1,5]oxazocin-2-yl]methyl]-N-methylbenzenesulfonamide '
               'REASON: WRONGLY CLASSIFIED Molecule has natural product-like '
               'core with synthetic modifications\n'
               ' * SMILES: OC1=C(CCC(=O)C2=CC=C(O)C=C2)C=CC(OC)=C1 NAME: '
               "2,4'-Dihydroxy-4-methoxydihydrochalcone REASON: WRONGLY "
               'CLASSIFIED Molecule has natural product-like core with '
               'synthetic modifications\n'
               ' * SMILES: '
               'CC1=CC(=NN1CC2=CC=C(C=C2)NC(=O)C3=CC=C(C=C3)COC4=CC=CC=C4Br)C '
               'NAME: '
               '4-[(2-bromophenoxy)methyl]-N-[4-[(3,5-dimethyl-1-pyrazolyl)methyl]phenyl]benzamide '
               'REASON: WRONGLY CLASSIFIED Molecule has natural product-like '
               'core with synthetic modifications\n'
               ' * SMILES: COC1=CC(=CC(=C1OC)OC)C=CC(=O)OCC(=O)NCCC2=CC=CC=C2 '
               'NAME: 3-(3,4,5-trimethoxyphenyl)-2-propenoic acid '
               '[2-oxo-2-(2-phenylethylamino)ethyl] ester REASON: WRONGLY '
               'CLASSIFIED Molecule has natural product-like core with '
               'synthetic modifications\n'
               ' * SMILES: '
               'O=C(C1=C(O)C=CC=C1O)C2=C(O)C=C(C)C=C2C(=O)C[C@@H](NC(=O)[C@@H](NC(=O)[C@@H](NC(=O)C[C@H](O)CCCCCCCCC)CC(=O)N)CCC(=O)N)CC(C)C '
               'NAME: Asperphenin B REASON: WRONGLY CLASSIFIED Molecule has '
               'natural product-like core with synthetic modifications\n'
               ' * SMILES: '
               'CC(=O)O[C@H]1CC[C@H]2[C@@H]3C[C@@H](OC(C)=O)c4cc(OC(C)=O)ccc4[C@H]3CC[C@]12C '
               'NAME: Estra-1,3,5(10)-triene-3,6beta,17beta-triol triacetate '
               'REASON: WRONGLY CLASSIFIED Molecule has natural product-like '
               'core with synthetic modifications\n'
               ' * SMILES: '
               'SC[C@H](NC(=O)[C@@H](NC(=O)[C@@H](N)CCC(O)=O)CC1=CC=CC=C1)C(O)=O '
               'NAME: Glu-Phe-Cys REASON: WRONGLY CLASSIFIED Molecule has '
               'natural product-like core with synthetic modifications\n'
               ' * SMILES: '
               'O([C@H]1[C@H](O)CC(=C[C@H]1O)C(O)=O)C(=O)/C=C/C2=CC(O)=C(O)C=C2 '
               'NAME: 4-O-Caffeoylshikimic acid REASON: WRONGLY CLASSIFIED '
               'Molecule has natural product-like core with synthetic '
               'modifications\n'
               ' * SMILES: '
               'O=C1O[C@@H]2[C@@H]([C@@H]([C@H](CC[C@H](OC)C3=CC(O)=CC=C3)C)O[C@]4(C1=C(O)[C@@H](CC4(C)C)C)C2)C '
               'NAME: Neo-debromoaplysiatoxin B REASON: WRONGLY CLASSIFIED '
               'Molecule has natural product-like core with synthetic '
               'modifications\n'
               ' * SMILES: ClC1=CC=C(CN2N=C(C=CC2=O)C)C=C1 NAME: '
               '2-(4-Chlorobenzyl)-6-methyl-2,3-dihydropyridazin-3-one REASON: '
               'WRONGLY CLASSIFIED Molecule has natural product-like core with '
               'synthetic modifications\n'
               ' * SMILES: O=C1O[C@@H](CC=CCCCCC(CC=2C1=C(O)C=C(OC)C2)=O)C '
               'NAME: Neocosmosin A REASON: WRONGLY CLASSIFIED Molecule has '
               'natural product-like core with synthetic modifications\n'
               ' * SMILES: OC(C(O)C(=O)C1=CC=CC=C1)C2=CC=CC=C2 NAME: '
               '2,3-Dihydroxy-1,3-diphenyl-1-propanone REASON: WRONGLY '
               'CLASSIFIED Molecule has natural product-like core with '
               'synthetic modifications\n'
               'False negatives: SMILES: '
               '[H][C@@]1(NC(=O)Cc2cccs2)C(=O)N2C(C(O)=O)=C(COC(C)=O)CS[C@]12[H] '
               'NAME: cefalotin REASON: MISSED No characteristic semisynthetic '
               'derivative patterns detected\n'
               ' * SMILES: '
               'COc1ccc2C[C@H]3N(C)CC[C@@]45[C@@H](Oc1c24)C(=O)CC[C@@]35O '
               'NAME: oxycodone REASON: MISSED No characteristic semisynthetic '
               'derivative patterns detected\n'
               ' * SMILES: '
               'CC[C@H](C)[C@H]1O[C@@]2(C[C@@H]3C[C@@H](C\\C=C(C)\\[C@@H](O[C@H]4C[C@H](OC)[C@@H](O[C@H]5C[C@H](OC)[C@@H](NC(C)=O)[C@H](C)O5)[C@H](C)O4)[C@@H](C)\\C=C\\C=C4/CO[C@@H]5[C@H](O)C(C)=C[C@@H](C(=O)O3)[C@]45O)O2)C=C[C@@H]1C '
               'NAME: eprinomectin component B1a REASON: MISSED No '
               'characteristic semisynthetic derivative patterns detected\n'
               ' * SMILES: '
               'CO[C@@H]1C[C@H](C[C@@H](C)[C@@H]2CC(=O)[C@H](C)\\C=C(C)\\[C@@H](O)C(OC)C(=O)[C@H](C)C[C@H](C)\\C=C\\C=C\\C=C(C)\\[C@H](C[C@@H]3CC[C@@H](C)[C@@](O)(O3)C(=O)C(=O)N3CCCC[C@H]3C(=O)O2)OC)CC[C@H]1OP(C)(C)=O '
               'NAME: ridaforolimus REASON: MISSED No characteristic '
               'semisynthetic derivative patterns detected\n'
               ' * SMILES: CCCCn1c2cc(OC)ccc2c2ccnc(C)c12 NAME: N-butylharmine '
               'REASON: MISSED No characteristic semisynthetic derivative '
               'patterns detected\n'
               ' * SMILES: '
               '[H][C@@]12CC[C@@]3(C)OO[C@@]11[C@@]([H])(CC[C@H]2C)[C@@H](C)[C@@H](OC)O[C@]1([H])O3 '
               'NAME: artemether REASON: MISSED No characteristic '
               'semisynthetic derivative patterns detected\n'
               ' * SMILES: '
               '[H][C@]12[C@H](C[C@H](O)C=C1C=C[C@H](C)[C@@H]2CC[C@@H](O)C[C@@H](O)CC(O)=O)OC(=O)[C@@H](C)CC '
               'NAME: pravastatin REASON: MISSED No characteristic '
               'semisynthetic derivative patterns detected\n'
               ' * SMILES: '
               '[C@]12(N(C(=C(CS1)C[N+]3=CC=CC=C3)C(=O)[O-])C([C@H]2NC(=O)CC=4SC=CC4)=O)[H] '
               'NAME: cefaloridine REASON: MISSED No characteristic '
               'semisynthetic derivative patterns detected\n'
               ' * SMILES: '
               'C(\\[C@H]([C@]1([C@H](/C=C/CCC[C@H](C)O)C[C@@H](C1)O)[H])O)=C/C(=O)O '
               'NAME: TX-1875 REASON: MISSED No characteristic semisynthetic '
               'derivative patterns detected\n'
               ' * SMILES: '
               'CC(C)C1=C[C@@H]2C[C@]3(C=O)[C@@H]4CC[C@@H](C)[C@H]4C[C@@]2(CO[C@H]2C[C@@H]4OC(C)(C)O[C@@H]4[C@@H](C)O2)[C@]13C(O)=O '
               'NAME: GM 193663 REASON: MISSED No characteristic semisynthetic '
               'derivative patterns detected\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'O1C=2C(=C(O)C(CC=C(C)C)=C(OC)C2)C(=O)C(C3=CC=C(O)C=C3)=C1',
                                     'name': 'Gancaonin G',
                                     'reason': 'No characteristic '
                                               'semisynthetic derivative '
                                               'patterns detected'},
                                 {   'smiles': 'S(CC[C@H](N)C(=O)N[C@@H](CCC(=O)N)C(=O)N[C@@H](C(C)C)C(O)=O)C',
                                     'name': 'Met-Gln-Val',
                                     'reason': 'No characteristic '
                                               'semisynthetic derivative '
                                               'patterns detected'},
                                 {   'smiles': 'CC(=O)N[C@H]1[C@@H](O)O[C@H](CO)[C@H](O)[C@@H]1O[C@@H]1O[C@H](CO)[C@H](O)[C@H](OS(O)(=O)=O)[C@H]1O',
                                     'name': 'beta-D-Galp3S-(1->3-)-alpha-D-GalpNAc',
                                     'reason': 'No characteristic '
                                               'semisynthetic derivative '
                                               'patterns detected'},
                                 {   'smiles': 'CN(C)C(=O)C[C@H]1CC[C@@H]2[C@@H](O1)COC[C@@H](CN2C(=O)NC3=CC(=CC=C3)OC)O',
                                     'name': '(3R,6aR,8R,10aR)-8-[2-(dimethylamino)-2-oxoethyl]-3-hydroxy-N-(3-methoxyphenyl)-3,4,6,6a,8,9,10,10a-octahydro-2H-pyrano[2,3-c][1,5]oxazocine-1-carboxamide',
                                     'reason': 'No characteristic '
                                               'semisynthetic derivative '
                                               'patterns detected'},
                                 {   'smiles': 'C[C@H]1CN([C@H](COC2=C(C=C(C=C2)NC(=O)C)C(=O)N(C[C@H]1OC)C)C)C(=O)C3=NC=CN=C3',
                                     'name': 'N-[(4S,7S,8S)-8-methoxy-4,7,10-trimethyl-11-oxo-5-[oxo(2-pyrazinyl)methyl]-2-oxa-5,10-diazabicyclo[10.4.0]hexadeca-1(12),13,15-trien-14-yl]acetamide',
                                     'reason': 'No characteristic '
                                               'semisynthetic derivative '
                                               'patterns detected'},
                                 {   'smiles': 'OC1CC(N(C1)C(=O)C(N)CC2=CC=CC=C2)C(O)=O',
                                     'name': 'Phenylalanyl-Hydroxyproline',
                                     'reason': 'No characteristic '
                                               'semisynthetic derivative '
                                               'patterns detected'},
                                 {   'smiles': 'O([C@H]1O[C@@H]([C@H]([C@@H]([C@@H]1O)O)O)CO)CCC(CCCCCCCCCCCCCCCCCCCCCCC[C@H](O)C)=O',
                                     'name': '1-(alpha-D-mannosyl)-3-keto-(1,27R)-octacosanediol',
                                     'reason': 'No characteristic '
                                               'semisynthetic derivative '
                                               'patterns detected'},
                                 {   'smiles': 'C(C(O)=O)CCCC/C=C\\C/C=C\\C\\C=C/C=C/C(C/C=C\\CC)=O',
                                     'name': '(7Z,10Z,13Z,15E,19Z)-17-oxodocosapentaenoic '
                                             'acid',
                                     'reason': 'No characteristic '
                                               'semisynthetic derivative '
                                               'patterns detected'},
                                 {   'smiles': 'OC(=O)[C@@H](NC(=O)[C@@H](NC(=O)[C@@H](N)C)C)[C@H](CC)C',
                                     'name': 'Ala-Ala-Ile',
                                     'reason': 'No characteristic '
                                               'semisynthetic derivative '
                                               'patterns detected'},
                                 {   'smiles': 'O1C2(OC=3C(C(C2O)C4=C1C=C(O)C5=C4OC(C(O)C5)C6=CC=C(O)C=C6)=C(O)C=C(O)C3)C7=CC=C(O)C=C7',
                                     'name': "(2S,2''S,3S,3''R,4S)-3,4',5,7-Tetrahydroxyflavan(2->7,4->8)-3,4',5,7-tetrahydroxyflavan",
                                     'reason': 'No characteristic '
                                               'semisynthetic derivative '
                                               'patterns detected'}],
    'sample_false_negatives': [   {   'smiles': 'C=1(C(=CC=C(C1)C(C(N[C@]2([C@@]3(N(C2=O)[C@](C(S3)(C)C)(C(O)=O)[H])[H])[H])=O)OC)Cl)Cl',
                                      'name': 'clometocillin',
                                      'reason': 'No characteristic '
                                                'semisynthetic derivative '
                                                'patterns detected'},
                                  {   'smiles': '[H][C@@]1(NC(=O)Cc2cccs2)C(=O)N2C(C(O)=O)=C(COC(C)=O)CS[C@]12[H]',
                                      'name': 'cefalotin',
                                      'reason': 'No characteristic '
                                                'semisynthetic derivative '
                                                'patterns detected'},
                                  {   'smiles': 'COc1ccc2C[C@H]3N(C)CC[C@@]45[C@@H](Oc1c24)C(=O)CC[C@@]35O',
                                      'name': 'oxycodone',
                                      'reason': 'No characteristic '
                                                'semisynthetic derivative '
                                                'patterns detected'},
                                  {   'smiles': 'C=1C(=C(C2=C(C1NC(=O)C(C)=CC=C[C@@H]([C@@H](OC(N)=O)C(C)=C[C@@H]([C@H]([C@H](C[C@@H](C2)C)OC)O)C)OC)O)NCC=C)O',
                                      'name': 'retaspimycin',
                                      'reason': 'No characteristic '
                                                'semisynthetic derivative '
                                                'patterns detected'},
                                  {   'smiles': 'CCCCn1c2cc(OC)ccc2c2ccnc(C)c12',
                                      'name': 'N-butylharmine',
                                      'reason': 'No characteristic '
                                                'semisynthetic derivative '
                                                'patterns detected'},
                                  {   'smiles': '[H][C@@]12CC[C@@]3(C)OO[C@@]11[C@@]([H])(CC[C@H]2C)[C@@H](C)[C@@H](OC)O[C@]1([H])O3',
                                      'name': 'artemether',
                                      'reason': 'No characteristic '
                                                'semisynthetic derivative '
                                                'patterns detected'},
                                  {   'smiles': '[H][C@]12[C@H](C[C@H](O)C=C1C=C[C@H](C)[C@@H]2CC[C@@H](O)C[C@@H](O)CC(O)=O)OC(=O)[C@@H](C)CC',
                                      'name': 'pravastatin',
                                      'reason': 'No characteristic '
                                                'semisynthetic derivative '
                                                'patterns detected'},
                                  {   'smiles': 'C(\\[C@H]([C@]1([C@H](/C=C/CCC[C@H](C)O)C[C@@H](C1)O)[H])O)=C/C(=O)O',
                                      'name': 'TX-1875',
                                      'reason': 'No characteristic '
                                                'semisynthetic derivative '
                                                'patterns detected'},
                                  {   'smiles': '[H][C@@]12Cc3c[nH]c4cccc(c34)[C@@]1([H])C[C@H](CN2C)C(=O)N[C@]1(C)O[C@]2(O)N([C@@H](Cc3ccccc3)C(=O)N3CCC[C@@]23[H])C1=O',
                                      'name': 'dihydroergotamine',
                                      'reason': 'No characteristic '
                                                'semisynthetic derivative '
                                                'patterns detected'},
                                  {   'smiles': 'CC[C@H]1[C@@H](O)[C@H](C)C\\C(C)=C\\C=C\\[C@H](OC)[C@H](OC(=O)\\C(OC)=C\\C(\\C)=C\\[C@@H](C)[C@H]1O)[C@@H](C)[C@@H](O)[C@H](C)[C@H]1C[C@@H](O[C@H]2C[C@@H](O)[C@H](OC(N)=O)[C@@H](C)O2)[C@H](C)[C@H](O1)\\C=C\\C',
                                      'name': '21-deoxyconcanamycin A',
                                      'reason': 'No characteristic '
                                                'semisynthetic derivative '
                                                'patterns detected'}],
    'attempt': 4,
    'reasoning': 'The previous code attempted to classify semisynthetic '
                 'derivatives by identifying natural product-like cores '
                 'combined with synthetic structural modifications. However, '
                 'it likely failed due to several challenges:\n'
                 '\n'
                 '1. **Pattern Complexity**: The chemical cores and '
                 'modifications used were too simplistic and may not capture '
                 'the complexity and diversity of real-world semisynthetic '
                 'derivatives.\n'
                 '\n'
                 "2. **Insufficient Coverage**: The patterns didn't cover the "
                 'wide variety of structures observed in semisynthetic '
                 'derivatives, which can include a diverse set of natural '
                 'cores and modifications.\n'
                 '\n'
                 '3. **Semantic Definition**: Identifying a semisynthetic '
                 "derivative isn't only about finding specific patterns; it "
                 "involves a broader assessment of the entire molecule's "
                 'origin and modifications.\n'
                 '\n'
                 'To improve, we should:\n'
                 '\n'
                 '- Broaden the scope of natural product cores by including '
                 'structural motifs common to known natural products.\n'
                 '- Enhance synthetic modification patterns by recognizing '
                 'more diverse chemical transformations.\n'
                 '- Possibly integrate functional annotations or chemical '
                 'descriptors that can give insights into the synthetic '
                 'modifications.\n'
                 '\n'
                 "Here's a revised approach:",
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 20,
    'num_false_positives': 28415,
    'num_true_negatives': 113842,
    'num_false_negatives': 23,
    'num_negatives': None,
    'precision': 0.000703358537014243,
    'recall': 0.46511627906976744,
    'f1': 0.0014045930191726949,
    'accuracy': 0.8001546029515109,
    'negative_predictive_value': 0.9997980064111008}