"""
Classifies: CHEBI:50263 2-hydroxydicarboxylic acid
"""
"""
Classifies: CHEBI:35681 2-hydroxydicarboxylic acid
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_2_hydroxydicarboxylic_acid(smiles: str):
    """
    Determines if a molecule is a 2-hydroxydicarboxylic acid based on its SMILES string.
    A 2-hydroxydicarboxylic acid has two carboxylic acid groups and a hydroxy group
    on the alpha carbon of one of the carboxyl groups.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a 2-hydroxydicarboxylic acid, False otherwise
        str: Reason for classification
    """
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Find carboxylic acid groups
    carboxyl_pattern = Chem.MolFromSmarts('C(=O)[OH]')
    carboxyl_matches = mol.GetSubstructMatches(carboxyl_pattern)
    
    if len(carboxyl_matches) != 2:
        return False, f"Found {len(carboxyl_matches)} carboxylic acid groups, need exactly 2"

    # Find alpha-hydroxy carboxylic acid pattern
    # Carbon with OH group that's also connected to a carboxyl group
    alpha_hydroxy_pattern = Chem.MolFromSmarts('[OH1]-[CH1,CH0]-C(=O)[OH1]')
    alpha_hydroxy_matches = mol.GetSubstructMatches(alpha_hydroxy_pattern)
    
    if not alpha_hydroxy_matches:
        return False, "No alpha-hydroxy carboxylic acid group found"

    # Get total atom count (excluding H)
    heavy_atom_count = mol.GetNumHeavyAtoms()
    
    # Check if molecule is too complex (likely not a simple dicarboxylic acid)
    if heavy_atom_count > 15:  # Most 2-hydroxydicarboxylic acids are relatively small
        return False, "Molecule too complex for a simple 2-hydroxydicarboxylic acid"

    # Count number of carbons and oxygens to ensure reasonable composition
    c_count = sum(1 for atom in mol.GetAtoms() if atom.GetAtomicNum() == 6)
    o_count = sum(1 for atom in mol.GetAtoms() if atom.GetAtomicNum() == 8)
    
    if o_count != 5:  # 2 from carboxylic acids (2*2=4) + 1 from hydroxy = 5
        return False, "Must have exactly 5 oxygen atoms"

    # Check for presence of unexpected elements
    allowed_elements = {1, 6, 8}  # H, C, O
    for atom in mol.GetAtoms():
        if atom.GetAtomicNum() not in allowed_elements:
            return False, "Contains elements other than C, H, and O"

    # Check ring count - most simple 2-hydroxydicarboxylic acids are not cyclic
    ring_info = mol.GetRingInfo()
    if ring_info.NumRings() > 0:
        return False, "Contains rings - most 2-hydroxydicarboxylic acids are acyclic"

    return True, "Contains two carboxylic acid groups with a hydroxy group on the alpha carbon"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:50263',
                          'name': '2-hydroxydicarboxylic acid',
                          'definition': 'Any dicarboxylic acid carrying a '
                                        'hydroxy group on the carbon atom at '
                                        'position alpha to the carboxy group.',
                          'parents': ['CHEBI:35692'],
                          'xrefs': ['KEGG:C03668'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': None,
    'message': '\n'
               'Attempt failed: F1 score of 0.15841584158415842 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: C[C@H](C(O)=O)[C@@](C)(O)C(O)=O NAME: '
               '(2R,3S)-2,3-dimethylmalic acid REASON: CORRECT Contains two '
               'carboxylic acid groups with a hydroxy group on the alpha '
               'carbon\n'
               ' * SMILES: CC(O)(CC(O)=O)C(O)=O NAME: citramalic acid REASON: '
               'CORRECT Contains two carboxylic acid groups with a hydroxy '
               'group on the alpha carbon\n'
               ' * SMILES: CC(C(O)=O)C(C)(O)C(O)=O NAME: 2,3-dimethylmalic '
               'acid REASON: CORRECT Contains two carboxylic acid groups with '
               'a hydroxy group on the alpha carbon\n'
               ' * SMILES: C[C@@](O)(CC(O)=O)C(O)=O NAME: D-citramalic acid '
               'REASON: CORRECT Contains two carboxylic acid groups with a '
               'hydroxy group on the alpha carbon\n'
               ' * SMILES: C[C@](O)(CC(O)=O)C(O)=O NAME: L-citramalic acid '
               'REASON: CORRECT Contains two carboxylic acid groups with a '
               'hydroxy group on the alpha carbon\n'
               ' * SMILES: C(C(CP(=O)(O)[H])(C(O)=O)O)C(O)=O NAME: '
               '2-phosphinomethylmalic acid REASON: CORRECT Contains two '
               'carboxylic acid groups with a hydroxy group on the alpha '
               'carbon\n'
               ' * SMILES: CSCCCC(O)(CC(O)=O)C(O)=O NAME: '
               '2-(3-methylthiopropyl)malic acid REASON: CORRECT Contains two '
               'carboxylic acid groups with a hydroxy group on the alpha '
               'carbon\n'
               ' * SMILES: CC[C@@](O)(CC(O)=O)C(O)=O NAME: (R)-2-ethylmalic '
               'acid REASON: CORRECT Contains two carboxylic acid groups with '
               'a hydroxy group on the alpha carbon\n'
               'False positives: SMILES: '
               'O=C1O[C@@H](C(=O)O)[C@@]([C@H]1CCCCCCCCCCC=C)(O)C(=O)O NAME: '
               'Cinatrin E REASON: WRONGLY CLASSIFIED Contains two carboxylic '
               'acid groups with a hydroxy group on the alpha carbon\n'
               ' * SMILES: OC(CC(=O)C)(CC(O)=O)C(O)=O NAME: '
               '2-Hydroxy-2-(2-oxopropyl)butanedioic acid REASON: WRONGLY '
               'CLASSIFIED Contains two carboxylic acid groups with a hydroxy '
               'group on the alpha carbon\n'
               ' * SMILES: CSCCCCC(O)(CC(O)=O)C(O)=O NAME: '
               "2-(4'-Methylthio)butylmalic acid REASON: WRONGLY CLASSIFIED "
               'Contains two carboxylic acid groups with a hydroxy group on '
               'the alpha carbon\n'
               ' * SMILES: OC(CC1=CC=CC=C1)(C(O)C(O)=O)C(O)=O NAME: '
               'hydroxybenzyltartaric acid REASON: WRONGLY CLASSIFIED Contains '
               'two carboxylic acid groups with a hydroxy group on the alpha '
               'carbon\n'
               ' * SMILES: OC(CC1=CC=C(O)C=C1)(CC(O)=O)C(O)=O NAME: '
               '2-hydroxy-2-(4-hydroxybenzyl)succinic acid REASON: WRONGLY '
               'CLASSIFIED Contains two carboxylic acid groups with a hydroxy '
               'group on the alpha carbon\n'
               ' * SMILES: '
               '[C@@H]1([C@@H]([C@H]([C@@H]([C@H](O1)CO)O)O)O)O[C@@H]2[C@H]([C@H](O[C@@H]([C@H]2O)CO)O[C@@H]3[C@H]([C@H](O[C@@H]([C@H]3O)CO)O[C@H]4[C@@H]([C@](O[C@H]([C@H]4O)O[C@H]5[C@@H]([C@](O[C@@H]([C@H]5O)O[C@H]6[C@](O[C@@](C[C@H]6O[C@@]7(C[C@H]([C@H]([C@](O7)([C@H](O)CO)[H])O)O)C(=O)O)(O)C(=O)O)([C@H](O)CO)[H])([C@H](CO)O)[H])OP(O)(=O)O)([C@@H](CO[C@H]8O[C@@]([C@H]([C@@H]([C@@H]8O)O)O)([C@@H](O)CO)[H])O)[H])OP(=O)(O)O)O)O[C@@H]9[C@@H]([C@H]([C@H]([C@H](O9)CO)O)O)O[C@@H]%10[C@@H]([C@H]([C@H]([C@H](O%10)CO)O)O)O '
               'NAME: E. coli strain O157 LPS core oligosaccharide R1 REASON: '
               'WRONGLY CLASSIFIED Contains two carboxylic acid groups with a '
               'hydroxy group on the alpha carbon\n'
               ' * SMILES: '
               'O[C@](CC1=CC(O)=C(O)C=C1)([C@H](OC(=O)/C=C/C2=CC(O)=C(O)C=C2)C(O)=O)C(O)=O '
               'NAME: Fukinolic acid REASON: WRONGLY CLASSIFIED Contains two '
               'carboxylic acid groups with a hydroxy group on the alpha '
               'carbon\n'
               ' * SMILES: '
               '[H][C@@]1(O[C@H](O[C@@H]2[C@@H](C[C@@](O)(O[C@]2([H])[C@H](O)CO)C(O)=O)O[C@@]2(C[C@@H](O)[C@@H](O)[C@]([H])(O2)[C@H](O)CO)C(O)=O)[C@@H](O)[C@@H](O[C@H]2O[C@@]([H])([C@@H](O)[C@H](O[C@@H]3O[C@H](CO)[C@@H](O)[C@H](O)[C@H]3O)[C@@H]2O[C@H]2O[C@H](CO)[C@@H](O)[C@H](O)[C@H]2NC(C)=O)[C@H](CO)OP(O)(=O)OCCN)[C@@H]1O)[C@@H](O)CO '
               'NAME: '
               'D-Glcp-(1->3)-[alpha-D-GlcpNAc-(1->2)]-6-PEA-L-alpha-D-Hepp-(1->3)-L-alpha-D-Hepp-(1->5)-[alpha-Kdo-(2->4)]-alpha-Kdo '
               'REASON: WRONGLY CLASSIFIED Contains two carboxylic acid groups '
               'with a hydroxy group on the alpha carbon\n'
               ' * SMILES: '
               'O[C@]([C@H](O)[C@@](O)(C(=O)/C=C/C1=CC(O)=C(O)C=C1)C(O)=O)([C@H](O)C(O)=O)C(=O)/C=C/C2=CC(O)=C(O)C=C2 '
               'NAME: 3,5-dicaffeoylaltraric acid REASON: WRONGLY CLASSIFIED '
               'Contains two carboxylic acid groups with a hydroxy group on '
               'the alpha carbon\n'
               ' * SMILES: OC(CC(OC)=O)(CC(O)=O)C(O)=O NAME: '
               '2-Hydroxy-2-(2-methoxy-2-oxoethyl)butanedioic acid REASON: '
               'WRONGLY CLASSIFIED Contains two carboxylic acid groups with a '
               'hydroxy group on the alpha carbon\n'
               ' * SMILES: '
               'O=C1O[C@@H](C(=O)O)[C@]([C@H]1[C@@H](O)CCCCCCCCCCC)(O)C(=O)O '
               'NAME: Cinatrin C2 REASON: WRONGLY CLASSIFIED Contains two '
               'carboxylic acid groups with a hydroxy group on the alpha '
               'carbon\n'
               ' * SMILES: '
               'O[C@@H]([C@@H](O)[C@H](O)C(O)=O)[C@@](O)(C(=O)/C=C/C1=CC(O)=C(O)C=C1)C(O)=O '
               'NAME: 2-caffeoylaltraric acid REASON: WRONGLY CLASSIFIED '
               'Contains two carboxylic acid groups with a hydroxy group on '
               'the alpha carbon\n'
               ' * SMILES: O[C@H]1C=C(C=C[C@]1(O)C(O)=O)C(O)=O NAME: '
               '(3S,4R)-3,4-dihydroxycyclohexa-1,5-diene-1,4-dicarboxylic acid '
               'REASON: WRONGLY CLASSIFIED Contains two carboxylic acid groups '
               'with a hydroxy group on the alpha carbon\n'
               ' * SMILES: '
               '[H][C@]1(C[C@@H](OC[C@@H](O)[C@@]2([H])O[C@](O)(C[C@@H](O)[C@H]2O)C(O)=O)C=C(O1)C(O)=O)[C@H](O)CO '
               'NAME: 5-deoxy-4-epi-2,3-dehydro-Kdo-(4->8)-alpha-Kdo REASON: '
               'WRONGLY CLASSIFIED Contains two carboxylic acid groups with a '
               'hydroxy group on the alpha carbon\n'
               ' * SMILES: '
               '[C@@H]1(N2C3=C(C(=NC=N3)N)N=C2)O[C@H](COP(OP(OCC(C)([C@H](C(NCCC(NCCSC(=O)C[C@@](C(=O)O)(O)CC(=O)O)=O)=O)O)C)(=O)O)(=O)O)[C@H]([C@H]1O)OP(O)(O)=O '
               'NAME: (3S)-citryl-CoA REASON: WRONGLY CLASSIFIED Contains two '
               'carboxylic acid groups with a hydroxy group on the alpha '
               'carbon\n'
               ' * SMILES: OC(CC(OC(C)C)=O)(CC(O)=O)C(O)=O NAME: 1-Isopropyl '
               'citrate REASON: WRONGLY CLASSIFIED Contains two carboxylic '
               'acid groups with a hydroxy group on the alpha carbon\n'
               ' * SMILES: '
               '[H][C@]1(CC=C[C@@](OC[C@@H](O)[C@@]2([H])O[C@](O)(C[C@@H](O)[C@H]2O)C(O)=O)(O1)C(O)=O)[C@H](O)CO '
               'NAME: alpha-3,4-dehydro-3,4,5-trideoxy-Kdo-(2->8)-alpha-Kdo '
               'REASON: WRONGLY CLASSIFIED Contains two carboxylic acid groups '
               'with a hydroxy group on the alpha carbon\n'
               ' * SMILES: '
               '[H][C@@]1(O[C@@](C[C@@H](O)[C@H]1O)(OC[C@@H](OC)[C@@]1([H])O[C@](O)(C[C@@H](O)[C@H]1O)C(O)=O)C(O)=O)[C@H](O)CO '
               'NAME: alpha-Kdo-(2->8)-alpha-7-O-Me-Kdo REASON: WRONGLY '
               'CLASSIFIED Contains two carboxylic acid groups with a hydroxy '
               'group on the alpha carbon\n'
               ' * SMILES: O[C@](CC(O)=O)(CO)C(O)=O NAME: Itatartaric acid '
               'REASON: WRONGLY CLASSIFIED Contains two carboxylic acid groups '
               'with a hydroxy group on the alpha carbon\n'
               ' * SMILES: C[C@](O)(C[C@H](N)C(O)=O)C(O)=O NAME: '
               '(4S)-4-hydroxy-4-methyl-L-glutamic acid REASON: WRONGLY '
               'CLASSIFIED Contains two carboxylic acid groups with a hydroxy '
               'group on the alpha carbon\n'
               ' * SMILES: S1C(CSC(C1)(O)C(O)=O)(C(O)=O)O NAME: sulfanegen '
               'REASON: WRONGLY CLASSIFIED Contains two carboxylic acid groups '
               'with a hydroxy group on the alpha carbon\n'
               ' * SMILES: '
               '[H][C@@]1(O[C@](O)(C[C@@H](O)[C@H]1O)C(O)=O)[C@H](O)CO[C@@]1(C[C@@H](O)[C@@H](O)[C@]([H])(O1)[C@H](O)CO)C(O)=O '
               'NAME: alpha-Kdo-(2->8)-alpha-Kdo REASON: WRONGLY CLASSIFIED '
               'Contains two carboxylic acid groups with a hydroxy group on '
               'the alpha carbon\n'
               ' * SMILES: OC(CC(O)C(O)=O)(C)C(O)=O NAME: '
               '2-methyl-2,4-dihydroxyglutarate REASON: WRONGLY CLASSIFIED '
               'Contains two carboxylic acid groups with a hydroxy group on '
               'the alpha carbon\n'
               ' * SMILES: '
               '[C@@]1(O[C@]([C@@H]([C@H](C1)O)NC(C)=O)([C@@H]([C@@H](CO)O)O)[H])(C(=O)O)OC[C@H]([C@H]([C@@]2(O[C@](C[C@H](O)[C@H]2NC(C)=O)(C(=O)O)O)[H])O)O '
               'NAME: alpha-D-NeuNAc-(2->9)-alpha-D-NeuNAc REASON: WRONGLY '
               'CLASSIFIED Contains two carboxylic acid groups with a hydroxy '
               'group on the alpha carbon\n'
               ' * SMILES: '
               'O1[C@H]([C@H](NC(=O)C)[C@@H](O)C[C@]1(OC[C@@H](O)[C@@H](O)[C@@H]2OC(O)(C[C@H](O)[C@H]2NC(=O)C)C(O)=O)C(O)=O)[C@H](O)[C@H](O)CO '
               'NAME: '
               '(4S,5R,6R)-5-Acetamido-6-[(1R,2R)-3-[(2R,4S,5R,6R)-5-acetamido-2-carboxy-4-hydroxy-6-[(1R,2R)-1,2,3-trihydroxypropyl]oxan-2-yl]oxy-1,2-dihydroxypropyl]-2,4-dihydroxyoxane-2-carboxylic '
               'acid REASON: WRONGLY CLASSIFIED Contains two carboxylic acid '
               'groups with a hydroxy group on the alpha carbon\n'
               'False negatives: SMILES: O[C@@H](CCC(O)=O)C(O)=O NAME: '
               '(S)-2-hydroxyglutaric acid REASON: MISSED No alpha-hydroxy '
               'carboxylic acid group found\n'
               ' * SMILES: OC(CCCCCC(O)=O)C(O)=O NAME: 2-hydroxyoctanedioic '
               'acid REASON: MISSED No alpha-hydroxy carboxylic acid group '
               'found\n'
               ' * SMILES: O[C@H](CC(O)=O)C(O)=O NAME: (R)-malic acid REASON: '
               'MISSED No alpha-hydroxy carboxylic acid group found\n'
               ' * SMILES: OC(=O)\\C=C/C=C(/O)C(O)=O NAME: '
               '(2E,4Z)-2-hydroxymuconic acid REASON: MISSED No alpha-hydroxy '
               'carboxylic acid group found\n'
               ' * SMILES: C(C(CP(O)=O)C(O)=O)(C(O)=O)O NAME: '
               'phosphinomethylisomalic acid REASON: MISSED No alpha-hydroxy '
               'carboxylic acid group found\n'
               ' * SMILES: O[C@@H](CC(=O)C(O)=O)[C@@H](O)C(O)=O NAME: '
               '5-dehydro-4-deoxy-D-glucaric acid REASON: MISSED No '
               'alpha-hydroxy carboxylic acid group found\n'
               ' * SMILES: CC(C)([C@@H](O)C(O)=O)C(O)=O NAME: '
               '(R)-3,3-dimethylmalic acid REASON: MISSED No alpha-hydroxy '
               'carboxylic acid group found\n'
               ' * SMILES: O[C@@H](CC(O)=O)C(O)=O NAME: (S)-malic acid REASON: '
               'MISSED No alpha-hydroxy carboxylic acid group found\n'
               ' * SMILES: CC(C)C(C(O)C(O)=O)C(O)=O NAME: 3-isopropylmalic '
               'acid REASON: MISSED No alpha-hydroxy carboxylic acid group '
               'found\n'
               ' * SMILES: OC(CCC(O)=O)C(O)=O NAME: 2-hydroxyglutaric acid '
               'REASON: MISSED No alpha-hydroxy carboxylic acid group found\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'C1C=C(N=C2N1NN=N2)C3=CC=CC=C3',
                                     'name': '5-phenyl-1,7-dihydrotetrazolo[1,5-a]pyrimidine',
                                     'reason': 'Found 0 carboxylic acid '
                                               'groups, need exactly 2'},
                                 {   'smiles': 'O(C(=O)CCCCCCCCCCC/C=C\\CCCCCCCC)[C@H](COC(=O)CCCCCCCCC/C=C\\CCCCCC)COC(=O)CCCCCCC/C=C\\CCCC',
                                     'name': 'TG(14:1(9Z)/22:1(13Z)/18:1(11Z))',
                                     'reason': 'Found 0 carboxylic acid '
                                               'groups, need exactly 2'},
                                 {   'smiles': 'CC(=O)N[C@H]1[C@H](O)O[C@H](CO)[C@@H](O[C@@H]2O[C@H](CO)[C@@H](O[C@@H]3O[C@H](CO[C@H]4O[C@H](CO[C@H]5O[C@H](CO)[C@@H](O)[C@H](O)[C@@H]5O)[C@@H](O)[C@H](O[C@H]5O[C@H](CO)[C@@H](O)[C@H](O)[C@@H]5O)[C@@H]4O)[C@@H](O)[C@H](O[C@H]4O[C@H](CO)[C@@H](O)[C@H](O)[C@@H]4O[C@@H]4O[C@H](CO)[C@@H](O)[C@H](O)[C@H]4NC(C)=O)[C@@H]3O)[C@H](O)[C@H]2NC(C)=O)[C@@H]1O',
                                     'name': 'beta-D-GlcpNAc-(1->2)-alpha-D-Manp-(1->3)-{alpha-D-Manp-(1->3)-[alpha-D-Manp-(1->6)]-alpha-D-Manp-(1->6)}-beta-D-Manp-(1->4)-beta-GlcpNAc-(1->4)-beta-D-GlcpNAc',
                                     'reason': 'Found 0 carboxylic acid '
                                               'groups, need exactly 2'},
                                 {   'smiles': '[C@@]12([C@@]([C@]([C@@H](CC1)C)(CCC(CC)C)C)(CCC[C@@H]2C)[H])C',
                                     'name': 'clerodane',
                                     'reason': 'Found 0 carboxylic acid '
                                               'groups, need exactly 2'},
                                 {   'smiles': 'S(O[C@@H]1[C@H](O)[C@@H](O)[C@H](O[C@@H]([C@@H](O)[C@H](O)CO[C@]2(O[C@H]([C@H](NC(=O)C)[C@@H](O)C2)[C@H](O)[C@H](O)CO)C(O)=O)[C@@H](NC(=O)C)CO)O[C@@H]1CO)(O)(=O)=O',
                                     'name': '(2R,4S,5R,6R)-5-Acetamido-2-[(2R,3S,4R,5S)-5-acetamido-4-[(2R,3R,4R,5R,6R)-3,4-dihydroxy-6-(hydroxymethyl)-5-sulfooxyoxan-2-yl]oxy-2,3,6-trihydroxyhexoxy]-4-hydroxy-6-[(1R,2R)-1,2,3-trihydroxypropyl]oxane-2-carboxylic '
                                             'acid',
                                     'reason': 'Found 1 carboxylic acid '
                                               'groups, need exactly 2'},
                                 {   'smiles': 'O=C(NC(CC(C)C)C(=O)N[C@@H](CCCN=C(N)N)C=O)C(NC(=O)CC)CC(C)C',
                                     'name': 'Leupeptin Pr-LL',
                                     'reason': 'Found 0 carboxylic acid '
                                               'groups, need exactly 2'},
                                 {   'smiles': 'COC1=CC=C(C=C1)CCNC(=O)C(=C2C3=CC=CC=C3C(=N2)NC(=O)C4=CC=CS4)C#N',
                                     'name': 'N-[3-[1-cyano-2-[2-(4-methoxyphenyl)ethylamino]-2-oxoethylidene]-1-isoindolyl]-2-thiophenecarboxamide',
                                     'reason': 'Found 0 carboxylic acid '
                                               'groups, need exactly 2'},
                                 {   'smiles': 'O=C1O[C@@H](CC=2C1=C(OC)C(O)=CC2)CCC[C@@H](O)C',
                                     'name': 'Penicimarin C',
                                     'reason': 'Found 0 carboxylic acid '
                                               'groups, need exactly 2'},
                                 {   'smiles': 'CO[C@@H]1[C@@H]2[C@@H](C[C@@H]3[C@@](O2)([C@H]([C@@H]([C@H](O3)C(=O)OC)O)O)O)OC1N4C=NC5=C4N=CN=C5N',
                                     'name': 'LSM-4497',
                                     'reason': 'Found 0 carboxylic acid '
                                               'groups, need exactly 2'},
                                 {   'smiles': 'C[C@@H]1[C@H](O)CCC2=CC[C@H](C[C@]12C)C(C)=C',
                                     'name': '1-deoxycapsidiol',
                                     'reason': 'Found 0 carboxylic acid '
                                               'groups, need exactly 2'}],
    'sample_false_negatives': [   {   'smiles': 'C(C(CP(O)=O)C(O)=O)(C(O)=O)O',
                                      'name': 'phosphinomethylisomalic acid',
                                      'reason': 'Must have exactly 5 oxygen '
                                                'atoms'},
                                  {   'smiles': 'O[C@@H](CC(=O)C(O)=O)[C@@H](O)C(O)=O',
                                      'name': '5-dehydro-4-deoxy-D-glucaric '
                                              'acid',
                                      'reason': 'Must have exactly 5 oxygen '
                                                'atoms'},
                                  {   'smiles': 'C(C(CP(=O)(O)[H])(C(O)=O)O)C(O)=O',
                                      'name': '2-phosphinomethylmalic acid',
                                      'reason': 'Must have exactly 5 oxygen '
                                                'atoms'},
                                  {   'smiles': 'CSCCCC(O)(CC(O)=O)C(O)=O',
                                      'name': '2-(3-methylthiopropyl)malic '
                                              'acid',
                                      'reason': 'Contains elements other than '
                                                'C, H, and O'},
                                  {   'smiles': 'OC(=O)C(\\O)=C(/O)C(O)=O',
                                      'name': 'dihydroxyfumaric acid',
                                      'reason': 'Must have exactly 5 oxygen '
                                                'atoms'},
                                  {   'smiles': 'C(C(C(O)=O)O)(CCSC)C(=O)O',
                                      'name': '3-(2-methylthioethyl)malic acid',
                                      'reason': 'Contains elements other than '
                                                'C, H, and O'},
                                  {   'smiles': 'OC(C(C1CC1=C)C(O)=O)C(O)=O',
                                      'name': '2-hydroxy-3-(2-methylidenecyclopropyl)butanedioic '
                                              'acid',
                                      'reason': 'Contains rings - most '
                                                '2-hydroxydicarboxylic acids '
                                                'are acyclic'}],
    'attempt': 1,
    'reasoning': 'Let me analyze the issues with the previous code and suggest '
                 'improvements:\n'
                 '\n'
                 '1. Main Issues Identified:\n'
                 '- High false positive rate: The code incorrectly classified '
                 'many complex molecules containing carboxylic acid and '
                 'hydroxyl groups\n'
                 '- High false negative rate: Missed many valid '
                 '2-hydroxydicarboxylic acids\n'
                 '- The SMARTS pattern for alpha-hydroxy acid was too '
                 'restrictive, requiring explicit hydrogens\n'
                 '\n'
                 '2. Key Improvements Needed:\n'
                 '- Simplify the SMARTS pattern for alpha-hydroxy carboxylic '
                 'acid detection\n'
                 '- Better handle different bond types (single/double bonds)\n'
                 '- Ensure the hydroxy group is properly positioned relative '
                 'to the carboxyl group\n'
                 '- Add checks to exclude more complex structures\n'
                 '\n'
                 "Here's the improved code:",
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 18,
    'num_false_positives': 18,
    'num_true_negatives': 142257,
    'num_false_negatives': 7,
    'num_negatives': None,
    'precision': 0.5,
    'recall': 0.72,
    'f1': 0.5901639344262295,
    'accuracy': 0.9998243148278285,
    'negative_predictive_value': 0.999950795703762}