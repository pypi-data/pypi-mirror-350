"""
Classifies: CHEBI:36092 clavulone
"""
"""
Classifies: clavulone
Definition: A class of esterified prostanoids obtained from marine corals.
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_clavulone(smiles: str):
    """
    Determines if a molecule is a clavulone based on its SMILES string.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a clavulone, False otherwise
        str: Reason for classification
    """
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Core cyclopentenone patterns
    # More flexible patterns to catch different substitution variants
    core_patterns = [
        # Basic cyclopentenone core with various substitutions
        Chem.MolFromSmarts("[#6]1[#6](=[O])[#6]=[#6][#6]1"),
        # Halogenated variant
        Chem.MolFromSmarts("[Cl,Br,I][#6]1[#6](=[O])[#6][#6][#6]1"),
        # Conjugated variant
        Chem.MolFromSmarts("[#6]1[#6](=[O])[#6](=[#6])[#6][#6]1")
    ]
    
    # Check for at least one core pattern
    core_found = False
    for pattern in core_patterns:
        if pattern is not None and mol.HasSubstructMatch(pattern):
            core_found = True
            break
    
    if not core_found:
        return False, "Missing cyclopentenone core structure"

    # Side chain patterns
    side_chain_patterns = [
        # Unsaturated aliphatic chain
        Chem.MolFromSmarts("C/C=C/CC"),
        # Ester-containing chain
        Chem.MolFromSmarts("CC(=O)OC"),
        # Conjugated unsaturated chain
        Chem.MolFromSmarts("C=CC=C"),
        # Acetoxy group
        Chem.MolFromSmarts("OC(=O)C")
    ]
    
    # Count matching side chain features
    side_chain_count = 0
    for pattern in side_chain_patterns:
        if pattern is not None and mol.HasSubstructMatch(pattern):
            side_chain_count += 1
    
    if side_chain_count < 2:
        return False, "Insufficient characteristic side chain features"

    # Count key atoms and features
    c_count = sum(1 for atom in mol.GetAtoms() if atom.GetAtomicNum() == 6)
    o_count = sum(1 for atom in mol.GetAtoms() if atom.GetAtomicNum() == 8)
    hal_count = sum(1 for atom in mol.GetAtoms() if atom.GetAtomicNum() in [9,17,35,53])
    ring_count = len(Chem.GetSymmSSSR(mol))
    
    # Basic requirements
    if not (15 <= c_count <= 35):
        return False, "Carbon count outside typical range for clavulones"
    
    if o_count < 2:
        return False, "Insufficient oxygen content"
        
    if ring_count != 1:
        return False, "Must contain exactly one ring"
        
    # Check for required functional groups
    ester_pattern = Chem.MolFromSmarts("C(=O)O[#6]")
    if ester_pattern is not None:
        ester_count = len(mol.GetSubstructMatches(ester_pattern))
        if ester_count < 1:
            return False, "Missing required ester group"

    # Additional check for conjugated system
    conjugated_pattern = Chem.MolFromSmarts("C=CC=C")
    if conjugated_pattern is not None and not mol.HasSubstructMatch(conjugated_pattern):
        return False, "Missing conjugated system"

    # Must have either halogen or multiple oxygen-containing groups
    if hal_count == 0 and o_count < 4:
        return False, "Insufficient characteristic substituents"

    return True, "Contains characteristic clavulone structural features including cyclopentenone core and required substitution patterns"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:36092',
                          'name': 'clavulone',
                          'definition': 'A class of esterified prostanoids '
                                        'obtained from marine corals.',
                          'parents': ['CHEBI:26347'],
                          'xrefs': ['LIPID_MAPS_class:LMFA0312'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': None,
    'message': '\n'
               'Attempt failed: F1 score of 0 is too low.\n'
               'Outcomes:\n'
               '------\n'
               '\n'
               'True positives: NONE\n'
               'False positives: NONE\n'
               'False negatives: SMILES: '
               'ClC1=C[C@@](O)([C@@]([C@@H](OC(=O)C)/C=C\\CCCC(OC)=O)(C1=O)[H])C/C=C\\CCCCC '
               'NAME: punaglandin 8 REASON: MISSED Missing characteristic '
               'clavulone core structure\n'
               ' * SMILES: '
               'ClC=1C(=O)[C@@H]([C@@](O)(C/C=C\\CCCCC)C1)C[C@H](OC(=O)C)[C@@H](OC(=O)C)CCCC(OC)=O '
               'NAME: punaglandin 6 REASON: MISSED Missing characteristic '
               'clavulone core structure\n'
               ' * SMILES: '
               'O=C1/C(=C\\C=C\\[C@H](OC(=O)C)CCC(=O)OC)/[C@](OC(=O)C)(C/C=C\\CCCCCOC(=O)C)C=C1 '
               'NAME: 20-acetoxy-claviridenone B REASON: MISSED Missing '
               'characteristic clavulone core structure\n'
               ' * SMILES: '
               'CCCCC\\C=C/C[C@]1(OC(C)=O)C=CC(=O)/C1=C/C=C/[C@@H](CCC(=O)OC)OC(C)=O '
               'NAME: clavulone II REASON: MISSED Missing characteristic '
               'clavulone core structure\n'
               ' * SMILES: '
               'CCCCC\\C=C/C[C@]1(OC(C)=O)C=CC(=O)\\C1=C\\C=C/[C@@H](CCC(=O)OC)OC(C)=O '
               'NAME: clavulone I REASON: MISSED Missing characteristic '
               'clavulone core structure\n'
               ' * SMILES: '
               'ClC1=C[C@@](O)(/C(=C/[C@H](OC(=O)C)[C@@H](OC(=O)C)CCCC(OC)=O)/C1=O)C/C=C\\CCCCC '
               'NAME: 7Z-punaglandin 4 REASON: MISSED Missing characteristic '
               'clavulone core structure\n'
               ' * SMILES: '
               'ClC1=C[C@](O)(C/C=C\\CCCCC)\\C(\\C1=O)=C/C=C\\CCCC(OC)=O NAME: '
               'chlorovulone I REASON: MISSED Missing characteristic clavulone '
               'core structure\n'
               ' * SMILES: '
               'Cl[C@]12O[C@H]1[C@@](O)(/C(/C2=O)=C\\C=C/CCCC(OC)=O)C/C=C\\CCCCC '
               'NAME: 10,11-Epoxy-chlorovulone I REASON: MISSED Missing '
               'characteristic clavulone core structure\n'
               ' * SMILES: O([C@]1(C/C=C\\CCCCC)/C(/C(=O)C=C1)=C\\C=O)C(=O)C '
               'NAME: Clavirin II REASON: MISSED Missing characteristic '
               'clavulone core structure\n'
               ' * SMILES: '
               'BrC1=C[C@@](O)([C@@]([C@@H](OC(=O)C)/C=C/CCCC(OC)=O)(C1=O)[H])C/C=C\\CCCCC '
               'NAME: 7-Acetoxy-7,8-dihydrobromovulone II REASON: MISSED '
               'Missing characteristic clavulone core structure\n'
               '------\n'
               '\n'
               'In your reasoning step, analyze the previous program and the '
               'above outcomes, hypothesizing about what went wrong, and how '
               'to improve.\n',
    'sample_true_negatives': [   {   'smiles': 'C1=CC=CC(=C1)CC[C@H](N[C@H](C(N2C(N(C[C@H]2C(O)=O)C)=O)=O)C)C(=O)O',
                                     'name': 'imidaprilat',
                                     'reason': 'Missing cyclopentenone core '
                                               'structure'},
                                 {   'smiles': 'C[C@H]1CN(C(=O)CCCN2C=C(CO[C@H]1CN(C)CC3=CC(=CC=C3)O)N=N2)[C@@H](C)CO',
                                     'name': '(8S,9R)-9-[[(3-hydroxyphenyl)methyl-methylamino]methyl]-6-[(2S)-1-hydroxypropan-2-yl]-8-methyl-10-oxa-1,6,13,14-tetrazabicyclo[10.2.1]pentadeca-12(15),13-dien-5-one',
                                     'reason': 'Missing cyclopentenone core '
                                               'structure'},
                                 {   'smiles': 'ClC1=C2C(C3=C(C(=O)CC)C(O[C@@]3(C1=O)C)=O)=CN(CC=C(C)C)C(=C2)/C=C/[C@H](CC)C',
                                     'name': '4′,5′-dinor-5′-deoxy-N-(3-methyl-2-butenyl)-2-aza-2-deoxychaetoviridin '
                                             'A',
                                     'reason': 'Missing cyclopentenone core '
                                               'structure'},
                                 {   'smiles': 'O1[C@@H](O[C@H]2[C@@H](O)[C@H](O[C@H](O)[C@@H]2O)CO)[C@H](NC(=O)C)[C@@H](O[C@@H]3O[C@@H]([C@H](O)[C@H](O)[C@H]3O)CO)[C@H](O)[C@H]1CO',
                                     'name': 'Lacto-N-triose I',
                                     'reason': 'Missing cyclopentenone core '
                                               'structure'},
                                 {   'smiles': 'O=C1OCC(=C1/C=C\\C)CC[C@]2(OC(=O)[C@@H](C2)O)C',
                                     'name': 'Pezizolide D',
                                     'reason': 'Missing cyclopentenone core '
                                               'structure'},
                                 {   'smiles': 'C[C@H]1CN(C(=O)C2=C(N=CC(=C2)C3=CCCCC3)O[C@H]1CN(C)S(=O)(=O)C4=CN(C=N4)C)[C@H](C)CO',
                                     'name': 'N-[[(2R,3S)-8-(1-cyclohexenyl)-5-[(2R)-1-hydroxypropan-2-yl]-3-methyl-6-oxo-3,4-dihydro-2H-pyrido[2,3-b][1,5]oxazocin-2-yl]methyl]-N,1-dimethyl-4-imidazolesulfonamide',
                                     'reason': 'Missing cyclopentenone core '
                                               'structure'},
                                 {   'smiles': '[H][C@]1(O[C@](O)(C[C@H](O)[C@H]1NC(=O)CC)C(O)=O)[C@H](O)[C@@H](CO)O[C@@]1(C[C@H](O)[C@@H](NC(=O)CC)[C@@]([H])(O1)[C@H](O)[C@@H](CO)O[C@@]1(C[C@H](O)[C@@H](NC(=O)CC)[C@@]([H])(O1)[C@H](O)[C@@H](CO)O[C@@]1(C[C@H](O)[C@@H](NC(=O)CC)[C@@]([H])(O1)[C@H](O)[C@@H](CO)O[C@@]1(C[C@H](O)[C@@H](NC(=O)CC)[C@@]([H])(O1)[C@H](O)[C@@H](CO)O[C@@]1(C[C@H](O)[C@@H](NC(=O)CC)[C@@]([H])(O1)[C@H](O)[C@@H](CO)O[C@@]1(C[C@H](O)[C@@H](NC(=O)CC)[C@@]([H])(O1)[C@H](O)[C@@H](CO)O[C@@]1(C[C@H](O)[C@@H](NC(=O)CC)[C@@]([H])(O1)[C@H](O)[C@@H](CO)O[C@@]1(C[C@H](O)[C@@H](NC(=O)CC)[C@@]([H])(O1)[C@H](O)[C@@H](CO)O[C@@]1(C[C@H](O)[C@@H](NC(=O)CC)[C@@]([H])(O1)[C@H](O)[C@H](O)CO)C(O)=O)C(O)=O)C(O)=O)C(O)=O)C(O)=O)C(O)=O)C(O)=O)C(O)=O)C(O)=O',
                                     'name': '[8)-alpha-Neu5Pr-(2->]10',
                                     'reason': 'Missing cyclopentenone core '
                                               'structure'},
                                 {   'smiles': 'O=C1C2=C(OC[C@@]1(O)C3=CC=C(O)C=C3)C=C(O)C=C2O',
                                     'name': 'Dothideoisoflavanone',
                                     'reason': 'Missing cyclopentenone core '
                                               'structure'},
                                 {   'smiles': 'O([C@H]1[C@@H]([C@H](O)[C@@H]([C@@H](O)[C@@H](C)C=CC=C(C(=O)NC2=C3OC4=CC(N5CCN(CC5)CC(C)C)=CC(=O)C4=NC3=C6C7=C(O)[C@@](OC=C[C@H](OC)[C@H]1C)(OC7=C(C(O)=C6C2=O)C)C)C)C)C)C(=O)C',
                                     'name': 'Rifalazil',
                                     'reason': 'Missing cyclopentenone core '
                                               'structure'},
                                 {   'smiles': 'C1CN(CCN1C2=C3C=CC=NC3=C(C=C2)[N+](=O)[O-])C(=O)C4=CC=C(C=C4)Cl',
                                     'name': '(4-chlorophenyl)-[4-(8-nitro-5-quinolinyl)-1-piperazinyl]methanone',
                                     'reason': 'Missing cyclopentenone core '
                                               'structure'}],
    'sample_false_negatives': [   {   'smiles': 'ClC1=C[C@@](O)([C@@]([C@@H](OC(=O)C)/C=C\\CCCC(OC)=O)(C1=O)[H])C/C=C\\CCCCC',
                                      'name': 'punaglandin 8',
                                      'reason': 'Missing conjugated system'},
                                  {   'smiles': 'ClC=1C(=O)[C@@H]([C@@](O)(C/C=C\\CCCCC)C1)C[C@H](OC(=O)C)[C@@H](OC(=O)C)CCCC(OC)=O',
                                      'name': 'punaglandin 6',
                                      'reason': 'Missing conjugated system'},
                                  {   'smiles': 'ClC1=C[C@@](O)(/C(=C/[C@H](OC(=O)C)[C@@H](OC(=O)C)CCCC(OC)=O)/C1=O)C/C=C\\CCCCC',
                                      'name': '7Z-punaglandin 4',
                                      'reason': 'Missing conjugated system'},
                                  {   'smiles': 'Cl[C@]12O[C@H]1[C@@](O)(/C(/C2=O)=C\\C=C/CCCC(OC)=O)C/C=C\\CCCCC',
                                      'name': '10,11-Epoxy-chlorovulone I',
                                      'reason': 'Must contain exactly one '
                                                'ring'},
                                  {   'smiles': 'O([C@]1(C/C=C\\CCCCC)/C(/C(=O)C=C1)=C\\C=O)C(=O)C',
                                      'name': 'Clavirin II',
                                      'reason': 'Missing conjugated system'},
                                  {   'smiles': 'BrC1=C[C@@](O)([C@@]([C@@H](OC(=O)C)/C=C/CCCC(OC)=O)(C1=O)[H])C/C=C\\CCCCC',
                                      'name': '7-Acetoxy-7,8-dihydrobromovulone '
                                              'II',
                                      'reason': 'Missing conjugated system'},
                                  {   'smiles': 'ClC=1C(=O)[C@@]([C@@](O)(C/C=C\\C/C=C\\CC)C1)([C@@H](OC(=O)C)/C=C\\CCCC(OC)=O)[H]',
                                      'name': 'punaglandin 7',
                                      'reason': 'Missing conjugated system'},
                                  {   'smiles': 'ClC1=C[C@@](O)(/C(=C\\[C@H](OC(=O)C)[C@@H](OC(=O)C)CCCC(OC)=O)/C1=O)C/C=C\\CCCCC',
                                      'name': 'punaglandin 4',
                                      'reason': 'Missing conjugated system'},
                                  {   'smiles': '[C@]1(/C(/C(C=C1)=O)=C/C(=O)[H])(C/C=C\\CCCCC)OC(C)=O',
                                      'name': 'clavirin I',
                                      'reason': 'Missing conjugated system'},
                                  {   'smiles': 'ClC1=C[C@@](O)(/C(=C/[C@H](OC(=O)C)[C@@H](OC(=O)C)CCCC(OC)=O)/C1=O)C/C=C\\C/C=C\\CC',
                                      'name': '7Z-punaglandin 3',
                                      'reason': 'Missing conjugated system'}],
    'attempt': 3,
    'reasoning': 'Let me analyze the previous attempt and suggest '
                 'improvements:\n'
                 '\n'
                 '1. Core Structure Analysis:\n'
                 '- The previous SMARTS patterns for the core structure were '
                 "too restrictive and didn't capture all variations\n"
                 '- Looking at the examples, clavulones have a cyclopentenone '
                 'core with various substitution patterns\n'
                 '- Some have direct halogen substitution, others have acetoxy '
                 'groups\n'
                 '- The core is often conjugated with unsaturated side chains\n'
                 '\n'
                 '2. Side Chain Patterns:\n'
                 "- The side chain patterns were too simple and didn't capture "
                 'the full range\n'
                 '- Most examples have a long aliphatic chain (often with '
                 'unsaturation)\n'
                 '- Many have ester-containing side chains\n'
                 '- The stereochemistry of double bonds is important (many E/Z '
                 'configurations)\n'
                 '\n'
                 '3. Key Improvements Needed:\n'
                 '- More flexible core pattern matching\n'
                 '- Better handling of stereochemistry\n'
                 '- More comprehensive side chain patterns\n'
                 '- Better accounting for various substitution patterns\n'
                 '- Recognition of both halogenated and non-halogenated '
                 'variants\n'
                 '\n'
                 "Here's my improved code:",
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 9,
    'num_false_positives': 3,
    'num_true_negatives': 142269,
    'num_false_negatives': 19,
    'num_negatives': None,
    'precision': 0.75,
    'recall': 0.32142857142857145,
    'f1': 0.45000000000000007,
    'accuracy': 0.9998453970484891,
    'negative_predictive_value': 0.9998664680085461}