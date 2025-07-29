"""
Classifies: CHEBI:26004 phenylpropanoid
"""
from rdkit import Chem
from rdkit.Chem import rdMolDescriptors

def is_phenylpropanoid(smiles: str):
    """
    Determines if a molecule is a phenylpropanoid based on its SMILES string.
    Phenylpropanoids contain an aromatic ring connected to a propane chain or similar structures like flavonoids.
    
    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a phenylpropanoid, False otherwise
        str: Reason for classification
    """
    
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Look for aromatic ring
    aromatic_pattern = Chem.MolFromSmarts("c1ccccc1")  # Simple benzene ring pattern
    if not mol.HasSubstructMatch(aromatic_pattern):
        return False, "No aromatic benzene ring found"

    # Look for aliphatic three-carbon chain attached to the aromatic ring
    # The pattern may look for a chain like -C-C-C- attached to an aromatic carbon
    propane_chain_pattern = Chem.MolFromSmarts("c-C-C-C")
    if not mol.HasSubstructMatch(propane_chain_pattern):
        return False, "No phenylpropane backbone found"

    # Check for common functional groups in phenylpropanoids
    # Hydroxy (-OH), Methoxy (-OCH3), Carbonyl (=O) are common.
    functional_group_patterns = [
        Chem.MolFromSmarts("c-[OH]"),       # Phenolic OH group
        Chem.MolFromSmarts("c-CO"),         # Carbonyl
        Chem.MolFromSmarts("c-COC")         # Methoxy
    ]
    function_group_count = sum(1 for pattern in functional_group_patterns 
                               if mol.HasSubstructMatch(pattern))

    if function_group_count < 1:
        return False, "No common phenylpropanoid functional groups found"

    return True, "Structure contains aromatic ring with a phenylpropane backbone and functional groups common to phenylpropanoids."


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:26004',
                          'name': 'phenylpropanoid',
                          'definition': 'Any organic aromatic compound with a '
                                        'structure based on a phenylpropane '
                                        'skeleton. The class includes '
                                        'naturally occurring phenylpropanoid '
                                        'esters, flavonoids, anthocyanins, '
                                        'coumarins and many small phenolic '
                                        'molecules as well as their '
                                        'semi-synthetic and synthetic '
                                        'analogues. Phenylpropanoids are also '
                                        'precursors of lignin.',
                          'parents': ['CHEBI:33659'],
                          'xrefs': ['Wikipedia:Phenylpropanoid'],
                          'all_positive_examples': []},
    'config': None,
    'code_statistics': {   'lines_of_code': 34,
                           'log_lines_of_code': 3.5263605246161616,
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
                                                 1,
                                                 2,
                                                 0,
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
                                                 2,
                                                 2,
                                                 1,
                                                 1,
                                                 1,
                                                 0,
                                                 1,
                                                 2,
                                                 0,
                                                 1],
                           'max_indent': 2,
                           'imports': [   'from rdkit import Chem',
                                          'from rdkit.Chem import '
                                          'rdMolDescriptors'],
                           'imports_count': 2,
                           'methods_called': [   'HasSubstructMatch',
                                                 'MolFromSmarts',
                                                 'MolFromSmiles'],
                           'methods_called_count': 3,
                           'smarts_strings': [   'c-CO',
                                                 'c1ccccc1',
                                                 'c-COC',
                                                 'c-C-C-C',
                                                 'c-[OH]'],
                           'smarts_strings_count': 5,
                           'defs': ['is_phenylpropanoid(smiles: str):'],
                           'defs_count': 1,
                           'returns': [   'False, "Invalid SMILES string"',
                                          'False, "No aromatic benzene ring '
                                          'found"',
                                          'False, "No phenylpropane backbone '
                                          'found"',
                                          'False, "No common phenylpropanoid '
                                          'functional groups found"',
                                          'True, "Structure contains aromatic '
                                          'ring with a phenylpropane backbone '
                                          'and functional groups common to '
                                          'phenylpropanoids."'],
                           'returns_count': 5,
                           'complexity': 2.9052721049232324},
    'message': None,
    'sample_true_negatives': [   {   'smiles': 'O1C2C34C(C(N(CC3)C)CC5=C4C1=C(OC)C=C5)C=CC2OC',
                                     'name': '6-O-Methylcodeine',
                                     'reason': 'No common phenylpropanoid '
                                               'functional groups found'},
                                 {   'smiles': 'CN1C2=C(C=CC(=C2)OC)C3=C1[C@H](N(CC34CCN(CC4)S(=O)(=O)C5=CC=CS5)CC6CC6)CO',
                                     'name': "[(1S)-2-(cyclopropylmethyl)-7-methoxy-9-methyl-1'-thiophen-2-ylsulfonyl-1-spiro[1,3-dihydropyrido[3,4-b]indole-4,4'-piperidine]yl]methanol",
                                     'reason': 'No common phenylpropanoid '
                                               'functional groups found'},
                                 {   'smiles': 'O(C(=O)CCCCCCCCCCCCCCC)[C@@H](COC(=O)CCCCCCCCCCCCCCCCCCC)COC(=O)CCCCCCC',
                                     'name': 'TG(20:0/16:0/8:0)',
                                     'reason': 'No aromatic benzene ring '
                                               'found'},
                                 {   'smiles': 'O[C@@H]1CC2[C@](C3=C(C4=NCCC([C@@]4(C)CC3)[C@@H](CCC(C(C)C)C)C)CC2)(C)CC1',
                                     'name': 'UCA-1064-B',
                                     'reason': 'No aromatic benzene ring '
                                               'found'},
                                 {   'smiles': 'C1=CC=C(C=C1)N2C(=NN=C2SCC#N)COC3=CC=CC=C3',
                                     'name': '2-[[5-(phenoxymethyl)-4-phenyl-1,2,4-triazol-3-yl]thio]acetonitrile',
                                     'reason': 'No phenylpropane backbone '
                                               'found'},
                                 {   'smiles': 'CC1(C)CC[C@@]2(CC[C@]3(C)C(=CC[C@@H]4[C@@]5(C)CC[C@H](O)C(C)(C)[C@@H]5CC[C@@]34C)[C@@H]2C1)C([O-])=O',
                                     'name': 'oleanolate',
                                     'reason': 'No aromatic benzene ring '
                                               'found'},
                                 {   'smiles': 'CC(C)(O)[C@H]1CC[C@@]2(C)[C@H]1CC[C@]1(CO)[C@@H]2C[C@@H](O)[C@@H]2[C@@]3(C)CCCC(C)(C)[C@@H]3[C@H](O)C[C@@]12C',
                                     'name': 'hopane-6beta,11alpha,22,27-tetraol',
                                     'reason': 'No aromatic benzene ring '
                                               'found'},
                                 {   'smiles': 'O1C2=C(CC=C(C)C)C(O)=CC(O)=C2C(=O)C=C1C3=CC(OC)=C(O)C(OC)=C3',
                                     'name': 'Baohuosu',
                                     'reason': 'No phenylpropane backbone '
                                               'found'},
                                 {   'smiles': 'C1CN(CCC1NC2=NC(=NC3=CC=CC=C32)C4=CC=CC=C4)CC5=CC=CC=C5',
                                     'name': '2-phenyl-N-[1-(phenylmethyl)-4-piperidinyl]-4-quinazolinamine',
                                     'reason': 'No phenylpropane backbone '
                                               'found'},
                                 {   'smiles': 'O(CCCCCCCCCCCCCCCCCC)C[C@@H](OC(=O)CCCCCCCCCCCCCC)COC(=O)CCCC/C=C\\C/C=C\\C/C=C\\CCCCC',
                                     'name': '(2R)-3-(Octadecyloxy)-2-(pentadecanoyloxy)propyl '
                                             '(6Z,9Z,12Z)-octadeca-6,9,12-trienoate',
                                     'reason': 'No aromatic benzene ring '
                                               'found'}],
    'sample_false_negatives': [   {   'smiles': 'O1[C@@H]([C@@H](O)[C@H](O)[C@@H](O)[C@@H]1OC2=C(OC)C=C3C(OC=C(C3=O)C4=CC=C(OC)C=C4)=C2)CO',
                                      'name': 'Wistin',
                                      'reason': 'No phenylpropane backbone '
                                                'found'},
                                  {   'smiles': 'CCNc1ccc2c(cc(=O)oc2c1)C(F)(F)F',
                                      'name': 'coumarin 500',
                                      'reason': 'No phenylpropane backbone '
                                                'found'},
                                  {   'smiles': 'CC=1C=2C(=CC(=C(C2)OCC(O)=O)O)OC(C1)=O',
                                      'name': 'metesculetol',
                                      'reason': 'No phenylpropane backbone '
                                                'found'},
                                  {   'smiles': 'O1C2=C(C(=O)C(O)=C1C3=CC=C(O)C=C3)C(O)=CC(OC)=C2O',
                                      'name': 'Pollenitin',
                                      'reason': 'No phenylpropane backbone '
                                                'found'},
                                  {   'smiles': 'O=C1OC2=C(C=CC(=C2)O[C@@H]3OC([C@H](OC)[C@H]([C@H]3O)OC(=O)C=4NC(C)=CC4)(C)C)C(=C1NC(=O)C5=CC(=C(O)C=C5)CC=C(C)C)O',
                                      'name': 'Novclobiocin 101',
                                      'reason': 'No phenylpropane backbone '
                                                'found'},
                                  {   'smiles': 'O([C@@H]1[C@]2(C([C@@](C1)(CC2)[H])(C)C)C)C(=O)/C=C/C3=CC=C(O)C=C3',
                                      'name': '(1R,4R)-1,7,7-Trimethylbicyclo[2.2.1]heptane-2beta-ol '
                                              '3-(4-hydroxyphenyl)acrylate',
                                      'reason': 'No phenylpropane backbone '
                                                'found'},
                                  {   'smiles': 'O(CC(CNC(C)(C)C)O)C1=C2C(=C(C=C1)C)C=CC(O2)=O',
                                      'name': 'bucumolol',
                                      'reason': 'No phenylpropane backbone '
                                                'found'},
                                  {   'smiles': 'O=C(OC)/C=C/C1=CC=C(OCC=C=C)C=C1',
                                      'name': 'Eucalyptene A',
                                      'reason': 'No phenylpropane backbone '
                                                'found'},
                                  {   'smiles': 'CC(=O)NC1=C(C2=CC=CC=C2OC1=O)N',
                                      'name': 'N-(4-amino-2-oxo-1-benzopyran-3-yl)acetamide',
                                      'reason': 'No phenylpropane backbone '
                                                'found'},
                                  {   'smiles': 'COc1ccc(cc1)\\C=C(NC=O)\\C(NC=O)=C\\c1ccc(O)cc1',
                                      'name': "N,N'-((1Z,3Z)-1-(4-hydroxyphenyl)-4-(4-methoxyphenyl)buta-1,3-diene-2,3-diyl)diformamide",
                                      'reason': 'No phenylpropane backbone '
                                                'found'}],
    'attempt': 0,
    'reasoning': 'To classify chemical entities as phenylpropanoids based on '
                 'their SMILES strings, we need to identify certain structural '
                 'elements common to this class. Phenylpropanoids are '
                 'characterized by a phenylpropane backbone, which entails a '
                 'benzene ring attached to a three-carbon chain. Compounds '
                 'within this class often have additional functional groups or '
                 'extended conjugations like those found in flavonoids and '
                 'lignin precursors. The key features to identify a '
                 'phenylpropanoid may include:\n'
                 '\n'
                 '1. Aromatic ring: Usually a benzene ring is present.\n'
                 '2. Three-carbon chain: Connected to the benzene ring, '
                 'potentially as part of more complex structures like those in '
                 'flavonoids and coumarins.\n'
                 '3. Additional functional groups: Such as hydroxy, methoxy, '
                 'or carbonyl groups, which are typical in naturally occurring '
                 'phenylpropanoids.\n'
                 '\n'
                 'A potential approach in RDKit might involve:\n'
                 '- Detecting an aromatic ring (e.g., benzene).\n'
                 '- Validating the presence of a three-carbon chain connecting '
                 'to the aromatic system.\n'
                 '- Considering additional functional group patterns that are '
                 'common in phenylpropanoids.\n'
                 '\n'
                 "Let's implement this classification using RDKit in a "
                 'function named `is_phenylpropanoid`.',
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 1280,
    'num_false_positives': 12479,
    'num_true_negatives': 127380,
    'num_false_negatives': 1161,
    'num_negatives': None,
    'precision': 0.09303001671633113,
    'recall': 0.5243752560426055,
    'f1': 0.1580246913580247,
    'accuracy': 0.9041461700632467,
    'negative_predictive_value': 0.9909678623941}