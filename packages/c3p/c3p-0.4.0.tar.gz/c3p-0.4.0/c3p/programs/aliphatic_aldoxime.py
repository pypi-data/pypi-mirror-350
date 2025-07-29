"""
Classifies: CHEBI:82744 aliphatic aldoxime
"""
"""
Classifies: aliphatic aldoxime
Definition: Any aldoxime derived from an aliphatic aldehyde
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_aliphatic_aldoxime(smiles: str):
    """
    Determines if a molecule is an aliphatic aldoxime based on its SMILES string.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is an aliphatic aldoxime, False otherwise
        str: Reason for classification
    """
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # First check for aldoxime group pattern [H]C=NOH
    # More specific SMARTS pattern for aldoxime
    aldoxime_pattern = Chem.MolFromSmarts("[CH1](=N[OH1])-[!$(C=O);!$(C=N);!$(C=C);!$([N+]=[O-])]")
    
    if not mol.HasSubstructMatch(aldoxime_pattern):
        return False, "No proper aldoxime group (HC=NOH) found"

    # Get matches for the aldoxime group
    matches = mol.GetSubstructMatches(aldoxime_pattern)
    
    # Check each potential aldoxime group
    for match in matches:
        c_atom = mol.GetAtomWithIdx(match[0])
        n_atom = mol.GetAtomWithIdx(match[1])
        o_atom = mol.GetAtomWithIdx(match[2])
        
        # Verify hybridization
        if c_atom.GetHybridization() != Chem.HybridizationType.SP2:
            return False, "Carbon in C=N must be sp2 hybridized"
        
        # Check that carbon has exactly one hydrogen
        if c_atom.GetTotalNumHs() != 1:
            return False, "Carbon must have exactly one hydrogen (aldoxime)"
        
        # Check formal charges
        if c_atom.GetFormalCharge() != 0 or n_atom.GetFormalCharge() != 0:
            return False, "Unexpected formal charges on C or N atoms"
            
        # Check for aci-nitro compounds
        aci_nitro = Chem.MolFromSmarts("[O-][N+](=C)O")
        if mol.HasSubstructMatch(aci_nitro):
            return False, "Compound is an aci-nitro compound, not an aldoxime"

    # Check for aromatic or conjugated systems
    conjugated_patterns = [
        Chem.MolFromSmarts("C=C-C=N"), # conjugated alkene
        Chem.MolFromSmarts("C=C-N=C"), # conjugated imine
        Chem.MolFromSmarts("O=C-C=N"), # conjugated carbonyl
        Chem.MolFromSmarts("n1ccccc1"), # pyridine
        Chem.MolFromSmarts("c1ccccc1")  # benzene
    ]
    
    for pattern in conjugated_patterns:
        if pattern is not None and mol.HasSubstructMatch(pattern):
            return False, "Contains conjugated or aromatic system"

    # Check that carbon attached to C=N is sp3 (aliphatic)
    for match in matches:
        neighbors = mol.GetAtomWithIdx(match[0]).GetNeighbors()
        for neighbor in neighbors:
            if neighbor.GetIdx() not in [match[1]]:  # exclude the N atom
                if neighbor.GetHybridization() != Chem.HybridizationType.SP3:
                    return False, "Carbon chain must be aliphatic"

    return True, "Contains aliphatic aldoxime group (HC=NOH)"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:82744',
                          'name': 'aliphatic aldoxime',
                          'definition': 'Any aldoxime derived from an '
                                        'aliphatic aldehyde.',
                          'parents': ['CHEBI:22307'],
                          'xrefs': ['MetaCyc:Aliphatic-Aldoximes'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': None,
    'message': '\n'
               'Attempt failed: F1 score of 0.7931034482758621 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: SMILES: [H]C(C)=NO NAME: acetaldehyde oxime '
               'REASON: CORRECT Contains aliphatic aldoxime group (HC=NOH)\n'
               ' * SMILES: C(\\CCCCCCCSC)=N/O NAME: '
               '(E)-8-(methylsulfanyl)octanal oxime REASON: CORRECT Contains '
               'aliphatic aldoxime group (HC=NOH)\n'
               ' * SMILES: C(CCCCSC)=NO NAME: 5-(methylsulfanyl)pentanal oxime '
               'REASON: CORRECT Contains aliphatic aldoxime group (HC=NOH)\n'
               ' * SMILES: [H]\\C(=N\\O)C(C)CC NAME: (Z)-2-methylbutanal oxime '
               'REASON: CORRECT Contains aliphatic aldoxime group (HC=NOH)\n'
               ' * SMILES: OC(C(O)C(O)\\C=N\\O)C(O)CO NAME: '
               '(1E)-2,3,4,5,6-pentahydroxyhexanal oxime REASON: CORRECT '
               'Contains aliphatic aldoxime group (HC=NOH)\n'
               ' * SMILES: C(\\CCCCSC)=N/O NAME: '
               '(E)-5-(methylsulfanyl)pentanal oxime REASON: CORRECT Contains '
               'aliphatic aldoxime group (HC=NOH)\n'
               ' * SMILES: [H]C(=NO)C(C)(C)SC NAME: '
               '2-methyl-2-(methylsulfanyl)propanal oxime REASON: CORRECT '
               'Contains aliphatic aldoxime group (HC=NOH)\n'
               ' * SMILES: [H]\\C(C(C)C)=N\\O NAME: (Z)-2-methylpropanal oxime '
               'REASON: CORRECT Contains aliphatic aldoxime group (HC=NOH)\n'
               ' * SMILES: C(CCCSC)=NO NAME: 4-(methylsulfanyl)butanal oxime '
               'REASON: CORRECT Contains aliphatic aldoxime group (HC=NOH)\n'
               ' * SMILES: C(\\CCCCCCCCSC)=N/O NAME: '
               '(E)-9-(methylsulfanyl)nonanal oxime REASON: CORRECT Contains '
               'aliphatic aldoxime group (HC=NOH)\n'
               ' * SMILES: C(CCCCCCCSC)=NO NAME: 8-(methylsulfanyl)octanal '
               'oxime REASON: CORRECT Contains aliphatic aldoxime group '
               '(HC=NOH)\n'
               ' * SMILES: [H]C(=NO)C(C)CC NAME: 2-methylbutanal oxime REASON: '
               'CORRECT Contains aliphatic aldoxime group (HC=NOH)\n'
               ' * SMILES: [H]\\C(=N/O)C(C)CC NAME: (E)-2-methylbutanal oxime '
               'REASON: CORRECT Contains aliphatic aldoxime group (HC=NOH)\n'
               ' * SMILES: [H]\\C(C(C)C)=N/O NAME: (E)-2-methylpropanal oxime '
               'REASON: CORRECT Contains aliphatic aldoxime group (HC=NOH)\n'
               ' * SMILES: C(CCCCCSC)=NO NAME: 6-(methylsulfanyl)hexanal oxime '
               'REASON: CORRECT Contains aliphatic aldoxime group (HC=NOH)\n'
               ' * SMILES: [H]\\C(C)=N\\O NAME: (Z)-acetaldehyde oxime REASON: '
               'CORRECT Contains aliphatic aldoxime group (HC=NOH)\n'
               ' * SMILES: C([C@@H](/C(=N/O)/[H])C)C NAME: '
               '(1E,2S)-2-methylbutanal oxime REASON: CORRECT Contains '
               'aliphatic aldoxime group (HC=NOH)\n'
               ' * SMILES: '
               '[H]C(CCCCNC(=O)CCC(=O)N(O)CCCCCNC(=O)CCC(=O)N(O)CCCCCN)=NO '
               'NAME: IC202C REASON: CORRECT Contains aliphatic aldoxime group '
               '(HC=NOH)\n'
               ' * SMILES: [H]C(CCCCCCSC)=NO NAME: 7-(methylsulfanyl)heptanal '
               'oxime REASON: CORRECT Contains aliphatic aldoxime group '
               '(HC=NOH)\n'
               ' * SMILES: [H]C(CSC)=NO NAME: (methylsulfanyl)acetaldehyde '
               'oxime REASON: CORRECT Contains aliphatic aldoxime group '
               '(HC=NOH)\n'
               ' * SMILES: C(CCCCCCCCSC)=NO NAME: 9-(methylsulfanyl)nonanal '
               'oxime REASON: CORRECT Contains aliphatic aldoxime group '
               '(HC=NOH)\n'
               ' * SMILES: C([C@@H](/C(=N\\O)/[H])C)C NAME: '
               '(1Z,2S)-2-methylbutanal oxime REASON: CORRECT Contains '
               'aliphatic aldoxime group (HC=NOH)\n'
               ' * SMILES: C(\\CCCCCSC)=N/O NAME: '
               '(E)-6-(methylsulfanyl)hexanal oxime REASON: CORRECT Contains '
               'aliphatic aldoxime group (HC=NOH)\n'
               'False positives: SMILES: C(C([O-])=O)[C@H](C([O-])=O)SC=NO '
               'NAME: S-[(2R)-succino]-(hydroxyimino)methanethiol(2-) REASON: '
               'WRONGLY CLASSIFIED Contains aliphatic aldoxime group (HC=NOH)\n'
               ' * SMILES: O[N+]([O-])=CCC(=O)O NAME: 3-aci-nitropropanoic '
               'acid REASON: WRONGLY CLASSIFIED Contains aliphatic aldoxime '
               'group (HC=NOH)\n'
               ' * SMILES: O/N=C/C=1N(CC=CC1)C NAME: '
               '1-Methyl-1,6-dihydropyridine-2-carbaldoxime REASON: WRONGLY '
               'CLASSIFIED Contains aliphatic aldoxime group (HC=NOH)\n'
               ' * SMILES: O/N=C/C1=CC[C@@H](C(=C)C)CC1 NAME: Perillartine '
               'REASON: WRONGLY CLASSIFIED Contains aliphatic aldoxime group '
               '(HC=NOH)\n'
               ' * SMILES: C(C=NO)=NO NAME: glyoxime REASON: WRONGLY '
               'CLASSIFIED Contains aliphatic aldoxime group (HC=NOH)\n'
               ' * SMILES: C1CCCN(CC1)CCCCCC(=O)C=NO NAME: '
               '7-(1-azepanyl)-2-oxoheptanal oxime REASON: WRONGLY CLASSIFIED '
               'Contains aliphatic aldoxime group (HC=NOH)\n'
               ' * SMILES: ON=CCS[C@H](CC([O-])=O)C([O-])=O NAME: '
               '(2R)-S-succinyl-2-(hydroxyimino)ethanethiol(2-) REASON: '
               'WRONGLY CLASSIFIED Contains aliphatic aldoxime group (HC=NOH)\n'
               ' * SMILES: '
               'O=C1C=C2C=C[C@H](OC(=O)/C=C/C(=C/[C@H](CC)C)/C)[C@@H]([C@@]2(C)C[C@@]1(OC)C(/C=N/O)=C)C '
               'NAME: Dendryphiellin J REASON: WRONGLY CLASSIFIED Contains '
               'aliphatic aldoxime group (HC=NOH)\n'
               ' * SMILES: O=C(N/C=C/C(=O)N)/C=N\\O NAME: '
               '3-(oximinoacetamido)acrylamide REASON: WRONGLY CLASSIFIED '
               'Contains aliphatic aldoxime group (HC=NOH)\n'
               ' * SMILES: O[N+]([O-])=CCC(=O)[O-] NAME: 3-aci-nitropropanoate '
               'REASON: WRONGLY CLASSIFIED Contains aliphatic aldoxime group '
               '(HC=NOH)\n'
               ' * SMILES: CN1C=CCC=C1\\C=N\\O NAME: ProPAM REASON: WRONGLY '
               'CLASSIFIED Contains aliphatic aldoxime group (HC=NOH)\n'
               ' * SMILES: C\\C=[N+](\\O)[O-] NAME: aci-nitroethane REASON: '
               'WRONGLY CLASSIFIED Contains aliphatic aldoxime group (HC=NOH)\n'
               'False negatives: NONE\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'O=C(N[C@@H](CCCCN)C(O)=O)[C@@H](NC(=O)[C@@H](N)CC=1C=2C(NC1)=CC=CC2)CC=3NC=NC3',
                                     'name': 'Trp-His-Lys',
                                     'reason': 'No proper aldoxime group '
                                               '(HC=NOH) found'},
                                 {   'smiles': 'CSCCC(=O)C(=O)COP(O)(O)=O',
                                     'name': '5-(methylsulfanyl)-2,3-dioxopentyl '
                                             'phosphate',
                                     'reason': 'No proper aldoxime group '
                                               '(HC=NOH) found'},
                                 {   'smiles': 'C[C@@H]1O[C@@H](OCCCCCCCCCCCCCCCC[C@@H](O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]2O[C@H]([C@H](O)[C@@H]2OP([O-])([O-])=O)N3C=NC4=C(N)N=CN=C34)[C@H](O)C[C@H]1O',
                                     'name': 'bhos#34-CoA(4-)',
                                     'reason': 'No proper aldoxime group '
                                               '(HC=NOH) found'},
                                 {   'smiles': 'ClC1=C(OC)C=C(/C=C/[C@H](OC)/C(=C(\\C(=O)OC)/CO)/C)C=C1',
                                     'name': 'Oudemansinol B',
                                     'reason': 'No proper aldoxime group '
                                               '(HC=NOH) found'},
                                 {   'smiles': 'O=C1[C@@](O)([C@H]2[C@H]([C@@H](CO)CC2)[C@@H]3[C@H](C1)[C@]3(CO)C)C',
                                     'name': 'Inonotin G',
                                     'reason': 'No proper aldoxime group '
                                               '(HC=NOH) found'},
                                 {   'smiles': 'OC[C@@]1(O)OC[C@H](O)[C@@H](O)[C@@H]1O',
                                     'name': 'alpha-L-sorbopyranose',
                                     'reason': 'No proper aldoxime group '
                                               '(HC=NOH) found'},
                                 {   'smiles': 'CC\\C=C/C\\C=C/C\\C=C/C\\C=C/C\\C=C/C\\C=C/CCCCCC[C@@H](O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12',
                                     'name': '(3R,10Z,13Z,16Z,19Z,22Z,25Z)-3-hydroxyoctacosahexaenoyl-CoA',
                                     'reason': 'No proper aldoxime group '
                                               '(HC=NOH) found'},
                                 {   'smiles': 'S(CC[C@H](NC(=O)[C@@H](N)CCC(=O)N)C(=O)N[C@@H](CC1=CC=CC=C1)C(O)=O)C',
                                     'name': 'Gln-Met-Phe',
                                     'reason': 'No proper aldoxime group '
                                               '(HC=NOH) found'},
                                 {   'smiles': 'C[C@H]1CN([C@H](COC2=C(C=C(C=C2)NC(=O)C)C(=O)N(C[C@H]1OC)C)C)CCC3=CC=CC=C3',
                                     'name': 'N-[(4S,7S,8S)-8-methoxy-4,7,10-trimethyl-11-oxo-5-(2-phenylethyl)-2-oxa-5,10-diazabicyclo[10.4.0]hexadeca-1(12),13,15-trien-14-yl]acetamide',
                                     'reason': 'No proper aldoxime group '
                                               '(HC=NOH) found'},
                                 {   'smiles': 'CCCN1C[C@@H]([C@H](CN(C(=O)C2=C(C=CC(=C2)NC(=O)NC3=CC=CC=C3F)OC[C@H]1C)C)OC)C',
                                     'name': '1-(2-fluorophenyl)-3-[(4R,7S,8R)-8-methoxy-4,7,10-trimethyl-11-oxo-5-propyl-2-oxa-5,10-diazabicyclo[10.4.0]hexadeca-1(12),13,15-trien-14-yl]urea',
                                     'reason': 'No proper aldoxime group '
                                               '(HC=NOH) found'}],
    'sample_false_negatives': [],
    'attempt': 1,
    'reasoning': "Let's analyze the issues from the previous attempt:\n"
                 '\n'
                 '1. False Positives Analysis:\n'
                 '- Many of the false positives contain C=NO groups but are '
                 'not aliphatic aldoximes:\n'
                 '  - Some are aromatic (like ProPAM)\n'
                 '  - Some are aci-nitro compounds (like aci-nitroethane)\n'
                 '  - Some have the C=NO group conjugated with other '
                 'unsaturated systems\n'
                 '  - Some have multiple C=NO groups (like glyoxime)\n'
                 '\n'
                 '2. Main Issues in Previous Code:\n'
                 "- The aromatic check wasn't sufficient - molecules with "
                 'conjugated systems were still being accepted\n'
                 '- The SMARTS patterns were too permissive\n'
                 '- No check for aci-nitro compounds which can have similar '
                 'patterns\n'
                 '- No check for conjugation with other unsaturated systems\n'
                 '\n'
                 "Here's an improved version:",
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 23,
    'num_false_positives': 2,
    'num_true_negatives': 142275,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.92,
    'recall': 1.0,
    'f1': 0.9583333333333334,
    'accuracy': 0.9999859451862263,
    'negative_predictive_value': 1.0}